"""Repack `Authoria Padborn.zip` as 3.2.0.

Takes the shipped 3.0.0 archive, swaps in: the 2.1.0 DLL (+ PDB), the updated README (root + Core),
both Padborn.json variants with the camera block, the Layout 402 controlmaps with Toggle POV off the
gamepad (text + binary), the updated fomod xmls, and the updated Source tree. Everything else is
copied byte-for-byte. The old archive is kept as `Authoria Padborn 3.1.0.zip`.
"""
import os
import sys
import time
import zipfile

ARCHIVE_DIR = r"D:\1. MOD STUFF\1. SKYRIM FILES\authoria own mods and patches"
OLD = os.path.join(ARCHIVE_DIR, "Authoria Padborn.zip")
OLD_KEEP = os.path.join(ARCHIVE_DIR, "Authoria Padborn 3.1.0.zip")
TMP = os.path.join(ARCHIVE_DIR, "Authoria Padborn.zip.new")

TOOLS = os.path.dirname(os.path.abspath(__file__))
MOD = r"C:\1. AUTHORIA\mods\Authoria - Padborn"
BUILD = r"D:\Mods\Code\padborn-build\Release"

BS = chr(92)


def read(p):
    with open(p, "rb") as f:
        return f.read()


def norm(name):
    return name.replace(BS, "/")


# ---------------------------------------------------------------- inputs
dll = read(os.path.join(BUILD, "Padborn.dll"))
pdb = read(os.path.join(BUILD, "Padborn.pdb"))
assert b"Padborn 2.2.0 loading" in dll and b"first-person block installed" in dll and b"zoom-in" in dll, "wrong DLL build"

readme = read(os.path.join(MOD, "README.md"))
assert b"Padborn 3.2.0" in readme

json_off = read(os.path.join(MOD, "SKSE", "Plugins", "Padborn.json"))
assert b'"camera": { "blockFirstPerson": true, "allowManualToggle": false, "allowZoomIn": true }' in json_off
off_line = b'"sprint": { "enabled": false, "log": false, "button": "keep" }'
assert json_off.count(off_line) == 1
json_on = json_off.replace(off_line, b'"sprint": { "enabled": true, "log": false, "button": "keep" }')

binary_map = read(os.path.join(MOD, "ControlMap_Custom.txt"))
info_xml = read(os.path.join(TOOLS, "fomod", "info.xml"))
module_xml = read(os.path.join(TOOLS, "fomod", "ModuleConfig.xml"))
assert b"<Version>3.2.0</Version>" in info_xml

# ---------------------------------------------------------------- old archive
old = zipfile.ZipFile(OLD)
entries = [(norm(i.filename), i) for i in old.infolist()]
by_name = {n: i for n, i in entries}

old_binary = old.read(by_name["Layout 402/ControlMap_Custom.txt"])
diff = [i for i, (x, y) in enumerate(zip(old_binary, binary_map)) if x != y]
assert len(old_binary) == len(binary_map) == 329 and diff in ([], [0x134]), diff

old_text = old.read(by_name["Layout 402/Interface/controls/pc/controlmap.txt"])
pov_old = b"Toggle POV\t\t\t0x21\t\t\t\t0xff\t0x0080\t\t\t\t1\t1\t1\t0x820"
pov_new = b"Toggle POV\t\t\t0x21\t\t\t\t0xff\t0xff\t\t\t\t1\t1\t1\t0x820"
if old_text.count(pov_new) == 1:
    text_map = old_text  # archive already carries the R3 fix (3.1.0+)
else:
    assert old_text.count(pov_old) == 1
    text_map = old_text.replace(pov_old, pov_new)

# ---------------------------------------------------------------- source tree
source_files = {}
src_root = os.path.join(TOOLS, "Source")
for dirpath, dirnames, filenames in os.walk(src_root):
    dirnames[:] = [d for d in dirnames if d not in ("extern", "build", ".vs", "out")]
    for fn in filenames:
        if fn.endswith((".pyc",)):
            continue
        full = os.path.join(dirpath, fn)
        rel = "Source/" + os.path.relpath(full, src_root).replace(BS, "/")
        source_files[rel] = read(full)
source_files["Source/BUILD.md"] = read(os.path.join(TOOLS, "BUILD.md"))
assert "Source/src/Camera.cpp" in source_files and "Source/src/plugin.cpp" in source_files

replacements = {
    "Core/SKSE/Plugins/Padborn.dll": dll,
    "Core/README.md": readme,
    "README.md": readme,
    "Config/rescue-off/SKSE/Plugins/Padborn.json": json_off,
    "Config/rescue-on/SKSE/Plugins/Padborn.json": json_on,
    "Layout 402/ControlMap_Custom.txt": binary_map,
    "Layout 402/Interface/controls/pc/controlmap.txt": text_map,
    "fomod/info.xml": info_xml,
    "fomod/ModuleConfig.xml": module_xml,
}
additions = {}
if "Core/SKSE/Plugins/Padborn.pdb" in by_name:
    replacements["Core/SKSE/Plugins/Padborn.pdb"] = pdb  # 3.1.0+ archives already carry it
else:
    additions["Core/SKSE/Plugins/Padborn.pdb"] = pdb

for name in replacements:
    assert name in by_name, f"{name} not in the old archive"

now = time.localtime()[:6]
changed, added, kept, dropped = [], [], [], []

# ---------------------------------------------------------------- write
with zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as new:
    for name, info in entries:
        if name.endswith("/"):
            continue  # directory entries are implied
        if name.startswith("Source/"):
            if name not in source_files:
                dropped.append(name)
            continue  # written from the tree below
        if name in replacements:
            data = replacements[name]
            zi = zipfile.ZipInfo(name, date_time=now)
            zi.compress_type = zipfile.ZIP_DEFLATED
            new.writestr(zi, data)
            changed.append((name, info.file_size, len(data)))
        else:
            data = old.read(info)
            zi = zipfile.ZipInfo(name, date_time=info.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            new.writestr(zi, data)
            kept.append(name)
    for name, data in additions.items():
        zi = zipfile.ZipInfo(name, date_time=now)
        zi.compress_type = zipfile.ZIP_DEFLATED
        new.writestr(zi, data)
        added.append((name, len(data)))
    for name in sorted(source_files):
        data = source_files[name]
        was = by_name.get(name)
        zi = zipfile.ZipInfo(name, date_time=now if (was is None or old.read(was) != data) else was.date_time)
        zi.compress_type = zipfile.ZIP_DEFLATED
        new.writestr(zi, data)
        if was is None:
            added.append((name, len(data)))
        elif old.read(was) != data:
            changed.append((name, was.file_size, len(data)))
        else:
            kept.append(name)
old.close()

bad = zipfile.ZipFile(TMP).testzip()
assert bad is None, f"corrupt entry {bad}"

if not os.path.exists(OLD_KEEP):
    os.rename(OLD, OLD_KEEP)
    print("old archive kept as", os.path.basename(OLD_KEEP))
else:
    os.remove(OLD)
os.rename(TMP, OLD)

print("wrote", OLD, os.path.getsize(OLD), "bytes")
print("changed:")
for n, a, b in changed:
    print(f"  {n}  {a} -> {b}")
print("added:")
for n, b in added:
    print(f"  {n}  {b}")
print("dropped:", dropped)
print("kept verbatim:", len(kept), "entries")
