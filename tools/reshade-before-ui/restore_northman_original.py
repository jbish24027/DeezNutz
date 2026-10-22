"""Put the untouched Northman II 1.0 preset (Nexus 159125) into the Picta-lane ReShade preset mod (used by
DEEZ CS NUTZ - PICTA and the Preset Studio twin). Keeps the user's 10-13 overlay edits as a backup, keeps a
pristine copy beside it, and frees Scroll Lock for Northman's own depth-blur toggle (KeyEffects back to none,
as the stock ReShade.ini has it). The pre-UI plugin is untouched. --write to apply."""
import os, sys, shutil, subprocess, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ARCHIVE_INI = sys.argv[1]
LANE = r'C:\1. AUTHORIA\mods\Authoria - ReShade - Picta lane preset'
PRESET = os.path.join(LANE, 'Root', 'Northman II.ini')
RSINI = os.path.join(LANE, 'Root', 'ReShade.ini')
PRISTINE = os.path.join(LANE, 'Root', 'Northman II.ini.original-159125-1.0')
STORE = r'D:\1. MOD STUFF\1. SKYRIM FILES\CS'
ARCHIVE = r'C:\Users\User\Downloads\Northman II Reshade-159125-1-0-1758577859.7z'
write = '--write' in sys.argv
out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
if write and any(n in out for n in ('skyrimse.exe', 'modorganizer.exe', 'skse64_loader.exe')):
    sys.exit('ABORT - MO2 or the game is running')
orig = open(ARCHIVE_INI, 'rb').read()
print('original preset', len(orig), 'bytes md5', hashlib.md5(orig).hexdigest())
rs = open(RSINI, 'rb').read()
rs_new = rs.replace(b'KeyEffects=145,0,0,0', b'KeyEffects=0,0,0,0')
print('ReShade.ini KeyEffects change:', rs_new != rs)
meta_p = os.path.join(LANE, 'meta.ini')
meta = open(meta_p, 'rb').read().decode('utf-8')
new_comment = ('comments=Picta-profile ReShade preset = the ORIGINAL Northman II 1.0 (Nexus 159125) since 2026-10-13, byte copy '
               '(pristine copy: Root\\Northman II.ini.original-159125-1.0). UI stays sharp through the Authoria - ReShade Before UI '
               'plugin. Scroll Lock = Northman\'s MagicDOF toggle (off at start), Ctrl+Delete = GloomAO + RadiantGI toggle. '
               'Root\\ReShade.ini = the Reshade - DLL file with KeyEffects none and PerformanceMode 0.')
lines = meta.split('\r\n') if '\r\n' in meta else meta.split('\n')
lines = [new_comment if l.startswith('comments=') else l for l in lines]
meta_new = ('\r\n' if '\r\n' in meta else '\n').join(lines)
if write:
    bak = PRESET + '.bak-useredits-20261013-0443'
    if not os.path.exists(bak):
        shutil.copy2(PRESET, bak)
    open(PRESET, 'wb').write(orig)
    open(PRISTINE, 'wb').write(orig)
    if rs_new != rs:
        b2 = RSINI + '.bak-northmanorig-20261013'
        if not os.path.exists(b2):
            shutil.copy2(RSINI, b2)
        open(RSINI, 'wb').write(rs_new)
    b3 = meta_p + '.bak-northmanorig-20261013'
    if not os.path.exists(b3):
        shutil.copy2(meta_p, b3)
    open(meta_p, 'wb').write(meta_new.encode('utf-8'))
    if os.path.isdir(STORE) and not os.path.exists(os.path.join(STORE, os.path.basename(ARCHIVE))):
        shutil.copy2(ARCHIVE, STORE)
        print('archive copied to the source store')
    assert open(PRESET, 'rb').read() == orig
    print('WRITTEN - preset is now byte-identical to the original')
else:
    print('dry run')
