"""Write the per-mod split straight to disk as folders. No zips.

    D:\\Eleonora\\<Mod Name>\\Sound\\DBVO\\elnordvoice\\*.fuz

The root has to be SHORT. The longest entry is <Mod>/Sound/DBVO/elnordvoice/<file> at
245 characters, so a root over 14 characters pushes the longest files past the 260
Windows limit and Explorer can no longer copy or delete them. D:\\Eleonora is 11.
"""
import os, sys, io, csv, shutil, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import package_by_mod as P

DEST = 'D:/Eleonora'
INNER = os.path.join('Sound', 'DBVO', 'elnordvoice')
LIMIT = 259


def main(dest=DEST):
    dest = os.path.normpath(dest)
    if os.path.isdir(dest) and os.listdir(dest):
        sys.stderr.write('REFUSING: %s already exists and is not empty\n' % dest)
        return 1
    budget = len(dest) + 1
    sys.stderr.write('destination %s (%d chars), longest entry 245 -> %d\n'
                     % (dest, len(dest), budget + 245))

    att, text, proper = P.load_attribution()
    files = os.listdir(P.SRC)

    vindex = collections.defaultdict(set)
    for k in att:
        for v in P.variants(k, text.get(k)):
            if v != k:
                vindex[v].add(k)
    renamed = {v: next(iter(ks)) for v, ks in vindex.items()
               if len(ks) == 1 and v not in att}

    plan = collections.defaultdict(list)
    unattributed = []
    for n in files:
        key, arc = n.lower(), n
        if key not in att and key in renamed:
            key = renamed[key]
            arc = proper.get(key, key)
        hit = att.get(key)
        if not hit:
            unattributed.append(n)
            continue
        for mod in hit[0]:
            plan[mod].append((arc, n, hit[1]))
    plan['_UNATTRIBUTED'] = [(n, n, 'no plugin on disk asks for this name')
                             for n in unattributed]

    manifest = [('mod', 'folder', 'file', 'attribution', 'text')]
    written = toolong = 0
    over = []
    for mod in sorted(plan):
        folder = P.safe_folder(mod)
        d = os.path.join(dest, folder, INNER)
        os.makedirs(P.LONG(d), exist_ok=True)
        for name, srcname, source in sorted(plan[mod]):
            full = os.path.join(d, name)
            if len(full) > LIMIT:
                toolong += 1
                over.append(full)
            shutil.copyfile(os.path.join(P.SRC, srcname), P.LONG(full))
            written += 1
            manifest.append((mod, folder, name, source, text.get(name.lower(), '')))

    buf = io.StringIO()
    csv.writer(buf, lineterminator='\n').writerows(manifest)
    io.open(os.path.join(dest, '_MANIFEST.csv'), 'w',
            encoding='utf-8-sig', newline='').write(buf.getvalue())
    io.open(os.path.join(dest, '_READ ME.txt'), 'w', encoding='utf-8').write(READ_ME)

    sys.stderr.write('%d mod folders, %d files written\n' % (len(plan), written))
    sys.stderr.write('files over the %d-character limit: %d\n' % (LIMIT, toolong))
    for f in over[:10]:
        sys.stderr.write('   %d  %s\n' % (len(f), f))
    return 0


READ_ME = """Eleonora (elnordvoice) - DBVO recordings generated 2026-08-28, split by mod.

    <Mod Name>\\Sound\\DBVO\\elnordvoice\\*.fuz

Every mod folder is complete on its own and drops straight into a mod folder. A few
lines are word-for-word identical across two mods, so those .fuz appear in both.

KEEP THIS TREE NEAR THE ROOT OF A DRIVE. The longest entry is 245 characters, so once
the folder it sits in goes past about 14 characters, the longest files cross the 260
character Windows limit and Explorer refuses to copy or delete them.

_MANIFEST.csv lists every file, the mod it was filed under, how it was attributed, and
the line it says.

Skyrim - Base Game holds the vanilla Skyrim.esm topics - the only lines here that are
not from a mod.

_UNATTRIBUTED holds 31 recordings whose text matches no player topic in any plugin.
Most are editor leftovers - "AMQ06a", "Enable_People" - or lines truncated by the run.

.fuz filenames must keep their exact characters, curly apostrophes and ellipses
included. DBVO looks the file up by the dialogue text, so a straightened quote is a
silent line. 27 files came out of the run mangled that way and are back under their
correct names here.
"""


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEST))
