"""Histogram of the currently-pinned head verts by distance-to-body, so the
distance gate can be chosen with evidence. Read-only."""
import sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad')
from nifparse import load_mesh

HEAD_ORIG = r"C:/1. AUTHORIA/backups/neckbib2-20260731/FemaleHead_tangent.nif"
BODY = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"

h = next(s for s in load_mesh(HEAD_ORIG)[1] if s['name'] == 'FemaleHead')
pos = np.array(h['positions'], np.float32)
bpos = np.array(load_mesh(BODY)[1][0]['positions'], np.float32)
neck = bpos[bpos[:, 2] > 104.0]

band = np.where(pos[:, 2] < 116.25)[0]          # what is pinned today
d = np.empty(len(band), np.float32)
for i in range(0, len(band), 256):
    ch = pos[band[i:i + 256]]
    d[i:i + 256] = np.sqrt(((ch[:, None, :] - neck[None, :, :]) ** 2).sum(axis=2)).min(axis=1)

print('currently pinned verts: %d' % len(band))
print('\n dist-to-body   n     Zrange        Yrange      (what it is)')
edges = [0, 0.05, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.5, 5.5, 7.0, 99]
for a, b in zip(edges, edges[1:]):
    sel = band[(d >= a) & (d < b)]
    if not len(sel): continue
    p = pos[sel]
    print('  %4.2f-%4.2f  %4d   %6.2f-%6.2f  %6.2f-%6.2f' % (
        a, b, len(sel), p[:, 2].min(), p[:, 2].max(), p[:, 1].min(), p[:, 1].max()))

# how many verts would each candidate gate free (g<0.5), and does the ring survive?
ring = band[d < 0.05]
print('\nring verts in band: %d (must stay fully locked)' % len(ring))
for D0, D1 in [(1.5, 3.5), (2.0, 4.5), (2.5, 5.0), (3.5, 5.5)]:
    freed = int(((d > (D0 + D1) / 2)).sum())
    kept = int((d <= D0).sum())
    print('  gate D0=%.1f D1=%.1f -> fully-locked-region verts=%d, mostly-freed verts=%d' % (D0, D1, kept, freed))
