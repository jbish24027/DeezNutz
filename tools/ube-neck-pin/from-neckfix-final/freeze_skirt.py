"""Freeze the UBE head neck-skirt in expression + chargen morphs.

Writes override copies into 'Authoria - Fix - UBE Neck Seam' (originals untouched).
Skirt deltas scaled by ramp(z): 0 for z<=114.5 (frozen), 1 from z>=116.25 (face free).
Excluded: SkinnyMorph (weight pairing) and any morph X paired with a body 'X__HEAD>' TRIP morph.
"""
import os, struct, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad')
from headtri import parse

SRC = r"C:/1. AUTHORIA/mods/Ultimate Body Enhancer/meshes/!UBE/Head/"
DST = r"C:/1. AUTHORIA/mods/Authoria - Fix - UBE Neck Seam/meshes/!UBE/Head/"
Z_FREEZE, Z_FREE = 114.5, 116.25

# body-paired head morph names: body TRIP morphs named 'X__HEAD>' pair with head morph 'X'
paired = set()
d = open(r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent.tri", 'rb').read()
o = 6
nshapes = struct.unpack_from('<H', d, 4)[0]
o = 6
for _ in range(nshapes):
    ln = d[o]; o += 1; o += ln
    nm = struct.unpack_from('<H', d, o)[0]; o += 2
    for _m in range(nm):
        ml = d[o]; o += 1
        name = d[o:o+ml].decode('ascii', 'replace'); o += ml
        o += 4
        nd = struct.unpack_from('<H', d, o)[0]; o += 2 + nd * 8
        if name.endswith('__HEAD>'):
            paired.add(name[:-len('__HEAD>')])
print('body-paired head morph names (excluded):', sorted(paired))
EXCLUDE = paired | {'SkinnyMorph'}

def ramp(z):
    if z <= Z_FREEZE: return 0.0
    if z >= Z_FREE: return 1.0
    t = (z - Z_FREEZE) / (Z_FREE - Z_FREEZE)
    return t * t * (3 - 2 * t)

os.makedirs(DST, exist_ok=True)
for fn in ('FemaleHead.tri', 'FemaleHeadCharGen.tri'):
    data, nv, verts, recs = parse(SRC + fn)
    buf = bytearray(data)
    factors = [ramp(v[2]) for v in verts]
    touched_verts = sum(1 for f in factors if f < 1.0)
    changed = 0
    frozen_morphs = 0
    for off, name, so, do in recs:
        if name in EXCLUDE:
            continue
        any_change = False
        for i, f in enumerate(factors):
            if f >= 1.0: continue
            p = do + i * 6
            dx, dy, dz = struct.unpack_from('<3h', buf, p)
            if dx or dy or dz:
                ndx, ndy, ndz = int(round(dx*f)), int(round(dy*f)), int(round(dz*f))
                if (ndx, ndy, ndz) != (dx, dy, dz):
                    struct.pack_into('<3h', buf, p, ndx, ndy, ndz)
                    changed += 1
                    any_change = True
        if any_change: frozen_morphs += 1
    out = DST + fn
    open(out, 'wb').write(bytes(buf))
    print('%s: %d morphs frozen in skirt (%d deltas), %d verts in freeze/taper zone -> %s' % (
        fn, frozen_morphs, changed, touched_verts, out))
    # verify: reparse the written file, confirm skirt movement ~0 for non-excluded morphs
    d2, nv2, verts2, recs2 = parse(out)
    worst = ('', 0.0)
    for off, name, so, do in recs2:
        if name in EXCLUDE: continue
        scale = struct.unpack_from('<f', d2, so)[0]
        for i, v in enumerate(verts2):
            if v[2] < Z_FREEZE:
                dx, dy, dz = struct.unpack_from('<3h', d2, do + i * 6)
                m = (dx*dx+dy*dy+dz*dz) ** 0.5 * scale
                if m > worst[1]: worst = (name, m)
    print('  verify: max residual skirt move in frozen zone = %.4f (%s)' % (worst[1], worst[0]))
