# WORKED EXAMPLE for the coat builder: the seven Stormcloak coats of NordwarUA's Sons of Skyrim 2.0, exactly as installed
# and confirmed in game (2026-10-11). Copy this file per project; every design here shows a different situation:
#   Braided    - coat + inward lining, belt band + tail, left-hip strap ('flaps' role, one plate), bag, sash end ('tail' role)
#   Lamellar   - the same parts, no bag                      Heavy       - knee-length plates, hem eased off the trousers (hem_clear), side_follow
#   Breastplate- sash + skirt cut by texture ISLAND          Hide        - skirt by island + a welded belt tail as role 'tail'
#   Chainmail  - mail outer + blue skirt inner on ONE rig via the 'hemband' selector, the inner double-sided
#   Officer    - THREE skirt layers on chains of their own ('skirt:outer@Under', '@Tasset' groups) + colliders between layers (layer_coll)
# Paths: the men's meshes come from the mod's BSA extracted to a folder (SOS_BSA); their shaders from frozen copies of the
# PBR-patched meshes (PBR_DONORS) so the men's mod can outrank the patcher output; the women's sets from the 3BA BodySlide mod
# (F_BS), each written .osp starting from the INSTALLED override (MOD_F) so the other coats keep their physics.
# Run:  python rebuild_coat.py <this file> Braided [--install]      (or build_coat_rig.py <this file> Braided m f)
# The file runs with build_coat_rig.py's names in scope (PHYS_CHAIN, STRAP_DEF, SKO_MAX_NZ, TIP_DEF ... os, np): no imports.
# Sons of Skyrim 2.0 designs for the skill's coat builder (scripts/coat/build_coat_rig.py). This is build_sos.py's designs
# block, moved out verbatim on 2026-10-11. It runs with the builder's names in scope (PHYS_CHAIN, STRAP_DEF, SKO_MAX_NZ,
# TIP_DEF ..., os, np) - no imports needed. COAT_STAGE_SUFFIX=_skill builds into stage_skill/ + out_skill/ (regression runs).
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'
MODS = 'E:/Modlists/LoreRim/mods/'
BACKUPS = 'C:/Users/earln/.claude/projects/E--claude-work/backups/'      # replaced mod files are copied here before an install (never inside the mods tree)
_sfx = os.environ.get('COAT_STAGE_SUFFIX', '')
WORK = HERE + ('out' + _sfx + '/' if _sfx else '')      # report (rework_report.json) + logs; the project keeps them in its root
PRESET = (MODS + '[NoDelete] Lovely Lady v6.1 - REDUCED/CalienteTools/BodySlide/SliderPresets/Lovely Lady v6 - Reduced (Clothed).xml',
          'Lovely Lady v6 - Reduced (Clothed)')      # the user's BodySlide preset (verify_coat.py builds with it)
TEX_ROOTS = [MODS + '[NoDelete] Sons of Skyrim PBR', MODS + 'Sons of Skyrim v2.0 - My patches and fixes by Xtudo SE',
             'C:/Users/earln/AppData/Local/Temp/claude/E--claude-work/9108c909-c715-411b-bdd8-c8748f38a3e2/scratchpad/sos_tex']

SOS_HERE = HERE
STAGE_M = HERE + 'stage' + _sfx + '/m/'
STAGE_F = HERE + 'stage' + _sfx + '/f/'
STAGE = STAGE_F             # build() / bodyslide() write the women's ShapeData + osd + osp under STAGE
MOD_M = MODS + '[NoDelete] Sons of Skyrim 2.0 - SMP Physics/'
MOD_F = MODS + '[NoDelete] Sons of Skyrim 2.0 - SMP Physics - 3BA BodySlide/'
SOS_BSA = r'C:/Users/earln/AppData/Local/Temp/claude/E--claude-work/9108c909-c715-411b-bdd8-c8748f38a3e2/scratchpad/sos_bsa/meshes/nordwar/sonsofskyrim/'
PBR_DONORS = HERE + 'pbr_donors/'       # frozen copies of the PBR-patched men's meshes (shader donors; geometry comes from the BSA)
F_BS = MODS + 'Sons of Skyrim - HIMBO and 3BA/CalienteTools/BodySlide/'
XM = 'SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\'

def _f_set(osp, set_):
    return dict(osp=F_BS + 'SliderSets/' + osp, osp_installed=MOD_F + 'CalienteTools/BodySlide/SliderSets/' + osp, set=set_)


# ---------------------------------------------------------------- Armors/BraidedLeatherSC = 'Stormcloak Chainmail with Leather Cuirass'
# One shape (Torso002). comp 0 = coat: mail skirt (islands 1508 / 1899, shoulders to hem, real side slits to z 63.5) + its
# quilted lining (1833 / 1834, inward, z 43.8-74.0) + the blue sash wrapped round the waist (static); comp 1 = trousers (781);
# comp 2 = belt band z 74.5-79.2 + tongue to z 56.5 (front right); comp 3 = left-hip strap loop (z 66-79); comp 5 = bag (back
# right, z 60-79.5); comp 7 / 9 = buckle + prong; comp 8 = the sash's hanging end (front left, z 54.9-71.8); comp 4/6/10 chest.
# Women's ShapeData: the same components and islands, ~1.3 higher at the waist.
_BR_EXPECT = {0: 2543, 1: 781, 2: 507, 3: 342, 5: 294, 7: 128, 8: 120, 9: 40}
_LM_EXPECT = {0: 2543, 1: 781, 2: 665, 3: 434, 6: 130, 7: 128, 12: 40}
_HV_EXPECT = {0: 3069, 1: 706, 2: 641, 3: 417, 6: 131, 7: 128, 12: 40}
# Reinforced: the v1 port's skirt feel the user likes (mass .6, damping .5 / .5) on the RA chain limits
PHYS_HEAVY = dict(PHYS_CHAIN, SK_DEF=dict(PHYS_CHAIN['SK_DEF'], mass=0.6, inertia=14.0, ang=0.55),    # v12 (user: 'this long piece in 4 sections, it bends weirdly'):
                  SK_LIM1=dict(lo=(-1.0, -0.25, -0.08), hi=(0.08, 0.25, 0.08), lin=0.0, stiff=(22, 8, 8)),    # a stiff sheet swinging from the belt - the lower
                  SK_LIM=dict(lo=(-0.3, -0.12, -0.05), hi=(0.08, 0.12, 0.05), lin=0.0, stiff=(26, 10, 10)))    # joints bend little and spring back (was -0.8 / 14)
HEAVY_HEM = dict(clear=2.8, full=46.0, top=56.0)        # knee: hem off the trousers (men's hem z 35-37); v2 2.0 -> 2.8: knees out 8 deg sank 20 side pts 1.5-1.8 by the slits
HEAVY_HEM_F = dict(clear=2.0, full=47.3, top=57.3)      # women's coat sits ~1.3 higher
# v3 (user in game: 'twitches a little bit standing still'): the knees-apart idle stance presses the knee-length hem's sides
# into the leg colliders (idle_check knees out 8 deg: men 95 / women 166 points, the short coats 14-66; all at z 35-56 within
# ~20 deg of the sides) -> there the hem follows the thighs more
HEAVY_SIDE = dict(half=25.0, fade=20.0, ztop=50.0, zfade=8.0, free=0.45)
HEAVY_SIDE_F = dict(half=25.0, fade=20.0, ztop=51.3, zfade=8.0, free=0.45)
# v3 (user: 'the sash ... gets stuck when i jump ... around the waist line'): the Braided sash limits let it fold up 83 deg
# (.55 + 3 x .3) - a jump flung its end up to the belt (heavy_sash_jump.py: the lifting skirt pushes 248 of 251 contact points
# UP). Folding now stops at ~51 deg (.35 + 3 x .18), sideways ~.85 rad (was 1.65), a bit heavier, less wind
HEAVY_SASH_DEF = dict(mass=0.35, inertia=4.5, lin=0.45, ang=0.45, friction=0.0, wind=0.15, gravity=1.0)   # v12: wind .5 -> .15 (gusts twitched it standing still)
HEAVY_SASH_LIM = dict(lo=(-0.35, -0.25, -0.2), hi=(0.0, 0.25, 0.2), lin=0.0, astiff=14)
HEAVY_SASH_LIM2 = dict(lo=(-0.18, -0.2, -0.2), hi=(0.0, 0.2, 0.2), lin=0.0, astiff=10)
# Breastplate (Padded Gambeson with Scaled Cuirass): comp 0 = the gambeson (islands 2599 back 774 / 2595 front 704, shoulders to
# hem 44.9, real side slits) + lining (1820 / 1814) + LONG SLEEVES (2772 / 3169 + cuffs 2798 / 3195, down to z 69 - a plain height
# cut would take the cuffs into the skirt) + the sash end WELDED in (3252 outer 60 + 3264 back 25, front-right z 54.9-71.5);
# comp 1 trousers, 2 belt + tongue, 3 left-hip strap, 4 bag (back right), 5 buckle, 6 prong. Same ids on the women's mesh.
_BP_EXPECT = {0: 3265, 1: 781, 2: 507, 3: 342, 4: 210, 5: 128, 6: 40}
_BP_SKIRT = {2599: 774, 2595: 704, 1820: 97, 1814: 89}
_BP_SASH = {3252: 60, 3264: 25}
# user: 'make the skirt a bit more free with this one. more flowy. reactive to movements ... the legs push the skirt every step'
# -> RA's cloth FLOW preset, less damping and more wind (quilted cloth, not mail)
PHYS_BREAST = dict(PHYS_FLOW, SK_DEF=dict(PHYS_FLOW['SK_DEF'], lin=0.4, ang=0.45, wind=0.35))
# ArmorHide (Leather Padded Gambeson, every Stormcloak soldier): user - 'improve the smp with the skirt and the belt. the skirt gets
# stuck on the legs, twitches a bit. and the belt needs that collision'. comp 0 = coat: outer back 1354 (313) / front 1357 (288),
# lining 1685 (107) / 1686 (91), back POUCH 370 (87, the coat has a hole behind it -> it rides the skirt), the hanging belt TAIL
# 679 (32) + 695 (16) welded in (front-left z 54.6-71.6), LONG SLEEVES 1271 / 816 + cuffs to z 69.8 (kept out by island);
# comp 1 trousers, 3 + 4 buckle + prong (static, the belt is painted), 2 + 5 chest buckle. CLOSED tube (slits painted).
# Women (re-indexed): outer 2882 (355) / 2889 (331), lining 1758 / 1759, pouch 399, tail 737 + 753; ~1.5 higher.
_HD_EXPECT_M = {0: 1687, 1: 781, 2: 128, 3: 128, 4: 33, 5: 33}
_HD_EXPECT_F = {0: 1787, 1: 781, 2: 128, 3: 128, 4: 33, 5: 33}
# keep the v1 feel (very light quilted cloth, damping .5 / .5) on the RA cloth preset
PHYS_HIDE = dict(PHYS_FLOW, SK_DEF=dict(PHYS_FLOW['SK_DEF'], mass=0.5, lin=0.5, ang=0.5, wind=0.25))
# Officer: subtle (user) - the RA chain preset with the swing cut to ~60% and stiffer springs
_OF_TASSETS = (2470, 2479, 2241, 2672, 2667, 2638, 2666)
_OF_SASH = {2109: 53, 2160: 16, 2155: 17}
# v2: the mail hangs from the tassets' folds (hinge z 62, 4 rows of ~3.7 - the v1 hinge at the belt swung its hidden top 13 units
# under the tassets, so a swing drove the mail out through the tasset / sash hems) - inertia 10 -> 7 for the shorter bones
# v3 (2026-10-11, user: v2 'still moves as one piece'): three DISTINCT feels. Mail = momentum (inertia 12, damping .3/.4) so it swings
# later and longer than the plates over it; springs lighter; no longer rides the tasset bones (v2 tied 344 pts to them).
# v4 (2026-10-11, user in game: the plates sat inside the mail, the blue hem creased out past the border): the mail = the author's
# WHOLE sheet (mail + border + embroidered hem row) on 5 bones per chain, the two hem rows looser (SK_LIM_LOW) so the blue hem trails
# the mail instead of being a separate chain that tore the painted seam at z 48; joint limits sum to 89 deg (New Legion lesson)
# v6 (user, in game: the trousers poke through the upper mail with a leg raised; combat leaves the mail inside a leg): the mail is
# hinged at the BELT line (sk_anchor 68, where the sheet is attached) instead of the plates' fold at 62 - the band under the plates
# now has 5-6 units of swing room and its own leg colliders (it had < 2 and none); first joint out .65, the rest .2 / .25 (sum 89 deg)
PHYS_OFFICER = dict(SK_DEF=dict(mass=0.8, inertia=12.0, lin=0.4, ang=0.5, friction=0.0, wind=0.12),      # v7: damping .3/.4 -> .4/.5 (the front band rang after each step's push)
                    SK_LIM1=dict(lo=(-0.65, -0.2, -0.08), hi=(0.05, 0.2, 0.08), lin=0.0, stiff=(20, 8, 8)),
                    SK_LIM=dict(lo=(-0.2, -0.15, -0.06), hi=(0.05, 0.15, 0.06), lin=0.0, stiff=(12, 5, 5)),
                    SK_LIM_LOW=dict(lo=(-0.25, -0.15, -0.06), hi=(0.05, 0.15, 0.06), lin=0.0, stiff=(6, 3, 3)))
# v6: the sash end calmed to the Heavy coat's values (user: 'gets stuck on the left side when it swings left to right' - the RA sash
# could fold 95 deg sideways on 8 / 5 springs and lie there): sideways .2 / .15, twist .15, springs 14 / 10, wind .45
OF_TIP_LIM = dict(lo=(-0.55, -0.02, -0.02), hi=(0.0, 0.02, 0.02), lin=0.0, astiff=70)     # the Officer v6 riveted strap: sideways / twist locked; v12: every belt tail, no play
OF_TIP_LIM2 = dict(lo=(-0.12, -0.02, -0.02), hi=(0.0, 0.02, 0.02), lin=0.0, astiff=90)    # lower joints near rigid - it pivots at the top (v7)
OF_SASH_DEF = dict(mass=0.35, inertia=4.5, lin=0.45, ang=0.45, friction=0.0, wind=0.15, gravity=1.0)   # v12: wind .45 -> .15 (gusts twitched it standing still)
OF_SASH_LIM = dict(lo=(-0.22, -0.12, -0.1), hi=(0.0, 0.12, 0.1), lin=0.0, astiff=14)    # v8: the free end (5 units) swings less - it came out in front of the strap
OF_SASH_LIM2 = dict(lo=(-0.12, -0.1, -0.1), hi=(0.0, 0.1, 0.1), lin=0.0, astiff=10)
# Officer v2 (user: 3 layers, 'subtle'): the blue cloth under the mail - lighter and quicker than the mail (shorter bones, ~4.5),
# smaller out-limits than the mail so it tends to stay inside it, in .05; the tassets - leather plates hinged at the belt, stiff,
# never in (they lie on the mail), small out-limits (the user: 'avoid seeing nothing under the armor'), plates held together
# v3: the blue skirt = light and quick (mass .3, inertia 5, damping .25/.3, wind .4), bigger out-limits, almost no springs
# v4: the Under layer is the LINING only (the hem row went back to the mail's sheet) - hidden under the mail, so no wind reaches it;
# its bottom edge is sewn to the hem row and rides it; smaller out-limits (it only has to stay on the legs under a flaring mail)
PHYS_OF_CLOTH = dict(SK_DEF=dict(mass=0.3, inertia=5.0, lin=0.3, ang=0.35, friction=0.0, wind=0.0),
                     SK_LIM1=dict(lo=(-0.35, -0.2, -0.08), hi=(0.05, 0.2, 0.08), lin=0.0, stiff=(8, 4, 4)),
                     SK_LIM=dict(lo=(-0.2, -0.15, -0.06), hi=(0.05, 0.15, 0.06), lin=0.0, stiff=(5, 3, 3)),
                     LINK=(0.3, 0.4))
# v3: the tassets = heavy, slow plates (mass 1.3, inertia 22, damping .45/.5) that lift up to .4 rad at the hinge (v2: .25, stiff 40 =
# 'barely move'), never in, moderate springs bringing them back down
PHYS_OF_TASSET = dict(SK_DEF=dict(mass=1.3, inertia=12.0, lin=0.35, ang=0.4, friction=0.0, wind=0.05),      # 2 rows of ~6.5 units; v6: inertia 22 -> 12, damping .45/.5 -> .35/.4 (the corners lagged behind a pushed mail band)
                      SK_LIM1=dict(lo=(-0.4, -0.08, -0.05), hi=(0.0, 0.08, 0.05), lin=0.0, stiff=(22, 12, 12)),
                      SK_LIM=dict(lo=(-0.18, -0.06, -0.04), hi=(0.0, 0.06, 0.04), lin=0.0, stiff=(16, 10, 10)),
                      LINK=(0.12, 0.15))
# v10 (user: 'the plate on the backside where the butt is ... a bit more of a bounce as you walk or run ... not too exaggerated'): the
# back plate's chains on lighter, less damped bodies with softer springs and a little more swing - it bounces on a step and settles;
# the front / side plates keep the heavier values (the strap and the sash rest on them)
PHYS_OF_TASSET_BACK = dict(SK_DEF=dict(mass=1.0, inertia=6.0, lin=0.15, ang=0.2, friction=0.0, wind=0.05),
                           SK_LIM1=dict(lo=(-0.5, -0.08, -0.05), hi=(0.0, 0.08, 0.05), lin=0.0, stiff=(10, 12, 12)),
                           SK_LIM=dict(lo=(-0.25, -0.06, -0.04), hi=(0.0, 0.06, 0.04), lin=0.0, stiff=(8, 10, 10)),
                           LINK=(0.12, 0.15))
# the top layer = the four tasset plates + their turned-under hems + the hem's edge faces (2671-2690) + the SASH END between the
# left plate and the front-left strip: sewn to both along its sides (z 60-72) and to the fold behind it along z 60, so it hangs
# with them (its free bottom below the folds swings on the lowest rows); + its edge faces 2124 / 2131 / 2135 / 2163 (v1 left
# them on the coat: the 'dark slash' next to the belt tip in the user's screenshot)
_OF_TOP = {2470: 68, 2479: 47, 2241: 28, 2672: 18, 2667: 24, 2638: 18, 2666: 16, 2671: 4, 2675: 3, 2678: 3, 2681: 3, 2684: 3, 2687: 3,
           2690: 3, 2109: 53, 2160: 16, 2155: 17, 2124: 7, 2131: 7, 2135: 4, 2163: 3}
# v3 (user: the sash stood out stiffly - in v2 it was part of the tasset layer and moved like a plate): the sash end + its edge faces
# become their own 'tail' piece on a light wind-driven chain, like every other coat's sash; the tasset layer keeps the plates only
_OF_SASH3 = {2109: 53, 2160: 16, 2155: 17, 2124: 7, 2131: 7, 2135: 4, 2163: 3}
_OF_PLATES = {k: v for k, v in _OF_TOP.items() if k not in _OF_SASH3}


def _of_groups(dz):
    """Officer v2 layers by gender (dz = how much higher the women's skirt sits)"""
    # Under side_follow: the knees-apart idle stance pressed its hem sides 1.5-1.8 into the thighs (idle_check 8 deg: 9 sunk)
    # v5 (user, in game: the blue lining spiked through the hem row and the mail in motion -> 'make the blue skirt and the chain mail
    # one rig, bringing the 3 layers down to 2'): NO Under layer - the lining is part of the mail piece and rides its chains
    return dict(Tasset=dict(phys=PHYS_OF_TASSET, note='leather tassets + the sash end sewn between them, hinged at the belt',
                            sk_belt=71.0 + dz, sk_anchor=73.0 + dz, ramp=6.0, nrow=2, slits=False, free_max=0.8, gap=(0.0, 1.5),   # 2 rows; v8: free .8 like the mail - the strap over plates AND mail then takes one leg share (no shear, no 'magnet' at a plate corner)
                            lining_all=True, legs=True,
                            force_slits=[(-101.0, 5.0, 74.0 + dz), (1.0, 3.0, 74.0 + dz), (101.0, 5.0, 74.0 + dz)],
                            sectors=[dict(name='back', centre=180.0, half=76.0, phys=PHYS_OF_TASSET_BACK, note='the back plate bounces on a step')]))   # v10


def _wg_groups(dz, slit=105.0):
    """Eastmarch Guard (light): the three plates (z 60-78, 18 units tall) on 3 rows, hinged just above their top; slits at the plate
    edges (front centre, where the two front plates meet; +-105, where the back plate (100..260 deg) overlaps the front plates' ends) so
    each plate rides its own chains"""
    return dict(Tasset=dict(phys=PHYS_OF_TASSET, note='the three leather plates, hinged above their top edge',
                            sk_belt=76.3 + dz, sk_anchor=78.3 + dz, ramp=6.0, nrow=3, slits=False, free_max=0.8, gap=(0.0, 1.5),   # v8: as the Officer
                            lining_all=True, legs=True,
                            force_slits=[(-slit, 4.0, 79.0 + dz), (0.0, 3.0, 79.0 + dz), (slit, 4.0, 79.0 + dz)],
                            sectors=[dict(name='back', centre=180.0, half=76.0, phys=PHYS_OF_TASSET_BACK, note='the back plate bounces on a step')]))   # v10: as the Officer


def _wg_layer_coll(clear=0.8, zmax=1e9):
    return [dict(name='Mail Over', surf='Malha', facing='out', pts='Tasset', clear=clear, pen=3.0, min_radial=0.3, pts_all=True, pts_zmax=zmax, pts_skip=((0.0, 25.0),))]   # v10: + the plates' face / edge pts below the band


def _of_layer_coll(dz, clear_in=0.4):
    """Officer v2 colliders between the layers: the mail's inside over the blue lining (not its border's bottom rows, where the
    lining converges on it at the hem - the first build pulled that part 1.5 out), the mail's outside under the tassets (only
    below the tassets' folds: above them the mail rides the tasset it is sewn to)"""
    # (and not over the front opening: the lining there lies behind the blue strip of its own layer; the opening's turned edges
    #  over it forced a 2.0 pull - the first women's build kept 1 resting contact under the big preset)
    # v3: NO skip sector. v2 left +-12 deg of the front out of this collider to pass verify (the mail's turned front-opening edges forced
    # 2.0 pulls there) and the blue strip came out over the mail exactly there. v3 keeps the front strip ON THE MAIL layer (the author's
    # one sheet has no opening), so the mail has no turned edges at the front and the collider covers the whole circle.
    # v3 bands: Mail Inside starts above the border band (z 48-51 men) where the lining converges on the sheet by design (the women's
    # big-preset build had 29 collider pts at the 2.0 pull cap there and 1 resting contact); Mail Over stops below the mail's top band
    # (z 59.5-61 men), hidden under the plates, where the mail following a knees-out thigh met the tasset lining (25-30 idle contacts)
    # v4: NO zmax on Mail Over. v3 stopped it at 59.5 to pass layer_check's idle count - the 25-30 contacts were the mail's top band
    # following the thighs (trousers' weights) under plates that did not; cutting the collider there let that band out THROUGH the
    # plates' bottom edge in a legs-apart stance (the user's screenshots). With 'top_follow': 'belt' the band hangs from the belt
    # like the plates and the collider covers the whole overlap (the gores between the plates too). min_radial: no side faces.
    # Mail Inside from the border's lower edge (48): the lining's hem band below it is sewn to the sheet and rides it.
    # min_gap 0.5: lining points resting closer than that to the mail (the convergence band over the sewn hem) are left out, as the
    # leg colliders do (v4c: the small Lovely Lady build still landed 1 back point on the collider pulled 0.8 clear)
    # v5: no 'Mail Inside' (no Under layer)
    return [dict(name='Mail Over', surf='Malha', facing='out', pts='Tasset', clear=0.8, pen=3.0, min_radial=0.3, pts_all=True, pts_zmax=68.0 + dz, pts_skip=((0.0, 25.0),))]   # v6: catch 3 (a band pushed out by a thigh); v10: + the plates' face / edge pts below the band
# its welded belt tail = the RA v12 belt-tail physics (TIP_DEF / TIP_LIM, defined further down - copied here for DESIGNS)
HIDE_TAIL_DEF = dict(mass=0.8, inertia=14.0, lin=0.3, ang=0.45, friction=0.0, wind=0.25, gravity=0.5)
HIDE_TAIL_LIM = dict(lo=(-0.55, -0.2, -0.12), hi=(0.0, 0.2, 0.12), lin=0.02, astiff=70)
DESIGNS = {
    'Braided': dict(
        prefix='SBR', title='Stormcloak Chainmail with Leather Cuirass (Armors/BraidedLeatherSC)',
        phys=PHYS_CHAIN, bag=True, tip_collide=True, tip_legs=(),
        # v1 build: lining to the trousers median 1.6 -> free share median .33 with the mail default gap (.5, 3.5) = mostly
        # following the legs; the RA rule for skirts resting within ~2 of the trousers: only cloth touching them follows them
        gap=(0.0, 1.5), free_max=0.85,
        flap_follow=STRAP_FOLLOW, flap_def=STRAP_DEF, flap_lim=STRAP_LIM, flap_note='left-hip strap: a leather loop - light, little damping, bouncy',
        bag_share=BAG_SHARE_SOS, bag_def=BAG_DEF_SOS, bag_lim=BAG_LIM_SOS,
        m=dict(src=SOS_BSA + 'armors/braidedleatherscm_{}.nif', shader_donor=PBR_DONORS + 'armors/braidedleatherscm_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/armors/braidedleatherscm_{}.nif', stage=STAGE_M,
               xml=XM + 'ArmorsBraidedM.xml',
               pieces=[('Saia', 'Torso002', ('below', 0, 72.9), 'skirt:outer'),
                       ('Cinto', 'Torso002', ('comps', (2, 5, 7, 9)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (3,)), 'flaps'),
                       ('Sash', 'Torso002', ('comps', (8,)), 'tail')],
               expect=_BR_EXPECT, static=('Torso002',), pants='Torso002', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=71.5, sk_anchor=73.5, ramp=8.0),
               # (v2 tried hem_clear=dict(clear=2.0, full=50.0, top=58.0): no gain in swing_stride / jump / idle at the RA gate
               #  (knees out 8 deg: 0 sunk either way) and a visible side flare up to 2.7 - not asked for here; kept off)
        f=dict(**_f_set('Sons - 3BA - Armors.osp', 'Sons - 3BA - Armors - BraidedLeatherSCF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\ArmorsBraidedF.xml',
               pieces=[('Saia', 'Torso002', ('below', 0, 74.2), 'skirt:outer'),
                       ('Cinto', 'Torso002', ('comps', (2, 5, 7, 9)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (3,)), 'flaps'),
                       ('Sash', 'Torso002', ('comps', (8,)), 'tail')],
               expect=_BR_EXPECT, static=('Torso002', '3BA'), pants='Torso002', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=72.8, sk_anchor=74.8, ramp=8.0,
               tb_clear=0.9),      # v1 verify: the bag met the skirt-outer copy under big BodySlide bodies (1-3 pts)
    ),
    # Armors/Lamellar = 'Stormcloak Heavy Lamellar Armor': the Braided coat geometry (comp 0 2543 pts, same z range) with the same
    # parts at the same places (belt 2 + buckle 7 + prong 12, left-hip strap 3, sash end 6), no bag. User: copy the Braided setup.
    'Lamellar': dict(
        prefix='SLM', title='Stormcloak Heavy Lamellar Armor (Armors/Lamellar)',
        phys=PHYS_CHAIN, bag=False, tip_collide=True, tip_legs=(), tail_max_nz=SKO_MAX_NZ,
        gap=(0.0, 1.5), free_max=0.85,
        flap_follow=STRAP_FOLLOW, flap_def=STRAP_DEF, flap_lim=STRAP_LIM, flap_note='left-hip strap: a leather loop - light, little damping, bouncy',
        m=dict(src=SOS_BSA + 'armors/lamellarm_{}.nif', shader_donor=PBR_DONORS + 'armors/lamellarm_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/armors/lamellarm_{}.nif', stage=STAGE_M,
               xml=XM + 'ArmorsLamellarM.xml',
               pieces=[('Saia', 'Torso002', ('below', 0, 72.9), 'skirt:outer'),
                       ('Cinto', 'Torso002', ('comps', (2, 7, 12)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (3,)), 'flaps'),
                       ('Sash', 'Torso002', ('comps', (6,)), 'tail')],
               expect=_LM_EXPECT, static=('Torso002',), pants='Torso002', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=71.5, sk_anchor=73.5, ramp=8.0),
        f=dict(**_f_set('Sons - 3BA - Armors.osp', 'Sons - 3BA - Armors - LamellarF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\ArmorsLamellarF.xml',
               pieces=[('Saia', 'Torso002', ('below', 0, 74.2), 'skirt:outer'),
                       ('Cinto', 'Torso002', ('comps', (2, 7, 12)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (3,)), 'flaps'),
                       ('Sash', 'Torso002', ('comps', (6,)), 'tail')],
               expect=_LM_EXPECT, static=('Torso002', '3BA'), pants='Torso002', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=72.8, sk_anchor=74.8, ramp=8.0, tb_clear=0.9),
    ),
    # Armors/ArmorHeavy = 'Stormcloak Heavy REINFORCED Lamellar Armor': lamellar plates to the knee (hem z 35-37), real side slits,
    # same parts as Lamellar (belt 2 + 7 + 12, strap 3, sash end 6), no bag. User: keep the v1 feel (skirt mass .6 / damping .5),
    # fix sticking + twitch, 'special care for collisions with the thigh and knee' - the trousers' knee puff came out through the
    # lowest rows by the slit (ingame/20261011_heavyreinforced_knee_clip.webp; rest room at the sides z 40-52 only +0.3..+1.2)
    # -> the hem eased >= 2 off the trousers below z 46 (fading out by z 56) + the one-sided leg colliders.
    'Heavy': dict(
        prefix='SHV', title='Stormcloak Heavy Reinforced Lamellar Armor (Armors/ArmorHeavy)',
        phys=PHYS_HEAVY, bag=False, tip_collide=True, tip_legs=(), tail_max_nz=SKO_MAX_NZ,
        sko_pen=3.0,     # v2: women's run L - the leg-driven skirt under the hip strap overran it by 16 pts past the 2.0 catch
        sash_def=HEAVY_SASH_DEF, sash_lim=HEAVY_SASH_LIM, sash_lim2=HEAVY_SASH_LIM2,       # v3: never folds up to the belt
        gap=(0.0, 1.5), free_max=0.85,
        flap_follow=STRAP_FOLLOW, flap_def=STRAP_DEF, flap_lim=STRAP_LIM, flap_note='left-hip strap: a leather loop - light, little damping, bouncy',
        m=dict(src=SOS_BSA + 'armors/armorheavym_{}.nif', shader_donor=PBR_DONORS + 'armors/armorheavym_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/armors/armorheavym_{}.nif', stage=STAGE_M,
               xml=XM + 'ArmorsHeavyM.xml',
               pieces=[('Saia', 'Torso002', ('below', 0, 72.9), 'skirt:outer'),
                       ('Cinto', 'Torso002', ('comps', (2, 7, 12)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (3,)), 'flaps'),
                       ('Sash', 'Torso002', ('comps', (6,)), 'tail')],
               expect=_HV_EXPECT, static=('Torso002',), pants='Torso002', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=71.5, sk_anchor=73.5, ramp=8.0,
               hem_clear=HEAVY_HEM, side_follow=HEAVY_SIDE),
        f=dict(**_f_set('Sons - 3BA - Armors.osp', 'Sons - 3BA - Armors - ArmorHeavyF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\ArmorsHeavyF.xml',
               pieces=[('Saia', 'Torso002', ('below', 0, 74.2), 'skirt:outer'),
                       ('Cinto', 'Torso002', ('comps', (2, 7, 12)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (3,)), 'flaps'),
                       ('Sash', 'Torso002', ('comps', (6,)), 'tail')],
               expect=_HV_EXPECT, static=('Torso002', '3BA'), pants='Torso002', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=72.8, sk_anchor=74.8, ramp=8.0, tb_clear=0.9,
               hem_clear=HEAVY_HEM_F, sash_collide_below=4.5, side_follow=HEAVY_SIDE_F),   # v3: 1 sash pt 4.1 under its top met its copy under the Lovely Lady preset
    ),
    'Breastplate': dict(
        prefix='SBP', title='Stormcloak Padded Gambeson with Scaled Cuirass (Armors/BreastplateSC)',
        phys=PHYS_BREAST, bag=True, tip_collide=True, tip_legs=(), tail_max_nz=SKO_MAX_NZ,
        gap=(0.0, 1.5), free_max=0.95,
        flap_follow=STRAP_FOLLOW, flap_def=STRAP_DEF, flap_lim=STRAP_LIM, flap_note='left-hip strap: a leather loop - light, little damping, bouncy',
        bag_share=BAG_SHARE_SOS, bag_def=BAG_DEF_SOS, bag_lim=BAG_LIM_SOS,
        m=dict(src=SOS_BSA + 'armors/breastplatescm_{}.nif', shader_donor=PBR_DONORS + 'armors/breastplatescm_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/armors/breastplatescm_{}.nif', stage=STAGE_M,
               xml=XM + 'ArmorsBreastplateM.xml',
               pieces=[('Sash', 'Torso002', ('islands', 0, _BP_SASH, ()), 'tail'),
                       ('Saia', 'Torso002', ('islands', 0, _BP_SKIRT, (), 72.9), 'skirt:outer'),
                       ('Cinto', 'Torso002', ('comps', (2, 4, 5, 6)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (3,)), 'flaps')],
               expect=_BP_EXPECT, static=('Torso002',), pants='Torso002', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=71.5, sk_anchor=73.5, ramp=8.0),
        f=dict(**_f_set('Sons - 3BA - Armors.osp', 'Sons - 3BA - Armors - BreastplateSCF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\ArmorsBreastplateF.xml',
               pieces=[('Sash', 'Torso001', ('islands', 0, _BP_SASH, ()), 'tail'),
                       ('Saia', 'Torso001', ('islands', 0, _BP_SKIRT, (), 73.2), 'skirt:outer'),
                       ('Cinto', 'Torso001', ('comps', (2, 4, 5, 6)), 'belt'),
                       ('Correia', 'Torso001', ('comps', (3,)), 'flaps')],
               expect=_BP_EXPECT, static=('Torso001', '3BA'), pants='Torso001', pants_comp=1, drop=(),
               subdiv=('Saia', 'tip', 'Sash'), slits=True, sk_belt=71.8, sk_anchor=73.8, ramp=8.0, tb_clear=0.9),
    ),
    # Armors/ChainmailSC = 'Stormcloak Chainmail': user - existing SMP really bad (v1 port 9 bones), more bones; belts / straps proper
    # SMP + collisions, never through the skirt; SPLIT the mail from the blue skirt (APPROVED mockup); the hem must not clip the
    # trousers (they poke 0.3-1.3 through at rest) -> hem >= 2 off them. comp 0 = coat: mail 996 / 990 (shoulders to hem, CLOSED
    # tube, slits painted) + lining 851 / 852, LONG SLEEVES to z 67 (kept out by island); comp 1 trousers; 2 main belt + tongue (front);
    # 3 thin slung belt (z 70-78, static: tight on the waist) + 9 its buckle; 4 left-hip strap; 6 pouch (back right); 8 main buckle;
    # 5 / 7 / 10 chest. Mail outer + blue skirt inner share one chain rig (RA SobreSaia / Saia); the blue skirt double-sided.
    # Women (re-indexed, +536 pts): mail 1044 / 1050, lining 899 / 900; the belts ~2.7-4 higher.
    'Chainmail': dict(
        prefix='SCM', title='Stormcloak Chainmail (Armors/ChainmailSC)',
        phys=PHYS_CHAIN, bag=True, tip_collide=True, tip_legs=(), tail_max_nz=SKO_MAX_NZ,
        gap=(0.0, 1.5), free_max=0.85,
        flap_follow=STRAP_FOLLOW, flap_def=STRAP_DEF, flap_lim=STRAP_LIM, flap_note='left-hip strap: a leather loop - light, little damping, bouncy',
        bag_share=BAG_SHARE_SOS, bag_def=BAG_DEF_SOS, bag_lim=BAG_LIM_SOS,
        m=dict(src=SOS_BSA + 'armors/chainmailscm_{}.nif', shader_donor=PBR_DONORS + 'armors/chainmailscm_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/armors/chainmailscm_{}.nif', stage=STAGE_M,
               xml=XM + 'ArmorsChainmailM.xml',
               pieces=[('Malha', 'Torso002', ('hemband', 0, (990, 996), (851, 852), 72.9, 'mail'), 'skirt:outer'),
                       ('Saia', 'Torso002', ('hemband', 0, (990, 996), (851, 852), 72.9, 'skirt'), 'skirt:inner'),
                       ('Cinto', 'Torso002', ('comps', (2, 6, 8)), 'belt'),
                       ('Correia', 'Torso002', ('comps', (4,)), 'flaps')],
               expect={0: 1658, 1: 781, 2: 377, 3: 342, 4: 270, 5: 267, 6: 212, 7: 128, 8: 103, 9: 88, 10: 33},
               static=('Torso002',), pants='Torso002', pants_comp=1, drop=(), double_sided=('Saia',),
               subdiv=('Malha', 'Saia', 'tip'), slits=False, sk_belt=71.5, sk_anchor=73.5, ramp=8.0,
               hem_clear=dict(clear=2.0, full=50.0, top=58.0)),
        f=dict(**_f_set('Sons - 3BA - Armors.osp', 'Sons - 3BA - Armors - ChainmailSCF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\ArmorsChainmailF.xml',
               pieces=[('Malha', 'Torso001', ('hemband', 0, (1044, 1050), (899, 900), 75.7, 'mail'), 'skirt:outer'),
                       ('Saia', 'Torso001', ('hemband', 0, (1044, 1050), (899, 900), 75.7, 'skirt'), 'skirt:inner'),
                       ('Cinto', 'Torso001', ('comps', (2, 6, 8)), 'belt'),
                       ('Correia', 'Torso001', ('comps', (4,)), 'flaps')],
               expect={0: 1743, 1: 781, 2: 483, 3: 470, 4: 361, 5: 351, 6: 246, 7: 128, 8: 109, 9: 90, 10: 33},
               static=('Torso001', '3BA'), pants='Torso001', pants_comp=1, drop=(), double_sided=('Saia',),
               subdiv=('Malha', 'Saia', 'tip'), slits=False, sk_belt=74.3, sk_anchor=76.3, ramp=8.0, tb_clear=0.9,
               hem_clear=dict(clear=2.0, full=53.0, top=61.0)),
    ),
    # Windhelm/OfficerArmor = 'Stormcloak Officer Cuirass' (ARMO 08697E:Skyrim.esm), NO SMP before. APPROVED 3 layers, kept SUBTLE
    # (user: 'keep it subtle with the smp to avoid seeing nothing under the armor'): TorsoM_1 comp 0 holds the skirt - leather
    # TASSETS (islands 2470 / 2479 / 2241 / 2672 + turned-under edges 2667 / 2638 / 2666, z 60-72), the SHEET 2609 (mail + beige
    # border + embroidered blue hem + blue front strip, all painted, edges on the painted lines: border's lower edge row uv v
    # .938-.946 at z ~48, front strip u .849-.869), lining 2801 / 2802, the sash end 2109 + 2160 + 2155 (front-left z 55-72).
    # v1: mail + border with the tassets riding on it = outer; blue hem row + front strip + lining = inner, double-sided; one
    # chain rig (tassets cannot cross the mail); the belts + the hanging brown strap = ONE welded part (PantsM_1 comp 0) -> the
    # 'belt' role: the strap below the band's lower edge gets the belt-tail chain + its own collider. Same island ids on women
    # (whole skirt ~4.5-6 higher).
    # v2 2026-10-11 (user in game, ingame 3.webp / 4.webp: 'why is the whole skirt moving as one piece? ... it moves through my
    # legs ... the belt and the sash ... its like theres no collision'): v1 hung all three layers on ONE rig, and its only leg
    # colliders were the tassets' turned-under hems (the 'lining' of the outer piece) - the mail face and the blue skirt had none.
    # v2 = three rigs: the mail (main, whole sheet = leg colliders), the blue skirt 'Under' (its lining eased out of the trousers
    # and colliding with the legs + the mail's inside), the tassets + sash end 'Tasset' (plates apart at their seams, colliding
    # with the legs + the mail's outside); the mail's top edge rides the tasset it is sewn to; the strap's collider = the layers
    # under it (the sash end, the mail).
    'Officer': dict(
        prefix='SOF', title='Stormcloak Officer Cuirass (Windhelm/OfficerArmor)',
        phys=PHYS_OFFICER, bag=False, tip_collide=True, tip_legs=(), tip_under=('Tasset', 'Malha', 'Sash'),   # v8: + the sash - the strap rides OVER it (user: 'the belt sits inside the sash')
        tail_under=('Tasset', 'Malha'), tail_max_nz=SKO_MAX_NZ,          # v3: the sash end hangs over the plates AND the mail
        # v7 (user: 'the belt tip and the sash keep getting caught by the crotch area'): the mail under them carries the trousers' share
        # (1 - free = 20%) and the deeper catches now push it every step - the strap and the sash take that same leg share again (the
        # v14 rule: a step moves both together, only the swing is left to the collider). In belt mode the share is honest (v4 set 0
        # because the band then carried 60-76% thigh)
        tip_leg_follow=1.0, under_min_radial={'*': 0.3, 'Sash': 0.7},   # v8d: the sash's curled edge (facing away from the strap) out of the strap's collider
        # v7: the sash end is SEWN to the plates along its sides from the belt to the plates' bottom edge (z 60) and hangs free only
        # below it (user: 'when the sash moves left or right there's no plate behind it' - the author never drew one): above 60 it rides
        # the plates, its free 5 units hang on 2 bones from the left plate's own bone, colliding with the mail under them only
        sash_n=2, tail_hang_on='Tasset',
        # v5 (user: 'the belt is zig zagging / sitting crooked' mid-walk): a riveted leather strap barely bends sideways or twists - the
        # RA tail's .2 / .12 per joint let its three bones zig-zag and the whole strap hang 30 deg off; out-swing as before
        tip_lim=OF_TIP_LIM,   # v6: locked sideways / twist (v5's .05 still showed as a lean)
        tip_lim2=OF_TIP_LIM2,  # v7 (user: the strap kinks in the middle when the mail pushes it): the lower joints nearly rigid - it pivots at the top
        tip_plumb=True,          # v6: the drawn strap leaned 6.5 deg to the left in the front view - sheared plumb (see build_coat_rig tip_plumb)
        sash_def=OF_SASH_DEF, sash_lim=OF_SASH_LIM, sash_lim2=OF_SASH_LIM2,
        hang_under={'belt tail': ('Tasset', 'Malha'), 'sash end': ('Tasset', 'Malha'), 'hip hangers': ('Tasset', 'Malha')},
        hang_under_layers=('Tasset', 'Malha'),       # v11 (user: the hangers 'need collisions, going through the armor'): the straps settle over and collide with these
        phys_note='the mail (main chains), the blue cloth skirt under it (Under chains), the tassets with the sash end (Tasset chains)',
        gap=(0.0, 1.5), free_max=0.8,
        m=dict(src=SOS_BSA + 'windhelm/officerarmorm_{}.nif', shader_donor=PBR_DONORS + 'windhelm/officerarmorm_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/windhelm/officerarmorm_{}.nif', stage=STAGE_M,
               xml=XM + 'WindhelmOfficerM.xml',
               # v3: the front strip stays on the mail (u-range empty): the mail is the author's closed sheet, the blue skirt = hem row + lining
               # v5: ONE piece = the whole sheet (mail + border + blue hem row) + the lining islands as extras; nothing is 'blue'
               pieces=[('Sash', 'TorsoM_1', ('islands', 0, _OF_SASH3, ()), 'tail'),
                       ('Malha', 'TorsoM_1', ('uvsplit', 0, (2609,), (2801, 2802), (), 2.0, (0.0, 0.0), 62.0, 'mail'), 'skirt:outer'),
                       ('Tasset', 'TorsoM_1', ('islands', 0, _OF_PLATES, ()), 'skirt:outer@Tasset'),
                       ('Cinto', 'PantsM_1', ('comps', (0,)), 'belt')],
               expect={}, static=('TorsoM_1', 'PantsM_1'), pants='PantsM_1', pants_comp=1, drop=(), double_sided=('Malha', 'Tasset', 'Sash'),
               subdiv=('Malha', 'Tasset', 'tip', 'Sash'), slits=True, lining_all=True, sk_belt=66.0, sk_anchor=68.0, ramp=4.0, nrow=5,   # v6: hinge at the belt line (was 62 / 60)
               max_chains=14, chain_spacing=26.0,     # v6: 14 chains (7.4 units apart at the hem) - a knee bulge spans fewer chain gaps
               leg_pen=dict(Front=5.5, Back=5.5, Side=3.0),   # v6: deeper catches (3 / 3 / 1.5): combat moves left the mail inside a leg
               top_follow='belt',       # v4: every layer hangs from the belt (see skirt_w) - the v3 mail band followed the thighs under plates that did not
               side_follow=dict(half=45.0, fade=20.0, ztop=49.0, zfade=5.0, free=0.4),   # v4: the hem by the knees follows the thighs; v6: 45 deg half (the back of the knees too)
               follow_zones=[dict(centre=0.0, half=35.0, fade=20.0, ztop=52.0, zfade=4.0, free=0.5), dict(centre=180.0, half=35.0, fade=20.0, ztop=52.0, zfade=4.0, free=0.5)],   # v10: the hem front / back follow the stride more (the trousers showed through the mail walking / running); catches 5.5
               tail_top=60.0, sash_collide_below=0.5,       # v7: the sash's free chain starts at the plates' bottom edge; collision points from 0.5 below it
               layer_lift=[(('Tasset', 'Sash', 'Cinto'), dict(under='Malha', clear=0.8, hinge=68.5))],
               layer_clear=[(('Tasset',), dict(under='Malha', clear=0.8, zmax=68.5, fade=2.0, sigma=2.0))],   # v10: the side edges near the pivot (the lift is capped) pushed out to 0.8 (user: the mail through the trim at the plate's edge)   # v7: the plates' trim rested ON the mail - rotated out until 0.8 clear, the sash with them; v7c: pivot at the belt band's lower edge (68.5), not the physics hinge (73) - pivoting at 73 moved the plate 0.5 out at the band's edge and opened a slot you could see into
               lining_clear=dict(clear=0.5, fade=1.5, weld_keep=0.5),   # v7: the lining z-fought through the embroidered band above their welded hem (user: 'the embroidered part disappears')
               # v5: the lining is inside the mail piece: the free-share field comes from the SHEET (outer faces) so the mail keeps the v4
               # feel, lining points inside the trousers (hidden, z 48-73) never pull the leg collider in, and the hem easing reads the sheet
               # v5b: the hidden lining's points on the trousers (gap < 0.8) neither collide nor pull the legs in - the sheet's points do that
               field_src='outer', flare_src='outer', leg_pull_min_gap=0.8, lining_min_gap=0.8,
               leg_max_nz=0.6,          # v5: no upward-facing trouser faces in the leg colliders - a knee bulge rising into the hem can only push it OUT, not up
               # v9 (user: 'the embroidered pattern disappears when moving', 'the pattern is now on the inside'): the lining and the sheet
               # had different bones - the field read at the nearest author's vertex (rows 4.3 apart in the band), the 4-bone cap at the
               # centre leaving one chain bone - and crossed by up to 2.1 with a thigh raised. The field is interpolated, a tiny pelvis
               # share folded before the cap, and every lining point takes the sheet's weights at its spot (lining_check: 0 through)
               field_interp=2.0, cap_pelvis_min=0.05, lining_ride=True,
               tail_clear=0.8,
               groups=_of_groups(0.0), layer_coll=_of_layer_coll(0.0),
               hangers=dict(n=3),       # v10 (user: 'add smp to these leather pieces on both sides ... swing off the hoop'): the strap slung between the two rings at each hip, the rings on their loops
               # v4: the sheet's hem touched the calves at the back of the knees and pulled the leg collider in 3.0 - eased 0.8 off the
               # trousers below 46, fading out by 50 (reads the sheet: src outer)
               layer_flare=[('Malha', dict(clear=0.8, full=46.0, top=50.0, src='outer'), False)]),
        f=dict(**_f_set('Sons - 3BA - Windhelm.osp', 'Sons - 3BA - Windhelm - OfficerArmorF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\WindhelmOfficerF.xml',
               pieces=[('Sash', 'TorsoF_0', ('islands', 0, _OF_SASH3, ()), 'tail'),
                       ('Malha', 'TorsoF_0', ('uvsplit', 0, (2609,), (2801, 2802), (), 2.0, (0.0, 0.0), 66.5, 'mail'), 'skirt:outer'),
                       ('Tasset', 'TorsoF_0', ('islands', 0, _OF_PLATES, ()), 'skirt:outer@Tasset'),
                       ('Cinto', 'PantsF_0', ('comps', (0,)), 'belt')],
               expect={}, static=('TorsoF_0', 'PantsF_0', '3BA'), pants='PantsF_0', pants_comp=1, drop=(), double_sided=('Malha', 'Tasset', 'Sash'),
               subdiv=('Malha', 'Tasset', 'tip', 'Sash'), slits=True, lining_all=True, sk_belt=70.5, sk_anchor=72.5, ramp=4.0, nrow=5, tb_clear=0.9,
               max_chains=14, chain_spacing=26.0, leg_pen=dict(Front=5.5, Back=5.5, Side=3.0),
               top_follow='belt', tail_clear=0.8,
               side_follow=dict(half=45.0, fade=20.0, ztop=53.5, zfade=5.0, free=0.4),
               follow_zones=[dict(centre=0.0, half=35.0, fade=20.0, ztop=56.5, zfade=4.0, free=0.5), dict(centre=180.0, half=35.0, fade=20.0, ztop=56.5, zfade=4.0, free=0.5)],
               tail_top=64.5, sash_collide_below=0.5,
               layer_lift=[(('Tasset', 'Sash', 'Cinto'), dict(under='Malha', clear=0.8, hinge=72.0))],
               layer_clear=[(('Tasset',), dict(under='Malha', clear=0.8, zmax=72.0, fade=2.0, sigma=2.0))],   # the women's band edge 72.0
               lining_clear=dict(clear=0.5, fade=1.5, weld_keep=0.5),
               field_src='outer', flare_src='outer', leg_pull_min_gap=0.8, lining_min_gap=0.8, leg_max_nz=0.6,
               field_interp=2.0, cap_pelvis_min=0.05, lining_ride=True,     # v9: as the Officer men's (the lining takes the sheet's weights)
               groups=_of_groups(4.5), layer_coll=_of_layer_coll(4.5),
               hangers=dict(n=3, z_top=80.5, z_bottom=70.5),       # v10: as the men's, the women's belt ~4.5 higher
               layer_flare=[('Malha', dict(clear=0.8, full=50.5, top=54.5, src='outer'), False)]),
    ),
    # Windhelm/WindhelmArmor = 'Eastmarch Guard Cuirass' (REQ_Light_Guard_Body_Eastmarch, Sons of Skyrim - Requiem Patch.esp; ARMA
    # 0_Windhelm_Armor_Light_AA). 2026-10-11 user: 'the eastmarsh guard cuirass has the same skirt setup ... same pants situation'.
    # ONE shape TorsoM_1 (6388 pts): comp 0 = the quilted coat (z 55-114), comp 1 = the skirt (1647 pts): the Officer's sheet (island
    # 1478, 496 tris, z 42.7-75.6: mail + border + blue hem painted, gores to 75.6 at the sides and 72 at the front), its lining
    # 1645 + 1646 (166 tris), THREE plates: back 1336 (128 tris), front-left 1096 (87, -111..0 deg), front-right 1345 (87, 0..110),
    # z 60-78, + their turned-under hems 1534 / 1506 / 1533; comp 2 = the trousers (766 tris, a lighter mesh than the Officer's);
    # comp 3 = belt band + pouch (static); comps 4/5 shoulder straps, 6 a buckle. No sash, no hanging strap. Women: TorsoF_0 + 3BA,
    # the same layout with its own island ids (6401 pts), the skirt ~3 units higher.
    # Design = Officer v6 (two layers hanging from the belt, 14 chains, deep leg catches, Mail Over catch 3) with the plates on
    # 3 rows (they are 18 units tall, hinged at 78.3) and their slits at the three plate gaps.
    'Guard': dict(
        prefix='SWG', title='Eastmarch Guard Cuirass (Windhelm/WindhelmArmor)',
        phys=PHYS_OFFICER, bag=False, tip_collide=False, tip_legs=(), tail_max_nz=SKO_MAX_NZ,
        tip_leg_follow=0.0, under_min_radial=0.3,
        phys_note='the mail with its lining (main chains) and the three plates (Tasset chains)',
        gap=(0.0, 1.5), free_max=0.8,
        m=dict(src=SOS_BSA + 'windhelm/windhelmarmorm_{}.nif', shader_donor=PBR_DONORS + 'windhelm/windhelmarmorm_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/windhelm/windhelmarmorm_{}.nif', stage=STAGE_M,
               xml=XM + 'WindhelmArmorM.xml',
               pieces=[('Malha', 'TorsoM_1', ('uvsplit', 1, (1478,), (1645, 1646), (), 2.0, (0.0, 0.0), 62.0, 'mail'), 'skirt:outer'),
                       ('Tasset', 'TorsoM_1', ('islands', 1, {1336: 80, 1096: 56, 1345: 56, 1534: 24, 1506: 16, 1533: 16}, ()), 'skirt:outer@Tasset')],
               expect={}, static=('TorsoM_1',), pants='TorsoM_1', pants_comp=2, drop=(), double_sided=('Malha', 'Tasset', 'Sash'),
               subdiv=('Malha', 'Tasset'), slits=True, lining_all=True, sk_belt=70.0, sk_anchor=72.0, ramp=4.0, nrow=5,
               max_chains=14, chain_spacing=26.0, leg_pen=dict(Front=5.5, Back=5.5, Side=3.0),
               top_follow='belt', side_follow=dict(half=45.0, fade=20.0, ztop=49.0, zfade=5.0, free=0.4),
               follow_zones=[dict(centre=0.0, half=35.0, fade=20.0, ztop=52.0, zfade=4.0, free=0.5), dict(centre=180.0, half=35.0, fade=20.0, ztop=52.0, zfade=4.0, free=0.5)],   # v10: as the Officer
               field_src='outer', flare_src='outer', leg_pull_min_gap=0.8, lining_min_gap=0.8, leg_max_nz=0.6,
               field_interp=2.0, cap_pelvis_min=0.05, lining_ride=True,     # v9: as the Officer men's (the lining takes the sheet's weights)
               groups=_wg_groups(0.0), layer_coll=_wg_layer_coll(zmax=73.0),
               layer_lift=[(('Tasset',), dict(under='Malha', clear=0.8, hinge=73.0))], layer_clear=[(('Tasset',), dict(under='Malha', clear=0.8, zmax=73.0, fade=2.0, sigma=2.0))], lining_clear=dict(clear=0.5, fade=1.5, weld_keep=0.5),   # v7c: as the Officer (same plates on the same mail; pivot where the coat covers the plates' top)
               layer_flare=[('Malha', dict(clear=0.8, full=46.0, top=50.0, src='outer'), False)]),
        f=dict(**_f_set('Sons - 3BA - Windhelm.osp', 'Sons - 3BA - Windhelm - WindhelmArmorF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\WindhelmArmorF.xml',
               pieces=[('Malha', 'TorsoF_0', ('uvsplit', 1, (1483,), (1650, 1651), (), 2.0, (0.0, 0.0), 65.0, 'mail'), 'skirt:outer'),
                       ('Tasset', 'TorsoF_0', ('islands', 1, {1341: 80, 1101: 56, 1350: 56, 1539: 24, 1511: 16, 1538: 16}, ()), 'skirt:outer@Tasset')],
               expect={}, static=('TorsoF_0', '3BA'), pants='TorsoF_0', pants_comp=2, drop=(), double_sided=('Malha', 'Tasset', 'Sash'),
               subdiv=('Malha', 'Tasset'), slits=True, lining_all=True, sk_belt=73.0, sk_anchor=75.0, ramp=4.0, nrow=5, tb_clear=0.9,
               max_chains=14, chain_spacing=26.0, leg_pen=dict(Front=5.5, Back=5.5, Side=3.0),
               top_follow='belt', side_follow=dict(half=45.0, fade=20.0, ztop=52.0, zfade=5.0, free=0.4),
               follow_zones=[dict(centre=0.0, half=35.0, fade=20.0, ztop=55.0, zfade=4.0, free=0.5), dict(centre=180.0, half=35.0, fade=20.0, ztop=55.0, zfade=4.0, free=0.5)],
               field_src='outer', flare_src='outer', leg_pull_min_gap=0.8, lining_min_gap=0.8, leg_max_nz=0.6,
               field_interp=2.0, cap_pelvis_min=0.05, lining_ride=True,     # v9: as the Officer men's (the lining takes the sheet's weights)
               groups=_wg_groups(3.0), layer_coll=_wg_layer_coll(zmax=76.0),
               layer_lift=[(('Tasset',), dict(under='Malha', clear=0.8, hinge=76.0))], layer_clear=[(('Tasset',), dict(under='Malha', clear=0.8, zmax=76.0, fade=2.0, sigma=2.0))], lining_clear=dict(clear=0.5, fade=1.5, weld_keep=0.5),
               layer_flare=[('Malha', dict(clear=0.8, full=49.0, top=53.0, src='outer'), False)]),
    ),
    # Windhelm/WindhelmArmorHeavy = 'Eastmarch Guard Heavy Cuirass' (REQ_Heavy_Guard_Body_Eastmarch; ARMA 0_Windhelm_Armor_Heavy_AA).
    # ONE shape ArmorM_1 (8367 pts): comp 0 = the coat + the Guard skirt (sheet 1798, lining 2077 + 2078, plates back 1656 (90..270 deg)
    # / front-left 1416 / front-right 1665, hems 1854 / 1826 / 1853 - the light cuirass's islands at other ids), comp 1 = belt band +
    # the hanging strap (2044 pts, z 54-80: the Officer's belt), comp 2 = the Officer's trousers (1624 tris), comp 5 = pouch (static).
    # Women: ArmorF_0 (no separate body shape), the SAME island ids, the skirt ~2.5 units higher.
    'GuardHeavy': dict(
        prefix='SWH', title='Eastmarch Guard Heavy Cuirass (Windhelm/WindhelmArmorHeavy)',
        phys=PHYS_OFFICER, bag=False, tip_collide=True, tip_legs=(), tip_under=('Tasset', 'Malha'), tail_max_nz=SKO_MAX_NZ,
        hang_under={'belt tail': ('Tasset', 'Malha')},
        tip_leg_follow=1.0, under_min_radial=0.3,      # v7: see the Officer
        tip_lim=OF_TIP_LIM, tip_plumb=True,
        tip_lim2=OF_TIP_LIM2,   # v7: see the Officer
        phys_note='the mail with its lining (main chains), the three plates (Tasset chains), the belt strap on its own chain',
        gap=(0.0, 1.5), free_max=0.8,
        m=dict(src=SOS_BSA + 'windhelm/windhelmarmorheavym_{}.nif', shader_donor=PBR_DONORS + 'windhelm/windhelmarmorheavym_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/windhelm/windhelmarmorheavym_{}.nif', stage=STAGE_M,
               xml=XM + 'WindhelmArmorHeavyM.xml',
               pieces=[('Malha', 'ArmorM_1', ('uvsplit', 0, (1798,), (2077, 2078), (), 2.0, (0.0, 0.0), 62.0, 'mail'), 'skirt:outer'),
                       ('Tasset', 'ArmorM_1', ('islands', 0, {1656: 80, 1416: 56, 1665: 56, 1854: 24, 1826: 16, 1853: 16}, ()), 'skirt:outer@Tasset'),
                       ('Cinto', 'ArmorM_1', ('comps', (1,)), 'belt')],
               expect={}, static=('ArmorM_1',), pants='ArmorM_1', pants_comp=2, drop=(), double_sided=('Malha', 'Tasset', 'Sash'),
               subdiv=('Malha', 'Tasset', 'tip'), slits=True, lining_all=True, sk_belt=70.0, sk_anchor=72.0, ramp=4.0, nrow=5,
               max_chains=14, chain_spacing=26.0, leg_pen=dict(Front=5.5, Back=5.5, Side=3.0),
               top_follow='belt', side_follow=dict(half=45.0, fade=20.0, ztop=49.0, zfade=5.0, free=0.4),
               follow_zones=[dict(centre=0.0, half=35.0, fade=20.0, ztop=52.0, zfade=4.0, free=0.5), dict(centre=180.0, half=35.0, fade=20.0, ztop=52.0, zfade=4.0, free=0.5)],   # v10: as the Officer
               field_src='outer', flare_src='outer', leg_pull_min_gap=0.8, lining_min_gap=0.8, leg_max_nz=0.6,
               field_interp=2.0, cap_pelvis_min=0.05, lining_ride=True,     # v9: as the Officer men's (the lining takes the sheet's weights)
               groups=_wg_groups(0.0, 100.0), layer_coll=_wg_layer_coll(zmax=68.2),
               layer_lift=[(('Tasset', 'Cinto'), dict(under='Malha', clear=0.8, hinge=68.2))], layer_clear=[(('Tasset',), dict(under='Malha', clear=0.8, zmax=68.2, fade=2.0, sigma=2.0))], lining_clear=dict(clear=0.5, fade=1.5, weld_keep=0.5),   # v7c: as the Officer; pivot at its belt band's lower edge
               layer_flare=[('Malha', dict(clear=0.8, full=46.0, top=50.0, src='outer'), False)]),
        f=dict(**_f_set('Sons - 3BA - Windhelm.osp', 'Sons - 3BA - Windhelm - WindhelmArmorHeavyF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\WindhelmArmorHeavyF.xml',
               pieces=[('Malha', 'ArmorF_0', ('uvsplit', 0, (1798,), (2077, 2078), (), 2.0, (0.0, 0.0), 64.5, 'mail'), 'skirt:outer'),
                       ('Tasset', 'ArmorF_0', ('islands', 0, {1656: 80, 1416: 56, 1665: 56, 1854: 24, 1826: 16, 1853: 16}, ()), 'skirt:outer@Tasset'),
                       ('Cinto', 'ArmorF_0', ('comps', (1,)), 'belt')],
               expect={}, static=('ArmorF_0',), pants='ArmorF_0', pants_comp=2, drop=(), double_sided=('Malha', 'Tasset', 'Sash'),
               subdiv=('Malha', 'Tasset', 'tip'), slits=True, lining_all=True, sk_belt=72.5, sk_anchor=74.5, ramp=4.0, nrow=5, tb_clear=0.9,
               max_chains=14, chain_spacing=26.0, leg_pen=dict(Front=5.5, Back=5.5, Side=3.0),
               top_follow='belt', side_follow=dict(half=45.0, fade=20.0, ztop=51.5, zfade=5.0, free=0.4),
               follow_zones=[dict(centre=0.0, half=35.0, fade=20.0, ztop=54.5, zfade=4.0, free=0.5), dict(centre=180.0, half=35.0, fade=20.0, ztop=54.5, zfade=4.0, free=0.5)],
               field_src='outer', flare_src='outer', leg_pull_min_gap=0.8, lining_min_gap=0.8, leg_max_nz=0.6,
               field_interp=2.0, cap_pelvis_min=0.05, lining_ride=True,     # v9: as the Officer men's (the lining takes the sheet's weights)
               groups=_wg_groups(2.5, 100.0), layer_coll=_wg_layer_coll(1.0, zmax=71.2),   # 1.0: the big Lovely Lady build met it at 1 front point with 0.8
               layer_lift=[(('Tasset', 'Cinto'), dict(under='Malha', clear=0.8, hinge=71.2))], layer_clear=[(('Tasset',), dict(under='Malha', clear=0.8, zmax=71.2, fade=2.0, sigma=2.0))], lining_clear=dict(clear=0.5, fade=1.5, weld_keep=0.5),
               layer_flare=[('Malha', dict(clear=0.8, full=48.5, top=52.5, src='outer'), False)]),
    ),
    'Hide': dict(
        prefix='SHD', title='Stormcloak Leather Padded Gambeson (Armors/ArmorHide)',
        phys=PHYS_HIDE, bag=False, tip_collide=True, tip_legs=(), tail_max_nz=SKO_MAX_NZ,
        gap=(0.0, 1.5), free_max=0.85,
        sash_def=HIDE_TAIL_DEF, sash_lim=HIDE_TAIL_LIM, sash_lim2=HIDE_TAIL_LIM,     # the welded tail is a LEATHER belt end
        m=dict(src=SOS_BSA + 'armors/armorhidem_{}.nif', shader_donor=PBR_DONORS + 'armors/armorhidem_1.nif',
               out=STAGE_M + 'meshes/nordwar/sonsofskyrim/armors/armorhidem_{}.nif', stage=STAGE_M,
               xml=XM + 'ArmorsHideM.xml',
               pieces=[('Tail', 'Torso', ('islands', 0, {679: 32, 695: 16}, ()), 'tail'),
                       ('Saia', 'Torso', ('islands', 0, {1354: 313, 1357: 288, 1685: 107, 1686: 91, 370: 87}, (), 72.5), 'skirt:outer')],
               expect=_HD_EXPECT_M, static=('Torso',), pants='Torso', pants_comp=1, drop=(),
               subdiv=('Saia', 'Tail'), slits=False, sk_belt=71.0, sk_anchor=73.0, ramp=8.0),
        f=dict(**_f_set('Sons - 3BA - Armors.osp', 'Sons - 3BA - Armors - ArmorHideF'), stage=STAGE_F,
               xml='SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\ArmorsHideF.xml',
               pieces=[('Tail', 'Torso', ('islands', 0, {737: 32, 753: 16}, ()), 'tail'),
                       ('Saia', 'Torso', ('islands', 0, {2882: 355, 2889: 331, 1758: 107, 1759: 91, 399: 87}, (), 74.0), 'skirt:outer')],
               expect=_HD_EXPECT_F, static=('Torso', '3BA'), pants='Torso', pants_comp=1, drop=(),
               subdiv=('Saia', 'Tail'), slits=False, sk_belt=72.5, sk_anchor=74.5, ramp=8.0, tb_clear=0.9),
    ),
}

# v11 (helmets, 2026-10-11: 'they need collisions against the armor'): every cuirass carries a PUBLIC collider of its outer surface above the
# chest (z > 92: collar, shoulders, chest, back) tagged for the Stormcloak helmets' flap skirts, whose points name the tag from their own
# file - the helmet rides over whichever Sons of Skyrim cuirass is worn (the v1 helmets carried ONE envelope over all cuirasses, pulled
# into a trench round the resting curtain: boxed in, they twitched and barely moved)
_TORSO = dict(zmin=92.0, tag='soscuirass', helm='soshelm', pen=2.0, margin=0.1)
for _d in DESIGNS.values(): _d.setdefault('torso_coll', _TORSO)

# ---------------------------------------------------------------- v12 (2026-10-12): the same strap physics everywhere
# User in game: the Lamellar / Heavy belt tails 'twitching, sitting weirdly, crooked, bending weird', the hip straps and bags 'jitter and
# twitch a lot', the hip strap 'clips and sits under the cloth sash'. Every belt tail takes the Officer's riveted-strap recipe (its v5
# zig-zag was these same .2 / .12 sideways limits) and hangs plumb; every hip strap loop (fixed to the belt at both ends) keeps its
# share on the belt at its ends and sags only in the middle.
for _d in DESIGNS.values():
    _d.setdefault('tip_lim', OF_TIP_LIM); _d.setdefault('tip_lim2', OF_TIP_LIM2); _d.setdefault('tip_plumb', True)
    if 'flap_follow' in _d: _d.setdefault('flap_end_fade', 0.75)
