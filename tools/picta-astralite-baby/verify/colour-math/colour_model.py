"""Independent colour/brightness model on the INSTALLED files (read-only on C:/1. AUTHORIA; writes only to this folder).

Picta lane : E11 = 'Authoria - Picta 1.1.2 - Darkened to 1.0.1' (VFS-checked: PICTA's effective E11 bytes), WTHR = PICTA winners
Baby lane  : E11 = installed 'Authoria - Picta x Astralite - E11', WTHR = installed ESL (houseCARL source= read)
E11 read with GetPrivateProfileStringA + registration defaults/clamps (e11read.py). Formulas from Effects11.cpp OverrideWeather,
UpdateSkyScattering, Sky.hlsl, SkyScattering.hlsli ApplySkyScattering/ShadeCloud, Effects11.cpp OverrideAmbientLighting,
ISCompositeLensFlareVolumetricLighting.hlsl.
"""
import json, math, os, re, sys, itertools
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from e11read import E11, tod_weights, gpps, PER

DARK = r'C:\1. AUTHORIA\mods\Authoria - Picta 1.1.2 - Darkened to 1.0.1'
FORK = r'C:\1. AUTHORIA\mods\Authoria - Picta x Astralite - E11'
LUM = np.array([0.2126, 0.7152, 0.0722])
SL = ['Sunrise', 'Day', 'Sunset', 'Night']
AX = ['DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus']
PICTA_CL = (6.0, 9.0, 17.0, 20.0)
FAIR_CL = (5.5, 10.0, 16.0, 20.5)
FAIR_W = {'19FA01', '19FA02', '19FB02', '19FC01'}


def Y(c):
    return float(LUM @ np.asarray(c, float))


def T_of(base):
    return {k: float(gpps(base, 'TIMEOFDAY', k)) for k in ('NightTime', 'SunriseTime', 'DawnDuration', 'DayTime', 'SunsetTime', 'DuskDuration')}


# ---------------------------------------------------------------- records
def _rgb(s):
    return np.array([float(x) for x in s.split(',')[:3]]) / 255.0


def load_records():
    D = json.load(open(os.path.join(H, 'wthr_pair.json')))
    out = {}
    for lane in ('P', 'B'):
        out[lane] = {}
        for w, f in D[lane].items():
            R = {}
            layers = sorted({int(m.group(1)) for k, v in f.items() for m in [re.match(r'Clouds\[(\d+)\]\.Enabled$', k)] if m and v == 'True'})
            for s in SL:
                R[s] = dict(upper=_rgb(f['SkyUpperColor.' + s]), horizon=_rgb(f['HorizonColor.' + s]), fogfar=_rgb(f['FogFarColor.' + s]),
                            fognear=_rgb(f['FogNearColor.' + s]), sun=_rgb(f['SunColor.' + s]), sunlight=_rgb(f['SunlightColor.' + s]),
                            clouds=[_rgb(f[f'Clouds[{i}].Colors.{s}']) for i in layers],
                            dalc={a: _rgb(f[f'DirectionalAmbientLightingColors.{s}.{a}']) for a in AX},
                            voli=f['VolumetricLighting.' + s])
            R['_layers'] = layers
            out[lane][w] = R
    return out


def load_voli():
    V = {}
    for fn in ('picta_voli.jsonl', 'baby_voli.jsonl'):
        for l in open(os.path.join(H, fn), encoding='utf-8').read().splitlines()[1:]:
            r = json.loads(l)
            d = {x['path']: x.get('value', x.get('note')) for x in r['fields']}
            V[r['formid']] = dict(I=float(d['Intensity']), cc=float(d['CustomColorContribution']),
                                  col=np.array([float(d['ColorR']), float(d['ColorG']), float(d['ColorB'])]),
                                  dens=float(d['DensityContribution']), rf=float(d['SamplingRepartitionRangeFactor']), name=r['editorid'])
    return V


# ---------------------------------------------------------------- climate / sun
def clmt_mid(h, C):
    h = h % 24
    rb, re_, sb, se = C
    rm, sm = (rb + re_) / 2, (sb + se) / 2
    w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)
    if h < rb or h >= se:
        w['Night'] = 1
    elif h < rm:
        t = (h - rb) / (rm - rb); w['Night'] = 1 - t; w['Sunrise'] = t
    elif h < re_:
        t = (h - rm) / (re_ - rm); w['Sunrise'] = 1 - t; w['Day'] = t
    elif h < sb:
        w['Day'] = 1
    elif h < sm:
        t = (h - sb) / (sm - sb); w['Day'] = 1 - t; w['Sunset'] = t
    else:
        t = (h - sm) / (se - sm); w['Sunset'] = 1 - t; w['Night'] = t
    return w


def clmt_plateau(h, C):
    h = h % 24
    rb, re_, sb, se = C
    w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)

    def win(a, b, s0, s1, s2):
        L = (b - a) / 3
        if h < a + L:
            t = (h - a) / L; w[s0] = 1 - t; w[s1] = t
        elif h < a + 2 * L:
            w[s1] = 1
        else:
            t = (h - a - 2 * L) / L; w[s1] = 1 - t; w[s2] = t
    if h < rb or h >= se:
        w['Night'] = 1
    elif h < re_:
        win(rb, re_, 'Night', 'Sunrise', 'Day')
    elif h < sb:
        w['Day'] = 1
    else:
        win(sb, se, 'Day', 'Sunset', 'Night')
    return w


def sunz(h, up, dn):
    h = h % 24
    if up <= h <= dn:
        e = math.radians(60) * math.sin(math.pi * (h - up) / (dn - up))
    else:
        d = min(abs(h - up), abs(h - dn), abs(h + 24 - up), abs(h - 24 - dn))
        e = -math.radians(12) * min(1, d / 1.5)
    return math.sin(e)


# ---------------------------------------------------------------- E11 evaluation
class Ctx:
    def __init__(self, e11, T):
        self.e, self.T = e11, T

    def g(self, cat, key, h):
        w = tod_weights(h, self.T)
        vals = self.e.get(cat, key)
        acc = 0.0
        for p, wp in w.items():
            if wp > 0:
                acc = acc + wp * np.asarray(vals[p], float)
        return acc


def rat(R, h, cw, C, key, ax=None, layer=None):
    w = cw(h, C)
    acc = np.zeros(3)
    for s in SL:
        if w[s] > 0:
            v = R[s]['dalc'][ax] if key == 'dalc' else (R[s]['clouds'][layer] if key == 'clouds' else R[s][key])
            acc = acc + w[s] * v
    return acc


def curve(c, p):
    return np.maximum(c, 0) ** p


def desat(c, d):
    c = np.asarray(c, float)
    return np.maximum(c + (c.mean() - c) * d, 0)


def comps(X, R, h, cw, C, sz):
    """every on-screen colour component at hour h for one lane."""
    g = lambda cat, k: X.g(cat, k, h)
    o = {}
    GI, GD = g('SKY', 'GradientIntensity'), g('SKY', 'GradientDesaturation')
    for nm, rk, key in (('top', 'upper', 'GradientTop'), ('hor', 'horizon', 'GradientHorizon')):
        c = curve(rat(R, h, cw, C, rk), g('SKY', key + 'Curve')) * g('SKY', key + 'ColorFilter')
        o['band_' + nm] = desat(c * g('SKY', key + 'Intensity') * GI, GD)
    sun = desat(rat(R, h, cw, C, 'sun'), g('SKY', 'SunDesaturation')) * g('SKY', 'SunColorFilter')
    sunN = np.maximum(sun, 0) / max(sun.max(), 1.0)
    sunFade = math.sqrt(min(1, max(0, 1 + 2 * sz)))
    color = (1 + (sunN - 1) * g('SKYSCATTERING', 'ColorFromSun')) * g('SKYSCATTERING', 'ScatteringColor') * sunFade
    peak = max(color.max(), 1e-6)
    dd = g('SKYSCATTERING', 'DustDensity')
    tint = np.maximum(0, 1 - color / peak) * 2 * dd * dd
    dustVol = 0.02 / max(g('SKYSCATTERING', 'DustVolume') ** 2, 1e-7)
    inten = g('SKYSCATTERING', 'Intensity')
    amt2 = g('SKYSCATTERING', 'Amount') ** 2
    hr = 1 / max(g('SKYSCATTERING', 'HorizonRange') ** 3, 1e-6)
    at = 100 / max(g('SKYSCATTERING', 'AtmosphereThickness') ** 2, 1e-6)
    agI, agR = g('SKYSCATTERING', 'AirGlowIntensity'), 1 / max(g('SKYSCATTERING', 'AirGlowRange') ** 2, 1e-6)
    sgI, sgR = g('SKYSCATTERING', 'SunGlowIntensity'), 10 / max(g('SKYSCATTERING', 'SunGlowRange') ** 2, 1e-6)
    shA = min(1, max(0, g('SKYSCATTERING', 'ShadowAmount')))
    ddk = g('SKYSCATTERING', 'DustDarkening')
    pgc = g('SKY', 'ProceduralGradientWeightCurve')

    def elev(z):
        return 1 - min(1, max(0, 1 - z)) * min(1, max(0, 1 + sz))

    def dband(el):
        return min(1, max(0, 1 - el * dustVol)) ** 32

    def scol(bd):
        return color * inten * np.clip(1 - bd * tint, 0, 1) ** 32

    def eshadow(el, fa):
        tw = 0.1 - sz
        th = (0.8 + 0.3 * min(1, max(0, tw * 5))) * (1 - fa) + (0.95 + min(1, max(0, sz * -0.5))) * fa
        sp = min(1, max(0, 1 - tw * 3))
        s_ = min(1, max(0, 1 + el - th)) * (4 * (0.1 + sp * sp)) * (1 + fa * 4)
        s_ = min(1, max(0, s_)); s_ = s_ * s_ * (3 - 2 * s_)
        return s_ * s_ * (3 - 2 * s_)
    cz = math.sqrt(max(0, 1 - sz * sz))
    sd = np.array([0, cz, sz])
    top, hz = o['band_top'], o['band_hor']
    for vn, z, toward in (('zenith', 1.0, 1), ('hor_sun', .05, 1), ('hor_away', .05, -1), ('mid_away', .44, -1), ('mid_sun', .2, 1)):
        v = np.array([0, toward * math.sqrt(1 - z * z), z])
        sky = top + (hz - top) * (1 - min(1, max(0, z))) ** pgc
        fa = min(1, max(0, float(v @ sd) * 0.5 + 0.5)); aw = 1 - fa
        el = elev(z); bd = dband(el)
        aboveH = min(1, max(0, 1 + z * 10)) ** 2
        sunAbove = min(1, max(0, 1 + z * 40)) ** 2
        spread = hr * aw * aw + (at - hr * aw * aw) * el * el
        sc = scol(bd) * (aboveH * (1 - bd * ddk))
        res = sky * (1 + agI / (1 + aw * agR))
        res = res + (sc - res) * min(1, max(0, amt2 / (1 + aw * spread)))
        res = res * (1 + sgI * sunAbove / (1 + aw * sgR))
        sh = 1 + (eshadow(el, fa) - 1) * shA
        o['dome_' + vn] = sky + ((top * 0.5 + (res - top * 0.5) * sh) - sky) * aboveH
        if vn == 'hor_sun':
            o['sunglow_hor'] = sc
    cc = g('SKY', 'CloudsCurve')
    tex = 0.7
    sunAt = scol(dband(elev(sz))) * min(1, amt2)  # GetScatteringColorAt(sunDir)
    o['scat_at_sun'] = sunAt
    sunAt_d = desat(sunAt, float(np.clip(g('SKYSCATTERING', 'CloudsLightingDesaturation'), -1, 1)))
    clsi = g('SKY', 'CloudsIntensity') * g('SKYSCATTERING', 'CloudsLightingSunMultiplier') + g('SKYSCATTERING', 'CloudsLightingSunMinIntensity')
    gray = tex ** cc
    for li in range(len(R['_layers'])):
        base = desat(curve(rat(R, h, cw, C, 'clouds', layer=li) * tex, cc), g('SKY', 'CloudsDesaturation')) * g('SKY', 'CloudsIntensity') * g('SKY', 'CloudsColorFilter')
        o[f'cloud_base_L{R["_layers"][li]}'] = base
        o[f'cloud_sunlit_L{R["_layers"][li]}'] = base + sunAt_d * gray * max(float(clsi), 0.0)
        # rim (CalculateCloudsEdgeFromScattering=true): scattering at view~sun * SunIntensity * mean(cloudColor)
        o[f'cloud_rim_L{R["_layers"][li]}'] = sunAt * g('SKY', 'SunIntensity') * float(np.mean(base))
    fc, ff, fa_, fm = g('ENVIRONMENT', 'FogColorCurve'), g('ENVIRONMENT', 'FogColorFilter'), g('ENVIRONMENT', 'FogColorFilterAmount'), g('ENVIRONMENT', 'FogColorMultiplier')
    for nm, rk in (('fog_far', 'fogfar'), ('fog_near', 'fognear')):
        c = curve(rat(R, h, cw, C, rk), fc)
        o[nm] = (c + (1 - c) * fa_) * ff * fm
    L = curve(rat(R, h, cw, C, 'sunlight'), g('ENVIRONMENT', 'DirectLightingCurve'))
    L = desat(L, g('ENVIRONMENT', 'DirectLightingDesaturation'))
    a = g('ENVIRONMENT', 'DirectLightingColorFilterAmount')
    L = (L + (1 - L) * a) * g('ENVIRONMENT', 'DirectLightingColorFilter') * g('ENVIRONMENT', 'DirectLightingIntensity')
    o['sunlight'] = L
    ad, ai = g('ENVIRONMENT', 'AmbientLightingDesaturation'), g('ENVIRONMENT', 'AmbientLightingIntensity')
    for axn in AX:
        o['amb_' + axn[11:]] = desat(rat(R, h, cw, C, 'dalc', axn), ad) * ai
    o['_gvr_I'] = float(g('GAMEVOLUMETRICRAYS', 'Intensity'))
    o['_gvr_F'] = g('GAMEVOLUMETRICRAYS', 'ColorFilter')
    o['_gvr_D'] = float(g('GAMEVOLUMETRICRAYS', 'Desaturation'))
    o['_gvr_R'] = float(g('GAMEVOLUMETRICRAYS', 'RangeFactor'))
    return o


def vl(o, R, V, h, cw, C):
    """intensity-only VL radiance relative to the key light: I_voli * GVR_I * Y(desat(lerp(L, col, cc)) * GVR_F) / Y(L)."""
    w = cw(h, C)
    I_ = cc = 0.0
    col = np.zeros(3)
    dens = 0.0
    for s in SL:
        v = V[R[s]['voli']]
        I_ += w[s] * v['I']; cc += w[s] * v['cc']; col = col + w[s] * v['col']; dens += w[s] * v['dens']
    L = o['sunlight']
    c = L + (col - L) * cc
    c = desat(c, o['_gvr_D']) * o['_gvr_F']
    return I_ * o['_gvr_I'] * Y(c) / max(Y(L), 1e-9), dens


def weather_files(fork):
    WL = {}
    p = os.path.join(fork, 'enbseries', '_weatherlist.ini')
    txt = open(chr(92) * 2 + '?' + chr(92) + p, 'rb').read().decode('utf-8', 'replace')
    for m in re.finditer(r'\[(WEATHER\d+)\]\s*\r?\nFileName=(.+?)\r?\nWeatherIDs=(.+?)\r?\n', txt):
        sec, fn, ids = m.group(1), m.group(2).strip(), [x.strip() for x in m.group(3).split(',')]
        for i in ids:
            WL.setdefault(i, fn)   # first section wins for an ID listed twice
    return WL
