"""VL transition swell vs GVR spread: solve the colour once, then solve_vl with GVR capped at X times Picta's per-period value."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import final2_model as m
src = open(m.__file__, encoding='utf-8').read()
assert "G[f] = {p: float(np.clip(x[i], 0.0, 1000.0)) for i, p in enumerate(FREE)}" in src
D = m.dials()
res = m.run_all(D)
PAIRS = [('19FA01', '19FD03'), ('19FE03', '19FD03'), ('19FE01', '19FD02'), ('19FA01', '19FC01'), ('19FC01', '19FC04'), ('19FA01', '19FE03'), ('19FA01', '19FE05'), ('19FC01', '19FD05')]
orig = m.solve_vl
out = {}
for capx in (None, 12.0, 8.0, 5.0, 3.0):
    # monkeypatch the clip bound
    code = src.split('def solve_vl(results, D, K_fixed=None):')[1].split('def voli_at_C')[0]
    if capx:
        code = code.replace("G[f] = {p: float(np.clip(x[i], 0.0, 1000.0)) for i, p in enumerate(FREE)}",
                            f"G[f] = {{p: float(np.clip(x[i], 0.0, min(1000.0, {capx} * max(GP[f][p], 0.1)))) for i, p in enumerate(FREE)}}")
    ns = dict(m.__dict__)
    exec('def solve_vl(results, D, K_fixed=None):' + code, ns)
    for amt in (0.5,):
        Dv = m.dials(); Dv['VOL_AMOUNT'] = amt
        V = ns['solve_vl'](res, Dv)
        TR = m.vl_transition3(V, PAIRS, hours=(13.0, 18.5))
        reach = {w: d['reached_at_peaks'] for w, d in V['per_weather'].items()}
        worst_swell = max((v['vs_brighter_end'], k) for k, v in TR.items() if k.endswith('baby'))
        worst_swell_A = max((v['vs_brighter_end'], k) for k, v in TR.items() if k.endswith('astralite'))
        mins = {k: min(v[13.0] for w, v in reach.items() if m.wclass(w).startswith(k)) for k in 'ABCDE'}
        gmax = max(g for f in V['GVR_Intensity'].values() for g in f.values())
        out[str(capx)] = dict(worst_swell_baby=worst_swell, worst_swell_astralite=worst_swell_A, min_reach_noon_by_class=mins, gvr_max=gmax,
                              reach_dawn={w: reach[w][7.5] for w in ('19FA01', '19FC01', '19FD02', '19FD03', '19FE05')},
                              swell={k: v['vs_brighter_end'] for k, v in TR.items() if k.endswith('baby')})
        print(f'cap {capx}: GVR max {gmax:.1f} | worst swell baby {worst_swell} | astralite {worst_swell_A} | min noon reach by class {mins} | dawn reach {out[str(capx)]["reach_dawn"]}', flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exp_vlcap.json'), 'w'), indent=1)
