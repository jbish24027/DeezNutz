"""Mists of Tamriel: STAT 080B-0816 (type, model), every placed REFR of them, their enable parents and the parents' flags."""
import os, sys, struct, collections, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse_esp import parse
from vfs import winner
PROFILE = 'DEEZ CS NUTZ - PICTA x ASTRALITE'
path = winner(PROFILE, 'Mists of Tamriel.esp')[1]
p = parse(path)
M = p['masters']; me = 'Mists of Tamriel.esp'
print('MoT header', p['header'], 'masters', M, 'records', len(p['records']))
print('MoT record types', dict(collections.Counter(r['sig'] for r in p['records'])))
def nm(f):
    if f == 0: return None
    i = f >> 24
    return (M[i] if i < len(M) else me, f & 0xFFFFFF)
targets = {(me, x) for x in range(0x80B, 0x817)}
byid = {}
for r in p['records']:
    byid[nm(int(r['formid'], 16))] = r
for t in sorted(targets, key=lambda x: x[1]):
    r = byid.get(t)
    if r is None:
        print('MISSING', t); continue
    d = dict(r['subs'])
    print('%06X' % t[1], r['sig'], r['edid'], 'flags', r['flags'], 'MODL', d.get('MODL', b'').rstrip(b'\0').decode('cp1252', 'replace'))
refs = collections.defaultdict(list); parents = collections.Counter(); parent_of = {}
for r in p['records']:
    if r['sig'] != 'REFR': continue
    d = dict(r['subs'])
    base = nm(struct.unpack('<I', d['NAME'])[0]) if 'NAME' in d else None
    if base in targets:
        xesp = d.get('XESP')
        par = None
        if xesp:
            pf, pflag = struct.unpack('<II', xesp[:8])
            par = (nm(pf), pflag)
        refs[base].append((r['formid'], r['flags'], par))
        parents[par] += 1
print('placed refs per static', {('%06X' % k[1]): len(v) for k, v in sorted(refs.items(), key=lambda kv: kv[0][1])})
print('ref record flags', collections.Counter(x[1] for v in refs.values() for x in v))
print('enable parents (parent, opposite-flag) -> count')
for (par), c in parents.most_common():
    if par is None:
        print('  none', c); continue
    pr = byid.get(par[0])
    info = (pr['sig'], pr['edid'], pr['flags'], dict(pr['subs']).get('NAME', b'').hex()) if pr else 'parent not in MoT'
    print('  ', '%06X:%s' % (par[0][1], par[0][0]), 'opposite' if par[1] & 1 else 'same', c, info)
# weathers in MoT listing them
for r in p['records']:
    if r['sig'] == 'WTHR':
        tn = [nm(struct.unpack('<I', b)[0]) for s, b in r['subs'] if s == 'TNAM']
        hit = [t for t in tn if t in targets]
        if hit:
            print('MoT WTHR', r['formid'], r['edid'], 'lists', len(hit), 'of the 12')
