"""Universal neck pin: apply the bib profile (Head weight -> 0 at Z<=112.5,
smoothstep to full by 116.25, removed mass -> Spine2) to EVERY skinned shape in
the enabled !UBE mesh trees plus the UBE NPC FaceGen heads.

Safety gate: a shape is only touched if it still has Head weight > 0.01 on a
vert at Z<=112.5 (read from PARTITION arrays). Already-pinned shapes read zero
there and are skipped, so the pass is safe to re-run (no ramp double-scaling).

Exclusions: hair/wig/scalp/beard/brow/lash shapes (must follow the head);
FaceGen dirs only touch 11498-vert UBE head shapes.
"""
import os, sys, struct, shutil, re
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh
from weld_taper import f16_encode

BK = r"C:/1. AUTHORIA/backups/bodypin2-20260731"
MODS_ROOT = r"C:/1. AUTHORIA/mods"
UBE_TREES = [
    "Authoria - Bodyslide Output - UBE",
    "Authoria - UBE Converter Output",
    "DDV - Hal's casual outfit - UBE",
    "Fuse00 - Thalmor Investigator UBE",
    "DD - Sigrin Silver Fox armor by Vergi UBE",
    "Ultimate Body Enhancer",
    "Authoria - Bodyslide Output - NSFW",
    "Arcane Mage Armor UBE",
    "Caenarvon's Cosplay Pack - UBE",
    "Dark Apprentice - UBE SMP",
    "Fuse00 - Scout Armor UBE",
    "Nirn Necessities - UBE patch",
    "Russian Bear - Sand Snake Armor - UBE",
    "SmolSaltLemon - Wine Duchess UBE",
    "Traveler's Armor Pack - Visually Upgradeable Outfit - UBE",
    "UBE Serana - NPC Replacer",
    "UBE Lydia - NPC Replacer",
    "Ultimate Body Enhancer - DF - Humanoid Asset Pack",
    "houseCARL - Authoria - Fix - Corsican Raider UBE Meshes",
]
FACEGEN_DIRS = [
    MODS_ROOT + "/UBE Serana - NPC Replacer/meshes/actors/Character/FaceGenData/FaceGeom",
    MODS_ROOT + "/UBE Lydia - NPC Replacer/Meshes/Actors/Character/FaceGenData/FaceGeom",
]
HEAD_VCOUNT = 11498
EXCL_SHAPE = re.compile(r'hair|wig|scalp|beard|brow|lash', re.I)
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
        p['nwpv'] = nwpv; p['nt'] = nt
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
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'parts': parts}

def h2f(hv):
    s = (hv >> 15) & 1; e = (hv >> 10) & 0x1F; m = hv & 0x3FF
    v = (m / 1024.0 * 2 ** -14) if e == 0 else ((1 + m / 1024.0) * 2 ** (e - 15) if e < 31 else 0.0)
    return -v if s else v

def locate_skin_off(data, pl, nverts):
    if pl['vbuf_off'] is None: return None
    vs = pl['vsize']
    samples = list(range(0, nverts, max(1, nverts // 30)))[:30]
    best = None
    for cand in range(0, vs - 11, 2):
        ok = 0
        for gv in samples:
            base = pl['vbuf_off'] + gv * vs + cand
            ws = [h2f(struct.unpack_from('<H', data, base + 2 * k)[0]) for k in range(4)]
            tot = sum(ws)
            if 0.95 < tot < 1.05 and all(-0.01 <= w <= 1.01 for w in ws): ok += 1
        if best is None or ok > best[1]: best = (cand, ok)
    return best[0] if best and best[1] >= len(samples) * 0.95 else None

def read_vert_weights(data, p, names, lk):
    d = {}
    for s in range(p['nwpv']):
        w = struct.unpack_from('<f', data, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
        b = data[p['bi_off'] + p['nwpv'] * lk + s]
        if w > 0 and b < len(names): d[names[b]] = d.get(names[b], 0.0) + w
    return d

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
warn = []
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
    for i in range(nif.num_blocks):
        if nif.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
        try:
            s2 = nif.parse_shape(i)
            if s2['skin_ref'] < 0: continue
            si = nif.parse_skin_instance(s2['skin_ref'])
            pl = walk_partition(nif, si['partition_ref'])
            nverts = max((max(p['vertex_map']) + 1 if p['vertex_map'] else 0) for p in pl['parts'])
            # pair with a load_mesh entry for positions
            sh = next((s for s in shape_pool if s['name'] == s2['name']
                       and s.get('positions') is not None and len(s['positions']) == nverts), None)
            if sh is None: continue
            shape_pool.remove(sh)
            if is_facegen and nverts != HEAD_VCOUNT: continue
            if EXCL_SHAPE.search(s2['name'] or ''):
                notes.append('skip-excluded:%s' % s2['name']); continue
            inst = si['bone_names']
            if 'NPC Head [Head]' not in inst: continue
            pos = np.array(sh['positions'], np.float32)
            vert_part = {}
            for pidx, p in enumerate(pl['parts']):
                for lk, gv in enumerate(p['vertex_map']):
                    vert_part.setdefault(gv, (pidx, lk))
            # GATE: unpinned bottom verts present?
            gate = False
            band = np.where(pos[:, 2] <= ZLO)[0]
            for vi in band:
                got = vert_part.get(int(vi))
                if got is None: continue
                pidx, lk = got
                p = pl['parts'][pidx]
                if p['w_off'] is None or p['bi_off'] is None: continue
                names = [inst[b] for b in p['bones']]
                if read_vert_weights(nif.data, p, names, lk).get('NPC Head [Head]', 0.0) > 0.01:
                    gate = True; break
            if not gate: continue
            skin_off = locate_skin_off(nif.data, pl, nverts)
            changed = 0
            headmax = 0.0
            below = np.where(pos[:, 2] < ZHI)[0]
            for vi in below:
                vi = int(vi)
                got = vert_part.get(vi)
                if got is None: continue
                pidx, lk = got
                p = pl['parts'][pidx]
                if p['w_off'] is None or p['bi_off'] is None: continue
                names = [inst[b] for b in p['bones']]
                cur = read_vert_weights(buf, p, names, lk)
                wh = cur.get('NPC Head [Head]', 0.0)
                if wh <= 0.001: continue
                s_ = scale_factor(pos[vi][2])
                if s_ >= 0.999: continue
                if pos[vi][2] <= ZLO: headmax = max(headmax, wh)
                recv = next((b for b in FALLBACK if b in names), None)
                if recv is None:
                    notes.append('skip-noreceiver:%s' % s2['name']); break
                moved = wh * (1 - s_)
                cur['NPC Head [Head]'] = wh - moved
                cur[recv] = cur.get(recv, 0.0) + moved
                top = sorted(cur.items(), key=lambda kv: -kv[1])[:p['nwpv']]
                tot = sum(w for _b, w in top)
                slots = [(names.index(bn), w / tot) for bn, w in top]
                while len(slots) < p['nwpv']: slots.append((slots[0][0], 0.0))
                for s_i, (bidx, w) in enumerate(slots):
                    struct.pack_into('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s_i), w)
                    struct.pack_into('<B', buf, p['bi_off'] + p['nwpv'] * lk + s_i, bidx)
                if skin_off is not None:
                    base2 = pl['vbuf_off'] + vi * pl['vsize'] + skin_off
                    for s_i, (bidx, w) in enumerate(slots[:4]):
                        struct.pack_into('<H', buf, base2 + 2 * s_i, f16_encode(w))
                        struct.pack_into('<B', buf, base2 + 8 + s_i, bidx)
                changed += 1
            if changed:
                total += changed
                notes.append('%s:%d' % (s2['name'], changed))
                if headmax > 0.5:
                    warn.append('%s | %s headmax=%.2f' % (os.path.relpath(path, MODS_ROOT), s2['name'], headmax))
        except Exception as e:
            notes.append('ERR:%s:%s' % (s2['name'] if 's2' in dir() else '?', e))
            continue
    if total == 0:
        skips = [n for n in notes if n.startswith(('skip-', 'ERR'))]
        if skips:
            print('  SKIPPED %-88s %s' % (os.path.relpath(path, MODS_ROOT), '; '.join(skips)))
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

print('\npinned: %d files | failed (untouched): %d' % (done, failed))
if warn:
    print('\nshapes that had DOMINANT head weight below Z112.5 (review these):')
    for w in warn: print('  ' + w)
