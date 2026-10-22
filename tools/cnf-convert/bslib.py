# Helpers for the Northern Folk conversion: BodySlide OSD/TRI io, PyNifly loading, nearest-point transfer.
import sys, struct, numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\pynifly-dl\io_scene_nifly")
from pyn.pynifly import NifFile

CBBE = r"C:\1. AUTHORIA\mods\Caliente's Beautiful Bodies Enhancer CBBE -\CalienteTools\BodySlide"
BA3 = r"C:\1. AUTHORIA\mods\CBBE 3BA (3BBB)\CalienteTools\BodySlide"
HIMBO = r"C:\1. AUTHORIA\mods\Highly Improved Male Body Overhaul -HIMBO-\CalienteTools\BodySlide"

def read_osd(path):
    """{target_name: {vert_index: (dx,dy,dz)}}"""
    b = open(path, 'rb').read(); o = 12
    magic, ver, n = struct.unpack('<III', b[:12]); out = {}
    for _ in range(n):
        L = b[o]; name = b[o+1:o+1+L].decode('latin1'); o += 1 + L
        c = struct.unpack('<H', b[o:o+2])[0]; o += 2
        arr = np.frombuffer(b[o:o+c*14], dtype=np.dtype([('i', '<u2'), ('v', '<f4', 3)])); o += c*14
        out[name] = dict(zip(arr['i'].tolist(), arr['v']))
    return out

def write_osd(path, sets):
    """sets: {target_name: (idx_array, delta_array)}"""
    parts = [struct.pack('<III', 0x4F534400, 1, len(sets))]
    for name, (idx, d) in sets.items():
        e = name.encode('latin1'); parts.append(bytes([len(e)]) + e + struct.pack('<H', len(idx)))
        rec = np.zeros(len(idx), dtype=np.dtype([('i', '<u2'), ('v', '<f4', 3)])); rec['i'] = idx; rec['v'] = d
        parts.append(rec.tobytes())
    open(path, 'wb').write(b''.join(parts))

def apply_diff(verts, diff):
    v = np.array(verts, dtype=float).copy()
    for i, d in diff.items(): v[i] += d
    return v

def shape(nif, name=None):
    n = NifFile(nif)
    for s in n.shapes:
        if name is None or s.name == name: return n, s
    raise KeyError(name)

def transfer(src_pts, src_vals, dst_pts, k=8, radius=None, power=2.0):
    """Inverse-distance blend of per-point values from the k nearest source points (Outfit Studio-style proximity)."""
    d, j = knn(src_pts, dst_pts, k)
    w = 1.0 / np.maximum(d, 1e-4) ** power
    if radius is not None: w = np.where(d <= radius, w, w * 1e-6)
    w /= w.sum(1, keepdims=True)
    return np.einsum('nk,nk...->n...', w, src_vals[j]), d[:, 0]

def knn(src, dst, k=8, chunk=2048):
    """Brute-force k nearest neighbours (numpy only): distances and indices, nearest first."""
    src = np.asarray(src, float); dst = np.asarray(dst, float); D = []; J = []
    s2 = (src ** 2).sum(1)
    for a in range(0, len(dst), chunk):
        q = dst[a:a+chunk]; dd = (q ** 2).sum(1)[:, None] - 2 * q @ src.T + s2[None]
        jj = np.argpartition(dd, min(k, len(src)-1), axis=1)[:, :k]
        part = np.take_along_axis(dd, jj, 1); o = np.argsort(part, 1)
        J.append(np.take_along_axis(jj, o, 1)); D.append(np.sqrt(np.maximum(np.take_along_axis(part, o, 1), 0)))
    return np.vstack(D), np.vstack(J)

def world_verts(s):
    """Shape vertices with the shape's own transform applied (CNF shapes carry an offset)."""
    t = s.transform; v = np.array(s.verts, float)
    R = np.array(t.rotation, float).reshape(3, 3) if hasattr(t, 'rotation') else np.eye(3)
    return (v @ R.T) * float(t.scale) + np.array(t.translation, float)

def bind_pose(C, shp, skel_G):
    """Rest-pose positions the game renders: sum over bones of w * (bone global @ skin-to-bone @ v). Handles meshes that
    keep an offset in their skin-to-bone transforms (CNF knitted boots) as well as in the node / global-to-skin."""
    v = np.c_[shp.pos, np.ones(len(shp.pos))]
    out = np.zeros((len(v), 3)); tot = np.zeros(len(v))
    M = {b: skel_G[b] @ C.tb2m(x) for b, x in shp.s2b.items() if b in skel_G}
    for i, w in enumerate(shp.w):
        for b, x in w.items():
            if b in M:
                out[i] += x * (M[b] @ v[i])[:3]; tot[i] += x
    miss = tot < 0.5
    out[~miss] /= tot[~miss, None]
    out[miss] = shp.pos[miss]
    return out, int(miss.sum())


def skeleton_G(C, path=r"C:\1. AUTHORIA\mods\BodySlide and Outfit Studio\CalienteTools\BodySlide\res\skeleton_female_sse.nif"):
    n = NifFile(path); G = {}
    def walk(node, M):
        for ch in node.children if hasattr(node, 'children') else []:
            pass
    for nm, node in n.nodes.items():
        G[nm] = C.tb2m(node.global_transform) if hasattr(node, 'global_transform') else None
    return {k: v for k, v in G.items() if v is not None}
