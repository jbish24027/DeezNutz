import btr,struct,os
base=r'C:\1. AUTHORIA\mods\Authoria - xLodGen Output\meshes\terrain\Tamriel'
def rep(fn, level, tx, ty):
    p=os.path.join(base,fn)
    if not os.path.exists(p): return fn+'  <MISSING FILE>'
    r=btr.parse(p); d=r['data']
    aabb={k:struct.unpack('<6f',d[o:o+24]) for k,t,o,s in r['blocks'] if t=='BSMultiBoundAABB'}
    mb={k:struct.unpack('<i',d[o:o+4])[0] for k,t,o,s in r['blocks'] if t=='BSMultiBound'}
    res='%-28s cells x %d..%d y %d..%d  strings=%s'%(fn,tx,tx+level-1,ty,ty+level-1,r['strs'])
    if 'WATER' not in r['strs']:
        return res+'\n    *** NO WATER NODE ***'
    for k,t,o,s in r['blocks']:
        if t!='BSMultiBoundNode': continue
        b=d[o:o+s]
        ni=struct.unpack('<i',b[:4])[0]
        if not (0<=ni<len(r['strs'])) or r['strs'][ni].upper()!='WATER': continue
        tail=struct.unpack('<%di'%(len(b)//4), b)
        for v in tail[-4:]:
            if v in mb and mb[v] in aabb:
                a=aabb[mb[v]]
                ox,oy=tx*4096, ty*4096
                res+='\n    WATER AABB local c=(%.0f,%.0f,%.0f) e=(%.0f,%.0f,%.0f)  world x %.0f..%.0f  y %.0f..%.0f  Z %.1f..%.1f'%(
                    a[0],a[1],a[2],a[3],a[4],a[5], ox+a[0]-a[3], ox+a[0]+a[3], oy+a[1]-a[4], oy+a[1]+a[4], a[2]-a[5], a[2]+a[5])
    return res
