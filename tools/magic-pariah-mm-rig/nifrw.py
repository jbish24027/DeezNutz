"""Block-level Skyrim SE NIF reader/writer (stream 100).

Loads a NIF into a document of raw blocks, knows where every block
reference and string-table index lives for the block types used by
outfit meshes, and re-serializes with a rebuilt header. Identity
round-trip must be byte-exact (see test_roundtrip.py).
"""
import struct

NAMED = {'NiNode', 'BSTriShape', 'BSDynamicTriShape', 'BSLightingShaderProperty',
         'NiAlphaProperty', 'NiStringExtraData', 'BSEffectShaderProperty'}


class Doc:
    def __init__(self, path=None):
        self.header_str = ''
        self.version = 0x14020007
        self.endian = 1
        self.user_version = 12
        self.stream = 100
        self.export_info = [b'', b'', b'']
        self.max_filepath = None
        self.blocks = []      # list of [typename, bytearray]
        self.strings = []     # list of str
        self.groups = []
        self.roots = [0]
        if path:
            self.load(path)

    # ------------------------------------------------------------ load
    def load(self, path):
        with open(path, 'rb') as f:
            d = f.read()
        nl = d.index(b'\n')
        self.header_str = d[:nl].decode('ascii')
        o = nl + 1

        def u8():
            nonlocal o
            v = d[o]; o += 1; return v

        def u16():
            nonlocal o
            v = struct.unpack_from('<H', d, o)[0]; o += 2; return v

        def u32():
            nonlocal o
            v = struct.unpack_from('<I', d, o)[0]; o += 4; return v

        def i32():
            nonlocal o
            v = struct.unpack_from('<i', d, o)[0]; o += 4; return v

        self.version = u32(); self.endian = u8(); self.user_version = u32()
        nblocks = u32(); self.stream = u32()
        self.export_info = []
        for _ in range(3):
            ln = u8(); self.export_info.append(d[o:o + ln]); o += ln
        if self.stream >= 130:
            ln = u8(); self.max_filepath = d[o:o + ln]; o += ln
        nbt = u16()
        types = []
        for _ in range(nbt):
            ln = u32(); types.append(d[o:o + ln].decode('ascii')); o += ln
        tidx = [u16() for _ in range(nblocks)]
        sizes = [u32() for _ in range(nblocks)]
        ns = u32(); u32()
        self.strings = []
        for _ in range(ns):
            ln = u32(); self.strings.append(d[o:o + ln].decode('utf-8', 'replace')); o += ln
        ng = u32(); self.groups = [u32() for _ in range(ng)]
        self.blocks = []
        for i in range(nblocks):
            self.blocks.append([types[tidx[i]], bytearray(d[o:o + sizes[i]])]); o += sizes[i]
        nr = u32(); self.roots = [i32() for _ in range(nr)]
        assert o == len(d), 'trailing bytes after footer: %d' % (len(d) - o)

    # ------------------------------------------------------------ save
    def tobytes(self):
        out = bytearray()
        out += self.header_str.encode('ascii') + b'\n'
        out += struct.pack('<IBII', self.version, self.endian, self.user_version, len(self.blocks))
        out += struct.pack('<I', self.stream)
        for s in self.export_info:
            out += bytes([len(s)]) + s
        if self.stream >= 130:
            mf = self.max_filepath or b''
            out += bytes([len(mf)]) + mf
        types = []
        for t, _ in self.blocks:
            if t not in types:
                types.append(t)
        out += struct.pack('<H', len(types))
        for t in types:
            b = t.encode('ascii'); out += struct.pack('<I', len(b)) + b
        for t, _ in self.blocks:
            out += struct.pack('<H', types.index(t))
        for _, b in self.blocks:
            out += struct.pack('<I', len(b))
        enc = [s.encode('utf-8') for s in self.strings]
        out += struct.pack('<II', len(enc), max([len(s) for s in enc] + [0]))
        for s in enc:
            out += struct.pack('<I', len(s)) + s
        out += struct.pack('<I', len(self.groups))
        for g in self.groups:
            out += struct.pack('<I', g)
        for _, b in self.blocks:
            out += b
        out += struct.pack('<I', len(self.roots))
        for r in self.roots:
            out += struct.pack('<i', r)
        return bytes(out)

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.tobytes())

    # ------------------------------------------------------------ strings
    def sidx(self, s):
        """index of string s in the table, adding it if absent."""
        if s not in self.strings:
            self.strings.append(s)
        return self.strings.index(s)

    def name_of(self, i):
        t, b = self.blocks[i]
        if t not in NAMED:
            return None
        off = 4 if t == 'BSLightingShaderProperty' else 0
        si = struct.unpack_from('<I', b, off)[0]
        return self.strings[si] if si < len(self.strings) else None

    def find(self, typename, name):
        for i, (t, b) in enumerate(self.blocks):
            if t == typename and self.name_of(i) == name:
                return i
        return None


def _objnet(b, o):
    """NiObjectNET fields: returns (name_off, extra_ref_offs, ctrl_off, next_off)."""
    name_off = o; o += 4
    ne = struct.unpack_from('<I', b, o)[0]; o += 4
    extras = [o + 4 * k for k in range(ne)]; o += 4 * ne
    ctrl = o; o += 4
    return name_off, extras, ctrl, o


def slots(t, b):
    """Return (ref_offsets, string_offsets) for block type t with bytes b.
    Refs are i32 block indices; strings are u32 string-table indices."""
    refs, strs = [], []
    if t == 'NiNode':
        n, ex, c, o = _objnet(b, 0); strs.append(n); refs += ex; refs.append(c)
        o += 4 + 12 + 36 + 4           # flags, trans, rot, scale
        refs.append(o); o += 4         # collision
        nc = struct.unpack_from('<I', b, o)[0]; o += 4
        refs += [o + 4 * k for k in range(nc)]; o += 4 * nc
        nf = struct.unpack_from('<I', b, o)[0]; o += 4
        refs += [o + 4 * k for k in range(nf)]; o += 4 * nf
    elif t in ('BSTriShape', 'BSDynamicTriShape'):
        n, ex, c, o = _objnet(b, 0); strs.append(n); refs += ex; refs.append(c)
        o += 4 + 12 + 36 + 4
        refs.append(o); o += 4         # collision
        o += 16                        # bound
        refs += [o, o + 4, o + 8]      # skin, shader, alpha
    elif t in ('BSDismemberSkinInstance', 'NiSkinInstance'):
        refs += [0, 4, 8]
        nb = struct.unpack_from('<I', b, 12)[0]
        refs += [16 + 4 * k for k in range(nb)]
    elif t == 'BSLightingShaderProperty':
        n, ex, c, o = _objnet(b, 4); strs.append(n); refs += ex; refs.append(c)
        o += 4 + 4 + 8 + 8             # sf1, sf2, uv offset, uv scale
        refs.append(o)                 # texture set
    elif t == 'BSEffectShaderProperty':
        n, ex, c, o = _objnet(b, 0); strs.append(n); refs += ex; refs.append(c)
    elif t == 'NiAlphaProperty':
        n, ex, c, o = _objnet(b, 0); strs.append(n); refs += ex; refs.append(c)
    elif t == 'NiStringExtraData':
        strs += [0, 4]
    elif t in ('BSInvMarker', 'NiIntegerExtraData', 'NiFloatExtraData', 'NiBooleanExtraData'):
        strs.append(0)                 # NiExtraData name only; the rest is plain data
    elif t in ('NiSkinData', 'NiSkinPartition', 'BSShaderTextureSet'):
        pass
    else:
        raise NotImplementedError('no slot map for block type %s' % t)
    return refs, strs


def remap_block(t, b, refmap, strmap):
    """Rewrite refs/strings in place using dict maps (missing ref -> KeyError)."""
    refs, strs = slots(t, b)
    for off in refs:
        v = struct.unpack_from('<i', b, off)[0]
        if v >= 0:
            struct.pack_into('<i', b, off, refmap[v])
    for off in strs:
        v = struct.unpack_from('<I', b, off)[0]
        if v != 0xFFFFFFFF:
            struct.pack_into('<I', b, off, strmap[v])


def block_refs(t, b):
    refs, _ = slots(t, b)
    return [struct.unpack_from('<i', b, off)[0] for off in refs]


def reachable(doc):
    seen = set(); stack = list(doc.roots)
    while stack:
        i = stack.pop()
        if i < 0 or i in seen:
            continue
        seen.add(i)
        for r in block_refs(*doc.blocks[i]):
            if r >= 0:
                stack.append(r)
    return seen


def rebuild(doc, keep_order=None):
    """Drop unreachable blocks and renumber. Returns (newdoc, oldidx->newidx)."""
    keep = keep_order if keep_order is not None else sorted(reachable(doc))
    refmap = {old: new for new, old in enumerate(keep)}
    nd = Doc()
    for a in ('header_str', 'version', 'endian', 'user_version', 'stream',
              'export_info', 'max_filepath', 'groups'):
        setattr(nd, a, getattr(doc, a))
    # strings: keep only used ones, in first-use order
    used = []
    for old in keep:
        t, b = doc.blocks[old]
        _, strs = slots(t, b)
        for off in strs:
            v = struct.unpack_from('<I', b, off)[0]
            if v != 0xFFFFFFFF and v not in used:
                used.append(v)
    strmap = {old: new for new, old in enumerate(used)}
    nd.strings = [doc.strings[v] for v in used]
    for old in keep:
        t, b = doc.blocks[old]
        nb = bytearray(b)
        remap_block(t, nb, refmap, strmap)
        nd.blocks.append([t, nb])
    nd.roots = [refmap[r] for r in doc.roots]
    return nd, refmap


# ------------------------------------------------------------ node helpers
def parse_node(b):
    o = 0
    name = struct.unpack_from('<I', b, o)[0]; o += 4
    ne = struct.unpack_from('<I', b, o)[0]; o += 4
    extra = list(struct.unpack_from('<%di' % ne, b, o)); o += 4 * ne
    ctrl = struct.unpack_from('<i', b, o)[0]; o += 4
    flags = struct.unpack_from('<I', b, o)[0]; o += 4
    trans = struct.unpack_from('<3f', b, o); o += 12
    rot = struct.unpack_from('<9f', b, o); o += 36
    scale = struct.unpack_from('<f', b, o)[0]; o += 4
    coll = struct.unpack_from('<i', b, o)[0]; o += 4
    nc = struct.unpack_from('<I', b, o)[0]; o += 4
    children = list(struct.unpack_from('<%di' % nc, b, o)); o += 4 * nc
    nf = struct.unpack_from('<I', b, o)[0]; o += 4
    effects = list(struct.unpack_from('<%di' % nf, b, o)); o += 4 * nf
    assert o == len(b), 'NiNode size mismatch'
    return dict(name=name, extra=extra, ctrl=ctrl, flags=flags, trans=trans, rot=rot,
                scale=scale, coll=coll, children=children, effects=effects)


def build_node(n):
    b = bytearray()
    b += struct.pack('<I', n['name'])
    b += struct.pack('<I', len(n['extra'])) + struct.pack('<%di' % len(n['extra']), *n['extra'])
    b += struct.pack('<i', n['ctrl'])
    b += struct.pack('<I', n['flags'])
    b += struct.pack('<3f', *n['trans']) + struct.pack('<9f', *n['rot']) + struct.pack('<f', n['scale'])
    b += struct.pack('<i', n['coll'])
    b += struct.pack('<I', len(n['children'])) + struct.pack('<%di' % len(n['children']), *n['children'])
    b += struct.pack('<I', len(n['effects'])) + struct.pack('<%di' % len(n['effects']), *n['effects'])
    return b


def parse_shape_hdr(b):
    """BSTriShape header -> dict; everything after dataSize kept raw in 'tail'."""
    o = 0
    d = {}
    d['name'] = struct.unpack_from('<I', b, o)[0]; o += 4
    ne = struct.unpack_from('<I', b, o)[0]; o += 4
    d['extra'] = list(struct.unpack_from('<%di' % ne, b, o)); o += 4 * ne
    d['ctrl'] = struct.unpack_from('<i', b, o)[0]; o += 4
    d['flags'] = struct.unpack_from('<I', b, o)[0]; o += 4
    d['trans'] = struct.unpack_from('<3f', b, o); o += 12
    d['rot'] = struct.unpack_from('<9f', b, o); o += 36
    d['scale'] = struct.unpack_from('<f', b, o)[0]; o += 4
    d['coll'] = struct.unpack_from('<i', b, o)[0]; o += 4
    d['bound'] = struct.unpack_from('<4f', b, o); o += 16
    d['skin'] = struct.unpack_from('<i', b, o)[0]; o += 4
    d['shader'] = struct.unpack_from('<i', b, o)[0]; o += 4
    d['alpha'] = struct.unpack_from('<i', b, o)[0]; o += 4
    d['vdesc'] = struct.unpack_from('<Q', b, o)[0]; o += 8
    d['ntri'] = struct.unpack_from('<H', b, o)[0]; o += 2
    d['nvert'] = struct.unpack_from('<H', b, o)[0]; o += 2
    d['dsize'] = struct.unpack_from('<I', b, o)[0]; o += 4
    d['tail'] = bytes(b[o:])
    return d


def build_shape(d):
    b = bytearray()
    b += struct.pack('<I', d['name'])
    b += struct.pack('<I', len(d['extra'])) + struct.pack('<%di' % len(d['extra']), *d['extra'])
    b += struct.pack('<i', d['ctrl']); b += struct.pack('<I', d['flags'])
    b += struct.pack('<3f', *d['trans']) + struct.pack('<9f', *d['rot']) + struct.pack('<f', d['scale'])
    b += struct.pack('<i', d['coll']); b += struct.pack('<4f', *d['bound'])
    b += struct.pack('<iii', d['skin'], d['shader'], d['alpha'])
    b += struct.pack('<Q', d['vdesc']); b += struct.pack('<HHI', d['ntri'], d['nvert'], d['dsize'])
    b += d['tail']
    return b


def parse_dismember(b):
    o = 0
    data, part, root = struct.unpack_from('<iii', b, o); o += 12
    nb = struct.unpack_from('<I', b, o)[0]; o += 4
    bones = list(struct.unpack_from('<%di' % nb, b, o)); o += 4 * nb
    npart = struct.unpack_from('<I', b, o)[0]; o += 4
    parts = [struct.unpack_from('<HH', b, o + 4 * k) for k in range(npart)]; o += 4 * npart
    assert o == len(b), 'BSDismemberSkinInstance size mismatch'
    return dict(data=data, part=part, root=root, bones=bones, parts=parts)


def build_dismember(d):
    b = bytearray(struct.pack('<iii', d['data'], d['part'], d['root']))
    b += struct.pack('<I', len(d['bones'])) + struct.pack('<%di' % len(d['bones']), *d['bones'])
    b += struct.pack('<I', len(d['parts']))
    for f, p in d['parts']:
        b += struct.pack('<HH', f, p)
    return b
