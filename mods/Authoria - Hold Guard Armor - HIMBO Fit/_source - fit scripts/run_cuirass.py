"""Fit the guard cuirass to HIMBO and write all 9 hold files (_0/_1).

Every distinct shape geometry is fitted ONCE and the fitted geometry + weights are copied into every hold
file that carries that shape (the holds share their geometry and differ only in textures; at _0 the mod
ships two geometry families, so two masters). For each output weight both source variants are tried
and the one with the lower interior poke-through on HIMBO is kept."""
import os, sys, json, shutil
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif
from worldpos import world_skel
from fitnif import fit_shape, write_back, visible_union, validate, shape_key, NOFIT
from fitlib import edge_strain, poke_design, pairs
from scipy_free_kd import nearest

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(JOB), 'guardarmor', 'extract', 'smppatch', 'HDT-SMP Hold Guard Armor Patch', 'Meshes', '1GuardArmor', 'M')
OUT = os.path.join(JOB, 'out', 'meshes', '1GuardArmor', 'M')
TMP = os.path.join(JOB, 'tmp')
HOLDS = ['White', 'Dawn', 'Folk', 'Mark', 'Mort', 'Rift', 'Sol', 'Wind', 'Winter']
os.makedirs(OUT, exist_ok=True)


def build(ws, wt):
    td = os.path.join(TMP, 'cuirass_%s_from%s' % (wt, ws)); os.makedirs(td, exist_ok=True)
    master, stats, copies = {}, {}, {}
    holds = {}
    for h in HOLDS:
        g = GNif(os.path.join(SRC, 'Cuirass%sM_%s.nif' % (h, ws)))
        before, after = {}, {}
        for s in g.shapes:
            Pw = world_skel(g, s)[0]
            before[s.name] = Pw
            if s.name in NOFIT:
                after[s.name] = Pw
                continue
            assert s.dsize == 0
            key = shape_key(g, s)
            if key not in master:
                res = fit_shape(g, s, ws, wt=wt)
                master[key] = res
                r = edge_strain(res['Pw0'], res['Pw1'], s.tris.astype(np.int64))
                dn = np.linalg.norm(res['disp'], axis=1)
                stats[key] = dict(fitted_in=h, verts=len(dn), disp_mean=round(float(dn.mean()), 3), disp_max=round(float(dn.max()), 3),
                                  strain_min=round(float(r.min()), 3), strain_max=round(float(r.max()), 3),
                                  weights_blended=res['wchanged'], collision_pushed=res['pushed'], rigid_verts=res['rigid'])
            copies.setdefault(key, []).append(h)
            res = master[key]
            write_back(g, s, res)
            after[s.name] = res['Pw1']
        out = os.path.join(td, 'Cuirass%sM_%s.nif' % (h, wt))
        g.save(out)
        g2 = GNif(out)
        A0, T0 = visible_union(g2, before); A1, T1 = visible_union(g2, after)
        pd, _ = poke_design(ws, A0, T0, A1, T1, wt=wt)
        pr = pairs()
        VP = pr['V'][ws][0]; HP = pr['H'][wt][0]
        dv, _ = nearest(A0, VP); dh0, _ = nearest(A0, HP); dh1, _ = nearest(A1, HP)
        near = dv < 4
        e0 = np.abs(dh0 - dv)[near]; e1 = np.abs(dh1 - dv)[near]
        holds[h] = dict(poke=pd, offset_err_before=(round(float(e0.mean()), 3), round(float(np.percentile(e0, 95)), 3)),
                        offset_err_after=(round(float(e1.mean()), 3), round(float(np.percentile(e1, 95)), 3)),
                        skin=validate(g2))
        print('out _%s from _%s %-6s poke %s offset %s -> %s' % (wt, ws, h, {k: float(v) for k, v in pd.items()}, holds[h]['offset_err_before'], holds[h]['offset_err_after']), flush=True)
    return td, dict(source='_' + ws, unique_fits=len(master), shape_stats=stats, copies=copies, holds=holds)


report = {}
for wt in '01':
    cands = [build(ws, wt) for ws in ('0', '1')]
    score = lambda c: np.mean([v['poke']['after_pct'] for v in c[1]['holds'].values()])
    # natural pairing (source weight == output weight) unless the other source is materially better (>1 point)
    nat = [c for c in cands if c[1]['source'] == '_' + wt][0]
    alt = [c for c in cands if c is not nat][0]
    best = alt if score(alt) < score(nat) - 1.0 else nat
    for h in HOLDS:
        shutil.copyfile(os.path.join(best[0], 'Cuirass%sM_%s.nif' % (h, wt)), os.path.join(OUT, 'Cuirass%sM_%s.nif' % (h, wt)))
    best[1]['alternatives'] = {c[1]['source']: round(float(score(c)), 2) for c in cands}
    report[wt] = best[1]
    print('== out _%s chosen source %s  (mean interior poke %s)' % (wt, best[1]['source'], best[1]['alternatives']), flush=True)
json.dump(report, open(os.path.join(JOB, 'report_cuirass.json'), 'w'), indent=1, default=float)
