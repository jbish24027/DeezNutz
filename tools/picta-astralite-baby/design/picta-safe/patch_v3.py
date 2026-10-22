import re
p = 'baby_model.py'
s = open(p, encoding='utf-8').read()

# 1) light group: drop SunColorFilter (sun disc + sunward glow stay Picta); god rays get their own product lock
a = """    ('light_dl', 'ENVIRONMENT', 'DirectLightingColorFilter', 'SunlightColor', LIGHT_MAP, 'light', L_dl),
    ('light_sun', 'SKY', 'SunColorFilter', 'SunlightColor', LIGHT_MAP, 'light', L_sun),
]"""
assert a in s
s = s.replace(a, """    ('light_dl', 'ENVIRONMENT', 'DirectLightingColorFilter', 'SunlightColor', LIGHT_MAP, 'light', L_dl),
]""")
a = """TIES = {('SKY', 'SunColorFilter'): [('SKY', 'MoonColorFilter')],                       # moon follows sun (Picta tie)
        ('ENVIRONMENT', 'DirectLightingColorFilter'): [('GAMEVOLUMETRICRAYS', 'ColorFilter')]}   # god rays follow sunlight"""
assert a in s
s = s.replace(a, "TIES = {}   # god rays (GAMEVOLUMETRICRAYS ColorFilter) are solved separately below; Sun/Moon filters are NOT touched")

# 2) general ridge solver replacing lsq_lock
i0 = s.index("def lsq_lock("); i1 = s.index("ini_cache = {rel")
new_solver = '''RIDGE = 0.02   # luminance first, hue second: weight of 'stay on the hue target' rows vs every-hour luminance rows

def grad(Lf, ini, rec, h):
    """Lf is linear in F -> return its gradient vector a_h (so Lh(F) = a_h . F)."""
    return np.array([Lf(ini, rec, h, e) for e in np.eye(3)])

def ridge_lock(ini, rec, Lf, old, dirs, ridge=RIDGE):
    """Unknown: full RGB filter F_p for each changed period p.
       rows 1: every hour, sum_p w_p(h) a_h.F_p == sum_p w_p(h) a_h.F_p_old   (relative to the component's total Y)
       rows 2: sqrt(ridge) * (F_p - k0_p u_p) / Y(k0_p u_p) == 0  (stay on the Astralite hue target)
       k0_p = scalar lock (best scale of u_p alone)."""
    pers = list(dirs); n = len(pers)
    rowsA = []; rowsb = []; scal_A = []
    for h in HOURS:
        w = tod_weights(h)
        if not any(w[p] > 0 for p in pers): continue
        a = grad(Lf, ini, rec, h)
        tot = sum(w[p] * float(a @ old[p]) for p in w if w[p] > 0 and p in old)
        if tot <= 1e-9: continue
        row = np.zeros(3 * n)
        for i, p in enumerate(pers): row[3 * i:3 * i + 3] = w[p] * a / tot
        rowsA.append(row); rowsb.append(sum(w[p] * float(a @ old[p]) for p in pers) / tot)
        scal_A.append([w[p] * float(a @ dirs[p]) / tot for p in pers])
    k0, *_ = np.linalg.lstsq(np.array(scal_A), np.array(rowsb), rcond=None)
    tgt = {p: k0[i] * dirs[p] for i, p in enumerate(pers)}
    for i, p in enumerate(pers):
        yt = max(Y(tgt[p]), 1e-9)
        for c in range(3):
            row = np.zeros(3 * n); row[3 * i + c] = math.sqrt(ridge) / yt
            rowsA.append(row); rowsb.append(math.sqrt(ridge) * tgt[p][c] / yt)
    x, *_ = np.linalg.lstsq(np.array(rowsA), np.array(rowsb), rcond=None)
    return {p: np.clip(x[3 * i:3 * i + 3], 0.0, 10.0) for i, p in enumerate(pers)}, tgt

'''
s = s[:i0] + new_solver + s[i1:]

a = """        k = lsq_lock(ini, rec, Lf, old, dirs)
        for per in pmap:
            new = np.clip(k[per] * dirs[per], 0.0, 10.0)"""
assert a in s
s = s.replace(a, """        sol, tgt = ridge_lock(ini, rec, Lf, old, dirs)
        for per in pmap:
            new = sol[per]""")
a = """                              t=round(STRENGTH * MULT[mk] * pmap[per][1], 4), donor_slot=pmap[per][0]))
            for (tsec, tkey)"""
assert a in s
s = s.replace(a, """                              t=round(STRENGTH * MULT[mk] * pmap[per][1], 4), donor_slot=pmap[per][0],
                              hue_target=[round(float(x), 4) for x in tgt[per]]))
            for (tsec, tkey)""")

# god rays
a = """    plan[rel] = edits
"""
assert s.count(a) == 1
s = s.replace(a, """    # god rays: colour = graded sunlight (E11 DL chain, no un-grade in 4ca678b) x GAMEVOLUMETRICRAYS ColorFilter
    iniB_dl = copy.deepcopy(ini)
    for e in edits:
        if e['key'].startswith('DirectLightingColorFilter'): iniB_dl['ENVIRONMENT'][e['key']] = ", ".join(repr(x) for x in e['new'])
    def L_gvr_factory(ini_light):
        def f(ini_, rec_, h, F):
            sl = desat(rec_at(rec_, 'SunlightColor', h) ** bf(ini_light, 'ENVIRONMENT', 'DirectLightingCurve', h, 1.0), bf(ini_light, 'ENVIRONMENT', 'DirectLightingDesaturation', h))
            return Y(sl * brgb(ini_light, 'ENVIRONMENT', 'DirectLightingColorFilter', h) * F) * bf(ini_light, 'ENVIRONMENT', 'DirectLightingIntensity', h, 1.0)
        return f
    oldg = {p: parse_rgb(ini['GAMEVOLUMETRICRAYS']['ColorFilter' + p]) for p in ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']}
    newdl = {e['key'][len('DirectLightingColorFilter'):]: np.array(e['new']) for e in edits if e['key'].startswith('DirectLightingColorFilter')}
    gdirs = {p: unit(newdl[p]) * Y(oldg[p]) for p in LIGHT_MAP}
    A = []; bvec = []; pers = list(LIGHT_MAP)
    LP = L_gvr_factory(ini); LB = L_gvr_factory(iniB_dl)
    for h in HOURS:
        w = tod_weights(h)
        if not any(w[p] > 0 for p in pers): continue
        refY = LP(ini, rec, h, brgb(ini, 'GAMEVOLUMETRICRAYS', 'ColorFilter', h))
        if refY <= 1e-9: continue
        fixed = np.zeros(3)
        for p in w:
            if w[p] > 0 and p not in pers: fixed = fixed + w[p] * oldg[p]
        A.append([w[p] * LB(iniB_dl, rec, h, gdirs[p]) / refY for p in pers])
        bvec.append((refY - LB(iniB_dl, rec, h, fixed)) / refY)
    kg, *_ = np.linalg.lstsq(np.array(A), np.array(bvec), rcond=None)
    for i, p in enumerate(pers):
        new = np.clip(kg[i] * gdirs[p], 0, 10)
        edits.append(dict(channel='godrays', section='GAMEVOLUMETRICRAYS', key='ColorFilter' + p, old=[round(x, 4) for x in oldg[p]],
                          new=[round(float(x), 4) for x in new], t=None, donor_slot=LIGHT_MAP[p][0]))
    plan[rel] = edits
""")

# 3) DALC: ridge per axis over the 3 record slots
i0 = s.index("        # LSQ over hours on the record clock (CLMT)")
i1 = s.index("            entry['DALC'][s][ax] = dict(old=")
new_dalc = '''        # ridge LSQ over hours on the record clock (CLMT) with that hour's E11 ambient desat/intensity
        rowsA = []; rowsb = []; scal_A = []
        for h in HOURS:
            cw = clmt_weights(h)
            if not any(cw[s] > 0 for s in REC_SLOTS): continue
            d = bf(ini, 'ENVIRONMENT', 'AmbientLightingDesaturation', h); I = bf(ini, 'ENVIRONMENT', 'AmbientLightingIntensity', h, 1.0)
            M = ((1 - d) * np.eye(3) + d / 3.0 * np.ones((3, 3)))          # desat as a linear map (valid while nothing clips)
            a = I * (L @ M) / 255.0
            tot = sum(cw[s] * float(a @ old[s]) for s in cw if cw[s] > 0)
            if tot <= 1e-9: continue
            row = np.zeros(9)
            for i, s in enumerate(REC_SLOTS): row[3 * i:3 * i + 3] = cw[s] * a / tot
            rowsA.append(row); rowsb.append(sum(cw[s] * float(a @ old[s]) for s in REC_SLOTS) / tot)
            scal_A.append([cw[s] * float(a @ dirs[s]) / tot for s in REC_SLOTS])
        k0, *_ = np.linalg.lstsq(np.array(scal_A), np.array(rowsb), rcond=None)
        tg = {s: k0[i] * dirs[s] for i, s in enumerate(REC_SLOTS)}
        for i, s in enumerate(REC_SLOTS):
            yt = max(Y(tg[s]), 1e-9)
            for c in range(3):
                row = np.zeros(9); row[3 * i + c] = math.sqrt(RIDGE) / yt
                rowsA.append(row); rowsb.append(math.sqrt(RIDGE) * tg[s][c] / yt)
        xs, *_ = np.linalg.lstsq(np.array(rowsA), np.array(rowsb), rcond=None)
        for i, s in enumerate(REC_SLOTS):
            target = np.clip(xs[3 * i:3 * i + 3], 0, 255)
            base = np.round(target)
            best = None
            hrs = [h for h in HOURS if clmt_weights(h)[s] > 0.5]
            for dlt in itertools.product((-1, 0, 1), repeat=3):
                c = np.clip(base + np.array(dlt), 0, 255)
                errs = []
                for h in hrs:
                    d = bf(ini, 'ENVIRONMENT', 'AmbientLightingDesaturation', h)
                    errs.append(abs(Y(desat(c, d)) - Y(desat(target, d))) / max(Y(desat(target, d)), 1e-6))
                err = (max(errs) if errs else 0) + 0.002 * np.abs(unit(c) - unit(target)).sum()
                if best is None or err < best[0]: best = (err, c)
'''
s = s[:i0] + new_dalc + s[i1:]
open(p, 'w', encoding='utf-8').write(s)
print('patched ok')
