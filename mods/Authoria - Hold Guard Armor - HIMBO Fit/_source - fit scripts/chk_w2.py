import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from gnif import GNif
for p in sys.argv[1:]:
    g = GNif(p)
    for s in g.shapes:
        if not s.bones or len(s.parts) < 2: continue
        w, bi = g.vweights(s)
        Wg = np.zeros((len(w), len(s.bones)))
        for j in range(4): np.add.at(Wg, (np.arange(len(w)), bi[:, j]), w[:, j])
        Wd = np.zeros_like(Wg)
        for k, bd in enumerate(s.skindata['bones']):
            Wd[bd['w']['v'], k] = bd['w']['w']
        # partition arrays: local index into partition bones
        Wp = np.zeros_like(Wg)
        for pp in s.parts:
            vm = pp['vmap']
            for j in range(pp['nw']):
                np.add.at(Wp, (vm, np.array(pp['bones'])[pp['bidx'][:, j]]), pp['weights'][:, j])
        cnt = np.zeros(len(w)); 
        for pp in s.parts: np.add.at(cnt, pp['vmap'], 1)
        print(os.path.basename(p), s.name, 'packed-global vs skindata %.4f' % np.abs(Wg - Wd).max(), 'partarr vs skindata %.4f' % np.abs(Wp/np.maximum(cnt,1)[:,None] - Wd).max(), 'verts in >1 partition', int((cnt>1).sum()), 'in 0', int((cnt==0).sum()))
