import sys, struct
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from nifrw import Doc, parse_shape_hdr
d = Doc(sys.argv[1])
for t, b in d.blocks:
    if t == 'BSTriShape':
        h = parse_shape_hdr(b)
        print(hex(h['vdesc']), h['nvert'], h['ntri'], h['dsize'], len(h['tail']), (h['vdesc'] & 0xF) * 4, struct.unpack_from('<3f', h['tail'], 0) if len(h['tail']) >= 12 else None, h['bound'])
