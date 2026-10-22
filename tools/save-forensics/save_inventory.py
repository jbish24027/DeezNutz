# usage: python save_inventory.py <save.ess> <out.json>  -> favorited (ExtraHotkey) + worn items with plugin + local FormID
"""Dump the player's inventory (with worn / favorite / enchant / temper extras) from a Skyrim SE .ess.

Layout (Resaver ChangeFormACHR): INITIAL | [HAVOK] | int32 + 4 bytes | [FORM_FLAGS] | [BASE] | [SCALE] |
[EXTRADATA list] | [INVENTORY] | [ANIMATIONS].  Inventory item = RefID + int32 count + vsval nLists +
nLists * (vsval nEntries + entries).  Entry = type byte + payload (Resaver ChangeFormExtraDataData table).
"""
import struct, sys, json
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import R, load, parse_body
from changeforms import parse_change_forms, read_formid_array, decompress

def resolve(rtype, rval, formids):
    # UESP: type 0 = index into formIDArray using value-1 (0 means null)
    if rtype == 0:
        if rval == 0: return 0
        return formids[rval-1] if rval-1 < len(formids) else None
    if rtype == 1: return rval
    if rtype == 2: return 0xFF000000 | rval
    return None


class Bad(Exception):
    pass

def refid(r):
    t, v = r.refid()
    return (t, v)

def read_entry(r, formids, depth=0):
    """Parse one extra-data entry. Returns (type, dict)."""
    t = r.u8()
    d = {}
    def rf():
        return resolve(*refid(r), formids)
    if t == 0:
        d['null'] = True
    elif t == 22: d['worn'] = True
    elif t == 23: d['wornLeft'] = True
    elif t == 24: rf(); r.f32(); r.f32(); r.f32(); r.f32()
    elif t == 25: rf(); rf(); r.u32(); r.p += 3
    elif t == 26: rf()
    elif t == 27:
        n = r.vsval(); r.p += 4 * n
    elif t == 28: d['refHandle'] = rf()
    elif t == 29: pass
    elif t == 30: r.u32()
    elif t == 31: r.u8()
    elif t == 32: pass
    elif t == 33: d['owner'] = rf()
    elif t == 34: rf()
    elif t == 35: rf()
    elif t == 36: d['count16'] = r.u16()
    elif t == 37: d['health'] = r.f32()
    elif t == 39: r.u32()
    elif t == 40: d['charge'] = r.f32()
    elif t == 42: r.p += 2; rf(); r.u32(); r.u32()
    elif t == 43: r.p += 24; r.u8(); rf()
    elif t == 44: r.u8()
    elif t == 46: d['leveledItem'] = (r.u32(), r.u8())
    elif t == 47: d['scale'] = r.f32()
    elif t == 52:
        n = r.vsval(); r.p += 8 * n
    elif t == 53: pass
    elif t == 56: rf()
    elif t == 61: d['cannotWear'] = True
    elif t == 62: d['poison'] = (rf(), r.u32())
    elif t == 68:
        n = r.vsval(); r.p += 4 * n
    elif t == 69: rf()
    elif t == 72: rf()
    elif t == 73: d['hotkey'] = struct.unpack('<b', bytes([r.u8()]))[0]
    elif t == 77: r.u8()
    elif t == 79: r.p += 2
    elif t == 83: r.u32()
    elif t == 84: r.u8()
    elif t == 85: r.f32()
    elif t == 88: rf(); r.u32()
    elif t == 89: r.f32()
    elif t == 91:
        n = r.vsval()
        for _ in range(n):
            rf(); r.u8()
        rf(); r.u8()
    elif t == 93: r.u32()
    elif t == 101: rf()
    elif t == 102: rf(); rf()
    elif t == 104: rf()
    elif t == 106: d['ammo'] = (rf(), r.u32())
    elif t == 111:
        n = r.vsval()
        for _ in range(n):
            rf(); r.u32(); r.u32()
    elif t == 112: d['encZone'] = rf()
    elif t == 120:
        n = r.vsval()
        for _ in range(n):
            rf(); r.u32(); r.u8()
    elif t == 133: rf()
    elif t == 135: rf(); rf(); rf(); rf()
    elif t == 136:
        n = r.vsval()
        al = []
        for _ in range(n):
            al.append((rf(), r.u32()))
        d['aliases'] = al
    elif t == 140:
        n = r.vsval()
        for _ in range(n):
            rf()
    elif t == 142: d['outfitItem'] = rf()
    elif t == 146: rf()
    elif t == 149: d['fromAlias'] = (rf(), r.u32())
    elif t == 150: d['shouldWear'] = r.u8()
    elif t == 152:
        n = r.vsval()
        for _ in range(n):
            ref = refid(r)
            if not (ref[0] == 0 and ref[1] == 0):
                u = r.u16()
                if u != 0xFFFF:
                    r.u32(); r.p += 32
        r.u16(); r.u16()
    elif t == 153:
        r1 = rf(); r2 = rf(); u = r.i32()
        if (r1 in (0, None)) and (r2 in (0, None)) and u == -2:
            d['name'] = r.wstr()
        else:
            d['textDisplay'] = (r1, r2, u)
    elif t == 155: d['ench'] = rf(); d['enchCharge'] = r.u16()
    elif t == 156: d['soul'] = r.u8()
    elif t == 157: rf()
    elif t == 159: d['uniqueId'] = (r.u32(), r.u16())
    elif t == 160: d['flags'] = r.u32()
    elif t == 161: r.p += 4 * 18 + 16
    elif t == 164: rf()
    elif t == 169: r.u32(); rf(); rf(); r.u8()
    elif t == 176: r.f32(); r.f32()
    else:
        raise Bad('unknown extra type %d at %d' % (t, r.p - 1))
    return t, d

def read_list(r, formids):
    n = r.vsval()
    if n > 2000:
        raise Bad('silly list count %d at %d' % (n, r.p))
    out = []
    for _ in range(n):
        out.append(read_entry(r, formids))
    return out

def parse_player(d, flags, formids):
    r = R(d)
    info = {}
    # initial (type 4 for player: MOVE set, not promoted/cell-changed)
    if flags & (0x02000000 | 0x8):
        r.p += 27 + 3 + 4
    elif flags & 0x6:
        r.p += 27
    if flags & 0x4:
        n = r.vsval(); r.p += n
    r.u32(); r.p += 4
    if flags & 0x1:
        r.u32(); r.u16()
    if flags & 0x80:
        refid(r)
    if flags & 0x10:
        r.f32()
    extra_flags = (0x40 | 0x02000000 | 0x800 | 0x1000 | 0x20000 | 0x04000000 | 0x20000000 | 0x40000000 | 0x80000000 | 0x40000)
    info['extraStart'] = r.p
    if flags & extra_flags:
        info['actorExtra'] = read_list(r, formids)
    info['invStart'] = r.p
    items = []
    if flags & (0x20 | 0x08000000):
        n = r.vsval()
        info['invCount'] = n
        for i in range(n):
            fid = resolve(*refid(r), formids)
            cnt = r.i32()
            nl = r.vsval()
            lists = []
            for _ in range(nl):
                lists.append(read_list(r, formids))
            items.append(dict(fid=fid, count=cnt, lists=lists, off=r.p))
    info['invEnd'] = r.p
    if flags & 0x10000000:
        n = r.vsval(); info['animLen'] = n; r.p += n
    info['end'] = r.p
    info['total'] = len(d)
    return info, items

def plugin_of(fid, plugins, light):
    if fid is None:
        return '?'
    hi = fid >> 24
    if hi == 0xFF:
        return 'CREATED'
    if hi == 0xFE:
        li = (fid >> 12) & 0xFFF
        return light[li] if li < len(light) else 'light#%d' % li
    return plugins[hi] if hi < len(plugins) else 'full#%d' % hi

def local_of(fid):
    if fid is None:
        return 0
    if (fid >> 24) == 0xFE:
        return fid & 0xFFF
    return fid & 0xFFFFFF

def main():
    path = sys.argv[1]
    hdr, body = load(path)
    fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
    formids = read_formid_array(body, flt['formIDArrayCountOffset'])
    forms, end = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], True)
    player = None
    for cf in forms:
        if resolve(cf['rtype'], cf['rval'], formids) == 0x14 and cf['type'] == 1:
            player = cf
    d = decompress(player)
    print('player blob %d bytes flags 0x%08X' % (len(d), player['flags']))
    try:
        info, items = parse_player(d, player['flags'], formids)
    except Bad as e:
        print('PARSE FAILED:', e)
        raise
    print({k: v for k, v in info.items() if k != 'actorExtra'})
    print('actor extra entries:', [t for t, _ in info.get('actorExtra', [])])
    out = []
    for it in items:
        fid = it['fid']
        rec = dict(formid='%08X' % (fid or 0), plugin=plugin_of(fid, plugins, light), local='%06X' % local_of(fid),
                   count=it['count'], lists=[])
        for lst in it['lists']:
            summ = {}
            for t, dd in lst:
                summ[str(t)] = dd if dd else True
            rec['lists'].append(summ)
        out.append(rec)
    json.dump(dict(player=hdr['playerName'], save=path, items=out), open(sys.argv[2], 'w'), indent=1)
    print('items:', len(out))
    # quick views
    fav = [x for x in out if any('hotkey' in v for l in x['lists'] for v in l.values() if isinstance(v, dict))]
    worn = [x for x in out if any((k in ('22', '23')) for l in x['lists'] for k in l)]
    print('\n--- FAVORITED (hotkey extra present) ---')
    for x in fav:
        print(' ', x['plugin'], x['local'], 'x%d' % x['count'], x['lists'])
    print('\n--- WORN ---')
    for x in worn:
        print(' ', x['plugin'], x['local'], 'x%d' % x['count'], x['lists'])

if __name__ == '__main__':
    main()
