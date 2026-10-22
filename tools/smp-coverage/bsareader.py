"""Minimal BSA (v104 LE / v105 SE) directory reader + single-file extractor."""
import struct, zlib
try:
    import lz4.frame as lz4f
except ImportError:
    lz4f = None


def bzstring(buf, pos):
    ln = buf[pos]
    s = buf[pos + 1:pos + 1 + ln].rstrip(b"\0").decode("latin-1")
    return s, pos + 1 + ln


class BSA:
    def __init__(self, path):
        self.path = path
        self.f = open(path, "rb")
        hdr = self.f.read(36)
        if hdr[:4] != b"BSA\0":
            raise ValueError("not a bsa: " + path)
        (self.version, self.folder_off, self.flags, self.nfolders, self.nfiles,
         self.tfnl, self.tfilenl, self.file_flags, _pad) = struct.unpack("<IIIIIIIHH", hdr[4:])
        self.files = {}  # lower "folder\\file" -> (offset, size, compressed_flag)
        self._read_dir()

    def _read_dir(self):
        f = self.f
        f.seek(self.folder_off)
        if self.version >= 105:
            frs = f.read(24 * self.nfolders)
            folders = [struct.unpack_from("<QIIQ", frs, i * 24) for i in range(self.nfolders)]
            folders = [(h, c, off) for (h, c, _p, off) in folders]
        else:
            frs = f.read(16 * self.nfolders)
            folders = [struct.unpack_from("<QII", frs, i * 16) for i in range(self.nfolders)]
        # file record blocks follow immediately; read the rest of the directory area in one go
        # compute end: folder record blocks + file names block
        start = f.tell()
        blob_len = 0
        for (_h, c, _o) in folders:
            blob_len += (1 + 0) + 16 * c  # name length unknown yet; we'll read sequentially instead
        # sequential read
        recs = []
        for (_h, c, _o) in folders:
            name = ""
            if self.flags & 0x1:
                ln = f.read(1)[0]
                name = f.read(ln).rstrip(b"\0").decode("latin-1")
            data = f.read(16 * c)
            fr = [struct.unpack_from("<QII", data, i * 16) for i in range(c)]
            recs.append((name, fr))
        names = []
        if self.flags & 0x2:
            nb = f.read(self.tfilenl)
            names = nb.split(b"\0")
        idx = 0
        default_comp = bool(self.flags & 0x4)
        for name, fr in recs:
            for (_h, size, off) in fr:
                fname = names[idx].decode("latin-1") if idx < len(names) else "?%d" % idx
                idx += 1
                comp = default_comp
                if size & 0x40000000:
                    comp = not comp
                    size &= ~0x40000000
                key = (name + "\\" + fname).lower() if name else fname.lower()
                self.files[key] = (off, size, comp)

    def read(self, key, head_only=0):
        off, size, comp = self.files[key.lower()]
        f = self.f
        f.seek(off)
        if self.flags & 0x100:
            ln = f.read(1)[0]
            f.read(ln)
            size -= 1 + ln
        if not comp:
            return f.read(size if not head_only else min(size, head_only))
        orig, = struct.unpack("<I", f.read(4))
        data = f.read(size - 4)
        if self.version >= 105:
            if lz4f is None:
                raise RuntimeError("lz4 missing")
            return lz4f.decompress(data)
        return zlib.decompress(data)

    def close(self):
        self.f.close()
