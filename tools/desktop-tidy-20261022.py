"""Move project files off the Desktop into C:\\1. AUTHORIA\\Notes and Files and repoint every reference.
Logs moves to Notes and Files\\_moved-from-desktop.txt (undo = move back)."""
import os, shutil, glob

DESK = r"C:\Users\User\Desktop"
DEST = r"C:\1. AUTHORIA\Notes and Files"
KEEP = {"WHAT TO TEST.txt", "desktop.ini", "setup", "Zen.exe", "Canva.lnk", "Games", "ARR.lnk", "Aniimo.lnk"}
os.makedirs(DEST, exist_ok=True)
moved = []
for name in sorted(os.listdir(DESK)):
    if name in KEEP:
        continue
    src = os.path.join(DESK, name)
    dst = os.path.join(DEST, name)
    assert not os.path.exists(dst), dst
    shutil.move(src, dst)
    moved.append(name)
open(os.path.join(DEST, "_moved-from-desktop.txt"), "w", encoding="utf-8").write(
    "Moved from the Desktop on 2026-10-22:\n" + "\n".join(moved) + "\n")
print("moved", len(moved)); print("\n".join(moved))

# repoint references (exact desktop paths of moved items only)
pairs = []
for n in moved:
    for sep in ("\\", "\\\\", "/"):
        old = DESK.replace("\\", sep) + sep + n
        new = DEST.replace("\\", sep) + sep + n
        pairs.append((old, new))
    pairs.append(("Desktop\\" + n, "Notes and Files\\" + n))     # prose mentions
    pairs.append(("Desktop\\\\" + n, "Notes and Files\\\\" + n))
roots = [r"C:\1. AUTHORIA\_tools", r"C:\Users\User\.claude\projects\C--1--AUTHORIA\memory", DEST]
changed = 0
for root in roots:
    for p in glob.glob(os.path.join(root, "**", "*"), recursive=True):
        if not p.lower().endswith((".py", ".md", ".txt", ".json")) or os.path.getsize(p) > 5_000_000:
            continue
        try:
            s = open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, PermissionError):
            continue
        t = s
        for a, b in pairs:
            t = t.replace(a, b)
        if t != s:
            open(p, "w", encoding="utf-8", newline="").write(t)
            changed += 1
print("files repointed:", changed)
