"""Robust SKSE co-save scanner for SpellHotbar.

Rather than trusting the header layout, scan for the plugin signature
0xE219D7E9 and the 'HOTB' chunk fourcc, then parse locally and sanity-check.
"""
import struct, sys, os

SHID = 0xE219D7E9
SHID_LE = struct.pack('<I', SHID)   # E9 D7 19 E2
SHID_BE = struct.pack('>I', SHID)
TEXT_SHOW = {0: 'Never', 1: 'Fade', 2: 'Always'}
BAR_SHOW = {0: 'Always', 1: 'Never', 2: 'Combat', 3: 'Drawn Weapon', 4: 'Combat or Drawn', 5: 'Combat And Drawn'}


def find_all(hay, needle):
    out, i = [], 0
    while True:
        j = hay.find(needle, i)
        if j < 0:
            return out
        out.append(j)
        i = j + 1


def decode_hotb(data, H=2160):
    if len(data) != 23:
        return None
    barsize, ctrl, shift, alt = struct.unpack_from('<4B', data, 0)
    slot_scale, off_x, off_y = struct.unpack_from('<3f', data, 4)
    spacing, text_show, bar_show, bar_vl, bar_ww, sheathed, no_menu = struct.unpack_from('<7B', data, 16)
    if not (1 <= barsize <= 12):
        return None
    if not (0.0 < slot_scale < 20.0):
        return None
    slot_px = int((H / 13.0) * slot_scale)
    content_w = barsize * slot_px + (barsize - 1) * spacing
    return {
        'number_of_slots': barsize, 'slot_scale': slot_scale, 'slot_spacing': spacing,
        'offset_x': off_x, 'offset_y': off_y,
        'ctrl': ctrl, 'shift': shift, 'alt': alt,
        'text_show': TEXT_SHOW.get(text_show, '?%d' % text_show),
        'hud_show': BAR_SHOW.get(bar_show, '?%d' % bar_show),
        'hud_show_vampire': BAR_SHOW.get(bar_vl, '?%d' % bar_vl),
        'hud_show_werewolf': BAR_SHOW.get(bar_ww, '?%d' % bar_ww),
        'default_bar_sheathed': sheathed, 'disable_menu_rendering': no_menu,
        'slot_px_at_%d' % H: slot_px,
        'slot_row_px': content_w,
        'pct_of_3840': round(100.0 * content_w / 3840, 1),
    }


def scan(path):
    d = open(path, 'rb').read()
    print('=== %s  (%d bytes) ===' % (os.path.basename(path), len(d)))
    print('    magic=%r formatVersion=%d' % (d[:4], struct.unpack_from('<I', d, 4)[0]))

    hits = find_all(d, SHID_LE) + find_all(d, SHID_BE)
    print('    signature 0xE219D7E9 occurrences: %d %s' % (len(hits), hits[:8]))

    for name in (b'HOTB', b'BTOH'):
        h = find_all(d, name)
        if h:
            print('    fourcc %r at %s' % (name.decode(), h[:8]))

    # Parse the plugin block at each signature hit
    for off in hits:
        p = off + 4
        try:
            nchunks, length = struct.unpack_from('<II', d, p)
        except struct.error:
            continue
        if not (0 < nchunks < 64) or not (0 < length < len(d)):
            print('    @%d: implausible header nchunks=%d length=%d — not a plugin block' % (off, nchunks, length))
            continue
        print('    @%d: PLUGIN BLOCK  numChunks=%d  dataLength=%d' % (off, nchunks, length))
        p += 8
        for c in range(nchunks):
            if p + 12 > len(d):
                print('       chunk %d: truncated' % c); break
            ctype, cver, clen = struct.unpack_from('<III', d, p)
            p += 12
            data = d[p:p + clen]
            p += clen
            nm = struct.pack('<I', ctype)[::-1]
            nms = ''.join(chr(x) if 32 <= x < 127 else '.' for x in nm)
            print('       chunk %d: %r v%d len=%d' % (c, nms, cver, clen))
            if nms == 'HOTB':
                got = decode_hotb(data)
                if got:
                    print('          *** LIVE SETTINGS ***')
                    for k, v in got.items():
                        print('          %-24s %s' % (k, v))
                else:
                    print('          !! HOTB failed sanity decode; raw=%s' % data.hex())
            else:
                nz = sum(1 for b in data if b)
                print('          %d non-zero bytes; raw[:64]=%s' % (nz, data[:64].hex()))
    if not hits:
        print('    => NO SpellHotbar data in this co-save. The mod wrote nothing when this save was made.')
    print()


if __name__ == '__main__':
    for a in sys.argv[1:]:
        scan(a)
