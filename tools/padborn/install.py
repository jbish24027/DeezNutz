"""Install the freshly built Padborn.dll (+ PDB) into the MO2 mod folder and bump meta.ini.
Backs up the previous DLL beside it. Refuses a DLL that does not carry the 2.2.0 banner."""
import os
import shutil
import sys
import time

BUILD = r"D:\Mods\Code\padborn-build\Release"
MOD = r"C:\1. AUTHORIA\mods\Authoria - Padborn"
PLUGINS = os.path.join(MOD, "SKSE", "Plugins")
STAMP = time.strftime("%Y%m%d")

dll = os.path.join(BUILD, "Padborn.dll")
pdb = os.path.join(BUILD, "Padborn.pdb")
for p in (dll, pdb):
    if not os.path.isfile(p):
        sys.exit(f"missing build output: {p}")

blob = open(dll, "rb").read()
if b"Padborn 2.2.0 loading" not in blob:
    sys.exit("built DLL does not carry the 2.2.0 banner - wrong build?")
if b"first-person block installed" not in blob:
    sys.exit("built DLL lacks the camera module strings - wrong build?")
if b"zoom-in" not in blob:
    sys.exit("built DLL lacks the 2.2.0 zoom-in exception - wrong build?")

dst_dll = os.path.join(PLUGINS, "Padborn.dll")
dst_pdb = os.path.join(PLUGINS, "Padborn.pdb")
if os.path.isfile(dst_dll):
    bak = os.path.join(PLUGINS, f"Padborn.dll.bak-2.1.0-{STAMP}")
    if not os.path.exists(bak):
        shutil.copy2(dst_dll, bak)
        print("backed up old DLL ->", os.path.basename(bak))
shutil.copy2(dll, dst_dll)
shutil.copy2(pdb, dst_pdb)
print(f"installed Padborn.dll ({len(blob)} bytes) + Padborn.pdb into {PLUGINS}")

meta = os.path.join(MOD, "meta.ini")
raw = open(meta, "rb").read()
if b"version=3.1.0" in raw:
    raw = raw.replace(b"version=3.1.0", b"version=3.2.0", 1)
    open(meta, "wb").write(raw)
    print("meta.ini version -> 3.2.0")
else:
    print("meta.ini version line not 3.1.0, left alone")
