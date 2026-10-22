"""Topic files for the player lines that still have no .fuz anywhere.

Built from the load order, not from the old topic files: every winning player topic,
named by the corrected rule in dbvoname.py, minus everything the installed pack now
holds. Same format as the originals - CP1252, CRLF, sorted and de-duplicated under
Windows collation, one line per topic.
"""
import os, sys, pickle, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pasrepro, vfs
from dbvoname import dbvo_name

B = chr(92)
LONG = lambda p: B + B + '?' + B + os.path.normpath(p)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = 'D:/1. MOD STUFF/1. SKYRIM FILES/- 1 TOOLS/z. DBVO crap'
PACK = LONG('C:/1. AUTHORIA/mods/Eleonora Female Nord Dbvo Pack With Patches/Sound/DBVO/elnordvoice')
OUT = os.path.normpath(ROOT + '/topic files still missing 20260828-run2')


def main():
    have = {n.lower() for n in os.listdir(PACK)}
    d = pickle.load(open(os.path.join(HERE, 'attribute.pkl'), 'rb'))
    nm, txt = d['name_mods'], d['name_text']

    per = collections.defaultdict(list)
    total = 0
    for k, mods in nm.items():
        if k in have:
            continue
        line = txt.get(k, '')
        if not line or not line.strip():
            continue
        total += 1
        for plugins in mods.values():
            for plug in plugins:
                per['topic files%s.txt' % os.path.splitext(plug)[0]].append(line)

    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            os.remove(os.path.join(OUT, f))
    else:
        os.makedirs(OUT)

    allines = []
    for fn, lines in per.items():
        srt = pasrepro.sorted_stringlist(lines)
        pasrepro.write_topic_file(os.path.join(OUT, fn), srt)
        allines.extend(srt)
    dedup = pasrepro.sorted_stringlist(allines)
    pasrepro.write_topic_file(os.path.join(OUT, '_ALL STILL MISSING deduplicated.txt'), dedup)

    with open(os.path.join(OUT, '_INDEX.txt'), 'wb') as f:
        f.write(('Player lines with no .fuz in the pack, after the 2026-08-28 run.\r\n'
                 '%d unique lines across %d plugins.\r\n'
                 'Names use the corrected rule: the trailing " (Persuade)" style tag is\r\n'
                 'dropped before the filename is built.\r\n\r\n'
                 % (len(dedup), len(per))).encode('cp1252', 'replace'))
        for fn, lines in sorted(per.items(), key=lambda kv: -len(kv[1])):
            f.write(('%5d  %s\r\n' % (len(lines), fn)).encode('cp1252', 'replace'))
    sys.stderr.write('%d plugins, %d unique lines -> %s\n' % (len(per), len(dedup), OUT))


if __name__ == '__main__':
    main()
