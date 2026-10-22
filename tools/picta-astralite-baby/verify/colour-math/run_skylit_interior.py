"""Sky-lit interiors (CELL flags IsInteriorCell + UseSkyLighting take the region weather's DALC): ambient luminance and hue,
baby vs Picta, with E11's Interior-period AmbientLightingDesaturation (unchanged files) instead of the exterior one."""
import os, sys, math
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11
M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])


def lch(c):
    c = np.asarray(c, float) * (0.18 / cm.Y(c))
    L, a, b = M2 @ np.cbrt(M1 @ np.maximum(c, 0))
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

REC = cm.load_records()
WL = cm.weather_files(cm.FORK)
BP = os.path.join(cm.DARK, 'enbseries.ini')
worst = (0, None)
hue = []
for w in sorted(REC['P']):
    e = E11(BP, os.path.join(cm.DARK, 'enbseries', WL[w].replace('/', os.sep)))
    dI = e.get('ENVIRONMENT', 'AmbientLightingDesaturation')
    for per in ('InteriorDay', 'InteriorNight'):
        d = float(dI[per])
        for h in [5.0 + 0.25 * i for i in range(67)]:
            for ax in cm.AX:
                a = cm.desat(cm.rat(REC['P'][w], h, cm.clmt_mid, cm.PICTA_CL, 'dalc', ax), d)
                b = cm.desat(cm.rat(REC['B'][w], h, cm.clmt_mid, cm.PICTA_CL, 'dalc', ax), d)
                r = cm.Y(b) / cm.Y(a) - 1
                if abs(r) > abs(worst[0]):
                    worst = (r, w, per, h, ax, d)
                if w in ('19FA01', '19FC01') and ax == 'DirectionalXPlus' and per == 'InteriorDay' and h in (7.5, 13.0, 18.5):
                    hue.append((w, h, round(lch(a)[2], 1), round(lch(b)[2], 1)))
print('sky-lit interior ambient, worst luminance change baby vs Picta:', round(100 * worst[0], 2), '%', worst[1:])
print('hue (InteriorDay desat) X+:', hue)
