"""Authoria robe SMP (2026-10-18): Helga-style cloth grids on the vanilla black mage robes (Clothes\\Warlock)
and the necromancer robes (Clothes\\Necromancer), men + women + the UBE women's lane, keeping their look.
User: "build cloth physics into the black mage robes and necromancer robes (men and women), keeping their look".

Per mesh pair (_0/_1): one rig fitted on the averaged skirt verts (identical bones in both weights), a 12-column grid
under NPC Pelvis (clothrig.ClothRig, same bone frame as Magic Pariah v4), smooth skinning blended with the mesh's own
body weights by height (body above the hip, cloth below), invisible shader-less leg colliders (rings around each
thigh/calf, radii measured from the matching body mesh), and the HDT physics link. Every original shape keeps its
positions; only the cloth shapes are re-skinned. Output goes to a NEW mod folder; sources are never touched.

usage: python -I build_robes.py <out_mod_dir>
"""
import os, re, sys, struct
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\ube-neck-pin\from-bodypin3")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifparse import load_mesh
from nifrw import Doc, rebuild, parse_node, build_node, parse_shape_hdr, build_shape, parse_dismember
from graft import bone_table, node_index, shape_index, build_skin, skin_offset
from clothrig import ClothRig, blend, stats
from build_v4 import partition_any, world_of, add_rig_nodes, reskin

MODS = r"C:\1. AUTHORIA\mods"
PHYS = "HDT Skinned Mesh Physics Object"
PREFIX = 'rsk'
COLS = ['B', 'L1', 'L2', 'L3', 'L4', 'L5', 'F', 'R5', 'R4', 'R3', 'R2', 'R1']
COLL = 'RobeLegColl'
HIMBO_BODY = MODS + r"\Highly Improved Male Body Overhaul -HIMBO-\meshes\actors\character\character assets\malebody_%s.nif"
F3BA_BODY = MODS + r"\Authoria - Bodyslide Output - 3BA\meshes\actors\character\character assets\femalebody_%s.nif"

# (source mod, mesh path without _0/_1, cloth shapes, body source for collider radii, xml, rig kind)
ROBE_XML = r"meshes\authoria robe smp\robes.xml"
NECRO_F_XML = r"meshes\authoria robe smp\necromancer skirt f.xml"
TARGETS = [
    ("Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors", r"meshes\clothes\warlock\warlockrobes", ['robes'], ('file', HIMBO_BODY, None), ROBE_XML, 'robe'),
    ("Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors", r"meshes\clothes\necromancer\necromancerrobes", ['robes'], ('file', HIMBO_BODY, None), ROBE_XML, 'robe'),
    ("CBBE 3BA Vanilla Outfits Redone - Prebuilt", r"meshes\clothes\warlock\warlockrobes_f", ['robes'], ('file', F3BA_BODY, None), ROBE_XML, 'robe'),
    ("Authoria - UBE Converter Output", r"meshes\!UBE\clothes\warlock\warlockrobes_f", ['robes'], ('self', None, 'BaseShape'), ROBE_XML, 'robe'),
    ("Authoria - Bodyslide Output - 3BA", r"meshes\clothes\necromancer\necromancerrobes_f", ['Skirt01Back', 'Skirt01bFront'], ('self', None, '3BA'), NECRO_F_XML, 'panels'),
    ("Authoria - UBE Converter Output", r"meshes\!UBE\clothes\necromancer\necromancerrobes_f", ['Skirt01Back', 'Skirt01bFront'], ('self', None, 'BaseShape'), NECRO_F_XML, 'panels'),
]
LEGS = [('NPC L Thigh [LThg]', 'NPC L Calf [LClf]'), ('NPC L Calf [LClf]', 'NPC L Foot [Lft ]'),
        ('NPC R Thigh [RThg]', 'NPC R Calf [RClf]'), ('NPC R Calf [RClf]', 'NPC R Foot [Rft ]')]
RINGS, SIDES = 6, 10
ROBE_ROWS, PANEL_ROWS = 8, 7
ARM = re.compile(r'(Arm|Hand|Finger|Clavicle)', re.I)


def ci_path(root, rel):
    p = root
    for part in rel.split("\\"):
        m = [x for x in os.listdir(p) if x.lower() == part.lower()]
        if not m:
            return None
        p = os.path.join(p, m[0])
    return p


def seg_ends(bone_xf, a, b):
    """world origins of a leg segment; a missing foot bone (UBE meshes) is extrapolated along the thigh->calf line."""
    _, Ta = world_of(bone_xf, a)
    if b in bone_xf:
        return Ta, world_of(bone_xf, b)[1]
    thigh = a.replace('Calf [LClf]', 'Thigh [LThg]').replace('Calf [RClf]', 'Thigh [RThg]')
    _, Tt = world_of(bone_xf, thigh)
    return Ta, Ta + (Ta - Tt) * 0.95


def leg_radii(body_pos, body_w, bone_xf_body):
    """per leg segment: RINGS radii, from the body verts dominated by that segment's bone."""
    P = np.array(body_pos); out = {}
    dom = [max(w.items(), key=lambda kv: kv[1])[0] if w else None for w in body_w]
    for a, b in LEGS:
        Ta, Tb = seg_ends(bone_xf_body, a, b)
        u = Tb - Ta; L = np.linalg.norm(u); u = u / L
        m = np.array([d == a for d in dom])
        D = P[m] - Ta; t = D @ u / L
        r = np.linalg.norm(D - np.outer(D @ u, u), axis=1)
        radii = []
        for k in range(RINGS):
            tc = (k + 0.5) / RINGS
            sel = np.abs(t - tc) < 0.5 / RINGS
            radii.append(float(np.percentile(r[sel], 60)) if sel.sum() >= 5 else np.nan)
        radii = np.array(radii)
        good = ~np.isnan(radii)
        radii[~good] = np.interp(np.where(~good)[0], np.where(good)[0], radii[good])
        out[a] = radii
    return out


def collider_geometry(bone_xf, radii):
    """ring vertices around each leg segment (in this file's skeleton), weight 1.0 to the segment bone."""
    pos, wts, tris = [], [], []
    for a, b in LEGS:
        Ta, Tb = seg_ends(bone_xf, a, b)
        u = Tb - Ta; L = np.linalg.norm(u); u = u / L
        e1 = np.cross(u, [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(u, e1)
        base = len(pos)
        for k in range(RINGS):
            c = Ta + u * L * (k + 0.5) / RINGS
            r = max(radii[a][k] - 0.8, 1.5)          # spheres (margin) sit on the skin, not outside it
            for s in range(SIDES):
                ph = 2 * np.pi * s / SIDES
                pos.append(c + r * (np.cos(ph) * e1 + np.sin(ph) * e2)); wts.append({a: 1.0})
        for k in range(RINGS - 1):
            for s in range(SIDES):
                i0 = base + k * SIDES + s; i1 = base + k * SIDES + (s + 1) % SIDES
                j0 = i0 + SIDES; j1 = i1 + SIDES
                tris += [(i0, i1, j0), (i1, j1, j0)]
    return np.array(pos), wts, tris


def add_collider(D, nodes, bone_xf, template_si, pos, wts, tris):
    """new shader-less skinned BSTriShape (invisible collision helper) cloned from a template shape header."""
    h = parse_shape_hdr(D.blocks[template_si][1])
    tdm = parse_dismember(D.blocks[h['skin']][1])
    vdesc = h['vdesc']
    vsize, soff = skin_offset(vdesc)
    vf = (vdesc >> 44) & 0xFFF
    pos_size = soff - 4 * sum(1 for f in (0x2, 0x8, 0x10, 0x20) if vf & f)
    assert pos_size in (8, 16), pos_size
    full = pos_size == 16                                   # full-precision layout: 3 floats + bitangent x
    vb = bytearray(len(pos) * vsize)
    for i, p in enumerate(pos):
        if full:
            struct.pack_into('<4f', vb, i * vsize, float(p[0]), float(p[1]), float(p[2]), 0.0)
        else:
            vb[i * vsize:i * vsize + 8] = np.array([p[0], p[1], p[2], 0], dtype='<f2').tobytes()
    dis_fn, sd_b, sp_b, bones, pv = build_skin(D, nodes, bone_xf, pos.tolist(), bytes(vb), vdesc, tris, wts, 38)
    D.blocks.append(['NiSkinData', bytearray(sd_b)]); di = len(D.blocks) - 1
    D.blocks.append(['NiSkinPartition', bytearray(sp_b)]); pi = len(D.blocks) - 1
    D.blocks.append(['BSDismemberSkinInstance', bytearray(dis_fn(di, pi))]); ski = len(D.blocks) - 1
    c = pos.mean(0); rad = float(np.linalg.norm(pos - c, axis=1).max())
    nh = dict(h)
    nh.update(name=D.sidx(COLL), extra=[], ctrl=-1, trans=(0.0, 0.0, 0.0), rot=(1.0, 0, 0, 0, 1.0, 0, 0, 0, 1.0), scale=1.0,
              coll=-1, bound=(float(c[0]), float(c[1]), float(c[2]), rad), skin=ski, shader=-1, alpha=-1,
              ntri=len(tris), nvert=len(pos), dsize=0)
    assert len(h['tail']) == 4 and h['dsize'] == 0, 'template is not a plain skinned SSE shape'
    D.blocks.append(['BSTriShape', bytearray(build_shape(nh))]); si = len(D.blocks) - 1
    root = D.roots[0]
    rn = parse_node(D.blocks[root][1]); rn['children'].append(si); D.blocks[root][1] = build_node(rn)
    return si


def add_phys_link(D, xml):
    root = D.roots[0]
    for t, b in D.blocks:
        if t == 'NiStringExtraData' and D.strings[struct.unpack_from('<I', b, 0)[0]] == PHYS:
            raise RuntimeError('mesh already carries a physics link')
    D.blocks.append(['NiStringExtraData', bytearray(struct.pack('<II', D.sidx(PHYS), D.sidx(xml)))])
    rn = parse_node(D.blocks[root][1]); rn['extra'].append(len(D.blocks) - 1); D.blocks[root][1] = build_node(rn)


def rig_for(kind, avgP, pelvis_z):
    if kind == 'robe':
        z0 = pelvis_z + 3.0
        hem = float(np.percentile(avgP[:, 2], 0.5))
        rows = list(np.linspace(z0, hem + 4.0, ROBE_ROWS))
        d_hi, d_lo = pelvis_z - 1.0, pelvis_z - 13.0
    else:   # split skirt panels hanging from the belt
        top = float(np.percentile(avgP[:, 2], 99.5))
        hem = float(np.percentile(avgP[:, 2], 0.5))
        z0 = top - 2.0
        rows = list(np.linspace(z0, hem + 3.0, PANEL_ROWS))
        d_hi, d_lo = top - 3.0, top - 13.0
    sel = avgP[:, 2] < d_hi
    xc = float(np.median(avgP[sel, 0])); yc = float(np.median(avgP[sel, 1]))
    rig = ClothRig(PREFIX, COLS, origin=(xc, yc, z0), axis=(0, 0, -1), ref=(0, -1, 0),
                   parent='NPC Pelvis [Pelv]', rows_t=[z0 - z for z in rows], spacing_t=float(rows[0] - rows[1]))
    rig.fit(avgP, sel)
    return rig, rows, d_hi, d_lo


def build(out_root, mod, base, cloth, body_src, xml, kind, log):
    paths = {w: ci_path(os.path.join(MODS, mod), base + w + '.nif') for w in ('_0', '_1')}
    assert all(paths.values()), paths
    loaded = {w: load_mesh(p) for w, p in paths.items()}
    shp = {w: {s['name']: s for s in loaded[w][1]} for w in paths}
    # averaged cloth geometry (identical vert order in _0/_1)
    avg = []
    for nm in cloth:
        a = np.array(shp['_0'][nm]['positions']); b = np.array(shp['_1'][nm]['positions'])
        assert a.shape == b.shape, (nm, a.shape, b.shape)
        avg.append((a + b) / 2)
    avgP = np.vstack(avg)
    bx1 = bone_table(*loaded['_1'])
    pelvis_z = float(world_of(bx1, 'NPC Pelvis [Pelv]')[1][2])
    rig, rows, d_hi, d_lo = rig_for(kind, avgP, pelvis_z)
    log('  rig rows z %s | cloth below %.1f, full cloth below %.1f | radius/row %s' % (
        ' '.join('%.0f' % z for z in rows), d_hi, d_lo, ' '.join('%.0f' % x for x in np.nanmean(rig.radius, axis=1))))
    # one weight set for both files
    new_w = {}
    off = 0
    for nm, P in zip(cloth, avg):
        rw = rig.weights(P)
        base_w = shp['_1'][nm]['weight_map']
        ws = []
        for k, (w, r_w) in enumerate(zip(base_w, rw)):
            z = P[k, 2]
            d = float(np.clip((d_hi - z) / (d_hi - d_lo), 0.0, 1.0))
            if sum(v for bn, v in w.items() if ARM.search(bn)) > 0.05:
                d = 0.0                                  # sleeve cuffs hang at hip height: they stay on the arm
            ws.append(blend(r_w, w, d))
        new_w[nm] = ws
        log('  %-14s %5d verts | %s' % (nm, len(P), stats(ws, PREFIX)))
    report = []
    for w, path in paths.items():
        D = Doc(path); nif, shapes = loaded[w]
        by = {s['name']: s for s in shapes}
        nodes = node_index(D); sidx = shape_index(D)
        bone_xf = bone_table(nif, shapes)
        assert not any(n.startswith(PREFIX + '_') for n in nodes), 'already rigged'
        flags = parse_node(D.blocks[nodes['NPC Pelvis [Pelv]']][1])['flags']
        add_rig_nodes(D, nodes, bone_xf, rig, flags)
        for nm in cloth:
            slot = parse_dismember(D.blocks[parse_shape_hdr(D.blocks[sidx[nm]][1])['skin']][1])['parts'][0][1]
            nb = reskin(D, nodes, bone_xf, by[nm], sidx[nm], new_w[nm], slot)
        # collider radii from the matching body
        if body_src[0] == 'file':
            bp = body_src[1] % w[1]
            bn, bs = load_mesh(bp); bsh = max(bs, key=lambda s: len(s['positions']))
            radii = leg_radii(bsh['positions'], bsh['weight_map'], bone_table(bn, bs))
        else:
            bsh = by[body_src[2]]
            radii = leg_radii(bsh['positions'], bsh['weight_map'], bone_xf)
        cp, cw, ct = collider_geometry(bone_xf, radii)
        add_collider(D, nodes, bone_xf, sidx[cloth[0]], cp, cw, ct)
        add_phys_link(D, xml)
        out, _ = rebuild(D)
        rel = os.path.relpath(path, os.path.join(MODS, mod))
        dst = os.path.join(out_root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        out.save(dst)
        # verify: every original shape keeps its positions; untouched shapes keep their weights; cloth normalised
        n2, s2 = load_mesh(dst); B = {s['name']: s for s in s2}
        for nm, s in by.items():
            assert np.allclose(np.array(s['positions']), np.array(B[nm]['positions']), atol=1e-4), nm
            if nm in cloth:
                assert all(abs(sum(x.values()) - 1) < 1e-3 for x in B[nm]['weight_map']), nm
            else:
                assert B[nm]['weight_map'] == s['weight_map'], nm
        assert COLL in B and len(B[COLL]['positions']) == len(cp)
        assert np.allclose(np.array(B[COLL]['positions']), cp, atol=1e-3), 'collider positions'
        links = [out.strings[struct.unpack_from('<I', b, 4)[0]] for t, b in out.blocks if t == 'NiStringExtraData']
        log('  wrote %s (%d blocks) radii thigh %.1f-%.1f calf %.1f-%.1f links %s' % (
            rel, len(out.blocks), radii[LEGS[0][0]].max(), radii[LEGS[0][0]].min(), radii[LEGS[1][0]].max(), radii[LEGS[1][0]].min(), links))
        report.append(dict(file=rel, src=mod, xml=xml, bones=sorted(set(b for nm in cloth for x in B[nm]['weight_map'] for b in x) | {LEGS[0][0], LEGS[1][0], LEGS[2][0], LEGS[3][0]})))
    return rig, rows, report


if __name__ == '__main__':
    import json
    out_root = sys.argv[1]
    allrep = []
    rigs = {}
    for mod, base, cloth, body_src, xml, kind in TARGETS:
        print('===', mod, '|', base)
        rig, rows, rep = build(out_root, mod, base, cloth, body_src, xml, kind, print)
        rigs.setdefault(xml, []).append(len(rows))
        allrep += rep
    json.dump(dict(files=allrep, rows=rigs), open(os.path.join(out_root, '..', 'build_report.json'), 'w'), indent=1)
    print('DONE', len(allrep), 'meshes; rows per xml', rigs)
