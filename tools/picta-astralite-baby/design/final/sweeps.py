"""MIX sweep (tone, set once), KAPPA amplitude demo, donor variant (family for achromatic partners). Writes sweeps.json/.txt."""
import sys, json, os
sys.argv = ["x"]; sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import final_model as M, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
F = {'19FA01': 'Picta - Weathers/00_Master/A01_Clear.ini', '19FC01': 'Picta - Weathers/00_Master/C01_Cloudy.ini',
     '19FD02': 'Picta - Weathers/00_Master/D02_Overcast_Heavy_Fog.ini', '19FD03': 'Picta - Weathers/00_Master/D03_Overcast_Rain_Light.ini',
     '19FE03': 'Picta - Weathers/00_Master/E03_Storm_Rain_Heavy_Thunder.ini'}
OUT = {}; L = []
def P(s=''): L.append(s); print(s, flush=True)
def worst_luma(r, w):
    worst, nm = M.audit_weather(r, w); return max(abs(v[0]) for k, v in worst.items() if k != 'scat_sunward'), worst.get('scat_sunward', [0])[0], nm
comps = ('dome_hor_away', 'dome_hor_sun', 'fog_far', 'clouds', 'amb_XPlus', 'sunlight')
for lvl, mix in (('Light', (0.35, 0.20, 0.35)), ('Medium', (0.50, 0.30, 0.50)), ('Strong', (0.75, 0.45, 0.75))):
    D = M.default_dials(); D['MIX'] = dict(Sunrise=mix[0], Day=mix[1], Sunset=mix[2])
    P(f'== MIX {lvl} {mix}')
    for w in ('19FA01', '19FC01', '19FD03'):
        r = M.solve_file(F[w], D); ht = M.hue_table(r, w, hours=(7.5, 13.0, 18.5), comps=comps); wl, ws, nm = worst_luma(r, w)
        OUT[f'{lvl} {w}'] = dict(hues=ht, worst_luma_pct=wl, scat_colour_pct=ws, night=nm)
        P(f'  {w}: worst visible |dY| {wl:.2f}% (scatter colour term {ws:+.2f}%), night diff {nm:.1e}')
        for h, row in ht.items():
            P(f'    {h:5.2f} ' + ' | '.join(f'{c} {row[c]["picta"].split(" ",1)[1]} -> {row[c]["baby"]} s={row[c]["share"]}' for c in comps))
D = M.default_dials(); D['KAPPA'] = dict(D['KAPPA'], fog=0.6, sky=0.6)
P('== KAPPA demo: sky 0.6, fog 0.6 (amplitude only) A01 vs default')
r1 = M.solve_file(F['19FA01'], M.default_dials()); r2 = M.solve_file(F['19FA01'], D)
for h in (7.5, 18.5):
    a = M.components(r1['_E_B'], r1['_RB']['19FA01'], h); b = M.components(r2['_E_B'], r2['_RB']['19FA01'], h)
    for c in ('dome_hor_away', 'fog_far'):
        La, Ca, ha = M.lch(a[c]); Lb, Cb, hb = M.lch(b[c])
        P(f'   {h} {c}: default h{ha:.1f} C{Ca:.3f} -> kappa0.6 h{hb:.1f} C{Cb:.3f} (chroma x{Cb/Ca:.2f}, hue shift {abs(((hb-ha+180)%360)-180):.1f} deg, Y ratio {M.Y(b[c])/M.Y(a[c]):.4f})')
        OUT[f'kappa {h} {c}'] = dict(default=[ha, Ca], kappa06=[hb, Cb], Y_ratio=M.Y(b[c]) / M.Y(a[c]))
P('== DONOR variant: family mix for achromatic canonical partners (rain/fog) vs canonical, Medium')
for w in ('19FD03', '19FD02', '19FE03'):
    for mode in ('canonical', 'family_achromatic'):
        D = M.default_dials(); D['DONOR'] = mode
        r = M.solve_file(F[w], D); ht = M.hue_table(r, w, hours=(7.5, 13.0), comps=('dome_hor_away', 'fog_far', 'amb_XPlus', 'clouds'))
        wl, ws, nm = worst_luma(r, w)
        OUT[f'donor {mode} {w}'] = dict(members=r['donor_members'], hues=ht, worst_luma_pct=wl)
        P(f'  {w} {mode} members={ {k: round(v, 2) for k, v in list(r["donor_members"].items())[:5]} } worst |dY| {wl:.2f}%')
        for h, row in ht.items():
            P(f'    {h:5.2f} ' + ' | '.join(f'{c} {row[c]["picta"].split(" ",1)[1]} -> {row[c]["baby"]}' for c in row))
json.dump(OUT, open(os.path.join(HERE, 'sweeps.json'), 'w'), indent=1, default=M.conv)
open(os.path.join(HERE, 'sweeps.txt'), 'w', encoding='utf-8').write('\n'.join(L))
