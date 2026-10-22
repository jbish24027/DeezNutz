"""Copy the stage into 'Authoria - SMP Vanilla Coats': MO2 + game must be closed, every file it replaces is backed up first
(outside the mods tree), hashes verified after; then report which mod wins each staged path in the given profiles."""
import os, sys, shutil, hashlib, subprocess, datetime
ROOT = r"C:\1. AUTHORIA"
STAGE = os.path.join(ROOT, r"_tools\coat-smp\designs\stage\m")
MOD = os.path.join(ROOT, r"mods\Authoria - SMP Vanilla Coats")
BK = r"D:\1. MOD STUFF\- ARR STUFF\coat-smp-backups\%s" % datetime.datetime.now().strftime("%Y%m%d-%H%M")
tl = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
if "modorganizer.exe" in tl or "skyrimse.exe" in tl:
    sys.exit("MO2 or the game is running - nothing written")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rels = [os.path.relpath(os.path.join(d, f), STAGE) for d, _, fs in os.walk(STAGE) for f in fs]
new = rep = same = 0
for r in rels:
    dst = os.path.join(MOD, r); src = os.path.join(STAGE, r)
    if os.path.exists(dst):
        if h(dst) == h(src): same += 1; continue
        b = os.path.join(BK, r); os.makedirs(os.path.dirname(b), exist_ok=True); shutil.copy2(dst, b); rep += 1
    else:
        new += 1
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
bad = [r for r in rels if h(os.path.join(MOD, r)) != h(os.path.join(STAGE, r))]
print(f"{len(rels)} staged files: {new} new, {rep} replaced (backed up to {BK if rep else '-'}), {same} unchanged; hash mismatches {len(bad)}")
for prof in sys.argv[1:]:
    on = [l[1:] for l in open(os.path.join(ROOT, "profiles", prof, "modlist.txt"), encoding="utf-8").read().splitlines() if l.startswith("+")]
    lost = []
    for r in rels:
        win = next((m for m in on if os.path.exists(os.path.join(ROOT, "mods", m, r))), None)
        if win != "Authoria - SMP Vanilla Coats": lost.append((r, win))
    print(f"{prof}: coats mod wins {len(rels) - len(lost)} of {len(rels)}" + "".join(f"\n   LOSES {r} to {w}" for r, w in lost))
