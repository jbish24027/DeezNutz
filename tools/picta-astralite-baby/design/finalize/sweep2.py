"""MIX levels (Light/Medium/Strong) + KAPPA amplitude demo on the finalize model: hue names and worst |dY| per level."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import final2_model as m
FILES = {'19FA01': 'Picta - Weathers/00_Master/A01_Clear.ini', '19FC01': 'Picta - Weathers/00_Master/C01_Cloudy.ini',
         '19FD03': 'Picta - Weathers/00_Master/D03_Overcast_Rain_Light.ini'}
LEVELS = {'Light': dict(Sunrise=0.35, Day=0.20, Sunset=0.35), 'Medium': dict(Sunrise=0.5, Day=0.3, Sunset=0.5), 'Strong': dict(Sunrise=0.75, Day=0.45, Sunset=0.75)}
out = {}
VIS = [c for c in ('band_top', 'band_hor', 'dome_zenith', 'dome_hor_sun', 'dome_hor_away', 'dome_mid_away', 'dome_toward_sun_20', 'clouds', 'cloud_sunlit',
                   'fog_far', 'fog_near', 'sunlight', 'scat_horizon_sunward', 'scat_at_sun') ] + ['amb_' + a[11:] for a in m.AXES]
for lvl, mix in list(LEVELS.items()) + [('Medium_kappa0.6', None)]:
    D = m.dials()
    if mix: D['MIX'] = mix
    else: D['KAPPA'] = dict(sky=0.6, clouds=0.6, fog=0.6, light=1.0, amb=1.0, scat=1.0)
    for w, fn in FILES.items():
        r = m.solve_file(fn, D)
        worst, _ = m.audit_weather(r, w, hours=[5.0 + 0.25 * i for i in range(67)])
        wv = max((abs(worst[c][0]), c) for c in VIS if c in worst)
        ws = max((abs(v[0]), c) for c, v in worst.items() if c.startswith('surf_'))
        row = {}
        for h in (7.5, 13.0, 18.5):
            a = m.components(r['_E_P'], r['_RP'][w], h, light=True); b = m.components(r['_E_B'], r['_RB'][w], h, light=True)
            for cn in ('dome_hor_away', 'fog_far', 'clouds', 'amb_XPlus', 'amb_ZMinus', 'sunlight'):
                La, Ca, ha = m.lch(a[cn]); Lb, Cb, hb = m.lch(b[cn])
                row[f'{cn}@{h}'] = f'{ha:.0f}/{Ca:.3f} -> {hb:.0f}/{Cb:.3f} {m.hue_name(hb, Cb)}'
        out[f'{lvl} {w}'] = dict(worst_visible=[round(wv[0], 2), wv[1]], worst_surface=[round(ws[0], 2), ws[1]], hues=row)
        print(lvl, w, 'worst visible', round(wv[0], 2), wv[1], '| surface', round(ws[0], 2), ws[1], flush=True)
        for k, v in row.items():
            if '@13.0' in k and 'amb_ZMinus' in k: continue
            print('     ', k, v, flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sweep2.json'), 'w'), indent=1)
