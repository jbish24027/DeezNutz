"""(e) weather-transition cross-term: E11 lerps each setting between the outgoing and incoming weather
(SettingManager InterpolateValues, weatherBlendFactor) and the engine lerps the record colours; the per-weather luminance
lock does not cover the product. Picta vs baby luminance at blend t for every pair of the 28 weathers."""
import os, sys, itertools, json
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11, PER

REC = cm.load_records()
WL = cm.weather_files(cm.FORK)
BP, BB = os.path.join(cm.DARK, 'enbseries.ini'), os.path.join(cm.FORK, 'enbseries.ini')
T = cm.T_of(BP)
E = {}
for w in REC['P']:
    fn = WL[w].replace('/', os.sep)
    E[w] = (E11(BP, os.path.join(cm.DARK, 'enbseries', fn)), E11(BB, os.path.join(cm.FORK, 'enbseries', fn)))


class Blend:
    def __init__(self, a, b, t):
        self.a, self.b, self.t = a, b, t

    def get(self, cat, key):
        A, B = self.a.get(cat, key), self.b.get(cat, key)
        return {p: np.asarray(A[p], float) * (1 - self.t) + np.asarray(B[p], float) * self.t for p in PER}


def blendR(Ra, Rb, t):
    R = {}
    n = min(len(Ra['_layers']), len(Rb['_layers']))
    for s in cm.SL:
        d = {}
        for k in ('upper', 'horizon', 'fogfar', 'fognear', 'sun', 'sunlight'):
            d[k] = Ra[s][k] * (1 - t) + Rb[s][k] * t
        d['clouds'] = [Ra[s]['clouds'][i] * (1 - t) + Rb[s]['clouds'][i] * t for i in range(n)]
        d['dalc'] = {a: Ra[s]['dalc'][a] * (1 - t) + Rb[s]['dalc'][a] * t for a in cm.AX}
        d['voli'] = Ra[s]['voli']
        R[s] = d
    R['_layers'] = Ra['_layers'][:n]
    return R


WS = sorted(REC['P'])
HOURS = [5.5 + 0.5 * i for i in range(31)]
worst = {}
for wa, wb in itertools.combinations(WS, 2):
    if WL[wa] == WL[wb]:
        continue
    for t in (0.5,):
        XP = cm.Ctx(Blend(E[wa][0], E[wb][0], t), T)
        XB = cm.Ctx(Blend(E[wa][1], E[wb][1], t), T)
        RP = blendR(REC['P'][wa], REC['P'][wb], t)
        RB = blendR(REC['B'][wa], REC['B'][wb], t)
        for h in HOURS:
            sz = cm.sunz(h, 7.5, 18.5)
            a = cm.comps(XP, RP, h, cm.clmt_mid, cm.PICTA_CL, sz)
            b = cm.comps(XB, RB, h, cm.clmt_mid, cm.PICTA_CL, sz)
            for k in a:
                if k.startswith('_'):
                    continue
                ya = cm.Y(a[k])
                if ya < 1e-6:
                    continue
                d = cm.Y(b[k]) / ya - 1
                kk = k.rsplit('_L', 1)[0]
                if kk not in worst or abs(d) > abs(worst[kk][0]):
                    worst[kk] = (d, h, wa, wb)
for k, (d, h, wa, wb) in sorted(worst.items(), key=lambda kv: -abs(kv[1][0])):
    print(f'{k:16s} {100 * d:+7.2f}% @{h:5.2f} {wa}<->{wb} (t=0.5)')
json.dump({k: [round(100 * v[0], 3), v[1], v[2], v[3]] for k, v in worst.items()}, open(os.path.join(H, 'transition_worst.json'), 'w'), indent=1)
