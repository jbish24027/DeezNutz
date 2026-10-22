import json, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
MODS = "C:/1. AUTHORIA/mods"
inv = json.load(open(HERE + "/inventory.json"))
a = json.load(open(HERE + "/winners_picta.json"))
b = json.load(open(HERE + "/winners_pbr.json"))
short = {
 "[NoDelete] Astralite Weathers": "AW", "[NoDelete] Soul Core Plugin and Assets": "SC",
 "[NoDelete] Mists of Tamriel": "MoT", "No More Blinding Fog": "NMBF", "[NoDelete] Picta - Assets 4K": "P4K",
 "[NoDelete] Picta - Weathers of Aurbis 1.1.1 (shipped)": "P111", "[NoDelete] Astralite Weathers - 4K Clouds": "AW4K",
 "Lux (main) - rerun": "LUX", "Picta Series - Improved Sky Meshes": "PISM", "Praedys Sky AIO": "PRAEDYS",
}
def s(n):
    return short.get(n, n)
def realpath(mod, rel):
    root = MODS + "/" + mod
    cur = root
    for seg in rel.split("/"):
        try:
            ents = {e.lower(): e for e in os.listdir(cur)}
        except Exception:
            return None
        if seg in ents: cur += "/" + ents[seg]
        else: return None
    return cur
def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()[:8] if p and os.path.isfile(p) else None
srcs = ["[NoDelete] Astralite Weathers", "[NoDelete] Soul Core Plugin and Assets", "[NoDelete] Mists of Tamriel", "No More Blinding Fog"]
paths = []
for sname in srcs:
    for f in inv[sname]:
        r = f["rel"].lower()
        if r.startswith(("meshes/", "textures/")) and r not in paths:
            paths.append(r)
rows = []
for p in sorted(paths):
    if p.startswith("textures/sky/") and ("cloud" in p or "masser" in p or "secunda" in p or "sunset" in p or "aurora" in p or "sovn" in p or "star" in p or "galaxy" in p or "constell" in p or "moon" in p or p.endswith("sun.dds") or "sunglare" in p):
        cls = "SKYTEX"
    else:
        cls = ""
    hashes = {}
    for m in set(a[p]["loose"] + b[p]["loose"]):
        if m.startswith("Data") : continue
        hashes[s(m)] = md5(realpath(m, p))
    row = {"path": p, "cls": cls, "picta_win": s(a[p]["winner"]), "pbr_win": s(b[p]["winner"]),
           "picta_loose": [s(x) for x in a[p]["loose"]], "pbr_loose": [s(x) for x in b[p]["loose"]],
           "picta_bsa": a[p]["bsa"][:2], "pbr_bsa": b[p]["bsa"][:2], "md5": hashes}
    rows.append(row)
json.dump(rows, open(HERE + "/asset_matrix.json", "w"), indent=1)
for r in rows:
    if r["cls"] == "SKYTEX": continue
    print(f"{r['path']}\n   PICTA win={r['picta_win']} loose={r['picta_loose']} bsa={[x.split(' [')[0] for x in r['picta_bsa']]}\n   PBR   win={r['pbr_win']} loose={r['pbr_loose']} bsa={[x.split(' [')[0] for x in r['pbr_bsa']]}\n   md5={r['md5']}")
print("---- sky textures (AW/SC) ----")
for r in rows:
    if r["cls"] != "SKYTEX": continue
    print(f"{r['path']}: PICTA={r['picta_win']} PBR={r['pbr_win']} md5={r['md5']}")
