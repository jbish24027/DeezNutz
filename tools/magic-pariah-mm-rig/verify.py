"""Verify the grafted skirt mesh and render weight-band pictures."""
import sys, struct, colorsys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\ube-neck-pin\from-bodypin3")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifparse import Nif, load_mesh
from nifrw import Doc, reachable, parse_node, parse_shape_hdr, parse_dismember, slots
from graft import MP_NIF, MM_NIF, OUT_NIF, OUT_DIR, PROXY_NAME, sk_row, COLUMNS, sk_name

ok = True
def check(cond, msg):
    global ok
    print(('PASS ' if cond else 'FAIL ') + msg)
    ok &= bool(cond)

raw = open(OUT_NIF, 'rb').read()
doc = Doc(OUT_NIF)
check(doc.tobytes() == raw, 'output re-serializes byte-exact')
check(len(reachable(doc)) == len(doc.blocks), 'every block reachable from the root (%d blocks)' % len(doc.blocks))
types = {}
for t, _ in doc.blocks: types[t] = types.get(t, 0) + 1
print('block census:', types)
for i, (t, b) in enumerate(doc.blocks):
    refs, strs = slots(t, b)
    for off in refs:
        v = struct.unpack_from('<i', b, off)[0]
        assert v < len(doc.blocks), ('dangling ref', i, v)
    for off in strs:
        v = struct.unpack_from('<I', b, off)[0]
        assert v == 0xFFFFFFFF or v < len(doc.strings), ('dangling string', i, v)
check(True, 'no dangling block/string references')

# node tree
names = {}
def walk(i, depth, parent):
    n = parse_node(doc.blocks[i][1]); nm = doc.strings[n['name']]
    names[nm] = parent
    for c in n['children']:
        if c >= 0 and doc.blocks[c][0] == 'NiNode': walk(c, depth + 1, nm)
walk(doc.roots[0], 0, None)
sk = sorted(n for n in names if n.startswith('sk_'))
check(len(sk) == 48 and all(sk_row(n) in (1, 2, 3, 4) for n in sk), '48 chain nodes, rows 1-4 only')
check(all(names[sk_name(c, 1)] == 'NPC Pelvis [Pelv]' for c in COLUMNS), 'row-1 anchors parented to NPC Pelvis')
check(all(names[sk_name(c, r)] == sk_name(c, r - 1) for c in COLUMNS for r in (2, 3, 4)), 'rows 2-4 chained under their row above')
check(not any(n.startswith('sk_') and len(n) <= 5 for n in names), 'old MP chain (sk_a..h) gone')

nif, shapes = load_mesh(OUT_NIF)
by = {s['name']: s for s in shapes}
print('shapes:', [s['name'] for s in shapes])
check('Cube' not in by and 'UniButt' not in by, 'Cube and UniButt removed')
check(all(n in by for n in ('Skirt Lower', 'Skirt Upper', 'SASH_2', 'chain belt_2', PROXY_NAME, 'CollThigh', 'CollCalves')), 'expected shapes present')

_, shP = load_mesh(MP_NIF); byP = {s['name']: s for s in shP}
_, shM = load_mesh(MM_NIF); byM = {s['name']: s for s in shM}

def packed_weights(nif, sh):
    si = nif.parse_skin_instance(sh['skin_ref'])
    sp = nif.parse_skin_partition(si['partition_ref'])
    p = sp['partitions'][0]
    out = []
    for v in range(sp['num_vertices']):
        d = {}
        for bidx, w in sp['weights_vb'][v]:
            if w > 0:
                d[si['bone_names'][p['bones'][bidx]]] = d.get(si['bone_names'][p['bones'][bidx]], 0) + w
        out.append(d)
    return out, sp, si

for n in ('Skirt Lower', 'Skirt Upper', 'SASH_2', 'chain belt_2'):
    a = np.array(by[n]['positions']); b = np.array(byP[n]['positions'])
    check(a.shape == b.shape and np.allclose(a, b), '%s positions unchanged (%d verts)' % (n, len(a)))
for n in ('CollThigh', 'CollCalves'):
    a = np.array(by[n]['positions']); b = np.array(byM[n]['positions'])
    check(a.shape == b.shape and np.allclose(a, b), '%s positions equal MM (%d verts)' % (n, len(a)))
a = np.array(by[PROXY_NAME]['positions']); b = np.array(byM['Draft Skirt weight test']['positions'])
check(a.shape == b.shape and np.allclose(a, b), 'proxy positions equal MM proxy')

for n in ('Skirt Lower', 'Skirt Upper', PROXY_NAME):
    sh = by[n]
    wm = sh['weight_map']
    sums = np.array([sum(w.values()) for w in wm])
    check(np.all(np.abs(sums - 1) < 1e-4), '%s NiSkinData weights sum to 1 (min %.5f max %.5f)' % (n, sums.min(), sums.max()))
    pk, sp, si = packed_weights(nif, sh)
    worst = 0.0
    for v in range(len(wm)):
        for bname in set(wm[v]) | set(pk[v]):
            worst = max(worst, abs(wm[v].get(bname, 0) - pk[v].get(bname, 0)))
    check(worst < 2e-3, '%s packed partition weights match NiSkinData (worst diff %.4f, %d bones)' % (n, worst, len(si['bone_names'])))
    rows = {}
    for w in wm:
        for bname in w:
            r = sk_row(bname)
            key = 'row%d' % r if r else ('thigh' if 'Thigh' in bname else 'body')
            rows[key] = rows.get(key, 0) + 1
    print('   %s bone classes used (vertex counts):' % n, dict(sorted(rows.items())))
    check(all(bname in names for w in wm for bname in w), '%s every weighted bone has a node' % n)
    tris = sp['partitions'][0]['num_triangles']
    print('   %s triangles %d' % (n, tris))

# HDT string
for i, (t, b) in enumerate(doc.blocks):
    if t == 'NiStringExtraData':
        a, s = struct.unpack_from('<II', b, 0)
        print('StringExtraData:', doc.strings[a], '=>', doc.strings[s])
# dismember parts of every shape
for s in shapes:
    h = parse_shape_hdr(doc.blocks[s['block']][1])
    d = parse_dismember(doc.blocks[h['skin']][1])
    print('   %-16s partitions %s  shader %d  flags 0x%X' % (s['name'], d['parts'], h['shader'], h['flags']))

# ---- pictures: side view coloured by dominant row, top view coloured by column
def colour_for(bname):
    r = sk_row(bname)
    if r is None:
        return (230, 230, 230) if 'Thigh' not in bname else (140, 140, 140)
    return {1: (255, 60, 60), 2: (255, 170, 0), 3: (60, 200, 60), 4: (60, 120, 255)}[r]
def col_colour(bname):
    r = sk_row(bname)
    if r is None: return (120, 120, 120)
    base = bname[3:].replace(str(r), '')
    k = COLUMNS.index(base) if base in COLUMNS else 0
    rgb = colorsys.hsv_to_rgb(k / 12.0, 0.9, 1.0)
    return tuple(int(255 * c) for c in rgb)
W, H = 1200, 900
img = Image.new('RGB', (W, H), (20, 20, 20)); dr = ImageDraw.Draw(img)
def dom(w):
    return max(w.items(), key=lambda kv: kv[1])[0]
panels = [('Skirt Lower front (x,z) by row', 'Skirt Lower', 'front', colour_for),
          ('Skirt Upper front (x,z) by row', 'Skirt Upper', 'front', colour_for),
          ('Skirt Lower top (x,y) by column', 'Skirt Lower', 'top', col_colour),
          ('Proxy side (y,z) by row', PROXY_NAME, 'side', colour_for)]
for k, (title, n, view, cf) in enumerate(panels):
    ox = (k % 2) * 600; oy = (k // 2) * 450
    dr.text((ox + 10, oy + 8), title, fill=(255, 255, 255))
    P = np.array(by[n]['positions']); wm = by[n]['weight_map']
    for v, p in enumerate(P):
        if view == 'front': u, w = p[0], p[2]
        elif view == 'side': u, w = p[1], p[2]
        else: u, w = p[0], p[1]
        if view == 'top':
            x = ox + 300 + u * 9; y = oy + 240 - w * 9
        else:
            x = ox + 300 + u * 9; y = oy + 440 - (w - 30) * 8
        c = cf(dom(wm[v])) if wm[v] else (255, 0, 255)
        dr.point((x, y), fill=c)
dr.text((10, H - 20), 'red=row1 orange=row2 green=row3 blue=row4 white=body grey=thigh', fill=(255, 255, 255))
img.save(OUT_DIR + r"\weights.png")
print('picture:', OUT_DIR + r"\weights.png")
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
