"""Small read-only Skyrim SE nif reader for skinned BSTriShapes.
Parses the header, locates blocks, and decodes NiSkinPartition (SSE layout:
vertex data lives in the partition), NiSkinData, NiSkinInstance /
BSDismemberSkinInstance bone lists, and BSTriShape names/bounds.
Pure python, no third-party deps."""
import struct

# flags as seen in (vertexDesc >> 44) & 0xFFF  (nifly's VertexFlags >> 4)
VF_VERTEX = 1 << 0
VF_UV = 1 << 1
VF_UV_2 = 1 << 2
VF_NORMAL = 1 << 3
VF_TANGENT = 1 << 4
VF_COLORS = 1 << 5
VF_SKINNED = 1 << 6
VF_LANDDATA = 1 << 7
VF_EYEDATA = 1 << 8
VF_FULLPREC = 1 << 10

def half_to_float(h):
    s = (h >> 15) & 1; e = (h >> 10) & 0x1f; f = h & 0x3ff
    if e == 0:
        v = (f / 1024.0) * 2.0 ** -14
    elif e == 31:
        v = float('inf') if f == 0 else float('nan')
    else:
        v = (1 + f / 1024.0) * 2.0 ** (e - 15)
    return -v if s else v

class Nif:
    def __init__(self, path):
        with open(path, 'rb') as fh:
            self.data = bytearray(fh.read())
        d = self.data
        pos = d.index(b'\n') + 1
        self.header_line = bytes(d[:pos-1]).decode('latin1')
        self.version, = struct.unpack_from('<I', d, pos); pos += 4
        pos += 1
        self.user_version, = struct.unpack_from('<I', d, pos); pos += 4
        self.num_blocks, = struct.unpack_from('<I', d, pos); pos += 4
        self.bs_ver, = struct.unpack_from('<I', d, pos); pos += 4
        self.export_info = []
        for _ in range(3):
            n = d[pos]; self.export_info.append(bytes(d[pos+1:pos+1+n]).decode('latin1')); pos += 1 + n
        if self.bs_ver == 130:
            n = d[pos]; pos += 1 + n
        num_types, = struct.unpack_from('<H', d, pos); pos += 2
        self.types = []
        for _ in range(num_types):
            n, = struct.unpack_from('<I', d, pos); pos += 4
            self.types.append(bytes(d[pos:pos+n]).decode('latin1')); pos += n
        self.type_idx = list(struct.unpack_from('<%dH' % self.num_blocks, d, pos)); pos += 2*self.num_blocks
        self.sizes_off = pos
        self.sizes = list(struct.unpack_from('<%dI' % self.num_blocks, d, pos)); pos += 4*self.num_blocks
        num_strings, = struct.unpack_from('<I', d, pos); pos += 4
        pos += 4
        self.strings = []
        for _ in range(num_strings):
            n, = struct.unpack_from('<I', d, pos); pos += 4
            self.strings.append(bytes(d[pos:pos+n]).decode('latin1')); pos += n
        num_groups, = struct.unpack_from('<I', d, pos); pos += 4
        pos += 4*num_groups
        self.block_start = pos
        self.offsets = []
        for i in range(self.num_blocks):
            self.offsets.append(pos); pos += self.sizes[i]
        self.end = pos
        self.btype = [self.types[self.type_idx[i] & 0x7FFF] for i in range(self.num_blocks)]

    def s(self, idx):
        return self.strings[idx] if idx != 0xFFFFFFFF else ''

    def blocks_of(self, t):
        return [i for i in range(self.num_blocks) if self.btype[i] == t]

    # ---- BSTriShape ----
    def trishape(self, i):
        d = self.data; o = self.offsets[i]; p = o
        name_i, = struct.unpack_from('<I', d, p); p += 4
        ned, = struct.unpack_from('<I', d, p); p += 4
        extra = list(struct.unpack_from('<%di' % ned, d, p)); p += 4*ned
        controller, = struct.unpack_from('<i', d, p); p += 4
        flags, = struct.unpack_from('<I', d, p); p += 4
        trans = struct.unpack_from('<3f', d, p); p += 12
        rot = struct.unpack_from('<9f', d, p); p += 36
        scale, = struct.unpack_from('<f', d, p); p += 4
        coll, = struct.unpack_from('<i', d, p); p += 4
        bound_off = p
        bound = struct.unpack_from('<4f', d, p); p += 16
        skin, shader, alpha = struct.unpack_from('<iii', d, p); p += 12
        vdesc, = struct.unpack_from('<Q', d, p); p += 8
        ntris, = struct.unpack_from('<I', d, p); p += 4
        nverts, = struct.unpack_from('<H', d, p); p += 2
        return dict(name=self.s(name_i), extra=extra, flags=flags, trans=trans, rot=rot, scale=scale,
                    bound=bound, bound_off=bound_off, skin=skin, shader=shader, alpha=alpha,
                    vdesc=vdesc, ntris=ntris, nverts=nverts)

    # ---- NiSkinInstance / BSDismemberSkinInstance ----
    def skininstance(self, i):
        d = self.data; p = self.offsets[i]
        sdata, spart, root, nb = struct.unpack_from('<iiiI', d, p); p += 16
        bones = list(struct.unpack_from('<%di' % nb, d, p)); p += 4*nb
        out = dict(data=sdata, partition=spart, root=root, bones=bones)
        if self.btype[i] == 'BSDismemberSkinInstance':
            npart, = struct.unpack_from('<I', d, p); p += 4
            parts = []
            for _ in range(npart):
                fl, bp = struct.unpack_from('<HH', d, p); p += 4
                parts.append((fl, bp))
            out['partitions'] = parts
        return out

    # ---- NiSkinData ----
    def skindata(self, i):
        d = self.data; p = self.offsets[i]
        skin_xf = struct.unpack_from('<13f', d, p); p += 52
        nb, = struct.unpack_from('<I', d, p); p += 4
        has_vw = d[p]; p += 1
        bones = []
        for _ in range(nb):
            xf = struct.unpack_from('<13f', d, p); p += 52
            bs = struct.unpack_from('<4f', d, p); p += 16
            nv, = struct.unpack_from('<H', d, p); p += 2
            if has_vw:
                p += 6*nv
            bones.append(dict(xf=xf, bound=bs, nv=nv))
        return dict(skin_xf=skin_xf, has_vw=has_vw, bones=bones)

    # ---- NiSkinPartition (SSE) ----
    def skinpartition(self, i):
        d = self.data; o = self.offsets[i]; p = o
        nparts, data_size, vsize = struct.unpack_from('<III', d, p); p += 12
        vdesc, = struct.unpack_from('<Q', d, p); p += 8
        vflags = (vdesc >> 44) & 0xFFF
        nverts = data_size // vsize if vsize else 0
        vdata_off = p
        p += data_size
        parts = []
        for _ in range(nparts):
            nv, nt, nbn, ns, nw = struct.unpack_from('<5H', d, p); p += 10
            bones = list(struct.unpack_from('<%dH' % nbn, d, p)); p += 2*nbn
            has_vmap = d[p]; p += 1
            vmap = None
            if has_vmap:
                vmap = list(struct.unpack_from('<%dH' % nv, d, p)); p += 2*nv
            has_vw = d[p]; p += 1
            if has_vw:
                p += 4*nv*nw
            p += 2*ns
            has_faces = d[p]; p += 1
            tris = None
            if has_faces:
                if ns:
                    raise RuntimeError('strips not supported')
                tris = list(struct.unpack_from('<%dH' % (3*nt), d, p)); p += 6*nt
            has_bi = d[p]; p += 1
            if has_bi:
                p += nv*nw
            p += 2  # unknown short
            if self.bs_ver == 100:
                p += 8  # vertex desc
                tris_copy = list(struct.unpack_from('<%dH' % (3*nt), d, p)); p += 6*nt
            else:
                tris_copy = None
            parts.append(dict(nv=nv, nt=nt, bones=bones, vmap=vmap, tris=tris, tris_copy=tris_copy, nw=nw))
        return dict(nparts=nparts, data_size=data_size, vsize=vsize, vdesc=vdesc, vflags=vflags,
                    nverts=nverts, vdata_off=vdata_off, parts=parts, end=p)

    def vertex_layout(self, vflags, vsize):
        """Return dict of field offsets inside one vertex for the given flags."""
        off = 0; lay = {}
        # Skyrim SE (bs 100) always stores full-precision float positions;
        # half positions only exist in FO4 (bs 130) without VF_FULLPREC.
        full = bool(vflags & VF_FULLPREC) or self.bs_ver == 100
        if vflags & VF_VERTEX:
            lay['pos'] = (off, 'full' if full else 'half')
            off += 16 if full else 8   # pos(3) + bitangentX
        if vflags & VF_UV:
            lay['uv'] = off; off += 4
        if vflags & VF_NORMAL:
            lay['normal'] = off; off += 4
            if vflags & VF_TANGENT:
                lay['tangent'] = off; off += 4
        if vflags & VF_COLORS:
            lay['colors'] = off; off += 4
        if vflags & VF_SKINNED:
            lay['weights'] = off; off += 8
            lay['bindices'] = off; off += 4
        if vflags & VF_EYEDATA:
            lay['eye'] = off; off += 4
        lay['size'] = off
        assert off == vsize, (off, vsize, hex(vflags))
        return lay

    def vertices(self, i):
        sp = self.skinpartition(i)
        lay = self.vertex_layout(sp['vflags'], sp['vsize'])
        d = self.data
        out = []
        for k in range(sp['nverts']):
            b = sp['vdata_off'] + k*sp['vsize']
            po, kind = lay['pos']
            if kind == 'full':
                pos = struct.unpack_from('<3f', d, b+po)
            else:
                pos = tuple(half_to_float(h) for h in struct.unpack_from('<3H', d, b+po))
            uv = tuple(half_to_float(h) for h in struct.unpack_from('<2H', d, b+lay['uv'])) if 'uv' in lay else None
            w = tuple(half_to_float(h) for h in struct.unpack_from('<4H', d, b+lay['weights'])) if 'weights' in lay else None
            bi = tuple(d[b+lay['bindices']:b+lay['bindices']+4]) if 'bindices' in lay else None
            out.append(dict(pos=pos, uv=uv, w=w, bi=bi))
        return out, sp, lay
