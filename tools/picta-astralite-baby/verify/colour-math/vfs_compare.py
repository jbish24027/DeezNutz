"""Read-only: compare the effective (VFS-winning) bytes of every E11-relevant path, PICTA vs baby."""
import os, json, hashlib
H = os.path.dirname(os.path.abspath(__file__))
INST = r'C:\1. AUTHORIA'
LP = chr(92) * 2 + '?' + chr(92)
A = json.load(open(os.path.join(H, 'vfs_DEEZ_CS_NUTZ_-_PICTA.json')))
B = json.load(open(os.path.join(H, 'vfs_DEEZ_CS_NUTZ_-_PICTA_x_ASTRALITE.json')))


def path(m, rel):
    return os.path.join(INST, 'overwrite', rel) if m == '<overwrite>' else os.path.join(INST, 'mods', m, rel)


def md5(p):
    return hashlib.md5(open(LP + p, 'rb').read()).hexdigest()


same = diff = 0
rows = []
for k in sorted(set(A) | set(B)):
    a, b = A.get(k), B.get(k)
    if a is None or b is None:
        rows.append(('ONLY_' + ('BABY' if a is None else 'PICTA'), k, a, b))
        continue
    ma, mb = md5(path(*a)), md5(path(*b))
    if ma == mb:
        same += 1
    else:
        diff += 1
        rows.append(('DIFF', k, a[0], b[0]))
print('same', same, 'diff', diff)
for r in rows:
    print(r)
print('--- non-SKSE winners from overwrite / raindrop / July DOF / MCM in baby')
for k, (m, rel) in sorted(B.items()):
    if m in ('<overwrite>', 'Authoria - Picta - Bottled raindrop', 'Authoria - Picta - July Depth of Field (AMON ADOF)', 'Authoria - MCM and INI Settings') and not k.startswith('skse'):
        print(m, rel)
