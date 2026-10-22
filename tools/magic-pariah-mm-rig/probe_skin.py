"""Probe the exact NiSkinPartition / NiSkinData layout of the shapes we will
rebuild, and check the skin-to-bone transform convention."""
import sys, struct
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\ube-neck-pin\from-bodypin3")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifparse import Nif, load_mesh
from nifrw import Doc, parse_dismember, parse_shape_hdr

SP = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\8d6204d3-5065-49b7-8bd8-da1d0615990c\scratchpad"
MM = SP + r"\mm\Meandering Meadowlark 3BA\CalienteTools\BodySlide\ShapeData\Meandering Meadowlark Dress 3BA\Meandering Meadowlark Dress 3BA.nif"
MP = SP + r"\mp\Magic Pariah\CalienteTools\BodySlide\ShapeData\Magic Pariah Skirt HDT\Magic Pariah Skirt HDT.nif"


def part_layout(nif, shape_name):
    _, shapes = load_mesh(nif.path)
    sh = next(s for s in shapes if s['name'] == shape_name)
    si = nif.parse_skin_instance(sh['skin_ref'])
    off = nif.block_offsets[si['partition_ref']]
    raw = nif.data[off:off + nif.block_sizes[si['partition_ref']]]
    o = 0
    np_ = struct.unpack_from('<I', raw, o)[0]; o += 4
    dsize, vsize = struct.unpack_from('<II', raw, o); o += 8
    desc = struct.unpack_from('<Q', raw, o)[0]; o += 8
    o += dsize
    out = []
    for k in range(np_):
        nv, nt, nb, ns, nwpv = struct.unpack_from('<HHHHH', raw, o); o += 10
        bones = list(struct.unpack_from('<%dH' % nb, raw, o)); o += 2 * nb
        has_vm = raw[o]; o += 1
        vm = None
        if has_vm:
            vm = list(struct.unpack_from('<%dH' % nv, raw, o)); o += 2 * nv
        has_w = raw[o]; o += 1
        if has_w:
            o += 4 * nwpv * nv
        o += 2 * ns
        has_f = raw[o]; o += 1
        if has_f:
            o += 6 * nt if ns == 0 else 0
        has_bi = raw[o]; o += 1
        if has_bi:
            o += nwpv * nv
        unk = struct.unpack_from('<H', raw, o)[0]; o += 2
        pdesc = struct.unpack_from('<Q', raw, o)[0]; o += 8
        o += 6 * nt
        ident_vm = (vm == list(range(nv))) if vm is not None else None
        ident_bones = bones == list(range(nb))
        out.append(dict(nv=nv, nt=nt, nb=nb, ns=ns, nwpv=nwpv, has_vm=has_vm, ident_vm=ident_vm,
                        has_w=has_w, has_f=has_f, has_bi=has_bi, unk=unk, pdesc=hex(pdesc),
                        ident_bones=ident_bones, bones_head=bones[:6]))
    assert o == len(raw), (o, len(raw))
    return dict(np=np_, dsize=dsize, vsize=vsize, desc=hex(desc), parts=out, si_bones=len(si['bone_names']))


for label, path, names in (("MP", MP, ['Skirt Lower', 'Skirt Upper', 'chain belt_2']),
                           ("MM", MM, ['Draft Skirt weight test', 'CollThigh', 'CollCalves', 'skirt upper retop'])):
    nif = Nif(path)
    for n in names:
        print(label, n, part_layout(nif, n))
    # skin data: global transform + one bone entry
    _, shapes = load_mesh(path)
    for n in names[:2]:
        sh = next(s for s in shapes if s['name'] == n)
        sd = sh['skin_data']
        gt = sd['global_transform']
        print('   skindata global rot', np.round(gt['rot'], 4), 'trans', np.round(gt['trans'], 4), 'scale', gt['scale'], 'hvw', sd['has_vertex_weights'])
        si = nif.parse_skin_instance(sh['skin_ref'])
        for bi, bname in enumerate(si['bone_names']):
            if bname == 'NPC Pelvis [Pelv]':
                bt = sd['bones'][bi]
                print('   Pelvis bone: rot', np.round(bt['transform']['rot'], 4), 'trans', np.round(bt['transform']['trans'], 4),
                      'scale', bt['transform']['scale'], 'bound', np.round(bt['bound'], 3), 'nweights', len(bt['weights']))
                # verts weighted to pelvis -> mean position
                idx = [v for v, w in bt['weights']]
                P = np.array(sh['positions'])[idx]
                print('     mean pos of pelvis-weighted verts (skin space):', np.round(P.mean(0), 3), 'n', len(idx))
                R = np.array(bt['transform']['rot']).reshape(3, 3); T = np.array(bt['transform']['trans'])
                c1 = (R @ P.T).T + T
                c2 = (P @ R) + T
                print('     candidate A (R@v+T) center', np.round(c1.mean(0), 3), 'rad', round(float(np.linalg.norm(c1 - c1.mean(0), axis=1).max()), 3))
                print('     candidate B (v@R+T) center', np.round(c2.mean(0), 3), 'rad', round(float(np.linalg.norm(c2 - c2.mean(0), axis=1).max()), 3))
                break

# dismember flags of MP skirt + MM proxies
doc = Doc(MP)
for i, (t, b) in enumerate(doc.blocks):
    if t == 'BSDismemberSkinInstance':
        d = parse_dismember(b)
        print('MP dismember blk', i, 'root', d['root'], 'parts', d['parts'])
docm = Doc(MM)
for n in ('Draft Skirt weight test', 'CollThigh', 'CollCalves'):
    i = docm.find('BSTriShape', n)
    h = parse_shape_hdr(docm.blocks[i][1])
    d = parse_dismember(docm.blocks[h['skin']][1])
    print('MM', n, 'shape flags 0x%X' % h['flags'], 'bound', np.round(h['bound'], 2), 'tail', h['tail'], 'dismember parts', d['parts'], 'root', d['root'])
# MP shapes header tails
for n in ('Skirt Lower', 'Skirt Upper'):
    i = doc.find('BSTriShape', n)
    h = parse_shape_hdr(doc.blocks[i][1])
    print('MP', n, 'flags 0x%X' % h['flags'], 'tail', h['tail'], 'vdesc', hex(h['vdesc']), 'ntri', h['ntri'], 'nvert', h['nvert'], 'dsize', h['dsize'])
