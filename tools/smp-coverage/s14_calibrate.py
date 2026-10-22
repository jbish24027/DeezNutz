"""Calibrate the hairstyle similarity on known pairs."""
import sys, os
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\smp-coverage")
sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad")
import hairgraft, nifrw, hairgeo, bsareader
inst = r"C:\1. AUTHORIA"
tmp = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8714b13a-8cba-4f6e-a284-eaf1cd40c73c\scratchpad\graft_tmp"
b = bsareader.BSA(inst + r"\Stock Game\Data\Skyrim - Meshes0.bsa")

def from_bsa(key):
    p = os.path.join(tmp, "cal_" + os.path.basename(key))
    open(p, "wb").write(b.read(key)); return p

def shape_pos(path, name=None):
    d = nifrw.Doc(path)
    best = None
    for i in hairgraft.shapes(d):
        if name is None or d.name_of(i) == name:
            return hairgeo.head_space(hairgeo.positions(d, i), d), d.name_of(i)
        if name and name.lower() in (d.name_of(i) or "").lower():
            best = i
    if best is not None:
        return hairgeo.head_space(hairgeo.positions(d, best), d), d.name_of(best)
    raise KeyError((name, [d.name_of(i) for i in hairgraft.shapes(d)]))

vhr = inst + r"\mods\Vanilla hair remake SMP\meshes\actors\character\character assets\hair\male\%s.nif"
vhrf = inst + r"\mods\Vanilla hair remake SMP\meshes\actors\character\character assets\hair\female\%s.nif"
cases = [
    ("vanilla static male hair01 vs VHR hair01 (SAME)", shape_pos(from_bsa("meshes\\actors\\character\\character assets\\hair\\male\\hair01.nif")), shape_pos(vhr % "hair01")),
    ("vanilla static male hair01 vs VHR hair10 (DIFF)", shape_pos(from_bsa("meshes\\actors\\character\\character assets\\hair\\male\\hair01.nif")), shape_pos(vhr % "hair10")),
    ("vanilla static male hair10 vs VHR hair10 (SAME)", shape_pos(from_bsa("meshes\\actors\\character\\character assets\\hair\\male\\hair10.nif")), shape_pos(vhr % "hair10")),
    ("vanilla static female hair03 vs VHR f hair03 (SAME)", shape_pos(from_bsa("meshes\\actors\\character\\character assets\\hair\\female\\hair03.nif")), shape_pos(vhrf % "hair03")),
    ("vanilla static female hair03 vs VHR f hair15 (DIFF)", shape_pos(from_bsa("meshes\\actors\\character\\character assets\\hair\\female\\hair03.nif")), shape_pos(vhrf % "hair15")),
    ("Rikke BAKE hair vs VHR f hair03 (SAME)", shape_pos(from_bsa("meshes\\actors\\character\\facegendata\\facegeom\\skyrim.esm\\000132a1.nif"), "HairFemaleNord03"), shape_pos(vhrf % "hair03")),
    ("Tolfdir BAKE 0Hair4 vs VHR hair01 (?)", shape_pos(inst + r"\mods\True Sons of Skyrim Refined\meshes\actors\character\facegendata\facegeom\Skyrim.esm\0001C19E.nif", "0Hair4"), shape_pos(vhr % "hair01")),
    ("Belethor BAKE vs VHR hair01 (?)", shape_pos(inst + r"\mods\Men of Skyrim Refined\meshes\actors\character\facegendata\facegeom\Skyrim.esm\00013BA1.nif", "0Hair3"), shape_pos(vhr % "hair01")),
    ("Farengar BAKE 0HairHL (phys, hair10) vs VHR hair10 (SAME)", shape_pos(inst + r"\mods\True Sons of Skyrim Refined\meshes\actors\character\facegendata\facegeom\Skyrim.esm\00013BBB.nif", "0HairHL"), shape_pos(vhr % "hair10")),
]
for cell in (1.0,):
    print("--- cell", cell)
    for label, (pa, na), (pb, nb) in cases:
        iou, ca, cb, ba, bb = hairgeo.similarity(pa, pb, cell)
        print("%-60s iou %.2f  covA %.2f covB %.2f | A %s..%s | B %s..%s" % (label, iou, ca, cb,
              tuple(round(v) for v in ba[0]), tuple(round(v) for v in ba[1]), tuple(round(v) for v in bb[0]), tuple(round(v) for v in bb[1])))
