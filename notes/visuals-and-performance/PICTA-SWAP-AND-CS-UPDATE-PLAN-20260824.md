# PICTA swap + Community Shaders update — PLAN v2
Written 2026-08-24. Profile: DEEZ CS NUTZ. MO2 closed while reading. Nothing changed yet.

v2 supersedes v1. Your decisions are folded in. Six agents plus three adversarial
verifiers went over the seasonal question. Two of my v1 conclusions were wrong and
one of the verifiers was wrong too. All three corrections are in Part 0.

YOUR DECISIONS, RECORDED
- Assets: you want 4K. See 0.4 — the 4K file is archived, not a normal download.
- Order: Community Shaders update first, test, then Picta. Agreed.
- Seasonal and Unfrozen weather: HARD REQUIREMENT, cannot be lost.
- Community Shaders keeps the sun. EVLaS stays off.
- Mists of Tamriel: drop it. See 0.3 — dropping it has one side effect you must know about.
- Silent Horizons shader core: update it.
- Astralite's puddle and rain wetness boosts: carry them into the global settings.
- New ask: account for weather in modded worldspaces. Part 5.

---

# PART 0 — WHAT CHANGED SINCE v1

## 0.1 Seasonal weather CAN be preserved. v1 was wrong to suggest accepting the loss.
I said "accept it". That was wrong and I withdraw it.

The Seasonal Weathers Framework does not swap weather records and does not use SKSE.
It ships 70 season globals plus a month tracker. A start-game quest puts a constant
ability on you. When the game month changes, a script writes a 0-100 number into each
global for that month. In a region record, every weather entry has three parts: the
weather, a fixed chance, and an optional global. When the global is filled, the game
reads the live global instead of the fixed chance. That is the whole mechanism.

Two consequences that decide everything:
1. **There is no patch registration of any kind.** No list, no keyword, no plugin-name
   check, no MCM entry. A patch is just any plugin whose region records point at those
   globals. So a Picta patch is possible without touching the framework at all.
2. **No new weather records are needed.** A patch is region records and nothing else.
   The existing Astralite patch is 35 region overrides and defines zero new records.

So the job is: rebuild the season wiring on top of Picta's regions. Part 4.

## 0.2 A NEW blocker I missed in v1 entirely: Helios.
Helios is not a lighting mod. It makes interiors show a dimmed copy of the weather
happening outside. It defines 85 "twin" weathers, 54 interior weather regions, and
attaches them to 868 interior cells through its Luma configs. A script watches you
change cell, reads the interior's region name, and forces the twin of whatever is
playing outdoors.

The twin is found **by name**. It looks for `Helios_` plus the outdoor weather's name.

Astralite defines zero new weather records, so every weather that can play already has
a twin. **Picta adds around 196 new weathers and repoints every region and climate onto
them.** Of the 112 weathers Picta's regions and climates can actually deliver, Helios has
a twin for exactly **five**.

I checked the Helios menu: there is no off switch, only a debug toggle. Its own tooltip
mentions "fallbacks", so Helios does have a defined path for a missing twin — but two
independent passes disagreed on what that fallback does, and I could not settle it from
the compiled script without writing files. **It is a two-minute in-game test.** See 4.5.

Good news that softens this a lot: Helios's own 54 interior regions carry their own
weather lists made of Helios twins. Those keep working regardless. What degrades is the
outdoor-to-indoor *match*, not interior weather itself.

## 0.3 Dropping Mists of Tamriel breaks one of your own plugins.
I scanned every active plugin's masters. `Mists of Tamriel.esp` is mastered by four
plugins, and one of them is **your own Snowy Holds Seasonal Snowfall patch** — which is
also one of the three plugins carrying seasonal weather.

It is not a problem in practice, because that patch is Astralite-based and is being
replaced anyway. But you cannot disable Mists on its own without breaking it first.
Drop Mists in the SAME session as the Astralite retirement, not before.

## 0.4 The 4K assets file is archived.
The author pulled it. Only 2K is a live main file, which is why you got 2K.
4K is 940 MB to download and 3.1 GB installed. 2K is 308 MB and 875 MB installed.
4K is still fetchable as an old file. Direct manager link:
`nxm://skyrimspecialedition/mods/178136/files/745308`
The author's warning applies: install 4K **or** 2K, never both.
4K is version 1.0.0 and was never re-uploaded, but neither was 2K — both assets files
are 1.0.0 and only the ENB and Plugins files moved to 1.0.1. So 4K is not stale.

## 0.5 A verifier was wrong about the renderer, and it matters
One verification pass concluded Picta's whole ENB preset would be inert here, because
"this build does not run ENB". That is wrong, and I proved it from the live log.

Effects 11 — Community Shaders' ENB emulation — is loaded and running. The log shows it
loading, hooking the sky, compiling the Silent Horizons shaders, and running its weather
manager against the preset's weather list. Two verbatim lines:

    [I] Loading Feature: 'Effects11'
    [W] [WeatherManager] Weather file not found: ...\Data\enbseries\SSECClear.ini

That second line is Effects 11 walking Soul Core's weather list right now. The `[NoDelete]
Effects 11` mod being disabled is a red herring — the AIO build provides Effects 11 itself.

This matters because it decides whether the seasonal patch produces a *visible* season.
See 4.3.

---

# PART 1 — JOB A: COMMUNITY SHADERS UPDATE

Unchanged from v1 except where noted. Summary of the diff: 33 files changed, 12 added,
0 removed. One collision with your hand edits.

## 1.1 What changed
New feature: **Procedural Grass**, alpha, 193 new settings, plus top-down occlusion
shaders that feed grass culling.

Removed feature: **snow melting around fires**. Gone from the shader and the renderer.
Your saved settings still carry four dead fire-melt keys.

Fixes worth knowing:
1. Screen Space GI no longer darkens surfaces close to the camera.
2. Snow Cover foliage tinting can now be switched off per mesh. Relevant to flora colour.
3. Grass collision reworked. 4. Reflection blur 7 steps to 8. 5. Dither strength adjustable.

## 1.2 Your local edits
Nine modified files, seven extra files. Only one collides.

| Your edit | Upstream touched it | Action |
|---|---|---|
| Snow shader foliage hue fix | **YES** | Re-apply by hand. One line. |
| Snow altitude map valley clamp | no | Copy as-is |
| Six snow worldspace configs | no | Copy as-is |
| Effects 11 volumetric ray clamp | no | Copy as-is |
| Notes file and backups | n/a | Copy as-is |

Upstream deleted the fire-melt code from the same snow file. Your fix is a stray multiply
removed from the foliage colour line. The two do not overlap.

## 1.3 Procedure
1. MO2 and game closed.
2. Back up mod folder, saved settings, shader cache.
3. Empty mod folder, copy in the new build.
4. Restore 8 of 9 local files. Re-apply the foliage hue fix by hand to the new snow file.
5. Restore notes and backup siblings. Update mod metadata.
6. Verify only expected files differ from the archive.
7. Move the shader cache aside. Do not delete.
8. Move the defaults settings file aside so the new build regenerates it.

## 1.4 Settings — the trap
A hand-written partial settings block is rejected wholesale and the feature then runs ON.
So: launch once, quit at the menu, let the build write full blocks, THEN edit inside them.

**Snow Cover must be rewritten.** Four dead keys are still in your saved block. Re-save
from the fresh block, then re-apply: physics effect off, snow line pinned, tree tint off
for Tamriel.

**Procedural Grass — expect it ON.** Start it OFF. You have five seasonal grass caches and
the interaction is untested.

**HDR — the pin has drifted.** The file says HDR off but the auto-detect flag is also off,
and that flag being off is exactly what lets the renderer re-enable HDR every launch.
Set it back to true.

**Confirm still off:** Screen Space GI (feature and GI), Sky Gradient, Screen Space
Reflections, all thirteen Post Processing sub-effects, the renderer's screenshot key.

**Confirm survived:** grass subsurface at full, grass mesh LOD off with its two distances,
interior shadow count, hair specular, contact shadows.

**NEW — add the wetness values you asked for.** Astralite's config boosted maximum puddle
wetness and maximum rain wetness above default. Those leave with Astralite. Write them into
the global Wetness Effects block during this step so nothing changes when Astralite goes.

## 1.5 Silent Horizons shader core 1.15 — do it, but know it is small
You asked to update it. It is safe. It is also almost empty.

Against your installed 1.10: 2 files added, 10 changed, 0 removed, 30 identical. Both added
files are SMAA lookup textures that Soul Core already ships byte-identically. The changelog
is one line: shader grafting added to the postpass.

The effect, bloom and adaptation UI headers are **byte-identical** between 1.10 and 1.15, so
those shaders' settings names did not change at all. Only the postpass and shared headers
moved. Picta's four shader parameter files hold 2224 keys and none of them mentions grafting.

So: nothing in 1.15 breaks Soul Core, nothing in 1.15 is required by Picta.

Two things when you do it:
- Update **both** copies — the enabled Data one and the disabled Root Builder one. They are
  byte-identical today and your other three profiles use the Root Builder copy.
- Grafting will stay off afterwards because Soul Core's own compiler config outranks the
  core's. Leave it off.

## 1.6 First launch
Full shader rebuild, about 12 minutes, roughly 3500 shaders. Three folder-creation errors
on first cache write are normal.

---

# PART 2 — JOB B, ENB SIDE

## 2.1 Like-for-like
Picta and Soul Core sit on the same shader core. I compared a Picta weather file against a
Soul Core one: both 37 sections, about 2000 keys. Effects 11 reads the same 16 sections in
both and ignores the same 21. No new loss.

**Read (16):** sky, environment, bloom, lens, fire, particle, rain, water, light sprites,
sun glare, procedural sun, volumetric fog, volumetric rays, game volumetric rays, cloud
shadows, image based lighting.

**Ignored (21):** skylighting, ambient occlusion, objects, vegetation, grass, complex grass,
snow, wet surfaces, rain wet surfaces, eyes, skin specular, underwater, rays, lens flare,
window light, object glow, membrane, sky scattering, complex material, complex fire lights,
complex particle lights. Community Shaders does all of those natively.

## 2.2 Sky colour by time of day
Three layers, all three survive.

**Layer 1 — the ENB time-of-day block.** Soul Core today: sunrise 8, day 13, sunset 18,
night 1. Picta: sunrise 9, day 10, sunset 17, night 20.5. Picta's day window is much shorter
and night starts far earlier.

**Layer 2 — per-weather sky settings, eight time slots each.** Every Picta weather file
carries dawn, sunrise, day, sunset, dusk, night, interior day and interior night values for
sky gradient strength, sky desaturation, stars and aurora. Effects 11 reads all of it — but
only if the file is actually loaded. See 2.3.

**Layer 3 — the game's own sunrise and sunset spans.** Picta sets sunrise 4 to 10 and sunset
16 to 22 from its plugin. Wider than vanilla, so the coloured part of the day stretches at
both ends. For reference, Astralite currently sets 4:30 to 9:30 and 16:30 to 21:30, so this
is a modest widening, not a jump.

Also: Picta lowers the sun's arc to less than half of Astralite's value. Sun sits lower,
shadows run longer. Since you chose Community Shaders to keep the sun, its Sky Sync settings
stay as they are and this is the only sun change.

## 2.3 The routing problem — still the main ENB-side work
Picta routes weather files through the ENB Worldspace Weatherlists helper. Effects 11 has
zero support for it. Effects 11 reads only the plain weather list and the interior list.
Picta's plain list is a leftover pointing at a folder that is not in the 1.0.1 package.

**As shipped, all 100 regional looks never load.** Everything falls back to one base file.

**The fix.** The per-worldspace list is a single file covering every worldspace, so the
routing flattens with no loss. Picta's own list names each weather by its short ID, and I
confirmed those short IDs are the real record IDs with the load-order byte stripped — the
numbers match the region records exactly. Generating a proper flat list is mechanical:
110 entries, scripted and verifiable.

The generated list is tied to where Picta's master sits in the load order. Move it and the
list must be regenerated. The generator goes in the mod folder so a rerun is one command.

**One unknown to test:** Soul Core's list uses flat filenames, Picta's uses folder paths. I
could not prove Effects 11 accepts a sub-folder path there. Fallback is to flatten the 128
files into one folder with unique names. A rename pass, not a rewrite.

## 2.4 The fire key bug, again
Picta writes fire settings under the plain names. Effects 11 wants the prefixed ones. Same
bug you fixed for Soul Core on 08-23. Base file plus 128 weather files plus 11 interior files.

Picta sets fire brightness to 25 in the base file and 5 per weather. Soul Core sits at 1.0
to 1.6. Port the curve values only and leave brightness alone, as you chose before.

## 2.5 The in-game editor preset
Picta's editor preset is packaged inside the ENB folder. The editor's own plugin says
plainly that a preset found in the ENB directory is ignored when ENB is not installed. You
run Community Shaders, so it must be relocated to the editor's own folder, matching how Soul
Core's is packaged.

Only one preset can be active. Soul Core's carries 61 interior lighting templates; Picta's
carries none. Interiors fall back to Lux's authored lighting plus Picta's 11 interior files.
That is a real, visible change indoors — and it stacks with the Helios question in 0.2.

## 2.6 Base settings differences to decide on
Picta turns on things Soul Core deliberately has off: volumetric rays, sun glare, detailed
shadows, normal map shadows, complex fire lights, wet surfaces, ambient occlusion, skin
specular, eye adaptation.

Volumetric rays, sun glare and adaptation are real Effects 11 features. Turning them on
stacks them on Community Shaders' own. Expect double god rays and double glare until settled.
Adaptation is the biggest single change — auto exposure starts moving as you look around.

Start from Picta's file unchanged, see it, then decide.

## 2.7 Not worth chasing
- **LUT grading.** The renderer rejects every shader include, so the core's LUT file has
  never applied on either build. Picta ships an empty LUT folder anyway.
- **The AELAS settings file.** AELAS is a separate sun simulator you do not have, and you
  chose Community Shaders for the sun. The only difference between the two files is the
  time-of-day block. Skip it.
- **Picta - ENB Game Tweaks.** Its three settings are already in Picta's master with
  identical values. Redundant, as the mod page says. Do not install.
- **The local ENB settings file** in the download. Only real ENB reads it.

---

# PART 3 — JOB B, PLUGIN SIDE

## 3.1 What the plugins contain
Master, full-size, costs one load slot:
218 weathers, 45 volumetric lighting records, 10 image spaces, 54 particle definitions,
319 sounds, 21 sound categories, 25 game settings, 9 statics, 1 climate, 1 region, 1 spell.

Second plugin, light, no slot cost:
65 regions, 8 climates, 4 weathers, 3 image space modifiers, 45 sounds, 24 worldspace copies,
46 cell copies, and 1243 new placed objects — the sky and fog props.

Budget: you are at 241 full slots of 254. Picta's master costs one. Retiring Astralite frees
several. No pressure.

## 3.2 Load order — your hard rule holds
Picta's page says load its second plugin after the LOD output. I checked what your LOD,
occlusion, map and water tail plugins actually touch: between them, zero climates and zero
regions. Those are the only records Picta needs to win. Picta's worldspace and cell copies
are forwarding copies with vanilla values — losing them costs nothing and avoids Picta
overwriting your water settings on 16 worldspaces.

The 1243 props are separate records and load regardless of who wins the cells around them.

**Picta goes where Astralite is now, above the output block.** No exception needed.

Standing note for the LOD runbook: if you ever regenerate LOD, disable both Picta plugins
first or the sky props get duplicated.

## 3.3 The dependency cascade — exact, scanned from every active plugin's masters
Retiring Astralite is not one switch. `Astralite Weathers.esp` is mastered by **eight**
active plugins and `Astralite ENB.esp` by four. Dropping Mists of Tamriel kills four more.

Everything below must go in ONE session:

Dies with Astralite Weathers:
- Astralite ENB.esp
- Wyrmstooth-Astralite-Weather-Patch.esp
- Astralite ENB - ECSS.esp
- Helios_Astralite.esp
- Helios_Astralite_Seasonal.esp
- Authoria - Patch - Gray Cowl - Astralite.esp
- Authoria - Patch - Snowy Holds Seasonal Snowfall.esp   ← one of your three seasonal plugins
- Authoria - Patch - Astralite Dawn Warmth.esp           ← already a no-op

Dies with Mists of Tamriel: Astralite ENB, the Wyrmstooth patch, Snowy Holds, Dawn Warmth.
All four are already on the list above, so dropping Mists costs nothing extra **provided you
do it in the same session**.

Also retire: Astralite Weathers 4K Clouds, Reverb Interior Sounds - Astralite, the Soul Core
ENB data and editor templates, and the two Soul Core compatibility patches.

**SURVIVES, and this is important:** `Seasonal Weathers Framework - Astralite Weathers.esp`
does **not** master Astralite at all. Its masters are Skyrim, Dawnguard, Dragonborn and the
framework. It stays loadable. See 4.2 for why that is both useful and dangerous.

**Also survives untouched:** `Helios.esp` masters only vanilla. All 85 interior twins and 54
interior regions stay. Only the Astralite-flavoured retune dies.

## 3.4 Sound
Picta replaces 364 weather and ambience sound records. You run an audio overhaul and a
thunder sound mod. Load order decides who wins. Test thunder and rain specifically.

---

# PART 4 — THE SEASONAL CHAIN (your hard requirement)

## 4.1 What "seasonal" actually is in this build — two independent systems
**Unfrozen is safe. Do not spend effort protecting it.**

I checked all 362 Seasons of Skyrim configuration files across 51 mods. Their sections are
only Worldspaces, LandTextures, Statics, Trees, MovableStatics, Activators, Flora, Furniture,
Grass and Blacklist. **Not one contains a weather section.** No Unfrozen-named plugin touches
a weather, climate or region record. Unfrozen is a snow-removal system for terrain textures
and static meshes, nothing more.

Picta and Unfrozen also do not collide on cells: none of Picta's 46 cell overrides is touched
by any Seasons or Unfrozen plugin, and 1198 of Picta's 1243 props sit in worldspace persistent
cells, so they add nothing on top of Unfrozen's terrain work.

**Seasonal WEATHER is the separate thing at risk.** It comes from three plugins:
1. `Seasonal Weathers Framework - Astralite Weathers.esp` — 35 exterior regions
2. `Authoria - Patch - Snowy Holds Seasonal Snowfall.esp` — your own, ~34 exterior regions, currently the winner
3. `Helios_Astralite_Seasonal.esp` — 35 **interior** regions

Between them they gate 43 exterior regions plus the interior set. **Picta's ESP overrides 35
of those 43 exterior regions, and every one of Picta's 397 region weather entries has a null
global.** Installed as-is under the seasonal patches, seasonal weather dies in 35 of 43 regions.
Installed over them, Picta's weathers never play in those regions. The two cannot both win.

## 4.2 The plan: two new patches, in two tiers

### TIER 1 — required. This is what protects your hard requirement.

**Patch A — `Authoria - Patch - Picta Seasonal.esp` (exterior).**
- Light plugin. Masters: Skyrim, Dawnguard, Dragonborn, Picta's master, Picta's ESP,
  Seasonal Weathers Framework.
- Content: **region records only**, about 42 of them. No new weathers, no climates, no cells.
- Method: copy each region from Picta's version so its shape, sounds, map colour, priorities
  and flags come across untouched, then fill the global field on every weather entry.
  Picta's slot numbering makes the mapping mechanical — slot 01 clear to the "pleasant A"
  global, 02 to 05 to "pleasant", 06 and 08 to "overcast", 07 to rain or snow, 09 and 10 to
  storm. Use the framework's snow-region lane for Picta's snow families.
- Then the part that actually matters: Picta's rain regions contain no snow weathers and its
  snow regions contain no rain weathers. Globals alone cannot give Falkreath a winter. So
  append extra entries at chance zero, borrowing Picta's own weathers from the paired family,
  and point each appended entry at the matching winter or summer global. This is exactly what
  the Astralite and NAT patches do.
- Disable all three existing seasonal patches at the same time. If any is left below the new
  one it overwrites the whole list and undoes the swap.

**Patch B — `Authoria - Patch - Helios Seasonal.esp` (interior).**
This one is a pleasant surprise. Helios's interior regions roll **Helios's own twin weathers**,
not Astralite's and not Picta's. So an interior seasonal patch needs **no Picta dependency at
all** — its masters are just Helios.esp and the framework.
- Content: ~35 interior region records, rebuilt from `Helios_Astralite_Seasonal.esp` with the
  Astralite and Astralite-patch masters dropped.
- This restores interior seasonality completely and cheaply.

### TIER 2 — optional, large, cosmetic.
**`Helios_Picta.esp` — interior weather twins matched to Picta.**
Restores the outdoor-to-indoor weather *match* described in 0.2. Needs roughly 107 brand-new
twin weather records plus 85 overrides. That is a big job and it is not required for
seasonality. Do it later, or not at all, depending on the test in 4.5.

Before committing to Tier 2: the Helios author already lists a Picta patch as in progress on
the mod page. Worth asking there first.

## 4.3 Will the seasons actually LOOK different? Yes — and here is the proof
This was the sharpest disagreement in the review, and both sides were half right.

A verifier byte-compared Picta's green and snow weather **records** and found them nearly
identical: same sky, fog, sun, star and ambient colours, differing only in four cloud texture
paths and a tiny ambient nudge. On that basis it concluded winter would look like summer.

That is true of the records. It is **not** true of what you will see, because Effects 11 grades
each weather from its own ENB file, and those files are very different. I diffed the Whiterun
Tundra clear-day file against the Snow Tundra clear-day file: **202 changed values.** The
direct-light colour goes from neutral white with a warm orange dawn to a cool blue-white with a
pink dawn. Ambient desaturation drops from 0.6 to 0.2 across the day. Direct-light desaturation
goes from -0.5 to 0.

So swapping a region to the snow family in winter gives you a genuinely colder picture — warm
neutral becomes cool blue — **provided the routing fix in 2.3 is done.** The seasonal patch and
the ENB routing fix are coupled. Neither is worth much without the other.

## 4.4 What seasons you will actually get
Picta has no spring, summer and autumn variety within a single terrain. It has a green family
and a snow family per terrain, and only two of the pairs line up cleanly rung for rung
(Whiterun Tundra with Snow Tundra, Reach Mountains with Snow Mountains).

So the honest result is **winter versus not-winter**, well differentiated, with spring, summer
and autumn sharing one look per place. That is a real reduction from what Astralite gives you.

Four families have no snow twin — Falkreath pine forest, Hjaalmarch marsh, Rift fall forest and
Eastmarch volcanic tundra. They would borrow Snow Tundra for winter, which means those holds
share a winter sky. Astralite already makes a similar compromise.

Optional extra: the permanently snowy belt (the Pale, Winterhold, Windhelm, the mountains)
could melt to rain in summer by adding the paired green family's rain rungs under the
non-winter globals. Another ~11 records.

**Decision for you:** four seasons, or winter-versus-not-winter? Picta only supports the second
cleanly. See Part 9.

## 4.5 The two-minute test that settles the Helios question
Helios has a debug toggle in its menu. Its own tooltip says it reports "weather changes, weather
region, and fallbacks".

After Picta is in: turn the debug toggle on, stand outside until a weather is running, then walk
into any interior. Helios will print the outgoing weather, the twin it looked for, and what it
fell back to. That tells us in one screenshot whether Tier 2 is needed or whether the fallback
is acceptable. Do this before committing to 107 new records.

---

# PART 5 — MODDED WORLDSPACES

## 5.1 The good news first
Roughly 50 modded worldspaces get nothing from Picta's ENB preset, because Picta covers only
24 vanilla and DLC worldspaces. Today they get nothing bespoke either — Soul Core's weather list
covers vanilla plus two small patches. So the ENB layer is close to a wash.

The two Soul Core patches you do lose bespoke coverage from are the Extended Cut and Wyrmstooth
ones. Worth noting: Effects 11's log already reports four of Soul Core's own weather files
missing, including both Extended Cut entries, so part of that coverage is already dead today.

## 5.2 The real problem: Picta repurposes four common vanilla weathers
A large number of modded worldspaces have no weather of their own — they roll plain vanilla
Skyrim weather records. Unslaad's six worldspaces, Olenveld's main world, Legacy of the
Dragonborn's Sancre Tor and Pale Pass, five Vigilant worldspaces, and all of Beyond Skyrim
Bruma are in that group.

Picta renames four vanilla weathers into one-off cinematic main-quest weathers:
- Skyrim's plain cloudy becomes the Helgen intro scene
- Skyrim's fog becomes the prison-cart scene
- Skyrim's snow storm becomes the dragon-altar scene
- The Helgen attack weather becomes the dragon-attack scene

So Bruma's fog would become a prison-cart sky and Unslaad's blizzard a dragon-altar sky.

**Fix: a four-record forward patch** restoring sane weather to those four records for the mods
that still roll them. Small and safe.

## 5.3 The general-purpose climate
Picta collapses the main Skyrim climate to a single weather — a thunderstorm at 100 percent.
Astralite already collapses it to a single weather too, so the structure is not a regression,
but the content changes from "cloudy" to "thunderstorm". Any small modded worldspace that falls
back to the climate rather than a region list would sit under a permanent thunderstorm.
**Fix: one record**, changed to a calm Picta weather.

## 5.4 Picta ships broken references — this needs repairing regardless
Independent of anything else, Picta 1.0.1 has integrity bugs. Twelve weather links in its own
region and climate records point at record IDs Picta never defines. **Seven regions are left
with an empty weather list.** The affected places are Darklight Tower, the four Mind of a Madman
worlds, the Shrine of Boethiah, Forgotten Vale Canyon, two Soul Cairn outskirts regions, and the
Volkihar Castle Isle. The Soul Cairn climate also points at a missing record.

Darklight Tower is one of the 43 seasonally gated regions, so Picta does not merely strip its
seasonality — it breaks its weather outright.

**Fix: rebuild those lists from Picta's own shipped weathers.** Around 8 to 12 region records
plus one climate. Worth reporting upstream too.

---

# PART 6 — ASSETS AND FILE COLLISIONS

Picta ships 576 asset files. 227 collide with a loose file from an enabled mod, but 167 of those
are byte-identical, so only **60 are real collisions**.

**Keep enabled, place BELOW Picta:** `Picta Series - Improved Sky Meshes`. It is a strict
superset of 160 of Picta's sky meshes and **Picta's own plugin depends on four of its meshes**.
Do not remove it.

**Keep enabled, place ABOVE Picta:** `Praedys Sky AIO`, so it keeps the stars mesh. Its version
is denser and pairs with its own star, constellation and galaxy textures. Picta's plugin also
needs two of Praedy's aurora meshes.

**Picta should WIN:** the six Astralite sky textures (sun, sun glare, Sovngarde eye and nebulas —
Astralite is the mod being replaced), the clouds mesh (Picta's is a six-times-denser rebuild that
its weather files are authored against), and every path currently served from a BSA.

**Picta should LOSE:** Lux's 37 low-mist meshes (Lux's carry interior variants its cells
reference), Rudy's 7 falling-leaf meshes, Lamae's Gaze's 2 vampire eye meshes, and the mesh-fix
compilation's camera-attach mesh. All four already sit above Picta at the install position below.

**Install position: around modlist line 3170**, below Lux, Rudy Falling Leaves and Lamae's Gaze,
above Astralite. That resolves 46 of the 60 real conflicts correctly with no manual rules.

**Two more:** you can drop `Less Distracting Blowing Snow Effects - ENB Particle Patch` — Picta
ships the same four files byte-for-byte. And decide whether you want Picta's vampire eye meshes
at all; if not, delete the actors folder from the install.

**ParallaxGen has zero overlap** with any Picta path, so there is no unprocessed-neighbour problem.
Every texture Picta's 263 meshes reference resolves in the current build — no missing textures —
except two broken references inside Picta's own plugin that the asset pack does not satisfy.
One is a Blackreach aurora mesh. Check whether the 4K pack contains it; if not, report upstream.

---

# PART 7 — THE FIXES WE KEEP

## 7.1 Renderer settings
1. HDR off, auto-detect flag pinned true. **Currently drifted — fix during Job A.**
2. Screen Space GI off, feature and GI. This was the real cause of the exterior colour cast.
3. Sky Gradient off. This was the magenta frame.
4. Screen Space Reflections off.
5. All thirteen Post Processing sub-effects off.
6. Renderer screenshot key unbound.
7. Snow physics effect off.
8. Interior shadow detail at 4.
9. Grass mesh LOD off with its two distances.
10. Grass subsurface at full.
11. **NEW:** Astralite's puddle and rain wetness boosts, written into the global block.

## 7.2 Hand-edited shader files
1. Snow foliage hue fix. **Collides with the new build.** Re-apply by hand.
2. Effects 11 volumetric ray negative clamp.
3. Snow altitude map valley clamp near Magpie Manor.
4. Six snow worldspace configs: snow line pinned, tree tint off for Tamriel.

## 7.3 ENB preset fixes to re-apply to Picta
1. The fire key-name fix, about 140 files.
2. Confirm no shader include errors at first launch. Picta ships no shader files, so the
   depth-of-field problem should not recur.

## 7.4 Nothing to port from the colour work
The Astralite dimming project was fully reverted on 08-22 and that plugin defines nothing.
The lesson carries, not the data: if a colour is too strong, change strength only — hue and
brightness stay identical.

## 7.5 Stay off
The purple flora retint, the blue flower soft-light mod, the Astralite ambient warmth patch,
night saturation floor at preset default.

---

# PART 8 — WORK INVENTORY

Job A — Community Shaders update: half a day including your test run.

Job B — Picta swap:
| Piece | Size | Required |
|---|---|---|
| Three mod folders built and laid out for Effects 11 | small | yes |
| Flat weather list generated, 110 entries | scripted | yes |
| Fire key fix across ~140 files | scripted | yes |
| Editor preset relocated | small | yes |
| Load order rewiring, 4 profile files | medium | yes |
| Patch A — exterior seasonal, ~42 region records | medium | **yes** |
| Patch B — interior seasonal, ~35 region records | small | **yes** |
| Picta integrity repair, ~8-12 regions + 1 climate | small | **yes** |
| Vanilla weather forward for modded worldspaces, 4 records | small | yes |
| Climate calm-weather fix, 1 record | tiny | yes |
| Patch C — Helios Picta twins, ~190 records | large | no, test first |

---

# PART 9 — DECISIONS STILL OPEN

**9.1 Four seasons, or winter versus not-winter?** Picta only supports the second cleanly.
Four seasons means every hold shares one spring look and one autumn look. I suggest
winter-versus-not-winter, because it is the one Picta's data actually supports and it is
where the visual difference is real.

**9.2 Should the snow belt melt in summer?** The Pale, Winterhold, Windhelm and the mountains
are snowy year-round today. Making them rain in summer is about 11 extra records. I suggest
yes — it is the clearest sign the seasons are working.

**9.3 Tier 2 Helios twins — build, skip, or wait?** I suggest running the debug test in 4.5
first, and asking the Helios author whether their Picta patch is close.

**9.4 4K assets — fetch the archived file, or stay on 2K?** You said 4K. Confirm you want the
archived download, given it is 3.1 GB installed.

**9.5 Bespoke coverage for Extended Cut and Wyrmstooth.** Soul Core has patches for these that
Picta has no equivalent of, and two of them are already broken today. Rebuild, or let them fall
back to Picta's base look?

---

# PART 10 — EXECUTION ORDER

## Job A
1. Confirm MO2 and game closed.
2. Back up mod folder, saved settings, shader cache.
3. Replace mod folder with the new build. Restore 8 of 9 local files.
4. Re-apply the foliage hue fix by hand. Restore notes and backups. Update metadata.
5. Verify against the archive. Move shader cache and defaults settings aside.
6. Update Silent Horizons core to 1.15 in **both** mod folders.
7. **You launch and quit at the main menu.** I do not launch the game.
8. I edit the freshly written blocks: the eleven items in 7.1, rewrite the snow block on the
   new schema, set procedural grass off.
9. **You play-test.** Grass, snow line, exterior colour, interiors, water.

## Job B
1. You fetch the 4K assets file if you want it.
2. I build the Picta mod folders, generate the flat weather list, apply the fire fix, relocate
   the editor preset.
3. I author the four required patches: exterior seasonal, interior seasonal, Picta integrity
   repair, modded-worldspace weather forward plus the climate fix.
4. I rewire the load order in one session: retire the Astralite and Soul Core set, drop Mists,
   insert Picta above the output block at around line 3170, place the new patches last among
   the weather plugins. All four profile files including the group file.
5. I verify: no missing masters, no errors, Picta wins weathers, climates and regions, and the
   seasonal patches win the regions they must.
6. **You launch.** Run the reload-climate console command once, since this is an existing save.
7. **You test.** Part 11. Turn the Helios debug toggle on for the first interior.

Nothing is written until you say go. MO2 closed for every write.

---

# PART 11 — TEST PLAN

1. Main menu loads. Log clean of shader errors and rejected settings blocks.
2. Outside at midday. Sky, clouds, distance haze.
3. Wait to 6am, 9am, 6pm, 9pm, midnight. Dawn and dusk are where Picta differs most.
4. Move between two regions with different Picta looks — the tundra and the pine forest.
   **If they look identical, the weather routing failed.** This is the single most diagnostic test.
5. Force a storm and a snowstorm.
6. Enter a house and an inn, with the Helios debug toggle ON. Read what it says about the twin.
7. Stand next to a fire, indoors and out. Confirms the fire fix.
8. Set the month to a winter month and re-check step 4. **Confirms seasonal weather.**
9. Set the month to a summer month and re-check. Confirms the other side of the gate.
10. Go to Solstheim. The ash region ships with no Picta ENB files — expect fallback.
11. Visit a modded worldspace that rolls vanilla weather. Bruma is the easy one.
12. A town at morning. Solitude is the reference case.
13. Water and puddles after rain, to confirm the wetness values carried.

---

# PART 12 — ROLLBACK

**Job A:** restore the mod folder, saved settings and shader cache from backup. Five minutes
plus a recompile.

**Job B:** the Astralite, Soul Core and Mists mods are never deleted, only switched off.
Restore the four profile files from their dated backups and flip the mods back on. All four
profile files must be restored together.

Every profile file gets a dated backup before any edit.
