"""Helmet builder: physics on a helmet's hanging parts, with colliders against the wearer's body and the cuirasses it is worn with.
Made for NordwarUA's Sons of Skyrim helmets (2026-10-11), after the Realistic Armor Mercenary helmet (build_merc_helmet.py):
  * the flap skirt / neck guard: here WELDED into the bowl - found by the author's own weights (the author fades Head -> Spine2 down
    the flaps; every point with a Spine2 share hangs). Its outward faces become the curtain, its inward faces (the lining) ride the
    curtain point in front of them. FLAP_N chains round its arc hang from the rim (row 0 = the head), FLAP_ROWS bones each; a curtain
    closed all round (a mail veil) gets chains round the full circle, linked round.
  * a crest (v3): a horsetail / tail that is its own shape (`crest=dict(shape='HorseTail_M', n=4)`): its hanging part (the author's
    Spine2 fade) on ONE chain of n bones from the crest down the tail, points bracketed by their position along it; the root stays
    on the head; its hanging points are collision points like the curtain's. A plume lying flat ON the bowl is left alone.
  * cheek guards: 'hinge' = a mirrored pair of welded pieces at the sides (the Realistic Armor rule), 'ears' = a mirrored pair of
    texture islands welded into the bowl, reaching below the rim; each a rigid plate on one bone hinged along its top edge.
  * colliders: the wearer's body round the neck (BODY, a hidden copy in the helmet, margin = min(BODY_MARGIN_MAX, rest -
    BODY_REST_CLEAR); nothing touches it at rest, the builder raises otherwise) and the CUIRASS it is worn with - not a copy: the
    Sons of Skyrim cuirass builds carry a public per-triangle collider of their outer surface above the chest (the coat builder's
    'torso_coll', tag CUIRASS_TAG) and the curtain's points are public, tagged HELM_TAG, naming it - FSMP matches the two across
    files on the same skeleton. (v1 carried ONE envelope over all cuirasses pulled into a trench round the resting curtain:
    boxed in, the skirts twitched and barely moved.) COLLARS (the built cuirasses per sex) now only feeds helmet_check.
  * limits per chain (v2): out = away from the head, never in; sideways favours the direction that trails the hem BACKWARD
    (a cape's flow on a walk) and allows little forward (never caving in over the face - the Realistic Armor lesson).
  * v4 (user 2026-10-12: 'all the helmets keep pulling forward, especially when I walk and run'): the curtain is SETTLED off every
    cuirass collider before the rig is built (settle_curtain: resting inside a collider's margin shell had the solver pushing those
    points every frame - forward at the chest / collar, up at the shoulders - and the shoulders' swing on a walk pumped it); the
    front chains barely swing out (out_front 0.05: a veil's front presses on the chest, it never lifts forward); a point with ANY
    share off the head hangs (the Officer pelt is partly on the clavicles); the Officer 'ear flaps' are painted panels welded all
    round (cheeks='ears' on them tore the bowl - dropped in the design).
Design file (Python, run in this module's namespace - see sos_helmets.py): SRC_ROOT, DONOR_ROOT (PBR-patched copies: geometry from
SRC, shader from the donor), STAGE, XD (XML dir), WORK (report dir), BODY = {'m': path, 'f': path}, COLLARS = {'m': [(name, path,
prefix) ...], 'f': [...]}, HELMETS = {name: dict(prefix, title, src ('folder/file_{}.nif'), variants, xml, cheeks=None|'hinge'|'ears',
n_chains=None, closed=None, flap_def/flap_lim1/flap_lim/flap_link/plate_def/plate_lim overrides)}. A variant ending in _0 reuses the
rig decided on its _1 (the game blends the two by vertex index).
usage: build_helmet_rig.py <designs.py> [helmet ...]"""
import os, sys, json, copy, runpy
import numpy as np
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
load, Writer, NifFile, NiStringExtraData = C.load, C.Writer, C.NifFile, C.NiStringExtraData
wrap, smooth01, lin_bracket, frame = C.wrap, C.smooth01, C.lin_bracket, C.frame
HEAD, SPINE2 = 'NPC Head [Head]', 'NPC Spine2 [Spn2]'

FLAP_ROWS = 3
# the curtain: light leather / mail that swings freely (no collar to fight: the Mercenary's final values were a compromise with the
# Realistic Armor collars - mass 1, inertia 6, damping .6/.7, out .35); here about half the mass, a third of the damping, twice the swing
# v2 (user: 'twitching in place ... barely react to walking ... flow like a cape when you move forward but never caving forward'):
# a little heavier and better damped than v1 (world-frame damping is what makes a hanging thing TRAIL when the wearer walks), wind .2
# (FSMP's wind, strength 2 here, fluttered the .5 flaps on the spot); the limits per chain by where it hangs - see flap_limits()
FLAP_DEF = dict(mass=0.6, inertia=4.0, lin=0.5, ang=0.45, friction=0.0, wind=0.2, gravity=1.0)    # v4: lin .45 -> .5 (a little more trail)
FLAP_LIM1 = dict(out_back=0.7, out_front=0.05, back=0.4, fwd=0.08, twist=0.12, stiff=(1, 2, 3))   # at the rim (v4: out_front .3 -> .05)
FLAP_LIM = dict(out_back=0.45, out_front=0.03, back=0.3, fwd=0.05, twist=0.08, stiff=(1, 2, 3))   # the lower joints (v4: .2 -> .03)
SETTLE_CLEAR, SETTLE_SPREAD, SETTLE_PIN = 0.3, 2.5, 2.5   # v4: the resting curtain clears every cuirass collider by its margins + this;
                                                          # a move is spread this far sideways (smooth mail) and fades to nothing this far under the rim
FLAP_LINK = (0.4, 0.5)            # neighbouring chains: loose enough to ripple
HELM_TAG, CUIRASS_TAG = 'soshelm', 'soscuirass'      # the cross-file pair: the curtain's points name the cuirass tag, the cuirass names this
# v6 'subtle' (user 2026-10-12, after v4 / v5 in game: the Officer mail 'moving on its own a bunch', the leather neck guards jittering as
# soon as the cuirass has a collar; decision: 'we'll stick with what we did with RA. keep it subtle. not problematic not crazy. super
# subtle'): the Realistic Armor Mercenary v7 recipe - heavy leather that barely moves (mass 1, inertia 6, damping .6/.7), out .35 / .25,
# a hair sideways (.08 / .06) on springs of 6, twist .05 / .04, links tight (one piece of leather, no ripple) - with NO wind (RA had .3;
# here the mail moved on the spot) and, per design (`cuirass_collide=False`), NO cuirass collision: the skirt keeps the author's drawn
# pose (no settle), its points are private and meet only the body copy round the neck; a tall collar it used to fight is clipped a
# little instead, exactly as the author's rigid mesh did. `link_round=False` leaves a closed veil's ring of links open at the front
# seam (a closed loop of tight links is over-constrained: the Officer veil crept on the spot). The front chains still lift next to nothing.
SUBTLE_FLAP_DEF = dict(mass=1.0, inertia=6.0, lin=0.6, ang=0.7, friction=0.0, wind=0.0, gravity=1.0)
SUBTLE_FLAP_LIM1 = dict(out_back=0.35, out_front=0.05, back=0.08, fwd=0.05, twist=0.05, stiff=(1, 6, 6))
SUBTLE_FLAP_LIM = dict(out_back=0.25, out_front=0.03, back=0.06, fwd=0.04, twist=0.04, stiff=(1, 6, 6))
SUBTLE_FLAP_LINK = (0.15, 0.2)
# a crest / horsetail / plume (v5): hair after the Realistic Armor Steel Lamellar ponytail (the user's reference) - weighty, damped,
# NEVER in (RA v6b: inward room let gravity press the hair onto the helmet = twitching), the springs' rest point a little outward so it
# hangs just off the bowl and bounces on a jump; 1 chain (a plume) or 3 side by side (a horsetail), bones along the tail's centreline
CREST_N = 5
CREST_DEF = dict(mass=0.9, inertia=16.0, lin=0.4, ang=0.4, friction=0.0, wind=0.5, gravity=0.9)
CREST_LIM1 = dict(lo=(-0.32, -0.2, -0.08), hi=(0.0, 0.2, 0.08), lin=0.0, stiff=(6, 3, 3), eq=(-0.04, 0.0, 0.0))   # at the root
CREST_LIM = dict(lo=(-0.28, -0.18, -0.06), hi=(0.0, 0.18, 0.06), lin=0.0, stiff=(4, 2, 2), eq=(-0.02, 0.0, 0.0))  # down the tail
CREST_LINK = (0.3, 0.3)           # the three chains of a horsetail, side by side
CREST_DX = 1.6                    # the side chains this far off the centre line (RA TAIL_DX), or the design's 'spread'
CREST_ROOT = 0.08                 # a tail without a Spine2 fade: this much of its length at the spike is the root tuft (welded)
CREST_PHYS_MIN = 0.3              # v5b: a tail point with less physics share than this (the root band, lying on the bowl under the pin) is not a collision point
BOWL_MARGIN, BOWL_PEN, BOWL_R = 0.25, 1.5, 6.0   # the hidden bowl copy under a tail: margin, catch, reach round the tail's points
CREST_ROOT_CLEAR, CREST_ROOT_SIGMA = 0.15, 0.6   # v7 (design key crest_settle_root): the plume's root lifted this far off the helmet, each
                                                 # move blended over this radius (a local lift - the static root only has to stop z-fighting)
# hinged cheek guards: v4 (user 2026-10-12 on the Haafingar plates: 'when they swing it's too loose') - half the swing of the Mercenary v5
# values, firmer springs, better damped: a riveted plate that stirs, not one that flaps
PLATE_DEF = dict(mass=0.6, inertia=2.5, lin=0.3, ang=0.35, friction=0.0, wind=0.0, gravity=1.0)
PLATE_LIM = dict(lo=(-0.1, -0.03, -0.01), hi=(0.03, 0.03, 0.01), lin=0.0, stiff=(12, 16, 40))
BODY_MARGIN_MAX, BODY_REST_CLEAR, BODY_PEN = 1.3, 0.35, 2.5     # body collider margin (a cuirass's thickness at most), rest clearance, catch
BODY_ZBELOW, BODY_R = 10.0, 18.0                                 # body triangles from this far under the curtain up, within this of the axis
BODY_PULL_SPREAD = 3.0            # v2: a pull-in under the resting curtain is spread this far sideways (a trench with walls caught the swing)
HANG_MIN = 0.02                   # a point with this much of the author's Spine2 share hangs
GUARD_PHYS_MIN = 0.15             # a curtain point with this much physics share is a collision point

SRC_ROOT = DONOR_ROOT = STAGE = XD = WORK = None; BODY = {}; COLLARS = {}; HELMETS = {}; DESIGNS_PATH = None


def use_designs(path):
    """run the design file in this module's namespace: it sets the paths, BODY, COLLARS and HELMETS"""
    global DESIGNS_PATH
    DESIGNS_PATH = os.path.abspath(path).replace(os.sep, '/')
    ns = runpy.run_path(DESIGNS_PATH, init_globals=dict(globals()))
    for k in ('SRC_ROOT', 'DONOR_ROOT', 'STAGE', 'XD', 'WORK', 'BODY', 'COLLARS', 'HELMETS'):
        if k in ns: globals()[k] = ns[k]
    for k in ('STAGE', 'WORK', 'SRC_ROOT', 'DONOR_ROOT'):
        if globals()[k]: globals()[k] = globals()[k].replace(os.sep, '/').rstrip('/') + '/'
    os.makedirs(WORK, exist_ok=True)


def islands(tris, n):
    """index-connected pieces (texture islands: UV seams split vertices)"""
    par = list(range(n))

    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for t in tris:
        for a, b in ((t[0], t[1]), (t[1], t[2])):
            ra, rb = f(int(a)), f(int(b))
            if ra != rb: par[ra] = rb
    return np.array([f(i) for i in range(n)])


def welded_components(pos, tris): return C.welded_components(pos, tris)


def signed_dist(Q, P, T_, ctr=None):
    # signed distance of points Q to a closed-ish surface (positive outside): by the triangles' normals, flipped if they face the
    # centre `ctr` (a body copy's winding is the author's)
    fn = np.cross(P[T_[:, 1]] - P[T_[:, 0]], P[T_[:, 2]] - P[T_[:, 0]]); fn = fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
    if ctr is not None:
        cen = P[T_].mean(1)
        if ((fn * (cen - ctr)).sum(1) < 0).mean() > 0.5: fn = -fn
    tri, _, d, cp = C.Surface([('s', P, T_)]).query(Q, k=8)
    return ((Q - cp) * fn[tri]).sum(1)


def signed_lat(Q, P, T_, ctr=None):
    # signed height over the nearest triangle's plane and the lateral distance to that triangle (0 = the point projects into it)
    fn = np.cross(P[T_[:, 1]] - P[T_[:, 0]], P[T_[:, 2]] - P[T_[:, 0]]); fn = fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
    if ctr is not None:
        cen = P[T_].mean(1)
        if ((fn * (cen - ctr)).sum(1) < 0).mean() > 0.5: fn = -fn
    tri, _, d, cp = C.Surface([('s', P, T_)]).query(Q, k=8)
    sd = ((Q - cp) * fn[tri]).sum(1)
    return sd, np.sqrt(np.maximum(d ** 2 - sd ** 2, 0.0))


def gmat(R, pos):
    gm = np.eye(4); gm[:3, :3] = R; gm[:3, 3] = pos; return gm


def ang_bracket(uk, u, closed):
    """the two chains round angle u (deg): plain bracket, or wrapping round for a closed curtain"""
    if not closed: return lin_bracket(uk, u)
    n = len(uk); d = np.array([float(wrap(u - a)) for a in uk]); i = int(np.argmin(np.abs(d)))
    j = (i + 1) % n if d[i] >= 0 else (i - 1) % n
    span = abs(float(wrap(uk[j] - uk[i]))); t = abs(d[i]) / max(span, 1e-6)
    return [(i, 1 - t), (j, t)]


def flap_limits(spec, phi):
    """joint limits for a chain hanging at azimuth phi (deg from the front, + = the actor's right), from a spec dict out_back /
    out_front / back / fwd / twist / stiff. The joint frame is X along the circumference (increasing azimuth), Y outward, Z up; Bullet
    measures the parent relative to the child, so a NEGATIVE X angle is a swing OUT and a POSITIVE Y angle a swing towards +X of the
    frame = increasing azimuth = BACKWARD on the actor's right side, FORWARD on the left. Out: out_front at the front chains (a veil's
    front lifts little off the chest) to out_back at the back; sideways: `back` in the trailing direction (full at the sides, fading to
    `fwd` at the front / back chains, whose sideways is left / right), `fwd` the other way - the skirt never caves in over the face."""
    s, c = np.sin(np.radians(phi)), np.cos(np.radians(phi))
    out = spec['out_front'] + (spec['out_back'] - spec['out_front']) * (1.0 - c) / 2.0
    side = spec['fwd'] + (spec['back'] - spec['fwd']) * abs(s)
    hi_y = side if s > 0 else spec['fwd']; lo_y = -(side if s < 0 else spec['fwd'])
    return dict(lo=(-round(float(out), 3), round(float(lo_y), 3), -spec['twist']), hi=(0.0, round(float(hi_y), 3), spec['twist']), lin=0.0, stiff=spec['stiff'])


class HelmRig:
    def __init__(self, t, H, log, vname, base=None, T=None):
        self.H, self.P = H, t.pos; P = t.pos; n = len(P); p = H['prefix']
        self.flap = lambda k, r: f'{p} Guard{k} {r}'; self.plate = lambda k, r: f'{p} Cheek{k} {r}'; self.crest_b = lambda c, r: f'{p} Crest{c} {r}'
        self.G, self.parent = {}, {}
        self.isl = islands(t.tris, n); self.lab = welded_components(P, t.tris)
        head1 = np.array([t.w[i].get(HEAD, 0.0) > 0.99 for i in range(n)])
        self.cx, self.cy = (float(P[head1, 0].mean()), float(P[head1, 1].mean())) if head1.any() else (float(P[:, 0].mean()), float(P[:, 1].mean()))
        hang = np.array([1.0 - t.w[i].get(HEAD, 0.0) for i in range(n)]) > HANG_MIN   # v4: any share off the head hangs (Spine2, or the clavicles on the Officer pelt)
        fn = np.cross(P[t.tris[:, 1]] - P[t.tris[:, 0]], P[t.tris[:, 2]] - P[t.tris[:, 0]]); cen = P[t.tris].mean(1)
        out_t = ((fn[:, :2] * (cen[:, :2] - [self.cx, self.cy])).sum(1) > 0)
        out_pt = np.zeros(n, bool); out_pt[np.unique(t.tris[out_t])] = True
        self.out_tris = t.tris[out_t]
        if base is not None:                       # the _0 of a pair: the _1's decisions (same vertex order)
            self.curtain_v, self.lining_v, self.plates = base.curtain_v, base.lining_v, base.plates
            self.closed, self.flap_uk, self.n_chains, self.kind = base.closed, base.flap_uk, base.n_chains, base.kind
        else:
            self.curtain_v = np.where(hang & out_pt)[0]; self.lining_v = np.where(hang & ~out_pt)[0]
            self.kind = H.get('cheeks'); self.plates = self._find_plates(t, log, vname) if self.kind else []
            if not self.plates: self.kind = None
            self.closed = None; self.flap_uk = None; self.n_chains = H.get('n_chains')
        self.has_flap = len(self.curtain_v) >= 30 and H.get('flap', True)
        if not H.get('flap', True): log.append(f'{vname}: flap skirt OFF by design (flap=False; {len(self.curtain_v)} curtain pts keep the author\'s weights)')
        elif not self.has_flap: log.append(f'{vname}: no hanging part (Spine2 share on {int(hang.sum())} pts)')
        else: self._flap(t, log, vname, base)
        if self.plates: self._plates(t, log)
        self.ang = lambda q: float(np.degrees(np.arctan2(q[0] - self.cx, q[1] - self.cy)))
        self.crest = None
        if H.get('crest') and T is not None: self._crest(T, log, vname, base)

    def _find_plates(self, t, log, vname):
        P = t.pos; rim = float(P[self.curtain_v, 2].max()) if len(self.curtain_v) else float(P[:, 2].min()) + 12.0
        groups = self.lab if self.kind == 'hinge' else self.isl
        ks = [k for k in set(groups.tolist()) if int((groups == k).sum()) >= 30]
        info = {}
        for k in ks:
            q = P[groups == k]; c = q.mean(0)
            info[k] = dict(n=int(len(q)), c=c, zmin=float(q[:, 2].min()), zmax=float(q[:, 2].max()), ang=float(np.degrees(np.arctan2(c[0] - self.cx, c[1] - self.cy))))
        best = None
        for i, a in enumerate(ks):
            for b in ks[i + 1:]:
                ia, ib = info[a], info[b]
                if ia['n'] != ib['n'] or abs(ia['c'][0] + ib['c'][0] - 2 * self.cx) > 0.8 or abs(ia['c'][1] - ib['c'][1]) > 0.8: continue
                if abs(ia['c'][0] - self.cx) < 3.0 or abs(ia['ang']) > 120 or ia['zmin'] > rim - 3.0: continue
                if best is None or ia['n'] > info[best[0]]['n']: best = sorted([a, b], key=lambda k: info[k]['c'][0])
        if best is None:
            log.append(f'{vname}: no mirrored cheek pair ({self.kind}) reaching below the rim {rim:.1f} - this variant gets no cheek guards (its own XML)'); return []
        log.append(f'{vname}: cheek guards ({self.kind}) = pieces {best} of {info[best[0]]["n"]} pts, z {info[best[0]]["zmin"]:.1f}..{info[best[0]]["zmax"]:.1f}')
        return [np.where(groups == k)[0] for k in best]

    def _plates(self, t, log):
        for k, v in enumerate(self.plates):
            q = t.pos[v]
            # v4: the hinge follows the plate's TOP EDGE along its whole length (per bin along the plate its highest point, a line through
            # those): a cheek piece riveted along a sloping rim turns about that slope. (v1-v3 took the highest 0.8 only - a level axis at
            # the back corner of the Haafingar plate, whose top edge drops 8 towards the face: its front swung off the bowl, 'disconnected'.)
            out2 = q[:, :2].mean(0) - [self.cx, self.cy]; out2 = out2 / (np.linalg.norm(out2) + 1e-9)     # the plate's outward direction
            along = np.array([-out2[1], out2[0]])                                                           # along its length (level)
            s = q[:, :2] @ along; bins = np.linspace(s.min(), s.max() + 1e-6, 9); tops = []
            for b0, b1 in zip(bins[:-1], bins[1:]):
                m = (s >= b0) & (s < b1)
                if m.sum() >= 2: tops.append(q[m][q[m, 2].argmax()])
            tops = np.array(tops); hinge = tops.mean(0); rise = float(np.ptp(tops[:, 2]))
            X = np.linalg.svd(tops - hinge, full_matrices=False)[2][0] if rise >= 0.6 else np.array([along[0], along[1], 0.0])
            phi = float(np.degrees(np.arctan2(out2[0], out2[1])))
            if X @ frame(phi)[:, 0] < 0: X = -X                                   # along increasing azimuth: the chains' convention (negative X = out)
            n3 = np.array([out2[0], out2[1], 0.0]); Y = n3 - (n3 @ X) * X; Y = Y / np.linalg.norm(Y); Z = np.cross(X, Y)
            Rm = np.c_[X, Y, Z]
            self.G[self.plate(k, 0)] = gmat(Rm, hinge); self.parent[self.plate(k, 0)] = HEAD
            self.G[self.plate(k, 1)] = gmat(Rm, q.mean(0)); self.parent[self.plate(k, 1)] = self.plate(k, 0)
            log.append(f'cheek guard {"LR"[k]}: hinge ({hinge[0]:.1f}, {hinge[1]:.1f}, {hinge[2]:.1f}) along its top edge ({rise:.1f} of rise over its length, '
                       f'axis tilted {np.degrees(np.arcsin(min(1.0, abs(float(X[2]))))):.0f} deg), faces {phi:.0f} deg, {q[:, 2].max() - q[:, 2].min():.1f} tall')

    def _flap(self, t, log, vname, base):
        P = t.pos; v = self.curtain_v; q = P[v]
        u = wrap(np.degrees(np.arctan2(q[:, 0] - self.cx, q[:, 1] - self.cy)) - 180.0)      # the back = 0, a face opening at +-180
        self.flap_u = u
        if self.closed is None:
            us = np.sort(u); gaps = np.diff(np.r_[us, us[0] + 360.0]); self.closed = bool(self.H.get('_closed', self.H.get('closed', gaps.max() < 25.0)))
        closed = self.closed
        if self.flap_uk is None:
            n_ = self.n_chains or self.H.get('_n_chains') or (int(self.H.get('n_closed', 12)) if closed else int(np.clip(round((u.max() - u.min() - 12.0) / 22.0) + 1, 4, 10)))   # decided on the first variant with a curtain (one XML per design)
            self.n_chains = n_
            self.flap_uk = self.H.get('_flap_uk') or (list(np.linspace(-180.0, 180.0, n_ + 1)[:-1]) if closed else list(np.linspace(u.min() + 6.0, u.max() - 6.0, n_)))   # v2: once per design
        uk = self.flap_uk; n_ = len(uk); hw = (360.0 / n_) / 2.0 + 6.0 if closed else 12.0
        tops, bots = [], []
        for k, a in enumerate(uk):
            m = np.abs(wrap(u - a)) < hw
            if m.sum() < 3: m = np.abs(wrap(u - a)) < hw * 2
            tops.append(float(q[m, 2].max())); bots.append(float(q[m, 2].min()))
            for r, sr in enumerate(np.linspace(0.0, 1.0, FLAP_ROWS + 1)):
                z = tops[-1] - sr * (tops[-1] - bots[-1] - 0.2)
                mm = m & (np.abs(q[:, 2] - z) < 0.9)
                rr = float(np.median(np.hypot(q[mm, 0] - self.cx, q[mm, 1] - self.cy))) if mm.sum() >= 2 else float(np.median(np.hypot(q[m, 0] - self.cx, q[m, 1] - self.cy)))
                th = np.radians(a + 180.0)
                self.G[self.flap(k, r)] = gmat(frame(a + 180.0), [self.cx + rr * np.sin(th), self.cy + rr * np.cos(th), z])
                self.parent[self.flap(k, r)] = HEAD if r == 0 else self.flap(k, r - 1)
        self.flap_top, self.flap_bot = tops, bots
        log.append(f'{vname}: curtain {len(v)} outward pts (+ {len(self.lining_v)} lining) round {u.min() + 180:.0f}..{u.max() + 180:.0f} deg'
                   f'{" (closed all round)" if closed else " (open at the face)"}, {n_} chains x {FLAP_ROWS} bones, top {min(tops):.1f}..{max(tops):.1f}, bottom {min(bots):.1f}..{max(bots):.1f}')

    def _crest(self, T, log, vname, base):
        cfg = self.H['crest']; cr = next((u for u in T if u.name == cfg['shape']), None) or next((u for u in T if u.name.lower().startswith(cfg['shape'].lower().split('_')[0])), None)   # HorseTail_M / _MA / _F ...
        if cr is None: log.append(f'{vname}: no crest shape {cfg["shape"]} (shapes {[u.name for u in T]}) - this variant gets no crest (its own XML)'); return
        n_ = int(cfg.get('n', CREST_N)); nc = int(cfg.get('chains', 1)); P = cr.pos
        if base is not None and base.crest is not None:
            hang, s, u = base.crest['hang'], base.crest['s'], base.crest['u']
        else:
            sp2 = np.array([w.get(SPINE2, 0.0) for w in cr.w]); faded = sp2 > HANG_MIN
            q0 = P - P.mean(0); d = np.linalg.svd(q0, full_matrices=False)[2][0]
            if faded.sum() >= 20:                                              # the author's fade: s = 0 at the crest, the fade grows along the tail
                if np.corrcoef((q0 @ d)[faded], sp2[faded])[0, 1] < 0: d = -d
                hang = faded
            else:                                                              # v5: no fade (the Riften plume): the tail runs DOWN from the spike
                if np.corrcoef(q0 @ d, P[:, 2])[0, 1] > 0: d = -d
                pr0 = q0 @ d; hang = pr0 > pr0.min() + CREST_ROOT * np.ptp(pr0)
            if hang.sum() < 20: log.append(f'{vname}: crest {cfg["shape"]} has no hanging part ({int(hang.sum())} pts)'); return
            pr = (P - P[hang].mean(0)) @ d; lo, hi = pr[hang].min(), pr[hang].max()
            s = np.clip((pr - lo) / max(hi - lo, 1e-6), 0.0, 1.0)
            lat = np.cross(d, [0.0, 0.0, 1.0]); lat = lat / (np.linalg.norm(lat) + 1e-9)       # across the tail (level)
            u = (P - P[hang].mean(0)) @ lat
        ss = [0.0] + [(j + 0.5) / n_ for j in range(n_)]; az = self.ang(P[hang].mean(0)); R = frame(az)
        pts = [P[hang & (s < 0.5 / n_)].mean(0)] + [P[hang & (s >= j / n_) & (s < (j + 1) / n_)].mean(0) if (hang & (s >= j / n_) & (s < (j + 1) / n_)).sum() >= 2 else None for j in range(n_)]
        for j in range(1, n_ + 1):
            if pts[j] is None or not np.all(np.isfinite(pts[j])): pts[j] = pts[j - 1] + (P[hang].mean(0) - pts[0]) / max(n_, 1)
        pts = np.array(pts)
        if len(pts) > 3: pts[1:-1] = np.array([np.convolve(pts[:, i], np.ones(3) / 3, 'same') for i in range(3)]).T[1:-1]   # a smooth centreline (RA)
        spread = float(cfg.get('spread', min(CREST_DX, 0.45 * float(np.percentile(np.abs(u[hang]), 90)) + 0.3))) if nc > 1 else 0.0
        self.crest_dx = [(c - (nc - 1) / 2.0) * spread for c in range(nc)]; X = R[:, 0]
        for c in range(nc):
            for r, cpt in enumerate(pts):
                self.G[self.crest_b(c, r)] = gmat(R, cpt + self.crest_dx[c] * X); self.parent[self.crest_b(c, r)] = HEAD if r == 0 else self.crest_b(c, r - 1)
        self.crest = dict(shape=cr.name, hang=hang, s=s, u=u, n=n_, chains=nc, ss=ss)
        log.append(f'{vname}: crest {cr.name}: {int(hang.sum())} of {len(P)} pts hang on {nc} chain(s) x {n_} bones from ({pts[0][0]:.1f}, {pts[0][1]:.1f}, {pts[0][2]:.1f}) to '
                   f'({pts[-1][0]:.1f}, {pts[-1][1]:.1f}, {pts[-1][2]:.1f}), facing {az:.0f} deg' + (f', chains {spread:.1f} apart' if nc > 1 else ''))

    def bowl_under_crest(self, t, cr):
        """v5: the bowl's outward faces within BOWL_R of the tail's hanging points - the hidden copy the tail collides with"""
        hv = np.where(self.crest['hang'])[0]; cen = t.pos[t.tris].mean(1)
        fn = np.cross(t.pos[t.tris[:, 1]] - t.pos[t.tris[:, 0]], t.pos[t.tris[:, 2]] - t.pos[t.tris[:, 0]])
        ctr = np.array([self.cx, self.cy, float(t.pos[:, 2].mean())])
        near = np.zeros(len(cen), bool)
        for s0 in range(0, len(cen), 1500):
            near[s0:s0 + 1500] = (np.linalg.norm(cen[s0:s0 + 1500, None, :] - cr.pos[hv][None, :, :], axis=2).min(1) < self.H.get('bowl_r', BOWL_R))   # v8: per design (the Riften plume's copy reaches the apex)
        sel = near & (((fn * (cen - ctr)).sum(1) / (np.linalg.norm(fn, axis=1) * np.linalg.norm(cen - ctr, axis=1) + 1e-9)) > 0.05)
        # v8b (Riften v8 in game: 'pulled like a magnet towards the chainmail, twitching'): a copy face that has tail points BEHIND it within
        # the catch at rest (the far side of the spike, the rim's underside, a face the tail never lies on) pushes them through itself every
        # frame. Keep only faces the tail lies IN FRONT of: drop every face with a hanging point behind it within the catch, and faces that
        # look down (the rim's underside). Measured on v8: 32 of 386 points 2.4-4.0 behind 8 faces at catch 4.0; 0 at catch 1.5.
        pen_ = float(self.H.get('bowl_pen', BOWL_PEN)); Q = cr.pos[hv]; n_ = fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
        bad = n_[:, 2] < -0.3
        A_, B_, C_ = t.pos[t.tris[:, 0]], t.pos[t.tris[:, 1]], t.pos[t.tris[:, 2]]
        for j in np.where(sel & ~bad)[0]:
            h = (Q - A_[j]) @ n_[j]; c = (h > -pen_) & (h < 0.0)
            if not c.any(): continue
            pr = Q[c] - h[c, None] * n_[j]; v0, v1, v2 = C_[j] - A_[j], B_[j] - A_[j], pr - A_[j]
            d00, d01, d11 = v0 @ v0, v0 @ v1, v1 @ v1; d02, d12 = v2 @ v0, v2 @ v1; den = d00 * d11 - d01 * d01 + 1e-12
            u = (d11 * d02 - d01 * d12) / den; v = (d00 * d12 - d01 * d02) / den
            if ((u >= -0.08) & (v >= -0.08) & (u + v <= 1.08)).any(): bad[j] = True
        self.bowl_dropped = int((sel & bad).sum()); sel &= ~bad
        if self.H.get('bowl_drop_contact'):
            # 2026-10-13 (the Whiterun horsetail): the same rule measured as FSMP (and helmet_check's contact) does - a point behind a face's plane
            # within the catch whose closest point on the triangle lies within the margins sideways (an edge counts), not only one projecting
            # inside it: the side walls on the back centre line (x +-1.5, facing each other) had strands 0.2-1.3 behind them just past their edges
            m_ = float(self.H.get('bowl_margin', BOWL_MARGIN)) + 0.1
            for _ in range(8):
                idx = np.where(sel)[0]
                if not len(idx): break
                tri, _, d, cp = C.Surface([('s', t.pos, t.tris[idx])]).query(Q, k=24)
                sd = ((Q - cp) * n_[idx][tri]).sum(1); lat = np.sqrt(np.maximum(d ** 2 - sd ** 2, 0.0))
                hit = (sd < 0.0) & (sd > -pen_) & (lat < m_)
                if not hit.any(): break
                drop_ = idx[np.unique(tri[hit])]; sel[drop_] = False; self.bowl_dropped += len(drop_)
        bt = t.tris[sel]; bv = np.unique(bt); rm = np.full(len(t.pos), -1); rm[bv] = np.arange(len(bv))
        return bv, rm[bt]

    def crest_weights(self, cr):
        """the crest shape's weights: hanging points bracketed along the chain (s = 0 is the head), the rest the author's"""
        W = [dict(w) for w in cr.w]; c = self.crest; dx = self.crest_dx
        for i in np.where(c['hang'])[0]:
            w = defaultdict(float)
            for a, x in lin_bracket(c['ss'], float(c['s'][i])):
                if a == 0: w[HEAD] += x; continue
                for ch, b in (lin_bracket(dx, float(c['u'][i])) if len(dx) > 1 else [(0, 1.0)]): w[self.crest_b(ch, a)] += x * b
            W[i] = dict(w)
        return W

    def weights(self, t, log):
        n = len(t.pos); W = [dict(t.w[i]) for i in range(n)]
        for k, v in enumerate(self.plates):
            for i in v: W[i] = {self.plate(k, 1): 1.0}
        if self.has_flap:
            srows = list(np.linspace(0.0, 1.0, FLAP_ROWS + 1))
            for j, i in enumerate(self.curtain_v):
                u = float(self.flap_u[j]); z = float(t.pos[i, 2])
                if self.closed:
                    uk_ = np.array(self.flap_uk); d_ = np.abs(wrap(u - uk_)); a_ = np.exp(-(d_ / (360.0 / len(uk_))) ** 2) + 1e-9
                    top = float((a_ * self.flap_top).sum() / a_.sum()); bot = float((a_ * self.flap_bot).sum() / a_.sum())
                else:
                    top = float(np.interp(u, self.flap_uk, self.flap_top)); bot = float(np.interp(u, self.flap_uk, self.flap_bot))
                s = float(np.clip((top - z) / max(top - bot - 0.2, 1e-3), 0.0, 1.0)); w = defaultdict(float)
                for r, a in lin_bracket(srows, s):
                    for k, b in ang_bracket(self.flap_uk, u, self.closed): w[HEAD if r == 0 else self.flap(k, r)] += a * b
                W[i] = dict(w)
            # the lining rides the curtain point in front of it (the same bones, the same motion - the SoS Officer skirt lesson)
            if len(self.lining_v):
                cv = self.curtain_v; rm = np.full(n, -1); rm[cv] = np.arange(len(cv)); ct = self.out_tris[(rm[self.out_tris] >= 0).all(1)]
                if len(ct):
                    tri, bary, dist, cp = C.Surface([('c', t.pos[cv], rm[ct])]).query(t.pos[self.lining_v], k=8)
                    for j, i in enumerate(self.lining_v):
                        acc = defaultdict(float)
                        for vv, bb in zip(rm[ct][tri[j]], bary[j]):
                            for b, x in W[cv[vv]].items(): acc[b] += bb * x
                        W[i] = dict(acc)
        ph = np.array([sum(x for b, x in w.items() if b.startswith(self.H['prefix'] + ' ')) for w in W])
        log.append(f'weights: curtain {len(self.curtain_v)} + lining {len(self.lining_v)} pts on the chains ({int((ph > GUARD_PHYS_MIN).sum())} with > {GUARD_PHYS_MIN} physics), '
                   f'cheek guards {sum(len(v) for v in self.plates)} pts, the rest on the head')
        self.phys_share = ph
        return W


_BODY = {}


def body_collider(g, rig, t, log, vname, ang_min, tri_sel=None):
    """the wearer's body round the neck near the curtain (back / sides, or all round for a closed curtain), facing out, its own
    weights (breast / belly physics bones folded into Spine2). tri_sel: a _0 helmet reuses its _1's triangle set (v6d: the game blends
    the _0 and _1 meshes shape by shape at load and reads one buffer with the other's vertex count - every shape must match)"""
    if g not in _BODY:                             # g = 'm' / 'f' / 'm0' / 'f0' (the weight-0 body for a _0 helmet)
        n_, Tb = load(BODY.get(g) or BODY[g[0]]); C.to_world(Tb); _BODY[g] = max(Tb, key=lambda x: len(x.pos))
    body = _BODY[g]; gv = np.r_[rig.curtain_v, rig.lining_v]; gz0, gz1 = float(t.pos[gv, 2].min()), float(t.pos[gv, 2].max())
    c = body.pos[body.tris].mean(1); a = np.degrees(np.arctan2(c[:, 0] - rig.cx, c[:, 1] - rig.cy)); r = np.hypot(c[:, 0] - rig.cx, c[:, 1] - rig.cy)
    own = (c[:, 2] > gz0 - BODY_ZBELOW) & (c[:, 2] < gz1 + 2.0) & (np.abs(a) > ang_min) & (r < BODY_R)
    sel = own if tri_sel is None else tri_sel
    if tri_sel is not None:
        log.append(f'{vname}: body copy shares the _1 triangle set ({int(sel.sum())} tris; {int((own & ~tri_sel).sum())} of its own {int(own.sum())} not in it)')
    tt = body.tris[sel]; vv = np.unique(tt); rm = np.full(len(body.pos), -1); rm[vv] = np.arange(len(vv))
    W = []
    for i in vv:
        acc = defaultdict(float)
        for b, x in body.w[i].items(): acc[b if b.startswith('NPC ') else SPINE2] += x
        W.append(dict(acc))
    BP, BT = body.pos[vv].copy(), rm[tt]; ctr_ = np.array([rig.cx, rig.cy, gz0 - 6.0])
    d = signed_dist(t.pos[gv], BP, BT, ctr=ctr_); pulled = 0
    if d.min() < BODY_REST_CLEAR + 0.1:     # the curtain rests on / inside the body proxy (a beast race's or an orc's helmet on the human
        # body copy): the copy is pulled in under those points (as the leg colliders are) so nothing touches at rest
        _, off = C.pull_in(BP, BT, t.pos[gv], BODY_REST_CLEAR + 0.15, 2.5, lat=1.5)
        if (off > 0.01).any():                  # v2: spread sideways - every vertex takes the largest pull within BODY_PULL_SPREAD, faded (no walls)
            off2 = off.copy(); src = np.where(off > 0.01)[0]
            for s0 in range(0, len(BP), 400):
                d_ = np.linalg.norm(BP[s0:s0 + 400, None, :] - BP[None, src, :], axis=2)
                off2[s0:s0 + 400] = np.maximum(off2[s0:s0 + 400], (off[None, src] * np.exp(-(d_ / BODY_PULL_SPREAD) ** 2)).max(1))
            off = off2
        nrm = C.vertex_normals(BP, BT)
        if ((nrm * (BP - ctr_)).sum(1) < 0).mean() > 0.5: nrm = -nrm
        BP = BP - off[:, None] * nrm; pulled = int((off > 0.01).sum()); d = signed_dist(t.pos[gv], BP, BT, ctr=ctr_)
    log.append(f'{vname}: body collider = {g} body, {len(tt)} tris (z {c[sel, 2].min():.1f}..{c[sel, 2].max():.1f}); the curtain rests {d.min():+.2f} off it ({int((d < 0).sum())} pts inside it)'
               + (f'; copy pulled in under {pulled} pts' if pulled else ''))
    return BP, BT, W, body.s2b, float(d.min()), sel


_CUIRASS = {}


def cuirass_colliders(gw, log):
    """the public torso colliders of every built cuirass of this sex / weight (COLLARS, as helmet_check reads them): (design, pos,
    tris, margin) - loaded once per run"""
    if gw in _CUIRASS: return _CUIRASS[gw]
    import re
    res = []
    for ent in (COLLARS.get(gw) or COLLARS.get(gw[0]) or []):
        d, path = ent[0], ent[1]; xml = ent[3] if len(ent) > 3 else None
        if not os.path.exists(path): continue
        n_, T_ = load(path); C.to_world(T_)
        xs = open(xml, encoding='utf-8', errors='replace').read() if xml and os.path.exists(xml) else ''
        for t_ in T_:
            if ' Torso Collide' not in t_.name: continue
            m = re.search(r'<per-triangle-shape name="' + re.escape(t_.name) + r'">\s*<margin>([\d.]+)', xs)
            res.append((d, t_.pos, t_.tris, float(m.group(1)) if m else 0.1))
    _CUIRASS[gw] = res
    log.append(f'cuirass colliders for {gw!r}: {len(res)} shapes from {len({r[0] for r in res})} builds')
    return res


def _sd_n(Q, BP, BT):
    """signed distance (positive outside, by the collider's own outward winding), lateral distance and the normal of the nearest triangle"""
    fn = np.cross(BP[BT[:, 1]] - BP[BT[:, 0]], BP[BT[:, 2]] - BP[BT[:, 0]]); fn = fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
    tri, _, d, cp = C.Surface([('s', BP, BT)]).query(Q, k=24)      # v4: 24 candidates, as the check (8 missed the nearest triangle at a collar fold - the Officer pelt)
    sd = ((Q - cp) * fn[tri]).sum(1)
    return sd, np.sqrt(np.maximum(d ** 2 - sd ** 2, 0.0)), fn[tri]


def _outward(nrm, Q, axis):
    """a settle direction never points in towards the head's axis: the inward part of a collider normal (a pauldron's inner slope) is
    dropped, so the point lifts out instead of moving onto the neck (a curtain moved onto the body copy could not be cleared)"""
    if axis is None: return nrm
    rad = Q[:, :2] - np.asarray(axis)[None, :]; rad = rad / (np.linalg.norm(rad, axis=1, keepdims=True) + 1e-9)
    inward = np.minimum((nrm[:, :2] * rad).sum(1), 0.0)
    n2 = nrm.copy(); n2[:, :2] -= inward[:, None] * rad
    ln = np.linalg.norm(n2, axis=1); flat = ln < 0.2
    n2[flat] = np.c_[rad[flat], np.zeros(int(flat.sum()))]; ln = np.linalg.norm(n2, axis=1)
    return n2 / (ln[:, None] + 1e-9)


def _settle_points(P, idx, ramp, cu, label, log, vname, ride_idx=None, axis=None):
    """move the points P[idx] out of every collider's margin shell (+ SETTLE_CLEAR) along the collider's normal there (never in towards
    the head's axis), the largest need winning, spread SETTLE_SPREAD sideways, scaled by ramp (0 pins); the points P[ride_idx] (a
    lining: the inner faces, deeper by the flap's thickness) ride their nearest point of idx and their own need counts for it;
    returns the total move per point"""
    P0 = P[idx].copy(); total = np.zeros((len(idx), 3)); worst = {}
    ride = None
    if ride_idx is not None and len(ride_idx):
        ride = np.zeros(len(ride_idx), int)
        for s0 in range(0, len(ride_idx), 500):
            ride[s0:s0 + 500] = np.linalg.norm(P[ride_idx[s0:s0 + 500]][:, None, :] - P0[None, :, :], axis=2).argmin(1)
    for it in range(14):
        Q = P[idx]; req = np.zeros((len(idx), 3)); rn = np.zeros(len(idx))
        Qr = P[ride_idx] if ride is not None else None
        for d, BP, BT, m_ in cu:
            sd, lat, nrm = _sd_n(Q, BP, BT); nrm = _outward(nrm, Q, axis)
            need = np.where(lat < 1.5, m_ + 0.1 + SETTLE_CLEAR - sd, 0.0)
            if ride is not None:                        # a lining point's need lands on the curtain point it rides
                sdr, latr, nrmr = _sd_n(Qr, BP, BT); nrmr = _outward(nrmr, Qr, axis); needr = np.where(latr < 1.5, m_ + 0.1 + SETTLE_CLEAR - sdr, 0.0)
                for j in np.argsort(needr):                 # ascending: the largest need on a shared curtain point lands last
                    if needr[j] > need[ride[j]]: need[ride[j]] = needr[j]; nrm[ride[j]] = nrmr[j]
            better = need > rn
            rn[better] = need[better]; req[better] = (np.minimum(need[better], 3.0) * ramp[better])[:, None] * nrm[better]
            if (need > 0.01).any(): worst[d] = max(worst.get(d, 0.0), float(need.max()))
        mag = np.linalg.norm(req, axis=1)
        if mag.max() <= 0.01: break
        src = np.where(mag > 0.01)[0]; off = np.zeros_like(req)
        for s0 in range(0, len(idx), 500):
            D = np.linalg.norm(Q[s0:s0 + 500, None, :] - Q[None, src, :], axis=2); wgt = mag[None, src] * np.exp(-(D / SETTLE_SPREAD) ** 2)
            j = wgt.argmax(1); off[s0:s0 + 500] = req[src[j]] * np.exp(-(D[np.arange(len(j)), j] / SETTLE_SPREAD) ** 2)[:, None]
        own = mag >= np.linalg.norm(off, axis=1); off[own] = req[own]
        P[idx] += off; total += off
        if ride is not None: P[ride_idx] += off[ride]
    moved = int((np.linalg.norm(total, axis=1) > 0.05).sum())
    if moved:
        tops = sorted(worst.items(), key=lambda kv: -kv[1])[:4]
        log.append(f'{vname}: {label} settled off the cuirass colliders: {moved} pts moved, up to {np.linalg.norm(total, axis=1).max():.2f} '
                   f'(needed most by {", ".join(f"{d} {x:.2f}" for d, x in tops)}; clearance = margins + {SETTLE_CLEAR}; {it + 1} passes)')
    return total, P0


def settle_curtain(t, rig, gw, log, vname, T=None):
    """v4: the resting curtain (and a crest's hanging part) is moved OUT of every cuirass collider's margin shell - see the header;
    v6: a design with cuirass_collide=False keeps the author's drawn curtain (nothing to settle it off); a crest still settles off the bowl"""
    cc = rig.H.get('cuirass_collide', True)
    cu = cuirass_colliders(gw, log) if cc else []
    if not cc: log.append(f'{vname}: no cuirass collision by design (v6 subtle) - the curtain keeps the author\'s drawn pose')
    if not cu and not rig.crest: return 0
    moved = 0
    if rig.has_flap and cu:
        P = t.pos; cv = rig.curtain_v; lv = rig.lining_v; top = float(P[cv, 2].max())
        ramp = np.clip((top - P[cv, 2]) / rig.H.get('settle_pin', SETTLE_PIN), 0.0, 1.0)   # per design: the Officer pelt meets the cuirass collars right under its welded rim
        total, P0 = _settle_points(P, cv, ramp, cu, 'curtain', log, vname, ride_idx=lv, axis=(rig.cx, rig.cy))   # the lining rides its nearest curtain point (as its weights do)
        moved += int((np.linalg.norm(total, axis=1) > 0.05).sum())
    if rig.crest and T is not None:
        cr = next(u for u in T if u.name == rig.crest['shape']); hv = np.where(rig.crest['hang'])[0]
        ramp = np.clip(rig.crest['s'][hv] / 0.15, 0.0, 1.0)      # v5b: a shorter root pin (the Whiterun mane lies on the bowl right under it)
        bv, BT = rig.bowl_under_crest(t, cr)                                           # v5: and off the bowl it hangs against
        total, _ = _settle_points(cr.pos, hv, ramp, cu + [('the bowl', t.pos[bv], BT, BOWL_MARGIN)], 'crest', log, vname, axis=(rig.cx, rig.cy))
        moved += int((np.linalg.norm(total, axis=1) > 0.05).sum())
        if rig.H.get('crest_settle_root'):
            # v7 (user 2026-10-12, the Riften plume: 'it would enter right at the top there ... instead of colliding with the helmet'): the
            # author drew the plume's root band (the welded tuft, never a hanging point, so never settled above) THROUGH the finial collar
            # under the spike tip (heavy 39 / light 102 pts, up to 0.32 under the outer surface) - static, so no collider can help. A LOCAL
            # lift (not the curtain settle: its 2.5 spread and 0.65 clearance tore the plume off the tip - v7a, survey/plume_apex_heavy_m_v7.png):
            # only the points inside or within crest_root_clear of the helmet's outward faces near the plume move, out along the face normal
            # (never in towards the axis) to that clearance, blended over crest_root_sigma; the plume's other points stay where drawn
            clear_, sig_ = rig.H.get('crest_root_clear', CREST_ROOT_CLEAR), rig.H.get('crest_root_sigma', CREST_ROOT_SIGMA); P = cr.pos
            cen = t.pos[t.tris].mean(1); fn = np.cross(t.pos[t.tris[:, 1]] - t.pos[t.tris[:, 0]], t.pos[t.tris[:, 2]] - t.pos[t.tris[:, 0]])
            ctr = np.array([rig.cx, rig.cy, float(t.pos[:, 2].mean())]); near = np.zeros(len(cen), bool)
            for s0 in range(0, len(cen), 1500): near[s0:s0 + 1500] = np.linalg.norm(cen[s0:s0 + 1500, None, :] - P[None, :, :], axis=2).min(1) < BOWL_R
            sel = near & (((fn * (cen - ctr)).sum(1) / (np.linalg.norm(fn, axis=1) * np.linalg.norm(cen - ctr, axis=1) + 1e-9)) > 0.05)
            if rig.H.get('crest_root_all_faces'):    # 2026-10-13 (the Whiterun horsetail): its centre strands run 0.02-0.27 INSIDE side-facing faces on
                sel = near                           # the back centre line (outward-filtered faces never saw them); every face near the plume counts
            bt_ = t.tris[sel]; bv_ = np.unique(bt_); rm_ = np.full(len(t.pos), -1); rm_[bv_] = np.arange(len(bv_))
            # 2026-10-13 (the Whiterun horsetail, user: 'rebuild ... properly ... with proper collisions'): its author drew a DEEP insertion inside
            # the helmet (95-130 head-bound pts, never moving, hidden); the v7 lift pushed that stub out by 1.0-1.6 (the cap floating off the
            # helmet - the Riften v7b lesson). crest_root_hanging: only the hanging points (the ones that move) are lifted
            tot = _lift_off(P, t.pos[bv_], rm_[bt_], clear_, sig_, (rig.cx, rig.cy), movable=rig.crest['hang'] if rig.H.get('crest_root_hanging') else None)
            nm_ = np.linalg.norm(tot, axis=1); moved += int((nm_ > 0.05).sum())
            log.append(f'{vname}: crest root lifted off the helmet ({len(bt_)} outward faces near the plume): {int((nm_ > 0.05).sum())} pts moved, up to '
                       f'{nm_.max():.2f} (clearance {clear_}, blend {sig_})')
    return moved


def _lift_off(P, BP, BT, clear, sigma, axis, passes=10, movable=None):
    """v7: move the points of P that sit inside or within `clear` of the surface (BP, BT; outward winding) out along the nearest face's
    normal (never in towards the axis) to `clear`, each move blended onto the points within ~sigma of it (the largest weighted move wins);
    P is moved in place; returns the total move per point. movable (2026-10-13, design key crest_root_hanging): only these points need or
    take a move - the rest (a deep head-bound insertion the author drew inside the helmet) stay where drawn"""
    total = np.zeros_like(P); mv_ = np.ones(len(P), bool) if movable is None else np.asarray(movable, bool)
    for _ in range(passes):
        sd, lat, nrm = _sd_n(P, BP, BT); nrm = _outward(nrm, P, axis)
        need = np.where((lat < 1.0) & mv_, np.maximum(0.0, clear - sd), 0.0)
        if need.max() < 0.005: break
        src = np.where(need > 0.005)[0]; off = np.zeros_like(P)
        for s0 in range(0, len(P), 500):
            D = np.linalg.norm(P[s0:s0 + 500, None, :] - P[None, src, :], axis=2); wgt = need[None, src] * np.exp(-(D / sigma) ** 2)
            j = wgt.argmax(1); off[s0:s0 + 500] = wgt[np.arange(len(j)), j][:, None] * nrm[src[j]]
        off[~mv_] = 0.0
        P += off; total += off
    return total


def _shared_sel(shared, key, own, log, vname, what):
    """v6d: a point selection shared by a _0 / _1 pair - the _1 build stores its own, the _0 build reuses it (the game blends the
    two meshes shape by shape at load and needs equal vertex counts); the _0's own selection is compared and logged"""
    own = np.asarray(own)
    if key not in shared:
        shared[key] = own; return own
    sel = shared[key]; miss = len(set(own.tolist()) - set(sel.tolist()))
    log.append(f'{vname}: {what} shared with the _1 build ({len(sel)} pts; {miss} of its own {len(own)} not in it)')
    return sel


def _shared_bowl(shared, rig, t, cr, log, vname):
    bv_own, BT_own = rig.bowl_under_crest(t, cr)
    if 'bowl' not in shared:
        shared['bowl'] = (bv_own, BT_own); return bv_own, BT_own
    bv, BT = shared['bowl']; miss = len(set(bv_own.tolist()) - set(bv.tolist()))
    log.append(f'{vname}: bowl copy shared with the _1 build ({len(bv)} verts, {len(BT)} tris; {miss} of its own {len(bv_own)} verts not in it)')
    return bv, BT


def build(h, v, log, base_rig=None, shared=None):
    H = HELMETS[h]; p = H['prefix']; g = 'f' if v.lstrip('_').startswith('f') else 'm'; vname = f'{h} {v}'
    if shared is None: shared = {}          # v6d: the point / copy selections of a _0 / _1 pair (filled by the _1 build, reused by the _0)
    gw = g + ('0' if v.endswith('_0') else '')          # a _0 helmet (narrower) against the weight-0 body and the _0 cuirass builds
    src = SRC_ROOT + H['src'].format(v)
    out = STAGE + H.get('out_dir', 'meshes/nordwar/sonsofskyrim/') + H['src'].format(v).lower()
    n, T = load(src); C.to_world(T); S = {t.name: t for t in T}
    t = max(T, key=lambda x: len(x.pos))
    donor = {}
    if DONOR_ROOT and os.path.exists(DONOR_ROOT + H['src'].format(v)):
        dn, DT = load(DONOR_ROOT + H['src'].format(v)); donor = {x.name: x for x in DT}
    # 2026-10-14 FLEET PERF (user: 'the three with a crest ... stay crest-only; the NoCrest variants and every other helmet static'): with
    # static_no_crest a crest helmet's variant that carries no crest shape (found as HelmRig finds it) is static on its own
    cfg_ = H.get('crest')
    no_crest_ = bool(H.get('static_no_crest') and cfg_ and not any(u.name == cfg_['shape'] or u.name.lower().startswith(cfg_['shape'].lower().split('_')[0]) for u in T))
    if H.get('static') or no_crest_:         # 2026-10-13 PERF (PLAN_PERF_WHITERUN.md 3): a STATIC helmet - the author's shapes and weights with the PBR donor's
        # shader (same file name, so no PG run), no rig bones, no HDT link, no XML: FSMP never builds a system for it
        os.makedirs(os.path.dirname(out), exist_ok=True)
        w = Writer(n, out); w.skel_G = {}
        for u in T:
            for nm, xf in u.s2b.items(): w.skel_G.setdefault(nm, np.linalg.inv(C.tb2m(xf)))
        w.custom_G, w.parent = {}, {}
        nb = {}
        for u in T:
            nb[u.name] = w.emit(u.name, u.pos, u.uv, u.norm, u.tris, u.s.flags, list(C.part_ids(u, T)), [C.top4(x) for x in u.w], u.s2b,
                                shader_from=donor.get(u.name, u), colors=[tuple(c) for c in u.s.colors] if u.s.colors else None)
        w.out.save()
        log.append(f'{vname}: STATIC (no physics by design): wrote {out.replace(STAGE, "")}; shapes {sorted(nb)}' + (' (PBR donor shader)' if donor else ' (NO donor - author shader)'))
        return dict(out=out, static=True, has_flap=False, xml=None, g=g, shape=t.name, donor=bool(donor)), None
    rig = HelmRig(t, H, [], vname, base=base_rig, T=T)             # a first pass only finds the hanging parts ...
    settled = settle_curtain(t, rig, gw, log, vname, T=T)           # ... which are settled off every cuirass collider (v4) ...
    rig = HelmRig(t, H, log, vname, base=base_rig, T=T)            # ... and the rig is built on the settled curtain
    if H.get('crest_from') and rig.crest:
        # 2026-10-13 (the Whiterun horsetail, user: 'rebuild the whiterun helmet properly so the only smp is the plume. with proper collisions'):
        # the crest's resting SHAPE, weights and bones from a frozen nif (crest_sources/: the build worn in game since 10-12, its shape never
        # reported) - today's settle / root lift fit this helmet's back channel worse (strands dragged into it: 1-6 moving pts inside at the
        # sideways corners, 3-5 resting in the bowl copy). Everything else is built here as usual: the bowl copy and its v8b drop and rest pull
        # on THIS shape, the Crest Points, the XML (stops, springs, collider)
        import re as _re
        ni_, Ti_ = load(H['crest_from'].format(v)); C.to_world(Ti_)
        cr_ = next(u for u in T if u.name == rig.crest['shape']); ci_ = next(u for u in Ti_ if u.name == cr_.name)
        if len(ci_.pos) != len(cr_.pos): raise RuntimeError(f'{vname}: crest_from {cr_.name} has {len(ci_.pos)} pts, the source {len(cr_.pos)}')
        cr_.pos[:] = ci_.pos; rig.crest_w_from = [dict(x) for x in ci_.w]
        nb_ = 0
        for nm_, nd_ in ni_.nodes.items():
            if _re.fullmatch(rf'{p} Crest\d+ \d+', nm_) and nm_ in rig.G: rig.G[nm_] = C.tb2m(nd_.global_transform); nb_ += 1
        if nb_ != sum(1 for k in rig.G if k.startswith(f'{p} Crest')): raise RuntimeError(f'{vname}: crest_from has {nb_} of the rig\'s crest bones')
        log.append(f'{vname}: crest shape, weights and {nb_} bones from {os.path.basename(H["crest_from"].format(v))} (frozen)')
    W = rig.weights(t, log)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    w = Writer(n, out); w.skel_G = {}
    for u in T:
        for nm, xf in u.s2b.items(): w.skel_G.setdefault(nm, np.linalg.inv(C.tb2m(xf)))
    w.custom_G = dict(rig.G); w.parent = dict(rig.parent)
    if HEAD not in w.out.nodes: w.out.add_node(HEAD, C.m2tb(w.skel_G[HEAD]), w.out.root)
    for nm in sorted(rig.G, key=lambda x: (int(x.split()[-1]), x)):
        par = rig.parent[nm]; Gp = rig.G[par] if par in rig.G else w.skel_G[par]
        w.out.add_node(nm, C.m2tb(np.linalg.inv(Gp) @ rig.G[nm]), w.out.nodes[par])
    nb = {}
    CW = (getattr(rig, 'crest_w_from', None) or rig.crest_weights(next(u for u in T if u.name == rig.crest['shape']))) if rig.crest else None
    for u in T:
        ws = W if u is t else (CW if (rig.crest and u.name == rig.crest['shape']) else u.w); pid = list(C.part_ids(u, T))
        nb[u.name] = w.emit(u.name, u.pos, u.uv, u.norm, u.tris, u.s.flags, pid, [C.top4(x) for x in ws], u.s2b, shader_from=donor.get(u.name, u),
                            colors=[tuple(c) for c in u.s.colors] if u.s.colors else None)
    pid = list(C.part_ids(t, T)); rests = {}
    if rig.has_flap:
        ang_min = 0.0 if rig.closed else float(H.get('body_ang', 55.0))
        BP, BT, BWt, bs2b, rest_b, bsel = body_collider(gw, rig, t, log, vname, ang_min, tri_sel=shared.get('body_sel'))
        shared.setdefault('body_sel', bsel)
        for nm_, xf in bs2b.items(): w.skel_G.setdefault(nm_, np.linalg.inv(C.tb2m(xf)))
        nb[f'{p} Body Collide'] = w.emit(f'{p} Body Collide', BP, np.zeros((len(BP), 2)), None, BT, 0xe, [pid[0]] * len(BT), [C.top4(x) for x in BWt], bs2b)
        rests['body'] = rest_b
        gv = np.r_[rig.curtain_v, rig.lining_v]
        gp_own = gv[rig.phys_share[gv] > H.get('guard_phys_min', GUARD_PHYS_MIN)]   # v4: per design - the Officer pelt's first row under the welded rim lies ON a cuirass collar and cannot be settled (the rim is pinned): not a collision point
        gp = _shared_sel(shared, 'gp', gp_own, log, vname, 'guard points')
        rmg = np.full(len(t.pos), -1); rmg[gp] = np.arange(len(gp))
        gt = rmg[t.tris[(rmg[t.tris] >= 0).all(1)]]
        if rig.crest:                                   # v3: the crest's hanging points meet the body copy and the cuirass too; v5: and the bowl
            cr = next(u for u in T if u.name == rig.crest['shape']); cv_own = np.array([i for i in np.where(rig.crest['hang'])[0] if 1.0 - CW[i].get(HEAD, 0.0) > CREST_PHYS_MIN])   # v5b: the root band is not a collision point
            cv = _shared_sel(shared, 'cv', cv_own, log, vname, 'crest points')
            rmc = np.full(len(cr.pos), -1); rmc[cv] = np.arange(len(cv)); ct_ = rmc[cr.tris[(rmc[cr.tris] >= 0).all(1)]]
            nb[f'{p} Crest Points'] = w.emit(f'{p} Crest Points', cr.pos[cv], np.zeros((len(cv), 2)), None, ct_, 0xe, [pid[0]] * max(len(ct_), 1) if len(ct_) else [], [C.top4(CW[i]) for i in cv], cr.s2b)
            bv, BT = _shared_bowl(shared, rig, t, cr, log, vname)
            BPc = t.pos[bv]
            if H.get('bowl_pull') and len(BT) and len(cv):    # 2026-10-13 (the Whiterun horsetail with the bowl collider): the resting tail lay 0.08 off the
                # copy (the root lift's clearance) inside the margins (bowl + points) - a contact every frame (Rule 1). As every coat copy: the copy
                # pulled in under the resting collision points to the margins + 0.05 (at most 2.0), decided on this variant's own rest pose
                bcl_ = H.get('bowl_margin', BOWL_MARGIN) + 0.1 + 0.05
                from coat import build_coat_rig as _CB         # the coat copies' exact pass: every triangle a point sits over (or behind, within the catch)
                pen_b, m_b, ndrop_ = float(H.get('bowl_pen', BOWL_PEN)), float(H.get('bowl_margin', BOWL_MARGIN)) + 0.1, 0
                for _it in range(6):
                    BPc, boff_ = C.pull_in(t.pos[bv], BT, cr.pos[cv], bcl_, 2.0)
                    boff_ = _CB.pull_exact(t.pos[bv], BT, boff_, cr.pos[cv], bcl_, pen=pen_b)
                    BPc = t.pos[bv] - boff_[:, None] * _CB.K.vertex_normals(t.pos[bv], BT)
                    if not H.get('bowl_drop_contact'): break
                    # the v8b drop again ON THE PULLED copy: a face pulled in shares its corners with its neighbours, so a side wall next to faces
                    # pulled under the tail moves toward a strand resting BEHIND it (the Whiterun channel walls: 1.1-1.6 deep after the pull)
                    fq_ = np.cross(BPc[BT[:, 1]] - BPc[BT[:, 0]], BPc[BT[:, 2]] - BPc[BT[:, 0]]); fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12
                    tri_, _, d_, cp_ = C.Surface([('s', BPc, BT)]).query(cr.pos[cv], k=24)
                    sd_ = ((cr.pos[cv] - cp_) * fq_[tri_]).sum(1); lt_ = np.sqrt(np.maximum(d_ ** 2 - sd_ ** 2, 0.0))
                    hit_ = (sd_ < 0.0) & (sd_ > -pen_b) & (lt_ < m_b)
                    if not hit_.any(): break
                    keep_ = np.ones(len(BT), bool); keep_[np.unique(tri_[hit_])] = False; ndrop_ += int((~keep_).sum())
                    gt_ = bv[BT[keep_]]; bv = np.unique(gt_); rmb_ = np.full(len(t.pos), -1); rmb_[bv] = np.arange(len(bv)); BT = rmb_[gt_]
                log.append(f'{vname}: bowl copy pulled in under the resting tail to {bcl_:.2f} clear: {int((boff_ > 0.005).sum())} of {len(bv)} pts, max {boff_.max():.2f}'
                           + (f'; {ndrop_} faces with a tail pt behind them after the pull dropped' if ndrop_ else ''))
            nb[f'{p} Bowl Collide'] = w.emit(f'{p} Bowl Collide', BPc, np.zeros((len(bv), 2)), None, BT, 0xe, [pid[0]] * max(len(BT), 1) if len(BT) else [], [C.top4(W[i]) for i in bv], t.s2b)
        nb[f'{p} Guard Points'] = w.emit(f'{p} Guard Points', t.pos[gp], np.zeros((len(gp), 2)), None, gt, 0xe, [pid[0]] * max(len(gt), 1) if len(gt) else [], [C.top4(W[i]) for i in gp], t.s2b)
    else:
        filler_ = not (rig.crest and not H.get('flap', True))      # 2026-10-13 PERF: a crest-only helmet (flap=False) needs no filler points - its crest's are the system
        pv_own = rig.plates[0] if rig.plates else np.arange(min(40, len(t.pos)))
        pv = _shared_sel(shared, 'pv', pv_own, log, vname, 'points') if filler_ else np.zeros(0, int)
        rm = np.full(len(t.pos), -1); rm[pv] = np.arange(len(pv)); pt = rm[t.tris[(rm[t.tris] >= 0).all(1)]]
        if filler_: nb[f'{p} Points'] = w.emit(f'{p} Points', t.pos[pv], np.zeros((len(pv), 2)), None, pt, 0xe, [pid[0]] * max(len(pt), 1) if len(pt) else [], [C.top4(W[i]) for i in pv], t.s2b)
        if rig.crest:                                   # v5: a tail on a helmet without a flap skirt
            cr = next(u for u in T if u.name == rig.crest['shape']); cv_own = np.array([i for i in np.where(rig.crest['hang'])[0] if 1.0 - CW[i].get(HEAD, 0.0) > CREST_PHYS_MIN])   # v5b: the root band is not a collision point
            cv = _shared_sel(shared, 'cv', cv_own, log, vname, 'crest points')
            rmc = np.full(len(cr.pos), -1); rmc[cv] = np.arange(len(cv)); ct_ = rmc[cr.tris[(rmc[cr.tris] >= 0).all(1)]]
            nb[f'{p} Crest Points'] = w.emit(f'{p} Crest Points', cr.pos[cv], np.zeros((len(cv), 2)), None, ct_, 0xe, [pid[0]] * max(len(ct_), 1) if len(ct_) else [], [C.top4(CW[i]) for i in cv], cr.s2b)
            bv, BT = _shared_bowl(shared, rig, t, cr, log, vname)
            BPc = t.pos[bv]
            if H.get('bowl_pull') and len(BT) and len(cv):    # 2026-10-13 (the Whiterun horsetail with the bowl collider): the resting tail lay 0.08 off the
                # copy (the root lift's clearance) inside the margins (bowl + points) - a contact every frame (Rule 1). As every coat copy: the copy
                # pulled in under the resting collision points to the margins + 0.05 (at most 2.0), decided on this variant's own rest pose
                bcl_ = H.get('bowl_margin', BOWL_MARGIN) + 0.1 + 0.05
                from coat import build_coat_rig as _CB         # the coat copies' exact pass: every triangle a point sits over (or behind, within the catch)
                pen_b, m_b, ndrop_ = float(H.get('bowl_pen', BOWL_PEN)), float(H.get('bowl_margin', BOWL_MARGIN)) + 0.1, 0
                for _it in range(6):
                    BPc, boff_ = C.pull_in(t.pos[bv], BT, cr.pos[cv], bcl_, 2.0)
                    boff_ = _CB.pull_exact(t.pos[bv], BT, boff_, cr.pos[cv], bcl_, pen=pen_b)
                    BPc = t.pos[bv] - boff_[:, None] * _CB.K.vertex_normals(t.pos[bv], BT)
                    if not H.get('bowl_drop_contact'): break
                    # the v8b drop again ON THE PULLED copy: a face pulled in shares its corners with its neighbours, so a side wall next to faces
                    # pulled under the tail moves toward a strand resting BEHIND it (the Whiterun channel walls: 1.1-1.6 deep after the pull)
                    fq_ = np.cross(BPc[BT[:, 1]] - BPc[BT[:, 0]], BPc[BT[:, 2]] - BPc[BT[:, 0]]); fq_ /= np.linalg.norm(fq_, axis=1, keepdims=True) + 1e-12
                    tri_, _, d_, cp_ = C.Surface([('s', BPc, BT)]).query(cr.pos[cv], k=24)
                    sd_ = ((cr.pos[cv] - cp_) * fq_[tri_]).sum(1); lt_ = np.sqrt(np.maximum(d_ ** 2 - sd_ ** 2, 0.0))
                    hit_ = (sd_ < 0.0) & (sd_ > -pen_b) & (lt_ < m_b)
                    if not hit_.any(): break
                    keep_ = np.ones(len(BT), bool); keep_[np.unique(tri_[hit_])] = False; ndrop_ += int((~keep_).sum())
                    gt_ = bv[BT[keep_]]; bv = np.unique(gt_); rmb_ = np.full(len(t.pos), -1); rmb_[bv] = np.arange(len(bv)); BT = rmb_[gt_]
                log.append(f'{vname}: bowl copy pulled in under the resting tail to {bcl_:.2f} clear: {int((boff_ > 0.005).sum())} of {len(bv)} pts, max {boff_.max():.2f}'
                           + (f'; {ndrop_} faces with a tail pt behind them after the pull dropped' if ndrop_ else ''))
            nb[f'{p} Bowl Collide'] = w.emit(f'{p} Bowl Collide', BPc, np.zeros((len(bv), 2)), None, BT, 0xe, [pid[0]] * max(len(BT), 1) if len(BT) else [], [C.top4(W[i]) for i in bv], t.s2b)
    xml_rel = XD + H['xml'] + ('' if (rig.has_flap or not H.get('flap', True)) else 'NoGuard') + ('' if (rig.kind or None) == (H.get('cheeks') or None) else 'NoCheeks') + ('NoCrest' if H.get('crest') and not rig.crest else '') + '.xml'
    NiStringExtraData.New(w.out, name='HDT Skinned Mesh Physics Object', string_value=xml_rel, parent=w.out.root)
    w.out.save()
    log.append(f'{vname}: wrote {out.replace(STAGE, "")}; bones per shape {nb}')
    return dict(out=out, has_flap=rig.has_flap, rests=rests, settled=settled, shape=t.name, kind=rig.kind, n_chains=rig.n_chains if rig.has_flap else 0,
                closed=bool(rig.closed) if rig.has_flap else None, flap_uk=[float(x) for x in rig.flap_uk] if rig.has_flap else None, axis=[rig.cx, rig.cy], bones={nm: x.tolist() for nm, x in rig.G.items()}, parent=rig.parent,
                curtain=len(rig.curtain_v), lining=len(rig.lining_v), plates=[len(v_) for v_ in rig.plates], xml=xml_rel, g=g,
                crest=dict(shape=rig.crest['shape'], n=rig.crest['n'], chains=rig.crest['chains'], pts=int(rig.crest['hang'].sum())) if rig.crest else None), rig


def write_xml(h, rel, has_flap, kind, n_chains, closed, flap_uk, body_margin, skel, log, crest_n=0, crest_c=1):
    H = HELMETS[h]; p = H['prefix']; tg = p.lower(); shape = C.shape; crest = lambda c, r: f'{p} Crest{c} {r}'
    CD, C1, C2 = H.get('crest_def', CREST_DEF), H.get('crest_lim1', CREST_LIM1), H.get('crest_lim', CREST_LIM)
    FD, F1, F2 = H.get('flap_def', FLAP_DEF), H.get('flap_lim1', FLAP_LIM1), H.get('flap_lim', FLAP_LIM); LK = H.get('flap_link', FLAP_LINK)
    PD, PL = H.get('plate_def', PLATE_DEF), H.get('plate_lim', PLATE_LIM)
    flap = lambda k, r: f'{p} Guard{k} {r}'; plate = lambda k, r: f'{p} Cheek{k} {r}'
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<!-- {H["title"]} ({"with its flap skirt" if has_flap else "variants without a flap skirt"}; every race, men + women): physics made 2026-10-11 for this',
         '     LoreRim setup (the helmet had none). Mesh, UVs and textures are the author\'s, unchanged - only weights, bones and this link.']
    cc = H.get('cuirass_collide', True); ring = bool(closed) and H.get('link_round', True); bc = H.get('body_collide', True)
    if has_flap and cc:
        L += [f'     Flap skirt: {n_chains} chains hanging from the rim{" all round" if closed else " round the back and sides"}, {FLAP_ROWS} bones each - light leather, damped so',
              '     it trails when the wearer walks: a free swing out and backward at the back and sides, next to none forward (the front',
              '     presses on the chest, never caving in over the face), never in towards the neck; loose links let it ripple. It rides over',
              '     the wearer\'s body (a hidden copy in this mesh, nothing touches at rest) and over the cuirass worn with it: the Sons of',
              f'     Skyrim cuirasses carry a public collider tagged {CUIRASS_TAG} that names this skirt\'s tag {HELM_TAG} (FSMP matches shapes',
              '     across files on one skeleton); the resting skirt was settled clear of every one of those colliders.']
    elif has_flap:
        L += [f'     Flap skirt: {n_chains} chains hanging from the rim{" all round" if closed else " round the back and sides"}, {FLAP_ROWS} bones each - heavy leather / mail',
              '     that barely moves (the Realistic Armor Mercenary recipe, v6): a small swing out and a hair sideways, never in towards the neck,',
              '     firm springs, no wind; tight links make it one piece. It meets only the wearer\'s body round the neck (a hidden copy in this',
              '     mesh, nothing touches at rest) and keeps the author\'s drawn pose: by design it does NOT collide with the cuirass worn with it',
              '     (a tall collar is clipped a little, as the author\'s rigid mesh did) - its points and the body copy are private to this file.']
    if kind:
        L += ['     Cheek guards: rigid, each on one bone hinged along its top edge (the whole edge, sloping where it slopes) - a little out, a hair',
              '     in, a hair fore / aft; firm springs bring them back.']
    if not H.get('flap', True): L += ['     2026-10-13 (performance): the flap skirt is OFF by design - it keeps the author\'s weights (head / neck); only the tail moves.']
    if crest_n: L += [f'     Tail: hair on {crest_c} chain(s) of {crest_n} bones from its root down the tail (after the Realistic Armor ponytail) - weighty, damped, swinging',
                      '     out and sideways, never in; the springs rest a little outward so it hangs just off the bowl, which it collides with (a hidden copy).']
    L += ['     Swing limits per joint: X = out/in (negative = outward), Y = sideways, Z = twist. Tuning: edit, save, "smp reset". -->',
          '<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="description.xsd">', '',
          '\t<!-- kinematic: the head, the body bones the collision shapes are skinned to, and the pinned top bone of every chain / hinge -->']
    L += [f'\t<bone name="{b}"/>' for b in skel]
    if kind: L += [f'\t<bone name="{plate(k, 0)}"/>' for k in range(2)]
    if has_flap: L += [f'\t<bone name="{flap(k, 0)}"/>' for k in range(n_chains)]
    if crest_n: L += [f'\t<bone name="{crest(c, 0)}"/>' for c in range(crest_c)]
    if has_flap:
        L += [''] + C.bone_default(FD, H.get('flap_note', 'flap skirt: light leather, lightly damped - a free swing'))
        L += [f'\t<bone name="{flap(k, r)}"/>' for r in range(1, FLAP_ROWS + 1) for k in range(n_chains)]
    if crest_n:
        L += [''] + C.bone_default(CD, 'crest: hair, light and free')
        L += [f'\t<bone name="{crest(c, r)}"/>' for r in range(1, crest_n + 1) for c in range(crest_c)]
    if kind:
        L += [''] + C.bone_default(PD, 'cheek guards: hinged plates, no wind')
        L += [f'\t<bone name="{plate(k, 1)}"/>' for k in range(2)]
    if has_flap:
        L += ['', f'\t<!-- flap skirt, joint limits per chain (X out/in: negative = out; Y sideways: the larger side trails the hem BACKWARD; Z twist): out',
              f'\t     {F1["out_back"]} at the back to {F1["out_front"]} at the front (rim) / {F2["out_back"]} to {F2["out_front"]} (lower), backward {F1["back"]} / {F2["back"]}, forward {F1["fwd"]} / {F2["fwd"]} -->']
        for k in range(n_chains):
            phi = float(wrap(flap_uk[k] + 180.0)); l1 = flap_limits(F1, phi); l2 = flap_limits(F2, phi)
            side = 'front' if abs(phi) < 30 else 'back' if abs(phi) > 150 else ('right' if phi > 0 else 'left')
            L += C.chain_default_xyz(l1, f'chain {k} ({side}, {phi:.0f} deg) at the rim: out {-l1["lo"][0]}, sideways {-l1["lo"][1]} / +{l1["hi"][1]}, twist {l1["hi"][2]}')
            L.append('\t<constraint-group>'); L.append(f'\t\t<generic-constraint bodyA="{flap(k, 1)}" bodyB="{flap(k, 0)}"/>'); L.append('\t</constraint-group>')
            L += C.chain_default_xyz(l2, f'chain {k}, lower joints: out {-l2["lo"][0]}, sideways {-l2["lo"][1]} / +{l2["hi"][1]}')
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{flap(k, r)}" bodyB="{flap(k, r - 1)}"/>' for r in range(2, FLAP_ROWS + 1)]; L.append('\t</constraint-group>')
        L += C.link_default(LK[0], LK[1], 'flap skirt, side by side: one piece of leather' + (' that may ripple' if LK[0] >= 0.3 else ', no ripple')
                            + (' (linked all round)' if ring else ' (the ring left open at the front seam: a closed loop of links is over-constrained)' if closed else ''))
        pairs = [(k, k + 1) for k in range(n_chains - 1)] + ([(n_chains - 1, 0)] if ring else [])
        for r in range(1, FLAP_ROWS + 1):
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{flap(b, r)}" bodyB="{flap(a, r)}"/>' for a, b in pairs]; L.append('\t</constraint-group>')
    if crest_n:
        L += C.chain_default_xyz(C1, f'tail, at the root: out (backward) {-C1["lo"][0]}, ' + (f'in {C1["hi"][0]}' if C1["hi"][0] >= 0 else f'never back to the drawn pose (its stop {-C1["hi"][0]} out)') + f', sideways {C1["hi"][1]}, twist {C1["hi"][2]}; springs rest {-C1.get("eq", (0,))[0]} out')
        L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{crest(c, 1)}" bodyB="{crest(c, 0)}"/>' for c in range(crest_c)]; L.append('\t</constraint-group>')
        if crest_n > 1:
            L += C.chain_default_xyz(C2, f'tail, down its length: out {-C2["lo"][0]}, ' + (f'in {C2["hi"][0]}' if C2["hi"][0] >= 0 else f'stop {-C2["hi"][0]} out of the drawn pose') + f', sideways {C2["hi"][1]}')
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{crest(c, r)}" bodyB="{crest(c, r - 1)}"/>' for c in range(crest_c) for r in range(2, crest_n + 1)]; L.append('\t</constraint-group>')
        if crest_c > 1:
            L += C.link_default(CREST_LINK[0], CREST_LINK[1], 'tail, its chains side by side: one hank of hair')
            L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{crest(c + 1, r)}" bodyB="{crest(c, r)}"/>' for r in range(1, crest_n + 1) for c in range(crest_c - 1)]; L.append('\t</constraint-group>')
    if kind:
        L += C.chain_default_xyz(PL, f'cheek guards, hinge along the top edge: out up to {-PL["lo"][0]} rad, in {PL["hi"][0]}, fore/aft {PL["hi"][1]}, barely twisting; firm springs bring them back')
        L.append('\t<constraint-group>'); L += [f'\t\t<generic-constraint bodyA="{plate(k, 1)}" bodyB="{plate(k, 0)}"/>' for k in range(2)]; L.append('\t</constraint-group>')
    if has_flap and cc:
        L += ['', f'\t<!-- collisions: the flap skirt vs the wearer\'s body round the neck (a hidden copy in this mesh, margin {body_margin}; nothing touches at',
              f'\t     rest) and vs the cuirass worn with it - its own file\'s public collider tagged {CUIRASS_TAG} (the Sons of Skyrim builds); the points are',
              '\t     public and name both, the body copy names only them -->']
        L += shape('per-triangle-shape', f'{p} Body Collide', tg + 'Body', body_margin, can=(HELM_TAG,), pen=BODY_PEN)
        L += shape('per-vertex-shape', f'{p} Guard Points', HELM_TAG, 0.1, can=(tg + 'Body', CUIRASS_TAG), shared='public')
        if crest_n:
            L += shape('per-vertex-shape', f'{p} Crest Points', (HELM_TAG, tg + 'Crest'), 0.1, can=(tg + 'Body', CUIRASS_TAG, tg + 'Bowl'), shared='public')
            L += shape('per-triangle-shape', f'{p} Bowl Collide', tg + 'Bowl', BOWL_MARGIN, can=(tg + 'Crest',), pen=BOWL_PEN)
    elif has_flap and bc:                              # v6 subtle: private on both sides, its own tag - the cuirasses' public colliders (which name
        L += ['', f'\t<!-- collisions: the flap skirt vs the wearer\'s body round the neck only (a hidden copy in this mesh, margin {body_margin}; nothing',      # the pair tag) cannot pair with it
              '\t     touches at rest); both private to this file with their own tags - by design no cuirass collision (v6 subtle) -->']
        L += shape('per-triangle-shape', f'{p} Body Collide', tg + 'Body', body_margin, can=(tg + 'Guard',), pen=BODY_PEN)
        L += shape('per-vertex-shape', f'{p} Guard Points', tg + 'Guard', 0.1, can=(tg + 'Body',))
        if crest_n:
            L += shape('per-vertex-shape', f'{p} Crest Points', tg + 'Crest', 0.1, can=(tg + 'Body', tg + 'Bowl'))
            L += shape('per-triangle-shape', f'{p} Bowl Collide', tg + 'Bowl', BOWL_MARGIN, can=(tg + 'Crest',), pen=BOWL_PEN)
    elif has_flap:                                     # v6b: NO collider at all - the skirt and the tail move on their springs and limits alone
        L += ['', '\t<!-- collisions: none, by design (v6b subtle). The author draws the skirt hugging the neck; with the body copy as a collider the',
              '\t     idle breathing pushed its points every frame (twitching). The limits never let it swing in past the drawn pose, so',
              '\t     nothing needs catching; the points are declared only so the system is well-formed, and meet nothing -->']
        L += shape('per-vertex-shape', f'{p} Guard Points', tg + 'Guard', 0.1, can=(tg + 'Nothing',))
        if crest_n and H.get('crest_collide'):          # v8 (Riften plume, 2026-10-13): the tail meets the BOWL (kinematic with the head - no breathing
            L += ['	<!-- v8: the tail meets its own copy of the bowl (head-bound, so nothing breathes under it): a tail leaning on a cone is held',   # under it), private, deep catch
                  '	     by contact, not by its joint stops alone; the flap skirt still meets nothing -->']
            L += shape('per-vertex-shape', f'{p} Crest Points', tg + 'Crest', 0.1, can=(tg + 'Bowl',))
            L += shape('per-triangle-shape', f'{p} Bowl Collide', tg + 'Bowl', H.get('bowl_margin', BOWL_MARGIN), can=(tg + 'Crest',), pen=H.get('bowl_pen', BOWL_PEN))
        elif crest_n: L += shape('per-vertex-shape', f'{p} Crest Points', tg + 'Crest', 0.1, can=(tg + 'Nothing',))
    else:
        if H.get('flap', True) or not crest_n:         # 2026-10-13 PERF: a crest-only helmet's crest points keep the system well-formed
            L += ['', '\t<!-- a few moving points as a collision shape that meets nothing (keeps the system well-formed) -->']
            L += shape('per-vertex-shape', f'{p} Points', tg + 'Pts', 0.1, can=(tg + 'Nothing',))
        if crest_n and cc:                             # v5: a tail on a helmet without a flap skirt
            L += shape('per-vertex-shape', f'{p} Crest Points', (HELM_TAG, tg + 'Crest'), 0.1, can=(CUIRASS_TAG, tg + 'Bowl'), shared='public')
            L += shape('per-triangle-shape', f'{p} Bowl Collide', tg + 'Bowl', BOWL_MARGIN, can=(tg + 'Crest',), pen=BOWL_PEN)
        elif crest_n and bc:                           # v6: the tail meets the bowl only, private
            L += shape('per-vertex-shape', f'{p} Crest Points', tg + 'Crest', 0.1, can=(tg + 'Bowl',))
            L += shape('per-triangle-shape', f'{p} Bowl Collide', tg + 'Bowl', BOWL_MARGIN, can=(tg + 'Crest',), pen=BOWL_PEN)
        elif crest_n and H.get('crest_collide'):       # v8: the tail meets the bowl only, private, deep catch
            L += shape('per-vertex-shape', f'{p} Crest Points', tg + 'Crest', 0.1, can=(tg + 'Bowl',))
            L += shape('per-triangle-shape', f'{p} Bowl Collide', tg + 'Bowl', H.get('bowl_margin', BOWL_MARGIN), can=(tg + 'Crest',), pen=H.get('bowl_pen', BOWL_PEN))
        elif crest_n:                                  # v6b: the tail meets nothing
            L += shape('per-vertex-shape', f'{p} Crest Points', tg + 'Crest', 0.1, can=(tg + 'Nothing',))
    L += ['</system>', '']
    path = STAGE + rel.replace('\\', '/'); os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f: f.write('\n'.join(L))
    log.append(f'wrote {rel} ({len(L)} lines)')


def main(helmets):
    rp = WORK + 'helmets_report.json'; allrep = json.load(open(rp)) if os.path.exists(rp) else {}; log = []
    try: _main(helmets, rp, allrep, log)
    finally:
        open(WORK + 'helmets_build.log', 'w', encoding='utf-8').write('\n'.join(log) + '\n'); print('\n'.join(log))


def _main(helmets, rp, allrep, log):
    for h in helmets:
        H = HELMETS[h]; log.append(f'===== {H["title"]}'); rep = {}; rigs = {}; sels = {}
        for v in [x for x in H['variants'] if not VARIANTS or x in VARIANTS]:      # 2026-10-13: --variants= (men only: m,ma,mk,mo)
            base = rigs.get(v[:-2]) if v.endswith('_0') else None
            shared = sels.setdefault(v[:-2], {}) if v.endswith(('_0', '_1')) else {}     # v6d: a _0 / _1 pair shares its point / copy selections
            r, rig = build(h, v, log, base_rig=base, shared=shared)
            if v.endswith('_1'): rigs[v[:-2]] = rig
            rep[v] = r
            if r['has_flap'] and '_n_chains' not in H: H['_n_chains'] = r['n_chains']; H['_closed'] = r['closed']; H['_flap_uk'] = r['flap_uk']
        if H.get('static') or all(r.get('static') for r in rep.values()):
            allrep[h] = dict(variants=rep, static=True, margin=None); json.dump(allrep, open(rp, 'w'), indent=1)
            log.append(f'{h}: static - no XML (the mod\'s {H["xml"]}.xml is no longer named by these variants)'); continue
        st_ = {v: r for v, r in rep.items() if r.get('static')}     # 2026-10-14: static_no_crest variants - no XML; the rest as before
        if st_:
            log.append(f'{h}: static (no crest shape): {", ".join(sorted(st_))} - no XML'); rep = {v: r for v, r in rep.items() if not r.get('static')}
        # the body collider's margin stands for a cuirass's thickness; a curtain resting closer gets less, so nothing touches at rest
        rests = [r['rests']['body'] for r in rep.values() if r.get('rests', {}).get('body') is not None]
        margin = round(max(0.15, min(BODY_MARGIN_MAX, min(rests) - BODY_REST_CLEAR)), 2) if rests else BODY_MARGIN_MAX   # (an Orc variant's curtain hangs closer to the human body proxy)
        if rests: log.append(f'{h}: the curtain rests {min(rests):.2f} .. {max(rests):.2f} off the body -> body collider margin {margin}')
        if rests and min(rests) < 0.26: raise RuntimeError(f'{h}: the curtain rests too close to the body for a margin ({min(rests):.2f})')
        # one XML per kind of variant (with / without a flap skirt, with / without cheek guards): every variant sharing it must agree
        for xml_rel in sorted({r['xml'] for r in rep.values()}):
            vs = [v for v, r in rep.items() if r['xml'] == xml_rel]
            kinds = {(r['has_flap'], r['kind'], r['n_chains'], r['closed'], tuple(r['flap_uk'] or ()), (r.get('crest') or {}).get('n', 0), (r.get('crest') or {}).get('chains', 0)) for v in vs for r in [rep[v]]}
            if len(kinds) != 1: raise RuntimeError(f'{h}: variants sharing {xml_rel} differ: {kinds}')
            hf, kind, n_chains, closed, flap_uk, crest_n, crest_c = next(iter(kinds))
            skel = {HEAD}
            for v in vs:
                for sh in NifFile(rep[v]['out']).shapes:
                    # 2026-10-13 (the Whiterun horsetail in game: 'its the helmet' - the plume stretched to the floor): EVERY hidden collision shape's
                    # skeleton bones are declared kinematic, not only the body copy's. The v8 bowl copy at reach 10 took neck-guard faces the author
                    # weights to Spine2; Spine2 undeclared, FSMP built no system for the helmet and its crest bones never attached (at the feet)
                    if sh.name.startswith(f'{H["prefix"]} '): skel |= {b for b in sh.bone_names if not b.startswith(f'{H["prefix"]} ')}
            write_xml(h, xml_rel, hf, kind, n_chains, closed, list(flap_uk), margin, sorted(skel, key=lambda b: (b != HEAD, b)), log, crest_n=crest_n, crest_c=crest_c)
        allrep[h] = dict(variants={**rep, **st_}, margin=margin); json.dump(allrep, open(rp, 'w'), indent=1)    # 2026-10-14: + the static variants (checked as static)     # per helmet: a later one failing keeps the earlier


VARIANTS = ()
if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    use_designs(sys.argv[1])
    VARIANTS = tuple(next((a.split('=', 1)[1].split(',') for a in sys.argv[2:] if a.startswith('--variants=')), ()))
    main([a for a in sys.argv[2:] if a in HELMETS] or list(HELMETS))
