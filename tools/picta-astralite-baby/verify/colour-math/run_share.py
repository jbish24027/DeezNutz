"""User-pick mapping: on-screen share of Astralite's colour reached by the INSTALLED values at 07:30 / 13:00 / 18:30
(MIX labels 0.5 / 0.3 / 0.5), rain/fog/snow classes included. Astralite's visible target comes from the design's own
Astra model (read-only import, no bytecode written); Picta and baby colours come from the installed-file port."""
import sys, os, json, math
sys.dont_write_bytecode = True
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11
D = r'C:\1. AUTHORIA\_tools\picta-astralite-baby\design'
sys.path.insert(0, os.path.join(D, 'final'))
sys.path.insert(0, os.path.join(D, 'finalize'))
import final_model as fm
import final2_model as f2

REC = cm.load_records()
WL = cm.weather_files(cm.FORK)
BP, BB = os.path.join(cm.DARK, 'enbseries.ini'), os.path.join(cm.FORK, 'enbseries.ini')
T = cm.T_of(BP)
VIEW = np.array([0, -math.sqrt(1 - .05 ** 2), .05])
CH = {
    'horizon(dome_hor_away)': ('dome_hor_away', lambda E, R, h: fm.sky_pixel(E, R, h, VIEW)),
    'fog_far': ('fog_far', lambda E, R, h: fm.V_fog(E, R, h)),
    'clouds': ('cloud', lambda E, R, h: f2.V_cloud(E, R, h)),
    'amb_XPlus': ('amb_XPlus', lambda E, R, h: fm.V_amb(E, R, h, 'DirectionalXPlus')),
    'sunlight': ('sunlight', lambda E, R, h: fm.V_light(E, R, h)),
}


def share(vP, vA, vB, lo, hi):
    if vA is None or fm.de_ok(vP, vA) < 0.004:
        return None
    best = min((fm.de_ok(f2.blend(vP, vA, a, 1.0, lo, hi), vB), a) for a in np.arange(0, 1.501, 0.01))
    return round(float(best[1]), 2), round(best[0], 4)


out = {}
for w in sorted(REC['P']):
    fn = WL[w].replace('/', os.sep)
    XP = cm.Ctx(E11(BP, os.path.join(cm.DARK, 'enbseries', fn)), T)
    XB = cm.Ctx(E11(BB, os.path.join(cm.FORK, 'enbseries', fn)), T)
    RP, RB = REC['P'][w], REC['B'][w]
    L0 = RP['_layers'][0]
    cp = fm.colour_partner(w)
    A = fm.Astra({cp: 1.0})
    row = {}
    for hs in (7.5, 13.0, 18.5):
        sz = cm.sunz(hs, 7.5, 18.5)
        a = cm.comps(XP, RP, hs, cm.clmt_mid, cm.PICTA_CL, sz)
        b = cm.comps(XB, RB, hs, cm.clmt_mid, cm.PICTA_CL, sz)
        a['cloud'], b['cloud'] = a[f'cloud_base_L{L0}'], b[f'cloud_base_L{L0}']
        for nm, (k, fa) in CH.items():
            va = A.vis(fa, hs)
            row[f'{nm}@{hs:g}'] = share(a[k], va, b[k], 120.0, 170.0)
    out[w] = row
    print(w, cp, {k: (v[0] if v else None) for k, v in row.items()})
json.dump(out, open(os.path.join(H, 'share_installed.json'), 'w'), indent=1)
