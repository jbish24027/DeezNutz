# WORKED EXAMPLE for the helmet builder: 26 helmets of NordwarUA's Sons of Skyrim 2.0: the ten Stormcloak-side ones and the 16 hold-guard ones (v4, 2026-10-12: settled off the cuirass colliders) (flap skirts
# welded into the bowl, a closed mail veil, hinged iron cheek guards, welded ear flaps; colliders vs the wearer's body and the
# Sons of Skyrim cuirasses' own public colliders, written by the coat builder's torso_coll and matched across files by tag). Copy per project; run: python build_helmet_rig.py <this file> [helmet ...]
# then helmet_check.py / render_helmets.py / install_helmets.py with the same file.
# Sons of Skyrim 2.0 helmets for the helmet builder (scripts/helmet/build_helmet_rig.py): the Stormcloak six first (user 2026-10-11:
# 'copying what we did for RA helmets and adding physics to the leather flaps and the cheek guards ... there aren't really any collars
# so ... make them more flowier'). Survey (survey/helmets_overview*.png): every SoS helmet has a flap skirt WELDED into the bowl
# (texture islands; the author fades Head -> Spine2 down it), some have cheek guards: the heavy iron helmet a hinged welded pair
# with knuckles, the Officer ear flaps as islands welded into the bowl.
# Run with the helmet builder's names in scope (this file is executed inside it): build_helmet_rig.py <this file> [helmet ...]
import os as _os, sys as _sys, json as _json
_HERE = _os.path.dirname(_os.path.abspath(__file__)).replace(_os.sep, '/') + '/'
SRC_ROOT = 'C:/Users/earln/AppData/Local/Temp/claude/E--claude-work/9108c909-c715-411b-bdd8-c8748f38a3e2/scratchpad/sos_bsa/meshes/nordwar/sonsofskyrim/'
DONOR_ROOT = _HERE + 'pbr_donors/'                    # frozen copies of the PG-patched meshes (shader blocks); geometry from the BSA
STAGE = _HERE + 'stage/helmets/'                      # its own stage tree (the coat stage's diff never sees it); installed into MOD
XD = 'SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\'
WORK = _HERE
MODS = 'E:/Modlists/LoreRim/mods/'
MOD = MODS + '[NoDelete] Sons of Skyrim 2.0 - SMP Physics/'     # the men's SMP mod holds every helmet variant (helmets are not BodySlide-built)
BACKUPS = 'C:/Users/earln/.claude/projects/E--claude-work/backups/'
CA = 'meshes/actors/character/character assets/'
BODY = {'m': MODS + '[NoDelete] Himbo M&V Vanilla output/' + CA + 'malebody_1.nif', 'm0': MODS + '[NoDelete] Himbo M&V Vanilla output/' + CA + 'malebody_0.nif',
        'f': MODS + '[NoDelete] Bodyslide output 2/' + CA + 'femalebody_1.nif', 'f0': MODS + '[NoDelete] Bodyslide output 2/' + CA + 'femalebody_0.nif'}
# the cuirasses the helmets are worn with: our built Sons of Skyrim coats + guards (men: the stage _1 builds; women: the 3BA ShapeData
# builds), with their physics prefixes so hidden shapes and physics points stay out of the envelope
_coat = 'C:/Users/earln/.claude/skills/authoring-smp-armor-physics/scripts/coat/'
if _coat not in _sys.path: _sys.path.insert(0, _coat)
import build_coat_rig as _W
_W.use_designs(_HERE + 'sos_designs.py')
_rep = _json.load(open(_HERE + 'rework_report.json'))
# (design, built cuirass nif, its physics prefix, its XML) - v2: only helmet_check reads these (the helmets meet the cuirasses' own public
# 'Torso Collide' copies across files; the v1 envelope built from them is gone)
_xml = lambda d, g: _W.DESIGNS[d][g]['stage'] + _W.DESIGNS[d][g]['xml'].replace('\\', '/')
COLLARS = {'m': [(d, [o for o in r['m']['outs'] if o.endswith('_1.nif')][0], _W.DESIGNS[d]['prefix'], _xml(d, 'm')) for d, r in _rep.items() if 'm' in r and d in _W.DESIGNS],
           'm0': [(d, [o for o in r['m']['outs'] if o.endswith('_0.nif')][0], _W.DESIGNS[d]['prefix'], _xml(d, 'm')) for d, r in _rep.items() if 'm' in r and d in _W.DESIGNS],
           'f': [(d, r['f']['outs'][0], _W.DESIGNS[d]['prefix'], _xml(d, 'f')) for d, r in _rep.items() if 'f' in r and d in _W.DESIGNS]}
_V7 = ('m', 'ma', 'mk', 'mo', 'f', 'fa', 'fk')
_V01 = ('m_1', 'm_0', 'ma_1', 'ma_0', 'mk_1', 'mk_0', 'mo_1', 'mo_0', 'f_1', 'f_0', 'fa_1', 'fa_0', 'fk_1', 'fk_0')
HELMETS = {
    'Stormcloak1': dict(prefix='SH1', title='Sons of Skyrim - Stormcloak Helmet (windhelm1)', src='helmets/windhelm1_{}.nif', variants=_V7, xml='StormcloakHelmet1', cheeks=None),
    'Stormcloak2': dict(prefix='SH2', title='Sons of Skyrim - Stormcloak Helmet, mail veil (windhelm2)', src='helmets/windhelm2_{}.nif', variants=_V7, xml='StormcloakHelmet2', cheeks=None),
    'IronHeavy': dict(prefix='SIH', title='Sons of Skyrim - Iron Helmet, heavy (hinged cheek guards)', src='helmets/ironhelmeth_{}.nif', variants=_V7, xml='IronHelmetHeavy', cheeks='hinge'),
    # IronLight = helmets/ironhelmetl = 'Stormcloak Nasal Iron Helmet with Coif': its coif hangs free round the back and sides - restored 2026-10-12
    # (dropped 2026-10-11 on 'the stormcloak nasal light helmet doesn't need any smp because of how the helmet is', which by its in-game name
    # is the Stormcloak LIGHT Nasal Iron Helmet = helmets/iron1, whose mail is a hood hugging the neck - that one stays rigid, see below)
    'IronLight': dict(prefix='SIL', title='Sons of Skyrim - Stormcloak Nasal Iron Helmet with Coif (helmets/ironhelmetl)', src='helmets/ironhelmetl_{}.nif', variants=_V7, xml='IronHelmetCoif', cheeks=None),
    'Eastmarch': dict(prefix='SEH', title='Sons of Skyrim - Eastmarch Guard Helmet', src='windhelm/helmet{}.nif', variants=_V01, xml='EastmarchHelmet', cheeks=None),
    'Officer': dict(prefix='SOH', title='Sons of Skyrim - Stormcloak Officer Helmet', src='windhelm/officerhelmet{}.nif',
                    variants=('m_1', 'm_0', 'mk_1', 'mk_0', 'mo_1', 'mo_0', 'f_1', 'f_0', 'fk_1', 'fk_0', '_ma', '_fa'), xml='OfficerHelmet', cheeks=None,
                    closed=True,        # the veil runs all round (a seam at the front centre read as a gap): chains round the full circle, linked round
                    guard_phys_min=0.3,    # v4: the pelt's first row under the welded rim (share .18-.24) lies ON the Dawnstar / Falkreath / Winterhold collars and cannot be settled - not collision points
                    settle_pin=1.0),       # v4: and the rows right under the rim may move (the collars rise to the rim here; the rim row itself stays welded)
                                        # cheeks: none (2026-10-12: the 'ear flaps' are painted panels welded to the bowl all round - hinging them tore it)
    # the other Stormcloak helmets (2026-10-12, user: 'you didn't do most of the stormcloak helmets'; survey/stormcloak_rest_overview.png):
    # hide = ear / neck flaps, conical leather + nasal leather + nasal iron (iron2) = a neck guard / coif round the back and sides. The Stormcloak
    # Light Nasal Iron Helmet (helmets/iron1) is a mail HOOD hugging the head and neck (591 pts on Spine2, nothing hangs free) - left rigid.
    'Hide': dict(prefix='SHD', title='Sons of Skyrim - Stormcloak Light Hide Helmet (helmets/hide)', src='helmets/hide_{}.nif', variants=_V7, xml='StormcloakHideHelmet', cheeks=None),
    'ConicalLeather': dict(prefix='SCL', title='Sons of Skyrim - Stormcloak Nasal Conical Leather Helmet (helmets/conicalleather)', src='helmets/conicalleather_{}.nif', variants=_V7, xml='StormcloakConicalLeatherHelmet', cheeks=None),
    'IronLeather': dict(prefix='SNL', title='Sons of Skyrim - Stormcloak Nasal Leather Helmet (helmets/ironleather)', src='helmets/ironleather_{}.nif', variants=_V7, xml='StormcloakNasalLeatherHelmet', cheeks=None),
    'Iron2': dict(prefix='SNI', title='Sons of Skyrim - Stormcloak Nasal Iron Helmet (helmets/iron2)', src='helmets/iron2_{}.nif', variants=_V7, xml='StormcloakNasalIronHelmet', cheeks=None),
}

# ---------------------------------------------------------------- the hold-guard helmets (2026-10-12, user: 'check out the rest of the helmets')
# Survey (survey/hold_helmets_survey.txt, hold_helmets_overview.png): every bowl carries the author's Head -> Spine2 fade down a flap skirt
# round the back and sides; mirrored welded cheek pairs on the Dawnstar light (102 pts), Solitude heavy (182) and Winterhold (197) - the
# visors / nasals at the front are single pieces (Head 1.0, rigid); the Riften plume (Box004) lies flat ON the bowl's ridge (454 of 740
# pts within 1.0 of it) - left alone; the Whiterun heavy horsetail (HorseTail_M, 1152 pts, Head -> Spine2 faded along the strands) hangs
# as a crest on one chain. The Morthal light / heavy and the Whiterun light / medium are the same mesh under two names.
_V9 = ('m_1', 'm_0', 'f_1', 'f_0', '_ma', '_mk', '_mo', '_fa', '_fk')      # the mixed scheme (humans _0 / _1, the other races one mesh)
HELMETS.update({
    'DawnstarLight': dict(prefix='DSL', title='Sons of Skyrim - The Pale Guard Helmet (dawnstar/helmet)', src='dawnstar/helmet_{}.nif', variants=_V7, xml='DawnstarHelmetLight', cheeks='hinge'),
    'DawnstarHeavy': dict(prefix='DSH', title='Sons of Skyrim - The Pale Heavy Helmet (dawnstar/helmetheavy)', src='dawnstar/helmetheavy{}.nif', variants=_V9, xml='DawnstarHelmetHeavy', cheeks=None),
    'FalkreathLight': dict(prefix='FKL', title='Sons of Skyrim - Falkreath Guard Helmet (falkreath/helmet)', src='falkreath/helmet_{}.nif', variants=_V7, xml='FalkreathHelmetLight', cheeks=None),
    'FalkreathHeavy': dict(prefix='FKH', title='Sons of Skyrim - Falkreath Guard Heavy Helmet (falkreath/helmetheavy)', src='falkreath/helmetheavy{}.nif', variants=_V9, xml='FalkreathHelmetHeavy', cheeks=None),
    'MarkarthLight': dict(prefix='MKL', title='Sons of Skyrim - The Reach Guard Helmet (markarth/helmet)', src='markarth/helmet_{}.nif', variants=_V7, xml='MarkarthHelmetLight', cheeks=None),
    'MarkarthHeavy': dict(prefix='MKH', title='Sons of Skyrim - The Reach Guard Heavy Helmet (markarth/heavyhelmet)', src='markarth/heavyhelmet_{}.nif', variants=_V7, xml='MarkarthHelmetHeavy', cheeks=None),
    'MorthalLight': dict(prefix='MOL', title='Sons of Skyrim - Hjaalmarch Guard Helmet (morthal/helmet)', src='morthal/helmet_{}.nif', variants=_V7, xml='MorthalHelmetLight', cheeks=None),
    'MorthalHeavy': dict(prefix='MOH', title='Sons of Skyrim - Hjaalmarch Guard Heavy Helmet (morthal/helmetheavy)', src='morthal/helmetheavy_{}.nif', variants=_V7, xml='MorthalHelmetHeavy', cheeks=None),
    'RiftenHeavy': dict(prefix='RFH', title='Sons of Skyrim - The Rift Guard Heavy Helmet (riften/helmet, horsehair plume)', src='riften/helmet{}.nif', variants=_V9 + ('_fo',), xml='RiftenHelmetHeavy', cheeks=None,
                        crest=dict(shape='Box004', n=5, chains=1)),      # v5 (user): the plume hangs down the back of the bowl on one chain, colliding with the bowl
    'RiftenLight': dict(prefix='RFL', title='Sons of Skyrim - The Rift Guard Helmet (riften/helmetlight, horsehair plume)', src='riften/helmetlight_{}.nif', variants=_V7, xml='RiftenHelmetLight', cheeks=None,
                        crest=dict(shape='Box004', n=5, chains=1)),
    'SolitudeHeavy': dict(prefix='SHH', title='Sons of Skyrim - Haafingar Guard Heavy Helmet (solitude/helmet)', src='solitude/helmet_{}.nif', variants=_V7, xml='SolitudeHelmetHeavy', cheeks='hinge'),
    'SolitudeLight': dict(prefix='SHL', title='Sons of Skyrim - Haafingar Guard Helmet (solitude/helmetlight)', src='solitude/helmetlight_{}.nif', variants=_V7, xml='SolitudeHelmetLight', cheeks=None),
    'WhiterunHeavy': dict(prefix='WRH', title='Sons of Skyrim - Whiterun Heavy Decorated Helmet (whiterun/helmet, horsetail crest)', src='whiterun/helmet_{}.nif', variants=_V7, xml='WhiterunHelmetHeavy', cheeks=None,
                          crest=dict(shape='HorseTail_M', n=5, chains=3)),   # v5 (user: 'like the RA one'): three chains side by side down the tail, colliding with the bowl
    'WhiterunLight': dict(prefix='WRL', title='Sons of Skyrim - Whiterun Guard Helmet (whiterun/helmetlight)', src='whiterun/helmetlight_{}.nif', variants=_V7, xml='WhiterunHelmetLight', cheeks=None),
    'WhiterunMedium': dict(prefix='WRM', title='Sons of Skyrim - Whiterun Heavy Helmet (whiterun/helmetlight2)', src='whiterun/helmetlight2_{}.nif', variants=_V7, xml='WhiterunHelmetMedium', cheeks=None),
    'Winterhold': dict(prefix='WHL', title='Sons of Skyrim - Winterhold Guard Helmet (winterhold/helmet)', src='winterhold/helmet_{}.nif', variants=_V7, xml='WinterholdHelmet', cheeks='hinge'),
})
# the hold cuirasses' colliders (cuirass_collider.py on sos_hold_cuirasses.py) join the check's list (men only: the hold women's cuirasses are not done)
_hc = _HERE + 'cuirass_colliders_report.json'
if _os.path.exists(_hc):
    for _n, _r in _json.load(open(_hc)).items():
        for _wt, _g in (('_1', 'm'), ('_0', 'm0')):
            if _wt in _r['variants']: COLLARS[_g].append((_n, _r['variants'][_wt]['out'], 'HC', _HERE + 'stage/holds/' + _r['xml'].replace('\\', '/')))
