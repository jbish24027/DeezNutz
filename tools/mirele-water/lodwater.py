"""Report which terrain-LOD tiles carry a LOD water plane.

xLODGen writes each terrain LOD tile as a NIF holding a 'land' shape plus, when
the tile contains water, a second shape for the LOD water surface. A tile that
lost its water shape shows in game as a rectangular chunk of lake bed with no
water on it.

Usage: python lodwater.py <terrain-lod-folder> [level]
"""
import os
import re
import struct
import sys


def block_types(path):
    with open(path, 'rb') as f:
        data = f.read(65536)
    # header string terminated by \n
    nl = data.index(b'\n')
    pos = nl + 1
    version = struct.unpack_from('<I', data, pos)[0]
    pos += 4
    pos += 1                      # endian
    pos += 4                      # user version
    num_blocks = struct.unpack_from('<I', data, pos)[0]
    pos += 4
    bs_version = struct.unpack_from('<I', data, pos)[0]
    pos += 4
    # export info: author, process script, export script (short strings)
    for _ in range(3):
        ln = data[pos]
        pos += 1 + ln
    if bs_version >= 130:
        ln = data[pos]
        pos += 1 + ln             # max filepath (FO4+ only)
    num_types = struct.unpack_from('<H', data, pos)[0]
    pos += 2
    types = []
    for _ in range(num_types):
        ln = struct.unpack_from('<I', data, pos)[0]
        pos += 4
        types.append(data[pos:pos + ln].decode('ascii', 'replace'))
        pos += ln
    idx = struct.unpack_from('<%dH' % num_blocks, data, pos)
    return [types[i] for i in idx]


SHAPE_TYPES = ('BSTriShape', 'BSSubIndexTriShape', 'BSMeshLODTriShape',
               'NiTriShape', 'NiTriStrips')

TILE_RE = re.compile(r'^Tamriel\.(\d+)\.(-?\d+)\.(-?\d+)\.btr$', re.I)


def main():
    folder = sys.argv[1]
    want_level = sys.argv[2] if len(sys.argv) > 2 else '4'

    rows = []
    for name in os.listdir(folder):
        m = TILE_RE.match(name)
        if not m or m.group(1) != want_level:
            continue
        x, y = int(m.group(2)), int(m.group(3))
        try:
            blocks = block_types(os.path.join(folder, name))
        except Exception as exc:
            rows.append((x, y, name, 'ERROR: %s' % exc, -1))
            continue
        shapes = [b for b in blocks if b in SHAPE_TYPES]
        rows.append((x, y, name, ','.join(shapes), len(shapes)))

    xs = sorted({r[0] for r in rows})
    ys = sorted({r[1] for r in rows}, reverse=True)
    by = {(r[0], r[1]): r for r in rows}

    print('level %s tiles: %d   (shape count per tile; 1 = land only, no LOD water)\n'
          % (want_level, len(rows)))
    print('        ' + ''.join('%5d' % x for x in xs))
    for y in ys:
        line = ['y=%-6d' % y]
        for x in xs:
            r = by.get((x, y))
            line.append('    .' if r is None else '%5d' % r[4])
        print(''.join(line))

    lonely = [r for r in rows if r[4] == 1]
    print('\n%d tile(s) carry a land shape but NO second shape:' % len(lonely))
    for x, y, name, s, n in sorted(lonely, key=lambda r: (-r[1], r[0])):
        print('  %s   cells x %d..%d, y %d..%d   blocks: %s'
              % (name, x, x + int(want_level) - 1, y, y + int(want_level) - 1, s))


if __name__ == '__main__':
    main()
