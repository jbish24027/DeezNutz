import sys,struct,os
def hdr(p):
    b=open(p,'rb').read(200000)
    assert b[:4]==b'TES4'
    size,flags=struct.unpack('<II',b[4:12])
    body=b[24:24+size]; i=0; masters=[]; nrec=None; desc=''
    while i<len(body):
        t=body[i:i+4]; l=struct.unpack('<H',body[i+4:i+6])[0]; d=body[i+6:i+6+l]
        if t==b'MAST': masters.append(d.rstrip(b'\0').decode('cp1252'))
        if t==b'HEDR': nrec=struct.unpack('<fiI',d)[1]
        if t==b'SNAM': desc=d.rstrip(b'\0').decode('cp1252','replace')[:150]
        i+=6+l
    return flags,nrec,masters,desc
for root in sys.argv[1:]:
  for dp,dn,fn in os.walk(root):
    for f in fn:
        if f.lower().endswith(('.esp','.esm','.esl')):
            p=os.path.join(dp,f); fl,n,m,d=hdr(p)
            print(f"{p}\n   flags={fl:#x} light={bool(fl&0x200)} recs={n} size={os.path.getsize(p)}\n   masters={m}\n   desc={d!r}")
