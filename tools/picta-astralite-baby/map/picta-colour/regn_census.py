import re
import json, collections, sys
S = r"C:/Users/User/AppData/Local/Temp/claude/C--Users-User--claude-spares-spare-39aXjK/91294a0d-ce03-47eb-8c5f-7425e9bd2ed4/scratchpad/baby/map/picta-colour/"
lines = open(S + "regn_weather_picta.jsonl", encoding="utf-8").read().splitlines()
rows = [json.loads(l) for l in lines[1:]]
weather_use = collections.Counter()
weather_regions = collections.defaultdict(set)
ws_of = {}
by_ws = collections.defaultdict(collections.Counter)
for r in rows:
    w = []; ws = None
    for f in r["fields"]:
        if re.fullmatch(r"Weather\.Weathers\[\d+\]\.Weather", f["path"]):
            w.append(f.get("value"))
        if f["path"] == "Worldspace":
            ws = f.get("value")
    for x in w:
        weather_use[x] += 1
        weather_regions[x].add(r.get("editorid") or r["formid"])
        by_ws[ws][x] += 1
out = {"weather_region_count": dict(weather_use.most_common()),
       "by_worldspace": {str(k): dict(v.most_common()) for k, v in by_ws.items()},
       "regions_per_weather": {k: sorted(v) for k, v in weather_regions.items()}}
json.dump(out, open(S + "regn_weather_census.json", "w"), indent=1)
for k, v in by_ws.items():
    print("WS", k, "regions-weather pairs", sum(v.values()))
    for w, n in v.most_common(60):
        print("   ", w, n)
