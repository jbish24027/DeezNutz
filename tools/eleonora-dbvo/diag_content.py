"""Compare the orphaned INFO overrides with their master, and find who currently wins the
three parent DIAL records."""
import struct, os
import vfs, espdial
from pasrepro import cp1252

FIX_SDA = r'C:\1. AUTHORIA\mods\Eleonora Female Nord Dbvo Pack With Patches\DBVO Fix - SDA.esp'
FIX_DAC = r'C:\1. AUTHORIA\mods\Eleonora Female Nord Dbvo Pack With Patches\DBVO Fix - DaCoda.esp'


def records(path):
    """every DIAL/INFO record in the DIAL top group: fid -> (sig, raw bytes incl header, subs)"""
    pl = espdial.Plugin(path)
    pl.parse_header()
    loc = pl.has_dial()
    if not loc:
        return {}, pl
    goff, gsize = loc
    buf = pl.buf
    out = {}

    def take(off):
        t, fid, data, nxt = espdial.record_data(buf, off)
        subs = [(st.decode(), sd) for st, sd in espdial.subrecords(data)]
        out.setdefault((t.decode(), fid & 0xFFFFFF), (buf[off:nxt], subs))
        return nxt

    off, end = goff + 24, goff + gsize
    while off + 24 <= end:
        if buf[off:off+4] == b'GRUP':
            gs = struct.unpack_from('<I', buf, off+4)[0]
            if struct.unpack_from('<i', buf, off+12)[0] == 7:
                ioff, iend = off + 24, off + gs
                while ioff + 24 <= iend:
                    if buf[ioff:ioff+4] == b'GRUP':
                        ioff += struct.unpack_from('<I', buf, ioff+4)[0]
                        continue
                    ioff = take(ioff)
            off += gs
            continue
        off = take(off)
    return out, pl


def show(tag, subs, only=('EDID', 'FULL', 'RNAM', 'NAM1', 'PNAM', 'DATA', 'SNAM', 'QNAM', 'BNAM', 'TIFC')):
    for st, sd in subs:
        if st not in only:
            continue
        if st in ('EDID', 'FULL', 'RNAM', 'NAM1'):
            v = repr(cp1252(sd))
        else:
            v = sd.hex()
        print('      %-6s %s' % (st, v[:120]))


pp = vfs.plugin_paths()
CASES = [
    ('SDA', FIX_SDA, pp['seranadialogaddon.esp'][0], [(0x045BF6, 0x045BFA), (0x0660BA, 0x0660C3)]),
    ('DAc0da', FIX_DAC, pp['dac0da.esm'][0], [(0x005292, 0x005293)]),
]

for tag, fix, master, cases in CASES:
    fr, fpl = records(fix)
    mr, mpl = records(master)
    print('=' * 90)
    print(tag, os.path.basename(fix), ' master localized=%s' % mpl.localized)
    for dial, info in cases:
        print('  --- DIAL %06X / INFO %06X ---' % (dial, info))
        print('    master DIAL record present: %s' % (('DIAL', dial) in mr))
        if ('DIAL', dial) in mr:
            print('    master DIAL subrecords:')
            show('m', mr[('DIAL', dial)][1])
        print('    fix INFO record:')
        show('f', fr[('INFO', info)][1])
        if ('INFO', info) in mr:
            print('    master INFO record:')
            show('m', mr[('INFO', info)][1])
        a = fr[('INFO', info)][1]
        b = mr.get(('INFO', info), (None, []))[1]
        sa = {k: v for k, v in a}
        sb = {k: v for k, v in b}
        diff = [k for k in set(sa) | set(sb) if sa.get(k) != sb.get(k)]
        print('    subrecords that differ from master: %s' % sorted(diff))
