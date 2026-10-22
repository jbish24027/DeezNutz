"""Writes one skirt-builder design file per long robe / apron (build_skirt_rig.py takes one DESIGN per file), all from the
recipe proven on the Blue Mage Robes (monk_robes.py) and the Redguard back panel (redguard_robe.py). Round 2, 2026-10-18
(user: 'I want all the long clothes to have smp'). Run once after editing ROBES; then skill/scripts/rebuild.py <file>."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
ISL = {k: {int(i): n for i, n in v.items()} for k, v in json.load(open(HERE + 'islands.json')).items()}
H = 'C:/1. AUTHORIA/mods/Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors/meshes/'
BODY = "dict(nif='C:/1. AUTHORIA/mods/Highly Improved Male Body Overhaul -HIMBO-/meshes/actors/character/character assets/malebody_{}.nif', shape='HIMBO - Body HP')"
FLOOR = dict(nrow=7, panels=2, ground_z=-1.5, row_margin=[1, 1, 1.5, 2, 2.5, 3, 3])
ONE_SIDE = dict(slits=True, slit_max_hw=170.0)

# name: (prefix, title, mesh path under meshes/ ({} = weight), shape, selector, legs, sk_belt, expect, extra target keys, extra design keys)
ROBES = {
    'MonkRobes2': ('AMR2', 'Monk Robes (clothes/monk/monkrobes)', 'clothes/monk/monkrobes_{}.nif', 'robes',
                   ('islands', 0, {4120: 2187, 1838: 801, 1219: 58}, (), 76.0), 'body', 72.0, {0: 4074, 1: 345, 2: 309},
                   dict(FLOOR), dict(lining_all=True), (1, 2, 3, 4, 5, 6)),
    'Vaermina': ('AVR', 'Vaermina Robes (clothes/monk/vaerminarobes)', 'clothes/monk/vaerminarobes_{}.nif', 'robes',
                 ('islands', 0, {4120: 2187, 1838: 801, 1219: 58}, (), 76.0), 'body', 72.0, {0: 4074, 1: 345, 2: 309},
                 dict(FLOOR), dict(lining_all=True), (1, 2, 3, 4, 5, 6)),
    'BlindMoth': ('ABM', 'Moth Priest Robes (dlc01/clothes/blindmothpriest)', 'dlc01/clothes/blindmothpriest/blindmothpriestrobesm_{}.nif', 'robes',
                  ('islands', 0, {4120: 2187, 1838: 801, 1219: 58}, (), 76.0), 'body', 72.0, {0: 4074, 1: 345, 2: 309},
                  dict(FLOOR), dict(lining_all=True), (1, 2, 3, 4, 5, 6)),
    # Greybeard: one doubled robe to the floor, long sleeves hanging to z 54 (left out by width); no belt
    'Greybeard': ('AGB', 'Greybeard Robes (clothes/graybeardrobe)', 'clothes/graybeardrobe/greybeardrobe_{}.nif', 'RobeDoubled3rdPerson',
                  ('islands', 0, ISL['greybeard'], (), 76.0), 'body', 72.0, {0: 12265}, dict(FLOOR), {}, ()),
    # Mythic Dawn: robe to the floor at the back, z 30 at the front; sleeves / cuffs left out by width
    'MythicDawn': ('AMD', 'Mythic Dawn Robes (clothes/robemythicdawn)', 'clothes/robemythicdawn/mdrobe_{}.nif', 'Mythic_Dawn_Outfit_body',
                   ('islands', 0, ISL['mythic'], (), 76.0), 'body', 72.0, {0: 5841}, dict(FLOOR, slits=True), {}, ()),
    # Psijic: front panels (comp 0) + back panel comp 1 + the front sash comp 3 ride one rig; belt comp 2 (z 70-83)
    'Psijic': ('APS', 'Psijic Robes (clothes/psiijic)', 'clothes/psiijic/psiijicrobesm_{}.nif', 'PsiijicRobes',
               ('islands', 0, ISL['psijic'], (1, 3), 76.0), 'body', 70.0, {0: 5662, 1: 1088, 2: 721, 3: 221}, dict(FLOOR, slits=True), {}, ()),
    # Thalmor: robe to the floor over the trousers comp 1; buckle at z 71-75
    'Thalmor': ('ATH', 'Thalmor Robes (clothes/thalmor)', 'clothes/thalmor/thalmorrobesm_{}.nif', 'ThalmorRobes',
                ('islands', 0, {k: v for k, v in ISL['thalmor'].items() if k not in (2759, 2760)}, (), 74.0), ('ThalmorRobes', (1,)), 71.0,
                {0: 4188, 1: 859}, dict(FLOOR, slits=True), {}, ('islands', 0, {2759: 123, 2760: 51}, (), 74.0)),
    # (v2: the front tabard 2759 / 2760 hanging between the legs tore into shards on the kick render - mixed leg / chain weights;
    #  it hangs on its own hinge now, a 'pendant')
    # Cultist (Dragonborn): the long doubled skirt comp 1 + the tunic over it (comp 0 islands 9880 / 3107) on one rig;
    # belt bits comps 3-8 (z 69-82); trousers comp 2
    'Cultist': ('ACU', 'Cultist Robes (dlc02/clothes/cultist)', 'dlc02/clothes/cultist/m/cultisttorso_{}.nif', 'TorsoNew',
                ('islands', 0, {9880: 2691, 3107: 99}, (1,), 74.0), ('TorsoNew', (2,)), 69.0, {0: 7750, 1: 2198, 2: 695}, dict(FLOOR, slits=True), {}, ()),
    # Dark Elf clothes (Dragonborn): front tunic to z 48 + the long back panel comp 1 (to z 9)
    'DarkElf': ('ADE', 'Dark Elf Clothes (dlc02/clothes/darkelf)', 'dlc02/clothes/darkelf/m/outfit_{}.nif', 'Dark_Elf_Outfit_male_robe_1',
                ('islands', 0, ISL['darkelf'], (1,), 78.0), 'body', 74.0, {0: 8406, 1: 1790}, dict(FLOOR, slits=True), {}, ()),
    # Telvanni robes: the paneled skirt (comp 0 panels + comps 1 / 2) under the waist sash 12682 (z 66-83)
    'Telvanni': ('ATV', 'Telvanni Robes (dlc02/clothes/telvanni)', 'dlc02/clothes/telvanni/telvannibodym_{}.nif', 'TelvanniBody',
                 ('islands', 0, ISL['telvanni'], (1, 2), 69.0), 'body', 66.0, {0: 11017, 1: 1046, 2: 980}, dict(FLOOR, slits=True), {}, ()),
    # Temple priest (Dragonborn): the coat (comp 0) + its side panels comps 1 / 2 + the back panel comp 3, below the waist
    'Temple': ('ATP', 'Temple Priest Robes (dlc02/clothes/temple)', 'dlc02/clothes/temple/templetorso_{}.nif', 'FinalCoat',
               ('islands', 0, ISL['temple'], (1, 2, 3), 70.0), 'body', 67.0, {0: 8000, 1: 1320, 2: 1296, 3: 1239}, dict(FLOOR, slits=True), {}, ()),
    # Executioner / reaper: hood-robe to z 19; pouch comp 1 rides it; the legs are the HIMBO body drawn in the mesh
    'Executioner': ('AEX', 'Executioner Robes (clothes/executioner)', 'clothes/executioner/body_{}.nif', 'torsor',
                    ('islands', 0, ISL['exec'], (1,), 76.0), ('HIMBO - Body', (0,)), 72.0, {0: 4634, 1: 182},
                    dict(nrow=6, panels=2, row_margin=[1, 1, 1.5, 2, 2.5, 3], slits=True), {}, ()),
    # Barkeeper / chef: a FRONT apron below the band 10573 (z 62-74) - one-sided panel on the body's axis
    'Barkeeper': ('ABK', 'Barkeeper Clothes (clothes/barkeeper)', 'clothes/barkeeper/m/torso_{}.nif', 'BarkeepBody',
                  ('islands', 0, {5290: 3726, 5468: 167}, (), 62.5), ('BarkeepBody', (1,)), 60.5, {0: 7837, 1: 1794},
                  dict(ONE_SIDE, axis_xy=(0.0, 2.0), nrow=4, pants_zmax=80.0, leg_zmin=-10.0), {}, ()),
    'Chef': ('ACF', 'Chef Clothes (clothes/chef)', 'clothes/chef/m/chef_{}.nif', 'BarkeepBody',
             ('islands', 0, {5290: 3726, 5468: 167}, (), 62.5), ('BarkeepBody', (1,)), 60.5, {0: 7837, 1: 1794},
             dict(ONE_SIDE, axis_xy=(0.0, 2.0), nrow=4, pants_zmax=80.0, leg_zmin=-10.0), {}, ()),
}

TEMPLATE = '''# GENERATED by make_robe_designs.py (2026-10-18) - edit ROBES there, not here.
MODS = 'C:/1. AUTHORIA/mods/'
WORK = 'C:/1. AUTHORIA/_tools/coat-smp/designs/out/'
STAGE = 'C:/1. AUTHORIA/_tools/coat-smp/designs/stage/m'
XM = 'SKSE\\\\Plugins\\\\hdtSkinnedMeshConfigs\\\\AuthoriaVanillaCoats\\\\'
DESIGN = dict(
    name={name!r}, prefix={prefix!r}, title={title!r},
    stage=STAGE, work=WORK, phys='cloth',
    tex_roots=[MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors'],
    install=MODS + 'Authoria - SMP Vanilla Coats', backups='D:/1. MOD STUFF/- ARR STUFF/coat-smp-backups',
    max_chains=12, chain_spacing=30.0, leg_zmin={leg_zmin},
    pendant_share=0.8,
    pendant_def=dict(mass=0.35, inertia=4.5, lin=0.45, ang=0.45, friction=0.0, wind=0.0),
    pendant_lim=dict(lo=(-0.35, -0.25, -0.2), hi=(0.0, 0.25, 0.2), lin=0.0, astiff=14),
{dkeys}    targets=dict(m=dict(
        mode='nif', src={src!r}, out={out!r}, xml=XM + {xml!r},
        pieces={pieces!r},
        static=({shape!r}, 'HIMBO - Body'), drop=(), {legs}
        subdiv=(), sk_belt={belt}, sk_anchor={anchor}, ramp=10.0, expect={expect!r},
{tkeys}    )),
)
'''
for name, (prefix, title, path, shape, sel, legs, belt, expect, tkeys, dkeys, pend) in ROBES.items():
    pieces = [('Robe', shape, sel, 'skirt:outer')]
    if pend:     # a tuple of components, or a full selector
        pieces.append(('Sash', shape, pend if isinstance(pend[0], str) else ('comps', tuple(pend)), 'pendants'))
    tk = dict(slits=False); tk.update(tkeys); dkeys = dict(dkeys)
    leg_zmin = tk.pop('leg_zmin', 6.0)      # trousers reaching below it are cut by height per weight (_0 / _1 differ): go lower
    for k in ('nrow', 'row_margin', 'max_chains', 'chain_spacing'):     # design-level keys (OVERRIDES / Dz) in the skirt builder
        if k in tk: dkeys[k] = tk.pop(k)
    if legs == 'body':
        lg = f"pants=None, legs_body={BODY},"
    else:
        # pants_zmax cuts by height per weight: above the trousers' top it keeps whole components (_0 / _1 match); v1 barkeeper
        # at belt + 2.5 = 63 cut the trousers mid-thigh differently in _0 and the leg pull failed
        lg = f"pants={legs[0]!r}, pants_comps={legs[1]!r}, pants_zmax={tk.pop('pants_zmax', belt + 2.5)},"
    txt = TEMPLATE.format(leg_zmin=leg_zmin, name=name, prefix=prefix, title=title, src=H + path, out='meshes/' + path, xml=name + 'M.xml',
                          pieces=pieces, shape=shape, legs=lg, belt=belt, anchor=belt + 2.0, expect=expect,
                          tkeys=''.join(f'        {k}={v!r},\n' for k, v in tk.items()),
                          dkeys=''.join(f'    {k}={v!r},\n' for k, v in dkeys.items()))
    open(HERE + 'robe_' + name.lower() + '.py', 'w', encoding='utf-8').write(txt)
    print('wrote robe_' + name.lower() + '.py')
