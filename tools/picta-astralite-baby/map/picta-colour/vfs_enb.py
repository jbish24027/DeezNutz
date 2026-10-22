"""Resolve the MO2 VFS winner for every enbseries file (Data and Root) in a profile. READ-ONLY."""
import os, sys, json
INST = r"C:/1. AUTHORIA"
PROFILE = sys.argv[1] if len(sys.argv) > 1 else "DEEZ CS NUTZ - PICTA"
OUT = sys.argv[2] if len(sys.argv) > 2 else None

def enabled_mods(profile):
    lines = open(os.path.join(INST, "profiles", profile, "modlist.txt"), encoding="utf-8").read().splitlines()
    mods = []
    for l in lines:
        if l.startswith("+") and not l.endswith("_separator"):
            mods.append(l[1:])
    return mods  # top = highest priority

mods = enabled_mods(PROFILE)
# lowest priority first
order = list(reversed(mods))
providers = {}  # relpath lower -> list of (mod, actualpath)
def scan(root, label, prefix_filter):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root).replace("\\", "/")
            rl = rel.lower()
            if any(rl.startswith(p) for p in prefix_filter):
                providers.setdefault(rl, []).append((label, full.replace("\\", "/")))

PREF = ["enbseries/", "enbseries.ini", "enblocal.ini", "root/enbseries", "root/enblocal", "root/enbseries.ini", "shaders/effects11", "skse/plugins/communityshaders", "skse/plugins/bottled"]
# game data
scan(os.path.join(INST, "Stock Game", "Data"), "<GameData>", PREF)
for m in order:
    p = os.path.join(INST, "mods", m)
    if os.path.isdir(p):
        scan(p, m, PREF)
scan(os.path.join(INST, "overwrite"), "<overwrite>", PREF)

res = {}
for rl, lst in sorted(providers.items()):
    res[rl] = {"winner": lst[-1][0], "path": lst[-1][1], "providers": [x[0] for x in lst]}
summary = {}
for rl, v in res.items():
    top = rl.split("/")[0] if not rl.startswith("enbseries/") else "/".join(rl.split("/")[:2])
    summary.setdefault((v["winner"]), 0)
    summary[v["winner"]] += 1
print(json.dumps(summary, indent=1))
if OUT:
    json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)
