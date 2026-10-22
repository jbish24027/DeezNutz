import sys, os, numpy as np
sys.path.insert(0, os.path.abspath('../final'))
import final_model as fm
ST = os.path.abspath('../final/stage/alive/Authoria - Picta x Astralite - E11/enbseries')
def LP(p): return chr(92) * 2 + '?' + chr(92) + p.replace('/', chr(92))
orig = fm.parse_ini_E
worst = {}
for fn, ws in fm.FILES.items():
    E_P, _ = fm.parse_ini_E(fm.DARK + '/' + fn)
    # parse staged with long path
    import re
    txt = open(LP(os.path.join(ST, fn)), 'rb').read().decode('utf-8', 'replace')
    tmp = os.path.abspath('tmp_stage.ini'); open(tmp, 'wb').write(txt.encode('utf-8'))
    E_W, _ = fm.parse_ini_E(tmp)
    for w in ws:
        R = fm.picta_records(w)
        for h in fm.AUDIT_H:
            for nm, f in (('band_top', lambda E: fm.V_band(E, R, h, 'top')), ('band_hor', lambda E: fm.V_band(E, R, h, 'hor')),
                          ('clouds', lambda E: fm.V_cloud(E, R, h)), ('fog_far', lambda E: fm.V_fog(E, R, h)), ('sunlight', lambda E: fm.V_light(E, R, h))):
                a = fm.Y(f(E_P))
                if a < 1e-9: continue
                d = fm.Y(f(E_W)) / a - 1
                if nm not in worst or abs(d) > abs(worst[nm][0]): worst[nm] = (d, h, w)
for k, (d, h, w) in worst.items(): print(f'{k:10s} written-file dY {100 * d:+.3f}% @{h} {w}')
