import importlib.util, numpy as np
spec = importlib.util.spec_from_file_location('m', 'indep_model.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ALB = {'grass/foliage': np.array([0.10, 0.17, 0.04]), 'pine needles': np.array([0.06, 0.10, 0.05]), 'dirt/brown rock': np.array([0.30, 0.22, 0.14]),
       'grey stone': np.array([0.30, 0.30, 0.30]), 'snow': np.array([0.80, 0.82, 0.88]), 'skin': np.array([0.55, 0.35, 0.27])}
for w, fn in (('19FA01', 'Picta - Weathers/00_Master/A01_Clear.ini'), ('19FC01', 'Picta - Weathers/00_Master/C01_Cloudy.ini')):
    iP = m.Ini(m.DARK + '/enbseries/' + fn, m.DARK + '/enbseries.ini'); iB = m.Ini(m.STAGE + '/enbseries/' + fn, m.STAGE + '/enbseries.ini')
    RP, RB = m.recs(w, False), m.recs(w, True)
    for h in (7.5, 13.0, 18.5):
        a = m.comps(iP, RP, h, m.clmt_mid, m.sunz_A); b = m.comps(iB, RB, h, m.clmt_mid, m.sunz_A)
        for comp in ('amb_ZMinus', 'amb_XPlus', 'sunlight'):
            la, lb = a[comp], b[comp]
            row = ' '.join(f'{k} {100 * (m.Y(alb * lb) / m.Y(alb * la) - 1):+.1f}%' for k, alb in ALB.items())
            print(f'{w} {h:5.2f} {comp:11s} light Y {100 * (m.Y(lb) / m.Y(la) - 1):+.2f}% | surface: {row}')
