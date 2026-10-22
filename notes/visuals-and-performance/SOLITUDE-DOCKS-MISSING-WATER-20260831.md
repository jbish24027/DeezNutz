# Missing water at Solitude docks - 2026-08-31

**Fixed.** Unified Water is off again. It had been silently switched back on four days ago.

---

## What you were looking at

Screenshots 349-354, taken 05:17:20 to 05:17:43. `Save19` was written at 05:17:51, eight
seconds after the last one, so the save is that exact spot.

- Worldspace **Tamriel**, cell **(-17, 22)**, FormID `0092DE` `STISolitudeIcerunnerExterior02`
- You stood at `x -68072.4  y 92571.2  z -13878.9`
- The water surface there sits at `z -14000`, so you were 121 units above it, on the dock

That is Solitude docks. The harbour is JK's Solitude Outskirts plus Dynamic Boats at Docks,
the red maples next door are Val Serano (`AXSafeHarbor01` is the cell one step west).

## What is actually wrong

A cell-shaped rectangle of **water surface** is not being drawn. The water itself is fine.
The koi are still swimming, the kelp is still standing upright, you can still fall in. Only
the drawn surface is gone.

You can see it is a rectangle, not a blur or a fade: in screenshot 354 the edge is two
straight lines meeting at a hard corner. A camera-distance effect would give you a curve.
Two straight edges and a corner means a flat, four-sided piece of geometry is missing.

## Why

Community Shaders' **Unified Water** draws water as one flat quad per cell. Here is the
mesh it ships, `meshes/water/WaterMesh.nif`:

    4 vertices:  (-2048,-2048,0) (2048,-2048,0) (2048,2048,0) (-2048,2048,0)
    2 triangles

One quad, 4096 x 4096, which is exactly one Skyrim cell. Fine so far. But the box the
engine uses to decide whether that quad is on screen is this:

    BSMultiBoundAABB   Center (0, 0, 0)   HalfExtents (2048, 2048, 0.0)

**The Z half-extent is zero.** The cull box has no height at all - it is a flat sheet, not
a box. Testing a flat sheet against the view frustum is a degenerate test, and at some
camera angles one cell's sheet fails it while the cells around it pass. That cell's water
quad is then never drawn.

That is the whole bug, and it explains every single thing in your screenshots: a hole
exactly one cell across, straight edges on cell boundaries, a sharp corner, neighbouring
cells fine, and the water body underneath completely untouched.

## It is not your mod data

I checked, because a missing water height in a winning cell override would look identical.
It is clean. The broken cell and the neighbours that render fine are identical in every
water field:

| cell | editorid | WaterHeight | Water type | Flags | draws? |
|---|---|---|---|---|---|
| (-17,22) | STISolitudeIcerunnerExterior02 | FLT_MAX | RiverWaterFlowSolitude | HasWater | **no** |
| (-16,22) | STISolitudeIcerunnerExterior01 | FLT_MAX | RiverWaterFlowSolitude | HasWater | yes |
| (-17,23) | EastEmpireTradingCompanyDocks | FLT_MAX | RiverWaterFlowSolitude | HasWater | yes |
| (-16,23) | SolitudeDocks01 | FLT_MAX | RiverWaterFlowSolitude | HasWater | yes |

`FLT_MAX` means "use the worldspace default", which for Tamriel is -14000. That is correct
and normal for every coastal cell. 24 plugins touch the broken cell and not one of them
does anything wrong to its water.

Unified Water's own precache agrees. Its `Tamriel_cache.wc` has a valid entry for
(-17, 22) carrying the right water type (`0x08FFE9`, RiverWaterFlowSolitude) and the right
height (-14000). The feature knows the water is there. It just doesn't draw it.

## Why it came back

You already had this fixed. This is the same bug as Lake Ilinalta on 2026-08-22, and
Unified Water was turned off that day. Then:

| when | `Disable at Boot -> UnifiedWater` | |
|---|---|---|
| 08-22 13:23 | `false` | before the fix - feature ON |
| 08-22 | `true` | fix applied |
| 08-24 15:57 | `true` | holding |
| 08-27 05:40:37 | `true` | holding |
| **08-27 05:41:02** | **`false`** | **reverted** |
| 08-30 04:10 | `false` | still reverted |

The flip is 25 seconds after the `pre-astralite-restore` backup. The culprit is
`Authoria-Astralite-CS-Build-Export-v2-20260820.zip`. Its
`overwrite-seed/SKSE/Plugins/CommunityShaders/SettingsUser.json` carries
`UnifiedWater: false` - it was packed on 08-20, two days *before* the fix existed. Restoring
CS settings out of it on 08-27 put the pre-fix state back.

And Unified Water definitely ran after that: it rebuilt all 130 of its worldspace cache
files on **08-28 at 14:06** with a fresh load-order hash. A disabled feature cannot do that.

## What I changed

One value, in `overwrite/SKSE/Plugins/CommunityShaders/SettingsUser.json`:

    "Disable at Boot": { ... "UnifiedWater": false  ->  true ... }

Backup: `SettingsUser.json.bak-pre-unifiedwater-off-20260831`. JSON re-validated, CRLF line
endings preserved, nothing else in the file touched. MO2 and Skyrim were both closed.

This puts you back exactly where you were between 08-22 and 08-27.

**What you lose:** Unified Water only adds subsurface scattering and PBR sun specular on
water. It is not your water transparency - that is Effects 11 `[WATER] Muddiness`, and it is
untouched. You ran without Unified Water for five days and didn't notice.

## The trap, so this doesn't happen a third time

The 08-20 Astralite export still contains `UnifiedWater: false`. **If you ever restore CS
settings from that zip again, this bug comes straight back.** I have not edited the zip -
it is a share you built for your friend and that is your call, not mine. But either fix the
seed file inside it or re-apply this flag every time you restore from it.

## If you want the feature back

I built the targeted fix but did **not** install it:

    C:\1. AUTHORIA\_staging\Authoria - Unified Water Cull Fix\

It is the same `WaterMesh.nif` with one byte changed, giving the cull box a real height:

    HalfExtents (2048, 2048, 0.0)  ->  (2048, 2048, 2048)

A bigger cull box is the safe direction - it can only make something draw when it didn't
strictly need to, never the reverse. Geometry is untouched, file size identical, md5s and
install steps are in that folder's README.

It is **untested**. The mechanism is read straight out of the shipped mesh, but nobody has
confirmed in game that the flat box is what makes the cull fail. Turning the feature off is
the known-good state and needs no test. Try the mesh only if you want the SSS back.

## What to check when you next play

Load `Save19`. You are standing on the spot. Look at the lake.

- **Water is there** - fixed, and the Ilinalta cell should be fixed too. That also finally
  settles the 08-22 test that was left pending.
- **Still a hole** - then Unified Water was not the cause after all. Say so and I will go
  to the next candidates from the Ilinalta hunt: Terrain Blending off, then Splashes of
  Skyrim off.

Worth a quick look at Lake Ilinalta between the Guardian Stones and Mirele too, since that
is the other known site and it confirms the fix generalises.
