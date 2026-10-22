"""For every installed graft: the record hair's extra-part hairline, its live model file, and the vertex counts of the bake's hairline shape vs the model's shape."""
import json, os, sys, struct, collections
sys.path.insert(0, "C:/1. AUTHORIA/_tools/smp-coverage")
import hairgraft, nifrw
BS = chr(92)
sp = "C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/8714b13a-8cba-4f6e-a284-eaf1cd40c73c/scratchpad"
npcs = {n["fid"]: n for n in json.load(open(sp + "/npc_hair.json"))}
grafted = json.load(open(sp + "/staging/final/grafted_fids.json"))
vfs = json.load(open(sp + "/loose_vfs.json"))
bsa = json.load(open(sp + "/bsa_vfs_meshes.json"))
hd = {}
for line in open(sp + "/hdpt_all.jsonl", encoding="utf-8"):
    r = json.loads(line)
    if r.get("type") != "HeadPart": continue
    f = {x["path"]: x.get("value") for x in r["fields"]}
    hd[r["formid"]] = dict(eid=r["editorid"], model=f.get("Model.File"), extras=[v for k, v in f.items() if k.startswith("ExtraParts[") and v], type=f.get("Type"), flags=f.get("Flags"))
print("hdpt records:", len(hd))
root = "C:/1. AUTHORIA/mods/Authoria - SMP Hair Grafts"
def norm(p): return ("meshes" + BS + p.lower().replace("/", BS)) if not p.lower().startswith("meshes") else p.lower().replace("/", BS)
cache = {}
def model_nverts(path):
    if path in cache: return cache[path]
    try:
        d = nifrw.Doc(path); sh = hairgraft.shapes(d)
        v = [(d.name_of(i), nifrw.parse_shape_hdr(d.blocks[i][1]).get("nvert")) for i in sh]
    except Exception as e:
        v = ("ERR", str(e))
    cache[path] = v; return v
jobs, stats = [], collections.Counter()
for n_i, fid in enumerate(grafted):
    n = npcs[fid]
    h = hd.get(n["hair"])
    if not h: stats["no hair hdpt"] += 1; continue
    hls = [hd[x] for x in h["extras"] if x in hd and (hd[x]["model"] or "").lower().find("hairline") >= 0 or (x in hd and "hairline" in hd[x]["eid"].lower())]
    if not hls: stats["no hairline extra part"] += 1; continue
    bake = os.path.join(root, "meshes/actors/character/facegendata/facegeom", n["plugin"], "00%s.nif" % fid.split(":")[0])
    bp = bake if len(bake) < 240 else BS + BS + "?" + BS + bake.replace("/", BS)
    try:
        d = nifrw.Doc(bp)
    except Exception as e:
        stats["bake unreadable"] += 1; continue
    shp = {d.name_of(i): nifrw.parse_shape_hdr(d.blocks[i][1]).get("nvert") for i in hairgraft.shapes(d)}
    for hl in hls:
        key = norm(hl["model"])
        win = vfs.get(key)
        src = win[1] if win else None
        prov = win[0] if win else ("BSA" if key in bsa else None)
        if hl["eid"] not in shp:
            stats["bake lacks hairline shape"] += 1; continue
        if not src:
            stats["hairline model not loose (BSA/missing): " + str(prov)] += 1; continue
        mv = model_nverts(src)
        mn = mv[0][1] if isinstance(mv, list) and mv else None
        same = (mn == shp[hl["eid"]])
        stats["same vertex count" if same else "differs"] += 1
        stats["provider " + prov] += 1
        jobs.append(dict(fid=fid, name=n["name"], plugin=n["plugin"], bake=bake, hairline_eid=hl["eid"], model=src, provider=prov, bake_nverts=shp[hl["eid"]], model_nverts=mn, model_shapes=mv if isinstance(mv, list) else None, same=same))
    if n_i % 500 == 0: print("...", n_i, dict(stats), flush=True)
json.dump(jobs, open(sp + "/staging/hairline_jobs.json", "w"), indent=0)
print("jobs:", len(jobs)); print(json.dumps(stats, indent=1))
print("multi-shape hairline models:", sum(1 for j in jobs if j["model_shapes"] and len(j["model_shapes"]) > 1))
print("examples:", json.dumps(jobs[:3], indent=1)[:1500])
