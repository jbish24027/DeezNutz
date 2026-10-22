"""Pose the converted dress + the full 3BA body with big sliders and count skin poking out (vs the same count at zero).
usage: python -I morphcheck.py <built _1.nif> <tri> <garment shape>"""
import sys, struct, numpy as np
sys.path.insert(0, '.'); import bslib as B, poke as P, convert_f3ba as F
def read_tri(p):
    b=open(p,'rb').read(); o=4; ns=struct.unpack('<H',b[o:o+2])[0]; o+=2; out={}
    for _ in range(ns):
        L=b[o]; sn=b[o+1:o+1+L].decode(); o+=1+L; nm=struct.unpack('<H',b[o:o+2])[0]; o+=2; d={}
        for _ in range(nm):
            L=b[o]; mn=b[o+1:o+1+L].decode(); o+=1+L; mult,c=struct.unpack('<fH',b[o:o+6]); o+=6
            r=np.frombuffer(b[o:o+8*c],dtype=np.dtype([('i','<u2'),('v','<i2',3)])); o+=8*c; d[mn]=(r['i'].astype(int),r['v']*mult)
        out[sn]=d
    return out
nif, tri, gname = sys.argv[1:4]
T = read_tri(tri); n = B.NifFile(nif); g = next(s for s in n.shapes if s.name == gname)
gp0 = B.world_verts(g); gt = np.array(g.tris)
sl = F.body_sliders(); _, bs = B.shape(F.BA3_NIF, '3BA'); bp0 = B.world_verts(bs) + sum(sm * a for sm, bg, a in sl.values())
for test in ({}, {'Breasts': 1.0, 'Hips': 1.0, 'BigButt': 1.0, 'Thighs': 1.0}, {'Breasts': 1.5, 'Butt': 1.0, 'Belly': 1.0}):
    gp = gp0.copy(); bp = bp0.copy()
    for m, v in test.items():
        if m in T[gname]: i, d = T[gname][m]; gp[i] += v * d
        bp += v * sl[m][2]
    band = (bp[:, 2] > 55) & (bp[:, 2] < 100)
    mk, sd, dist = P.poke(bp[band], gp, gt)
    print(test or 'zero', ': skin out through the dress in the torso band %d (deep >0.5: %d)' % (mk.sum(), (mk & (sd > 0.5)).sum()))
