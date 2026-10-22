"""FAITHFUL ASTRALITE baby - design solver + numeric proof (v2).

Route A: hue lives in the RECORDS (as in Astralite). Picta's per-weather E11 colour filters are re-solved
(least squares over 05:00-21:00) so that on screen: luminance == Picta's (Rec.709, the user's brightness lock)
and chromaticity == Astralite's authored chromaticity at strength KAPPA (house transform c' = L + (c-L)*k).
Night slot + Night/Interior periods reproduce Picta exactly (records x m, filters / m).

v1 (v1_vector_mix/) mixed Picta and Astralite chromaticities 85/15 and produced magenta/grey intermediates
where the two hues oppose (red Picta dawn light vs blue-grey Astralite fog light): rejected; the dial is now
an AMPLITUDE dial on Astralite's chroma (complies with the colour-strength-not-tone rule).

Read-only inputs; scratch outputs only (this folder).
"""
import json, math, os, colorsys, copy, sys
import numpy as np

SCR = 'C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby'
OUT = SCR + '/design/faithful'
LIVE_MOD = 'C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1'
LIVE = LIVE_MOD + '/enbseries'

DIALS = dict(
    KAPPA_SKY=1.0,      # Astralite chroma strength: sky top/horizon/lower, clouds, sun disc + scattering
    KAPPA_FOG=1.0,      # fog near/far colour
    KAPPA_LIGHT=1.0,    # sunlight colour
    KAPPA_AMB=1.0,      # DALC ambient (6 axes)
    KAPPA_FX=1.0,       # EffectLighting + SkyStatics (mist meshes, MoT/Picta fog statics); gamut-limited
    IMGS_NEUTRAL=1.0,   # Sunrise/Day/Sunset IMGS tint colour -> equal-luma grey (amount kept)
    VL_STRENGTH=1.0,    # transplanted VOLI effective intensity relative to the Astralite lane
    FOG_DENSITY=0.5,    # log-space step of the effective fog FAR distance toward Astralite (add-only)
    LUMA_WEIGHT=20.0,    # LS weight of the luminance rows vs chroma rows
    REFIT_RECORDS=1.0,  # alternate record/filter least squares (1) or records fixed at slot targets (0)
    DL_DESAT_ZERO=1.0,
    SOLVER=1.0,         # 1 = strict Route A: grey daylight filters, record chroma fixed at the slot targets, LUMA-ONLY scalar LS (records x filters);
                        # 0 = free LS on full colour (v2b; produced green dawn light in fog/rain - kept for comparison only)
    LIGHT_FREE_FILTERS=1.0,  # sun + sunlight, weathers whose Astralite dawn light is warm: refit the Dawn/Dusk filters per RGB (records fixed) so the moonlit Night record does not turn pre-dawn light blue
    GREY_REG=1.0,       # ridge pulling each daylight filter toward grey (hue belongs in the records)  # 1 = set DirectLightingDesaturation 0 for the daylight periods; 0 = keep Picta's (-0.5 / 1.0)
)
QUICK = False
for a in sys.argv[1:]:
    if a == 'quick': QUICK = True; continue
    k, v = a.split('='); DIALS[k] = float(v)

PER = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night', 'InteriorDay', 'InteriorNight']
DAYP = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk']
SLOTS = ['Sunrise', 'Day', 'Sunset', 'Night']
CHG = ['Sunrise', 'Day', 'Sunset']
AXES = ['DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus']

# ---------------- colour helpers ----------------
def L(c): return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
def mean3(c): return (c[0]+c[1]+c[2])/3.0
def mul(a, b): return [x*y for x, y in zip(a, b)]
def sc(a, s): return [x*s for x in a]
def add(a, b): return [x+y for x, y in zip(a, b)]
def lerp(a, b, t):
    if isinstance(a, list): return [x+(y-x)*t for x, y in zip(a, b)]
    return a+(b-a)*t
def sat01(x): return max(0.0, min(1.0, x))
def curve(c, p): return [max(x, 0.0)**p for x in c]
def desat(c, d):
    m = mean3(c); return [max(lerp(x, m, d), 0.0) for x in c]
def inv_desat(t, d):
    if abs(1-d) < 1e-6 or d == 0: return list(t)
    m = mean3(t); return [max((x - d*m)/(1-d), 0.0) for x in t]
def cfilter(c, f, amt): return mul([lerp(x, 1.0, amt) for x in c], f)
def norm(c):
    l = L(c); return [x/l for x in c] if l > 1e-9 else [1.0, 1.0, 1.0]
def strength(chat, k):
    """house transform on a luma-normalised chromaticity: 1 + (c-1)*k"""
    return [1.0 + (x-1.0)*k for x in chat]
def hsv(c):
    mx = max(c)
    if mx <= 1e-12: return (0.0, 0.0)
    h, s, v = colorsys.rgb_to_hsv(*[max(x, 0)/mx for x in c]); return (h*360.0, s)
def hue_s(c):
    h, s = hsv(c); return f"h{h:5.1f} s{s:.2f}"
def cdist(a, b):
    """distance between two colours' luma-normalised chromaticities (0 = same hue+saturation)"""
    na, nb = norm(a), norm(b); return math.sqrt(sum((x-y)**2 for x, y in zip(na, nb)))
def rgb01(s): return [float(x)/255.0 for x in str(s).split(',')[:3]]
def to255(c): return [int(round(max(0.0, min(1.0, x))*255)) for x in c]
def q255(c): return [x/255.0 for x in to255(c)]
def gamut_chroma(Lt, chat):
    c = sc(chat, Lt)
    if max(c) <= 1.0 and min(c) >= 0: return c
    k = (1.0 - Lt)/(max(c) - Lt) if max(c) > Lt else 0.0
    return [Lt + (x-Lt)*k for x in c]

# ---------------- ini ----------------
def read_ini(path):
    secs, cur = {}, None
    with open(path, encoding='latin-1') as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line[0] in ';#': continue
            if line.startswith('['):
                cur = line[1:line.index(']')].strip().upper(); secs.setdefault(cur, {}); continue
            if cur is None or '=' not in line: continue
            k, v = line.split('=', 1); k = k.strip().lower(); v = v.split(';')[0].strip()
            if k not in secs[cur]: secs[cur][k] = v
    return secs
def pval(v):
    if v is None: return None
    if ',' in v: return [float(x) for x in v.split(',')[:3]]
    if v.lower() in ('true', 'false'): return 1.0 if v.lower() == 'true' else 0.0
    return float(v)
BASE = read_ini(LIVE_MOD + '/enbseries.ini')
def ini_get(wf, sec, key, per):
    for src in (wf, BASE):
        if src is None: continue
        s = src.get(sec.upper(), {})
        if (key+per).lower() in s: return pval(s[(key+per).lower()])
        if key.lower() in s: return pval(s[key.lower()])
    return None
KEYS = {
 'SKY': ['GradientIntensity', 'GradientDesaturation', 'GradientTopIntensity', 'GradientTopCurve', 'GradientTopColorFilter',
         'GradientMiddleColorFilter', 'GradientHorizonIntensity', 'GradientHorizonCurve', 'GradientHorizonColorFilter',
         'ProceduralGradientWeightCurve', 'CloudsIntensity', 'CloudsCurve', 'CloudsDesaturation', 'CloudsColorFilter',
         'SunDesaturation', 'SunColorFilter', 'MoonColorFilter'],
 'SKYSCATTERING': ['Intensity', 'Amount', 'ColorFromSun', 'ScatteringColor', 'AirGlowIntensity', 'AirGlowRange', 'SunGlowIntensity',
                   'SunGlowRange', 'HorizonRange', 'AtmosphereThickness', 'DustVolume', 'DustDensity', 'DustDarkening', 'ShadowAmount'],
 'ENVIRONMENT': ['DirectLightingIntensity', 'DirectLightingCurve', 'DirectLightingDesaturation', 'DirectLightingColorFilter',
                 'DirectLightingColorFilterAmount', 'AmbientLightingIntensity', 'AmbientLightingDesaturation', 'FogColorMultiplier',
                 'FogColorCurve', 'FogColorFilter', 'FogColorFilterAmount', 'FogAmountMultiplier', 'FogCurveMultiplier'],
 'GAMEVOLUMETRICRAYS': ['Intensity', 'ColorFilter', 'Desaturation', 'RangeFactor'],
 'VOLUMETRICFOG': ['ColorFilter', 'Opacity'],
}
def load_e11(path):
    wf = read_ini(path) if path else None
    return {sec+'.'+k: {p: ini_get(wf, sec, k, p) for p in PER} for sec, ks in KEYS.items() for k in ks}
SOUL = json.load(open(SCR + '/map/astralite-colour/soulcore_e11_colour_keys.json'))
def load_soul(fname):
    wfv = SOUL['weather_files'].get(fname, {}).get('values', {})
    d = {}
    for sec, ks in KEYS.items():
        for k in ks:
            key = sec+'.'+k; src = wfv.get(key) or SOUL['base_values'].get(key); row = {}
            for p in PER:
                v = None
                if src is not None:
                    if p in src: v = src[p]
                    elif 'value' in src: v = pval(str(src['value']))
                row[p] = v
            d[key] = row
    return d

# ---------------- clocks ----------------
def tod_weights(h, T):
    night, sunrise, dawnD, day, sunset, duskD = T['NightTime'], T['SunriseTime'], T['DawnDuration'], T['DayTime'], T['SunsetTime'], T['DuskDuration']
    tp = [night, sunrise-dawnD, sunrise-dawnD*0.5, sunrise, day, sunset, sunset+duskD*0.5, sunset+duskD]
    tp = tp + [x+24 for x in tp]
    fmap = ['Night', 'Night', 'Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
    ci = ni = 0; cpt = 0.0; npt = 24.0
    for i, t in enumerate(tp):
        if h >= t and t >= cpt: ci, cpt = i, t
        if t > h and npt >= t: ni, npt = i, t
    cf, nf = fmap[ci % 8], fmap[ni % 8]
    td = abs(npt-cpt) or 1.0; b = abs(h-cpt)/td
    f = dict(Dawn=0.0, Sunrise=0.0, Day=0.0, Sunset=0.0, Dusk=0.0, Night=0.0)
    if cf == nf: f[cf] = 1.0
    else: f[cf] = sat01(1-b); f[nf] = sat01(b)
    pd = sat01(f['Day']**0.6)
    if pd > 1e-30:
        if f['Sunrise'] > 1e-30: f['Sunrise'] = sat01(1-pd)
        if f['Sunset'] > 1e-30: f['Sunset'] = sat01(1-pd)
    f['Day'] = pd
    return f
TOD_P = dict(DawnDuration=3.5, SunriseTime=9.0, DayTime=10.0, SunsetTime=17.0, DuskDuration=3.5, NightTime=20.5)
TOD_A = dict(DawnDuration=3.5, SunriseTime=8.0, DayTime=13.0, SunsetTime=18.0, DuskDuration=3.5, NightTime=1.0)
CLMT_P = (6.0, 9.0, 17.0, 20.0)
CLMT_A = (4.5, 9.5, 16.5, 21.5)
def clmt_w(t, C):
    b, e, sb, se = C; m1 = (b+e)/2; m2 = (sb+se)/2
    w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)
    if t < b or t >= se: w['Night'] = 1
    elif t < m1: f = (t-b)/(m1-b); w['Night'] = 1-f; w['Sunrise'] = f
    elif t < e: f = (t-m1)/(e-m1); w['Sunrise'] = 1-f; w['Day'] = f
    elif t < sb: w['Day'] = 1
    elif t < m2: f = (t-sb)/(m2-sb); w['Day'] = 1-f; w['Sunset'] = f
    else: f = (t-m2)/(se-m2); w['Sunset'] = 1-f; w['Night'] = f
    return w
PH = [(0, 0), (6.0, 4.5), (7.5, 7.0), (9.0, 9.5), (17.0, 16.5), (18.5, 19.0), (20.0, 21.5), (24, 24)]
def phase_map(t):
    for (a, a2), (b, b2) in zip(PH, PH[1:]):
        if a <= t <= b: return a2 + (t-a)/(b-a)*(b2-a2)
    return t
SLOT_PEAK = dict(Sunrise=7.5, Day=10.0, Sunset=18.5, Night=22.0)
GRID = [q/4.0 for q in range(20, 85)]           # 05:00 .. 21:00, 15 min

def ini_at(E, key, w):
    acc = None
    for p, wt in w.items():
        if wt <= 0: continue
        v = E[key][p]
        if v is None: continue
        if isinstance(v, list): acc = sc(v, wt) if acc is None else add(acc, sc(v, wt))
        else: acc = v*wt if acc is None else acc + v*wt
    return acc
def rec_at(Rf, w):
    acc = [0.0, 0.0, 0.0]
    for s, wt in w.items():
        if wt > 0: acc = add(acc, sc(Rf[s], wt))
    return acc

# ---------------- channel chains (Effects11.cpp 557-780 @4ca678b) ----------------
FIELD = {'top': 'SkyUpperColor', 'hor': 'HorizonColor', 'clouds': 'CloudMain', 'fogfar': 'FogFarColor', 'fognear': 'FogNearColor',
         'sunlight': 'SunlightColor', 'sun': 'SunColor', 'sunraw': 'SunColor'}
FKEY = {'top': 'SKY.GradientTopColorFilter', 'hor': 'SKY.GradientHorizonColorFilter', 'clouds': 'SKY.CloudsColorFilter',
        'fogfar': 'ENVIRONMENT.FogColorFilter', 'fognear': 'ENVIRONMENT.FogColorFilter', 'sunlight': 'ENVIRONMENT.DirectLightingColorFilter',
        'sun': 'SKY.SunColorFilter', 'sunraw': 'SKY.SunColorFilter'}
def chain(ch, x, E, we):
    """x = record colour already interpolated on the CLMT clock; E11 values blended with we"""
    g = lambda k: ini_at(E, k, we)
    if ch in ('top', 'hor'):
        b = 'GradientTop' if ch == 'top' else 'GradientHorizon'
        c = sc(mul(curve(x, g('SKY.'+b+'Curve')), g('SKY.'+b+'ColorFilter')), g('SKY.'+b+'Intensity')*g('SKY.GradientIntensity'))
        return desat(c, g('SKY.GradientDesaturation'))
    if ch == 'clouds':
        c = desat(curve(x, g('SKY.CloudsCurve')), g('SKY.CloudsDesaturation'))
        return mul(sc(c, g('SKY.CloudsIntensity')), g('SKY.CloudsColorFilter'))
    if ch in ('fogfar', 'fognear'):
        c = cfilter(curve(x, g('ENVIRONMENT.FogColorCurve')), g('ENVIRONMENT.FogColorFilter'), g('ENVIRONMENT.FogColorFilterAmount'))
        return sc(c, g('ENVIRONMENT.FogColorMultiplier'))
    if ch == 'sunlight':
        c = desat(curve(x, g('ENVIRONMENT.DirectLightingCurve')), g('ENVIRONMENT.DirectLightingDesaturation'))
        c = cfilter(c, g('ENVIRONMENT.DirectLightingColorFilter'), g('ENVIRONMENT.DirectLightingColorFilterAmount'))
        return sc(c, g('ENVIRONMENT.DirectLightingIntensity'))
    if ch in ('sun', 'sunraw'):
        c = cfilter(desat(x, g('SKY.SunDesaturation')), g('SKY.SunColorFilter'), 0.0)
        if ch == 'sunraw': return c
        pk = max(max(c), 1.0); return [max(v, 0)/pk for v in c]
    if ch == 'scat':     # scattering colour S at the sun (sunN * ScatteringColor), ColorFromSun = 1 in every Picta file
        c = cfilter(desat(x, g('SKY.SunDesaturation')), g('SKY.SunColorFilter'), 0.0)
        pk = max(max(c), 1.0); c = [max(v, 0)/pk for v in c]
        cfs = g('SKYSCATTERING.ColorFromSun')
        return [(1.0+(s-1.0)*cfs)*k for s, k in zip(c, g('SKYSCATTERING.ScatteringColor'))]
    if ch.startswith('DALC.'):
        return sc(desat(x, g('ENVIRONMENT.AmbientLightingDesaturation')), g('ENVIRONMENT.AmbientLightingIntensity'))
    return x
def field_of(ch):
    if ch.startswith('DALC.'): return ch
    if ch == 'scat': return 'SunColor'
    return FIELD.get(ch, ch)
def lane(ch, R, E, t, clmt, tod):
    return chain(ch, rec_at(R[field_of(ch)], clmt_w(t, clmt)), E, tod_weights(t, tod))

# ---------------- records ----------------
def load_picta_records():
    rows = [json.loads(l) for l in open(SCR + '/map/picta-colour/wthr_winners_everything.jsonl')][1:]
    out = {}
    for r in rows:
        fid = r['formid'].split(':')[0]
        if fid[:3] not in ('19F', '5AF'): continue
        F = {f['path']: f.get('value', f.get('note')) for f in r['fields']}
        R = {'_edid': r['editorid'], '_winner': r['winner']}
        for fld in ('SkyUpperColor', 'SkyLowerColor', 'HorizonColor', 'FogNearColor', 'FogFarColor', 'SunlightColor', 'SunColor',
                    'EffectLightingColor', 'SkyStaticsColor', 'AmbientColor'):
            R[fld] = {s: rgb01(F[fld+'.'+s]) for s in SLOTS}
        for ax in AXES:
            R['DALC.'+ax] = {s: rgb01(F[f'DirectionalAmbientLightingColors.{s}.{ax}']) for s in SLOTS}
        layers = []
        for i in range(32):
            if F.get(f'Clouds[{i}].Enabled') == 'True' and F.get(f'CloudTextures[{i}]', '(absent)') != '(absent)':
                layers.append({'i': i, 'tex': F.get(f'CloudTextures[{i}]'), 'col': {s: rgb01(F[f'Clouds[{i}].Colors.{s}']) for s in SLOTS}})
        R['_layers'] = layers
        main = [l for l in layers if 'Cloud_Panorama' in (l['tex'] or '')] or layers
        R['CloudMain'] = {s: list(main[0]['col'][s]) for s in SLOTS}
        R['_fog'] = {k: float(F[k]) for k in ('FogDistanceDayNear', 'FogDistanceDayFar', 'FogDistanceDayPower', 'FogDistanceDayMax',
                                              'FogDistanceNightNear', 'FogDistanceNightFar', 'FogDistanceNightPower', 'FogDistanceNightMax')}
        R['_voli'] = {s: F.get('VolumetricLighting.'+s) for s in SLOTS}
        R['_imgs'] = {s: F.get('ImageSpaces.'+s) for s in SLOTS}
        R['_ve'] = F.get('VisualEffect')
        out[fid] = R
    return out
AST = json.load(open(SCR + '/map/astralite-colour/astralite_rotating_weathers_colour.json'))
def load_astra(key):
    a = AST[key]; R = {'_edid': a['editorid'], '_soul': a.get('e11_weather_file')}
    for fld, v in a['colors'].items(): R[fld] = {s: [x/255.0 for x in v[s]] for s in SLOTS}
    for s in SLOTS:
        for ax, v in a['dalc'][s].items():
            if ax.startswith('Directional'): R.setdefault('DALC.'+ax, {})[s] = [x/255.0 for x in v]
    en = [c for c in a['clouds'] if c.get('enabled') == 'True']
    R['CloudMain'] = {}
    for s in SLOTS:
        cols = [[x/255.0 for x in c['colors'][s]] for c in en if sum(c['colors'][s]) > 0]
        R['CloudMain'][s] = [sum(c[i] for c in cols)/len(cols) for i in range(3)] if cols else [1, 1, 1]
    R['_fog'] = a['fog_distance']; R['_voli'] = a.get('volumetric_resolved'); R['_ve'] = a.get('visual_effect')
    return R

PARTNER = {
 '19FA01': '00081A:Skyrim.esm', '19FA03': '00081A:Skyrim.esm', '19FB01': '00081A:Skyrim.esm',
 '5AFA01': '00081A:Skyrim.esm', '5AFA03': '00081A:Skyrim.esm', '5AFB01': '00081A:Skyrim.esm',
 '19FA02': '10E1F2:Skyrim.esm', '19FB02': '10E1F2:Skyrim.esm', '5AFA02': '10E1F2:Skyrim.esm', '5AFB02': '10E1F2:Skyrim.esm',
 '19FB03': '0C821E:Skyrim.esm', '19FC03': '0C821E:Skyrim.esm', '19FD02': '0C821E:Skyrim.esm',
 '19FC01': '012F89:Skyrim.esm', '19FC02': '012F89:Skyrim.esm', '19FD01': '012F89:Skyrim.esm',
 '19FC04': '0C821F:Skyrim.esm', '19FD03': '0C821F:Skyrim.esm', '19FD04': '0C821F:Skyrim.esm',
 '19FE01': '0C8220:Skyrim.esm', '19FE03': '0C8220:Skyrim.esm', '19FE04': '0C8220:Skyrim.esm',
 '19FC05': '04D7FB:Skyrim.esm', '19FD05': '04D7FB:Skyrim.esm', '19FD06': '04D7FB:Skyrim.esm',
 '19FE02': '0C8221:Skyrim.esm', '19FE05': '0C8221:Skyrim.esm', '19FE06': '0C8221:Skyrim.esm',
}
FILES = {
 'Picta - Weathers/00_Master/A01_Clear.ini': ['19FA01', '19FA02'],
 'Picta - Weathers/00_Master/A02_Clear_Mist.ini': ['19FA03'],
 'Picta - Weathers/00_Master/B01_Lightly_Cloudy.ini': ['19FB01', '19FB02'],
 'Picta - Weathers/00_Master/B02_Lightly_Cloudy_Misty_Fog.ini': ['19FB03'],
 'Picta - Weathers/00_Master/C01_Cloudy.ini': ['19FC01'],
 'Picta - Weathers/00_Master/C02_Cloudy_Stormy.ini': ['19FC02'],
 'Picta - Weathers/00_Master/C03_Cloudy_Light_Fog.ini': ['19FC03'],
 'Picta - Weathers/00_Master/C04_Cloudy_Rain_Very_Light.ini': ['19FC04'],
 'Picta - Weathers/00_Master/C05_Cloudy_Snow_Very_Light.ini': ['19FC05'],
 'Picta - Weathers/00_Master/D01_Overcast.ini': ['19FD01'],
 'Picta - Weathers/00_Master/D02_Overcast_Heavy_Fog.ini': ['19FD02'],
 'Picta - Weathers/00_Master/D03_Overcast_Rain_Light.ini': ['19FD03'],
 'Picta - Weathers/00_Master/D04_Overcast_Rain_Medium.ini': ['19FD04'],
 'Picta - Weathers/00_Master/D05_Overcast_Snow_Light.ini': ['19FD05'],
 'Picta - Weathers/00_Master/D06_Overcast_Snow_Medium.ini': ['19FD06'],
 'Picta - Weathers/00_Master/E01_Storm_Thunder.ini': ['19FE01'],
 'Picta - Weathers/00_Master/E02_Storm_Cold_Thunder.ini': ['19FE02'],
 'Picta - Weathers/00_Master/E03_Storm_Rain_Heavy_Thunder.ini': ['19FE03'],
 'Picta - Weathers/00_Master/E04_Storm_Rain_Extreme_Thunder.ini': ['19FE04'],
 'Picta - Weathers/00_Master/E05_Storm_Snow_Heavy.ini': ['19FE05'],
 'Picta - Weathers/00_Master/E06_Storm_Snow_Extreme.ini': ['19FE06'],
 'Authoria - Summer/A01_Clear_Summer.ini': ['5AFA01', '5AFA02'],
 'Authoria - Summer/A02_Clear_Mist_Summer.ini': ['5AFA03'],
 'Authoria - Summer/B01_Lightly_Cloudy_Summer.ini': ['5AFB01', '5AFB02'],
}
if QUICK: FILES = {k: v for k, v in FILES.items() if any(x in k for x in ('A01_Clear.ini', 'C01_', 'D02_', 'D03_'))}
FILE_OF = {w: f for f, ws in FILES.items() for w in ws}
SHARE = {r['formid'].split(':')[0]: r['rolls']['region_month_share_sum']
         for r in json.load(open(SCR + '/map/pairing/pairing_table.json'))['picta_rotation']}

PIC_ALL = load_picta_records()
PIC = {k: v for k, v in PIC_ALL.items() if k in FILE_OF}
E_P = {f: load_e11(LIVE + '/' + f) for f in FILES}
AREC = {k: load_astra(k) for k in set(PARTNER[w] for w in PIC)}
E_S = {k: load_soul(AREC[k]['_soul']) for k in AREC}

def P_out(ch, fid, t): return lane(ch, PIC[fid], E_P[FILE_OF[fid]], t, CLMT_P, TOD_P)
def A_out(ch, fid, t): return lane(ch, AREC[PARTNER[fid]], E_S[PARTNER[fid]], phase_map(t), CLMT_A, TOD_A)
KAPPA = {'top': 'KAPPA_SKY', 'hor': 'KAPPA_SKY', 'clouds': 'KAPPA_SKY', 'sun': 'KAPPA_SKY', 'sunraw': 'KAPPA_SKY', 'scat': 'KAPPA_SKY',
         'fogfar': 'KAPPA_FOG', 'fognear': 'KAPPA_FOG', 'sunlight': 'KAPPA_LIGHT'}
def kappa(ch): return DIALS[KAPPA.get(ch, 'KAPPA_AMB')]
def target(ch, fid, t):
    """on-screen target: Picta luma x Astralite chroma (phase-mapped clock) at strength kappa.
    Returns (target, picta_now, chroma_weight); the chroma weight fades with the share of Picta's Night record slot."""
    p = P_out(ch, fid, t); a = A_out(ch, fid, t)
    tau = 1.0 - clmt_w(t, CLMT_P)['Night']
    ah = strength(norm(a), kappa(ch)) if L(a) > 1e-9 else norm(p)
    return sc(ah, L(p)), p, tau

# ---------------- solver ----------------
CKEY = {'top': 'SKY.GradientTopCurve', 'hor': 'SKY.GradientHorizonCurve', 'clouds': 'SKY.CloudsCurve', 'fog': 'ENVIRONMENT.FogColorCurve',
        'sunlight': 'ENVIRONMENT.DirectLightingCurve', 'sun': None}
FCH = {'top': ['top'], 'hor': ['hor'], 'clouds': ['clouds'], 'fog': ['fogfar', 'fognear'], 'sunlight': ['sunlight'], 'sun': ['sunraw']}
FOG_W = {'fogfar': 1.0, 'fognear': 0.25}

def lstsq_filters(f, grp, B_REC, B_E, periods=None):
    """least squares for the 5 daylight filters (x3 channels) of one E11 file + channel group; Night/Interior fixed"""
    fk = FKEY[FCH[grp][0]]
    rows, rhs = [], []
    for fid in FILES[f]:
        sw = math.sqrt(SHARE.get(fid, 1.0))
        for ch in FCH[grp]:
            cw = FOG_W.get(ch, 1.0)
            for t in GRID:
                tgt, p, tau = target(ch, fid, t)
                lp = L(p)
                if lp < 1e-7: continue
                x = rec_at(B_REC[fid][field_of(ch)], clmt_w(t, CLMT_P)); we = tod_weights(t, TOD_P)
                PP = periods or DAYP
                save = {pp: B_E[f][fk][pp] for pp in PP}
                for pp in PP: B_E[f][fk][pp] = [0.0, 0.0, 0.0]
                c0 = chain(ch, x, B_E[f], we)
                cols = []
                for pp in PP:
                    for c in range(3):
                        e = [0.0, 0.0, 0.0]; e[c] = 1.0; B_E[f][fk][pp] = e
                        v = chain(ch, x, B_E[f], we); cols.append([vi - ci for vi, ci in zip(v, c0)])
                        B_E[f][fk][pp] = [0.0, 0.0, 0.0]
                for pp in PP: B_E[f][fk][pp] = save[pp]
                s = sw*cw/lp
                for c in range(3):
                    rows.append([col[c]*s*tau for col in cols]); rhs.append((tgt[c]-c0[c])*s*tau)
                lw = DIALS['LUMA_WEIGHT']
                rows.append([L(col)*s*lw for col in cols]); rhs.append((L(tgt)-L(c0))*s*lw)
    PP = periods or DAYP; NU = 3*len(PP)
    nsamp = max(1, len(rows)//4)
    lam = DIALS['GREY_REG']*math.sqrt(nsamp)
    for k in range(len(PP)):
        for c in range(3):
            r = [0.0]*NU
            for cc in range(3): r[k*3+cc] = -lam/3.0
            r[k*3+c] += lam
            rows.append(r); rhs.append(0.0)
    A = np.array(rows); b = np.array(rhs)
    free = list(range(NU)); x = np.zeros(NU)
    for _ in range(8):
        fixed = [i for i in range(NU) if i not in free]
        rhs_eff = b - A[:, fixed] @ x[fixed] if fixed else b
        sol, *_ = np.linalg.lstsq(A[:, free], rhs_eff, rcond=None)
        x[free] = sol
        bad = [i for i in free if x[i] < 0 or x[i] > 10]
        if not bad: break
        for i in bad: x[i] = min(10.0, max(0.0, x[i])); free.remove(i)
    for k, pp in enumerate(PP): B_E[f][fk][pp] = [float(x[k*3+c]) for c in range(3)]

def lstsq_records(f, grp, B_REC, B_E, m):
    """least squares for the Sunrise/Day/Sunset record colours of each weather (Night fixed), then byte-clip"""
    for fid in FILES[f]:
        for ch in FCH[grp]:
            fld = field_of(ch)
            rows, rhs = [], []
            for t in GRID:
                tgt, p, tau = target(ch, fid, t); lp = L(p)
                if lp < 1e-7: continue
                wr = clmt_w(t, CLMT_P); we = tod_weights(t, TOD_P)
                if wr['Night'] >= 0.999: continue
                saveR = {s: B_REC[fid][fld][s] for s in CHG}
                for s in CHG: B_REC[fid][fld][s] = [0.0, 0.0, 0.0]
                c0 = chain(ch, rec_at(B_REC[fid][fld], wr), B_E[f], we)
                cols = []
                for s in CHG:
                    for c in range(3):
                        e = [0.0, 0.0, 0.0]; e[c] = 1.0; B_REC[fid][fld][s] = e
                        v = chain(ch, rec_at(B_REC[fid][fld], wr), B_E[f], we); cols.append([vi-ci for vi, ci in zip(v, c0)])
                        B_REC[fid][fld][s] = [0.0, 0.0, 0.0]
                for s in CHG: B_REC[fid][fld][s] = saveR[s]
                for c in range(3):
                    rows.append([col[c]/lp*tau for col in cols]); rhs.append((tgt[c]-c0[c])/lp*tau)
                lw = DIALS['LUMA_WEIGHT']
                rows.append([L(col)/lp*lw for col in cols]); rhs.append((L(tgt)-L(c0))/lp*lw)
            sol, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
            for k, s in enumerate(CHG):
                v = [float(sol[k*3+c]) for c in range(3)]
                v = [min(1.0, max(0.0, x)) for x in v]
                B_REC[fid][fld][s] = q255(v)

def lum_rows_scalar(f, grp, B_REC, B_E, which, lvals, kvals):
    """luma-only design rows. which='k': columns = grey daylight filter scalars; which='l': columns = record slot luma scalars"""
    chs = FCH[grp]; fk = FKEY[chs[0]]
    rows, rhs = [], []
    for fid in FILES[f]:
        sw = math.sqrt(SHARE.get(fid, 1.0))
        for ch in chs:
            cw = FOG_W.get(ch, 1.0); fld = field_of(ch)
            for t in GRID:
                p = P_out(ch, fid, t); lp = L(p)
                if lp < 1e-7: continue
                wr = clmt_w(t, CLMT_P); we = tod_weights(t, TOD_P)
                def outL(recs, ks):
                    for k, pp in enumerate(DAYP): B_E[f][fk][pp] = [ks[k]]*3
                    R = dict(B_REC[fid][fld]); R.update(recs)
                    return L(chain(ch, rec_at(R, wr), B_E[f], we))
                base_recs = {S: sc(CHAT[(fid, ch, S)], lvals[(fid, ch, S)]) for S in CHG}
                if which == 'k':
                    c0 = outL(base_recs, [0.0]*5)
                    cols = []
                    for k in range(5):
                        e = [0.0]*5; e[k] = 1.0; cols.append(outL(base_recs, e) - c0)
                else:
                    zero = {S: [0.0, 0.0, 0.0] for S in CHG}
                    c0 = outL(zero, kvals)
                    cols = []
                    for S in CHG:
                        one = dict(zero); one[S] = CHAT[(fid, ch, S)]; cols.append(outL(one, kvals) - c0)
                s_ = sw*cw/lp
                rows.append([c*s_ for c in cols]); rhs.append((lp - c0)*s_)
    for k, pp in enumerate(DAYP): B_E[f][fk][pp] = [kvals[k]]*3
    return np.array(rows), np.array(rhs)
CHAT = {}
LV0 = {}
def lum_rows_scalar_single(f, grp, B_REC, B_E, fid, ch, lvals, kvals):
    fk = FKEY[FCH[grp][0]]; fld = field_of(ch); rows, rhs = [], []
    for t in GRID:
        p = P_out(ch, fid, t); lp = L(p)
        if lp < 1e-7: continue
        wr = clmt_w(t, CLMT_P); we = tod_weights(t, TOD_P)
        for k, pp in enumerate(DAYP): B_E[f][fk][pp] = [kvals[k]]*3
        zero = {S: [0.0, 0.0, 0.0] for S in CHG}
        R = dict(B_REC[fid][fld]); R.update(zero); c0 = L(chain(ch, rec_at(R, wr), B_E[f], we))
        cols = []
        for S in CHG:
            R1 = dict(R); R1[S] = CHAT[(fid, ch, S)]; cols.append(L(chain(ch, rec_at(R1, wr), B_E[f], we)) - c0)
        rows.append([c/lp for c in cols]); rhs.append((lp - c0)/lp)
    return np.array(rows), np.array(rhs)

def build_baby():
    B_REC = {fid: copy.deepcopy(PIC[fid]) for fid in PIC}
    B_E = {f: copy.deepcopy(E_P[f]) for f in FILES}
    info = {'m': {}, 'iters': {}}
    if DIALS['DL_DESAT_ZERO'] == 1:      # all five daylight periods -> 0
        for f in FILES:
            for p in DAYP: B_E[f]['ENVIRONMENT.DirectLightingDesaturation'][p] = 0.0
    elif DIALS['DL_DESAT_ZERO'] == 2:    # only Day (Picta 1.0 erases the record hue at noon); keep Picta's -0.5 elsewhere
        for f in FILES: B_E[f]['ENVIRONMENT.DirectLightingDesaturation']['Day'] = 0.0
    for f, wids in FILES.items():
        for grp, chs in FCH.items():
            fk = FKEY[chs[0]]
            # initial records: target chroma at the slot peak (pre-compensating the record-side desat), luma m * Picta record luma
            chat = {}
            for fid in wids:
                for ch in chs:
                    for s in CHG:
                        t = SLOT_PEAK[s]
                        tgt, p, _ = target(ch, fid, t)
                        d = 0.0
                        if ch in ('top', 'hor'): d = ini_at(B_E[f], 'SKY.GradientDesaturation', tod_weights(t, TOD_P))
                        if ch == 'clouds': d = ini_at(B_E[f], 'SKY.CloudsDesaturation', tod_weights(t, TOD_P))
                        c0 = norm(inv_desat(tgt, d)) if L(tgt) > 0 else [1, 1, 1]
                        cv = ini_at(B_E[f], CKEY[grp], tod_weights(t, TOD_P)) if CKEY[grp] else 1.0
                        if abs(cv-1.0) > 1e-6: c0 = norm([max(x, 0.0)**(1.0/cv) for x in c0])
                        if ch == 'sunlight':
                            dl = ini_at(B_E[f], 'ENVIRONMENT.DirectLightingDesaturation', tod_weights(t, TOD_P))
                            if dl and dl < 0.999: c0 = norm(inv_desat(c0, dl))
                        chat[(fid, ch, s)] = c0
            m = 1.0
            for fid in wids:
                for ch in chs:
                    fld = field_of(ch)
                    for s in SLOTS:
                        if fld == 'CloudMain': LP = max(L(l['col'][s]) for l in PIC[fid]['_layers'])
                        else: LP = L(PIC[fid][fld][s])
                        c = chat.get((fid, ch, s)) or (norm(PIC[fid][fld][s]) if L(PIC[fid][fld][s]) > 0 else [1, 1, 1])
                        if max(c)*LP > 1e-9: m = min(m, 0.85/(max(c)*LP))
            info['m'][f+'|'+grp] = round(m, 4)
            for fid in wids:
                for ch in chs:
                    fld = field_of(ch)
                    for s in SLOTS:
                        LP = L(PIC[fid][fld][s])
                        c = chat[(fid, ch, s)] if s != 'Night' else (norm(PIC[fid][fld][s]) if LP > 0 else [1, 1, 1])
                        B_REC[fid][fld][s] = q255(sc(c, m*LP))
            for p in ('Night', 'InteriorDay', 'InteriorNight'):
                cv = E_P[f][CKEY[grp]][p] if CKEY[grp] else 1.0
                v = E_P[f][fk][p]; B_E[f][fk][p] = sc(v, 1.0/(m**(cv or 1.0)))
            for p in DAYP: B_E[f][fk][p] = [1.0, 1.0, 1.0]
            if DIALS['SOLVER'] == 1:
                lv = {}
                for fid in wids:
                    for ch in chs:
                        for S in CHG:
                            CHAT[(fid, ch, S)] = norm(B_REC[fid][field_of(ch)][S]) if L(B_REC[fid][field_of(ch)][S]) > 0 else [1, 1, 1]
                            lv[(fid, ch, S)] = L(B_REC[fid][field_of(ch)][S])
                for kk_ in lv: LV0[kk_] = lv[kk_]
                kv = [1.0]*5
                curved_ = CKEY[grp] and any(abs((E_P[f][CKEY[grp]][p] or 1.0)-1.0) > 1e-6 for p in DAYP+['Night'])
                for it in range(8):
                    A, b = lum_rows_scalar(f, grp, B_REC, B_E, 'k', lv, kv)
                    kv = [float(min(10.0, max(0.0, x))) for x in np.linalg.lstsq(A, b, rcond=None)[0]]
                    if curved_: continue
                    A, b = lum_rows_scalar(f, grp, B_REC, B_E, 'l', lv, kv)
                    # weak prior: slot luma stays near its initial value (removes the l*k scale freedom)
                    keys = [(fid, ch, S) for fid in wids for ch in chs for S in CHG]
                    # rows are per weather/channel; solve one weather/channel block at a time
                    sol_all = {}
                    for fid in wids:
                        for ch in chs:
                            Ab, bb = lum_rows_scalar_single(f, grp, B_REC, B_E, fid, ch, lv, kv)
                            prior = 0.3*math.sqrt(max(1, len(bb)))
                            Ap = np.vstack([Ab, prior*np.eye(3)]); bp = np.concatenate([bb, prior*np.array([LV0[(fid, ch, S)] for S in CHG])])
                            sol = np.linalg.lstsq(Ap, bp, rcond=None)[0]
                            for k2, S in enumerate(CHG):
                                cap = 0.999/max(CHAT[(fid, ch, S)])
                                lv[(fid, ch, S)] = float(min(cap, max(0.0, sol[k2])))
                for k, pp in enumerate(DAYP): B_E[f][fk][pp] = [kv[k]]*3
                for fid in wids:
                    for ch in chs:
                        for S in CHG: B_REC[fid][field_of(ch)][S] = q255(sc(CHAT[(fid, ch, S)], lv[(fid, ch, S)]))
                n_it = 0
                def warm_dawn(fid_):
                    h_, s_ = hsv(A_out('sunlight', fid_, SLOT_PEAK['Sunrise']))
                    return s_ > 0.3 and (h_ < 60 or h_ > 330)
                if grp in ('sunlight', 'sun') and DIALS['LIGHT_FREE_FILTERS'] and all(warm_dawn(x) for x in wids):
                    # the moonlit Night record meets the dawn record inside the Dawn/Dusk E11 windows: free RGB filters there only
                    lstsq_filters(f, grp, B_REC, B_E, periods=['Dawn', 'Dusk'])
            # alternate LS (records are only refit when the channel has no E11 curve: the record LS is linear only then)
            curved = CKEY[grp] and any(abs((E_P[f][CKEY[grp]][p] or 1.0)-1.0) > 1e-6 for p in DAYP+['Night'])
            if DIALS['SOLVER'] != 1: n_it = 4 if (DIALS['REFIT_RECORDS'] and not curved) else 1
            for it in range(n_it):
                lstsq_filters(f, grp, B_REC, B_E)
                if DIALS['REFIT_RECORDS'] and it < n_it-1: lstsq_records(f, grp, B_REC, B_E, m)
            # clouds: every enabled layer takes the main layer's chroma at its own (Picta) luma x m; Night unchanged x m
            if grp == 'clouds':
                for fid in wids:
                    LPmain = {s: L(PIC[fid]['CloudMain'][s]) for s in SLOTS}
                    for li, lay in enumerate(B_REC[fid]['_layers']):
                        for s in SLOTS:
                            LPl = L(PIC[fid]['_layers'][li]['col'][s])
                            if s == 'Night': lay['col'][s] = q255(sc(norm(PIC[fid]['_layers'][li]['col'][s]) if LPl > 0 else [1, 1, 1], m*LPl))
                            else:
                                ch_ = norm(B_REC[fid]['CloudMain'][s]) if L(B_REC[fid]['CloudMain'][s]) > 0 else [1, 1, 1]
                                lay['col'][s] = q255(gamut_chroma(m*LPl*L(B_REC[fid]['CloudMain'][s])/max(m*LPmain[s], 1e-9), ch_))
        # scattering colour: grey ScatteringColor g per period (luma lock of S after the max(peak,1) normalisation)
        for p in DAYP: B_E[f]['SKYSCATTERING.ScatteringColor'][p] = [1.0, 1.0, 1.0]
        for p in DAYP:
            num = den = 0.0
            for fid in wids:
                for t in GRID:
                    w = tod_weights(t, TOD_P)[p]
                    if w < 0.5: continue
                    num += L(lane('scat', PIC[fid], E_P[f], t, CLMT_P, TOD_P)); den += L(lane('scat', B_REC[fid], B_E[f], t, CLMT_P, TOD_P))
            g = min(10.0, num/den) if den > 0 else 1.0
            B_E[f]['SKYSCATTERING.ScatteringColor'][p] = [g, g, g]
        for p in DAYP:
            gl = L(E_P[f]['VOLUMETRICFOG.ColorFilter'][p]); B_E[f]['VOLUMETRICFOG.ColorFilter'][p] = [gl, gl, gl]
            B_E[f]['GAMEVOLUMETRICRAYS.ColorFilter'][p] = [1.0, 1.0, 1.0]
    # unfiltered record fields
    for fid in PIC:
        f = FILE_OF[fid]
        for ax in AXES:
            name = 'DALC.'+ax
            for s in CHG:
                t = SLOT_PEAK[s]
                tgt, p, _ = target(name, fid, t)
                # effective desaturation over the hours this slot dominates (AmbientLightingDesaturation varies 0-0.3 inside the Day slot)
                ds = [ini_at(B_E[f], 'ENVIRONMENT.AmbientLightingDesaturation', tod_weights(tt, TOD_P)) or 0.0 for tt in GRID if clmt_w(tt, CLMT_P)[s] >= 0.5]
                d = sum(ds)/len(ds) if ds else 0.0
                ai = ini_at(B_E[f], 'ENVIRONMENT.AmbientLightingIntensity', tod_weights(t, TOD_P))
                tgt = sc(norm(tgt), L(desat(PIC[fid][name][s], d))*ai)
                pre = inv_desat(sc(tgt, 1.0/ai), d)
                B_REC[fid][name][s] = q255(gamut_chroma(L(pre), norm(pre)) if L(pre) > 0 else pre)
        for name in ('EffectLightingColor', 'SkyStaticsColor', 'SkyLowerColor', 'AmbientColor'):
            kk = DIALS['KAPPA_FX'] if name in ('EffectLightingColor', 'SkyStaticsColor') else DIALS['KAPPA_SKY'] if name == 'SkyLowerColor' else DIALS['KAPPA_AMB']
            for s in CHG:
                a = AREC[PARTNER[fid]][name][s]
                T = strength(norm(a), kk) if L(a) > 1e-9 else norm(PIC[fid][name][s])
                B_REC[fid][name][s] = q255(gamut_chroma(L(PIC[fid][name][s]), T))
    return B_REC, B_E, info

B_REC, B_E, INFO = build_baby()
def B_out(ch, fid, t): return lane(ch, B_REC[fid], B_E[FILE_OF[fid]], t, CLMT_P, TOD_P)
NAIVE = {}
for fid in PIC:
    R = copy.deepcopy(PIC[fid]); A = AREC[PARTNER[fid]]
    for fld in ['SkyUpperColor', 'HorizonColor', 'FogFarColor', 'FogNearColor', 'SunlightColor', 'SunColor', 'CloudMain'] + ['DALC.'+a for a in AXES]:
        for s in CHG: R[fld][s] = A[fld][s]
    NAIVE[fid] = R
def N_out(ch, fid, t): return lane(ch, NAIVE[fid], E_P[FILE_OF[fid]], t, CLMT_P, TOD_P)

# ---------------- dome pixel (procedural top/horizon + SkyScattering) ----------------
def vnorm(a):
    l = math.sqrt(sum(x*x for x in a)); return [x/l for x in a]
def sun_dir_at(t):
    el = 2.0 if (t <= 7.5 or t >= 18.5) else max(2.0, 55.0*math.sin(math.pi*(t-7.5)/11.0))
    e = math.radians(el); return vnorm([0.0, math.cos(e), math.sin(e)])
def dome(R, E, t, view):
    wr = clmt_w(t, CLMT_P); we = tod_weights(t, TOD_P); g = lambda k: ini_at(E, k, we)
    top = chain('top', rec_at(R['SkyUpperColor'], wr), E, we); hor = chain('hor', rec_at(R['HorizonColor'], wr), E, we)
    sund = sun_dir_at(t); z = view[2]
    sky = lerp(top, hor, (1.0-sat01(z))**g('SKY.ProceduralGradientWeightCurve'))
    col = chain('scat', rec_at(R['SunColor'], wr), E, we)
    sunH = sund[2]; col = sc(col, math.sqrt(sat01(1.0+2.0*sunH)))
    cpk = max(max(col), 1e-6); dd = g('SKYSCATTERING.DustDensity')
    dustTint = [max(0.0, 1.0-x/cpk)*2*dd**2 for x in col]
    dustVol = 0.02/max(g('SKYSCATTERING.DustVolume')**2, 1e-7)
    hR = 1.0/max(g('SKYSCATTERING.HorizonRange')**3, 1e-6); aT = 100.0/max(g('SKYSCATTERING.AtmosphereThickness')**2, 1e-6)
    agR = 1.0/max(g('SKYSCATTERING.AirGlowRange')**2, 1e-6); sgR = 10.0/max(g('SKYSCATTERING.SunGlowRange')**2, 1e-6)
    amount = g('SKYSCATTERING.Amount')**2
    facing = sat01(sum(a*b for a, b in zip(view, sund))*0.5+0.5); away = 1.0-facing
    elev = 1.0 - sat01(1.0-z)*sat01(1.0+sunH)
    dustBand = sat01(1.0-elev*dustVol)**32
    aboveH = sat01(1.0+z*10.0)**2; sunAbove = sat01(1.0+z*40.0)**2
    spread = lerp(hR*away*away, aT, elev*elev)
    scat = [c*g('SKYSCATTERING.Intensity')*sat01(1.0-dustBand*tt)**32 for c, tt in zip(col, dustTint)]
    scat = sc(scat, aboveH*(1.0-dustBand*g('SKYSCATTERING.DustDarkening')))
    res = sc(sky, 1.0+g('SKYSCATTERING.AirGlowIntensity')/(1.0+away*agR))
    res = lerp(res, scat, sat01(amount/(1.0+away*spread)))
    res = sc(res, 1.0+g('SKYSCATTERING.SunGlowIntensity')*sunAbove/(1.0+away*sgR))
    return lerp(sky, lerp(sc(top, 0.5), res, 1.0), aboveH)
VIEWS = {'zenith': [0, 0, 1], 'hor_sun': vnorm([0, 1, 0.05]), 'hor_away': vnorm([0, -1, 0.05])}

# ---------------- evaluation ----------------
CHS = ['top', 'hor', 'clouds', 'fogfar', 'fognear', 'sunlight', 'sunraw', 'scat', 'DALC.DirectionalXPlus', 'DALC.DirectionalXMinus', 'DALC.DirectionalZMinus']
TIMES = [5.5, 6.0, 6.5, 7.0, 7.25, 7.5, 8.0, 8.5, 9.0, 10.0, 13.0, 15.0, 17.0, 17.5, 18.0, 18.5, 18.75, 19.0, 19.5, 20.0, 20.5]
lines = []
def P(s): lines.append(s)
P('FAITHFUL ASTRALITE v2 - pre-tonemap numeric model of Bottled 4ca678b. dials=' + json.dumps(DIALS))
P('Per time: luma ratio BABY/PICTA (1.000 = brightness locked) | Picta now | BABY | Astralite own lane (phase-mapped clock) | NAIVE = Astralite records under Picta filters')
P('chroma error d = distance of luma-normalised chromaticities (0 = identical hue+saturation); dA = baby vs Astralite target, dP = Picta vs target')
audit = {}
for fid in PIC:
    audit[fid] = {}
    for ch in CHS:
        dev = 0.0; dA = []; dP = []
        for t in GRID:
            lp = L(P_out(ch, fid, t)); lb = L(B_out(ch, fid, t))
            if lp > 1e-7: dev = max(dev, abs(lb/lp-1))
        for s in CHG:
            t = SLOT_PEAK[s]
            tgt, p, _ = target(ch, fid, t) if ch != 'scat' else target('sunraw', fid, t)
            dA.append(round(cdist(B_out(ch, fid, t), tgt), 3)); dP.append(round(cdist(p, tgt), 3))
        audit[fid][ch] = dict(max_luma_dev=round(dev, 4), chroma_err_baby=dA, chroma_err_picta=dP)
SHOW = [x for x in ('19FA01', '19FC01', '19FD02', '19FD03') if x in PIC]
for fid in SHOW:
    P(f"\n=========== {fid} {PIC[fid]['_edid']}  partner {AREC[PARTNER[fid]]['_edid']}  file {FILE_OF[fid]}")
    for ch in CHS:
        P(f"-- {ch}")
        for t in TIMES:
            pc = P_out(ch, fid, t); bc = B_out(ch, fid, t); ac = A_out(ch, fid, t); nc = N_out(ch, fid, t)
            r = L(bc)/L(pc) if L(pc) > 1e-9 else float('nan')
            P(f"  {t:5.2f}h luma {r:6.3f} | picta {hue_s(pc)} | BABY {hue_s(bc)} | astra {hue_s(ac)} | naive {hue_s(nc)} x{(L(nc)/L(pc) if L(pc) > 1e-9 else 0):.2f}")
    P('-- dome pixels (view relative to the sun azimuth)')
    for t in (7.0, 7.5, 8.0, 10.0, 13.0, 17.0, 18.0, 18.5, 19.0):
        for vn, vd in VIEWS.items():
            pc = dome(PIC[fid], E_P[FILE_OF[fid]], t, vd); bc = dome(B_REC[fid], B_E[FILE_OF[fid]], t, vd); nc = dome(NAIVE[fid], E_P[FILE_OF[fid]], t, vd)
            P(f"  {t:5.2f}h {vn:9s} luma {L(bc)/L(pc):6.3f} | picta {hue_s(pc)} | BABY {hue_s(bc)} | naive {hue_s(nc)} x{L(nc)/L(pc):.2f}")
P('\n=========== ALL weathers: max |luma(baby)/luma(picta)-1| over 05:00-21:00 (15-min grid)')
for fid in PIC:
    P(f"{fid} {PIC[fid]['_edid'][16:]:30s} " + ' '.join(f"{ch.replace('DALC.Directional','')}:{audit[fid][ch]['max_luma_dev']:.3f}" for ch in CHS))
P('\nchroma error to target at the Sunrise/Day/Sunset slot peaks: baby | picta-now')
for fid in PIC:
    P(f"{fid} " + ' '.join(f"{ch.replace('DALC.Directional','')}:{audit[fid][ch]['chroma_err_baby']}|{audit[fid][ch]['chroma_err_picta']}" for ch in CHS))

# ---------------- design tables ----------------
design = {'dials': DIALS, 'm_luma_scale': INFO['m'], 'e11': {}, 'records': {}, 'voli': {}, 'fog_distance': {}, 'imgs': {}}
EDIT_KEYS = ['SKY.GradientTopColorFilter', 'SKY.GradientHorizonColorFilter', 'SKY.CloudsColorFilter', 'SKY.SunColorFilter',
             'ENVIRONMENT.FogColorFilter', 'ENVIRONMENT.DirectLightingColorFilter', 'ENVIRONMENT.DirectLightingDesaturation',
             'SKYSCATTERING.ScatteringColor', 'VOLUMETRICFOG.ColorFilter', 'GAMEVOLUMETRICRAYS.ColorFilter']
for f in FILES:
    design['e11'][f] = {}
    for k in EDIT_KEYS:
        row = {}
        for p in PER:
            nv, ov = B_E[f][k][p], E_P[f][k][p]
            if nv != ov:
                row[p] = {'new': [round(x, 4) for x in nv] if isinstance(nv, list) else round(nv, 4),
                          'was': [round(x, 4) for x in ov] if isinstance(ov, list) else ov}
        if row: design['e11'][f][k] = row
for fid in PIC:
    R = B_REC[fid]; o = {'partner': AREC[PARTNER[fid]]['_edid'] + ' ' + PARTNER[fid] + ' (Astralite ENB.esp values)'}
    for fld in ['SkyUpperColor', 'SkyLowerColor', 'HorizonColor', 'FogNearColor', 'FogFarColor', 'SunlightColor', 'SunColor',
                'EffectLightingColor', 'SkyStaticsColor', 'AmbientColor'] + ['DALC.'+a for a in AXES]:
        o[fld] = {s: {'was': to255(PIC[fid][fld][s]), 'new': to255(R[fld][s])} for s in SLOTS if to255(PIC[fid][fld][s]) != to255(R[fld][s])}
    o['clouds'] = [{'layer': l['i'], 'tex': l['tex'], 'col': {s: {'was': to255(PIC[fid]['_layers'][j]['col'][s]), 'new': to255(l['col'][s])} for s in SLOTS}}
                   for j, l in enumerate(R['_layers'])]
    design['records'][fid + ' ' + PIC[fid]['_edid']] = o
# VOLI transplant (needs vanilla VL enabled in the baby, see plumbing)
for fid in PIC:
    A = AREC[PARTNER[fid]]; vr = A['_voli'] or {}; row = {}
    for s in CHG:
        v = vr.get(s)
        if not isinstance(v, dict): continue
        tP = SLOT_PEAK[s]; tA = phase_map(tP)
        gS = ini_at(E_S[PARTNER[fid]], 'GAMEVOLUMETRICRAYS.Intensity', tod_weights(tA, TOD_A))
        gP = ini_at(E_P[FILE_OF[fid]], 'GAMEVOLUMETRICRAYS.Intensity', tod_weights(tP, TOD_P))
        inten = v.get('intensity')
        row[s] = dict(copy_of=v.get('editorid'), src=v.get('formid'), rgb255=v.get('color_rgb255'), custom_color_contribution=v.get('custom_color_contribution'),
                      density=v.get('density_contribution'), astra_intensity=inten, soul_gvr_at_phase=round(gS, 3), picta_gvr_at_peak=round(gP, 3),
                      baby_intensity=round(inten*gS/gP*DIALS['VL_STRENGTH'], 3) if (inten is not None and gP) else None)
    design['voli'][fid + ' ' + PIC[fid]['_edid']] = row
EFF = {r['editorid']: r for r in json.load(open(SCR + '/map/fog-mist/effective_fog_after_e11.json'))}
for fid in PIC:
    f = FILE_OF[fid]; A = AREC[PARTNER[fid]]; pe = PIC[fid]['_fog']; ae = EFF.get(A['_edid']); row = {}
    for dn in ('Day', 'Night'):
        fam = E_P[f]['ENVIRONMENT.FogAmountMultiplier'][dn]; fcm = E_P[f]['ENVIRONMENT.FogCurveMultiplier'][dn]
        pf = pe[f'FogDistance{dn}Far']/fam; af = ae[f'{dn.lower()}_far'] if ae else None
        # fog-density transplant only on Picta's fog/mist classes and snow storms; dry thunderstorms E01/E02 keep Picta
        # (their Astralite partners are precipitation storms whose fog is rain/snow haze)
        if af and af < pf and fid in ('19FB03', '19FC03', '19FD02', '19FE05', '19FE06'):
            nf = math.exp(lerp(math.log(pf), math.log(af), DIALS['FOG_DENSITY']))
            row[dn] = dict(picta_eff_far=round(pf), astra_eff_far=round(af), baby_eff_far=round(nf), set_record_FogDistance_Far=round(nf*fam),
                           record_was=pe[f'FogDistance{dn}Far'], near_power_max='unchanged')
        else:
            row[dn] = dict(picta_eff_far=round(pf), astra_eff_far=(round(af) if af else None), action='keep - Picta already as dense or denser')
    design['fog_distance'][fid + ' ' + PIC[fid]['_edid']] = row
IM = json.load(open(SCR + '/map/picta-colour/picta_imgs_by_weather.json'))
seen = {}
for w, v in IM.items():
    for s in CHG:
        x = v['imgs'][s]
        if x['imgs'] in seen: continue
        t = [int(c) for c in x['tint'].split(',')[:3]]; Lt = L(t)
        g = [round(lerp(c, Lt, DIALS['IMGS_NEUTRAL'])) for c in t]
        seen[x['imgs']] = dict(editorid=x['editorid'], slot=s, tint_was=t, tint_new=g, amount_kept=x['tint_amt'], saturation_kept=x['sat'])
design['imgs'] = seen
json.dump(design, open(OUT + '/design_values.json', 'w'), indent=1, default=str)
json.dump(audit, open(OUT + '/luma_audit.json', 'w'), indent=1)
open(OUT + '/model_out.txt', 'w').write('\n'.join(lines))
print('\n'.join(lines[:4])); print('m:', INFO['m']); print('written', OUT)
