"""Compute which provider wins each candidate asset path in a given MO2 profile.
Loose: highest-priority enabled mod (modlist.txt top = highest), overwrite above all.
BSA: archives attached to active plugins (basename match) in plugin load order + Skyrim.ini archive list; later wins.
Loose beats BSA.  Read-only.
"""
import os, sys, json, struct, hashlib

INST = "C:/1. AUTHORIA"
MODS = INST + "/mods"
DATA = INST + "/Stock Game/Data"
HERE = os.path.dirname(os.path.abspath(__file__))

def read_modlist(profile):
    lines = open(f"{INST}/profiles/{profile}/modlist.txt", encoding="utf-8").read().splitlines()
    out = []
    for l in lines:
        if not l or l.startswith("#"): continue
        flag, name = l[0], l[1:]
        if name.endswith("_separator"): continue
        out.append((flag == "+", name))
    return out  # top = highest priority

def read_plugins(profile):
    lines = open(f"{INST}/profiles/{profile}/plugins.txt", encoding="utf-8", errors="replace").read().splitlines()
    act = []
    for l in lines:
        if not l or l.startswith("#"): continue
        if l.startswith("*"): act.append(l[1:])
    return act

def bsa_names(path):
    try:
        with open(path, "rb") as f:
            hdr = f.read(36)
            if hdr[:4] != b"BSA\x00": return []
            ver, off, aflags, nfold, nfile, lfold, lfile, fflags = struct.unpack("<IIIIIIII", hdr[4:36])
            f.seek(off)
            recsz = 24 if ver == 105 else 16
            folders = []
            for i in range(nfold):
                rec = f.read(recsz)
                cnt = struct.unpack("<I", rec[8:12])[0]
                folders.append(cnt)
            fnames_dirs = []
            for cnt in folders:
                if aflags & 1:
                    ln = f.read(1)[0]
                    d = f.read(ln).rstrip(b"\x00").decode("cp1252", "replace")
                else:
                    d = ""
                f.seek(16 * cnt, 1)
                fnames_dirs.append((d, cnt))
            names = []
            if aflags & 2:
                blob = f.read(lfile).split(b"\x00")
                idx = 0
                for d, cnt in fnames_dirs:
                    for j in range(cnt):
                        names.append((d + "\\" + blob[idx].decode("cp1252", "replace")).replace("\\", "/").lower())
                        idx += 1
            return names
    except Exception as e:
        print("BSA ERR", path, e)
        return []

def main(profile, cand_paths, tag):
    cand = sorted(set(p.lower().replace("\\", "/") for p in cand_paths))
    cdirs = sorted(set(os.path.dirname(p) for p in cand))
    ml = read_modlist(profile)
    enabled = [n for e, n in ml if e]
    providers = {p: [] for p in cand}   # loose providers in priority order (highest first)
    # overwrite
    roots = [("overwrite", INST + "/overwrite")] + [(n, MODS + "/" + n) for n in enabled]
    for name, root in roots:
        if not os.path.isdir(root): continue
        # case-insensitive dir resolution
        for d in cdirs:
            # walk down resolving case
            cur = root
            ok = True
            for seg in d.split("/"):
                try:
                    ents = {e.lower(): e for e in os.listdir(cur)}
                except Exception:
                    ok = False; break
                if seg in ents:
                    cur = cur + "/" + ents[seg]
                else:
                    ok = False; break
            if not ok: continue
            try:
                files = {e.lower() for e in os.listdir(cur)}
            except Exception:
                continue
            for p in cand:
                if os.path.dirname(p) == d and os.path.basename(p) in files:
                    providers[p].append(name)
    # game Data loose
    for p in cand:
        if os.path.exists(DATA + "/" + p):
            providers[p].append("Data(loose)")
    # BSAs: map active plugin order
    act = read_plugins(profile)
    # implicit masters first
    implicit = ["Skyrim.esm", "Update.esm", "Dawnguard.esm", "HearthFires.esm", "Dragonborn.esm"]
    order = implicit + [a for a in act if a not in implicit]
    base = {os.path.splitext(a)[0].lower(): i for i, a in enumerate(order)}
    # find BSAs: in enabled mods + Data
    bsa_files = []
    for n in enabled:
        root = MODS + "/" + n
        try:
            for e in os.listdir(root):
                if e.lower().endswith(".bsa"):
                    bsa_files.append((n, root + "/" + e, e))
        except Exception:
            pass
    for e in os.listdir(DATA):
        if e.lower().endswith(".bsa"):
            bsa_files.append(("Data", DATA + "/" + e, e))
    # winning BSA file per name: mod priority decides which copy of the same bsa filename
    seen = {}
    for n, full, e in bsa_files:
        if e.lower() not in seen:
            seen[e.lower()] = (n, full, e)
    bsa_prov = {p: [] for p in cand}
    for el, (n, full, e) in seen.items():
        stem = os.path.splitext(e)[0].lower()
        key = None
        if stem in base: key = base[stem]
        elif " - " in stem and stem.rsplit(" - ", 1)[0] in base: key = base[stem.rsplit(" - ", 1)[0]]
        elif stem.startswith("skyrim - "): key = -1
        if key is None: continue
        names = set(bsa_names(full))
        for p in cand:
            if p in names:
                bsa_prov[p].append((key, e, n))
    res = {}
    for p in cand:
        bl = sorted(bsa_prov[p], key=lambda x: -x[0])
        res[p] = {
            "loose": providers[p],
            "bsa": [f"{e} [{n}] (lo#{k})" for k, e, n in bl],
            "winner": providers[p][0] if providers[p] else (f"BSA:{bl[0][1]}" if bl else "ABSENT"),
        }
    json.dump(res, open(f"{HERE}/winners_{tag}.json", "w"), indent=1)
    return res

if __name__ == "__main__":
    inv = json.load(open(HERE + "/inventory.json"))
    srcs = ["[NoDelete] Astralite Weathers", "[NoDelete] Soul Core Plugin and Assets", "[NoDelete] Mists of Tamriel",
            "No More Blinding Fog", "[NoDelete] Astralite Weathers - 4K Clouds"]
    cand = []
    for s in srcs:
        for f in inv[s]:
            r = f["rel"].lower()
            if r.startswith(("meshes/", "textures/")):
                cand.append(r)
    # extra: picta camera fog + vanilla-ish fog meshes
    for f in inv["[NoDelete] Picta - Assets 4K"]:
        r = f["rel"].lower()
        if r.startswith("meshes/effects/fxcameraattach") or "fog" in r or "mist" in r or r.startswith("textures/volmist"):
            cand.append(r)
    for prof, tag in [("DEEZ CS NUTZ - PICTA", "picta"), ("DEEZ CS NUTZ - PBR", "pbr")]:
        r = main(prof, cand, tag)
        print("=====", prof, len(r))
        for p, v in sorted(r.items()):
            print(f"  {p}\n     WIN={v['winner']}  loose={v['loose'][:6]}  bsa={v['bsa'][:3]}")
