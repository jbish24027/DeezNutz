"""Model Picta's live per-weather/per-period sky, light and fog colours under Bottled E11 (pre-tonemap linear),
using the WTHR winners (picta_wthr_colours.json) + effective E11 inis (picta_e11_colour.json) and the formulas in
Bottled Bottle-Compendium Effects11.cpp OverrideWeather/OverrideAmbientLighting + SkyScattering.hlsli ApplySkyScattering.
Record TOD used per ENB period: Dawn->Sunrise rec, Sunrise->Sunrise, Day->Day, Sunset->Sunset, Dusk->Sunset, Night->Night
(approximation: the engine itself blends record TODs by climate timing 06-09 / 17-20)."""
import json, os, math, colorsys
S = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(S, "picta_wthr_colours.json")))
E = json.load(open(os.path.join(S, "picta_e11_colour.json"), encoding="utf-8"))
P = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night"]
REC = {"Dawn": "Sunrise", "Sunrise": "Sunrise", "Day": "Day", "Sunset": "Sunset", "Dusk": "Sunset", "Night": "Night"}
SUNZ = {"Dawn": 0.02, "Sunrise": 0.25, "Day": 0.8, "Sunset": 0.25, "Dusk": 0.02, "Night": -0.3}
FILEMAP = {}
for sec, r in E["routing"].items():
    for wid in r["WeatherIDs"]:
        FILEMAP[wid.upper().zfill(6)] = r["FileName"]

def v3(s):
    if s is None: return None
    p = [float(x) for x in str(s).replace(" ", "").split(",")]
    return p[:3] if len(p) >= 3 else [p[0]] * 3
def f(s, d=1.0):
    try: return float(s)
    except Exception: return d
def desat(c, d):
    l = sum(c) / 3
    return [max(x + (l - x) * d, 0) for x in c]
def mul(a, b): return [x * y for x, y in zip(a, b)]
def sc(a, k): return [x * k for x in a]
def curve(c, p): return [max(x, 0) ** p for x in c]
def hue(c):
    m = max(c)
    if m <= 0: return "black"
    h, s, v = colorsys.rgb_to_hsv(*[x / m for x in c])
    return f"h{h*360:.0f} s{s:.2f}"
def r3(c): return [round(x, 3) for x in c]

out = {}
for fid, rec in W.items():
    short = fid.split(":")[0]
    if not (short.startswith("19F") or short.startswith("5AF")): continue
    fn = FILEMAP.get(short)
    if not fn: continue
    eff = E["effective"][fn]
    g = lambda sec, k: eff.get(sec, {}).get(k)
    wo = {"file": fn, "editorid": rec["editorid"], "periods": {}}
    for p in P:
        t = REC[p]
        col = rec["colours"]
        up = [x / 255 for x in col["SkyUpperColor"][t]]; hz = [x / 255 for x in col["HorizonColor"][t]]
        gi = f(g("SKY", "GradientIntensity" + p)); gd = f(g("SKY", "GradientDesaturation" + p), 0)
        top = desat(sc(mul(curve(up, f(g("SKY", "GradientTopCurve" + p))), v3(g("SKY", "GradientTopColorFilter" + p))), f(g("SKY", "GradientTopIntensity" + p)) * gi), gd)
        hor = desat(sc(mul(curve(hz, f(g("SKY", "GradientHorizonCurve" + p))), v3(g("SKY", "GradientHorizonColorFilter" + p))), f(g("SKY", "GradientHorizonIntensity" + p)) * gi), gd)
        # sun colour graded -> scattering colour
        sunc = [x / 255 for x in col["SunColor"][t]]
        sunc = mul(desat(sunc, f(g("SKY", "SunDesaturation" + p), 0)), v3(g("SKY", "SunColorFilter" + p)))
        pk = max(max(sunc), 1.0); sunn = [max(x, 0) / pk for x in sunc]
        cfs = f(g("SKYSCATTERING", "ColorFromSun" + p), 0); scol = v3(g("SKYSCATTERING", "ScatteringColor" + p))
        z = SUNZ[p]; sunfade = math.sqrt(min(max(1 + 2 * z, 0), 1))
        scat = [(1 + (s - 1) * cfs) * c * sunfade for s, c in zip(sunn, scol)]
        I = f(g("SKYSCATTERING", "Intensity" + p)); A = f(g("SKYSCATTERING", "Amount" + p), 0) ** 2
        AG = f(g("SKYSCATTERING", "AirGlowIntensity" + p), 0); AGR = 1 / max(f(g("SKYSCATTERING", "AirGlowRange" + p), 0.2) ** 2, 1e-6)
        SG = f(g("SKYSCATTERING", "SunGlowIntensity" + p), 0); SGR = 10 / max(f(g("SKYSCATTERING", "SunGlowRange" + p), 0.2) ** 2, 1e-6)
        HR = 1 / max(f(g("SKYSCATTERING", "HorizonRange" + p), 0.5) ** 3, 1e-6); AT = 100 / max(f(g("SKYSCATTERING", "AtmosphereThickness" + p), 1) ** 2, 1e-6)
        DV = 0.02 / max(f(g("SKYSCATTERING", "DustVolume" + p), 0.2) ** 2, 1e-7); DD = f(g("SKYSCATTERING", "DustDarkening" + p), 0)
        def dome(sky, away, elev, above=1.0):
            spread = HR * away * away + (AT - HR * away * away) * elev * elev
            dust = min(max(1 - elev * DV, 0), 1) ** 32
            res = sc(sky, 1 + AG / (1 + away * AGR))
            w = min(max(A / (1 + away * spread), 0), 1)
            sdark = 1 - dust * DD
            res = [r + (s * I * sdark - r) * w for r, s in zip(res, scat)]
            res = sc(res, 1 + SG / (1 + away * SGR))
            return res
        zen = dome(top, 0.5, 1.0)
        hz_side = dome(hor, 0.5, 0.0)
        hz_anti = dome(hor, 1.0, 0.0)
        hz_sun = dome(hor, 0.0, 0.0)
        # clouds base (before lighting): record cloud colour (layer day colours ~250) x filter x intensity
        cfil = v3(g("SKY", "CloudsColorFilter" + p)); cint = f(g("SKY", "CloudsIntensity" + p))
        cloud = sc(mul([0.98, 0.98, 0.98], cfil), cint)
        # sunlight
        sl = [x / 255 for x in col["SunlightColor"][t]]
        sl = curve(sl, f(g("ENVIRONMENT", "DirectLightingCurve" + p)))
        sl = desat(sl, f(g("ENVIRONMENT", "DirectLightingDesaturation" + p), 0))
        amt = f(g("ENVIRONMENT", "DirectLightingColorFilterAmount" + p), 0)
        sl = mul([x + (1 - x) * amt for x in sl], v3(g("ENVIRONMENT", "DirectLightingColorFilter" + p)))
        sl = sc(sl, f(g("ENVIRONMENT", "DirectLightingIntensity" + p)))
        # ambient (DALC up / side / down)
        dal = col["DALC"][t]; ad = f(g("ENVIRONMENT", "AmbientLightingDesaturation" + p), 0); ai = f(g("ENVIRONMENT", "AmbientLightingIntensity" + p))
        amb = {k: r3(sc(desat([x / 255 for x in dal[kk]], ad), ai)) for k, kk in [("up", "DirectionalZPlus"), ("side", "DirectionalXPlus"), ("down", "DirectionalZMinus")]}
        # fog far
        ff = [x / 255 for x in col["FogFarColor"][t]]
        ff = curve(ff, f(g("ENVIRONMENT", "FogColorCurve" + p)))
        famt = f(g("ENVIRONMENT", "FogColorFilterAmount" + p), 0)
        ff = mul([x + (1 - x) * famt for x in ff], v3(g("ENVIRONMENT", "FogColorFilter" + p)))
        ff = sc(ff, f(g("ENVIRONMENT", "FogColorMultiplier" + p)))
        vf = sc(v3(g("VOLUMETRICFOG", "ColorFilter" + p)), f(g("VOLUMETRICFOG", "Intensity" + p)))
        wo["periods"][p] = {
            "sky_zenith": r3(zen), "sky_zenith_hue": hue(zen),
            "sky_horizon_side": r3(hz_side), "sky_horizon_side_hue": hue(hz_side),
            "sky_horizon_antisun": r3(hz_anti), "sky_horizon_sunward": r3(hz_sun), "sky_horizon_sunward_hue": hue(hz_sun),
            "scattering_colour": r3(sc(scat, I)), "scattering_hue": hue(scat),
            "cloud_base": r3(cloud), "cloud_hue": hue(cloud),
            "sunlight": r3(sl), "sunlight_hue": hue(sl),
            "ambient": amb, "ambient_side_hue": hue(amb["side"]),
            "fog_far": r3(ff), "fog_far_hue": hue(ff),
            "volumetric_fog_mesh_tint": r3(vf), "volumetric_fog_opacity": f(g("VOLUMETRICFOG", "Opacity" + p)),
            "fog_distance_scale_FogAmountMultiplier": f(g("ENVIRONMENT", "FogAmountMultiplier" + p)),
            "fog_curve_FogCurveMultiplier": f(g("ENVIRONMENT", "FogCurveMultiplier" + p)),
        }
    out[short] = wo
json.dump(out, open(os.path.join(S, "picta_palette_model.json"), "w"), indent=1)
# print compact
for wid in ["19FA01", "19FB01", "19FC01", "19FD01", "19FD02", "19FE03", "19FE05", "5AFA01"]:
    o = out[wid]; print("=====", wid, o["editorid"], o["file"])
    for p in P:
        q = o["periods"][p]
        print(f"  {p:7} zen{q['sky_zenith']} {q['sky_zenith_hue']} | hzSide{q['sky_horizon_side']} {q['sky_horizon_side_hue']} | hzSun{q['sky_horizon_sunward']} {q['sky_horizon_sunward_hue']}")
        print(f"          sun{q['sunlight']} {q['sunlight_hue']} | amb side{q['ambient']['side']} {q['ambient_side_hue']} | fog{q['fog_far']} {q['fog_far_hue']} | cloud{q['cloud_base']} {q['cloud_hue']} | volfog{q['volumetric_fog_mesh_tint']} op{q['volumetric_fog_opacity']}")
