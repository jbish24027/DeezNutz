"""Final generator: one 'topic files<Plugin>.txt' per plugin, containing only the
lines Eleonora is still missing, attributed to the plugin that actually WINS the
record in this load order.

Extraction rules are a byte-exact reimplementation of DBVO-SSEEdit-Topic-Extract.pas
(verified line-for-line against the five hand-made gold files).
"""
import os, sys, json, collections, pickle
import vfs, pasrepro, winners as W
from pasrepro import sorted_stringlist, write_topic_file, should_ignore

OUT = r"D:\1. MOD STUFF\1. SKYRIM FILES\- 1 TOOLS\z. DBVO crap\topic files missing 20260828"
BAD = '\\/:*?"<>|'
TRANS = {ord(c): '_' for c in BAD}
TRANS[ord(' ')] = '_'


def fuzname(text):
    return (text.translate(TRANS) + '.fuz').lower()


def covered():
    plain, broken = set(), set()
    for mod in vfs.enabled_mods():
        base = os.path.join(vfs.MODS, mod)
        for sub in (os.path.join('Sound', 'DBVO', 'elnordvoice'),
                    os.path.join('Sound', 'elnordvoice')):
            d = os.path.join(base, sub)
            if not os.path.isdir(d):
                continue
            for name in os.listdir(d):
                if not name.lower().endswith('.fuz'):
                    continue
                low = name.lower()
                plain.add(low)
                k = low.rfind('___broken___')
                if k != -1:
                    broken.add(low[k + len('___broken___'):])
    return plain, broken


def main():
    plain, brk = covered()
    win = pickle.load(open('winners.pkl', 'rb'))
    pp = vfs.plugin_paths()
    modof = {p.lower(): m for p, (q, m) in pp.items()}

    # The naming pipeline trims the line before building the filename: verified on 235
    # padded strings - 78 match only their trimmed form, 0 match only their raw form.
    live = collections.defaultdict(list)
    dropped = 0
    unvoiceable = []
    for (key, kind), (plug, raw, edid, fid) in win.items():
        if not raw:
            continue
        line = raw.strip()
        if not line or should_ignore(line, edid, fid):
            dropped += 1
            continue
        if any(c in line for c in '\r\n\t'):
            # an interior control character cannot appear in a Windows filename
            unvoiceable.append((plug, line))
            continue
        live[plug].append(line)

    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            os.remove(os.path.join(OUT, f))
    os.makedirs(OUT, exist_ok=True)

    index, allmiss = [], []
    for plug, lines in live.items():
        lines = sorted_stringlist(lines)                      # sort + dedupe, xEdit rules
        miss = [s for s in lines if fuzname(s) not in plain and fuzname(s) not in brk]
        mod = modof.get(plug.lower(), '?')
        index.append((plug, mod, len(lines), len(miss)))
        if miss:
            write_topic_file(os.path.join(OUT, 'topic files' + os.path.splitext(plug)[0] + '.txt'), miss)
            allmiss.extend(miss)

    dedup = sorted_stringlist(allmiss)
    write_topic_file(os.path.join(OUT, '_ALL MISSING deduplicated.txt'), dedup)

    index.sort(key=lambda r: (-r[3], r[0].lower()))
    nfiles = sum(1 for r in index if r[3])
    with open(os.path.join(OUT, '_INDEX.txt'), 'wb') as f:
        def w(s):
            f.write(s.encode('cp1252', 'replace') + b'\r\n')
        w('Eleonora / DBVO - player lines with no recording yet.')
        w('Profile: DEEZ CS NUTZ - PBR.   Generated 2026-08-28.')
        w('')
        w('%d topic files, %d lines, %d unique after de-duplication.' % (nfiles, len(allmiss), len(dedup)))
        w('Format matches your xEdit script output: CP1252, CRLF, sorted, one line per topic.')
        w('Lines are attributed to the plugin that WINS the record, so a topic')
        w('rewritten by a "DBVO Fix - *.esp" is listed under the fix, not the original mod.')
        w('')
        w('_ALL MISSING deduplicated.txt is every line once - a filename only ever needs')
        w('recording once, so use that one if you are paying per character.')
        w('')
        w('%-52s %7s %7s  %s' % ('PLUGIN', 'TOPICS', 'MISSING', 'MOD'))
        for plug, mod, tot, miss in index:
            if miss:
                w('%-52s %7d %7d  %s' % (plug[:52], tot, miss, mod))
        if unvoiceable:
            w('')
            w('--- cannot be voiced: the topic text contains a line break or tab, so no legal')
            w('    Windows filename exists for it. Left out of the topic files. ---')
            for plug, line in sorted(set(unvoiceable)):
                w('%-52s %s' % (plug[:52], line.replace('\r', ' ').replace('\n', ' ')[:150]))
        w('')
        w('--- fully covered already ---')
        for plug, mod, tot, miss in sorted(index, key=lambda r: r[0].lower()):
            if not miss:
                w('%-52s %7d        0  %s' % (plug[:52], tot, mod))
    json.dump([{'plugin': p, 'mod': m, 'topics': t, 'missing': ms} for p, m, t, ms in index],
              open('gen2_index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.stderr.write('%d files, %d lines, %d unique (ignored by .pas rules: %d)\n'
                     % (nfiles, len(allmiss), len(dedup), dropped))


if __name__ == '__main__':
    main()
