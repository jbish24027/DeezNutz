"""Baby profile: every active plugin's header; who masters the baby ESL; every override of the 28 WTHR in baby load order;
REGN/CLMT/WTHR counts of the Picta Seasonal and fair climate patches."""
import os, sys, struct, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vfs import providers, ROOT
PROFILE = 'DEEZ CS NUTZ - PICTA x ASTRALITE'
BABY = 'authoria - patch - picta x astralite.esp'
PICTA = 'picta - weathers of aurbis.esm'
KEYS = {0x19FA01, 0x19FA02, 0x19FA03, 0x19FB01, 0x19FB02, 0x19FB03, 0x19FC01, 0x19FC02, 0x19FC03, 0x19FC04, 0x19FC05,
        0x19FD01, 0x19FD02, 0x19FD03, 0x19FD04, 0x19FD05, 0x19FD06, 0x19FE01, 0x19FE02, 0x19FE03, 0x19FE04, 0x19FE05, 0x19FE06,
        0x5AFA01, 0x5AFA02, 0x5AFA03, 0x5AFB01, 0x5AFB02}
def header(path):
    with open(path, 'rb') as f:
        h = f.read(24); sig, dsize, flags = struct.unpack_from('<4sII', h, 0); body = f.read(dsize)
    masters = []; p = 0
    while p < len(body):
        st, ss = struct.unpack_from('<4sH', body, p); p += 6
        if st == b'MAST': masters.append(body[p:p+ss].rstrip(b'\0').decode('cp1252'))
        p += ss
    return flags, masters, 24 + dsize
def group_records(path, start, label):
    out = []
    with open(path, 'rb') as f:
        f.seek(0, 2); size = f.tell(); p = start
        while p < size:
            f.seek(p); g = f.read(24)
            gsize = struct.unpack_from('<I', g, 4)[0]
            if g[8:12] == label:
                f.seek(p + 24); data = f.read(gsize - 24); q = 0
                while q < len(data):
                    rsig, rsize, rflags, rfid = struct.unpack_from('<4sIII', data, q)
                    out.append(rfid); q += 24 + rsize
            p += gsize
    return out
order = [l.strip() for l in open(os.path.join(ROOT, 'profiles', PROFILE, 'loadorder.txt'), encoding='utf-8-sig') if l.strip() and not l.startswith('#')]
active = {l.strip()[1:].lower() for l in open(os.path.join(ROOT, 'profiles', PROFILE, 'plugins.txt'), encoding='utf-8-sig') if l.strip().startswith('*')}
implicit = {'skyrim.esm', 'update.esm', 'dawnguard.esm', 'hearthfires.esm', 'dragonborn.esm'}
chain = collections.defaultdict(list); masters_baby = []; baby_idx = None; missing = []
for idx, name in enumerate(order):
    low = name.lower()
    if low not in active and low not in implicit and not low.startswith('cc'):
        continue
    pv = providers(PROFILE, name)
    if not pv:
        missing.append(name); continue
    flags, masters, start = header(pv[0][1])
    mlow = [m.lower() for m in masters]
    if low == BABY: baby_idx = idx
    if BABY in mlow: masters_baby.append(name)
    if PICTA in mlow or low == PICTA:
        for fid in group_records(pv[0][1], start, b'WTHR'):
            mi = fid >> 24
            owner = mlow[mi] if mi < len(mlow) else low
            if owner == PICTA and (fid & 0xFFFFFF) in KEYS:
                chain['%06X' % (fid & 0xFFFFFF)].append((idx, name))
print('baby ESL load index', baby_idx, 'of', len(order))
print('active plugins with no file in VFS:', missing[:20], len(missing))
print('plugins mastering the baby ESL:', masters_baby)
after = {k: [x for x in v if x[0] > baby_idx] for k, v in chain.items()}
print('overrides AFTER the baby ESL:', {k: v for k, v in after.items() if v})
for k in sorted(chain):
    print(k, [n for i, n in chain[k]])
