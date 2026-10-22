"""PICTA-SAFE baby (v2): re-hue Picta's own Effects 11 colour filters toward Astralite tones with a luminance lock,
plus minimal record edits only where E11 has no lever (DALC ambient, SkyStaticsColor).

READ-ONLY on C:/1. AUTHORIA.  Writes only under design/picta-safe/out.

Per channel, per changed period p:
    u_p   = lerp(unit(F_p_picta), unit(A_p), t_p)          unit(c) = c / Y(c), Y = Rec.709 linear luma
    F_p'  = k_p * u_p
    k_p   = least-squares luminance lock over every 15-min step 05:00-21:30, using the real E11 chain for that channel
            (time-of-day weights, record colour under it on Picta's climate, desaturation, intensities), so that
            Y(baby component) == Y(Picta component) at every hour, not just at the period peak.
A_p = Astralite on-screen colour (Soul Core filters are 1,1,1 / curves 1 -> record colour == on-screen chroma),
      taken as the family-equal mix of the Picta weather's Astralite partners (pairing_table family_partner_summary).
t_p = STRENGTH * channel multiplier * phase factor.  Night + Interior periods are never touched.
"""
import json, math, os, re, colorsys, copy, itertools
import numpy as np

BASE = "C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby"
MAP = BASE + "/map"
OUT = BASE + "/design/picta-safe/out"
DARK = "C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1/enbseries"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------------------------------------------- DIALS
STRENGTH = float(os.environ.get('BABY_STRENGTH', '0.6'))
MULT = dict(sky=1.0, clouds=0.8, fog=1.0, volfog=1.0, light=0.5, ambient=0.8, statics=1.0)
DONOR_MODE = os.environ.get('BABY_DONOR', 'family')       # 'family' (default) or 'canonical'
PH = 2 * (7.25 - 6.0) / 3.0                                 # 0.833: share of sunrise/sunset record colour at E11 Dawn/Dusk peak
SKY_MAP = {'Dawn': ('Sunrise', PH), 'Sunrise': ('Day', 1.0), 'Day': ('Day', 1.0), 'Sunset': ('Day', 1.0), 'Dusk': ('Sunset', PH)}
LIGHT_MAP = {'Sunrise': ('Sunrise', 1.0), 'Day': ('Day', 1.0), 'Sunset': ('Sunset', 1.0)}
REC_SLOTS = ['Sunrise', 'Day', 'Sunset']
LUMA_TOL = 0.01                                             # 1 % (below the ~2 % luminance JND); target is << 0.5 %

# ---------------------------------------------------------------------------------------------------------------- donors
astr = json.load(open(MAP + '/astralite-colour/astralite_rotating_weathers_colour.json', encoding='utf-8'))
pic = json.load(open(MAP + '/picta-colour/picta_wthr_colours.json', encoding='utf-8'))
pal = json.load(open(MAP + '/astralite-colour/astralite_palette_summary.json', encoding='utf-8'))
pt = json.load(open(MAP + '/pairing/pairing_table.json', encoding='utf-8'))
BY_EDID = {v['editorid']: k for k, v in astr.items()}

CANON = {'Clear': 'SkyrimClear', 'Clear_A': 'SkyrimClear_A', 'Cloudy': 'SkyrimCloudy', 'Cloudy_A': 'SkyrimCloudy_A',
         'Fog': 'SkyrimFog', 'OvercastRain': 'SkyrimOvercastRain', 'StormRain': 'SkyrimStormRain',
         'OvercastSnow': 'SkyrimOvercastSnow', 'StormSnow': 'SkyrimStormSnow'}
FOGMIX = {'SkyrimFog': 0.6, 'SkyrimCloudy': 0.4}
CANON_BY_PICTA = {
    'PIC_WTHR_MASTER_A01_Clear': {'SkyrimClear': 1}, 'PIC_WTHR_MASTER_A02_Clear_Aurora': {'SkyrimClear_A': 1},
    'PIC_WTHR_MASTER_A03_Clear_Mist': {'SkyrimClear': 1}, 'PIC_WTHR_MASTER_B01_Lightly_Cloudy': {'SkyrimClear': 1},
    'PIC_WTHR_MASTER_B02_Lightly_Cloudy_Aurora': {'SkyrimClear_A': 0.7, 'SkyrimCloudy_A': 0.3},
    'PIC_WTHR_MASTER_B03_Lightly_Cloudy_Misty_Fog': FOGMIX, 'PIC_WTHR_MASTER_C01_Cloudy': {'SkyrimCloudy': 1},
    'PIC_WTHR_MASTER_C02_Cloudy_Storm': {'SkyrimCloudy': 1}, 'PIC_WTHR_MASTER_C03_Cloudy_Light_Fog': FOGMIX,
    'PIC_WTHR_MASTER_C04_Cloudy_Rain_Very_Light': {'SkyrimOvercastRain': 1}, 'PIC_WTHR_MASTER_C05_Cloudy_Snow_Very_Light': {'SkyrimOvercastSnow': 1},
    'PIC_WTHR_MASTER_D01_Overcast': FOGMIX, 'PIC_WTHR_MASTER_D02_Overcast_Heavy_Fog': {'SkyrimFog': 1},
    'PIC_WTHR_MASTER_D03_Overcast_Rain_Light': {'SkyrimOvercastRain': 1}, 'PIC_WTHR_MASTER_D04_Overcast_Rain_Medium': {'SkyrimOvercastRain': 1},
    'PIC_WTHR_MASTER_D05_Overcast_Snow_Light': {'SkyrimOvercastSnow': 1}, 'PIC_WTHR_MASTER_D06_Overcast_Snow_Medium': {'SkyrimOvercastSnow': 1},
    'PIC_WTHR_MASTER_E01_Storm_Thunder': {'SkyrimStormRain': 1}, 'PIC_WTHR_MASTER_E02_Storm_Cold_Thunder': {'SkyrimStormSnow': 1},
    'PIC_WTHR_MASTER_E03_Storm_Rain_Heavy_Thunder': {'SkyrimStormRain': 1}, 'PIC_WTHR_MASTER_E04_Storm_Rain_Extreme_Thunder': {'SkyrimStormRain': 1},
    'PIC_WTHR_MASTER_E05_Storm_Snow_Heavy': {'SkyrimStormSnow': 1}, 'PIC_WTHR_MASTER_E06_Storm_Snow_Extreme': {'SkyrimStormSnow': 1},
    'PIC_WTHR_SUMMER_A01_Clear': {'SkyrimClear': 1}, 'PIC_WTHR_SUMMER_A02_Clear_Aurora': {'SkyrimClear_A': 1},
    'PIC_WTHR_SUMMER_A03_Clear_Mist': {'SkyrimClear': 1}, 'PIC_WTHR_SUMMER_B01_Lightly_Cloudy': {'SkyrimClear': 1},
    'PIC_WTHR_SUMMER_B02_Lightly_Cloudy_Aurora': {'SkyrimClear_A': 0.7, 'SkyrimCloudy_A': 0.3}}

def family_mix(picta_edid):
    agg = {}
    for fam, d in pt['family_partner_summary'].items():
        for name, w in d.get(picta_edid, []):
            if name in BY_EDID: agg[name] = agg.get(name, 0.0) + w
    tot = sum(agg.values())
    return {k: v / tot for k, v in agg.items()} if tot > 0 else None

def donor_mix(picta_edid):
    if DONOR_MODE == 'family':
        m = family_mix(picta_edid)
        if m: return m
    return CANON_BY_PICTA[picta_edid]

FILE_WEATHER = {  # E11 file -> the Picta weather whose partners feed it (the non-aurora one where a file serves two)
    'Picta - Weathers/00_Master/A01_Clear.ini': '19FA01', 'Picta - Weathers/00_Master/A02_Clear_Mist.ini': '19FA03',
    'Picta - Weathers/00_Master/B01_Lightly_Cloudy.ini': '19FB01', 'Picta - Weathers/00_Master/B02_Lightly_Cloudy_Misty_Fog.ini': '19FB03',
    'Picta - Weathers/00_Master/C01_Cloudy.ini': '19FC01', 'Picta - Weathers/00_Master/C02_Cloudy_Stormy.ini': '19FC02',
    'Picta - Weathers/00_Master/C03_Cloudy_Light_Fog.ini': '19FC03', 'Picta - Weathers/00_Master/C04_Cloudy_Rain_Very_Light.ini': '19FC04',
    'Picta - Weathers/00_Master/C05_Cloudy_Snow_Very_Light.ini': '19FC05', 'Picta - Weathers/00_Master/D01_Overcast.ini': '19FD01',
    'Picta - Weathers/00_Master/D02_Overcast_Heavy_Fog.ini': '19FD02', 'Picta - Weathers/00_Master/D03_Overcast_Rain_Light.ini': '19FD03',
    'Picta - Weathers/00_Master/D04_Overcast_Rain_Medium.ini': '19FD04', 'Picta - Weathers/00_Master/D05_Overcast_Snow_Light.ini': '19FD05',
    'Picta - Weathers/00_Master/D06_Overcast_Snow_Medium.ini': '19FD06', 'Picta - Weathers/00_Master/E01_Storm_Thunder.ini': '19FE01',
    'Picta - Weathers/00_Master/E02_Storm_Cold_Thunder.ini': '19FE02', 'Picta - Weathers/00_Master/E03_Storm_Rain_Heavy_Thunder.ini': '19FE03',
    'Picta - Weathers/00_Master/E04_Storm_Rain_Extreme_Thunder.ini': '19FE04', 'Picta - Weathers/00_Master/E05_Storm_Snow_Heavy.ini': '19FE05',
    'Picta - Weathers/00_Master/E06_Storm_Snow_Extreme.ini': '19FE06',
    'Authoria - Summer/A01_Clear_Summer.ini': '5AFA01', 'Authoria - Summer/A02_Clear_Mist_Summer.ini': '5AFA03',
    'Authoria - Summer/B01_Lightly_Cloudy_Summer.ini': '5AFB01'}
WEATHERS = ['19FA01', '19FA02', '19FA03', '19FB01', '19FB02', '19FB03', '19FC01', '19FC02', '19FC03', '19FC04', '19FC05',
            '19FD01', '19FD02', '19FD03', '19FD04', '19FD05', '19FD06', '19FE01', '19FE02', '19FE03', '19FE04', '19FE05', '19FE06',
            '5AFA01', '5AFA02', '5AFA03', '5AFB01', '5AFB02']
def precol(fid): return pic[fid + ':Picta - Weathers of Aurbis.esm']

# ---------------------------------------------------------------------------------------------------------------- colour helpers
L = np.array([0.2126, 0.7152, 0.0722])
def Y(c): return float(np.dot(L, c))
def unit(c):
    c = np.asarray(c, float); y = Y(c)
    return c / y if y > 1e-9 else np.ones(3)
def desat(c, d):
    c = np.asarray(c, float); m = c.mean()
    return np.maximum(c + (m - c) * d, 0.0)
def hsv(c):
    c = np.asarray(c, float); mx = c.max()
    if mx <= 0: return (0.0, 0.0)
    h, s, v = colorsys.rgb_to_hsv(*(c / mx))
    return (h * 360.0, s)
def parse_rgb(s): return np.array([float(x) for x in s.split(',')])
def lerp(a, b, t): return a + (b - a) * t

def gamut_guard(old, target, hi=255.0):
    """keep target's luminance, pull its chroma back toward old's chroma until no channel exceeds hi"""
    target = np.asarray(target, float)
    if target.max() <= hi: return target
    yt = Y(target); uo = unit(old); ut = unit(target)
    lo_s, hi_s = 0.0, 1.0
    for _ in range(40):
        m = (lo_s + hi_s) / 2; c = yt * lerp(uo, ut, m)
        if c.max() <= hi: lo_s = m
        else: hi_s = m
    return yt * lerp(uo, ut, lo_s)

def donor_colour(mix, field, slot):
    acc = np.zeros(3); sw = 0.0
    for name, w in mix.items():
        rec = astr[BY_EDID[name]]
        if field == 'Clouds':
            lay = [l for l in rec.get('clouds', []) if str(l.get('enabled')) == 'True' and float(l['alphas'][slot]) > 0]
            if lay:
                c = sum(float(l['alphas'][slot]) * np.array(l['colors'][slot], float) for l in lay) / sum(float(l['alphas'][slot]) for l in lay)
            else:  # cloudless donor: use its horizon colour (what a thin cloud picks up) -- documented fallback
                c = np.array(rec['colors']['HorizonColor'][slot], float)
        elif field.startswith('DALC.'):
            c = np.array(rec['dalc'][slot][field[5:]], float)
        else:
            c = np.array(rec['colors'][field][slot], float)
        acc += w * unit(np.maximum(c, 0.5)); sw += w
    return acc / sw

# ---------------------------------------------------------------------------------------------------------------- clocks
def tod_weights(h, T=dict(DawnDuration=3.5, SunriseTime=9.0, DayTime=10.0, SunsetTime=17.0, DuskDuration=3.5, NightTime=20.5)):
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
    f = dict(Dawn=0.0, Sunrise=0.0, Day=0.0, Sunset=0.0, Dusk=0.0, Night=0.0)
    if cf == nf: f[cf] = 1.0
    else: f[cf] = min(max(1 - b, 0), 1); f[nf] = min(max(b, 0), 1)
    pd = min(max(f['Day'] ** 0.6, 0), 1)
    if pd > 1e-38:
        if f['Sunrise'] > 1e-38: f['Sunrise'] = min(max(1 - pd, 0), 1)
        if f['Sunset'] > 1e-38: f['Sunset'] = min(max(1 - pd, 0), 1)
    f['Day'] = pd
    return f
def clmt_weights(h, sr=(6.0, 9.0), ss=(17.0, 20.0)):
    """record slots on Picta's climate; ASSUMED engine rule: colour peaks at the window midpoint."""
    w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)
    a, b = sr; c, d = ss; ma = (a + b) / 2; mc = (c + d) / 2
    if h < a or h >= d: w['Night'] = 1.0
    elif h < ma: x = (h - a) / (ma - a); w['Night'] = 1 - x; w['Sunrise'] = x
    elif h < b: x = (h - ma) / (b - ma); w['Sunrise'] = 1 - x; w['Day'] = x
    elif h < c: w['Day'] = 1.0
    elif h < mc: x = (h - c) / (mc - c); w['Day'] = 1 - x; w['Sunset'] = x
    else: x = (h - mc) / (d - mc); w['Sunset'] = 1 - x; w['Night'] = x
    return w
HOURS = [5 + q * 0.25 for q in range(int((21.5 - 5) / 0.25) + 1)]
NIGHT_HOURS = [20.5 + q * 0.25 for q in range(int((24 + 5.5 - 20.5) / 0.25) + 1)]

# ---------------------------------------------------------------------------------------------------------------- ini io (read-only)
def parse_ini(path):
    txt = open(path, 'rb').read().decode('utf-8', errors='replace')
    sec = None; d = {}
    for line in txt.splitlines():
        s = line.strip()
        m = re.match(r'^\[(.+)\]$', s)
        if m: sec = m.group(1); d.setdefault(sec, {}); continue
        if '=' in s and sec and not s.startswith(';'):
            k, v = s.split('=', 1); d[sec][k.strip()] = v.strip()
    return d
def bf(ini, sec, key, h, default=0.0):
    w = tod_weights(h); acc = 0.0
    for p, x in w.items():
        if x > 0:
            v = ini.get(sec, {}).get(key + p); acc += x * (float(v) if v is not None else default)
    return acc
def brgb(ini, sec, key, h):
    w = tod_weights(h); acc = np.zeros(3)
    for p, x in w.items():
        if x > 0: acc += x * parse_rgb(ini[sec][key + p])
    return acc
def rec_at(rec, field, h):
    w = clmt_weights(h); return sum(x * np.array(rec[field][s], float) / 255.0 for s, x in w.items() if x > 0)
def dalc_at(rec, ax, h):
    w = clmt_weights(h); return sum(x * np.array(rec['DALC'][s][ax], float) / 255.0 for s, x in w.items() if x > 0)

# ---------------------------------------------------------------------------------------------------------------- per-channel luminance functionals
# Lh(ini, rec, h, F) = Y of the component when filter F is used, all other (unchanged) blended scalars at hour h.
def L_sky(field, ikey, ckey):
    def f(ini, rec, h, F):
        c = rec_at(rec, field, h) ** bf(ini, 'SKY', ckey, h, 1.0)
        x = c * F * bf(ini, 'SKY', ikey, h, 1.0) * bf(ini, 'SKY', 'GradientIntensity', h, 1.0)
        return Y(desat(x, bf(ini, 'SKY', 'GradientDesaturation', h)))
    return f
def L_clouds(ini, rec, h, F): return Y(np.full(3, 250 / 255.0) * F) * bf(ini, 'SKY', 'CloudsIntensity', h, 1.0)
def L_fog(ini, rec, h, F):
    c = rec_at(rec, 'FogFarColor', h) ** bf(ini, 'ENVIRONMENT', 'FogColorCurve', h, 1.0)
    return Y(lerp(c, 1.0, bf(ini, 'ENVIRONMENT', 'FogColorFilterAmount', h)) * F) * bf(ini, 'ENVIRONMENT', 'FogColorMultiplier', h, 1.0)
def L_volfog(ini, rec, h, F): return Y(F) * bf(ini, 'VOLUMETRICFOG', 'Intensity', h, 1.0)
def L_dl(ini, rec, h, F):
    c = desat(rec_at(rec, 'SunlightColor', h) ** bf(ini, 'ENVIRONMENT', 'DirectLightingCurve', h, 1.0), bf(ini, 'ENVIRONMENT', 'DirectLightingDesaturation', h))
    return Y(lerp(c, 1.0, bf(ini, 'ENVIRONMENT', 'DirectLightingColorFilterAmount', h)) * F) * bf(ini, 'ENVIRONMENT', 'DirectLightingIntensity', h, 1.0)
def L_sun(ini, rec, h, F): return Y(desat(rec_at(rec, 'SunColor', h), bf(ini, 'SKY', 'SunDesaturation', h)) * F)
def L_plain(ini, rec, h, F): return Y(F)

CHANNELS = [  # name, section, key, donor field, period map, multiplier, functional
    ('sky_top', 'SKY', 'GradientTopColorFilter', 'SkyUpperColor', SKY_MAP, 'sky', L_sky('SkyUpperColor', 'GradientTopIntensity', 'GradientTopCurve')),
    ('sky_horizon', 'SKY', 'GradientHorizonColorFilter', 'HorizonColor', SKY_MAP, 'sky', L_sky('HorizonColor', 'GradientHorizonIntensity', 'GradientHorizonCurve')),
    ('clouds', 'SKY', 'CloudsColorFilter', 'Clouds', SKY_MAP, 'clouds', L_clouds),
    ('fog', 'ENVIRONMENT', 'FogColorFilter', 'FogFarColor', SKY_MAP, 'fog', L_fog),
    ('volfog', 'VOLUMETRICFOG', 'ColorFilter', 'FogFarColor', SKY_MAP, 'volfog', L_volfog),
    ('light_dl', 'ENVIRONMENT', 'DirectLightingColorFilter', 'SunlightColor', LIGHT_MAP, 'light', L_dl),
]
TIES = {}   # god rays (GAMEVOLUMETRICRAYS ColorFilter) are solved separately below; Sun/Moon filters are NOT touched

RIDGE = 0.02   # luminance first, hue second: weight of 'stay on the hue target' rows vs every-hour luminance rows

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

ini_cache = {rel: parse_ini(DARK + '/' + rel) for rel in FILE_WEATHER}
plan = {}; donors_used = {}
for rel, fid in FILE_WEATHER.items():
    ini = ini_cache[rel]; rec = precol(fid)['colours']; edid = precol(fid)['editorid']
    mix = donor_mix(edid); donors_used[rel] = mix
    edits = []
    for (name, sec, key, field, pmap, mk, Lf) in CHANNELS:
        old = {p: parse_rgb(ini[sec][key + p]) for p in ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']}
        dirs = {}
        for per, (slot, ph) in pmap.items():
            t = STRENGTH * MULT[mk] * ph
            dirs[per] = lerp(unit(old[per]), donor_colour(mix, field, slot), t)
        sol, tgt = ridge_lock(ini, rec, Lf, old, dirs)
        for per in pmap:
            new = sol[per]
            edits.append(dict(channel=name, section=sec, key=key + per, old=[round(x, 4) for x in old[per]], new=[round(float(x), 4) for x in new],
                              t=round(STRENGTH * MULT[mk] * pmap[per][1], 4), donor_slot=pmap[per][0],
                              hue_target=[round(float(x), 4) for x in tgt[per]]))
            for (tsec, tkey) in TIES.get((sec, key), []):
                o2 = parse_rgb(ini[tsec][tkey + per])
                if np.allclose(o2, old[per], atol=0.006):
                    n2 = new
                else:  # keep any authored difference: same per-channel gain, then Y lock
                    g = np.where(old[per] > 1e-6, new / np.maximum(old[per], 1e-6), 1.0); n2 = o2 * g; n2 = n2 * (Y(o2) / max(Y(n2), 1e-9))
                edits.append(dict(channel=name + '_tie', section=tsec, key=tkey + per, old=[round(x, 4) for x in o2],
                                  new=[round(float(x), 4) for x in n2], t=None, donor_slot=pmap[per][0]))
    # god rays: colour = graded sunlight (E11 DL chain, no un-grade in 4ca678b) x GAMEVOLUMETRICRAYS ColorFilter
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
    A = []; bvec = []; GA = []; Gb = []; pers = list(LIGHT_MAP)
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
        new = np.clip(xg[3 * i:3 * i + 3], 0, 10)
        edits.append(dict(channel='godrays', section='GAMEVOLUMETRICRAYS', key='ColorFilter' + p, old=[round(x, 4) for x in oldg[p]],
                          new=[round(float(x), 4) for x in new], t=None, donor_slot=LIGHT_MAP[p][0]))
    plan[rel] = edits

# ---------------------------------------------------------------------------------------------------------------- records: DALC + SkyStaticsColor
AXES = ['DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus']
FILE_OF = {}
for rel, fid in FILE_WEATHER.items(): FILE_OF[fid] = rel
FILE_OF.update({'19FA02': 'Picta - Weathers/00_Master/A01_Clear.ini', '19FB02': 'Picta - Weathers/00_Master/B01_Lightly_Cloudy.ini',
                '5AFA02': 'Authoria - Summer/A01_Clear_Summer.ini', '5AFB02': 'Authoria - Summer/B01_Lightly_Cloudy_Summer.ini'})

def amb_Y(ini, h, c):
    return Y(desat(c, bf(ini, 'ENVIRONMENT', 'AmbientLightingDesaturation', h))) * bf(ini, 'ENVIRONMENT', 'AmbientLightingIntensity', h, 1.0)

rec_plan = {}
for fid in WEATHERS:
    p = precol(fid); ini = ini_cache[FILE_OF[fid]]; mix = donor_mix(p['editorid'])
    entry = dict(editorid=p['editorid'], winner=p['winner'], donor_mix=mix, DALC={s: {} for s in REC_SLOTS}, SkyStaticsColor={})
    t = STRENGTH * MULT['ambient']
    for ax in AXES:
        old = {s: np.array(p['colours']['DALC'][s][ax], float) for s in ['Sunrise', 'Day', 'Sunset', 'Night']}
        dirs = {s: lerp(unit(old[s]), donor_colour(mix, 'DALC.' + ax, s), t) for s in REC_SLOTS}
        # ridge LSQ over hours on the record clock (CLMT) with that hour's E11 ambient desat/intensity
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
            target = np.clip(gamut_guard(old[s], xs[3 * i:3 * i + 3], 254.4), 0, 255)
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
            entry['DALC'][s][ax] = dict(old=[int(x) for x in old[s]], new=[int(x) for x in best[1]])
    for s in REC_SLOTS:
        old = np.array(p['colours']['SkyStaticsColor'][s], float)
        tgt = lerp(unit(old), donor_colour(mix, 'SkyStaticsColor', s), STRENGTH * MULT['statics'])
        target = gamut_guard(old, tgt * (Y(old) / Y(tgt)), 254.4); base = np.round(target); best = None
        for dlt in itertools.product((-1, 0, 1), repeat=3):
            c = np.clip(base + np.array(dlt), 0, 255)
            err = abs(Y(c) - Y(target)) / max(Y(target), 1e-6) + 0.02 * np.abs(unit(c) - unit(target)).sum()
            if best is None or err < best[0]: best = (err, c)
        entry['SkyStaticsColor'][s] = dict(old=[int(x) for x in old], new=[int(x) for x in best[1]])
    rec_plan[fid] = entry

json.dump(dict(dials=dict(STRENGTH=STRENGTH, MULT=MULT, DONOR_MODE=DONOR_MODE, PH=PH, SKY_MAP=SKY_MAP, LIGHT_MAP=LIGHT_MAP),
               donors=donors_used, e11=plan), open(OUT + f'/e11_rehue_plan_s{STRENGTH:.2f}.json', 'w'), indent=1)
json.dump(dict(dials=dict(STRENGTH=STRENGTH, MULT=MULT, DONOR_MODE=DONOR_MODE), records=rec_plan),
          open(OUT + f'/records_plan_s{STRENGTH:.2f}.json', 'w'), indent=1)

# ---------------------------------------------------------------------------------------------------------------- VERIFICATION
def apply_plan(ini, edits):
    ni = copy.deepcopy(ini)
    for e in edits: ni[e['section']][e['key']] = ", ".join(repr(x) for x in e['new'])
    return ni
def baby_rec(fid):
    p = copy.deepcopy(precol(fid)['colours']); rp = rec_plan[fid]
    for s in REC_SLOTS:
        for ax in AXES: p['DALC'][s][ax] = rp['DALC'][s][ax]['new']
        p['SkyStaticsColor'][s] = rp['SkyStaticsColor'][s]['new']
    return p
def sun_dir(h):
    el = 55.0 * math.sin(math.pi * (h - 7.5) / 11.0) if 7.5 <= h <= 18.5 else -8.0
    az = math.pi * (h - 7.5) / 11.0; e = math.radians(el)
    return np.array([math.cos(e) * math.cos(az), math.cos(e) * math.sin(az), math.sin(e)])
def nrm(a): a = np.asarray(a, float); return a / np.linalg.norm(a)
def sat01(x): return min(max(x, 0.0), 1.0)
def sky_pixel(ini, rec, h, view):
    g = lambda k, d=0.0: bf(ini, 'SKY', k, h, d); s = lambda k, d=0.0: bf(ini, 'SKYSCATTERING', k, h, d)
    up = rec_at(rec, 'SkyUpperColor', h); hor = rec_at(rec, 'HorizonColor', h); GI = g('GradientIntensity', 1.0); gd = g('GradientDesaturation')
    top = desat(up ** g('GradientTopCurve', 1.0) * brgb(ini, 'SKY', 'GradientTopColorFilter', h) * g('GradientTopIntensity', 1.0) * GI, gd)
    hz = desat(hor ** g('GradientHorizonCurve', 1.0) * brgb(ini, 'SKY', 'GradientHorizonColorFilter', h) * g('GradientHorizonIntensity', 1.0) * GI, gd)
    z = view[2]; sky = lerp(top, hz, (1.0 - sat01(z)) ** g('ProceduralGradientWeightCurve', 1.75))
    sunc = desat(rec_at(rec, 'SunColor', h), g('SunDesaturation')) * brgb(ini, 'SKY', 'SunColorFilter', h)
    sunN = np.maximum(sunc, 0) / max(sunc.max(), 1.0)
    sd = nrm(sun_dir(h)); sunH = sd[2]; sunFade = math.sqrt(sat01(1.0 + 2.0 * sunH))
    col = (1.0 + (sunN - 1.0) * s('ColorFromSun')) * brgb(ini, 'SKYSCATTERING', 'ScatteringColor', h) * sunFade
    cpk = max(col.max(), 1e-6); dd = s('DustDensity'); dustTint = np.maximum(0.0, 1.0 - col / cpk) * 2 * dd ** 2
    dustVol = 0.02 / max(s('DustVolume', 0.25) ** 2, 1e-7); hR = 1.0 / max(s('HorizonRange', 1.0) ** 3, 1e-6)
    aT = 100.0 / max(s('AtmosphereThickness', 1.0) ** 2, 1e-6); agR = 1.0 / max(s('AirGlowRange', 1.0) ** 2, 1e-6)
    sgR = 10.0 / max(s('SunGlowRange', 1.0) ** 2, 1e-6); amount = s('Amount') ** 2
    facing = sat01(float(np.dot(view, sd)) * 0.5 + 0.5); away = 1.0 - facing
    elev = 1.0 - sat01(1.0 - z) * sat01(1.0 + sunH); dustBand = sat01(1.0 - elev * dustVol) ** 32
    aboveH = sat01(1.0 + z * 10.0) ** 2; sunAbove = sat01(1.0 + z * 40.0) ** 2
    spread = lerp(hR * away * away, aT, elev * elev)
    scat = col * s('Intensity') * np.clip(1.0 - dustBand * dustTint, 0, 1) ** 32 * aboveH * (1.0 - dustBand * s('DustDarkening'))
    res = sky * (1.0 + s('AirGlowIntensity') / (1.0 + away * agR)); wgt = sat01(amount / (1.0 + away * spread))
    res = lerp(res, scat, wgt) * (1.0 + s('SunGlowIntensity') * sunAbove / (1.0 + away * sgR))
    return lerp(sky, res, aboveH), top, hz, sunc
def components(ini, rec, h):
    sd = nrm(sun_dir(h)); az = np.array([sd[0], sd[1], 0.0]); az = az / (np.linalg.norm(az) or 1)
    views = {'zenith': np.array([0, 0, 1.0]), 'hor_sun': nrm([az[0], az[1], 0.05]), 'hor_away': nrm([-az[0], -az[1], 0.05]), 'mid_away': nrm([-az[0], -az[1], 0.44])}
    c = {}
    for vn, vd in views.items():
        px, top, hz, sunc = sky_pixel(ini, rec, h, vd); c['sky_' + vn] = px
    c['band_top'] = top; c['band_horizon'] = hz; c['sun_disc'] = sunc
    ff = rec_at(rec, 'FogFarColor', h) ** bf(ini, 'ENVIRONMENT', 'FogColorCurve', h, 1.0)
    c['fog_far'] = lerp(ff, 1.0, bf(ini, 'ENVIRONMENT', 'FogColorFilterAmount', h)) * brgb(ini, 'ENVIRONMENT', 'FogColorFilter', h) * bf(ini, 'ENVIRONMENT', 'FogColorMultiplier', h, 1.0)
    sl = desat(rec_at(rec, 'SunlightColor', h) ** bf(ini, 'ENVIRONMENT', 'DirectLightingCurve', h, 1.0), bf(ini, 'ENVIRONMENT', 'DirectLightingDesaturation', h))
    c['sunlight'] = sl * brgb(ini, 'ENVIRONMENT', 'DirectLightingColorFilter', h) * bf(ini, 'ENVIRONMENT', 'DirectLightingIntensity', h, 1.0)
    c['clouds'] = np.full(3, 250 / 255.0) * brgb(ini, 'SKY', 'CloudsColorFilter', h) * bf(ini, 'SKY', 'CloudsIntensity', h, 1.0)
    c['volfog'] = brgb(ini, 'VOLUMETRICFOG', 'ColorFilter', h) * bf(ini, 'VOLUMETRICFOG', 'Intensity', h, 1.0)
    c['godray_tint'] = brgb(ini, 'GAMEVOLUMETRICRAYS', 'ColorFilter', h) * c['sunlight']
    for ax in AXES:
        c['amb_' + ax[11:]] = desat(dalc_at(rec, ax, h), bf(ini, 'ENVIRONMENT', 'AmbientLightingDesaturation', h)) * bf(ini, 'ENVIRONMENT', 'AmbientLightingIntensity', h, 1.0)
    c['sky_statics'] = rec_at(rec, 'SkyStaticsColor', h)
    return c

lines = []
def P(s=''): lines.append(s)
def hs(c): h, s = hsv(c); return f"{h:5.1f}/{s:.2f}"
P("PICTA-SAFE baby numeric model v2 (pre-tonemap Bottled 4ca678b chain; 15-min steps 05:00-21:30 + night 20:30-05:30)")
P(f"dials: STRENGTH={STRENGTH} MULT={MULT} donors={DONOR_MODE}; Dawn/Dusk phase factor {PH:.3f}; luminance tolerance {LUMA_TOL*100:.1f}%")
CASES = [('A01 Clear', 'Picta - Weathers/00_Master/A01_Clear.ini', '19FA01'), ('A02 Clear Aurora', 'Picta - Weathers/00_Master/A01_Clear.ini', '19FA02'),
         ('SUMMER A01 Clear', 'Authoria - Summer/A01_Clear_Summer.ini', '5AFA01'), ('B03 Misty Fog', 'Picta - Weathers/00_Master/B02_Lightly_Cloudy_Misty_Fog.ini', '19FB03'),
         ('C01 Cloudy', 'Picta - Weathers/00_Master/C01_Cloudy.ini', '19FC01'), ('D02 Heavy Fog', 'Picta - Weathers/00_Master/D02_Overcast_Heavy_Fog.ini', '19FD02'),
         ('D03 Rain Light', 'Picta - Weathers/00_Master/D03_Overcast_Rain_Light.ini', '19FD03'), ('E03 Storm Rain', 'Picta - Weathers/00_Master/E03_Storm_Rain_Heavy_Thunder.ini', '19FE03'),
         ('E05 Storm Snow', 'Picta - Weathers/00_Master/E05_Storm_Snow_Heavy.ini', '19FE05')]
SHOW = [7.25, 8.0, 9.0, 12.0, 17.0, 18.0, 18.75]
summary = {}; global_worst = (0, None)
for label, rel, fid in CASES:
    iniP = ini_cache[rel]; iniB = apply_plan(iniP, plan[rel]); recP = precol(fid)['colours']; recB = baby_rec(fid)
    worst = {}; night_max = 0.0; rows = {}
    for h in HOURS:
        a = components(iniP, recP, h); b = components(iniB, recB, h)
        for cn in a:
            ya, yb = Y(a[cn]), Y(b[cn])
            if ya < 1e-7: continue
            r = yb / ya - 1.0
            if cn not in worst or abs(r) > abs(worst[cn][0]): worst[cn] = (r, h)
        if h in SHOW: rows[h] = (a, b)
    for h in NIGHT_HOURS:
        hh = h - 24 if h >= 24 else h
        a = components(iniP, recP, hh); b = components(iniB, recB, hh)
        for cn in a: night_max = max(night_max, float(np.abs(a[cn] - b[cn]).max()))
    P(); P(f"=== {label}   [{rel}]  record {fid}   donors: " + ", ".join(f"{k} {v:.2f}" for k, v in sorted(donor_mix(precol(fid)['editorid']).items(), key=lambda x: -x[1])[:4]))
    P("  luminance, worst hour of the day, baby vs Picta:  " + "  ".join(f"{cn} {r*100:+.2f}%@{h:g}" for cn, (r, h) in sorted(worst.items())))
    over = [cn for cn, (r, h) in worst.items() if abs(r) > LUMA_TOL]
    P(f"  -> max |dY/Y| = {max(abs(r) for r, h in worst.values())*100:.3f}%   over tolerance: {over if over else 'none'}   night 20:30-05:30 max abs channel diff = {night_max:.2e}")
    for cn, (r, h) in worst.items():
        if abs(r) > abs(global_worst[0]): global_worst = (r, (label, cn, h))
    summary[label] = {cn: round(r * 100, 3) for cn, (r, h) in worst.items()}
    P("  hue/sat (deg / HSV-sat)  Picta -> baby:")
    for h in SHOW:
        a, b = rows[h]
        P(f"   {h:5.2f}h " + " | ".join(f"{cn} {hs(a[cn])}->{hs(b[cn])}" for cn in ('sky_hor_away', 'sky_hor_sun', 'sky_zenith', 'fog_far', 'clouds', 'sunlight', 'amb_XPlus', 'amb_ZMinus', 'sky_statics')))
P(); P(f"GLOBAL worst luminance deviation: {global_worst[0]*100:+.3f}% at {global_worst[1]}")
json.dump(dict(strength=STRENGTH, worst_pct=summary, global_worst=[global_worst[0] * 100, global_worst[1]]), open(OUT + f'/model_summary_s{STRENGTH:.2f}.json', 'w'), indent=1)

# donor check: canonical vs family-weighted
P(); P("=== donor check (hue/sat of Astralite targets): canonical generic vs family-equal partner mix")
for edid in ('PIC_WTHR_MASTER_A01_Clear', 'PIC_WTHR_MASTER_C01_Cloudy', 'PIC_WTHR_MASTER_D02_Overcast_Heavy_Fog', 'PIC_WTHR_MASTER_D03_Overcast_Rain_Light', 'PIC_WTHR_MASTER_E03_Storm_Rain_Heavy_Thunder'):
    fm = family_mix(edid); cm = CANON_BY_PICTA[edid]
    for field, slot in (('HorizonColor', 'Sunrise'), ('FogFarColor', 'Sunrise'), ('SkyUpperColor', 'Day'), ('FogFarColor', 'Day'), ('DALC.DirectionalXPlus', 'Sunrise'), ('SunlightColor', 'Day')):
        P(f"  {edid[16:]:28s} {field:22s} {slot:7s} canonical {hs(donor_colour(cm, field, slot))}   family {hs(donor_colour(fm, field, slot))}")
open(OUT + f'/model_report_s{STRENGTH:.2f}.txt', 'w').write("\n".join(lines))
print("\n".join(lines))
