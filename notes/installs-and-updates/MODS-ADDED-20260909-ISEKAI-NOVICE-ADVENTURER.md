# Isekai Novice Adventurer Outfit 3BA - PBR

**2026-09-09.** Nexus 172230, v1.2.2. Installed, Requiem-patched, BodySlide group built,
UBE-converted and registered. Registered in the **current profile only**
(`DEEZ CS NUTZ - PBR`), per the choice made during the install.

## Mods added - three, now four

| Mod | Contents |
|---|---|
| `Isekai Novice Adventurer Outfit 3BA - PBR` | the source mod, plugin `[Stella]IsekaiNoviceAdventurer3BA.esp` (ESL) |
| `Authoria - BodySlide Group - Isekai Novice Adventurer` | slider group, 7 projects, no duplicate output paths |
| `houseCARL - Authoria - Isekai Novice Adventurer - Requiem` | the Requiem patch (ESL) |
| `Authoria - UBE Converter Output - Isekai Novice Adventurer` | UBE meshes + patch plugin (ESL) |

## Requiem patch

22 records over 40 in the source. Leather tier for the worn armour, iron for the shield,
cosmetic for everything on an extra slot. Recipes are Craftsmanship-gated.

| Piece | Slot | Class | Armour | Value | Weight |
|---|---|---|---|---|---|
| Outfit | 32 | Light | 150 | 100 | 5.0 |
| Boots | 37 | Light | 45 | 30 | 1.5 |
| Armwrap | 33 | Light | 45 | 30 | 1.5 |
| Buckler | 39 | Heavy | 75 | 31 | 5.0 |
| Tights, Tights TR | 53 | Clothing | - | 10 | 0.2 |
| Armor decoration | 56 | Clothing | - | 25 | 2.0 |
| Cape (x2) | 57 | Clothing | - | 10 | 0.5 |

**The Reqtificator does NOT need a re-run.** Its output is from 28 August and predates
this patch, but the patcher would decline to touch these records anyway: `ArmorRatingScaling`
only fires when a rating is at or below the type threshold (light body 62, feet/hands 18,
heavy shield 54) and every rating here is above it, and `ArmorKeywordsFromRules` is guarded
by `keywords_none` over the assignable set, which the patch has already filled. So the
values above are final and the patch stays out of the master list. See
[[reqtificator-254-master-cap]] for why that guard matters.

The patch loads before `Requiem for the Indifferent.esp`; the UBE output loads after it, in
the `Authoria - Outputs` block, which is correct for an appearance-only patch.

## BodySlide

Group `Authoria - Isekai Novice Adventurer 3BA`, 7 projects: main armor, tights, tights TR,
boots, armwrap, cape, and the armor decoration. Built by the user into
`Authoria - Bodyslide Output - UBE` - 14 nifs, both weights, no zero-filled files.

## UBE conversion

`tools\CBBE to UBE\Authoria-DaysTool.exe`, scoped to the source plugin. 8 conversion units,
8 records minted, plugin ESL-flagged with 2040 forms of headroom. 14 output meshes and one
SMP config for the cape. Converter notes worth keeping: the tights were kept rigid (no source
physics and no chain bones, so no soft body was generated) and the belt and corset shapes
were kept skinned and morphable as body-conforming rather than given soft-body physics.
1383 overlay-band verts were lifted back on top of their under-layer.

**The first run stalled and had to be redone.** Twelve worker processes sat at zero CPU for
twenty minutes with the mesh phase all but finished - one mesh short, no plugin written. The
cause was the parent's stdout being a pipe nothing was draining, so the workers blocked on a
full buffer. Killed, output folder deleted whole (a killed run leaves partial and zero-filled
files - see [[ube-converter-run-traps]]), and re-run detached with stdout and stderr going
straight to files. Second run finished in **26.5 seconds**.

A wrinkle in between: `Start-Process -ArgumentList` given an array did not quote the paths
with spaces, and the tool rejected the split arguments. Each argument had to be wrapped in
double quotes and joined into one string.

## Registration

Current profile only, one line added to each of the four profile files, CRLF preserved,
diffed to confirm nothing else moved:

- `modlist.txt` line 194, at the top of the UBE output block
- `plugins.txt` line 4042 and `loadorder.txt` line 4102, after the Ninirim UBE patch
- `plugingroups.txt` line 83, group `Authoria - Outputs`

Backups: `_backups\<file>.bak-profile-pre-isekai-ube-20260909`.

## Verification

- `check_errors` on all three plugins: 0 dangling references, 0 missing masters, 0 unscannable records
- houseCARL sees the new plugin ACTIVE and resolved; 4125 plugins resolved to real files
- No zero-filled meshes in either the BodySlide output or the converter output
- **Outfit Wheeler: 86 items, 0 rewritten, calibrate 86 match / 0 mismatch.** Three ESL
  plugins went in today and none of them shifted an outfit plugin's light index - all three
  load after every plugin the wheel references. Reindexed and calibrated anyway, before launch,
  per [[wheeler-rawids-die-on-esl-change]].

## Not done

Nothing outstanding on this outfit. The staging folder with the install scripts, the
before/after profile snapshots and both converter logs is at
`_staging\isekai-novice-20260909`.
