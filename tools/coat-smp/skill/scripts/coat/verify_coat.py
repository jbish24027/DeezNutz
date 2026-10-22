# skill coat copy (from sos-smp-rework/) of verify_rework.py (2026-10-11): checks build_sos designs; ported 2026-10-11.
"""Checks for build_rework.py output (one design, men + women):
  A every source triangle is in the output once (unchanged, or - for split pieces - its 4 children cover it exactly);
    each visible piece keeps its source shape's shader / textures / alpha / flags; <= 4 influences summing to 1,
    <= 80 bones per shape; HDT string -> the XML; XML shapes in the mesh, XML bones mesh nodes or skeleton bones,
    collision-shape bones declared, constraint bodies declared, every rig node declared
  B rest contacts for every pair the XML lets collide (men _1 and _0; women on the set defaults and the user's preset,
    small + big)
  C women: every visible point's simulated BodySlide build = the original set's build of its source point; every
    collision copy moves like the points it was made from
  D skirt smoothness
usage: verify_rework.py <design> [m] [f]"""
from collections import defaultdict
import os, sys, json
import numpy as np
import xml.etree.ElementTree as ET
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
import build_coat_rig as W, coat_lib as F
load, wrap, rot, prism_rest = C.load, C.wrap, K.rot, F.prism_rest
check = K.check
read_osd = C.read_osd
D = C


check = K.check


def area(P, T_): return np.linalg.norm(np.cross(P[T_[:, 1]] - P[T_[:, 0]], P[T_[:, 2]] - P[T_[:, 0]]), axis=1).sum() / 2


def dropped_of(design, g, v):
    """v19b: source triangles build_rework dropped on purpose (the gusset bridging the openings) - {source shape: [[i,j,k], ...]}"""
    rep = json.load(open(W.WORK + 'rework_report.json'))[design][g]
    return {nm: {tuple(x) for x in tris} for nm, tris in rep.get('dropped', {}).get(v, {}).items()}


def lift_of(design, g, v):
    """v12: the belt-tail points build_rework lifted onto the skirt (shape -> (indices, offsets)) for this weight"""
    rep = json.load(open(W.WORK + 'rework_report.json'))[design][g]
    return {nm: (np.asarray(ix, int), np.asarray(of, float).reshape(-1, 3)) for nm, (ix, of) in rep.get('lift', {}).get(v, {}).items()}


def relift(pos_by_shape, lift):
    """positions with the recorded lift put back (rest contacts are judged on what the game shows)"""
    out = dict(pos_by_shape)
    for nm, (ix, of) in lift.items():
        if nm in out: q = np.array(out[nm], float); q[ix] += of; out[nm] = q
    return out


def unlift(pos_by_shape, lift):
    """built positions with the recorded lift taken OFF again (the inverse of relift: what the author drew)"""
    out = dict(pos_by_shape)
    for nm, (ix, of) in lift.items():
        if nm in out: q = np.array(out[nm], float); q[ix] -= of; out[nm] = q
    return out


DZ_PLUMB = {}     # v12: design -> tip_plumb (a plumbed strap's recorded shear may reach the drawn lean, ~2.7 on a 3BA woman)

def _bedges(tris):
    e = {}
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            k = (min(int(u), int(v)), max(int(u), int(v))); e[k] = e.get(k, 0) + 1
    return np.array([k for k, cnt in e.items() if cnt == 1], int).reshape(-1, 2)


def _seg_dist(P, A, B):
    out = np.empty(len(P))
    for s in range(0, len(P), 400):
        p = P[s:s + 400]; AB = B - A; t = np.clip(((p[:, None, :] - A[None]) * AB[None]).sum(2) / ((AB * AB).sum(1)[None] + 1e-12), 0, 1)
        Q = A[None] + t[:, :, None] * AB[None]; out[s:s + 400] = np.linalg.norm(p[:, None, :] - Q, axis=2).min(1)
    return out


def _seg_dist_t(Q, A, B):
    AB = B - A; L2 = (AB * AB).sum(1)[None] + 1e-12
    tt = np.clip(((Q[:, None, :] - A[None]) * AB[None]).sum(2) / L2, 0.0, 1.0)
    return np.linalg.norm(Q[:, None, :] - (A[None] + tt[:, :, None] * AB[None]), axis=2), tt


def source_edges(tc, M=None):
    """every edge of the source triangles, keyed by its canonical (position + UV) vertex ids, with its end positions in key order"""
    M = M or K.Matcher(tc.pos, tc.uv); edges = {}
    for tr in tc.tris:
        for a, b in ((tr[0], tr[1]), (tr[1], tr[2]), (tr[2], tr[0])):
            ca, cb = int(M.canon[a]), int(M.canon[b])
            if ca == cb: continue
            edges[(min(ca, cb), max(ca, cb))] = (tc.pos[a], tc.pos[b]) if ca < cb else (tc.pos[b], tc.pos[a])
    keys = list(edges)
    return M, keys, np.array([edges[k][0] for k in keys]).reshape(-1, 3), np.array([edges[k][1] for k in keys]).reshape(-1, 3)


def weld_cover(tc, o):
    """v13: source triangles of tc split in the output o along one edge at welded points - a parent counts as covered when its children's
    pieces of that edge tile it from end to end (one weld = two children, two welds on one edge = three)"""
    M, ekeys, EA, EB = source_edges(tc)
    src_tris = {frozenset(int(M.canon[x]) for x in tr) for tr in tc.tris}
    cid = []
    for p, u in zip(o.pos, o.uv):
        m = M.near(p, u)
        if m: cid.append(('src', int(M.canon[m[0]]))); continue
        d, tt = _seg_dist_t(np.asarray(p, float)[None], EA, EB); js = np.where(d[0] < 0.02)[0]     # every source edge under the point (the builder welds
        cid.append(('edge', [(ekeys[j][0], ekeys[j][1], float(tt[0, j])) for j in js]) if len(js) else None)   # up to 0.02 off it): a texture island's edge coincides with the torso's
    # a child belongs to the one source triangle whose corners / edges hold all of its vertices (corners matched by position: a texture
    # island's vertex on the torso's corner is the same corner); a parent is covered when its children's areas add up to its own -
    # whatever the number of welds and whichever of its edges they sit on
    area1 = lambda P3: 0.5 * float(np.linalg.norm(np.cross(P3[1] - P3[0], P3[2] - P3[0])))
    ptris = {}
    for tr in tc.tris:
        key = frozenset(int(M.canon[x]) for x in tr)
        if len(key) == 3 and key not in ptris: ptris[key] = area1(tc.pos[list(key)])
    by_edge = defaultdict(list)
    for key in ptris:
        a, b, c = sorted(key)
        for e in ((a, b), (a, c), (b, c)): by_edge[e].append(key)
    got = defaultdict(float)
    for tr in o.tris:
        ids = [cid[int(i)] for i in tr]
        if any(x is None for x in ids): continue
        ss = [x[1] for x in ids if x[0] == 'src']; eds = [x[1] for x in ids if x[0] == 'edge']
        if not eds: continue
        cands = None
        for cl in eds:
            s = set()
            for a, b, tt in cl: s.update(by_edge.get((min(a, b), max(a, b)), []))
            cands = s if cands is None else cands & s
        cands = [k for k in cands if all(any(np.linalg.norm(tc.pos[c] - tc.pos[s]) < 1e-3 for c in k) for s in ss)]
        if len(cands) != 1: continue
        got[cands[0]] += area1(o.pos[list(int(i) for i in tr)])
    return sum(1 for k, ar in got.items() if abs(ar - ptris[k]) < 2e-2 * max(ptris[k], 1e-9) + 1e-4)   # a weld up to 0.02 off the edge shifts the children's area a little


def seam_check(SO, cfg, pos=None):
    """v13: every piece boundary vertex that lies on its source remainder's boundary edge must BE a remainder vertex (no T-junction) with
    the same skeleton weights - the waist seam is watertight under any pose. Reported and checked per piece, on the positions AS WRITTEN
    (pos = {shape: positions} before any lift was undone: a lifted hem point sits off the edge in the game too)."""
    for pname, src in [(p[0], p[1]) for p in cfg['pieces']]:
        if pname not in SO or src not in SO or pname == src: continue
        o, r = SO[pname], SO[src]
        opos = pos[pname] if pos else o.pos; rpos = pos[src] if pos else r.pos
        Er = _bedges(r.tris)
        if not len(Er): continue
        bv = np.unique(_bedges(o.tris)); P = opos[bv]
        de = _seg_dist(P, rpos[Er[:, 0]], rpos[Er[:, 1]]); on = de < 0.02
        if not on.any(): continue
        rb = np.unique(Er); RP = rpos[rb]
        tj = 0; wm = 0; worst = 0.0
        for i in np.where(on)[0]:
            d = np.linalg.norm(RP - P[i], axis=1); j = int(d.argmin())
            if d[j] > 1e-3: tj += 1; continue
            wa, wb = o.w[int(bv[i])], r.w[int(rb[j])]
            diff = max(abs(wa.get(k, 0.0) - wb.get(k, 0.0)) for k in set(wa) | set(wb))
            if diff > 1e-3: wm += 1; worst = max(worst, diff)
        check(tj == 0 and wm == 0, f'seam {pname} / {src}: {int(on.sum())} piece boundary pts on the remainder edge, T-junctions {tj}, weight mismatches {wm}' + (f' (worst {worst:.3f})' if wm else ''))


def structure(label, out_path, src_path, cfg, N, names_1=None, lift=None, dropped=None, welded=None):
    print(f'== {label}: {os.path.basename(out_path)}')
    no, TO = load(out_path); C.to_world(TO); SO = {t.name: t for t in TO}
    pos_written = {t.name: np.array(t.pos, float) for t in TO}   # v13: the seam check looks at the mesh AS WRITTEN (what the game draws), before the lift is undone
    for nm, (ix, of) in (lift or {}).items():       # v12: undo the tail lift -> every visible point must be a source point again
        check(nm in SO and float(np.abs(of).max(initial=0)) < (cfg.get('hem_clear', {}).get('cap', 3.0) + 0.05 if nm in [p[0] for p in cfg['pieces'] if p[3].startswith('skirt')] and cfg.get('hem_clear') else (4.5 if cfg.get('layer_lift') else (3.5 if W.DESIGNS.get(DZ_PLUMB.get('design', ''), {}).get('tip_plumb') else 2.5))), f'{nm}: tail lift recorded for {len(ix)} pts (max {float(np.linalg.norm(of, axis=1).max(initial=0)):.2f})')
        if nm in SO: SO[nm].pos = np.array(SO[nm].pos, float); SO[nm].pos[ix] -= of
    ns, TS = load(src_path); C.to_world(TS)
    don = {}                                         # SoS: men's shaders come from the frozen PBR donor (same shape name)
    if cfg.get('shader_donor'):
        dn_, DT_ = load(cfg['shader_donor']); don = {x.name: x for x in DT_}
    if names_1: W.canon_names(TS, {'names_1': names_1}, '0')        # vanilla women: the author's _0 shape names -> the _1 ones
    vis_out = [t for t in TO if t.name not in N.hidden and t.name not in getattr(N, 'added', ())]
    for t in [t for t in TO if t.name in getattr(N, 'added', ())]:      # 2026-10-14: an added drawn shape (the Eastmarch backing) - no source by design
        print(f'   {t.name}: added by design ({len(t.pos)} pts, {len(t.tris)} tris) - not compared with the source')
    for t in TS:
        if t.name in cfg['drop'] or t.name == 'VirtualGround': check(t.name not in SO or t.name == 'VirtualGround', f'{t.name} dropped'); continue
        outs = [o for o in vis_out if o.tex == (don[t.name].tex if t.name in don else t.tex)]
        tc = t
        if t.name in cfg.get('drop_comps', {}):           # removed on purpose (duplicates the HDT patch left behind)
            from types import SimpleNamespace
            lab_ = D.welded_components(t.pos, t.tris); keep_ = ~np.isin(lab_[t.tris], cfg['drop_comps'][t.name]).all(1)
            tc = SimpleNamespace(pos=t.pos, uv=t.uv, tris=t.tris[keep_])
            print(f'   {t.name}: {int((~keep_).sum())} triangles of components {cfg["drop_comps"][t.name]} removed on purpose')
        if dropped and t.name in dropped:                  # v19b: the gusset strip bridging the openings, dropped by build_rework
            from types import SimpleNamespace
            gone = dropped[t.name]
            keep_ = np.array([tuple(sorted(int(v) for v in tr)) not in gone for tr in tc.tris])
            tc = SimpleNamespace(pos=tc.pos, uv=tc.uv, tris=tc.tris[keep_])
            check(int((~keep_).sum()) == len(gone), f'{t.name}: {int((~keep_).sum())} gusset triangles dropped on purpose (recorded {len(gone)})')
        n, kept, new, extra = K.compare(tc, outs)
        if welded and welded.get(t.name) and t.name in SO:       # v13: seam triangles split at welded points - nothing lost, nothing doubled
            cov = weld_cover(tc, SO[t.name]); wrec = welded[t.name]; want = wrec['parents'] if isinstance(wrec, dict) else wrec
            made_p = [p[0] for p in cfg['pieces'] if p[1] == t.name and p[0] in SO]
            a_rem = area(SO[t.name].pos, SO[t.name].tris); a_exp = area(tc.pos, tc.tris) - sum(area(SO[nm].pos, SO[nm].tris) for nm in made_p)
            check(abs(a_rem - a_exp) < 1e-3 * a_exp, f'{t.name}: welded remainder area {a_rem:.1f} vs the source minus its pieces {a_exp:.1f} '
                  f'({cov} of {want} split triangles tiled exactly by their children; {wrec["points"] if isinstance(wrec, dict) else wrec} weld points)')
            kept += want
        # triangles this source shape shares with another source shape of the same texture (already doubled in the original)
        tk = lambda x: {tuple(sorted(tuple(np.round(x.pos[i], 3)) for i in tr)) for tr in x.tris}
        dup_src = len(tk(tc) & set().union(*[tk(u) for u in TS if u is not t and u.tex == t.tex])) if any(u is not t and u.tex == t.tex for u in TS) else 0
        if dup_src: print(f'   {t.name}: {dup_src} triangles are doubled in the original mesh already')
        split_names = [p[0] for p in cfg['pieces'] if p[1] == t.name and p[0] in cfg['subdiv']]
        if split_names:
            made = [p[0] for p in cfg['pieces'] if p[1] == t.name] + ([t.name] if t.name in SO and t.name not in [p[0] for p in cfg['pieces']] else [])
            a_src = area(tc.pos, tc.tris); a_out = sum(area(SO[nm].pos, SO[nm].tris) for nm in made if nm in SO)   # v19b: minus the dropped gusset (SO is already unlifted above)
            check(abs(a_out - a_src) < 1e-2 * a_src, f'{t.name}: split into 4 per triangle, area {a_out:.1f} vs {a_src:.1f}')
        elif t.name == next((p[1] for p in cfg['pieces'] if p[0] == 'Cinto' or p[3] == 'belt'), None) and 'tip' in cfg['subdiv']:
            a_out = area(SO['Cinto'].pos, SO['Cinto'].tris); a_src = area(t.pos, t.tris)
            bsel = next((p[2] for p in cfg['pieces'] if p[0] == 'Cinto' or p[3] == 'belt'), None)
            if bsel is not None and bsel[0] == 'comps':     # SoS Officer: the belt is ONE component of the trousers shape - compare its own triangles
                lab_b = D.welded_components(t.pos, t.tris); a_src = area(t.pos, t.tris[np.isin(lab_b[t.tris], bsel[1]).all(1)])
            else:       # 2026-10-13: a belt cut by islands out of a shape that gives other pieces too (the Whiterun heavy's BeltsM_1: belt + its side bag,
                        # the bag no longer subdivided) - every piece cut from it + its remainder must tile it (the split branch's sum)
                made_b = [p[0] for p in cfg['pieces'] if p[1] == t.name] + ([t.name] if t.name in SO and t.name not in [p[0] for p in cfg['pieces']] else [])
                a_out = sum(area(SO[nm].pos, SO[nm].tris) for nm in made_b if nm in SO)
            check(kept + 0 <= n and abs(a_out - a_src) < 1e-2 * a_src, f'{t.name}: belt (tip split) area {a_out:.1f} vs {a_src:.1f}; untouched triangles kept {kept} of {n}')
        else:
            check(kept == n and extra <= dup_src, f'{t.name}: {n} triangles, kept {kept} in {[o.name for o in outs]}, duplicated {extra}' + (f' (original already doubles {dup_src})' if dup_src else ''))
        for o in outs:
            if o.name != t.name and o.name not in [p[0] for p in cfg['pieces'] if p[1] == t.name]: continue   # same texture, other source
            p0, p1 = (don[t.name] if t.name in don else t).s.shader.properties, o.s.shader.properties
            ds = o.name in cfg.get('double_sided', ())          # v18: a piece the builder makes double-sided (SLSF2 0x10) on purpose
            f2_src, f2_out = p0.Shader_Flags_2 | (0x10 if ds else 0), p1.Shader_Flags_2
            same = (p0.Shader_Type, p0.Shader_Flags_1, f2_src) == (p1.Shader_Type, p1.Shader_Flags_1, f2_out) and o.s.flags == t.s.flags
            al = (t.s.has_alpha_property == o.s.has_alpha_property)
            if not (same and al): check(False, f'{o.name}: shader / flags / alpha differ from {t.name}')
            if ds: check(bool(p1.Shader_Flags_2 & 0x10), f'{o.name}: double-sided flag set')
    infl = max(len(w) for t in TO for w in t.w); sums = max(abs(sum(w.values()) - 1) for t in TO for w in t.w)
    nbm = max(len(t.s2b) for t in TO)
    check(infl <= 4 and sums < 1e-3 and nbm <= 80, f'influences max {infl}, weight sums off by <= {sums:.1e}, bones per shape max {nbm}')
    hdt = [e.string_data for e in no.root.extra_data() if 'HDT' in (e.name or '')]
    check(hdt == [cfg['xml']], f'HDT -> {hdt}')
    xs, xb, cons = K.xml_info(cfg.get('stage', W.STAGE) + cfg['xml'].replace('\\', '/'))
    nodes = set(no.nodes)
    check(all(s in SO for s in xs), f'XML shapes in the mesh: {[s for s in xs if s not in SO] or "all"}')
    check(all(b in nodes or C.is_skel(b) for b in xb), f'XML bones are nodes / skeleton: {[b for b in xb if b not in nodes and not C.is_skel(b)] or "all"}')
    used = set()
    for s in xs: used |= set(SO[s].s2b)
    check(not (used - set(xb)), f'collision-shape bones declared: {sorted(used - set(xb)) or "all"}')
    check(all(a in xb and b in xb for a, b in cons), f'{len(cons)} constraints, bodies declared')
    rig_nodes = [b for b in nodes if N.is_phys(b) and b not in SO]
    check(all(b in xb for b in rig_nodes), f'{len(rig_nodes)} rig nodes, all declared')
    seam_check(SO, cfg, pos_written)                               # v13: the cut seams are watertight (no T-junctions, same weights both sides)
    return SO, TS, xs


def smooth(label, SO, cfg, N):
    for nm in [p[0] for p in cfg['pieces'] if p[3].startswith('skirt')]:
        s = SO[nm]
        ch = np.array([len({b.rsplit(' ', 1)[0] for b in w if b.startswith(tuple(f'{N.p} {x}' for x in ('Skirt',) + W.GROUP_WORDS))}) for w in s.w])   # SoS Officer v2: + the extra layers' chains
        mov = ch > 0
        print(f'  {label} {nm}: points with physics {mov.mean():.0%}, of those on 2 chains {np.mean(ch[mov] == 2):.0%}')


def bag_checks(label, design, g, nif_path, SO, rep_g):
    """2026-10-13 (PLAN_BAGS.md; user: the bags 'stretch and bend weirdly'): every RIGID tail (a bag / pouch, tail_rigid) - each body point
    below its hang line 1.0 on the bag's one bone, and the body's edges stretch less than 0.5 % over the game's clips and with the bag swung
    to every corner of its joint limits (coat_lib.piece_strain)"""
    Dz = W.DESIGNS[design]; p = Dz['prefix']
    for key, tr in (rep_g.get('tails') or {}).items():
        if not tr.get('rigid') or key not in SO: continue
        idx = tr['rigid']; bone = W.Names(p).tail(key, 1)
        bad = F.rigid_weights(SO[key], idx, bone)
        check(not bad, f'{label}: {key} rigid - {len(idx)} body pts below z {tr["hang_z"]:.1f} each 1.0 on {bone}' + (f' ({len(bad)} are not)' if bad else ''))
        worst, per, ntri = F.piece_strain(nif_path, key, p, key, Dz.get('sash_lim', W.SASH_LIM), idx, g='f' if g == 'f' else 'm')
        check(worst < F.STRAIN_MAX, f'{label}: {key} body ({ntri} tris) edge strain over the clips and its swing to every limit corner {worst * 100:.2f} % '
              f'(< {F.STRAIN_MAX * 100:.1f} %: ' + ', '.join(f'{k} {v * 100:.2f}' for k, v in per.items()) + ')')


SRC_FOLD_MAX_W = 0.55     # 2026-10-13: the user accepted THIN source folds - the Heavy women's 0.3-0.4-wide front strips under the Lovely Lady preset, then
                          # (same ruling) the light Eastmarch guard women's four 0.52-wide mail front-centre triangles: 0.5 -> 0.55 by the user's decision


def drop_gate(label, rep_g):
    """2026-10-13: copy triangles the build dropped for facing in (the builder's copy_drop / copy_drop_src). CALIBRATED: a triangle the SOURCE
    folds in (a BodySlide build / the thin weight, before any pull) up to SRC_FOLD_MAX_W wide is an accepted residual (user 2026-10-13: 'a
    gap that thin cannot let a point through, an in-facing face that size CAN pull points in') - reported, not a FAIL. A pull fold the repair
    could not undo, or a wider source fold, still FAILs (dropping folded copy triangles cost the Officer's hangers 13-20 covered points)"""
    allp = {k: set(v) for k, v in (rep_g.get('copy_drop') or {}).items()}
    src = {k: {int(t): float(w) for t, w in v} for k, v in (rep_g.get('copy_drop_src') or {}).items()}
    n_all = sum(len(v) for v in allp.values()); n_src = sum(len(v) for v in src.values())
    wide = [(k, t, round(w, 2)) for k, v in src.items() for t, w in v.items() if w > SRC_FOLD_MAX_W]
    posed = {k: set(v) for k, v in (rep_g.get('copy_drop_posed') or {}).items()}; n_posed = sum(len(v) for v in posed.values())    # 2026-10-14: dropped by design
    pull = {k: v - set(src.get(k, {})) - posed.get(k, set()) for k, v in allp.items()}; n_pull = sum(len(v) for v in pull.values())
    if not n_all: check(True, f'{label}: no copy triangle dropped'); return
    wmax = max((w for v in src.values() for w in v.values()), default=0.0)
    check(not n_pull and not wide, f'{label}: {n_src - len(wide)} source-fold copy triangles dropped (folded in by the source before any pull, <= {SRC_FOLD_MAX_W} wide, '
          f'widest {wmax:.2f}: accepted residual, user 2026-10-13)' + (f'; {len(wide)} WIDER source folds {wide[:4]}' if wide else '')
          + (f'; {n_pull} pull folds dropped: ' + ', '.join(f'{k} {len(v)}' for k, v in pull.items() if v) if n_pull else '')
          + (f'; {n_posed} dropped by posed_drop (a hanging piece behind them on the clips - the rule, not a fold)' if n_posed else ''))


def men(design, g='m'):
    """men, or (g='v') the women on the vanilla body - same layout: the author's _0 / _1 meshes in, _0 / _1 out"""
    DZ_PLUMB['design'] = design; cfg = W.DESIGNS[design][g]; N = W.Names(W.DESIGNS[design]['prefix']); who = 'men' if g == 'm' else 'vanilla women'
    n1, T1 = load(cfg['src'].format('1')); names_1 = [(t.name, len(t.pos), len(t.tris)) for t in T1]
    hid = {}
    rep_g = json.load(open(W.WORK + 'rework_report.json'))[design][g]
    swp = {}
    for v in ('1', '0'):
        lf = lift_of(design, g, v)
        SO, TS, xs = structure(f'{who} _{v}', cfg['out'].format(v), cfg['src'].format(v), cfg, N, names_1=names_1 if v == '0' else None, lift=lf, dropped=dropped_of(design, g, v),
                               welded=rep_g.get('welded', {}))
        if v == '1': smooth(who, SO, cfg, N)
        K.rest(f'{who} _{v}', relift({n: t.pos for n, t in SO.items()}, lf), {n: t.tris for n, t in SO.items()}, xs)
        prism_rest(f'{who} _{v}', relift({n: t.pos for n, t in SO.items()}, lf), {n: t.tris for n, t in SO.items()}, xs)   # v15b
        hid[v] = {n: (len(t.pos), len(t.tris)) for n, t in SO.items()}
        swp[v] = (relift({n: t.pos for n, t in SO.items()}, lf), {n: t.tris for n, t in SO.items()}, xs)
        bag_checks(f'{who} _{v}', design, g, cfg['out'].format(v), SO, rep_g)        # 2026-10-13: rigid bags
    if cfg.get('pants_vary'):            # v12: Northern Knight's author trousers differ per weight by design (1821 vs 2213 pts)
        for v in hid: hid[v].pop(cfg['pants'], None)
    check(hid['0'] == hid['1'], f'{who}: _0 and _1 have the same shapes, points and triangles' +
          ('' if hid['0'] == hid['1'] else f' (differ: {[n for n in set(hid["0"]) | set(hid["1"]) if hid["0"].get(n) != hid["1"].get(n)]})'))
    # 2026-10-13 (user: 'Guards wear these armours at random weights, so every fix ... has to hold at EVERY weight'): the game blends _0 / _1
    # vertex by vertex - every hanging piece vs its copy at weights 0..1 in 0.1 steps (points within the margins + 0.4, in-facing copy triangles)
    F.weight_sweep(f'{who} weights', swp['0'][0], swp['1'][0], swp['1'][1], swp['1'][2], rep_g['centre'])
    drop_gate(f'{who}', rep_g)                 # 2026-10-13: dropped copy triangles - only the accepted source folds pass


def women(design):
    DZ_PLUMB['design'] = design; cfg = W.DESIGNS[design]['f']; N = W.Names(W.DESIGNS[design]['prefix'])
    rep = json.load(open(W.WORK + 'rework_report.json'))[design]['f']
    tree0 = ET.parse(cfg['osp']); ss0 = next(s for s in tree0.getroot().findall('SliderSet') if s.get('name') == cfg['set'])
    src = os.path.dirname(os.path.dirname(cfg['osp'])) + f'/ShapeData/{ss0.findtext("DataFolder")}/{ss0.findtext("SourceFile")}'
    out = rep['outs'][0]
    lf = lift_of(design, 'f', '1')
    SO, TS, xs = structure('women (BodySlide ShapeData)', out, src, cfg, N, lift=lf, dropped=dropped_of(design, 'f', '1'), welded=rep.get('welded', {}))
    bag_checks('women', design, 'f', out, SO, rep)        # 2026-10-13: rigid bags
    smooth('women', SO, cfg, N)
    tree1 = ET.parse(W.STAGE_F + 'CalienteTools/BodySlide/SliderSets/' + os.path.basename(cfg['osp']))
    ss1 = next(s for s in tree1.getroot().findall('SliderSet') if s.get('name') == cfg['set'])
    check(sorted(e.get('target') for e in ss1.findall('Shape')) == sorted(SO), f'osp set shapes = mesh shapes ({len(SO)})')
    e0 = dict(read_osd(src[:-4] + '.osd')[2]); e1 = dict(read_osd(out[:-4] + '.osd')[2])
    keys = [d.text.split('\\', 1)[1] for sl in ss1.findall('Slider') for d in sl.findall('Data')]
    check(all(k in e1 for k in keys), f'every osp slider entry ({len(keys)}) is in the osd')
    S0 = {t.name: t for t in TS}
    base0 = {n: t.pos for n, t in S0.items()}; base1 = {n: t.pos for n, t in SO.items()}
    # visible point -> source point by position + UV
    vis = [n for n in SO if n not in N.hidden and n not in getattr(N, 'added', ())]     # 2026-10-14: an added drawn shape (the backing) has no source by design
    for n in [n for n in SO if n in getattr(N, 'added', ())]: print(f'   {n}: added by design ({len(SO[n].pos)} pts) - not matched to the source; its slider data by provenance')
    match = {}
    for n in vis:
        o = SO[n]; srcs = [t for t in TS if t.tex == o.tex]; idx = []
        Ms = [(t, K.Matcher(t.pos, t.uv)) for t in srcs]
        for k in range(len(o.pos)):
            hit = None
            for t, M in Ms:
                mm = M.near(o.pos[k], o.uv[k])
                if mm: hit = (t.name, mm[0]); break
            idx.append(hit)
        if any(h is None for h in idx) and (n in cfg['subdiv'] or (n == 'Cinto' and 'tip' in cfg['subdiv']) or n in rep.get('welded', {})):   # v13: welded seam points are source-edge midpoints too
            mids = defaultdict(list)       # by position only: the game keeps UVs at half precision (~2e-4)
            for t in srcs:
                for a_, b_ in {tuple(sorted(e)) for tr in t.tris for e in ((tr[0], tr[1]), (tr[1], tr[2]), (tr[2], tr[0]))}:
                    key = tuple(np.round((t.pos[a_] + t.pos[b_]) / 2, 3))
                    mids[key].append((t.name, int(a_), int(b_), (t.uv[a_] + t.uv[b_]) / 2))
            for k, h in enumerate(idx):
                if h is None:
                    c_ = mids.get(tuple(np.round(o.pos[k], 3)), [])
                    if c_:
                        best = min(c_, key=lambda e: float(np.abs(e[3] - o.uv[k]).max()))
                        if float(np.abs(best[3] - o.uv[k]).max()) < 5e-3: idx[k] = ('mid',) + best[:3]
            allm = [e for v_ in mids.values() for e in v_]
            for k, h in enumerate(idx):            # a midpoint on a rounding boundary: nearest one within 1e-3
                if h is None and allm:
                    src_ = {t.name: t for t in srcs}
                    dd = [(float(np.linalg.norm((src_[e[0]].pos[e[1]] + src_[e[0]].pos[e[2]]) / 2 - o.pos[k])), e) for e in allm]
                    dmin, e = min(dd, key=lambda x: x[0] + float(np.abs(x[1][3] - o.uv[k]).max()))
                    if dmin < 1e-3 and float(np.abs(e[3] - o.uv[k]).max()) < 5e-3: idx[k] = ('mid',) + e[:3]
            if n in rep.get('welded', {}) and any(h is None for h in idx):   # v13: a welded point lies ON a source edge (any parameter: an author T-junction)
                segs = {t.name: source_edges(t) for t in srcs}
                for k, h in enumerate(idx):
                    if h is not None: continue
                    for t in srcs:
                        M_, ek, EA, EB = segs[t.name]
                        if not len(ek): continue
                        d, tt = _seg_dist_t(np.asarray(o.pos[k], float)[None], EA, EB); j = int(d[0].argmin())
                        if d[0, j] < 0.02: idx[k] = ('edge', t.name, ek[j][0], ek[j][1], float(tt[0, j])); break
        match[n] = idx
        nmid = sum(1 for h in idx if h is not None and h[0] == 'mid'); nedge = sum(1 for h in idx if h is not None and h[0] == 'edge')
        check(all(h is not None for h in idx), f'{n}: every point is a source point' + (f' or the midpoint of a source edge ({nmid} midpoints)' if nmid else '')
              + (f' or a welded point on a source edge ({nedge})' if nedge else '') + f' ({sum(h is None for h in idx)} not found)')
    pre = K.preset(*W.PRESET)
    for lab, p in (('defaults', {}), ('user preset', pre)):
        ends = {}
        for size in ('small', 'big'):
            m0 = K.morph(ss0, e0, base0, p, size); m1 = K.morph(ss1, e1, base1, p, size)
            ends[size] = relift({n: m1[n] for n in SO}, lf)
            worst = 0.0
            for n in vis:
                for k, h in enumerate(match[n]):
                    if h is None: continue
                    if h[0] == 'edge':                      # v13: a welded point sits (up to 0.02 off) a source edge: its MORPH must be the edge's, interpolated
                        dw = (1.0 - h[4]) * (m0[h[1]][h[2]] - base0[h[1]][h[2]]) + h[4] * (m0[h[1]][h[3]] - base0[h[1]][h[3]])
                        worst = max(worst, float(np.abs((m1[n][k] - base1[n][k]) - dw).max())); continue
                    want = (m0[h[1]][h[2]] + m0[h[1]][h[3]]) / 2 if h[0] == 'mid' else m0[h[0]][h[1]]
                    worst = max(worst, float(np.abs(m1[n][k] - want).max()))
            check(worst < 1e-3, f'{lab} {size}: visible points = the original set\'s build (worst {worst:.1e})')
            wc = 0.0
            for c, mp in rep['copies'].items():
                if not mp: continue
                C0 = SO[c].pos
                for k, (sn, si) in enumerate(mp):
                    wc = max(wc, float(np.abs((m1[c][k] - C0[k]) - (m1[sn][si] - SO[sn].pos[si])).max()))
            check(wc < 1e-3, f'{lab} {size}: collision copies move like their source points (worst {wc:.1e})')
            K.rest(f'women {lab} {size}', relift({n: m1[n] for n in SO}, lf), {n: SO[n].tris for n in SO}, xs)
            prism_rest(f'women {lab} {size}', relift({n: m1[n] for n in SO}, lf), {n: SO[n].tris for n in SO}, xs)   # v15b
        # 2026-10-13: BodySlide writes the small / big builds as _0 / _1 and the game blends them at the character's weight - every hanging
        # piece vs its copy at weights 0..1 in 0.1 steps between them (points within the margins + 0.4, in-facing copy triangles)
        F.weight_sweep(f'women {lab} weights', ends['small'], ends['big'], {n: SO[n].tris for n in SO}, xs, rep['centre'])
    drop_gate('women', rep)                    # 2026-10-13: dropped copy triangles - only the accepted source folds pass


if __name__ == '__main__':
    W.use_designs(sys.argv[1]); d = sys.argv[2]; which = [a for a in sys.argv[3:] if a in ('m', 'f', 'v')] or ['m', 'f']
    which = [g for g in which if g in W.DESIGNS[d]]          # men-only designs
    if 'm' in which: men(d)
    if 'f' in which: women(d)
    if 'v' in which: men(d, 'v')
    print('ALL OK' if K.ok_all else 'CHECK ABOVE')
