"""List Magpie Manor exterior placed references by base EditorID (STAT/TREE/FLOR/ACTI...).
Walks the plugin's group tree; tracks whether we're inside a WRLD children group (exterior) and the current CELL.
"""
import struct, sys, zlib, os, collections

path = sys.argv[1]
with open(path, 'rb') as f:
    data = f.read()

def subrecords(body):
    pos = 0; out = []
    while pos < len(body):
        st = body[pos:pos+4]; sl = struct.unpack_from('<H', body, pos+4)[0]
        if st == b'XXXX':
            real = struct.unpack_from('<I', body, pos+6)[0]
            pos += 10
            st = body[pos:pos+4]
            out.append((st, body[pos+6:pos+6+real])); pos += 6 + real
            continue
        out.append((st, body[pos+6:pos+6+sl])); pos += 6 + sl
    return out

# header
size = struct.unpack_from('<I', data, 4)[0]
masters = [p.rstrip(b'\0').decode('cp1252','replace') for st,p in subrecords(data[24:24+size]) if st == b'MAST']
pos = 24 + size

edid = {}      # formid -> editorid for records defined in this file
base_of = {}   # refr formid -> (base formid, cellctx, pos)
cell_ctx = {}  # cell formid -> (is_exterior, grid)
placed_by_cell = collections.defaultdict(list)

def walk(start, end, ctx):
    # ctx: dict(exterior=bool, cell=None)
    pos = start
    while pos < end:
        typ = data[pos:pos+4]
        if typ == b'GRUP':
            gsize = struct.unpack_from('<I', data, pos+4)[0]
            label = data[pos+8:pos+12]
            gtype = struct.unpack_from('<I', data, pos+12)[0]
            nctx = dict(ctx)
            if gtype == 1:      # world children
                nctx['exterior'] = True
            elif gtype in (2, 3):   # interior block/subblock
                nctx['exterior'] = False
            elif gtype in (6, 8, 9, 10):  # cell children / persistent / temporary / VWD
                nctx['cell'] = struct.unpack_from('<I', label, 0)[0]
            walk(pos + 24, pos + gsize, nctx)
            pos += gsize
            continue
        rsize, flags, formid = struct.unpack_from('<III', data, pos+4)
        body = data[pos+24:pos+24+rsize]
        if flags & 0x00040000:
            body = zlib.decompress(body[4:])
        if typ == b'CELL':
            subs = subrecords(body)
            grid = None; e = None
            for st, p in subs:
                if st == b'XCLC': grid = struct.unpack_from('<ii', p, 0)
                if st == b'EDID': e = p.rstrip(b'\0').decode('cp1252','replace')
            cell_ctx[formid] = (ctx.get('exterior', False), grid, e)
        elif typ in (b'REFR', b'ACHR'):
            base = None; pos3 = None; disabled = bool(flags & 0x800)
            for st, p in subrecords(body):
                if st == b'NAME': base = struct.unpack_from('<I', p, 0)[0]
                if st == b'DATA': pos3 = struct.unpack_from('<fff', p, 0)
            base_of[formid] = (base, ctx.get('cell'), pos3, disabled, typ.decode())
        else:
            for st, p in subrecords(body):
                if st == b'EDID':
                    edid[formid] = (p.rstrip(b'\0').decode('cp1252','replace'), typ.decode()); break
        pos += 24 + rsize

walk(pos, len(data), dict(exterior=False, cell=None))

nmasters = len(masters)
def fmt(fid):
    idx = fid >> 24
    mod = masters[idx] if idx < nmasters else os.path.basename(path)
    return f"{fid & 0xFFFFFF:06X}:{mod}"

ext_refs = [(r, v) for r, v in base_of.items() if v[1] in cell_ctx and cell_ctx[v[1]][0]]
print(f"placed refs total: {len(base_of)}; exterior: {len(ext_refs)}")
by_cell = collections.Counter(cell_ctx[v[1]][1] for r, v in ext_refs)
print("exterior refs per cell grid:", dict(by_cell))
# per base
cnt = collections.Counter(); disabled_cnt = collections.Counter()
for r, v in ext_refs:
    cnt[v[0]] += 1
    if v[3]: disabled_cnt[v[0]] += 1
rows = []
for b, n in cnt.most_common():
    e, t = edid.get(b, ("<vanilla/other>", "?"))
    rows.append((t, e, fmt(b), n, disabled_cnt[b]))
with open(sys.argv[2], 'w', encoding='utf-8') as out:
    out.write("type\teditorid\tformid\text_refs\tdisabled_refs\n")
    for t, e, f, n, d in rows:
        out.write(f"{t}\t{e}\t{f}\t{n}\t{d}\n")
print(f"distinct bases placed in exterior: {len(rows)}")
print("by type:", collections.Counter(t for t, *_ in rows))
