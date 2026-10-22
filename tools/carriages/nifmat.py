import os, sys, struct
sys.path.insert(0, r'C:/1. AUTHORIA/_tools/magic-pariah-mm-rig')
from nifrw import Doc, parse_shape_hdr
def raw_types(path):
    """Block-type table in the file's own order (nifrw rewrites it in first-use order; keep the original)."""
    raw = open(path, 'rb').read(); o = raw.index(b'\n') + 1 + 4 + 1 + 4 + 4 + 4
    for _ in range(3): o += 1 + raw[o]
    nbt = struct.unpack_from('<H', raw, o)[0]; o += 2; types = []
    for _ in range(nbt):
        ln = struct.unpack_from('<I', raw, o)[0]; types.append(raw[o + 4:o + 4 + ln].decode('ascii')); o += 4 + ln
    return types

def tobytes_ordered(doc, types):
    """Doc.tobytes() with a fixed block-type table order."""
    out = bytearray(); out += doc.header_str.encode('ascii') + b'\n'
    out += struct.pack('<IBII', doc.version, doc.endian, doc.user_version, len(doc.blocks)); out += struct.pack('<I', doc.stream)
    for s in doc.export_info: out += bytes([len(s)]) + s
    if doc.stream >= 130: mf = doc.max_filepath or b''; out += bytes([len(mf)]) + mf
    assert set(t for t, _ in doc.blocks) <= set(types)
    out += struct.pack('<H', len(types))
    for t in types: b = t.encode('ascii'); out += struct.pack('<I', len(b)) + b
    for t, _ in doc.blocks: out += struct.pack('<H', types.index(t))
    for _, b in doc.blocks: out += struct.pack('<I', len(b))
    enc = [s.encode('utf-8') for s in doc.strings]
    out += struct.pack('<II', len(enc), max([len(s) for s in enc] + [0]))
    for s in enc: out += struct.pack('<I', len(s)) + s
    out += struct.pack('<I', len(doc.groups))
    for g in doc.groups: out += struct.pack('<I', g)
    for _, b in doc.blocks: out += b
    out += struct.pack('<I', len(doc.roots))
    for r in doc.roots: out += struct.pack('<i', r)
    return bytes(out)

def shader(doc, si):
    t, b = doc.blocks[si]; assert t == 'BSLightingShaderProperty', t
    o = 4; name = struct.unpack_from('<I', b, o)[0]; o += 4
    ne = struct.unpack_from('<I', b, o)[0]; o += 4 + 4 * ne
    ctrl = struct.unpack_from('<i', b, o)[0]; o += 4
    f1o = o; f1, f2 = struct.unpack_from('<II', b, o); o += 8
    o += 16  # uv offset + scale
    tso = o; ts = struct.unpack_from('<i', b, o)[0]
    return dict(stype=struct.unpack_from('<I', b, 0)[0], name=name, ne=ne, ctrl=ctrl, f1=f1, f2=f2, f1o=f1o, tso=tso, ts=ts)

def texset(doc, ti):
    t, b = doc.blocks[ti]; assert t == 'BSShaderTextureSet', t
    n = struct.unpack_from('<I', b, 0)[0]; q = 4; out = []
    for k in range(n):
        ln = struct.unpack_from('<I', b, q)[0]; q += 4; out.append(b[q:q + ln].decode('latin-1')); q += ln
    return out

def shapes(doc):
    out = []
    for i, (t, b) in enumerate(doc.blocks):
        if t not in ('BSTriShape', 'BSDynamicTriShape'): continue
        h = parse_shape_hdr(b)
        if h['shader'] < 0 or doc.blocks[h['shader']][0] != 'BSLightingShaderProperty': continue
        s = shader(doc, h['shader']); tex = texset(doc, s['ts']) if s['ts'] >= 0 else []
        out.append(dict(idx=i, name=doc.strings[h['name']], sh=h['shader'], s=s, tex=tex, tex0=(tex[0].lower() if tex else '')))
    return out

