"""Rewrite a BSDismemberSkinInstance body-part id inside Skyrim SE .nif files.

Used to move the Einar backpack off the quiver's biped slot: every partition
tagged 60 becomes 47, leaving the body partitions (32) alone. Size-preserving,
so no block sizes or offsets shift.

Parses the real NIF header (block type table + per-block sizes) and only writes
inside blocks whose type is BSDismemberSkinInstance - it never pattern-matches
raw bytes.

    python repartition.py --from 60 --to 47 <file-or-dir> ...        # dry run
    python repartition.py --from 60 --to 47 --apply <paths>
"""
import argparse
import os
import shutil
import struct
import sys

HEADER_TAIL = b"\n"


class Nif:
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as fh:
            self.buf = bytearray(fh.read())
        self._parse_header()

    def _u8(self):
        v = self.buf[self.pos]
        self.pos += 1
        return v

    def _u16(self):
        v = struct.unpack_from("<H", self.buf, self.pos)[0]
        self.pos += 2
        return v

    def _u32(self):
        v = struct.unpack_from("<I", self.buf, self.pos)[0]
        self.pos += 4
        return v

    def _sized(self):
        n = self._u32()
        s = bytes(self.buf[self.pos:self.pos + n])
        self.pos += n
        return s

    def _export(self):
        n = self._u8()
        s = bytes(self.buf[self.pos:self.pos + n])
        self.pos += n
        return s

    def _parse_header(self):
        end = self.buf.find(HEADER_TAIL)
        if end < 0 or not self.buf.startswith(b"Gamebryo File Format"):
            raise ValueError("not a Gamebryo nif")
        self.header_string = bytes(self.buf[:end])
        self.pos = end + 1
        self.version = self._u32()
        self.endian = self._u8()
        self.user_version = self._u32()
        self.num_blocks = self._u32()
        self.bs_version = self._u32()
        if self.bs_version >= 130:
            raise ValueError("bsVersion %d not supported (FO4-era header)" % self.bs_version)
        self._export()          # author
        self._export()          # process script
        self._export()          # export script
        n_types = self._u16()
        self.block_types = [self._sized().decode("latin1") for _ in range(n_types)]
        self.block_type_index = [self._u16() for _ in range(self.num_blocks)]
        self.block_size = [self._u32() for _ in range(self.num_blocks)]
        n_strings = self._u32()
        self._u32()             # max string length
        self.strings = [self._sized() for _ in range(n_strings)]
        n_groups = self._u32()
        for _ in range(n_groups):
            self._u32()
        self.blocks_start = self.pos

    def block_span(self, i):
        off = self.blocks_start + sum(self.block_size[:i])
        return off, self.block_size[i]

    def type_of(self, i):
        return self.block_types[self.block_type_index[i] & 0x7FFF]

    def dismember_partitions(self):
        """[(absolute offset of the bodyPart u16, current value)] over every
        BSDismemberSkinInstance block."""
        out = []
        for i in range(self.num_blocks):
            if self.type_of(i) != "BSDismemberSkinInstance":
                continue
            off, size = self.block_span(i)
            p = off + 12                                   # data, skinPartition, skeletonRoot
            num_bones = struct.unpack_from("<I", self.buf, p)[0]
            p += 4 + 4 * num_bones
            num_parts = struct.unpack_from("<I", self.buf, p)[0]
            p += 4
            if num_parts > 100 or p + num_parts * 4 > off + size:
                raise ValueError("%s: implausible partition list in block %d" % (self.path, i))
            for _ in range(num_parts):
                body_at = p + 2                            # skip the u16 part flags
                out.append((body_at, struct.unpack_from("<H", self.buf, body_at)[0]))
                p += 4
        return out

    def write(self):
        with open(self.path, "wb") as fh:
            fh.write(self.buf)


def walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in names:
                    if n.lower().endswith(".nif"):
                        yield os.path.join(root, n)
        else:
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--from", dest="src", type=int, required=True)
    ap.add_argument("--to", dest="dst", type=int, required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-suffix", default=".bak-slot")
    a = ap.parse_args()

    total = touched = 0
    for path in sorted(set(walk(a.paths))):
        try:
            nif = Nif(path)
            parts = nif.dismember_partitions()
        except Exception as exc:                       # noqa: BLE001 - report and skip
            print("SKIP  %s  (%s)" % (path, exc))
            continue
        hits = [(o, v) for o, v in parts if v == a.src]
        others = sorted({v for _, v in parts if v != a.src})
        print("%-4s %-3d/%-3d  %s   others: %s"
              % ("HIT" if hits else "-", len(hits), len(parts), path, others or "none"))
        if not hits:
            continue
        total += len(hits)
        touched += 1
        if a.apply:
            shutil.copy2(path, path + a.backup_suffix)
            for off, _ in hits:
                struct.pack_into("<H", nif.buf, off, a.dst)
            nif.write()
            check = [v for _, v in Nif(path).dismember_partitions()]
            if a.src in check:
                sys.exit("VERIFY FAILED, %s still has %d" % (path, a.src))
            print("      -> written, partitions now %s" % sorted(set(check)))

    print("\n%d partition(s) across %d file(s)%s"
          % (total, touched, "" if a.apply else "  [dry run - nothing written]"))


if __name__ == "__main__":
    main()
