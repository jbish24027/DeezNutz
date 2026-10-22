import btr,struct,numpy as np,os
BASE=r'C:\1. AUTHORIA\mods\Authoria - xLodGen Output\meshes\terrain\Tamriel'
def quads(fn, tx, ty):
    p=os.path.join(BASE,fn)
    r=btr.parse(p); d=r['data']
    ox,oy=tx*4096.0, ty*4096.0
    out=[]
    for k,t,o,s in r['blocks']:
        if t not in ('BSSubIndexTriShape','BSTriShape'): continue
        b=d[o:o+s]
        # find ntri/nvert/dsz by trying the tail: dsz = nvert*vsize, tri bytes = ntri*6
        # scan backwards for a consistent (ntri,nvert,dsz) header
        found=None
        for off in range(len(b)-40, 0, -1):
            try:
                ntri,nvert=struct.unpack('<HH', b[off:off+4]); dsz=struct.unpack('<I',b[off+4:off+8])[0]
            except struct.error: continue
            if nvert and ntri and dsz and off+8+dsz+ntri*6==len(b) and dsz%nvert==0 and dsz//nvert in (8,12,16,20,24,28,32,36,40,44,48):
                found=(off,ntri,nvert,dsz); break
        if not found: continue
        off,ntri,nvert,dsz=found
        vs=dsz//nvert
        vb=b[off+8:off+8+dsz]
        # scale: read from earlier - find the float 'scale' by scanning; instead try scale candidates
        verts=[struct.unpack('<3f', vb[i*vs:i*vs+12]) for i in range(nvert)]
        out.append(dict(block=k,type=t,ntri=ntri,nvert=nvert,vsize=vs,verts=verts,raw=b,hdroff=off))
    return out, r
