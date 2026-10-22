"""Resolve every NPC's hair head part, whether its baked face carries physics, and whether an installed SMP
equivalent of the same style exists."""
import os, sys, json, re, collections
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
hdpt = json.load(open(sp + r"\hdpt.json"))
hcls = json.load(open(sp + r"\hair_class.json"))
fg = json.load(open(sp + r"\facegen_phys.json"))

def rows(fn):
    with open(fn, encoding="utf-8") as f:
        next(f)
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def fields(r):
    d = {}
    for fl in r.get("fields", []):
        p = fl["path"]
        if "value" in fl:
            d.setdefault(p, fl["value"])
        elif "note_ref" in fl:
            d.setdefault(p, fl["note_ref"])
    return d

# race default head parts by sex
race_def = {}
for r in rows(sp + r"\race_all.jsonl"):
    f = fields(r)
    for sex in (0, 1):
        parts = [v for k, v in f.items() if re.match(r"HeadData\[%d\]\.HeadParts\[\d+\]$" % sex, k)]
        race_def[(r["formid"], sex)] = parts
    race_def[r["formid"]] = f.get("Name") or f.get("EditorID")

def norm_path(p):
    p = p.lower().replace("/", "\\")
    if not p.startswith("meshes\\"):
        p = "meshes\\" + p
    return p

def part_phys(fid, seen=None):
    """physics anywhere in the head part's model or its extra parts"""
    seen = seen or set()
    if fid in seen or fid not in hdpt:
        return False, None
    seen.add(fid)
    h = hdpt[fid]
    if h["model"]:
        c = hcls.get(norm_path(h["model"]))
        if c and c["phys"]:
            return True, c["prov"]
    for e in h["extras"]:
        ok, prov = part_phys(e, seen)
        if ok:
            return True, prov
    return False, None

def stem(path):
    s = os.path.splitext(os.path.basename(path.lower()))[0]
    s = re.sub(r"[^a-z0-9]", "", s)
    return s

# ---- build the SMP style index from every physics hair model file the instance has
smp_styles = {}  # normalised stem -> (path, provider)
for k, v in hcls.items():
    if not v.get("phys"):
        continue
    s = stem(k)
    for suf in ("smp", "hdt"):
        if s.endswith(suf):
            s = s[:-len(suf)]
    smp_styles.setdefault(s, (k, v["prov"]))
print("smp style stems", len(smp_styles))

def family(path, prov):
    p = path.lower()
    if "character assets\\hair" in p:
        return "vanilla"
    if "ks hairdo's\\hdt" in p or (prov or "").startswith("KS Hairdos SMP"):
        return "KS SMP"
    if "ks hairdo's" in p:
        return "KS Hairdos"
    if "hg hairdos" in (prov or "").lower() or "\\hg\\" in p or "hghair" in p:
        return "HG Hairdos"
    if "[dint999]" in p or "dint" in p:
        return "Dint999"
    if "[d] bdor" in p or "bdor" in p:
        return "BDOR (Dint999)"
    if "fuse00" in p:
        return "Fuse00"
    if "sala hairs" in p:
        return "saLa SMP (KS conversions)"
    if "evgmodular" in p:
        return "Modular SMP"
    if "apachii" in p:
        return "Apachii"
    return "other"

npcs = []
stats = collections.Counter()
for r in rows(sp + r"\npc_all.jsonl"):
    f = fields(r)
    fid = r["formid"]
    local, plugin = fid.split(":", 1)
    tflags = f.get("Configuration.TemplateFlags", "") or ""
    flags = f.get("Configuration.Flags", "") or ""
    female = "Female" in flags.split(", ")
    if "Traits" in tflags.split(", ") and f.get("Template"):
        stats["traits_inherited"] += 1
        continue
    race = f.get("Race")
    parts = [v for k, v in f.items() if re.match(r"HeadParts\[\d+\]$", k)]
    hair = None
    for p in parts:
        h = hdpt.get(p)
        if h and h["type"] == "Hair":
            hair = p
            break
    src = "record"
    if hair is None and race:
        for p in race_def.get((race, 1 if female else 0), []):
            h = hdpt.get(p)
            if h and h["type"] == "Hair":
                hair = p; src = "race default"; break
    if hair is None:
        stats["no_hair"] += 1
        continue
    h = hdpt[hair]
    model = h["model"] or ""
    mk = norm_path(model) if model else None
    mc = hcls.get(mk) if mk else None
    prov = mc["prov"] if mc else None
    phys_any, phys_prov = part_phys(hair)
    fam = family(model, prov)
    fgkey = ("meshes\\actors\\character\\facegendata\\facegeom\\%s\\00%s.nif" % (plugin, local)).lower()
    fgi = fg.get(fgkey)
    fg_phys = fgi["phys"] if fgi else None
    fg_win = fgi["winner"] if fgi else None
    # SMP equivalent
    equiv = None
    if phys_any:
        equiv = ("self", phys_prov)
    else:
        s = stem(model)
        if fam == "vanilla" and mc and mc["phys"]:
            equiv = ("same path (Vanilla hair remake SMP)", prov)
        elif s in smp_styles:
            equiv = smp_styles[s]
        else:
            # KS copies often carry the KS stem with a prefix; try stripping leading 'ks'/'hair' tokens
            s2 = re.sub(r"^(ks|hair|hairfemale|hairmale|female|male)", "", s)
            if s2 and s2 in smp_styles:
                equiv = smp_styles[s2]
    npcs.append(dict(fid=fid, plugin=plugin, eid=f.get("EditorID"), name=f.get("Name"), female=female,
                     race=race_def.get(race, race), hair=hair, hair_eid=h["eid"], hair_def=h["defined"],
                     model=model, prov=prov, fam=fam, hair_phys=phys_any, fg=fgkey if fgi else None,
                     fg_phys=fg_phys, fg_win=fg_win, equiv=equiv, src=src, outfit=f.get("DefaultOutfit"),
                     worn=f.get("WornArmor"), winner=r["winner"]))
print(stats, "npcs with hair", len(npcs))
json.dump(npcs, open(sp + r"\npc_hair.json", "w"))

def bucket(n):
    if n["fg_phys"]:
        return "A already physics"
    if n["hair_phys"]:
        return "B SMP hair, face bake lacks link" if n["fg"] else "B2 SMP hair, no face bake"
    if n["equiv"]:
        return "C static hair, SMP equivalent installed"
    return "D static hair, no equivalent installed"
named = [n for n in npcs if n["name"]]
c_all = collections.Counter(bucket(n) for n in npcs)
c_named = collections.Counter(bucket(n) for n in named)
print("ALL", sorted(c_all.items()))
print("NAMED", sorted(c_named.items()))
print("by family (named):")
for k, v in collections.Counter((n["fam"], bucket(n)) for n in named).most_common(40):
    print(" ", v, k)
print("no-bake named by provider of hair:")
for k, v in collections.Counter((n["prov"], bucket(n)) for n in named if bucket(n).startswith("D")).most_common(25):
    print(" ", v, k)
print("D named styles (stem) most used:")
for k, v in collections.Counter((n["fam"], stem(n["model"])) for n in named if bucket(n).startswith("D")).most_common(40):
    print(" ", v, k)
print("face winners for C+D named:")
for k, v in collections.Counter(n["fg_win"] for n in named if bucket(n)[0] in "CD").most_common(30):
    print(" ", v, k)
