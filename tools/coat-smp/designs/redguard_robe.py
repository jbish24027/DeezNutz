# Authoria (2026-10-18): Redguard Clothes (clothes/redguard/redguardoutfit, HIMBO Vanilla Armors men's mesh).
# Shape 'Redguard Fat Outfit': comp 0 = chest + sleeves + the BAGGY TROUSERS 7161 (z 6.7-85.9 - v1 took them for a robe and
# swung them; they stay on the legs); comp 4 = the long back panel (outer 6810 / inner 7020) hanging from the shoulders to z 19:
# the only long cloth -> its part below the belt line swings, colliding with the trousers; comp 1 = belt (z 74-83), comp 2 =
# buckle; comps 3 / 5 / 6 = the sash wrapped and hanging on the left hip (z 54-90) -> 'pendants'.
MODS = 'C:/1. AUTHORIA/mods/'
HIMBO = MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors/meshes/clothes/'
WORK = 'C:/1. AUTHORIA/_tools/coat-smp/designs/out/'
STAGE = 'C:/1. AUTHORIA/_tools/coat-smp/designs/stage/m'
XM = 'SKSE\\Plugins\\hdtSkinnedMeshConfigs\\AuthoriaVanillaCoats\\'

DESIGN = dict(
    name='RedguardRobe', prefix='ARG', title='Redguard Clothes (clothes/redguard/redguardoutfit)',
    stage=STAGE, work=WORK,
    phys='cloth',
    tex_roots=[MODS + 'Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors'],
    install=MODS + 'Authoria - SMP Vanilla Coats',
    backups='D:/1. MOD STUFF/- ARR STUFF/coat-smp-backups',
    nrow=7, max_chains=12, chain_spacing=30.0, leg_zmin=6.0,
    row_margin=[1, 1, 1.5, 2, 2.5, 3, 3],
    # the sash: a cloth strip on one hinge (the SoS cloth sash-end recipe, no wind so it never twitches standing still)
    pendant_share=0.8,
    pendant_def=dict(mass=0.35, inertia=4.5, lin=0.45, ang=0.45, friction=0.0, wind=0.0),
    pendant_lim=dict(lo=(-0.35, -0.25, -0.2), hi=(0.0, 0.25, 0.2), lin=0.0, astiff=14),
    targets=dict(
        m=dict(
            mode='nif',
            src=HIMBO + 'redguard/redguardoutfit_{}.nif',
            out='meshes/clothes/redguard/redguardoutfit_{}.nif',
            xml=XM + 'RedguardRobeM.xml',
            pieces=[('Robe', 'Redguard Fat Outfit', ('islands', 4, {6810: 415, 7020: 305}, (), 76.0), 'skirt:outer'),
                    ('Sash', 'Redguard Fat Outfit', ('comps', (3, 5, 6)), 'pendants')],
            static=('Redguard Fat Outfit', 'HIMBO - Body'), pants='Redguard Fat Outfit', pants_comps=(0,), pants_zmax=73.0, drop=(),
            subdiv=(), slits=True, slit_max_hw=170.0, axis_xy=(-0.5, 1.5), sk_belt=73.5, sk_anchor=75.5, ramp=10.0,
            expect={0: 6358, 1: 1508, 3: 904, 4: 720, 5: 402, 6: 310}, ground_z=-1.5, panels=2,
        ),
    ),
)
