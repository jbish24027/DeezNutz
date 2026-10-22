"""Install 'Authoria - SMP Black and Necromancer Robes' (built by build_robes.py + make_xml.py) into mods\\ and register it
directly above 'Authoria - SMP Hair Grafts' in every profile that carries that mod, with the same enabled state.
Refuses while MO2 or the game runs, or if the mod folder already exists. CRLF kept; modlist backups .bak-robesmp-20261018.
usage: python -I install.py <staged_mod_dir> [--apply]
"""
import os, sys, shutil, hashlib, subprocess
INST = r"C:\1. AUTHORIA"
NAME = "Authoria - SMP Black and Necromancer Robes"
ANCHOR = "Authoria - SMP Hair Grafts"
BAK = ".bak-robesmp-20261018"

src = sys.argv[1]
apply = "--apply" in sys.argv
tl = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
for p in ("modorganizer.exe", "skyrimse.exe", "skse64_loader.exe"):
    if p in tl:
        sys.exit("REFUSED: %s is running" % p)
dst = os.path.join(INST, "mods", NAME)
if os.path.exists(dst):
    sys.exit("REFUSED: %s exists" % dst)
plans = []
for prof in sorted(os.listdir(os.path.join(INST, "profiles"))):
    ml = os.path.join(INST, "profiles", prof, "modlist.txt")
    if not os.path.isfile(ml):
        continue
    raw = open(ml, "rb").read()
    lines = raw.split(b"\r\n")
    names = [l[1:].decode("utf-8") for l in lines if l[:1] in (b"+", b"-")]
    if NAME in names:
        sys.exit("REFUSED: %s already lists %s" % (prof, NAME))
    idx = [i for i, l in enumerate(lines) if l[1:].decode("utf-8", "replace") == ANCHOR]
    if not idx:
        continue
    i = idx[0]
    state = lines[i][:1]
    new = lines[:i] + [state + NAME.encode("utf-8")] + lines[i:]
    plans.append((prof, ml, raw, b"\r\n".join(new), state.decode()))
for prof, ml, raw, new, st in plans:
    print("%-36s %s%s above %s" % (prof, st, NAME, ANCHOR))
if not apply:
    sys.exit(0)
shutil.copytree(src, dst)
h = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
n = 0
for dp, dn, fn in os.walk(src):
    for f in fn:
        s = os.path.join(dp, f); d = os.path.join(dst, os.path.relpath(s, src))
        assert h(s) == h(d), d; n += 1
for prof, ml, raw, new, st in plans:
    if not os.path.exists(ml + BAK):
        open(ml + BAK, "wb").write(raw)
    open(ml, "wb").write(new)
    assert open(ml, "rb").read() == new
print("installed %d files, registered in %d profiles" % (n, len(plans)))
