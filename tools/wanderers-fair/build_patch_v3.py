"""Stage trim v3 for 'Authoria - Patch - Wanderers Fair - No Reseat.esp' (2026-10-17).

Same as v2 (5 dancers, lute + drum, lead + left singer, dropped dancers on crowd layer 99) with ONE change:
the Orchestra array is left as the original 9 refs instead of being emptied. An EMPTY array in a VMAD
makes the game log 'Property Orchestra ... cannot be initialized because the value is the incorrect type'
and leaves the property None. The 9 orchestra refs are InitiallyDisabled by the Holidays and Fair patch,
and every use of Orchestra in SkyrimFairAudioScript is guarded by Is3DLoaded(), so keeping them listed
costs nothing and the orchestra still never plays.

Source is the PRE-TRIM patch (the 10-14 build: 3000 u Table cap + SeatLayoutVersion 0), not the installed one.

Usage: python -I build_patch_v3.py <config.json> <source.esp> <out.esp>
"""
import json
import os
import struct
import sys

sys.path.insert(0, "C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/35577e0a-6804-467b-92d6-5366d0c7976f/scratchpad/build")
from espmini import read_plugin, iter_records, subrecords, pack_subrecords, pack_record, pack_grup, walk_vmad, tes4_masters  # noqa: E402

FAIR = 1  # SkyrimFair.esp master index inside this patch

cfg = json.load(open(sys.argv[1]))
SRC = sys.argv[2]
OUT = sys.argv[3]
keep_dancers = [int(x, 16) | (FAIR << 24) for x in cfg["keep_dancers"]]
assert len(keep_dancers) == 5
BAND_KEEP = [0x010014C1, 0x010014C5]
SINGERS_KEEP = [0x010016B3, 0x010016B6]

data = read_plugin(SRC)
tflags, tfver, tsubs, masters = tes4_masters(data)
assert masters == ["Skyrim.esm", "SkyrimFair.esp", "HeightSizeFix.esp"], masters

recs = list(iter_records(data))
qust = [r for r in recs if r[0] == "QUST" and (r[2] & 0xFFFFFF) == 0x0014BD][0]
spel = [r for r in recs if r[0] == "SPEL"][0]
assert len([r for r in recs if r[0] not in ("TES4",)]) == 2, [r[0] for r in recs]

typ, flags, fid, vc, fver, unk, payload, _, _ = qust
subs = subrecords(payload)
vi = [i for i, (s, _) in enumerate(subs) if s == "VMAD"]
assert len(vi) == 1
vmad = bytearray(subs[vi[0]][1])
ver, objfmt, scripts, end = walk_vmad(bytes(vmad))
assert ver == 5 and objfmt == 2 and end <= len(vmad), (ver, objfmt, end, len(vmad))
tail = bytes(vmad[end:])
print(f"  VMAD {len(vmad)} bytes: scripts end at {end}, quest fragment tail {len(tail)} bytes (kept verbatim)")
props = {(sn, p[0]): p for sn, _st, pl in scripts for p in pl}


def obj_array(fids):
    b = struct.pack("<I", len(fids))
    for f in fids:
        b += struct.pack("<HhI", 0, -1, f)
    return b


def int_array(vals):
    return struct.pack("<I%di" % len(vals), len(vals), *vals)


dancers = [f for f, _a in props[("SkyrimFairAudioScript", "Dancers2")][5]]
band = [f for f, _a in props[("SkyrimFairAudioScript", "Band")][5]]
singers = [f for f, _a in props[("SkyrimFairAudioScript", "Singers")][5]]
orchestra = [f for f, _a in props[("SkyrimFairAudioScript", "Orchestra")][5]]
actors2 = [f for f, _a in props[("SkyrimFairCrowdCull", "Actors2")][5]]
layers = list(props[("SkyrimFairCrowdCull", "Layers")][5])
assert len(dancers) == 43 and len(band) == 3 and len(singers) == 3 and len(orchestra) == 9, (len(dancers), len(band), len(singers), len(orchestra))
assert len(actors2) == 184 and len(layers) == 184
assert all(k in dancers for k in keep_dancers) and all(k in band for k in BAND_KEEP) and all(k in singers for k in SINGERS_KEEP)
assert props[("SkyrimFairAudioScript", "SeatLayoutVersion")][5] == 0, "source is not the No Reseat build"

dropped_dancers = [f for f in dancers if f not in keep_dancers]
assert len(dropped_dancers) == 38
new_layers = list(layers)
hits = 0
for i, f in enumerate(actors2):
    if f in dropped_dancers:
        new_layers[i] = 99
        hits += 1
assert hits == 38, hits

edits = [
    (props[("SkyrimFairAudioScript", "Dancers2")], obj_array(keep_dancers)),
    (props[("SkyrimFairAudioScript", "Band")], obj_array(BAND_KEEP)),
    (props[("SkyrimFairAudioScript", "Singers")], obj_array(SINGERS_KEEP)),
    (props[("SkyrimFairCrowdCull", "Layers")], int_array(new_layers)),
]
for (pname, ptype, pstatus, voff, vlen, val), newb in sorted(edits, key=lambda e: -e[0][3]):
    assert ptype in (11, 13)
    vmad[voff:voff + vlen] = newb
    print(f"  {pname:10s} {vlen:5d} -> {len(newb):5d} bytes")

ver2, objfmt2, scripts2, end2 = walk_vmad(bytes(vmad))
assert bytes(vmad[end2:]) == tail, "quest fragment tail changed"
p2 = {(sn, p[0]): p for sn, _st, pl in scripts2 for p in pl}
assert [f for f, _ in p2[("SkyrimFairAudioScript", "Dancers2")][5]] == keep_dancers
assert [f for f, _ in p2[("SkyrimFairAudioScript", "Band")][5]] == BAND_KEEP
assert [f for f, _ in p2[("SkyrimFairAudioScript", "Singers")][5]] == SINGERS_KEEP
assert [f for f, _ in p2[("SkyrimFairAudioScript", "Orchestra")][5]] == orchestra and len(orchestra) == 9
assert list(p2[("SkyrimFairCrowdCull", "Layers")][5]) == new_layers
assert list(p2[("SkyrimFairCrowdCull", "Actors2")][5]) == list(props[("SkyrimFairCrowdCull", "Actors2")][5])
assert list(p2[("SkyrimFairCrowdCull", "Table")][5]) == list(props[("SkyrimFairCrowdCull", "Table")][5])
assert p2[("SkyrimFairAudioScript", "SeatLayoutVersion")][5] == 0
changed = {"Dancers2", "Band", "Singers", "Layers"}
empties = []
for key, p in props.items():
    if key[1] in changed:
        continue
    assert p2[key][5] == p[5], key
for key, p in p2.items():
    if p[1] in (11, 12, 13, 14, 15) and len(p[5]) == 0:
        empties.append(key)
assert not empties, ("EMPTY ARRAY PROPERTIES WOULD FAIL TO INITIALISE", empties)
print("  no empty array properties in the result")

subs[vi[0]][1] = bytes(vmad)
qust_bytes = pack_record("QUST", flags, fid, vc, fver, unk, pack_subrecords(subs))
spel_bytes = pack_record("SPEL", spel[1], spel[2], spel[3], spel[4], spel[5], spel[6])

hdr = []
for sig, d in tsubs:
    if sig == "SNAM":
        d = ("Wanderer's Fair 2.0.1.3: crowd cull capped at 3000 units, Reseat skipped, fair visitors excluded from the "
             "Furnitures Height Size Fix ability. 2026-10-16 stage trim (v3 2026-10-17): 5 dancers, 2 singers (lead, left), "
             "band lute + drum; dropped dancers on crowd layer 99; the 9 orchestra refs stay listed (InitiallyDisabled by the "
             "Holidays and Fair patch) because an empty VMAD array fails to initialise.").encode("cp1252") + b"\x00"
    hdr.append([sig, d])
tes4 = pack_record("TES4", tflags, 0, 0, tfver, 0, pack_subrecords(hdr))
body = tes4 + pack_grup(b"SPEL", 0, spel_bytes) + pack_grup(b"QUST", 0, qust_bytes)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "wb").write(body)
print("wrote", OUT, len(body), "bytes; dropped dancers:", ["%06X" % (f & 0xFFFFFF) for f in dropped_dancers])
