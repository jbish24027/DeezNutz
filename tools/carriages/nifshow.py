import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from nifmat import *
for p in sys.argv[1:]:
    doc=Doc(p); print('==',p, len(doc.blocks),'blocks')
    for x in shapes(doc):
        s=x['s']; print('  [%3d] %-26s stype=%d f1=%08X f2=%08X sh=%d ts=%d  %s'%(x['idx'],x['name'],s['stype'],s['f1'],s['f2'],x['sh'],s['ts'],' | '.join(t for t in x['tex'] if t)))
