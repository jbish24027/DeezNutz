"""Re-skin a grafted Magic Pariah skirt nif so the skirt swings on the bone chain.

The first graft copied Meadowlark's own weighting, in which the hip region of a floor-length
skirt follows the thighs. On the knee-length Magic Pariah skirt that region IS most of the skirt,
so it moved with the legs like a skinned mesh. Rule here: body-bone weight (pelvis / spine /
thighs) fades out between Z_FULL and Z_NONE and is handed to the chain bones instead.
Works on the BodySlide ShapeData nif and on built _0/_1 nifs alike (positions may be morphed;
weights are transferred from Meadowlark by nearest neighbour exactly as in graft.py).

usage: python retune.py <nif> [<nif> ...] [--apply]   (writes <nif>.bak-stiff-20260903 first)
"""
import os, shutil, struct, sys
import numpy as np
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\ube-neck-pin\from-bodypin3")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifparse import load_mesh
from nifrw import Doc, parse_shape_hdr, parse_dismember
from graft import (MM_NIF, SOURCE_SHAPES, PROXY_SRC, PROXY_NAME, RESKIN, BODY_PART, bone_table,
                   node_index, shape_index, partition_raw, build_skin, knn_transfer, prune_rows, sk_row)

Z_NONE = 60.0     # below this: no body-bone weight at all, the chain owns the vertex
Z_FULL = 68.0     # above this: weights untouched (waistband stays on the pelvis)
BODY_TAG = 'body'


def free_body(wd, z):
    f = min(1.0, max(0.0, (z - Z_NONE) / (Z_FULL - Z_NONE)))
    chain = {b: w for b, w in wd.items() if b.startswith('sk_')}
    body = {b: w for b, w in wd.items() if not b.startswith('sk_')}
    if not body or f >= 1.0 or not chain:
        return wd
    keep = sum(body.values()) * f
    out = {b: w * f for b, w in body.items() if w * f > 0.005}
    csum = sum(chain.values())
    for b, w in chain.items():
        out[b] = w / csum * (1.0 - keep)
    tot = sum(out.values())
    return {b: w / tot for b, w in out.items()}


def band_stats(positions, wmap, label):
    P = np.array(positions)
    print('   %-14s z-band   body%%  thigh%%  chain%%   (weight share)' % label)
    for z0 in range(36, 80, 6):
        m = (P[:, 2] >= z0) & (P[:, 2] < z0 + 6)
        if m.sum() < 5:
            continue
        body = thigh = chain = 0.0
        for i in np.where(m)[0]:
            for b, w in wmap[i].items():
                if b.startswith('sk_'): chain += w
                elif 'Thigh' in b: thigh += w
                else: body += w
        t = body + thigh + chain
        print('                  %2d-%2d   %5.1f   %5.1f   %5.1f   (%d verts)' % (z0, z0 + 6, 100 * body / t, 100 * thigh / t, 100 * chain / t, m.sum()))


def retune(path, apply):
    nif, shapes = load_mesh(path)
    by = {s['name']: s for s in shapes}
    P = Doc(path)
    nodes = node_index(P); shp = shape_index(P)
    nifM, shM = load_mesh(MM_NIF); byM = {s['name']: s for s in shM}
    bone_xf = dict(bone_table(nifM, shM)); bone_xf.update(bone_table(nif, shapes))
    src_pos, src_w = [], []
    for n in SOURCE_SHAPES:
        s = byM[n]; src_pos += s['positions']; src_w += [prune_rows(w) for w in s['weight_map']]
    for name in RESKIN + [PROXY_NAME]:
        s = by[name]; si = shp[name]
        h = parse_shape_hdr(P.blocks[si][1]); dm = parse_dismember(P.blocks[h['skin']][1])
        dsize, vsize, vdesc, vbuf, tris = partition_raw(P, dm['part'])
        if name == PROXY_NAME:
            base = [prune_rows(w) for w in byM[PROXY_SRC]['weight_map']]
            assert len(base) == len(s['positions'])
        else:
            base, _ = knn_transfer(src_pos, src_w, s['positions'])
            base = [prune_rows(w) for w in base]
        new_w = [free_body(w, p[2]) for w, p in zip(base, s['positions'])]
        print(' %s: before' % name); band_stats(s['positions'], s['weight_map'], 'current')
        print(' %s: after' % name); band_stats(s['positions'], new_w, 'retuned')
        for w in new_w:
            for b in w:
                assert b in nodes, b
        dis_fn, sd_b, sp_b, bones, pv = build_skin(P, nodes, bone_xf, s['positions'], vbuf, vdesc, tris, new_w, BODY_PART)
        P.blocks[dm['data']][1] = bytearray(sd_b)
        P.blocks[dm['part']][1] = bytearray(sp_b)
        P.blocks[h['skin']][1] = dis_fn(dm['data'], dm['part'])
        print('   -> %d bones' % len(bones))
    if apply:
        bak = path + '.bak-stiff-20260903'
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
        P.save(path)
        # verify
        nif2, shapes2 = load_mesh(path)
        by2 = {s['name']: s for s in shapes2}
        for name in RESKIN + [PROXY_NAME]:
            a = np.array(by2[name]['positions']); b = np.array(by[name]['positions'])
            assert np.allclose(a, b) and all(abs(sum(w.values()) - 1) < 1e-4 for w in by2[name]['weight_map'])
        print('   written + verified:', path)
    else:
        print('   (dry run, nothing written)')


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    for p in [a for a in sys.argv[1:] if a != '--apply']:
        print('=== ', p)
        retune(p, apply)
