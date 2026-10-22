import os, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifrw import Doc

R = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\6e2f18d5-cfd2-4285-8d26-e57dcbdef3d1\scratchpad\romance-dl\x\Skyrim Romance SE\meshes\BlackWidow71"
for p in [os.path.join(R, "New_Baby_Julian_Crib_Out.nif"), os.path.join(R, "New_Baby_Julian_Crib_In.nif"),
          r"C:\1. AUTHORIA\mods\Lux (main) - rerun\meshes\architecture\whiterun\wrclutter\wrrugsmall01.nif"]:
    d = Doc(p)
    print(os.path.basename(p), d.roots, d.strings[:8])
    for i, (t, b) in enumerate(d.blocks):
        print("  ", i, t, len(b), bytes(b[:40]).hex() if t.startswith("bhk") or t == "BSXFlags" else "")
