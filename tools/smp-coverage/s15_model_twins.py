"""Model-twin fix for grafted NPCs whose hair head part still points at a STATIC mesh on a different path
than the SMP twin that was grafted into their face bake (s13 bucket C).

Why: at runtime the engine loads the head part's model nif. FSMP (processGeometry) takes the facegen shape's
bone names 0-7 from the game's facegen extra data (filled from that model) and bone 8+ from that model's own
skin; a model with fewer bones than the grafted shape leaves the remaining bone slots as garbage, and the
physics build (generateMeshBody) then dereferences them -> CTD (Fralia Gray-Mane, 2026-10-14 16:09).

Fix: give the engine a model whose bones equal the grafted shape's: a copy of the SMP twin placed at the static
model path (main hair + every grafted companion piece such as the HL). When the graft added the KS-style
VirtualHead shape (which makes FSMP read the per-NPC facegen xml), the placed copy has its own physics tag
removed so FSMP builds exactly one system; VHR-style (bone-only xml, no VirtualHead) copies keep the tag.

usage: python -I s15_model_twins.py <staging_root> [--apply]
  stages <staging_root>\\Authoria - SMP Hair Grafts\\meshes\\... and a report; --apply copies the staged tree
  into mods\\Authoria - SMP Hair Grafts (refuses while MO2 or the game run).
"""
import os, sys, json, struct, shutil, subprocess, collections, csv
tools = r"C:\1. AUTHORIA\_tools\smp-coverage"
sys.path.insert(0, tools)
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
import s13_graft_jobs as s13
import nifrw, hairgraft, nifhdr

inst = s13.inst
MODNAME = s13.MODNAME
hdpt, npcs = s13.hdpt, s13.npcs
GRAFT_FG = os.path.join(inst, "mods", MODNAME, "meshes", "actors", "character", "facegendata", "facegeom")


def grafted_fids():
    out = []
    for plug in sorted(os.listdir(GRAFT_FG)):
        for fn in sorted(os.listdir(os.path.join(GRAFT_FG, plug))):
            if fn.lower().endswith(".nif"):
                out.append(fn[2:8] + ":" + plug)
    return out


def shape_bones(doc, shape_idx):
    sh = nifrw.parse_shape_hdr(doc.blocks[shape_idx][1])
    if sh["skin"] < 0:
        return []
    sb = doc.blocks[sh["skin"]][1]
    nb = struct.unpack_from("<I", sb, 12)[0]
    return [hairgraft.node_name(doc, x) for x in struct.unpack_from("<%di" % nb, sb, 16)]


def first_shape_bones(path):
    d = nifrw.Doc(path)
    sh = hairgraft.shapes(d)
    if not sh:
        return None, 0
    i = sh[0]
    return shape_bones(d, i), nifrw.parse_shape_hdr(d.blocks[i][1])["nvert"]


def bake_shape_bones(bake_path, name):
    d = nifrw.Doc(bake_path)
    for i in hairgraft.shapes(d):
        if d.name_of(i) == name:
            return shape_bones(d, i), nifrw.parse_shape_hdr(d.blocks[i][1])["nvert"]
    return None, 0


def strip_physics_tag(src, dst):
    """copy src -> dst without the 'HDT Skinned Mesh Physics Object' extra data on any root node"""
    d = nifrw.Doc(src)
    victims = set()
    for i, (t, b) in enumerate(d.blocks):
        if t == "NiStringExtraData":
            n, _s = struct.unpack_from("<II", b, 0)
            if d.strings[n] == hairgraft.PHYS:
                victims.add(i)
    if not victims:
        shutil.copyfile(src, dst)   # nothing to strip (companion pieces carry no tag)
        return
    for i, (t, b) in enumerate(d.blocks):
        if t in ("NiNode", "BSFadeNode"):
            n = nifrw.parse_node(b)
            if any(e in victims for e in n["extra"]):
                n["extra"] = [e for e in n["extra"] if e not in victims]
                d.blocks[i][1] = nifrw.build_node(n)
    g, _ = nifrw.rebuild(d)
    g.save(dst)


def main():
    staging = sys.argv[1]
    apply = "--apply" in sys.argv
    fids = grafted_fids()
    rows, places = [], {}   # places: static_key -> dict(src, strip, keep_case, users)
    for fid in fids:
        n = npcs.get(fid)
        if not n or n["hair_phys"]:
            continue   # bucket B: the model already is the SMP mesh the bake carries
        try:
            p, why = s13.plan(fid)
        except Exception as ex:
            p, why = None, "plan error: %s" % str(ex)[:80]
        if not p:
            rows.append(dict(fid=fid, name=n["name"], hair=n["hair_eid"], status="PLAN-FAIL", note=why))
            continue
        main_fid = n["hair"]
        has_vh = any(r["name"] == "VirtualHead" for r in p["reps"])
        bake = os.path.join(GRAFT_FG, n["plugin"], "00%s.nif" % fid.split(":")[0])
        # (static model key, twin source on disk, bake shape name, original-case model path)
        wants = [(s13.norm(hdpt[main_fid]["model"]), p["src"], p["reps"][0]["name"], hdpt[main_fid]["model"])]
        for r in p["reps"][1:]:
            if r["name"] == "VirtualHead":
                continue
            e = next((e for e in s13.part_tree(main_fid)[1:] if hdpt[e]["eid"] == r["name"]), None)
            if e is None or not hdpt[e]["model"]:
                continue
            wants.append((s13.norm(hdpt[e]["model"]), r["hair"], r["name"], hdpt[e]["model"]))
        for skey, src, shape, mpath in wants:
            srckey = s13.norm(os.path.relpath(src, os.path.dirname(os.path.dirname(src))))  # not used for identity
            winner_path, winner = s13.disk_path(skey)
            tb, tn = first_shape_bones(src)
            bb, bn = bake_shape_bones(bake, shape)
            wb = first_shape_bones(winner_path)[0] if winner_path else None
            same_file = winner_path and os.path.normcase(os.path.abspath(winner_path)) == os.path.normcase(os.path.abspath(src))
            status = "ok"
            note = ""
            if bb is None:
                status, note = "BAKE-SHAPE-MISSING", "grafted bake has no shape %s" % shape
            elif bb != tb:
                status, note = "BONES-DIFFER", "bake %s vs twin %s" % (bb, tb)
            elif same_file:
                status, note = "already-twin", "model path already resolves to the twin"
            elif not winner_path:
                status, note = "model-absent", "no file at the model path; engine loads no model (clone path, safe)"
            elif wb == tb:
                status, note = "winner-bones-match", "winner %s already has the twin's bones" % winner
            rows.append(dict(fid=fid, name=n["name"], hair=shape, status=status, note=note, static=mpath,
                             winner=winner or "", twin=os.path.relpath(src, os.path.join(inst, "mods")),
                             twin_nvert=tn, bake_nvert=bn, bones=len(tb or []), winner_bones=len(wb or []) if wb else 0,
                             strip=has_vh))
            if status == "ok":
                pl = places.setdefault(skey, dict(src=src, strip=has_vh, path=mpath, users=[], twin_bones=tb))
                pl["users"].append(n["name"])
                if pl["src"] != src or pl["strip"] != has_vh:
                    pl.setdefault("conflict", []).append((n["name"], src, has_vh))
    # ---- stage
    out_root = os.path.join(staging, MODNAME)
    staged = []
    for skey, pl in sorted(places.items()):
        if pl.get("conflict"):
            print("CONFLICT at", skey, pl["conflict"]); continue
        rel = pl["path"].replace("/", "\\")
        rel = rel if rel.lower().startswith("meshes\\") else "meshes\\" + rel
        dst = os.path.join(out_root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if pl["strip"]:
            strip_physics_tag(pl["src"], dst)
        else:
            shutil.copyfile(pl["src"], dst)
        # verify the staged file
        sb, _ = first_shape_bones(dst)
        phys = nifhdr.file_physics(dst)[0]
        src_phys = nifhdr.file_physics(pl["src"])[0]
        ok = sb == pl["twin_bones"] and (phys == (bool(src_phys) and not pl["strip"]))
        staged.append((rel, os.path.relpath(pl["src"], os.path.join(inst, "mods")), pl["strip"], phys, ok, pl["users"]))
        print("%s %-70s <- %-50s strip=%s phys=%s users=%s" % ("OK  " if ok else "BAD ", rel, os.path.relpath(pl["src"], os.path.join(inst, "mods")), pl["strip"], phys, ", ".join(pl["users"])))
    # ---- report
    os.makedirs(staging, exist_ok=True)
    with open(os.path.join(staging, "model_twins_report.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["fid", "name", "hair", "status", "note", "static", "winner", "twin", "twin_nvert", "bake_nvert", "bones", "winner_bones", "strip"])
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in w.fieldnames})
    json.dump(staged, open(os.path.join(staging, "model_twins_staged.json"), "w"), indent=1)
    c = collections.Counter(r["status"] for r in rows)
    print("rows", dict(c), "| staged files", len(staged), "| all verified", all(s[4] for s in staged))
    # ---- apply
    if apply:
        tl = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
        if "modorganizer.exe" in tl or "skyrimse.exe" in tl:
            print("REFUSED: Mod Organizer or the game is running; close them and rerun with --apply"); return 2
        n = 0
        for rel, *_ in staged:
            src = os.path.join(out_root, rel); dst = os.path.join(inst, "mods", MODNAME, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst); n += 1
        print("APPLIED %d files into mods\\%s" % (n, MODNAME))
    return 0


if __name__ == "__main__":
    sys.exit(main())
