"""Parse Bethesda FaceGen FRTRI003 head tri: base verts + dense morphs (validated chain-walk)."""
import struct

def parse(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'FRTRI003', d[:8]
    hdr = struct.unpack_from('<10i', d, 8)
    nv, nt = hdr[0], hdr[1]
    nmorph = hdr[7]
    # base vertices follow the 0x40-byte header region in most exports; find by validation:
    base_off = None
    for cand in (48, 56, 64):
        try:
            zs = [struct.unpack_from('<3f', d, cand + i * 12)[2] for i in range(0, nv, 997)]
        except struct.error:
            continue
        if all(-200 < z < 400 for z in zs) and max(zs) > 50:
            base_off = cand
            break
    assert base_off is not None, 'base verts not found'
    verts = [struct.unpack_from('<3f', d, base_off + i * 12) for i in range(nv)]

    def chain(start):
        """try to walk morph records from start; return list of (off, name, scale_off, delta_off) or None"""
        recs, o = [], start
        while len(recs) < nmorph:
            if o + 8 > len(d): return None
            ln = struct.unpack_from('<I', d, o)[0]
            if not (1 <= ln <= 64): return None
            name = d[o+4:o+4+ln]
            if not all((32 <= b < 127) or b == 0 for b in name): return None
            scale_off = o + 4 + ln
            delta_off = scale_off + 4
            nxt = delta_off + nv * 6
            if nxt > len(d): return None
            recs.append((o, name.rstrip(b'\x00').decode('ascii'), scale_off, delta_off))
            o = nxt
        return recs if o <= len(d) else None

    # find the earliest offset from which exactly nmorph records fit
    recs = None
    for start in range(base_off + nv * 12, len(d) - nv * 6):
        ln = struct.unpack_from('<I', d, start)[0]
        if 1 <= ln <= 64:
            s = d[start+4:start+4+ln]
            if s and all((32 <= b < 127) or b == 0 for b in s) and any(65 <= b <= 122 for b in s):
                r = chain(start)
                if r:
                    recs = r
                    break
    assert recs, 'morph chain not found'
    return d, nv, verts, recs
