"""Compact the houseCARL 'everything' WTHR dump into a colour-only JSON per weather per TOD."""
import json, re, sys
S = r"C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/picta-colour/"
src = sys.argv[1] if len(sys.argv) > 1 else S + "wthr_winners_everything.jsonl"
dst = sys.argv[2] if len(sys.argv) > 2 else S + "picta_wthr_colours.json"
TOD = ["Sunrise", "Day", "Sunset", "Night"]
COLOR_FIELDS = ["SkyUpperColor", "SkyLowerColor", "HorizonColor", "FogNearColor", "FogFarColor", "AmbientColor",
                "SunlightColor", "SunColor", "StarsColor", "EffectLightingColor", "CloudLodDiffuseColor",
                "CloudLodAmbientColor", "WaterMultiplierColor", "SkyStaticsColor", "SunGlareColor", "MoonGlareColor",
                "UnknownColor"]
SCAL = ["FogDistanceDayNear", "FogDistanceDayFar", "FogDistanceDayMax", "FogDistanceDayPower",
        "FogDistanceNightNear", "FogDistanceNightFar", "FogDistanceNightMax", "FogDistanceNightPower",
        "Flags", "SunGlare", "SunDamage", "TransDelta", "WindSpeed", "Precipitation", "VisualEffect", "LightningColor",
        "Aurora", "PrecipitationBeginFadeIn", "PrecipitationEndFadeOut"]
def rgb(v):
    if v is None: return None
    p = v.split(",")
    try: return [int(p[0]), int(p[1]), int(p[2])]
    except Exception: return v
lines = open(src, encoding="utf-8").read().splitlines()
out = {}
for l in lines[1:]:
    r = json.loads(l)
    f = {}
    for x in r["fields"]:
        f[x["path"]] = x.get("value", x.get("note"))
    rec = {"editorid": r.get("editorid"), "winner": r.get("winner"), "override_depth": r.get("override_depth")}
    col = {}
    for c in COLOR_FIELDS:
        col[c] = {t: rgb(f.get(f"{c}.{t}")) for t in TOD}
    dalc = {}
    for t in TOD:
        b = f"DirectionalAmbientLightingColors.{t}."
        dalc[t] = {k: rgb(f.get(b + k)) for k in ["DirectionalXPlus", "DirectionalXMinus", "DirectionalYPlus",
                                                  "DirectionalYMinus", "DirectionalZPlus", "DirectionalZMinus", "Specular"]}
        dalc[t]["Scale"] = f.get(b + "Scale")
        dalc[t]["Fresnel"] = f.get(b + "FresnelPower") if (b + "FresnelPower") in f else None
    col["DALC"] = dalc
    rec["colours"] = col
    rec["scalars"] = {k: f.get(k) for k in SCAL}
    rec["imagespaces"] = {t: f.get(f"ImageSpaces.{t}") for t in TOD}
    rec["voli"] = {t: f.get(f"VolumetricLighting.{t}") for t in TOD}
    clouds = []
    for i in range(32):
        if f.get(f"Clouds[{i}].Enabled") == "True":
            clouds.append({"layer": i, "texture": f.get(f"CloudTextures[{i}]"),
                           "colors": {t: rgb(f.get(f"Clouds[{i}].Colors.{t}")) for t in TOD},
                           "alphas": {t: f.get(f"Clouds[{i}].Alphas.{t}") for t in TOD}})
    rec["clouds_enabled"] = clouds
    # unseen extra paths for DALC (fresnel etc)
    extra = sorted(k for k in f if k.startswith("DirectionalAmbientLightingColors.Day.") )
    rec["_dalc_paths"] = extra
    out[r["formid"]] = rec
json.dump(out, open(dst, "w"), indent=1)
print(len(out), "weathers ->", dst)
