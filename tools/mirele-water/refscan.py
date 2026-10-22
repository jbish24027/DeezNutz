"""Scan ChangeForms for references moved/disabled near the player."""
import math
import struct
import sys
from collections import Counter

sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import R, load, parse_body, global_data, player_location
from changeforms import (TYPE_NAMES, parse_change_forms, read_formid_array,
                         resolve, decompress, decode_initial, flagstr)

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ\saves\Save16_A67A30D7_0_456E6F7261_Tamriel_000240_20260822162235_1_1.ess'

hdr, body = load(PATH)
fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
formids = read_formid_array(body, flt['formIDArrayCountOffset'])
forms, end = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], True)

truth = None
for o, c in ((flt['globalDataTable1Offset'], flt['globalDataTable1Count']),
             (flt['globalDataTable2Offset'], flt['globalDataTable2Count']),
             (flt['globalDataTable3Offset'], flt['globalDataTable3Count'])):
    for t, chunk in global_data(body, o, c):
        if t == 1:
            truth = player_location(chunk)
PX, PY, PZ = truth['posX'], truth['posY'], truth['posZ']

# ---- heading -------------------------------------------------------------
for cf in forms:
    if resolve(cf['rtype'], cf['rval'], formids) == 0x14 and cf['type'] == 1:
        d = decompress(cf)
        init, _ = decode_initial(d, cf['flags'])
        rz = init['rotZ']; rx = init['rotX']
        print('=== PLAYER HEADING ===')
        print(' rotZ = %.6f rad = %.3f deg' % (rz, math.degrees(rz) % 360))
        print(' rotX = %.6f rad = %.3f deg (pitch, +ve = looking down)'
              % (rx, math.degrees(rx)))
        hd = math.degrees(rz) % 360
        dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
        print(' compass = %s' % dirs[int((hd + 11.25) % 360 // 22.5)])
        vx, vy = math.sin(rz), math.cos(rz)
        print(' view unit vector (x,y) = (%.4f, %.4f)' % (vx, vy))
        for bx in (0, -4096, -8192, -12288):
            if vx < 0 and bx < PX:
                t = (PX - bx) / -vx
                print('  crosses world x=%-7d at t=%8.1f  -> y=%.1f  (cell y=%d)'
                      % (bx, t, PY + t*vy, math.floor((PY + t*vy)/4096)))
        for by in (-57344, -53248):
            if vy > 0 and by > PY:
                t = (by - PY) / vy
                print('  crosses world y=%-7d at t=%8.1f  -> x=%.1f  (cell x=%d)'
                      % (by, t, PX + t*vx, math.floor((PX + t*vx)/4096)))
        # where does the eye ray meet the water plane z=600
        eye = PZ + 120.0
        drop = eye - 600.0
        if rx > 0:
            hyp = drop / math.tan(rx)
            print('  eye z~%.0f, water z=600: centre-screen ray meets water plane at'
                  ' horiz dist %.0f -> world (%.0f, %.0f)'
                  % (eye, hyp, PX + hyp*vx, PY + hyp*vy))
        break

print()
print('=== REFERENCE CHANGE FORMS ===')
REF_TYPES = {0, 1, 2, 3, 4, 5}
moved = []
flagged = []
nearby = []
badparse = 0
cnt_by_type_flag = Counter()

for cf in forms:
    if cf['type'] not in REF_TYPES:
        continue
    f = cf['flags']
    if f & 0x00000001:
        cnt_by_type_flag[(cf['type'], 'FORM_FLAGS')] += 1
    if f & 0x00000002:
        cnt_by_type_flag[(cf['type'], 'MOVE')] += 1
    if f & 0x00000004:
        cnt_by_type_flag[(cf['type'], 'HAVOK_MOVE')] += 1
    if f & 0x00000008:
        cnt_by_type_flag[(cf['type'], 'CELL_CHANGED')] += 1

    fid = resolve(cf['rtype'], cf['rval'], formids)
    d = decompress(cf)
    if d is None:
        badparse += 1
        continue
    init = None
    if f & 0x00000003:
        try:
            init, _ = decode_initial(d, f)
        except Exception:
            badparse += 1
            continue
    rec = dict(cf=cf, fid=fid, init=init)
    if init and 'recordFlags' in init:
        flagged.append(rec)
    if init and 'posX' in init:
        moved.append(rec)
        dx = init['posX'] - PX; dy = init['posY'] - PY
        dist = math.hypot(dx, dy)
        if dist < 12000:
            nearby.append((dist, rec))

print('reference change forms with each flag:')
for k, v in sorted(cnt_by_type_flag.items()):
    print('   type %d %-11s %-11s %6d' % (k[0], TYPE_NAMES.get(k[0]), k[1], v))
print('decoded MOVE blocks : %d' % len(moved))
print('decoded FORM_FLAGS  : %d' % len(flagged))
print('undecodable         : %d' % badparse)

# disabled = record flag bit 11 (0x800) "Initially Disabled"
DISABLED = 0x00000800
DELETED = 0x00000020
dis = [r for r in flagged if r['init']['recordFlags'] & DISABLED]
dele = [r for r in flagged if r['init']['recordFlags'] & DELETED]
print('records with Initially-Disabled bit set at save time : %d' % len(dis))
print('records with Deleted bit set at save time            : %d' % len(dele))

print()
print('=== MOVED REFERENCES WITHIN 12000 UNITS OF THE PLAYER ===')
nearby.sort(key=lambda t: t[0])
print('%d found' % len(nearby))
for dist, rec in nearby[:200]:
    cf = rec['cf']; init = rec['init']
    rf = init.get('recordFlags')
    print(' %8.1f  fid=%08X  type=%-4s  flags=%s  pos=(%.0f, %.0f, %.0f)%s'
          % (dist, rec['fid'] or 0, TYPE_NAMES.get(cf['type']), flagstr(cf['flags']),
             init['posX'], init['posY'], init['posZ'],
             ('  recFlags=0x%08X%s' % (rf, ' DISABLED' if rf & DISABLED else ''))
             if rf is not None else ''))

print()
print('=== DISABLED/DELETED RECORDS (all, with formid) ===')
print('disabled count %d' % len(dis))
import json
out = []
for r in dis:
    out.append(dict(fid='%08X' % (r['fid'] or 0), type=TYPE_NAMES.get(r['cf']['type']),
                    rtype=r['cf']['rtype'],
                    recFlags='0x%08X' % r['init']['recordFlags'],
                    changeFlags='0x%08X' % r['cf']['flags'],
                    pos=[r['init'].get('posX'), r['init'].get('posY'), r['init'].get('posZ')]))
open(r'C:\1. AUTHORIA\_tools\mirele-water\disabled_refs.json', 'w').write(json.dumps(out, indent=1))
print('written disabled_refs.json')
