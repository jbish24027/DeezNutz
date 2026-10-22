"""Classify every hair-type HDPT model (and its extra parts) as physics / static, with the file's provider."""
import os, sys, json, time, collections, re
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
sys.path.insert(0, sp)
import nifhdr, bsareader
inst = r"C:\1. AUTHORIA"
t0 = time.time()
vfs = json.load(open(sp + r"\loose_vfs.json"))
hdpt = json.load(open(sp + r"\hdpt.json"))

# ---- BSA index (directory only) over enabled mods + stock data
mods_hi_first = [l.rstrip("\r\n")[1:] for l in open(sp + r"\modlist.txt", encoding="utf-8") if l.startswith("+")]
active_plugins = []
for l in open(os.path.join(inst, "profiles", "DEEZ CS NUTZ - PICTA", "plugins.txt"), encoding="utf-8"):
    l = l.strip()
    if l.startswith("*"):
        active_plugins.append(l[1:].lower())
plug_rank = {p: i for i, p in enumerate(active_plugins)}
implicit = ["skyrim.esm", "update.esm", "dawnguard.esm", "hearthfires.esm", "dragonborn.esm"]
for i, p in enumerate(implicit):
    plug_rank.setdefault(p, -100 + i)

def bsa_plugin(bsaname):
    base = bsaname[:-4].lower()
    for suffix in (" - textures", " - meshes", " - animations", " - sounds", " - voices", " - interface", " - misc", " - shaders"):
        if base.endswith(suffix):
            base = base[:-len(suffix)]
    for ext in (".esp", ".esm", ".esl"):
        if base + ext in plug_rank:
            return base + ext
    return None

bsa_index = {}  # lower path -> (bsa path, bsa name, rank)
nb = 0
cands = []
for m in mods_hi_first:
    root = os.path.join(inst, "mods", m)
    try:
        for e in os.listdir(root):
            if e.lower().endswith(".bsa"):
                cands.append((e, os.path.join(root, e), m))
    except OSError:
        pass
seen_names = set()
loaded = []
for e, p, m in cands:  # highest priority mod first; same-name BSA from a lower mod is hidden
    if e.lower() in seen_names:
        continue
    seen_names.add(e.lower())
    pl = bsa_plugin(e)
    if pl is None:
        continue
    loaded.append((e, p, plug_rank[pl]))
stock = os.path.join(inst, "Stock Game", "Data")
for e in os.listdir(stock):
    if e.lower().endswith(".bsa") and e.lower() not in seen_names and e.lower().startswith("skyrim - "):
        loaded.append((e, os.path.join(stock, e), -200))
print("loaded BSAs", len(loaded))
for e, p, rank in loaded:
    try:
        b = bsareader.BSA(p)
    except Exception as ex:
        print("bsa fail", e, ex); continue
    for k in b.files:
        if not k.startswith("meshes\\"):
            continue
        cur = bsa_index.get(k)
        if cur is None or rank > cur[2]:
            bsa_index[k] = (p, e, rank)
    b.close()
    nb += 1
print("bsa index paths", len(bsa_index), "from", nb, "archives", "secs", round(time.time() - t0))
json.dump({k: [v[0], v[1]] for k, v in bsa_index.items()}, open(sp + r"\bsa_vfs_meshes.json", "w"))

# ---- classify each unique hair-related model path
paths = [l.strip() for l in open(sp + r"\hair_paths.txt")]
cls = {}
bsa_cache = {}
for p in paths:
    k = p.lower()
    if k in vfs:
        m, disk = vfs[k]
        try:
            phys, xmls, bsver, h = nifhdr.file_physics(disk)
            cls[k] = dict(prov=m, kind="loose", phys=phys, xml=xmls[:2], bsver=bsver)
        except Exception as ex:
            cls[k] = dict(prov=m, kind="loose", phys=None, err=str(ex)[:60])
    elif k in bsa_index:
        bp, bn, rank = bsa_index[k]
        b = bsa_cache.get(bp)
        if b is None:
            b = bsa_cache[bp] = bsareader.BSA(bp)
        try:
            data = b.read(k)
            phys, xmls, bsver, h = nifhdr.physics_info(data)
            cls[k] = dict(prov=bn, kind="BSA", phys=phys, xml=xmls[:2], bsver=bsver)
        except Exception as ex:
            cls[k] = dict(prov=bn, kind="BSA", phys=None, err=str(ex)[:60])
    else:
        cls[k] = dict(prov=None, kind="absent", phys=None)
for b in bsa_cache.values():
    b.close()
json.dump(cls, open(sp + r"\hair_class.json", "w"))
c = collections.Counter((v["kind"], v["phys"]) for v in cls.values())
print(c, "secs", round(time.time() - t0))
# per provider summary of hair HDPT model files
prov = collections.Counter()
for v in cls.values():
    prov[(v["prov"], v["phys"])] += 1
for (pv, ph), n in prov.most_common(70):
    print(n, ph, pv)
