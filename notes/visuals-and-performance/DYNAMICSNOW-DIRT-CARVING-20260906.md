# DynamicSnow carves dirt - findings 2026-09-06

Mod: `DynamicShader-DynamicSnow` (Nexus 189713, v2, file 796201) + `DynamicShader Core` (file 796202).
Enabled in profiles `DEEZ CS NUTZ` and `DEEZ CS NUTZ - PBR` (active). Disabled in the other four.
Nexus check 2026-09-06: both installed files are still the current files. No newer build exists.
Plan and 08-27 audit: `DYNAMICSNOW-INSTALL-PLAN.md`.

## 1. User report

"snow deformation is happening on dirt" - CONFIRMED from the mod's own log
(`Documents\My Games\Skyrim Special Edition\SKSE\DynamicSnow.log`, session 09:15-09:44 today,
walk through the river woods around Tamriel cells (19..23, -14..-7), cell (20,-13) = POIFallForest11).

## 2. Mechanism (from disassembly of DynamicSnow.dll, sha256 5b70248b0805...b7b56a, 903,680 bytes)

1. The landscape cache (`func_2a6a0`) rates every landscape QUAD = quarter cell, 2048 x 2048 units
   (about 29 m square). For each quad it runs the texture classifier on the quad's base texture AND
   all 6 paint layers, and keeps the HIGHEST class. Classes: 0 other, 1 snow, 2 sand, 3 mud.
   So mud outranks sand outranks snow, and one small painted strip anywhere in the quarter cell sets
   the class for the whole quarter cell.
2. Classifier (`func_27ef0`): lowercases the winning TextureSet diffuse path and substring-matches
   snow: snow01 snow02 snowpath grasssnow snowrocks snowstone snowslope
   sand: sand desert dune beach
   mud:  mud muddy soil peat swamp marsh bog
3. Stamps (feet, colliders, dropped objects, arrows, deaths) are recorded class-blind.
4. The per-frame rebuild `UpdateLandscape` (`func_336d0`) walks the 7x7 cached cells x 4 quads.
   At 0x33c0c it SKIPS a quad whose class is 0. For every other quad it sinks every vertex under a
   stamp with a per-class factor (0x343d1): snow 1.0, sand 0.4 (ridge 0.25), mud 0.65, times the
   18-unit base depth. Class 0 would also get 1.0 - it never reaches that code.

Result: a dirt trail, rock, or forest floor carves whenever its quarter cell also contains any
mud/marsh/river-mud texture (65% depth, about 12 units) or any snow texture (full depth, 18 units).
Only quarter cells with no snow/sand/mud texture at all are left alone.

## 3. Log evidence (today)

Quads whose VISIBLE textures are rock/dirt/forest floor but were rated mud or snow
(`v449-dbg: q{} class={} def={} layer0={}` lines, count of dumps):

| class | base texture | layer0 | dumps |
|---|---|---|---|
| 3 mud | Rocks01 | PineForest02 | 11 |
| 3 mud | Rocks01 | RiverbedEdge | 7 |
| 3 mud | PineForest02 | RiverbedEdge | 6 |
| 3 mud | RiverbedEdge | Dirt02 | 14 |
| 3 mud | Rocks01 / Dirt02 | Dirt02 / RiverbedEdge | 2 + 2 |
| 1 snow | Rocks01 | FallForestDirt01 | 7 |

The mud/snow texture sits in one of the deeper paint layers (the river bank, a snow patch), not in
the two textures the log prints. Typical `deepest` this session was -10 to -12 units = the mud
factor (0.65 x 18 = 11.7), with -19 to -23 spikes from object/actor stamps.

Object stamps on pure class-0 quads (`s0=18`) were recorded but produce nothing (the rebuild skips
those quads). Footprint bursts (`v404-def` rate up to 10/s) all happened with mud- or snow-rated
quads under the player.

Note: two different log lines share the prefix `player-cell quads=[...]`: v206 (S/A/M/- = class)
and v140 (Q/m/l/- = mesh resolution). `[--ll]` is the v140 line, not classes.

## 4. Options

A. Disable the trial (clean, one minute). Flip these three lines from `+` to `-`:
   - `profiles\DEEZ CS NUTZ - PBR\modlist.txt` lines 53-55:
     `Authoria - Smooth Terrain - Snow Trial Profile`, `DynamicShader-DynamicSnow`, `DynamicShader Core`
   - `profiles\DEEZ CS NUTZ\modlist.txt` lines 51-53: same three.
   Do NOT restore `modlist.txt.bak-snow-20260827` - it is 10 days stale and would undo later edits.
   No plugin, no co-save data, no settings: saves untouched.

B. Two-byte patch: make sand and mud count as "other" so only snow-textured quarter cells carve.
   **APPLIED 2026-09-06 10:13** at the user's request via `_tools\dynamicsnow\patch_classes.py --apply`
   (--check / --revert available). Patched DLL sha256 4f490a6a775b...63c0bd5f. Backup of the original
   beside it: `DynamicSnow.dll.bak-pre-classpatch-20260906` (not a *.dll, SKSE ignores it).
   MO2 was open at the time; nothing in profiles\ was written.
   File offset 0x27557: 02 -> 00 (`mov ebx,2` sand class)
   File offset 0x27562: 03 -> 00 (`mov ebx,3` mud class)
   Effect: river-bank / marsh / beach quarter cells stop carving entirely (dirt next to them too).
   Remaining: dirt inside a quarter cell that also holds any snow texture still carves at full depth.
   Verify in game: `DynamicSnow.log` v206 lines show only `S` and `-`; v449 lines never show class=2/3.

C. Per-vertex classification (use the layer alpha weights under each vertex) is the real fix.
   That is new code, not a byte patch. The official CS Snow Deformation alpha build in Downloads is
   a whole-renderer migration (plan doc section 7) and has not been checked for this behaviour.

## 5. Disassembly bookmarks (DynamicSnow.dll RVA)

- func_27ef0 classifier; returns at 0x2814b (1), 0x28156 (2), 0x28161 (3), 0x281b5 (0)
- func_2a6a0 landscape cache; class = max over base + 6 layers at 0x2ad02-0x2ad3d; stored quad+0x64
- func_336d0 UpdateLandscape; class-0 skip 0x33c0c -> 0x34ee0 (next quad); factors 0x343d1, 0x344f7
- func_32ad0 object stamps (v469 sClass counters, no gate); func_3c190 actor stamps (no class read)
- Listing + tooling: session scratchpad `snowdis\` (snowdis2.py builds `listing.txt` with capstone)
