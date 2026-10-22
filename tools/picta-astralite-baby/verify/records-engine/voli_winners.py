"""PBR-lane winner of each Astralite VOLI source, by header scan of every active plugin in DEEZ CS NUTZ - PBR
that masters an Astralite plugin; then dump the subrecords of every version (raw bytes + floats)."""
import os, struct, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfs import providers, ROOT
PROFILE = sys.argv[1] if len(sys.argv) > 1 else 'DEEZ CS NUTZ - PBR'
ASTRA = {'astralite weathers.esp', 'astralite enb.esp'}
SOURCES = {('astralite weathers.esp', 0x814), ('astralite weathers.esp', 0x861), ('astralite weathers.esp', 0x85D),
           ('astralite enb.esp', 0x82D), ('astralite weathers.esp', 0x86F), ('astralite enb.esp', 0x821),
           ('astralite weathers.esp', 0x85A), ('astralite weathers.esp', 0x810)}

def header(path):
    with open(path, 'rb') as f:
        h = f.read(24)
        sig, dsize, flags = struct.unpack_from('<4sII', h, 0)
        body = f.read(dsize)
    masters = []; p = 0
    while p < len(body):
        st, ss = struct.unpack_from('<4sH', body, p); p += 6
        if st == b'MAST':
            masters.append(body[p:p+ss].rstrip(b'\0').decode('cp1252'))
        p += ss
    return flags, masters, 24 + dsize

def voli_records(path, start):
    out = []
    with open(path, 'rb') as f:
        f.seek(0, 2); size = f.tell(); p = start
        while p < size:
            f.seek(p); g = f.read(24)
            gsize = struct.unpack_from('<I', g, 4)[0]; label = g[8:12]
            if label == b'VOLI':
                f.seek(p + 24); data = f.read(gsize - 24); q = 0
                while q < len(data):
                    rsig, rsize, rflags, rfid = struct.unpack_from('<4sIII', data, q)
                    body = data[q+24:q+24+rsize]; subs = []; r = 0
                    while r < len(body):
                        st, ss = struct.unpack_from('<4sH', body, r); r += 6
                        subs.append((st.decode(), body[r:r+ss])); r += ss
                    out.append((rfid, rflags, subs)); q += 24 + rsize
            p += gsize
    return out

order = [l.strip() for l in open(os.path.join(ROOT, 'profiles', PROFILE, 'loadorder.txt'), encoding='utf-8-sig') if l.strip() and not l.startswith('#')]
active = set()
for l in open(os.path.join(ROOT, 'profiles', PROFILE, 'plugins.txt'), encoding='utf-8-sig'):
    l = l.strip()
    if l.startswith('*'):
        active.add(l[1:].lower())
versions = {}  # (plugin, fid) -> list of (loader, subs)
for idx, name in enumerate(order):
    low = name.lower()
    if low not in active and low not in ASTRA:
        continue
    pv = providers(PROFILE, name)
    if not pv:
        continue
    path = pv[0][1]
    flags, masters, start = header(path)
    mlow = [m.lower() for m in masters]
    if low in ASTRA or any(m in ASTRA for m in mlow):
        for rfid, rflags, subs in voli_records(path, start):
            mi = rfid >> 24; local = rfid & 0xFFFFFF
            if flags & 0x200:
                local = rfid & 0xFFF
            owner = mlow[mi] if mi < len(mlow) else low
            key = (owner, rfid & 0xFFFFFF)
            if key in SOURCES:
                versions.setdefault('%06X:%s' % key[::-1] if False else '%s|%06X' % key, []).append(
                    {'plugin': name, 'mod': pv[0][0], 'active': low in active, 'loadidx': idx, 'flags': hex(rflags),
                     'subs': {s: (b.hex(), struct.unpack('<f', b)[0] if len(b) == 4 else None) for s, b in subs if s != 'EDID'},
                     'edid': [b.rstrip(b'\0').decode() for s, b in subs if s == 'EDID']})
json.dump(versions, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voli_versions_%s.json' % PROFILE.replace(' ', '_')), 'w'), indent=1)
for k, v in versions.items():
    print(k, '->', [(x['plugin'], x['active'], x['loadidx'], x['edid']) for x in v])
