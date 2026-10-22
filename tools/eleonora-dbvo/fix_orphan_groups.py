"""Repair the two DBVO Fix plugins that carry a dialog child group with no parent DIAL record.

Diagnosis (see the session notes): in all three cases the GROUP LABEL is correct - the INFO
inside really does belong to the labelled topic in the master - and what is missing is the
parent DIAL override record. The groups even sit at exactly the right place in the
FormID-ascending record order. So the repair is to insert a DIAL override for the labelled
topic immediately before its group, copied verbatim from the current load-order winner (which
for all three is the master itself), with the master indices remapped.

That makes the file structurally valid without changing a single field of game data.
"""
import os, struct, shutil, sys
import vfs, espdial
import diag_content as C

STAMP = '20260828'
FIXES = [
    (r'C:\1. AUTHORIA\mods\Eleonora Female Nord Dbvo Pack With Patches\DBVO Fix - SDA.esp',
     'SeranaDialogAddon.esp'),
    (r'C:\1. AUTHORIA\mods\Eleonora Female Nord Dbvo Pack With Patches\DBVO Fix - DaCoda.esp',
     'DAc0da.esm'),
]
# DIAL subrecords that carry a FormID. PNAM on DIAL is a float priority, deliberately excluded.
FORMID_SUBS = (b'BNAM', b'QNAM')


def remap_formid(v, src_own_index, dst_index):
    idx = v >> 24
    if idx == src_own_index:
        return (dst_index << 24) | (v & 0xFFFFFF)
    raise ValueError('reference to master index %02X - not handled' % idx)


def build_dial(src_raw, src_own_index, dst_index):
    """copy a DIAL record verbatim, remapping its FormID and its BNAM/QNAM references"""
    out = bytearray(src_raw)
    fid = struct.unpack_from('<I', out, 12)[0]
    struct.pack_into('<I', out, 12, (dst_index << 24) | (fid & 0xFFFFFF))
    size = struct.unpack_from('<I', out, 4)[0]
    off, end = 24, 24 + size
    while off + 6 <= end:
        t = bytes(out[off:off+4])
        sz = struct.unpack_from('<H', out, off+4)[0]
        if t in FORMID_SUBS and sz == 4:
            v = struct.unpack_from('<I', out, off+6)[0]
            struct.pack_into('<I', out, off+6, remap_formid(v, src_own_index, dst_index))
        off += 6 + sz
    assert off == end, 'subrecord walk did not land on the record end'
    return bytes(out)


def orphan_groups(buf, goff, gsize):
    """[(group_offset, group_size, label)] for type-7 groups with no DIAL record in the file"""
    dials, groups = set(), []
    off, end = goff + 24, goff + gsize
    while off + 24 <= end:
        if buf[off:off+4] == b'GRUP':
            gs = struct.unpack_from('<I', buf, off+4)[0]
            label = struct.unpack_from('<I', buf, off+8)[0]
            gtype = struct.unpack_from('<i', buf, off+12)[0]
            groups.append((off, gs, label, gtype))
            off += gs
            continue
        t, fid, data, nxt = espdial.record_data(buf, off)
        if t == b'DIAL':
            dials.add(fid)
        off = nxt
    return [(o, s, l) for o, s, l, gt in groups if gt == 7 and l not in dials]


def repair(fix_path, master_name, dry_run=True):
    pp = vfs.plugin_paths()
    master_path = pp[master_name.lower()][0]
    fpl = espdial.Plugin(fix_path)
    fpl.parse_header()
    mpl = espdial.Plugin(master_path)
    mpl.parse_header()
    dst_index = [m.lower() for m in fpl.masters].index(master_name.lower())
    src_own = len(mpl.masters)
    buf = bytearray(fpl.buf)
    goff, gsize = fpl.has_dial()

    bad = orphan_groups(bytes(buf), goff, gsize)
    print('  %-24s masters=%s  master index=%d  source own index=%d'
          % (os.path.basename(fix_path), fpl.masters, dst_index, src_own))
    print('  orphaned groups: %d' % len(bad))
    if not bad:
        return 0

    mrecs, _ = C.records(master_path)
    inserts = []
    for off, size, label in bad:
        local = label & 0xFFFFFF
        key = ('DIAL', local)
        if key not in mrecs:
            raise SystemExit('  master has no DIAL %06X - aborting' % local)
        rec = build_dial(mrecs[key][0], src_own, dst_index)
        edid = ''
        for st, sd in espdial.subrecords(rec[24:]):
            if st == b'EDID':
                edid = sd.split(b'\x00')[0].decode('cp1252')
                break
        print('     group at %d (label %08X) <- insert DIAL %08X %-34s %d bytes'
              % (off, label, struct.unpack_from('<I', rec, 12)[0], edid, len(rec)))
        inserts.append((off, rec))

    # splice from the end so earlier offsets stay valid
    added = 0
    for off, rec in sorted(inserts, key=lambda x: -x[0]):
        buf[off:off] = rec
        added += len(rec)
    # grow the DIAL top-level group
    struct.pack_into('<I', buf, goff + 4, gsize + added)
    # HEDR "number of records" in these files counts records AND groups
    hoff = 24
    hend = 24 + struct.unpack_from('<I', buf, 4)[0]
    while hoff < hend:
        t = bytes(buf[hoff:hoff+4])
        sz = struct.unpack_from('<H', buf, hoff+4)[0]
        if t == b'HEDR':
            n = struct.unpack_from('<I', buf, hoff + 6 + 4)[0]
            struct.pack_into('<I', buf, hoff + 6 + 4, n + len(inserts))
            print('     HEDR record count %d -> %d' % (n, n + len(inserts)))
        hoff += 6 + sz

    if dry_run:
        print('     DRY RUN - %d bytes would be added (%d -> %d)'
              % (added, len(fpl.buf), len(buf)))
        return buf
    bak = fix_path + '.bak-orphangroup-' + STAMP
    if not os.path.exists(bak):
        shutil.copy2(fix_path, bak)
        print('     backup -> %s' % os.path.basename(bak))
    with open(fix_path, 'wb') as f:
        f.write(buf)
    print('     written: %d -> %d bytes' % (len(fpl.buf), len(buf)))
    return buf


if __name__ == '__main__':
    dry = '--write' not in sys.argv
    print('DRY RUN' if dry else 'WRITING')
    for path, master in FIXES:
        repair(path, master, dry_run=dry)
