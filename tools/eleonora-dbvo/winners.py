"""Resolve, for every dialogue string, which plugin actually wins the record."""
import os, struct, sys, json, pickle
import vfs, espdial, pasrepro, bsa
from pasrepro import cp1252, should_ignore


def load_order():
    """true game order, active plugins only"""
    order = []
    active = {p.lower() for p in vfs.active_plugins()}
    with open(os.path.join(vfs.PROFILE, 'loadorder.txt'), encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.lower() in active:
                order.append(line)
    return order


def definer(fid, masters, selfname):
    i = fid >> 24
    return (masters[i] if i < len(masters) else selfname).lower()


_BSA_INDEX = None


def _all_bsas():
    """every .bsa the VFS exposes, highest-priority mod first, Stock Game last"""
    global _BSA_INDEX
    if _BSA_INDEX is None:
        _BSA_INDEX = []
        for mod in vfs.enabled_mods():
            d = os.path.join(vfs.MODS, mod)
            try:
                for n in os.listdir(d):
                    if n.lower().endswith('.bsa'):
                        _BSA_INDEX.append(os.path.join(d, n))
            except (FileNotFoundError, NotADirectoryError):
                pass
        try:
            for n in os.listdir(vfs.DATA):
                if n.lower().endswith('.bsa'):
                    _BSA_INDEX.append(os.path.join(vfs.DATA, n))
        except FileNotFoundError:
            pass
    return _BSA_INDEX


def _strings_bytes(path):
    """Strings\\<name>_English.STRINGS: loose next to the plugin, else inside a BSA.

    Vanilla and every Creation Club plugin keep theirs in an archive, so the
    loose-only lookup used to drop those plugins without a word.
    """
    base = os.path.splitext(os.path.basename(path))[0]
    loose = os.path.join(os.path.dirname(path), 'Strings', base + '_English.STRINGS')
    if os.path.exists(loose):
        with open(loose, 'rb') as fh:
            return fh.read()
    want = ('strings\\%s_english.strings' % base).lower()
    own = [p for p in _all_bsas()
           if os.path.splitext(os.path.basename(p))[0].lower().split(' - ')[0] == base.lower()]
    for cand in own + _all_bsas():
        a = bsa.open_bsa(cand)
        if a is None:
            continue
        d = a.read(want)
        if d is not None:
            return d
    return None


def _strings_table(path):
    b = _strings_bytes(path)
    if b is None:
        return None
    count = struct.unpack_from('<I', b, 0)[0]
    dstart = 8 + count * 8
    t = {}
    for i in range(count):
        sid, off = struct.unpack_from('<II', b, 8 + i * 8)
        p = dstart + off
        t[sid] = b[p:b.index(b'\x00', p)].decode('cp1252', errors='replace')
    return t


def scan(path, selfname):
    """yield ((key, kind), text, edid, fid) for every DIAL FULL / INFO RNAM"""
    pl = espdial.Plugin(path)
    pl.parse_header()
    strtbl = _strings_table(path) if pl.localized else None
    if pl.localized and strtbl is None:
        sys.stderr.write('WARNING no English STRINGS for localized plugin %s - '
                         'its dialogue is being skipped\n' % selfname)
        return
    loc = pl.has_dial()
    if not loc:
        return
    masters = pl.masters
    goff, gsize = loc
    buf = pl.buf

    def emit(sig, fid, data):
        edid, rnam, full = '', None, None

        def text(sd):
            if strtbl is None:
                return cp1252(sd)
            return strtbl.get(struct.unpack_from('<I', sd, 0)[0]) if len(sd) == 4 else None

        for st, sd in espdial.subrecords(data):
            if st == b'EDID':
                edid = cp1252(sd)
            elif st == b'RNAM':
                rnam = text(sd)
            elif st == b'FULL':
                full = text(sd)
        key = (definer(fid, masters, selfname), fid & 0xFFFFFF)
        for kind, line in (('RNAM', rnam), ('FULL', full)):
            if line is not None:
                yield (key, kind), line, edid, fid

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
                    t, fid, data, nxt = espdial.record_data(buf, ioff)
                    if t == b'INFO':
                        for x in emit(t, fid, data):
                            yield x
                    ioff = nxt
            off += gs
            continue
        t, fid, data, nxt = espdial.record_data(buf, off)
        if t == b'DIAL':
            for x in emit(t, fid, data):
                yield x
        off = nxt


def build():
    pp = vfs.plugin_paths()
    win = {}
    for plug in load_order():                      # earliest -> latest, later wins
        ent = pp.get(plug.lower())
        if not ent:
            continue
        try:
            for key, line, edid, fid in scan(ent[0], plug):
                win[key] = (plug, line, edid, fid)
        except Exception as e:
            sys.stderr.write('skip %s: %r\n' % (plug, e))
    return win


if __name__ == '__main__':
    w = build()
    pickle.dump(w, open('winners.pkl', 'wb'))
    sys.stderr.write('dialogue strings resolved: %d\n' % len(w))
