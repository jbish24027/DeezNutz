import json, os, collections
S = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(S, "picta_e11_colour.json"), encoding="utf-8"))
P = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night", "InteriorDay", "InteriorNight"]
masters = [f for f in d["effective"] if "00_Master" in f or "Summer" in f]
KEYS = [("SKY", "GradientTopColorFilter"), ("SKY", "GradientMiddleColorFilter"), ("SKY", "GradientHorizonColorFilter"),
        ("SKY", "GradientIntensity"), ("SKY", "GradientTopIntensity"), ("SKY", "GradientHorizonIntensity"), ("SKY", "GradientDesaturation"),
        ("SKY", "CloudsColorFilter"), ("SKY", "CloudsIntensity"), ("SKY", "SunColorFilter"),
        ("SKYSCATTERING", "ScatteringColor"), ("SKYSCATTERING", "ColorFromSun"), ("SKYSCATTERING", "Intensity"), ("SKYSCATTERING", "Amount"), ("SKYSCATTERING", "AirGlowIntensity"), ("SKYSCATTERING", "AirGlowRange"), ("SKYSCATTERING", "SunGlowIntensity"),
        ("SKYSCATTERING", "CloudsLightingSunMultiplier"), ("SKYSCATTERING", "CloudsLightingSunMinIntensity"), ("SKYSCATTERING", "DustDensity"), ("SKYSCATTERING", "ShadowAmount"),
        ("ENVIRONMENT", "DirectLightingColorFilter"), ("ENVIRONMENT", "DirectLightingColorFilterAmount"), ("ENVIRONMENT", "DirectLightingDesaturation"), ("ENVIRONMENT", "DirectLightingIntensity"),
        ("ENVIRONMENT", "AmbientLightingDesaturation"), ("ENVIRONMENT", "AmbientLightingIntensity"),
        ("ENVIRONMENT", "FogColorFilter"), ("ENVIRONMENT", "FogColorFilterAmount"), ("ENVIRONMENT", "FogColorMultiplier"), ("ENVIRONMENT", "FogAmountMultiplier"), ("ENVIRONMENT", "FogCurveMultiplier"), ("ENVIRONMENT", "ColorPow"),
        ("VOLUMETRICFOG", "ColorFilter"), ("VOLUMETRICFOG", "Intensity"), ("VOLUMETRICFOG", "Opacity"),
        ("GAMEVOLUMETRICRAYS", "ColorFilter"), ("IMAGEBASEDLIGHTING", "MultiplicativeAmount")]
out = {}
for sec, k in KEYS:
    for p in P[:6]:
        c = collections.defaultdict(list)
        for f in masters:
            v = d["effective"][f].get(sec, {}).get(k + p)
            c[v].append(os.path.basename(f).split("_")[0])
        out[f"{sec}.{k}{p}"] = {str(v): names for v, names in c.items()}
        if len(c) <= 4:
            print(f"{sec[:6]} {k+p:40} " + " ; ".join(f"{v} [{len(n)}: {','.join(n) if len(n) < 8 else 'many'}]" for v, n in c.items()))
        else:
            print(f"{sec[:6]} {k+p:40} {len(c)} distinct values")
json.dump(out, open(os.path.join(S, "picta_e11_variance.json"), "w"), indent=1)
