import sys, os, struct
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from gnif import GNif, layout
from fitlib import pairs
from scipy_free_kd import nearest
D = 'lotd/meshes/dbm resources/armor/guardarmordisp/'
for f in ['frame.nif', 'cuirass.nif', 'helm.nif', 'boots.nif', 'gloves.nif']:
    g = GNif(D + f)
    print(f, [(i, t) for i, (t, _) in enumerate(g.doc.blocks)])
    for s in g.shapes:
        lay = layout(s.vdesc)
        P = g.positions(s) if hasattr(s, 'vraw') else None
        b = g.doc.blocks[s.block][1]
        exp = s.vbuf_off + s.nvert_hdr * lay['size'] + s.ntri_hdr * 6
        print('  ', s.name, hex(s.vdesc), 'vflags', hex(lay['flags']), 'vsize', lay['size'], 'flags', hex(s.flags), 'trans', s.trans, 'scale', s.scale, 'tail bytes', len(b) - exp, b[exp:exp+8].hex() if len(b) > exp else '')
        if P is not None:
            Pw = P @ s.rot.T * s.scale + s.trans
            print('     bbox', Pw.min(0).round(1), Pw.max(0).round(1))
            if s.name == 'MaleBodyStormcloak':
                pr = pairs()
                for w in '01':
                    d, _ = nearest(Pw, pr['V'][w][0]); print('     mannequin -> vanilla body _%s mean %.3f' % (w, d.mean()))
