"""Minimal Skyrim SE plugin parser: pull player-dialogue prompt strings out of DIAL/INFO."""
import struct, zlib, os, io

REC_HDR = 24
GRP_HDR = 24

class Plugin:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            self.buf = f.read()
        self.localized = False
        self.masters = []

    def parse_header(self):
        b = self.buf
        if b[0:4] != b'TES4':
            raise ValueError('not a plugin')
        self.masters = []          # idempotent: top_groups() re-parses the header
        size = struct.unpack_from('<I', b, 4)[0]
        flags = struct.unpack_from('<I', b, 8)[0]
        self.localized = bool(flags & 0x80)
        self.esl = bool(flags & 0x200)
        off = REC_HDR
        end = REC_HDR + size
        while off < end:
            t = b[off:off+4]
            sz = struct.unpack_from('<H', b, off+4)[0]
            if t == b'MAST':
                self.masters.append(b[off+6:off+6+sz].split(b'\x00')[0].decode('cp1252'))
            off += 6 + sz
        return end

    def top_groups(self):
        """yield (label, start_of_group, size)"""
        off = self.parse_header()
        n = len(self.buf)
        b = self.buf
        while off + GRP_HDR <= n:
            if b[off:off+4] != b'GRUP':
                break
            size = struct.unpack_from('<I', b, off+4)[0]
            label = b[off+8:off+12]
            if size < GRP_HDR:
                break
            yield label, off, size
            off += size

    def has_dial(self):
        try:
            for label, off, size in self.top_groups():
                if label == b'DIAL':
                    return (off, size)
        except Exception:
            return None
        return None


def subrecords(data):
    off = 0
    n = len(data)
    pending = None
    while off + 6 <= n:
        t = data[off:off+4]
        sz = struct.unpack_from('<H', data, off+4)[0]
        off += 6
        if t == b'XXXX':
            pending = struct.unpack_from('<I', data, off)[0]
            off += sz
            continue
        if pending is not None:
            sz = pending
            pending = None
        yield t, data[off:off+sz]
        off += sz


def record_data(buf, off):
    """returns (type, formid, data) for record at off"""
    t = buf[off:off+4]
    size = struct.unpack_from('<I', buf, off+4)[0]
    flags = struct.unpack_from('<I', buf, off+8)[0]
    formid = struct.unpack_from('<I', buf, off+12)[0]
    data = buf[off+REC_HDR:off+REC_HDR+size]
    if flags & 0x00040000:
        try:
            data = zlib.decompress(data[4:])
        except Exception:
            data = b''
    return t, formid, data, off + REC_HDR + size


def zstr(b):
    return b.split(b'\x00')[0].decode('utf-8', errors='replace')


def walk_dial(pl):
    """yield dicts describing player prompts."""
    loc = pl.has_dial()
    if not loc:
        return
    goff, gsize = loc
    buf = pl.buf
    off = goff + GRP_HDR
    end = goff + gsize
    cur_dial = None
    while off + REC_HDR <= end:
        sig = buf[off:off+4]
        if sig == b'GRUP':
            gs = struct.unpack_from('<I', buf, off+4)[0]
            gtype = struct.unpack_from('<i', buf, off+12)[0]
            if gtype == 7:  # topic children -> INFOs
                ioff = off + GRP_HDR
                iend = off + gs
                while ioff + REC_HDR <= iend:
                    if buf[ioff:ioff+4] == b'GRUP':
                        ioff += struct.unpack_from('<I', buf, ioff+4)[0]
                        continue
                    t, fid, data, nxt = record_data(buf, ioff)
                    if t == b'INFO':
                        info = {'dial': cur_dial, 'formid': fid, 'rnam': None,
                                'nam1': [], 'edid': None}
                        for st, sd in subrecords(data):
                            if st == b'EDID':
                                info['edid'] = zstr(sd)
                            elif st == b'RNAM':
                                info['rnam'] = zstr(sd) if not pl.localized else None
                                if pl.localized:
                                    info['rnam_id'] = struct.unpack_from('<I', sd, 0)[0] if len(sd) == 4 else None
                            elif st == b'NAM1':
                                if not pl.localized:
                                    info['nam1'].append(zstr(sd))
                        yield info
                    ioff = nxt
                off += gs
                continue
            else:
                off += gs
                continue
        t, fid, data, nxt = record_data(buf, off)
        if t == b'DIAL':
            d = {'formid': fid, 'edid': None, 'full': None, 'subtype': None, 'flags': None}
            for st, sd in subrecords(data):
                if st == b'EDID':
                    d['edid'] = zstr(sd)
                elif st == b'FULL':
                    if not pl.localized:
                        d['full'] = zstr(sd)
                elif st == b'DATA':
                    if len(sd) >= 4:
                        d['flags'] = sd[1]
                        d['subtype'] = struct.unpack_from('<H', sd, 2)[0]
                elif st == b'SNAM':
                    d['snam'] = sd.decode('cp1252', errors='replace')
            cur_dial = d
        off = nxt
