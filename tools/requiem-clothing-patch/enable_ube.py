"""Register + enable the two UBE converter output mods and their plugins (MO2 closed).

modlist.txt: both output mods inserted directly before (= one priority step above)
  "Authoria - UBE Converter Output - Sera", enabled where that mod is enabled, disabled where it is not.
loadorder/plugins/plugingroups (profiles that carry KW_SerasArmor UBE patch.esp):
  Magic Pariah UBE patch.esp, Burlesque UBE patch.esp after KW_SerasArmor UBE patch.esp, group "Authoria - Outputs".
Backups: <file>.bak-ube-20260903. Dry run by default, --apply to write.
"""
import os, shutil, sys

ROOT = r"C:\1. AUTHORIA\profiles"
TAG = 'bak-ube-20260903'
MODS = ['Authoria - UBE Converter Output - Magic Pariah', 'Authoria - UBE Converter Output - Burlesque']
MOD_ANCHOR = 'Authoria - UBE Converter Output - Sera'
PLUGINS = [('Magic Pariah UBE patch.esp', 'KW_SerasArmor UBE patch.esp', 'Authoria - Outputs'),
           ('Burlesque UBE patch.esp', 'Magic Pariah UBE patch.esp', 'Authoria - Outputs')]
APPLY = '--apply' in sys.argv


def read(p):
    raw = open(p, 'rb').read(); assert b'\r\n' in raw, p
    return raw.decode('utf-8').split('\r\n')


def write(p, lines):
    if not APPLY:
        return
    bak = p + '.' + TAG
    if not os.path.exists(bak):
        shutil.copy2(p, bak)
    open(p, 'wb').write('\r\n'.join(lines).encode('utf-8'))


def header_runs(lo_lines, groups):
    runs = {}; prev = None
    for l in lo_lines:
        if not l or l.startswith('#'):
            continue
        g = groups.get(l, '<ungrouped>')
        if g != prev:
            runs[g] = runs.get(g, 0) + 1; prev = g
    return runs


for prof in sorted(os.listdir(ROOT)):
    pdir = os.path.join(ROOT, prof)
    if not os.path.isdir(pdir):
        continue
    ml_p = os.path.join(pdir, 'modlist.txt'); ml = read(ml_p)
    anchor = [l for l in ml if l[1:] == MOD_ANCHOR]
    assert len(anchor) == 1, (prof, anchor)
    sign = anchor[0][0]
    stray = [l for l in ml if l[1:] in MODS]
    ml = [l for l in ml if l[1:] not in MODS]
    i = ml.index(anchor[0])
    for k, m in enumerate(MODS):
        ml.insert(i + k, sign + m)
    assert ml[:37] == read(ml_p)[:37] or stray, prof   # protected head unchanged (unless a stray sat there)
    write(ml_p, ml)
    print('%-45s modlist %s at lines %s (stray removed %d)' % (prof, sign, [ml.index(sign + m) + 1 for m in MODS], len(stray)))
    lo_p = os.path.join(pdir, 'loadorder.txt'); pl_p = os.path.join(pdir, 'plugins.txt'); pg_p = os.path.join(pdir, 'plugingroups.txt')
    lo = read(lo_p); pl = read(pl_p); pg = read(pg_p)
    if PLUGINS[0][1] not in lo:
        print('%-45s no Sera UBE patch plugin here - plugins not added' % '')
        continue
    groups = dict(l.split('|', 1) for l in pg if l and not l.startswith('#'))
    before = header_runs(lo, groups)
    for name, anc, group in PLUGINS:
        assert name not in lo and ('*' + name) not in pl and name not in pl, (prof, name)
        lo.insert(lo.index(anc) + 1, name)
        anc_pl = '*' + anc if ('*' + anc) in pl else anc
        pl.insert(pl.index(anc_pl) + 1, '*' + name)
        assert groups[anc] == group, (prof, anc, groups[anc])
        groups[name] = group
        body = [l for l in pg if l and not l.startswith('#')]
        k = next((j for j, l in enumerate(body) if l.split('|', 1)[0].lower() > name.lower()), len(body))
        body.insert(k, name + '|' + group)
        pg = [pg[0]] + body + ([''] if pg[-1] == '' else [])
    after = header_runs(lo, groups)
    assert after == before, (prof, {g: (before.get(g), after.get(g)) for g in set(before) | set(after) if before.get(g) != after.get(g)})
    # still inside the UBE outputs block: adjacent to the anchor, and before PG / DynDOLOD / the FWMF maps
    assert lo.index(PLUGINS[0][0]) == lo.index(PLUGINS[0][1]) + 1, prof
    tail = [n for n in ('PG_1.esp', 'DynDOLOD.esp', 'Occlusion.esp', 'Authoria - Master Patch - FWMF.esp') if n in lo]
    assert tail and all(lo.index(t) > lo.index(PLUGINS[-1][0]) for t in tail), (prof, tail)
    write(lo_p, lo); write(pl_p, pl); write(pg_p, pg)
    print('%-45s plugins at loadorder %s | header runs unchanged' % ('', [lo.index(n) + 1 for n, _, _ in PLUGINS]))
print('APPLIED' if APPLY else 'DRY RUN')
