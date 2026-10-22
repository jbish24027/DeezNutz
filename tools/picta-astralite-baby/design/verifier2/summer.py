import sys, os, numpy as np, importlib.util
sys.path.insert(0, os.path.abspath('../final'))
import final_model as fm
spec = importlib.util.spec_from_file_location('m', 'indep_model.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
pairs = [('19FA01', 'Picta - Weathers/00_Master/A01_Clear.ini', '5AFA01', 'Authoria - Summer/A01_Clear_Summer.ini'),
         ('19FB01', 'Picta - Weathers/00_Master/B01_Lightly_Cloudy.ini', '5AFB01', 'Authoria - Summer/B01_Lightly_Cloudy_Summer.ini'),
         ('19FA03', 'Picta - Weathers/00_Master/A02_Clear_Mist.ini', '5AFA03', 'Authoria - Summer/A02_Clear_Mist_Summer.ini')]
def lab(c): return fm.to_oklab(fm.norm_y(c))
for wm, fmn, ws, fsn in pairs:
    I = {}
    for lane, root in (('P', m.DARK), ('B', m.STAGE)):
        I[lane] = (m.Ini(root + '/enbseries/' + fmn, root + '/enbseries.ini'), m.Ini(root + '/enbseries/' + fsn, root + '/enbseries.ini'))
    print('==', wm, 'vs', ws)
    for h in (7.5, 13.0, 18.5):
        line = []
        for k in ('dome_hor_away', 'dome_zenith', 'fog_far', 'cloud_base', 'sunlight', 'amb_XPlus'):
            g = {}
            for lane in ('P', 'B'):
                a = m.comps(I[lane][0], m.recs(wm, lane == 'B'), h, m.clmt_mid, m.sunz_A)[k]
                b = m.comps(I[lane][1], m.recs(ws, lane == 'B'), h, m.clmt_mid, m.sunz_A)[k]
                g[lane] = float(np.linalg.norm(lab(a) - lab(b)))
            line.append(f'{k} gapP {g["P"]:.4f} gapB {g["B"]:.4f} kept {g["B"] / g["P"] if g["P"] > 1e-4 else float("nan"):.2f}')
        print(f'  {h:5.2f} ' + ' | '.join(line))
