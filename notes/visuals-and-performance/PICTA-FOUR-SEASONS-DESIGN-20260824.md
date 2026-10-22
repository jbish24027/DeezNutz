# Picta four-season weather — design, planning only
Written 2026-08-24. Nothing built. Nothing changed.

Two adversarial passes were run over this. Both refuted the first draft. Everything below is
the post-correction version, and where a number was recounted I use the recount.

---

# 1. YOU ALREADY HAVE HALF OF THIS

Worth saying first, because it changes what "four seasons" needs to deliver.

Seasons of Skyrim, Seasonal Landscapes, Seasonal Landscapes Unfrozen and Turn of the Seasons
are all enabled. Between them they already swap **terrain textures, statics, trees, grass,
flora and furniture** by month. That is the half of four seasons you actually walk around in,
and **none of it is affected by the weather-mod swap.** Not one Seasons config file contains a
weather section. I checked all 362 of them across 51 mods.

So what we are designing here is the **sky and light** half only. The ground already changes.

---

# 2. THE MECHANISM, IN PLAIN TERMS

A weather region is a list. Each line is one weather plus a percentage.

The Seasonal Weathers Framework lets a line use a **counter** instead of a percentage. It runs
70 counters. A script sets them from the in-game month and forces every out-of-season counter
to zero.

So one region can hold four separate sets of lines, one per season, and only the current
season's set can ever roll. That is the whole capability. It already works. Nothing needs
building for the machinery itself.

Two structural details that matter:

**Scopes.** Each counter belongs to a scope: Common, Spring, Summer, Autumn or Winter. The
Common counters are refilled every single month and never zeroed — a line on a Common counter
fires all year. The four season-named scopes are zeroed in the other nine months.

**Lanes.** Every counter exists twice: a plain lane and a snow-region lane. They are two
independent sets of monthly values, so the same bucket can behave differently in a snowy hold
than in a green one.

---

# 3. WHAT PICTA ACTUALLY GIVES US

Picta ships 90 regional weathers as **nine families of ten rungs**. The rungs are the same
ladder every time: clear, lightly cloudy, lightly cloudy windy, cloudy, cloudy-with-weather,
overcast, overcast-with-weather, overcast fog, storm, heavy storm.

**The critical fact, verified twice: Picta's weather records carry almost no colour.**
All nine families' clear-day records are 172 subrecords each, and 162 of those slots are
byte-identical across all nine. Sky upper, sky lower, horizon, fog, sunlight, ambient, cloud
timings — identical. Only the name, four cloud-panorama texture slots, the aurora model and
the directional ambient block differ.

Picta ships a **flat grey canvas** on purpose. Every family's sky is 7D7D7D by day and 4B4B4B
at night, with black sun glare, black cloud LOD and near-black fog. **All the colour is done in
the preset file.**

That has two consequences and you need both:

**Good:** to change how a season looks, you only have to make the region roll a different
family's weather. The matching preset file comes with it. No new weather records, no new
preset files, no colour editing.

**Bad, and this is new since my last message:** a Picta weather with **no** preset file mapped
to it renders as that flat grey canvas. Not "a bit off" — genuinely colourless. So the preset
routing is not polish. It is load-bearing. See section 8.

---

# 4. THE CASTING

I had all nine families scored on their actual numbers — sun colour filter, direct-light
desaturation, ambient filter and desaturation, sky gradient, bloom, fog curve — then had the
scoring recomputed independently. The table survived, within one degree of hue on three
families.

| Season | Family | Character |
|---|---|---|
| Spring | Falkreath Pine Forest | cool mint-green, hue 166 |
| Summer | Whiterun Tundra | warm gold, hue ~23 |
| Autumn | Rift Fall Forest | heavy orange, hue 29, green drained out of foliage |
| Winter | Snow Tundra / Snow Mountains / North Coast | strong blue, hue 219-228, green pushed cold |

One correction to my earlier guess: **Reach Mountains is technically the greenest family but
its colour cast is the faintest of all nine.** As spring it would read as no season at all.
Falkreath is the right spring.

## The honest verdict on how distinct they are

**About three and a half looks, not four.**

- Spring at mint 166 and winter at blue 219-228 are unmistakable. No argument.
- **Summer and autumn sit six degrees apart in hue.** They separate only on tint strength and
  the per-hue rotations, and all of it is applied at 10 percent tint weight.

So out of the box you would clearly feel spring, summer-ish, autumn-ish, winter — with the
middle two closer than you want.

## Fixing summer versus autumn

Do not weaken summer to separate them. My first instinct was to drop summer's tint weight, and
that was wrong twice over: it makes summer fainter, pushing it toward the exact "no season at
all" failure that disqualified Reach, and a tint weight is a blend against the untinted image,
so lowering it shifts the result's hue rather than just its strength.

The right levers are the opposite direction:
- **Strengthen autumn's foliage rotation.** The Rift family already drains green out of
  foliage. Push that further and autumn separates on foliage, not sky.
- **Raise summer's green and yellow saturation.** Summer becomes lush rather than merely warm.

Both are saturation-and-rotation moves inside the preset files, and both respect the standing
rule: amplitude only, hue and brightness locked, unless you explicitly ask for a hue change.
Autumn's foliage rotation is the one place where a hue move might be wanted, and that needs
your explicit sign-off.

---

# 5. YOUR NO-SNOW-IN-SPRING-AND-SUMMER RULE

Found it. It is baked into the region records, not a menu setting. There is no settings file
anywhere for the framework — its sliders live in the save.

**What the stock Astralite patch does:** wires all 53 of its snow lines to the four **Common**
counters. Common is refilled every month and never zeroed. So stock snows all year.

**What your patch does:** uses **none** of those four. Every snow line was duplicated into an
**Autumn copy and a Winter copy** at the same chance in the same lane. 145 snow lines across 34
regions, and not one touches a Common, Spring or Summer counter. Autumn and Winter are zeroed
in the other nine months, so snow simply cannot roll March through August.

The policy has no leak: the eight regions your patch does not win carry no snow lines at all.

**This is exactly reproducible on Picta and it is the model for the whole design.**

## A trap the review caught

The snow-region lane keeps snow through midsummer by its own defaults — June 25, July 20,
August 25. If snow lines were hung on that lane under a **Common** scope, you would get snowy
summers.

Your Autumn/Winter scoping makes that irrelevant, because the scope is zeroed regardless of
what the lane's monthly value says. **Keep the scoping. It is what does the work.** This is
why your patch has held up.

---

# 6. MELTING THE SNOW BELT IN SUMMER

You asked for this and it costs nothing new.

Winterhold, Windhelm, the Pale, the mountains and similar sit on snow families all year today.
Under the design they get the paired green family's **rain** rungs hung on their spring, summer
and autumn slots, and keep their own snow only on winter — and on autumn if you want a shoulder
season.

Two pairs line up rung for rung with no compromise:
- Whiterun Tundra pairs with Snow Tundra
- Reach Mountains pairs with Snow Mountains

**The trap:** 15 of the 26 Picta regions involved contain **no snow weather at all**, because
Picta puts snow only in its three snow families and the green families carry rain in those
slots. Those 15 need a snow rung appended at zero chance with the autumn and winter counters —
which is precisely what your current patch already does in Whiterun, Riften and Falkreath.

The affected regions: Whiterun, Solitude, Riften, Markarth, Reach, Tundra, Tundra Marsh, Fall
Forest, Falkreath, Pine Forest, Japhet's Folly, Volcanic Tundra, Riften Fall Forest, Darklight
Tower and Labyrinthian Maze.

---

# 7. COST

Region records only. No new weather records. No new preset files.

- About **41 regions** need wiring.
- A wired region grows from about 10 lines to about **28**.
- Precedent: the shipped framework patch for another weather mod peaks at 27 lines, and your
  own snowy-holds patch peaks at 21 and already uses zero-chance lines. This is proven ground.

**But the cost framing "one small patch and nothing else" is wrong**, and the review was right
to call it out. Those region records are already contested. One of them sits at override depth
seven and is currently won by your snowy-holds patch with 17 lines already carrying counters.
A Picta four-season patch has to **displace that whole chain**, not start from Picta's clean
ten-line lists. That is a bigger authoring and verification job than the record count suggests.

Also in the cost: **Picta's master is a full plugin and cannot be made light.** Its records run
to high FormIDs, and compacting it would renumber the very local IDs its own preset routing
references. It takes a full load slot permanently.

## The approach I am NOT recommending

Cloning each terrain's preset folder three times and regrading per season, so every hold keeps
its own identity in all four seasons.

It sounds better and it is not. The roughly 100 keys a regrade would overwrite **are** the
colour identity. After grafting, only 82 keys remain to tell the families apart, and those
carry no hue at all — two of the families collapse to byte-identical files. So it buys almost
nothing in per-hold identity, for 162 to 270 new weather records and 108 to 231 new preset
files. Drop it, or scope its claim honestly as "preserves bloom scale, fog curve, god-ray range,
aurora intensity and snow brightness".

---

# 8. THE HOLES THAT HAVE TO BE FILLED FIRST

These are new and they are why I am not recommending we start authoring yet.

**Picta's preset routing has no entries for four of its own families.** Forgotten Vale and the
three Solstheim families have nothing in the weather list, and the Solstheim ash folder ships
empty. A further nine routing entries point at files that do not ship. Since Picta's weather
records are colourless, **that means Solstheim and the Forgotten Vale would render as a flat
grey dome.** Eleven of the 41 regions we want to wire are in that hole.

**Picta's fallback weather list is a dead leftover.** Its single populated entry points at a
folder path from the 1.0.0 layout that does not exist in 1.0.1. So there is no working safety
net either.

**The routing generator needs one correction I got wrong earlier.** I said the short IDs in
Picta's list are its record IDs with the load-order byte stripped, and the fix is to prepend
the runtime index. That is right. But an intermediate report claimed the leading digits were
plugin indices and should be **replaced** — that is wrong and would destroy real FormID data.
The list holds 126 IDs: 122 are Picta's own local IDs needing the runtime index prepended, and
**four are vanilla Skyrim weather IDs written without a leading zero, which must be left
completely alone.**

---

# 8b. REVISED BRIEF — MAXIMUM PICTA VARIETY (your 2026-08-24 direction)

Your words: *"I want the seasonal weather framework patch rewritten for Picta, and I want to be
able to see as many picta weathers as possible while respecting our seasons and unfrozen
patches. picta weathers should be able to be spread out through the year/seasons."*

That changes the casting brief, for the better. Section 4 assumed one family per season
globally. Spreading for variety is a different and richer shape.

## The arithmetic of variety

Picta has 90 regional weathers: nine families of ten rungs.

- **Today's shape (Picta as shipped):** each region rolls its own terrain family only.
  You see **10 of 90** in any given place, and the same 10 all year.
- **One-family-per-season (section 4):** each region rolls four families across the year.
  You see **up to 40 of 90** per place. Four distinct looks.
- **Maximum spread:** each region draws from as many families as its terrain plausibly
  supports, distributed across the four seasons. Approaching **90 of 90** across a playthrough.

The cost is identical in all three. A region's list is just longer. There are no new records
and no new preset files either way — this is purely a question of which weathers get listed
against which season counter.

## What limits the spread

Two real constraints, not preferences.

**Terrain plausibility.** A weather carries its cloud panorama and its preset grade. Rolling
the volcanic-tundra family in Falkreath would put Eastmarch's sky over a pine forest. Some
cross-casting reads as seasonal variety; some just reads as wrong. The families that cross
well are the ones whose identity is a *mood* rather than a *place* — pine forest, fall forest,
tundra, mountains, snow tundra, snow mountains. The ones that read as a specific place are
marsh, volcanic tundra and north coast.

**Your snow rule.** Snow rungs may only ever be hung on autumn and winter counters. That is
non-negotiable and it is what protects Unfrozen. So the three snow families are confined to
the back half of the year everywhere except the holds that are meant to stay white.

## The shape I would build

Per region, four slots, each drawing from a different family:

| Slot | Draws from | Why |
|---|---|---|
| Spring | Falkreath pine forest | mint-green, the freshest grade Picta has |
| Summer | the region's OWN terrain family | keeps each hold's identity in the season you play most |
| Autumn | Rift fall forest | orange, foliage green drained — literally an autumn grade |
| Winter | the region's paired snow family | blue, and the only slot allowed to carry snow |

That gives every hold four looks, keeps its own identity in summer, and spreads roughly 40 of
the 90 weathers per region — the whole set across a playthrough as you travel.

**Then add spread inside each slot.** A season slot does not have to be one family. Falkreath's
spring can list Falkreath's clear rungs *and* Whiterun's, both on spring counters, so even one
season rolls varied skies. This is where "as many Picta weathers as possible" is actually won,
and it costs only list length.

## The ceiling

A region list grows from 10 lines to roughly 28 under section 4's shape, and could reach the
mid-30s with intra-season spread. Known precedent: the shipped framework patch for another
weather mod peaks at 27 lines, and your own snowy-holds patch peaks at 21. Mid-30s is beyond
anything I can point to as proven. **I would build to 28 first, confirm it behaves, then widen.**
Widening later is a re-run of the same generator, not a rewrite.

## Full coverage, per your instruction

*"let's make sure every worldspace/region exterior that has seasons enabled gets to have
weathers."*

Taken literally that means the patch covers every seasonally-gated exterior region, not just
the 26 Picta happens to overlap. Three groups:

1. **26 regions Picta overrides** — rebuild from Picta's version, wire all four seasons.
2. **8 gated regions Picta does not touch** (Bruma, Legacy, Wyrmstooth and one vanilla) —
   carry forward from your current patch, then decide whether to repoint them at Picta
   weathers so they get the Picta look rather than the vanilla one.
3. **15 of the 26 have no snow weather at all** — append snow rungs at zero chance on the
   autumn and winter counters, exactly as your current patch already does in three regions.

Group 2 is the one that interacts with the custom-worldspace work in the main plan. Repointing
those regions at Picta weathers is the same operation that fixes Bruma's and Wyrmstooth's sky,
so the two jobs should be done together, in one patch, not separately.

---

# 8c. THE SNOW LINE — MEASURED, NOT GUESSED (2026-08-24 re-plan)

Your rules: no snow in typically frozen areas in **spring and summer**; snow everywhere in
**winter**; snow at **high altitude in every season**.

## The sign convention is settled

Proven three ways, one of them from the renderer's own UI text. The binary contains
"What is the snow line altitude in summer?" next to the label "Summer Height Offset", and
"In which month is the snow line lowest?" next to "Maximum Winter Month".

**The two offsets ARE the snow line altitude in world Z. A bigger number means a higher line
and therefore less snow.** Both known data points fall out of it: shipped summer 20000 sits
34,000 above sea level (peaks only), shipped winter −20000 sits 6,000 below sea level
(everything white), and the 9,999,999 pin puts the line at ten million (no altitude snow ever).

Full formula, Tamriel:

    snow begins at world Z = HeightOffset(month) − (map − 0.5) × 75000
    fully white 2082 units above that

## The altitude map is not an altitude map

This is the finding that decides everything. The map was decoded — BC4, 3808×3008, one channel,
128 world units per texel, covering the Tamriel cell grid exactly.

**It is a regional snowiness painting with the hold borders still visible in it.** The north
reads 173–202. The Rift reads 37–55. That bias is worth between +21,000 and −27,000 world units
of snow line — **larger than Skyrim's entire terrain relief.**

It actively fights real altitude. The Throat of the World samples *below* neutral, so the map
*raises* its snow line. Lost Tongue Overlook, a genuine peak, gets its line raised by 22,484.
Meanwhile the Winterhold Imperial camp, on a coastal shelf, gets its line *lowered* by 21,324.

## So your three rules cannot all be met with numbers alone

The binding conflict: the highest place that must stay clear in summer scores 14,455. The lowest
peak that should stay white scores −5,255. **The gap is 19,710 units and no single value bridges
it.**

Restricting "peaks" to the marquee summits — Throat of the World, High Hrothgar, Mount Anthor,
Skyborn Altar, the Shrine of Azura ridge — leaves a usable window, but only **341 units wide**.

## Recommended values

    SummerHeightOffset = 14600
    WinterHeightOffset = -20000

Applied to **all six** worldspace configs, which all currently carry the 9,999,999 pin.

At those values, verified point by point:
- Clear in July: Morthal, Dawnstar town and docks, Windhelm, Winterhold town and College,
  Labyrinthian entrance, Nightgate Inn, the Pale Imperial camp, Snow Veil Sanctum, Stonehill
  Bluff, and the Winterhold Imperial camp.
- White in July: Throat of the World, High Hrothgar, the Shrine of Azura ridge, Skyborn Altar,
  Mount Anthor.
- White in January: all 63 sampled points. Tightest is Falkreath with 3,506 units of margin.

**What you lose:** the Jerall and Velothi mountain rings — Autumnwatch Tower, Lost Tongue
Overlook, Northwind Mine and Summit, Ansilvund, Tolvald's. They stay bare in summer. Getting
them back is a **map edit**, not a number, and the technique already exists here (the Magpie
Manor valley clamp changed 26,433 texels within a bounded box).

## Three caveats that matter

**1. The margin is inside the noise.** Extended Materials parallax adds a displacement term to
the same calculation worth roughly ±5,200 world units. The usable window is 341 units. So this
setting must be confirmed in game, not trusted from arithmetic. Expect to nudge it.

**2. The city configs behave differently.** Markarth, Riften, Solitude, Whiterun and Windhelm
all use a blend band of 5000 against Tamriel's 2082 — **2.4 times wider**. Same numbers, softer
and higher-reaching transition inside city worldspaces.

**3. Spring cannot be clean.** The system ramps between two poles across the year. January is
the low pole and July the high pole, so March sits a quarter of the way up from
white-everywhere. **There is no pair of values that makes February white and March clear in the
north.** Options: accept lingering early-spring snow (it is arguably correct), or move the
winter pole earlier so the ramp starts sooner. Nothing else in the feature can fix it.

## The biggest open risk

At these values, summer snow returns to northern terrain above roughly 6,700–10,200 units above
sea level. **Nobody has checked where Unfrozen's green summer terrain actually sits.** If any of
it is above that line, snow will paint over it — the exact failure the pin was created to
prevent. That check has to happen before these values ship.

## Month alignment: clean

No mismatch. The snow line poles (winter month 0, summer month 6) line up exactly with both
Seasons of Skyrim and the Seasonal Weathers Framework, all zero-based, January and July.

---

# 8d. CASTING — CORRECTED

## The safety case holds, and it opens a door

Attacked hard and it survived. **In all three snow families, rungs 05, 06, 07, 09 and 10 carry
snow. Only rungs 01, 02, 03, 04 and 08 are clean** — Pleasant flag, null precipitation link,
null visual effect. Three independent signals agree: the flag byte, the particle link, and which
cloud-texture pool the rung draws from.

Note rung 06 is snow in the snow families even though it is dry in the rain families. Easy trap.

**So the snow families' five clean rungs are legal in spring and summer.** That gives cold, clear,
blue-toned skies with no snowfall — real seasonal character in the shoulder months without
touching your rule.

## But variety costs more than I said

I claimed one list entry equals one weather. **That is wrong.** Seasonal scoping works by
duplicating a weather onto another season's counter. Your own patch proves it: 410 entries across
34 regions carrying only 338 distinct weathers — 72 duplicates, and every one of the 34 regions
has at least one weather occupying two entries.

**A weather wanted in two seasons costs two entries.** So the coverage estimates in section 8b
were optimistic. Real anchors: the shipped framework patch for another weather mod peaks at 27
entries; your current patch peaks at 21. There is no hard 30 limit — I made that up and withdraw
it.

## Cross-casting is narrower than I said

Snow Mountains has the strongest positive green shift of all nine families plus a blue-violet
tint, constant across every rung. **Cross-cast into a green summer hold it will frost the
foliage** — the same visual failure the snow line pin was created to prevent.

**Only Reach and Falkreath are genuinely neutral cross-casts.** Reach is the faintest of the nine
with a slightly negative green shift; Falkreath has a zero green shift. Everything else carries
enough tint to read as "wrong place" rather than "different season" when moved.

Hjaalmarch and Eastmarch are separated from the rest by fog and god-ray tier — on a clear rung
they run about 30 times the fog and 31 times the god-ray spread of the other seven. That is a
place signature, not a season signature. Keep them local.

---

# 8e. THE REGION CENSUS — CORRECTED NUMBERS

- **42 gated exterior regions, not 43.** Fallowstone is won outright by Lux with a single Lux
  weather at 100 percent, so its seasonal wiring is already dead today, before Picta.
- **No fourth gating source exists.** All 4322 plugin files were scanned for the framework as a
  master: nine hits, all accounted for.
- **Picta carries 66 regions** — 65 overrides plus one new. 57 carry weather entries, 9 do not.
- **9 regions end up with a completely empty weather list**: both Soul Cairn outskirts, Forgotten
  Vale Canyon, all four Mind of a Madman worlds, the Shrine of Boethiah, and Darklight Tower.
- **25 regions have no snow weather at all** and need one appended at zero chance on the autumn
  and winter counters.
- Picta's chances are not uniform: 380 entries at 10, 15 single-weather regions at 100, and
  Labyrinthian Maze at 70/15/10/5.

## A trap for the authoring pass

**Picta's region EditorID tags lie.** Japhet's Folly is tagged as the coast family but every one
of its ten entries is a pine-forest weather. All four Forgotten Vale regions are tagged as a
Forgotten Vale family but use snow-tundra weathers. **Match regions to families by the weather
records they actually list, never by the tag in the name.**

---

# 9. WHAT I NEED FROM YOU

1. **Confirm the casting.** Falkreath spring, Whiterun summer, Rift autumn, snow families
   winter. Or tell me a different mapping.
2. **Summer versus autumn.** Accept them close, or let me strengthen autumn's foliage rotation
   and summer's green/yellow saturation? The autumn foliage move may need a hue change, which
   needs your explicit yes under your own colour rule.
3. **Shoulder seasons.** Snow in autumn as well as winter, as your current patch does? Or
   winter only?
4. **The melted holds.** Rain in spring, summer and autumn, with snow returning in winter only?
   Or keep a light autumn snow there too?
5. **Solstheim and the Forgotten Vale.** They have no Picta preset files at all. Options are:
   borrow another family's files, author files for them, or leave them out of the seasonal
   wiring and accept a flat sky there. This one is genuinely open.

---

# 10. ORDER OF WORK, WHEN YOU SAY GO

1. Fix the routing first — generate the flat weather list, fill the four missing families,
   repair the fallback. Without this every Picta weather is a grey canvas and nothing else
   matters.
2. Rebuild the seasonal snowfall patch on Picta with your autumn/winter policy intact.
3. Add the four-season casting on top of the same records.
4. Add the snow-belt melt.
5. Then the separate jobs: Wyrmstooth, Extended Cut, Gray Cowl, and the Picta integrity repair.

Steps 2 through 4 are one plugin, authored in one pass. Splitting them would mean writing the
same 41 region records three times.
