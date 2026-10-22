"""(c) hue moves from the INSTALLED values vs the design's hue_tables.json promises. Read-only."""
import json, os, sys, math
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11

M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])


def lch(c):
    c = np.asarray(c, float)
    c = c * (0.18 / cm.Y(c))
    L, a, b = M2 @ np.cbrt(M1 @ np.maximum(c, 0))
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


REC = cm.load_records()
WL = cm.weather_files(cm.FORK)
BP, BB = os.path.join(cm.DARK, 'enbseries.ini'), os.path.join(cm.FORK, 'enbseries.ini')
T = cm.T_of(BP)
HT = json.load(open(r'C:\1. AUTHORIA\_tools\picta-astralite-baby\design\finalize\hue_tables.json'))
MAP = {'dome_hor_away': 'dome_hor_away', 'dome_hor_sun': 'dome_hor_sun', 'dome_zenith': 'dome_zenith', 'fog_far': 'fog_far',
       'sunlight': 'sunlight', 'amb_XPlus': 'amb_XPlus', 'amb_ZMinus': 'amb_ZMinus'}
worst = []
rows = []
for w, tab in HT.items():
    fn = WL[w].replace('/', os.sep)
    XP = cm.Ctx(E11(BP, os.path.join(cm.DARK, 'enbseries', fn)), T)
    XB = cm.Ctx(E11(BB, os.path.join(cm.FORK, 'enbseries', fn)), T)
    RP, RB = REC['P'][w], REC['B'][w]
    L0 = RP['_layers'][0]
    for hs, row in tab.items():
        h = float(hs)
        sz = cm.sunz(h, 7.5, 18.5)
        a = cm.comps(XP, RP, h, cm.clmt_mid, cm.PICTA_CL, sz)
        b = cm.comps(XB, RB, h, cm.clmt_mid, cm.PICTA_CL, sz)
        a['clouds'], b['clouds'] = a[f'cloud_base_L{L0}'], b[f'cloud_base_L{L0}']
        a['cloud_sunlit'], b['cloud_sunlit'] = a[f'cloud_sunlit_L{L0}'], b[f'cloud_sunlit_L{L0}']
        for cn, v in row.items():
            if cn not in a:
                continue
            _, Cp, hp = lch(a[cn]); _, Cb, hb = lch(b[cn])
            dp, db = float(v['picta'].split('/')[0]), float(v['baby'].split('/')[0])
            cdp, cdb = float(v['picta'].split('/')[1].split()[0]), float(v['baby'].split('/')[1].split()[0])
            dY = 100 * (cm.Y(b[cn]) / cm.Y(a[cn]) - 1)
            err = max(abs(((hp - dp + 180) % 360) - 180), abs(((hb - db + 180) % 360) - 180))
            rows.append((w, h, cn, round(hp, 1), round(Cp, 3), round(hb, 1), round(Cb, 3), dp, cdp, db, cdb, round(dY, 2), v['dY_pct']))
            if Cb >= 0.012:
                worst.append((err, w, h, cn, hp, hb, dp, db))
for r in rows:
    if r[2] in ('dome_hor_away', 'fog_far', 'clouds', 'amb_XPlus', 'dome_hor_sun') and r[1] in (7.5, 13.0, 18.5):
        print('%s %5.2f %-14s installed P %5.1f/%.3f -> B %5.1f/%.3f | design P %5.1f/%.3f -> B %5.1f/%.3f | dY inst %+.2f%% design %+.2f%%' % r)
worst.sort(reverse=True)
print('largest |installed - design| hue gap (chroma >= 0.012):', [(round(e, 2), w, h, cn) for e, w, h, cn, *_ in worst[:6]])
json.dump(rows, open(os.path.join(H, 'hue_installed.json'), 'w'), indent=0)
