import os, sys
inst = r"C:/1. AUTHORIA/mods/[NoDelete] Bottled Shaders/Shaders"
src = sys.argv[1] if len(sys.argv) > 1 else "src"
pairs = []
for root, dirs, files in os.walk(src):
    for f in files:
        p = os.path.join(root, f).replace(os.sep, '/')
        rel = p[len(src) + 1:]
        if rel.startswith('package/Shaders/'):
            ip = inst + '/' + rel[len('package/Shaders/'):]
        elif rel.startswith('features/'):
            parts = rel.split('/')
            if len(parts) > 3 and parts[2] == 'Shaders':
                ip = inst + '/' + '/'.join(parts[3:])
            else:
                continue
        else:
            continue
        pairs.append((p, ip))

def norm(b):
    return b.replace(b'\r\n', b'\n')

same = diff = missing = 0
for a, b in sorted(pairs):
    if not os.path.exists(b):
        missing += 1
        print('MISSING-IN-INSTALL', b)
        continue
    A = norm(open(a, 'rb').read())
    B = norm(open(b, 'rb').read())
    if A == B:
        same += 1
    else:
        diff += 1
        print('DIFF', a[len(src) + 1:])
print('same', same, 'diff', diff, 'missing', missing)
