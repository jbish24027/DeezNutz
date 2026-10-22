"""
Local TES5 plugin parser: build ARMO -> ARMA -> mesh path maps without tool calls.

Why local: the armour->addon->mesh chain needs a list field expanded per record,
which is thousands of MCP calls. The chain lives in the defining plugin and is
not something the Reqtificator rewrites, so parsing the file is safe here.

EditorIDs for the actual KID lines still come from houseCARL (winner-aware),
because Requiem/Reqtificator DO rename those. This module is only for meshes.
"""

import struct
import zlib
import os

COMPRESSED = 0x00040000


def _subrecords(data):
    """Yield (type, payload) from a record's data block, honouring XXXX."""
    i = 0
    override = None
    n = len(data)
    while i + 6 <= n:
        typ = data[i:i + 4]
        size = struct.unpack_from('<H', data, i + 4)[0]
        i += 6
        if typ == b'XXXX':
            override = struct.unpack_from('<I', data, i)[0]
            i += size
            continue
        if override is not None:
            size = override
            override = None
        yield typ, data[i:i + size]
        i += size


def _zstr(b):
    return b.split(b'\x00', 1)[0].decode('cp1252', 'replace')


def iter_records(path, wanted=(b'ARMO', b'ARMA')):
    """Yield (sig, formid, {subrec_type: [payloads]}) for records of interest."""
    with open(path, 'rb') as fh:
        buf = fh.read()
    n = len(buf)

    # header record
    hdr_size = struct.unpack_from('<I', buf, 4)[0]
    i = 24 + hdr_size

    while i + 24 <= n:
        sig = buf[i:i + 4]
        if sig == b'GRUP':
            # group header is 24 bytes and groupSize includes it; descend
            i += 24
            continue
        size, flags = struct.unpack_from('<II', buf, i + 4)
        formid = struct.unpack_from('<I', buf, i + 12)[0]
        body = buf[i + 24:i + 24 + size]
        if sig in wanted:
            if flags & COMPRESSED:
                try:
                    body = zlib.decompress(body[4:])
                except Exception:
                    body = b''
            subs = {}
            for t, p in _subrecords(body):
                subs.setdefault(t, []).append(p)
            yield sig, formid, subs
        i += 24 + size


def masters(path):
    with open(path, 'rb') as fh:
        buf = fh.read(65536)
    hdr_size = struct.unpack_from('<I', buf, 4)[0]
    out, i, end = [], 24, 24 + hdr_size
    while i < end:
        t = buf[i:i + 4]
        sz = struct.unpack_from('<H', buf, i + 4)[0]
        if t == b'MAST':
            out.append(_zstr(buf[i + 6:i + 6 + sz]))
        i += 6 + sz
    return out


def _alt_textures(payload):
    """
    Decode an MO2S/MO4S (Alternate Textures) subrecord.
    uint32 count, then per entry: uint32 nameLen, char[nameLen] shape name,
    uint32 TXST formid, uint32 shape index.
    """
    out = []
    if len(payload) < 4:
        return out
    n = struct.unpack_from('<I', payload, 0)[0]
    i = 4
    for _ in range(n):
        if i + 4 > len(payload):
            break
        ln = struct.unpack_from('<I', payload, i)[0]
        i += 4
        if i + ln + 8 > len(payload):
            break
        shape = payload[i:i + ln].decode('cp1252', 'replace')
        i += ln
        txst, idx = struct.unpack_from('<II', payload, i)
        i += 8
        out.append((shape, txst, idx))
    return out


SKIN_HINT = ('femalebody', 'malebody', 'femalehands', 'malehands',
             'femalehead', 'malehead', 'bodyfemale', 'bodymale',
             '\\skin\\', 'skinnaked', 'femalefeet', 'malefeet',
             'blankdetailmap', 'default_n')


def looks_like_skin(tex):
    t = tex.lower()
    return any(h in t for h in SKIN_HINT)


def build_map(plugin_path):
    """
    Returns:
      armo: {local_formid: {"edid":.., "name":.., "slots":int, "atype":int,
                            "arma":[local_formid,...], "male_model":str, "female_model":str}}
      arma: {local_formid: {"edid":.., "models":{b'MOD2':path, b'MOD3':path, ...}}}
    Local formid = the low 24 bits, so it is master-independent.
    """
    armo, arma, txst = {}, {}, {}
    for sig, fid, subs in iter_records(plugin_path, wanted=(b'ARMO', b'ARMA', b'TXST')):
        if sig == b'TXST':
            # TX00 is the diffuse slot
            if b'TX00' in subs:
                txst[fid & 0xFFFFFF] = _zstr(subs[b'TX00'][0])
            continue
        local = fid & 0xFFFFFF
        edid = _zstr(subs[b'EDID'][0]) if b'EDID' in subs else ''
        if sig == b'ARMO':
            slots = atype = 0
            if b'BOD2' in subs and len(subs[b'BOD2'][0]) >= 8:
                slots, atype = struct.unpack_from('<II', subs[b'BOD2'][0], 0)
            elif b'BODT' in subs and len(subs[b'BODT'][0]) >= 12:
                slots = struct.unpack_from('<I', subs[b'BODT'][0], 0)[0]
                atype = struct.unpack_from('<I', subs[b'BODT'][0], 8)[0]
            name = ''
            if b'FULL' in subs:
                raw = subs[b'FULL'][0]
                if len(raw) != 4 or b'\x00' in raw:
                    name = _zstr(raw)
            armo[local] = {
                'edid': edid,
                'name': name,
                'slots': slots,
                'atype': atype,
                'arma': [struct.unpack_from('<I', p, 0)[0] & 0xFFFFFF
                         for p in subs.get(b'MODL', []) if len(p) == 4],
                'male_model': _zstr(subs[b'MOD2'][0]) if b'MOD2' in subs else '',
                'female_model': _zstr(subs[b'MOD4'][0]) if b'MOD4' in subs else '',
                'alt': ([x for p_ in subs.get(b'MO2S', []) for x in _alt_textures(p_)] +
                        [x for p_ in subs.get(b'MO4S', []) for x in _alt_textures(p_)]),
            }
        else:  # ARMA
            models = {}
            for t in (b'MOD2', b'MOD3', b'MOD4', b'MOD5'):
                if t in subs:
                    models[t.decode()] = _zstr(subs[t][0])
            arma[local] = {'edid': edid, 'models': models,
                           'txst': [struct.unpack_from('<I', p, 0)[0]
                                    for p in subs.get(b'NAM0', []) + subs.get(b'NAM1', [])
                                    if len(p) == 4]}
    return armo, arma, txst


def diffuse_for(armo_rec, txst):
    """
    The garment diffuse this record actually shows, if the record carries a
    texture-set swap. Per-item colourways live here, not in the mesh -- a mod
    can ship one nif and 40 TXST recolours.
    Returns None when the record has no swap and the mesh must be read.
    """
    best = None
    for _shape, fid, _idx in armo_rec.get('alt', []):
        path = txst.get(fid & 0xFFFFFF)
        if not path:
            continue
        if looks_like_skin(path):
            continue
        if not path.lower().startswith('textures'):
            path = 'textures' + chr(92) + path.lstrip(chr(92))
        best = path
        break
    return best


def meshes_for(armo_rec, arma):
    """All distinct mesh paths an armour resolves to, female preferred first."""
    out = []
    for a in armo_rec.get('arma', []):
        m = arma.get(a, {}).get('models', {})
        # MOD2 male world, MOD3 female world (SSE ARMA ordering)
        for key in ('MOD3', 'MOD2'):
            if m.get(key):
                out.append(m[key])
    for k in ('female_model', 'male_model'):
        if armo_rec.get(k):
            out.append(armo_rec[k])
    seen, uniq = set(), []
    for p in out:
        pl = p.lower().replace('/', '\\')
        if pl not in seen:
            seen.add(pl)
            uniq.append(p)
    return uniq


NIF_DDS = None


def textures_in_nif(path):
    """Extract embedded texture paths from a .nif by scanning for '...dds'."""
    import re
    global NIF_DDS
    if NIF_DDS is None:
        NIF_DDS = re.compile(rb'\.[Dd][Dd][Ss]')
    try:
        with open(path, 'rb') as fh:
            d = fh.read()
    except OSError:
        return []
    out = []
    for m in NIF_DDS.finditer(d):
        e = m.end()
        s = e
        while s > 0 and 32 <= d[s - 1] < 127:
            s -= 1
        t = d[s:e].decode('cp1252', 'replace')
        if t.lower().startswith('textures'):
            out.append(t.replace('/', '\\'))
    seen, uniq = set(), []
    for t in out:
        if t.lower() not in seen:
            seen.add(t.lower())
            uniq.append(t)
    return uniq


def is_diffuse(tex):
    t = tex.lower()
    return not any(t.endswith(x) for x in
                   ('_n.dds', '_m.dds', '_s.dds', '_sk.dds', '_e.dds', '_g.dds',
                    '_em.dds', '_msn.dds', '_p.dds', '_b.dds'))
