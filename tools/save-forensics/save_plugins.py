"""Dump the engine's plugin order (full + light arrays) from a Skyrim SE .ess save.
Usage: python save_plugins.py <save.ess> [out.json]"""
import os, struct, sys, json, zlib
try:
    import lz4.block
except ImportError:
    lz4 = None

def wstr(b, o):
    n = struct.unpack_from('<H', b, o)[0]
    return b[o + 2:o + 2 + n].decode('latin1'), o + 2 + n

def parse(path):
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
    h += 2 + 4 + 4 + 8                       # sex, curExp, lvlUpExp, filetime
    shotw, shoth = struct.unpack_from('<II', b, h); h += 8
    comp = struct.unpack_from('<H', b, h)[0] if version >= 12 else 0
    o += hsz
    o += shotw * shoth * (4 if version >= 12 else 3)   # screenshot
    if comp:
        unc, cl = struct.unpack_from('<II', b, o); o += 8
        raw = b[o:o + cl]
        data = lz4.block.decompress(raw, uncompressed_size=unc) if comp == 2 else zlib.decompress(raw)
    else:
        data = b[o:]
    p = 0
    formver = data[p]; p += 1
    p += 4                                    # pluginInfoSize
    cnt = data[p]; p += 1
    full = []
    for _ in range(cnt):
        s, p = wstr(data, p); full.append(s)
    light = []
    if formver >= 78:
        lcnt = struct.unpack_from('<H', data, p)[0]; p += 2
        for _ in range(lcnt):
            s, p = wstr(data, p); light.append(s)
    return {'file': os.path.basename(path), 'version': version, 'saveNumber': savenum, 'player': name, 'level': level,
            'location': loc, 'gameDate': gdate, 'formVersion': formver, 'full': full, 'light': light}

if __name__ == '__main__':
    r = parse(sys.argv[1])
    print(f"{r['file']}: v{r['version']} form {r['formVersion']} | {r['player']} L{r['level']} @ {r['location']} {r['gameDate']} | full {len(r['full'])} light {len(r['light'])}")
    if len(sys.argv) > 2:
        json.dump(r, open(sys.argv[2], 'w'), indent=0)
