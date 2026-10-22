import json, os, sys, re
S = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(S, "picta_e11_colour.json"), encoding="utf-8"))
P = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night"]
if len(sys.argv) > 2 and sys.argv[2] == "int":
    P = ["InteriorDay", "InteriorNight"]
KEYS = [
    ("SKY", "GradientIntensity"), ("SKY", "GradientDesaturation"),
    ("SKY", "GradientTopIntensity"), ("SKY", "GradientTopCurve"), ("SKY", "GradientTopColorFilter"),
    ("SKY", "GradientMiddleIntensity"), ("SKY", "GradientMiddleColorFilter"),
    ("SKY", "GradientHorizonIntensity"), ("SKY", "GradientHorizonCurve"), ("SKY", "GradientHorizonColorFilter"),
    ("SKY", "CloudsIntensity"), ("SKY", "CloudsDesaturation"), ("SKY", "CloudsColorFilter"), ("SKY", "CloudsOpacity"),
    ("SKY", "SunIntensity"), ("SKY", "SunDesaturation"), ("SKY", "SunColorFilter"), ("SKY", "MoonColorFilter"),
    ("SKYSCATTERING", "Intensity"), ("SKYSCATTERING", "Amount"), ("SKYSCATTERING", "ColorFromSun"), ("SKYSCATTERING", "ScatteringColor"),
    ("SKYSCATTERING", "AirGlowIntensity"), ("SKYSCATTERING", "AirGlowRange"), ("SKYSCATTERING", "SunGlowIntensity"), ("SKYSCATTERING", "SunGlowRange"),
    ("SKYSCATTERING", "AtmosphereThickness"), ("SKYSCATTERING", "HorizonRange"),
    ("ENVIRONMENT", "DirectLightingIntensity"), ("ENVIRONMENT", "DirectLightingDesaturation"), ("ENVIRONMENT", "DirectLightingColorFilterAmount"), ("ENVIRONMENT", "DirectLightingColorFilter"),
    ("ENVIRONMENT", "AmbientLightingIntensity"), ("ENVIRONMENT", "AmbientLightingDesaturation"),
    ("ENVIRONMENT", "FogColorMultiplier"), ("ENVIRONMENT", "FogColorCurve"), ("ENVIRONMENT", "FogAmountMultiplier"), ("ENVIRONMENT", "FogCurveMultiplier"),
    ("ENVIRONMENT", "FogColorFilterAmount"), ("ENVIRONMENT", "FogColorFilter"), ("ENVIRONMENT", "ColorPow"),
    ("VOLUMETRICFOG", "Intensity"), ("VOLUMETRICFOG", "Opacity"), ("VOLUMETRICFOG", "ColorFilter"),
    ("IMAGEBASEDLIGHTING", "MultiplicativeAmount"), ("IMAGEBASEDLIGHTING", "AdditiveAmount"),
    ("GAMEVOLUMETRICRAYS", "Intensity"), ("GAMEVOLUMETRICRAYS", "Desaturation"), ("GAMEVOLUMETRICRAYS", "ColorFilter"),
    ("VOLUMETRICRAYS", "Intensity"), ("VOLUMETRICRAYS", "SkyColorAmount"),
    ("CLOUDSHADOWS", "Amount"),
]
sel = sys.argv[1] if len(sys.argv) > 1 else "00_Master/A01"
targets = [f for f in d["effective"] if sel.lower() in f.lower()] if sel != "BASE" else ["BASE"]
for f in targets:
    eff = d["base"]["colour"] if f == "BASE" else d["effective"][f]
    own = {} if f == "BASE" else d["files"][f]["colour"]
    print("=====", f)
    for sec, k in KEYS:
        vals = []
        for p in P:
            key = k + p
            v = eff.get(sec, {}).get(key)
            mark = "" if f == "BASE" or key in own.get(sec, {}) else "*"
            vals.append(f"{v}{mark}")
        print(f"  {sec[:6]:6} {k:32} " + " | ".join(vals))
    # grade
    fx = eff.get("ENBEFFECT.FX", {})
    for kk, vv in fx.items():
        if any(x in kk for x in ["Tint", "Saturation", "Color Balance", "Exposure"]) and "Bloom" not in kk and any(p in kk for p in ["Day", "Night", "Interior", "Dawn", "Sunrise", "Sunset", "Dusk"]):
            print("  FX    ", kk, "=", vv)
    pp = eff.get("ENBEFFECTPOSTPASS.FX", {})
    for kk, vv in pp.items():
        if any(x in kk for x in ["Tint", "Saturation  ", "- Saturation", "Vibrance", "Channel"]) and vv.strip() not in ("1.0", "0.0", "1.0, 1.0, 1.0, 0.0", "1.0, 0.0, 0.0", "0.0, 1.0, 0.0", "0.0, 0.0, 1.0"):
            print("  PP    ", kk, "=", vv)
