import sys, os, math, numpy as np
sys.path.insert(0, os.path.abspath('../final'))
import final_model as fm
res = {}
out = []
for fn, ws in fm.FILES.items():
    E_P, RAW = fm.parse_ini_E(fm.DARK + '/' + fn)
    cp = fm.colour_partner(ws[0]); A = fm.Astra({cp: 1.0})
    for w in ws[:1]:
        R = fm.picta_records(w)
        chans = {'hor': lambda E, R_, h: fm.V_band(E, R_, h, 'hor'), 'top': lambda E, R_, h: fm.V_band(E, R_, h, 'top'),
                 'clouds': fm.V_cloud, 'fog': lambda E, R_, h: fm.V_fog(E, R_, h), 'light': lambda E, R_, h: fm.V_light(E, R_, h),
                 'scat': lambda E, R_, h: fm.scat_parts(E, R_, h, fm.views(0)['hor_sun'])['scat']}
        for ax in ('DirectionalXPlus', 'DirectionalZMinus'):
            chans['amb_' + ax[11:]] = (lambda ax: (lambda E, R_, h: fm.V_amb(E, R_, h, ax)))(ax)
        for cn, Vf in chans.items():
            dhs = []
            for h in fm.FIT_H:
                vp = Vf(E_P, R, h); va = A.vis(lambda E, R_, hh: Vf(E, R_, hh), h)
                if va is None or fm.Y(vp) <= 1e-9: continue
                Lp, Cp, hp = fm.lch(vp); La, Ca, ha = fm.lch(va)
                if Cp < 0.01 or Ca < 0.01: continue
                a = fm.alpha_fn(None, {'x': {'Sunrise': .5, 'Day': .3, 'Sunset': .5}}, 'x')(h)
                if a <= 0.02: continue
                dhs.append((h, ((ha - hp + 180) % 360) - 180, Cp, Ca))
            big = [d for d in dhs if abs(d[1]) > 150]
            signs = {np.sign(d[1]) for d in big}
            if big:
                out.append((w, fn.split('/')[-1], cn, len(big), 'FLIP' if len(signs) > 1 else '', [(h, round(d, 0)) for h, d, _, _ in big][:12]))
for o in out: print(o)
