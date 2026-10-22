import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from fitlib import *
pr = pairs()
for w in '01':
    for nm, folder, comp, filt in [('vanilla', VAN, 'V', {'MaleUnderwearBody:0'}), ('HIMBO', BODY, 'H', None)]:
        P, T, W, b = composite(folder, ['1stpersonmalebody_%s.nif' % w], filt)
        d, _ = nearest(P, pr[comp][w][0])
        print(w, nm, '1st-person body -> 3rd-person composite: mean %.3f p95 %.3f max %.3f' % (d.mean(), np.percentile(d, 95), d.max()))
d = np.linalg.norm(pr['T']['1'] - pr['S']['1'], axis=1)
P = pr['S']['1']; m = P[:, 2] > 118
print('VAL verts above z118 (head):', m.sum(), 'delta mean %.3f max %.3f' % (d[m].mean(), d[m].max()))
