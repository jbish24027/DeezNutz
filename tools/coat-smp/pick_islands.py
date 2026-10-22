"""Island lists for the skirt pieces: every texture island of a component that reaches below zcut and stays within |x| <= xmax
(sleeves / cuffs hang wider and are left out). Writes designs/islands.json {key: {island id: size}}."""
import sys, json
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\skill\scripts")
import smpkit
C = smpkit.init()
from coat.build_coat_rig import islands

M = "C:/1. AUTHORIA/mods/Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors/meshes/"
SPECS = {
    'greybeard': (M + 'clothes/graybeardrobe/greybeardrobe_1.nif', 'RobeDoubled3rdPerson', 0, 76, 22),
    'yarl03': (M + 'clothes/yarlclothes03/outfitm_1.nif', 'YarlClothes03_Cloth', 0, 72, 21),
    'temple': (M + 'dlc02/clothes/temple/templetorso_1.nif', 'FinalCoat', 0, 70, 27.5),
    'mythic': (M + 'clothes/robemythicdawn/mdrobe_1.nif', 'Mythic_Dawn_Outfit_body', 0, 76, 25),
    'thalmor': (M + 'clothes/thalmor/thalmorrobesm_1.nif', 'ThalmorRobes', 0, 74, 21),
    'db': (M + 'clothes/robedarkbrotherhood/dbtorso_1.nif', 'DBbody3rdPerson', 0, 76, 19),
    'exec': (M + 'clothes/executioner/body_1.nif', 'torsor', 0, 76, 17),
    'yarl02_0': (M + 'clothes/yarlclothes02/outfitm_1.nif', 'Clothes', 0, 76, 22.5),
    'yarl02_1': (M + 'clothes/yarlclothes02/outfitm_1.nif', 'Clothes', 1, 76, 22.5),
    'ulfric_0': (M + 'clothes/yarlclothes02/ulfric_1.nif', 'ClothesREVISED', 0, 76, 22.5),
    'ulfric_1': (M + 'clothes/yarlclothes02/ulfric_1.nif', 'ClothesREVISED', 1, 76, 22.5),
    'telvanni': (M + 'dlc02/clothes/telvanni/telvannibodym_1.nif', 'TelvanniBody', 0, 69, 25),
    'darkelf': (M + 'dlc02/clothes/darkelf/m/outfit_1.nif', 'Dark_Elf_Outfit_male_robe_1', 0, 78, 17),
    'psijic': (M + 'clothes/psiijic/psiijicrobesm_1.nif', 'PsiijicRobes', 0, 76, 25),
}
out = {}
for k, (src, shape, comp, zcut, xmax) in SPECS.items():
    n, T = C.load(src); C.to_world(T)
    t = next(x for x in T if x.name == shape)
    lab = C.welded_components(t.pos, t.tris); isl = islands(t.tris, len(t.pos))
    d = {}
    for r in sorted(set(isl[lab == comp].tolist())):
        m = (isl == r) & (lab == comp); q = t.pos[m]
        if q[:, 2].min() < zcut and np.abs(q[:, 0]).max() <= xmax:
            d[int(r)] = int(m.sum())
    out[k] = d
    print(k, len(d), 'islands', sum(d.values()), 'pts')
json.dump(out, open(r"C:\1. AUTHORIA\_tools\coat-smp\designs\islands.json", "w"), indent=0)
