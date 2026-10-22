"""CELL change forms + disabled refs near the lake."""
import math, struct, sys, json
from collections import Counter
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import R, load, parse_body, global_data, player_location
from changeforms import (TYPE_NAMES, parse_change_forms, read_formid_array,
                         resolve, decompress, decode_initial, flagstr)

PATH = r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ\saves\Save16_A67A30D7_0_456E6F7261_Tamriel_000240_20260822162235_1_1.ess'
hdr, body = load(PATH)
fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
formids = read_formid_array(body, flt['formIDArrayCountOffset'])
forms, end = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], True)

def cellfid(x, y):
    return 0x009B4F + (-13 - y) * 0x21 + (-x)

# lake / surrounding cells: x -10..2, y -20..-12
want = {}
for x in range(-10, 3):
    for y in range(-20, -11):
        want[cellfid(x, y)] = (x, y)

print('=== CELL change forms (421 total) ===')
hits = []
for cf in forms:
    if cf['type'] != 6:
        continue
    fid = resolve(cf['rtype'], cf['rval'], formids)
    if fid in want:
        hits.append((fid, want[fid], cf))
print('CELL change forms whose FormID is one of the %d Tamriel cells x[-10..2] y[-20..-12]: %d'
      % (len(want), len(hits)))
for fid, xy, cf in sorted(hits, key=lambda h: h[1]):
    d = decompress(cf)
    print('  %08X cell(%d,%d)  changeFlags=0x%08X  l1=%d l2=%d  data[:32]=%s'
          % (fid, xy[0], xy[1], cf['flags'], cf['l1'], cf['l2'],
             (d[:32].hex() if d else 'UNDECOMP')))

# all CELL change forms, grouped by flag
print()
cc = Counter()
for cf in forms:
    if cf['type'] == 6:
        cc[cf['flags']] += 1
print('CELL change form changeFlags histogram:')
for k, v in sorted(cc.items(), key=lambda kv: -kv[1]):
    print('   0x%08X  %5d' % (k, v))

# CELL change flags per UESP
CELLFLAGS = [(0x00000001,'FORM_FLAGS'),(0x00000002,'CELL_FLAGS'),
             (0x00000004,'CELL_FULLNAME'),(0x00000008,'CELL_OWNERSHIP'),
             (0x00000010,'CELL_EXTERIOR_SHORT'),(0x00000020,'CELL_EXTERIOR_CHAR'),
             (0x00000040,'CELL_DETACHTIME'),(0x00000080,'CELL_SEENDATA')]
for k in sorted(cc):
    names = [n for m,n in CELLFLAGS if k & m]
    rest = k & ~sum(m for m,_ in CELLFLAGS)
    print('   0x%08X -> %s %s' % (k, '|'.join(names), ('+0x%08X'%rest) if rest else ''))

print()
print('=== water-plane created refs ===')
for cf in forms:
    if cf['type'] not in (0,1,2,3,4,5): continue
    if not (cf['flags'] & 2): continue
    d = decompress(cf)
    if d is None: continue
    try: init,_ = decode_initial(d, cf['flags'])
    except Exception: continue
    if abs(init['posZ'] - 600.0) < 0.01 and -12288 < init['posX'] < 4096 and -65536 < init['posY'] < -53248:
        fid = resolve(cf['rtype'], cf['rval'], formids)
        print('  fid=%08X type=%s pos=(%.1f,%.1f,%.1f) rot=(%.3f,%.3f,%.3f) cellref=%s l1=%d flags=%s'
              % (fid, TYPE_NAMES.get(cf['type']), init['posX'],init['posY'],init['posZ'],
                 init['rotX'],init['rotY'],init['rotZ'], init['cell'], cf['l1'], flagstr(cf['flags'])))

print()
print('=== disabled non-created refs: resolve sample ===')
DIS=0x800
dis=[]
for cf in forms:
    if cf['type'] not in (0,1,2,3,4,5): continue
    if not (cf['flags'] & 1): continue
    d = decompress(cf)
    if d is None: continue
    try: init,_ = decode_initial(d, cf['flags'])
    except Exception: continue
    if init['recordFlags'] & DIS:
        fid = resolve(cf['rtype'], cf['rval'], formids)
        dis.append((fid, cf, init))
print('total disabled refs: %d' % len(dis))
created = [d for d in dis if d[0] is not None and (d[0] >> 24) == 0xFF]
print('  of which created 0xFF: %d' % len(created))
withpos = [d for d in dis if 'posX' in d[2]]
print('  of which carry a position: %d' % len(withpos))
PX,PY = 1139.57,-59578.77
near = [d for d in withpos if math.hypot(d[2]['posX']-PX, d[2]['posY']-PY) < 20000]
print('  disabled WITH position within 20000 units: %d' % len(near))
for fid, cf, init in sorted(near, key=lambda d: math.hypot(d[2]['posX']-PX, d[2]['posY']-PY))[:40]:
    print('   %8.0f  %08X %-4s pos=(%.0f,%.0f,%.0f) recFlags=0x%08X'
          % (math.hypot(init['posX']-PX, init['posY']-PY), fid,
             TYPE_NAMES.get(cf['type']), init['posX'],init['posY'],init['posZ'],
             init['recordFlags']))

json.dump([{'fid':'%08X'%(f or 0),'type':TYPE_NAMES.get(c['type']),
            'recFlags':'0x%08X'%i['recordFlags'],'changeFlags':'0x%08X'%c['flags'],
            'pos':[i.get('posX'),i.get('posY'),i.get('posZ')]} for f,c,i in dis],
          open(r'C:\1. AUTHORIA\_tools\mirele-water\disabled_refs.json','w'), indent=1)
print('wrote disabled_refs.json')
