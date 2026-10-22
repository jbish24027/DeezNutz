import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from fitlib import *
pr = pairs()
for w in '01':
    V = pr['V'][w][0]; H = pr['H'][w][0]
    d, _ = nearest(V, pr['S'][w]); d2, _ = nearest(H, pr['T'][w])
    print('w%s: vanilla composite -> S: mean %.3f p95 %.3f | HIMBO composite -> T: mean %.3f p95 %.3f max %.3f | |T-S| mean %.2f max %.2f' % (
        w, d.mean(), np.percentile(d, 95), d2.mean(), np.percentile(d2, 95), d2.max(), np.linalg.norm(pr['T'][w]-pr['S'][w],axis=1).mean(), np.linalg.norm(pr['T'][w]-pr['S'][w],axis=1).max()))
