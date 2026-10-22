import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from nifmat import *
MATS={'prisonercarriage01','mrkwood01','woodwall01','riftencanalplanks01'}
for root in sys.argv[1:]:
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if not f.lower().endswith('.nif'): continue
            p=os.path.join(dp,f)
            try: doc=Doc(p); sh=shapes(doc)
            except Exception as e: print('ERR',p,e); continue
            hits=[(x['name'],os.path.basename(x['tex0']).split('.')[0]) for x in sh if os.path.basename(x['tex0']).split('.')[0] in MATS]
            if hits: print(os.path.relpath(p,root), len(hits), sorted(set(h[1] for h in hits)))
