"""OES NG co-save reader / assignment remover.

Skyrim Outfit Equipment System NG stores its live state in the SKSE co-save
(.skse), NOT in overwrite\\SKSE\\Plugins\\OutfitEquipmentSystemNGData.json.
Editing the JSON is a silent no-op.

Layout
------
SKSE co-save:
    char   magic[4]          "SKSE"
    uint32 formatVersion
    uint32 skseVersion
    uint32 runtimeVersion
    uint32 numPlugins
  per plugin:
    uint32 signature         OES = 'tzOc'
    uint32 numChunks
    uint32 length            total bytes of this plugin's chunk data
    per chunk:
      uint32 type            'SOAA' (ArmorAddonOverrideService) | 'SCSO' (cache)
      uint32 version
      uint32 length
      byte   data[length]

SOAA payload is clean protobuf, no checksums:
    field 1  varint            enabled
    field 2  len-delim rep.    outfits
    field 3  len-delim rep.    actor assignments
    field 4  varint            playerInventoryManagementMode
    field 5  varint            npcInventoryManagementMode

Removing one assignment = drop its whole field-3 record (key byte + length
varint + body), then decrement BOTH the SOAA chunk length and the owning
plugin's length by the same amount. Nothing else changes.

Every file is re-walked to EOF and re-counted before anything is written.
"""
import os
import struct
import sys

OES_SIG = b'tzOc'
CHUNK_SOAA = b'SOAA'


# ---------------------------------------------------------------- protobuf

def read_varint(buf, pos):
    """Return (value, new_pos)."""
    val = 0
    shift = 0
    while True:
        if pos >= len(buf):
            raise ValueError('varint ran past end of buffer')
        b = buf[pos]
        pos += 1
        val |= (b & 0x7F) << shift
        if not (b & 0x80):
            return val, pos
        shift += 7
        if shift > 63:
            raise ValueError('varint too long')


def walk_protobuf(buf):
    """Yield (field_number, wire_type, record_start, body_start, body_end)."""
    pos = 0
    while pos < len(buf):
        rec_start = pos
        key, pos = read_varint(buf, pos)
        field = key >> 3
        wire = key & 0x07
        if wire == 0:
            _, pos = read_varint(buf, pos)
            yield field, wire, rec_start, rec_start, pos
        elif wire == 2:
            ln, pos = read_varint(buf, pos)
            body_start = pos
            pos += ln
            if pos > len(buf):
                raise ValueError('length-delimited field ran past end')
            yield field, wire, rec_start, body_start, pos
        elif wire == 5:
            pos += 4
            yield field, wire, rec_start, rec_start, pos
        elif wire == 1:
            pos += 8
            yield field, wire, rec_start, rec_start, pos
        else:
            raise ValueError('unsupported wire type %d at %d' % (wire, rec_start))


# ------------------------------------------------------------- co-save walk

class Chunk(object):
    def __init__(self, ctype, version, length, hdr_off, data_off):
        self.type = ctype
        self.version = version
        self.length = length
        self.hdr_off = hdr_off      # offset of the chunk's type dword
        self.data_off = data_off    # offset of the chunk payload


class Plugin(object):
    def __init__(self, sig, num_chunks, length, hdr_off, data_off):
        self.sig = sig
        self.num_chunks = num_chunks
        self.length = length
        self.hdr_off = hdr_off      # offset of the plugin's signature dword
        self.data_off = data_off    # offset of the first chunk header
        self.chunks = []


def walk_cosave(data):
    """Walk every plugin chunk. Raises unless the walk lands exactly on EOF."""
    if data[:4] != b'SKSE':
        raise ValueError('not an SKSE co-save (magic=%r)' % data[:4])
    pos = 4
    fmt_ver, skse_ver, rt_ver, num_plugins = struct.unpack_from('<4I', data, pos)
    pos += 16

    plugins = []
    for _ in range(num_plugins):
        hdr_off = pos
        sig = data[pos:pos + 4]
        num_chunks, length = struct.unpack_from('<2I', data, pos + 4)
        pos += 12
        pl = Plugin(sig, num_chunks, length, hdr_off, pos)
        end_of_plugin = pos + length
        for _ in range(num_chunks):
            c_hdr = pos
            ctype = data[pos:pos + 4]
            cver, clen = struct.unpack_from('<2I', data, pos + 4)
            pos += 12
            pl.chunks.append(Chunk(ctype, cver, clen, c_hdr, pos))
            pos += clen
        if pos != end_of_plugin:
            raise ValueError('plugin %r chunk walk ended at %d, expected %d'
                             % (sig, pos, end_of_plugin))
        plugins.append(pl)

    if pos != len(data):
        raise ValueError('walk ended at %d but file is %d bytes' % (pos, len(data)))

    return {'formatVersion': fmt_ver, 'skseVersion': skse_ver,
            'runtimeVersion': rt_ver, 'plugins': plugins}


def find_soaa(info):
    for pl in info['plugins']:
        if pl.sig != OES_SIG:
            continue
        for ch in pl.chunks:
            if ch.type == CHUNK_SOAA:
                return pl, ch
    return None, None


def summarize_soaa(data, chunk):
    """Return dict with outfit count, assignment records, and the mode fields."""
    body = data[chunk.data_off:chunk.data_off + chunk.length]
    outfits = []
    assignments = []
    modes = {}
    enabled = None
    for field, wire, rec_start, body_start, body_end in walk_protobuf(body):
        if field == 1 and wire == 0:
            enabled, _ = read_varint(body, body_start + 1)
        elif field == 2 and wire == 2:
            outfits.append((rec_start, body_end))
        elif field == 3 and wire == 2:
            assignments.append({
                'rec_start': rec_start,
                'body_start': body_start,
                'rec_end': body_end,
                'blob': body[body_start:body_end],
            })
        elif field in (4, 5) and wire == 0:
            v, _ = read_varint(body, body_start + 1)
            modes[field] = v
    return {'enabled': enabled, 'outfits': outfits,
            'assignments': assignments, 'modes': modes, 'body': body}


def assignment_label(blob):
    """Best-effort: the actor key string inside an assignment record."""
    try:
        for field, wire, rs, bs, be in walk_protobuf(blob):
            if field == 1 and wire == 2:
                return blob[bs:be].decode('utf-8', 'replace')
    except ValueError:
        pass
    # fall back: first printable ascii run that looks like a form key
    txt = blob.decode('latin-1')
    best = ''
    cur = ''
    for chpr in txt:
        if 32 <= ord(chpr) < 127:
            cur += chpr
        else:
            if len(cur) > len(best):
                best = cur
            cur = ''
    if len(cur) > len(best):
        best = cur
    return best


# ------------------------------------------------------------------ actions

def scan(path, verbose=True):
    data = open(path, 'rb').read()
    info = walk_cosave(data)
    pl, ch = find_soaa(info)
    if ch is None:
        if verbose:
            print('%-72s  no OES chunk' % os.path.basename(path))
        return None
    s = summarize_soaa(data, ch)
    if verbose:
        print('%s  (%d bytes)' % (os.path.basename(path), len(data)))
        print('   plugins=%d  SOAA len=%d  enabled=%s  modes=%s'
              % (len(info['plugins']), ch.length, s['enabled'], s['modes']))
        print('   outfits=%d  assignments=%d' % (len(s['outfits']), len(s['assignments'])))
        for a in s['assignments']:
            print('      %s   (%d bytes)'
                  % (assignment_label(a['blob']), a['rec_end'] - a['rec_start']))
    return {'data': data, 'info': info, 'plugin': pl, 'chunk': ch, 'soaa': s}


def remove_assignment(path, needle, dry_run=True):
    """Drop the single field-3 assignment whose record contains `needle`."""
    st = scan(path, verbose=False)
    if st is None:
        return 'no-oes-chunk'
    data, info, pl, ch, s = (st['data'], st['info'], st['plugin'],
                             st['chunk'], st['soaa'])

    hits = [a for a in s['assignments'] if needle in a['blob']]
    if not hits:
        return 'not-present'
    if len(hits) > 1:
        raise ValueError('%s: %d assignments match %r — refusing'
                         % (os.path.basename(path), len(hits), needle))
    a = hits[0]
    cut = a['rec_end'] - a['rec_start']

    # absolute file offsets of the record inside the SOAA payload
    abs_start = ch.data_off + a['rec_start']
    abs_end = ch.data_off + a['rec_end']

    new = bytearray(data)
    del new[abs_start:abs_end]
    # SOAA chunk length dword sits at chunk.hdr_off + 8
    struct.pack_into('<I', new, ch.hdr_off + 8, ch.length - cut)
    # plugin length dword sits at plugin.hdr_off + 8
    struct.pack_into('<I', new, pl.hdr_off + 8, pl.length - cut)
    new = bytes(new)

    # ---- verify the rewritten file before it touches disk ----
    info2 = walk_cosave(new)                 # raises unless it lands on EOF
    pl2, ch2 = find_soaa(info2)
    s2 = summarize_soaa(new, ch2)
    if len(s2['outfits']) != len(s['outfits']):
        raise ValueError('%s: outfit count changed %d -> %d'
                         % (path, len(s['outfits']), len(s2['outfits'])))
    if len(s2['assignments']) != len(s['assignments']) - 1:
        raise ValueError('%s: assignment count %d -> %d, expected %d'
                         % (path, len(s['assignments']), len(s2['assignments']),
                            len(s['assignments']) - 1))
    if s2['modes'] != s['modes'] or s2['enabled'] != s['enabled']:
        raise ValueError('%s: enabled/modes changed' % path)
    if any(needle in x['blob'] for x in s2['assignments']):
        raise ValueError('%s: target still present after cut' % path)
    if len(new) != len(data) - cut:
        raise ValueError('%s: size delta %d, expected %d'
                         % (path, len(data) - len(new), cut))

    if not dry_run:
        bak = path + '.bak-pre-oes-kaidan-20260823'
        if not os.path.exists(bak):
            with open(bak, 'wb') as fh:
                fh.write(data)
        with open(path, 'wb') as fh:
            fh.write(new)
    return 'removed:%d' % cut


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print('usage: oes_cosave.py scan   <saves-dir>')
        print('       oes_cosave.py remove <saves-dir> <needle> [--apply]')
        return 2
    cmd, folder = sys.argv[1], sys.argv[2]
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith('.skse'))

    if cmd == 'scan':
        for f in files:
            scan(os.path.join(folder, f))
            print()
        print('%d co-save(s)' % len(files))
        return 0

    if cmd == 'remove':
        needle = sys.argv[3].encode('utf-8')
        apply_it = '--apply' in sys.argv
        tally = {}
        for f in files:
            try:
                r = remove_assignment(os.path.join(folder, f), needle,
                                      dry_run=not apply_it)
            except Exception as exc:                      # noqa: BLE001
                r = 'ERROR: %s' % exc
            tally[r] = tally.get(r, 0) + 1
            print('%-76s %s' % (f, r))
        print()
        print('mode: %s' % ('APPLIED' if apply_it else 'DRY RUN'))
        for k in sorted(tally):
            print('  %-28s %d' % (k, tally[k]))
        return 0

    print('unknown command %r' % cmd)
    return 2


if __name__ == '__main__':
    sys.exit(main())
