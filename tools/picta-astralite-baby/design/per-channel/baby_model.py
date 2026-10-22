"""PER-CHANNEL PHYSICS model for the Picta x Astralite "baby" (read-only, numbers only).

Implements the design in this folder:
  * one hue carrier per channel (no double tint),
  * Astralite colours re-timed onto PICTA's clocks (records on Picta CLMT 06-09 / 17-20, ini on Picta [TIMEOFDAY]),
  * OKLCh blend with luminance (Y) lock and an amplitude dial,
  * ini-carried channels solved by least squares over the day (TIMEOFDAY carrier fitted to a CLMT-timed target),
  * record-carried channels solved per CLMT slot (DALC, sunlight) with the ini side neutralised to a grey scalar,
  * weather-transition cross-term and Lab/LCh/RGB opposite-hue comparison.
Formulas follow Bottled 4ca678b (Effects11.cpp 513-737, SkyScattering.hlsli 74-104, Sky.hlsl 373-384,
EffectManager.cpp 902-1029) as transcribed in map_e11-colour-model.json.  Pre-tonemap, no adaptation/SH2.
Outputs: baby_model_out.txt, baby_model_out.json (same folder).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BABY = os.path.normpath(os.path.join(HERE, '..', '..'))
MAP = os.path.join(BABY, 'map')

# ------------------------------------------------------------------ dials (defaults of the design)
DIALS = dict(MIX_DAWN=0.50, MIX_DAY=0.30, MIX_DUSK=0.50, MIX_NIGHT=0.0,
             STRENGTH=1.0,        # chroma amplitude of the final blended colour (1 = as mixed)
             VOL_AMOUNT=1.0)      # multiplier on Astralite's effective volumetric-light intensity
PERIODS = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
FREE = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk']          # Night is never solved (stays Picta)
SLOTS = ['Sunrise', 'Day', 'Sunset', 'Night']
PICTA_TOD = dict(DawnDuration=3.5, SunriseTime=9.0, DayTime=10.0, SunsetTime=17.0, DuskDuration=3.5, NightTime=20.5)
NAT_TOD = dict(DawnDuration=3.5, SunriseTime=8.0, DayTime=13.0, SunsetTime=18.0, DuskDuration=3.5, NightTime=1.0)
PICTA_CLMT = (6.0, 9.0, 17.0, 20.0)       # houseCARL 000812 winner (Darkened patch): sunrise 06-09, sunset 17-20
ASTRA_CLMT = (4.5, 9.5, 16.5, 21.5)       # Astralite ENB.esp SkyrimClimate
HOURS = np.arange(5.5, 20.5001, 0.25)     # every hour where a non-Night period has weight on the Picta TOD
REPORT_H = [6.5, 7.25, 8.25, 9.0, 10.0, 13.0, 15.0, 17.0, 17.75, 18.75, 19.75]

def lerp(a, b, t): return a + (b - a) * t
def sat(x): return max(0.0, min(1.0, x))

# ------------------------------------------------------------------ clocks
def tod_weights(h, T=PICTA_TOD):
    """EffectManager.cpp 902-1029 @4ca678b (copied from map colour_model.py)."""
    night, sunrise, dawnD, day, sunset, duskD = T['NightTime'], T['SunriseTime'], T['DawnDuration'], T['DayTime'], T['SunsetTime'], T['DuskDuration']
    dawnStart = sunrise - dawnD; dawnMid = sunrise - dawnD * 0.5; duskMid = sunset + duskD * 0.5; duskEnd = sunset + duskD
    tp = [night, dawnStart, dawnMid, sunrise, day, sunset, duskMid, duskEnd]
    tp = tp + [x + 24 for x in tp]
    fmap = ['Night', 'Night', 'Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
    ci = ni = 0; cpt = 0.0; npt = 24.0
    for i, t in enumerate(tp):
        if h >= t and t >= cpt: ci, cpt = i, t
        if t > h and npt >= t: ni, npt = i, t
    cf, nf = fmap[ci % 8], fmap[ni % 8]
    td = abs(npt - cpt) or 1.0
    b = abs(h - cpt) / td
    f = dict(Dawn=0.0, Sunrise=0.0, Day=0.0, Sunset=0.0, Dusk=0.0, Night=0.0)
    if cf == nf: f[cf] = 1.0
    else: f[cf] = sat(1 - b); f[nf] = sat(b)
    pd = sat(f['Day'] ** 0.6)
    if pd > 1.17549435e-38:
        if f['Sunrise'] > 1.17549435e-38: f['Sunrise'] = sat(1 - pd)
        if f['Sunset'] > 1.17549435e-38: f['Sunset'] = sat(1 - pd)
    f['Day'] = pd
    return f

def clmt_weights(h, C=PICTA_CLMT):
    """ASSUMED engine rule: record colours peak at the midpoint of the sunrise/sunset window
    (Night->Sunrise over the first half, Sunrise->Day over the second; mirrored at sunset)."""
    rb, re, sb, se = C
    rm, sm = (rb + re) / 2, (sb + se) / 2
    w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)
    if h < rb or h >= se: w['Night'] = 1.0
    elif h < rm: t = (h - rb) / (rm - rb); w['Night'] = 1 - t; w['Sunrise'] = t
    elif h < re: t = (h - rm) / (re - rm); w['Sunrise'] = 1 - t; w['Day'] = t
    elif h < sb: w['Day'] = 1.0
    elif h < sm: t = (h - sb) / (sm - sb); w['Day'] = 1 - t; w['Sunset'] = t
    else: t = (h - sm) / (se - sm); w['Sunset'] = 1 - t; w['Night'] = t
    return w

def alpha_at(h):
    c = clmt_weights(h)
    return (c['Sunrise'] * DIALS['MIX_DAWN'] + c['Day'] * DIALS['MIX_DAY'] + c['Sunset'] * DIALS['MIX_DUSK']
            + c['Night'] * DIALS['MIX_NIGHT'])

def sun_z(h):
    """Rough sun height on the Picta clock: horizon at the CLMT window midpoints (07:30 / 18:30), 60 deg peak."""
    rb, re, sb, se = PICTA_CLMT
    up, down = (rb + re) / 2, (sb + se) / 2
    if up <= h <= down:
        e = math.radians(60.0) * math.sin(math.pi * (h - up) / (down - up))
    else:
        d = min(abs(h - up), abs(h - down))
        e = -math.radians(12.0) * min(1.0, d / 1.5)
    return math.sin(e)

# ------------------------------------------------------------------ colour science
M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
               [0.2119034982, 0.6806995451, 0.1073969566],
               [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
               [1.9779984951, -2.4285922050, 0.4505937099],
               [0.0259040371, 0.7827717662, -0.8086757660]])
M1i, M2i = np.linalg.inv(M1), np.linalg.inv(M2)
def Y(c): return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
def to_oklab(c):
    lms = M1 @ np.maximum(np.asarray(c, float), 0.0)
    return M2 @ np.cbrt(lms)
def from_oklab(lab):
    lms_ = M2i @ np.asarray(lab, float)
    return M1i @ (lms_ ** 3)
def lch(c):
    L, a, b = to_oklab(c); return L, math.hypot(a, b), (math.degrees(math.atan2(b, a)) % 360)
def norm_y(c, y=0.18):
    yy = Y(c)
    return np.asarray(c, float) * (y / yy) if yy > 1e-9 else np.asarray(c, float)

def _fit_gamut(L, C, hdeg):
    """Reduce chroma until every linear channel is >= 0 (HDR: no upper clip)."""
    lo, hi = 0.0, C
    for _ in range(40):
        rgb = from_oklab([L, C * math.cos(math.radians(hdeg)), C * math.sin(math.radians(hdeg))])
        if rgb.min() >= -1e-6: return rgb, C
        hi = C; C = (lo + hi) / 2
    rgb = from_oklab([L, 0.0, 0.0]); return rgb, 0.0

def blend(cP, cA, a, mode='lch', strength=None, ylock=None):
    """Mix the CHROMATICITY of cP toward cA by a, keep cP's luminance Y (or ylock)."""
    strength = DIALS['STRENGTH'] if strength is None else strength
    cP = np.asarray(cP, float); cA = np.asarray(cA, float)
    yP = Y(cP) if ylock is None else ylock
    if yP <= 1e-9: return cP.copy()
    if Y(cA) <= 1e-9 or a <= 0:
        out = cP.copy()
        if strength != 1.0:
            L, C, h = lch(norm_y(cP)); out, _ = _fit_gamut(L, C * strength, h)
        return norm_y(out, yP)
    p, q = norm_y(cP), norm_y(cA)
    if mode == 'rgb':
        out = lerp(p, q, a)
        if strength != 1.0:
            L, C, h = lch(out); out, _ = _fit_gamut(L, C * strength, h)
        return norm_y(out, yP)
    LP, aP, bP = to_oklab(p); LA, aA, bA = to_oklab(q)
    if mode == 'lab':
        lab = [lerp(LP, LA, a), lerp(aP, aA, a), lerp(bP, bA, a)]
        L, C, h = lab[0], math.hypot(lab[1], lab[2]), math.degrees(math.atan2(lab[2], lab[1])) % 360
    else:
        CP, hP = math.hypot(aP, bP), math.degrees(math.atan2(bP, aP)) % 360
        CA, hA = math.hypot(aA, bA), math.degrees(math.atan2(bA, aA)) % 360
        if CA < 0.01: hA = hP          # achromatic partner: no hue swing, chroma just shrinks
        if CP < 0.01: hP = hA
        dh = ((hA - hP + 180) % 360) - 180   # short arc
        L, C, h = lerp(LP, LA, a), lerp(CP, CA, a), (hP + a * dh) % 360
    out, _ = _fit_gamut(L, C * strength, h)
    return norm_y(out, yP)

def desc(c):
    c = np.asarray(c, float)
    if Y(c) <= 1e-9: return "black"
    L, C, h = lch(norm_y(c))
    return f"Y={Y(c):8.4g} h={h:5.1f} C={C:.3f}"

def hue_diff(c1, c2):
    _, C1, h1 = lch(norm_y(c1)); _, C2, h2 = lch(norm_y(c2))
    d = abs(((h1 - h2 + 180) % 360) - 180)
    return d if min(C1, C2) > 0.02 else 0.0

def de_ok(c1, c2):
    """OKLab distance at equal luminance (pure chromaticity error)."""
    return float(np.linalg.norm(to_oklab(norm_y(c1)) - to_oklab(norm_y(c2))))

# ------------------------------------------------------------------ E11 ops (Effects11.cpp 513-545)
def curve(c, p): return np.maximum(np.asarray(c, float), 0.0) ** p
def desat(c, d):
    c = np.asarray(c, float); m = c.mean(); return np.maximum(lerp(c, m, d), 0.0)
def inv_desat(v, d):
    v = np.asarray(v, float); m = v.mean()
    return v if abs(1 - d) < 1e-6 else (v - d * m) / (1 - d)
def cfilter(c, f, amt): return lerp(np.asarray(c, float), 1.0, amt) * np.asarray(f, float)

# ------------------------------------------------------------------ data
def j(p): return json.load(open(p, encoding='utf-8'))
PT = j(os.path.join(MAP, 'picta-colour', 'picta_e11_colour_table.json'))
PR = j(os.path.join(MAP, 'picta-colour', 'picta_wthr_colours.json'))
AR = j(os.path.join(MAP, 'astralite-colour', 'astralite_rotating_weathers_colour.json'))
SC = j(os.path.join(MAP, 'astralite-colour', 'soulcore_e11_colour_keys.json'))

def parse(v):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, (list, tuple)): return np.array([float(x) for x in v[:3]]) if len(v) >= 3 else float(v[0])
    s = str(v).strip().strip('[]')
    if ',' in s: return np.array([float(x) for x in s.split(',')[:3]])
    try: return float(s)
    except ValueError: return None

def picta_ini(fname):
    P = PT[fname]['periods']
    return {p: {k: parse(v) for k, v in P[p].items()} for p in PERIODS}

def soul_ini(name):
    vals = SC['weather_files'][name]['values']; base = SC['base_values']
    def get(key, p):
        src = vals.get(key) or base.get(key)
        if src is None: return None
        if 'value' in src: return parse(src['value'])
        return parse(src.get(p))
    keys = {'GradDesat': 'SKY.GradientDesaturation', 'TopF': 'SKY.GradientTopColorFilter', 'HorF': 'SKY.GradientHorizonColorFilter',
            'CloudsF': 'SKY.CloudsColorFilter', 'CloudsDesat': 'SKY.CloudsDesaturation', 'SunF': 'SKY.SunColorFilter',
            'SunDesat': 'SKY.SunDesaturation', 'FogF': 'ENVIRONMENT.FogColorFilter', 'FogCurve': 'ENVIRONMENT.FogColorCurve',
            'DLF': 'ENVIRONMENT.DirectLightingColorFilter', 'DLDesat': 'ENVIRONMENT.DirectLightingDesaturation',
            'AmbDesat': 'ENVIRONMENT.AmbientLightingDesaturation', 'CFS': 'SKYSCATTERING.ColorFromSun',
            'ScatColor': 'SKYSCATTERING.ScatteringColor', 'Amount': 'SKYSCATTERING.Amount', 'ScatInt': 'SKYSCATTERING.Intensity',
            'AirGlow': 'SKYSCATTERING.AirGlowIntensity', 'GVRInt': 'GAMEVOLUMETRICRAYS.Intensity', 'GVRF': 'GAMEVOLUMETRICRAYS.ColorFilter'}
    out = {}
    for p in PERIODS:
        out[p] = {}
        for k, key in keys.items():
            v = get(key, p)
            if v is None:
                v = np.array([1.0, 1, 1]) if k.endswith('F') or k == 'ScatColor' else (1.0 if k in ('FogCurve', 'ScatInt') else 0.0)
            out[p][k] = v
    return out

def rgb01(x): return np.array(x, float) / 255.0

WEATHERS = {
    'A01 Clear':        dict(rec='19FA01:Picta - Weathers of Aurbis.esm', ini='Picta - Weathers/00_Master/A01_Clear.ini',
                             partner='00081A:Skyrim.esm', soul='SoulClear.ini'),
    'C01 Cloudy':       dict(rec='19FC01:Picta - Weathers of Aurbis.esm', ini='Picta - Weathers/00_Master/C01_Cloudy.ini',
                             partner='012F89:Skyrim.esm', soul='SoulCloudy.ini'),
    'D02 Heavy Fog':    dict(rec='19FD02:Picta - Weathers of Aurbis.esm', ini='Picta - Weathers/00_Master/D02_Overcast_Heavy_Fog.ini',
                             partner='0C821E:Skyrim.esm', soul='SoulFog.ini'),
    'D03 Rain Light':   dict(rec='19FD03:Picta - Weathers of Aurbis.esm', ini='Picta - Weathers/00_Master/D03_Overcast_Rain_Light.ini',
                             partner='0C821F:Skyrim.esm', soul='SoulOvercast.ini'),
    'SUMMER A01 Clear': dict(rec='5AFA01:Picta - Weathers of Aurbis.esm', ini='Authoria - Summer/A01_Clear_Summer.ini',
                             partner='00081A:Skyrim.esm', soul='SoulClear.ini'),
}

def picta_records(fid):
    r = PR[fid]['colours']; R = {}
    for slot in SLOTS:
        R[slot] = dict(upper=rgb01(r['SkyUpperColor'][slot]), horizon=rgb01(r['HorizonColor'][slot]),
                       fogfar=rgb01(r['FogFarColor'][slot]), sun=rgb01(r['SunColor'][slot]),
                       sunlight=rgb01(r['SunlightColor'][slot]),
                       cloud=rgb01(PR[fid]['clouds_enabled'][0]['colors'][slot]) if PR[fid].get('clouds_enabled') else rgb01([250, 250, 250]),
                       dalc={ax: rgb01(r['DALC'][slot][ax]) for ax in ('DirectionalXPlus', 'DirectionalXMinus', 'DirectionalZPlus', 'DirectionalZMinus')})
    R['_voli'] = PR[fid]['voli']
    return R

def astra_records(fid):
    x = AR[fid]; c = x['colors']; R = {}
    clouds = [cl for cl in x['clouds'] if cl['enabled'] == 'True'] or x['clouds']
    for slot in SLOTS:
        R[slot] = dict(upper=rgb01(c['SkyUpperColor'][slot]), horizon=rgb01(c['HorizonColor'][slot]),
                       lower=rgb01(c['SkyLowerColor'][slot]), fogfar=rgb01(c['FogFarColor'][slot]),
                       fognear=rgb01(c['FogNearColor'][slot]), sun=rgb01(c['SunColor'][slot]),
                       sunlight=rgb01(c['SunlightColor'][slot]), cloud=rgb01(clouds[0]['colors'][slot]),
                       dalc={ax: rgb01(x['dalc'][slot][ax]) for ax in ('DirectionalXPlus', 'DirectionalXMinus', 'DirectionalZPlus', 'DirectionalZMinus')})
    R['_voli'] = x['volumetric_resolved']; R['_name'] = x['editorid']; R['_ve'] = x['visual_effect']
    return R

def rec_at(R, h, key, C=PICTA_CLMT, ax=None):
    w = clmt_weights(h, C)
    acc = 0.0
    for s in SLOTS:
        v = R[s]['dalc'][ax] if key == 'dalc' else R[s][key]
        acc = acc + w[s] * v
    return acc

def ini_at(I, h, key, T=PICTA_TOD, override=None):
    w = tod_weights(h, T); acc = 0.0
    for p in PERIODS:
        v = override[p] if (override is not None and p in override) else I[p][key]
        acc = acc + w[p] * v
    return acc

# ------------------------------------------------------------------ channel models (pre-tonemap)
def v_sky(I, R, h, band, F=None):
    rk, fk, ik = ('upper', 'sky_top_filter', 'sky_top_int') if band == 'top' else ('horizon', 'sky_horizon_filter', 'sky_horizon_int')
    filt = ini_at(I, h, fk, override=F)
    g = ini_at(I, h, ik) * ini_at(I, h, 'sky_gradient_int')
    return desat(curve(rec_at(R, h, rk), 1.0) * filt * g, ini_at(I, h, 'sky_gradient_desat'))

def v_cloud(I, R, h, F=None):
    return desat(rec_at(R, h, 'cloud') * ini_at(I, h, 'clouds_filter', override=F) * ini_at(I, h, 'clouds_int'), ini_at(I, h, 'clouds_desat'))

def v_fog(I, R, h, F=None):
    return cfilter(curve(rec_at(R, h, 'fogfar'), ini_at(I, h, 'fog_color_curve')), ini_at(I, h, 'fog_filter', override=F), 0.0) * ini_at(I, h, 'fog_color_mult')

def v_sunlight(I, R, h, DLF=None, DLD=None):
    c = desat(rec_at(R, h, 'sunlight'), ini_at(I, h, 'direct_desat', override=DLD))
    return cfilter(c, ini_at(I, h, 'direct_filter', override=DLF), 0.0) * ini_at(I, h, 'direct_int')

def v_ambient(I, R, h, ax):
    return desat(rec_at(R, h, 'dalc', ax=ax), ini_at(I, h, 'ambient_desat')) * ini_at(I, h, 'ambient_int')

def scat_colour(I, R, h, SCo=None, CFS=None):
    """C++ UpdateSkyScattering colour term: (1+(sunN-1)*ColorFromSun)*ScatteringColor (before Intensity)."""
    sunc = cfilter(desat(rec_at(R, h, 'sun'), ini_at(I, h, 'sun_desat')), ini_at(I, h, 'sun_filter'), 0.0)
    peak = max(float(sunc.max()), 1.0); sunN = np.maximum(sunc, 0) / peak
    c = ini_at(I, h, 'scat_from_sun', override=CFS)
    return (1.0 + (sunN - 1.0) * c) * ini_at(I, h, 'scat_color', override=SCo)

def v_sunward(I, R, h, Fh=None, SCo=None, CFS=None):
    """Horizon pixel looking at the sun (view z=0.05, azimuth = sun); SkyScattering.hlsli 84-104, dust terms ~1."""
    hor = v_sky(I, R, h, 'hor', F=Fh); top = v_sky(I, R, h, 'top')
    z = 0.05; sz = sun_z(h); cz = math.sqrt(max(0.0, 1 - sz * sz))
    view = np.array([0, math.sqrt(1 - z * z), z]); sund = np.array([0, cz, sz])
    pgwc = 1.6
    sky = lerp(top, hor, (1 - z) ** pgwc)
    facing = sat(float(view @ sund) * 0.5 + 0.5); away = 1 - facing
    elev = 1 - sat(1 - z) * sat(1 + sz)
    hR = 1.0 / 0.9 ** 3; aT = 100.0 / 0.4 ** 2
    spread = lerp(hR * away * away, aT, elev * elev)
    amount = ini_at(I, h, 'scat_amount') ** 2
    w = sat(amount / (1 + away * spread))
    sunFade = math.sqrt(sat(1 + 2 * sz))
    S = scat_colour(I, R, h, SCo, CFS) * ini_at(I, h, 'scat_int') * sunFade
    airglow = 1 + ini_at(I, h, 'airglow') / (1 + away / ini_at(I, h, 'airglow_range') ** 2)
    aboveH = sat(1 + z * 10) ** 2
    res = lerp(sky * airglow, S, w)
    return lerp(sky, res, aboveH), w, S

# Astralite side (its own records under Soul's near-neutral grade), re-timed onto PICTA clocks for the target
def a_val(AI, AR_, h, chan, ax=None):
    if chan == 'top':
        return desat(rec_at(AR_, h, 'upper') * ini_at(AI, h, 'TopF'), ini_at(AI, h, 'GradDesat'))
    if chan == 'hor':
        return desat(rec_at(AR_, h, 'horizon') * ini_at(AI, h, 'HorF'), ini_at(AI, h, 'GradDesat'))
    if chan == 'cloud':
        return desat(rec_at(AR_, h, 'cloud') * ini_at(AI, h, 'CloudsF'), ini_at(AI, h, 'CloudsDesat'))
    if chan == 'fog':
        return curve(rec_at(AR_, h, 'fogfar'), ini_at(AI, h, 'FogCurve')) * ini_at(AI, h, 'FogF')
    if chan == 'sunlight':
        return desat(rec_at(AR_, h, 'sunlight'), ini_at(AI, h, 'DLDesat')) * ini_at(AI, h, 'DLF')
    if chan == 'ambient':
        return desat(rec_at(AR_, h, 'dalc', ax=ax), ini_at(AI, h, 'AmbDesat'))
    if chan == 'sunward':
        # Astralite lane: dome horizon (NAT weights, z~0 -> horizon band) mixed with Soul scattering S
        hor = a_val(AI, AR_, h, 'hor')
        sunc = desat(rec_at(AR_, h, 'sun'), ini_at(AI, h, 'SunDesat')) * ini_at(AI, h, 'SunF')
        sunN = np.maximum(sunc, 0) / max(float(sunc.max()), 1.0)
        S = (1 + (sunN - 1) * ini_at(AI, h, 'CFS')) * ini_at(AI, h, 'ScatColor') * ini_at(AI, h, 'ScatInt')
        w = ini_at(AI, h, 'Amount') ** 2
        return lerp(hor * (1 + ini_at(AI, h, 'AirGlow')), S, w)
    raise KeyError(chan)

# ------------------------------------------------------------------ solvers
LUMA_WEIGHT = 4.0   # weight of the luminance rows in the joint fit (brightness is the user's hard constraint)

def lsq_periods(target_fn, fixed_night, floor_frac=0.02, scale_fn=None):
    """Joint fit of the 5 free periods x RGB.  Rows: relative per-channel error (weight 1) and, when scale_fn is given,
    relative LUMINANCE error of the visible colour (weight LUMA_WEIGHT).  scale_fn(h) -> per-channel multiplier m(h)
    such that visible(h) = m(h) * filter(h) (componentwise).  NaN targets = unconstrained channel at that hour."""
    if scale_fn is None:
        return _lsq_periods_plain(target_fn, fixed_night, floor_frac)
    T = np.array([target_fn(h) for h in HOURS]); M = np.array([scale_fn(h) for h in HOURS])
    W = np.array([[tod_weights(h)[p] for p in FREE] for h in HOURS]); wN = np.array([tod_weights(h)['Night'] for h in HOURS])
    rows, rhs = [], []
    lum = np.array([0.2126, 0.7152, 0.0722])
    for i in range(len(HOURS)):
        t = T[i]; ok = np.isfinite(t); tt = np.where(ok, t, 0.0)
        for ch in range(3):
            if not ok[ch]: continue
            fl = max(floor_frac * float(np.nanmax(np.abs(T[:, ch]))), 1e-6); sc = 1.0 / max(abs(tt[ch]), fl)
            r = np.zeros(15); r[ch::3] = W[i] * sc; rows.append(r); rhs.append((tt[ch] - wN[i] * fixed_night[ch]) * sc)
        # luminance row on the visible colour: sum_ch lum_ch * m_ch * F_ch(h)  ~  sum_ch lum_ch * m_ch * T_ch
        if ok.all():
            yt = float(np.sum(lum * M[i] * tt))
            if yt > 1e-9:
                r = np.zeros(15)
                for ch in range(3): r[ch::3] = LUMA_WEIGHT * lum[ch] * M[i][ch] * W[i] / yt
                rows.append(r); rhs.append(LUMA_WEIGHT * (yt - float(np.sum(lum * M[i] * wN[i] * np.asarray(fixed_night)))) / yt)
    x, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
    x = np.clip(x, 0.0, 10.0)
    return {p: x[3 * k:3 * k + 3] for k, p in enumerate(FREE)}

def _lsq_periods_plain(target_fn, fixed_night, floor_frac=0.02):
    """Fit 5 period values (Dawn..Dusk) per RGB channel so that sum_p w_p(h) F_p (+ w_Night F_Night) ~ target(h),
    minimising relative error over HOURS.  Returns dict period->rgb and the fit table."""
    T = np.array([target_fn(h) for h in HOURS])            # (n,3)
    W = np.array([[tod_weights(h)[p] for p in FREE] for h in HOURS])
    wN = np.array([tod_weights(h)['Night'] for h in HOURS])
    sol = np.zeros((5, 3))
    for ch in range(3):
        t = T[:, ch]; ok = np.isfinite(t)          # NaN = channel unconstrained at that hour (zero upstream)
        tt = np.where(ok, t, 0.0)
        fl = max(floor_frac * float(np.abs(tt).max()), 1e-6)
        sc = np.where(ok, 1.0 / np.maximum(np.abs(tt), fl), 0.0)
        A = W * sc[:, None]; b = (tt - wN * fixed_night[ch]) * sc
        x, *_ = np.linalg.lstsq(A, b, rcond=None)
        sol[:, ch] = np.clip(x, 0.0, 10.0)
    return {p: sol[i] for i, p in enumerate(FREE)}

def peak_periods(target_fn):
    peaks = dict(Dawn=7.25, Sunrise=9.0, Day=10.0, Sunset=17.0, Dusk=18.75)
    return {p: np.clip(np.asarray(target_fn(h)), 0, 10) for p, h in peaks.items()}

def solve_filter_channel(I, R, AI, AR_, chan):
    """ini-carried channel: target filter T(h) = F_P(h) * (u'(h)/u_P(h)) where u = pre-desat visible."""
    key = {'top': 'sky_top_filter', 'hor': 'sky_horizon_filter', 'cloud': 'clouds_filter', 'fog': 'fog_filter'}[chan]
    dkey = {'top': 'sky_gradient_desat', 'hor': 'sky_gradient_desat', 'cloud': 'clouds_desat', 'fog': None}[chan]
    vfun = {'top': lambda h, F=None: v_sky(I, R, h, 'top', F), 'hor': lambda h, F=None: v_sky(I, R, h, 'hor', F),
            'cloud': lambda h, F=None: v_cloud(I, R, h, F), 'fog': lambda h, F=None: v_fog(I, R, h, F)}[chan]
    def target_vis(h):
        vp = vfun(h); return blend(vp, a_val(AI, AR_, h, chan), alpha_at(h))
    def target_filter(h):
        vp = vfun(h); vt = target_vis(h)
        d = ini_at(I, h, dkey) if dkey else 0.0
        up, ut = inv_desat(vp, d), inv_desat(vt, d)
        Fp = ini_at(I, h, key)
        ratio = np.where(up > 1e-9, ut / np.maximum(up, 1e-9), 1.0)
        return Fp * ratio
    def scale(h):
        Fp = ini_at(I, h, key); vp = vfun(h)
        return np.where(Fp > 1e-9, vp / np.maximum(Fp, 1e-9), 0.0)
    F_lsq = lsq_periods(target_filter, I['Night'][key], scale_fn=scale)
    F_pk = peak_periods(target_filter)
    return dict(key=key, F=F_lsq, F_peak=F_pk, vfun=vfun, target=target_vis)

def solve_sunlight(I, R, AI, AR_):
    """record-carried: kSunlight per CLMT slot gets the hue; DLF -> grey k_p, DirectLightingDesaturation -> 0 (Dawn..Dusk)."""
    vt = lambda h: blend(v_sunlight(I, R, h), a_val(AI, AR_, h, 'sunlight'), alpha_at(h))
    peaks = dict(Sunrise=7.5, Day=13.0, Sunset=18.5)
    newrec = {}
    for s, hs in peaks.items():
        chroma = vt(hs); yrec = Y(R[s]['sunlight'])
        r = norm_y(chroma, yrec)
        if r.max() > 1.0: r = r / r.max()                 # 8-bit headroom; k_p absorbs the loss
        newrec[s] = np.round(r * 255) / 255
    Rb = {s: dict(R[s]) for s in SLOTS}
    for s in newrec: Rb[s] = dict(Rb[s]); Rb[s]['sunlight'] = newrec[s]
    DLD = {p: 0.0 for p in FREE}
    # luminance fit of k_p (linear): Y(V_B(h)) = DLInt(h) * sum_p w_p(h) * Y(Fp (.) D(h)),  Fp = k_p*1 (free) / Picta (Night)
    rows, rhs = [], []
    for h in HOURS:
        w = tod_weights(h); D = desat(rec_at(Rb, h, 'sunlight'), ini_at(I, h, 'direct_desat', override=DLD))
        dli = ini_at(I, h, 'direct_int'); yp = Y(v_sunlight(I, R, h))
        if yp <= 1e-6: continue
        rows.append([dli * w[p] * Y(D) / yp for p in FREE])
        rhs.append((yp - dli * w['Night'] * Y(I['Night']['direct_filter'] * D)) / yp)
    k, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
    k = np.clip(k, 0, 10)
    DLF = {p: np.array([k[i]] * 3) for i, p in enumerate(FREE)}
    vb = lambda h: v_sunlight(I, Rb, h, DLF=DLF, DLD=DLD)
    return dict(rec=newrec, k=dict(zip(FREE, k)), DLF=DLF, DLD=DLD, vb=vb, vt=vt, Rb=Rb)


def _fit_dlf(I, Rb, DLD, vt):
    """LSQ: DirectLightingColorFilter per period (RGB, Dawn..Dusk) so that DLInt*DLF(h)*Desat(rec'(h),d'(h)) ~ vt(h)."""
    def freq(h):
        D = desat(rec_at(Rb, h, 'sunlight'), ini_at(I, h, 'direct_desat', override=DLD))
        return vt(h) / (ini_at(I, h, 'direct_int') * np.maximum(D, 1e-4))
    return lsq_periods(freq, I['Night']['direct_filter'])

def solve_sunlight_variant(I, R, AI, AR_, mode):
    """mode 'ini': records Sunrise/Day/Sunset -> neutral grey (Y kept), DLF carries all hue (TOD clock).
       mode 'hyb': records carry the blended chroma, DLF re-fitted (RGB) as the clock corrector."""
    vt = lambda h: blend(v_sunlight(I, R, h), a_val(AI, AR_, h, 'sunlight'), alpha_at(h))
    peaks = dict(Sunrise=7.5, Day=13.0, Sunset=18.5)
    newrec = {}
    for s, hs in peaks.items():
        yrec = Y(R[s]['sunlight'])
        if mode == 'ini':
            r = np.array([yrec] * 3)
        else:
            r = norm_y(vt(hs), yrec)
            if r.max() > 1.0: r = r / r.max()
        newrec[s] = np.round(np.clip(r, 0, 1) * 255) / 255
    Rb = {s: dict(R[s]) for s in SLOTS}
    for s in newrec: Rb[s] = dict(Rb[s]); Rb[s]['sunlight'] = newrec[s]
    DLD = {p: 0.0 for p in FREE}
    DLF = _fit_dlf(I, Rb, DLD, vt)
    vb = lambda h: v_sunlight(I, Rb, h, DLF=DLF, DLD=DLD)
    return dict(rec=newrec, k={p: float(Y(DLF[p])) for p in FREE}, DLF=DLF, DLD=DLD, vb=vb, vt=vt, Rb=Rb)

LUMA_PASS = False
D_MIN = 0.05   # DirectLightingDesaturation floor used only where a mix is requested (unlocks the zero blue channel)

def period_alpha():
    """alpha seen by each TIMEOFDAY period = w_p-weighted mean of alpha(h) over the day."""
    out = {}
    for p in PERIODS:
        ws = [tod_weights(h)[p] for h in HOURS]; s = sum(ws)
        out[p] = (sum(w * alpha_at(h) for w, h in zip(ws, HOURS)) / s) if s > 0 else 0.0
    return out

def solve_sunlight_filter(I, R, AI, AR_):
    """CHOSEN: records untouched (Picta), DirectLightingColorFilter carries the correction (TIMEOFDAY, LSQ),
    DirectLightingDesaturation lifted to >= D_MIN only in periods that receive a mix (zero-channel unlock)."""
    ap = period_alpha()
    DLD = {}
    for p in FREE:
        dP = I[p]['direct_desat']
        DLD[p] = D_MIN if (ap[p] > 1e-6 and dP < D_MIN) else dP     # minimal change: only lift negative (saturation-boost) periods
    vt = lambda h: blend(v_sunlight(I, R, h), a_val(AI, AR_, h, 'sunlight'), alpha_at(h))
    def freq(h):
        D = desat(rec_at(R, h, 'sunlight'), ini_at(I, h, 'direct_desat', override=DLD))
        q = vt(h) / (ini_at(I, h, 'direct_int') * np.maximum(D, 1e-9))
        return np.where(D > 1e-3, q, np.nan)
    def dscale(h):
        D = desat(rec_at(R, h, 'sunlight'), ini_at(I, h, 'direct_desat', override=DLD))
        return ini_at(I, h, 'direct_int') * D
    DLF = lsq_periods(freq, I['Night']['direct_filter'], scale_fn=dscale)
    if LUMA_PASS:
        # second pass: one scalar per period, least squares on relative LUMINANCE error vs Picta (brightness has priority)
        rows, rhs = [], []
        for h in HOURS:
            yp = Y(v_sunlight(I, R, h))
            if yp <= 1e-6: continue
            D = desat(rec_at(R, h, 'sunlight'), ini_at(I, h, 'direct_desat', override=DLD)); w = tod_weights(h); dli = ini_at(I, h, 'direct_int')
            rows.append([dli * w[p] * Y(DLF[p] * D) / yp for p in FREE])
            rhs.append((yp - dli * w['Night'] * Y(I['Night']['direct_filter'] * D)) / yp)
        s, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
        DLF = {p: np.clip(DLF[p] * s[i], 0, 10) for i, p in enumerate(FREE)}
    vb = lambda h: v_sunlight(I, R, h, DLF=DLF, DLD=DLD)
    return dict(rec={s: R[s]['sunlight'] for s in ('Sunrise', 'Day', 'Sunset')}, k={p: float(Y(DLF[p])) for p in FREE},
                DLF=DLF, DLD=DLD, vb=vb, vt=vt, Rb=R)

def solve_scatter_filter(I, R, AI, AR_):
    """CHOSEN: ColorFromSun = lerp(Picta, Astralite, alpha_p) (structural mix weight), ScatteringColor carries the hue (LSQ)."""
    ap = period_alpha()
    CFS = {p: lerp(I[p]['scat_from_sun'], AI[p]['CFS'], ap[p]) for p in FREE}
    tgt = lambda h: blend(scat_colour(I, R, h), a_scat(AI, AR_, h), alpha_at(h))
    def req(h):
        base = scat_colour(I, R, h, SCo={p: np.array([1.0, 1, 1]) for p in PERIODS}, CFS=CFS)
        return np.where(base > 1e-3, tgt(h) / np.maximum(base, 1e-9), np.nan)
    SCo = lsq_periods(req, I['Night']['scat_color'],
                      scale_fn=lambda h: scat_colour(I, R, h, SCo={p: np.array([1.0, 1, 1]) for p in PERIODS}, CFS=CFS))
    return dict(SC=SCo, CFS=CFS, req=tgt)

PV = j(os.path.join(MAP, 'picta-colour', 'picta_voli.json'))
def picta_voli(fid):
    f = PV[fid]['fields']
    return dict(I=float(f.get('Intensity', 1)), cc=float(f.get('CustomColorContribution', 0)),
                col=np.array([float(f['ColorR']), float(f['ColorG']), float(f['ColorB'])]), dens=float(f.get('DensityContribution', 0)))
def astra_voli(AR_, s):
    a = AR_['_voli'][s]
    return dict(I=float(a['intensity']), cc=float(a['custom_color_contribution']), col=np.array(a['color_rgb01'], float),
                dens=float(a['density_contribution']), name=a['editorid'])
PICTA_GVR = {'Dawn': .75, 'Sunrise': 2.0, 'Day': 4.0, 'Sunset': 2.0, 'Dusk': .75, 'Night': 8.0}
ASTRA_SLOT_PEAK = dict(Sunrise=7.0, Day=13.0, Sunset=19.0)   # midpoints of Astralite's own CLMT windows

def voli_at(slotvals, h):
    c = clmt_weights(h); I_ = cc = 0.0; col = np.zeros(3); d = 0.0
    for s in SLOTS:
        v = slotvals[s]; I_ += c[s] * v['I']; cc += c[s] * v['cc']; col = col + c[s] * v['col']; d += c[s] * v['dens']
    return I_, cc, col, d

def solve_voli(I, R, AI, AR_, sl):
    """Volumetric fog/god-ray AIR.  Records: Astralite VOLI copied verbatim into the Sunrise/Day/Sunset slots (Night = Picta).
    Hue: GAMEVOLUMETRICRAYS ColorFilter -> 1,1,1 in Dawn..Dusk (the VOLI custom colour + baby sunlight carry it; no multiply).
    Amplitude: GAMEVOLUMETRICRAYS Intensity (TIMEOFDAY) solved by LSQ so that VL radiance / key-light luminance
    equals Astralite's own ratio at the same CLMT slot (scalar regimes are translated as ratios, never copied)."""
    picta_slots = {s: picta_voli(R['_voli'][s]) for s in SLOTS}
    baby_slots = {s: (astra_voli(AR_, s) if s != 'Night' else picta_slots['Night']) for s in SLOTS}
    # Astralite ratio per slot, in its own lane
    ratioA = {}
    for s, hs in ASTRA_SLOT_PEAK.items():
        v = astra_voli(AR_, s)
        LA = desat(AR_[s]['sunlight'], ini_at(AI, hs, 'DLDesat', T=NAT_TOD)) * ini_at(AI, hs, 'DLF', T=NAT_TOD)
        gA = ini_at(AI, hs, 'GVRInt', T=NAT_TOD)
        vlc = lerp(LA, v['col'], v['cc'])
        ratioA[s] = v['I'] * gA * Y(vlc) / max(Y(LA), 1e-6)
    def rel_picta(h):
        Lp = v_sunlight(I, R, h); Ip, ccp, colp, dp = voli_at(picta_slots, h)
        gp = sum(tod_weights(h)[p] * PICTA_GVR[p] for p in PERIODS)
        vlp = lerp(Lp, colp, ccp) * ini_at(I, h, 'godray_filter')
        return Ip * gp * Y(vlp) / max(Y(Lp), 1e-6)
    def target(h):
        c = clmt_weights(h)
        if c['Night'] >= 1: return np.nan
        astra = sum(c[s] * ratioA[s] for s in ratioA) * DIALS['VOL_AMOUNT'] / max(1e-6, 1 - c['Night'])
        return max(astra, rel_picta(h))     # floor: the baby's volumetric light is never weaker than Picta's (fog is ADDED)
    GVRF = {p: np.array([1.0, 1, 1]) for p in FREE}
    def req(h):
        t = target(h)
        # moon-crossfade hours (TOD Night weight > 0) are left out of the fit: Picta's Night GVR 8.0 owns them and
        # Sky Sync's under-horizon VL dimming (DimVolumetricLighting=true, HorizonFadeHours 0.7) acts there
        if not np.isfinite(t) or tod_weights(h)['Night'] > 0: return np.array([np.nan] * 3)
        L = sl['vb'](h); I_, cc, col, d = voli_at(baby_slots, h)
        vlc = lerp(L, col, cc)
        g = t * max(Y(L), 1e-6) / max(I_ * Y(vlc), 1e-9)
        return np.array([g] * 3)
    G = lsq_periods(req, np.array([PICTA_GVR['Night']] * 3))
    GVR = {p: float(G[p][0]) for p in FREE}
    rows = []
    for h in REPORT_H:
        Lp = v_sunlight(I, R, h); Ip, ccp, colp, dp = voli_at(picta_slots, h)
        gp = sum(tod_weights(h)[p] * PICTA_GVR[p] for p in PERIODS)
        vlp = lerp(Lp, colp, ccp) * ini_at(I, h, 'godray_filter')
        Lb = sl['vb'](h); Ib, ccb, colb, db = voli_at(baby_slots, h)
        gb = sum(tod_weights(h)[p] * (GVR[p] if p in GVR else PICTA_GVR[p]) for p in PERIODS)
        vlb = lerp(Lb, colb, ccb) * sum(tod_weights(h)[p] * (GVRF[p] if p in GVRF else I[p]['godray_filter']) for p in PERIODS)
        rows.append(dict(h=h, picta=dict(eff=round(Ip * gp, 2), dens=round(dp, 2), rel=round(Ip * gp * Y(vlp) / max(Y(Lp), 1e-6), 2), colour=desc(vlp)),
                         baby=dict(eff=round(Ib * gb, 2), dens=round(db, 2), rel=round(Ib * gb * Y(vlb) / max(Y(Lb), 1e-6), 2), colour=desc(vlb)),
                         astralite_target_rel=(round(float(target(h)), 2) if np.isfinite(target(h)) else None)))
    return dict(GVR=GVR, GVRF=GVRF, ratioA=ratioA, rows=rows, slots={s: baby_slots[s].get('name', 'Picta night VOLI') for s in SLOTS})

def solve_dalc(I, R, AI, AR_, ax):
    peaks = dict(Sunrise=7.5, Day=13.0, Sunset=18.5)
    out = {}
    for s, hs in peaks.items():
        vp = v_ambient(I, R, hs, ax); va = a_val(AI, AR_, hs, 'ambient', ax)
        vt = blend(vp, va, alpha_at(hs))
        d, inten = ini_at(I, hs, 'ambient_desat'), ini_at(I, hs, 'ambient_int')
        rec = inv_desat(vt / inten, d)
        # what the Picta record would have to be at that instant, for reference
        out[s] = np.clip(np.round(rec * 255), 0, 255) / 255
    return out

def a_scat(AI, AR_, h):
    sunc = desat(rec_at(AR_, h, 'sun'), ini_at(AI, h, 'SunDesat')) * ini_at(AI, h, 'SunF')
    sunN = np.maximum(sunc, 0) / max(float(sunc.max()), 1.0)
    return (1 + (sunN - 1) * ini_at(AI, h, 'CFS')) * ini_at(AI, h, 'ScatColor')

def solve_scatter(I, R, AI, AR_, Fh=None):
    """Scattering colour S is its own channel (sky near the sun + cloud sun-lighting).  ColorFromSun -> 0 (Dawn..Dusk)
    so ScatteringColor becomes the only hue carrier; target = blend(S_Picta, S_Astralite) with S_Picta's Y."""
    CFS = {p: 0.0 for p in FREE}
    tgt = lambda h: blend(scat_colour(I, R, h), a_scat(AI, AR_, h), alpha_at(h))
    SCo = lsq_periods(tgt, I['Night']['scat_color'])
    return dict(SC=SCo, CFS=CFS, req=tgt)

# ------------------------------------------------------------------ run
out_lines, OUT = [], {'dials': DIALS, 'weathers': {}}
def P(s=''): out_lines.append(s)

P('BABY MODEL - per-channel physics (pre-tonemap engine-value space; Y = Rec.709 luminance; hue/chroma = OKLCh at equal Y)')
P(f'dials: {DIALS}')
P('clocks: ini on Picta [TIMEOFDAY] 5.5/7.25/9/10/17/18.75/20.5; records on Picta CLMT 06-09/17-20 (midpoint-peak rule ASSUMED)')
P('')
P('== CLOCK ALIGNMENT (Picta) hour | TOD weights | CLMT record weights | mix alpha(h)')
for h in [5.5, 6.0, 6.75, 7.25, 7.5, 8.0, 8.25, 9.0, 10.0, 13.0, 16.0, 17.0, 17.75, 18.5, 18.75, 19.5, 20.0, 20.5]:
    tw = {k: round(v, 2) for k, v in tod_weights(h).items() if v > 0}
    cw = {k: round(v, 2) for k, v in clmt_weights(h).items() if v > 0}
    P(f'  {h:5.2f}  TOD {tw}  CLMT {cw}  alpha={alpha_at(h):.2f}')

# ---- opposite-hue study
P('')
P('== OPPOSITE-HUE BLEND: Picta visible vs Astralite visible at 07:30 (A01 / SkyrimClear), modes rgb / lab / lch')
I = picta_ini(WEATHERS['A01 Clear']['ini']); R = picta_records(WEATHERS['A01 Clear']['rec'])
AI = soul_ini('SoulClear.ini'); AR_ = astra_records('00081A:Skyrim.esm')
study = {}
for chan, vp, va in [('sky horizon', v_sky(I, R, 7.5, 'hor'), a_val(AI, AR_, 7.5, 'hor')),
                     ('fog far', v_fog(I, R, 7.5), a_val(AI, AR_, 7.5, 'fog')),
                     ('sunlight', v_sunlight(I, R, 7.5), a_val(AI, AR_, 7.5, 'sunlight')),
                     ('ambient X+', v_ambient(I, R, 7.5, 'DirectionalXPlus'), a_val(AI, AR_, 7.5, 'ambient', 'DirectionalXPlus'))]:
    P(f'  {chan}: Picta {desc(vp)} | Astralite {desc(va)}')
    study[chan] = {}
    for a in (0.25, 0.5, 0.75):
        row = []
        for m in ('rgb', 'lab', 'lch'):
            c = blend(vp, va, a, m); L, C, hh = lch(norm_y(c)); row.append(f'{m}: h={hh:5.1f} C={C:.3f}')
            study[chan][f'{m}@{a}'] = dict(h=round(hh, 1), C=round(C, 3))
        P(f'    a={a:.2f}  ' + ' | '.join(row))
OUT['opposite_hue'] = study

# ---- per weather
for wname, W in WEATHERS.items():
    I = picta_ini(W['ini']); R = picta_records(W['rec'])
    AI = soul_ini(W['soul']); AR_ = astra_records(W['partner'])
    P(''); P('=' * 110)
    P(f'== {wname}  (Picta {W["rec"].split(":")[0]} / {W["ini"].split("/")[-1]})  <-  Astralite {AR_["_name"]} ({W["partner"].split(":")[0]}) + {W["soul"]}')
    WO = {}
    sols = {}
    for chan in ('top', 'hor', 'cloud', 'fog'):
        sols[chan] = solve_filter_channel(I, R, AI, AR_, chan)
    SUN_VARIANTS = {'filter': lambda: solve_sunlight_filter(I, R, AI, AR_), 'rec': lambda: solve_sunlight(I, R, AI, AR_),
                    'ini': lambda: solve_sunlight_variant(I, R, AI, AR_, 'ini'), 'hyb': lambda: solve_sunlight_variant(I, R, AI, AR_, 'hyb')}
    slv = {k: f() for k, f in SUN_VARIANTS.items()}
    sc = solve_scatter_filter(I, R, AI, AR_)
    sc_c0 = solve_scatter(I, R, AI, AR_)
    dalc = {ax: solve_dalc(I, R, AI, AR_, ax) for ax in ('DirectionalXPlus', 'DirectionalXMinus', 'DirectionalZPlus', 'DirectionalZMinus')}

    # identity check first (all mixes 0) -> decides the sunlight carrier
    saved = dict(DIALS)
    for k in ('MIX_DAWN', 'MIX_DAY', 'MIX_DUSK'): DIALS[k] = 0.0
    idt = {}
    for chan in ('top', 'hor', 'cloud', 'fog'):
        s0 = solve_filter_channel(I, R, AI, AR_, chan)
        idt[chan] = max(de_ok(s0['vfun'](h, s0['F']), s0['vfun'](h)) for h in HOURS)
    lit = [h for h in HOURS if Y(v_sunlight(I, R, h)) > 1e-6]
    for k, f in SUN_VARIANTS.items():
        s0 = f()
        idt[f'sunlight[{k}]'] = max(de_ok(s0['vb'](h), v_sunlight(I, R, h)) for h in lit)
        idt[f'sunlight[{k}]_dY_max_pct'] = max(abs(100 * (Y(s0['vb'](h)) / Y(v_sunlight(I, R, h)) - 1)) for h in lit)
    for nm, f in (('scatter[filter: CFS lerp + SC]', solve_scatter_filter), ('scatter[CFS=0 + SC] rejected', solve_scatter)):
        sc0 = f(I, R, AI, AR_)
        idt[nm] = max(de_ok(scat_colour(I, R, h, sc0['SC'], sc0['CFS']), scat_colour(I, R, h)) for h in HOURS if 6.0 <= h <= 20.0)
    for ax in ('DirectionalXPlus', 'DirectionalZMinus'):
        d0 = solve_dalc(I, R, AI, AR_, ax)
        idt[f'dalc {ax}'] = max(de_ok(d0[s], R[s]['dalc'][ax]) for s in d0)
    DIALS.update(saved)
    P('  -- IDENTITY CHECK (all mixes = 0): max OKLab chroma error vs Picta over 05:30-20:30 (0.02 ~ just noticeable)')
    for k, v in idt.items(): P(f'       {k:32s} {v:8.4f}')
    best = min(('filter', 'ini', 'hyb', 'rec'), key=lambda k: idt[f'sunlight[{k}]'] + idt[f'sunlight[{k}]_dY_max_pct'] / 100.0)
    sl = slv[best]
    P(f'  -- sunlight carrier chosen by identity error: {best}')
    vo = solve_voli(I, R, AI, AR_, sl)

    P('  -- solved ini values (Dawn..Dusk; Night = Picta).  LSQ fit vs Picta original')
    for chan, s in sols.items():
        for p in FREE:
            P(f'     [{s["key"]}{p}]  picta={np.round(I[p][s["key"]], 3).tolist()}  baby={np.round(s["F"][p], 3).tolist()}  (peak-sample {np.round(s["F_peak"][p], 3).tolist()})')
    for p in FREE:
        P(f'     [ScatteringColor{p}] picta=[1,1,1] baby={np.round(sc["SC"][p], 3).tolist()}  ColorFromSun{p}={sc["CFS"][p]:.3f} (picta {I[p]["scat_from_sun"]})')
    for p in FREE:
        P(f'     [DirectLightingColorFilter{p}] picta={np.round(I[p]["direct_filter"], 3).tolist()} -> {np.round(sl["DLF"][p], 3).tolist()}; DirectLightingDesaturation{p} {I[p]["direct_desat"]} -> {sl["DLD"][p]}')
    P('  -- solved record values (bytes)')
    for s in ('Sunrise', 'Day', 'Sunset'):
        P(f'     SunlightColor[{s}] picta={np.round(R[s]["sunlight"] * 255).astype(int).tolist()} -> baby={np.round(sl["rec"][s] * 255).astype(int).tolist()}')
    for ax in dalc:
        P(f'     DALC {ax:18s} ' + '  '.join(f'{s}: {np.round(R[s]["dalc"][ax] * 255).astype(int).tolist()}->{np.round(dalc[ax][s] * 255).astype(int).tolist()}' for s in ('Sunrise', 'Day', 'Sunset')))

    # evaluation
    P('  -- evaluation per hour: before (Picta) | target | after (baby, as solved) ; dh = hue error after-vs-target (deg), dE = OKLab chroma error, dY% = luminance change vs Picta')
    rows = {}
    def ev(label, fp, ft, fb):
        P(f'   {label}')
        recs = []
        for h in REPORT_H:
            vp, vt, vb = fp(h), ft(h), fb(h)
            if Y(vp) <= 1e-9: continue
            dy = 100 * (Y(vb) / Y(vp) - 1)
            P(f'     {h:5.2f}  P {desc(vp)} | T {desc(vt)} | B {desc(vb)} | dh={hue_diff(vb, vt):5.1f} dE={de_ok(vb, vt):.3f} dY={dy:+5.1f}%')
            Lp, Cp, hp = lch(norm_y(vp)); Lb, Cb, hb = lch(norm_y(vb))
            recs.append(dict(h=h, picta=dict(h=round(hp, 1), C=round(Cp, 3), Y=Y(vp)), baby=dict(h=round(hb, 1), C=round(Cb, 3), Y=Y(vb)),
                             hue_err_vs_target=round(hue_diff(vb, vt), 1), dE=round(de_ok(vb, vt), 3), dY_pct=round(dy, 2)))
        rows[label] = recs
    for chan, s in sols.items():
        F = s['F']; vfun = s['vfun']
        ev({'top': 'sky zenith', 'hor': 'sky horizon (away from sun)', 'cloud': 'cloud base colour', 'fog': 'fog far colour'}[chan],
           lambda h, vfun=vfun: vfun(h), s['target'], lambda h, vfun=vfun, F=F: vfun(h, F))
    ev('scattering colour S (sun-side sky glow + cloud sun-lighting)', lambda h: scat_colour(I, R, h), sc['req'],
       lambda h: scat_colour(I, R, h, sc['SC'], sc['CFS']))
    ev('sunward horizon pixel (information: dome x AirGlow mixed with S)',
       lambda h: v_sunward(I, R, h)[0],
       lambda h: blend(v_sunward(I, R, h)[0], a_val(AI, AR_, h, 'sunward'), alpha_at(h)),
       lambda h: v_sunward(I, R, h, Fh=sols['hor']['F'], SCo=sc['SC'], CFS=sc['CFS'])[0])
    for k in ('filter', 'hyb', 'ini', 'rec'):
        ev(f'direct sunlight [{k} carrier]' + (' <- CHOSEN' if k == best else ''), lambda h: v_sunlight(I, R, h), slv[k]['vt'], slv[k]['vb'])
    Rd = {s: dict(R[s]) for s in SLOTS}
    for s in ('Sunrise', 'Day', 'Sunset'):
        Rd[s] = dict(Rd[s]); Rd[s]['dalc'] = dict(R[s]['dalc'])
        for ax in dalc: Rd[s]['dalc'][ax] = dalc[ax][s]
    for ax in ('DirectionalXPlus', 'DirectionalZMinus'):
        ev(f'ambient DALC {ax}', lambda h, ax=ax: v_ambient(I, R, h, ax),
           lambda h, ax=ax: blend(v_ambient(I, R, h, ax), a_val(AI, AR_, h, 'ambient', ax), alpha_at(h)),
           lambda h, ax=ax: v_ambient(I, Rd, h, ax))
    WO['sun_carrier'] = best
    P('   volumetric light: slots ' + json.dumps(vo['slots']) + '  GAMEVOLUMETRICRAYS Intensity ' + json.dumps({p: round(v, 3) for p, v in vo['GVR'].items()}) + ' (Picta 0.75/2/4/2/0.75), ColorFilter 1,1,1, RangeFactor 1.0')
    P('     hour | Picta eff, density, VL/keylight ratio, colour | baby eff, density, ratio, colour | Astralite ratio (target)')
    for r in vo['rows']:
        P(f"     {r['h']:5.2f} | P {r['picta']['eff']:6.2f} d{r['picta']['dens']:.2f} rel {r['picta']['rel']:6.2f} {r['picta']['colour']} | B {r['baby']['eff']:6.2f} d{r['baby']['dens']:.2f} rel {r['baby']['rel']:6.2f} {r['baby']['colour']} | A {r['astralite_target_rel']}")
    WO['voli'] = dict(GVR=vo['GVR'], slots=vo['slots'], rows=vo['rows'])
    # transition cross-term (only for the first two weathers, clear -> rain)
    WO['eval'] = rows; WO['identity_max_dE'] = {k: round(v, 4) for k, v in idt.items()}
    WO['solved'] = {chan: {p: np.round(s['F'][p], 4).tolist() for p in FREE} for chan, s in sols.items()}
    WO['solved']['ScatteringColor'] = {p: np.round(sc['SC'][p], 4).tolist() for p in FREE}
    WO['solved']['ColorFromSun'] = {p: round(float(sc['CFS'][p]), 4) for p in FREE}
    WO['solved']['DirectLightingDesaturation'] = {p: round(float(sl['DLD'][p]), 4) for p in FREE}
    WO['period_alpha'] = {p: round(v, 3) for p, v in period_alpha().items()}
    WO['solved']['DirectLightingColorFilter'] = {p: np.round(sl['DLF'][p], 4).tolist() for p in FREE}
    WO['solved']['SunlightRecord'] = {s: np.round(sl['rec'][s] * 255).astype(int).tolist() for s in sl['rec']}
    WO['solved']['DALC'] = {ax: {s: np.round(dalc[ax][s] * 255).astype(int).tolist() for s in dalc[ax]} for ax in dalc}
    OUT['weathers'][wname] = WO
    sols_cache = OUT.setdefault('_cache', {}); sols_cache[wname] = (I, R, AI, AR_, sols, sl, sc, Rd)

# ---- transition cross-term clear -> rain
P(''); P('=' * 110)
P('== WEATHER-TRANSITION CROSS-TERM  A01 Clear -> D03 Rain, t = currentWeatherPct.  runtime = engine lerps records, E11 lerps ini, product taken;')
P('   ideal = lerp of the two endpoint visible colours.  Reported at t=0.5: hue gap and luminance gap runtime-vs-ideal, Picta vs baby.')
ca, cb = OUT['_cache']['A01 Clear'], OUT['_cache']['D03 Rain Light']
def mixI(Ia, Ib, t):
    return {p: {k: (None if Ia[p][k] is None or Ib[p].get(k) is None else lerp(Ia[p][k], Ib[p][k], t)) for k in Ia[p]} for p in PERIODS}
def mixR(Ra, Rb_, t):
    out = {}
    for s in SLOTS:
        out[s] = {}
        for k, v in Ra[s].items():
            if k == 'dalc': out[s][k] = {ax: lerp(v[ax], Rb_[s][k][ax], t) for ax in v}
            else: out[s][k] = lerp(v, Rb_[s][k], t)
    return out
def with_filters(I, sols, sc, sl):
    J = {p: dict(I[p]) for p in PERIODS}
    for chan, s in sols.items():
        for p in FREE: J[p][s['key']] = s['F'][p]
    for p in FREE:
        J[p]['scat_color'] = sc['SC'][p]; J[p]['scat_from_sun'] = sc['CFS'][p]
        J[p]['direct_filter'] = sl['DLF'][p]; J[p]['direct_desat'] = sl['DLD'][p]
    return J
cross = {}
for lane in ('picta', 'baby'):
    Ia, Ra = ca[0], ca[1]; Ib, Rb_ = cb[0], cb[1]
    if lane == 'baby':
        Ia, Ra = with_filters(ca[0], ca[4], ca[6], ca[5]), ca[7]; Ib, Rb_ = with_filters(cb[0], cb[4], cb[6], cb[5]), cb[7]
        for s in ('Sunrise', 'Day', 'Sunset'):
            Ra[s] = dict(Ra[s]); Ra[s]['sunlight'] = ca[5]['rec'][s]; Rb_[s] = dict(Rb_[s]); Rb_[s]['sunlight'] = cb[5]['rec'][s]
    for h in (7.25, 13.0, 18.75):
        Im, Rm = mixI(Ia, Ib, 0.5), mixR(Ra, Rb_, 0.5)
        for name, f in (('sky horizon', lambda I_, R_: v_sky(I_, R_, h, 'hor')), ('fog far', lambda I_, R_: v_fog(I_, R_, h)),
                        ('sunlight', lambda I_, R_: v_sunlight(I_, R_, h)), ('ambient X+', lambda I_, R_: v_ambient(I_, R_, h, 'DirectionalXPlus'))):
            run = f(Im, Rm); ideal = lerp(f(Ia, Ra), f(Ib, Rb_), 0.5)
            g = dict(hue_gap=round(hue_diff(run, ideal), 2), Y_gap_pct=round(100 * (Y(run) / Y(ideal) - 1), 2) if Y(ideal) > 1e-9 else 0.0,
                     endpoints=f'{desc(f(Ia, Ra))} -> {desc(f(Ib, Rb_))}')
            cross[f'{lane} {h} {name}'] = g
            P(f'   {lane:5s} {h:5.2f} {name:12s} hue gap {g["hue_gap"]:5.2f} deg, Y gap {g["Y_gap_pct"]:+6.2f}%   [{g["endpoints"]}]')
OUT['transition_crossterm'] = cross

del OUT['_cache']
open(os.path.join(HERE, 'baby_model_out.txt'), 'w', encoding='utf-8').write('\n'.join(out_lines))
def conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.floating,)): return float(o)
    raise TypeError(type(o))
json.dump(OUT, open(os.path.join(HERE, 'baby_model_out.json'), 'w', encoding='utf-8'), indent=1, default=conv)
print('\n'.join(out_lines))
