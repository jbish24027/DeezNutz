# Astralite + Soul Core on Community Shaders / Effects 11 — Swap Plan (v2)

Written 2026-08-09, revised same day after archive-level analysis of the 33 staged downloads.
Working profile: **DEEZ CS NUTZ** (active; clone of the ENB-era list with LOD outputs + grass caches
deliberately disabled). **DEEEZ NUTTZZZ stays untouched as the NAT+AMON ENB fallback.**
All 33 archives are staged in `C:\1. AUTHORIA\downloads\` (0.39 GB, copied 2026-08-09).

## EXECUTION STATUS — 2026-08-09

Phases 0–4 file work is **DONE and verified** (houseCARL: 3798 mods enabled / 86 disabled; 3976 active
plugins = 3976 resolved, zero unresolved, zero missing masters; 13 inactive incl. the 11 retired NAT/AMON
lane + TerrainHelper.esp, whose only provider was the disabled Terrain Helper mod — matches Net's stack):
- 20 ENB-lane mods disabled; 23 mods installed ([NoDelete] CS/E11/wind/weather lanes + 2 restored authored
  patches); ENB Extender updated 1.4.2 → 1.4.3 in place; Soul Core preset built as Root Builder mod.
- 11 plugins deactivated (incl. AMONENB.esp — no dummy existed — and TerrainHelper.esp); 11 inserted at
  exact slots; plugingroups updated; FOMOD picks as decided (SWF patch only; no nights/moon/volume patches;
  Lux CS "Effect 11" + "Lux Orbis Tweaks").
- Profile snapshot: `profile-backup-pre-astralite-cs-20260809`. Play profile DEEEZ NUTTZZZ untouched.

**TRIPLE-CHECK PASS (same day, user-requested) — one real seasons bug found and FIXED:**
- `Astralite ENB.esp` (Soulmancer's region-variation edits, 35 REGN) was clobbering the SWF-Astralite
  patch in 26 of 35 weather regions — his entries carry `Global=(null link)` where SWF's carry the
  `Season_*` globals, so seasonal weather gating was dead in every major region (verified by field diff
  on WeatherPineForest). **Fix applied:** SWF-Astralite moved to load AFTER Astralite ENB.esp → now wins
  34/35 (verified). Cost: Soulmancer's extra per-region weather-mix entries in those regions; his weather
  STYLING is unaffected (he still wins all WTHR records). Order is now: DynamicWindSkyrim → MoT →
  Astralite Weathers → Astralite ENB → SWF-Astralite → WT patch → ECSS patch.
- Coverage delta vs NAT era: old SWF-NAT patch = 40 regions; Astralite's = 35. Dropped: Karthspire
  Redoubt, DLC01Weather02/03 (Forgotten Vale area), VolcanicAsh01/02 (Solstheim). Low impact (ash/frozen
  areas); optional future extension patch could forward globals into those 5.
- `WeatherFallowstone` is won by Lux.esp (no globals) — TRUE UNDER NAT TOO (Lux loads after both SWF
  patches); pre-existing list state, left alone.
- Snow classification: 41 snow-flagged weathers, Astralite lane wins its set (18 + WT patch 1);
  NAT-ENB.esp's 7 flagged customs are dormant orphans (nothing active references them).
- Soulmancer's "load after landscape mods" ini rule: satisfied — none of the landscape/tree/grass mods
  after the weather block ship plugin-paired inis, so Soul Core's tuned `Astralite Weathers.ini`
  ([Display] SAO/grass/shadow keys) has no later competitor.
- `Authoria - Patch - SRC - NATENB.esp`: verified harmless — its CELL/WRLD overrides do NOT win (later
  plugins own them) and its live effect is exactly 2 scenery refs (position/rotation/scale + a
  LocationReference), weather-agnostic. No re-author needed; chip withdrawn.
- Authored Gray Cowl patch verified live: wins GC's 2 weathers + 2 climates. ECSS patch = 4 WTHR +
  4 volumetrics + 1 imagespace (SEC regions revert to SEC's own now that SEC-NAT3 is inactive). SWF base
  esp confirmed as the 71-global + MCM framework; its region Sounds lists (incl. Dawnguard's entry) are
  correctly carried by both Astralite plugins.

**HELIOS INSTALLED 2026-08-09 (later same day):** archive re-downloaded (181533 v1.01, staged). Selection
decoded from ModuleConfig and mirrored from stock (installed Helios.esp hash-matched the **Radiant**
variant): Weathers=Astralite → `Helios_Astralite.esp` (Default folder base) + conditional
`Helios_Astralite_Radiant.esp` + SWF=Yes → `Helios_Astralite_Seasonal.esp`; Helios.esp base unchanged
(already Radiant); Lux + the 8 JK interior patches unchanged (JK Winking Skeever/Temple of Divines not in
list → their patches stay skipped); **added the Ryften window patch** stock had skipped (6 Luma jsons for
vanilla Riften interiors — Authoria runs RYFTEN window add-ons); NAT Helios esps left on disk, inactive.
3 plugins inserted at the old Helios NAT slots (group: Lighting - Lux Patches). Verified: 3979 active =
3979 resolved. Architecture verified: Helios keeps a PARALLEL record space (its own Helios_Weather*/
Helios_Region* copies — all 84 WTHR + 54/35 REGN it touches are `xxx:Helios.esp`, zero overrides of real
weather/region records) → it cannot clobber Soulmancer's styling or SWF gating; its Seasonal esp masters
the SWF-Astralite patch (season-aware, mirrors stock NAT wiring: NAT Seasonal had 40 records, same
pattern). Vanilla-region winners re-verified after install: SWF-Astralite 34/35 + Lux 1 — unchanged.

**SNOWY-HOLDS SEASONAL SNOWFALL PATCH (2026-08-09, after the user asked "what about Unfrozen —
Dawnstar/Winterhold/Windhelm should never snow in spring/summer"):** investigation proved the SWF
FRAMEWORK's shipped defaults keep snowy-region snowfall chances nonzero YEAR-ROUND (SN snow: Jun 25 /
Jul 20 / Aug 25 + storms 20–25; spring 30–50) — the region patches gate by `SN_Season_Common_Snow*`
globals whose month values live in the save/MCM, so nothing structural stopped summer snow over
Unfrozen's green ground (true in the NAT era too unless the MCM was tuned). Fix (user-chosen):
authored **`Authoria - Patch - Snowy Holds Seasonal Snowfall.esp`** (mod folder `houseCARL - Authoria -
Patch - Snowy Holds Seasonal Snowfall`, group Authoria - Custom Patches, slotted after the Reverb
Astralite patch) overriding 6 regions on top of the SWF-Astralite patch — WeatherSnow (Dawnstar/Pale),
WeatherWinterhold, WeatherWindhelm + Solstheim's WeatherDLC2SolstheimSnow/SnowHeavy/SkaalVillage01
(included because the authored Solstheim seasons mod dresses the north seasonally: snow materials
winter-only). Each region's 2 snow entries re-keyed `SN_Common_Snow{,_Storm}` → `SN_Season_Autumn_*`
plus appended winter-keyed duplicates → snowfall possible Sep–Feb, **structurally impossible Mar–Aug**
(season globals are script-zeroed outside their season), MCM/save-proof. Verified: field-level readback
clean, check_errors 0/0/0, patch wins all 6 regions, 3980 active = 3980 resolved. Mountains and other
SN regions intentionally untouched (white peaks may snow year-round; MCM SN sliders still govern them).

**TERRAIN HELPER CORRECTION (2026-08-09, caught by the user via MO2's Missing Masters warning):**
disabling "Terrain Helper for ENB" was WRONG for Authoria — `Vanaheimr Landscapes.esp` (active) has
`TerrainHelper.esp` as a MASTER. Net's guide unchecks the mod in HIS list (no consumer there), and
July's Bottle build kept the slot filled because Bottle's AIO shipped its own copy; official CS 1.8.3
ships no esp. FIXED: mod re-enabled + `*TerrainHelper.esp` restored at its original slot (after
StormLightning.esp) in plugins/loadorder + plugingroups re-added (Visuals - Weather & Sky). Its
content (placement esp + helper meshes) is renderer-agnostic. LESSON (MO2 behavior): on close MO2
PRUNES plugins whose file no longer resolves — the 7 deactivated NAT/AMON-lane lines with disabled
provider mods (AMONENB, Bizarre Shadow Fix, WT-NAT, SEC-NAT3, GCN10th, SWF-NAT, TerrainHelper) were
dropped from plugins.txt/loadorder.txt; inactive-but-resolvable lines survive (Lux - NAT ENB, Helios
NAT ×3, Reverb-NAT). Original slots live in `profile-backup-pre-astralite-cs-20260809` if the ENB lane
is ever restored on this profile (DEEEZ NUTTZZZ unaffected). FULL-ORDER INTEGRITY SWEEP run after the
fix: 3,979 plugins scanned, **0 missing masters** (TerrainHelper was the only one of its class — and
with zero deactivated plugins mastered by anything active, dangling refs into them are structurally
impossible); 4,353 dangling refs are pre-existing vanilla/list background (sample = Skyrim.esm's own
dirty CWTestHold/region refs); unscannable: 2 DBVO plugins + 4 Kaidan dialog + 1 Requiem Special Feats
record — all pre-existing parse quirks, unrelated. Final: 3,800 mods enabled, 3,981 active = 3,981 resolved.

**FIRST-LAUNCH FIXES (2026-08-09, after user feedback — dark AP start room / bright Moorside +
heavy bloom / SUMMER SNOW IN MORTHAL):**
- **Snow root cause found:** Astralite adds snow *Precipitation* (Sakura particles) to AMBIENT weathers
  vanilla never precipitates — CloudySN/_A, FogMA, FogCO, CloudyMA_A, the two DLC1 FV cloudies — and
  those ride Pleasant/Overcast globals that stay nonzero in summer. Morthal = FogMA snowing through the
  marsh fog. This bypassed every snow-global gate including the holds patch.
- **Fix, per the user's "everywhere with seasons" directive** (all inside `Authoria - Patch - Snowy
  Holds Seasonal Snowfall.esp`, now 34 regions + 8 weathers, wins all 42, check_errors clean):
  precipitation stripped from the 7 ambient weathers + WyrmstoothStormFog (ambiance stays year-round,
  vanilla-parity; real snowfall only from true snow weathers) + Common/ungated true-snow entries
  re-keyed to Autumn+Winter global pairs across 28 more regions (20 mainland incl. Morthal's
  TundraMarsh, 3 LOTD worlds, 2 Bruma, 3 Wyrmstooth). Deliberately skipped: Glenmoril's 100%-snow
  perpetual zones, Forgotten Vale/Skuldafn/quest-ambiance weathers, NoPrecip regions, ash weathers.
- **Interior fix deployed (route B):** KreatE re-enabled + new mod `[NoDelete] Soul Core - KreatE
  Templates` (Soulmancer's 73 Lux lighting-template DALC fixes from the preset payload; Preset.ini
  auto-selects "Soul Core"). This is the author's own answer to interior template variance.
- **User in-game checks:** (a) bloom — Effects 11 menu → enbbloom.fx section (Soul Core's bloom is
  E11-tunable), and verify CS HDR is OFF; (b) dark start room — 30-second isolation: toggle
  Skylighting off in the CS menu while in the room (if it brightens, it's Skylighting hitting a
  behaves-like-exterior cell), then toggle E11 UseEffect off (isolates preset grading); report which
  toggle moves it. KreatE templates should already normalize normal interiors like Moorside.

**REMAINING:** Reqtificator (user — re-run it now that the snow patch gained masters/records) → Phase 6 first launch → Phase 7 generation runs
→ Phase 8 sweep. Watch-items: Helios GetRegion CTD (authored fix gone post-hotfix; recover from delta
bundle if region-transition CTDs appear; MMSF 183073 still absent = Helios suspect #2). SRC-NATENB patch:
verified harmless (live effect = 2 scenery refs; CELL/WRLD overrides lose to later plugins) — no action.

## The architecture

**Effects 11 replaces ENBSeries entirely — CS is the only renderer.** Effects 11 (Nexus 179824) is a
CS feature that executes ENB preset `.fx` configs natively. Hard incompatibilities: ENB binary,
KiLoader, EVLaS. Soul Core is a Silent Horizons 2 Shader Core preset — the SH2 rules apply:

- **ENB Extender and Helper stays** (E11 extracts the SH2 decryption key through it) — must be **v1.4.3** (installed: 1.4.2).
- **KiLoader must NOT be installed.** **Silent Horizons 2 - Shader Core stays enabled.**
- No `d3d11.dll` in game root = CS active. `ENB Binary Files` stays off.
- PumboAutoHDR is already integrated into Effects 11; nothing to install. Leave CS HDR off (preset is SDR-tuned).

**CS 1.8.3 core bundles 26 features** (verified from the zip): CloudShadows, **SkySync**, TerrainShadows,
TruePBR, UnifiedWater, LODBlending, GrassLighting, GrassCollision, LightLimitFix, InverseSquareLighting,
ExtendedMaterials, ExtendedTranslucency, ImageBasedLighting, InteriorSun, ScreenSpaceShadows,
SubsurfaceScattering, VolumetricLighting, VolumetricShadows, WaterEffects, DynamicCubemaps, HorizonFix,
CSEditor, PerformanceOverlay, RemoteControl, RenderDoc, Screenshot.
→ **Do NOT download separate Sky Sync (153543) or Cloud Shadows (139185) — they're legacy pre-1.8 packages.**
NOT in core (separate mods): **Effects 11** ✓staged, **Skylighting** ✓staged, **Wetness Effects** ✗missing.

## Download status

**Staged ✓ (in instance downloads):** Community Shaders 1.8.3 · Effects 11 1.0.0 · Skylighting 1.5.1 ·
Astralite Weathers 2.1.1 + 4K Clouds · Soul Core preset 2.1 · Soul Core Plugin and Assets 2.1 ·
Soul Core WT patch 1.01 · Soul Core ECSS patch 1.01 · Lux CS 2.6.0 · ISL Helper SKSE 1.0.5 ·
Dynamic Wind Framework 1.4 · Dynamic Wind - Skyrim 1 · ParticleWind NG 3.5 · Dynamic Wind NOTWL patch 1.0 ·
Bobbing Framework 2.0 + Configs 2.0 · Animated Ships Bobbing 1.0.0 · Smooth Terrain 0.4.0 ·
Terrain Shadows ×9 · (archive-only: NAT E11 preset v3 + Plugins, Cabbage CS Preset v6, NMLFF 1.5.1, FollowerParkour 2.2)

**Still needed (all nxm/manager-only):**
1. **Mists of Tamriel** (78703, base file) — hard requirement of Soul Core.
2. **ENB Extender and Helper v1.4.3** (99406, the non-Legacy file, same variant as installed 1.4.2).
3. **Wetness Effects** (112739, v3.1.0) — separate CS feature; Astralite ships an override json tuned for it.

## Archive analysis — decisions locked by contents

- **Soul Core preset** = clean root-form (`enbseries\` + `enbseries.ini`): SH2 configs (`*.fx.ini`),
  per-weather `Soul*.ini` + its own `_weatherlist.ini`, one custom fx (DoF), textures — and a bundled
  **KreatE preset** (`enbseries\KreatE\Soul Core\LightingTemplates\Lux_*.ini` + `Preset.ini`): the Lux
  DALC/lighting-template fixes are IN the preset package (route B no longer needs the separate misc file;
  files must be relocated to `KreatE\Presets\Soul Core\` if route B is activated).
- **Soul Core Plugin and Assets** installs from subfolder `Astralite ENB\` (set data root there; discard
  the packed `meta.ini`): `Astralite ENB.esp`, tuned `Astralite Weathers.ini` (must WIN the file conflict
  over Astralite's own — place the mod at higher priority than Astralite), assets, and a stray
  `SKSE\Plugins\DVLaSS.ini` (EVLaS config — inert with EVLaS off, harmless).
- **Astralite FOMOD picks:** Patches → **Seasonal Weather Framework Patch ONLY** (installs
  `Seasonal Weathers Framework - Astralite Weathers.esp`; auto-recommended since SWF.esp is active);
  **skip Mists of Tamriel patch** (Soul Core's plugin embeds it); Options → none by default
  (Darker/Brighter Nights conflict with Soul Core's tuning; Lower SoundFX Volume and Vanilla Moon Size
  are taste — decide at install). Payload ships CS override jsons for CloudShadows / GrassLighting /
  SkySync / Skylighting / WetnessEffects — they auto-apply per feature present.
- **Lux CS FOMOD picks:** Step 1 Main → **"Effect 11"** (installs only `Lux CS - Bulbs.esp` + LightPlacer
  configs — no `Lux - HDR.esp`, and the Lighting Templates step disappears entirely under E11);
  Step 2 Options → **"Lux Orbis Tweaks"** (`Lux Orbis CS.esp`, ISL patch for Lux Orbis — load after Orbis
  and its patches; works with E11). LightPlacer jsons stay inert without Light Placer (127557) — fine;
  Light Placer is an optional later add. ISL feature is in CS core; **ISL Helper SKSE** ✓staged is the
  required companion.
- **Soul Core patch esp names:** `Wyrmstooth-Astralite-Weather-Patch.esp`, `Astralite ENB - ECSS.esp`.
- **Dynamic Wind lane** (user-requested addition):
  - Dynamic Wind Framework 1.4 = `DynamicWind.dll` + ini, no esp. SKSE Menu Framework already installed → in-game config works.
  - Dynamic Wind - Skyrim = **`DynamicWindSkyrim.esp` (ESL-flagged, 41 banner variants — ONE plugin insert)** + ~230 configs.
  - **NOTWL patch** (729 tree configs, generated from NOTWL 3.14 CNAM data — installed NOTWL is exactly 3.14.0.0):
    README rule — **place BELOW "Dynamic Wind - Skyrim" in the left pane so its 32 vanilla-tree overrides win**. No esp.
  - ParticleWind NG 3.5 = dll + ini, no esp. Runtime-injected; explicitly compatible with any weather mod and CS.
  - Known cosmetic gap: seasonal `_WIN/_AUT` tree variant records (Seasonal Landscapes' own esps) have no
    wind configs — winter/autumn swapped trees won't sway. Future authoring candidate (same CNAM method).
- **Bobbing lane** (user-added): Bobbing Framework 2.0 (dll) + Configs (JK's-aware jsons) + Animated Ships
  Bobbing (meshes over `Animated Ships` ✓installed + `Animated Ships Patches` ✓). No esps. Winter note:
  bobbing boats/icebergs vs frozen winter water — eyeball in winter, disable individual jsons if silly.
- **Smooth Terrain 0.4.0** (hakasapl): dll + ini, CS-compatible, runtime terrain subdivision; no LOD
  interaction. Optional — enable, benchmark, tune `iSubdivisions` if GPU-bound.
- **EXCLUDED from this profile:**
  - **Native Mesh Light Flicker Fix** — author states **"CS isn't compatible."** Candidate for the ENB
    fallback profile (DEEEZ NUTTZZZ) only. Do not enable on DEEZ CS NUTZ.
  - **Cabbage CS Preset v6** — requires **Jiaye's Discord AIO build of CS** (different binary than official
    1.8.3) + NAT.CS III, and its ImageSpaces overrides are keyed to `NAT-ENB.esp`. Wrong ecosystem for this
    build in every dimension. Keep archived only.
  - **NAT Effect 11 Preset v3 + Plugins (`NAT-CS.ENB.esp`)** — kept as the known-good **E11 debug fallback**
    (Net's proven stack): if Soul Core misbehaves under E11, temporarily disable the Astralite/Soul Core
    lane, install NAT E11 over the original NAT preset per its page, and retest — isolates "E11 broken"
    from "preset broken". Not part of the active build.
  - **FollowerParkour 2.2** — update for a currently-disabled mod; unrelated to this swap.

## Phase 0 — Snapshot (MO2 + game CLOSED before any profile/mods write)

1. Copy `profiles\DEEZ CS NUTZ` → `C:\1. AUTHORIA\profile-backup-pre-astralite-cs-20260809`.
2. Standing rules: no LOOT; `plugins.txt` + `loadorder.txt` in lockstep at exact slots; plugin
   *insertions* also update the profile plugin-groups file (4-file rule); uncheck don't delete.

## Phase 2 — ENB lane teardown on DEEZ CS NUTZ

**Disable mods** (Visuals - ENB separator): ENB Binary Files · ENB Anti-Aliasing · ENB Light Detection Fix ·
ELIF · ENB Terrain Blending Fix (core LODBlending replaces) · ENB Worldspace Weatherlists · DALC Fix Preset
(NAT-keyed KreatE preset) · KiLoader for Skyrim · KreatE (route B may re-enable) · Native EditorID Fix ·
Parallax Occlusion Mapping · Terrain Helper for ENB.
**Keep:** ENB Extender and Helper (→1.4.3) · Silent Horizons 2 - Shader Core.
**Disable elsewhere:** EVLaS · AMON ENB REBORN · Authoria - ENB PrintScreen Fix · NAT-ENB Bizarre Shadow Fix ·
Seasonal Weathers Framework - NAT-ENB III - 3.1.1C · The Gray Cowl of Nocturnal - NAT3 ·
Wyrmstooth - NAT.ENB Patch · Skyrim Extended Cut - NAT3 - Patch.
**Keep `NAT.ENB - ESP WEATHER PLUGIN v3.1.1C - Fixed` enabled — NAT-ENB.esp stays ACTIVE** (master-satisfier
for `Authoria - Reqtificated - Wyrmstooth.esp`).
**Plugins to uncheck** (lines preserved): NAT-ENB Bizarre Shadow Fix.esp · SWF NAT-ENB III patch ·
Lux - NAT ENB.esp · SEC NAT3 patch · Wyrmstooth NAT patch · Authoria - Patch - Reverb Interior Sounds - NAT-ENB.esp ·
Gray Cowl NAT3 · Helios_NAT III{,_Seasonal,_Radiant}.esp. `Amon NAT III Esp Fix.esp` + `Amon Night Eye ENB
Fix.esp` stay checked (dummies in `Authoria - Dummy Plugins` take over). Post-teardown: resolver check,
uncheck anything unresolved.

## Phase 3 — CS stack install (above the `Authoria - LOD Outputs` separator)

Order: **Community Shaders 1.8.3 → Effects 11 → Skylighting → Wetness Effects → Lux CS (+ ISL Helper SKSE)**.
Existing `Particle Patch` (enabled) satisfies E11's requirement — do NOT install "CS Particle Patch".
Plugin inserts: `Lux CS - Bulbs.esp` + `Lux Orbis CS.esp` (slot at end of Lux / Lux Orbis patch blocks).

## Phase 3b — Wind + motion + extras lane

Left-pane order (top→bottom): **Dynamic Wind Framework → Dynamic Wind - Skyrim → Dynamic Wind NOTWL patch**
(must be below DWS per its README) **→ ParticleWind NG → Smooth Terrain → Bobbing Framework → Bobbing
Framework Configs → Animated Ships Bobbing** (below Animated Ships + Patches so its meshes win).
Plugin insert: `DynamicWindSkyrim.esp` (ESL-flagged; slot near other environmental esl-flagged plugins).

## Phase 4 — Weather swap

Mod priority (Weather/Sky region; weather/ENB plugins AFTER all landscape+grass mods per Soul Core):
1. **Mists of Tamriel** (base) — once downloaded.
2. **Astralite Weathers 2.1.1** (FOMOD picks above) + **4K Cloud Textures** over it.
3. **Soul Core Astralite Plugin and Assets 2.1** (data root = `Astralite ENB\`; wins `Astralite Weathers.ini`).
4. **Soul Core WT patch** + **ECSS patch**.
5. **Soul Core ENB preset 2.1** as `[NoDelete]` ROOT mod (Root Builder), priority above SH2 Shader Core.
6. **Restore authored patches** from `D:\1. MOD STUFF\- ARR STUFF\irreplaceable-core-20260725\authored-mods\`:
   `Authoria - Patch - Gray Cowl - Astralite` + `Authoria - Patch - Reverb Interior Sounds - Astralite`.
   (SNCT-Astralite not in cold copy — delta bundle, or re-set audio sliders once.)
7. **Helios FOMOD re-run** → Astralite + Seasonal + Lux selections. Luma + XEMI stay. ⚠ GetRegion-CTD
   authored fix gone post-hotfix (delta bundle if needed); MMSF (183073) still absent — Helios suspect #2.

Plugin insert block: `Mists of Tamriel.esp → Astralite Weathers.esp → Seasonal Weathers Framework -
Astralite Weathers.esp → Astralite ENB.esp → Wyrmstooth-Astralite-Weather-Patch.esp → Astralite ENB - ECSS.esp`,
authored patches near their old NAT slots, Helios Astralite esps at old Helios slots. 4-file rule.
Then housecarl zero-missing-masters verify → **user runs the Reqtificator**.

## Phase 5 — Seasons / Unfrozen thoroughness

- Only weather-keyed configs instance-wide were the DALC Fix Preset (retired) + disabled presets'
  `_weatherlist.ini`. **Unfrozen (all variants) is season-keyed — untouched by the weather swap.**
  Prior "Unfrozen hiccups" = wrong-season distant snow = stale DynDOLOD → cured by Phase 7 regen.
- `po3_SeasonsOfSkyrim.ini` (winner: Authoria - MCM and INI Settings): seasonal mode, all LOD swaps true,
  Grass=true — correct as-is; DynDOLOD regen must run with it.
- SWF: base 1.01 stays; verify `Seasonal Weathers Framework - Astralite Weathers.esp` weather lists resolve
  into Astralite (houseCARL). FOMOD-confirmed load order: SWF.esp → Astralite Weathers.esp → SWF-Astralite.
- Post-install grep of `mods\**\*.ini` for `Astralite` + orphaned NAT references.
- In-game: one snow weather → Frostfall exposure/footprints/Snowy Surfaces classification check.

## Phase 6 — First launch + tuning (before LOD regen)

1. Root Builder **Clear → Build** (Autobuild=false — AMON root files out, Soul Core root files in).
2. Delete stale `Overwrite\SKSE\Plugins\CommunityShaders\SettingsUser.json`; launch; let CS compile.
   `error compilation X enb shaders` ⇒ Extender not 1.4.3 or SH2/preset files not in VFS.
3. CS menu: rebind key off **End** (Modex); enable Skylighting + Terrain Shadows + Wetness; confirm
   Sky Sync + Cloud Shadows active (in-core); Effects 11 lists Soul Core auto-enabled;
   `UseOriginalPostProcessing` OFF; HDR off; **Save**.
4. Smoke test weathers/interiors/night/particle lights/water; wind: watch banners + NOTWL forest react.
5. **Route B** (only if interiors drift from Soul Core intent): re-enable KreatE; relocate the preset's
   `enbseries\KreatE\Soul Core\` files into a mod shipping `KreatE\Presets\Soul Core\`; select in KreatE UI.

## Phase 7 — Generation pipeline

Profile state for all runs: finished visual stack; **enable the five `Authoria - Grass Cache - *` mods**
(reuse; regen only if near-grass mismatches); NGIO stays disabled; Grass Cache Helper NG enabled.

| Step | Tool | Notes | Output mod |
|------|------|-------|-----------|
| a | PGPatcher | patches meshes for CS/TruePBR path | Authoria - PG Output |
| b | TexGen | defaults + complex-grass billboards (CS grass lighting now covers LOD grass) | Authoria - TexGen Output |
| c | xLODGen | enable `xLODGen Resource - SSE Terrain Tamriel` for this run only | Authoria - xLodGen Output |
| d | DynDOLOD | High + shipped Authoria rules; Seasons auto (po3 ini); Grass LOD from caches; Occlusion | Authoria - Dyndolod Output |

DynDOLOD.esm/esp + Occlusion.esp reuse their preserved slots. The 9 Terrain Shadows heightmap patches are
data-only and safe to install any time (core TerrainShadows feature reads them; unmatched worldspaces ignore).
Ballpark: PG 0.5–1 h · TexGen 0.5–1 h · xLODGen 1–3 h · DynDOLOD 2–6 h.

## Phase 8 — Verification sweep

- houseCARL: zero unresolved / zero missing masters.
- Seasons×LOD matrix (`Season Type` 1→4, restart each): near/far tree+grass agreement, winter-only snow
  LOD, Unfrozen water intent, Solstheim/Bruma/Wyrmstooth spot checks; restore `Season Type = 5`.
- Weather×region + WT/SEC/Gray Cowl uniques; wind: banners swap states, trees sway scales with weather,
  particles drift downwind; winter: seasonal-variant trees won't sway (known gap), bobbing vs ice check.
- Systems: Frostfall, Wet&Cold, footprints, rain wetness, auroras.
- Performance vs ENB profile, same save/spot; then fresh save.

## Known-unrelated

`DBVO Fix - SDA.esp` / `DBVO Fix - DaCoda.esp` fail houseCARL's parser (malformed dialog groups) —
pre-existing, unrelated. FollowerParkour 2.2 update staged for a separate decision.

## Correction 2026-08-11: Snow Cover baseline paint (Dawnstar dead grass, round 2)
1. Symptom: summer Dawnstar groundcover/grass looked dead and wintery again. Foggy weather. Tree swaps were fine.
2. Root cause: Snow Cover has TWO paint lanes. Lane 1 = realtime weather accumulation (TimeSnowing, gated by our snow-flag strips - was already fixed). Lane 2 = BASELINE snow from a static worldspace mask (Shaders\SnowCover\Skyrim.dds) plus its own linear calendar model (MaxWinterMonth=0, MaxSummerMonth=6, snow line lerped WinterHeightOffset -20000 to SummerHeightOffset +20000). Lane 2 ignores po3 Seasons entirely. AffectGrassTint/AffectTreeTint=1 made it frost grass and foliage. Shader combines lanes with max(), so they are independent.
3. Compounding bug: all 6 worldspace jsons pointed MainTexture/AltTexture at PBR snow textures that do not exist yet (no PGPatcher run). CS log: "Snow Cover: Error loading ...snow01_rmaos.dds 0x80070003". Broken material = flat gray paint = "dead" look.
4. Fix applied to all 6 jsons in [NoDelete] Community Shaders AIO\Shaders\SnowCover\ (Tamriel, Markarth, Riften, Solitude, Whiterun, Windhelm):
   - SummerHeightOffset AND WinterHeightOffset -> 9999999.0 (snow line above the whole map in every month; baseline lane permanently dead; realtime lane untouched).
   - MainTexture/AltTexture -> Shaders/SnowCover/default/main (feature's own shipped complete PBR set: main.dds, main_n.dds, main_rmaos.dds).
5. Result: snow paint now appears ONLY during actual snowfall weathers (winter-gated by region patch) and melts after (TimeSnowing decays; rain = -1). Summer structurally clean.
6. Optional later: after PGPatcher/Phase 7 produces real PBR landscape textures, MainTexture can point at a true snow texture again. Not required.

## Wind round 3, 2026-08-11: verified delivery, fixed targeting
1. Logs prove the earlier edits DID load: ParticleWind.log says "Default strength: 3"; DynamicWind.log read NotWL_3E525B.json. The problem was magnitude and test-tree choice, not delivery.
2. Trunk test made global: ALL 729 configs in [NoDelete] Dynamic Wind - NOTWL Patch now have trunkAmplitude=2.0, trunkFlexibility=3.0 (test values, deliberately strong). Every NOTWL tree is now the test. Revert = set both to 0.0 across the folder.
3. Flames: new file [NoDelete] ParticleWind NG\SKSE\Plugins\ParticleWind\AuthoriaFlames.json targets fire particle systems by name (harvested from ParticleWind.log full hierarchies, which print on the LINE AFTER "hierarchy:"). Campfires=FXfireWithEmbers keys, torches=TorchFire/MXTorchFire01/MPSTorchFire01, forge=Fire, lighthouse=*Flames*, candles=CandleFlame01 at 0.5. Flames now 1.0 vs global 3.0. Smoke and embers stay at global 3 on purpose.
4. ParticleWind config grammar (from mod page 174812): keys = exact NiParticleSystem name, parent node name, full ">" path, or *wildcard* (star both ends, case-sensitive). Priority exact > path > wildcard > default. 0 = no wind injection at all.
