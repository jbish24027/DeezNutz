"""Regenerate MANIFEST.md5 over the whole export tree, then re-verify every shipped file against its live source."""
import os, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_export as B

OUT = B.OUT


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


# 1. manifest over everything except itself
lines = []
count = 0
total = 0
for dp, dn, fn in os.walk(OUT):
    for name in fn:
        p = os.path.join(dp, name)
        rel = os.path.relpath(p, OUT).replace('\\', '/')
        if rel == 'MANIFEST.md5':
            continue
        lines.append('%s *%s' % (md5(p), rel))
        count += 1
        total += os.path.getsize(p)
lines.sort(key=lambda x: x.split(' *', 1)[1])
with open(os.path.join(OUT, 'MANIFEST.md5'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')
print('manifest: %d files, %.1f MB' % (count, total / 1048576))

# 2. freshness: every shipped copy vs its live source, right now
def src_for(rel):
    parts = rel.split('/')
    if parts[0] in ('mods', 'optional'):
        return os.path.join(B.MODS, *parts[1:])
    if parts[0] == 'downloads':
        for folder, name in B.ARCHIVES:
            if name == parts[1]:
                return os.path.join(folder, name)
    if parts[0] == 'reference' and parts[1] == 'profile-snapshot':
        return os.path.join(B.PROFILE, *parts[3:])
    if parts[0] == 'reference' and parts[1] == 'tools':
        for src, name, skip in B.TOOL_DIRS:
            if name == parts[2]:
                return os.path.join(src, *parts[3:])
    if parts[0] == 'reference' and len(parts) == 2 and parts[1] in B.DOCS:
        return os.path.join(B.INSTANCE, parts[1])
    if parts[0] == 'overwrite-seed':
        for s, seed_rel in B.SEEDS:
            if seed_rel.replace('\\', '/') == '/'.join(parts[1:]):
                return s
    return None

stale = []
checked = 0
for l in lines:
    h, rel = l.split(' *', 1)
    s = src_for(rel)
    if s is None:
        continue
    checked += 1
    if not os.path.isfile(s) or md5(s) != h:
        stale.append(rel)
print('freshness: %d shipped files compared with the live instance, %d differ' % (checked, len(stale)))
for r in stale:
    print('  STALE', r)
