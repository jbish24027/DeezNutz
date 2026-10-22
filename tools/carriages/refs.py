import sys,struct,os
sys.path.insert(0,os.path.dirname(__file__))
from recs import load
old=load(sys.argv[1]); new=load(sys.argv[2])
moved={k&0xFFFFFF for k in old if k not in new}
changed={k&0xFFFFFF for k in old if k in new and old[k][3]!=new[k][3]}
def masters(p):
    b=open(p,'rb').read(65536); s=struct.unpack('<I',b[4:8])[0]; body=b[24:24+s]; i=0; m=[]
    while i<len(body):
        t=body[i:i+4]; l=struct.unpack('<H',body[i+4:i+6])[0]
        if t==b'MAST': m.append(body[i+6:i+6+l].rstrip(b'\0').decode('cp1252'))
        i+=6+l
    return m
for p in sys.argv[3:]:
    m=masters(p); idx=[x.lower() for x in m].index('animatedcarriage.esm')
    recs=load(p)
    ov=[(hex(k),v[0],v[1]) for k,v in recs.items() if k>>24==idx]
    ovmoved=[o for o in ov if int(o[0],16)&0xFFFFFF in moved]
    ovchanged=[o for o in ov if int(o[0],16)&0xFFFFFF in changed]
    refs=set()
    for k,v in recs.items():
        d=v[3]
        for lid in moved:
            if struct.pack('<I',(idx<<24)|lid) in d: refs.add((hex(lid),hex(k),v[0]))
    print('==',os.path.basename(p),'AC overrides:',len(ov),'override moved:',len(ovmoved),'override changed-in-1.2.1:',len(ovchanged),'refs to moved ids:',len(refs))
    for o in ovchanged[:40]: print('   chg',o)
    for r in list(refs)[:20]: print('   ref',r)
