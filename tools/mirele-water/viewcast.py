"""Render the view from a world position using the landscape heightmap + the water plane.

Shows what the engine ought to draw: blue where a ray crosses the water plane before it
hits ground, shaded ground otherwise. Ignores placed objects (rocks, trees, buildings), so
compare silhouettes and shorelines, not clutter.

Usage:
  python viewcast.py <plugin.esp> <out.png> --pos X Y Z [--yaw DEG] [--pitch DEG]
                     [--fov DEG] [--size W H] [--sweep]

Yaw follows Skyrim: 0 = north (+Y), 90 = east (+X), 180 = south, 270 = west.
"""
import argparse
import math

import numpy as np
from PIL import Image, ImageDraw

from waterscan import scan_plugin

WATER_Z = 600.0
CELL = 4096.0
VSPACING = 128.0            # world units between landscape vertices

XS = [-4, -3, -2, -1, 0]
YS = [-17, -16, -15, -14, -13]      # south -> north
CELL_BASE = 0x009B4F


def land_id(x, y):
    return CELL_BASE + (-13 - y) * 0x21 + (-x) + 0x1000


def build_field(plugin):
    ids = {land_id(x, y) for x in XS for y in YS}
    found = scan_plugin(plugin, ids)
    nx = len(XS) * 32 + 1
    ny = len(YS) * 32 + 1
    field = np.full((ny, nx), np.nan, dtype=np.float32)
    for cy, y in enumerate(YS):
        for cx, x in enumerate(XS):
            H = found.get(land_id(x, y))
            if H is None:
                continue
            for vy in range(33):
                for vx in range(33):
                    field[cy * 32 + vy, cx * 32 + vx] = H[(vx, vy)]
    origin = (XS[0] * CELL, YS[0] * CELL)       # world x,y of field[0,0]
    print('height field %dx%d  origin %s  missing %d cells'
          % (nx, ny, origin, len(ids) - len(found)))
    return field, origin


def sample(field, origin, wx, wy):
    fx = (wx - origin[0]) / VSPACING
    fy = (wy - origin[1]) / VSPACING
    x0, y0 = int(math.floor(fx)), int(math.floor(fy))
    if x0 < 0 or y0 < 0 or x0 + 1 >= field.shape[1] or y0 + 1 >= field.shape[0]:
        return None
    tx, ty = fx - x0, fy - y0
    h00, h10 = field[y0, x0], field[y0, x0 + 1]
    h01, h11 = field[y0 + 1, x0], field[y0 + 1, x0 + 1]
    if np.isnan(h00) or np.isnan(h10) or np.isnan(h01) or np.isnan(h11):
        return None
    return ((h00 * (1 - tx) + h10 * tx) * (1 - ty) +
            (h01 * (1 - tx) + h11 * tx) * ty)


def render(field, origin, cam, yaw, pitch, fov, size):
    W, H = size
    img = Image.new('RGB', (W, H))
    px = img.load()
    aspect = W / H
    tan_h = math.tan(math.radians(fov) / 2)
    tan_v = tan_h / aspect

    ry = math.radians(yaw)
    rp = math.radians(pitch)
    # forward: yaw 0 = +Y (north), 90 = +X (east)
    fwd = np.array([math.sin(ry) * math.cos(rp), math.cos(ry) * math.cos(rp), math.sin(rp)])
    right = np.array([math.cos(ry), -math.sin(ry), 0.0])
    up = np.cross(right, fwd)

    MAXT, STEP = 26000.0, 24.0
    for j in range(H):
        sy = (1 - 2 * (j + 0.5) / H) * tan_v
        for i in range(W):
            sx = (2 * (i + 0.5) / W - 1) * tan_h
            d = fwd + right * sx + up * sy
            d /= np.linalg.norm(d)

            col = (past_end := None)
            t = 8.0
            step = STEP
            water_t = None
            hit = None
            prev_above = None
            while t < MAXT:
                p = cam + d * t
                g = sample(field, origin, p[0], p[1])
                if g is None:
                    break
                if water_t is None and p[2] <= WATER_Z and g < WATER_Z:
                    water_t = t
                above = p[2] - g
                if prev_above is not None and prev_above > 0 >= above:
                    hit = (t, g)
                    break
                prev_above = above
                t += step
                step = min(step * 1.02, 200.0)

            if water_t is not None and (hit is None or water_t <= hit[0]):
                fade = min(1.0, water_t / 14000.0)
                col = (int(24 + 150 * fade), int(58 + 150 * fade), int(120 + 110 * fade))
            elif hit is not None:
                t_, g = hit
                hgt = max(0.0, min(1.0, (g - WATER_Z) / 2200.0))
                fade = min(1.0, t_ / 16000.0)
                base = (110 + 100 * hgt, 100 + 95 * hgt, 78 + 85 * hgt)
                col = tuple(int(b * (1 - fade) + 205 * fade) for b in base)
            else:
                col = (150, 165, 195)
            px[i, j] = col
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plugin')
    ap.add_argument('out')
    ap.add_argument('--pos', nargs=3, type=float, required=True)
    ap.add_argument('--yaw', type=float, default=270.0)
    ap.add_argument('--pitch', type=float, default=-10.0)
    ap.add_argument('--fov', type=float, default=85.0)
    ap.add_argument('--size', nargs=2, type=int, default=[560, 315])
    ap.add_argument('--eye', type=float, default=120.0)
    ap.add_argument('--back', type=float, default=170.0)
    ap.add_argument('--sweep', action='store_true')
    a = ap.parse_args()

    field, origin = build_field(a.plugin)

    def cam_for(yaw):
        ry = math.radians(yaw)
        fwd = np.array([math.sin(ry), math.cos(ry), 0.0])
        return np.array([a.pos[0], a.pos[1], a.pos[2] + a.eye]) - fwd * a.back

    if a.sweep:
        yaws = list(range(180, 361, 30))
        tiles = []
        for y in yaws:
            im = render(field, origin, cam_for(y), y, a.pitch, a.fov, a.size)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, 92, 18], fill=(0, 0, 0))
            d.text((4, 4), 'yaw %d' % y, fill=(255, 255, 0))
            tiles.append(im)
            print('rendered yaw', y)
        cols = 3
        rows = (len(tiles) + cols - 1) // cols
        w, h = tiles[0].size
        sheet = Image.new('RGB', (w * cols, h * rows))
        for k, im in enumerate(tiles):
            sheet.paste(im, ((k % cols) * w, (k // cols) * h))
        sheet.save(a.out)
        print('wrote sweep', a.out, sheet.size)
    else:
        im = render(field, origin, cam_for(a.yaw), a.yaw, a.pitch, a.fov, a.size)
        im.save(a.out)
        print('wrote', a.out, im.size)


if __name__ == '__main__':
    main()
