"""Graft the Meandering Meadowlark skirt physics rig onto the Magic Pariah skirt.

Input : Magic Pariah Skirt HDT.nif (BodySlide ShapeData) + Meandering Meadowlark Dress 3BA.nif
Output: a new Magic Pariah Skirt HDT.nif with
  - MM's 12-column skirt bone chain (rows 1-4) under NPC Pelvis
  - MM's CollThigh / CollCalves leg collision proxies (partition 49)
  - MM's invisible skirt collision proxy, cut to the MP hem, renamed MMSkirtProxy
  - Skirt Lower / Skirt Upper re-skinned to the MM chain (weights transferred
    from MM's own skirt layers by nearest-neighbour)
  - the old MP chain (sk_a..h), the old 'Cube' collider and the duplicate
    'UniButt' body removed
Vertex positions, UVs, normals, tangents and triangle order of the visible
shapes are untouched, so the BodySlide .osd slider data stays valid.
"""
import sys, struct, re, os
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\ube-neck-pin\from-bodypin3")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifparse import Nif, load_mesh
from nifrw import (Doc, rebuild, reachable, parse_node, build_node, parse_shape_hdr,
                   build_shape, parse_dismember, build_dismember)

SP = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8d6204d3-5065-49b7-8bd8-da1d0615990c\scratchpad"
MM_NIF = SP + r"\mm\Meandering Meadowlark 3BA\CalienteTools\BodySlide\ShapeData\Meandering Meadowlark Dress 3BA\Meandering Meadowlark Dress 3BA.nif"
MP_NIF = SP + r"\mp\Magic Pariah\CalienteTools\BodySlide\ShapeData\Magic Pariah Skirt HDT\Magic Pariah Skirt HDT.nif"
OUT_DIR = SP + r"\out"
OUT_NIF = OUT_DIR + r"\Magic Pariah Skirt HDT.nif"

PROXY_SRC = 'Draft Skirt weight test'
PROXY_NAME = 'MMSkirtProxy'
COLL_SHAPES = ['CollThigh', 'CollCalves']
RESKIN = ['Skirt Lower', 'Skirt Upper']
DELETE_SHAPES = ['Cube', 'UniButt']
SOURCE_SHAPES = ['skirt upper retop', 'skirt outer retop cut', 'skirt outer cuff retop',
                 'skirt belt retop', 'skirt mid', PROXY_SRC]
KEEP_ROWS = 4
PROXY_CUT_Z = 36.0          # drop proxy triangles entirely below this height
BODY_PART = 49              # MP skirt ARMA slot
KNN_K = 8
MIN_W = 0.02

COLUMNS = ['front', 'frontA.l', 'frontA.r', 'frontB.l', 'frontB.r', 'side.l', 'side.r',
           'backB.l', 'backB.r', 'backA.l', 'backA.r', 'back']


def sk_name(col, row):
    if '.' in col:
        base, side = col.split('.')
        return 'sk_%s%d.%s' % (base, row, side)
    return 'sk_%s%d' % (col, row)


def sk_row(name):
    m = re.match(r'sk_[A-Za-z]+(\d)(\.[lr])?$', name)
    return int(m.group(1)) if m else None


PRUNE = {sk_name(c, r): sk_name(c, KEEP_ROWS) for c in COLUMNS for r in range(KEEP_ROWS + 1, 7)}
KEEP_SK = {sk_name(c, r) for c in COLUMNS for r in range(1, KEEP_ROWS + 1)}


# ----------------------------------------------------------------- helpers
def node_index(doc):
    return {doc.name_of(i): i for i, (t, _) in enumerate(doc.blocks) if t == 'NiNode'}


def shape_index(doc):
    return {doc.name_of(i): i for i, (t, _) in enumerate(doc.blocks) if t == 'BSTriShape'}


def bone_table(nif, shapes):
    tbl = {}
    for sh in shapes:
        if sh['skin_ref'] < 0 or not sh.get('skin_data'):
            continue
        si = nif.parse_skin_instance(sh['skin_ref'])
        for bn, b in zip(si['bone_names'], sh['skin_data']['bones']):
            xf = (tuple(b['transform']['rot']), tuple(b['transform']['trans']), b['transform']['scale'])
            if bn in tbl:
                old = tbl[bn]
                diff = max(abs(a - c) for a, c in zip(old[0] + old[1] + (old[2],), xf[0] + xf[1] + (xf[2],)))
                assert diff < 1e-3, ('bone transform disagreement inside one file', bn, diff)
            else:
                tbl[bn] = xf
    return tbl


def world_transforms(doc):
    """name -> (R 3x3, T) world transform of every NiNode (composition R@v+T)."""
    out = {}
    def rec(i, R0, T0):
        n = parse_node(doc.blocks[i][1])
        R = np.array(n['rot']).reshape(3, 3); T = np.array(n['trans'])
        Rw = R0 @ R; Tw = R0 @ T + T0
        out[doc.strings[n['name']]] = (Rw, Tw)
        for c in n['children']:
            if c >= 0 and doc.blocks[c][0] == 'NiNode':
                rec(c, Rw, Tw)
    rec(doc.roots[0], np.eye(3), np.zeros(3))
    return out


def skin_offset(vdesc):
    vsize = (vdesc & 0xF) * 4
    vflags = (vdesc >> 44) & 0xFFF
    has_vtx = vflags & 0x1; has_uv = vflags & 0x2; has_nrm = vflags & 0x8
    has_tan = vflags & 0x10; has_col = vflags & 0x20; has_skin = vflags & 0x40; has_eye = vflags & 0x100
    assert has_skin, 'vertex layout has no skin data'
    extras = (4 if has_uv else 0) + (4 if has_nrm else 0) + (4 if has_tan else 0) + (4 if has_col else 0) + 12 + (4 if has_eye else 0)
    if vsize == 16 + extras:
        pos = 16
    elif vsize == 8 + extras:
        pos = 8
    else:
        raise ValueError('cannot infer position precision')
    off = pos + (4 if has_uv else 0) + (4 if has_nrm else 0) + (4 if has_tan else 0) + (4 if has_col else 0)
    return vsize, off


def partition_raw(doc, part_idx):
    raw = doc.blocks[part_idx][1]
    np_, dsize, vsize = struct.unpack_from('<III', raw, 0)
    desc = struct.unpack_from('<Q', raw, 12)[0]
    assert np_ == 1, 'expected a single partition'
    vbuf = bytes(raw[20:20 + dsize])
    o = 20 + dsize
    nv, nt, nb, ns, nwpv = struct.unpack_from('<HHHHH', raw, o); o += 10
    o += 2 * nb
    assert ns == 0
    has_vm = raw[o]; o += 1
    if has_vm: o += 2 * nv
    has_w = raw[o]; o += 1
    if has_w: o += 4 * nwpv * nv
    has_f = raw[o]; o += 1
    tris = [struct.unpack_from('<HHH', raw, o + 6 * k) for k in range(nt)]
    return dsize, vsize, desc, vbuf, tris


def top4(wd):
    items = [(b, w) for b, w in wd.items() if w > 0]
    items.sort(key=lambda kv: -kv[1])
    items = items[:4]
    s = sum(w for _, w in items)
    return [(b, w / s) for b, w in items]


def build_skin(doc, node_idx, bone_xf, positions, vbuf, vdesc, tris, wmap, body_part):
    """Return (dismember_bytes_fn, skindata_bytes, partition_bytes). The dismember
    block needs the data/partition block indices, so it is returned as a function."""
    nvert = len(positions)
    assert len(wmap) == nvert
    per_vertex = [top4(w) for w in wmap]
    bones = []
    for pv in per_vertex:
        for b, _ in pv:
            if b not in bones:
                bones.append(b)
    assert len(bones) <= 255, 'too many bones for one partition'
    for b in bones:
        assert b in node_idx, 'no node for bone %s' % b
        assert b in bone_xf, 'no bind transform for bone %s' % b
    bidx = {b: k for k, b in enumerate(bones)}
    P = np.array(positions, dtype=np.float64)
    # ---- NiSkinData
    sd = bytearray()
    sd += struct.pack('<9f', 1, 0, 0, 0, 1, 0, 0, 0, 1) + struct.pack('<3f', 0, 0, 0) + struct.pack('<f', 1.0)
    sd += struct.pack('<I', len(bones)) + bytes([1])
    per_bone = [[] for _ in bones]
    for v, pv in enumerate(per_vertex):
        for b, w in pv:
            per_bone[bidx[b]].append((v, w))
    for k, b in enumerate(bones):
        rot, trans, scale = bone_xf[b]
        R = np.array(rot).reshape(3, 3); T = np.array(trans)
        vs = np.array([v for v, _ in per_bone[k]])
        X = (R @ P[vs].T).T * scale + T
        lo, hi = X.min(0), X.max(0); c = (lo + hi) / 2
        rad = float(np.linalg.norm(X - c, axis=1).max())
        sd += struct.pack('<9f', *rot) + struct.pack('<3f', *trans) + struct.pack('<f', scale)
        sd += struct.pack('<3f', *c) + struct.pack('<f', rad)
        sd += struct.pack('<H', len(per_bone[k]))
        for v, w in per_bone[k]:
            sd += struct.pack('<Hf', v, w)
    # ---- NiSkinPartition
    vsize, soff = skin_offset(vdesc)
    assert len(vbuf) == nvert * vsize, (len(vbuf), nvert, vsize)
    vb = bytearray(vbuf)
    w32 = np.zeros((nvert, 4), dtype=np.float32)
    bi = np.zeros((nvert, 4), dtype=np.uint8)
    for v, pv in enumerate(per_vertex):
        for s, (b, w) in enumerate(pv):
            w32[v, s] = w; bi[v, s] = bidx[b]
    w16 = w32.astype('<f2')
    for v in range(nvert):
        o = v * vsize + soff
        vb[o:o + 8] = w16[v].tobytes()
        vb[o + 8:o + 12] = bi[v].tobytes()
    sp = bytearray()
    sp += struct.pack('<III', 1, len(vb), vsize) + struct.pack('<Q', vdesc) + vb
    sp += struct.pack('<HHHHH', nvert, len(tris), len(bones), 0, 4)
    sp += struct.pack('<%dH' % len(bones), *range(len(bones)))
    sp += bytes([1]) + struct.pack('<%dH' % nvert, *range(nvert))
    sp += bytes([1]) + w32.astype('<f4').tobytes()
    tri_bytes = b''.join(struct.pack('<HHH', *t) for t in tris)
    sp += bytes([1]) + tri_bytes
    sp += bytes([1]) + bi.tobytes()
    sp += struct.pack('<H', 0) + struct.pack('<Q', vdesc) + tri_bytes

    def dismember(data_idx, part_idx):
        return build_dismember(dict(data=data_idx, part=part_idx, root=0,
                                    bones=[node_idx[b] for b in bones], parts=[(257, body_part)]))
    return dismember, bytes(sd), bytes(sp), bones, per_vertex


def knn_transfer(src_pos, src_w, tgt_pos, k=KNN_K):
    src = np.array(src_pos, dtype=np.float64); tgt = np.array(tgt_pos, dtype=np.float64)
    out = []; nearest = []
    for s in range(0, len(tgt), 256):
        T = tgt[s:s + 256]
        d2 = ((T[:, None, :] - src[None, :, :]) ** 2).sum(-1)
        idx = np.argpartition(d2, k, axis=1)[:, :k]
        for r in range(len(T)):
            ids = idx[r]; d = np.sqrt(d2[r, ids])
            nearest.append(float(d.min()))
            inv = 1.0 / (d + 0.05) ** 2
            acc = {}
            for j, wgt in zip(ids, inv):
                for b, w in src_w[j].items():
                    acc[b] = acc.get(b, 0.0) + w * wgt
            tot = sum(acc.values())
            out.append({b: w / tot for b, w in acc.items()})
    return out, np.array(nearest)


def prune_rows(wd):
    acc = {}
    for b, w in wd.items():
        b2 = PRUNE.get(b, b)
        acc[b2] = acc.get(b2, 0.0) + w
    acc = {b: w for b, w in acc.items() if w >= MIN_W}
    tot = sum(acc.values())
    return {b: w / tot for b, w in acc.items()}


# ----------------------------------------------------------------- main
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    P = Doc(MP_NIF); M = Doc(MM_NIF)
    nifP, shP = load_mesh(MP_NIF); nifM, shM = load_mesh(MM_NIF)
    byP = {s['name']: s for s in shP}; byM = {s['name']: s for s in shM}

    # bind transforms: MP's own first, MM fills the chain bones; common bones must agree
    xfP = bone_table(nifP, shP); xfM = bone_table(nifM, shM)
    worst = 0.0
    for b in set(xfP) & set(xfM):
        a, c = xfP[b], xfM[b]
        worst = max(worst, max(abs(x - y) for x, y in zip(a[0] + a[1] + (a[2],), c[0] + c[1] + (c[2],))))
    print('common bind bones %d, worst disagreement %.5f' % (len(set(xfP) & set(xfM)), worst))
    assert worst < 1e-3, 'MM and MP were not skinned on the same skeleton'
    bone_xf = dict(xfM); bone_xf.update(xfP)

    nodesP = node_index(P); nodesM = node_index(M); shapesP = shape_index(P); shapesM = shape_index(M)
    worldM = world_transforms(M)
    root = P.roots[0]

    # ---- 1. detach MP's old chain from the pelvis, delete Cube/UniButt from the root
    pelvis = nodesP['NPC Pelvis [Pelv]']
    pn = parse_node(P.blocks[pelvis][1])
    old_chain = [c for c in pn['children'] if c >= 0 and (P.name_of(c) or '').startswith('sk_')]
    pn['children'] = [c for c in pn['children'] if c not in old_chain]
    print('removed %d old chain roots from NPC Pelvis' % len(old_chain))
    rn = parse_node(P.blocks[root][1])
    dels = [shapesP[n] for n in DELETE_SHAPES]
    rn['children'] = [c for c in rn['children'] if c not in dels]
    print('removed shapes from root:', DELETE_SHAPES)

    # ---- 2. copy MM chain rows 1..KEEP_ROWS under NPC Pelvis
    def copy_chain(mi):
        n = parse_node(M.blocks[mi][1]); name = M.strings[n['name']]
        row = sk_row(name)
        assert row is not None, name
        new = dict(n); new['name'] = P.sidx(name); new['extra'] = []; new['ctrl'] = -1
        new['coll'] = -1; new['effects'] = []
        kids = []
        if row < KEEP_ROWS:
            for c in n['children']:
                if c >= 0 and M.blocks[c][0] == 'NiNode':
                    kids.append(copy_chain(c))
        new['children'] = kids
        P.blocks.append(['NiNode', build_node(new)])
        return len(P.blocks) - 1
    mpelvis = parse_node(M.blocks[nodesM['NPC Pelvis [Pelv]']][1])
    roots1 = [c for c in mpelvis['children'] if (M.name_of(c) or '').startswith('sk_')]
    assert len(roots1) == 12, len(roots1)
    for c in roots1:
        pn['children'].append(copy_chain(c))
    P.blocks[pelvis][1] = build_node(pn)
    nodesP = node_index(P)
    added = sorted(n for n in nodesP if n in KEEP_SK)
    assert len(added) == 12 * KEEP_ROWS, len(added)
    print('added %d chain nodes' % len(added))

    # ---- helper: make sure every bone we need has a node in P (flat, MM world transform)
    def ensure_node(name):
        if name in nodesP:
            return nodesP[name]
        R, T = worldM[name]
        nd = dict(name=P.sidx(name), extra=[], ctrl=-1, flags=0x8000E, trans=tuple(T),
                  rot=tuple(R.reshape(-1)), scale=1.0, coll=-1, children=[], effects=[])
        P.blocks.append(['NiNode', build_node(nd)])
        nodesP[name] = len(P.blocks) - 1
        rn['children'].append(nodesP[name])
        print('  created flat node for', name)
        return nodesP[name]

    # ---- 3. copy CollThigh / CollCalves verbatim (bones re-pointed, partition -> 49)
    new_shape_refs = []
    for name in COLL_SHAPES:
        mi = shapesM[name]
        h = parse_shape_hdr(M.blocks[mi][1])
        dm = parse_dismember(M.blocks[h['skin']][1])
        bone_names = [M.name_of(b) for b in dm['bones']]
        for b in bone_names:
            ensure_node(b)
        data_b = bytes(M.blocks[dm['data']][1]); part_b = bytes(M.blocks[dm['part']][1])
        P.blocks.append(['NiSkinData', bytearray(data_b)]); di = len(P.blocks) - 1
        P.blocks.append(['NiSkinPartition', bytearray(part_b)]); pi = len(P.blocks) - 1
        nd = dict(data=di, part=pi, root=root, bones=[nodesP[b] for b in bone_names],
                  parts=[(f, BODY_PART) for f, _ in dm['parts']])
        P.blocks.append(['BSDismemberSkinInstance', build_dismember(nd)]); si = len(P.blocks) - 1
        h2 = dict(h); h2['name'] = P.sidx(name); h2['extra'] = []; h2['ctrl'] = -1; h2['coll'] = -1
        h2['skin'] = si; h2['shader'] = -1; h2['alpha'] = -1
        P.blocks.append(['BSTriShape', build_shape(h2)]); shi = len(P.blocks) - 1
        new_shape_refs.append(shi)
        print('copied %s: %d bones, partitions %s' % (name, len(bone_names), nd['parts']))

    # ---- 4. the invisible skirt proxy: rows 5/6 folded into 4, cut below the hem
    src = byM[PROXY_SRC]
    mi = shapesM[PROXY_SRC]
    h = parse_shape_hdr(M.blocks[mi][1])
    dm = parse_dismember(M.blocks[h['skin']][1])
    dsize, vsize, vdesc, vbuf, tris = partition_raw(M, dm['part'])
    pos = src['positions']
    keep_tris = [t for t in tris if max(pos[v][2] for v in t) >= PROXY_CUT_Z]
    wmap = [prune_rows(w) for w in src['weight_map']]
    for w in wmap:
        for b in w:
            ensure_node(b)
    dis_fn, sd_b, sp_b, bones, pv = build_skin(P, nodesP, bone_xf, pos, vbuf, vdesc, keep_tris, wmap, BODY_PART)
    P.blocks.append(['NiSkinData', bytearray(sd_b)]); di = len(P.blocks) - 1
    P.blocks.append(['NiSkinPartition', bytearray(sp_b)]); pi = len(P.blocks) - 1
    P.blocks.append(['BSDismemberSkinInstance', dis_fn(di, pi)]); si = len(P.blocks) - 1
    h2 = dict(h); h2['name'] = P.sidx(PROXY_NAME); h2['extra'] = []; h2['ctrl'] = -1; h2['coll'] = -1
    h2['skin'] = si; h2['shader'] = -1; h2['alpha'] = -1
    P.blocks.append(['BSTriShape', build_shape(h2)]); shi = len(P.blocks) - 1
    new_shape_refs.append(shi)
    print('proxy: %d verts, tris %d -> %d, bones %d' % (len(pos), len(tris), len(keep_tris), len(bones)))

    # ---- 5. re-skin the visible MP skirt layers from MM's skirt layers
    src_pos = []; src_w = []
    for name in SOURCE_SHAPES:
        s = byM[name]
        src_pos += s['positions']; src_w += [prune_rows(w) for w in s['weight_map']]
    print('kNN source cloud: %d verts from %s' % (len(src_pos), SOURCE_SHAPES))
    for name in RESKIN:
        s = byP[name]; pi_ = shapesP[name]
        h = parse_shape_hdr(P.blocks[pi_][1])
        dm = parse_dismember(P.blocks[h['skin']][1])
        dsize, vsize, vdesc, vbuf, tris = partition_raw(P, dm['part'])
        new_w, nearest = knn_transfer(src_pos, src_w, s['positions'])
        new_w = [prune_rows(w) for w in new_w]
        for w in new_w:
            for b in w:
                ensure_node(b)
        dis_fn, sd_b, sp_b, bones, pv = build_skin(P, nodesP, bone_xf, s['positions'], vbuf, vdesc, tris, new_w, BODY_PART)
        P.blocks[dm['data']][1] = bytearray(sd_b)
        P.blocks[dm['part']][1] = bytearray(sp_b)
        P.blocks[h['skin']][1] = dis_fn(dm['data'], dm['part'])
        use = {}
        for w in pv:
            for b, _ in w:
                use[b] = use.get(b, 0) + 1
        top = sorted(use.items(), key=lambda kv: -kv[1])[:10]
        print('re-skinned %s: %d verts, %d bones, nearest-source dist mean %.2f max %.2f' % (
            name, len(s['positions']), len(bones), nearest.mean(), nearest.max()))
        print('   top bones:', top)

    # ---- 6. root children + rebuild
    rn['children'] += new_shape_refs
    P.blocks[root][1] = build_node(rn)
    out, refmap = rebuild(P)
    out.save(OUT_NIF)
    print('wrote', OUT_NIF, 'blocks', len(out.blocks), 'strings', len(out.strings))


if __name__ == '__main__':
    main()
