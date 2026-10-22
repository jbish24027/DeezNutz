import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'final2_model.py')
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new)
# chroma weight per case
rep("""        Mf = extra.get('Mf') if isinstance(extra, dict) else None""",
"""        Mf = extra.get('Mf') if isinstance(extra, dict) else None
        CW = extra.get('CW', 1.0) if isinstance(extra, dict) else 1.0""")
rep("""            for ch in range(3):
                r = np.zeros(15)
                for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = w[p] * B[ch, :] / yp
                rows.append(r); rhs.append((t[ch] - const[ch]) / yp)
            lb = LUM @ B; r = np.zeros(15)
            for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = WLc * w[p] * lb / yp""",
"""            for ch in range(3):
                if CW <= 0: break
                r = np.zeros(15)
                for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = CW * w[p] * B[ch, :] / yp
                rows.append(r); rhs.append(CW * (t[ch] - const[ch]) / yp)
            lb = LUM @ B; r = np.zeros(15)
            for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = WLc * w[p] * lb / yp""")
rep("""dict(WL=D['WL_SCAT_SUN'])))""", """dict(WL=D['WL_SCAT_SUN'], CW=D['CW_SCAT_SUN'])))""")
rep("""        for it in range(6):
            cases = []""", """        for it in range(D['SCAT_ITERS']):
            cases = []""")
rep("""            new = solve_periods(cases, E_P['SKYSCATTERING']['ScatteringColor']['Night'], D['WL_SCAT'])
            SCo = {p: new[p] for p in FREE}""",
"""            new = solve_periods(cases, E_P['SKYSCATTERING']['ScatteringColor']['Night'], D['WL_SCAT'])
            SCo = {p: (new[p] if it == 0 else lerp(np.asarray(SCo[p], float), new[p], D['SCAT_DAMP'])) for p in FREE}""")
rep("""WL_SCAT_SUN=25.0, WL_CLOUD_MEAN=0.0)""", """WL_SCAT_SUN=25.0, WL_CLOUD_MEAN=0.0, CW_SCAT_SUN=1.0, SCAT_ITERS=6, SCAT_DAMP=1.0)""")
open(p, 'w', encoding='utf-8').write(s)
e = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exp1.py')
t = open(e, encoding='utf-8').read()
t = t.replace("""'cmean3': dict(WL_CLOUD_MEAN=3.0),""", """'cmean3': dict(WL_CLOUD_MEAN=3.0), 'cfs0': dict(CFS_SHARE=0.0), 'sunCW0': dict(CW_SCAT_SUN=0.0),
        'it12d5': dict(SCAT_ITERS=14, SCAT_DAMP=0.5), 'w100': dict(WL_SCAT=100.0, WL_SCAT_SUN=100.0),""")
open(e, 'w', encoding='utf-8').write(t)
print('ok')
