"""Export the per-NPC CSV + a few report numbers."""
import os, sys, json, csv, collections
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
sys.path.insert(0, sp)
import nifhdr
inst = r"C:\1. AUTHORIA"
npcs = json.load(open(sp + r"\npc_hair.json"))
outs = {o["fid"]: o for o in json.load(open(sp + r"\npc_outfit.json"))}
vfs = json.load(open(sp + r"\loose_vfs.json"))
LABEL = {"A": "hair physics works now", "B": "SMP hair mesh, face file lacks the physics link",
         "B2": "SMP hair mesh, no face file (made at runtime)", "C": "static hair, SMP version of this style is installed",
         "D": "static hair, no SMP version installed"}
def bucket(n):
    if n["fg_phys"]: return "A"
    if n["hair_phys"]: return "B" if n["fg"] else "B2"
    if n["equiv"]: return "C"
    return "D"
rows = []
for n in npcs:
    o = outs.get(n["fid"], {})
    body = o.get("body") or []
    b = bucket(n)
    rows.append(dict(name=n["name"] or "", editorid=n["eid"] or "", plugin=n["plugin"], formid=n["fid"].split(":")[0],
                     race=n["race"] or "", sex="F" if n["female"] else "M", hair_bucket=b, hair_state=LABEL[b],
                     hair_style=os.path.basename(n["model"] or "") or "(baked only)", hair_family=n["fam"],
                     hair_mesh_from=n["prov"] or "", smp_equivalent=(n["equiv"][0] if n["equiv"] else ""),
                     face_file_from=n["fg_win"] or "(none)", outfit=o.get("outfit_eid") or "",
                     outfit_physics=("yes" if o.get("any_phys") else ("no" if o.get("outfit") else "")),
                     body_piece=(body[0][1] or body[0][0]) if body else "", body_mesh_from=body[0][3] if body else ""))
rows.sort(key=lambda r: (r["name"] == "", r["hair_bucket"], r["name"], r["plugin"]))
with open(os.path.join(inst, "SMP-HAIR-OUTFIT-COVERAGE-20261014.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print("csv rows", len(rows))

# physics kind for the top physics body meshes worn by named NPCs: body-only (3BA/HIMBO body xml) vs cloth
named = [n for n in npcs if n["name"]]
cnt = collections.Counter()
for n in named:
    o = outs.get(n["fid"])
    if not o or not o.get("outfit") or not o["any_phys"]:
        continue
    for p in o["pieces"]:
        if p["phys"] and p.get("mesh"):
            cnt[p["mesh"].lower()] += 1
kind = collections.Counter()
for mesh, v in cnt.most_common(400):
    k = mesh if mesh.startswith("meshes\\") else "meshes\\" + mesh
    if k in vfs:
        try:
            phys, xmls, bsver, h = nifhdr.file_physics(vfs[k][1])
        except Exception:
            continue
        xs = " ".join(xmls).lower()
        if any(t in xs for t in ("3ba", "3bbb", "cbbe", "himbo", "bhunp", "ube")) and not any(t in xs for t in ("skirt", "cloak", "cape", "robe", "dress", "cloth")):
            kind["body-jiggle only"] += v
        else:
            kind["cloth/other xml: " + os.path.basename(xmls[0]) if xmls else "cloth?"] += v
for k, v in kind.most_common(25):
    print(" ", v, k)
