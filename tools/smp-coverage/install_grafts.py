"""Install the staged graft mod + the SMP-NPC crash fix into the MO2 instance. Dry-run unless --apply.
Refuses while ModOrganizer.exe or SkyrimSE.exe is running. Registers both mods in the six profiles that carry
the Younglings faces patch (DEEEZ, HPH, CS, CS PBR, CS PICTA, PICTA EXPERIMENT), grafts at top priority
(directly under Testing_separator), crash fix directly above FSMP.
usage: install_grafts.py <staging graft mod folder> [--apply]
"""
import os, sys, shutil, subprocess, datetime
inst = r"C:\1. AUTHORIA"
GRAFT = "Authoria - SMP Hair Grafts"
FIX = "SMP-NPC crash fix"
PROFILES = ["DEEEZ NUTTZZZ", "Authoria - Preset Studio - HPH", "DEEZ CS NUTZ", "DEEZ CS NUTZ - PBR", "DEEZ CS NUTZ - PICTA", "PICTA EXPERIMENT"]
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")


def running():
    out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
    return [p for p in ("modorganizer.exe", "skyrimse.exe") if p in out]


def main():
    src = sys.argv[1]
    apply = "--apply" in sys.argv
    fix_src = os.path.join(os.path.dirname(src.rstrip("\\/")), FIX)
    r = running()
    if r:
        print("REFUSED: still running:", r); return 2
    n = sum(len(f) for _, _, f in os.walk(src))
    print("graft mod files:", n, "| crash fix present:", os.path.isdir(fix_src))
    for name, s in ((GRAFT, src), (FIX, fix_src)):
        dst = os.path.join(inst, "mods", name)
        print("%s -> %s (%s)" % (s, dst, "exists, will be replaced" if os.path.isdir(dst) else "new"))
        if apply:
            lp = lambda p: "\\\\?\\" + os.path.abspath(p)  # long-path safe (one plugin name pushes a path past 260)
            if os.path.isdir(dst):
                shutil.rmtree(lp(dst))
            shutil.copytree(lp(s), lp(dst))
            meta = os.path.join(dst, "meta.ini")
            if not os.path.exists(meta):
                body = "[General]\ngameName=skyrimse\nmodid=%s\nversion=%s\ninstallationFile=\n" % (("91616", "1") if name == FIX else ("0", stamp))
                open(meta, "w", encoding="utf-8").write(body.replace("\n", "\r\n"))
    for prof in PROFILES:
        ml = os.path.join(inst, "profiles", prof, "modlist.txt")
        if not os.path.exists(ml):
            print("  profile missing:", prof); continue
        raw = open(ml, "rb").read()
        lines = raw.decode("utf-8").split("\r\n")
        lines = [l for l in lines if l[1:] not in (GRAFT, FIX)]
        try:
            ti = next(i for i, l in enumerate(lines) if l.endswith("Testing_separator"))
        except StopIteration:
            ti = 0
        lines.insert(ti + 1, "+" + GRAFT)
        try:
            fi = next(i for i, l in enumerate(lines) if l == "+FSMP - Faster HDT-SMP")
            lines.insert(fi, "+" + FIX)
        except StopIteration:
            lines.insert(ti + 2, "+" + FIX)
        print("  %s: grafts at line %d, crash fix above FSMP" % (prof, ti + 2))
        if apply:
            shutil.copy2(ml, ml + ".bak-smphair-" + stamp)
            open(ml, "wb").write("\r\n".join(lines).encode("utf-8"))
    print("APPLIED" if apply else "DRY RUN (add --apply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
