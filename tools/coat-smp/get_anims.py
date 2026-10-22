"""Extract the vanilla character skeleton.hkx (m/f) and walk/run/sprint clips from the game BSAs for the coat toolkit checks."""
import os, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\smp-coverage")
from bsareader import BSA

DATA = r"C:\1. AUTHORIA\Stock Game\Data"
OUT = r"C:\1. AUTHORIA\_tools\coat-smp\anims"
WANT = [r"meshes\actors\character\character assets\skeleton.hkx",
        r"meshes\actors\character\character assets female\skeleton_female.hkx"]
for clip in ("mt_walkforward", "mt_runforward", "mt_sprintforward", "mt_idle"):
    WANT += [r"meshes\actors\character\animations\male\%s.hkx" % clip,
             r"meshes\actors\character\animations\female\%s.hkx" % clip,
             r"meshes\actors\character\animations\%s.hkx" % clip]
found = {}
for name in sorted(os.listdir(DATA)):
    if not name.lower().endswith(".bsa"):
        continue
    try:
        b = BSA(os.path.join(DATA, name))
    except Exception as e:
        continue
    for w in WANT:
        if w in b.files and w not in found:
            data = b.extract(w) if hasattr(b, "extract") else b.read(w)
            p = os.path.join(OUT, w)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(data)
            found[w] = name
for w in WANT:
    print(("OK  " + found[w]) if w in found else "--  missing", w)
