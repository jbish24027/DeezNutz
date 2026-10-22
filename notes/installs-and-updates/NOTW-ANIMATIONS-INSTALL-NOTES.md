# Nature of the Wild Lands - Animations Addon (Nexus 148132)

Installed 2026-08-18. Both files the user supplied are the current ones on the page.
The plugins file is older than the meshes file by design; the author has not reuploaded it.

## What went in

Two MO2 mods, not one:

| Mod folder | Contents | Source archive |
|---|---|---|
| `Nature of the Wild Lands - Animations Addon - Plugin` | `Nature of the Wild Lands - Animation Plugin.esp` | `NotW Animation - PLUGINS (FOMOD)-148132-1-03-1758872431.7z` |
| `Nature of the Wild Lands - Animations Addon - Meshes` | 721 animated tree meshes | `Nature of the Wild Lands - Animations MESHES-148132-1-04-1769870167.7z` |

Split deliberately. The mod page says the meshes must be disabled when running
DynDOLOD/TexGen while the plugin may stay enabled. Two mods makes that one checkbox.

## FOMOD choices

Step 1 - Wind Strength (SelectExactlyOne): **Normal** ("Author's preference").
Step 2 - Autumn Rift (SelectAtMostOne): **none**.
Step 2 - Autumn Tundra (SelectAtMostOne): **none**.

The two Autumn plugins master `NotWL - Autumn Rift.esp` and `NotWL - Autumn Tundra.esp`.
Neither exists anywhere in `mods/`, so both optionals would have been broken masters.

All three sway variants (plus their Autumn plugins) are kept unpacked at
`_tools/mod-install-helpers/notw-animation-sway-variants/`.
Swapping sway = copy one ESP over the one in the Plugin mod folder. Nothing else changes;
all three ESPs are byte-identical apart from the wind values.

## What the plugin actually does

- ESL-flagged already (record flags 0x200). Costs no full plugin slot.
- Masters: Skyrim.esm, Dawnguard.esm, Dragonborn.esm, Nature of the Wild Lands.esp.
- 725 records: 720 TREE + 5 STAT.
- Every one is an override of a record Nature of the Wild Lands.esp already defines.
  No new records.
- On the TREE records it changes **only the CNAM block** - trunk flexibility, branch
  flexibility and the eight wind-simulation floats. Verified: `MODL` is byte-identical on
  all 720, no VMAD is added or removed, nothing else differs.
- The 5 STAT records (Solstheim ash pines) differ only in a junk denormal float in DNAM
  being normalised to 0.0. Effectively ITMs.

Typical delta (`whiterun_temple_tree01_summer`):

```
NotW : trunk 1.0  branch 1.0   wind 0.04 0.03 0.04 0.034 0.5  0.5  0.4  1.0
anim : trunk 0.0  branch 2.407 wind 0.0  0.135 0.18 0.153 2.25 2.25 1.8 1.0
```

## Plugin position - and why it is early

`Nature of the Wild Lands - Animation Plugin.esp` loads **directly after
Nature of the Wild Lands.esp**, not at the end of the tree block.

This is deliberate. Four plugins already beat NotW on TREE records, and because the
animation plugin carries whole NotW records, loading it late would revert all of them:

| Plugin | Records | What it would have lost |
|---|---|---|
| `Aspens Ablaze.esp` | 6 aspens | Points MODL back at vanilla `TreeAspen04.nif` and zeroes flexibility. A late animation plugin restores NotW's aspen meshes and **silently undoes Aspens Ablaze.** |
| `Authoria - Output - Synthesis Worldspace.esp` | 6 shrubs/plants | Adds the `critterspawn` script (VMAD). A late animation plugin **strips the script.** |
| `Authoria - Seasons - City Trees.esp` | 2 ferns | User's own seasonal fern overrides. |
| `Authoria - Patch - Requiem - NOTWL.esp` | 1 juniper | Not in the animation plugin at all - no interaction either way. |

Verified after install (houseCARL, profile DEEZ CS NUTZ):

```
720 TREE matches, grouped by winner
  Nature of the Wild Lands - Animation Plugin.esp = 706
  Aspens Ablaze.esp                              = 6
  Authoria - Output - Synthesis Worldspace.esp    = 6
  Authoria - Seasons - City Trees.esp            = 2
```

Cost of the early slot: 5 small plants (young pine x2, nettle, tundra shrub, young conifer)
keep NotW's stock wind values while using an animated mesh, so they may over-sway.
Aspens are unaffected - Aspens Ablaze's `TreeAspen04.nif` is not in the animations addon,
so there is no animated mesh there to over-sway. The 5 plants resolve on the next
Synthesis run, which forwards the new winner and re-adds critterspawn.
**Do not hand-edit the Synthesis output** to fix them.

## Mesh position

```
Authoria - PG Output                                      (priority 36)
  ...
Nature of the Wild Lands - Animations Addon - Plugin       (3043)
Nature of the Wild Lands - Animations Addon - Meshes       (3044)
Nature of the Wild Lands - Snowier Spruce Trees            (3045)
Nature of the Wild Lands - 3D hybrid LODs and regions      (3046)
Nature of the Wild Lands - forest and trees improvement    (3047)
```
(DEEZ CS NUTZ line numbers; the other three profiles differ only by offset.)

### ParallaxGen buries most of this

`Authoria - PG Output` already carries **643 of the 721** animated mesh names and sits far
above them. Confirmed by VFS resolution - PG Output wins every one.

- 78 of 721 trees animate immediately.
- 643 do not, until **ParallaxGen is re-run** with the Meshes mod enabled.

Do not "fix" this by moving the Meshes mod above PG Output. That is not a stable state:
ParallaxGen reads the VFS winner, so on its next run it would read the animated meshes,
process them, and write an output that the animations mod then buries again.

### Snowier Spruce Trees overlap

NotW 3.14's spruce TREE records point at `spruce_*_winter.nif`, but the mod only ships
`spruce_*_winterL.nif`. `Nature of the Wild Lands - Snowier Spruce Trees` is currently the
only provider of those 14 winter spruce meshes. The animations addon ships all 14 too, and
now wins them.

Comparing the meshes:

| | diffuse | normal |
|---|---|---|
| Snowier Spruce | `spruce03_winter.dds` | `spruce03_winter_n.dds` |
| Animations addon | `spruce03_winter.dds` | `spruce03_summer_n.dds` |

Snowier Spruce also replaces the diffuse texture at its own path, and textures resolve
separately from meshes, so **the snowier diffuse survives**. Only the snowier normal map is
lost on those 14 trees.

Proper fix: mod 149165 has an optional file **`NOTWL - Snowier Spruce Trees - Animations
Addon`** (v0.1). Not currently installed. Install it above the Meshes mod.
Caveat: it is dated 2025-05-04, built against animations v1.0-1.02, so its meshes are two
versions behind. Alternative: repoint the normal map on those 14 meshes - one string per
file - which stays current with v1.04.

## LODs

No DynDOLOD or TexGen re-run needed. The plugin changes no model paths and adds no records,
so existing LODs stay valid. The author calls this case plug & play.

For any future LOD run: **disable the Meshes mod, keep the Plugin mod enabled.**

## Files changed

All 4 profiles - `Authoria - Requiem Reforged - Main Profile`,
`Authoria - Requiem Reforged - NSFW Profile`, `DEEEZ NUTTZZZ`, `DEEZ CS NUTZ`:

- `modlist.txt` - two mods inserted above Snowier Spruce Trees
- `plugins.txt` - plugin enabled, directly after Nature of the Wild Lands.esp
- `loadorder.txt` - same position
- `plugingroups.txt` - added alphabetically under group `Visuals - Seasons and Landscape`

Backups: `*.bak-notwanim-20260818` in each profile folder.
