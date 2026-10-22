import importlib.util, numpy as np
spec = importlib.util.spec_from_file_location('m', 'indep_model.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.CL = (5.5, 10.0, 16.0, 20.5)
def sunz_fair(h):
    up, dn = (5.5 + 10) / 2, (16 + 20.5) / 2
    import math
    if up <= h <= dn: e = math.radians(60) * math.sin(math.pi * (h - up) / (dn - up))
    else:
        d = min(abs(h - up), abs(h - dn)); e = -math.radians(12) * min(1, d / 1.5)
    return math.sin(e)
fair = {'19FC01': 'Picta - Weathers/00_Master/C01_Cloudy.ini', '19FA01': 'Picta - Weathers/00_Master/A01_Clear.ini',
        '19FA02': 'Picta - Weathers/00_Master/A01_Clear.ini', '19FB02': 'Picta - Weathers/00_Master/B01_Lightly_Cloudy.ini'}
for w, fn in fair.items():
    iP = m.Ini(m.DARK + '/enbseries/' + fn, m.DARK + '/enbseries.ini'); iB = m.Ini(m.STAGE + '/enbseries/' + fn, m.STAGE + '/enbseries.ini')
    RP, RB = m.recs(w, False), m.recs(w, True); worst = {}
    for h in m.HOURS:
        a = m.comps(iP, RP, h, m.clmt_mid, sunz_fair); b = m.comps(iB, RB, h, m.clmt_mid, sunz_fair)
        for k in a:
            if k.startswith('_') or k == 'vl_keylight_x_filter': continue
            ya = m.Y(a[k])
            if ya < 1e-7: continue
            d = m.Y(b[k]) / ya - 1
            if k not in worst or abs(d) > abs(worst[k][0]): worst[k] = (d, h)
    top = sorted(worst.items(), key=lambda kv: -abs(kv[1][0]))[:8]
    print(w, ' '.join(f'{k} {100 * d:+.2f}%@{h:g}' for k, (d, h) in top))
