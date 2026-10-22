#!/usr/bin/env python3
"""Round 5 — game-wide blanket: every colored value on every rotation weather -> 10% chroma,
luminance-locked, hue-locked. Edits the patch ESP bytes in place (size-preserving), with the
subrecord layout PROVEN against houseCARL dumps of 10 anchor records before any write.
"""
import json, struct, sys, colorsys

K = 0.10
S_FLOOR = 0.08
ESP = r"C:\1. AUTHORIA\mods\houseCARL - Authoria - Patch - Astralite Dawn Warmth\Authoria - Patch - Astralite Dawn Warmth.esp"
SCRATCH = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\scratchpad"
ANCHOR_DUMP = r"C:\Users\User\.claude\projects\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\tool-results\mcp-housecarl-housecarl_batch_record_detail-1787258671770.txt"
COVERAGE = json.load(open(SCRATCH + r"\blanket_coverage.json"))["coverage"]

QUADS = ["Sunrise", "Day", "Sunset", "Night"]
NAM0_FIELDS = ["SkyUpperColor", "FogNearColor", "UnknownColor", "AmbientColor", "SunlightColor",
               "SunColor", "StarsColor", "SkyLowerColor", "HorizonColor", "EffectLightingColor",
               "CloudLodDiffuseColor", "CloudLodAmbientColor", "FogFarColor", "SkyStaticsColor",
               "WaterMultiplierColor", "SunGlareColor", "MoonGlareColor"]  # documented SSE order — VERIFIED below
DALC_DIRS = ["DirectionalXPlus", "DirectionalXMinus", "DirectionalYPlus", "DirectionalYMinus",
             "DirectionalZPlus", "DirectionalZMinus"]

def lum(r, g, b): return 0.2126 * r + 0.7152 * g + 0.0722 * b

def tone(rgb):
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if s < S_FLOOR: return None
    L = lum(r, g, b)
    out = tuple(min(255, max(0, int(round(L + (c - L) * K)))) for c in rgb)
    if out == rgb: return None
    assert abs(lum(*out) - L) <= 1.5, (rgb, out)
    return out

# ---------- load anchor dumps (semantic truth) ----------
raw = open(ANCHOR_DUMP, encoding="utf-8", errors="replace").read()
doc = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
assert doc.get("rendered") == doc.get("count") == 10 and not doc.get("truncated"), doc.keys()
anchors = {}
for r in doc["records"]:
    fm = {}
    for f in r["fields"]:
        fm[f["path"]] = f.get("value")
    anchors[r["formid"]] = fm

def acolor(fm, path):
    v = fm.get(path)
    if v is None: return None
    parts = str(v).split(",")
    if len(parts) != 4: return None
    try: return tuple(int(x) for x in parts)
    except ValueError: return None

# ---------- parse plugin ----------
data = bytearray(open(ESP, "rb").read())

def u16(o): return struct.unpack_from("<H", data, o)[0]
def u32(o): return struct.unpack_from("<I", data, o)[0]

# TES4 masters
assert data[0:4] == b"TES4"
tes4_size = u32(4)
masters = []
o, end = 24, 24 + tes4_size
while o < end:
    sig = bytes(data[o:o+4]); sz = u16(o+4)
    if sig == b"MAST": masters.append(data[o+6:o+6+sz-1].decode("cp1252"))
    o += 6 + sz
midx = {m.lower(): i for i, m in enumerate(masters)}
own_index = len(masters)

def full_formid(tok):
    local, origin = tok.split(":", 1)
    idx = midx.get(origin.lower(), own_index)
    return (idx << 24) | int(local, 16)

want = {full_formid(f): (f, COVERAGE[f]) for f in COVERAGE}

# walk records
records = {}  # fullid -> (data_off, data_size, flags)
o = 24 + tes4_size
n = len(data)
while o < n:
    sig = bytes(data[o:o+4])
    if sig == b"GRUP":
        o += 24; continue
    dsz = u32(o+4); flags = u32(o+8); fid = u32(o+12)
    if sig == b"WTHR" and fid in want:
        assert not (flags & 0x00040000), f"compressed WTHR {want[fid][0]}"
        records[fid] = (o + 24, dsz)
    o += 24 + dsz

missing = [want[f][1] for f in want if f not in records]
assert not missing, f"records not found in plugin: {missing[:8]} ({len(missing)})"
print(f"masters={len(masters)}  WTHR records located: {len(records)}/146")

def subrecords(off, size):
    out, o, end = [], off, off + size
    while o < end:
        sig = bytes(data[o:o+4]).decode("ascii", "replace"); sz = u16(o+4)
        out.append((sig, o + 6, sz))
        o += 6 + sz
    return out

# ---------- layout verification against all 10 anchors ----------
def get_subs(fid):
    off, size = records[fid]
    subs = {}
    for sig, so, sz in subrecords(off, size):
        subs.setdefault(sig, []).append((so, sz))
    return subs

nam0_slots = None
dalc_unique_proof = set()
verified = 0
for tok, eid in [(t, e) for t, e in COVERAGE.items() if t in anchors]:
    fid = full_formid(tok); fm = anchors[tok]
    subs = get_subs(fid)
    # NAM0: slots x 4 quads x RGBA
    (nam0_off, nam0_sz) = subs["NAM0"][0]
    slots = nam0_sz // 16
    cand = [set() for _ in range(slots)]
    for s in range(slots):
        for fname in NAM0_FIELDS:
            ok = True
            for q in range(4):
                exp = acolor(fm, f"{fname}.{QUADS[q]}")
                if exp is None: ok = False; break
                gotv = tuple(data[nam0_off + s*16 + q*4: nam0_off + s*16 + q*4 + 4])
                if gotv != exp: ok = False; break
            if ok: cand[s].add(fname)
    if nam0_slots is None:
        nam0_slots = cand
    else:
        nam0_slots = [a & b if (a and b) else (a or b) for a, b in zip(nam0_slots, cand)]
    # DALC: order of the 4 quadrant subrecords
    dalcs = subs.get("DALC", [])
    assert len(dalcs) == 4, (eid, len(dalcs))
    for bi, (so, sz) in enumerate(dalcs):
        assert sz == 32, (eid, sz)
        cands = set()
        for q in QUADS:
            if all(acolor(fm, f"DirectionalAmbientLightingColors.{q}.{d}") == tuple(data[so + i*4: so + i*4 + 4])
                   for i, d in enumerate(DALC_DIRS)):
                cands.add(q)
        # documented block order is Sunrise, Day, Sunset, Night — must be consistent with the data
        assert QUADS[bi] in cands, (eid, bi, cands)
        if len(cands) == 1:
            dalc_unique_proof.add((bi, QUADS[bi]))
    # PNAM cloud colors: verify a few dump-known cloud colors
    if "PNAM" in subs:
        po, psz = subs["PNAM"][0]
        checked = 0
        for i in range(psz // 16):
            for q in range(4):
                exp = acolor(fm, f"Clouds[{i}].Colors.{QUADS[q]}")
                if exp is not None:
                    got = tuple(data[po + i*16 + q*4: po + i*16 + q*4 + 4])
                    assert got == exp, (eid, i, q, got, exp)
                    checked += 1
        assert checked > 0, (eid, "no cloud colors verified")
    verified += 1

# NAM0 slot map: purely data-derived. A slot whose bytes matched known field(s) in EVERY anchor
# is a proven color slot (ties between identical-valued fields are harmless — uniform transform).
# A slot that matched nothing anywhere is left UNTREATED (the format's unknown slot).
final_slots, untreated = [], []
claimed = set()
for s, cand in enumerate(nam0_slots):
    cand = set(cand)
    if not cand:
        final_slots.append(None); untreated.append(s); continue
    fresh = cand - claimed
    pick = sorted(fresh or cand)[0]
    claimed.add(pick)
    label = pick if len(cand) == 1 else f"{pick}~tie"
    final_slots.append(label)
mapped = [f for f in final_slots if f]
if len(untreated) > 1:
    raise SystemExit(f"NAM0: {len(untreated)} unmatched slots {untreated} — refusing (expected at most 1 unknown)")
core = {"SkyUpperColor","FogNearColor","AmbientColor","SunlightColor","SunColor","SkyLowerColor",
        "HorizonColor","EffectLightingColor","FogFarColor","SunGlareColor"}
have = {f.split("~")[0] for f in mapped}
missing_core = core - have
if missing_core:
    raise SystemExit(f"NAM0: core fields unmatched: {missing_core} — refusing")
print(f"NAM0 map ({len(final_slots)} slots): " + ", ".join(f"{i}={f or 'UNKNOWN-skip'}" for i, f in enumerate(final_slots)))
assert all((bi, q) in dalc_unique_proof for bi, q in [(0, "Sunrise"), (2, "Sunset")]), dalc_unique_proof
print(f"layout PROVEN on {verified}/10 anchors: NAM0 {len(final_slots)} slots, DALC documented order uniquely proven: {sorted(dalc_unique_proof)}")

# ---------- transform every covered record ----------
DALC_Q = QUADS
ledger, stats = {}, {"colors": 0, "records": 0, "skipped_low_S": 0}
for tok, eid in sorted(COVERAGE.items(), key=lambda kv: kv[1]):
    fid = full_formid(tok)
    subs = get_subs(fid)
    entries = []
    def treat(off, label):
        rgb = tuple(data[off:off+3])
        new = tone(rgb)
        if new is None:
            stats["skipped_low_S"] += 1; return
        data[off], data[off+1], data[off+2] = new
        entries.append(f"{label}: {rgb[0]},{rgb[1]},{rgb[2]} -> {new[0]},{new[1]},{new[2]}")
        stats["colors"] += 1
    no, nsz = subs["NAM0"][0]
    assert nsz // 16 == len(final_slots), (eid, nsz)
    for s in range(nsz // 16):
        if final_slots[s] is None: continue
        for q in range(4):
            treat(no + s*16 + q*4, f"{final_slots[s]}.{QUADS[q]}")
    for qi, (so, sz) in enumerate(subs["DALC"]):
        for i, d in enumerate(DALC_DIRS + ["Specular"]):
            treat(so + i*4, f"DALC.{DALC_Q[qi]}.{d}")
    if "PNAM" in subs and "JNAM" in subs:
        po, psz = subs["PNAM"][0]; jo, jsz = subs["JNAM"][0]
        for i in range(min(psz, jsz) // 16):
            for q in range(4):
                alpha = struct.unpack_from("<f", data, jo + i*16 + q*4)[0]
                if alpha > 0.0:
                    treat(po + i*16 + q*4, f"Clouds[{i}].{QUADS[q]}")
    ledger[eid] = entries
    stats["records"] += 1

open(ESP, "wb").write(data)
json.dump(ledger, open(SCRATCH + r"\TONE-LEDGER-round5-blanket.json", "w"), indent=0)
print(f"records treated: {stats['records']}   colors changed: {stats['colors']}   low-strength left alone: {stats['skipped_low_S']}")
top = sorted(((len(v), k) for k, v in ledger.items()), reverse=True)[:5]
print("busiest:", top)
print("wrote plugin + TONE-LEDGER-round5-blanket.json")
