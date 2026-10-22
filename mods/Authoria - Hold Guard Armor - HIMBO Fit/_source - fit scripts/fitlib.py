"""Automatic vanilla -> HIMBO conform for the hold guard armour.

Reference pairs (one topology, HIMBO's own conversion reference):
  weight 0:  S0 = 'HIMBO - VAL' base (= vanilla malebody_0 shape)      T0 = VAL + 'Vanilla to HIMBO' slider (= HIMBO malebody_0)
  weight 1:  S1 = S0 + (vanilla _1 - vanilla _0) transferred           T1 = T0 + (HIMBO _1 - HIMBO _0) transferred
Each armour vertex moves by a smooth, bone-gated, inverse-distance blend of the reference
displacement at its nearest reference vertices (offset from the body is carried unchanged).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif
from worldpos import world_skel
from refbody import conversion_pair, load_world, tri_normals, VAN, BODY
from scipy_free_kd import knn, nearest, TriGrid

SKEL_PREFIX = 'NPC '


def composite(folder, names, shape_filter=None):
    Ps, Ts, Ws, off = [], [], [], 0
    bones_all = []
    parts = []
    for nm in names:
        g = GNif(os.path.join(folder, nm))
        for s in g.shapes:
            if not s.bones:
                continue
            if shape_filter and s.name not in shape_filter:
                continue
            P, _, _ = world_skel(g, s)
            W = g.weight_matrix(s)
            parts.append((P, s.tris.astype(np.int64) + off, W, s.bones))
            off += len(P)
    bones_all = sorted({b for p in parts for b in p[3]})
    bi = {b: i for i, b in enumerate(bones_all)}
    P = np.concatenate([p[0] for p in parts]); T = np.concatenate([p[1] for p in parts])
    W = np.zeros((len(P), len(bones_all)))
    o = 0
    for p in parts:
        for k, b in enumerate(p[3]):
            W[o:o + len(p[0]), bi[b]] = p[2][:, k]
        o += len(p[0])
    return P, T, W, bones_all


def transfer_delta(Q, A0, A1, k=6, fade0=1.5, fade1=4.0):
    """delta (A1-A0) of a reference mesh sampled at points Q by IDW over k nearest A0 verts;
    fades to zero for Q farther than fade0..fade1 from the reference (head region)."""
    D, I = knn(Q, A0, k)
    w = 1.0 / (D ** 2 + 1e-4)
    w /= w.sum(1, keepdims=True)
    d = ((A1 - A0)[I] * w[:, :, None]).sum(1)
    f = np.clip((fade1 - D[:, 0]) / (fade1 - fade0), 0, 1)
    return d * f[:, None]


_PAIRS = None


def pairs():
    global _PAIRS
    if _PAIRS is not None:
        return _PAIRS
    g, s, S0, T0, tris = conversion_pair()
    Wval = g.weight_matrix(s)
    vbones = s.bones
    V = {}
    H = {}
    for w in '01':
        V[w] = composite(VAN, ['malebody_%s.nif' % w, 'malehands_%s.nif' % w, 'malefeet_%s.nif' % w], {'MaleUnderwearBody:0', 'HandMaleBig3rd', 'FootMale_Big'})
        H[w] = composite(BODY, ['malebody_%s.nif' % w, 'malehands_%s.nif' % w, 'malefeet_%s.nif' % w], None)
    # vanilla composite: drop underwear shape (MaleUnderwear_1 sits off the skin)
    S1 = S0 + transfer_delta(S0, V['0'][0], V['1'][0])
    T1 = T0 + transfer_delta(T0, H['0'][0], H['1'][0])
    _PAIRS = dict(tris=tris, vbones=vbones, Wval=Wval,
                  S={'0': S0, '1': S1}, T={'0': T0, '1': T1}, V=V, H=H)
    return _PAIRS


def bone_vec(W, bones, target_bones):
    """re-express weight matrix W (columns=bones) on target_bones (skeleton bones only)."""
    idx = {b: i for i, b in enumerate(target_bones)}
    out = np.zeros((len(W), len(target_bones)))
    for k, b in enumerate(bones):
        if b in idx:
            out[:, idx[b]] += W[:, k]
    return out


def conform_disp(Pw, Wa, abones, w, k=16, gate=True, wt=None):
    """displacement for armour points Pw (world) with weights Wa over abones: source made on vanilla
    weight w, target HIMBO weight wt (default = w)."""
    pr = pairs()
    wt = w if wt is None else wt
    S = pr['S'][w]; T = pr['T'][wt]
    Dref = T - S
    D, I = knn(Pw, S, k)
    if gate:
        sk = [b for b in pr['vbones'] if b.startswith(SKEL_PREFIX)]
        A = bone_vec(Wa, abones, sk)
        R = bone_vec(pr['Wval'], pr['vbones'], sk)
        asum = A.sum(1)
        sim = np.minimum(A[:, None, :], R[I]).sum(2)  # overlap in [0,1]
        # vertices with little skeleton weight (pure cloth) -> no gating
        gatew = np.where(asum[:, None] > 0.5, np.clip((sim - 0.05) / 0.25, 0.02, 1.0), 1.0)
    else:
        gatew = 1.0
    dmin = D[:, :1]
    sig = np.maximum(1.0, 0.6 * dmin)
    wgt = np.exp(-((D - dmin) ** 2) / (2 * sig ** 2)) / (D + 0.25) * gatew
    wgt /= wgt.sum(1, keepdims=True)
    disp = (Dref[I] * wgt[:, :, None]).sum(1)
    return disp, D[:, 0]


def smooth_on_mesh(disp, tris, n, iters=3, lam=0.5, mask=None):
    """Laplacian smoothing of a per-vertex field over mesh edges (keeps the field continuous)."""
    if len(tris) == 0 or iters == 0:
        return disp
    e = np.concatenate([tris[:, [0, 1]], tris[:, [1, 2]], tris[:, [2, 0]]])
    e = np.concatenate([e, e[:, ::-1]])
    deg = np.bincount(e[:, 0], minlength=n).astype(np.float64)
    out = disp.copy()
    for _ in range(iters):
        acc = np.zeros_like(out)
        np.add.at(acc, e[:, 0], out[e[:, 1]])
        avg = np.where(deg[:, None] > 0, acc / np.maximum(deg, 1)[:, None], out)
        upd = out + lam * (avg - out)
        out = upd if mask is None else np.where(mask[:, None], upd, out)
    return out


def weld_groups(P, tol=1e-4):
    """map coincident vertices (UV seams) to a shared id so they get identical displacement."""
    key = np.round(P / tol).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    return inv.ravel()


def local_from_world_delta(g, s, dW):
    """convert world deltas to the shape's skin space using the weighted bone linear maps."""
    from worldpos import skeleton_world
    from gnif import xf_from13
    sk = skeleton_world(); nw = g.node_world()
    W = g.weight_matrix(s)
    M = np.zeros((len(dW), 3, 3)); acc = np.zeros(len(dW))
    for k, (bn, bd) in enumerate(zip(s.bones, s.skindata['bones'])):
        R, T, sc = xf_from13(bd['xf'])
        Rw = sk[bn][0] if bn in sk else (nw[bn][0] if bn in nw else None)
        if Rw is None:
            continue
        L = Rw @ R * sc
        M += W[:, k][:, None, None] * L[None]
        acc += W[:, k]
    M /= np.maximum(acc, 1e-9)[:, None, None]
    return np.einsum('nij,nj->ni', np.linalg.inv(M), dW)


# ------------------------------------------------------------------ metrics
def poke_metric(body_P, body_T, armour_P, armour_T, covered=None, tfront=25.0, tback=6.0, hug=4.0):
    """% of covered body vertices with NO armour surface in front of them along the body normal
    (a hit within 0.1 behind counts as flush). covered = vertices with an armour surface within +-hug units along the normal (the hugging region)."""
    N = tri_normals(body_P, body_T)
    grid = TriGrid(armour_P, armour_T, cell=1.5)
    tpos, tneg = grid.raycast(body_P, N, -tback, tfront)
    front = (tpos < np.inf) | (tneg >= -0.1)
    cov = (tpos <= hug) | (tneg >= -hug)
    if covered is None:
        covered = cov
    poke = covered & ~front
    return poke, covered


def edge_strain(P0, P1, tris):
    e = np.concatenate([tris[:, [0, 1]], tris[:, [1, 2]], tris[:, [2, 0]]])
    l0 = np.linalg.norm(P0[e[:, 0]] - P0[e[:, 1]], axis=1)
    l1 = np.linalg.norm(P1[e[:, 0]] - P1[e[:, 1]], axis=1)
    m = l0 > 1e-4
    r = l1[m] / l0[m]
    return r


def boundary_points(P, T, step=0.5):
    e = np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1)
    # weld by position so UV seams are not counted as open edges
    key = np.round(P / 1e-3).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
    e = np.sort(inv[e], 1)
    e = e[e[:, 0] != e[:, 1]]
    u, c = np.unique(e, axis=0, return_counts=True)
    b = u[c == 1]
    rep = np.zeros(inv.max() + 1, np.int64); rep[inv] = np.arange(len(P))
    a = P[rep[b[:, 0]]]; z = P[rep[b[:, 1]]]
    pts = [a, z]
    L = np.linalg.norm(z - a, axis=1)
    for f in np.arange(step, 1.0, step / max(L.max(), 1e-6)):
        pts.append(a + (z - a) * f)
    return np.concatenate(pts) if len(b) else np.zeros((0, 3))


def poke_design(w, A0, T0, A1, T1, hug=3.0, edge_excl=2.0, flush=0.3, wt=None):
    """Design-referenced poke-through.
    covered  = vanilla-body vertices the ORIGINAL armour hugs (an armour surface within +-hug along the
               skin normal) -> carried to the HIMBO body by nearest vertex.
    baseline = % of covered vanilla verts with no armour in front (original armour on the body it was made for)
    before   = same test, original armour on the HIMBO body
    after    = same test, fitted armour on the HIMBO body"""
    pr = pairs()
    VP, VT = pr['V'][w][0], pr['V'][w][1]
    wt = w if wt is None else wt
    HP, HT = pr['H'][wt][0], pr['H'][wt][1]
    VN = tri_normals(VP, VT); HN = tri_normals(HP, HT)
    g0 = TriGrid(A0, T0, cell=1.5); g1 = TriGrid(A1, T1, cell=1.5)
    tp, tn = g0.raycast(VP, VN, -6.0, 25.0)
    covV = (tp <= hug) | (tn >= -hug)
    baseV = covV & ~((tp < np.inf) | (tn >= -flush))
    _, j = nearest(HP, VP)
    covH = covV[j] & (np.linalg.norm(HP - VP[j], axis=1) < 4.0)
    # interior only: drop skin points within edge_excl of an open armour edge (hems, cuffs, collars)
    B0 = boundary_points(A0, T0); B1 = boundary_points(A1, T1)
    if len(B0):
        dV, _ = nearest(VP, B0); covV &= dV > edge_excl; baseV &= covV
        dH0, _ = nearest(HP, B0); covH &= dH0 > edge_excl
    if len(B1):
        dH1, _ = nearest(HP, B1); covH &= dH1 > edge_excl
    out = {}
    for nm, g in (('before', g0), ('after', g1)):
        tp, tn = g.raycast(HP, HN, -6.0, 25.0)
        front = (tp < np.inf) | (tn >= -flush)
        out[nm] = covH & ~front
        out[nm + '_depth'] = float(np.median(-tn[out[nm]])) if out[nm].any() else 0.0
    return dict(covered_vanilla=int(covV.sum()), covered_himbo=int(covH.sum()),
                baseline_pct=round(100.0 * baseV.sum() / max(covV.sum(), 1), 2),
                before_pct=round(100.0 * out['before'].sum() / max(covH.sum(), 1), 2),
                after_pct=round(100.0 * out['after'].sum() / max(covH.sum(), 1), 2),
                before_median_depth=round(out['before_depth'], 2), after_median_depth=round(out['after_depth'], 2)), out
