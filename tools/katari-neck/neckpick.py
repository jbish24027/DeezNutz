"""Pick the Katari neck geometry to delete, from the mesh itself, with assertions.

Selection rules (validated against Fuse00's 1.1 topology - jacket 12089 v,
DressNew 4196 v):

  _Fuse00_Katari_Jacket   drop 3 whole triangle islands:
                            the standing collar   (661 v, tops out above z=114)
                            the two V-yoke straps (276 + 267 v)
                          identified as: 260 <= verts < 1000 and max z > 99.
                          The 206-v heart studs and the 252-v hem trim are
                          excluded by the size and height bounds respectively.

  _Fuse00_Katari_DressNew trim the cream shirt bodice (islands whose max z > 110,
                          i.e. front + back panel, 523 + 506 v) down to Z_CUT.
                          The 541-v shoulder caps (max z 105) and the skirt are
                          untouched, so the sleeves and shoulders survive.

A triangle goes if ANY of its vertices is condemned - the OutfitStudio
delete-vertices rule - so the surviving edge sits just under the cut plane.
"""
import os, sys
sys.path.insert(0, r'C:\1. AUTHORIA\tools\nifcheck')
import numpy as np
import trishape_cut as tc

Z_CUT = 110.0          # body shoulders top out at 110.5, neck at 114

JACKET = '_Fuse00_Katari_Jacket'
DRESS  = '_Fuse00_Katari_DressNew'


def _tris_touching(tris, dead):
    return {i for i, (a, b, c) in enumerate(tris) if a in dead or b in dead or c in dead}


def jacket_drop(path, verbose=False):
    P, comps, tris = tc.islands(path, JACKET)
    P = np.array(P, float)
    picked = [c for c in comps if 260 <= len(c) < 1000 and P[c][:, 2].max() > 99.0]
    if verbose:
        for c in picked:
            A = P[c]
            print(f"    jacket island {len(c):5d} v  z[{A[:,2].min():.1f},{A[:,2].max():.1f}]")
    assert len(picked) == 3, f"expected 3 jacket islands, got {len(picked)}"
    assert sum(len(c) for c in picked) == 1204, "jacket island vert total changed"
    dead = set().union(*[set(c) for c in picked])
    return _tris_touching(tris, dead), len(tris)


def dress_drop(path, z_cut=Z_CUT, verbose=False):
    P, comps, tris = tc.islands(path, DRESS)
    P = np.array(P, float)
    bodice = [c for c in comps if P[c][:, 2].max() > 110.0]
    if verbose:
        for c in bodice:
            A = P[c]
            print(f"    dress bodice   {len(c):5d} v  z[{A[:,2].min():.1f},{A[:,2].max():.1f}]")
    assert len(bodice) == 2, f"expected 2 bodice islands, got {len(bodice)}"
    assert sum(len(c) for c in bodice) == 1029, "bodice vert total changed"
    band = set().union(*[set(c) for c in bodice])
    dead = {v for v in band if P[v][2] > z_cut}
    return _tris_touching(tris, dead), len(tris)
