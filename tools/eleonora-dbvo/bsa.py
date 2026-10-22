"""Minimal Skyrim SE BSA (version 105) reader - just enough to pull a file out by path."""
import struct, zlib, os

try:
    import lz4.block as _lz4
except ImportError:
    _lz4 = None


class BSA:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            hdr = f.read(36)
            if hdr[:4] != b'BSA\x00':
                raise ValueError('not a BSA: %s' % path)
            (self.version, offset, self.flags, self.folder_count, self.file_count,
             self.tot_folder_name_len, self.tot_file_name_len, self.file_flags) = \
                struct.unpack_from('<IIIIIIII', hdr, 4)
            f.seek(offset)
            fr_size = 24 if self.version >= 105 else 16
            folders = []
            raw = f.read(fr_size * self.folder_count)
            for i in range(self.folder_count):
                if self.version >= 105:
                    _h, cnt, _pad, off = struct.unpack_from('<QIIQ', raw, i * fr_size)
                else:
                    _h, cnt, off = struct.unpack_from('<QII', raw, i * fr_size)
                folders.append((cnt, off - self.tot_file_name_len))
            self.files = []                       # (folder_name, size_field, data_offset)
            for cnt, off in folders:
                f.seek(off)
                fname = ''
                if self.flags & 0x1:
                    n = f.read(1)[0]
                    fname = f.read(n).split(b'\x00')[0].decode('cp1252')
                blk = f.read(16 * cnt)
                for j in range(cnt):
                    _h, size, doff = struct.unpack_from('<QII', blk, j * 16)
                    self.files.append([fname, size, doff, None])
            if self.flags & 0x2:                  # file name block, same order
                names = f.read(self.tot_file_name_len).split(b'\x00')
                for i, rec in enumerate(self.files):
                    if i < len(names):
                        rec[3] = names[i].decode('cp1252')
        self.index = {}
        for fname, size, doff, name in self.files:
            if name is None:
                continue
            key = (fname + '\\' + name).lower().replace('/', '\\')
            self.index[key] = (size, doff)

    def read(self, path):
        key = path.lower().replace('/', '\\')
        if key not in self.index:
            return None
        size, doff = self.index[key]
        toggled = bool(size & 0x40000000)
        size &= 0x3FFFFFFF
        compressed = bool(self.flags & 0x4) != toggled
        with open(self.path, 'rb') as f:
            f.seek(doff)
            if self.flags & 0x100:                # embedded file name
                n = f.read(1)[0]
                f.read(n)
                size -= n + 1
            blob = f.read(size)
        if not compressed:
            return blob
        orig = struct.unpack_from('<I', blob, 0)[0]
        body = blob[4:]
        if self.version >= 105:
            if _lz4 is None:
                raise RuntimeError('lz4 needed for SSE BSA decompression')
            return _lz4.decompress(body, uncompressed_size=orig)
        return zlib.decompress(body)


_cache = {}


def open_bsa(path):
    p = os.path.normcase(path)
    if p not in _cache:
        try:
            _cache[p] = BSA(path)
        except Exception:
            _cache[p] = None
    return _cache[p]
