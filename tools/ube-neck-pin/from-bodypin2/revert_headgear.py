"""Revert the rigid headgear decorations that pin_all wrongly pinned:
 - FalmerSlayerFaceguard.nif: restore file from backup, re-pin ONLY FemaleHead
 - FalmerSlayerHelmet.nif:    restore file from backup, re-pin FemaleHead + ThalmorHoodF.002
 - MiraakSkeleton.nif:        full restore (only the rigid helm was pinned)
Verification: per-file re-read confirms decoration weights byte-match the backup
and kept shapes match the pre-revert pinned state."""
import os, sys, struct, shutil
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh
from weld_taper import f16_encode

MODS = r"C:/1. AUTHORIA/mods"
BK = r"C:/1. AUTHORIA/backups/bodypin2-20260731"
ZLO, ZHI = 112.5, 116.25
FALLBACK = ['NPC Spine2 [Spn2]', 'NPC Spine1 [Spn1]', 'NPC Spine [Spn0]',
            'NPC L Clavicle [LClv]', 'NPC R Clavicle [RClv]']

JOBS = [
    (r"Authoria - Bodyslide Output - UBE\meshes\!UBE\falmerslayer\FalmerSlayerFaceguard.nif", ['FemaleHead']),
    (r"Authoria - Bodyslide Output - UBE\meshes\!UBE\falmerslayer\FalmerSlayerHelmet.nif", ['FemaleHead', 'ThalmorHoodF.002']),
    (r"Authoria - UBE Converter Output\meshes\!UBE\DLC02\Effects\MiraakSkeleton.nif", []),
]

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

for rel, keep in JOBS:
    live = os.path.join(MODS, rel)
    bak = os.path.join(BK, rel)
    assert os.path.exists(bak), 'missing backup: ' + bak
    shutil.copy2(bak, live)
    if not keep:
        print('RESTORED (full): %s' % rel)
        continue
    nif = Nif(live)
    _, shapes = load_mesh(live)
    buf = bytearray(nif.data)
    total = 0
    for i in range(nif.num_blocks):
        if nif.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
        s2 = nif.parse_shape(i)
        if s2['name'] not in keep or s2['skin_ref'] < 0: continue
        si = nif.parse_skin_instance(s2['skin_ref'])
        pl = walk_partition(nif, si['partition_ref'])
        nverts = max((max(p['vertex_map']) + 1 if p['vertex_map'] else 0) for p in pl['parts'])
        sh = next(s for s in shapes if s['name'] == s2['name'] and s.get('positions') is not None
                  and len(s['positions']) == nverts)
        inst = si['bone_names']
        pos = np.array(sh['positions'], np.float32)
        skin_off = locate_skin_off(nif.data, pl, nverts)
        vert_part = {}
        for pidx, p in enumerate(pl['parts']):
            for lk, gv in enumerate(p['vertex_map']):
                vert_part.setdefault(gv, (pidx, lk))
        for vi in np.where(pos[:, 2] < ZHI)[0]:
            vi = int(vi)
            got = vert_part.get(vi)
            if got is None: continue
            pidx, lk = got
            p = pl['parts'][pidx]
            if p['w_off'] is None or p['bi_off'] is None: continue
            names = [inst[b] for b in p['bones']]
            cur = {}
            for s in range(p['nwpv']):
                w = struct.unpack_from('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
                b = buf[p['bi_off'] + p['nwpv'] * lk + s]
                if w > 0 and b < len(names): cur[names[b]] = cur.get(names[b], 0.0) + w
            wh = cur.get('NPC Head [Head]', 0.0)
            if wh <= 0.001: continue
            s_ = scale_factor(pos[vi][2])
            if s_ >= 0.999: continue
            recv = next((b for b in FALLBACK if b in names), None)
            if recv is None: continue
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
            total += 1
    tmp = live + '.tmp'
    open(tmp, 'wb').write(bytes(buf))
    n2 = Nif(tmp)
    _, sh2 = load_mesh(tmp)
    p_ok = all(np.array_equal(np.array(a['positions'], np.float32), np.array(b['positions'], np.float32))
               for a, b in zip(shapes, sh2) if a.get('positions') is not None and b.get('positions') is not None)
    assert p_ok, 'position check failed: ' + rel
    os.replace(tmp, live)
    print('RESTORED+REPINNED %s (kept shapes %s, %d verts pinned)' % (rel, keep, total))
print('done')
