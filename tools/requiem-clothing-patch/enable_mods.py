"""Register + enable the 2026-09-03 outfit mods in every MO2 profile (MO2 closed).

modlist.txt (descending priority; a line inserted AFTER an anchor sits just below it in priority):
  Magic Pariah - Meadowlark Physics, Burlesque Dress        -> after "+Sera's Armor"
  Authoria - BodySlide Group - Magic Pariah and Burlesque   -> before "Authoria - Ninirim and Cute Adventurer - BodySlide Groups"
  Authoria - Magic Pariah and Burlesque - Requiem Clothing  -> after "Authoria - Ninirim and Cute Adventurer - Requiem Clothing"
  enabled in the four profiles where Sera's Armor is enabled, disabled in the two Requiem Reforged profiles;
  the four stray lines MO2/houseCARL left at the top of the PBR modlist are removed.
loadorder.txt / plugins.txt / plugingroups.txt (enabled profiles only):
  Magic Pariah.esp, Burlesque.esp                            -> after KW_SerasArmor.esp   (Gameplay - Armors and Weapons)
  Authoria - Burlesque Dress - Requiem Clothing.esp          -> after Authoria - Reqtificated - Armor Folder.esp (Authoria - Reqtificated)
Backups: <file>.bak-pariah-20260903 beside each file. Verifies the protected blocks and header runs after writing.
"""
import os, shutil, sys

ROOT = r"C:\1. AUTHORIA\profiles"
TAG = 'bak-pariah-20260903'
ENABLED = {'DEEEZ NUTTZZZ', 'DEEZ CS NUTZ', 'DEEZ CS NUTZ - PBR', 'PICTA EXPERIMENT'}
DISABLED = {'Authoria - Requiem Reforged - Main Profile', 'Authoria - Requiem Reforged - NSFW Profile'}
MODS = ['Magic Pariah - Meadowlark Physics', 'Burlesque Dress',
        'Authoria - BodySlide Group - Magic Pariah and Burlesque',
        'Authoria - Magic Pariah and Burlesque - Requiem Clothing']
PLUGINS = [('Magic Pariah.esp', 'KW_SerasArmor.esp', 'Gameplay - Armors and Weapons'),
           ('Burlesque.esp', 'Magic Pariah.esp', 'Gameplay - Armors and Weapons'),
           ('Authoria - Burlesque Dress - Requiem Clothing.esp', 'Authoria - Reqtificated - Armor Folder.esp', 'Authoria - Reqtificated')]
APPLY = '--apply' in sys.argv


def read(p):
    raw = open(p, 'rb').read()
    assert b'\r\n' in raw, p
    return raw.decode('utf-8').split('\r\n')


def write(p, lines):
    if not APPLY:
        return
    bak = p + '.' + TAG
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write('\r\n'.join(lines).encode('utf-8'))


def insert_after(lines, anchor, new, before=False):
    idx = [i for i, l in enumerate(lines) if l == anchor]
    assert len(idx) == 1, (anchor, len(idx))
    i = idx[0] if before else idx[0] + 1
    for k, n in enumerate(new):
        lines.insert(i + k, n)


def header_runs(lo_lines, groups):
    """MO2 pane replica: count group runs across loadorder (inactive included)."""
    runs = {}; prev = None
    for l in lo_lines:
        if not l or l.startswith('#'):
            continue
        g = groups.get(l, '<ungrouped>')
        if g != prev:
            runs[g] = runs.get(g, 0) + 1; prev = g
    return runs


report = []
for prof in sorted(os.listdir(ROOT)):
    pdir = os.path.join(ROOT, prof)
    if not os.path.isdir(pdir) or prof not in ENABLED | DISABLED:
        continue
    sign = '+' if prof in ENABLED else '-'
    ml_p = os.path.join(pdir, 'modlist.txt')
    ml = read(ml_p)
    protected_before = [l for l in ml[:60] if l not in ['-' + m for m in MODS] + ['+' + m for m in MODS]]
    # remove any existing lines for our mods (the stray top-of-file registrations)
    stray = [l for l in ml if l[1:] in MODS]
    ml = [l for l in ml if l[1:] not in MODS]
    # anchor next to Sera's Armor in the curated armor block; in the two profiles that PARK Sera's
    # Armor disabled at the top of the file, fall back to the block's separator instead
    sera = [i for i, l in enumerate(ml) if l[1:] == "Sera's Armor"]
    if sera and sera[0] > 100:
        insert_after(ml, ml[sera[0]], [sign + 'Magic Pariah - Meadowlark Physics', sign + 'Burlesque Dress'])
    else:
        insert_after(ml, '-Armor and Weapons - Modded_separator',
                     [sign + 'Magic Pariah - Meadowlark Physics', sign + 'Burlesque Dress'], before=True)
    anc = [l for l in ml if l[1:] == 'Authoria - Ninirim and Cute Adventurer - BodySlide Groups']
    insert_after(ml, anc[0], [sign + 'Authoria - BodySlide Group - Magic Pariah and Burlesque'], before=True)
    anc = [l for l in ml if l[1:] == 'Authoria - Ninirim and Cute Adventurer - Requiem Clothing']
    insert_after(ml, anc[0], [sign + 'Authoria - Magic Pariah and Burlesque - Requiem Clothing'])
    # protected head must be unchanged apart from the stray removals
    head_after = [l for l in ml[:60 - len(stray)]]
    assert protected_before[:len(head_after)] == head_after[:len(protected_before)], prof
    assert sum(1 for l in ml if l[1:] in MODS) == 4
    write(ml_p, ml)
    pos = {m: next(i for i, l in enumerate(ml) if l[1:] == m) + 1 for m in MODS}
    report.append('%-45s modlist: %s stray removed=%d  lines %s' % (prof, sign, len(stray), pos))

    if prof in DISABLED:
        continue
    lo_p = os.path.join(pdir, 'loadorder.txt'); pl_p = os.path.join(pdir, 'plugins.txt'); pg_p = os.path.join(pdir, 'plugingroups.txt')
    lo = read(lo_p); pl = read(pl_p); pg = read(pg_p)
    groups = dict(l.split('|', 1) for l in pg if l and not l.startswith('#'))
    runs_before = header_runs(lo, groups)
    for name, anchor, group in PLUGINS:
        assert name not in lo and ('*' + name) not in pl and name not in pl, (prof, name, 'already present')
        insert_after(lo, anchor, [name])
        anc_pl = '*' + anchor if ('*' + anchor) in pl else anchor
        assert anc_pl in pl, (prof, anchor)
        insert_after(pl, anc_pl, ['*' + name])
        assert groups.get(anchor) == group, (prof, anchor, groups.get(anchor))
        groups[name] = group
        # alphabetical insert into plugingroups (same collation as neighbours: plain string compare)
        entry = name + '|' + group
        body = [l for l in pg if l and not l.startswith('#')]
        k = next((i for i, l in enumerate(body) if l.split('|', 1)[0].lower() > name.lower()), len(body))
        body.insert(k, entry)
        pg = [pg[0]] + body + ([''] if pg[-1] == '' else [])
    runs_after = header_runs(lo, groups)
    assert runs_after == runs_before, (prof, {g: (runs_before.get(g), runs_after.get(g)) for g in set(runs_before) | set(runs_after) if runs_before.get(g) != runs_after.get(g)})
    tail_anchor = 'Authoria - Output - Synthesis Gameplay.esp'
    ti = lo.index(tail_anchor)
    assert not any(n in lo[ti:] for n, _, _ in PLUGINS)
    write(lo_p, lo); write(pl_p, pl); write(pg_p, pg)
    lpos = {n: lo.index(n) + 1 for n, _, _ in PLUGINS}
    report.append('%-45s plugins: loadorder %s | header runs unchanged (%d groups)' % ('', lpos, len(runs_after)))

print('APPLIED' if APPLY else 'DRY RUN')
for r in report:
    print(' ', r)
