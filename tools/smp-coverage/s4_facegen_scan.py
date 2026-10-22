"""Scan every facegen head mesh the VFS provides for the HDT-SMP physics link (loose + BSA winners)."""
import os, json, time, sys, collections
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
sys.path.insert(0, sp)
import nifhdr, bsareader
inst = r"C:\1. AUTHORIA"
t0 = time.time()
doc = json.load(open(sp + r"\facegeom_vfs.json", encoding="utf-8"))
res = doc["results"]
print("facegeom entries", len(res))

# index BSA files on disk: name -> path (enabled mods + stock data)
mods = [l.rstrip("\r\n")[1:] for l in open(sp + r"\modlist.txt", encoding="utf-8") if l.startswith("+")]
bsa_paths = {}
for m in mods:
    root = os.path.join(inst, "mods", m)
    try:
        for e in os.listdir(root):
            if e.lower().endswith(".bsa"):
                bsa_paths.setdefault(e.lower(), []).append(os.path.join(root, e))
    except OSError:
        pass
for e in os.listdir(os.path.join(inst, "Stock Game", "Data")):
    if e.lower().endswith(".bsa"):
        bsa_paths.setdefault(e.lower(), []).append(os.path.join(inst, "Stock Game", "Data", e))

out = {}
bsa_groups = collections.defaultdict(list)
nloose = 0
for r in res:
    p = r["path"]
    w = r.get("winner")
    if not r.get("exists") or not w:
        out[p.lower()] = dict(winner=None, kind=None, phys=None)
        continue
    if w["kind"] == "loose":
        if w["name"].lower() == "overwrite":
            disk = os.path.join(inst, "overwrite", p)
        else:
            disk = os.path.join(inst, "mods", w["name"], p)
        try:
            phys, xmls, bsver, h = nifhdr.file_physics(disk)
            out[p.lower()] = dict(winner=w["name"], kind="loose", phys=phys, xml=xmls[:3], bsver=bsver)
        except Exception as ex:
            out[p.lower()] = dict(winner=w["name"], kind="loose", phys=None, err=str(ex)[:80])
        nloose += 1
    else:
        bsa_groups[w["name"]].append(p)
print("loose scanned", nloose, "bsa groups", len(bsa_groups), "secs", round(time.time() - t0))
for bname, paths in sorted(bsa_groups.items(), key=lambda kv: -len(kv[1])):
    cands = bsa_paths.get(bname.lower())
    if not cands:
        for p in paths:
            out[p.lower()] = dict(winner=bname, kind="BSA", phys=None, err="bsa not found on disk")
        print("BSA not found", bname, len(paths))
        continue
    # if several mods ship the same BSA name, take the highest-priority enabled one (last in modlist order = lowest; first = highest)
    bpath = cands[0]
    try:
        b = bsareader.BSA(bpath)
    except Exception as ex:
        for p in paths:
            out[p.lower()] = dict(winner=bname, kind="BSA", phys=None, err="bsa open: " + str(ex)[:60])
        print("BSA open fail", bname, ex)
        continue
    ok = 0
    for p in paths:
        key = p.lower()
        if key not in b.files:
            out[key] = dict(winner=bname, kind="BSA", phys=None, err="not in bsa dir")
            continue
        try:
            data = b.read(key)
            phys, xmls, bsver, h = nifhdr.physics_info(data)
            out[key] = dict(winner=bname, kind="BSA", phys=phys, xml=xmls[:3], bsver=bsver)
            ok += 1
        except Exception as ex:
            out[key] = dict(winner=bname, kind="BSA", phys=None, err=str(ex)[:80])
    b.close()
    print("BSA", bname, len(paths), "ok", ok, "secs", round(time.time() - t0))
json.dump(out, open(sp + r"\facegen_phys.json", "w"))
c = collections.Counter((v["kind"], v["phys"]) for v in out.values())
print(c)
print("done secs", round(time.time() - t0))
