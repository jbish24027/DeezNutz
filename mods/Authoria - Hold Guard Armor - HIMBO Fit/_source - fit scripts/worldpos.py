"""World (bind) positions of skinned shapes: world = NodeWorld_b * SkinToBone_b * v, per bone.
Reports per-shape disagreement across bones (should be ~0 when the file is self-consistent)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif, xf_from13


def shape_world(g, s, nw=None):
    nw = nw or g.node_world()
    P = g.positions(s)
    W = g.weight_matrix(s)
    res = np.zeros_like(P); acc = np.zeros(len(P))
    spread = np.zeros(len(P))
    perbone = []
    for k, (bn, bd) in enumerate(zip(s.bones, s.skindata['bones'])):
        R, T, sc = xf_from13(bd['xf'])
        if bn not in nw:
            continue
        Rw, Tw = nw[bn]
        Q = (P @ R.T * sc + T) @ Rw.T + Tw
        perbone.append((k, Q))
    # weighted average using weights
    for k, Q in perbone:
        w = W[:, k]
        res += Q * w[:, None]; acc += w
    res /= np.maximum(acc, 1e-9)[:, None]
    for k, Q in perbone:
        m = W[:, k] > 0.01
        spread[m] = np.maximum(spread[m], np.linalg.norm(Q[m] - res[m], axis=1))
    return res, spread


def skin_space_to_world_xf(g, s, nw=None):
    """Return (A, t) such that world = A @ v + t, estimated from all bones (least squares)."""
    nw = nw or g.node_world()
    As = []
    for bn, bd in zip(s.bones, s.skindata['bones']):
        if bn in nw:
            R, T, sc = xf_from13(bd['xf'])
            Rw, Tw = nw[bn]
            As.append((Rw @ R * sc, Rw @ T + Tw))
    A = np.mean([a for a, _ in As], axis=0); t = np.mean([b for _, b in As], axis=0)
    dev = max(max(np.abs(a - A).max(), np.abs(b - t).max()) for a, b in As)
    return A, t, dev


if __name__ == '__main__':
    for p in sys.argv[1:]:
        g = GNif(p); nw = g.node_world()
        print(os.path.basename(p))
        for s in g.shapes:
            if not s.bones or not s.skindata:
                continue
            A, t, dev = skin_space_to_world_xf(g, s, nw)
            print('   %-26s A~I:%s t=%s maxdev=%.4f' % (s.name, np.allclose(A, np.eye(3), atol=1e-3), np.round(t, 3), dev))


SKEL = r"C:\1. AUTHORIA\mods\XP32 Maximum Skeleton Special Extended - XPMSSE\meshes\actors\character\character assets\skeleton.nif"
_skel = None


def skeleton_world():
    global _skel
    if _skel is None:
        from nifrw import Doc, parse_node
        d = Doc(SKEL)
        out = {}
        def rec(i, R0, T0, S0):
            t, b = d.blocks[i]
            if t not in ('NiNode', 'BSFadeNode'):
                return
            n = parse_node(b)
            R = np.array(n['rot']).reshape(3, 3); T = np.array(n['trans'])
            Rw = R0 @ R; Tw = R0 @ (T * S0) + T0; Sw = S0 * n['scale']
            out[d.strings[n['name']]] = (Rw, Tw)
            for c in n['children']:
                if c >= 0:
                    rec(c, Rw, Tw, Sw)
        rec(d.roots[0], np.eye(3), np.zeros(3), 1.0)
        _skel = out
    return _skel


def world_skel(g, s, nw_file=None):
    """per-vertex bind world positions using the game skeleton (file nodes for non-skeleton bones).
    returns world (n,3), spread (n,) = max distance between per-bone answers, and per-bone A matrices"""
    sk = skeleton_world()
    nw_file = nw_file or g.node_world()
    P = g.positions(s)
    W = g.weight_matrix(s)
    res = np.zeros_like(P); acc = np.zeros(len(P)); spread = np.zeros(len(P))
    Qs = []
    lin = []
    for k, (bn, bd) in enumerate(zip(s.bones, s.skindata['bones'])):
        R, T, sc = xf_from13(bd['xf'])
        if bn in sk:
            Rw, Tw = sk[bn]
        elif bn in nw_file:
            Rw, Tw = nw_file[bn]
        else:
            continue
        Q = (P @ R.T * sc + T) @ Rw.T + Tw
        Qs.append((k, Q)); lin.append(Rw @ R * sc)
        w = W[:, k]
        res += Q * w[:, None]; acc += w
    res /= np.maximum(acc, 1e-9)[:, None]
    for k, Q in Qs:
        m = W[:, k] > 0.05
        spread[m] = np.maximum(spread[m], np.linalg.norm(Q[m] - res[m], axis=1))
    return res, spread, lin
