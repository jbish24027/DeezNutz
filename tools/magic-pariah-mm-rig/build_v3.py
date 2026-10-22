"""Magic Pariah skirt, tune v3 (2026-09-06). User: "skirt flowier, especially the back; butt pokes
through; physics looser and starting higher up in the back".

Per skirt nif (all three lanes: ShapeData, BodySlide-built _0/_1, converter !UBE _0/_1):
  1. weights (Skirt Lower / Skirt Upper / MMSkirtProxy): the v2 rule handed body weight to the
     chain below z 60..68 everywhere. v3 raises that hand-over and shifts row-1 (static anchor)
     weight into row 2 so the flap hinges higher: back z 71..76 / shift below 73, front z 63..70 /
     shift below 66, blended by the vertex's y (front..back).
  2. a new per-vertex collider 'CollButt' cut from the SAME lane's body (the top's body shape),
     rear + sides of the hips z 54..78, skinned as the body is (pelvis / thighs / butt bones), so the
     skirt has something to drape over where the butt is.
  3. the converter's placeholder shaders on the three collision-only shapes are stripped (the
     purple-square trap) and their flags set to MM's 0xE.
The xml (make_xml.py TUNE='v3') gets the CollButt shape, the two butt bones and looser joints.

usage: python build_v3.py [--apply]     (dry run by default; backups <nif>.bak-v2-20260906)
"""
import os, re, shutil, struct, sys
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\ube-neck-pin\from-bodypin3")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifparse import load_mesh
from nifrw import Doc, rebuild, parse_node, build_node, parse_shape_hdr, build_shape, parse_dismember
from graft import (RESKIN, PROXY_NAME, BODY_PART, bone_table, node_index, shape_index,
                   partition_raw, build_skin, skin_offset)

TAG = 'bak-v2-20260906'
MODS = r"C:\1. AUTHORIA\mods"
UBE = MODS + r"\Authoria - UBE Converter Output - Magic Pariah\meshes\!UBE\clothes\magic pariah"
BS = MODS + r"\Authoria - Bodyslide Output - UBE\Meshes\clothes\magic pariah"
SD = MODS + r"\Magic Pariah - Meadowlark Physics\CalienteTools\BodySlide\ShapeData"
LANES = [
    (UBE + r"\magic pariah skirt HDT_0.nif", UBE + r"\Magic Pariah Top_0.nif"),
    (UBE + r"\magic pariah skirt HDT_1.nif", UBE + r"\Magic Pariah Top_1.nif"),
    (BS + r"\Magic Pariah Skirt HDT_0.nif", BS + r"\Magic Pariah Top_0.nif"),
    (BS + r"\Magic Pariah Skirt HDT_1.nif", BS + r"\Magic Pariah Top_1.nif"),
    (SD + r"\Magic Pariah Skirt HDT\Magic Pariah Skirt HDT.nif", SD + r"\Magic Pariah Top\Magic Pariah Top.nif"),
]
COLL_ALL = ['CollThigh', 'CollCalves', PROXY_NAME]
BUTT_NAME = 'CollButt'
BUTT_BONES = ['NPC Pelvis [Pelv]', 'NPC L Thigh [LThg]', 'NPC R Thigh [RThg]', 'NPC L Butt', 'NPC R Butt',
              'NPC L RearThigh', 'NPC R RearThigh', 'NPC L FrontThigh', 'NPC R FrontThigh', 'NPC Spine [Spn0]']
ARM_WORDS = ('Forearm', 'UpperArm', 'Hand', 'Clavicle', 'Finger')
CELL = 1.3          # voxel decimation of the collider (sphere spacing < 2 * margin 1.2)
MIN_W = 0.02

# ---------------------------------------------------------------- v3 weight rule
def clamp(v):
    return 0.0 if v < 0 else 1.0 if v > 1 else v

def lerp(a, b, t):
    return a + (b - a) * t

def retune_v3(wd, pos):
    x, y, z = pos
    t = clamp((-y - 2.0) / 6.0)              # 0 = front/side (y >= -2), 1 = back (y <= -8)
    z_none = lerp(63.0, 71.0, t)             # below: no body weight, chain owns the vertex
    z_full = lerp(70.0, 75.0, t)             # above: weights untouched (waistband on the pelvis)
    z_shift = lerp(66.0, 73.0, t)            # below: row-1 (static) weight moves to row 2
    out = dict(wd)
    chain = {b: w for b, w in out.items() if b.startswith('sk_')}
    body = {b: w for b, w in out.items() if not b.startswith('sk_')}
    if body and chain:
        f = clamp((z - z_none) / (z_full - z_none))
        if f < 1.0:
            keep = sum(body.values()) * f
            out = {b: w * f for b, w in body.items() if w * f > 0.005}
            csum = sum(chain.values())
            for b, w in chain.items():
                out[b] = w / csum * (1.0 - keep)
    g = clamp((z_shift - z) / 6.0)           # 1 = all of row 1 handed to row 2
    if g > 0:
        moved = {}
        for b, w in list(out.items()):
            m = re.match(r'(sk_[A-Za-z]+)1(\.[lr])?$', b)
            if m:
                tgt = '%s2%s' % (m.group(1), m.group(2) or '')
                moved[tgt] = moved.get(tgt, 0.0) + w * g
                out[b] = w * (1.0 - g)
        for b, w in moved.items():
            out[b] = out.get(b, 0.0) + w
    out = {b: w for b, w in out.items() if w >= MIN_W}
    tot = sum(out.values())
    return {b: w / tot for b, w in out.items()}


def band_report(name, positions, before, after):
    P = np.array(positions)
    print('   %-13s  back:   z-band  body%%  row1%%  row2%%   ->   body%%  row1%%  row2%%   n' % name)
    for z0 in range(56, 80, 4):
        m = (P[:, 2] >= z0) & (P[:, 2] < z0 + 4) & (P[:, 1] < -6)
        if m.sum() < 3:
            continue
        def stats(wm):
            body = r1 = r2 = tot = 0.0
            for i in np.where(m)[0]:
                for b, w in wm[i].items():
                    tot += w
                    if not b.startswith('sk_'): body += w
                    elif re.match(r'sk_[A-Za-z]+1(\.|$)', b): r1 += w
                    elif re.match(r'sk_[A-Za-z]+2(\.|$)', b): r2 += w
            return 100 * body / tot, 100 * r1 / tot, 100 * r2 / tot
        a = stats(before); c = stats(after)
        print('                         %2d-%2d  %5.1f  %5.1f  %5.1f   ->   %5.1f  %5.1f  %5.1f  %4d' % (z0, z0 + 4, *a, *c, m.sum()))



def all_triangles(raw):
    """Every triangle of an SSE NiSkinPartition, across all partitions (global vertex indices)."""
    np_, dsize, vsize = struct.unpack_from('<III', raw, 0)
    o = 20 + dsize
    out = []
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
            out += [struct.unpack_from('<HHH', raw, o + 6 * i) for i in range(nt)]; o += 6 * nt
        if raw[o]: o += 1 + nwpv * nv
        else: o += 1
        o += 2 + 8 + 6 * nt
    assert o == len(raw), (o, len(raw))
    return out

# ---------------------------------------------------------------- collider from the body
def extract_butt(top_path):
    nif, shapes = load_mesh(top_path)
    body = max(shapes, key=lambda s: len(s['positions']))
    P = np.array(body['positions']); W = body['weight_map']
    D = Doc(top_path); shp = shape_index(D)
    h = parse_shape_hdr(D.blocks[shp[body['name']]][1]); dm = parse_dismember(D.blocks[h['skin']][1])
    tris = all_triangles(D.blocks[dm['part']][1])
    sel = []
    for i in range(len(P)):
        if P[i, 1] < 2.0 and 54.0 <= P[i, 2] <= 78.0 and abs(P[i, 0]) < 19.0:
            if any(any(a in b for a in ARM_WORDS) for b in W[i]):
                continue
            sel.append(i)
    seen = set(); keep = []
    for i in sel:
        key = tuple(np.floor(P[i] / CELL).astype(int))
        if key not in seen:
            seen.add(key); keep.append(i)
    idx = {v: k for k, v in enumerate(keep)}
    ktris = [tuple(idx[v] for v in t) for t in tris if all(v in idx for v in t)]
    wmap = []
    for i in keep:
        w = {b: v for b, v in W[i].items() if b in BUTT_BONES}
        tot = sum(w.values())
        wmap.append({b: v / tot for b, v in w.items()})
    xf = bone_table(nif, shapes)
    return body['name'], P[keep], wmap, ktris, xf


def vertex_buffer(positions, vdesc):
    vsize, soff = skin_offset(vdesc)
    assert vsize == 40 and soff == 28, (vsize, soff)     # float pos + bitanX, uv, nrm, tan, skin
    vb = bytearray()
    for p in positions:
        vb += struct.pack('<4f', float(p[0]), float(p[1]), float(p[2]), 0.0)
        vb += b'\x00\x00\x00\x00'                       # uv (half2)
        vb += bytes([128, 128, 255, 0])                 # normal + bitangent y
        vb += bytes([255, 128, 128, 0])                 # tangent + bitangent z
        vb += b'\x00' * 12                              # skin slots, filled by build_skin
    return bytes(vb)


# ---------------------------------------------------------------- per-nif job
def process(skirt_path, top_path, apply):
    print('=== ', skirt_path)
    D = Doc(skirt_path)
    nif, shapes = load_mesh(skirt_path)
    by = {s['name']: s for s in shapes}
    nodes = node_index(D); shp = shape_index(D)
    root = D.roots[0]
    assert BUTT_NAME not in shp, 'already has ' + BUTT_NAME
    bone_xf = bone_table(nif, shapes)

    # 1. weights
    for name in RESKIN + [PROXY_NAME]:
        s = by[name]; si = shp[name]
        h = parse_shape_hdr(D.blocks[si][1]); dm = parse_dismember(D.blocks[h['skin']][1])
        dsize, vsize, vdesc, vbuf, tris = partition_raw(D, dm['part'])
        new_w = [retune_v3(w, p) for w, p in zip(s['weight_map'], s['positions'])]
        band_report(name, s['positions'], s['weight_map'], new_w)
        for w in new_w:
            for b in w:
                assert b in nodes and b in bone_xf, b
        dis_fn, sd_b, sp_b, bones, pv = build_skin(D, nodes, bone_xf, s['positions'], vbuf, vdesc, tris, new_w, BODY_PART)
        D.blocks[dm['data']][1] = bytearray(sd_b)
        D.blocks[dm['part']][1] = bytearray(sp_b)
        D.blocks[h['skin']][1] = dis_fn(dm['data'], dm['part'])

    # 2. the butt collider
    body_name, bpos, bw, btris, top_xf = extract_butt(top_path)
    for b in BUTT_BONES:
        if b in top_xf and b not in bone_xf:
            bone_xf[b] = top_xf[b]
    used = sorted({b for w in bw for b in w})
    rn = parse_node(D.blocks[root][1])
    for b in used:
        if b not in nodes:
            nd = dict(name=D.sidx(b), extra=[], ctrl=-1, flags=0x8000E, trans=(0.0, 0.0, 0.0),
                      rot=(1, 0, 0, 0, 1, 0, 0, 0, 1), scale=1.0, coll=-1, children=[], effects=[])
            D.blocks.append(['NiNode', build_node(nd)])
            nodes[b] = len(D.blocks) - 1
            rn['children'].append(nodes[b])
            print('   created flat node', b)
        assert b in bone_xf, 'no bind transform for ' + b
    ref_h = parse_shape_hdr(D.blocks[shp['CollThigh']][1])
    vdesc = ref_h['vdesc']
    vbuf = vertex_buffer(bpos, vdesc)
    dis_fn, sd_b, sp_b, bones, pv = build_skin(D, nodes, bone_xf, [tuple(p) for p in bpos], vbuf, vdesc, btris, bw, BODY_PART)
    D.blocks.append(['NiSkinData', bytearray(sd_b)]); di = len(D.blocks) - 1
    D.blocks.append(['NiSkinPartition', bytearray(sp_b)]); pi = len(D.blocks) - 1
    D.blocks.append(['BSDismemberSkinInstance', dis_fn(di, pi)]); si = len(D.blocks) - 1
    c = (bpos.min(0) + bpos.max(0)) / 2; rad = float(np.linalg.norm(bpos - c, axis=1).max())
    h2 = dict(ref_h); h2['name'] = D.sidx(BUTT_NAME); h2['extra'] = []; h2['ctrl'] = -1; h2['coll'] = -1
    h2['flags'] = 0xE; h2['bound'] = (float(c[0]), float(c[1]), float(c[2]), rad)
    h2['skin'] = si; h2['shader'] = -1; h2['alpha'] = -1
    D.blocks.append(['BSTriShape', build_shape(h2)]); shi = len(D.blocks) - 1
    rn['children'].append(shi)
    D.blocks[root][1] = build_node(rn)
    print('   %s from %s %r: %d spheres, %d tris, bones %s' % (BUTT_NAME, os.path.basename(top_path), body_name, len(bpos), len(btris), bones))

    # 3. shader-less collision shapes (the converter's purple-square placeholders)
    for name in COLL_ALL:
        hh = parse_shape_hdr(D.blocks[shp[name]][1])
        if hh['shader'] >= 0 or hh['flags'] != 0xE:
            print('   %s: shader %d -> none, flags 0x%X -> 0xE' % (name, hh['shader'], hh['flags']))
            hh['shader'] = -1; hh['flags'] = 0xE
            D.blocks[shp[name]][1] = build_shape(hh)

    out, refmap = rebuild(D)
    if not apply:
        print('   (dry run) would write %d blocks' % len(out.blocks))
        return
    bak = skirt_path + '.' + TAG
    if not os.path.exists(bak):
        shutil.copy2(skirt_path, bak)
    out.save(skirt_path)
    # verify against the backup
    nifA, shA = load_mesh(bak); nifB, shB = load_mesh(skirt_path)
    A = {s['name']: s for s in shA}; B = {s['name']: s for s in shB}
    assert set(B) == set(A) | {BUTT_NAME}, (set(A), set(B))
    for name in A:
        assert np.allclose(np.array(A[name]['positions']), np.array(B[name]['positions'])), name
        assert all(abs(sum(w.values()) - 1) < 1e-3 for w in B[name]['weight_map']), name
    assert len(B[BUTT_NAME]['positions']) == len(bpos)
    xml = [out.strings[struct.unpack_from('<I', b, 4)[0]] for t, b in out.blocks if t == 'NiStringExtraData']
    print('   written + verified: %d blocks, extra strings %s' % (len(out.blocks), xml))


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    for skirt, top in LANES:
        process(skirt, top, apply)
