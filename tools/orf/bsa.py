"""
Minimal Bethesda BSA reader for SSE (v105) and Oldrim/SSE (v104).

Only what this job needs: list paths, extract one file's bytes.
v105 payloads are LZ4 block-compressed; v104 uses zlib.
"""

import struct
import os
import zlib

try:
    # SSE (BSA v105) payloads are LZ4 FRAME format, not raw LZ4 blocks.
    import lz4.frame as _lz4f
    import lz4.block as _lz4b
except ImportError:
    _lz4f = _lz4b = None

FLAG_DIRNAMES = 0x1
FLAG_FILENAMES = 0x2
FLAG_COMPRESSED = 0x4
FLAG_EMBED_NAMES = 0x100


class Bsa:
    def __init__(self, path):
        self.path = path
        self.files = {}          # 'meshes\\foo\\bar.nif' -> (offset, rawsize, compressed)
        self._parse()

    def _parse(self):
        with open(self.path, 'rb') as fh:
            head = fh.read(36)
            if len(head) < 36 or head[:4] != b'BSA\x00':
                raise ValueError('not a BSA: %s' % self.path)
            (_id, ver, off, aflags, nfold, nfile,
             lfoldname, lfilename, _fflags) = struct.unpack('<4sIIIIIIII', head)
            self.version = ver
            self.default_compressed = bool(aflags & FLAG_COMPRESSED)
            self.embed_names = bool(aflags & FLAG_EMBED_NAMES)

            fh.seek(off)
            frec = 24 if ver >= 105 else 16
            folders = []
            blob = fh.read(nfold * frec)
            for i in range(nfold):
                b = blob[i * frec:(i + 1) * frec]
                if ver >= 105:
                    _h, cnt, _u, foff = struct.unpack('<QIIQ', b)
                else:
                    _h, cnt, foff = struct.unpack('<QII', b)
                folders.append((cnt, foff))

            entries = []          # (folder_name, [(size, offset), ...])
            for cnt, foff in folders:
                # foff is measured from the start of the file, minus totalFileNameLength
                fh.seek(foff - lfilename)
                name = ''
                if aflags & FLAG_DIRNAMES:
                    ln = fh.read(1)[0]
                    name = fh.read(ln)[:-1].decode('cp1252', 'replace')
                fl = []
                fb = fh.read(cnt * 16)
                for j in range(cnt):
                    _h, sz, o = struct.unpack('<QII', fb[j * 16:(j + 1) * 16])
                    fl.append((sz, o))
                entries.append((name, fl))

            names = []
            if aflags & FLAG_FILENAMES:
                blk = fh.read(lfilename)
                names = [x.decode('cp1252', 'replace') for x in blk.split(b'\x00') if x]

        k = 0
        for folder, fl in entries:
            for sz, o in fl:
                fname = names[k] if k < len(names) else 'unknown_%d' % k
                k += 1
                comp = self.default_compressed
                if sz & 0x40000000:
                    comp = not comp
                    sz &= 0x3FFFFFFF
                full = (folder + '\\' + fname).lower().lstrip('\\')
                self.files[full] = (o, sz, comp)

    def read(self, path):
        key = path.lower().replace('/', '\\').lstrip('\\')
        rec = self.files.get(key)
        if rec is None:
            return None
        off, size, comp = rec
        with open(self.path, 'rb') as fh:
            fh.seek(off)
            data = fh.read(size)
        i = 0
        if self.embed_names:
            ln = data[0]
            i = 1 + ln
        if comp:
            orig = struct.unpack_from('<I', data, i)[0]
            payload = data[i + 4:]
            if self.version >= 105:
                if _lz4f is None:
                    raise RuntimeError('lz4 needed for SSE BSA')
                try:
                    return _lz4f.decompress(payload)
                except Exception:
                    # a few SSE archives are repacked with zlib or raw blocks
                    try:
                        return zlib.decompress(payload)
                    except Exception:
                        return _lz4b.decompress(payload, uncompressed_size=orig)
            return zlib.decompress(payload)
        return data[i:]


class BsaIndex:
    """Path -> (bsa_path, providing mod). Later-added archives win."""

    def __init__(self):
        self.map = {}
        self._open = {}

    def add(self, bsa_path, mod):
        try:
            b = Bsa(bsa_path)
        except Exception:
            return 0
        n = 0
        for p in b.files:
            if p.startswith(('meshes\\', 'textures\\')):
                self.map[p] = (bsa_path, mod)
                n += 1
        return n

    def read(self, path):
        key = path.lower().replace('/', '\\').lstrip('\\')
        hit = self.map.get(key)
        if not hit:
            return None, None
        bsa_path, mod = hit
        b = self._open.get(bsa_path)
        if b is None:
            b = self._open[bsa_path] = Bsa(bsa_path)
        try:
            return b.read(key), mod
        except Exception:
            return None, mod
