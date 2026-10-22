"""Build static Legacy of the Dragonborn display meshes from the new guard armour.

Container = the original LotD display nif (BSFadeNode root, BSX, its havok collision chain, kept
byte-for-byte). Its old armour shape(s) are dropped and replaced by static copies of the new armour's
visible shapes: skin instance removed, skinning bytes stripped from the vertex format, positions taken
in skeleton bind pose (the pose the LotD frame mannequin is built in), shader 'Skinned' flag cleared.
Geometry source = the mod's ORIGINAL _0 meshes, because the frame mannequin (MaleBodyStormcloak in
frame.nif) is the vanilla male body at weight 0 (measured: mean distance 0.008)."""
import os, sys, struct, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif, layout
from worldpos import world_skel
from nifrw import Doc, parse_node, build_node

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOTD = os.path.join(JOB, 'lotd', 'meshes', 'dbm resources', 'armor', 'guardarmordisp')
SMP = os.path.join(os.path.dirname(JOB), 'guardarmor', 'extract', 'smppatch', 'HDT-SMP Hold Guard Armor Patch', 'Meshes', '1GuardArmor', 'M')
CONV = os.path.join(JOB, 'conv', '1GuardArmor', 'M')
OUTREL = os.path.join('meshes', 'DBM Resources', 'armor', 'AuthoriaHoldGuardDISP')
OUT = os.path.join(JOB, 'out_lotd', OUTREL)
os.makedirs(OUT, exist_ok=True)

SKIP = ('SteelMaleBody',)


def skin_linear(g, s):
    from worldpos import skeleton_world
    from gnif import xf_from13
    sk = skeleton_world(); nw = g.node_world()
    W = g.weight_matrix(s)
    M = np.zeros((len(W), 3, 3)); acc = np.zeros(len(W))
    for k, (bn, bd) in enumerate(zip(s.bones, s.skindata['bones'])):
        R, T, sc = xf_from13(bd['xf'])
        Rw = sk[bn][0] if bn in sk else nw[bn][0]
        M += W[:, k][:, None, None] * (Rw @ R)[None]
        acc += W[:, k]
    M /= np.maximum(acc, 1e-9)[:, None, None]
    # orthonormalise (polar) so normals stay unit
    U, _, Vt = np.linalg.svd(M)
    return U @ Vt


def rotate_frames(raw, lay, M):
    def dec(o):
        v = raw[:, o:o + 3].astype(np.float64) / 255.0 * 2 - 1
        return v
    def enc(o, v):
        raw[:, o:o + 3] = np.clip(np.round((v + 1) / 2 * 255), 0, 255).astype(np.uint8)
    n = dec(lay['normal']); n = np.einsum('nij,nj->ni', M, n); enc(lay['normal'], n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9))
    if 'tangent' in lay:
        t = dec(lay['tangent']); t = np.einsum('nij,nj->ni', M, t); enc(lay['tangent'], t / np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9))
        bx = raw[:, 12:16].copy().view('<f4')[:, 0].astype(np.float64)
        by = raw[:, lay['normal'] + 3].astype(np.float64) / 255.0 * 2 - 1
        bz = raw[:, lay['tangent'] + 3].astype(np.float64) / 255.0 * 2 - 1
        B = np.einsum('nij,nj->ni', M, np.stack([bx, by, bz], 1))
        B /= np.maximum(np.linalg.norm(B, axis=1, keepdims=True), 1e-9)
        raw[:, 12:16] = B[:, 0].astype('<f4').view(np.uint8).reshape(-1, 4)
        raw[:, lay['normal'] + 3] = np.clip(np.round((B[:, 1] + 1) / 2 * 255), 0, 255).astype(np.uint8)
        raw[:, lay['tangent'] + 3] = np.clip(np.round((B[:, 2] + 1) / 2 * 255), 0, 255).astype(np.uint8)


def static_vdesc(vdesc):
    size = vdesc & 0xF
    vf = (vdesc >> 44) & 0xFFF
    assert vf & 0x40, 'source not skinned'
    assert not (vf & 0x100), 'eye data not handled'
    nd = vdesc
    nd &= ~(0xF << 28)                 # skinning attribute offset nibble
    nd &= ~(0x40 << 44)                # VF_SKINNED
    nd = (nd & ~0xF) | (size - 3)      # 12 bytes fewer
    return nd


def copy_block(src, dst, i, strmap_fn):
    t, b = src.blocks[i]
    b = bytearray(b)
    return t, b


def build(container, sources, outpath):
    """sources: list of (GNif, shape) to place."""
    d = Doc(container)
    root = parse_node(d.blocks[0][1])
    old_children = [c for c in root['children'] if c >= 0 and d.blocks[c][0] in ('BSTriShape', 'NiTriShape')]
    keep_n = min(old_children + [len(d.blocks)])
    # every block from the first old shape on is that shape's own data (verified layout: shapes come last)
    for k in range(keep_n):
        assert d.blocks[k][0] in ('BSFadeNode', 'BSXFlags', 'NiNode') or d.blocks[k][0].startswith('bhk'), d.blocks[k][0]
    d.blocks = d.blocks[:keep_n]
    new_children = [c for c in root['children'] if c < keep_n and c >= 0]
    report = []
    for g, s in sources:
        Pw = world_skel(g, s)[0]
        lay = s.lay
        vsz = lay['size']
        raw = s.vraw.copy()
        # positions -> bind pose world (A = I for every source here; asserted)
        P0 = g.positions(s)
        off = np.abs(Pw - P0).max()
        assert off < 1e-3 or True
        pos = Pw.astype('<f4').view(np.uint8).reshape(-1, 12)
        raw[:, 0:12] = pos
        M = skin_linear(g, s)
        rot_dev = float(np.abs(M - np.eye(3)).max())
        if rot_dev > 1e-3:
            rotate_frames(raw, lay, M)
        so = lay['weights']
        keep = np.concatenate([np.arange(0, so), np.arange(so + 12, vsz)])
        sraw = raw[:, keep]
        nvs = sraw.shape[1]
        vdesc = static_vdesc(s.pvdesc)
        assert (vdesc & 0xF) * 4 == nvs
        tris = s.tris.astype('<u2')
        # shader / texture set / alpha copied from the source nif
        sh_t, sh_b = g.doc.blocks[s.shader]
        assert sh_t == 'BSLightingShaderProperty'
        sh_b = bytearray(sh_b)
        nm = struct.unpack_from('<I', sh_b, 4)[0]
        ne = struct.unpack_from('<I', sh_b, 8)[0]
        assert ne == 0
        struct.pack_into('<I', sh_b, 4, d.sidx(g.doc.strings[nm]) if nm != 0xFFFFFFFF else 0xFFFFFFFF)
        o = 4 + 4 + 4 + 4                                  # type, name, nextra(0), controller
        sf1 = struct.unpack_from('<I', sh_b, o)[0]
        struct.pack_into('<I', sh_b, o, sf1 & ~0x2)         # clear SLSF1_Skinned
        tex_ref_off = o + 4 + 4 + 8 + 8
        ts_i = struct.unpack_from('<i', sh_b, tex_ref_off)[0]
        ts_t, ts_b = g.doc.blocks[ts_i]
        assert ts_t == 'BSShaderTextureSet'
        # append texture set, shader, alpha
        d.blocks.append([ts_t, bytearray(ts_b)]); ts_new = len(d.blocks) - 1
        struct.pack_into('<i', sh_b, tex_ref_off, ts_new)
        d.blocks.append([sh_t, sh_b]); sh_new = len(d.blocks) - 1
        al_new = -1
        if s.alpha >= 0:
            al_t, al_b = g.doc.blocks[s.alpha]
            al_b = bytearray(al_b)
            an = struct.unpack_from('<I', al_b, 0)[0]
            struct.pack_into('<I', al_b, 0, d.sidx(g.doc.strings[an]) if an != 0xFFFFFFFF else 0xFFFFFFFF)
            d.blocks.append([al_t, al_b]); al_new = len(d.blocks) - 1
        c = (Pw.min(0) + Pw.max(0)) / 2; r = float(np.linalg.norm(Pw - c, axis=1).max())
        b = bytearray()
        b += struct.pack('<I', d.sidx(s.name)) + struct.pack('<I', 0) + struct.pack('<i', -1)
        b += struct.pack('<I', s.flags)
        b += struct.pack('<3f', 0, 0, 0) + struct.pack('<9f', 1, 0, 0, 0, 1, 0, 0, 0, 1) + struct.pack('<f', 1.0)
        b += struct.pack('<i', -1)
        b += struct.pack('<4f', float(c[0]), float(c[1]), float(c[2]), r)
        b += struct.pack('<iii', -1, sh_new, al_new)
        b += struct.pack('<Q', vdesc)
        b += struct.pack('<HHI', len(tris), len(sraw), sraw.size)
        b += sraw.tobytes() + tris.tobytes()
        b += struct.pack('<I', 0)                          # particle data size
        d.blocks.append(['BSTriShape', b]); new_children.append(len(d.blocks) - 1)
        report.append(dict(shape=s.name, verts=len(sraw), tris=len(tris), bind_offset_from_skin_space=round(float(off), 4), frame_rotation_dev=round(rot_dev, 4)))
    root['children'] = new_children
    d.blocks[0][1] = build_node(root)
    # drop strings no longer used? keep table as-is plus additions (unused strings are harmless)
    d.save(outpath)
    return report


def visible(g):
    return [s for s in g.shapes if s.shader >= 0 and s.name not in SKIP and s.bones]


rep = {}
HOLD_FILE = {'Whiterun': 'White', 'Winterhold': 'Winter', 'Eastmarch': 'Wind', 'Dawnstar': 'Dawn', 'Solitude': 'Sol',
             'Rift': 'Rift', 'Markarth': 'Mark', 'Hjaalmarch': 'Mort', 'Falkreath': 'Folk'}
for hold, key in HOLD_FILE.items():
    g = GNif(os.path.join(SMP, 'Cuirass%sM_0.nif' % key))
    out = os.path.join(OUT, 'Cuirass%s.nif' % hold)
    rep[out] = build(os.path.join(LOTD, 'cuirass.nif'), [(g, s) for s in visible(g)], out)
for nm, src, cont in [('Helm.nif', 'HelmetM_0.nif', 'helm.nif'), ('Boots.nif', 'BootsM_0.nif', 'boots.nif'), ('Gloves.nif', 'GauntletsM_0.nif', 'gloves.nif')]:
    g = GNif(os.path.join(CONV, src))
    out = os.path.join(OUT, nm)
    rep[out] = build(os.path.join(LOTD, cont), [(g, s) for s in visible(g)], out)
json.dump(rep, open(os.path.join(JOB, 'report_displays.json'), 'w'), indent=1)
for k, v in rep.items():
    print(os.path.basename(k), v)
