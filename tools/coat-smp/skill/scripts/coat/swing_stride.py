# skill coat copy (from sos-smp-rework/) of swing_stride.py (2026-10-11): checks build_sos designs; ported 2026-10-11.
"""Stuck-on-the-legs check with the skirt mid-swing: the legs stride (stride_test poses) while the skirt chains are turned
(curled in to the joint limit / swung back / forward / sideways, clamped to the design's own XML limits). For every
skirt lining point (the per-vertex colliders 'Skirt Front/Side/Back') against its matching one-sided leg piece:
  caught = inside the leg collider within its catch depth (pushed back out),
  hooked = caught but pushed the wrong way (front panel pushed back / back panel pushed forward),
  sunk   = deeper than the catch depth: the collider lets go, the point sits inside the leg until the leg moves away.
usage: swing_stride.py <design> [m|f]"""
import sys, json, numpy as np
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
import build_coat_rig as W, coat_lib as F
load, wrap, rot, prism_rest = C.load, C.wrap, K.rot, F.prism_rest
import coat_layers as LY


PEN = {'Front': 3.0, 'Back': 3.0, 'Side': 1.5}


def lims(phys):
    l1, l = phys['SK_LIM1'], phys['SK_LIM']
    return (dict(out=-l1['lo'][0], inn=l1['hi'][0], side=l1['hi'][1]), dict(out=-l['lo'][0], inn=l['hi'][0], side=l['hi'][1]))


def curl(Gw, ch, cx, cy, l1, l, k=1.0):
    """every chain folds IN to k x its joint limit (the swing-back rebound after a stop, at its worst)"""
    return F.flare(Gw, ch, cx, cy, -k * l1['inn'], -k * l['inn'])


def main(d, g='m', path=None):
    Dz = W.DESIGNS[d]; p = Dz['prefix']; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    PEN.update(Dz[g].get('leg_pen', Dz.get('leg_pen', {})))     # v6: the design's leg catch depths (default 3 / 3 / 1.5)
    path = path or rep['outs'][0]
    outer = next(n for n, s_, sel, r in Dz[g]['pieces'] if r == 'skirt:outer')
    n, T = load(path); C.to_world(T); S = {t.name: t for t in T}; Gw = F.bone_world(T)
    for nm, nd in n.nodes.items():
        if nm not in Gw and nm.startswith(p + ' '):
            M_ = np.eye(4); M_[:3, 3] = nd.global_transform.translation; Gw[nm] = M_
    s2b = {}
    for t in T: s2b.update(t.s2b)
    c0 = S[outer].pos; cx, cy = c0[:, 0].mean(), c0[:, 1].mean(); ch = F.chains(Gw, p)
    l1, l = lims(Dz['phys'])
    F.LIM1.update(l1); F.LIM.update(l)
    # SoS Officer v2: every skirt layer's chains posed (each clamped to its own limits), every layer's lining checked
    LW = [w_ for w_, _ in LY.layers(d, g)]
    poses = [('at rest', lambda: {}),
             ('curled in (limit)', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'curl', 1.0)),
             ('swung back .3/.15', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'swing', [-1, 0, 0], 0.30, 0.15)),
             ('swung forward .3/.15', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'swing', [1, 0, 0], 0.30, 0.15)),
             ('swung sideways .3/.15', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'swing', [0, 1, 0], 0.30, 0.15))]
    per = {w_: np.zeros(3, int) for w_ in LW}
    strides = [('sprint R', (50.0, 25.0)), ('sprint L', (-20.0, -60.0)), ('walk R', (28.0, 14.0)), ('walk L', (-14.0, -28.0))]
    print(f'== {d} {g}: {path.split("/")[-1]}  limits first joint {l1}, lower {l}')
    tot = np.zeros(3, int)
    for pl, pf in poses:
        Ds = pf()
        row = []
        for sl, (a, b) in strides:
            Dm = dict(K.stride(T, a, b)); Dm.update(Ds)
            c_ = h_ = s_ = 0
            for word, side in [(w_, s_) for w_ in LW for s_ in ('Front', 'Back', 'Side')]:
                if f'{p} {word} {side}' not in S: continue
                sk = S[f'{p} {word} {side}']; q = F.skin(sk.pos, sk.w, Dm)
                ang = np.degrees(np.arctan2(sk.pos[:, 0] - cx, sk.pos[:, 1] - cy))
                reg = np.where(np.abs(wrap(ang)) < 55, 1, np.where(np.abs(wrap(ang - 180)) < 55, -1, 0))
                c = S[f'{p} Legs {side}']; cq = F.skin(c.pos, c.w, Dm); tt = c.tris
                if C.outward_fraction(c.pos, tt, W.leg_axes(type('P', (), {'s2b': {}})(), {'s2b_all': s2b})) < 0.5: tt = tt[:, [0, 2, 1]]
                fn = K.faces(cq, tt); tri, bary, dist, cp = C.Surface([('s', cq, tt)]).query(q, k=8); sd = ((q - cp) * fn[tri]).sum(1)
                hit = (sd < 0) & (sd >= -PEN[side])
                wrong = hit & (((reg == 1) & (fn[tri][:, 1] < -0.1)) | ((reg == -1) & (fn[tri][:, 1] > 0.1))) & (fn[tri][:, 2] < 0.7)
                c_ += int(hit.sum()); h_ += int(wrong.sum()); s_ += int((sd < -PEN[side]).sum())
                per[word] += [int(hit.sum()), int(wrong.sum()), int((sd < -PEN[side]).sum())]
            row.append(f'{sl} {c_:3d}/{h_:2d}/{s_:3d}'); tot += [c_, h_, s_]
        print(f'   {pl:22s} ' + '   '.join(row))
    if len(LW) > 1: print('   per layer caught/hooked/sunk: ' + ', '.join(f'{w_} {a}/{b}/{c}' for w_, (a, b, c) in per.items()))
    print(f'   total caught/hooked/sunk {tot[0]}/{tot[1]}/{tot[2]}; lining pts ' +
          ', '.join(f'{x} {len(S[f"{p} Skirt {x}"].pos)}' for x in ('Front', 'Back', 'Side')) +
          ''.join(f'; {w_} ' + ', '.join(f'{x} {len(S[f"{p} {w_} {x}"].pos)}' for x in ('Front', 'Back', 'Side') if f'{p} {w_} {x}' in S) for w_ in LW[1:]))


if __name__ == '__main__':
    W.use_designs(sys.argv[1]); main(*sys.argv[2:5])
