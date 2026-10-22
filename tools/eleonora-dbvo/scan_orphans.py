"""Scan every active plugin for type-7 dialog child groups whose parent DIAL record is missing
or whose label does not match the DIAL that precedes them."""
import struct, sys
import vfs, espdial


def check(path):
    pl = espdial.Plugin(path)
    pl.parse_header()
    loc = pl.has_dial()
    if not loc:
        return []
    goff, gsize = loc
    buf = pl.buf
    off, end = goff + 24, goff + gsize
    last = None
    bad = []
    seen_dials = set()
    groups = []
    while off + 24 <= end:
        if buf[off:off+4] == b'GRUP':
            gs = struct.unpack_from('<I', buf, off+4)[0]
            label = struct.unpack_from('<I', buf, off+8)[0]
            gtype = struct.unpack_from('<i', buf, off+12)[0]
            groups.append((label, gtype, last))
            off += gs
            continue
        t, fid, data, nxt = espdial.record_data(buf, off)
        if t == b'DIAL':
            last = fid
            seen_dials.add(fid)
        off = nxt
    for label, gtype, prev in groups:
        if gtype != 7:
            bad.append(('non-type-7 group in DIAL top group', label, gtype, prev))
        elif label not in seen_dials:
            bad.append(('orphan: no DIAL record for label', label, gtype, prev))
        elif label != prev:
            bad.append(('label != preceding DIAL (record exists elsewhere)', label, gtype, prev))
    return bad


if __name__ == '__main__':
    pp = vfs.plugin_paths()
    total = 0
    for p in vfs.active_plugins():
        ent = pp.get(p.lower())
        if not ent:
            continue
        try:
            bad = check(ent[0])
        except Exception as e:
            print('%-50s PARSE ERROR %r' % (p, e))
            continue
        if bad:
            total += 1
            print('%-50s  (%s)' % (p, ent[1]))
            for kind, label, gtype, prev in bad:
                print('    %-52s label=%08X prev DIAL=%s'
                      % (kind, label, ('%08X' % prev) if prev is not None else 'None'))
    print('\nplugins with a malformed dialog child group: %d' % total)
