"""ReShade A/B: `off` disables the 'Reshade - DLL' mod (no dxgi.dll deployed by Root Builder = no ReShade at all) in the PICTA and
Preset Studio lanes; `on` re-enables it. The two preset mods stay as they are (inert without the DLL). Backup once per file.
Refuses to run with MO2 or the game open."""
import os, sys, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
MODE = sys.argv[1] if len(sys.argv) > 1 else 'status'
INST = r'C:\1. AUTHORIA'; PROFILES = ['DEEZ CS NUTZ - PICTA', 'Authoria - Preset Studio - HPH']; MOD = 'Reshade - DLL'
def running():
    out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    return 'modorganizer' in out or 'skyrimse' in out
for p in PROFILES:
    path = os.path.join(INST, 'profiles', p, 'modlist.txt')
    raw = open(path, 'rb').read(); eol = b'\r\n' if raw.count(b'\r\n') >= raw.count(b'\n') // 2 else b'\n'
    trailing = raw.endswith(eol); lines = (raw[:-len(eol)] if trailing else raw).split(eol)
    idx = [i for i, l in enumerate(lines) if l[1:] == MOD.encode()]
    assert len(idx) == 1, (p, idx)
    cur = lines[idx[0]][:1].decode()
    if MODE == 'status': print('%-34s %s %s' % (p, 'ON ' if cur == '+' else 'off', MOD)); continue
    if running(): sys.exit('MO2 or the game is running - aborting')
    want = b'+' if MODE == 'on' else b'-'
    bak = path + '.bak-reshadeab-20261012'
    if not os.path.exists(bak): shutil.copy2(path, bak)
    lines[idx[0]] = want + MOD.encode()
    open(path, 'wb').write(eol.join(lines) + (eol if trailing else b''))
    chk = open(path, 'rb').read().split(eol)[idx[0]]
    print('%-34s %s -> %s  (%s)' % (p, cur, chk[:1].decode(), 'verified' if chk == want + MOD.encode() else 'VERIFY FAILED'))
