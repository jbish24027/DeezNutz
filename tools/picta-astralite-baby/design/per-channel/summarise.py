"""Compact evidence table from baby_model_out.json: per weather, per period peak, per channel: Picta -> baby (OKLCh hue, chroma, Y change)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, 'baby_model_out.json'), encoding='utf-8'))
PK = {7.25: 'Dawn', 9.0: 'Sunrise', 13.0: 'Day', 17.0: 'Sunset', 18.75: 'Dusk'}
CH = ['sky zenith', 'sky horizon (away from sun)', 'sunward horizon pixel (information: dome x AirGlow mixed with S)',
      'cloud base colour', 'fog far colour', 'direct sunlight [filter carrier] <- CHOSEN', 'ambient DALC DirectionalXPlus']
SHORT = {CH[0]: 'zenith', CH[1]: 'horizon', CH[2]: 'sunward', CH[3]: 'clouds', CH[4]: 'fog', CH[5]: 'sunlight', CH[6]: 'ambientX+'}
out = []
for wn, W in d['weathers'].items():
    out.append(f'== {wn}  (period alpha {W.get("period_alpha")})')
    stats = []
    for ch in CH:
        rows = W['eval'].get(ch)
        if not rows: continue
        cells = []
        for r in rows:
            if r['h'] in PK:
                cells.append(f"{PK[r['h']][:4]} h{r['picta']['h']:.0f}->{r['baby']['h']:.0f} C{r['picta']['C']:.3f}->{r['baby']['C']:.3f} dY{r['dY_pct']:+.1f}%")
        mx = max(abs(r['dY_pct']) for r in rows); mh = max(r['hue_err_vs_target'] for r in rows); me = max(r.get('dE', 0) for r in rows)
        out.append(f'  {SHORT[ch]:9s} | ' + ' | '.join(cells))
        stats.append(f'{SHORT[ch]} max|dY|={mx:.1f}% max hue err vs target={mh:.1f} max dE={me:.3f}')
    out.append('  residuals (all report hours 06:30-19:45): ' + '; '.join(stats))
    out.append('  identity (mix=0) max dE: ' + json.dumps({k: v for k, v in W['identity_max_dE'].items() if not k.startswith(('sunlight[rec', 'sunlight[ini', 'sunlight[hyb'))}))
    v = W.get('voli')
    if v: out.append('  VOLI slots ' + json.dumps(v['slots']) + ' GVR Intensity ' + json.dumps({k: round(x, 2) for k, x in v['GVR'].items()}))
s = '\n'.join(out); open(os.path.join(HERE, 'summary_out.txt'), 'w', encoding='utf-8').write(s); print(s)
