"""Read-only: simulate MO2 VFS winners for E11-relevant paths for a profile."""
import os, sys, json
INST = r'C:\1. AUTHORIA'
LP = chr(92) * 2 + '?' + chr(92)
SEP = chr(92)


def enabled(profile):
    L = open(os.path.join(INST, 'profiles', profile, 'modlist.txt'), encoding='utf-8-sig').read().splitlines()
    return [l[1:] for l in L if l.startswith('+')]  # highest priority first


def relevant(rel):
    r = rel.replace('/', SEP).lower()
    return (r.startswith('enbseries' + SEP) or r == 'enbseries.ini' or r == 'picta - weathers of aurbis.ini'
            or r.startswith('root' + SEP + 'enb') or r.startswith('skse' + SEP + 'plugins' + SEP + 'communityshaders'))


def walk(base):
    for dp, dn, fn in os.walk(LP + base):
        for f in fn:
            p = os.path.join(dp, f)[len(LP):]
            yield os.path.relpath(p, base)


prof = sys.argv[1]
mods = enabled(prof)
win = {}
ov = os.path.join(INST, 'overwrite')
for rel in walk(ov):
    if relevant(rel):
        win.setdefault(rel.lower(), ('<overwrite>', rel))
for m in mods:
    base = os.path.join(INST, 'mods', m)
    if not os.path.isdir(LP + base):
        continue
    for rel in walk(base):
        if relevant(rel):
            win.setdefault(rel.lower(), (m, rel))
cnt = {}
for k, (m, rel) in win.items():
    cnt[m] = cnt.get(m, 0) + 1
print(prof)
for m, n in sorted(cnt.items(), key=lambda kv: -kv[1]):
    print('  ', n, m)
json.dump(win, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vfs_' + prof.replace(' ', '_') + '.json'), 'w'), indent=0)
