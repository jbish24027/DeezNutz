#!/usr/bin/env python3
"""Solstheim ash-weather tone-down, round 3 of the Astralite Dawn Warmth series.

Same math as round 2 (dawn_tone_r2.py), verified against TONE-LEDGER-round2.json anchors:
  new_c = round_half_even(max_channel - (max_channel - c) * STRENGTH)
which is exactly: V (max channel) byte-identical, hue preserved, S -> S*STRENGTH.

Modes:
  analyze  - hue/sat census of the authored colors (choose the gate from data)
  ops      - emit bulk_apply operations JSON + ledger, applying the gate
"""
import json, re, sys, colorsys

STRENGTH = 0.25  # target strength = 25% of authored saturation. NEVER add hue shifts.

SRC = r"C:\Users\User\.claude\projects\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\tool-results\mcp-housecarl-housecarl_batch_record_detail-1787247574711.txt"
OUT_DIR = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\9365d3db-dff4-4ffd-859f-d3cb4c9270cd\scratchpad"

QUADRANTS = ["Sunrise", "Sunset", "Night"]  # treated quadrants (round 2 = Sunrise/Sunset; user flagged night too)
DIRS = ["DirectionalXPlus", "DirectionalXMinus", "DirectionalYPlus",
        "DirectionalYMinus", "DirectionalZPlus", "DirectionalZMinus"]

def load():
    raw = open(SRC, encoding="utf-8", errors="replace").read()
    start = raw.find("{")
    doc = json.loads(raw[start:raw.rfind("}") + 1])
    recs = doc["records"] if isinstance(doc, dict) else doc
    out = []
    for r in recs:
        fields = r.get("fields")
        # fields may be list of {path,value} or dict
        fmap = {}
        if isinstance(fields, list):
            for f in fields:
                fmap[f.get("path") or f.get("field")] = f.get("value")
        elif isinstance(fields, dict):
            fmap = dict(fields)
        out.append({"formid": r.get("formid"), "editorid": r.get("editorid"),
                    "winner": r.get("winner"), "fields": fmap})
    return out

COLOR_RE = re.compile(r"(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")

def parse_color(tok):
    if tok is None:
        return None
    m = COLOR_RE.search(str(tok))
    if not m:
        return None
    rgb = tuple(int(x) for x in m.groups())
    if all(0 <= c <= 255 for c in rgb):
        return rgb
    return None

def hsv(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360.0, s, v

def tone(rgb):
    mx = max(rgb)
    return tuple(int(round(mx - (mx - c) * STRENGTH)) for c in rgb)

def color_paths(fmap):
    """yield (path, rgb) for every treated-candidate color present in fmap."""
    for q in QUADRANTS + ["Day"]:
        for d in DIRS:
            p = "DirectionalAmbientLightingColors.%s.%s" % (q, d)
            c = parse_color(fmap.get(p))
            if c is not None:
                yield p, q, c
        p = "FogNearColor.%s" % q
        c = parse_color(fmap.get(p))
        if c is not None:
            yield p, q, c

def self_test():
    # anchors from TONE-LEDGER-round2.json (round-2 ground truth)
    anchors = [((105, 88, 205), (180, 176, 205)),
               ((50, 60, 88), (78, 81, 88)),
               ((71, 89, 141), (124, 128, 141)),
               ((137, 96, 124), (137, 127, 134))]
    for src, want in anchors:
        got = tone(src)
        assert got == want, "self-test FAIL %s -> %s wanted %s" % (src, got, want)
    print("self-test OK: 4/4 round-2 anchors reproduced")

def analyze():
    recs = load()
    print("loaded %d records" % len(recs))
    lines = []
    band_hist = {}
    for r in recs:
        per_q = {}
        for p, q, c in color_paths(r["fields"]):
            h, s, v = hsv(c)
            per_q.setdefault(q, []).append((p.split(".")[-1] if "Fog" not in p else "FogNear", c, h, s, v))
            if q != "Day" and s >= 0.08:
                bucket = int(h // 20) * 20
                band_hist[bucket] = band_hist.get(bucket, 0) + 1
        lines.append("== %s (%s)" % (r["editorid"], r["formid"]))
        for q in QUADRANTS + ["Day"]:
            for name, c, h, s, v in per_q.get(q, []):
                lines.append("  %-7s %-8s %-13s H=%5.1f S=%.3f V=%.2f" %
                             (q, name, "%d,%d,%d" % c, h, s, v))
    open(OUT_DIR + r"\census.txt", "w").write("\n".join(lines))
    print("full census -> census.txt")
    print("hue histogram of S>=0.08 colors in Sunrise/Sunset/Night (bucket:count):")
    for k in sorted(band_hist):
        print("  %3d-%3d: %d" % (k, k + 20, band_hist[k]))
    # summary of what a red gate would catch per quadrant
    for lo, hi in ((0, 45), (315, 360)):
        pass
    caught = {q: 0 for q in QUADRANTS}
    total = {q: 0 for q in QUADRANTS}
    for r in recs:
        for p, q, c in color_paths(r["fields"]):
            if q == "Day":
                continue
            total[q] += 1
            h, s, v = hsv(c)
            if s >= 0.08 and (h <= 45 or h >= 315):
                caught[q] += 1
    for q in QUADRANTS:
        print("gate(H<=45 or H>=315, S>=0.08) %s: %d/%d colors" % (q, caught[q], total[q]))

COLOR4_RE = re.compile(r"^\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*$")

def gated(rgb):
    h, s, v = hsv(rgb)
    return s >= 0.08 and (h <= 45.0 or h >= 300.0)

def ops():
    recs = load()
    operations, ledger = [], {}
    per_rec = []
    for r in recs:
        entries = []
        for q in QUADRANTS:
            paths = ["DirectionalAmbientLightingColors.%s.%s" % (q, d) for d in DIRS]
            paths.append("FogNearColor.%s" % q)
            for p in paths:
                tok = r["fields"].get(p)
                if tok is None:
                    continue
                m = COLOR4_RE.match(str(tok))
                if not m:
                    raise SystemExit("unparseable color token %r at %s %s" % (tok, r["editorid"], p))
                rgba = tuple(int(x) for x in m.groups())
                rgb, alpha = rgba[:3], rgba[3]
                if not gated(rgb):
                    continue
                new = tone(rgb)
                if new == rgb:
                    continue
                assert max(new) == max(rgb), "V changed at %s %s" % (r["editorid"], p)
                operations.append({"formid": r["formid"], "field_path": p, "verb": "Set",
                                   "value": "%d,%d,%d,%d" % (new + (alpha,))})
                entries.append("%s: %d,%d,%d -> %d,%d,%d" % ((p,) + rgb + new))
        ledger[r["editorid"]] = entries
        per_rec.append((r["editorid"], len(entries)))
    with open(OUT_DIR + r"\ops_round3.json", "w") as f:
        json.dump(operations, f, separators=(",", ":"))
    with open(OUT_DIR + r"\TONE-LEDGER-round3-solstheim.json", "w") as f:
        json.dump(ledger, f, indent=1)
    print("records: %d   ops: %d" % (len(recs), len(operations)))
    for eid, n in per_rec:
        print("  %-36s %d edits" % (eid, n))
    print("wrote ops_round3.json + TONE-LEDGER-round3-solstheim.json")

if __name__ == "__main__":
    self_test()
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        analyze()
    elif len(sys.argv) > 1 and sys.argv[1] == "ops":
        ops()
