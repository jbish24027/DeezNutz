"""FAITHFUL ASTRALITE baby - design solver + numeric proof.

Route A: hue moves to the RECORD side (as in Astralite); Picta's chromatic E11 filters become
luma-only scalars (grey), so Picta brightness is locked by Rec.709 luma at every E11 anchor.

Inputs (all read-only):
  live Picta E11 override  C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1/enbseries(+.ini)
  map dumps under scratchpad/baby/map (Picta winners, Astralite ENB records, Soul Core E11 values)
Outputs (scratch only): design_values.json, model_out.txt, luma_audit.json in this folder.

Engine model = map/e11-colour-model/colour_model.py (Bottled 4ca678b): Curve/Desat/ColorFilter, sky bands,
procedural dome + SkyScattering, fog, direct light, DALC; E11 [TIMEOFDAY] weights; CLMT record interpolation
(Night->Sunrise over the first half of the sunrise window, Sunrise->Day over the second half; same for sunset -
assumed engine behaviour, flagged open in the map).
"""
import json, math, os, re, colorsys, copy, sys

SCR = 'C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby'
OUT = SCR + '/design/faithful'
LIVE_MOD = 'C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1'
LIVE = LIVE_MOD + '/enbseries'

# ---------------- dials (defaults = the Faithful design) ----------------
DIALS = dict(
    ALPHA_SKY=0.85,      # sky top/horizon/lower bands, clouds, sun disc + scattering colour
    ALPHA_FOGCOL=0.85,   # fog near/far colour
    ALPHA_LIGHT=0.85,    # sunlight (direct light) colour
    ALPHA_AMB=0.85,      # DALC ambient, 6 axes
    ALPHA_FX=0.85,       # EffectLighting + SkyStatics colour (mist meshes / sky statics) - gamut limited
    SHOULDER=1.0,        # fraction of ALPHA used at E11 Sunrise(9:00)/Sunset(17:00) anchors; 0 keeps Picta's golden shoulders
    IMGS_NEUTRAL=1.0,    # Sunrise/Day/Sunset IMGS tint colour -> equal-luma grey (amount kept)
    VL_STRENGTH=1.0,     # transplanted VOLI effective intensity relative to the Astralite lane
    FOG_DENSITY=0.5,     # log-space step from Picta toward Astralite effective fog far (add-only)
)
for a in sys.argv[1:]:
    k, v = a.split('=')
    DIALS[k] = float(v)

PER = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night', 'InteriorDay', 'InteriorNight']
EXT6 = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
DAYP = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk']
SLOTS = ['Sunrise', 'Day', 'Sunset', 'Night']
CHG_SLOTS = ['Sunrise', 'Day', 'Sunset']

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
    """record r with desat(r,d)==t (mean is invariant); clipped at 0"""
    if abs(1-d) < 1e-6: return list(t)
    m = mean3(t); return [max((x - d*m)/(1-d), 0.0) for x in t]
def cfilter(c, f, amt): return mul([lerp(x, 1.0, amt) for x in c], f)
def norm(c):
    l = L(c); return [x/l for x in c] if l > 1e-9 else [1.0, 1.0, 1.0]
def hsv(c):
    mx = max(c)
    if mx <= 0: return (0.0, 0.0)
    h, s, v = colorsys.rgb_to_hsv(*[max(x, 0)/mx for x in c])
    return (h*360.0, s)
def hue_s(c):
    h, s = hsv(c); return f"h{h:5.1f} s{s:.2f}"
def hdist(a, b):
    d = abs(a-b) % 360; return min(d, 360-d)
def rgb01(s):
    p = [float(x) for x in str(s).split(',')[:3]]; return [x/255.0 for x in p]
def to255(c): return [int(round(max(0.0, min(1.0, x))*255)) for x in c]
def gamut_chroma(Lt, chat):
    """colour with luma Lt and chromaticity chat (L(chat)=1); chroma shrunk (house transform c'=L+(c-L)k) to fit [0,1]"""
    c = sc(chat, Lt)
    if max(c) <= 1.0: return c, 1.0
    k = (1.0 - Lt)/(max(c) - Lt) if max(c) > Lt else 0.0
    return [Lt + (x-Lt)*k for x in c], k

# ---------------- ini reading (GetPrivateProfileString semantics) ----------------
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
    d = {}
    for sec, ks in KEYS.items():
        for k in ks:
            d[sec+'.'+k] = {p: ini_get(wf, sec, k, p) for p in PER}
    return d

SOUL = json.load(open(SCR + '/map/astralite-colour/soulcore_e11_colour_keys.json'))
def load_soul(fname):
    wfv = SOUL['weather_files'].get(fname, {}).get('values', {})
    d = {}
    for sec, ks in KEYS.items():
        for k in ks:
            key = sec+'.'+k; src = wfv.get(key) or SOUL['base_values'].get(key)
            row = {}
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
CLMT_P = (6.0, 9.0, 17.0, 20.0)       # PIC_CLMT_Skyrim (Darkened patch)
CLMT_A = (4.5, 9.5, 16.5, 21.5)       # Astralite ENB SkyrimClimate
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
ANCHOR = dict(Dawn=7.25, Sunrise=9.0, Day=10.0, Sunset=17.0, Dusk=18.75, Night=22.0)
SLOT_PEAK = dict(Sunrise=7.5, Day=10.0, Sunset=18.5, Night=22.0)

def ini_at(E, key, w):
    vals = E[key]; acc = None
    for p, wt in w.items():
        if wt <= 0: continue
        v = vals[p]
        if v is None: continue
        if isinstance(v, list): acc = sc(v, wt) if acc is None else add(acc, sc(v, wt))
        else: acc = v*wt if acc is None else acc + v*wt
    return acc
def rec_at(R, field, w):
    acc = [0.0, 0.0, 0.0]
    for s, wt in w.items():
        if wt > 0: acc = add(acc, sc(R[field][s], wt))
    return acc

# ---------------- channel chains (Effects11.cpp 557-780 @4ca678b) ----------------
def ch_band(R, E, w, band):
    k = {'top': ('SkyUpperColor', 'GradientTop'), 'hor': ('HorizonColor', 'GradientHorizon')}[band]
    c = rec_at(R, k[0], w)
    c = curve(c, ini_at(E, 'SKY.'+k[1]+'Curve', w))
    c = sc(mul(c, ini_at(E, 'SKY.'+k[1]+'ColorFilter', w)), ini_at(E, 'SKY.'+k[1]+'Intensity', w)*ini_at(E, 'SKY.GradientIntensity', w))
    return desat(c, ini_at(E, 'SKY.GradientDesaturation', w))
def ch_clouds(R, E, w):
    c = rec_at(R, 'CloudMain', w)
    c = desat(curve(c, ini_at(E, 'SKY.CloudsCurve', w)), ini_at(E, 'SKY.CloudsDesaturation', w))
    return mul(sc(c, ini_at(E, 'SKY.CloudsIntensity', w)), ini_at(E, 'SKY.CloudsColorFilter', w))
def ch_fog(R, E, w, which='FogFarColor'):
    c = curve(rec_at(R, which, w), ini_at(E, 'ENVIRONMENT.FogColorCurve', w))
    c = cfilter(c, ini_at(E, 'ENVIRONMENT.FogColorFilter', w), ini_at(E, 'ENVIRONMENT.FogColorFilterAmount', w))
    return sc(c, ini_at(E, 'ENVIRONMENT.FogColorMultiplier', w))
def ch_sunlight(R, E, w):
    c = curve(rec_at(R, 'SunlightColor', w), ini_at(E, 'ENVIRONMENT.DirectLightingCurve', w))
    c = desat(c, ini_at(E, 'ENVIRONMENT.DirectLightingDesaturation', w))
    c = cfilter(c, ini_at(E, 'ENVIRONMENT.DirectLightingColorFilter', w), ini_at(E, 'ENVIRONMENT.DirectLightingColorFilterAmount', w))
    return sc(c, ini_at(E, 'ENVIRONMENT.DirectLightingIntensity', w))
def ch_sun(R, E, w):
    c = cfilter(desat(rec_at(R, 'SunColor', w), ini_at(E, 'SKY.SunDesaturation', w)), ini_at(E, 'SKY.SunColorFilter', w), 0.0)
    pk = max(max(c), 1.0); return [max(x, 0)/pk for x in c]
def ch_amb(R, E, w, axis):
    c = rec_at(R, 'DALC.'+axis, w)
    return sc(desat(c, ini_at(E, 'ENVIRONMENT.AmbientLightingDesaturation', w)), ini_at(E, 'ENVIRONMENT.AmbientLightingIntensity', w))
def ch_raw(R, E, w, field): return rec_at(R, field, w)

def vnorm(a):
    l = math.sqrt(sum(x*x for x in a)); return [x/l for x in a]
def dome_pixel(R, E, w, view, sun_dir):
    """colour_model.sky_pixel generalised to blended ini (UseProceduralGradientWeights=true lanes only)"""
    g = lambda k: ini_at(E, k, w)
    top = ch_band(R, E, w, 'top'); hor = ch_band(R, E, w, 'hor')
    z = view[2]
    sky = lerp(top, hor, (1.0-sat01(z))**g('SKY.ProceduralGradientWeightCurve'))
    sunN = ch_sun(R, E, w)
    sunH = sun_dir[2]; sunFade = math.sqrt(sat01(1.0+2.0*sunH))
    col = [(1.0+(s-1.0)*g('SKYSCATTERING.ColorFromSun'))*c*sunFade for s, c in zip(sunN, g('SKYSCATTERING.ScatteringColor'))]
    cpk = max(max(col), 1e-6)
    dd = g('SKYSCATTERING.DustDensity')
    dustTint = [max(0.0, 1.0-x/cpk)*2*dd**2 for x in col]
    dustVol = 0.02/max(g('SKYSCATTERING.DustVolume')**2, 1e-7)
    hR = 1.0/max(g('SKYSCATTERING.HorizonRange')**3, 1e-6)
    aT = 100.0/max(g('SKYSCATTERING.AtmosphereThickness')**2, 1e-6)
    agR = 1.0/max(g('SKYSCATTERING.AirGlowRange')**2, 1e-6)
    sgR = 10.0/max(g('SKYSCATTERING.SunGlowRange')**2, 1e-6)
    amount = g('SKYSCATTERING.Amount')**2
    facing = sat01(sum(a*b for a, b in zip(view, sun_dir))*0.5+0.5); away = 1.0-facing
    elev = 1.0 - sat01(1.0-z)*sat01(1.0+sunH)
    dustBand = sat01(1.0-elev*dustVol)**32
    aboveH = sat01(1.0+z*10.0)**2; sunAbove = sat01(1.0+z*40.0)**2
    spread = lerp(hR*away*away, aT, elev*elev)
    scat = [c*g('SKYSCATTERING.Intensity')*sat01(1.0-dustBand*t)**32 for c, t in zip(col, dustTint)]
    scat = sc(scat, aboveH*(1.0-dustBand*g('SKYSCATTERING.DustDarkening')))
    res = sc(sky, 1.0+g('SKYSCATTERING.AirGlowIntensity')/(1.0+away*agR))
    wgt = sat01(amount/(1.0+away*spread))
    res = lerp(res, scat, wgt)
    res = sc(res, 1.0+g('SKYSCATTERING.SunGlowIntensity')*sunAbove/(1.0+away*sgR))
    return lerp(sky, lerp(sc(top, 0.5), res, 1.0), aboveH)

def sun_dir_at(t):
    # sun elevation along a simple day arc on Picta's clock: 0 deg at 6.0/20.0 is not right for Skyrim; use the
    # CLMT midpoints as horizon crossings (7.5 / 18.5), noon peak 55 deg.
    if t <= 7.5 or t >= 18.5: el = 2.0
    else: el = max(2.0, 55.0*math.sin(math.pi*(t-7.5)/11.0))
    e = math.radians(el); return vnorm([0.0, math.cos(e), math.sin(e)])
VIEWS = {'zenith': [0, 0, 1], 'hor_sun': vnorm([0, 1, 0.05]), 'hor_away': vnorm([0, -1, 0.05])}

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
                    'EffectLightingColor', 'SkyStaticsColor', 'AmbientColor', 'WaterMultiplierColor'):
            R[fld] = {s: rgb01(F[fld+'.'+s]) for s in SLOTS}
        for ax in ('DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus'):
            R['DALC.'+ax] = {s: rgb01(F[f'DirectionalAmbientLightingColors.{s}.{ax}']) for s in SLOTS}
        layers = []
        for i in range(32):
            if F.get(f'Clouds[{i}].Enabled') == 'True' and F.get(f'CloudTextures[{i}]', '(absent)') != '(absent)':
                layers.append({'i': i, 'tex': F.get(f'CloudTextures[{i}]'), 'col': {s: rgb01(F[f'Clouds[{i}].Colors.{s}']) for s in SLOTS}})
        R['_layers'] = layers
        main = [l for l in layers if 'Cloud_Panorama' in (l['tex'] or '')] or layers
        R['CloudMain'] = main[0]['col']
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
    for fld, v in a['colors'].items():
        R[fld] = {s: [x/255.0 for x in v[s]] for s in SLOTS}
    for s in SLOTS:
        for ax, v in a['dalc'][s].items():
            if ax.startswith('Directional'): R.setdefault('DALC.'+ax, {})[s] = [x/255.0 for x in v]
    en = [c for c in a['clouds'] if c.get('enabled') == 'True']
    R['_ncloud'] = len(en)
    R['CloudMain'] = {}
    for s in SLOTS:
        cols = [[x/255.0 for x in c['colors'][s]] for c in en if sum(c['colors'][s]) > 0]
        R['CloudMain'][s] = [sum(c[i] for c in cols)/len(cols) for i in range(3)] if cols else [1, 1, 1]
    R['_fog'] = a['fog_distance']; R['_voli'] = a.get('volumetric_resolved'); R['_ve'] = a.get('visual_effect')
    return R

# canonical partner per Picta weather (Astralite ENB.esp record values = PBR live, Dawn Warmth is a verified no-op)
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
SHARE = {}   # roll share for weighting shared files (pairing_table region_month_share_sum)
for r in json.load(open(SCR + '/map/pairing/pairing_table.json'))['picta_rotation']:
    SHARE[r['formid'].split(':')[0]] = r['rolls']['region_month_share_sum']

PIC = load_picta_records()
E_P = {f: load_e11(LIVE + '/' + f) for f in FILES}
AREC = {k: load_astra(k) for k in set(PARTNER.values())}
E_S = {k: load_soul(AREC[k]['_soul']) for k in AREC}
NAT_BASE_E = None

# channel registry: name -> (fields, filter keys, chain)
FILTERED = {
 'top':      dict(fields=['SkyUpperColor'], fkeys=['SKY.GradientTopColorFilter'], dkey='SKY.GradientDesaturation', alpha='ALPHA_SKY'),
 'hor':      dict(fields=['HorizonColor'], fkeys=['SKY.GradientHorizonColorFilter'], dkey='SKY.GradientDesaturation', alpha='ALPHA_SKY'),
 'clouds':   dict(fields=['CloudMain'], fkeys=['SKY.CloudsColorFilter'], dkey='SKY.CloudsDesaturation', alpha='ALPHA_SKY'),
 'fog':      dict(fields=['FogFarColor', 'FogNearColor'], fkeys=['ENVIRONMENT.FogColorFilter'], dkey=None, alpha='ALPHA_FOGCOL'),
 'sunlight': dict(fields=['SunlightColor'], fkeys=['ENVIRONMENT.DirectLightingColorFilter'], dkey=None, alpha='ALPHA_LIGHT'),
 'sun':      dict(fields=['SunColor'], fkeys=['SKY.SunColorFilter'], dkey='SKY.SunDesaturation', alpha='ALPHA_SKY'),
}
def chain(name, R, E, w, field=None):
    if name == 'top': return ch_band(R, E, w, 'top')
    if name == 'hor': return ch_band(R, E, w, 'hor')
    if name == 'clouds': return ch_clouds(R, E, w)
    if name == 'fog': return ch_fog(R, E, w, field or 'FogFarColor')
    if name == 'sunlight': return ch_sunlight(R, E, w)
    if name == 'sun': return ch_sun(R, E, w)
    if name.startswith('DALC.'): return ch_amb(R, E, w, name[5:])
    return ch_raw(R, E, w, name)

FILE_OF = {w: f for f, ws in FILES.items() for w in ws}

def lane_eval(name, R, E, t, clmt, tod, field=None):
    """records interpolate on the CLMT clock, ini values on the E11 [TIMEOFDAY] clock"""
    wr = clmt_w(t, clmt); we = tod_weights(t, tod)
    V = {k: {'X': rec_at(R, k, wr)} for k, v in R.items()
         if isinstance(v, dict) and set(v.keys()) >= set(SLOTS) and all(isinstance(v[x], list) for x in SLOTS)}
    return chain_view(name, V, E, we, field)
def chain_view(name, V, E, we, field):
    # same chains as ch_* but with records already resolved to the single slot 'X'
    if name in ('top', 'hor'):
        k = {'top': ('SkyUpperColor', 'GradientTop'), 'hor': ('HorizonColor', 'GradientHorizon')}[name]
        c = curve(V[k[0]]['X'], ini_at(E, 'SKY.'+k[1]+'Curve', we))
        c = sc(mul(c, ini_at(E, 'SKY.'+k[1]+'ColorFilter', we)), ini_at(E, 'SKY.'+k[1]+'Intensity', we)*ini_at(E, 'SKY.GradientIntensity', we))
        return desat(c, ini_at(E, 'SKY.GradientDesaturation', we))
    if name == 'clouds':
        c = desat(curve(V['CloudMain']['X'], ini_at(E, 'SKY.CloudsCurve', we)), ini_at(E, 'SKY.CloudsDesaturation', we))
        return mul(sc(c, ini_at(E, 'SKY.CloudsIntensity', we)), ini_at(E, 'SKY.CloudsColorFilter', we))
    if name == 'fog':
        c = curve(V[field or 'FogFarColor']['X'], ini_at(E, 'ENVIRONMENT.FogColorCurve', we))
        c = cfilter(c, ini_at(E, 'ENVIRONMENT.FogColorFilter', we), ini_at(E, 'ENVIRONMENT.FogColorFilterAmount', we))
        return sc(c, ini_at(E, 'ENVIRONMENT.FogColorMultiplier', we))
    if name == 'sunlight':
        c = curve(V['SunlightColor']['X'], ini_at(E, 'ENVIRONMENT.DirectLightingCurve', we))
        c = desat(c, ini_at(E, 'ENVIRONMENT.DirectLightingDesaturation', we))
        c = cfilter(c, ini_at(E, 'ENVIRONMENT.DirectLightingColorFilter', we), ini_at(E, 'ENVIRONMENT.DirectLightingColorFilterAmount', we))
        return sc(c, ini_at(E, 'ENVIRONMENT.DirectLightingIntensity', we))
    if name == 'sun':
        c = cfilter(desat(V['SunColor']['X'], ini_at(E, 'SKY.SunDesaturation', we)), ini_at(E, 'SKY.SunColorFilter', we), 0.0)
        pk = max(max(c), 1.0); return [max(x, 0)/pk for x in c]
    if name.startswith('DALC.'):
        return sc(desat(V[name]['X'], ini_at(E, 'ENVIRONMENT.AmbientLightingDesaturation', we)), ini_at(E, 'ENVIRONMENT.AmbientLightingIntensity', we))
    return V[name]['X']
def dome_eval(R, E, t, clmt, tod, view):
    wr = clmt_w(t, clmt); we = tod_weights(t, tod)
    V = {k: {'X': rec_at(R, k, wr)} for k, v in R.items()
         if isinstance(v, dict) and set(v.keys()) >= set(SLOTS) and all(isinstance(v[x], list) for x in SLOTS)}
    return dome_pixel(V, E, we, view, sun_dir_at(t))
# patch rec_at to understand single-slot 'X' views
_rec_at_orig = rec_at
def rec_at(R, field, w):
    if 'X' in R[field] and len(R[field]) == 1: return R[field]['X']
    return _rec_at_orig(R, field, w)

def P_out(name, fid, t, field=None): return lane_eval(name, PIC[fid], E_P[FILE_OF[fid]], t, CLMT_P, TOD_P, field)
def A_out(name, akey, tA, field=None): return lane_eval(name, AREC[akey], E_S[akey], tA, CLMT_A, TOD_A, field)

# ---------------- solver ----------------
def target_hat(name, fid, t, alpha, field=None):
    P = P_out(name, fid, t, field); A = A_out(name, PARTNER[fid], phase_map(t), field)
    return lerp(norm(P), norm(A), alpha), P, A

def build_baby():
    B_REC = {fid: copy.deepcopy(PIC[fid]) for fid in PIC}
    B_E = {f: copy.deepcopy(E_P[f]) for f in FILES}
    design = {'dials': DIALS, 'files': {}, 'records': {}, 'm': {}}
    # 0) DirectLightingDesaturation -> 0 for the five daylight periods (record now carries the light hue)
    for f in FILES:
        for p in DAYP: B_E[f]['ENVIRONMENT.DirectLightingDesaturation'][p] = 0.0
    # 1) per file, per filtered channel: records (all weathers of the file) then filters
    for f, wids in FILES.items():
        design['files'][f] = {}
        for ch, spec in FILTERED.items():
            a = DIALS[spec['alpha']]
            chat = {}   # (fid, field, slot) -> record chromaticity (L=1)
            for fid in wids:
                for fld in spec['fields']:
                    for s in CHG_SLOTS:
                        t = SLOT_PEAK[s]
                        T, P, A = target_hat(ch, fid, t, a, fld if ch == 'fog' else None)
                        d = 0.0
                        if spec['dkey'] and ch != 'sunlight':
                            d = ini_at(B_E[f], spec['dkey'], tod_weights(t, TOD_P)) or 0.0
                        chat[(fid, fld, s)] = norm(inv_desat(T, d)) if d else T
            # m: largest common luma scale so every slot of every weather (incl. Night) fits in bytes
            m = 1.0
            for fid in wids:
                for fld in spec['fields']:
                    for s in SLOTS:
                        LP = L(PIC[fid][fld][s] if fld != 'CloudMain' else PIC[fid]['CloudMain'][s])
                        if fld == 'CloudMain':
                            LP = max(L(l['col'][s]) for l in PIC[fid]['_layers'])
                        c = chat.get((fid, fld, s), norm(PIC[fid][fld][s]) if L(PIC[fid][fld][s]) > 0 else [1, 1, 1])
                        mx = max(c)*LP
                        if mx > 1e-9: m = min(m, 0.999/mx)
            design['m'][(f + '|' + ch)] = m
            # write records
            for fid in wids:
                for fld in spec['fields']:
                    for s in SLOTS:
                        if fld == 'CloudMain':
                            for li, lay in enumerate(B_REC[fid]['_layers']):
                                LPl = L(PIC[fid]['_layers'][li]['col'][s])
                                c = chat.get((fid, fld, s)) if s != 'Night' else norm(PIC[fid]['_layers'][li]['col'][s]) if LPl > 0 else [1, 1, 1]
                                lay['col'][s] = [x/255.0 for x in to255(sc(c, m*LPl))]
                            main = [l for l in B_REC[fid]['_layers'] if 'Cloud_Panorama' in (l['tex'] or '')] or B_REC[fid]['_layers']
                            B_REC[fid]['CloudMain'][s] = main[0]['col'][s]
                        else:
                            LPs = L(PIC[fid][fld][s])
                            if s == 'Night': c = norm(PIC[fid][fld][s]) if LPs > 0 else [1, 1, 1]
                            else: c = chat[(fid, fld, s)]
                            B_REC[fid][fld][s] = [x/255.0 for x in to255(sc(c, m*LPs))]
            # filters: Night + interiors = Picta / m (identical output); daylight periods solved at anchors
            for fk in spec['fkeys']:
                for p in ('Night', 'InteriorDay', 'InteriorNight'):
                    v = E_P[f][fk][p]
                    B_E[f][fk][p] = sc(v, 1.0/m) if isinstance(v, list) else v
                for p in DAYP: B_E[f][fk][p] = [1.0, 1.0, 1.0]
        # 2) solve k (and shoulder hue H) per period at the anchors, iterate (records + filters interact via desat)
        for it in range(3):
            for ch, spec in FILTERED.items():
                fk = spec['fkeys'][0]
                a = DIALS[spec['alpha']]
                for p in DAYP:
                    t = ANCHOR[p]
                    H = [1.0, 1.0, 1.0]
                    if p in ('Sunrise', 'Sunset'):
                        # residual hue so the baby output at the shoulder hits the (alpha*SHOULDER) target
                        acc = [0.0, 0.0, 0.0]; wsum = 0.0
                        for fid in wids:
                            fld = 'FogFarColor' if ch == 'fog' else None
                            T, P, A = target_hat(ch, fid, t, a*DIALS['SHOULDER'], fld)
                            B_E[f][fk][p] = [1.0, 1.0, 1.0]
                            Bo = lane_eval(ch, B_REC[fid], B_E[f], t, CLMT_P, TOD_P, fld)
                            h = [tt/max(bb, 1e-9) for tt, bb in zip(T, norm(Bo))] if L(Bo) > 0 else [1, 1, 1]
                            sw = SHARE.get(fid, 1.0); acc = add(acc, sc(h, sw)); wsum += sw
                        H = sc(acc, 1.0/wsum)
                        H = sc(H, 1.0/max(H))
                    # luma lock: k so that baby luma == Picta luma at the anchor (share-weighted over the file's weathers)
                    B_E[f][fk][p] = H
                    num = den = 0.0
                    for fid in wids:
                        sw = SHARE.get(fid, 1.0)
                        fld = 'FogFarColor' if ch == 'fog' else None
                        num += sw*L(P_out(ch, fid, t, fld)); den += sw*L(lane_eval(ch, B_REC[fid], B_E[f], t, CLMT_P, TOD_P, fld))
                    k = num/den if den > 1e-12 else 1.0
                    B_E[f][fk][p] = [min(10.0, max(0.0, x*k)) for x in H]
        # 3) tied/auxiliary filters
        for p in DAYP:
            g = L(E_P[f]['VOLUMETRICFOG.ColorFilter'][p]); B_E[f]['VOLUMETRICFOG.ColorFilter'][p] = [g, g, g]
            B_E[f]['GAMEVOLUMETRICRAYS.ColorFilter'][p] = [1.0, 1.0, 1.0]
        for ch, spec in FILTERED.items():
            design['files'][f][spec['fkeys'][0]] = {p: [round(x, 4) for x in B_E[f][spec['fkeys'][0]][p]] for p in PER}
        design['files'][f]['ENVIRONMENT.DirectLightingDesaturation'] = {p: B_E[f]['ENVIRONMENT.DirectLightingDesaturation'][p] for p in PER}
        design['files'][f]['VOLUMETRICFOG.ColorFilter'] = {p: [round(x, 4) for x in B_E[f]['VOLUMETRICFOG.ColorFilter'][p]] for p in PER}
        design['files'][f]['GAMEVOLUMETRICRAYS.ColorFilter'] = {p: B_E[f]['GAMEVOLUMETRICRAYS.ColorFilter'][p] for p in PER}
    # 4) unfiltered record fields: DALC 6 axes (AmbientLightingDesaturation kept -> pre-compensated), EffectLighting, SkyStatics
    for fid in PIC:
        f = FILE_OF[fid]
        for ax in ('DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus'):
            name = 'DALC.'+ax
            for s in CHG_SLOTS:
                t = SLOT_PEAK[s]
                T, P, A = target_hat(name, fid, t, DIALS['ALPHA_AMB'])
                d = ini_at(B_E[f], 'ENVIRONMENT.AmbientLightingDesaturation', tod_weights(t, TOD_P)) or 0.0
                LP = L(desat(PIC[fid][name][s], d))
                pre = inv_desat(sc(T, LP), d)
                col, kk = gamut_chroma(L(pre), norm(pre)) if L(pre) > 0 else (pre, 1)
                B_REC[fid][name][s] = [x/255.0 for x in to255(col)]
        for name, alpha in (('EffectLightingColor', 'ALPHA_FX'), ('SkyStaticsColor', 'ALPHA_FX')):
            for s in CHG_SLOTS:
                t = SLOT_PEAK[s]
                Pn = norm(PIC[fid][name][s]); An = norm(AREC[PARTNER[fid]][name][s]) if L(AREC[PARTNER[fid]][name][s]) > 0 else [1, 1, 1]
                T = lerp(Pn, An, DIALS[alpha])
                col, kk = gamut_chroma(L(PIC[fid][name][s]), T)
                B_REC[fid][name][s] = [x/255.0 for x in to255(col)]
        # SkyLower: invisible under UseProceduralGradientWeights=true; carried for consistency (m=1, gamut-limited)
        for s in CHG_SLOTS:
            An = norm(AREC[PARTNER[fid]]['SkyLowerColor'][s]); T = lerp(norm(PIC[fid]['SkyLowerColor'][s]), An, DIALS['ALPHA_SKY'])
            col, kk = gamut_chroma(L(PIC[fid]['SkyLowerColor'][s]), T)
            B_REC[fid]['SkyLowerColor'][s] = [x/255.0 for x in to255(col)]
    return B_REC, B_E, design

B_REC, B_E, DESIGN = build_baby()
def B_out(name, fid, t, field=None): return lane_eval(name, B_REC[fid], B_E[FILE_OF[fid]], t, CLMT_P, TOD_P, field)
# naive = Astralite record colours dropped under Picta's live filters (what Route A avoids)
NAIVE_REC = {}
for fid in PIC:
    R = copy.deepcopy(PIC[fid]); A = AREC[PARTNER[fid]]
    for fld in ('SkyUpperColor', 'HorizonColor', 'FogFarColor', 'FogNearColor', 'SunlightColor', 'SunColor', 'CloudMain') + tuple('DALC.'+a for a in ('DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus')):
        for s in CHG_SLOTS: R[fld][s] = A[fld][s]
    NAIVE_REC[fid] = R
def N_out(name, fid, t, field=None): return lane_eval(name, NAIVE_REC[fid], E_P[FILE_OF[fid]], t, CLMT_P, TOD_P, field)

# ---------------- evaluation ----------------
TIMES = [5.5, 6.0, 6.5, 7.0, 7.25, 7.5, 8.0, 8.5, 9.0, 10.0, 12.0, 14.0, 16.0, 17.0, 17.5, 18.0, 18.5, 18.75, 19.0, 19.5, 20.0, 20.5]
CHS = [('top', None), ('hor', None), ('clouds', None), ('fog', 'FogFarColor'), ('sunlight', None), ('sun', None),
       ('DALC.DirectionalXPlus', None), ('DALC.DirectionalZMinus', None)]
lines = []
def P(s): lines.append(s)
P('FAITHFUL ASTRALITE - numeric model (pre-tonemap, Bottled 4ca678b chains). dials=' + json.dumps(DIALS))
P('Columns: luma ratio baby/picta (1.000 = brightness locked) | hue+HSV-sat of Picta now | BABY | ASTRALITE own lane at the phase-mapped clock | NAIVE (Astralite records under Picta filters)')
audit = {}
for fid in PIC:
    audit[fid] = {}
    for ch, fld in CHS:
        worst = 0.0
        for q in range(int(5.5*4), int(20.5*4)+1):
            t = q/4.0
            lp = L(P_out(ch, fid, t, fld)); lb = L(B_out(ch, fid, t, fld))
            if lp > 1e-6: worst = max(worst, abs(lb/lp-1))
        hd = []
        for s in CHG_SLOTS:
            t = SLOT_PEAK[s]
            hb = hsv(B_out(ch, fid, t, fld)); ha = hsv(A_out(ch, PARTNER[fid], phase_map(t), fld)); hp = hsv(P_out(ch, fid, t, fld))
            hd.append((round(hdist(hb[0], ha[0]), 1), round(hdist(hp[0], ha[0]), 1)))
        audit[fid][ch] = dict(max_luma_dev=round(worst, 4), hue_gap_to_astralite_baby_vs_picta=hd)
for fid in ('19FA01', '19FC01', '19FD02', '19FD03'):
    P(f"\n=========== {fid} {PIC[fid]['_edid']}  partner {AREC[PARTNER[fid]]['_edid']}  file {FILE_OF[fid]}")
    for ch, fld in CHS:
        P(f"-- {ch}")
        for t in TIMES:
            pc = P_out(ch, fid, t, fld); bc = B_out(ch, fid, t, fld); ac = A_out(ch, PARTNER[fid], phase_map(t), fld); nc = N_out(ch, fid, t, fld)
            r = L(bc)/L(pc) if L(pc) > 1e-9 else float('nan')
            P(f"  {t:5.2f}h luma {r:6.3f} | picta {hue_s(pc)} | BABY {hue_s(bc)} | astra {hue_s(ac)} | naive {hue_s(nc)} (naive luma x{(L(nc)/L(pc) if L(pc)>1e-9 else 0):.2f})")
    P('-- dome pixels (procedural top/horizon lerp + SkyScattering; view relative to the sun azimuth)')
    for t in (7.25, 7.5, 9.0, 12.0, 17.0, 18.5, 18.75):
        for vn, vd in VIEWS.items():
            pc = dome_eval(PIC[fid], E_P[FILE_OF[fid]], t, CLMT_P, TOD_P, vd)
            bc = dome_eval(B_REC[fid], B_E[FILE_OF[fid]], t, CLMT_P, TOD_P, vd)
            nc = dome_eval(NAIVE_REC[fid], E_P[FILE_OF[fid]], t, CLMT_P, TOD_P, vd)
            P(f"  {t:5.2f}h {vn:9s} luma {L(bc)/L(pc):6.3f} | picta {hue_s(pc)} | BABY {hue_s(bc)} | naive {hue_s(nc)}")
P('\n=========== ALL 28: max |luma(baby)/luma(picta)-1| over 05:30-20:30 per channel, and hue gap to Astralite at the 3 slot peaks (baby, picta)')
for fid in PIC:
    row = ' '.join(f"{ch}:{audit[fid][ch]['max_luma_dev']:.3f}" for ch, _ in CHS)
    P(f"{fid} {PIC[fid]['_edid'][16:]:28s} {row}")
P('\nhue gaps (deg) baby->astralite vs picta->astralite at Sunrise/Day/Sunset slot peaks:')
for fid in PIC:
    P(f"{fid} " + ' '.join(f"{ch}:{audit[fid][ch]['hue_gap_to_astralite_baby_vs_picta']}" for ch, _ in CHS[:6]))

# ---------------- design tables ----------------
def b255(c): return to255(c)
rec_out = {}
for fid in PIC:
    R = B_REC[fid]; o = {}
    for fld in ('SkyUpperColor', 'SkyLowerColor', 'HorizonColor', 'FogNearColor', 'FogFarColor', 'SunlightColor', 'SunColor', 'EffectLightingColor', 'SkyStaticsColor'):
        o[fld] = {s: (to255(PIC[fid][fld][s]), b255(R[fld][s])) for s in SLOTS}
    for ax in ('DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus'):
        o['DALC.'+ax] = {s: (to255(PIC[fid]['DALC.'+ax][s]), b255(R['DALC.'+ax][s])) for s in SLOTS}
    o['clouds'] = [{'layer': l['i'], 'tex': l['tex'], 'col': {s: (to255(PIC[fid]['_layers'][j]['col'][s]), b255(l['col'][s])) for s in SLOTS}} for j, l in enumerate(R['_layers'])]
    o['partner'] = AREC[PARTNER[fid]]['_edid'] + ' (' + PARTNER[fid] + ' as authored in Astralite ENB.esp)'
    rec_out[fid + ' ' + PIC[fid]['_edid']] = o
DESIGN['records'] = rec_out
DESIGN['m'] = {k: round(v, 4) for k, v in DESIGN['m'].items()}

# VOLI transplant: effective Astralite amplitude = VOLI.Intensity x GVR.Intensity(Soul, phase clock);
# baby VOLI intensity = that / Picta GVR.Intensity at the slot peak x VL_STRENGTH
voli = {}
for fid in PIC:
    A = AREC[PARTNER[fid]]; vr = A['_voli'] or {}
    row = {}
    for s in CHG_SLOTS:
        v = vr.get(s)
        if not v or not isinstance(v, dict): continue
        tP = SLOT_PEAK[s]; tA = phase_map(tP)
        gS = ini_at(E_S[PARTNER[fid]], 'GAMEVOLUMETRICRAYS.Intensity', tod_weights(tA, TOD_A))
        gP = ini_at(E_P[FILE_OF[fid]], 'GAMEVOLUMETRICRAYS.Intensity', tod_weights(tP, TOD_P))
        inten = v.get('intensity')
        new = inten*gS/gP*DIALS['VL_STRENGTH'] if (inten and gP) else None
        row[s] = dict(astralite_voli=v.get('editorid'), formid=v.get('formid'), rgb255=v.get('color_rgb255'), cc=v.get('custom_color_contribution'),
                      density=v.get('density_contribution'), astra_intensity=inten, soul_gvr=round(gS, 3), picta_gvr=round(gP, 3),
                      baby_intensity=round(new, 3) if new else None)
    voli[fid + ' ' + PIC[fid]['_edid']] = row
DESIGN['voli'] = voli

# fog distance: add-only log blend of the EFFECTIVE far distance toward the partner's effective (record / Soul FAM)
fogd = {}
EFF = {r['editorid']: r for r in json.load(open(SCR + '/map/fog-mist/effective_fog_after_e11.json'))}
for fid in PIC:
    f = FILE_OF[fid]; A = AREC[PARTNER[fid]]; pe = PIC[fid]['_fog']
    famD = ini_at(E_P[f], 'ENVIRONMENT.FogAmountMultiplier', {'Day': 1.0}); famN = ini_at(E_P[f], 'ENVIRONMENT.FogAmountMultiplier', {'Night': 1.0})
    fcmD = ini_at(E_P[f], 'ENVIRONMENT.FogCurveMultiplier', {'Day': 1.0})
    ae = EFF.get(A['_edid'])
    row = {}
    for dn, fam in (('Day', famD), ('Night', famN)):
        pf = pe[f'FogDistance{dn}Far']/fam
        af = (ae[f'{dn.lower()}_far'] if ae else None)
        if af and af < pf:
            nf = math.exp(lerp(math.log(pf), math.log(af), DIALS['FOG_DENSITY']))
            row[dn] = dict(picta_eff_far=round(pf), astra_eff_far=round(af), baby_eff_far=round(nf), record_far=round(nf*fam),
                           record_far_was=pe[f'FogDistance{dn}Far'], power_kept=pe[f'FogDistance{dn}Power'])
        else:
            row[dn] = dict(picta_eff_far=round(pf), astra_eff_far=round(af) if af else None, action='keep (Picta already denser or equal)')
    fogd[fid + ' ' + PIC[fid]['_edid']] = row
DESIGN['fog_distance'] = fogd

json.dump(DESIGN, open(OUT + '/design_values.json', 'w'), indent=1, default=str)
json.dump(audit, open(OUT + '/luma_audit.json', 'w'), indent=1)
open(OUT + '/model_out.txt', 'w').write('\n'.join(lines))
print('\n'.join(lines[:3])); print('written', OUT)
