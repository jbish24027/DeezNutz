# Grass cache rebuild - 2026-10-15

## What changed
- New cache mod `Authoria - Grass Cache - Smooth 2026-10-15` (slot of the old Default cache in all 8 profiles; the five old
  `Authoria - Grass Cache - <season>` mods are unticked in every profile and kept on disk as fallback).
- Built with FasterNGIO 1.4 (tools\FasterNGIO, MO2 executable "FasterNGIO - grass cache"), smooth placement, all 121
  worldspaces with terrain ticked, Seasons of Skyrim detected: one run writes the plain file plus WIN/SPR/SUM/AUT per cell.
  Run 2 took 5 min; 418,150 files written, 329,888 of them 4-byte "no grass" placeholders that were deleted (Only-load-from-cache
  treats a missing file the same way). 88,262 grass files remain. Grass-bearing cells per season: plain 15,750, winter 14,691,
  spring 20,467, summer 20,471, autumn 16,883 (Tamriel alone: 5,630 / 4,986 / 8,123 / 8,123 / 6,275).
- Coverage grew: city worldspaces (Whiterun 48 cells, Riften 54, Markarth 629, Windhelm 23, Solitude 27), the fair (605 files),
  Blackreach, Bruma, Solstheim and every other worldspace the old ini list skipped. Whiterun city was configured for grass by
  Grass Cache Helper NG but had never had a cache.
- Before the bake: Witchy Wilderness flower densities cut to about half in `DEEZ NUTS.esp` (36 records, see memory), and the
  three seasonal master configs (`Authoria - Seasons Patches\Seasons\xAuthoria*MasterConfig_SUM|SPR|AUT.ini`) had 72 Seasonal
  Landscapes swap lines commented out (`;AUTHORIA-WW-WINS 2026-10-15:`) because Seasons keeps the LAST line per texture and those
  lines sat below Witchy's, giving Seasonal Landscapes grass on the tundra, field grass, forest floors, Reach meadows, frozen marsh
  and hot springs in spring/summer/autumn since July. Autumn tundra and field grass now fall back to Witchy's base grass
  (user choice).
- CRDW: the interface cache was deleted in the HPH, PBR and PICTA profile cache folders so CRDW rebuilds its directory walk
  (including Data\Grass) on each profile's next launch.

## Verified
- Whiterun tundra cell: Witchy grass in plain/summer/spring/autumn, winter unchanged; Reach meadow and Rift forest cells Witchy in
  summer and autumn; a 391-file random sample of Tamriel season files carries no Seasonal Landscapes grass; FormIDs point at the
  current Witchy Wilderness Resources slot.
- Not yet seen in game.

## Backups
- `_backups\2026-10-15 - Grass cache FasterNGIO bake\` (modlists before, bake 1 parked), `...- Seasons master config WW wins\`,
  `...- WW fewer flowers\`, `...- FasterNGIO setup\`.

## Open
- A future FasterNGIO run must tick all worldspaces again (the GrassControl.ini list still skips 45 of them).
- The orange "Ray-cast-texture-forms: expected formid:Plugin.esp, not '904'" line = a malformed entry in GrassControl.ini (NGIO
  ignores it too); fix when convenient.
- Vanilla placement can be baked into a second mod to compare against smooth.

## 2026-10-15 later: "grass not 3D / sideways / quarter quality" - CAUSE AND FIX
- Not the cache. Blade data decoded against the game's own August bake: positions, heights, upright and slope-fitted bases identical
  in form (orthonormality error 0.001 under the tool's slot layout for both engine-written and FasterNGIO files).
- Cause: the 2026-09-26 DynDOLOD run ("Create assets for CS Optimized Grass") rewrote 142 of 145 grass meshes into
  `Authoria - Dyndolod Output\meshes\landscape\grass\` (winning over Witchy / DrJacopo originals): each one swaps its own complex-grass
  texture (e.g. ComplexGrassHybridDrJ_skinny.dds, TundraSedum_DrJ.dds) for a tile of a 4096 DynDOLOD atlas, and most geometry bytes
  change. Result: low-res tile, flat shading (no complex-grass lighting data), plus CS Grass Optimizations Mesh LOD swapping in flat
  stand-in planes (`meshes\LOD\Grass\*_lod1.nif`) past 8 px. Hidden until now because the old summer tundra used three Seasonal
  Landscapes grasses that were never rewritten; every Witchy model was.
- Fix applied (MO2 + game closed): both folders parked to `_backups\2026-10-15 - DynDOLOD CS grass assets parked\` (145 + 145 files);
  CS SettingsUser.json Grass Optimizations EnableMeshLOD/EnableMidLOD/EnableFarLOD true -> false (backup beside the parked files);
  CRDW interface cache deleted in PICTA (HPH/PBR already pending). The 290 atlases (5.0 GB) stay in the output, unreferenced.
- Long-term equivalent: rerun DynDOLOD without "Create assets for CS Optimized Grass".
- Side note: FasterNGIO smooth mode wrote ~40 % fewer blades per cell than the game's own bakes (cap blades per quadrant = on,
  per-type density calibration); revisit with vanilla placement and the cap off if the grass reads thin.

## 2026-10-16 ~05:15 user check after the parking
- "grass looks better" - the September rewrites were the cause; CONFIRMED in game.
- Open: far tundra grass reads orange (candidates: CS Grass Lighting transmission saturation 1.4 / subsurface 1.0 under low sun,
  or the orange-yellow tundra ground showing through thin far grass). Screenshot 344: a hard-edged dark green land-texture patch
  against yellow-orange tundra ground = two texture sets meeting (ground, not grass). User intends to swap the texture overhaul;
  that swap needs xLODGen + TexGen + DynDOLOD (without CS grass assets) + a grass rebake afterwards, as one job.
