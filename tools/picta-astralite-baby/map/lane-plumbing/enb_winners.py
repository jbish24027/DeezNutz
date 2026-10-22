"""Resolve MO2 VFS winners for Data\\enbseries* and Root\\enbseries* files in a profile (read-only).

usage: python enb_winners.py "<profile name>" [outfile]
"""
import os, sys, collections, json

INST = r"C:/1. AUTHORIA"
prof = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else None
ml = open(os.path.join(INST, "profiles", prof, "modlist.txt"), encoding="utf-8-sig").read().splitlines()
enabled = []  # highest priority first (file order)
for line in ml:
    if line.startswith("#") or not line:
        continue
    if line.endswith("_separator"):
        continue
    if line[0] == "+":
        enabled.append(line[1:])
# MO2: line 1 = highest priority. Walk lowest -> highest so later wins.
order = list(reversed(enabled))
data_owner = collections.OrderedDict()
data_all = collections.defaultdict(list)
root_owner = {}
root_all = collections.defaultdict(list)
for mod in order:
    p = os.path.join(INST, "mods", mod)
    if not os.path.isdir(p):
        continue
    for top in os.listdir(p):
        tl = top.lower()
        if tl in ("enbseries", "enbseries.ini"):
            tp = os.path.join(p, top)
            if os.path.isfile(tp):
                data_owner["enbseries.ini"] = mod
                data_all["enbseries.ini"].append(mod)
            else:
                for r, ds, fs in os.walk(tp):
                    for f in fs:
                        rel = os.path.relpath(os.path.join(r, f), p).replace("\\", "/").lower()
                        data_owner[rel] = mod
                        data_all[rel].append(mod)
        if tl == "root":
            rp = os.path.join(p, top)
            for r, ds, fs in os.walk(rp):
                for f in fs:
                    rel = os.path.relpath(os.path.join(r, f), rp).replace("\\", "/").lower()
                    root_owner[rel] = mod
                    root_all[rel].append(mod)
# overwrite
ow = os.path.join(INST, "overwrite")
for r, ds, fs in os.walk(ow):
    for f in fs:
        rel = os.path.relpath(os.path.join(r, f), ow).replace("\\", "/").lower()
        if rel.startswith("enbseries"):
            data_owner[rel] = "<overwrite>"
            data_all[rel].append("<overwrite>")
        if rel.startswith("root/"):
            rr = rel[5:]
            root_owner[rr] = "<overwrite/Root>"
            root_all[rr].append("<overwrite/Root>")

lines = []
lines.append(f"PROFILE {prof}: enabled mods {len(enabled)}")
cnt = collections.Counter(data_owner.values())
lines.append("DATA enbseries winners by mod:")
for m, c in cnt.most_common():
    lines.append(f"  {c:5d}  {m}")
cntr = collections.Counter(root_owner.values())
lines.append("ROOT winners by mod (all root files, not just enbseries):")
for m, c in cntr.most_common():
    lines.append(f"  {c:5d}  {m}")
lines.append("ROOT enbseries*/enbcache files:")
for rel in sorted(root_owner):
    if rel.startswith(("enbseries", "enbcache", "enblocal", "d3d11", "dxgi", "reshade", "northman")):
        lines.append(f"  {rel:70s} <- {root_owner[rel]}   (all: {root_all[rel]})")
lines.append("DATA top-level enbseries files (not in a subfolder) + routing:")
for rel in sorted(data_owner):
    if rel.count("/") <= 1:
        lines.append(f"  {rel:70s} <- {data_owner[rel]}   (all: {data_all[rel]})")
txt = "\n".join(lines)
print(txt)
if out:
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
        fh.write("\nFULL DATA MAP\n")
        for rel in sorted(data_owner):
            fh.write(f"{rel}\t{data_owner[rel]}\t{data_all[rel]}\n")
