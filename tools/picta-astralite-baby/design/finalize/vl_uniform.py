"""VL variant 'uniform GVR': ONE GAMEVOLUMETRICRAYS Intensity curve (Dawn..Dusk) shared by all 24 routed files, and all
per-weather scale in per-file, per-slot VOLI copies (K per copy). Alternating least squares with the 1.10 cap.
Kills the GVR x VOLI cross-term in weather transitions; reports reach, cap, crossfade leak, transition swell."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import final2_model as m
from final2_model import *
SL3 = {'Sunrise': 'Sr', 'Day': 'Dy', 'Sunset': 'Ss'}

def build_W(results, D):
    branch = D['VL_BRANCH']; VOL = D['VOL_AMOUNT']; W = []
    for r in results.values():
        E_P, E_B = r['_E_P'], r['_E_B']
        short = r['file'].split('/')[-1].split('_')[0] + ('S' if 'Summer' in r['file'] else '')
        for w in r['weathers']:
            R = r['_RP'][w]; mp = fm.mist_partner(w); AR_ = astra_records(mp); SE = soul_E(AR_['_soul'])
            pslots = {s: fm.picta_voli(R['_voli'][s]) for s in SLOTS}; bslots = {}
            for s in SLOTS:
                if s == 'Night': bslots[s] = pslots['Night']; continue
                v = fm.astra_voli(AR_['_voli'][s]); v['src'] = v['name']; v['rf'] = pslots[s]['rf']
                v['name'] = f"{v['name']}_{short}_{SL3[s]}"; bslots[s] = v
            relA = {}
            for s, hs in dict(Sunrise=7.0, Day=13.0, Sunset=19.0).items():
                v = bslots[s]; LA = V_light(SE, AR_, hs, NAT_TOD, ASTRA_CLMT)
                gA = ev(SE, 'GAMEVOLUMETRICRAYS', 'Intensity', hs, NAT_TOD); gF = ev(SE, 'GAMEVOLUMETRICRAYS', 'ColorFilter', hs, NAT_TOD)
                relA[s] = v['I'] * gA * Y(gF * lerp(LA, v['col'], v['cc'])) / max(Y(LA), 1e-9)
            GN = 0.0 if branch == 'newly_on' else float(E_P['GAMEVOLUMETRICRAYS']['Intensity']['Night'])
            def relP(h, E_P=E_P, R=R, pslots=pslots):
                if branch == 'newly_on': return 0.0
                L = V_light(E_P, R, h); I_, cc, col, dd = fm.voli_at(pslots, h)
                return fm.vl_rad(I_, cc, col, L, ev(E_P, 'GAMEVOLUMETRICRAYS', 'Intensity', h), ev(E_P, 'GAMEVOLUMETRICRAYS', 'ColorFilter', h)) / max(Y(L), 1e-9)
            def target(h, relA=relA, relP=relP):
                c = clmt_weights(h); rp = relP(h)
                return max(VOL * sum(c[s] * relA[s] for s in RSLOTS) + c['Night'] * rp, rp)
            W.append(dict(file=r['file'], w=w, E_P=E_P, E_B=E_B, R=R, pslots=pslots, bslots=bslots, relA=relA, relP=relP, target=target, GN=GN, partner=mp))
    return W

def solve_vl_uniform(results, D):
    W = build_W(results, D); CAP = 1.10; LAM = 0.02
    names = sorted({wd['bslots'][s]['name'] for wd in W for s in RSLOTS}); ix = {n: i for i, n in enumerate(names)}
    GP = {p: float(np.median([wd['E_P']['GAMEVOLUMETRICRAYS']['Intensity'][p] for wd in W])) for p in FREE}
    def GF_B(wd, h):
        w = tod_weights(h); gf = wd['E_P']['GAMEVOLUMETRICRAYS']['ColorFilter']
        return sum(w[p] * (Y(gf[p]) * np.ones(3) if p in FREE else gf[p]) for p in TODP)
    cache = {}
    def pieces(wd, h):
        key = (wd['w'], h)
        if key in cache: return cache[key]
        c = clmt_weights(h); L = V_light(wd['E_B'], wd['R'], h)
        cc = sum(c[s] * wd['bslots'][s]['cc'] for s in SLOTS); col = sum(c[s] * wd['bslots'][s]['col'] for s in SLOTS)
        f = Y(GF_B(wd, h) * lerp(L, col, cc)) / max(Y(L), 1e-9); w = tod_weights(h)
        kc = np.zeros(len(names))
        for s in RSLOTS: kc[ix[wd['bslots'][s]['name']]] += c[s] * wd['bslots'][s]['I'] * f
        night = c['Night'] * wd['bslots']['Night']['I'] * f
        cache[key] = (kc, night, w); return cache[key]
    def rad(wd, h, K, G):
        kc, night, w = pieces(wd, h)
        g = sum(w[p] * G[p] for p in FREE) + w['Night'] * wd['GN']
        return (kc @ K + night) * g
    K = np.ones(len(names)) * 1.0; G = dict(GP); capw = {}
    for it in range(40):
        # K step (G fixed)
        rows, rhs = [], []
        for wd in W:
            for h in FIT_H:
                t = wd['target'](h)
                if t <= 1e-6: continue
                kc, night, w = pieces(wd, h); g = sum(w[p] * G[p] for p in FREE) + w['Night'] * wd['GN']
                if not kc.any(): continue
                wg = capw.get((wd['w'], h), 1.0); tt = t * CAP / 1.02 if wg > 1 else t
                rows.append(wg * kc * g / t); rhs.append(wg * (tt - night * g) / t)
        K, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None); K = np.clip(K, 0.0, None)
        # G step (K fixed): one curve for every file
        rows, rhs = [], []
        for wd in W:
            for h in FIT_H:
                t = wd['target'](h)
                if t <= 1e-6: continue
                kc, night, w = pieces(wd, h); a = kc @ K + night
                if a <= 1e-9: continue
                wg = capw.get((wd['w'], h), 1.0); tt = t * CAP / 1.02 if wg > 1 else t
                rows.append([wg * a * w[p] / t for p in FREE]); rhs.append(wg * (tt - a * w['Night'] * wd['GN']) / t)
        for i, p in enumerate(FREE):
            r = [0.0] * 5; r[i] = LAM / max(GP[p], 0.1); rows.append(r); rhs.append(LAM * GP[p] / max(GP[p], 0.1))
        x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
        G = {p: float(np.clip(x[i], 0.0, 1000.0)) for i, p in enumerate(FREE)}
        if it >= 8:
            worst = 0.0
            for wd in W:
                for h in FIT_H:
                    t = wd['target'](h)
                    if t <= 1e-6: continue
                    q = rad(wd, h, K, G) / t; worst = max(worst, q)
                    if q > CAP: capw[(wd['w'], h)] = capw.get((wd['w'], h), 1.0) * 3.0
            if worst <= CAP + 1e-3: break
    rep = {}
    for wd in W:
        over = (0, None); leak = (0, None)
        for h in AUDIT_H:
            t = wd['target'](h); rr = rad(wd, h, K, G)
            if t > 1e-6:
                if rr / t > over[0]: over = (round(rr / t, 3), h)
            elif rr > leak[0]: leak = (round(rr, 3), h)
        pk = {hh: round(rad(wd, hh, K, G) / max(wd['target'](hh), 1e-9), 2) for hh in (7.5, 13.0, 18.5)}
        xp = {hh: (round(rad(wd, hh, K, G) / wd['relP'](hh), 2) if wd['relP'](hh) > 1e-6 else None) for hh in (7.5, 13.0, 18.5)}
        rep[wd['w']] = dict(reached=pk, intensity_only_x_picta=xp, max_over=over, leak=leak, voli={s: wd['bslots'][s]['name'] for s in RSLOTS})
    Kd = {n: float(K[ix[n]]) for n in names}
    copies = {}
    for wd in W:
        for s in RSLOTS:
            v = wd['bslots'][s]; copies[v['name']] = dict(source=v['formid'], src=v['src'], intensity=round(Kd[v['name']] * v['I'], 3), rf=v['rf'], dens=v['dens'], cc=v['cc'])
    return dict(G={p: round(G[p], 3) for p in FREE}, G_picta=GP, K=Kd, copies=copies, per_weather=rep, _W=W, _G=G, _Kv=K, _rad=rad,
                worst=max((d['max_over'][0], w) for w, d in rep.items()), leak=max((d['leak'][0], w, d['leak'][1]) for w, d in rep.items()))

def transition(V, pairs, hours=(7.5, 13.0, 18.5)):
    Wd = {wd['w']: wd for wd in V['_W']}; K = V['K']; G = V['_G']; out = {}
    def parts(w, h, lane):
        wd = Wd[w]; sl = wd['bslots'] if lane == 'baby' else wd['pslots']
        c = clmt_weights(h); I_ = sum(c[s] * sl[s]['I'] * (K.get(sl[s]['name'], 1.0) if (lane == 'baby' and s != 'Night') else 1.0) for s in SLOTS)
        cc = sum(c[s] * sl[s]['cc'] for s in SLOTS); col = sum(c[s] * sl[s]['col'] for s in SLOTS)
        L = V_light(wd['E_B'] if lane == 'baby' else wd['E_P'], wd['R'], h); w_ = tod_weights(h)
        g = (sum(w_[p] * G[p] for p in FREE) + w_['Night'] * wd['GN']) if lane == 'baby' else ev(wd['E_P'], 'GAMEVOLUMETRICRAYS', 'Intensity', h)
        return I_, cc, col, L, g
    for a, b in pairs:
        for h in hours:
            for lane in ('picta', 'baby'):
                Ia, cca, cola, La, ga = parts(a, h, lane); Ib, ccb, colb, Lb, gb = parts(b, h, lane)
                ra = Ia * ga * Y(lerp(La, cola, cca)); rb = Ib * gb * Y(lerp(Lb, colb, ccb))
                run = (Ia + Ib) / 2 * (ga + gb) / 2 * Y(lerp((La + Lb) / 2, (cola + colb) / 2, (cca + ccb) / 2))
                out[f'{a}<->{b} {h:g} {lane}'] = dict(vs_ideal=round(100 * (run / max((ra + rb) / 2, 1e-12) - 1), 1), vs_brighter_end=round(100 * (run / max(ra, rb, 1e-12) - 1), 1))
    return out

PAIRS = [('19FA01', '19FD03'), ('19FE03', '19FD03'), ('19FE01', '19FD02'), ('19FA01', '19FC01'), ('19FC01', '19FC04'), ('19FA01', '19FE03'), ('19FA01', '19FE05'), ('19FC01', '19FD05'), ('19FB01', '19FB03')]
if __name__ == '__main__':
    D = m.dials(); res = m.run_all(D)
    OUT = {}
    for amt in (0.5, 1.0):
        for br in ('alive', 'newly_on'):
            Dv = m.dials(); Dv['VOL_AMOUNT'] = amt; Dv['VL_BRANCH'] = br
            V = solve_vl_uniform(res, Dv); TR = transition(V, PAIRS)
            sw = max((v['vs_brighter_end'], k) for k, v in TR.items() if k.endswith('baby'))
            swi = max((abs(v['vs_ideal']), k) for k, v in TR.items() if k.endswith('baby'))
            print(f'== uniform amount {amt} {br}: G {V["G"]} (picta {V["G_picta"]}) worst over {V["worst"]} leak {V["leak"]} swell above brighter end {sw} | worst vs ideal {swi}', flush=True)
            for w in ('19FA01', '19FA02', '19FA03', '19FB03', '19FC01', '19FC04', '19FD02', '19FD03', '19FE03', '19FE05', '5AFA01'):
                print('   ', w, V['per_weather'][w]['reached'], 'x Picta (intensity only)', V['per_weather'][w]['intensity_only_x_picta'], flush=True)
            ii = [c['intensity'] for c in V['copies'].values()]
            print('    copies', len(V['copies']), 'intensity min/median/max', min(ii), float(np.median(ii)), max(ii), flush=True)
            OUT[f'{amt}_{br}'] = dict(G=V['G'], worst=V['worst'], leak=V['leak'], swell=TR, per_weather=V['per_weather'], copies=V['copies'])
    json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vl_uniform.json'), 'w'), indent=1, default=m.conv)
