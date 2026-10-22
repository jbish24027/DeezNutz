"""Compact survey of every candidate mesh: per shape its welded components (size, z range, mean angle, SKIRT = cloth between
the legs at z 35-55, LEGS = two leg tubes with nothing between them), and for each SKIRT component its texture islands that
reach below z 72. usage: autosurvey.py candidates.json [name filter]"""
import sys, json, os
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\skill\scripts")
import smpkit
C = smpkit.init()
from coat.build_coat_rig import islands

cands = json.load(open(sys.argv[1]))
flt = sys.argv[2] if len(sys.argv) > 2 else ''
for c in cands:
    if flt not in c['path']: continue
    src = c['src']
    if not os.path.exists(src):
        print('##', c['path'], 'MISSING', src); continue
    n, T = C.load(src); C.to_world(T)
    print(f"## {c['path']}  [{c['mod']}]  {', '.join(c['eds'][:2])}")
    for t in T:
        p = t.pos
        if len(p) < 30: continue
        lab = C.welded_components(p, t.tris)
        line = []
        for k in range(lab.max() + 1):
            m = lab == k; q = p[m]
            if m.sum() < 20: continue
            between = ((q[:, 2] > 35) & (q[:, 2] < 55) & (np.abs(q[:, 0]) < 2.5) & (np.abs(q[:, 1]) > 3)).sum() >= 3
            mid = (q[:, 2] > 25) & (q[:, 2] < 50)
            legs = mid.sum() > 20 and (q[mid, 0] < -3).any() and (q[mid, 0] > 3).any() and not (np.abs(q[mid, 0]) < 1.5).any()
            a = np.degrees(np.arctan2(q[:, 0].mean(), q[:, 1].mean()))
            tag = 'SKIRT' if between else ('LEGS' if legs else '')
            line.append(f"c{k}:{int(m.sum())} z{q[:,2].min():.0f}-{q[:,2].max():.0f} a{a:.0f}{' ' + tag if tag else ''}")
        print(f"  [{t.name}] {len(p)}p: " + " | ".join(line))
        isl = None
        for k in range(lab.max() + 1):
            m = lab == k; q = p[m]
            if m.sum() < 20: continue
            if not (((q[:, 2] > 35) & (q[:, 2] < 55) & (np.abs(q[:, 0]) < 2.5) & (np.abs(q[:, 1]) > 3)).sum() >= 3): continue
            if isl is None: isl = islands(t.tris, len(p))
            out = []
            for r in sorted(set(isl[m].tolist()), key=lambda r: -int(((isl == r) & m).sum())):
                mm = (isl == r) & m; qq = p[mm]
                if qq[:, 2].min() >= 72: continue
                aa = np.degrees(np.arctan2(qq[:, 0].mean(), qq[:, 1].mean()))
                out.append(f"{r}:{int(mm.sum())} z{qq[:,2].min():.0f}-{qq[:,2].max():.0f} a{aa:.0f} x{qq[:,0].min():.0f}..{qq[:,0].max():.0f}")
            print(f"     c{k} islands<72: " + " ; ".join(out[:18]) + (f" ; +{len(out)-18} more" if len(out) > 18 else ''))
