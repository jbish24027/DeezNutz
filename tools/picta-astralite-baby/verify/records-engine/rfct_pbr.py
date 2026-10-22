import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfs import providers, ROOT
from parse_esp import parse
P = 'DEEZ CS NUTZ - PBR'
order = [l.strip() for l in open(os.path.join(ROOT, 'profiles', P, 'loadorder.txt'), encoding='utf-8-sig') if l.strip() and not l.startswith('#')]
active = {l.strip()[1:].lower() for l in open(os.path.join(ROOT, 'profiles', P, 'plugins.txt'), encoding='utf-8-sig') if l.strip().startswith('*')}
def masters(path):
    with open(path, 'rb') as f:
        h = f.read(24); dsize = struct.unpack_from('<I', h, 4)[0]; body = f.read(dsize)
    out = []; p = 0
    while p < len(body):
        st, ss = struct.unpack_from('<4sH', body, p); p += 6
        if st == b'MAST': out.append(body[p:p+ss].rstrip(b'\0').decode('cp1252').lower())
        p += ss
    return out
T = {0x812, 0x834, 0x81C, 0x802, 0x803, 0x80C}
for name in order:
    low = name.lower()
    if low not in active: continue
    pv = providers(P, name)
    if not pv: continue
    m = masters(pv[0][1])
    if 'astralite enb.esp' not in m: continue
    p = parse(pv[0][1])
    for r in p['records']:
        if r['sig'] in ('RFCT', 'ARTO'):
            f = int(r['formid'], 16); mi = f >> 24
            if mi < len(m) and m[mi] == 'astralite enb.esp' and (f & 0xFFFFFF) in T:
                print('OVERRIDE', name, r['sig'], hex(f), r['edid'])
print('done')
