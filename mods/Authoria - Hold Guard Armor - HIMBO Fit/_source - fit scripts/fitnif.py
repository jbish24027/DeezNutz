"""Fit one skinned armour NIF (in memory) to HIMBO and report numbers."""
import os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif, xf_from13
from worldpos import world_skel, skeleton_world
from fitlib import (pairs, conform_disp, smooth_on_mesh, weld_groups, local_from_world_delta,
                    poke_metric, edge_strain, bone_vec)
from scipy_free_kd import knn

PROXY = ('HDT', 'Col', 'VirtualGround')
NOFIT = ('VirtualGround',)
RIGID_DIAM = 12.0


def components(tris, grp, n):
    parent = np.arange(n)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    # weld coincident vertices first
    first = {}
    for v, gi in enumerate(grp):
        if gi in first:
            a, b = find(v), find(first[gi])
            if a != b: parent[a] = b
        else:
            first[gi] = v
    for t in tris:
        a = find(t[0])
        for x in t[1:]:
            b = find(x)
            if a != b: parent[b] = a
    return np.array([find(v) for v in range(n)])


def is_proxy(name):
    return name.startswith(PROXY)


def shape_key(g, s):
    return s.name + ':' + hashlib.md5(np.round(g.positions(s), 3).tobytes() + s.tris.tobytes()).hexdigest()[:10]


def fit_shape(g, s, w, weights=True, wt_near=1.0, wt_far=3.0, smooth_iters=3, wt=None):
    wt = w if wt is None else wt
    """returns dict(newP local, W new or None, stats)"""
    P0 = g.positions(s)
    Pw, spread, _ = world_skel(g, s)
    W = g.weight_matrix(s)
    disp, dbody = conform_disp(Pw, W, s.bones, w, wt=wt)
    grp = weld_groups(Pw)
    # identical displacement for coincident vertices (UV / normal seams)
    acc = np.zeros((grp.max() + 1, 3)); cnt = np.bincount(grp)
    np.add.at(acc, grp, disp)
    disp = acc[grp] / cnt[grp][:, None]
    disp = smooth_on_mesh(disp, s.tris.astype(np.int64), len(disp), iters=smooth_iters)
    acc = np.zeros((grp.max() + 1, 3)); np.add.at(acc, grp, disp); disp = acc[grp] / cnt[grp][:, None]
    # ---- collision pass: a vertex that sat OUTSIDE the vanilla skin must stay outside the HIMBO skin
    pushed = 0
    if not s.name.startswith('Col') and s.name not in ('SteelMaleBody',):
        pr = pairs()
        VP, VT = pr['V'][w][0], pr['V'][w][1]
        HP, HT = pr['H'][wt][0], pr['H'][wt][1]
        from refbody import tri_normals
        VN = tri_normals(VP, VT); HN = tri_normals(HP, HT)
        dv, iv = knn(Pw, VP, 1); dv = dv[:, 0]; iv = iv[:, 0]
        sd0 = ((Pw - VP[iv]) * VN[iv]).sum(1)                 # signed offset over the vanilla skin
        Q = Pw + disp
        dh, ih = knn(Q, HP, 1); ih = ih[:, 0]
        sd1 = ((Q - HP[ih]) * HN[ih]).sum(1)                  # signed offset over the HIMBO skin
        want = np.minimum(np.maximum(sd0, 0.0), 0.3) + 0.05   # keep at least the old clearance (capped)
        need = (sd0 > -0.05) & (sd1 < want) & (dh[:, 0] < 3.0)
        push = np.zeros_like(disp)
        push[need] = HN[ih[need]] * (want[need] - sd1[need])[:, None]
        push = smooth_on_mesh(push, s.tris.astype(np.int64), len(push), iters=2, lam=0.5)
        push[need] = np.maximum((push[need] * HN[ih[need]]).sum(1), (want[need] - sd1[need]))[:, None] * HN[ih[need]]
        acc = np.zeros((grp.max() + 1, 3)); np.add.at(acc, grp, push); push = acc[grp] / cnt[grp][:, None]
        disp = disp + push
        pushed = int(need.sum())
    # ---- rigid hardware: small disconnected pieces (buckles, pouches, studs) translate as one
    comp = components(s.tris.astype(np.int64), grp, len(disp))
    rigid = 0
    for c in np.unique(comp):
        m = comp == c
        ext = Pw[m].max(0) - Pw[m].min(0)
        if np.linalg.norm(ext) < RIGID_DIAM and m.sum() >= 3 and not is_proxy(s.name):
            disp[m] = disp[m].mean(0); rigid += int(m.sum())
    dloc = local_from_world_delta(g, s, disp)
    P1 = P0 + dloc
    out = dict(P=P1, Pw0=Pw, Pw1=Pw + disp, disp=disp, dbody=dbody, W=None, wchanged=0, pushed=pushed, rigid=rigid)
    if weights and not is_proxy(s.name):
        pr = pairs()
        HP, HT, HW, Hb = pr['H'][wt]
        D, I = knn(Pw + disp, HP, 4)
        iw = 1.0 / (D ** 2 + 1e-3); iw /= iw.sum(1, keepdims=True)
        Hs = (HW[I] * iw[:, :, None]).sum(1)                      # HIMBO weights at the nearest skin
        Hloc = bone_vec(Hs, Hb, s.bones)                           # restricted to this shape's bones
        cover = Hloc.sum(1)                                        # share of HIMBO weight mass representable
        Hloc /= np.maximum(cover, 1e-9)[:, None]
        is_cloth = np.array([not b.startswith('NPC ') for b in s.bones])
        cloth_w = W[:, is_cloth].sum(1) if is_cloth.any() else np.zeros(len(W))
        a = np.clip((wt_far - D[:, 0]) / (wt_far - wt_near), 0, 1)
        a *= np.clip((cover - 0.9) / 0.1, 0, 1)                    # don't force unrepresentable weights
        a[cloth_w > 1e-4] = 0                                       # never touch SMP cloth-bone vertices
        if a.any():
            Wn = (1 - a)[:, None] * W + a[:, None] * Hloc
            out['W'] = Wn
            out['wchanged'] = int((a > 0).sum())
            out['walpha'] = a
    return out


def visible_union(g, shapes_P):
    Ps, Ts, off = [], [], 0
    for s in g.shapes:
        if is_proxy(s.name) or s.shader < 0:
            continue
        P = shapes_P[s.name]
        Ps.append(P); Ts.append(s.tris.astype(np.int64) + off); off += len(P)
    return np.concatenate(Ps), np.concatenate(Ts)


def body_for(w, which=('body', 'hands', 'feet')):
    pr = pairs()
    return pr['H'][w][0], pr['H'][w][1]


def write_back(g, s, res):
    g.set_positions(s, res['P'])
    if res['W'] is not None:
        g.set_weights(s, res['W'])
    recompute_bounds(g, s)
    if s.part_block >= 0:
        g.write_partition(s)
    if s.skindata:
        g.write_skindata(s)


def recompute_bounds(g, s):
    P = g.positions(s)
    if s.skindata:
        gR, gT, gS = xf_from13(s.skindata['glob'])
        Pc = P
        c = (P.min(0) + P.max(0)) / 2
        r = np.linalg.norm(P - c, axis=1).max()
        g.write_bound(s, c, r)
        W = g.weight_matrix(s)
        for k, bd in enumerate(s.skindata['bones']):
            m = W[:, k] > 0
            if not m.any():
                continue
            R, T, sc = xf_from13(bd['xf'])
            Q = (P[m] @ R.T) * sc + T
            cc = (Q.min(0) + Q.max(0)) / 2
            rr = np.linalg.norm(Q - cc, axis=1).max()
            bd['bound'] = (float(cc[0]), float(cc[1]), float(cc[2]), float(rr))


def bound_convention_check(g, s):
    """how far the file's own bounds are from the recompute formula (before any edit)."""
    P = g.positions(s)
    c = (P.min(0) + P.max(0)) / 2; r = np.linalg.norm(P - c, axis=1).max()
    b = np.array(s.bound)
    return np.linalg.norm(b[:3] - c), b[3] - r


def validate(g):
    """skin validity: indices in range, weights sum to 1, packed == NiSkinData == partition arrays,
    partitions/bone lists present."""
    rows = []
    for s in g.shapes:
        if not s.bones:
            continue
        w, bi = g.vweights(s)
        W = g.weight_matrix(s)
        ok_idx = bool((bi < len(s.bones)).all())
        sums = W.sum(1)
        Wd = np.zeros_like(W)
        for k, bd in enumerate(s.skindata['bones']):
            if bd['w'] is not None and len(bd['w']):
                Wd[bd['w']['v'], k] = bd['w']['w']
        pa_ok = True
        for p in s.parts:
            if p['hb'] and (p['bidx'] >= len(p['bones'])).any():
                pa_ok = False
        rows.append(dict(shape=s.name, idx_ok=ok_idx, wsum_min=float(sums.min()), wsum_max=float(sums.max()),
                         packed_vs_skindata=float(np.abs(W - Wd).max()), part_idx_ok=pa_ok,
                         partitions=[b for _, b in s.parts_dismember], nbones=len(s.bones)))
    return rows
