import os
d = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(d, 'final2_model.py'); s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:90]
    s = s.replace(old, new)
# VL transition: three lanes, and run vs the brighter endpoint
rep('''def vl_transition(vl, pairs, hours=(7.5, 13.0, 18.5)):''', '''def voli_at_C(sl, h, C, K=None):
    c = clmt_weights(h, C); I_ = cc = 0.0; col = np.zeros(3)
    for s_ in SLOTS:
        v = sl[s_]; k = (K.get(v['name'], 1.0) if (K is not None and s_ != 'Night') else 1.0)
        I_ += c[s_] * v['I'] * k; cc += c[s_] * v['cc']; col = col + c[s_] * v['col']
    return I_, cc, col
def vl_transition3(vl, pairs, hours=(7.5, 13.0, 18.5)):
    """weather transition at t=0.5: engine lerps VOLI + sunlight records, E11 lerps GVR. Lanes picta / baby / astralite (own clocks).
    Reports runtime/ideal-1 and runtime/brighter-endpoint-1 (a swell above both endpoints is what the eye would see)."""
    W = {wd['w']: wd for wd in vl['_W']}; G = vl['_G']; GN = vl['_GN']; K = vl['_K']; out = {}
    def parts(w, h, lane):
        wd = W[w]
        if lane == 'astralite':
            AR_ = astra_records(wd['partner']); SE = soul_E(AR_['_soul'])
            sl = {s_: (fm.astra_voli(AR_['_voli'][s_]) if AR_['_voli'].get(s_) else wd['pslots'][s_]) for s_ in SLOTS}
            I_, cc, col = voli_at_C(sl, h, ASTRA_CLMT); L = V_light(SE, AR_, h, NAT_TOD, ASTRA_CLMT)
            g = ev(SE, 'GAMEVOLUMETRICRAYS', 'Intensity', h, NAT_TOD); return I_, cc, col, L, g
        sl = wd['bslots'] if lane == 'baby' else wd['pslots']
        I_, cc, col = voli_at_C(sl, h, PICTA_CLMT, K if lane == 'baby' else None)
        L = V_light(wd['E_B'] if lane == 'baby' else wd['E_P'], wd['R'], h)
        w_ = tod_weights(h)
        g = (sum(w_[p] * G[wd['file']][p] for p in FREE) + w_['Night'] * GN[wd['file']]) if lane == 'baby' else ev(wd['E_P'], 'GAMEVOLUMETRICRAYS', 'Intensity', h)
        return I_, cc, col, L, g
    for a, b in pairs:
        for h in hours:
            for lane in ('picta', 'baby', 'astralite'):
                Ia, cca, cola, La, ga = parts(a, h, lane); Ib, ccb, colb, Lb, gb = parts(b, h, lane)
                ra = Ia * ga * Y(lerp(La, cola, cca)); rb = Ib * gb * Y(lerp(Lb, colb, ccb))
                run = (Ia + Ib) / 2 * (ga + gb) / 2 * Y(lerp((La + Lb) / 2, (cola + colb) / 2, (cca + ccb) / 2))
                out[f'{a}<->{b} {h:g} {lane}'] = dict(vs_ideal=round(100 * (run / max((ra + rb) / 2, 1e-12) - 1), 1),
                                                     vs_brighter_end=round(100 * (run / max(ra, rb, 1e-12) - 1), 1))
    return out
def vl_transition(vl, pairs, hours=(7.5, 13.0, 18.5)):''')
rep('''    TR = vl_transition(VLR[(0.5, 'alive')], [('19FA01', '19FD03'), ('19FE03', '19FD03'), ('19FE01', '19FD02'), ('19FA01', '19FC01')])
    P('== VL TRANSITION cross-term at t=0.5 (runtime vs ideal, %): ' + json.dumps(TR))''',
'''    TR = vl_transition3(VLR[(0.5, 'alive')], [('19FA01', '19FD03'), ('19FE03', '19FD03'), ('19FE01', '19FD02'), ('19FA01', '19FC01'), ('19FC01', '19FC04'), ('19FA01', '19FE03')])
    P('== VL TRANSITION at t=0.5, % (vs ideal lerp / vs brighter endpoint), lanes picta | baby | astralite:')
    for k in sorted({kk.rsplit(' ', 1)[0] for kk in TR}):
        P('   ' + k + ': ' + ' | '.join(f"{ln} {TR[k + ' ' + ln]['vs_ideal']:+.0f}/{TR[k + ' ' + ln]['vs_brighter_end']:+.0f}" for ln in ('picta', 'baby', 'astralite')))''')
# flip detector: chroma-weighted steps for all weathers
rep('''    HS = {}
    for fn, r in res.items():
        for w in r['weathers']: HS[w] = hue_steps(r, w)
    worst_excess = sorted(((v['baby_max_step_deg'] - v['picta_max_step_deg'], w, cn, v) for w, d in HS.items() for cn, v in d.items()), key=lambda x: -x[0])[:8]
    P('== HUE STEP (largest 15-min hue jump, chroma>0.015): worst baby-minus-Picta excess')
    for ex, w, cn, v in worst_excess: P(f'   {w} {cn:14s} Picta {v["picta_max_step_deg"]}@{v["at"]}  baby {v["baby_max_step_deg"]}@{v["baby_at"]}  excess {ex:+.1f}')''',
'''    HS = {}
    for fn, r in res.items():
        for w in r['weathers']: HS[w] = ab_steps(r, w)
    worst_excess = sorted(((v['baby_max_step'] - v['picta_max_step'], w, cn, v) for w, d in HS.items() for cn, v in d.items()), key=lambda x: -x[0])[:10]
    P('== COLOUR STEP (largest 15-min chromatic jump, OKLab a,b at equal Y; 0.02 ~ just noticeable): worst baby-minus-Picta excess')
    for ex, w, cn, v in worst_excess: P(f'   {w} {cn:14s} Picta {v["picta_max_step"]}@{v["at"]}  baby {v["baby_max_step"]}@{v["baby_at"]}  excess {ex:+.4f}')''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
