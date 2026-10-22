"""Read a Skyrim SE .ess save: header, player position, and (optionally) change forms.

Usage: python savepos.py <save.ess> [--forms] [--formfilter HEXPREFIX]
"""
import struct
import sys

import lz4.block


class R:
    def __init__(self, b, pos=0):
        self.b = b
        self.p = pos

    def u8(self):
        v = self.b[self.p]
        self.p += 1
        return v

    def u16(self):
        v = struct.unpack_from('<H', self.b, self.p)[0]
        self.p += 2
        return v

    def u32(self):
        v = struct.unpack_from('<I', self.b, self.p)[0]
        self.p += 4
        return v

    def i32(self):
        v = struct.unpack_from('<i', self.b, self.p)[0]
        self.p += 4
        return v

    def f32(self):
        v = struct.unpack_from('<f', self.b, self.p)[0]
        self.p += 4
        return v

    def u64(self):
        v = struct.unpack_from('<Q', self.b, self.p)[0]
        self.p += 8
        return v

    def wstr(self):
        n = self.u16()
        s = self.b[self.p:self.p + n].decode('cp1252', 'replace')
        self.p += n
        return s

    def refid(self):
        a, b, c = self.b[self.p], self.b[self.p + 1], self.b[self.p + 2]
        self.p += 3
        raw = (a << 16) | (b << 8) | c
        return (raw >> 22) & 0x3, raw & 0x3FFFFF

    def vsval(self):
        """Variable-size value: low 2 bits give the byte width."""
        first = self.b[self.p]
        kind = first & 0x3
        if kind == 0:
            self.p += 1
            return first >> 2
        if kind == 1:
            v = struct.unpack_from('<H', self.b, self.p)[0]
            self.p += 2
            return v >> 2
        v = struct.unpack_from('<I', self.b, self.p)[0]
        self.p += 4
        return v >> 2


def load(path):
    data = open(path, 'rb').read()
    assert data[:13] == b'TESV_SAVEGAME', data[:13]
    r = R(data, 13)
    header_size = r.u32()
    hstart = r.p
    hdr = {}
    hdr['version'] = r.u32()
    hdr['saveNumber'] = r.u32()
    hdr['playerName'] = r.wstr()
    hdr['playerLevel'] = r.u32()
    hdr['playerLocation'] = r.wstr()
    hdr['gameDate'] = r.wstr()
    hdr['playerRace'] = r.wstr()
    hdr['playerSex'] = r.u16()
    hdr['curExp'] = r.f32()
    hdr['lvlExp'] = r.f32()
    hdr['filetime'] = r.u64()
    hdr['shotWidth'] = r.u32()
    hdr['shotHeight'] = r.u32()
    compression = r.u16() if hdr['version'] >= 12 else 0
    hdr['compression'] = compression
    r.p = hstart + header_size

    # SSE: the screenshot follows the header directly (RGBA); the form-version
    # byte lives at the start of the DEcompressed body, not here.
    shot_bytes = hdr['shotWidth'] * hdr['shotHeight'] * 4
    r.p += shot_bytes

    if compression == 0:
        body = data[r.p:]
    else:
        uncomp_len = r.u32()
        comp_len = r.u32()
        raw = data[r.p:r.p + comp_len]
        if compression == 2:
            body = lz4.block.decompress(raw, uncompressed_size=uncomp_len)
        else:
            import zlib
            body = zlib.decompress(raw)
    # FLT offsets are absolute offsets into the UNCOMPRESSED file layout, so
    # everything before the body has to come off them.
    hdr['bodyBase'] = 13 + 4 + header_size + shot_bytes
    return hdr, body


def parse_body(body, base=0):
    r = R(body)
    form_version = r.u8()
    plugin_info_size = r.u32()
    after_plugins = r.p + plugin_info_size
    count = r.u8()
    plugins = [r.wstr() for _ in range(count)]
    light = []
    if form_version >= 78:
        lcount = r.u16()
        light = [r.wstr() for _ in range(lcount)]
    end_of_lists = r.p

    r.p = after_plugins
    flt = {}
    for k in ('formIDArrayCountOffset', 'unknownTable3Offset',
              'globalDataTable1Offset', 'globalDataTable2Offset',
              'changeFormsOffset', 'globalDataTable3Offset'):
        flt[k] = r.u32()
    for k in ('globalDataTable1Count', 'globalDataTable2Count',
              'globalDataTable3Count', 'changeFormCount'):
        flt[k] = r.u32()
    if base:
        for k in list(flt):
            if k.endswith('Offset'):
                flt[k] -= base
    return form_version, plugins, light, flt


def global_data(body, offset, count):
    r = R(body, offset)
    out = []
    for _ in range(count):
        t = r.u32()
        ln = r.u32()
        out.append((t, body[r.p:r.p + ln]))
        r.p += ln
    return out


def player_location(chunk):
    r = R(chunk)
    next_obj = r.u32()
    ws1 = r.refid()
    cx = r.i32()
    cy = r.i32()
    ws2 = r.refid()
    px = r.f32()
    py = r.f32()
    pz = r.f32()
    return dict(nextObjectId=next_obj, worldspace1=ws1, cellX=cx, cellY=cy,
                worldspace2=ws2, posX=px, posY=py, posZ=pz)


def main():
    path = sys.argv[1]
    hdr, body = load(path)
    print('save        : %s' % path.rsplit('\\', 1)[-1])
    print('player      : %s  level %d' % (hdr['playerName'], hdr['playerLevel']))
    print('location    : %s' % hdr['playerLocation'])
    print('game date   : %s' % hdr['gameDate'])
    print('screenshot  : %dx%d   compression=%d' %
          (hdr['shotWidth'], hdr['shotHeight'], hdr['compression']))

    form_version, plugins, light, flt = parse_body(body, hdr['bodyBase'])
    print('form version: %d   plugins=%d  light=%d  changeForms=%d'
          % (form_version, len(plugins), len(light), flt['changeFormCount']))

    for tbl, off, cnt in (
            (1, flt['globalDataTable1Offset'], flt['globalDataTable1Count']),
            (2, flt['globalDataTable2Offset'], flt['globalDataTable2Count']),
            (3, flt['globalDataTable3Offset'], flt['globalDataTable3Count'])):
        for t, chunk in global_data(body, off, cnt):
            if t == 1:
                loc = player_location(chunk)
                print('\n--- player location (global data type 3, table %d)' % tbl)
                for k, v in loc.items():
                    print('   %-14s %s' % (k, v))
                print('   cell grid    (%d, %d)' % (loc['cellX'], loc['cellY']))
                print('   world pos    x=%.1f  y=%.1f  z=%.1f'
                      % (loc['posX'], loc['posY'], loc['posZ']))
                print('   derived cell (%d, %d)'
                      % (int(loc['posX'] // 4096), int(loc['posY'] // 4096)))


if __name__ == '__main__':
    main()
