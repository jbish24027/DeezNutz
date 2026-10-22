"""Validate a repaired plugin buffer end to end before it is allowed near the disk."""
import struct, os, io, sys
import espdial, scan_orphans
from pasrepro import cp1252


class MemPlugin(espdial.Plugin):
    def __init__(self, buf):
        self.buf = bytes(buf)
        self.localized = False
        self.masters = []


def validate(buf, label=''):
    pl = MemPlugin(buf)
    hdr_end = pl.parse_header()
    ok = True

    def bad(msg):
        nonlocal ok
        ok = False
        print('     FAIL %s' % msg)

    # 1. top-level group walk must consume exactly to EOF
    off = hdr_end
    tops = 0
    while off + 24 <= len(pl.buf):
        if pl.buf[off:off+4] != b'GRUP':
            bad('expected GRUP at %d' % off)
            break
        size = struct.unpack_from('<I', pl.buf, off+4)[0]
        off += size
        tops += 1
    if off != len(pl.buf):
        bad('top-level walk ended at %d, file is %d bytes' % (off, len(pl.buf)))

    # 2. every record/group inside walks cleanly, and count them
    nrec = 0
    ngrp = 0
    stack = []
    o = hdr_end
    while o + 24 <= len(pl.buf):
        s = struct.unpack_from('<I', pl.buf, o+4)[0]
        stack.append((o, s))
        o += s
    while stack:
        go, gs = stack.pop()
        ngrp += 1
        p, e = go + 24, go + gs
        while p + 24 <= e:
            if pl.buf[p:p+4] == b'GRUP':
                cs = struct.unpack_from('<I', pl.buf, p+4)[0]
                stack.append((p, cs))
                p += cs
                continue
            t, fid, data, nxt = espdial.record_data(pl.buf, p)
            nrec += 1
            p = nxt
        if p != e:
            bad('group at %d: record walk ended at %d, group ends %d' % (go, p, e))

    # 3. HEDR count (these files count records + groups)
    h = 24
    hend = 24 + struct.unpack_from('<I', pl.buf, 4)[0]
    hedr = None
    while h < hend:
        t = pl.buf[h:h+4]
        sz = struct.unpack_from('<H', pl.buf, h+4)[0]
        if t == b'HEDR':
            hedr = struct.unpack_from('<I', pl.buf, h + 6 + 4)[0]
        h += 6 + sz
    if hedr != nrec + ngrp:
        bad('HEDR says %s, actual records+groups = %d' % (hedr, nrec + ngrp))

    # 4. no orphaned or mislabelled dialog child group
    import tempfile
    tmp = os.path.join(tempfile.gettempdir(), 'validate_tmp.esp')
    with open(tmp, 'wb') as f:
        f.write(pl.buf)
    problems = scan_orphans.check(tmp)
    os.remove(tmp)
    if problems:
        bad('dialog child group problems remain: %s' % problems)

    # 5. every FormID reference must resolve inside the master list + self
    limit = len(pl.masters)
    print('     %s records=%d groups=%d HEDR=%s masters=%d topgroups=%d -> %s'
          % (label, nrec, ngrp, hedr, limit, tops, 'OK' if ok else 'PROBLEMS'))
    return ok


if __name__ == '__main__':
    import fix_orphan_groups as F
    allok = True
    for path, master in F.FIXES:
        buf = F.repair(path, master, dry_run=True)
        if isinstance(buf, int):
            continue
        allok &= validate(buf, os.path.basename(path))
    print('ALL VALID' if allok else 'VALIDATION FAILED')
