"""Numerical model of Bottled Effects 11 (installed build = InTheBottle/Bottled-Shaders@4ca678b70a) colour path.
Pre-tonemap, single pure time-of-day period, exterior, E11 enabled.  Read-only; numbers only.
Source refs (4ca678b): src/Features/Effects11.cpp 164-250 (UpdateSkyScattering), 513-545 (Curve/Desat/ColorFilter),
557-737 (OverrideWeather); package/Shaders/Sky.hlsl 373-384; features/Effects11/Shaders/Effects11/SkyScattering.hlsli 84-104;
src/Features/Effects11/EffectManager.cpp 902-1029 (time-of-day weights).
"""
import math, colorsys

def v(*a): return list(a)
def mul(a, b): return [x*y for x, y in zip(a, b)]
def sc(a, s): return [x*s for x in a]
def add(a, b): return [x+y for x, y in zip(a, b)]
def lerp(a, b, t):
    if isinstance(a, list): return [x+(y-x)*t for x, y in zip(a, b)]
    return a+(b-a)*t
def sat(x): return max(0.0, min(1.0, x))
def curve(c, p): return [max(x, 0.0)**p for x in c]
def desat(c, d):
    m = sum(c)/3.0
    return [max(lerp(x, m, d), 0.0) for x in c]
def cfilter(c, f, amt): return mul([lerp(x, 1.0, amt) for x in c], f)
def rgb255(*a): return [x/255.0 for x in a]
def pow32(x): return x**32
def hue(c):
    s = sum(c)
    if s <= 0: return "black"
    r, g, b = [x/max(c) for x in c]
    h, l, s2 = colorsys.rgb_to_hls(r, g, b)
    return f"chroma=({c[0]/s:.2f},{c[1]/s:.2f},{c[2]/s:.2f}) hue={h*360:5.1f}deg sat={s2:.2f}"

def fmt(c): return "(" + ", ".join(f"{x:.4g}" for x in c) + ")"

# ---------- Picta A01_Clear routed ini, Day and Sunset periods (values read from the live file) ----------
PICTA_INI = {
 'Day': dict(GradInt=0.3, GradDesat=0.05, TopInt=0.075, TopCurve=1.0, TopF=v(0.0314,0.169,0.404), HorInt=0.5, HorCurve=1.0,
             HorF=v(0.0706,0.208,0.62), PGWC=1.75, Amount=0.5, Intensity=10.0, ColorFromSun=1.0, ScatColor=v(1,1,1),
             AirGlow=1000.0, AirGlowRange=1.0, SunGlow=1.0, SunGlowRange=0.5, HorizonRange=0.9, AtmThick=0.3,
             DustVolume=0.25, DustDensity=0.05, DustDark=0.9, ShadowAmount=0.0, SunDesat=0.0, SunF=v(0.98,0.941,0.902),
             FogCurve=1.0, FogF=v(0.157,0.353,0.863), FogFAmt=0.0, FogMul=2.5,
             DLDesat=1.0, DLF=v(0.98,0.941,0.902), DLFAmt=0.0, DLInt=4.0, DLCurve=1.0),
 'Sunset': dict(GradInt=0.3, GradDesat=0.05, TopInt=0.25, TopCurve=1.0, TopF=v(0.051,0.173,0.4), HorInt=0.5, HorCurve=1.0,
             HorF=v(0.118,0.227,0.62), PGWC=1.65, Amount=0.8, Intensity=6.0, ColorFromSun=1.0, ScatColor=v(1,1,1),
             AirGlow=1000.0, AirGlowRange=1.0, SunGlow=1.0, SunGlowRange=0.5, HorizonRange=0.9, AtmThick=0.4,
             DustVolume=0.25, DustDensity=0.05, DustDark=0.8, ShadowAmount=0.0, SunDesat=0.0, SunF=v(0.98,0.706,0.51),
             FogCurve=1.0, FogF=v(0.255,0.396,0.867), FogFAmt=0.0, FogMul=2.0,
             DLDesat=-0.5, DLF=v(0.98,0.706,0.51), DLFAmt=0.0, DLInt=2.0, DLCurve=1.0),
}
NEUTRAL_INI = {k: dict(d, TopF=v(1,1,1), HorF=v(1,1,1), SunF=v(1,1,1), FogF=v(1,1,1), DLF=v(1,1,1), DLDesat=0.0) for k, d in PICTA_INI.items()}

# ---------- record colours (houseCARL reads) ----------
REC = {
 'Picta 19FA01 A01_Clear (Darkened patch)': {
   'Day': dict(upper=rgb255(125,125,125), horizon=rgb255(125,125,125), sun=rgb255(255,255,255), sunlight=rgb255(255,255,255), fogfar=rgb255(125,125,125)),
   'Sunset': dict(upper=rgb255(125,125,125), horizon=rgb255(125,125,125), sun=rgb255(250,135,35), sunlight=rgb255(250,80,0), fogfar=rgb255(75,75,75))},
 'Astralite ENB.esp 10A230 SkyrimClearMA': {
   'Day': dict(upper=rgb255(39,78,218), horizon=rgb255(121,129,255), sun=rgb255(255,180,139), sunlight=rgb255(219,224,238), fogfar=rgb255(127,147,255)),
   'Sunset': dict(upper=rgb255(19,24,54), horizon=rgb255(246,139,83), sun=rgb255(255,86,38), sunlight=rgb255(255,124,45), fogfar=rgb255(253,147,91))},
}

def sky_pixel(ini, rec, view, sun_dir):
    top = desat(sc(mul(curve(rec['upper'], ini['TopCurve']), ini['TopF']), ini['TopInt']*ini['GradInt']), ini['GradDesat'])
    hor = desat(sc(mul(curve(rec['horizon'], ini['HorCurve']), ini['HorF']), ini['HorInt']*ini['GradInt']), ini['GradDesat'])
    z = view[2]
    sky = lerp(top, hor, (1.0 - sat(z))**ini['PGWC'])          # UseProceduralGradientWeights=true: middle band unused
    # scattering colour (C++ UpdateSkyScattering)
    sunc = cfilter(desat(rec['sun'], ini['SunDesat']), ini['SunF'], 0.0)
    peak = max(max(sunc), 1.0)
    sunN = [max(x, 0)/peak for x in sunc]
    sunH = sun_dir[2]
    sunFade = math.sqrt(sat(1.0 + 2.0*sunH))
    col = [(1.0 + (s-1.0)*ini['ColorFromSun'])*c*sunFade for s, c in zip(sunN, ini['ScatColor'])]
    cpk = max(max(col), 1e-6)
    dustTint = [max(0.0, 1.0 - x/cpk)*2*ini['DustDensity']**2 for x in col]
    dustVol = 0.02/max(ini['DustVolume']**2, 1e-7)
    hR = 1.0/max(ini['HorizonRange']**3, 1e-6)
    aT = 100.0/max(ini['AtmThick']**2, 1e-6)
    agR = 1.0/max(ini['AirGlowRange']**2, 1e-6)
    sgR = 10.0/max(ini['SunGlowRange']**2, 1e-6)
    amount = ini['Amount']**2
    # shader ApplySkyScattering
    facing = sat(sum(a*b for a, b in zip(view, sun_dir))*0.5+0.5)
    away = 1.0 - facing
    elev = 1.0 - sat(1.0 - z)*sat(1.0 + sunH)
    dustBand = pow32(sat(1.0 - elev*dustVol))
    aboveH = sat(1.0 + z*10.0)**2
    sunAbove = sat(1.0 + z*40.0)**2
    spread = lerp(hR*away*away, aT, elev*elev)
    scat = [c*ini['Intensity']*pow32(sat(1.0 - dustBand*t)) for c, t in zip(col, dustTint)]
    scat = sc(scat, aboveH*(1.0 - dustBand*ini['DustDark']))
    shadow = 1.0  # ShadowAmount 0 in Picta routed files
    res = sc(sky, 1.0 + ini['AirGlow']/(1.0 + away*agR))
    w = sat(amount/(1.0 + away*spread))
    res = lerp(res, scat, w)
    res = sc(res, 1.0 + ini['SunGlow']*sunAbove/(1.0 + away*sgR))
    out = lerp(sky, lerp(sc(top, 0.5), res, shadow), aboveH)
    return out, w, sky, scat

def fog_far(ini, rec):
    return sc(cfilter(curve(rec['fogfar'], ini['FogCurve']), ini['FogF'], ini['FogFAmt']), ini['FogMul'])

def sunlight(ini, rec, sunlight_scale=1.0):
    c = sc(rec['sunlight'], sunlight_scale)
    c = curve(c, ini['DLCurve'])
    c = desat(c, ini['DLDesat'])
    c = cfilter(c, ini['DLF'], ini['DLFAmt'])
    c = sc(c, ini['DLInt'])
    return sc(c, 1.0/sunlight_scale)

def norm(a):
    l = math.sqrt(sum(x*x for x in a)); return [x/l for x in a]

lines = []
SUN = {'Day': norm([0.0, 0.57, 0.82]), 'Sunset': norm([0.0, 0.99, 0.05])}
VIEWS = {'zenith': [0, 0, 1], 'horizon-toward-sun (z=0.05)': norm([0, 1, 0.05]), 'horizon-away (z=0.05)': norm([0, -1, 0.05]), 'mid-away (z=0.4)': norm([0, -1, 0.44])}
for iniName, INI in (("PICTA A01_Clear ini", PICTA_INI), ("PICTA ini with hue filters set to 1,1,1 and DL desat 0", NEUTRAL_INI)):
    for recName, R in REC.items():
        for per in ('Day', 'Sunset'):
            ini = INI[per]; rec = R[per]
            lines.append(f"\n== {iniName} | records: {recName} | period {per}")
            for vn, vd in VIEWS.items():
                out, w, sky, scat = sky_pixel(ini, rec, vd, SUN[per])
                lines.append(f"  sky {vn:28s} out={fmt(out)} {hue(out)} | scatter-weight={w:.2f} gradient-only={hue(sky)}")
            f = fog_far(ini, rec)
            lines.append(f"  fog far colour  {fmt(f)} {hue(f)}")
            s = sunlight(ini, rec)
            lines.append(f"  sunlight colour {fmt(s)} {hue(s)}")

# ---------- time-of-day weights (EffectManager.cpp 902-1029) ----------
def tod_weights(h, T):
    night, sunrise, dawnD, day, sunset, duskD = T['NightTime'], T['SunriseTime'], T['DawnDuration'], T['DayTime'], T['SunsetTime'], T['DuskDuration']
    dawnStart = sunrise - dawnD; dawnMid = sunrise - dawnD*0.5; duskMid = sunset + duskD*0.5; duskEnd = sunset + duskD
    tp = [night, dawnStart, dawnMid, sunrise, day, sunset, duskMid, duskEnd]
    tp = tp + [x+24 for x in tp]
    fmap = ['Night', 'Night', 'Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night']
    ci = ni = 0; cpt = 0.0; npt = 24.0
    for i, t in enumerate(tp):
        if h >= t and t >= cpt: ci, cpt = i, t
        if t > h and npt >= t: ni, npt = i, t
    cf, nf = fmap[ci % 8], fmap[ni % 8]
    td = abs(npt - cpt) or 1.0
    b = abs(h - cpt)/td
    f = dict(Dawn=0, Sunrise=0, Day=0, Sunset=0, Dusk=0, Night=0)
    if cf == nf: f[cf] = 1.0
    else:
        f[cf] = sat(1-b); f[nf] = sat(b)
    pd = sat(f['Day']**0.6)
    if pd > 1.17549435e-38:
        if f['Sunrise'] > 1.17549435e-38: f['Sunrise'] = sat(1-pd)
        if f['Sunset'] > 1.17549435e-38: f['Sunset'] = sat(1-pd)
    f['Day'] = pd
    return f
TODS = {'Picta base': dict(DawnDuration=3.5, SunriseTime=9.0, DayTime=10.0, SunsetTime=17.0, DuskDuration=3.5, NightTime=20.5),
        'NAT/Astralite lane base': dict(DawnDuration=3.5, SunriseTime=8.0, DayTime=13.0, SunsetTime=18.0, DuskDuration=3.5, NightTime=1.0)}
for name, T in TODS.items():
    lines.append(f"\n== time-of-day weights, {name} {T}")
    mx = 0
    for q in range(0, 24*4):
        h = q/4.0
        f = tod_weights(h, T)
        s = sum(f.values()); mx = max(mx, s)
        if q % 4 == 0 or abs(s-1) > 1e-6:
            lines.append(f"  {h:5.2f}h " + " ".join(f"{k}={x:.2f}" for k, x in f.items() if x > 0) + f"  sum={s:.3f}")
    lines.append(f"  max sum over the day = {mx:.4f}")

open('colour_model_out.txt', 'w').write("\n".join(lines))
print("\n".join(lines))
