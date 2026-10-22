import sys, numpy as np
sys.path.insert(0, r'C:/1. AUTHORIA/_tools/mirele-water')
from waterscan import scan_plugin

SYN = r'C:/1. AUTHORIA/mods/Authoria - Synthesis Output - NSFW/Authoria - Output - Synthesis Worldspace.esp'
ESM = r'C:/1. AUTHORIA/Stock Game/Data/Skyrim.esm'
CELL=4096.0; VS=128.0

def land_id(cx,cy): return 0x009B4F + (-13-cy)*0x21 + (-cx) + 0x1000

def build(xs, ys):
    ids={}
    for cx in xs:
        for cy in ys: ids[land_id(cx,cy)]=(cx,cy)
    got = scan_plugin(SYN, set(ids))
    src = {k:'SYN' for k in got}
    miss = set(ids)-set(got)
    if miss:
        g2 = scan_plugin(ESM, miss)
        for k,v in g2.items(): got[k]=v; src[k]='ESM'
    nx=len(xs)*32+1; ny=len(ys)*32+1
    Z=np.full((ny,nx), np.nan)          # [row=y index from south, col=x index from west]
    for lid,(cx,cy) in ids.items():
        H=got.get(lid)
        if H is None: continue
        i=xs.index(cx); j=ys.index(cy)
        for vy in range(33):
            for vx in range(33):
                Z[j*32+vy, i*32+vx]=H[(vx,vy)]
    return Z, src, got

def make_sampler(Z, xs, ys):
    x0 = xs[0]*CELL; y0 = ys[0]*CELL
    ny,nx = Z.shape
    Zf = np.nan_to_num(Z, nan=20000.0)
    def sample(wx, wy):
        u=(wx-x0)/VS; v=(wy-y0)/VS
        u=np.clip(u,0,nx-1.001); v=np.clip(v,0,ny-1.001)
        i0=np.floor(u).astype(int); j0=np.floor(v).astype(int)
        fu=u-i0; fv=v-j0
        a=Zf[j0,i0]; b=Zf[j0,i0+1]; c=Zf[j0+1,i0]; d=Zf[j0+1,i0+1]
        return (a*(1-fu)*(1-fv)+b*fu*(1-fv)+c*(1-fu)*fv+d*fu*fv)
    return sample
