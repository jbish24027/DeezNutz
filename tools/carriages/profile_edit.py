"""Edit every profile's modlist/plugins/loadorder/plugingroups in lockstep from a JSON spec. Re-reads every file fresh,
keeps each file's own line endings and BOM, refuses if any anchor is missing, verifies after writing.
spec = {
  "mods_before": [[anchor_mod_name, [names...]], ...],   # insert lines just BEFORE the anchor line (= higher priority);
                                                          # each name may start with + or -; '=' means copy the anchor's state
  "mods_before_first_of": [[[anchor candidates], [names]]],
  "mods_set": {name: "+"|"-"},
  "plugins_after": [[anchor_plugin, [plugins...]]],       # loadorder + plugins.txt (active '*') right after anchor
  "groups": {plugin: group}
}
usage: profile_edit.py spec.json [--write]"""
import os, sys, json, time
WRITE = '--write' in sys.argv
ROOT = r'C:\1. AUTHORIA\profiles'
spec = json.load(open(sys.argv[1], encoding='utf-8'))


def rd(p):
    b = open(p, 'rb').read()
    bom = b.startswith(b'\xef\xbb\xbf')
    t = b[3:].decode('utf-8') if bom else b.decode('utf-8')
    eol = '\r\n' if '\r\n' in t else '\n'
    trail = t.endswith(eol)
    lines = t.split(eol)
    if trail: lines = lines[:-1]
    return dict(bom=bom, eol=eol, trail=trail, lines=lines, mtime=os.path.getmtime(p))


def wr(p, f):
    t = f['eol'].join(f['lines']) + (f['eol'] if f['trail'] else '')
    b = (b'\xef\xbb\xbf' if f['bom'] else b'') + t.encode('utf-8')
    tmp = p + '.tmp-carriage'
    open(tmp, 'wb').write(b); os.replace(tmp, p)


def idx_mod(lines, name):
    for i, l in enumerate(lines):
        if l[1:] == name and l[:1] in '+-': return i
    return -1


plan = {}
for prof in sorted(os.listdir(ROOT)):
    pd = os.path.join(ROOT, prof)
    if not os.path.isdir(pd): continue
    F = {n: rd(os.path.join(pd, n)) for n in ('modlist.txt', 'plugins.txt', 'loadorder.txt', 'plugingroups.txt')}
    ml = F['modlist.txt']['lines']
    log = []
    for anchor, names in spec.get('mods_before', []):
        i = idx_mod(ml, anchor)
        if i < 0: sys.exit('REFUSE %s: anchor mod missing: %s' % (prof, anchor))
        st = ml[i][0]
        new = [(st + n[1:]) if n.startswith('=') else n for n in names]
        for n in new:
            if idx_mod(ml, n[1:]) >= 0: sys.exit('REFUSE %s: mod already listed: %s' % (prof, n[1:]))
        ml[i:i] = new; log.append('mods %s before %s' % (new, anchor))
    for cands, names in spec.get('mods_before_first_of', []):
        hits = [idx_mod(ml, c) for c in cands]; hits = [h for h in hits if h >= 0]
        if not hits: sys.exit('REFUSE %s: none of %s' % (prof, cands))
        i = min(hits)
        for n in names:
            if idx_mod(ml, n[1:]) >= 0: sys.exit('REFUSE %s: mod already listed: %s' % (prof, n[1:]))
        ml[i:i] = names; log.append('mods %s before %s' % (names, ml[i + len(names)]))
    for name, st in spec.get('mods_set', {}).items():
        i = idx_mod(ml, name)
        if i < 0: sys.exit('REFUSE %s: mod missing for state set: %s' % (prof, name))
        if ml[i][0] != st: log.append('%s %s -> %s' % (name, ml[i][0], st)); ml[i] = st + name
    lo = F['loadorder.txt']['lines']; pl = F['plugins.txt']['lines']
    for anchor, plugs in spec.get('plugins_after', []):
        low = [x.lower() for x in lo]
        if anchor.lower() not in low: sys.exit('REFUSE %s: anchor plugin missing in loadorder: %s' % (prof, anchor))
        for p in plugs:
            if p.lower() in low: sys.exit('REFUSE %s: plugin already in loadorder: %s' % (prof, p))
        i = low.index(anchor.lower()); lo[i + 1:i + 1] = plugs
        pk = [x.lstrip('*').lower() for x in pl]
        if anchor.lower() not in pk: sys.exit('REFUSE %s: anchor plugin missing in plugins.txt: %s' % (prof, anchor))
        j = pk.index(anchor.lower()); pl[j + 1:j + 1] = ['*' + p for p in plugs]
        log.append('plugins %s after %s' % (plugs, anchor))
    g = F['plugingroups.txt']['lines']
    for p, grp in spec.get('groups', {}).items():
        if any(x.split('|')[0].lower() == p.lower() for x in g): continue
        body = list(range(1, len(g)))
        k = next((i for i in body if g[i] and not g[i].startswith('#') and g[i].split('|')[0].lower() > p.lower()), len(g))
        g.insert(k, '%s|%s' % (p, grp))
    plan[prof] = (pd, F, log)
    print('==', prof); [print('   ', x) for x in log]

if WRITE:
    for prof, (pd, F, log) in plan.items():
        for n, f in F.items():
            p = os.path.join(pd, n)
            if os.path.getmtime(p) != f['mtime']: sys.exit('REFUSE: %s changed on disk since read' % p)
    for prof, (pd, F, log) in plan.items():
        for n, f in F.items(): wr(os.path.join(pd, n), f)
    # verify
    for prof, (pd, F, log) in plan.items():
        for n, f in F.items():
            again = rd(os.path.join(pd, n))
            assert again['lines'] == f['lines'] and again['eol'] == f['eol'], 'verify failed ' + prof + n
    print('WRITTEN + verified', len(plan), 'profiles')
else:
    print('(dry run)')
