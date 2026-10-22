import pickle, csv, collections, io, os
import vfs, gen2, pasrepro

win = pickle.load(open('winners.pkl', 'rb'))
plain, brk = gen2.covered()
pp = vfs.plugin_paths()
modof = {p.lower(): m for p, (q, m) in pp.items()}

rows, tot = [], collections.Counter()
for (key, kind), (plug, raw, edid, fid) in win.items():
    if not raw:
        continue
    line = raw.strip()
    if not line or pasrepro.should_ignore(line, edid, fid):
        continue
    if any(c in line for c in '\r\n\t'):
        continue
    mod = modof.get(plug.lower(), '?')
    tot[mod] += 1
    f = gen2.fuzname(line)
    if f in plain or f in brk:
        continue
    rows.append((mod, plug, line.translate(gen2.TRANS) + '.fuz', line))

seen, ded = set(), []
for r in rows:
    k = (r[1].lower(), r[2].lower())
    if k in seen:
        continue
    seen.add(k)
    ded.append(r)
ded.sort(key=lambda r: (r[0].lower(), r[1].lower(), r[2].lower()))
with open(r'C:\1. AUTHORIA\ELEONORA-DBVO-MISSING-LINES-20260828.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['mod', 'plugin', 'target_filename', 'text'])
    w.writerows(ded)

c = collections.Counter(r[0] for r in ded)
o = io.StringIO()


def tbl(rs):
    o.write('| Missing | Live topics | Covered | Mod |\n|---:|---:|---:|---|\n')
    for m, n in rs:
        t = tot.get(m, n)
        o.write('| %d | %d | %d%% | %s |\n' % (n, t, 100 * (t - n) // max(t, 1), m))
    o.write('\n')


ranked = c.most_common()
o.write('## Big jobs (100+ lines)\n\n');  tbl([x for x in ranked if x[1] >= 100])
o.write('## Medium (20-99 lines)\n\n');   tbl([x for x in ranked if 20 <= x[1] < 100])
o.write('## Small (3-19 lines)\n\n');     tbl([x for x in ranked if 3 <= x[1] < 20])
o.write('## One or two lines each\n\n')
o.write(', '.join(m for m, n in ranked if n < 3) + '\n')
open('tables3.md', 'w', encoding='utf-8').write(o.getvalue())
print('csv rows %d | mods with gaps %d | live strings %d' % (len(ded), len(c), sum(tot.values())))
