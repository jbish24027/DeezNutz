"""Neck-bib softening on the UBE head, with empirical offset location and full
pre-deploy verification. Writes to a temp file; deploys only if every check passes."""
import sys, os, struct, shutil, tempfile
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad')
from nifparse import Nif, load_mesh
from weld_taper import f16_encode

HEAD = r"C:/1. AUTHORIA/mods/Authoria - Fix - UBE Neck Seam/meshes/!UBE/Head/FemaleHead_tangent.nif"
BODY = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"
BK = r"C:/1. AUTHORIA/backups/neckbib4-20260731"
FLOOR = 0.0

def walk_partition(nif, part_ref):
    """Structure-walk identical to the VALIDATED nifparse parser, recording offsets."""
    r = nif.block_reader(part_ref)
    np_ = r.u32()
    dsize = r.u32(); vsize = r.u32(); desc = r.u64()
    vbuf_off = r.o if dsize else None
    r.o += dsize
    parts = []
    for _ in range(np_):
        p = {}
        nv = r.u16(); nt = r.u16(); nb = r.u16(); ns = r.u16(); nwpv = r.u16()
        p['nv'], p['nt'], p['nwpv'] = nv, nt, nwpv
        p['bones'] = [r.u16() for _ in range(nb)]
        if r.u8():
            p['vertex_map'] = [r.u16() for _ in range(nv)]
        else:
            p['vertex_map'] = list(range(nv))
        if r.u8():
            p['w_off'] = r.o; r.o += 4 * nwpv * nv
        else:
            p['w_off'] = None
        slens = [r.u16() for _ in range(ns)]
        if r.u8():
            if ns:
                for l in slens: r.o += 2 * l
            else:
                r.o += 6 * nt
        if r.u8():
            p['bi_off'] = r.o; r.o += nwpv * nv
        else:
            p['bi_off'] = None
        r.u16()
        r.u64()
        p['tris_off'] = r.o
        r.o += 6 * nt
        parts.append(p)
    consumed = r.o - nif.block_offsets[part_ref]
    assert consumed == nif.block_sizes[part_ref], 'partition walk mismatch: %d vs %d' % (consumed, nif.block_sizes[part_ref])
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'dsize': dsize, 'parts': parts}

def read_part_weights(data, pl, inst, vi_lookup):
    """vertex -> {bone: weight} from partition arrays."""
    out = {}
    for p in pl['parts']:
        if p['w_off'] is None or p['bi_off'] is None: continue
        names = [inst[b] for b in p['bones']]
        for lk, gv in enumerate(p['vertex_map']):
            if gv in out: continue
            d = {}
            for s in range(p['nwpv']):
                w = struct.unpack_from('<f', data, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
                b = data[p['bi_off'] + p['nwpv'] * lk + s]
                if w > 0 and b < len(names):
                    d[names[b]] = d.get(names[b], 0.0) + w
            out[gv] = d
    return out

# --- load ---
nif = Nif(HEAD)
_, hs = load_mesh(HEAD)
h = next(s for s in hs if s['name'] == 'FemaleHead')
pos = np.array(h['positions'], np.float32)
for i in range(nif.num_blocks):
    if nif.btype(i) == 'BSDynamicTriShape':
        blk = i
        sh = nif.parse_shape(i)
        si = nif.parse_skin_instance(sh['skin_ref'])
        pl = walk_partition(nif, si['partition_ref'])
        inst = si['bone_names']
        break
print('partition walk OK | vbuf dsize=%d vsize=%d parts=%d' % (pl['dsize'], pl['vsize'], len(pl['parts'])))

# reference weights from partition (reader #1) and NiSkinData (reader #2, via load_mesh)
part_w = read_part_weights(nif.data, pl, inst, None)
agree = sum(1 for vi in range(0, len(pos), 199)
            if sum(abs(part_w.get(vi, {}).get(b, 0) - h['weight_map'][vi].get(b, 0))
                   for b in set(part_w.get(vi, {})) | set(h['weight_map'][vi])) < 0.02)
print('partition-vs-NiSkinData agreement on samples: %d/%d' % (agree, len(range(0, len(pos), 199))))

# empirically locate vbuf skin fields (if any): find offset where f16x4+u8x4 matches partition
skin_off = None
if pl['vbuf_off'] is not None:
    vs = pl['vsize']
    # candidate offsets
    def h2f(hv):
        s = (hv >> 15) & 1; e = (hv >> 10) & 0x1F; m = hv & 0x3FF
        v = (m / 1024.0 * 2 ** -14) if e == 0 else ((1 + m / 1024.0) * 2 ** (e - 15) if e < 31 else 0.0)
        return -v if s else v
    sample_verts = [gv for gv in range(0, len(pos), 401)][:40]
    best = None
    for cand in range(0, vs - 11, 2):
        ok = 0
        for gv in sample_verts:
            base = pl['vbuf_off'] + gv * vs + cand
            ws = [h2f(struct.unpack_from('<H', nif.data, base + 2 * k)[0]) for k in range(4)]
            tot = sum(ws)
            if 0.95 < tot < 1.05 and all(-0.01 <= w <= 1.01 for w in ws):
                ok += 1
        if best is None or ok > best[1]:
            best = (cand, ok)
    if best and best[1] >= len(sample_verts) * 0.95:
        skin_off = best[0]
    print('vbuf skin fields: %s (offset %s, %d/%d samples valid)' % (
        'LOCATED' if skin_off is not None else 'NOT FOUND — vbuf writes will be SKIPPED',
        best[0] if best else '-', best[1] if best else 0, len(sample_verts)))

# ring verts (sealed, untouched)
_, bs = load_mesh(BODY)
bpos = np.array(bs[0]['positions'], np.float32)
bsub = bpos[bpos[:, 2] > 105.0]
ring = set()
for vi in range(len(pos)):
    if pos[vi][2] > 116.0: continue
    d2 = ((pos[vi][None, :] - bsub) ** 2).sum(axis=1)
    if float(d2.min()) ** 0.5 < 0.05: ring.add(vi)

def scale_factor(z):
    if z >= 116.25: return 1.0
    if z <= 112.5: return FLOOR
    t = (z - 112.5) / (116.25 - 112.5)
    return FLOOR + (1.0 - FLOOR) * (t * t * (3 - 2 * t))

# --- apply to buffer ---
buf = bytearray(nif.data)
vert_part = {}
for pidx, p in enumerate(pl['parts']):
    for lk, gv in enumerate(p['vertex_map']):
        vert_part.setdefault(gv, (pidx, lk))
touched = {}
for vi in range(len(pos)):
    z = pos[vi][2]
    if z >= 116.25: continue
    got = vert_part.get(vi)
    if got is None: continue
    pidx, lk = got
    p = pl['parts'][pidx]
    if p['w_off'] is None or p['bi_off'] is None: continue
    names = [inst[b] for b in p['bones']]
    cur = {}
    for s in range(p['nwpv']):
        w = struct.unpack_from('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
        b = buf[p['bi_off'] + p['nwpv'] * lk + s]
        if w > 0 and b < len(names): cur[names[b]] = cur.get(names[b], 0.0) + w
    wh = cur.get('NPC Head [Head]', 0.0)
    if wh <= 0.001: continue
    s_ = scale_factor(z)
    if s_ >= 0.999: continue
    if 'NPC Spine2 [Spn2]' not in names: continue  # must be able to receive mass in this partition
    moved = wh * (1 - s_)
    cur['NPC Head [Head]'] = wh - moved
    cur['NPC Spine2 [Spn2]'] = cur.get('NPC Spine2 [Spn2]', 0.0) + moved
    top = sorted(cur.items(), key=lambda kv: -kv[1])[:p['nwpv']]
    tot = sum(w for _b, w in top)
    slots = [(names.index(bn), w / tot) for bn, w in top]
    while len(slots) < p['nwpv']: slots.append((slots[0][0], 0.0))
    for s_i, (bidx, w) in enumerate(slots):
        struct.pack_into('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s_i), w)
        struct.pack_into('<B', buf, p['bi_off'] + p['nwpv'] * lk + s_i, bidx)
    if skin_off is not None:
        base = pl['vbuf_off'] + vi * pl['vsize'] + skin_off
        for s_i, (bidx, w) in enumerate(slots[:4]):
            struct.pack_into('<H', buf, base + 2 * s_i, f16_encode(w))
            struct.pack_into('<B', buf, base + 8 + s_i, bidx)
    touched[vi] = dict(top)
print('verts modified in buffer:', len(touched))

# --- verification gauntlet on temp file ---
tmp = os.path.join(tempfile.gettempdir(), 'bib_test.nif')
open(tmp, 'wb').write(bytes(buf))
nif2 = Nif(tmp)
sh2 = nif2.parse_shape(blk)
pos2 = np.array(sh2['positions'], np.float32)
checks = []
checks.append(('reparse clean', True))
checks.append(('positions byte-identical', bool(np.array_equal(pos, pos2))))
pl2 = walk_partition(nif2, si['partition_ref'])
t_same = all(nif.data[p1['tris_off']:p1['tris_off'] + 6 * p1['nt']] == bytes(buf[p2['tris_off']:p2['tris_off'] + 6 * p2['nt']])
             for p1, p2 in zip(pl['parts'], pl2['parts']))
checks.append(('triangles byte-identical', t_same))
pw2 = read_part_weights(bytes(buf), pl2, inst, None)
sums_ok = all(abs(sum(pw2[vi].values()) - 1.0) < 0.02 for vi in touched)
checks.append(('touched weights sum to 1.0', sums_ok))
intent_ok = True
for vi, want in list(touched.items())[::7]:
    got = pw2.get(vi, {})
    if sum(abs(got.get(b, 0) - want.get(b, 0)) for b in set(got) | set(want)) > 0.03:
        intent_ok = False; break
checks.append(('written weights match intent', intent_ok))
untouched_ok = True
for vi in range(0, len(pos), 307):
    if vi in touched or vi in ring: continue
    a, b2 = part_w.get(vi, {}), pw2.get(vi, {})
    if sum(abs(a.get(x, 0) - b2.get(x, 0)) for x in set(a) | set(b2)) > 0.005:
        untouched_ok = False; break
checks.append(('untouched verts unchanged', untouched_ok))
ring_zeroed = all(pw2.get(vi, {}).get('NPC Head [Head]', 0.0) < 0.01
                  for vi in ring if pos[vi][2] <= 112.5)
checks.append(('bottom ring fully torso-bound', ring_zeroed))

print('\nVERIFICATION:')
allok = True
for name, ok in checks:
    print('  %-34s %s' % (name, 'PASS' if ok else 'FAIL'))
    allok &= ok
if allok:
    os.makedirs(BK, exist_ok=True)
    shutil.copy2(HEAD, os.path.join(BK, 'FemaleHead_tangent.nif'))
    shutil.copy2(tmp, HEAD)
    print('\nDEPLOYED (backup in %s)' % BK)
else:
    print('\nNOT deployed — mod untouched.')
