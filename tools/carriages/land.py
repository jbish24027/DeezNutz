import struct,zlib,sys,os,math,pickle
sys.path.insert(0,os.path.dirname(__file__))
from plug import masters,subs
def scan_land(path,targets,store,tag=None):
    """targets: set of (world_gid,(gx,gy)). store[(world,grid)] = (plugin, heights 33x33 floats)"""
    with open(path,'rb') as fh: b=fh.read()
    if b[:4]!=b'TES4': return 0
    m=masters(b); name=os.path.basename(path)
    def gid(k):
        i=k>>24; return ((m[i] if i<len(m) else name).lower(), k&0xFFFFFF)
    s=struct.unpack('<I',b[4:8])[0]; off=24+s; n=0
    worlds={w for w,g in targets}
    def walk(o,end,world,grid):
        nonlocal n
        while o<end:
            sig=b[o:o+4]; size=struct.unpack('<I',b[o+4:o+8])[0]
            if sig==b'GRUP':
                gtype=struct.unpack('<i',b[o+12:o+16])[0]; label=b[o+8:o+12]
                if gtype==1:
                    w=gid(struct.unpack('<I',label)[0])
                    if w in worlds: walk(o+24,o+size,w,None)
                elif gtype==4 or gtype==5:
                    walk(o+24,o+size,world,None)
                elif gtype in (6,9):
                    if grid and (world,grid) in targets: walk(o+24,o+size,world,grid)
                o+=size; continue
            size,flags,fid=struct.unpack('<III',b[o+4:o+16])
            if sig==b'CELL':
                d=b[o+24:o+24+size]
                if flags&0x40000: d=zlib.decompress(d[4:])
                g=None; i=0
                while i<len(d):
                    t=d[i:i+4]; l=struct.unpack('<H',d[i+4:i+6])[0]
                    if t==b'XCLC': g=struct.unpack('<ii',d[i+6:i+14]); break
                    i+=6+l
                grid=g
            elif sig==b'LAND' and grid and (world,grid) in targets:
                d=b[o+24:o+24+size]
                if flags&0x40000: d=zlib.decompress(d[4:])
                for t,v in subs(d):
                    if t=='VHGT':
                        base=struct.unpack('<f',v[:4])[0]; dl=struct.unpack('<1089b',v[4:4+1089])
                        H=[]; rs=base
                        for r in range(33):
                            rs+=dl[r*33]; h=rs; row=[h*8]
                            for c in range(1,33): h+=dl[r*33+c]; row.append(h*8)
                            H.append(row)
                        store[(world,grid)]=(name,H); n+=1
            o+=24+size
    while off<len(b):
        size=struct.unpack('<I',b[off+4:off+8])[0]
        if b[off+8:off+12]==b'WRLD': walk(off+24,off+size,None,None)
        off+=size
    return n
def height(store,world,x,y):
    gx=math.floor(x/4096); gy=math.floor(y/4096)
    e=store.get((world,(gx,gy)))
    if not e: return None
    H=e[1]; fx=(x-gx*4096)/128.0; fy=(y-gy*4096)/128.0
    c=min(int(fx),31); r=min(int(fy),31); tx=fx-c; ty=fy-r
    h00=H[r][c];h01=H[r][c+1];h10=H[r+1][c];h11=H[r+1][c+1]
    # triangle interpolation like the engine (quad split); use bilinear approx
    return h00*(1-tx)*(1-ty)+h01*tx*(1-ty)+h10*(1-tx)*ty+h11*tx*ty
