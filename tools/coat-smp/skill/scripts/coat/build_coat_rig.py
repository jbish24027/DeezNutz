"""Coat builder (the skill's second garment builder): a coat whose skirt is WELDED INTO THE TORSO shape, with an inward
lining, a belt band + tail, a left-hip strap, a bag and a sash end - the Sons of Skyrim 2.0 rework builder made generic
(ported 2026-10-11 from E:/claude work/sos-smp-rework/build_sos.py; byte-identical output). Designs live in a DESIGN FILE
(paths + DESIGNS, see coat/designs/coat_example.py) that runs with this module's names in scope.
usage: build_coat_rig.py <designs.py> <design> [m] [f]
--- the original header follows ---
(E:/claude work/realistic-armor-hdt, v23 2026-10-11): the skirt rig, leg colliders, belt tail (RA v12 Sir Duncan tail on its
own chain + its own copy of the skirt under it, v14 leg follow), bag and hip plates are RA's code unchanged. Added here:
  * pants_comp: the trousers are a welded COMPONENT of the torso shape (Armors/ coats) - the leg colliders and the leg
    follow use only that component's triangles (point indices stay the shape's, so the women's slider data copies)
  * shader_donor (men): geometry from the author's BSA mesh, the shader block (PBR textures / flags) from a frozen copy
    of the PG-patched mesh in pbr_donors/ (the men's mod outranks the PG output, so its meshes carry PBR themselves)
  * role 'tail' (the sash end): a hanging piece on its own SASH_N-bone chain hinged at its top, very light and wind-driven,
    taking the leg share of the skirt under it, colliding with ITS OWN pulled-in copy of the skirt under it
  * per-design hanging-piece physics (strap_follow / flap_def / flap_lim / bag_share / bag_def / bag_lim / tip_def ...)
  * women: each design names its own .osp; the stage copy of the .osp starts from the INSTALLED override (the other
    coats keep their current physics) and only the rebuilt set is replaced, from the ORIGINAL set
MAP: designs + hanging-piece physics = the 'Sons of Skyrim 2.0 designs' block; pieces / tails / weights / colliders =
build(); XML = write_xml(); women's slider data + osp = bodyslide(). Report: rework_report.json (this folder, the name
RA's check scripts read); log: rework_<design>.log.
usage: build_sos.py <design> [m] [f]"""
import os, shutil, sys, json, copy
import numpy as np
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as KC     # v12: the stride poses + skinning for the stance-aware copies
load, Writer, subdivide_c, read_osd, write_osd = C.load, C.Writer, C.subdivide_c, C.read_osd, C.write_osd
NifFile, NiStringExtraData = C.NifFile, C.NiStringExtraData


class _NS: pass


# the project modules the original imported, served by the skill library under the same names
R = _NS(); R.is_skel, R.MAXB = C.is_skel, C.MAXB                                  # build_ra3ba
BW = _NS(); BW.chain_default_xyz = C.chain_default_xyz                             # build_wolf
B = _NS(); B.Surface, B.top, B.part_ids, B.to_world = C.Surface, C.top4, C.part_ids, C.to_world   # de_build
B.top4, B.tb2m, B.m2tb = C.top4, C.tb2m, C.m2tb
D = K = G = BWS = C                                                                  # build_duncan / build_aketon / aketon_geom / build_wolf_bs

wrap, smooth01, row_bracket, lin_bracket, frame = C.wrap, C.smooth01, C.row_bracket, C.lin_bracket, C.frame
PELV, ROOT = 'NPC Pelvis [Pelv]', 'NPC Root [Root]'
# set by use_designs(): the design file defines the paths and DESIGNS
MODS = None; WORK = HERE; DESIGNS = {}; STAGE = STAGE_M = STAGE_F = MOD_M = MOD_F = None; PRESET = None; TEX_ROOTS = []; BACKUPS = None; DESIGNS_PATH = None
NROW = 5
TIP_N = 3
TIP_BLEND, TIP_RIDE = 4.0, 0.9       # v6: 2.5 -> 4 - a longer belt->tail blend (user: tails bent sharply under the buckle)
# v10 (user: 'the belts on the tunics ... sway through the chainmail when its suppose to sit on top of that layer'; Northern Knight:
# 'it likes to sit under the chainmail'): riding 35% (v6) the tail's own 65% lags while the skirt swings out / forward - tail_all.py:
# 1-3 units into the skirt on 14 of 16 designs; the LNC men's 90% flat ride (v7) sank 0.63. Every tail now rides the layer
# under it 90% along its whole length (TIP_RIDE .35 -> .9, flat), keeping 10% of its own swing; still no collider (v6)
TIP_RIDE_FLAT = True
FLAP_FOLLOW = 0.95         # v2: each flap point follows the skirt right under it by this much (banded lames bend with the
                           # mail; v1 rode 0.3 of the plate's average = the mail outran the plate and came through it)
                           # v3c 0.7 -> 0.95: after a stop the plate's own hinge swings out of step with the mail and its
                           # share dipped the plate up to 1.2 (men) / 1.6 (women) into the mail (flap_swing.py); 0.95 -> 0.26 / 0.37
GAP_NEAR, GAP_FAR = 0.5, 3.5   # v2: skirt lying this close to the trousers moves exactly like them; this far off it swings
                               # (up to FREE_MAX)
FREE_SIGMA = 3.0           # the swing share is smoothed over the cloth by this much
FREE_MAX = 0.8            # v2c: at most this much of the skirt swings freely; the rest always follows the legs (a sprint
                          # stride outruns a fully free skirt: it was carried 0.01 units by the legs vs the author's 1.9)
LEG_FACING = 0.25          # v2c: leg triangles facing forward (normal y > this) / backward / sideways (|x| > SIDE_FACING)
SIDE_FACING = 0.6
SEAM_FADE = 4.0            # v3b: a skirt cut out of a bigger shape fades its physics + leg-follow to 0 over this distance to the cut
BAG_SHARE = 0.62           # a bag without the author's bag weights (women's 3BA projects): this much on its own bone, as the author did
FRONT_DEG = 55.0           # skirt lining within this of straight ahead / behind collides with the leg fronts / backs, the rest with the sides
LEG_SIGMA = 3.0            # the trousers' weights the skirt borrows are smoothed over this much
CHAIN_SPACING = 32.0       # degrees between chains inside a panel (aim)
MAX_CHAINS = 12            # bone budget: 12 x 5 + the skeleton bones stays under 80 per shape
PMIN_C, LEG_CLEAR, LEG_MAXIN, LINING_MIN_GAP, TB_CLEAR, LEG_ZMIN = 0.2, 0.8, 3.0, 0.6, 0.6, 15.0
# v12: the belt tail meets its OWN copy of the skirt (and flap plates) under it, pulled in only as far as the tail needs to
# rest clear (margins .1 + .1 + .15): the shared skirt-outer collider is pulled in up to 2 units for the flaps / bag, which
# would let the tail sink that far into the visible skirt before being caught
TIP_CLEAR = 0.4           # v12: .35 -> .4 after the exact pass (a buffer for the BodySlide presets)
# v12: tails the author drew INTO the skirt (Long Nordic Chainmail men: 43 of 157 points, up to 1.5 deep where the mail
# bulges over the right thigh) are lifted out to rest TIP_LIFT on top of it - otherwise their collider has to be pulled in
# behind them and the rest of the strap sinks that far before it is caught. Lift spread over the strap (soft max over
# neighbours, sigma TIP_LIFT_SIGMA) so its faces move together, along the skirt's outward normal, faded in with the tail's own
# share (the strap stays joined to the band). Recorded in rework_report.json ('lift') so verify_rework can undo it.
TIP_LIFT, TIP_LIFT_SIGMA = 0.15, 1.5
# v14 (user: 'the belt is getting stuck and twitching on the long nordic chainmail'): tail_idle.py - with every physics bone
# held still and only the legs moving, the mail under the LNC men's strap (thigh share ~.13) met the strap's collider in an
# idle stance (6 pts) and every right-leg stride (walk 49, run 39); Nordic Chainmail / Nord Padded / LNC women in runs. The
# strap now follows the legs as much as the surface under it does
TIP_LEG_FOLLOW = 1.0
TIP_LAT = 0.8


def prism_min_sd(pts, P, tris, lo, hi, tol=0.02):
    """v15b: per triangle, the lowest height (along its winding normal) of the points that project INSIDE it with
    lo <= height < hi - the way a per-triangle collider decides contact (inf = none). The unsigned nearest distance used
    before missed points sitting behind a tilted triangle: the plane audit found resting belt-tail / tasset contacts"""
    A_, B_, C_ = P[tris[:, 0]], P[tris[:, 1]], P[tris[:, 2]]
    n = np.cross(B_ - A_, C_ - A_); n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    e0, e1 = B_ - A_, C_ - A_; d00 = (e0 * e0).sum(1); d01 = (e0 * e1).sum(1); d11 = (e1 * e1).sum(1); den = d00 * d11 - d01 ** 2 + 1e-12
    out = np.full(len(tris), np.inf)
    for s_ in range(0, len(pts), 256):
        v = pts[s_:s_ + 256][:, None, :] - A_[None]
        sd = (v * n[None]).sum(2); d20 = (v * e0[None]).sum(2); d21 = (v * e1[None]).sum(2)
        b1 = (d11 * d20 - d01 * d21) / den; b2 = (d00 * d21 - d01 * d20) / den
        hit = (b1 >= -tol) & (b2 >= -tol) & (b1 + b2 <= 1 + tol) & (sd >= lo) & (sd < hi)
        out = np.minimum(out, np.where(hit, sd, np.inf).min(0))
    return out


def umr(Dz, name):
    """a design's 'under_min_radial' for one piece: a float for all, or a dict per piece (v8d: the sash's curled edge needs 0.7)"""
    v = Dz.get('under_min_radial', 0.0)
    return float(v.get(name, v.get('*', 0.0))) if isinstance(v, dict) else float(v)


def umr_tip(Dz, name):
    """2026-10-14 (Whiterun-rig job): the BELT TIP's own radial filter (tip_min_radial) - under_min_radial also filters the sash / tail copy
    (the same skirt layer), so setting it for the tip changed the Heavy's sash collider (554 -> 537 tris); unset = under_min_radial"""
    return float(Dz['tip_min_radial']) if Dz.get('tip_min_radial') is not None else umr(Dz, name)


def radial_dot(P, tris, cx, cy):
    """per triangle: its unit normal . the unit outward (xy) direction from the skirt axis (1 = facing straight out, 0 = a side
    face, < 0 = facing in). Officer v4: the hanging pieces' under-colliders keep only faces above a design's 'under_min_radial'
    (the plates' rims and edge faces, 29 of the sash's 391 triangles, pushed the sash sideways; 7 faced inward and pulled it in)"""
    fn = np.cross(P[tris[:, 1]] - P[tris[:, 0]], P[tris[:, 2]] - P[tris[:, 0]]); fn = fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
    cc = P[tris].mean(1); r = np.c_[cc[:, 0] - cx, cc[:, 1] - cy]; r = r / (np.linalg.norm(r, axis=1, keepdims=True) + 1e-12)
    return (fn[:, :2] * r).sum(1)


def rec_lift(shared, variant, name, idx, offs):
    """a piece's recorded lift (verify undoes it point for point) - MERGED when a piece is lifted twice (v7: the sash is rotated with
    the plates it is sewn to and then lifted onto them)"""
    d = shared.setdefault('lift', {}).setdefault(variant, {})
    if name in d:
        acc = {int(i): np.array(o, float) for i, o in zip(*d[name])}
        for i, o in zip(idx, offs): acc[int(i)] = acc.get(int(i), np.zeros(3)) + np.asarray(o, float)
        ks = sorted(acc); d[name] = [ks, [acc[k].tolist() for k in ks]]
    else:
        d[name] = [[int(i) for i in idx], [[float(c) for c in o] for o in offs]]


def prism_sd(q, P, TT, lo=-6.0, hi=3.0):
    """per point: the signed height over the triangle it projects into (+ = the triangle's front), nan = none within reach
    (layer_check.prism; here to find lining points that start BEHIND a layer collider = sewn there)"""
    A_, B_, C_ = P[TT[:, 0]], P[TT[:, 1]], P[TT[:, 2]]
    n = np.cross(B_ - A_, C_ - A_); n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    e0, e1 = B_ - A_, C_ - A_; d00 = (e0 * e0).sum(1); d01 = (e0 * e1).sum(1); d11 = (e1 * e1).sum(1); den = d00 * d11 - d01 ** 2 + 1e-12
    out = np.full(len(q), np.nan)
    for s_ in range(0, len(q), 128):
        v = q[s_:s_ + 128][:, None, :] - A_[None]
        sd = (v * n[None]).sum(2); d20 = (v * e0[None]).sum(2); d21 = (v * e1[None]).sum(2)
        b1 = (d11 * d20 - d01 * d21) / den; b2 = (d00 * d21 - d01 * d20) / den
        hit = (b1 >= -0.02) & (b2 >= -0.02) & (b1 + b2 <= 1.02) & (sd > lo) & (sd < hi)
        best = np.where(hit, np.abs(sd), np.inf).argmin(1); ok = hit[np.arange(len(best)), best]
        out[s_:s_ + 128][ok] = sd[np.arange(len(best)), best][ok]
    return out


def prism_sd_min(q, P, TT, lo=-4.0, hi=3.0):
    """per point: the LOWEST signed height over any triangle it projects into with lo < height < hi (nan = none) - what a per-triangle
    collider with that catch sees first (prism_sd takes the nearest triangle; a fold or curled corner in front of the point is missed)"""
    A_, B_, C_ = P[TT[:, 0]], P[TT[:, 1]], P[TT[:, 2]]
    n = np.cross(B_ - A_, C_ - A_); n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    e0, e1 = B_ - A_, C_ - A_; d00 = (e0 * e0).sum(1); d01 = (e0 * e1).sum(1); d11 = (e1 * e1).sum(1); den = d00 * d11 - d01 ** 2 + 1e-12
    out = np.full(len(q), np.nan)
    for s_ in range(0, len(q), 128):
        v = q[s_:s_ + 128][:, None, :] - A_[None]
        sd = (v * n[None]).sum(2); d20 = (v * e0[None]).sum(2); d21 = (v * e1[None]).sum(2)
        b1 = (d11 * d20 - d01 * d21) / den; b2 = (d00 * d21 - d01 * d20) / den
        hit = (b1 >= -0.02) & (b2 >= -0.02) & (b1 + b2 <= 1.02) & (sd > lo) & (sd < hi)
        m = np.where(hit, sd, np.inf).min(1); ok = np.isfinite(m)
        out[s_:s_ + 128][ok] = m[ok]
    return out


class _shared_lock:
    """2026-10-13: a lock file beside a file several parallel builds rewrite (the .osp, rework_report.json): O_EXCL create, retry 2 min"""
    def __init__(self, path): self.lp = path + '.lock'
    def __enter__(self):
        import time as _t
        t0 = _t.time(); os.makedirs(os.path.dirname(self.lp), exist_ok=True)
        while True:
            try: self.fd = os.open(self.lp, os.O_CREAT | os.O_EXCL | os.O_WRONLY); return self
            except FileExistsError:
                if _t.time() - t0 > 120: raise RuntimeError(f'lock held too long: {self.lp}')
                _t.sleep(0.2)
    def __exit__(self, *a):
        os.close(self.fd)
        try: os.remove(self.lp)
        except OSError: pass


def pull_exact(P, TT, off, pts, clear, max_in=2.0, iters=12, pen=2.0, Nv=None):
    """v12: after K.pull_in (vertex-normal heights within a lateral reach), push the triangle nearest each point that is
    still closer than `clear` further in until every point clears it (a short reach misses big triangles under a point).
    v15b: and every triangle a point sits over (or behind, within the collider's catch `pen`) closer than `clear`.
    2026-10-13: Nv = the directions the offsets move along (default: P's vertex normals) - a BodySlide build moves the written copy
    (pulled along the BASE shape's normals) by its slider data, so its exact pass runs on the morphed points along the base normals"""
    Nv = K.vertex_normals(P, TT) if Nv is None else Nv; off = np.array(off, float)
    for _ in range(iters):
        Q = P - off[:, None] * Nv
        tri, _, d, _ = B.Surface([('u', Q, TT)]).query(pts, k=8)
        bad = np.where(d < clear - 0.01)[0]
        tmin = prism_min_sd(pts, Q, TT, -pen, clear - 0.01); badt = np.where(np.isfinite(tmin))[0]
        if not len(bad) and not len(badt): break
        for i in bad:
            for vx in TT[tri[i]]: off[vx] = min(max_in, off[vx] + (clear - d[i]) * 1.2 + 0.02)
        for t in badt:
            for vx in TT[t]: off[vx] = min(max_in, off[vx] + (clear - tmin[t]) * 1.1 + 0.02)
    return off


# 2026-10-13 (user: the Officer's belt tail + sash and the Heavy Reinforced's sash + hip loop twitch for 1-2 s after a stop, the hip
# hangers at idle; 'Guards wear these armours at random weights, so every fix ... has to hold at EVERY weight'). Measured on the
# installed meshes (sos-smp-rework tools/rest_sweep.py, weights 0..1 in 0.1 steps, women at BodySlide's small / big ends): the copies
# under the hanging pieces were pulled only TIP_CLEAR .4 (belt tail, hangers, the default sash) / .6 (TB_CLEAR: hip loop, bag) / .8
# (pouches) clear of their points - with the two margins .2-.25 that left ~.2 of room, and the layer under a piece, settling after a
# stop, pushes it through that (belt tails 14-32 pts within .6 on the Officer / guards, sashes 11-26, hangers up to 132; women's big
# builds closed a pouch to .20); and pulled copies carried triangles facing INTO the body (Heavy hip loop copy 45, Braided 34, the
# GuardHeavy pouch copy 24 - the Heavy's loop rested 2.9 inside its copy at weight .5). Now every copy under a hanging piece (belt
# tail, sash end / pouch / bag, hip loop, hangers) is pulled HANG_CLEAR clear of its points (the exact pass kept; women: on every
# BodySlide build too - the set defaults and the user's preset, small and big - along the base normals the written copy moves on);
# a triangle the pull folds to face in gets the largest pull of its corners on all three (a uniform offset keeps its facing); one
# still facing in on any weight, build or blend between them is dropped from the copy on EVERY weight (main() builds again with it
# out - the _0 / _1 pair keeps one triangle list). verify sweeps every weight (coat_lib.weight_sweep): FAIL on a point within the
# margins + REST_BUFFER .4 or on an in-facing copy triangle. A design may set hang_clear; older tb_clear / tail_clear act as minimums.
HANG_CLEAR = 1.0


def _edges(T):
    E = np.unique(np.sort(np.vstack([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), axis=1), axis=0)
    return E


def slope_limit(off, T, P, s, cap=2.0, iters=400):
    """2026-10-13: a gentle pull - raise the shallow end of every edge until the two ends' offsets differ by at most s x its length
    (offsets only grow, so every clearance holds); a step from the 2.0 cap to ~0 across one coarse triangle is what folds it"""
    E = _edges(T); L = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1); o = np.array(off, float)
    for _ in range(iters):
        o2 = o.copy()
        np.maximum.at(o2, E[:, 0], o[E[:, 1]] - s * L); np.maximum.at(o2, E[:, 1], o[E[:, 0]] - s * L)
        o2 = np.minimum(o2, cap)
        if np.abs(o2 - o).max() < 1e-6: break
        o = o2
    return o


def smooth_dirs(Nv, T, iters=8):
    """2026-10-13: the directions a copy's points are pulled along, averaged over their neighbours (a crease's vertex normals part, so even
    an even pull folds the triangles between them); unit length"""
    E = _edges(T); D = np.array(Nv, float)
    for _ in range(iters):
        acc = D.copy(); np.add.at(acc, E[:, 0], D[E[:, 1]]); np.add.at(acc, E[:, 1], D[E[:, 0]])
        D = acc / (np.linalg.norm(acc, axis=1, keepdims=True) + 1e-12)
    return D


def local_dirs(Nv, Rad, T, seed, rings=2):
    """2026-10-13: the pull directions around some vertices (a fold's corners) turned to Rad (straight in toward the body axis), blended
    back to the vertex normals over `rings` rings of neighbours; the rest of the copy keeps its normals"""
    E = _edges(T); a = np.zeros(len(Nv)); a[np.asarray(seed, int)] = 1.0; m = a > 0
    for r in range(rings):
        nb = np.zeros(len(Nv), bool); nb[E[:, 0][m[E[:, 1]]]] = True; nb[E[:, 1][m[E[:, 0]]]] = True
        a = np.maximum(a, np.where(nb & ~m, 1.0 - (r + 1) / (rings + 1.0), 0.0)); m |= nb
    D = (1.0 - a)[:, None] * np.asarray(Nv, float) + a[:, None] * np.asarray(Rad, float)
    return D / (np.linalg.norm(D, axis=1, keepdims=True) + 1e-12)


def cdir(shared, key, P, T):
    """the directions a copy was pulled along (finish_copy stores them when it repaired a fold; else the vertex normals, as always)"""
    d = shared.get(key + '#dir')
    return d if d is not None and len(d) == len(P) else K.vertex_normals(P, T)


def coarsen(P, T, frac, iters=22):
    """2026-10-13 PERF (PLAN_PERF_WHITERUN.md 2): a collider copy at collider resolution - the triangles T over points P clustered to about
    frac of their count. Every cluster keeps one REAL point (the member nearest its mean), so the result indexes the source's own points and
    everything keyed by them (weights, pull offsets, BodySlide displacements, the women's slider provenance) works unchanged; clusters are
    split by the dominant direction of the vertex normal (a lining never merges with the face over it, nor the two sides of a thin plate).
    A triangle that collapses is dropped, a duplicate kept once, one whose normal turns more than ~70 deg from its source triangles' is
    dropped. Deterministic (a pure function of P, T, frac): the same on every pass. Returns the coarse triangles (n, 3)."""
    T = np.asarray(T, int).reshape(-1, 3)
    if frac is None or frac >= 1.0 or len(T) < 12: return T
    v = np.unique(T); Q = P[v]; rm = np.full(len(P), -1); rm[v] = np.arange(len(v)); Tl = rm[T]
    fn = np.cross(Q[Tl[:, 1]] - Q[Tl[:, 0]], Q[Tl[:, 2]] - Q[Tl[:, 0]])          # area-weighted face normals
    nv = np.zeros_like(Q)
    for j in range(3): np.add.at(nv, Tl[:, j], fn)
    nv /= np.linalg.norm(nv, axis=1, keepdims=True) + 1e-12
    dk = np.argmax(np.abs(nv), axis=1) * 2 + (nv[np.arange(len(nv)), np.argmax(np.abs(nv), axis=1)] < 0)
    le = float(np.mean(np.linalg.norm(Q[Tl] - np.roll(Q[Tl], 1, axis=1), axis=2)))
    target = frac * len(T)

    def build(h):
        cell = np.floor(Q / h).astype(np.int64)
        _, cl = np.unique(np.c_[cell, dk], axis=0, return_inverse=True); cl = cl.ravel(); nc = int(cl.max()) + 1
        mean = np.zeros((nc, 3)); np.add.at(mean, cl, Q); cnt = np.bincount(cl, minlength=nc); mean /= cnt[:, None]
        d = np.linalg.norm(Q - mean[cl], axis=1)
        order = np.lexsort((d, cl)); first = np.r_[True, cl[order][1:] != cl[order][:-1]]
        rep = np.empty(nc, int); rep[cl[order][first]] = order[first]
        R = rep[cl][Tl]
        ok = (R[:, 0] != R[:, 1]) & (R[:, 1] != R[:, 2]) & (R[:, 0] != R[:, 2])
        R, F = R[ok], fn[ok]
        key = np.sort(R, axis=1); _, ui, inv = np.unique(key, axis=0, return_index=True, return_inverse=True); inv = inv.ravel()
        acc = np.zeros((len(ui), 3)); np.add.at(acc, inv, F)                  # the source triangles' summed normal per coarse triangle
        R = R[ui]; nn = np.cross(Q[R[:, 1]] - Q[R[:, 0]], Q[R[:, 2]] - Q[R[:, 0]])
        cosang = (nn * acc).sum(1) / (np.linalg.norm(nn, axis=1) * np.linalg.norm(acc, axis=1) + 1e-12)
        R = R[cosang > 0.34]
        return R[np.argsort(ui[cosang > 0.34])]                                # in source order (stable ids)

    lo, hi = 0.3 * le, 12.0 * le; best = None
    for _ in range(iters):
        h = 0.5 * (lo + hi); R = build(h)
        if len(R) > target: lo = h
        else:
            hi = h; best = R
    if best is None: best = build(hi)
    return v[best]


def coarse_sag(PC, TC, cparts, Nv, cx, cy, iters=3, cap=1.0):
    """2026-10-14 item 4 (Fable audit_regress: the performance pass's copy_res pulled curved collider copies INSIDE their drawn surface -
    Eastmarch heavy pouch -.61, Officer hangers -.46, Breastplate sash -.52): a coarse copy's triangles are chords of the curved surface it
    was decimated from, so they sit inside it by their sag. Per copy vertex the outward move (along Nv) that brings every coarse triangle's
    centroid and edge midpoints back ONTO the original surface (the source pieces' outward faces; signed height over the face each
    projects into, the nearest by |h|); the largest need of the triangles around a vertex, iterated, capped. -> (n,) >= 0"""
    FV, FF, o_ = [], [], 0
    for q, v in cparts:
        m_ = G.outer_mask(q.pos, q.tris, cx, cy); FV.append(q.pos); FF.append(q.tris[m_] + o_); o_ += len(q.pos)
    if not FF: return np.zeros(len(PC))
    FV = np.vstack(FV); FF = np.vstack(FF)
    A_, B_, C_ = FV[FF[:, 0]], FV[FF[:, 1]], FV[FF[:, 2]]; Nf = np.cross(B_ - A_, C_ - A_); ln = np.linalg.norm(Nf, axis=1); ok = ln > 1e-9; Nf[ok] /= ln[ok][:, None]
    v0, v1 = B_ - A_, C_ - A_; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); den = d00 * d11 - d01 * d01

    def h_over(Q):
        out = np.full(len(Q), np.nan)
        for s0 in range(0, len(Q), 48):
            q = Q[s0:s0 + 48]; h = np.einsum('nmk,mk->nm', q[:, None, :] - A_[None], Nf); w2 = (q[:, None, :] - h[..., None] * Nf[None]) - A_[None]
            d20 = np.einsum('nmk,mk->nm', w2, v0); d21 = np.einsum('nmk,mk->nm', w2, v1)
            with np.errstate(divide='ignore', invalid='ignore'):
                vv = (d11 * d20 - d01 * d21) / den; ww = (d00 * d21 - d01 * d20) / den
            h = np.where((vv >= -0.02) & (ww >= -0.02) & (vv + ww <= 1.02) & ok[None] & (np.abs(h) < 3.0), h, np.nan)
            ah = np.where(np.isnan(h), np.inf, np.abs(h)); j = ah.argmin(1); hh = h[np.arange(len(q)), j]; hh[~np.isfinite(ah.min(1))] = np.nan; out[s0:s0 + 48] = hh
        return out
    comp = np.zeros(len(PC))
    for _ in range(iters):
        Q = PC + comp[:, None] * Nv; a_, b_, c_ = Q[TC[:, 0]], Q[TC[:, 1]], Q[TC[:, 2]]
        samples = [(a_ + b_ + c_) / 3.0, (a_ + b_) / 2.0, (b_ + c_) / 2.0, (c_ + a_) / 2.0]
        need = np.zeros(len(TC))
        for sm in samples:
            hh = h_over(sm); need = np.maximum(need, np.where(np.isfinite(hh), np.maximum(0.0, -hh), 0.0))
        if need.max() < 0.01: break
        add = np.zeros(len(PC))
        for c in range(3): np.maximum.at(add, TC[:, c], need)
        comp = np.minimum(cap, comp + add)
    return comp


def keep_mask(shared, mkey, mask):
    """a copy's triangle selection minus the triangles main() dropped for facing in on some weight (by the selection's own key)"""
    d = shared.get('copy_drop', {}).get(mkey)
    if not d: return mask
    m = np.array(mask, bool).copy(); m[sorted(d)] = False
    return m


def hang_proxy(tris, idx, step, pos=None):
    """2026-10-13 PERF (PLAN_PERF_WHITERUN.md 4): the hip hangers' collision-point proxy - every other point. The hanger points idx (rings +
    straps) keep EVERY point on their own mesh boundary (both edge rows of a strap, a ring's rims: where a gap would let an edge through)
    and drop a maximal independent set of the interior points, in index order - no two neighbours both dropped, so every dropped point has
    a kept one an edge away. step 2 only. Returns the kept indices (sorted, a subset of idx)."""
    if step <= 1 or not len(idx): return np.asarray(idx)
    assert step == 2, 'hang_pts_step: 2 only'
    idx = np.asarray(idx)
    if pos is not None:      # 2026-10-14 (user: 'Change 1 yes'): the seam twins first - the hanger mesh is split at its UV / normal seams, so
        # every seam was an open 'boundary' kept whole (Whiterun light: 658 of 908 boundary, 552 of them a twin at the same spot) and the
        # proxy only reached 810. One point per position (the lowest index; a twin adds nothing to a per-vertex collider), the triangles
        # re-indexed onto it, then the same rule: true rims kept, every other interior point. Measured: light 908 -> 498, heavy 407 -> 221
        rep_, first_ = {}, {}
        for i in sorted(int(x) for x in idx): rep_[i] = first_.setdefault(tuple(np.round(pos[i], 4)), i)
        tris = np.array([[rep_.get(int(x), int(x)) for x in t] for t in tris])
        tris = tris[(tris[:, 0] != tris[:, 1]) & (tris[:, 1] != tris[:, 2]) & (tris[:, 0] != tris[:, 2])]
        idx = np.array(sorted(set(rep_.values())), int)
    inn = np.zeros(int(max(tris.max(), idx.max())) + 1, bool); inn[idx] = True
    tt = tris[inn[tris].all(1)]; cnt = {}
    for a, b, c in tt:
        for u, v in ((a, b), (b, c), (c, a)):
            k = (min(int(u), int(v)), max(int(u), int(v))); cnt[k] = cnt.get(k, 0) + 1
    nb = defaultdict(set); bnd = set()
    for (u, v), c in cnt.items():
        nb[u].add(v); nb[v].add(u)
        if c == 1: bnd.update((u, v))
    drop = set()
    for i in sorted(int(x) for x in idx):
        if i in bnd or not nb[i]: continue
        if not (nb[i] & drop): drop.add(i)
    return np.array(sorted(set(int(x) for x in idx) - drop), int)


def flap_cuirass(S, T, rest, cfg, shared):
    """2026-10-14 HOLDS (flap_settle): the cuirass the hip strap hangs against as a pseudo-piece - the static shape flap_settle['surf']
    (default cfg['static'][0]), its kept triangles minus the trousers component (cfg pants / pants_comp), decided once on _1"""
    fs = cfg.get('flap_settle_surf') or cfg['static'][0]; t = S[fs]
    if 'flapc_tm' not in shared:
        tm = np.asarray(rest.get(fs, np.ones(len(t.tris), bool)), bool).copy()
        if fs == cfg.get('pants') and cfg.get('pants_comp') is not None:
            lab = D.welded_components(t.pos, t.tris); tm &= ~np.isin(lab[t.tris], cfg['pants_comp']).all(1)
        shared['flapc_tm'] = tm
    return Piece(fs, fs, 'cuirass', t.pos, t.uv, None, t.w, t.tris[shared['flapc_tm']], None, np.arange(len(t.pos)))


def radial_height(Q, cx, cy, V, F, reach=5.0):
    """2026-10-14 HOLDS: each point's height over the triangles V[F] measured the way a radial settle pushes - a horizontal ray from the body
    axis at the point's height through it; the outermost hit no farther than reach beyond the point (a sleeve / hand beside the hip is not
    the surface under it). h = point radius - hit radius (> 0: in front); nan where the ray meets none"""
    o = np.c_[np.full(len(Q), cx), np.full(len(Q), cy), Q[:, 2]]; dv = Q - o; dv[:, 2] = 0; r = np.linalg.norm(dv, axis=1); d = dv / np.maximum(r, 1e-9)[:, None]
    A, B_, C_ = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]; e1, e2 = B_ - A, C_ - A; out = np.full(len(Q), np.nan)
    for s in range(0, len(Q), 64):
        dd = d[s:s + 64][:, None, :]; oo = o[s:s + 64][:, None, :]
        pv = np.cross(dd, e2[None]); det = (e1[None] * pv).sum(2); ok = np.abs(det) > 1e-9; inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
        tv = oo - A[None]; u = (tv * pv).sum(2) * inv; qv = np.cross(tv, e1[None]); v = (dd * qv).sum(2) * inv; t = (e2[None] * qv).sum(2) * inv
        hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0) & (t < (r[s:s + 64] + reach)[:, None])
        tt = np.where(hit, t, -np.inf).max(1); tt[~np.isfinite(tt)] = np.nan; out[s:s + 64] = tt
    return r - out


def flap_wrap(flaps, flab, plates, belt, cx, cy, shared):
    """2026-10-14 HOLDS: the hip strap's points that WRAP the belt (an outward horizontal ray from the point meets the belt piece within
    3.0) - they stay where the author drew them and are no collision points; decided once on _1. Returns the strap's other points
    (of its plate components) = the points flap_settle settles and flap_pts 'strap' collides"""
    if 'flap_free' not in shared:
        v = np.where(np.isin(flab, plates))[0]; Q = flaps.pos[v]
        u = np.c_[Q[:, 0] - cx, Q[:, 1] - cy, np.zeros(len(Q))]; u /= np.linalg.norm(u, axis=1, keepdims=True) + 1e-12
        wr = np.zeros(len(v), bool)
        if len(belt.tris):
            A, B_, C_ = belt.pos[belt.tris[:, 0]], belt.pos[belt.tris[:, 1]], belt.pos[belt.tris[:, 2]]; e1, e2 = B_ - A, C_ - A
            for i in range(len(v)):
                h = np.cross(u[i], e2); a = (e1 * h).sum(1); ok = np.abs(a) > 1e-9; f = np.where(ok, 1.0 / np.where(ok, a, 1.0), 0.0)
                s = Q[i] - A; uu = f * (s * h).sum(1); q = np.cross(s, e1); vv = f * (q @ u[i]); tt = f * (e2 * q).sum(1)
                wr[i] = bool((ok & (uu >= -1e-4) & (vv >= -1e-4) & (uu + vv <= 1 + 1e-4) & (tt > 0.0) & (tt < 3.0)).any())
        shared['flap_free'] = v[~wr]; shared['flap_wrapn'] = int(wr.sum())
        # the settle fades in over 2.0 from the wrap (Riften first build: the edge between a settled point and a wrap point stretched x5,
        # +1.14); the points inside that fade are no collision points (they rest closer than the copy clearance, held by the belt's ends)
        dw = np.min(np.linalg.norm(Q[~wr][:, None] - Q[wr][None], axis=2), axis=1) if wr.any() else np.full(int((~wr).sum()), np.inf)
        shared['flap_fade'] = np.clip(dw / 2.0, 0.0, 1.0) ** 2 * (3 - 2 * np.clip(dw / 2.0, 0.0, 1.0))
        shared['flap_coll'] = v[~wr][dw >= 2.0]
    return shared['flap_free']


def copy_frac(Dz, cfg, kind):
    """2026-10-13 PERF: design key copy_res - a float (every copy kind) or {kind: frac} for kind in legs / tipu / hangu / tailu; None = the
    author's resolution (unchanged)"""
    r = cfg.get('copy_res', Dz.get('copy_res'))
    if r is None: return None
    return r.get(kind) if isinstance(r, dict) else float(r)


def copy_tris(shared, Dz, cfg, kind, q, mk_, tsel):
    """a copy's triangles (indices into q.pos) and their drop ids. At the author's resolution: the selection minus its dropped triangles
    (as always). With copy_res: the selection coarsened ONCE (the first call - the _1 build - and reused on _0 and every pass, rule 6),
    then minus ITS dropped triangles, keyed '<selection>#c' (finish_copy records in-facing coarse triangles under that key)"""
    fr = copy_frac(Dz, cfg, kind)
    if not fr:
        ts = keep_mask(shared, mk_, tsel)
        return q.tris[ts], [(mk_, int(i)) for i in np.where(ts)[0]]
    ck = ('coarse', mk_)
    if ck not in shared:
        shared[ck] = coarsen(q.pos, q.tris[np.asarray(tsel, bool)], fr)
    ct = shared[ck]; m = keep_mask(shared, mk_ + '#c', np.ones(len(ct), bool))
    return ct[m], [(mk_ + '#c', int(i)) for i in np.where(m)[0]]


def morph_builds(shared, T, ss_override=None):
    """women: each source shape's slider displacement at BodySlide's small and big ends, under the set's defaults and under the user's
    preset (PRESET) - [(label, {source shape: (n, 3)})], the builds verify sweeps"""
    if 'f_morph' in shared: return shared['f_morph']
    fp = shared['f_paths']; _, _, entries = read_osd(fp['osd']); ss = ss_override if ss_override is not None else fp['ss']
    nverts = {t.name: len(t.pos) for t in T}
    data = BWS.slider_data(ss, entries, set(nverts), nverts)
    pre = KC.preset(*PRESET) if PRESET else {}
    out = []
    for lab, pr in (('defaults', {}), ('user preset', pre)):
        for size in ('small', 'big'):
            Dm = {}
            for sl in ss.findall('Slider'):
                f = pr.get((sl.get('name'), size), float(sl.get(size))) / 100.0
                if sl.get('invert') == 'true': f = 1.0 - f
                if abs(f) < 1e-9: continue
                for shp, arr in data.get(sl.get('name'), {}).items(): Dm[shp] = Dm.get(shp, 0.0) + f * arr
            out.append((f'{lab} {size}', Dm))
    shared['f_morph'] = out
    return out


def piece_disp(p, Dm):
    """a piece's per-point displacement in one BodySlide build, the way bodyslide() writes its slider data (split points = the mean of
    their edge's ends)"""
    out = np.zeros((len(p.pos), 3)); arr = Dm.get(p.src) if p.src is not None else None
    if arr is None or np.ndim(arr) != 2: return out
    n0 = p.n0 or len(p.pos); out[:n0] = arr[p.src_idx[:n0]]
    for j, (a, b) in enumerate(p.mids): out[n0 + j] = (out[a] + out[b]) / 2
    return out
SLIT_MAX_HW = 25.0         # wider gaps at the hem are hem shape, not slits
SHEET_ON_LAYER = 1.0       # a single-sheet skirt layer's points this close to another layer lie on it (no lining there)

# ====================================================================== Sons of Skyrim 2.0 designs (2026-10-11)
# Forked from Realistic Armor's build_rework.py (v23, its belts = the user-confirmed v12 Sir Duncan tails + v14 leg follow).
# Requests per armour: REQUESTS.md. Mesh facts: MAP.md (+ its CORRECTIONS). Stages mirror the two mods this replaces in place:
#   men   -> stage/m/ = [NoDelete] Sons of Skyrim 2.0 - SMP Physics              (must stay HIGHER priority than the PG output)
#   women -> stage/f/ = [NoDelete] Sons of Skyrim 2.0 - SMP Physics - 3BA BodySlide (higher than Sons of Skyrim - HIMBO and 3BA)
TIP_RIDE = 0.0              # RA v12: the belt tail hangs on its own chain only and collides with its own copy of the skirt under it
LOW_FROM = 4                # RA v13: rows from here down use SK_LIM_LOW when a preset has one
TWO_LAYER = {}              # RA's two-layer pass B is not used here
PHYS_FLOW = dict(SK_DEF=dict(mass=0.8, inertia=38.0, lin=0.55, ang=0.6, friction=0.0, wind=0.2),
                 SK_LIM1=dict(lo=(-1.1, -0.3, -0.12), hi=(0.08, 0.3, 0.12), lin=0.0, stiff=(24, 6, 6)),
                 SK_LIM=dict(lo=(-0.7, -0.3, -0.12), hi=(0.08, 0.3, 0.12), lin=0.0, stiff=(12, 4, 4)),
                 SK_LIM_LOW=dict(lo=(-0.9, -0.4, -0.18), hi=(0.08, 0.4, 0.18), lin=0.0, stiff=(4, 2, 2)),
                 LINK=(0.5, 0.7))
PHYS_FLOW_LAM = dict(SK_DEF=dict(mass=0.9, inertia=42.0, lin=0.5, ang=0.55, friction=0.0, wind=0.15),
                     SK_LIM1=dict(lo=(-1.0, -0.25, -0.1), hi=(0.08, 0.25, 0.1), lin=0.0, stiff=(30, 8, 8)),
                     SK_LIM=dict(lo=(-0.62, -0.25, -0.1), hi=(0.08, 0.25, 0.1), lin=0.0, stiff=(15, 5, 5)),
                     SK_LIM_LOW=dict(lo=(-0.8, -0.35, -0.15), hi=(0.08, 0.35, 0.15), lin=0.0, stiff=(6, 2, 2)),
                     LINK=(0.4, 0.6))
# RA v6 PHYS_CHAIN (mail skirts the user confirmed: Banded, Mercenary, Long Nordic ...) with friction 0 (RA v9: a light
# skirt resting close to bulky trousers sticks with any friction)
PHYS_CHAIN = dict(SK_DEF=dict(mass=0.5, inertia=10.0, lin=0.5, ang=0.5, friction=0.0, wind=0.15),
                  SK_LIM1=dict(lo=(-1.2, -0.3, -0.1), hi=(0.08, 0.3, 0.1), lin=0.0, stiff=(22, 8, 8)),
                  SK_LIM=dict(lo=(-0.8, -0.2, -0.08), hi=(0.08, 0.2, 0.08), lin=0.0, stiff=(14, 5, 5)))


# hanging-piece physics (per design overrides: tip_def / tip_lim / sash_def / sash_lim / flap_def / flap_lim / bag_def / bag_lim)
# SASH: the user - 'extremely light, and flowy, reactive to movements and wind ... never clip through' (a cloth end, 4 bones of
# ~4 units). Cloak-like (skill: cloak mass .2 / inertia 4 / wind .9), in 0 (never folds in past its drawn line - the mail under it
# pushes it out through its own copy of the skirt), the chain's summed out-limits < 90 deg (RA tassel lesson: 0.55 + 3 x 0.3).
SASH_N = 4
SASH_DEF = dict(mass=0.2, inertia=3.0, lin=0.35, ang=0.3, friction=0.0, wind=0.15, gravity=1.0)   # v12: wind .9 -> .15 (FSMP's gusts twitched it standing still)
SASH_LIM = dict(lo=(-0.55, -0.45, -0.25), hi=(0.0, 0.45, 0.25), lin=0.0, astiff=8)      # v12: no linear play
SASH_LIM2 = dict(lo=(-0.3, -0.4, -0.25), hi=(0.0, 0.4, 0.25), lin=0.0, astiff=5)
TAIL_KEYS = ('Sash', 'Tail', 'Bolsa', 'Cantil')      # piece names that may carry the 'tail' role (their hidden colliders are named after them); 'Tail' = ArmorHide's welded belt tail
# 2026-10-13 + 'Bolsa' / 'Cantil' (SoS Winterhold: a bag and a canteen as two rigid tails) - otherwise their colliders count as visible shapes
# (women's verify: 'WHA Cantil Points: every point is a source point (300 not found)')
# SoS Officer v2 (user: 'i thought we talked about 3 layers of smp. why is the whole skirt moving as one piece?'): extra skirt
# layers on chains of their own - pieces with role 'skirt:outer@<word>' (cfg 'groups' {word: options}); their bones are
# '<p> <word>NN r', their lining colliders '<p> <word> Front/Side/Back'; LAYER_COLL = the colliders between layers
GROUP_WORDS = ('Under', 'Tasset')
LAYER_COLL = ('Mail Inside', 'Mail Over')
# catch depths of the hanging pieces' colliders: the belt tail / sash end / strap / bag always hang OUTSIDE the skirt, so a
# point behind the copy can only have been overrun by the swinging skirt - a deeper catch pushes it back out (hang_check v1:
# a forward swing / flare carried the mail 2+ units past a lagging tail / sash: 57-171 points beyond the 2.0 catch)
SKO_PEN, TAILU_PEN = 2.0, 4.0      # v2: the strap / bag copy back to RA's 2.0 (3.0 gave the strap 6 resting contacts behind it)
SKO_MAX_NZ = 0.6            # the skirt-outer collider (bag / strap) keeps only triangles facing outward, not up / down
SASH_COLLIDE_OWN = 0.6     # sash points with less of their own chain than this (the top, under the belt) do not collide
SASH_COLLIDE_BELOW = 3.0    # ... nor within this of its top (the mail's flared waist)
SASH_BLEND = 2.5           # units below its top over which the sash fades from the band onto its own chain
# LEFT-HIP STRAP (a leather loop slung on the left hip, the 'flaps' role with one plate): 'pretty bouncy when I move' -> a
# bigger own share than RA's riveted plates (FLAP_FOLLOW .95), lighter, little damping, a spring to bounce back on
STRAP_FOLLOW = 0.55
STRAP_DEF = dict(mass=0.9, inertia=10.0, lin=0.4, ang=0.4, friction=0.0, wind=0.0)      # v12: no wind, better damped (it twitched standing still)
STRAP_LIM = dict(lo=(-0.6, -0.08, -0.05), hi=(0.05, 0.08, 0.05), lin=0.0, astiff=40)   # v12: a loop fixed to the belt at both ends: out / in only, a hair along the belt / twist (.25 / .15 let its front end rise under the belt), no linear play
# BAG: 'reactive to movements' -> more of it on its own hinge than RA's .62, less damping than K.BAG_DEF (.5/.6)
BAG_SHARE_SOS = 0.8
BAG_DEF_SOS = dict(mass=0.6, inertia=4.0, lin=0.45, ang=0.5, friction=0.1, wind=0.0)     # v12: no wind, better damped (it twitched standing still)
BAG_LIM_SOS = dict(lo=(-0.5, -0.3, -0.12), hi=(0.05, 0.3, 0.12), lin=0.0, astiff=18)    # v12: half the swing, no linear play (.1 of play buzzed under gravity)




def use_designs(path):
    """load a design file (paths + DESIGNS, see coat/designs/coat_example.py) and make it current. The file runs with this
    module's names in scope (PHYS_CHAIN, STRAP_DEF, SKO_MAX_NZ, os, np ...); it must define STAGE_M, STAGE_F, STAGE, MODS and
    DESIGNS, and may define WORK (report + logs; default: its own folder), MOD_M / MOD_F (the installed mods), PRESET
    (the BodySlide preset verify_coat.py builds with) and TEX_ROOTS (texture folders for render_layers.py)."""
    global DESIGNS, STAGE, STAGE_M, STAGE_F, MODS, WORK, PRESET, TEX_ROOTS, MOD_M, MOD_F, BACKUPS, DESIGNS_PATH
    import runpy
    path = os.path.abspath(path).replace(os.sep, "/")
    ns = runpy.run_path(path, init_globals=dict(globals()))
    DESIGNS = ns["DESIGNS"]
    for k in ('STAGE', 'STAGE_M', 'STAGE_F', 'MODS', 'PRESET', 'TEX_ROOTS', 'MOD_M', 'MOD_F', 'BACKUPS'):
        if k in ns: globals()[k] = ns[k]
    WORK = (ns.get('WORK') or os.path.dirname(path)).replace(os.sep, '/').rstrip('/') + '/'
    os.makedirs(WORK, exist_ok=True); DESIGNS_PATH = path
    return DESIGNS



class Names:
    def __init__(self, p):
        self.p = p
        self.LEGC, self.SKC, self.SKO, self.FLP, self.FLO, self.TIPC = (f'{p} {x}' for x in ('Legs Collide', 'Skirt Lining', 'Skirt Outer', 'Flap Points', 'Flap Outer', 'Tip Points'))
        self.GROUND = 'VirtualGround'
        self.BAGC = f'{p} Bag Points'
        self.TIPU = f'{p} Skirt Under Tip'               # v12: the tail's own copy of the skirt under it
        self.SIDES = ('Front', 'Side', 'Back')         # v2c: legs and skirt lining split by facing (one-sided collisions)
        self.hidden = (self.LEGC, self.SKC, self.SKO, self.FLP, self.FLO, self.TIPC, self.BAGC, self.TIPU, self.GROUND) + \
            tuple(self.legc(x) for x in self.SIDES) + tuple(self.skc(x) for x in self.SIDES) + \
            tuple(self.tailc(k) for k in TAIL_KEYS) + tuple(self.tailu(k) for k in TAIL_KEYS) + \
            tuple(f'{p} {w} {x}' for w in GROUP_WORDS for x in self.SIDES) + tuple(f'{p} {x}' for x in LAYER_COLL)   # SoS Officer v2
        self.HANGU, self.HANGC = f'{p} Skirt Under Hang', f'{p} Hang Points'      # v11: the hip hangers' copy of the layers under them + their points
        self.TORSO = tuple(f'{p} Torso Collide {i}' for i in range(4))            # v11: the cuirass's outer surface for the helmets (one per source shape)
        self.BOOT = f'{p} Boot Collide'                  # 2026-10-14: the paired boot's cuff (boot_coll)
        self.FLAPU = f'{p} Skirt Under Flap'             # 2026-10-14 HOLDS: the hip strap's own copy of the cuirass hem + skirt under it (flap_settle)
        self.added = ('TassetBacking',)                  # 2026-10-14: DRAWN shapes the author's mesh has no source for (backing) - verify reports them apart
        self.hidden = self.hidden + (self.HANGU, self.HANGC, self.BOOT, self.FLAPU) + self.TORSO

    def legc(self, side): return f'{self.p} Legs {side}'
    def skc(self, side): return f'{self.p} Skirt {side}'

    def sk(self, k, r): return f'{self.p} Skirt{k:02d} {r}'
    def flap(self, k, r): return f'{self.p} Flap{k} {r}'
    def tip(self, r): return f'{self.p} BeltTip {r}'
    def bag(self, r): return f'{self.p} Bag {r}'
    def tail(self, k, r): return f'{self.p} {k} {r}'              # SoS: a hanging tail's chain (the sash end)
    def hang(self, k, j): return f'{self.p} Hang{k} {j}'            # v10: a hip hanger (0 front anchor, 1 front ring, 2.. strap, n+2 back anchor, n+3 back ring)
    def tailc(self, k): return f'{self.p} {k} Points'
    def tailu(self, k): return f'{self.p} Skirt Under {k}'
    def is_phys(self, b): return b.startswith(self.p + ' ')


class GroupNames:
    """SoS Officer v2: an extra skirt layer on its own chains - bones '<p> <word>03 2', lining colliders '<p> <word> Front'"""
    def __init__(self, N, word): self.N, self.p, self.word = N, N.p, word
    def sk(self, k, r): return f'{self.p} {self.word}{k:02d} {r}'
    def skc(self, side): return f'{self.p} {self.word} {side}'
    def is_phys(self, b): return self.N.is_phys(b)


def fold(w):
    out = defaultdict(float)
    for b, x in w.items(): out[b if R.is_skel(b) else PELV] += x
    return dict(out)


def cap4(N, w, keep_body=False, keep=(), pelv_min=0.0):
    out = {b: x for b, x in w.items() if x > 1e-5}
    side = {D.LCLF: D.LTHG, D.RCLF: D.RTHG}
    if pelv_min and len(out) > 4 and 0.0 < out.get(PELV, 0.0) < pelv_min:   # v9: a pelvis share this small is folded into the thighs
        th = [b for b in (D.LTHG, D.RTHG) if b in out]     # before the cap - with keep_body it held a third body slot and the cap
        if th:                                               # crushed 2 chains x 2 rows into ONE chain bone at the front / back centre
            x = out.pop(PELV); t = sum(out[b] for b in th)
            for b in th: out[b] += x * out[b] / t
    while len(out) > 4:
        cand = [b for b in out if not (keep_body and b in (D.LTHG, D.RTHG, PELV)) and b not in keep] or list(out)
        b = min(cand, key=lambda k: out[k]); x = out.pop(b)
        if N.is_phys(b):
            same = [k for k in out if N.is_phys(k) and k.rsplit(' ', 1)[0] == b.rsplit(' ', 1)[0] and k not in keep]
            tgt = max(same or [k for k in out if N.is_phys(k) and k not in keep] or [k for k in out if k not in keep] or list(out), key=lambda k: out[k])
        elif b in side and side[b] in out: tgt = side[b]
        elif b in (D.LTHG, D.RTHG) and PELV in out: tgt = PELV
        else: tgt = max([k for k in out if not N.is_phys(k)] or [k for k in out if k not in keep] or list(out), key=lambda k: out[k])
        out[tgt] += x
    t = sum(out.values())
    return {b: x / t for b, x in out.items()}


def islands(tris, n):
    par = list(range(n))

    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for t in tris:
        for a, b in ((t[0], t[1]), (t[1], t[2])):
            ra, rb = f(int(a)), f(int(b))
            if ra != rb: par[ra] = rb
    return np.array([f(i) for i in range(n)])


def find_slits(P, tris, cx, cy):
    """[(centre, half-width, top)] of the gaps in the outer wall at the hem narrower than SLIT_MAX_HW"""
    om = G.outer_mask(P, tris, cx, cy); Q = G.surface_samples(P, tris[om])
    th = np.degrees(np.arctan2(Q[:, 0] - cx, Q[:, 1] - cy)); z = Q[:, 2]; hem = float(P[:, 2].min())
    a = np.sort(th[z < hem + 4.0]); g = np.diff(np.r_[a, a[0] + 360.0]); out = []
    for k in np.where(g > 6.0)[0]:
        lo = a[k]; hi = a[(k + 1) % len(a)] + (360.0 if k == len(a) - 1 else 0.0)
        c, hw = float(wrap((lo + hi) / 2)), float((hi - lo) / 2)
        if hw > SLIT_MAX_HW: continue
        top = None
        for z0 in np.arange(hem, P[:, 2].max(), 0.5):
            b = (z >= z0) & (z < z0 + 0.5)
            if b.any() and (np.abs(wrap(th[b] - c)) < max(2.0, hw / 3)).any(): top = float(z0); break
        if top is None: top = float(P[:, 2].max())      # v22: an opening that never closes (the lamellar aketon's front) runs to the top
        out.append((c, hw, top))
    return sorted(out)


class Rig:
    """skirt chains in panels between slits; per-layer slit tops"""

    def __init__(self, N, cfg, layers, log):
        self.N, self.cfg = N, cfg
        self.nrow = cfg.get('nrow', NROW)          # SoS Officer v2: a short layer (the tassets) on fewer rows
        outer = layers['outer']
        if cfg.get('axis_z'):      # the skirt's own top is not level (a lining running up under the cuirass): centre from a band
            z0, z1 = cfg['axis_z']; m = (outer[0][:, 2] > z0) & (outer[0][:, 2] < z1)
            self.cx, self.cy = float(outer[0][m, 0].mean()), float(outer[0][m, 1].mean())
        else:
            self.cx, self.cy = G.axis_centre(outer[0], outer[1])
        self.slits = find_slits(outer[0], outer[1], self.cx, self.cy) if cfg['slits'] else []
        self.tops = {}          # layer -> [top per slit]
        if cfg.get('force_slits'):          # v16: the outer layer cut into panels up to the belt (cut_panels)
            self.slits = [tuple(x) for x in cfg['force_slits']]
            layers = {}; self.tops = {'outer': [x[2] for x in self.slits]}
        for ln, (P, T_) in layers.items():
            own = find_slits(P, T_, self.cx, self.cy) if cfg['slits'] else []
            tops = []
            for c, hw, top in self.slits:
                m = [s for s in own if abs(wrap(s[0] - c)) < 20]
                tops.append(m[0][2] if m else -1e9)        # a layer without that slit: closed (blend) everywhere
            self.tops[ln] = tops
        if self.slits:
            edges = []
            for i, (c, hw, _) in enumerate(self.slits):
                c2, hw2, _ = self.slits[(i + 1) % len(self.slits)]
                lo, hi = c + hw, c2 - hw2
                if hi <= lo: hi += 360.0
                n = max(2, int(round((hi - lo) / self.cfg.get('chain_spacing', CHAIN_SPACING))) + 1)
                edges.append(list(np.linspace(lo, hi, n)))
            tot = sum(len(e) for e in edges)
            while tot > self.cfg.get('max_chains', MAX_CHAINS):
                j = max(range(len(edges)), key=lambda i: len(edges[i])); e = edges[j]
                edges[j] = list(np.linspace(e[0], e[-1], len(e) - 1)); tot -= 1
            self.panels = edges
        else:
            n = self.cfg.get('max_chains', MAX_CHAINS); self.panels = [list(np.linspace(0.0, 360.0 - 360.0 / n, n))]   # v6: per design (Officer 14: 14 x 5 + skeleton < 80)
        self.ang_k = [float(wrap(a)) for p in self.panels for a in p]
        self.panel_of = [i for i, p in enumerate(self.panels) for _ in p]
        log.append(f'skirt axis ({self.cx:.2f}, {self.cy:.2f}); slits (centre, half-width, top): ' +
                   ('; '.join(f'{c:.1f}/{hw:.1f}/{t:.1f}' for c, hw, t in self.slits) or 'none (all round)') +
                   '; per-layer tops ' + str({k: [round(x, 1) for x in v] for k, v in self.tops.items()}) +
                   f'; {len(self.ang_k)} chains at ' + ' '.join(f'{a:.0f}' for a in self.ang_k))

    def ang(self, p): return float(np.degrees(np.arctan2(p[0] - self.cx, p[1] - self.cy)))

    def chains(self, p, layer, side=None):
        a, z = self.ang(p), float(p[2])
        if not self.slits:
            ks = self.ang_k; n = len(ks); u = (a - ks[0]) % 360.0; step = 360.0 / n
            i = int(u // step) % n; t = (u - i * step) / step
            return [(i, 1 - t), ((i + 1) % n, t)]
        base = 0
        for pi, p_ in enumerate(self.panels):
            lo, hi = p_[0], p_[-1]; u = (a - lo) % 360.0
            if u <= (hi - lo) % 360.0 + 1e-9:
                return [(base + k, w) for k, w in lin_bracket([(x - lo) % 360.0 for x in p_], u)]
            base += len(p_)
        # inside a slit: between the last chain of one panel and the first of the next
        for si, (c, hw, _) in enumerate(self.slits):
            x = float(wrap(a - c))
            if abs(x) <= hw + 1e-6:
                right_panel = si; left_panel = (si - 1) % len(self.panels)
                k_hi = sum(len(q) for q in self.panels[:right_panel])                 # first chain after the slit
                k_lo = sum(len(q) for q in self.panels[:left_panel]) + len(self.panels[left_panel]) - 1
                t = (x + hw) / (2 * hw)
                top = self.tops[layer][si]
                f = float(smooth01((z - (top - 1.0)) / 2.0))
                w_hi = f * t + (1 - f) * (1.0 if ((x >= 0) if not side else (side > 0)) else 0.0)   # v16: cut panels by topology
                return [(k_hi, w_hi), (k_lo, 1 - w_hi)]
        raise RuntimeError(f'angle {a:.1f} in no panel and no slit')

    def place(self, P, sk_v, outer_v, log):
        N, cfg = self.N, self.cfg
        self.G, self.parent, self.rows = {}, {}, {}
        th = np.degrees(np.arctan2(P[:, 0] - self.cx, P[:, 1] - self.cy)); rr = np.hypot(P[:, 0] - self.cx, P[:, 1] - self.cy)

        def radius(a, z):
            for da, dz in ((8, 2), (15, 4), (30, 8), (60, 12)):
                m = (np.abs(wrap(th[outer_v] - a)) < da) & (np.abs(P[outer_v, 2] - z) < dz)
                if m.sum() >= 3:
                    w = np.exp(-(wrap(th[outer_v][m] - a) / 5) ** 2 - ((P[outer_v, 2][m] - z) / 1.5) ** 2) + 1e-9
                    return float((w * rr[outer_v][m]).sum() / w.sum())
            raise RuntimeError(f'no skirt surface near {a:.0f} deg z {z:.1f}')
        for k, a in enumerate(self.ang_k):
            near = sk_v[np.abs(wrap(th[sk_v] - a)) < 8]
            if not len(near): near = sk_v[np.abs(wrap(th[sk_v] - a)) < 20]
            zs = list(np.linspace(cfg['sk_anchor'], float(P[near, 2].min()), self.nrow + 1)); self.rows[k] = zs
            for r, z in enumerate(zs):
                g = np.eye(4); g[:3, :3] = frame(a); rad = radius(a, z)
                g[:3, 3] = [self.cx + rad * np.sin(np.radians(a)), self.cy + rad * np.cos(np.radians(a)), z]
                self.G[N.sk(k, r)] = g; self.parent[N.sk(k, r)] = PELV if r == 0 else N.sk(k, r - 1)
        log.append('skirt rows (anchor..hem): ' + '; '.join(f'{a:.0f}:' + '/'.join(f'{z:.1f}' for z in self.rows[k]) for k, a in enumerate(self.ang_k)))


def skirt_w(rig, cfg, p, aw, layer, free=1.0, legw=None, seam=1.0, side=None):
    """v2: the part physics does not move follows the trousers under the skirt (fading in from the author's weights
    at the belt over 3 units); the physics share = the belt ramp x how freely this part of the skirt hangs"""
    z = float(p[2]); r_ = float(smooth01((cfg['sk_belt'] - z) / cfg['ramp'])) * seam; s = r_ * free
    w = defaultdict(float)
    if cfg.get('top_follow') == 'belt':
        # Officer v4: a layer that hangs clear of the trousers hangs from the BELT. Below the ramp the author's thigh / calf / foot
        # weights go to the pelvis (faded in from any seam, so a cut edge still matches its source) and the trousers carry only the
        # share physics leaves at that point (1 - free) - never the whole ramp. The default blend gave the Officer mail's top band
        # the trousers' weights (60-76% thigh) under plates riding their own chains (7%): a legs-apart stance pushed the band out
        # through the plates and swept the sash / strap colliders built from it under them every stance and step.
        t = r_ * (1 - free) if legw else 0.0; a_ = (1 - r_) if legw else (1 - s)
        for b, x in fold(aw).items():
            leg = any(k in b for k in ('Thigh', 'Calf', 'Foot'))
            w[PELV if leg else b] += a_ * seam * x
            if seam < 1.0: w[b] += a_ * (1 - seam) * x
        for b, x in (legw or {}).items(): w[b] += t * x
    else:
        q = float(smooth01((cfg['sk_belt'] - z) / 3.0)) * seam if legw else 0.0
        for b, x in fold(aw).items(): w[b] += (1 - s) * (1 - q) * x
        for b, x in (legw or {}).items(): w[b] += (1 - s) * q * x
    if s > 1e-4:
        for k, a in rig.chains(p, layer, side):
            if a <= 0: continue
            for r, t in row_bracket(rig.rows[k], z): w[PELV if r == 0 else rig.N.sk(k, r)] += s * a * t
    return dict(w), s


def leg_axes(pants, shared):
    """v6: hip / knee / ankle positions per side for the trousers' outward test. Trousers that stop above the boots (the
    Northern Knight's brigandine) have no foot bones: take them from another shape of the mesh, else continue the shin"""
    s2b = dict(shared.get('s2b_all', {})); s2b.update(pants.s2b)
    g = {b: np.linalg.inv(B.tb2m(x))[:3, 3] for b, x in s2b.items()}
    out = {}
    for side, (th, ca, ft) in {'L': ('NPC L Thigh [LThg]', 'NPC L Calf [LClf]', 'NPC L Foot [Lft ]'),
                               'R': ('NPC R Thigh [RThg]', 'NPC R Calf [RClf]', 'NPC R Foot [Rft ]')}.items():
        foot = g.get(ft, g[ca] + (g[ca] - g[th]))
        out[side] = [g[th], g[ca], foot]
    return out


def trousers(pants, shared, log):
    """the trousers as a surface with outward winding + normals (orientation decided once, on _1)"""
    fk = f'flip_{len(pants.pos)}'               # v6: per trousers mesh (the Northern Knight's _0 / _1 trousers differ)
    if fk not in shared:
        pt = pants.tris[pants.pos[pants.tris].mean(1)[:, 2] > LEG_ZMIN]
        frac = K.outward_fraction(pants.pos, pt, leg_axes(pants, shared)); shared[fk] = frac < 0.5
        log.append(f'legs from {pants.name} ({len(pt)} tris above z {LEG_ZMIN}), winding outward {frac:.0%}' + (' -> flipped' if frac < 0.5 else ''))
    shared['flip'] = shared[fk]
    tris = pants.tris[:, [0, 2, 1]] if shared['flip'] else pants.tris
    return type('Tr', (), dict(pos=pants.pos, tris=tris, norm=K.vertex_normals(pants.pos, tris), w=pants.w))()


def pants_of(S, cfg):
    """v7: the trousers the legs follow / collide with - only their first cfg['pants_n'] points when the _1 mesh has extra
    pieces the _0 one lacks (both weights must write leg colliders with the same points).
    SoS: cfg['pants_comp'] = the trousers are this welded component of the shape (Armors/ coats: comp 1 of the torso) -> a
    compacted copy of just that component (the leg follow's nearest-point search must not see coat points); src_map = the
    shape's point index per copy point (the leg colliders' provenance for the women's slider data)"""
    t = S[cfg['pants']]; n = cfg.get('pants_n'); comp = cfg.get('pants_comp')
    if comp is not None:
        # Authoria 2026-10-18: a tuple of components = trousers drawn as one component per leg (vanilla robem / merchant)
        lab = D.welded_components(t.pos, t.tris); inc = np.isin(lab, comp); v = np.where(inc)[0]
        rm = np.full(len(t.pos), -1); rm[v] = np.arange(len(v)); keep = inc[t.tris].all(1)
        c = copy.copy(t); c.pos, c.tris, c.w = t.pos[v], rm[t.tris[keep]], [t.w[i] for i in v]
        if getattr(t, 'norm', None) is not None: c.norm = t.norm[v]
        c.src_map = v
        return c
    if not n or len(t.pos) == n: return t
    c = copy.copy(t); keep = (t.tris < n).all(1)
    c.pos, c.tris, c.w = t.pos[:n], t.tris[keep], t.w[:n]
    if getattr(t, 'norm', None) is not None: c.norm = t.norm[:n]
    return c


def lining_src(p, rig, all_=False):
    """the points of a skirt layer that face the legs: its inward side, or all of it when it is a single sheet.
    all_ (v19, the two-layer designs): the whole sheet at the author's resolution (source points) - the v16 panel cuts
    turned 10% of the outer's triangles sideways, so the 5% rule took the cut edges + hem lip for the lining and the
    panels' faces had no leg collider at all (user: 'the skirt is sitting in the thigh'); the cloth's only inward
    triangles are the little shelf of its hem tier, so its lining was a ring at z 51"""
    if all_:
        v = np.unique(p.tris); src = getattr(p, 'src_idx', None)
        return v[src[v] >= 0] if src is not None and (src[v] >= 0).sum() >= 50 else v
    it = ~G.outer_mask(p.pos, p.tris, rig.cx, rig.cy)
    return np.unique(p.tris[it]) if it.mean() >= 0.05 else np.unique(p.tris)


def thighs_only(w):
    out = defaultdict(float)
    for b, x in w.items(): out[{D.LCLF: D.LTHG, D.RCLF: D.RTHG}.get(b, b)] += x
    return dict(out)


def smooth_field(P, ws, sigma):
    out = []
    for a0 in range(0, len(P), 400):
        d = np.linalg.norm(P[a0:a0 + 400, None, :] - P[None, :, :], axis=2); wk = np.exp(-(d / sigma) ** 2) * (d < 3 * sigma)
        for r in range(len(d)):
            acc = defaultdict(float); nz = np.where(wk[r] > 1e-4)[0]; tot = wk[r, nz].sum()
            for j in nz:
                for b, x in ws[j].items(): acc[b] += wk[r, j] * x / tot
            out.append(dict(acc))
    return out


def smooth_scalar(P, v, sigma):
    out = np.zeros(len(P))
    for a0 in range(0, len(P), 400):
        d = np.linalg.norm(P[a0:a0 + 400, None, :] - P[None, :, :], axis=2); wk = np.exp(-(d / sigma) ** 2) * (d < 3 * sigma)
        out[a0:a0 + 400] = (wk * v[None, :]).sum(1) / wk.sum(1)
    return out


def blend_under(surf, tris_g, W, pts):
    """weights of the surface under each point (barycentric blend of its corners' weights)"""
    tri, bary, dist, cp = surf.query(pts, k=10); out = []
    for j in range(len(pts)):
        acc = defaultdict(float)
        for vv, bb in zip(tris_g[tri[j]], bary[j]):
            for bn, x in W[int(vv)].items(): acc[bn] += bb * x
        out.append(dict(acc))
    return out, dist


class Piece:
    """one written visible shape: positions etc. (after any split), its source shape and source point per point"""
    def __init__(self, name, src, role, pos, uv, nrm, ow, tris, partid, src_idx, mids=None, n0=None, col=None):
        self.name, self.src, self.role, self.col = name, src, role, col
        self.pos, self.uv, self.nrm, self.ow, self.tris, self.partid = pos, uv, nrm, ow, tris, partid
        self.src_idx = src_idx            # source point index per point (-1 = new split point)
        self.mids, self.n0 = mids or [], n0


def cut_pieces(T, S, cfg, log, memo=None):
    """the visible pieces: whole shapes or parts of one cut out by component / texture island; returns (pieces, rest)
    where rest = {shape: kept triangle mask} for the shapes that lose triangles to pieces.
    SoS: memo (the build's shared dict) - a height cut ('below') is decided once, on _1, and reused by triangle index for _0
    (the thin body's points sit at other heights: the same z picked other triangles)"""
    pieces, taken = [], defaultdict(lambda: None)
    memo = {} if memo is None else memo
    comps_cache = {}
    for name, src, sel, role in cfg['pieces']:
        t = S[src]; zcut = False
        if sel is None:
            tm = np.ones(len(t.tris), bool)
        else:
            if src not in comps_cache:
                lab = D.welded_components(t.pos, t.tris); comps_cache[src] = lab
                for k, n in cfg.get('expect', {}).items():
                    if int((lab == k).sum()) != n: raise RuntimeError(f'{src} component {k}: {(lab == k).sum()} points, expected {n}')
            lab = comps_cache[src]
            if sel[0] == 'comps':
                vm = np.isin(lab, sel[1])
            elif sel[0] == 'islands':  # ('islands', comp, {island id: size}, extra comps): named texture islands of one component
                isl = islands(t.tris, len(t.pos))
                for r, n in sel[2].items():
                    if int(((isl == r) & (lab == sel[1])).sum()) != n: raise RuntimeError(f'{name}: island {r} of {src} comp {sel[1]} has {int(((isl == r) & (lab == sel[1])).sum())} points, expected {n}')
                vm = (np.isin(isl, list(sel[2])) & (lab == sel[1])) | np.isin(lab, sel[3])
                if len(sel) > 4 and sel[4] is not None:     # v5: only the part of those islands wholly below a height
                    mk = ('isl_tm', name, src)          # SoS: decided once on _1 like 'below' (_0's points sit at other heights)
                    if mk not in memo: memo[mk] = vm[t.tris].all(1) & (t.pos[t.tris][:, :, 2] < sel[4]).all(1)
                    tm = memo[mk]
                    vm = np.zeros(len(t.pos), bool); vm[np.unique(t.tris[tm])] = True; zcut = True
                if len(sel) > 5 and sel[5]:     # 2026-10-13 (SoS Morthal): {island id: z} - THOSE islands (listed in sel[2]) give only their
                    mk = ('isl_cut', name, src)  # triangles wholly below their own z (a wrap's hanging tab over the skirt; the rest of the
                    if mk not in memo:           # wrap stays on the body); the other islands whole. Decided once on _1 like 'below'.
                        tm_ = vm[t.tris].all(1)
                        for r, zc in sel[5].items():
                            ti_ = ((isl[t.tris] == r) & (lab[t.tris] == sel[1])).all(1)
                            tm_ &= ~(ti_ & ~(t.pos[t.tris][:, :, 2] < zc).all(1))
                        memo[mk] = tm_
                    tm = memo[mk]
                    vm = np.zeros(len(t.pos), bool); vm[np.unique(t.tris[tm])] = True; zcut = True
            elif sel[0] == 'hemband':   # SoS Chainmail split (user-approved mockup survey/checks/chainmailscm_split_mockup.png):
                # ('hemband', comp, coat islands, lining islands, zcut, 'mail' | 'skirt'): the painted blue band row (coat triangles
                # touching the hem ring, where the coat is welded to its lining) moves from the mail to the lining -> mail = coat below
                # zcut minus that row (ends at its trim); blue skirt = the row + the lining. Decided once on _1 (indices) like 'below'.
                mk = ('hemband', src, sel[1], tuple(sel[2]), tuple(sel[3]), sel[4])
                if mk not in memo:
                    isl = islands(t.tris, len(t.pos)); cm = (lab[t.tris] == sel[1]).all(1); ti = isl[t.tris[:, 0]]
                    coat = cm & np.isin(ti, sel[2]) & (t.pos[t.tris][:, :, 2] < sel[4]).all(1)
                    lin = cm & np.isin(ti, sel[3])
                    keys = {tuple(np.round(t.pos[i], 3)) for i in np.unique(t.tris[lin])}
                    ring = np.array([tuple(np.round(t.pos[i], 3)) in keys for i in range(len(t.pos))])
                    band = coat & ring[t.tris].any(1)
                    memo[mk] = {'mail': coat & ~band, 'skirt': band | lin}
                    log.append(f'hemband split of {src}: hem ring {int(ring[np.unique(t.tris[coat])].sum())} pts, band row {int(band.sum())} tris -> '
                               f'mail {int((coat & ~band).sum())} tris, blue skirt {int((band | lin).sum())} tris')
                tm = memo[mk][sel[5]]
                vm = np.zeros(len(t.pos), bool); vm[np.unique(t.tris[tm])] = True; zcut = True
            elif sel[0] == 'uvsplit':   # SoS Officer: ('uvsplit', comp, sheet islands, extra islands (mail side), lining islands, vcut,
                # (ulo, uhi), zstrip, 'mail' | 'skirt'): the skirt SHEET carries mail + beige border + blue hem + front strip all painted,
                # with its edges on the painted lines -> cut by texture: blue = triangles below the border's lower edge row (uv v > vcut)
                # + the front strip (u in (ulo, uhi), below zstrip); mail = the rest of the sheet + the extra islands (the tassets ride
                # with it); blue skirt = blue part + the lining. Decided once on _1 (indices).
                mk = ('uvsplit', src, sel[1], tuple(sel[2]), tuple(sel[3]), tuple(sel[4]), sel[5], tuple(sel[6]), sel[7])
                if mk not in memo:
                    isl = islands(t.tris, len(t.pos)); cm = (lab[t.tris] == sel[1]).all(1); ti = isl[t.tris[:, 0]]
                    uvc = np.asarray(t.uv, float)[t.tris].mean(1); zc = t.pos[t.tris][:, :, 2].mean(1)
                    sheet = cm & np.isin(ti, sel[2])
                    blue = sheet & ((uvc[:, 1] > sel[5]) | ((uvc[:, 0] > sel[6][0]) & (uvc[:, 0] < sel[6][1]) & (zc < sel[7])))
                    memo[mk] = {'mail': (sheet & ~blue) | (cm & np.isin(ti, sel[3])), 'skirt': blue | (cm & np.isin(ti, sel[4]))}
                    log.append(f'uvsplit of {src}: sheet {int(sheet.sum())} tris -> mail {int((sheet & ~blue).sum())} (+ {int((cm & np.isin(ti, sel[3])).sum())} '
                               f'extra), blue {int(blue.sum())} (+ lining {int((cm & np.isin(ti, sel[4])).sum())})')
                tm = memo[mk][sel[8]]
                vm = np.zeros(len(t.pos), bool); vm[np.unique(t.tris[tm])] = True; zcut = True
            elif sel[0] == 'vtris':     # vanilla women: the triangles prep_vanilla_f.py found for this piece (a cut across a
                tm = np.zeros(len(t.tris), bool); tm[np.asarray(sel[1], int)] = True     # component follows triangle edges)
                vm = np.zeros(len(t.pos), bool); vm[np.unique(t.tris[tm])] = True; zcut = True
            elif sel[0] == 'below':     # ('below', comp, zcut): the component's triangles lying wholly below zcut
                mk = ('below_tm', name, src)
                if mk not in memo: memo[mk] = (lab[t.tris] == sel[1]).all(1) & (t.pos[t.tris][:, :, 2] < sel[2]).all(1)
                tm = memo[mk]
                vm = np.zeros(len(t.pos), bool); vm[np.unique(t.tris[tm])] = True
            else:   # ('islands_below', comp, zmax) - the texture islands of one component lying wholly below zmax
                isl = islands(t.tris, len(t.pos)); cv = lab == sel[1]
                want = sorted((r for r in set(isl[cv].tolist()) if t.pos[isl == r, 2].max() < sel[2]), key=lambda r: -int((isl == r).sum()))
                sizes = tuple(int((isl == r).sum()) for r in want)
                if 'island_sizes' in cfg and sizes != tuple(cfg['island_sizes']): raise RuntimeError(f'{src} islands {sizes}, expected {cfg["island_sizes"]}')
                vm = np.isin(isl, want)
            if sel[0] != 'below' and not zcut:
                tm = vm[t.tris].all(1)
                if (vm[t.tris].any(1) & ~tm).any(): raise RuntimeError(f'{name}: a triangle straddles the cut')
        prev = taken[src]
        if prev is not None and (prev & tm).any(): raise RuntimeError(f'{name}: triangles already taken')
        taken[src] = tm if prev is None else (prev | tm)
        v = np.unique(t.tris[tm]); rm = np.full(len(t.pos), -1); rm[v] = np.arange(len(v))
        pieces.append(Piece(name, src, role, t.pos[v], t.uv[v], t.norm[v] if t.norm is not None else None, [t.w[i] for i in v],
                            rm[t.tris[tm]], np.array(B.part_ids(t, T))[tm], v, col=(np.asarray(t.s.colors, float)[v] if t.s.colors else None)))
        if name in cfg.get('flip_pieces', ()):    # v15 pass B: the inward-only cloth turned to face out (the merge adds the inward twin)
            pc = pieces[-1]; pc.tris = pc.tris[:, [0, 2, 1]]; pc.nrm = -pc.nrm if pc.nrm is not None else None
        sel_s = '' if sel is None else ' ' + (f"('vtris', {len(sel[1])} tris)" if sel[0] == 'vtris' else str(sel))
        log.append(f'piece {name} <- {src}{sel_s}: {len(v)} pts / {int(tm.sum())} tris ({role})')
    for src, comps in cfg.get('drop_comps', {}).items():       # v5: duplicates the HDT patch left in a static shape
        t = S[src]; lab = D.welded_components(t.pos, t.tris); tm = np.isin(lab[t.tris], comps).all(1)
        prev = taken[src]; taken[src] = tm if prev is None else (prev | tm)
        log.append(f'dropped {src} components {tuple(comps)}: {int(tm.sum())} tris')
    rest = {src: ~m for src, m in taken.items() if src not in [p.name for p in pieces]}
    return pieces, rest


def weld_seams(t, tm, pieces, pws, log, g):
    """v13 (user 2026-10-12: 'i could see through the officers waist line, like there was a disconnect ... the same on the Gambeson'): a cut
    piece that was subdivided carries a midpoint on every seam edge it shares with its source shape's remainder, while the remainder kept
    the author's straight edge - the two sides shared only the author's vertices, and under a pose the piece's midpoints drifted off the
    remainder's edge (a hairline crack along the waist you see through). Here every such remainder edge is split at the piece's own point
    (position, UV, normal, weights, colour copied from the piece), so both sides share every seam vertex and move identically.
    pws = {piece name: its final top-4 weights per point}. Every piece BOUNDARY point that lies on the remainder's boundary edge without
    being a remainder vertex is a weld point - the subdivision's midpoints, and any T-junction the author left between a texture island
    and the torso (the Officer's tassets). Returns [dict(pos, uv, nrm, w, col, piece, k)]; the caller splits the remainder edge at each."""
    rest_t = np.where(tm)[0]
    if not len(rest_t) or not pieces: return []
    E = _boundary_edges(t.tris[tm])
    if not len(E): return []
    A, B = t.pos[E[:, 0]], t.pos[E[:, 1]]; rbv = np.unique(E); RP = t.pos[rbv]
    out = []
    for p in pieces:
        pb = np.unique(_boundary_edges(np.asarray(p.tris)))
        if not len(pb): continue
        P = np.asarray(p.pos, float)[pb]
        dv = np.empty(len(P)); de = np.empty(len(P))
        for s0 in range(0, len(P), 300):
            q = P[s0:s0 + 300]
            dv[s0:s0 + 300] = np.linalg.norm(q[:, None, :] - RP[None], axis=2).min(1)
            de[s0:s0 + 300] = _seg_dist_t(q, A, B)[0].min(1)
        on = (de < 0.02) & (dv > 1e-3); pw = pws[p.name]      # 0.02 as the seam check: an island vertex the author left a hair off the edge is welded too
        for i in np.where(on)[0]:
            k = int(pb[i])
            out.append(dict(pos=np.array(p.pos[k], float), uv=np.array(p.uv[k], float), nrm=(np.array(p.nrm[k], float) if p.nrm is not None else None),
                            w=pw[k], col=(tuple(p.col[k]) if p.col is not None else None), piece=p.name, k=k))
    if out: log.append(f'{g}: {t.name}: {len(out)} seam points of {sorted({w["piece"] for w in out})} to weld into the remainder')
    return out


def _boundary_edges(tris):
    e = {}
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            k = (min(int(u), int(v)), max(int(u), int(v))); e[k] = e.get(k, 0) + 1
    return np.array([k for k, cnt in e.items() if cnt == 1], int).reshape(-1, 2)


def _seg_dist_t(Q, A, B):
    """distance from each point of Q to each segment A->B and the parameter along it: (n, m) arrays"""
    AB = B - A; L2 = (AB * AB).sum(1)[None] + 1e-12
    tt = np.clip(((Q[:, None, :] - A[None]) * AB[None]).sum(2) / L2, 0.0, 1.0)
    C_ = A[None] + tt[:, :, None] * AB[None]
    return np.linalg.norm(Q[:, None, :] - C_, axis=2), tt


def split_piece(pc, sel_tris=None):
    """midpoint split (x4) of the piece's triangles (all, or the selected), recording the source of new points"""
    sel = np.ones(len(pc.tris), bool) if sel_tris is None else sel_tris
    mids = []
    pos, uv, nrm, ow, col, tris, par, _ = subdivide_c(pc.pos, pc.uv, pc.nrm, pc.ow, pc.col, pc.tris, sel, 1, mids=mids)
    n0 = len(pc.pos)
    return Piece(pc.name, pc.src, pc.role, pos, uv, nrm, ow, tris, pc.partid[par], np.r_[pc.src_idx, -np.ones(len(pos) - n0, int)], mids, n0, col=col)


def drop_gusset(pc, u_max, variant, shared, log):
    """v19b (user: 'part of the cloth is attached to the scale skirt'): the author's front and back openings are bridged by a
    brown cloth strip that belongs to the OUTER shape - set in ~1.5 behind the panel edges, textured from the left strip of
    the atlas (u < 0.10), welded to one half. In the two-layer build it is not the cloth skirt; the v16 cut split it down the
    middle and each panel carried half of it along. Dropped here: triangles at the front / back whose median vertex u is
    under u_max. The dropped source triangles (source point triples) go to shared['dropped'] -> the report, so verify can
    leave them out of its kept-triangle count. Runs before the notch fill / subdivision / cuts (on the author's triangles)."""
    P, Tr, UV = pc.pos, np.asarray(pc.tris), pc.uv
    cx, cy = float(P[:, 0].mean()), float(P[:, 1].mean())
    cc = P[Tr].mean(1); ang = np.degrees(np.arctan2(cc[:, 0] - cx, cc[:, 1] - cy))
    umed = np.median(UV[Tr][:, :, 0], axis=1)
    drop = (umed < u_max) & ((np.abs(ang) < 30.0) | (np.abs(ang) > 150.0))
    if not drop.any():
        log.append(f'{pc.name}: no gusset triangles found (u < {u_max} at the front / back)'); return pc
    keep_t = ~drop
    used = np.zeros(len(P), bool); used[Tr[keep_t]] = True
    newi = -np.ones(len(P), int); newi[used] = np.arange(int(used.sum()))
    tris = newi[Tr[keep_t]]; src = np.asarray(pc.src_idx)
    gone = [sorted(int(src[v]) for v in t) for t in Tr[drop]]
    shared.setdefault('dropped', {}).setdefault(variant, {}).setdefault(pc.src, []).extend(gone)
    log.append(f'{pc.name}: {int(drop.sum())} gusset triangles dropped at the front / back openings (u < {u_max}; z {cc[drop, 2].min():.0f}-'
               f'{cc[drop, 2].max():.0f}, radius {np.hypot(cc[drop, 0] - cx, cc[drop, 1] - cy).mean():.1f}); {int((~used).sum())} points went with them')
    k = np.where(used)[0]
    return Piece(pc.name, pc.src, pc.role, P[k], UV[k], (pc.nrm[k] if pc.nrm is not None else None), [pc.ow[i] for i in k], tris,
                 pc.partid[keep_t], src[k], list(pc.mids), pc.n0, col=(pc.col[k] if pc.col is not None else None))


def clear_legs(pc, pants, clear, shared, log, sigma=1.5, cap=4.0):
    """v19: move a skirt piece radially out until every point is at least `clear` off the trousers' surface (smoothed over
    neighbours so the sheet stays a sheet). The author's inner cloth lining starts inside the trousers at the hips (up to 2.4
    in) and 0.1-0.6 off them at the hem sides: the legs then show through it wherever it shows, and the lining collider
    (points >= LINING_MIN_GAP off the legs) shrank to a ring at the hem. Returns a copy of the piece."""
    tr = trousers(pants, shared, log)
    P = pc.pos.copy(); cx, cy = float(P[:, 0].mean()), float(P[:, 1].mean())
    rad = np.c_[P[:, 0] - cx, P[:, 1] - cy, np.zeros(len(P))]; rad /= np.linalg.norm(rad, axis=1, keepdims=True) + 1e-12
    K_ = np.exp(-(np.linalg.norm(P[:, None] - P[None], axis=2) / sigma) ** 2)
    S_ = B.Surface([('t', tr.pos, tr.tris)]); tot = np.zeros(len(P)); need0 = None
    for it in range(10):
        Q = P + tot[:, None] * rad
        tri, bary, dist, cp = S_.query(Q, k=8)
        nn = (tr.norm[tr.tris[tri]] * bary[:, :, None]).sum(1)
        sd = ((Q - cp) * nn).sum(1)                                   # signed: negative = inside the trousers
        need = np.maximum(0.0, clear - sd); need[dist > clear + 3.0] = 0.0
        if need0 is None: need0 = need.copy()
        if need.max() <= 1e-3: break
        tot = np.minimum(cap, tot + (K_ * need[None, :]).max(1))
    tot[tot <= 1e-3] = 0.0                            # every moved point is recorded (verify undoes the move point for point)
    mv = np.where(tot > 0)[0]
    log.append(f'{pc.name}: moved out of the trousers at {len(mv)} of {len(P)} pts (max {tot.max():.2f}; was up to {need0.max() - clear:.2f} inside, '
               f'{int((need0 > 0).sum())} pts closer than {clear})')
    out = copy.copy(pc); out.pos = P + tot[:, None] * rad
    return out, mv, (tot[:, None] * rad)[mv]


def boot_band(bc, variant, shared, log, rig_c):
    """2026-10-14 (user: 'The whiterun heavy guard armor always is paired with the whiterun heavy boots. The bottom of the skirt is clipping
    into the top of the heavy boot'; Fable: hem z 28.5, 71-75 hem pts per side inside the cuff at rest, up to 3.1 deep; PG serves the boots
    above our mod, so the collider lives in the cuirass): the cuff's OUTER surface in its band bc['z'] = (zmin, zmax) from the author's boot
    of the same weight (bc['src'].format(variant)) - faces whose normal points away from their own leg's axis (that side's boot points
    at that height) by > .3, wound outward - decided once on _1 (same topology on _0). Returns an object with pos / tris / norm / w / s2b
    (the band's own points) and the source indices (src_v)."""
    _, BT = load(bc['src'].format(variant)); B.to_world(BT); bt = max(BT, key=lambda x: len(x.pos))
    if 'boot_t' not in shared:
        P = bt.pos; T_ = bt.tris; c = P[T_].mean(1); z0, z1 = bc['z']
        fn = np.cross(P[T_[:, 1]] - P[T_[:, 0]], P[T_[:, 2]] - P[T_[:, 0]]); fn /= np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12
        sel = (c[:, 2] >= z0) & (c[:, 2] <= z1); rad = np.zeros((len(c), 2))
        for sgn in (-1.0, 1.0):
            m = sel & (np.sign(c[:, 0] - rig_c[0]) == sgn)
            if not m.any(): continue
            pv = P[(np.sign(P[:, 0] - rig_c[0]) == sgn) & (P[:, 2] >= z0 - 2.0) & (P[:, 2] <= z1 + 2.0)]
            for i in np.where(m)[0]:
                near = pv[np.abs(pv[:, 2] - c[i, 2]) < 2.0]; ax = near[:, :2].mean(0) if len(near) else pv[:, :2].mean(0)
                rad[i] = c[i, :2] - ax
        rad /= np.linalg.norm(rad, axis=1, keepdims=True) + 1e-12; dot = (fn[:, :2] * rad).sum(1)
        out_ = sel & (dot > 0.3); inn_ = sel & (dot < -0.3)
        # the shell's winding = the majority: the minority are the cuff's inside (its lining / thickness) and are left out - one-sided
        flip_ = int(inn_.sum()) > int(out_.sum())
        shared['boot_t'] = (np.where(inn_ if flip_ else out_)[0], flip_)
        log.append(f'boot cuff band z {z0:.1f}..{z1:.1f} from {os.path.basename(bc["src"].format(variant))}: {int(out_.sum())} faces facing out, '
                   f'{int(inn_.sum())} facing in, of {int(sel.sum())} in the band -> the {"inward-wound (flipped)" if flip_ else "outward"} ones')
    ts_, flip_ = shared['boot_t']; tt = bt.tris[ts_][:, [0, 2, 1]] if flip_ else bt.tris[ts_]
    vv = np.unique(tt); rm = np.full(len(bt.pos), -1); rm[vv] = np.arange(len(vv)); tt = rm[tt]
    return type('Boot', (), dict(pos=bt.pos[vv], tris=tt, norm=K.vertex_normals(bt.pos[vv], tt), w=[bt.w[i] for i in vv], s2b=bt.s2b, src_v=vv,
                                  name=bt.name))()


def flare_hem(pc, pants, rig_c, hc, shared, log, ref=None, surf=None):
    """SoS: ease the skirt's hem out of the trousers - only near the hem. hc = dict(clear, full, top): the lining (the piece's
    inward side) is moved radially until it rests >= clear off the trousers below z `full`, fading to no move at z `top`; every
    point of the piece takes the move of the lining under it (same angle + height, smoothed) so the mail and its lining keep
    their gap. RA's clear_legs moved EVERY point (it would push the hip lining - inside the trousers under the mail - out
    through the mail). Braided v1 idle_check: knees out 8-12 deg + a thigh forward sank 16-46 side points 1.5-3.3 deep at
    z 45-52 (the hem sides rest 0.3-1.0 off the trousers). Returns (piece copy, moved point ids, offsets).
    2026-10-14 surf: ease out of that surface instead of the trousers (pos / tris / norm, wound outward: the boot cuff band)"""
    tr = trousers(pants, shared, log) if surf is None else surf
    P = pc.pos.copy(); cx, cy = rig_c
    rad = np.c_[P[:, 0] - cx, P[:, 1] - cy, np.zeros(len(P))]; rad /= np.linalg.norm(rad, axis=1, keepdims=True) + 1e-12
    it = ~G.outer_mask(P, pc.tris, cx, cy); lv = np.unique(pc.tris[it]) if it.mean() >= 0.05 else np.unique(pc.tris)
    if hc.get('src') == 'outer': lv = np.unique(pc.tris[~it])      # v5: read the outer faces (a lining hidden in the trousers must not drag the sheet out)
    fade0 = smooth01((hc['top'] - P[:, 2]) / max(hc['top'] - hc['full'], 1e-3)); fade = fade0
    if 'bottom' in hc: fade = fade0 * smooth01((P[:, 2] - hc['bottom']) / hc.get('bfade', 2.0))     # Officer v4: the hem's welds stay put
    if hc.get('sides'):      # 2026-10-14 (Reach guards side clip): only where |angle| is within (lo, hi) deg, fading over hc['afade'] - the sides
        lo_, hi_ = hc['sides']; af_ = hc.get('afade', 10.0); aa_ = np.abs(np.degrees(np.arctan2(P[:, 0] - cx, P[:, 1] - cy)))
        fade = fade * smooth01((aa_ - lo_) / af_) * smooth01((hi_ - aa_) / af_)
    ang = np.arctan2(P[:, 0] - cx, P[:, 1] - cy)
    cyl = np.c_[14.0 * np.sin(ang), 14.0 * np.cos(ang), P[:, 2]]          # angle + height, radius-free: mail over lining
    rtot = None
    if ref is not None:         # SoS Chainmail: the mail takes the move of the blue skirt's lining under it (same angle / height)
        Lc, Lm = ref
        K_ = np.exp(-(np.linalg.norm(cyl[:, None] - Lc[None], axis=2) / hc.get('sigma', 1.5)) ** 2)
        # Officer v4 hc['ref_mode'] == 'max': this piece eases itself as well and every point takes the LARGER of the two moves, the
        # ref's without the bottom fade - the lining sewn to the mail's hem takes exactly the hem's move at the welds
        rtot = (K_ * Lm[None, :]).max(1) * (fade0 if hc.get('ref_mode') == 'max' else fade); rtot[rtot <= 1e-3] = 0.0
        if hc.get('ref_mode') != 'max':
            tot = rtot; mv = np.where(tot > 0)[0]
            log.append(f'{pc.name}: moved with the layer under it at {len(mv)} of {len(P)} pts (max {tot.max():.2f})')
            out = copy.copy(pc); out.pos = P + tot[:, None] * rad
            return out, mv, (tot[:, None] * rad)[mv], ref
    K_ = np.exp(-(np.linalg.norm(cyl[:, None] - cyl[None, lv], axis=2) / hc.get('sigma', 1.5)) ** 2)
    S_ = B.Surface([('t', tr.pos, tr.tris)]); mov = np.zeros(len(lv)); need0 = None
    for _ in range(10):
        Q = P[lv] + mov[:, None] * rad[lv]
        tri, bary, dist, cp = S_.query(Q, k=8)
        nn = (tr.norm[tr.tris[tri]] * bary[:, :, None]).sum(1); nn /= np.linalg.norm(nn, axis=1, keepdims=True) + 1e-12
        sd = ((Q - cp) * nn).sum(1)
        need = np.maximum(0.0, hc['clear'] - sd) * fade[lv]; need[dist > hc['clear'] + 3.0] = 0.0
        if need0 is None: need0 = need.copy()
        if need.max() <= 1e-3: break
        mov = np.minimum(hc.get('cap', 3.0), mov + need)
    tot = (K_ * mov[None, :]).max(1) * fade                       # every point: the move of the lining at its angle / height
    if rtot is not None: tot = np.maximum(tot, rtot)              # Officer v4 ref_mode max (see above)
    tot[tot <= 1e-3] = 0.0
    mv = np.where(tot > 0)[0]
    log.append(f'{pc.name}: hem eased out of the trousers at {len(mv)} of {len(P)} pts (max {tot.max():.2f}; the lining was up to '
               f'{max(0.0, (need0 / np.maximum(fade[lv], 1e-6)).max() - hc["clear"]):.2f} inside / {int((need0 > 0).sum())} lining pts closer than '
               f'{hc["clear"]} below z {hc["top"]})')
    out = copy.copy(pc); out.pos = P + tot[:, None] * rad
    return out, mv, (tot[:, None] * rad)[mv], (cyl[lv], mov)


def coarse_tris(p):
    """SoS Officer v2: the author's triangles of a split piece (every centre child's three midpoints name its parent's corners),
    for the per-vertex collider shapes made of the source points only (lining_all) - a shape of points with no triangles"""
    n0 = getattr(p, 'n0', None)
    if not n0 or not p.mids: return np.asarray(p.tris)
    out = []
    for t in np.asarray(p.tris):
        if (t >= n0).all():
            par = sorted({x for v in t for x in p.mids[int(v) - n0]})
            if len(par) == 3: out.append(par)
    return np.array(out, int).reshape(-1, 3)


def seam_sides(p, rig):
    """SoS Officer v2: which side of each of a rig's slits a point belongs to (+1 = the panel after it, -1 = before, 0 = in no
    slit), by its texture island's mean angle - tasset plates meet UNWELDED on a seam at the same angle, so the angle alone
    cannot tell their edge points apart (Rig.chains takes the hint)"""
    out = np.zeros(len(p.pos), int)
    if not rig.slits: return out
    isl = islands(p.tris, len(p.pos)); ang = np.degrees(np.arctan2(p.pos[:, 0] - rig.cx, p.pos[:, 1] - rig.cy))
    mean = {}
    for r in np.unique(isl):
        a = np.radians(ang[isl == r]); mean[r] = float(np.degrees(np.arctan2(np.sin(a).mean(), np.cos(a).mean())))
    ma = np.array([mean[r] for r in isl])
    for c, hw, _ in rig.slits:
        inn = np.abs(wrap(ang - c)) <= hw + 1e-6
        out[inn] = np.where(wrap(ma[inn] - c) >= 0, 1, -1)
    return out


def ride_weights(pr, Wr, po, Wo, rig, rd, N, log):
    """SoS Officer v2: the mail's top edge is SEWN to the tassets' turned-under hem (welds at z 61.5-66.7, the gore tips at
    72): under a tasset the mail takes the weights of the tasset surface right over it, fading to its own chains over
    rd['depth'] below the tasset's lowest edge at that angle (tasset points above rd['zmin'] only - not the sash end hanging
    below the folds). The seam never opens (no gap to the trousers under a lifting tasset - the user: 'avoid seeing nothing
    under the armor') and the mail below the tassets swings on its own chains."""
    a_o = np.degrees(np.arctan2(po.pos[:, 0] - rig.cx, po.pos[:, 1] - rig.cy)); ok = po.pos[:, 2] >= rd.get('zmin', -1e9)
    zb = np.full(180, np.inf); bo = np.floor((a_o + 180.0) / 2.0).astype(int) % 180
    for b, z in zip(bo[ok], po.pos[ok, 2]): zb[b] = min(zb[b], z)
    a_r = np.degrees(np.arctan2(pr.pos[:, 0] - rig.cx, pr.pos[:, 1] - rig.cy)); br = np.floor((a_r + 180.0) / 2.0).astype(int) % 180
    zr = np.array([min(zb[(b - 1) % 180], zb[b], zb[(b + 1) % 180]) for b in br])
    dep = rd.get('depth', 5.0)
    r = np.where(np.isfinite(zr), smooth01((pr.pos[:, 2] - (np.where(np.isfinite(zr), zr, 0.0) - dep)) / dep), 0.0)
    if rd.get('at') == 'bottom':       # Officer v4: the lining's BOTTOM edge is sewn to the sheet's hem (36 welds at z 42.7-43.7 men):
        ko_ = {tuple(np.round(x, 3)) for x in po.pos}       # it rides the hem row there, fading out over `depth` above the highest weld
        wz = [float(pr.pos[i, 2]) for i in range(len(pr.pos)) if tuple(np.round(pr.pos[i], 3)) in ko_]
        zw = (max(wz) + 0.2) if wz else -1e9
        r = smooth01((zw + dep - pr.pos[:, 2]) / dep)
        log.append(f'{pr.name} is sewn to {po.name} at {len(wz)} pts (z up to {zw - 0.2:.1f}): rides it there, fading out over {dep} above')
    under, dist = blend_under(B.Surface([('o', po.pos, po.tris)]), po.tris, Wo, pr.pos)
    out = []
    for i in range(len(pr.pos)):
        if r[i] <= 1e-4: out.append(Wr[i]); continue
        w = defaultdict(float)
        for b, x in Wr[i].items(): w[b] += (1 - r[i]) * x
        for b, x in under[i].items(): w[b] += r[i] * x
        out.append(cap4(N, dict(w)))
    log.append(f'{pr.name} rides {po.name} near the seam: {int((r > 0.99).sum())} pts fully, {int(((r > 1e-4) & (r <= 0.99)).sum())} fading over '
               f'{dep} below its lowest edge (z of that edge {np.min(zr[np.isfinite(zr)]):.1f}..{np.max(zr[np.isfinite(zr)]):.1f}); '
               f'{int((~np.isfinite(zr)).sum())} pts with no {po.name} over them')
    return out, r


def cut_panels(pc, cfg, shared, log):
    """v16 (user 2026-10-10: the scale / leather layer 'split into 4 sections', up to the belt): the author's outer sheet is
    one piece joined all round above small notches at the hem (front, back, both sides). Each notch is continued straight up
    to the belt along the mesh's own edges (shortest path keeping to the notch's angle) and the sheet is split there: points
    on the path get a twin for the triangles on one side, so every panel is its own piece of mesh. Decided once on _1
    (indices), the same in _0. Returns the cut piece and a side (+1 / -1 / 0) per point for the panels' chains; the cuts
    become the rig's slits (shared['cuts'], top = the belt line: no links across them)."""
    import heapq
    P, Tr = pc.pos, pc.tris
    if 'cut_sel' not in shared:
        z0, z1 = cfg.get('axis_z', (cfg['sk_belt'] - 10.0, cfg['sk_belt'] - 2.0)); m = (P[:, 2] > z0) & (P[:, 2] < z1)
        cx, cy = float(P[m, 0].mean()), float(P[m, 1].mean())
        kp = {}; wid = np.array([kp.setdefault(tuple(np.round(x, 3)), len(kp)) for x in P])     # welded ids
        nW = len(kp); wpos = np.zeros((nW, 3)); wpos[wid] = P
        wang = np.degrees(np.arctan2(wpos[:, 0] - cx, wpos[:, 1] - cy)); wr = np.hypot(wpos[:, 0] - cx, wpos[:, 1] - cy)
        ec = Counter(); adj = defaultdict(set)
        for t in Tr:
            for a_, b_ in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                u, v = int(wid[a_]), int(wid[b_])
                if u == v: continue
                ec[(min(u, v), max(u, v))] += 1; adj[u].add(v); adj[v].add(u)
        bnd = {x for e, c in ec.items() if c == 1 for x in e}
        hem = float(P[:, 2].min()); top = float(cfg.get('cut_top', cfg['sk_belt'] - 3.0))
        # v18: the cuts stop at the first swinging row (sk_belt - 3), under the cloth's top - cut to the belt (sk_belt + 1) they
        # parted over nothing at the back of the waist (cloth top 69.4, cuirass 74.2) = see-through at a sprint
        if log: log.append(f'{pc.name}: panel cuts stop at z {top:.1f} (hinge row), not at the belt line {cfg["sk_belt"] + 1.0:.1f}')
        cand = sorted([u for u in bnd if hem + 1.0 < wpos[u, 2] < hem + 10.0], key=lambda u: wang[u])
        cl = []
        for u in cand:
            if cl and abs(wrap(wang[u] - wang[cl[-1][-1]])) < 8.0: cl[-1].append(u)
            else: cl.append([u])
        if len(cl) > 1 and abs(wrap(wang[cl[0][0]] - wang[cl[-1][-1]])) < 8.0: cl[0] = cl.pop() + cl[0]
        if cfg.get('cut_angles'):                 # v19b: the cut angles are given (with the gusset gone the open front / back have no
            circ = lambda c: float(np.degrees(np.arctan2(np.mean(np.sin(np.radians(wang[c]))), np.mean(np.cos(np.radians(wang[c]))))))
            apexes = []                           # notch apex of their own: the nearest boundary cluster's top point starts the path,
            for a_t in cfg['cut_angles']:         # the path keeps to the GIVEN angle, and the cut is recorded at it)
                c_ = min(cl, key=lambda c: abs(wrap(circ(c) - a_t)))
                apexes.append((max(c_, key=lambda u: wpos[u, 2]), float(a_t)))
        else:
            apexes = [(u, None) for u in sorted((max(c_, key=lambda u: wpos[u, 2]) for c_ in cl), key=lambda u: -wpos[u, 2])[:cfg['cut_panels']]]
        cuts = []
        for ap, a_t in sorted(apexes, key=lambda x: wang[x[0]]):
            a0 = float(wang[ap]) if a_t is None else a_t
            if a_t is not None:                   # v19b: an opening already parted up to the hinge row (the gusset gone) needs no path:
                ep = [u for u in bnd if abs(wrap(wang[u] - a0)) < 35.0 and hem + 1.0 < wpos[u, 2] < top + 3.0]   # its edge points ARE the cut
                if ep and max(wpos[u, 2] for u in ep) >= top - 0.6:
                    L_ = [u for u in ep if wrap(wang[u] - a_t) < 0]; R_ = [u for u in ep if wrap(wang[u] - a_t) >= 0]
                    if L_ and R_:                 # the slit is centred between the opening's two edges (the author's V is off the
                        aL, aR = circ(L_), circ(R_); a0 = float(wrap(aL + wrap(aR - aL) / 2.0))   # target angle, women's by ~10 deg)
                    else: a0 = circ(ep)
                    cuts.append((a0, sorted(ep, key=lambda u: wpos[u, 2]), True)); continue
            perp = lambda u: abs(wr[u] * np.sin(np.radians(wrap(wang[u] - a0))))
            dist = {ap: 0.0}; prev = {}; hq = [(0.0, ap)]; end = None
            while hq:
                dcur, u = heapq.heappop(hq)
                if dcur > dist.get(u, 1e18): continue
                if wpos[u, 2] >= top - 0.6 and perp(u) < 2.0: end = u; break
                for v in adj[u]:
                    L = float(np.linalg.norm(wpos[v] - wpos[u])); mid = 0.5 * (perp(u) + perp(v))
                    c_ = L * (1.0 + 3.0 * mid) + (5.0 * L if wpos[v, 2] < wpos[u, 2] - 0.05 else 0.0)
                    if dcur + c_ < dist.get(v, 1e18): dist[v] = dcur + c_; prev[v] = u; heapq.heappush(hq, (dcur + c_, v))
            if end is None: raise RuntimeError(f'cut at {a0:.0f} deg: no path to the belt')
            path = [end]
            while path[-1] != ap: path.append(prev[path[-1]])
            path = path[::-1]
            open_ = all(ec.get((min(int(path[i]), int(path[i + 1])), max(int(path[i]), int(path[i + 1]))), 0) == 1 for i in range(len(path) - 1))
            cuts.append((a0, path, open_))         # v19b: open_ = the sheet is already parted along the path (gusset gone): nothing to split
        # sides (v17): flood over the triangles round each cut, never across a path edge - one label per panel. v16 took the
        # side of each triangle by its centre's angle against the path: where the path zig-zags (the side cuts, z 61-70) some
        # triangles landed on the wrong side, the side panels stayed joined there and a 16-degree strip of one panel rode the
        # other's chains (user 2026-10-10: 'the sides are twitching and deforming and moving on its own', panels 'stick together')
        from collections import deque
        side_t = np.zeros(len(Tr), int); lab_t = np.zeros(len(Tr), int); tw_ = wid[Tr]
        tc = P[Tr].mean(1); tang = np.degrees(np.arctan2(tc[:, 0] - cx, tc[:, 1] - cy)); tzmax = P[Tr][:, :, 2].max(1)
        for a0, path, open_ in cuts:
            if open_: continue                         # v19b: no sheet to split here, no sides to label, no twins
            pe = {(min(int(path[i]), int(path[i + 1])), max(int(path[i]), int(path[i + 1]))) for i in range(len(path) - 1)}
            ztw = float(wpos[path[-2], 2])                 # the highest twinned point: above it the sheet is whole
            pw = set(path[:-1])                            # + every triangle touching a twinned point (the fan round the
            touch = np.array([any(int(x) in pw for x in t) for t in tw_])   # top one reaches above it; v17 first left those
            reg = np.where((np.abs(wrap(tang - a0)) < 30.0) & ((tzmax <= ztw + 1e-3) | touch))[0]   # out = a sliver joining panels)
            e2t = defaultdict(list)
            for ti in reg:
                t = tw_[ti]
                for a_, b_ in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                    e = (min(int(a_), int(b_)), max(int(a_), int(b_)))
                    if e[0] != e[1] and e not in pe: e2t[e].append(ti)
            lab = {}
            for sgn in (1, -1):
                seeds = [ti for ti in reg if sgn * wrap(tang[ti] - a0) > 22.0]
                for s_ in seeds:
                    if lab.get(s_, sgn) != sgn: raise RuntimeError(f'cut at {a0:.0f} deg: the path does not split the sheet')
                    lab[s_] = sgn
                dq = deque(seeds)
                while dq:
                    t = tw_[dq.popleft()]
                    for a_, b_ in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                        for tj in e2t.get((min(int(a_), int(b_)), max(int(a_), int(b_))), ()):
                            if tj not in lab: lab[tj] = sgn; dq.append(tj)
                            elif lab[tj] != sgn: raise RuntimeError(f'cut at {a0:.0f} deg: the path does not split the sheet')
            pw = set(path[:-1])
            for ti, s_ in lab.items(): lab_t[ti] = s_
            for ti in reg:
                if any(int(x) in pw for x in tw_[ti]):
                    if ti not in lab: raise RuntimeError(f'cut at {a0:.0f} deg: triangle {ti} by the path reached from neither side')
                    side_t[ti] = lab[ti]
        used = defaultdict(set)
        for ti, t in enumerate(Tr):
            if side_t[ti]:
                for x in t: used[int(x)].add(int(side_t[ti]))
        cutw = {u for _, path, op in cuts if not op for u in path[:-1]}
        dup = sorted(i for i in range(len(P)) if int(wid[i]) in cutw and used[i] == {1, -1})
        open_hw = {a0: float(min(12.0, max(abs(wrap(wang[u] - a0)) for u in path) + 0.5)) for a0, path, op in cuts if op}   # the opening's half-width about its own centre
        shared['cut_sel'] = dict(side_t=side_t, lab_t=lab_t, dup=dup, cuts=cuts, cx=cx, cy=cy, top=top, open_hw=open_hw)
        lg = [f'{a0:.1f} deg: {len(path) - 1} edges, z {wpos[path[0], 2]:.1f} -> {wpos[path[-1], 2]:.1f}, off the line max '
              f'{max(abs(wr[u] * np.sin(np.radians(wrap(wang[u] - a0)))) for u in path):.2f}' + (' (already open)' if op else '') for a0, path, op in cuts]
        if log: log.append(f'{pc.name} cut into {len(cuts)} panels up to z {top:.1f}: ' + '; '.join(lg) + f'; {len(dup)} points twinned')
    cs = shared['cut_sel']; side_t, dup = cs['side_t'], cs['dup']
    n = len(P); remap = {i: n + j for j, i in enumerate(dup)}
    tris = Tr.copy()
    for ti in np.where(side_t > 0)[0]:
        tris[ti] = [remap.get(int(x), int(x)) for x in Tr[ti]]
    n0 = pc.n0 if pc.n0 else n
    mids = list(pc.mids) + [(i, i) for i in dup]
    new = Piece(pc.name, pc.src, pc.role, np.r_[P, P[dup]], np.r_[pc.uv, pc.uv[dup]], (np.r_[pc.nrm, pc.nrm[dup]] if pc.nrm is not None else None),
                list(pc.ow) + [pc.ow[i] for i in dup], tris, pc.partid, np.r_[pc.src_idx, -np.ones(len(dup), int)], mids, n0,
                col=(np.r_[pc.col, pc.col[dup]] if pc.col is not None else None))
    # side per point (v17): the label of the panel its triangles belong to (the flood above); 0 above the cut's top
    Pn = new.pos; cx, cy = cs['cx'], cs['cy']; an = np.degrees(np.arctan2(Pn[:, 0] - cx, Pn[:, 1] - cy))
    side = np.zeros(len(Pn), int); cuts_out = []
    for ti in np.where(cs['lab_t'] != 0)[0]:
        for v in tris[ti]: side[int(v)] = int(cs['lab_t'][ti])
    adjt = np.where(side_t != 0)[0]
    for a0, path, op in cs['cuts']:
        vv = np.unique(tris[adjt]); vv = vv[np.abs(wrap(an[vv] - a0)) < 20.0]
        hw = cs['open_hw'][a0] if op else (float(min(15.0, np.abs(wrap(an[vv] - a0)).max() + 0.5)) if len(vv) else 2.0)
        cuts_out.append((float(a0), hw, cs['top']))
    shared['cuts'] = cuts_out
    if log: log.append(f'{pc.name} panels: cuts (angle / band half-width / top) ' + ', '.join(f'{a:.1f}/{h:.1f}/{t:.1f}' for a, h, t in cuts_out))
    return new, side


def _ear_clip(xy):
    """triangles (index triples into xy) of a simple polygon, or None"""
    idx = list(range(len(xy)))
    if 0.5 * sum(xy[i - 1][0] * xy[i][1] - xy[i][0] * xy[i - 1][1] for i in range(len(xy))) < 0: idx = idx[::-1]
    out = []
    while len(idx) > 3:
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = xy[i0], xy[i1], xy[i2]
            if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) <= 1e-9: continue
            inside = False
            for j in idx:
                if j in (i0, i1, i2): continue
                p = xy[j]
                d1 = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
                d2 = (c[0] - b[0]) * (p[1] - b[1]) - (c[1] - b[1]) * (p[0] - b[0])
                d3 = (a[0] - c[0]) * (p[1] - c[1]) - (a[1] - c[1]) * (p[0] - c[0])
                if d1 >= -1e-9 and d2 >= -1e-9 and d3 >= -1e-9: inside = True; break
            if inside: continue
            out.append((i0, i1, i2)); idx.pop(k); break
        else:
            return None
    out.append(tuple(idx))
    return out


def fill_notches(pc, cfg, shared, log):
    """v17 (user 2026-10-10: the inner cloth is 'supposed to be one piece', like the New Legion light armour / Sir Duncan):
    the author's cloth has a notch in its hem band under each of the outer layer's cuts (men 3 units tall, women 4-5); with
    the panels parting to the belt the cloth read as 4 pieces. Each notch is closed with a patch on its own open edge
    (ear-clipped, closed straight across the hem), so the cloth is one full skirt behind every gap. The patch's points are
    twins of the notch's edge points (same place, weights and slider data) with their own UVs: each half mirrors the hem
    band beside it (the atlas under the notch is unpainted). Decided once on _1 (indices), the same in _0."""
    P, Tr = pc.pos, pc.tris
    if 'fill_sel' not in shared:
        z0, z1 = cfg.get('axis_z', (cfg['sk_belt'] - 10.0, cfg['sk_belt'] - 2.0)); m = (P[:, 2] > z0) & (P[:, 2] < z1)
        cx, cy = float(P[m, 0].mean()), float(P[m, 1].mean())
        kp = {}; wid = np.array([kp.setdefault(tuple(np.round(x, 3)), len(kp)) for x in P])
        nW = len(kp); wpos = np.zeros((nW, 3)); wpos[wid] = P; rep_i = np.zeros(nW, int); rep_i[wid] = np.arange(len(P))
        wang = np.degrees(np.arctan2(wpos[:, 0] - cx, wpos[:, 1] - cy)); wr = np.hypot(wpos[:, 0] - cx, wpos[:, 1] - cy)
        ec = Counter()
        for t in Tr:
            for a_, b_ in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                u, v = int(wid[a_]), int(wid[b_])
                if u != v: ec[(min(u, v), max(u, v))] += 1
        badj = defaultdict(list)
        for (u, v), c in ec.items():
            if c == 1: badj[u].append(v); badj[v].append(u)
        start = min(badj, key=lambda u: wpos[u, 2]); loop = [start]; prev = None
        while True:                                   # the hem's open edge, in order
            if len(badj[loop[-1]]) != 2: raise RuntimeError(f'{pc.name}: the hem edge is not a simple loop at z {wpos[loop[-1], 2]:.1f}')
            cur = next(x for x in badj[loop[-1]] if x != prev); prev = loop[-1]
            if cur == start: break
            loop.append(cur)
        L = np.array(loop); zl = wpos[L, 2]; nL = len(L); hem = float(zl.min()); up = zl > hem + 2.5
        o0 = int(np.where(~up)[0][0]); runs, cur = [], []
        for k in [(o0 + j) % nL for j in range(nL)]:
            if up[k]: cur.append(k)
            elif cur: runs.append(cur); cur = []
        if cur: runs.append(cur)
        hor = lambda a, b: float(np.radians(abs(wrap(wang[L[a]] - wang[L[b]])))) * 0.5 * (wr[L[a]] + wr[L[b]])
        tc = P[Tr].mean(1); tang = np.degrees(np.arctan2(tc[:, 0] - cx, tc[:, 1] - cy))
        new_src, new_uv, new_tris, lg = [], [], [], []
        for run in runs:
            a = run[0]
            while zl[(a - 1) % nL] < zl[a] - 1e-4 and zl[a] - zl[(a - 1) % nL] > 0.35 * hor(a, (a - 1) % nL): a = (a - 1) % nL
            b = run[-1]
            while zl[(b + 1) % nL] < zl[b] - 1e-4 and zl[b] - zl[(b + 1) % nL] > 0.35 * hor(b, (b + 1) % nL): b = (b + 1) % nL
            seq = [a]
            while seq[-1] != b: seq.append((seq[-1] + 1) % nL)
            ws = [int(L[k]) for k in seq]
            ac = float(np.degrees(np.angle(np.exp(1j * np.radians(wang[ws])).mean()))); rm = float(wr[ws].mean())
            xy = [(float(np.radians(wrap(wang[w] - ac))) * rm, float(wpos[w, 2])) for w in ws]
            tri = _ear_clip(xy)
            if tri is None: raise RuntimeError(f'{pc.name}: notch at {ac:.0f} deg is not a simple polygon')
            # the piece's own surface near the notch, unwrapped, for the mirrored UV look-up
            near = np.where(np.abs(wrap(tang - ac)) < 45.0)[0]
            Q = np.stack([np.radians(wrap(np.degrees(np.arctan2(P[:, 0] - cx, P[:, 1] - cy)) - ac)) * rm, P[:, 2]], 1)

            def uv_at(x, z):
                for ti in near:
                    t = Tr[ti]; A_, B_, C_ = Q[t[0]], Q[t[1]], Q[t[2]]
                    den = (B_[1] - C_[1]) * (A_[0] - C_[0]) + (C_[0] - B_[0]) * (A_[1] - C_[1])
                    if abs(den) < 1e-12: continue
                    l1 = ((B_[1] - C_[1]) * (x - C_[0]) + (C_[0] - B_[0]) * (z - C_[1])) / den
                    l2 = ((C_[1] - A_[1]) * (x - C_[0]) + (A_[0] - C_[0]) * (z - C_[1])) / den
                    if l1 >= -1e-6 and l2 >= -1e-6 and l1 + l2 <= 1 + 1e-6:
                        return l1 * pc.uv[t[0]] + l2 * pc.uv[t[1]] + (1 - l1 - l2) * pc.uv[t[2]]
                j = near_v[np.argmin((Q[near_v, 0] - x) ** 2 + (Q[near_v, 1] - z) ** 2)]
                return pc.uv[j]
            near_v = np.unique(Tr[near])
            xa, xb = xy[0][0], xy[-1][0]
            slot = {}
            for t3 in tri:
                xc = np.mean([xy[k][0] for k in t3]); sd = 0 if abs(xc - xa) <= abs(xc - xb) else 1; xm = (xa, xb)[sd]
                ids = []
                for k in t3:
                    if (k, sd) not in slot:
                        slot[(k, sd)] = len(new_src)
                        new_src.append(int(rep_i[ws[k]])); new_uv.append(uv_at(2 * xm - xy[k][0], xy[k][1]))
                    ids.append(slot[(k, sd)])
                pa, pb, pc_ = (wpos[ws[k]] for k in t3)
                nrm_ = np.cross(pb - pa, pc_ - pa); cen = (pa + pb + pc_) / 3
                new_tris.append(ids if nrm_[0] * (cen[0] - cx) + nrm_[1] * (cen[1] - cy) > 0 else [ids[0], ids[2], ids[1]])
            lg.append(f'{ac:.0f} deg ({abs(xb - xa):.1f} wide, {max(p[1] for p in xy) - min(xy[0][1], xy[-1][1]):.1f} tall, {len(tri)} tris)')
        pid = Counter(int(pc.partid[ti]) for ti in range(len(Tr)) if np.isin(wid[Tr[ti]], list({int(L[k]) for r in runs for k in r})).any())
        shared['fill_sel'] = dict(src=new_src, uv=np.array(new_uv), tris=np.array(new_tris, int),
                                  partid=(pid.most_common(1)[0][0] if pid else int(pc.partid[0])))
        if log: log.append(f'{pc.name}: {len(runs)} hem notches closed (one full skirt): ' + ', '.join(lg) + f'; {len(new_src)} points added')
    fs = shared['fill_sel']; n = len(P); src = fs['src']
    n0 = pc.n0 if pc.n0 else n
    return Piece(pc.name, pc.src, pc.role, np.r_[P, P[src]], np.r_[pc.uv, fs['uv']], (np.r_[pc.nrm, pc.nrm[src]] if pc.nrm is not None else None),
                 list(pc.ow) + [pc.ow[i] for i in src], np.r_[Tr, fs['tris'] + n], np.r_[pc.partid, np.full(len(fs['tris']), fs['partid'])],
                 np.r_[pc.src_idx, -np.ones(len(src), int)], list(pc.mids) + [(i, i) for i in src], n0,
                 col=(np.r_[pc.col, pc.col[src]] if pc.col is not None else None))


def canon_names(T, shared, variant, log=None):
    """the author's original _0 meshes name some shapes differently from the _1 ones (same points and triangles): use the _1
    names (decided by point / triangle count, only where that is unambiguous)"""
    if variant == '1':
        shared['names_1'] = [(t.name, len(t.pos), len(t.tris)) for t in T]; return
    # v23: decide every rename first, then apply - the Elite Wolf men's _0 chains its names (its 'main3_1' is the _1 'main3_2'
    # while its 'Fur' is the _1 'main3_1'), which a one-pass rename blocked
    want = {}
    for t in T:
        m = [n for n, a, b in shared.get('names_1', []) if (a, b) == (len(t.pos), len(t.tris))]
        if len(m) == 1 and m[0] != t.name: want[t.name] = m[0]
    final = {t.name: want.get(t.name, t.name) for t in T}
    if len(set(final.values())) == len(final):                 # a clean bijection: apply all
        for t in T:
            if t.name in want:
                if log is not None: log.append(f'_{variant}: shape {t.name} = the _1 mesh shape {want[t.name]} (renamed)')
                t.name = want[t.name]
    else:
        for t in T:
            m = want.get(t.name)
            if m and m not in [u.name for u in T]:
                if log is not None: log.append(f'_{variant}: shape {t.name} = the _1 mesh shape {m} (renamed)')
                t.name = m


def build(design, g, variant, shared, log, rec=None):
    Dz = DESIGNS[design]; cfg = Dz[g]; N = Names(Dz['prefix'])
    if g in ('m', 'v'):
        src = cfg['src'].format(variant)
    else:
        # SoS: the ORIGINAL set of the design's own .osp (never our installed override of it)
        tree = ET.parse(cfg['osp']); ss = next(s for s in tree.getroot().findall('SliderSet') if s.get('name') == cfg['set'])
        src = os.path.dirname(os.path.dirname(cfg['osp'])) + f'/ShapeData/{ss.findtext("DataFolder")}/{ss.findtext("SourceFile")}'
        shared['f_paths'] = dict(nif=src, osd=src[:-4] + '.osd', ss=ss, folder=ss.findtext('DataFolder'), srcfile=ss.findtext('SourceFile'))
    nif, T = load(src); B.to_world(T)
    canon_names(T, shared, variant, log)
    S = {t.name: t for t in T}
    shared.setdefault('s2b_all', {})
    for t in T: shared['s2b_all'].update(t.s2b)
    sig = sorted((t.name, len(t.pos), len(t.tris)) for t in T if not (cfg.get('pants_vary') and t.name == cfg['pants']))
    if 'sig' in shared and shared['sig'] != sig: raise RuntimeError(f'{g}_{variant} topology differs')
    first = 'sig' not in shared; shared['sig'] = sig
    pieces, rest = cut_pieces(T, S, cfg, log if first else [], memo=shared)
    P_ = {p.name: p for p in pieces}
    skirts = [p for p in pieces if p.role.startswith('skirt')]
    if cfg.get('drop_gusset'):                    # v19b: the brown strip bridging the front / back openings is not the cloth skirt
        for i, p in enumerate(skirts):
            if p.role == 'skirt:outer':
                skirts[i] = drop_gusset(p, cfg['drop_gusset'], variant, shared, log if first else []); P_[p.name] = skirts[i]
    flaps = next((p for p in pieces if p.role == 'flaps'), None); belt = next((p for p in pieces if p.role == 'belt'), None)
    if belt is not None:
        # belt: band piece = the component with the lowest point (the hanging tip); tip = its points below the band's edge
        blab = D.welded_components(belt.pos, belt.tris)
        if 'belt_sel' not in shared:              # decided once, on _1 (the thin vanilla women's _0 cut its tail elsewhere)
            band = min(range(blab.max() + 1), key=lambda k: belt.pos[blab == k, 2].min())
            bv = np.where(blab == band)[0]; bp = belt.pos[bv]
            bcx, bcy = bp[:, 0].mean(), bp[:, 1].mean(); bth = np.degrees(np.arctan2(bp[:, 0] - bcx, bp[:, 1] - bcy))
            mins = [bp[(bth >= a) & (bth < a + 10), 2].min() for a in range(-180, 180, 10) if ((bth >= a) & (bth < a + 10)).any()]
            med = float(np.median(mins)); edge = min(m for m in mins if m > med - 3.0); split = edge - 0.3
            if cfg.get('tail_split') is not None:     # v5: the piece is only the tail (its band is part of a static shape)
                split = float(cfg['tail_split']); edge = split + 0.3
            shared['belt_sel'] = (band, edge, split, bv[belt.pos[bv, 2] < split])
        band, edge, split, tip_src = shared['belt_sel']
    else:                                         # v5: no hanging belt (it is part of the cuirass)
        belt = Piece('__nobelt__', None, 'belt', np.zeros((0, 3)), np.zeros((0, 2)), None, [], np.zeros((0, 3), int), np.zeros(0, int), np.zeros(0, int))
        blab, band, edge, split, tip_src = np.zeros(0, int), -1, 0.0, 0.0, np.zeros(0, int)
    has_belt = belt.name != '__nobelt__'
    # split (men): skirt layers whole, the belt tip
    if 'tip' in cfg['subdiv'] and has_belt:
        tsel = np.isin(belt.tris, tip_src).all(1); belt = split_piece(belt, tsel); P_[belt.name] = belt
        blab = np.r_[blab, [blab[a] for a, b in belt.mids]]
    if cfg.get('fill_notches'):                   # v17: the inner cloth one full skirt (its hem notches under the cuts closed)
        for i, p in enumerate(skirts):
            if p.role == 'skirt:outer':
                skirts[i] = fill_notches(p, cfg, shared, log if first else []); P_[p.name] = skirts[i]
    for i, p in enumerate(skirts):
        if p.name in cfg['subdiv']: skirts[i] = split_piece(p); P_[p.name] = skirts[i]
    cut_side = {}
    if cfg.get('cut_panels'):                     # v16: the outer layer in separate panels (user: '4 sections', up to the belt)
        for i, p in enumerate(skirts):
            if p.role == 'skirt:outer':
                skirts[i], cut_side[p.name] = cut_panels(p, cfg, shared, log if first else []); P_[p.name] = skirts[i]
    if cfg.get('leg_clear'):                      # v19 (pass B): the author's cloth lining sits INSIDE the baggy trousers at rest
        for i, p in enumerate(skirts):            # (hidden under the mail, never meant to show) - the legs poked through it at the
            if p.role == 'skirt:outer':           # cuts and only its hem row ever qualified as a collider. Move it out first.
                skirts[i], mv_, off_ = clear_legs(p, pants_of(S, cfg), cfg['leg_clear'], shared, log if first else []); P_[p.name] = skirts[i]
                if len(mv_): rec_lift(shared, variant, p.name, mv_.tolist(), off_.tolist())   # verify undoes it
    if cfg.get('hem_clear'):                      # SoS: ease the hem out of the trousers (idle stance sank the hem sides)
        pn_ = pants_of(S, cfg); rc_ = (float(pn_.pos[:, 0].mean()), float(pn_.pos[:, 1].mean()))
        # the layer against the trousers is eased: the inner skirt when there is one (Chainmail's blue skirt), else the outer;
        # the outer then takes the inner's move at the same angle / height (stays over it)
        inn = [i for i, p in enumerate(skirts) if p.role == 'skirt:inner']; ref_ = None
        for i in inn + [i for i, p in enumerate(skirts) if p.role == 'skirt:outer']:
            p = skirts[i]
            skirts[i], mv_, off_, r_ = flare_hem(p, pn_, rc_, cfg['hem_clear'], shared, log if first else [], ref=ref_ if p.role == 'skirt:outer' else None)
            if p.role == 'skirt:inner': ref_ = r_ if ref_ is None else (np.vstack([ref_[0], r_[0]]), np.r_[ref_[1], r_[1]])
            P_[p.name] = skirts[i]
            if len(mv_): rec_lift(shared, variant, p.name, mv_.tolist(), off_.tolist())   # verify undoes it
    if cfg.get('boot_coll'):                      # 2026-10-14: the hem eased out of the paired boot's cuff (boot_band) - after hem_clear
        bc_ = cfg['boot_coll']; pn_ = pants_of(S, cfg); rc_ = (float(pn_.pos[:, 0].mean()), float(pn_.pos[:, 1].mean()))
        band_ = boot_band(bc_, variant, shared, log if first else [], rc_); shared['boot_band_' + variant] = band_
        inn = [i for i, p in enumerate(skirts) if p.role == 'skirt:inner']; ref_ = None
        for i in inn + [i for i, p in enumerate(skirts) if p.role == 'skirt:outer']:
            p = skirts[i]
            skirts[i], mv_, off_, r_ = flare_hem(p, None, rc_, bc_['hem'], shared, log, ref=ref_ if p.role == 'skirt:outer' else None, surf=band_)
            if p.role == 'skirt:inner': ref_ = r_ if ref_ is None else (np.vstack([ref_[0], r_[0]]), np.r_[ref_[1], r_[1]])
            P_[p.name] = skirts[i]
            if len(mv_): rec_lift(shared, variant, p.name, mv_.tolist(), off_.tolist())
    if cfg.get('layer_flare'):                    # SoS Officer v2: per piece, in order (name, hc, take the earlier pieces' moves):
        # the blue skirt's lining sat INSIDE the trousers above z ~48 - eased >= hc['clear'] off them below hc['full'] (fading out by
        # hc['top']) so it can carry leg colliders over the thighs; its hem row / front strip take the lining's move
        pn_ = pants_of(S, cfg); rc_ = (float(pn_.pos[:, 0].mean()), float(pn_.pos[:, 1].mean())); ref_ = None
        for nm_, hc_, use_ref in cfg['layer_flare']:
            i = next(i for i, p in enumerate(skirts) if p.name == nm_); p = skirts[i]
            skirts[i], mv_, off_, r_ = flare_hem(p, pn_, rc_, hc_, shared, log if first else [], ref=ref_ if use_ref else None)
            if not use_ref: ref_ = r_ if ref_ is None else (np.vstack([ref_[0], r_[0]]), np.r_[ref_[1], r_[1]])
            P_[p.name] = skirts[i]
            if len(mv_): rec_lift(shared, variant, p.name, mv_.tolist(), off_.tolist())   # verify undoes it
    # SoS: hanging tails (the sash end) - pieces of their own, split x4 like the belt tip when listed in subdiv
    for q in [q for q in pieces if q.role == 'tail' and q.name in cfg['subdiv']]:
        P_[q.name] = split_piece(P_[q.name])
    if cfg.get('lining_clear'):    # v7 (Officer, user: 'when the embroidered cloth stretches, the embroidered part disappears'): the author's
        # lining lies within ~0.1 of the sheet just above their welded hem edge; two surfaces that close z-fight through each other as
        # soon as the skin stretches between chains. The lining's points closer than `clear` to the sheet's outer face are moved inward
        # to `clear` along the sheet's normal, fading out over `fade` above the weld (the welded edge stays); recorded as a lift
        lc_ = cfg['lining_clear']; nm_ = lc_.get('piece', next(p.name for p in skirts if p.role == 'skirt:outer')); p = P_[nm_]
        pl_ = pants_of(S, cfg); rl_ = (float(pl_.pos[:, 0].mean()), float(pl_.pos[:, 1].mean()))
        om_ = G.outer_mask(p.pos, p.tris, rl_[0], rl_[1]); ot_ = p.tris[om_]
        inner_v = np.setdiff1d(np.unique(p.tris[~om_]), np.unique(ot_))       # the lining: points in no outward-facing triangle
        if len(inner_v) and len(ot_):
            fnu = np.cross(p.pos[ot_[:, 1]] - p.pos[ot_[:, 0]], p.pos[ot_[:, 2]] - p.pos[ot_[:, 0]]); fnu = fnu / (np.linalg.norm(fnu, axis=1, keepdims=True) + 1e-12)
            q_ = p.pos[inner_v]; tri_, _, d_, cp_ = B.Surface([('o', p.pos, ot_)]).query(q_, k=8)
            h_ = ((q_ - cp_) * fnu[tri_]).sum(1); lat_ = np.sqrt(np.maximum(d_ ** 2 - h_ ** 2, 0.0))
            zw_ = float(lc_.get('weld', q_[:, 2].min())); fade_ = smooth01((q_[:, 2] - zw_ - float(lc_.get('weld_keep', 0.5))) / float(lc_.get('fade', 1.5)))
            need_ = np.where((lat_ < 1.0) & (h_ > -float(lc_['clear'])) & (h_ < 0.5), np.maximum(0.0, float(lc_['clear']) + h_), 0.0)
            Kd_ = np.exp(-(np.linalg.norm(q_[:, None] - q_[None], axis=2) / float(lc_.get('sigma', 1.5))) ** 2)
            tot_ = (Kd_ * need_[None, :]).max(1) * fade_; tot_[tot_ <= 1e-3] = 0.0
            nd_ = Kd_ @ fnu[tri_]; nd_ = nd_ / (np.linalg.norm(nd_, axis=1, keepdims=True) + 1e-12)
            offs_ = -tot_[:, None] * nd_; mv_ = tot_ > 0
            if mv_.any():
                q2 = copy.copy(p); q2.pos = p.pos.copy(); q2.pos[inner_v[mv_]] += offs_[mv_]; P_[nm_] = q2
                for i_, s_ in enumerate(skirts):
                    if s_.name == nm_: skirts[i_] = q2
                rec_lift(shared, variant, nm_, inner_v[mv_].tolist(), offs_[mv_].tolist())
            if first: log.append(f'{g}: lining clearance: {int(mv_.sum())} of {len(inner_v)} lining pts of {nm_} moved inward by up to {tot_.max():.2f} '
                                 f'({int((need_ > 0).sum())} were closer than {lc_["clear"]} to the sheet, nearest {h_[(lat_ < 1.0)].max():+.2f}; weld at z {zw_:.1f} kept)')
    if cfg.get('layer_lift'):      # v7 (Officer, user: the plates sit INSIDE the mail at idle): a layer whose underside rests ON the layer
        # below it (the plates' turned-under trim on the mail: gap 0 by the author's design) shows that layer through itself at the first
        # tenth of a unit of relative motion, and no collider can defend a gap that is not there. Rotate it outward about its hinge until
        # every point of it clears the layer below by `clear` - a rigid rotation (its seam at the hinge never opens) - and the pieces sewn
        # to it (the sash) turn with it. Recorded as a lift (verify undoes it).
        pl_ = pants_of(S, cfg); rl_ = (float(pl_.pos[:, 0].mean()), float(pl_.pos[:, 1].mean()))
        for names_, lc_ in cfg['layer_lift']:
            up_ = P_[lc_['under']]; om_ = G.outer_mask(up_.pos, up_.tris, rl_[0], rl_[1]); ut_ = up_.tris[om_]
            fnu = np.cross(up_.pos[ut_[:, 1]] - up_.pos[ut_[:, 0]], up_.pos[ut_[:, 2]] - up_.pos[ut_[:, 0]]); fnu = fnu / (np.linalg.norm(fnu, axis=1, keepdims=True) + 1e-12)
            usurf = B.Surface([('u', up_.pos, ut_)]); hz = float(lc_['hinge']); clear_ = float(lc_['clear']); ang_ = 0.0
            p0 = P_[names_[0]]
            tri_, _, d_, cp_ = usurf.query(p0.pos, k=8); h_ = ((p0.pos - cp_) * fnu[tri_]).sum(1); lat_ = np.sqrt(np.maximum(d_ ** 2 - h_ ** 2, 0.0))
            on_ = (lat_ < 1.0) & (p0.pos[:, 2] < hz - 2.0) & (h_ < clear_) & (h_ > -2.0)
            if on_.any(): ang_ = min(float(lc_.get('max', 0.12)), float(((clear_ - h_[on_]) / (hz - p0.pos[on_, 2])).max()))
            shared['belt_lift'] = (ang_, hz) if any(P_[nm_].role == 'belt' for nm_ in names_) else None
            if ang_ > 1e-4:
                for nm_ in [n_ for n_ in names_ if P_[n_].role != 'belt']:     # the belt's strap: after its tip split (the rig block)
                    p = P_[nm_]; rad_ = np.c_[p.pos[:, 0] - rl_[0], p.pos[:, 1] - rl_[1], np.zeros(len(p.pos))]; rad_ /= np.linalg.norm(rad_, axis=1, keepdims=True) + 1e-12
                    dr_ = ang_ * np.maximum(0.0, hz - p.pos[:, 2]); offs_ = dr_[:, None] * rad_; mv_ = dr_ > 1e-4
                    q = copy.copy(p); q.pos = p.pos + offs_; P_[nm_] = q
                    for i_, s_ in enumerate(skirts):
                        if s_.name == nm_: skirts[i_] = q
                    rec_lift(shared, variant, nm_, np.where(mv_)[0].tolist(), offs_[mv_].tolist())
                if first: log.append(f'{g}: layer lift: {", ".join(names_)} rotated {np.degrees(ang_):.1f} deg outward about the hinge at {hz:.1f} so {names_[0]} clears {lc_["under"]} by {clear_} ({int(on_.sum())} pts were closer, min {h_[on_].min():+.2f})')
            elif first: log.append(f'{g}: layer lift: {names_[0]} already clears {lc_["under"]} by {clear_}')
    if cfg.get('layer_clear'):     # v10 (Officer, user: the mail through the front plate's trim at its side edge): the lift is a rigid rotation
        # capped at 0.12 rad - points near its pivot gain almost nothing by it (the side plates' rims rested 0.21 over the mail at z 66.7,
        # the trim faces 0.42). Every point of the named pieces below zmax that projects onto the layer under it closer than `clear` is
        # pushed out along that layer's normal to `clear`, spread over the piece (sigma) and faded to nothing at zmax over `fade` (the rows
        # under the band stay put: a slot at the band's edge is what pivoting higher opened). Recorded as a lift (verify undoes it).
        pl_ = pants_of(S, cfg); rl_ = (float(pl_.pos[:, 0].mean()), float(pl_.pos[:, 1].mean()))
        for names_, lc_ in cfg['layer_clear']:
            up_ = P_[lc_['under']]; om_ = G.outer_mask(up_.pos, up_.tris, rl_[0], rl_[1]); ut_ = up_.tris[om_]
            fnu = np.cross(up_.pos[ut_[:, 1]] - up_.pos[ut_[:, 0]], up_.pos[ut_[:, 2]] - up_.pos[ut_[:, 0]]); fnu = fnu / (np.linalg.norm(fnu, axis=1, keepdims=True) + 1e-12)
            usurf = B.Surface([('u', up_.pos, ut_)]); clear_ = float(lc_['clear']); zmax_ = float(lc_['zmax']); fade_ = float(lc_.get('fade', 2.0)); sig_ = float(lc_.get('sigma', 2.0))
            for nm_ in names_:
                p = P_[nm_]; tri_, _, d_, cp_ = usurf.query(p.pos, k=8); h_ = ((p.pos - cp_) * fnu[tri_]).sum(1); lat_ = np.sqrt(np.maximum(d_ ** 2 - h_ ** 2, 0.0))
                need_ = np.where((lat_ < 1.0) & (h_ < clear_) & (h_ > -1.0) & (p.pos[:, 2] < zmax_), clear_ - h_, 0.0)
                if not (need_ > 0).any():
                    if first: log.append(f'{g}: layer clear: {nm_} already clears {lc_["under"]} by {clear_} below z {zmax_:.1f}')
                    continue
                Kd_ = np.exp(-(np.linalg.norm(p.pos[:, None] - p.pos[None], axis=2) / sig_) ** 2)
                tot_ = (Kd_ * need_[None, :]).max(1) * smooth01((zmax_ - p.pos[:, 2]) / fade_); tot_[tot_ <= 1e-3] = 0.0
                nd_ = Kd_ @ fnu[tri_]; nd_ = nd_ / (np.linalg.norm(nd_, axis=1, keepdims=True) + 1e-12)
                offs_ = tot_[:, None] * nd_; mv_ = tot_ > 0
                q2 = copy.copy(p); q2.pos = p.pos.copy(); q2.pos[mv_] += offs_[mv_]; P_[nm_] = q2
                for i_, s_ in enumerate(skirts):
                    if s_.name == nm_: skirts[i_] = q2
                rec_lift(shared, variant, nm_, np.where(mv_)[0].tolist(), offs_[mv_].tolist())
                if first: log.append(f'{g}: layer clear: {nm_} pushed out over {lc_["under"]} at {int(mv_.sum())} pts by up to {tot_.max():.2f} '
                                     f'({int((need_ > 0).sum())} were closer than {clear_} below z {zmax_:.1f}, nearest {h_[need_ > 0].min():+.2f})')
    pieces = [P_[p.name] for p in pieces]
    tails = [p for p in pieces if p.role == 'tail']
    tip_v = np.unique(belt.tris[np.isin(belt.tris, np.where(blab == band)[0]).all(1)]) if has_belt else np.zeros(0, int)
    tip_v = tip_v[belt.pos[tip_v, 2] < split] if has_belt else tip_v
    if cfg.get('hangers') and has_belt:          # v10 (Officer, user: 'add smp to these leather pieces on both sides of the armor ... the leather
        # piece to just swing off the hoop'): per hip a leather strap slung between two rings that hang from loops over the belt band.
        # Pieces by texture island (decided once, on _1): rings = compact islands (every extent <= ring_ext, >= ring_min_pts) at the
        # front / back of the hip, the strap = the other islands out there below the loops (z_bottom..z_top). They leave the tip's set.
        if 'hang_sel' not in shared:
            hc = cfg['hangers']; isl_b = islands(belt.tris, len(belt.pos)); sel_ = []
            # 2026-10-13 (SoS Whiterun heavy): hangers 'sides' = the hips that carry a strap between their rings (-1 = -x, +1 = +x); the
            # other hip may carry something else between its rings (the Whiterun heavy's side bag, a piece of its own)
            for k, sgn in enumerate(tuple(hc.get('sides', (-1.0, 1.0)))):
                cands = {}
                for i_ in set(isl_b.tolist()):
                    v = np.where(isl_b == i_)[0]
                    if len(v) < hc.get('min_pts', 8): continue
                    q = belt.pos[v]; c = q.mean(0); ext = q.max(0) - q.min(0)
                    if sgn * c[0] < hc.get('x_min', 8.5) or q[:, 2].max() > hc.get('z_top', 76.0) or q[:, 2].min() < hc.get('z_bottom', 66.0): continue
                    cands[i_] = (v, q, c, ext)
                small = {i_: t for i_, t in cands.items() if (t[3] <= hc.get('ring_ext', 3.6)).all() and len(t[0]) >= hc.get('ring_min_pts', 40)}
                fr = max([i_ for i_, t in small.items() if t[2][1] > hc.get('front_y', 4.0)], key=lambda i_: len(small[i_][0]), default=None)
                bk = max([i_ for i_, t in small.items() if t[2][1] < hc.get('back_y', -7.0)], key=lambda i_: len(small[i_][0]), default=None)
                if fr is None or bk is None:
                    raise RuntimeError(f'{g}: hanger {"LR"[k]}: rings not found; islands out there: ' + ', '.join(
                        f'{i_}: {len(t[0])} pts at ({t[2][0]:.1f}, {t[2][1]:.1f}, {t[2][2]:.1f}) ext {np.round(t[3], 1).tolist()}' for i_, t in cands.items()))
                strap = np.concatenate([t[0] for i_, t in cands.items() if i_ not in (fr, bk)]) if len(cands) > 2 else np.zeros(0, int)
                if len(strap) < hc.get('strap_min_pts', 40) or belt.pos[strap, 1].max() - belt.pos[strap, 1].min() < hc.get('min_span', 10.0):
                    raise RuntimeError(f'{g}: hanger {"LR"[k]}: strap too small ({len(strap)} pts)')
                cf, cb = belt.pos[cands[fr][0]].mean(0), belt.pos[cands[bk][0]].mean(0); ax = cb - cf; ax[2] = 0.0; L_ = float(np.linalg.norm(ax)); ax = ax / L_
                s_ = np.clip(((belt.pos[strap] - cf) @ ax) / L_, 0.0, 1.0)
                sel_.append(dict(front=cands[fr][0], back=cands[bk][0], strap=strap, s=s_, n=int(hc.get('n', 3))))
                log.append(f'{g}: hanger {"LR"[k]}: front ring {len(cands[fr][0])} pts at ({cf[0]:.1f}, {cf[1]:.1f}, {cf[2]:.1f}), back ring {len(cands[bk][0])} pts at '
                           f'({cb[0]:.1f}, {cb[1]:.1f}, {cb[2]:.1f}), strap {len(strap)} pts over {L_:.1f} units ({len(cands) - 2} islands), {int(hc.get("n", 3))} bones')
            shared['hang_sel'] = sel_
        tip_v = np.setdiff1d(tip_v, np.concatenate([np.r_[h['front'], h['back'], h['strap']] for h in shared['hang_sel']]))
    # bag (v3): the biggest belt piece that is not the band; its straps = the small pieces over its top
    bag_c, bag_straps = None, []
    if Dz.get('bag') and has_belt:
        others = [k for k in range(blab.max() + 1) if k != band]
        bag_c = max(others, key=lambda k: int((blab == k).sum()))
        q = belt.pos[blab == bag_c]; lo, hi = q[:, :2].min(0) - 1.0, q[:, :2].max(0) + 1.0; btop = q[:, 2].max()
        for k in others:
            if k == bag_c: continue
            c = belt.pos[blab == k].mean(0)
            if (c[:2] >= lo).all() and (c[:2] <= hi).all() and belt.pos[blab == k, 2].max() >= btop - 3.0: bag_straps.append(k)
    bag_v = np.where(blab == bag_c)[0] if bag_c is not None else np.zeros(0, int)
    # flaps: plates = the two biggest pieces of the flaps piece (left first), straps = the rest
    if flaps is not None:
        flab = D.welded_components(flaps.pos, flaps.tris)
        psizes = sorted(range(flab.max() + 1), key=lambda k: -int((flab == k).sum()))[:2]
        plates = sorted(psizes, key=lambda k: flaps.pos[flab == k, 0].mean())         # left (-x) first
    else:
        flab, plates = None, []
    # skirt layers -> outer / inner geometry for the rig (SoS Officer v2: the extra layers 'skirt:outer@<word>' hang on rigs of their own)
    msk = [p for p in skirts if '@' not in p.role]
    layers = {p.role.split(':')[1]: (p.pos, p.tris) for p in msk}
    if first:
        rig = Rig(N, dict(cfg, force_slits=shared.get('cuts')) if shared.get('cuts') else cfg, {k: v for k, v in layers.items()}, log); shared['rig'] = rig
        rig.tip_split = split
        log.append((f'belt: band component {band}, lower edge {edge:.2f}, tip {len(tip_v)} pts below {split:.2f}; ' if has_belt else 'no belt; ')
                   + (f'flap plates (left, right) components {plates} of {flab.max() + 1}; ' if flaps is not None else 'no flaps; ')
                   + (f'bag component {bag_c} ({len(bag_v)} pts), straps {bag_straps}' if bag_c is not None else 'no bag'))
        rig.nfl, rig.has_bag = len(plates), bag_c is not None
    rig = shared['rig']
    out_p = next(p for p in skirts if p.role == 'skirt:outer')
    o_t = G.outer_mask(out_p.pos, out_p.tris, rig.cx, rig.cy)
    if shared.get('belt_lift') and len(tip_v):     # v8 (Officer): the strap RESTS on the layers under it. v7c turned it out by the whole
        # plate angle (20 deg of forward lean where it hangs over the mail below the plates, against 5 deg on the other coats); now every
        # strap point is pushed out radially until it sits TIP_CLEAR + .15 in front of EVERY triangle it projects into (within the
        # collider's catch) of every layer named in tip_under - the lifted plates, the mail, and the sash whose edge the author drew level
        # with it (user: 'the belt sits inside the sash'). Nearest-triangle heights alone missed a curled sash corner and a plate hem fold.
        tpb = belt.pos[tip_v]; want_ = TIP_CLEAR + 0.15; push_b = np.zeros(len(tpb))
        for q in [p for p in skirts + tails if p.name in Dz.get('tip_under', ())]:
            keep_ = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > max(0.3, umr(Dz, q.name)))
            if not keep_.any(): continue
            sd_ = prism_sd_min(tpb, q.pos, q.tris[keep_], lo=-TAILU_PEN, hi=3.0)
            push_b = np.maximum(push_b, np.where(np.isfinite(sd_), np.maximum(0.0, want_ - sd_), 0.0))
        Kb = np.exp(-(np.linalg.norm(tpb[:, None] - tpb[None], axis=2) / 1.5) ** 2); push_b = (Kb * push_b[None, :]).max(1)   # spread over the strap, no steps
        rad_b = np.c_[tpb[:, 0] - rig.cx, tpb[:, 1] - rig.cy, np.zeros(len(tpb))]; rad_b = rad_b / (np.linalg.norm(rad_b, axis=1, keepdims=True) + 1e-12)
        offs_b = push_b[:, None] * rad_b; mv_b = push_b > 1e-3
        if mv_b.any():
            belt.pos = belt.pos.copy(); belt.pos[tip_v[mv_b]] += offs_b[mv_b]
            rec_lift(shared, variant, belt.name, tip_v[mv_b].tolist(), offs_b[mv_b].tolist())
        log.append(f'{g}_{variant}: strap settled {want_:.2f} over the layers under it (and the sash): {int(mv_b.sum())} pts pushed out by up to {push_b.max():.2f}')
    hang_layers = [p for p in skirts + tails if p.name in Dz.get('hang_under_layers', Dz.get('tip_under', ()))]
    if shared.get('hang_sel') and hang_layers:     # v11 (user: the hangers 'go through the armor'): the straps rest TIP_CLEAR + .15 in front of the
        # layers under them (8 strap points sat up to 0.3 inside the lifted plates), settled like the belt tip; the rings stay on their loops
        # 2026-10-13 hang_settle (SoS Eastmarch guards, user: 'the side leather pieces on both are clipping through the plate. i dont think
        # you gave them proper colliders'): the copy under the hangers is pulled HANG_CLEAR (1.0) clear of every hanger point, so a strap
        # resting .55 over the plates put the copy ~.45-1.2 BEHIND the real plate - tools/hanger_plate_ride.py, the plates flared to their
        # limits, the strap skinned with them: 162 / 199 strap pts still through the plate by up to .94 with the collider pushing none.
        # hang_settle = the copy's own clearance + .15: the strap rests where the copy can lie on the plate itself
        want_ = float(Dz.get('hang_settle', TIP_CLEAR + 0.15))
        hs = np.concatenate([h['strap'] for h in shared['hang_sel']]); tpb = belt.pos[hs]; push_b = np.zeros(len(tpb))
        for q in hang_layers:
            keep_ = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > max(0.3, umr(Dz, q.name)))
            if not keep_.any(): continue
            sd_ = prism_sd_min(tpb, q.pos, q.tris[keep_], lo=-TAILU_PEN, hi=3.0)
            push_b = np.maximum(push_b, np.where(np.isfinite(sd_), np.maximum(0.0, want_ - sd_), 0.0))
        Kb = np.exp(-(np.linalg.norm(tpb[:, None] - tpb[None], axis=2) / 1.5) ** 2); push_b = (Kb * push_b[None, :]).max(1)
        rad_b = np.c_[tpb[:, 0] - rig.cx, tpb[:, 1] - rig.cy, np.zeros(len(tpb))]; rad_b = rad_b / (np.linalg.norm(rad_b, axis=1, keepdims=True) + 1e-12)
        offs_b = push_b[:, None] * rad_b; mv_b = push_b > 1e-3
        if mv_b.any():
            belt.pos = belt.pos.copy(); belt.pos[hs[mv_b]] += offs_b[mv_b]
            rec_lift(shared, variant, belt.name, hs[mv_b].tolist(), offs_b[mv_b].tolist())
        log.append(f'{g}_{variant}: hanger straps settled {want_:.2f} over the layers under them: {int(mv_b.sum())} pts pushed out by up to {push_b.max():.2f}')
        if Dz.get('hang_settle_exact'):
            # 2026-10-14 (user job 1, Whiterun hangers: 'copy behind plate 0 (within .05)'): the settle above measures along each face's
            # normal (prism) and leaves the rings where they are, but the copy is pulled until every hanger point is HANG_CLEAR away by the
            # TRUE nearest distance (edges and corners count) - Whiterun heavy _0 at hang_settle 1.3: the front ring (26 pts) and 6 strap
            # pts still pulled the copy .06 behind the plate. Here every hanger point (rings + strap) is pushed out until it is the copy's
            # clearance + .05 from the faces the copy is made of (outward, radial > hang_min_radial, |nz| < SKO_MAX_NZ), measured as the
            # pull measures it: the strap point by point (smoothed as above), each ring as ONE rigid piece (its shape on its loop kept).
            # The copy then needs no pull and lies on the plate
            ex_ = Dz.get('hang_settle_exact'); wx_ = float(cfg.get('hang_clear', HANG_CLEAR)) + (0.05 if ex_ is True else float(ex_)); FS_ = []     # True = + .05, a number = that headroom
            for q in hang_layers:
                fq_ = np.cross(q.pos[q.tris[:, 1]] - q.pos[q.tris[:, 0]], q.pos[q.tris[:, 2]] - q.pos[q.tris[:, 0]]); fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12
                k_ = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > Dz.get('hang_min_radial', HANG_MIN_RADIAL)) & (np.abs(fq_[:, 2]) < SKO_MAX_NZ)
                if k_.any(): FS_.append((q.name, q.pos, q.tris[k_]))
            parts_x = [('strap', h['strap']) for h in shared['hang_sel']] + [('ring', h[k]) for h in shared['hang_sel'] for k in ('front', 'back')]
            su_ = B.Surface(FS_) if FS_ else None; tot_ = np.zeros(len(belt.pos)); moved_ = set()
            VV_, VN_ = [], []      # + the copy pull's own first measure (K.pull_in): the height along each copy VERTEX normal of the points within its lateral reach
            for _, qp_, qt_ in FS_:
                u_ = np.unique(qt_); VV_.append(qp_[u_]); VN_.append(K.vertex_normals(qp_, qt_)[u_])
            VV_ = np.vstack(VV_) if VV_ else np.zeros((0, 3)); VN_ = np.vstack(VN_) if VN_ else np.zeros((0, 3))
            def vn_need(P_):
                if not len(VV_): return np.zeros(len(P_))
                v_ = P_[:, None, :] - VV_[None]; s_ = (v_ * VN_[None]).sum(2); la_ = np.linalg.norm(v_ - s_[..., None] * VN_[None], axis=2)
                return np.where((la_ < TIP_LAT) & (s_ > -2.0), wx_ - s_, 0.0).max(1)
            for _it in range(8):
                if su_ is None: break
                any_ = False
                for kind_, ix_ in parts_x:
                    ix_ = np.asarray(ix_); P_ = belt.pos[ix_]; _, _, dd_, _ = su_.query(P_, k=24); need_ = np.maximum(0.0, np.maximum(wx_ - dd_, vn_need(P_)))
                    if need_.max() < 1e-3: continue
                    rad_ = np.c_[P_[:, 0] - rig.cx, P_[:, 1] - rig.cy, np.zeros(len(P_))]; rad_ /= np.linalg.norm(rad_, axis=1, keepdims=True) + 1e-12
                    if kind_ == 'ring':
                        rm_ = rad_.mean(0); rm_ /= np.linalg.norm(rm_) + 1e-12; off_ = np.tile(need_.max() * rm_, (len(P_), 1))
                    else:
                        Kx_ = np.exp(-(np.linalg.norm(P_[:, None] - P_[None], axis=2) / 1.5) ** 2); off_ = (Kx_ * need_[None, :]).max(1)[:, None] * rad_
                    belt.pos = belt.pos.copy(); belt.pos[ix_] += off_; rec_lift(shared, variant, belt.name, ix_.tolist(), off_.tolist())
                    tot_[ix_] += np.linalg.norm(off_, axis=1); moved_ |= set(ix_.tolist()); any_ = True
                if not any_: break
            log.append(f'{g}_{variant}: hangers settled EXACT {wx_:.2f} from their copy faces (rings rigid): {len(moved_)} pts moved, by up to {tot_.max():.2f}')
    if Dz.get('bag_settle') and len(bag_v):
        # 2026-10-14 HOLDS (PLAN_HOLDS 5: 'the bag rests slightly inside the surface under it (Riften 8 pts / -.23, Morthal 24 / -.38) -
        # bag_settle >= .3 clear'): every bag point pushed out radially (smoothed, sigma 1.5) until it is bag_settle (+ .05) in front of the
        # drawn surfaces under it - the cuirass (flap_cuirass) and the skirt's outer faces (outward, radial > .3, |nz| < SKO_MAX_NZ) - by the
        # signed prism height (the bag's top rested INSIDE the coat at the belt line) AND the radial height the push moves along, over every
        # outward face near the bag (Morthal: the coat's turned hem at z 72.7-74.2, outside the prism faces' filter, left 8 pts .29 over it)
        bcl_ = float(Dz['bag_settle']) + 0.05; fc_ = flap_cuirass(S, T, rest, cfg, shared); bq0_ = belt.pos[bag_v].copy(); FB_, FR_ = [], []
        for q in (fc_, out_p):
            kq = 'bagset_t_' + q.name
            if kq not in shared:
                fq_ = np.cross(q.pos[q.tris[:, 1]] - q.pos[q.tris[:, 0]], q.pos[q.tris[:, 2]] - q.pos[q.tris[:, 0]]); fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12
                cq_ = q.pos[q.tris].mean(1); dq_ = np.min(np.linalg.norm(cq_[:, None, :2] - bq0_[None, :, :2], axis=2), axis=1)
                near_ = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (dq_ < 6.0) & (cq_[:, 2] > bq0_[:, 2].min() - 4.0) & (cq_[:, 2] < bq0_[:, 2].max() + 1.0)
                shared[kq] = near_ & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > 0.3) & (np.abs(fq_[:, 2]) < SKO_MAX_NZ); shared[kq + '#ray'] = near_
            if shared[kq].any(): FB_.append((q.name, q.pos, q.tris[shared[kq]], q))
            if shared[kq + '#ray'].any(): FR_.append((q.pos, q.tris[shared[kq + '#ray']], q))
        # women: measured on the base AND every BodySlide build verify simulates (the user's preset grew the coat .3-.7 into the bag:
        # Riften f .36 -> -.07, MorthalHeavy f .37 -> -.36) - the push is the largest need over them (the women's 'every weight')
        MBs_ = [None] + [Dm for _, Dm in morph_builds(shared, T)] if g == 'f' else [None]
        Kb_ = np.exp(-(np.linalg.norm(bq0_[:, None] - bq0_[None], axis=2) / 1.5) ** 2)
        rb_ = np.c_[bq0_[:, 0] - rig.cx, bq0_[:, 1] - rig.cy, np.zeros(len(bq0_))]; rb_ /= np.linalg.norm(rb_, axis=1, keepdims=True) + 1e-12
        for _it in range(4):
            pb_ = np.zeros(len(bag_v))
            for Dm_ in MBs_:
                bq_ = belt.pos[bag_v] + (0.0 if Dm_ is None else piece_disp(belt, Dm_)[bag_v])
                for _, qp_, qt_, q_ in FB_:
                    qd_ = qp_ + (0.0 if Dm_ is None else piece_disp(q_, Dm_))
                    sd_ = prism_sd_min(bq_, qd_, qt_, lo=-3.0, hi=3.0); pb_ = np.maximum(pb_, np.where(np.isfinite(sd_), np.maximum(0.0, bcl_ - sd_), 0.0))
                for qp_, qt_, q_ in FR_:
                    qd_ = qp_ + (0.0 if Dm_ is None else piece_disp(q_, Dm_))
                    hr_ = radial_height(bq_, rig.cx, rig.cy, qd_, qt_); pb_ = np.maximum(pb_, np.where(np.isfinite(hr_), np.maximum(0.0, bcl_ - hr_), 0.0))
            if pb_.max() < 1e-3: break
            pb_ = (Kb_ * pb_[None, :]).max(1); belt.pos = belt.pos.copy(); belt.pos[bag_v] += pb_[:, None] * rb_
        db_ = belt.pos[bag_v] - bq0_; mb_ = np.linalg.norm(db_, axis=1) > 1e-4
        if mb_.any(): rec_lift(shared, variant, belt.name, bag_v[mb_].tolist(), db_[mb_].tolist())
        log.append(f'{g}_{variant}: bag settled {bcl_:.2f} in front of {", ".join(n for n, _, _, _ in FB_)}' + (f' on the base + {len(MBs_) - 1} BodySlide builds' if len(MBs_) > 1 else '') + f': {int(mb_.sum())} of {len(bag_v)} pts pushed out by up to {np.linalg.norm(db_, axis=1).max():.2f}')
    if Dz.get('flap_settle') and flaps is not None and len(plates):
        # 2026-10-14 HOLDS (PLAN_HOLDS 1; user: 'For both Rift armors the side leather piece is also clipping side the armor'): the left-hip
        # strap rested up to .5 (Riften) / 1.2 (Morthal) INSIDE the cuirass at its belt ends and its hanging part over the hip had NO
        # collision points (the 'inner half by radius' rule of hip plates picks a loop's two ends: Riften 0 of 141 drawn pts at the hip).
        # Every strap point but the wrap round the belt (flap_wrap) is pushed out radially until it is flap_settle (+ .05) clear of the faces
        # its copy (Skirt Under Flap) is made of - the cuirass hem (flap_cuirass) and the skirt's outer faces - measured as the hangers'
        # exact settle: signed prism height first (points behind the surface), then the true distance and the height along each copy
        # vertex normal within TIP_LAT; smoothed (sigma 1.5) over the settled points, the wrap points stay. The copy then needs no pull.
        fcl_ = float(Dz['flap_settle']); wf_ = fcl_ + 0.05; fc_ = flap_cuirass(S, T, rest, cfg, shared)
        cxf_, cyf_ = rig.cx, rig.cy; fv_ = flap_wrap(flaps, flab, plates, belt, cxf_, cyf_, shared)
        FQ_, FQq_ = [], []
        for q in (fc_, out_p):
            kq = 'flapu_t_' + q.name
            if kq not in shared:     # decided once, on _1: outward faces near the strap (as the hangers' copy: radial > .3, |nz| < SKO_MAX_NZ)
                fq_ = np.cross(q.pos[q.tris[:, 1]] - q.pos[q.tris[:, 0]], q.pos[q.tris[:, 2]] - q.pos[q.tris[:, 0]]); fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12
                cq = q.pos[q.tris].mean(1); hq_ = flaps.pos[fv_]; dq = np.min(np.linalg.norm(cq[:, None, :2] - hq_[None, :, :2], axis=2), axis=1)
                shared[kq] = G.outer_mask(q.pos, q.tris, cxf_, cyf_) & (radial_dot(q.pos, q.tris, cxf_, cyf_) > 0.3) & (np.abs(fq_[:, 2]) < SKO_MAX_NZ) \
                    & (dq < 6.0) & (cq[:, 2] > hq_[:, 2].min() - 4.0) & (cq[:, 2] < hq_[:, 2].max() + 1.0)
            if shared[kq].any(): FQ_.append((q.name, q.pos, q.tris[shared[kq]])); FQq_.append(q)
        # women: on the base AND every BodySlide build (the copy is pulled clear on every build: a strap settled on the base alone left it
        # .13 behind the base surface - Falkreath f 44-48 copy pts, Markarth f 13); the push = the largest need over them
        MBf_ = [None] + [Dm for _, Dm in morph_builds(shared, T)] if g == 'f' else [None]
        def fdisp_(Dm_):
            return (np.zeros((len(fv_), 3)) if Dm_ is None else piece_disp(flaps, Dm_)[fv_]), [(n_, qp_ + (0.0 if Dm_ is None else piece_disp(q_, Dm_)), qt_) for (n_, qp_, qt_), q_ in zip(FQ_, FQq_)]
        if FQ_ and len(fv_):
            P0f_ = flaps.pos[fv_].copy(); push_ = np.zeros(len(fv_)); out0_ = np.zeros(len(fv_))     # out0_: the fade by the wrap still leaves no point BEHIND the drawn surface (Riften: 1 position .1 in at the belt's top)
            for Dm_ in MBf_:
                dP_, FQd_ = fdisp_(Dm_)
                for _, qp_, qt_ in FQd_:
                    sd_ = prism_sd_min(P0f_ + dP_, qp_, qt_, lo=-3.0, hi=3.0); push_ = np.maximum(push_, np.where(np.isfinite(sd_), np.maximum(0.0, wf_ - sd_), 0.0))
                    out0_ = np.maximum(out0_, np.where(np.isfinite(sd_), np.maximum(0.0, 0.05 - sd_), 0.0))
            Kf_ = np.exp(-(np.linalg.norm(P0f_[:, None] - P0f_[None], axis=2) / 1.5) ** 2); fd_ = shared['flap_fade']; push_ = np.maximum((Kf_ * push_[None, :]).max(1) * fd_, out0_)
            radf_ = np.c_[P0f_[:, 0] - cxf_, P0f_[:, 1] - cyf_, np.zeros(len(P0f_))]; radf_ /= np.linalg.norm(radf_, axis=1, keepdims=True) + 1e-12
            flaps.pos = flaps.pos.copy(); flaps.pos[fv_] += push_[:, None] * radf_
            SB_ = []
            for Dm_ in MBf_:
                dP_, FQd_ = fdisp_(Dm_)
                SB_.append((dP_, B.Surface(FQd_), np.vstack([qp_[np.unique(qt_)] for _, qp_, qt_ in FQd_]), np.vstack([K.vertex_normals(qp_, qt_)[np.unique(qt_)] for _, qp_, qt_ in FQd_])))
            for _it in range(8):
                need_ = np.zeros(len(fv_))
                for dP_, su_, VV_, VN_ in SB_:
                    P_ = flaps.pos[fv_] + dP_; _, _, dd_, _ = su_.query(P_, k=24)
                    v_ = P_[:, None, :] - VV_[None]; s_ = (v_ * VN_[None]).sum(2); la_ = np.linalg.norm(v_ - s_[..., None] * VN_[None], axis=2)
                    need_ = np.maximum(need_, np.maximum(0.0, np.maximum(wf_ - dd_, np.where((la_ < TIP_LAT) & (s_ > -2.0), wf_ - s_, 0.0).max(1))))
                if need_.max() < 1e-3: break
                need_ = need_ * (fd_ >= 1.0)      # only the collision points need the clearance; the fade keeps its share of the push
                if need_.max() < 1e-3: break
                nd_ = (Kf_ * need_[None, :]).max(1) * fd_; flaps.pos = flaps.pos.copy(); flaps.pos[fv_] += nd_[:, None] * radf_
            offf_ = flaps.pos[fv_] - P0f_; mvf_ = np.linalg.norm(offf_, axis=1) > 1e-4
            if mvf_.any(): rec_lift(shared, variant, flaps.name, fv_[mvf_].tolist(), offf_[mvf_].tolist())
            log.append(f'{g}_{variant}: hip strap settled EXACT {wf_:.2f} from its copy faces ({", ".join(n for n, _, _ in FQ_)})' + (f' on the base + {len(MBf_) - 1} BodySlide builds' if len(MBf_) > 1 else '') + f': {int(mvf_.sum())} of {len(fv_)} pts moved, '
                       f'by up to {np.linalg.norm(offf_, axis=1).max():.2f}; {shared["flap_wrapn"]} wrap pts (behind the belt) stay, {int((fd_ < 1.0).sum())} fade in over 2.0 from them')
    if Dz.get('tip_plumb') and len(tip_v):       # v6 (Officer, user: 'the belt looks crooked'): the author drew the strap leaning 6.5 deg
        # sideways (x) in the front view; a hanging strap is plumb. Shear its points so every chain row's centre keeps the top row's x
        # (the forward lean that lies on the flaring skirt stays); recorded as a lift so verify can undo it. Rows from the _1 build.
        tp0 = belt.pos[tip_v]; rows_z = rig.tip_rows if not first else list(np.linspace(split, float(tp0[:, 2].min()) + 0.6, TIP_N + 1))
        cxs = []
        for z in rows_z:
            w_ = np.exp(-((tp0[:, 2] - z) / 1.0) ** 2) + 1e-12; cxs.append(float((w_ * tp0[:, 0]).sum() / w_.sum()))
        xline = np.interp(tp0[:, 2], rows_z[::-1], cxs[::-1]); dx = cxs[0] - xline
        offs = np.c_[dx, np.zeros(len(dx)), np.zeros(len(dx))]
        # the shear must not carry the strap INTO the surface it hangs over (heavy guard: 5 resting contacts on the front-left plate):
        # every point keeps its drawn height over the union of the layers under it, pushed back out along the surface normal
        und_ = [p for p in skirts if p.name in Dz.get('tip_under', (next(p for p in skirts if p.role == 'skirt:outer').name,))]
        UPp = np.vstack([q.pos for q in und_]); uo_ = np.cumsum([0] + [len(q.pos) for q in und_])
        UTt = np.vstack([q.tris[G.outer_mask(q.pos, q.tris, rig.cx, rig.cy)] + uo_[j] for j, q in enumerate(und_)])
        fnu = np.cross(UPp[UTt[:, 1]] - UPp[UTt[:, 0]], UPp[UTt[:, 2]] - UPp[UTt[:, 0]]); fnu = fnu / (np.linalg.norm(fnu, axis=1, keepdims=True) + 1e-12)
        usurf = B.Surface([('u', UPp, UTt)])
        tri0, _, d0, cp0 = usurf.query(tp0, k=8); h0 = ((tp0 - cp0) * fnu[tri0]).sum(1)
        q1 = tp0 + offs; tri1, _, d1, cp1 = usurf.query(q1, k=8); h1 = ((q1 - cp1) * fnu[tri1]).sum(1)
        lat1 = np.sqrt(np.maximum(d1 ** 2 - h1 ** 2, 0.0)); push = np.where(lat1 < 1.5, np.maximum(0.0, h0 - h1), 0.0)
        offs = offs + push[:, None] * fnu[tri1]; mv = np.linalg.norm(offs, axis=1) > 1e-4
        belt.pos = belt.pos.copy(); belt.pos[tip_v[mv]] += offs[mv]
        rec_lift(shared, variant, belt.name, tip_v[mv].tolist(), offs[mv].tolist())
        log.append(f'{g}_{variant}: strap plumbed: {int(mv.sum())} pts sheared by up to {np.abs(dx).max():.2f} (the drawn chain leaned {cxs[-1] - cxs[0]:+.2f} in x); '
                   f'{int((push > 1e-3).sum())} pts pushed back out over the skirt by up to {push.max():.2f}')
    if Dz.get('tip_settle') and Dz.get('tip_under') and len(tip_v):
        # 2026-10-14 (user job, Eastmarch belt tips: 'the tip settled >= 1.0 over the DRAWN plates at every weight with its copy ON the
        # plate (tip_settle like hang_settle)'; Fable: the tip rested .36 / .47 over the plates and its copy lay 1.0 / .5 behind them):
        # hang_settle_exact for the tip - every hanging tip point (below the split; the band stays on the belt) pushed out, smoothed, until
        # the copy pull's two measures (true nearest distance; height along each copy vertex normal within TIP_LAT) read the copy
        # clearance + tip_settle headroom against the faces the tip's copy is made of, so that copy needs no pull and lies on the plates
        ex_ = Dz.get('tip_settle'); wt_ = float(cfg.get('hang_clear', HANG_CLEAR)) + (0.05 if ex_ is True else float(ex_)); FS_, FSq_ = [], []
        for q in [p for p in skirts + tails if p.name in Dz['tip_under']]:
            fq_ = np.cross(q.pos[q.tris[:, 1]] - q.pos[q.tris[:, 0]], q.pos[q.tris[:, 2]] - q.pos[q.tris[:, 0]]); fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12
            # tip_max_nz (2026-10-14, Eastmarch light, tools/tip_clip_faces.py): tip riding + settled, every tip pt still through a plate at .5 of
            # its limits (30, max .38) met the plates' rolled hem at the inner corner, faces at nz -.63 / -.65, just past SKO_MAX_NZ .6 (the
            # Officer's sash-edge rule): the tip copy (tip_under selection) and this settle take faces to tip_max_nz; the settle keeps the tip clear
            k_ = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (np.abs(fq_[:, 2]) < Dz.get('tip_max_nz', SKO_MAX_NZ)) & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > umr_tip(Dz, q.name))
            if k_.any(): FS_.append((q.name, q.pos, q.tris[k_])); FSq_.append(q)
        tv_ = tip_v[belt.pos[tip_v, 2] < split]; FTR_ = []
        if Dz.get('tip_sel_at') == 'author': shared['tip_sel_belt'] = belt.pos.copy()      # 2026-10-14: see tip_sel_at below
        if Dz.get('tip_settle_cuirass') and len(tv_):     # 2026-10-14 HOLDS (Riften): the tip's top rows hang over the CUIRASS hem, not the skirt (.94 over
            fc_ = flap_cuirass(S, T, rest, cfg, shared); tq_ = belt.pos[tv_]     # it at z 73.8): its outward faces near the tip join the settle (decided on _1)
            if 'tipc_t' not in shared:
                fq_ = np.cross(fc_.pos[fc_.tris[:, 1]] - fc_.pos[fc_.tris[:, 0]], fc_.pos[fc_.tris[:, 2]] - fc_.pos[fc_.tris[:, 0]]); fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12
                cq_ = fc_.pos[fc_.tris].mean(1); dq_ = np.min(np.linalg.norm(cq_[:, None, :2] - tq_[None, :, :2], axis=2), axis=1)
                shared['tipc_t'] = G.outer_mask(fc_.pos, fc_.tris, rig.cx, rig.cy) & (np.abs(fq_[:, 2]) < Dz.get('tip_max_nz', SKO_MAX_NZ)) & (radial_dot(fc_.pos, fc_.tris, rig.cx, rig.cy) > 0.3) \
                    & (dq_ < 6.0) & (cq_[:, 2] > tq_[:, 2].min() - 4.0) & (cq_[:, 2] < tq_[:, 2].max() + 1.0)
            if shared['tipc_t'].any(): FS_.append((fc_.name, fc_.pos, fc_.tris[shared['tipc_t']])); FSq_.append(fc_)
            # + the RADIAL height (the push's own direction) over every outward cuirass face near the tip: the women's Morthal tip top hung .31 over
            # the coat's turned hem (z 73-74), faces outside the filter above (the bag_settle refinement)
            if 'tipc_t#ray' not in shared:
                cq_ = fc_.pos[fc_.tris].mean(1); dq_ = np.min(np.linalg.norm(cq_[:, None, :2] - tq_[None, :, :2], axis=2), axis=1)
                shared['tipc_t#ray'] = G.outer_mask(fc_.pos, fc_.tris, rig.cx, rig.cy) & (dq_ < 6.0) & (cq_[:, 2] > tq_[:, 2].min() - 4.0) & (cq_[:, 2] < tq_[:, 2].max() + 1.0)
            if shared['tipc_t#ray'].any(): FTR_.append((fc_.pos, fc_.tris[shared['tipc_t#ray']], fc_))
        if FS_ and len(tv_):
            su_ = B.Surface(FS_); VV_ = np.vstack([qp_[np.unique(qt_)] for _, qp_, qt_ in FS_]); VN_ = np.vstack([K.vertex_normals(qp_, qt_)[np.unique(qt_)] for _, qp_, qt_ in FS_])
            TB_ = []
            for _, Dm_ in (morph_builds(shared, T) if g == 'f' else []):
                FSd_ = [(n_, qp_ + piece_disp(q_, Dm_), qt_) for (n_, qp_, qt_), q_ in zip(FS_, FSq_)]
                TB_.append((piece_disp(belt, Dm_)[tv_], FSd_, B.Surface(FSd_), np.vstack([qp_[np.unique(qt_)] for _, qp_, qt_ in FSd_]),
                            np.vstack([K.vertex_normals(qp_, qt_)[np.unique(qt_)] for _, qp_, qt_ in FSd_]), [(qp_ + piece_disp(q_, Dm_), qt_) for qp_, qt_, q_ in FTR_]))
            tot_ = np.zeros(len(tv_)); P00_ = belt.pos[tv_].copy()
            # 2026-10-14 tip_sel_at (job 'the Whiterun rig everywhere'): the hip strap's skirt copy (sko_t) is chosen near the tip points too, so a
            # tip settled farther out changed ANOTHER piece's collider (Markarth: Skirt Outer 564 -> 563 tris, piece_regress FAIL 'Flap'). With
            # tip_sel_at = h the settle first runs to HANG_CLEAR + h with the old measures (the previous install's tip) and that tip chooses the
            # selection; then it goes on to the design's own target ('author' = the tip as drawn chooses it)
            sel_ = Dz.get('tip_sel_at'); phases_ = ([(float(cfg.get('hang_clear', HANG_CLEAR)) + float(sel_), False)] if isinstance(sel_, (int, float)) and not isinstance(sel_, bool) else []) + [(wt_, True)]
            wt_final_ = wt_
            for ph_i_, (wt_, prism_on_) in enumerate(phases_):
              for _it in range(8):
                  P_ = belt.pos[tv_]; _, _, dd_, _ = su_.query(P_, k=24)
                  v_ = P_[:, None, :] - VV_[None]; s_ = (v_ * VN_[None]).sum(2); la_ = np.linalg.norm(v_ - s_[..., None] * VN_[None], axis=2)
                  need_ = np.maximum(0.0, np.maximum(wt_ - dd_, np.where((la_ < TIP_LAT) & (s_ > -2.0), wt_ - s_, 0.0).max(1)))
                  # 2026-10-14 (Falkreath, Whiterun-rig job): + the exact signed height over each face it projects into (the women's builds
                  # had it; the base did not): over a big skirt face whose corners lie past TIP_LAT both measures above missed it (2 pts
                  # stayed 1.44-1.48 under a 1.65 target; the copy's own check read 1.47)
                  for _, qp_, qt_ in (FS_ if prism_on_ else []):
                      sd_ = prism_sd_min(P_, qp_, qt_, lo=-3.0, hi=3.0); need_ = np.maximum(need_, np.where(np.isfinite(sd_), np.maximum(0.0, wt_ - sd_), 0.0))
                  for qp_, qt_, _ in FTR_:
                      hr_ = radial_height(P_, rig.cx, rig.cy, qp_, qt_); need_ = np.maximum(need_, np.where(np.isfinite(hr_), np.maximum(0.0, wt_ - hr_), 0.0))
                  for dP_, FSd_, su2_, VV2_, VN2_, FTd_ in TB_:     # women: every BodySlide build too (Chainmail f: the mail grew out under the tip on
                      Pb_ = P_ + dP_; _, _, dd2_, _ = su2_.query(Pb_, k=24)     # the user's preset - its copy was pulled to the 2.0 cap, 1.36 behind the mail)
                      v2_ = Pb_[:, None, :] - VV2_[None]; s2_ = (v2_ * VN2_[None]).sum(2); la2_ = np.linalg.norm(v2_ - s2_[..., None] * VN2_[None], axis=2)
                      need_ = np.maximum(need_, np.maximum(0.0, np.maximum(wt_ - dd2_, np.where((la2_ < TIP_LAT) & (s2_ > -2.0), wt_ - s2_, 0.0).max(1))))
                      for _, qp2_, qt2_ in FSd_:      # signed: on a build the surface can pass the tip (unsigned distance reads that as clear)
                          sd2_ = prism_sd_min(Pb_, qp2_, qt2_, lo=-3.0, hi=3.0); need_ = np.maximum(need_, np.where(np.isfinite(sd2_), np.maximum(0.0, wt_ - sd2_), 0.0))
                      for qp2_, qt2_ in FTd_:
                          hr_ = radial_height(Pb_, rig.cx, rig.cy, qp2_, qt2_); need_ = np.maximum(need_, np.where(np.isfinite(hr_), np.maximum(0.0, wt_ - hr_), 0.0))
                  if need_.max() < 1e-3: break
                  Kx_ = np.exp(-(np.linalg.norm(P_[:, None] - P_[None], axis=2) / 1.5) ** 2); nd_ = (Kx_ * need_[None, :]).max(1)
                  rad_ = np.c_[P_[:, 0] - rig.cx, P_[:, 1] - rig.cy, np.zeros(len(P_))]; rad_ /= np.linalg.norm(rad_, axis=1, keepdims=True) + 1e-12
                  off_ = nd_[:, None] * rad_; belt.pos = belt.pos.copy(); belt.pos[tv_] += off_
                  rec_lift(shared, variant, belt.name, tv_.tolist(), off_.tolist()); tot_ += nd_
              if not prism_on_: shared['tip_sel_belt'] = belt.pos.copy()
            wt_ = wt_final_
            # the band above the split did not move: carry the tip's move into it, fading to 0 over 2.0 (GuardHeavy first build: 4 edges
            # across the split seam stretched 1.5-2.7x - .23 -> .63)
            dv_ = belt.pos[tv_] - P00_; ot_ = np.setdiff1d(np.arange(len(belt.pos)), tip_v)
            if len(ot_) and np.abs(dv_).max() > 1e-4:
                dn_ = np.linalg.norm(belt.pos[ot_][:, None] - P00_[None], axis=2); j_ = dn_.argmin(1); r_ = dn_[np.arange(len(ot_)), j_]
                fd_ = np.clip(1.0 - r_ / 2.0, 0.0, 1.0) ** 2; nb_ = fd_ > 1e-3
                if nb_.any():
                    ob_ = dv_[j_[nb_]] * fd_[nb_, None]; belt.pos = belt.pos.copy(); belt.pos[ot_[nb_]] += ob_
                    rec_lift(shared, variant, belt.name, ot_[nb_].tolist(), ob_.tolist())
                log.append(f'{g}_{variant}:   the band carries it over 2.0 above the split: {int(nb_.sum())} pts, by up to {np.linalg.norm(dv_, axis=1).max():.2f} at the seam')
            log.append(f'{g}_{variant}: belt tip settled EXACT {wt_:.2f} from its copy faces ({", ".join(n for n, _, _ in FS_)})' + (f' on the base + {len(TB_)} BodySlide builds' if TB_ else '') + f': {int((tot_ > 1e-3).sum())} pts moved, by up to {tot_.max():.2f}')
    if first:
        allP = np.vstack([p.pos for p in msk]); off = np.cumsum([0] + [len(p.pos) for p in msk])
        rig.place(allP, np.arange(len(allP)), np.unique(out_p.tris[o_t]) + off[msk.index(out_p)], log)
        # tip chain + flap bones
        tp = belt.pos[tip_v]; rig.tip_bottom = float(tp[:, 2].min()) if len(tp) else None
        rig.tip_rows = list(np.linspace(split, rig.tip_bottom + 0.6, TIP_N + 1)) if len(tp) else []
        for r, z in enumerate(rig.tip_rows):
            w = np.exp(-((tp[:, 2] - z) / 1.0) ** 2) + 1e-12; c = (w[:, None] * tp).sum(0) / w.sum()
            gm = np.eye(4); gm[:3, :3] = frame(rig.ang(c)); gm[:3, 3] = [c[0], c[1], z]
            rig.G[N.tip(r)] = gm; rig.parent[N.tip(r)] = PELV if r == 0 else N.tip(r - 1)
        rig.hangers = shared.get('hang_sel', [])      # v10: hip hangers - front anchor (0, kinematic, at the front ring's top), front ring (1),
        for k, hg in enumerate(rig.hangers):          # strap bones (2..n+1 along it), back anchor (n+2, kinematic), back ring (n+3, hangs from it)
            n_ = hg['n']; qf, qb, qs = belt.pos[hg['front']], belt.pos[hg['back']], belt.pos[hg['strap']]
            cf, cb = qf.mean(0), qb.mean(0); tf = qf[qf[:, 2] > qf[:, 2].max() - 0.6].mean(0); tb = qb[qb[:, 2] > qb[:, 2].max() - 0.6].mean(0)
            nodes_ = [(0, tf, PELV), (1, cf, N.hang(k, 0))]
            for j in range(n_):
                sj = (j + 1) / (n_ + 1); m_ = np.abs(hg['s'] - sj) < 0.5 / (n_ + 1)
                nodes_.append((2 + j, qs[m_].mean(0) if m_.sum() >= 2 else cf + (cb - cf) * sj, N.hang(k, 1 + j)))
            nodes_ += [(n_ + 2, tb, PELV), (n_ + 3, cb, N.hang(k, n_ + 2))]
            for j, c, par in nodes_:
                gm = np.eye(4); gm[:3, :3] = frame(rig.ang(c)); gm[:3, 3] = c
                rig.G[N.hang(k, j)] = gm; rig.parent[N.hang(k, j)] = par
            log.append(f'hanger {"LR"[k]} bones: anchors ({tf[0]:.1f}, {tf[1]:.1f}, {tf[2]:.1f}) / ({tb[0]:.1f}, {tb[1]:.1f}, {tb[2]:.1f}), strap at ' +
                       ', '.join(f'({c[0]:.1f}, {c[1]:.1f}, {c[2]:.1f})' for j, c, par in nodes_[2:2 + n_]))
        for k, c_ in enumerate(plates):
            q = flaps.pos[flab == c_]; c1 = q.mean(0); top = q[q[:, 2] > q[:, 2].max() - 1.0].mean(0)
            for r, c in ((0, top), (1, c1)):
                gm = np.eye(4); gm[:3, :3] = frame(rig.ang(c1)); gm[:3, 3] = c
                rig.G[N.flap(k, r)] = gm; rig.parent[N.flap(k, r)] = PELV if r == 0 else N.flap(k, 0)
        if bag_c is not None:
            q = belt.pos[bag_v]; c1 = q.mean(0); top = q[q[:, 2] > q[:, 2].max() - 1.5].mean(0)
            for r, c in ((0, top), (1, c1)):
                gm = np.eye(4); gm[:3, :3] = frame(rig.ang(c1)); gm[:3, 3] = c
                rig.G[N.bag(r)] = gm; rig.parent[N.bag(r)] = PELV if r == 0 else N.bag(0)
            log.append(f'bag hinge ({top[0]:.1f}, {top[1]:.1f}, {top[2]:.1f}) body ({c1[0]:.1f}, {c1[1]:.1f}, {c1[2]:.1f})')
        log.append(f'tip rows ' + '/'.join(f'{z:.1f}' for z in rig.tip_rows) + '; flap hinges ' +
                   ', '.join(f'({rig.G[N.flap(k, 0)][0, 3]:.1f},{rig.G[N.flap(k, 0)][1, 3]:.1f},{rig.G[N.flap(k, 0)][2, 3]:.1f})' for k in range(len(plates))))
        # SoS: tail chains (the sash end) - hinged at the piece's top, SASH_N bones down to its lowest point, frames like the tip's
        rig.tails, rig.tailu = {}, {}
        for tp_ in tails:
            key = tp_.name; q = tp_.pos; top_, bot_ = float(q[:, 2].max()), float(q[:, 2].min())
            # v7 (Officer): a sash end SEWN to the plates along its sides hangs free only below cfg 'tail_top' - the chain starts there
            # (sash_n bones); above it the cloth rides the layers it is sewn to (tail_hang_on), so the gap it fills never shows
            top_ = min(top_, float(cfg.get('tail_top', Dz.get('tail_top', 1e9)))); n_ = int(cfg.get('sash_n', Dz.get('sash_n', SASH_N)))
            rigid_ = cfg.get('tail_rigid', Dz.get('tail_rigid', False)); rigid_ = bool(rigid_) and (rigid_ is True or key in rigid_)
            if rigid_:
                # 2026-10-13 (PLAN_BAGS.md; user: the bags 'stretch and bend weirdly ... doesn't look realisitc'): a bag / pouch is ONE rigid
                # body - one bone below its hang line (tail_hang_z, default its top - 1.0: the strap / loops above it hang it from the belt),
                # hinged at its top (row 0, top - 0.3, as before) and the body bone at the body's centre of mass (a rigid body's bone sits
                # where its mass is - not at its bottom + 0.6). The sash-end recipe (hinge share 0 at the top -> 0.85 at the bottom, a thigh
                # share) bent and stretched it with every step: 30-206 % worst-edge strain over the clips / its swing (tools/bag_strain.py)
                hz_ = float(cfg.get('tail_hang_z', Dz.get('tail_hang_z', top_ - 1.0)))
                # tail_hang_islands (source texture island ids): the loops a bag hangs by (the Whiterun heavy's side bag: round its two rings,
                # z 69-74 beside the body's own top band at 73.7 - no height line separates them) blend from the belt at their top to the
                # bag's bone at their bottom (they bend like the straps they are); every other point below the line is the rigid body
                sl_ = islands(S[tp_.src].tris, len(S[tp_.src].pos)) if tp_.src in S else None
                n0_ = tp_.n0 or len(q); lab_ = np.full(len(q), -1)
                if sl_ is not None:
                    lab_[:n0_] = sl_[tp_.src_idx[:n0_]]
                    for j_, (a_, b_) in enumerate(tp_.mids): lab_[n0_ + j_] = lab_[a_]
                loop_ = np.isin(lab_, list(cfg.get('tail_hang_islands', Dz.get('tail_hang_islands', ())))) & (lab_ >= 0)
                body_ = (q[:, 2] < hz_) & ~loop_
                bt_ = tp_.tris[body_[tp_.tris].all(1)]
                ar_ = np.linalg.norm(np.cross(q[bt_[:, 1]] - q[bt_[:, 0]], q[bt_[:, 2]] - q[bt_[:, 0]]), axis=1) / 2
                com_ = (q[bt_].mean(1) * ar_[:, None]).sum(0) / max(float(ar_.sum()), 1e-9) if len(bt_) else q[body_].mean(0)
                loop_s = {}                       # loop point -> its share on the bag bone (0 at the loops' top, 1 at their bottom: one ramp for all)
                if loop_.any():
                    zt_, zb_ = float(q[loop_, 2].max()), float(q[loop_, 2].min())
                    for i_ in np.where(loop_)[0]: loop_s[int(i_)] = float(smooth01((zt_ - q[i_, 2]) / max(zt_ - zb_, 1e-3)))
                n_ = 1; rows_ = [top_ - 0.3, float(com_[2])]
            else:
                rows_ = [float(x) for x in np.linspace(top_ - 0.3, bot_ + 0.6, n_ + 1)]
            for r, z in enumerate(rows_):
                wz = np.exp(-((q[:, 2] - z) / 1.0) ** 2) + 1e-12; c = (wz[:, None] * q).sum(0) / wz.sum()
                if rigid_ and r == 1: c = com_
                gm = np.eye(4); gm[:3, :3] = frame(rig.ang(c)); gm[:3, 3] = [c[0], c[1], z]
                rig.G[N.tail(key, r)] = gm; rig.parent[N.tail(key, r)] = PELV if r == 0 else N.tail(key, r - 1)
            rig.tails[key] = dict(rows=rows_, top=top_, bottom=bot_, n=n_, root=PELV)
            if rigid_:
                rig.tails[key].update(hang_z=hz_, rigid=[int(i) for i in np.where(body_)[0]], com=[float(x) for x in com_],
                                      loops={str(k_): v_ for k_, v_ in loop_s.items()})
            log.append(f'tail {key}: {len(q)} pts z {bot_:.1f}..{top_:.1f}, rows ' + '/'.join(f'{z:.1f}' for z in rows_)
                       + (f'; RIGID below z {hz_:.1f} ({len(rig.tails[key]["rigid"])} pts on {N.tail(key, 1)} at its centre of mass '
                          f'({com_[0]:.1f}, {com_[1]:.1f}, {com_[2]:.1f}); {len(loop_s)} loop pts in {len(np.unique(lab_[loop_]))} islands blend belt -> bag' if rigid_ else ''))
        # ---- weights
        # v2: how freely each part of the skirt hangs = the gap between its lining (innermost layer, inward side) and the
        # trousers; skirt lying on the thighs moves like them (no collision needed, it cannot be left behind a leg).
        # Both fields live on the lining and are looked up for every skirt point by angle + height, so all layers agree.
        # v2b: the OUTER layer decides (it is what shows and what meets the legs; inner layers are covered by it and
        # ride the same chains - the men's cloth even sits partly inside the trousers at rest, hidden under the mail)
        tr = trousers(pants_of(S, cfg), shared, log)
        lv_ = lining_src(out_p, rig, cfg.get('lining_all', False)); LPp = out_p.pos[lv_]
        if cfg.get('field_src') == 'outer':      # v5 (Officer): the lining rides the sheet - the free-share field reads the sheet alone
            lv_ = np.intersect1d(lv_, np.unique(out_p.tris[G.outer_mask(out_p.pos, out_p.tris, rig.cx, rig.cy)])); LPp = out_p.pos[lv_]
        legw_l, gap_l = D.trouser_follow(tr, LPp)
        legw_l = smooth_field(LPp, [thighs_only(x) for x in legw_l], LEG_SIGMA)
        gn, gf = cfg.get('gap', Dz.get('gap', (GAP_NEAR, GAP_FAR)))         # v5: per-gender override (different skirt shapes)
        free_l = np.minimum(cfg.get('free_max', Dz.get('free_max', FREE_MAX)), smooth_scalar(LPp, smooth01((np.asarray(gap_l) - gn) / (gf - gn)), FREE_SIGMA))
        if cfg.get('side_follow'):      # SoS Heavy v3 (user: 'twitches a little bit standing still'): a knee-length hem's SIDES lie
            # by the knees, which move out ~5 units at the hem in a knees-apart idle stance (idle_check: 95 / 166 points pressed every
            # frame, the short coats 14-66) - there the skirt follows the thighs more (free capped), so a stance carries it along
            sf = cfg['side_follow']; a_l = np.abs(wrap(np.degrees(np.arctan2(LPp[:, 0] - rig.cx, LPp[:, 1] - rig.cy))))
            sw = smooth01((sf['half'] + sf['fade'] - np.abs(a_l - 90.0)) / sf['fade']) * smooth01((sf['ztop'] - LPp[:, 2]) / sf['zfade'])
            f0 = free_l.copy(); free_l = f0 * (1 - sw) + np.minimum(f0, sf['free']) * sw
            log.append(f'{g}: side follow - free share capped at {sf["free"]} within {sf["half"]} deg of the sides below z {sf["ztop"]} '
                       f'({int((sw > 0.5).sum())} lining pts; free there was median {np.median(f0[sw > 0.5]) if (sw > 0.5).any() else 0:.2f})')
        for fz in cfg.get('follow_zones', []):      # v10 (Officer, user: 'something blue through the chainmail when I walk or run'): the trousers
            # show through the hem FRONT until the mail catches up with a stride (the game's clips: 144-291 point-frames 5+ units deep at
            # z 43-56) - more leg follow in that sector of the hem, as side_follow does by the knees
            a_f = wrap(np.degrees(np.arctan2(LPp[:, 0] - rig.cx, LPp[:, 1] - rig.cy)) - fz['centre'])
            sw = smooth01((fz['half'] + fz['fade'] - np.abs(a_f)) / fz['fade']) * smooth01((fz['ztop'] - LPp[:, 2]) / fz['zfade'])
            f0 = free_l.copy(); free_l = f0 * (1 - sw) + np.minimum(f0, fz['free']) * sw
            log.append(f'{g}: follow zone at {fz["centre"]:.0f} deg - free share capped at {fz["free"]} within {fz["half"]} deg below z {fz["ztop"]} '
                       f'({int((sw > 0.5).sum())} pts; free there was median {np.median(f0[sw > 0.5]) if (sw > 0.5).any() else 0:.2f})')

        def cyl_of(r_):
            def cyl_(P):
                th = np.arctan2(P[:, 0] - r_.cx, P[:, 1] - r_.cy)
                return np.c_[14.0 * np.sin(th), 14.0 * np.cos(th), P[:, 2]]
            return cyl_
        cyl = cyl_of(rig)
        LC = cyl(LPp)
        log.append(f'{g}: lining to the trousers at rest: p10 {np.percentile(gap_l, 10):.2f} median {np.median(gap_l):.2f}; '
                   f'free share p10 {np.percentile(free_l, 10):.2f} median {np.median(free_l):.2f}')
        W = {}; share = {}
        # v3b: points on the cut where a skirt piece leaves its source shape keep the source's own weights, fading in
        rest_pts = {}
        for src_name, m in rest.items():
            if src_name in cfg['drop']: continue          # v23: a dropped leftover (Elite Wolf's hidden crotch fans) holds nothing to stay attached to
            t_ = S[src_name]; rest_pts[src_name] = {tuple(x) for x in np.round(t_.pos[np.unique(t_.tris[m])], 4)}

        def weigh(p, rig_, cfg_, legw_, free_, LC_, cyl_, sides=None):
            ln = p.role.split(':')[1].split('@')[0]; ws, sh = [], np.zeros(len(p.pos))
            PC = cyl_(p.pos)
            seam_pts = np.array([x for x in p.pos if tuple(np.round(x, 4)) in rest_pts.get(p.src, set())]).reshape(-1, 3)
            if len(seam_pts):
                sd = np.array([np.linalg.norm(seam_pts - x, axis=1).min() for x in p.pos]); seam_f = smooth01(sd / SEAM_FADE)
                log.append(f'{g}: {p.name} is cut out of {p.src}: {len(seam_pts)} seam points (z {seam_pts[:, 2].min():.1f}..{seam_pts[:, 2].max():.1f}) keep its weights, physics fading in over {SEAM_FADE}')
            else:
                seam_f = np.ones(len(p.pos))
            nn = np.array([int(np.argmin(((LC_ - c) ** 2).sum(1))) for c in PC])
            fi_ = cfg_.get('field_interp')       # v9 (Officer): the swing share / leg follow read at the NEAREST source vertex gave the
            if fi_:                              # hem band's vertices 45% or 76% free by which of two author's rows (4.3 apart) was
                fr_i = np.zeros(len(PC)); lw_i = []      # nearer - the band stretched, and its lining read the other row: interpolated
                for s0 in range(0, len(PC), 256):        # (gaussian, sigma fi_ in cylinder units) the field is continuous over the cloth
                    d2 = ((PC[s0:s0 + 256, None, :] - LC_[None, :, :]) ** 2).sum(2); wk = np.exp(-d2 / float(fi_) ** 2); wk[d2 > (3.0 * float(fi_)) ** 2] = 0.0
                    tot = wk.sum(1)
                    for r_ in range(len(wk)):
                        i_ = s0 + r_
                        if tot[r_] <= 1e-9: fr_i[i_] = free_[nn[i_]]; lw_i.append(legw_[nn[i_]]); continue
                        fr_i[i_] = float(wk[r_] @ free_) / tot[r_]; acc = defaultdict(float)
                        for j in np.where(wk[r_] > 1e-4 * tot[r_])[0]:
                            for b, x in legw_[j].items(): acc[b] += wk[r_, j] * x / tot[r_]
                        lw_i.append(dict(acc))
            for i in range(len(p.pos)):
                a = rig_.ang(p.pos[i])
                lw = D.smooth_lr(lw_i[i] if fi_ else legw_[nn[i]], a, rig_)
                fr = float(fr_i[i]) if fi_ else float(free_[nn[i]])
                if cfg_.get('crotch_follow'):     # v6: the skirt's front / back centre at crotch height follows both thighs
                    a_ = rig_.ang(p.pos[i]); off_ = min(abs(float(wrap(a_))), abs(float(wrap(a_ - 180.0)))); z_ = float(p.pos[i, 2]); top_ = cfg_['sk_belt']
                    cw = float(smooth01((25.0 - off_) / 10.0)) * float(smooth01((top_ - 4.0 - z_) / 3.0)) * float(smooth01((z_ - (top_ - 16.0)) / 3.0))
                    fr *= 1.0 - cfg_['crotch_follow'] * cw
                sd_ = (int(cut_side[p.name][i]) or None) if p.name in cut_side else ((int(sides[i]) or None) if sides is not None else None)
                w, s = skirt_w(rig_, cfg_, p.pos[i], p.ow[i], ln, free=fr, legw=lw, seam=float(seam_f[i]), side=sd_)
                a = rig_.ang(p.pos[i]); mid = min(abs(float(wrap(a))), abs(float(wrap(a - 180.0)))) < 20
                ws.append(cap4(N, w, keep_body=mid, pelv_min=cfg_.get('cap_pelvis_min', 0.0))); sh[i] = s
            W[p.name], share[p.name] = ws, sh
        for p in msk:
            weigh(p, rig, cfg, legw_l, free_l, LC, cyl)
        # SoS Officer v2: the extra layers, each on its own rig placed on its own pieces, its free share / leg follow from its own
        # lining's gap to the trousers (cfg 'groups' {word: options overriding cfg: sk_belt, sk_anchor, ramp, nrow, slits /
        # force_slits, free_max, gap, lining_all, legs})
        rigs = {}
        for gw_, gc_ in cfg.get('groups', {}).items():
            gp = [p for p in skirts if p.role == 'skirt:outer@' + gw_]; gcfg = dict(cfg, **gc_)
            r_ = Rig(GroupNames(N, gw_), gcfg, {'outer': (gp[0].pos, gp[0].tris)}, log)
            gP = np.vstack([p.pos for p in gp])
            r_.place(gP, np.arange(len(gP)), np.arange(len(gP)), log)     # bones at the layer's own surface (both faces)
            glv = lining_src(gp[0], r_, gc_.get('lining_all', False)); GLP = gp[0].pos[glv]
            gleg, ggap = D.trouser_follow(tr, GLP)
            gleg = smooth_field(GLP, [thighs_only(x) for x in gleg], LEG_SIGMA)
            gn_, gf_ = gc_.get('gap', (GAP_NEAR, GAP_FAR))
            gfree = np.minimum(gc_.get('free_max', FREE_MAX), smooth_scalar(GLP, smooth01((np.asarray(ggap) - gn_) / (gf_ - gn_)), FREE_SIGMA))
            if gc_.get('side_follow'):      # (as the main skirt's: the hem sides by the knees follow the thighs more)
                sf = gc_['side_follow']; a_g = np.abs(wrap(np.degrees(np.arctan2(GLP[:, 0] - r_.cx, GLP[:, 1] - r_.cy))))
                sw = smooth01((sf['half'] + sf['fade'] - np.abs(a_g - 90.0)) / sf['fade']) * smooth01((sf['ztop'] - GLP[:, 2]) / sf['zfade'])
                gfree = gfree * (1 - sw) + np.minimum(gfree, sf['free']) * sw
            gcyl = cyl_of(r_)
            log.append(f'{g}: layer {gw_} ({", ".join(p.name for p in gp)}): its lining to the trousers p10 {np.percentile(ggap, 10):.2f} median '
                       f'{np.median(ggap):.2f}; free share p10 {np.percentile(gfree, 10):.2f} median {np.median(gfree):.2f}')
            for p in gp:
                weigh(p, r_, gcfg, gleg, gfree, gcyl(GLP), gcyl, sides=seam_sides(p, r_))
            rigs[gw_] = r_
        shared['rigs'] = rigs
        for nm_, rd in cfg.get('ride', {}).items():      # SoS Officer v2: a layer sewn to the one over it rides it near the seam
            pr, po = next(p for p in skirts if p.name == nm_), next(p for p in skirts if p.name == rd['on'])
            W[nm_], rr_ = ride_weights(pr, W[nm_], po, W[po.name], rig, rd, N, log)
            share[nm_] = share[nm_] * (1 - rr_)          # riding points carry the other layer's bones: not this layer's collision points
        if cfg.get('lining_ride'):      # v9 (Officer, user: 'the embroidered pattern disappears when moving' / 'the pattern is now on the
            # inside'): the author's lining lies 0.5-1 behind the sheet, and weighed as separate points the two ended with different
            # bones - the 4-bone cap at the centre (3 body bones kept) left ONE chain bone, which one flipping with z (the sheet's vertex
            # at 45.5 held row 5, the lining's at 45.7 row 4), the sides read the swing share from different author's rows (55% vs 23%
            # thigh) - and crossed by up to 0.9 (chains swinging) / 2.1 (a thigh raised). A hidden lining has no motion of its own:
            # every lining point that projects onto the sheet takes the sheet's capped weights at that spot - the same bones, the same
            # motion. (names, or True = the outer sheet)
            lr_ = cfg['lining_ride']
            for nm_ in (lr_ if isinstance(lr_, (list, tuple)) else (out_p.name,)):
                p_ = next(p for p in skirts if p.name == nm_)
                ot_ = p_.tris[G.outer_mask(p_.pos, p_.tris, rig.cx, rig.cy)]; ov_ = np.unique(ot_); iv_ = np.setdiff1d(np.unique(p_.tris), ov_)
                if not len(iv_) or not len(ot_): continue
                rm_ = np.full(len(p_.pos), -1); rm_[ov_] = np.arange(len(ov_)); s_ = B.Surface([('o', p_.pos[ov_], rm_[ot_])])
                fn_ = np.cross(p_.pos[ot_[:, 1]] - p_.pos[ot_[:, 0]], p_.pos[ot_[:, 2]] - p_.pos[ot_[:, 0]]); fn_ = fn_ / (np.linalg.norm(fn_, axis=1, keepdims=True) + 1e-12)
                tri_, _, d_, cp_ = s_.query(p_.pos[iv_], k=8); h_ = ((p_.pos[iv_] - cp_) * fn_[tri_]).sum(1); lat_ = np.sqrt(np.maximum(d_ ** 2 - h_ ** 2, 0.0))
                on_ = (lat_ < 1.0) & (h_ > -6.0) & (h_ < 1.0)
                under_, _ = blend_under(s_, rm_[ot_], [W[nm_][i] for i in ov_], p_.pos[iv_[on_]])
                for i, u in zip(iv_[on_], under_):
                    a = rig.ang(p_.pos[i]); mid = min(abs(float(wrap(a))), abs(float(wrap(a - 180.0)))) < 20
                    W[nm_][i] = cap4(N, u, keep_body=mid, pelv_min=cfg.get('cap_pelvis_min', 0.0))
                log.append(f'{g}: {nm_} lining rides the sheet: {int(on_.sum())} of {len(iv_)} lining pts (z {p_.pos[iv_[on_], 2].min():.1f}..{p_.pos[iv_[on_], 2].max():.1f}) '
                           f'take the sheet\'s weights at their spot; {int((~on_).sum())} project onto no sheet and keep their own')
        # surfaces of the skirt's outer layer (outward triangles) for riding / colliders
        ov = np.unique(out_p.tris[o_t]); rmo = np.full(len(out_p.pos), -1); rmo[ov] = np.arange(len(ov))
        so_surf = B.Surface([('o', out_p.pos[ov], rmo[out_p.tris[o_t]])])
        # flaps (v2): every plate point follows the skirt right under it by FLAP_FOLLOW and its own hinged bone by the
        # rest; straps fade from the belt (top) to the plate point nearest them (bottom)
        fw = [fold(x) for x in flaps.ow] if flaps is not None else []
        for k, c_ in enumerate(plates):
            v = np.where(flab == c_)[0]
            under, _ = blend_under(so_surf, out_p.tris[o_t], W[out_p.name], flaps.pos[v])
            zt_, zb_ = float(flaps.pos[v, 2].max()), float(flaps.pos[v, 2].min())
            for i, u in zip(v, under):
                ff = Dz.get('flap_follow', FLAP_FOLLOW)          # SoS: per design (the bouncy left-hip strap rides less)
                if Dz.get('flap_end_fade'):                      # v12: a loop fixed to the belt at both ends - its own share fades to nothing at the top (the ends), full at the sag
                    ff = 1.0 - (1.0 - ff) * float(np.clip((zt_ - flaps.pos[i, 2]) / max(zt_ - zb_, 1e-6), 0.0, 1.0)) ** Dz['flap_end_fade']
                pw = defaultdict(float); pw[N.flap(k, 1)] += 1 - ff
                for b, x in cap4(N, u).items(): pw[b] += ff * x
                fw[i] = cap4(N, dict(pw), keep=(N.flap(k, 1),))      # v3c: the plate's own small share is never dropped
        plv = np.where(np.isin(flab, plates))[0] if flaps is not None else []
        for c_ in (range(flab.max() + 1) if flaps is not None else []):
            if c_ in plates: continue
            v = np.where(flab == c_)[0]; q = flaps.pos[v]
            k = int(np.argmin([np.linalg.norm(q.mean(0)[:2] - flaps.pos[flab == pc, :2].mean(0)) for pc in plates]))
            zt, zb = q[:, 2].max(), q[:, 2].min()
            for i in v:
                s = float(smooth01((zt - flaps.pos[i, 2]) / max(zt - zb, 1e-3)))
                j = plv[int(np.argmin(np.linalg.norm(flaps.pos[plv] - flaps.pos[i], axis=1)))]
                w = defaultdict(float)
                for b, x in fold(flaps.ow[i]).items(): w[b] += (1 - s) * x
                for b, x in fw[j].items(): w[b] += s * x
                fw[i] = cap4(N, dict(w))
        if flaps is not None: W[flaps.name] = fw
        # belt: band folded; tip on its chain, riding the surface under it (skirt outer or a flap plate)
        btw = [fold(x) for x in belt.ow]; own = np.zeros(len(belt.pos))
        if len(tip_v) and Dz.get('tip_under'):   # SoS Officer v2: the strap hangs over other layers (the sash end in the tasset layer)
            uq = [next(p for p in skirts if p.name == nm_) for nm_ in Dz['tip_under'] if any(p.name == nm_ for p in skirts)]; uo = np.cumsum([0] + [len(q.pos) for q in uq])   # v8: skirt layers (a tail named here joins the collider only)
            UT = np.vstack([q.tris[G.outer_mask(q.pos, q.tris, rig.cx, rig.cy)] + uo[j] for j, q in enumerate(uq)])
            u1, d1 = blend_under(B.Surface([('u', np.vstack([q.pos for q in uq]), UT)]), UT, [x for q in uq for x in W[q.name]], belt.pos[tip_v])
        elif len(tip_v):
            u1, d1 = blend_under(so_surf, out_p.tris[o_t], W[out_p.name], belt.pos[tip_v])
        else:
            u1, d1 = [], np.zeros(0)
        if flaps is not None and len(tip_v):
            pl_tris = flaps.tris[np.isin(flab[flaps.tris], plates).all(1)]
            pv = np.unique(pl_tris); rmp = np.full(len(flaps.pos), -1); rmp[pv] = np.arange(len(pv))
            fl_surf = B.Surface([('f', flaps.pos[pv], rmp[pl_tris])])
            u2, d2 = blend_under(fl_surf, pl_tris, fw, belt.pos[tip_v])
        else:
            u2, d2 = u1, np.full(len(tip_v), 1e9)
        if cfg.get('tip_hang_on', Dz.get('tip_hang_on')) == 'skirt' and len(tip_v):   # 2026-10-13 (SoS Heavy): as tail_hang_on='skirt' -
            a_t = float(rig.ang(belt.pos[tip_v].mean(0))); k_t = int(np.argmin([abs(float(wrap(a - a_t))) for a in rig.ang_k]))   # the strap's
            rig.tip_hang = N.sk(k_t, 1)       # first joint on the first swinging bone of the main skirt chain nearest it; weights unchanged
            log.append(f'{g}: belt tip hangs from {rig.tip_hang} (skirt chain at {rig.ang_k[k_t]:.0f} deg, the strap at {a_t:.0f}); weights unchanged')
        for j, i in enumerate(tip_v):
            under = u2[j] if d2[j] < d1[j] else u1[j]
            z = float(belt.pos[i, 2]); o = float(smooth01((split - z) / Dz.get('tip_blend', TIP_BLEND)))      # tip_blend (2026-10-14): per design, so a strip starting close under its split gets the reference belt's top-band share
            chain = defaultdict(float)
            for r, t in row_bracket(rig.tip_rows, z): chain[PELV if r == 0 else N.tip(r)] += t
            ride = cfg.get('tip_ride', Dz.get('tip_ride', TIP_RIDE)) * (1.0 if cfg.get('tip_ride_flat', Dz.get('tip_ride_flat', TIP_RIDE_FLAT)) else float(smooth01((split - z) / (split - rig.tip_bottom))))
            w = defaultdict(float)
            # v14: the strap takes the LEG share of the skirt under it (the part the thighs carry), so a step moves both
            # together - only the swing is left to the collider (v12 straps were pushed onto it every stride)
            tlf = Dz.get('tip_leg_follow', TIP_LEG_FOLLOW)      # Officer v4: 0 - the strap hangs on its chain alone (its surface no longer follows the thighs)
            legs_u = {b: x for b, x in under.items() if R.is_skel(b) and any(k in b for k in ('Thigh', 'Calf', 'Foot'))} if tlf else {}
            ls = tlf * sum(legs_u.values())
            # 2026-10-14 (job 'the Whiterun rig everywhere': the Whiterun light front belt, the user's reference, takes .08-.13 on the thigh;
            # Falkreath's skirt under its tip carries .26-.28 thigh share up high, so tip_leg_follow 1 put the strap .37 / .72 on its own bones
            # in the top bands): tip_leg_cap = the most leg share a tip point takes; the rest goes to its OWN chain (never the skirt)
            lc_ = Dz.get('tip_leg_cap')
            if lc_ is not None and ls > lc_:
                legs_u = {b: x * lc_ / ls for b, x in legs_u.items()}; ls = float(lc_)
            for b, x in fold(belt.ow[i]).items(): w[b] += (1 - o) * x
            for b, x in chain.items(): w[b] += o * (1 - ride) * (1 - ls) * x
            for b, x in legs_u.items(): w[b] += o * (1 - ride) * tlf * x
            for b, x in under.items(): w[b] += o * ride * x
            btw[i] = cap4(N, dict(w)); own[i] = o
        # bag (v3): the author's bag weights where it has them (men), else BAG_SHARE on its own bone; straps fade from the
        # belt (top) to the bag point nearest them (bottom)
        if bag_c is not None:
            for i in bag_v:
                aw = belt.ow[i]
                if aw.get('Bolsa 1', 0) > 0:
                    w = defaultdict(float)
                    for b, x in aw.items(): w[N.bag(1) if b == 'Bolsa 1' else (b if R.is_skel(b) else PELV)] += x
                else:
                    bs_ = Dz.get('bag_share', BAG_SHARE)         # SoS: per design ('reactive' bags hang more on their own hinge)
                    w = defaultdict(float); w[N.bag(1)] += bs_
                    for b, x in fold(aw).items(): w[b] += (1 - bs_) * x
                btw[i] = cap4(N, dict(w))
            for k in bag_straps:
                v = np.where(blab == k)[0]; zt, zb = belt.pos[v, 2].max(), belt.pos[v, 2].min()
                for i in v:
                    aw = belt.ow[i]
                    if aw.get('Bolsa 1', 0) > 0:
                        w = defaultdict(float)
                        for b, x in aw.items(): w[N.bag(1) if b == 'Bolsa 1' else (b if R.is_skel(b) else PELV)] += x
                    else:
                        s_ = float(smooth01((zt - belt.pos[i, 2]) / max(zt - zb, 1e-3)))
                        j = bag_v[int(np.argmin(np.linalg.norm(belt.pos[bag_v] - belt.pos[i], axis=1)))]
                        w = defaultdict(float)
                        for b, x in fold(aw).items(): w[b] += (1 - s_) * x
                        for b, x in btw[j].items(): w[b] += s_ * x
                    btw[i] = cap4(N, dict(w))
        for k, hg in enumerate(getattr(rig, 'hangers', [])):     # v10: the rings on their ring bones, the strap bracketed ring to ring
            n_ = hg['n']; nodes_ = [N.hang(k, 1)] + [N.hang(k, 2 + j) for j in range(n_)] + [N.hang(k, n_ + 3)]; ss = list(np.linspace(0.0, 1.0, n_ + 2))
            for i in hg['front']: btw[i] = {N.hang(k, 1): 1.0}
            for i in hg['back']: btw[i] = {N.hang(k, n_ + 3): 1.0}
            for i, s in zip(hg['strap'], hg['s']):
                w = defaultdict(float)
                for a, t in lin_bracket(ss, float(s)): w[nodes_[a]] += t
                btw[i] = dict(w)
        hf_ = float(Dz.get('hang_follow', 0.0))
        if hf_ > 0 and getattr(rig, 'hangers', []):
            # 2026-10-13 (SoS Eastmarch heavy, user: 'the side leather pieces are floating on its own and acting out. jittering'): v10 put
            # every hanger point wholly on its own ring / strap bones - a closed loop of light bodies between two kinematic anchors, drawn
            # with nothing of the plate it lies on, so its every twitch showed and a plate swinging out under it left it 'floating'. The
            # Stormcloak hip strap loop (also fixed to the belt at both ends, confirmed calm) rides the skirt under it by STRAP_FOLLOW
            # and keeps the rest on its own hinge: here each hanger point takes hang_follow of the layers under it (hang_under_layers,
            # their outer faces) and the rest of its v10 weights
            uq_ = [p for p in skirts if p.name in Dz.get('hang_under_layers', Dz.get('tip_under', ()))]
            uo_ = np.cumsum([0] + [len(q.pos) for q in uq_])
            UT_h = np.vstack([q.tris[G.outer_mask(q.pos, q.tris, rig.cx, rig.cy)] + uo_[j] for j, q in enumerate(uq_)])
            hv_ = np.concatenate([np.r_[hg['front'], hg['back'], hg['strap']] for hg in rig.hangers])
            uh_, _ = blend_under(B.Surface([('u', np.vstack([q.pos for q in uq_]), UT_h)]), UT_h, [x for q in uq_ for x in W[q.name]], belt.pos[hv_])
            for i, u in zip(hv_, uh_):
                own_ = btw[i]; w = defaultdict(float)
                for b, x in own_.items(): w[b] += (1.0 - hf_) * x
                for b, x in cap4(N, u).items(): w[b] += hf_ * x
                btw[i] = cap4(N, dict(w), keep=tuple(own_))
            log.append(f'{g}: hip hangers ride the layers under them ({", ".join(q.name for q in uq_)}) by {hf_:.2f} ({len(hv_)} pts)')
        tf_ = float(Dz.get('tip_follow', 0.0))
        if tf_ > 0 and len(tip_v):
            # 2026-10-14 (user job, Eastmarch belt tips; Fable tools/tip_plate_ride.py: the tip had NO ride share on the Tasset chains, so the
            # plates overtook it as soon as they swung - light .25 of their limits: 120 tip pts inside a plate, the collider pushing 16 - 'the
            # crotch magnet'): as hang_follow, each tip point takes tip_follow of the layers under it (tip_under, outer faces) - scaled by its
            # own share o (the band above the split stays on the belt) - and keeps the rest of its weights
            uq_ = [p for p in skirts if p.name in Dz.get('tip_under', ())]
            uo_ = np.cumsum([0] + [len(q.pos) for q in uq_])
            UT_t = np.vstack([q.tris[G.outer_mask(q.pos, q.tris, rig.cx, rig.cy)] + uo_[j] for j, q in enumerate(uq_)])
            ut_, _ = blend_under(B.Surface([('u', np.vstack([q.pos for q in uq_]), UT_t)]), UT_t, [x for q in uq_ for x in W[q.name]], belt.pos[tip_v])
            for i, u in zip(tip_v, ut_):
                s_ = tf_ * float(own[i]); own_ = btw[i]; w = defaultdict(float)
                if s_ <= 0: continue
                for b, x in own_.items(): w[b] += (1.0 - s_) * x
                for b, x in cap4(N, u).items(): w[b] += s_ * x
                # keep only the tip's OWN chain bones (every tip point already carries 4 influences - chain + thighs + pelvis: keeping them
                # all folded the plate share away, first build: Tasset share median 0.00); the rest compete with the plates' bones
                btw[i] = cap4(N, dict(w), keep=tuple(b for b in own_ if 'BeltTip' in b or b == getattr(rig, 'tip_hang', None)))
            log.append(f'{g}: belt tip rides the layers under it ({", ".join(q.name for q in uq_)}) by {tf_:.2f} x its own share ({len(tip_v)} pts)')
        if has_belt: W[belt.name] = btw
        # SoS: tails - their own chain below a short blend from the top, plus the LEG share of the skirt under them (RA v14: a
        # step moves both together, only the swing is left to the collider); never riding the skirt's own bones
        own_t = {}
        for tp_ in tails:
            key = tp_.name; tr_ = rig.tails[key]
            if Dz.get('tail_under'):    # v3 (Officer): the sash hangs over the tasset layer AND the mail - its leg share comes from both (like tip_under)
                uq_ = [next(p for p in skirts if p.name == nm_) for nm_ in Dz['tail_under']]; uo_ = np.cumsum([0] + [len(q.pos) for q in uq_])
                UT_u = np.vstack([q.tris[G.outer_mask(q.pos, q.tris, rig.cx, rig.cy)] + uo_[j] for j, q in enumerate(uq_)])
                under_t, _ = blend_under(B.Surface([('u', np.vstack([q.pos for q in uq_]), UT_u)]), UT_u, [x for q in uq_ for x in W[q.name]], tp_.pos)
            else:
                under_t, _ = blend_under(so_surf, out_p.tris[o_t], W[out_p.name], tp_.pos)
            hang_on = cfg.get('tail_hang_on', Dz.get('tail_hang_on'))
            if hang_on == 'skirt':    # 2026-10-13 (SoS Heavy, 'the sash and the belt keep getting stuck around the crotch'): a kinematic thigh
                # drives the skirt past its joint limits (tools/leg_flare.py, the game's run: front chains 1.1-1.6 x their limits, sprint
                # 2-3.2 x), so a sash end hung from the pelvis is overtaken however far it may swing. Its first joint hangs from the first
                # swinging bone of the MAIN skirt chain nearest it instead: the skirt carries it. Only the joint moves - the weights stay
                # (its top is sewn to the waist, not to the skirt), so the root stays the pelvis for skinning.
                a_s = float(rig.ang(tp_.pos.mean(0))); k_ = int(np.argmin([abs(float(wrap(a - a_s))) for a in rig.ang_k]))
                tt_ = cfg.get('tail_top', Dz.get('tail_top'))
                if tt_ is None:
                    tr_['hang'] = N.sk(k_, 1); hang_on = None
                    log.append(f'{g}: tail {key} hangs from {tr_["hang"]} (skirt chain at {rig.ang_k[k_]:.0f} deg, the sash at {a_s:.0f}); weights unchanged')
                else:     # 2026-10-13 (SoS Riften light, user: 'copy what we did for the officer and only have the bottom half below the plates
                    # have smp to keep the hole from showing'): the Officer v7 recipe on the MAIN skirt - above tail_top the sash is sewn to the
                    # plates (rides the skirt surface under it, row 0 included), its free chain hangs from the skirt bone at that height
                    rz_ = rig.rows[k_]; r_ = min(range(1, len(rz_)), key=lambda r: (rz_[r] < tt_ - 0.5, abs(rz_[r] - tt_)))
                    tr_['hang'] = N.sk(k_, r_); tr_['sewn'] = True; hang_on = None
                    log.append(f'{g}: tail {key} sewn to the skirt above z {tt_:.1f}; its free chain hangs from {tr_["hang"]} (skirt chain at '
                               f'{rig.ang_k[k_]:.0f} deg, row at z {rz_[r_]:.1f}; the sash at {a_s:.0f})')
            if hang_on:        # v7: the free chain hangs from the lowest bone of that layer's chain nearest the sash (a physics body, so the
                rg_ = shared['rigs'][hang_on]; GN_ = GroupNames(N, hang_on)      # sewn cloth above and the free end below move together)
                a_s = float(rig.ang(tp_.pos.mean(0))); k_ = int(np.argmin([abs(float(wrap(a - a_s))) for a in rg_.ang_k]))
                tr_['root'] = GN_.sk(k_, rg_.nrow)
                log.append(f'{g}: tail {key} hangs from {tr_["root"]} ({hang_on} chain at {rg_.ang_k[k_]:.0f} deg, the sash at {a_s:.0f}); above z {tr_["top"]:.1f} it rides the layers it is sewn to')
            root_ = tr_.get('root', PELV)
            tw, ow_ = [], np.zeros(len(tp_.pos))
            rig_set = set(tr_.get('rigid', ())); loops_ = {int(k_): v_ for k_, v_ in tr_.get('loops', {}).items()}
            if 'rigid' in tr_:        # 2026-10-13 tail_rigid: the body = 1.0 on its one bone (no sewn blend, no leg share - the thighs are
                for i in range(len(tp_.pos)):   # the collider's job, as for a plate); the strap above the hang line keeps the belt's weights,
                    if i in rig_set: tw.append({N.tail(key, 1): 1.0}); ow_[i] = 1.0; continue      # a loop blends belt (top) -> bag (bottom)
                    w = defaultdict(float); s_ = loops_.get(i, 0.0)
                    for b, x in (under_t[i] if hang_on else fold(tp_.ow[i])).items(): w[b] += (1.0 - s_) * x
                    if s_ > 0: w[N.tail(key, 1)] += s_
                    tw.append(cap4(N, dict(w)))
                W[tp_.name] = tw; own_t[key] = ow_
                log.append(f'{g}: tail {key} RIGID: {len(rig_set)} pts 1.0 on {N.tail(key, 1)}; {len(loops_)} loop pts blend belt -> bag; '
                           f'{len(tp_.pos) - len(rig_set) - len(loops_)} above z {tr_["hang_z"]:.1f} on the belt\'s weights')
                continue
            sewn_ = bool(tr_.get('sewn'))          # 2026-10-13 tail_hang_on='skirt' + tail_top: sewn above it, the top row too, on the skirt under it
            for i in range(len(tp_.pos)):
                z = float(tp_.pos[i, 2]); o = float(smooth01((tr_['top'] - z) / SASH_BLEND))
                chain = defaultdict(float)
                for r, t in row_bracket(tr_['rows'], z):
                    if r == 0 and sewn_:
                        for b, x in under_t[i].items(): chain[b] += t * x
                    else: chain[root_ if r == 0 else N.tail(key, r)] += t
                tlf = Dz.get('tip_leg_follow', TIP_LEG_FOLLOW)
                legs_u = {b: x for b, x in under_t[i].items() if R.is_skel(b) and any(k in b for k in ('Thigh', 'Calf', 'Foot'))} if tlf else {}
                ls = tlf * sum(legs_u.values())
                w = defaultdict(float)
                for b, x in (under_t[i] if (hang_on or sewn_) else fold(tp_.ow[i])).items(): w[b] += (1 - o) * x     # v7: sewn part = the surface under it
                for b, x in chain.items(): w[b] += o * (1 - ls) * x
                for b, x in legs_u.items(): w[b] += o * tlf * x
                tw.append(cap4(N, dict(w))); ow_[i] = o
            W[tp_.name] = tw; own_t[key] = ow_
        shared.update(W=W, share=share, own=own, plates=plates, flab=flab, tip_v=tip_v, own_t=own_t)
        log.append(f'{g}: skirt ' + ', '.join(f'{p.name} {len(p.pos)} pts ({int((share[p.name] > 0.01).sum())} move)' for p in skirts) +
                   (f'; flaps {len(flaps.pos)} pts' if flaps is not None else '') + f'; tip {len(tip_v)} pts' + (f'; bag {len(bag_v)} pts' if bag_c is not None else ''))
    W, share, own = shared['W'], shared['share'], shared['own']
    own_t = shared['own_t']
    plates, flab, tip_v = shared['plates'], shared['flab'], shared['tip_v']
    for p in pieces:
        if p.name in W and len(W[p.name]) != len(p.pos): raise RuntimeError(f'{g}_{variant} {p.name}: split differs from _1')
    # ---- colliders
    pants = pants_of(S, cfg)
    trousers(pants, shared, log)
    kz_ = 'leg_tri_sel'          # v5 (Officer, cfg leg_max_nz): no up / down-facing trouser faces - a knee bulge rising into the hem can only
    if kz_ not in shared or not cfg.get('leg_max_nz'):      # push it OUT, never up (a hanging chain cannot move up); decided once, on _1
        sel_ = pants.pos[pants.tris].mean(1)[:, 2] > LEG_ZMIN
        if cfg.get('leg_max_nz'):
            fn_ = np.cross(pants.pos[pants.tris[:, 1]] - pants.pos[pants.tris[:, 0]], pants.pos[pants.tris[:, 2]] - pants.pos[pants.tris[:, 0]])
            fn_ = fn_ / (np.linalg.norm(fn_, axis=1, keepdims=True) + 1e-12); sel_ &= np.abs(fn_[:, 2]) < cfg['leg_max_nz']
        shared[kz_] = sel_
    pt = pants.tris[shared[kz_]]
    if shared['flip']: pt = pt[:, [0, 2, 1]]
    if copy_frac(Dz, cfg, 'legs'):          # 2026-10-13 PERF (PLAN_PERF_WHITERUN.md 2): the leg colliders at collider resolution - the trousers'
        ckl_ = ('coarse_legs', len(pants.pos))  # selected (outward-wound) faces clustered once, on _1 (rule 6); the pull, the lining keep and the
        if ckl_ not in shared: shared[ckl_] = coarsen(pants.pos, pt, copy_frac(Dz, cfg, 'legs'))   # Front / Back / Side split all read it
        pt = shared[ckl_]
    lv = np.unique(pt); rml = np.full(len(pants.pos), -1); rml[lv] = np.arange(len(lv)); LT = rml[pt]
    # lining = inward-facing points of every skirt layer that physics moves
    # lining (v2b): the outer layer's inward side (or all of it when it is a single sheet), where physics moves it
    if 'lin_it' not in shared:                    # decided once, on _1 (by position the thin _0 picked other triangles)
        it = ~G.outer_mask(out_p.pos, out_p.tris, rig.cx, rig.cy)
        shared['lin_it'] = np.ones(len(out_p.tris), bool) if cfg.get('lining_all') else (it if it.mean() >= 0.05 else np.ones(len(out_p.tris), bool))
    it = shared['lin_it']
    v = lining_src(out_p, rig, cfg.get('lining_all', False)); v = v[share[out_p.name][v] > PMIN_C]
    lin = [(out_p, it, v)]
    glin = []           # SoS Officer v2: every extra layer meets the legs with its own lining (its own collider shapes)
    for gw_, gc_ in cfg.get('groups', {}).items():
        if not gc_.get('legs', True): continue
        gp0 = next(p for p in skirts if p.role == 'skirt:outer@' + gw_); rg = shared['rigs'][gw_]; kk = 'lin_it_' + gw_
        if kk not in shared:
            it_ = ~G.outer_mask(gp0.pos, gp0.tris, rg.cx, rg.cy)
            shared[kk] = np.ones(len(gp0.tris), bool) if gc_.get('lining_all') else (it_ if it_.mean() >= 0.05 else np.ones(len(gp0.tris), bool))
        if 'glin_v_' + gw_ not in shared:          # decided once, on _1 (every hidden copy has the same points in _0 and _1)
            gv = lining_src(gp0, rg, gc_.get('lining_all', False)); gv = gv[share[gp0.name][gv] > PMIN_C]
            # only points resting clear of the trousers (the blue lining at the hips lies ON the thighs and rides them): the main
            # skirt's leg colliders are never pulled in for an extra layer (v2 first build: 226 leg points pulled in up to 1.9)
            gg_ = D.trouser_follow(trousers(pants, shared, log), gp0.pos[gv])[1]
            shared['glin_v_' + gw_] = gv[np.asarray(gg_) >= gc_.get('leg_gap', LEG_CLEAR)]
        glin.append((gp0, shared[kk], shared['glin_v_' + gw_], gw_, rg))
    LIN = np.vstack([p.pos[v] for p, it, v in lin])      # (the extra layers' points never pull the legs in: they are chosen clear of them)
    if cfg.get('leg_pull_min_gap') is not None:      # v5 (Officer): lining points inside the trousers (a hidden lining) never pull the legs in
        g_ = np.asarray(D.trouser_follow(trousers(pants, shared, log), LIN)[1]); LIN = LIN[g_ >= cfg['leg_pull_min_gap']]
    lk = f'loff_{len(pants.pos)}'               # v6: per trousers mesh
    if g == 'v': lk += '_' + variant            # vanilla women: per weight (the thin _0 skirt rests closer to its legs)
    if lk not in shared:
        # 2026-10-13 cfg 'leg_pull' (default LEG_CLEAR .8): the lining's rest clearance over the leg colliders (SoS Pale heavy women: the user's
        # preset at full weight left 1 front lining point 0.49 off the legs at .8 - the Eastmarch heavy women's layer collider .8 -> 1.0 the same way)
        _, loff = K.pull_in(pants.pos[lv], LT, LIN, cfg.get('leg_pull', LEG_CLEAR), LEG_MAXIN); shared[lk] = loff
    shared['loff'] = shared[lk]
    LP = pants.pos[lv] - shared['loff'][:, None] * K.vertex_normals(pants.pos[lv], LT)
    if first:
        keep = {}
        for p, it, v in lin + [(p, it, v) for p, it, v, _, _ in glin]:
            _, _, gap, _ = B.Surface([('l', LP, LT)]).query(p.pos[v], k=8); ok_ = gap >= cfg.get('lining_min_gap', LINING_MIN_GAP)   # v5: per design (a hidden lining on the trousers)
            if cfg.get('leg_pull_min_gap') is not None:      # v6: that distance is unsigned - a hidden lining INSIDE the trousers by more than the gap is not a collision point either
                ok_ &= np.asarray(D.trouser_follow(trousers(pants, shared, log), p.pos[v])[1]) >= cfg.get('lining_min_gap', LINING_MIN_GAP)
            keep[p.name] = v[ok_]
        shared['lin_keep'] = keep
        log.append(f'{g}: legs collider pulled in at {int((shared["loff"] > 0.01).sum())} of {len(lv)} pts (max {shared["loff"].max():.2f}); lining points ' +
                   ', '.join(f'{p.name} {len(keep[p.name])}/{len(v)}' for p, it, v in lin + [(p, it, v) for p, it, v, _, _ in glin]) +
                   ''.join(f'; {p.name} lining z {p.pos[keep[p.name], 2].min():.1f}..{p.pos[keep[p.name], 2].max():.1f}' for p, it, v in lin + [(p, it, v) for p, it, v, _, _ in glin]
                           if glin and len(keep[p.name])))
    keep = shared['lin_keep']
    # flap points (inner side of the plates), bag points (inner half) and tip points
    # (vanilla women: decided once, on _1 - the median split by radius picked different points on the thin _0 body, and every
    # hidden copy must have the same points in _0 and _1)
    if 'flv' not in shared:
        inner_fl = []
        for k, c_ in enumerate(plates):
            v = np.where(flab == c_)[0]; r_ = np.hypot(flaps.pos[v, 0] - rig.cx, flaps.pos[v, 1] - rig.cy)
            inner_fl.append(v[r_ <= np.median(r_)])
        shared['flv'] = np.concatenate(inner_fl) if inner_fl else np.zeros(0, int)
        if Dz.get('flap_settle') and 'flap_free' in shared:     # 2026-10-14 HOLDS: a hip STRAP (a loop) - every settled point, the part hanging over
            shared['flv'] = np.asarray(shared['flap_coll'])       # the hip included (the plates' inner half was its two ends at the belt); not the fade by the wrap
        if len(bag_v):
            br = np.hypot(belt.pos[bag_v, 0] - rig.cx, belt.pos[bag_v, 1] - rig.cy); shared['bagv'] = bag_v[br <= np.median(br)]
        else:
            shared['bagv'] = np.zeros(0, int)
    FLV, BAGV = shared['flv'], shared['bagv']
    if len(tip_v) and cfg.get('tip_lift', Dz.get('tip_lift', True)):
        tv = tip_v[own[tip_v] > 0.2]; tp = belt.pos[tv]
        tt = out_p.tris[o_t]; fno = np.cross(out_p.pos[tt[:, 1]] - out_p.pos[tt[:, 0]], out_p.pos[tt[:, 2]] - out_p.pos[tt[:, 0]])
        fno /= np.linalg.norm(fno, axis=1, keepdims=True) + 1e-12
        tri_, _, dist_, cp_ = B.Surface([('o', out_p.pos, tt)]).query(tp, k=8); sd_ = ((tp - cp_) * fno[tri_]).sum(1)
        lat_ = np.sqrt(np.maximum(dist_ ** 2 - sd_ ** 2, 0.0))
        need = np.where((lat_ < 0.3) & (sd_ > -2.5), np.maximum(0.0, TIP_LIFT - sd_), 0.0)
        if need.max() > 1e-4:
            Kd = np.exp(-(np.linalg.norm(tp[:, None] - tp[None], axis=2) / TIP_LIFT_SIGMA) ** 2)
            Lf = (Kd * need[None, :]).max(1) * smooth01((own[tv] - 0.2) / 0.5)
            nd = Kd @ fno[tri_]; nd /= np.linalg.norm(nd, axis=1, keepdims=True) + 1e-12
            offs = np.round(Lf[:, None] * nd, 6); mv = Lf > 1e-4          # rounded = exactly what the report records
            belt.pos = belt.pos.copy(); belt.pos[tv[mv]] += offs[mv]
            rec_lift(shared, variant, belt.name, tv[mv].tolist(), offs[mv].tolist())   # v19: keeps the outer's leg_clear lift
            log.append(f'{g}_{variant}: tail lifted onto the skirt at {int(mv.sum())} of {len(tv)} pts (needed max {need.max():.2f}, '
                       f'{int((need > 0).sum())} pts; moved max {Lf.max():.2f})')
    TIPV = tip_v[own[tip_v] > 0.2]
    FLP_ = flaps.pos[FLV] if flaps is not None else np.zeros((0, 3)); FLP_W = [W[flaps.name][i] for i in FLV] if flaps is not None and flaps.name in W else []   # v12: their final weights (the stance pull)
    # skirt outer surface near the flaps and the tip; the flaps' outer surface near the tip
    if first:
        cc = out_p.pos[out_p.tris].mean(1)
        near_pts = np.vstack([FLP_, shared.get('tip_sel_belt', belt.pos)[TIPV], belt.pos[BAGV]])      # tip_sel_at: the tip that chooses the selection
        zc = min(float(S[st].pos[:, 2].min()) for st in cfg['static'] if st in S and st not in [q.src for q in pieces]) if any(
            st in S and st not in [q.src for q in pieces] for st in cfg['static']) else 1e9
        if len(near_pts):
            dxy = np.min(np.linalg.norm(cc[:, None, :2] - near_pts[None, :, :2], axis=2), axis=1)
            shared['sko_t'] = o_t & (dxy < 6.0) & (cc[:, 2] > near_pts[:, 2].min() - 4.0) & (cc[:, 2] < min(near_pts[:, 2].max() + 1.0, zc + 1.0))
            # v15b: none above the pin line - the skirt does not move there, and the ILH men's tasset tops rest 1.4-2 inside it
            # at their hinges (a contact the plane audit found, pushed every frame)
            shared['sko_t'] &= cc[:, 2] < cfg['sk_belt'] - 1.5      # (- 1.5: pulling in along the flared top's normal lifts it ~1)
            # SoS: no up-facing triangles (the flared waist): the women's Braided bag rested 0.88 BEHIND one (normal z .71) under a
            # BodySlide body = pushed upward every frame; the bag / strap only ever meet the skirt's outward-facing sides
            fn_ = np.cross(out_p.pos[out_p.tris[:, 1]] - out_p.pos[out_p.tris[:, 0]], out_p.pos[out_p.tris[:, 2]] - out_p.pos[out_p.tris[:, 0]])
            fn_ /= np.linalg.norm(fn_, axis=1, keepdims=True) + 1e-12
            shared['sko_t'] &= np.abs(fn_[:, 2]) < SKO_MAX_NZ
        else:
            shared['sko_t'] = np.zeros(len(out_p.tris), bool)
        if flaps is not None:
            pl_t = np.isin(flab[flaps.tris], plates).all(1)
            out_fl = G.outer_mask(flaps.pos, flaps.tris, rig.cx, rig.cy) & pl_t
            cf = flaps.pos[flaps.tris].mean(1)
            dxy2 = np.min(np.linalg.norm(cf[:, None, :2] - belt.pos[TIPV][None, :, :2], axis=2), axis=1)
            shared['flo_t'] = out_fl & (dxy2 < 5.0) & (cf[:, 2] > belt.pos[TIPV, 2].min() - 3.0)
        if len(TIPV):                             # v12: the skirt under the tail (and where it can swing sideways to)
            tq = belt.pos[TIPV]; dxy3 = np.min(np.linalg.norm(cc[:, None, :2] - tq[None, :, :2], axis=2), axis=1)
            # no cut at the cuirass's lowest point (that suits the flaps / bag): skirt under the cuirass is never reached
            # (the tail cannot swing in past its drawn line) and the cut left whole tails uncovered (Steel Scaled men)
            shared['tipu_t'] = o_t & (dxy3 < 6.0) & (cc[:, 2] > tq[:, 2].min() - 4.0) & (cc[:, 2] < tq[:, 2].max() + 1.0)
        else:
            shared['tipu_t'] = np.zeros(len(out_p.tris), bool)
    STANCES = [KC.stride(T, 10, 8), KC.stride(T, -8, -10), KC.stride(T, 25, 15), KC.stride(T, -15, -25)]   # v12: idle + walk, both leads (hang_check's cases)

    def pull_stances(P_, TT, Wp, pts, Wq, clear, lat, exact, pen, o_):
        """v12: the pull a copy needs in the idle and walk stances (the leg-driven part of the layer under a piece moves into it there -
        in game a piece pressed in the idle stance twitches standing still: the Officer strap, 3 points) - the largest over the stances
        and the bind pose, along each vertex's own normal"""
        for Dm in STANCES:
            Pp = KC.skin(P_, Wp, Dm); qp = KC.skin(pts, Wq, Dm)
            _, op = K.pull_in(Pp, TT, qp, clear, 2.0, lat=lat)
            if exact: op = pull_exact(Pp, TT, op, qp, clear, pen=pen)
            o_ = np.maximum(o_, op)
        return o_

    HC_ = float(cfg.get('hang_clear', HANG_CLEAR))           # 2026-10-13: the room every hanging piece keeps over its copy

    def finish_copy(name, PC, TC, okey, ids, cparts, pts, pparts, clear, pen):
        """2026-10-13 (see HANG_CLEAR): a hanging piece's copy after its pull (shared[okey] = the offsets on this weight). Women: pulled
        exactly on every BodySlide build as well. A pull that FOLDS triangles to face in (a corner pulled to the 2.0 cap beside one pulled
        ~0 tips a coarse triangle over) is repaired, keeping the clearance (offsets only grow): (1) a gentle offset field - no edge's ends
        differ by more than s x its length (s .3 / .15 / .08, the shallow end raised); (2) the offsets along a smoothed direction field (the
        vertex normals part at a crease, where even an even pull folds); (3) the old equalising per triangle. Only what still faces in on
        this weight, a BodySlide build or a blend with the weight built before is recorded for main() to drop on every weight (the first
        builds dropped up to 186 folded triangles and opened holes under the guards' pouches: tools/copy_cover.py)"""
        if not len(TC): return
        shared.setdefault('copy_ids', {})[name] = [[str(k_), int(i_)] for k_, i_ in ids]      # 2026-10-14: the report's copy_ids (posed_drop)
        off = np.array(shared[okey], float); Nv = K.vertex_normals(PC, TC); cx_, cy_ = rig.cx, rig.cy
        if any(str(k_).endswith('#c') for k_, _ in ids) and Dz.get('copy_reproject', False):      # opt-in: a coarse copy whose points rest close still ends inside (Eastmarch heavy pouch -1.89 vs -1.57) - item 4 restores those copies' full resolution instead
            # 2026-10-14 item 4: a COARSE copy (copy_res) starts on its original surface - every triangle pushed out of the chord sag
            # it was decimated into; the pull below then adds only what the points' clearance needs (as on the full-resolution copy)
            # (first build: the sag alone left the Eastmarch heavy pouch copy -1.94 vs the full-resolution -1.57: the clearance pull then
            # dragged whole BIG triangles in for one close point) - so the pull is solved at FULL resolution over the copy's area and each
            # coarse corner (a full-resolution vertex) takes that vertex's pull, minus its chord sag; the coarse pull below adds only what
            # its chords still need
            sag_ = coarse_sag(PC, TC, cparts, Nv, cx_, cy_)
            fo_ = np.full(len(PC), np.nan); o0_ = 0
            for q_, v_ in cparts:
                v_ = np.asarray(v_); m_ = G.outer_mask(q_.pos, q_.tris, cx_, cy_); ft_ = q_.tris[m_]
                if len(v_) and len(ft_):
                    cc_ = q_.pos[ft_].mean(1); dmin_ = np.full(len(ft_), np.inf)
                    for s0 in range(0, len(v_), 256): dmin_ = np.minimum(dmin_, np.linalg.norm(cc_[:, None] - q_.pos[v_[s0:s0 + 256]][None], axis=2).min(1))
                    ft_ = ft_[dmin_ < 3.0]
                if len(ft_):
                    fv_ = np.unique(ft_); rm_ = np.full(len(q_.pos), -1); rm_[fv_] = np.arange(len(fv_))
                    of_ = pull_exact(q_.pos[fv_], rm_[ft_], np.zeros(len(fv_)), pts, clear, pen=pen)
                    hit_ = rm_[v_] >= 0; idx_ = np.where(hit_)[0]
                    fo_[o0_ + idx_] = of_[rm_[v_[hit_]]]
                o0_ += len(v_)
            if np.isfinite(fo_).any():
                off = np.where(np.isfinite(fo_), fo_, off) - sag_; shared[okey] = list(off)
                log.append(f'{g}_{variant}: {name}: coarse copy on the full-resolution copy surface: pulls from the full-resolution solve '
                           f'(max {np.nanmax(fo_):.2f}), chord sag out by median {np.median(sag_[sag_ > 1e-3]) if (sag_ > 1e-3).any() else 0:.2f} max {sag_.max():.2f}')
        MB = morph_builds(shared, T) if g == 'f' else []
        dC = [np.vstack([piece_disp(q, Dm)[v] for q, v in cparts]) for _, Dm in MB]
        dQ = [np.vstack([piece_disp(q, Dm)[i] for q, i in pparts]) if pparts else np.zeros((len(pts), 3)) for _, Dm in MB]
        prev = shared.setdefault('copy_q', {}).get(name) if not MB else None
        prev = prev if prev is not None and len(prev) == len(PC) else None

        def pull_all(o, D):
            for _ in range(2 if MB else 1):
                for dc, dq in zip(dC, dQ): o = pull_exact(PC + dc, TC, o, pts + dq, clear, pen=pen, Nv=D)
                o = pull_exact(PC, TC, o, pts, clear, pen=pen, Nv=D)
            return o

        def facing(o, D):          # the lowest radial facing per triangle over this weight, the BodySlide builds and the blends
            Q = PC - o[:, None] * D; fr = radial_dot(Q, TC, cx_, cy_)
            for dc in dC: fr = np.minimum(fr, radial_dot(Q + dc, TC, cx_, cy_))
            for i_ in range(0, len(dC) - 1, 2):
                for w_ in np.linspace(0.1, 0.9, 9): fr = np.minimum(fr, radial_dot(Q + (1 - w_) * dC[i_] + w_ * dC[i_ + 1], TC, cx_, cy_))
            if prev is not None:
                for w_ in np.linspace(0.1, 0.9, 9): fr = np.minimum(fr, radial_dot((1 - w_) * Q + w_ * prev, TC, cx_, cy_))
            return fr
        Dir = Nv; off = pull_all(off, Dir)
        src_in = radial_dot(PC, TC, cx_, cy_) < 0                  # faces in on this weight before any pull (a selection made on _1, reused)
        if MB:     # 2026-10-13 item B (PLAN_SPEED): women - faces in on a BodySlide build / blend with NO pull = the build's own geometry, which no
            src_in = src_in | (facing(np.zeros(len(PC)), Nv) < 0)  # pull repairs: left out of the repair (it chased them through every candidate) and counted
        fold0 = (facing(off, Dir) < 0) & ~src_in; nfix = int(fold0.sum()); how = []
        if fold0.any():
            for s_ in (0.3, 0.15, 0.08):
                off = pull_all(slope_limit(off, TC, PC, s_), Dir)
                if not ((facing(off, Dir) < 0) & ~src_in).any(): how.append(f'slope {s_}'); break
            else:
                # (2) the plates' EDGE STRIPS (0.16-0.29 wide - the plate's thickness - at their hems and side edges, corner normals 45-59 deg
                # apart: GuardHeavy) turn inside out at a 2.0 pull along any normal-like field: pull straight in toward the body axis instead -
                # two corners 0.2 apart then move in parallel (~1 deg), no strip can invert; then a smoothed normal field
                rad_ = np.c_[PC[:, 0] - cx_, PC[:, 1] - cy_, np.zeros(len(PC))]; rad_ = rad_ / (np.linalg.norm(rad_, axis=1, keepdims=True) + 1e-12)
                # first only AROUND the folds (their corners + 2 rings, blended back to the normals): elsewhere the normal pull clears a
                # point over a tilted face with less depth - the all-radial field left a Chainmail bag point at +0.56 with the pull at its cap
                seed_ = np.unique(TC[fold0 | ((facing(off, Dir) < 0) & ~src_in)])
                loc_ = local_dirs(Nv, rad_, TC, seed_, 2)
                for dname_, D_ in (('local radial', loc_), ('radial', rad_), ('smoothed', smooth_dirs(Nv, TC, 8))):
                    Dir = D_; off = pull_all(np.array(shared[okey], float), Dir)
                    if not ((facing(off, Dir) < 0) & ~src_in).any(): how.append(f'{dname_} directions'); break
                    for s_ in (0.3, 0.15, 0.08):
                        off = pull_all(slope_limit(off, TC, PC, s_), Dir)
                        if not ((facing(off, Dir) < 0) & ~src_in).any(): how.append(f'{dname_} directions + slope {s_}'); break
                    else: continue
                    break
                else:
                    for _ in range(12):
                        fo = (facing(off, Dir) < 0) & ~src_in
                        if not fo.any(): how.append('smoothed directions + equalised'); break
                        for t in np.where(fo)[0]: off[TC[t]] = off[TC[t]].max()
                        off = pull_all(off, Dir)
                    else: how.append('NOT repaired')
        if how and how[-1] == 'NOT repaired':      # debug: what the folded triangles are
            fo = np.where((facing(off, Dir) < 0) & ~src_in)[0]; r0 = radial_dot(PC, TC, cx_, cy_)
            for t in fo[:8]:
                a_, b_, c_ = PC[TC[t]]; el = [np.linalg.norm(b_ - a_), np.linalg.norm(c_ - b_), np.linalg.norm(a_ - c_)]
                nn = Nv[TC[t]]; spread = float(np.degrees(np.arccos(np.clip(min(nn[0] @ nn[1], nn[1] @ nn[2], nn[0] @ nn[2]), -1, 1))))
                cc = PC[TC[t]].mean(0)
                log.append(f'      folded {ids[t][0]} tri {ids[t][1]}: z {cc[2]:.1f} at {np.degrees(np.arctan2(cc[0] - cx_, cc[1] - cy_)):.0f} deg, edges {min(el):.2f}..{max(el):.2f}, '
                           f'radial before {r0[t]:+.2f}, corner pulls {off[TC[t]].round(2).tolist()}, corner normals spread {spread:.0f} deg')
        shared[okey] = off; shared[okey + '#dir'] = Dir; Q = PC - off[:, None] * Dir
        bad = facing(off, Dir) < 0
        if not MB: shared['copy_q'][name] = Q                        # men: the next weight's blends are checked against this one
        rec_ = shared.setdefault('copy_infacing', {}); rsrc_ = shared.setdefault('copy_src_infacing', {}); alt_ = shared.setdefault('copy_src_width', {})
        for t in np.where(bad)[0]:
            (rsrc_ if src_in[t] else rec_).setdefault(ids[t][0], set()).add(int(ids[t][1]))   # item B: the source's own apart
            if src_in[t]:             # its width (the smallest altitude, on the source): the user accepted THIN source folds (0.3-0.4-wide strips)
                a_, b_, c_ = PC[TC[t]]; el_ = max(np.linalg.norm(b_ - a_), np.linalg.norm(c_ - b_), np.linalg.norm(a_ - c_))
                alt_[(ids[t][0], int(ids[t][1]))] = float(np.linalg.norm(np.cross(b_ - a_, c_ - a_)) / max(el_, 1e-9))
        gq = np.inf
        if len(pts):
            gq = float(np.min(B.Surface([('c', Q, TC)]).query(pts, k=8)[2]))
        log.append(f'{g}_{variant}: {name}: {len(TC)} tris pulled {clear:.2f} clear' + (f' on the base + {len(MB)} BodySlide builds' if MB else '') +
                   f' (max {off.max():.2f}); folded by the pull {nfix}' + (f' -> repaired: {", ".join(how)}' if how else '') +
                   f'; facing in: {int(src_in.sum())} before any pull (' + ('base / BodySlide builds / blends' if MB else 'this weight') +
                   f'), {int((bad & src_in).sum())} of them still, {int((bad & ~src_in).sum())} folded by the pull and not repaired; points over it min {gq:.2f}')

    def surf_copy(p, tsel, pts, clear, key, lat=2.0, exact=False, pen=2.0, pts_w=None, name=None, mkey=None, pparts=None, kind=None):
        if kind is not None and mkey is not None and copy_frac(Dz, cfg, kind):     # 2026-10-13 PERF: copy_res - the selection coarsened once
            tt, ids_c = copy_tris(shared, Dz, cfg, kind, p, mkey, tsel)
        else:
            if mkey is not None: tsel = keep_mask(shared, mkey, tsel)       # 2026-10-13: minus the triangles dropped for facing in
            tt = p.tris[tsel]; ids_c = [(mkey, int(i)) for i in np.where(tsel)[0]]
        v = np.unique(tt); rm = np.full(len(p.pos), -1); rm[v] = np.arange(len(v)); TT = rm[tt]
        if exact: key = f'{key}_{variant}'          # v12 (tail copies): per weight, exact clearance
        if (first or exact) and key not in shared and len(tt):
            _, o_ = K.pull_in(p.pos[v], TT, pts, clear, 2.0, lat=lat)
            if exact: o_ = pull_exact(p.pos[v], TT, o_, pts, clear, pen=pen)
            if pts_w is not None and len(pts_w) == len(pts) and Dz.get('stance_pull'):   # v12: opt-in - no design had a collider contact in the idle / walk stances, and the pull tilted small copy triangles whose planes reached strap points from behind (the prism test)
                o_ = pull_stances(p.pos[v], TT, [(W[p.name][i] if p.name in W else p.w[i]) for i in v], pts, pts_w, clear, lat, exact, pen, o_)
                if exact: o_ = pull_exact(p.pos[v], TT, o_, pts, clear, pen=pen)     # v12: re-validated in the bind pose - a stance pull tilts triangles, whose planes can reach a point from behind
            shared[key] = o_
            if name is not None and exact:
                finish_copy(name, p.pos[v], TT, key, ids_c, [(p, v)], pts, pparts, clear, pen)
        if not len(tt): shared[key] = np.zeros(0)
        return v, TT, (p.pos[v] - shared[key][:, None] * cdir(shared, key, p.pos[v], TT) if len(tt) else p.pos[v])     # 2026-10-13: cdir = the pull's own directions
    sko_pp = ([(flaps, FLV)] if flaps is not None else []) + [(belt, TIPV), (belt, BAGV)]
    # tip_sel_at (2026-10-14): the strap copy's pull reads the previous install's tip too (Lamellar / Heavy women: its offset moved .1-.15)
    sko_v, SKOT, SKOP = surf_copy(out_p, shared['sko_t'], np.vstack([FLP_, shared.get('tip_sel_belt', belt.pos)[TIPV], belt.pos[BAGV]]), max(cfg.get('tb_clear', TB_CLEAR), HC_), 'sko_off', exact=True, pen=Dz.get('sko_pen', SKO_PEN),
                                  pts_w=(FLP_W + [W[belt.name][i] for i in TIPV] + [W[belt.name][i] for i in BAGV]) if belt.name in W and len(FLP_W) == len(FLP_) else None,   # v15b: exact by plane (ILH tassets rested on it); SoS: per target (the women's bag met the skirt under big BodySlide bodies)
                                  name=N.SKO, mkey='sko_t', pparts=sko_pp)      # 2026-10-13: HANG_CLEAR (TB_CLEAR / tb_clear only as a minimum)
    if flaps is not None:
        flo_v, FLOT, FLOP = surf_copy(flaps, shared['flo_t'], belt.pos[TIPV], HC_, 'flo_off', exact=True, pen=1.0, pts_w=[W[belt.name][i] for i in TIPV] if belt.name in W else None,   # v12: TB_CLEAR -> TIP_CLEAR, exact (it only meets the tail)
                                      name=N.FLO, mkey='flo_t', pparts=[(belt, TIPV)])   # 2026-10-13: TIP_CLEAR -> HANG_CLEAR
    else:
        flo_v, FLOT, FLOP = np.zeros(0, int), np.zeros((0, 3), int), np.zeros((0, 3))
    # lateral reach TIP_LAT (not 2.0): on the curved skirt a tail point 2 units to the side reads as closer than it is along
    # a vertex's normal, which pulled the copy ~0.6 behind straps lying right on it (women's hide family)
    tipu_v, TIPUT, TIPUP = surf_copy(out_p, shared['tipu_t'], belt.pos[TIPV], HC_, 'tipu_off', lat=TIP_LAT, exact=True, pen=TAILU_PEN, pts_w=[W[belt.name][i] for i in TIPV] if belt.name in W else None,
                                     name=None if (Dz.get('tip_all_layers') or Dz.get('tip_under')) else N.TIPU, mkey='tipu_t', pparts=[(belt, TIPV)], kind='tipu')   # 2026-10-13: TIP_CLEAR -> HANG_CLEAR (the union copies below replace this one)
    tipu_parts = [(out_p, tipu_v)]
    if Dz.get('tip_all_layers') and len(TIPV):
        # v16 (user screenshot: the Long Nordic men's belt tail half under the right front mail panel): the strap hangs partly
        # over the front slit, where its copy of the mail had nothing - it fell into the gap and the panel's edge came over
        # it. The copy now also takes the inner layer near the strap (the cloth under the slit), all pulled in together.
        tq = belt.pos[TIPV]; parts_ = [(out_p, shared['tipu_t'], 'tipu_t')]
        for q in skirts:
            if q is out_p: continue
            kq = 'tipu_t_' + q.name
            if kq not in shared:
                cq = q.pos[q.tris].mean(1); dq = np.min(np.linalg.norm(cq[:, None, :2] - tq[None, :, :2], axis=2), axis=1)
                shared[kq] = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (dq < 6.0) & (cq[:, 2] > tq[:, 2].min() - 4.0) & (cq[:, 2] < tq[:, 2].max() + 1.0)
            parts_.append((q, shared[kq], kq))
        tipu_parts, TTs, Ps, o_, ids_ = [], [], [], 0, []
        for q, tsel, mk_ in parts_:
            tt, id_q = copy_tris(shared, Dz, cfg, 'tipu', q, mk_, tsel); ids_ += id_q       # 2026-10-13: minus dropped in-facing triangles; PERF: copy_res
            v = np.unique(tt); rm = np.full(len(q.pos), -1); rm[v] = np.arange(len(v))
            tipu_parts.append((q, v)); TTs.append(rm[tt] + o_); Ps.append(q.pos[v]); o_ += len(v)
        PC, TC = np.vstack(Ps), np.vstack(TTs)
        kk = 'tipu_all_off_' + variant
        if kk not in shared:
            _, off_ = K.pull_in(PC, TC, tq, HC_, 2.0, lat=TIP_LAT); shared[kk] = pull_exact(PC, TC, off_, tq, HC_, pen=2.0)     # 2026-10-13: TIP_CLEAR -> HANG_CLEAR
            finish_copy(N.TIPU, PC, TC, kk, ids_, tipu_parts, tq, [(belt, TIPV)], HC_, 2.0)
        TIPUT, TIPUP = TC, PC - shared[kk][:, None] * cdir(shared, kk, PC, TC)
    if Dz.get('tip_under') and len(TIPV):
        # SoS Officer v2 (user: 'the belt and the sash are all fucking up. its like theres no collision'): the strap hangs over the
        # sash end (tasset layer) and the mail - v1 gave it a copy of the mail only, which is not under it above z 60. Its copy now
        # comes from every layer listed, each part skinned to its own layer, pulled in together so the strap rests clear
        tq = belt.pos[TIPV]; parts_ = []
        for nm_ in Dz['tip_under']:
            q = next(p for p in skirts + tails if p.name == nm_); kq = 'tipu_t_' + nm_      # v8: + tails (the Officer strap over the sash end)
            if kq not in shared:
                cq = q.pos[q.tris].mean(1); dq = np.min(np.linalg.norm(cq[:, None, :2] - tq[None, :, :2], axis=2), axis=1)
                fq = np.cross(q.pos[q.tris[:, 1]] - q.pos[q.tris[:, 0]], q.pos[q.tris[:, 2]] - q.pos[q.tris[:, 0]]); fq /= np.linalg.norm(fq, axis=1, keepdims=True) + 1e-12
                # outward-facing SIDES only (first build: the sash's downward edge faces at z 57.5 'held' strap points 3.5 above them)
                shared[kq] = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (dq < 6.0) & (cq[:, 2] > tq[:, 2].min() - 4.0) & (cq[:, 2] < tq[:, 2].max() + 1.0) & (np.abs(fq[:, 2]) < Dz.get('tip_max_nz', SKO_MAX_NZ)) \
                    & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > umr_tip(Dz, q.name))
            parts_.append((q, shared[kq], kq))        # 2026-10-13: copy_tris takes the dropped in-facing triangles out (and coarsens at copy_res)
        tipu_parts, TTs, Ps, o_, ids_ = [], [], [], 0, []
        for q, tsel, mk_ in parts_:
            tt, id_q = copy_tris(shared, Dz, cfg, 'tipu', q, mk_, tsel); ids_ += id_q
            v = np.unique(tt); rm = np.full(len(q.pos), -1); rm[v] = np.arange(len(v))
            tipu_parts.append((q, v)); TTs.append(rm[tt] + o_); Ps.append(q.pos[v]); o_ += len(v)
        PC, TC = np.vstack(Ps), np.vstack(TTs)
        kk = 'tipu_under_off_' + variant
        if kk not in shared:
            _, off_ = K.pull_in(PC, TC, tq, HC_, 2.0, lat=TIP_LAT); shared[kk] = pull_exact(PC, TC, off_, tq, HC_, pen=TAILU_PEN)     # 2026-10-13: TIP_CLEAR -> HANG_CLEAR
            finish_copy(N.TIPU, PC, TC, kk, ids_, tipu_parts, tq, [(belt, TIPV)], HC_, TAILU_PEN)
        TIPUT, TIPUP = TC, PC - shared[kk][:, None] * cdir(shared, kk, PC, TC)
        if first: log.append(f'{g}: strap collider from ' + ', '.join(f'{q.name} {int(t.sum())} tris' for q, t, _ in parts_) + f' (pulled in max {shared[kk].max():.2f})')
    # v11 (Officer hangers, user: 'need collisions, going through the armor'): the straps and rings vs their own copy of the layers under
    # them (the plates and the mail), each part skinned to its own layer and pulled in so nothing rests on it - a plate swinging out on
    # a step now meets the strap, which is hinged at its rings and holds it in (the strap's own in-swing is 0.03)
    HANGV = np.concatenate([np.r_[h['front'], h['back'], h['strap']] for h in shared.get('hang_sel', [])]) if shared.get('hang_sel') else np.zeros(0, int)
    HANGUT, HANGUP, hangu_parts = np.zeros((0, 3), int), np.zeros((0, 3)), []
    HANGP = HANGV                       # 2026-10-13 PERF: the emitted collision points (hang_pts_step 2: the proxy, decided once on _1); the copy is
    if len(HANGV) and int(Dz.get('hang_pts_step', 1)) > 1:      # still pulled clear of EVERY hanger point (HANGV)
        if 'hang_proxy' not in shared: shared['hang_proxy'] = hang_proxy(belt.tris, HANGV, int(Dz['hang_pts_step']), pos=belt.pos)
        HANGP = shared['hang_proxy']
        if first: log.append(f'{g}: hip hanger collision points: proxy {len(HANGP)} of {len(HANGV)} (every boundary point + every other interior point)')
    if len(HANGV):
        hq = belt.pos[HANGV]; parts_ = []
        for nm_ in Dz.get('hang_under_layers', Dz.get('tip_under', ())):
            q = next((p for p in skirts + tails if p.name == nm_), None)
            if q is None: continue
            kq = 'hangu_t_' + nm_
            if kq not in shared:
                cq = q.pos[q.tris].mean(1); dq = np.min(np.linalg.norm(cq[:, None, :2] - hq[None, :, :2], axis=2), axis=1)
                fq = np.cross(q.pos[q.tris[:, 1]] - q.pos[q.tris[:, 0]], q.pos[q.tris[:, 2]] - q.pos[q.tris[:, 0]]); fq /= np.linalg.norm(fq, axis=1, keepdims=True) + 1e-12
                shared[kq] = G.outer_mask(q.pos, q.tris, rig.cx, rig.cy) & (dq < 6.0) & (cq[:, 2] > hq[:, 2].min() - 4.0) & (cq[:, 2] < hq[:, 2].max() + 1.0) & (np.abs(fq[:, 2]) < SKO_MAX_NZ) \
                    & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > Dz.get('hang_min_radial', HANG_MIN_RADIAL))     # faces that face OUT: a plate's side-edge trim would shove the strap sideways
            if shared[kq].any(): parts_.append((q, shared[kq], kq))     # 2026-10-13: copy_tris takes the dropped in-facing triangles out (and coarsens at copy_res)
        if parts_:
            TTs, Ps, o_, ids_ = [], [], 0, []
            for q, tsel, mk_ in parts_:
                tt, id_q = copy_tris(shared, Dz, cfg, 'hangu', q, mk_, tsel); ids_ += id_q
                v = np.unique(tt); rm = np.full(len(q.pos), -1); rm[v] = np.arange(len(v))
                hangu_parts.append((q, v)); TTs.append(rm[tt] + o_); Ps.append(q.pos[v]); o_ += len(v)
            PC, TC = np.vstack(Ps), np.vstack(TTs)
            kk = 'hangu_off_' + variant
            if kk not in shared:     # 2026-10-13: TIP_CLEAR -> HANG_CLEAR (the hangers rested .55 over the real layers and their copy - 28-132 pts within .6)
                _, off_ = K.pull_in(PC, TC, hq, HC_, 2.0, lat=TIP_LAT); off_ = pull_exact(PC, TC, off_, hq, HC_, pen=TAILU_PEN)
                WC = [(W[q.name][i] if q.name in W else q.w[i]) for q, v in hangu_parts for i in v]
                shared[kk] = pull_exact(PC, TC, pull_stances(PC, TC, WC, hq, [W[belt.name][i] for i in hs], HC_, TIP_LAT, True, TAILU_PEN, off_), hq, HC_, pen=TAILU_PEN) if belt.name in W and Dz.get('stance_pull') else off_
                finish_copy(N.HANGU, PC, TC, kk, ids_, hangu_parts, hq, [(belt, HANGV)], HC_, TAILU_PEN)
            HANGUT, HANGUP = TC, PC - shared[kk][:, None] * cdir(shared, kk, PC, TC)
            if first: log.append(f'{g}: hanger collider from ' + ', '.join(f'{q.name} {int(t.sum())} tris' for q, t, _ in parts_) + f' (pulled in max {shared[kk].max():.2f})')
    # 2026-10-14 HOLDS (flap_settle): the hip strap's own copy of the cuirass hem + the skirt under it, ON their surface (the strap was
    # settled flap_settle + .05 clear of exactly these faces, so the pull at flap_settle finds nothing to do on the men's weights)
    FLAPUT, FLAPUP, flapu_parts = np.zeros((0, 3), int), np.zeros((0, 3)), []
    if Dz.get('flap_settle') and flaps is not None and len(FLV):
        fq = flaps.pos[FLV]; FCL_ = float(Dz['flap_settle']); parts_ = []
        for q in (flap_cuirass(S, T, rest, cfg, shared), out_p):
            kq = 'flapu_t_' + q.name
            if kq in shared and shared[kq].any(): parts_.append((q, shared[kq], kq))
        if parts_:
            TTs, Ps, o_, ids_ = [], [], 0, []
            for q, tsel, mk_ in parts_:
                tt, id_q = copy_tris(shared, Dz, cfg, 'flapu', q, mk_, tsel); ids_ += id_q
                v = np.unique(tt); rm = np.full(len(q.pos), -1); rm[v] = np.arange(len(v))
                flapu_parts.append((q, v)); TTs.append(rm[tt] + o_); Ps.append(q.pos[v]); o_ += len(v)
            PC, TC = np.vstack(Ps), np.vstack(TTs)
            kk = 'flapu_off_' + variant
            if kk not in shared:
                _, off_ = K.pull_in(PC, TC, fq, FCL_, 2.0, lat=TIP_LAT); shared[kk] = pull_exact(PC, TC, off_, fq, FCL_, pen=TAILU_PEN)
                finish_copy(N.FLAPU, PC, TC, kk, ids_, flapu_parts, fq, [(flaps, FLV)], FCL_, TAILU_PEN)
            FLAPUT, FLAPUP = TC, PC - shared[kk][:, None] * cdir(shared, kk, PC, TC)
            if first: log.append(f'{g}: hip strap collider from ' + ', '.join(f'{q.name} {int(t.sum())} tris' for q, t, _ in parts_) + f' (pulled in max {shared[kk].max():.2f}); strap collision pts {len(FLV)}')
    # SoS Officer v2: colliders BETWEEN the layers (cfg 'layer_coll': name, surf piece, facing 'in' (wound inward - keeps the layer
    # under it inside) / 'out' (keeps the layer over it outside), pts = the layer whose lining meets it, clear, pen): the blue
    # skirt's lining vs the mail's inside, the tasset layer vs the mail's outside - each pulled exactly so nothing rests on it
    LCOLL = {}
    for lc in cfg.get('layer_coll', ()):
        sp = next(p for p in skirts if p.name == lc['surf']); gp0 = next(p for p in skirts if p.role == 'skirt:outer@' + lc['pts'])
        if lc.get('pts_all') and ('lc_all', lc['name']) not in shared:     # v10 (Officer): the plate's FACE and trim-edge points join the collision
            # points (the rims alone let the mail through the trim at the side edges in a stance); only below pts_zmax (the top rows rest on
            # the mail under the belt band by the author's design - those stay out); decided once
            ex_ = np.setdiff1d(np.arange(len(gp0.pos)), keep[gp0.name]); ex_ = ex_[gp0.pos[ex_, 2] < lc.get('pts_zmax', 1e9)]
            om0 = G.outer_mask(sp.pos, sp.tris, rig.cx, rig.cy); t0 = sp.tris[om0] if lc['facing'] == 'out' else sp.tris[~om0][:, [0, 2, 1]]
            h0 = prism_sd_min(gp0.pos[ex_], sp.pos, t0, lo=-3.0, hi=6.0)        # only points resting IN FRONT of the surface (a turned-under
            ex_ = ex_[np.isfinite(h0) & (h0 > lc.get('pts_min_h', 0.5))]       # hem behind it, a point over no surface, or one without real air (a bigger
            # BodySlide body closes it: the Lovely Lady preset met 3 at the front plate's inner edge at 0.1) is no collision point
            for c_, hw_ in lc.get('pts_skip', ()):          # angles left out (the Officer's front centre: the sash and the strap hang over the plates'
                ex_ = ex_[np.abs(wrap(np.degrees(np.arctan2(gp0.pos[ex_, 0] - rig.cx, gp0.pos[ex_, 1] - rig.cy)) - c_)) > hw_]   # inner edges there, a big preset closes the air)
            keep[gp0.name] = np.r_[keep[gp0.name], ex_]; shared[('lc_all', lc['name'])] = int(len(ex_))
            log.append(f'{g}: layer collider {lc["name"]}: + {len(ex_)} {lc["pts"]} face / edge pts below z {lc.get("pts_zmax", 1e9):.1f} as collision points (v10)')
        pts_ = gp0.pos[keep[gp0.name]]; kt = 'lc_t_' + lc['name']
        if kt not in shared:          # decided once, on _1: the surface's triangles near the points
            cc_ = sp.pos[sp.tris].mean(1); dxy_ = np.min(np.linalg.norm(cc_[:, None, :2] - pts_[None, :, :2], axis=2), axis=1)
            m_ = (dxy_ < lc.get('reach', 4.0)) & (cc_[:, 2] > max(pts_[:, 2].min() - 2.0, lc.get('zmin', -1e9))) & (cc_[:, 2] < min(pts_[:, 2].max() + 2.0, lc.get('zmax', 1e9)))
            if lc['facing'] == 'out': m_ &= G.outer_mask(sp.pos, sp.tris, rig.cx, rig.cy)
            if lc.get('min_radial'): m_ &= radial_dot(sp.pos, sp.tris, rig.cx, rig.cy) > lc['min_radial']     # Officer v4: no side faces
            for c_, hw_ in lc.get('skip', ()):          # angles left out (the mail's turned front-opening edges over the blue strip)
                m_ &= np.abs(wrap(np.degrees(np.arctan2(cc_[:, 0] - rig.cx, cc_[:, 1] - rig.cy)) - c_)) > hw_
            shared[kt] = m_
        tt = sp.tris[shared[kt]]
        if lc['facing'] == 'in': tt = tt[:, [0, 2, 1]]
        v_ = np.unique(tt); rm_ = np.full(len(sp.pos), -1); rm_[v_] = np.arange(len(v_)); TT_ = rm_[tt]
        if first and lc.get('min_gap') and ('lc_gap', lc['name']) not in shared:
            # v4 (as the leg colliders' LINING_MIN_GAP): lining points resting closer than min_gap to the surface at rest are where the
            # two layers converge by design (the blue lining on the mail's border above its sewn hem) - holding them clear would pull
            # the collider out through the visible surface, and a BodySlide preset can still land them on it. Left out of this layer.
            gap0 = B.Surface([('s', sp.pos[v_], TT_)]).query(pts_, k=8)[2]; near = gap0 < lc['min_gap']
            shared[('lc_gap', lc['name'])] = int(near.sum())
            if near.any():
                keep[gp0.name] = keep[gp0.name][~near]; pts_ = gp0.pos[keep[gp0.name]]
                log.append(f'{g}: layer collider {lc["name"]}: {int(near.sum())} {lc["pts"]} lining pts resting closer than {lc["min_gap"]} to it (z {gp0.pos[keep[gp0.name], 2].min():.1f}..) left out of the collision points')
        ko = f'lc_off_{lc["name"]}_{variant}'
        if ko not in shared:
            _, o_ = K.pull_in(sp.pos[v_], TT_, pts_, lc['clear'], 2.0, lat=lc.get('lat', 2.0)); shared[ko] = pull_exact(sp.pos[v_], TT_, o_, pts_, lc['clear'], pen=lc['pen'])
            if first and ('lc_held', lc['name']) not in shared:
                # v4: points the pull could not clear (it hit its 2.0 cap - the plates' turned-under hem sewn under the mail's top edge,
                # where the tilted top-edge triangles end up over the point) are sewn there: no collider can hold them and the catch
                # would pop them out through the mail. Left out of this layer's collision points; the pull is redone without them.
                PPt = sp.pos[v_] - shared[ko][:, None] * K.vertex_normals(sp.pos[v_], TT_)
                sd0 = prism_sd_min(pts_, PPt, TT_, lo=-lc['pen'] - 0.5, hi=3.0)      # v10: the LOWEST plane over any triangle the point projects into (what verify tests), not the nearest triangle's
                held = np.isfinite(sd0) & (sd0 < lc['clear'] - 0.25)
                shared[('lc_held', lc['name'])] = int(held.sum())
                if held.any():
                    hp = pts_[held]
                    keep[gp0.name] = keep[gp0.name][~held]; pts_ = gp0.pos[keep[gp0.name]]
                    _, o_ = K.pull_in(sp.pos[v_], TT_, pts_, lc['clear'], 2.0, lat=lc.get('lat', 2.0)); shared[ko] = pull_exact(sp.pos[v_], TT_, o_, pts_, lc['clear'], pen=lc['pen'])
                    log.append(f'{g}: layer collider {lc["name"]}: {int(held.sum())} {lc["pts"]} lining pts the pull could not clear (sewn to it; at ' +
                               ', '.join(f'({x[0]:.1f}, {x[1]:.1f}, {x[2]:.1f})' for x in hp[:3]) + ') left out of the collision points; pull redone')
        PP_ = sp.pos[v_] - shared[ko][:, None] * K.vertex_normals(sp.pos[v_], TT_)
        LCOLL[lc['name']] = (sp, v_, TT_, PP_)
        if first:
            d_ = B.Surface([('c', PP_, TT_)]).query(pts_, k=8)[2]
            log.append(f'{g}: layer collider {lc["name"]}: {len(TT_)} tris of {sp.name} ({lc["facing"]}), z {PP_[:, 2].min():.1f}..{PP_[:, 2].max():.1f}, '
                       f'moved max {shared[ko].max():.2f}; {lc["pts"]} lining pts {len(pts_)}, rest gap min {d_.min():.2f}')
    # SoS: per tail, its own copy of the skirt under it (pulled in exactly as far as the tail needs to rest clear) + its points
    TAILC = {}
    for tp_ in tails:
        # collision points only where the tail really swings: its top under the belt (own share < SASH_COLLIDE_OWN) barely moves,
        # was only partly lifted, and bent its skirt copy in 2 units (Braided v1: 3-4 resting contacts at z 69.8-71)
        # v2: and not within SASH_COLLIDE_BELOW of its top - there the sash points behind the flared waist of the mail fell
        # into tilted copy triangles (copy pulled in 1.5-1.8, 3-4 contacts); neither the mail nor the sash swings that close
        # to their hinges
        key = tp_.name; tv_ = np.where((own_t[key] > SASH_COLLIDE_OWN) & (tp_.pos[:, 2] < rig.tails[key]['top'] - cfg.get('sash_collide_below', SASH_COLLIDE_BELOW)))[0]; kt = 'tailu_t_' + key
        # the author tucked the sash's top INTO the mail (Braided men: up to .47 deep at z 66-72) - a collider cannot hold that
        # clear (verify: 10 resting contacts). RA v12 tail lift: those points rest TIP_LIFT on top of the skirt, the lift spread
        # over the cloth (sigma TIP_LIFT_SIGMA) along the skirt's outward normal and faded in with the tail's own share
        # (the top stays joined to the band); recorded in the report ('lift') so verify can undo it
        # v3 (Officer): the surface under a tail may be SEVERAL layers (design key tail_under, like the strap's tip_under): the tasset
        # layer and the mail under the sash end. Lift and copy use the union of their outward-facing triangles; the copy's points are
        # later skinned each to its own layer (uparts). Without tail_under everything below is the single-layer code, unchanged.
        if Dz.get('tail_under'):
            uq_ = [next(p for p in skirts if p.name == nm_) for nm_ in Dz['tail_under']]; uo_ = np.cumsum([0] + [len(q.pos) for q in uq_])
            lp_pos = np.vstack([q.pos for q in uq_]); lp_tris = np.vstack([q.tris[G.outer_mask(q.pos, q.tris, rig.cx, rig.cy)] + uo_[j] for j, q in enumerate(uq_)])
        else:
            uq_, uo_, lp_pos, lp_tris = [out_p], np.array([0, len(out_p.pos)]), out_p.pos, out_p.tris[o_t]
        if Dz.get('tail_lift', True) and len(tv_):
            tq_ = tp_.pos[tv_]; tt_ = lp_tris
            fno_ = np.cross(lp_pos[tt_[:, 1]] - lp_pos[tt_[:, 0]], lp_pos[tt_[:, 2]] - lp_pos[tt_[:, 0]])
            fno_ /= np.linalg.norm(fno_, axis=1, keepdims=True) + 1e-12
            tri_, _, dist_, cp_ = B.Surface([('o', lp_pos, tt_)]).query(tq_, k=8); sd_ = ((tq_ - cp_) * fno_[tri_]).sum(1)
            lat_ = np.sqrt(np.maximum(dist_ ** 2 - sd_ ** 2, 0.0))
            need = np.where((lat_ < 0.3) & (sd_ > -2.5), np.maximum(0.0, TIP_LIFT - sd_), 0.0)
            if need.max() > 1e-4:
                Kd = np.exp(-(np.linalg.norm(tq_[:, None] - tq_[None], axis=2) / TIP_LIFT_SIGMA) ** 2)
                Lf = (Kd * need[None, :]).max(1) * smooth01((own_t[key][tv_] - 0.2) / 0.5)
                nd = Kd @ fno_[tri_]; nd /= np.linalg.norm(nd, axis=1, keepdims=True) + 1e-12
                offs = np.round(Lf[:, None] * nd, 6); mv = Lf > 1e-4
                tp_.pos = tp_.pos.copy(); tp_.pos[tv_[mv]] += offs[mv]
                rec_lift(shared, variant, tp_.name, tv_[mv].tolist(), offs[mv].tolist())
                log.append(f'{g}_{variant}: tail {key} lifted onto the skirt at {int(mv.sum())} of {len(tv_)} pts (needed max {need.max():.2f}, '
                           f'{int((need > 0).sum())} pts; moved max {Lf.max():.2f})')
        if first:
            tq = tp_.pos[tv_]
            for j, q in enumerate(uq_):             # per layer under the tail: its outward triangles near the tail's collision points
                kq = kt if not Dz.get('tail_under') else f'{kt}_{q.name}'
                cc_ = q.pos[q.tris].mean(1)
                dxy_ = np.min(np.linalg.norm(cc_[:, None, :2] - tq[None, :, :2], axis=2), axis=1) if len(tq) else np.full(len(cc_), 99.0)
                om_ = o_t if q is out_p else G.outer_mask(q.pos, q.tris, rig.cx, rig.cy)
                zlo_, zhi_ = (tq[:, 2].min(), tq[:, 2].max()) if len(tq) else (0.0, 0.0)
                shared[kq] = om_ & (dxy_ < 6.0) & (cc_[:, 2] > zlo_ - 4.0) & (cc_[:, 2] < zhi_ + 1.0) & (radial_dot(q.pos, q.tris, rig.cx, rig.cy) > umr(Dz, q.name))
                if Dz.get('tail_max_nz'):   # SoS (Lamellar / Heavy v1: 4-7 sash points at z 66 sat behind the flared waist's tilted
                    fq_ = np.cross(q.pos[q.tris[:, 1]] - q.pos[q.tris[:, 0]], q.pos[q.tris[:, 2]] - q.pos[q.tris[:, 0]])
                    fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12      # triangles within the 4.0 catch, the copy at its
                    shared[kq] &= np.abs(fq_[:, 2]) < Dz['tail_max_nz']            # 2.0 pull-in cap) - outward-facing sides only, like the bag's
        tcl_ = cfg.get('tail_clear', 0.0); tcl_ = tcl_.get(key, 0.0) if isinstance(tcl_, dict) else tcl_     # 2026-10-13: or {tail name: clear}
        tcl_ = max(tcl_, HC_)      # 2026-10-13: HANG_CLEAR (a design's tail_clear only as a minimum; was TIP_CLEAR .4 / .8)
        tse_ = Dz.get('tail_settle')
        if tse_ and len(tv_) and key in (tse_ if isinstance(tse_, (tuple, list)) else (key,)):
            # 2026-10-14 HOLDS (PLAN_HOLDS 4: the RiftenLight sash end rested .40 over the skirt, its copy 82 pts .6-.7 BEHIND it - 'settled
            # >= 1.0, copy on the surface, as the tips'): tip_settle for a tail - its collision pts pushed out radially until the copy pull's
            # two measures (true distance; height along each copy vertex normal within TIP_LAT) read the copy clearance + .05 against the
            # faces its copy is made of, so the copy needs no pull; the push spread over the whole tail (sigma 1.5: it fades into the sewn top)
            wts_ = tcl_ + 0.05; FT_ = []
            for q in uq_:
                kq = kt if not Dz.get('tail_under') else f'{kt}_{q.name}'
                if shared[kq].any(): FT_.append((q.name, q.pos, q.tris[shared[kq]]))
            if FT_:
                suT_ = B.Surface(FT_); VVt_ = np.vstack([qp_[np.unique(qt_)] for _, qp_, qt_ in FT_]); VNt_ = np.vstack([K.vertex_normals(qp_, qt_)[np.unique(qt_)] for _, qp_, qt_ in FT_])
                Pt0_ = tp_.pos.copy(); totT_ = 0.0
                for _it in range(8):
                    P_ = tp_.pos[tv_]; _, _, dd_, _ = suT_.query(P_, k=24)
                    v_ = P_[:, None, :] - VVt_[None]; s_ = (v_ * VNt_[None]).sum(2); la_ = np.linalg.norm(v_ - s_[..., None] * VNt_[None], axis=2)
                    need_ = np.maximum(0.0, np.maximum(wts_ - dd_, np.where((la_ < TIP_LAT) & (s_ > -2.0), wts_ - s_, 0.0).max(1)))
                    if need_.max() < 1e-3: break
                    PA_ = tp_.pos; Kt_ = np.exp(-(np.linalg.norm(PA_[:, None] - P_[None], axis=2) / 1.5) ** 2); nd_ = (Kt_ * need_[None, :]).max(1)
                    rad_ = np.c_[PA_[:, 0] - rig.cx, PA_[:, 1] - rig.cy, np.zeros(len(PA_))]; rad_ /= np.linalg.norm(rad_, axis=1, keepdims=True) + 1e-12
                    tp_.pos = tp_.pos + nd_[:, None] * rad_; totT_ = max(totT_, float(nd_.max()))
                dT_ = tp_.pos - Pt0_; mT_ = np.where(np.linalg.norm(dT_, axis=1) > 1e-4)[0]
                if len(mT_): rec_lift(shared, variant, tp_.name, mT_.tolist(), dT_[mT_].tolist())
                log.append(f'{g}_{variant}: tail {key} settled EXACT {wts_:.2f} from its copy faces ({", ".join(n for n, _, _ in FT_)}): {len(mT_)} of {len(tp_.pos)} pts moved, '
                           f'by up to {np.linalg.norm(dT_, axis=1).max():.2f}')
        if not Dz.get('tail_under'):
            uv_, UT_, UP_ = surf_copy(out_p, shared[kt], tp_.pos[tv_], tcl_, 'tailu_off_' + key, lat=TIP_LAT, exact=True, pen=TAILU_PEN, pts_w=[W[tp_.name][i] for i in tv_] if tp_.name in W and len(W[tp_.name]) == len(tp_.pos) else None,
                                      name=N.tailu(key), mkey=kt, pparts=[(tp_, tv_)], kind='tailu')
            uparts = [(out_p, uv_)]
        else:                                       # the union copy, pulled in together; each part keeps its own layer's points
            TTs, Ps, o_, uparts, ids_ = [], [], 0, [], []
            for q in uq_:
                mk_ = f'{kt}_{q.name}'; tt, id_q = copy_tris(shared, Dz, cfg, 'tailu', q, mk_, shared[mk_]); ids_ += id_q   # 2026-10-13: minus dropped in-facing triangles; PERF: copy_res
                v = np.unique(tt); rm = np.full(len(q.pos), -1); rm[v] = np.arange(len(v))
                uparts.append((q, v)); TTs.append(rm[tt] + o_); Ps.append(q.pos[v]); o_ += len(v)
            UT_ = np.vstack(TTs) if TTs else np.zeros((0, 3), int); PU = np.vstack(Ps) if Ps else np.zeros((0, 3))
            kk = f'tailu_under_off_{key}_{variant}'
            if kk not in shared and len(UT_):
                _, off_ = K.pull_in(PU, UT_, tp_.pos[tv_], tcl_, 2.0, lat=TIP_LAT)
                shared[kk] = pull_exact(PU, UT_, off_, tp_.pos[tv_], tcl_, pen=TAILU_PEN)
                finish_copy(N.tailu(key), PU, UT_, kk, ids_, uparts, tp_.pos[tv_], [(tp_, tv_)], tcl_, TAILU_PEN)
            if not len(UT_): shared[kk] = np.zeros(0)
            UP_ = PU - shared[kk][:, None] * cdir(shared, kk, PU, UT_) if len(UT_) else PU
        TAILC[key] = (tp_, tv_, uparts, UT_, UP_)
    if first:
        rig.has_tipu = bool(len(TIPUT)); rig.has_hangu = bool(len(HANGUT)); rig.has_flapu = bool(len(FLAPUT))
        res = {}
        for key, (tp_, tv_, uparts, UT_, UP_) in TAILC.items():
            rig.tailu[key] = bool(len(UT_)); pts = tp_.pos[tv_]
            d1 = B.Surface([('u', UP_, UT_)]).query(pts, k=8)[2].min() if len(UT_) else 99
            d2 = B.Surface([('l', LP, LT)]).query(pts, k=8)[2].min()
            res[key.lower()] = (len(pts), float(d1), float(d2), 99.0)
            offk = f'tailu_under_off_{key}_{variant}' if Dz.get('tail_under') else 'tailu_off_' + key + '_' + variant
            log.append(f'{g}: tail {key}: {len(pts)} collision pts, its skirt copy {len(UT_)} tris' + (' from ' + ' + '.join(q.name for q, _ in uparts) if Dz.get('tail_under') else '') + f' (pulled in max '
                       f'{shared[offk].max() if len(UT_) else 0:.2f}), rest gap to it {d1:.2f}, to the legs {d2:.2f}')
        for nm, pts in (('flap', FLP_), ('tip', belt.pos[TIPV]), ('bag', belt.pos[BAGV])):
            if not len(pts): continue
            d1 = (B.Surface([('o', SKOP, SKOT)]).query(pts, k=8)[2].min() if len(SKOT) else 99) if nm != 'tip' else                 (B.Surface([('u', TIPUP, TIPUT)]).query(pts, k=8)[2].min() if len(TIPUT) else 99)
            d2 = B.Surface([('l', LP, LT)]).query(pts, k=8)[2].min()
            d3 = B.Surface([('f', FLOP, FLOT)]).query(pts, k=8)[2].min() if (nm == 'tip' and len(FLOT)) else 99
            res[nm] = (len(pts), float(d1), float(d2), float(d3))
        shared['rest'] = res
        log.append(f'{g}: skirt-outer collider {len(SKOT)} tris (pulled in max {shared["sko_off_" + variant].max() if len(shared["sko_off_" + variant]) else 0:.2f}), flap-outer {len(FLOT)} tris, '
                   f'skirt-under-tip {len(TIPUT)} tris (pulled in max {shared["tipu_off_" + variant].max() if len(shared["tipu_off_" + variant]) else 0:.2f}); ' +
                   '; '.join(f'{nm} pts {n}: to {"skirt-under-tip" if nm == "tip" else "skirt-outer"} {a:.2f}, legs {b:.2f}' + (f', flap-outer {c:.2f}' if c < 99 else '') for nm, (n, a, b, c) in res.items()))
    # ---- write
    out = cfg['out'].format(variant) if g in ('m', 'v') else STAGE + f'CalienteTools/BodySlide/ShapeData/{shared["f_paths"]["folder"]}/{shared["f_paths"]["srcfile"]}'
    w = Writer(nif, out); w.skel_G = {}
    for t in T:
        for nm, xf in t.s2b.items():
            if not N.is_phys(nm) and R.is_skel(nm): w.skel_G.setdefault(nm, np.linalg.inv(B.tb2m(xf)))
    w.skel_G.setdefault(ROOT, np.eye(4))
    allG, allPar = dict(rig.G), dict(rig.parent)          # SoS Officer v2: + the extra layers' rigs
    for r_ in shared.get('rigs', {}).values(): allG.update(r_.G); allPar.update(r_.parent)
    w.custom_G = dict(allG); w.parent = dict(allPar)
    made = [False]

    def make_nodes():
        if made[0]: return
        if PELV not in w.out.nodes: w.out.add_node(PELV, B.m2tb(w.skel_G[PELV]), w.out.root)
        for nm in sorted(allG, key=lambda n: (int(n.split()[-1]), n)):
            if nm in w.out.nodes: continue
            par = allPar[nm]; Gp = allG[par] if par in allG else w.skel_G[par]
            w.out.add_node(nm, B.m2tb(np.linalg.inv(Gp) @ allG[nm]), w.out.nodes[par])
        made[0] = True
    nb, parts, prov, welded = {}, {}, {}, {}
    seg = lambda name, idx, keys=None: (np.array([name] * len(idx), object), np.array(keys if keys is not None else [None] * len(idx), object), np.asarray(idx, int))
    piece_of_src = defaultdict(list)
    for p in pieces: piece_of_src[p.src].append(p)
    emitted = set()
    # SoS: the men's shader blocks come from the frozen PG-patched copy of the mesh (same shape name), so the written meshes
    # carry PBR themselves (the men's mod outranks the PG output, which then writes no copy of them)
    donor = {}
    if g in ('m', 'v') and cfg.get('shader_donor'):
        if 'donor' not in shared:
            dn, DT = load(cfg['shader_donor']); shared['donor'] = (dn, {x.name: x for x in DT})
            miss = [t.name for t in T if t.name not in shared['donor'][1] and t.name != 'VirtualGround']
            if miss: raise RuntimeError(f'shader donor {cfg["shader_donor"]} lacks shapes {miss}')
            log.append(f'{g}: shaders from {cfg["shader_donor"].replace(HERE, "")} for ' + ', '.join(f'{t.name} ({shared["donor"][1][t.name].tex[0]})' for t in T if t.name != 'VirtualGround'))
        donor = shared['donor'][1]
    for t in T:
        if t.name == 'VirtualGround': continue
        dropped = t.name in cfg['drop']                   # v23: a dropped source shape still hands over its pieces (Elite Wolf:
        if dropped and not piece_of_src.get(t.name): continue   # the skirt is cut out of 'FurBase', whose leftover is dropped)
        partid = np.array(B.part_ids(t, T)); pws = {}            # v13: the pieces' final (seam-pinned) weights, filled with the remainder
        # the source shape's own remainder (women: Armor003 minus the cut pieces), then its pieces
        if not dropped and (t.name in rest or not piece_of_src.get(t.name)) and rest.get(t.name, np.ones(1, bool)).any():   # v5: never an empty remainder
            tm = rest.get(t.name, np.ones(len(t.tris), bool))
            v = np.unique(t.tris[tm]); rm = np.full(len(t.pos), -1); rm[v] = np.arange(len(v))
            ww = [B.top4(fold(t.w[i])) for i in v]
            P_o, UV_o, NR_o = t.pos[v], t.uv[v], (t.norm[v] if t.norm is not None else None); TR_o = rm[t.tris[tm]]; PID_o = list(partid[tm])
            COL_o = [tuple(t.s.colors[i]) for i in v] if t.s.colors else None; keys_o = [None] * len(v); idx_o = [int(i) for i in v]
            # v13: the pieces' seam midpoints welded into the remainder (see weld_seams) - the piece weights exactly as they are emitted below,
            # with the seam PINNED first: a piece point that IS a remainder vertex (same source index, or the same position after a cut that
            # made new points) takes the remainder's weights, so the two sides of the seam move as one (the Officer sash's seam row was off by
            # up to 0.09 from its own rig's belt fade - a crack of its own)
            pws.update({p.name: ([B.top4(x) for x in W[p.name]] if p.name in W else [B.top4(fold(x)) for x in p.ow]) for p in piece_of_src.get(t.name, [])})
            rvs = {int(i): k_ for k_, i in enumerate(v)}; RPv = t.pos[v]
            for p in piece_of_src.get(t.name, []):
                src_ = np.asarray(p.src_idx); pinned = 0
                for i_ in range(len(p.pos)):
                    s_ = int(src_[i_]) if i_ < len(src_) else -1
                    if s_ >= 0 and s_ in rvs: k_ = rvs[s_]
                    else:                                              # a UV-island seam (own vertices on the same positions) or a cut's new point
                        d_ = np.linalg.norm(RPv - p.pos[i_], axis=1); k_ = int(d_.argmin())
                        if d_[k_] > 1e-3: continue
                    if pws[p.name][i_] != ww[k_]: pws[p.name][i_] = dict(ww[k_]); pinned += 1
                if pinned: log.append(f'{g}: {p.name}: {pinned} seam points pinned to the remainder\'s weights')
            wl = weld_seams(t, tm, piece_of_src.get(t.name, []), pws, log, g)
            if wl:
                # split the remainder's boundary edge under each weld point (re-found on the CURRENT triangles, so two welds on one author
                # edge split it twice); the new vertex copies the piece point; origin[] remembers each triangle's source triangle
                TR = [[int(x) for x in tr] for tr in TR_o]; PID = list(PID_o); origin = list(range(len(TR)))
                P_l = [np.array(x, float) for x in P_o]; UV_l = [np.array(x, float) for x in UV_o]; NR_l = ([np.array(x, float) for x in NR_o] if NR_o is not None else None)
                placed, parents = 0, set()
                for wd in wl:
                    cnt, tri_of = {}, {}
                    for ti, (a, b, c) in enumerate(TR):
                        for u_, v_ in ((a, b), (b, c), (c, a)):
                            key = (min(u_, v_), max(u_, v_)); cnt[key] = cnt.get(key, 0) + 1; tri_of[key] = ti
                    bnd = [k_ for k_, c_ in cnt.items() if c_ == 1]
                    Aq = np.array([P_l[k_[0]] for k_ in bnd]); Bq = np.array([P_l[k_[1]] for k_ in bnd])
                    dq, tq = _seg_dist_t(wd['pos'][None], Aq, Bq); j = int(dq[0].argmin())
                    if dq[0, j] > 0.02: continue              # (a lifted or sloppy island vertex up to 0.02 off the edge is welded where it is)
                    u_, v_ = bnd[j]; ti = tri_of[bnd[j]]; tt = float(tq[0, j]); m = len(P_l)
                    # the weld's weights = the edge's own, blended along it (skeleton only: a seam row is pinned) - and the piece's point takes
                    # the same, so the two sides are identical (its own rig gave a midpoint just under the anchor a little physics share)
                    wb = {}
                    for bn, x in ww[u_].items(): wb[bn] = wb.get(bn, 0.0) + (1.0 - tt) * x
                    for bn, x in ww[v_].items(): wb[bn] = wb.get(bn, 0.0) + tt * x
                    wq = B.top4(wb); pws[wd['piece']][wd['k']] = dict(wq)
                    # 2026-10-13 (SoS Eastmarch, user screenshot: 'weird distortions on the plate armor just above the belt'): at a T-junction
                    # between two texture islands (the guards' plate tops on the coat's lower edge behind the belt) the piece's UV / normal
                    # belong to ITS island - copied into the remainder they stretched the coat's texture across the atlas over every
                    # triangle fanning to the weld (tools uv_smear: 14-72 smeared tris per coat, 0 in the author's meshes; the guards' at
                    # z 79, under the belt's top edge at 80, poked out as teeth). The remainder's weld takes ITS edge's UV and normal
                    # where the piece's differ; a subdivision midpoint on a shared island agrees within 0.002 and keeps the piece's (unchanged)
                    uv_e = (1.0 - tt) * np.asarray(UV_l[u_], float) + tt * np.asarray(UV_l[v_], float)
                    uv_w = wd['uv'] if np.abs(np.asarray(wd['uv'], float) - uv_e).max() <= 0.002 else uv_e
                    P_l.append(wd['pos']); UV_l.append(uv_w); ww.append(wq)
                    if NR_l is not None:
                        nr_e = (1.0 - tt) * NR_l[u_] + tt * NR_l[v_]; nr_e = nr_e / (np.linalg.norm(nr_e) + 1e-12)
                        nr_w = wd['nrm'] if (wd['nrm'] is not None and float(np.dot(wd['nrm'], nr_e)) > 0.9) else nr_e
                        NR_l.append(nr_w)
                    if COL_o is not None: COL_o.append(wd['col'] if wd['col'] is not None else COL_o[u_])
                    keys_o.append(('weld', int(u_), int(v_), tt)); idx_o.append(int(idx_o[u_]))     # slider data: along the edge (output indices, resolved in order)
                    tri = TR[ti]; TR[ti] = [m if x == v_ else x for x in tri]; TR.append([m if x == u_ else x for x in tri]); PID.append(PID[ti]); origin.append(origin[ti])
                    placed += 1; parents.add(origin[ti])
                P_o = np.array(P_l); UV_o = np.array(UV_l); NR_o = (np.array(NR_l) if NR_l is not None else None); TR_o = np.array(TR, int); PID_o = PID
                welded[t.name] = dict(points=placed, parents=len(parents))
                log.append(f'{g}: {t.name}: {placed} of {len(wl)} seam points welded into the remainder ({len(parents)} triangles split)')
            nb[t.name] = w.emit(t.name, P_o, UV_o, NR_o, TR_o, t.s.flags, PID_o, ww, t.s2b, shader_from=donor.get(t.name, t), colors=COL_o)
            if cfg.get('backing') and t.name == cfg['backing']['torso']: bk_torso_ = (t, P_o, UV_o, TR_o, ww, PID_o)     # 2026-10-14: the backing patch reads it
            ko = np.empty(len(keys_o), object)
            for i_, kk in enumerate(keys_o): ko[i_] = kk
            parts[t.name] = (len(P_o), len(TR_o)); prov[t.name] = (np.array([t.name] * len(idx_o), object), ko, np.asarray(idx_o, int))
        for p in piece_of_src.get(t.name, []):
            make_nodes()
            keys = [None if s >= 0 else 'split' for s in p.src_idx]
            ww = pws[p.name] if p.name in pws else ([B.top4(x) for x in W[p.name]] if p.name in W else [B.top4(fold(x)) for x in p.ow])   # v13: seam-pinned where a remainder exists
            nb[p.name] = w.emit(p.name, p.pos, p.uv, p.nrm, p.tris, t.s.flags, list(p.partid), ww, t.s2b, shader_from=donor.get(t.name, t),
                                colors=[tuple(c) for c in p.col] if p.col is not None else None,
                                double_sided=p.name in cfg.get('double_sided', ()))        # v18: see cfg['double_sided']
            parts[p.name] = (len(p.pos), len(p.tris)); prov[p.name] = ('piece', p)
    make_nodes()
    bk_ = cfg.get('backing')
    if bk_:
        # 2026-10-14 (SoS Eastmarch guards, user: the light tasset 'flipping up on a jump and showing undrawn parts'; Fable
        # tools/under_plate_drawn.py: behind the plates' top strip z 76-80 nothing is drawn - light 47 / 51 pts, heavy 51 / 51 + 21 / 122 at
        # z 72-76 - the author modelled that strip as the torso surface itself, so it is a hole in his mesh, not a cut of ours; the Officer's
        # plates end at 72.5): a STATIC backing behind the band - the plate piece's faces from z bk['zmin'] up (decided once on _1), moved
        # bk['depth'] in toward the body axis (the gap the lower bands keep over the mail / coat), with the coat body's shader, UVs and
        # weights read off its surface at those points (nearest triangle, barycentric; decided on _1, the same triangle + weights on _0)
        tp_ = next(p for lst in piece_of_src.values() for p in lst if p.name == bk_['piece']); ts_, TP_o, TUV_o, TTR_o, Tww_, TPID_ = bk_torso_
        if 'bk_sel' not in shared:
            ct_ = tp_.pos[tp_.tris].mean(1); shared['bk_sel'] = tp_.tris[ct_[:, 2] >= bk_['zmin']]
        tf_ = shared['bk_sel']; vv_ = np.unique(tf_); rm_ = np.full(len(tp_.pos), -1); rm_[vv_] = np.arange(len(vv_)); tt_ = rm_[tf_]
        rd_ = np.c_[tp_.pos[vv_, 0] - rig.cx, tp_.pos[vv_, 1] - rig.cy, np.zeros(len(vv_))]; rd_ /= np.linalg.norm(rd_, axis=1, keepdims=True) + 1e-12
        BP_ = tp_.pos[vv_] - float(bk_.get('depth', 3.0)) * rd_
        gr_ = float(bk_.get('grow', 1.0))
        if gr_ > 0:      # its boundary grown bk['grow'] along the patch (away from its island's centre, the radial part removed): the plate's own
            # edge rows otherwise graze the patch edge (first build: z 76-80 still 25 of 51 pts with nothing drawn behind them)
            ec_ = {}
            for a_, b_, c_ in tt_:
                for u_, v_ in ((a_, b_), (b_, c_), (c_, a_)): k_ = (min(u_, v_), max(u_, v_)); ec_[k_] = ec_.get(k_, 0) + 1
            bnd_ = np.array(sorted({x for k_, c_ in ec_.items() if c_ == 1 for x in k_}), int)
            lab_ = D.welded_components(BP_, tt_)
            for i_ in bnd_:
                cen_ = BP_[lab_ == lab_[i_]].mean(0); dv_ = BP_[i_] - cen_; dv_ -= (dv_ @ rd_[i_]) * rd_[i_]
                BP_[i_] = BP_[i_] + gr_ * dv_ / (np.linalg.norm(dv_) + 1e-12)
        if 'bk_map' not in shared:
            tri_, bary_, _, _ = B.Surface([('t', TP_o, TTR_o)]).query(BP_, k=8); shared['bk_map'] = (tri_, bary_)
        tri_, bary_ = shared['bk_map']; corn_ = TTR_o[tri_]
        BUV_ = (np.asarray(TUV_o, float)[corn_] * bary_[:, :, None]).sum(1)
        Bww_ = [Tww_[int(corn_[i][int(np.argmax(bary_[i]))])] for i in range(len(vv_))]
        BPID_ = [int(TPID_[int(tri_[tt_[j][0]])]) if len(TPID_) > int(tri_[tt_[j][0]]) else int(TPID_[0]) for j in range(len(tt_))]
        BN_ = K.vertex_normals(BP_, tt_)
        nm_ = N.added[0]
        nb[nm_] = w.emit(nm_, BP_, BUV_, BN_, tt_, ts_.s.flags, BPID_, Bww_, ts_.s2b, shader_from=donor.get(ts_.name, ts_), double_sided=True)
        parts[nm_] = (len(BP_), len(tt_))
        prov[nm_] = ('multi', [(tp_, vv_)])     # women: each patch point takes the slider data of the plate point it was offset from (the copies' rule)
        if first: log.append(f'{g}: backing patch {nm_}: {len(tt_)} faces of {tp_.name} above z {bk_["zmin"]:.1f} moved {bk_.get("depth", 3.0):.1f} in, '
                             f'{ts_.name}\'s shader / UVs / weights ({len(vv_)} pts)')
    tc_ = Dz.get('torso_coll')
    if tc_:          # v11 (helmets): the cuirass's outer surface above zmin as hidden per-triangle copies (one per source shape, the author's
        # winding, faces seen from a point low in the chest: out and up, never a collar's inside), skinned as the author did; PUBLIC in the XML
        # with a tag the Sons of Skyrim helmets' flap-skirt points name - so a veil rides over whichever cuirass is worn, from its own file
        zmin = float(tc_.get('zmin', 92.0)); ctr_t = np.array([rig.cx, rig.cy, zmin - 6.0]); tnames = []
        for t in T:
            if t.name == 'VirtualGround' or t.name in cfg['drop'] or t.name not in nb or any(s_ in t.name for s_ in tc_.get('skip', ('3BA', 'HIMBO', 'Body'))): continue
            tm = rest.get(t.name, np.ones(len(t.tris), bool))
            c = t.pos[t.tris].mean(1); fn = np.cross(t.pos[t.tris[:, 1]] - t.pos[t.tris[:, 0]], t.pos[t.tris[:, 2]] - t.pos[t.tris[:, 0]])
            dv = c - ctr_t; facing = (fn * dv).sum(1) / (np.linalg.norm(fn, axis=1) * np.linalg.norm(dv, axis=1) + 1e-12)
            kt_ = 'torso_sel_' + t.name
            if kt_ not in shared: shared[kt_] = tm & (c[:, 2] > zmin) & (facing > 0.05)      # decided once, on _1 (the _0 mesh faces differ a hair)
            sel = shared[kt_]
            if sel.sum() < 20: continue
            vv = np.unique(t.tris[sel]); rm = np.full(len(t.pos), -1); rm[vv] = np.arange(len(vv)); nm = N.TORSO[len(tnames)]
            nb[nm] = w.emit(nm, t.pos[vv], np.zeros((len(vv), 2)), None, rm[t.tris[sel]], 0xe, [32] * int(sel.sum()), [B.top4(fold(t.w[i])) for i in vv], t.s2b)
            parts[nm] = (len(vv), int(sel.sum())); prov[nm] = ('copy', t.name, vv); tnames.append(nm)
            if first: log.append(f'{g}: torso collider {nm}: {int(sel.sum())} of {t.name}\'s tris above z {zmin:.0f} facing out / up ({len(vv)} pts), for the helmets')
            if len(tnames) == len(N.TORSO): break
        if first: rig.torso_names = tnames
    # hidden colliders (v2c): the legs as three one-sided pieces by facing - front, back, sides - and the skirt lining in
    # three matching pieces by where it hangs. A front panel only ever meets the leg fronts, so however deep a fast
    # thigh goes into it, it is pushed back out in FRONT (a closed shell could push it out the side or back = hooked).
    sk_ = ('leg_sel', len(LP), len(LT))
    if sk_ not in shared:               # v7: decided once (on _1) per trousers mesh - per weight, faces near the limits switched piece
        fnl = np.cross(LP[LT[:, 1]] - LP[LT[:, 0]], LP[LT[:, 2]] - LP[LT[:, 0]]); fnl /= np.linalg.norm(fnl, axis=1, keepdims=True) + 1e-12
        leg_sel = {'Front': fnl[:, 1] > LEG_FACING, 'Back': fnl[:, 1] < -LEG_FACING, 'Side': np.abs(fnl[:, 0]) > SIDE_FACING}
        if cfg.get('front_no_inner'):       # v6: inner-thigh faces at the crotch push a front centre back between the legs
            fc = LP[LT].mean(1); inward = -np.sign(fc[:, 0] - rig.cx) * fnl[:, 0]
            leg_sel['Front'] = leg_sel['Front'] & (inward < 0.5)
        if cfg.get('legs_drop_infacing', Dz.get('legs_drop_infacing')):
            # 2026-10-14 (Reach guards, user: 'the left side of the armor clips into the pants at idle and during movement'): with the side
            # catch raised 1.5 -> 3.0 the verify rest test found side lining pts ~.5 OUTSIDE the drawn trousers sitting 1.6-2.8 BEHIND Legs
            # Side faces whose normals point INTO their own leg (+x on the left leg's outer side - the trousers' folds / inner layer wound
            # in; tools/side_rest.py): out of reach of the old 1.5 catch, inside the new one = pushed into the thigh every frame. A face
            # whose normal points toward its own leg's bone axis (hip-knee-ankle, as outward_fraction measures) by more than .2 leaves
            # every leg piece - a one-sided collider must only push OUT
            fc_ = LP[LT].mean(1); ax_ = leg_axes(pants, shared); dn_ = np.zeros(len(LT))
            for t_ in range(len(LT)):
                pl_ = ax_['L' if fc_[t_, 0] < 0 else 'R']; best_, bd_ = None, 1e9
                for a_, b_ in ((pl_[0], pl_[1]), (pl_[1], pl_[2])):
                    ab_ = b_ - a_; s_ = np.clip((fc_[t_] - a_) @ ab_ / (ab_ @ ab_), 0, 1); q_ = a_ + s_ * ab_; d_ = np.linalg.norm(fc_[t_] - q_)
                    if d_ < bd_: best_, bd_ = q_, d_
                r_ = fc_[t_] - best_; dn_[t_] = fnl[t_] @ (r_ / (np.linalg.norm(r_) + 1e-12))
            inf_ = dn_ < -0.2
            for k_ in leg_sel: leg_sel[k_] = leg_sel[k_] & ~inf_
            log.append(f'{g}: legs: {int(inf_.sum())} trouser faces facing into their own leg left out of the leg pieces (legs_drop_infacing)')
        shared[sk_] = leg_sel
    leg_sel = shared[sk_]
    for side, m in leg_sel.items():
        tt = LT[m]; vv = np.unique(tt); rm = np.full(len(LP), -1); rm[vv] = np.arange(len(vv)); nm = N.legc(side)
        nb[nm] = w.emit(nm, LP[vv], np.zeros((len(vv), 2)), None, rm[tt], 0xe, [32] * len(tt), [B.top4(pants.w[lv[i]]) for i in vv], pants.s2b)
        parts[nm] = (len(vv), len(tt)); prov[nm] = ('copy', pants.name, getattr(pants, 'src_map', np.arange(len(pants.pos)))[lv[vv]])
    if cfg.get('boot_coll') and ('boot_band_' + variant) in shared:     # 2026-10-14: the boot cuff's outer band (boot_band), skinned as the boot is
        bb_ = shared['boot_band_' + variant]
        nb[N.BOOT] = w.emit(N.BOOT, bb_.pos, np.zeros((len(bb_.pos), 2)), None, bb_.tris, 0xe, [32] * len(bb_.tris), [B.top4(x) for x in bb_.w], bb_.s2b)
        parts[N.BOOT] = (len(bb_.pos), len(bb_.tris))
    for side in N.SIDES:
        LPts, LTris, LW = [], [], []; off = 0; lin_prov = []
        for p, it, v in lin:
            kv = keep[p.name]
            if ('lin_reg', p.name) not in shared:     # v7: decided once (on _1) - per weight, points near 55 deg could switch piece
                a_ = np.array([rig.ang(x) for x in p.pos[kv]])
                shared[('lin_reg', p.name)] = np.where(np.abs(wrap(a_)) < FRONT_DEG, 'Front', np.where(np.abs(wrap(a_ - 180.0)) < FRONT_DEG, 'Back', 'Side'))
            reg = shared[('lin_reg', p.name)]
            kv = kv[reg == side]
            if not len(kv): continue
            rm = np.full(len(p.pos), -1); rm[kv] = np.arange(len(kv)); kt = p.tris[it]; kt = kt[(rm[kt] >= 0).all(1)]
            if not len(kt) and cfg.get('lining_all'):      # SoS Officer v2: source points only - their own (the author's) triangles
                kt = coarse_tris(p); kt = kt[(rm[kt] >= 0).all(1)]
            LPts.append(p.pos[kv]); LTris.append(rm[kt] + off); LW += [B.top4(W[p.name][i]) for i in kv]; off += len(kv); lin_prov.append((p, kv))
        nm = N.skc(side)
        TT = np.vstack(LTris) if any(len(x) for x in LTris) else np.zeros((0, 3), int)
        nb[nm] = w.emit(nm, np.vstack(LPts), np.zeros((off, 2)), None, TT, 0xe, [32] * max(len(TT), 1) if len(TT) else [], LW, S[skirts[0].src].s2b)
        parts[nm] = (off, len(TT)); prov[nm] = ('multi', lin_prov)
    lin_sides = {}
    for p, it, v, gw_, rg in glin:                # SoS Officer v2: each extra layer's own lining colliders, split by facing
        kv0 = keep[p.name]
        if ('lin_reg', p.name) not in shared:
            a_ = np.array([rg.ang(x) for x in p.pos[kv0]])
            shared[('lin_reg', p.name)] = np.where(np.abs(wrap(a_)) < FRONT_DEG, 'Front', np.where(np.abs(wrap(a_ - 180.0)) < FRONT_DEG, 'Back', 'Side'))
        reg = shared[('lin_reg', p.name)]; lin_sides[gw_] = []
        for side in N.SIDES:
            kv = kv0[reg == side]
            if not len(kv): continue
            rm = np.full(len(p.pos), -1); rm[kv] = np.arange(len(kv)); kt = p.tris[it]; kt = rm[kt[(rm[kt] >= 0).all(1)]]
            if not len(kt): kt = coarse_tris(p); kt = rm[kt[(rm[kt] >= 0).all(1)]]
            if not len(kt): continue
            nm = GroupNames(N, gw_).skc(side)
            nb[nm] = w.emit(nm, p.pos[kv], np.zeros((len(kv), 2)), None, kt, 0xe, [32] * len(kt), [B.top4(W[p.name][i]) for i in kv], S[p.src].s2b)
            parts[nm] = (len(kv), len(kt)); prov[nm] = ('multi', [(p, kv)]); lin_sides[gw_].append(side)
    for nm_, (sp, v_, TT_, PP_) in LCOLL.items():     # SoS Officer v2: the colliders between the layers
        nm = f'{N.p} {nm_}'
        nb[nm] = w.emit(nm, PP_, np.zeros((len(PP_), 2)), None, TT_, 0xe, [32] * len(TT_), [B.top4(W[sp.name][i]) for i in v_], S[sp.src].s2b)
        parts[nm] = (len(PP_), len(TT_)); prov[nm] = ('multi', [(sp, v_)])
    if first:
        rig.groups = shared.get('rigs', {}); rig.lin_sides = lin_sides; rig.lcoll = list(LCOLL)
    if len(SKOT):
        nb[N.SKO] = w.emit(N.SKO, SKOP, np.zeros((len(SKOP), 2)), None, SKOT, 0xe, [32] * len(SKOT), [B.top4(W[out_p.name][i]) for i in sko_v], S[out_p.src].s2b)
        parts[N.SKO] = (len(SKOP), len(SKOT)); prov[N.SKO] = ('multi', [(out_p, sko_v)])
    if len(TIPUT):
        nb[N.TIPU] = w.emit(N.TIPU, TIPUP, np.zeros((len(TIPUP), 2)), None, TIPUT, 0xe, [32] * len(TIPUT),
                            [B.top4(W[q.name][i]) for q, v in tipu_parts for i in v], S[out_p.src].s2b)
        parts[N.TIPU] = (len(TIPUP), len(TIPUT)); prov[N.TIPU] = ('multi', tipu_parts)
    if len(HANGUT):                                 # v11: the hip hangers' copy of the layers under them
        nb[N.HANGU] = w.emit(N.HANGU, HANGUP, np.zeros((len(HANGUP), 2)), None, HANGUT, 0xe, [32] * len(HANGUT),
                             [B.top4(W[q.name][i]) for q, v in hangu_parts for i in v], S[out_p.src].s2b)
        parts[N.HANGU] = (len(HANGUP), len(HANGUT)); prov[N.HANGU] = ('multi', hangu_parts)
    if len(FLAPUT):                                 # 2026-10-14 HOLDS: the hip strap's copy (the cuirass part keeps the cuirass's own weights)
        s2b_f = {}
        for q, _ in flapu_parts: s2b_f.update(S[q.src].s2b)
        nb[N.FLAPU] = w.emit(N.FLAPU, FLAPUP, np.zeros((len(FLAPUP), 2)), None, FLAPUT, 0xe, [32] * len(FLAPUT),
                             [B.top4(W[q.name][i] if q.name in W and q.role != 'cuirass' else fold(q.ow[i])) for q, v in flapu_parts for i in v], s2b_f)
        parts[N.FLAPU] = (len(FLAPUP), len(FLAPUT)); prov[N.FLAPU] = ('multi', flapu_parts)
    for key, (tp_, tv_, uparts, UT_, UP_) in TAILC.items():       # SoS: the tails' skirt copies + points (v3: a copy may span several layers)
        if len(UT_):
            nm = N.tailu(key); s2b_u = {}
            for q, _ in uparts: s2b_u.update(S[q.src].s2b)
            nb[nm] = w.emit(nm, UP_, np.zeros((len(UP_), 2)), None, UT_, 0xe, [32] * len(UT_), [B.top4(W[q.name][i]) for q, sel in uparts for i in sel], s2b_u)
            parts[nm] = (len(UP_), len(UT_)); prov[nm] = ('multi', uparts)
        nm = N.tailc(key); rm = np.full(len(tp_.pos), -1); rm[tv_] = np.arange(len(tv_)); ct = tp_.tris[(rm[tp_.tris] >= 0).all(1)]
        nb[nm] = w.emit(nm, tp_.pos[tv_], np.zeros((len(tv_), 2)), None, rm[ct], 0xe, [32] * len(ct), [B.top4(W[tp_.name][i]) for i in tv_], S[tp_.src].s2b)
        parts[nm] = (len(tv_), len(ct)); prov[nm] = ('multi', [(tp_, tv_)])
    for nm, p, idx in ([(N.FLP, flaps, FLV)] if flaps is not None else []) + ([(N.TIPC, belt, TIPV)] if len(TIPV) else []) + ([(N.BAGC, belt, BAGV)] if len(BAGV) else []) \
            + ([(N.HANGC, belt, HANGP)] if len(HANGUT) else []):      # v11: the hangers' points (rings + straps); 2026-10-13 PERF: the proxy
        rm = np.full(len(p.pos), -1); rm[idx] = np.arange(len(idx)); ct = p.tris[(rm[p.tris] >= 0).all(1)]
        nb[nm] = w.emit(nm, p.pos[idx], np.zeros((len(idx), 2)), None, rm[ct], 0xe, [32] * len(ct), [B.top4(W[p.name][i]) for i in idx], S[p.src].s2b)
        parts[nm] = (len(idx), len(ct)); prov[nm] = ('multi', [(p, idx)])
    if flaps is not None and len(FLOT):
        nb[N.FLO] = w.emit(N.FLO, FLOP, np.zeros((len(FLOP), 2)), None, FLOT, 0xe, [32] * len(FLOT), [B.top4(W[flaps.name][i]) for i in flo_v], S[flaps.src].s2b)
        parts[N.FLO] = (len(FLOP), len(FLOT)); prov[N.FLO] = ('multi', [(flaps, flo_v)])
    if 'VirtualGround' in S:
        gr = S['VirtualGround']
        nb['VirtualGround'] = w.emit('VirtualGround', gr.pos, gr.uv, None, gr.tris, gr.s.flags, list(B.part_ids(gr, T)), [B.top4(x) for x in gr.w], gr.s2b)
    else:
        GV = np.array([[-80.0, 80.0, 0.0], [-80.0, -80.0, 0.0], [80.0, 80.0, 0.0], [80.0, -80.0, 0.0]]); GF = np.array([[0, 1, 2], [2, 1, 3]])
        if np.cross(GV[GF[0, 1]] - GV[GF[0, 0]], GV[GF[0, 2]] - GV[GF[0, 0]])[2] < 0: GF = GF[:, [0, 2, 1]]
        nb['VirtualGround'] = w.emit('VirtualGround', GV, np.zeros((4, 2)), None, GF, 0x8000e, [32, 32], [{ROOT: 1.0}] * 4, {})
    parts['VirtualGround'] = (4, 2)
    NiStringExtraData.New(w.out, name='HDT Skinned Mesh Physics Object', string_value=cfg['xml'], parent=w.out.root)
    w.out.save()
    for k_, b in nb.items():
        if b > R.MAXB: raise RuntimeError(f'{k_}: {b} bones')
    log.append(f'{g}_{variant}: wrote {out.replace(STAGE, "")}; shapes (pts, tris) {parts}; bones per shape {nb}')
    if rec is not None: rec.update(prov=prov, parts=parts, T=T, welded=welded)
    return out


# ------------------------------------------------------------------ XML
SK_DEF = dict(mass=1.0, inertia=40.0, lin=0.4, ang=0.6, friction=0.1, wind=0.15)       # v2 'more oomph' (v1 = Wolf v4: inertia 55, damping .5/.7, wind .1)
TIP_DEF = dict(mass=0.8, inertia=14.0, lin=0.3, ang=0.45, friction=0.0, wind=0.0, gravity=0.5)  # Sir Duncan belt tail; v12 (own chain again, 'barely moving'): quicker - inertia 21 -> 14, damping .53 -> .45, gravity back to .5 (in-limit 0 holds it off the skirt)
FLAP_DEF = dict(mass=1.2, inertia=20.0, lin=0.4, ang=0.6, friction=0.1, wind=0.0)      # riveted iron plate (v2 quicker: v1 1.5 / 30 / .7)
SK_LIM1 = dict(lo=(-0.85, -0.12, -0.05), hi=(0.25, 0.12, 0.05), lin=0.0, stiff=(150, 50, 50))     # v2: out .75 -> .85, springs 200 -> 150
SK_LIM = dict(lo=(-0.45, -0.08, -0.05), hi=(0.25, 0.08, 0.05), lin=0.0, stiff=(90, 30, 30))       # v2: springs 120 -> 90
TIP_LIM = dict(lo=(-0.55, -0.2, -0.12), hi=(0.0, 0.2, 0.12), lin=0.0, astiff=70)    # v6 springs 100 -> 130; v12: 70, out .4 -> .55, sideways .15 -> .2 (Duncan's 100 / .4 / .15 with a bit more life; never in past the drawn line)
FLAP_LIM = dict(lo=(-0.9, -0.12, -0.1), hi=(0.05, 0.12, 0.1), lin=0.05, astiff=60)


HANG_DEF = dict(mass=0.4, inertia=2.0, lin=0.35, ang=0.4, friction=0.0, wind=0.0, gravity=1.0)        # v10 (Officer): the hip hanger strap slung between its rings
HANG_RING_DEF = dict(mass=0.3, inertia=1.0, lin=0.3, ang=0.35, friction=0.0, wind=0.0, gravity=1.0)   # the rings: small pendulums on their leather loops
HANG_MIN_RADIAL = 0.5       # v11: the hanger copy keeps only faces facing out this much (the Officer v4 lesson: edge faces push a strap sideways)
HANG_LIM = dict(lo=(-0.25, -0.2, -0.08), hi=(0.03, 0.2, 0.08), lin=0.0, astiff=4)        # strap joints: flap out, a hair in (the band is behind it), sag up / down, no fore / aft
HANG_RING_LIM = dict(lo=(-0.3, -0.25, -0.1), hi=(0.03, 0.25, 0.1), lin=0.0, astiff=3)   # a ring on its loop: out, fore / aft, a little twist


def group_sectors(rg, gc_):
    # v10: [(sector or None, [chain k ...])] - chains within a sector's half-width of its centre angle take that sector's physics
    secs = gc_.get('sectors', []); out = [(None, [])] + [(s_, []) for s_ in secs]
    for k, a in enumerate(rg.ang_k):
        si = next((i for i, s_ in enumerate(secs) if abs(float(wrap(a - s_['centre']))) <= s_['half']), None)
        out[0 if si is None else si + 1][1].append(k)
    return [(s_, ks) for s_, ks in out if ks]


def write_xml(design, g, rig, skel, has_flo, log):
    Dz = DESIGNS[design]; cfg = Dz[g]; N = Names(Dz['prefix']); shape = K.shape
    nk = len(rig.ang_k); nfl = rig.nfl; has_tip = bool(rig.tip_rows)
    ph = Dz.get('phys', {})
    SK_DEF_, SK_LIM1_, SK_LIM_ = ph.get('SK_DEF', SK_DEF), ph.get('SK_LIM1', SK_LIM1), ph.get('SK_LIM', SK_LIM)
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<!-- Realistic Armor - {Dz["title"]}, {"men" if g == "m" else "women (vanilla body)" if g == "v" else "women (3BA BodySlide set " + chr(34) + cfg["set"] + chr(34) + ")"}: skirt, hip flaps and belt tip physics,',
         '     rebuilt 2026-10-08 for this LoreRim setup (replaces the HDT patch\'s 8x3 panels; skirt feel after Companions Wolf Armor Redone v4).',
         f'     Skirt: {nk} chains (pinned under the belt + {rig.nrow} swinging bones), every point blending two chains and two rows; ' +
         ('the halves part at the slits below each layer\'s slit top.' if rig.slits else 'one piece all round.'),
         ('     All skirt layers hang on the same chains, so they never fight each other. Where the skirt lies on the thighs it moves with' if not getattr(rig, 'groups', {}) else
          f'     Layers on chains of their own: {Dz["phys_note"] if "phys_note" in Dz else ", ".join(["the main skirt"] + [w_.lower() for w_ in rig.groups])}; colliders keep each over or under the next. Where a layer lies on the thighs it moves with'),
         '     them; where it hangs clear it swings.' + (' Hip flaps: iron plates on their own hinged bones, following the skirt under them.' if nfl else '')
         + (' Bag: its own bone hinged at the belt.' if rig.has_bag else '') + (' Belt tip: its own 3-bone strap.' if has_tip else ''),
         '     Collisions (hidden copies, this armour only): the skirt vs the trousers, split into front / side / back so a leg always',
         '     pushes the skirt back out the way it came; ' + ', '.join([x for x, on in (('flaps', nfl), ('bag', rig.has_bag)) if on]) +
         (' vs the skirt\'s outer surface and the trousers' + (' (the flaps: front-facing pieces only)' if nfl and Dz.get('flap_legs') else '') + '; ' if (nfl or rig.has_bag) else '') +
         ('the belt tip (its own chain) vs the skirt\'s outer surface only; ' if (has_tip and cfg.get('tip_collide', Dz.get('tip_collide', False))) else '') + 'ground.',
         '     Nothing touches anything while standing. Swing limits per joint: X = out/in (negative = outward), Y = sideways, Z = twist.',
         '     Tuning: edit, save, "smp reset". -->',
         '<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="description.xsd">', '']
    L += shape('per-triangle-shape', N.GROUND, 'ground', 0.5, no=('ground', 'legsF', 'legsS', 'legsB'), pen=10)
    L += ['\t<!-- the trousers (hidden copies) in three one-sided pieces by facing: front, back, sides. Each part of the skirt meets only',
          '\t     the matching piece, so a leg that goes deep into it always pushes it back out the way it came, never hooks it behind the leg -->']
    legs_no = ('legsF', 'legsS', 'legsB', 'ground')
    lp_ = dict(Front=3.0, Back=3.0, Side=1.5); lp_.update(cfg.get('leg_pen', Dz.get('leg_pen', {})))   # v6 (Officer): deeper catches - combat left the mail inside a leg
    L += shape('per-triangle-shape', N.legc('Front'), 'legsF', 0.4, no=legs_no, pen=lp_['Front'])
    L += shape('per-triangle-shape', N.legc('Back'), 'legsB', 0.4, no=legs_no, pen=lp_['Back'])
    L += shape('per-triangle-shape', N.legc('Side'), 'legsS', 0.4, no=legs_no, pen=lp_['Side'])
    L += ['', '\t<!-- kinematic: skeleton bones the collision shapes are skinned to, and the pinned top bone of every chain -->']
    L += [f'\t<bone name="{b}"/>' for b in skel]
    L += [f'\t<bone name="{N.sk(k, 0)}"/>' for k in range(nk)] + ([f'\t<bone name="{N.tip(0)}"/>'] if has_tip else []) + [f'\t<bone name="{N.flap(k, 0)}"/>' for k in range(nfl)]
    if rig.has_bag: L += [f'\t<bone name="{N.bag(0)}"/>']
    for k, hg in enumerate(getattr(rig, 'hangers', [])): L += [f'\t<bone name="{N.hang(k, 0)}"/>', f'\t<bone name="{N.hang(k, hg["n"] + 2)}"/>']   # v10: the hangers' anchors at their loops
    L += [f'\t<bone name="{N.tail(k_, 0)}"/>' for k_ in getattr(rig, 'tails', {})]     # SoS: tail anchors (v7: still declared when the chain hangs from a plate's bone - the node exists; nothing uses it)
    GR = getattr(rig, 'groups', {})               # SoS Officer v2: the extra layers' pinned top bones
    for gw_, rg in GR.items(): L += [f'\t<bone name="{GroupNames(N, gw_).sk(k, 0)}"/>' for k in range(len(rg.ang_k))]
    FR = ph.get('FRONT')                          # v23 (Elite Wolf): the chains over the front strips get their own bodies and limits
    front = [k for k, a in enumerate(rig.ang_k) if abs(wrap(a)) <= FR['hw']] if FR else []
    rest_k = [k for k in range(nk) if k not in front]
    L += [''] + D.bone_default(SK_DEF_, 'skirt: heavy cloth / mail that swings in and out but settles')
    for r in range(1, rig.nrow + 1): L += [f'\t<bone name="{N.sk(k, r)}"/>' for k in rest_k]
    if front:
        L += [''] + D.bone_default(FR['SK_DEF'], f'front strips (chains at {" ".join(f"{rig.ang_k[k]:.0f}" for k in front)} deg): hinged leather hanging over the thighs, no friction so a knee slides under')
        for r in range(1, rig.nrow + 1): L += [f'\t<bone name="{N.sk(k, r)}"/>' for k in front]
    if nfl:
        L += [''] + D.bone_default(Dz.get('flap_def', FLAP_DEF), Dz.get('flap_note', 'hip flaps: riveted iron plates - heavy, slow, no wind'))
        L += [f'\t<bone name="{N.flap(k, 1)}"/>' for k in range(nfl)]
    if rig.has_bag:
        L += [''] + D.bone_default(Dz.get('bag_def', K.BAG_DEF), 'bag: light, swings on its hinge, damped so it settles when you stop')
        L += [f'\t<bone name="{N.bag(1)}"/>']
    if has_tip:
        L += [''] + D.bone_default(Dz.get('tip_def', TIP_DEF), 'belt tip: leather strap (Sir Duncan belt tail)')
        L += [f'\t<bone name="{N.tip(r)}"/>' for r in range(1, TIP_N + 1)]
    HG_ = getattr(rig, 'hangers', [])
    if HG_:                                       # v10: the hip hangers
        L += [''] + D.bone_default(Dz.get('hang_ring_def', HANG_RING_DEF), 'hip hanger rings: each a small pendulum on its leather loop over the belt')
        L += [f'\t<bone name="{N.hang(k, j)}"/>' for k, hg in enumerate(HG_) for j in (1, hg['n'] + 3)]
        L += [''] + D.bone_default(Dz.get('hang_def', HANG_DEF), 'hip hanger straps: leather slung between the two rings - flaps out and sags on a step')
        L += [f'\t<bone name="{N.hang(k, 2 + j)}"/>' for k, hg in enumerate(HG_) for j in range(hg['n'])]
    for k_ in getattr(rig, 'tails', {}):           # SoS: the sash end
        n_ = rig.tails[k_].get('n', SASH_N)
        # 2026-10-13 (SoS Winterhold: a bag and a canteen, both rigid tails, pivot-to-centre 6.6 vs 14): 'tail_def' {piece name: bone values}
        # overrides sash_def for that tail - one recipe, inertia scaled by length squared per piece; the limits stay shared
        L += [''] + D.bone_default(Dz.get('tail_def', {}).get(k_, Dz.get('sash_def', SASH_DEF)), f'{k_.lower()}: a RIGID bag - one body on its hinge at the top, everything below its strap on that one bone'
                                   if rig.tails[k_].get('rigid') else f'{k_.lower()} end: cloth - very light, the wind takes it, its own {n_}-bone chain')
        L += [f'\t<bone name="{N.tail(k_, r)}"/>' for r in range(1, n_ + 1)]
    for gw_, rg in GR.items():                    # SoS Officer v2: each extra layer's own swinging bones (v10: per sector)
        gc_ = cfg['groups'][gw_]; GN_ = GroupNames(N, gw_)
        for sec_, ks_ in group_sectors(rg, gc_):
            ph_ = sec_['phys'] if sec_ else gc_['phys']
            L += [''] + D.bone_default(ph_['SK_DEF'], f'{gw_.lower()} layer' + (f', {sec_["name"]} sector ({sec_.get("note", "")}): chains at {" ".join(f"{rg.ang_k[k]:.0f}" for k in ks_)} deg' if sec_ else
                                                       f': {gc_.get("note", "")} - its own {len(rg.ang_k)} chains x {rg.nrow} bones'))
            for r in range(1, rg.nrow + 1): L += [f'\t<bone name="{GN_.sk(k, r)}"/>' for k in ks_]
    L += BW.chain_default_xyz(SK_LIM1_, f'skirt, first joint under the belt: out up to {-SK_LIM1_["lo"][0]} rad, in {SK_LIM1_["hi"][0]} (onto the legs), sideways {SK_LIM1_["hi"][1]}, twist {SK_LIM1_["hi"][2]}; springs hold the shape and calm the sway')
    L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.sk(k, 1)}" bodyB="{N.sk(k, 0)}"/>' for k in rest_k]; L.append('\t</constraint-group>')
    if front:                                     # v23: the front strips' first joint (Wolf Armor Redone flap: out 1.2 so a raised knee lifts them)
        F1 = FR['SK_LIM1']
        L += BW.chain_default_xyz(F1, f'front strips, first joint under the belt: out up to {-F1["lo"][0]} rad (a raised knee lifts them), back {F1["hi"][0]}, sideways {F1["hi"][1]}, twist {F1["hi"][2]}; weak out-spring, strong sideways')
        L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.sk(k, 1)}" bodyB="{N.sk(k, 0)}"/>' for k in front]; L.append('\t</constraint-group>')
    L += BW.chain_default_xyz(SK_LIM_, f'skirt, further down: out up to {-SK_LIM_["lo"][0]} rad per joint, in {SK_LIM_["hi"][0]}, sideways {SK_LIM_["hi"][1]}, twist {SK_LIM_["hi"][2]}; lighter springs')
    SK_LOW_ = ph.get('SK_LIM_LOW'); r_mid = range(2, LOW_FROM if SK_LOW_ else rig.nrow + 1)
    for k in rest_k:
        L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.sk(k, r)}" bodyB="{N.sk(k, r - 1)}"/>' for r in r_mid]; L.append('\t</constraint-group>')
    if front:
        F2 = FR['SK_LIM']
        L += BW.chain_default_xyz(F2, f'front strips, further down: out up to {-F2["lo"][0]} rad per joint, back {F2["hi"][0]}, sideways {F2["hi"][1]}, twist {F2["hi"][2]}')
        for k in front:
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.sk(k, r)}" bodyB="{N.sk(k, r - 1)}"/>' for r in range(2, rig.nrow + 1)]; L.append('\t</constraint-group>')
    if SK_LOW_:                                   # v13: the hem rows freer (Dawnguard's lowest bones)
        L += BW.chain_default_xyz(SK_LOW_, f'skirt, the hem rows: out up to {-SK_LOW_["lo"][0]} rad per joint, in {SK_LOW_["hi"][0]}, sideways {SK_LOW_["hi"][1]}, twist {SK_LOW_["hi"][2]}; almost no springs - it flows')
        for k in rest_k:
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.sk(k, r)}" bodyB="{N.sk(k, r - 1)}"/>' for r in range(LOW_FROM, rig.nrow + 1)]; L.append('\t</constraint-group>')
    lk_ = ph.get('LINK', (0.25, 0.3))
    L += D.link_default(lk_[0], lk_[1], 'skirt, round the body: neighbouring chains stay one piece (across a slit only above the slit)' +
                        (f' - loosely (+-{lk_[0]} / +-{lk_[1]} rad), so the panels flow on their own' if 'LINK' in ph else ''))
    links = []
    base = 0
    for pi, p in enumerate(rig.panels):
        for i in range(len(p) - 1): links.append((base + i, base + i + 1, None))
        base += len(p)
    if rig.slits:
        for si in range(len(rig.slits)):
            right = si; left = (si - 1) % len(rig.panels)
            k_hi = sum(len(q) for q in rig.panels[:right]); k_lo = sum(len(q) for q in rig.panels[:left]) + len(rig.panels[left]) - 1
            top = max(rig.tops[l][si] for l in rig.tops)           # linked only where every layer is closed
            links.append((k_lo, k_hi, top))
    else:
        links.append((nk - 1, 0, None))
    for r in range(1, rig.nrow + 1):
        L.append('\t<constraint-group>')
        for a, b, top in links:
            if top is None or min(rig.rows[a][r], rig.rows[b][r]) > top + 1.0:
                L.append(f'\t\t<generic-constraint bodyA="{N.sk(b, r)}" bodyB="{N.sk(a, r)}"/>')
        L.append('\t</constraint-group>')
    if nfl:
        FL_ = Dz.get('flap_lim', FLAP_LIM)
        L += D.chain_default(FL_, f'hip flaps: hinge at the top edge - swing out up to {-FL_["lo"][0]} rad, in {FL_["hi"][0]}, sideways {FL_["hi"][1]}, twist {FL_["hi"][2]}; springs {FL_["astiff"]} bring them back')
        L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.flap(k, 1)}" bodyB="{N.flap(k, 0)}"/>' for k in range(nfl)]; L.append('\t</constraint-group>')
    if rig.has_bag:
        BL_ = Dz.get('bag_lim', K.BAG_LIM)
        L += D.chain_default(BL_, f'bag: swings out {-BL_["lo"][0]} rad, barely in (it hangs against the hip), sideways {BL_["hi"][1]}, twist {BL_["hi"][2]}; light springs bring it back')
        L += ['\t<constraint-group>', f'\t\t<generic-constraint bodyA="{N.bag(1)}" bodyB="{N.bag(0)}"/>', '\t</constraint-group>']
    if has_tip:
        TL_ = Dz.get('tip_lim', TIP_LIM)
        TL2_ = Dz.get('tip_lim2')        # v7 (Officer): the lower joints stiffer - a leather strap pushed in the middle pivots at the top, it does not kink
        th_ = getattr(rig, 'tip_hang', None)       # 2026-10-13 tip_hang_on='skirt': the first joint on the skirt chain under the strap
        L += D.chain_default(TL_, f'belt tip (Sir Duncan belt, a bit livelier): swings out {-TL_["lo"][0]} rad per joint, never in past its drawn shape, sideways {TL_["hi"][1]}; springs hold the drawn shape'
                             + (f'; its first joint hangs from {th_} - the skirt carries it wherever the thighs drive the skirt' if th_ else ''))
        L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.tip(r)}" bodyB="{th_ if (th_ and r == 1) else N.tip(r - 1)}"/>' for r in range(1, (2 if TL2_ else TIP_N + 1))]; L.append('\t</constraint-group>')
        if TL2_:
            L += D.chain_default(TL2_, f'belt tip, lower joints: out up to {-TL2_["lo"][0]} rad, sideways {TL2_["hi"][1]} - the strap bends at the top, not in the middle')
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.tip(r)}" bodyB="{N.tip(r - 1)}"/>' for r in range(2, TIP_N + 1)]; L.append('\t</constraint-group>')
    if HG_:                                       # v10: the hip hangers' joints
        RL_ = Dz.get('hang_ring_lim', HANG_RING_LIM); SL_ = Dz.get('hang_lim', HANG_LIM)
        L += D.chain_default(RL_, f'hip hanger rings on their loops: out {-RL_["lo"][0]} rad, in {RL_["hi"][0]}, fore / aft {RL_["hi"][1]}, twist {RL_["hi"][2]}, springs {RL_["astiff"]}')
        L.append('\t<constraint-group>')
        L += [f'\t\t<generic-constraint bodyA="{N.hang(k, 1)}" bodyB="{N.hang(k, 0)}"/>' for k in range(len(HG_))]
        L += [f'\t\t<generic-constraint bodyA="{N.hang(k, hg["n"] + 3)}" bodyB="{N.hang(k, hg["n"] + 2)}"/>' for k, hg in enumerate(HG_)]
        L.append('\t</constraint-group>')
        L += D.chain_default(SL_, f'hip hanger straps, joint by joint from the front ring to the back ring (the last joint closes on the back ring): out {-SL_["lo"][0]} rad, in {SL_["hi"][0]}, up / down {SL_["hi"][1]}, fore / aft {SL_["hi"][2]}, springs {SL_["astiff"]}')
        L.append('\t<constraint-group>')
        for k, hg in enumerate(HG_):
            L += [f'\t\t<generic-constraint bodyA="{N.hang(k, 2 + j)}" bodyB="{N.hang(k, 1 + j)}"/>' for j in range(hg['n'])]
            L += [f'\t\t<generic-constraint bodyA="{N.hang(k, hg["n"] + 1)}" bodyB="{N.hang(k, hg["n"] + 3)}"/>']
        L.append('\t</constraint-group>')
    for k_ in getattr(rig, 'tails', {}):           # SoS: the sash end's joints (summed out-limits under 90 deg)
        S1, S2 = Dz.get('sash_lim', SASH_LIM), Dz.get('sash_lim2', SASH_LIM2)
        hs_ = rig.tails[k_].get('hang')            # 2026-10-13 tail_hang_on='skirt': the joint on the main skirt chain under it
        L += D.chain_default(S1, f'{k_.lower()} end, first joint: out up to {-S1["lo"][0]} rad, never in past its drawn line, sideways {S1["hi"][1]}, twist {S1["hi"][2]}, springs {S1["astiff"]}'
                             + (f'; hangs from {hs_} - the skirt carries it wherever the thighs drive the skirt' if hs_ else ''))
        rb_ = rig.tails[k_].get('root', PELV); rb_ = N.tail(k_, 0) if rb_ == PELV else rb_; n_ = rig.tails[k_].get('n', SASH_N)
        rb_ = hs_ or rb_
        L += ['\t<constraint-group>', f'\t\t<generic-constraint bodyA="{N.tail(k_, 1)}" bodyB="{rb_}"/>', '\t</constraint-group>']
        L += D.chain_default(S2, f'{k_.lower()} end, further down: out up to {-S2["lo"][0]} rad per joint, sideways {S2["hi"][1]}, twist {S2["hi"][2]}, springs {S2["astiff"]}')
        L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{N.tail(k_, r)}" bodyB="{N.tail(k_, r - 1)}"/>' for r in range(2, n_ + 1)]; L.append('\t</constraint-group>')
    for gw_, rg in GR.items():                    # SoS Officer v2: each extra layer's joints and its ring links (none across its slits)
        gph = cfg['groups'][gw_]['phys']; GN_ = GroupNames(N, gw_); tg_ = gw_.lower(); nkg, nr = len(rg.ang_k), rg.nrow
        for sec_, ks_ in group_sectors(rg, cfg['groups'][gw_]):          # v10: per sector (the Officer's back plate bounces on its own values)
            ph_ = sec_['phys'] if sec_ else gph; G1, G2, GLOW = ph_['SK_LIM1'], ph_['SK_LIM'], ph_.get('SK_LIM_LOW'); sn_ = f', {sec_["name"]} sector' if sec_ else ''
            L += BW.chain_default_xyz(G1, f'{tg_} layer{sn_}, first joint: out up to {-G1["lo"][0]} rad, in {G1["hi"][0]}, sideways {G1["hi"][1]}, twist {G1["hi"][2]}')
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{GN_.sk(k, 1)}" bodyB="{GN_.sk(k, 0)}"/>' for k in ks_]; L.append('\t</constraint-group>')
            r_mid = list(range(2, (LOW_FROM if GLOW else nr + 1)))
            if r_mid:
                L += BW.chain_default_xyz(G2, f'{tg_} layer{sn_}, further down: out up to {-G2["lo"][0]} rad per joint, in {G2["hi"][0]}, sideways {G2["hi"][1]}, twist {G2["hi"][2]}')
                for k in ks_:
                    L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{GN_.sk(k, r)}" bodyB="{GN_.sk(k, r - 1)}"/>' for r in r_mid]; L.append('\t</constraint-group>')
            if GLOW and nr >= LOW_FROM:
                L += BW.chain_default_xyz(GLOW, f'{tg_} layer{sn_}, the hem rows: out up to {-GLOW["lo"][0]} rad per joint, in {GLOW["hi"][0]}, sideways {GLOW["hi"][1]}, twist {GLOW["hi"][2]}')
                for k in ks_:
                    L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{GN_.sk(k, r)}" bodyB="{GN_.sk(k, r - 1)}"/>' for r in range(LOW_FROM, nr + 1)]; L.append('\t</constraint-group>')
        glk = gph.get('LINK', (0.25, 0.3))
        L += D.link_default(glk[0], glk[1], f'{tg_} layer, round the body: neighbouring chains stay one piece (+-{glk[0]} / +-{glk[1]} rad); never across its slits')
        glinks, base = [], 0
        for p_ in rg.panels:
            for i in range(len(p_) - 1): glinks.append((base + i, base + i + 1, None))
            base += len(p_)
        if rg.slits:
            for si in range(len(rg.slits)):
                k_hi = sum(len(q) for q in rg.panels[:si]); k_lo = sum(len(q) for q in rg.panels[:(si - 1) % len(rg.panels)]) + len(rg.panels[(si - 1) % len(rg.panels)]) - 1
                glinks.append((k_lo, k_hi, max(rg.tops[l][si] for l in rg.tops)))
        else:
            glinks.append((nkg - 1, 0, None))
        for r in range(1, nr + 1):
            L.append('\t<constraint-group>')
            for a, b, top in glinks:
                if top is None or min(rg.rows[a][r], rg.rows[b][r]) > top + 1.0:
                    L.append(f'\t\t<generic-constraint bodyA="{GN_.sk(b, r)}" bodyB="{GN_.sk(a, r)}"/>')
            L.append('\t</constraint-group>')
    L += ['', '\t<!-- collisions -->']
    bt_ = ('boot',) if cfg.get('boot_coll') else ()      # 2026-10-14: the skirt lining meets the paired boot's cuff
    L += shape('per-vertex-shape', N.skc('Front'), 'skirtF', 0.1, can=('legsF', 'ground') + bt_)
    L += shape('per-vertex-shape', N.skc('Side'), 'skirtS', 0.1, can=('legsS', 'ground') + bt_)
    L += shape('per-vertex-shape', N.skc('Back'), 'skirtB', 0.1, can=('legsB', 'ground') + bt_)
    if bt_:
        bc_ = cfg['boot_coll']; L += ['\t<!-- the paired boot cuff (its outer band, one-sided), for the skirt lining: the hem is settled clear of it -->']
        L += shape('per-triangle-shape', N.BOOT, 'boot', bc_.get('margin', 0.2), can=('skirtF', 'skirtS', 'skirtB'), pen=bc_.get('pen', 1.5))
    LC_ = [lc for lc in cfg.get('layer_coll', ()) if lc['name'] in getattr(rig, 'lcoll', [])]
    for gw_, sides in getattr(rig, 'lin_sides', {}).items():     # SoS Officer v2: the extra layers vs the legs (+ the layer next to them)
        GN_ = GroupNames(N, gw_); extra = tuple(lc['name'].lower().replace(' ', '') for lc in LC_ if lc['pts'] == gw_)
        L += [f'\t<!-- {gw_.lower()} layer: its lining vs the trousers (front / side / back pieces)' + (f' and {", ".join(extra)}' if extra else '') + ' -->']
        for side in sides: L += shape('per-vertex-shape', GN_.skc(side), gw_.lower() + side[0], 0.1, can=('legs' + side[0], 'ground') + extra)
    for lc in LC_:
        sides = getattr(rig, 'lin_sides', {}).get(lc['pts'], [])
        L += [f'\t<!-- {lc["name"].lower()}: the {lc["surf"]} layer\'s {"inside (wound inward) keeps the " + lc["pts"].lower() + " layer under it" if lc["facing"] == "in" else "outside keeps the " + lc["pts"].lower() + " layer over it"}; pulled so nothing rests on it -->']
        L += shape('per-triangle-shape', f'{N.p} {lc["name"]}', lc['name'].lower().replace(' ', ''), 0.1, can=tuple(lc['pts'].lower() + s[0] for s in sides), pen=lc['pen'])
    L += ['\t<!-- the skirt\'s outer surface where the hanging pieces rest (pulled in so they rest clear of it) -->']
    tipc = cfg.get('tip_collide', Dz.get('tip_collide', False)) and has_tip      # v6: tails never collide
    sko_can = (('flap',) if nfl else ()) + (('bag',) if rig.has_bag else ())     # v12: the tail meets its own copy (below)
    if sko_can: L += shape('per-triangle-shape', N.SKO, 'skirtouter', 0.1, can=sko_can, pen=Dz.get('sko_pen', SKO_PEN))
    fu_ = getattr(rig, 'has_flapu', False)
    if nfl: L += shape('per-vertex-shape', N.FLP, 'flap', 0.15, can=('skirtouter',) + (('flapunder',) if fu_ else ()) + tuple(Dz.get('flap_legs', ('legsF', 'legsS', 'legsB'))))   # v12: per design (ILH: front only)
    if nfl and fu_:       # 2026-10-14 HOLDS: the cuirass hem + skirt under the hip strap, on their surface (the strap is settled clear of it)
        L += ['\t<!-- the cuirass hem and the skirt under the hip strap (its own copy, on their surface; the strap is settled clear of it): a swing cannot push it in -->']
        L += shape('per-triangle-shape', N.FLAPU, 'flapunder', 0.1, can=('flap',), pen=TAILU_PEN)
    if rig.has_bag: L += shape('per-vertex-shape', N.BAGC, 'bag', 0.15, can=('skirtouter', 'legsF', 'legsS', 'legsB'))
    if has_flo:
        L += shape('per-triangle-shape', N.FLO, 'flapouter', 0.1, can=('tip',), pen=1.0)
    if tipc and getattr(rig, 'has_tipu', False):
        L += ['	<!-- the skirt under the belt tail (its own copy, pulled in only where the tail rests closer than 0.35) -->']
        L += shape('per-triangle-shape', N.TIPU, 'tipunder', 0.1, can=('tip',), pen=TAILU_PEN)
    if tipc: L += shape('per-vertex-shape', N.TIPC, 'tip', 0.1, can=(('tipunder',) if getattr(rig, 'has_tipu', False) else ()) + tuple(cfg.get('tip_legs', Dz.get('tip_legs', ()))) + (('flapouter',) if has_flo else ()))
    if getattr(rig, 'has_hangu', False):           # v11: the hip hangers (rings + straps) vs their copy of the plates and the mail under them
        L += ['\t<!-- the plates and the mail under the hip hangers (their own copy, pulled in so the straps rest clear of it); a plate swinging out meets the strap -->']
        L += shape('per-triangle-shape', N.HANGU, 'hangunder', 0.1, can=('hang',), pen=TAILU_PEN)
        L += shape('per-vertex-shape', N.HANGC, 'hang', 0.1, can=('hangunder',))
    for nm in getattr(rig, 'torso_names', []):     # v11: the cuirass's outer surface for the Sons of Skyrim helmets' flap skirts (public, by tag)
        tc = Dz['torso_coll']
        L += [f'\t<!-- the cuirass above z {tc.get("zmin", 92.0):.0f}: its outer surface as a collider for the Sons of Skyrim helmets\' flap skirts (shared across files:',
              f'\t     the helmets\' collision points name the tag {tc.get("tag", "soscuirass")} and this names theirs; nothing in this file meets it) -->']
        L += shape('per-triangle-shape', nm, tc.get('tag', 'soscuirass'), tc.get('margin', 0.1), can=(tc.get('helm', 'soshelm'),), pen=tc.get('pen', 2.0), shared='public')
    for k_ in getattr(rig, 'tails', {}):           # SoS: the sash end vs its own copy of the skirt under it (and the legs when tail_legs names them)
        tg = k_.lower(); has_u = getattr(rig, 'tailu', {}).get(k_)
        if has_u:
            L += [f'\t<!-- the skirt under the {tg} end (its own copy, pulled in only as far as the {tg} needs to rest clear) -->']
            L += shape('per-triangle-shape', N.tailu(k_), tg + 'under', 0.1, can=(tg,), pen=TAILU_PEN)
        # 2026-10-13 (SoS guards' bags, user: 'it'll need colliders too'): a bag on its own hinge meets the trousers like the Stormcloak bags do
        L += shape('per-vertex-shape', N.tailc(k_), tg, 0.1, can=((tg + 'under',) if has_u else ()) + tuple(cfg.get('tail_legs', Dz.get('tail_legs', ()))))
    L += ['</system>', '']
    path = cfg.get('stage', STAGE) + cfg['xml'].replace('\\', '/'); os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f: f.write('\n'.join(L))
    log.append(f'{g}: wrote {cfg["xml"]} ({len(L)} lines); cross-slit links {[(a, b, None if t is None else round(t, 1)) for a, b, t in links if t is not None or not rig.slits][:4]}')


# ------------------------------------------------------------------ women: slider data + osp set
def bodyslide(design, rec, shared, log):
    cfg = DESIGNS[design]['f']; fp = shared['f_paths']
    magic, ver, entries = read_osd(fp['osd'])
    ss = copy.deepcopy(fp['ss']); osd_name = fp['srcfile'][:-4] + '.osd'
    T = rec['T']; nverts = {t.name: len(t.pos) for t in T}
    data = BWS.slider_data(ss, entries, set(nverts), nverts)

    def dense(prov_entry, per_src):
        kind = prov_entry[0]
        if isinstance(kind, np.ndarray):                   # (names, keys, idx) - a source shape's own subset (+ v13 welded seam midpoints)
            names, keys, idx = prov_entry; arr = per_src.get(names[0]) if len(names) else None
            if arr is None: return None
            Dd = np.array(arr[idx], float)
            for k_, key in enumerate(keys):                 # a welded point lies on an edge of the written remainder: its data along that edge
                if isinstance(key, tuple) and key and key[0] == 'weld': _, ia, ib, tt = key; Dd[k_] = (1.0 - tt) * Dd[ia] + tt * Dd[ib]   # (output indices, in creation order)
            return Dd
        if kind == 'piece':
            p = prov_entry[1]; arr = per_src.get(p.src)
            if arr is None: return None
            Dd = np.zeros((len(p.pos), 3)); n0 = p.n0 or len(p.pos)
            Dd[:n0] = arr[p.src_idx[:n0]]
            for j, (a, b) in enumerate(p.mids): Dd[n0 + j] = (Dd[a] + Dd[b]) / 2
            return Dd
        if kind == 'copy':
            arr = per_src.get(prov_entry[1]); return None if arr is None else arr[prov_entry[2]]
        if kind == 'multi':
            outs = [dense(('piece', p), per_src) for p, idx in prov_entry[1]]
            if all(o is None for o in outs): return None
            return np.vstack([(o[idx] if o is not None else np.zeros((len(idx), 3))) for o, (p, idx) in zip(outs, prov_entry[1])])
        if isinstance(prov_entry[0], np.ndarray):       # (names, keys, idx) - a source shape's own subset
            names, keys, idx = prov_entry; arr = per_src.get(names[0]) if len(names) else None
            return None if arr is None else arr[idx]
        raise RuntimeError(kind)
    written = list(rec['parts'])
    gone = [nm for nm in nverts if nm not in written]
    # rebuild the set's shapes and data from scratch for every written shape
    for el in list(ss.findall('Shape')): ss.remove(el)
    kids = list(ss); at = next(i for i, el in enumerate(kids) if el.tag == 'Slider')
    for i, nm in enumerate(written):
        e = ET.Element('Shape', {'target': nm}); e.text = nm; ss.insert(at + i, e)
    old_keys = set()
    for sl in ss.findall('Slider'):
        for d in list(sl.findall('Data')): old_keys.add(d.text.split('\\', 1)[1]); sl.remove(d)
    keep_entries = [(k, d) for k, d in entries if k not in old_keys]
    new_entries = []; n_new = 0
    for sl in ss.findall('Slider'):
        sname = sl.get('name'); per_src = data.get(sname, {})
        for nm in written:
            pe = rec['prov'].get(nm)
            if pe is None: continue
            Dd = dense(pe, per_src)
            if Dd is None: continue
            nd = {i: tuple(float(c) for c in x) for i, x in enumerate(Dd) if np.abs(x).max() > 1e-6}
            if not nd: continue
            key = nm + sname
            new_entries.append((key, nd)); n_new += 1
            ET.SubElement(sl, 'Data', {'name': key, 'target': nm, 'local': 'true'}).text = f'{osd_name}\\{key}'
    final = keep_entries + new_entries
    for k, d in final:
        if len(d) > 65535: raise RuntimeError(f'{k}: too many diffs')
    out_osd = STAGE + f'CalienteTools/BodySlide/ShapeData/{fp["folder"]}/{osd_name}'
    write_osd(out_osd, magic, ver, final)
    # SoS: the stage copy of the design's .osp starts from the INSTALLED override (the 10-04 port's sets for the coats not
    # rebuilt yet keep their physics), else the original; only this design's set is replaced (from the ORIGINAL set)
    with _shared_lock(STAGE + 'CalienteTools/BodySlide/SliderSets/' + os.path.basename(cfg['osp'])):   # 2026-10-13: several designs rewrite one .osp - serialised
        osp = STAGE + 'CalienteTools/BodySlide/SliderSets/' + os.path.basename(cfg['osp'])
        if not os.path.exists(osp):
            os.makedirs(os.path.dirname(osp), exist_ok=True)
            base = cfg.get('osp_installed') if cfg.get('osp_installed') and os.path.exists(cfg['osp_installed']) else cfg['osp']
            shutil.copy(base, osp); log.append(f'f: stage {os.path.basename(osp)} started from {base}')
        tree = ET.parse(osp); root = tree.getroot()
        i = next(i for i, s in enumerate(list(root)) if s.tag == 'SliderSet' and s.get('name') == cfg['set'])
        root.remove(list(root)[i]); root.insert(i, ss)
        ET.indent(tree, '    '); tree.write(osp, encoding='UTF-8', xml_declaration=True)
    log.append(f'f: osd {len(final)} entries ({n_new} written for {len(written)} shapes; removed shapes {gone}); osp set rebuilt from the ORIGINAL 3BA set')


def skel_of(path, N):
    n = NifFile(path); out = []
    for sh in n.shapes:
        if sh.name in N.hidden:
            for b in sh.bone_names:
                if not N.is_phys(b) and b not in out: out.append(b)
    return sorted(out)


def main(design, which):
    Dz = DESIGNS[design]; N = Names(Dz['prefix']); log, rep = [f'===== {design}'], {}
    for g in [x for x in which if x in Dz]:      # v5: some designs have no women's project
        # 2026-10-13: a copy triangle facing IN on some weight / BodySlide build / blend (finish_copy) is dropped from that copy on EVERY
        # weight - the weights are built one after the other, so the build runs again with it out until no copy has one (pass 1 = as before)
        drop, src_drop, posed_ = {}, {}, {}
        # 2026-10-14 (job 'the Whiterun rig everywhere', item 2: 'every copy face a hanger point is behind on the jump / flare clips is
        # DROPPED, not ridden'): posed_drop = True seeds the drops from <WORK>posed_drop_<design>_<g>.json ({selection key: [triangle
        # ids]}), written by sos tools/hang_posed_drop.py from the previous build posed through the plates' flares and the idle
        pdf_ = WORK + f'posed_drop_{design}_{g}.json'
        if Dz.get('posed_drop') and os.path.exists(pdf_):
            for k_, v_ in json.load(open(pdf_)).items(): drop.setdefault(k_, set()).update(int(x) for x in v_); posed_.setdefault(k_, set()).update(int(x) for x in v_)
            log.append(f'{g}: posed drops seeded from {os.path.basename(pdf_)}: ' + ', '.join(f'{k_} {len(v_)}' for k_, v_ in drop.items()))
        keep_in = os.environ.get('COAT_KEEP_INFACING') == '1'      # 2026-10-13 item B test (user): drop nothing - count what is left and stop
        for pass_ in range(6):
            shared, rec, plog = {'copy_drop': {k: set(v) for k, v in drop.items()}}, {}, []
            outs = [build(design, g, v, shared, plog, rec=rec if v == '1' else None) for v in (('1', '0') if g in ('m', 'v') else ('1',))]
            found = {k: set(v) for k, v in shared.get('copy_infacing', {}).items()}
            for k, v in shared.get('copy_src_infacing', {}).items(): found.setdefault(k, set()).update(v)
            new = {k: v - drop.get(k, set()) for k, v in found.items()}; new = {k: v for k, v in new.items() if v}
            if keep_in:
                if new: log.append(f'{g}: COAT_KEEP_INFACING - NOT dropped: ' + ', '.join(f'{k} {len(v)}' for k, v in new.items()) + ' copy triangles facing in (of them on the source '
                                   'itself, before any pull: ' + ', '.join(f'{k} {len(v)}' for k, v in shared.get('copy_src_infacing', {}).items() if v) + ')')
                break
            if not new: break
            log.extend(f'  (pass {pass_ + 1}) {l_}' for l_ in plog if 'tris pulled' in l_ or '      folded ' in l_)
            for k, v in new.items():
                drop.setdefault(k, set()).update(v)
                for t_ in v:          # 2026-10-13: which of them the SOURCE folds (a BodySlide build, before any pull) and how wide - verify's calibrated gate
                    if t_ in shared.get('copy_src_infacing', {}).get(k, ()): src_drop.setdefault(k, {})[int(t_)] = shared.get('copy_src_width', {}).get((k, t_), -1.0)
            log.append(f'{g}: pass {pass_ + 1}: copy triangles facing in on some weight / build / blend: ' + ', '.join(f'{k} {len(v)}' for k, v in new.items()) + ' - dropped on every weight, built again')
        else:
            log.append(f'{g}: copy triangles still facing in after 6 passes (verify will FAIL)')
        log.extend(plog)
        if drop: log.append(f'{g}: copy triangles dropped for facing in (selection key: count): ' + ', '.join(f'{k}: {len(v)}' for k, v in drop.items()))
        if g == 'f': bodyslide(design, rec, shared, log)
        rig = shared['rig']
        write_xml(design, g, rig, skel_of(outs[0], N), N.FLO in rec['parts'], log)
        rep[g] = dict(outs=outs, xml=Dz[g]['xml'], centre=[rig.cx, rig.cy], slits=rig.slits, tops=rig.tops, ang_k=rig.ang_k,
                      panels=rig.panels, rows={str(k): v for k, v in rig.rows.items()}, tip_rows=rig.tip_rows, tails=getattr(rig, 'tails', {}),
                      hangers=[dict(n=h['n'], front=len(h['front']), back=len(h['back']), strap=len(h['strap'])) for h in getattr(rig, 'hangers', [])],
                      groups={gw_: dict(centre=[r_.cx, r_.cy], slits=r_.slits, tops=r_.tops, ang_k=r_.ang_k, panels=r_.panels, nrow=r_.nrow,
                                        rows={str(k): v for k, v in r_.rows.items()}, phys=Dz[g]['groups'][gw_]['phys'])
                              for gw_, r_ in getattr(rig, 'groups', {}).items()},
                      bones={nm: x.tolist() for nm, x in rig.G.items()}, parent=rig.parent, rest=shared['rest'], lift=shared.get('lift', {}), dropped=shared.get('dropped', {}),
                      welded=rec.get('welded', {}),        # v13: {remainder shape: seam midpoints welded in} - verify accepts those points as source-edge midpoints
                      copy_drop={k: sorted(int(i) for i in v) for k, v in drop.items()},     # 2026-10-13: copy triangles dropped for facing in (by selection key)
                      copy_drop_posed={k: sorted(v) for k, v in posed_.items()},     # 2026-10-14: ... of them dropped by posed_drop (a hanging piece behind them on the clips)
                      copy_ids=shared.get('copy_ids', {}),       # 2026-10-14: per copy shape, each written triangle's drop id [selection key, index] (the _1 / last weight)
                      copy_drop_src={k: [[t_, w_] for t_, w_ in sorted(v.items())] for k, v in src_drop.items()},     # ... of them folded by the source itself [tri, width]
                      copies={nm: _copy_map(pe, rec['prov']) for nm, pe in rec['prov'].items() if nm in N.hidden and nm != N.GROUND} if g == 'f' else {})
    with _shared_lock(WORK + 'rework_report.json'):       # 2026-10-13: builds run in parallel - the report's read-modify-write is serialised
        old = json.load(open(WORK + 'rework_report.json')) if os.path.exists(WORK + 'rework_report.json') else {}
        old[design] = {**old.get(design, {}), **rep}; json.dump(old, open(WORK + 'rework_report.json', 'w'), indent=1)
    open(WORK + f'rework_{design}.log', 'w', encoding='utf-8').write('\n'.join(log) + '\n')
    print('\n'.join(log))


def _copy_map(pe, prov=None):
    """hidden copy -> list of [visible shape it was made from, its point index there] per copy point.
    SoS: a 'copy' records SOURCE indices (the slider data needs them); when that source shape was written as a cut remainder
    (the trousers component of the Armors torso) its output points are renumbered - map to the output index"""
    if pe[0] == 'copy':
        src = (prov or {}).get(pe[1])
        if src is not None and isinstance(src[0], np.ndarray):
            inv = {int(s): k for k, s in enumerate(src[2]) if not isinstance(src[1][k], tuple)}     # v13: welded seam points are not source points
            return [[pe[1], inv[int(i)]] for i in pe[2]]
        return [[pe[1], int(i)] for i in pe[2]]
    if pe[0] == 'multi':
        out = []
        for p, idx in pe[1]:
            src = (prov or {}).get(p.name) if getattr(p, 'role', None) == 'cuirass' else None
            if src is not None and isinstance(src[0], np.ndarray):     # 2026-10-14 HOLDS: a part made of a STATIC shape (flap_settle's cuirass,
                inv = {int(s): k for k, s in enumerate(src[2]) if not isinstance(src[1][k], tuple)}    # by source index) - its written points are
                out += [[p.name, inv[int(i)]] for i in idx]                                            # renumbered by the cut: the output index
            else: out += [[p.name, int(i)] for i in idx]
        return out
    return None


if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    use_designs(sys.argv[1]); d = sys.argv[2]
    if d not in DESIGNS: sys.exit(f'no design {d!r} in {sys.argv[1]} (has {list(DESIGNS)})')
    if d in TWO_LAYER and not os.environ.get('RA_TWOLAYER_PASS'):
        sys.exit(f'{d} is a two-layer skirt: not supported by the coat builder')
    main(d, [a for a in sys.argv[3:] if a in ('m', 'f', 'v')] or ['m', 'f'])
