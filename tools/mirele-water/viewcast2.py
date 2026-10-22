"""Vectorised version of viewcast.py — marches every ray at once with numpy.

Same model: landscape heightmap + a flat water plane, no placed objects.

Usage:
  python viewcast2.py <plugin.esp> <out.png> --pos X Y Z --yaw D --pitch D
                      [--fov 85] [--size W H] [--sweep A B STEP]
"""
import argparse
import math

import numpy as np
from PIL import Image, ImageDraw

from waterscan import scan_plugin

WATER_Z = 600.0
CELL = 4096.0
VSPACING = 128.0

XS = [-4, -3, -2, -1, 0]
YS = [-17, -16, -15, -14, -13]
CELL_BASE = 0x009B4F


def land_id(x, y):
    return CELL_BASE + (-13 - y) * 0x21 + (-x) + 0x1000


def build_field(plugin):
    ids = {land_id(x, y) for x in XS for y in YS}
    found = scan_plugin(plugin, ids)
    nx, ny = len(XS) * 32 + 1, len(YS) * 32 + 1
    field = np.full((ny, nx), np.nan, dtype=np.float32)
    for cy, y in enumerate(YS):
        for cx, x in enumerate(XS):
            H = found.get(land_id(x, y))
            if H is None:
                continue
            arr = np.array([[H[(vx, vy)] for vx in range(33)] for vy in range(33)],
                           dtype=np.float32)
            field[cy * 32:cy * 32 + 33, cx * 32:cx * 32 + 33] = arr
    return field, (XS[0] * CELL, YS[0] * CELL)


def sample(field, origin, wx, wy):
    """Bilinear sample; NaN outside the field."""
    fx = (wx - origin[0]) / VSPACING
    fy = (wy - origin[1]) / VSPACING
    x0 = np.floor(fx).astype(np.int32)
    y0 = np.floor(fy).astype(np.int32)
    ok = (x0 >= 0) & (y0 >= 0) & (x0 + 1 < field.shape[1]) & (y0 + 1 < field.shape[0])
    x0c = np.clip(x0, 0, field.shape[1] - 2)
    y0c = np.clip(y0, 0, field.shape[0] - 2)
    tx = (fx - x0c).astype(np.float32)
    ty = (fy - y0c).astype(np.float32)
    h00 = field[y0c, x0c]
    h10 = field[y0c, x0c + 1]
    h01 = field[y0c + 1, x0c]
    h11 = field[y0c + 1, x0c + 1]
    out = (h00 * (1 - tx) + h10 * tx) * (1 - ty) + (h01 * (1 - tx) + h11 * tx) * ty
    return np.where(ok, out, np.nan)


def render(field, origin, cam, yaw, pitch, fov, W, H):
    aspect = W / H
    tan_h = math.tan(math.radians(fov) / 2)
    tan_v = tan_h / aspect
    ry, rp = math.radians(yaw), math.radians(pitch)
    fwd = np.array([math.sin(ry) * math.cos(rp), math.cos(ry) * math.cos(rp), math.sin(rp)])
    right = np.array([math.cos(ry), -math.sin(ry), 0.0])
    up = np.cross(right, fwd)

    j, i = np.mgrid[0:H, 0:W]
    sy = (1 - 2 * (j + 0.5) / H) * tan_v
    sx = (2 * (i + 0.5) / W - 1) * tan_h
    d = (fwd[None, None, :] + right[None, None, :] * sx[..., None]
         + up[None, None, :] * sy[..., None])
    d /= np.linalg.norm(d, axis=2, keepdims=True)

    n = H * W
    dx, dy, dz = d[..., 0].ravel(), d[..., 1].ravel(), d[..., 2].ravel()
    water_t = np.full(n, np.inf, np.float32)
    hit_t = np.full(n, np.inf, np.float32)
    hit_g = np.full(n, np.nan, np.float32)
    prev_above = np.full(n, np.nan, np.float32)
    prev_t = np.zeros(n, np.float32)
    live = np.ones(n, bool)

    t, step = 8.0, 16.0
    while t < 26000.0 and live.any():
        wx = cam[0] + dx * t
        wy = cam[1] + dy * t
        wz = cam[2] + dz * t
        g = sample(field, origin, wx, wy)
        outside = np.isnan(g)
        live &= ~outside

        # first crossing of the water plane over ground that is below it
        crossed = live & np.isinf(water_t) & (wz <= WATER_Z) & (g < WATER_Z)
        water_t[crossed] = t

        above = wz - g
        landed = live & ~np.isnan(prev_above) & (prev_above > 0) & (above <= 0)
        if landed.any():
            # linear refine between the last two samples
            frac = prev_above[landed] / (prev_above[landed] - above[landed])
            hit_t[landed] = prev_t[landed] + frac * (t - prev_t[landed])
            hit_g[landed] = g[landed]
            live[landed] = False
        prev_above = np.where(live, above, prev_above)
        prev_t = np.where(live, t, prev_t)
        t += step
        step = min(step * 1.03, 160.0)

    img = np.zeros((n, 3), np.uint8)
    sky = np.isinf(hit_t) & np.isinf(water_t)
    img[sky] = (150, 165, 195)

    is_water = (water_t <= hit_t) & ~np.isinf(water_t)
    fw = np.clip(water_t[is_water] / 14000.0, 0, 1)[:, None]
    img[is_water] = (np.array([24, 58, 120]) * (1 - fw) + np.array([170, 200, 225]) * fw)

    is_land = ~is_water & ~np.isinf(hit_t)
    hgt = np.clip((hit_g[is_land] - WATER_Z) / 2200.0, 0, 1)[:, None]
    fl = np.clip(hit_t[is_land] / 16000.0, 0, 1)[:, None]
    base = np.array([110, 100, 78]) + np.array([100, 95, 85]) * hgt
    img[is_land] = base * (1 - fl) + np.array([205, 205, 205]) * fl

    return Image.fromarray(img.reshape(H, W, 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plugin')
    ap.add_argument('out')
    ap.add_argument('--pos', nargs=3, type=float, required=True)
    ap.add_argument('--yaw', type=float, default=270.0)
    ap.add_argument('--pitch', type=float, default=-10.0)
    ap.add_argument('--fov', type=float, default=85.0)
    ap.add_argument('--size', nargs=2, type=int, default=[640, 360])
    ap.add_argument('--eye', type=float, default=120.0)
    ap.add_argument('--back', type=float, default=170.0)
    ap.add_argument('--sweep', nargs=3, type=float)
    a = ap.parse_args()

    field, origin = build_field(a.plugin)
    print('field %s  origin %s' % (field.shape, origin))

    def cam_for(yaw):
        ry = math.radians(yaw)
        return (np.array([a.pos[0], a.pos[1], a.pos[2] + a.eye])
                - np.array([math.sin(ry), math.cos(ry), 0.0]) * a.back)

    W, H = a.size
    if a.sweep:
        lo, hi, st = a.sweep
        yaws = [lo + k * st for k in range(int((hi - lo) / st) + 1)]
        tiles = []
        for y in yaws:
            im = render(field, origin, cam_for(y), y, a.pitch, a.fov, W, H)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, 88, 16], fill=(0, 0, 0))
            d.text((4, 3), 'yaw %d' % int(y), fill=(255, 255, 0))
            tiles.append(im)
            print('yaw %d done' % int(y))
        cols = 3
        rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new('RGB', (W * cols, H * rows))
        for k, im in enumerate(tiles):
            sheet.paste(im, ((k % cols) * W, (k // cols) * H))
        sheet.save(a.out)
        print('wrote', a.out, sheet.size)
    else:
        render(field, origin, cam_for(a.yaw), a.yaw, a.pitch, a.fov, W, H).save(a.out)
        print('wrote', a.out)


if __name__ == '__main__':
    main()
