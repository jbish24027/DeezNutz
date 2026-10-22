import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from refbody import *
from scipy_free_kd import nearest
from worldpos import world_skel
D = sys.argv[1]
for w in '01':
    g = GNif(os.path.join(D, 'CuirassWhiteM_%s.nif' % w))
    s = [x for x in g.shapes if x.name == 'SteelMaleBody'][0]
    P, _, _ = world_skel(g, s)
    for vw in '01':
        _, _, Q = load_world(os.path.join(VAN, 'malebody_%s.nif' % vw), 'MaleUnderwearBody:0')
        d, _ = nearest(P, Q)
        print('armor _%s SteelMaleBody -> vanilla body _%s: mean %.3f p95 %.3f' % (w, vw, d.mean(), np.percentile(d, 95)))
