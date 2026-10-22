"""pair_check.py - the game blends a _0 and a _1 mesh shape by shape at load: every shape must exist in both with the same vertex and
triangle counts (and the same order). Scans a folder for *_0.nif / *_1.nif pairs and flags any mismatch. usage: pair_check.py <folder> ..."""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nif_blocks as NB


def shapes(path):
    b, types, tidx, sizes, strings, starts = NB.parse(path)
    out = []; pending = None
    for i, (ti, sz, st) in enumerate(zip(tidx, sizes, starts)):
        t = types[ti]
        if t == 'BSTriShape':
            d = NB.tri_shape(b, st, strings); pending = d; out.append([d['name'], d['nvert'], d['ntri'], d['stride'], d['skin'] >= 0, None, i])
        elif t == 'NiSkinPartition' and out:
            h, parts = NB.skin_partition(b, st)
            # attach to the most recent skinned shape without partition info
            for rec in reversed(out):
                if rec[4] and rec[5] is None:
                    rec[5] = (h['nvert_in_data'], sum(p['ntri'] for p in parts), h['stride']); break
    res = []
    for name, nv, nt, stride, skinned, part, idx in out:
        if skinned and part: nv, nt, stride = part
        res.append((name, nv, nt, stride))
    return res


bad = 0; pairs = 0
for folder in sys.argv[1:]:
    for f0 in sorted(os.path.join(r, fn) for r, _, fs in os.walk(folder) for fn in fs if fn.lower().endswith('_0.nif')):
        f1 = f0[:-6] + '_1.nif'
        if not os.path.exists(f1): continue
        pairs += 1
        try:
            s0, s1 = shapes(f0), shapes(f1)
        except Exception as e:
            print(f'!! {f0}: unparseable {e!r}'); bad += 1; continue
        msgs = []; info = []
        if [s[0] for s in s0] != [s[0] for s in s1]: info.append(f'shape names differ (fine, the game pairs by position): _0 {[s[0] for s in s0]} vs _1 {[s[0] for s in s1]}')
        if len(s0) != len(s1): msgs.append(f'shape COUNT differs: _0 {len(s0)} vs _1 {len(s1)}')
        for a, b in zip(s0, s1):            # the game pairs shapes by position
            if a[1] != b[1] or a[2] != b[2] or a[3] != b[3]:
                msgs.append(f'{a[0]!r} / {b[0]!r}: _0 verts {a[1]} tris {a[2]} stride {a[3]} | _1 verts {b[1]} tris {b[2]} stride {b[3]}')
        if msgs:
            bad += 1; print(f'MISMATCH {f0}'); [print('   ' + m) for m in msgs + info]
print(f'{pairs} pairs checked, {bad} MISMATCHED (a shape differing in vertex / triangle count or stride, or a different number of shapes - the game would read past a buffer)')
