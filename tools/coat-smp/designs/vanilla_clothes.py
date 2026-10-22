# Authoria (2026-10-18): cloth physics on the long vanilla men's coats (HIMBO Vanilla Armors meshes), coat builder of the
# authoring-smp-armor-physics skill. User: "Build cloth physics for the long men's coats first: fine clothes, belted tunic,
# merchant, the plain clothes, Redguard clothes, blue mage robes. Same look, same method as the robes."
# Men only (the women's 3BA vanilla outfits already carry cloth physics). Sources = the meshes that win in game today
# (HIMBO Vanilla Armors, Common Clothing Retexture for farmerrobe); output = a NEW mod that must outrank them.
# Run:  python rebuild_coat.py <this file> <design> --bodies=m      (build_coat_rig.py <this file> <design> m)
# Runs with build_coat_rig.py's names in scope (PHYS_FLOW, ..., os, np); json imported below.
import json
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
MODS = 'C:/1. AUTHORIA/mods/'
BACKUPS = 'D:/1. MOD STUFF/- ARR STUFF/coat-smp-backups/'
WORK = HERE + 'out/'
PRESET = None
HIMBO = MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors/meshes/clothes/'
TEX_ROOTS = [MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors', MODS + 'Common Clothing Retexture SE']
STAGE_M = HERE + 'stage/m/'
STAGE_F = HERE + 'stage/f/'
STAGE = STAGE_F
MOD_M = MODS + 'Authoria - SMP Vanilla Coats/'
MOD_F = None
XM = 'SKSE\\Plugins\\hdtSkinnedMeshConfigs\\AuthoriaVanillaCoats\\'

# cloth feel: the skill's quilted-cloth FLOW preset, a little lighter like the SoS Hide gambeson (user liked the robes' Helga swing)
PHYS_COAT = dict(PHYS_FLOW, SK_DEF=dict(PHYS_FLOW['SK_DEF'], mass=0.5, lin=0.5, ang=0.5, wind=0.25))

# ---------------------------------------------------------------- clothes/fineclothes02/outfitm (Fine Clothes, Lonely-Gale)
# One shape 'cloth'. comp 0 = the coat: skirt outer island 3598 (1150, waist seam z 75.7-78.1 -> hem 29.4, open at the front
# from z ~56-60 up), lining 3858 (295, inward), hem edge 3599 (129), front-opening facings 6370 / 6372 (82 / 80); bodice 5575 /
# 5503, sleeves 4649 / 4859 hang to z 67.7 (kept by island, not by height). comp 1 = trousers (1224). comp 2 = a pouch on the
# left hip, z 70-80 (static for now). No belt: the skirt is sewn to the bodice at the waist seam.
_FC2_EXPECT = {0: 5104, 1: 1224, 2: 365}

LEGS_ONCE = 0.9      # leg_max_nz: leg faces picked once, on _1 (v1 Fine02 verify: picked per weight, _0 / _1 colliders differed)

# ---------------------------------------------------------------- clothes/fineclothes01/outfitm (Fine Clothes, the long blue-grey coat)
# One shape 'Clothes'. comp 0 = coat sheet chest -> hem 38.6 in ONE piece (front 5582, sides 6450 / 6517, open at the front from z 60
# up), lining 1785 (to z 67) + its top edge 3359, small corner islands at the opening (3206 / 5279 / 3623); sleeves + cuffs at
# x +-25..32 kept out by island. Front buckle 5877 + its 59xx bits z 66.7-77.2 = static. comp 1 = trousers.
_FC1_SKIRT = {5582: 638, 6450: 502, 6517: 499, 1785: 223, 3359: 45, 3206: 15, 5279: 6, 3623: 6}
# ---------------------------------------------------------------- clothes/farmclothes01/torsom (Belted Tunic)
# 'upperbody': comp 0 = tunic; skirt = front 5001 / back 3669 (belt line z 80 -> hem 44.8, sides open from ~55-62); belt band 6258
# (z 77.5-84.7) + buckle comp 2 (lowest 76.6) static. comp 1 = trousers.
# ---------------------------------------------------------------- clothes/merchantclothes/outfitm (Merchant Clothes)
# 'merchanttorso_1': comp 0 = coat front 2330 / back 2325 shoulders -> hem 49, no belt; pouches comp 4 / 5 (z 67-79, right side /
# front right) + back bag comp 3 (z 70.8-83) static -> the skirt swings below them. Trousers = comp 1 + comp 2 (one per leg).
# ---------------------------------------------------------------- clothes/farmclothes02/m/torso (Clothes - the long brown work coat)
# 'BODY': comp 0 = coat 5876 shoulders -> hem 45; belt comp 1 (z 70.8-81), buckle comp 4, pouch comp 5 (right, to z 65.5), bag
# comp 3 (back right, to z 63.5) static -> the skirt swings below the bag. comp 2 = trousers.
# ---------------------------------------------------------------- clothes/farmclothes04/robem (Clothes - the long grey robe)
# 'upperbody': comp 0 = robe front 4585 / back 4517 shoulders -> hem 42, hem bands 2087 / 3324; belt at the front only (comp 1 /
# comp 4, z 71.6-77.7) static. Trousers = comp 2 + comp 3.
# ---------------------------------------------------------------- clothes/farmclothes03/farmerrobe (Clothes - farmer robe; Common
# Clothing Retexture wins) - low-poly: 'robemorph' comp 0 = top 967 / skirt 266 + 934 / 935 / 855 (z 43.6-77.6); belt band 731
# (z 75.1-83.2) + buckle comps 3 / 4 static. Trousers = their own shape 'Pants' (both legs).

# v2: + the 15 six-point gusset islands inside the skirt top (z 64-71, welded to it; left on the body they made a seam that welded
# differently on _0 and _1)
_TUNIC_SKIRT = dict({5001: 991, 3669: 360}, **{})
_TUNIC_SKIRT.update({i: 6 for i in (3848, 1552, 1565, 4136, 4396, 1970, 1981, 4547, 4556, 2253, 2262, 3436, 2679, 3449, 2684)})
# ---------------------------------------------------------------- round 2 (user 10-18: "I want all the long clothes to have smp")
# island lists from pick_islands.py (every island of the coat component reaching below the cut, sleeves / cuffs left out by width)
ISL = {k: {int(i): n for i, n in v.items()} for k, v in json.load(open(HERE + 'islands.json')).items()}
DLC = MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors/meshes/'
PBR_DONORS = 'C:/1. AUTHORIA/_tools/coat-smp/pbr_donors/'      # frozen copies of the PG-patched emperor / jarl meshes (shaders only)
CCR = MODS + 'Common Clothing Retexture SE/meshes/clothes/'


def _coat(prefix, title, src, out, xml, shape, sel, expect, pants_comp, belt, pants=None, **extra):
    """one coat: the skirt cut from `shape` by `sel`, hinged 2 under its top at belt + 2 (belt = the lowest rigid edge over it)"""
    return dict(prefix=prefix, title=title, phys=PHYS_COAT, bag=False, tip_collide=False, tip_legs=(),
                gap=(0.0, 1.5), free_max=0.85,
                m=dict(src=src, out=STAGE_M + out, stage=STAGE_M, xml=XM + xml,
                       pieces=[('Saia', shape, sel, 'skirt:outer')],
                       expect=expect, static=(shape,), pants=pants or shape, pants_comp=pants_comp, drop=(),
                       subdiv=('Saia',), slits=True, sk_belt=belt, sk_anchor=belt + 2.0, ramp=8.0, leg_max_nz=LEGS_ONCE,
                       # v2 (lining check: 500-940 lining pts through the sheet on the jarl coats): the hidden lining takes the
                       # sheet's weights where it lies under it, the field is interpolated, two chain bones survive the 4-cap
                       lining_ride=True, field_interp=2.0, cap_pelvis_min=0.05, **extra))


DESIGNS = {
    'Fine02': dict(
        prefix='AFC2', title='Fine Clothes (clothes/fineclothes02)',
        phys=PHYS_COAT, bag=False, tip_collide=False, tip_legs=(),
        gap=(0.0, 1.5), free_max=0.85,
        m=dict(src=HIMBO + 'fineclothes02/outfitm_{}.nif',
               out=STAGE_M + 'meshes/clothes/fineclothes02/outfitm_{}.nif', stage=STAGE_M,
               xml=XM + 'FineClothes02M.xml',
               pieces=[('Saia', 'cloth', ('islands', 0, {3598: 1150, 3858: 295, 3599: 129, 6370: 82, 6372: 80}, ()), 'skirt:outer')],
               expect=_FC2_EXPECT, static=('cloth',), pants='cloth', pants_comp=1, drop=(),
               subdiv=('Saia',), slits=True, sk_belt=75.5, sk_anchor=77.5, ramp=8.0,
               # v1 verify: the leg faces were picked by height per weight (_0 / _1 colliders differed) - leg_max_nz makes the
               # pick once, on _1, and keeps knee tops from pushing the hem up
               leg_max_nz=0.9, lining_ride=True, field_interp=2.0, cap_pelvis_min=0.05),
    ),
    'Fine01': _coat('AFC1', 'Fine Clothes (clothes/fineclothes01)', HIMBO + 'fineclothes01/outfitm_{}.nif',
                    'meshes/clothes/fineclothes01/outfitm_{}.nif', 'FineClothes01M.xml', 'Clothes',
                    ('islands', 0, _FC1_SKIRT, (), 72.0), {0: 4616, 1: 1203}, 1, 66.5),
    'Tunic': _coat('AFT1', 'Belted Tunic (clothes/farmclothes01)', HIMBO + 'farmclothes01/torsom_{}.nif',
                   'meshes/clothes/farmclothes01/torsom_{}.nif', 'BeltedTunicM.xml', 'upperbody',
                   ('islands', 0, _TUNIC_SKIRT, (), 79.0), {0: 4863, 1: 1125, 2: 416}, 1, 76.5),
    'Merchant': _coat('AMC', 'Merchant Clothes (clothes/merchantclothes)', HIMBO + 'merchantclothes/outfitm_{}.nif',
                      'meshes/clothes/merchantclothes/outfitm_{}.nif', 'MerchantClothesM.xml', 'merchanttorso_1',
                      ('islands', 0, {2330: 1460, 2325: 519}, (), 72.0), {0: 2847, 1: 356, 2: 356}, (1, 2), 67.0),
    'Farm02': _coat('AFM2', 'Clothes (clothes/farmclothes02)', HIMBO + 'farmclothes02/m/torso_{}.nif',
                    'meshes/clothes/farmclothes02/m/torso_{}.nif', 'FarmClothes02M.xml', 'BODY',
                    ('islands', 0, {5876: 2736}, (), 72.0), {0: 4198, 1: 1038, 2: 806, 3: 472}, 2, 63.5),
    'Farm04': _coat('AFM4', 'Clothes (clothes/farmclothes04)', HIMBO + 'farmclothes04/robem_{}.nif',
                    'meshes/clothes/farmclothes04/robem_{}.nif', 'FarmClothes04M.xml', 'upperbody',
                    ('islands', 0, {4585: 1549, 4517: 776, 2087: 75, 3324: 61}, (), 76.0), {0: 3913, 2: 425, 3: 425}, (2, 3), 71.5),
    'Farm03': _coat('AFM3', 'Clothes (clothes/farmclothes03 farmer robe)', CCR + 'farmclothes03/farmerrobe_{}.nif',
                    'meshes/clothes/farmclothes03/farmerrobe_{}.nif', 'FarmClothes03M.xml', 'robemorph',
                    ('islands', 0, {266: 120, 934: 78, 935: 57, 855: 37}, ()), {0: 651}, None, 74.0, pants='Pants'),
    # ---- round 2: same meshes as round 1 under other paths
    'Wedding': _coat('AFCW', 'Wedding Clothes (clothes/fineclothes01/weddingoutfitm)', HIMBO + 'fineclothes01/weddingoutfitm_{}.nif',
                     'meshes/clothes/fineclothes01/weddingoutfitm_{}.nif', 'WeddingClothesM.xml', 'Clothes',
                     ('islands', 0, _FC1_SKIRT, (), 72.0), {0: 4616, 1: 1203}, 1, 66.5),
    'Wench': _coat('AWN', 'Tavern Clothes (clothes/wench)', HIMBO + 'wench/wenchoutfitm_{}.nif',
                   'meshes/clothes/wench/wenchoutfitm_{}.nif', 'WenchOutfitM.xml', 'merchanttorso_1',
                   ('islands', 0, {2330: 1460, 2325: 519}, (), 72.0), {0: 2848, 1: 356, 2: 356}, (1, 2), 67.0),
    'Farm03x': _coat('AFM3X', 'Clothes, hooded (clothes/farmclothes03 farmer03mextras)', CCR + 'farmclothes03/farmer03mextras_{}.nif',
                     'meshes/clothes/farmclothes03/farmer03mextras_{}.nif', 'FarmClothes03xM.xml', 'robemorph',
                     ('islands', 0, {266: 120, 934: 78, 935: 57, 855: 37}, ()), {0: 651}, None, 74.0, pants='Pants',
                     hem_clear=dict(clear=1.5, full=46.0, top=54.0)),   # v1-3: 2-5 _0 back pts at z 46-48 rested on the legs (gap / pull did not clear them) -> hem eased off
    # ---- round 2: new coats over trousers
    # beggar: one ragged shirt to z 32-41, no belt; trousers = shape 'rags'
    'Beggar': _coat('ABG', 'Beggar Clothes (clothes/beggarclothes)', HIMBO + 'beggarclothes/torsom_{}.nif',
                    'meshes/clothes/beggarclothes/torsom_{}.nif', 'BeggarClothesM.xml', 'BeggarModel',
                    ('below', 0, 76.0), {0: 3080}, None, 72.0, pants='rags',
                    lining_min_gap=0.9),     # v1: 3 side pts by the knees rested on the legs
    # blacksmith: apron + shirt island 2047 (front to 43, back to 52); belt comp 2 (z 74.7-81); pouch comp 3 hangs to 62.4 front
    # left -> the apron swings below it. comp 1 = trousers
    'Smith': _coat('ABS', 'Blacksmith Apron (clothes/blacksmith)', HIMBO + 'blacksmith/m/torso_{}.nif',
                   'meshes/clothes/blacksmith/m/torso_{}.nif', 'BlacksmithM.xml', 'TorsoRig',
                   ('islands', 0, {2047: 4149}, (), 76.0), {0: 5036, 1: 1170, 2: 825}, 1, 62.0),
    # jester: front 5807 / back 1797 to z 40, band 5737 (z 63-74) + buckle comp 3 + pouch comp 2 (to 59) static; comp 1 trousers
    'Jester': _coat('AJS', 'Jester Clothes (clothes/jester)', HIMBO + 'jester/jesterm_{}.nif',
                    'meshes/clothes/jester/jesterm_{}.nif', 'JesterM.xml', 'JesterBody',
                    ('islands', 0, {5807: 2042, 1797: 860}, (), 70.0), {0: 4882, 1: 1234}, 1, 61.0),
    # vampire clothes (Dawnguard): skirt 4063 / hem 4775 / lining 1252 + 1234 (z 43-78), front belt comps 1 / 2 static;
    # the legs are the HIMBO body drawn in the mesh (shape 'HIMBO - Body' comp 0)
    'VampClothes': _coat('AVC', 'Vampire Clothes (dlc01/clothes/vampclothes)', DLC + 'dlc01/clothes/vampclothes/vampclothesm_{}.nif',
                         'meshes/dlc01/clothes/vampclothes/vampclothesm_{}.nif', 'VampClothesM.xml', 'robemorph',
                         ('islands', 0, {4063: 877, 4775: 302, 1252: 198, 1234: 108}, ()), {0: 4136}, 0, 74.0, pants='HIMBO - Body'),
    # jarl / emperor coat (low-poly Common Clothing Retexture meshes - they outrank HIMBO; the PG PBR copy of them wins in game): coat below the belt, belt bits comps 6 / 7 (z 72-82);
    # trousers comps 3 + 4; the shader comes from the frozen PBR copy (this mod outranks the PG output)
    'Emperor': _coat('AEM', 'Emperor Clothes (clothes/emperor)', CCR + 'emperor/emperoroutfitm_{}.nif',
                     'meshes/clothes/emperor/emperoroutfitm_{}.nif', 'EmperorM.xml', 'Torso',
                     ('below', 0, 76.0), {0: 1077, 3: 88, 4: 88}, (3, 4), 72.0, shader_donor=PBR_DONORS + 'emperor/emperoroutfitm_1.nif'),
    'Jarl1': _coat('AJ1', 'Jarl Clothes (clothes/yarlclothes torso)', CCR + 'yarlclothes/m/torso_{}.nif',
                   'meshes/clothes/yarlclothes/m/torso_{}.nif', 'Jarl1M.xml', 'Torso',
                   ('below', 0, 76.0), {0: 1077, 3: 88, 4: 88}, (3, 4), 72.0, shader_donor=PBR_DONORS + 'yarlclothes/m/torso_1.nif'),
    'Jarl1v1': _coat('AJ1A', 'Jarl Clothes (clothes/yarlclothes torso_var1)', CCR + 'yarlclothes/m/torso_var1_{}.nif',
                     'meshes/clothes/yarlclothes/m/torso_var1_{}.nif', 'Jarl1Var1M.xml', 'Torso',
                     ('below', 0, 76.0), {0: 1077, 3: 88, 4: 88}, (3, 4), 72.0, shader_donor=PBR_DONORS + 'yarlclothes/m/torso_var1_1.nif'),
    'Jarl1v2': _coat('AJ1B', 'Jarl Clothes (clothes/yarlclothes torso_var2)', CCR + 'yarlclothes/m/torso_var2_{}.nif',
                     'meshes/clothes/yarlclothes/m/torso_var2_{}.nif', 'Jarl1Var2M.xml', 'Torso',
                     ('below', 0, 76.0), {0: 1077, 3: 88, 4: 88}, (3, 4), 72.0, shader_donor=PBR_DONORS + 'yarlclothes/m/torso_var2_1.nif'),
    # jarl coat 03: long coat to z 24, buttons / buckles comps 3-6 ride it; trousers = shape 'YarlPants'
    'Jarl3': _coat('AJ3', 'Jarl Clothes (clothes/yarlclothes03)', HIMBO + 'yarlclothes03/outfitm_{}.nif',
                   'meshes/clothes/yarlclothes03/outfitm_{}.nif', 'Jarl3M.xml', 'YarlClothes03_Cloth',
                   ('islands', 0, ISL['yarl03'], (3, 4, 5, 6), 72.0), {0: 7463}, None, 64.0, pants='YarlPants'),
    'Jarl3v1': _coat('AJ3A', 'Jarl Clothes (clothes/yarlclothes03 var1)', HIMBO + 'yarlclothes03/outfitm_var1_{}.nif',
                     'meshes/clothes/yarlclothes03/outfitm_var1_{}.nif', 'Jarl3Var1M.xml', 'YarlClothes03_Cloth',
                     ('islands', 0, ISL['yarl03'], (3, 4, 5, 6), 72.0), {0: 7463}, None, 64.0, pants='YarlPants'),
    # jarl coat 02 + Ulfric: an inner coat (comp 0) under an open outer coat (comp 1) on ONE rig; sash comp 3 (z 66-79) static;
    # comp 2 = trousers
    'Jarl2': _coat('AJ2', 'Jarl Clothes (clothes/yarlclothes02)', HIMBO + 'yarlclothes02/outfitm_{}.nif',
                   'meshes/clothes/yarlclothes02/outfitm_{}.nif', 'Jarl2M.xml', 'Clothes',
                   ('islands', 0, ISL['yarl02_0'], (1,), 76.0), {0: 6191, 1: 3922, 2: 1209, 3: 908}, 2, 66.0),
    'Ulfric': _coat('AUL', 'Ulfric Clothes (clothes/yarlclothes02/ulfric)', HIMBO + 'yarlclothes02/ulfric_{}.nif',
                    'meshes/clothes/yarlclothes02/ulfric_{}.nif', 'UlfricM.xml', 'ClothesREVISED',
                    ('islands', 0, ISL['ulfric_0'], (1,), 76.0), {0: 7241, 1: 3937, 2: 1156, 3: 878}, 2, 66.0),
    # Dark Brotherhood robes: tunic islands to z 41 + the sash comp 5 (z 55-82) riding it; belt comps 3 / 4; comp 1 trousers
    'DarkBro': _coat('ADB', 'Dark Brotherhood Robes (clothes/robedarkbrotherhood)', HIMBO + 'robedarkbrotherhood/dbtorso_{}.nif',
                     'meshes/clothes/robedarkbrotherhood/dbtorso_{}.nif', 'DarkBrotherhoodM.xml', 'DBbody3rdPerson',
                     ('islands', 0, ISL['db'], (5,), 76.0), {0: 5215, 1: 1304, 5: 482}, 1, 75.0),
}
