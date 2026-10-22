# skill coat copy (from sos-smp-rework/) of flap_jump.py (2026-10-11): checks build_sos designs; ported 2026-10-11.
"""Flap (hip plate / tasset) points vs the trousers in the jump_check poses. In the XML the flap points may meet ALL three
leg pieces (front / side / back), unlike the skirt lining (each part only its matching one-sided piece). Counts per piece:
pushed (inside within the piece's catch) and wrong-way (front-region point pushed backward, back-region pushed forward).
usage: flap_jump.py <design> [m|f|v]"""
import sys, json, numpy as np
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
import build_coat_rig as W, coat_lib as F
load, wrap, rot, prism_rest = C.load, C.wrap, K.rot, F.prism_rest
import jump_check as J, swing_stride as SS



def main(d, g='m', shape='Flap Points'):
    Dz = W.DESIGNS[d]; p = Dz['prefix']; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    path = rep['outs'][0]
    outer = next(n for n, s_, sel, r in Dz[g]['pieces'] if r == 'skirt:outer')
    n, T = load(path); C.to_world(T); S = {t.name: t for t in T}; Gw = F.bone_world(T)
    for nm, nd in n.nodes.items():
        if nm not in Gw and nm.startswith(p + ' '):
            M_ = np.eye(4); M_[:3, 3] = nd.global_transform.translation; Gw[nm] = M_
    s2b = {}
    for t in T: s2b.update(t.s2b)
    c0 = S[outer].pos; cx, cy = c0[:, 0].mean(), c0[:, 1].mean(); ch = F.chains(Gw, p)
    l1, l = SS.lims(Dz['phys']); F.LIM1.update(l1); F.LIM.update(l)
    fl = S[f'{p} {shape}']
    ang = np.degrees(np.arctan2(fl.pos[:, 0] - cx, fl.pos[:, 1] - cy))
    reg = np.where(np.abs(wrap(ang)) < 55, 1, np.where(np.abs(wrap(ang - 180)) < 55, -1, 0))
    print(f'== {d} {g} {shape}: {len(fl.pos)} pts, z {fl.pos[:, 2].min():.1f}..{fl.pos[:, 2].max():.1f}, front {int((reg == 1).sum())} side {int((reg == 0).sum())} back {int((reg == -1).sum())}')
    poses = [('at rest', lambda: {}), ('curled in', lambda: SS.curl(Gw, ch, cx, cy, l1, l)),
             ('swung back', lambda: F.swing(Gw, ch, cx, cy, [-1, 0, 0], 0.30, 0.15)), ('swung forward', lambda: F.swing(Gw, ch, cx, cy, [1, 0, 0], 0.30, 0.15))]
    jumps = [('stand', None), ('jump R lead', (70.0, 40.0, 80.0, 60.0)), ('jump L lead', (40.0, 70.0, 60.0, 80.0)), ('tuck', (60.0, 60.0, 90.0, 90.0))]
    tot = {}
    for pl, pf in poses:
        Ds = pf(); row = []
        for jl, args in jumps:
            Dm = dict(J.jump(T, *args)) if args else {}; Dm.update(Ds)
            q = F.skin(fl.pos, fl.w, Dm); cell = []
            for side in ('Front', 'Side', 'Back'):
                c = S[f'{p} Legs {side}']; cq = F.skin(c.pos, c.w, Dm); tt = c.tris
                if C.outward_fraction(c.pos, tt, W.leg_axes(type('P', (), {'s2b': {}})(), {'s2b_all': s2b})) < 0.5: tt = tt[:, [0, 2, 1]]
                fn = K.faces(cq, tt); tri, bary, dist, cp = C.Surface([('s', cq, tt)]).query(q, k=8); sd = ((q - cp) * fn[tri]).sum(1)
                lat = np.sqrt(np.maximum(dist ** 2 - sd ** 2, 0))
                hit = (sd < 0.25) & (sd >= -J.PEN[side]) & (lat < 0.3)   # margin .15 + .1; inside the triangle's prism (not off an edge)
                wrong = hit & (((reg == 1) & (fn[tri][:, 1] < -0.1)) | ((reg == -1) & (fn[tri][:, 1] > 0.1)))
                cell.append(f'{side[0]} {int(hit.sum()):3d}/{int(wrong.sum()):3d}')
                k = (jl, side); a = tot.get(k, np.zeros(2, int)); tot[k] = a + [int(hit.sum()), int(wrong.sum())]
            row.append(f'{jl}: ' + ' '.join(cell))
        print(f'   {pl:13s} ' + ' | '.join(row))
    print('   pushed/wrong-way by leg piece (F front, S side, B back)')


if __name__ == '__main__':
    W.use_designs(sys.argv[1]); main(*sys.argv[2:5])
