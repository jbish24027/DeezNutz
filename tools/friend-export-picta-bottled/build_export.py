"""Build the Picta + Bottled friend package: byte-for-byte copies, hash-verified, with a lane-state report.

Reads the live instance only. Writes only under the new export root.
"""
import os, sys, hashlib, shutil, json, time, subprocess

INSTANCE = r'C:\1. AUTHORIA'
MODS = os.path.join(INSTANCE, 'mods')
PROFILE = os.path.join(INSTANCE, 'profiles', 'DEEZ CS NUTZ - PICTA')
DSTORE = r'D:\1. MOD STUFF\1. SKYRIM FILES'
MO2DL = os.path.join(INSTANCE, 'downloads')
OUT = os.path.join(INSTANCE, '_export-for-friend-picta-bottled-20261022')

CORE_MODS = [
    'Authoria - ENB Extender 1.6.0 - KiENBExtender only',
    'Authoria - Picta ENB - Root twin',
    'Authoria - Picta 1.1.2 - Darkened to 1.0.1',
    'Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1',
    'Authoria - Picta - Bottled raindrop',
    'Authoria - ReShade - Picta lane preset',
    'Authoria - Helios - Picta exit weather',
    'houseCARL - Authoria - Patch - Picta Seasonal',
    'houseCARL - Authoria - Patch - Picta Seasonal - No Fair',
    'houseCARL - Authoria - Patch - Wanderers Fair - Picta Climate',
    'houseCARL - Authoria - Picta over NAT',
    '[NoDelete] Picta - Cloudy Windy panoramas 11-15 (2K originals)',
    '[NoDelete] Picta ENB 1.1.2 - Data (shipped)',
    '[NoDelete] Silent Horizons 2 - Data',
    'Silent Horizons 2 - Shader Core',
    '[NoDelete] Picta Aurbis - Nordic Winds - Patch 1.1.1 (shipped)',
    '[NoDelete] Bottled Shaders',
    'KiLoader for Skyrim',
    'Authoria - CS Light - Interior Windows',
    'houseCARL - Authoria - Patch - Picta Clear Skies x Requiem',
]
OPTIONAL_MODS = [
    'Bottled - Upscaling runtime 1.0.4',
    'Authoria - ReShade Before UI',
]
ARCHIVES = [
    (DSTORE, 'Bottled Shaders 192816 1.0.11 2026-10-11T01-45Z 587RqTpcR.7z'),
    (DSTORE, 'Picta Aurbis - ENB 178136 1.1.2 2026-10-08T19-08Z MWx0rvXxk.zip'),
    (DSTORE, 'Picta Aurbis - Weather Mod 178136 1.1.1 2026-10-06T22-13Z 587RqTp64.zip'),
    (DSTORE, 'Picta Aurbis - Nordic Winds - Patch 178136 1.1.1 2026-10-06T22-15Z kATsMWUR4.zip'),
    (DSTORE, 'ENB Extender and Helper Legacy (1.6.629-1.6.1179) 99406 1.6.0 2026-09-20T13-01Z n0oTCmVdt.7z'),
    (os.path.join(DSTORE, 'CS'), 'Northman II Reshade-159125-1-0-1758577859.7z'),
    (MO2DL, 'KiLoader for Skyrim-99404-1-2-1713391803.7z'),
    (MO2DL, 'Silent Horizons 2 - Shader Core-101696-1-10-1756049324.7z'),
    (MO2DL, 'Picta Series - Improved Sky Meshes-58263-1-0-2-1636718744.zip'),
    (MO2DL, 'Nordic Winds-112370-1-21-1740767230.7z'),
    (MO2DL, 'ISL Helper SKSE 179132 1.0.5 2026-07-11T01-51Z HZCMOyGHy.zip'),
]
PROFILE_FILES = ['modlist.txt', 'plugins.txt', 'loadorder.txt', 'plugingroups.txt',
                 'Skyrim.ini', 'SkyrimPrefs.ini', 'skyrimcustom.ini']
TOOL_DIRS = [
    (os.path.join(INSTANCE, '_tools', 'picta-bridge'), 'picta-bridge', None),
    (os.path.join(INSTANCE, '_tools', 'reshade-before-ui'), 'reshade-before-ui', {'build'}),
]
DOCS = ['PICTA-DLSS5NR-PLAN-20260930.md']
SEED = os.path.join(INSTANCE, 'overwrite', 'SKSE', 'Plugins', 'CommunityShaders', 'SettingsUser.json')
# (live source, path under overwrite-seed/)
SEEDS = [
    (SEED, os.path.join('SKSE', 'Plugins', 'CommunityShaders', 'SettingsUser.json')),
    (os.path.join(INSTANCE, 'overwrite', 'SKSE', 'Plugins', 'CommunityShaders', 'SceneSettings', 'InteriorOnly',
                  'Authoria_ScreenSpaceGI.json'),
     os.path.join('SKSE', 'Plugins', 'CommunityShaders', 'SceneSettings', 'InteriorOnly', 'Authoria_ScreenSpaceGI.json')),
    (os.path.join(MODS, '[NoDelete] ISL Helper SKSE', 'skse', 'plugins', 'SKSE_ISL.ini'),
     os.path.join('ISL Helper SKSE (mod ini)', 'skse', 'plugins', 'SKSE_ISL.ini')),
]


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def skip_meta(name):
    return name.lower().startswith('meta.ini')


pairs = []  # (src, dst)


def copy_tree(src_root, dst_root, skip_dirs=None, skip_file=None):
    n = 0
    for dp, dn, fn in os.walk(src_root):
        if skip_dirs:
            dn[:] = [d for d in dn if d not in skip_dirs]
        rel = os.path.relpath(dp, src_root)
        for name in fn:
            if skip_file and skip_file(name):
                continue
            s = os.path.join(dp, name)
            d = os.path.join(dst_root, rel if rel != '.' else '', name)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            pairs.append((s, d))
            n += 1
    return n


def running():
    out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    return [x for x in ('modorganizer.exe', 'skyrimse.exe', 'skse64_loader.exe') if x in out]


if __name__ == '__main__':
    if os.path.exists(OUT):
        sys.exit('export root already exists: ' + OUT)
    r = running()
    print('processes:', r or 'MO2 and game closed')
    os.makedirs(OUT)
    report = []

    for m in CORE_MODS:
        n = copy_tree(os.path.join(MODS, m), os.path.join(OUT, 'mods', m), skip_file=skip_meta)
        report.append(('mods', m, n))
    for m in OPTIONAL_MODS:
        n = copy_tree(os.path.join(MODS, m), os.path.join(OUT, 'optional', m), skip_file=skip_meta)
        report.append(('optional', m, n))
    for folder, name in ARCHIVES:
        s = os.path.join(folder, name)
        if not os.path.isfile(s):
            report.append(('downloads MISSING', name, 0))
            continue
        d = os.path.join(OUT, 'downloads', name)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        pairs.append((s, d))
        report.append(('downloads', name, 1))
    snap = os.path.join(OUT, 'reference', 'profile-snapshot', 'DEEZ CS NUTZ - PICTA')
    os.makedirs(snap)
    for f in PROFILE_FILES:
        s = os.path.join(PROFILE, f)
        d = os.path.join(snap, f)
        shutil.copy2(s, d)
        pairs.append((s, d))
    report.append(('reference', 'profile-snapshot', len(PROFILE_FILES)))
    for src, name, skip in TOOL_DIRS:
        n = copy_tree(src, os.path.join(OUT, 'reference', 'tools', name), skip_dirs=skip)
        report.append(('reference/tools', name, n))
    for doc in DOCS:
        s = os.path.join(INSTANCE, doc)
        d = os.path.join(OUT, 'reference', doc)
        shutil.copy2(s, d)
        pairs.append((s, d))
        report.append(('reference', doc, 1))
    for s, rel in SEEDS:
        d = os.path.join(OUT, 'overwrite-seed', rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        pairs.append((s, d))
        report.append(('overwrite-seed', os.path.basename(rel), 1))

    # verify + manifest
    bad = 0
    lines = []
    total = 0
    for s, d in pairs:
        hs, hd = md5(s), md5(d)
        if hs != hd or os.path.getsize(s) != os.path.getsize(d):
            bad += 1
            print('MISMATCH', d)
        total += os.path.getsize(d)
        lines.append('%s *%s' % (hd, os.path.relpath(d, OUT).replace('\\', '/')))
    with open(os.path.join(OUT, 'MANIFEST.md5'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorted(lines, key=lambda x: x.split(' *', 1)[1])) + '\n')
    print()
    for kind, name, n in report:
        print('%-18s %5d  %s' % (kind, n, name))
    print()
    print('files copied: %d  verified: %d  mismatches: %d  bytes: %d (%.1f MB)' % (
        len(pairs), len(pairs) - bad, bad, total, total / 1048576))
    json.dump({'pairs': len(pairs), 'bad': bad, 'bytes': total, 'report': report},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_result.json'), 'w'), indent=1)
