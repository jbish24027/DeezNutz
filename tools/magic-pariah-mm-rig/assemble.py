"""Assemble the MO2 mod folder 'Magic Pariah - Meadowlark Physics'."""
import os, re, shutil, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from graft import SP, OUT_NIF, OUT_DIR, PROXY_NAME

SRC = SP + r"\mp\Magic Pariah"
MOD = r"C:\1. AUTHORIA\mods\Magic Pariah - Meadowlark Physics"
SKIRT_OSP = r"CalienteTools\BodySlide\SliderSets\Magic Pariah Skirt HDT.osp"
SKIRT_NIF = r"CalienteTools\BodySlide\ShapeData\Magic Pariah Skirt HDT\Magic Pariah Skirt HDT.nif"
XML_DST = r"meshes\clothes\magic pariah\MagicPariahSkirtHDT.xml"
SKIP = {r"meshes\clothes\magic pariah\MagicPariahSkirtHDT backup.xml"}

if os.path.isdir(MOD):
    shutil.rmtree(MOD)
copied = 0
for root, dirs, files in os.walk(SRC):
    for f in files:
        src = os.path.join(root, f)
        rel = os.path.relpath(src, SRC)
        if rel in SKIP:
            continue
        dst = os.path.join(MOD, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst); copied += 1
print('copied', copied, 'files from the Magic Pariah archive')

# grafted skirt mesh
shutil.copy2(OUT_NIF, os.path.join(MOD, SKIRT_NIF))
# new physics xml
shutil.copy2(os.path.join(OUT_DIR, 'MagicPariahSkirtHDT.xml'), os.path.join(MOD, XML_DST))

# skirt BodySlide project: drop Cube/UniButt, add the three proxy shapes
p = os.path.join(MOD, SKIRT_OSP)
raw = open(p, 'rb').read()
crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.split('\r\n' if crlf else '\n')
out = []; dropped = 0
for ln in lines:
    if re.search(r'target="(Cube|UniButt)"', ln):
        dropped += 1; continue
    out.append(ln)
    if '<Shape target="SASH_2">' in ln:
        indent = ln[:len(ln) - len(ln.lstrip())]
        for n in ('CollCalves', 'CollThigh', PROXY_NAME):
            out.append('%s<Shape target="%s">%s</Shape>' % (indent, n, n))
new = ('\r\n' if crlf else '\n').join(out)
open(p, 'wb').write(('\ufeff' + new).encode('utf-8') if text != raw.decode('utf-8') else new.encode('utf-8'))
print('osp: dropped %d Cube/UniButt lines, added 3 proxy shapes, crlf=%s' % (dropped, crlf))
shapes = re.findall(r'<Shape target="([^"]+)"', new)
print('osp shapes now:', shapes)

# notes file
notes = """Magic Pariah - Meadowlark Physics
=================================
Magic Pariah Fit (Nexus 155585, blickRARRI, v1.0) with the skirt physics rig of
Meandering Meadowlark (Nexus 181245, same author, v1.101) grafted onto the skirt.
Built 2026-09-03 with C:\\1. AUTHORIA\\_tools\\magic-pariah-mm-rig\\ (graft.py, make_xml.py).

Top, hat, boots, textures, ESP: unchanged from the Magic Pariah archive.
(The hat xml was already identical between the two mods.)

Skirt (CalienteTools\\BodySlide\\ShapeData\\Magic Pariah Skirt HDT\\Magic Pariah Skirt HDT.nif):
  - Meadowlark's 12-column skirt bone chain, rows 1-4, under NPC Pelvis
  - Meadowlark's CollThigh + CollCalves leg colliders (partition slot 49)
  - Meadowlark's invisible skirt collision proxy, cut just below the knee-length hem,
    renamed MMSkirtProxy
  - Skirt Lower / Skirt Upper re-skinned to the new chain (weights transferred from
    Meadowlark's own skirt layers by nearest neighbour); positions/UVs/triangles untouched,
    so the .osd slider data still applies
  - removed: the old 8-column chain, the rigid 'Cube' hip collider, and the duplicate
    'UniButt' 3BA body that shipped inside the skirt (the top already carries the body)
meshes\\clothes\\magic pariah\\MagicPariahSkirtHDT.xml: Meadowlark's MMDress.xml numbers,
  rows 1-4, without the dress-only dangles/feet collider; two MM typos fixed.

Build the outfit in BodySlide like the original (no prebuilt meshes ship).
"""
open(os.path.join(MOD, '_Meadowlark Physics graft.txt'), 'w', encoding='utf-8', newline='\r\n').write(notes)

# manifest
for root, dirs, files in os.walk(MOD):
    for f in files:
        fp = os.path.join(root, f)
        print('%10d  %s' % (os.path.getsize(fp), os.path.relpath(fp, MOD)))
