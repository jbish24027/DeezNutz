"""Simulate an MO2 profile's VFS for Data-root files. modlist.txt lists highest priority FIRST."""
import os, sys
ROOT = r'C:\1. AUTHORIA'
MODS = os.path.join(ROOT, 'mods')
DATA = os.path.join(ROOT, 'Stock Game', 'Data')
OVERWRITE = os.path.join(ROOT, 'overwrite')

def enabled_mods(profile):
    lines = open(os.path.join(ROOT, 'profiles', profile, 'modlist.txt'), encoding='utf-8-sig').read().splitlines()
    out = []
    for l in lines:
        if l.startswith('+') and not l.endswith('_separator'):
            out.append(l[1:])
    return out  # highest priority first

def providers(profile, relpath):
    res = []
    if os.path.exists(os.path.join(OVERWRITE, relpath)):
        res.append(('overwrite', os.path.join(OVERWRITE, relpath)))
    for m in enabled_mods(profile):
        p = os.path.join(MODS, m, relpath)
        if os.path.exists(p):
            res.append((m, p))
    p = os.path.join(DATA, relpath)
    if os.path.exists(p):
        res.append(('Data', p))
    return res

def winner(profile, relpath):
    r = providers(profile, relpath)
    return r[0] if r else None

if __name__ == '__main__':
    prof = sys.argv[1]
    for f in sys.argv[2:]:
        print(f, '->', providers(prof, f))
