"""Same split, packaged so Windows Explorer can actually extract it.

One zip PER MOD, each containing only:

    Sound/DBVO/elnordvoice/*.fuz

The mod name moves out of the path and into the zip's filename, which takes up to
60 characters off every path. Longest path inside a mod zip is then 24 + 176 = 200,
so it extracts anywhere sensible without long-path support.

Those 181 zips are then wrapped in one outer zip for sending. The outer zip holds
single files, so extracting IT is short-path safe too.
"""
import os, sys, io, csv, zipfile, shutil, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import package_by_mod as P

OUTDIR = os.path.normpath(P.ROOT + '/Eleonora-DBVO-20260828-per-mod')
OUTER = os.path.normpath(P.ROOT + '/Eleonora-DBVO-20260828-per-mod.zip')
INNER = 'Sound/DBVO/elnordvoice/'


def main():
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

    if os.path.isdir(OUTDIR):
        shutil.rmtree(OUTDIR)
    os.makedirs(OUTDIR)

    manifest = [('mod', 'zip', 'file', 'attribution', 'text')]
    longest = 0
    for mod in sorted(plan):
        folder = P.safe_folder(mod)
        zpath = os.path.join(OUTDIR, folder + '.zip')
        with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
            for name, srcname, source in sorted(plan[mod]):
                arc = INNER + name
                longest = max(longest, len(arc))
                zf.write(os.path.join(P.SRC, srcname), arc)
                manifest.append((mod, folder + '.zip', name, source,
                                 text.get(name.lower(), '')))
    sys.stderr.write('%d mod zips, longest inner path %d chars\n' % (len(plan), longest))

    buf = io.StringIO()
    csv.writer(buf, lineterminator='\n').writerows(manifest)
    io.open(os.path.join(OUTDIR, '_MANIFEST.csv'), 'w',
            encoding='utf-8-sig', newline='').write(buf.getvalue())
    io.open(os.path.join(OUTDIR, '_READ ME.txt'), 'w', encoding='utf-8').write(READ_ME)

    with zipfile.ZipFile(OUTER, 'w', zipfile.ZIP_STORED, allowZip64=True) as zf:
        for n in sorted(os.listdir(OUTDIR)):
            zf.write(os.path.join(OUTDIR, n), n)
    sys.stderr.write('wrote %s (%.1f MB)\n' % (OUTER, os.path.getsize(OUTER) / 1048576.0))


READ_ME = """Eleonora (elnordvoice) - DBVO recordings generated 2026-08-28, one zip per mod.

Extract this outer zip anywhere - it only holds single files, so no long paths.
Then extract whichever mod's zip you want. Each one contains:

    Sound/DBVO/elnordvoice/*.fuz

and nothing else, so it drops straight into a mod folder.

It is split this way on purpose. Some dialogue lines are long, and the longest
filename in here is 176 characters. With the mod name in the path as well, Windows
Explorer refuses to extract at 260 characters. Keeping the mod name in the zip's
filename instead takes it back under the limit.

Every mod zip is complete on its own. A few lines are word-for-word identical across
two mods, so those .fuz appear in both.

_MANIFEST.csv lists every file, which mod zip it is in, how it was attributed, and the
line it says.

_UNATTRIBUTED.zip holds 31 recordings whose text matches no player topic in any plugin
here. Most are editor leftovers - "AMQ06a", "Enable_People" - or lines truncated by the
TTS run.

One thing worth knowing: .fuz filenames must keep their exact characters, curly
apostrophes and ellipses included. DBVO looks the file up by the dialogue text, so a
straightened quote is a silent line. 27 files came out of the run mangled that way and
are back under their correct names in here.

"""


if __name__ == '__main__':
    main()
