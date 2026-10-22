"""Sample DayOnly's 3BA -> UBE garment move from the user's existing converter output: for every !UBE mesh in
'Authoria - UBE Converter Output' whose 3BA source still exists with the same shape names and point counts, every
garment point gives (3BA rest position, UBE rest position - 3BA rest position). Saved to ube_field.npz.
usage: python -I build_ube_field.py"""
import os, sys, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\coat-smp\skill\scripts")
import bslib as B
from smpkit import core as C

MODS = r"C:\1. AUTHORIA\mods"
UBE_OUT = MODS + r"\Authoria - UBE Converter Output\meshes\!UBE"
SRC_MODS = ["Authoria - Bodyslide Output - 3BA", "CBBE 3BA Vanilla Outfits Redone - Prebuilt", "Somewhere in Between - 3BA Clothes Replacer",
            "Authoria - Bodyslide Output - NSFW"]
PER_FILE = 1500


def main():
    skel = B.skeleton_G(C); P, D, files = [], [], 0
    rng = np.random.default_rng(1)
    for f in glob.glob(UBE_OUT + r"\**\*_1.nif", recursive=True):
        rel = os.path.relpath(f, UBE_OUT)
        src = next((os.path.join(MODS, m, 'meshes', rel) for m in SRC_MODS if os.path.isfile(os.path.join(MODS, m, 'meshes', rel))), None)
        if not src: continue
        try:
            _, us = C.load(f); _, ss = C.load(src)
        except Exception:
            continue
        S = {s.name: s for s in ss}; got = 0
        for u in us:
            s = S.get(u.name)
            if s is None or len(s.pos) != len(u.pos) or u.name in ('BaseShape', '3BA') or len(u.pos) < 50: continue
            a, ma = B.bind_pose(C, s, skel); b, mb = B.bind_pose(C, u, skel)
            if ma or mb: continue
            d = b - a
            if np.linalg.norm(d, axis=1).max() > 15: continue       # not the same garment any more
            k = rng.choice(len(a), min(PER_FILE, len(a)), replace=False)
            P.append(a[k]); D.append(d[k]); got += 1
        files += bool(got)
    P = np.vstack(P); D = np.vstack(D)
    np.savez(os.path.join(HERE, 'ube_field.npz'), P=P, D=D)
    print('pairs from %d meshes, %d samples, move mean %.2f max %.2f, z %.0f..%.0f' % (
        files, len(P), np.linalg.norm(D, axis=1).mean(), np.linalg.norm(D, axis=1).max(), P[:, 2].min(), P[:, 2].max()))


if __name__ == '__main__':
    main()
