"""FINAL synthesized model for the Picta x Astralite "baby" (read-only on C:/1. AUTHORIA; numbers only).

Base = the per-channel design (one hue carrier per channel, Picta clocks, OKLCh mix, luminance lock), with the
judges' grafts and must-fixes:
  * all 24 routed exterior files and all 28 rotating records (shared files solved jointly over the weathers they serve)
  * Bottled's hue-dependent dust term inside the ScatteringColor / ColorFromSun solve (Effects11.cpp 192-197,
    SkyScattering.hlsli GetScatteringColor) and full ApplySkyScattering dome pixels in the audit
  * DirectLightingColorFilter solved luminance-first against the real per-hour record sunlight (picta-safe graft)
  * DALC: joint hourly solve per axis + integer +-1 search on the worst-hour luminance (picta-safe graft)
  * MIX normalised so the on-screen share at the record peaks (07:30 / 13:00 / 18:30) equals the MIX label
  * amplitude dials: STRENGTH per time slot x KAPPA per component (chroma only, hue fixed)
  * volumetric fog: Astralite VOLI translated into Picta's scalar regime (one factor per VOLI copy) + GVR Intensity solved
    INCLUDING the moon/sun crossfade hours, overshoot capped; RangeFactor pinned to Soul's 1.0; ColorFilter 1,1,1 baseline;
    two branches: 'alive' (VL works today, Picta night 8.0 kept) and 'newly_on' (VL dead today, fallback ini, night GVR 0)
  * sky-IBL proxy (E11-managed IBL: SkyIBLScale = MultiplicativeAmount, DALCMode 3) in the audit
  * identity regression (all mixes 0 -> every planned value equal to Picta's text), naive transplant row,
    sunward dome row, weather-transition cross-term, canonical vs family donor variant, MIX sweep with honest hue names.
Outputs go to this folder only.
"""
import json, math, os, re, sys, copy, itertools, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BABY = os.path.normpath(os.path.join(HERE, '..', '..'))
MAP = os.path.join(BABY, 'map')
DARK = 'C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1/enbseries'

ALLP = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night', 'InteriorDay', 'InteriorNight']
TODP = ALLP[:6]
FREE = ALLP[:5]
SLOTS = ['Sunrise', 'Day', 'Sunset', 'Night']
RSLOTS = ['Sunrise', 'Day', 'Sunset']
AXES = ['DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus']
PICTA_TOD = dict(DawnDuration=3.5, SunriseTime=9.0, DayTime=10.0, SunsetTime=17.0, DuskDuration=3.5, NightTime=20.5)
NAT_TOD = dict(DawnDuration=3.5, SunriseTime=8.0, DayTime=13.0, SunsetTime=18.0, DuskDuration=3.5, NightTime=1.0)
PICTA_CLMT = (6.0, 9.0, 17.0, 20.0)
ASTRA_CLMT = (4.5, 9.5, 16.5, 21.5)
FIT_H = [5.5 + 0.25 * i for i in range(61)]             # 05:30 .. 20:30
AUDIT_H = [5.0 + 0.25 * i for i in range(67)]           # 05:00 .. 21:30
NIGHT_H = [20.5 + 0.25 * i for i in range(37)]          # 20:30 .. 05:30 (+24)
PEAK = dict(Sunrise=7.5, Day=13.0, Sunset=18.5)
LUM = np.array([0.2126, 0.7152, 0.0722])

# ------------------------------------------------------------------ dials
def default_dials():
    return dict(MIX=dict(Sunrise=0.50, Day=0.30, Sunset=0.50),
                STRENGTH=dict(Sunrise=1.0, Day=1.0, Sunset=1.0),
                KAPPA=dict(sky=1.0, clouds=1.0, fog=1.0, light=1.0, amb=1.0, scat=1.0),
                VOL_AMOUNT=1.0, VL_BRANCH='alive', D_MIN=None, DONOR='canonical', NORMALISE=True,
                WL_FILTER=10.0, WL_LIGHT=None, WL_AMB=20.0, WL_SCAT=25.0, CFS_SHARE=0.5, VOL_ON=True)

# ------------------------------------------------------------------ helpers
def lerp(a, b, t): return a + (b - a) * t
def sat(x): return max(0.0, min(1.0, x))
def Y(c): return float(LUM @ np.asarray(c, float))
def curve(c, p): return np.maximum(np.asarray(c, float), 0.0) ** p
def desat(c, d):
    c = np.asarray(c, float); return np.maximum(lerp(c, c.mean(), d), 0.0)
def Dm(d): return (1 - d) * np.eye(3) + d / 3.0 * np.ones((3, 3))
def cfilter(c, f, a): return lerp(np.asarray(c, float), 1.0, a) * np.asarray(f, float)

def tod_weights(h, T=PICTA_TOD):
    h = h % 24
    night, sunrise, dawnD, day, sunset, duskD = T['NightTime'], T['SunriseTime'], T['DawnDuration'], T['DayTime'], T['SunsetTime'], T['DuskDuration']
    tp = [night, sunrise - dawnD, sunrise - dawnD * 0.5, sunrise, day, sunset, sunset + duskD * 0.5, sunset + duskD]
    tp = tp + [x + 24 for x in tp]
    fmap = ['Night', 'Night', 'Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
    ci = ni = 0; cpt = 0.0; npt = 48.0
    for i, t in enumerate(tp):
        if h >= t and t >= cpt: ci, cpt = i, t
        if t > h and npt >= t: ni, npt = i, t
    cf, nf = fmap[ci % 8], fmap[ni % 8]
    td = abs(npt - cpt) or 1.0
    b = abs(h - cpt) / td
    f = {p: 0.0 for p in TODP}
    if cf == nf: f[cf] = 1.0
    else: f[cf] = sat(1 - b); f[nf] = sat(b)
    pd = sat(f['Day'] ** 0.6)
    if pd > 1.17549435e-38:
        if f['Sunrise'] > 1.17549435e-38: f['Sunrise'] = sat(1 - pd)
        if f['Sunset'] > 1.17549435e-38: f['Sunset'] = sat(1 - pd)
    f['Day'] = pd
    return f

def clmt_weights(h, C=PICTA_CLMT):
    """ASSUMED engine rule: record colours peak at the window midpoint."""
    h = h % 24
    rb, re_, sb, se = C; rm, sm = (rb + re_) / 2, (sb + se) / 2
    w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)
    if h < rb or h >= se: w['Night'] = 1.0
    elif h < rm: t = (h - rb) / (rm - rb); w['Night'] = 1 - t; w['Sunrise'] = t
    elif h < re_: t = (h - rm) / (re_ - rm); w['Sunrise'] = 1 - t; w['Day'] = t
    elif h < sb: w['Day'] = 1.0
    elif h < sm: t = (h - sb) / (sm - sb); w['Day'] = 1 - t; w['Sunset'] = t
    else: t = (h - sm) / (se - sm); w['Sunset'] = 1 - t; w['Night'] = t
    return w

def sun_z(h, C=PICTA_CLMT):
    h = h % 24
    rb, re_, sb, se = C; up, down = (rb + re_) / 2, (sb + se) / 2
    if up <= h <= down: e = math.radians(60.0) * math.sin(math.pi * (h - up) / (down - up))
    else:
        d = min(abs(h - up), abs(h - down), abs(h + 24 - up), abs(h - 24 - down))
        e = -math.radians(12.0) * min(1.0, d / 1.5)
    return math.sin(e)

# OKLab
M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])
M1i, M2i = np.linalg.inv(M1), np.linalg.inv(M2)
def to_oklab(c): return M2 @ np.cbrt(M1 @ np.maximum(np.asarray(c, float), 0.0))
def from_oklab(lab): return M1i @ ((M2i @ np.asarray(lab, float)) ** 3)
def norm_y(c, y=0.18):
    c = np.asarray(c, float); yy = Y(c); return c * (y / yy) if yy > 1e-12 else c
def lch(c):
    L, a, b = to_oklab(norm_y(c)); return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360
def _fit_gamut(L, C, hd):
    lo, hi = 0.0, C
    for _ in range(40):
        rgb = from_oklab([L, C * math.cos(math.radians(hd)), C * math.sin(math.radians(hd))])
        if rgb.min() >= -1e-6: return rgb
        hi = C; C = (lo + hi) / 2
    return from_oklab([L, 0, 0])
def blend(cP, cA, a, k=1.0):
    """OKLCh short-arc mix of chromaticity (equal-Y), chroma x k (amplitude, hue fixed), luminance of cP kept."""
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
    L, C, h = lerp(LP, LA, a), lerp(CP, CA, a), (hP + a * dh) % 360
    return norm_y(_fit_gamut(L, C * k, h), yP)
def de_ok(c1, c2): return float(np.linalg.norm(to_oklab(norm_y(c1)) - to_oklab(norm_y(c2))))
def hue_name(h, C):
    if C < 0.012: return 'grey'
    bins = [(12, 'rose-pink'), (35, 'salmon'), (50, 'coral'), (75, 'orange-peach'), (100, 'gold'), (125, 'yellow'),
            (170, 'green'), (215, 'teal'), (250, 'sky-blue'), (272, 'blue'), (292, 'blue-violet'), (315, 'violet-mauve'),
            (340, 'magenta-pink'), (361, 'rose-pink')]
    nm = next(n for lim, n in bins if h < lim)
    q = 'greyish ' if C < 0.03 else ('soft ' if C < 0.06 else '')
    return q + nm
def desc(c):
    if Y(c) <= 1e-12: return 'black'
    L, C, h = lch(c); return f"h{h:5.1f} C{C:.3f} ({hue_name(h, C)})"
def share(vP, vA, vB, k=1.0):
    """on-screen mix share actually reached (0 = Picta, 1 = Astralite chromaticity)."""
    if vA is None or de_ok(vP, vA) < 0.004: return None
    best = min((de_ok(blend(vP, vA, a, k), vB), a) for a in np.arange(0, 1.501, 0.01))
    return round(float(best[1]), 2)

# ------------------------------------------------------------------ data
def j(p): return json.load(open(p, encoding='utf-8'))
PR = j(os.path.join(MAP, 'picta-colour', 'picta_wthr_colours.json'))
PV = j(os.path.join(MAP, 'picta-colour', 'picta_voli.json'))
AR = j(os.path.join(MAP, 'astralite-colour', 'astralite_rotating_weathers_colour.json'))
SC = j(os.path.join(MAP, 'astralite-colour', 'soulcore_e11_colour_keys.json'))
PT = j(os.path.join(MAP, 'pairing', 'pairing_table.json'))
AR_BY = {v['editorid']: k for k, v in AR.items()}

PER_RE = re.compile(r'^(.*?)(InteriorDay|InteriorNight|Dawn|Sunrise|Day|Sunset|Dusk|Night)$')
def parse_val(v):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, (list, tuple)): return np.array([float(x) for x in v[:3]]) if len(v) >= 3 else float(v[0])
    s = str(v).strip().strip('[]')
    if ',' in s:
        try: return np.array([float(x) for x in s.split(',')[:3]])
        except ValueError: return None
    try: return float(s)
    except ValueError: return None

def parse_ini_E(path):
    txt = open(path, 'rb').read().decode('utf-8', errors='replace')
    E = {}; RAW = {}; sec = None
    for line in txt.splitlines():
        s = line.strip()
        m = re.match(r'^\[(.+)\]$', s)
        if m: sec = m.group(1); continue
        if not sec or '=' not in s or s.startswith(';'): continue
        k, v = s.split('=', 1); k = k.strip(); v = v.strip()
        RAW.setdefault(sec, {})[k] = v
        mm = PER_RE.match(k)
        if not mm: continue
        val = parse_val(v)
        if val is None: continue
        E.setdefault(sec, {}).setdefault(mm.group(1), {})[mm.group(2)] = val
    return E, RAW

def soul_E(fname):
    vals = SC['weather_files'].get(fname, {}).get('values', {}); base = SC['base_values']
    E = {}
    for full in set(base) | set(vals):
        src = vals.get(full) or base.get(full)
        sec, key = full.split('.', 1)
        if 'value' in src:
            v = parse_val(src['value'])
            if v is None: continue
            E.setdefault(sec, {})[key] = {p: v for p in ALLP}
        else:
            d = {p: parse_val(src.get(p)) for p in ALLP if src.get(p) is not None}
            if d: E.setdefault(sec, {})[key] = d
    return E

def default_for(key):
    if key.endswith('ColorFilter') or key == 'ScatteringColor': return np.ones(3)
    if 'Desaturation' in key or key.endswith('FilterAmount') or key in ('ShadowAmount', 'DustDensity', 'DustDarkening'): return 0.0
    return 1.0

def ev(E, sec, key, h, T=PICTA_TOD, ovr=None):
    w = tod_weights(h, T); acc = None
    for p in TODP:
        if w[p] <= 0: continue
        if ovr is not None and p in ovr: v = ovr[p]
        else: v = E.get(sec, {}).get(key, {}).get(p)
        if v is None: v = default_for(key)
        acc = w[p] * np.asarray(v, float) if acc is None else acc + w[p] * np.asarray(v, float)
    return acc if np.ndim(acc) else float(acc)

def rgb01(x): return np.array(x, float) / 255.0
def picta_records(fid):
    x = PR[fid + ':Picta - Weathers of Aurbis.esm']; c = x['colours']; R = {}
    cl = x.get('clouds_enabled') or []
    for s in SLOTS:
        R[s] = dict(upper=rgb01(c['SkyUpperColor'][s]), horizon=rgb01(c['HorizonColor'][s]), lower=rgb01(c['SkyLowerColor'][s]),
                    fogfar=rgb01(c['FogFarColor'][s]), fognear=rgb01(c['FogNearColor'][s]), sun=rgb01(c['SunColor'][s]),
                    sunlight=rgb01(c['SunlightColor'][s]), statics=rgb01(c['SkyStaticsColor'][s]),
                    cloud=rgb01(cl[0]['colors'][s]) if cl else rgb01([250, 250, 250]),
                    dalc={ax: rgb01(c['DALC'][s][ax]) for ax in AXES})
    R['_voli'] = {s: x['voli'][s] for s in SLOTS}; R['_edid'] = x['editorid']
    return R
def astra_records(name):
    x = AR[AR_BY[name]]; c = x['colors']; R = {}
    clouds = [cl for cl in x['clouds'] if str(cl['enabled']) == 'True'] or x['clouds']
    for s in SLOTS:
        R[s] = dict(upper=rgb01(c['SkyUpperColor'][s]), horizon=rgb01(c['HorizonColor'][s]), lower=rgb01(c['SkyLowerColor'][s]),
                    fogfar=rgb01(c['FogFarColor'][s]), fognear=rgb01(c['FogNearColor'][s]), sun=rgb01(c['SunColor'][s]),
                    sunlight=rgb01(c['SunlightColor'][s]), statics=rgb01(c['SkyStaticsColor'][s]),
                    cloud=rgb01(clouds[0]['colors'][s]) if clouds else rgb01(c['HorizonColor'][s]),
                    dalc={ax: rgb01(x['dalc'][s][ax]) for ax in AXES})
    R['_voli'] = x['volumetric_resolved']; R['_edid'] = x['editorid']; R['_soul'] = x.get('e11_weather_file') or 'SoulClear.ini'
    return R
def rec_at(R, h, key, C=PICTA_CLMT, ax=None):
    w = clmt_weights(h, C); acc = 0.0
    for s in SLOTS:
        if w[s] <= 0: continue
        v = R[s]['dalc'][ax] if key == 'dalc' else R[s][key]
        acc = acc + w[s] * v
    return np.asarray(acc, float) * np.ones(3)

# ------------------------------------------------------------------ channel models (pre-tonemap engine-value space)
BAND = {'top': ('upper', 'GradientTop'), 'hor': ('horizon', 'GradientHorizon')}
def B_band(E, R, h, band, T=PICTA_TOD, C=PICTA_CLMT):
    rk, nm = BAND[band]
    m = curve(rec_at(R, h, rk, C), ev(E, 'SKY', nm + 'Curve', h, T)) * ev(E, 'SKY', nm + 'Intensity', h, T) * ev(E, 'SKY', 'GradientIntensity', h, T)
    return Dm(ev(E, 'SKY', 'GradientDesaturation', h, T)) @ np.diag(m)
def V_band(E, R, h, band, T=PICTA_TOD, C=PICTA_CLMT):
    rk, nm = BAND[band]
    c = curve(rec_at(R, h, rk, C), ev(E, 'SKY', nm + 'Curve', h, T)) * ev(E, 'SKY', nm + 'ColorFilter', h, T) * ev(E, 'SKY', nm + 'Intensity', h, T) * ev(E, 'SKY', 'GradientIntensity', h, T)
    return desat(c, ev(E, 'SKY', 'GradientDesaturation', h, T))
def B_cloud(E, R, h, T=PICTA_TOD, C=PICTA_CLMT):
    m = curve(rec_at(R, h, 'cloud', C), ev(E, 'SKY', 'CloudsCurve', h, T)) * ev(E, 'SKY', 'CloudsIntensity', h, T)
    return Dm(ev(E, 'SKY', 'CloudsDesaturation', h, T)) @ np.diag(m)
def V_cloud(E, R, h, T=PICTA_TOD, C=PICTA_CLMT):
    c = curve(rec_at(R, h, 'cloud', C), ev(E, 'SKY', 'CloudsCurve', h, T)) * ev(E, 'SKY', 'CloudsColorFilter', h, T) * ev(E, 'SKY', 'CloudsIntensity', h, T)
    return desat(c, ev(E, 'SKY', 'CloudsDesaturation', h, T))
def B_fog(E, R, h, key='fogfar', T=PICTA_TOD, C=PICTA_CLMT):
    a = ev(E, 'ENVIRONMENT', 'FogColorFilterAmount', h, T)
    m = lerp(curve(rec_at(R, h, key, C), ev(E, 'ENVIRONMENT', 'FogColorCurve', h, T)), 1.0, a) * ev(E, 'ENVIRONMENT', 'FogColorMultiplier', h, T)
    return np.diag(m)
def V_fog(E, R, h, key='fogfar', T=PICTA_TOD, C=PICTA_CLMT):
    return cfilter(curve(rec_at(R, h, key, C), ev(E, 'ENVIRONMENT', 'FogColorCurve', h, T)), ev(E, 'ENVIRONMENT', 'FogColorFilter', h, T),
                   ev(E, 'ENVIRONMENT', 'FogColorFilterAmount', h, T)) * ev(E, 'ENVIRONMENT', 'FogColorMultiplier', h, T)
def V_volfog(E, h, T=PICTA_TOD): return ev(E, 'VOLUMETRICFOG', 'ColorFilter', h, T) * ev(E, 'VOLUMETRICFOG', 'Intensity', h, T)
def light_pre(E, R, h, T=PICTA_TOD, C=PICTA_CLMT):
    return desat(curve(rec_at(R, h, 'sunlight', C), ev(E, 'ENVIRONMENT', 'DirectLightingCurve', h, T)), ev(E, 'ENVIRONMENT', 'DirectLightingDesaturation', h, T))
def B_light(E, R, h, T=PICTA_TOD, C=PICTA_CLMT):
    a = ev(E, 'ENVIRONMENT', 'DirectLightingColorFilterAmount', h, T)
    return np.diag(lerp(light_pre(E, R, h, T, C), 1.0, a) * ev(E, 'ENVIRONMENT', 'DirectLightingIntensity', h, T))
def V_light(E, R, h, T=PICTA_TOD, C=PICTA_CLMT): return B_light(E, R, h, T, C) @ ev(E, 'ENVIRONMENT', 'DirectLightingColorFilter', h, T)
def B_amb(E, h, T=PICTA_TOD): return ev(E, 'ENVIRONMENT', 'AmbientLightingIntensity', h, T) * Dm(ev(E, 'ENVIRONMENT', 'AmbientLightingDesaturation', h, T))
def V_amb(E, R, h, ax, T=PICTA_TOD, C=PICTA_CLMT): return B_amb(E, h, T) @ rec_at(R, h, 'dalc', C, ax)
def V_sundisc(E, R, h, T=PICTA_TOD, C=PICTA_CLMT):
    return cfilter(desat(rec_at(R, h, 'sun', C), ev(E, 'SKY', 'SunDesaturation', h, T)), ev(E, 'SKY', 'SunColorFilter', h, T), 0.0)
def scat_parts(E, R, h, view, T=PICTA_TOD, C=PICTA_CLMT, SCo=None, CFS=None):
    """Effects11.cpp 180-222 + SkyScattering.hlsli ApplySkyScattering pieces (incl. hue-dependent dust)."""
    g = lambda k, d=None: ev(E, 'SKYSCATTERING', k, h, T)
    sunc = V_sundisc(E, R, h, T, C); sunN = np.maximum(sunc, 0) / max(float(sunc.max()), 1.0)
    sz = sun_z(h, C); cz = math.sqrt(max(0.0, 1 - sz * sz)); sd = np.array([0.0, cz, sz])
    sunFade = math.sqrt(sat(1 + 2 * sz))
    cfs = ev(E, 'SKYSCATTERING', 'ColorFromSun', h, T, ovr=CFS); scol = ev(E, 'SKYSCATTERING', 'ScatteringColor', h, T, ovr=SCo)
    m = (1.0 + (sunN - 1.0) * cfs) * sunFade
    color = m * scol
    peak = max(float(color.max()), 1e-6); dd = g('DustDensity'); tint = np.maximum(0.0, 1.0 - color / peak) * 2 * dd * dd
    z = view[2]; elev = 1 - sat(1 - z) * sat(1 + sz); dustVol = 0.02 / max(g('DustVolume') ** 2, 1e-7)
    band = sat(1 - elev * dustVol) ** 32
    aboveH = sat(1 + z * 10) ** 2
    dust = np.clip(1.0 - band * tint, 0, 1) ** 32
    k = g('Intensity') * aboveH * (1 - band * g('DustDarkening'))
    return dict(m=m, color=color, dust=dust, k=k, scat=color * dust * k, sd=sd, sz=sz, elev=elev, band=band, aboveH=aboveH)
def earth_shadow(elev, facing, sunH):
    tw = 0.1 - sunH; th = lerp(0.8 + 0.3 * sat(tw * 5), 0.95 + sat(sunH * -0.5), facing); sp = sat(1 - tw * 3)
    s = sat(1 + elev - th) * (4 * (0.1 + sp * sp)) * (1 + facing * 4)
    s = s * s * (3 - 2 * s); return s * s * (3 - 2 * s)
def sky_pixel(E, R, h, view, T=PICTA_TOD, C=PICTA_CLMT):
    g = lambda k: ev(E, 'SKYSCATTERING', k, h, T)
    top = V_band(E, R, h, 'top', T, C); hz = V_band(E, R, h, 'hor', T, C)
    z = view[2]; sky = lerp(top, hz, (1 - sat(z)) ** ev(E, 'SKY', 'ProceduralGradientWeightCurve', h, T))
    sp = scat_parts(E, R, h, view, T, C)
    facing = sat(float(view @ sp['sd']) * 0.5 + 0.5); away = 1 - facing
    hR = 1 / max(g('HorizonRange') ** 3, 1e-6); aT = 100 / max(g('AtmosphereThickness') ** 2, 1e-6)
    agR = 1 / max(g('AirGlowRange') ** 2, 1e-6); sgR = 10 / max(g('SunGlowRange') ** 2, 1e-6)
    spread = lerp(hR * away * away, aT, sp['elev'] ** 2)
    res = sky * (1 + g('AirGlowIntensity') / (1 + away * agR))
    res = lerp(res, sp['scat'], sat(g('Amount') ** 2 / (1 + away * spread)))
    sunAbove = sat(1 + z * 40) ** 2
    res = res * (1 + g('SunGlowIntensity') * sunAbove / (1 + away * sgR))
    sh = lerp(1.0, earth_shadow(sp['elev'], facing, sp['sz']), sat(g('ShadowAmount')))
    return lerp(sky, lerp(top * 0.5, res, sh), sp['aboveH'])
def views(h, C=PICTA_CLMT):
    v = {'zenith': np.array([0, 0, 1.0]), 'hor_sun': np.array([0, math.sqrt(1 - .05 ** 2), .05]),
         'hor_away': np.array([0, -math.sqrt(1 - .05 ** 2), .05]), 'mid_away': np.array([0, -math.sqrt(1 - .44 ** 2), .44])}
    return v
IBL_DIRS = []
for el in (5, 15, 30, 50, 70, 85):
    for az in range(0, 360, 45):
        e, a = math.radians(el), math.radians(az)
        IBL_DIRS.append((np.array([math.cos(e) * math.sin(a), math.cos(e) * math.cos(a), math.sin(e)]), math.sin(e) * math.cos(e)))
def sky_ibl(E, R, h):
    """cosine-weighted dome average (proxy for the sky-IBL SH term; SkyIBLScale = [IMAGEBASEDLIGHTING] MultiplicativeAmount)."""
    acc = np.zeros(3); ws = 0.0
    for d, w in IBL_DIRS: acc += w * sky_pixel(E, R, h, d); ws += w
    return acc / ws * ev(E, 'IMAGEBASEDLIGHTING', 'MultiplicativeAmount', h)

# ------------------------------------------------------------------ pairing
FILES = {}
WL_TXT = open(DARK + '/_weatherlist.ini', 'rb').read().decode('utf-8', 'replace')
for m in re.finditer(r'\[(WEATHER\d+)\]\s*\r?\nFileName=(.+?)\r?\nWeatherIDs=(.+?)\r?\n', WL_TXT):
    sec, fn, ids = m.group(1), m.group(2).strip(), [x.strip() for x in m.group(3).split(',')]
    if (fn.startswith('Picta - Weathers/00_Master/') or fn.startswith('Authoria - Summer/')) and sec != 'WEATHER901':
        FILES[fn] = ids
COLOUR_PARTNER = {'A01': 'SkyrimClear', 'A02': 'SkyrimClear', 'A03': 'SkyrimClear', 'B01': 'SkyrimClear', 'B02': 'SkyrimClear',
                  'B03': 'SkyrimCloudy', 'C01': 'SkyrimCloudy', 'C02': 'SkyrimCloudy', 'C03': 'SkyrimCloudy',
                  'C04': 'SkyrimOvercastRain', 'D03': 'SkyrimOvercastRain', 'D04': 'SkyrimOvercastRain',
                  'C05': 'SkyrimOvercastSnow', 'D05': 'SkyrimOvercastSnow', 'D06': 'SkyrimOvercastSnow',
                  'D01': 'SkyrimFog', 'D02': 'SkyrimFog',
                  'E01': 'SkyrimStormRain', 'E03': 'SkyrimStormRain', 'E04': 'SkyrimStormRain',
                  'E02': 'SkyrimStormSnow', 'E05': 'SkyrimStormSnow', 'E06': 'SkyrimStormSnow'}
def wclass(fid):
    ed = PR[fid + ':Picta - Weathers of Aurbis.esm']['editorid']
    return re.search(r'_([A-E]\d\d)_', ed).group(1)
def colour_partner(fid): return COLOUR_PARTNER[wclass(fid)]
def mist_partner(fid):
    c = wclass(fid)
    if c in ('A02', 'B02'): return 'SkyrimClear_A'
    if c in ('B03', 'C03', 'D01', 'D02'): return 'SkyrimFog'
    return colour_partner(fid)
RINGS = {'Lite': ['A01', 'A03', 'B01', 'C01'], 'Heavy': ['B03', 'C03', 'D01', 'D02'], 'Rain': ['C04', 'D03', 'D04', 'C05', 'D05', 'D06']}
MOT_BANKS = ['A01', 'A02', 'A03', 'B01', 'B02', 'B03', 'C01', 'C02', 'C03', 'D01', 'D02']
ACHROMATIC = {'SkyrimOvercastRain', 'SkyrimFog', 'SkyrimStormRain'}

def family_members(picta_edid):
    agg = {}
    for fam, d in PT['family_partner_summary'].items():
        for name, w in dict(d).get(picta_edid, []):
            if name in AR_BY: agg[name] = agg.get(name, 0.0) + w
    t = sum(agg.values())
    return {k: v / t for k, v in agg.items()} if t > 0 else None

class Astra:
    """Astralite visible colours for a donor = one canonical partner, or a family mix in unit-luminance chroma space."""
    def __init__(self, members):
        self.mem = [(astra_records(n), soul_E(astra_records(n)['_soul']), w) for n, w in members.items()]
        self.R0, self.E0 = self.mem[0][0], self.mem[0][1]
    def vis(self, fn, *a, **k):
        acc = np.zeros(3); ws = 0.0
        for R, E, w in self.mem:
            c = fn(E, R, *a, **k)
            if Y(c) > 1e-12: acc += w * norm_y(c, 1.0); ws += w
        return acc / ws if ws > 0 else None

# ------------------------------------------------------------------ solvers
def alpha_fn(D, ALPHA, comp):
    def a(h):
        c = clmt_weights(h); return sum(c[s] * ALPHA[comp][s] for s in RSLOTS)
    return a
def kstr_fn(D, comp):
    def k(h):
        c = clmt_weights(h); return (sum(c[s] * D['STRENGTH'][s] for s in RSLOTS) + c['Night']) * D['KAPPA'][comp]
    return k

def solve_periods(cases, F_night, WL):
    """cases: list of (Bfun, target_fn, yP_fn). V(h) = B(h) @ F(h), F(h) = sum_p w_p F_p + w_N F_N.
    rows: chromaticity (V-T)/Y(T) per channel (weight 1) + luminance (Y(V)-Y_P)/Y_P (weight WL)."""
    rows, rhs = [], []
    for Bf, Tf, Yf in cases:
        for h in FIT_H:
            w = tod_weights(h)
            if sum(w[p] for p in FREE) <= 0: continue
            B = Bf(h); t = Tf(h); yp = Yf(h)
            if yp <= 1e-9: continue
            const = B @ (w['Night'] * np.asarray(F_night, float))
            for ch in range(3):
                r = np.zeros(15)
                for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = w[p] * B[ch, :] / yp
                rows.append(r); rhs.append((t[ch] - const[ch]) / yp)
            lb = LUM @ B; r = np.zeros(15)
            for i, p in enumerate(FREE): r[3 * i:3 * i + 3] = WL * w[p] * lb / yp
            rows.append(r); rhs.append(WL * (yp - Y(const)) / yp)
    x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
    x = np.clip(x, 0.0, 10.0)
    return {p: x[3 * i:3 * i + 3] for i, p in enumerate(FREE)}

def snap(new, old, tol=5e-4):
    new = np.asarray(new, float); old = np.asarray(old, float)
    return old.copy() if np.all(np.abs(new - old) < tol) else new

def solve_file(fn, D, verbose=False):
    E_P, RAW = parse_ini_E(DARK + '/' + fn)
    ws = FILES[fn]; RP = {w: picta_records(w) for w in ws}
    cp = colour_partner(ws[0])
    if D['DONOR'] == 'family_achromatic' and cp in ACHROMATIC:
        mem = family_members(RP[ws[0]]['_edid']) or {cp: 1.0}
    else: mem = {cp: 1.0}
    A = Astra(mem)
    ALPHA = {comp: dict(D['MIX']) for comp in ('sky', 'clouds', 'fog', 'light', 'amb', 'scat')}
    E_B = copy.deepcopy(E_P)
    out = dict(file=fn, weathers=ws, colour_partner=cp, donor_members=mem, e11={}, records={}, notes=[])

    def channel_specs():
        return [('sky', 'SKY', 'GradientTopColorFilter', lambda E, R, h: B_band(E, R, h, 'top'), lambda E, R, h: V_band(E, R, h, 'top')),
                ('sky', 'SKY', 'GradientHorizonColorFilter', lambda E, R, h: B_band(E, R, h, 'hor'), lambda E, R, h: V_band(E, R, h, 'hor')),
                ('clouds', 'SKY', 'CloudsColorFilter', lambda E, R, h: B_cloud(E, R, h), lambda E, R, h: V_cloud(E, R, h)),
                ('fog', 'ENVIRONMENT', 'FogColorFilter', lambda E, R, h: B_fog(E, R, h), lambda E, R, h: V_fog(E, R, h))]

    def run_filters(ALPHA):
        res = {}
        for comp, sec, key, Bf, Vf in channel_specs():
            af, kf = alpha_fn(D, ALPHA, comp), kstr_fn(D, comp)
            cases = []
            for w, R in RP.items():
                Va = lambda h, Vf=Vf: A.vis(lambda E, R_, hh: Vf(E, R_, hh), h)
                cases.append((lambda h, R=R, Bf=Bf: Bf(E_P, R, h),
                              lambda h, R=R, Vf=Vf, Va=Va: blend(Vf(E_P, R, h), Va(h), af(h), kf(h)),
                              lambda h, R=R, Vf=Vf: Y(Vf(E_P, R, h))))
            F = solve_periods(cases, E_P[sec][key]['Night'], D['WL_FILTER'])
            res[(sec, key)] = {p: snap(F[p], E_P[sec][key][p]) for p in FREE}
        return res

    # --- light (DirectLightingColorFilter + DirectLightingDesaturation unlock)
    def period_alpha(ALPHA, comp):
        af = alpha_fn(D, ALPHA, comp); out_ = {}
        for p in FREE:
            wsum = [tod_weights(h)[p] for h in FIT_H]; s = sum(wsum)
            out_[p] = sum(wv * af(h) for wv, h in zip(wsum, FIT_H)) / s if s > 0 else 0.0
        return out_
    def run_light(ALPHA):
        ap = period_alpha(ALPHA, 'light'); DLD = {}
        for p in FREE:
            dP = E_P['ENVIRONMENT']['DirectLightingDesaturation'][p]
            DLD[p] = D['D_MIN'] if (D['D_MIN'] is not None and ap[p] > 1e-6 and dP < D['D_MIN']) else dP
        E_t = copy.deepcopy(E_P)
        for p in FREE: E_t['ENVIRONMENT']['DirectLightingDesaturation'][p] = DLD[p]
        af, kf = alpha_fn(D, ALPHA, 'light'), kstr_fn(D, 'light')
        best = None
        for WL in ([D['WL_LIGHT']] if D['WL_LIGHT'] else [100, 400, 1000]):
            cases = []
            for w, R in RP.items():
                Va = lambda h, R=R: A.vis(lambda E, R_, hh: V_light(E, R_, hh), h)
                cases.append((lambda h, R=R: B_light(E_t, R, h), lambda h, R=R, Va=Va: blend(V_light(E_P, R, h), Va(h), af(h), kf(h)),
                              lambda h, R=R: Y(V_light(E_P, R, h))))
            F = solve_periods(cases, E_P['ENVIRONMENT']['DirectLightingColorFilter']['Night'], WL)
            E_x = copy.deepcopy(E_t)
            for p in FREE: E_x['ENVIRONMENT']['DirectLightingColorFilter'][p] = F[p]
            worst = max(abs(Y(V_light(E_x, R, h)) / Y(V_light(E_P, R, h)) - 1) for R in RP.values() for h in AUDIT_H if Y(V_light(E_P, R, h)) > 1e-6)
            if best is None or worst < best[0] - 1e-9: best = (worst, WL, F)
            if worst <= 0.005: break
        F = {p: snap(best[2][p], E_P['ENVIRONMENT']['DirectLightingColorFilter'][p]) for p in FREE}
        return F, DLD, best[1]

    # --- scattering (ColorFromSun lerp + ScatteringColor, dust-aware fixed point)
    def run_scat(ALPHA):
        ap = period_alpha(ALPHA, 'scat')
        CFS = {p: float(lerp(E_P['SKYSCATTERING']['ColorFromSun'][p], ev(A.E0, 'SKYSCATTERING', 'ColorFromSun', {'Dawn': 7.25, 'Sunrise': 9, 'Day': 13, 'Sunset': 17, 'Dusk': 18.75}[p]), D['CFS_SHARE'] * ap[p])) for p in FREE}
        if all(abs(CFS[p] - E_P['SKYSCATTERING']['ColorFromSun'][p]) < 5e-4 for p in FREE):
            CFS = {p: E_P['SKYSCATTERING']['ColorFromSun'][p] for p in FREE}
        af, kf = alpha_fn(D, ALPHA, 'scat'), kstr_fn(D, 'scat')
        vsun = views(0)['hor_sun']
        SCo = {p: E_P['SKYSCATTERING']['ScatteringColor'][p] for p in FREE}
        for it in range(5):
            cases = []
            for w, R in RP.items():
                def Bf(h, R=R, SCo=SCo):
                    sp = scat_parts(E_P, R, h, vsun, SCo=SCo, CFS=CFS); return np.diag(sp['m'] * sp['dust'] * sp['k'])
                def Tf(h, R=R):
                    vp = scat_parts(E_P, R, h, vsun)['scat']
                    va = A.vis(lambda E, R_, hh: scat_parts(E, R_, hh, vsun)['scat'], h)
                    return blend(vp, va, af(h), kf(h))
                cases.append((Bf, Tf, lambda h, R=R: Y(scat_parts(E_P, R, h, vsun)['scat'])))
            new = solve_periods(cases, E_P['SKYSCATTERING']['ScatteringColor']['Night'], D['WL_SCAT'])
            SCo = {p: new[p] for p in FREE}
        SCo = {p: snap(SCo[p], E_P['SKYSCATTERING']['ScatteringColor'][p]) for p in FREE}
        return SCo, CFS

    def apply(ALPHA):
        Eb = copy.deepcopy(E_P)
        fl = run_filters(ALPHA)
        for (sec, key), d in fl.items():
            for p in FREE: Eb[sec][key][p] = d[p]
        DLF, DLD, wl = run_light(ALPHA)
        for p in FREE:
            Eb['ENVIRONMENT']['DirectLightingColorFilter'][p] = DLF[p]; Eb['ENVIRONMENT']['DirectLightingDesaturation'][p] = DLD[p]
        SCo, CFS = run_scat(ALPHA)
        for p in FREE:
            Eb['SKYSCATTERING']['ScatteringColor'][p] = SCo[p]; Eb['SKYSCATTERING']['ColorFromSun'][p] = CFS[p]
        # [VOLUMETRICFOG] ColorFilter is left Picta: Bottled applies it only to non-effect-lit soft meshes and every
        # fog/mist mesh in this lane is effect-lit (map_fog-mist), so re-hueing it would only tint unrelated effects.
        return Eb, wl

    # --- MIX normalisation: on-screen share at the record peaks == MIX label
    comp_probe = {'sky': lambda E, R, h: V_band(E, R, h, 'hor'), 'clouds': V_cloud, 'fog': lambda E, R, h: V_fog(E, R, h),
                  'light': lambda E, R, h: V_light(E, R, h), 'scat': lambda E, R, h: scat_parts(E, R, h, views(0)['hor_sun'])['scat']}
    Rr = RP[ws[0]]
    E_B, wl = apply(ALPHA)
    gains = {}
    if D['NORMALISE'] and any(v > 0 for v in D['MIX'].values()):
        for it in range(2):
            for comp, Vf in comp_probe.items():
                for s, hs in PEAK.items():
                    lab = D['MIX'][s]
                    if lab <= 0 or (comp == 'light' and s != 'Day'): continue
                    va = A.vis(lambda E, R_, hh: Vf(E, R_, hh), hs)
                    if va is None or de_ok(Vf(E_P, Rr, hs), va) < 0.02: continue
                    sh = share(Vf(E_P, Rr, hs), va, Vf(E_B, Rr, hs), kstr_fn(D, comp)(hs))
                    if sh is None or sh <= 0.02: continue
                    ALPHA[comp][s] = float(np.clip(ALPHA[comp][s] * lab / sh, 0.0, min(1.0, 2.0 * lab)))
            ALPHA['amb'] = dict(ALPHA['sky'])  # ambient is record-carried at the peaks: no two-clock loss -> label as is
            ALPHA['amb'] = dict(D['MIX'])
            E_B, wl = apply(ALPHA)
    out['alpha_used'] = {c: {s: round(v, 3) for s, v in d.items()} for c, d in ALPHA.items()}
    out['light_luma_weight'] = wl

    # --- DALC (records) per weather: joint hourly solve per axis + integer search
    RB = {}
    for w, R in RP.items():
        Rb = copy.deepcopy(R); af, kf = alpha_fn(D, ALPHA, 'amb'), kstr_fn(D, 'amb'); recs = {}
        for ax in AXES:
            rows, rhs = [], []
            for h in FIT_H:
                c = clmt_weights(h)
                if sum(c[s] for s in RSLOTS) <= 0: continue
                Bm = B_amb(E_P, h); vp = V_amb(E_P, R, h, ax); yp = Y(vp)
                if yp <= 1e-9: continue
                va = A.vis(lambda E, R_, hh: V_amb(E, R_, hh, ax), h)
                t = blend(vp, va, af(h), kf(h)); const = Bm @ (c['Night'] * R['Night']['dalc'][ax])
                for ch in range(3):
                    r = np.zeros(9)
                    for i, s in enumerate(RSLOTS): r[3 * i:3 * i + 3] = c[s] * Bm[ch, :] / yp
                    rows.append(r); rhs.append((t[ch] - const[ch]) / yp)
                lb = LUM @ Bm; r = np.zeros(9)
                for i, s in enumerate(RSLOTS): r[3 * i:3 * i + 3] = D['WL_AMB'] * c[s] * lb / yp
                rows.append(r); rhs.append(D['WL_AMB'] * (yp - Y(const)) / yp)
            x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
            for i, s in enumerate(RSLOTS):
                tgt = np.clip(x[3 * i:3 * i + 3], 0, 254.4 / 255) * 255
                old = R[s]['dalc'][ax] * 255
                if np.all(np.abs(tgt - old) < 0.5): recs[(s, ax)] = np.round(old); continue
                base = np.round(tgt); bestc = None
                hrs = [h for h in FIT_H if clmt_weights(h)[s] >= 0.5]
                for dl in itertools.product((-1, 0, 1), repeat=3):
                    cc = np.clip(base + np.array(dl), 0, 255); Rt = copy.deepcopy(Rb); Rt[s]['dalc'][ax] = cc / 255
                    err = max(abs(Y(V_amb(E_P, Rt, h, ax)) / max(Y(V_amb(E_P, R, h, ax)), 1e-9) - 1) for h in hrs)
                    err += 0.002 * float(np.abs(norm_y(cc, 1) - norm_y(tgt, 1)).sum())
                    if bestc is None or err < bestc[0]: bestc = (err, cc)
                Rb[s]['dalc'][ax] = bestc[1] / 255; recs[(s, ax)] = bestc[1]
            for s in RSLOTS: Rb[s]['dalc'][ax] = recs[(s, ax)] / 255
        RB[w] = Rb
        out['records'][w] = dict(editorid=R['_edid'], DALC={s: {ax: [int(v) for v in recs[(s, ax)]] for ax in AXES} for s in RSLOTS},
                                 DALC_picta={s: {ax: [int(round(v * 255)) for v in R[s]['dalc'][ax]] for ax in AXES} for s in RSLOTS})
        # optional (default OFF) SkyStaticsColor re-hue, Y-locked
        ssc = {}
        for s, hs in PEAK.items():
            vp = R[s]['statics'] * 255; va = A.vis(lambda E, R_, hh: R_[s]['statics'], hs)
            t = blend(vp, va, D['MIX'][s], kstr_fn(D, 'fog')(hs))
            if t.max() > 254.4: t = norm_y(blend(vp, va, D['MIX'][s] * 0.7, 1.0), Y(vp))
            ssc[s] = [int(v) for v in np.clip(np.round(t), 0, 255)]
        out['records'][w]['SkyStaticsColor_optional'] = ssc
    out['_E_P'], out['_E_B'], out['_RP'], out['_RB'], out['_A'], out['_RAW'] = E_P, E_B, RP, RB, A, RAW
    return out

# ------------------------------------------------------------------ volumetric light
def picta_voli(fid_voli):
    f = PV[fid_voli]['fields']
    return dict(I=float(f.get('Intensity', 1)), cc=float(f.get('CustomColorContribution', 0)),
                col=np.array([float(f['ColorR']), float(f['ColorG']), float(f['ColorB'])]), dens=float(f.get('DensityContribution', 0)),
                rf=float(f.get('SamplingRepartitionRangeFactor', 100)), name=PV[fid_voli]['editorid'])
def astra_voli(v):
    return dict(I=float(v['intensity']), cc=float(v['custom_color_contribution']), col=np.array(v['color_rgb01'], float),
                dens=float(v['density_contribution']), rf=float(v['sampling_range_factor']), name=v['editorid'], formid=v['formid'])
def voli_at(sl, h, K=None):
    c = clmt_weights(h); I_ = cc = d = 0.0; col = np.zeros(3)
    for s in SLOTS:
        v = sl[s]; k = (K.get(v['name'], 1.0) if (K is not None and s != 'Night') else 1.0)
        I_ += c[s] * v['I'] * k; cc += c[s] * v['cc']; col = col + c[s] * v['col']; d += c[s] * v['dens']
    return I_, cc, col, d
def vl_rad(I_, cc, col, L, G, GF):
    return I_ * G * Y(np.asarray(GF) * lerp(L, col, cc))

def solve_vl(results, D, K_fixed=None):
    """GVR Intensity per file (Dawn..Dusk) + one regime factor K per Astralite VOLI copy, crossfades included."""
    branch = D['VL_BRANCH']; VOL = D['VOL_AMOUNT']
    W = []   # per weather: dict with everything needed
    for r in results.values():
        E_P, E_B = r['_E_P'], r['_E_B']
        for w in r['weathers']:
            R = r['_RP'][w]; mp = mist_partner(w); AR_ = astra_records(mp); SE = soul_E(AR_['_soul'])
            pslots = {s: picta_voli(R['_voli'][s]) for s in SLOTS}
            bslots = {s: (astra_voli(AR_['_voli'][s]) if s != 'Night' else pslots['Night']) for s in SLOTS}
            relA = {}
            for s, hs in dict(Sunrise=7.0, Day=13.0, Sunset=19.0).items():
                v = bslots[s]
                LA = V_light(SE, AR_, hs, NAT_TOD, ASTRA_CLMT)
                gA = ev(SE, 'GAMEVOLUMETRICRAYS', 'Intensity', hs, NAT_TOD); gF = ev(SE, 'GAMEVOLUMETRICRAYS', 'ColorFilter', hs, NAT_TOD)
                relA[s] = v['I'] * gA * Y(gF * lerp(LA, v['col'], v['cc'])) / max(Y(LA), 1e-9)
            def relP(h, E_P=E_P, R=R, pslots=pslots):
                if branch == 'newly_on': return 0.0
                L = V_light(E_P, R, h); I_, cc, col, dd = voli_at(pslots, h)
                return vl_rad(I_, cc, col, L, ev(E_P, 'GAMEVOLUMETRICRAYS', 'Intensity', h), ev(E_P, 'GAMEVOLUMETRICRAYS', 'ColorFilter', h)) / max(Y(L), 1e-9)
            def target(h, relA=relA, relP=relP):
                c = clmt_weights(h); rp = relP(h)
                t = VOL * sum(c[s] * relA[s] for s in RSLOTS) + c['Night'] * rp
                return max(t, rp)
            W.append(dict(file=r['file'], w=w, E_P=E_P, E_B=E_B, R=R, pslots=pslots, bslots=bslots, relA=relA, relP=relP, target=target, partner=mp))
    names = sorted({wd['bslots'][s]['name'] for wd in W for s in RSLOTS})
    K = {n: 1.25 / next(wd['bslots'][s]['I'] for wd in W for s in RSLOTS if wd['bslots'][s]['name'] == n) for n in names}
    if K_fixed: K = dict(K_fixed)
    files = sorted({wd['file'] for wd in W})
    GN = {f: (0.0 if branch == 'newly_on' else float(results[f]['_E_P']['GAMEVOLUMETRICRAYS']['Intensity']['Night'])) for f in files}
    GP = {f: {p: float(results[f]['_E_P']['GAMEVOLUMETRICRAYS']['Intensity'][p]) for p in FREE} for f in files}
    G = {f: dict(GP[f]) for f in files}
    def GF_B(wd, h):
        # luma-equal grey in Dawn..Dusk: no double tint on the Astralite custom colour, Picta's VL luminance kept in crossfades
        w = tod_weights(h); gf = wd['E_P']['GAMEVOLUMETRICRAYS']['ColorFilter']
        return sum(w[p] * (Y(gf[p]) * np.ones(3) if p in FREE else gf[p]) for p in TODP)
    def a_of(wd, h):
        L = V_light(wd['E_B'], wd['R'], h); I_, cc, col, dd = voli_at(wd['bslots'], h, K)
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
                    q = rad_of(wd, h) / t; worst = max(worst, q)
                    if q > CAP: capw[(wd['w'], h)] = capw.get((wd['w'], h), 1.0) * 3.0
            if worst <= CAP + 1e-3: break
    rep = {}
    for wd in W:
        f = wd['file']; rows = []; over = (0.0, None); under = (9.0, None)
        for h in AUDIT_H:
            t = wd['target'](h); w = tod_weights(h)
            rad = a_of(wd, h) * (sum(w[p] * G[f][p] for p in FREE) + w['Night'] * GN[f])
            if t > 1e-6:
                q = rad / t
                if q > over[0]: over = (q, h)
                if q < under[0]: under = (q, h)
            if h in (6.5, 7.0, 7.25, 7.5, 9.0, 13.0, 17.0, 18.5, 18.75, 19.5, 20.0):
                Lp = V_light(wd['E_P'], wd['R'], h); Ip, ccp, colp, dp = voli_at(wd['pslots'], h)
                Ib, ccb, colb, db = voli_at(wd['bslots'], h, K)
                rows.append(dict(h=h, picta_ratio=round(wd['relP'](h) if branch == 'alive' else 0.0, 2), target=round(t, 2), baby_ratio=round(rad, 2),
                                 picta_density=round(dp, 2), baby_density=round(db, 2)))
        pk = {hh: round(rad_of(wd, hh) / max(wd['target'](hh), 1e-9), 2) for hh in (7.5, 13.0, 18.5)}
        rep[wd['w']] = dict(file=f, mist_partner=wd['partner'], reached_at_peaks=pk, voli={s: wd['bslots'][s]['name'] for s in SLOTS},
                            astralite_ratio_at_slot_peaks={s: round(v, 2) for s, v in wd['relA'].items()},
                            max_over_target=[round(over[0], 3), over[1]], min_vs_target=[round(under[0], 3), under[1]], rows=rows)
    return dict(branch=branch, K={n: K[n] for n in names},
                voli_copy_intensity={n: round(K[n] * next(wd['bslots'][s]['I'] for wd in W for s in RSLOTS if wd['bslots'][s]['name'] == n), 3) for n in names},
                GVR_Intensity={f: {p: round(G[f][p], 3) for p in FREE} for f in files},
                GVR_Intensity_picta={f: GP[f] for f in files}, GVR_Night={f: GN[f] for f in files}, per_weather=rep)

# ------------------------------------------------------------------ audit
COMPS = ['band_top', 'band_hor', 'dome_zenith', 'dome_hor_sun', 'dome_hor_away', 'dome_mid_away', 'sky_ibl', 'clouds', 'fog_far',
         'fog_near', 'volfog', 'sunlight', 'sun_disc', 'scat_sunward'] + ['amb_' + a[11:] for a in AXES]
def components(E, R, h):
    v = views(h); c = {}
    c['band_top'] = V_band(E, R, h, 'top'); c['band_hor'] = V_band(E, R, h, 'hor')
    for k, vd in v.items(): c['dome_' + k] = sky_pixel(E, R, h, vd)
    c['sky_ibl'] = sky_ibl(E, R, h)
    c['clouds'] = V_cloud(E, R, h); c['fog_far'] = V_fog(E, R, h); c['fog_near'] = V_fog(E, R, h, 'fognear')
    c['volfog'] = V_volfog(E, h); c['sunlight'] = V_light(E, R, h); c['sun_disc'] = V_sundisc(E, R, h)
    c['scat_sunward'] = scat_parts(E, R, h, v['hor_sun'])['scat']
    for ax in AXES: c['amb_' + ax[11:]] = V_amb(E, R, h, ax)
    return c
def audit_weather(r, w, hours=AUDIT_H):
    E_P, E_B, R, Rb = r['_E_P'], r['_E_B'], r['_RP'][w], r['_RB'][w]
    worst = {}; night_max = 0.0
    for h in hours:
        a = components(E_P, R, h); b = components(E_B, Rb, h)
        for cn in a:
            ya = Y(a[cn])
            if ya < 1e-7: continue
            d = Y(b[cn]) / ya - 1
            if cn not in worst or abs(d) > abs(worst[cn][0]): worst[cn] = (d, h)
    for h in NIGHT_H[::2]:
        a = components(E_P, R, h); b = components(E_B, Rb, h)
        for cn in a: night_max = max(night_max, float(np.abs(a[cn] - b[cn]).max()))
    return {cn: [round(100 * v[0], 3), v[1]] for cn, v in worst.items()}, night_max

def hue_table(r, w, hours=(7.25, 7.5, 9.0, 13.0, 17.0, 18.5, 18.75), comps=('dome_hor_away', 'dome_hor_sun', 'dome_zenith', 'fog_far', 'clouds', 'sunlight', 'amb_XPlus', 'amb_ZMinus', 'sky_ibl')):
    E_P, E_B, R, Rb, A = r['_E_P'], r['_E_B'], r['_RP'][w], r['_RB'][w], r['_A']
    out = {}
    for h in hours:
        a = components(E_P, R, h); b = components(E_B, Rb, h)
        row = {}
        for cn in comps:
            if cn.startswith('dome_'):
                va = A.vis(lambda E, R_, hh: sky_pixel(E, R_, hh, views(hh)[cn[5:]]), h)
            elif cn == 'sky_ibl': va = A.vis(lambda E, R_, hh: sky_ibl(E, R_, hh), h)
            elif cn == 'fog_far': va = A.vis(lambda E, R_, hh: V_fog(E, R_, hh), h)
            elif cn == 'clouds': va = A.vis(V_cloud, h)
            elif cn == 'sunlight': va = A.vis(lambda E, R_, hh: V_light(E, R_, hh), h)
            else: va = A.vis(lambda E, R_, hh: V_amb(E, R_, hh, 'Directional' + cn[4:]), h)
            Lp, Cp, hp = lch(a[cn]); Lb, Cb, hb = lch(b[cn]); La, Ca, ha = lch(va) if va is not None else (0, 0, 0)
            row[cn] = dict(picta=f"{hp:5.1f}/{Cp:.3f} {hue_name(hp, Cp)}", baby=f"{hb:5.1f}/{Cb:.3f} {hue_name(hb, Cb)}",
                           astralite=f"{ha:5.1f}/{Ca:.3f} {hue_name(ha, Ca)}", dY_pct=round(100 * (Y(b[cn]) / max(Y(a[cn]), 1e-12) - 1), 2),
                           share=share(a[cn], va, b[cn]))
        out[h] = row
    return out

def naive_rows(r, w):
    """Astralite records dropped under Picta's live filters (the double tint the design avoids)."""
    E_P, R, A = r['_E_P'], r['_RP'][w], r['_A']
    AR_ = A.R0; res = {}
    for h in (7.5, 13.0, 18.5):
        for nm, fP, fN in (('horizon', lambda: V_band(E_P, R, h, 'hor'), lambda: V_band(E_P, AR_, h, 'hor')),
                           ('fog_far', lambda: V_fog(E_P, R, h), lambda: V_fog(E_P, AR_, h)),
                           ('fog_near', lambda: V_fog(E_P, R, h, 'fognear'), lambda: V_fog(E_P, AR_, h, 'fognear')),
                           ('dome_hor_sun', lambda: sky_pixel(E_P, R, h, views(h)['hor_sun']), lambda: sky_pixel(E_P, AR_, h, views(h)['hor_sun']))):
            p, n = fP(), fN(); va = A.vis(lambda E, R_, hh: (V_band(E, R_, hh, 'hor') if nm == 'horizon' else V_fog(E, R_, hh, 'fognear' if nm == 'fog_near' else 'fogfar') if nm.startswith('fog') else sky_pixel(E, R_, hh, views(hh)['hor_sun'])), h)
            res[f'{h} {nm}'] = dict(picta=desc(p), naive=desc(n), astralite_own=desc(va) if va is not None else None, naive_luma_x=round(Y(n) / max(Y(p), 1e-12), 2))
    return res

def crossterm(ra, wa, rb, wb):
    """weather transition: engine lerps records, E11 lerps ini values; runtime product vs ideal endpoint lerp."""
    def mixE(Ea, Eb_, t):
        out = {}
        for sec in Ea:
            out[sec] = {}
            for k in Ea[sec]:
                out[sec][k] = {}
                for p in Ea[sec][k]:
                    va = Ea[sec][k][p]; vb = Eb_.get(sec, {}).get(k, {}).get(p, va)
                    out[sec][k][p] = lerp(np.asarray(va, float), np.asarray(vb, float), t) if np.ndim(va) else lerp(va, vb, t)
        return out
    def mixR(Ra, Rb_, t):
        out = {}
        for s in SLOTS:
            out[s] = {}
            for k, v in Ra[s].items():
                out[s][k] = {ax: lerp(v[ax], Rb_[s][k][ax], t) for ax in v} if k == 'dalc' else lerp(v, Rb_[s][k], t)
        return out
    res = {}
    for lane in ('picta', 'baby'):
        Ea, Ra = (ra['_E_P'], ra['_RP'][wa]) if lane == 'picta' else (ra['_E_B'], ra['_RB'][wa])
        Eb_, Rb_ = (rb['_E_P'], rb['_RP'][wb]) if lane == 'picta' else (rb['_E_B'], rb['_RB'][wb])
        Em, Rm = mixE(Ea, Eb_, 0.5), mixR(Ra, Rb_, 0.5)
        for h in (7.25, 13.0, 18.75):
            for nm, f in (('horizon', lambda E, R: V_band(E, R, h, 'hor')), ('fog_far', lambda E, R: V_fog(E, R, h)),
                          ('sunlight', lambda E, R: V_light(E, R, h)), ('amb_XPlus', lambda E, R: V_amb(E, R, h, 'DirectionalXPlus'))):
                run = f(Em, Rm); ideal = lerp(f(Ea, Ra), f(Eb_, Rb_), 0.5)
                _, C1, h1 = lch(run); _, C2, h2 = lch(ideal)
                res[f'{lane} {h} {nm}'] = dict(hue_gap=round(abs(((h1 - h2 + 180) % 360) - 180) if min(C1, C2) > 0.02 else 0.0, 2),
                                              Y_gap_pct=round(100 * (Y(run) / max(Y(ideal), 1e-12) - 1), 2))
    return res

# ------------------------------------------------------------------ plan formatting
def fmt3(v):
    v = np.atleast_1d(np.asarray(v, float))
    f = lambda x: (f"{x:.3f}".rstrip('0').rstrip('.') if abs(x) >= 5e-4 else '0')
    return ', '.join(f(x) for x in v)
PLAN_KEYS = [('SKY', 'GradientTopColorFilter'), ('SKY', 'GradientHorizonColorFilter'), ('SKY', 'CloudsColorFilter'),
             ('ENVIRONMENT', 'FogColorFilter'), ('ENVIRONMENT', 'DirectLightingColorFilter'),
             ('ENVIRONMENT', 'DirectLightingDesaturation'), ('SKYSCATTERING', 'ScatteringColor'), ('SKYSCATTERING', 'ColorFromSun')]
def e11_plan(r, vl=None):
    """only lines whose value really changes; unchanged values keep Picta's text (byte identity)."""
    E_P, E_B, RAW = r['_E_P'], r['_E_B'], r['_RAW']; edits = []
    for sec, key in PLAN_KEYS:
        for p in FREE:
            a, b = np.asarray(E_P[sec][key][p], float), np.asarray(E_B[sec][key][p], float)
            if np.all(np.abs(a - b) < 5e-4): continue
            edits.append(dict(section=sec, key=key + p, old=RAW[sec][key + p], new=fmt3(b)))
    if vl is not None:
        f = r['file']; GV = vl['GVR_Intensity'][f]
        for p in FREE:
            old = RAW['GAMEVOLUMETRICRAYS']['Intensity' + p]
            if abs(float(old) - GV[p]) >= 5e-4: edits.append(dict(section='GAMEVOLUMETRICRAYS', key='Intensity' + p, old=old, new=fmt3(GV[p])))
            oldc = RAW['GAMEVOLUMETRICRAYS']['ColorFilter' + p]; g = Y(parse_val(oldc))
            if np.any(np.abs(parse_val(oldc) - g) >= 5e-4): edits.append(dict(section='GAMEVOLUMETRICRAYS', key='ColorFilter' + p, old=oldc, new=fmt3([g, g, g])))
            oldr = RAW['GAMEVOLUMETRICRAYS']['RangeFactor' + p]
            if abs(float(oldr) - 1.0) >= 5e-4: edits.append(dict(section='GAMEVOLUMETRICRAYS', key='RangeFactor' + p, old=oldr, new='1.0'))
        if vl['branch'] == 'newly_on':
            old = RAW['GAMEVOLUMETRICRAYS']['IntensityNight']
            if abs(float(old)) >= 5e-4: edits.append(dict(section='GAMEVOLUMETRICRAYS', key='IntensityNight', old=old, new='0.0'))
    return edits

# ------------------------------------------------------------------ main
def run_all(D, files=None, with_vl=True):
    res = {}
    for fn in (files or list(FILES)):
        res[fn] = solve_file(fn, D)
    vl = solve_vl(res, D) if (with_vl and D['VOL_ON']) else None
    return res, vl

def strip(r): return {k: v for k, v in r.items() if not k.startswith('_')}
def conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    raise TypeError(type(o))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', default='all')
    args = ap.parse_args()
    LOG = []
    def P(s=''): LOG.append(s); print(s, flush=True)
    D = default_dials()
    P('FINAL MODEL - Picta x Astralite baby (pre-tonemap Bottled 4ca678b chain; Picta clocks TOD 5.5/7.25/9/10/17/18.75/20.5, CLMT 06-09/17-20)')
    P(f'dials: {json.dumps(D)}')
    P(f'routed files: {len(FILES)}; weathers: {sum(len(v) for v in FILES.values())}')

    # 1) identity regression (all mixes 0, no fog transplant)
    D0 = default_dials(); D0['MIX'] = dict(Sunrise=0.0, Day=0.0, Sunset=0.0); D0['VOL_ON'] = False
    r0, _ = run_all(D0, with_vl=False)
    idn = {fn: dict(e11_edits=len(e11_plan(r)), dalc_changed=sum(1 for w in r['weathers'] for s in RSLOTS for ax in AXES
                                                                    if r['records'][w]['DALC'][s][ax] != r['records'][w]['DALC_picta'][s][ax])) for fn, r in r0.items()}
    P(''); P('== IDENTITY REGRESSION (MIX 0/0/0, fog off): planned E11 lines and changed DALC bytes must all be 0')
    P('   ' + ('PASS - 0 lines, 0 bytes in all 24 files / 28 records' if all(v['e11_edits'] == 0 and v['dalc_changed'] == 0 for v in idn.values()) else json.dumps(idn)))
    json.dump(idn, open(os.path.join(HERE, 'identity_check.json'), 'w'), indent=1)

    # 2) default build (alive branch) + newly_on branch for VL
    res, vl = run_all(D)
    D_no = default_dials(); D_no['VL_BRANCH'] = 'newly_on'
    vl_no = solve_vl(res, D_no, K_fixed=vl['K'])
    plan = dict(dials=D, files={fn: dict(weathers=r['weathers'], colour_partner=r['colour_partner'], alpha_used=r['alpha_used'],
                                         light_luma_weight=r['light_luma_weight'], e11_edits=e11_plan(r, vl), e11_edits_newly_on=e11_plan(r, vl_no))
                                for fn, r in res.items()},
                records={w: dict(r['records'][w], mist_partner=mist_partner(w), colour_partner=r['colour_partner'],
                                 visual_effect=next((k for k, v in RINGS.items() if wclass(w) in v), None),
                                 mot_banks=wclass(w) in MOT_BANKS)
                         for r in res.values() for w in r['weathers']},
                vl_alive=vl, vl_newly_on=vl_no)
    json.dump(plan, open(os.path.join(HERE, 'final_plan.json'), 'w'), indent=1, default=conv)
    # houseCARL records manifest (field_path ops); the ESL is branch-independent (VOLI copy intensities from the alive solve)
    MOT = [f'{x:06X}:Mists of Tamriel.esp' for x in range(0x00080B, 0x000817)]
    RING_SRC = {'Lite': ('000834', '000802'), 'Heavy': ('000812', '000803'), 'Rain': ('00081C', '00080C')}
    RING_BE = {'Lite': 0.0, 'Heavy': 0.4980392, 'Rain': 0.0}
    voli_src = {}
    for d in vl['per_weather'].values(): pass
    for r in res.values():
        for w in r['weathers']:
            AR_ = astra_records(mist_partner(w))
            for s_ in RSLOTS: voli_src[AR_['_voli'][s_]['editorid']] = (AR_['_voli'][s_]['formid'], AR_['_voli'][s_].get('winner'))
    new_records = [dict(type='VOLI', editorid='PXA_' + n, copy_of=voli_src[n][0], copy_version_from=voli_src[n][1], set=dict(Intensity=round(vl['voli_copy_intensity'][n], 3)),
                        note='verbatim copy except Intensity (Picta scalar regime)') for n in sorted(voli_src)]
    for k, (rf, ao) in RING_SRC.items():
        new_records.append(dict(type='ARTO', editorid=f'PXA_Distant_Mounts_{k}01', copy_of=f'{ao}:Astralite ENB.esp', source_mod='[NoDelete] Soul Core Plugin and Assets'))
        new_records.append(dict(type='RFCT', editorid=f'PXA_Distant_Mounts_{k}', copy_of=f'{rf}:Astralite ENB.esp', source_mod='[NoDelete] Soul Core Plugin and Assets',
                                relink=dict(EffectArt=f'PXA_Distant_Mounts_{k}01')))
    ops = {}
    for r in res.values():
        for w in r['weathers']:
            rec = r['records'][w]; o = []
            for s_ in RSLOTS:
                for ax in AXES:
                    if rec['DALC'][s_][ax] != rec['DALC_picta'][s_][ax]:
                        o.append(dict(field=f'DirectionalAmbientLightingColors.{s_}.{ax}', old=rec['DALC_picta'][s_][ax], new=rec['DALC'][s_][ax]))
            AR_ = astra_records(mist_partner(w))
            for s_ in RSLOTS: o.append(dict(field=f'VolumetricLighting.{s_}', new='PXA_' + AR_['_voli'][s_]['editorid']))
            ring = next((k for k, v in RINGS.items() if wclass(w) in v), None)
            if ring: o += [dict(field='VisualEffect', new=f'PXA_Distant_Mounts_{ring}'), dict(field='VisualEffectBegin', new=RING_BE[ring]), dict(field='VisualEffectEnd', new=RING_BE[ring])]
            if wclass(w) in MOT_BANKS: o.append(dict(field='SkyStatics', op='add', new=MOT))
            ops[w + ':Picta - Weathers of Aurbis.esm'] = dict(editorid=rec['editorid'],
                forward_from=('Authoria - Patch - Picta Seasonal.esp' if w.startswith('5AF') else 'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp'), ops=o)
    json.dump(dict(plugin='Authoria - Patch - Picta x Astralite.esp', flags=['ESL'], form_version=44,
                   masters=['Skyrim.esm', 'Update.esm', 'Dawnguard.esm', 'Dragonborn.esm', 'Picta - Weathers of Aurbis.esm', 'Mists of Tamriel.esp',
                            'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp', 'Authoria - Patch - Picta Seasonal.esp'],
                   new_records=new_records, overrides=ops,
                   optional_off_by_default=dict(SkyStaticsColor={w: r['records'][w]['SkyStaticsColor_optional'] for r in res.values() for w in r['weathers']})),
              open(os.path.join(HERE, 'records_manifest.json'), 'w'), indent=1, default=conv)
    P(f'== RECORDS MANIFEST: {len(ops)} WTHR overrides, {sum(len(v["ops"]) for v in ops.values())} field ops, {len(new_records)} new records')
    P(''); P('== E11 LINES PLANNED per file (alive branch / newly_on branch)')
    for fn, f in plan['files'].items():
        keys = sorted({e['key'] for e in f['e11_edits']})
        P(f'   {fn.split("/")[-1]:42s} {len(f["e11_edits"]):3d} / {len(f["e11_edits_newly_on"]):3d}  light WL={f["light_luma_weight"]}  alpha sky {f["alpha_used"]["sky"]} light {f["alpha_used"]["light"]}')
    allkeys = sorted({re.sub(r'(Dawn|Sunrise|Day|Sunset|Dusk|Night)$', '', e['section'] + '.' + e['key']) for f in plan['files'].values() for e in f['e11_edits'] + f['e11_edits_newly_on']})
    P('   whitelist of keys touched: ' + ', '.join(allkeys))
    nightkeys = [e['key'] for f in plan['files'].values() for e in f['e11_edits'] if re.search(r'(Night|InteriorDay|InteriorNight)$', e['key'])]
    P(f'   Night/Interior lines in alive branch: {len(nightkeys)}')

    # 3) luma audit all 28 weathers
    P(''); P('== LUMA AUDIT: worst |dY| baby vs Picta over 05:00-21:30 every 15 min, all 28 weathers (percent @ hour)')
    audit = {}; gw = {}
    for fn, r in res.items():
        for w in r['weathers']:
            worst, nm = audit_weather(r, w)
            audit[w] = dict(file=fn, worst=worst, night_max_abs=nm)
            for cn, (d, h) in worst.items():
                if cn not in gw or abs(d) > abs(gw[cn][0]): gw[cn] = (d, h, w)
            top = sorted(worst.items(), key=lambda kv: -abs(kv[1][0]))[:4]
            P(f'   {w} {r["_RP"][w]["_edid"][9:]:34s} ' + '  '.join(f'{cn} {d:+.2f}%@{h:g}' for cn, (d, h) in top) + f'   night max abs {nm:.1e}')
    P('   GLOBAL worst per component: ' + '; '.join(f'{cn} {d:+.2f}% ({w} @{h:g})' for cn, (d, h, w) in sorted(gw.items(), key=lambda kv: -abs(kv[1][0]))))
    json.dump(audit, open(os.path.join(HERE, 'luma_audit.json'), 'w'), indent=1, default=conv)

    # 4) hue tables (A01, C01, D02, D03, SUMMER A01, E05)
    HT = {}
    P(''); P('== HUE / CHROMA (OKLCh hue/chroma, name)  Picta -> baby [Astralite], dY%, share reached (0 Picta .. 1 Astralite)')
    for w in ('19FA01', '19FC01', '19FD02', '19FD03', '5AFA01', '19FE05', '19FB03'):
        fn = next(f for f, r in res.items() if w in r['weathers']); r = res[fn]
        HT[w] = hue_table(r, w)
        P(f' -- {w} {r["_RP"][w]["_edid"]} <- {r["colour_partner"]} (mist {mist_partner(w)})')
        for h, row in HT[w].items():
            P(f'   {h:5.2f} ' + ' | '.join(f'{cn}: {v["picta"]} -> {v["baby"]} [{v["astralite"]}] {v["dY_pct"]:+.1f}% s={v["share"]}' for cn, v in row.items() if cn in ('dome_hor_away', 'dome_hor_sun', 'fog_far', 'sunlight', 'amb_XPlus')))
    json.dump(HT, open(os.path.join(HERE, 'hue_tables.json'), 'w'), indent=1, default=conv)

    # 5) naive transplant + crossterm
    fa = next(f for f, r in res.items() if '19FA01' in r['weathers']); fd = next(f for f, r in res.items() if '19FD03' in r['weathers'])
    NV = naive_rows(res[fa], '19FA01'); CT = crossterm(res[fa], '19FA01', res[fd], '19FD03')
    P(''); P('== NAIVE TRANSPLANT (Astralite A01-partner records under Picta filters) - the double tint avoided')
    for k, v in NV.items(): P(f'   {k:22s} Picta {v["picta"]} | naive {v["naive"]} x{v["naive_luma_x"]} | Astralite own {v["astralite_own"]}')
    P(''); P('== TRANSITION CROSS-TERM A01 -> D03 at t=0.5 (runtime vs ideal endpoint lerp)')
    for k, v in CT.items(): P(f'   {k:28s} hue gap {v["hue_gap"]:5.2f}  Y gap {v["Y_gap_pct"]:+5.2f}%')

    # 6) VL tables
    for nm, V in (('alive', vl), ('newly_on', vl_no)):
        P(''); P(f'== VOLUMETRIC LIGHT branch {nm}: VOLI copy intensities (Picta regime) {V["voli_copy_intensity"]}')
        for w, d in V['per_weather'].items():
            if w not in ('19FA01', '19FA02', '19FC01', '19FD02', '19FD03', '19FE03', '19FE05', '5AFA01'): continue
            P(f'   {w} {d["voli"]} max baby/target {d["max_over_target"]} min {d["min_vs_target"]} GVR {V["GVR_Intensity"][d["file"]]} (Picta {V["GVR_Intensity_picta"][d["file"]]})')
            P('      ' + ' '.join(f'{x["h"]:g}: P{x["picta_ratio"]} T{x["target"]} B{x["baby_ratio"]} d{x["baby_density"]}' for x in d['rows']))
        worst = max((d['max_over_target'][0], w) for w, d in V['per_weather'].items())
        P(f'   worst overshoot over all 28: {worst}')

    open(os.path.join(HERE, 'final_model_out.txt'), 'w', encoding='utf-8').write('\n'.join(LOG))
    json.dump(dict(naive=NV, crossterm=CT, global_worst=gw), open(os.path.join(HERE, 'extras.json'), 'w'), indent=1, default=conv)
