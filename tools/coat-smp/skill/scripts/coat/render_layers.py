"""What the user asked to see before anything installs: each MOVING layer of a built design ALONE (textured, four sides), the
whole armour at rest, the whole armour with the skirt chains flared out, and ray-casts through every slit (from outside, at
three heights, at rest and flared): which shapes a ray meets in order = what you see through the opening.
usage: render_layers.py <design> <g> <out.png> [flare1=0.45 flare=0.15]"""
import sys, json, numpy as np, cv2
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
import build_coat_rig as W, coat_lib as F
load, wrap, rot, prism_rest = C.load, C.wrap, K.rot, F.prism_rest
import numpy as np, cv2
import coat_layers as LY
K.TEX = None



def ray_hits(o, d, P, T_):
    v0, v1, v2 = P[T_[:, 0]], P[T_[:, 1]], P[T_[:, 2]]; e1, e2 = v1 - v0, v2 - v0
    h = np.cross(d, e2); a = (e1 * h).sum(1); ok = np.abs(a) > 1e-9; f = np.zeros_like(a); f[ok] = 1.0 / a[ok]
    s = o - v0; u = f * (s * h).sum(1); q = np.cross(s, e1); v = f * (d * q).sum(1); t = f * (e2 * q).sum(1)
    hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0.05)
    return t[hit]


def main(d, g, out, f1=0.45, f2=0.15):
    Dz = W.DESIGNS[d]; cfg = Dz[g]; p = Dz['prefix']; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    n, T = load(rep['outs'][0]); C.to_world(T); S = {t.name: t for t in T}
    Gw = F.bone_world(T)
    for nm, nd in n.nodes.items():
        if nm not in Gw and nm.startswith(p + ' '):
            M_ = np.eye(4); M_[:3, 3] = nd.global_transform.translation; Gw[nm] = M_
    cx, cy = rep['centre']; ch = F.chains(Gw, p)
    Dm = LY.pose_all(F, Gw, p, d, g, cx, cy, 'flare', float(f1), float(f2))      # SoS Officer v2: every layer's chains
    vis = [t for t in T if t.tex and any(t.tex)]
    tex = {t.name: (K.load_tex(t.tex[0]) if t.tex[0] else None) for t in vis}
    posed = {t.name: F.skin(t.pos, t.w, Dm) for t in vis}
    moving = [nm for nm, src, sel, role in cfg['pieces']]
    grey = [(t.pos, t.tris, t.uv, None, (70, 70, 70)) for t in vis if t.name not in moving]   # the static rest, grey, for context
    rows = []

    def row(label, geoms, z0=84, z1=34):
        img = np.hstack([K.render(geoms, v, S=4.0, W=260, Z0=z0, Z1=z1) for v in ('front', 'side', 'back', 'left')])
        cv2.putText(img, label, (6, 16), 0, 0.45, (255, 255, 255), 1); rows.append(img)
    row(f'{d} {g}: as built, at rest', [(t.pos, t.tris, t.uv, tex[t.name], 0) for t in vis])
    for nm in moving:
        if nm in S: row(f'{nm} ALONE (static parts grey)', grey + [(S[nm].pos, S[nm].tris, S[nm].uv, tex[nm], 0)])
    row(f'skirt flared {f1}/{f2} rad (chains out; hanging pieces on their own bones at rest)', [(posed[t.name], t.tris, t.uv, tex[t.name], 0) for t in vis])
    LW = LY.layers(d, g)
    if len(LW) > 1:          # SoS Officer v2: each layer swung out ALONE (the others at rest) - the layers move separately
        for word, ph in LW:
            l1, l = LY.lims(ph); F.LIM1.update(l1); F.LIM.update(l)
            Dw = F.flare(Gw, LY.chains(Gw, p, word), cx, cy, min(float(f1), l1['out']), min(float(f2), l['out']))
            row(f'only the {"mail" if word == "Skirt" else word.lower()} layer swung out (the other layers at rest)',
                [(F.skin(t.pos, t.w, Dw), t.tris, t.uv, tex[t.name], 0) for t in vis])
    cv2.imwrite(out, np.vstack(rows)); print(out)
    # rays through the slits: from outside, aimed at the body axis, at three heights per slit
    print('rays through the slits (from outside toward the body axis; shapes met in order, first = outermost):')
    for c, hw, top in list(rep['slits']) + [tuple(s_) for gr in rep.get('groups', {}).values() for s_ in gr['slits']]:   # + the extra layers' openings
        hem = float(min(t.pos[:, 2].min() for t in vis))     # v5: the lowest visible moving piece (no fixed piece name)
        for z in (top - 3.0, (top + hem) / 2, hem + 2.0):
            for lab, PP in (('rest', {t.name: t.pos for t in vis}), ('flared', posed)):
                a = np.radians(c); dvec = -np.array([np.sin(a), np.cos(a), 0.0]); o = np.array([cx, cy, z]) - dvec * 40.0
                hits = []
                for t in vis:
                    for tt in ray_hits(o, dvec, np.asarray(PP[t.name]), t.tris): hits.append((float(tt), t.name))
                hits.sort(); seq = [nm for _, nm in hits]
                seq = [x for i, x in enumerate(seq) if i == 0 or x != seq[i - 1]]
                print(f'   slit at {c:+.0f} deg (top z {top:.1f}), z {z:.1f} {lab:6s}: ' + (' > '.join(seq[:5]) or 'nothing'))


if __name__ == '__main__':
    a = sys.argv[1:]; W.use_designs(a[0]); K.TEX = W.WORK + 'tex_png'; K.TEXROOTS[:0] = list(W.TEX_ROOTS); main(a[1], a[2], a[3], *(float(x) for x in a[4:6]))
