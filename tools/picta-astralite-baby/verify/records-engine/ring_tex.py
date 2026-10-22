import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfs import providers
P = 'DEEZ CS NUTZ - PICTA x ASTRALITE'
for n in ['lite', 'heavy', 'rain']:
    b = open(r'C:\1. AUTHORIA\mods\Authoria - Picta x Astralite - Mist assets\meshes\effects\distant_mounts_%s.nif' % n, 'rb').read()
    t = sorted(set(x.decode('cp1252') for x in re.findall(rb'[A-Za-z0-9_\\/ .-]+\.dds', b, re.I)))
    print(n, t)
    for x in t:
        rel = x if x.lower().startswith('textures') else 'textures\\' + x
        print('   ', rel, [m for m, _ in providers(P, rel.replace('\\', '/'))])
