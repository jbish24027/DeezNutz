"""PBR lane: every WTHR version in plugins that master Astralite (or are Astralite): NNAM visual effect + DATA VE begin/end bytes.
Also dumps the Astralite ENB RFCT/ARTO sources for the chain check."""
import os, struct, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vfs import providers, ROOT
from parse_esp import parse
PROFILE = 'DEEZ CS NUTZ - PBR'
ASTRA = {'astralite weathers.esp', 'astralite enb.esp'}
def header(path):
    with open(path, 'rb') as f:
        h = f.read(24); sig, dsize, flags = struct.unpack_from('<4sII', h, 0); body = f.read(dsize)
    masters = []; p = 0
    while p < len(body):
        st, ss = struct.unpack_from('<4sH', body, p); p += 6
        if st == b'MAST': masters.append(body[p:p+ss].rstrip(b'\0').decode('cp1252'))
        p += ss
    return flags, masters
order = [l.strip() for l in open(os.path.join(ROOT, 'profiles', PROFILE, 'loadorder.txt'), encoding='utf-8-sig') if l.strip() and not l.startswith('#')]
active = {l.strip()[1:].lower() for l in open(os.path.join(ROOT, 'profiles', PROFILE, 'plugins.txt'), encoding='utf-8-sig') if l.strip().startswith('*')}
cand = []
for idx, name in enumerate(order):
    low = name.lower()
    if low not in active: continue
    pv = providers(PROFILE, name)
    if not pv: continue
    flags, masters = header(pv[0][1])
    if low in ASTRA or any(m.lower() in ASTRA for m in masters):
        cand.append((idx, name, pv[0][1]))
print('candidates', [c[1] for c in cand])
res = {}
dump = {}
for idx, name, path in cand:
    p = parse(path); M = p['masters']
    def nm(f):
        if f == 0: return None
        return '%06X:%s' % (f & 0xFFFFFF, M[f >> 24] if (f >> 24) < len(M) else name)
    for r in p['records']:
        if r['sig'] == 'WTHR':
            d = dict(r['subs'])
            nn = nm(struct.unpack('<I', d['NNAM'])[0]) if 'NNAM' in d else 'ABSENT'
            data = d.get('DATA', b'')
            key = nm(int(r['formid'], 16))
            res.setdefault(key, []).append({'plugin': name, 'edid': r['edid'], 'NNAM': nn, 'VE': (data[15], data[16]) if len(data) >= 17 else None})
        if r['sig'] in ('RFCT', 'ARTO') and name.lower() == 'astralite enb.esp':
            dump[nm(int(r['formid'], 16))] = {'sig': r['sig'], 'edid': r['edid'], 'subs': [(s, b.hex()) for s, b in r['subs']]}
json.dump({'wthr': res, 'enb_rfct_arto': dump}, open(os.path.join(HERE, 'astra_wthr_ve.json'), 'w'), indent=1)
for k, v in res.items():
    w = v[-1]
    if w['NNAM'] and w['NNAM'] != 'ABSENT':
        print(k, w['edid'], 'winner', w['plugin'], 'NNAM', w['NNAM'], 'VE', w['VE'], '| chain', [(x['plugin'][:22], x['NNAM'], x['VE']) for x in v[:-1]])
