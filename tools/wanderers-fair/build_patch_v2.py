"""Stage trim for 'Authoria - Patch - Wanderers Fair - No Reseat.esp' (2026-10-16).

Starts from the INSTALLED patch (which already carries the 3000 u capped Table and SeatLayoutVersion 0)
and edits the QUST 0014BD VMAD only:
  SkyrimFairAudioScript.Dancers2   43 -> KEEP_DANCERS (5)
  SkyrimFairAudioScript.Band        3 -> Lute, Drum          (Flute dropped)
  SkyrimFairAudioScript.Singers     3 -> lead, left          (right dropped)
  SkyrimFairAudioScript.Orchestra   9 -> 0
  SkyrimFairCrowdCull.Layers        dropped dancers -> 99 (never 'on' for any CrowdLayers value; Table indices untouched)
The SPEL record and the TES4 masters are copied as they are; the SNAM text is updated.

Usage: python -I build_patch_v2.py <config.json>   (config: {"keep_dancers": ["0C00C5", ...]} local SkyrimFair ids)
"""
import json
import os
import struct
import sys

sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\35577e0a-6804-467b-92d6-5366d0c7976f\scratchpad\build")
from espmini import read_plugin, iter_records, subrecords, pack_subrecords, pack_record, pack_grup, walk_vmad, tes4_masters  # noqa: E402

SRC = r"C:\1. AUTHORIA\mods\houseCARL - Authoria - Patch - Wanderers Fair - No Reseat\Authoria - Patch - Wanderers Fair - No Reseat.esp"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "Authoria - Patch - Wanderers Fair - No Reseat.esp")
FAIR = 1  # SkyrimFair.esp master index inside this patch

cfg = json.load(open(sys.argv[1]))
keep_dancers = [int(x, 16) | (FAIR << 24) for x in cfg["keep_dancers"]]
assert len(keep_dancers) == 5
BAND_KEEP = [0x010014C1, 0x010014C5]
SINGERS_KEEP = [0x010016B3, 0x010016B6]
ORCHESTRA_KEEP = []

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
# a QUST VMAD carries a fragment/alias section after the scripts; walk_vmad stops at the scripts' end.
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


# current arrays
dancers = [f for f, _a in props[("SkyrimFairAudioScript", "Dancers2")][5]]
band = [f for f, _a in props[("SkyrimFairAudioScript", "Band")][5]]
singers = [f for f, _a in props[("SkyrimFairAudioScript", "Singers")][5]]
orchestra = [f for f, _a in props[("SkyrimFairAudioScript", "Orchestra")][5]]
actors2 = [f for f, _a in props[("SkyrimFairCrowdCull", "Actors2")][5]]
layers = list(props[("SkyrimFairCrowdCull", "Layers")][5])
assert len(dancers) == 43 and len(band) == 3 and len(singers) == 3 and len(orchestra) == 9
assert len(actors2) == 184 and len(layers) == 184
assert all(k in dancers for k in keep_dancers) and all(k in band for k in BAND_KEEP) and all(k in singers for k in SINGERS_KEEP)

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
    (props[("SkyrimFairAudioScript", "Orchestra")], obj_array(ORCHESTRA_KEEP)),
    (props[("SkyrimFairCrowdCull", "Layers")], int_array(new_layers)),
]
# splice from the highest offset down so earlier offsets stay valid
for (pname, ptype, pstatus, voff, vlen, val), newb in sorted(edits, key=lambda e: -e[0][3]):
    assert ptype in (11, 13)
    vmad[voff:voff + vlen] = newb
    print(f"  {pname:10s} {vlen:5d} -> {len(newb):5d} bytes")

# re-walk to prove the result parses and holds the intended values
ver2, objfmt2, scripts2, end2 = walk_vmad(bytes(vmad))
assert bytes(vmad[end2:]) == tail, "quest fragment tail changed"
p2 = {(sn, p[0]): p for sn, _st, pl in scripts2 for p in pl}
assert [f for f, _ in p2[("SkyrimFairAudioScript", "Dancers2")][5]] == keep_dancers
assert [f for f, _ in p2[("SkyrimFairAudioScript", "Band")][5]] == BAND_KEEP
assert [f for f, _ in p2[("SkyrimFairAudioScript", "Singers")][5]] == SINGERS_KEEP
assert list(p2[("SkyrimFairAudioScript", "Orchestra")][5]) == []
assert list(p2[("SkyrimFairCrowdCull", "Layers")][5]) == new_layers
assert list(p2[("SkyrimFairCrowdCull", "Actors2")][5]) == list(props[("SkyrimFairCrowdCull", "Actors2")][5])
assert list(p2[("SkyrimFairCrowdCull", "Table")][5]) == list(props[("SkyrimFairCrowdCull", "Table")][5])
assert p2[("SkyrimFairAudioScript", "SeatLayoutVersion")][5] == 0
# every other property byte-identical in value
for key, p in props.items():
    if key in {k for k, _ in [(e[0][0], 0) for e in edits]} or key[1] in ("Dancers2", "Band", "Singers", "Orchestra", "Layers"):
        continue
    assert p2[key][5] == p[5], key

subs[vi[0]][1] = bytes(vmad)
qust_bytes = pack_record("QUST", flags, fid, vc, fver, unk, pack_subrecords(subs))
spel_bytes = pack_record("SPEL", spel[1], spel[2], spel[3], spel[4], spel[5], spel[6])

# TES4: keep everything, replace SNAM text
hdr = []
for sig, d in tsubs:
    if sig == "SNAM":
        d = ("Wanderer's Fair 2.0.1.3: crowd cull capped at 3000 units, Reseat skipped, fair visitors excluded from the "
             "Furnitures Height Size Fix ability. 2026-10-16 stage trim: 5 dancers, 2 singers (lead, left), band lute + drum, "
             "no orchestra; dropped dancers on crowd layer 99.").encode("cp1252") + b"\x00"
    hdr.append([sig, d])
tes4 = pack_record("TES4", tflags, 0, 0, tfver, 0, pack_subrecords(hdr))
body = tes4 + pack_grup(b"SPEL", 0, spel_bytes) + pack_grup(b"QUST", 0, qust_bytes)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "wb").write(body)
print("wrote", OUT, len(body), "bytes; dropped dancers:", ["%06X" % (f & 0xFFFFFF) for f in dropped_dancers])
json.dump({"dropped_dancers": ["%06X" % (f & 0xFFFFFF) for f in dropped_dancers]},
          open(os.path.join(os.path.dirname(OUT), "dropped.json"), "w"))
