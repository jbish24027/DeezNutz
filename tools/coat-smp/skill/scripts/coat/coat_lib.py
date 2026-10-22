"""Pose / contact helpers for the coat checks that the skill's smpkit.checks does not carry (ported from realistic-armor-hdt
flap_swing.py + build_twolayer.py, 2026-10-11). Everything else (bone_world, chains, swing, flare, skin, rot, LIM1 / LIM, stride,
LEG, faces, check, rest, xml_info, preset, morph, Matcher, compare, render, load_tex) is smpkit.checks."""
import os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
LIM1, LIM = K.LIM1, K.LIM            # the SAME dicts K.swing / K.flare read (the checks update them per design)
bone_world, chains, swing, flare, skin, rot = K.bone_world, K.chains, K.swing, K.flare, K.skin, K.rot


def signed(points, P, tris):
    Nv = C.vertex_normals(P, tris)
    tri, bary, dist, cp = C.Surface([('s', P, tris)]).query(points, k=8)
    return ((points - cp) * (Nv[tris[tri]] * bary[:, :, None]).sum(1)).sum(1)


def prism_hits(pts, P, tris, lo, hi, tol=0.02):
    """the per-triangle collider test: a point is in contact with a triangle when it projects INSIDE it and lies between
    lo (= -penetration, behind it) and hi (= the two margins, in front of it) along its winding normal. Returns per-triangle
    and per-point hit flags (an unsigned distance misses points sitting behind a tilted triangle - slit edges)"""
    A_, B_, C_ = P[tris[:, 0]], P[tris[:, 1]], P[tris[:, 2]]
    n = np.cross(B_ - A_, C_ - A_); nl = np.linalg.norm(n, axis=1); n = n / (nl[:, None] + 1e-12)
    e0, e1 = B_ - A_, C_ - A_; d00 = (e0 * e0).sum(1); d01 = (e0 * e1).sum(1); d11 = (e1 * e1).sum(1); den = d00 * d11 - d01 ** 2 + 1e-12
    th = np.zeros(len(tris), bool); ph = np.zeros(len(pts), bool)
    for s in range(0, len(pts), 256):
        q = pts[s:s + 256]; v = q[:, None, :] - A_[None]                     # (k, t, 3)
        sd = (v * n[None]).sum(2)
        d20 = (v * e0[None]).sum(2); d21 = (v * e1[None]).sum(2)
        b1 = (d11 * d20 - d01 * d21) / den; b2 = (d00 * d21 - d01 * d20) / den
        hit = (b1 >= -tol) & (b2 >= -tol) & (b1 + b2 <= 1 + tol) & (sd >= lo) & (sd < hi)
        th |= hit.any(0); ph[s:s + 256] = hit.any(1)
    return th, ph


def prism_rest(label, pos, tris, xs):
    """rest contacts the way a per-triangle collider sees them: every per-vertex / per-triangle pair the XML lets collide,
    points projecting inside a triangle between -penetration and the two margins"""
    bad = {}; where = []
    for a, A_ in xs.items():
        if A_['kind'] != 'per-vertex-shape' or a not in pos: continue
        for b, B_ in xs.items():
            if B_['kind'] != 'per-triangle-shape' or b not in pos or not K.collide(A_, B_) or not len(tris[b]): continue
            _, ph = prism_hits(np.asarray(pos[a]), np.asarray(pos[b]), np.asarray(tris[b]), -B_['pen'], A_['margin'] + B_['margin'])
            if ph.any():
                q = np.asarray(pos[a])[ph]; bad[f'{a} -> {b}'] = int(ph.sum())     # v4: say WHERE (the Officer blind-spot lesson)
                where.append(f'{a} -> {b} at ' + ', '.join(f'({x[0]:.1f}, {x[1]:.1f}, {x[2]:.1f})' for x in q[:4]))
    K.check(not bad, f'{label}: no rest contacts by triangle plane (in front within the margins / behind within the catch)' + ('' if not bad else f' {bad}; ' + '; '.join(where)))


# ==================== 2026-10-13: every hanging piece vs its copy at EVERY character weight ====================
HANG_SUFFIX = (' Tip Points', ' Flap Points', ' Bag Points', ' Hang Points', ' Sash Points', ' Tail Points')   # belt tail, hip loop, bag, hangers, sash end / pouch
REST_BUFFER = 0.4          # room a piece keeps over its copy beyond the two margins (user 2026-10-13: within 0.6 = pushed by a settling layer)
SWEEP_W = tuple(round(0.1 * i, 1) for i in range(11))


def hanging_pairs(xs):
    """(points shape, copy shape) for every hanging piece the XML lets collide with a hidden copy (legs / ground / helmet colliders out)"""
    out = []
    for a, A_ in xs.items():
        if A_['kind'] != 'per-vertex-shape' or not a.endswith(HANG_SUFFIX): continue
        for b, B_ in xs.items():
            if B_['kind'] != 'per-triangle-shape' or not K.collide(A_, B_): continue
            if any(w in b for w in ('Legs', 'VirtualGround', 'Torso Collide')): continue
            out.append((a, b, A_['margin'] + B_['margin'], B_['pen'] or 1.0))
    return out


def radial_facing(P, tris, cx, cy):
    """per triangle: unit normal . the unit outward (xy) direction from the body axis (< 0 = faces IN: FSMP pushes a point into the body)"""
    n = np.cross(P[tris[:, 1]] - P[tris[:, 0]], P[tris[:, 2]] - P[tris[:, 0]]); n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    c = P[tris].mean(1); r = np.c_[c[:, 0] - cx, c[:, 1] - cy]; r = r / (np.linalg.norm(r, axis=1, keepdims=True) + 1e-12)
    return (n[:, :2] * r).sum(1)


def rest_gap(q, P, tris, pen):
    """per point: the rest gap FSMP acts on - the LOWEST signed height over any triangle it projects into (behind it within the catch
    counts, negative), or the Euclidean distance to the nearest triangle when that is smaller (an edge counts); and the facing of the
    triangle that sets the height (nan = set by the distance)"""
    A_, B_, C_ = P[tris[:, 0]], P[tris[:, 1]], P[tris[:, 2]]
    n = np.cross(B_ - A_, C_ - A_); n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    e0, e1 = B_ - A_, C_ - A_; d00 = (e0 * e0).sum(1); d01 = (e0 * e1).sum(1); d11 = (e1 * e1).sum(1); den = d00 * d11 - d01 ** 2 + 1e-12
    h = np.full(len(q), np.inf); tix = np.full(len(q), -1)
    for s in range(0, len(q), 256):
        v = q[s:s + 256][:, None, :] - A_[None]
        sd = (v * n[None]).sum(2); d20 = (v * e0[None]).sum(2); d21 = (v * e1[None]).sum(2)
        b1 = (d11 * d20 - d01 * d21) / den; b2 = (d00 * d21 - d01 * d20) / den
        inside = (b1 >= -0.02) & (b2 >= -0.02) & (b1 + b2 <= 1.02) & (sd > -pen) & (sd < 3.0)
        hh = np.where(inside, sd, np.inf); h[s:s + 256] = hh.min(1); tix[s:s + 256] = np.where(np.isfinite(hh.min(1)), hh.argmin(1), -1)
    d = C.Surface([('s', P, tris)]).query(q, k=8)[2] if len(tris) else np.full(len(q), np.inf)
    return np.minimum(h, d), tix, h <= d


def weight_sweep(label, pos0, pos1, tris, xs, centre, weights=SWEEP_W, buffer=REST_BUFFER, check=True, verbose=False):
    """the game blends the _0 and _1 meshes vertex by vertex at the character's weight (guards wear these at random weights): every hanging
    piece's points vs their copy at every weight 0 .. 1 - points within the two margins + buffer of the copy, and copy triangles facing IN
    (FSMP pushes along the normal: an in-facing copy pulls a point into the body). FAIL on either at any weight. pos0 / pos1 / tris: dicts
    by shape name (positions as the game sees them, lifts included). Returns {pair: (worst gap, max near, max in-facing tris)}"""
    cx, cy = centre; res = {}; bad = []
    for a, b, mar, pen in hanging_pairs(xs):
        if a not in pos1 or b not in pos1 or not len(tris[b]): continue
        q0, q1, P0, P1, T_ = np.asarray(pos0[a]), np.asarray(pos1[a]), np.asarray(pos0[b]), np.asarray(pos1[b]), np.asarray(tris[b])
        worst, nmax, imax, umax, wat, rows = np.inf, 0, 0, 0, None, []
        for w in weights:
            q = (1 - w) * q0 + w * q1; P = (1 - w) * P0 + w * P1
            g, tix, by_plane = rest_gap(q, P, T_, pen); fr = radial_facing(P, T_, cx, cy)
            near = g < mar + buffer; nin = int((fr < 0).sum()); unc = int((tix < 0).sum())     # unc: points with NO copy triangle under them (a hole / past its edge)
            on_in = int((near & (tix >= 0) & by_plane & (fr[np.maximum(tix, 0)] < 0)).sum())
            if np.isfinite(g).any() and g.min() < worst: worst, wat = float(g.min()), w
            nmax = max(nmax, int(near.sum())); imax = max(imax, nin); umax = max(umax, unc)
            rows.append(f'w{w:.1f} {g.min():+.2f}/{int(near.sum())}' + (f'/in{nin}' if nin else '') + (f'(on-in {on_in})' if on_in else '') + f'/u{unc}')
        res[f'{a} -> {b}'] = (worst, nmax, imax, umax)
        msg = f'{a} -> {b}: worst gap {worst:+.2f} (w {wat}), max {nmax} of {len(q0)} pts within {mar + buffer:.1f}, in-facing copy tris max {imax} of {len(T_)}'
        if verbose: msg += f'; pts with no copy triangle under them max {umax}'
        if nmax or imax: bad.append(msg)
        if verbose: print(f'     {msg}\n        ' + ' '.join(rows))
    if check:
        K.check(not bad, f'{label}: every hanging piece rests clear of its copy (margins + {buffer}) with no in-facing copy triangle at weights '
                f'{weights[0]:.1f}..{weights[-1]:.1f} step {weights[1] - weights[0]:.1f} ({len(res)} pairs)' + ('' if not bad else ': ' + '; '.join(bad)))
    return res


# ==================== 2026-10-13: rigid bags (PLAN_BAGS.md - the bags 'stretch and bend weirdly') ====================
STRAIN_MAX = 0.005         # a rigid leather bag: its edges stretch less than 0.5 % in any pose


def node_world(n, T, names):
    """bind world 4x4 of bones / nodes by name: the skin's bind matrices, else the nif node's translation (physics roots nothing is weighted to)"""
    Gw = bone_world(T)
    for nm in names:
        if nm not in Gw and nm in n.nodes:
            M_ = np.eye(4); M_[:3, 3] = n.nodes[nm].global_transform.translation; Gw[nm] = M_
    return Gw


def rigid_weights(t, idx, bone):
    """points idx of shape t carry exactly one bone (>= 0.999): returns the indices that do not"""
    return [int(i) for i in idx if t.w[i].get(bone, 0.0) < 0.999]


def piece_strain(nif_path, piece, prefix, key, lim, idx, g='m', every=2, extra_clips=('mt_idle.hkx',)):
    """rest -> posed edge-length strain of a hanging piece's body (the triangles whose corners are all in idx): over the game's clips
    (smpkit.anim CLIPS + an idle clip found next to them; the physics bones held at rest on their parents) and with its chain swung
    rigidly about its root to every corner of its joint limits (lim: lo / hi per axis, the bone's own frame). A body weighted as one
    piece stays at 0; one weighted partly to the pelvis / a thigh and partly to its hinge bends or stretches.
    Returns (worst strain, {pose kind: worst})"""
    import itertools
    n, T = C.load(nif_path); C.to_world(T); S = {t.name: t for t in T}; t = S[piece]
    inb = np.zeros(len(t.pos), bool); inb[np.asarray(idx, int)] = True
    tri = t.tris[inb[t.tris].all(1)]
    E = np.unique(np.sort(np.vstack([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]]), axis=1), axis=0)
    L0 = np.linalg.norm(t.pos[E[:, 0]] - t.pos[E[:, 1]], axis=1); E = E[L0 > 1e-4]; L0 = L0[L0 > 1e-4]
    chain = [f'{prefix} {key} {r}' for r in range(8) if f'{prefix} {key} {r}' in n.nodes or any(f'{prefix} {key} {r}' in u.s2b for u in T)]
    Gw = node_world(n, T, chain)
    poses = []
    from smpkit import anim as A
    if A.configured(g):
        clips = dict(A.CLIPS[g])
        d0 = os.path.dirname(next(iter(clips.values())))
        for x in extra_clips:
            if os.path.exists(os.path.join(d0, x)): clips[x.replace('mt_', '').replace('.hkx', '')] = os.path.join(d0, x)
        for ck, cp in clips.items():
            for Dm in A.load_clip(cp, g)[0][::every]: poses.append((ck, Dm))
    if len(chain) > 1 and chain[0] in Gw and chain[1] in Gw:
        piv = Gw[chain[0]][:3, 3]; ax = Gw[chain[1]][:3, :3]
        lo, hi = lim['lo'], lim['hi']
        for cx_, cy_, cz_ in itertools.product(*[(lo[i], 0.0, hi[i]) for i in range(3)]):
            M = K.rot(ax[:, 0], cx_, piv) @ K.rot(ax[:, 1], cy_, piv) @ K.rot(ax[:, 2], cz_, piv)
            poses.append(('swing', {b: M for b in chain[1:]}))
    worst, per = 0.0, {}
    for lab, Dm in poses:
        P = skin(t.pos, t.w, Dm); L = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1)
        s = float(np.abs(L / L0 - 1.0).max()) if len(L0) else 0.0
        per[lab] = max(per.get(lab, 0.0), s); worst = max(worst, s)
    return worst, per, len(tri)
