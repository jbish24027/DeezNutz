#!/usr/bin/env python3
"""Round 4 — Solstheim ash tint, hugely reduced, tone-locked.

User: "whatever the tinting mechanism is I want is hugely reduced" +
"I dont want you to change the tone at all, i just want the tone less strong."

Mechanism found: the ash weathers' own authored colors at ALL quadrants (sky,
fogs, clouds, sunlight, ambient) — image spaces have zero tint, VL is shared
with the mainland. So: whole color surface, luminance-preserving chroma cut.

Transform (fixes round 3's brightening): c' = L + (c - L) * K, with L =
Rec.709 luminance of the color. Brightness EXACT, hue preserved, chroma -> K.
Round 3 held the MAX channel instead, which brightened dark reds 50-85%.

Gate: red family only — S >= 0.08 and (H <= 45 or H >= 300). Blues/neutrals
byte-identical.
"""
import json, re, sys, colorsys

K = 0.25
SRC = [
    r"C:\Users\User\.claude\projects\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\tool-results\mcp-housecarl-housecarl_batch_record_detail-1787251101612.txt",
    r"C:\Users\User\.claude\projects\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\tool-results\mcp-housecarl-housecarl_batch_record_detail-1787251288340.txt",
    r"C:\Users\User\.claude\projects\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\tool-results\mcp-housecarl-housecarl_batch_record_detail-1787251291080.txt",
]
OUT = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\scratchpad"

QUADS = ["Sunrise", "Day", "Sunset", "Night"]
DIRS = ["DirectionalXPlus", "DirectionalXMinus", "DirectionalYPlus",
        "DirectionalYMinus", "DirectionalZPlus", "DirectionalZMinus"]
WHOLE = ["SkyUpperColor", "SkyLowerColor", "HorizonColor", "FogNearColor",
         "FogFarColor", "AmbientColor", "SunlightColor", "SunColor",
         "SunGlareColor", "StarsColor", "MoonGlareColor",
         "WaterMultiplierColor", "EffectLightingColor",
         "CloudLodDiffuseColor", "CloudLodAmbientColor"]

C4 = re.compile(r"^\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*$")

def load():
    out, seen = [], set()
    for src in SRC:
        raw = open(src, encoding="utf-8", errors="replace").read()
        doc = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
        recs = doc["records"]
        # accounting: a truncated file may only PARTIALLY render — take what it
        # rendered, later files supply the rest; final count is asserted below.
        for r in recs:
            if r["formid"] in seen:
                continue
            seen.add(r["formid"])
            fm = {}
            fl = r.get("fields")
            if isinstance(fl, list):
                for f in fl:
                    fm[f.get("path")] = f.get("value")
            else:
                fm = dict(fl or {})
            out.append({"formid": r["formid"], "editorid": r.get("editorid"), "fields": fm})
    assert len(out) == 22, "expected all 22 ash weathers, got %d: %s" % (
        len(out), sorted(r["editorid"] for r in out))
    return out

def rgba(tok):
    if tok is None:
        return None
    m = C4.match(str(tok))
    if not m:
        return None
    v = tuple(int(x) for x in m.groups())
    return v if all(c <= 255 for c in v) else None

def lum(rgb):
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

def gated(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360.0
    return s >= 0.08 and (h <= 45.0 or h >= 300.0)

def tone(rgb):
    L = lum(rgb)
    out = tuple(min(255, max(0, int(round(L + (c - L) * K)))) for c in rgb)
    assert abs(lum(out) - L) <= 1.5, (rgb, out)
    return out

def hue_of(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    return colorsys.rgb_to_hsv(r, g, b)[0] * 360.0

def self_test():
    # brightness must hold exactly on the round-3 problem children
    for src in [(32, 11, 5), (71, 35, 35), (91, 30, 22), (200, 60, 40)]:
        out = tone(src)
        assert abs(lum(out) - lum(src)) <= 1.5, (src, out)
        if max(src) != min(src) and max(out) != min(out):
            assert abs(hue_of(src) - hue_of(out)) <= 12.0, (src, out, hue_of(src), hue_of(out))
    print("self-test OK: luminance held, hue held on dark reds")

def candidates(rec):
    fm = rec["fields"]
    for w in WHOLE:
        for q in QUADS:
            p = "%s.%s" % (w, q)
            v = rgba(fm.get(p))
            if v:
                yield p, w, q, v
    for q in QUADS:
        for d in DIRS:
            p = "DirectionalAmbientLightingColors.%s.%s" % (q, d)
            v = rgba(fm.get(p))
            if v:
                yield p, "DALC", q, v
    i = 0
    while True:
        base = "Clouds[%d]" % i
        if not any(k.startswith(base) for k in fm):
            break
        en = str(fm.get(base + ".Enabled", "True"))
        for q in QUADS:
            v = rgba(fm.get("%s.Colors.%s" % (base, q)))
            if v is None:
                continue
            try:
                a = float(str(fm.get("%s.Alphas.%s" % (base, q), "0")))
            except ValueError:
                a = 0.0
            if en == "True" and a > 0.0:
                yield "%s.Colors.%s" % (base, q), "Clouds", q, v
        i += 1

def census():
    per_family = {}
    day_examples = []
    for rec in load():
        for p, fam, q, v in candidates(rec):
            rgb, _ = v[:3], v[3]
            if gated(rgb):
                per_family.setdefault(fam, [0, 0, 0, 0])[QUADS.index(q)] += 1
                if q == "Day" and fam in ("SkyUpperColor", "SkyLowerColor", "FogFarColor", "SunlightColor", "Clouds") and len(day_examples) < 12:
                    day_examples.append((rec["editorid"], p, rgb))
    print("gated (red) colors per family [Sunrise, Day, Sunset, Night]:")
    for fam in sorted(per_family, key=lambda f: -sum(per_family[f])):
        print("  %-22s %s  total %d" % (fam, per_family[fam], sum(per_family[fam])))
    print("sample DAY reds:")
    for eid, p, rgb in day_examples:
        print("  %-30s %-28s %s" % (eid[:30], p, "%d,%d,%d" % rgb))

def ops():
    operations, ledger = [], {}
    for rec in load():
        entries = []
        for p, fam, q, v in candidates(rec):
            rgb, alpha = v[:3], v[3]
            if not gated(rgb):
                continue
            new = tone(rgb)
            if new == rgb:
                continue
            operations.append({"formid": rec["formid"], "field_path": p, "verb": "Set",
                               "value": "%d,%d,%d,%d" % (new + (alpha,))})
            entries.append("%s: %d,%d,%d -> %d,%d,%d" % ((p,) + rgb + new))
        ledger[rec["editorid"]] = entries
    with open(OUT + r"\ops_round4.json", "w") as f:
        json.dump(operations, f, separators=(",", ":"))
    with open(OUT + r"\TONE-LEDGER-round4-solstheim.json", "w") as f:
        json.dump(ledger, f, indent=1)
    print("ops: %d" % len(operations))
    for eid in ledger:
        print("  %-36s %d" % (eid, len(ledger[eid])))

if __name__ == "__main__":
    self_test()
    {"census": census, "ops": ops}[sys.argv[1]]()
