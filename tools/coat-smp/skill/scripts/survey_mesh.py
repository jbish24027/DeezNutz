"""Survey an armour mesh before writing a design file: what each shape is made of and which numbers the design needs.

usage:  python survey_mesh.py <mesh_1.nif>
        python survey_mesh.py --osp <project.osp> --set "<slider set name>"      (a BodySlide project's ShapeData mesh)

Prints, per shape: points / triangles / height range / diffuse texture / moving (non-skeleton) bones; per welded
component (pieces joined by shared points, UV seams welded) its size, height range, angle round the body (0 = front,
+90 = the actor's right, 180 = back) and moving-weight share; for big components below the chest, their texture islands
(the units the 'islands' piece selector uses) with an 'outward' fraction: the share of its triangles facing away from
the body axis - ~1 = an outer surface, ~0 = a lining / inner wall, ~0.5 = a double-walled piece or a strap edge.
For shapes whose bottom edge lies between z 55 and 85 (belt bands, cuirass hems): their LOWER EDGE per 45-degree
sector - the lowest of these over the skirt's top is where the skirt starts to swing (the design's sk_belt).
Flags: no texture = an old collision body / hidden part (usually 'drop'); moving bones = the shape already carries a
physics rig (the builder folds bones it does not know into the pelvis and writes a new HDT link - the old XML is then
unused). Also: the HDT XML the mesh links now, and whether _0 and _1 have the same topology.
The gap between the skirt lining and the trousers, slits and free share are measured by the first build (read its log).
Coordinates: Skyrim units, z up (ground 0, pelvis ~68, knee ~33), +y = the actor's front."""
import os, sys, re
import numpy as np
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smpkit
C = smpkit.init()


def islands(tris, n):
    par = list(range(n))

    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for t in tris:
        for a, b in ((t[0], t[1]), (t[1], t[2])):
            ra, rb = f(int(a)), f(int(b))
            if ra != rb: par[ra] = rb
    return np.array([f(i) for i in range(n)])


def ang(q, cx, cy): return float(np.degrees(np.arctan2(q[:, 0].mean() - cx, q[:, 1].mean() - cy)))


def outward(P, tris, cx, cy):
    fn = np.cross(P[tris[:, 1]] - P[tris[:, 0]], P[tris[:, 2]] - P[tris[:, 0]]); cc = P[tris].mean(1)
    return float(((fn[:, :2] * (cc[:, :2] - [cx, cy])).sum(1) > 0).mean()) if len(tris) else 0.0


def moving(t, idx):
    return float(np.mean([sum(x for b, x in t.w[i].items() if not C.is_skel(b)) for i in idx])) if len(idx) else 0.0


def survey(path, label):
    n, T = C.load(path); C.to_world(T)
    try: hdt = [e.string_data for e in n.root.extra_data() if 'HDT' in (e.name or '')]
    except Exception: hdt = '?'
    allp = np.vstack([t.pos for t in T if len(t.pos)])
    band = allp[(allp[:, 2] > 60) & (allp[:, 2] < 75)]
    cx, cy = (band[:, 0].mean(), band[:, 1].mean()) if len(band) else (0.0, 0.0)
    print(f'##### {label}: {path}\n  HDT link: {hdt or "none"}; body axis at hip height ({cx:.2f}, {cy:.2f})')
    for t in T:
        mv = sorted({b for w in t.w for b, x in w.items() if x > 0.01 and not C.is_skel(b)})
        tex = t.tex[0].split('\\')[-1] if t.tex and t.tex[0] else '-'
        z = (t.pos[:, 2].min(), t.pos[:, 2].max()) if len(t.pos) else (0, 0)
        print(f'  {t.name:28s} {len(t.pos):6d} pts {len(t.tris):6d} tris z {z[0]:6.1f}..{z[1]:6.1f}  tex {tex:28s} '
              f'bones {len(t.s2b):3d}, moving {len(mv)}' + (f' e.g. {mv[:3]}' if mv else '') +
              ('   <- no texture: collision body / hidden part?' if tex == '-' else '') +
              ('   <- already rigged' if mv else ''))
        if len(t.pos) and 55.0 <= z[0] <= 85.0:
            a = np.degrees(np.arctan2(t.pos[:, 0] - cx, t.pos[:, 1] - cy))
            edge = []
            for lo in range(-180, 180, 45):
                m = (a >= lo - 22.5) & (a < lo + 22.5) if lo != -180 else (np.abs(a) >= 157.5)
                edge.append(f'{lo if lo != -180 else 180:4d}:{t.pos[m, 2].min():5.1f}' if m.any() else f'{lo:4d}:  -  ')
            print('      lower edge by angle (deg:z, 0 = front, 90 = right): ' + ' '.join(edge))
        if not len(t.tris) or z[0] > 85: continue
        lab = C.welded_components(t.pos, t.tris)
        rows = []
        for k in range(lab.max() + 1):
            idx = np.where(lab == k)[0]; q = t.pos[idx]
            if len(q) < 6: continue
            rows.append((k, len(q), q[:, 2].min(), q[:, 2].max(), ang(q, cx, cy), moving(t, idx)))
        for k, m, z0, z1, a, mvs in rows[:30]:
            print(f'      comp {k:3d}: {m:6d} pts z {z0:6.1f}..{z1:6.1f} at {a:5.0f} deg; moving share {mvs:.2f}')
        if len(rows) > 30: print(f'      ... {len(rows) - 30} more components')
        isl = islands(t.tris, len(t.pos))
        for k, m, z0, z1, a, mvs in rows[:3]:
            if z0 > 72 or m < 200: continue
            print(f'      texture islands of comp {k} (for an "islands" selector: {{island id: size}}):')
            ids = sorted(set(isl[lab == k].tolist()), key=lambda r: -int(((isl == r) & (lab == k)).sum()))
            for r in ids[:20]:
                msk = (isl == r) & (lab == k); q = t.pos[msk]
                if msk.sum() < 6: continue
                tm = msk[t.tris].all(1)
                print(f'         island {r:6d}: {int(msk.sum()):5d} pts z {q[:, 2].min():6.1f}..{q[:, 2].max():6.1f} at {ang(q, cx, cy):5.0f} deg, '
                      f'outward {outward(t.pos, t.tris[tm], cx, cy):.2f}')
    return [(t.name, len(t.pos), len(t.tris)) for t in T]


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    if a[0] == '--osp':
        osp, setname = a[1], a[a.index('--set') + 1]
        ss = next((s for s in ET.parse(osp).getroot().findall('SliderSet') if s.get('name') == setname), None)
        if ss is None:
            print('sets in this project:'); [print('  ', s.get('name')) for s in ET.parse(osp).getroot().findall('SliderSet')]; sys.exit(1)
        root = os.path.dirname(os.path.dirname(osp))
        path = os.path.join(root, 'ShapeData', ss.findtext('DataFolder'), ss.findtext('SourceFile'))
        print('osp shapes:', [(s.text, s.get('target')) for s in ss.findall('Shape')])
        survey(path, f'BodySlide set "{setname}"')
    else:
        sig = survey(a[0], 'mesh')
        other = re.sub(r'_1\.nif$', '_0.nif', a[0], flags=re.I)
        if other != a[0] and os.path.exists(other):
            n0, T0 = C.load(other)
            sig0 = [(t.name, len(t.pos), len(t.tris)) for t in T0]
            print(f'  _0 vs _1 topology: {"identical" if sig0 == sig else "DIFFERENT - " + str([x for x in sig0 if x not in sig])}')
