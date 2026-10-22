import json, os, colorsys
from wlib import *

W = winners()
R = json.load(open(os.path.join(HERE, "regions_pbr.json")))

# --- VOLI lookup (PBR winner) ---
VOLI_FILES = {"Astralite Weathers.esp": "VOLI__AstraliteWeathers.jsonl", "Astralite ENB.esp": "VOLI__AstraliteENB.jsonl",
              "NAT-ENB.esp": "VOLI__NATENB.jsonl", "Update.esm": "VOLI__Update.jsonl",
              "Astralite ENB - ECSS.esp": "VOLI__ECSS.jsonl", "Dragonborn.esm": "VOLI__Dragonborn.jsonl"}
voli_by_plugin = {}
for p, fn in VOLI_FILES.items():
    d = {}
    for r in load_jsonl(os.path.join(DUMPS, fn)):
        f = {x["path"]: x.get("value", x.get("note")) for x in r["fields"]}
        d[r["formid"]] = {"editorid": r.get("editorid"), "fields": f}
    voli_by_plugin[p] = d

def voli(fid):
    w = W["VOLI"].get(fid)
    if not w:
        return {"formid": fid, "note": "not in PBR VOLI presence (null or unknown)"}
    p = w["winner"]
    rec = voli_by_plugin.get(p, {}).get(fid)
    if not rec:
        return {"formid": fid, "winner": p, "note": "winner not dumped"}
    f = rec["fields"]
    def fl(k):
        try:
            return round(float(f.get(k)), 4)
        except Exception:
            return f.get(k)
    col = [fl("ColorR"), fl("ColorG"), fl("ColorB")]
    return {"formid": fid, "editorid": rec["editorid"], "winner": p, "stack": w["stack"],
            "color_rgb01": col, "color_rgb255": [round(c * 255) if isinstance(c, float) else c for c in col],
            "intensity": fl("Intensity"), "custom_color_contribution": fl("CustomColorContribution"),
            "density_contribution": fl("DensityContribution"), "density_size": fl("DensitySize"),
            "density_wind_speed": fl("DensityWindSpeed"), "density_falling_speed": fl("DensityFallingSpeed"),
            "phase_contribution": fl("PhaseFunctionContribution"), "phase_scattering": fl("PhaseFunctionScattering"),
            "sampling_range_factor": fl("SamplingRepartitionRangeFactor")}

# --- region membership ---
EXCL_PREFIX = ("Helios_", "FX", "Lux_")
member = {}
region_rows = []
for rid, r in R.items():
    if not r["weather_entries"]:
        continue
    ed = r["editorid"] or ""
    interior = ed.startswith(EXCL_PREFIX) or "Cave" in ed or r["pbr_winner"] == "Lux - Forgotten City.esp"
    region_rows.append({"formid": rid, "editorid": ed, "worldspace": r["worldspace"], "pbr_winner": r["pbr_winner"],
                        "pbr_stack": r["pbr_stack"], "class": "interior/fx" if interior else "exterior",
                        "entries": r["weather_entries"]})
    if interior:
        continue
    for e in r["weather_entries"]:
        member.setdefault(e["weather"], []).append({"region": ed, "region_formid": rid, "worldspace": r["worldspace"],
                                                    "chance": e["chance"], "global": e["global"]})

rot = json.load(open(os.path.join(HERE, "rotating_weather_ids.json")))
out = {}
for fid in rot:
    w = W["WTHR"][fid]
    p = w["winner"]
    rec = plugin_records(p).get(fid)
    if rec is None:
        out[fid] = {"winner": p, "note": "winner not dumped"}
        continue
    c = extract_colour(rec["fields"])
    c["volumetric_resolved"] = {t: voli(v) if v and ":" in v else v for t, v in c["volumetric"].items()}
    # astralite ancestry for comparison
    anc = {}
    for ap in ("Astralite Weathers.esp", "Astralite ENB.esp", "Helios_Astralite.esp",
               "Authoria - Patch - Snowy Holds Seasonal Snowfall.esp", "Wyrmstooth-Astralite-Weather-Patch.esp",
               "Mists of Tamriel.esp", "Skyrim.esm", "Update.esm", "Dawnguard.esm", "Dragonborn.esm"):
        if ap in w["stack"]:
            anc[ap] = True
    colour_source = p
    if p == "Authoria - Patch - Astralite Dawn Warmth.esp":
        st = w["stack"]; colour_source = st[st.index(p) - 1] + " (forwarded verbatim by Dawn Warmth)"
    out[fid] = {"editorid": rec["editorid"], "pbr_winner": p, "colour_author": colour_source, "pbr_stack": w["stack"],
                "regions": member.get(fid, []), **c}
json.dump(out, open(os.path.join(HERE, "astralite_rotating_weathers_colour.json"), "w"), indent=1)
json.dump(region_rows, open(os.path.join(HERE, "astralite_region_weather_lists.json"), "w"), indent=1)

# VOLI table of everything referenced
vt = {}
for fid, v in out.items():
    for t, vv in v.get("volumetric_resolved", {}).items():
        if isinstance(vv, dict):
            vt[vv["formid"]] = vv
json.dump(vt, open(os.path.join(HERE, "astralite_voli_referenced.json"), "w"), indent=1)
print(len(out), "weathers;", len(vt), "VOLI referenced")
