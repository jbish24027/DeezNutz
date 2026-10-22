"""Diff mod enable-state and plugin active-state between two profiles (read-only)."""
import os, sys
INST = r"C:/1. AUTHORIA/profiles"
a, b = sys.argv[1], sys.argv[2]

def mods(p):
    out = {}
    order = []
    for l in open(os.path.join(INST, p, 'modlist.txt'), encoding='utf-8-sig').read().splitlines():
        if not l or l.startswith('#') or l.endswith('_separator'):
            continue
        out[l[1:]] = l[0]
        order.append(l[1:])
    return out, order

def plugins(p):
    out = {}
    for l in open(os.path.join(INST, p, 'plugins.txt'), encoding='utf-8-sig').read().splitlines():
        if not l or l.startswith('#'):
            continue
        out[l.lstrip('*')] = l.startswith('*')
    return out

ma, oa = mods(a); mb, ob = mods(b)
print('MODS enabled in %s only:' % a)
for m in oa:
    if ma[m] == '+' and mb.get(m) != '+':
        print('   +A  %-80s B=%s  (A line %d)' % (m, mb.get(m, 'absent'), oa.index(m) + 2))
print('MODS enabled in %s only:' % b)
for m in ob:
    if mb[m] == '+' and ma.get(m) != '+':
        print('   +B  %-80s A=%s  (B line %d)' % (m, ma.get(m, 'absent'), ob.index(m) + 2))
pa, pb = plugins(a), plugins(b)
print('PLUGINS active in %s only:' % a)
for p, v in pa.items():
    if v and not pb.get(p):
        print('   *A  %s  (B: %s)' % (p, 'inactive' if p in pb else 'absent'))
print('PLUGINS active in %s only:' % b)
for p, v in pb.items():
    if v and not pa.get(p):
        print('   *B  %s  (A: %s)' % (p, 'inactive' if p in pa else 'absent'))
# order differences for common mods
common = [m for m in oa if m in mb]
pos_b = {m: i for i, m in enumerate([m for m in ob if m in ma])}
moved = [m for i, m in enumerate(common) if pos_b.get(m) != i]
print('common mods %d, relative-order mismatches (rough) %d' % (len(common), len(moved)))
