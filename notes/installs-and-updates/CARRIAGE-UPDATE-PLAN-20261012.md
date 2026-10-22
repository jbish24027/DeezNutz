# Carriage update plan - 2026-10-12

Status: PLAN ONLY. Nothing in mods/ or profiles/ has been written.

## What is installed now (all 8 profiles)
- Animated Carriage 1.1.0 (AnimatedCarriage.esm is FULL - costs a slot) + ACLine_Whiterun.esp
- Witcher Horses - Animated Carriage Patch (horse textures on the 16 carts; carriage meshes with Witcher horses)
- Authoria - Patch - Animated Carriage NR - No Additional Routes.esp (86 Whiterun-line markers moved for
  Northern Roads + Lux Via bridge). Only the 2 Whiterun routes run today.
- Authoria - Reqtificated - Animated Carriages.esp (Requiem output)
- PG_1.esp in "Authoria - PG Output" overrides 10 carriage goods containers
- Authoria - Carriage PBR Wood Fix (PBR, PICTA, Preset Studio only)
- CFTO stack, Snazzy Diverse Carriages, Wait Carriage in Inns, Followers Sit on Carriages - untouched

## What the downloads are
| Archive | Version | Notes |
|---|---|---|
| Animated Carriage | 1.2.1 | ESM is now ESL-flagged (frees 1 full slot). 31 Solstheim records (Redoran/Telvanni/Skaal) got NEW FormIDs. 4 scripts updated. ACLine_Whiterun.esp byte-identical. |
| Animated Carriage Additional Route | 1.6.4 (2026-08) | 42 routes, 2 ESPFE plugins. Vanilla-road heights. |
| Animated Carriage for Northern Roads | v1 (2024-05) | Fork of Additional Route 1.6 with NR heights. Misses 1.6.1-1.6.4 fixes (broken Whiterun link, Hadvar stuck at Riverwood, overwritten records, linked refs). 1852 of 1905 markers moved, mostly z (median -17). |
| Additional Route compat patches FOMOD | 0.83 | Relevant to us: GG Markarth Outskirts (Northern Roads variant) and JKs Solitude Outskirts. Both master the VANILLA-road Additional Route plugin. |
| Carriage Stops of Skyrim | 1.9 | Benches + brazier stops, fade-to-black paid travel. 16 vanilla REFR overrides, 49 CELL overrides. |
| Animated Carriages Take You Everywhere | 2.2.2 | Needs Carriage Stops. Updated for AC 1.2.1 (changelog 2.2). Ships its own build of AC's cart script and of Carriage Stops' bench script. Overrides 24 cart activators (adds a script property) - collides with the Witcher patch on 16 of them (Witcher changes the horse texture, ACTYE the script). 9 new NPCs. |
| Skyking Carriages | 1.2 | Retextures + high-poly wheels for VANILLA carriage meshes only. Textures are named after the carriage materials (Markarth wood, farmhouse wall, Riften planks, prisoner carriage, wheel) in textures\Skyking\carriage. |
| Skyking Carriages Embers XD patch | 1.0 | Burnt Helgen cart. |

## Breakage the update causes (must be fixed in the same pass)
1. Authoria - Reqtificated - Animated Carriages.esp: 7 overrides + 2 references point at the 31 renumbered IDs.
2. PG_1.esp (Authoria - PG Output): 1 override (Redoran goods container) points at a renumbered ID.
   Fix for both: remap old ID -> new ID by EditorID, in place, backup first. No generator rerun.
3. Witcher patch vs ACTYE on 16 carts: one merged patch carrying both changes.
4. Animated Carriage meshes are custom (clutter\vicn\cart). Skyking does not touch them. PG output copies win over
   every carriage mesh in all profiles, so a plain Skyking install would show nothing.

## Proposed build
- Update Animated Carriage in place to 1.2.1 (all 8 profiles; mod folder shared).
- Routes: Additional Route 1.6.4 as the base, plus a new "Authoria - Animated Carriage Routes - Terrain Fit" patch:
  every route marker keeps the author's height above ground but sits on OUR winning terrain
  (Northern Roads + all Authoria landscape edits + Synthesis Worldspace). Where the NR author moved a marker sideways,
  take their x/y. Markers on bridges are listed and checked one by one.
- Add the relevant compat patches, rebased the same way.
- Carriage Stops + ACTYE: install, then check every bench for clipping against our town mods; fix by moving the stop.
- Skyking: one new mod with Skyking's own meshes + the 8 Animated Carriage meshes re-pointed at Skyking textures,
  placed where the Carriage PBR Wood Fix sits now (that fix retires - Skyking replaces those exact wood textures).
- All new plugins ESL-flagged. Positions decided by hand, all 3 profile files + plugingroups in lockstep, all profiles.
- Verify: whole-order missing-masters check, conflict tree on every CELL the new plugins touch, asset winners.

## STATUS 2026-10-12 11:05 - BUILT (one step owed)
Done in all 8 profiles:
- Animated Carriage 1.2.1; Reqtificated AC patch + PG_1.esp remapped to the new IDs (0 dangling, 0 missing masters).
- Additional Route 1.6.4 + 2 compat patches; Carriage Stops 1.9; ACTYE 2.2.2 (all light; plugins right after ACLine_Whiterun.esp).
- houseCARL - Authoria - Patch - Animated Carriage Routes - Terrain Fit (2170 route points; bridge decks by mesh raycast;
  11 Whiterun junctions keep the new branch links; cell headers from the last non-output plugin).
- houseCARL - Authoria - Patch - Animated Carriage - Witcher x ACTYE (16 carts: Witcher horses + go-anywhere script).
- Skyking Carriages 2K parallax + Embers XD patch; Authoria - Skyking Carriages - Over Outputs replaces the wood fix (disabled).
Owed: MO2 + Skyrim were started at 10:59 mid-job. When closed, apply _tools\carriages\stop_ops.json (17 stop fixes) into the
Terrain Fit patch and re-check its light flag. Reports: _tools\carriages\fit_report.csv, fit_final_bridges.csv.

## STATUS 2026-10-12 12:20 - COMPLETE
Stop fixes written (17 objects at Riverwood, Riften, Ivarstead, Markarth, Dragon Bridge road, Pale road). Patch light, 2187 positions
verified, 0 missing masters in the whole order, 0 dangling refs in both Authoria carriage patches.

## STATUS 2026-10-15 - bridge crowns fixed (user screenshot: horse belly-deep in Another Riverwood Bridge)
Cause: the 10-12 deck fit took the surface NEAREST the author's z (or the lowest one above it), which on a humped
bridge with an underside is the beam under the deck, not the planks. Facing-aware re-audit of all 133 raised markers
(_tools\carriages\bridges5.py / audit_all.py) found five bridges with a real deck above the cart; the Solitude one was
the vanilla SBridge01, which JK's Solitude Outskirts leaves initially-disabled, so it was dropped (JK's own bridge is fine).
Written into houseCARL - Authoria - Patch - Animated Carriage Routes - Terrain Fit (backup: _backups\2026-10-15 - carriage
bridge crowns\, md5 74652ff2...; after: c0011047..., 258852 bytes, light flag kept, 0 dangling / 0 missing masters):
- Riverwood (ARB main span, humped -167..+75): 00080D z -38 -> 80.                       sink <= 8, float <= 9
- Markarth outskirts (Lux Via hump bridge, scale 0.8): ED2 -7481 -> -7437, ED3 -7367 -> -7206, ED4 -7353 -> -7217,
  ED5 -7470 -> -7446, plus 2 NEW markers 000800 / 000801 (Terrain Fit) spliced into the chain ED2 -> 800 -> ED3 and
  ED4 -> 801 -> ED5 (base zxACCartMarker03, persistent, rotation interpolated).         sink <= 10
- Road west of Rorikstead (Lux Via ViaBridge01 CotN): 9D1 -5917 -> -5791 plus NEW marker 000802 between 9D1 and 9D2
  (base zxACCartMarker04).                                                               sink <= 6
- Windhelm (Lux Via CotN bridge; NR fork had lowered these onto NR's bridge): 966 -> -12742, 967 -> -12604, 968 -> -12652.
                                                                                          sink <= 14, float <= 14
Mechanics confirmed in zxAC_RqBaseScript: the cart does TranslateToRef marker to marker (straight chord, marker rotation =
cart pitch), so chord sag is real and a convex hump needs a marker near its crown. Residual floats of 30-78 on the two
approach segments of Markarth / Windhelm / Rorikstead are the bridge end ramps below the chord and were there before
(terrain not modelled); in-game check owed. Lux Via's Windhelm dockside gallows stands on the route at 966 (not touched).
