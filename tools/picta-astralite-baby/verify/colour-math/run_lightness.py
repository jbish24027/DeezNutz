"""(e) Equal luminance is not equal perceived lightness: OKLab L of baby vs Picta for each component at the same Y-lock,
plus a per-channel tonemap probe (Reinhard x/(1+x) at exposure k) to see how a per-channel curve turns hue into brightness."""
import os, sys, math, json
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11

M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])


def L_ok(c):
    return float((M2 @ np.cbrt(M1 @ np.maximum(np.asarray(c, float), 0)))[0])


REC = cm.load_records()
WL = cm.weather_files(cm.FORK)
BP, BB = os.path.join(cm.DARK, 'enbseries.ini'), os.path.join(cm.FORK, 'enbseries.ini')
T = cm.T_of(BP)
worstL = {}
worstT = {}
for w in sorted(REC['P']):
    fn = WL[w].replace('/', os.sep)
    XP = cm.Ctx(E11(BP, os.path.join(cm.DARK, 'enbseries', fn)), T)
    XB = cm.Ctx(E11(BB, os.path.join(cm.FORK, 'enbseries', fn)), T)
    for h in [5.5 + 0.25 * i for i in range(61)]:
        sz = cm.sunz(h, 7.5, 18.5)
        a = cm.comps(XP, REC['P'][w], h, cm.clmt_mid, cm.PICTA_CL, sz)
        b = cm.comps(XB, REC['B'][w], h, cm.clmt_mid, cm.PICTA_CL, sz)
        for k in a:
            if k.startswith('_') or cm.Y(a[k]) < 1e-6:
                continue
            kk = k.rsplit('_L', 1)[0]
            # perceived lightness at the component's own level (scaled to mid-grey so L is comparable across components)
            s = 0.18 / cm.Y(a[k])
            dL = L_ok(b[k] * s) - L_ok(a[k] * s)
            if kk not in worstL or abs(dL) > abs(worstL[kk][0]):
                worstL[kk] = (dL, h, w)
            # per-channel Reinhard after scaling to mid-grey exposure
            ta, tb = (a[k] * s) / (1 + a[k] * s), (b[k] * s) / (1 + b[k] * s)
            dT = cm.Y(tb) / cm.Y(ta) - 1
            if kk not in worstT or abs(dT) > abs(worstT[kk][0]):
                worstT[kk] = (dT, h, w)
print('OKLab L difference at equal Y (0.18 grey level; 1 JND ~ 0.005-0.01):')
for k, (d, h, w) in sorted(worstL.items(), key=lambda kv: -abs(kv[1][0])):
    print(f'   {k:16s} dL {d:+.4f} @{h:5.2f} {w}   | per-channel Reinhard Y {100 * worstT[k][0]:+.2f}% @{worstT[k][1]:5.2f} {worstT[k][2]}')
