"""For every route marker that floats >60 above our ground (bridges, ledges), find placed objects within 700 units
horizontally that sit under it (z between ground-50 and marker+50) and whose final winning version differs from the
version the route author built against (Skyrim+DLC+Northern Roads.esp). Those markers need review."""
import sys, os, struct, zlib, math, pickle, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plug import masters, subs
from lo import resolve
from land import height
from refpos import iter_world_refs

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = pickle.load(open('land_picta.pkl', 'rb'))
cells = {((('skyrim.esm', 60) if c[0] == 60 else ('dragonborn.esm', 2048)), (c[1], c[2])) for c in json.load(open('elev_cells.json'))}
tg = set()
for w, (gx, gy) in cells:
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1): tg.add((w, (gx + dx, gy + dy)))


def scan(path, store, plugname):
    b = open(path, 'rb').read()
    if b[:4] != b'TES4': return
    m = masters(b); name = os.path.basename(path)
    def gid(k):
        i = k >> 24; return ((m[i] if i < len(m) else name).lower(), k & 0xFFFFFF)
    s = struct.unpack('<I', b[4:8])[0]; off = 24 + s
    worlds = {w for w, g in tg}
    def walk(o, end, world, grid):
        while o < end:
            sig = b[o:o + 4]; size = struct.unpack('<I', b[o + 4:o + 8])[0]
            if sig == b'GRUP':
                gt = struct.unpack('<i', b[o + 12:o + 16])[0]; lab = b[o + 8:o + 12]
                if gt == 1:
                    w = gid(struct.unpack('<I', lab)[0])
                    if w in worlds: walk(o + 24, o + size, w, None)
                elif gt in (4, 5): walk(o + 24, o + size, world, None)
                elif gt in (6, 9, 8):
                    if grid and (world, grid) in tg: walk(o + 24, o + size, world, grid)
                o += size; continue
            size, flags, fid = struct.unpack('<III', b[o + 4:o + 16])
            if sig == b'CELL':
                d = b[o + 24:o + 24 + size]
                if flags & 0x40000: d = zlib.decompress(d[4:])
                grid = None
                for t, v in subs(d):
                    if t == 'XCLC': grid = struct.unpack('<ii', v[:8]); break
            elif sig == b'REFR' and grid and (world, grid) in tg:
                d = b[o + 24:o + 24 + size]
                if flags & 0x40000: d = zlib.decompress(d[4:])
                dd = dict(subs(d))
                if 'DATA' in dd and 'NAME' in dd:
                    store[gid(fid)] = (plugname, world, struct.unpack('<6f', dd['DATA'][:24]), gid(struct.unpack('<I', dd['NAME'][:4])[0]), bool(flags & 0x20), dd.get('XSCL'))
            o += 24 + size
    while off < len(b):
        size = struct.unpack('<I', b[off + 4:off + 8])[0]
        if b[off + 8:off + 12] == b'WRLD': walk(off + 24, off + size, None, None)
        off += size


lo = resolve('DEEZ CS NUTZ - PICTA')
base_set = {'skyrim.esm', 'update.esm', 'dawnguard.esm', 'hearthfires.esm', 'dragonborn.esm', 'northern roads.esp'}
ref_author, ref_final = {}, {}
for p, path in lo:
    if not path: continue
    if p.lower() in base_set: scan(path, ref_author, p)
    scan(path, ref_final, p)
print('refs in elevated cells: author-view', len(ref_author), 'final', len(ref_final))

M = r'C:/1. AUTHORIA/mods/'
markers = []
for f in [M + 'Animated Carriage Additional Route/Animated Carriage Additional Route.esp', M + 'Animated Carriage Additional Route/Animated Carriage Additional Route 0.esp',
          r'arch/ACNR/Animated Carriage Additional Route NR.esp', r'arch/ACNR/Animated Carriage Additional Route 0 NR.esp']:
    for r in iter_world_refs(f):
        x, y, z = r['pos'][:3]; g = height(P, r['world'], x, y)
        if g is not None and z - g > 60: markers.append((os.path.basename(f), r['gid'], r['world'], x, y, z, g))

changed = {}
for k, v in ref_final.items():
    a = ref_author.get(k)
    if v[4]: continue  # deleted ref
    if a is None or a[2][:3] != v[2][:3] or a[3] != v[3] or a[5] != v[5]:
        changed[k] = (v, a)
print('changed/new refs in those cells:', len(changed))
hits = {}
for fname, g, w, x, y, z, gr in markers:
    for k, (v, a) in changed.items():
        if v[1] != w: continue
        vx, vy, vz = v[2][:3]
        if math.dist((vx, vy), (x, y)) < 700 and gr - 50 < vz < z + 50:
            hits.setdefault((fname, g), []).append((k, v[0], v[3], 'NEW' if a is None else 'MOVED' if a[2][:3] != v[2][:3] else 'BASE/SCALE', round(vz - z)))
print('elevated markers', len(markers), 'with changed objects beneath:', len(hits))
plugins = {}
for key, lst in hits.items():
    for k, pl, base, kind, dz in lst: plugins[pl] = plugins.get(pl, 0) + 1
print(sorted(plugins.items(), key=lambda x: -x[1])[:40])
pickle.dump((hits, markers), open('bridge_hits.pkl', 'wb'))
near_a, near_f = {}, {}
for fname, g, w, x, y, z, gr in markers:
    for src, dst in ((ref_author, near_a), (ref_final, near_f)):
        for k, v in src.items():
            if v[1] == w and not v[4] and math.dist(v[2][:2], (x, y)) < 1200: dst[k] = v
pickle.dump((near_a, near_f), open('near_refs.pkl', 'wb'))
print('near refs author', len(near_a), 'final', len(near_f))
