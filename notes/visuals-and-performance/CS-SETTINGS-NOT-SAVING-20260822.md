# CS settings not saving - investigation 2026-08-22

Session examined: CommunityShaders.log, 08:25:11 -> 08:34:24 (game quit ~08:34).
CS build: v1-8-0-0. Profile: DEEZ CS NUTZ.

## What the session actually wrote to disk

Only four files, all in `mods\[NoDelete] Soul Core ENB - Data\enbseries\`:

    enbadaptation.fx.ini      08-22 08:34
    enbbloom.fx.ini           08-22 08:34
    enbeffect.fx.ini          08-22 08:34
    enbeffectpostpass.fx.ini  08-22 08:34

Plus `overwrite\SKSE\Plugins\CommunityShaders\SettingsUser.json` (08-22 08:34).

NOT written: `enbseries.ini` (still 08-17 05:17) and every per-weather preset
ini (`SoulClear.ini` etc., still 08-11 / 08-13).

No read-only attributes on any of them. No VFS conflict: only one mod supplies
`enbseries.ini`. Overwrite holds the only `SettingsUser.json`.

## Finding 1 - five CS features are pinned by override files (PROVEN)

`mods\[NoDelete] Astralite Weathers\SKSE\Plugins\CommunityShaders\Overrides\`
holds five override JSONs. CS applies them at load AND again 6 ms before it
saves:

    [08:34:17.405] Applied override from Astralite to GrassLighting
    [08:34:17.405] Applied override from Astralite to WetnessEffects
    [08:34:17.405] Applied override from Astralite to CloudShadows
    [08:34:17.405] Applied override from Astralite to Skylighting
    [08:34:17.405] Applied override from Astralite to SkySync
    [08:34:17.411] Saving settings to ...\SettingsUser.json

Every pinned value in the saved SettingsUser.json is byte-identical to the
override file. In-menu edits to these values cannot survive a save.

Pinned values (19 total):

| Feature panel   | Key                          | Pinned to |
|-----------------|------------------------------|-----------|
| Cloud Shadows   | Opacity                      | 0.6       |
| Grass Lighting  | BasicGrassBrightness         | 0.6       |
| Grass Lighting  | SubsurfaceScatteringAmount   | 1.0       |
| Grass Lighting  | OverrideComplexGrassSettings | 1         |
| Skylighting     | MaxZenith                    | 1.5707963 |
| Skylighting     | MinDiffuseVisibility         | 0.1       |
| Skylighting     | MinSpecularVisibility        | 0.1       |
| Wetness Effects | MaxPuddleWetness             | 2.1       |
| Wetness Effects | MaxRainWetness               | 1.15      |
| Sky Sync        | Enabled                      | true      |
| Sky Sync        | UseAlternateSunPath          | true      |
| Sky Sync        | SunPath                      | 1         |
| Sky Sync        | CustomAngle                  | -35.0     |
| Sky Sync        | MinShadowElevation           | 0.25      |
| Sky Sync        | MoonLightSource              | 0         |
| Sky Sync        | SunriseBeginOffset           | 0.0       |
| Sky Sync        | SunriseEndOffset             | 0.0       |
| Sky Sync        | SunsetBeginOffset            | 0.0       |
| Sky Sync        | SunsetEndOffset              | 1.0       |

Fix: edit the override JSON, not the in-game slider. Or delete/rename the
override file to hand control back to the menu.

## Finding 2 - Effects 11 left column never reaches disk (PROVEN)

Four "Save & Apply" presses today (08:33:29, 08:33:34, 08:34:17, 08:34:22).
Each one logged `[EFFECTS11] Saved settings to ...` for the four .fx.ini files
and nothing for `enbseries.ini`. That file's mtime is unchanged since 08-17.

The left column of the Effects 11 panel (BLOOM, ENVIRONMENT, SKY, PARTICLE,
RAIN, FIRE, VOLUMETRICRAYS, PROCEDURALSUN, SUNGLARE, VOLUMETRICFOG, GLOBAL,
LIGHTSPRITE, EFFECT, GAMEVOLUMETRICRAYS) is stored in `enbseries.ini`.

Worse: Save & Apply RELOADS the preset from disk afterwards -

    [08:33:36.892] [EFFECTS11] Applying effect 'enbbloom.fx' / Unloaded ...
    [08:33:38.785] [EFFECTS11] Preset loaded from '...\enbseries',
                               settings from '...\enbseries.ini'

so pressing Save & Apply actively reverts left-column edits to whatever is on
disk. That is a visible "my change just undid itself".

Fix: left-column values have to be written into `enbseries.ini` on disk.

## Finding 3 - CS core settings unchanged since 08-19

`SettingsUser.json` was rewritten today, but its 729 values are identical to
the 08-19 post-fix state (SSR off, Sky Gradient off, 13 Post Processing
sub-effects off, Snow Cover AffectHavok 0, Grass Optimizations MeshLOD off,
screenshot key 0). Nothing else has changed in three days.

## Ruled out

- Read-only flags: none.
- MO2 write redirection: writes reach the mod folder fine (the four .fx.ini
  files prove it).
- Competing copies of SettingsUser.json / SettingsDefault.json in mods: none.
- "Invalid settings for <feature>, using default" (the 08-19 partial-block
  trap): does not appear in this log.
- HDR auto-detect: handled by `Disable at Boot -> HDRDisplay: true`.
- Right column of Effects 11: writes work. enbeffect.fx.ini has drifted from
  its 08-17 backup (Bloom Blending Day Linear Blend Amount, three Kitsuune
  tonemap values, AGIS Night Min Saturation).

---

## Confirmed with user 2026-08-22: Effects 11, Weather tab, FIRE + ENVIRONMENT

Both categories have `IgnoreWeatherSystem=false` in `enbseries.ini`, so the live
values come from the ACTIVE weather's preset ini, not from `enbseries.ini`.

Neither destination was written by today's session:
- `enbseries.ini`            08-17 05:17 (unchanged)
- all 21 weather preset inis 08-11 / 08-12 / 08-13 (unchanged)

Save & Apply writes the four .fx.ini files only, then reloads the whole preset
from disk (log 08:33:36 -> 08:33:38), which is what visibly snaps the edit back.

### How much the two categories vary per weather

    [FIRE]         21 weather files -> 2 distinct blocks
                   20 files identical; only OtherWorld.ini differs
    [ENVIRONMENT]  21 weather files -> 21 distinct blocks (all unique)

So a FIRE change is effectively weather-independent and can be applied
uniformly, or driven from one file by setting [FIRE] IgnoreWeatherSystem=true
in enbseries.ini (cost: loses the OtherWorld.ini variant).
An ENVIRONMENT change is weather-specific and has to be applied per weather, or
as a proportional delta across all 21.

### FIRE keys (identical in 20 of 21 weathers)

    IntensityDawn=1.1   IntensitySunrise=1.3  IntensityDay=1.6
    IntensitySunset=1.3 IntensityDusk=1.1     IntensityNight=1.0
    IntensityInteriorDay=1.15  IntensityInteriorNight=1.15
    CurveDawn=1.1  CurveSunrise=1.05  CurveDay=1.0   CurveSunset=1.05
    CurveDusk=1.1  CurveNight=1.1     CurveInteriorDay=1.0
    CurveInteriorNight=1.0

### Next-session proof test

Baseline hashes of enbseries.ini + all 30 preset inis taken 2026-08-22 08:47:
`_tools\cs-e11-left-column-baseline-20260822.md5`

Test: launch, Effects 11 -> Weather tab -> FIRE, change one value to something
obvious, press Save & Apply, quit. Re-run md5sum -c against the baseline. If
every file still matches, the left column cannot write and all left-column
edits must be made on disk from now on.

---

## Applied on disk 2026-08-22 08:55 (user request)

Backup of all 22 originals:
`_backups\2026-08-22 - E11 fire curve + ambient\`

Written into `enbseries.ini` + all 21 weather preset inis (22 files,
347 values changed, 352 verified):

    [ENVIRONMENT]
      AmbientLightingIntensityDawn      = 0.75
      AmbientLightingIntensitySunrise   = 0.75
      AmbientLightingIntensityDay       = 0.75
      AmbientLightingIntensitySunset    = 0.75
      AmbientLightingIntensityDusk      = 0.75
      AmbientLightingIntensityNight     = 0.75
      AmbientLightingIntensityInteriorDay   = 0.5
      AmbientLightingIntensityInteriorNight = 0.5

    [FIRE]
      CurveDawn CurveSunrise CurveDay CurveSunset
      CurveDusk CurveNight CurveInteriorDay CurveInteriorNight = 2.0

CRLF and no-BOM preserved; line counts unchanged.

### What these values were before

Exterior ambient ranged 0.7 - 1.0 per weather and time of day (outliers:
SSECMania dawn/dusk 2.0, SoulWyrmstoothFog night 0.25). Interior ambient was
1.0 in every file. Fire curve was 1.0 - 1.1 (OtherWorld 1.06).

So: interiors are halved, exteriors are flattened to one value for every
weather, and fire curve roughly doubles.

Revert = copy the backup folder back over the mod.

Baseline hashes in `_tools\cs-e11-left-column-baseline-20260822.md5` were
REFRESHED after this edit, so the "does Save & Apply write anything" test is
still valid on the next session.

---

## Correction 2026-08-23: the FIRE edit above used the wrong key names

The 08-22 edit wrote `[FIRE] CurveDawn..CurveInteriorNight=2.0`. Effects 11 never
reads those keys, so nothing changed in game.

Proof: the CS AIO DLL's setting-name table contains `FireCurve`, `FireIntensity`,
`GlowCurve`, `GlowIntensity` for the FIRE category, and no `CurveDawn` /
`IntensityDawn` string at all. The ini key is the base name plus the period
suffix, e.g. `FireCurveInteriorNight`.

Independent confirmation: a 08-23 06:00 in-game "Save & Apply" appended
`FireCurveDawn..FireCurveInteriorNight=2.0` to `SoulFog.ini` (the weather active
at the time) - the game writes the prefixed names too.

Side effect of the same mismatch: Soul Core's `IntensityDawn=1.1 .. IntensityDay
=1.6` are also dead, so fire intensity runs at the 1.0 default in every slot.
NOT changed - left for the user to decide.

Also note this build DOES write weather preset inis on Save & Apply (SoulFog.ini
08-23 06:00), which the 08-22 "left column never reaches disk" finding said it
could not. `enbseries.ini` is still only written by hand.

### Applied on disk 2026-08-23

`FireCurveDawn Sunrise Day Sunset Dusk Night InteriorDay InteriorNight = 2.0`
added to `enbseries.ini` + all 21 weather preset inis (22 files, 168 lines added;
SoulFog.ini already had all 8 from the in-game save).

CRLF and no-BOM preserved. The dead `Curve*` lines were left in place.
Backup: `_backups\2026-08-23 - E11 FireCurve key fix\`.
