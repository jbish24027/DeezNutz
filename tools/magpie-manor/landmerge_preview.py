"""Preview the merged LAND for Magpie cells: Magpie heights + Northern Roads corner vertices.
Prints, per cell, the NR-changed vertices with vanilla/NR/Magpie heights and the VHGT delta bytes
that a merged record must carry (Magpie's encoding with the NR vertices substituted).
"""
import sys, struct, os
sys.path.insert(0, os.path.dirname(__file__))
from landscan import find_land

CELLS = {"(21,-1) 000A5CC": 0x000A5CC, "(20,-1) 000A5CD": 0x000A5CD, "(21,-2) 000A5EB": 0x000A5EB}
VAN = r"C:\1. AUTHORIA\Stock Game\Data\Skyrim.esm"
NR = r"C:\1. AUTHORIA\mods\Northern Roads\Northern Roads.esp"
MAG = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\9a43b8e7-0b19-41bd-935d-ecdecbe3c85d\scratchpad\extract\bsa\data\Magpie Manor\MagpieManor.esp"

def encode(H, offset):
    """Return the 1089 delta bytes for absolute heights H (dict (x,y)->units) using the given float offset.
    Heights are in game units; VHGT stores (offset + cumulative deltas) * 8."""
    raw = [0]*1089
    prev_rowstart = 0.0
    for y in range(33):
        h0 = H[(0, y)] / 8.0 - offset
        d = round(h0 - prev_rowstart)
        raw[y*33] = d
        prev_rowstart = prev_rowstart + d
        cur = prev_rowstart
        for x in range(1, 33):
            hx = H[(x, y)] / 8.0 - offset
            d = round(hx - cur)
            raw[y*33 + x] = d
            cur += d
    bad = [d for d in raw if d < -128 or d > 127]
    return raw, bad

for name, lid in CELLS.items():
    Hv, _ = find_land(VAN, lid); Hn, _ = find_land(NR, lid); Hm, _ = find_land(MAG, lid)
    print(f"\n===== {name}")
    nr_changed = [k for k in Hv if abs(Hn[k]-Hv[k]) > 0.01]
    mag_changed = [k for k in Hv if abs(Hm[k]-Hv[k]) > 0.01]
    print(f"NR changed {len(nr_changed)} vertices; Magpie changed {len(mag_changed)}; overlap {len(set(nr_changed)&set(mag_changed))}")
    if not mag_changed:
        print("  -> Magpie heights == vanilla here: patch should simply carry Northern Roads' LAND (forward from NR).")
        continue
    merged = dict(Hm)
    for k in nr_changed: merged[k] = Hn[k]
    print("  NR vertices to graft onto Magpie's LAND (x,y: vanilla -> NR height, game units):")
    for k in sorted(nr_changed, key=lambda t: (t[1], t[0])):
        print(f"    ({k[0]:2d},{k[1]:2d}): {Hv[k]:9.1f} -> {Hn[k]:9.1f}   (Magpie has {Hm[k]:9.1f})")
    # Magpie's own offset: read raw VHGT to get offset — approximate by decoding: offset = H[(0,0)]/8 - raw[0]; simpler: use Magpie's (0,0) height/8 as offset if raw[0]==0
    # We recompute using Magpie's own encoding: find offset such that Magpie re-encodes with zero mismatch
    # (offset = Hm[(0,0)]/8 works only when raw[0]==0, which is the CK's convention.)
    off = Hm[(0,0)]/8.0
    raw_m, bad_m = encode(Hm, off)
    raw_x, bad_x = encode(merged, off)
    changed_bytes = [(i % 33, i // 33, raw_m[i], raw_x[i]) for i in range(1089) if raw_m[i] != raw_x[i]]
    print(f"  merged VHGT: {len(changed_bytes)} delta bytes differ from Magpie's encoding (offset {off:.1f}); out-of-range deltas: {len(bad_x)}")
    for x, y, a, b in changed_bytes:
        print(f"    byte at (x={x:2d},y={y:2d}): {a:4d} -> {b:4d}")
