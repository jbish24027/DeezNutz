"""Register 'Authoria - SMP Vanilla Coats' enabled directly above 'Authoria - SMP Black and Necromancer Robes' in every profile
that has the robes mod. Byte-preserving (CRLF kept), backup modlist.txt.bak-coatsmp-20261018 first, idempotent."""
import os, subprocess, sys
ROOT = r"C:\1. AUTHORIA"
NEW, ANCHOR = "Authoria - SMP Vanilla Coats", "Authoria - SMP Black and Necromancer Robes"
tl = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
if "modorganizer.exe" in tl or "skyrimse.exe" in tl:
    sys.exit("MO2 or the game is running - nothing written")
for prof in sorted(os.listdir(os.path.join(ROOT, "profiles"))):
    p = os.path.join(ROOT, "profiles", prof, "modlist.txt")
    if not os.path.exists(p):
        continue
    raw = open(p, "rb").read()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    lines = raw.split(nl)
    names = [l[1:].decode("utf-8") for l in lines if l[:1] in (b"+", b"-")]
    if ANCHOR not in names:
        continue
    if NEW in names:
        print(prof, "already has it"); continue
    i = next(k for k, l in enumerate(lines) if l[1:].decode("utf-8") == ANCHOR and l[:1] in (b"+", b"-"))
    open(p + ".bak-coatsmp-20261018", "wb").write(raw)
    lines.insert(i, b"+" + NEW.encode("utf-8"))
    open(p, "wb").write(nl.join(lines))
    print(prof, "added at line", i + 1)
