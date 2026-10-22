"""Summarise file trees of the Picta-lane E11 delivery mods (read-only)."""
import os, sys, collections, hashlib

MODS = r"C:/1. AUTHORIA/mods"
names = sys.argv[1:] or [
    "Authoria - Picta ENB - Root twin",
    "Authoria - Picta 1.1.2 - Darkened to 1.0.1",
    "[NoDelete] Picta ENB 1.1.2 - Data (shipped)",
    "Authoria - Picta - July Depth of Field (AMON ADOF)",
    "Authoria - Picta - Bottled raindrop",
    "[NoDelete] Silent Horizons 2 - Data",
    "Silent Horizons 2 - Shader Core",
    "Authoria - ENB Extender 1.6.0 - KiENBExtender only",
    "KiLoader for Skyrim",
    "[NoDelete] Bottled Shaders",
    "Authoria - ReShade - Picta lane preset",
    "[NoDelete] Soul Core ENB - Data",
    "Authoria - Effects 11 Core - NAT (plain)",
    "houseCARL - Authoria - Patch - Astralite Dawn Warmth",
]
for n in names:
    p = os.path.join(MODS, n)
    print("=" * 100)
    print(n, "exists" if os.path.isdir(p) else "MISSING")
    if not os.path.isdir(p):
        continue
    dirs = collections.Counter()
    total = 0
    files = []
    for root, ds, fs in os.walk(p):
        for f in fs:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, p).replace("\\", "/")
            files.append((rel, os.path.getsize(fp), os.path.getmtime(fp)))
            top = "/".join(rel.split("/")[:3]) if rel.count("/") >= 2 else rel
            dirs["/".join(rel.split("/")[:-1]) or "."] += 1
            total += 1
    print("files:", total)
    for d, c in sorted(dirs.items()):
        print(f"   {c:5d}  {d}/")
    if total <= 60:
        import time
        for rel, sz, mt in sorted(files):
            print(f"      {sz:10d} {time.strftime('%Y-%m-%d %H:%M', time.localtime(mt))} {rel}")
