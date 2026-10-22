"""Package the newly generated .fuz into one zip, one folder per mod.

    <Mod Name>/Sound/DBVO/elnordvoice/<only that mod's .fuz>

Attribution, most trustworthy first:
  1. ELEONORA-DBVO-MISSING-LINES-20260828.csv  (mod, plugin, target_filename)
  2. attribute.pkl   - the full live-winner map for the DEEZ CS NUTZ - PBR profile
  3. fallback.pkl    - every plugin on disk, including ones disabled in that profile

A line that belongs to more than one mod is copied into each of those mods, so any
single folder is complete on its own.
"""
import os, sys, csv, io, pickle, zipfile, collections

B = chr(92)
LONG = lambda p: B + B + '?' + B + os.path.normpath(p)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = 'D:/1. MOD STUFF/1. SKYRIM FILES/- 1 TOOLS/z. DBVO crap'
SRC = LONG(ROOT + '/3 output final/Sound/DBVO/elnordvoice')
CSVP = 'C:/1. AUTHORIA/ELEONORA-DBVO-MISSING-LINES-20260828.csv'
OUT = os.path.normpath(ROOT + '/Eleonora-DBVO-20260828-by-mod.zip')

ILLEGAL = '<>:"/' + B + '|?*'


RENAME = {'<Stock Game>': 'Skyrim - Base Game'}


def safe_folder(name):
    name = RENAME.get(name, name)
    s = ''.join('_' if c in ILLEGAL else c for c in name).rstrip(' .')
    return s or '_unnamed'


from dbvoname import dbvo_name, BAD as P_BAD


def load_attribution():
    """filename(lower) -> ({mod: [plugin,...]}, source_label), plus text and true case

    attribute.pkl is the authority: every player topic that WINS in the load order,
    named by the corrected rule. The old missing-lines CSV is not used - it was built
    with the pre-correction rule, before the trailing (tag) was understood.
    """
    att, text, proper = {}, {}, {}
    n_csv = 0

    live = pickle.load(open(os.path.join(HERE, 'attribute.pkl'), 'rb'))
    for k, mods in live['name_mods'].items():
        line = live['name_text'].get(k, '')
        proper.setdefault(k, dbvo_name(line) if line else k)
        att[k] = (dict(mods), 'live player topic')
        text.setdefault(k, line)
    n_live = len(att)

    # deep.pkl is deliberately NOT used: it matches any string in any plugin, so a
    # common line like "A battleaxe." lands in dozens of unrelated mods. 29 names were
    # not worth 99 junk folders.
    n_fb = n_deep = 0
    for fn, label in (('fallback.pkl', 'inactive plugin'),):
        p = os.path.join(HERE, fn)
        if not os.path.exists(p):
            continue
        for k, mods in pickle.load(open(p, 'rb')).items():
            proper.setdefault(k, k)
            if k not in att:
                att[k] = (dict(mods), label)
                if fn == 'fallback.pkl':
                    n_fb += 1
                else:
                    n_deep += 1
    sys.stderr.write('attribution sources: missing-list %d, live %d, inactive %d, deep %d\n'
                     % (n_csv, n_live, n_fb, n_deep))
    return att, text, proper


def flat(s):
    """What the TTS pipeline did to non-ASCII characters: turned each into '_'."""
    return ''.join(c if ord(c) < 128 else '_' for c in s)


def variants(name, line):
    """Every filename this pipeline has actually been seen to produce for one line.

    Three quirks, all read off the output rather than assumed:
      * non-ASCII becomes '_'  (curly apostrophe, ellipsis, accent)
      * a trailing '_' is then dropped, so a line ending in an ellipsis loses it
      * trailing whitespace is NOT trimmed, so "Kynesgrove. " keeps its '_'
    """
    out = {name}
    if line:
        untrimmed = ''.join('_' if c in P_BAD else c for c in line.rstrip('\r\n')) + '.fuz'
        out.add(untrimmed)
    for n in list(out):
        f = flat(n)
        out.add(f)
        for x in (n, f):
            stem = x[:-4] if x.lower().endswith('.fuz') else x
            out.add(stem.rstrip('_') + '.fuz')
    return {v.lower() for v in out}


def main():
    att, text, proper = load_attribution()
    files = os.listdir(SRC)
    sys.stderr.write('generated files: %d\n' % len(files))

    # The pipeline mangles some names (see variants()). DBVO looks a file up by the
    # verbatim dialogue text, so a mangled name is a silent line. Map every variant
    # back to the one canonical name, and only where the mapping is unambiguous.
    vindex = collections.defaultdict(set)
    for k in att:
        for v in variants(k, text.get(k)):
            if v != k:
                vindex[v].add(k)
    renamed = {v: next(iter(ks)) for v, ks in vindex.items()
               if len(ks) == 1 and v not in att}

    plan = collections.defaultdict(list)     # mod -> [(arcname, source_path, source)]
    unattributed = []
    fixed = []
    for n in files:
        key, arc = n.lower(), n
        if key not in att and key in renamed:
            key = renamed[key]
            arc = proper.get(key, key)
            fixed.append((n, arc))
        hit = att.get(key)
        if not hit:
            unattributed.append(n)
            continue
        mods, source = hit
        for mod in mods:
            plan[mod].append((arc, n, source))
    sys.stderr.write('renamed back to the verbatim dialogue text: %d\n' % len(fixed))
    with io.open(os.path.join(HERE, 'renamed_nonascii.txt'), 'w', encoding='utf-8') as f:
        for a, b in sorted(fixed):
            f.write('%s\n  -> %s\n' % (a, b))
    sys.stderr.write('mods: %d   placements: %d   unattributed: %d\n'
                     % (len(plan), sum(len(v) for v in plan.values()), len(unattributed)))

    manifest = [('mod', 'file', 'attribution', 'text')]
    zf = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True)
    try:
        for mod in sorted(plan):
            folder = safe_folder(mod)
            for name, srcname, source in sorted(plan[mod]):
                arc = '%s/Sound/DBVO/elnordvoice/%s' % (folder, name)
                zf.write(os.path.join(SRC, srcname), arc)
                manifest.append((mod, name, source, text.get(name.lower(), '')))
        for n in sorted(unattributed):
            arc = '_UNATTRIBUTED/Sound/DBVO/elnordvoice/%s' % n
            zf.write(os.path.join(SRC, n), arc)
            manifest.append(('_UNATTRIBUTED', n, 'no plugin on disk asks for this name', ''))

        buf = io.StringIO()
        w = csv.writer(buf, lineterminator='\n')
        w.writerows(manifest)
        zf.writestr('_MANIFEST.csv', buf.getvalue().encode('utf-8-sig'))
        zf.writestr('_READ ME.txt', READ_ME.encode('utf-8'))
    finally:
        zf.close()
    sys.stderr.write('wrote %s (%.1f MB)\n' % (OUT, os.path.getsize(OUT) / 1048576.0))

    with io.open(os.path.join(HERE, 'package_report.txt'), 'w', encoding='utf-8') as f:
        f.write('%-6s %s\n' % ('files', 'mod'))
        for mod, items in sorted(plan.items(), key=lambda kv: -len(kv[1])):
            f.write('%-6d %s\n' % (len(items), mod))
        f.write('\nunattributed: %d\n' % len(unattributed))
    return plan, unattributed


READ_ME = """Eleonora (elnordvoice) - DBVO recordings generated 2026-08-28, split by mod.

One folder per mod. Inside each:

    <Mod Name>/Sound/DBVO/elnordvoice/*.fuz

Every folder is complete on its own. A handful of lines are word-for-word identical
across two mods; those .fuz appear in both folders rather than only one, so you can
ship any single folder without hunting for a missing file.

_MANIFEST.csv lists every file, the mod it was filed under, how it was attributed,
and the dialogue line it says.

_UNATTRIBUTED holds 31 recordings whose text matches no player topic in any plugin
here. Most are editor leftovers - "AMQ06a", "Enable_People" - or lines truncated by the
TTS run.

One thing worth knowing: .fuz filenames must keep their exact characters, curly
apostrophes and ellipses included. DBVO looks the file up by the dialogue text, so a
straightened quote is a silent line. 27 files came out of the run mangled that way and
are back under their correct names in here.

"""


if __name__ == '__main__':
    main()
