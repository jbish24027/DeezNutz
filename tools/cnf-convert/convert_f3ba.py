"""Clothes of the Northern Folk -> CBBE 3BA (women), 2026-10-22 prototype (Fralia's Black Hardanger Viking attire).

What it does, per garment mesh (vanilla-body CNF female mesh):
  1. conform: every garment point moves with the vanilla->CBBE body change at its nearest body points (BodySlide's own
     'Vanilla To CBBE' reference), the move field smoothed over the garment, then any point left inside the 3BA body is
     pushed out to a small clearance;
  2. body: the CNF vanilla body piece is replaced by the 3BA body (SE 3BBB Amazing '3BA' shape, its own weights), with
     triangles the garment fully hides removed;
  3. weights: garment skinning copied from the nearest 3BA body points (so 3BA breast/butt/belly physics bones follow);
  4. sliders: every 3BA slider copied onto the garment from the nearest body points -> a BodySlide .tri morph file
     (OBody / RaceMenu body morphs) linked by BODYTRI; _0/_1 built at the user's '- Zeroed Sliders -' preset (hidden
     sliders at their project defaults, as BodySlide does).
Sources are never touched. usage: python -I convert_f3ba.py <src _1.nif> <out mesh dir> <tri data path (Data-relative)>
"""
import os, sys, struct, xml.etree.ElementTree as ET
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\skill\scripts")
import bslib as B
from smpkit import core as C

BA3_OSP = B.BA3 + r"\SliderSets\SE 3BBB Amazing.osp"
BA3_SET = "CBBE 3BBB Body Amazing"
BA3_NIF = B.BA3 + r"\ShapeData\SE 3BBB Amazing\SE 3BBB Body Amazing v2.nif"
BA3_OSD = B.BA3 + r"\ShapeData\SE 3BBB Amazing\SE 3BBB Body Amazing v2.osd"
V2C_NIF = B.CBBE + r"\ShapeData\References\Vanilla To CBBE.nif"
V2C_OSD = B.CBBE + r"\ShapeData\References\Vanilla To CBBE.osd"
CLEAR = 0.35          # garment clearance over the 3BA body after conforming
SMOOTH_IT = 6         # Laplacian passes over the conform field
FEET_Z = 13.0         # below this (feet) a piece keeps its own foot/toe weights and is not pushed
SKIN_MARGIN = 2.5     # 3BA skin kept within this distance of the CNF author's visible skin piece
HIMBO_A = r"C:\1. AUTHORIA\mods\Highly Improved Male Body Overhaul -HIMBO- Vanilla Armors\CalienteTools\BodySlide\SliderSets\HIMBO Vanilla Refits.osp"
RES = r"C:\1. AUTHORIA\mods\BodySlide and Outfit Studio\CalienteTools\BodySlide\res"
# women -> CBBE 3BA; men -> HIMBO (the slider list of HIMBO's own vanilla-outfit refits, skin piece 'HIMBO - Body')
PROFILES = {
    'f3ba': dict(v2c_nif=V2C_NIF, v2c_osd=V2C_OSD, v2c_key='BaseShapeHRVanilla To CBBE', body_nif=BA3_NIF, body='3BA',
                 osp=BA3_OSP, set=BA3_SET, osd=BA3_OSD, skel=RES + r"\skeleton_female_sse.nif"),
    'mhimbo': dict(v2c_nif=B.HIMBO + r"\ShapeData\HIMBO Conversion\HIMBO - VAL.nif", v2c_osd=B.HIMBO + r"\ShapeData\HIMBO Conversion\HIMBO - VAL.osd",
                   v2c_key='HIMBO Conversion - VALVanilla to HIMBO', body_nif=B.HIMBO + r"\ShapeData\HIMBO Ref\HIMBO Ref - Vanilla Nude.nif",
                   body='HIMBO - Body', osp=HIMBO_A, set='HIMBO Vanilla - Body - Farm Clothes 1',
                   osd=B.HIMBO + r"\ShapeData\HIMBO Ref\HIMBO Ref - Vanilla Nude.osd", skel=RES + r"\skeleton_male_sse.nif"),
}


def neighbours(n, tris):
    nb = [set() for _ in range(n)]
    for a, b, c in tris:
        nb[a] |= {b, c}; nb[b] |= {a, c}; nb[c] |= {a, b}
    return [np.array(sorted(x), int) for x in nb]


def smooth_field(F, nb, it):
    for _ in range(it):
        F = np.array([F[i] * 0.5 + F[j].mean(0) * 0.5 if len(j) else F[i] for i, j in enumerate(nb)])
    return F


def vnormals(P, T):
    N = np.zeros_like(P); f = np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]])
    for k in range(3): np.add.at(N, T[:, k], f)
    return N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)


def body_sliders(P=None):
    """body slider list from the project: name -> (default value at weight 0, at weight 100, dense diff (n,3))"""
    P = P or PROFILES['f3ba']
    ss = next(s for s in ET.parse(P['osp']).getroot().findall('SliderSet') if s.get('name') == P['set'])
    _, _, ent = C.read_osd(P['osd']); E = dict(ent)
    n_body = len(B.shape(P['body_nif'], P['body'])[1].verts)
    out = {}
    for sl in ss.findall('Slider'):
        d = next((x for x in sl.findall('Data') if x.get('target') == P['body']), None)
        if d is None: continue
        key = d.text.split('\\', 1)[1]
        arr = np.zeros((n_body, 3))
        for i, x in E.get(key, {}).items(): arr[i] = x
        inv = sl.get('invert') == 'true'
        hidden = sl.get('hidden') == 'true'
        sm = float(sl.get('small', 0)) / 100 if hidden else 0.0     # '- Zeroed Sliders -': visible sliders at 0
        bg = float(sl.get('big', 0)) / 100 if hidden else 0.0
        if inv: sm, bg = 1 - sm, 1 - bg
        out[sl.get('name')] = (sm, bg, arr)
    return out


def write_tri(path, shapes):
    """shapes: [(shape name, {morph: dense (n,3) diff})] -> BodySlide 'PIRT' morph file (zero diffs dropped)."""
    parts = [b'PIRT', struct.pack('<H', len(shapes))]
    for sname, morphs in shapes:
        keep = [(m, d) for m, d in morphs.items() if np.abs(d).max() > 1e-5]
        e = sname.encode(); parts.append(bytes([len(e)]) + e + struct.pack('<H', len(keep)))
        for m, d in keep:
            idx = np.where(np.abs(d).max(1) > 1e-5)[0]
            mult = float(np.abs(d[idx]).max()) / 32767.0
            q = np.round(d[idx] / mult).astype('<i2')
            me = m.encode(); parts.append(bytes([len(me)]) + me + struct.pack('<fH', mult, len(idx)))
            rec = np.zeros(len(idx), dtype=np.dtype([('i', '<u2'), ('v', '<i2', 3)])); rec['i'] = idx; rec['v'] = q
            parts.append(rec.tobytes())
    parts.append(struct.pack('<H', 0))       # no UV morphs
    open(path, 'wb').write(b''.join(parts))


def is_skin(shp):
    return any('actors' + chr(92) + 'character' in (t or '').lower() for t in shp.tex[:1])


def conform(src_pts, tris, vb, vc, bp, near):
    """vanilla -> CBBE move (smoothed over the piece), then snapped onto the 3BA zero shape"""
    move, _ = B.transfer(vb, vc - vb, src_pts, k=10)
    if tris is not None and len(tris):
        move = smooth_field(move, neighbours(len(src_pts), tris), SMOOTH_IT)
    p = src_pts + move
    return p + B.transfer(vc, bp[near] - vc, p, k=6)[0], move


def main(src1, out_dir, tri_rel, prof='f3ba', log=print):
    P = PROFILES[prof]
    stem = os.path.basename(src1)[:-6]                  # ..._f / ..._m
    nif, shapes = C.load(src1)
    skel = B.skeleton_G(C, P['skel'])
    cloth = [s for s in shapes if not is_skin(s)]
    skin = [s for s in shapes if is_skin(s)]
    _, rsh = C.load(P['v2c_nif']); vb = B.bind_pose(C, rsh[0], skel)[0] if rsh[0].bones else B.world_verts(rsh[0].s)
    dv = B.read_osd(P['v2c_osd'])[P['v2c_key']]; vc = B.apply_diff(vb, dv)
    bnif, bshapes = C.load(P['body_nif']); body = next(s for s in bshapes if s.name == P['body'])
    C.to_world([body])
    bp = body.pos.copy(); bt = body.tris; bn = vnormals(bp, bt)
    near = B.knn(bp, vc, 1)[1][:, 0]
    sliders = body_sliders(P)
    skel.update({nm: np.linalg.inv(C.tb2m(xf)) for nm, xf in body.s2b.items()})
    done = []
    for G in cloth:
        gsrc, miss = B.bind_pose(C, G, skel)
        gp, move = conform(gsrc, G.tris, vb, vc, bp, near)
        d, j = B.knn(bp, gp, 1); d = d[:, 0]; j = j[:, 0]
        depth = np.einsum('ij,ij->i', gp - bp[j], bn[j])
        feet = gp[:, 2] < FEET_Z
        push = np.where((d < 4.0) & (depth < CLEAR) & ~feet, CLEAR - depth, 0.0)
        gp = gp + bn[j] * push[:, None]
        log('  %s: %d points, move mean %.2f max %.2f | pushed out %d (max %.2f) | feet zone %d | unbound %d' % (
            G.name, len(gp), np.linalg.norm(move, axis=1).mean(), np.linalg.norm(move, axis=1).max(), (push > 0).sum(),
            push.max(), feet.sum(), miss))
        # weights: nearest 3BA body points (3BA breast/butt/belly bones follow); the feet zone keeps its own foot bones
        dw, jw = B.knn(bp, gp, 4)
        wv = 1.0 / np.maximum(dw, 0.05) ** 2; wv /= wv.sum(1, keepdims=True)
        gw = []
        for i in range(len(gp)):
            if feet[i]:
                gw.append(C.top4(G.w[i])); continue
            acc = {}
            for k in range(4):
                for bnm, x in body.w[jw[i, k]].items(): acc[bnm] = acc.get(bnm, 0) + x * wv[i, k]
            gw.append(C.top4(acc))
        dm, jm = B.knn(bp, gp, 6)
        wm = 1.0 / np.maximum(dm, 0.05) ** 2; wm /= wm.sum(1, keepdims=True)
        gmorph = {nm: np.einsum('nk,nkc->nc', wm, arr[jm]) for nm, (sm, bg, arr) in sliders.items()}
        done.append((G, gp, gw, gmorph))
    # skin: the CNF author included body only where it shows. Keep the 3BA skin near that piece, drop the rest.
    keep_t = np.zeros(len(bt), bool)
    for VB in skin:
        vsrc, _ = B.bind_pose(C, VB, skel)
        vpos, _ = conform(vsrc, VB.tris, vb, vc, bp, near)
        keep_t |= (B.knn(vpos, bp, 1)[0][:, 0] < SKIN_MARGIN)[bt].any(1)
    vk = np.unique(bt[keep_t]); rm = -np.ones(len(bp), int); rm[vk] = np.arange(len(vk))
    log('  %s skin:' % P['body'] + ' kept %d of %d triangles (%d points) from %d CNF skin piece(s)' % (keep_t.sum(), len(bt), len(vk), len(skin)))
    bmorph = {nm: arr[vk] for nm, (sm, bg, arr) in sliders.items()}
    os.makedirs(out_dir, exist_ok=True)
    for wt in ('0', '1'):
        f = 1.0 if wt == '1' else 0.0
        val = {nm: sm + (bg - sm) * f for nm, (sm, bg, _) in sliders.items()}
        out = os.path.join(out_dir, stem + '_' + wt + '.nif')
        w = C.Writer(nif, out); w.skel_G = skel
        for G, gp, gw, gmorph in done:
            gpos = gp + sum(v * gmorph[nm] for nm, v in val.items())
            w.emit(G.name, gpos, G.uv, G.norm, G.tris, G.s.flags, C.part_ids(G, [G]), gw, body.s2b, shader_from=G)
        if len(vk):
            bpos = bp[vk] + sum(v * bmorph[nm] for nm, v in val.items())
            w.emit(P['body'], bpos, body.uv[vk], body.norm[vk] if body.norm is not None else None, rm[bt[keep_t]],
                   skin[0].s.flags, C.part_ids(body, [body])[keep_t], [body.w[i] for i in vk], body.s2b, shader_from=skin[0])
        C.NiStringExtraData.New(w.out, name='BODYTRI', string_value=tri_rel, parent=w.out.root)
        w.out.save()
        log('  wrote %s' % out)
    tri_shapes = [(G.name, gmorph) for G, gp, gw, gmorph in done] + ([(P['body'], bmorph)] if len(vk) else [])
    write_tri(os.path.join(out_dir, stem + '.tri'), tri_shapes)
    log('  wrote %s.tri (%d sliders, %d shapes)' % (stem, len(sliders), len(tri_shapes)))
    return out_dir


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], *(sys.argv[4:5]))
