"""piece_regress.py - the per-PIECE regression diff (user 2026-10-14, after a hold job changed belt tips the user had approved: "the
regression diff in rebuild_coat.py (per piece: physics, root, bone shares, rest height over the copy, copy offset from the drawn surface,
vs the last approved install; FAIL on any change outside the job's named pieces), and read APPROVED.md in the project - those pieces are
frozen").

A PIECE is a bone family: a physics bone's name minus the armour prefix and every digit ('MOA BeltTip 2' -> 'BeltTip', 'SWG Hang0 3' ->
'Hang', 'NLO Mail Skirt04 2' -> 'Mail Skirt'). Per piece, between a BASELINE (the approved build, else the installed files) and the NEW
build (the stage):
  physics  every bone's bone-default values and every constraint's constraint-default values in effect (XML, defaults accumulate)
  root     the bodyB of every constraint whose bodyA is in the piece and bodyB is not (where the chain hangs)
  shares   the drawn points whose largest physics weight is the piece: count, mean share on the piece's own bones, on other pieces,
           on the leg bones, on the rest of the skeleton
  rest     per collision pair a piece's point shape takes part in (its per-vertex shape vs every per-triangle shape it may collide with):
           median / min signed height over the partner (rest_pairs.py's metric), per weight file
  copy     per per-triangle (hidden) shape: triangle count and the signed offset of its points from the nearest DRAWN surface (median,
           p10; + = outside), charged to EVERY piece whose points collide with it (a collider change changes all of them)
Tolerances: values exact (physics / root), shares .02, heights / offsets .05, any triangle-count change.
Verdict: CHANGED pieces that the job named are reported; any other changed piece = FAIL (rebuild_coat.py holds the install);
any changed joint / link LIMIT or collider CATCH (margin / penetration) = FAIL even in a named piece unless --limits-ok (the user's
standing rule: 'do not touch any catch, margin or limit').

usage: piece_regress.py <base_nif_1> <base_xml> <new_nif_1> <new_xml> [--base0=<nif_0>] [--new0=<nif_0>] [--pieces=A,B] [--prefix=XYZ]
       (in rebuild_coat.py: per design and body, baseline from APPROVED pieces (approved_pieces.json in the work folder) or the mods)"""
import os, re, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()

TOL_SHARE, TOL_H = 0.02, 0.05
LIMIT_KEYS = ('linearLowerLimit', 'linearUpperLimit', 'angularLowerLimit', 'angularUpperLimit')
SKEL = re.compile(r'^(NPC |CME |Weapon|Shield|Quiver|MagicEffects|Camera|Skirt[LRFB]Bone)|\[')      # Skirt?Bone: XPMSE's skeleton skirt bones


def family(bone):
    if SKEL.search(bone): return None
    toks = bone.split()
    if len(toks) > 1 and re.fullmatch(r'[A-Z]{2,5}', toks[0]): toks = toks[1:]
    f = ' '.join(re.sub(r'\d+', '', t) for t in toks).strip()
    return f or None


def _leaf(block):
    d = {}
    for m in re.finditer(r'<([A-Za-z\-]+)((?:\s+\w+="[^"]*")*)\s*/>|<([A-Za-z\-]+)>([^<]*)</\3>', block):
        if m.group(1): d[m.group(1)] = m.group(2).strip()
        else: d[m.group(3)] = m.group(4).strip()
    return d


def parse_xml(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)
    bones, cons, shapes = {}, [], {}
    bd, cd = {}, {}
    tok = re.compile(r'<bone-default>(.*?)</bone-default>|<bone name="([^"]+)"\s*/>|<bone name="([^"]+)">(.*?)</bone>'
                     r'|<generic-constraint-default>(.*?)</generic-constraint-default>'
                     r'|<generic-constraint bodyA="([^"]+)" bodyB="([^"]+)"\s*/>|<generic-constraint bodyA="([^"]+)" bodyB="([^"]+)">(.*?)</generic-constraint>'
                     r'|<per-(vertex|triangle)-shape name="([^"]+)">(.*?)</per-\11-shape>', re.S)
    for m in tok.finditer(txt):
        if m.group(1) is not None: bd = dict(bd, **_leaf(m.group(1)))
        elif m.group(2): bones[m.group(2)] = dict(bd)
        elif m.group(3): bones[m.group(3)] = dict(bd, **_leaf(m.group(4)))
        elif m.group(5) is not None: cd = dict(cd, **_leaf(m.group(5)))
        elif m.group(6): cons.append((m.group(6), m.group(7), dict(cd)))
        elif m.group(8): cons.append((m.group(8), m.group(9), dict(cd, **_leaf(m.group(10)))))
        elif m.group(11):
            b = m.group(13); g = lambda k, dflt: (re.search(rf'<{k}>([^<]*)</{k}>', b) or [None, dflt])[1]
            shapes[m.group(12)] = dict(kind=m.group(11), margin=float(g('margin', 1.0)), pen=float(g('penetration', 1.0)), tag=g('tag', ''),
                                       can=re.findall(r'<can-collide-with-tag>([^<]*)', b), no=re.findall(r'<no-collide-with-tag>([^<]*)', b))
    return bones, cons, shapes


def heights(Q, V, F, lo=-6.0, hi=6.0):
    A, B, Cc = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    N = np.cross(B - A, Cc - A); ln = np.linalg.norm(N, axis=1); ok = ln > 1e-9; N[ok] /= ln[ok][:, None]
    v0, v1 = B - A, Cc - A; d00 = (v0 * v0).sum(1); d01 = (v0 * v1).sum(1); d11 = (v1 * v1).sum(1); den = d00 * d11 - d01 * d01
    out = np.full(len(Q), np.nan)
    for s in range(0, len(Q), 48):
        q = Q[s:s + 48]; h = np.einsum('nmk,mk->nm', q[:, None, :] - A[None], N); v2 = (q[:, None, :] - h[..., None] * N[None]) - A[None]
        d20 = np.einsum('nmk,mk->nm', v2, v0); d21 = np.einsum('nmk,mk->nm', v2, v1)
        with np.errstate(divide='ignore', invalid='ignore'):
            v = (d11 * d20 - d01 * d21) / den; w = (d00 * d21 - d01 * d20) / den
        h = np.where((v >= -0.02) & (w >= -0.02) & (v + w <= 1.02) & ok[None] & (h > lo) & (h < hi), h, np.nan)
        ah = np.where(np.isnan(h), np.inf, np.abs(h)); j = ah.argmin(1); hh = h[np.arange(len(q)), j]
        hh[~np.isfinite(ah.min(1))] = np.nan; out[s:s + 48] = hh
    return out


def surface_offset(P, PN, V, F, k=24):
    """signed distance of P (normals PN) from the surface V[F]: + = along PN (outside)"""
    cen = V[F].mean(1); idx, _ = C.knn(cen, P, k)
    best = np.full(len(P), np.inf); sgn = np.zeros(len(P))
    for j in range(idx.shape[1]):
        t = F[idx[:, j]]; cp, _ = C.closest_on_tris(P, V[t[:, 0]], V[t[:, 1]], V[t[:, 2]])
        d = np.linalg.norm(P - cp, axis=1); b = d < best; best[b] = d[b]; sgn[b] = np.sign(((P - cp) * PN).sum(1))[b]
    return best * np.where(sgn == 0, 1, sgn)


def vnormals(P, F):
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); n = np.zeros_like(P)
    for c in range(3): np.add.at(n, F[:, c], fn)
    ln = np.linalg.norm(n, axis=1); return n / np.maximum(ln, 1e-9)[:, None]


def load(path):
    n, T = C.load(path); C.to_world(T); return {t.name: t for t in T}


def dom_family(w):
    acc = {}
    for b, x in w.items():
        f = family(b)
        if f: acc[f] = acc.get(f, 0.0) + x
    return max(acc, key=acc.get) if acc else None


def summary(nif1, xml, nif0=None):
    bones, cons, shapes = parse_xml(xml)
    S = {'1': load(nif1)}
    if nif0 and os.path.exists(nif0): S['0'] = load(nif0)
    S1 = S['1']; out = {}
    P = lambda f: out.setdefault(f, dict(physics={}, root=set(), shares=None, rest={}, copy={}, catch={}))
    for b, d in bones.items():
        f = family(b)
        if f: P(f)['physics'][b] = json.dumps(d, sort_keys=True)
    for a, b, d in cons:
        fa, fb = family(a), family(b)
        root_ = fb != fa or float(_nums(bones.get(b, {}).get('mass'))[0] if _nums(bones.get(b, {}).get('mass')) else 0.0) == 0.0     # another piece, or a kinematic bone
        if fa: P(fa)['physics'][f'{a} <- {"(root)" if root_ else b}'] = json.dumps(d, sort_keys=True)     # a root's move shows on the root line, its values here
        if fa and root_: P(fa)['root'].add(b)
    hidden = set(shapes) | {'VirtualGround'}
    acc = {}; pts_ = {}
    for nm, t in S1.items():
        if nm in hidden: continue
        doms_, vals_ = [], np.zeros((len(t.w), 4)); pts_[nm] = (doms_, vals_)
        for vi, w in enumerate(t.w):
            f = dom_family(w); doms_.append(f)
            if not f: continue
            tot = sum(w.values()) or 1.0; own = oth = leg = body = 0.0
            for b, x in w.items():
                fb = family(b)
                if fb == f: own += x
                elif fb: oth += x
                elif any(k in b for k in ('Thigh', 'Calf', 'Foot')): leg += x
                else: body += x
            a = acc.setdefault(f, np.zeros(5)); a += (1, own / tot, oth / tot, leg / tot, body / tot); vals_[vi] = (own / tot, oth / tot, leg / tot, body / tot)
    for f, a in acc.items(): P(f)['shares'] = dict(n=int(a[0]), own=a[1] / a[0], other=a[2] / a[0], legs=a[3] / a[0], body=a[4] / a[0])
    pv_fam = {nm: dom_family({b: sum(w.get(b, 0) for w in S1[nm].w) for b in {b for w in S1[nm].w for b in w}}) for nm, s in shapes.items() if s['kind'] == 'vertex' and nm in S1}
    users = {}
    for pn, pc in shapes.items():
        if pc['kind'] != 'vertex' or pn not in S1 or not pv_fam.get(pn): continue
        for tn, tc in shapes.items():
            if tc['kind'] != 'triangle' or tn not in S1 or tc['tag'] not in pc['can'] or tc['tag'] in pc['no']: continue
            users.setdefault(tn, set()).add(pv_fam[pn]); P(pv_fam[pn])['catch'][pn] = (pc['margin'], pc['pen'])
            for v, Sv in S.items():
                if pn not in Sv or tn not in Sv: continue
                h = heights(Sv[pn].pos, Sv[tn].pos, Sv[tn].tris.astype(int)); h = h[~np.isnan(h)]
                P(pv_fam[pn])['rest'][f'{pn} vs {tn} _{v}'] = (round(float(np.median(h)), 3), round(float(h.min()), 3), int(len(h))) if len(h) else None
    drawn = [t for nm, t in S1.items() if nm not in hidden and len(t.tris)]
    if drawn:
        DV = np.vstack([t.pos for t in drawn]); offs = np.cumsum([0] + [len(t.pos) for t in drawn])
        DF = np.vstack([t.tris + o for t, o in zip(drawn, offs[:-1])]).astype(int)
    for tn, fams in users.items():
        t = S1[tn]
        if not len(t.tris) or not drawn: continue
        d = surface_offset(t.pos, vnormals(t.pos, t.tris.astype(int)), DV, DF)
        for f in fams: P(f)['copy'][tn] = (int(len(t.tris)), round(float(np.median(d)), 3), round(float(np.percentile(d, 10)), 3))
    for tn, fams in users.items():
        for f in fams: P(f)['catch'][tn] = (shapes[tn]['margin'], shapes[tn]['pen'])
    for f in out: out[f]['root'] = sorted(out[f]['root'])
    out['__pts__'] = pts_
    return out


def point_shares(base, new):
    """point by point over the drawn shapes both builds have with the same vertex count: per piece, the shares over the points that belong
    to it in BOTH builds (a point that changed piece is not a share change of either), and the points that changed piece, charged to
    the piece that gained them. -> ({piece: (base vals, new vals, n)}, {gaining piece: {losing piece: n}})"""
    A, B = base.get('__pts__', {}), new.get('__pts__', {}); st, sw = {}, {}
    if not (set(A) & set(B)): return None, None
    for nm in set(A) & set(B):
        (da, va), (db, vb) = A[nm], B[nm]
        if len(da) != len(db): continue          # a shape rebuilt with other points (e.g. an unused copy): not compared point by point
        for i, (fa, fb) in enumerate(zip(da, db)):
            if fa and fa == fb:
                e = st.setdefault(fa, [np.zeros(4), np.zeros(4), 0]); e[0] += va[i]; e[1] += vb[i]; e[2] += 1
            elif fa != fb and fb: sw.setdefault(fb, {}).setdefault(fa, 0); sw[fb][fa] += 1
    return {f: (e[0] / e[2], e[1] / e[2], e[2]) for f, e in st.items()}, sw


def _nums(v):
    """a limit attribute string -> its numbers (so '-0.0' == '0')"""
    return tuple(round(float(x), 6) + 0.0 for x in re.findall(r'-?\d+(?:\.\d+)?(?:e-?\d+)?', v or ''))


def compare(base, new):
    """{piece: [change lines]} for every piece that differs"""
    ch = {}
    pst, psw = point_shares(base, new)
    # rest pairs, copies and catches compared SHAPE by shape over the whole armour (a pair whose points changed piece - a ride share
    # removed - is not a change of its values); a difference is charged to the piece that owns the key now (or owned it, if removed)
    fams_ = (set(base) | set(new)) - {'__pts__'}
    gl = {kind: ({k: v for f in fams_ if f in base for k, v in base[f].get(kind, {}).items()}, {k: v for f in fams_ if f in new for k, v in new[f].get(kind, {}).items()})
          for kind in ('rest', 'copy', 'catch')}
    own_ = lambda kind, f, k: (k in (new.get(f) or {}).get(kind, {})) or (k not in gl[kind][1] and k in (base.get(f) or {}).get(kind, {}))
    for f in sorted((set(base) | set(new)) - {'__pts__'}):
        a, b = base.get(f), new.get(f); L = []
        if a is None or b is None: ch[f] = ['piece ' + ('added' if a is None else 'removed')]; continue
        pk = set(a['physics']) | set(b['physics'])
        dp = [k for k in sorted(pk) if a['physics'].get(k) != b['physics'].get(k)]
        if dp:
            k = dp[0]; da = json.loads(a['physics'].get(k) or '{}'); db = json.loads(b['physics'].get(k) or '{}')
            diff = {x: (da.get(x), db.get(x)) for x in set(da) | set(db) if da.get(x) != db.get(x)}
            L.append(f'physics: {len(dp)} bones / constraints differ, e.g. {k}: ' + ', '.join(f'{x} {u} -> {v}' for x, (u, v) in list(diff.items())[:4]))
        lim = [k for k in dp if ' <- ' in k and any(x in json.loads(a['physics'].get(k) or '{}').keys() | json.loads(b['physics'].get(k) or '{}').keys()
                                                   and _nums(json.loads(a['physics'].get(k) or '{}').get(x)) != _nums(json.loads(b['physics'].get(k) or '{}').get(x)) for x in LIMIT_KEYS)]
        if lim: L.append(f'LIMIT: {len(lim)} constraints change a joint / link limit, e.g. {lim[0]}')
        for k in sorted(set(a.get('catch', {})) | set(b.get('catch', {}))):
            u, v = gl['catch'][0].get(k), gl['catch'][1].get(k)
            if own_('catch', f, k) and u != v:
                L.append(f'CATCH: {k} margin / penetration {u} -> {v}' if (u is not None and v is not None) else f'collider {"added" if u is None else "removed"}: {k} {u or v}')
        if a['root'] != b['root']: L.append(f'root: {a["root"]} -> {b["root"]}')
        sa, sb = a['shares'], b['shares']
        if pst is not None:            # point by point (same topology): the points of this piece in both builds; points that changed piece apart
            if f in pst:
                ua, ub, n_ = pst[f]; K_ = ('own', 'other', 'legs', 'body')
                if np.abs(ua - ub).max() > TOL_SHARE: L.append('shares: ' + ', '.join(f'{K_[j]} {ua[j]:.2f} -> {ub[j]:.2f}' for j in range(4) if abs(ua[j] - ub[j]) > TOL_SHARE) + f' ({n_} pts that are this piece in both)')
            if psw.get(f): L.append('points now on this piece: ' + ', '.join(f'{n_} from {g_ or "no piece"}' for g_, n_ in psw[f].items()))
        elif (sa is None) != (sb is None): L.append(f'shares: {sa} -> {sb}')
        elif sa and any(abs(sa[k] - sb[k]) > TOL_SHARE for k in ('own', 'other', 'legs', 'body')):
            L.append('shares: ' + ', '.join(f'{k} {sa[k]:.2f} -> {sb[k]:.2f}' for k in ('own', 'other', 'legs', 'body') if abs(sa[k] - sb[k]) > TOL_SHARE) + f' (pts {sa["n"]} -> {sb["n"]})')
        for k in sorted(set(a['rest']) | set(b['rest'])):
            u, v = gl['rest'][0].get(k), gl['rest'][1].get(k)
            if not own_('rest', f, k): continue
            if (u is None) != (v is None) or (u and (abs(u[0] - v[0]) > TOL_H or abs(u[1] - v[1]) > TOL_H)):
                L.append(f'rest {k}: median / min {u[:2] if u else None} -> {v[:2] if v else None}')
        for k in sorted(set(a['copy']) | set(b['copy'])):
            u, v = gl['copy'][0].get(k), gl['copy'][1].get(k)
            if not own_('copy', f, k): continue
            if (u is None) != (v is None) or (u and (u[0] != v[0] or abs(u[1] - v[1]) > TOL_H or abs(u[2] - v[2]) > TOL_H)):
                L.append(f'copy {k}: tris / offset median / p10 {u} -> {v}')
        if L: ch[f] = L
    return ch


def verdict(changes, named, limits_ok=False):
    named = {x.strip() for x in named if x.strip()}
    bad = [f for f in changes if (f not in named and '*' not in named)
           or (not limits_ok and any('LIMIT:' in l or 'CATCH:' in l for l in changes[f]))]      # the user's standing rule: no catch, margin or limit
    return bad


def report(label, changes, named, out=print, limits_ok=False):
    bad = verdict(changes, named, limits_ok)
    out(f'{label}: piece regression - {len(changes)} pieces changed' + (f', FAIL: {bad} changed but not named by the job, or a limit / catch / margin changed (--limits-ok to allow)' if bad else (' (all named)' if changes else '')))
    for f, L in changes.items():
        out(f'   {"FAIL " if f in bad else "named"} {f}:')
        for l in L[:8]: out(f'        {l}')
    return bad


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]; kv = dict(x[2:].split('=', 1) for x in sys.argv[1:] if x.startswith('--') and '=' in x)
    if len(a) < 4: print(__doc__); sys.exit(1)
    base = summary(a[0], a[1], kv.get('base0')); new = summary(a[2], a[3], kv.get('new0'))
    bad = report(os.path.basename(a[2]), compare(base, new), kv.get('pieces', '').split(','), limits_ok='--limits-ok' in sys.argv)
    sys.exit(1 if bad else 0)
