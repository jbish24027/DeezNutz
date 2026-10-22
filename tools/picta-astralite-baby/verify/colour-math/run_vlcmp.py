"""Why do installed-value VL numbers differ from the plan? Compare design functions vs this port for one weather/hour."""
import sys, os
sys.dont_write_bytecode = True
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import colour_model as cm
from e11read import E11
D = r'C:\1. AUTHORIA\_tools\picta-astralite-baby\design'
sys.path.insert(0, os.path.join(D, 'final'))
import final_model as fm

REC = cm.load_records(); VOL = cm.load_voli(); WL = cm.weather_files(cm.FORK)
T = cm.T_of(os.path.join(cm.DARK, 'enbseries.ini'))
for w, h in (('19FD06', 18.5), ('19FD06', 7.5), ('19FA01', 7.5), ('19FC05', 13.0)):
    fn = WL[w]
    E_P, _ = fm.parse_ini_E(os.path.join(cm.DARK, 'enbseries', fn.replace('/', os.sep)))
    R = fm.picta_records(w)
    ps = {s: fm.picta_voli(R['_voli'][s]) for s in fm.SLOTS}
    I_, cc, col, dd = fm.voli_at(ps, h)
    L = fm.V_light(E_P, R, h)
    G = fm.ev(E_P, 'GAMEVOLUMETRICRAYS', 'Intensity', h); GF = fm.ev(E_P, 'GAMEVOLUMETRICRAYS', 'ColorFilter', h)
    d_rel = fm.vl_rad(I_, cc, col, L, G, GF) / fm.Y(L)
    X = cm.Ctx(E11(os.path.join(cm.DARK, 'enbseries.ini'), os.path.join(cm.DARK, 'enbseries', fn.replace('/', os.sep))), T)
    o = cm.comps(X, REC['P'][w], h, cm.clmt_mid, cm.PICTA_CL, cm.sunz(h, 7.5, 18.5))
    m_rel, _ = cm.vl(o, REC['P'][w], VOL, h, cm.clmt_mid, cm.PICTA_CL)
    print(w, h, 'design relP %.4f  port relP %.4f' % (d_rel, m_rel), '| L design', np.round(L, 4), 'port', np.round(o['sunlight'], 4),
          '| G', round(float(G), 4), round(o['_gvr_I'], 4), '| GF', np.round(GF, 4), np.round(o['_gvr_F'], 4), '| I cc', I_, cc)
