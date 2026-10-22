"""Minimal NIF header parser: block types + string table. Enough to detect the HDT-SMP physics link."""
import struct

PHYS = "HDT Skinned Mesh Physics Object"


def parse_header(buf):
    """buf: bytes of at least the header. Returns dict(version, bsver, nblocks, block_types, strings) or raises."""
    nl = buf.find(b"\n")
    if nl < 0 or not buf.startswith((b"Gamebryo File Format", b"NetImmerse File Format")):
        raise ValueError("not a nif")
    pos = nl + 1
    version, = struct.unpack_from("<I", buf, pos); pos += 4
    if version < 0x14000000:
        raise ValueError("old nif version")
    endian = buf[pos]; pos += 1
    userver, = struct.unpack_from("<I", buf, pos); pos += 4
    nblocks, = struct.unpack_from("<I", buf, pos); pos += 4
    bsver = 0
    if userver >= 3:
        bsver, = struct.unpack_from("<I", buf, pos); pos += 4
        # export info: 3 short strings (author, process script, export script)
        for _ in range(3):
            ln = buf[pos]; pos += 1 + ln
        if bsver == 130:
            ln = buf[pos]; pos += 1 + ln
    nbt, = struct.unpack_from("<H", buf, pos); pos += 2
    btypes = []
    for _ in range(nbt):
        ln, = struct.unpack_from("<I", buf, pos); pos += 4
        btypes.append(buf[pos:pos + ln].decode("latin-1")); pos += ln
    bidx = list(struct.unpack_from("<%dH" % nblocks, buf, pos)); pos += 2 * nblocks
    if version >= 0x14020005:
        pos += 4 * nblocks  # block sizes
    nstr, = struct.unpack_from("<I", buf, pos); pos += 4
    pos += 4  # max string length
    strings = []
    for _ in range(nstr):
        ln, = struct.unpack_from("<I", buf, pos); pos += 4
        strings.append(buf[pos:pos + ln].decode("latin-1", "replace")); pos += ln
    return dict(version=version, bsver=bsver, nblocks=nblocks, block_types=btypes,
                block_type_of=[btypes[i] if i < len(btypes) else "?" for i in bidx], strings=strings)


def physics_info(buf):
    """Return (has_phys_link: bool, xml_paths: list, bsver) from header bytes."""
    h = parse_header(buf)
    has_sed = "NiStringExtraData" in h["block_types"]
    has_name = PHYS in h["strings"]
    xmls = [s for s in h["strings"] if s.lower().endswith(".xml")]
    return (has_sed and has_name), xmls, h["bsver"], h


def read_head(path, n=262144):
    with open(path, "rb") as f:
        return f.read(n)


def file_physics(path):
    buf = read_head(path)
    try:
        return physics_info(buf)
    except (struct.error, IndexError):
        buf = read_head(path, 4 * 1024 * 1024)
        return physics_info(buf)
