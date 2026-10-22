# Magpie Manor — install, Seasons winter patch, grass-cache regen

Plan written 2026-08-17 (executed 2026-08-19). Status: ALL FOUR PHASES DONE 2026-08-19. Remaining: you run Synthesis (worldspace group) and the in-game checks. See section 9 (execution log).
Profile: `DEEZ CS NUTZ`. Instance: `C:\1. AUTHORIA`.
Analysis tools + data used for this plan: `C:\1. AUTHORIA\_tools\magpie-manor\`.

Rules honoured throughout: MO2 closed before every write; I never launch MO2 or the game;
you run Synthesis / Reqtificator / DynDOLOD / the grass passes; nothing goes below the outputs block;
every new plugin I author is ESL-flagged; plugins.txt + loadorder.txt + plugingroups.txt edited together;
you pick the final positions (I propose them below).

---

## 0. One-screen summary

| Lane | What happens | Blocking facts |
|---|---|---|
| A. Install | Magpie Manor BSA main 1.2.1 + 4K textures + Lux patch + LOTD storage integration (needs the compacted Storage Extension ESP). 1 full plugin + 6 light plugins. | 251 full plugins active → 3 free slots. Magpie takes 1. |
| B. Landscape patch | Small ESL patch that merges Magpie's terrain with Northern Roads' road terrain in 3 cells. | Without it: either the manor sinks/floats or the road does. Synthesis re-run needed after (you). |
| C. Seasons | Snow in winter mostly works by itself (ground swaps + runtime snow shader + the mod's own tree swaps). Add a no-snow blacklist for glass/cloth, and optional winter greenery hides. | No ESP needed. INI files only. |
| D. Grass cache | Back up the 5 caches (11.6 GB), then regenerate only 70 cells (manor area + Morskom area) in 5 passes. | The ini has NO cell-range option. Partial regen = "Updating-Cache = true" + delete just those files. Default `false` WIPES the whole cache — must flip first. |

Order: A → B → (you: Synthesis) → C → D → tests. Reqtificator, DynDOLOD/TexGen/Occlusion, PG are follow-ups (see §6).

---

## 1. What I found

### 1.1 The seven archives

| Archive | Content | Verdict |
|---|---|---|
| Magpie Manor - BSA 1.2.1 (2.7 GB) | `MagpieManor.esp` (FULL, 7660 records), 4 BSAs (192 MB meshes/scripts + 3 texture BSAs 1.26/1.21/0.54 GB), 2 header-only ESL dummy plugins `MagpieManor0.esp` / `MagpieManor1.esp` (they exist only to load the 2nd/3rd texture BSA), `seasons\MagpieManor_WIN.ini` + `_AUT.ini`, readme, the author's own `meta.ini`. Packaged as an MO2 mod folder (`data\Magpie Manor\...`). | INSTALL THIS ONE. |
| Magpie Manor - Loose Files 1.2.1 (2.35 GB) | Same content, loose (5,014 files). Meshes are namespaced (`meshes\aproco\...`), but 367 textures sit on shared/vanilla paths: ~250 vanilla book covers, SMIM ingredient bowl + salt pile, Dragonsreach window glass, DLC2 coloured lanterns, some rugs. Loose, those would fight your book/SMIM/Whiterun retextures. | DO NOT install. Keep the download. |
| Magpie Manor - 4K Textures 1.0 (660 MB) | 90 loose textures. 86 override files that still exist in 1.2.1, 4 are dead (renamed since). Loose files always beat BSA content, so it works on top of the BSA install. Adds ~1.2 GB VRAM-side texture data. | Optional. Recommend install (author still lists it for 1.2.1). Skip if VRAM is tight. |
| Magpie Manor - Lux Patch 1.01 (Temryuu, 2023-12) | ESL. 195 placed refs, 5 interior CELL overrides (lighting), 1 interior navmesh override (main hall). Masters: Lux - Resources, Lux - Master plugin, Lux, MagpieManor. | Install. Navmesh override has the same vertex/triangle count as 1.2.1's → almost certainly an ITM; verify after install with a diff. |
| Magpie_LOTD (mod 165886, 2025-11) | ESL `Magpie_LOTD.esp` + `Scripts\ManorLSE.pex`. Links Magpie's storage to the LOTD sorting system. Masters: LOTD.esm, MagpieManor.esp, LegacyStorageExtended.esp. Touches: main interior cell, exterior cell (21,-1), the persistent worldspace cell, and one stray ref in cell (21,1). | Install. |
| LegacyStorage Patch (mod 165886) | `LegacyStorageExtended.esp` — ESL-flagged, FormIDs COMPACTED, masters trimmed (no `_ResourcePack.esl`, no Update/HearthFires). | USE THIS ESP. Magpie_LOTD.esp was built against these compacted IDs. |
| LotD Storage Extension 3.31 (mod 25236) | Original `LegacyStorageExtended.esp` (FULL esp, different FormIDs, needs `_ResourcePack.esl`) + `meshes\lse\*.nif` (5) + `Scripts\LSE_*.pex` (8) + readme. | Take ONLY the assets (meshes/scripts/readme). Do NOT use its ESP (wrong IDs for Magpie_LOTD, and it would eat a full slot). |

Neither Storage Extension ESP is in your load order today, so nothing else depends on the original IDs.

### 1.2 Where the manor is
- Tamriel worldspace, east of Whiterun beside Darkshade, on the White River road.
- Cells touched by MagpieManor.esp: **(21,-1)** main yard (1,165 refs), **(20,-1)** (57 refs), plus landscape-only records in (21,0), (20,0), (21,-2), and a bare cell record for (22,-1). The LOTD patch adds one ref in (21,1).
- Ground textures in the manor's cells are all vanilla ones. Every one of them is already in your winter land-texture swap list → snow-covered ground in winter comes for free.
- 6 exterior cells' CELL records are currently won by `Occlusion.esp` (DynDOLOD output). See §1.4.

### 1.3 Plugin budget (counted from the profile, 2026-08-17)
- 4,018 active plugins: **251 full** + 3,767 light. Full cap is 254 → **3 free full slots**.
- MagpieManor.esp is FULL (author: too many records to flag). Everything else new is light. After install: 252 full, 2 spare.
- New light plugins: MagpieManor0.esp, MagpieManor1.esp, LegacyStorageExtended.esp (patch version), Magpie_LOTD.esp, MagpieManor - Lux Patch.esp, my landscape patch. Light count stays far below 4,096.

### 1.4 Conflicts (checked record by record)

**Northern Roads — REAL, needs a patch (the mod page says so too).**
- Northern Roads edits terrain heights in 3 of Magpie's 5 landscape cells: (21,-1), (20,-1), (21,-2).
- Vertex-level diff (all 1,089 vertices per cell, `_tools\magpie-manor\landmerge_preview.txt`):
  - (21,-1): NR changed 15 vertices in the SW corner (the road), Magpie changed 74 in the middle (up to 152 units lower — the manor's flattened yard). **Zero overlapping vertices.**
  - (20,-1): NR changed 9 (SE corner), Magpie changed 21 (east edge, up to 216 units). **Zero overlap.**
  - (21,-2): NR changed 82 (the road along the west edge). Magpie's record here has vanilla heights (0 changed) — it must NOT win, or the road terrain reverts.
- Consequence: no single load order is right. If NR wins → manor sinks/floats. If Magpie wins → road terrain reverts in (21,-2) and the two corners. Fix = a merged landscape patch (§3).
- Texture paint: NR also repaints the road corners (22 vs 23 layers in (21,-1); 24 vs 20 in (20,-1)). The merged patch keeps Magpie's paint → possible small paint seam at the road corner. Revisit only if visible.
- Placed refs: NR buries the vanilla road pieces along the south edge of (21,-1) (moves them to Z −30000) and shifts a few vanilla plants. Magpie overrides 35 vanilla refs; only 2 (a nettle, a thistle) are also touched by NR — harmless (Magpie disables them). Magpie's yard edits stop ~600 units north of the road. Clipping between NR road clutter and the manor fence must be checked in game.

**Synthesis Worldspace output — REAL, needs a re-run (you).**
- `Authoria - Output - Synthesis Worldspace.esp` (RemoveLandscapeVertexColor + Z-Floor + BlacksmithForgeWater + NoStartingMapMarkers + WingsInTheWild) overrides EVERY landscape record with the winner-at-run-time. It currently carries the pre-Magpie terrain. Until you re-run Synthesis after install, the manor's terrain sculpting is lost → the exact "parts of the home buried under terrain" symptom the author describes.

**Occlusion.esp (DynDOLOD output) — minor, cosmetic until DynDOLOD is re-run.**
- Occlusion.esp overrides the exterior CELL records. Magpie assigns its exterior cells to its own Location; Occlusion.esp's copies have no Location. Until DynDOLOD/Occlusion are regenerated the yard is not "inside" the manor's location (interior cells are unaffected — they are new cells). No LOD for the manor either way (custom meshes have no LOD models). Not blocking.

**Nature of the Wild Lands / Realistic Treeline / Lux Via / Fishing CC — check in game.**
- No record conflicts found, but NotWL plants trees everywhere; the mod page warns Traverse the Ulvenwald trees clip the house. Expect the same possibility here. Fix = a tiny disable-refs patch after a walk-around.

**Lux — fine.** Lux patch loads after Lux.esp and after the LOTD patch, so it wins the interior lighting. Many toggleable lights + Lux lights: with CS Light Limit Fix that is fine.

**LOTD Storage Extension — watch the 6 vanilla dungeon cell overrides + 1 navmesh.** Its ESP overrides 5 vanilla dungeon cells and 1 navmesh (Kilkreath, Falmer Valley, Glacial Crevice, Falmer Temple, Book02 dungeon). Placed early (before Lux and the dungeon overhauls) nothing legit is clobbered. Verify with conflict trees after install.

**Nothing else in the list has a Magpie patch.** Northern Roads Patch Collection 1.40.1, NotWL patch collection, Lux Via hub, LOTD official patches — none mention Magpie (checked the archives).

### 1.5 Seasons of Skyrim — how winter will reach the manor
- Winning config: `mods\Authoria - MCM and INI Settings\SKSE\Plugins\po3_SeasonsOfSkyrim.ini` (uncontested). Season Type = 5 (seasonal). Tamriel is registered for all four seasons → no `[Worldspaces]` section needed.
- `Ignore auto generated WIN formswap = true` → nothing is swapped automatically; only what INIs say.
- Winter snow shader: applied at runtime to every static / movable static / container that was not swapped and has no snow material. Multipass unless the mesh has alpha (then single-pass). Trees, activators, furniture never get it. → The manor's walls, roofs, fences, planters, statues will be snow-dusted with zero records. Things that look wrong snowed (glass, cloth) go on a blacklist.
- Blacklist file suffix in this instance is `_NOSNOW` (DynDOLOD's own output uses it; 8 mods do). `[Blacklist]` takes base or reference FormIDs.
- Configs are read alphabetically, later wins. House naming: `a…` for blacklists, `zz…` for the last word. Key lines by `0xFormID~Plugin.esp` with the EditorID in a comment above (your rule after the Ash Nomad breakage). Check `Auhoria - Seasons Empty INIs` for name collisions (none for `MagpieManor_*`).
- The mod's own INIs: WIN swaps oak/willow/twisted tree → winter models; AUT swaps oak/willow → autumn models. All target meshes exist. There is NO spring INI, and the SPR tree records point at meshes that are not in the archive → do not add spring swaps.
- Test switch: Select Your Season MCM (installed) → force winter at the manor.

### 1.6 Grass cache — how it really works here
- NGIO-NG 1.6.8 (Nexus now has 1.6.10 — do NOT update before the regen; the caches must stay consistent with the version that made them). Grass Cache Helper NG 1.0.1 owns the seasonal suffix.
- Config: `mods\Authoria - MCM and INI Settings\SKSE\Plugins\GrassControl.ini` (uncontested; nothing in overwrite or Stock Game).
- **There is no cell-range / X-Y bounds setting in NGIO-NG** (all 34 keys checked in the DLL). Area limiting exists only per worldspace (`Only-pregenerate-world-spaces`). Partial regeneration works because NGIO skips every cell that already has a cache file and only generates the missing ones — IF `Updating-Cache = true`. It is currently `false`, and `false` means "delete the whole grass folder first" — through the VFS that would delete files inside all five cache mods.
- Cache mods: `Authoria - Grass Cache - Default / Autumn / Summer / Spring / Winter` (modlist lines 29–33, inside the protected outputs block). 94,777 files, 11.56 GB total. All generated 2026-07-18; no partial regen has ever happened.
- File name pattern: `Tamrielx0021y-001.cgid` (Default), `Tamrielx0021y-001.WIN.cgid` / `.SPR.` / `.SUM.` / `.AUT.` — coordinates zero-padded to 4 chars including the minus sign, no separators. Season lives in the file name → each season is a separate generation run.
- The generation trigger is an empty `PrecacheGrass.txt` next to `SkyrimSE.exe` in `Stock Game` (Root Builder already excludes that name). MO2 has the "Precache Grass" tool plugin installed (creates the file, launches SKSE, restarts on crash). Grass Cache Helper NG flips the ini grass flags itself.
- Season per pass is pinned with `Season Type` in `po3_SeasonsOfSkyrim.ini` (1 winter, 2 spring, 3 summer, 4 autumn, 0 = no seasons → Default files).
- Runtime: `Only-load-from-cache = true` → any cell whose file is missing renders bare ground. So every deleted file must be regenerated and verified.
- Watch item from memory: two CS grass-shader compile crashes on 2026-08-12 (BSGrassShader). If a pass crashes repeatedly at the same cell, that is the first suspect.

Morskom Estate cells (from `Morskom.esp`): (7,25) (7,26) (8,25) (8,26) (8,27) (9,25) (9,26) (9,27) (9,28) (10,26) (10,27) + fishing spot (9,31) (+ two far-away marker-only cells (34,7) and (−18,22), ignored).

---

## 2. Phase A — Install (MO2 closed for every write)

### A1. Backups first
- Copy `modlist.txt`, `plugins.txt`, `loadorder.txt`, `plugingroups.txt` → `*.bak-magpie-20260817` (same convention as the existing `.bak-*` files).
- `ModOrganizer.ini` untouched.

### A2. Mod folders to create under `C:\1. AUTHORIA\mods\`

| Mod folder (proposed name) | Contents | meta.ini |
|---|---|---|
| `Magpie Manor` | everything from the BSA archive's `data\Magpie Manor\` EXCEPT the author's `meta.ini` (write our own). Keep `seasons\` folder as shipped. | modid 79391, version 1.2.1, installationFile = the BSA 7z, fileid from the .meta if present |
| `Magpie Manor - 4K Textures` | `textures\...` from the 4K 7z (`Data\` stripped) | modid 79391, version 1.0 |
| `Magpie Manor - Lux Patch` | `MagpieManor - Lux Patch.esp` | modid 79391, version 1.01 |
| `Legacy Storage Extension Util - Magpie ESL` | 3.31 assets: `meshes\lse\`, `Scripts\`, `Readme.txt` — and the ESP from **LegacyStorage Patch** (compacted, ESL). The original 3.31 ESP is NOT installed (note this in meta notes). | modid 25236 (assets) — note the ESP source (165886) in notes |
| `Magpie Manor - LOTD Storage Integration` | `Magpie_LOTD.esp`, `Scripts\ManorLSE.pex`, `Scripts\Source\...` | modid 165886, version 1 |
| `Authoria - Magpie Manor - Patches` | my ESL landscape patch (§3), Seasons INIs (§4), later disable-refs patch if needed | modid 0, version 1.0, comments "Authoria hand-authored" |

Install check (your FOMOD-diff rule): compare archive file lists vs installed folders (counts + sizes), including the 4 BSAs (1,259,678,146 / 191,835,532 / 1,206,950,222 / 539,808,603 bytes).

### A3. Install order (modlist.txt) — proposed
Into the "City Stuff - Player Homes" group, next to Morskom. In file order (top = higher priority):

```
+Authoria - Magpie Manor - Patches
+Magpie Manor - LOTD Storage Integration
+Legacy Storage Extension Util - Magpie ESL
+Magpie Manor - Lux Patch
+Magpie Manor - 4K Textures
+Magpie Manor
```
inserted between `+Talos' Tease` (line 2532) and `+Morskom Quest Startup Patch` (line 2533).
Asset conflicts are nil (namespaced meshes; BSA textures lose to any loose retexture), so priority inside the group is cosmetic. `archives.txt` is regenerated by MO2 itself — no manual edit; just confirm the 4 Magpie BSAs appear in the Archives tab afterwards.

### A4. Plugins — names, flags, proposed slots (plugins.txt / loadorder.txt / plugingroups.txt in lockstep)

| Plugin | Flag | Proposed position | Group (plugingroups.txt) |
|---|---|---|---|
| `MagpieManor.esp` | FULL | Houses block, right after `cs_Morskom_patch.esp` (plugins.txt line 842) | Quests and Newlands - Houses |
| `MagpieManor0.esp`, `MagpieManor1.esp` | ESL (header-only BSA loaders) | directly after MagpieManor.esp | Quests and Newlands - Houses |
| `LegacyStorageExtended.esp` (compacted) | ESL | after MagpieManor1.esp | Quests and Newlands - Houses (or Gameplay - DBM Patches — your call) |
| `Magpie_LOTD.esp` | ESL | after LegacyStorageExtended.esp | same as above |
| `MagpieManor - Lux Patch.esp` | ESL | Lux patches block, right after `Lux - Morskom Estate patch.esp` (line 3095) | Lighting - Lux Patches |
| `Authoria - Landscape - Magpie Manor - Northern Roads.esp` | ESL (mine) | Landscape block, right after `Authoria - Landscape - Morskom - City Trees.esp` (line 3875) | Authoria - Landscape Patches |

Why these slots: MagpieManor before its patches; Storage Extension well before Lux.esp (2937) so Lux keeps every dungeon cell's lighting; the landscape patch after Northern Roads (3164) and its patches, before the outputs. Everything stays above the outputs block. plugingroups.txt gets one line per plugin (your "4th file" rule).

### A5. Post-install verification (houseCARL, read-only)
1. All 6 plugins resolve their masters; ESL flags read back as expected.
2. Conflict trees for the 6 exterior CELLs, the 5 LAND records, the persistent-cell refs the LOTD patch relinks, and the stray (21,1) ref (identify what it is; disable via my patch if it is junk in the wild).
3. Storage Extension: conflict trees for its 6 vanilla dungeon CELL/NAVM overrides — confirm nothing legit lost.
4. Lux patch navmesh vs Magpie 1.2.1 navmesh: field diff; if identical, note "ITM, harmless".
5. `housecarl_check_errors` on the six plugins.
6. Reqtificator: MagpieManor.esp adds 2 creature NPCs (goat, rooster) + 1 armor record. Not blocking; recommend a re-run before real play. If the Reqtificator complains, a small `Authoria - Reqtificated - Magpie Manor.esp` like the Morskom one.

---

## 3. Phase B — Landscape patch vs Northern Roads

Plugin: `Authoria - Landscape - Magpie Manor - Northern Roads.esp` (ESL, in `Authoria - Magpie Manor - Patches`).

| Cell | Record content |
|---|---|
| (21,-2) | Northern Roads' landscape record forwarded verbatim (Magpie's copy is vanilla heights). |
| (21,-1) | Magpie's landscape record forwarded, then NR's 15 corner vertices grafted in = 24 delta bytes changed (exact list in `landmerge_preview.txt`, no out-of-range deltas). |
| (20,-1) | Magpie's record forwarded, NR's 9 corner vertices grafted = 11 delta bytes changed. |

Method: houseCARL `forward_record` (from MagpieManor.esp / Northern Roads.esp) into the new patch, then `set_field` on the height-map entries; verify by re-running `landscan.py` against the written patch (must show: vs Magpie = only NR's vertices differ; vs NR = only Magpie's vertices differ). If the dictionary-entry write turns out unsupported, fallback = write the record with the Python ESP writer and verify the same way.
Texture paint stays Magpie's. If the road corner shows a paint seam in game, phase 2 = alpha-layer merge (same tooling, more work).
After this patch is in: **you re-run Synthesis (Worldspace group at least)** so the output forwards the merged terrain. Until then terrain judgement is meaningless.

---

## 4. Phase C — Seasons winter patch (INI only, no plugin)

Files in `Authoria - Magpie Manor - Patches\Seasons\`:

1. `zzAuthoriaMagpieManor_WIN.ini`
   - `[Trees]` — optional polish: climbing roses (2 forms) and the flowering wall bush → `CHA_invisiplant` (Seasonal Alchemy.esp 0xD62, an invisible tree already used by your master config). Trees do not get the snow shader, so without this they bloom in winter.
   - `[Statics]` — optional polish: winter hides for exterior greenery → `InvisiStatic` (Seasonal Alchemy Add-on.esp 0x844). Candidates with exterior refs: rose bushes (9+2), sunflowers (8+5+1), lupins (2+1+1), pink flower bushes, purple creeper, yellow flowering vine, marigold, chamomile, nettle, celandine, lady's mantle, wood anemone, cranesbill, chickweed, goldenrod. Planters with flowers → the mod's own soil-only / empty planter forms where the model matches. Full list with ref counts: `_tools\magpie-manor\magpie_exterior_bases.tsv`. Decide after the first winter visit — the snow shader may already make them acceptable.
2. `aAuthoriaMagpieManor_NOSNOW.ini` `[Blacklist]` — greenhouse roof/wall glass panels, glass dome, exterior arched windows and bay window, red curtains, roof awning, the clothes-line laundry pieces, water lilies, plus every reference found under a roof during the walk-through (things under cover still get top-down snow).
3. No spring file (see 1.5). Autumn/summer: nothing needed (the mod's own AUT swap handles trees; summer is the base state).
4. Keep the mod's own `seasons\MagpieManor_WIN.ini` / `_AUT.ini` untouched (they load from the mod folder). Note the folder is lower-case `seasons` — fine on Windows.

Verification: Select Your Season → winter → walk the yard: white ground, snow on roofs/fences, bare trees, no snow on glass/cloth, no green summer bushes if the polish lines are in. Then autumn (orange oak/willow), spring, summer.

---

## 5. Phase D — Grass cache: backup + partial regeneration

### D1. Backup (before touching any ini)
- `robocopy` each of the 5 cache mods to `C:\1. AUTHORIA\_backups\2026-08-17 - grass cache pre-magpie-morskom regen\<mod name>\` (11.6 GB; C: has 273 GB free). Verify file counts (20,918 / 17,128 / 20,893 / 20,915 / 14,943) and byte totals match. Use .NET/robocopy, not PowerShell globbing.
- Also zip only the 350 target files (`_backups\...\targets-only.7z`) for a 10-second rollback of just those cells.

### D2. Target cells (70) → 350 files
- Manor: x 19..23, y −3..1 (25 cells) — 1-cell margin around everything Magpie touches.
- Morskom: x 6..11, y 24..29 (36 cells) + x 8..10, y 30..32 (9 cells, fishing spot) — 1-cell margin.
- Names: `Tamrielx00NNy0MMM[.WIN|.SPR|.SUM|.AUT].cgid` — script builds the exact 350 names; every one is confirmed present today, so "delete → regenerate → verify" is closed-loop.

### D3. INI edits (with `.bak-grassregen-20260817` copies)
- `GrassControl.ini`: `Updating-Cache = true` (mandatory), `Only-pregenerate-world-spaces = Tamriel` (keep the original 69-worldspace list in a comment for restore). Everything else unchanged. NGIO stays 1.6.8.
- `po3_SeasonsOfSkyrim.ini`: `Season Type` set per pass (below), restored to 5 at the end.

### D4. Five passes — order matters, Default LAST
Why: NGIO resumes by "file missing". If it checks the base name and the Default files came back first, the seasonal passes would see nothing to do. Deleting all five variants up front and running Default last is safe either way.

| Pass | Season Type | I delete (70 files) | Files expected in `overwrite\Grass\` | Then I move them into |
|---|---|---|---|---|
| 1 | 1 (winter) | `*.WIN.cgid` for the 70 cells | 70 `.WIN.cgid` | Authoria - Grass Cache - Winter |
| 2 | 2 (spring) | `*.SPR.cgid` | 70 `.SPR.cgid` | … - Spring |
| 3 | 3 (summer) | `*.SUM.cgid` | 70 `.SUM.cgid` | … - Summer |
| 4 | 4 (autumn) | `*.AUT.cgid` | 70 `.AUT.cgid` | … - Autumn |
| 5 | 0 (off) | plain `.cgid` | 70 `.cgid` | … - Default |

(All 350 deletions can happen before pass 1; per-pass deletion is just tidier.)
Per pass: I set the ini + delete; you start the game via MO2 → tools → "Precache Grass" (or drop `PrecacheGrass.txt` in `Stock Game` and launch SKSE); NGIO generates only the missing cells and exits when done (message box). I then move the new files, check 70 present, sizes sane (> a few KB), timestamps fresh, no `.fail` markers, log clean. If a pass crashes repeatedly on one cell → the CS grass shader watch item.

### D5. Restore
- `Season Type = 5`. `Only-pregenerate-world-spaces` back to the full list.
- `Updating-Cache`: recommend leaving `true` permanently — it only matters in generation mode and it stops an accidental "Precache Grass" click from deleting 11 GB. Your call (deviates from the published list's value).
- Confirm `overwrite\` has no leftover `Grass\` files. Confirm all 5 cache mods have exactly the original file counts again.

### D6. In-game checks
- Manor: no grass through yard paving, greenhouse floors, garden beds, in each season (Select Your Season).
- Morskom: the area you saw the bug in, each season.
- Everything else unchanged (spot check a random field).

### D7. Rollback
- Copy the 350 files back from `targets-only.7z` (or the full backup), restore the two inis from `.bak-grassregen-20260817`.

---

## 6. Follow-ups that are NOT part of this job (but will be needed)
- Synthesis Worldspace group re-run — REQUIRED for the terrain (you). Also re-run Gameplay group if you want the LOTD/Requiem-side outputs to see the new records.
- Reqtificator — recommended (2 animal NPCs, 1 armor). Watch its log for the Magpie animals.
- DynDOLOD + TexGen + Occlusion — later: cell Location fix, tree billboards for the oak/willow seasonal forms, occlusion data. Manor itself gets no LOD (no LOD meshes).
- ParallaxGen — later, so Magpie meshes get CS materials like the rest of the world.
- NotWL/Lux Via clutter clipping the yard — small disable-refs patch after the walk-around, into `Authoria - Magpie Manor - Patches`.
- Optional Nexus extras not downloaded: Skald's Mail patch (you don't run Skald's Mail), Pilgrim add-on (no Pilgrim). Fabled Forests patch is irrelevant (not installed).

## 7. Decisions I need from you (defaults in bold)
1. Install the 4K textures optional? (**yes**)
2. Plugin/mod positions as proposed in A3/A4? (**yes**, or tell me the slots)
3. Winter greenery hides (§4 item 1) now, or after the first winter visit? (**after**)
4. Leave `Updating-Cache = true` after the regen? (**yes**)
5. Storage Extension: keep the original 3.31 ESP anywhere as reference? (**no**, notes only)

## 8. Appendix — data

### 8.1 Landscape merge detail
See `C:\1. AUTHORIA\_tools\magpie-manor\landmerge_preview.txt` (vertex lists and the exact delta bytes per cell). Vertex maps (`.`=same, `+`/`-` raised/lowered vs vanilla) are reproducible with `landscan.py`.

### 8.2 Magpie exterior placements
1,278 exterior refs (1,165 in (21,-1), 57 in (20,-1), 56 persistent). 428 distinct base objects; 235 are Magpie statics, 147 vanilla (rocks, plants, markers, HearthFire soil planters ×46). Full table: `magpie_exterior_bases.tsv`.

### 8.3 Files that would collide if the LOOSE variant were ever installed
`magpie_loose_vanilla_path_textures.txt` (367 paths; book covers, SMIM, Dragonsreach windows, DLC2 lanterns, rugs).

### 8.4 Header facts
MagpieManor.esp: 7,660 records, 5 landscape records, 19 navmeshes, 13 cells (6 interior + 7 exterior overrides), 2 NPCs, 77 placed actors (animals), no ESL flag. Lux patch / Magpie_LOTD / LegacyStorage Patch / dummy plugins: ESL flag set. Original Storage Extension 3.31: no ESL flag, needs `_ResourcePack.esl`.

### 8.5 Grass cache inventory (2026-07-18 generation)
Default 20,918 files 3.12 GB · Autumn 17,128 / 1.26 GB · Summer 20,893 / 3.09 GB · Spring 20,915 / 3.17 GB · Winter 14,943 / 0.91 GB. Tamriel coverage x −57..61, y −43..44. All 25 manor cells present in all five caches.


---

## 9. Execution log (2026-08-19)

### Done
- A. Installed (MO2 closed): `Magpie Manor` (BSA main, 4 BSAs + 2 loader ESLs, sizes verified), `Magpie Manor - 4K Textures` (90 files), `Magpie Manor - Lux Patch`, `Legacy Storage Extension Util - Magpie ESL` (3.31 assets + the compacted ESL-flagged ESP), `Magpie Manor - LOTD Storage Integration`, `Authoria - Magpie Manor - Patches`. modlist/plugins/loadorder/plugingroups edited in lockstep (backups `*.bak-magpie-20260819`). Positions exactly as proposed in §2. Archives were found in `C:\Users\User\Downloads\to add\`.
- A5 checks: no missing masters; 77 "dangling" links in MagpieManor.esp all point at the same non-existent vanilla form 000028 (alternate-texture slots on food/planter statics — harmless, the mod has always shipped like this). Storage Extension's 6 vanilla dungeon cell overrides all lose to later Lux/other winners (no clobber). Lux patch navmesh = byte-identical to Magpie's apart from master-index bytes (true ITM). LOTD patch stray ref in cell (21,1) = an LSE_Weapons activator buried at Z −14000 (unreachable, harmless). Side finding: `Authoria - Reqtificated - Snow Elven Arsenal.esp` wins the Falmer Temple cell and reverts Lux's lighting there — pre-existing, not Magpie related.
- B. `Authoria - Landscape - Magpie Manor - Northern Roads.esp` (ESL) written via houseCARL forward + byte-level VHGT graft (`_tools\magpie-manor\landpatch_graft.py`). Verified: (21,-1) = Magpie's 74 + NR's 15 vertices, (20,-1) = 21 + 9, (21,-2) = NR's 82. It also carries the 3 CELL records (Magpie's versions for the two manor cells, NR's for (21,-2)) and an inert Tamriel WRLD copy (later plugins still win). Placed after `Authoria - Landscape - Morskom - City Trees.esp`, group Authoria - Landscape Patches.
- C. `Authoria - Magpie Manor - Patches\Seasons\zzAuthoriaMagpieManor_WIN.ini` (winter hides: outside roses, sunflowers, pink flower bush, flowering vine, nettle, celandine, lady's mantle, water lilies → InvisiStatic; climbing roses → CHA_invisiplant) and `aAuthoriaMagpieManor_NOSNOW.ini` (glass/cloth bases + all 189 references under the greenhouse roof). Greenhouse plants are kept alive in winter and kept snow-free. Mod's own tree swaps untouched. No spring file (dangling meshes).
- Plugin budget now: 238 full / 3801 light active (16 free full slots — the 08-18 session had already flagged more plugins light).

### Grass — what changed since the plan (from the 2026-08-18 pilot session, see memory)
- NGIO writes BASE-named output; seasonal suffix must be added by renaming; NGIO writes in place into whichever mod owns an existing filename; and in that session the generated cell set did not react to deleting files. Most likely cause: files were deleted while MO2 was open (stale VFS tree). So before touching the 350 target files, one controlled pilot with MO2 closed during the deletion.
- Full backup of all five caches already exists and is verified identical to the live mods: `D:\AUTHORIA-GrassCache-Backup-20260818`.

### Pilot staged (waiting for one game launch)
- Japhet's Folly worldspace (24 cells, complete in all five caches). 3 cells removed in all five variants → `_backups\2026-08-19 - grass pilot JaphetsFolly 3 cells\`: x0001y0001, x0000y0001, x-002y0000.
- `GrassControl.ini`: Updating-Cache = true, Only-pregenerate-world-spaces = JaphetsFollyWorld (original list kept in a comment line). `po3_SeasonsOfSkyrim.ini`: Season Type = 1 (winter). Backups `*.bak-magpieregen-20260819`. Empty `Stock Game\PrecacheGrass.txt` created.
- Expected if the method is sound: exactly 3 cells generated, 3 files in `overwrite\Grass\` (base-named), nothing else touched, NGIO log says resuming/generating for JaphetsFollyWorld only.
- Real run after the pilot: 70 cells (347 files exist today; 3 winter files never existed for x9y24, x9y25, x11y25), five passes, Default last, rename + move per pass.

### Grass — DONE (2026-08-19, 12:30–13:37)
Two pilots on Japhet's Folly settled how NGIO-NG 1.6.8 really works: it regenerates every cell of the listed worldspaces regardless of which cache files exist, writes base-named files, APPENDS to an existing base file through the VFS (corrupting it), and is gated only by the progress list inside `PrecacheGrass.txt` (`cell_<Worldspace>_<x>_<y>`, CRLF). So the method became: pre-fill the trigger file with all 16,571 other Tamriel cells, move the Default files of the two areas (300 files) out of the mod, pin the season, let the game run (~20 s of generation, positions (8,26) (21,-1) (9,30) (11,25) (6,29)), rename the 70 target outputs with the season suffix into the season mod, park the margin outputs, restore. Driver: `_tools\magpie-manor\grass_regen.py` (stage / collect / finish).

Result, verified name-by-name and size-by-size against the pristine backup `D:\AUTHORIA-GrassCache-Backup-20260818`: exactly the 70 target cells changed in Default/Spring/Summer/Autumn and 67 in Winter (the three Morskom cells x9y24, x9y25, x11y25 have no winter grass and never had a file); zero other files touched; file counts identical. The Default pass was redone in summer state (Season Type 3) after a seasons-off run produced no grass for the snowy Dawnstar cells — the July Default cache was clearly built in summer state. `po3_SeasonsOfSkyrim.ini` back to Season Type 5 (identical to its backup); `GrassControl.ini` back to the full worldspace list with `Updating-Cache = true` left on deliberately. Everything replaced or discarded is kept under `_backups\2026-08-19 - grass regen magpie-morskom\` (old-<pass>, discarded-<pass>, originals-targets, discarded-DEF-seasons-off).

Still yours to do: Synthesis (worldspace group) re-run, then the in-game walk (manor yard/greenhouse floors and Morskom in each season via Select Your Season; road corner at the manor's south-west; clutter clipping). Later: Reqtificator, DynDOLOD/TexGen/Occlusion, ParallaxGen.

### Blue-world incident (2026-08-19 afternoon) — RESOLVED, not Magpie/tools
Symptom: at the manor everything except sky and HUD deep blue; FWMF map dark. Evidence chain: the game's own screenshots show the SAME failure class (whole scene magenta) at 08:12 — before the Magpie install (11:29), before Synthesis/Reqtificator/ParallaxGen (13:42-13:54); the five regenerated outputs define zero weather/region/lighting records; the CS logs from the 08-18, 10:56 and 14:19 sessions (recovered via VSS shadow copies) show identical pipeline state. Cause: the 07:05 Community Shaders AIO dev-build update — Sky Gradient + Screen Space Reflections force-reset ON (the saved OFF blocks were schema-invalid and discarded at every load; the morning session's short-form off-entries were rejected too), plus a new Post Processing feature with five sub-effects silently ON (GT7 grading etc.). Sky Gradient corrupts sky stops per weather and SkySync propagates that into scene ambient → geometry tint varies by weather (magenta / blue), sky+HUD normal, map dark.
Fix applied: `overwrite\SKSE\Plugins\CommunityShaders\SettingsUser.json` (backup `.bak-blue-20260819`) — inside the full-schema blocks the build itself saved: SSR off, Sky Gradient off, all 13 Post Processing sub-effects off, and the update's other silent resets restored (Snow Cover havok, SSGI thickness, grass LOD trio). ENB preset files verified byte-identical (the 14:44 auto-save contaminated nothing). Details in memory `cs-aio-build-update-traps`.

### Blue manor, round 2 (2026-08-19 15:xx) — Snow Cover map, FIXED
After the settings fix the MAP was normal but the manor stayed blue -> second, location-keyed cause. CS Snow Cover's altitude map (`Shaders\SnowCover\Skyrim.dds`) is blurred; the big ridge next to Darkshade bleeds into the valley: the manor's map value said the yard sits ~12,000 units higher than it does, so the shader painted snow albedo (blue-white in shade) on every surface and purple foliage tint on the trees — rooster included. Whiterun/Riverwood read lowland values and stayed clean; Dawnstar/Winterhold read legit snow values.
Fix: repainted the valley pocket (world x 79000..98500, y -11000..8500) down to lowland grade 112 with a 24-px feather, rewriting only the 1,721 affected BC4 blocks; everything else byte-identical; backup `Skyrim.dds.bak-pre-valleyfix-20260819`. Next CS AIO update: this file counts as user-modified — preserve it (the update method's hash-diff will flag it). Memory: `cs-snowcover-map-valley-contamination`.

### Floating grass at the manor (2026-08-20) — FIXED
Cause: sequencing. The 70-cell grass regen ran 12:50-13:36 on 08-19; Synthesis (which re-asserts terrain) ran 13:42 — after it. So the manor cells' grass was baked against the pre-Magpie ground; when the merged terrain went live the yard dropped up to 152 units and the tufts floated at the old height. Only (21,-1) and (20,-1) changed height.
Fix: verified the Synthesis output's LAND now equals the merged patch exactly (0/1089 vertices differ, both cells), then re-baked just those 2 cells x 5 passes with the driver (now supports GRASS_REGEN_JOB / GRASS_REGEN_CELLS env overrides). All 10 files rewritten 08-20 06:29-06:55; round-1 files kept in `_backups6-08-20 - grass floaters magpie 2cells\`. RULE captured for next time: run grass passes AFTER Synthesis/terrain patches, never before.

### Rooster misplaced texture (2026-08-20) — FIX BUILT, pending enable + in-game check
Symptom: manor rooster (`_mag_RoosterNPC`) renders with its texture scrambled — head pattern on the torso. Cause: MagpieManor.bsa bundles Mihail's OLD-generation rooster mesh (shape `rdmobj00`) at an `aproco\magpie\` path but with Mihail's ORIGINAL texture paths embedded; `mihail - Roosters (se-ae)` provides the 22 MB REMASTERED `rooster.dds`/`_n` loose at that same path (pairs with the MMOP `grp020` mesh). Loose beats BSA → old mesh + new-layout texture. Broken since install day; only manifests alongside the Mihail rooster mod. Record chain, skeleton (vanilla-identical bones incl. the wattle/comb nodes), and Reqtificator output all verified healthy first.
Fix: new asset-only mod `Authoria - Magpie Manor Rooster Fix` (no plugin) — bundled mesh copied loose with its two embedded texture paths same-length byte-patched to private `textures\aproco\magpie\` names, plus the matched old-gen textures extracted from `MagpieManor0 - Textures.bsa` under those names (sole provider). Mihail's own roosters untouched. Full-archive audit: only other foreign-texture bundles are a Toxin Doctor chair + clock, no loose challenger, clean. ENABLED 08-20 via modlist.txt edit (MO2 confirmed closed; backup `modlist.txt.bak-roosterfix-20260820`), placed directly above `Authoria - Magpie Manor - Patches`; other 3 profiles untouched (their modlists predate Magpie entirely — MO2 syncs on next refresh, disabled). In-game check pending. Ledger: README inside the fix mod.
