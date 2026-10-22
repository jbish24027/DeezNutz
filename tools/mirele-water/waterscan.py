"""Map terrain height vs cell water height across a block of Tamriel cells.

Shows, per vertex, whether the ground sits BELOW the water plane (water visible)
or ABOVE it (dry). Compares a reference plugin (vanilla) against the winner so a
lost patch of water shows up as an explicit mark.

Usage: python waterscan.py <label=path> [<label=path> ...]
"""
import struct, sys, zlib, os

WATER_Z = 600.0

# cell grid -> LAND local formid (LAND = CELL + 0x1000)
CELLS = {}
for i, x in enumerate([0, -1, -2, -3, -4]):
    CELLS[(x, -13)] = 0x00AB4F + i
    CELLS[(x, -14)] = 0x00AB70 + i
    CELLS[(x, -15)] = 0x00AB91 + i
    CELLS[(x, -16)] = 0x00ABB2 + i
    CELLS[(x, -17)] = 0x00ABD3 + i

XS = [-4, -3, -2, -1, 0]                  # west -> east (left -> right)
YS = [-13, -14, -15, -16, -17]            # north -> south (top -> bottom)

# CELL water height as the load order resolves it (houseCARL): rows -14..-16 hold
# the lake at Z=600; rows -13 and -17 are flagged "no water at all".
HAS_WATER = {y: (y in (-14, -15, -16)) for y in YS}


def read_masters(data):
    typ = data[0:4]
    assert typ == b'TES4', typ
    size = struct.unpack_from('<I', data, 4)[0]
    body = data[24:24 + size]
    masters = []
    pos = 0
    while pos < len(body):
        st = body[pos:pos + 4]
        sl = struct.unpack_from('<H', body, pos + 4)[0]
        payload = body[pos + 6:pos + 6 + sl]
        if st == b'MAST':
            masters.append(payload.rstrip(b'\x00').decode('cp1252', 'replace'))
        pos += 6 + sl
    return masters, 24 + size


def iter_records(data, start, want_types):
    end = len(data)
    stack = [(start, end)]
    while stack:
        pos, end = stack.pop()
        while pos < end:
            typ = data[pos:pos + 4]
            if typ == b'GRUP':
                gsize = struct.unpack_from('<I', data, pos + 4)[0]
                stack.append((pos + gsize, end))
                end = pos + gsize
                pos = pos + 24
                continue
            size, flags, formid = struct.unpack_from('<IIII', data, pos + 4)[0:3]
            if typ in want_types:
                body = data[pos + 24:pos + 24 + size]
                if flags & 0x00040000:
                    body = zlib.decompress(body[4:])
                yield typ, formid, flags, body
            pos += 24 + size


def subrecords(body):
    pos = 0
    out = []
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


def heights_from_vhgt(vhgt):
    off = struct.unpack_from('<f', vhgt, 0)[0]
    raw = vhgt[4:4 + 1089]
    H = {}
    rowstart = 0.0
    for y in range(33):
        d = raw[y * 33]
        d = d - 256 if d > 127 else d
        rowstart += d
        h = rowstart
        H[(0, y)] = h
        for x in range(1, 33):
            d = raw[y * 33 + x]
            d = d - 256 if d > 127 else d
            h += d
            H[(x, y)] = h
    return {k: (off + v) * 8 for k, v in H.items()}


def scan_plugin(path, wanted_ids):
    with open(path, 'rb') as f:
        data = f.read()
    masters, start = read_masters(data)
    base = os.path.basename(path)
    found = {}
    for typ, formid, flags, body in iter_records(data, start, {b'LAND'}):
        low = formid & 0xFFFFFF
        if low not in wanted_ids:
            continue
        idx = formid >> 24
        mname = masters[idx] if idx < len(masters) else base
        if mname.lower() != 'skyrim.esm':
            continue
        for st, payload in subrecords(body):
            if st == b'VHGT':
                found[low] = heights_from_vhgt(payload)
                break
    return found


def build_map(found):
    """Stitch cells into one grid keyed by (gx, gy), origin at NW corner."""
    grid = {}
    for cy, y in enumerate(YS):
        for cx, x in enumerate(XS):
            lid = CELLS[(x, y)]
            H = found.get(lid)
            if H is None:
                continue
            for vy in range(33):
                for vx in range(33):
                    # vertex y=0 is the SOUTH edge of the cell -> flip for display
                    gx = cx * 32 + vx
                    gy = cy * 32 + (32 - vy)
                    grid[(gx, gy)] = H[(vx, vy)]
    return grid


def render(grid, step=2):
    lines = []
    for gy in range(0, len(YS) * 32 + 1, step):
        cy = min(gy // 32, len(YS) - 1)
        wet_cell = HAS_WATER[YS[cy]]
        row = []
        for gx in range(0, len(XS) * 32 + 1, step):
            z = grid.get((gx, gy))
            if z is None:
                row.append(' ')
            elif z < WATER_Z:
                row.append('~' if wet_cell else 'X')
            else:
                row.append('#' if wet_cell else '.')
        lines.append(''.join(row))
    return lines


def main():
    entries = [a.split('=', 1) for a in sys.argv[1:]]
    wanted = set(CELLS.values())
    results = {}
    for label, path in entries:
        found = scan_plugin(path, wanted)
        results[label] = build_map(found)
        missing = [k for k, v in CELLS.items() if v not in found]
        print('%-28s LAND records found: %d/%d  missing cells: %s'
              % (label, len(found), len(wanted), missing if missing else 'none'))

    labels = [e[0] for e in entries]
    print('\nwater line Z = %.0f    ~ = ground below water (wet)   # = ground above water (dry)' % WATER_Z)
    print('columns: cells x=-4..0 (west->east)   rows: cells y=-14..-16 (north->south)\n')
    for lab in labels:
        g = results[lab]
        if not g:
            continue
        print('--- %s' % lab)
        for line in render(g):
            print('   ' + line)
        print()

    if len(labels) >= 2:
        base = results[labels[0]]
        for lab in labels[1:]:
            other = results[lab]
            if not other or not base:
                continue
            lost = [k for k in base if k in other and base[k] < WATER_Z <= other[k]]
            gained = [k for k in base if k in other and other[k] < WATER_Z <= base[k]]
            print('=== %s vs %s: %d vertices lost water, %d gained water'
                  % (lab, labels[0], len(lost), len(gained)))
            if lost:
                deltas = [other[k] - base[k] for k in lost]
                print('    raised by %.0f to %.0f units' % (min(deltas), max(deltas)))


if __name__ == '__main__':
    main()
