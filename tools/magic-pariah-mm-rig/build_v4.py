"""Magic Pariah v4 (2026-09-06): Helga-style cloth rigs on the skirt AND the sleeves.
User: "same cloth feel as the Helga dress skirt; the Pariah skirt and sleeves move as one big piece".

Skirt: the 12x4 Meadowlark chain is replaced by a 14-column x 7-row grid (Helga's layout) placed on
the skirt surface under NPC Pelvis, with ~4-bone smooth skinning per vertex (Helga: ~2 columns x
~3 rows per vertex). The v3 body/cloth hand-over heights are kept (cloth share = the v3 chain share).
Sleeves: the single dangling bone per sleeve (sl_a2 / sl_b2) is replaced by an 8-column x 4-row
grid around each forearm; the designer's dynamic region (the old sl_* weight) is kept as the mask.
Colliders (CollThigh/CollCalves/CollButt, Cube) untouched. XML: make_xml_v4.py.

usage: python build_v4.py [--apply]   (dry run by default; backups <nif>.bak-v3-20260906)
"""
import os, re, shutil, struct, sys
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\ube-neck-pin\from-bodypin3")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifparse import load_mesh
from nifrw import Doc, rebuild, parse_node, build_node, parse_shape_hdr, build_shape, parse_dismember
from graft import bone_table, node_index, shape_index, build_skin
from clothrig import ClothRig, blend, stats

TAG = 'bak-v3-20260906'
MODS = r"C:\1. AUTHORIA\mods"
UBE = MODS + r"\Authoria - UBE Converter Output - Magic Pariah\meshes\!UBE\clothes\magic pariah"
BS = MODS + r"\Authoria - Bodyslide Output - UBE\Meshes\clothes\magic pariah"
SD = MODS + r"\Magic Pariah - Meadowlark Physics\CalienteTools\BodySlide\ShapeData"
SKIRTS = [UBE + r"\magic pariah skirt HDT_0.nif", UBE + r"\magic pariah skirt HDT_1.nif",
          BS + r"\Magic Pariah Skirt HDT_0.nif", BS + r"\Magic Pariah Skirt HDT_1.nif",
          SD + r"\Magic Pariah Skirt HDT\Magic Pariah Skirt HDT.nif"]
TOPS = [UBE + r"\Magic Pariah Top_0.nif", UBE + r"\Magic Pariah Top_1.nif",
        BS + r"\Magic Pariah Top_0.nif", BS + r"\Magic Pariah Top_1.nif",
        SD + r"\Magic Pariah Top\Magic Pariah Top.nif"]

SKIRT_COLS = ['B', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'F', 'R6', 'R5', 'R4', 'R3', 'R2', 'R1']
SKIRT_ROWS_Z = [73.5, 69.5, 64.5, 59.5, 54.5, 49.5, 44.5, 39.5]      # row 0 = static anchor ring
SKIRT_SHAPES = ['Skirt Lower', 'Skirt Upper', 'MMSkirtProxy']
SLEEVE_COLS = ['c%d' % k for k in range(8)]
SLEEVES = {'L': dict(prefix='slvL', parent='NPC L Forearm [LLar]', hand='NPC L Hand [LHnd]', twist='NPC L ForearmTwist1 [LLt1]', old=('sl_1a1', 'sl_a2')),
           'R': dict(prefix='slvR', parent='NPC R Forearm [RLar]', hand='NPC R Hand [RHnd]', twist='NPC R ForearmTwist1 [RLt1]', old=('sl_b1', 'sl_b2'))}


def partition_any(doc, part_idx):
    """(vsize, vdesc, vbuf, tris) of an SSE NiSkinPartition with any number of partitions."""
    raw = doc.blocks[part_idx][1]
    np_, dsize, vsize = struct.unpack_from('<III', raw, 0)
    vdesc = struct.unpack_from('<Q', raw, 12)[0]
    vbuf = bytes(raw[20:20 + dsize]); o = 20 + dsize
    tris = []
    for _ in range(np_):
        nv, nt, nb, ns, nwpv = struct.unpack_from('<HHHHH', raw, o); o += 10
        o += 2 * nb
        assert ns == 0
        if raw[o]: o += 1 + 2 * nv
        else: o += 1
        if raw[o]: o += 1 + 4 * nwpv * nv
        else: o += 1
        has_f = raw[o]; o += 1
        if has_f:
            tris += [struct.unpack_from('<HHH', raw, o + 6 * i) for i in range(nt)]; o += 6 * nt
        if raw[o]: o += 1 + nwpv * nv
        else: o += 1
        o += 2 + 8 + 6 * nt
    assert o == len(raw), (o, len(raw))
    return vsize, vdesc, vbuf, tris


def world_of(bone_xf, name):
    rot, trans, scale = bone_xf[name]
    R = np.array(rot).reshape(3, 3); T = np.array(trans)
    return R.T, -R.T @ T                     # inverse of the skin-to-bone bind = the bone's rest world


def add_rig_nodes(D, nodes, bone_xf, rig, flags):
    """Create the rig's NiNodes (row 0 under the anchor body bone, rows chained), return bind table."""
    worlds = {}
    for name, par, R, T, row in rig.bones():
        worlds[name] = (R, T)
        if par in worlds:
            Rp, Tp = worlds[par]
        else:
            Rp, Tp = world_of(bone_xf, par)
        Rl = Rp.T @ R; Tl = Rp.T @ (T - Tp)
        nd = dict(name=D.sidx(name), extra=[], ctrl=-1, flags=flags, trans=tuple(float(x) for x in Tl),
                  rot=tuple(float(x) for x in Rl.reshape(-1)), scale=1.0, coll=-1, children=[], effects=[])
        D.blocks.append(['NiNode', build_node(nd)])
        idx = len(D.blocks) - 1
        nodes[name] = idx
        pn = parse_node(D.blocks[nodes[par]][1])
        pn['children'].append(idx)
        D.blocks[nodes[par]][1] = build_node(pn)
        bone_xf[name] = (tuple(float(x) for x in R.T.reshape(-1)), tuple(float(x) for x in (-R.T @ T)), 1.0)
    return worlds


def detach(D, nodes, parent_name, child_names):
    pn = parse_node(D.blocks[nodes[parent_name]][1])
    before = len(pn['children'])
    pn['children'] = [c for c in pn['children'] if c < 0 or D.name_of(c) not in child_names]
    D.blocks[nodes[parent_name]][1] = build_node(pn)
    return before - len(pn['children'])


def reskin(D, nodes, bone_xf, shape, si, new_w, slot=None):
    h = parse_shape_hdr(D.blocks[si][1]); dm = parse_dismember(D.blocks[h['skin']][1])
    vsize, vdesc, vbuf, tris = partition_any(D, dm['part'])
    part = slot if slot is not None else dm['parts'][0][1]
    for w in new_w:
        for b in w:
            assert b in nodes and b in bone_xf, b
    dis_fn, sd_b, sp_b, bones, pv = build_skin(D, nodes, bone_xf, shape['positions'], vbuf, vdesc, tris, new_w, part)
    D.blocks[dm['data']][1] = bytearray(sd_b)
    D.blocks[dm['part']][1] = bytearray(sp_b)
    D.blocks[h['skin']][1] = dis_fn(dm['data'], dm['part'])
    return len(bones)


def verify_only(path, expect_shapes):
    bak = path + '.' + TAG
    nifA, shA = load_mesh(bak); nifB, shB = load_mesh(path)
    A = {s['name']: s for s in shA}; B = {s['name']: s for s in shB}
    assert set(A) == set(B), (set(A) ^ set(B))
    for name in A:
        assert np.allclose(np.array(A[name]['positions']), np.array(B[name]['positions'])), name
        if name in expect_shapes[:-1]:
            assert all(abs(sum(w.values()) - 1) < 1e-3 for w in B[name]['weight_map']), name
        else:
            assert B[name]['weight_map'] == A[name]['weight_map'], name
    print('   verified against backup:', os.path.basename(path))


def finish(D, path, apply, expect_shapes):
    out, refmap = rebuild(D)
    if not apply:
        print('   (dry run) would write %d blocks' % len(out.blocks))
        return
    bak = path + '.' + TAG
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    out.save(path)
    nifA, shA = load_mesh(bak); nifB, shB = load_mesh(path)
    A = {s['name']: s for s in shA}; B = {s['name']: s for s in shB}
    assert set(A) == set(B), (set(A) ^ set(B))
    for name in A:
        assert np.allclose(np.array(A[name]['positions']), np.array(B[name]['positions'])), name
        if name in expect_shapes[:-1]:         # the re-skinned shape(s): weights must be normalised
            assert all(abs(sum(w.values()) - 1) < 1e-3 for w in B[name]['weight_map']), name
        else:                                 # untouched shapes: weights byte-for-byte as before
            assert B[name]['weight_map'] == A[name]['weight_map'], name
    for name in expect_shapes:
        assert name in B
    links = [out.strings[struct.unpack_from('<I', b, 4)[0]] for t, b in out.blocks if t == 'NiStringExtraData']
    print('   written + verified: %d blocks, links %s' % (len(out.blocks), links))


# ---------------------------------------------------------------- skirt
def do_skirt(path, apply):
    print('=== SKIRT', path)
    D = Doc(path); nif, shapes = load_mesh(path)
    by = {s['name']: s for s in shapes}; nodes = node_index(D); shp = shape_index(D)
    bone_xf = bone_table(nif, shapes)
    assert not any(n.startswith('psk_') for n in nodes), 'already v4'
    flags = parse_node(D.blocks[nodes['sk_back1']][1])['flags']
    # rig on the skirt surface: axis straight down through the skirt's centre
    P_all = np.vstack([np.array(by[n]['positions']) for n in ('Skirt Lower', 'Skirt Upper')])
    yc = float(np.median(P_all[:, 1])); xc = float(np.median(P_all[:, 0]))
    z0 = SKIRT_ROWS_Z[0]
    rig = ClothRig('psk', SKIRT_COLS, origin=(xc, yc, z0), axis=(0, 0, -1), ref=(0, -1, 0),
                   parent='NPC Pelvis [Pelv]', rows_t=[z0 - z for z in SKIRT_ROWS_Z], spacing_t=5.0)
    rig.fit(P_all, np.ones(len(P_all), bool))
    print('   centre x%.1f y%.1f; radius by row: %s' % (xc, yc, ' '.join('%.0f' % r for r in np.nanmean(rig.radius, axis=1))))
    # old Meadowlark chain off the pelvis
    old = {n for n in nodes if re.match(r'sk_[A-Za-z]+\d(\.[lr])?$', n)}
    n_det = detach(D, nodes, 'NPC Pelvis [Pelv]', old)
    print('   detached %d old chain roots (%d old chain nodes)' % (n_det, len(old)))
    add_rig_nodes(D, nodes, bone_xf, rig, flags)
    for name in SKIRT_SHAPES:
        s = by[name]; P = np.array(s['positions'])
        rw = rig.weights(P)
        new_w = []
        for w, r_w in zip(s['weight_map'], rw):
            d = sum(v for b, v in w.items() if b.startswith('sk_'))
            base = {b: v for b, v in w.items() if not b.startswith('sk_')}
            new_w.append(blend(r_w, base, d))
        nb = reskin(D, nodes, bone_xf, s, shp[name], new_w, 49)
        print('   %-13s %d verts -> %d bones | %s' % (name, len(P), nb, stats(new_w, 'psk')))
    finish(D, path, apply, SKIRT_SHAPES + ['CollButt'])


# ---------------------------------------------------------------- sleeves
def do_top(path, apply):
    print('=== TOP', path)
    D = Doc(path); nif, shapes = load_mesh(path)
    by = {s['name']: s for s in shapes}; nodes = node_index(D); shp = shape_index(D)
    bone_xf = bone_table(nif, shapes)
    if any(n.startswith('slv') for n in nodes):
        print('   already v4 - verifying against the backup only')
        return verify_only(path, ['Sleeves', 'Cube'])
    flags = parse_node(D.blocks[nodes['sl_1a1']][1])['flags']
    s = by['Sleeves']; P = np.array(s['positions']); wm = s['weight_map']
    new_w = [None] * len(P)
    for side, cfg in SLEEVES.items():
        oldb = set(cfg['old'])
        d = np.array([sum(v for b, v in w.items() if b in oldb) for w in wm])
        Rf, Tf = world_of(bone_xf, cfg['parent'])
        tip = cfg['hand'] if cfg['hand'] in bone_xf else cfg['twist']
        _, Tt = world_of(bone_xf, tip)
        u = Tt - Tf
        side_mask = (P[:, 0] < 0) if side == 'L' else (P[:, 0] > 0)
        dyn = side_mask & (d > 0.5)
        rig0 = ClothRig(cfg['prefix'], SLEEVE_COLS, origin=Tf, axis=u, ref=(0, 0, -1), parent=cfg['parent'], rows_t=[0], spacing_t=1)
        t, r, phi = rig0.cyl(P[dyn])
        t_lo, t_hi = np.percentile(t, 5), np.percentile(t, 95)
        rows_t = [t_lo - 1.5] + [t_lo + (t_hi - t_lo) * f for f in (0.15, 0.4, 0.65, 0.9)]
        rig = ClothRig(cfg['prefix'], SLEEVE_COLS, origin=Tf, axis=u, ref=(0, 0, -1), parent=cfg['parent'],
                       rows_t=rows_t, spacing_t=(t_hi - t_lo) / 4.0)
        rig.fit(P, side_mask & (d > 0.2))
        print('   %s sleeve: axis via %s, t %.1f..%.1f, rows_t %s, radius/row %s, dyn verts %d' % (
            side, tip, t_lo, t_hi, ['%.1f' % x for x in rows_t], ' '.join('%.0f' % x for x in np.nanmean(rig.radius, axis=1)), dyn.sum()))
        n_det = detach(D, nodes, cfg['parent'], {cfg['old'][0]})
        assert n_det == 1, (side, n_det)
        add_rig_nodes(D, nodes, bone_xf, rig, flags)
        rw = rig.weights(P[side_mask])
        for k, i in enumerate(np.where(side_mask)[0]):
            base = {b: v for b, v in wm[i].items() if b not in oldb}
            new_w[i] = blend(rw[k], base, float(d[i]))
    assert all(w is not None for w in new_w)
    nb = reskin(D, nodes, bone_xf, s, shp['Sleeves'], new_w)
    print('   Sleeves %d verts -> %d bones | L %s | R %s' % (len(P), nb, stats(new_w, 'slvL'), stats(new_w, 'slvR')))
    finish(D, path, apply, ['Sleeves', 'Cube'])


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    which = [a for a in sys.argv[1:] if a in ('skirt', 'top')] or ['skirt', 'top']
    if 'skirt' in which:
        for p in SKIRTS:
            do_skirt(p, apply)
    if 'top' in which:
        for p in TOPS:
            do_top(p, apply)
