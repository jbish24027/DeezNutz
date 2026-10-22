"""Where does the jaw start relative to the seam? Read-only measurement on the
ORIGINAL head weights (neckbib2 backup) + the live body reference."""
import sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad')
from nifparse import load_mesh

HEAD_ORIG = r"C:/1. AUTHORIA/backups/neckbib2-20260731/FemaleHead_tangent.nif"
BODY = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"

h = next(s for s in load_mesh(HEAD_ORIG)[1] if s['name'] == 'FemaleHead')
pos = np.array(h['positions'], np.float32)
wm = h['weight_map']
bpos = np.array(load_mesh(BODY)[1][0]['positions'], np.float32)
neck = bpos[bpos[:, 2] > 104.0]
print('head Z %.1f..%.1f  |  body neck-cloud verts=%d Z %.1f..%.1f' % (
    pos[:, 2].min(), pos[:, 2].max(), len(neck), neck[:, 2].min(), neck[:, 2].max()))

# distance from each low head vert to the body neck surface
low = np.where(pos[:, 2] < 126.0)[0]
d = np.empty(len(low), np.float32)
for i in range(0, len(low), 256):
    ch = pos[low[i:i + 256]]
    d[i:i + 256] = np.sqrt(((ch[:, None, :] - neck[None, :, :]) ** 2).sum(axis=2)).min(axis=1)
dist = dict(zip(low.tolist(), d.tolist()))

print('\n  Zband    n   Yfwd_max  dist_to_body(min/med/max)  origHeadW(mean)  curPinned')
for z0 in np.arange(110.0, 124.0, 1.0):
    idx = [v for v in low if z0 <= pos[v][2] < z0 + 1]
    if not idx: continue
    dd = np.array([dist[v] for v in idx])
    hw = np.array([wm[v].get('NPC Head [Head]', 0.0) for v in idx])
    npin = sum(1 for v in idx if pos[v][2] < 116.25)
    print('  %5.1f %5d   %7.2f   %5.2f /%5.2f /%5.2f      %.3f          %d' % (
        z0, len(idx), max(pos[v][1] for v in idx), dd.min(), np.median(dd), dd.max(), hw.mean(), npin))

# chin tip = most forward vertex in the lower head
cand = [v for v in low if pos[v][2] < 122]
chin = max(cand, key=lambda v: pos[v][1])
print('\nchin tip: Z=%.2f Y=%.2f  dist_to_body=%.2f  origHeadW=%.3f' % (
    pos[chin][2], pos[chin][1], dist[chin], wm[chin].get('NPC Head [Head]', 0.0)))
# jaw underside: forward verts (Y > 60% of chin Y) sorted by Z
fwd = sorted([v for v in cand if pos[v][1] > pos[chin][1] * 0.6], key=lambda v: pos[v][2])
print('lowest jaw/front verts (Y>%.1f):' % (pos[chin][1] * 0.6))
for v in fwd[:8]:
    print('   Z=%6.2f Y=%6.2f dist=%5.2f origHeadW=%.3f  %s' % (
        pos[v][2], pos[v][1], dist[v], wm[v].get('NPC Head [Head]', 0.0),
        'PINNED-NOW' if pos[v][2] < 116.25 else ''))
# how far from the seam ring is the chin, vs the nape
ring = [v for v in low if dist[v] < 0.05]
print('\ncoincident ring verts=%d  Z %.2f..%.2f' % (
    len(ring), min(pos[v][2] for v in ring), max(pos[v][2] for v in ring)))
