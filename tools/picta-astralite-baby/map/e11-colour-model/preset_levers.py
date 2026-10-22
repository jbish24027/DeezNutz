"""Summarise the colour levers of an E11 preset as Bottled 4ca678b reads them (read-only).
Usage: python preset_levers.py <winners.json> <label> <outfile>
Ini semantics approximate GetPrivateProfileString: section/key names case-insensitive, first section, first key wins.
"""
import os, sys, json, re
from collections import defaultdict, Counter

INST = r"C:/1. AUTHORIA/mods"
winners = json.load(open(sys.argv[1]))
label = sys.argv[2]
outp = sys.argv[3]

def vfs(rel):
    rel = rel.lower()
    mod = winners.get(rel)
    if not mod:
        return None
    base = os.path.join(INST, mod)
    # find case-insensitively
    parts = rel.split('/')
    cur = base
    for p in parts:
        if not os.path.isdir(cur):
            return None
        m = [x for x in os.listdir(cur) if x.lower() == p]
        if not m:
            return None
        cur = os.path.join(cur, m[0])
    return cur

def parse_ini(path):
    secs = {}
    cur = None
    seen = set()
    with open(path, encoding='latin-1') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith(';') or s.startswith('#') or s.startswith('//'):
                continue
            if s.startswith('[') and ']' in s:
                name = s[1:s.index(']')].strip().upper()
                if name in seen:
                    cur = None  # duplicate section ignored (first wins)
                else:
                    seen.add(name)
                    cur = secs.setdefault(name, {})
                continue
            if cur is None or '=' not in s:
                continue
            k, v = s.split('=', 1)
            k = k.strip().lower()
            if k not in cur:
                cur[k] = v.strip()
    return secs

PER = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night", "InteriorDay", "InteriorNight"]

def get_tod(secs, sec, key):
    d = secs.get(sec, {})
    res = {}
    if key.lower() in d:
        for p in PER:
            res[p] = d[key.lower()]
    for p in PER:
        k = (key + p).lower()
        if k in d:
            res[p] = d[k]
    return res

base_path = vfs('enbseries.ini')
base = parse_ini(base_path)
lines = [f"# {label}: base = {base_path}"]

bools = [("EFFECT", k) for k in ["UseEffect", "UseOriginalPostProcessing", "EnableAdaptation", "EnableBloom", "EnableLens", "EnablePostPassShader",
         "EnableCloudShadows", "EnableCloudsScattering", "EnableImageBasedLighting", "EnableVolumetricRays", "EnableSunRays", "EnableMoonRays", "EnableWater"]]
bools += [("GLOBAL", "UseEffect"), ("WEATHER", "EnableMultipleWeathers"), ("WEATHER", "EnableLocationWeather"),
          ("SKY", "DisableWrongSkyMath"), ("SKY", "FixBlackCrush"), ("SKY", "UseProceduralGradientWeights"),
          ("SKYSCATTERING", "EnableCloudsLightingFromMoon"), ("SKYSCATTERING", "CalculateCloudsEdgeFromScattering"),
          ("VOLUMETRICFOG", "EnableLighting"), ("RAYS", "UseLinearMath")]
for sec, k in bools:
    lines.append(f"[{sec}] {k} = {base.get(sec, {}).get(k.lower())}")
for sec in ["TIMEOFDAY"]:
    lines.append(f"[TIMEOFDAY] {base.get('TIMEOFDAY')}")
# ignore flags
for sec in ["ENVIRONMENT", "SKY", "SKYSCATTERING", "VOLUMETRICFOG", "GAMEVOLUMETRICRAYS", "IMAGEBASEDLIGHTING", "FIRE", "PARTICLE", "LIGHTSPRITE", "BLOOM", "LENS", "SUNGLARE", "WATER", "CLOUDSHADOWS", "VOLUMETRICRAYS", "RAYS", "NIGHTEYE", "RAIN"]:
    d = base.get(sec, {})
    lines.append(f"[{sec}] IgnoreWeatherSystem={d.get('ignoreweathersystem')} IgnoreWeatherSystemInterior={d.get('ignoreweathersysteminterior')}")

tod_keys = [
    ("SKY", "GradientIntensity"), ("SKY", "GradientDesaturation"),
    ("SKY", "GradientTopIntensity"), ("SKY", "GradientTopCurve"), ("SKY", "GradientTopColorFilter"),
    ("SKY", "GradientMiddleIntensity"), ("SKY", "GradientMiddleCurve"), ("SKY", "GradientMiddleColorFilter"),
    ("SKY", "GradientHorizonIntensity"), ("SKY", "GradientHorizonCurve"), ("SKY", "GradientHorizonColorFilter"),
    ("SKY", "ProceduralGradientWeightCurve"),
    ("SKY", "CloudsIntensity"), ("SKY", "CloudsCurve"), ("SKY", "CloudsDesaturation"), ("SKY", "CloudsOpacity"), ("SKY", "CloudsColorFilter"),
    ("SKY", "SunIntensity"), ("SKY", "SunColorFilter"),
    ("SKYSCATTERING", "Amount"), ("SKYSCATTERING", "Intensity"), ("SKYSCATTERING", "ColorFromSun"), ("SKYSCATTERING", "ScatteringColor"),
    ("SKYSCATTERING", "AirGlowIntensity"), ("SKYSCATTERING", "SunGlowIntensity"), ("SKYSCATTERING", "ShadowAmount"),
    ("ENVIRONMENT", "DirectLightingIntensity"), ("ENVIRONMENT", "DirectLightingCurve"), ("ENVIRONMENT", "DirectLightingDesaturation"),
    ("ENVIRONMENT", "DirectLightingColorFilter"), ("ENVIRONMENT", "DirectLightingColorFilterAmount"),
    ("ENVIRONMENT", "AmbientLightingIntensity"), ("ENVIRONMENT", "AmbientLightingDesaturation"),
    ("ENVIRONMENT", "FogColorMultiplier"), ("ENVIRONMENT", "FogColorCurve"), ("ENVIRONMENT", "FogAmountMultiplier"),
    ("ENVIRONMENT", "FogCurveMultiplier"), ("ENVIRONMENT", "FogColorFilter"), ("ENVIRONMENT", "FogColorFilterAmount"),
    ("ENVIRONMENT", "ColorPow"),
    ("VOLUMETRICFOG", "Intensity"), ("VOLUMETRICFOG", "Curve"), ("VOLUMETRICFOG", "Opacity"), ("VOLUMETRICFOG", "ColorFilter"),
    ("GAMEVOLUMETRICRAYS", "Intensity"), ("GAMEVOLUMETRICRAYS", "ColorFilter"), ("GAMEVOLUMETRICRAYS", "Desaturation"),
    ("IMAGEBASEDLIGHTING", "MultiplicativeAmount"),
]
lines.append("\n## base enbseries.ini time-of-day levers (period: value)")
for sec, k in tod_keys:
    v = get_tod(base, sec, k)
    lines.append(f"[{sec}] {k}: " + ("; ".join(f"{p}={v[p]}" for p in PER if p in v) if v else "(absent -> default)"))

# legacy/unregistered keys present in base
reg_absent = []
for sec in base:
    for k in base[sec]:
        if sec == "FOG" or k.startswith("fogheight") or k.startswith("ambientlightingcurve") or k.startswith("ambientlightingcolorfilter"):
            reg_absent.append(f"[{sec}] {k}")
lines.append("\n## keys in base that this build does not register (sample): " + ", ".join(reg_absent[:40]))

# weather list
wl_path = vfs('enbseries/_weatherlist.ini')
wl = parse_ini(wl_path) if wl_path else {}
files = Counter()
for s, d in wl.items():
    if s.startswith('WEATHER') and d.get('filename') and d.get('weatherids'):
        files[d['filename']] += 1
lines.append(f"\n## _weatherlist.ini = {wl_path}: {sum(1 for s in wl if s.startswith('WEATHER'))} WEATHER sections, {len(files)} distinct files")

# per-weather file statistics for the hue levers
stats = defaultdict(lambda: defaultdict(Counter))
defined = Counter()
nfiles = 0
for fn in sorted(files):
    p = vfs('enbseries/' + fn.replace('\\', '/'))
    if not p:
        lines.append(f"  MISSING weather file {fn}")
        continue
    nfiles += 1
    w = parse_ini(p)
    for sec, k in tod_keys:
        v = get_tod(w, sec, k)
        if v:
            defined[(sec, k)] += 1
        for per, val in v.items():
            stats[(sec, k)][per][val] += 1
lines.append(f"weather files parsed: {nfiles}")
lines.append("\n## per-weather files: how many define each lever, and the most common values per period")
for sec, k in tod_keys:
    if defined[(sec, k)] == 0:
        lines.append(f"[{sec}] {k}: defined in 0 files")
        continue
    parts = []
    for per in PER:
        c = stats[(sec, k)][per]
        if c:
            top = ", ".join(f"{val} x{n}" for val, n in c.most_common(3))
            parts.append(f"{per}: {top} ({len(c)} distinct)")
    lines.append(f"[{sec}] {k}: defined in {defined[(sec, k)]} files | " + " | ".join(parts))

open(outp, 'w', encoding='utf-8').write("\n".join(lines))
print("\n".join(lines[:60]))
