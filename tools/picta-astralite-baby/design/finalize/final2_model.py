"""FINALIZE pass: the final_model.py solver with the verifier fixes folded in (read-only on C:/1. AUTHORIA; numbers only).

Changes against design/final/final_model.py (which is imported for data, channel models and helpers):
  F1  sunlit clouds: ShadeCloud's sun term (SkyScattering.hlsli 218-228) = DesaturateCloudLight(GetScatteringColorAt(sunDir))
      * CloudsLightingSunIntensity * textureGray, with GetScatteringColorAt at elevation sunZ^2 and NO aboveH / DustDarkening but
      x saturate(Amount^2). It is now (a) solved: luminance + chromaticity rows for that sun-direction colour inside the
      ScatteringColor fixed point, and (b) audited: cloud_lit, cloud_sunlit (base + lit, texture 0.7), cloud_edge.
  F2  cloud formula order: desaturate the record term, then x Intensity x ColorFilter (Sky.hlsl 426).
  F3  hue mix: OKLCh short arc blended smoothly into a straight OKLab line as |dh| goes 90 -> 150 deg, so near-opposite
      hues mix through grey and the target never flips side between 15-minute steps.
  F4  ambient: albedo-weighted luminance rows (foliage, pine, dirt, stone, snow, skin) beside the light-luminance row, and the
      integer search scores surface error too.
  F5  precision: filter values written with 4 decimals; snap tolerance 5e-5; every audit runs on the quantised (written) values.
  F6  fair climate: the 4 fair weathers (19FA01, 19FA02, 19FB02, 19FC01) are solved jointly on Picta's clock AND the fair clock
      (SkyrimFairWorldClimate 05:30-10:00 / 16:00-20:30) and audited on both.
  F7  summer contrast: summer weathers aim at Astralite's colour shifted by Picta's own summer-minus-master OKLab offset.
  F8  volumetric light: range pinned to Picta (VOLI copies take the SamplingRepartitionRangeFactor of the Picta VOLI they
      replace, split into _R100/_R80 copies where needed; GVR RangeFactor untouched); zero-target crossfade hours audited
      (newly_on leak); VL weather-transition cross-term reported; VOL_AMOUNT 0.5 and 1.0 both solved.
  F9  mist table: one rule, the generic mist partner's own fields (ring and/or MoT banks) where Picta's slot is free.
Outputs go to this folder only.
"""
import sys, os, json, math, copy, itertools, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', 'final')))
import final_model as fm
from final_model import (Y, lerp, sat, curve, desat, Dm, tod_weights, clmt_weights, sun_z, to_oklab, from_oklab, norm_y, lch,
                         _fit_gamut, de_ok, hue_name, ev, parse_ini_E, picta_records, astra_records, soul_E, rec_at, V_band, B_band,
                         B_fog, V_fog, B_light, V_light, B_amb, V_amb, V_sundisc, earth_shadow, FILES, PICTA_TOD, NAT_TOD, PICTA_CLMT,
                         ASTRA_CLMT, FIT_H, AUDIT_H, NIGHT_H, PEAK, LUM, FREE, TODP, SLOTS, RSLOTS, AXES, DARK, PV, colour_partner,
                         wclass, Astra, parse_val)

FAIR_CLMT = (5.5, 10.0, 16.0, 20.5)
FAIR_W = {'19FA01', '19FA02', '19FB02', '19FC01'}
SUMMER_MASTER = {'5AFA01': '19FA01', '5AFA02': '19FA02', '5AFA03': '19FA03', '5AFB01': '19FB01', '5AFB02': '19FB02'}
FILE_OF = {w: f for f, ws in FILES.items() for w in ws}
TEX = 0.7
ALB = {'foliage': np.array([0.10, 0.17, 0.04]), 'pine': np.array([0.06, 0.10, 0.05]), 'dirt': np.array([0.30, 0.22, 0.14]),
       'stone': np.array([0.30, 0.30, 0.30]), 'snow': np.array([0.80, 0.82, 0.88]), 'skin': np.array([0.55, 0.35, 0.27])}
SNAP = 5e-5

def dials():
    D = fm.default_dials()
    D.update(VOL_AMOUNT=0.5, WL_ALB=4.0, FAIR=True, SUMMER_OFFSET=True, HUE_LO=120.0, HUE_HI=170.0, Q=4, WL_SCAT_SUN=100.0, WL_CLOUD_MEAN=3.0, CW_SCAT_SUN=1.0, SCAT_ITERS=6, SCAT_DAMP=1.0, CFS_SHARE=0.0, WL_SCAT=100.0)
    return D

# ------------------------------------------------------------------ F3 hybrid hue mix
def smoothstep(e0, e1, x):
    t = sat((x - e0) / (e1 - e0)); return t * t * (3 - 2 * t)
def blend(cP, cA, a, k=1.0, lo=90.0, hi=150.0):
    cP = np.asarray(cP, float); yP = Y(cP)
    if yP <= 1e-12: return cP.copy()
    if cA is None or Y(cA) <= 1e-12 or a <= 0:
        if abs(k - 1) < 1e-9: return cP.copy()
        L, C, h = lch(cP); return norm_y(_fit_gamut(L, C * k, h), yP)
    LP, aP, bP = to_oklab(norm_y(cP)); LA, aA, bA = to_oklab(norm_y(cA))
    CP, hP = math.hypot(aP, bP), math.degrees(math.atan2(bP, aP)) % 360
    CA, hA = math.hypot(aA, bA), math.degrees(math.atan2(bA, aA)) % 360
    if CA < 0.01: hA = hP
    if CP < 0.01: hP = hA
    dh = ((hA - hP + 180) % 360) - 180
    C1, h1 = lerp(CP, CA, a), math.radians((hP + a * dh) % 360)
    a1, b1 = C1 * math.cos(h1), C1 * math.sin(h1)
    a2, b2 = lerp(aP, aA, a), lerp(bP, bA, a)
    t = smoothstep(lo, hi, abs(dh))
    aa, bb = lerp(a1, a2, t), lerp(b1, b2, t)
    C, h = math.hypot(aa, bb), math.degrees(math.atan2(bb, aa)) % 360
    return norm_y(_fit_gamut(lerp(LP, LA, a), C * k, h), yP)
def share(vP, vA, vB, k=1.0):
    if vA is None or de_ok(vP, vA) < 0.004: return None
    best = min((de_ok(blend(vP, vA, a, k), vB), a) for a in np.arange(0, 1.501, 0.01))
    return round(float(best[1]), 2)

# ------------------------------------------------------------------ F2 clouds, F1 sun term
def B_cloud(E, R, h, T=PICTA_TOD, C=PICTA_CLMT, tex=1.0):
    c = desat(curve(rec_at(R, h, 'cloud', C) * tex, ev(E, 'SKY', 'CloudsCurve', h, T)), ev(E, 'SKY', 'CloudsDesaturation', h, T))
    return np.diag(c * ev(E, 'SKY', 'CloudsIntensity', h, T))
def V_cloud(E, R, h, T=PICTA_TOD, C=PICTA_CLMT, tex=1.0):
    return B_cloud(E, R, h, T, C, tex) @ ev(E, 'SKY', 'CloudsColorFilter', h, T)
def vsun(h, C=PICTA_CLMT):
    sz = sun_z(h, C); return np.array([0.0, math.sqrt(max(0.0, 1 - sz * sz)), sz])
VHOR_SUN = np.array([0.0, math.sqrt(1 - .05 ** 2), .05])
def S_parts_sun(E, R, h, T=PICTA_TOD, C=PICTA_CLMT, SCo=None, CFS=None):
    """GetScatteringColorAt(sunDir): SkyScatteringColor * Intensity * Pow32(sat(1-band(sz^2)*tint)) * sat(Amount^2)."""
    sp = fm.scat_parts(E, R, h, vsun(h, C), T, C, SCo, CFS)
    k = ev(E, 'SKYSCATTERING', 'Intensity', h, T) * sat(ev(E, 'SKYSCATTERING', 'Amount', h, T) ** 2)
    return sp['m'], sp['dust'], k
def S_sun(E, R, h, T=PICTA_TOD, C=PICTA_CLMT, SCo=None, CFS=None):
    m, dust, k = S_parts_sun(E, R, h, T, C, SCo, CFS)
    scol = ev(E, 'SKYSCATTERING', 'ScatteringColor', h, T, ovr=SCo)
    return m * scol * dust * k
def S_hor(E, R, h, T=PICTA_TOD, C=PICTA_CLMT): return fm.scat_parts(E, R, h, VHOR_SUN, T, C)['scat']
def cloud_lit(E, R, h, T=PICTA_TOD, C=PICTA_CLMT):
    if sun_z(h, C) < -0.02: return np.zeros(3)
    clsi = ev(E, 'SKY', 'CloudsIntensity', h, T) * ev(E, 'SKYSCATTERING', 'CloudsLightingSunMultiplier', h, T) + ev(E, 'SKYSCATTERING', 'CloudsLightingSunMinIntensity', h, T)
    d = float(np.clip(ev(E, 'SKYSCATTERING', 'CloudsLightingDesaturation', h, T), -1, 1))
    gray = TEX ** ev(E, 'SKY', 'CloudsCurve', h, T)
    return desat(S_sun(E, R, h, T, C), d) * gray * max(float(clsi), 0.0)
def cloud_sunlit(E, R, h, T=PICTA_TOD, C=PICTA_CLMT): return V_cloud(E, R, h, T, C, TEX) + cloud_lit(E, R, h, T, C)
def cloud_edge(E, R, h, T=PICTA_TOD, C=PICTA_CLMT):
    return S_sun(E, R, h, T, C) * ev(E, 'SKY', 'SunIntensity', h, T) * float(np.mean(V_cloud(E, R, h, T, C, TEX)))

def sky_pixel(E, R, h, view, T=PICTA_TOD, C=PICTA_CLMT): return fm.sky_pixel(E, R, h, view, T, C)

# ------------------------------------------------------------------ per-weather Astralite target (F7)
class SummerAstra:
    def __init__(self, A, Em, Rm, Es, Rs): self.A, self.Em, self.Rm, self.Es, self.Rs = A, Em, Rm, Es, Rs; self.E0 = A.E0; self.R0 = A.R0
    def vis(self, fn, h):
        va = self.A.vis(fn, h)
        if va is None: return None
        pm, ps = fn(self.Em, self.Rm, h), fn(self.Es, self.Rs, h)
        if Y(pm) <= 1e-12 or Y(ps) <= 1e-12: return va
        d = to_oklab(norm_y(ps, 1.0)) - to_oklab(norm_y(pm, 1.0)); d[0] = 0.0
        lab = to_oklab(norm_y(va, 1.0)) + d
        L, a, b = lab; C, hh = math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360
        return norm_y(_fit_gamut(L, C, hh), 1.0)

# ------------------------------------------------------------------ solver core
def solve_periods(cases, F_night, WL, MW=0.0):
    rows, rhs = [], []
    for Bf, Tf, Yf, extra in cases:
        WLc = WL if not (isinstance(extra, dict) and 'WL' in extra) else extra['WL']
        Mf = extra.get('Mf') if isinstance(extra, dict) else None
        CW = extra.get('CW', 1.0) if isinstance(extra, dict) else 1.0
        for h in FIT_H:
            w = tod_weights(h)
            if sum(w[p] for p in FREE) <= 0: continue
            B = Bf(h); yp = Yf(h)
            if yp <= 1e-9: continue
            t = Tf(h)
            const = B @ (w['Night'] * np.asarray(F_night, float))
            for ch in range(3):
                if CW <= 0: break
                r = np.zeros(15)
                for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = CW * w[p] * B[ch, :] / yp
                rows.append(r); rhs.append(CW * (t[ch] - const[ch]) / yp)
            lb = LUM @ B; r = np.zeros(15)
            for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = WLc * w[p] * lb / yp
            rows.append(r); rhs.append(WLc * (yp - Y(const)) / yp)
            if MW > 0 and Mf is not None:
                mp = Mf(h)
                if mp > 1e-9:
                    mb = np.ones(3) / 3 @ B; r = np.zeros(15)
                    for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = MW * w[p] * mb / mp
                    rows.append(r); rhs.append(MW * (mp - float(np.mean(const))) / mp)
    x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
    x = np.clip(x, 0.0, 10.0)
    return {p: x[3 * i:3 * i + 3] for i, p in enumerate(FREE)}

def q(v, nd=4):
    return np.round(np.asarray(v, float), nd)
def snapq(new, old, nd=4):
    new = np.asarray(new, float); old = np.asarray(old, float)
    if np.all(np.abs(new - old) < SNAP): return old.copy()
    return q(new, nd)

def solve_file(fname, D):
    E_P, RAW = parse_ini_E(DARK + '/' + fname)
    ws = FILES[fname]; RP = {w: picta_records(w) for w in ws}
    cp = colour_partner(ws[0]); A0 = Astra({cp: 1.0})
    AW = {}
    for w in ws:
        if D['SUMMER_OFFSET'] and w in SUMMER_MASTER:
            m = SUMMER_MASTER[w]; Em, _ = parse_ini_E(DARK + '/' + FILE_OF[m]); AW[w] = SummerAstra(A0, Em, picta_records(m), E_P, RP[w])
        else: AW[w] = A0
    CLK = {w: [PICTA_CLMT] + ([FAIR_CLMT] if (D['FAIR'] and w in FAIR_W) else []) for w in ws}
    ALPHA = {comp: dict(D['MIX']) for comp in ('sky', 'clouds', 'fog', 'light', 'amb', 'scat')}
    BL = lambda vp, va, a, k: blend(vp, va, a, k, D['HUE_LO'], D['HUE_HI'])
    def af(ALPHA, comp):
        return lambda h, C=PICTA_CLMT: sum(clmt_weights(h, C)[s] * ALPHA[comp][s] for s in RSLOTS)
    def kf(comp):
        def k(h, C=PICTA_CLMT):
            c = clmt_weights(h, C); return (sum(c[s] * D['STRENGTH'][s] for s in RSLOTS) + c['Night']) * D['KAPPA'][comp]
        return k
    chans = [('sky', 'SKY', 'GradientTopColorFilter', lambda E, R, h, C: B_band(E, R, h, 'top', C=C), lambda E, R, h, C: V_band(E, R, h, 'top', C=C)),
             ('sky', 'SKY', 'GradientHorizonColorFilter', lambda E, R, h, C: B_band(E, R, h, 'hor', C=C), lambda E, R, h, C: V_band(E, R, h, 'hor', C=C)),
             ('clouds', 'SKY', 'CloudsColorFilter', lambda E, R, h, C: B_cloud(E, R, h, C=C), lambda E, R, h, C: V_cloud(E, R, h, C=C)),
             ('fog', 'ENVIRONMENT', 'FogColorFilter', lambda E, R, h, C: B_fog(E, R, h, C=C), lambda E, R, h, C: V_fog(E, R, h, C=C))]

    def mkcases(Bf, Vf, a_, k_, E_for_B=None):
        cs = []
        for w, R in RP.items():
            for C in CLK[w]:
                Va = (lambda h, R=R, C=C, w=w: AW[w].vis(lambda E, R_, hh: Vf(E, R_, hh, C), h))
                cs.append((lambda h, R=R, C=C: Bf(E_for_B if E_for_B is not None else E_P, R, h, C),
                           lambda h, R=R, C=C, Va=Va: BL(Vf(E_P, R, h, C), Va(h), a_(h, C), k_(h, C)),
                           lambda h, R=R, C=C: Y(Vf(E_P, R, h, C)), dict(Mf=lambda h, R=R, C=C: float(np.mean(Vf(E_P, R, h, C))))))
        return cs

    def run_filters(ALPHA):
        res = {}
        for comp, sec, key, Bf, Vf in chans:
            F = solve_periods(mkcases(Bf, Vf, af(ALPHA, comp), kf(comp)), E_P[sec][key]['Night'], D['WL_FILTER'], D['WL_CLOUD_MEAN'] if comp == 'clouds' else 0.0)
            res[(sec, key)] = {p: snapq(F[p], E_P[sec][key][p]) for p in FREE}
        return res

    def run_light(ALPHA):
        Bf = lambda E, R, h, C: B_light(E, R, h, C=C); Vf = lambda E, R, h, C: V_light(E, R, h, C=C)
        best = None
        for WL in [100, 400, 1000, 3000]:
            F = solve_periods(mkcases(Bf, Vf, af(ALPHA, 'light'), kf('light')), E_P['ENVIRONMENT']['DirectLightingColorFilter']['Night'], WL)
            E_x = copy.deepcopy(E_P)
            for p in FREE: E_x['ENVIRONMENT']['DirectLightingColorFilter'][p] = q(F[p])
            worst = max(abs(Y(V_light(E_x, R, h, C=C)) / Y(V_light(E_P, R, h, C=C)) - 1) for w, R in RP.items() for C in CLK[w] for h in AUDIT_H
                        if Y(V_light(E_P, R, h, C=C)) > 1e-6)
            if best is None or worst < best[0] - 1e-9: best = (worst, WL, F)
            if worst <= 0.005: break
        return {p: snapq(best[2][p], E_P['ENVIRONMENT']['DirectLightingColorFilter'][p]) for p in FREE}, best[1]

    def run_scat(ALPHA):
        ap = {}
        a_ = af(ALPHA, 'scat')
        for p in FREE:
            wsum = [tod_weights(h)[p] for h in FIT_H]; s = sum(wsum)
            ap[p] = sum(wv * a_(h) for wv, h in zip(wsum, FIT_H)) / s if s > 0 else 0.0
        CFS = {p: float(lerp(E_P['SKYSCATTERING']['ColorFromSun'][p], ev(A0.E0, 'SKYSCATTERING', 'ColorFromSun', {'Dawn': 7.25, 'Sunrise': 9, 'Day': 13, 'Sunset': 17, 'Dusk': 18.75}[p]), D['CFS_SHARE'] * ap[p])) for p in FREE}
        CFS = {p: (E_P['SKYSCATTERING']['ColorFromSun'][p] if abs(CFS[p] - E_P['SKYSCATTERING']['ColorFromSun'][p]) < SNAP else round(CFS[p], 4)) for p in FREE}
        k_ = kf('scat')
        SCo = {p: E_P['SKYSCATTERING']['ScatteringColor'][p] for p in FREE}
        for it in range(D['SCAT_ITERS']):
            cases = []
            for w, R in RP.items():
                for C in CLK[w]:
                    def Bh(h, R=R, C=C, SCo=SCo):
                        sp = fm.scat_parts(E_P, R, h, VHOR_SUN, C=C, SCo=SCo, CFS=CFS); return np.diag(sp['m'] * sp['dust'] * sp['k'])
                    def Th(h, R=R, C=C, w=w):
                        return BL(S_hor(E_P, R, h, C=C), AW[w].vis(lambda E, R_, hh: S_hor(E, R_, hh, C=C), h), a_(h, C), k_(h, C))
                    cases.append((Bh, Th, lambda h, R=R, C=C: Y(S_hor(E_P, R, h, C=C)), None))
                    def Bs(h, R=R, C=C, SCo=SCo):
                        m, dust, kk = S_parts_sun(E_P, R, h, C=C, SCo=SCo, CFS=CFS); return np.diag(m * dust * kk)
                    def Ts(h, R=R, C=C, w=w):
                        return BL(S_sun(E_P, R, h, C=C), AW[w].vis(lambda E, R_, hh: S_sun(E, R_, hh, C=C), h), a_(h, C), k_(h, C))
                    cases.append((Bs, Ts, lambda h, R=R, C=C: Y(S_sun(E_P, R, h, C=C)), dict(WL=D['WL_SCAT_SUN'], CW=D['CW_SCAT_SUN'])))
            new = solve_periods(cases, E_P['SKYSCATTERING']['ScatteringColor']['Night'], D['WL_SCAT'])
            SCo = {p: (new[p] if it == 0 else lerp(np.asarray(SCo[p], float), new[p], D['SCAT_DAMP'])) for p in FREE}
        return {p: snapq(SCo[p], E_P['SKYSCATTERING']['ScatteringColor'][p]) for p in FREE}, CFS

    def apply(ALPHA):
        Eb = copy.deepcopy(E_P)
        for (sec, key), d in run_filters(ALPHA).items():
            for p in FREE: Eb[sec][key][p] = d[p]
        DLF, wl = run_light(ALPHA)
        for p in FREE: Eb['ENVIRONMENT']['DirectLightingColorFilter'][p] = DLF[p]
        SCo, CFS = run_scat(ALPHA)
        for p in FREE: Eb['SKYSCATTERING']['ScatteringColor'][p] = SCo[p]; Eb['SKYSCATTERING']['ColorFromSun'][p] = CFS[p]
        return Eb, wl

    probe = {'sky': lambda E, R, h: V_band(E, R, h, 'hor'), 'clouds': lambda E, R, h: V_cloud(E, R, h), 'fog': lambda E, R, h: V_fog(E, R, h),
             'light': lambda E, R, h: V_light(E, R, h), 'scat': lambda E, R, h: S_hor(E, R, h)}
    w0 = ws[0]; Rr = RP[w0]
    E_B, wl = apply(ALPHA)
    if D['NORMALISE'] and any(v > 0 for v in D['MIX'].values()):
        for it in range(2):
            for comp, Vf in probe.items():
                for s, hs in PEAK.items():
                    lab = D['MIX'][s]
                    if lab <= 0 or (comp == 'light' and s != 'Day'): continue
                    va = AW[w0].vis(lambda E, R_, hh: Vf(E, R_, hh), hs)
                    if va is None or de_ok(Vf(E_P, Rr, hs), va) < 0.02: continue
                    sh = share(Vf(E_P, Rr, hs), va, Vf(E_B, Rr, hs), kf(comp)(hs))
                    if sh is None or sh <= 0.02: continue
                    ALPHA[comp][s] = float(np.clip(ALPHA[comp][s] * lab / sh, 0.0, min(1.0, 2.0 * lab)))
            ALPHA['amb'] = dict(D['MIX'])
            E_B, wl = apply(ALPHA)
    out = dict(file=fname, weathers=ws, colour_partner=cp, records={}, alpha_used={c: {s: round(v, 3) for s, v in d.items()} for c, d in ALPHA.items()},
               light_luma_weight=wl)

    # --- DALC with albedo rows (F4), both clocks for fair weathers (F6)
    a_amb, k_amb = af(ALPHA, 'amb'), kf('amb')
    RB = {}
    for w, R in RP.items():
        Rb = copy.deepcopy(R); recs = {}
        for ax in AXES:
            rows, rhs = [], []
            for C in CLK[w]:
                for h in FIT_H:
                    c = clmt_weights(h, C)
                    if sum(c[s] for s in RSLOTS) <= 0: continue
                    Bm = B_amb(E_P, h); vp = V_amb(E_P, R, h, ax, C=C); yp = Y(vp)
                    if yp <= 1e-9: continue
                    va = AW[w].vis(lambda E, R_, hh: V_amb(E, R_, hh, ax, C=C), h)
                    t = BL(vp, va, a_amb(h, C), k_amb(h, C)); const = Bm @ (c['Night'] * R['Night']['dalc'][ax])
                    for ch in range(3):
                        r = np.zeros(9)
                        for i, s in enumerate(RSLOTS): r[3 * i:3 * i + 3] = c[s] * Bm[ch, :] / yp
                        rows.append(r); rhs.append((t[ch] - const[ch]) / yp)
                    for nm, alb in [('grey', np.ones(3))] + list(ALB.items()):
                        wgt = D['WL_AMB'] if nm == 'grey' else D['WL_ALB']
                        if wgt <= 0: continue
                        lb = (LUM * alb) @ Bm; ya = float((LUM * alb) @ vp); r = np.zeros(9)
                        for i, s in enumerate(RSLOTS): r[3 * i:3 * i + 3] = wgt * c[s] * lb / ya
                        rows.append(r); rhs.append(wgt * (ya - float((LUM * alb) @ const)) / ya)
            x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
            for i, s in enumerate(RSLOTS):
                tgt = np.clip(x[3 * i:3 * i + 3], 0, 254.4 / 255) * 255
                old = R[s]['dalc'][ax] * 255
                if np.all(np.abs(tgt - old) < 0.5): recs[(s, ax)] = np.round(old); Rb[s]['dalc'][ax] = recs[(s, ax)] / 255; continue
                base = np.round(tgt); bestc = None
                for dl in itertools.product((-1, 0, 1), repeat=3):
                    cc = np.clip(base + np.array(dl), 0, 255); Rt = copy.deepcopy(Rb); Rt[s]['dalc'][ax] = cc / 255
                    e1 = e2 = 0.0
                    for C in CLK[w]:
                        for h in FIT_H:
                            if clmt_weights(h, C)[s] < 0.5: continue
                            vb, vp = V_amb(E_P, Rt, h, ax, C=C), V_amb(E_P, R, h, ax, C=C)
                            e1 = max(e1, abs(Y(vb) / max(Y(vp), 1e-9) - 1))
                            for alb in ALB.values(): e2 = max(e2, abs(Y(alb * vb) / max(Y(alb * vp), 1e-9) - 1))
                    err = e1 + 0.25 * e2 + 0.002 * float(np.abs(norm_y(cc, 1) - norm_y(tgt, 1)).sum())
                    if bestc is None or err < bestc[0]: bestc = (err, cc)
                Rb[s]['dalc'][ax] = bestc[1] / 255; recs[(s, ax)] = bestc[1]
        RB[w] = Rb
        out['records'][w] = dict(editorid=R['_edid'], DALC={s: {ax: [int(v) for v in recs[(s, ax)]] for ax in AXES} for s in RSLOTS},
                                 DALC_picta={s: {ax: [int(round(v * 255)) for v in R[s]['dalc'][ax]] for ax in AXES} for s in RSLOTS})
        ssc = {}
        for s, hs in PEAK.items():
            vp = R[s]['statics'] * 255; va = AW[w].vis(lambda E, R_, hh: R_[s]['statics'], hs)
            t = BL(vp, va, D['MIX'][s], kf('fog')(hs))
            if t.max() > 254.4: t = norm_y(BL(vp, va, D['MIX'][s] * 0.7, 1.0), Y(vp))
            ssc[s] = [int(v) for v in np.clip(np.round(t), 0, 255)]
        out['records'][w]['SkyStaticsColor_optional'] = ssc
    out['_E_P'], out['_E_B'], out['_RP'], out['_RB'], out['_A'], out['_AW'], out['_RAW'], out['_CLK'] = E_P, E_B, RP, RB, A0, AW, RAW, CLK
    return out

# ------------------------------------------------------------------ F9 mist table: the generic mist partner's own fields
MIST_PARTNER_FIELDS = {  # from the PBR-lane winners (verify-records-fog/a4b.py): ring, MoT banks
    'SkyrimClear': (None, True), 'SkyrimClear_A': ('Lite', False), 'SkyrimCloudy': ('Lite', True), 'SkyrimFog': ('Heavy', True),
    'SkyrimOvercastRain': ('Rain', False), 'SkyrimOvercastSnow': ('Rain', False), 'SkyrimStormRain': ('DistRain', False), 'SkyrimStormSnow': ('816', False)}
PICTA_NEEDLES = {'C02', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06'}
def mist_plan(w):
    mp = fm.mist_partner(w); ring, mot = MIST_PARTNER_FIELDS[mp]
    if wclass(w) in PICTA_NEEDLES: ring = None   # Picta's own needles keep the slot
    return mp, ring, mot

# ------------------------------------------------------------------ F8 volumetric light
MIXED_RF = {'LAM_FogVL', 'LAM_FogVL_Blue', 'LAM_StormVL'}
def copy_name(src_name, picta_rf):
    return src_name + ('_R%d' % int(picta_rf) if src_name in MIXED_RF else '')

def solve_vl(results, D, K_fixed=None):
    branch = D['VL_BRANCH']; VOL = D['VOL_AMOUNT']
    W = []
    for r in results.values():
        E_P, E_B = r['_E_P'], r['_E_B']
        for w in r['weathers']:
            R = r['_RP'][w]; mp = fm.mist_partner(w); AR_ = astra_records(mp); SE = soul_E(AR_['_soul'])
            pslots = {s: fm.picta_voli(R['_voli'][s]) for s in SLOTS}
            bslots = {}
            for s in SLOTS:
                if s == 'Night': bslots[s] = pslots['Night']; continue
                v = fm.astra_voli(AR_['_voli'][s]); v['src'] = v['name']; v['name'] = copy_name(v['name'], pslots[s]['rf']); v['rf'] = pslots[s]['rf']
                bslots[s] = v
            relA = {}
            for s, hs in dict(Sunrise=7.0, Day=13.0, Sunset=19.0).items():
                v = bslots[s]; LA = V_light(SE, AR_, hs, NAT_TOD, ASTRA_CLMT)
                gA = ev(SE, 'GAMEVOLUMETRICRAYS', 'Intensity', hs, NAT_TOD); gF = ev(SE, 'GAMEVOLUMETRICRAYS', 'ColorFilter', hs, NAT_TOD)
                relA[s] = v['I'] * gA * Y(gF * lerp(LA, v['col'], v['cc'])) / max(Y(LA), 1e-9)
            def relP(h, E_P=E_P, R=R, pslots=pslots):
                if branch == 'newly_on': return 0.0
                L = V_light(E_P, R, h); I_, cc, col, dd = fm.voli_at(pslots, h)
                return fm.vl_rad(I_, cc, col, L, ev(E_P, 'GAMEVOLUMETRICRAYS', 'Intensity', h), ev(E_P, 'GAMEVOLUMETRICRAYS', 'ColorFilter', h)) / max(Y(L), 1e-9)
            def target(h, relA=relA, relP=relP):
                c = clmt_weights(h); rp = relP(h)
                return max(VOL * sum(c[s] * relA[s] for s in RSLOTS) + c['Night'] * rp, rp)
            W.append(dict(file=r['file'], w=w, E_P=E_P, E_B=E_B, R=R, pslots=pslots, bslots=bslots, relA=relA, relP=relP, target=target, partner=mp))
    names = sorted({wd['bslots'][s]['name'] for wd in W for s in RSLOTS})
    K = {n: 1.25 / next(wd['bslots'][s]['I'] for wd in W for s in RSLOTS if wd['bslots'][s]['name'] == n) for n in names}
    if K_fixed: K = dict(K_fixed)
    files = sorted({wd['file'] for wd in W})
    GN = {f: (0.0 if branch == 'newly_on' else float(results[f]['_E_P']['GAMEVOLUMETRICRAYS']['Intensity']['Night'])) for f in files}
    GP = {f: {p: float(results[f]['_E_P']['GAMEVOLUMETRICRAYS']['Intensity'][p]) for p in FREE} for f in files}
    G = {f: dict(GP[f]) for f in files}
    def GF_B(wd, h):
        w = tod_weights(h); gf = wd['E_P']['GAMEVOLUMETRICRAYS']['ColorFilter']
        return sum(w[p] * (Y(gf[p]) * np.ones(3) if p in FREE else gf[p]) for p in TODP)
    def a_of(wd, h):
        L = V_light(wd['E_B'], wd['R'], h); I_, cc, col, dd = fm.voli_at(wd['bslots'], h, K)
        return I_ * Y(GF_B(wd, h) * lerp(L, col, cc)) / max(Y(L), 1e-9)
    LAM = 0.05; CAP = 1.10
    def rad_of(wd, h):
        w = tod_weights(h); f = wd['file']
        return a_of(wd, h) * (sum(w[p] * G[f][p] for p in FREE) + w['Night'] * GN[f])
    capw = {}
    for it in range(30):
        for f in files:
            rows, rhs = [], []
            for wd in [x for x in W if x['file'] == f]:
                for h in FIT_H:
                    t = wd['target'](h)
                    if t <= 1e-6: continue
                    w = tod_weights(h); a = a_of(wd, h)
                    if a <= 1e-9: continue
                    wgt = capw.get((wd['w'], h), 1.0)
                    tt = min(t, t * CAP / 1.02) if wgt > 1 else t
                    rows.append([wgt * a * w[p] / t for p in FREE]); rhs.append(wgt * (tt - a * w['Night'] * GN[f]) / t)
            for i, p in enumerate(FREE):
                r = [0.0] * 5; r[i] = LAM / max(GP[f][p], 0.1); rows.append(r); rhs.append(LAM * GP[f][p] / max(GP[f][p], 0.1))
            x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
            G[f] = {p: float(np.clip(x[i], 0.0, 1000.0)) for i, p in enumerate(FREE)}
        if it < 10 and not K_fixed:
            for n in names:
                logs = []
                for wd in W:
                    for s in RSLOTS:
                        if wd['bslots'][s]['name'] != n: continue
                        for h in FIT_H:
                            if clmt_weights(h)[s] < 0.99 or tod_weights(h)['Night'] > 0: continue
                            t = wd['target'](h); rad = rad_of(wd, h)
                            if t > 1e-6 and rad > 1e-9: logs.append(math.log(t / rad))
                if logs: K[n] *= math.exp(0.5 * float(np.mean(logs)))
        else:
            worst = 0.0
            for wd in W:
                for h in FIT_H:
                    t = wd['target'](h)
                    if t <= 1e-6: continue
                    qq = rad_of(wd, h) / t; worst = max(worst, qq)
                    if qq > CAP: capw[(wd['w'], h)] = capw.get((wd['w'], h), 1.0) * 3.0
            if worst <= CAP + 1e-3: break
    rep = {}
    for wd in W:
        f = wd['file']; over = (0.0, None); under = (9.0, None); leak = (0.0, None); rows = []
        for h in AUDIT_H:
            t = wd['target'](h); rad = rad_of(wd, h)
            if t > 1e-6:
                qq = rad / t
                if qq > over[0]: over = (qq, h)
                if qq < under[0]: under = (qq, h)
            elif rad > leak[0]: leak = (rad, h)
            if h in (6.0, 6.5, 7.0, 7.5, 9.0, 13.0, 17.0, 18.5, 19.0, 19.5, 20.0):
                rp = wd['relP'](h) if branch == 'alive' else 0.0
                rows.append(dict(h=h, picta=round(rp, 2), target=round(t, 2), baby=round(rad, 2)))
        pk = {hh: round(rad_of(wd, hh) / max(wd['target'](hh), 1e-9), 2) for hh in (7.5, 13.0, 18.5)}
        xp = {hh: (round(rad_of(wd, hh) / wd['relP'](hh), 2) if (branch == 'alive' and wd['relP'](hh) > 1e-6) else None) for hh in (7.5, 13.0, 18.5)}
        rep[wd['w']] = dict(file=f, mist_partner=wd['partner'], reached_at_peaks=pk, intensity_only_x_picta=xp,
                            voli={s: wd['bslots'][s]['name'] for s in SLOTS}, max_over_target=[round(over[0], 3), over[1]],
                            min_vs_target=[round(under[0], 3), under[1]], zero_target_leak=[round(leak[0], 3), leak[1]], rows=rows)
    copies = {}
    for wd in W:
        for s in RSLOTS:
            v = wd['bslots'][s]
            copies[v['name']] = dict(source=v['formid'], source_editorid=v['src'], intensity=round(K[v['name']] * v['I'], 3),
                                     SamplingRepartitionRangeFactor=v['rf'], density=v['dens'], custom_colour_contribution=v['cc'])
    return dict(branch=branch, VOL_AMOUNT=VOL, K={n: K[n] for n in names}, copies=copies,
                GVR_Intensity={f: {p: round(G[f][p], 3) for p in FREE} for f in files}, GVR_Intensity_picta={f: GP[f] for f in files},
                GVR_Night={f: GN[f] for f in files}, per_weather=rep, _W=W, _G=G, _GN=GN, _K=K)

def voli_at_C(sl, h, C, K=None):
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
def vl_transition(vl, pairs, hours=(7.5, 13.0, 18.5)):
    W = {wd['w']: wd for wd in vl['_W']}; G = vl['_G']; GN = vl['_GN']; K = vl['_K']; out = {}
    def parts(wd, h, lane):
        sl = wd['bslots'] if lane == 'baby' else wd['pslots']; kk = K if lane == 'baby' else None
        I_, cc, col, dd = fm.voli_at(sl, h, kk); L = V_light(wd['E_B'] if lane == 'baby' else wd['E_P'], wd['R'], h)
        w = tod_weights(h)
        g = (sum(w[p] * G[wd['file']][p] for p in FREE) + w['Night'] * GN[wd['file']]) if lane == 'baby' else ev(wd['E_P'], 'GAMEVOLUMETRICRAYS', 'Intensity', h)
        return I_, cc, col, L, g
    for a, b in pairs:
        for h in hours:
            for lane in ('picta', 'baby'):
                Ia, cca, cola, La, ga = parts(W[a], h, lane); Ib, ccb, colb, Lb, gb = parts(W[b], h, lane)
                ra = Ia * ga * Y(lerp(La, cola, cca)); rb = Ib * gb * Y(lerp(Lb, colb, ccb))
                Im, ccm, colm, Lm, gm = (Ia + Ib) / 2, (cca + ccb) / 2, (cola + colb) / 2, (La + Lb) / 2, (ga + gb) / 2
                run = Im * gm * Y(lerp(Lm, colm, ccm)); ideal = (ra + rb) / 2
                out[f'{a}<->{b} {h} {lane}'] = round(100 * (run / max(ideal, 1e-12) - 1), 1)
    return out

# ------------------------------------------------------------------ audit
def components(E, R, h, C=PICTA_CLMT, light=False):
    c = {}
    c['band_top'] = V_band(E, R, h, 'top', C=C); c['band_hor'] = V_band(E, R, h, 'hor', C=C)
    for k, vd in fm.views(h).items(): c['dome_' + k] = sky_pixel(E, R, h, vd, C=C)
    c['dome_toward_sun_20'] = sky_pixel(E, R, h, np.array([0, math.sqrt(1 - .2 ** 2), .2]), C=C)
    c['sky_ibl'] = fm.sky_ibl(E, R, h) if (C == PICTA_CLMT and not light) else None
    c['clouds'] = V_cloud(E, R, h, C=C); c['cloud_lit'] = cloud_lit(E, R, h, C=C); c['cloud_sunlit'] = cloud_sunlit(E, R, h, C=C)
    c['cloud_edge'] = cloud_edge(E, R, h, C=C)
    c['fog_far'] = V_fog(E, R, h, C=C); c['fog_near'] = V_fog(E, R, h, 'fognear', C=C)
    c['sunlight'] = V_light(E, R, h, C=C); c['scat_horizon_sunward'] = S_hor(E, R, h, C=C); c['scat_at_sun'] = S_sun(E, R, h, C=C)
    for ax in AXES:
        v = V_amb(E, R, h, ax, C=C); c['amb_' + ax[11:]] = v
        for nm, alb in ALB.items(): c[f'surf_{nm}_{ax[11:]}'] = alb * v
    for nm, alb in ALB.items(): c[f'surf_{nm}_sun'] = alb * c['sunlight']
    return {k: v for k, v in c.items() if v is not None}
def audit_weather(r, w, C=PICTA_CLMT, hours=AUDIT_H):
    E_P, E_B, R, Rb = r['_E_P'], r['_E_B'], r['_RP'][w], r['_RB'][w]
    worst = {}; night_max = 0.0
    for h in hours:
        a = components(E_P, R, h, C); b = components(E_B, Rb, h, C)
        for cn in a:
            ya = Y(a[cn])
            if ya < 1e-7: continue
            d = Y(b[cn]) / ya - 1
            if cn not in worst or abs(d) > abs(worst[cn][0]): worst[cn] = (d, h)
    if C == PICTA_CLMT:
        for h in NIGHT_H[::2]:
            a = components(E_P, R, h % 24, C); b = components(E_B, Rb, h % 24, C)
            for cn in a: night_max = max(night_max, float(np.abs(a[cn] - b[cn]).max()))
    return {cn: [round(100 * v[0], 3), v[1]] for cn, v in worst.items()}, night_max

def ab_steps(r, w, comps=('dome_hor_away', 'fog_far', 'clouds', 'cloud_sunlit', 'amb_XPlus', 'amb_ZMinus', 'sunlight', 'scat_at_sun')):
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

def hue_steps(r, w, comps=('dome_hor_away', 'fog_far', 'clouds', 'cloud_sunlit', 'amb_XPlus', 'amb_ZMinus', 'sunlight')):
    """largest hue change between consecutive 15-minute steps (chroma > 0.015), Picta vs baby: the flip detector."""
    E_P, E_B, R, Rb = r['_E_P'], r['_E_B'], r['_RP'][w], r['_RB'][w]
    hs = [5.75 + 0.25 * i for i in range(59)]
    prev = None; out = {c: [0.0, None, 0.0, None] for c in comps}
    for h in hs:
        a = components(E_P, R, h, light=True); b = components(E_B, Rb, h, light=True); cur = {}
        for cn in comps:
            La, Ca, ha = lch(a[cn]) if Y(a[cn]) > 1e-9 else (0, 0, 0); Lb, Cb, hb = lch(b[cn]) if Y(b[cn]) > 1e-9 else (0, 0, 0)
            cur[cn] = (Ca, ha, Cb, hb)
            if prev:
                pCa, pha, pCb, phb = prev[cn]
                if min(Ca, pCa) > 0.015:
                    d = abs(((ha - pha + 180) % 360) - 180)
                    if d > out[cn][0]: out[cn][0], out[cn][1] = round(d, 1), h
                if min(Cb, pCb) > 0.015:
                    d = abs(((hb - phb + 180) % 360) - 180)
                    if d > out[cn][2]: out[cn][2], out[cn][3] = round(d, 1), h
        prev = cur
    return {cn: dict(picta_max_step_deg=v[0], at=v[1], baby_max_step_deg=v[2], baby_at=v[3]) for cn, v in out.items()}

def hue_table(r, w, hours=(7.25, 7.5, 13.0, 18.5, 18.75), comps=('dome_hor_away', 'dome_hor_sun', 'dome_zenith', 'fog_far', 'clouds', 'cloud_sunlit', 'sunlight', 'amb_XPlus', 'amb_ZMinus')):
    E_P, E_B, R, Rb, A = r['_E_P'], r['_E_B'], r['_RP'][w], r['_RB'][w], r['_AW'][w]
    out = {}
    for h in hours:
        a = components(E_P, R, h); b = components(E_B, Rb, h); row = {}
        for cn in comps:
            if cn.startswith('dome_'):
                vd = fm.views(h)[cn[5:]]; va = A.vis(lambda E, R_, hh: sky_pixel(E, R_, hh, vd), h)
            elif cn == 'fog_far': va = A.vis(lambda E, R_, hh: V_fog(E, R_, hh), h)
            elif cn == 'clouds': va = A.vis(lambda E, R_, hh: V_cloud(E, R_, hh), h)
            elif cn == 'cloud_sunlit': va = A.vis(lambda E, R_, hh: cloud_sunlit(E, R_, hh), h)
            elif cn == 'sunlight': va = A.vis(lambda E, R_, hh: V_light(E, R_, hh), h)
            else: va = A.vis(lambda E, R_, hh: V_amb(E, R_, hh, 'Directional' + cn[4:]), h)
            Lp, Cp, hp = lch(a[cn]); Lb, Cb, hb = lch(b[cn]); La, Ca, ha = lch(va) if va is not None else (0, 0, 0)
            row[cn] = dict(picta=f"{hp:5.1f}/{Cp:.3f} {hue_name(hp, Cp)}", baby=f"{hb:5.1f}/{Cb:.3f} {hue_name(hb, Cb)}",
                           astralite=f"{ha:5.1f}/{Ca:.3f} {hue_name(ha, Ca)}", dY_pct=round(100 * (Y(b[cn]) / max(Y(a[cn]), 1e-12) - 1), 2),
                           share=share(a[cn], va, b[cn]))
        out[h] = row
    return out

def summer_gap(res):
    out = {}
    for s, m in SUMMER_MASTER.items():
        rs, rm = res[FILE_OF[s]], res[FILE_OF[m]]
        for h in (7.5, 13.0, 18.5):
            ca = components(rm['_E_P'], rm['_RP'][m], h); cb = components(rs['_E_P'], rs['_RP'][s], h)
            ba = components(rm['_E_B'], rm['_RB'][m], h); bb = components(rs['_E_B'], rs['_RB'][s], h)
            for cn in ('dome_hor_away', 'fog_far', 'sunlight', 'amb_XPlus'):
                gp = float(np.linalg.norm(to_oklab(norm_y(ca[cn])) - to_oklab(norm_y(cb[cn]))))
                gb = float(np.linalg.norm(to_oklab(norm_y(ba[cn])) - to_oklab(norm_y(bb[cn]))))
                if gp > 1e-3: out[f'{s} {h} {cn}'] = dict(gap_picta=round(gp, 4), gap_baby=round(gb, 4), kept=round(gb / gp, 2))
    return out

# ------------------------------------------------------------------ plan
def fmtq(v, nd=4):
    v = np.atleast_1d(np.asarray(v, float))
    f = lambda x: (f"{x:.{nd}f}".rstrip('0').rstrip('.') if abs(x) >= 0.5 * 10 ** -nd else '0')
    return ', '.join(f(x) for x in v)
PLAN_KEYS = [('SKY', 'GradientTopColorFilter'), ('SKY', 'GradientHorizonColorFilter'), ('SKY', 'CloudsColorFilter'),
             ('ENVIRONMENT', 'FogColorFilter'), ('ENVIRONMENT', 'DirectLightingColorFilter'),
             ('SKYSCATTERING', 'ScatteringColor'), ('SKYSCATTERING', 'ColorFromSun')]
def e11_plan(r, vl=None):
    E_P, E_B, RAW = r['_E_P'], r['_E_B'], r['_RAW']; edits = []
    for sec, key in PLAN_KEYS:
        for p in FREE:
            a, b = np.asarray(E_P[sec][key][p], float), np.asarray(E_B[sec][key][p], float)
            if np.all(np.abs(a - b) < SNAP): continue
            edits.append(dict(section=sec, key=key + p, old=RAW[sec][key + p], new=fmtq(b)))
    if vl is not None:
        f = r['file']; GV = vl['GVR_Intensity'][f]
        for p in FREE:
            old = RAW['GAMEVOLUMETRICRAYS']['Intensity' + p]
            if abs(float(old) - GV[p]) >= 5e-4: edits.append(dict(section='GAMEVOLUMETRICRAYS', key='Intensity' + p, old=old, new=fmtq(GV[p], 3)))
            oldc = RAW['GAMEVOLUMETRICRAYS']['ColorFilter' + p]; g = Y(parse_val(oldc))
            if np.any(np.abs(parse_val(oldc) - g) >= 5e-4): edits.append(dict(section='GAMEVOLUMETRICRAYS', key='ColorFilter' + p, old=oldc, new=fmtq([g, g, g], 3)))
        if vl['branch'] == 'newly_on':
            old = RAW['GAMEVOLUMETRICRAYS']['IntensityNight']
            if abs(float(old)) >= 5e-4: edits.append(dict(section='GAMEVOLUMETRICRAYS', key='IntensityNight', old=old, new='0.0'))
    return edits

def run_all(D, files=None):
    return {fn: solve_file(fn, D) for fn in (files or list(FILES))}
def conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    raise TypeError(type(o))
def strip(d): return {k: v for k, v in d.items() if not k.startswith('_')}

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--quick', action='store_true'); ap.add_argument('--files', nargs='*')
    args = ap.parse_args()
    LOG = []
    def P(s=''): LOG.append(s); print(s, flush=True)
    D = dials()
    files = args.files or None
    P('FINALIZE MODEL (final2) - fixes F1..F9 over final_model.py'); P('dials: ' + json.dumps(D))
    # identity
    D0 = dials(); D0['MIX'] = dict(Sunrise=0.0, Day=0.0, Sunset=0.0)
    r0 = run_all(D0, files)
    idn = {fn: dict(e11_edits=len(e11_plan(r)), dalc_changed=sum(1 for w in r['weathers'] for s in RSLOTS for ax in AXES
                                                                    if r['records'][w]['DALC'][s][ax] != r['records'][w]['DALC_picta'][s][ax])) for fn, r in r0.items()}
    ok = all(v['e11_edits'] == 0 and v['dalc_changed'] == 0 for v in idn.values())
    P('== IDENTITY (MIX 0, no VL): ' + ('PASS 0 lines / 0 DALC bytes' if ok else json.dumps(idn)))
    json.dump(idn, open(os.path.join(HERE, 'identity_check.json'), 'w'), indent=1)
    res = run_all(D, files)
    # audits
    P('== LUMA AUDIT on written (4-decimal) values, 05:00-21:30 every 15 min; fair weathers on both clocks')
    audit = {}; gw = {}; gwf = {}
    for fn, r in res.items():
        for w in r['weathers']:
            worst, nm = audit_weather(r, w)
            entry = dict(file=fn, worst=worst, night_max_abs=nm)
            for cn, (d, h) in worst.items():
                if cn not in gw or abs(d) > abs(gw[cn][0]): gw[cn] = (d, h, w)
            if w in FAIR_W and D['FAIR']:
                wf, _ = audit_weather(r, w, FAIR_CLMT); entry['fair_clock_worst'] = wf
                for cn, (d, h) in wf.items():
                    if cn not in gwf or abs(d) > abs(gwf[cn][0]): gwf[cn] = (d, h, w)
            audit[w] = entry
            top = sorted([kv for kv in worst.items() if not kv[0].startswith('surf_')], key=lambda kv: -abs(kv[1][0]))[:5]
            P(f'   {w} ' + '  '.join(f'{cn} {d:+.2f}%@{h:g}' for cn, (d, h) in top) + f'   night {nm:.1e}')
    P('   GLOBAL worst (Picta clock): ' + '; '.join(f'{cn} {d:+.2f}% ({w}@{h:g})' for cn, (d, h, w) in sorted(gw.items(), key=lambda kv: -abs(kv[1][0]))))
    P('   GLOBAL worst (fair clock): ' + '; '.join(f'{cn} {d:+.2f}% ({w}@{h:g})' for cn, (d, h, w) in sorted(gwf.items(), key=lambda kv: -abs(kv[1][0]))))
    json.dump(dict(per_weather=audit, global_worst={k: [round(v[0], 3), v[1], v[2]] for k, v in gw.items()},
                   global_worst_fair={k: [round(v[0], 3), v[1], v[2]] for k, v in gwf.items()}), open(os.path.join(HERE, 'luma_audit.json'), 'w'), indent=1, default=conv)
    # hue steps (flip detector) all weathers
    HS = {}
    for fn, r in res.items():
        for w in r['weathers']: HS[w] = ab_steps(r, w)
    worst_excess = sorted(((v['baby_max_step'] - v['picta_max_step'], w, cn, v) for w, d in HS.items() for cn, v in d.items()), key=lambda x: -x[0])[:10]
    P('== COLOUR STEP (largest 15-min chromatic jump, OKLab a,b at equal Y; 0.02 ~ just noticeable): worst baby-minus-Picta excess')
    for ex, w, cn, v in worst_excess: P(f'   {w} {cn:14s} Picta {v["picta_max_step"]}@{v["at"]}  baby {v["baby_max_step"]}@{v["baby_at"]}  excess {ex:+.4f}')
    json.dump(HS, open(os.path.join(HERE, 'hue_steps.json'), 'w'), indent=1, default=conv)
    # hue tables
    HT = {}
    for w in ('19FA01', '19FC01', '19FD01', '19FD02', '19FD03', '19FE05', '5AFA01'):
        fn = FILE_OF[w]
        if fn not in res: continue
        HT[w] = hue_table(res[fn], w)
        P(f' -- {w} <- {res[fn]["colour_partner"]}')
        for h, row in HT[w].items():
            P(f'   {h:5.2f} ' + ' | '.join(f'{cn}: {v["picta"]} -> {v["baby"]} [{v["astralite"]}] {v["dY_pct"]:+.1f}% s={v["share"]}' for cn, v in row.items() if cn in ('dome_hor_away', 'fog_far', 'clouds', 'cloud_sunlit', 'amb_XPlus', 'amb_ZMinus', 'sunlight')))
    json.dump(HT, open(os.path.join(HERE, 'hue_tables.json'), 'w'), indent=1, default=conv)
    if all(FILE_OF[s] in res and FILE_OF[m] in res for s, m in SUMMER_MASTER.items()):
        SG = summer_gap(res); json.dump(SG, open(os.path.join(HERE, 'summer_gap.json'), 'w'), indent=1)
        kept = [v['kept'] for v in SG.values()]
        P(f'== SUMMER vs MASTER OKLab gap kept: min {min(kept):.2f} median {float(np.median(kept)):.2f} max {max(kept):.2f} over {len(kept)} cells')
    if args.quick:
        open(os.path.join(HERE, 'final2_quick_out.txt'), 'w', encoding='utf-8').write('\n'.join(LOG)); sys.exit(0)
    # VL
    VLR = {}
    for amt in (0.5, 1.0):
        for br in ('alive', 'newly_on'):
            Dv = dials(); Dv['VOL_AMOUNT'] = amt; Dv['VL_BRANCH'] = br
            K_fixed = None if (amt, br) == (0.5, 'alive') else VLR[(0.5, 'alive')]['_K']
            VLR[(amt, br)] = solve_vl(res, Dv, K_fixed=K_fixed)
            V = VLR[(amt, br)]
            worst = max((d['max_over_target'][0], w) for w, d in V['per_weather'].items())
            leak = max((d['zero_target_leak'][0], w, d['zero_target_leak'][1]) for w, d in V['per_weather'].items())
            P(f'== VL amount {amt} branch {br}: worst baby/target {worst}; zero-target leak max {leak}')
            for w in ('19FA01', '19FA03', '19FB03', '19FC01', '19FD02', '19FD03', '19FE03', '19FE05'):
                d = V['per_weather'][w]
                P(f'   {w} reached {d["reached_at_peaks"]} intensity-only x Picta {d["intensity_only_x_picta"]} GVR {V["GVR_Intensity"][d["file"]]}')
            P('   copies: ' + json.dumps({n: (c['intensity'], c['SamplingRepartitionRangeFactor']) for n, c in V['copies'].items()}))
    TR = vl_transition3(VLR[(0.5, 'alive')], [('19FA01', '19FD03'), ('19FE03', '19FD03'), ('19FE01', '19FD02'), ('19FA01', '19FC01'), ('19FC01', '19FC04'), ('19FA01', '19FE03')])
    P('== VL TRANSITION at t=0.5, % (vs ideal lerp / vs brighter endpoint), lanes picta | baby | astralite:')
    for k in sorted({kk.rsplit(' ', 1)[0] for kk in TR}):
        P('   ' + k + ': ' + ' | '.join(f"{ln} {TR[k + ' ' + ln]['vs_ideal']:+.0f}/{TR[k + ' ' + ln]['vs_brighter_end']:+.0f}" for ln in ('picta', 'baby', 'astralite')))
    # plan + stage-ready manifest
    vlA, vlN = VLR[(0.5, 'alive')], VLR[(0.5, 'newly_on')]
    plan = dict(dials=D, files={fn: dict(weathers=r['weathers'], colour_partner=r['colour_partner'], alpha_used=r['alpha_used'], light_luma_weight=r['light_luma_weight'],
                                         e11_edits=e11_plan(r, vlA), e11_edits_newly_on=e11_plan(r, vlN), e11_edits_full_alive=e11_plan(r, VLR[(1.0, 'alive')]), e11_edits_full_newly_on=e11_plan(r, VLR[(1.0, 'newly_on')]))
                                for fn, r in res.items()},
                records={w: dict(r['records'][w], colour_partner=r['colour_partner'], mist=mist_plan(w)) for r in res.values() for w in r['weathers']},
                vl={f'{a}_{b}': strip(v) for (a, b), v in VLR.items()}, vl_transition=TR)
    json.dump(plan, open(os.path.join(HERE, 'final2_plan.json'), 'w'), indent=1, default=conv)
    nlines = {k: sum(len(f[k]) for f in plan['files'].values()) for k in ('e11_edits', 'e11_edits_newly_on', 'e11_edits_full_alive', 'e11_edits_full_newly_on')}
    keys = sorted({re.sub(r'(Dawn|Sunrise|Day|Sunset|Dusk|Night)$', '', e['section'] + '.' + e['key']) for f in plan['files'].values() for e in f['e11_edits'] + f['e11_edits_newly_on']})
    nightkeys = [e['key'] for f in plan['files'].values() for e in f['e11_edits'] if re.search(r'(Night|InteriorDay|InteriorNight)$', e['key'])]
    P(f'== E11 LINES routed files: {nlines}; Night/Interior in alive: {len(nightkeys)}')
    P('   keys: ' + ', '.join(keys))
    # records manifest
    MOT = [f'{x:06X}:Mists of Tamriel.esp' for x in range(0x00080B, 0x000817)]
    RING_SRC = {'Lite': ('000834', '000802'), 'Heavy': ('000812', '000803'), 'Rain': ('00081C', '00080C')}
    RING_BE = {'Lite': 0.0, 'Heavy': 0.4980392, 'Rain': 0.0}
    ops = {}; nring = {}; nmot = 0
    for r in res.values():
        for w in r['weathers']:
            rec = r['records'][w]; o = []
            for s_ in RSLOTS:
                for ax in AXES:
                    if rec['DALC'][s_][ax] != rec['DALC_picta'][s_][ax]:
                        o.append(dict(field=f'DirectionalAmbientLightingColors.{s_}.{ax}', old=rec['DALC_picta'][s_][ax], new=rec['DALC'][s_][ax]))
            names = vlA['per_weather'][w]['voli']
            for s_ in RSLOTS: o.append(dict(field=f'VolumetricLighting.{s_}', new='PXA_' + names[s_]))
            mp, ring, mot = mist_plan(w)
            if ring in RING_SRC:
                o += [dict(field='VisualEffect', new=f'PXA_Distant_Mounts_{ring}'), dict(field='VisualEffectBegin', new=RING_BE[ring]), dict(field='VisualEffectEnd', new=RING_BE[ring])]
                nring[ring] = nring.get(ring, 0) + 1
            if mot: o.append(dict(field='SkyStatics', op='add', new=MOT)); nmot += 1
            ops[w + ':Picta - Weathers of Aurbis.esm'] = dict(editorid=rec['editorid'], mist_partner=mp, ring=ring, mot_banks=mot,
                forward_from=('Authoria - Patch - Picta Seasonal.esp' if w.startswith('5AF') else 'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp'), ops=o)
    new_records = [dict(type='VOLI', editorid='PXA_' + n, create_from=c['source'], set=dict(Intensity=c['intensity'], SamplingRepartitionRangeFactor=c['SamplingRepartitionRangeFactor']),
                        note='housecarl_create with every field of the source read; only Intensity and range differ') for n, c in sorted(vlA['copies'].items())]
    used = sorted({v for v in nring})
    for k in used:
        rf, ao = RING_SRC[k]
        new_records.append(dict(type='RFCT', editorid=f'PXA_Distant_Mounts_{k}', copy_of=f'{rf}:Astralite ENB.esp', seed_paths=['EffectArt'],
                                internalized=dict(type='ARTO', from_=f'{ao}:Astralite ENB.esp', rename_to=f'PXA_Distant_Mounts_{k}_Art')))
    json.dump(dict(plugin='Authoria - Patch - Picta x Astralite.esp', flags=['ESL'], new_records=new_records, overrides=ops,
                   vl_copies_full_strength={n: c['intensity'] for n, c in VLR[(1.0, 'alive')]['copies'].items()},
                   optional_off_by_default=dict(SkyStaticsColor={w: r['records'][w]['SkyStaticsColor_optional'] for r in res.values() for w in r['weathers']})),
              open(os.path.join(HERE, 'records_manifest.json'), 'w'), indent=1, default=conv)
    P(f'== RECORDS: {len(ops)} WTHR overrides, {sum(len(v["ops"]) for v in ops.values())} field ops, {len(new_records)} new records (+{len(used)} internalized ARTO); rings {nring}; MoT banks on {nmot}')
    open(os.path.join(HERE, 'final2_out.txt'), 'w', encoding='utf-8').write('\n'.join(LOG))
