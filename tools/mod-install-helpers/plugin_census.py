"""Full-vs-light plugin census per MO2 profile (winner resolved by modlist rank).
Usage: python plugin_census.py [profile name ...]
"""
import os, sys, struct

INST = r"C:\1. AUTHORIA"
MODS = os.path.join(INST, "mods")
DATA = os.path.join(INST, "Stock Game", "Data")


def is_light(path):
    with open(path, 'rb') as f:
        head = f.read(12)
    if len(head) < 12 or head[:4] != b'TES4':
        return None
    flags = struct.unpack_from('<I', head, 8)[0]
    return bool(flags & 0x200) or path.lower().endswith('.esl')


def profile_census(prof):
    pdir = os.path.join(INST, 'profiles', prof)
    modlist = [l.rstrip('\n') for l in open(os.path.join(pdir, 'modlist.txt'), encoding='utf-8-sig')]
    # enabled mods with rank (line index; lower = higher priority)
    enabled = {}
    for i, l in enumerate(modlist):
        if l.startswith('+'):
            enabled[l[1:]] = i
    plugins = [l.rstrip('\n') for l in open(os.path.join(pdir, 'plugins.txt'), encoding='utf-8-sig')]
    active = [l[1:] for l in plugins if l.startswith('*')]
    # index: plugin filename (lower) -> list of (rank, modname, path)
    idx = {}
    for m, rank in enabled.items():
        mp = os.path.join(MODS, m)
        try:
            for e in os.listdir(mp):
                el = e.lower()
                if el.endswith(('.esp', '.esm', '.esl')):
                    idx.setdefault(el, []).append((rank, m, os.path.join(mp, e)))
        except FileNotFoundError:
            pass
    full = []
    light = []
    unresolved = []
    for p in active:
        cands = idx.get(p.lower())
        if cands:
            cands.sort()
            path = cands[0][2]
            src = cands[0][1]
        else:
            path = os.path.join(DATA, p)
            src = 'Stock Game Data'
            if not os.path.exists(path):
                unresolved.append(p)
                continue
        li = is_light(path)
        if li is None:
            unresolved.append(p + ' (bad header)')
        elif li:
            light.append((p, src))
        else:
            full.append((p, src))
    # implicit plugins: game Data masters + CC (not in plugins.txt); check winners in enabled mods too
    implicit_full = []
    implicit_light = []
    active_lower = set(a.lower() for a in active)
    # implicit = 5 base masters + every cc*.esm/.esl visible in Data or an enabled mod (engine force-loads them)
    names = set()
    for e in os.listdir(DATA):
        names.add(e.lower())
    for k in idx.keys():
        names.add(k)
    for el in sorted(names):
        if not el.endswith(('.esm', '.esl', '.esp')) or el in active_lower:
            continue
        base = el in ('skyrim.esm', 'update.esm', 'dawnguard.esm', 'hearthfires.esm', 'dragonborn.esm')
        if base or el.startswith('cc'):
            cands = idx.get(el)
            if cands:
                cands.sort()
                path = cands[0][2]
                src = cands[0][1]
            else:
                path = os.path.join(DATA, el)
                src = 'Stock Game Data'
                if not os.path.exists(path):
                    continue
            li = is_light(path)
            if li:
                implicit_light.append((el, src))
            else:
                implicit_full.append((el, src))
    return {
        'active': len(active), 'full': full, 'light': light, 'unresolved': unresolved,
        'implicit_full': implicit_full, 'implicit_light': implicit_light,
    }


if __name__ == '__main__':
    profs = sys.argv[1:] or sorted(os.listdir(os.path.join(INST, 'profiles')))
    for prof in profs:
        r = profile_census(prof)
        tot_full = len(r['full']) + len(r['implicit_full'])
        print('== %s: active plugins in plugins.txt=%d | starred FULL=%d, starred LIGHT=%d | implicit FULL=%d, implicit LIGHT=%d | TOTAL FULL SLOTS=%d / 254 | unresolved=%d' % (
            prof, r['active'], len(r['full']), len(r['light']), len(r['implicit_full']), len(r['implicit_light']), tot_full, len(r['unresolved'])))
        for u in r['unresolved']:
            print('     unresolved:', u)
        if '-v' in sys.argv:
            for p, s in r['implicit_full']:
                print('     implicit full:', p, '<-', s)
