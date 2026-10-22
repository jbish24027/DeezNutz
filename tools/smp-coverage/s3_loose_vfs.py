"""Build the loose-file VFS for meshes\\ (MO2 priority: modlist.txt first line = highest; overwrite on top)."""
import os, json, time
sp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad"
inst = r"C:\1. AUTHORIA"
t0 = time.time()
mods = []
for line in open(sp + r"\modlist.txt", encoding="utf-8"):
    line = line.rstrip("\r\n")
    if line.startswith("+"):
        mods.append(line[1:])
mods.reverse()  # lowest priority first
print("enabled mods", len(mods))
vfs = {}  # lower relpath (under meshes) -> (mod, fullpath)
nfiles = 0
for m in mods:
    root = os.path.join(inst, "mods", m)
    if not os.path.isdir(root):
        continue
    # find meshes dir case-insensitively
    try:
        entries = os.listdir(root)
    except OSError:
        continue
    md = None
    for e in entries:
        if e.lower() == "meshes" and os.path.isdir(os.path.join(root, e)):
            md = os.path.join(root, e)
            break
    if not md:
        continue
    for dp, dn, fn in os.walk(md):
        rel = os.path.relpath(dp, md)
        for f in fn:
            if not f.lower().endswith((".nif", ".xml", ".tri")):
                continue
            r = ("meshes\\" + (rel + "\\" if rel != "." else "") + f).lower()
            vfs[r] = (m, os.path.join(dp, f))
            nfiles += 1
# overwrite
ow = os.path.join(inst, "overwrite", "meshes")
if os.path.isdir(ow):
    for dp, dn, fn in os.walk(ow):
        rel = os.path.relpath(dp, ow)
        for f in fn:
            if not f.lower().endswith((".nif", ".xml", ".tri")):
                continue
            r = ("meshes\\" + (rel + "\\" if rel != "." else "") + f).lower()
            vfs[r] = ("overwrite", os.path.join(dp, f))
print("files seen", nfiles, "unique paths", len(vfs), "secs", round(time.time() - t0))
json.dump(vfs, open(sp + r"\loose_vfs.json", "w"))
