import sys, collections
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from gnif import GNif

for p in sys.argv[1:]:
    g = GNif(p)
    cen = collections.Counter(t for t, _ in g.doc.blocks)
    print('=' * 80); print(p.split('guardbuild')[-1].split('extract')[-1]); print('  blocks', dict(cen))
    for s in g.shapes:
        P = g.positions(s) if hasattr(s, 'vraw') else None
        print('  shape %-28s flags=%#x nv=%s ntri=%d lay=%s skin=%s' % (s.name, s.flags, None if P is None else len(P), len(s.tris) if hasattr(s, 'tris') else -1,
              {k: v for k, v in getattr(s, 'lay', {}).items() if k in ('pos', 'size', 'flags')}, getattr(s, 'skin_type', None)))
        if P is not None and len(P):
            print('     bbox min', np.round(P.min(0), 2), 'max', np.round(P.max(0), 2), 'shape trans', np.round(s.trans, 3), 'scale', s.scale)
        if s.bones:
            print('     dismember', s.parts_dismember, ' nparts', len(s.parts), [(len(pp['bones']), pp['nw'], pp['hw'], pp['hb']) for pp in s.parts])
            print('     bones(%d):' % len(s.bones), s.bones)
            if s.skindata:
                print('     skindata hvw', s.skindata['hvw'], 'glob', np.round(s.skindata['glob'], 3))
