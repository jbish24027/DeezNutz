import btr,struct,os
BASE=r'C:\1. AUTHORIA\mods\Authoria - xLodGen Output\meshes\terrain\Tamriel'
def shapes(fn):
    r=btr.parse(os.path.join(BASE,fn)); d=r['data']
    # map node -> children for WATER node
    water_children=set()
    for k,t,o,s in r['blocks']:
        if t!='BSMultiBoundNode': continue
        b=d[o:o+s]
        ni=struct.unpack('<i',b[:4])[0]
        nm=r['strs'][ni] if 0<=ni<len(r['strs']) else None
        # children: after collision ref at 68? layout: name4 numED4 (+refs) ctrl4 flags4 tr12 rot36 scale4 col4 then numChildren4 children.. then multibound4
        off=4; ned=struct.unpack('<I',b[off:off+4])[0]; off+=4+4*ned
        off+=4  # controller
        off+=4  # flags
        off+=12+36+4  # tr rot scale
        off+=4  # collision
        nc=struct.unpack('<I',b[off:off+4])[0]; off+=4
        ch=struct.unpack('<%di'%nc, b[off:off+4*nc]); off+=4*nc
        if nm and nm.upper()=='WATER': water_children=set(ch)
    out=[]
    for k,t,o,s in r['blocks']:
        if t not in ('BSSubIndexTriShape','BSTriShape'): continue
        b=d[o:o+s]
        off=4; ned=struct.unpack('<I',b[off:off+4])[0]; off+=4+4*ned
        off+=4+4          # controller, flags
        tr=struct.unpack('<3f',b[off:off+12]); off+=12
        off+=36
        sc=struct.unpack('<f',b[off:off+4])[0]; off+=4
        off+=4            # collision
        bs=struct.unpack('<4f',b[off:off+16]); off+=16
        off+=12           # skin, shader, alpha
        vd=struct.unpack('<Q',b[off:off+8])[0]; off+=8
        ntri,nvert=struct.unpack('<HH',b[off:off+4]); off+=4
        dsz=struct.unpack('<I',b[off:off+4])[0]; off+=4
        vs=(dsz-ntri*6)//nvert if nvert else 0
        verts=[struct.unpack('<3f', b[off+i*vs:off+i*vs+12]) for i in range(nvert)]
        out.append(dict(block=k,water=(k in water_children),tr=tr,scale=sc,nvert=nvert,vsize=vs,verts=verts))
    return out
def report(fn,tx,ty):
    ox,oy=tx*4096.0,ty*4096.0
    print('===',fn,' tile origin world (%.0f, %.0f)'%(ox,oy))
    for sh in shapes(fn):
        if not sh['water']: continue
        s=sh['scale']; t=sh['tr']
        xs=[v[0]*s+t[0]+ox for v in sh['verts']]
        ys=[v[1]*s+t[1]+oy for v in sh['verts']]
        zs=[v[2]*s+t[2] for v in sh['verts']]
        print('  water shape block %d: %d verts  world x %.0f..%.0f  y %.0f..%.0f  z %.1f..%.1f'%(
            sh['block'],sh['nvert'],min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)))
