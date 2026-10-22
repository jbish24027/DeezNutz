"""Install AuthoriaReShadeBeforeUI as its own MO2 mod, add its modlist line (enabled in the Picta lane and the
Preset Studio twin, disabled in the other profiles that carry the Picta-lane ReShade preset), and put
MagicDOF + GaussianBlur back into the Picta-lane preset. Backs up every file it changes.
Run with --write; without it, only prints what it would do."""
import os, sys, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = r'C:\1. AUTHORIA'
HERE = os.path.dirname(os.path.abspath(__file__))
MOD = 'Authoria - ReShade Before UI'
ANCHOR = 'Authoria - ReShade - Picta lane preset'
ON = ('DEEZ CS NUTZ - PICTA', 'Authoria - Preset Studio - HPH')
TAG = '.bak-beforeui-20261013'
PRESET = os.path.join(ROOT, 'mods', ANCHOR, 'Root', 'Northman II.ini')
TECH = ('prod80_02_Bonus_LUT_pack@PD80_02_Bonus_LUT_pack.fx,ContrastAdaptiveSharpen@CAS.fx,Curves@Curves.fx,Clarity@Clarity.fx,'
        'AmbientLight@AmbientLight.fx,Vibrance@Vibrance.fx,Vignette@Vignette.fx,Technicolor@Technicolor.fx,'
        'GaussianBlur@GaussianBlur.fx,Colourfulness@Colourfulness.fx,MagicDOF@DOF.fx')
SORT = TECH + ',MartyMcFlyDOF@DOF.fx,MatsoDOF@DOF.fx,RingDOF@DOF.fx,GP65CJ042DOF@DOF.fx'
META = ('[General]\r\ngameName=SkyrimSE\r\nmodid=0\r\nversion=1.0.0\r\nnewestVersion=\r\ncategory="-1,"\r\ninstallationFile=\r\n'
        'repository=\r\ncomments=Renders ReShade effects right before the game draws its menus and HUD (depth of field and blur '
        'stay off the UI). Authoria-built SKSE plugin + ReShade add-on, same method as SSE ReShade Helper. Skyrim 1.6.1170 only; '
        'it checks the exe and the patched bytes and does nothing if they differ. Source and build: _tools\\reshade-before-ui. '
        'Log: Documents\\My Games\\Skyrim Special Edition\\SKSE\\AuthoriaReShadeBeforeUI.log\r\n'
        'notes="2026-10-13. Enabled in DEEZ CS NUTZ - PICTA and Authoria - Preset Studio - HPH. If a frame-generation proxy puts '
        'ReShade on a D3D12 swap chain the plugin stands aside (ReShade renders at Present as before)."\r\n')
write = '--write' in sys.argv


def running():
    out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    return [n for n in ('skyrimse.exe', 'modorganizer.exe', 'skse64_loader.exe') if n in out]


if write and running():
    sys.exit('ABORT - still running: %s' % running())

# 1. the mod folder
dll_src = os.path.join(HERE, 'build', 'AuthoriaReShadeBeforeUI.dll')
mod_dir = os.path.join(ROOT, 'mods', MOD)
dst = os.path.join(mod_dir, 'SKSE', 'Plugins', 'AuthoriaReShadeBeforeUI.dll')
print('mod:', mod_dir, 'exists' if os.path.isdir(mod_dir) else 'new')
if write:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(dll_src, dst)
    open(os.path.join(mod_dir, 'meta.ini'), 'wb').write(META.encode('utf-8'))

# 2. modlist lines
for prof in sorted(os.listdir(os.path.join(ROOT, 'profiles'))):
    ml = os.path.join(ROOT, 'profiles', prof, 'modlist.txt')
    if not os.path.isfile(ml):
        continue
    raw = open(ml, 'rb').read()
    eol = b'\r\n' if b'\r\n' in raw else b'\n'
    lines = raw.split(eol)
    names = [l[1:].decode('utf-8', 'replace') for l in lines if l[:1] in (b'+', b'-', b'*')]
    if MOD in names:
        print('  %-40s already has the line' % prof)
        continue
    idx = next((i for i, l in enumerate(lines) if l[1:].decode('utf-8', 'replace') == ANCHOR), None)
    if idx is None:
        print('  %-40s no Picta-lane preset line - skipped' % prof)
        continue
    flag = b'+' if prof in ON else b'-'
    lines.insert(idx, flag + MOD.encode('utf-8'))
    print('  %-40s %s at line %d' % (prof, flag.decode(), idx + 1))
    if write:
        bak = ml + TAG
        if not os.path.exists(bak):
            shutil.copy2(ml, bak)
        open(ml, 'wb').write(eol.join(lines))

# 3. the preset
raw = open(PRESET, 'rb').read()
eol = b'\r\n' if b'\r\n' in raw else b'\n'
out = []
for l in raw.split(eol):
    if l.startswith(b'Techniques='):
        l = b'Techniques=' + TECH.encode()
    elif l.startswith(b'TechniqueSorting='):
        l = b'TechniqueSorting=' + SORT.encode()
    out.append(l)
new = eol.join(out)
print('preset: Techniques ->', TECH.count(',') + 1, 'effects (MagicDOF + GaussianBlur back)')
if write and new != raw:
    bak = PRESET + TAG
    if not os.path.exists(bak):
        shutil.copy2(PRESET, bak)
    open(PRESET, 'wb').write(new)
print('WRITTEN' if write else 'dry run')
