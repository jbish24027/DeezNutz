"""Structural census: top-level GRUP labels and record counts (headers only, no field parsing)."""
import struct, sys, collections, zlib
def census(path):
    b = open(path, "rb").read()
    o = 0
    # TES4
    sz = struct.unpack_from("<I", b, 4)[0]
    o = 24 + sz
    out = collections.Counter()
    def walk(start, end, top):
        p = start
        while p < end:
            sig = b[p:p+4].decode("latin1")
            size = struct.unpack_from("<I", b, p+4)[0]
            if sig == "GRUP":
                walk(p + 24, p + size, top)
                p += size
            else:
                out[sig] += 1
                p += 24 + size
    while o < len(b):
        sig = b[o:o+4]
        size = struct.unpack_from("<I", b, o+4)[0]
        label = b[o+8:o+12].decode("latin1")
        walk(o + 24, o + size, label)
        o += size
    return out
for f in sys.argv[1:]:
    c = census(f)
    print("==", f.split("/")[-1], dict(sorted(c.items())))
