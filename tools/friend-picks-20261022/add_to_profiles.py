"""Add friend picks (2026-10-22) to PICTA + HPH. Usage: add_to_profiles.py <step>"""
import os, shutil, sys
ROOT = r"C:\1. AUTHORIA\profiles"
PROFILES = ("DEEZ CS NUTZ - PICTA", "Authoria - Preset Studio - HPH")
STEPS = {
    # name: (mods [(mod, insert above this modlist line)], plugins [(plugin, after plugin, group)])
    "xp_hma": ([("Authoria - Experience INI Fix", "+Authoria - MCM and INI Settings"),
                ("Hearthfire Multiple Adoptions - Assorted Patches (Lewis)", "+Hearthfire Multiple Adoptions Expanded Patch Hub")],
               [("Hearthfire Multiple Adoptions - USSEP Fixes - Lux.esp", "Lux - USSEP patch.esp", "Lighting - Lux Patches")]),
    "ride_fish_poisons": ([("Animated Poisons Redone", "+Animated Mounted Casting"),
                           ("Ride Along - Horse Riding Companion", "+Animated Mounted Casting"),
                           ("Dynamic Underwater Fish - SKSE", "+Animated Mounted Casting")],
                          [("RideAlong.esp", "AnimatedMountedCasting.esp", "-- Animations --"),
                           ("DynamicUnderwaterFish.esp", "RideAlong.esp", "-- Animations --")]),
}

def rd(p):
    b = open(p, "rb").read(); assert b"\r\n" in b, p
    return b.decode("utf-8").split("\r\n")

def wr(p, L): open(p, "wb").write("\r\n".join(L).encode("utf-8"))

step = sys.argv[1]
mods, plugins = STEPS[step]
tag = ".bak-pre-friendpicks-%s-20261022" % step
for prof in PROFILES:
    d = os.path.join(ROOT, prof)
    for f in ("plugins.txt", "loadorder.txt", "modlist.txt", "plugingroups.txt"):
        b = os.path.join(d, f + tag)
        if not os.path.exists(b): shutil.copy2(os.path.join(d, f), b)
    p = os.path.join(d, "modlist.txt"); L = rd(p)
    for mod, above in mods:
        assert "+" + mod not in L and "-" + mod not in L, mod
        L.insert(L.index(above), "+" + mod)
    wr(p, L)
    for f, pre in (("plugins.txt", "*"), ("loadorder.txt", "")):
        p = os.path.join(d, f); L = rd(p)
        for plug, after, _ in plugins:
            names = [x.lstrip("*") for x in L]
            assert plug not in names, plug
            L.insert(names.index(after) + 1, pre + plug)
        wr(p, L)
    p = os.path.join(d, "plugingroups.txt"); L = rd(p)
    for plug, _, group in plugins:
        pos = len(L) - (1 if L[-1] == "" else 0)
        L.insert(pos, f"{plug}|{group}")
    wr(p, L)
    print(prof, "ok")
