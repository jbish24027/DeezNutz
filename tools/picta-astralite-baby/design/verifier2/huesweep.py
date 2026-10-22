import sys, os, numpy as np, importlib.util
sys.path.insert(0, os.path.abspath('../final'))
import final_model as fm
spec = importlib.util.spec_from_file_location('m', 'indep_model.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def lc(c):
    L, C, h = fm.lch(c); return h, C
for fn, ids in m.FILES.items():
    w = ids[0]
    iP = m.Ini(m.DARK + '/enbseries/' + fn, m.DARK + '/enbseries.ini'); iB = m.Ini(m.STAGE + '/enbseries/' + fn, m.STAGE + '/enbseries.ini')
    RP, RB = m.recs(w, False), m.recs(w, True)
    out = []
    for h in (7.25, 18.75):
        a = m.comps(iP, RP, h, m.clmt_mid, m.sunz_A); b = m.comps(iB, RB, h, m.clmt_mid, m.sunz_A)
        for k in ('dome_hor_away', 'fog_far', 'cloud_base', 'amb_XPlus'):
            hp, cp = lc(a[k]); hb, cb = lc(b[k]); dh = ((hb - hp + 180) % 360) - 180
            out.append(f'{k[:8]}@{h}: {hp:4.0f}/{cp:.3f}->{hb:4.0f}/{cb:.3f} (dh {dh:+4.0f})')
    print(w, fn.split('/')[-1][:24].ljust(24), ' | '.join(out))
