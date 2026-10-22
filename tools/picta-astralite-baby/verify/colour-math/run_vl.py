"""(d) VL on INSTALLED values: baby intensity-only VL vs the design's half-strength target (cap 1.10) and vs Picta,
every 15 min 05:00-21:30, Picta clock and (fair weathers) the fair clock. Astralite's own VL-to-key ratio (relA) comes from
the design's Astralite model (read-only import); everything else from the installed files / houseCARL reads."""
import sys, os, json, math
sys.dont_write_bytecode = True
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11
D = r'C:\1. AUTHORIA\_tools\picta-astralite-baby\design'
sys.path.insert(0, os.path.join(D, 'final'))
import final_model as fm

VOLAMT = 0.5
REC = cm.load_records()
VOL = cm.load_voli()
WL = cm.weather_files(cm.FORK)
BP, BB = os.path.join(cm.DARK, 'enbseries.ini'), os.path.join(cm.FORK, 'enbseries.ini')
T = cm.T_of(BP)
HOURS = [5.0 + 0.25 * i for i in range(67)]
PLAN = json.load(open(os.path.join(D, 'finalize', 'final2_plan.json')))['vl']['0.5_alive']['per_weather']
out = {}
glob_over = (0, None)
glob_x = {}
for w in sorted(REC['P']):
    fn = WL[w].replace('/', os.sep)
    XP = cm.Ctx(E11(BP, os.path.join(cm.DARK, 'enbseries', fn)), T)
    XB = cm.Ctx(E11(BB, os.path.join(cm.FORK, 'enbseries', fn)), T)
    RP, RB = REC['P'][w], REC['B'][w]
    mp = fm.mist_partner(w)
    AR_ = fm.astra_records(mp)
    SE = fm.soul_E(AR_['_soul'])
    relA = {}
    for s, hs in dict(Sunrise=7.0, Day=13.0, Sunset=19.0).items():
        v = fm.astra_voli(AR_['_voli'][s])
        LA = fm.V_light(SE, AR_, hs, fm.NAT_TOD, fm.ASTRA_CLMT)
        gA = fm.ev(SE, 'GAMEVOLUMETRICRAYS', 'Intensity', hs, fm.NAT_TOD)
        gF = fm.ev(SE, 'GAMEVOLUMETRICRAYS', 'ColorFilter', hs, fm.NAT_TOD)
        relA[s] = v['I'] * gA * fm.Y(gF * fm.lerp(LA, v['col'], v['cc'])) / max(fm.Y(LA), 1e-9)
    clocks = [('picta', cm.PICTA_CL)] + ([('fair', cm.FAIR_CL)] if w in cm.FAIR_W else [])
    for ck, C in clocks:
        up, dn = (C[0] + C[1]) / 2, (C[2] + C[3]) / 2
        over = (0.0, None); under = (9.0, None); xmax = (0.0, None); rows = {}
        for h in HOURS:
            sz = cm.sunz(h, up, dn)
            a = cm.comps(XP, RP, h, cm.clmt_mid, C, sz)
            b = cm.comps(XB, RB, h, cm.clmt_mid, C, sz)
            rp, dp = cm.vl(a, RP, VOL, h, cm.clmt_mid, C)
            rb, db = cm.vl(b, RB, VOL, h, cm.clmt_mid, C)
            c = cm.clmt_mid(h, C)
            tgt = max(VOLAMT * sum(c[s] * relA[s] for s in ('Sunrise', 'Day', 'Sunset')) + c['Night'] * rp, rp)
            q = rb / tgt if tgt > 1e-6 else None
            if q is not None and q > over[0]:
                over = (q, h)
            if q is not None and q < under[0]:
                under = (q, h)
            if rp > 1e-9 and rb / rp > xmax[0]:
                xmax = (rb / rp, h)
            rows[h] = dict(picta=round(rp, 3), baby=round(rb, 3), target=round(tgt, 3), dens_p=round(dp, 3), dens_b=round(db, 3),
                           gvrI_p=round(a['_gvr_I'], 3), gvrI_b=round(b['_gvr_I'], 3), gvrR_p=a['_gvr_R'], gvrR_b=b['_gvr_R'],
                           gvrF_b=[round(x, 4) for x in b['_gvr_F']])
        out[f'{w}/{ck}'] = dict(max_over_target=over, min_vs_target=under, max_x_picta=xmax,
                                plan_max_over=PLAN[w]['max_over_target'], rows=rows)
        if over[0] > glob_over[0]:
            glob_over = (over[0], w, ck, over[1])
        print(f'{w} {ck:5s} baby/target max {over[0]:.3f}@{over[1]}  min {under[0]:.3f}@{under[1]}  baby/Picta max {xmax[0]:.2f}@{xmax[1]}'
              f'  | 07:30 {rows[7.5]["baby"] / max(rows[7.5]["picta"], 1e-9):.2f}x 13:00 {rows[13.0]["baby"] / max(rows[13.0]["picta"], 1e-9):.2f}x'
              f' 18:30 {rows[18.5]["baby"] / max(rows[18.5]["picta"], 1e-9):.2f}x | plan max {PLAN[w]["max_over_target"]}')
print('GLOBAL baby/target max', glob_over)
json.dump(out, open(os.path.join(H, 'vl_installed.json'), 'w'), indent=0, default=float)
