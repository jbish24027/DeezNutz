"""Repair a flattened NiNode hierarchy in a converted nif using a reference nif that has
the correct tree (same node names). For every NiNode that exists in both:
  - if its parent (by name) differs from the reference, move it under the reference's parent
    (when that node exists in the target)
  - copy the local transform (translation, rotation, scale) from the reference
Root nodes are never moved. Shapes are untouched. Header + block sizes rebuilt.
Verifies by re-parsing. Read-only on both inputs."""
import os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from niflib import Nif
from nif_extradata import Header

NODE_TYPES = ('NiNode', 'BSFadeNode', 'BSLeafAnimNode', 'BSTreeNode', 'BSOrderedNode', 'BSMultiBoundNode', 'BSBlastNode', 'BSDamageStage', 'BSValueNode')

def parse_node(data, off):
    p = off
    name_i, ned = struct.unpack_from('<II', data, p); p += 8
    extra = list(struct.unpack_from('<%di' % ned, data, p)); p += 4*ned
    ctrl, = struct.unpack_from('<i', data, p); p += 4
    flags, = struct.unpack_from('<I', data, p); p += 4
    trans = struct.unpack_from('<3f', data, p); p += 12
    rot = struct.unpack_from('<9f', data, p); p += 36
    scale, = struct.unpack_from('<f', data, p); p += 4
    coll, = struct.unpack_from('<i', data, p); p += 4
    nch, = struct.unpack_from('<I', data, p); p += 4
    ch = list(struct.unpack_from('<%di' % nch, data, p)); p += 4*nch
    nef, = struct.unpack_from('<I', data, p); p += 4
    ef = list(struct.unpack_from('<%di' % nef, data, p)); p += 4*nef
    return dict(name_i=name_i, extra=extra, ctrl=ctrl, flags=flags, trans=list(trans), rot=list(rot), scale=scale,
                coll=coll, children=ch, effects=ef, end=p)

def build_node(nd):
    out = struct.pack('<II', nd['name_i'], len(nd['extra'])) + struct.pack('<%di' % len(nd['extra']), *nd['extra'])
    out += struct.pack('<i', nd['ctrl']) + struct.pack('<I', nd['flags']) + struct.pack('<3f', *nd['trans']) + struct.pack('<9f', *nd['rot'])
    out += struct.pack('<f', nd['scale']) + struct.pack('<i', nd['coll'])
    out += struct.pack('<I', len(nd['children'])) + struct.pack('<%di' % len(nd['children']), *nd['children'])
    out += struct.pack('<I', len(nd['effects'])) + struct.pack('<%di' % len(nd['effects']), *nd['effects'])
    return out

def tree_by_name(n):
    parent = {}; nodes = {}
    for i in range(n.num_blocks):
        if n.btype[i] in NODE_TYPES:
            nd = parse_node(n.data, n.offsets[i])
            nodes[i] = nd
            for c in nd['children']:
                if c >= 0: parent[c] = i
    name_of = {i: n.s(nd['name_i']) for i, nd in nodes.items()}
    return nodes, parent, name_of

def repair(target_path, ref_path, out_path, log, add_missing=True):
    T = Nif(target_path); R = Nif(ref_path)
    tn, tparent, tname = tree_by_name(T)
    rn, rparent, rname = tree_by_name(R)
    t_by_name = {}
    for i, nm in tname.items():
        t_by_name.setdefault(nm, i)
    r_by_name = {}
    for i, nm in rname.items():
        r_by_name.setdefault(nm, i)
    footer_len = len(T.data) - T.end
    h = Header(T.data)
    assert h.serialize() == bytes(T.data[:h.end])
    blocks = [bytes(T.data[T.offsets[k]:T.offsets[k]+T.sizes[k]]) for k in range(T.num_blocks)]
    types_str = [t.decode('latin1') for t in h.types]
    added = []
    if add_missing:
        # create NiNode blocks for reference nodes the target lacks (transform/flags from the reference)
        if 'NiNode' not in types_str:
            h.types.append(b'NiNode'); types_str.append('NiNode')
        tidx = types_str.index('NiNode')
        for nm, ri in r_by_name.items():
            if nm in t_by_name: continue
            b = nm.encode('latin1')
            if b in h.strings: name_i = h.strings.index(b)
            else: h.strings.append(b); name_i = len(h.strings) - 1
            rd = rn[ri]
            nd = dict(name_i=name_i, extra=[], ctrl=-1, flags=rd['flags'], trans=rd['trans'], rot=rd['rot'], scale=rd['scale'],
                      coll=-1, children=[], effects=[])
            new_index = len(blocks)
            blocks.append(build_node(nd)); h.type_idx.append(tidx); h.sizes.append(len(blocks[-1])); h.num_blocks += 1
            tn[new_index] = nd; tname[new_index] = nm; t_by_name[nm] = new_index
            added.append(nm)
    root_t = [i for i in tn if i not in tparent and i < T.num_blocks][0]
    moves = []; xf_copies = 0
    for i, nm in list(tname.items()):
        if nm not in r_by_name: continue
        ri = r_by_name[nm]
        # transform copy
        tn[i]['trans'] = rn[ri]['trans']; tn[i]['rot'] = rn[ri]['rot']; tn[i]['scale'] = rn[ri]['scale']; xf_copies += 1
        if i == root_t:                 # target root: never move
            continue
        rp = rparent.get(ri)
        if rp is None:
            # reference root; a newly added orphan with no reference parent goes under the target root
            if i not in tparent:
                tn[root_t]['children'].append(i); tparent[i] = root_t; moves.append((nm, None, tname[root_t]))
            continue
        rp_name = rname[rp]; tp_name = tname.get(tparent.get(i)) if i in tparent else None
        if rp_name != tp_name:
            newp = t_by_name.get(rp_name, root_t)
            if i in tparent:
                oldp = tparent[i]
                tn[oldp]['children'] = [c for c in tn[oldp]['children'] if c != i]
            tn[newp]['children'].append(i)
            tparent[i] = newp
            moves.append((nm, tp_name, tname[newp]))
    # rebuild
    for i, nd in tn.items():
        blocks[i] = build_node(nd)
        h.sizes[i] = len(blocks[i])
    footer = bytes(T.data[T.end:])
    out = h.serialize() + b''.join(blocks) + footer
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as fh:
        fh.write(out)
    # verify: parents by name now match the reference for all shared nodes
    V = Nif(out_path)
    assert len(V.data) - V.end == footer_len
    vn, vparent, vname = tree_by_name(V)
    v_by_name = {}
    for i, nm in vname.items(): v_by_name.setdefault(nm, i)
    mismatch = []
    for nm, vi in v_by_name.items():
        if nm in r_by_name:
            ri = r_by_name[nm]
            vp = vname.get(vparent.get(vi)); rp = rname.get(rparent.get(ri))
            if vp != rp and rp in v_by_name:
                mismatch.append((nm, vp, rp))
    # every child ref must be a valid block referenced exactly once
    refs = [c for nd in vn.values() for c in nd['children'] if c >= 0]
    assert len(refs) == len(set(refs)), 'duplicate child refs'
    log.append('%s: added %d node(s) %s; moved %d node(s); transforms copied for %d nodes; residual parent mismatches: %s' % (
        os.path.basename(out_path), len(added), added, len(moves), xf_copies, mismatch))
    return moves, mismatch

if __name__ == '__main__':
    log = []
    repair(sys.argv[1], sys.argv[2], sys.argv[3], log)
    print('\n'.join(log))
