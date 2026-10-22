# Example design file for build_skirt_rig.py - a mail skirt over a cloth skirt, two hip plates, a belt with a hanging
# tail; men's finished meshes (_0/_1) + the women's BodySlide project. Every key is explained; copy this file per armour
# and fill it from survey_mesh.py's output. Numbers below are illustrative: SURVEY YOUR OWN MESH.
#
# Paths: forward slashes. 'src' / 'osp' are read only. Everything is written under 'stage' (an MO2 mod folder layout -
# make it a work folder, then install it as a new mod). 'xml' is the SMP XML path relative to Data, with backslashes,
# exactly as the game will look it up.

MODS = 'C:/Modding/MO2/mods/'                         # your MO2 mods folder (only used to build the paths below)

DESIGN = dict(
    name='BandedMercenary',            # used for report / log file names
    prefix='BMR',                      # bone + collider name prefix: UNIQUE per armour family. SMP finds bones by NAME on the
                                       # actor - two armours sharing bone names tangle when both are worn or swapped
    title='Banded Mercenary Armor',    # goes into the XML header comment
    stage='C:/Modding/work/banded-smp/stage',   # output folder (mirrors Data: meshes/, SKSE/, CalienteTools/)
    # work='...',                      # report/log folder (default: <this file's folder>/out)

    # feel: a preset name ('cloth', 'leather', 'leather_lamellar', 'lamellar', 'chain') or a dict
    # dict(SK_DEF=..., SK_LIM1=..., SK_LIM=...) - see references/xml-and-physics.md. Omit = heavy lively default.
    phys='chain',
    # free_max=0.85,                   # max share of the skirt that swings free of the legs (preset default; 0.8-0.9)
    # gap=(0.5, 3.5),                  # (near, far): cloth this close to the trousers follows them, this far swings.
                                       # short hip-hugging skirts (0.0, 1.5)
    # bag=True,                        # the belt piece has a bag: its biggest non-band component gets its own hinged bone
    # bag_bone='Bolsa 1',              # ... the author's existing bag bone name, if the source mesh has one
    # tip_collide=False,               # belt tail colliders - leave off: a tail that rides the skirt and also collides
                                       # pushes the skirt twice = twitching
    # tip_ride=0.9, tip_ride_flat=True # (per target) a long tail that sinks into the skirt in tests rides it 90%
    # tex_roots=[MODS + 'Realistic Armor'],   # mod folders holding textures\... for pose_render.py

    # ---- rebuild.py (one command per round): where the stage installs, where backups go, what to equip in game
    # install=MODS + '[NoDelete] My Armor SMP',   # the mod folder the stage is compared with and copied into (--install)
    # backups='C:/Modding/work/backups',          # replaced files are copied here first (default <work>/backups; never in mods/)
    # items=['xx000D62 Mercenary cuirass'],       # FormIDs -> <work>/<name>_console.txt (player.additem / equipitem + smp reset)

    # ---- rig size (defaults suit a knee skirt: 5 rows, up to 12 chains, 30 deg apart). A floor-length gown wants more:
    # nrow=8, max_chains=18, chain_spacing=20.0,  # rows per chain, chains round the body, degrees between chains
    # leg_zmin=6.0,                   # trouser / body triangles below this height are not leg colliders (default 15 = above the boots)
    # free_sigma=6.0,                 # width (units) of the hand-over from following the thigh to swinging free (default 4)
    # leg_sigma=3.0,                  # smoothing of the leg-follow weights
    # ---- collider fit (defaults are the confirmed knee-skirt values)
    # pmin_c=0.05,                    # a skirt point collides when its physics share is at least this (default 0.5)
    # lining_min_gap=0.6,             # cloth resting closer than this to the real trousers follows them and does not collide
    # leg_maxin=1.0,                  # the leg collider is pulled in at most this far to clear resting cloth (1.0 max - more = thigh clips)
    # leg_clear=0.6,                  # clearance the pull-in aims for
    # leg_facing=0.25, side_facing=0.6,   # one-sided leg pieces: front/back = |normal y| above leg_facing, sides = |normal x| above side_facing
    # leg_margin=0.4, lining_margin=0.1,  # XML collision margins of the leg pieces and the skirt lining
    # row_margin=[1, 1, 1.5, 2, 2.5, 3, 3, 3],   # per-row margin multiplier (gowns: grows towards the hem so legs push it early)
    # ---- XML extras
    # links=dict(lin=3.0, ang=0.6, lstiff=10, astiff=0),   # ring links between neighbouring chains: how far they may part / turn,
                                       # with springs pulling them back (default lin .25 ang .3, no springs = one stiff bell)
    # thigh_leash=dict(slack=0.15, cos=0.3),   # tie the first swinging bone of the front / back chains to the thigh of its side:
                                       # free ahead of the thigh, never more than `slack` rad behind its swing (confirmed in
                                       # game: New Legion); cos = how far round the body the leashed chains reach (0.5 = 60 deg)

    targets=dict(
        # ---------------------------------------------------------------- a finished mesh pair (_0 / _1 weights)
        m=dict(
            mode='nif',
            src=MODS + 'Realistic Armor/Meshes/Armor/Mercenary/Armor2M_{}.nif',   # {} = 0 / 1
            out='meshes/armor/mercenary/Armor2M_{}.nif',                           # relative to stage = the path the game loads
            xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\MyArmorSMP\\BandedMercenaryM.xml',
            # pieces: (output shape name, source shape, selector, role)
            #   selector None = the whole shape; ('comps', (ids...)) = welded components; ('islands', comp, {island id: size},
            #   (extra comps...)[, zmax]) = texture islands of one component; ('below', comp, z) = a component's triangles
            #   wholly below z; ('islands_below', comp, z) = a component's texture islands wholly below z.
            #   roles: 'skirt:outer' (exactly one - the visible layer that meets the legs), 'skirt:inner', 'flaps' (the two
            #   biggest components become rigid plates, the rest straps), 'belt' (band + hanging tail [+ bag]),
            #   'bag' (any number: a separate bag / pouch shape on its own hinge at its top edge; design keys
            #   bag_share / bag_def / bag_lim - the confirmed SoS bag = .8 / BAG_DEF_SOS / BAG_LIM_SOS in coat/build_coat_rig.py -
            #   and bag_leg_clear (default .8): bag points resting closer than this to the legs do not collide).
            #   'pendants' (claws, charms, a strap on a cord: each group of touching welded components on its own hinge at
            #   its top, child of the skeleton bone that carries it, no colliders; design keys pendant_share / pendant_def /
            #   pendant_lim - Black Bear heavy: the SoS bag recipe at half the swing).
            pieces=[('SobreSaia', 'SobreSaia', None, 'skirt:outer'), ('Saia', 'Saia', None, 'skirt:inner'),
                    ('Escudo', 'Escudo', None, 'flaps'), ('Cinto', 'Cinto', None, 'belt')],
            static=('Armor003', 'Armor004'),   # shapes that stay rigid (cuirass); used to keep colliders below them
            pants='Armor001',                  # the trousers shape: the legs the skirt follows and collides with
            drop=('Under', 'coll_body'),       # shapes NOT written (the author's old collision bodies, hidden underwear)
            # drop_comps={'Armor': (3, 13)},   # components removed from a static shape (duplicates of a moving piece)
            subdiv=('SobreSaia', 'Saia', 'tip'),   # split every triangle 1->4 (low-poly cloth only bends at its vertices);
                                                   # 'tip' = the belt's hanging tail
            slits=True,                        # find slits in the outer layer's hem and part the chains there
            sk_belt=68.0,                      # where the skirt starts to swing: the LOWEST point of the rigid cover's lower
                                               # edge over the skirt's top (belt band or cuirass hem, whichever hangs lower;
                                               # survey_mesh.py prints 'lower edge by angle'), or up to 1 unit under it
            sk_anchor=70.0,                    # pinned anchor row of every chain: sk_belt + 2
            ramp=8.0,                          # units below sk_belt over which physics fades in (6-12; default 6)
            # axis_z=(58.0, 66.0),             # height band whose centre is the skirt axis (default sk_belt-10..sk_belt-2);
                                               # 'top' = the skirt's own top edge
            # tail_split=74.4,                 # the belt piece is ONLY a tail (band is part of a static shape): split height
            # expect={'SobreSaia': {0: 279}},  # component sizes you rely on - the build stops if the mesh differs.
                                               # {'Shape': {comp: size}} checks that shape (whole-shape pieces too);
                                               # {comp: size} checks every shape that is CUT by a selector
            # pants_n=1821,                    # use only the first N trouser points (when _1 trousers carry extra pieces)
            # pants_zmax=80.0,                 # only trouser points under this height are legs (one component with a torso)
            # vary=('Fur',),                   # shapes whose _0 / _1 point counts differ in the author's mesh (rigid ones; a piece
                                               # cut from one is still checked point for point)
            # rename0={'MaleBody': 'MaleBody_outfit'},   # the author named a shape differently in _0
            # slit_max_hw=80.0,                # widest gap (half-width, deg) at the hem that counts as a slit (default 25): a
                                               # loincloth's open sides between front + back flap
            # flap_leg_clear=0.8,              # hip-plate collision points resting closer than this to the legs do not collide
            # pants_comps=(1,),                # only these welded components of the trousers shape are legs (the shape
                                               # also holds a shirt / torso whose points are interleaved with the legs')
                                               # A lining region with no points (side slits under hip plates) gets no
                                               # collider and no XML entry - the build log says so.
            # front_no_inner=True,             # leg fronts exclude inner-thigh faces (front centre pushed between the legs)
        ),
        # ---------------------------------------------------------------- a BodySlide project's slider set
        f=dict(
            mode='bodyslide',
            osp=MODS + 'Realistic Armor 3BA/CalienteTools/BodySlide/SliderSets/Realistic Armor 3BA.osp',
            set='Realistic Armor 3BA Nord Mercenary Heavy Armor (Physics)',
            xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\MyArmorSMP3BA\\BandedMercenary.xml',   # each body gets its OWN xml
            # one big 3BA shape: cut the pieces out of it (survey_mesh.py --osp ... --set ... lists components/islands)
            pieces=[('Skirt', 'Armor003', ('islands_below', 0, 72.5), 'skirt:outer'),
                    ('Escudo', 'Armor003', ('comps', (3, 4, 6, 7, 8, 9, 10, 11, 12, 13)), 'flaps'),
                    ('Cinto', 'Armor003', ('comps', (2, 17, 18, 19)), 'belt')],
            expect={0: 6187, 2: 1214, 3: 498, 4: 498, 17: 250, 18: 187, 19: 47}, island_sizes=(979, 549),
            static=('Armor003', 'Armor004'), pants='Armor002', slits=False,
            sk_belt=69.0, sk_anchor=71.0, ramp=8.0,
            # preset=(MODS + 'MyBody/CalienteTools/BodySlide/SliderPresets/My Preset.xml', 'My Preset'),  # verify_rig.py
            # ---- dresses over bare legs / dense rigs (per target)
            # legs_body=dict(osp=MODS + 'CBBE 3BA (3BBB)/CalienteTools/BodySlide/SliderSets/SE 3BBB Amazing.osp',
            #                set='CBBE 3BBB Body Amazing', shape='3BA'),   # the legs come from the BODY's own set (an outfit
                                       # project usually cuts the thighs away under a skirt); its slider data goes onto the leg
                                       # colliders; nif targets: legs_body=dict(nif='.../femalebody_{}.nif', shape='...')
            # ground_z=-1.5,                 # lower the ground plane for a hem resting at z 0 (nothing may touch at rest)
            # panels=3,                      # cut the skirt into N shapes by chain sector when the rig exceeds 80 bones
            # lining_lr=True,                # the side lining as left + right shapes (needed with many chains)
        ),
    ),
)
