"""Oriented-box overlap test: every carriage-stop bench and brazier (at its terrain-corrected height) against every
other placed object in our final world, using each base object's OBND bounds. For clashing benches, search the smallest
slide along the bench's long axis (keeps the approach path along the road) that clears everything."""
import sys, os, math, pickle, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plug import Plugin, subs
from lo import resolve
from refpos import iter_world_refs
from scanmod import scan
from land import height

M = r'C:/1. AUTHORIA/mods/'
OWN = ('simplecarriageexpansion.esp', 'animated carriages take you everywhere.esp')
refs = {}
for f in [M + 'Carriage Stops of Skyrim/simpleCarriageExpansion.esp', M + 'Animated Carriages Take You Everywhere/Animated Carriages Take You Everywhere.esp']:
    for r in iter_world_refs(f):
        if r['gid'][0] in OWN: refs[r['gid']] = r
van, fin = pickle.load(open('land_stops.pkl', 'rb'))
tg = {(r['world'], (math.floor(r['pos'][0] / 4096) + dx, math.floor(r['pos'][1] / 4096) + dy)) for r in refs.values() for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
lo = resolve('DEEZ CS NUTZ - PICTA'); paths = {p.lower(): path for p, path in lo if path}
final = {}; author = {}
AUTH = {'skyrim.esm', 'update.esm', 'dawnguard.esm', 'hearthfires.esm', 'dragonborn.esm', 'unofficial skyrim special edition patch.esp'}
for p, path in lo:
    if not path: continue
    if p.lower() in AUTH: scan(path, author, p, tg)
    scan(path, final, p, tg)
# OBND for every base used near the stops (winning base record approximated by the defining plugin)
need = {v[3] for v in final.values()} | {r['base'] for r in refs.values()}
ob = {}; nm = {}
for f in sorted({b[0] for b in need}):
    if f not in paths: continue
    P = Plugin(paths[f])
    for b in need:
        if b[0] == f and b in P.recs:
            v = P.recs[b]; d = dict(subs(v[3])); nm[b] = (v[0], v[1])
            if 'OBND' in d and v[0] in ('STAT', 'TREE', 'FURN', 'ACTI', 'CONT', 'MSTT', 'FLOR', 'DOOR', 'MISC'):
                ob[b] = struct.unpack('<6h', d['OBND'])


def poly(b, pos, rz, s=1.0):
    x0, y0, z0, x1, y1, z1 = b; c, sn = math.cos(rz), math.sin(rz)
    # Skyrim heading is clockwise: world = (x*cos + y*sin, -x*sin + y*cos)
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return [(pos[0] + s * (x * c + y * sn), pos[1] + s * (-x * sn + y * c)) for x, y in pts], (pos[2] + s * z0, pos[2] + s * z1)


def sat(a, b):
    for P in (a, b):
        for i in range(4):
            p, q = P[i], P[(i + 1) % 4]; ax = (q[1] - p[1], p[0] - q[0])
            pa = [ax[0] * x + ax[1] * y for x, y in a]; pb = [ax[0] * x + ax[1] * y for x, y in b]
            if max(pa) <= min(pb) or max(pb) <= min(pa): return False
    return True


def clashes(base, pos, rz, skip):
    A, za = poly(ob[base], pos, rz)
    out = []
    for k, v in final.items():
        if k in skip or k[0] in OWN or v[4] or v[6] or v[1] != W or v[3] not in ob or v[2][2] < -29000: continue
        if math.dist(v[2][:2], pos[:2]) > 400: continue
        t, en = nm.get(v[3], ('', ''))
        if t in ('TREE', 'FLOR') or any(w in en.lower() for w in ('flora', 'fern', 'grass', 'fx', 'marker', 'smoke', 'mist', 'snowdrift', 'decal', 'moss')): continue
        a = author.get(k)
        if a is not None and a[2][:3] == v[2][:3] and a[3] == v[3]: continue
        s = struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
        B, zb = poly(ob[v[3]], v[2], v[2][5], s)
        if zb[1] <= za[0] + 5 or zb[0] >= za[1] - 5: continue
        if sat(A, B): out.append((nm[v[3]][1], v[0][:34], round(math.dist(v[2][:2], pos[:2]))))
    return out


rows = []
for g, r in refs.items():
    W = r['world']
    n = nm.get(r['base'], ('', ''))[1]
    if n not in ('sm_sce_activator', 'sm_sce_WRBrazier01'): continue
    x, y, z = r['pos'][:3]; gv = height(van, W, x, y); gf = height(fin, W, x, y)
    dz = (gf - gv) if (gv is not None and gf is not None) else 0
    pos = (x, y, z + dz)
    c = clashes(r['base'], pos, r['pos'][5], set())
    fix = None
    if c and n == 'sm_sce_activator':
        ax = (math.cos(r['pos'][5]), -math.sin(r['pos'][5]))     # bench long axis (local x) in world
        for d in sorted([s * k for k in range(25, 401, 25) for s in (1, -1)], key=abs):
            nx, ny = x + ax[0] * d, y + ax[1] * d; ngf = height(fin, W, nx, ny); ngv = height(van, W, nx, ny)
            npos = (nx, ny, z + (ngf - height(van, W, x, y)))
            if not clashes(r['base'], npos, r['pos'][5], set()):
                fix = (d, npos); break
    rows.append((n, hex(g[1]), round(dz, 1), c, fix, r))
    if c or abs(dz) > 8:
        print(n, hex(g[1]), 'ground shift', round(dz), '| clashes:', c[:5], '| slide fix:', (fix[0], [round(v) for v in fix[1]]) if fix else None)
pickle.dump(rows, open('bench_rows.pkl', 'wb'))
print(len(rows), 'checked')

# ---- whole-stop translation search (bench + brazier together) for a named stop
if len(sys.argv) > 1:
    bh, zh = int(sys.argv[1], 16), int(sys.argv[2], 16)
    b = refs[('simplecarriageexpansion.esp', bh)]; z_ = refs[('simplecarriageexpansion.esp', zh)]
    W = b['world']
    best = None
    for r_ in range(0, 501, 25):
        for a_ in range(0, 360, 15):
            dx, dy = r_ * math.cos(math.radians(a_)), r_ * math.sin(math.radians(a_))
            ok = True; newp = []
            for o in (b, z_):
                x, y, z = o['pos'][:3]; nx, ny = x + dx, y + dy
                nz = z + (height(fin, W, nx, ny) - height(van, W, x, y))
                if clashes(o['base'], (nx, ny, nz), o['pos'][5], set()): ok = False; break
                newp.append((nx, ny, nz))
            if ok: best = (r_, a_, dx, dy, newp); break
            if r_ == 0: break
        if best: break
    print('group move:', best and (best[0], best[1], [[round(v) for v in p] for p in best[4]]))
