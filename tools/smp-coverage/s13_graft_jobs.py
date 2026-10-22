"""Build graft jobs for NPCs whose static hair has an SMP twin, run them into a staging mod folder.
usage: python -I s13_graft_jobs.py <staging_root> <fid> [<fid> ...]   or   --bucket B|C [--limit N]
"""
import os, sys, json, re, struct, shutil, collections
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
tools = r"C:\1. AUTHORIA\_tools\smp-coverage"
sys.path.insert(0, sp); sys.path.insert(0, tools)
import nifhdr, bsareader, hairgraft, hairgeo
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
import nifrw
inst = r"C:\1. AUTHORIA"
MODNAME = "Authoria - SMP Hair Grafts"
# style guard thresholds (bake-in-twin, twin-in-bake); --relax X lowers both to X for named, same-style picks
RELAX = (0.95, 0.90)
if "--relax" in sys.argv:
    _v = float(sys.argv[sys.argv.index("--relax") + 1]); RELAX = (_v, _v)
    del sys.argv[sys.argv.index("--relax"):sys.argv.index("--relax") + 2]

npcs = {n["fid"]: n for n in json.load(open(sp + r"\npc_hair.json"))}
hdpt = json.load(open(sp + r"\hdpt.json"))
hcls = json.load(open(sp + r"\hair_class.json"))
fg = json.load(open(sp + r"\facegen_phys.json"))
vfs = json.load(open(sp + r"\loose_vfs.json"))
bsa_vfs = json.load(open(sp + r"\bsa_vfs_meshes.json"))
tmp = os.path.join(sp, "graft_tmp"); os.makedirs(tmp, exist_ok=True)
_bsa_cache = {}


def norm(p):
    p = p.lower().replace("/", "\\")
    return p if p.startswith("meshes\\") else "meshes\\" + p


def disk_path(key):
    """Data-relative lowercase mesh key -> a readable file on disk (loose winner, or extracted from the BSA winner)."""
    if key in vfs:
        return vfs[key][1], vfs[key][0]
    if key in bsa_vfs:
        bp, bn = bsa_vfs[key]
        b = _bsa_cache.get(bp)
        if b is None:
            b = _bsa_cache[bp] = bsareader.BSA(bp)
        out = os.path.join(tmp, "bsa", re.sub(r"[^a-z0-9_.]", "_", key))
        if not os.path.exists(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "wb").write(b.read(key))
        return out, bn
    return None, None


def bake_path(n):
    k = n["fg"]
    f = fg.get(k) if k else None
    if not f or not f.get("winner"):
        return None, None
    if f["kind"] == "loose":
        root = os.path.join(inst, "overwrite") if f["winner"].lower() == "overwrite" else os.path.join(inst, "mods", f["winner"])
        return os.path.join(root, k), f["winner"]
    # BSA facegen
    bname = f["winner"]
    cands = []
    for m in [l.rstrip("\r\n")[1:] for l in open(sp + r"\modlist.txt", encoding="utf-8") if l.startswith("+")]:
        p = os.path.join(inst, "mods", m, bname)
        if os.path.isfile(p):
            cands.append(p)
    p = os.path.join(inst, "Stock Game", "Data", bname)
    if os.path.isfile(p):
        cands.append(p)
    if not cands:
        return None, None
    b = _bsa_cache.get(cands[0])
    if b is None:
        b = _bsa_cache[cands[0]] = bsareader.BSA(cands[0])
    out = os.path.join(tmp, "bake", re.sub(r"[^a-z0-9_.]", "_", k))
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "wb").write(b.read(k))
    return out, bname


# ---- SMP twin lookup for a static mesh
smp_by_stem = collections.defaultdict(list)
for k, v in hcls.items():
    if v.get("phys") and "\\wig\\" not in k:
        s = re.sub(r"[^a-z0-9]", "", os.path.splitext(os.path.basename(k))[0])
        for suf in ("smp", "hdt"):
            if s.endswith(suf):
                s = s[:-len(suf)]
        smp_by_stem[s].append(k)
GENERIC = re.compile(r"^(hair|hairline|hl|scalp|female|male)?\d*$")


def twin_for(model_key, nvert=None):
    """returns the Data-relative key of an installed SMP mesh of the same style, or None"""
    base = os.path.basename(model_key)
    stem = re.sub(r"[^a-z0-9]", "", os.path.splitext(base)[0])
    if GENERIC.match(stem) or len(stem) < 4:
        return None
    elves = "elves" in model_key or "\\elf" in model_key
    cands = []
    ks = "meshes\\ks hairdo's\\hdt\\" + ("elves\\" if elves else "") + base
    if ks in hcls and hcls[ks].get("phys"):
        cands.append(ks)
    for c in smp_by_stem.get(stem, []):
        if c not in cands:
            cands.append(c)
    if not cands:
        return None
    # prefer the race variant that matches the path, then the exact vertex count
    def score(c):
        s = 0
        if ("elves" in c) == elves: s += 2
        if "ks hairdo's\\hdt" in c: s += 1
        if nvert is not None:
            try:
                d = nifrw.Doc(disk_path(c)[0])
                nv = max(nifrw.parse_shape_hdr(d.blocks[i][1])["nvert"] for i in hairgraft.shapes(d))
                if nv == nvert: s += 4
            except Exception:
                pass
        return -s
    cands.sort(key=score)
    return cands[0]


_mods_hi_first = [l.rstrip("\r\n")[1:] for l in open(sp + r"\modlist.txt", encoding="utf-8") if l.startswith("+")]
_static_cache = {}


def mesh_nverts(path):
    try:
        d = nifrw.Doc(path)
        return set(nifrw.parse_shape_hdr(d.blocks[i][1])["nvert"] for i in hairgraft.shapes(d))
    except Exception:
        return set()


def static_nverts(model_key):
    """vertex counts of every STATIC copy of this mesh path the instance holds (loose providers + the BSA copy)."""
    if model_key in _static_cache:
        return _static_cache[model_key]
    out = set()
    for m in _mods_hi_first:
        p = os.path.join(inst, "mods", m, model_key)
        if os.path.isfile(p):
            try:
                if not nifhdr.file_physics(p)[0]:
                    out |= mesh_nverts(p)
            except Exception:
                pass
    if model_key in bsa_vfs:
        bp, bn = bsa_vfs[model_key]
        b = _bsa_cache.get(bp)
        if b is None:
            b = _bsa_cache[bp] = bsareader.BSA(bp)
        try:
            data = b.read(model_key)
            if not nifhdr.physics_info(data)[0]:
                tmpf = os.path.join(tmp, "static", re.sub(r"[^a-z0-9_.]", "_", model_key))
                os.makedirs(os.path.dirname(tmpf), exist_ok=True)
                open(tmpf, "wb").write(data)
                out |= mesh_nverts(tmpf)
        except Exception:
            pass
    _static_cache[model_key] = out
    return out


def part_tree(fid, seen=None):
    seen = seen or set()
    if fid in seen or fid not in hdpt:
        return []
    seen.add(fid)
    out = [fid]
    for e in hdpt[fid]["extras"]:
        out.extend(part_tree(e, seen))
    return out


def physics_skinned(H):
    """True when any shape of the nif is skinned to a non-standard (physics) bone."""
    for si in hairgraft.shapes(H):
        sh, deps = hairgraft.shape_deps(H, si)
        if any(not str(hairgraft.node_name(H, b)).startswith("NPC ") for b in deps.get("bones", [])):
            return True
    return False


def xml_shape_refs(xml_path):
    txt = open(xml_path, encoding="utf-8", errors="replace").read()
    return txt, sorted(set(re.findall(r'(?:per-vertex-shape|per-triangle-shape)\s+name="([^"]+)"', txt)))


def plan(fid):
    n = npcs[fid]
    plugin, local = n["plugin"], fid.split(":")[0]
    bake, bake_from = bake_path(n)
    if not bake:
        return None, "no face bake"
    F = nifrw.Doc(bake)
    if F.stream != 100:
        return None, "bake is not an SE nif"
    fsh = {}
    for i in hairgraft.shapes(F):
        fsh[F.name_of(i)] = nifrw.parse_shape_hdr(F.blocks[i][1])["nvert"]
    main = n["hair"]
    meid = hdpt[main]["eid"]
    if meid not in fsh:
        return None, "bake lacks the hair shape %s (has %s)" % (meid, sorted(fsh))
    mmodel = hdpt[main]["model"]
    if not mmodel:
        return None, "hair part has no model"
    if fsh[meid] == 0:
        return None, "bake's hair shape %s is empty (no hair by design)" % meid
    mkey = norm(mmodel)
    mc = hcls.get(mkey, {})
    if mc.get("phys"):
        src_key = mkey
    else:
        src_key = twin_for(mkey, fsh[meid])
        if not src_key:
            return None, "no SMP twin for %s" % os.path.basename(mkey)
    src, src_from = disk_path(src_key)
    if not src:
        return None, "twin mesh not readable: " + src_key
    # the bake must hold THIS style: exact static geometry, or the same silhouette as the SMP twin
    sv = static_nverts(mkey)
    style = "exact static copy"
    if fsh[meid] not in sv:
        try:
            fi = [i for i in hairgraft.shapes(F) if F.name_of(i) == meid][0]
            pa = hairgeo.head_space(hairgeo.positions(F, fi), F)
            Ht = nifrw.Doc(src)
            hi = max(hairgraft.shapes(Ht), key=lambda i: nifrw.parse_shape_hdr(Ht.blocks[i][1])["nvert"])
            pb = hairgeo.head_space(hairgeo.positions(Ht, hi), Ht)
        except Exception as ex:
            return None, "cannot read hair geometry to confirm the style (%s)" % str(ex)[:60]
        if not pa or not pb:
            return None, "bake hair geometry (%d verts) is not the static %s and cannot be compared" % (fsh[meid], os.path.basename(mkey))
        iou, ca, cb, ba, bb = hairgeo.similarity(pa, pb, 1.0)
        if ca < RELAX[0] or cb < RELAX[1]:
            return None, "bake hair is a different style than %s (overlap %.2f/%.2f, bake z %d..%d vs twin %d..%d)" % (
                os.path.basename(mkey), ca, cb, ba[0][2], ba[1][2], bb[0][2], bb[1][2])
        style = "same silhouette %.2f/%.2f" % (ca, cb)
    reps = [dict(name=meid, hair=src, keep_bake_alpha=False)]
    folder = os.path.dirname(src_key)
    for e in part_tree(main)[1:]:
        h = hdpt[e]
        if not h["model"] or h["eid"] not in fsh:
            continue
        ek = norm(h["model"])
        if ek == mkey and fsh[h["eid"]] == fsh[meid] and fsh[meid] > 0:
            reps.append(dict(name=h["eid"], hide=True))  # duplicate hair copy: hide, never a 2nd physics copy
            continue
        if src_key != mkey:
            # a static pack's companion piece (hairline etc.): take the SMP pack's same-named companion if it has one
            cand = folder + "\\" + os.path.basename(ek)
            if cand != src_key and cand in hcls and fsh[h["eid"]] > 0:
                cp, cf = disk_path(cand)
                if cp:
                    H2 = nifrw.Doc(cp)
                    if hairgraft.shapes(H2):
                        if physics_skinned(H2):
                            reps.append(dict(name=h["eid"], hide=True))  # KS HL = full physics duplicate: hide
                        else:
                            reps.append(dict(name=h["eid"], hair=cp, keep_bake_alpha=True, companion=True))
    # physics xml: KS-style xmls name the shapes; write a per-NPC copy with the bake's shape names
    H = nifrw.Doc(src)
    xml_rel = hairgraft.hair_physics_xml(H)
    xml_disk = None
    xml_key = norm(re.sub(r"^data\\", "", xml_rel.lower().replace("/", "\\")))
    if xml_key in vfs:
        xml_disk = vfs[xml_key][1]
    override = None
    if xml_disk:
        txt, refs = xml_shape_refs(xml_disk)
        rename = {}
        for r in reps:
            if r.get("hide"):
                continue
            Hr = nifrw.Doc(r["hair"])
            for k, i in enumerate(hairgraft.shapes(Hr)):
                rename[Hr.name_of(i)] = r["name"] if k == 0 else "%s_%d" % (r["name"], k)
        # the pack's collision helper, if the xml wants it and the pack ships it
        vh = folder + "\\virtualhead.nif"
        if "VirtualHead" in refs and vh in hcls and src_key != mkey:
            vp, vf = disk_path(vh)
            if vp:
                reps.append(dict(name="VirtualHead", hair=vp, replace=False))
        if any(r in rename for r in refs):
            new_txt = txt
            # drop the pack's HL shape blocks whose bake shape is hidden (no physics copy carries them)
            hidden_src = [sn for sn in refs if sn.endswith("_HL")] if any(r.get("hide") for r in reps) else []
            for sn in hidden_src:
                new_txt = re.sub(r'\s*<per-vertex-shape name="%s">.*?</per-vertex-shape>' % re.escape(sn), "", new_txt, flags=re.S)
            for sn, nn in rename.items():
                new_txt = new_txt.replace('name="%s"' % sn, 'name="%s"' % nn)
            rel = "meshes\\actors\\character\\facegendata\\facegeom\\%s\\00%s.xml" % (plugin, local)
            override = (rel, new_txt)
    return dict(fid=fid, name=n["name"], bake=bake, bake_from=bake_from, src=src, src_key=src_key, src_from=src_from,
                reps=reps, xml=xml_rel, override=override, plugin=plugin, local=local, bucket=("B" if mc.get("phys") else "C"), style=style), None


def run(staging, fids, log=print, skip_existing=False):
    results = []
    for fid in fids:
        n = npcs[fid]
        pre = os.path.join(staging, MODNAME, "meshes", "actors", "character", "facegendata", "facegeom", n["plugin"], "00%s.nif" % fid.split(":")[0])
        if skip_existing and os.path.exists(pre):
            results.append((fid, "ok", {"replaced": [], "removed": [], "xml": [], "note": "already staged"})); continue
        try:
            p, why = plan(fid)
        except Exception as ex:
            p, why = None, "unreadable nif: %s" % str(ex)[:80]
        if not p:
            log("SKIP %s %s: %s" % (fid, npcs[fid]["name"], why)); results.append((fid, "skip", why)); continue
        out = pre
        xo = None
        if p["override"]:
            rel, txt = p["override"]
            xp = os.path.join(staging, MODNAME, rel)
            os.makedirs(os.path.dirname(xp), exist_ok=True)
            open(xp, "w", encoding="utf-8").write(txt)
            xo = {p["src"]: rel}
        try:
            rep = hairgraft.graft(p["bake"], out, p["reps"], xml_override=xo, log=lambda m: log("   " + m))
        except Exception as ex:
            log("FAIL %s %s: %s" % (fid, p["name"], ex)); results.append((fid, "fail", str(ex))); continue
        phys, xmls, bsver, h = nifhdr.file_physics(out if len(out) <= 240 else "\\\\?\\" + os.path.abspath(out))
        log("OK   %s %-24s bucket %s | %s | bake from %s | hair %s (%s) | shapes %s | removed %s | xml %s | phys %s" % (
            fid, p["name"], p["bucket"], p["style"], p["bake_from"], os.path.basename(p["src_key"]), p["src_from"],
            [r[0] for r in rep["replaced"]], rep["removed"], xmls, phys))
        results.append((fid, "ok", rep))
    return results


if __name__ == "__main__":
    staging = sys.argv[1]
    args = sys.argv[2:]
    if args and args[0] == "--bucket":
        want = args[1]
        limit = int(args[3]) if len(args) > 3 and args[2] == "--limit" else None
        fids = []
        for fid, n in npcs.items():
            if n["fg_phys"]:
                continue
            if want == "B" and n["hair_phys"] and n["fg"]:
                fids.append(fid)
            elif want == "C" and not n["hair_phys"] and n["equiv"]:
                fids.append(fid)
        if limit:
            fids = fids[:limit]
    elif args and args[0] == "--names":
        fids = []
        for nm in args[1:]:
            for fid, n in npcs.items():
                if n["name"] == nm and n["fg"] and not n["fg_phys"]:
                    fids.append(fid); break
    else:
        fids = args
    res = run(staging, fids, skip_existing="--skip-existing" in sys.argv)
    c = collections.Counter(r[1] for r in res)
    print("DONE", dict(c))
    json.dump([(r[0], r[1], r[2] if r[1] != "ok" else {"replaced": r[2]["replaced"], "removed": r[2]["removed"], "xml": r[2]["xml"]}) for r in res],
              open(os.path.join(staging, "graft_results.json"), "w"), indent=1)
