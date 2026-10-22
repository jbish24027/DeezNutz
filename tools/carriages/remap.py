"""Remap FormIDs that point into a master whose author renumbered records (Animated Carriage 1.1.0 -> 1.2.1 ESL compaction).
Mapping is built by EditorID between the old and new master. For the target plugin: record header FormIDs and every
subrecord value equal to an old FormID (scanned at every subrecord's 4-byte-aligned offsets) are rewritten.
usage: remap.py old_master new_master target.esp [--write]"""
import sys, os, struct, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recs import load
from plug import masters

WRITE = '--write' in sys.argv
old, new, tgt = sys.argv[1:4]
O = load(old); N = load(new)
byedid = {v[1]: k for k, v in N.items() if v[1]}
mapping = {}
for k, v in O.items():
    if k not in N or N[k][:2] != v[:2]:
        nk = byedid[v[1]]
        assert N[nk][0] == v[0], 'type mismatch ' + v[1]
        mapping[k & 0xFFFFFF] = nk & 0xFFFFFF
print('mapping', {hex(a): hex(b) for a, b in mapping.items()})
b = bytearray(open(tgt, 'rb').read())
m = masters(bytes(b)); mname = os.path.basename(new).lower()
idx = [x.lower() for x in m].index(mname)
full = {(idx << 24) | a: (idx << 24) | c for a, c in mapping.items()}
hits = []


def fix_data(d, ctx):
    """d: bytes of a record body (uncompressed). Walk subrecords, replace aligned 4-byte FormIDs inside each."""
    out = bytearray(d); i = 0
    while i < len(out):
        t = bytes(out[i:i + 4]); l = struct.unpack_from('<H', out, i + 4)[0]
        s = i + 6
        for q in range(s, s + l - 3):
            v = struct.unpack_from('<I', out, q)[0]
            if v in full:
                struct.pack_into('<I', out, q, full[v]); hits.append((ctx, t.decode('latin1'), q - s, hex(v), hex(full[v])))
        i = s + l
    return bytes(out)


def walk(o, end, out):
    while o < end:
        sig = bytes(b[o:o + 4]); size = struct.unpack_from('<I', b, o + 4)[0]
        if sig == b'GRUP':
            hdr = bytearray(b[o:o + 24]); inner = bytearray(); walk(o + 24, o + size, inner)
            struct.pack_into('<I', hdr, 4, 24 + len(inner))
            lab = struct.unpack_from('<I', hdr, 8)[0]; gt = struct.unpack_from('<i', hdr, 12)[0]
            if gt in (1, 6, 7, 8, 9, 10) and lab in full:
                struct.pack_into('<I', hdr, 8, full[lab]); hits.append(('GRUP', 'label', 0, hex(lab), hex(full[lab])))
            out += hdr + inner; o += size; continue
        hdr = bytearray(b[o:o + 24]); flags, fid = struct.unpack_from('<II', hdr, 8)
        data = bytes(b[o + 24:o + 24 + size])
        if fid in full:
            struct.pack_into('<I', hdr, 12, full[fid]); hits.append(('%08X' % fid, 'HEADER', 0, hex(fid), hex(full[fid])))
        if flags & 0x40000:
            raw = zlib.decompress(data[4:]); nraw = fix_data(raw, '%08X' % fid)
            if nraw != raw:
                data = struct.pack('<I', len(nraw)) + zlib.compress(nraw)
        else:
            data = fix_data(data, '%08X' % fid)
        struct.pack_into('<I', hdr, 4, len(data))
        out += hdr + data; o += 24 + size


hs = struct.unpack_from('<I', b, 4)[0]
res = bytearray(b[:24 + hs])
walk(24 + hs, len(b), res)
for h in hits: print('  ', h)
print(len(hits), 'rewrites;', len(b), '->', len(res), 'bytes')
if WRITE and hits:
    tmp = tgt + '.tmp-remap'; open(tmp, 'wb').write(res); os.replace(tmp, tgt); print('written', tgt)
