# WORKED EXAMPLE for cuirass_collider.py: the 15 men's hold-guard cuirasses of NordwarUA's Sons of Skyrim 2.0 (2026-10-12) - nine from the BSA with
# no physics (a minimal XML), six carrying the author's ported physics (the mod's nif + XML, extended). Copy per project; paths are this user's.
# Sons of Skyrim 2.0 HOLD cuirasses (men) for cuirass_collider.py: every one gets a public collider of its outer surface above the
# chest (tag soscuirass, naming soshelm) so the hold helmets' flap skirts ride over it - the same cross-file collision the coat builder
# gives the Stormcloak cuirasses (torso_coll). Six of them carry the author's ported physics (the SMP mod's nif + XML: those are the
# sources, the XML is extended); the other nine come from the BSA with no physics of their own (a minimal XML). Shaders from the frozen
# PG copies in pbr_donors/<hold>/. 2026-10-12. Women's hold cuirasses: not done (the family pass).
# Run: cuirass_collider.py <this file> [name ...]; install with install_helmets.py <this file> <label> (same STAGE / MOD / BACKUPS keys).
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__)).replace(_os.sep, '/') + '/'
BSA = 'C:/Users/earln/AppData/Local/Temp/claude/E--claude-work/9108c909-c715-411b-bdd8-c8748f38a3e2/scratchpad/sos_bsa/meshes/nordwar/sonsofskyrim/'
MODS = 'E:/Modlists/LoreRim/mods/'
MOD = MODS + '[NoDelete] Sons of Skyrim 2.0 - SMP Physics/'
MODM = MOD + 'meshes/nordwar/sonsofskyrim/'
MODX = MOD + 'SKSE/Plugins/hdtSkinnedMeshConfigs/SonsOfSkyrimSMP/'
PGD = _HERE + 'pbr_donors/'
STAGE = _HERE + 'stage/holds/'
XD = 'SKSE\\Plugins\\hdtSkinnedMeshConfigs\\SonsOfSkyrimSMP\\'
WORK = _HERE
BACKUPS = 'C:/Users/earln/.claude/projects/E--claude-work/backups/'
_M = 'meshes/nordwar/sonsofskyrim/'


def _new(hold, stem, xml):
    return dict(src=BSA + f'{hold}/{stem}{{}}.nif', donor=PGD + f'{hold}/{stem}{{}}.nif', out=_M + f'{hold}/{stem}{{}}.nif', xml=None, xml_out=XD + xml)


def _ported(hold, stem, xml):
    return dict(src=MODM + f'{hold}/{stem}{{}}.nif', donor=PGD + f'{hold}/{stem}{{}}.nif', out=_M + f'{hold}/{stem}{{}}.nif', xml=MODX + xml, xml_out=XD + xml)


CUIRASSES = {
    # no physics of their own (the BSA mesh)
    'DawnstarArmor': _new('dawnstar', 'armorm', 'DawnstarArmorM.xml'),               # The Pale Guard Armor (0_Dawnstar_Armor_Light_AA)
    'DawnstarArmorHeavy': _new('dawnstar', 'armorheavym', 'DawnstarArmorHeavyM.xml'),
    'FalkreathArmor': _new('falkreath', 'armorm', 'FalkreathArmorM.xml'),
    'FalkreathArmorHeavy': _new('falkreath', 'armorheavym', 'FalkreathArmorHeavyM.xml'),
    'MarkarthArmor': _new('markarth', 'armorm', 'MarkarthArmorM.xml'),
    'MarkarthArmorHeavy': _new('markarth', 'armorheavym', 'MarkarthArmorHeavyM.xml'),
    'MorthalArmor': _new('morthal', 'armorm', 'MorthalArmorM.xml'),                   # (the plugin calls this one the heavy; by mesh)
    'RiftenArmorLight': _new('riften', 'armorlightm', 'RiftenArmorLightM.xml'),
    'WhiterunArmor': _new('whiterun', 'armorm', 'WhiterunArmorM.xml'),
    # the author's physics, ported 2026-10-04 (the SMP mod's own nif + XML)
    'WinterholdArmor': _ported('winterhold', 'armorm', 'WinterholdArmorM.xml'),
    'SolitudeArmorHeavy': _ported('solitude', 'armorheavym', 'SolitudeHeavyM.xml'),
    'SolitudeArmor': _ported('solitude', 'armorm', 'SolitudeArmorM.xml'),
    'MorthalArmorHeavy': _ported('morthal', 'armorheavym', 'MorthalHeavyM.xml'),
    'WhiterunArmorHeavy': _ported('whiterun', 'armorheavym', 'WhiterunHeavyM.xml'),
    'RiftenArmor': _ported('riften', 'armorm', 'RiftenArmorM.xml'),
}
