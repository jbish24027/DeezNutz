"""Real leg motion from the game's own animation clips (PyNifly's Skyrim HKX reader): per frame, every leg bone's deformation
in the mesh's bind space, measured RELATIVE TO THE PELVIS (a skirt hangs from the pelvis; where the body is in the world does
not matter to the cloth-vs-legs question).
  load_clip(path, g) -> (frames [{bone: 4x4 deformation} ...], animation, {bone: bind world 4x4})
Settings (smpkit/settings.json or the environment): SKELETON_HKX_M / SKELETON_HKX_F = the game's skeleton.hkx per sex (XPMSSE:
meshes/actors/character/character assets/skeleton.hkx and .../character assets female/skeleton_female.hkx), CLIPS = {"m": {"walk":
"<path>.hkx", "run": ..., "sprint": ...}, "f": {...}} - the clips the wearer actually plays (an animation replacer's forward
walk / run / sprint). usage: anim.py   (prints each clip's frames and the ankle's reach)"""
import os, sys, numpy as np
from smpkit import setting, setup_pynifly

_pn = setup_pynifly()
if os.path.join(_pn, 'hkx') not in sys.path: sys.path.insert(0, os.path.join(_pn, 'hkx'))
import anim_skyrim as AS

SKEL = {'m': setting('SKELETON_HKX_M'), 'f': setting('SKELETON_HKX_F')}
CLIPS = setting('CLIPS') or {}
LEGB = ['NPC Pelvis [Pelv]', 'NPC L Thigh [LThg]', 'NPC R Thigh [RThg]', 'NPC L Calf [LClf]', 'NPC R Calf [RClf]',
        'NPC L Foot [Lft ]', 'NPC R Foot [Rft ]', 'NPC L Toe0 [LToe]', 'NPC R Toe0 [RToe]']
PELV = LEGB[0]


def configured(g='m'):
    """True when a skeleton hkx and at least one clip are configured for this sex"""
    return bool(SKEL.get(g)) and bool(CLIPS.get(g))


def qmat(q):     # (x, y, z, w)
    x, y, z, w = q; n = np.sqrt(x * x + y * y + z * z + w * w); x, y, z, w = x / n, y / n, z / n, w / n
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def trs(t, q, s=1.0):
    M = np.eye(4); M[:3, :3] = qmat(q) * s; M[:3, 3] = t; return M


_skel_cache = {}


def skeleton(g):
    if g not in _skel_cache:
        if not SKEL.get(g): raise RuntimeError(f'SKELETON_HKX_{g.upper()} not configured (smpkit/settings.json)')
        _skel_cache[g] = AS.load_skyrim_skeleton(SKEL[g])
    return _skel_cache[g]


def world(sk, local):
    """local: list of 4x4 per skeleton bone -> world 4x4 per bone"""
    W = [None] * len(local)
    for i in range(len(local)):
        p = sk.parents[i]
        W[i] = local[i] if p < 0 else W[p] @ local[i]
    return W


def load_clip(path, g):
    sk = skeleton(g); an = AS.load_skyrim_animation(path)
    names = list(sk.bones)
    ref = [trs(p.translation, p.rotation, float(np.mean(p.scale))) for p in sk.reference_pose]
    Wref = world(sk, ref)
    track_bone = list(an.track_to_bone_indices) if an.track_to_bone_indices else list(range(len(an.tracks)))
    idx = {n: i for i, n in enumerate(names)}
    frames = []
    nf = len(an.tracks[0].translations) if hasattr(an.tracks[0], 'translations') else an.num_frames
    for f in range(nf):
        loc = list(ref)
        for t, b in zip(an.tracks, track_bone):
            loc[b] = trs(t.translations[f], t.rotations[f])
        W = world(sk, loc)
        Pa, Pr = W[idx[PELV]], Wref[idx[PELV]]
        D = {}
        for nm in LEGB:
            i = idx[nm]
            rel_a = np.linalg.inv(Pa) @ W[i]; rel_r = np.linalg.inv(Pr) @ Wref[i]
            D[nm] = Pr @ rel_a @ np.linalg.inv(rel_r) @ np.linalg.inv(Pr)
        frames.append(D)
    return frames, an, {nm: Wref[idx[nm]] for nm in LEGB}


def main():
    for g in ('m', 'f'):
        if not configured(g): print(f'{g}: not configured'); continue
        for k, path in CLIPS[g].items():
            fr, an, Wr = load_clip(path, g)
            ys, zs = [], []
            for D in fr:
                for side in 'LR':
                    ft = f'NPC {side} Foot [{side}ft ]'; p = (D[ft] @ np.r_[Wr[ft][:3, 3], 1])[:3]; ys.append(p[1]); zs.append(p[2])
            print(f'{g} {k}: {len(fr)} frames, {an.duration:.3f}s; ankle y {min(ys):.1f}..{max(ys):.1f} z {min(zs):.1f}..{max(zs):.1f}')


if __name__ == '__main__':
    main()
