"""Sweep the DirectLightingDesaturation floor D_MIN (zero-channel unlock) -> residual vs target and luminance drift."""
import os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'baby_model.py'), encoding='utf-8').read()
ns = {'__file__': os.path.join(HERE, 'baby_model.py')}
exec(compile(src[:src.index("# ------------------------------------------------------------------ run")], 'bm', 'exec'), ns)
lines = []
for wn in ('A01 Clear', 'C01 Cloudy', 'D02 Heavy Fog', 'D03 Rain Light'):
    W = ns['WEATHERS'][wn]
    I = ns['picta_ini'](W['ini']); R = ns['picta_records'](W['rec']); AI = ns['soul_ini'](W['soul']); AR_ = ns['astra_records'](W['partner'])
    for lp in (False, True):
      for dmin in (0.05, 0.10, 0.20):
          ns['D_MIN'] = dmin; ns['LUMA_PASS'] = lp
          s = ns['solve_sunlight_filter'](I, R, AI, AR_)
          hs = [h for h in ns['HOURS'] if ns['Y'](ns['v_sunlight'](I, R, h)) > 1e-6]
          dE = max(ns['de_ok'](s['vb'](h), s['vt'](h)) for h in hs)
          dY = max(abs(100 * (ns['Y'](s['vb'](h)) / ns['Y'](ns['v_sunlight'](I, R, h)) - 1)) for h in hs)
          dYc = max(abs(100 * (ns['Y'](s['vb'](h)) / ns['Y'](ns['v_sunlight'](I, R, h)) - 1)) for h in hs if 7.0 <= h <= 19.0)
          clamp = sorted({p for p in ns['FREE'] for c in s['DLF'][p] if c >= 9.999})
          lines.append(f"{wn:15s} luma_pass={lp!s:5s} D_MIN={dmin:.2f}  max dE vs target={dE:.3f}  max |dY| 05:30-20:30={dY:5.1f}%  07:00-19:00={dYc:5.1f}%  DLF clamped at 10 in {clamp}")
open(os.path.join(HERE, 'sweep_dmin_out.txt'), 'w').write("\n".join(lines)); print("\n".join(lines))
