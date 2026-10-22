"""Decide heights for raised route points (bridges, ledges) from real bridge geometry.
author world = vanilla + Northern Roads (what the route author built on); final world = our whole load order."""
import sys, os, pickle, struct, json, csv, warnings, math
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import hits_at, load_tris
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
na, nf = pickle.load(open('near_refs.pkl', 'rb')); info_all, br = pickle.load(open('bases.pkl', 'rb'))
info = {b: 'meshes/' + i[2].replace(chr(92), '/').lower() for b, i in br.items() if i[2]}
sc = lambda v: struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
el = pickle.load(open('elevated.pkl', 'rb'))
res = []; cnt = {}
for e in el:
    w = e['world']; x, y, z = e['nx'], e['ny'], e['zsrc']
    author = na if e['src'] in ('nr', 'acar') else nf
    za = hits_at({k: v for k, v in author.items() if v[1] == w}, info, x, y, 'A', sc)
    zf = hits_at({k: v for k, v in nf.items() if v[1] == w}, info, x, y, 'A', sc)
    near_a = [h for h in za if abs(h - z) <= 40]
    if near_a:
        da = min(near_a, key=lambda h: abs(h - z)); off = z - da
        cand = [h for h in zf if abs(h - da) <= 150]
        if cand:
            df = min(cand, key=lambda h: abs(h - da)); nz = df + off
            kind = 'deck-same' if abs(df - da) < 2 else 'deck-moved'
        else:
            nz = z; kind = 'REVIEW-deck-gone'
    else:
        on_new = [h for h in zf if abs(h - z) <= 40]
        nz = z; kind = 'rests-on-new-deck' if on_new else 'no-deck-keep'
    # anything of ours ABOVE the point that the carriage (about 300 tall) would drive into
    over = [h for h in zf if z + 30 < h < z + 300]
    if over and kind != 'REVIEW-deck-gone': kind += '+OVERHEAD'
    cnt[kind] = cnt.get(kind, 0) + 1
    res.append(dict(e, nz=nz, kind=kind, za=sorted(round(h) for h in za)[:6], zf=sorted(round(h) for h in zf)[:6]))
print(cnt)
for r in res:
    if 'REVIEW' in r['kind'] or 'OVERHEAD' in r['kind'] or r['kind'] == 'deck-moved':
        print('%-8s %-6s %-28s z %7.0f -> %7.0f  author hits %s  final hits %s' % ('%06X' % r['g'][1], r['src'], r['kind'], r['zsrc'], r['nz'], r['za'], r['zf']))
pickle.dump(res, open('elevated_res.pkl', 'wb'))
