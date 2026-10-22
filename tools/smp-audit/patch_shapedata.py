"""Durable fix: add / retarget the SMP physics link on the conversion sets' BodySlide
ShapeData nifs, so future batch builds carry it. Backs up each file first (hash-verified)."""
import os, sys, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nif_extradata import add_smp_extradata
from niflib import Nif
import struct

MODS = r"C:\1. AUTHORIA\mods"
BAK = r"C:\1. AUTHORIA\_backups\2026-08-16 - ShapeData before SMP link patch"
SD = r"CalienteTools\BodySlide\ShapeData"
JOBS = [
    (r"Armors of the Velothi Pt. I - HIMBO Refit", r"HIMBO Pulcharmsolis - Head - Velothi Pt. I Indoril Wayfarer\helmet_0.nif", r"meshes\pulcharmsolis\indoril wayfarer\TSXML.xml"),
    (r"Armors of the Velothi Pt. I - HIMBO Refit", r"HIMBO Pulcharmsolis - Head - Velothi Pt. I Indoril Wayfarer Scarf\helmetwithscarfm_0.nif", r"meshes\pulcharmsolis\indoril wayfarer\TSXML.xml"),
    (r"Armors of the Velothi Pt. I - HIMBO Refit", r"HIMBO Pulcharmsolis - Boots - Velothi Pt. I Ashlander Seer\bootsm_0.nif", r"meshes\pulcharmsolis\RedoranExile\REXML.xml"),
    (r"Armors of the Velothi Pt. I - 3BA", r"3BA - Armors of the Velothi 1 - Ashlander Seer\3BA - Armors of the Velothi 1 - Ashlander Seer - boots.nif", r"meshes\pulcharmsolis\RedoranExile\REXML.xml"),
    (r"Armors of the Velothi Pt. II - 3BA", r"3BA - Armors of the Velothi 2 - Ashlander Warrior\3BA - Armors of the Velothi 2 - Ashlander Warrior - body.nif", r"meshes\pulcharmsolis\ashlanderwarrior\data.xml"),
    (r"Armors of the Velothi Pt. II - 3BA", r"3BA - Armors of the Velothi 2 - Camona Tong\3BA - Armors of the Velothi 2 - Camona Tong - gloves.nif", r"meshes\pulcharmsolis\camonnatong\data.xml"),
    (r"Falmer Slayer - UBE Conversion", r"Falmer Slayer Helmet UBE\Falmer Slayer Helmet UBE.nif", r"meshes\falmerslayer\hood.xml"),
    (r"Falmer Slayer - UBE Conversion", r"Falmer Slayer Face Guard UBE\Falmer Slayer Face Guard UBE.nif", r"meshes\falmerslayer\hood.xml"),
    (r"Tullius SMP Wig 3 - 1004 Default Head", r"Tullius SMP Wig 3\Tullius SMP Wig 3 - 532_DOA Tsukushi.nif", r"meshes\00XML\SweetEscapeWig.xml"),
]

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def has_link(path):
    n = Nif(path)
    for i in n.blocks_of('NiStringExtraData'):
        a, b = struct.unpack_from('<II', n.data, n.offsets[i])
        if n.s(a) == 'HDT Skinned Mesh Physics Object':
            return n.s(b)
    return None

for mod, rel, xml in JOBS:
    src = os.path.join(MODS, mod, SD, rel)
    assert os.path.isfile(src), src
    before = has_link(src)
    bak = os.path.join(BAK, mod, SD, rel)
    os.makedirs(os.path.dirname(bak), exist_ok=True)
    shutil.copy2(src, bak)
    assert sha(src) == sha(bak)
    mode = add_smp_extradata(src, src, xml)
    after = has_link(src)
    print('%-42s %-75s before=%s | %s | after=%s' % (mod, rel, before, mode, after))
print('backup:', BAK)
