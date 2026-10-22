import os, shutil
ROOT = r"C:\1. AUTHORIA\profiles"
TAG = ".bak-pre-bf-requiem-20261021"
PLUGIN, MOD = "Authoria - Requiem - Beeing Female.esp", "houseCARL - Authoria - Requiem - Beeing Female"
ANCHOR, MOD_ANCHOR = "Authoria - Patch - Requiem - Wounds.esp", "+Authoria - BF RS Children Faces"

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
        assert PLUGIN not in names
        L.insert(names.index(ANCHOR) + 1, pre + PLUGIN); wr(p, L)
    p = os.path.join(d, "modlist.txt"); L = rd(p)
    assert "+" + MOD not in L and "-" + MOD not in L
    L.insert(L.index(MOD_ANCHOR), "+" + MOD); wr(p, L)
    p = os.path.join(d, "plugingroups.txt"); L = rd(p)
    pos = len(L) - (1 if L[-1] == "" else 0)
    L.insert(pos, f"{PLUGIN}|Authoria - Custom Patches"); wr(p, L)
    print(prof, "ok")
