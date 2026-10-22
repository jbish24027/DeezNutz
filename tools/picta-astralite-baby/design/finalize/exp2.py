import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import final2_model as m
fn = 'Picta - Weathers/00_Master/A01_Clear.ini'
for tag, kw in (('cfs.5', dict(WL_SCAT=100.0, WL_SCAT_SUN=100.0)), ('cfs0', dict(CFS_SHARE=0.0, WL_SCAT=100.0, WL_SCAT_SUN=100.0)),
                ('cfs.25', dict(CFS_SHARE=0.25, WL_SCAT=100.0, WL_SCAT_SUN=100.0))):
    D = m.dials(); D.update(kw)
    r = m.solve_file(fn, D)
    ht = m.hue_table(r, '19FA01', hours=(7.5, 18.5), comps=('dome_hor_sun', 'cloud_sunlit'))
    for h, row in ht.items():
        print(tag, h, ' | '.join(f"{cn}: {v['picta']} -> {v['baby']} [{v['astralite']}] s={v['share']} dY {v['dY_pct']}" for cn, v in row.items()), flush=True)
    worst, _ = m.audit_weather(r, '19FA01', hours=[5.0 + 0.25 * i for i in range(67)])
    print(tag, 'scat_at_sun', worst['scat_at_sun'], 'scat_hor', worst['scat_horizon_sunward'], 'dome_hor_sun', worst['dome_hor_sun'], flush=True)
