"""Build PBR-effective Astralite weather set and Picta-lane rotating set; compare fog fields by class.
Outputs weather_fog_compare.json + prints a class summary.  Read-only (reads housecarl jsonl dumps)."""
import json, os, re, statistics as st, collections
H = os.path.dirname(os.path.abspath(__file__))
def load(fn):
    rows = [json.loads(l) for l in open(os.path.join(H, fn), encoding="utf-8")][1:]
    out = {}
    for r in rows:
        f = {}
        for x in r["fields"]:
            f[x["path"]] = x.get("value", x.get("note"))
        out[r["formid"]] = {"editorid": r.get("editorid"), "src": r.get("source") or fn, "f": f}
    return out
# PBR-lane effective: later overrides earlier (whole-record)
order = ["wthr_astralite_aw.jsonl", "wthr_astralite_enb.jsonl", "wthr_ecss.jsonl", "wthr_helios_astralite.jsonl",
         "wthr_graycowl.jsonl", "wthr_snowyholds.jsonl", "wthr_dawnwarmth.jsonl"]
pbr = {}
for fn in order:
    for k, v in load(fn).items():
        v["src"] = fn.replace("wthr_", "").replace(".jsonl", "")
        pbr[k] = v
picta = load("wthr_picta_lane_winners.jsonl")
# rotating sets
def regn_weathers(fn):
    rows = [json.loads(l) for l in open(os.path.join(H, fn), encoding="utf-8")][1:]
    res = {}
    for r in rows:
        ws = []
        for x in r["fields"]:
            m = re.match(r"Weather\.Weathers\[(\d+)\]\.Weather$", x["path"])
            if m and "value" in x:
                ws.append(x["value"])
        res[r["formid"]] = ws
    return res
regn = {}
for fn in ["regn_aenb.jsonl", "regn_swf_astralite.jsonl", "regn_snowyholds.jsonl"]:
    for k, v in regn_weathers(fn).items():
        if v: regn[k] = v
ast_rot = collections.Counter(w for ws in regn.values() for w in ws)
pic_rot = [k for k, v in picta.items() if v["editorid"] and (v["editorid"].startswith("PIC_WTHR_MASTER_") or v["editorid"].startswith("PIC_WTHR_SUMMER_"))]
KEYS = ["FogDistanceDayNear", "FogDistanceDayFar", "FogDistanceDayPower", "FogDistanceDayMax",
        "FogDistanceNightNear", "FogDistanceNightFar", "FogDistanceNightPower", "FogDistanceNightMax"]
def num(x):
    try: return float(x)
    except: return None
def cls_ast(e):
    e = e or ""
    if "Fog" in e: return "fog"
    if "StormSnow" in e or "Blizzard" in e: return "storm_snow"
    if "StormRain" in e or "Storm" in e: return "storm_rain"
    if "OvercastSnow" in e or "CloudySnow" in e or "Snow" in e: return "snow"
    if "OvercastRain" in e or "Rain" in e: return "overcast_rain"
    if "Overcast" in e: return "overcast"
    if "Cloudy" in e and e.endswith("_A"): return "cloudy_aurora"
    if "Cloudy" in e: return "cloudy"
    if "Clear" in e and e.endswith("_A"): return "clear_aurora"
    if "Clear" in e: return "clear"
    return "other"
def cls_pic(e):
    e = e or ""
    if "Fog" in e or "Mist" in e: return "fog"
    if "Storm_Snow" in e or "Storm_Cold" in e: return "storm_snow"
    if "Storm" in e and "Cloudy" not in e: return "storm_rain"
    if "Snow" in e: return "snow"
    if "Rain" in e: return "overcast_rain"
    if "Overcast" in e: return "overcast"
    if "Aurora" in e and "Cloudy" in e: return "cloudy_aurora"
    if "Cloudy" in e: return "cloudy"
    if "Aurora" in e: return "clear_aurora"
    if "Clear" in e: return "clear"
    return "other"
def rec(k, v, side):
    f = v["f"]
    d = {"formid": k, "editorid": v["editorid"], "src": v["src"], "flags": f.get("Flags")}
    for kk in KEYS: d[kk] = num(f.get(kk))
    for c in ["FogNearColor", "FogFarColor"]:
        for t in ["Sunrise", "Day", "Sunset", "Night"]:
            d[f"{c}.{t}"] = f.get(f"{c}.{t}")
    d["Precipitation"] = f.get("Precipitation"); d["VisualEffect"] = f.get("VisualEffect")
    for t in ["Sunrise", "Day", "Sunset", "Night"]:
        d[f"VOLI.{t}"] = f.get(f"VolumetricLighting.{t}")
    sk = [x for kk, x in f.items() if kk.startswith("SkyStatics[")]
    d["SkyStatics_count"] = len(sk)
    d["SkyStatics_MoT"] = sum(1 for x in sk if isinstance(x, str) and "Mists of Tamriel" in x)
    return d
out = {"astralite_pbr_effective": [], "picta_lane": []}
for k, n in ast_rot.most_common():
    v = pbr.get(k)
    if not v:
        continue
    r = rec(k, v, "ast"); r["class"] = cls_ast(v["editorid"]); r["region_refs"] = n
    out["astralite_pbr_effective"].append(r)
for k in pic_rot:
    r = rec(k, picta[k], "pic"); r["class"] = cls_pic(picta[k]["editorid"]); r["winner"] = picta[k]["src"]
    out["picta_lane"].append(r)
missing = [k for k in ast_rot if k not in pbr]
out["astralite_rotating_not_in_astralite_plugins"] = missing
json.dump(out, open(os.path.join(H, "weather_fog_compare.json"), "w"), indent=1)
# summary
def summ(rows):
    by = collections.defaultdict(list)
    for r in rows: by[r["class"]].append(r)
    res = {}
    for c, rs in sorted(by.items()):
        res[c] = {"n": len(rs)}
        for kk in KEYS:
            vals = [r[kk] for r in rs if r[kk] is not None]
            if vals: res[c][kk] = (round(st.median(vals), 3), round(min(vals), 3), round(max(vals), 3))
        res[c]["MoT_skystatics"] = sum(1 for r in rs if r["SkyStatics_MoT"])
        res[c]["visfx"] = collections.Counter(str(r["VisualEffect"]) for r in rs).most_common(4)
    return res
A = summ(out["astralite_pbr_effective"]); P = summ(out["picta_lane"])
print("missing (rotating ids not defined/overridden by any Astralite-lane plugin dumped):", missing)
for c in sorted(set(A) | set(P)):
    print("=====", c)
    print("  AST", json.dumps(A.get(c)))
    print("  PIC", json.dumps(P.get(c)))
print("\nPicta rotating detail:")
for r in out["picta_lane"]:
    print(" ", r["editorid"], r["winner"], [r[k] for k in KEYS], "VFX", r["VisualEffect"], "prec", r["Precipitation"], "sky", r["SkyStatics_count"])
print("\nAstralite rotating detail:")
for r in out["astralite_pbr_effective"]:
    print(" ", r["editorid"], r["src"], r["region_refs"], [r[k] for k in KEYS], "VFX", r["VisualEffect"], "prec", r["Precipitation"], "sky", r["SkyStatics_count"], "MoT", r["SkyStatics_MoT"])
