import struct, zlib, io, sys

def records(data, off, end, depth=0):
    """Yield (sig, size, flags, formid, ver, dataoff, datalen) for records; recurse GRUPs."""
    while off < end:
        sig = data[off:off+4]
        if sig == b'GRUP':
            gsize, label, gtype = struct.unpack('<I4si', data[off+4:off+16])
            yield ('GRUP', gtype, label, off, gsize)
            for r in records(data, off+24, off+gsize, depth+1):
                yield r
            off += gsize
        else:
            size, flags, fid, ts, ver = struct.unpack('<IIIHH', data[off+4:off+20])
            yield ('REC', sig, flags, fid, off+24, size)
            off += 24 + size

def rec_data(data, off, size, flags):
    d = data[off:off+size]
    if flags & 0x00040000:
        dsize = struct.unpack('<I', d[:4])[0]
        d = zlib.decompress(d[4:])
    return d

def subs(d):
    off=0; big=0
    while off < len(d):
        s = d[off:off+4]; sz = struct.unpack('<H', d[off+4:off+6])[0]
        off += 6
        if s == b'XXXX':
            big = struct.unpack('<I', d[off:off+4])[0]; off += sz; continue
        if big: sz = big; big = 0
        yield s, d[off:off+sz]
        off += sz
