import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from refbody import *
from scipy_free_kd import nearest
g, s, S, T, tris = conversion_pair()
for nm in ['malebody_1.nif', 'malebody_0.nif']:
    _, _, Q = load_world(os.path.join(VAN, nm), 'MaleUnderwearBody:0')
    d, _ = nearest(Q, S); d2, _ = nearest(Q, T)
    print('vanilla %s -> VAL base: mean %.3f p95 %.3f max %.3f | -> VAL+slider mean %.3f' % (nm, d.mean(), np.percentile(d, 95), d.max(), d2.mean()))
for nm in ['malehands_1.nif', 'malehands_0.nif', 'malefeet_1.nif', 'malefeet_0.nif']:
    _, _, Q = load_world(os.path.join(VAN, nm))
    d, _ = nearest(Q, S)
    print('vanilla %s -> VAL base: mean %.3f max %.3f' % (nm, d.mean(), d.max()))
for nm in ['malehands_1.nif', 'malehands_0.nif', 'malefeet_1.nif', 'malefeet_0.nif']:
    _, _, Q = load_world(os.path.join(BODY, nm))
    d, _ = nearest(Q, T)
    print('HIMBO %s -> VAL+slider: mean %.3f max %.3f' % (nm, d.mean(), d.max()))
_, _, H1 = load_world(os.path.join(BODY, 'malebody_1.nif')); _, _, H0 = load_world(os.path.join(BODY, 'malebody_0.nif'))
dd = np.linalg.norm(H1 - H0, axis=1); print('HIMBO 0vs1 per-vertex |d| mean %.3f max %.3f' % (dd.mean(), dd.max()))
_, _, V1 = load_world(os.path.join(VAN, 'malebody_1.nif'), 'MaleUnderwearBody:0'); _, _, V0 = load_world(os.path.join(VAN, 'malebody_0.nif'), 'MaleUnderwearBody:0')
dd = np.linalg.norm(V1 - V0, axis=1); print('vanilla 0vs1 |d| mean %.3f max %.3f' % (dd.mean(), dd.max()))
