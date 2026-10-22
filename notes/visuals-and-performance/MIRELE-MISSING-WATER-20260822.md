# Missing water near Mirele / the Guardian Stones — 2026-08-22

Reported: a whole chunk of water missing near Mirele Bismath Reborn and the Guardian Stones.

## Answer

The lake water is not missing from the game's data. It is missing from the picture.

One cell of lake — the cell between the Guardian Stones shore and Mirele's island — does not
draw its water. The cells on either side draw theirs normally. That is why the edge is a
razor-straight line: it is a cell boundary, and the hole is cell-shaped.

Cause: **Unified Water**, a beta feature in the Community Shaders build. It is the thing that
draws the lake here, and it draws water as one quad per cell. A per-cell drawer failing on one
cell gives exactly a cell-shaped hole. I have turned it off (§5). Second suspect is Terrain
Blending. One of the two is doing it; the test in §6 tells you which.

---

## 1. Where you were standing

Read out of the save.

- Guardian Stones cell, on the shore of Lake Ilinalta.
- Standing 281 units above the lake surface, on the bank.
- Looking roughly due west, across the water, towards Mirele's tower.

**Correction worth recording.** The save stores the *character's* heading, not the camera's,
and this build runs True Directional Movement, which deliberately decouples the two. I first
took the character heading (295 degrees) as the camera heading and drew a wrong conclusion
from it — see §4. Solving the camera from landmarks in the frame instead gives roughly 274 to
280 degrees, close to due west.

## 2. Proof the water is really missing, not just shallow shore

Water lilies are placed by their mod to float on the lake surface. Every one near you sits at
exactly the lake's surface height.

In the picture, two clumps are standing on dry gravel with their stems fully exposed and their
pads hovering about a metre above the ground. The ground under them is 77 to 115 units below
the lake surface. That ground should be under water. Further out, past the far edge of the
hole, the same lilies are floating correctly on rendered water.

So the lilies are at the right height, the bed is at the right height, and the water between
them is simply not drawn.

## 3. Proof it is a drawing fault and not a data fault

The most conclusive single thing found.

Twenty-four critter landing markers, created by the running game moments before you saved, are
sitting at exactly the lake's surface height over lake bed 120 and 168 units lower. The game
places those on water. So the engine's own water system knows the surface is there and is
using it. Only the visible surface is absent.

## 4. Where the hole is, and how that was pinned down

The water stops on one straight line and starts again on another. Both lines land on cell
boundaries: the near one on the boundary between the Guardian Stones cell and the cell west of
it, the far one on the next boundary west, where Mirele's island cell begins. Projecting those
two boundaries onto the screenshot puts them along the two edges, and puts the stranded lilies
between them and the floating lilies beyond.

**The error I made, and the correction.** I tested whether the edge was a world boundary or a
fixed distance from the camera by measuring its slope across the frame. The measured slope is
-0.021 pixels per pixel. Using the character heading from the save, a cell boundary would have
projected at about -0.12, so I concluded the edge could not be a cell boundary and had to be
camera-locked. That was wrong, because the character heading is not the camera heading here.
Re-running the same test across camera headings: a cell boundary projects at -0.021 at a
camera heading of 274 degrees, and at -0.045 at 280 degrees. Both are within the range the
landmarks give. The slope test does not rule out a cell boundary at all — it is consistent
with one.

The lesson: a nearly flat screen edge means the boundary is nearly perpendicular to the view,
which is exactly what a north-south cell boundary looks like when you face west.

## 5. Everything that was checked and cleared

Each was checked against the actual files.

| Checked | Result |
|---|---|
| Water surface height, all 75 lake cells | Identical everywhere. |
| Water settings on the dry cell vs the cells either side | Byte-for-byte identical, in every one of the 24 plugins that touch them. |
| The water definition itself | Intact, uncontested, all textures present. |
| Ground heights | Correct, and correctly below the water line. |
| Placed objects, all 4,002 active plugins, 9 cells | No water plane, nothing large laid over the lake, nothing disabled or deleted. |
| Distant-water tiles | All present, all at the right height, no gap between them. |
| DynDOLOD occlusion | No occlusion planes exist here at all. |
| Occlusion / LOD staleness | Not stale for this spot. No landscape input changed since they were generated. |
| Runtime record patching | Nothing patches cells or water. |
| Game water settings | All at defaults. |
| ENB | Not running at all. Community Shaders draws the water. |
| Papyrus, crash and shader logs | Clean. No compile failures, no crash. |

Since the dry cell and its neighbours are byte-identical and only one of them fails, no record
can be responsible. It has to be the renderer.

## 6. What I changed

Two things, both reversible, both made while Mod Organizer was closed.

1. **Turned Unified Water off**, using the feature's own disable-at-boot switch in the
   Community Shaders user settings. One key. Backup:
   `SettingsUser.json.bak-pre-unifiedwater-off-20260822`, same folder.
   Confirmed live: the session started at 13:26 loads every shader feature except this one.
2. **Set the Unified Water cache aside**, renamed with a `.stale-loadorder-20260822` suffix.
   It was built on the 21st; the load order was rewritten on the 22nd. The log shows it was
   loaded, not rebuilt, so the game was running on a cache keyed to a load order that no
   longer exists. Same stale-artifact trap as Synthesis and the Reqtificator. With the feature
   off it is unused; if you turn the feature back on it will rebuild clean.

Why Unified Water first:

1. It is the component that draws the lake in this setup.
2. Its own settings file marks it Beta, version 0-2-0.
3. It replaces the engine's water surfaces with its own, **one cell-sized quad per cell** —
   and the hole is exactly one cell. A per-cell drawer is the only thing in the render path
   that can fail per cell.
4. The quad it ships has a bounding box with zero height. A flat, zero-thickness bounding box
   is fragile for culling, and a culled bounding box means that cell's water is never drawn.
5. It has a built-in off switch, so turning it off costs only the beta's own polish.

## 7. The test

1. Stand where you were and look. If the lake is whole, that is the answer. Leave Unified
   Water off; it is a beta.
2. If it is still cut, restore the settings backup and instead turn **Terrain Blending** off
   in the Community Shaders menu, then look again. Terrain Blending replaces the depth buffer
   the water is tested against.
3. If neither works, disable **Splashes of Skyrim**. It rewrites 222 water definitions at
   startup to switch on displacement, which the beta water shader then has to handle.
4. Free five-second check worth doing in the same session before anything else: purge the cell
   buffer at the spot. If the water comes straight back, this is transient render state rather
   than configuration.

Whichever one fixes it, report it to the Community Shaders AIO author — this is an unofficial
dev build.

## 8. Separate real problems found on the way

Neither causes the missing water. Both are genuine.

1. **Northern Roads floods the south shore of Mirele's island.** It loads after Mirele and
   overwrites about twenty ground points that Mirele lifts out of the lake, pushing them back
   under the water line. No Northern Roads patch for Mirele exists. Fix is a small landscape
   patch loading after both, same shape as the Magpie Manor merge.
2. **Nature of the Wild Lands moves four of Mirele's trees.** It wins over Mirele and drops
   each tree 1,200 to 1,800 units from where Mirele put it. Cosmetic.

Also noticed: two copies of Smooth Terrain are both enabled. Only the higher-priority one is
live, so an edit to the other silently does nothing. Worth disabling one.

## 9. Tools written for this

All in `_tools\mirele-water\`. Reusable for any missing-water or flooded-terrain report.

- `savepos.py` — reads a save: player position, and with `changeforms.py` the character's
  heading. Two traps, both now handled: the offsets in the save's location table are absolute
  file offsets so the header and thumbnail have to come off them, and player location is
  global-data type 1, not type 3. **And the heading it gives is the body, not the camera,
  whenever True Directional Movement is installed.**
- `waterscan.py` / `lakescan.py` — ground height vs the water line, per cell and per vertex.
- `topomap.py` — top-down map of ground vs water with the player marked.
- `viewcast2.py` — renders the view from any world position using the landscape heightmap, so
  you can see what the engine ought to be drawing and compare it to a screenshot.
- `cellraw.py` — dumps a cell's raw subrecords from every plugin that touches it. This is what
  proved the records identical; the engine uses the winning cell record whole, so a winner
  that merely omits a field silently changes behaviour.
- `lodwater.py` — checks every distant-water tile for a missing water surface.
- `refscan_placed.py` / `refanalyse.py` — placed-object census across the whole load order.

**Method note.** Objects placed at a known height are free survey markers. Water lilies sit on
the water surface; lilies standing on dry ground prove the surface is not drawn and measure how
deep it should have been. Projecting candidate cell boundaries onto the screenshot and seeing
which one lands on the edge is more reliable than any slope test, because it does not depend on
knowing the camera heading precisely.
