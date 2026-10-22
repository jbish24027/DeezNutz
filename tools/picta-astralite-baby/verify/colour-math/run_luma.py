"""(a) luminance gate, (b) night identity, (d) filter/GVR ranges + VL ratios, on INSTALLED values. Read-only."""
import json, os, sys, math
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11, PER

REC = cm.load_records()
VOL = cm.load_voli()
WLP = cm.weather_files(cm.DARK)
WLB = cm.weather_files(cm.FORK)
BASE_P = os.path.join(cm.DARK, 'enbseries.ini')
BASE_B = os.path.join(cm.FORK, 'enbseries.ini')
TP, TB = cm.T_of(BASE_P), cm.T_of(BASE_B)
assert TP == TB, (TP, TB)
WS = sorted(REC['P'])
HOURS = [5.0 + 0.25 * i for i in range(67)]
NIGHT = [20.5 + 0.25 * i for i in range(37)]
ctx = {}
for w in WS:
    assert WLP[w] == WLB[w], (w, WLP[w], WLB[w])
    fp = os.path.join(cm.DARK, 'enbseries', WLP[w].replace('/', os.sep))
    fb = os.path.join(cm.FORK, 'enbseries', WLB[w].replace('/', os.sep))
    ctx[w] = (cm.Ctx(E11(BASE_P, fp), TP), cm.Ctx(E11(BASE_B, fb), TB))

SUN = {'A_mid': lambda C: ((C[0] + C[1]) / 2, (C[2] + C[3]) / 2), 'B_edge': lambda C: (C[0], C[3])}
RULES = {'mid': cm.clmt_mid, 'plateau': cm.clmt_plateau}
res = {}
worst_all = {}
nightmax = 0.0
night_where = None
vlrows = {}
for rule, cw in RULES.items():
    for sp, sfn in SUN.items():
        lab = f'{rule}+{sp}'
        worst = {}
        for w in WS:
            XP, XB = ctx[w]
            RP, RB = REC['P'][w], REC['B'][w]
            clocks = [('picta', cm.PICTA_CL)] + ([('fair', cm.FAIR_CL)] if w in cm.FAIR_W else [])
            for ck, C in clocks:
                up, dn = sfn(C)
                for h in HOURS:
                    sz = cm.sunz(h, up, dn)
                    a = cm.comps(XP, RP, h, cw, C, sz)
                    b = cm.comps(XB, RB, h, cw, C, sz)
                    for k in a:
                        if k.startswith('_'):
                            continue
                        ya = cm.Y(a[k])
                        if ya < 1e-7:
                            continue
                        d = cm.Y(b[k]) / ya - 1
                        kk = k if not k.startswith('cloud_') else k.rsplit('_L', 1)[0]
                        if kk not in worst or abs(d) > abs(worst[kk][0]):
                            worst[kk] = (d, h, w, ck)
                    if rule == 'mid' and sp == 'A_mid':
                        va, da = cm.vl(a, RP, VOL, h, cw, C)
                        vb, db = cm.vl(b, RB, VOL, h, cw, C)
                        vlrows.setdefault(w, {}).setdefault(ck, {})[h] = dict(picta=va, baby=vb, dens_p=da, dens_b=db,
                                                                             gvrI_p=a['_gvr_I'], gvrI_b=b['_gvr_I'], gvrR_p=a['_gvr_R'], gvrR_b=b['_gvr_R'])
                for h in NIGHT:
                    hh = h % 24
                    sz = cm.sunz(hh, up, dn)
                    a = cm.comps(XP, RP, hh, cw, C, sz)
                    b = cm.comps(XB, RB, hh, cw, C, sz)
                    for k in a:
                        if k.startswith('_'):
                            dv = abs(np.asarray(a[k], float) - np.asarray(b[k], float)).max()
                        else:
                            dv = float(np.abs(a[k] - b[k]).max())
                        if dv > nightmax:
                            nightmax, night_where = dv, (lab, w, ck, hh, k)
                    va, _ = cm.vl(a, RP, VOL, hh, cw, C)
                    vb, _ = cm.vl(b, RB, VOL, hh, cw, C)
                    if abs(va - vb) > nightmax:
                        nightmax, night_where = abs(va - vb), (lab, w, ck, hh, 'vl')
        res[lab] = worst
        print(f'== {lab}')
        for k, (d, h, w, ck) in sorted(worst.items(), key=lambda kv: -abs(kv[1][0])):
            flag = '  <-- OVER 1.0%' if abs(d) > 0.01 else ''
            print(f'   {k:16s} {100 * d:+7.3f}%  @{h:5.2f} {w} ({ck} clock){flag}')
print('NIGHT 20:30-05:30 max abs difference (all components, all rules/clocks/weathers):', nightmax, night_where)
json.dump({k: {kk: [round(100 * v[0], 4), v[1], v[2], v[3]] for kk, v in d.items()} for k, d in res.items()},
          open(os.path.join(H, 'luma_worst.json'), 'w'), indent=1)
json.dump(vlrows, open(os.path.join(H, 'vl_rows.json'), 'w'), default=float)
