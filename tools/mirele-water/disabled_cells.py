"""Attribute disabled/moved refs to source plugins, then check whether any of them
live in the cells around Lake Ilinalta / the Guardian Stones."""
import sys, os, struct, math, zlib
from collections import Counter, defaultdict
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import R, load, parse_body, global_data
from changeforms import (TYPE_NAMES, parse_change_forms, read_formid_array,
                         resolve, decompress, decode_initial)

PATH = r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ\saves\Save16_A67A30D7_0_456E6F7261_Tamriel_000240_20260822162235_1_1.ess'
hdr, body = load(PATH)
fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
formids = read_formid_array(body, flt['formIDArrayCountOffset'])
forms, _ = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], True)

def plugin_of(fid):
    hi = fid >> 24
    if hi == 0xFF:
        return '<created>'
    if hi == 0xFE:
        idx = (fid >> 12) & 0xFFF
        return light[idx] if idx < len(light) else '<light %d?>' % idx
    return plugins[hi] if hi < len(plugins) else '<full %d?>' % hi

DIS = 0x800
DEL = 0x20
dis = []; dele = []; moved = []
for cf in forms:
    if cf['type'] not in (0, 1, 2, 3, 4, 5):
        continue
    d = decompress(cf)
    if d is None:
        continue
    try:
        init, _ = decode_initial(d, cf['flags'])
    except Exception:
        continue
    fid = resolve(cf['rtype'], cf['rval'], formids)
    if fid is None:
        continue
    rf = init.get('recordFlags')
    if rf is not None and rf & DIS:
        dis.append((fid, cf, init))
    if rf is not None and rf & DEL:
        dele.append((fid, cf, init))
    if 'posX' in init:
        moved.append((fid, cf, init))

print('disabled refs %d   deleted-flag refs %d   moved refs %d' % (len(dis), len(dele), len(moved)))
c = Counter(plugin_of(f) for f, _, _ in dis)
print()
print('disabled refs by source plugin (top 25):')
for k, v in c.most_common(25):
    print('   %-60s %5d' % (k, v))

# ---- which cells? scan the source plugins for cell-children GRUP labels
def cellfid(x, y):
    return 0x009B4F + (-13 - y) * 0x21 + (-x)
LAKE = {}
for x in range(-10, 3):
    for y in range(-20, -11):
        LAKE[cellfid(x, y)] = (x, y)

def refs_in_cells(path, wanted_local):
    """Return {localFormID(24bit) of REFR/ACHR: parent cell local id} for wanted cells."""
    out = {}
    try:
        data = open(path, 'rb').read()
    except OSError:
        return out
    if data[:4] != b'TES4':
        return out
    size = struct.unpack_from('<I', data, 4)[0]
    pos = 24 + size
    stack = [(pos, len(data), None)]
    while stack:
        pos, end, parent = stack.pop()
        while pos < end:
            typ = data[pos:pos+4]
            if typ == b'GRUP':
                gsize, label, gtype = struct.unpack_from('<IiI', data, pos+4)
                gtype &= 0xFFFFFFFF
                gt = struct.unpack_from('<i', data, pos+12)[0]
                newparent = parent
                if gt in (6, 8, 9):
                    newparent = label & 0xFFFFFF
                    if gt == 6 and newparent not in wanted_local:
                        pos += gsize
                        continue
                stack.append((pos+gsize, end, parent))
                end = pos + gsize
                parent = newparent
                pos += 24
                continue
            rsize = struct.unpack_from('<I', data, pos+4)[0]
            fid = struct.unpack_from('<I', data, pos+12)[0]
            if typ in (b'REFR', b'ACHR', b'PHZD', b'PGRE', b'PMIS', b'PARW', b'PBAR', b'PBEA', b'PCON', b'PFLA'):
                if parent in wanted_local:
                    out[fid & 0xFFFFFF] = parent
            pos += 24 + rsize
    return out

# figure out the on-disk path of each plugin via the MO2 mods tree + Stock Game
import glob
SEARCH = [r'C:\1. AUTHORIA\Stock Game\Data']
modroots = glob.glob(r'C:\1. AUTHORIA\mods\*')
pathcache = {}
def find_plugin(name):
    if name in pathcache: return pathcache[name]
    p = os.path.join(r'C:\1. AUTHORIA\Stock Game\Data', name)
    if os.path.exists(p):
        pathcache[name] = p; return p
    for m in modroots:
        q = os.path.join(m, name)
        if os.path.exists(q):
            pathcache[name] = q; return q
    pathcache[name] = None; return None

srcs = sorted({plugin_of(f) for f, _, _ in dis} | {plugin_of(f) for f, _, _ in dele})
srcs = [s for s in srcs if not s.startswith('<')]
print()
print('scanning %d source plugins for refs in the %d lake cells...' % (len(srcs), len(LAKE)))
hitmap = {}
for s in srcs:
    p = find_plugin(s)
    if not p:
        continue
    r = refs_in_cells(p, set(LAKE))
    if r:
        hitmap[s] = r
print('plugins that place refs in those cells: %d' % len(hitmap))
for s, r in hitmap.items():
    print('   %-60s %d refs' % (s, len(r)))

print()
print('=== disabled/deleted refs that live in a lake-area cell ===')
found = 0
for label, lst in (('DISABLED', dis), ('DELETED', dele)):
    for fid, cf, init in lst:
        s = plugin_of(fid)
        r = hitmap.get(s)
        if not r:
            continue
        loc = fid & 0xFFFFFF
        if loc in r:
            cx, cy = LAKE[r[loc]]
            print('  %-8s %08X  %-40s cell(%d,%d)  recFlags=0x%08X changeFlags=0x%08X'
                  % (label, fid, s[:40], cx, cy, init['recordFlags'], cf['flags']))
            found += 1
print('total: %d' % found)
