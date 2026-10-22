"""Merge bulk-B and bulk-C staging into one final mod folder and print the census of what got grafted."""
import os, sys, json, shutil, collections
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
S = os.path.join(sp, "staging")
MOD = "Authoria - SMP Hair Grafts"
final = os.path.join(S, "final", MOD)
if os.path.isdir(final):
    shutil.rmtree(final)
n = 0
for b in ("bulk-B", "bulk-C"):
    root = os.path.join(S, b, MOD)
    for dp, dn, fn in os.walk(root):
        for f in fn:
            src = os.path.join(dp, f)
            rel = os.path.relpath(src, root)
            dst = os.path.join(final, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst); n += 1
npcs = {x["fid"]: x for x in json.load(open(sp + r"\npc_hair.json"))}
ok = {"named": [], "unnamed": []}
skips = collections.Counter()
for b in ("bulk-B", "bulk-C"):
    for fid, st, rep in json.load(open(os.path.join(S, b, "graft_results.json"))):
        if st == "ok":
            ok["named" if npcs[fid]["name"] else "unnamed"].append(fid)
        else:
            skips[(b, str(rep).split("(")[0][:60])] += 1
print("files merged", n, "| grafted named", len(ok["named"]), "unnamed", len(ok["unnamed"]))
print("by defining plugin (named):")
for k, v in collections.Counter(npcs[f]["plugin"] for f in ok["named"]).most_common(20):
    print("  ", v, k)
print("by face source (named):")
for k, v in collections.Counter(npcs[f]["fg_win"] for f in ok["named"]).most_common(20):
    print("  ", v, k)
print("skips:")
for k, v in skips.most_common(12):
    print("  ", v, k)
json.dump(sorted(ok["named"]) + sorted(ok["unnamed"]), open(os.path.join(S, "final", "grafted_fids.json"), "w"))
with open(os.path.join(S, "final", "GRAFTED-NPCS.txt"), "w", encoding="utf-8") as f:
    for fid in sorted(ok["named"], key=lambda x: npcs[x]["name"]):
        nn = npcs[fid]
        f.write("%s | %s | %s | hair %s | face from %s\n" % (nn["name"], nn["eid"], fid, os.path.basename(nn["model"] or ""), nn["fg_win"]))
    f.write("\n-- unnamed --\n")
    for fid in sorted(ok["unnamed"]):
        nn = npcs[fid]
        f.write("%s | %s | hair %s\n" % (nn["eid"], fid, os.path.basename(nn["model"] or "")))
