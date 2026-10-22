"""
Insert the Player Dirt Overlays bridge into all four Authoria profiles.

Usage: python insert_player_dirt_overlays.py [--dry]

Follows the house rules:
  * modlist.txt is DESCENDING priority (line 1 = highest). The two new mod folders go directly
    ABOVE (= earlier in the file than) "Ultimate Body Enhancer - Dirt and Blood", enabled.
  * The plugin goes right AFTER "Ultimate Body Enhancer - Dirt and Blood.esp" in plugins.txt
    (starred) and loadorder.txt - i.e. before every "Authoria - Output -" plugin.
  * plugingroups.txt gets "<plugin>|Authoria - Master Patches" (the anchor plugin's group),
    file kept sorted.
  * Any line MO2 may already have auto-parked for these names is removed first (idempotent).
  * Backups: <file>.bak-playerdirt-20260821 beside each touched file (only if not present yet).
  * Refuses to run while ModOrganizer.exe / SkyrimSE.exe is running.
  * Verifies afterwards that nothing new sits in the FWMF/LOD-output head of any modlist or in
    the output tail of any loadorder.
"""
import os, sys, io, subprocess

ROOT = r"C:\1. AUTHORIA"
PROFILES = [
    "Authoria - Requiem Reforged - Main Profile",
    "Authoria - Requiem Reforged - NSFW Profile",
    "DEEEZ NUTTZZZ",
    "DEEZ CS NUTZ",
]
NEW_MODS = [  # file order = priority order (first = highest of the two)
    "houseCARL - Authoria - Patch - Player Dirt Overlays",
    "BISR - Zaki Renewed - UBE Set A",
]
ANCHOR_MOD = "Ultimate Body Enhancer - Dirt and Blood"
NEW_PLUGIN = "Authoria - Patch - Player Dirt Overlays.esp"
ANCHOR_PLUGIN = "Ultimate Body Enhancer - Dirt and Blood.esp"
GROUP = "Authoria - Master Patches"
BAK = ".bak-playerdirt-20260821"
DRY = "--dry" in sys.argv


def running(names):
    out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
    return [n for n in names if n.lower() in out]


def read_lines(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        raw = f.read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    return raw.split(nl), nl


def write_lines(p, lines, nl):
    if DRY:
        return
    if not os.path.exists(p + BAK):
        with io.open(p, "rb") as src, io.open(p + BAK, "wb") as dst:
            dst.write(src.read())
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(lines))


def strip_existing(lines, names, plugin=False):
    out = []
    for l in lines:
        core = l[1:] if (not plugin and l[:1] in "+-") else (l[1:] if (plugin and l[:1] == "*") else l)
        if core in names:
            continue
        out.append(l)
    return out


def main():
    busy = running(["ModOrganizer.exe", "SkyrimSE.exe", "skse64_loader.exe"])
    if busy and not DRY:
        print("REFUSING: running ->", busy)
        sys.exit(2)
    report = []
    for prof in PROFILES:
        d = os.path.join(ROOT, "profiles", prof)

        # ---- modlist ----
        p = os.path.join(d, "modlist.txt")
        lines, nl = read_lines(p)
        lines = strip_existing(lines, set(NEW_MODS))
        idx = next((i for i, l in enumerate(lines) if l[1:] == ANCHOR_MOD), None)
        if idx is None:
            report.append("!! %s: modlist anchor %r missing" % (prof, ANCHOR_MOD)); continue
        for k, m in enumerate(NEW_MODS):
            lines.insert(idx + k, "+" + m)
        write_lines(p, lines, nl)
        report.append("%s: modlist -> %s at lines %d-%d (above %r, line %d)" % (
            prof, ", ".join(NEW_MODS), idx + 1, idx + len(NEW_MODS), ANCHOR_MOD, idx + len(NEW_MODS) + 1))

        # ---- plugins.txt ----
        p = os.path.join(d, "plugins.txt")
        lines, nl = read_lines(p)
        lines = strip_existing(lines, {NEW_PLUGIN}, plugin=True)
        idx = next((i for i, l in enumerate(lines) if l.lstrip("*") == ANCHOR_PLUGIN), None)
        if idx is None:
            report.append("!! %s: plugins.txt anchor missing" % prof); continue
        lines.insert(idx + 1, "*" + NEW_PLUGIN)
        write_lines(p, lines, nl)
        report.append("%s: plugins.txt -> line %d (after %s)" % (prof, idx + 2, ANCHOR_PLUGIN))

        # ---- loadorder.txt ----
        p = os.path.join(d, "loadorder.txt")
        lines, nl = read_lines(p)
        lines = strip_existing(lines, {NEW_PLUGIN}, plugin=True)
        idx = next((i for i, l in enumerate(lines) if l == ANCHOR_PLUGIN), None)
        if idx is None:
            report.append("!! %s: loadorder anchor missing" % prof); continue
        lines.insert(idx + 1, NEW_PLUGIN)
        write_lines(p, lines, nl)
        report.append("%s: loadorder.txt -> line %d" % (prof, idx + 2))

        # ---- plugingroups.txt ----
        p = os.path.join(d, "plugingroups.txt")
        lines, nl = read_lines(p)
        head = [l for l in lines if l.startswith("#")]
        body = [l for l in lines if not l.startswith("#") and l.strip() and not l.startswith(NEW_PLUGIN + "|")]
        body.append(NEW_PLUGIN + "|" + GROUP)
        body.sort(key=lambda s: s.split("|")[0].lower())
        trailing = [""] if lines and lines[-1] == "" else []
        write_lines(p, head + body + trailing, nl)
        report.append("%s: plugingroups.txt -> %s|%s" % (prof, NEW_PLUGIN, GROUP))

        # ---- verify the protected blocks ----
        ml, _ = read_lines(os.path.join(d, "modlist.txt"))
        bad = [l for l in ml[:38] if l[1:] in NEW_MODS]
        lo, _ = read_lines(os.path.join(d, "loadorder.txt"))
        try:
            t = lo.index("Authoria - Output - Synthesis Gameplay.esp")
            bad += [l for l in lo[t:] if l == NEW_PLUGIN]
        except ValueError:
            report.append("!! %s: Synthesis Gameplay anchor not found for tail check" % prof)
        report.append("%s: protected-block check %s" % (prof, "OK" if not bad else "FAILED " + repr(bad)))

    print("\n".join(report))
    print("DRY RUN - nothing written" if DRY else "written")


if __name__ == "__main__":
    main()
