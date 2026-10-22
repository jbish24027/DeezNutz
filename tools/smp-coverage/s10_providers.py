"""(1) which hair HDPTs have no model; (2) for the static body meshes worn most, does ANY enabled mod ship a physics copy?"""
import os, sys, json, collections
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
sys.path.insert(0, sp)
import nifhdr
inst = r"C:\1. AUTHORIA"
hdpt = json.load(open(sp + r"\hdpt.json"))
npcs = json.load(open(sp + r"\npc_hair.json"))
outs = json.load(open(sp + r"\npc_outfit.json"))
mods_hi_first = [l.rstrip("\r\n")[1:] for l in open(sp + r"\modlist.txt", encoding="utf-8") if l.startswith("+")]

print("== hair head parts with NO model used by named NPCs")
c = collections.Counter((n["hair"], n["hair_eid"], hdpt[n["hair"]]["winner"], len(hdpt[n["hair"]]["extras"])) for n in npcs if n["name"] and not n["model"])
for k, v in c.most_common(15):
    print(" ", v, k)

def providers(rel):
    out = []
    for m in mods_hi_first:
        p = os.path.join(inst, "mods", m, rel)
        if os.path.isfile(p):
            try:
                ph = nifhdr.file_physics(p)[0]
            except Exception:
                ph = None
            out.append((m, ph))
    return out

byfid = {n["fid"]: n for n in npcs}
print("== static BODY meshes worn by named NPCs: all loose providers (winner first) and whether a physics copy exists")
cnt = collections.Counter()
for o in outs:
    n = byfid[o["fid"]]
    if not n["name"] or not o.get("outfit") or o["any_phys"]:
        continue
    for p in o["pieces"]:
        if "Body" in (p["slots"] or "").split(", ") and p.get("mesh") and p["phys"] is False:
            cnt[(p["mesh"].lower(), p["name"] or p["eid"])] += 1
rescue = []
for (mesh, name), v in cnt.most_common(70):
    rel = mesh if mesh.startswith("meshes\\") else "meshes\\" + mesh
    prov = providers(rel)
    physcopies = [m for m, ph in prov if ph]
    print(" ", v, name, "|", os.path.basename(mesh), "| winner:", prov[0][0] if prov else "BSA/none", "| physics copies:", physcopies[:3])
    if physcopies:
        rescue.append((v, name, mesh, prov[0][0] if prov else None, physcopies))
json.dump(rescue, open(sp + r"\outfit_rescue.json", "w"), indent=1)
print("== static vanilla-family hair meshes (bucket D): any physics provider?")
cnt = collections.Counter()
for n in npcs:
    if n["name"] and not n["fg_phys"] and not n["hair_phys"] and not n["equiv"] and n["fam"] == "vanilla":
        cnt[n["model"].lower()] += 1
for mesh, v in cnt.most_common(25):
    rel = "meshes\\" + mesh
    prov = providers(rel)
    print(" ", v, os.path.basename(mesh), "| providers:", [(m[:40], ph) for m, ph in prov][:5])
