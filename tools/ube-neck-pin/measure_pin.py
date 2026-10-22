"""Measure the UBE neck pin state of a nif: per skinned shape that carries the Head bone,
report Head-bone weight (read from the VBUF, the renderer's source) on verts at/below the
seam ring (Z<=112.5) and in the ramp band (112.5..116.25).
Pinned profile  = Head weight 0 at Z<=112.5, smoothstep to full by 116.25.
Unpinned (raw BodySlide) = Head weight 0.1..0.3 on the ring.
Read-only. Usage: python measure_pin.py <nif> [<nif> ...]"""
import os, sys, struct
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'from-bodypin3'))
from nifparse import Nif, load_mesh
from weld_taper import layout
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ZLO, ZHI = 112.5, 116.25

def walk_partition(nif, part_ref):
    r = nif.block_reader(part_ref)
    np_ = r.u32()
    dsize = r.u32(); vsize = r.u32(); desc = r.u64()
    vbuf_off = r.o if dsize else None
    r.o += dsize
    parts = []
    for _ in range(np_):
        p = {}
        nv = r.u16(); nt = r.u16(); nb = r.u16(); ns = r.u16(); nwpv = r.u16()
        p['nwpv'] = nwpv
        p['bones'] = [r.u16() for _ in range(nb)]
        if r.u8(): p['vertex_map'] = [r.u16() for _ in range(nv)]
        else: p['vertex_map'] = list(range(nv))
        if r.u8(): p['w_off'] = r.o; r.o += 4 * nwpv * nv
        else: p['w_off'] = None
        slens = [r.u16() for _ in range(ns)]
        if r.u8():
            if ns:
                for l in slens: r.o += 2 * l
            else: r.o += 6 * nt
        if r.u8(): p['bi_off'] = r.o; r.o += nwpv * nv
        else: p['bi_off'] = None
        r.u16(); r.u64()
        r.o += 6 * nt
        parts.append(p)
    assert r.o - nif.block_offsets[part_ref] == nif.block_sizes[part_ref]
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'dsize': dsize, 'desc': desc, 'parts': parts}

def h2f(hv):
    s = (hv >> 15) & 1; e = (hv >> 10) & 0x1F; m = hv & 0x3FF
    v = (m / 1024.0 * 2 ** -14) if e == 0 else ((1 + m / 1024.0) * 2 ** (e - 15) if e < 31 else 0.0)
    return -v if s else v

def skin_offset(desc, dsize, vsize, dynamic):
    if not dsize: return None
    _vs, full = layout(desc)
    vflags = (desc >> 44) & 0xFFF
    if not (vflags & 0x40): return None
    off = 0 if dynamic else (16 if full else 8)
    if vflags & 0x2: off += 4
    if vflags & 0x8: off += 4
    if vflags & 0x10: off += 4
    if vflags & 0x20: off += 4
    return off

def read_vbuf(data, pl, dso, vi):
    base = pl['vbuf_off'] + vi * pl['vsize'] + dso
    ws = [h2f(struct.unpack_from('<H', data, base + 2 * k)[0]) for k in range(4)]
    bi = [data[base + 8 + k] for k in range(4)]
    return ws, bi

def measure(path):
    nif = Nif(path)
    _, shapes = load_mesh(path)
    pool = list(shapes)
    print('\n=== %s' % path)
    for i in range(nif.num_blocks):
        if nif.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
        dynamic = nif.btype(i) == 'BSDynamicTriShape'
        s2 = nif.parse_shape(i)
        if s2['skin_ref'] < 0: continue
        si = nif.parse_skin_instance(s2['skin_ref'])
        pl = walk_partition(nif, si['partition_ref'])
        nverts = pl['dsize'] // pl['vsize'] if pl['vsize'] else 0
        sh = next((s for s in pool if s['name'] == s2['name'] and s.get('positions') is not None
                   and len(s['positions']) == nverts), None)
        if sh is None: continue
        pool.remove(sh)
        inst = si['bone_names']
        nm = s2['name']
        if 'NPC Head [Head]' not in inst:
            print("  shape '%s' verts=%d: no Head bone (not neck-relevant)" % (nm, nverts)); continue
        dso = skin_offset(pl['desc'], pl['dsize'], pl['vsize'], dynamic)
        pos = np.array(sh['positions'], np.float32)
        parts = pl['parts']
        vert_parts = {}
        for pidx, p in enumerate(parts):
            for lk, gv in enumerate(p['vertex_map']):
                vert_parts.setdefault(gv, []).append((pidx, lk))
        if all(len(p['bones']) == len(inst) and p['bones'] == list(range(len(inst))) for p in parts):
            conv = 'same'
        elif len(parts) == 1:
            conv = 'local'
        else:
            conv = 'global'
        def head_w(v, convention):
            ws, bi = read_vbuf(nif.data, pl, dso, v)
            occ = vert_parts.get(v)
            if convention == 'local' and occ:
                names = [inst[b] for b in parts[occ[0][0]]['bones']]
            else:
                names = inst
            return sum(w for w, b in zip(ws, bi) if w > 0 and b < len(names) and names[b] == 'NPC Head [Head]')
        # sum sanity
        samp = list(range(0, nverts, max(1, nverts // 200)))[:200]
        bad = sum(1 for v in samp if not (0.95 < sum(read_vbuf(nif.data, pl, dso, v)[0]) < 1.05))
        ring = np.where(pos[:, 2] <= ZLO)[0]
        band = np.where((pos[:, 2] > ZLO) & (pos[:, 2] < ZHI))[0]
        hw_ring = np.array([head_w(int(v), conv) for v in ring]) if len(ring) else np.zeros(0)
        hw_band = np.array([head_w(int(v), conv) for v in band]) if len(band) else np.zeros(0)
        # the ring proper: topmost body verts (within 4 units of the shape's max Z) -- where head meets body
        zmax = float(pos[:, 2].max())
        top = np.where(pos[:, 2] >= zmax - 4.0)[0]
        hw_top = np.array([head_w(int(v), conv) for v in top]) if len(top) else np.zeros(0)
        print("  shape '%s' verts=%d parts=%d conv=%s sum-gate bad=%d/%d Zmax=%.2f" % (nm, nverts, len(parts), conv, bad, len(samp), zmax))
        print("    Z<=112.5 : %5d verts | Head>0.01 on %5d | max Head %.3f | mean Head %.3f" % (
            len(ring), int((hw_ring > 0.01).sum()), float(hw_ring.max()) if len(hw_ring) else 0, float(hw_ring.mean()) if len(hw_ring) else 0))
        print("    112.5-116.25: %5d verts | Head>0.01 on %5d | max Head %.3f" % (
            len(band), int((hw_band > 0.01).sum()), float(hw_band.max()) if len(hw_band) else 0))
        print("    top 4 units (Z>=%.2f): %4d verts | Head>0.01 on %4d | max Head %.3f | mean Head %.3f" % (
            zmax - 4.0, len(top), int((hw_top > 0.01).sum()), float(hw_top.max()) if len(hw_top) else 0, float(hw_top.mean()) if len(hw_top) else 0))
        verdict = 'PINNED' if (len(hw_ring) and (hw_ring > 0.01).sum() == 0) else ('UNPINNED' if len(hw_ring) else 'n/a (no verts at/below 112.5)')
        print("    VERDICT: %s" % verdict)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        try: measure(p)
        except Exception as e: print('  ERROR %s: %s' % (p, e))
