"""helmet_check: the built helmets against their own body collider and against the cuirasses they are worn with (the cuirass builds'
own public 'Torso Collide' copies, which the helmets meet across files by tag). For each design (its men's and women's human variants):
  rest     = the flap skirt's collision points vs the body copy (FAIL within the margins: nothing may touch it at rest) and vs every
             cuirass's torso collider (v4: FAIL within the margins too - the builder settles the skirt off them); earlier: vs every
             cuirass's torso collider: points resting on it (within the margins), inside it, and of those deeper than its catch (they
             stay inside until the skirt swings; the catch pushes the rest out onto the cuirass at the first frame) - reported, not
             failed: a mail veil the author drew lying on a chest is meant to lie on it
  head poses: the head pitched back 25 / down 30, turned 40 either way, tilted 20 either way, the flap skirt carried rigidly with the
             head (the worst case: it has not reacted) vs the static body / cuirasses - caught = behind the surface within the catch
             (pushed back out), sunk = deeper than the catch (the skirt sits inside until the head comes back)
  swing    = every chain swung to its own outward limit (rows rotated about their X axis by the XML's per-chain limits): skirt points
             inside the helmet's own bowl (a flap folding back into the helmet)
Also: every custom bone declared in the XML, the hidden shapes' bones declared, _0 / _1 pairs with the same bones and point counts,
the flap skirt's points public and naming the cuirass tag, every cuirass build carrying a public torso collider that names the helmet tag.
usage: helmet_check.py <designs.py> [helmet ...]      (SUMMARY per helmet = worst sunk over the head poses, body and cuirasses)"""
import os, sys, json, re, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import build_helmet_rig as W
from smpkit import checks as K
C = W.C
HEAD = W.HEAD
TAIL_SAG = 0.05     # v7c: a draped tail pressed onto its never-in stop by gravity overshoots it in game (the v7b Riften plume, stop at the
                    # drawn pose, showed in the cone; offline 0.02 rad past it at every joint = 9 pts in, 0.03 = 28): from the stop, every
                    # joint this far IN past it must leave no moving tail point inside the helmet
POSES = [('back 25', [1.0, 0, 0], 25.0), ('down 30', [1.0, 0, 0], -30.0), ('turn L 40', [0, 0, 1.0], 40.0), ('turn R 40', [0, 0, 1.0], -40.0),
         ('tilt L 20', [0, 1.0, 0], 20.0), ('tilt R 20', [0, 1.0, 0], -20.0)]


def xml_info(path):
    s = open(path, encoding='utf-8').read(); out = {}
    for m in re.finditer(r'<(per-triangle-shape|per-vertex-shape) name="([^"]+)">(.*?)</\1>', s, re.S):
        body = m.group(3)

        def g(k, d=0.0):                                  # someone's XML may write negatives / exponents, or leave a value out
            mm = re.search(rf'<{k}>\s*([-+0-9.eE]+)\s*</{k}>', body)
            try: return float(mm.group(1)) if mm else d
            except ValueError: return d
        shared = re.search(r'<shared>([^<]+)</shared>', body)
        out[m.group(2)] = dict(kind=m.group(1), margin=g('margin'), pen=g('penetration'), shared=shared.group(1) if shared else 'public',
                               tag=re.findall(r'<tag>([^<]+)</tag>', body), can=re.findall(r'<can-collide-with-tag>([^<]+)</can-collide-with-tag>', body))
    bones = set(re.findall(r'<bone name="([^"]+)"', s))
    return out, bones


def faces(P, F):
    n = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)


def signed(Q, P, T_, lat=False):
    tri, _, d, cp = C.Surface([('s', P, T_)]).query(Q, k=24); sd = ((Q - cp) * faces(P, T_)[tri]).sum(1)
    return (sd, np.sqrt(np.maximum(d ** 2 - sd ** 2, 0.0))) if lat else sd


def behind_faces(Q, P, T_, pen, margin):
    """v8b: FSMP pushes a point along a triangle's normal when it projects into the triangle and its signed height is in (-pen, margin). A
    point BEHIND a copy face within the catch at rest is pushed through it every frame (the Riften v8 'magnet'). -> count behind, count
    resting in front within the margin"""
    A, B, Cc = P[T_[:, 0]], P[T_[:, 1]], P[T_[:, 2]]; fn = np.cross(B - A, Cc - A); fn = fn / (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
    behind = 0; front = 0
    for x in Q:
        h = ((x - A) * fn).sum(1); cand = np.where((h > -pen) & (h < margin))[0]
        if len(cand) == 0: continue
        pr = x - h[cand, None] * fn[cand]; v0 = Cc[cand] - A[cand]; v1 = B[cand] - A[cand]; v2 = pr - A[cand]
        d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); d02 = (v0 * v2).sum(1); d12 = (v1 * v2).sum(1); den = d00 * d11 - d01 * d01 + 1e-12
        u = (d11 * d02 - d01 * d12) / den; v = (d00 * d12 - d01 * d02) / den; ins = (u >= -0.08) & (v >= -0.08) & (u + v <= 1.08)
        hh = h[cand][ins]
        if len(hh) == 0: continue
        if hh.min() < 0: behind += 1
        elif hh.min() < margin: front += 1
    return behind, front


def contact(Q, P, T_, m=0.2):
    """FSMP's view of a point against a per-triangle collider (v4c): outside the surface its distance to the nearest triangle - edges
    count, so a point beyond a collider's edge is free; inside it the depth under the plane, but only where the point projects within
    the margins (m) of the triangle - beyond its edge the closest point is on the edge, farther than the margins, and FSMP lets it be;
    9 = nowhere near"""
    tri, _, d, cp = C.Surface([('s', P, T_)]).query(Q, k=24); sd = ((Q - cp) * faces(P, T_)[tri]).sum(1)
    lat = np.sqrt(np.maximum(d ** 2 - sd ** 2, 0.0))
    return np.where(sd >= 0, d, np.where(lat < m, sd, 9.0))


_CUIR = {}


def cuirasses(g, out, need=True):
    """every built cuirass of this sex with its public torso collider(s): (design, pos, tris, margin, pen); problems reported once"""
    if (g, need) in _CUIR: return _CUIR[(g, need)]
    res = []
    for ent in W.COLLARS.get(g, []):
        d, path, pre = ent[0], ent[1], ent[2]; xml = ent[3] if len(ent) > 3 else None
        if not os.path.exists(path): out.append(f'   FAIL cuirass {d}: build missing {path}'); continue
        n_, T = C.load(path); C.to_world(T)
        tc = [t for t in T if ' Torso Collide' in t.name]
        if not tc: out.append(f'   FAIL cuirass {d}: no torso collider in {os.path.basename(path)} (rebuild the coats with torso_coll)'); continue
        xs = xml_info(xml)[0] if xml and os.path.exists(xml) else {}
        for t in tc:
            x = xs.get(t.name)
            if x is None: out.append(f'   FAIL cuirass {d}: {t.name} not declared in its XML {xml}'); continue
            if x['shared'] != 'public' or W.HELM_TAG not in x['can'] or W.CUIRASS_TAG not in x['tag']:
                out.append(f'   FAIL cuirass {d}: {t.name} must be public, tagged {W.CUIRASS_TAG}, naming {W.HELM_TAG} (has {x["shared"]}, {x["tag"]}, {x["can"]})')
            res.append((d, t.pos, t.tris, x['margin'], x['pen']))
    # 2026-10-14 FLEET PERF: every cuirass is built without its public collider (nothing names the tag) - an empty list FAILs only a
    # helmet that collides with cuirasses (need); a static / crest-only helmet gets the line as info
    if not res: out.append(f'   {"FAIL" if need else "info"} no cuirass torso colliders found for {g!r}' + ('' if need else ' (none built by design; this helmet does not collide with cuirasses)'))
    _CUIR[(g, need)] = res
    return res


def check_variant(h, v, r, H, xs, xbones, out):
    p = H['prefix']; n, T = C.load(r['out']); C.to_world(T); S = {t.name: t for t in T}
    t = S[r['shape']]; ok = True; g = r['g']
    custom = set(r['bones'])
    miss = [b for b in custom if b not in xbones]
    if miss: out.append(f'   FAIL {v}: custom bones not declared in the XML: {miss[:6]}'); ok = False
    # 2026-10-13 (the Whiterun horsetail stretched to the floor in game): every bone a DECLARED collision shape is skinned to must be a declared
    # bone too - FSMP builds no system otherwise (the custom bones then never attach). The old test covered the custom bones only.
    for nm_ in [k for k in xs if k in S]:
        und_ = [b for b in (getattr(S[nm_], 's2b', None) or {}) if b not in xbones]
        if und_: out.append(f'   FAIL {v}: collision shape {nm_} is skinned to bones the XML does not declare: {und_[:4]}'); ok = False
    gp = S.get(f'{p} Guard Points'); body = S.get(f'{p} Body Collide'); cp = S.get(f'{p} Crest Points')
    crest_only = gp is None and cp is not None and not H.get('flap', True)     # 2026-10-13 PERF: flap=False by design - the crest tests only
    if gp is None and not crest_only: out.append(f'   {v}: no flap skirt (no guard points)'); return ok, 0
    if crest_only: out.append(f'   ok   {v}: crest-only by design (flap=False) - the flap skirt keeps the author\'s weights; {len(cp.pos)} crest points, the crest tests only')
    cc = H.get('cuirass_collide', True)                # v6: a design without cuirass collision must be sealed off from the cuirasses' public colliders
    if cp is not None:                                 # v3: a crest's hanging points are tested with the skirt's (same tags, same colliders)
        xc = xs.get(f'{p} Crest Points')
        if cc and (xc is None or xc['shared'] != 'public' or W.CUIRASS_TAG not in xc['can']): out.append(f'   FAIL {v}: crest points not declared public with the cuirass tag'); ok = False
        if not cc and (xc is None or xc['shared'] == 'public' or W.CUIRASS_TAG in xc['can'] or W.HELM_TAG in xc['tag']):
            out.append(f'   FAIL {v}: crest points must be private, not tagged {W.HELM_TAG}, not naming {W.CUIRASS_TAG} (no cuirass collision by design; has {xc})'); ok = False
        if crest_only: gp = cp
        else:
            gp = type('GP', (), dict(pos=np.vstack([gp.pos, cp.pos]), w=list(gp.w) + list(cp.w)))()
            out.append(f'   {v}: {len(cp.pos)} crest points tested with the {len(gp.pos) - len(cp.pos)} skirt points')
    xg = xs[f'{p} Crest Points'] if crest_only else xs[f'{p} Guard Points']; mg = xg['margin']
    if crest_only: pass
    elif cc and (xg['shared'] != 'public' or W.CUIRASS_TAG not in xg['can'] or W.HELM_TAG not in xg['tag']):
        out.append(f'   FAIL {v}: the guard points must be public, tagged {W.HELM_TAG}, naming {W.CUIRASS_TAG} (has {xg["shared"]}, {xg["tag"]}, {xg["can"]})'); ok = False
    if not crest_only and not cc and (xg['shared'] == 'public' or W.CUIRASS_TAG in xg['can'] or W.HELM_TAG in xg['tag']):
        out.append(f'   FAIL {v}: the guard points must be private, not tagged {W.HELM_TAG}, not naming {W.CUIRASS_TAG} (no cuirass collision by design; has {xg["shared"]}, {xg["tag"]}, {xg["can"]})'); ok = False
    nmb0 = f'{p} Body Collide'; bc = H.get('body_collide', True)
    if not cc and bc and nmb0 in xs and (xs[nmb0]['shared'] == 'public' or W.HELM_TAG in xs[nmb0]['can'] or not set(xs[nmb0]['can']) & set(xg['tag'])):
        out.append(f'   FAIL {v}: the body copy must be private and name the guard points\' own tag (has {xs[nmb0]["shared"]}, names {xs[nmb0]["can"]})'); ok = False
    if not bc:                                         # v6b: no collider at all - the XML may declare none, and the points must meet nothing
        crc = bool(H.get('crest_collide'))              # v8: a design with crest_collide keeps ONE collider - the tail vs its bowl copy, private, both naming only each other
        nmbw = f'{p} Bowl Collide'
        decl = [s for s, x in xs.items() if x['kind'] == 'per-triangle-shape' and not (crc and s == nmbw)]
        if decl: out.append(f'   FAIL {v}: no colliders by design, but the XML declares {decl}'); ok = False
        for nm_ in (f'{p} Guard Points', f'{p} Crest Points'):
            if nm_ not in xs: continue
            if crc and nm_.endswith('Crest Points'):
                bw = xs.get(nmbw)
                if bw is None: out.append(f'   FAIL {v}: crest_collide, but the XML declares no {nmbw}'); ok = False
                elif set(xs[nm_]['can']) != set(bw['tag'] if isinstance(bw['tag'], (list, tuple)) else [bw['tag']]) or set(bw['can']) != set(xs[nm_]['tag'] if isinstance(xs[nm_]['tag'], (list, tuple)) else [xs[nm_]['tag']]) or xs[nm_]['shared'] == 'public' or bw['shared'] == 'public':
                    out.append(f'   FAIL {v}: crest_collide: the crest points and the bowl copy must be private and name only each other (points name {xs[nm_]["can"]}, bowl names {bw["can"]})'); ok = False
                else: out.append(f'   ok   {v}: the tail meets its bowl copy only (private pair, margin {bw["margin"]}, catch {bw["pen"]}); the skirt meets nothing')
            elif any(not c.endswith('Nothing') for c in xs[nm_]['can']): out.append(f'   FAIL {v}: {nm_} must meet nothing (names {xs[nm_]["can"]})'); ok = False
    worst = 0
    # rest vs the body copy (nothing may touch); v6b: no pair - the distance is reported (the clipping to expect on a head turn starts there)
    nmb = f'{p} Body Collide'
    if body is not None and nmb in xs:
        m_, pen = xs[nmb]['margin'], xs[nmb]['pen']
        sd = contact(gp.pos, body.pos, body.tris, m_ + mg)
        touch = int((sd < m_ + mg).sum()); inside = int((sd < 0).sum())
        if touch: out.append(f'   FAIL {v}: at rest {touch} skirt pts within the margins of the body copy ({inside} inside, nearest {sd.min():+.2f})'); ok = False
        else: out.append(f'   ok   {v}: at rest the skirt sits {sd.min():+.2f} off the body copy (contact under {m_ + mg:.2f})')
    elif body is not None and not bc:
        sd = contact(gp.pos, body.pos, body.tris, 0.3)
        out.append(f'   info {v}: at rest the skirt sits {sd.min():+.2f} off the body ({int((sd < 0).sum())} pts inside it; no collision by design)')
    elif crest_only:
        out.append(f'   info {v}: crest-only - no body copy (the flap skirt it served is off by design)')
    else:
        out.append(f'   FAIL {v}: no body collider'); ok = False
    # v5: a tail's points vs the hidden bowl copy it hangs against (nothing may rest within the margins - the builder settles it clear)
    nmw = f'{p} Bowl Collide'; crp = next((t_ for t_ in T if t_.name == f'{p} Crest Points'), None)
    bowl = next((t_ for t_ in T if t_.name == nmw), None)
    if nmw in xs and crp is not None:
        if bowl is None: out.append(f'   FAIL {v}: {nmw} declared but not in the nif'); ok = False
        else:
            m_, pen = xs[nmw]['margin'], xs[nmw]['pen']; mg_c = xs.get(f'{p} Crest Points', {}).get('margin', 0.1)
            sdw = contact(crp.pos, bowl.pos, bowl.tris, m_ + mg_c); touch = int((sdw < m_ + mg_c).sum())
            if touch: out.append(f'   FAIL {v}: at rest {touch} tail pts within the margins of the bowl copy (nearest {sdw.min():+.2f})'); ok = False
            else: out.append(f'   ok   {v}: at rest the tail sits {sdw.min():+.2f} off the bowl copy (contact under {m_ + mg_c:.2f})')
            beh, frt = behind_faces(crp.pos, bowl.pos, bowl.tris, pen, m_ + mg_c)     # v8b: nothing may sit BEHIND a copy face within the catch
            if beh: out.append(f'   FAIL {v}: {beh} tail pts sit BEHIND a bowl-copy face within its catch {pen} at rest (pushed through it every frame - the v8 magnet)'); ok = False
            else: out.append(f'   ok   {v}: no tail pt behind a bowl-copy face within the catch {pen} at rest ({frt} resting in front within the margin)')
    elif crp is not None and bowl is not None and not bc:
        sdw = contact(crp.pos, bowl.pos, bowl.tris, 0.3)
        out.append(f'   info {v}: at rest the tail sits {sdw.min():+.2f} off the bowl ({int((sdw < 0).sum())} pts inside it; no collision by design)')
    # rest vs every cuirass: nothing may rest within the margins (v4: the builder settles the curtain off every collider - a point
    # resting inside one had the solver pushing it every frame, forward at the chest: the 'pull forward' of v2 / v3)
    cu = cuirasses(g, out, need=bool(cc)); rows = []; bad = 0
    for d, P_, T_, m_, pen in cu:
        sd = contact(gp.pos, P_, T_, m_ + mg)
        onit = int((sd < m_ + mg).sum()); ins = int((sd < 0).sum()); deep = int((sd < -(pen + m_ + mg)).sum())
        if onit: rows.append(f'{d} {onit} within the margins ({ins} inside, {deep} past the catch {pen:.1f}, deepest {sd.min():+.2f})'); bad += onit
    if cc and bad: out.append(f'   FAIL {v}: at rest vs the cuirasses: ' + '; '.join(rows)); ok = False
    elif cc: out.append(f'   ok   {v}: at rest clear of every cuirass collider ({len(cu)}) by its margins')
    else:    # v6: no collision pair exists - the overlap of the drawn pose with each cuirass is the clipping to expect in game, reported, not failed
        out.append(f'   info {v}: the drawn skirt vs the cuirasses it does not collide with (clipping to expect): ' + ('; '.join(rows) if rows else f'clear of all {len(cu)}'))
    # head poses: the helmet (and every custom bone, children of the head) rigid with the head; the body / cuirasses static
    hg = np.linalg.inv(C.tb2m(t.s2b[HEAD])); piv = hg[:3, 3]
    surfs = ([('body', body.pos, body.tris, xs[nmb]['margin'], xs[nmb]['pen'])] if body is not None and nmb in xs else []) + [(d, P_, T_, m_, pen) for d, P_, T_, m_, pen in cu]
    for name, axis, deg in POSES:
        M = K.rot(np.array(axis, float), np.radians(deg), piv)
        Q = (M @ np.c_[gp.pos, np.ones(len(gp.pos))].T)[:3].T
        row = []
        for d, P_, T_, m_, pen in surfs:
            sd = contact(Q, P_, T_, m_ + mg)
            caught = int(((sd < m_ + mg) & (sd > -(pen + m_ + mg))).sum()); sunk = int((sd < -(pen + m_ + mg)).sum())
            if caught or sunk: row.append(f'{d} caught {caught} sunk {sunk}')
            worst = max(worst, sunk)
        out.append(f'   {v} head {name}: ' + ('; '.join(row) if row else 'clear'))
    # chains swung to their own outward limit about their X (the rim joint's limit; lower joints their own), per chain
    if r['n_chains']:
        G = {nm: np.array(x) for nm, x in r['bones'].items()}; cx, cy = r['axis']
        F1, F2 = H.get('flap_lim1', W.FLAP_LIM1), H.get('flap_lim', W.FLAP_LIM)
        rad0 = np.hypot(gp.pos[:, 0] - cx, gp.pos[:, 1] - cy).mean()
        best = None
        for sgn in (1.0, -1.0):                       # whichever sign of the X rotation moves the skirt AWAY from the axis is 'out'
            Dm = {}
            for k in range(r['n_chains']):
                phi = float(C.wrap(r['flap_uk'][k] + 180.0)); o1 = -W.flap_limits(F1, phi)['lo'][0]; o2 = -W.flap_limits(F2, phi)['lo'][0]
                Mc = np.eye(4)
                for rr in range(1, W.FLAP_ROWS + 1):
                    b = f'{p} Guard{k} {rr}'; g0 = G[b]; ax = g0[:3, 0]; o = g0[:3, 3]
                    Mc = K.rot(ax, sgn * (o1 if rr == 1 else o2), (Mc @ np.r_[o, 1])[:3]) @ Mc; Dm[b] = Mc
            Q = K.skin(gp.pos, [dict(w) for w in gp.w], Dm); rad = np.hypot(Q[:, 0] - cx, Q[:, 1] - cy).mean()
            if best is None or rad > best[0]: best = (rad, Q)
        Q = best[1]
        bt = t.tris[np.array([all(max(t.w[i], key=t.w[i].get) == HEAD for i in tri) for tri in t.tris])]
        if len(bt):
            rm = np.full(len(t.pos), -1); hv = np.unique(bt); rm[hv] = np.arange(len(hv))
            sd = signed(Q, t.pos[hv], rm[bt]); into = int((sd < -0.3).sum())
            out.append(f'   {v} chains swung to their outward limits (hem radius {rad0:.1f} -> {best[0]:.1f}): skirt pts inside the bowl {into} (nearest {sd.min():+.2f})')
    # v6c: a tail swung to its own limits (sideways either way, out, twist either way, each joint its own) must stay OUT of the bowl copy:
    # with no bowl collider (v6b) the limits are all that keeps a draped plume from sinking into the helmet (a straight chain swung
    # sideways across a curved bowl cuts into it like a chord into a circle - the Riften plume, user's screenshot 2026-10-12)
    if r.get('crest') and crp is not None and bowl is not None:
        G = {nm: np.array(x) for nm, x in r['bones'].items()}; cr_ = r['crest']; nC, nR = int(cr_['chains']), int(cr_['n'])
        C1, C2 = H.get('crest_lim1', W.CREST_LIM1), H.get('crest_lim', W.CREST_LIM)
        worst_c = (9.0, '')

        def swung(axis_i, sgn, which):
            Dm = {}
            for c in range(nC):
                Mc = np.eye(4)
                for rr in range(1, nR + 1):
                    b = f'{p} Crest{c} {rr}'
                    if b not in G: break
                    lim = C1 if rr == 1 else C2; amp = -lim['lo'][which] if which == 0 else lim['hi'][which]
                    g0 = G[b]; ax = g0[:3, axis_i]; o = g0[:3, 3]
                    Mc = K.rot(ax, sgn * amp, (Mc @ np.r_[o, 1])[:3]) @ Mc; Dm[b] = Mc
            Q = K.skin(crp.pos, [dict(w) for w in crp.w], Dm)
            return contact(Q, bowl.pos, bowl.tris, 0.3)
        # out: the limits allow ONE sign of the X swing (the other is 'in', blocked at 0) - the allowed one is whichever moves the tail away
        # from the bowl, as the flap test decides it; sideways and twist are symmetric, both signs are tested
        o1, o2 = swung(0, 1.0, 0), swung(0, -1.0, 0); sd_out = o1 if o1.min() >= o2.min() else o2
        cases = [('out', sd_out), ('sideways +', swung(2, 1.0, 1)), ('sideways -', swung(2, -1.0, 1)), ('twist +', swung(1, 1.0, 2)), ('twist -', swung(1, -1.0, 2))]
        for lbl, sdq in cases:
            deep = int((sdq < -0.25).sum())
            out.append(f'   {v} tail swung {lbl} to its limits: pts inside the bowl copy {deep} (nearest {sdq.min():+.2f})')
            if sdq.min() < worst_c[0]: worst_c = (float(sdq.min()), lbl)
        if worst_c[0] < -0.25:
            crc_ = bool(H.get('crest_collide')); pen_c = xs[nmw]['pen'] if (crc_ and nmw in xs) else None     # v8b: with the bowl as its collider an entry within the catch is pushed back out
            if pen_c is not None and worst_c[0] > -pen_c: out.append(f'   ok   {v}: the tail enters the bowl copy at its own limits ({worst_c[1]}: {worst_c[0]:+.2f}) - within its catch {pen_c}: the collider pushes it back out')
            else: out.append(f'   FAIL {v}: the tail enters the bowl at its own limits ({worst_c[1]}: {worst_c[0]:+.2f}) - ' + ('past the catch, the collider cannot recover it' if pen_c is not None else 'with no collider the limits must keep it out')); ok = False
        else: out.append(f'   ok   {v}: the tail stays out of the bowl at every limit (nearest {worst_c[0]:+.2f})')
    # v7 (PLAN_RIFTEN_PLUME 2026-10-12, user: 'the plume still sits inside the helmet. it enters at the top of the conical'): the v6c test above
    # keeps the benign X sign, measures only the bowl COPY (outward faces near the HANGING points - the apex and the root band are outside
    # it), turns each bone about its OWN origin (FSMP turns the child about its PARENT: frameInB = identity in bodyB), applies the y limit about
    # Z and the z limit about Y (the XML's angular y / z turn about the frame's Y / Z), and tests rest only in the drawn pose (the springs
    # rest at eq). Here: the X sign the constraint ALLOWS (the chain convention: a downward segment goes OUT, as every skirt chain does in
    # game), parent pivots, each limit about its own axis, the drawn pose, the spring rest and every limit; a crest point that MOVES (own
    # share > 0.02) INSIDE the helmet as SEEN - the shell or the hollow under it, ray parity against the WHOLE main shape - FAILS; FSMP's
    # contact view against the bowl's outward faces near EVERY crest point (root band included) is reported. The v6c lines stay.
    crs = next((t_ for t_ in T if r.get('crest') and t_.name == r['crest']['shape']), None)
    if r.get('crest') and crs is not None:
        G = {nm: np.array(x) for nm, x in r['bones'].items()}; nC, nR = int(r['crest']['chains']), int(r['crest']['n'])
        C1, C2 = H.get('crest_lim1', W.CREST_LIM1), H.get('crest_lim', W.CREST_LIM)
        main = max((t_ for t_ in T if t_ is not crs and t_.tex and any(t_.tex)), key=lambda t_: len(t_.tris))
        cx_, cy_ = (r['axis'] if r.get('axis') else (np.mean([g_[0, 3] for g_ in G.values()]), np.mean([g_[1, 3] for g_ in G.values()])))
        ctr = np.array([float(cx_), float(cy_), float(main.pos[:, 2].mean())])
        chains = [[f'{p} Crest{c} {k}' for k in range(nR + 1) if f'{p} Crest{c} {k}' in G] for c in range(nC)]
        R0 = G[chains[0][0]][:3, :3]; sx = 1.0 if (_rodrigues(R0[:, 0], 0.3) @ np.array([0, 0, -1.0])) @ R0[:, 1] > 0 else -1.0
        wts = [dict(w) for w in crs.w]; own = np.array([1.0 - w.get(HEAD, 0.0) for w in wts])
        cen = main.pos[main.tris].mean(1); fn = np.cross(main.pos[main.tris[:, 1]] - main.pos[main.tris[:, 0]], main.pos[main.tris[:, 2]] - main.pos[main.tris[:, 0]])
        near = np.zeros(len(cen), bool)
        for s0 in range(0, len(cen), 1500): near[s0:s0 + 1500] = np.linalg.norm(cen[s0:s0 + 1500, None] - crs.pos[None], axis=2).min(1) < W.BOWL_R
        outw = ((fn * (cen - ctr)).sum(1) / (np.linalg.norm(fn, axis=1) * np.linalg.norm(cen - ctr, axis=1) + 1e-9)) > 0.05
        bt_out = main.tris[near & outw]
        e1, e2 = C1.get('eq', (0, 0, 0)), C2.get('eq', (0, 0, 0))
        poses = [('drawn pose', [(0, 0, 0)] * nR), ('spring rest (eq)', [(-sx * e1[0], 0, 0)] + [(-sx * e2[0], 0, 0)] * (nR - 1)),
                 ('out to its limits', [(-sx * C1['lo'][0], 0, 0)] + [(-sx * C2['lo'][0], 0, 0)] * (nR - 1))]
        for i_, nm_ in ((1, 'sideways'), (2, 'twist')):
            for sg_, lim_ in (('+', 'hi'), ('-', 'lo')):
                a1 = [0, 0, 0]; a1[i_] = C1[lim_][i_]; a2 = [0, 0, 0]; a2[i_] = C2[lim_][i_]
                poses.append((f'{nm_} {sg_} (about {"YZ"[i_ - 1]}) at the spring rest', [(-sx * e1[0], a1[1], a1[2])] + [(-sx * e2[0], a2[1], a2[2])] * (nR - 1)))
        worst_v = (0, '')
        for lbl, angs in poses:
            Dm = {}
            for ch in chains: Dm.update(_pose_chain(G, ch, angs))
            Q = K.skin(crs.pos, wts, Dm); vol = _inside_volume(Q, main.pos, main.tris, ctr); mv = vol & (own > 0.02)
            sdo = contact(Q, main.pos, bt_out, 0.3)
            out.append(f'   {v} tail ({crs.name}, every pt) {lbl}: MOVING pts inside the helmet {int(mv.sum())}' +
                       (f' (z {Q[mv, 2].min():.1f}..{Q[mv, 2].max():.1f}, share {own[mv].min():.2f}..{own[mv].max():.2f})' if mv.any() else '') +
                       f'; head-bound inside {int((vol & ~(own > 0.02)).sum())} (the author\'s insertion); vs the outward bowl faces near it: nearest moving {sdo[own > 0.02].min():+.2f}')
            if mv.sum() > worst_v[0]: worst_v = (int(mv.sum()), lbl)
            if lbl == 'drawn pose': hb_in = vol & ~(own > 0.02); hb_z = Q[hb_in, 2] if hb_in.any() else None
        Dm = {}
        for ch in chains: Dm.update(_pose_chain(G, ch, [(sx * C1['lo'][0], 0, 0)] + [(sx * C2['lo'][0], 0, 0)] * (nR - 1)))
        Q = K.skin(crs.pos, wts, Dm); mvo = _inside_volume(Q, main.pos, main.tris, ctr) & (own > 0.02)
        out.append(f'   info {v}: allowed out = child turn {sx:+.0f} x |lo| about X (the skirt chains\' convention); the OTHER sign would put {int(mvo.sum())} moving pts inside the helmet')
        if H.get('crest_settle_root') and hb_in.any():     # v7: a design that settles its root band must show NO plume point inside the helmet
            out.append(f'   FAIL {v}: {int(hb_in.sum())} head-bound tail pts inside the helmet as drawn (z {hb_z.min():.1f}..{hb_z.max():.1f}) - the root settle must lift them out'); ok = False
        elif H.get('crest_settle_root'): out.append(f'   ok   {v}: no tail point at all inside the helmet as drawn (root band settled)')
        if worst_v[0]: out.append(f'   FAIL {v}: the tail enters the helmet ({worst_v[1]}: {worst_v[0]} moving pts inside the shell or its hollow)'); ok = False
        else: out.append(f'   ok   {v}: no moving tail point inside the helmet - drawn, at the spring rest, at every limit (allowed sign, parent pivots, the whole main shape)')
        # v7c (user 2026-10-13, v7b in game: 'the pony tail is still inside the helmet' - the lower plume runs into the cone): the poses above
        # test sideways / twist only from the spring rest (eq, lifted out), but a draped tail whose gravity beats its springs rests ON its
        # never-in stop (X at hi - the drawn pose when hi is 0), and the stop gives a little under that load. From the stop: every sideways /
        # twist corner, then every joint TAIL_SAG further IN past it. FAIL on any moving tail point inside the helmet (ray parity).
        hi1, hi2 = C1['hi'][0], C2['hi'][0]; bad_ = []
        pk_ = lambda C_, i, k: (C_['lo'][i], 0.0, C_['hi'][i])[k]
        for yi_, zi_ in itertools.product((0, 1, 2), (0, 1, 2)):
            angs = [(-sx * hi1, pk_(C1, 1, yi_), pk_(C1, 2, zi_))] + [(-sx * hi2, pk_(C2, 1, yi_), pk_(C2, 2, zi_))] * (nR - 1)
            Dm = {}
            for ch in chains: Dm.update(_pose_chain(G, ch, angs))
            Q = K.skin(crs.pos, wts, Dm); mv = _inside_volume(Q, main.pos, main.tris, ctr) & (own > 0.02)
            if mv.any(): bad_.append(f'sideways {"-0+"[yi_]} twist {"-0+"[zi_]}: {int(mv.sum())} (z {Q[mv, 2].min():.1f}..{Q[mv, 2].max():.1f})')
        Dm = {}
        for ch in chains: Dm.update(_pose_chain(G, ch, [(-sx * hi1 - sx * TAIL_SAG, 0, 0)] + [(-sx * hi2 - sx * TAIL_SAG, 0, 0)] * (nR - 1)))
        Q = K.skin(crs.pos, wts, Dm); mv = _inside_volume(Q, main.pos, main.tris, ctr) & (own > 0.02)
        if mv.any(): bad_.append(f'every joint {TAIL_SAG} IN past the stop: {int(mv.sum())} (z {Q[mv, 2].min():.1f}..{Q[mv, 2].max():.1f})')
        stop_ = f'stop {0.0 - hi1:g} / {0.0 - hi2:g} out of the drawn pose'
        if bad_: out.append(f'   FAIL {v}: the tail resting on its never-in stop ({stop_}) enters the helmet - moving pts inside at ' + '; '.join(bad_)); ok = False
        else: out.append(f'   ok   {v}: the tail on its never-in stop ({stop_}): nothing inside at any sideways / twist corner, nor {TAIL_SAG} rad past the stop at every joint')
    return ok, worst


def _rodrigues(axis, th):
    a = np.asarray(axis, float); a = a / np.linalg.norm(a); Kx = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(th) * Kx + (1 - np.cos(th)) * (Kx @ Kx)


def _pose_chain(G, chain, angs):
    """v7: joint r turns the child about its PARENT's posed origin and the parent frame's own axes; angs[r-1] = (about X, about Y, about Z)"""
    Dm = {}; D = np.eye(4)
    for r in range(1, len(chain)):
        par = G[chain[r - 1]]; piv = (D @ np.r_[par[:3, 3], 1])[:3]; B = D[:3, :3] @ par[:3, :3]; R = np.eye(3)
        for i, th in enumerate(angs[r - 1]):
            if th: R = _rodrigues(B[:, i], th) @ R
        M = np.eye(4); M[:3, :3] = R; M[:3, 3] = piv - R @ piv; D = M @ D; Dm[chain[r]] = D.copy()
    return Dm


def _ray_hits(o, d, P, T_):
    v0, v1, v2 = P[T_[:, 0]], P[T_[:, 1]], P[T_[:, 2]]; e1, e2 = v1 - v0, v2 - v0
    h = np.cross(d, e2); a = (e1 * h).sum(1); ok = np.abs(a) > 1e-12; f = np.zeros_like(a); f[ok] = 1.0 / a[ok]
    s = o - v0; u = f * (s * h).sum(1); q = np.cross(s, e1); v = f * (d * q).sum(1); t = f * (e2 * q).sum(1)
    return int((ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-6)).sum())


def _inside_volume(Q, P, T_, ctr):
    """v7: inside the helmet as SEEN (its shell or the hollow under it): rays straight up AND up-and-outward both cross the whole mesh an odd
    number of times (a helmet is open only at the neck, below)"""
    out = np.zeros(len(Q), bool)
    for i, q in enumerate(Q):
        r_ = np.array([q[0] - ctr[0], q[1] - ctr[1], 0.0]); r_ = r_ / (np.linalg.norm(r_) + 1e-9)
        out[i] = _ray_hits(q, np.array([0.0, 0.0, 1.0]), P, T_) % 2 == 1 and _ray_hits(q, (r_ + np.array([0, 0, 1.0])) / np.sqrt(2), P, T_) % 2 == 1
    return out


def check_static(h, v, r, H, out):
    """2026-10-13 PERF (PLAN_PERF_WHITERUN.md 3): a STATIC helmet passes as 'no physics by design' when its nif carries no HDT link, no
    custom bone, the author's shapes with their vertex / triangle counts, and the PBR donor's textures (when a donor exists)"""
    ok = True; p = H['prefix']; n = W.NifFile(r['out'])
    hdt = [x for x in getattr(n.rootNode, 'string_data', []) if 'HDT' in str(x)] if hasattr(n, 'rootNode') else []
    raw = open(r['out'], 'rb').read()
    if b'HDT Skinned Mesh Physics Object' in raw or hdt: out.append(f'   FAIL {v}: static, but the nif still carries an HDT link'); ok = False
    if (p + ' ').encode() in raw: out.append(f'   FAIL {v}: static, but the nif names {p} bones'); ok = False
    src = W.NifFile(W.SRC_ROOT + H['src'].format(v))
    a = [(s_.name, len(s_.verts), len(s_.tris)) for s_ in src.shapes]; b = [(s_.name, len(s_.verts), len(s_.tris)) for s_ in n.shapes]
    if a != b: out.append(f'   FAIL {v}: static shapes differ from the author\'s: {a} vs {b}'); ok = False
    dpath = (W.DONOR_ROOT or '') + H['src'].format(v)
    if W.DONOR_ROOT and os.path.exists(dpath):
        dn = {s_.name: s_ for s_ in W.NifFile(dpath).shapes}
        for s_ in n.shapes:
            if s_.name in dn and dict(s_.textures) != dict(dn[s_.name].textures): out.append(f'   FAIL {v}: {s_.name} textures differ from the PBR donor'); ok = False
    out.append(f'   {"ok  " if ok else "FAIL"} {v}: static - no physics by design (no HDT link, no custom bones, the author\'s {len(b)} shapes'
               + (', the PBR donor\'s textures)' if W.DONOR_ROOT and os.path.exists(dpath) else ', NO donor)'))
    return ok


def main(dp, helmets):
    W.use_designs(dp); rep = json.load(open(W.WORK + 'helmets_report.json')); allok = True
    for h in helmets or list(rep):
        if h not in W.HELMETS: print(f'== {h}: in the report but not in the design file (dropped) - skipped'); continue
        H = W.HELMETS[h]; out = [f'== {h}']; worst = 0
        vs = [v for v in H['variants'] if v.lstrip('_')[:1] in 'mf' and not v.endswith('_0')]
        for v in vs:
            if v not in rep[h]['variants']: out.append(f'   info {v}: not built in this round (--variants)'); continue
            r = rep[h]['variants'][v]
            if r.get('static'): allok &= check_static(h, v, r, H, out); continue
            xs, xbones = xml_info(W.STAGE + r['xml'].replace('\\', '/'))
            ok, w_ = check_variant(h, v, r, H, xs, xbones, out); allok &= ok; worst = max(worst, w_)
        # _0 / _1 pairs: same bones and point counts
        for v in H['variants']:
            if v.endswith('_0'):
                a, b = rep[h]['variants'][v], rep[h]['variants'][v[:-2] + '_1']
                if a.get('static') or b.get('static'): same = bool(a.get('static') and b.get('static'))     # 2026-10-14: static pairs - no rig to compare (the shape match below still runs)
                else: same = set(a['bones']) == set(b['bones']) and a['curtain'] == b['curtain'] and a['lining'] == b['lining']
                out.append(f'   {"ok  " if same else "FAIL"} {v}: same bones and point counts as {v[:-2]}_1'); allok &= same
                # v6d (crash 2026-10-12 21:45): the game blends the _0 and _1 meshes shape by shape at load and reads one vertex buffer
                # with the other's count - EVERY shape (the hidden copies included) must exist in both, in the same order, with the same
                # vertex and triangle counts
                s0 = [(s.name, len(s.verts), len(s.tris)) for s in W.NifFile(a['out']).shapes]; s1 = [(s.name, len(s.verts), len(s.tris)) for s in W.NifFile(b['out']).shapes]
                bad = [f'{x[0]!r} {x[1]}v/{x[2]}t vs {y[0]!r} {y[1]}v/{y[2]}t' for x, y in zip(s0, s1) if x[1:] != y[1:]]
                if len(s0) != len(s1): bad.append(f'{len(s0)} shapes vs {len(s1)}')
                out.append(f'   {"ok  " if not bad else "FAIL"} {v}: every shape matches {v[:-2]}_1 in vertex and triangle count' + (f' - {"; ".join(bad)}' if bad else f' ({len(s0)} shapes)'))
                allok &= not bad
        allok &= not any(x.startswith('   FAIL') for x in out)
        out.append(f'SUMMARY {h} worst sunk over the head poses: {worst}')
        print('\n'.join(out))
    print('ALL OK' if allok else 'CHECK')
    return 0 if allok else 1


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2:]))
