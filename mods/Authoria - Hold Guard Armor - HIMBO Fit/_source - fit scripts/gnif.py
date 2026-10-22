"""Skinned SSE NIF geometry access for the guard-armour fit (read + in-place vertex/skin rewrite).

Built on nifrw.Doc (block-level, byte-exact round trip). Adds:
  - BSTriShape / NiSkinInstance / BSDismemberSkinInstance / NiSkinData / NiSkinPartition decode
  - numpy views of positions, normals, weights, bone indices
  - re-encode of NiSkinPartition (same layout), NiSkinData (weights + bounds), shape bound
"""
import struct, sys
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifrw import Doc, parse_node  # noqa

VF_VERTEX, VF_UV, VF_UV2, VF_NORMAL, VF_TANGENT, VF_COLORS, VF_SKINNED, VF_LAND, VF_EYE = 1, 2, 4, 8, 16, 32, 64, 128, 256
VF_FULLPREC = 1024


def layout(vdesc):
    vsize = (vdesc & 0xF) * 4
    vf = (vdesc >> 44) & 0xFFF
    lay = {}
    extras = (4 if vf & VF_UV else 0) + (4 if vf & VF_NORMAL else 0) + (4 if vf & VF_TANGENT else 0) \
        + (4 if vf & VF_COLORS else 0) + (12 if vf & VF_SKINNED else 0) + (4 if vf & VF_EYE else 0)
    off = 0
    if vf & VF_VERTEX:
        full = (vsize == 16 + extras)
        lay['pos'] = (0, full); off = 16 if full else 8
    if vf & VF_UV:
        lay['uv'] = off; off += 4
    if vf & VF_NORMAL:
        lay['normal'] = off; off += 4
        if vf & VF_TANGENT:
            lay['tangent'] = off; off += 4
    if vf & VF_COLORS:
        lay['colors'] = off; off += 4
    if vf & VF_SKINNED:
        lay['weights'] = off; off += 8
        lay['bidx'] = off; off += 4
    if vf & VF_EYE:
        lay['eye'] = off; off += 4
    assert off == vsize, (off, vsize, hex(vf))
    lay['size'] = vsize; lay['flags'] = vf
    return lay


def xf_from13(f):
    R = np.array(f[0:9], dtype=np.float64).reshape(3, 3)
    T = np.array(f[9:12], dtype=np.float64)
    return R, T, float(f[12])


class Shape:
    pass


class GNif:
    def __init__(self, path):
        self.path = path
        self.doc = Doc(path)
        self.shapes = []
        for i, (t, b) in enumerate(self.doc.blocks):
            if t in ('BSTriShape',):
                self.shapes.append(self._shape(i))

    # -------------------------------------------------- decode
    def _shape(self, i):
        b = self.doc.blocks[i][1]
        s = Shape(); s.block = i
        o = 0
        s.name = self.doc.strings[struct.unpack_from('<I', b, 0)[0]]
        ne = struct.unpack_from('<I', b, 4)[0]; o = 8 + 4 * ne + 4
        s.flags = struct.unpack_from('<I', b, o)[0]; o += 4
        s.trans = np.array(struct.unpack_from('<3f', b, o)); o += 12
        s.rot = np.array(struct.unpack_from('<9f', b, o)).reshape(3, 3); o += 36
        s.scale = struct.unpack_from('<f', b, o)[0]; o += 4
        o += 4
        s.bound_off = o
        s.bound = struct.unpack_from('<4f', b, o); o += 16
        s.skin, s.shader, s.alpha = struct.unpack_from('<iii', b, o); o += 12
        s.vdesc = struct.unpack_from('<Q', b, o)[0]; o += 8
        s.ntri_hdr = struct.unpack_from('<H', b, o)[0]; o += 2
        s.nvert_hdr = struct.unpack_from('<H', b, o)[0]; o += 2
        s.dsize = struct.unpack_from('<I', b, o)[0]; o += 4
        s.vbuf_off = o
        s.bones = []; s.parts_dismember = []
        s.skindata = None; s.part = None
        if s.dsize:
            lay = layout(s.vdesc); s.lay = lay
            n = s.nvert_hdr
            s.vraw = np.frombuffer(bytes(b[o:o + n * lay['size']]), dtype=np.uint8).reshape(n, lay['size']).copy()
            s.tris = np.frombuffer(bytes(b[o + n * lay['size']:o + n * lay['size'] + 6 * s.ntri_hdr]), dtype='<u2').reshape(-1, 3).copy()
        if s.skin >= 0:
            st, sb = self.doc.blocks[s.skin]
            data, part, root, nb = struct.unpack_from('<iiiI', sb, 0)
            s.skin_type = st
            s.bone_refs = list(struct.unpack_from('<%di' % nb, sb, 16))
            s.bones = [self.doc.name_of(r) for r in s.bone_refs]
            if st == 'BSDismemberSkinInstance':
                p = 16 + 4 * nb
                npart = struct.unpack_from('<I', sb, p)[0]; p += 4
                s.parts_dismember = [struct.unpack_from('<HH', sb, p + 4 * k) for k in range(npart)]
            s.skindata_block = data; s.part_block = part
            s.skindata = self._skindata(data) if data >= 0 else None
            if part >= 0:
                self._partition(s, part)
        return s

    def _skindata(self, i):
        b = self.doc.blocks[i][1]
        o = 0
        g = struct.unpack_from('<13f', b, o); o += 52
        nb = struct.unpack_from('<I', b, o)[0]; o += 4
        hvw = b[o]; o += 1
        bones = []
        for _ in range(nb):
            xf = struct.unpack_from('<13f', b, o); o += 52
            bs = struct.unpack_from('<4f', b, o); o += 16
            nv = struct.unpack_from('<H', b, o)[0]; o += 2
            w = None
            if hvw:
                arr = np.frombuffer(bytes(b[o:o + 6 * nv]), dtype=np.dtype([('v', '<u2'), ('w', '<f4')])).copy()
                w = arr; o += 6 * nv
            bones.append(dict(xf=xf, bound=bs, w=w))
        assert o == len(b)
        return dict(glob=g, hvw=hvw, bones=bones)

    def _partition(self, s, i):
        b = self.doc.blocks[i][1]
        o = 0
        np_, dsize, vsize = struct.unpack_from('<III', b, o); o += 12
        vdesc = struct.unpack_from('<Q', b, o)[0]; o += 8
        lay = layout(vdesc); s.lay = lay; s.pvdesc = vdesc
        n = dsize // vsize if vsize else 0
        s.vraw = np.frombuffer(bytes(b[o:o + dsize]), dtype=np.uint8).reshape(n, vsize).copy(); o += dsize
        parts = []
        for _ in range(np_):
            p = {}
            nv, nt, nb, ns, nw = struct.unpack_from('<5H', b, o); o += 10
            p['nw'] = nw
            p['bones'] = list(struct.unpack_from('<%dH' % nb, b, o)); o += 2 * nb
            hvm = b[o]; o += 1
            p['vmap'] = np.frombuffer(bytes(b[o:o + 2 * nv]), dtype='<u2').copy() if hvm else None
            if hvm: o += 2 * nv
            hw = b[o]; o += 1
            p['hw'] = hw
            p['weights'] = np.frombuffer(bytes(b[o:o + 4 * nv * nw]), dtype='<f4').reshape(nv, nw).copy() if hw else None
            if hw: o += 4 * nv * nw
            assert ns == 0, 'strips'
            hf = b[o]; o += 1
            p['hf'] = hf
            p['tris'] = np.frombuffer(bytes(b[o:o + 6 * nt]), dtype='<u2').reshape(nt, 3).copy() if hf else None
            if hf: o += 6 * nt
            hb = b[o]; o += 1
            p['hb'] = hb
            p['bidx'] = np.frombuffer(bytes(b[o:o + nv * nw]), dtype=np.uint8).reshape(nv, nw).copy() if hb else None
            if hb: o += nv * nw
            p['unk'] = struct.unpack_from('<H', b, o)[0]; o += 2
            p['vdesc'] = struct.unpack_from('<Q', b, o)[0]; o += 8
            p['tris_g'] = np.frombuffer(bytes(b[o:o + 6 * nt]), dtype='<u2').reshape(nt, 3).copy(); o += 6 * nt
            parts.append(p)
        assert o == len(b), ('partition size', o, len(b))
        s.parts = parts
        s.tris = np.concatenate([p['tris_g'] for p in parts]) if parts else np.zeros((0, 3), np.uint16)

    # -------------------------------------------------- accessors
    @staticmethod
    def positions(s):
        off, full = s.lay['pos']
        if full:
            return s.vraw[:, off:off + 12].copy().view('<f4').reshape(-1, 3).astype(np.float64)
        return s.vraw[:, off:off + 6].copy().view('<f2').reshape(-1, 3).astype(np.float64)

    @staticmethod
    def set_positions(s, P):
        off, full = s.lay['pos']
        if full:
            s.vraw[:, off:off + 12] = P.astype('<f4').view(np.uint8).reshape(-1, 12)
        else:
            s.vraw[:, off:off + 6] = P.astype('<f2').view(np.uint8).reshape(-1, 6)

    @staticmethod
    def normals(s):
        if 'normal' not in s.lay:
            return None
        o = s.lay['normal']
        n = s.vraw[:, o:o + 3].astype(np.float64) / 255.0 * 2.0 - 1.0
        return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)

    @staticmethod
    def vweights(s):
        o = s.lay['weights']
        w = s.vraw[:, o:o + 8].copy().view('<f2').reshape(-1, 4).astype(np.float64)
        bi = s.vraw[:, s.lay['bidx']:s.lay['bidx'] + 4].copy()
        return w, bi

    def vert_part(self, s):
        """global vertex -> partition index"""
        vp = np.full(len(s.vraw), -1, dtype=np.int64)
        for k, p in enumerate(s.parts):
            vm = p['vmap'] if p['vmap'] is not None else np.arange(len(s.vraw))
            vp[vm] = k
        return vp

    def weight_matrix(self, s):
        """dense (nvert, nbones_shape) weights from the packed per-vertex data.
        SSE packed bone indices are GLOBAL skin-instance indices (verified against NiSkinData
        on multi-partition HIMBO / vanilla bodies); the per-partition arrays use partition-local ones."""
        w, bi = self.vweights(s)
        W = np.zeros((len(s.vraw), len(s.bones)))
        for j in range(4):
            np.add.at(W, (np.arange(len(w)), np.minimum(bi[:, j], len(s.bones) - 1)), w[:, j])
        return W

    def set_weights(self, s, W):
        """write a dense weight matrix back: top-4 per vertex, renormalised, into packed data,
        per-partition arrays (partition-local indices; a bone missing from a partition's list is
        dropped for that partition and the rest renormalised) and NiSkinData per-bone lists."""
        n, nb = W.shape
        if nb < 4:
            W = np.pad(W, ((0, 0), (0, 4 - nb)))
        order = np.argsort(-W, axis=1)[:, :4]
        top = np.take_along_axis(W, order, axis=1)
        top[top < 1e-4] = 0
        top /= np.maximum(top.sum(1, keepdims=True), 1e-9)
        # pad index for zero weights: repeat first bone index (engine convention)
        order = np.where(top > 0, order, order[:, :1])
        o = s.lay['weights']
        s.vraw[:, o:o + 8] = top.astype('<f2').view(np.uint8).reshape(n, 8)
        s.vraw[:, s.lay['bidx']:s.lay['bidx'] + 4] = order.astype(np.uint8)
        Wq = np.zeros((n, max(nb, 4)))
        tq = top.astype('<f2').astype(np.float64)
        for j in range(4):
            np.add.at(Wq, (np.arange(n), order[:, j]), tq[:, j])
        assert np.abs(Wq[:, nb:]).sum() == 0
        Wq = Wq[:, :nb]
        for p in s.parts:
            vm = p['vmap'] if p['vmap'] is not None else np.arange(n)
            pb = np.array(p['bones'])
            loc = {b: i for i, b in enumerate(pb)}
            sub = Wq[vm][:, pb] if len(pb) else np.zeros((len(vm), 0))
            nw = p['nw']
            if sub.shape[1] < nw:
                sub = np.pad(sub, ((0, 0), (0, nw - sub.shape[1])))
            o2 = np.argsort(-sub, axis=1)[:, :nw]
            t2 = np.take_along_axis(sub, o2, axis=1)
            t2 /= np.maximum(t2.sum(1, keepdims=True), 1e-9)
            if p['hw']:
                p['weights'] = t2.astype('<f4')
            if p['hb']:
                bi2 = np.where(t2 > 0, o2, o2[:, :1])
                assert (bi2 < max(len(pb), 1)).all()
                p['bidx'] = bi2.astype(np.uint8)
        if s.skindata and s.skindata['hvw']:
            dt = np.dtype([('v', '<u2'), ('w', '<f4')])
            for k, bd in enumerate(s.skindata['bones']):
                idx = np.where(Wq[:, k] > 0)[0]
                arr = np.zeros(len(idx), dtype=dt); arr['v'] = idx; arr['w'] = Wq[idx, k]
                bd['w'] = arr
        return Wq

    def bind_world(self, s):
        """bone name -> (R,T) world bind derived from NiSkinData (inverse of skin->bone)."""
        out = {}
        if not s.skindata:
            return out
        gR, gT, gS = xf_from13(s.skindata['glob'])
        for name, bd in zip(s.bones, s.skindata['bones']):
            R, T, sc = xf_from13(bd['xf'])
            # bone-space = R*v + T  (v in skin space). bone world = inverse
            Ri = R.T; Ti = -Ri @ T
            out[name] = (Ri, Ti)
        return out

    def node_world(self):
        out = {}
        def rec(i, R0, T0, S0):
            t, b = self.doc.blocks[i]
            if t != 'NiNode':
                return
            n = parse_node(b)
            R = np.array(n['rot']).reshape(3, 3); T = np.array(n['trans'])
            Rw = R0 @ R; Tw = R0 @ (T * S0) + T0; Sw = S0 * n['scale']
            out[self.doc.strings[n['name']]] = (Rw, Tw)
            for c in n['children']:
                if c >= 0:
                    rec(c, Rw, Tw, Sw)
        rec(self.doc.roots[0], np.eye(3), np.zeros(3), 1.0)
        return out

    # -------------------------------------------------- encode
    def write_partition(self, s):
        b = self.doc.blocks[s.part_block][1]
        out = bytearray()
        out += struct.pack('<III', len(s.parts), s.vraw.size, s.lay['size'])
        out += struct.pack('<Q', s.pvdesc)
        out += s.vraw.tobytes()
        for p in s.parts:
            nv = len(p['vmap']) if p['vmap'] is not None else len(s.vraw)
            nt = len(p['tris_g'])
            out += struct.pack('<5H', nv, nt, len(p['bones']), 0, p['nw'])
            out += struct.pack('<%dH' % len(p['bones']), *p['bones'])
            out += bytes([1 if p['vmap'] is not None else 0])
            if p['vmap'] is not None:
                out += p['vmap'].astype('<u2').tobytes()
            out += bytes([p['hw']])
            if p['hw']:
                out += p['weights'].astype('<f4').tobytes()
            out += bytes([p['hf']])
            if p['hf']:
                out += p['tris'].astype('<u2').tobytes()
            out += bytes([p['hb']])
            if p['hb']:
                out += p['bidx'].astype(np.uint8).tobytes()
            out += struct.pack('<H', p['unk'])
            out += struct.pack('<Q', p['vdesc'])
            out += p['tris_g'].astype('<u2').tobytes()
        self.doc.blocks[s.part_block][1] = out

    def write_skindata(self, s):
        sd = s.skindata
        out = bytearray(struct.pack('<13f', *sd['glob']))
        out += struct.pack('<I', len(sd['bones'])) + bytes([sd['hvw']])
        for bd in sd['bones']:
            out += struct.pack('<13f', *bd['xf'])
            out += struct.pack('<4f', *bd['bound'])
            if sd['hvw']:
                out += struct.pack('<H', len(bd['w'])) + bd['w'].tobytes()
            else:
                out += struct.pack('<H', 0)
        self.doc.blocks[s.skindata_block][1] = out

    def write_bound(self, s, center, radius):
        b = self.doc.blocks[s.block][1]
        struct.pack_into('<4f', b, s.bound_off, float(center[0]), float(center[1]), float(center[2]), float(radius))

    def save(self, path):
        self.doc.save(path)
