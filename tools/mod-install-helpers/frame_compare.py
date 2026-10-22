"""Decode the hotbar frame art and compare Vel'dun's override against stock Spell Hotbar.
Pure stdlib PNG decode (zlib + struct), no Pillow.
"""
import struct, zlib, os, sys, io
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def readpng(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n', path
    i = 8
    idat = b''
    w = h = bd = ct = None
    plte = None
    while i < len(d):
        ln = struct.unpack('>I', d[i:i + 4])[0]
        typ = d[i + 4:i + 8]
        data = d[i + 8:i + 8 + ln]
        i += 12 + ln
        if typ == b'IHDR':
            w, h, bd, ct, comp, filt, inter = struct.unpack('>IIBBBBB', data[:13])
            assert inter == 0, 'interlaced not supported'
        elif typ == b'PLTE':
            plte = data
        elif typ == b'IDAT':
            idat += data
        elif typ == b'IEND':
            break
    raw = zlib.decompress(idat)
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct]
    assert bd == 8, 'bit depth %d' % bd
    bpp = ch
    stride = w * bpp
    out = bytearray()
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        f = raw[pos]; pos += 1
        line = bytearray(raw[pos:pos + stride]); pos += stride
        if f == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out += line
        prev = line
    return w, h, ch, ct, plte, bytes(out)


def px(buf, w, ch, ct, plte, x, y):
    o = (y * w + x) * ch
    if ct == 6:
        return buf[o], buf[o + 1], buf[o + 2], buf[o + 3]
    if ct == 2:
        return buf[o], buf[o + 1], buf[o + 2], 255
    if ct == 3:
        idx = buf[o]
        return plte[idx * 3], plte[idx * 3 + 1], plte[idx * 3 + 2], 255
    if ct == 4:
        return buf[o], buf[o], buf[o], buf[o + 1]
    return buf[o], buf[o], buf[o], 255


def analyse(path, label, u0, v0, u1, v1):
    w, h, ch, ct, plte, buf = readpng(path)
    x0, y0 = int(round(u0 * w)), int(round(v0 * h))
    x1, y1 = int(round(u1 * w)), int(round(v1 * h))
    cw, chh = x1 - x0, y1 - y0
    cnt = Counter()
    opaque = 0
    total = cw * chh
    alphas = Counter()
    # border thickness probe: scan the middle row inward for first opaque pixel
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px(buf, w, ch, ct, plte, x, y)
            alphas[a // 32] += 1
            if a > 24:
                opaque += 1
                cnt[(r, g, b)] += 1
    midy = (y0 + y1) // 2
    left_edge = None
    for x in range(x0, x1):
        r, g, b, a = px(buf, w, ch, ct, plte, x, midy)
        if a > 24:
            left_edge = x - x0
            break
    thick = 0
    if left_edge is not None:
        x = x0 + left_edge
        while x < x1:
            r, g, b, a = px(buf, w, ch, ct, plte, x, midy)
            if a <= 24:
                break
            thick += 1
            x += 1
    # centre pixel
    cr, cg, cb, ca = px(buf, w, ch, ct, plte, (x0 + x1) // 2, midy)
    print('--- %s ---' % label)
    print('    source %s  (%dx%d, colourtype %d)  cell %dx%d at (%d,%d)' % (os.path.basename(path), w, h, ct, cw, chh, x0, y0))
    print('    opaque coverage: %.1f%%   (%d of %d px with alpha>24)' % (100.0 * opaque / total, opaque, total))
    print('    centre pixel: #%02X%02X%02X alpha %d  -> %s' % (cr, cg, cb, ca, 'FILLED PANEL' if ca > 24 else 'HOLLOW (outline only)'))
    print('    first opaque px from left on centre row: offset %s, run length %s' % (left_edge, thick))
    print('    distinct opaque colours: %d' % len(cnt))
    for col, n in cnt.most_common(8):
        print('       #%02X%02X%02X  %6d px  (%.1f%%)' % (col[0], col[1], col[2], n, 100.0 * n / max(1, opaque)))
    return cnt


if __name__ == '__main__':
    VEL = r"C:\1. AUTHORIA\mods\Vel'dun UI Overhauls - Patches\SKSE\Plugins\SpellHotbar\images\default_icons_veldun.png"
    STOCK = r"C:\1. AUTHORIA\mods\Spell Hotbar\SKSE\Plugins\SpellHotbar\images\default_icons.png"
    CSV = r"C:\1. AUTHORIA\mods\Spell Hotbar\SKSE\Plugins\SpellHotbar\images\default_icons.csv"

    print('=== Vel\'dun override (only 2 keys) ===')
    analyse(VEL, "VELDUN BAR_EMPTY", 0.0, 0.0, 0.5, 0.5)
    analyse(VEL, "VELDUN BAR_OVERLAY", 0.5, 0.0, 1.0, 0.5)

    print()
    print('=== stock Spell Hotbar equivalents (from default_icons.csv) ===')
    want = {'BAR_EMPTY', 'BAR_OVERLAY', 'BAR_HIGHLIGHT', 'UNKNOWN', 'UNBIND_SLOT'}
    for line in open(CSV, encoding='utf-8-sig'):
        parts = [p.strip() for p in line.replace(',', '\t').split('\t') if p.strip()]
        if len(parts) < 5 or parts[0] not in want:
            continue
        name = parts[0]
        try:
            a, b, c, dd = (float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))
        except ValueError:
            continue
        analyse(STOCK, 'STOCK ' + name, a, b, c, dd)
