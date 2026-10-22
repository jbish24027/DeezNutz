"""Stage the carriage mods into C:\\1. AUTHORIA\\mods. Copies files from the extracted archives (data only).
--write to write; otherwise prints the plan."""
import os, sys, shutil, hashlib

WRITE = '--write' in sys.argv
S = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\7b213a74-5dbb-466e-845a-b77c408e90d7\scratchpad\arch'
MODS = r'C:\1. AUTHORIA\mods'
DL = r'C:\1. AUTHORIA\downloads'


def meta(modid, version, archive, comment=''):
    return ('[General]\r\ngameName=SkyrimSE\r\nmodid=%s\r\nversion=%s\r\nnewestVersion=%s\r\ncategory="-1,"\r\n'
            'nexusFileStatus=1\r\ninstallationFile=%s\r\nrepository=Nexus\r\nignoredVersion=\r\ncomments=%s\r\nnotes=\r\n'
            'nexusDescription=\r\nurl=\r\nhasCustomURL=false\r\nconverted=false\r\nvalidated=false\r\ntracked=0\r\n\r\n'
            '[installedFiles]\r\nsize=0\r\n' % (modid, version, version, archive, comment))


# (mod folder, [(src path relative to S, dest relative path)], meta args)
def tree(src_rel, dst_prefix=''):
    out = []
    root = os.path.join(S, src_rel)
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            out.append((p, os.path.join(dst_prefix, os.path.relpath(p, root))))
    return out


CP = r'ACARP\Animated Carriage Additional Route compatibility patches'
PLAN = [
    ('Animated Carriage Additional Route',
     [(os.path.join(S, 'ACAR', f), f) for f in ('Animated Carriage Additional Route.esp', 'Animated Carriage Additional Route 0.esp')],
     ('112548', '1.6.4', 'Animated Carriage Additional Route 112548 1.6.4 2026-08-11T03-14Z 8gJHT4Fjy.7z')),
    ('Animated Carriage Additional Route - Compatibility Patches',
     [(os.path.join(S, CP, f), f) for f in ('ACAR_GG Markarth Outskirts_Northern Roads compatibility patch.esp',
                                              'ACAR_JKs Solitude Outskirts compatibility patch.esp')],
     ('126155', '0.83', 'Animated Carriage Additional Route patches FOMOD 126155 0.83 2026-08-12T17-35Z 9LMpgbzB5.rar',
      'FOMOD picks: GG Markarth Outskirts (Northern Roads) + JKs Solitude Outskirts')),
    ('Carriage Stops of Skyrim', tree('CSOS'),
     ('10434', '1.9', 'Carriage Stops of Skyrim-10434-1-9-1780702326.7z')),
    ('Animated Carriages Take You Everywhere', tree('ACTYE'),
     ('154706', '2.2.2', 'Animated Carriages Take You Everywhere 154706 2.2.2 2026-08-10T15-00Z 2Bej58mJP.zip')),
    ('Skyking Carriages',
     tree(r'SK\Skyking Carriages\2k\textures', 'textures') + tree(r'SK\Skyking Carriages\parallax meshes\meshes', 'meshes'),
     ('156805', '1.2', 'Skyking Carriages-156805-1-2-1755797295.7z', 'FOMOD picks: 2k + parallax meshes')),
    ('Skyking Carriages - Embers XD Patch',
     tree(r'SKEXD\Skyking Carriages - Embers XD Patch\parallax meshes\meshes', 'meshes'),
     ('156805', '1.0', 'Skyking Carriages - Embers XD Patch-156805-1-0-1755127632.7z', 'FOMOD pick: Parallax')),
]

# Animated Carriage 1.1.0 -> 1.2.1: only the 9 files that changed (the folder never carried the carriage/horse meshes)
AC_CHANGED = ['AnimatedCarriage.esm', r'scripts\zxAC_CartSciprt.pex', r'scripts\zxAC_ManagerQuestScript.pex',
              r'scripts\zxAC_RqBaseScript.pex', r'scripts\zxAC_StartMarkerScript.pex',
              r'scripts\source\zxAC_CartSciprt.psc', r'scripts\source\zxAC_ManagerQuestScript.psc',
              r'scripts\source\zxAC_RqBaseScript.psc', r'scripts\source\zxAC_StartMarkerScript.psc']


def find_ci(root, rel):
    cur = root
    for part in rel.split('\\'):
        names = {n.lower(): n for n in os.listdir(cur)}
        cur = os.path.join(cur, names[part.lower()])
    return cur


ops = []
for rel in AC_CHANGED:
    src = os.path.join(S, r'AC\AnimatedCarriageSE\10 English', rel) if rel.endswith('.esm') else find_ci(os.path.join(S, r'AC\AnimatedCarriageSE\00 Core Files'), rel)
    dst = find_ci(os.path.join(MODS, 'Animated Carriage'), rel)
    ops.append((src, dst))

for folder, files, m in PLAN:
    d = os.path.join(MODS, folder)
    if os.path.exists(d):
        sys.exit('REFUSE: folder already exists: ' + d)
    for src, rel in files:
        ops.append((src, os.path.join(d, rel)))

for src, dst in ops:
    print(('COPY ' if WRITE else 'plan ') + dst.replace(MODS + '\\', ''))
    if WRITE:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        assert hashlib.md5(open(src, 'rb').read()).digest() == hashlib.md5(open(dst, 'rb').read()).digest()

if WRITE:
    for folder, files, m in PLAN:
        open(os.path.join(MODS, folder, 'meta.ini'), 'wb').write(meta(*m).encode('utf-8'))
    # Animated Carriage meta: bump version + archive name, keep everything else
    mp = os.path.join(MODS, 'Animated Carriage', 'meta.ini')
    t = open(mp, 'rb').read().decode('utf-8')
    t = t.replace('version=1.1.0.0', 'version=1.2.1').replace('newestVersion=1.1.0.0', 'newestVersion=1.2.1')
    t = t.replace('installationFile=Animated Carriage-112397-1-1-0-1718044068.7z',
                  'installationFile=Animated Carriage 112397 1.2.1 2026-07-25T02-59Z Yj6wQRvIp.7z')
    open(mp, 'wb').write(t.encode('utf-8'))
    # archives into MO2 downloads (copy, never move)
    src_dl = r'C:\Users\User\Downloads'
    for folder, files, m in PLAN:
        a = m[2]
        if not os.path.exists(os.path.join(DL, a)):
            shutil.copyfile(os.path.join(src_dl, a), os.path.join(DL, a))
    a = 'Animated Carriage 112397 1.2.1 2026-07-25T02-59Z Yj6wQRvIp.7z'
    if not os.path.exists(os.path.join(DL, a)):
        shutil.copyfile(os.path.join(src_dl, a), os.path.join(DL, a))
    for a in ['Animated Carriage For Northern Roads-118850-1-1715091946.7z']:
        if not os.path.exists(os.path.join(DL, a)):
            shutil.copyfile(os.path.join(src_dl, a), os.path.join(DL, a))
print('%d files %s' % (len(ops), 'written' if WRITE else '(dry run)'))
