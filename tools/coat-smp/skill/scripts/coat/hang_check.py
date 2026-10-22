"""Hanging pieces vs the mail / skirt under them - the user's 'never clip through the chainmail' check, for every hanging piece
the design has: belt tail (own chain 'BeltTip'), sash end ('Sash'), the left-hip strap ('Flap'), the bag ('Bag'), the hip hangers ('Hang': rings + straps, v11).
Worst-case lag: the piece's OWN bones stay at rest while
  (a) legs only (idle / walk / run strides, both leads; every physics bone at rest): the leg-driven part of the skirt under the
      piece moves into it - points of its collision layer that touch their collider here = a piece pressed every step = twitch
  (b) the skirt swings (its chains forward / back / flared out within ~0.3 + 0.12 rad, legs still)
Reported per case: visible points of the piece that end up INSIDE the visible skirt (> 0.2 past its outer surface) and of those how
many are deeper than the piece's collider can catch (its copy of the skirt + the catch depth) = a clip physics cannot undo.
Offline: no lag / momentum - the real swing is smaller than these worst cases and the colliders act on top.
usage: hang_check.py <design> [m|f]"""
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


PEN = {"Skirt Outer": W.SKO_PEN}     # catch depth per collider (the under-copies: W.TAILU_PEN)


def main(d, g='m'):
    Dz = W.DESIGNS[d]; p = Dz['prefix']; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    n, T = load(rep['outs'][0]); C.to_world(T); S = {t.name: t for t in T}; Gw = F.bone_world(T)
    for nm, nd in n.nodes.items():
        if nm not in Gw and nm.startswith(p + ' '):
            M_ = np.eye(4); M_[:3, 3] = nd.global_transform.translation; Gw[nm] = M_
    ch = F.chains(Gw, p); cx, cy = rep['centre']

    def under_of(lab):
        """the visible layer(s) under a hanging piece (SoS Officer v2: Dz 'hang_under' - the strap hangs over the tasset layer and
        the mail; default the skirt 'Saia') as one surface: positions, weights, outward triangles"""
        nms = Dz.get('hang_under', {}).get(lab, ('Saia',)); o = 0; P_, W_, T_ = [], [], []
        for nm in nms:
            u = S[nm]; P_.append(u.pos); W_ += list(u.w); T_.append(u.tris[C.outer_mask(u.pos, u.tris, cx, cy)] + o); o += len(u.pos)
        return type('U', (), dict(pos=np.vstack(P_), w=W_))(), np.vstack(T_)
    # (label, visible shape, its own-bone prefix, collision points shape, collider shape)
    pieces = [('belt tail', 'Cinto', f'{p} BeltTip', f'{p} Tip Points', f'{p} Skirt Under Tip'),
              ('sash end', 'Sash', f'{p} Sash ', f'{p} Sash Points', f'{p} Skirt Under Sash'),
              ('welded belt tail', 'Tail', f'{p} Tail ', f'{p} Tail Points', f'{p} Skirt Under Tail'),
              ('hip strap', 'Correia', f'{p} Flap', f'{p} Flap Points', f'{p} Skirt Outer'),
              ('bag', 'Cinto', f'{p} Bag', f'{p} Bag Points', f'{p} Skirt Outer'),
              ('hip hangers', 'Cinto', f'{p} Hang', f'{p} Hang Points', f'{p} Skirt Under Hang')]     # v11: rings + straps on their own bones
    # 2026-10-13 (SoS Winterhold): every other 'tail' piece the design names (a bag 'Bolsa', a canteen 'Cantil' - rigid tails), under its own copy
    pieces += [(f'tail {nm.lower()}', nm, f'{p} {nm} ', f'{p} {nm} Points', f'{p} Skirt Under {nm}')
               for nm in [pc[0] for pc in Dz.get(g, {}).get('pieces', ()) if len(pc) > 3 and pc[3] == 'tail'] if nm not in ('Sash', 'Tail')]
    cases = [('idle', lambda: K.stride(T, 10, 8)), ('idle L', lambda: K.stride(T, -8, -10)),
             ('walk', lambda: K.stride(T, 25, 15)), ('walk L', lambda: K.stride(T, -15, -25)),
             ('run', lambda: K.stride(T, 45, 25)), ('run L', lambda: K.stride(T, -25, -45)),
             ('skirt fwd', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'swing', [1, 0, 0], 0.30, 0.12, keep_lims=not Dz[g].get('groups'))),      # every skirt layer
             ('skirt back', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'swing', [-1, 0, 0], 0.30, 0.12, keep_lims=not Dz[g].get('groups'))),
             ('skirt flare', lambda: LY.pose_all(F, Gw, p, d, g, cx, cy, 'flare', 0.30, 0.12, keep_lims=not Dz[g].get('groups')))]
    Dms = [(lab, f()) for lab, f in cases]
    tot = {}; fails = []
    for lab, vis, own, cpts, coll in pieces:
        if vis not in S or cpts not in S: continue
        v = S[vis]; sk, st = under_of(lab)
        share = np.array([sum(x for b, x in w.items() if b.startswith(own)) for w in v.w]); vv = np.where(share > 0.05)[0]
        if not len(vv): continue
        rest_sd = F.signed(v.pos[vv], sk.pos, st)
        row, worst = [], (0, 0)
        for cl, Dm in Dms:
            q = F.skin(v.pos[vv], [v.w[i] for i in vv], Dm); sq = F.skin(sk.pos, sk.w, Dm)
            sd = F.signed(q, sq, st)
            inside = (sd < -0.2) & (rest_sd >= -0.05)
            cc = S[coll]; cq = F.skin(cc.pos, cc.w, Dm)
            past = np.zeros(len(q), bool)
            if inside.any():                         # deeper than its collider can catch: below the copy by more than the catch
                tri, bary, dist, cp_ = C.Surface([('c', cq, cc.tris)]).query(q[inside], k=8)
                fn = np.cross(cq[cc.tris[:, 1]] - cq[cc.tris[:, 0]], cq[cc.tris[:, 2]] - cq[cc.tris[:, 0]]); fn /= np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12
                pen_ = Dz.get('sko_pen', W.SKO_PEN) if coll.endswith('Skirt Outer') else W.TAILU_PEN
                sdc = ((q[inside] - cp_) * fn[tri]).sum(1); past[np.where(inside)[0]] = sdc < -pen_
            # legs-only contacts of the collision layer with its collider (the twitch test, RA tail_idle)
            con = 0
            if not cl.startswith('skirt'):
                pc = S[cpts]; pq = F.skin(pc.pos, pc.w, Dm)
                con = int((C.Surface([('c', cq, cc.tris)]).query(pq, k=8)[2] < 0.2).sum())
            row.append(f'{cl} {int(inside.sum())}/{int(past.sum())}' + (f' c{con}' if con else ''))
            if con and cl in ('idle', 'idle L', 'walk', 'walk L'): fails.append(f'  FAIL {d} {g} {lab}: pressed onto its collider by the skirt under it in the {cl} stance ({con} contacts) - a twitch standing still / walking (v12: the copies are pulled in for these stances)')
            worst = (max(worst[0], int(inside.sum())), max(worst[1], int(past.sum())))
        tot[lab] = worst
        print(f'{d} {g} {lab:9s} ({len(vv)} pts): ' + '  '.join(row))
    for f_ in fails: print(f_)
    print(f'{d} {g} SUMMARY inside/past-collider worst: ' + ', '.join(f'{k} {a}/{b}' for k, (a, b) in tot.items()) + (f'; PRESSED in a stance: {len(fails)}' if fails else ''))


if __name__ == '__main__':
    W.use_designs(sys.argv[1]); main(*sys.argv[2:4])
