"""Build 'Authoria - Patch - Wanderers Fair - No Reseat.esp' on Wanderer's Fair 2.0.1.3.

Records:
  QUST 0014BD SkyrimFairAudioQuest - the 2.0.1.3 record, byte for byte, except
      SkyrimFairCrowdCull.Table  -> distance-capped table (3000 u, +512 animals, +1024 children)
      SkyrimFairAudioScript.SeatLayoutVersion 4 -> 0 (same as the shipped No Reseat; Reseat never runs)
  SPEL 00080B neabAttribSizeFix (HeightSizeFix.esp) - original + condition HasKeyword(SkyrimFairNPC) == 0
Masters: Skyrim.esm, SkyrimFair.esp, HeightSizeFix.esp. ESL flag, form version 44.
"""
import json, struct, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from espmini import *

FAIR13 = r"C:\1. AUTHORIA\_staging\skyrimfair-2.0.1.3-extract\SkyrimFair.esp"
HSF = r"C:\1. AUTHORIA\mods\Furnitures Height Size Fix\HeightSizeFix.esp"
TABLE = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\35577e0a-6804-467b-92d6-5366d0c7976f\scratchpad\upd\table\table_cap3000_movers.json"
OUT = os.path.join(HERE, "out", "Authoria - Patch - Wanderers Fair - No Reseat.esp")

MASTERS = ["Skyrim.esm", "SkyrimFair.esp", "HeightSizeFix.esp"]
KW_FAIRNPC = 0x0100171E  # SkyrimFairNPC, SkyrimFair.esp = master index 1 here


def find(path, typ, local):
    for rec in iter_records(read_plugin(path)):
        if rec[0] == typ and rec[2] & 0xFFFFFF == local:
            return rec
    raise KeyError((path, typ, hex(local)))


# ---------- QUST 0014BD ----------
typ, flags, fid, vc, fver, unk, payload, _, _ = find(FAIR13, "QUST", 0x0014BD)
assert fid == 0x010014BD and fver == 44
subs = subrecords(payload)
vi = [i for i, (s, _) in enumerate(subs) if s == "VMAD"]
assert len(vi) == 1
vmad = bytearray(subs[vi[0]][1])
ver, objfmt, scripts, end = walk_vmad(bytes(vmad))
props = {(sn, p[0]): p for sn, _st, pl in scripts for p in pl}

table = json.load(open(TABLE))
assert len(table) == 29 * 33 * 6 == 5742
assert all(isinstance(v, int) and 0 <= v <= 0x7FFFFFFF for v in table)
pn, pt, ps, voff, vlen, val = props[("SkyrimFairCrowdCull", "Table")]
assert pt == 13 and len(val) == 5742 and vlen == 4 + 4 * 5742
struct.pack_into("<I%di" % 5742, vmad, voff, 5742, *table)

pn, pt, ps, voff, vlen, val = props[("SkyrimFairAudioScript", "SeatLayoutVersion")]
assert pt == 3 and val == 4
struct.pack_into("<i", vmad, voff, 0)

assert len(vmad) == len(subs[vi[0]][1])
subs[vi[0]][1] = bytes(vmad)
qust = pack_record("QUST", flags, fid, vc, fver, unk, pack_subrecords(subs))

# ---------- SPEL 00080B ----------
hsf_masters = tes4_masters(read_plugin(HSF))[3]
hsf_self = len(hsf_masters)  # 5: HeightSizeFix's own index in its file
NEW_HSF = MASTERS.index("HeightSizeFix.esp")  # 2


def remap(formid):
    idx = formid >> 24
    if formid == 0:
        return 0
    if idx == hsf_self:
        return (NEW_HSF << 24) | (formid & 0xFFFFFF)
    if idx == 0:
        return formid
    raise ValueError("unexpected master index in %08X" % formid)


typ, flags, fid, vc, fver, unk, payload, _, _ = find(HSF, "SPEL", 0x00080B)
subs = subrecords(payload)
out = []
ctda_seen = 0
for sig, d in subs:
    d = bytearray(d)
    if sig in ("ETYP", "EFID"):
        struct.pack_into("<I", d, 0, remap(struct.unpack_from("<I", d, 0)[0]))
    elif sig == "CTDA":
        func = struct.unpack_from("<H", d, 8)[0]
        p1 = struct.unpack_from("<I", d, 12)[0]
        if func in (264, 560):  # HasSpell, HasKeyword: param1 is a form
            struct.pack_into("<I", d, 12, remap(p1))
        else:
            raise ValueError("unexpected condition function %d" % func)
        ctda_seen += 1
    elif sig in ("OBND", "FULL", "DESC", "SPIT", "EFIT", "EDID"):
        pass
    else:
        raise ValueError("unexpected subrecord " + sig)
    out.append([sig, bytes(d)])
assert ctda_seen == 2 and out[-1][0] == "CTDA"
# copy of the HasKeyword(ActorTypeNPC) == 1 row, as HasKeyword(SkyrimFairNPC) == 0 (AND, EqualTo, run on Subject)
last = bytearray(out[-1][1])
assert struct.unpack_from("<H", last, 8)[0] == 560 and struct.unpack_from("<f", last, 4)[0] == 1.0 and last[0] == 0
struct.pack_into("<f", last, 4, 0.0)
struct.pack_into("<I", last, 12, KW_FAIRNPC)
out.append(["CTDA", bytes(last)])
spel = pack_record("SPEL", flags, remap(fid), vc, fver, unk, pack_subrecords(out))

# ---------- TES4 + groups ----------
hdr_subs = [["HEDR", struct.pack("<fiI", 1.71, 4, 0x800)],  # 2 records + 2 groups
            ["CNAM", b"Authoria\x00"],
            ["SNAM", ("Wanderer's Fair 2.0.1.3: crowd cull capped at 3000 units (new game), Reseat skipped, "
                      "fair visitors excluded from the Furnitures Height Size Fix ability.").encode("cp1252") + b"\x00"]]
for m in MASTERS:
    hdr_subs += [["MAST", m.encode("cp1252") + b"\x00"], ["DATA", b"\x00" * 8]]
tes4 = pack_record("TES4", 0x200, 0, 0, 44, 0, pack_subrecords(hdr_subs))

body = tes4 + pack_grup(b"SPEL", 0, spel) + pack_grup(b"QUST", 0, qust)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "wb").write(body)
print("wrote", OUT, len(body), "bytes")
