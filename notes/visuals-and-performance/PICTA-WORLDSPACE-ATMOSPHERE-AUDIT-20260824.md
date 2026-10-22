# Picta — quest space and worldspace atmosphere audit
Written 2026-08-24. Planning only. Nothing changed.

Prompted by two reports from the Picta community:
- "Picta doesnt yet have weathers for apocrypha ands soul cairn."
- "Some quest mods like vigilant, soul cairn etc just dont have weather types that would suite
  the atmosphere those mods demand."

Both are true observations. Both have the cause backwards. Three agents audited it and two
adversarial passes refuted the first conclusions. This is the corrected version.

---

# 1. THE HEADLINE

**Picta is not missing suitable weathers. It ships them, with full colour, and does not wire
them up — while simultaneously reaching into places it has no business touching.**

Picta's ESM carries 218 weather records:

| Group | Count | What they are |
|---|---|---|
| Terrain families | 90 | The nine families of ten rungs. Ordinary Skyrim outdoor moods. |
| Label rows | 45 | Not weathers. All-black separator rows the author uses in xEdit. Nothing points at them. |
| Technical wind variants | 27 | All-black. They exist only to carry a wind speed. |
| **Empty stubs** | **16** | **Completely blank. Every colour slot black, no fog, no imagespace, no clouds.** |
| Grey-canvas quest weathers | 7 | Picta's own main-quest moments. Flat grey plus a cloud panorama. |
| Vanilla / DLC overrides | 33 | **29 of these keep their real colour.** Only 4 were repainted. |

So the realm weathers a quest mod needs already exist inside Picta's own plugin, untouched:

- **Soul Cairn** — all five vanilla weathers, violet-indigo void, dead sun, tight fog.
  Colour block byte-identical to Dawnguard.
- **Apocrypha** — toxic green horizon at all four times of day, eye-tile cloud panorama.
  Byte-identical to Dragonborn. The strongest realm weather in the plugin.
- **Blackreach** — cyan cave fog intact, byte-identical to vanilla.
- **Sovngarde, Skuldafn, the Mind of a Madman set, Boethiah, Karthspire** — all byte-identical
  in colour. Picta only touched their sky-statics list.

**The fix for the atmosphere complaint is therefore wiring, not authoring.**

---

# 2. THE THREE DAMAGE CHANNELS

This is what actually goes wrong, and it is not what either community report describes.

## Channel 1 — four vanilla weathers repainted grey

Picta takes four extremely common vanilla weathers, renames them, and rewrites their colour into
the flat grey canvas:

| Vanilla record | Renamed to | Colour slots changed |
|---|---|---|
| SkyrimCloudy | Helgen intro scene | 60 of 68 |
| SkyrimFog | Prison cart scene | 49 of 68 |
| SkyrimStormSnow | Dragon altar scene | 49 of 68 |
| HelgenAttackWeather | Dragon attack scene | 49 of 68 |

All four read sky 7D7D7D by day, near-fog 050505, black sun glare, black cloud LOD. Both the ESM
and the ESP carry the rewrite.

**A live reverse lookup found 62 regions that roll at least one of these four.** Among them:

- **Vigilant** — its Coldharbour climate, Molag and NoCore regions
- **Beyond Skyrim Bruma** — mountains, Blackwood, Gold Coast, Great Forest, snowy mountains,
  Frostfire Glade twice
- **Wyrmstooth** — three regions
- **Olenveld** — three regions
- **Legacy of the Dragonborn** — Sancre Tor, Pale Pass, the Planetarium storm
- **Glenmoril** (2), **Unslaad**, **Sea of Causality** (2), **The Frozen Heart** (2),
  **Siege at Icemoth**, **ClefJ's Fort Dawnguard**
- The entire vanilla Skyrim region set

**This is how Picta reaches mods it does not master, and it is almost certainly the answer to
both the Bruma and Wyrmstooth black-sky reports.** No plugin dependency required — the mods roll
a shared vanilla record, and Picta repainted it.

## Channel 2 — four climates re-pointed at colourless weathers

Picta's eight climate overrides send four vanilla climates to its own new grey weathers:

| Climate | Now points at |
|---|---|
| DefaultClimate | a grey Picta weather at 100% |
| SkyrimClimate | a grey Picta weather at 100% |
| BlackreachClimate | a grey Picta weather at 100% |
| BloatedMansClimate | a grey Picta weather at 100% |

Ten worldspaces use DefaultClimate. Also caught: Blackreach itself, Darkwater, Alftand,
Wyrmstooth's Dimfrost, and a Bloated Man's Grotto duplicate from another mod.

**Correction to an earlier draft of this plan:** patching BloatedMansClimate does *not* fix the
grotto. The real Bloated Man's Grotto worldspace has a null climate and inherits Tamriel's. The
only worldspace using that climate belongs to a different mod entirely.

## Channel 3 — Solstheim and the Forgotten Vale are silently rewritten

**All 65 of Picta's regions are overrides of vanilla regions. Not one is new.** Seven of them
overwrite Dragonborn's own Solstheim regions and four overwrite Dawnguard's Forgotten Vale
regions.

**Solstheim loses its ashstorms outright.** Picta re-points the ash regions at Rift Fall Forest
weathers, which carry no precipitation at all. Its own ash family — ten rungs — was never
finished: **all ten records are completely empty.** Black sky, no fog, no imagespace, no clouds,
not even a weather classification.

**The Forgotten Vale** gets snow-tundra weathers, its own family was never authored, its Canyon
region points at a record that does not exist, and the preset has no entries for it.

So both places run on borrowed, unpresetted weather. This is worse than the "no preset files"
problem noted earlier — the records themselves are blank.

---

# 3. THE REPAIR ROUTE, CORRECTED

An earlier draft said "point it back at the vanilla weather" is always safe, on the grounds that
Picta never strips vanilla colour. **That is false and it broke two of the proposed fixes.**

Route rules, corrected:

1. **Leave it alone** — best where a mod's own weather is untouched by Picta. Renders correctly
   with no preset file, because mod weathers carry real colour.
2. **Point at a vanilla weather** — safe for the **29** untouched overrides. **Never for the
   four repainted ones.**
3. **Point at a Picta weather** — only where Picta has a suitable record *and* it has a preset
   file mapped, otherwise it is a grey canvas.
4. **Restore colour** — for the four repainted records, copy the vanilla colour block back. This
   is the only route that fixes the 62 affected regions in one move.

## Fixes that were wrong and are now corrected

- **"SkyrimClimate back to SkyrimCloudy"** was billed as the highest-impact single fix. It is a
  **no-op** — it swaps one grey record for another, because SkyrimCloudy is one of the four
  repainted. Pick an untouched weather, or restore the colour block.
- **The Forgotten Vale Canyon fix** restores a seven-entry vanilla list that includes two
  repainted records. Two rolls in ten would still be colourless.
- **The Volkihar Isle fix** lands on a repainted record at 1 percent.

---

# 4. TWO NEW DEFECTS FOUND

**Blackreach is mis-targeted in Picta itself.** Its region override points at Picta's Throat of
the World weather, not its Blackreach weather. Both records exist, so this is a wrong target
rather than a dead link — but Blackreach gets the mountaintop sky, and its own preset entry is
never reached. The region and the climate disagree with each other.

**Apocrypha would clobber Lux.** The live winner for the Apocrypha worldspace is your FWMF master
patch, carrying Lux's Apocrypha climate. Picta's ESP overrides that worldspace and resets it to
Dragonborn's climate. Colour-wise Apocrypha is fine either way, but Lux's version loses.

---

# 4b. AN UNMAPPED WEATHER DOES **NOT** RENDER BLACK ON THIS RENDERER

Settled 2026-08-24 from the live build. This is load-bearing and it narrows the whole job.

**The community finding, under real ENB:** "A weather ID absent from the applicable list renders
nothing. No hidden default, no Base_Weather catch-all." That is an empirical result and there is
no reason to doubt it — **for ENBSeries**.

**It does not transfer to Effects 11.** Proof from this build, not from reasoning:

- The live Soul Core preset maps exactly **143 weather IDs, and every single one is from
  Skyrim.esm** (load index 00). Not one mod-added weather is mapped.
- The load order contains **372 weather records**. So **229 are unmapped right now.**
- Among the unmapped: every weather added by Vigilant, Glenmoril, Beyond Skyrim Bruma,
  Wyrmstooth, Morskom, DAc0da, the Forgotten City, Olenveld, Unslaad and the Deadlands — and
  also **all 14 weathers Astralite itself defines**, including `Seasons_CloudySnow`,
  `Seasons_CloudySnow02`, `SkyrimStormRainRE`, `JawzSkyrimStormRain`, `SkyrimStormSnowBlizzard`
  and the eight `DLC02Volcanic*` records that are the whole of Solstheim's ash weather.
- Several of those are in active mainland rotation — the user's own seasonal snowfall patch
  places `Seasons_CloudySnow`, `JawzSkyrimStormRain` and `SkyrimStormRainRE` into region lists.

**And nothing is black.** No black-sky report has ever come from this build. The opposite:
Solstheim was reported as *too red*, which is positive evidence that an unmapped weather renders,
in colour, using the base preset settings.

## The rule this gives us, which is tighter than "map everything"

The asymmetry from section 1 still decides it, but the consequence is now precise:

- **A mod-authored or vanilla weather, unmapped → renders correctly.** It carries real colour in
  the record. Leave it alone. This is what already happens today for 229 weathers.
- **A Picta weather, unmapped → renders as the flat grey canvas.** Picta's records carry no
  colour, so the preset entry is the only thing supplying it.

So the flat weather list must cover **every Picta weather that can play** — that is
non-negotiable and it is the single most important build step. It does **not** need to cover mod
weathers, and adding them would be work for nothing.

## And it resolves the takeover disagreement

The community advice — "let Picta records take over the added worldspaces, keeping their own
doesn't really work well" — is **correct under real ENB**, where an unmapped mod weather renders
nothing and taking over is the only way to get a sky at all.

**On this renderer the reverse is true.** A mod's own weather renders fine unmapped; a Picta
weather does not. Letting Picta take over an added worldspace would *replace a working sky with a
grey one* unless every substituted weather is also added to the list.

Both positions are right in their own environment. Ours is Effects 11, so mod realms keep their
own weathers.

Caveat worth stating: this is inferred from 229 unmapped weathers producing no complaint across
months of play, plus one positive colour report. A deliberate in-game check would make it
airtight, and it costs one visit to Solstheim.

---

# 5. THE PRESET LAYER

**Picta's shipped weather list is stale and maps nothing usable.** The file the renderer actually
reads has a single populated block pointing ~100 vanilla weather IDs at a folder that does not
exist in this release, and it contains no entry for any of Picta's own weathers.

So under this renderer, **until the flat list is generated, nothing gets a Picta grade at all**.
That is already on the plan; this audit just confirms it is load-bearing rather than polish.

Picta also planned a block of nine unique realm weathers, wrote weather-list entries and region
and climate links for all nine, and never shipped the records or the preset folders. That block
is exactly the twelve dead links already on file.

---

# 6. RECOMMENDED SHAPE OF THE REPAIR

One patch, sized roughly:

| Piece | Size | Why |
|---|---|---|
| Restore the colour block on the four repainted vanilla weathers | 4 records | Fixes 62 regions across a dozen quest mods in one move. The single highest-value item in this document. |
| Re-point the four grey climates at coloured weathers | 4 records | Fixes ten DefaultClimate worlds plus Blackreach, Darkwater, Alftand, Dimfrost. |
| Repair the twelve dead links | 11 records | Soul Cairn, Mind of a Madman, Darklight Tower, Boethiah, Forgotten Vale Canyon, Volkihar Isle. Point each at the real vanilla weather for that place — all verified to exist. |
| Fix the Blackreach mis-target | 1 record | Point the region at the Blackreach weather, or better, at the coloured vanilla one. |
| Restore Solstheim's ash regions | 7 records | Picta's ash family is empty. Give them back Dragonborn's ashstorms. |
| Restore the Forgotten Vale regions | 4 records | Picta's vale family was never authored. |
| Preserve Lux's Apocrypha climate | 1 record | Forward Lux's value over Picta's reset. |

**About 32 records.** Every replacement target was individually verified to exist, to be a
weather record, and to belong to the place claimed.

---

# 7. IMPLEMENTATION METHOD — ARCHETYPES, NOT REALMS

Adopted from a community note the user passed on 2026-08-24, assessed and adjusted against what
this audit actually found. The core idea is right and it is the difference between a tractable job
and an untractable one.

**Do not tune 60 realms. Group them into 6–8 visual archetypes, tune each archetype once against
one representative realm, then apply it to every member.** That turns roughly 60 tuning problems
into about 8.

It also happens to match the data. **Picta is already built this way** — its nine terrain families
*are* archetypes. So we are not imposing a structure, we are reusing the one that is there.

## The archetype library, mapped to what actually exists

| Archetype | Representative | Where it comes from | Members |
|---|---|---|---|
| Alpine / Snow | Snow Tundra family | Picta | Northern holds, Forgotten Vale, Solstheim snow, Unslaad, The Frozen Heart |
| Temperate Forest | Falkreath Pine Forest | Picta | Falkreath, Bruma's Great Forest, Glenmoril, Olenveld |
| Marsh / Mist | Hjaalmarch Marsh | Picta | Hjaalmarch, Blackwood, the foggy Sea of Causality regions |
| Volcanic / Ash | Eastmarch Volcanic Tundra | Picta | Eastmarch. **Solstheim ash must use Dragonborn's own records — Picta's ash family is ten empty stubs.** |
| Dark Void | Soul Cairn set | Dawnguard, shipped intact inside Picta | Soul Cairn, Vigilant's Coldharbour, the Deadlands |
| Otherworldly Bright | Apocrypha set | Dragonborn, shipped intact inside Picta | Apocrypha, Praedy's Apocrypha |
| Desert | Gray Cowl's own | Gray Cowl of Nocturnal | The Alik'r / Hammerfell spaces |
| Cave / Enclosed | Blackreach vanilla | Skyrim, shipped intact inside Picta | Blackreach, Darkfall, Alftand, Darkwater |

Note that **three of the eight archetypes cannot come from Picta at all** — Dark Void,
Otherworldly Bright and Desert. That is not a gap to fill by authoring; those records already
exist with full colour and simply need wiring. It is the same conclusion this audit reached from
the other direction.

"Storm" is deliberately not an archetype here. In Picta it is rungs 09 and 10 of every family,
not a separate mood, so it comes along free with whichever archetype a realm is assigned.

## Phasing

- **Phase 0 — audit.** Every non-vanilla climate into one table: climate, worldspaces, weathers,
  classification flags, current state, assigned archetype. **Largely done already** — sections 1
  to 5 of this document plus the region census in the four-seasons doc. No game time needed.
- **Phase 1 — build and tune the library.** One representative realm per archetype.
- **Phase 2 — bulk apply.** One light patch per source mod; assign worldspaces to archetype lists.
- **Phase 3 — batch verify.** 8–10 realms per session from a prepared travel list.
- **Phase 4 — individual attention** only where a realm genuinely deviates.

## Feedback vocabulary

Each phrase maps to exactly one cause, so a one-line report is actionable without a screenshot.
This is worth using verbatim:

| What you say | What it means |
|---|---|
| "black" | an unmapped weather ID — **or** one of the four repainted vanilla weathers |
| "clouds mashed" | a foreign record survived the swap |
| "too bright" / "too dark" | ambient or direct light scale |
| "hue wrong" | colour filters |

**One adjustment to the source note.** It lists "black" as meaning an unmapped weather ID only.
This audit found a second cause with the identical symptom: the four vanilla weathers Picta
repaints to a flat grey canvas will read as black-ish **however** they are mapped, because the
greyness is in the record, not the preset. So "black" needs one follow-up question: *which
weather was running?* If it is one of those four, the fix is restoring its colour block, not
adding a preset entry.

## One disagreement worth recording

The source note calls **Bruma and Wyrmstooth the known-good anchors**, to compare other realms
against. For that author they may well be, after their own fixes.

**For this build they are the opposite** — they are the two realms reported black, and neither has
been verified here. Until they are, they are test cases, not reference points. Use a realm we have
actually confirmed as the anchor instead.

## Test order

Currently-black realms first, then the places actually visited in play, then the long tail.
Realms never entered do not deserve a test cycle. That ordering is correct and is adopted.

## What deliberately gets no work

Every mod realm whose own weathers Picta does not touch. Vigilant's bespoke Coldharbour skies,
Glenmoril's, Olenveld's, DAc0da's and the Deadlands' all render correctly today and will keep
doing so. They do not need Picta and should not get it.

**That is the real answer to the atmosphere complaint.** Not "Picta lacks suitable weathers", and
not "we must author realm weathers" — but "stop Picta reaching into places that were already
right, and wire up the good weathers it already ships."
