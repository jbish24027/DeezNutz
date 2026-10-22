#!/usr/bin/env python3
"""
ROUND 6 (2026-08-22) - VOLUMETRIC LIGHTING (god-ray / atmospheric fill) CHROMA CUT.

WHY THIS ROUND EXISTS
---------------------
Rounds 2-5 dimmed the WEATHER colour surface (sky, clouds, both fogs, sunlight,
sun, glare, stars, water, ambient/DALC). Round 5 took that game-wide to 10%.
Every one of those rounds DELIBERATELY EXCLUDED the shared god-ray VOLI records
("would need duplicate+repoint" - round 4 watch item).

That exclusion was the residual complaint. After round 5 the weather behind the
player was near-monochrome while a SECOND, independent colour layer - the
volumetric light filling the exterior air - was still running at 57-100%
saturation, three-quarter contribution, intensity 12, density 0.9. Rose and hot
pink at sunrise/sunset, saturated orange/gold/yellow, tinted green/blue/purple
fog. That is what was still painting mornings and evenings.

The old blocker (records are SHARED across weathers, so you cannot dim the
mainland without dimming Solstheim) stopped mattering the moment the user chose
a game-wide blanket. Where a record is shared with a REALM or QUEST FX weather
whose colour is deliberately kept, a dimmed DUPLICATE is minted and only the
rotation weathers are repointed.

TRANSFORM (identical to round 4/5, per [[color-strength-not-tone]])
------------------------------------------------------------------
    L  = 0.2126*R + 0.7152*G + 0.0722*B        (Rec.709 luminance)
    c' = L + (c - L) * K,  K = 0.10

Luminance EXACT, hue locked, chroma to 10% of authored. No warm/cool nudges.
Verified: 0 luminance mismatches across all 18 records (max delta 2.5e-08),
no channel clamped. God rays stay exactly as bright; they stop being coloured.

SCOPE
-----
16 records dimmed IN PLACE (override in this patch).
 2 records DUPLICATED dimmed + 4 rotation weathers repointed, so the realm /
   quest FX that share them keep their authored colour:
     AUTH_LAM_GreenVL_Dim10  <- LAM_GreenVL  (Apocrypha keeps its green)
     AUTH_LAM_BloodVL_Dim10  <- LAM_BloodVL  (DLC1Eclipse, MQ206,
                                              BloatedMansGrotto keep their red)
Already neutral, untouched: LAM_NoVL, LAM_StormVL, LAM_FogVL, LAM_DayVL,
LAM_StormVL_Night, LAM_PureVL, LAM_BlizzardVL, the three Helios interior VOLIs.
Untouched by design: every NAT-ENB VOLI (NAT's weathers are referenced by ZERO
regions and ZERO climates - they never load), the ECSS realm VOLIs, vanilla
Update.esm/Dragonborn.esm VOLIs.

KNOWN SPILLOVER (accepted, reported to the user)
------------------------------------------------
18 realm / quest / Gray-Cowl weathers borrow at least one of the 16 in-place
records for one or more time slots, so those slots dim too. Their OWN sky,
cloud and fog colours are untouched (round 5 excluded them). Fix if ever wanted:
mint dimmed duplicates the same way and repoint only the rotation weathers.

IMAGESPACES ARE NOT INVOLVED - audited 2026-08-22: tint amount 0, cinematic
saturation 1.0 on the live set. Do not go looking there again.

DIAL: K below. Re-running needs the records re-forwarded to authored first
(the .bak-pre-voli-20260822 backup is the pre-round-6 state).
"""

K = 0.10

def lum(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def dim(r, g, b, k=K):
    L = lum(r, g, b)
    return tuple(min(1.0, max(0.0, L + (c - L) * k)) for c in (r, g, b))

# editorid -> (formid, authored R, G, B, disposition)
AUTHORED = {
    "LAM_YellowVL":     ("000810:Astralite Weathers.esp", 0.69411767, 0.56078434, 0.0,         "in-place"),
    "LAM_OrangeVL":     ("000813:Astralite Weathers.esp", 1.0,        0.4509804,  0.0,         "in-place"),
    "LAM_RoseVL":       ("00085C:Astralite Weathers.esp", 1.0,        0.23529412, 0.23529412,  "in-place"),
    "LAM_NightVL":      ("000811:Astralite Weathers.esp", 0.03529412, 0.05490196, 0.101960786, "in-place"),
    "LAM_PinkVL":       ("000866:Astralite Weathers.esp", 1.0,        0.36078432, 0.8039216,   "in-place"),
    "LAM_StormVL_Red":  ("000879:Astralite Weathers.esp", 0.75686276, 0.30588236, 0.30588236,  "in-place"),
    "LAM_PeachVL":      ("00086F:Astralite Weathers.esp", 1.0,        0.54901963, 0.43137255,  "in-place"),
    "LAM_FogVLNight":   ("00085E:Astralite Weathers.esp", 0.078431375,0.1254902,  0.1764706,   "in-place"),
    "LAM_FogVL_Green":  ("00085F:Astralite Weathers.esp", 0.23529412, 0.2901961,  0.14509805,  "in-place"),
    "LAM_FogVL_Blue":   ("000861:Astralite Weathers.esp", 0.1882353,  0.22745098, 0.3647059,   "in-place"),
    "LAM_FogVL_Ourple": ("000860:Astralite Weathers.esp", 0.11372549, 0.09803922, 0.14117648,  "in-place"),
    "LAM_OurpleVL":     ("000868:Astralite Weathers.esp", 0.11372549, 0.09803922, 0.14117648,  "in-place"),
    "LAM_GoldVL":       ("00082D:Astralite ENB.esp",      1.0,        0.60784316, 0.0,         "in-place"),
    "LAM_FogVL_Gold":   ("00082A:Astralite ENB.esp",      1.0,        0.6666667,  0.0,         "in-place"),
    "LAM_FogVL_Purple": ("00082B:Astralite ENB.esp",      0.22745098, 0.19607843, 0.35686275,  "in-place"),
    "LAM_StormTealVL":  ("00082C:Astralite ENB.esp",      0.0,        0.37254903, 0.3882353,   "in-place"),
    "LAM_GreenVL":      ("000867:Astralite Weathers.esp", 0.24705882, 0.2784314,  0.14509805,  "duplicate"),
    "LAM_BloodVL":      ("000829:Astralite ENB.esp",      1.0,        0.11764706, 0.11764706,  "duplicate"),
}

# rotation weathers repointed to the dimmed duplicates (slot -> new record)
REPOINTS = {
    "SkyrimFogVT (10A7A7:Skyrim.esm)":                  ("Sunrise, Sunset",      "AUTH_LAM_GreenVL_Dim10"),
    "DLC02VolcanicAshTundra02_A (000840:Astralite ENB.esp)": ("Sunrise, Sunset", "AUTH_LAM_GreenVL_Dim10"),
    "DLC02VolcanicAsh03 (000831:Astralite ENB.esp)":    ("Sunrise, Sunset",      "AUTH_LAM_BloodVL_Dim10"),
    "DLC02VolcanicAsh04 (00083A:Astralite ENB.esp)":    ("Sunrise, Day, Sunset", "AUTH_LAM_BloodVL_Dim10"),
}

if __name__ == "__main__":
    import json, sys
    ledger = {"round": 6, "date": "2026-08-22", "K": K,
              "transform": "c' = L + (c - L) * K, L = Rec.709 luminance; hue + luminance locked",
              "records": {}, "repoints": REPOINTS}
    worst = 0.0
    for eid, (fid, r, g, b, how) in AUTHORED.items():
        n = dim(r, g, b)
        d = abs(lum(r, g, b) - lum(*n))
        worst = max(worst, d)
        ledger["records"][eid] = {
            "formid": fid, "disposition": how,
            "authored": [r, g, b], "dimmed": [round(x, 8) for x in n],
            "luminance": round(lum(r, g, b), 8), "luminance_delta": d,
        }
    ledger["max_luminance_delta"] = worst
    json.dump(ledger, open("TONE-LEDGER-round6-volumetric.json", "w"), indent=2)
    print("wrote TONE-LEDGER-round6-volumetric.json")
    print("records: %d   max luminance delta: %.2e" % (len(AUTHORED), worst))
