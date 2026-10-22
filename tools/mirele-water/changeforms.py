"""Parse the ChangeForm table of a Skyrim SE .ess and decode reference moves.

Usage: python changeforms.py <save.ess>
"""
import struct
import sys
import zlib
from collections import Counter

sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import R, load, parse_body, global_data, player_location

# ChangeForm "type" low 6 bits -> save form type name (UESP table)
TYPE_NAMES = {
    0: 'REFR', 1: 'ACHR', 2: 'PMIS', 3: 'PGRE', 4: 'PBEA', 5: 'PFLA',
    6: 'CELL', 7: 'INFO', 8: 'QUST', 9: 'NPC_', 10: 'ACTI', 11: 'TACT',
    12: 'ARMO', 13: 'BOOK', 14: 'CONT', 15: 'DOOR', 16: 'INGR', 17: 'LIGH',
    18: 'MISC', 19: 'APPA', 20: 'STAT', 21: 'MSTT', 22: 'FURN', 23: 'WEAP',
    24: 'AMMO', 25: 'KEYM', 26: 'ALCH', 27: 'IDLM', 28: 'NOTE', 29: 'ECZN',
    30: 'CLAS', 31: 'FACT', 32: 'PACK', 33: 'NAVM', 34: 'WOOP', 35: 'MGEF',
    36: 'SMQN', 37: 'SCEN', 38: 'LCTN', 39: 'RELA', 40: 'PHZD', 41: 'PBAR',
    42: 'PCON', 43: 'FLST', 44: 'LVLN', 45: 'LVLI', 46: 'LVSP', 47: 'PARW',
    48: 'ENCH',
}

FLAG_NAMES = [
    (0x00000001, 'FORM_FLAGS'),
    (0x00000002, 'REFR_MOVE'),
    (0x00000004, 'REFR_HAVOK_MOVE'),
    (0x00000008, 'REFR_CELL_CHANGED'),
    (0x00000010, 'REFR_SCALE'),
    (0x00000020, 'REFR_INVENTORY'),
    (0x00000040, 'REFR_EXTRA_OWNERSHIP'),
    (0x00000080, 'REFR_BASEOBJECT'),
    (0x02000000, 'REFR_PROMOTED'),
    (0x04000000, 'REFR_EXTRA_ACTIVATING_CHILDREN'),
    (0x08000000, 'REFR_LEVELED_INVENTORY'),
    (0x10000000, 'REFR_ANIMATION'),
    (0x20000000, 'REFR_EXTRA_ENCOUNTER_ZONE'),
    (0x40000000, 'REFR_EXTRA_CREATED_ONLY'),
    (0x80000000, 'REFR_EXTRA_GAME_ONLY'),
]


def flagstr(f):
    out = [n for m, n in FLAG_NAMES if f & m]
    rest = f & ~sum(m for m, _ in FLAG_NAMES)
    if rest:
        out.append('0x%08X' % rest)
    return '|'.join(out) if out else '-'


def read_formid_array(body, off):
    r = R(body, off)
    n = r.u32()
    arr = struct.unpack_from('<%dI' % n, body, r.p)
    return list(arr)


def resolve(rtype, rval, formids):
    """Turn a (type,value) RefID into a real FormID, or None."""
    if rtype == 0:
        if 0 <= rval < len(formids):
            return formids[rval]
        return None
    if rtype == 1:
        return rval
    if rtype == 2:
        return 0xFF000000 | rval
    return None


def parse_change_forms(body, off, count, with_version=True):
    r = R(body, off)
    forms = []
    for i in range(count):
        start = r.p
        rt, rv = r.refid()
        flags = r.u32()
        t = r.u8()
        ver = r.u8() if with_version else None
        sz = (t >> 6) & 0x3
        if sz == 0:
            l1 = r.u8(); l2 = r.u8()
        elif sz == 1:
            l1 = r.u16(); l2 = r.u16()
        elif sz == 2:
            l1 = r.u32(); l2 = r.u32()
        else:
            raise ValueError('bad size bits at form %d offset %d' % (i, start))
        data = body[r.p:r.p + l1]
        r.p += l1
        forms.append(dict(idx=i, off=start, rtype=rt, rval=rv, flags=flags,
                          type=t & 0x3F, sizebits=sz, ver=ver,
                          l1=l1, l2=l2, data=data))
    return forms, r.p


def decompress(cf):
    if cf['l2'] == 0:
        return cf['data']
    try:
        return zlib.decompress(cf['data'])
    except Exception:
        try:
            import lz4.block
            return lz4.block.decompress(cf['data'], uncompressed_size=cf['l2'])
        except Exception:
            return None


def decode_initial(data, flags):
    """Decode ChangeFormInitialData -> dict. Returns (dict, bytes_consumed)."""
    r = R(data)
    out = {}
    if flags & 0x00000001:
        out['recordFlags'] = r.u32()
        out['unk16'] = r.u16()
    if flags & 0x00000002:
        out['cell'] = r.refid()
        out['posX'] = r.f32(); out['posY'] = r.f32(); out['posZ'] = r.f32()
        out['rotX'] = r.f32(); out['rotY'] = r.f32(); out['rotZ'] = r.f32()
    # CHANGE_REFR_HAVOK_MOVE (0x4) is a variable-length havok blob, NOT another
    # 27-byte transform. It always follows CHANGE_REFR_MOVE, so stop here.
    if flags & 0x00000004:
        out['havokBlobFollows'] = True
    return out, r.p


def main():
    path = sys.argv[1]
    hdr, body = load(path)
    fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
    print('save          : %s' % path.rsplit('\\', 1)[-1])
    print('formVersion   : %d  plugins=%d light=%d' % (fv, len(plugins), len(light)))
    print('changeForms   : offset=%d count=%d'
          % (flt['changeFormsOffset'], flt['changeFormCount']))

    formids = read_formid_array(body, flt['formIDArrayCountOffset'])
    print('formIDArray   : %d entries' % len(formids))

    # ground truth position from global data type 1
    truth = None
    for tbl, o, c in ((1, flt['globalDataTable1Offset'], flt['globalDataTable1Count']),
                      (2, flt['globalDataTable2Offset'], flt['globalDataTable2Count']),
                      (3, flt['globalDataTable3Offset'], flt['globalDataTable3Count'])):
        for t, chunk in global_data(body, o, c):
            if t == 1:
                truth = player_location(chunk)
    print('truth pos     : %.2f %.2f %.2f' % (truth['posX'], truth['posY'], truth['posZ']))

    for wv in (True, False):
        try:
            forms, end = parse_change_forms(body, flt['changeFormsOffset'],
                                            flt['changeFormCount'], wv)
        except Exception as e:
            print('  with_version=%s -> PARSE FAILED: %s' % (wv, e))
            continue
        # sanity: does the table end where globalDataTable3 begins?
        g3 = flt['globalDataTable3Offset']
        print('  with_version=%s -> parsed %d, table ends at %d, gdt3 at %d, delta %d'
              % (wv, len(forms), end, g3, end - g3))
        if end == g3:
            good = forms
            good_wv = wv
    print()

    forms, end = parse_change_forms(body, flt['changeFormsOffset'],
                                    flt['changeFormCount'], good_wv)

    # --- type histogram
    hist = Counter()
    for cf in forms:
        hist[cf['type']] += 1
    print('--- change form count by type (%d total)' % len(forms))
    for t, n in sorted(hist.items(), key=lambda kv: -kv[1]):
        print('   %3d  %-6s  %6d' % (t, TYPE_NAMES.get(t, '?'), n))

    # --- the player
    print()
    print('--- player (0x14)')
    for cf in forms:
        fid = resolve(cf['rtype'], cf['rval'], formids)
        if fid == 0x14 and cf['type'] in (0, 1):
            d = decompress(cf)
            print('   idx=%d rtype=%d rval=0x%X type=%d(%s) ver=%s flags=0x%08X [%s]'
                  % (cf['idx'], cf['rtype'], cf['rval'], cf['type'],
                     TYPE_NAMES.get(cf['type']), cf['ver'], cf['flags'],
                     flagstr(cf['flags'])))
            print('   l1=%d l2=%d decompressed=%s'
                  % (cf['l1'], cf['l2'], len(d) if d else None))
            if d:
                init, used = decode_initial(d, cf['flags'])
                for k, v in init.items():
                    print('      %-12s %s' % (k, v))
                print('      consumed %d of %d bytes' % (used, len(d)))
    return forms, formids, truth


if __name__ == '__main__':
    main()
