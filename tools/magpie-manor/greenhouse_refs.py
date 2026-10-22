"""List Magpie exterior refs (with positions) and find which ones sit inside the greenhouse footprints."""
import sys, os, struct, zlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landscan import read_masters, subrecords
path = r"C:\1. AUTHORIA\mods\Magpie Manor\MagpieManor.esp"
data = open(path,'rb').read()
masters, start = read_masters(data)
edid = {}; refs = []
def walk(pos, end, exterior, cell):
    while pos < end:
        typ = data[pos:pos+4]
        if typ == b'GRUP':
            gsize = struct.unpack_from('<I', data, pos+4)[0]
            label = data[pos+8:pos+12]; gtype = struct.unpack_from('<I', data, pos+12)[0]
            ex, ce = exterior, cell
            if gtype == 1: ex = True
            elif gtype in (2,3): ex = False
            elif gtype in (6,8,9,10): ce = struct.unpack_from('<I', label, 0)[0]
            walk(pos+24, pos+gsize, ex, ce); pos += gsize; continue
        rsize, flags, fid = struct.unpack_from('<III', data, pos+4)
        body = data[pos+24:pos+24+rsize]
        if flags & 0x40000: body = zlib.decompress(body[4:])
        if typ == b'REFR' and exterior:
            base = None; p3 = None; scale = 1.0
            for st, p in subrecords(body):
                if st == b'NAME': base = struct.unpack_from('<I', p, 0)[0]
                elif st == b'DATA': p3 = struct.unpack_from('<fff', p, 0)
                elif st == b'XSCL': scale = struct.unpack_from('<f', p, 0)[0]
            refs.append((fid, base, p3, bool(flags & 0x800), scale))
        elif typ != b'REFR':
            for st, p in subrecords(body):
                if st == b'EDID': edid[fid] = p.rstrip(b'\0').decode('cp1252','replace'); break
        pos += 24 + rsize
walk(start, len(data), False, None)
def name(b): return edid.get(b, "%08X" % b if b is not None else "?")
gh = [r for r in refs if name(r[1]).startswith("_mag_Greenhouse")]
print("greenhouse piece refs:", len(gh))
for r in sorted(gh, key=lambda r: (r[2][0], r[2][1])):
    print(f"  {name(r[1]):28s} x={r[2][0]:9.1f} y={r[2][1]:9.1f} z={r[2][2]:8.1f}")
# cluster greenhouse pieces by proximity (simple: union-find with 700-unit radius)
pts = [(r[2][0], r[2][1]) for r in gh]
parent = list(range(len(pts)))
def find(i):
    while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
    return i
for i in range(len(pts)):
    for j in range(i+1, len(pts)):
        if (pts[i][0]-pts[j][0])**2 + (pts[i][1]-pts[j][1])**2 <= 700**2:
            parent[find(i)] = find(j)
clusters = collections.defaultdict(list)
for i in range(len(pts)): clusters[find(i)].append(gh[i])
print("\nclusters:", len(clusters))
boxes = []
for k, members in clusters.items():
    xs = [m[2][0] for m in members]; ys = [m[2][1] for m in members]; zs = [m[2][2] for m in members]
    box = (min(xs)-64, max(xs)+64, min(ys)-64, max(ys)+64, min(zs)-32, max(zs)+400)
    boxes.append(box)
    print(f"  cluster of {len(members)} pieces: x {box[0]:.0f}..{box[1]:.0f}  y {box[2]:.0f}..{box[3]:.0f}  z {box[4]:.0f}..{box[5]:.0f}")
inside = []
for r in refs:
    if r[1] is None or r[2] is None: continue
    n = name(r[1])
    if n.startswith("_mag_Greenhouse"): continue
    x, y, z = r[2]
    for b in boxes:
        if b[0] <= x <= b[1] and b[2] <= y <= b[3] and b[4] <= z <= b[5]:
            inside.append((r, n)); break
print("\nrefs inside greenhouse footprints:", len(inside))
cnt = collections.Counter(n for r, n in inside)
for n, c in cnt.most_common(): print(f"  {c:3d}  {n}")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "greenhouse_inside_refs.tsv"), "w") as f:
    f.write("refid\tbase\tx\ty\tz\tdisabled\n")
    for r, n in inside:
        f.write(f"{r[0] & 0xFFFFFF:06X}\t{n}\t{r[2][0]:.1f}\t{r[2][1]:.1f}\t{r[2][2]:.1f}\t{r[3]}\n")
