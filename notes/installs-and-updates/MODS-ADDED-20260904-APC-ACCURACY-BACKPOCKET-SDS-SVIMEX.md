# Mods updated / added 2026-09-04

Selected profile at the time: **DEEZ CS NUTZ - PBR**. All six profiles were written. MO2 was closed for every write.

## Backups taken first

| What | Where |
| --- | --- |
| Accurate Projectile Collision 2.0.0 (whole folder) | `_backups\2026-09-04 - APC 2.0.0 pre-2.0.1` (4 files) |
| Accuracy 1.0.0 (whole folder) | `_backups\2026-09-04 - Accuracy 1.0.0 pre-1.0.1` (16 files) |
| Back Pocket 0.2.0 (whole folder) | `_backups\2026-09-04 - BackPocket 0.2.0 pre-0.2.2` (6 files) |
| Simple Diving 1.0.3 (whole folder) | `_backups\2026-09-04 - Simple Diving 1.0.3 pre-1.0.4` (12 files) |
| All six profiles: `modlist.txt`, `plugins.txt`, `loadorder.txt`, `plugingroups.txt` | suffix `.bak-svimex-20260904` |
| Outfit Wheeler live JSON | `_backups\PrismaOutfitWheel.json.bak-20260904-164147` |
| Outfit Wheeler known-good snapshot (77 items) | `_backups\outfits.known-good.json.bak-20260904` |
| Wheeler helper script | `_tools\outfit-wheeler\add_keepers.py.bak-20260904` |

Every folder backup was verified by file count and byte total. Every profile backup was verified byte for byte.

---

## 1. Accurate Projectile Collision 2.0.0 -> 2.0.1

**Updated in place.** Folder `Accurate Projectile Collision`, unchanged position.

- Changelog: CommonLibSSE-NG bump for game versions 1.7.99 and up, plus a build-system refactor. No gameplay change.
- Only the DLL changed. The ini in the archive is byte-identical to the installed one.
- 2.0.0 shipped a 36 MB debug symbol file (.pdb). 2.0.1 does not ship one. The stale 2.0.0 symbol file was removed. It is in the backup.
- Manifest check after install: version 2.0.1, Address Library build, loads on any supported runtime.
- meta.ini: version 2.0.1, new archive name, file id 799399.

## 2. Accuracy (Localized Combat Damage) 1.0.0 -> 1.0.1

**Updated in place.** Folder `Accuracy (Localized Combat Damage)`, unchanged position.

- Changelog: same CommonLibSSE-NG bump and refactor as APC. No gameplay change.
- Only the DLL changed. All 12 CIF JSON files are byte-identical to the installed ones.
- The shipped `Accuracy.ini` differs from ours in exactly two lines: our `bEnableFeatures = true` under `[LocalizedDamage:Humanoid]` and `[LocalizedDamage:Creature]` (set 2026-08-18). The installed ini was kept, so both flips survive.
- The stale 1.0.0 symbol file was removed (in the backup). 1.0.1 ships none.
- Manifest check: version 1.0.1, Address Library build.
- meta.ini: version 1.0.1, new archive name, file id 799404.

## 3. Back Pocket 0.2.0 -> 0.2.2

**Updated in place.** Folder `Back Pocket`, unchanged position.

- 0.2.1: switching between the back pocket and a follower or container menu now reselects the Misc tab in the follower's inventory.
- 0.2.2: pocketed enchanted items are hidden from the Disenchant list. Pocketed unenchanted items can still be enchanted. Default on.
- DLL and ini changed. The ini gained a `[menus]` section with `hide_pocketed_from_disenchanting=true`. Our ini had no custom values, so the new ini was installed as shipped.
- The category icon is byte-identical. The LICENSE and third-party notice files from 0.2.0 are still in the folder (0.2.2 does not ship them; harmless).
- Manifest check: version 0.2.2, locked to game runtimes 1.5.97 and 1.6.1170. The game exe here is 1.6.1170, so it loads. The 0.2.0 build was the same 1.6.1170 line.
- meta.ini: version 0.2.2, new archive name, file id 798275.

## 4. Simple Diving System 1.0.3 -> 1.0.4

**Updated in place.** Folder `Simple Diving - Modder Resource Only`, unchanged position.

- The installed base is the optional "Modder Resource Only" file 1.0.3-NoAnims. The 1.0.4 file is an "install over the main file" update containing only the DLL and its symbol file. It supports 1.5.97 through 1.7.104.
- DLL and symbol file replaced. The two Pandora patches (`sds1p`, `sds3p`) and the Behavior Data Injector JSON are untouched. Both patches are in the current Pandora output.
- Manifest check: version 1.0.4, Address Library build.
- meta.ini: version 1.0.4, archive name of the update, and both file ids listed (704391 base, 798335 update).

## 5. Swimming Extensions (Svimex) 1.0.0 - NEW

**Installed and enabled in all six profiles, but dormant.** See the caveat below.

What it is: procedural body and hand turning while swimming, sprint swimming, swim-enter animations (from ground and from a fall), and the missing first-person directional swim animations. Same author as Simple Diving, and recommended alongside it.

### Placement

| File | Where | Neighbour |
| --- | --- | --- |
| Mod folder `Swimming Extensions (Svimex)` | all six `modlist.txt` | the line after `+Simple Diving - Modder Resource Only` (shown directly above it in MO2) |
| `SwimmingExtensions.esp` (ESL-flagged, form 44) | all six `plugins.txt` and `loadorder.txt` | right after `SkyParkour.esp` |
| Group | all six `plugingroups.txt` | `-- Animations --` |

Each of the 24 profile files gained exactly one line. Line endings preserved per file (the PBR `plugins.txt` is the game-owned LF file and stayed LF). The modlist head block and the load-order tail from the Synthesis outputs down are identical to the backups in every profile.

### What the plugin does

Fourteen overrides of vanilla records, all of them the sprint "breath" dialogue (two topics, twelve responses). Each response gains an `IsSwimming == 0` condition, so the sprint breathing lines do not fire while sprint-swimming. Dawnguard's race condition on those records is carried forward. Only Skyrim.esm and Dawnguard.esm touch these records, so the plugin wins them at any position. Error sweep: clean. The optional "PCHT Patch" file on Nexus does the same for PC Head Tracking's breathing sounds and was not installed.

### Loose files

Eleven animation files and one Pandora patch (`Nemesis_Engine\mod\svimex`). No other installed mod ships any of the eleven paths. Dynamic Female Swimming Idles, No More Swimming In Air and Stronger Swimming Animations use different files and are not overridden.

### The caveat: dormant, and the archive is short

Two facts, stated once:

1. Ten of the eleven animation files are new names (sprint swim, swim enter, first-person directions). Nothing references them until the Pandora engine has run with the `svimex` patch ticked. The one file that replaces a vanilla animation directly, the first-person swim idle, is live now. The dialogue plugin is live now.
2. The 1.0.0 archive you downloaded is missing files. The author published **1.0.1** the same day (file id 800258, 0.36 MB) with the changelog "I forgot to upload the animation caches, added now. Please re-run Nemesis / Pandora", plus a separate main file **"Svimex Pandora Cache"** (file id 800259, 432 bytes) marked "Mandatory for Pandora, install below the mod file". That cache file is the same kind of thing as `HorsePower - Pandora Cache` and `SkyParkour - Pandora Patch`. Your 1.0.0 file is now listed as an old version on Nexus.

So the folder, placement and plugin are done, and the mod does nothing new in game yet. When 1.0.1 and the cache file are handed over they get overlaid into the same folder; the plugin and profile placement do not change.

The `svimex` patch edits the same swimming behaviour nodes as Simple Diving's patches. That is by design (same author, recommended together); Pandora merges them.

---

## Outfit Wheeler check after the plugin insert

Adding a light plugin shifts the light index of every light plugin after it. The Wheeler helper crashed on the current JSON: the 3.0 build has rewritten the file into its new shape (`actors -> 0x00000007 -> profile -> wheels`). The helper was given a small shim that reads both shapes; the old script is backed up beside it.

Result: calibrate 86 match / 0 mismatch before and after, reindex rewrote 0 entries, and the live JSON is byte-identical to its backup. Every outfit item comes from a plugin that loads before `SwimmingExtensions.esp`, so nothing moved. The known-good snapshot was refreshed to the current 12 outfits / 86 items (the old 77-item snapshot is in the backups).

## Plugin census

Full slots unchanged in every profile: Main 199, NSFW 208, DEEEZ 232, CS 240, PBR 242, PICTA 243 of 254. Light plugins +1 in each.

## Archives filed

Moved from `Downloads` to `D:\1. MOD STUFF\1. SKYRIM FILES`: APC and Accuracy into `gameplay and quests`, Back Pocket into `ui`, SDS Update and Svimex into `animation`. Older versions left in place.
