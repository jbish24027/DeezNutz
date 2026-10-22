"""Count body points that poke OUT through a garment: a body point counts when the nearest garment surface point lies
within 'reach' and the body point is on the outer side of that garment triangle by more than 'tol'.
usage: python -I poke.py <nif> <body shape> <garment shape> [...]"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\skill\scripts")
import bslib as B
from smpkit import core as C


def poke(bp, gp, gt, reach=6.0, tol=0.05):
    surf = C.Surface([('g', gp, gt)])
    res = surf.query(bp, k=8)
    tri, _, dist, cp = res
    A, Bv, Cv = gp[gt[tri, 0]], gp[gt[tri, 1]], gp[gt[tri, 2]]
    n = np.cross(Bv - A, Cv - A); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
    sd = np.einsum('ij,ij->i', bp - cp, n)
    return (dist < reach) & (sd > tol), sd, dist


if __name__ == '__main__':
    n = B.NifFile(sys.argv[1]); S = {s.name: s for s in n.shapes}
    bp = B.world_verts(S[sys.argv[2]])
    for g in sys.argv[3:]:
        gs = S[g]; m, sd, dist = poke(bp, B.world_verts(gs), np.array(gs.tris))
        z = bp[m, 2]
        print('%s vs %s: %d of %d body points outside the garment (max %.2f); z bands %s' % (
            sys.argv[2], g, m.sum(), len(bp), sd[m].max() if m.any() else 0,
            np.histogram(z, bins=[0, 20, 40, 60, 80, 100, 130])[0].tolist() if m.any() else []))
