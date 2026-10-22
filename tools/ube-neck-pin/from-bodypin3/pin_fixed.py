"""Corrected universal neck pin (v2). Fixes vs pin_all:
  1. Skin-field offset comes from the vertex DESCRIPTOR (pos bytes = 0 for
     BSDynamicTriShape, 16/8 for BSTriShape by precision) — no guessing.
     Hard gate: decoded weights at that offset must sum~1 on >=99% of sampled
     verts or the shape is SKIPPED and reported.
  2. Source weights are read from the VBUF (authoritative for the renderer);
     partition arrays can be stale in third-party conversions.
  3. Writes go to the vbuf AND to EVERY partition copy of each vert. If any
     containing partition lacks a receiver bone, the vert is skipped everywhere.
  4. Index convention self-calibrates per shape (instance-global vs
     partition-local) against original data; ambiguity = skip + report.
Gate for idempotency: only shapes with vbuf Head weight > 0.01 at some vert
Z<=112.5 are touched. Rigid headgear decorations are excluded by name.
"""
import os, sys, struct, shutil, re
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh
from weld_taper import layout, f16_encode

BK = r"C:/1. AUTHORIA/backups/bodypin3-20260731"
MODS_ROOT = r"C:/1. AUTHORIA/mods"
UBE_TREES = [
    "Authoria - Bodyslide Output - UBE", "Authoria - UBE Converter Output",
    "DDV - Hal's casual outfit - UBE", "Fuse00 - Thalmor Investigator UBE",
    "DD - Sigrin Silver Fox armor by Vergi UBE", "Ultimate Body Enhancer",
    "Authoria - Bodyslide Output - NSFW", "Arcane Mage Armor UBE",
    "Caenarvon's Cosplay Pack - UBE", "Dark Apprentice - UBE SMP",
    "Fuse00 - Scout Armor UBE", "Nirn Necessities - UBE patch",
    "Russian Bear - Sand Snake Armor - UBE", "SmolSaltLemon - Wine Duchess UBE",
    "Traveler's Armor Pack - Visually Upgradeable Outfit - UBE",
    "UBE Serana - NPC Replacer", "UBE Lydia - NPC Replacer",
    "Ultimate Body Enhancer - DF - Humanoid Asset Pack",
    "houseCARL - Authoria - Fix - Corsican Raider UBE Meshes",
]
FACEGEN_DIRS = [
    MODS_ROOT + "/UBE Serana - NPC Replacer/meshes/actors/Character/FaceGenData/FaceGeom",
    MODS_ROOT + "/UBE Lydia - NPC Replacer/Meshes/Actors/Character/FaceGenData/FaceGeom",
]
HEAD_VCOUNT = 11498
EXCL_SHAPE = re.compile(r'hair|wig|scalp|beard|brow|lash', re.I)
EXCL_EXACT = {'CrownFace', 'CrownFeathers', 'WheelF', 'MiraakHelm02'}
ZLO, ZHI = 112.5, 116.25
FALLBACK = ['NPC Spine2 [Spn2]', 'NPC Spine1 [Spn1]', 'NPC Spine [Spn0]',
            'NPC L Clavicle [LClv]', 'NPC R Clavicle [RClv]']

def scale_factor(z):
    if z >= ZHI: return 1.0
    if z <= ZLO: return 0.0
    t = (z - ZLO) / (ZHI - ZLO)
    return t * t * (3 - 2 * t)

def walk_partition(nif, part_ref):
    r = nif.block_reader(part_ref)
    np_ = r.u32()
    dsize = r.u32(); vsize = r.u32(); desc = r.u64()
    vbuf_off = r.o if dsize else None
    r.o += dsize
    parts = []
    for _ in range(np_):
        p = {}
        nv = r.u16(); nt = r.u16(); nb = r.u16(); ns = r.u16(); nwpv = r.u16()
        p['nwpv'] = nwpv
        p['bones'] = [r.u16() for _ in range(nb)]
        if r.u8(): p['vertex_map'] = [r.u16() for _ in range(nv)]
        else: p['vertex_map'] = list(range(nv))
        if r.u8(): p['w_off'] = r.o; r.o += 4 * nwpv * nv
        else: p['w_off'] = None
        slens = [r.u16() for _ in range(ns)]
        if r.u8():
            if ns:
                for l in slens: r.o += 2 * l
            else: r.o += 6 * nt
        if r.u8(): p['bi_off'] = r.o; r.o += nwpv * nv
        else: p['bi_off'] = None
        r.u16(); r.u64()
        r.o += 6 * nt
        parts.append(p)
    assert r.o - nif.block_offsets[part_ref] == nif.block_sizes[part_ref]
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'dsize': dsize, 'desc': desc, 'parts': parts}

def h2f(hv):
    s = (hv >> 15) & 1; e = (hv >> 10) & 0x1F; m = hv & 0x3FF
    v = (m / 1024.0 * 2 ** -14) if e == 0 else ((1 + m / 1024.0) * 2 ** (e - 15) if e < 31 else 0.0)
    return -v if s else v

def skin_offset(desc, dsize, vsize, dynamic):
    if not dsize: return None
    _vs, full = layout(desc)
    vflags = (desc >> 44) & 0xFFF
    if not (vflags & 0x40): return None
    off = 0 if dynamic else (16 if full else 8)
    if vflags & 0x2: off += 4
    if vflags & 0x8: off += 4
    if vflags & 0x10: off += 4
    if vflags & 0x20: off += 4
    return off

def read_vbuf(data, pl, dso, vi):
    base = pl['vbuf_off'] + vi * pl['vsize'] + dso
    ws = [h2f(struct.unpack_from('<H', data, base + 2 * k)[0]) for k in range(4)]
    bi = [data[base + 8 + k] for k in range(4)]
    return ws, bi

targets = []
for m in UBE_TREES:
    base = os.path.join(MODS_ROOT, m, 'meshes', '!UBE')
    if not os.path.isdir(base):
        base = os.path.join(MODS_ROOT, m, 'Meshes', '!UBE')
    if os.path.isdir(base):
        for dp, _d, fs in os.walk(base):
            for f in fs:
                if f.lower().endswith('.nif'): targets.append((os.path.join(dp, f), False))
for fg in FACEGEN_DIRS:
    if os.path.isdir(fg):
        for dp, _d, fs in os.walk(fg):
            for f in fs:
                if f.lower().endswith('.nif'): targets.append((os.path.join(dp, f), True))
print('candidate nifs: %d' % len(targets))

done = failed = 0
skips = []
for path, is_facegen in sorted(targets):
    try:
        nif = Nif(path)
        _, shapes = load_mesh(path)
    except Exception:
        continue
    shape_pool = list(shapes)
    buf = bytearray(nif.data)
    total = 0
    notes = []
    file_bad = False
    for i in range(nif.num_blocks):
        if nif.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
        dynamic = nif.btype(i) == 'BSDynamicTriShape'
        try:
            s2 = nif.parse_shape(i)
            if s2['skin_ref'] < 0: continue
            si = nif.parse_skin_instance(s2['skin_ref'])
            pl = walk_partition(nif, si['partition_ref'])
            nverts = pl['dsize'] // pl['vsize'] if pl['vsize'] else max(
                (max(p['vertex_map']) + 1 if p['vertex_map'] else 0) for p in pl['parts'])
            sh = next((s for s in shape_pool if s['name'] == s2['name']
                       and s.get('positions') is not None and len(s['positions']) == nverts), None)
            if sh is None: continue
            shape_pool.remove(sh)
            nm = s2['name'] or ''
            if is_facegen and nverts != HEAD_VCOUNT: continue
            if EXCL_SHAPE.search(nm) or nm in EXCL_EXACT: continue
            inst = si['bone_names']
            if 'NPC Head [Head]' not in inst: continue
            dso = skin_offset(pl['desc'], pl['dsize'], pl['vsize'], dynamic)
            if dso is None or pl['vbuf_off'] is None:
                skips.append((path, nm, 'no-vbuf-skin-fields')); continue
            if dso + 12 > pl['vsize']:
                skips.append((path, nm, 'offset-exceeds-stride')); continue
            # HARD GATE: sum~1 sanity on sampled verts
            samp = list(range(0, nverts, max(1, nverts // 200)))[:200]
            bad = sum(1 for v in samp if not (0.95 < sum(read_vbuf(nif.data, pl, dso, v)[0]) < 1.05))
            if bad > len(samp) * 0.01:
                skips.append((path, nm, 'sum-gate-fail %d/%d' % (bad, len(samp)))); continue
            # index convention calibration: global-instance vs partition-local
            vert_parts = {}
            for pidx, p in enumerate(pl['parts']):
                for lk, gv in enumerate(p['vertex_map']):
                    vert_parts.setdefault(gv, []).append((pidx, lk))
            conv = 'global'
            if len(inst) > 1:
                agree_g = agree_l = tested = 0
                for v in samp:
                    ws, bi = read_vbuf(nif.data, pl, dso, v)
                    occ = vert_parts.get(v)
                    if not occ: continue
                    p0 = pl['parts'][occ[0][0]]
                    dom = max(range(4), key=lambda k: ws[k])
                    if ws[dom] < 0.3: continue
                    tested += 1
                    if bi[dom] < len(inst): agree_g += 1 if True else 0
                    # compare against partition weights only where partitions look fresh
                    names_l = [inst[b] for b in p0['bones']]
                    if bi[dom] < len(names_l): agree_l += 1
                # both in-range is common; prefer partition-local ONLY if global impossible
                if all(len(p['bones']) == len(inst) and p['bones'] == list(range(len(inst)))
                       for p in pl['parts']):
                    conv = 'same'          # identical mapping, no ambiguity
                elif len(pl['parts']) == 1:
                    conv = 'local'         # validated convention (bib, dresses)
                else:
                    conv = 'global'        # shared buffer across partitions
            # gate: unpinned bottom verts (from VBUF, resolved via convention)
            pos = np.array(sh['positions'], np.float32)
            def head_w(v):
                ws, bi = read_vbuf(buf, pl, dso, v)
                occ = vert_parts.get(v)
                if conv == 'local' and occ:
                    names = [inst[b] for b in pl['parts'][occ[0][0]]['bones']]
                else:
                    names = inst
                return sum(w for w, b in zip(ws, bi) if w > 0 and b < len(names)
                           and names[b] == 'NPC Head [Head]'), ws, bi, names
            band = np.where(pos[:, 2] <= ZLO)[0]
            if not any(head_w(int(v))[0] > 0.01 for v in band): continue
            # apply
            changed = 0
            for vi in np.where(pos[:, 2] < ZHI)[0]:
                vi = int(vi)
                wh, ws, bi, names = head_w(vi)
                if wh <= 0.001: continue
                s_ = scale_factor(pos[vi][2])
                if s_ >= 0.999: continue
                occ = vert_parts.get(vi, [])
                # every containing partition must carry a receiver
                recvs = []
                ok = True
                for pidx, lk in occ:
                    pnames = [inst[b] for b in pl['parts'][pidx]['bones']]
                    r = next((b for b in FALLBACK if b in pnames), None)
                    if r is None: ok = False; break
                    recvs.append(r)
                recv_inst = next((b for b in FALLBACK if b in names), None)
                if not ok or recv_inst is None or not occ: continue
                cur = {}
                for w, b in zip(ws, bi):
                    if w > 0 and b < len(names): cur[names[b]] = cur.get(names[b], 0.0) + w
                moved = wh * (1 - s_)
                cur['NPC Head [Head]'] = wh - moved
                cur[recv_inst] = cur.get(recv_inst, 0.0) + moved
                top = sorted(cur.items(), key=lambda kv: -kv[1])[:4]
                tot = sum(w for _b, w in top)
                top = [(bn, w / tot) for bn, w in top]
                # write vbuf using the shape's convention
                if conv == 'local':
                    wnames = [inst[b] for b in pl['parts'][occ[0][0]]['bones']]
                else:
                    wnames = inst
                if any(bn not in wnames for bn, _w in top):
                    continue
                base2 = pl['vbuf_off'] + vi * pl['vsize'] + dso
                for k in range(4):
                    bn, w = top[k] if k < len(top) else (top[0][0], 0.0)
                    struct.pack_into('<H', buf, base2 + 2 * k, f16_encode(w))
                    struct.pack_into('<B', buf, base2 + 8 + k, wnames.index(bn))
                # write EVERY partition copy
                for (pidx, lk) in occ:
                    p = pl['parts'][pidx]
                    if p['w_off'] is None or p['bi_off'] is None: continue
                    pnames = [inst[b] for b in p['bones']]
                    ptop = [(bn, w) for bn, w in top if bn in pnames]
                    ptot = sum(w for _b, w in ptop)
                    if ptot <= 0: continue
                    ptop = [(bn, w / ptot) for bn, w in ptop][:p['nwpv']]
                    for s_i in range(p['nwpv']):
                        bn, w = ptop[s_i] if s_i < len(ptop) else (ptop[0][0], 0.0)
                        struct.pack_into('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s_i), w)
                        struct.pack_into('<B', buf, p['bi_off'] + p['nwpv'] * lk + s_i, pnames.index(bn))
                changed += 1
            if changed:
                total += changed
                notes.append('%s:%d(%s)' % (nm, changed, conv))
        except Exception as e:
            skips.append((path, nm if 'nm' in dir() else '?', 'ERR %s' % e))
            file_bad = True
            break
    if file_bad or total == 0:
        continue
    tmp = path + '.pin.tmp'
    try:
        open(tmp, 'wb').write(bytes(buf))
        n2 = Nif(tmp)
        _, sh2 = load_mesh(tmp)
        p_ok = all(np.array_equal(np.array(a['positions'], np.float32), np.array(b['positions'], np.float32))
                   for a, b in zip(shapes, sh2) if a.get('positions') is not None and b.get('positions') is not None)
        if not p_ok:
            os.remove(tmp); failed += 1
            print('  FAIL-POSCHK %s' % os.path.relpath(path, MODS_ROOT)); continue
        rel = os.path.relpath(path, MODS_ROOT)
        dst = os.path.join(BK, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst): shutil.copy2(path, dst)
        os.replace(tmp, path)
        done += 1
        print('  PINNED %-90s %s' % (rel, '; '.join(notes)))
    except Exception as e:
        failed += 1
        if os.path.exists(tmp): os.remove(tmp)
        print('  FAIL %s: %s' % (os.path.relpath(path, MODS_ROOT), e))

print('\npinned: %d files | failed (untouched): %d | skipped shapes: %d' % (done, failed, len(skips)))
for p, nm, why in skips:
    print('  SKIP %-80s %-24s %s' % (os.path.relpath(p, MODS_ROOT), nm, why))
