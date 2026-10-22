import struct, sys, os, json
sys.path.insert(0, r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\b9a87f9f-844d-48e6-97f9-91a42cb52bda\scratchpad\tools')
from espscan import subrecs, walk, zstr
p = sys.argv[1]
buf = open(p, 'rb').read()
size, flags = struct.unpack_from('<II', buf, 4)
hdr = buf[24:24 + size]
masters = [zstr(d) for t, d in subrecs(hdr) if t == b'MAST']
recs = []; walk(buf, 24 + size, len(buf), recs)
def fk(x):
    i = x >> 24
    return '%06X:%s' % (x & 0xFFFFFF, masters[i] if i < len(masters) else 'SELF')
out = {}
for t, fid, fl, d in recs:
    if t not in ('ARMA', 'ARMO') or (fid >> 24) < len(masters): continue
    r = {'type': t, 'flags': fl, 'races': [], 'alt': {}}
    for st, sd in subrecs(d):
        s = st.decode()
        if s == 'EDID': r['edid'] = zstr(sd)
        elif s in ('MOD2', 'MOD3', 'MOD4', 'MOD5'): r[s] = zstr(sd)
        elif s == 'MODL' and t == 'ARMA': r['races'].append(fk(struct.unpack_from('<I', sd)[0]))
        elif s == 'RNAM': r['race'] = fk(struct.unpack_from('<I', sd)[0])
        elif s == 'BOD2': r['bod2'] = struct.unpack_from('<II', sd)
        elif s == 'DNAM' and t == 'ARMA': r['dnam'] = list(sd)
        elif s == 'SNDD': r['sndd'] = fk(struct.unpack_from('<I', sd)[0])
        elif s in ('MO2S', 'MO3S', 'MO4S', 'MO5S'):
            n = struct.unpack_from('<I', sd, 0)[0]; o = 4; L = []
            for _ in range(n):
                ln = struct.unpack_from('<I', sd, o)[0]; o += 4
                nm = sd[o:o + ln].decode('latin1'); o += ln
                ts, ix = struct.unpack_from('<Ii', sd, o); o += 8
                L.append((nm, fk(ts), ix))
            r['alt'][s] = L
        elif s == 'OBND': r['obnd'] = struct.unpack_from('<6h', sd)
    out[fk(fid)] = r
json.dump(out, open(sys.argv[2], 'w'), indent=1)
for k, v in out.items():
    print(k, v.get('edid'), v.get('bod2'), v.get('dnam'), len(v['races']), v.get('MOD2'), v.get('MOD4'), v['alt'], v.get('sndd'), v.get('obnd'))
