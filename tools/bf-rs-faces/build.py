"""Build the Beeing Female RS Children baby face pool (2026-10-21).

Each unused child face (a losing appearance whose own FaceGen still ships in its
mod) becomes a new BF player-child baby model: the BF RS template body for that
race/sex, with the face record fields and FaceGen files from the losing mod.
Input: unused_faces.json (from find_losers.py). Output: the mod folder below.
"""
import json, os, shutil, struct, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\requiem-clothing-patch")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
import esp_tools as et
import nifrw

HERE = os.path.dirname(os.path.abspath(__file__))
MODS = r"C:\1. AUTHORIA\mods"
OUT_MOD = os.path.join(MODS, "Authoria - BF RS Children Faces")
PLUGIN = "AuthoriaBFRSFaces.esp"
RS = os.path.join(MODS, "Beeing Female NG", "BeeingFemale_RS_PatchSE_ESPFE.esp")

# BF player-child templates (from BFASE_RSChildren_SE_Opt.ini), as (master, id)
TEMPLATES = {
    ("Nord", "girl"): ("BeeingFemale.esm", 0x02AB17), ("Nord", "boy"): ("BeeingFemale.esm", 0x02AB16),
    ("Imperial", "girl"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x864), ("Imperial", "boy"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x865),
    ("Redguard", "girl"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x868), ("Redguard", "boy"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x869),
    ("Breton", "girl"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x859), ("Breton", "boy"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x858),
    ("Orc", "girl"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x8B0), ("Orc", "boy"): ("BeeingFemale_RS_PatchSE_ESPFE.esp", 0x8B2),
}
RACE_ALIAS = {"00086E:KiNRefined.esp": "Imperial", "00086F:KiNRefined.esp": "Redguard", "000870:KiNRefined.esp": "Nord",
              "000871:KiNRefined.esp": "Breton", "000872:KiNRefined.esp": "Breton", "Breton(vamp)": "Breton"}
APPEAR_HEAD = (b"PNAM", b"HCLF")                       # sit mid-record
APPEAR_TAIL = (b"FTST", b"QNAM", b"NAM9", b"NAMA", b"TINI", b"TINC", b"TINV", b"TIAS")
FORMID_SUBS = (b"PNAM", b"HCLF", b"FTST")


def find_ci(base, *parts):
    """Case-insensitive path walk; returns the real path or None."""
    cur = base
    for p in parts:
        if not os.path.isdir(cur):
            return None
        hit = [e for e in os.listdir(cur) if e.lower() == p.lower()]
        if not hit:
            return None
        cur = os.path.join(cur, hit[0])
    return cur


def raw_fid(pl, master, fid):
    names = [m.lower() for m in pl.masters]
    idx = names.index(master.lower()) if master.lower() in names else len(names)
    return (idx << 24) | fid


def get_rec(pl, raw):
    for r in pl.records:
        if r.formid == raw:
            return r
    return None


def main():
    faces = json.load(open(os.path.join(HERE, "unused_faces.json")))
    rs = et.Plugin(RS)
    masters = list(rs.masters) + [rs.name]           # template bodies resolve unchanged
    def midx(name):
        low = [m.lower() for m in masters]
        if name.lower() not in low:
            masters.append(name)
            low.append(name.lower())
        return low.index(name.lower())

    if os.path.exists(OUT_MOD):
        sys.exit("output mod already exists - remove it first: " + OUT_MOD)
    records, pool, report, nextid = [], {}, [], 0x800
    loaded = {}
    for f in faces:
        race = RACE_ALIAS.get(f["race"], f["race"])
        key = (race, f["sex"])
        if key not in TEMPLATES:
            report.append(f"SKIP no template {key}: {f['editorid']}"); continue
        fid_hex, master = f["formid"].split(":", 1)
        fid = int(fid_hex, 16)
        lp_path = find_ci(MODS, f["loser_mod"], f["loser"])
        if lp_path not in loaded:
            loaded[lp_path] = et.Plugin(lp_path)
        lp = loaded[lp_path]
        src = get_rec(lp, raw_fid(lp, master, fid))
        tmpl = get_rec(rs, raw_fid(rs, *TEMPLATES[key]))
        nif = find_ci(MODS, f["loser_mod"], "meshes", "actors", "character", "facegendata", "facegeom", master, f"00{fid_hex}.nif")
        dds = find_ci(MODS, f["loser_mod"], "textures", "actors", "character", "facegendata", "facetint", master, f"00{fid_hex}.dds")
        if not (src and tmpl and nif and dds):
            report.append(f"SKIP missing piece ({'rec' if not src else ''}{'tmpl' if not tmpl else ''}{'nif' if not nif else ''}{'dds' if not dds else ''}): {f['editorid']} in {f['loser_mod']}")
            continue

        def remap(d):
            raw = struct.unpack("<I", d[:4])[0]
            i, low = raw >> 24, raw & 0xFFFFFF
            owner = lp.masters[i] if i < len(lp.masters) else lp.name
            return struct.pack("<I", (midx(owner) << 24) | low) + d[4:]

        try:
            doc = nifrw.Doc(nif)
        except AssertionError as e:
            report.append(f"SKIP unreadable FaceGen mesh ({e}): {f['editorid']} in {f['loser_mod']}")
            continue
        head = [(s, remap(d) if s in FORMID_SUBS else d) for s, d in src.subs if s in APPEAR_HEAD]
        tail = [(s, remap(d) if s in FORMID_SUBS else d) for s, d in src.subs if s in APPEAR_TAIL]
        weight = src.sub(b"NAM7")
        new_edid = f"AuthBF_{race}{'Girl' if f['sex'] == 'girl' else 'Boy'}_{f['editorid']}"
        subs, placed_head = [], False
        for s, d in tmpl.subs:
            if s == b"EDID":
                subs.append((s, new_edid.encode("cp1252") + b"\x00")); continue
            if s in APPEAR_HEAD or s in APPEAR_TAIL:
                if s in APPEAR_HEAD and not placed_head:
                    subs += head; placed_head = True
                continue
            if s in (b"ZNAM", b"GNAM", b"NAM5") and not placed_head:
                subs += head; placed_head = True
            if s == b"NAM7" and weight is not None:
                d = weight
            subs.append((s, d))
        if not placed_head:
            subs += head
        subs += tail
        body = et.build_subrecords(subs)
        myid = nextid; nextid += 1
        records.append((b"NPC_", tmpl.flags & ~et.COMPRESSED, myid, tmpl.tail, body))
        pool.setdefault(key, []).append(myid)

        # FaceGen: copy, then repoint the tint path inside the head mesh
        new_hex = f"{myid:06X}"
        gdir = os.path.join(OUT_MOD, "meshes", "actors", "character", "FaceGenData", "FaceGeom", PLUGIN)
        tdir = os.path.join(OUT_MOD, "textures", "actors", "character", "FaceGenData", "FaceTint", PLUGIN)
        os.makedirs(gdir, exist_ok=True); os.makedirs(tdir, exist_ok=True)
        shutil.copy2(dds, os.path.join(tdir, f"00{new_hex}.dds"))
        hits = 0
        for blk in doc.blocks:
            if blk[0] != "BSShaderTextureSet":
                continue
            b = blk[1]; n = struct.unpack_from("<I", b, 0)[0]; o = 4; strs = []
            for _ in range(n):
                ln = struct.unpack_from("<I", b, o)[0]; strs.append(b[o + 4:o + 4 + ln].decode("cp1252")); o += 4 + ln
            changed = False
            for i, s in enumerate(strs):
                if "facetint" in s.lower():
                    pre = s[: s.lower().index("facetint")]
                    strs[i] = pre + f"FaceTint\\{PLUGIN}\\00{new_hex}.dds"; changed = True; hits += 1
            if changed:
                nb = bytearray(struct.pack("<I", n))
                for s in strs:
                    e = s.encode("cp1252"); nb += struct.pack("<I", len(e)) + e
                nb += b[o:]
                blk[1] = nb
        doc.save(os.path.join(gdir, f"00{new_hex}.nif"))
        report.append(f"OK {new_edid} -> {PLUGIN}:{myid:X}  tint paths repointed: {hits}  (face from {f['loser_mod']})")

    os.makedirs(OUT_MOD, exist_ok=True)
    own = len(masters) << 24                      # new records belong to this plugin, not a master
    records = [(s, fl, own | fid, t, b) for s, fl, fid, t, b in records]
    et.write_patch(os.path.join(OUT_MOD, PLUGIN), masters, records,
                   description="Beeing Female baby face pool from unused RS Children faces (Authoria 2026-10-21)",
                   esl=True, nextid=nextid)
    json.dump({f"{k[0]}|{k[1]}": v for k, v in pool.items()}, open(os.path.join(HERE, "pool.json"), "w"), indent=1)
    open(os.path.join(HERE, "build_report.txt"), "w", encoding="utf-8").write("\n".join(report))
    print("masters:", masters)
    print("built", len(records), "baby models;", sum(1 for r in report if r.startswith("SKIP")), "skipped")
    for k, v in sorted(pool.items()): print(" ", k, len(v))


if __name__ == "__main__":
    main()
