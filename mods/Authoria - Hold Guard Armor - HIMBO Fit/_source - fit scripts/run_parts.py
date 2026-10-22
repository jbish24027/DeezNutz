"""Fit boots, gauntlets and the first-person sleeves (male) to HIMBO _0 and _1.
For each output weight both source variants (_0, _1) are fitted and the one with the lower interior
poke-through on the HIMBO body is kept (the mod's _1 boots/gauntlets/sleeves do not cover the vanilla _1
body they were meant for, so the _0 source can be the better start)."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif
from worldpos import world_skel
from fitnif import fit_shape, write_back, visible_union, validate
from fitlib import edge_strain, pairs, poke_design
from scipy_free_kd import nearest

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(JOB, 'conv', '1GuardArmor', 'M')
OUT = os.path.join(JOB, 'out', 'meshes', '1GuardArmor', 'M')
TMP = os.path.join(JOB, 'tmp'); os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
ITEMS = sys.argv[1:] or ['BootsM', 'GauntletsM', '1stPersonCuirassSleevesM']
report = {}


def run(item, ws, wt):
    src = os.path.join(SRC, '%s_%s.nif' % (item, ws))
    g = GNif(src)
    before, after, st = {}, {}, {}
    for s in g.shapes:
        if not s.bones:
            continue
        assert s.dsize == 0
        before[s.name] = world_skel(g, s)[0]
        res = fit_shape(g, s, ws, wt=wt)
        write_back(g, s, res)
        after[s.name] = res['Pw1']
        r = edge_strain(res['Pw0'], res['Pw1'], s.tris.astype(np.int64))
        dn = np.linalg.norm(res['disp'], axis=1)
        st[s.name] = dict(verts=len(dn), disp_mean=round(float(dn.mean()), 3), disp_max=round(float(dn.max()), 3),
                          strain_min=round(float(r.min()), 3), strain_max=round(float(r.max()), 3),
                          weights_blended=res['wchanged'], collision_pushed=res['pushed'], rigid_verts=res['rigid'])
    tmp = os.path.join(TMP, '%s_%s_from%s.nif' % (item, wt, ws))
    g.save(tmp)
    g2 = GNif(tmp)
    A0, T0 = visible_union(g2, before); A1, T1 = visible_union(g2, after)
    pd, _ = poke_design(ws, A0, T0, A1, T1, wt=wt)
    pr = pairs()
    VP = pr['V'][ws][0]; HP = pr['H'][wt][0]
    dv, _ = nearest(A0, VP); dh0, _ = nearest(A0, HP); dh1, _ = nearest(A1, HP)
    near = dv < 4
    e0 = np.abs(dh0 - dv)[near]; e1 = np.abs(dh1 - dv)[near]
    return tmp, dict(source='_%s' % ws, shapes=st, poke=pd,
                     offset_err_before=(round(float(e0.mean()), 3), round(float(np.percentile(e0, 95)), 3)),
                     offset_err_after=(round(float(e1.mean()), 3), round(float(np.percentile(e1, 95)), 3)),
                     skin=validate(g2))


for item in ITEMS:
    for wt in '01':
        cands = [run(item, ws, wt) for ws in ('0', '1')]
        for _, c in cands:
            print(item, 'out _%s from %s' % (wt, c['source']), 'poke', c['poke'], 'offset', c['offset_err_before'], '->', c['offset_err_after'], flush=True)
        nat = [c for c in cands if c[1]['source'] == '_' + wt][0]
        alt = [c for c in cands if c is not nat][0]
        best = alt if alt[1]['poke']['after_pct'] < nat[1]['poke']['after_pct'] - 1.0 else nat
        out = os.path.join(OUT, '%s_%s.nif' % (item, wt))
        open(out, 'wb').write(open(best[0], 'rb').read())
        best[1]['alternatives'] = [dict(source=c['source'], poke=c['poke']) for _, c in cands]
        report['%s_%s' % (item, wt)] = best[1]
        print('  -> chosen', best[1]['source'])
json.dump(report, open(os.path.join(JOB, 'report_parts.json'), 'w'), indent=1, default=float)
