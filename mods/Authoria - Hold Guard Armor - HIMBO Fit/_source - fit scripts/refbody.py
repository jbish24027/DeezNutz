"""Reference body pair for the vanilla -> HIMBO conform.

S (source, what the armour was authored on) and T (target, the HIMBO body the game uses) with ONE
topology: HIMBO's own conversion reference 'HIMBO - VAL.nif' (a vanilla-shaped body in HIMBO
topology) and its 'Vanilla to HIMBO' slider (.osd).
"""
import os, sys, struct
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gnif import GNif
from worldpos import world_skel

HIMBO = r"C:\1. AUTHORIA\mods\Highly Improved Male Body Overhaul -HIMBO-"
CONV = HIMBO + r"\CalienteTools\BodySlide\ShapeData\HIMBO Conversion"
BODY = HIMBO + r"\meshes\actors\character\character assets"
JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAN = os.path.join(JOB, 'vanilla', 'meshes', 'actors', 'character', 'character assets')


def read_osd(path):
    d = open(path, 'rb').read()
    o = 4
    ver, n = struct.unpack_from('<II', d, o); o += 8
    out = {}
    for _ in range(n):
        ln = d[o]; o += 1
        name = d[o:o + ln].decode('latin1'); o += ln
        cnt = struct.unpack_from('<H', d, o)[0]; o += 2
        arr = np.frombuffer(d[o:o + 14 * cnt], dtype=np.dtype([('i', '<u2'), ('d', '<f4', 3)])).copy(); o += 14 * cnt
        out[name] = arr
    assert o == len(d), (o, len(d))
    return out


def tri_normals(P, T):
    N = np.zeros_like(P)
    fn = np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]])
    for j in range(3):
        np.add.at(N, T[:, j], fn)
    return N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)


def load_world(path, shape=None):
    g = GNif(path)
    s = [x for x in g.shapes if x.bones and (shape is None or x.name == shape)][0]
    P, spread, _ = world_skel(g, s)
    return g, s, P


def conversion_pair():
    g, s, P0 = load_world(os.path.join(CONV, 'HIMBO - VAL.nif'))
    osd = read_osd(os.path.join(CONV, 'HIMBO - VAL.osd'))
    arr = list(osd.values())[0]
    D = np.zeros_like(P0)
    D[arr['i']] = arr['d']
    # osd deltas are in shape (skin) space; VAL skin space == world here (checked: A=I, t=0)
    return g, s, P0, P0 + D, s.tris.astype(np.int64)


if __name__ == '__main__':
    from scipy_free_kd import nearest
    g, s, S, T, tris = conversion_pair()
    print('VAL verts', len(S), 'moved by slider', int((np.linalg.norm(T - S, axis=1) > 1e-4).sum()), 'max |d| %.2f' % np.linalg.norm(T - S, axis=1).max())
    for nm, path in [('vanilla_1', os.path.join(VAN, 'malebody_1.nif')), ('vanilla_0', os.path.join(VAN, 'malebody_0.nif'))]:
        _, _, Q = load_world(path, 'MaleUnderwearBody:0')
        d, _ = nearest(S, Q)
        print('VAL base -> %s verts: dist mean %.3f p95 %.3f max %.3f' % (nm, d.mean(), np.percentile(d, 95), d.max()))
    for nm, path in [('HIMBO_1', os.path.join(BODY, 'malebody_1.nif')), ('HIMBO_0', os.path.join(BODY, 'malebody_0.nif'))]:
        _, _, Q = load_world(path)
        d, _ = nearest(Q, T)
        d2, _ = nearest(Q, S)
        print('%s verts -> VAL+slider: mean %.3f p95 %.3f max %.3f   (-> VAL base: mean %.3f)' % (nm, d.mean(), np.percentile(d, 95), d.max(), d2.mean()))
