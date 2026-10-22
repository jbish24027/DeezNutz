"""Classify every FULL plugin in a profile for ESL-ability.
Class A = 0 originating records (override-only)  -> flag-only, save-safe
Class B = all originating FormIDs already in 0x800-0xFFF -> flag-only valid (index change!)
Class C = <=2048 originating records but out of range -> needs COMPACTION (renumber)
Class D = >2048 originating records -> cannot be ESL
"""
import os, sys, struct

INST = r"C:\1. AUTHORIA"
MODS = os.path.join(INST, "mods")
DATA = os.path.join(INST, "Stock Game", "Data")
PROF = sys.argv[1] if len(sys.argv) > 1 else "DEEZ CS NUTZ"

def build_index(prof):
    pdir = os.path.join(INST, 'profiles', prof)
    modlist = [l.rstrip('\n') for l in open(os.path.join(pdir, 'modlist.txt'), encoding='utf-8-sig')]
    enabled = {l[1:]: i for i, l in enumerate(modlist) if l.startswith('+')}
    plugins = [l.rstrip('\n') for l in open(os.path.join(pdir, 'plugins.txt'), encoding='utf-8-sig')]
    active = [l[1:] for l in plugins if l.startswith('*')]
    idx = {}
    for m, rank in enabled.items():
        mp = os.path.join(MODS, m)
        try:
            for e in os.listdir(mp):
                if e.lower().endswith(('.esp', '.esm', '.esl')):
                    idx.setdefault(e.lower(), []).append((rank, m, os.path.join(mp, e)))
        except FileNotFoundError:
            pass
    for v in idx.values():
        v.sort()
    return active, idx

def winner(p, idx):
    c = idx.get(p.lower())
    if c:
        return c[0][2], c[0][1]
    d = os.path.join(DATA, p)
    return (d, 'Stock Game Data') if os.path.exists(d) else (None, None)

def parse(path):
    """return (is_light, nmasters, originating_formids set, override_count, total_records)"""
    with open(path, 'rb') as f:
        buf = f.read()
    if buf[:4] != b'TES4':
        return None
    dsz = struct.unpack_from('<I', buf, 4)[0]
    flags = struct.unpack_from('<I', buf, 8)[0]
    light = bool(flags & 0x200) or path.lower().endswith('.esl')
    # count MAST in TES4 data
    p = 24
    end = 24 + dsz
    nm = 0
    while p < end:
        sig = buf[p:p+4]; sz = struct.unpack_from('<H', buf, p+4)[0]
        if sig == b'MAST':
            nm += 1
        p += 6 + sz
    own = nm
    orig = set(); ovr = 0; tot = 0
    def walk(a, b):
        nonlocal ovr, tot
        while a + 24 <= b:
            sig = buf[a:a+4]
            sz = struct.unpack_from('<I', buf, a+4)[0]
            if sig == b'GRUP':
                walk(a + 24, a + sz)
                a += sz
            else:
                fid = struct.unpack_from('<I', buf, a+12)[0]
                tot += 1
                if (fid >> 24) >= own:
                    orig.add(fid & 0xFFFFFF)
                else:
                    ovr += 1
                a += 24 + sz
    walk(end, len(buf))
    return light, nm, orig, ovr, tot

active, idx = build_index(PROF)
rows = []
for p in active:
    path, src = winner(p, idx)
    if not path:
        continue
    try:
        r = parse(path)
    except Exception as e:
        print('ERR', p, e); continue
    if r is None:
        continue
    light, nm, orig, ovr, tot = r
    if light:
        continue
    n = len(orig)
    if n == 0:
        cls = 'A'
    elif orig and max(orig) <= 0xFFF and min(orig) >= 0x800:
        cls = 'B'
    elif n <= 2048:
        cls = 'C'
    else:
        cls = 'D'
    rows.append((cls, n, ovr, tot, os.path.getsize(path), p, src, path,
                 (hex(min(orig)), hex(max(orig))) if orig else ('-', '-')))

order = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
rows.sort(key=lambda r: (order[r[0]], r[1], r[4]))
from collections import Counter
print('profile:', PROF, '| FULL plugins:', len(rows))
print(Counter(r[0] for r in rows))
print()
for cls, n, ovr, tot, size, p, src, path, rng in rows:
    print('%s | orig=%-5d ovr=%-6d tot=%-6d %7dKB | %-58s | %s | %s..%s' % (
        cls, n, ovr, tot, size//1024, p[:58], src[:44], rng[0], rng[1]))
