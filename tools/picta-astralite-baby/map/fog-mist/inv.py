import os, sys, json, hashlib
MODS = "C:/1. AUTHORIA/mods"
mods = [
 "[NoDelete] Astralite Weathers",
 "[NoDelete] Astralite Weathers - 4K Clouds",
 "[NoDelete] Soul Core Plugin and Assets",
 "[NoDelete] Soul Core ENB - Data",
 "[NoDelete] Mists of Tamriel",
 "[NoDelete] Picta - Assets 4K",
 "[NoDelete] Picta - Weathers of Aurbis 1.1.1 (shipped)",
 "[NoDelete] Picta - Cloudy Windy panoramas 11-15 (2K originals)",
 "[NoDelete] Picta ENB 1.1.2 - Data (shipped)",
 "Picta Series - Improved Sky Meshes",
 "Authoria - Picta 1.1.2 - Darkened to 1.0.1",
 "Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1",
 "Authoria - Picta ENB - Root twin",
 "houseCARL - Authoria - Patch - Picta Seasonal",
 "houseCARL - Authoria - Picta over NAT",
 "Authoria - Effects 11 Core - NAT (plain)",
 "houseCARL - Authoria - Patch - Astralite Dawn Warmth",
 "No More Blinding Fog",
 "Praedys Sky AIO",
 "Interior Floating Fog Remover",
 "Remove Interior Fog",
 "NAT.ENB - ESP WEATHER PLUGIN v3.1.1C - Fixed",
 "Helios",
 "Authoria - Helios - Picta exit weather",
 "[NoDelete] Soul Core - KreatE Templates",
 "Less Distracting Blowing Snow Effects - ENB Particle Patch",
 "The Mists of Blackreach",
 "[NoDelete] Bottled Shaders",
]
out = {}
def md5(p):
    h = hashlib.md5()
    with open(p,'rb') as f:
        for ch in iter(lambda: f.read(1<<20), b''):
            h.update(ch)
    return h.hexdigest()
for m in mods:
    root = os.path.join(MODS, m)
    if not os.path.isdir(root):
        out[m] = None; print("MISSING", m); continue
    files = []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root).replace("\\", "/")
            sz = os.path.getsize(full)
            files.append({"rel": rel, "size": sz})
    out[m] = files
    print("==", m, len(files))
json.dump(out, open(os.path.join(os.path.dirname(__file__), "inventory.json"), "w"), indent=1)
