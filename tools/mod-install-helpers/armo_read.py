"""Read ARMO balance fields straight out of a plugin file.

Returns per record: editorid, name, biped slot mask, armor type, value, weight,
armor rating (as houseCARL shows it, i.e. the DNAM u16 pair / 100), and the raw
keyword FormIDs with their source-master index resolved against the file's own
master table.

Read-only. Used to derive an existing patch's conventions in bulk instead of
one read_record call per record.
"""
import struct, zlib

ARMOR_TYPE = {0: 'LightArmor', 1: 'HeavyArmor', 2: 'Clothing'}


def _subrecords(body):
    o = 0
    big = None
    while o + 6 <= len(body):
        sig = body[o:o + 4]
        size = struct.unpack_from('<H', body, o + 4)[0]
        if sig == b'XXXX':
            big = struct.unpack_from('<I', body, o + 6)[0]
            o += 6 + size
            continue
        if big is not None:
            size = big
            big = None
        yield sig, body[o + 6:o + 6 + size]
        o += 6 + size


def read_armo(path):
    data = open(path, 'rb').read()
    masters = []
    out = []

    def walk(off, end, in_tes4=True):
        while off < end:
            sig = data[off:off + 4]
            if len(sig) < 4:
                return
            size = struct.unpack_from('<I', data, off + 4)[0]
            if sig == b'GRUP':
                walk(off + 24, off + size, False)
                off += size
                continue
            flags = struct.unpack_from('<I', data, off + 8)[0]
            formid = struct.unpack_from('<I', data, off + 12)[0]
            body = data[off + 24:off + 24 + size]
            if flags & 0x00040000:
                try:
                    body = zlib.decompress(body[4:])
                except Exception:
                    body = b''
            if sig == b'TES4':
                for st, sd in _subrecords(body):
                    if st == b'MAST':
                        masters.append(sd.split(b'\x00')[0].decode('cp1252', 'replace'))
            elif sig == b'ARMO':
                r = {'formid': formid & 0xFFFFFF, 'edid': '', 'name': '',
                     'slots': None, 'armortype': None, 'value': None,
                     'weight': None, 'ar': None, 'keywords': []}
                for st, sd in _subrecords(body):
                    if st == b'EDID':
                        r['edid'] = sd.split(b'\x00')[0].decode('cp1252', 'replace')
                    elif st == b'FULL':
                        r['name'] = sd.split(b'\x00')[0].decode('cp1252', 'replace')
                    elif st == b'BOD2' and len(sd) >= 8:
                        r['slots'], at = struct.unpack_from('<II', sd, 0)
                        r['armortype'] = ARMOR_TYPE.get(at, at)
                    elif st == b'DATA' and len(sd) >= 8:
                        r['value'], r['weight'] = struct.unpack_from('<If', sd, 0)
                    elif st == b'DNAM' and len(sd) >= 4:
                        r['ar'] = struct.unpack_from('<I', sd, 0)[0] / 100.0
                    elif st == b'KWDA':
                        r['keywords'] = list(struct.unpack_from('<%dI' % (len(sd) // 4), sd, 0))
                out.append(r)
            off += 24 + size

    walk(0, len(data))
    return masters, out


def slot_names(mask):
    """Decode a BOD2 FirstPersonFlags mask into slot numbers."""
    return [30 + b for b in range(32) if mask >> b & 1]
