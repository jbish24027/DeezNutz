"""Independent re-implementation of the Bottled 4ca678b colour chain, run on the WRITTEN stage files
(alive branch) vs the live Picta Darkened files. Read-only on C:/1. AUTHORIA.
Written from the source (Effects11.cpp OverrideWeather 557-737, UpdateSkyScattering 164-213,
Sky.hlsl 360-436, SkyScattering.hlsli, ISCompositeLensFlareVolumetricLighting.hlsl 35-41,
EffectManager.cpp 921-1000, SettingManager.cpp ResolveWeatherValue 167-195), not from final_model.py.
"""
import json, re, math, os, sys
import numpy as np

S = 'C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby'
DARK = 'C:/1. AUTHORIA/mods/Authoria - Picta 1.1.2 - Darkened to 1.0.1'
STAGE = S + '/design/finalize/stage/alive/Authoria - Picta x Astralite - E11'
OUT = S + '/design/finalize'
PER = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night', 'InteriorDay', 'InteriorNight']
LUM = np.array([0.2126, 0.7152, 0.0722])
def Y(c): return float(LUM @ np.asarray(c, float))

def parse(path):
    lp = chr(92) * 2 + '?' + chr(92) + os.path.abspath(path).replace('/', chr(92))
    t = open(lp, 'rb').read().decode('utf-8', 'replace'); D = {}; sec = None
    for l in t.splitlines():
        s = l.strip(); m = re.match(r'^\[(.+)\]$', s)
        if m: sec = m.group(1); D.setdefault(sec, {}); continue
        if sec and '=' in s and not s.startswith(';'):
            k, v = s.split('=', 1); D[sec][k.strip()] = v.strip()
    return D
def val(s):
    s = s.strip()
    if ',' in s: return np.array([float(x) for x in s.split(',')[:3]])
    try: return float(s)
    except ValueError: return None

class Ini:
    """weather file over base: per-period fallback (ResolveWeatherValue)."""
    def __init__(self, wpath, bpath):
        self.W = parse(wpath); self.B = parse(bpath)
    def get(self, sec, key, p):
        k = key + p
        if k in self.W.get(sec, {}): return val(self.W[sec][k])
        if k in self.B.get(sec, {}): return val(self.B[sec][k])
        return None

BASE = parse(DARK + '/enbseries.ini')['TIMEOFDAY']
T = {k: float(v) for k, v in BASE.items()}
def tod(h):
    h = h % 24
    nt, sr, dd, dt, ss, ud = T['NightTime'], T['SunriseTime'], T['DawnDuration'], T['DayTime'], T['SunsetTime'], T['DuskDuration']
    tp = [nt, sr - dd, sr - dd * 0.5, sr, dt, ss, ss + ud * 0.5, ss + ud]
    tp = tp + [x + 24 for x in tp]
    fm = ['Night', 'Night', 'Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
    ci = ni = 0; cpt = 0.0; npt = 24.0
    for i, t in enumerate(tp):
        if h >= t and t >= cpt: ci, cpt = i, t
        if t > h and npt >= t: ni, npt = i, t
    cf, nf = fm[ci % 8], fm[ni % 8]
    td = abs(npt - cpt) or 1.0; b = abs(h - cpt) / td
    f = {p: 0.0 for p in PER[:6]}
    if cf == nf: f[cf] = 1.0
    else: f[cf] = min(1, max(0, 1 - b)); f[nf] = min(1, max(0, b))
    pd = min(1.0, max(0.0, f['Day'] ** 0.6))
    if pd > 1.17549435e-38:
        if f['Sunrise'] > 1.17549435e-38: f['Sunrise'] = 1 - pd
        if f['Sunset'] > 1.17549435e-38: f['Sunset'] = 1 - pd
    f['Day'] = pd
    return f
def ev(ini, sec, key, h, ovr=None, default=None):
    w = tod(h); acc = 0.0
    for p, wp in w.items():
        if wp <= 0: continue
        v = ini.get(sec, key, p)
        if v is None: v = default
        acc = acc + wp * np.asarray(v, float)
    return acc

# record clock (CLMT) - two candidate engine rules
CL = (6.0, 9.0, 17.0, 20.0)
def clmt_mid(h):
    rb, re_, sb, se = CL; rm, sm = (rb + re_) / 2, (sb + se) / 2
    w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)
    if h < rb or h >= se: w['Night'] = 1
    elif h < rm: t = (h - rb) / (rm - rb); w['Night'] = 1 - t; w['Sunrise'] = t
    elif h < re_: t = (h - rm) / (re_ - rm); w['Sunrise'] = 1 - t; w['Day'] = t
    elif h < sb: w['Day'] = 1
    elif h < sm: t = (h - sb) / (sm - sb); w['Day'] = 1 - t; w['Sunset'] = t
    else: t = (h - sm) / (se - sm); w['Sunset'] = 1 - t; w['Night'] = t
    return w
def clmt_plateau(h):
    """alternative: colours hold their slot over the middle third of each window."""
    rb, re_, sb, se = CL; w = dict(Sunrise=0.0, Day=0.0, Sunset=0.0, Night=0.0)
    def win(a, b, s0, s1, s2):
        L = (b - a) / 3
        if h < a + L: t = (h - a) / L; w[s0] = 1 - t; w[s1] = t
        elif h < a + 2 * L: w[s1] = 1
        else: t = (h - a - 2 * L) / L; w[s1] = 1 - t; w[s2] = t
    if h < rb or h >= se: w['Night'] = 1
    elif h < re_: win(rb, re_, 'Night', 'Sunrise', 'Day')
    elif h < sb: w['Day'] = 1
    else: win(sb, se, 'Day', 'Sunset', 'Night')
    return w

def sunz_A(h):  # same shape the design used: up 7.5, down 18.5, peak 60
    up, dn = 7.5, 18.5
    if up <= h <= dn: e = math.radians(60) * math.sin(math.pi * (h - up) / (dn - up))
    else:
        d = min(abs(h - up), abs(h - dn)); e = -math.radians(12) * min(1, d / 1.5)
    return math.sin(e)
def sunz_B(h):  # alternative: up 6.0, down 20.0
    up, dn = 6.0, 20.0
    if up <= h <= dn: e = math.radians(60) * math.sin(math.pi * (h - up) / (dn - up))
    else:
        d = min(abs(h - up), abs(h - dn)); e = -math.radians(12) * min(1, d / 1.5)
    return math.sin(e)

PR = json.load(open(S + '/map/picta-colour/picta_wthr_colours.json'))
RM = json.load(open(S + '/design/finalize/records_manifest.json'))
AX = ['DirectionalXPlus', 'DirectionalXMinus', 'DirectionalYPlus', 'DirectionalYMinus', 'DirectionalZPlus', 'DirectionalZMinus']
SL = ['Sunrise', 'Day', 'Sunset', 'Night']
def recs(fid, baby):
    x = PR[fid + ':Picta - Weathers of Aurbis.esm']; c = x['colours']
    R = {s: {k: np.array(c[k][s], float) / 255 for k in ('SkyUpperColor', 'HorizonColor', 'FogNearColor', 'FogFarColor', 'SunColor', 'SunlightColor')} for s in SL}
    cl = (x.get('clouds_enabled') or [])
    for s in SL:
        R[s]['cloud'] = np.array(cl[0]['colors'][s], float) / 255 if cl else np.ones(3)
        R[s]['dalc'] = {a: np.array(c['DALC'][s][a], float) / 255 for a in AX}
    if baby:
        for op in RM['overrides'][fid + ':Picta - Weathers of Aurbis.esm']['ops']:
            m = re.match(r'DirectionalAmbientLightingColors\.(\w+)\.(\w+)$', op['field'])
            if m: R[m.group(1)]['dalc'][m.group(2)] = np.array(op['new'], float) / 255
    R['_voli'] = x['voli']
    return R
def rat(R, h, key, cw, ax=None):
    w = cw(h); acc = np.zeros(3)
    for s in SL:
        if w[s] > 0: acc = acc + w[s] * (R[s]['dalc'][ax] if key == 'dalc' else R[s][key])
    return acc

def Curve(c, p): return np.maximum(c, 0) ** p
def Desat(c, d): return np.maximum(c + (c.mean() - c) * d, 0)

def comps(ini, R, h, cw, sz_fn):
    g = lambda sec, k, d=None: ev(ini, sec, k, h, default=d)
    out = {}
    GI = g('SKY', 'GradientIntensity'); GD = g('SKY', 'GradientDesaturation')
    for nm, rk, key in (('top', 'SkyUpperColor', 'GradientTop'), ('hor', 'HorizonColor', 'GradientHorizon')):
        c = Curve(rat(R, h, rk, cw), g('SKY', key + 'Curve')) * g('SKY', key + 'ColorFilter', np.ones(3))
        c = c * g('SKY', key + 'Intensity') * GI
        out['band_' + nm] = Desat(c, GD)
    # sun disc / scattering colour (Effects11.cpp 634-647, 180-197)
    sun = Desat(rat(R, h, 'SunColor', cw), g('SKY', 'SunDesaturation', 0.0)) * g('SKY', 'SunColorFilter', np.ones(3))
    sunN = np.maximum(sun, 0) / max(sun.max(), 1.0)
    sz = sz_fn(h); sunFade = math.sqrt(min(1, max(0, 1 + 2 * sz)))
    cfs = g('SKYSCATTERING', 'ColorFromSun'); scol = g('SKYSCATTERING', 'ScatteringColor', np.ones(3))
    color = (1 + (sunN - 1) * cfs) * scol * sunFade
    peak = max(color.max(), 1e-6); dd = g('SKYSCATTERING', 'DustDensity', 0.0)
    tint = np.maximum(0, 1 - color / peak) * 2 * dd * dd
    dustVol = 0.02 / max(g('SKYSCATTERING', 'DustVolume') ** 2, 1e-7)
    inten = g('SKYSCATTERING', 'Intensity'); amt2 = g('SKYSCATTERING', 'Amount') ** 2
    def elevation(z): return 1 - min(1, max(0, 1 - z)) * min(1, max(0, 1 + sz))
    def band(el): return min(1, max(0, 1 - el * dustVol)) ** 32
    def scatcol(bd): return color * inten * np.clip(1 - bd * tint, 0, 1) ** 32
    cz = math.sqrt(max(0, 1 - sz * sz)); sd = np.array([0, cz, sz])
    # sky dome pixels (Sky.hlsl 373-380 + ApplySkyScattering)
    pgc = g('SKY', 'ProceduralGradientWeightCurve')
    hr = 1 / max(g('SKYSCATTERING', 'HorizonRange') ** 3, 1e-6); at = 100 / max(g('SKYSCATTERING', 'AtmosphereThickness') ** 2, 1e-6)
    agI = g('SKYSCATTERING', 'AirGlowIntensity'); agR = 1 / max(g('SKYSCATTERING', 'AirGlowRange') ** 2, 1e-6)
    sgI = g('SKYSCATTERING', 'SunGlowIntensity'); sgR = 10 / max(g('SKYSCATTERING', 'SunGlowRange') ** 2, 1e-6)
    shA = min(1, max(0, g('SKYSCATTERING', 'ShadowAmount', 0.0))); ddk = g('SKYSCATTERING', 'DustDarkening', 0.0)
    def es(el, fa, sh):
        tw = 0.1 - sh; th = (0.8 + 0.3 * min(1, max(0, tw * 5))) * (1 - fa) + (0.95 + min(1, max(0, sh * -0.5))) * fa
        sp = min(1, max(0, 1 - tw * 3)); s_ = min(1, max(0, 1 + el - th)) * (4 * (0.1 + sp * sp)) * (1 + fa * 4)
        s_ = min(1, max(0, s_)); s_ = s_ * s_ * (3 - 2 * s_); return s_ * s_ * (3 - 2 * s_)
    top, hz = out['band_top'], out['band_hor']
    for vn, v in (('zenith', np.array([0, 0, 1.0])), ('hor_sun', np.array([0, math.sqrt(1 - .0025), .05])),
                  ('hor_away', np.array([0, -math.sqrt(1 - .0025), .05])), ('mid_away', np.array([0, -math.sqrt(1 - .44 ** 2), .44])),
                  ('mid_sun', np.array([0, math.sqrt(1 - .2 ** 2), .2]))):
        z = v[2]; sky = top + (hz - top) * (1 - min(1, max(0, z))) ** pgc
        fa = min(1, max(0, float(v @ sd) * 0.5 + 0.5)); aw = 1 - fa; el = elevation(z); bd = band(el)
        aboveH = min(1, max(0, 1 + z * 10)) ** 2; sunAbove = min(1, max(0, 1 + z * 40)) ** 2
        spread = hr * aw * aw + (at - hr * aw * aw) * el * el
        sc = scatcol(bd) * (aboveH * (1 - bd * ddk))
        res = sky * (1 + agI / (1 + aw * agR))
        res = res + (sc - res) * min(1, max(0, amt2 / (1 + aw * spread)))
        res = res * (1 + sgI * sunAbove / (1 + aw * sgR))
        sh = 1 + (es(el, fa, sz) - 1) * shA
        out['dome_' + vn] = sky + ((top * 0.5 + (res - top * 0.5) * sh) - sky) * aboveH
        if vn == 'hor_sun': out['scat_sunward'] = sc
    # clouds (Sky.hlsl 423-426: curve -> desat -> *Intensity*Filter) + ShadeCloud sun term (SkyScattering.hlsli 218-228)
    cc = g('SKY', 'CloudsCurve'); tex = 0.7
    cloud = Curve(rat(R, h, 'cloud', cw) * tex, cc)
    cloud = Desat(cloud, g('SKY', 'CloudsDesaturation', 0.0)) * g('SKY', 'CloudsIntensity') * g('SKY', 'CloudsColorFilter', np.ones(3))
    out['cloud_base'] = cloud
    clsi = g('SKY', 'CloudsIntensity') * g('SKYSCATTERING', 'CloudsLightingSunMultiplier', 0.0) + g('SKYSCATTERING', 'CloudsLightingSunMinIntensity', 0.0)
    elS = elevation(sz)  # view = sun direction
    sunLight = Desat(scatcol(band(elS)) * min(1, amt2), float(np.clip(g('SKYSCATTERING', 'CloudsLightingDesaturation', 0.0), -1, 1)))
    gray = tex ** cc
    out['cloud_sunlit'] = cloud + sunLight * (gray * max(clsi, 0.0))
    out['_cloud_lit_share'] = Y(sunLight * gray * max(clsi, 0.0)) / max(Y(out['cloud_sunlit']), 1e-12)
    # fog
    fc = g('ENVIRONMENT', 'FogColorCurve'); ff = g('ENVIRONMENT', 'FogColorFilter', np.ones(3)); fa_ = g('ENVIRONMENT', 'FogColorFilterAmount', 0.0); fm = g('ENVIRONMENT', 'FogColorMultiplier')
    for nm, rk in (('fog_far', 'FogFarColor'), ('fog_near', 'FogNearColor')):
        c = Curve(rat(R, h, rk, cw), fc); out[nm] = (c + (1 - c) * fa_) * ff * fm
    # direct light (sunlightScale cancels when DirectLightingCurve==1)
    L = Curve(rat(R, h, 'SunlightColor', cw), g('ENVIRONMENT', 'DirectLightingCurve'))
    L = Desat(L, g('ENVIRONMENT', 'DirectLightingDesaturation', 0.0))
    a = g('ENVIRONMENT', 'DirectLightingColorFilterAmount', 0.0)
    L = (L + (1 - L) * a) * g('ENVIRONMENT', 'DirectLightingColorFilter', np.ones(3)) * g('ENVIRONMENT', 'DirectLightingIntensity')
    out['sunlight'] = L
    # ambient
    ad = g('ENVIRONMENT', 'AmbientLightingDesaturation', 0.0); ai = g('ENVIRONMENT', 'AmbientLightingIntensity')
    for axn in AX: out['amb_' + axn[11:]] = Desat(rat(R, h, 'dalc', cw, axn), ad) * ai
    # GVR colour stage (shader 37-38) applied to the graded key light only (custom colour 0 for Picta VOLIs)
    gd = g('GAMEVOLUMETRICRAYS', 'Desaturation', 0.0); gf = g('GAMEVOLUMETRICRAYS', 'ColorFilter', np.ones(3))
    out['vl_keylight_x_filter'] = Desat(L, gd) * gf * g('GAMEVOLUMETRICRAYS', 'Intensity')
    out['_gvr_range'] = float(g('GAMEVOLUMETRICRAYS', 'RangeFactor'))
    out['_sz'] = sz
    return out

WL = parse(DARK + '/enbseries/_weatherlist.ini')
FILES = {}
for sec, d in WL.items():
    fn = d.get('FileName', '')
    if (fn.startswith('Picta - Weathers/00_Master/') or fn.startswith('Authoria - Summer/')) and sec != 'WEATHER901':
        FILES[fn] = [x.strip() for x in d['WeatherIDs'].split(',')]

HOURS = [5.0 + 0.25 * i for i in range(67)]
NIGHT = [20.5 + 0.25 * i for i in range(37)]
def run(cw, sz_fn, label):
    worst = {}; nightmax = 0.0; rows = {}
    for fn, ids in FILES.items():
        iP = Ini(DARK + '/enbseries/' + fn, DARK + '/enbseries.ini'); iB = Ini(STAGE + '/enbseries/' + fn, STAGE + '/enbseries.ini')
        for w in ids:
            RP, RB = recs(w, False), recs(w, True)
            for h in HOURS + NIGHT:
                a = comps(iP, RP, h % 24, cw, sz_fn); b = comps(iB, RB, h % 24, cw, sz_fn)
                for k in a:
                    if k.startswith('_'): continue
                    ya = Y(a[k])
                    if h >= 20.5 and (h % 24 >= 20.5 or h % 24 <= 5.5):
                        nightmax = max(nightmax, float(np.abs(a[k] - b[k]).max()))
                        if h % 24 not in (21.0,): pass
                    if h not in HOURS or ya < 1e-7: continue
                    d = Y(b[k]) / ya - 1
                    if k not in worst or abs(d) > abs(worst[k][0]): worst[k] = (d, h, w)
                rows.setdefault(w, {})[h] = (a, b)
    return worst, nightmax, rows

if __name__ == '__main__':
    res = {}
    for lab, cw, sf in (('mid+sunA', clmt_mid, sunz_A), ('plateau+sunA', clmt_plateau, sunz_A), ('mid+sunB', clmt_mid, sunz_B)):
        worst, nm, rows = run(cw, sf, lab)
        print(f'== {lab}: night max abs diff {nm:.3g}')
        for k, (d, h, w) in sorted(worst.items(), key=lambda kv: -abs(kv[1][0])):
            print(f'   {k:22s} {100 * d:+7.2f}%  @{h:5.2f}  {w}')
        res[lab] = {k: [round(100 * d, 3), h, w] for k, (d, h, w) in worst.items()}
        if lab == 'mid+sunA':
            # cloud lit share and GVR range/colour in crossfades for A01 / D03
            for w in ('19FA01', '19FC01', '19FD03', '19FE05'):
                for h in (5.5, 6.0, 6.5, 7.0, 7.5, 13.0, 18.5, 19.5, 20.0, 20.25):
                    a, b = rows[w][h]
                    print(f'   {w} {h:5.2f} cloudlit share P {a["_cloud_lit_share"]:.3f} B {b["_cloud_lit_share"]:.3f} | GVR range P {a["_gvr_range"]:.3f} B {b["_gvr_range"]:.3f} | VLkey x filter Y ratio {Y(b["vl_keylight_x_filter"]) / max(Y(a["vl_keylight_x_filter"]), 1e-12):.3f}')
    json.dump(res, open(OUT + '/indep_check_worst.json', 'w'), indent=1)
