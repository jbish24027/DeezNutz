"""Resolve MO2 VFS winners for enbseries files in a profile (read-only)."""
import os, sys, json
INST = r"C:/1. AUTHORIA"
profile = sys.argv[1]
out = sys.argv[2]
ml = os.path.join(INST, "profiles", profile, "modlist.txt")
lines = open(ml, encoding="utf-8", errors="replace").read().splitlines()
enabled = [l[1:] for l in lines if l.startswith("+")]
# modlist.txt: first line = highest priority. Build low->high.
order = list(reversed(enabled))
winners = {}
for mod in order:
    base = os.path.join(INST, "mods", mod)
    for sub in ("enbseries.ini", "enbseries", "Root/enbseries.ini", "Root/enbseries", "enbseries.fx.ini", "Root"):
        p = os.path.join(base, sub)
        if not os.path.exists(p):
            continue
        if os.path.isfile(p):
            winners[sub.lower()] = mod
        else:
            for root, dirs, files in os.walk(p):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, base).replace(os.sep, "/").lower()
                    if rel.startswith("root/") and not (rel.startswith("root/enbseries") or rel.endswith(".fx") or rel.endswith(".ini") or rel.endswith(".fxh")):
                        continue
                    winners[rel] = mod
# overwrite
ow = os.path.join(INST, "overwrite")
for sub in ("enbseries.ini", "enbseries"):
    p = os.path.join(ow, sub)
    if os.path.isfile(p):
        winners[sub] = "<overwrite>"
    elif os.path.isdir(p):
        for root, dirs, files in os.walk(p):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), ow).replace(os.sep, "/").lower()
                winners[rel] = "<overwrite>"
json.dump(winners, open(out, "w"), indent=1, sort_keys=True)
from collections import Counter
c = Counter(v for k, v in winners.items() if k.startswith("enbseries"))
print("Data enbseries.ini winner:", winners.get("enbseries.ini"))
print("Data enbseries/_weatherlist.ini winner:", winners.get("enbseries/_weatherlist.ini"))
print("Data enbseries/_locationweather.ini winner:", winners.get("enbseries/_locationweather.ini"))
print("Root enbseries.ini winner:", winners.get("root/enbseries.ini"))
print("Data enbseries/* file count by winning mod:", c.most_common())
c2 = Counter(v for k, v in winners.items() if k.startswith("root/"))
print("Root/* by mod:", c2.most_common())
