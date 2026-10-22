"""Render a top-down map of ground height vs the water line, with the player marked.

Blue  = ground below the water line (water should be visible here)
Tan   = ground above the water line (dry by design)
Red   = player position
Grid  = cell boundaries

Usage: python topomap.py <plugin.esp> <out.png> [player_x player_y]
"""
import sys

from PIL import Image, ImageDraw

from waterscan import scan_plugin

WATER_Z = 600.0
CELL = 4096.0
PX = 8                      # pixels per landscape vertex (vertex = 128 world units)

XS = [-4, -3, -2, -1, 0]
YS = [-13, -14, -15, -16, -17]
CELL_BASE = 0x009B4F        # cell (0,-13); LAND = cell + 0x1000


def land_id(x, y):
    return CELL_BASE + (-13 - y) * 0x21 + (-x) + 0x1000


def main():
    plugin, out = sys.argv[1], sys.argv[2]
    px_, py_ = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (None, None)

    ids = {land_id(x, y) for x in XS for y in YS}
    found = scan_plugin(plugin, ids)
    print('LAND found %d/%d' % (len(found), len(ids)))

    W = len(XS) * 32 * PX + 1
    H = len(YS) * 32 * PX + 1
    img = Image.new('RGB', (W, H), (20, 20, 24))
    d = ImageDraw.Draw(img)

    for cy, y in enumerate(YS):
        for cx, x in enumerate(XS):
            Hm = found.get(land_id(x, y))
            if Hm is None:
                continue
            for vy in range(32):
                for vx in range(32):
                    z = Hm[(vx, vy)]
                    gx = (cx * 32 + vx) * PX
                    gy = (cy * 32 + (31 - vy)) * PX
                    if z < WATER_Z:
                        depth = min(1.0, (WATER_Z - z) / 900.0)
                        col = (int(30 + 40 * (1 - depth)), int(70 + 90 * (1 - depth)),
                               int(150 + 80 * (1 - depth)))
                    else:
                        hgt = min(1.0, (z - WATER_Z) / 2500.0)
                        col = (int(110 + 110 * hgt), int(100 + 100 * hgt),
                               int(80 + 90 * hgt))
                    d.rectangle([gx, gy, gx + PX - 1, gy + PX - 1], fill=col)

    # cell grid + labels
    for cx, x in enumerate(XS):
        gx = cx * 32 * PX
        d.line([(gx, 0), (gx, H)], fill=(255, 60, 60), width=1)
    for cy, y in enumerate(YS):
        gy = cy * 32 * PX
        d.line([(0, gy), (W, gy)], fill=(255, 60, 60), width=1)
        for cx, x in enumerate(XS):
            d.text((cx * 32 * PX + 4, gy + 4), '(%d,%d)' % (x, y), fill=(255, 230, 120))

    # player
    if px_ is not None:
        gx = (px_ - XS[0] * CELL) / CELL * 32 * PX
        gy = (YS[0] * CELL + CELL - py_) / CELL * 32 * PX
        d.ellipse([gx - 7, gy - 7, gx + 7, gy + 7], outline=(255, 40, 40), width=3)
        d.line([(gx - 14, gy), (gx + 14, gy)], fill=(255, 40, 40), width=2)
        d.line([(gx, gy - 14), (gx, gy + 14)], fill=(255, 40, 40), width=2)
        print('player pixel (%.0f, %.0f)' % (gx, gy))

    img.save(out)
    print('wrote %s  %dx%d   north is up, east is right' % (out, W, H))


if __name__ == '__main__':
    main()
