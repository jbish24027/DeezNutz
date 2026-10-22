# Authoria - RMF Purple Retint — LOCKED 2026-08-12

> ## ⚠ 2026-08-16: THE HUE-ROTATION MODEL BELOW IS NOT TRUE ANY MORE
> Measured directly off the user's screenshots (overwrite\Root\screenshots,
> 07:50-07:51) against what is painted in the winning textures:
>
> | Texture | Painted | RENDERED |
> |---|---|---|
> | blue_lupin01 flowers | H 288.0  S 0.653 | **H ~284**  S 0.75 |
> | Lavender buds        | H 304.1  S 0.500 | **H ~303**  S 0.61-0.66 |
>
> **Hue transfer is essentially IDENTITY. Only SATURATION is pushed, by ~+0.12.**
> There is no dead band, no -90 deg rotation, no per-material hue map in play for
> these flowers. The "paint H300 to get purple" doctrine in the sections below
> produced pink flowers for a simple reason: H288 and H304 ARE magenta-violet
> hues, so they rendered as magenta-violet. Three rounds were lost compensating
> for a rotation that was not happening.
>
> **METHOD, use this first:** the screenshots are on disk. Measure the rendered
> hue from them and compare to the painted hue before theorising. That is one
> command and it settles the question; extrapolating from an old calibration grid
> does not. Whatever the E11 pipeline did when that grid was made, verify it is
> still doing it before you trust it.
>
> Everything below is kept as history. Treat its aim points as SUSPECT.

## CURRENT aim points for the two plants re-derived under the identity model (2026-08-16)

| Plant | Files | Painted | Status |
|---|---|---|---|
| Lavender | Lavender.dds, LavenderSUM.dds | window H285-335 S>0.20 -> **H272, S 0.30, V unchanged**. Petals RGB ~(77,63,90). | **USER-APPROVED — "the lavender is perfect". Do not repaint.** |
| Blue Mountain Flower | blue_lupin01.dds + blue_lupin01_sk.dds | **08-17 06:45 FINAL STATE = r11 restored** (diffuse H205 S0.48 hash EFED6FB5, sk H205 S0.40 hash B605DDB3). Five variants (r11, dark sk, r12 deep blue + sk, magenta sk) and the Soft_Lighting-flag mesh mod all render identically: cream/yellow whenever Effects 11 is on and direct light hits the spikes, blue when Effects 11 is off or in shade/overcast. The yellow saturation tracks the painted blue saturation. Every E11 post switch was tried live with no change. **The flower files are innocent - do not repaint again.** Next step is a RenderDoc capture or an upstream Effects 11 report (frame pairs CS_2026-08-17_04-17-22/26 and 04-17-41/44). |
| Blue Mountain Flower (subsurface) | blue_lupin01_sk.dds | **r12 petal-darkening (08-16 14:45) had NO visible effect (user: sunny Morthal still cream, CS_2026-08-17_04-17-44) and was REVERTED 08-17 04:2x to the r11 file** (hash B605DDB3..., from `_backups\2026-08-16 - lupin sk pre-petal-darken`). The r12 source PNG stays in `_source-pngs-locked` for reference only. | Why it could not work: Effects 11 does not implement `[VEGETATION]` at all (its source registers ENVIRONMENT/SKY/PARTICLE/RAIN/FIRE/VOLUMETRIC*/SUN* only), and CS's own soft lighting multiplies the light by the petal albedo, so no sk value can turn blue into cream. Live suspects now: E11 bloom (enbbloom.fx Day Saturation 2.15, enbeffect.fx Bloom Blending Linear Blend Amount 0.5 Day in Clear) and Astralite's orange low sun (SunlightColor Sunrise/Sunset 255,124,45). |

Blue lupin round 1 was H205 **S 0.25** V x1.30 and the user reported it as "basically
white". Value was NOT the problem — "light" was correct — S 0.25 simply leaves no
chroma once the petal is lit. Round 2 keeps the lightness and puts the blue back.
Note the subsurface map is deliberately lighter and less saturated than the diffuse,
which is how the r5 original was built too (V 0.710 vs 0.486).

Saturation is painted ~0.10 BELOW target on purpose: the pipeline adds ~+0.12 back.

Backups: `_backups\2026-08-16 - lavender+lupin pre-babyblue` (the r5 state) and
`_backups\2026-08-16 - lupin pre-satraise` (the too-white round 1).


User-approved final calibrated colors, tuned over 5 feedback rounds against the
Effects 11 / Soul Core rendering pipeline (which mangles painted hues ~215-295).
Do not repaint these without re-running the feedback loop with the user.

## Locked aim points (painted values -> what they RENDER as in game)
| Plant | Files | Painted | Renders |
|---|---|---|---|
| Lavender buds        | Lavender.dds, LavenderSUM.dds (star region x374-501 y436-561) | H304 S0.50 V=0.27+0.28v | muted natural lavender |
| Blue Mountain Flower | blue_lupin01.dds, blue_lupin01_sk.dds | H288 S>=0.65 V x0.85 | natural blue |
| Purple Mountain Flower | periwinkle.dds, periwinkle_sk.dds | H300 S<=0.60 V x0.85 | soft purple (PARKED by user) |
| Thistle / Nightshade | thistle01, NightShade, nightshade01 | H300 window remap | unverified by user |
| Witchy lupines       | lupine.dds, lupine2.dds | H300 window remap | unverified by user |
| Flax / blue grass    | Flower_LinumLewisii_Blue, LinumLewisiiDrJ, Flower_Lupine_Blue | H200 window remap | unverified by user |

## Rebuild pipeline (if ever needed)
1. Decode ORIGINAL source dds (from the providing mod, NOT this mod) with texconv -ft png (run texconv from PowerShell - it fails under bash on bracketed paths).
2. Python/PIL HSV remap per the table above (cool-hue window 185-310 for petal remaps).
3. Encode: texconv -f BC7_UNORM -m 0 (PowerShell), replace the dds here.

## Why this mod exists
The Effects 11 (CS 1.8) + Silent Horizons 2 + Soul Core pipeline hue-rotates
painted colors in the ~215-295 band (blue->green, violet->cyan). Root cause is
upstream in E11's compositing (all preset shaders decrypted and exonerated;
evidence bundle in the Claude session memory). If E11 ever fixes this, this
mod's colors will render WRONG (over-rotated) - retire it then.

## Addendum 2026-08-12: dust + driftwood
| Asset | Files | Change | Why |
|---|---|---|---|
| Wagon/road dust particles | textures\effects\dusttiny(.dds/_dim/_dimmer) | saturation x0.15, V x0.92 | tan dust was hue-shifted to yellow-green by the pipeline's +25deg warm shift; grey dust is shift-proof |
| Coastal driftwood | textures\TBS_Mods\coastdriftwood.dds | V x0.72, S x0.85 | bleached-white logs clashed with lush summer tundra; now weathered grey-brown |

## Revision 2026-08-16 lavender + blue lupin — RESTORED FROM THE r5 SOURCES
The 08-15 saturation-only rebuild below was NOT faithful. Compared against the
kept sources `_source-pngs-locked\*_r5.png` (the round-5 images, 2026-08-13): the
flower medians matched (H 304.0/S 0.505 vs H 302.9/S 0.500) but **55,995 pixels on
blue_lupin01 still differed**, because round 6 had repainted a WIDER cool-hue window
than my narrow [270,310] restore touched. Lesson: when a round's source PNG is kept,
INSTALL IT, don't reconstruct it.

Installed `Lavender_r5.png`, `LavenderSUM_r5.png`, `blue_lupin01_r5.png`,
`blue_lupin01_sk_r5.png` directly -> BC7_UNORM, byte-size identical to what they
replaced. Verified on disk: Lavender H 304.1 / S 0.500 / V 0.353, blue_lupin S 0.654.
These now match the "Locked aim points" table at the top of this file exactly.
Backup of the pre-restore state: `_backups\2026-08-16 - lavender+lupin pre-r5-restore`.

IF STILL PINK: the texture is then EXONERATED — it is byte-faithful to the state the
user approved on 08-12 — and the cause is downstream of the texture. Ruled out so far:
`hdrAutoDetected` is false (not the auto-HDR trap). CS SettingsUser.json changed only
two things since 08-14: Vanilla Fresnel Enable 1->0 (the deliberate hair-specular fix)
and the Advanced Skin block. No backup exists from before 08-12, so the 12->14 Aug
window is not diffable. NEXT STEP is NOT another hue guess — console-click the plant
with More Informative Console first and confirm which mesh and texture it actually
uses. The deathbell round-1 detour came from skipping exactly that check.

## Revision 2026-08-15 lavender + blue mountain flower — superseded by the r5 restore
User: "blue mountain flowers went pink, as did lavender", with screenshots.

NOT a regression from that day's deathbell work — those files were last written
2026-08-14 04:41 and were never touched again. Measured what was actually on disk:
Lavender bud region H 303.4 / **S 0.421** / V 0.353, and blue_lupin01 flowers
H 288.0 / **S 0.555**. That is round 6 ("paler"), not the round 4-5 values the user
approved with "hues are MUCH better". Round 6 lowered saturation on these two and
**no verdict was ever recorded for them** — round 7 only covered nightshade, thistle
and the maple. So they have been sitting in an unverified paler state since 08-14
and simply had not been looked at until now.

Why paler went pink: round 6 pushed both into the mid-saturation band this file
already warns about — "the transform mangles mid-saturation cool colors; full
saturation passes through" — and the round-3 note "H315 S0.62 -> PINK" is the same
failure. Low saturation near H300 lands pink.

Reverted to the last user-approved values. Saturation ONLY; hue and value are
identical between rounds 5 and 6, so neither was touched.

| Plant | Files | Restored |
|---|---|---|
| Lavender buds | Lavender.dds, LavenderSUM.dds | S 0.421 -> **0.50** (round 5). H 303 and V 0.353 unchanged. |
| Blue Mountain Flower | blue_lupin01.dds, blue_lupin01_sk.dds | S floor 0.555 -> **0.65** (round 5). H 288 and V unchanged. |

Notes:
- Safe to apply to the round-6 file rather than rebuilding from source: both specs
  are ABSOLUTE (a set value / a floor), so set(set(x,0.42),0.50) == set(x,0.50) and
  floor(floor(x,0.55),0.65) == floor(x,0.65). No compounding.
- Non-flower pixels 0 altered, alpha bit-identical, byte-size identical to the
  round-6 files, all four verified.
- Round 6 dds backed up: C:\1. AUTHORIA\_backups\2026-08-15 - lavender+lupin round6 pre-satrestore
- LESSON: round 6 changed four plants at once and only two got verdicts. Do not
  ship a "paler/darker" pass on several plants in one round without getting a
  per-plant verdict — an unverified change hides for days.

## Revision 2026-08-15 deathbell round 3 (CURRENT — awaiting user verify)
User verdict on round 2, with screenshot: still blue, just darker.

**Round 2's premise was WRONG and the correction matters.** Dropping V did not move
the rendered hue at all — it only darkened it (bright blue at V 0.57 became navy at
V 0.27). On the deathbell material, painted H302 renders BLUE at any value. The
"bright renders blue, dark renders purple" reading of the Lavender note does not
generalise. What DOES hold is this file's own older warning: **the transfer is
PER-MATERIAL.** The calibration grid was painted on the Lavender material; deathbell
is a different material and does not reach purple by hue at all. Two failed rounds
came from reusing another plant's map instead of calibrating this one.

Fix: stop fighting the rotation. The user asked for "grey/black purple" — and grey
is ROTATION-PROOF, because at low saturation there is almost no chroma left to
rotate. Whatever the pipeline does to the hue, the petals read as dark grey.

| Plant | Files | Painted |
|---|---|---|
| Deathbell — unverified | DeathBell02.dds, DeathBell02SUM.dds | window H185-300 S>0.15 -> H302, S **clamped to 0.30** (a clamp, not a floor — that is what drives it to grey), V x0.30. Petals -> RGB ~(55,38,54), R-B spread 1. |
| Deathbell winter — unverified | DeathBell02WIN.dds | same window, S>0.10 -> H302, S clamp 0.22, V x0.55. Petals -> ~(90,70,89). |

The purple now comes from the LIGHT, not the texture. The light's magenta renders
correctly — the pink pool in the user's screenshot proves the light channel is not
subject to the rotation. Authoria_Glow_Deathbell was re-shaped from a broad dim wash
to a concentrated glow: radius 200 -> **150**, fade 0.9 -> **2.5**.

Notes:
- Rebuilt from the ORIGINAL Seasonal Landscapes decode. No compounding across rounds.
- Leaves 0 px altered, alpha bit-identical, BC7_UNORM 4096 13 mips, byte-size
  identical to source, verified on all three installed files.
- Round 2 dds backed up: C:\1. AUTHORIA\_backups\2026-08-15 - deathbell round2 pre-grey
- IF A FUTURE ROUND IS NEEDED: do not guess another hue. Paint a calibration grid on
  the DEATHBELL atlas specifically and have the user screenshot it, exactly as the
  2026-08-12 lavender calibration did. Reusing another plant's map has now failed twice.

## Revision 2026-08-15 deathbell round 2 (superseded by round 3)
User verdict on round 1, with an in-game screenshot: petals came out BLUE, and
"it's a bit too bright right now"; wants grey / black-purple.

Diagnosis — this is a REAL ADDITION to the transfer map, worth keeping:
at H~300 the pipeline is VALUE-DEPENDENT. Bright resolves to BLUE, dark resolves
to PURPLE. The evidence was already in this file and I did not join it up:
round-3 notes record "Lavender H300 bright -> BLUE neon", and nightshade renders
correct purple only because it is painted near-black (V x0.38). Round 1 kept
deathbell at V x0.80 (V 0.573) to preserve the flower's brightness — that single
choice is what made it blue. So the user's two complaints, wrong hue and too
bright, have ONE cause and ONE fix.

Fix: nightshade's exact user-approved recipe, applied verbatim.

| Plant | Files | Painted |
|---|---|---|
| Deathbell — unverified | DeathBell02.dds, DeathBell02SUM.dds | window H185-300 S>0.15 -> H302, S floor 0.70, **V x0.38**. Petals H 246.7 -> 302.3, S 0.534 -> 0.700, V 0.714 -> 0.271, petal RGB ~(69,21,68) — near-black plum. |
| Deathbell winter — unverified | DeathBell02WIN.dds | same window, S>0.10 -> H302, S floor 0.40, V x0.50. Petals -> ~(82,49,80). |

Notes:
- Rebuilt from the ORIGINAL Seasonal Landscapes decode, never re-transformed from
  round 1 — no compounding.
- Leaves 0 px altered, alpha bit-identical, BC7_UNORM 4096 13 mips, byte-size
  identical to source, in all three files.
- Round 1 dds backed up: C:\1. AUTHORIA\_backups\2026-08-15 - deathbell round1 pre-darken
- The plant is now deliberately very dark. Its Light Placer glow was strengthened
  to compensate (Authoria_Glow_Deathbell: radius 110 -> 200, fade 0.4 -> 0.9,
  colour deepened to 200,55,190). Tune brightness THERE, not by raising V here —
  raising V is what turns it blue again.
- Console-confirmed live record: TreeFloraDeathBell01SUM, a **TREE** record (not
  Flora) from Seasonal Landscapes.esp, model FloraDeathBell01SUM.nif.

## Revision 2026-08-15 deathbell round 1 (superseded by round 2)
User: "the deathbell is supposed to be purple but is green ... similar to the nightshade color".

Diagnosis: textbook dead-band victim, and the reason it was missed is an asset-identity
trap. The obvious file `deathbell01.dds` is NOT what renders. Every winning deathbell
mesh — floradeathbell01.nif, floradeathbell01SUM.nif, and deathbell01.nif (whose winner
is the ParallaxGen output) — reads the **DeathBell02** family instead. Measured on the
real atlas: petals sit at H 246.8 (95% inside H 235-255), S 0.533, V 0.714. That is dead
centre of the painted-240 catastrophic flip (-110 deg) that renders GREEN.

| Plant | Files | Painted |
|---|---|---|
| Deathbell — unverified | DeathBell02.dds, DeathBell02SUM.dds | window H185-300 S>0.15 -> H302, S floor 0.70, V x0.80. Petals H 246.8 -> 302.0, S 0.533 -> 0.700, V 0.714 -> 0.573, new petal RGB ~(146,44,142). |
| Deathbell winter — unverified | DeathBell02WIN.dds | same window, S>0.10 -> H302, S floor 0.32, V untouched. Winter petals stay muted under snow (S 0.239 -> 0.320). |

Notes:
- H302 is the nightshade aim point, per the user's "similar to the nightshade color".
  Deathbell deliberately keeps far more value than nightshade (V x0.80 vs nightshade's
  x0.38) — nightshade is meant to read near-black, deathbell has to stay a readable bell.
  If the user wants it deeper, lower the V multiplier; that is the only knob to touch.
- Leaves and stems verified UNCHANGED: 0 pixels altered outside the petal window, in all
  three files. Alpha channel bit-identical (alpha-tested flora depends on it).
- Encoded BC7_UNORM 4096x4096 13 mips, byte-size identical to the originals (22369796).
- deathbell01.dds / deathbell01SUM.dds were left alone ON PURPOSE — no winning mesh
  reads them. Do not "fix" them; that was the wrong-asset trap.
- Source PNGs at _source-pngs-locked\DeathBell02*_deathbell_round1_H302.png.

## Revision 2026-08-15 round 9
User verdict on round 8: "Val Serano trees I'd like much less bright."

Diagnosis: the atlas was never bright, it was near-monochromatic. Median V was only
0.227, but S was 0.982 with G=0.012 / B=0.020 - the red channel carried everything.
Nothing in the scene (fog, distance, dim weather) can desaturate a pure-channel red,
so it stayed screaming crimson while everything around it washed out.

| Plant | Files | Painted |
|---|---|---|
| Val Serano red maple - unverified | treefloweringbranch02.dds + _SUM + _SPR in this hub | HSV scale on RGB only: S x0.70, V x0.62. Measured V p50 0.227 -> 0.141, S p50 0.982 -> 0.676. Hue untouched, alpha copied through untouched. |

Notes:
- All three files are byte-identical (verified md5 before AND after). The base
  treefloweringbranch02.dds is NEW here - the AUT meshes read it straight from
  AX ValSerano - Textures.bsa, so without a loose override autumn would have stayed
  bright while spring/summer darkened.
- WIN (winter) still left as authored.
- Encoded BC7_UNORM 2048x2048 12 mips. The originals were DXT5; BC7 is the same file
  size with better alpha precision. Alpha-test mask at the mesh threshold (130) shifted
  by 0.026% - edge quantization only.
- Source PNG kept at _source-pngs-locked\treefloweringbranch02_round9_medium.png.
  Two alternates were built and NOT installed: mild S x0.80 V x0.75, strong S x0.62 V x0.50.
  Strong drifts toward brown-mauve and loses the maple identity.
- KNOWN GAP: Authoria - TexGen Output holds maple billboards baked from the OLD bright
  atlas (redmaplelarge/small/tiny_spr_*.dds). Distant tree LOD stays bright until
  TexGen + DynDOLOD are rerun. Deliberately not touched - generator output.
- Round 8 dds backed up: C:\1. AUTHORIA\_backups\2026-08-15 - RMF round9 pre-darken maple

## Revision 2026-08-14 round 8
Round 7 verdicts: nightshade APPROVED-LOCKED; thistle "better but a bit too pigmented";
maple green "still just too much" + user wants RED leaves year round.
| Plant | Files | Painted |
|---|---|---|
| Nightshade — **LOCKED, user-verified** | NightShade.dds, nightshade01.dds | petal window H220-340 S>0.15 -> H302 S>=0.70 V x0.38 (near-black purple) |
| Thistle — unverified | thistle01.dds | bloom window H240-340 S>0.12 -> H300, S clamped [0.40, 0.58], V x0.80 |
| Val Serano red maple — SUPERSEDED by round 9 | treefloweringbranch02_SUM.dds + _SPR.dds in this hub | REPLACED with the mod's ORIGINAL red autumn atlas (from AX ValSerano - Textures.bsa) -> red leaves in spring+summer+autumn; WIN (winter) left as authored. The round-7 darkened-green approach is retired. If red reads too bright under CS, round 9 = darken the red atlas. |
Round 6 dds backed up: C:\1. AUTHORIA\_backups\2026-08-14 - RMF round6 pre-round7

## Revision 2026-08-12 round 6 (supersedes table above where they overlap)
| Plant | Painted |
|---|---|
| Nightshade (NightShade, nightshade01) | H306 S>=0.65 V x0.75 (deeper purple) |
| Lavender buds | H304 S0.42 V=0.27+0.28v (paler) |
| Blue Mountain Flower (blue_lupin01+_sk) | H288 S>=0.55 V x0.85 (paler) |
| Witchy asters (AsterAlpinusDrJ, Aster_OJ, Aster_SC, ScabiosaDrJ) | cool window 170-310 -> H300 S>=0.55 (were teal dead-band victims) |
