"""Scan Skyrim plugins for LAND records by FormID and compare VHGT heightmaps.
Usage: python landscan.py <formid-hex> <label=path> [<label=path> ...]
The FormID is the load-order-independent local id with master index 00 assumed to be Skyrim.esm (e.g. 000A5CC).
We match by the low 24 bits and require the record's master index to resolve to Skyrim.esm in that plugin's master list.
"""
import struct, sys, zlib, os

def read_masters(data):
    # TES4 header record
    typ = data[0:4]
    assert typ == b'TES4', typ
    size = struct.unpack_from('<I', data, 4)[0]
    body = data[24:24+size]
    masters = []
    pos = 0
    while pos < len(body):
        st = body[pos:pos+4]; sl = struct.unpack_from('<H', body, pos+4)[0]
        payload = body[pos+6:pos+6+sl]
        if st == b'MAST':
            masters.append(payload.rstrip(b'\0').decode('cp1252', 'replace'))
        pos += 6 + sl
    return masters, 24 + size

def iter_records(data, start, want_types):
    """Yield (type, formid, flags, body_bytes) for records of want_types anywhere (recursing into groups)."""
    pos = start
    end = len(data)
    stack = [(pos, end)]
    while stack:
        pos, end = stack.pop()
        while pos < end:
            typ = data[pos:pos+4]
            if typ == b'GRUP':
                gsize = struct.unpack_from('<I', data, pos+4)[0]
                # descend
                stack.append((pos + gsize, end))
                end = pos + gsize
                pos = pos + 24
                continue
            size, flags, formid = struct.unpack_from('<IIII', data, pos+4)[0:3]
            hdr = 24
            if typ in want_types:
                body = data[pos+hdr:pos+hdr+size]
                if flags & 0x00040000:
                    dsize = struct.unpack_from('<I', body, 0)[0]
                    body = zlib.decompress(body[4:])
                yield typ, formid, flags, body
            pos += hdr + size

def subrecords(body):
    pos = 0; out = []
    while pos < len(body):
        st = body[pos:pos+4]; sl = struct.unpack_from('<H', body, pos+4)[0]
        if st == b'XXXX':
            real = struct.unpack_from('<I', body, pos+6)[0]
            pos += 6 + 4
            st = body[pos:pos+4]; sl = real
            payload = body[pos+6:pos+6+sl]
            out.append((st, payload)); pos += 6 + sl
            continue
        out.append((st, body[pos+6:pos+6+sl])); pos += 6 + sl
    return out

def heights_from_vhgt(vhgt):
    off = struct.unpack_from('<f', vhgt, 0)[0]
    raw = vhgt[4:4+1089]
    H = {}
    rowstart = 0.0
    for y in range(33):
        d = raw[y*33]; d = d - 256 if d > 127 else d
        rowstart += d
        h = rowstart
        H[(0, y)] = h
        for x in range(1, 33):
            d = raw[y*33 + x]; d = d - 256 if d > 127 else d
            h += d
            H[(x, y)] = h
    return {k: (off + v) * 8 for k, v in H.items()}

def find_land(path, local_id):
    with open(path, 'rb') as f:
        data = f.read()
    masters, start = read_masters(data)
    base = os.path.basename(path)
    for typ, formid, flags, body in iter_records(data, start, {b'LAND'}):
        idx = formid >> 24
        low = formid & 0xFFFFFF
        if low != local_id: continue
        # resolve master
        mname = masters[idx] if idx < len(masters) else base
        if mname.lower() != 'skyrim.esm': continue
        subs = subrecords(body)
        vhgt = None; layers = []
        for st, payload in subs:
            if st == b'VHGT': vhgt = payload
            elif st in (b'BTXT', b'ATXT'):
                tex = struct.unpack_from('<I', payload, 0)[0]
                quad = payload[4]
                layers.append((st.decode(), tex, quad))
        return heights_from_vhgt(vhgt) if vhgt else None, layers
    return None, None

def main():
    local_id = int(sys.argv[1], 16)
    entries = [a.split('=', 1) for a in sys.argv[2:]]
    results = {}
    for label, path in entries:
        H, layers = find_land(path, local_id)
        results[label] = (H, layers)
        print(f"{label}: {'found' if H else 'NOT FOUND'}; layers={len(layers) if layers else 0}")
    labels = [e[0] for e in entries]
    base = labels[0]
    Hb, Lb = results[base]
    for lab in labels[1:]:
        Ho, Lo = results[lab]
        if Ho is None or Hb is None: continue
        diffs = [(k, Ho[k]-Hb[k]) for k in Hb if abs(Ho[k]-Hb[k]) > 0.01]
        print(f"\n=== {lab} vs {base}: {len(diffs)}/1089 vertices differ")
        if diffs:
            ds = [d for _, d in diffs]
            print(f"  delta min {min(ds):.1f} max {max(ds):.1f} units")
            for y in range(32, -1, -1):
                row = ''.join('.' if abs(Ho[(x,y)]-Hb[(x,y)]) <= 0.01 else ('+' if Ho[(x,y)]-Hb[(x,y)] > 0 else '-') for x in range(33))
                print(f"  y={y:2d} {row}")
        if Lo != Lb:
            print(f"  texture layers differ: {base}={len(Lb)} layers, {lab}={len(Lo)} layers")
    # pairwise between the non-base ones (e.g. NR vs Magpie): where both changed vanilla
    if len(labels) >= 3:
        for i in range(1, len(labels)):
            for j in range(i+1, len(labels)):
                Hi = results[labels[i]][0]; Hj = results[labels[j]][0]
                if Hi is None or Hj is None: continue
                both = [k for k in Hb if abs(Hi[k]-Hb[k]) > 0.01 and abs(Hj[k]-Hb[k]) > 0.01]
                conflict = [k for k in both if abs(Hi[k]-Hj[k]) > 0.01]
                print(f"\n=== overlap {labels[i]} & {labels[j]}: both changed {len(both)} vertices; disagree on {len(conflict)}")
                if conflict:
                    for y in range(32, -1, -1):
                        row = ''.join('X' if (x,y) in conflict else ('i' if abs(Hi[(x,y)]-Hb[(x,y)])>0.01 else ('j' if abs(Hj[(x,y)]-Hb[(x,y)])>0.01 else '.')) for x in range(33))
                        print(f"  y={y:2d} {row}")

if __name__ == '__main__':
    main()
