"""Weld UBE _0 bodies to _1 in the head-skirt band and taper .tri morph deltas there.

Band: f(z)=1 for z>=110.5 (fully pinned to the _1 build shape),
      smoothstep 104.5->110.5, 0 below (full weight-blend/morphs).
Only shapes with the UBE rig signature are touched:
  has 'NPC Spine2 [Spn2]' or 'NPC Head [Head]' bone, NO 'NPC Neck [Neck]' bone,
  and >=1 vertex in Z 104.5..115.5.
In-place edits with mirrored backups. Dry-run by default; pass --write to apply.
"""
import os, sys, struct, shutil, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nifparse import Nif

WRITE = '--write' in sys.argv
BACKUP_ROOT = r"C:\1. AUTHORIA\backups\neckweld-20260730"
MODS = r"C:/1. AUTHORIA/mods"
TARGET_MODS = [
    "Authoria - Bodyslide Output - UBE",
    "Authoria - UBE Converter Output",
    "DDV - Hal's casual outfit - UBE",
    "Fuse00 - Thalmor Investigator UBE",
    "DD - Sigrin Silver Fox armor by Vergi UBE",
    "Ultimate Body Enhancer",
    "Ultimate Body Enhancer - Hotfix",
]
Z_LO, Z_HI, Z_TOP = 104.5, 110.5, 115.5
R_IN, R_OUT = 8.0, 12.0  # neck cylinder: full effect inside R_IN, released by R_OUT

def f_band(p):
    x, y, z = p
    if z <= Z_LO: return 0.0
    if z >= Z_HI:
        fz = 1.0
    else:
        t = (z - Z_LO) / (Z_HI - Z_LO)
        fz = t * t * (3 - 2 * t)
    r = (x * x + y * y) ** 0.5
    if r >= R_OUT: return 0.0
    if r <= R_IN:
        fr = 1.0
    else:
        t = (R_OUT - r) / (R_OUT - R_IN)
        fr = t * t * (3 - 2 * t)
    return fz * fr

def f16_encode(v):
    # float -> half (round to nearest even), clamps to half range
    f32 = struct.unpack('<I', struct.pack('<f', v))[0]
    sign = (f32 >> 16) & 0x8000
    exp = (f32 >> 23) & 0xFF
    man = f32 & 0x7FFFFF
    if exp == 0xFF: return sign | 0x7C00 | (man and 1)
    e = exp - 127 + 15
    if e >= 0x1F: return sign | 0x7C00
    if e <= 0:
        if e < -10: return sign
        man |= 0x800000
        shift = 14 - e
        half_man = man >> shift
        if (man >> (shift - 1)) & 1: half_man += 1
        return sign | half_man
    half = sign | (e << 10) | (man >> 13)
    if (man >> 12) & 1: half += 1
    return half

def layout(desc):
    vsize = (desc & 0xF) * 4
    vf = (desc >> 44) & 0xFFF
    extras = (4 if vf & 0x2 else 0) + (4 if vf & 0x8 else 0) + (4 if vf & 0x10 else 0) \
           + (4 if vf & 0x20 else 0) + (12 if vf & 0x40 else 0) + (4 if vf & 0x100 else 0)
    if not (vf & 0x1): return vsize, None
    if vsize == 16 + extras: return vsize, True   # full precision
    if vsize == 8 + extras: return vsize, False   # half
    raise ValueError('cannot infer precision vsize=%d extras=%d' % (vsize, extras))

def shape_buffers(nif):
    """Per shape name: positions + writable buffer location (partition vbuf or shape vbuf or dynamic)."""
    out = {}
    for i in range(nif.num_blocks):
        bt = nif.btype(i)
        if bt not in ('BSTriShape', 'BSDynamicTriShape'):
            continue
        sh = nif.parse_shape(i)
        name = sh['name']
        info = {'block': i, 'type': bt, 'bones': [], 'positions': None, 'writer': None}
        if sh['skin_ref'] >= 0:
            si = nif.parse_skin_instance(sh['skin_ref'])
            info['bones'] = si['bone_names']
            if bt == 'BSDynamicTriShape':
                # dynamic: float4 positions at block tail
                end = nif.block_offsets[i] + nif.block_sizes[i]
                dyn_off = end - sh['num_vertices'] * 16
                info['positions'] = sh['positions']
                info['writer'] = ('dyn', dyn_off)
            elif si['partition_ref'] >= 0:
                r = nif.block_reader(si['partition_ref'])
                r.u32()  # num partitions
                dsize = r.u32(); vsize = r.u32(); desc = r.u64()
                if dsize > 0:
                    vb_off = r.o
                    nvert = dsize // vsize
                    vs, full = layout(desc)
                    assert vs == vsize
                    pos = []
                    for vi in range(nvert):
                        o = vb_off + vi * vsize
                        if full:
                            pos.append(struct.unpack_from('<3f', nif.data, o))
                        else:
                            rr = nif.block_reader(0); rr.o = o
                            pos.append((rr.f16(), rr.f16(), rr.f16()))
                    info['positions'] = pos
                    info['writer'] = ('vbuf', vb_off, vsize, full)
        elif sh['data_size']:
            vs, full = layout(sh['vertex_desc'])
            info['positions'] = sh['positions']
            info['writer'] = ('vbuf', sh['vbuf_off'], vs, full)
        out.setdefault(name, info)
    return out

def qualifies(info):
    if info['positions'] is None: return False
    bones = set(info['bones'])
    if 'NPC Neck [Neck]' in bones: return False
    if not ({'NPC Spine2 [Spn2]', 'NPC Head [Head]'} & bones): return False
    return any(f_band(p) > 0.0 for p in info['positions'])

def write_pos(buf, writer, vi, p):
    kind = writer[0]
    if kind == 'dyn':
        off = writer[1] + vi * 16
        struct.pack_into('<3f', buf, off, *p)
    else:
        _, base, vsize, full = writer
        off = base + vi * vsize
        if full:
            struct.pack_into('<3f', buf, off, *p)
        else:
            struct.pack_into('<3H', buf, off, f16_encode(p[0]), f16_encode(p[1]), f16_encode(p[2]))

def backup(path):
    rel = os.path.relpath(path, MODS)
    dst = os.path.join(BACKUP_ROOT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy2(path, dst)

def process_set(base, n0, n1, tri):
    """base: path without suffix. n0/n1/tri: existing file paths or None. Returns report dict."""
    rep = {'base': base.replace(MODS + '/', ''), 'shapes': [], 'welded': 0, 'tapered': 0, 'skip': None}
    ref_path = n1 or n0  # single-weight sets use the lone nif
    try:
        nif1 = Nif(ref_path)
        shapes1 = shape_buffers(nif1)
    except Exception as e:
        rep['skip'] = 'parse fail %s: %s' % (os.path.basename(ref_path), e)
        return rep
    qual = {n: s for n, s in shapes1.items() if qualifies(s)}
    if not qual:
        rep['skip'] = 'no qualifying shapes'
        return rep
    rep['shapes'] = sorted(qual)

    # WELD _0 -> _1 in band
    if n0 and n1:
        try:
            nif0 = Nif(n0)
            shapes0 = shape_buffers(nif0)
        except Exception as e:
            rep['skip'] = 'parse fail _0: %s' % e
            return rep
        buf0 = bytearray(nif0.data)
        changed = 0
        for name, s1 in qual.items():
            s0 = shapes0.get(name)
            if not s0 or s0['positions'] is None or s0['writer'] is None: continue
            if len(s0['positions']) != len(s1['positions']): continue
            for vi, p1 in enumerate(s1['positions']):
                fz = f_band(p1)
                if fz <= 0.0: continue
                p0 = s0['positions'][vi]
                d2 = (p0[0]-p1[0])**2 + (p0[1]-p1[1])**2 + (p0[2]-p1[2])**2
                if d2 < 1e-8: continue
                np_ = tuple(p0[k] + (p1[k] - p0[k]) * fz for k in range(3))
                write_pos(buf0, s0['writer'], vi, np_)
                changed += 1
        rep['welded'] = changed
        if changed and WRITE:
            backup(n0)
            with open(n0, 'wb') as f:
                f.write(buf0)

    # TAPER tri morph deltas in band
    if tri:
        d = open(tri, 'rb').read()
        buf = bytearray(d)
        if d[:4] != b'PIRT':
            rep['skip'] = (rep['skip'] or '') + ' tri not TRIP'
            return rep
        o = 4
        nshapes = struct.unpack_from('<H', d, o)[0]; o += 2
        tapered = 0
        for _ in range(nshapes):
            ln = d[o]; o += 1
            sname = d[o:o+ln].decode('ascii', 'replace'); o += ln
            nmorph = struct.unpack_from('<H', d, o)[0]; o += 2
            s1 = qual.get(sname)
            pos = s1['positions'] if s1 else None
            for _m in range(nmorph):
                ml = d[o]; o += 1
                o += ml  # name
                o += 4   # mult
                nd = struct.unpack_from('<H', d, o)[0]; o += 2
                for _k in range(nd):
                    idx = struct.unpack_from('<H', d, o)[0]
                    if pos is not None and idx < len(pos):
                        fz = f_band(pos[idx])
                        if fz > 0.0:
                            dx, dy, dz = struct.unpack_from('<3h', d, o + 2)
                            scale = 1.0 - fz
                            ndx, ndy, ndz = int(round(dx*scale)), int(round(dy*scale)), int(round(dz*scale))
                            if (ndx, ndy, ndz) != (dx, dy, dz):
                                struct.pack_into('<3h', buf, o + 2, ndx, ndy, ndz)
                                tapered += 1
                    o += 8
        rep['tapered'] = tapered
        if tapered and WRITE:
            backup(tri)
            with open(tri, 'wb') as f:
                f.write(buf)
    return rep

def main():
    # collect file sets per relative path; later mods in TARGET_MODS DON'T override —
    # duplicates across mods are resolved by picking the mod that wins the VFS.
    sets = {}
    dup_paths = []
    for mod in TARGET_MODS:
        root = os.path.join(MODS, mod, 'meshes')
        if not os.path.isdir(root): continue
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                lf = fn.lower()
                if not (lf.endswith('.tri') or lf.endswith('.nif')): continue
                full = os.path.join(dirpath, fn).replace('\\', '/')
                rel = os.path.relpath(full, os.path.join(MODS, mod)).replace('\\', '/').lower()
                # base key: strip _0/_1/.tri
                if lf.endswith('_0.nif'): base = rel[:-6]; kind = '0'
                elif lf.endswith('_1.nif'): base = rel[:-6]; kind = '1'
                elif lf.endswith('.tri'): base = rel[:-4]; kind = 't'
                else: base = rel[:-4]; kind = 'n'
                entry = sets.setdefault(base, {})
                if kind in entry and entry[kind][0] != mod:
                    dup_paths.append((base, kind, entry[kind][0], mod))
                    continue  # keep first (earlier in TARGET_MODS = output mods first)
                entry.setdefault(kind, (mod, full))
    print('file sets: %d  (dup shadowed: %d)' % (len(sets), len(dup_paths)))

    reports = []
    for base, entry in sorted(sets.items()):
        n0 = entry.get('0', (None, None))[1]
        n1 = entry.get('1', (None, None))[1]
        tri = entry.get('t', (None, None))[1]
        single = entry.get('n', (None, None))[1]
        if not tri and not (n0 and n1):
            continue  # nothing to do (no weight pair, no morphs)
        if not n1 and single: n1 = single
        if not (n1 or n0): continue
        rep = process_set(base, n0, n1, tri)
        reports.append(rep)

    acted = [r for r in reports if not r['skip'] and (r['welded'] or r['tapered'])]
    skipped = [r for r in reports if r['skip'] and 'no qualifying' not in (r['skip'] or '')]
    print('\n%s MODE' % ('WRITE' if WRITE else 'DRY-RUN'))
    print('sets touched: %d' % len(acted))
    for r in acted:
        print('  %-95s weld=%-5d taper=%-5d shapes=%s' % (r['base'][:95], r['welded'], r['tapered'], ','.join(r['shapes'])))
    if skipped:
        print('\nskipped with issues: %d' % len(skipped))
        for r in skipped:
            print('  %-95s %s' % (r['base'][:95], r['skip']))
    json.dump(reports, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weld_report.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
