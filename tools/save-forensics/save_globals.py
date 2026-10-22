"""Read GlobalVariable values out of a Skyrim SE .ess save (Global Variables table, globalData type 3).

Usage:
  python save_globals.py <save.ess>                          -> dumps every global (runtime formID = value)
  python save_globals.py <save.ess> "<Plugin.esp>" 0x853 ... -> resolves the plugin's runtime index inside THIS
                                                                save (full or light list) and prints those globals
The save's own plugin arrays are used, so a light-index shift between sessions cannot mislead the lookup.
"""
import os, struct, sys, zlib
try:
    import lz4.block
except ImportError:
    lz4 = None


def wstr(b, o):
    n = struct.unpack_from('<H', b, o)[0]
    return b[o + 2:o + 2 + n].decode('latin1'), o + 2 + n


def vsval(b, o):
    t = b[o] & 3
    if t == 0:
        return b[o] >> 2, o + 1
    if t == 1:
        return struct.unpack_from('<H', b, o)[0] >> 2, o + 2
    return struct.unpack_from('<I', b, o)[0] >> 2, o + 4


def load(path):
    b = open(path, 'rb').read()
    assert b[:13] == b'TESV_SAVEGAME', 'not a Skyrim SE save'
    o = 13
    hsz = struct.unpack_from('<I', b, o)[0]; o += 4
    h = o
    version, savenum = struct.unpack_from('<II', b, h); h += 8
    name, h = wstr(b, h)
    level = struct.unpack_from('<I', b, h)[0]; h += 4
    loc, h = wstr(b, h)
    gdate, h = wstr(b, h)
    race, h = wstr(b, h)
    h += 2 + 4 + 4 + 8
    shotw, shoth = struct.unpack_from('<II', b, h); h += 8
    comp = struct.unpack_from('<H', b, h)[0] if version >= 12 else 0
    o += hsz
    o += shotw * shoth * (4 if version >= 12 else 3)
    base = o            # offsets in the file location table count from the start of a virtual
    if comp:            # uncompressed file: everything before this point plus the decompressed body
        unc, cl = struct.unpack_from('<II', b, o); o += 8
        raw = b[o:o + cl]
        data = lz4.block.decompress(raw, uncompressed_size=unc) if comp == 2 else zlib.decompress(raw)
    else:
        data = b[o:]
    p = 0
    formver = data[p]; p += 1
    p += 4
    cnt = data[p]; p += 1
    full = []
    for _ in range(cnt):
        s, p = wstr(data, p); full.append(s)
    light = []
    if formver >= 78:
        lcnt = struct.unpack_from('<H', data, p)[0]; p += 2
        for _ in range(lcnt):
            s, p = wstr(data, p); light.append(s)
    # file location table
    (fidArrOff, unk3Off, gd1Off, gd2Off, cfOff, gd3Off,
     gd1Cnt, gd2Cnt, gd3Cnt, cfCnt) = struct.unpack_from('<10I', data, p)
    # sanity: pick the base that makes the formID-array count and the first globalData type plausible
    cands = [base, base + 8, 0]
    for cb in cands:
        fo = fidArrOff - cb; go = gd1Off - cb
        if 0 <= fo < len(data) - 4 and 0 <= go < len(data) - 8:
            n = struct.unpack_from('<I', data, fo)[0]
            t = struct.unpack_from('<I', data, go)[0]
            if n < 5_000_000 and t <= 8:
                fidArrOff -= cb; gd1Off -= cb
                break
    else:
        raise ValueError('could not establish offset base for %s' % path)
    return dict(file=os.path.basename(path), player=name, level=level, location=loc, gameDate=gdate,
                data=data, full=full, light=light, fidArrOff=fidArrOff, gd1Off=gd1Off, gd1Cnt=gd1Cnt)


def formid_array(s):
    d = s['data']; o = s['fidArrOff']
    n = struct.unpack_from('<I', d, o)[0]
    return list(struct.unpack_from('<%dI' % n, d, o + 4))


def resolve_ref(raw3, fids):
    t = raw3[0] >> 6
    v = ((raw3[0] & 0x3F) << 16) | (raw3[1] << 8) | raw3[2]
    if t == 0:
        return 0 if v == 0 else fids[v - 1]
    if t == 1:
        return v
    if t == 2:
        return 0xFF000000 | v
    return None


def globals_table(s):
    d = s['data']; o = s['gd1Off']
    fids = formid_array(s)
    out = {}
    for _ in range(s['gd1Cnt']):
        typ, ln = struct.unpack_from('<II', d, o); o += 8
        body = d[o:o + ln]; o += ln
        if typ == 3:
            n, q = vsval(body, 0)
            for _ in range(n):
                fid = resolve_ref(body[q:q + 3], fids); q += 3
                val = struct.unpack_from('<f', body, q)[0]; q += 4
                out[fid] = val
    return out


def runtime_id(s, plugin, local):
    pl = plugin.lower()
    fulls = [x.lower() for x in s['full']]
    lights = [x.lower() for x in s['light']]
    if pl in fulls:
        return (fulls.index(pl) << 24) | (local & 0xFFFFFF)
    if pl in lights:
        return 0xFE000000 | (lights.index(pl) << 12) | (local & 0xFFF)
    return None


if __name__ == '__main__':
    s = load(sys.argv[1])
    g = globals_table(s)
    print(f"{s['file']}: {s['player']} L{s['level']} @ {s['location']} {s['gameDate']} | globals {len(g)} | light plugins {len(s['light'])}")
    if len(sys.argv) > 3:
        plugin = sys.argv[2]
        for hx in sys.argv[3:]:
            local = int(hx, 16)
            rid = runtime_id(s, plugin, local)
            print(f"  {plugin} {hx} -> runtime {rid:08X} = {g.get(rid, 'NOT IN TABLE')}" if rid is not None else f"  {plugin} not in this save")
    else:
        for k in sorted(g):
            print(f"  {k:08X} = {g[k]}")
