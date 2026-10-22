"""Global data tables: Papyrus health, temp effects, created objects, weather."""
import sys, struct
from collections import Counter
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mirele-water')
from savepos import R, load, parse_body, global_data, player_location
from changeforms import (TYPE_NAMES, parse_change_forms, read_formid_array,
                         resolve, decompress, decode_initial, flagstr)

PATH = r'C:\1. AUTHORIA\profiles\DEEZ CS NUTZ\saves\Save16_A67A30D7_0_456E6F7261_Tamriel_000240_20260822162235_1_1.ess'
hdr, body = load(PATH)
fv, plugins, light, flt = parse_body(body, hdr['bodyBase'])
formids = read_formid_array(body, flt['formIDArrayCountOffset'])

NAMES = {0:'MiscStats',1:'PlayerLocation',2:'TES',3:'GlobalVariables',4:'CreatedObjects',
         5:'Effects',6:'Weather',7:'Audio',8:'SkyCells',
         100:'ProcessLists',101:'Combat',102:'Interface',103:'ActorCauses',104:'Unknown104',
         105:'DetectionManager',106:'LocationMetaData',107:'QuestStaticData',108:'StoryTeller',
         109:'MagicFavorites',110:'PlayerControls',111:'StoryEventManager',
         112:'IngredientShared',113:'MenuControls',114:'MenuTopicManager',
         1000:'TempEffects',1001:'Papyrus',1002:'AnimObjects',1003:'Timer',
         1004:'SynchronizedAnimations',1005:'Main'}

chunks = {}
for tbl,(o,c) in enumerate([(flt['globalDataTable1Offset'],flt['globalDataTable1Count']),
                            (flt['globalDataTable2Offset'],flt['globalDataTable2Count']),
                            (flt['globalDataTable3Offset'],flt['globalDataTable3Count'])],1):
    print('--- global data table %d (%d entries)' % (tbl, c))
    for t, ch in global_data(body, o, c):
        chunks[t] = ch
        print('   type %-5d %-24s %10d bytes' % (t, NAMES.get(t,'?'), len(ch)))

# Papyrus header
p = chunks.get(1001)
if p:
    r = R(p)
    ver = r.u16()
    strcount = r.u16()
    print()
    print('=== Papyrus ===')
    print(' version=%d  stringTableCount=%d  totalBytes=%d' % (ver, strcount, len(p)))
    # skip strings
    strs=[]
    for _ in range(strcount):
        strs.append(r.wstr())
    print(' strings parsed=%d  next offset=%d' % (len(strs), r.p))
    scriptCount = r.u32()
    print(' scriptCount=%d' % scriptCount)

# temp effects
te = chunks.get(1000)
print()
print('=== TempEffects === %d bytes' % (len(te) if te else -1))

# created objects
co = chunks.get(4)
if co:
    r = R(co)
    print()
    print('=== CreatedObjects === %d bytes' % len(co))
    for label in ('weapons','armors','potions','enchantments'):
        n = r.u32()
        print('  %-14s %d' % (label, n))
        for _ in range(n):
            rid = r.refid(); ncomp = r.u32()
            for _ in range(ncomp):
                r.refid(); r.u32()

# weather
w = chunks.get(6)
if w:
    r = R(w)
    print()
    print('=== Weather === %d bytes' % len(w))
    for k in ('climate','weather','prevWeather','unkWeather1','unkWeather2','regnWeather'):
        print('  %-14s %s' % (k, r.refid()))
    print('  curTime %.3f  begTime %.3f  weatherPct %.4f' % (r.f32(), r.f32(), r.f32()))

# process lists
pl = chunks.get(100)
if pl:
    r = R(pl)
    print()
    print('=== ProcessLists === %d bytes' % len(pl))
    print('  unk floats %.3f %.3f %.3f' % (r.f32(), r.f32(), r.f32()))
    for i in range(3):
        n = r.u32()
        print('  list %d count=%d' % (i, n))
        for _ in range(n):
            r.refid()

# --- dump the 12+12 water-plane created refs in full
forms, end = parse_change_forms(body, flt['changeFormsOffset'], flt['changeFormCount'], True)
print()
print('=== raw bytes of the z=600 created refs ===')
n=0
for cf in forms:
    fid = resolve(cf['rtype'], cf['rval'], formids)
    if fid in (0xFF000E8B, 0xFF002567, 0xFF0026AC, 0xFF00129D):
        d = decompress(cf)
        print(' %08X flags=0x%08X ver=%d l1=%d : %s' % (fid, cf['flags'], cf['ver'], cf['l1'], d.hex()))
        n+=1
print()
print('nextObjectId from PlayerLocation =', player_location(chunks[1])['nextObjectId'],
      '= 0x%X' % player_location(chunks[1])['nextObjectId'])
