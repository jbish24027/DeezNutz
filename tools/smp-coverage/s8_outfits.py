"""Per-NPC default outfit -> armor pieces -> world meshes -> physics link present?"""
import os, sys, json, re, collections, time
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
sys.path.insert(0, sp)
import nifhdr, bsareader
t0 = time.time()
vfs = json.load(open(sp + r"\loose_vfs.json"))
bsa = json.load(open(sp + r"\bsa_vfs_meshes.json"))
npcs = json.load(open(sp + r"\npc_hair.json"))

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
        if "value" in fl:
            d.setdefault(fl["path"], fl["value"])
    return d

otft, armo, arma, lvli = {}, {}, {}, {}
for r in rows(sp + r"\otft_all.jsonl"):
    f = fields(r)
    otft[r["formid"]] = dict(eid=f.get("EditorID"), items=[v for k, v in f.items() if re.match(r"Items\[\d+\]$", k)], winner=r["winner"])
for r in rows(sp + r"\armo_all.jsonl"):
    f = fields(r)
    armo[r["formid"]] = dict(eid=f.get("EditorID"), name=f.get("Name"), arma=[v for k, v in f.items() if re.match(r"Armature\[\d+\]$", k)],
                             slots=f.get("BodyTemplate.FirstPersonFlags", ""), tmpl=f.get("TemplateArmor"), winner=r["winner"])
for r in rows(sp + r"\arma_all.jsonl"):
    f = fields(r)
    arma[r["formid"]] = dict(eid=f.get("EditorID"), male=f.get("WorldModel[0].File"), female=f.get("WorldModel[1].File"),
                             slots=f.get("BodyTemplate.FirstPersonFlags", ""))
for r in rows(sp + r"\lvli_all.jsonl"):
    f = fields(r)
    lvli[r["formid"]] = [v for k, v in f.items() if re.match(r"Entries\[\d+\]\.Data\.Reference$", k)]
print("otft", len(otft), "armo", len(armo), "arma", len(arma), "lvli", len(lvli))

def expand(fid, depth=0, seen=None):
    seen = seen if seen is not None else set()
    if fid in seen or depth > 6:
        return []
    seen.add(fid)
    if fid in armo:
        return [fid]
    if fid in lvli:
        out = []
        for e in lvli[fid]:
            out.extend(expand(e, depth + 1, seen))
        return out
    return []

mesh_cache = {}
bsa_cache = {}
def norm(p):
    p = p.lower().replace("/", "\\")
    return p if p.startswith("meshes\\") else "meshes\\" + p
def mesh_phys(path):
    k = norm(path)
    if k in mesh_cache:
        return mesh_cache[k]
    res = (None, None)
    if k in vfs:
        m, disk = vfs[k]
        try:
            phys, xmls, bsver, h = nifhdr.file_physics(disk)
            res = (phys, m)
        except Exception:
            res = (None, m)
    elif k in bsa:
        bp, bn = bsa[k]
        b = bsa_cache.get(bp)
        if b is None:
            b = bsa_cache[bp] = bsareader.BSA(bp)
        try:
            phys, xmls, bsver, h = nifhdr.physics_info(b.read(k))
            res = (phys, bn)
        except Exception:
            res = (None, bn)
    mesh_cache[k] = res
    return res

out = []
for n in npcs:
    o = n.get("outfit")
    if not o or o not in otft:
        out.append(dict(fid=n["fid"], outfit=None))
        continue
    pieces = []
    for it in otft[o]["items"]:
        for a in expand(it):
            ar = armo[a]
            src = ar
            if ar["tmpl"] and ar["tmpl"] in armo:
                src = armo[ar["tmpl"]]
            best = None
            for aa in src["arma"]:
                am = arma.get(aa)
                if not am:
                    continue
                mp = (am["female"] if n["female"] else am["male"]) or am["male"] or am["female"]
                if not mp:
                    continue
                ph, prov = mesh_phys(mp)
                if best is None or (ph and not best[0]):
                    best = (ph, prov, mp, am["slots"])
            pieces.append(dict(armo=a, eid=ar["eid"], name=ar["name"], slots=ar["slots"], phys=best[0] if best else None,
                               prov=best[1] if best else None, mesh=best[2] if best else None))
    body = [p for p in pieces if "Body" in (p["slots"] or "").split(", ")]
    out.append(dict(fid=n["fid"], outfit=o, outfit_eid=otft[o]["eid"], pieces=pieces,
                    any_phys=any(p["phys"] for p in pieces), body_phys=any(p["phys"] for p in body),
                    body=[(p["eid"], p["name"], p["phys"], p["prov"]) for p in body]))
json.dump(out, open(sp + r"\npc_outfit.json", "w"))
print("meshes checked", len(mesh_cache), "secs", round(time.time() - t0))
byfid = {n["fid"]: n for n in npcs}
named = [o for o in out if byfid[o["fid"]]["name"]]
c = collections.Counter()
for o in named:
    if o["outfit"] is None: c["no outfit"] += 1
    elif o["any_phys"]: c["outfit has a physics piece"] += 1
    else: c["outfit all static"] += 1
print("NAMED outfit:", dict(c))
c2 = collections.Counter()
for o in out:
    if o["outfit"] is None: c2["no outfit"] += 1
    elif o["any_phys"]: c2["phys"] += 1
    else: c2["static"] += 1
print("ALL outfit:", dict(c2))
print("== static body pieces most worn by named NPCs (eid, name, provider)")
cnt = collections.Counter()
for o in named:
    if o["outfit"] and not o["any_phys"]:
        for (e, nm, ph, pv) in o["body"]:
            cnt[(e, nm, pv)] += 1
for k, v in cnt.most_common(60):
    print(" ", v, k)
print("== physics body pieces most worn by named NPCs")
cnt = collections.Counter()
for o in named:
    if o["outfit"] and o["any_phys"]:
        for (e, nm, ph, pv) in o["body"]:
            if ph: cnt[(e, nm, pv)] += 1
for k, v in cnt.most_common(30):
    print(" ", v, k)
print("== static outfits most used by named NPCs")
cnt = collections.Counter((o["outfit_eid"]) for o in named if o["outfit"] and not o["any_phys"])
for k, v in cnt.most_common(40):
    print(" ", v, k)
