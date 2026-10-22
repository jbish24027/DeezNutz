"""2026-10-13: give the Picta lane the July automatic depth of field (AMON ENB REBORN's ADOF Kitsuune Edition, drawn by
Bottled Effects 11 before the UI). Steps: build the DOF mod, rebuild the darkening override (EnableDepthOfField=true +
AMON's focusing times), re-sync the Root twin, add the modlist line directly above the override (+ PICTA / Preset Studio,
- in the other profiles that carry the override). Aborts if MO2 or the game is running."""
import os, sys, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = r'C:\1. AUTHORIA'
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5d4e206c-02a2-415b-a991-88488f69ab10\scratchpad'
MOD = 'Authoria - Picta - July Depth of Field (AMON ADOF)'
ANCHOR = 'Authoria - Picta 1.1.2 - Darkened to 1.0.1'
ON = ('DEEZ CS NUTZ - PICTA', 'Authoria - Preset Studio - HPH')
TAG = '.bak-julydof-20261013'


def running():
    out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    return [n for n in ('skyrimse.exe', 'modorganizer.exe', 'skse64_loader.exe') if n in out]


if running():
    sys.exit('ABORT - still running: %s' % running())
for cmd in ([sys.executable, '-I', os.path.join(SCRATCH, 's21_dofmod.py'), '--write'],
            [sys.executable, '-I', os.path.join(HERE, 'picta_darken_v3_full.py'), '--write'],
            [sys.executable, '-I', os.path.join(HERE, 'sync_root_twin.py'), '--write']):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    tail = [l for l in r.stdout.splitlines() if l.strip()][-4:]
    print('>>', os.path.basename(cmd[2]), 'exit', r.returncode); [print('   ', l[:160]) for l in tail]
    if r.returncode:
        print(r.stderr[-1500:]); sys.exit('ABORT - step failed')
for prof in sorted(os.listdir(os.path.join(ROOT, 'profiles'))):
    ml = os.path.join(ROOT, 'profiles', prof, 'modlist.txt')
    if not os.path.isfile(ml):
        continue
    raw = open(ml, 'rb').read(); eol = b'\r\n' if b'\r\n' in raw else b'\n'
    lines = raw.split(eol); names = [l[1:].decode('utf-8', 'replace') for l in lines]
    if MOD in names:
        print('  %-44s already has it' % prof); continue
    if ANCHOR not in names:
        continue
    idx = names.index(ANCHOR); flag = b'+' if prof in ON else b'-'
    lines.insert(idx, flag + MOD.encode('utf-8'))
    if not os.path.exists(ml + TAG):
        shutil.copy2(ml, ml + TAG)
    open(ml, 'wb').write(eol.join(lines))
    print('  %-44s %s at line %d' % (prof, flag.decode(), idx + 1))
ini = open(os.path.join(ROOT, 'mods', ANCHOR, 'enbseries.ini'), 'rb').read()
print('override enbseries.ini EnableDepthOfField=true:', b'EnableDepthOfField=true' in ini)
print('DOF files:', sorted(os.listdir(os.path.join(ROOT, 'mods', MOD, 'enbseries'))))
print('DONE')
