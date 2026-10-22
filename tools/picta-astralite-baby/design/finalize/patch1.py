import sys, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'final2_model.py')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new)
rep("""def solve_periods(cases, F_night, WL):
    rows, rhs = [], []
    for Bf, Tf, Yf, extra in cases:
        for h in FIT_H:""",
"""def solve_periods(cases, F_night, WL, MW=0.0):
    rows, rhs = [], []
    for Bf, Tf, Yf, extra in cases:
        WLc = WL if not (isinstance(extra, dict) and 'WL' in extra) else extra['WL']
        Mf = extra.get('Mf') if isinstance(extra, dict) else None
        for h in FIT_H:""")
rep("""            lb = LUM @ B; r = np.zeros(15)
            for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = WL * w[p] * lb / yp
            rows.append(r); rhs.append(WL * (yp - Y(const)) / yp)
    x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)""",
"""            lb = LUM @ B; r = np.zeros(15)
            for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = WLc * w[p] * lb / yp
            rows.append(r); rhs.append(WLc * (yp - Y(const)) / yp)
            if MW > 0 and Mf is not None:
                mp = Mf(h)
                if mp > 1e-9:
                    mb = np.ones(3) / 3 @ B; r = np.zeros(15)
                    for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = MW * w[p] * mb / mp
                    rows.append(r); rhs.append(MW * (mp - float(np.mean(const))) / mp)
    x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)""")
rep("""                           lambda h, R=R, C=C: Y(Vf(E_P, R, h, C)), None))
        return cs""",
"""                           lambda h, R=R, C=C: Y(Vf(E_P, R, h, C)), dict(Mf=lambda h, R=R, C=C: float(np.mean(Vf(E_P, R, h, C))))))
        return cs""")
rep("""            F = solve_periods(mkcases(Bf, Vf, af(ALPHA, comp), kf(comp)), E_P[sec][key]['Night'], D['WL_FILTER'])""",
"""            F = solve_periods(mkcases(Bf, Vf, af(ALPHA, comp), kf(comp)), E_P[sec][key]['Night'], D['WL_FILTER'], D['WL_CLOUD_MEAN'] if comp == 'clouds' else 0.0)""")
rep("""                    cases.append((Bs, Ts, lambda h, R=R, C=C: Y(S_sun(E_P, R, h, C=C)), None))""",
"""                    cases.append((Bs, Ts, lambda h, R=R, C=C: Y(S_sun(E_P, R, h, C=C)), dict(WL=D['WL_SCAT_SUN'])))""")
rep("""    D.update(VOL_AMOUNT=0.5, WL_ALB=4.0, FAIR=True, SUMMER_OFFSET=True, HUE_LO=90.0, HUE_HI=150.0, Q=4)""",
"""    D.update(VOL_AMOUNT=0.5, WL_ALB=4.0, FAIR=True, SUMMER_OFFSET=True, HUE_LO=90.0, HUE_HI=150.0, Q=4, WL_SCAT_SUN=25.0, WL_CLOUD_MEAN=0.0)""")
rep("""def hue_steps(r, w, comps=('dome_hor_away', 'fog_far', 'clouds', 'cloud_sunlit', 'amb_XPlus', 'amb_ZMinus', 'sunlight')):""",
'''def ab_steps(r, w, comps=('dome_hor_away', 'fog_far', 'clouds', 'cloud_sunlit', 'amb_XPlus', 'amb_ZMinus', 'sunlight', 'scat_at_sun')):
    """largest chromatic jump between consecutive 15-minute steps (OKLab a,b distance at equal luminance), Picta vs baby."""
    E_P, E_B, R, Rb = r['_E_P'], r['_E_B'], r['_RP'][w], r['_RB'][w]
    hs = [5.75 + 0.25 * i for i in range(59)]
    prev = None; out = {c: [0.0, None, 0.0, None] for c in comps}
    for h in hs:
        a = components(E_P, R, h, light=True); b = components(E_B, Rb, h, light=True); cur = {}
        for cn in comps:
            ab_a = to_oklab(norm_y(a[cn]))[1:] if Y(a[cn]) > 1e-9 else None
            ab_b = to_oklab(norm_y(b[cn]))[1:] if Y(b[cn]) > 1e-9 else None
            cur[cn] = (ab_a, ab_b)
            if prev:
                pa, pb = prev[cn]
                if ab_a is not None and pa is not None:
                    d = float(np.linalg.norm(ab_a - pa))
                    if d > out[cn][0]: out[cn][0], out[cn][1] = round(d, 4), h
                if ab_b is not None and pb is not None:
                    d = float(np.linalg.norm(ab_b - pb))
                    if d > out[cn][2]: out[cn][2], out[cn][3] = round(d, 4), h
        prev = cur
    return {cn: dict(picta_max_step=v[0], at=v[1], baby_max_step=v[2], baby_at=v[3]) for cn, v in out.items()}

def hue_steps(r, w, comps=('dome_hor_away', 'fog_far', 'clouds', 'cloud_sunlit', 'amb_XPlus', 'amb_ZMinus', 'sunlight')):''')
open(p, 'w', encoding='utf-8').write(s)
print('patched')
