import json, os, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "winners_DEEZ_CS_NUTZ_-_PBR.json")))

def load_jsonl(p):
    rows = []
    with open(p, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for l in lines[1:]:
        if l.strip():
            rows.append(json.loads(l))
    return rows

regions = {}
for p in sorted(os.listdir(os.path.join(HERE, "dumps"))):
    if not p.startswith("REGN__"):
        continue
    for r in load_jsonl(os.path.join(HERE, "dumps", p)):
        fid = r["formid"]
        win = W["REGN"].get(fid, {}).get("winner")
        src = r["source"]
        f = {}
        for x in r["fields"]:
            f[x["path"]] = x.get("value", x.get("note"))
        ws = f.get("Worldspace")
        entries = []
        i = 0
        while f"Weather.Weathers[{i}]" in f or f"Weather.Weathers[{i}].Weather" in f:
            entries.append({"weather": f.get(f"Weather.Weathers[{i}].Weather"),
                            "chance": f.get(f"Weather.Weathers[{i}].Chance"),
                            "global": f.get(f"Weather.Weathers[{i}].Global")})
            i += 1
        regions[fid] = {"editorid": r.get("editorid"), "dump_file": p, "dump_source": src,
                        "pbr_winner": win, "pbr_stack": W["REGN"].get(fid, {}).get("stack"),
                        "worldspace": ws, "weather_entries": entries,
                        "has_weather": f.get("Weather") not in (None, "(absent)")}
json.dump(regions, open(os.path.join(HERE, "regions_pbr.json"), "w"), indent=1)
withw = {k: v for k, v in regions.items() if v["weather_entries"]}
print("regions dumped", len(regions), "with weather lists", len(withw))
for k, v in sorted(withw.items(), key=lambda x: (str(x[1]["worldspace"]), x[1]["editorid"] or "")):
    print(k, v["editorid"], "|ws", v["worldspace"], "|win", v["pbr_winner"], "|n", len(v["weather_entries"]))
