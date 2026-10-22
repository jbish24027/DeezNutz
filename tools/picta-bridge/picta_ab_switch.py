"""Picta A/B switch for the PICTA + Preset Studio lanes: `to101` = run the old Picta 1.0.1 weathers + 1.0.1 ENB data (Nordic
Winds patch off, fair patch and clouds.nif back to their 1.0.1 versions, Root twin re-synced); `to111` = back to 1.1.1/1.1.2.
Every file it touches is backed up once (.bak-pictaab-20261012). Refuses to run with MO2 or the game open."""
import os, sys, shutil, subprocess, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
MODE = sys.argv[1] if len(sys.argv) > 1 else 'status'
INST = r'C:\1. AUTHORIA'; MODS = os.path.join(INST, 'mods'); PROFILES = ['DEEZ CS NUTZ - PICTA', 'Authoria - Preset Studio - HPH']
ON_101 = ['[NoDelete] Picta ENB 1.0.1 - Data (shipped)', '[NoDelete] Picta - Weathers of Aurbis 1.0.1 (shipped)']
ON_111 = ['[NoDelete] Picta ENB 1.1.2 - Data (shipped)', '[NoDelete] Picta - Weathers of Aurbis 1.1.1 (shipped)']
# The Nordic Winds patch MOD stays enabled in both states; only its esp is starred/unstarred. (MO2 drops the plugin line from
# plugins/loadorder/plugingroups when the mod is disabled and it is opened - learned 2026-10-12, repaired by s15_nordic_fix.py.)
NORDIC_MOD = '[NoDelete] Picta Aurbis - Nordic Winds - Patch 1.1.1 (shipped)'
NORDIC_ESP = 'Picta Aurbis - Nordic Winds - Patch.esp'
FAIR = os.path.join(MODS, 'houseCARL - Authoria - Patch - Wanderers Fair - Picta Climate', 'Authoria - Patch - Wanderers Fair - Picta Climate.esp')
FAIR_101 = FAIR + '.bak-picta101-20261012'; FAIR_111 = FAIR + '.bak-picta111-ab'
CLOUDS = os.path.join(MODS, '[NoDelete] Picta - Assets 4K', 'meshes', 'sky', 'clouds.nif')
CLOUDS_101 = CLOUDS + '.shipped-101.bak-picta111-20261012'; CLOUDS_111 = CLOUDS + '.shipped-111.bak-ab'
SYNC = os.path.join(INST, '_tools', 'picta-bridge', 'sync_root_twin.py')
DATA_101 = "DATA_MOD = os.path.join(INSTANCE, 'mods', '[NoDelete] Picta ENB 1.0.1 - Data (shipped)')"
DATA_111 = "DATA_MOD = os.path.join(INSTANCE, 'mods', '[NoDelete] Picta ENB 1.1.2 - Data (shipped)')"

def running():
    out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    return 'modorganizer' in out or 'skyrimse' in out
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def rw(path, fn):
    raw = open(path, 'rb').read(); eol = b'\r\n' if raw.count(b'\r\n') >= raw.count(b'\n') // 2 else b'\n'
    trailing = raw.endswith(eol); lines = (raw[:-len(eol)] if trailing else raw).split(eol)
    bak = path + '.bak-pictaab-20261012'
    if not os.path.exists(bak): shutil.copy2(path, bak)
    lines = fn([l.decode('utf-8') for l in lines])
    open(path, 'wb').write(eol.join(l.encode('utf-8') for l in lines) + (eol if trailing else b''))

def set_mods(lines, on, off):
    names = {l[1:] for l in lines}
    for n in on + off: assert n in names, 'modlist lacks ' + n
    return [('+' if l[1:] in on else '-' if l[1:] in off else l[0]) + l[1:] if l[1:] in on + off else l for l in lines]
def set_plugin(lines, name, active):
    out = []; hit = 0
    for l in lines:
        if l.lstrip('*') == name: out.append(('*' if active else '') + name); hit += 1
        else: out.append(l)
    assert hit == 1, 'plugin line count %d for %s' % (hit, name); return out

def status():
    for p in PROFILES:
        ml = open(os.path.join(INST, 'profiles', p, 'modlist.txt'), encoding='utf-8').read().splitlines()
        pl = open(os.path.join(INST, 'profiles', p, 'plugins.txt'), encoding='utf-8').read().splitlines()
        st = {l[1:]: l[0] for l in ml if l[1:] in ON_101 + ON_111 + [NORDIC_MOD]}
        print('%-34s mods: %s | nordic esp: %s' % (p, ' '.join('%s%s' % (st[n], n.split('Picta')[1].strip()[:28]) for n in ON_101 + ON_111 + [NORDIC_MOD]), 'ON' if ('*' + NORDIC_ESP) in pl else 'off'))
    print('fair patch bytes: %d (356 = 1.0.1 build, 488 = 1.1.1 build)' % os.path.getsize(FAIR))
    print('clouds.nif = 1.0.1 shipped: %s' % (md5(CLOUDS) == md5(CLOUDS_101)))
    print('twin sync constant: %s' % ('1.1.2' if DATA_111 in open(SYNC, encoding='utf-8').read() else '1.0.1' if DATA_101 in open(SYNC, encoding='utf-8').read() else '??'))

if MODE == 'status': status(); sys.exit()
assert MODE in ('to101', 'to111')
if running(): sys.exit('MO2 or the game is running - aborting')
to101 = MODE == 'to101'
for p in PROFILES:
    rw(os.path.join(INST, 'profiles', p, 'modlist.txt'), lambda L: set_mods(L, (ON_101 if to101 else ON_111) + [NORDIC_MOD], ON_111 if to101 else ON_101))
    rw(os.path.join(INST, 'profiles', p, 'plugins.txt'), lambda L: set_plugin(L, NORDIC_ESP, not to101))
# fair patch
if to101:
    if not os.path.exists(FAIR_111): shutil.copy2(FAIR, FAIR_111)
    shutil.copy2(FAIR_101, FAIR)
else:
    shutil.copy2(FAIR_111, FAIR)
# clouds
if to101:
    if not os.path.exists(CLOUDS_111): shutil.copy2(CLOUDS, CLOUDS_111)
    shutil.copy2(CLOUDS_101, CLOUDS)
else:
    shutil.copy2(CLOUDS_111, CLOUDS)
# root twin
src = open(SYNC, encoding='utf-8').read(); bak = SYNC + '.bak-pictaab-20261012'
if not os.path.exists(bak): shutil.copy2(SYNC, bak)
src2 = src.replace(DATA_111, DATA_101) if to101 else src.replace(DATA_101, DATA_111)
assert (DATA_101 if to101 else DATA_111) in src2
open(SYNC, 'w', encoding='utf-8', newline='').write(src2)
r = subprocess.run([sys.executable, SYNC, '--write'], capture_output=True, text=True, cwd=os.path.dirname(SYNC))
print('twin sync rc=%d\n%s' % (r.returncode, (r.stdout + r.stderr).strip()[-600:]))
print('== state after', MODE); status()
