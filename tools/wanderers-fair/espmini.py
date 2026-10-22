"""Minimal SSE plugin reader/writer for the fair patch build (records + subrecords, zlib, VMAD walk)."""
import struct, zlib

REC_HDR = 24


def read_plugin(path):
    data = open(path, "rb").read()
    return data


def iter_records(data, start=0, end=None, path=()):
    """Yield (type, flags, formid, version_info, form_version, unk, payload_bytes, offset, grup_path) for every record."""
    end = len(data) if end is None else end
    off = start
    while off < end:
        typ = data[off:off + 4]
        size = struct.unpack_from("<I", data, off + 4)[0]
        if typ == b"GRUP":
            label = data[off + 8:off + 12]
            gtype = struct.unpack_from("<i", data, off + 12)[0]
            yield from iter_records(data, off + 24, off + size, path + ((label, gtype),))
            off += size
            continue
        flags, formid, vc = struct.unpack_from("<III", data, off + 8)
        fver, unk = struct.unpack_from("<HH", data, off + 20)
        raw = data[off + REC_HDR:off + REC_HDR + size]
        if flags & 0x40000:
            payload = zlib.decompress(raw[4:])
            assert len(payload) == struct.unpack_from("<I", raw, 0)[0]
        else:
            payload = raw
        yield (typ.decode(), flags, formid, vc, fver, unk, payload, off, path)
        off += REC_HDR + size


def subrecords(payload):
    out = []
    off = 0
    big = None
    while off < len(payload):
        sig = payload[off:off + 4].decode()
        size = struct.unpack_from("<H", payload, off + 4)[0]
        off += 6
        if sig == "XXXX":
            big = struct.unpack_from("<I", payload, off)[0]
            off += size
            continue
        if big is not None:
            size = big
            big = None
        out.append([sig, payload[off:off + size]])
        off += size
    return out


def pack_subrecords(subs):
    b = bytearray()
    for sig, d in subs:
        if len(d) > 0xFFFF:
            b += b"XXXX" + struct.pack("<H", 4) + struct.pack("<I", len(d))
            b += sig.encode() + struct.pack("<H", 0) + d
        else:
            b += sig.encode() + struct.pack("<H", len(d)) + d
    return bytes(b)


def pack_record(typ, flags, formid, vc, fver, unk, payload):
    flags &= ~0x40000  # write uncompressed
    return typ.encode() + struct.pack("<IIIIHH", len(payload), flags, formid, vc, fver, unk) + payload


def pack_grup(label, gtype, body, stamp=0, vc=0, unk=0):
    # GRUP header: sig, total size, label, group type, timestamp u16, version control u16, unknown u32 = 24 bytes
    return b"GRUP" + struct.pack("<I4siHHI", 24 + len(body), label, gtype, stamp, vc, unk) + body


def tes4_masters(data):
    typ, flags, formid, vc, fver, unk, payload, off, path = next(iter_records(data[:struct.unpack_from("<I", data, 4)[0] + 24]))
    assert typ == "TES4"
    subs = subrecords(payload)
    masters = [d[:-1].decode("cp1252") for s, d in subs if s == "MAST"]
    return flags, fver, subs, masters


# ---------------- VMAD walk ----------------

def _wstr(b, o):
    n = struct.unpack_from("<H", b, o)[0]
    return b[o + 2:o + 2 + n].decode("cp1252"), o + 2 + n


def walk_vmad(b):
    """Return (version, objfmt, scripts, end_offset) where scripts = [(name, status, [(pname, ptype, pstatus, value_offset, value_len, value)])]."""
    ver, objfmt, nscripts = struct.unpack_from("<hhH", b, 0)
    o = 6
    scripts = []
    for _ in range(nscripts):
        name, o = _wstr(b, o)
        status = b[o]; o += 1
        nprops = struct.unpack_from("<H", b, o)[0]; o += 2
        props = []
        for _ in range(nprops):
            pname, o = _wstr(b, o)
            ptype = b[o]; pstatus = b[o + 1]; o += 2
            vstart = o
            if ptype == 1:
                if objfmt == 2:
                    _u, alias, fid = struct.unpack_from("<HhI", b, o)
                else:
                    fid, alias, _u = struct.unpack_from("<IhH", b, o)
                val = (fid, alias); o += 8
            elif ptype == 2:
                val, o = _wstr(b, o)
            elif ptype == 3:
                val = struct.unpack_from("<i", b, o)[0]; o += 4
            elif ptype == 4:
                val = struct.unpack_from("<f", b, o)[0]; o += 4
            elif ptype == 5:
                val = b[o]; o += 1
            elif ptype in (11, 12, 13, 14, 15):
                n = struct.unpack_from("<I", b, o)[0]; o += 4
                if ptype == 11:
                    val = []
                    for _ in range(n):
                        if objfmt == 2:
                            _u, alias, fid = struct.unpack_from("<HhI", b, o)
                        else:
                            fid, alias, _u = struct.unpack_from("<IhH", b, o)
                        val.append((fid, alias)); o += 8
                elif ptype == 12:
                    val = []
                    for _ in range(n):
                        s, o = _wstr(b, o); val.append(s)
                elif ptype == 13:
                    val = list(struct.unpack_from("<%di" % n, b, o)); o += 4 * n
                elif ptype == 14:
                    val = list(struct.unpack_from("<%df" % n, b, o)); o += 4 * n
                else:
                    val = list(b[o:o + n]); o += n
            else:
                raise ValueError("unknown property type %d at %d" % (ptype, o))
            props.append((pname, ptype, pstatus, vstart, o - vstart, val))
        scripts.append((name, status, props))
    return ver, objfmt, scripts, o
