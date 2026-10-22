"""Pin the body-side neck to the torso with the SAME profile as the bib
(zero Head weight below Z 112.5, smoothstep back to full by 116.25), so the
head-bib and every body/outfit neck transform identically. Per-file empirical
skin-offset location + verification gate; a failing file is skipped, not written."""
import os, sys, struct, shutil
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh
from weld_taper import f16_encode

BK = r"C:/1. AUTHORIA/backups/bodypin-20260731"
REF_BODY_1 = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"
REF_BODY_0 = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_0.nif"
MODS = [
    r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes",
    r"C:/1. AUTHORIA/mods/Authoria - UBE Converter Output/meshes",
    r"C:/1. AUTHORIA/mods/DDV - Hal's casual outfit - UBE/meshes",
    r"C:/1. AUTHORIA/mods/Fuse00 - Thalmor Investigator UBE/meshes",
    r"C:/1. AUTHORIA/mods/DD - Sigrin Silver Fox armor by Vergi UBE/meshes",
    r"C:/1. AUTHORIA/mods/Ultimate Body Enhancer/meshes",
]

def scale_factor(z):
    if z >= 116.25: return 1.0
    if z <= 112.5: return 0.0
    t = (z - 112.5) / (116.25 - 112.5)
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
        p['nt'] = nt; p['nwpv'] = nwpv
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
        p['tris_off'] = r.o
        r.o += 6 * nt
        parts.append(p)
    assert r.o - nif.block_offsets[part_ref] == nif.block_sizes[part_ref]
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'parts': parts}

def h2f(hv):
    s = (hv >> 15) & 1; e = (hv >> 10) & 0x1F; m = hv & 0x3FF
    v = (m / 1024.0 * 2 ** -14) if e == 0 else ((1 + m / 1024.0) * 2 ** (e - 15) if e < 31 else 0.0)
    return -v if s else v

def locate_skin_off(data, pl, samples):
    if pl['vbuf_off'] is None: return None
    vs = pl['vsize']
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

refs = [np.array(load_mesh(p)[1][0]['positions'], np.float32) for p in (REF_BODY_1, REF_BODY_0)]
ref = refs[0]
targets = []
for root in MODS:
    for dp, _d, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith('.nif'):
                targets.append(os.path.join(dp, f))
print('candidate nifs: %d' % len(targets))

done = skipped = failed = 0
for path in sorted(targets):
    try:
        nif = Nif(path)
        _, shapes = load_mesh(path)
    except Exception:
        continue
    work = []
    for sh in shapes:
        if sh.get('positions') is None or 'weight_map' not in sh: continue
        if len(sh['positions']) != len(ref): continue
        pos = np.array(sh['positions'], np.float32)
        if min(np.abs(pos[::97] - r[::97]).max() for r in refs) > 0.6: continue
        # neck verts with head weight
        neck = [vi for vi in range(len(pos))
                if pos[vi][2] < 116.25 and sh['weight_map'][vi].get('NPC Head [Head]', 0.0) > 0.001
                and scale_factor(pos[vi][2]) < 0.999]
        if neck: work.append((sh, pos, neck))
    if not work:
        continue
    buf = bytearray(nif.data)
    file_ok = True
    total = 0
    for sh, pos, neck in work:
        blk = None
        for i in range(nif.num_blocks):
            if nif.btype(i) in ('BSTriShape', 'BSDynamicTriShape'):
                s2 = nif.parse_shape(i)
                if s2['name'] != sh['name'] or s2['skin_ref'] < 0: continue
                si = nif.parse_skin_instance(s2['skin_ref'])
                r2 = nif.block_reader(si['partition_ref'])
                r2.u32(); ds2 = r2.u32(); vs2 = r2.u32()
                if vs2 and ds2 // vs2 == len(pos):
                    blk = (s2, si); break
        if blk is None: file_ok = False; break
        s2, si = blk
        pl = walk_partition(nif, si['partition_ref'])
        inst = si['bone_names']
        if 'NPC Spine2 [Spn2]' not in inst: file_ok = False; break
        skin_off = locate_skin_off(nif.data, pl, [gv for gv in range(0, len(pos), 977)][:30])
        vert_part = {}
        for pidx, p in enumerate(pl['parts']):
            for lk, gv in enumerate(p['vertex_map']):
                vert_part.setdefault(gv, (pidx, lk))
        for vi in neck:
            got = vert_part.get(vi)
            if got is None: continue
            pidx, lk = got
            p = pl['parts'][pidx]
            if p['w_off'] is None or p['bi_off'] is None: continue
            names = [inst[b] for b in p['bones']]
            if 'NPC Spine2 [Spn2]' not in names: continue
            cur = {}
            for s in range(p['nwpv']):
                w = struct.unpack_from('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
                b = buf[p['bi_off'] + p['nwpv'] * lk + s]
                if w > 0 and b < len(names): cur[names[b]] = cur.get(names[b], 0.0) + w
            wh = cur.get('NPC Head [Head]', 0.0)
            if wh <= 0.001: continue
            s_ = scale_factor(pos[vi][2])
            moved = wh * (1 - s_)
            cur['NPC Head [Head]'] = wh - moved
            cur['NPC Spine2 [Spn2]'] = cur.get('NPC Spine2 [Spn2]', 0.0) + moved
            top = sorted(cur.items(), key=lambda kv: -kv[1])[:p['nwpv']]
            tot = sum(w for _b, w in top)
            slots = [(names.index(bn), w / tot) for bn, w in top]
            while len(slots) < p['nwpv']: slots.append((slots[0][0], 0.0))
            for s_i, (bidx, w) in enumerate(slots):
                struct.pack_into('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s_i), w)
                struct.pack_into('<B', buf, p['bi_off'] + p['nwpv'] * lk + s_i, bidx)
            if skin_off is not None:
                base = pl['vbuf_off'] + vi * pl['vsize'] + skin_off
                for s_i, (bidx, w) in enumerate(slots[:4]):
                    struct.pack_into('<H', buf, base + 2 * s_i, f16_encode(w))
                    struct.pack_into('<B', buf, base + 8 + s_i, bidx)
            total += 1
    if not file_ok or total == 0:
        skipped += 1
        continue
    # verify: positions byte-identical + reparse
    try:
        tmp = path + '.bodypin.tmp'
        open(tmp, 'wb').write(bytes(buf))
        n2 = Nif(tmp)
        _, sh2 = load_mesh(tmp)
        p_ok = all(np.array_equal(np.array(a['positions'], np.float32), np.array(b['positions'], np.float32))
                   for a, b in zip(shapes, sh2) if a.get('positions') is not None and b.get('positions') is not None)
        if not p_ok:
            os.remove(tmp); failed += 1; continue
        rel = os.path.relpath(path, r"C:/1. AUTHORIA/mods")
        dst = os.path.join(BK, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst): shutil.copy2(path, dst)
        os.replace(tmp, path)
        done += 1
        print('  PINNED %-70s verts=%d' % (os.path.relpath(path, r"C:/1. AUTHORIA/mods"), total))
    except Exception:
        failed += 1
        if os.path.exists(tmp): os.remove(tmp)
print('pinned: %d files | no-body-copy/skipped: %d | verification-failed (untouched): %d' % (done, skipped, failed))
