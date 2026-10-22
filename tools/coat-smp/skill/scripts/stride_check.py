"""Stuck-on-the-legs check: the legs stride (sprint / walk, each side) while the skirt chains are held in five states -
at rest, curled IN to the joint limit (the rebound after a stop), swung back / forward / sideways (clamped to the
design's own XML limits). For every skirt lining point (the per-vertex colliders '<prefix> Skirt Front/Side/Back')
against its matching one-sided leg piece:
  caught = inside the leg collider within its catch depth (penetration): pushed back out - fine,
  hooked = caught but pushed the WRONG way (front panel pushed backwards / back panel forwards) = stuck behind the leg,
  sunk   = deeper than the catch depth: the collider lets go and the point sits inside the leg until the leg moves away.
Use it to COMPARE versions (and against the armour author's own rig): hooked is what reads in game as 'stuck on the
legs'. Reference: a mail skirt the user confirmed 'perfect' in game scored 1002 caught / 15 hooked / 666 sunk summed
over all 20 rows; the version before it, which stuck, hooked 44 in the sprint-at-rest row alone. Sunk is normal in the
extreme rows (the collider simply lets go and the leg passes through).
It poses bones by hand - it cannot see inertia or lag (see references/testing.md).

usage:  python stride_check.py <design.py> [target] [mesh.nif]"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_skirt_rig as W
from smpkit import checks as K
C = W.C
wrap = C.wrap
PEN = {'Front': 3.0, 'Back': 3.0, 'Side': 1.5}      # = the leg pieces' <penetration> in the XML builder


def lims(phys):
    l1, l = phys['SK_LIM1'], phys['SK_LIM']
    return (dict(out=-l1['lo'][0], inn=l1['hi'][0], side=l1['hi'][1]), dict(out=-l['lo'][0], inn=l['hi'][0], side=l['hi'][1]))


def main(d, g=None, path=None):
    Dz = W.DESIGNS[d]; g = g or next(iter(Dz['targets'])); p = Dz['prefix']
    rep = json.load(open(W.WORK + f'{d}_report.json'))[g]
    path = path or rep['outs'][0]
    outer = next(n for n, s_, sel, r in Dz[g]['pieces'] if r == 'skirt:outer')
    n, T = C.load(path); C.to_world(T); S = {t.name: t for t in T}; Gw = K.bone_world(T)
    for nm, nd in n.nodes.items():
        if nm not in Gw and nm.startswith(p + ' '):
            M_ = np.eye(4); M_[:3, 3] = nd.global_transform.translation; Gw[nm] = M_
    s2b = {}
    for t in T: s2b.update(t.s2b)
    c0 = S[outer].pos; cx, cy = c0[:, 0].mean(), c0[:, 1].mean(); ch = K.chains(Gw, p, W.NROW)
    l1, l = lims(Dz.get('phys') or dict(SK_LIM1=W.SK_LIM1, SK_LIM=W.SK_LIM))
    K.LIM1.update(l1); K.LIM.update(l)
    poses = [('at rest', lambda: {}),
             ('curled in (limit)', lambda: K.flare(Gw, ch, cx, cy, -l1['inn'], -l['inn'])),
             ('swung back .3/.15', lambda: K.swing(Gw, ch, cx, cy, [-1, 0, 0], 0.30, 0.15)),
             ('swung forward .3/.15', lambda: K.swing(Gw, ch, cx, cy, [1, 0, 0], 0.30, 0.15)),
             ('swung sideways .3/.15', lambda: K.swing(Gw, ch, cx, cy, [0, 1, 0], 0.30, 0.15))]
    # thigh swing in degrees (forward, back): a sprint and a walk, leading with each leg
    strides = [('sprint R', (50.0, 25.0)), ('sprint L', (-20.0, -60.0)), ('walk R', (28.0, 14.0)), ('walk L', (-14.0, -28.0))]
    print(f'== {d} {g}: {os.path.basename(path)}  limits first joint {l1}, lower {l}')
    print('   pose                    per stride: caught/hooked/sunk')
    tot = np.zeros(3, int)
    for pl, pf in poses:
        Ds = pf()
        row = []
        for sl, (a, b) in strides:
            Dm = dict(K.stride(T, a, b)); Dm.update(Ds)
            c_ = h_ = s_ = 0
            for lreg in ('Front', 'Back', 'Side', 'Side L', 'Side R'):     # lining_lr designs: side lining in two shapes
                if f'{p} Skirt {lreg}' not in S: continue
                side = lreg.split()[0]
                sk = S[f'{p} Skirt {lreg}']; q = K.skin(sk.pos, sk.w, Dm)
                ang = np.degrees(np.arctan2(sk.pos[:, 0] - cx, sk.pos[:, 1] - cy))
                reg = np.where(np.abs(wrap(ang)) < 55, 1, np.where(np.abs(wrap(ang - 180)) < 55, -1, 0))
                c = S[f'{p} Legs {side}']; cq = K.skin(c.pos, c.w, Dm); tt = c.tris
                if C.outward_fraction(c.pos, tt, W.leg_axes(type('P', (), {'s2b': {}})(), {'s2b_all': s2b})) < 0.5: tt = tt[:, [0, 2, 1]]
                fn = K.faces(cq, tt); tri, bary, dist, cp = C.Surface([('s', cq, tt)]).query(q, k=8); sd = ((q - cp) * fn[tri]).sum(1)
                hit = (sd < 0) & (sd >= -PEN[side])
                wrong = hit & (((reg == 1) & (fn[tri][:, 1] < -0.1)) | ((reg == -1) & (fn[tri][:, 1] > 0.1))) & (fn[tri][:, 2] < 0.7)
                c_ += int(hit.sum()); h_ += int(wrong.sum()); s_ += int((sd < -PEN[side]).sum())
            row.append(f'{sl} {c_:3d}/{h_:2d}/{s_:3d}'); tot += [c_, h_, s_]
        print(f'   {pl:22s} ' + '   '.join(row))
    print(f'   total caught/hooked/sunk {tot[0]}/{tot[1]}/{tot[2]}; lining pts ' +
          ', '.join(f'{x} {len(S[f"{p} Skirt {x}"].pos)}' for x in ('Front', 'Back', 'Side', 'Side L', 'Side R') if f'{p} Skirt {x}' in S))
    return tot


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    d = W.use_design(sys.argv[1])
    main(d['name'], *sys.argv[2:4])
