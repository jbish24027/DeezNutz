"""Byte-exact reimplementation of DBVO-SSEEdit-Topic-Extract.pas."""
import ctypes, struct, functools
from ctypes import wintypes
import espdial

LOCALE_USER_DEFAULT = 0x0400
NORM_IGNORECASE = 0x00000001
CSTR_LESS_THAN, CSTR_EQUAL, CSTR_GREATER_THAN = 1, 2, 3

_k32 = ctypes.WinDLL('kernel32', use_last_error=True)
_k32.CompareStringW.argtypes = [wintypes.LCID, wintypes.DWORD,
                                wintypes.LPCWSTR, ctypes.c_int,
                                wintypes.LPCWSTR, ctypes.c_int]
_k32.CompareStringW.restype = ctypes.c_int


def anscmptext(a, b):
    r = _k32.CompareStringW(LOCALE_USER_DEFAULT, NORM_IGNORECASE, a, len(a), b, len(b))
    if r == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return r - CSTR_EQUAL          # -1 / 0 / +1


def sorted_stringlist(items):
    """TStringList with Sorted=True, Duplicates=dupIgnore, CaseSensitive=False."""
    out = []
    for s in items:
        lo, hi = 0, len(out) - 1
        dup = False
        while lo <= hi:
            mid = (lo + hi) // 2
            c = anscmptext(out[mid], s)
            if c < 0:
                lo = mid + 1
            elif c > 0:
                hi = mid - 1
            else:
                dup = True
                break
        if not dup:
            out.insert(lo, s)
    return out


def cp1252(b):
    return b.split(b'\x00')[0].decode('cp1252', errors='replace')


def should_ignore(line, edid, formid):
    if (line.startswith('(') and line.endswith(')')) or \
       (line.startswith('[') and line.endswith(']')) or \
       (line.startswith('--') and line.endswith('--')):
        return True
    if str(formid) in line:
        return True
    if edid and edid in line:
        return True
    return False


def extract(path, lo_index=None):
    """Walk every DIAL/INFO in the file exactly as the .pas Process() does."""
    pl = espdial.Plugin(path)
    pl.parse_header()
    if pl.localized:
        return None
    loc = pl.has_dial()
    if not loc:
        return []
    goff, gsize = loc
    buf = pl.buf
    lines = []

    def do_record(t, fid, data):
        edid, rnam, full = '', None, None
        for st, sd in espdial.subrecords(data):
            if st == b'EDID':
                edid = cp1252(sd)
            elif st == b'RNAM':
                rnam = cp1252(sd)
            elif st == b'FULL':
                full = cp1252(sd)
        # GetLoadOrderFormID: local formid with the load-order index in the top byte
        lofid = fid if lo_index is None else (fid & 0x00FFFFFF) | (lo_index << 24)
        for line in (rnam, full):
            if line:
                if not should_ignore(line, edid, lofid):
                    lines.append(line)

    off, end = goff + 24, goff + gsize
    while off + 24 <= end:
        if buf[off:off+4] == b'GRUP':
            gs = struct.unpack_from('<I', buf, off+4)[0]
            gtype = struct.unpack_from('<i', buf, off+12)[0]
            if gtype == 7:
                ioff, iend = off + 24, off + gs
                while ioff + 24 <= iend:
                    if buf[ioff:ioff+4] == b'GRUP':
                        ioff += struct.unpack_from('<I', buf, ioff+4)[0]
                        continue
                    t, fid, data, nxt = espdial.record_data(buf, ioff)
                    if t == b'INFO':
                        do_record(t, fid, data)
                    ioff = nxt
            off += gs
            continue
        t, fid, data, nxt = espdial.record_data(buf, off)
        if t == b'DIAL':
            do_record(t, fid, data)
        off = nxt
    return sorted_stringlist(lines)


def write_topic_file(path, lines):
    with open(path, 'wb') as f:
        for s in lines:
            f.write(s.encode('cp1252', errors='replace') + b'\r\n')
