"""Quick shaded render of a mesh's shapes (front / side / back) to a PNG, plus a poke-through count.
usage: python -I render.py <out.png> <nif> [<nif> ...]   (several nifs -> one row each)"""
import sys, os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bslib as B
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\coat-smp\skill\scripts')
from smpkit import core as C
SKF = B.skeleton_G(C)
SKM = B.skeleton_G(C, r'C:\1. AUTHORIA\mods\BodySlide and Outfit Studio\CalienteTools\BodySlide\res\skeleton_male_sse.nif')

COLORS = [(0.55, 0.25, 0.2), (0.85, 0.7, 0.6), (0.3, 0.4, 0.6), (0.4, 0.55, 0.3), (0.6, 0.6, 0.3)]


def draw(ax, shapes, yaw):
    c, s = np.cos(yaw), np.sin(yaw)
    polys, cols, depth = [], [], []
    for k, (P, T) in enumerate(shapes):
        Q = P @ np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]).T
        tri = Q[T]; n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
        lit = 0.35 + 0.65 * np.abs(n @ np.array([0.3, -0.8, 0.5]) / np.linalg.norm([0.3, -0.8, 0.5]))
        base = np.array(COLORS[k % len(COLORS)])
        polys += list(tri[:, :, [0, 2]]); cols += list(np.clip(base[None] * lit[:, None], 0, 1)); depth += list(tri[:, :, 1].mean(1))
    o = np.argsort(-np.array(depth))
    ax.add_collection(PolyCollection([polys[i] for i in o], facecolors=[cols[i] for i in o], edgecolors='none'))
    ax.set_xlim(-50, 50); ax.set_ylim(-5, 155); ax.set_aspect('equal'); ax.axis('off')


def main(png, nifs):
    fig, axes = plt.subplots(len(nifs), 3, figsize=(9, 5 * len(nifs)), squeeze=False)
    for r, f in enumerate(nifs):
        nif, sh = C.load(f); sk = SKM if ('_m_' in os.path.basename(f).lower() or 'male' in f.lower() and 'female' not in f.lower()) else SKF
        shapes = [(B.bind_pose(C, s, sk)[0], np.array(s.tris)) for s in sh if len(s.tris) and 'coll' not in s.name.lower()]
        for cidx, yaw in enumerate((0.0, np.pi / 2, np.pi)):
            draw(axes[r][cidx], shapes, yaw)
        axes[r][0].set_title(os.path.basename(f), fontsize=8, loc='left')
    fig.tight_layout(); fig.savefig(png, dpi=110)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
