r"""Install the two file-level fair script-flood edits (SkyPatcher INI + OBody JSON) with backups.

The third edit (the SOS condition) is a houseCARL in-place apply, run separately with
staging\SOS\sos_fair_exclusion_ops.json; this script only backs up that plugin.

Usage: python -I install.py [--dry-run] [--undo]
Refuses to run while ModOrganizer.exe or SkyrimSE.exe is running.
"""
import argparse, os, shutil, subprocess, sys, json, datetime as dt

ROOT = r"C:\1. AUTHORIA"
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.join(HERE, "staging")
BACKUP = os.path.join(ROOT, "_backups", "2026-10-15 - Fair script flood")

INI_SRC = os.path.join(STAGE, "SkyPatcher", "npc", "Authoria - Wanderers Fair", "SkyrimFair.esp.ini")
INI_DST = os.path.join(ROOT, "mods", "houseCARL - Authoria - Patch - Holidays and Fair - Requiem",
                       "SKSE", "Plugins", "SkyPatcher", "npc", "Authoria - Wanderers Fair", "SkyrimFair.esp.ini")
JSON_SRC = os.path.join(STAGE, "OBody", "OBody_presetDistributionConfig.json")
JSON_DST = os.path.join(ROOT, "mods", "Authoria - OBODY Distro", "skse", "plugins", "OBody_presetDistributionConfig.json")
SOS_ESP = os.path.join(ROOT, "mods", "Authoria - Ostim tweaks and Patches", "Authoria - SOS Custom Races.esp")

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ap.add_argument("--undo", action="store_true")
a = ap.parse_args()

def running(*names):
    out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
    return [n for n in names if n.lower() in out]

busy = running("ModOrganizer.exe", "SkyrimSE.exe", "skse64_loader.exe")
if busy:
    print("REFUSED: still running:", ", ".join(busy)); sys.exit(2)

def say(*x): print(*x)

if a.undo:
    say("UNDO")
    if os.path.exists(INI_DST):
        say(" delete", INI_DST); a.dry_run or os.remove(INI_DST)
    for name, dst in (("OBody_presetDistributionConfig.json", JSON_DST), ("Authoria - SOS Custom Races.esp", SOS_ESP)):
        src = os.path.join(BACKUP, name)
        if os.path.exists(src):
            say(" restore", src, "->", dst); a.dry_run or shutil.copy2(src, dst)
        else:
            say(" no backup for", name, "- nothing restored")
    sys.exit(0)

say("INSTALL" + (" (dry run)" if a.dry_run else ""))
# 0. sanity on the staged files
assert os.path.exists(INI_SRC), INI_SRC
d = json.load(open(JSON_SRC, encoding="utf-8"))
for k in ("blacklistedNpcsPluginFemale", "blacklistedNpcsPluginMale"):
    assert "SkyrimFair.esp" in d[k], k
assert os.path.exists(JSON_DST) and os.path.exists(SOS_ESP)

# 1. backups (never overwrite an existing backup)
if not a.dry_run: os.makedirs(BACKUP, exist_ok=True)
for src in (JSON_DST, SOS_ESP):
    dst = os.path.join(BACKUP, os.path.basename(src))
    if os.path.exists(dst):
        say(" backup exists, kept:", dst)
    else:
        say(" backup", src, "->", dst); a.dry_run or shutil.copy2(src, dst)

# 2. SkyPatcher INI
say(" copy", INI_SRC, "->", INI_DST)
if not a.dry_run:
    os.makedirs(os.path.dirname(INI_DST), exist_ok=True); shutil.copy2(INI_SRC, INI_DST)

# 3. OBody JSON
say(" copy", JSON_SRC, "->", JSON_DST)
if not a.dry_run: shutil.copy2(JSON_SRC, JSON_DST)

say("done. Next: houseCARL apply in place on 'Authoria - SOS Custom Races.esp' with staging\\SOS\\sos_fair_exclusion_ops.json")
