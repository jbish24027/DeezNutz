"""Analyse the simulated baby VFS for checks (a), (b), (c). Read-only."""
import collections, configparser, hashlib, json, os, re, sys

INST = r"C:\1. AUTHORIA"
HERE = os.path.dirname(os.path.abspath(__file__))
LP = "\\\\?\\"
FORK = "Authoria - Picta x Astralite - E11"
DARK = "Authoria - Picta 1.1.2 - Darkened to 1.0.1"
BTWIN = "Authoria - Picta x Astralite - Root twin"
PTWIN = "Authoria - Picta ENB - Root twin"
MIST = "Authoria - Picta x Astralite - Mist assets"
CSL = "Authoria - CS Light - Interior Windows"

v = json.load(open(os.path.join(HERE, "baby_vfs.json"), encoding="utf-8"))
vp = json.load(open(os.path.join(HERE, "picta_vfs.json"), encoding="utf-8"))
order = v["order"]
pos = {m: i for i, m in enumerate(order)}


def md5(p):
    return hashlib.md5(open(LP + p, "rb").read()).hexdigest()


def winner(tbl, k):
    lst = sorted(tbl.get(k, []))
    return lst[0][1] if lst else None


def report(title):
    print("\n=== " + title)


# ---------- (a)
report("(a) Data enbseries winners in BABY")
enb = {k: e for k, e in v["data"].items() if k.startswith("enbseries\\") or k in (
    "enbseries.ini", "picta - weathers of aurbis.ini")}
cnt = collections.Counter()
by_w = collections.defaultdict(list)
for k in sorted(enb):
    w = winner(v["data"], k)
    cnt[w] += 1
    by_w[w].append(k)
for w, n in cnt.most_common():
    print(f"  {n:4d}  {w}")
non_fork_ini = [(k, winner(v["data"], k)) for k in sorted(enb) if k.endswith(".ini") and winner(v["data"], k) != FORK]
print("  .ini paths NOT won by fork:", non_fork_ini)
print("  paths won by Darkened E11 mod:", by_w.get(DARK, []))
for w in by_w:
    if w != FORK:
        print(f"  -- {w}: {by_w[w]}")
# all top-level data ini named enb* or Picta
for k in sorted(v["data"]):
    if "\\" not in k and (k.startswith("enb") or "picta" in k or "weathers of aurbis" in k):
        print("  top-level", k, "->", winner(v["data"], k), [e[1] for e in sorted(v["data"][k])])
specific = ["enbseries.ini", "picta - weathers of aurbis.ini", "enbseries\\enbeffectpostpass.fx.ini",
            "enbseries\\enblens.fx.ini", "enbseries\\enbdepthoffield.fx.ini", "enbseries\\enbpresetoverlays.ini",
            "enbseries\\enbeffect.fx.ini", "enbseries\\enbbloom.fx.ini", "enbseries\\enbadaptation.fx.ini",
            "enbseries\\_weatherlist.ini", "enbseries\\_locationweather.ini", "enbseries\\_worldspaceweatherlist.ini"]
for k in specific:
    print(f"  {k:45s} -> {winner(v['data'], k)}   stack={[e[1] for e in sorted(v['data'].get(k, []))]}")
# read-only providers
for k in sorted(enb):
    if not k.endswith(".ini") and winner(v["data"], k) != FORK:
        pass
print("  read-only providers (non-ini, non-fork winners):")
for w in by_w:
    if w == FORK:
        continue
    kinds = collections.Counter(os.path.splitext(k)[1] for k in by_w[w])
    print(f"    {w}: {dict(kinds)}")
# compare with PICTA: same non-ini providers?
pic_w = {k: winner(vp["data"], k) for k in vp["data"] if k.startswith("enbseries\\") or k in ("enbseries.ini", "picta - weathers of aurbis.ini")}
changed_nonini = [(k, pic_w.get(k), winner(v["data"], k)) for k in sorted(set(pic_w) | set(enb))
                  if not k.endswith(".ini") and pic_w.get(k) != winner(v["data"], k)]
print("  non-ini paths whose winner differs PICTA->baby:", len(changed_nonini))
for x in changed_nonini:
    print("    ", x)
gone = sorted(set(pic_w) - set(enb))
new = sorted(set(enb) - set(pic_w))
print("  paths in PICTA VFS not in baby:", gone)
print("  paths in baby VFS not in PICTA:", new)

# _weatherlist / _locationweather FileName resolution inside the fork
fork_dir = os.path.join(INST, "mods", FORK)
fork_files = {r.lower() for r in (os.path.relpath(os.path.join(dp, f), fork_dir) for dp, _, fn in os.walk(fork_dir) for f in fn)}


def ini_filenames(path):
    out = []
    cur = None
    for ln in open(path, "rb").read().decode("utf-8", "replace").splitlines():
        s = ln.strip()
        if s.startswith("[") and s.endswith("]"):
            cur = s[1:-1]
        elif "=" in s and not s.startswith(";") and s.split("=", 1)[0].strip().lower() == "filename":
            out.append((cur, s.split("=", 1)[1].strip()))
    return out


for lst in ("_weatherlist.ini", "_locationweather.ini", "_worldspaceweatherlist.ini"):
    p = os.path.join(fork_dir, "enbseries", lst)
    w = winner(v["data"], "enbseries\\" + lst)
    src = os.path.join(INST, "mods", w, "enbseries", lst) if w and w != "<overwrite>" else None
    if not src or not os.path.exists(src):
        print(f"  {lst}: winner {w}, no file")
        continue
    fns = ini_filenames(src)
    bad, outside, uniq = [], [], set()
    for sec, fn in fns:
        key = ("enbseries\\" + fn.replace("/", "\\")).lower()
        uniq.add(key)
        wn = winner(v["data"], key)
        if wn is None:
            bad.append((sec, fn))
        elif wn != FORK:
            outside.append((sec, fn, wn))
    print(f"  {lst} (winner {w}): {len(fns)} FileName lines, {len(uniq)} unique files; unresolved {bad}; resolved outside fork {outside}")

# ---------- (b)
report("(b) Root winners in BABY")
rcnt = collections.Counter()
for k in v["root"]:
    rcnt[winner(v["root"], k)] += 1
for w, n in rcnt.most_common():
    print(f"  {n:4d}  {w}")
twin_paths = sorted(k for k, e in v["root"].items() if any(x[1] == BTWIN for x in e))
print("  baby-twin paths:", len(twin_paths))
for k in twin_paths:
    print(f"    {k:45s} -> {winner(v['root'], k)}  stack={[x[1] for x in sorted(v['root'][k])]}")
enbish = sorted(k for k in v["root"] if k.startswith("enb") or "enbseries" in k or "enbcache" in k or k.startswith("d3d") or "reshade" in k)
print("  every enb*/d3d*/reshade Root path and its winner:")
for k in enbish:
    print(f"    {k:55s} -> {winner(v['root'], k)}  stack={[x[1] for x in sorted(v['root'][k])]}")
print("  Picta twin enabled in baby?", PTWIN in order, "; disabled list has it?", PTWIN in v["disabled"])
sh2 = "Silent Horizons 2 - Shader Core"
print(f"  modlist priority index: baby twin {pos.get(BTWIN)}  SH2 Shader Core {pos.get(sh2)}  (lower = higher priority)")
# twin mirrors vs fork
for rel_t, rel_f in [("Root\\enbseries.ini", "enbseries.ini")] + [
        (f"Root\\enbseries\\{n}.fx.ini", f"enbseries\\{n}.fx.ini") for n in ("enbadaptation", "enbbloom", "enbeffect", "enbeffectpostpass")]:
    a = md5(os.path.join(INST, "mods", BTWIN, rel_t)); b = md5(os.path.join(INST, "mods", FORK, rel_f))
    print(f"    {rel_t:45s} twin {a}  fork {b}  {'EQUAL' if a == b else 'DIFF'}")
for rel in ("Root\\enbseries\\enbfxcompiler.ini", "Root\\enbcache\\extexternal.sc", "meta.ini"):
    a = md5(os.path.join(INST, "mods", BTWIN, rel)); b = md5(os.path.join(INST, "mods", PTWIN, rel))
    print(f"    {rel:45s} baby {a}  picta {b}  {'EQUAL' if a == b else 'DIFF'}")
# Root paths in PICTA vs baby winners
diffs = [(k, winner(vp["root"], k), winner(v["root"], k)) for k in sorted(set(vp["root"]) | set(v["root"])) if winner(vp["root"], k) != winner(v["root"], k)]
print("  Root paths whose winner differs PICTA->baby:", diffs)

# ---------- (c)
report("(c) Mist assets + CS Light JSONs in BABY")
mist_paths = sorted(k for k, e in v["data"].items() if any(x[1] == MIST for x in e))
print("  mist mod paths:", len(mist_paths))
for k in mist_paths:
    print(f"    {k:55s} -> {winner(v['data'], k)}  stack={[x[1] for x in sorted(v['data'][k])]}")
for k in sorted(v["data"]):
    if "distant_mounts" in k or "distant_fogs" in k or k.startswith("meshes\\mistsvolumetric") or k.startswith("textures\\volmist"):
        if k not in mist_paths:
            print("    other:", k, "->", winner(v["data"], k), [x[1] for x in sorted(v["data"][k])])
csl = sorted(k for k, e in v["data"].items() if any(x[1] == CSL for x in e))
print("  CS Light window JSONs:", len(csl))
for k in csl:
    print(f"    {k:70s} -> {winner(v['data'], k)}  stack={[x[1] for x in sorted(v['data'][k])]}")
# any LightPlacer path whose winner differs between PICTA and baby
lp = [(k, winner(vp["data"], k), winner(v["data"], k)) for k in sorted(set(vp["data"]) | set(v["data"])) if k.startswith("lightplacer") and winner(vp["data"], k) != winner(v["data"], k)]
print("  LightPlacer winners differing PICTA->baby:", lp)
alld = [(k, winner(vp["data"], k), winner(v["data"], k)) for k in sorted(set(vp["data"]) | set(v["data"])) if winner(vp["data"], k) != winner(v["data"], k)]
print("  ALL collected Data paths whose winner differs PICTA->baby:", len(alld))
cc = collections.Counter((a, b) for _, a, b in alld)
for (a, b), n in cc.most_common():
    print(f"    {n:4d}  {a} -> {b}")
