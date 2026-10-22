"""Read-only: line-level diff of every installed fork ini vs the live Darkened source; classify (section, key, period);
check ranges ([0,10] colour, [0,1000] GVR Intensity), CRLF, line counts, bare keys of the changed settings."""
import os, re, glob, collections, json
H = os.path.dirname(os.path.abspath(__file__))
LP = chr(92) * 2 + '?' + chr(92)
DARK = r'C:\1. AUTHORIA\mods\Authoria - Picta 1.1.2 - Darkened to 1.0.1'
FORK = r'C:\1. AUTHORIA\mods\Authoria - Picta x Astralite - E11'
PER = ['Dawn', 'Sunrise', 'Day', 'Sunset', 'Dusk', 'Night', 'InteriorDay', 'InteriorNight']


def rd(p):
    return open(LP + p, 'rb').read()


def sec_lines(b):
    t = b.decode('utf-8', 'replace')
    sec = None
    out = []
    for i, l in enumerate(t.split('\r\n')):
        s = l.strip()
        m = re.match(r'^\[(.+)\]$', s)
        if m:
            sec = m.group(1)
        out.append((sec, s))
    return out


def splitkey(k):
    for p in sorted(PER, key=len, reverse=True):
        if k.endswith(p):
            return k[:-len(p)], p
    return k, ''


cls = collections.Counter()
rng = []
bad = []
files = 0
changed_keys = collections.defaultdict(set)
for fp in [os.path.join(FORK, 'enbseries.ini'), os.path.join(FORK, 'Picta - Weathers of Aurbis.ini')] + glob.glob(FORK + r'\enbseries\**\*.ini', recursive=True):
    rel = os.path.relpath(fp, FORK)
    src = os.path.join(DARK, rel)
    if not os.path.exists(LP + src):
        continue
    a, b = rd(src), rd(fp)
    if a == b:
        continue
    files += 1
    if a.count(b'\r\n') != b.count(b'\r\n') or a.count(b'\n') != b.count(b'\n'):
        bad.append(('LINECOUNT/CRLF', rel))
    A, B = sec_lines(a), sec_lines(b)
    if len(A) != len(B):
        bad.append(('LEN', rel))
        continue
    for (sa, la), (sb, lb) in zip(A, B):
        if la == lb:
            continue
        if sa != sb or '=' not in la or '=' not in lb:
            bad.append(('STRUCT', rel, la, lb))
            continue
        ka, va = la.split('=', 1)
        kb, vb = lb.split('=', 1)
        if ka != kb:
            bad.append(('KEY', rel, la, lb))
            continue
        base, per = splitkey(kb)
        cls[(sb, base, per)] += 1
        changed_keys[rel].add((sb, kb))
        try:
            vals = [float(x) for x in vb.split(',')]
        except ValueError:
            bad.append(('PARSE', rel, lb))
            continue
        if len(vals) == 3:
            if min(vals) < 0 or max(vals) > 10:
                rng.append((rel, sb, kb, vb))
        else:
            if sb == 'GAMEVOLUMETRICRAYS' and base == 'Intensity' and not (0 <= vals[0] <= 1000):
                rng.append((rel, sb, kb, vb))
print('changed files', files)
for k, n in sorted(cls.items()):
    print(k, n)
print('out of range', rng)
print('bad', bad[:20])
# bare keys of changed settings anywhere in fork weather files or base
bare = []
for fp in [os.path.join(FORK, 'enbseries.ini')] + glob.glob(FORK + r'\enbseries\**\*.ini', recursive=True):
    sec = None
    for l in rd(fp).decode('utf-8', 'replace').splitlines():
        s = l.strip()
        m = re.match(r'^\[(.+)\]$', s)
        if m:
            sec = m.group(1)
            continue
        if '=' in s and not s.startswith(';'):
            k = s.split('=', 1)[0].strip()
            for (S, base, per) in cls:
                if sec == S and k.lower() == base.lower():
                    bare.append((os.path.relpath(fp, FORK), sec, k))
print('bare keys of changed settings:', bare[:20])
