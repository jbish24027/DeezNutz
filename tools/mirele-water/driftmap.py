"""Show where the winning terrain sits above the lake surface but vanilla was under it.

Renders the 2x2 cell block Mirele Bismath Reborn sculpts (cells x=-2..-1, y=-16..-15),
the ground between the Guardian Stones and the island.

Usage: python driftmap.py <vanilla.esm> <other.esp> [more.esp ...]
"""
import sys
from waterscan import scan_plugin, WATER_Z

# LAND records, laid out west->east then north->south
BLOCK = [
    [0x00AB93, 0x00AB92],   # cells (-2,-15) (-1,-15)
    [0x00ABB4, 0x00ABB3],   # cells (-2,-16) (-1,-16)
]
LABELS = [['(-2,-15)', '(-1,-15)'], ['(-2,-16)', '(-1,-16)']]


def grid_for(found):
    g = {}
    for cy, row in enumerate(BLOCK):
        for cx, lid in enumerate(row):
            H = found.get(lid)
            if H is None:
                continue
            for vy in range(33):
                for vx in range(33):
                    g[(cx * 32 + vx, cy * 32 + (32 - vy))] = H[(vx, vy)]
    return g


def main():
    wanted = {lid for row in BLOCK for lid in row}
    maps = []
    for arg in sys.argv[1:]:
        label, path = arg.split('=', 1)
        maps.append((label, grid_for(scan_plugin(path, wanted))))

    base_label, base = maps[0]
    print('cells: %s   water line Z=%.0f' % (
        ' '.join(l for row in LABELS for l in row), WATER_Z))
    print('legend:  ~ under water in both    # dry in both')
    print('         D dry now, under water in %s (water LOST)' % base_label)
    print('         W under water now, dry in %s (water GAINED)\n' % base_label)

    for label, g in maps[1:]:
        print('--- %s  vs %s' % (label, base_label))
        for gy in range(0, 65, 2):
            row = []
            for gx in range(0, 65, 2):
                a, b = base.get((gx, gy)), g.get((gx, gy))
                if a is None or b is None:
                    row.append(' ')
                    continue
                wa, wb = a < WATER_Z, b < WATER_Z
                row.append('~' if wa and wb else '#' if not wa and not wb
                           else 'D' if wa else 'W')
            print('   ' + ''.join(row))
        lost = sum(1 for k in base if k in g and base[k] < WATER_Z <= g[k])
        print('   %d vertices dry that vanilla had under water\n' % lost)


if __name__ == '__main__':
    main()
