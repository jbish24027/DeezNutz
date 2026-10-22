"""Minimal Skyrim SE NIF parser: positions, skin weights, bind transforms.

Targets Gamebryo 20.2.0.7, user 12, stream 100 (Skyrim SE).
Handles BSTriShape / BSDynamicTriShape, NiSkinInstance / BSDismemberSkinInstance,
NiSkinData, NiSkinPartition (SSE: vertex buffer lives in the partition for
skinned shapes; dynamic shapes keep float4 positions in the shape block).
"""
import struct, sys, json

class R:
    def __init__(self, data, off=0):
        self.d = data; self.o = off
    def u8(self):  v = self.d[self.o]; self.o += 1; return v
    def u16(self): v = struct.unpack_from('<H', self.d, self.o)[0]; self.o += 2; return v
    def i32(self): v = struct.unpack_from('<i', self.d, self.o)[0]; self.o += 4; return v
    def u32(self): v = struct.unpack_from('<I', self.d, self.o)[0]; self.o += 4; return v
    def u64(self): v = struct.unpack_from('<Q', self.d, self.o)[0]; self.o += 8; return v
    def f32(self): v = struct.unpack_from('<f', self.d, self.o)[0]; self.o += 4; return v
    def f16(self):
        h = self.u16()
        s = (h >> 15) & 1; e = (h >> 10) & 0x1F; m = h & 0x3FF
        if e == 0: val = m / 1024.0 * 2**-14
        elif e == 31: val = float('inf') if m == 0 else float('nan')
        else: val = (1 + m / 1024.0) * 2**(e - 15)
        return -val if s else val
    def floats(self, n): v = struct.unpack_from('<%df' % n, self.d, self.o); self.o += 4*n; return v
    def bytes_(self, n): v = self.d[self.o:self.o+n]; self.o += n; return v

class Nif:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            data = f.read()
        self.data = data
        nl = data.index(b'\x0a')
        self.header_str = data[:nl].decode('ascii')
        r = R(data, nl + 1)
        self.version = r.u32()
        self.endian = r.u8()
        self.user_version = r.u32()
        self.num_blocks = r.u32()
        self.stream = r.u32()  # BS stream / user version 2
        # export info: 3 short strings (len-prefixed u8)
        for _ in range(3):
            ln = r.u8(); r.bytes_(ln)
        if self.stream >= 130:
            ln = r.u8(); r.bytes_(ln)  # max filepath
        nbt = r.u16()
        self.block_types = []
        for _ in range(nbt):
            ln = r.u32(); self.block_types.append(r.bytes_(ln).decode('ascii'))
        self.block_type_idx = [r.u16() for _ in range(self.num_blocks)]
        self.block_sizes = [r.u32() for _ in range(self.num_blocks)]
        ns = r.u32(); r.u32()  # num strings, max len
        self.strings = []
        for _ in range(ns):
            ln = r.u32(); self.strings.append(r.bytes_(ln).decode('ascii', 'replace'))
        ng = r.u32(); [r.u32() for _ in range(ng)]
        self.block_offsets = []
        off = r.o
        for i in range(self.num_blocks):
            self.block_offsets.append(off)
            off += self.block_sizes[i]
        self.trailer_off = off

    def btype(self, i): return self.block_types[self.block_type_idx[i]]
    def blocks_of(self, name): return [i for i in range(self.num_blocks) if self.btype(i) == name]
    def block_reader(self, i): return R(self.data, self.block_offsets[i])
    def block_name(self, i):
        r = self.block_reader(i)
        si = r.u32()
        return self.strings[si] if si < len(self.strings) else '<none>'

    def parse_shape(self, i):
        """BSTriShape / BSDynamicTriShape -> dict"""
        r = self.block_reader(i)
        out = {'block': i, 'type': self.btype(i)}
        si = r.u32(); out['name'] = self.strings[si] if si < len(self.strings) else '<none>'
        ne = r.u32(); [r.i32() for _ in range(ne)]
        r.i32()  # controller
        out['flags'] = r.u32()
        out['translation'] = r.floats(3)
        out['rotation'] = r.floats(9)
        out['scale'] = r.f32()
        r.i32()  # collision
        out['bound'] = r.floats(4)
        out['skin_ref'] = r.i32()
        out['shader_ref'] = r.i32()
        out['alpha_ref'] = r.i32()
        desc = r.u64(); out['vertex_desc'] = desc
        vsize = (desc & 0xF) * 4
        vflags = (desc >> 44) & 0xFFF
        out['vertex_size'] = vsize
        out['vertex_flags'] = vflags
        ntri = r.u16()
        nvert = r.u16()
        dsize = r.u32()
        out['num_triangles'] = ntri; out['num_vertices'] = nvert; out['data_size'] = dsize
        out['positions'] = None
        out['vbuf_off'] = r.o if dsize else None
        if dsize:
            out['positions'], out['weights_vb'] = self.read_vbuf(r, nvert, desc)
            r.o = out['vbuf_off'] + dsize
            r.bytes_(6 * ntri)  # triangles
        if out['type'] == 'BSDynamicTriShape':
            # anchor dynamic float4 data at the block tail; u32 size sits just before
            end = self.block_offsets[i] + self.block_sizes[i]
            dyn_off = end - nvert * 16
            dyn_size = struct.unpack_from('<I', self.d if False else self.data, dyn_off - 4)[0]
            assert dyn_size == nvert * 16, ('dyn size mismatch', dyn_size, nvert * 16)
            r.o = dyn_off
            pos = []
            for _ in range(nvert):
                x, y, z, w = r.floats(4)
                pos.append((x, y, z))
            out['positions'] = pos
        return out

    def read_vbuf(self, r, nvert, desc, with_weights=True):
        vsize = (desc & 0xF) * 4
        vflags = (desc >> 44) & 0xFFF
        has_vtx = bool(vflags & 0x1)
        has_uv = bool(vflags & 0x2)
        has_nrm = bool(vflags & 0x8)
        has_tan = bool(vflags & 0x10)
        has_col = bool(vflags & 0x20)
        has_skin = bool(vflags & 0x40)
        has_eye = bool(vflags & 0x100)
        # infer position precision from stride: extras are fixed-size
        extras = (4 if has_uv else 0) + (4 if has_nrm else 0) + (4 if has_tan else 0) \
               + (4 if has_col else 0) + (12 if has_skin else 0) + (4 if has_eye else 0)
        if has_vtx and vsize == 16 + extras:
            full = True
        elif has_vtx and vsize == 8 + extras:
            full = False
        elif has_vtx:
            raise ValueError('cannot infer position precision: vsize=%d extras=%d' % (vsize, extras))
        base = r.o
        positions = []; weights = []
        for vi in range(nvert):
            r.o = base + vi * vsize
            if has_vtx:
                if full:
                    x, y, z = r.floats(3); r.f32()
                else:
                    x = r.f16(); y = r.f16(); z = r.f16(); r.f16()
                positions.append((x, y, z))
            if has_uv: r.o += 4
            if has_nrm: r.o += 4
            if has_tan: r.o += 4
            if has_col: r.o += 4
            if has_skin:
                w = [r.f16() for _ in range(4)]
                b = [r.u8() for _ in range(4)]
                weights.append(list(zip(b, w)))
            if has_eye: r.o += 4
        r.o = base + nvert * vsize
        return positions, weights

    def parse_skin_instance(self, i):
        r = self.block_reader(i)
        out = {'block': i, 'type': self.btype(i)}
        out['data_ref'] = r.i32()
        out['partition_ref'] = r.i32()
        out['root_ref'] = r.i32()
        nb = r.u32()
        out['bone_refs'] = [r.i32() for _ in range(nb)]
        out['bone_names'] = [self.block_name(b) for b in out['bone_refs']]
        return out

    def parse_skin_data(self, i):
        r = self.block_reader(i)
        out = {'block': i}
        out['global_transform'] = {'rot': r.floats(9), 'trans': r.floats(3), 'scale': r.f32()}
        nb = r.u32()
        hvw = r.u8()
        out['has_vertex_weights'] = hvw
        bones = []
        for _ in range(nb):
            bt = {'rot': r.floats(9), 'trans': r.floats(3), 'scale': r.f32()}
            bs = r.floats(4)
            nv = r.u16()
            vw = []
            if hvw:
                for _ in range(nv):
                    vidx = r.u16(); w = r.f32(); vw.append((vidx, w))
            bones.append({'transform': bt, 'bound': bs, 'weights': vw})
        out['bones'] = bones
        assert r.o - self.block_offsets[i] == self.block_sizes[i], 'NiSkinData size mismatch'
        return out

    def parse_skin_partition(self, i, want_tris=False):
        r = self.block_reader(i)
        out = {'block': i}
        np_ = r.u32()
        out['num_partitions'] = np_
        if self.stream == 100:
            dsize = r.u32()
            vsize = r.u32()
            desc = r.u64()
            out['data_size'] = dsize; out['vertex_size'] = vsize; out['vertex_desc'] = desc
            if dsize > 0:
                nvert = dsize // vsize
                out['num_vertices'] = nvert
                pos, wts = self.read_vbuf(r, nvert, desc)
                out['positions'] = pos; out['weights_vb'] = wts
        parts = []
        for _ in range(np_):
            p = {}
            nv = r.u16(); nt = r.u16(); nb = r.u16(); ns = r.u16(); nwpv = r.u16()
            p['num_vertices'] = nv; p['num_triangles'] = nt; p['num_bones'] = nb
            p['bones'] = [r.u16() for _ in range(nb)]
            if r.u8(): p['vertex_map'] = [r.u16() for _ in range(nv)]
            if r.u8(): p['weights'] = [[r.f32() for _ in range(nwpv)] for _ in range(nv)]
            slens = [r.u16() for _ in range(ns)]
            if r.u8():
                if ns:
                    p['strips'] = [[r.u16() for _ in range(l)] for l in slens]
                else:
                    p['tris'] = [(r.u16(), r.u16(), r.u16()) for _ in range(nt)]
            if r.u8(): p['bone_indices'] = [[r.u8() for _ in range(nwpv)] for _ in range(nv)]
            r.u16()  # unknown
            if self.stream == 100:
                r.u64()  # per-partition vertex desc
                p['tris_copy'] = [(r.u16(), r.u16(), r.u16()) for _ in range(nt)]
            parts.append(p)
        out['partitions'] = parts
        assert r.o - self.block_offsets[i] == self.block_sizes[i], \
            'NiSkinPartition size mismatch: consumed %d vs %d' % (r.o - self.block_offsets[i], self.block_sizes[i])
        return out

def load_mesh(path):
    """Returns list of shapes with resolved positions + per-vertex weights by bone name."""
    nif = Nif(path)
    shapes = []
    for i in range(nif.num_blocks):
        if nif.btype(i) in ('BSTriShape', 'BSDynamicTriShape'):
            sh = nif.parse_shape(i)
            if sh['skin_ref'] >= 0:
                si = nif.parse_skin_instance(sh['skin_ref'])
                sh['bones'] = si['bone_names']
                sd = nif.parse_skin_data(si['data_ref']) if si['data_ref'] >= 0 else None
                sp = nif.parse_skin_partition(si['partition_ref']) if si['partition_ref'] >= 0 else None
                sh['skin_data'] = sd
                if sh['positions'] is None and sp and 'positions' in sp:
                    sh['positions'] = sp['positions']
                # per-vertex weights: prefer NiSkinData (bone-major, float32)
                nvert = sh['num_vertices']
                if sh['positions'] is not None:
                    nvert = max(nvert, len(sh['positions']))
                if sd and sd['has_vertex_weights']:
                    for b in sd['bones']:
                        for vidx, _w in b['weights']:
                            if vidx >= nvert: nvert = vidx + 1
                sh['num_vertices'] = nvert
                wmap = [dict() for _ in range(nvert)]
                if sd and sd['has_vertex_weights']:
                    for bi, b in enumerate(sd['bones']):
                        bn = si['bone_names'][bi]
                        for vidx, w in b['weights']:
                            if w > 0: wmap[vidx][bn] = wmap[vidx].get(bn, 0.0) + w
                    sh['weights_source'] = 'NiSkinData'
                elif sp and 'partitions' in sp:
                    for p in sp['partitions']:
                        vm = p.get('vertex_map') or list(range(p['num_vertices']))
                        for k in range(p['num_vertices']):
                            v = vm[k]
                            ws = p.get('weights'); bs = p.get('bone_indices')
                            if ws and bs:
                                for w, bidx in zip(ws[k], bs[k]):
                                    if w > 0:
                                        bn = si['bone_names'][p['bones'][bidx]]
                                        wmap[v][bn] = wmap[v].get(bn, 0.0) + w
                    sh['weights_source'] = 'NiSkinPartition'
                sh['weight_map'] = wmap
            shapes.append(sh)
    return nif, shapes

if __name__ == '__main__':
    path = sys.argv[1]
    nif, shapes = load_mesh(path)
    print('%s: %s | stream %d | %d blocks' % (path.split('\\')[-1], nif.header_str, nif.stream, nif.num_blocks))
    for sh in shapes:
        pos = sh['positions'] or []
        zs = [p[2] for p in pos]
        print("shape '%s' (%s) verts=%d tris=%d full_prec=%s" % (
            sh['name'], sh['type'], sh['num_vertices'], sh['num_triangles'],
            bool(sh['vertex_flags'] & 0x400)))
        if zs:
            print('  Z range: %.3f .. %.3f' % (min(zs), max(zs)))
        if 'bones' in sh:
            print('  bones: %s' % ', '.join(sh['bones']))
            print('  weights from: %s' % sh.get('weights_source'))
            sd = sh['skin_data']
            if sd:
                gt = sd['global_transform']
                print('  skin global: trans=%s scale=%.4f' % (
                    tuple(round(v, 4) for v in gt['trans']), gt['scale']))
