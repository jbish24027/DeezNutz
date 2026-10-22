import sys, os, numpy as np, importlib.util
sys.path.insert(0, os.path.abspath('../final'))
import final_model as fm
spec = importlib.util.spec_from_file_location('m', 'indep_model.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for w, fn in (('19FD02', 'Picta - Weathers/00_Master/D02_Overcast_Heavy_Fog.ini'), ('19FE05', 'Picta - Weathers/00_Master/E05_Storm_Snow_Heavy.ini'),
              ('19FD01', 'Picta - Weathers/00_Master/D01_Overcast.ini'), ('19FA01', 'Picta - Weathers/00_Master/A01_Clear.ini')):
    iP = m.Ini(m.DARK + '/enbseries/' + fn, m.DARK + '/enbseries.ini'); iB = m.Ini(m.STAGE + '/enbseries/' + fn, m.STAGE + '/enbseries.ini')
    RP, RB = m.recs(w, False), m.recs(w, True)
    E_P, _ = fm.parse_ini_E(fm.DARK + '/' + fn); A = fm.Astra({fm.colour_partner(w): 1.0}); R = fm.picta_records(w)
    print('==', w)
    for h in [6.0 + 0.25 * i for i in range(13)] + [17.5, 18.0, 18.5, 19.0, 19.5]:
        a = m.comps(iP, RP, h, m.clmt_mid, m.sunz_A); b = m.comps(iB, RB, h, m.clmt_mid, m.sunz_A)
        va = A.vis(fm.V_cloud, h)
        t = fm.blend(fm.V_cloud(E_P, R, h), va, fm.alpha_fn(None, {'x': {'Sunrise': .5, 'Day': .3, 'Sunset': .5}}, 'x')(h))
        def f(c):
            try: return '%5.1f/%.3f' % (fm.lch(c)[2], fm.lch(c)[1])
            except Exception: return '  n/a  '
        print(f'  {h:5.2f} picta {f(a["cloud_base"])}  baby {f(b["cloud_base"])}  astralite {f(va)}  target(MIX.5) {f(t)}')
