import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from fitlib import *
from gnif import GNif
pr = pairs()
for f in sys.argv[1:]:
    for w in '01':
        g = GNif(f % w)
        for s in g.shapes:
            P = world_skel(g, s)[0]
            r = []
            for vw in '01':
                d, _ = nearest(P, pr['V'][vw][0]); r.append('vanilla_%s med %.2f' % (vw, np.median(d)))
            for hw in '01':
                d, _ = nearest(P, pr['H'][hw][0]); r.append('HIMBO_%s med %.2f' % (hw, np.median(d)))
            print(os.path.basename(f % w), s.name, ' | '.join(r))
