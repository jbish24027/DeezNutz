"""Generate LANE-STATE.md from the live PICTA profile: lane mods in priority order + plugin slots."""
import os, re, sys

INSTANCE = r'C:\1. AUTHORIA'
PROFILE = os.path.join(INSTANCE, 'profiles', 'DEEZ CS NUTZ - PICTA')
OUT = sys.argv[1]

LANE_RE = re.compile(
    r'picta|bottled|enb extender|kiloader|effects 11|soul core|silent horizons|community shaders|reshade|'
    r'skyrim upscaler|dlss-unlocked|dynamicshaderframegen|enb frame generation|helios|astralite|kreate|'
    r'sky meshes|nordic winds|enb binary|enb worldspace|enb terrain|enb anti|enb light inv|enb light det|'
    r'terrain helper for enb|dalc fix|snowy holds|gray cowl - astralite|mists of tamriel|nat\.enb|nat-enb|'
    r'enhanced volumetric lighting|seasonal weathers framework|universal weather|no reseat|wanderers fair - picta|'
    r'northman|visuals - enb|visuals - weather|reverb interior sounds - ',
    re.I)

PLUGINS = [
    'Picta - Weathers of Aurbis.esm',
    'Picta - Weathers of Skyrim.esp',
    'Authoria - Picta over NAT.esp',
    'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp',
    'Picta Aurbis - Nordic Winds - Patch.esp',
    'Authoria - Patch - Wanderers Fair - Picta Climate.esp',
    'Authoria - Patch - Picta Seasonal.esp',
    'Helios_Astralite.esp',
    'Helios_Astralite_Seasonal.esp',
    'Helios_Astralite_Radiant.esp',
    'Helios_NAT III.esp',
    'Helios_NAT III_Seasonal.esp',
    'Helios_NAT III_Radiant.esp',
    'Authoria - Patch - Remove Interior Fog - Lux.esp',
    'Authoria - Patch - Reverb Interior Sounds - NAT-ENB.esp',
    'Authoria - Patch - Reverb Interior Sounds - Astralite.esp',
    'Beyond Skyrim Bruma - Universal Weather Compatibility.esp',
    'NAT-CS.ENB.esp',
    'Seasonal Weathers Framework.esp',
    'Mists of Tamriel.esp',
    'Helios.esp',
]


def read(name):
    with open(os.path.join(PROFILE, name), encoding='utf-8-sig') as f:
        return [l.rstrip('\r\n') for l in f if l.strip()]


modlist = read('modlist.txt')
plugins = read('plugins.txt')
loadorder = read('loadorder.txt')
active = {l[1:] for l in plugins if l.startswith('*')}
listed = {l.lstrip('*') for l in plugins if not l.startswith('#')}

out = []
out.append('# Lane state - profile `DEEZ CS NUTZ - PICTA`, read live on 2026-10-15')
out.append('')
out.append('Generated from the profile files in `reference/profile-snapshot/`. This is the ordering authority.')
out.append('')
out.append('## Mods (MO2 priority order: first row wins conflicts = bottom of the MO2 left pane)')
out.append('')
out.append('Only the rows that belong to the Picta / Bottled / ENB / weather lane are shown; `+` enabled, `-` disabled,')
out.append('`_separator` rows mark the MO2 separators they sit under. Row = line number in modlist.txt.')
out.append('')
out.append('| row | state | mod |')
out.append('|---:|:---:|---|')
for i, l in enumerate(modlist, 1):
    if l.startswith('#'):
        continue
    name = l[1:]
    if LANE_RE.search(name):
        out.append('| %d | %s | %s |' % (i, l[0], name.replace('|', '\\|')))
out.append('')
out.append('## Plugins (loadorder.txt slot = the active plugin directly above it)')
out.append('')
out.append('| plugin | in plugins.txt | active | loadorder line | directly after |')
out.append('|---|:---:|:---:|---:|---|')
pos = {p: i for i, p in enumerate(loadorder)}
for p in PLUGINS:
    if p not in pos:
        out.append('| %s | no | - | - | (not in this profile) |' % p)
        continue
    i = pos[p]
    j = i - 1
    while j >= 0 and loadorder[j] not in active:
        j -= 1
    anchor = loadorder[j] if j >= 0 else '(top)'
    out.append('| %s | %s | %s | %d | %s |' % (
        p, 'yes' if p in listed else 'no', 'yes' if p in active else 'NO', i + 1, anchor))
out.append('')
out.append('## Counts')
out.append('')
out.append('- mods enabled: %d of %d lines' % (sum(1 for l in modlist if l.startswith('+')), len(modlist)))
out.append('- plugins active: %d; listed: %d' % (len(active), len(listed)))
out.append('')
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(out))
print('\n'.join(out))
