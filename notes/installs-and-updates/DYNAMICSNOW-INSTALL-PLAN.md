# DynamicShader-DynamicSnow — Careful Install Plan
**Date:** 2026-08-27 · **Target profile:** DEEZ CS NUTZ · **Status: INSTALLED 2026-08-27 (later same day) — TRIAL PENDING, keep/rollback gate open**

Installed on user instruction after the seasonal/Unfrozen audit in §2b came back clean. Three mod folders:
`DynamicShader Core` (DLL 601,088 B ✓), `DynamicShader-DynamicSnow` (DLL 938,496 B ✓),
`Authoria - Smooth Terrain - Snow Trial Profile` (our tuned ini with exactly iSubdivisions 2→3,
iSmoothedQuads 3→6 — verified equal to the author's "My Ini" file, which differs from ours in only those
two lines and was NOT installed). Wired above `[NoDelete] Smooth Terrain` in DEEZ CS NUTZ (+PICTA
disabled at same anchor; other 3 profiles disabled after header). Backups: `modlist.txt.bak-snow-20260827`
in all five profiles. Author's personal meta.ini files from the archives replaced with proper Nexus metas.
No plugins — plugins.txt/loadorder/plugingroups untouched. Smooth Terrain 0.4.0 archive hash-checked
against installed `[NoDelete] Smooth Terrain`: DLL byte-identical, nothing to update.

Mod: [DynamicShader-DynamicSnow](https://www.nexusmods.com/skyrimspecialedition/mods/189713) (id 189713, JET654, v1, 2026-08-26).
Source reviewed in full: github.com/jatelop8/SnowDeformationPlugin (single commit, build "v563").
Five-agent source review archived at the session scratchpad (`snowreview\*.md`); key facts below are from
reading the actual code, the Nexus file manifests, all 44 mod-page comments, and the upstream CS PR #2659.

---

## 1. What this mod actually is (evidence, not marketing)

- **Two DLLs, no plugin.** `DynamicShader.dll` ("Core", 601 KB, **closed source** — the README's source link
  is a 404) + `DynamicSnow.dll` (938 KB, the open-source part). No ESP/ESL, no MCM, no INI of its own.
  **Zero plugin slots, zero Wheeler rawID impact, zero co-save writes — uninstall is save-safe.** This is
  the one genuinely clean property and it's what makes a trial acceptable at all.
- The page says "Phase 1 data layer, no visible deformation" — **wrong; the shipped build visibly deforms
  terrain.** It CPU-edits the live landscape mesh vertices (trenches ~18 units deep, normals recomputed)
  and re-uploads them every dirty frame. The ported CS "data layer" (GPU deformation map) also runs every
  frame but its output is read by **nothing** — pure overhead.
- **The Core DLL owns a swapchain Present hook** and drives everything. That hook meets our
  FidelityFX/Streamline frame-generation proxy swapchain sight-unseen (unauditable, closed source).
  The single closest user datapoint (RTX 5090 + FG + ENB-heavy list): ~20 FPS loss, constant stutter,
  "FG didn't make it any better", verdict "unusable in its current state". Every performance report on
  day one agrees; the author's reply: "Yeah, it does take a FPS hit… I'm still pretty new to this."
- **Shipped debug build:** a forced GPU sync stall every 600 frames (~10 s) from a debug BMP export aimed
  at the author's own D:\ path; ~138 log call sites (per-stamp lines while walking); F9/F10 debug hotkeys
  polled globally (fire even in menus); heavy per-2-second perf logging. Log file: `My Games\...\SKSE\DynamicSnow.log`
  (the page names a different file — the code wins).
- **Known crash classes in the code** (author's own crash diary + review): game-data walks on the render
  thread every frame (against the author's own in-code warning); a use-after-free window against Smooth
  Terrain's mesh rebuilds with access-violation-swallowing as the "fix"; an unguarded reset race on every
  save load. No CTD reports in the 9-hour comment window before Nexus locked the comments — weak evidence.
- **Footprints do not persist**: wiped on every save load. Refill is a fixed rate (weather gating was
  dropped in the port — it does NOT stop refilling when snowfall stops, nor snow-gate it).
- Comments are **moderator-locked** (attribution dispute over the unreleased CS PR it was AI-ported from);
  zero updates since release; the only support channel left is the empty Bugs tab.

## 2. How it interacts with THIS build (pre-flight results, 2026-08-27)

| Check | Result |
|---|---|
| CS AIO 08-24 contains the upstream snow feature? | **No** — no SnowDeformation files in the AIO. No double-deformation risk today. |
| F9 = quickload collision? | **Defused** — our controlmap has Quickload on F2. F9/F10 remain global debug keys that fire even in menus (harmless actions: re-cache / mesh scan). |
| Snow detection vs our textures | Detection is **LTEX diffuse path substring matching** (lowercased full path; keywords snow01/snow02/snowpath/grasssnow/snowrocks/snowstone/snowslope; also sand and mud keyword classes). It reads the **runtime-loaded** land texture per quad (base + all 6 painted layers, best class wins), so it sees terrain **after** Seasons of Skyrim swaps by construction. Fully audited against our live seasonal web — see §2b: winter carves everywhere it should, Unfrozen greens never carve. **CS Snow Cover painted snow will NEVER carve** (albedo-only, no LTEX). |
| Smooth Terrain | Installed 0.4.0 ([NoDelete], wins) — the snow plugin **consumes** its subdivided meshes; no hook conflict (verified against both sources; the snow author abandoned his own terrain hook because Smooth Terrain owns the call site). But it wants `iSubdivisions=3 / iSmoothedQuads=6`; ours is tuned `2 / 3`. At 2/3 it runs degraded: coarse trenches, seam fixes disabled, plus a skip-warning log line every 800 ms forever. |
| Archery stack (APC/Accuracy/Ricochet) | The mod vtable-patches arrow/spell projectile impact (craters). Composes with our arrow hooks by load order only; never unhooked. **Test archery explicitly in trial.** |
| RAM/VRAM | ~206 MB RAM fields (up to ~0.5 GB worst case with mesh copies) + 32 MB VRAM for the dead GPU map. |
| Save safety | Clean. No serialization, no scripts, no plugin. Rollback = disable mod folders. |

## 2b. Seasonal & Unfrozen audit — VERIFIED IN DATA 2026-08-27 (pre-install)

How the live seasonal web actually works here: `po3_SeasonsOfSkyrim.ini` has **Ignore auto generated WIN
formswap = true**, and `Auhoria - Seasons Empty INIs` (modlist line ~190) blanks every upstream seasonal
swap ini (all Unfrozen_*, Missing worldspaces, WW originals, etc.). The ONLY live land-texture swaps are
the consolidated master configs in `Authoria - Seasons Patches` (x/y/z prefixed, z = Unfrozen layer wins
by load order). Every LandTextures swap TARGET in those configs was resolved through houseCARL to its
winning TextureSet diffuse path and classified against the DLL's keyword sets:

- **Winter (x/y WIN configs): carving matches the visuals.** All snow targets resolve to
  vanilla-style paths — Snow01Landscape/Snow02Landscape/GrassSnow01/SnowRocks01/DirtSnowPath01/
  SnowStone01.dds (Vanaheimr Landscapes.esp overrides these TXSTs but KEEPS vanilla-style names —
  the author's documented Vanaheimr failure mode does NOT apply to this instance). Witchy Wilderness
  WIN variants (incl. our LOD Fix esp overrides) point at the same snow TXSTs → carve. Unfrozen's
  LSnowRoad (winter roads in snowy holds) → Snow01.dds → carves. COTN glacier snow → glaciersnow01.dds
  → carves.
- **Winter exceptions (deliberate, visually consistent):** Northern Roads winter road surfaces
  (grounddirt01_winter etc. via our Seasons-NR esp + Vanaheimr NR patch) contain NO snow keyword →
  roads do NOT take footprints (plausible: packed surfaces). Volcanic tundra / Reach moss / rocks kept
  un-snowed in winter by our configs → no carve, and they don't look snowy either. Mountain-slab snow
  (not LTEX-swapped, names lack the keywords) won't carve — moot, the DLL slope-limits at 45° anyway.
- **Summer/Spring (z Unfrozen configs): zero false positives.** Every green target resolves green:
  LSnow01/02/03SUM → FieldGrass02/PineForest01/02.dds (via Witchy Wilderness Unfrozen.esp overrides),
  glacier → DirtPath01, WWLGrassSnow01SUM → FieldGrass01SUM.dds. No summer target's diffuse contains
  any snow keyword → Unfrozen terrain never carves snow.
- **Autumn:** z AUT wins → LGrassSnow01/LSnow02 resolve to LSnow01AUT → FieldGrass01.dds (green, no
  carve). Frozen-marsh autumn variants keep "marsh" in their paths → classify as MUD (0.65 factor) —
  mud prints in autumn Hjaalmarch, plausible flavor, not a defect. Beaches ("beach") classify as SAND
  year-round — shallow prints, plausible.
- **Weather chain:** untouched by design — the DLL's weather API is unused (refill is a fixed ~1-day
  constant, NOT snowfall-gated). Our REGN-global seasonal weather chain and Helios interiors are
  irrelevant to it. Footprints refilling during clear skies is a known cosmetic simplification.
- **The one seasonal RISK found (goes in the trial): season flips ride door transitions.** po3 Seasons
  applies a season change on a load screen; the DLL has NO cell-load hook and resets only on save load.
  An interior→exterior round trip rebuilds the exterior land meshes while the DLL's 7×7-cell cache still
  holds the OLD BSTriShape/rendererData pointers, and it only re-caches after the player moves >512
  units. Until then its per-frame validity check reads freed memory (SEH-guarded CPU-side; driver-side
  is not guardable) and can re-upload stale-season geometry. This is the author's own documented
  "wrote correct data to the wrong object" failure class, and every season transition sits exactly in
  that window. Test door loops + a forced season flip explicitly (§5).

## 3. Recommendation (stated once)

Every day-one datapoint, including hardware far stronger than needed, says this build is not playable-with
yet, and its riskiest component cannot be audited. The careful play is to run the plan below as a
**time-boxed trial with an explicit keep/rollback gate**, expecting rollback — or park this until the
author ships an optimization pass (or the official CS feature matures; PR #2659 is Part 1 of 4, in
changes-requested state, feature-gated invisible even in CS test builds). Standing rule either way:
**if a future CS AIO build ever adds Snow Deformation, uninstall this mod first.**

## 4. Install steps (when executed)

Preconditions: MO2 + game closed · Nexus MCP login refreshed (all 3 files are manager-download-only).

1. **Download** (Nexus 189713): `DynamicShaderCore v1` (fileid 795459) and `DynamicShader-DynamicSnow v1`
   (fileid 795460). **Do NOT install the third file** ("Smooth Terrain My Ini") — it's a bare replacement
   `SmoothTerrain.ini` that would fight our tuned one. Hash-check sizes vs manifests (DLLs 601,088 / 938,496 B).
2. **Create mod folders** (archives are loose `SKSE/Plugins/<dll>` + the author's stray personal `meta.ini` — strip his meta.ini):
   - `DynamicShader Core` → `SKSE\Plugins\DynamicShader.dll`
   - `DynamicShader-DynamicSnow` → `SKSE\Plugins\DynamicSnow.dll`
   - `Authoria - Smooth Terrain - Snow Trial Profile` → `SKSE\plugins\SmoothTerrain.ini` authored by us:
     our tuned file with only `iSubdivisions=2→3` and `iSmoothedQuads=3→6` changed (`fMaxRise`,
     `iGradientStep` kept). One-toggle revert to tuned terrain settings.
3. **modlist.txt wiring** (backup first, CRLF, MO2 closed): all three enabled in DEEZ CS NUTZ near the
   other SKSE-plugin mods; the Snow Trial Profile must sit ABOVE (win over) `[NoDelete] Smooth Terrain`.
   Disabled entries in the other profiles. No plugins.txt / plugingroups changes (no ESP).
4. **Pre-launch guard:** confirm `D:\Modding\SnowDeformationPlugin` does NOT exist (if it ever does, the
   mod dumps 12 MB debug BMPs there every ~10 s). Do not create it.
5. User launches their own test session (never me).

## 5. Trial protocol (one session, ~20 minutes, user-run)

Baseline first, in an always-snow area (Winterhold/Dawnstar road), current build, note FPS + frametime feel.
Then enable the three mods and repeat, same spot, same weather:
1. Footprints carve behind you on wilderness snow? Expected per §2b: yes on snow/grass-snow/snow-path
   ground; NO on Northern Roads road surfaces (by data, not a bug); NO on painted-only CS Snow Cover
   snow. Horse + NPCs too, or player-only (tester consensus: player-only)?
2. FPS delta + stutter: any ~10-second cadence hitch (the debug readback); hitching when crossing
   cell/quad boundaries; hitch on any >512-unit sprint (re-cache).
3. Archery check: fire arrows at snow + at enemies — craters appear, and APC/Accuracy/Ricochet behavior unchanged.
4. Save, then load that save mid-session (the known reset-race window) — repeat 3–4 times.
5. **Door-transition loop (new, from §2b):** in a snowy exterior, enter and exit a building 4–5 times,
   walking around near the door between trips (inside the stale-cache window). Watch for terrain
   spikes/garbage near the door, or a crash. Then walk >512 units and confirm carving resumes cleanly.
6. **Season-flip test (new, from §2b):** `set gamemonth to 5` (or sleep across a month boundary), pass a
   load door so the season applies, and immediately walk the same ground: the now-green terrain must NOT
   carve, no visual corruption during the first ~512 units. Then flip back to a winter month and confirm
   carving returns after the terrain re-cache.
7. After quitting: check `SKSE\DynamicSnow.log` size (log-spam scale) and that no BMP folder appeared
   (D: exists on this machine — `D:\Modding\SnowDeformationPlugin` must never be created).

**Keep/rollback gate:** keep only if the FPS cost and stutter are genuinely acceptable to you AND nothing
crashed. Anything else → rollback.

## 6. Rollback (complete, one minute)

Disable (or delete) the three mod folders in modlist.txt (restore the .bak). Delete `DynamicSnow.log` if
large. Nothing else to clean: no plugin, no co-save data, no settings files, saves untouched. The tuned
SmoothTerrain.ini was never modified — it resumes winning automatically.

## 7. ADDENDUM 2026-08-27 (later same day): the Alpha Test build in Downloads

`Community Shaders - Snow Deformation (Alpha Test 1)(2).rar` (70.5 MB) turned out to be in
`C:\Users\User\Downloads` — this is the "more official CS build" option, inspected (443 files, NOT installed):

- It is a **full Community Shaders build from the feature's own author** (josefplyr1 lineage), carrying the
  **complete snow deformation implementation** — not the data-only Part 1 from the public PR: 20 snow shader
  files including the 3D snow shells (`SnowShell`, `SnowStaticsShell`), snow shading/shadow/parallax/lights,
  berm + exclusion fields, depth sync, height capture, and a trench debug view. Plus its own `TerrainHelper.esp`
  (we already run Terrain Helper separately — dedup at migration) and the full Streamline/FidelityFX upscaling set.
- Feature roster vs our AIO: it HAS Effects 11 (the Soul Core stack could carry over), TruePBR, LOD Blending,
  Horizon Fix, Interior Sun, Unified Water; it LACKS the Bottled-Shaders-only features — **no Snow Cover,
  no Procedural Grass, no Post Processing / Sky Gradient / SSR / NRD**.
- **Installing it = replacing the whole renderer**, i.e. the full CS-build-migration protocol: backup,
  settings do NOT carry (launch once, then edit saved full blocks), new features default ON (magenta-frame
  class traps), local shader edits and the three Snow Cover fixes become moot/lost, Effects 11 re-verify,
  ShaderCache move, and a re-tune pass on the DEEZ CS NUTZ look. A real project — its own session, its own plan.

**Comparison, honestly:** the Nexus plugin is a cheap, reversible bolt-on experiment with known heavy
performance pain and an unauditable core. The Alpha build is the real feature done right, at the cost of a
renderer migration and the AIO-only features. If deformed snow matters enough to migrate for, the Alpha is
the quality path; the Nexus mod is only worth a curiosity trial on the current build.

## 8. Standing notes

- The baseline-list duplicate mod folder `Smooth Terrain` (older copy, fully shadowed by `[NoDelete] Smooth Terrain`)
  is a stale-duplicate landmine if the NoDelete copy is ever disabled — flagged, not touched.
- Never update Smooth Terrain (0.5.0 adds collision hooks) mid-trial; one variable at a time.
- If the author ships an update: comments are locked and he ships no changelogs — re-audit the source diff
  before updating (the GitHub repo is the only visibility).
- Full source-review evidence: session scratchpad `snowreview\{arch,hooks,risk,prcmp,distro}.md`.
