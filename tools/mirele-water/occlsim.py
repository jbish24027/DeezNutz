import espscan, struct, numpy as np, os
P=r'C:\1. AUTHORIA\mods\Authoria - Dyndolod Output\Occlusion.esp'
def cid(x,y): return 0x009B4F + (-13-y)*0x21 + (-x)
XMIN,XMAX=-14,0
YMIN,YMAX=-22,-11
def load():
    d=open(P,'rb').read()
    sz=struct.unpack('<I',d[4:8])[0]; off=24+sz
    want={cid(x,y):(x,y) for x in range(XMIN,XMAX+1) for y in range(YMIN,YMAX+1)}
    out={}
    for r in espscan.records(d, off, len(d)):
        if r[0]!='REC' or r[1]!=b'CELL': continue
        fid=r[3]&0xFFFFFF
        if fid not in want: continue
        dd=espscan.rec_data(d, r[4], r[5], r[2])
        e={s:v for s,v in espscan.subs(dd)}
        out[want[fid]]=e
    return out
cells=load()
NX=(XMAX-XMIN+1)*32; NY=(YMAX-YMIN+1)*32
H=np.full((NX,NY), -1e9, dtype=np.float64)
W=np.zeros((XMAX-XMIN+1, YMAX-YMIN+1), dtype=bool)
for (x,y),e in cells.items():
    m=e[b'MHDT']; o=struct.unpack('<f',m[:4])[0]; b=np.frombuffer(m[4:],dtype=np.uint8).astype(np.float64)
    g=o+b*8.0           # index = xi*32+yi
    g=g.reshape(32,32)  # [xi][yi]
    H[(x-XMIN)*32:(x-XMIN)*32+32, (y-YMIN)*32:(y-YMIN)*32+32]=g
    w=struct.unpack('<f', e[b'XCLW'])[0] if b'XCLW' in e else 3.4e38
    W[x-XMIN, y-YMIN] = abs(w-600.0)<0.5
X0=XMIN*4096.0; Y0=YMIN*4096.0
def hgt(wx,wy):
    xi=np.clip(((wx-X0)/128.0).astype(int),0,NX-1)
    yi=np.clip(((wy-Y0)/128.0).astype(int),0,NY-1)
    return H[xi,yi]
