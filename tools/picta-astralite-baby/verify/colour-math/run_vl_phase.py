"""(e) What the intensity-only VL model leaves out: the VOLI phase function and density term
(ISVolumetricLightingGenerateCS.hlsl 86-107). Baby/Picta VL ratio at several view angles to the sun, using the installed
VOLI fields (houseCARL reads), the installed E11 GVR lines and the same key light as run_vl.py."""
import os, sys, math, json
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11

FULL = {}
for fn in ('picta_voli.jsonl', 'baby_voli.jsonl'):
    for l in open(os.path.join(H, fn), encoding='utf-8').read().splitlines()[1:]:
        r = json.loads(l)
        d = {x['path']: x.get('value', x.get('note')) for x in r['fields']}
        FULL[r['formid']] = dict(pc=float(d['PhaseFunctionContribution']), g=float(d['PhaseFunctionScattering']), dc=float(d['DensityContribution']))


def phase(pc, g, c):
    pf = (1 - g * g) / (4 * math.pi * (1 - c * g))
    return 1 + (pf - 1) * pc


REC = cm.load_records(); VOL = cm.load_voli(); WL = cm.weather_files(cm.FORK)
BP, BB = os.path.join(cm.DARK, 'enbseries.ini'), os.path.join(cm.FORK, 'enbseries.ini')
T = cm.T_of(BP)
ANG = (1.0, 0.9, 0.5, 0.0, -1.0)
NOISE_MEAN = 0.5   # assumption: mean of the 3D noise texture; height term ignored (ground level)
rows = {}
for w in sorted(REC['P']):
    fn = WL[w].replace('/', os.sep)
    XP = cm.Ctx(E11(BP, os.path.join(cm.DARK, 'enbseries', fn)), T)
    XB = cm.Ctx(E11(BB, os.path.join(cm.FORK, 'enbseries', fn)), T)
    out = {}
    for h in (7.5, 13.0, 18.5):
        sz = cm.sunz(h, 7.5, 18.5)
        res = {}
        for lane, X, R in (('P', XP, REC['P'][w]), ('B', XB, REC['B'][w])):
            o = cm.comps(X, R, h, cm.clmt_mid, cm.PICTA_CL, sz)
            rad, _ = cm.vl(o, R, VOL, h, cm.clmt_mid, cm.PICTA_CL)
            c = cm.clmt_mid(h, cm.PICTA_CL)
            ph = {a: sum(c[s] * phase(FULL[R[s]['voli']]['pc'], FULL[R[s]['voli']]['g'], a) for s in cm.SL) for a in ANG}
            dens = sum(c[s] * (1 + (NOISE_MEAN - 1) * FULL[R[s]['voli']]['dc']) for s in cm.SL)
            res[lane] = (rad, ph, dens)
        (rp, php, dp), (rb, phb, db) = res['P'], res['B']
        out[h] = {'intensity_only': round(rb / rp, 2), **{f'c={a:+.1f}': round(rb * phb[a] * db / (rp * php[a] * dp), 1) for a in ANG},
                  'baby_offsun_vs_picta_sunpeak': round(rb * phb[0.0] * db / (rp * php[1.0] * dp), 2)}
    rows[w] = out
    names = {s: VOL[REC['B'][w][s]['voli']]['name'] for s in ('Sunrise', 'Day', 'Sunset')}
    print(w, names['Day'], ' | '.join(f"{h:g}: io {v['intensity_only']}x, 90deg {v['c=+0.0']}x, away {v['c=-1.0']}x, at-sun {v['c=+1.0']}x, off-sun/Picta-peak {v['baby_offsun_vs_picta_sunpeak']}" for h, v in out.items()))
json.dump(rows, open(os.path.join(H, 'vl_phase.json'), 'w'), indent=1)
