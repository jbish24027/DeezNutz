"""Checks for build_skirt_rig.py output. Run it after every build, before anything goes in game.

usage:  python verify_rig.py <design.py> [target ...]

  A structure: every source triangle is in the output once (unchanged, or - for subdivided pieces - its 4 children
    cover it exactly); each visible piece keeps its source shape's shader / textures / alpha / flags; <= 4 influences
    summing to 1, <= 80 bones per shape; the HDT string points at the XML; XML shapes exist in the mesh, XML bones are
    mesh nodes or skeleton bones, collision-shape bones declared, constraint bodies declared, every rig node declared
  B rest contacts: nothing the XML lets collide touches while standing (a contact at rest = twitching in game)
  C bodyslide targets: every visible point's simulated BodySlide build (small + big, set defaults and the optional
    target 'preset') = the original set's build of its source point; every collision copy moves like its source points
  D skirt smoothness: share of skirt points on physics, and of those how many blend two chains
Prints 'ALL OK' or 'CHECK ABOVE'."""
import os, sys, json
from collections import defaultdict
from types import SimpleNamespace
import numpy as np
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_skirt_rig as W
from smpkit import checks as K
C = W.C
check = K.check


def area(P, T_): return np.linalg.norm(np.cross(P[T_[:, 1]] - P[T_[:, 0]], P[T_[:, 2]] - P[T_[:, 0]]), axis=1).sum() / 2


def structure(label, out_path, src_path, cfg, N):
    print(f'== {label}: {os.path.basename(out_path)}')
    no, TO = C.load(out_path); C.to_world(TO); SO = {t.name: t for t in TO}
    ns, TS = C.load(src_path); C.to_world(TS)
    vis_out = [t for t in TO if t.name not in N.hidden]
    piece_names = [p[0] for p in cfg['pieces']]
    belt = next((p for p in cfg['pieces'] if p[3] == 'belt'), None)
    for t in TS:
        if t.name in cfg['drop'] or t.name == 'VirtualGround': check(t.name not in SO or t.name == 'VirtualGround', f'{t.name} dropped'); continue
        outs = [o for o in vis_out if o.tex == t.tex]
        tc = t
        if t.name in cfg.get('drop_comps', {}):           # removed on purpose
            lab_ = C.welded_components(t.pos, t.tris); keep_ = ~np.isin(lab_[t.tris], cfg['drop_comps'][t.name]).all(1)
            tc = SimpleNamespace(pos=t.pos, uv=t.uv, tris=t.tris[keep_])
            print(f'   {t.name}: {int((~keep_).sum())} triangles of components {cfg["drop_comps"][t.name]} removed on purpose')
        cu = cfg.get('cull_under')
        if t.name in cfg.get('cull', {}) or (cu and t.name == cu['shape']):     # body culled under a long skirt / a bodice, on purpose
            keep_ = np.ones(len(t.tris), bool)
            if t.name in cfg.get('cull', {}):
                keep_ &= ~W.cull_mask(t, cfg['cull'][t.name])
                print(f'   {t.name}: {int(W.cull_mask(t, cfg["cull"][t.name]).sum())} triangles between z {cfg["cull"][t.name]} culled on purpose')
            if cu and t.name == cu['shape']:
                um = W.cull_under_mask(t, [next(u for u in TS if u.name == c) for c in cu['cover']], cu); keep_ &= ~um
                print(f'   {t.name}: {int(um.sum())} triangles under {cu["cover"]} culled on purpose')
            tc = SimpleNamespace(pos=t.pos, uv=t.uv, tris=t.tris[keep_])       # (not combined with drop_comps)
        n, kept, new, extra = K.compare(tc, outs)
        # triangles this source shape shares with another source shape of the same texture (already doubled in the original)
        tk = lambda x: {tuple(sorted(tuple(np.round(x.pos[i], 3)) for i in tr)) for tr in x.tris}
        others = [u for u in TS if u is not t and u.tex == t.tex]
        dup_src = len(tk(tc) & set().union(*[tk(u) for u in others])) if others else 0
        if dup_src: print(f'   {t.name}: {dup_src} triangles are doubled in the original mesh already')
        split_names = [p[0] for p in cfg['pieces'] if p[1] == t.name and p[0] in cfg['subdiv']]
        if split_names:
            made = [p[0] for p in cfg['pieces'] if p[1] == t.name] + ([t.name] if t.name in SO and t.name not in piece_names else [])
            a_src = area(t.pos, t.tris); a_out = sum(area(SO[nm].pos, SO[nm].tris) for nm in made if nm in SO)
            check(abs(a_out - a_src) < 1e-2 * a_src, f'{t.name}: split into 4 per triangle, area {a_out:.1f} vs {a_src:.1f}')
        elif belt is not None and t.name == belt[1] and 'tip' in cfg['subdiv']:
            a_out = area(SO[belt[0]].pos, SO[belt[0]].tris); a_src = area(t.pos, t.tris)
            check(kept <= n and abs(a_out - a_src) < 1e-2 * a_src, f'{t.name}: belt (tip split) area {a_out:.1f} vs {a_src:.1f}; untouched triangles kept {kept} of {n}')
        else:
            check(kept == n and extra <= dup_src, f'{t.name}: {n} triangles, kept {kept} in {[o.name for o in outs]}, duplicated {extra}' + (f' (original already doubles {dup_src})' if dup_src else ''))
        for o in outs:
            if o.name != t.name and o.name not in [p[0] for p in cfg['pieces'] if p[1] == t.name]: continue   # same texture, other source
            p0, p1 = t.s.shader.properties, o.s.shader.properties
            same = (p0.Shader_Type, p0.Shader_Flags_1, p0.Shader_Flags_2) == (p1.Shader_Type, p1.Shader_Flags_1, p1.Shader_Flags_2) and o.s.flags == t.s.flags
            al = (t.s.has_alpha_property == o.s.has_alpha_property)
            if not (same and al): check(False, f'{o.name}: shader / flags / alpha differ from {t.name}')
    infl = max(len(w) for t in TO for w in t.w); sums = max(abs(sum(w.values()) - 1) for t in TO for w in t.w)
    nbm = max(len(t.s2b) for t in TO)
    check(infl <= 4 and sums < 1e-3 and nbm <= C.MAXB, f'influences max {infl}, weight sums off by <= {sums:.1e}, bones per shape max {nbm}')
    hdt = [e.string_data for e in no.root.extra_data() if 'HDT' in (e.name or '')]
    check(hdt == [cfg['xml']], f'HDT -> {hdt}')
    xs, xb, cons = K.xml_info(W.STAGE + cfg['xml'].replace('\\', '/'))
    nodes = set(no.nodes)
    check(all(s in SO for s in xs), f'XML shapes in the mesh: {[s for s in xs if s not in SO] or "all"}')
    check(all(b in nodes or C.is_skel(b) for b in xb), f'XML bones are nodes / skeleton: {[b for b in xb if b not in nodes and not C.is_skel(b)] or "all"}')
    used = set()
    for s in xs: used |= set(SO[s].s2b)
    check(not (used - set(xb)), f'collision-shape bones declared: {sorted(used - set(xb)) or "all"}')
    check(all(a in xb and b in xb for a, b in cons), f'{len(cons)} constraints, bodies declared')
    rig_nodes = [b for b in nodes if N.is_phys(b) and b not in SO]
    check(all(b in xb for b in rig_nodes), f'{len(rig_nodes)} rig nodes, all declared')
    return SO, TS, xs


def smooth(label, SO, cfg, N):
    for nm in [p[0] for p in cfg['pieces'] if p[3].startswith('skirt')]:
        s = SO[nm]
        ch = np.array([len({b.rsplit(' ', 1)[0] for b in w if b.startswith(N.p + ' Skirt')}) for w in s.w])
        mov = ch > 0
        print(f'  {label} {nm}: points with physics {mov.mean():.0%}, of those on 2 chains {np.mean(ch[mov] == 2):.0%}')


def nif_target(design, g):
    cfg = W.DESIGNS[design][g]; N = W.Names(W.DESIGNS[design]['prefix'])
    for v in ('1', '0'):
        SO, TS, xs = structure(f'{g} _{v}', W.STAGE + cfg['out'].format(v), cfg['src'].format(v), cfg, N)
        if v == '1': smooth(g, SO, cfg, N)
        K.rest(f'{g} _{v}', {n: t.pos for n, t in SO.items()}, {n: t.tris for n, t in SO.items()}, xs)


def legs_body_part(part, ss1):
    """one body part a dress's leg colliders were made from, restricted to the dress set's sliders with the dress set's
    defaults (what BodySlide applies to the colliders) -> (set, osd, {shape: base pos}, shape)"""
    ssb = next(s for s in ET.parse(part['osp']).getroot().findall('SliderSet') if s.get('name') == part['set'])
    src = (part.get('bsroot') or os.path.dirname(os.path.dirname(part['osp']))).rstrip('/') + \
        f'/ShapeData/{ssb.findtext("DataFolder")}/{ssb.findtext("SourceFile")}'
    _, B = C.load(src); C.to_world(B); body = next(t for t in B if t.name == part['shape'])
    bsl = {sl.get('name'): sl for sl in ssb.findall('Slider') if sl.get('uv') != 'true' and sl.get('zap') != 'true'}
    ss = ET.Element('SliderSet'); osd = {}
    for sl in ss1.findall('Slider'):
        if sl.get('name') not in bsl: continue
        e = ET.SubElement(ss, 'Slider', dict(sl.attrib))
        for d in bsl[sl.get('name')].findall('Data'):
            if d.get('target') != part['shape']: continue
            e.append(d); fname = d.text.split('\\', 1)[0]
            if fname not in osd: osd.update(C.read_osd(os.path.dirname(src) + '/' + fname)[2])
    return ss, osd, {part['shape']: body.pos}, part['shape']


def legs_body_set(lb, ss1):
    """report 'legs_body' -> ([per part (set, osd, base, shape)], {collider: [(part, point)]}); old single-part reports
    (osp/set/shape at the top, plain point lists) still read"""
    if not lb: return None
    parts = lb.get('parts') or [lb]
    copies = {nm: [tuple(x) if isinstance(x, (list, tuple)) else (0, int(x)) for x in ix] for nm, ix in lb['copies'].items()}
    return [legs_body_part(p, ss1) for p in parts], copies


def bodyslide_target(design, g):
    cfg = W.DESIGNS[design][g]; N = W.Names(W.DESIGNS[design]['prefix'])
    rep = json.load(open(W.WORK + f'{design}_report.json'))[g]
    bsroot = os.path.dirname(os.path.dirname(cfg['osp'])) + '/'
    tree0 = ET.parse(cfg['osp']); ss0 = next(s for s in tree0.getroot().findall('SliderSet') if s.get('name') == cfg['set'])
    src = bsroot + f'ShapeData/{ss0.findtext("DataFolder")}/{ss0.findtext("SourceFile")}'
    out = rep['outs'][0]
    SO, TS, xs = structure(f'{g} (BodySlide ShapeData)', out, src, cfg, N)
    smooth(g, SO, cfg, N)
    tree1 = ET.parse(W.STAGE + 'CalienteTools/BodySlide/SliderSets/' + os.path.basename(cfg['osp']))
    ss1 = next(s for s in tree1.getroot().findall('SliderSet') if s.get('name') == cfg['set'])
    check(sorted(e.get('target') for e in ss1.findall('Shape')) == sorted(SO), f'osp set shapes = mesh shapes ({len(SO)})')
    e0 = dict(C.read_osd(src[:-4] + '.osd')[2]); e1 = dict(C.read_osd(out[:-4] + '.osd')[2])
    keys = [d.text.split('\\', 1)[1] for sl in ss1.findall('Slider') for d in sl.findall('Data')]
    check(all(k in e1 for k in keys), f'every osp slider entry ({len(keys)}) is in the osd')
    S0 = {t.name: t for t in TS}
    base0 = {n: t.pos for n, t in S0.items()}; base1 = {n: t.pos for n, t in SO.items()}
    belt = next((p[0] for p in cfg['pieces'] if p[3] == 'belt'), None)
    # visible point -> source point by position + UV (or the midpoint of a source edge, for subdivided pieces)
    vis = [n for n in SO if n not in N.hidden]
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
        if any(h is None for h in idx) and (n in cfg['subdiv'] or (n == belt and 'tip' in cfg['subdiv'])):
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
        match[n] = idx
        nmid = sum(1 for h in idx if h is not None and h[0] == 'mid')
        check(all(h is not None for h in idx), f'{n}: every point is a source point' + (f' or the midpoint of a source edge ({nmid} midpoints)' if nmid else '') +
              f' ({sum(h is None for h in idx)} not found)')
    presets = [('set defaults', {})]
    if cfg.get('preset'): presets.append(('preset', K.preset(*cfg['preset'])))      # (preset xml path, preset name)
    lbody = legs_body_set(rep.get('legs_body'), ss1)
    for lab, p in presets:
        for size in ('small', 'big'):
            m0 = K.morph(ss0, e0, base0, p, size); m1 = K.morph(ss1, e1, base1, p, size)
            if lbody is not None:       # leg colliders made from the body's own mesh (+ feet) move like the body's own build
                parts, copies = lbody
                disp = [K.morph(ssb, eb, baseb, p, size)[shp] - baseb[shp] for ssb, eb, baseb, shp in parts]; wl = 0.0
                for nm, pix in copies.items():
                    want = np.array([disp[pp][ii] for pp, ii in pix])
                    wl = max(wl, float(np.abs((m1[nm] - SO[nm].pos) - want).max()))
                check(wl < 1e-3, f'{lab} {size}: leg colliders move like the body parts they were made from ({len(parts)} part(s), worst {wl:.1e})')
            worst = 0.0
            for n in vis:
                for k, h in enumerate(match[n]):
                    if h is None: continue
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
            K.rest(f'{g} {lab} {size}', {n: m1[n] for n in SO}, {n: SO[n].tris for n in SO}, xs)


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    d = W.use_design(sys.argv[1])
    for g in sys.argv[2:] or list(d['targets']):
        (nif_target if d['targets'][g]['mode'] == 'nif' else bodyslide_target)(d['name'], g)
    print('ALL OK' if K.ok_all else 'CHECK ABOVE')
