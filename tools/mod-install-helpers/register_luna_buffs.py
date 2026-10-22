"""Register the mod folder 'Authoria - Luna Weapon Buffs' (SkyPatcher INI only, no plugin) in every
MO2 profile's modlist.txt: enabled in the four play profiles, disabled in the two Requiem Reforged
profiles, placed directly below 'Authoria - Requiem - Companions Giant' (another INI-only Authoria mod).
No plugin => loadorder/plugins/plugingroups untouched, no Wheeler reindex needed.

usage: python register_luna_buffs.py [--apply]   (dry run by default; backups modlist.txt.bak-lunabuffs-20260906)
"""
import os, shutil, sys

ROOT = r"C:\1. AUTHORIA\profiles"
TAG = 'bak-lunabuffs-20260906'
MOD = 'Authoria - Luna Weapon Buffs'
ANCHOR = 'Authoria - Requiem - Companions Giant'
ENABLED = {'DEEEZ NUTTZZZ', 'DEEZ CS NUTZ', 'DEEZ CS NUTZ - PBR', 'PICTA EXPERIMENT'}
DISABLED = {'Authoria - Requiem Reforged - Main Profile', 'Authoria - Requiem Reforged - NSFW Profile'}
APPLY = '--apply' in sys.argv

assert os.path.isdir(os.path.join(r"C:\1. AUTHORIA\mods", MOD)), 'mod folder missing'
for prof in sorted(os.listdir(ROOT)):
    pdir = os.path.join(ROOT, prof)
    if not os.path.isdir(pdir) or prof not in ENABLED | DISABLED:
        continue
    p = os.path.join(pdir, 'modlist.txt')
    raw = open(p, 'rb').read()
    assert b'\r\n' in raw, p
    lines = raw.decode('utf-8').split('\r\n')
    stray = [l for l in lines if l[1:] == MOD]
    lines = [l for l in lines if l[1:] != MOD]
    idx = [i for i, l in enumerate(lines) if l[1:] == ANCHOR]
    assert len(idx) == 1, (prof, ANCHOR, len(idx))
    sign = '+' if prof in ENABLED else '-'
    lines.insert(idx[0] + 1, sign + MOD)
    print('%-45s %s%s at line %d (below %s%s), stray removed %d' % (prof, sign, MOD, idx[0] + 2, lines[idx[0]][0], ANCHOR, len(stray)))
    if APPLY:
        bak = p + '.' + TAG
        if not os.path.exists(bak):
            shutil.copy2(p, bak)
        open(p, 'wb').write('\r\n'.join(lines).encode('utf-8'))
print('APPLIED' if APPLY else 'DRY RUN')
