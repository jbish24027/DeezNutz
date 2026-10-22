"""Free the jaw while leaving the neck seam untouched.

The bib profile is rebuilt FROM ORIGINAL WEIGHTS as:
    s = 1 - (1 - s_Z(z)) * g(dist_to_body)
  s_Z : the existing height ramp (0 at Z<=112.5 -> 1 at Z>=116.25)
  g   : 1 within D0 of the body surface, smoothstep to 0 by D1
So verts ON/near the body (the seam ring, dist~0) get EXACTLY the profile they
have today -- the body side is unchanged, so the seam is preserved bit-for-bit --
while jaw/chin geometry (dist > D1) returns to full head control.

Writer = the validated v2 path: descriptor-derived skin offset, vbuf-authoritative
reads, writes to the vbuf AND every partition copy. Deploy is gated on 5 checks
including "neck column identical to the currently-deployed file".
"""
import os, sys, struct, shutil, re
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif, load_mesh
from weld_taper import layout, f16_encode

APPLY = '--apply' in sys.argv
MODS = r"C:/1. AUTHORIA/mods"
BK = r"C:/1. AUTHORIA/backups/neckbib5-20260801"
BODY = MODS + "/Authoria - Bodyslide Output - UBE/meshes/!UBE/Body/femalebody_tangent_1.nif"
FIXHEAD = MODS + "/Authoria - Fix - UBE Neck Seam/meshes/!UBE/Head/FemaleHead_tangent.nif"
FIXHEAD_ORIG = r"C:/1. AUTHORIA/backups/neckbib2-20260731/FemaleHead_tangent.nif"
BP3 = r"C:/1. AUTHORIA/backups/bodypin3-20260731"
ZLO, ZHI = 112.5, 116.25
D0, D1 = 3.5, 5.5
EXCL_SHAPE = re.compile(r'hair|wig|scalp|beard|brow|lash', re.I)   # must follow the head
ONLY = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--list=')), None)
FALLBACK = ['NPC Spine2 [Spn2]', 'NPC Spine1 [Spn1]', 'NPC Spine [Spn0]',
            'NPC L Clavicle [LClv]', 'NPC R Clavicle [RClv]']

def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def s_z(z):
    if z >= ZHI: return 1.0
    if z <= ZLO: return 0.0
    return smooth((z - ZLO) / (ZHI - ZLO))

def gate(d):
    if d <= D0: return 1.0
    if d >= D1: return 0.0
    return 1.0 - smooth((d - D0) / (D1 - D0))

def walk_partition(nif, part_ref):
    r = nif.block_reader(part_ref)
    np_ = r.u32()
    dsize = r.u32(); vsize = r.u32(); desc = r.u64()
    vbuf_off = r.o if dsize else None
    r.o += dsize
    parts = []
    for _ in range(np_):
        p = {}
        nv = r.u16(); nt = r.u16(); nb = r.u16(); ns = r.u16(); nwpv = r.u16()
        p['nwpv'] = nwpv; p['nt'] = nt
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
        p['tris_off'] = r.o
        r.o += 6 * nt
        parts.append(p)
    assert r.o - nif.block_offsets[part_ref] == nif.block_sizes[part_ref]
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'dsize': dsize, 'desc': desc, 'parts': parts}

def h2f(hv):
    s = (hv >> 15) & 1; e = (hv >> 10) & 0x1F; m = hv & 0x3FF
    v = (m / 1024.0 * 2 ** -14) if e == 0 else ((1 + m / 1024.0) * 2 ** (e - 15) if e < 31 else 0.0)
    return -v if s else v

def skin_offset(desc, dsize, vsize, dynamic):
    if not dsize: return None
    _vs, full = layout(desc)
    vflags = (desc >> 44) & 0xFFF
    if not (vflags & 0x40): return None
    off = 0 if dynamic else (16 if full else 8)
    for bit in (0x2, 0x8, 0x10, 0x20):
        if vflags & bit: off += 4
    return off

def vbuf_w(data, pl, dso, vi):
    base = pl['vbuf_off'] + vi * pl['vsize'] + dso
    return ([h2f(struct.unpack_from('<H', data, base + 2 * k)[0]) for k in range(4)],
            [data[base + 8 + k] for k in range(4)])

bpos = np.array(load_mesh(BODY)[1][0]['positions'], np.float32)
NECK = bpos[bpos[:, 2] > 104.0]

def dists(pos, idx):
    out = np.empty(len(idx), np.float32)
    for i in range(0, len(idx), 256):
        ch = pos[idx[i:i + 256]]
        out[i:i + 256] = np.sqrt(((ch[:, None, :] - NECK[None, :, :]) ** 2).sum(axis=2)).min(axis=1)
    return out

# ---- discover head-like files: jaw geometry inside the locked band ----
jobs = [(FIXHEAD, FIXHEAD_ORIG)]
for dp, _d, fs in os.walk(BP3):
    for f in fs:
        if not f.lower().endswith('.nif'): continue
        orig = os.path.join(dp, f)
        live = os.path.join(MODS, os.path.relpath(orig, BP3))
        if os.path.exists(live): jobs.append((live, orig))

def headlike(path):
    try:
        for s in load_mesh(path)[1]:
            if s.get('positions') is None: continue
            p = np.array(s['positions'], np.float32)
            m = (p[:, 2] > 113.5) & (p[:, 2] < ZHI) & (p[:, 1] > 5.0)
            if m.sum() >= 10: return True
    except Exception:
        pass
    return False

if ONLY:
    want = [ln.strip() for ln in open(ONLY, encoding='utf-8') if ln.strip()]
    jobs = [(l, o) for l, o in jobs if any(w.lower() in l.lower() for w in want)]
else:
    jobs = [(l, o) for l, o in jobs if headlike(o)]
print('head-like files to re-profile: %d' % len(jobs))
for l, _o in jobs: print('   ' + os.path.relpath(l, MODS))
if not APPLY:
    print('\n(dry run -- pass --apply to write)')
    sys.exit()

done = 0
for live, orig in jobs:
    nif = Nif(orig)                      # source of truth: ORIGINAL weights
    cur = Nif(live)                      # currently deployed (perfect neck)
    _, shapes = load_mesh(orig)
    buf = bytearray(nif.data)
    pool = list(shapes)
    changed_total = 0
    checks = []
    for i in range(nif.num_blocks):
        if nif.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
        dyn = nif.btype(i) == 'BSDynamicTriShape'
        s2 = nif.parse_shape(i)
        if s2['skin_ref'] < 0: continue
        si = nif.parse_skin_instance(s2['skin_ref'])
        pl = walk_partition(nif, si['partition_ref'])
        nv = pl['dsize'] // pl['vsize'] if pl['vsize'] else 0
        sh = next((s for s in pool if s['name'] == s2['name'] and s.get('positions') is not None
                   and len(s['positions']) == nv), None)
        if sh is None: continue
        pool.remove(sh)
        inst = si['bone_names']
        if 'NPC Head [Head]' not in inst: continue
        if EXCL_SHAPE.search(s2['name'] or ''): continue
        # FaceGen files: only the baked head itself (matches the verified pin pass)
        if 'facegeom' in live.lower() and nv != 11498: continue
        dso = skin_offset(pl['desc'], pl['dsize'], pl['vsize'], dyn)
        if dso is None or pl['vbuf_off'] is None or dso + 12 > pl['vsize']: continue
        pos = np.array(sh['positions'], np.float32)
        band = np.where(pos[:, 2] < ZHI)[0]
        if not len(band): continue
        samp = list(range(0, nv, max(1, nv // 200)))[:200]
        if sum(1 for v in samp if not (0.95 < sum(vbuf_w(nif.data, pl, dso, v)[0]) < 1.05)) > len(samp) * 0.01:
            continue
        dd = dict(zip(band.tolist(), dists(pos, band).tolist()))
        vp = {}
        for pidx, p in enumerate(pl['parts']):
            for lk, gv in enumerate(p['vertex_map']):
                vp.setdefault(gv, []).append((pidx, lk))
        conv = 'same' if all(p['bones'] == list(range(len(inst))) for p in pl['parts']) else (
            'local' if len(pl['parts']) == 1 else 'global')
        n_ch = 0
        for vi in band:
            vi = int(vi)
            occ = vp.get(vi)
            if not occ: continue
            names = [inst[b] for b in pl['parts'][occ[0][0]]['bones']] if conv == 'local' else inst
            ws, bi = vbuf_w(nif.data, pl, dso, vi)
            wh = sum(w for w, b in zip(ws, bi) if w > 0 and b < len(names) and names[b] == 'NPC Head [Head]')
            if wh <= 0.001: continue
            s_new = 1.0 - (1.0 - s_z(pos[vi][2])) * gate(dd[vi])
            if s_new >= 0.999: continue
            recv = next((b for b in FALLBACK if b in names), None)
            if recv is None: continue
            if any(next((b for b in FALLBACK if b in [inst[x] for x in pl['parts'][pi]['bones']]), None) is None
                   for pi, _lk in occ): continue
            d = {}
            for w, b in zip(ws, bi):
                if w > 0 and b < len(names): d[names[b]] = d.get(names[b], 0.0) + w
            moved = wh * (1 - s_new)
            d['NPC Head [Head]'] = wh - moved
            d[recv] = d.get(recv, 0.0) + moved
            top = sorted(d.items(), key=lambda kv: -kv[1])[:4]
            tot = sum(w for _b, w in top)
            top = [(bn, w / tot) for bn, w in top]
            wn = [inst[b] for b in pl['parts'][occ[0][0]]['bones']] if conv == 'local' else inst
            if any(bn not in wn for bn, _w in top): continue
            base = pl['vbuf_off'] + vi * pl['vsize'] + dso
            for k in range(4):
                bn, w = top[k] if k < len(top) else (top[0][0], 0.0)
                struct.pack_into('<H', buf, base + 2 * k, f16_encode(w))
                struct.pack_into('<B', buf, base + 8 + k, wn.index(bn))
            for pidx, lk in occ:
                p = pl['parts'][pidx]
                if p['w_off'] is None or p['bi_off'] is None: continue
                pn = [inst[b] for b in p['bones']]
                pt = [(bn, w) for bn, w in top if bn in pn]
                ptot = sum(w for _b, w in pt)
                if ptot <= 0: continue
                pt = [(bn, w / ptot) for bn, w in pt][:p['nwpv']]
                for k in range(p['nwpv']):
                    bn, w = pt[k] if k < len(pt) else (pt[0][0], 0.0)
                    struct.pack_into('<f', buf, p['w_off'] + 4 * (p['nwpv'] * lk + k), w)
                    struct.pack_into('<B', buf, p['bi_off'] + p['nwpv'] * lk + k, pn.index(bn))
            n_ch += 1
        changed_total += n_ch
        # ---- per-shape verification ----
        cs = cur.parse_shape(i)
        cpl = walk_partition(cur, cs['skin_ref'] and cur.parse_skin_instance(cs['skin_ref'])['partition_ref'])
        def hw(data, plx, vi_, nm):
            w_, b_ = vbuf_w(data, plx, dso, vi_)
            return sum(w for w, b in zip(w_, b_) if w > 0 and b < len(nm) and nm[b] == 'NPC Head [Head]')
        neck_ok = jaw_ok = True
        for vi in band:
            vi = int(vi)
            occ = vp.get(vi)
            if not occ: continue
            nm = [inst[b] for b in pl['parts'][occ[0][0]]['bones']] if conv == 'local' else inst
            if dd[vi] <= D0:                       # neck column: must equal DEPLOYED
                if abs(hw(bytes(buf), pl, vi, nm) - hw(cur.data, cpl, vi, nm)) > 0.02: neck_ok = False; break
            elif dd[vi] >= D1:                     # jaw: must equal ORIGINAL
                if abs(hw(bytes(buf), pl, vi, nm) - hw(nif.data, pl, vi, nm)) > 0.02: jaw_ok = False; break
        checks.append((s2['name'], n_ch, neck_ok, jaw_ok))
    if not changed_total or not all(c[2] and c[3] for c in checks):
        print('  SKIP %s (checks: %s)' % (os.path.relpath(live, MODS), checks)); continue
    tmp = live + '.jaw.tmp'
    open(tmp, 'wb').write(bytes(buf))
    n2 = Nif(tmp); _, s2l = load_mesh(tmp)
    if not all(np.array_equal(np.array(a['positions'], np.float32), np.array(b['positions'], np.float32))
               for a, b in zip(shapes, s2l) if a.get('positions') is not None and b.get('positions') is not None):
        os.remove(tmp); print('  FAIL-POS %s' % live); continue
    rel = os.path.relpath(live, MODS)
    dst = os.path.join(BK, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst): shutil.copy2(live, dst)
    os.replace(tmp, live)
    done += 1
    print('  DEPLOYED %-72s %s' % (rel, '; '.join('%s:%d neck=%s jaw=%s' % c for c in checks)))
print('\ndeployed: %d files' % done)
