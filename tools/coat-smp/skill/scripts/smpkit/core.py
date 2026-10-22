"""smpkit core: NIF in/out (PyNifly), geometry, weights, SMP XML snippets and BodySlide OSD slider data.

Extracted from working per-armour build scripts; the algorithms are unchanged. PyNifly must be importable as `pyn`
(add its io_scene_nifly folder to sys.path BEFORE importing this module - smpkit.setup_pynifly does that).
Units are Skyrim units (1 unit ~ 1.43 cm); z is up, the actor faces +y, +x is the actor's right
(NPC L Thigh sits at x ~ -6.6). Angles round the body: atan2(x, y) in degrees, 0 = front, +90 = the actor's right."""
import os, re, struct
from ctypes import c_char
from collections import defaultdict, Counter
import numpy as np
from pyn.pynifly import NifFile, NiStringExtraData, SkyPartition, nifly
from pyn.nifdefs import PynBufferTypes, NiShapeBuf
from pyn.structs import TransformBuf
from pyn.nifconstants import NO_SHADER_REF

# ==================== NIF loading: a plain-data snapshot of every shape ====================
class Shape:
    """Plain-data snapshot of a NiShape (bones via node ids, not the truncating name buffer)."""

    def __init__(self, nif, s):
        self.nif, self.s, self.name = nif, s, s.name
        self.pos = np.array(s.verts, dtype=float)
        self.tris = np.array(s.tris, dtype=int)
        self.uv = np.array(s.uvs, dtype=float)
        self.norm = np.array(s.normals, dtype=float) if s.normals else None
        self.tex = slots(nif, s)
        self.bones = [nif.read_node(id=i).name for i in s.bone_ids]
        self.w = [dict() for _ in range(len(self.pos))]
        for bi, nm in enumerate(self.bones):
            for v, wt in s._bone_weights(bi):
                self.w[v][nm] = self.w[v].get(nm, 0.0) + wt
        self.parts = list(s.partitions)
        self.ptris = list(s.partition_tris)
        self.s2b = {}
        for nm in dict.fromkeys(self.bones):
            xf = s.get_shape_skin_to_bone(nm)
            if xf is not None:
                self.s2b[nm] = xf

def load(path):
    n = NifFile(path)
    return n, [Shape(n, s) for s in n.shapes]
def slots(nif, shape):
    out = []
    for i in range(9):
        buf = (c_char * 500)()
        nifly.getShaderTextureSlot(nif._handle, shape._handle, i, buf, 500)
        out.append(buf.value.decode('utf-8'))
    return out

# ==================== nearest-surface queries, transforms, weight caps ====================
def knn(src, q, k):
    s = np.asarray(src, np.float32); ss = (s * s).sum(1)
    k = min(k, len(s))
    idx = np.empty((len(q), k), np.int64); dist = np.empty((len(q), k), np.float32)
    for a in range(0, len(q), 1024):
        x = np.asarray(q[a:a + 1024], np.float32)
        d2 = (x * x).sum(1)[:, None] + ss[None, :] - 2 * x @ s.T
        np.maximum(d2, 0, out=d2)
        part = np.argpartition(d2, k - 1, axis=1)[:, :k] if k < len(s) else np.tile(np.arange(len(s)), (len(x), 1))
        pd = np.take_along_axis(d2, part, 1)
        order = np.argsort(pd, axis=1)
        idx[a:a + 1024] = np.take_along_axis(part, order, 1)
        dist[a:a + 1024] = np.sqrt(np.take_along_axis(pd, order, 1))
    return idx, dist
def closest_on_tris(p, A, B, C):
    """Ericson's closest point on triangle, vectorised over triangles. -> points (M,3), barycentrics (M,3)"""
    ab, ac, ap = B - A, C - A, p - A
    d1, d2 = (ab * ap).sum(1), (ac * ap).sum(1)
    bp = p - B; d3, d4 = (ab * bp).sum(1), (ac * bp).sum(1)
    cp = p - C; d5, d6 = (ab * cp).sum(1), (ac * cp).sum(1)
    vc = d1 * d4 - d3 * d2; vb = d5 * d2 - d1 * d6; va = d3 * d6 - d5 * d4
    with np.errstate(divide='ignore', invalid='ignore'):
        den = va + vb + vc
        v = np.where(np.abs(den) > 1e-20, vb / den, 1 / 3); w = np.where(np.abs(den) > 1e-20, vc / den, 1 / 3)
        bary = np.stack([1 - v - w, v, w], 1)
        # edges and vertices, applied from the last test to the first so the earliest test wins
        t = np.where(np.abs((d4 - d3) + (d5 - d6)) > 1e-20, (d4 - d3) / ((d4 - d3) + (d5 - d6)), 0)
        m = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0); bary[m] = np.stack([0 * t, 1 - t, t], 1)[m]
        t = np.where(np.abs(d2 - d6) > 1e-20, d2 / (d2 - d6), 0)
        m = (vb <= 0) & (d2 >= 0) & (d6 <= 0); bary[m] = np.stack([1 - t, 0 * t, t], 1)[m]
        m = (d6 >= 0) & (d5 <= d6); bary[m] = [0, 0, 1]
        t = np.where(np.abs(d1 - d3) > 1e-20, d1 / (d1 - d3), 0)
        m = (vc <= 0) & (d1 >= 0) & (d3 <= 0); bary[m] = np.stack([1 - t, t, 0 * t], 1)[m]
        m = (d3 >= 0) & (d4 <= d3); bary[m] = [0, 1, 0]
        m = (d1 <= 0) & (d2 <= 0); bary[m] = [1, 0, 0]
    pts = A * bary[:, :1] + B * bary[:, 1:2] + C * bary[:, 2:]
    return pts, bary
def closest_on_tris_batched(p, A, B, C):
    """closest_on_tris over a (N, K, 3) table of triangles per point (p is (N, 3)); the same arithmetic, one axis deeper"""
    p = p[:, None, :]
    ab, ac, ap = B - A, C - A, p - A
    d1, d2 = (ab * ap).sum(2), (ac * ap).sum(2)
    bp = p - B; d3, d4 = (ab * bp).sum(2), (ac * bp).sum(2)
    cp = p - C; d5, d6 = (ab * cp).sum(2), (ac * cp).sum(2)
    vc = d1 * d4 - d3 * d2; vb = d5 * d2 - d1 * d6; va = d3 * d6 - d5 * d4
    with np.errstate(divide='ignore', invalid='ignore'):
        den = va + vb + vc
        v = np.where(np.abs(den) > 1e-20, vb / den, 1 / 3); w = np.where(np.abs(den) > 1e-20, vc / den, 1 / 3)
        bary = np.stack([1 - v - w, v, w], -1)
        t = np.where(np.abs((d4 - d3) + (d5 - d6)) > 1e-20, (d4 - d3) / ((d4 - d3) + (d5 - d6)), 0)
        m = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0); bary[m] = np.stack([0 * t, 1 - t, t], -1)[m]
        t = np.where(np.abs(d2 - d6) > 1e-20, d2 / (d2 - d6), 0)
        m = (vb <= 0) & (d2 >= 0) & (d6 <= 0); bary[m] = np.stack([1 - t, 0 * t, t], -1)[m]
        m = (d6 >= 0) & (d5 <= d6); bary[m] = [0, 0, 1]
        t = np.where(np.abs(d1 - d3) > 1e-20, d1 / (d1 - d3), 0)
        m = (vc <= 0) & (d1 >= 0) & (d3 <= 0); bary[m] = np.stack([1 - t, t, 0 * t], -1)[m]
        m = (d3 >= 0) & (d4 <= d3); bary[m] = [0, 1, 0]
        m = (d1 <= 0) & (d2 <= 0); bary[m] = [1, 0, 0]
    pts = A * bary[..., :1] + B * bary[..., 1:2] + C * bary[..., 2:]
    return pts, bary
class Surface:
    """Triangle soup over several shapes, with nearest-point queries."""

    def __init__(self, parts):
        """parts: list of (name, pos (N,3), tris (M,3))"""
        V, F, owner, local, names = [], [], [], [], []
        off = 0
        for si, (nm, pos, tris) in enumerate(parts):
            V.append(pos); F.append(np.asarray(tris) + off); owner.append(np.full(len(pos), si)); local.append(np.arange(len(pos)))
            names.append(nm); off += len(pos)
        self.V = np.vstack(V); self.F = np.vstack(F); self.owner = np.concatenate(owner); self.local = np.concatenate(local)
        self.names = names
        self.vt = defaultdict(list)
        for ti, t in enumerate(self.F):
            for v in t:
                self.vt[int(v)].append(ti)

    def _query_loop(self, P, k=6):
        idx, _ = knn(self.V, P, k)
        tri = np.zeros(len(P), np.int64); bary = np.zeros((len(P), 3)); dist = np.zeros(len(P)); pt = np.zeros((len(P), 3))
        for i, p in enumerate(P):
            cand = sorted({t for j in idx[i] for t in self.vt[int(j)]})
            if not cand:
                tri[i] = -1; dist[i] = np.inf; continue
            T = np.array(cand)
            q, b = closest_on_tris(p, self.V[self.F[T, 0]], self.V[self.F[T, 1]], self.V[self.F[T, 2]])
            dd = np.linalg.norm(q - p, axis=1); m = int(np.argmin(dd))
            tri[i], bary[i], dist[i], pt[i] = T[m], b[m], dd[m], q[m]
        return tri, bary, dist, pt

    def query(self, P, k=6):
        """-> tri index (N,), barycentrics (N,3), distance (N,), closest point (N,3)
        2026-10-13: batched - the same candidate triangles per point (those of its k nearest vertices, sorted) in one padded table and
        ONE vectorised closest-point pass; identical results to the per-point loop (proved bit-for-bit on the Heavy skirt), 3x faster."""
        if os.environ.get('SMPKIT_QUERY_LOOP'): return self._query_loop(P, k)      # the pre-2026-10-13 loop, for regression runs
        P = np.asarray(P, float)
        tri = np.full(len(P), -1, np.int64); bary = np.zeros((len(P), 3)); dist = np.full(len(P), np.inf); pt = np.zeros((len(P), 3))
        if len(P) == 0 or len(self.F) == 0: return tri, bary, dist, pt
        idx, _ = knn(self.V, P, k)
        vt = self.vt; cands = [sorted({t for j in idx[i] for t in vt[int(j)]}) for i in range(len(P))]
        K = max((len(c) for c in cands), default=0)
        if K == 0: return tri, bary, dist, pt
        T = np.zeros((len(P), K), np.int64); valid = np.zeros((len(P), K), bool)
        for i, c in enumerate(cands):
            if not c: continue
            T[i, :len(c)] = c; T[i, len(c):] = c[0]; valid[i, :len(c)] = True
        q, b = closest_on_tris_batched(P, self.V[self.F[T, 0]], self.V[self.F[T, 1]], self.V[self.F[T, 2]])
        dd = np.linalg.norm(q - P[:, None, :], axis=2); dd[~valid] = np.inf
        m = dd.argmin(1); ar = np.arange(len(P)); ok = valid.any(1)
        tri[ok] = T[ar, m][ok]; bary[ok] = b[ar, m][ok]; dist[ok] = dd[ar, m][ok]; pt[ok] = q[ar, m][ok]
        return tri, bary, dist, pt
def tb2m(tb):
    m = np.eye(4); m[:3, :3] = np.array([list(r) for r in tb.rotation]) * tb.scale; m[:3, 3] = list(tb.translation); return m
def m2tb(m):
    tb = TransformBuf(); s = np.cbrt(np.linalg.det(m[:3, :3])); r = m[:3, :3] / s
    tb.store(m[:3, 3].tolist(), r.tolist(), [s, s, s]); return tb
def to_world(shapes):
    """Bring every skinned shape into bind-pose (global) space: some 3BA projects store a shape around the origin with a
    global-to-skin translation (Silent Mist cloaks, Freja steel skirt...). Positions, normals and skin-to-bone binds are
    rewritten so the whole port works - and writes - in one space with identity transforms."""
    for s in shapes:
        if getattr(s, '_world', False):
            continue
        s._world = True
        if not s.s.has_global_to_skin:
            continue
        G = tb2m(s.s.global_to_skin)
        if np.allclose(G, np.eye(4), atol=1e-5):
            continue
        if not np.allclose(G[:3, :3], np.eye(3), atol=1e-4):
            # slider data would need rotating/scaling too; none of the meshes here do this, so refuse rather than guess
            raise RuntimeError(f'shape {s.name!r}: global-to-skin has rotation/scale')
        Gi = np.linalg.inv(G)
        s.pos = s.pos @ Gi[:3, :3].T + Gi[:3, 3]
        s.s2b = {nm: m2tb(tb2m(xf) @ G) for nm, xf in s.s2b.items()}
        s.g2s_offset = G[:3, 3].copy()
    return shapes
def top4(w):
    items = sorted(((b, x) for b, x in w.items() if x > 1e-5), key=lambda t: -t[1])[:4]
    tot = sum(x for _, x in items)
    return {b: x / tot for b, x in items} if tot > 0 else {}
def part_ids(t, T):
    """per-triangle BSDismember partition ids; a shape that had no skin (so no partitions) gets the mesh's main one"""
    if len(t.ptris) == len(t.tris) and len(t.tris):
        return np.array([t.parts[p].id if p < len(t.parts) else p for p in t.ptris])
    main = Counter(x.parts[p].id for x in T if x.ptris for p in x.ptris if p < len(x.parts)).most_common(1)
    return np.full(len(t.tris), main[0][0] if main else 32)

# ==================== NIF writing: shapes, skin, custom bone nodes ====================
MAXB = 80          # bones per shape: the engine's skin partition limit as used throughout (keep well under it)
class Writer:
    def __init__(self, src_nif, out_path):
        self.out = NifFile()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        self.out.initialize('SKYRIMSE', out_path, root_type='NiNode', root_name=src_nif.rootName)
        self.out.root.flags = src_nif.root.flags
        self.custom_G = {}
        self.parent = {}

    def node(self, nm, G, parent):
        if nm in self.out.nodes:
            return
        if parent is None:
            self.out.add_node(nm, m2tb(G), self.out.root)
        else:
            self.out.add_node(nm, m2tb(np.linalg.inv(self.custom_G.get(parent, self.skel_G[parent])) @ G), self.out.nodes[parent])

    def emit(self, name, pos, uv, norm, tris, flags, partids, weights, s2b, shader_from=None, colors=None, nif_src=None, double_sided=False):
        """double_sided (2026-10-10, Realistic Armor v18): also set SLSF2 Double_Sided (0x10) on the copied shader - for a layer
        whose inside the author never drew because another layer was welded inside it (separated outer panels showed
        see-through insides in game). Default False = the shader is copied unchanged, as before."""
        out = self.out
        props = NiShapeBuf(); props.bufType = PynBufferTypes.BSTriShapeBufType
        if shader_from is None:
            props.shaderPropertyID = NO_SHADER_REF
        sh = out.createShapeFromData(name, [tuple(p) for p in pos], [tuple(t) for t in tris], [tuple(u) for u in uv],
                                     [tuple(n) for n in norm] if norm is not None else None, props=props, parent=out.root)
        sh.flags = flags
        if colors:
            sh.set_colors(colors)
        if shader_from is not None:
            ssh = shader_from.s.shader
            dst = sh.shader.properties
            keep = {f: getattr(dst, f) for f in ('textureSetID', 'nameID', 'controllerID', 'rootMaterialNameID', 'extraDataCount')}
            buf = ssh.properties.copy()
            for f, v in keep.items():
                setattr(buf, f, v)
            if double_sided:
                buf.Shader_Flags_2 |= 0x10
            sh.shader._properties = buf
            sh.shader.name = ssh.name or ''
            for i, tx in enumerate(shader_from.tex):
                if tx:
                    nifly.setShaderTextureSlot(out._handle, sh._handle, i, tx.encode('utf-8'))
            if shader_from.s.has_alpha_property:
                sh.has_alpha_property = True
                src_ap = shader_from.s.alpha_property.properties
                ap = sh.alpha_property.properties
                ap.flags = src_ap.flags; ap.threshold = src_ap.threshold
                sh.save_alpha_property()
            sh.save_shader_attributes()
        sh.skin()
        sh.set_global_to_skin(TransformBuf())
        used = sorted({b for w in weights for b in w})
        if len(used) > MAXB:
            raise RuntimeError(f'{name}: {len(used)} bones > {MAXB}')
        for bn in [b for b in used if b not in self.custom_G]:
            sh.add_bone(bn, m2tb(self.skel_G[bn]), None)
        for bn in sorted([b for b in used if b in self.custom_G], key=lambda n: (int(n.split()[-1]) if n.split()[-1].isdigit() else 0, n)):   # a mesh may carry nodes without a number (SkirtBBone03)
            par = self.parent[bn]
            if par not in self.out.nodes:
                raise RuntimeError(f'{name}: parent node {par} of {bn} not written yet')
            G = self.custom_G[bn]
            sh.add_bone(bn, m2tb(np.linalg.inv(self.custom_G.get(par, self.skel_G.get(par))) @ G), par)
        for bn in used:
            if bn in s2b and bn not in self.custom_G:
                xf = s2b[bn]                                   # the shape's own bind for skeleton bones
            else:
                xf = m2tb(np.linalg.inv(self.custom_G.get(bn, self.skel_G.get(bn))))
            sh.set_skin_to_bone_xform(bn, xf)
        per_bone = defaultdict(list)
        for vi, w in enumerate(weights):
            for bn, x in w.items():
                per_bone[bn].append((vi, x))
        for bn in used:
            sh.setShapeWeights(bn, per_bone[bn])
        pids = sorted(set(partids))
        sh.set_partitions([SkyPartition(part_id=p, flags=257, namedict=out.dict) for p in pids], list(partids))
        return len(used)

# ==================== skeleton (body) bones vs physics bones ====================
SKEL = set()


def set_skeleton(path):
    """load the node names of a skeleton nif (BodySlide ships CalienteTools/BodySlide/res/skeleton_female_sse.nif): a bone
    of the armour that is in the skeleton is a body bone, everything else is a physics bone"""
    SKEL.clear()
    if path:
        if not os.path.exists(path): raise FileNotFoundError(f'skeleton nif not found: {path}')
        SKEL.update(NifFile(path).nodes)
def is_skel(b):
    return b in SKEL or b in ('NPC', 'Scene Root', 'NPC Root [Root]') or b.startswith(('NPC ', 'CME ', 'MOV ', 'x_', 'Weapon', 'Shield', 'Quiver', 'Bow', 'Ankle', 'Camera',
                                      'AnimObject', 'Tail')) or re.match(r'^Skirt[FBLR]Bone\d+$', b) is not None

# ==================== subdivision; per-axis spring constraint default ====================
def subdivide_c(pos, uv, nrm, ow, col, tris, sel, levels, mids=None):
    """midpoint subdivision (each selected triangle -> 4) carrying UVs, normals, weights and vertex colours; mids (a list) collects the two parent
    vertices of every new point in creation order (BodySlide slider data for a new point = the mean of its parents')"""
    pos, uv, nrm, ow = [p for p in pos], [u for u in uv], [n for n in nrm], [dict(w) for w in ow]
    col = [np.asarray(c, float) for c in col] if col is not None else None
    keep = [(tuple(t), i) for i, t in enumerate(tris) if not sel[i]]
    cur = [(tuple(t), i) for i, t in enumerate(tris) if sel[i]]
    for _ in range(levels):
        mid = {}

        def m(a, b):
            k = (min(a, b), max(a, b))
            if k not in mid:
                pos.append((pos[a] + pos[b]) / 2); uv.append((uv[a] + uv[b]) / 2)
                n = nrm[a] + nrm[b]; nn = np.linalg.norm(n); nrm.append(n / nn if nn > 1e-9 else nrm[a])
                if col is not None: col.append((col[a] + col[b]) / 2)
                w = defaultdict(float)
                for bn, x in ow[a].items(): w[bn] += x / 2
                for bn, x in ow[b].items(): w[bn] += x / 2
                ow.append(dict(w)); mid[k] = len(pos) - 1
                if mids is not None: mids.append(k)
            return mid[k]
        nxt = []
        for (a, b, c), par in cur:
            ab, bc, ca = m(a, b), m(b, c), m(c, a)
            nxt += [((a, ab, ca), par), ((ab, b, bc), par), ((ca, bc, c), par), ((ab, bc, ca), par)]
        cur = nxt
    allt = keep + cur
    return (np.array(pos), np.array(uv), np.array(nrm), ow, (np.array(col) if col is not None else None),
            np.array([t for t, _ in allt]), np.array([p for _, p in allt]), len(keep))
def chain_default_xyz(lim, comment):
    """chain_default with a stiffness per axis (the springs only hold the in/out swing)"""
    L = chain_default(dict(lim, astiff=0), comment)
    k = lim['stiff']
    return [f'\t\t<angularStiffness x="{k[0]}" y="{k[1]}" z="{k[2]}"/>' if l.strip().startswith('<angularStiffness') else l for l in L]

# ==================== rig maths, leg follow, SMP XML snippets ====================
PELV, LTHG, RTHG, LCLF, RCLF = 'NPC Pelvis [Pelv]', 'NPC L Thigh [LThg]', 'NPC R Thigh [RThg]', 'NPC L Calf [LClf]', 'NPC R Calf [RClf]'
LR_W = 60.0   # degrees over which cloth between the legs (front and back centre) blends from one thigh to the other
              # (a narrow blend tore a step into the cloth there whenever the legs stood apart)
MAIL_NEAR, MAIL_FAR = 1.0, 5.0   # mail closer than NEAR to the trousers moves exactly like them; beyond FAR it swings fully
def wrap(d): return (np.asarray(d) + 180.0) % 360.0 - 180.0
def smooth01(x):
    x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)
def row_bracket(zs, z):
    if z >= zs[0]: return [(0, 1.0)]
    if z <= zs[-1]: return [(len(zs) - 1, 1.0)]
    for r in range(len(zs) - 1):
        if zs[r] >= z >= zs[r + 1]:
            t = (zs[r] - z) / (zs[r] - zs[r + 1]); return [(r, 1 - t), (r + 1, t)]
def lin_bracket(cs, u):
    """piecewise-linear weights over sorted positions cs (clamped at the ends)"""
    if u <= cs[0]: return [(0, 1.0)]
    if u >= cs[-1]: return [(len(cs) - 1, 1.0)]
    for i in range(len(cs) - 1):
        if cs[i] <= u <= cs[i + 1]:
            t = (u - cs[i]) / (cs[i + 1] - cs[i]); return [(i, 1 - t), (i + 1, t)]
def frame(phi):
    """chain frame at angle phi (deg, 0 = front +y, + = +x = the actor's right): X along the skirt, Y outward, Z up"""
    c, s = np.cos(np.radians(phi)), np.sin(np.radians(phi))
    R = np.eye(3); R[:, 0] = [c, -s, 0]; R[:, 1] = [s, c, 0]; R[:, 2] = [0, 0, 1]
    return R
def welded_components(pos, tris):
    """connected pieces, joining vertices that share an index OR sit at the same position (UV seams split vertices)"""
    par = list(range(len(pos)))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for t in tris:
        for a, b in ((t[0], t[1]), (t[1], t[2])):
            ra, rb = f(int(a)), f(int(b))
            if ra != rb: par[ra] = rb
    key = {}
    for i, p in enumerate(np.round(pos, 3)):
        k = tuple(p)
        if k in key:
            ra, rb = f(i), f(key[k])
            if ra != rb: par[ra] = rb
        else:
            key[k] = i
    R = np.array([f(i) for i in range(len(pos))])
    order = [r for r, _ in Counter(R).most_common()]
    lab = np.zeros(len(pos), int)
    for k, r in enumerate(order): lab[R == r] = k
    return lab
def smooth_lr(legw, ang, rig):
    """the trousers' own weights switch from one thigh to the other within a unit at the front and back centre; cloth
    hanging there (joined above the slits) then tore into a step whenever the legs stood apart. Blend the thighs (with their
    calves) smoothly across LR_W degrees instead, so the cloth between the legs follows both"""
    u_f = float(wrap(ang)); u_b = float(wrap(ang - 180.0))
    if abs(u_f) < LR_W / 2: sL = float(smooth01(0.5 - u_f / LR_W))          # front: negative angles = left leg
    elif abs(u_b) < LR_W / 2: sL = float(smooth01(0.5 + u_b / LR_W))        # back: positive (past 180) = left leg
    else: return legw
    Lb = {b: x for b, x in legw.items() if b in (LTHG, LCLF)}; Rb = {b: x for b, x in legw.items() if b in (RTHG, RCLF)}
    Lt, Rt = sum(Lb.values()), sum(Rb.values()); T = Lt + Rt
    if T < 1e-6: return legw
    out = defaultdict(float, {b: x for b, x in legw.items() if b not in (LTHG, LCLF, RTHG, RCLF)})
    for b, x in (Lb.items() if Lt > 1e-6 else [(LTHG, 1.0)]): out[b] += T * sL * x / (Lt if Lt > 1e-6 else 1.0)
    for b, x in (Rb.items() if Rt > 1e-6 else [(RTHG, 1.0)]): out[b] += T * (1 - sL) * x / (Rt if Rt > 1e-6 else 1.0)
    return dict(out)
def trouser_follow(tr, pts):
    """for each point: weights that move it the way the trousers around it move, and its signed gap to the trousers.
    Close to the trousers: the trousers' own weights at the nearest surface point; further away: a sharp inverse-distance
    blend of the trouser vertices around it (follows the nearest leg; between the legs it mixes both thighs, no seam)"""
    tri, bary, dist, cp = Surface([('tr', tr.pos, tr.tris)]).query(pts, k=8)
    N = tr.norm / (np.linalg.norm(tr.norm, axis=1, keepdims=True) + 1e-12)
    nrm = (N[tr.tris[tri]] * bary[:, :, None]).sum(1); nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
    gap = ((pts - cp) * nrm).sum(1)
    nn, nd = knn(tr.pos, pts, 10)
    out = []
    for k, (t, b) in enumerate(zip(tri, bary)):
        near = defaultdict(float)
        for vi, bb in zip(tr.tris[t], b):
            for bn, x in tr.w[vi].items(): near[bn] += bb * x
        idw = defaultdict(float); ws = 1.0 / (nd[k].astype(float) ** 4 + 0.5); ws /= ws.sum()
        for vi, a in zip(nn[k], ws):
            for bn, x in tr.w[int(vi)].items(): idw[bn] += a * x
        f = float(smooth01((gap[k] - MAIL_NEAR) / (MAIL_FAR - MAIL_NEAR)))
        w = defaultdict(float)
        for bn, x in near.items(): w[bn] += (1 - f) * x
        for bn, x in idw.items(): w[bn] += f * x
        w = top4(w)
        if not w: raise RuntimeError(f'mail point {pts[k]} got no weights')
        out.append(w)
    return out, gap
def bone_default(d, comment):
    return [f'\t<!-- {comment} -->', '\t<bone-default>', f'\t\t<mass>{d["mass"]}</mass>', f'\t\t<inertia x="{d["inertia"]}" y="{d["inertia"]}" z="{d["inertia"]}"/>',
            '\t\t<centerOfMassTransform>', '\t\t\t<basis x="0" y="0" z="0" w="1"/>', '\t\t\t<origin x="0" y="0" z="0"/>', '\t\t</centerOfMassTransform>',
            f'\t\t<linearDamping>{d["lin"]}</linearDamping>', f'\t\t<angularDamping>{d["ang"]}</angularDamping>',
            f'\t\t<friction>{d["friction"]}</friction>', f'\t\t<rollingFriction>{d.get("rolling", 0)}</rollingFriction>', '\t\t<restitution>0</restitution>',
            f'\t\t<gravity-factor>{d.get("gravity", 1)}</gravity-factor>', f'\t\t<wind-factor>{d["wind"]}</wind-factor>', '\t</bone-default>']
def chain_default(lim, comment):
    lo, hi, l, k = lim['lo'], lim['hi'], lim['lin'], lim.get('astiff', 0)
    return ['', f'\t<!-- {comment} -->', '\t<generic-constraint-default>',
            '\t\t<frameInB>', '\t\t\t<basis x="0" y="0" z="0" w="1"/>', '\t\t\t<origin x="0" y="0" z="0"/>', '\t\t</frameInB>',
            '\t\t<useLinearReferenceFrameA>false</useLinearReferenceFrameA>',
            f'\t\t<linearLowerLimit x="{-l}" y="{-l}" z="{-l}"/>', f'\t\t<linearUpperLimit x="{l}" y="{l}" z="{l}"/>',
            f'\t\t<angularLowerLimit x="{lo[0]}" y="{lo[1]}" z="{lo[2]}"/>', f'\t\t<angularUpperLimit x="{hi[0]}" y="{hi[1]}" z="{hi[2]}"/>',
            '\t\t<linearStiffness x="0" y="0" z="0"/>', f'\t\t<angularStiffness x="{k}" y="{k}" z="{k}"/>',
            '\t\t<linearDamping x="0" y="0" z="0"/>', '\t\t<angularDamping x="0" y="0" z="0"/>',
            '\t\t<linearEquilibrium x="0" y="0" z="0"/>', '\t\t<angularEquilibrium x="{}" y="{}" z="{}"/>'.format(*lim.get('eq', (0, 0, 0))),   # eq: the springs' rest point (hair: a little outward, RA TAIL_EQ)
            '\t</generic-constraint-default>']
def link_default(lin, ang, comment, lstiff=0, astiff=0):
    return ['', f'\t<!-- {comment} -->', '\t<generic-constraint-default>',
            '\t\t<frameInLerp>', '\t\t\t<translationLerp>0.5</translationLerp>', '\t\t\t<rotationLerp>0.5</rotationLerp>', '\t\t</frameInLerp>',
            '\t\t<useLinearReferenceFrameA>false</useLinearReferenceFrameA>',
            f'\t\t<linearLowerLimit x="{-lin}" y="{-lin}" z="{-lin}"/>', f'\t\t<linearUpperLimit x="{lin}" y="{lin}" z="{lin}"/>',
            f'\t\t<angularLowerLimit x="{-ang}" y="{-ang}" z="{-ang}"/>', f'\t\t<angularUpperLimit x="{ang}" y="{ang}" z="{ang}"/>',
            f'\t\t<linearStiffness x="{lstiff}" y="{lstiff}" z="{lstiff}"/>', f'\t\t<angularStiffness x="{astiff}" y="{astiff}" z="{astiff}"/>',
            '\t\t<linearDamping x="0" y="0" z="0"/>', '\t\t<angularDamping x="0" y="0" z="0"/>',
            '\t\t<linearEquilibrium x="0" y="0" z="0"/>', '\t\t<angularEquilibrium x="0" y="0" z="0"/>',
            '\t</generic-constraint-default>']

# ==================== skirt geometry ====================
def axis_centre(P, tris):
    top = P[:, 2] > P[:, 2].max() - 4.0
    return float(P[top, 0].mean()), float(P[top, 1].mean())
def outer_mask(P, tris, cx, cy):
    """triangles facing away from the skirt axis (the outer wall); the rest is the lining"""
    fn = np.cross(P[tris[:, 1]] - P[tris[:, 0]], P[tris[:, 2]] - P[tris[:, 0]]); cc = P[tris].mean(1)
    return (fn[:, :2] * (cc[:, :2] - [cx, cy])).sum(1) > 0
def surface_samples(P, tris, n=6):
    """points spread over the triangles (so a coarse mesh covers its surface evenly): barycentric grid of n steps"""
    bc = np.array([(i / n, j / n, 1 - (i + j) / n) for i in range(n + 1) for j in range(n + 1 - i)])
    return np.einsum('kb,tbd->tkd', bc, P[tris]).reshape(-1, 3)

# ==================== normals, collider pull-in, SMP XML collision shape ====================
def vertex_normals(P, tris):
    fn = np.cross(P[tris[:, 1]] - P[tris[:, 0]], P[tris[:, 2]] - P[tris[:, 0]])
    vn = np.zeros_like(P)
    for j in range(3): np.add.at(vn, tris[:, j], fn)
    return vn / (np.linalg.norm(vn, axis=1, keepdims=True) + 1e-12)
def outward_fraction(P, tris, axes):
    fn = np.cross(P[tris[:, 1]] - P[tris[:, 0]], P[tris[:, 2]] - P[tris[:, 0]]); c = P[tris].mean(1); out = 0
    for t in range(len(tris)):
        pl = axes['L' if c[t, 0] < 0 else 'R']          # the left leg is on -x
        best, bd = None, 1e9
        for a, b in ((pl[0], pl[1]), (pl[1], pl[2])):
            ab = b - a; s = np.clip((c[t] - a) @ ab / (ab @ ab), 0, 1); q = a + s * ab; d = np.linalg.norm(c[t] - q)
            if d < bd: best, bd = q, d
        out += (fn[t] @ (c[t] - best)) > 0
    return out / len(tris)
def spread(off, tris, n=2, f=0.6):
    nbr = defaultdict(set)
    for t in tris:
        for a in t: nbr[int(a)].update(int(b) for b in t)
    for _ in range(n):
        off = np.array([max(off[i], f * max((off[j] for j in nbr[i]), default=0.0)) for i in range(len(off))])
    return off
def pull_in(P, tris, pts, clear, max_in, lat=2.5):
    """offsets along -normal (winding normals, outward) so every point lying over the surface stays `clear` off it"""
    N = vertex_normals(P, tris); off = np.zeros(len(P))
    if len(pts):
        for i in range(len(P)):
            v = pts - P[i]; d = np.linalg.norm(v, axis=1); m = d < lat + clear + 3.0
            if not m.any(): continue
            v = v[m]; s = v @ N[i]; la = np.linalg.norm(v - np.outer(s, N[i]), axis=1)
            mm = (la < lat) & (s > -max_in)
            if mm.any(): off[i] = min(max_in, max(0.0, clear - float(s[mm].min())))
    off = spread(off, tris)
    return P - off[:, None] * N, off
def shape(kind, name, tag, margin, can=(), no=(), pen=None, shared='private'):
    # shared: 'private' = this file only; 'public' = any file on this (or another) skeleton - FSMP's hdtSMP64.xsd; a shape that must meet
    # a shape from ANOTHER nif (a cuirass collider for a helmet) is public on both sides and the two whitelist each other's tag
    L = [f'\t<{kind} name="{name}">', f'\t\t<margin>{margin}</margin>']
    if pen is not None: L.append(f'\t\t<penetration>{pen}</penetration>')
    L += [f'\t\t<shared>{shared}</shared>'] + [f'\t\t<tag>{t_}</tag>' for t_ in ((tag,) if isinstance(tag, str) else tag)]   # a tuple = several tags (a helmet tail: the cuirasses' tag + its own)
    L += [f'\t\t<can-collide-with-tag>{c}</can-collide-with-tag>' for c in can] + [f'\t\t<no-collide-with-tag>{c}</no-collide-with-tag>' for c in no] + [f'\t</{kind}>']
    return L
BAG_DEF = dict(mass=0.6, inertia=4.0, lin=0.5, ang=0.6, friction=0.2, wind=0.05)       # the author's 0.6 bag, damped to settle
BAG_LIM = dict(lo=(-0.7, -0.45, -0.3), hi=(0.05, 0.45, 0.3), lin=0.1, astiff=25)

# ==================== BodySlide slider data ====================
def slider_data(ss, entries, src_names, nverts):
    """{slider: {target shape: dense (n, 3) diff array}} for the source shapes"""
    E = dict(entries); out = {}
    for sl in ss.findall('Slider'):
        for d in sl.findall('Data'):
            tgt = d.get('target')
            if tgt not in src_names: continue
            key = d.text.split('\\', 1)[1]
            if key not in E: raise RuntimeError(f'slider {sl.get("name")}: entry {key} missing from the osd')
            arr = out.setdefault(sl.get('name'), {}).setdefault(tgt, np.zeros((nverts[tgt], 3)))
            for i, x in E[key].items():
                if i >= nverts[tgt]: raise RuntimeError(f'{key}: vertex {i} >= {nverts[tgt]}')
                arr[i] += x
    return out

# ==================== BodySlide .osd files ====================
def read_osd(path):
    """-> (version, [(name, {vertex_index: (dx, dy, dz)})])  in file order."""
    with open(path, 'rb') as f:
        b = f.read()
    if b[:4] not in (b'OSD\x00', b'\x00DSO'):
        raise ValueError(f'not an OSD file: {path}')
    ver, n = struct.unpack_from('<II', b, 4)
    o, out = 12, []
    for _ in range(n):
        ln = b[o]; o += 1
        name = b[o:o + ln].decode('utf-8'); o += ln
        cnt = struct.unpack_from('<H', b, o)[0]; o += 2
        arr = np.frombuffer(b, dtype=np.dtype([('i', '<u2'), ('d', '<f4', 3)]), count=cnt, offset=o); o += 14 * cnt
        out.append((name, {int(r['i']): tuple(float(x) for x in r['d']) for r in arr}))
    return b[:4], ver, out
def write_osd(path, magic, ver, entries):
    parts = [magic, struct.pack('<II', ver, len(entries))]
    for name, diffs in entries:
        nb = name.encode('utf-8')
        if len(nb) > 255:
            raise ValueError(f'osd entry name too long: {name}')
        if len(diffs) > 65535:
            raise ValueError(f'too many diffs in {name}')
        parts.append(struct.pack('<B', len(nb)) + nb + struct.pack('<H', len(diffs)))
        for i in sorted(diffs):
            dx, dy, dz = diffs[i]
            parts.append(struct.pack('<H3f', i, dx, dy, dz))
    with open(path, 'wb') as f:
        f.write(b''.join(parts))
