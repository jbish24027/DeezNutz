"""SoS Officer v2 - the colliders BETWEEN skirt layers (cfg 'layer_coll': the blue skirt's lining vs 'Mail Inside', the tasset
layer vs 'Mail Over'). For every pair, the points of the layer that meets the collider (its lining colliders) against the
collider, by triangle plane (inside = in front of it, its own side; past = behind it):
  legs only  - idle / walk / run strides, both leads, every physics bone at rest: contacts here = the legs carry one layer into
               the other every step (a twitch)
  apart      - the two layers swung against each other, legs still: the point layer swung OUT (k x .3 / .12 rad) while the
               collider's layer swings IN / stays, and the reverse - behind the collider within its catch = pushed back (fine),
               past the catch = the layers pass through each other (a clip physics cannot undo)
  apart+run  - the same with a run stride
Offline: no lag / momentum. usage: layer_check.py <design> [m|f]"""
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



def prism(q, P, TT):
    """per point: the signed height over the triangle it projects into (+ = the triangle's front), nan = none within reach"""
    A_, B_, C_ = P[TT[:, 0]], P[TT[:, 1]], P[TT[:, 2]]
    n = np.cross(B_ - A_, C_ - A_); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    e0, e1 = B_ - A_, C_ - A_; d00 = (e0 * e0).sum(1); d01 = (e0 * e1).sum(1); d11 = (e1 * e1).sum(1); den = d00 * d11 - d01 ** 2 + 1e-12
    out = np.full(len(q), np.nan)
    for s_ in range(0, len(q), 128):
        v = q[s_:s_ + 128][:, None, :] - A_[None]
        sd = (v * n[None]).sum(2); d20 = (v * e0[None]).sum(2); d21 = (v * e1[None]).sum(2)
        b1 = (d11 * d20 - d01 * d21) / den; b2 = (d00 * d21 - d01 * d20) / den
        hit = (b1 >= -0.02) & (b2 >= -0.02) & (b1 + b2 <= 1.02) & (sd > -6.0) & (sd < 3.0)
        best = np.where(hit, np.abs(sd), np.inf).argmin(1); ok = hit[np.arange(len(best)), best]
        out[s_:s_ + 128][ok] = sd[np.arange(len(best)), best][ok]
    return out


def main(d, g='m'):
    Dz = W.DESIGNS[d]; cfg = Dz[g]; p = Dz['prefix']; rep = json.load(open(W.WORK + 'rework_report.json'))[d][g]
    n, T = load(rep['outs'][0]); C.to_world(T); S = {t.name: t for t in T}; Gw = F.bone_world(T)
    for nm, nd in n.nodes.items():
        if nm not in Gw and nm.startswith(p + ' '):
            M_ = np.eye(4); M_[:3, 3] = nd.global_transform.translation; Gw[nm] = M_
    cx, cy = rep['centre']; LYS = dict(LY.layers(d, g))
    surf_word = {nm: ('Skirt' if r == 'skirt:outer' else r.split('@')[1]) for nm, s_, sel, r in cfg['pieces'] if r.startswith('skirt')}

    def swing_layer(word, kind, *a):
        ch = LY.chains(Gw, p, word); l1, l = LY.lims(LYS[word]); F.LIM1.update(l1); F.LIM.update(l)
        if kind == 'flare': return F.flare(Gw, ch, cx, cy, *a)
        return F.swing(Gw, ch, cx, cy, *a)
    print(f'== {d} {g}: {rep["outs"][0].split("/")[-1]}  (touch < 0.2 = the two margins; catch = the collider\'s penetration)')
    summ = []
    for lc in cfg.get('layer_coll', ()):
        cn = f'{p} {lc["name"]}'
        if cn not in S: print(f'   {lc["name"]}: not in the mesh'); continue
        cc = S[cn]; pts = [S[f'{p} {lc["pts"]} {s}'] for s in ('Front', 'Side', 'Back') if f'{p} {lc["pts"]} {s}' in S]
        wo, wp = surf_word[lc['surf']], lc['pts']; pen = lc['pen']
        # 'in' (the mail's inside over the blue lining): the lining swinging OUT meets it; 'out' (the mail's outside under the
        # tassets): the tassets swinging IN, or the mail swinging OUT, meets it
        if lc['facing'] == 'in':
            apart = [('pts out .3/.12', {**swing_layer(wp, 'flare', 0.30, 0.12)}),
                     ('pts out, surf in', {**swing_layer(wp, 'flare', 0.30, 0.12), **swing_layer(wo, 'flare', -0.05, -0.05)}),
                     ('pts fwd, surf back', {**swing_layer(wp, 'swing', [1, 0, 0], 0.30, 0.12), **swing_layer(wo, 'swing', [-1, 0, 0], 0.30, 0.12)}),
                     ('pts back, surf fwd', {**swing_layer(wp, 'swing', [-1, 0, 0], 0.30, 0.12), **swing_layer(wo, 'swing', [1, 0, 0], 0.30, 0.12)})]
        else:
            apart = [('surf out .3/.12', {**swing_layer(wo, 'flare', 0.30, 0.12)}),
                     ('surf out, pts stay', {**swing_layer(wo, 'flare', 0.30, 0.12), **swing_layer(wp, 'flare', 0.0, 0.0)}),
                     ('surf fwd, pts back', {**swing_layer(wo, 'swing', [1, 0, 0], 0.30, 0.12), **swing_layer(wp, 'swing', [-1, 0, 0], 0.30, 0.12)}),
                     ('surf back, pts fwd', {**swing_layer(wo, 'swing', [-1, 0, 0], 0.30, 0.12), **swing_layer(wp, 'swing', [1, 0, 0], 0.30, 0.12)})]
        cases = [('rest', {})] + [(lab, K.stride(T, a, b)) for lab, a, b in (('idle', 10, 8), ('idle L', -8, -10), ('walk', 25, 15), ('walk L', -15, -25),
                                                                                   ('run', 45, 25), ('run L', -25, -45))]
        cases += apart + [(lab + ' +run', {**K.stride(T, 45, 25), **Dm}) for lab, Dm in apart[2:]]
        row, worst_con, worst_past, worst_none = [], 0, 0, 0
        zlo, zhi = float(cc.pos[:, 2].min()), float(cc.pos[:, 2].max())
        for lab, Dm in cases:
            cq = F.skin(cc.pos, cc.w, Dm); touch = caught = past = none = 0
            for sh in pts:
                q = F.skin(sh.pos, sh.w, Dm); sd = prism(q, cq, cc.tris); ok = np.isfinite(sd)
                touch += int((ok & (sd >= 0) & (sd < 0.2)).sum()); caught += int((ok & (sd < 0) & (sd >= -pen)).sum()); past += int((ok & (sd < -pen)).sum())
                # BLIND SPOT (Officer v2 lesson): a point with NO collider triangle under it is never counted by the three numbers above -
                # a hole cut in the collider silenced this check exactly where it failed in game. Count them (within the collider's height band).
                none += int((~ok & (q[:, 2] >= zlo - 0.5) & (q[:, 2] <= zhi + 0.5)).sum())
            row.append(f'{lab} {touch}/{caught}/{past}' + (f' none{none}' if none else ''))
            if lab in ('rest', 'idle', 'idle L', 'walk', 'walk L', 'run', 'run L'): worst_con = max(worst_con, touch + caught + past)
            worst_past = max(worst_past, past); worst_none = max(worst_none, none)
        print(f'   {lc["name"]} ({lc["pts"]} lining {sum(len(x.pos) for x in pts)} pts vs {len(cc.tris)} tris, catch {pen}): touch/caught/past [none = no collider under the point]  ' + '  '.join(row))
        summ.append(f'{lc["name"]} {worst_con}/{worst_past}' + (f' (none-under {worst_none})' if worst_none else ''))
    print(f'{d} {g} SUMMARY layer legs-only contacts/past-catch worst: ' + ', '.join(summ))


if __name__ == '__main__':
    W.use_designs(sys.argv[1]); main(*sys.argv[2:4])
