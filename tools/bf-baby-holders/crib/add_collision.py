"""Give Bishop's (Skyrim Romance) crib meshes a box collision so the crib can be
activated. Copies the bhk box/rigid-body/collision-object blocks from vanilla's
Whiterun small rug (Lux copy), resizes the box to the crib's bounds and hangs it
on a new child node at the crib's centre.
    python -I add_collision.py <in.nif> <out.nif>
"""
import struct, sys
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifrw import Doc, parse_node, build_node, parse_shape_hdr

DONOR = r"C:\1. AUTHORIA\mods\Lux (main) - rerun\meshes\architecture\whiterun\wrclutter\wrrugsmall01.nif"
HAVOK = 69.99124  # game units per havok unit


def shape_points(b):
    d = parse_shape_hdr(b)
    vsize = (d['vdesc'] & 0xF) * 4
    attrs = d['vdesc'] >> 44
    full = bool(attrs & 0x400)
    raw = d['tail']
    pts = []
    for i in range(d['nvert']):
        o = i * vsize
        pts.append(struct.unpack_from('<3f', raw, o))   # SSE stores full-float positions
    if not pts:
        return np.zeros((0, 3)), d['skin']
    p = np.array(pts, dtype=float) * d['scale']
    rot = np.array(d['rot']).reshape(3, 3)
    return p @ rot.T + np.array(d['trans']), d['skin']


def main(src, dst):
    donor = Doc(DONOR)
    don = {t: bytearray(b) for t, b in donor.blocks if t.startswith('bhk') or t == 'BSXFlags'}

    doc = Doc(src)
    root = parse_node(doc.blocks[0][1])
    lo, hi = np.full(3, 1e9), np.full(3, -1e9)
    for t, b in doc.blocks:
        if t == 'BSTriShape':
            p, skin = shape_points(b)
            if len(p) and skin < 0:          # rigid shapes only; the skinned baby sits inside
                lo = np.minimum(lo, p.min(0)); hi = np.maximum(hi, p.max(0))
    centre, half = (lo + hi) / 2, (hi - lo) / 2
    print('crib bounds', lo.round(1), hi.round(1))

    n0 = len(doc.blocks)
    i_box, i_rb, i_co, i_node, i_bsx = n0, n0 + 1, n0 + 2, n0 + 3, n0 + 4

    box = don['bhkBoxShape']
    struct.pack_into('<3f', box, 16, *(half / HAVOK))
    rb = don['bhkRigidBody']
    struct.pack_into('<i', rb, 0, i_box)
    co = don['bhkCollisionObject']
    struct.pack_into('<i', co, 0, i_node)
    struct.pack_into('<i', co, 6, i_rb)

    if 'CribCollision' not in doc.strings:
        doc.strings.append('CribCollision')
    if 'BSX' not in doc.strings:
        doc.strings.append('BSX')
    node = dict(name=doc.strings.index('CribCollision'), extra=[], ctrl=-1, flags=14,
                trans=tuple(centre), rot=(1, 0, 0, 0, 1, 0, 0, 0, 1), scale=1.0,
                coll=i_co, children=[], effects=[])
    bsx = bytearray(don['BSXFlags'])
    struct.pack_into('<I', bsx, 0, doc.strings.index('BSX'))
    struct.pack_into('<I', bsx, 4, 130)    # Havok + articulated/external-emit as vanilla statics

    doc.blocks += [['bhkBoxShape', box], ['bhkRigidBody', rb], ['bhkCollisionObject', co],
                   ['NiNode', build_node(node)], ['BSXFlags', bsx]]
    # the basket is modelled ~86 units up; drop it so it sits on the floor where placed
    root['trans'] = (root['trans'][0], root['trans'][1], root['trans'][2] - lo[2])
    root['children'].append(i_node)
    root['extra'].append(i_bsx)
    doc.blocks[0][1] = build_node(root)
    doc.save(dst)
    print('wrote', dst, 'box half-extents', half.round(1), 'centre', centre.round(1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
