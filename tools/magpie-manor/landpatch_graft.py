"""Graft Northern Roads' corner vertices into the Magpie LAND copies inside the landscape patch,
and set the ESL flag on the TES4 header. Rewrites the plugin with correct group sizes.
Usage: python landpatch_graft.py <patch.esp>
"""
import sys, struct, zlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landscan import find_land, subrecords

VAN = r"C:\1. AUTHORIA\Stock Game\Data\Skyrim.esm"
NR  = r"C:\1. AUTHORIA\mods\Northern Roads\Northern Roads.esp"
MAG = r"C:\1. AUTHORIA\mods\Magpie Manor\MagpieManor.esp"
TARGETS = {0x000A5CC: "(21,-1)", 0x000A5CD: "(20,-1)"}   # Magpie copies that receive NR's corner vertices

def parse(data, pos, end):
    nodes = []
    while pos < end:
        typ = data[pos:pos+4]
        if typ == b'GRUP':
            gsize = struct.unpack_from('<I', data, pos+4)[0]
            hdr = bytearray(data[pos:pos+24])
            children = parse(data, pos+24, pos+gsize)
            nodes.append(['GRUP', hdr, children])
            pos += gsize
        else:
            size = struct.unpack_from('<I', data, pos+4)[0]
            hdr = bytearray(data[pos:pos+24])
            body = bytearray(data[pos+24:pos+24+size])
            nodes.append(['REC', hdr, body])
            pos += 24 + size
    return nodes

def serialize(nodes):
    out = bytearray()
    for n in nodes:
        if n[0] == 'GRUP':
            inner = serialize(n[2])
            hdr = bytearray(n[1]); struct.pack_into('<I', hdr, 4, 24 + len(inner))
            out += hdr + inner
        else:
            hdr = bytearray(n[1]); struct.pack_into('<I', hdr, 4, len(n[2]))
            out += hdr + n[2]
    return bytes(out)

def walk(nodes):
    for n in nodes:
        if n[0] == 'GRUP':
            yield from walk(n[2])
        else:
            yield n

def encode_vhgt(H, offset):
    raw = bytearray(1089)
    prev_rowstart = 0.0
    for y in range(33):
        h0 = H[(0, y)] / 8.0 - offset
        d = int(round(h0 - prev_rowstart)); raw[y*33] = d & 0xFF; prev_rowstart += d; cur = prev_rowstart
        for x in range(1, 33):
            hx = H[(x, y)] / 8.0 - offset
            d = int(round(hx - cur)); raw[y*33 + x] = d & 0xFF; cur += d
    return bytes(raw)

def main(path):
    data = open(path, 'rb').read()
    assert data[:4] == b'TES4'
    tes4_size = struct.unpack_from('<I', data, 4)[0]
    tes4 = bytearray(data[:24 + tes4_size])
    masters = [p.rstrip(b'\0').decode('cp1252') for st, p in subrecords(bytes(tes4[24:])) if st == b'MAST']
    sky_idx = [m.lower() for m in masters].index('skyrim.esm')
    nodes = parse(data, 24 + tes4_size, len(data))
    changed = 0
    for n in walk(nodes):
        if n[1][0:4] != b'LAND': continue
        flags, fid = struct.unpack_from('<II', n[1], 8)
        if (fid >> 24) != sky_idx or (fid & 0xFFFFFF) not in TARGETS: continue
        label = TARGETS[fid & 0xFFFFFF]
        body = bytes(n[2]); compressed = bool(flags & 0x40000)
        if compressed:
            body = zlib.decompress(body[4:])
        # locate VHGT
        pos = 0; vh_off = None
        while pos < len(body):
            st = body[pos:pos+4]; sl = struct.unpack_from('<H', body, pos+4)[0]
            if st == b'VHGT': vh_off = pos + 6; break
            pos += 6 + sl
        assert vh_off is not None
        vhgt = body[vh_off:vh_off+1096]
        offset = struct.unpack_from('<f', vhgt, 0)[0]
        Hv, _ = find_land(VAN, fid & 0xFFFFFF); Hn, _ = find_land(NR, fid & 0xFFFFFF); Hm, _ = find_land(MAG, fid & 0xFFFFFF)
        merged = dict(Hm)
        nr_changed = [k for k in Hv if abs(Hn[k]-Hv[k]) > 0.01]
        for k in nr_changed: merged[k] = Hn[k]
        # sanity: the patch body must currently encode Magpie's heights
        cur_raw = vhgt[4:4+1089]
        mag_raw = encode_vhgt(Hm, offset)
        assert cur_raw == mag_raw, f"{label}: patch VHGT is not Magpie's encoding (offset {offset})"
        new_raw = encode_vhgt(merged, offset)
        nbytes = sum(1 for i in range(1089) if new_raw[i] != cur_raw[i])
        newbody = bytearray(body); newbody[vh_off+4:vh_off+4+1089] = new_raw
        if compressed:
            comp = zlib.compress(bytes(newbody), 9)
            n[2] = bytearray(struct.pack('<I', len(newbody)) + comp)
        else:
            n[2] = newbody
        print(f"{label}: grafted {len(nr_changed)} NR vertices -> {nbytes} VHGT bytes changed; compressed={compressed}")
        changed += 1
    assert changed == 2, changed
    # ESL flag on TES4
    flags = struct.unpack_from('<I', tes4, 8)[0]
    struct.pack_into('<I', tes4, 8, flags | 0x200)
    out = bytes(tes4) + serialize(nodes)
    bak = path + ".pre-graft"
    if not os.path.exists(bak): open(bak, 'wb').write(data)
    open(path, 'wb').write(out)
    print(f"written {len(out)} bytes (was {len(data)}); ESL flag set; backup at {bak}")

if __name__ == '__main__':
    main(sys.argv[1])
