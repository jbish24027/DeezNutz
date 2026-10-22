"""Forensics on the reverted body-pin passes.
For every quarantined (bad) file vs its restored original (live):
  A. classify every differing byte range: partition weight array / partition index
     array / vbuf skin field at the DESCRIPTOR-derived offset / OUT-OF-BAND.
  B. detect multi-partition vertex copies whose weights now disagree in the bad file.
  C. compare the empirically-located skin offset (what pin scripts used) vs the
     descriptor-derived offset (ground truth from weight_copy's validated math).
Read-only. Prints worst offenders first at the end."""
import os, sys, struct
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\5e1047d0-0af7-4956-b8a9-e0821adb4625\scratchpad'
sys.path.insert(0, SP)
from nifparse import Nif
from weld_taper import layout

MODS = r"C:/1. AUTHORIA/mods"
BAD = r"C:/1. AUTHORIA/backups/bodypin-bad-20260731"

def walk_partition_full(nif, part_ref):
    r = nif.block_reader(part_ref)
    np_ = r.u32()
    dsize = r.u32(); vsize = r.u32(); desc = r.u64()
    vbuf_off = r.o if dsize else None
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
    return {'vbuf_off': vbuf_off, 'vsize': vsize, 'dsize': dsize, 'desc': desc, 'parts': parts}

def descriptor_skin_off(desc, dsize, vsize):
    """weight_copy's validated math: pos(16/8 by full-precision) + uv4 + nrm4 + tan4 + col4 -> skin."""
    if not dsize: return None
    vs, full = layout(desc)
    vflags = (desc >> 44) & 0xFFF
    off = 16 if full else 8
    if vflags & 0x2: off += 4
    if vflags & 0x8: off += 4
    if vflags & 0x10: off += 4
    if vflags & 0x20: off += 4
    return off if (vflags & 0x40) else None

results = []
nfiles = 0
for dp, _d, fs in os.walk(BAD):
    for f in fs:
        if not f.lower().endswith('.nif'): continue
        badp = os.path.join(dp, f)
        rel = os.path.relpath(badp, BAD)
        livep = os.path.join(MODS, rel)
        if not os.path.exists(livep): continue
        nfiles += 1
        try:
            orig = Nif(livep)
            bad = open(badp, 'rb').read()
        except Exception as e:
            results.append((rel, 'PARSE-FAIL %s' % e, 9)); continue
        if len(orig.data) != len(bad):
            results.append((rel, 'SIZE CHANGED %d->%d' % (len(orig.data), len(bad)), 9)); continue
        o = orig.data
        # collect legit regions from the ORIGINAL structure
        legit = []          # (start,end,tag)
        shapes_meta = []
        for i in range(orig.num_blocks):
            if orig.btype(i) not in ('BSTriShape', 'BSDynamicTriShape'): continue
            try:
                s2 = orig.parse_shape(i)
                if s2['skin_ref'] < 0: continue
                si = orig.parse_skin_instance(s2['skin_ref'])
                pl = walk_partition_full(orig, si['partition_ref'])
            except Exception:
                continue
            dso = descriptor_skin_off(pl['desc'], pl['dsize'], pl['vsize'])
            nverts = pl['dsize'] // pl['vsize'] if pl['vsize'] else 0
            shapes_meta.append((s2['name'], pl, si['bone_names'], dso, nverts))
            for p in pl['parts']:
                nv = len(p['vertex_map'])
                if p['w_off'] is not None: legit.append((p['w_off'], p['w_off'] + 4 * p['nwpv'] * nv, 'pw'))
                if p['bi_off'] is not None: legit.append((p['bi_off'], p['bi_off'] + p['nwpv'] * nv, 'pi'))
            if pl['vbuf_off'] is not None and dso is not None:
                legit.append((pl['vbuf_off'], pl['vbuf_off'] + pl['dsize'], 'vbuf'))
        legit.sort()
        # diff scan
        a = np.frombuffer(o, np.uint8); b = np.frombuffer(bad, np.uint8)
        diff_idx = np.where(a != b)[0]
        oob = 0; vbuf_bad_off = {}
        for off in diff_idx:
            off = int(off)
            tag = None
            for s, e, t in legit:
                if s <= off < e: tag = t; break
            if tag is None:
                oob += 1
            elif tag == 'vbuf':
                # locate which shape's vbuf + offset within the vertex record
                for name, pl, inst, dso, nverts in shapes_meta:
                    if pl['vbuf_off'] is not None and pl['vbuf_off'] <= off < pl['vbuf_off'] + pl['dsize']:
                        ro = (off - pl['vbuf_off']) % pl['vsize']
                        ok = dso is not None and dso <= ro < dso + 12
                        if not ok:
                            vbuf_bad_off[(name, ro)] = vbuf_bad_off.get((name, ro), 0) + 1
                        break
        # multi-partition disagreement in BAD
        mp_bad = 0
        for name, pl, inst, dso, nverts in shapes_meta:
            if len(pl['parts']) < 2: continue
            seen = {}
            for p in pl['parts']:
                if p['w_off'] is None or p['bi_off'] is None: continue
                names = [inst[bn] for bn in p['bones']]
                for lk, gv in enumerate(p['vertex_map']):
                    hw = 0.0
                    for s in range(p['nwpv']):
                        w = struct.unpack_from('<f', bad, p['w_off'] + 4 * (p['nwpv'] * lk + s))[0]
                        bi = bad[p['bi_off'] + p['nwpv'] * lk + s]
                        if w > 0 and bi < len(names) and names[bi] == 'NPC Head [Head]': hw += w
                    if gv in seen:
                        if abs(seen[gv] - hw) > 0.05: mp_bad += 1
                    else:
                        seen[gv] = hw
        sev = 0
        msgs = []
        if oob: sev = 9; msgs.append('OUT-OF-BAND diff bytes=%d' % oob)
        if vbuf_bad_off:
            sev = max(sev, 8)
            worst = sorted(vbuf_bad_off.items(), key=lambda kv: -kv[1])[:3]
            msgs.append('VBUF WRONG-OFFSET writes: ' + ', '.join('%s@rec+%d x%d' % (n, ro, c) for (n, ro), c in worst))
        if mp_bad:
            sev = max(sev, 7)
            msgs.append('MULTI-PARTITION disagree verts=%d' % mp_bad)
        if msgs:
            results.append((rel, '; '.join(msgs), sev))

print('files examined: %d, flagged: %d' % (nfiles, len(results)))
for rel, msg, sev in sorted(results, key=lambda r: -r[2]):
    print('  [%d] %-95s %s' % (sev, rel, msg))
