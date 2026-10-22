import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif
from worldpos import world_skel
a, b = sys.argv[1], sys.argv[2]
g0 = GNif(a); g1 = GNif(b)
for s0, s1 in zip(g0.shapes, g1.shapes):
    if not s0.bones: continue
    P0 = world_skel(g0, s0)[0]; P1 = world_skel(g1, s1)[0]
    T = s0.tris.astype(np.int64)
    e = np.unique(np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1), axis=0)
    l0 = np.linalg.norm(P0[e[:, 0]] - P0[e[:, 1]], axis=1); l1 = np.linalg.norm(P1[e[:, 0]] - P1[e[:, 1]], axis=1)
    m = l0 > 0.05
    r = l1[m] / l0[m]; dl = np.abs(l1 - l0)[m]
    bad = (np.abs(r - 1) > 0.4) & (dl > 0.15)
    W = g0.weight_matrix(s0); dom = np.array(s0.bones)[W.argmax(1)]
    c = collections.Counter(dom[e[m][bad][:, 0]])
    print('%-14s edges %6d  |strain-1|>40%% and >0.15u: %4d (%.2f%%)  max abs length change %.2f' % (s0.name, m.sum(), bad.sum(), 100 * bad.mean(), dl.max()), c.most_common(4))
