"""clip_check: leg-collider trap check on the game's OWN clips (walk / run / sprint - whatever smpkit settings CLIPS names) for a
coat design, men's _1 mesh. The legs move frame by frame (smpkit.anim: PyNifly's Skyrim hkx reader, deformations relative to the
pelvis) while the skirt is HELD AT REST - the honest worst case, cloth that has not reacted yet. For every point of the skirt's
per-vertex lining shapes ('<p> Skirt Front/Side/Back' and the extra layers') against the leg piece its XML lets it hit:
  entered = inside the real trousers (the thigh went through the resting cloth there)
  caught  = ... and within the leg piece's catch (penetration + the two margins) behind an outward-facing triangle: pushed back out
  hooked  = behind a triangle whose normal points at the body's centre line (inner thigh): pushed between the legs
  pinched = within the catch of two triangles facing each other (pushed both ways)
  unseen  = entered but deeper than the catch: the trousers show through until the cloth reacts (the lag a wearer sees walking)
Numbers are summed over every second frame of a clip; the per-piece lines say WHERE (which shape, the heights). Compare versions and
designs (the SoS Officer: walk 1552/1058/319/0/175 vs the Chainmail coat the user confirmed 1979/1147/227/0/605). It cannot see
inertia or the chains' reaction - a comparison tool, not a promise.
usage: clip_check.py <designs.py> <design> [m]      (rebuild_coat.py runs it when CLIPS are configured; SUMMARY = worst clip)"""
import os, sys, json, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
import build_coat_rig as W
INNER = 0.6


def skin(t, Dm):
    out = np.zeros_like(t.pos)
    for i, (p, w) in enumerate(zip(t.pos, t.w)):
        ph = np.r_[p, 1]; acc = np.zeros(3); tot = 0.0
        for b, x in w.items(): acc += x * (Dm.get(b, np.eye(4)) @ ph)[:3]; tot += x
        out[i] = acc / max(tot, 1e-9)
    return out


def faces(P, F):
    n = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)


def xml_shapes(path):
    s = open(path, encoding='utf-8').read(); out = {}
    for m in re.finditer(r'<(per-triangle-shape|per-vertex-shape) name="([^"]+)">(.*?)</\1>', s, re.S):
        body = m.group(3); g = lambda k, d=0.0: float(re.search(rf'<{k}>([\d.]+)</{k}>', body).group(1)) if re.search(rf'<{k}>', body) else d
        out[m.group(2)] = dict(kind=m.group(1), margin=g('margin'), pen=g('penetration'), tags=re.findall(r'<tag>([^<]+)</tag>', body), can=re.findall(r'<can-collide-with-tag>([^<]+)</can-collide-with-tag>', body))
    return out


def main(d, g='m'):
    from smpkit import anim as A
    if not A.configured(g):
        print(f'{d} {g}: no clips configured (smpkit settings SKELETON_HKX_{g.upper()} + CLIPS)\nSUMMARY clips worst unseen/frame: 0 (not configured)'); return 0
    Dz = W.DESIGNS[d]; cfg = Dz[g]; p = Dz['prefix']
    rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    mesh = cfg['out'].format('1') if g == 'm' else rep['outs'][0]; xml = cfg['stage'] + cfg['xml'].replace('\\', '/')
    n, T = C.load(mesh); C.to_world(T); S = {t.name: t for t in T}; xs = xml_shapes(xml)
    legs = {nm: xs[nm] for nm in xs if nm.startswith(p + ' Legs ')}
    pts = {nm: xs[nm] for nm in xs if xs[nm]['kind'] == 'per-vertex-shape' and nm in S and any(c in {t for l in legs.values() for t in l['tags']} for c in xs[nm]['can'])}
    # the real trousers in the WRITTEN mesh: the component of the trousers shape that reaches the shins (component numbers shift once a
    # belt is cut out of the shape)
    t0 = S[cfg['pants']]; lab0 = W.D.welded_components(t0.pos, t0.tris)
    low = [c for c in set(lab0.tolist()) if t0.pos[lab0 == c, 2].min() < 30.0]
    c0 = max(low, key=lambda c: int((lab0 == c).sum())); v0 = np.where(lab0 == c0)[0]; rm0 = np.full(len(t0.pos), -1); rm0[v0] = np.arange(len(v0))
    pants = type('P', (), dict(pos=t0.pos[v0], tris=rm0[t0.tris[(lab0[t0.tris] == c0).all(1)]], w=[t0.w[i] for i in v0], s2b=t0.s2b))()
    s2b = {}
    for t in T: s2b.update(t.s2b)
    tris = pants.tris[pants.pos[pants.tris].mean(1)[:, 2] > W.LEG_ZMIN]
    if C.outward_fraction(pants.pos, tris, W.leg_axes(pants, {'s2b_all': s2b})) < 0.5: tris = tris[:, [0, 2, 1]]
    pants_t = type('P', (), dict(pos=pants.pos, tris=tris, w=pants.w))(); cx = float(pants.pos[:, 0].mean())
    print(f'== {d} {g} _1: {os.path.basename(mesh)}; leg pieces ' + ', '.join(f'{nm.split()[-1]} pen {legs[nm]["pen"]} margin {legs[nm]["margin"]}' for nm in legs)
          + '; points ' + ', '.join(f'{nm.replace(p + " ", "")} {len(S[nm].pos)}' for nm in pts))
    print('   clip      frames   entered  caught  HOOKED  PINCHED  unseen   (summed over every 2nd frame; worst frame = most unseen in one frame)')
    worst_all = 0
    for ck, cp in A.CLIPS[g].items():
        fr = A.load_clip(cp, g)[0]; tot = np.zeros(5, int); worst = 0; per = {}; zz = {}
        for Dm in fr[::2]:
            PP = skin(pants_t, Dm); posed = {nm: (skin(S[nm], Dm), S[nm].tris) for nm in legs}
            ent = cau = hook = pin = uns = 0
            for pn, px in pts.items():
                Q = S[pn].pos
                tri, _, dd, cp_ = C.Surface([('t', PP, pants_t.tris)]).query(Q, k=8)
                fn = faces(PP, pants_t.tris)[tri]; inside = ((Q - cp_) * fn).sum(1) < -0.1
                if not inside.any(): continue
                Qi = Q[inside]; seen = np.zeros(len(Qi), bool); hooked = np.zeros(len(Qi), bool); pushes = [[] for _ in range(len(Qi))]
                for ln, lx in legs.items():
                    if not any(t in px['can'] for t in lx['tags']): continue
                    LP, LT = posed[ln]; LN = faces(LP, LT)
                    tri2, _, d2, cp2 = C.Surface([('l', LP, LT)]).query(Qi, k=8); n2 = LN[tri2]; sd = ((Qi - cp2) * n2).sum(1)
                    catch = (sd < 0) & (sd > -(lx['pen'] + lx['margin'] + px['margin']))
                    c2 = LP[LT[tri2]].mean(1); inner = (n2[:, 0] * np.sign(c2[:, 0] - cx)) < -INNER
                    seen |= catch; hooked |= catch & inner
                    for i in np.where(catch)[0]: pushes[i].append(n2[i])
                pinched = np.array([any(float(a @ b) < -0.5 for ai, a in enumerate(pp) for b in pp[ai + 1:]) for pp in pushes])
                ent += int(inside.sum()); cau += int((seen & ~hooked).sum()); hook += int(hooked.sum()); pin += int(pinched.sum()); uns += int((~seen).sum())
                per.setdefault(pn, np.zeros(3, int)); per[pn] += np.array([int(inside.sum()), int(hooked.sum()), int((~seen).sum())])
                if (~seen).any(): zz.setdefault(pn, []).extend(Qi[~seen][:, 2].tolist())
            tot += np.array([ent, cau, hook, pin, uns]); worst = max(worst, uns)
        print(f'   {ck:8s} {len(fr[::2]):6d}   {tot[0]:7d} {tot[1]:7d} {tot[2]:7d} {tot[3]:8d} {tot[4]:7d}   worst frame unseen {worst}')
        for pn in per:
            print(f'      {pn.replace(p + " ", ""):20s} entered {per[pn][0]:5d} hooked {per[pn][1]:4d} unseen {per[pn][2]:4d}' +
                  (f'  unseen z p10 {np.percentile(zz[pn], 10):.1f} p50 {np.median(zz[pn]):.1f} p90 {np.percentile(zz[pn], 90):.1f}' if pn in zz else ''))
        worst_all = max(worst_all, worst)
    print(f'SUMMARY clips worst unseen/frame: {worst_all}')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    W.use_designs(sys.argv[1]); sys.exit(main(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'm'))
