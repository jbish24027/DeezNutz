"""lining_check: a skirt sheet with a lining behind it (the SoS Officer's embroidered hem band and its author's lining) - do
the two move as one? Three synthetic poses skinned with the WRITTEN weights: (A) alternate chains swing out / in 12 deg about
their top, (B) every chain flares out 15 deg, (C) the left thigh (with its calf and foot) raised 35 deg. For every lining point
that projects onto the sheet (within 1.0 lateral) the signed height over the sheet's outer face is measured after each pose;
'through' = in front of the face by more than 0.1 (what shows as the lining through the band, or the band through the lining
from inside). A lining weighed from the same bones as its sheet cannot come through in any pose.
usage: lining_check.py <designs.py> <design> [m|f]      (rebuild_coat.py runs it; SUMMARY line = worst pose)"""
import os, sys, json, re, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE.rstrip('/')))
import smpkit
C = smpkit.init()
import build_coat_rig as W

THRESH = 0.1


def rot(axis, deg):
    a = np.asarray(axis, float); a = a / (np.linalg.norm(a) + 1e-12); c, s = np.cos(np.radians(deg)), np.sin(np.radians(deg))
    x, y, z = a
    return np.array([[c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
                     [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
                     [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)]])


def main(d, g='m'):
    Dz = W.DESIGNS[d]; cfg = Dz[g]; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    n, T = C.load(rep['outs'][0]); C.to_world(T); S = {t.name: t for t in T}
    sheet = next((nm for nm, src, sel, role in cfg['pieces'] if role == 'skirt:outer'), None)
    if sheet is None or sheet not in S:
        print(f'{d} {g}: no outer sheet piece\nSUMMARY lining through/deepest worst: 0/0.00'); return 0
    cx, cy = rep['centre']; p = S[sheet]; P, TT, Wt = p.pos, p.tris, p.w
    om = W.G.outer_mask(P, TT, cx, cy); ot = TT[om]
    if not om.any() or om.all():
        print(f'{d} {g}: {sheet} has no lining (all triangles face out)\nSUMMARY lining through/deepest worst: 0/0.00'); return 0
    sheet_v = np.unique(ot); inner_v = np.setdiff1d(np.unique(TT[~om]), sheet_v)
    if not len(inner_v):
        print(f'{d} {g}: {sheet} has no lining points\nSUMMARY lining through/deepest worst: 0/0.00'); return 0
    ang = lambda X: np.degrees(np.arctan2(X[:, 0] - cx, X[:, 1] - cy))

    def height(Q, Ps):
        fnp = np.cross(Ps[ot[:, 1]] - Ps[ot[:, 0]], Ps[ot[:, 2]] - Ps[ot[:, 0]]); fnp = fnp / (np.linalg.norm(fnp, axis=1, keepdims=True) + 1e-12)
        tri, _, dd, cp = W.B.Surface([('o', Ps, ot)]).query(Q, k=8)
        h = ((Q - cp) * fnp[tri]).sum(1); return h, np.sqrt(np.maximum(dd ** 2 - h ** 2, 0.0))

    s2b = dict(getattr(p, 's2b', {})); org = {b: np.linalg.inv(W.B.tb2m(x))[:3, 3] for b, x in s2b.items()}
    bones = sorted(set(b for w in Wt for b in w)); pre = Dz['prefix']
    chain_re = re.compile(re.escape(pre) + r' (\w+?)(\d\d) (\d+)$')
    groups = {}
    for b in bones:
        mm = chain_re.match(b)
        if mm: groups.setdefault(mm.group(1) + mm.group(2), []).append((int(mm.group(3)), b))
    main_word = next((nm for nm, src, sel, role in cfg['pieces'] if role == 'skirt:outer'), None)
    chains = sorted(k for k in groups if k.startswith('Skirt'))      # the main skirt's chains (the sheet's own)
    if not chains: chains = sorted(groups)

    def skin(Tb):
        out = np.zeros_like(P)
        for i in range(len(P)):
            acc = np.zeros(3)
            for b, x in Wt[i].items():
                if b in Tb: R, o = Tb[b]; acc += x * (R @ (P[i] - o) + o)
                else: acc += x * P[i]
            out[i] = acc
        return out

    def chain_pose(f_deg):
        Tb = {}
        for n_, k in enumerate(chains):
            o = org.get(min(groups[k])[1])
            if o is None: continue
            th = np.arctan2(o[0] - cx, o[1] - cy); tang = np.array([np.cos(th), -np.sin(th), 0.0]); R = rot(tang, f_deg(n_))
            for r_, b in groups[k]: Tb[b] = (R, o)
        return Tb
    poses = {'A alternate chains +-12': chain_pose(lambda n_: 12.0 if n_ % 2 == 0 else -12.0),
             'B every chain out 15': chain_pose(lambda n_: 15.0)}
    lt = 'NPC L Thigh [LThg]'
    if lt in org:
        R = rot([1.0, 0.0, 0.0], -35.0)
        poses['C left thigh raised 35'] = {b: (R, org[lt]) for b in bones if b in ('NPC L Thigh [LThg]', 'NPC L Calf [LClf]', 'NPC L Foot [Lft ]')}
    h0, lat0 = height(P[inner_v], P); on0 = lat0 < 1.0
    print(f'{d} {g}: {sheet} {len(P)} pts, sheet {len(sheet_v)}, lining {len(inner_v)} ({int(on0.sum())} project onto the sheet); at rest the lining sits '
          f'{-np.median(h0[on0]):.2f} behind it (median), nearest {-h0[on0].max():+.2f}; {len(chains)} chains')
    worst_n, worst_h = 0, 0.0
    for name, Tb in poses.items():
        Pp = skin(Tb); h, lat = height(Pp[inner_v], Pp); on = lat < 1.0; thr = on & (h > THRESH)
        n_ = int(thr.sum()); hmax = float(h[on].max()) if on.any() else 0.0
        print(f'   {name}: {int(on.sum())} lining pts over the sheet, through by more than {THRESH}: {n_}, deepest {max(hmax, 0.0):.2f}')
        if n_:
            zz = P[inner_v][thr][:, 2]; aa = ang(P[inner_v][thr])
            print(f'      z {zz.min():.1f}..{zz.max():.1f}, angles ' + ', '.join(f'{a:.0f}' for a in sorted(set((np.round(aa / 15) * 15).tolist()))))
        worst_n = max(worst_n, n_); worst_h = max(worst_h, hmax)
    print(f'SUMMARY lining through/deepest worst: {worst_n}/{max(worst_h, 0.0):.2f}')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    W.use_designs(sys.argv[1]); sys.exit(main(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'm'))
