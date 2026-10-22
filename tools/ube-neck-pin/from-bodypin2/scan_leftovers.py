"""Read-only audit after body_pin:
1. Verify the naked body _0/_1 are pinned (partition read-back, band stats).
2. Sweep ALL six UBE trees for ANY skinned shape (any vert count) that still has
   NPC Head weight on verts lying ON the neck ring (within 1.2 units of the
   reference body's neck band) — catches trimmed body copies (VirtualBody etc.)
   that the 29298-vert gate skipped. Reads PARTITION weights (NiSkinData may be stale).
3. List any mods\*\meshes\!UBE trees NOT covered by the six roots.
"""
import os, sys, struct
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh

MODS_ROOT = r"C:/1. AUTHORIA/mods"
ROOTS = [
    "Authoria - Bodyslide Output - UBE",
    "Authoria - UBE Converter Output",
    "DDV - Hal's casual outfit - UBE",
    "Fuse00 - Thalmor Investigator UBE",
    "DD - Sigrin Silver Fox armor by Vergi UBE",
    "Ultimate Body Enhancer",
    "Authoria - Bodyslide Output - NSFW",
    "Arcane Mage Armor UBE",
    "Caenarvon's Cosplay Pack - UBE",
    "Dark Apprentice - UBE SMP",
    "Fuse00 - Scout Armor UBE",
    "Nirn Necessities - UBE patch",
    "Russian Bear - Sand Snake Armor - UBE",
    "SmolSaltLemon - Wine Duchess UBE",
    "Traveler's Armor Pack - Visually Upgradeable Outfit - UBE",
    "UBE Serana - NPC Replacer",
    "UBE Lydia - NPC Replacer",
    "Ultimate Body Enhancer - DF - Humanoid Asset Pack",
    "houseCARL - Authoria - Fix - Corsican Raider UBE Meshes",
    "Authoria - Fix - UBE Neck Seam",
]
REF1 = MODS_ROOT + "/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"
REF0 = MODS_ROOT + "/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_0.nif"

def walk_partition(nif, part_ref):
    r = nif.block_reader(part_ref)
    np_ = r.u32()
    dsize = r.u32(); vsize = r.u32(); desc = r.u64()
    r.o += dsize
    parts = []
    for _ in range(np_):
        p = {}
        nv = r.u16(); nt = r.u16(); nb = r.u16(); ns = r.u16(); nwpv = r.u16()
        p['nwpv'] = nwpv
        p['bones'] = [r.u16() for _ in range(nb)]
        if r.u8(): p['vertex_map'] = [r.u16() for _ in range(nv)]
        else: p['vertex_map'] = list(range(nv))
        if r.u8(): p['w_off'] = r.o; r.o += 4 * nwpv * nv
        else: p['w_off'] = None
        slens = [r.u16() for _ in range(ns)]
        if r.u8():
            if ns:
                for l in slens: r.o += 2 * l
            else: r.o += 6 * nt
        if r.u8(): p['bi_off'] = r.o; r.o += nwpv * nv
        else: p['bi_off'] = None
        r.u16(); r.u64()
        r.o += 6 * nt
        parts.append(p)
    assert r.o - nif.block_offsets[part_ref] == nif.block_sizes[part_ref]
    return parts

def part_head_weights(nif, parts, inst):
    out = {}
    for p in parts:
        if p['w_off'] is None or p['bi_off'] is None: continue
        names = [inst[b] for b in p['bones']]
        if 'NPC Head [Head]' not in names:
            for gv in p['vertex_map']: out.setdefault(gv, 0.0)
            continue
        for lk, gv in enumerate(p['vertex_map']):
            if gv in out: continue
            w = 0.0
            for s in range(p['nwpv']):
                wt = struct.unpack_from('<f', nif.data, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
                b = nif.data[p['bi_off'] + p['nwpv'] * lk + s]
                if b < len(names) and names[b] == 'NPC Head [Head]': w += wt
            out[gv] = w
    return out

# neck-ring reference cloud: body verts Z 108-115 from BOTH weights
ring_pts = []
for rp in (REF1, REF0):
    bp = np.array(load_mesh(rp)[1][0]['positions'], np.float32)
    ring_pts.append(bp[(bp[:, 2] > 108.0) & (bp[:, 2] < 115.0)])
ring = np.concatenate(ring_pts)
print('ring reference points: %d' % len(ring))

# --- 1. naked body verification ---
print('\n== NAKED BODY read-back ==')
for rp in (REF0, REF1):
    nif = Nif(rp)
    _, shapes = load_mesh(rp)
    sh = shapes[0]
    pos = np.array(sh['positions'], np.float32)
    for i in range(nif.num_blocks):
        if nif.btype(i) in ('BSTriShape', 'BSDynamicTriShape'):
            s2 = nif.parse_shape(i)
            if s2['skin_ref'] < 0: continue
            si = nif.parse_skin_instance(s2['skin_ref'])
            parts = walk_partition(nif, si['partition_ref'])
            hw = part_head_weights(nif, parts, si['bone_names'])
            lo = [hw.get(v, 0) for v in range(len(pos)) if pos[v][2] <= 112.5]
            hi = [hw.get(v, 0) for v in range(len(pos)) if pos[v][2] > 112.5]
            print('  %-24s %-14s Z<=112.5: n=%d headmax=%.4f | Z>112.5: n=%d headmax=%.4f' % (
                os.path.basename(rp), s2['name'], len(lo), max(lo) if lo else 0, len(hi), max(hi) if hi else 0))
            break

# --- 2. leftover sweep ---
print('\n== LEFTOVER SWEEP (partition Head weight on ring-adjacent verts) ==')
leftovers = []
nfiles = 0
for root in ROOTS:
    base = os.path.join(MODS_ROOT, root, 'meshes')
    for dp, _d, fs in os.walk(base):
        for f in fs:
            if not f.lower().endswith('.nif'): continue
            path = os.path.join(dp, f)
            nfiles += 1
            try:
                nif = Nif(path)
                _, shapes = load_mesh(path)
            except Exception:
                continue
            for i in range(nif.num_blocks):
                if nif.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
                try:
                    s2 = nif.parse_shape(i)
                    if s2['skin_ref'] < 0: continue
                    sh = next((s for s in shapes if s['name'] == s2['name'] and s.get('positions') is not None), None)
                    if sh is None: continue
                    pos = np.array(sh['positions'], np.float32)
                    band = np.where((pos[:, 2] > 108.0) & (pos[:, 2] < 116.25))[0]
                    if not len(band): continue
                    # ring proximity
                    bp = pos[band]
                    d2 = ((bp[:, None, :] - ring[None, ::4, :]) ** 2).sum(axis=2).min(axis=1)
                    onring = band[np.sqrt(d2) < 1.2]
                    if not len(onring): continue
                    si = nif.parse_skin_instance(s2['skin_ref'])
                    parts = walk_partition(nif, si['partition_ref'])
                    # match by partition vert count
                    total_nv = max((max(p['vertex_map']) + 1 if p['vertex_map'] else 0) for p in parts)
                    if total_nv != len(pos): continue
                    hw = part_head_weights(nif, parts, si['bone_names'])
                    bad = [(int(v), hw.get(int(v), 0.0)) for v in onring
                           if hw.get(int(v), 0.0) > 0.01 and pos[v][2] <= 112.5]
                    badhi = [(int(v), hw.get(int(v), 0.0)) for v in onring
                             if 112.5 < pos[v][2] < 116.25 and hw.get(int(v), 0.0) > 0.01]
                    if bad:
                        leftovers.append((os.path.relpath(path, MODS_ROOT), s2['name'], len(pos),
                                          len(bad), max(w for _v, w in bad), len(badhi)))
                except Exception:
                    continue
print('files scanned: %d' % nfiles)
if leftovers:
    print('shapes with Head weight >0.01 on ring verts Z<=112.5 (NOT pinned):')
    for rel, name, nv, nbad, wmax, nhi in leftovers:
        print('  %-80s %-18s verts=%-6d badverts=%-4d headmax=%.3f rampverts=%d' % (rel, name, nv, nbad, wmax, nhi))
else:
    print('CLEAN — no unpinned ring verts anywhere in the six trees.')

# --- 3. uncovered !UBE trees ---
print('\n== OTHER mods with meshes\\!UBE not in the six roots ==')
others = []
for m in os.listdir(MODS_ROOT):
    if m in ROOTS: continue
    p = os.path.join(MODS_ROOT, m, 'meshes', '!UBE')
    if os.path.isdir(p):
        n = sum(1 for dp, _d, fs in os.walk(p) for f in fs if f.lower().endswith('.nif'))
        others.append((m, n))
for m, n in sorted(others):
    print('  %-60s %d nifs' % (m, n))
if not others: print('  none')
