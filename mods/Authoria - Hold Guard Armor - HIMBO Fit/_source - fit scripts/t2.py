import sys, os, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from gnif import GNif
D = sys.argv[1]
ref = None
for h in ['White', 'Dawn', 'Folk', 'Mark', 'Mort', 'Rift', 'Sol', 'Wind', 'Winter']:
    g0 = GNif(os.path.join(D, 'Cuirass%sM_0.nif' % h)); g1 = GNif(os.path.join(D, 'Cuirass%sM_0.nif' % h))
    row = []
    for s0, s1 in zip(g0.shapes, g1.shapes):
        P0 = g0.positions(s0); P1 = g1.positions(s1)
        dd = np.linalg.norm(P0 - P1, axis=1).max() if len(P0) == len(P1) else -1
        tex = None
        hsh = hashlib.md5(np.round(P1, 3).tobytes() + s1.tris.tobytes()).hexdigest()[:6]
        row.append('%s:%d:%s:%.2f' % (s1.name[-4:], len(P1), hsh, dd))
    print(h, len(g1.shapes), ' '.join(row))
