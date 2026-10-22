# skill coat copy (from sos-smp-rework/) of jump_check.py (2026-10-11): checks build_sos designs; ported 2026-10-11.
"""Jump check: both thighs raised (one leading), knees bent (shins back), with the skirt at rest / curled in / swung back /
swung forward. For every skirt lining point (Skirt Front/Side/Back) against its one-sided leg piece: caught (pushed back
out), hooked (pushed the wrong way), sunk (past the catch: sits inside the leg until it moves away). Offline = no lag.
usage: jump_check.py <design> [m|f]"""
import sys, json, numpy as np
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
from smpkit import checks as K
import build_coat_rig as W, coat_lib as F
load, wrap, rot, prism_rest = C.load, C.wrap, K.rot, F.prism_rest
import coat_layers as LY, swing_stride as SS


PEN = {'Front': 3.0, 'Back': 3.0, 'Side': 1.5}


def jump(T, right, left, knee_r, knee_l):
    """thighs forward by right / left degrees about the hip, then the calf + foot bent back about the knee"""
    s2b = {}
    for t in T: s2b.update(t.s2b)
    Dm = {}
    for side, ang, kn in (('R', right, knee_r), ('L', left, knee_l)):
        th, ca, ft, to = K.LEG[side]
        hip = np.linalg.inv(C.tb2m(s2b[th]))[:3, 3]
        M1 = rot(np.array([1.0, 0, 0]), np.radians(ang), hip)
        for b in K.LEG[side]: Dm[b] = M1
        if ca in s2b:
            knee = (M1 @ np.r_[np.linalg.inv(C.tb2m(s2b[ca]))[:3, 3], 1])[:3]
            M2 = rot(np.array([1.0, 0, 0]), np.radians(-kn), knee) @ M1
            for b in (ca, ft, to): Dm[b] = M2
    return Dm


def main(d, g='m'):
    Dz = W.DESIGNS[d]; p = Dz['prefix']; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    PEN.update(Dz[g].get('leg_pen', Dz.get('leg_pen', {})))     # v6: the design's leg catch depths (default 3 / 3 / 1.5)
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
    LW = [w_ for w_, _ in LY.layers(d, g)]        # SoS Officer v2: every skirt layer posed and checked
    poses = [('at rest', lambda: {}), ('curled in', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'curl', 1.0)),
             ('swung back', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'swing', [-1, 0, 0], 0.30, 0.15)),
             ('swung forward', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'swing', [1, 0, 0], 0.30, 0.15))]
    per = {w_: np.zeros(3, int) for w_ in LW}
    jumps = [('jump R lead', (70.0, 40.0, 80.0, 60.0)), ('jump L lead', (40.0, 70.0, 60.0, 80.0)), ('tuck', (60.0, 60.0, 90.0, 90.0))]
    print(f'== {d} {g}: {path.split("/")[-1]}')
    tot = np.zeros(3, int)
    for pl, pf in poses:
        Ds = pf(); row = []
        for jl, args in jumps:
            Dm = dict(jump(T, *args)); Dm.update(Ds)
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
            row.append(f'{jl} {c_:3d}/{h_:2d}/{s_:3d}'); tot += [c_, h_, s_]
        print(f'   {pl:14s} ' + '   '.join(row))
    if len(LW) > 1: print('   per layer caught/hooked/sunk: ' + ', '.join(f'{w_} {a}/{b}/{c}' for w_, (a, b, c) in per.items()))
    print(f'   total caught/hooked/sunk {tot[0]}/{tot[1]}/{tot[2]}')


if __name__ == '__main__':
    W.use_designs(sys.argv[1]); main(*sys.argv[2:4])
