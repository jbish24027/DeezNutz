"""experiments: WL_SCAT_SUN, hue window, WL_ALB, cloud mean row - on A01, C01, D02, E05."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import final2_model as m
FILES = {'A01': 'Picta - Weathers/00_Master/A01_Clear.ini', 'C01': 'Picta - Weathers/00_Master/C01_Cloudy.ini',
         'D02': 'Picta - Weathers/00_Master/D02_Overcast_Heavy_Fog.ini', 'E05': 'Picta - Weathers/00_Master/E05_Storm_Snow_Heavy.ini'}
WID = {'A01': '19FA01', 'C01': '19FC01', 'D02': '19FD02', 'E05': '19FE05'}
KEYS = ['cloud_sunlit', 'cloud_lit', 'cloud_edge', 'scat_at_sun', 'scat_horizon_sunward', 'dome_hor_sun', 'dome_toward_sun_20', 'clouds', 'band_hor', 'fog_far', 'sunlight', 'amb_XPlus']
def run(tag, files=None, **kw):
    D = m.dials(); D.update(kw); t0 = time.time(); out = {}
    for k, fn in FILES.items():
        if files and k not in files: continue
        r = m.solve_file(fn, D); w = WID[k]
        worst, _ = m.audit_weather(r, w, hours=[5.0 + 0.25 * i for i in range(67)])
        surf = max((abs(v[0]), cn) for cn, v in worst.items() if cn.startswith('surf_'))
        st = m.ab_steps(r, w)
        exc = max((v['baby_max_step'] - v['picta_max_step'], cn, v['baby_at']) for cn, v in st.items())
        hues = {}
        for hh in (7.25, 7.5, 18.75):
            a = m.components(r['_E_P'], r['_RP'][w], hh, light=True); b = m.components(r['_E_B'], r['_RB'][w], hh, light=True)
            for cn in ('dome_hor_away', 'fog_far', 'clouds', 'amb_XPlus'):
                hues[f'{cn}@{hh}'] = (round(m.lch(a[cn])[2]), round(m.lch(b[cn])[2]), round(m.lch(b[cn])[1], 3))
        out[k] = dict(worst={kk: worst[kk][0] for kk in KEYS if kk in worst}, surf=surf, step_excess=exc, hues=hues, alpha=r['alpha_used'])
    print(f'--- {tag} {kw} ({time.time() - t0:.0f}s)', flush=True)
    for k, v in out.items():
        print(f'  {k} ' + ' '.join(f'{kk}={vv:+.2f}' for kk, vv in v['worst'].items()) + f' | surf {v["surf"][0]:.2f} {v["surf"][1]} | step+ {v["step_excess"][0]:.3f} {v["step_excess"][1]}@{v["step_excess"][2]}', flush=True)
        print('       ' + ' '.join(f'{kk}:{vv[0]}->{vv[1]}/{vv[2]}' for kk, vv in v['hues'].items()), flush=True)
    return out
CFGS = {'base': {}, 'scatsun100': dict(WL_SCAT_SUN=100.0), 'scat100both': dict(WL_SCAT=100.0, WL_SCAT_SUN=100.0),
        'scat400both': dict(WL_SCAT=400.0, WL_SCAT_SUN=400.0),
        'hue140_175': dict(HUE_LO=140.0, HUE_HI=175.0), 'hue120_170': dict(HUE_LO=120.0, HUE_HI=170.0),
        'alb0': dict(WL_ALB=0.0), 'alb10': dict(WL_ALB=10.0), 'cmean3': dict(WL_CLOUD_MEAN=3.0), 'cfs0': dict(CFS_SHARE=0.0), 'sunCW0': dict(CW_SCAT_SUN=0.0),
        'it12d5': dict(SCAT_ITERS=14, SCAT_DAMP=0.5), 'w100': dict(WL_SCAT=100.0, WL_SCAT_SUN=100.0), 'cmean10': dict(WL_CLOUD_MEAN=10.0), 'purearc': dict(HUE_LO=179.0, HUE_HI=180.0), 'hue90_150': dict(HUE_LO=90.0, HUE_HI=150.0), 'alb2': dict(WL_ALB=2.0), 'alb20': dict(WL_ALB=20.0), 'cmean20': dict(WL_CLOUD_MEAN=20.0)}
if __name__ == '__main__':
    args = sys.argv[1:]
    files = None
    if args and args[0].startswith('files='): files = args[0][6:].split(','); args = args[1:]
    for k in (args or list(CFGS)):
        if '+' in k:
            kw = {}
            for part in k.split('+'): kw.update(CFGS[part])
            run(k, files, **kw)
        else: run(k, files, **CFGS[k])
