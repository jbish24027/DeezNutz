"""nif_blocks.py - raw block-level dump of a Skyrim SE nif (20.2.0.7 / user 12 / stream 100): per block its type and size, and for every
BSTriShape and NiSkinPartition the fields the engine sizes its buffers from (vertex desc -> stride, numVertices, numTriangles, dataSize,
per-partition counts and vertex maps). Flags a block whose declared sizes disagree with its counts. usage: nif_blocks.py [--quiet] <nif> ...
(--quiet prints only files with a flagged block)"""
import sys, struct, os


def rd(fmt, b, o):
    v = struct.unpack_from('<' + fmt, b, o); return v, o + struct.calcsize('<' + fmt)


def parse(path):
    b = open(path, 'rb').read()
    o = b.index(b'\n') + 1                      # header string
    (ver,), o = rd('I', b, o); (endian,), o = rd('B', b, o); (uv,), o = rd('I', b, o); (nblocks,), o = rd('I', b, o); (uv2,), o = rd('I', b, o)
    for _ in range(3):                           # export info: 3 short strings (len byte + chars)
        (ln,), o = rd('B', b, o); o += ln
    (ntypes,), o = rd('H', b, o); types = []
    for _ in range(ntypes):
        (ln,), o = rd('I', b, o); types.append(b[o:o + ln].decode('latin1')); o += ln
    tidx, o = rd(f'{nblocks}H', b, o); sizes, o = rd(f'{nblocks}I', b, o)
    (nstr,), o = rd('I', b, o); (maxlen,), o = rd('I', b, o); strings = []
    for _ in range(nstr):
        (ln,), o = rd('I', b, o); strings.append(b[o:o + ln].decode('latin1')); o += ln
    (ngroups,), o = rd('I', b, o); o += 4 * ngroups
    starts = []; p = o
    for i in range(nblocks): starts.append(p); p += sizes[i]
    return b, types, tidx, sizes, strings, starts


def desc_stride(desc):
    return (desc & 0xF) * 4


def flags_of(desc):
    f = (desc >> 44) & 0xFFF; names = {0x1: 'VERTEX', 0x2: 'UVS', 0x4: 'UVS_2', 0x8: 'NORMALS', 0x10: 'TANGENTS', 0x20: 'COLORS', 0x40: 'SKINNED', 0x80: 'LANDDATA', 0x100: 'EYEDATA', 0x400: 'FULL_PREC'}
    return '|'.join(n for k, n in names.items() if f & k)


def tri_shape(b, o, strings):
    (nm,), o = rd('i', b, o); (nx,), o = rd('I', b, o); o += 4 * nx; o += 4            # name, extra data, controller
    (flags,), o = rd('I', b, o); o += 12 + 36 + 4; o += 4                               # translation, rotation, scale, collision
    o += 16                                                                              # bounding sphere
    (skin, shader, alpha), o = rd('iii', b, o)
    (desc,), o = rd('Q', b, o); (ntri,), o = rd('I', b, o); (nvert,), o = rd('H', b, o); (dsize,), o = rd('I', b, o)
    return dict(name=strings[nm] if nm >= 0 else '?', flags=flags, skin=skin, shader=shader, alpha=alpha, desc=desc, stride=desc_stride(desc), vflags=flags_of(desc), ntri=ntri, nvert=nvert, dsize=dsize)


def skin_partition(b, o):
    (npart,), o = rd('I', b, o); (dsize,), o = rd('I', b, o); (vsize,), o = rd('I', b, o); (desc,), o = rd('Q', b, o)
    hdr = dict(npart=npart, dsize=dsize, vsize=vsize, desc=desc, stride=desc_stride(desc), vflags=flags_of(desc))
    nv_total = dsize // vsize if vsize else 0; hdr['nvert_in_data'] = nv_total; hdr['data_remainder'] = dsize - nv_total * vsize if vsize else dsize
    o += dsize                                                                            # the vertex data
    parts = []
    for i in range(npart):
        (nv, ntri, nbones, nstrips, nwpv), o = rd('HHHHH', b, o)
        o += 2 * nbones
        (hasvm,), o = rd('B', b, o); vm = []
        if hasvm: vm, o = rd(f'{nv}H', b, o)
        (hasw,), o = rd('B', b, o)
        if hasw: o += 4 * nwpv * nv
        o += 2 * nstrips
        (hasf,), o = rd('B', b, o)
        if hasf: o += 6 * ntri
        (hasb,), o = rd('B', b, o)
        if hasb: o += nwpv * nv
        (unk,), o = rd('H', b, o)                                                         # 'Unknown Short' (user version 2 > 34)
        (pdesc,), o = rd('Q', b, o); tm, o = rd(f'{3 * ntri}H', b, o)
        parts.append(dict(nv=nv, ntri=ntri, nbones=nbones, nwpv=nwpv, vmap_max=max(vm) if vm else None, vmap_n=len(vm), tri_max=max(tm) if tm else None, pdesc_stride=desc_stride(pdesc)))
    return hdr, parts


QUIET = '--quiet' in sys.argv
for path in ([a for a in sys.argv[1:] if a != '--quiet'] if __name__ == '__main__' else []):
    try:
        b, types, tidx, sizes, strings, starts = parse(path)
    except Exception as e:
        print(f'== {path}: UNPARSEABLE {e!r}'); continue
    lines = []; bad = []; big = []
    lines.append(f'== {path} ({os.path.getsize(path)} B): ' + ', '.join(f'{t}x{sum(1 for i in tidx if types[i] == t)}' for t in sorted(set(types), key=types.index)))
    for i, (ti, sz, st) in enumerate(zip(tidx, sizes, starts)):
        t = types[ti]
        if t == 'BSTriShape':
            try:
                d = tri_shape(b, st, strings)
            except Exception as e:
                bad.append(f'BSTriShape block {i}: unparseable {e!r}'); continue
            exp = d['nvert'] * d['stride'] + d['ntri'] * 6
            if d['skin'] < 0 and d['dsize'] != exp: bad.append(f'{d["name"]!r}: unskinned dataSize {d["dsize"]} != {exp}')
            if d['skin'] >= 0 and (d['nvert'] or d['dsize']): bad.append(f'{d["name"]!r}: skinned shape carries its own vertex data (nvert {d["nvert"]}, dataSize {d["dsize"]})')
            if d['skin'] >= 0 and 'SKINNED' not in d['vflags']: bad.append(f'{d["name"]!r}: skinned shape without the SKINNED vertex flag')
            if d['shader'] < 0 and not (d['flags'] & 1): big.append(f'{d["name"]!r} (visible, no shader)')
            lines.append(f'   [{i:2d}] BSTriShape {d["name"]!r} | flags {d["flags"]:#x} skin {d["skin"]} shader {d["shader"]} | stride {d["stride"]} {d["vflags"]} | nvert {d["nvert"]} ntri {d["ntri"]} dataSize {d["dsize"]}')
        elif t == 'NiSkinPartition':
            try:
                h, parts = skin_partition(b, st)
            except Exception as e:
                bad.append(f'NiSkinPartition block {i}: unparseable {e!r}'); continue
            nvd = h['nvert_in_data']
            if h['data_remainder']: bad.append(f'partition block {i}: dataSize {h["dsize"]} not a multiple of vsize {h["vsize"]}')
            if h['vsize'] != h['stride']: bad.append(f'partition block {i}: vsize {h["vsize"]} != desc stride {h["stride"]}')
            if sum(p['nv'] for p in parts) != nvd: bad.append(f'partition block {i}: parts nv sum {sum(p["nv"] for p in parts)} != verts in data {nvd}')
            for j, p in enumerate(parts):
                if p['vmap_max'] is not None and p['vmap_max'] >= nvd: bad.append(f'partition block {i} part {j}: vmap max {p["vmap_max"]} >= verts in data {nvd}')
                if p['tri_max'] is not None and p['tri_max'] >= nvd: bad.append(f'partition block {i} part {j}: tri idx max {p["tri_max"]} >= verts in data {nvd}')
                if p['vmap_n'] != p['nv']: bad.append(f'partition block {i} part {j}: vmap {p["vmap_n"]} entries for nv {p["nv"]}')
                if p['nwpv'] != 4: bad.append(f'partition block {i} part {j}: {p["nwpv"]} weights per vertex')
            lines.append(f'   [{i:2d}] NiSkinPartition | parts {h["npart"]} dataSize {h["dsize"]} vsize {h["vsize"]} {h["vflags"]} | verts in data {nvd}' + ''.join(f' | p{j}: nv {p["nv"]} ntri {p["ntri"]} bones {p["nbones"]} vmap max {p["vmap_max"]} tri max {p["tri_max"]}' for j, p in enumerate(parts)))
    if bad or not QUIET:
        print('\n'.join(lines))
        for m in bad: print('   <<< ' + m)
        if big: print('   note: visible shapes without a shader: ' + ', '.join(big))
        print()
