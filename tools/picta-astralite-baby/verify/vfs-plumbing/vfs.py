"""Read-only MO2 VFS simulation for selected path families in a profile.

Usage: python -I -B vfs.py <profile name> <out.json>
Loose files only. Priority: overwrite > modlist top ('+' lines, first = highest) > ... > Stock Game\\Data (Data only).
Collects: Data enbseries/**, top-level *.ini, LightPlacer/**, meshes/effects/**, meshes/mistsvolumetric/**,
textures/effects/**, textures/volmist/**, and Root/** (Root Builder mods).
"""
import json, os, sys

INST = r"C:\1. AUTHORIA"
LP = "\\\\?\\"
prof = sys.argv[1]
out_path = sys.argv[2]

lines = open(os.path.join(INST, "profiles", prof, "modlist.txt"), "rb").read().decode("utf-8").split("\r\n")
enabled = [l[1:] for l in lines if l.startswith("+")]
disabled = [l[1:] for l in lines if l.startswith("-")]
order = ["<overwrite>"] + enabled  # index 0 = highest priority

DATA_DIRS = {"enbseries": None, "lightplacer": None,
             "meshes": {"effects", "mistsvolumetric"}, "textures": {"effects", "volmist"}}


def mod_dir(m):
    return os.path.join(INST, "overwrite") if m == "<overwrite>" else os.path.join(INST, "mods", m)


def walk(base):
    for dp, dn, fn in os.walk(LP + base):
        for f in fn:
            p = os.path.join(dp, f)[len(LP):]
            yield os.path.relpath(p, base)


def collect(base):
    data, root = {}, {}
    if not os.path.isdir(LP + base):
        return data, root, False
    for e in os.scandir(LP + base):
        n = e.name.lower()
        if e.is_file():
            if n.endswith(".ini") or n.endswith(".txt") or n.endswith(".json"):
                data[n] = e.name
            continue
        if n == "root":
            for rel in walk(os.path.join(base, e.name)):
                root[rel.lower()] = rel
        elif n in DATA_DIRS:
            subs = DATA_DIRS[n]
            if subs is None:
                for rel in walk(os.path.join(base, e.name)):
                    data[(n + "\\" + rel).lower()] = e.name + "\\" + rel
            else:
                for s in os.scandir(e.path):
                    if s.is_dir() and s.name.lower() in subs:
                        for rel in walk(os.path.join(base, e.name, s.name)):
                            data[(n + "\\" + s.name + "\\" + rel).lower()] = e.name + "\\" + s.name + "\\" + rel
    return data, root, True


res = {"profile": prof, "order": order, "disabled": disabled, "data": {}, "root": {}, "missing_mod_folders": []}
for i, m in enumerate(order):
    d, r, ok = collect(mod_dir(m))
    if not ok:
        res["missing_mod_folders"].append(m)
        continue
    for k, v in d.items():
        res["data"].setdefault(k, []).append([i, m, v])
    for k, v in r.items():
        res["root"].setdefault(k, []).append([i, m, v])
# Stock Game Data as the lowest layer
sg = os.path.join(INST, "Stock Game", "Data")
d, _, _ = collect(sg)
for k, v in d.items():
    res["data"].setdefault(k, []).append([10 ** 6, "<Stock Game\\Data>", v])
json.dump(res, open(out_path, "w", encoding="utf-8"), indent=0)
print("mods enabled", len(enabled), "data paths", len(res["data"]), "root paths", len(res["root"]),
      "missing folders", res["missing_mod_folders"])
