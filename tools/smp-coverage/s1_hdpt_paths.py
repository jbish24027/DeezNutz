import json, sys, collections
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"

def rows(fn):
    with open(fn, encoding="utf-8") as f:
        first = True
        for line in f:
            line = line.strip()
            if not line:
                continue
            if first:
                first = False
                continue
            yield json.loads(line)

def fields(r):
    d = {}
    for fl in r.get("fields", []):
        p = fl["path"]
        if "value" in fl:
            d.setdefault(p, fl["value"])
        elif "note" in fl:
            d.setdefault(p + "#note", fl["note"])
    return d

hdpt = {}
types = collections.Counter()
for r in rows(sp + r"\hdpt_all.jsonl"):
    f = fields(r)
    extras = [v for k, v in f.items() if k.startswith("ExtraParts[") and not k.endswith("#note")]
    hdpt[r["formid"]] = dict(eid=f.get("EditorID"), name=f.get("Name"), type=f.get("Type"),
                            model=f.get("Model.File"), flags=f.get("Flags", ""), extras=extras,
                            races=f.get("ValidRaces"), winner=r["winner"], defined=r["formid"].split(":", 1)[1])
    types[f.get("Type")] += 1
print("HDPT total", len(hdpt), types)
json.dump(hdpt, open(sp + r"\hdpt.json", "w"), indent=0)

hair = {k: v for k, v in hdpt.items() if v["type"] == "Hair"}
print("Hair HDPT", len(hair))
paths = set()
for v in hair.values():
    if v["model"]:
        paths.add(v["model"].lower().replace("/", "\\"))
    for e in v["extras"]:
        ev = hdpt.get(e)
        if ev and ev["model"]:
            paths.add(ev["model"].lower().replace("/", "\\"))
print("unique hair model paths (incl. extras)", len(paths))
with open(sp + r"\hair_paths.txt", "w") as f:
    for p in sorted(paths):
        f.write("meshes\\" + p + "\n")
# by defining plugin
c = collections.Counter(v["defined"] for v in hair.values())
for k, n in c.most_common(60):
    print(n, k)
