"""Is each outfit piece still referenced by the player's changeform in a save?

Answers the question auto-stash raises: bAutoStashInactive=1 with an
unresolvable wardrobe container hands RemoveItem a null container, so a
stripped piece is destroyed rather than stored. If that happened, the outfit
JSON can be perfect and equipping still does nothing.

Method: an ESL item's runtime FormID (0xFExxxYYY) cannot fit a 22-bit RefID,
so the save stores it as a type-0 RefID - an index into the save's formIDArray.
Find the index, then look for that 3-byte RefID inside the player's change form.
"""
import struct, sys, zlib, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mirele-water'))
from savepos import load, parse_body, R
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_keepers as A
import json, io

def formid_array(body, flt):
    r = R(body, flt['formIDArrayCountOffset'])
    n = r.u32()
    return list(struct.unpack_from('<%dI' % n, body, r.p))

def change_forms(body, flt):
    r = R(body, flt['changeFormsOffset'])
    out = []
    for _ in range(flt['changeFormCount']):
        raw = (body[r.p] << 16) | (body[r.p+1] << 8) | body[r.p+2]; r.p += 3
        rtype, val = (raw >> 22) & 0x3, raw & 0x3FFFFF
        flags = r.u32(); ftype = r.u8(); ver = r.u8()
        lenkind = ftype >> 6
        def sized():
            if lenkind == 0: v = body[r.p]; r.p += 1; return v
            if lenkind == 1: v = struct.unpack_from('<H', body, r.p)[0]; r.p += 2; return v
            v = struct.unpack_from('<I', body, r.p)[0]; r.p += 4; return v
        l1 = sized(); l2 = sized()
        data = body[r.p:r.p + l1]; r.p += l1
        out.append((rtype, val, flags, ftype & 0x3F, ver, l1, l2, data))
    return out

save = sys.argv[1]
hdr, body = load(save)
fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
print("save     : %s" % os.path.basename(save))
print("player   : %s  level %d   %s" % (hdr['playerName'], hdr['playerLevel'], hdr['gameDate']))
print("changeForms %d   plugins %d + %d light" % (flt['changeFormCount'], len(plugins), len(light)))

fids = formid_array(body, flt)
index_of = {}
for i, f in enumerate(fids):
    index_of.setdefault(f, i)
print("formIDArray: %d entries" % len(fids))

cfs = change_forms(body, flt)
player = [c for c in cfs if c[0] == 1 and c[1] == 0x14]
if not player:
    sys.exit("player change form (RefID type 1, 0x14) not found")
rtype, val, flags, ftype, ver, l1, l2, data = player[0]
if l2:
    data = zlib.decompress(data)
print("player changeform: type=%d flags=0x%08X  %d bytes (%s)"
      % (ftype, flags, len(data), "zlib" if l2 else "raw"))

def refid_bytes(idx):
    raw = idx & 0x3FFFFF          # type 0 = index into formIDArray
    return bytes(((raw >> 16) & 0xFF, (raw >> 8) & 0xFF, raw & 0xFF))

doc = json.load(io.open(A.DATA, encoding='utf-8-sig'))
missing_all = []
for wheel in doc['wheels']:
    for slot in wheel['slots']:
        if not slot.get('hasOutfit'): continue
        print("\n--- %s" % slot['name'])
        for it in slot['items']:
            raw = it['rawID']
            idx = index_of.get(raw)
            if idx is None:
                print("   ABSENT from formIDArray   %-45s %s  raw 0x%08X"
                      % (it['plugin'], it['localID'], raw))
                missing_all.append((slot['name'], it, 'not-in-save'))
                continue
            hit = refid_bytes(idx) in data
            print("   %-9s idx %-6d %-45s %s"
                  % ("IN PLAYER" if hit else "not found", idx, it['plugin'], it['localID']))
            if not hit:
                missing_all.append((slot['name'], it, 'not-in-player'))
print("\n%d of %d entries not found in the player change form"
      % (len(missing_all), sum(len(s['items']) for w in doc['wheels'] for s in w['slots'] if s.get('hasOutfit'))))
