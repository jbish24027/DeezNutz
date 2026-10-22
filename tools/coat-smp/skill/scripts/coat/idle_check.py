# skill coat copy (from sos-smp-rework/) of idle_check.py (2026-10-11): checks build_sos designs; ported 2026-10-11.
"""Idle stance check: thighs abducted (knees out) by a few degrees, no stride. For the OUTER's points and the cloth's:
caught = inside its leg collider within the catch depth, sunk = deeper (the collider lets go). usage: idle_check.py <design> [m]"""
import sys, json
import numpy as np
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


def abduct(T, deg_r, deg_l, fwd=0.0):
    s2b = {}
    for t in T: s2b.update(t.s2b)
    Dm = {}
    hips = {side: np.linalg.inv(C.tb2m(s2b[K.LEG[side][0]]))[:3, 3] for side in ('R', 'L')}
    cx = (hips['R'][0] + hips['L'][0]) / 2
    for side, deg in (('R', deg_r), ('L', deg_l)):
        hip = hips[side]; sgn = 1.0 if hip[0] > cx else -1.0
        M = K.rot(np.array([0, 1.0, 0]), -sgn * np.radians(deg), hip)   # knee moves outward
        if fwd: M = K.rot(np.array([1.0, 0, 0]), np.radians(fwd), hip) @ M
        for b in K.LEG[side]: Dm[b] = M
        knee = np.array([hip[0], hip[1], hip[2] - 20.0, 1.0]); k2 = (M @ knee)[:3]
        if deg == deg_r and side == 'R': print(f'   (check: R knee 20 below the hip moves x {k2[0] - hip[0]:+.2f} for {deg} deg; hip x {hip[0]:+.1f} vs centre {cx:+.1f})')
    return Dm, s2b


def main(d, g='m'):
    Dz = W.DESIGNS[d]; p = Dz['prefix']; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    PEN.update(Dz[g].get('leg_pen', Dz.get('leg_pen', {})))     # v6: the design's leg catch depths (default 3 / 3 / 1.5)
    path = Dz['m']['out'].format('1') if g == 'm' else rep['outs'][0]
    n, T = load(path); C.to_world(T); S = {t.name: t for t in T}
    cx, cy = rep['centre']            # v5: from the report (no fixed piece name)
    print(f'== {d} {g}: {path.split("/")[-1]}  side pen {PEN["Side"]}, front/back {PEN["Front"]}')
    pc = W.DESIGNS[W.TWO_LAYER[d]]['prefix'] if d in W.TWO_LAYER else None
    for deg in (0, 4, 8, 12):
        for fwd in (0, 8):
            Dm, s2b = abduct(T, deg, deg, fwd)
            out = []
            ents = [('outer', p, 'Skirt'), ('cloth', pc, 'Skirt')] + [(w_, p, w_) for w_, _ in LY.layers(d, g)[1:]]   # SoS Officer v2: + the extra layers
            for lab, pref, word in ents:
                if pref is None: continue
                c_ = s_ = 0; deep = []
                for side in ('Front', 'Back', 'Side'):          # as SMP pairs them: the lining piece of one facing vs the leg piece of that facing
                    if f'{pref} {word} {side}' not in S: continue
                    sk = S[f'{pref} {word} {side}']; q = F.skin(sk.pos, sk.w, Dm)
                    c = S[f'{pref} Legs {side}']; cq = F.skin(c.pos, c.w, Dm); tt = c.tris
                    if C.outward_fraction(c.pos, tt, W.leg_axes(type('P', (), {'s2b': {}})(), {'s2b_all': s2b})) < 0.5: tt = tt[:, [0, 2, 1]]
                    fn = K.faces(cq, tt); tri, bary, dist, cp = C.Surface([('s', cq, tt)]).query(q, k=8); sd = ((q - cp) * fn[tri]).sum(1)
                    hit = (sd < 0) & (sd >= -PEN[side]); sunk = sd < -PEN[side]
                    c_ += int(hit.sum()); s_ += int(sunk.sum())
                    if sunk.any():
                        ang = np.degrees(np.arctan2(q[sunk, 0] - cx, q[sunk, 1] - cy)); deep.append(f'{side}: z {q[sunk, 2].min():.0f}-{q[sunk, 2].max():.0f} ang {ang.min():.0f}..{ang.max():.0f} depth {-sd[sunk].max():.1f}..{-sd[sunk].min():.1f}')
                out.append(f'{lab} caught/sunk {c_:3d}/{s_:3d}' + (f' [{"; ".join(deep)}]' if deep else ''))
            print(f'   knees out {deg:2d} deg, fwd {fwd:d}:  ' + '   '.join(out))


if __name__ == '__main__':
    W.use_designs(sys.argv[1]); main(*sys.argv[2:4])
