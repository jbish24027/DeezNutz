"""VL variant 'fixed GVR': Picta's GAMEVOLUMETRICRAYS Intensity stays (uniform across routed files), all per-weather scale
moves into per-file VOLI copies (one K per file x source VOLI x range group). Removes the GVR x VOLI transition cross-term
and leaves Picta's crossfade VL exactly as it is. Reports reach, cap, crossfade leak and the transition swell."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import final2_model as m
from final2_model import *

def solve_vl_fixed(results, D):
    branch = D['VL_BRANCH']; VOL = D['VOL_AMOUNT']; CAP = 1.10
    W = []
    for r in results.values():
        E_P, E_B = r['_E_P'], r['_E_B']
        short = r['file'].split('/')[-1].split('_')[0] + ('S' if 'Summer' in r['file'] else '')
        for w in r['weathers']:
            R = r['_RP'][w]; mp = fm.mist_partner(w); AR_ = astra_records(mp); SE = soul_E(AR_['_soul'])
            pslots = {s: fm.picta_voli(R['_voli'][s]) for s in SLOTS}
            bslots = {}
            for s in SLOTS:
                if s == 'Night': bslots[s] = pslots['Night']; continue
                v = fm.astra_voli(AR_['_voli'][s]); v['src'] = v['name']; v['rf'] = pslots[s]['rf']
                v['name'] = f"{v['name']}_{short}" + ('_R80' if v['rf'] == 80 and v['src'] in m.MIXED_RF else ''); bslots[s] = v
            relA = {}
            for s, hs in dict(Sunrise=7.0, Day=13.0, Sunset=19.0).items():
                v = bslots[s]; LA = V_light(SE, AR_, hs, NAT_TOD, ASTRA_CLMT)
                gA = ev(SE, 'GAMEVOLUMETRICRAYS', 'Intensity', hs, NAT_TOD); gF = ev(SE, 'GAMEVOLUMETRICRAYS', 'ColorFilter', hs, NAT_TOD)
                relA[s] = v['I'] * gA * Y(gF * lerp(LA, v['col'], v['cc'])) / max(Y(LA), 1e-9)
            def G_of(h, E_P=E_P):
                g = ev(E_P, 'GAMEVOLUMETRICRAYS', 'Intensity', h)
                if branch == 'newly_on':
                    w_ = tod_weights(h); g = g - w_['Night'] * E_P['GAMEVOLUMETRICRAYS']['Intensity']['Night']
                return g
            def relP(h, E_P=E_P, R=R, pslots=pslots):
                if branch == 'newly_on': return 0.0
                L = V_light(E_P, R, h); I_, cc, col, dd = fm.voli_at(pslots, h)
                return fm.vl_rad(I_, cc, col, L, ev(E_P, 'GAMEVOLUMETRICRAYS', 'Intensity', h), ev(E_P, 'GAMEVOLUMETRICRAYS', 'ColorFilter', h)) / max(Y(L), 1e-9)
            def target(h, relA=relA, relP=relP):
                c = clmt_weights(h); rp = relP(h)
                return max(VOL * sum(c[s] * relA[s] for s in RSLOTS) + c['Night'] * rp, rp)
            W.append(dict(file=r['file'], w=w, E_P=E_P, E_B=E_B, R=R, pslots=pslots, bslots=bslots, relA=relA, relP=relP, target=target, G=G_of, partner=mp))
    names = sorted({wd['bslots'][s]['name'] for wd in W for s in RSLOTS}); ix = {n: i for i, n in enumerate(names)}
    def GF_B(wd, h):
        w = tod_weights(h); gf = wd['E_P']['GAMEVOLUMETRICRAYS']['ColorFilter']
        return sum(w[p] * (Y(gf[p]) * np.ones(3) if p in FREE else gf[p]) for p in TODP)
    def basis(wd, h):
        """rad = sum_n coef_n * K_n + const"""
        c = clmt_weights(h); L = V_light(wd['E_B'], wd['R'], h)
        cc = sum(c[s] * wd['bslots'][s]['cc'] for s in SLOTS); col = sum(c[s] * wd['bslots'][s]['col'] for s in SLOTS)
        f = wd['G'](h) * Y(GF_B(wd, h) * lerp(L, col, cc)) / max(Y(L), 1e-9)
        coef = np.zeros(len(names))
        for s in RSLOTS: coef[ix[wd['bslots'][s]['name']]] += c[s] * wd['bslots'][s]['I'] * f
        return coef, c['Night'] * wd['bslots']['Night']['I'] * f
    capw = {}
    for it in range(25):
        rows, rhs = [], []
        for wd in W:
            for h in FIT_H:
                t = wd['target'](h)
                if t <= 1e-6: continue
                coef, k0 = basis(wd, h)
                if not coef.any(): continue
                wg = capw.get((wd['w'], h), 1.0); tt = t * CAP / 1.02 if wg > 1 else t
                rows.append(wg * coef / t); rhs.append(wg * (tt - k0) / t)
        K, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None); K = np.clip(K, 0, None)
        worst = 0.0
        for wd in W:
            for h in FIT_H:
                t = wd['target'](h)
                if t <= 1e-6: continue
                coef, k0 = basis(wd, h); q = (coef @ K + k0) / t; worst = max(worst, q)
                if q > CAP: capw[(wd['w'], h)] = capw.get((wd['w'], h), 1.0) * 3.0
        if worst <= CAP + 1e-3: break
    rep = {}; Kd = {n: float(K[ix[n]]) for n in names}
    for wd in W:
        over = (0, None); leak = (0, None); pk = {}
        for h in AUDIT_H:
            t = wd['target'](h); coef, k0 = basis(wd, h); rad = coef @ K + k0
            if t > 1e-6:
                if rad / t > over[0]: over = (round(rad / t, 3), h)
            elif rad > leak[0]: leak = (round(rad, 3), h)
        for hh in (7.5, 13.0, 18.5):
            coef, k0 = basis(wd, hh); pk[hh] = round((coef @ K + k0) / max(wd['target'](hh), 1e-9), 2)
        rep[wd['w']] = dict(reached=pk, max_over=over, leak=leak)
    copies = {}
    for wd in W:
        for s in RSLOTS:
            v = wd['bslots'][s]; copies[v['name']] = dict(source=v['formid'], src=v['src'], intensity=round(Kd[v['name']] * v['I'], 3), rf=v['rf'])
    return dict(K=Kd, copies=copies, per_weather=rep, _W=W, worst=max((d['max_over'][0], w) for w, d in rep.items()),
                leak=max((d['leak'][0], w, d['leak'][1]) for w, d in rep.items()))

def transition(V, pairs, hours=(7.5, 13.0, 18.5)):
    Wd = {wd['w']: wd for wd in V['_W']}; K = V['K']; out = {}
    def parts(w, h, lane):
        wd = Wd[w]; sl = wd['bslots'] if lane == 'baby' else wd['pslots']
        c = clmt_weights(h); I_ = sum(c[s] * sl[s]['I'] * (K.get(sl[s]['name'], 1.0) if (lane == 'baby' and s != 'Night') else 1.0) for s in SLOTS)
        cc = sum(c[s] * sl[s]['cc'] for s in SLOTS); col = sum(c[s] * sl[s]['col'] for s in SLOTS)
        L = V_light(wd['E_B'] if lane == 'baby' else wd['E_P'], wd['R'], h)
        g = wd['G'](h) if lane == 'baby' else ev(wd['E_P'], 'GAMEVOLUMETRICRAYS', 'Intensity', h)
        return I_, cc, col, L, g
    for a, b in pairs:
        for h in hours:
            for lane in ('picta', 'baby'):
                Ia, cca, cola, La, ga = parts(a, h, lane); Ib, ccb, colb, Lb, gb = parts(b, h, lane)
                ra = Ia * ga * Y(lerp(La, cola, cca)); rb = Ib * gb * Y(lerp(Lb, colb, ccb))
                run = (Ia + Ib) / 2 * (ga + gb) / 2 * Y(lerp((La + Lb) / 2, (cola + colb) / 2, (cca + ccb) / 2))
                out[f'{a}<->{b} {h:g} {lane}'] = (round(100 * (run / max((ra + rb) / 2, 1e-12) - 1), 1), round(100 * (run / max(ra, rb, 1e-12) - 1), 1))
    return out

if __name__ == '__main__':
    D = m.dials(); res = m.run_all(D)
    PAIRS = [('19FA01', '19FD03'), ('19FE03', '19FD03'), ('19FE01', '19FD02'), ('19FA01', '19FC01'), ('19FC01', '19FC04'), ('19FA01', '19FE03'), ('19FA01', '19FE05'), ('19FC01', '19FD05')]
    OUT = {}
    for amt in (0.5, 1.0):
        for br in ('alive', 'newly_on'):
            Dv = m.dials(); Dv['VOL_AMOUNT'] = amt; Dv['VL_BRANCH'] = br
            V = solve_vl_fixed(res, Dv); TR = transition(V, PAIRS)
            sw = max((v[1], k) for k, v in TR.items() if k.endswith('baby'))
            print(f'== fixedG amount {amt} {br}: worst over {V["worst"]} leak {V["leak"]} worst swell above brighter end {sw}', flush=True)
            for w in ('19FA01', '19FA03', '19FB03', '19FC01', '19FD02', '19FD03', '19FE03', '19FE05', '5AFA01'):
                print('   ', w, V['per_weather'][w]['reached'], flush=True)
            print('    copies', len(V['copies']), 'intensity range', min(c['intensity'] for c in V['copies'].values()), max(c['intensity'] for c in V['copies'].values()), flush=True)
            OUT[f'{amt}_{br}'] = dict(worst=V['worst'], leak=V['leak'], swell=TR, per_weather=V['per_weather'], copies=V['copies'])
    json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vl_fixedg.json'), 'w'), indent=1, default=m.conv)
