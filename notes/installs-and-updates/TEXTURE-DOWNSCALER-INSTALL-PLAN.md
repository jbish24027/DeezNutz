# Texture Downscaler 2.4.0 — install plan

Date: 2026-08-27
Archive: `Texture Downscaler 187049 2.4.0 2026-08-22T22-52Z Ks18n0wVk.zip` (Downloads)
Nexus: mod 187049, file 793592, main, 2026-08-22
Cap: **4096**, with two targeted exceptions at 2048 (overlays, normal maps)
Status: PLAN ONLY — nothing written yet

---

## 1. What it does

It is an SKSE DLL. It hooks texture creation and skips the largest mip levels.

An 8192 texture asked to load at 4096 uses about a quarter of the video memory, and
takes about a quarter of the upload time.

Your texture files are never touched. Uninstalling restores full resolution instantly.

There is no plugin, no script, and no co-save data. It costs nothing against the 254 cap.

## 2. Compatibility checks — all clean

1. Game is 1.6.1170. Address Library has the matching file. The DLL is version-independent.
2. SKSE Menu Framework 3.0.0 is installed and enabled in all five profiles. The menu will work.
3. The DLL is a release build. No debug runtime, so no missing-dependency failure.
4. It does not import Direct3D directly and does not touch meshes. ParallaxGen is unaffected.
5. Not an input to Reqtificator, Synthesis, DynDOLOD or TexGen. Nothing needs re-running.
6. No mod in the list ships a file of the same name. Nothing to conflict with.
7. VRAMr is installed but has never been run — no output mod exists. No double downscale.

Two things worth knowing, neither a blocker:

- The mod is 26 days old with 12 releases in that time. It is moving fast.
- The author tags it as AI-assisted. The binary itself checks out clean.

## 3. Census — the whole picture

I read the DDS header of every loose texture over 7 MB in the enabled mods for this profile.
204,859 loose textures in total, 263 GB.

True resolutions:

| Resolution | Files | On disk |
|---|---|---|
| 8192 | 161 | 11.1 GB |
| 4096 | 4,549 | 84.8 GB |
| 2048 | 593 | 9.4 GB |
| everything else | ~199,500 | ~157 GB |

At a 4096 cap, only the top row is in play. **163 files, 11.2 GB.** Nothing else in your
build is touched at all.

## 4. The one thing that decides this

The shipped presets exempt skin, faces, armour, clothes and grass by folder name. Those
exemptions exist to protect those things from a 2048 cap. At a 4096 cap they protect
nothing — and they happen to cover almost every 8K file you own.

- Quality preset + 4096 cap: **28 files affected, 2.2 GB.** Effectively a no-op.
- Structural exemptions only + 4096 cap: **125 files affected, 9.6 GB.** The real version.

So the folder rules have to be cut down, or the mod sits there doing nothing.

Where your 8K actually lives:

| Group | Files | On disk | Verdict |
|---|---|---|---|
| RaceMenu overlays | 70 | 5.83 GB | cap it — over half your 8K, and an overlay is a blend layer |
| DynDOLOD LOD atlases | 22 | 1.02 GB | **keep exempt** — reducing an atlas blurs everything packed in it |
| a dragon replacer | 8 | 0.67 GB | cap it |
| UBE body | 8 | 0.67 GB | cap it |
| one jewellery set | 12 | 1.00 GB | cap it — 8K on earrings and a pendant |
| grass | 9 | 0.33 GB | cap it — a mip change, colour is untouched |
| a creature pack | 4 | 0.33 GB | cap it |
| terrain heightmaps, sky, UI | 38 | 1.6 GB | **keep exempt** — and most have no mips, so the plugin skips them anyway |
| assorted small sets | ~12 | 0.5 GB | cap it |

No face tint in your build is 8K, so dropping that exemption changes nothing.
Same for parallax and material data — you have 503 and 3 files, none above 4096.

## 5. The ini

A 4096 cap everywhere, except normal maps and RaceMenu overlays which go to 2048
(reasoning in section 6b). Folder rules cut to the structural ones only — atlases,
heightmaps and UI, which are the only textures where reducing is technically wrong
rather than merely a matter of taste.

```
[General]
Enabled=1
LogLevel=2
TrackUsedFolders=1

[Textures]
Diffuse=4096
Normal=2048
Parallax=4096
Material=4096
Glow=4096
Mask=4096

[Folders]
_shell=0
\interface\=0
\terrain\=0
\lod\=0
\dyndolod\=0
\lodgen\=0
\tintmasks\=0
\sky\=0
\overlays\=2048
```

Nine folder rules instead of the preset's twenty-eight, and every one of them earns
its place. Folder tracking is on so the first session gives real numbers.

Note on ordering: folder rules beat type limits, and the first match wins reading down.
The overlays line is last so the structural exemptions above it stay at full size.

## 6. What to expect

This is a surgical change. About 125 textures load at a quarter of their size.

An 8K texture with mips costs roughly 89 MB resident; at 4K it is roughly 22 MB.

On a 32 GB card the memory saved is not pressure relief — you have no pressure. The
benefit is the upload. Loading an 89 MB texture is a hitch; loading a 22 MB one is much
less of one. That is what this buys, and it is real but modest.

It is also the safest configuration available. Nothing below 8K changes in any way.

See section 6b for the two 2048 exceptions, which is where most of the actual gain comes from.

## 6b. The two things dropped to 2048

I read the header of every 4096 texture as well: 4,549 files, 84.8 GB. Two blocks stand out
as safe to halve, for different reasons.

**RaceMenu overlays — 1,619 files at 4K plus 70 at 8K, about 38 GB.**

This is the largest single block of textures in your entire build, larger than skin, armour
and world textures combined. Every one of them is a diffuse blend layer — dirt, blood,
scars, warpaint, tattoos — composited onto skin at partial opacity. That is the one kind of
texture where resolution matters least, because it is never the surface you are actually
reading. They also cost per actor, so they are exactly what spikes when you walk into a
crowd of overlaid NPCs. Halving them takes an applied overlay from roughly 21 MB resident
to roughly 5 MB.

One honest caveat: fine tattoo linework is the one overlay type where 2K could show in a
close-up. If you do character shots, look at that first. It is a one-line change in the
in-game menu with no restart.

**Normal maps — 710 files at 4K, 13.9 GB.**

Normals survive halving better than any other map type. They encode surface direction, not
detail you read directly, and they get mip-filtered hard anyway. This one is spread across
everything — modded gear packs, skin, armour, architecture — so it is not a spike fix, it
lowers the baseline for whatever is on screen at any moment.

Between them: overlays cut the crowd spike, normals cut the floor.

### Correction to the earlier draft

I previously called NPC face tints the biggest crowd win. That was wrong, and it came from
judging by file size instead of reading the headers.

Only 23 face tints in your build are actually 4096. The rest are already 2048 — they are
just large on disk because they are stored uncompressed. Capping face tints at 2048 would
do nothing. Dropped from the plan.

### Deliberately left at 4096

- Diffuse on skin, gear and world surfaces. That is what you actually look at.
- Masks (316 files, 5.3 GB). Safe to halve on the same logic as normals if you want a third
  lever later, but the return is smaller. Not doing it now.

## 7. Install steps

Preconditions: MO2 closed. It is closed now.

1. Back up the five `modlist.txt` files.
2. Create `mods\Texture Downscaler` by hand from the archive. Skip the FOMOD — it only
   picks which of four ini files to copy, and none of them is the one we want.
   - DLL and PDB go in. Keep the PDB; it makes crash logs readable if this DLL is ever
     named in one. 22 MB on disk, nothing at runtime.
   - Write the ini from section 5.
   - Write a `meta.ini` with mod id 187049, file 793592, version 2.4.0, so update checks see it.
3. Insert `+Texture Downscaler` directly above `+VRAMr` in every profile's `modlist.txt`.
   - That is inside the Essential - Utilities group, next to the other memory tool.
   - It must go into all five profiles even if you play one. A mod folder missing from a
     profile gets inserted at the top on next MO2 start, which would put it above the
     flat maps and outputs block.
   - Files stay CRLF.
4. No plugin to place. No load order change. No group file to touch.

## 8. Verifying it worked

1. Start a session. The in-game menu gets a Texture Downscaler entry.
2. If the entry is missing, the DLL did not load — check the SKSE log.
3. Open the folder browser to confirm it is seeing your folders and counting loads.
4. Watch for anything soft up close. Raise that folder's limit in the menu and it applies
   immediately to anything loaded from that point on.

One thing to watch: the in-game menu writes settings back to the ini. Under MO2 that write
can land in Overwrite instead of the mod folder. Check Overwrite after the first session
and move the file into the mod if it turns up there.

## 9. Rollback

Uncheck the mod in MO2. That is the whole rollback.

Safe mid-playthrough. No save data, no scripts. Full resolution returns on the next load.

## 10. Do not

- Do not run VRAMr as well. It bakes a downscaled copy of all 263 GB to disk. This does the
  same job at runtime, for free and reversibly. Running both would downscale twice.
- Do not keep the preset folder rules. At a 4096 cap they cancel out almost the entire effect.
