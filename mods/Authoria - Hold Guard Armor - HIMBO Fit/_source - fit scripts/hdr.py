import sys, os, struct, collections
def hdr(p):
    d = open(p, 'rb').read(200)
    nl = d.index(b'\n'); o = nl + 1
    ver = struct.unpack_from('<I', d, o)[0]; o += 5
    uv = struct.unpack_from('<I', d, o)[0]; o += 4
    nb = struct.unpack_from('<I', d, o)[0]; o += 4
    bs = struct.unpack_from('<I', d, o)[0]
    return hex(ver), uv, bs, nb
for root in sys.argv[1:]:
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
            if f.lower().endswith('.nif'):
                p = os.path.join(dp, f)
                print(hdr(p), os.path.relpath(p, root))
