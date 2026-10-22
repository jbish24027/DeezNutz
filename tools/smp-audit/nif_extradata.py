"""Add (or retarget) the HDT-SMP NiStringExtraData on a Skyrim SE nif.

add_smp_extradata(src, dst, xml_path):
  - if a 'HDT Skinned Mesh Physics Object' NiStringExtraData already exists: rewrite its
    string to xml_path (header string edit only)
  - else: append a new NiStringExtraData block, link it from the ROOT NiNode's extra data
    list, register the two strings, and rebuild the header.
Pure python; verifies by re-parsing. Read-only on src.
"""
import struct, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HDT_NAME = 'HDT Skinned Mesh Physics Object'

class Header:
    def __init__(self, data):
        d = data
        pos = d.index(b'\n') + 1
        self.line = bytes(d[:pos])
        self.version, = struct.unpack_from('<I', d, pos); pos += 4
        self.endian = d[pos]; pos += 1
        self.user_version, = struct.unpack_from('<I', d, pos); pos += 4
        self.num_blocks, = struct.unpack_from('<I', d, pos); pos += 4
        self.bs_ver, = struct.unpack_from('<I', d, pos); pos += 4
        self.export = []
        for _ in range(3):
            n = d[pos]; self.export.append(bytes(d[pos+1:pos+1+n])); pos += 1 + n
        self.maxpath = None
        if self.bs_ver == 130:
            n = d[pos]; self.maxpath = bytes(d[pos+1:pos+1+n]); pos += 1 + n
        num_types, = struct.unpack_from('<H', d, pos); pos += 2
        self.types = []
        for _ in range(num_types):
            n, = struct.unpack_from('<I', d, pos); pos += 4
            self.types.append(bytes(d[pos:pos+n])); pos += n
        self.type_idx = list(struct.unpack_from('<%dH' % self.num_blocks, d, pos)); pos += 2*self.num_blocks
        self.sizes = list(struct.unpack_from('<%dI' % self.num_blocks, d, pos)); pos += 4*self.num_blocks
        num_strings, = struct.unpack_from('<I', d, pos); pos += 4
        self.max_len, = struct.unpack_from('<I', d, pos); pos += 4
        self.strings = []
        for _ in range(num_strings):
            n, = struct.unpack_from('<I', d, pos); pos += 4
            self.strings.append(bytes(d[pos:pos+n])); pos += n
        num_groups, = struct.unpack_from('<I', d, pos); pos += 4
        self.groups = list(struct.unpack_from('<%dI' % num_groups, d, pos)); pos += 4*num_groups
        self.end = pos

    def serialize(self):
        out = bytearray(self.line)
        out += struct.pack('<I', self.version) + bytes([self.endian]) + struct.pack('<II', self.user_version, self.num_blocks) + struct.pack('<I', self.bs_ver)
        for e in self.export:
            out += bytes([len(e)]) + e
        if self.bs_ver == 130:
            out += bytes([len(self.maxpath)]) + self.maxpath
        out += struct.pack('<H', len(self.types))
        for t in self.types:
            out += struct.pack('<I', len(t)) + t
        out += struct.pack('<%dH' % self.num_blocks, *self.type_idx)
        out += struct.pack('<%dI' % self.num_blocks, *self.sizes)
        out += struct.pack('<II', len(self.strings), max((len(s) for s in self.strings), default=0))
        for s in self.strings:
            out += struct.pack('<I', len(s)) + s
        out += struct.pack('<I', len(self.groups)) + struct.pack('<%dI' % len(self.groups), *self.groups)
        return bytes(out)

def add_smp_extradata(src, dst, xml_path):
    with open(src, 'rb') as fh:
        data = bytearray(fh.read())
    h = Header(data)
    assert h.serialize() == bytes(data[:h.end]), 'header round-trip mismatch on %s' % src
    # blocks
    offs = []; p = h.end
    for i in range(h.num_blocks):
        offs.append(p); p += h.sizes[i]
    footer = bytes(data[p:])
    assert len(footer) >= 4
    blocks = [bytes(data[offs[i]:offs[i]+h.sizes[i]]) for i in range(h.num_blocks)]
    types_str = [t.decode('latin1') for t in h.types]
    def stridx(s):
        b = s.encode('latin1')
        if b in h.strings:
            return h.strings.index(b)
        h.strings.append(b); return len(h.strings) - 1
    # existing?
    for i in range(h.num_blocks):
        if types_str[h.type_idx[i]] == 'NiStringExtraData':
            name_i, str_i = struct.unpack_from('<II', blocks[i], 0)
            if name_i != 0xFFFFFFFF and h.strings[name_i].decode('latin1') == HDT_NAME:
                # retarget: point at (possibly new) string
                new_i = stridx(xml_path)
                blocks[i] = struct.pack('<II', name_i, new_i)
                mode = 'retargeted existing block #%d' % i
                break
    else:
        # append new block
        if 'NiStringExtraData' not in types_str:
            h.types.append(b'NiStringExtraData'); types_str.append('NiStringExtraData')
        tidx = types_str.index('NiStringExtraData')
        name_i = stridx(HDT_NAME); str_i = stridx(xml_path)
        newblock = struct.pack('<II', name_i, str_i)
        new_index = h.num_blocks
        blocks.append(newblock); h.type_idx.append(tidx); h.sizes.append(len(newblock)); h.num_blocks += 1
        # link from the ROOT node named in the footer
        nroots, = struct.unpack_from('<I', footer, 0)
        root = struct.unpack_from('<i', footer, 4)[0]
        root_t = types_str[h.type_idx[root]]
        assert root_t in ('NiNode', 'BSFadeNode', 'BSLeafAnimNode', 'BSTreeNode', 'BSOrderedNode', 'BSMultiBoundNode'), 'root #%d is %s' % (root, root_t)
        rb = bytearray(blocks[root])
        n_extra, = struct.unpack_from('<I', rb, 4)
        refs = list(struct.unpack_from('<%di' % n_extra, rb, 8))
        refs.append(new_index)
        rest = rb[8 + 4*n_extra:]
        blocks[root] = bytes(rb[:4]) + struct.pack('<I', n_extra + 1) + struct.pack('<%di' % (n_extra+1), *refs) + bytes(rest)
        h.sizes[root] = len(blocks[root])
        mode = 'added block #%d linked from root #%d (root extra data %d -> %d)' % (new_index, root, n_extra, n_extra + 1)
    out = h.serialize() + b''.join(blocks) + footer
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'wb') as fh:
        fh.write(out)
    # verify with the generic parser
    from niflib import Nif
    V = Nif(dst)
    assert len(V.data) - V.end == len(footer), 'footer mismatch'
    found = None
    for i in V.blocks_of('NiStringExtraData'):
        a, b = struct.unpack_from('<II', V.data, V.offsets[i])
        if V.s(a) == HDT_NAME:
            found = V.s(b)
    assert found == xml_path, (found, xml_path)
    return mode

if __name__ == '__main__':
    src, dst, xml = sys.argv[1:4]
    print(add_smp_extradata(src, dst, xml))
