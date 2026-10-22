import struct, sys
for f in sys.argv[1:]:
    b = open(f, "rb").read()
    sz = struct.unpack_from("<I", b, 4)[0]
    flags = struct.unpack_from("<I", b, 8)[0]
    p = 24; end = 24 + sz; ms = []
    while p < end:
        sig = b[p:p+4].decode("latin1"); ln = struct.unpack_from("<H", b, p+4)[0]
        if sig == "MAST": ms.append(b[p+6:p+6+ln-1].decode("latin1"))
        p += 6 + ln
    print(f.split("/")[-1], hex(flags), ms)
