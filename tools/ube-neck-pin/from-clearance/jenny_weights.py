"""Copy body skin weights onto outfit shell verts (near-skin), fixing pose-shear clipping.

Writes, per affected vertex, consistently into:
  - the NiSkinPartition per-partition weights (float32) + bone_indices (u8 into partition bones)
  - the SSE global vertex buffer skin fields (4x f16 weights + 4x u8 indices)
No block resizes. NiSkinData left untouched (unused by the SSE renderer for skinning).
Dry-run by default; --apply writes with backups. Targets: Caenarvon casual dresses with
measured shell-vs-body weight L1 mean > 0.25.
"""
import os, sys, struct, shutil, re
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh
from weld_taper import layout, f16_encode

APPLY = '--apply' in sys.argv
BK = r"C:\1. AUTHORIA\backups\jenny-weights-20260801"
BODY = r"C:/1. AUTHORIA/mods/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"
NEAR, K = 2.0, 3
L1_GATE = 0.25

_, bs = load_mesh(BODY)
body = bs[0]
bpos = np.array(body['positions'], np.float32)
bw = body['weight_map']

def partition_layout(nif, part_ref):
    """Walk NiSkinPartition recording writable offsets."""
    r = nif.block_reader(part_ref)
    np_ = r.u32()
    dsize = r.u32(); vsize = r.u32(); desc = r.u64()
    vbuf_off = r.o if dsize else None
    nvert_global = dsize // vsize if vsize else 0
    r.o += dsize
    vs, full = layout(desc) if dsize else (0, None)
    vflags = (desc >> 44) & 0xFFF
    # skin fields offset within a vertex record: pos + uv + normal + tangent + color
    off = (16 if full else 8)
    if vflags & 0x2: off += 4
    if vflags & 0x8: off += 4
    if vflags & 0x10: off += 4
    if vflags & 0x20: off += 4
    skin_off = off if (vflags & 0x40) else None
    parts = []
    for _ in range(np_):
        p = {}
        nv = r.u16(); nt = r.u16(); nb = r.u16(); ns = r.u16(); nwpv = r.u16()
        p['bones'] = [r.u16() for _ in range(nb)]
        p['nwpv'] = nwpv
        if r.u8():
            p['vm_off'] = r.o
            p['vertex_map'] = [r.u16() for _ in range(nv)]
        else:
            p['vertex_map'] = list(range(nv))
        if r.u8():
            p['w_off'] = r.o
            r.o += 4 * nwpv * nv
        else:
            p['w_off'] = None
        slens = [r.u16() for _ in range(ns)]
        if r.u8():
            if ns:
                for l in slens: r.o += 2 * l
            else:
                r.o += 6 * nt
        if r.u8():
            p['bi_off'] = r.o
            r.o += nwpv * nv
        else:
            p['bi_off'] = None
        r.u16()
        r.u64()
        r.o += 6 * nt  # tris copy (stream 100)
        parts.append(p)
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'skin_off': skin_off, 'parts': parts, 'nvert': nvert_global}

TARGETS = []
DRESSES = ('seradefault', 'seradefaultsleeveless', 'seradress', 'serasundress',
           'serasweater', 'serasweaterdress')
_root = r"C:/1. AUTHORIA/mods/Authoria - UBE Converter Output/meshes/!UBE/kw_stuff"
for f in sorted(os.listdir(_root)):
    lf = f.lower()
    if lf.endswith(('_0.nif', '_1.nif')) and lf[:-6].rstrip('_') in DRESSES:
        TARGETS.append(os.path.join(_root, f))

report = []
for path in sorted(TARGETS):
    try:
        nif = Nif(path)
    except Exception as e:
        report.append((path, 'PARSE FAIL %s' % e)); continue
    buf = bytearray(nif.data)
    _, shapes = load_mesh(path)
    file_changed = 0
    notes = []
    for sh in shapes:
        if sh.get('positions') is None or 'weight_map' not in sh or 'bones' not in sh: continue
        if re.search(r'proxy|collision|virtual', sh['name'] or '', re.I): continue  # SMP physics shapes, not rendered
        if len(sh['positions']) == len(bpos): continue  # body copy
        pos = np.array(sh['positions'], np.float32)
        if len(pos) < 100: continue
        # measure mismatch first
        n = len(pos)
        near_idx, near_body = [], []
        for c0 in range(0, n, 1024):
            ch = pos[c0:c0+1024]
            d2 = ((ch[:, None, :] - bpos[None, :, :]) ** 2).sum(axis=2)
            ni = d2.argmin(axis=1)
            dmin = np.sqrt(d2[np.arange(len(ch)), ni])
            for k in range(len(ch)):
                if dmin[k] <= NEAR:
                    near_idx.append(c0 + k); near_body.append(ni[k])
        if not near_idx: continue
        l1s = []
        for vi, bi in zip(near_idx, near_body):
            wsh, wbd = sh['weight_map'][vi], bw[bi]
            bones = set(wsh) | set(wbd)
            l1s.append(sum(abs(wsh.get(b, 0.0) - wbd.get(b, 0.0)) for b in bones))
        mean_l1 = float(np.mean(l1s))
        if mean_l1 < L1_GATE:
            notes.append('%s ok(l1=%.2f)' % (sh['name'], mean_l1)); continue
        # locate this shape's skin instance + partition offsets
        target_block = None
        for i in range(nif.num_blocks):
            if nif.btype(i) in ('BSTriShape', 'BSDynamicTriShape'):
                s2 = nif.parse_shape(i)
                if s2['name'] != sh['name'] or s2['skin_ref'] < 0:
                    continue
                # verify via the partition's vertex count (shape block may store 0)
                si2 = nif.parse_skin_instance(s2['skin_ref'])
                r2 = nif.block_reader(si2['partition_ref'])
                r2.u32(); ds2 = r2.u32(); vs2 = r2.u32()
                if vs2 and ds2 // vs2 == len(pos):
                    target_block = s2; break
        if target_block is None or target_block['skin_ref'] < 0:
            notes.append('%s NO SKIN' % sh['name']); continue
        si = nif.parse_skin_instance(target_block['skin_ref'])
        pl = partition_layout(nif, si['partition_ref'])
        inst_bones = si['bone_names']
        # vertex -> partition + local slot
        vert_part = {}
        for pidx, p in enumerate(pl['parts']):
            for local_k, gv in enumerate(p['vertex_map']):
                vert_part.setdefault(gv, (pidx, local_k))
        changed = 0
        dropped_mass_max = 0.0
        for vi, bi in zip(near_idx, near_body):
            got = vert_part.get(vi)
            if got is None: continue
            pidx, lk = got
            p = pl['parts'][pidx]
            if p['w_off'] is None or p['bi_off'] is None: continue
            part_bone_names = [inst_bones[b] for b in p['bones']]
            wbd = bw[bi]
            avail = {bn: w for bn, w in wbd.items() if bn in part_bone_names}
            if not avail: continue
            dropped = sum(w for bn, w in wbd.items() if bn not in part_bone_names)
            dropped_mass_max = max(dropped_mass_max, dropped)
            top = sorted(avail.items(), key=lambda kv: -kv[1])[:p['nwpv']]
            tot = sum(w for _bn, w in top)
            if tot <= 0: continue
            slots = [(part_bone_names.index(bn), w / tot) for bn, w in top]
            while len(slots) < p['nwpv']:
                slots.append((slots[0][0], 0.0))
            # write partition arrays
            for s_i, (bidx, w) in enumerate(slots):
                struct.pack_into('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + s_i), w)
                struct.pack_into('<B', buf, p['bi_off'] + p['nwpv'] * lk + s_i, bidx)
            # write global vbuf skin fields
            if pl['vbuf_off'] is not None and pl['skin_off'] is not None:
                base = pl['vbuf_off'] + vi * pl['vsize'] + pl['skin_off']
                for s_i, (bidx, w) in enumerate(slots[:4]):
                    struct.pack_into('<H', buf, base + 2 * s_i, f16_encode(w))
                    struct.pack_into('<B', buf, base + 8 + s_i, bidx)
            changed += 1
        notes.append('%s FIXED l1=%.2f verts=%d dropmax=%.2f' % (sh['name'], mean_l1, changed, dropped_mass_max))
        file_changed += changed
    if file_changed and APPLY:
        rel = os.path.relpath(path, r"C:/1. AUTHORIA/mods")
        dst = os.path.join(BK, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst): shutil.copy2(path, dst)
        with open(path, 'wb') as f: f.write(bytes(buf))
        Nif(path)  # reparse sanity
    if notes:
        report.append((path, '; '.join(notes)))

print('%s | %d files examined' % ('APPLIED' if APPLY else 'DRY-RUN', len(TARGETS)))
for p, msg in report:
    print('  %-72s %s' % (os.path.basename(p), msg))
