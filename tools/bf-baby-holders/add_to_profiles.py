"""Add Authoria - Kaidan Holds Baby to PICTA and HPH. Plugin right after HSFVorstag.esp
(its last master); mod folder just above Beeing Female NG in priority so its patched
BF scripts win. Backs up the four profile files first; refuses while MO2/the game runs."""
import os, shutil, subprocess, sys

out = subprocess.run(["tasklist"], stdout=subprocess.PIPE).stdout.decode("utf-8", "replace").lower()
if any(x in out for x in ("modorganizer.exe", "skyrimse.exe", "skse64_loader.exe")):
    sys.exit("MO2 or the game is running - stopped")

ROOT = r"C:\1. AUTHORIA\profiles"
TAG = ".bak-pre-kaidan-holds-baby-20261022"
PLUGIN, MOD = "Authoria - Kaidan Holds Baby.esp", "houseCARL - Authoria - Kaidan Holds Baby"
ANCHOR, GROUP = "HSFVorstag.esp", "Visuals - Racemenu Addons"


def rd(p):
    b = open(p, "rb").read(); assert b"\r\n" in b, p
    return b.decode("utf-8").split("\r\n")


def wr(p, L): open(p, "wb").write("\r\n".join(L).encode("utf-8"))


for prof in ("DEEZ CS NUTZ - PICTA", "Authoria - Preset Studio - HPH"):
    d = os.path.join(ROOT, prof)
    for f in ("plugins.txt", "loadorder.txt", "modlist.txt", "plugingroups.txt"):
        b = os.path.join(d, f + TAG)
        if not os.path.exists(b): shutil.copy2(os.path.join(d, f), b)
    for f, pre in (("plugins.txt", "*"), ("loadorder.txt", "")):
        p = os.path.join(d, f); L = rd(p); names = [x.lstrip("*") for x in L]
        assert PLUGIN not in names, (prof, f)
        L.insert(names.index(ANCHOR) + 1, pre + PLUGIN); wr(p, L)
    p = os.path.join(d, "modlist.txt"); L = rd(p)
    assert "+" + MOD not in L and "-" + MOD not in L
    L.insert(L.index("+Beeing Female NG"), "+" + MOD); wr(p, L)
    p = os.path.join(d, "plugingroups.txt"); L = rd(p)
    i = next(k for k, x in enumerate(L) if x.startswith(ANCHOR + "|"))
    L.insert(i + 1, f"{PLUGIN}|{GROUP}"); wr(p, L)
    print(prof, "ok")
