# Authoria - Patch - Astralite Dawn Warmth

## Round 6, 2026-08-22 — VOLUMETRIC LIGHTING (the god-ray / air fill) — LIVE, test pending

**ADDITIVE to round 5, not a replacement.** Round 5 left the weather colour
surface at 10% game-wide. The user came back with "still seeing some of that
misbalance, I want to castrate the mechanism doing it."

**Cause found:** there are TWO independent colour layers on exteriors. Rounds
2-5 only ever touched the weather one. The second is the VOLUMETRIC LIGHTING
(VOLI) records — the coloured light filling the outdoor air / god rays — and
every previous round EXCLUDED it on purpose ("shared god-ray VOLI would need
duplicate+repoint", round 4 watch item). It was still running at 57-100%
saturation, contribution 0.75, intensity 12, density 0.9: rose and hot pink at
sunrise/sunset, saturated orange/gold/yellow, tinted green/blue/purple fog.
Weather at 10% behind a colour layer at 100% is exactly the residual complaint.

The sharing objection died the moment the decision went game-wide.

**Transform:** identical to rounds 4/5 — c' = L + (c - L) * 0.10, L = Rec.709.
Luminance EXACT, hue locked, chroma to 10%. Verified 0 mismatches over 18
records (max delta 2.5e-08 as written to disk, no channel clamped). Brightness
of the god rays is unchanged; only the colour is gone. Mean saturation over the
first 12: 0.614 -> 0.097.

**Scope:** 16 records dimmed in place; 2 minted as dimmed DUPLICATES
(`AUTH_LAM_GreenVL_Dim10`, `AUTH_LAM_BloodVL_Dim10`) with 4 rotation weathers
repointed, so Apocrypha keeps its green and DLC1Eclipse / MQ206 /
BloatedMansGrotto keep their blood red. Already-neutral records untouched
(NoVL, StormVL, FogVL, DayVL, StormVL_Night, PureVL, BlizzardVL, Helios
interiors).

**Verified:** patch wins all 18; per-field readback exact; diff on LAM_RoseVL =
exactly 3 deltas (the 3 colour channels), nothing else disturbed; check_errors
0 dangling / 0 missing masters. Masters unchanged (Astralite Weathers.esp and
Astralite ENB.esp were already there). No wiring changes — same plugin, already
enabled and positioned.

**Two findings worth keeping:**
- **NAT-ENB's 24 weathers are DEAD.** Zero regions and zero climates reference
  them. NAT-ENB.esp is a master carrier only. Never patch them; never count
  them as a coverage hole again.
- **Imagespaces are NOT involved.** Audited the live set 2026-08-22: tint
  amount 0, cinematic saturation 1.0. Do not go looking there again.

**Known spillover (accepted):** 18 realm / quest FX / Gray-Cowl weathers borrow
at least one of the 16 in-place records for one or more time slots, so those
slots dim too. Their own sky/cloud/fog stay authored (round 5 excluded them).
If that ever reads wrong, mint dimmed duplicates the same way and repoint only
the rotation weathers.

**Dial:** K in `tone_round6_volumetric.py`. Full old->new table in
`TONE-LEDGER-round6-volumetric.json`. Pre-round-6 backup:
`Authoria - Patch - Astralite Dawn Warmth.esp.bak-pre-voli-20260822`.

## Round 5, 2026-08-20 — GAME-WIDE BLANKET (LIVE, test pending) — supersedes rounds 2 and 4

User: "riften exterior winter 7 am bright blue. im tired of these coloring
problems and i want a blanket across the game fix to dim any of this shit to
like 10%." Trigger case confirmed in data: SkyrimClearSN (the snow-region
clear that plays around Riften in SWF winter) had sunrise sky 16,26,95 and
day sky 54,83,186 — a strong blue the earlier dawn-only rounds never touched.

**What the patch now IS:** one uniform rule. Every weather in overworld
rotation — 146 records — was re-forwarded byte-authored from its source and
then EVERY color on it (sky upper/lower, horizon, near+far fog, ambient,
all 6 DALC directions + specular, sunlight, sun, sun glare, stars, moon
glare, sky statics, water multiplier, effect lighting, cloud-LOD, every
cloud layer with visible alpha) at ALL FOUR times of day was cut to **10%
chroma, luminance-locked, hue-locked** (c' = L + (c-L)x0.10, L = Rec.709).
No hue gate — red, blue, purple, gold, everything. 17,241 colors changed;
9,308 were already neutral (S < 0.08) and stayed byte-identical.

**Coverage** (`blanket_coverage.json`): derived from live data — every
weather referenced by the 97 overworld region weather lists (Tamriel, all
city worldspaces, Solstheim, Bruma via UWC, Wyrmstooth, Inigo's basin,
seasonal-framework swap regions) + the 6 overworld climates + all seasonal
twins. Sources: Astralite ENB 72, Helios_Astralite 64 (incl. 4 new FV
twins), Snowy Holds 8 (incl. 4 FV overworld weathers), Wyrmstooth patch 2.

**Deliberately NOT covered** (unchanged): realm/quest weathers (Sovngarde,
Soul Cairn, Apocrypha, Blackreach, Forgotten Vale interior, Shivering
Isles/ECSS, Blue Palace fogs incl. the Gray Cowl oasis fog, Skuldafn,
eclipse/quest FX); Lux's fake lighting weathers; Wet and Cold FX clones;
the paper-map weather (FWMF); the Authoria dragon-battle FX weathers; the
shared sunny-god-ray volumetric lights (would bleed into realms; separate
dial). The image spaces carry zero tint (verified round 4) — nothing to cut.

**Method:** forwards via houseCARL (4 calls, groups in blanket_coverage.json),
then ONE byte-level pass `tone_round5_blanket.py` — subrecord layout was
PROVEN against houseCARL dumps of 10 anchor records before writing (NAM0
slot map derived from data, not documentation — the documented order was
wrong at slot 2; DALC quadrant order proven uniquely; cloud colors
position-verified). Size-preserving byte writes only.

**Verify:** fresh houseCARL re-reads of 4 treated records = 880 colors
checked against computed expectations, 0 mismatches; check_errors clean;
plugin re-parses. Ledger: `TONE-LEDGER-round5-blanket.json`.

**Dial:** K in `tone_round5_blanket.py` (0.10 = current). Rebuild: restore
`.bak-authored-reset-20260820` (all-authored state) OR re-run the 4
forwards, then re-run the script (needs fresh anchor dump; SRC paths die
with the session). `.bak-pre-blanket-20260820` = the old round-2+4 state
(mainland dawn 25% + Solstheim 25%).

**Expected look, by design of the request:** near-monochrome weather with a
10% whisper of the original color everywhere — including wanted colors:
clear-day skies read pale grey-blue, sunsets grey, ash barely warm. If that
is too far anywhere, the fix is the single K constant, not a new hunt.

## Round 4, 2026-08-20 — Solstheim whole-surface tint cut (SUPERSEDED by round 5)

User after round 3: "it was redder and the red stayed during the overcast day.
whatever the tinting mechanism is I want is hugely reduced" + "I dont want you
to change the tone at all, i just want the tone less strong." All times of day
including daytime.

**Mechanism found:** NOT the image spaces (all five the ash weathers use have
Tint.Amount=0, Cinematic.Saturation=1 — and they are shared with ~90 mainland
weathers, untouchable anyway). NOT volumetric lighting (shared, sunny-ray
only). The all-day tint is the ash weathers' OWN authored colors: midday sky
dome at S~0.78 orange-red (195,89,43), lower sky S~0.89, brick-red cloud
decks, red sunlight, red far fog. Round 3 only ever touched dawn/dusk/night
ambient + near fog — the day layer was never treated.

**Round 4 treatment:** the ENTIRE color surface of all 22 ash-family
weathers — sky upper/lower, horizon, near+far fog, ambient (legacy + all six
DALC directions), sunlight, sun, sun glare, stars, moon glare, water
multiplier, effect lighting, cloud-LOD colors, and every ENABLED, VISIBLE
cloud layer — at ALL FOUR quadrants. 1220 color edits.

- Gate: red family only — H <= 45 or H >= 300, S >= 0.08. Cool/neutral
  components untouched (night blues keep their authored character).
- Transform: **luminance-preserving chroma cut**, c' = L + (c-L) x 0.25 with
  L = Rec.709 luminance. Brightness EXACT (fixes round 3's brightening bug —
  see below), hue preserved, color strength -> 25%. Dial: K in
  `tone_round4_solstheim.py` (needs a fresh houseCARL color dump; SRC paths
  inside die with the session).
- Verify: per-edit readback exact on all 1220; field diff DLC02VolcanicAsh01
  vs Astralite ENB.esp = 61 color deltas + 1 clouds-aggregate = exactly the
  edit set, everything else agreed; same for the Helios twin; check_errors
  clean; patch is winner. Sample: midday sky 195,89,43 -> 130,103,92 (same
  luminance, same hue direction, quarter chroma).
- Ledger: `TONE-LEDGER-round4-solstheim.json`. The image spaces and
  volumetric lights were left alone on purpose — if sunny-day god rays still
  read too orange, the shared orange/gold volumetric lights are the next
  dial (needs duplicate-and-repoint, they're shared with the mainland).

## Round 3, 2026-08-20 — Solstheim ash weathers — **REVERTED same day**

User verdict after testing: "you made it worse i think." All 19 records were
re-forwarded from their authored sources (Astralite ENB.esp x12,
Helios_Astralite.esp x7) — diff-verified byte-identical, so the island is
back to raw authored. The overrides stay in the patch as staged
identical copies for a round 4.

**Suspected cause (unconfirmed until the user describes "worse"):** the
round-2 transform holds the strongest channel fixed and lifts the others
toward it. On the mainland's light pastels that leaves brightness alone. On
Solstheim's DEEP dark reds it brightens hard while it desaturates: night
ambient went +50% luminance, the near fog +86%. Meanwhile sky, far fog,
clouds, sun stayed authored deep red. So the likely in-game result was a
brighter, milkier island under a still-red sky — worse, not calmer. Lesson
candidate for the color rule: "V byte-identical" is only a valid proxy for
"brightness unchanged" on light colors; dark saturated colors need
luminance-preserving desaturation instead.

Original round-3 record (what was tried):

User: "solsthiem is very red in the morning, probably also at night."
Round 2 had deliberately excluded "Solstheim ash" — this closes that gap with
the SAME strength-only math (see round 2 below), extended to the ash family.

- **Scope**: the volcanic-ash weather family — 7 Dragonborn ash weathers
  (winners were Astralite ENB.esp), 8 Astralite-added ash weathers, 7
  Helios_Astralite seasonal ash twins (winners were Helios_Astralite.esp).
  22 candidates, 19 patched, 275 color edits. 3 had no red in the treated
  quadrants and were left out entirely: DLC02VolcanicAshTundra01,
  DLC02VolcanicSnow, DLC02VolcanicAshStorm02.
- **Quadrants**: Sunrise + Sunset + **Night** (night is new vs round 2 — the
  user flagged it, and the data agreed: night reds were STRONGER than dawn,
  median S 0.51 vs 0.27, up to 0.84 on the near fog).
- **Fields**: same as round 2 — the six DALC directions + near fog. Day, sky,
  sun, horizon, far fog, specular untouched.
- **Gate**: red band this time, not the cool band — hue <= 45 or >= 300, S >=
  0.08. The cool night-blue components (H 200-260) are deliberately NOT
  touched; only the red/pink cast dropped to 25% strength. Hue and brightness
  byte-identical, verified.
- **Verify**: diff DLC02VolcanicAsh01 vs Astralite ENB.esp = exactly 21
  deltas; diff Helios_DLC02VolcanicAsh01 vs Helios_Astralite.esp = exactly 21
  deltas; all other fields agreed. check_errors clean, 0 dangling / 0 missing
  masters. Patch confirmed load-order winner. Masters gained Dragonborn.esm.
- **Known boundary**: the three vanilla fog/rain variants the ash regions
  borrow (SkyrimFogVT, SkyrimOvercastRainVT, SkyrimFogFF) are round-2 records:
  dawn/dusk treated, Night NOT (they are shared with the mainland, whose
  nights are accepted as-is). If a foggy Solstheim night still reads red,
  their Night quadrants are the next dial. Apocrypha stays untouched (realm).
- Ledger: `TONE-LEDGER-round3-solstheim.json`. Script:
  `tone_round3_solstheim.py` (STRENGTH=0.25; self-verifies against 4 round-2
  ledger anchors; needs a fresh houseCARL color dump — edit SRC — since the
  session tool-result path inside it dies with the session).

## Round 2, 2026-08-20 — mainland (LIVE) — **STRENGTH-ONLY.**
User: "the purpleish hue is okay but not so strong over everything. like 25%
would be good."

## What it changes (round 2)

96 of 116 covered weathers, 622 color edits. ESL-flagged, overrides only.

- **Sunrise + Sunset quadrants only**: the six directional-ambient light colors
  and the near fog. Hue-gated (cool band 180-340 deg, saturation >= 0.08):
  **saturation reduced to 25% of authored. Hue unchanged. Brightness unchanged.
  No warm shift of any kind.** The purple cast keeps its exact color direction
  at a quarter of the strength.
- **Everything else is byte-identical to the authored winners**: lower sky
  (full authored purple dawn sky), Day quadrant (no warmth formula), night,
  specular, sun, horizon, far fog.

Independent verify: field diff of SkyrimClear vs Astralite ENB.esp = exactly
14 deltas (12 DALC + 2 FogNear), 133 fields agreed. check_errors clean.

## Round 1 (REJECTED - kept for history)

S x0.5 + warm nudge (R x1.06 / B x0.94) + sky x0.7 + the old Day G>R warmth
formula. User verdict: "now its fucking red. I didn't want the tone changed I
wanted the strength changed." Lesson recorded in memory: strength complaints
get amplitude changes (saturation only), never hue shifts.
Ledger: `TONE-LEDGER-round1.json` (historical). The old Day-only patch
"Authoria - Patch - Astralite DALC Warmth" stays disabled permanently.

## Coverage and exclusions

116 normal overworld weathers forwarded from their live winners (Astralite ENB
55, Helios_Astralite seasonal twins 53, Snowy Holds patch 6, Wyrmstooth patch 2).
Realm/FX weathers untouched: Sovngarde, Soul Cairn, Apocrypha, Blackreach,
Solstheim ash, Forgotten Vale, Shivering Isles, Blue Palace, eclipse/quest FX,
Skuldafn, Bloated Man's Grotto.

## Rebuild / iterate

1. Re-forward all 116 from their winners via houseCARL (4 forward_record calls,
   lists in the session notes / memory) — this resets the patch to authored.
2. Run `dawn_tone_r2.py` (scratchpad; STRENGTH constant = 0.25). It is
   self-verifying against four anchor values and writes `TONE-LEDGER-round2.json`.
3. The dial: STRENGTH up for more purple (0.40 = a bit stronger), down for less.
   Change ONLY that constant. Never add hue shifts.

Load AFTER: Astralite ENB.esp, ECSS, Helios_Astralite*.esp, Snowy Holds
Seasonal Snowfall, Wyrmstooth-Astralite patches. Wired 2026-08-20 into profile
DEEZ CS NUTZ only (other profiles lack the masters).
