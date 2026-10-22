"""3BA conversion (convert_f3ba.py output) -> UBE 2.0 (the !UBE lane), 2026-10-22 prototype.

Cloth: moved by DayOnly's own 3BA -> UBE garment move, sampled from the user's 'Authoria - UBE Converter Output'
(build_ube_field.py -> ube_field_vox.npz); points with no nearby sample fall back to the 3BA body -> UBE body nearest-
surface move. Then cleared off the UBE body, skinned from the UBE body (its own physics bones), and every UBE slider
copied on -> .tri + BODYTRI. Skin: the in-game UBE body (!UBE\\Body\\femalebody_tangent) kept where the 3BA skin was.
usage: python -I convert_ube.py <3BA _1.nif> <out mesh dir> <tri data path>"""
import os, sys, xml.etree.ElementTree as ET
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\skill\scripts")
import bslib as B
from smpkit import core as C
from convert_f3ba import vnormals, write_tri, neighbours, smooth_field, BA3_NIF

UBE = r"C:\1. AUTHORIA\mods\Ultimate Body Enhancer\CalienteTools\Bodyslide"
UBE_OSP = UBE + r"\SliderSets\UBE SE 2.0 Release Body.osp"
UBE_OSD = UBE + r"\ShapeData\UBE SE 2.0 Release Body\UBE SE 2.0 Release Body.osd"
UBE_ZERO = UBE + r"\ShapeData\UBE SE 2.0 Release Body\UBE SE 2.0 Release Body.nif"
UBE_GAME = r"C:\1. AUTHORIA\mods\Authoria - Bodyslide Output - UBE\meshes\!UBE\Body\femalebody_tangent_%s.nif"
FIELD_R = 3.0          # field samples within this radius count
CLEAR = 0.35
SKIN_MARGIN = 1.2


def ube_sliders(n):
    ss = ET.parse(UBE_OSP).getroot().find('SliderSet')
    _, _, ent = C.read_osd(UBE_OSD); E = dict(ent); out = {}
    for sl in ss.findall('Slider'):
        d = next((x for x in sl.findall('Data') if x.get('target') == 'BaseShape'), None)
        if d is None: continue
        arr = np.zeros((n, 3))
        for i, x in E.get(d.text.split('\\', 1)[1], {}).items(): arr[i] = x
        if np.abs(arr).max() > 0: out[sl.get('name')] = arr
    return out


def main(src1, out_dir, tri_rel, log=print):
    stem = os.path.basename(src1)[:-6]
    skel = B.skeleton_G(C)
    nif, shapes = C.load(src1)
    cloth = [s for s in shapes if s.name != '3BA']
    has_skin = any(s.name == '3BA' for s in shapes)
    _, zs = C.load(UBE_ZERO); zero, _ = B.bind_pose(C, zs[0], skel)
    game = {}
    for w in '01':
        _, gs = C.load(UBE_GAME % w); game[w] = gs[0]
    ub = game['1']; up = {w: B.bind_pose(C, game[w], skel)[0] for w in '01'}
    ut = ub.tris; un = vnormals(up['1'], ut)
    skel.update({nm: np.linalg.inv(C.tb2m(xf)) for nm, xf in ub.s2b.items()})
    fz = np.load(os.path.join(HERE, 'ube_field_vox.npz')); FP, FD = fz['P'], fz['D']
    _, b3 = C.load(BA3_NIF); body3 = next(s for s in b3 if s.name == '3BA'); C.to_world([body3])
    # body -> body fallback move: each 3BA body point to the nearest UBE zero point
    j3 = B.knn(zero, body3.pos, 1)[1][:, 0]; bb_move = zero[j3] - body3.pos
    sliders = ube_sliders(len(zero))
    done = []
    for G in cloth:
        gp3, _ = B.bind_pose(C, G, skel)
        d, j = B.knn(FP, gp3, 12)
        wv = np.where(d < FIELD_R, 1.0 / np.maximum(d, 0.1) ** 2, 0.0)
        cover = wv.sum(1) > 0
        fmove = np.einsum('nk,nkc->nc', wv, FD[j]) / np.maximum(wv.sum(1, keepdims=True), 1e-9)
        bmove, _ = B.transfer(body3.pos, bb_move, gp3, k=10)
        move = np.where(cover[:, None], fmove, bmove)
        move = smooth_field(move, neighbours(len(gp3), G.tris), 4)
        gp = gp3 + move
        d1, j1 = B.knn(up['1'], gp, 1); d1 = d1[:, 0]; j1 = j1[:, 0]
        depth = np.einsum('ij,ij->i', gp - up['1'][j1], un[j1])
        feet = gp[:, 2] < 13.0
        push = np.where((d1 < 4.0) & (depth < CLEAR) & ~feet, CLEAR - depth, 0.0)
        gp = gp + un[j1] * push[:, None]
        log('  %s: %d points, field covers %d, move mean %.2f max %.2f, pushed out %d' % (
            G.name, len(gp), cover.sum(), np.linalg.norm(move, axis=1).mean(), np.linalg.norm(move, axis=1).max(), (push > 0).sum()))
        dw, jw = B.knn(up['1'], gp, 4)
        wv = 1.0 / np.maximum(dw, 0.05) ** 2; wv /= wv.sum(1, keepdims=True)
        gw = []
        for i in range(len(gp)):
            if feet[i]:
                gw.append(C.top4(G.w[i])); continue
            acc = {}
            for k in range(4):
                for bnm, x in ub.w[jw[i, k]].items(): acc[bnm] = acc.get(bnm, 0) + x * wv[i, k]
            gw.append(C.top4(acc))
        dm, jm = B.knn(zero, gp, 6)
        wm = 1.0 / np.maximum(dm, 0.05) ** 2; wm /= wm.sum(1, keepdims=True)
        gmorph = {nm: np.einsum('nk,nkc->nc', wm, arr[jm]) for nm, arr in sliders.items()}
        pres = {w: np.einsum('nk,nkc->nc', wm, (up[w] - zero)[jm]) for w in '01'}   # in-game body vs zero, per weight
        done.append((G, gp - pres['1'], gw, gmorph, pres))
    keep_t = np.zeros(len(ut), bool)
    if has_skin:
        s3 = next(s for s in shapes if s.name == '3BA'); sp, _ = B.bind_pose(C, s3, skel)
        sp = sp + B.transfer(body3.pos, bb_move, sp, k=6)[0]
        keep_t = (B.knn(sp, up['1'], 1)[0][:, 0] < SKIN_MARGIN)[ut].any(1)
    vk = np.unique(ut[keep_t]); rm = -np.ones(len(zero), int); rm[vk] = np.arange(len(vk))
    log('  UBE skin: kept %d of %d triangles' % (keep_t.sum(), len(ut)))
    os.makedirs(out_dir, exist_ok=True)
    for w in '01':
        out = os.path.join(out_dir, stem + '_' + w + '.nif')
        W = C.Writer(nif, out); W.skel_G = skel
        for G, g0, gw, gmorph, pres in done:
            W.emit(G.name, g0 + pres[w], G.uv, G.norm, G.tris, G.s.flags, C.part_ids(G, [G]), gw, ub.s2b, shader_from=G)
        if len(vk):
            W.emit('BaseShape', up[w][vk], ub.uv[vk], ub.norm[vk] if ub.norm is not None else None, rm[ut[keep_t]],
                   game[w].s.flags, C.part_ids(ub, [ub])[keep_t], [ub.w[i] for i in vk], ub.s2b, shader_from=game[w])
        C.NiStringExtraData.New(W.out, name='BODYTRI', string_value=tri_rel, parent=W.out.root)
        W.out.save(); log('  wrote %s' % out)
    tri = [(G.name, gm) for G, g0, gw, gm, pr in done] + ([('BaseShape', {nm: a[vk] for nm, a in sliders.items()})] if len(vk) else [])
    write_tri(os.path.join(out_dir, stem + '.tri'), tri)
    log('  wrote %s.tri (%d sliders)' % (stem, len(sliders)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
