# Authoria (2026-10-18): Blue Mage Robes (clothes/monk/monkvariantoutfit, HIMBO Vanilla Armors men's mesh) - a floor-length
# robe welded into the torso shape, no trousers under it -> skirt builder (build_skirt_rig.py) with the legs from the HIMBO body.
# Shape 'robes': comp 0 = robe front 4120 / back 1838 shoulders -> floor (z 6), hem band 1219; sleeves 3206 / 3060 + cuffs
# 3051 / 3211 hang to z 68 at x +-12..32 (kept out by island). comps 1 / 2 = the sash hanging at the front left from z 72.8
# (to 41.7), comps 3-6 = its buttons -> 'pendants' (own hinge at their top, no colliders). No belt: the robe swings from the hips.
MODS = 'C:/1. AUTHORIA/mods/'
HIMBO = MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors/meshes/clothes/'
WORK = 'C:/1. AUTHORIA/_tools/coat-smp/designs/out/'
STAGE = 'C:/1. AUTHORIA/_tools/coat-smp/designs/stage/m'
XM = 'SKSE\\Plugins\\hdtSkinnedMeshConfigs\\AuthoriaVanillaCoats\\'

DESIGN = dict(
    name='MonkRobes', prefix='AMR', title='Blue Mage Robes (clothes/monk/monkvariantoutfit)',
    stage=STAGE, work=WORK,
    phys='cloth',
    tex_roots=[MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors'],
    install=MODS + 'Authoria - SMP Vanilla Coats',
    backups='D:/1. MOD STUFF/- ARR STUFF/coat-smp-backups',
    nrow=7, max_chains=12, chain_spacing=30.0, leg_zmin=6.0,
    row_margin=[1, 1, 1.5, 2, 2.5, 3, 3],
    lining_all=True,             # one visible sheet, no lining: every point of it meets the legs
    # the sash: a cloth strip on one hinge (the SoS cloth sash-end recipe, no wind so it never twitches standing still)
    pendant_share=0.8,
    pendant_def=dict(mass=0.35, inertia=4.5, lin=0.45, ang=0.45, friction=0.0, wind=0.0),
    pendant_lim=dict(lo=(-0.35, -0.25, -0.2), hi=(0.0, 0.25, 0.2), lin=0.0, astiff=14),
    targets=dict(
        m=dict(
            mode='nif',
            src=HIMBO + 'monk/monkvariantoutfit_{}.nif',
            out='meshes/clothes/monk/monkvariantoutfit_{}.nif',
            xml=XM + 'MonkRobesM.xml',
            pieces=[('Robe', 'robes', ('islands', 0, {4120: 2187, 1838: 801, 1219: 58}, (), 76.0), 'skirt:outer'),
                    ('Sash', 'robes', ('comps', (1, 2, 3, 4, 5, 6)), 'pendants')],
            static=('robes', 'HIMBO - Body'), pants=None, drop=(),
            legs_body=dict(nif=MODS + 'Highly Improved Male Body Overhaul -HIMBO-/meshes/actors/character/character assets/malebody_{}.nif',
                           shape='HIMBO - Body HP'),
            subdiv=(), slits=False, sk_belt=72.0, sk_anchor=74.0, ramp=10.0,
            expect={0: 4074, 1: 345, 2: 309}, ground_z=-1.5, panels=2,
        ),
    ),
)
