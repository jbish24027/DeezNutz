import json, os, colorsys
from collections import defaultdict
from wlib import *

d = json.load(open(os.path.join(HERE, "astralite_rotating_weathers_colour.json")))
MAINWS = {"00003C:Skyrim.esm", "01A26F:Skyrim.esm", "037EDF:Skyrim.esm", "01691D:Skyrim.esm", "016BB4:Skyrim.esm",
          "016D71:Skyrim.esm", "046033:Skyrim.esm", "000800:Dragonborn.esm"}
TOD4 = ["Sunrise", "Day", "Sunset", "Night"]

def hname(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    H = h * 360
    if s < 0.08:
        tone = "grey"
    elif H < 15 or H >= 345: tone = "red"
    elif H < 40: tone = "orange"
    elif H < 65: tone = "yellow"
    elif H < 160: tone = "green"
    elif H < 195: tone = "cyan"
    elif H < 225: tone = "azure"
    elif H < 255: tone = "blue"
    elif H < 285: tone = "violet"
    elif H < 320: tone = "purple/magenta"
    else: tone = "rose/pink"
    return {"hex": "#%02x%02x%02x" % (r, g, b), "H": round(H), "S": round(s, 2), "V": round(v, 2), "tone": tone}

def classify(flags):
    f = flags or ""
    if "Snow" in f: return "snow"
    if "Rainy" in f: return "rainy"
    if "Cloudy" in f: return "cloudy"
    if "Pleasant" in f: return "pleasant"
    return "unclassified(precip stripped)"

FIELDS = ["SkyUpperColor", "SkyLowerColor", "HorizonColor", "FogNearColor", "FogFarColor", "AmbientColor",
          "SunlightColor", "SunColor", "EffectLightingColor", "SkyStaticsColor", "CloudLodDiffuseColor", "SunGlareColor",
          "MoonGlareColor", "WaterMultiplierColor", "StarsColor"]
agg = defaultdict(lambda: defaultdict(list))
main = {}
for fid, v in d.items():
    regs = v.get("regions", [])
    if not any(r["worldspace"] in MAINWS for r in regs):
        continue
    main[fid] = v
    cl = classify(v["flags"])
    for t in TOD4:
        for fld in FIELDS:
            c = v["colors"].get(fld, {}).get(t)
            if c:
                agg[(cl, t)][fld].append(c); agg[("ALL", t)][fld].append(c)
        dd = v["dalc"].get(t)
        if dd:
            axes = [dd[a] for a in ("DirectionalXPlus", "DirectionalXMinus", "DirectionalYPlus", "DirectionalYMinus", "DirectionalZPlus", "DirectionalZMinus")]
            m = [round(sum(x[i] for x in axes) / 6) for i in range(3)]
            agg[(cl, t)]["DALC_mean6"].append(m); agg[("ALL", t)]["DALC_mean6"].append(m)
            agg[(cl, t)]["DALC_ZMinus(up-facing? see note)"].append(dd["DirectionalZMinus"])
            agg[(cl, t)]["DALC_ZPlus"].append(dd["DirectionalZPlus"])
        # enabled cloud layers mean colour
        cc = [L["colors"].get(t) for L in v["clouds"] if L["enabled"] == "True" and L["colors"].get(t)]
        if cc:
            m = [round(sum(x[i] for x in cc) / len(cc)) for i in range(3)]
            agg[(cl, t)]["CloudLayers_enabled_mean"].append(m); agg[("ALL", t)]["CloudLayers_enabled_mean"].append(m)

summary = {}
for (cl, t), flds in agg.items():
    s = {}
    for fld, lst in flds.items():
        m = [round(sum(x[i] for x in lst) / len(lst)) for i in range(3)]
        s[fld] = {"mean_rgb": m, "n": len(lst), **hname(*m)}
    summary.setdefault(cl, {})[t] = s
json.dump({"main_weather_count": len(main), "per_class_per_tod": summary}, open(os.path.join(HERE, "astralite_palette_summary.json"), "w"), indent=1)

for cl in ["ALL", "pleasant", "cloudy", "rainy", "snow", "unclassified(precip stripped)"]:
    if cl not in summary: continue
    print("=====", cl, "n weathers:", sum(1 for v in main.values() if cl == "ALL" or classify(v["flags"]) == cl))
    for t in TOD4:
        s = summary[cl].get(t, {})
        line = []
        for fld in ["SkyUpperColor", "SkyLowerColor", "HorizonColor", "FogNearColor", "FogFarColor", "AmbientColor", "DALC_mean6", "SunlightColor", "SunColor", "CloudLayers_enabled_mean", "EffectLightingColor", "SkyStaticsColor"]:
            if fld in s:
                x = s[fld]
                line.append(f"{fld.replace('Color','')}={tuple(x['mean_rgb'])}{x['tone']}(S{x['S']})")
        print(" ", t, "; ".join(line))
