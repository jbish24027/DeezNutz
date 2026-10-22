"""Which enabled mod wins each target mesh path (loose files only) in a profile, top winner first, plus the full stack."""
import os, sys
ROOT = r"C:\1. AUTHORIA"
PROFILE = sys.argv[1] if len(sys.argv) > 1 else "DEEZ CS NUTZ - PICTA"
PATHS = [r"meshes\clothes\fineclothes01\outfitm_%d.nif", r"meshes\clothes\fineclothes02\outfitm_%d.nif",
         r"meshes\clothes\farmclothes01\torsom_%d.nif", r"meshes\clothes\merchantclothes\outfitm_%d.nif",
         r"meshes\clothes\farmclothes02\m\torso_%d.nif", r"meshes\clothes\farmclothes03\farmerrobe_%d.nif",
         r"meshes\clothes\farmclothes04\robem_%d.nif", r"meshes\clothes\redguard\redguardoutfit_%d.nif",
         r"meshes\clothes\monk\monkvariantoutfit_%d.nif"]
lines = open(os.path.join(ROOT, "profiles", PROFILE, "modlist.txt"), encoding="utf-8").read().splitlines()
enabled = [l[1:] for l in lines if l.startswith("+")]   # top of file = highest priority


def ci(root, rel):
    p = root
    for part in rel.split("\\"):
        try:
            m = [x for x in os.listdir(p) if x.lower() == part.lower()]
        except OSError:
            return None
        if not m:
            return None
        p = os.path.join(p, m[0])
    return p


for pat in PATHS:
    rel = pat % 1
    stack = [m for m in enabled if ci(os.path.join(ROOT, "mods", m), rel)]
    print(rel, "\n   ", " > ".join(stack) if stack else "(BSA only)")
