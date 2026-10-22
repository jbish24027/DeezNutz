import sys, os, collections
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from fitlib import *
from fitnif import visible_union
from gnif import GNif
from analyse import world_shapes
a, b, w = sys.argv[1:4]
g0 = GNif(a); g1 = GNif(b)
A0, T0 = visible_union(g0, world_shapes(g0)); A1, T1 = visible_union(g1, world_shapes(g1))
res, m = poke_design(w, A0, T0, A1, T1)
print(res)
pr = pairs(); HP, HT, HW, Hb = pr['H'][w]
dom = np.array(Hb)[HW.argmax(1)]
for k in ('before', 'after'):
    print(k, collections.Counter(dom[m[k]]).most_common(10))
new = m['after'] & ~m['before']
print('newly poking', new.sum(), collections.Counter(dom[new]).most_common(10))
if new.sum():
    d, _ = nearest(HP[new], A1); print('dist from newly-poking skin verts to fitted armour: median %.2f p90 %.2f' % (np.median(d), np.percentile(d, 90)))
    d0, _ = nearest(HP[new], A0); print('                               to original armour: median %.2f p90 %.2f' % (np.median(d0), np.percentile(d0, 90)))
