"""Re-sync the Root Builder twin of the Picta preset inis from the Data copy.

Effects 11 (Bottled Shaders) reads and SAVES the preset in Data\\enbseries (the shipped Picta Data mod, or
overwrite if the editor wrote a new file there). The ENB Extender compiles from <game root>\\enbseries, which
Root Builder deploys from 'Authoria - Picta ENB - Root twin'. If the Extender reads compile-time options from
the root .fx.ini, the two copies must match, so run this after any editor save and before the next launch.

usage: python sync_root_twin.py          (report only)
       python sync_root_twin.py --write  (copy changed files into the twin; MO2 and the game must be closed)
"""
import os, sys, hashlib, shutil, subprocess

INSTANCE = r'C:\1. AUTHORIA'
DATA_MOD = os.path.join(INSTANCE, 'mods', '[NoDelete] Picta ENB 1.1.2 - Data (shipped)')
OVERWRITE = os.path.join(INSTANCE, 'overwrite')
# 2026-10-12: the darkened-grade override sits above the Data mod; when it is enabled in the PICTA profile its copy is what
# Effects 11 reads, so the twin must mirror it. Precedence: overwrite > OVERRIDE_MOD (if enabled) > DATA_MOD.
OVERRIDE_MOD = os.path.join(INSTANCE, 'mods', 'Authoria - Picta 1.1.2 - Darkened to 1.0.1')
PICTA_MODLIST = os.path.join(INSTANCE, 'profiles', 'DEEZ CS NUTZ - PICTA', 'modlist.txt')


def override_enabled():
    try:
        return ('+' + os.path.basename(OVERRIDE_MOD)) in open(PICTA_MODLIST, encoding='utf-8-sig').read().splitlines()
    except OSError:
        return False
TWIN = os.path.join(INSTANCE, 'mods', 'Authoria - Picta ENB - Root twin', 'Root')
FILES = ['enbseries.ini', r'enbseries\enbeffect.fx.ini', r'enbseries\enbbloom.fx.ini',
         r'enbseries\enbadaptation.fx.ini', r'enbseries\enbeffectpostpass.fx.ini']


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def closed():
    out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    return not any(x in out for x in ('modorganizer.exe', 'skyrimse.exe', 'skse64_loader.exe'))


write = '--write' in sys.argv
if write and not closed():
    sys.exit('MO2 or the game is running; close them first')
changed = 0
for rel in FILES:
    src = os.path.join(OVERWRITE, rel)
    where = 'overwrite'
    if not os.path.isfile(src) and override_enabled() and os.path.isfile(os.path.join(OVERRIDE_MOD, rel)):
        src = os.path.join(OVERRIDE_MOD, rel)
        where = 'override'
    if not os.path.isfile(src):
        src = os.path.join(DATA_MOD, rel)
        where = 'Data mod'
    dst = os.path.join(TWIN, rel)
    same = os.path.isfile(dst) and md5(src) == md5(dst)
    print('%-38s source: %-9s %s' % (rel, where, 'in sync' if same else 'DIFFERS'))
    if not same:
        changed += 1
        if write:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print('   copied into the twin')
print('files out of sync:', changed, '(written)' if write and changed else '')
