"""Vertical raycast against bridge/dock visual geometry to find deck heights under raised route markers.
Self-calibrates the placed-object rotation convention against the author's own markers."""
import sys, os, struct, math, pickle, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, r'C:/1. AUTHORIA/_tools/magic-pariah-mm-rig')
from nifrw import Doc, parse_shape_hdr

NODE_T = {'NiNode', 'BSFadeNode', 'BSLeafAnimNode', 'BSMultiBoundNode', 'BSOrderedNode', 'BSValueNode', 'BSTreeNode', 'NiSwitchNode', 'BSRangeNode', 'BSDebrisNode', 'BSBlastNode', 'BSDamageStage', 'NiBillboardNode', 'NiLODNode'}
SHAPE_T = {'BSTriShape', 'BSMeshLODTriShape', 'BSSubIndexTriShape', 'BSLODTriShape'}
src = json.load(open('model_src.json'))
MODS = r'C:/1. AUTHORIA/mods/'


def mesh_file(path):
    p = path.lower()
    if p in src['loose']:
        return os.path.join(MODS, src['loose'][p], *p.split('/'))
    for arc, lst in src['bsa'].items():
        if p in lst:
            root = 'bsa/luxvia' if 'Lux' in arc else 'bsa/jksol'
            return os.path.join(root, *p.split('/'))
    return None


def ci(path):
    if os.path.exists(path): return path
    parts = path.replace('\\', '/').split('/'); cur = parts[0] + '/'
    for q in parts[1:]:
        if not q: continue
        names = {n.lower(): n for n in os.listdir(cur)}
        if q.lower() not in names: return None
        cur = os.path.join(cur, names[q.lower()])
    return cur


def node_prefix(b):
    o = 4; ne = struct.unpack_from('<I', b, o)[0]; o += 4 + 4 * ne + 4
    flags = struct.unpack_from('<I', b, o)[0]; o += 4
    t = np.array(struct.unpack_from('<3f', b, o)); o += 12
    r = np.array(struct.unpack_from('<9f', b, o)).reshape(3, 3); o += 36
    s = struct.unpack_from('<f', b, o)[0]; o += 4 + 4
    nc = struct.unpack_from('<I', b, o)[0]; o += 4
    ch = list(struct.unpack_from('<%di' % nc, b, o))
    return flags, t, r, s, ch


_cache = {}
def load_tris(path):
    """local-space triangles (N,3,3) of all visible shapes"""
    if path in _cache: return _cache[path]
    f = mesh_file(path); f = ci(f) if f else None
    if not f: _cache[path] = None; return None
    doc = Doc(f); tris = []
    def visit(i, M, T, S):
        t, b = doc.blocks[i]
        if t in NODE_T:
            flags, lt, lr, ls, ch = node_prefix(b)
            if flags & 1: return
            nM = M @ lr; nT = T + S * (M @ lt); nS = S * ls
            for c in ch:
                if c >= 0: visit(c, nM, nT, nS)
        elif t in SHAPE_T:
            h = parse_shape_hdr(b)
            if h['flags'] & 1 or h['skin'] >= 0 or h['dsize'] == 0: return
            lr = np.array(h['rot']).reshape(3, 3); lt = np.array(h['trans']); ls = h['scale']
            nM = M @ lr; nT = T + S * (M @ lt); nS = S * ls
            vd = h['vdesc']; vs = (vd & 0xF) * 4; attrs = vd >> 44; full = True  # SSE stream 100: positions are always float32
            tail = h['tail']; nv = h['nvert']; nt = h['ntri']
            raw = np.frombuffer(tail[:nv * vs], dtype=np.uint8).reshape(nv, vs)
            if full: pos = raw[:, :12].copy().view('<f4').reshape(nv, 3).astype(np.float64)
            else: pos = raw[:, :6].copy().view('<f2').reshape(nv, 3).astype(np.float64)
            idx = np.frombuffer(tail[nv * vs:nv * vs + nt * 6], dtype='<u2').reshape(nt, 3)
            w = (nS * (pos @ nM.T)) + nT
            tris.append(w[idx])
    visit(0, np.eye(3), np.zeros(3), 1.0)
    out = np.concatenate(tris) if tris else None
    _cache[path] = out; return out


def Rx(a): c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def Ry(a): c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def Rz(a): c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
CONV = {
    'A': lambda x, y, z: Rz(-z) @ Ry(-y) @ Rx(-x),
    'B': lambda x, y, z: Rx(x) @ Ry(y) @ Rz(z),
    'C': lambda x, y, z: Rz(z) @ Ry(y) @ Rx(x),
    'D': lambda x, y, z: Rx(-x) @ Ry(-y) @ Rz(-z),
}


def hits_at(refs, info, px, py, conv, scale_of):
    """all z values where a vertical line at (px,py) crosses bridge geometry of the given refs"""
    zs = []
    for k, v in refs.items():
        base = v[3]
        if base not in info: continue
        tris = load_tris(info[base])
        if tris is None: continue
        pos = np.array(v[2][:3]); rot = v[2][3:]; s = scale_of(v)
        if math.dist(pos[:2], (px, py)) > 3000: continue
        R = CONV[conv](*rot)
        # local query point
        q = (R.T @ (np.array([px, py, 0.0]) - pos)) / s
        d = R.T @ np.array([0, 0, 1.0])
        # ray q + t d against local triangles (Moller-Trumbore, vectorised, both directions)
        v0 = tris[:, 0]; e1 = tris[:, 1] - v0; e2 = tris[:, 2] - v0
        pv = np.cross(d, e2); det = (e1 * pv).sum(1)
        ok = np.abs(det) > 1e-9
        inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
        tv = q - v0; u = (tv * pv).sum(1) * inv
        qv = np.cross(tv, e1); w = (qv @ d) * inv; t = (e2 * qv).sum(1) * inv
        m = ok & (u >= 0) & (w >= 0) & (u + w <= 1)
        for tt in t[m]:
            pl = q + tt * d; wz = (R @ (pl * s) + pos)[2]; zs.append(wz)
    return zs


if __name__ == '__main__':
    na, nf = pickle.load(open('near_refs.pkl', 'rb'))
    info_all, br = pickle.load(open('bases.pkl', 'rb'))
    info = {b: 'meshes/' + i[2].replace('\\', '/').lower() for b, i in br.items() if i[2]}
    hits, markers = pickle.load(open('bridge_hits.pkl', 'rb'))
    def scale_of(v):
        return struct.unpack('<f', v[5][:4])[0] if v[5] else 1.0
    # calibration: NR-author markers (raised) against the author's own world (vanilla + NR)
    nrm = [m for m in markers if m[0].endswith('NR.esp')]
    for conv in CONV:
        good = 0; tot = 0
        for fname, g, w, x, y, z, gr in nrm:
            zs = hits_at({k: v for k, v in na.items() if v[1] == w}, info, x, y, conv, scale_of)
            if not zs: continue
            tot += 1
            if min(abs(z - h) for h in zs) < 40: good += 1
        print('convention', conv, 'markers with a deck hit', tot, 'of', len(nrm), '; within 40 units of the author marker:', good)
