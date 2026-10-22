import sys,struct,os
targets={t.lower() for t in sys.argv[2:]}
root=sys.argv[1]
for dp,dn,fn in os.walk(root):
    for f in fn:
        if not f.lower().endswith(('.esp','.esm','.esl')): continue
        p=os.path.join(dp,f)
        try:
            b=open(p,'rb').read(65536)
            if b[:4]!=b'TES4': continue
            size=struct.unpack('<I',b[4:8])[0]; body=b[24:24+size]; i=0; m=[]
            while i+6<=len(body):
                t=body[i:i+4]; l=struct.unpack('<H',body[i+4:i+6])[0]
                if t==b'MAST': m.append(body[i+6:i+6+l].rstrip(b'\0').decode('cp1252'))
                i+=6+l
            hit=[x for x in m if x.lower() in targets]
            if hit: print(os.path.relpath(p,root),'->',hit)
        except Exception as e: print('ERR',p,e)
