import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from gnif import GNif
for p in sys.argv[1:]:
    g = GNif(p); print(os.path.basename(p))
    for s in g.shapes:
        if not s.bones: continue
        W = g.weight_matrix(s)
        Wd = np.zeros_like(W)
        for k, bd in enumerate(s.skindata['bones']):
            if bd['w'] is not None and len(bd['w']):
                Wd[bd['w']['v'], k] = bd['w']['w']
        # partition arrays
        Wp = np.zeros_like(W)
        for pp in s.parts:
            vm = pp['vmap'] if pp['vmap'] is not None else np.arange(len(W))
            for j in range(pp['nw']):
                np.add.at(Wp, (vm, np.array(pp['bones'])[pp['bidx'][:, j]]), pp['weights'][:, j])
        pb_ident = [pp['bones'] == list(range(len(pp['bones']))) for pp in s.parts]
        print('   %-22s packed-vs-skindata %.4f packed-vs-partarrays %.4f  identity-bone-lists %s  vmap-identity %s' % (
            s.name, np.abs(W - Wd).max(), np.abs(W - Wp).max(), pb_ident, [pp['vmap'] is None or bool((pp['vmap'] == np.arange(len(pp['vmap']))).all()) for pp in s.parts]))
