import json, os, colorsys, math
S = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(S, "picta_palette_model.json")))
C = json.load(open(os.path.join(S, "regn_weather_census.json")))
tam = C["by_worldspace"]["00003C:Skyrim.esm"]
w = {k.split(":")[0]: v for k, v in tam.items() if "Picta" in k}
P = ["Dawn", "Sunrise", "Day", "Sunset", "Dusk", "Night"]
def hsv(c):
    m = max(c)
    if m <= 0: return (0, 0, 0)
    h, s, v = colorsys.rgb_to_hsv(*[x / m for x in c]); return (h * 360, s, m)
def chroma_mean(items):
    # weighted mean of normalised colour (direction), plus mean luminance
    tw = sum(wt for _, wt in items) or 1
    acc = [0, 0, 0]; lum = 0
    for c, wt in items:
        L = sum(c) / 3 or 1e-9
        for i in range(3): acc[i] += c[i] / L * wt
        lum += L * wt
    n = [a / tw for a in acc]; Lm = lum / tw
    return [x * Lm for x in n]
out = {}
for p in P:
    row = {}
    for key in ["sky_zenith", "sky_horizon_side", "sky_horizon_sunward", "sunlight", "fog_far", "cloud_base", "volumetric_fog_mesh_tint"]:
        items = [(M[k]["periods"][p][key], w.get(k, 0)) for k in M]
        c = chroma_mean(items)
        h, s, v = hsv(c)
        row[key] = {"rgb_linear_weighted": [round(x, 3) for x in c], "hue_deg": round(h), "sat": round(s, 2), "peak": round(v, 3)}
    items = [(M[k]["periods"][p]["ambient"]["side"], w.get(k, 0)) for k in M]
    c = chroma_mean(items); h, s, v = hsv(c)
    row["ambient_side"] = {"rgb_linear_weighted": [round(x, 3) for x in c], "hue_deg": round(h), "sat": round(s, 2), "peak": round(v, 3)}
    out[p] = row
json.dump({"weights": "Tamriel REGN weather-list membership counts (picta weathers only)", "periods": out}, open(os.path.join(S, "picta_palette_summary.json"), "w"), indent=1)
for p in P:
    print(p)
    for k, v in out[p].items():
        print(f"   {k:26} hue {v['hue_deg']:4} sat {v['sat']:.2f} peak {v['peak']:.3f}  rgb {v['rgb_linear_weighted']}")
