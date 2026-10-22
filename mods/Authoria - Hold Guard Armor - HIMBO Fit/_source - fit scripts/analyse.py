"""Where are the poke-throughs, and how well is the armour-to-skin offset preserved?
usage: analyse.py <orig nif> <fitted nif> <w>"""
import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif
from worldpos import world_skel
from fitnif import visible_union, is_proxy
from fitlib import pairs, poke_metric
from scipy_free_kd import nearest


def world_shapes(g):
    out = {}
    for s in g.shapes:
        if s.bones:
            out[s.name] = world_skel(g, s)[0]
    return out


def surf_dist(Q, P, T):
    """approx point-to-surface distance: nearest vertex refined by triangle-plane projection of the
    nearest vertex's incident triangles."""
    d, i = nearest(Q, P)
    return d


def main(orig, fit, w):
    g0 = GNif(orig); g1 = GNif(fit)
    W0 = world_shapes(g0); W1 = world_shapes(g1)
    pr = pairs()
    HP, HT, HW, Hb = pr['H'][w]
    VP, VT, VW, Vb = pr['V'][w]
    A0, T0 = visible_union(g0, W0); A1, T1 = visible_union(g1, W1)
    # offset preservation on the visible armour vertices near the skin
    d_orig_van = surf_dist(A0, VP, VT)
    d_orig_him = surf_dist(A0, HP, HT)
    d_fit_him = surf_dist(A1, HP, HT)
    near = d_orig_van < 4.0
    e_before = np.abs(d_orig_him - d_orig_van)[near]
    e_after = np.abs(d_fit_him - d_orig_van)[near]
    print('offset error (|gap to HIMBO - original gap to vanilla|) on %d skin-hugging armour verts:' % near.sum())
    print('   unfitted: mean %.3f p95 %.3f   fitted: mean %.3f p95 %.3f' % (e_before.mean(), np.percentile(e_before, 95), e_after.mean(), np.percentile(e_after, 95)))
    pk0, cov0 = poke_metric(HP, HT, A0, T0)
    pk1, cov1 = poke_metric(HP, HT, A1, T1)
    cov = cov0 | cov1
    pk0 &= cov; pk1 &= cov
    dom = np.array(Hb)[HW.argmax(1)]
    for nm, pk in (('before', pk0), ('after', pk1)):
        c = collections.Counter(dom[pk])
        print(nm, int(pk.sum()), 'poke verts by dominant bone:', c.most_common(8))
        if pk.sum():
            print('    z range', np.round(HP[pk][:, 2].min(), 1), np.round(HP[pk][:, 2].max(), 1))
    return pk0, pk1


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
