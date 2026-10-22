"""Install the 2026-10-16 fair stage trim + far-view fixes. Run ONLY with MO2 and the game closed.

 1. backup + replace 'Authoria - Patch - Wanderers Fair - No Reseat.esp' in its mod folder
 2. copy the two shadow-free paper lantern meshes into the Holidays and Fair Requiem patch mod
 3. SSE FPS Stabilizer: FPSStabilizerEnabled = 0 in BOTH ini copies (winner + base mod)
 4. every profile: SkyrimCustom.ini + SkyrimPrefs.ini fade multipliers -> Objects 15, Actors 12, Items 4.5
 5. CRDW: delete the interface cache in every profile cache dir (new loose meshes -> full rebuild)
Byte-preserving line endings; every touched file is copied to the backup folder first.
"""
import os
import re
import shutil

ROOT = r"C:\1. AUTHORIA"
SCR = os.path.dirname(os.path.abspath(__file__))
BK = os.path.join(ROOT, r"_backups\2026-10-16 - Fair stage trim + stabilizer off")
os.makedirs(BK, exist_ok=True)


def backup(path, tag=""):
    rel = os.path.relpath(path, ROOT).replace("\\", "__").replace("/", "__")
    dst = os.path.join(BK, rel + tag)
    shutil.copy2(path, dst)
    return dst


def edit_keys(path, changes, add_missing_section=None):
    """changes: {key_lower: 'Key=Value' full line}. Byte-preserving newline. Returns count changed."""
    raw = open(path, "rb").read()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    lines = raw.decode("utf-8", errors="surrogateescape").split(nl.decode())
    done = set()
    out = []
    for line in lines:
        m = re.match(r"^\s*([A-Za-z0-9_]+)\s*=", line)
        key = m.group(1).lower() if m else None
        if key in changes and key not in done:
            out.append(changes[key])
            done.add(key)
        else:
            out.append(line)
    open(path, "wb").write(nl.decode().join(out).encode("utf-8", errors="surrogateescape"))
    return len(done)


# 1. patch esp
mod = os.path.join(ROOT, r"mods\houseCARL - Authoria - Patch - Wanderers Fair - No Reseat")
esp = os.path.join(mod, "Authoria - Patch - Wanderers Fair - No Reseat.esp")
print("backup:", backup(esp, ".before"))
shutil.copy2(os.path.join(SCR, "out", "Authoria - Patch - Wanderers Fair - No Reseat.esp"), esp)
print("installed trimmed patch:", os.path.getsize(esp), "bytes")

# 2. lantern meshes
dst_dir = os.path.join(ROOT, r"mods\houseCARL - Authoria - Patch - Holidays and Fair - Requiem\meshes\barry_paper_lanterns")
os.makedirs(dst_dir, exist_ok=True)
for n in ("lantern_round_blue.nif", "lantern_tall_red.nif"):
    shutil.copy2(os.path.join(SCR, "lanterns", "meshes", "barry_paper_lanterns", n), os.path.join(dst_dir, n))
    print("lantern mesh placed:", n)

# 3. stabilizer off (both copies)
for ini in (os.path.join(ROOT, r"mods\Authoria - MCM and INI Settings\SKSE\Plugins\SSEFpsStabilizer.ini"),
            os.path.join(ROOT, r"mods\SSE FPS Stabilizer\SKSE\Plugins\SSEFpsStabilizer.ini")):
    backup(ini, ".before")
    n = edit_keys(ini, {"fpsstabilizerenabled": "FPSStabilizerEnabled = 0\t\t\t#Set this to 0 if you only want to use console feature of this mod. (Authoria 2026-10-16: off - it sat on its bottom rung at 4K)"})
    print("stabilizer off:", ini.split(os.sep)[-4], "changed", n)

# 4. fades in every profile
prof = os.path.join(ROOT, "profiles")
for p in sorted(os.listdir(prof)):
    for name, fmt in (("SkyrimCustom.ini", "{k}={v}"), ("SkyrimPrefs.ini", "{k} ={v}")):
        f = os.path.join(prof, p, name)
        if not os.path.isfile(f):
            continue
        backup(f, "." + p + ".before")
        vals = {"flodfadeoutmultobjects": ("fLODFadeOutMultObjects", "15.0000" if name == "SkyrimPrefs.ini" else "15.0"),
                "flodfadeoutmultactors": ("fLODFadeOutMultActors", "12.0000" if name == "SkyrimPrefs.ini" else "12.0"),
                "flodfadeoutmultitems": ("fLODFadeOutMultItems", "4.5000" if name == "SkyrimPrefs.ini" else "4.5")}
        n = edit_keys(f, {k: fmt.format(k=v[0], v=v[1]) for k, v in vals.items()})
        print(f"  {p} / {name}: {n} fade keys set")

# 5. CRDW
for p in sorted(os.listdir(prof)):
    c = os.path.join(prof, p, "CRDW Automatic Mode", "cache", "data_interface_.cache")
    if os.path.isfile(c):
        os.remove(c)
        print("  CRDW rebuild forced:", p)
print("done; backups in", BK)
