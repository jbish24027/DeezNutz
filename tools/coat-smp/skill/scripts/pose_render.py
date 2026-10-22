"""Pose render: the source mesh at rest, then the built mesh at rest and with a right-front kick of the skirt chains
(every chain swung outward, strongest 25 deg right of front), front + right-side views. Use it to SEE the rig before
anyone loads the game: panels should bend smoothly, slits open, layers stay together, nothing tears at the belt.
Needs opencv-python. Textures are found under the design's 'tex_roots' (mod folders holding textures\\...) and
converted with texconv (setting TEXCONV); without them shapes render flat grey.

usage:  python pose_render.py <design.py> [target] [kick_radians]      -> <work>/<name>_<target>_pose.png"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_skirt_rig as W
from smpkit import checks as K
C = W.C


def views(cv2, T, Q, label, z0=95, z1=25):
    Gs = [(q, t.tris, t.uv, K.load_tex(t.tex[0]), (170, 170, 170)) for t, q in zip(T, Q) if t.tex and t.tex[0]]
    im = np.hstack([K.render(Gs, v, S=6.0, W=400, Z0=z0, Z1=z1) for v in ('front', 'side')])
    cv2.putText(im, label, (8, 16), 0, 0.5, (255, 255, 255), 1); return im


def main(d, g=None, kick=1.0):
    import cv2
    Dz = W.DESIGNS[d]; g = g or next(iter(Dz['targets'])); N = W.Names(Dz['prefix'])
    r = json.load(open(W.WORK + f'{d}_report.json'))[g]
    K.TEX = W.WORK + 'tex_png'; K.TEXROOTS[:] = list(Dz.get('tex_roots', ()))
    K.TOTAL = float(kick)
    G = {nm: np.array(x) for nm, x in r['bones'].items()}
    chains = []
    for k in range(len(r['ang_k'])):
        bones = [N.sk(k, j) for j in range(1, W.NROW + 1)]
        chains.append((bones, np.array([G[b][:3, 3] for b in bones]), np.array([G[N.sk(k, j - 1)][:3, 3] for j in range(1, W.NROW + 1)])))
    rows = []
    cfg = Dz['targets'][g]
    if cfg['mode'] == 'nif':
        n0, T0 = C.load(cfg['src'].format(1)); C.to_world(T0)
        T0v = [t for t in T0 if t.tex and t.tex[0]]
        rows.append(views(cv2, T0v, [t.pos for t in T0v], 'source mesh, rest'))
    n1, T1 = C.load(r['outs'][0]); C.to_world(T1); T1v = [t for t in T1 if t.tex and t.tex[0]]
    rows.append(views(cv2, T1v, [t.pos for t in T1v], 'built mesh, rest'))
    rows.append(views(cv2, T1v, K.skin_shapes(T1v, K.pose(chains, r['centre'][0], r['centre'][1])), f'built mesh, right-front kick {kick} rad'))
    out = W.WORK + f'{d}_{g}_pose.png'
    cv2.imwrite(out, np.vstack(rows)); print('wrote', out)


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    d = W.use_design(sys.argv[1])
    main(d['name'], *(sys.argv[2:3] or [None]), *(sys.argv[3:4] or [1.0]))
