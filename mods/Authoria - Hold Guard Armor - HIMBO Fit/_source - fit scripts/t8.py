import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from fitlib import *
from fitnif import visible_union
from gnif import GNif
from analyse import world_shapes
g0 = GNif('conv/1GuardArmor/M/GauntletsM_1.nif')
A0, T0 = visible_union(g0, world_shapes(g0))
pr = pairs(); VP, VT = pr['V']['1'][0], pr['V']['1'][1]
VN = tri_normals(VP, VT)
grid = TriGrid(A0, T0)
tp, tn = grid.raycast(VP, VN, -6, 25)
cov = (tp <= 3) | (tn >= -3)
poke = cov & ~((tp < np.inf) | (tn >= -0.1))
idx = np.where(poke)[0][:40]
# brute force
def brute(o, d):
    V0 = A0[T0[:, 0]]; V1 = A0[T0[:, 1]]; V2 = A0[T0[:, 2]]
    e1 = V1 - V0; e2 = V2 - V0; h = np.cross(d, e2); a = (e1 * h).sum(1)
    f = 1 / np.where(np.abs(a) > 1e-12, a, 1); s = o - V0; u = f * (s * h).sum(1); q = np.cross(s, e1); v = f * (q @ d); t = f * (e2 * q).sum(1)
    hit = (np.abs(a) > 1e-12) & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > -6) & (t < 25)
    return np.sort(t[hit])
for i in idx[:15]:
    print(i, np.round(VP[i], 1), 'grid tp', tp[i], 'tn', np.round(tn[i], 2), 'brute', np.round(brute(VP[i], VN[i]), 2))
print('normals sanity: mean dot(normal, p-centroid of hand)?')
