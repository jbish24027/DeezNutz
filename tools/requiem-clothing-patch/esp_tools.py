"""Minimal Skyrim SE plugin reader + override-patch writer.

Reader: flattens every record (any group depth), decompresses zlib bodies,
resolves FormID master indices against the file's own master table.
Writer: emits an override-only patch by copying record bodies verbatim and
rewriting only the subrecords we hand it. Master list rule (see the
'bulk-esp-by-verbatim-record-copy' memory): declare the source's masters in
the source's own order, then the source plugin itself, then extras (Requiem.esp)
- so every FormID index inside a copied body still resolves without a remap.
"""
import struct, zlib, os

COMPRESSED = 0x00040000
ESL = 0x00000200


def iter_subrecords(body):
    o = 0
    big = None
    while o + 6 <= len(body):
        sig = body[o:o + 4]
        size = struct.unpack_from('<H', body, o + 4)[0]
        if sig == b'XXXX':
            big = struct.unpack_from('<I', body, o + 6)[0]
            o += 6 + size
            continue
        if big is not None:
            size = big
            big = None
        yield sig, body[o + 6:o + 6 + size]
        o += 6 + size


def build_subrecords(subs):
    out = bytearray()
    for sig, data in subs:
        if len(data) > 0xFFFF:
            out += b'XXXX' + struct.pack('<H', 4) + struct.pack('<I', len(data))
            out += sig + struct.pack('<H', 0) + data
        else:
            out += sig + struct.pack('<H', len(data)) + data
    return bytes(out)


def zstr(b):
    return b.split(b'\x00')[0].decode('cp1252', 'replace')


class Record:
    __slots__ = ('sig', 'flags', 'formid', 'tail', 'body', 'subs')

    def __init__(self, sig, flags, formid, tail, body):
        self.sig = sig; self.flags = flags; self.formid = formid; self.tail = tail
        self.body = body
        self.subs = list(iter_subrecords(body))

    def sub(self, sig):
        for s, d in self.subs:
            if s == sig:
                return d
        return None

    def subs_all(self, sig):
        return [d for s, d in self.subs if s == sig]

    @property
    def edid(self):
        d = self.sub(b'EDID')
        return zstr(d) if d else ''

    @property
    def full(self):
        d = self.sub(b'FULL')
        return zstr(d) if d else ''


class Plugin:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.data = open(path, 'rb').read()
        self.masters = []
        self.records = []
        self.tes4 = None
        self._walk(0, len(self.data), True)

    def _walk(self, off, end, top):
        d = self.data
        while off < end:
            sig = d[off:off + 4]
            if len(sig) < 4:
                return
            size = struct.unpack_from('<I', d, off + 4)[0]
            if sig == b'GRUP':
                self._walk(off + 24, off + size, False)
                off += size
                continue
            flags = struct.unpack_from('<I', d, off + 8)[0]
            formid = struct.unpack_from('<I', d, off + 12)[0]
            tail = d[off + 16:off + 24]
            body = d[off + 24:off + 24 + size]
            if flags & COMPRESSED:
                body = zlib.decompress(body[4:])
            rec = Record(sig, flags, formid, tail, body)
            if sig == b'TES4':
                self.tes4 = rec
                for s, sd in rec.subs:
                    if s == b'MAST':
                        self.masters.append(zstr(sd))
            else:
                self.records.append(rec)
            off += 24 + size

    def of(self, sig):
        return [r for r in self.records if r.sig == sig]

    def master_name(self, formid):
        idx = formid >> 24
        return self.masters[idx] if idx < len(self.masters) else self.name

    def fmt(self, formid):
        return '%06X:%s' % (formid & 0xFFFFFF, self.master_name(formid))

    def by_formid(self):
        return {r.formid: r for r in self.records}


# ------------------------------------------------------------------ decoders
ARMOR_TYPE = {0: 'LightArmor', 1: 'HeavyArmor', 2: 'Clothing'}


def slots_of(mask):
    return [30 + i for i in range(32) if mask & (1 << i)]


def parse_armo(rec, pl):
    out = dict(formid=pl.fmt(rec.formid), edid=rec.edid, name=rec.full, flags=rec.flags)
    bod2 = rec.sub(b'BOD2'); bodt = rec.sub(b'BODT')
    if bod2 is not None:
        m, at = struct.unpack_from('<II', bod2, 0)
    elif bodt is not None:
        m = struct.unpack_from('<I', bodt, 0)[0]
        at = struct.unpack_from('<I', bodt, 8)[0] if len(bodt) >= 12 else 0
    else:
        m, at = 0, 0
    out['slots'] = slots_of(m); out['armor_type'] = ARMOR_TYPE.get(at, at)
    data = rec.sub(b'DATA')
    out['value'], out['weight'] = struct.unpack_from('<If', data, 0) if data else (None, None)
    dnam = rec.sub(b'DNAM')
    out['ar'] = struct.unpack_from('<I', dnam, 0)[0] / 100.0 if dnam else None
    kwda = rec.sub(b'KWDA')
    out['keywords'] = [pl.fmt(f) for f in struct.unpack_from('<%dI' % (len(kwda) // 4), kwda, 0)] if kwda else []
    out['armature'] = [pl.fmt(struct.unpack_from('<I', d, 0)[0]) for d in rec.subs_all(b'MODL')]
    eitm = rec.sub(b'EITM'); out['enchant'] = pl.fmt(struct.unpack_from('<I', eitm, 0)[0]) if eitm else None
    tnam = rec.sub(b'TNAM'); out['template'] = pl.fmt(struct.unpack_from('<I', tnam, 0)[0]) if tnam else None
    return out


CTDA_FUNC = {47: 'GetItemCount', 72: 'GetIsID', 448: 'HasPerk', 560: 'HasKeyword', 67: 'GetLevel',
             99: 'GetIsRace', 71: 'GetInFaction', 176: 'GetPCIsSex', 56: 'GetQuestCompleted', 58: 'GetStage',
             14: 'GetActorValue', 27: 'GetVMQuestVariable', 566: 'GetGlobalValue'}


def parse_ctda(d):
    typ = d[0]
    comp = struct.unpack_from('<f', d, 4)[0]
    func = struct.unpack_from('<H', d, 8)[0]
    p1, p2, run_on, ref = struct.unpack_from('<IIII', d, 12)
    return dict(op=typ >> 5, or_=bool(typ & 1), use_global=bool(typ & 4), comp=comp,
                func=CTDA_FUNC.get(func, 'fn%d' % func), p1=p1, p2=p2, run_on=run_on, ref=ref)


def parse_cobj(rec, pl):
    out = dict(formid=pl.fmt(rec.formid), edid=rec.edid)
    items = []
    for d in rec.subs_all(b'CNTO'):
        f, c = struct.unpack_from('<II', d, 0)
        items.append((pl.fmt(f), c))
    out['items'] = items
    conds = []
    for d in rec.subs_all(b'CTDA'):
        c = parse_ctda(d)
        c['p1_fmt'] = pl.fmt(c['p1']) if c['func'] in ('HasPerk', 'GetItemCount', 'HasKeyword', 'GetIsID', 'GetGlobalValue') else c['p1']
        conds.append(c)
    out['conditions'] = conds
    cnam = rec.sub(b'CNAM'); out['created'] = pl.fmt(struct.unpack_from('<I', cnam, 0)[0]) if cnam else None
    bnam = rec.sub(b'BNAM'); out['workbench'] = pl.fmt(struct.unpack_from('<I', bnam, 0)[0]) if bnam else None
    nam1 = rec.sub(b'NAM1'); out['count'] = struct.unpack_from('<H', nam1, 0)[0] if nam1 else None
    return out


def parse_book(rec, pl):
    out = dict(formid=pl.fmt(rec.formid), edid=rec.edid, name=rec.full)
    data = rec.sub(b'DATA')
    if data:
        flags, typ = struct.unpack_from('<BB', data, 0)
        out['book_flags'] = flags; out['book_type'] = typ
        out['teaches'] = struct.unpack_from('<I', data, 4)[0]
        out['value'], out['weight'] = struct.unpack_from('<If', data, 8)
    kwda = rec.sub(b'KWDA')
    out['keywords'] = [pl.fmt(f) for f in struct.unpack_from('<%dI' % (len(kwda) // 4), kwda, 0)] if kwda else []
    return out


# ------------------------------------------------------------------ writer
def rewrite_subs(subs, replace=None, keywords=None, insert_before=b'DESC'):
    """Return a new subrecord list. replace: {sig: new_data} for single subrecords.
    keywords: list of u32 FormIDs -> KSIZ/KWDA rewritten in place (or inserted)."""
    replace = replace or {}
    out = []
    kw_done = False
    kw_bytes = None
    if keywords is not None:
        kw_bytes = struct.pack('<%dI' % len(keywords), *keywords)
    for sig, d in subs:
        if keywords is not None and sig in (b'KSIZ', b'KWDA'):
            if not kw_done:
                out.append((b'KSIZ', struct.pack('<I', len(keywords))))
                out.append((b'KWDA', kw_bytes))
                kw_done = True
            continue
        if keywords is not None and not kw_done and sig == insert_before:
            out.append((b'KSIZ', struct.pack('<I', len(keywords))))
            out.append((b'KWDA', kw_bytes))
            kw_done = True
        if sig in replace:
            out.append((sig, replace[sig]))
        else:
            out.append((sig, d))
    if keywords is not None and not kw_done:
        out.append((b'KSIZ', struct.pack('<I', len(keywords))))
        out.append((b'KWDA', kw_bytes))
    return out


def write_patch(path, masters, records, author='Authoria', description='', esl=True, nextid=0x800):
    """records: list of (sig, flags, formid, tail, body) in the patch's FormID frame."""
    groups = {}
    order = []
    for sig, flags, formid, tail, body in records:
        if sig not in groups:
            groups[sig] = []; order.append(sig)
        hdr = sig + struct.pack('<III', len(body), flags & ~COMPRESSED, formid) + tail
        groups[sig].append(hdr + body)
    total = sum(len(v) for v in groups.values()) + len(groups)
    subs = [(b'HEDR', struct.pack('<fII', 1.7, total, nextid)),
            (b'CNAM', author.encode('cp1252') + b'\x00'),
            (b'SNAM', description.encode('cp1252') + b'\x00')]
    for m in masters:
        subs.append((b'MAST', m.encode('cp1252') + b'\x00'))
        subs.append((b'DATA', struct.pack('<Q', 0)))
    tes4_body = build_subrecords(subs)
    out = bytearray()
    out += b'TES4' + struct.pack('<III', len(tes4_body), ESL if esl else 0, 0)
    out += struct.pack('<HHHH', 0, 0, 44, 0)
    out += tes4_body
    for sig in order:
        recs = groups[sig]
        size = 24 + sum(len(r) for r in recs)
        out += b'GRUP' + struct.pack('<I', size) + sig + struct.pack('<iHHI', 0, 0, 0, 0)
        for r in recs:
            out += r
    with open(path, 'wb') as f:
        f.write(bytes(out))
    return len(out)
