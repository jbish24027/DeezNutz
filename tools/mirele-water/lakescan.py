"""Find every cell in a bounding box whose ground dips below the lake surface.

Reads the load-order-winning landscape and reports, per cell, how many of its
1089 vertices sit below the water line. Cells with sub-water ground but no water
configured are the ones that show as dry lake bed in game.

Usage: python lakescan.py <plugin-path> [water_z]
"""
import sys
from waterscan import scan_plugin, WATER_Z

# cell(x, y) for x in -32..0, y <= -13 : rows step 0x21 south, +1 per cell west
CELL_BASE = 0x009B4F   # cell (0, -13)


def cell_formid(x, y):
    return CELL_BASE + (-13 - y) * 0x21 + (-x)


X_RANGE = range(0, -13, -1)     # 0 .. -12
Y_RANGE = range(-12, -21, -1)   # -12 .. -20


def main():
    path = sys.argv[1]
    water_z = float(sys.argv[2]) if len(sys.argv) > 2 else WATER_Z

    cells = {(x, y): cell_formid(x, y) for x in X_RANGE for y in Y_RANGE}
    land_ids = {cid + 0x1000 for cid in cells.values()}
    found = scan_plugin(path, land_ids)
    print('LAND records found: %d/%d\n' % (len(found), len(land_ids)))

    print('vertices below Z=%.0f per cell (out of 1089)' % water_z)
    header = '      ' + ''.join('%6d' % x for x in X_RANGE)
    print(header)
    wet_cells = []
    for y in Y_RANGE:
        row = ['y=%-4d' % y]
        for x in X_RANGE:
            H = found.get(cells[(x, y)] + 0x1000)
            if H is None:
                row.append('     ?')
                continue
            n = sum(1 for v in H.values() if v < water_z)
            row.append('     .' if n == 0 else '%6d' % n)
            if n:
                wet_cells.append((x, y, n, cells[(x, y)]))
        print(''.join(row))

    print('\n%d cells have ground below the water line:' % len(wet_cells))
    for x, y, n, cid in wet_cells:
        print('  (%d,%d)  %06X:Skyrim.esm   %d/1089 vertices submerged' % (x, y, cid, n))


if __name__ == '__main__':
    main()
