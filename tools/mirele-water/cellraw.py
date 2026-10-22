"""Dump the RAW subrecords of one exterior CELL from every plugin that defines it.

The engine does not merge CELL subrecords across plugins — the winning record is used
whole. So a winning override that simply omits XCLW (water height) leaves the cell on the
worldspace default water level, which is far below the terrain, and the cell draws no
water at all. This prints exactly which water subrecords each plugin's copy carries.

  XCLC = grid, XCLW = water height, XCWT = water type, XCLR = regions,
  XCLL = lighting, XLCN = location, XOCN = occlusion data, DATA = cell flags

Usage: python cellraw.py <cell-formid-hex> <plugin.esp> [plugin.esp ...]
"""
import os
import struct
import sys
import zlib

WATER_SUBS = {b'XCLW', b'XCWT', b'XCLC', b'DATA', b'XLCN', b'XOCN', b'XCLL', b'XWEM'}


def read_masters(data):
    size = struct.unpack_from('<I', data, 4)[0]
    body = data[24:24 + size]
    masters, pos = [], 0
    while pos < len(body):
        st = body[pos:pos + 4]
        sl = struct.unpack_from('<H', body, pos + 4)[0]
        if st == b'MAST':
            masters.append(body[pos + 6:pos + 6 + sl].rstrip(b'\x00')
                           .decode('cp1252', 'replace'))
        pos += 6 + sl
    return masters, 24 + size


def iter_records(data, start, want):
    stack = [(start, len(data))]
    while stack:
        pos, end = stack.pop()
        while pos < end:
            typ = data[pos:pos + 4]
            if typ == b'GRUP':
                gsize = struct.unpack_from('<I', data, pos + 4)[0]
                stack.append((pos + gsize, end))
                end = pos + gsize
                pos += 24
                continue
            size, flags, formid = struct.unpack_from('<IIII', data, pos + 4)[0:3]
            if typ in want:
                body = data[pos + 24:pos + 24 + size]
                if flags & 0x00040000:
                    body = zlib.decompress(body[4:])
                yield typ, formid, flags, body
            pos += 24 + size


def subrecords(body):
    pos, out = 0, []
    while pos < len(body):
        st = body[pos:pos + 4]
        sl = struct.unpack_from('<H', body, pos + 4)[0]
        if st == b'XXXX':
            real = struct.unpack_from('<I', body, pos + 6)[0]
            pos += 10
            st = body[pos:pos + 4]
            sl = real
            out.append((st, body[pos + 6:pos + 6 + sl]))
            pos += 6 + sl
            continue
        out.append((st, body[pos + 6:pos + 6 + sl]))
        pos += 6 + sl
    return out


def main():
    local = int(sys.argv[1], 16)
    print('cell %06X — raw subrecords per plugin\n' % local)
    print('%-58s %-9s %-11s %-9s %s' % ('plugin', 'XCLW', 'value', 'XCWT', 'other water-ish subrecords'))
    print('-' * 132)
    for path in sys.argv[2:]:
        if not os.path.exists(path):
            print('%-58s  MISSING FILE' % os.path.basename(path)[:58])
            continue
        data = open(path, 'rb').read()
        masters, start = read_masters(data)
        base = os.path.basename(path)
        hit = False
        for typ, formid, flags, body in iter_records(data, start, {b'CELL'}):
            if (formid & 0xFFFFFF) != local:
                continue
            idx = formid >> 24
            mname = masters[idx] if idx < len(masters) else base
            if mname.lower() != 'skyrim.esm':
                continue
            hit = True
            subs = subrecords(body)
            names = [s[0].decode('ascii', 'replace') for s in subs]
            d = dict(subs)
            xclw = d.get(b'XCLW')
            if xclw is not None and len(xclw) >= 4:
                val = struct.unpack_from('<f', xclw, 0)[0]
                vs = '%.1f' % val if abs(val) < 1e30 else '%.3e' % val
            else:
                vs = '—'
            xcwt = d.get(b'XCWT')
            if xcwt is not None and len(xcwt) >= 4:
                wt = '%08X' % struct.unpack_from('<I', xcwt, 0)[0]
            else:
                wt = '—'
            other = ' '.join(n for n in names if n.encode() in WATER_SUBS and n not in ('XCLW', 'XCWT'))
            print('%-58s %-9s %-11s %-9s %s'
                  % (base[:58], 'yes' if xclw is not None else 'ABSENT', vs, wt, other))
        if not hit:
            print('%-58s  (does not touch this cell)' % base[:58])


if __name__ == '__main__':
    main()
