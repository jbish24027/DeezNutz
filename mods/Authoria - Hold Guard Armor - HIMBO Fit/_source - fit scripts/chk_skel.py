import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from gnif import GNif
from worldpos import world_skel
for p in sys.argv[1:]:
    g = GNif(p); print(os.path.basename(p))
    for s in g.shapes:
        if not s.bones: continue
        Wp, sp, lin = world_skel(g, s)
        rotdev = max(np.abs(L - np.eye(3)).max() for L in lin)
        print('   %-24s spread max %.3f mean %.4f  rotdev %.4f  zrange %.1f..%.1f' % (s.name, sp.max(), sp.mean(), rotdev, Wp[:,2].min(), Wp[:,2].max()))
