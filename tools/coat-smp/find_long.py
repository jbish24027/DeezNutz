"""Every vanilla men's body-slot clothing mesh (ARMA list from houseCARL), its winning file in a profile (loose by modlist
priority, else the game BSAs), and whether it hangs a skirt between the legs (cloth at x ~ 0 in front of / behind the
crotch at knee-to-thigh height) and already carries an HDT-SMP link. usage: find_long.py <arma jsonl> [profile]"""
import os, sys, json, tempfile
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\skill\scripts")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\smp-coverage")
import smpkit
C = smpkit.init()
from bsareader import BSA

ROOT = r"C:\1. AUTHORIA"
PROFILE = sys.argv[2] if len(sys.argv) > 2 else "DEEZ CS NUTZ - PICTA"
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")][1:]
paths = {}
for r in rows:
    f = {x["path"]: x for x in r["fields"]}
    slots = f.get("BodyTemplate.FirstPersonFlags", {}).get("slots") or []
    m = f.get("WorldModel.Male.File", {}).get("value")
    if m and 32 in slots:
        paths.setdefault(m.lower(), []).append(r["editorid"])
enabled = [l[1:] for l in open(os.path.join(ROOT, "profiles", PROFILE, "modlist.txt"), encoding="utf-8").read().splitlines() if l.startswith("+")]
mod_files = {}
for m in enabled:      # top = highest priority
    base = os.path.join(ROOT, "mods", m, "meshes")
    if not os.path.isdir(base):
        continue
    for dp, _, fs in os.walk(base):
        for fn in fs:
            rel = os.path.relpath(os.path.join(dp, fn), os.path.join(ROOT, "mods", m)).lower()
            mod_files.setdefault(rel, m)
bsas = []
data = os.path.join(ROOT, "Stock Game", "Data")
for n in sorted(os.listdir(data)):
    if n.lower().endswith(".bsa") and "mesh" in n.lower() or n.lower() in ("dawnguard.bsa", "dragonborn.bsa", "hearthfires.bsa"):
        try: bsas.append(BSA(os.path.join(data, n)))
        except Exception: pass
tmp = tempfile.mkdtemp()
out = []
for mp, eds in sorted(paths.items()):
    rel = "meshes\\" + mp
    src = None
    if rel in mod_files:
        src = os.path.join(ROOT, "mods", mod_files[rel], rel); who = mod_files[rel]
    else:
        for b in bsas:
            if rel in b.files:
                src = os.path.join(tmp, os.path.basename(rel)); open(src, "wb").write(b.read(rel)); who = os.path.basename(b.path); break
    if not src:
        out.append((mp, "MISSING", "", "", eds)); continue
    try:
        n, T = C.load(src); C.to_world(T)
    except Exception as e:
        out.append((mp, who, "unreadable", "", eds)); continue
    raw = open(src, "rb").read()
    hdt = b"HDT Skinned Mesh Physics Object" in raw
    best = None
    for t in T:
        p = t.pos
        band = (p[:, 2] > 35) & (p[:, 2] < 55) & (np.abs(p[:, 0]) < 2.5) & (np.abs(p[:, 1]) > 3)
        if band.sum() >= 3:
            lo = float(p[np.abs(p[:, 0]) < 4, 2].min())
            best = (t.name, lo) if best is None or lo < best[1] else best
    out.append((mp, who, ("HDT " if hdt else "") + ("SKIRT %s hem %.0f" % best if best else "no skirt"), "", eds))
for mp, who, what, _, eds in out:
    print(f"{what:40s} | {mp} | {who} | {', '.join(eds[:3])}")
if len(sys.argv) > 3:      # json of the candidates (no HDT, a skirt) with their source file; BSA ones extracted under argv[3]
    cand = []
    for mp, who, what, _, eds in out:
        if not what.startswith("SKIRT"): continue
        rel = "meshes\\" + mp
        if who.lower().endswith(".bsa"):
            b = next(b for b in bsas if os.path.basename(b.path) == who)
            for v in ("_0", "_1"):
                r2 = rel[:-6] + v + ".nif" if rel.endswith(("_0.nif", "_1.nif")) else rel
                if r2 in b.files:
                    d = os.path.join(sys.argv[3], r2); os.makedirs(os.path.dirname(d), exist_ok=True); open(d, "wb").write(b.read(r2))
            src = os.path.join(sys.argv[3], rel)
        else:
            src = os.path.join(ROOT, "mods", who, rel)
        cand.append(dict(path=mp, mod=who, src=src.replace("\\", "/"), eds=eds, what=what))
    json.dump(cand, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidates_" + os.path.basename(sys.argv[1]).split(".")[0] + ".json"), "w"), indent=1)
