"""Read-only check: confirm the DEPLOYED head nif has the bib pinned
(zero Head weight at/below Z 112.5, ramp to full by 116.25). Reads the
partition arrays (what the renderer uses), not NiSkinData."""
import sys, struct
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad')
from nifparse import Nif, load_mesh

HEAD = r"C:/1. AUTHORIA/mods/Authoria - Fix - UBE Neck Seam/meshes/!UBE/Head/FemaleHead_tangent.nif"

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
    return {'parts': parts}

nif = Nif(HEAD)
_, hs = load_mesh(HEAD)
h = next(s for s in hs if s['name'] == 'FemaleHead')
pos = np.array(h['positions'], np.float32)
for i in range(nif.num_blocks):
    if nif.btype(i) == 'BSDynamicTriShape':
        sh = nif.parse_shape(i)
        si = nif.parse_skin_instance(sh['skin_ref'])
        pl = walk_partition(nif, si['partition_ref'])
        inst = si['bone_names']
        break

hw = {}
for p in pl['parts']:
    if p['w_off'] is None or p['bi_off'] is None: continue
    names = [inst[b] for b in p['bones']]
    for lk, gv in enumerate(p['vertex_map']):
        if gv in hw: continue
        w = 0.0
        for s in range(p['nwpv']):
            wt = struct.unpack_from('<f', nif.data, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
            b = nif.data[p['bi_off'] + p['nwpv'] * lk + s]
            if b < len(names) and names[b] == 'NPC Head [Head]': w += wt
        hw[gv] = w

bands = [('bottom (Z<=112.5) — must be 0', lambda z: z <= 112.5),
         ('ramp (112.5-116.25)', lambda z: 112.5 < z < 116.25),
         ('above 116.25 — full head', lambda z: z >= 116.25)]
for label, f in bands:
    vs = [hw[vi] for vi in range(len(pos)) if f(pos[vi][2])]
    print('%-36s n=%5d  Head weight max=%.4f mean=%.4f' % (label, len(vs), max(vs), sum(vs) / len(vs)))
