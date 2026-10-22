p = 'baby_model.py'
s = open(p, encoding='utf-8').read()
a = """        A.append([w[p] * LB(iniB_dl, rec, h, gdirs[p]) / refY for p in pers])
        bvec.append((refY - LB(iniB_dl, rec, h, fixed)) / refY)
    kg, *_ = np.linalg.lstsq(np.array(A), np.array(bvec), rcond=None)
    for i, p in enumerate(pers):
        new = np.clip(kg[i] * gdirs[p], 0, 10)"""
assert a in s
b = """        A.append([w[p] * LB(iniB_dl, rec, h, gdirs[p]) / refY for p in pers])
        bvec.append((refY - LB(iniB_dl, rec, h, fixed)) / refY)
        gB = np.array([LB(iniB_dl, rec, h, e) for e in np.eye(3)])
        row = np.zeros(3 * len(pers))
        for i, p in enumerate(pers): row[3 * i:3 * i + 3] = w[p] * gB / refY
        GA.append(row); Gb.append(bvec[-1])
    kg, *_ = np.linalg.lstsq(np.array(A), np.array(bvec), rcond=None)
    for i, p in enumerate(pers):          # ridge rows: stay on the light's hue (Picta tie GVR == DL kept in hue)
        tg = kg[i] * gdirs[p]; yt = max(Y(tg), 1e-9)
        for c in range(3):
            row = np.zeros(3 * len(pers)); row[3 * i + c] = math.sqrt(RIDGE) / yt
            GA.append(row); Gb.append(math.sqrt(RIDGE) * tg[c] / yt)
    xg, *_ = np.linalg.lstsq(np.array(GA), np.array(Gb), rcond=None)
    for i, p in enumerate(pers):
        new = np.clip(xg[3 * i:3 * i + 3], 0, 10)"""
s = s.replace(a, b)
a = """    A = []; bvec = []; pers = list(LIGHT_MAP)
    LP = L_gvr_factory(ini)"""
assert a in s
s = s.replace(a, """    A = []; bvec = []; GA = []; Gb = []; pers = list(LIGHT_MAP)
    LP = L_gvr_factory(ini)""")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
