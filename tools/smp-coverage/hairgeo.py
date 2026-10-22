"""Vertex positions of BSTriShape / BSDynamicTriShape blocks and a coarse 'same hairstyle?' similarity."""
import struct, sys, math
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
import nifrw

VF_FULLPREC = 0x400  # in the vertex-attribute byte of vdesc: positions are float32


def vdesc_info(vdesc):
    size = (vdesc & 0xF) * 4
    attrs = (vdesc >> 44) & 0xFFF
    return size, attrs


def half_to_float(h):
    s = (h >> 15) & 1; e = (h >> 10) & 0x1F; f = h & 0x3FF
    if e == 0:
        v = (f / 1024.0) * 2.0 ** -14
    elif e == 31:
        v = float("inf")
    else:
        v = (1 + f / 1024.0) * 2.0 ** (e - 15)
    return -v if s else v


def positions(doc, si):
    """list of (x, y, z) in the mesh's own space"""
    t, b = doc.blocks[si]
    sh = nifrw.parse_shape_hdr(b)
    nvert, ntri, dsize = sh["nvert"], sh["ntri"], sh["dsize"]
    tail = sh["tail"]
    vsize, attrs = vdesc_info(sh["vdesc"])
    pos = []
    if t == "BSDynamicTriShape":
        # SSE layout after Data Size: [vertex data][triangles] (only if Data Size > 0), Particle Data Size (u32),
        # then Vertex Data Size (u32) and the float4 head-space positions
        o = (dsize if dsize > 0 else 0) + 4
        dyn_size = struct.unpack_from("<I", tail, o)[0]; o += 4
        if dyn_size != nvert * 16:
            raise ValueError("dynamic data size %d != %d" % (dyn_size, nvert * 16))
        for i in range(nvert):
            x, y, z, w = struct.unpack_from("<4f", tail, o + 16 * i)
            pos.append((x, y, z))
        return pos
    if dsize == 0:
        return pos  # skinned static shape keeps its vertices in the NiSkinPartition; not read here
    full = bool(attrs & VF_FULLPREC)
    for i in range(nvert):
        o = i * vsize
        if full:
            x, y, z = struct.unpack_from("<3f", tail, o)
        else:
            hx, hy, hz = struct.unpack_from("<3H", tail, o)
            x, y, z = half_to_float(hx), half_to_float(hy), half_to_float(hz)
        pos.append((x, y, z))
    return pos


HEAD_DEFAULT = (0.0, -1.548, 120.344)


def head_world(doc):
    """world translation of 'NPC Head [Head]' by composing the node chain from the root (rotation-aware)."""
    import nifrw as _n
    nodes = {i: _n.parse_node(b) for i, (t, b) in enumerate(doc.blocks) if t in ("NiNode", "BSFadeNode")}
    parent = {}
    for i, n in nodes.items():
        for c in n["children"]:
            if c in nodes:
                parent[c] = i
    head = None
    for i, n in nodes.items():
        si = n["name"]
        if si < len(doc.strings) and doc.strings[si] == "NPC Head [Head]":
            head = i; break
    if head is None:
        return None
    chain = []
    i = head
    while i is not None:
        chain.append(i); i = parent.get(i)
    chain.reverse()
    # compose world = parent_world * local  (v' = R v + T, row-major 3x3 as stored)
    T = [0.0, 0.0, 0.0]; R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for i in chain:
        n = nodes[i]
        r = n["rot"]; t = n["trans"]; s = n["scale"]
        Rl = [[r[0], r[1], r[2]], [r[3], r[4], r[5]], [r[6], r[7], r[8]]]
        # T' = R*t*s + T ; R' = R*Rl
        tt = [sum(R[a][k] * t[k] for k in range(3)) * s + T[a] for a in range(3)]
        RR = [[sum(R[a][k] * Rl[k][b] for k in range(3)) for b in range(3)] for a in range(3)]
        T, R = tt, RR
    return tuple(T)


def head_space(pos, doc):
    """positions relative to the head: clouds stored in world space (head at z~120) get the head translation removed."""
    if not pos:
        return pos
    zc = sum(p[2] for p in pos) / len(pos)
    if zc < 50:
        return pos
    h = head_world(doc)
    if not h or h[2] < 50:
        h = HEAD_DEFAULT
    return [(x - h[0], y - h[1], z - h[2]) for x, y, z in pos]


def bbox(pos):
    xs = [p[0] for p in pos]; ys = [p[1] for p in pos]; zs = [p[2] for p in pos]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def voxels(pos, cell=2.0):
    return set((int(math.floor(x / cell)), int(math.floor(y / cell)), int(math.floor(z / cell))) for x, y, z in pos)


def similarity(pa, pb, cell=2.0):
    """returns (iou, coverage_a_in_b, coverage_b_in_a, bbox_a, bbox_b): voxel overlap with 1-cell dilation tolerance."""
    va, vb = voxels(pa, cell), voxels(pb, cell)
    def dilate(v):
        out = set()
        for x, y, z in v:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        out.add((x + dx, y + dy, z + dz))
        return out
    da, db = dilate(va), dilate(vb)
    cov_a = len([v for v in va if v in db]) / max(1, len(va))
    cov_b = len([v for v in vb if v in da]) / max(1, len(vb))
    inter = len(va & vb); union = len(va | vb)
    return inter / max(1, union), cov_a, cov_b, bbox(pa), bbox(pb)
