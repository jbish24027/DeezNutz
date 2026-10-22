"""Read-back proof on the PLAYER's head: per distance band, compare
original vs pre-jaw-fix deployed vs live. Reads the vbuf (renderer truth)."""
import os, sys, struct
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh
ex = {}
exec(open(os.path.join(SP, 'free_jaw.py')).read().split('bpos = np.array')[0].replace("APPLY = '--apply' in sys.argv", "APPLY=False"), ex)
walk, skin_offset, vbuf_w = ex['walk_partition'], ex['skin_offset'], ex['vbuf_w']

LIVE = r"C:/1. AUTHORIA/mods/Authoria - Fix - UBE Neck Seam/meshes/!UBE/Head/FemaleHead_tangent.nif"
ORIG = r"C:/1. AUTHORIA/backups/neckbib2-20260731/FemaleHead_tangent.nif"
PREV = r"C:/1. AUTHORIA/backups/neckbib5-20260801/Authoria - Fix - UBE Neck Seam/meshes/!UBE/Head/FemaleHead_tangent.nif"
BODY = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"
print('pre-jaw-fix backup exists:', os.path.exists(PREV))

n_live, n_orig = Nif(LIVE), Nif(ORIG)
n_prev = Nif(PREV) if os.path.exists(PREV) else None
h = next(s for s in load_mesh(ORIG)[1] if s['name'] == 'FemaleHead')
pos = np.array(h['positions'], np.float32)
blk = next(i for i in range(n_orig.num_blocks) if n_orig.btype(i) == 'BSDynamicTriShape')
si = n_orig.parse_skin_instance(n_orig.parse_shape(blk)['skin_ref'])
pl = walk(n_orig, si['partition_ref'])
inst = si['bone_names']
dso = skin_offset(pl['desc'], pl['dsize'], pl['vsize'], True)
print('skin offset (descriptor):', dso, ' vsize', pl['vsize'])

bpos = np.array(load_mesh(BODY)[1][0]['positions'], np.float32)
neck = bpos[bpos[:, 2] > 104.0]
band = np.where(pos[:, 2] < 116.25)[0]
d = np.empty(len(band), np.float32)
for i in range(0, len(band), 256):
    ch = pos[band[i:i + 256]]
    d[i:i + 256] = np.sqrt(((ch[:, None, :] - neck[None, :, :]) ** 2).sum(axis=2)).min(axis=1)

def hw(data, vi):
    ws, bi = vbuf_w(data, pl, dso, vi)
    return sum(w for w, b in zip(ws, bi) if w > 0 and b < len(inst) and inst[b] == 'NPC Head [Head]')

print('\n dist band      n   headW original -> pre-fix -> LIVE NOW   verdict')
for a, b in [(0, 0.05), (0.05, 1.5), (1.5, 3.5), (3.5, 5.5), (5.5, 8.0), (8.0, 99)]:
    sel = band[(d >= a) & (d < b)]
    if not len(sel): continue
    o = np.mean([hw(n_orig.data, int(v)) for v in sel])
    p = np.mean([hw(n_prev.data, int(v)) for v in sel]) if n_prev else float('nan')
    l = np.mean([hw(n_live.data, int(v)) for v in sel])
    if b <= 3.5: verdict = 'seam UNCHANGED' if abs(l - p) < 0.02 else '!! SEAM MOVED !!'
    elif a >= 5.5: verdict = 'jaw FREED' if abs(l - o) < 0.02 else '!! still locked !!'
    else: verdict = 'blend'
    print('  %4.2f-%5.2f %5d      %.3f  ->  %.3f  ->  %.3f     %s' % (a, b, len(sel), o, p, l, verdict))

ring = [int(v) for v, dd in zip(band, d) if dd < 0.05]
print('\nseam ring (%d verts) head weight now: max %.4f  (0 = fully torso-locked)'
      % (len(ring), max(hw(n_live.data, v) for v in ring)))
