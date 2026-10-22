# Batch add/update - 2026-09-03

Nine archives handed over. Two were updates. Seven were new mods (one of them your own Padborn package).
MO2 and the game were closed the whole time. Every archive verified against Nexus at file level (exact file IDs + byte sizes).

Backups: `_backups\2026-09-03 - batch add-update\` (whole MFO and Sonders folders, plus the three firepit
meshes I removed from the generator outputs). Profile files: `*.bak-batch-20260903` in all six profiles.
Outfit Wheeler JSON: `_backups\PrismaOutfitWheel.json.bak-20260903-045209`.

An independent three-lens adversarial review (file layer / records / runtime) ran against the plan before any
write. It found no blockers; its two should-fix items are folded in below (Padborn dodge ini booleans, MFO
settings-layer decision).

---

## Updated in place (2)

| Mod | From -> to | What actually changed |
|---|---|---|
| Sonder's Raysense Wall Leaning | 1.0 -> 1.1 | Only the 9 OAR `config.json` files. They add RaySense "ledge" and "obstacle" checks so the lean no longer fires against workbenches and similar spots. All 32 animations byte-identical. Needs RaySense 1.2.0 (installed 08-28) and OAR 3.2.0 (installed). |
| marth Follower Overhaul (MFO) | 1.0.66 -> 1.1.4 | New DLL, plugin, trade script and settings. Faster looting, no more followers freezing next to unreachable corpses, summoners stop re-summoning, clean records for xEdit. **1.1.3 added a per-follower on/off checkbox on the board's Followers tab** - the per-NPC exclusion that did not exist on 08-27. Plugin lost one keyword (the add-on manifest moved to the Progression add-on, which is not installed); nothing referenced it. |

MFO settings: the 08-27 hands-off posture is carried over in both ini layers (`bLogistics=0 bEconomy=0
bAutoRetreat=0 bMagicLoadout=0 bDollsMode=1 bCommandTarget=0 iCastControl=0`, focus key `[` = 26).
New in 1.1.x and set OFF for the same reason: `bHmsRedistribute=0` (would reshape followers' health/magicka/
stamina growth per class). Adopted upstream's new defaults `fRapportRate 2.0` and `fBatchLinger 1.5`.
Six 1.0.66-era keys that upstream dropped from the MCM layer were not re-added (four keep their SKSE-ini
defaults; `fLooseAcquireDist`/`fMeleeReach` fall back to the 1.1.4 DLL defaults, which is the "reach loot from
where you stand" change). The 495 KB Synthesis item catalog was kept (schema 1, same as the new DLL reads);
the archive's 1.4 KB fallback was not installed. Settings file written without BOM. The Synthesis patcher
pin is untouched; nothing to regenerate.
Follow-up for me after your first session: read `MFO.log` for `[hms]` lines - a "fixed-stat grant" line would
mean a unique follower's stats were still touched and the posture needs a second look.

## New (7)

**High Quality Hearth - 3D Farmhouse Firepit 1.1** (mesh + 17 textures, no plugin) - the triple-checked one.
- Record layer: the firepit STAT is touched by no mod, so the replacer applies to every vanilla placement,
  including the Dawnguard/Seasons "snow" variants (same mesh, projected snow material).
- File layer: the only other copies were Embers XD's (differs from vanilla just in the ash texture) and the
  ParallaxGen'd versions of that Embers mesh in both PG outputs plus the PBR revert mod. Those three
  generator-derived copies sit in the outputs head block and would have hidden the new hearth, so they were
  removed (backed up), same as the WiZkiD signs on 08-28. The hearth mod sits directly above the Embers block
  in every profile and now wins in all six; the two PG `ParallaxGen_Diff.json` manifests still list the mesh -
  expected and harmless.
- Mesh: self-contained (own collision, own textures, no parallax/PBR flags, no Light Placer or particle-light
  hook references this model), vanilla shape and scale. Author states Embers XD compatibility; confirmed.
- Two placed firepits use Embers' own separate "Base" mesh (COTN Dawnstar and Kynesgrove Embers patches) and
  keep the old look. Everything else gets the new one.

**The Mists of Blackreach 1.2 + Lux Patch 1** (two ESL plugins)
- Replaces the 20 big steam emitters in Blackreach with a volumetric fog mesh and adds 16 new fog spots. Lux's
  master ESM currently owns those 20 refs (and one is owned by Gleamstrike); the Lux patch loads right after
  `Lux - No grass in caves patch.esp` and is the final winner for all of them in every profile, forwarding Lux's
  emittance colour. One vanilla emitter the mod also lists is untouched by anything.
- The worldspace and persistent-cell container records lose to the FWMF map patch / DynDOLOD.esp as usual
  (in DEEZ CS NUTZ, which has no DynDOLOD.esp, the Lux patch ends the chain with the same net data).
- Ships a DynDOLOD exclusion ini for the fog mesh; it is inert until someone runs DynDOLOD.
- Plugins: `FS_BlackreachGrass.esp` then `FS_BlackreachMists.esp` at the end of "Visuals - Misc Worldspace"
  (see the group tidy below); the Lux patch in Lighting - Lux Patches. Mod folders sit together directly above
  "Blackreach Bush - FOMOD". Particle budget (`iMaxDesired 7500`) is fine.

**Grassreach 1.2** (one ESL plugin) - **installed, correctly placed, but dormant**
- Its grass grows only where its three new land textures are painted, and that painting lives in 78
  landscape records. 50 of those are overridden by `Authoria - Output - Synthesis Worldspace.esp`, 10 by
  Northern Roads (a real terrain conflict - Northern Roads raises the ground there by up to 136 units, so
  those ten would need a merged landscape record, not just a re-run), and 18 are untouched vanilla. In the
  10 untouched-but-painted cells Grassreach is live right now: the terrain looks identical (its textures
  reuse vanilla's cave-dirt texture set, heights are vanilla).
- On top of that the list runs grass from cache only (`Only-load-from-cache=true`), and Blackreach's nine
  cache files per season predate this mod, so no new grass can appear anywhere until the worldspace output
  and then the Blackreach grass cache are regenerated. Those are generator runs and are yours to raise; nothing
  is scheduled. Enabled so it is picked up automatically if that ever happens. Requires CS grass lighting
  (present on the CS profiles).

**SkyParkour V3 - Zodd's RL Step Low And High 1** (4 animation files, no plugin)
- Plain replacement of SkyParkour v3's third-person step-up clips. v3's behaviour binds those exact files, so no
  Pandora/Nemesis re-run is involved. First-person step clips stay SkyParkour's (Zodd ships none).
- "SkyParkour - JellyFishInLoop animations" replaces steps through the old v2 lever-pull OAR path, which
  v3.5.4 no longer plays, so it cannot shadow these. Left as is.
- Sits directly above JellyFish (top of the SkyParkour cluster), enabled in all six.

**UBE Yuki-ra Face Preset 2** (RaceMenu preset + sculpt, no plugin)
- Directly above Anita in the RaceMenu presets block, enabled in all six.
- Missing from this build: Zhizhen Brows and the Tullius Eyes pack (both referenced by the preset), plus the
  Veilguard overlays and MO Skin the author lists. The preset loads; brows/eyes fall back and some makeup
  layers will not render. Same situation as Anita's horns.

**Authoria - Padborn 3.0.0** (your controller package; loose files + Padborn.dll, no plugin)
- Installed with the archive's recommended answers: **Hold B = Sprint (CCS LAYOUT 402)** and **sprint rescue
  Off**. Layout 402 = CCS author's own binary + text controlmaps (byte-identical to the CCS 5.3.5 archive),
  differing from your current 406 in exactly three rows: Sprint = hold B, Sneak = L3 click, Auto-Move = B+L3.
  Your F2 quickload was merged into the text controlmap, so that survives.
- Placed directly above "Authoria - Controller Configs", the highest-priority file it must beat. Enabled in
  DEEZ CS NUTZ, DEEZ CS NUTZ - PBR, DEEEZ NUTTZZZ and PICTA; listed disabled in both Requiem Reforged profiles
  (their whole controller block is disabled). It now wins every file it ships: gpp_keyhandler.pex, StancesNG.toml,
  TK Dodge RE.ini, TKDodgeAddon.ini (MCM Settings + Config), StyyTKDodgeMCM.pex, both controlmaps, the MCM pictures.
- Review fix applied: Layout 402's `MCM\Settings\TKDodgeAddon.ini` shipped its booleans as `true/false` with
  mixed line endings; every other MCM Helper ini here uses `1/0`, and the README itself says the word spelling
  read false on this list (which would have silently switched the Requiem dodge perk lock off). Rewritten as
  `iDodgeKey=-1, bEnableSprintDodge=1, bUseMCORecovery=1, bUsePercentages=0, bUsePerkLock=1`, CRLF, no BOM.
- Also in the 402 dodge setup (README design): `EnableDodgeInPlace=false` (a stationary tap no longer dodges)
  and `SprintingPressDuration=0.25`. Set the first back to true in `SKSE\Plugins\TK Dodge RE.ini` inside the
  mod if you want in-place dodges.
- Cosmetic: the DLL's log banner says "Padborn 2.0.0"; the CCS MCM combo picture (CI.dds) is CCS's 37c.dds,
  which may or may not be the one CCS assigns to 402 - swap for 42c.dds if it looks wrong.
- Side effect: StancesNG wolf key moves from `[` back to `x`, which ends the latent collision with MFO's focus
  key `[` (inert anyway while Commanded targeting is off).
- The archive stays in your Downloads; the README wants it kept outside the instance for reinstalls.

---

## Where things landed (neighbour names, same in all six profiles)

- High Quality Hearth: directly above "Embers XD (Less Poly)".
- Grassreach, Mists Lux Patch, Mists of Blackreach: directly above "Blackreach Bush - FOMOD", in that order.
- UBE Yuki-ra Face Preset: directly above "Anita - UBE Face Preset".
- SkyParkour Zodd steps: directly above "SkyParkour - JellyFishInLoop animations".
- Authoria - Padborn: directly above "Authoria - Controller Configs".
- Plugins: `FS_BlackreachGrass.esp`, `FS_BlackreachMists.esp` at the end of "Visuals - Misc Worldspace" (after
  `Ash Nomad - Campfire Addon.esp`, moved there in the group tidy below); `FS_BlackreachMists_LuxPatch.esp` after
  `Lux - No grass in caves patch.esp`. All three ESL-flagged.

Head block (through the LOD Outputs separator) and the tail from the Synthesis outputs down are unchanged in
every profile. All four profile files stayed CRLF; every change is a pure insert.

Plugin cap unchanged: 199 / 208 / 232 / 240 / 242 / 243 of 254 (Main / NSFW / DEEEZ / CS / PBR / PICTA).
`housecarl_check_errors` on the three new plugins + MFO.esp: 0 dangling refs, 0 missing masters.
Outfit Wheeler reindexed for the three new light plugins: 75 entries rewritten, calibrate 77 match / 0 mismatch.
All eight Nexus archives copied into MO2's downloads folder with `.meta` files (mod + file IDs).

---

## Plugin-group tidy, same day (all six profiles)

You reported duplicated group headers in MO2's plugin pane. Measured from the profile files: the ten duplicated
headers existed in every backup back to 2026-08-28, so they predate this batch. Cause: a few plugins carry a
different group tag than the block they sit in, and MO2 opens a new header at every tag change.

One part was mine. I had put the two Blackreach plugins (today) and the three Imperial Mail plugins (08-28) next
to `Natural Waterfalls - Blackreach.esp`, inside the master-file block. MO2 enforces masters-first and slid them to
the head of the normal block on launch, where they sat mis-tagged "Master Files - Visuals". In-game order was
never affected (the engine loads masters first regardless), but the tags were wrong.

Done, with your go:
- Moved `FS_BlackreachGrass.esp` + `FS_BlackreachMists.esp` to the end of "Visuals - Misc Worldspace" (after
  `Ash Nomad - Campfire Addon.esp`) and the three Imperial Mail plugins to the end of "Quests and Newlands - Misc"
  (after `A new debt additional options.esp`). Winner check before moving: Imperial Mail's only shared record is the
  global navmesh map, still won by the late Authoria navmesh patch; the Blackreach plugins still load before every
  plugin that already beats them. Active flags preserved.
- Relabelled the wedge plugins to the block they sit in: the weather cluster (Dynamic Wind, Mists of Tamriel,
  Astralite + its two patches) and Vanilla PBR -> Seasons and Landscape; Immersive Encounters High Poly AIO ->
  Early Loaders; the two disabled leftovers (old PEM patch, Sacrilege master patch) -> Requiem n Tweaks; in the CS
  profile the two Vibrant weapons .esl -> Master Files - Visuals; in the Requiem Reforged profiles the ungrouped
  rows got the groups they carry in the CS profiles (RFTI, Late Custom Patches, Outputs) and Locked Chests Have
  Keys x3 -> DBM Patches; in PICTA the Picta/Helios weather rows follow the same scheme. 8 / 14 / 1 / 11 / 10 / 9
  relabels (Main / NSFW / DEEEZ / CS / PBR / PICTA). Labels only.
- Result: 56-57 headers per profile, 0 duplicates, 0 ungrouped rows. Plugin sets, every other plugin's relative
  order, all modlists, and the protected tail are unchanged. Backups `*.bak-groups-20260903`.
- Outfit Wheeler reindexed again (two light plugins moved): 77 rewritten, calibrate 77 / 0.

Rule learned: a plugin that is not a master (no ESM flag, .esp extension) must never be inserted into the master
block, even when the thematically nearest anchor lives there. MO2 relocates it on the next launch and the group
tag becomes a wedge.

---

## Blackreach grass, later the same day

You re-ran the Synthesis worldspace group and did the grass bake. State now:
- Grassreach's painting is live in 34 of its 68 cells. The other 34 are held by Northern Roads, which re-sculpts
  and re-paints Blackreach's terrain in those cells (heights, normals and textures all differ from vanilla), so its
  version wins there and the grass texture is not painted. Full coverage would need a three-way terrain merge
  patch from me, another worldspace run, and a second bake.
- Bake: driver `_tools\blackreach-grass\grass_regen_blackreach.py`, one pass, ~10 s. 37 Blackreach cells now
  hold grass (was 9), copied to all five cache mods (Blackreach has no seasons). 12 of Grassreach's 14 grass
  types are placed. One cell came out doubled in the same run; kept the later write. All 185 files parse clean.
  Old files and the doubled originals: `_backups6-09-03 - grass regen Blackreach\`. Both ini files restored
  byte-identical.

**Why the first look showed nothing.** The CRDW directory cache was rebuilt at the bake launch (06:15) while the
old Blackreach cache files were parked and the new ones did not exist yet, so the rebuilt Data/Grass walk listed no
Blackreach file. The collect step put the files back outside MO2's sight, the next launch loaded that walk, and NGIO
found no Blackreach cache at all. Fix: removed the stale grass walk file from the profile's CRDW cache folder (backed
up), which makes the plug-in rebuild at the next launch. Rule recorded: after any scripted loose-file change, drop the
matching CRDW cache file before handing off.

---

## Batch 2, same day: six more archives

Backups: `_backups/2026-09-03 - batch2 add-update/` (the three swap inis and the meta files that changed). Profile files
`*.bak-batch2-20260903`. No plugin was added, removed or moved, so no wheeler reindex was needed. Every archive
verified against Nexus at file level.

| Archive | Verdict | What changed |
|---|---|---|
| Canidae 2.24 -> 2.25 | nothing to install | All 56 installed files are byte-identical in 2.25. The only 2.25 change is the Dynamic Animal Variants dog add-on being ESL-flagged, an option you do not use (no DAV in the load order). Version stamped 2.25. |
| Cisterns of Skyrim 1.4.8 -> 1.4.11 | nothing to install | Your install is the meshes-and-textures-only choice (2K, no drips, 2D blood puddle, no distribution plugin). All 14 files identical in 1.4.11; the 1.4.9 to 1.4.11 changes are script and patch fixes for options you do not have. Version stamped 1.4.11. |
| Ash Nomad Tents 2.6 -> 2.7 | swap ini replaced | One new line: a Solstheim tent placement (a Dragonborn reference) now gets the Dunmer tent. Plugin, meshes and textures identical. The Dovahnique's Lanterns patch and the seasons patch are unaffected. |
| Publican's Perch 1.0.8 -> 1.0.9 | swap ini replaced (both folders) | Excludes the two Grey Quarter shops (Sadri's Used Wares, New Gnisis Cornerclub), which go back to vanilla counters. The author points at "Dunmeri Furniture in the Gray Quarter" for those; not installed. Meshes and textures identical (1.0.8 already carried the optimized meshes, so the separate Meshes Optimization Project folder is now redundant but harmless). The older 2k folder, which is the live one in the two Requiem Reforged profiles and DEEEZ, got the same ini. |
| Samples of Stools - HFs Buttocks Rest patch 1 | NEW, but inert | One swap ini that mixes the three "HFs - Buttocks rest" stool models into the hold variants. Those three models are base objects that only the BOS edition of HFs defines; your HFs is the standalone Version 2 replacer, so the referenced forms do not exist and Base Object Swapper skips them (it logs them as not found and keeps the hold variants). Installed directly above Samples of Stools with the same enabled state (on in the CS profiles, off where Samples is parked). It becomes live the moment "HFs - Buttocks rest (BOS)" is installed. |
| Bedroll Alternative - Alt - Quilted Blankets 1.1 | NEW | The quilted texture set for every Bedroll Alternative variant (mesh replacer, BOS colours, Campfire, Basic Camp Gear, CC Camping, Always With a Bedroll, Use Those Blankets colour variants). For your install only the vanilla-path bedroll mesh and its textures are live; the rest is inert. Textures are 4K (16 to 22 MB each). Placed directly above "Bedroll Alternative - UTB Patch", enabled in all six. No path overlap with the Ash Nomad, Fluffy Beds or Campfire bedroll files. |

Seen in passing, not touched: "Publican's Perch - BOS Bar and Counter Replacer" and "Samples of Stools" are listed
disabled at the very end of the modlist (lowest priority) in the two Requiem Reforged profiles, DEEEZ and PICTA,
and "Canidae - A Wolf Replacer" plus its Requiem patch are absent from the Requiem Reforged and DEEEZ modlists
entirely (MO2 will auto-add them at the top of the pane the next time one of those profiles is opened).

CRDW: the profile's directory cache is already flagged for a rebuild from the grass fix, so the new textures and
meshes are picked up at the next launch.

### Addendum: HFs - Buttocks rest (BOS) - 4K

Installed as "HFs - Buttocks rest (BOS) - 4K" (Nexus 146910, file 614349): light plugin `HFs_Buttocks_Rest_BOS.esp`
(3 furniture + 6 static variants, V1 round/V2 vanilla-style/V3 fancy), 9 meshes at their own paths, 17 4K textures
(22 MB each, about 375 MB) and its own swap ini. Placed directly above the standalone "HFs - Buttocks rest" in all six
profiles so its 4K copies of the five shared texture paths win; the standalone stays as the fallback mesh for any stool
nothing swaps. Plugin after the Samples of Stools plugin in the CS profiles, after the Publican's Perch plugin elsewhere
(group of the anchor). Check-errors clean. Wheeler reindexed (one light plugin added), calibrate 77/0.

How the two swap files interact, read from the swapper's source (Manager.cpp): a reference is resolved reference-swap
first, then location-filtered swaps, then plain swaps, and the first hit wins. The Samples of Stools HFs patch is
hold-filtered, so it owns every Skyrim hold and now mixes the three HFs stools into each hold's pool; HFs' own plain
swap only reaches stools no hold filter covers (Solstheim and the like). In the profiles where Samples is parked,
HFs' own swap randomises V1/V2/V3 everywhere. No entry is dropped any more; the earlier "not found" log lines are gone
with the plugin present.

---

## Blackreach grass, second look: where the grass is and why the landmarks are bare

You saw no grass after the bake and after the CRDW rebuild. Everything below comes from files, not guesses.

**What the cache and the engine agree on.** The engine's real plugin order is in the header of every save
(`_tools\save-forensics\save_plugins.py`, new). In the 05:55 save the light plugin `FS_BlackreachGrass.esp` sits at
index 7CA, and every grass FormID in the 37 Blackreach cache files is `FE7CAxxx`. So the bake is internally correct.
The 37 files win from "Authoria - Grass Cache - Default", the CRDW grass walk lists them, the Blackreach worldspace
carries no No-Grass flag (winner is the FWMF master patch: SmallWorld, NoSky), and Blackreach is outside the Seasons
whitelist, so the base file is what gets read.

**A shift happened, but it is not the cause.** Rovan's Market Stall (installed 06:53, plugins.txt line 427, light)
loads before every grass plugin and pushed each later light index up by one. NGIO's own log shows it: Seasonal
Landscapes' cliff forms are `0xfe470xxx` in the 06:22 session and `0xfe471xxx` at 07:08. Grassreach went 7CA to 7CB.
I checked whether that matters against the Tamriel cache: its July and August files name Seasonal Landscapes as
FE:3E8 and FE:457 and Witchy Wilderness as FE:3FE and FE:46D. Today those indices belong to Simple Snow Improvements,
SelectYourSeason, JS Instruments and The Gildergreen Grows, none of which has a grass record, and they had already
moved by 18 August when near grass was verified rendering correctly. Cached grass is resolved by the model path stored
next to the FormID, so the shift does not hide it. Rovan's plugin has no overrides and stays where it is.

**Why the landmarks are bare.** Grassreach adds no grass to vanilla textures. It defines its own land texture
`LCaveDirtBlackreachGrass` (12 grasses, same texture set as vanilla cave dirt) and paints it into its 78 land records.
Northern Roads re-sculpts 34 Blackreach cells and wins them through the Synthesis worldspace output; its layers are
vanilla `LCaveDirt`, `LDirt01/02`, rocks, mud and its Dwemer road texture, none with a grass list. Those 34 cells are the
places you arrive at:

| Place | Cell | Cached grass |
|---|---|---|
| Alftand lift (arrival) | (5,3) | empty file |
| Raldbthar lift | (2,0) | empty file |
| Mzinchaleft lift, Overpass | (-2,3), (-1,3) | none |
| Blackreach Origin, Silent City, sewer entrance | (0,0), (0,1), (1,1) | none |
| Towers, Fungus Field, Pump Station, Arena, Sinderion's shack | (2,2), (3,2), (2,3), (3,0), (4,4) | none |
| densest grass cells | (0,-3) 6685, (0,3) 2565, (5,2) 2491, (1,-1) 2166, (6,3) 2140, (-2,-2) 1911 | yes |
| Spider Lair | (0,4) 1418, (1,5) 792 | yes |

Total: 33,837 instances over 37 cells. (5,2) is the cell right next to the Alftand lift, one cliff over.

**Test.** Load the 05:55 save, open the console, type `cow Blackreach 0 -3`. Grass at your feet means the bake, the
walk and the loader are all fine and the bare spots are Northern Roads cells. No grass there would put the FormID
theory back on the table; the fix then is a re-bake once the plugin list is final (stage, Play, collect, finish; about
ten seconds of game time).

**Outcome (08:18).** You had been standing near the Silent City, a Northern Roads cell. After the teleport you found
grass and saved in it. That save's plugin list has Grassreach at light index 7CB while the cache files still say 7CA,
so the FormID shift is proven harmless: an ESL inserted before a grass plugin does not invalidate a grass cache.

**Fix for the landmark cells: BUILT 08:32, live in all six profiles.** New mod "Authoria - Patch - Grassreach
Northern Roads Land" (light plugin of the same name, 523 KB), built by `_tools\blackreach-grass\build_nr_land_patch.py`
and re-runnable if Northern Roads updates. It copies Northern Roads' 34 Blackreach land records byte-for-byte
(heights, normals, colours, every layer and alpha map, the Dwemer road) and changes only the texture link of the
cave-dirt layer, `025414:Skyrim.esm` (LCaveDirt) to `000800:FS_BlackreachGrass.esp` (LCaveDirtBlackreachGrass, same
texture set, 12 grasses): 122 layer entries across 34 cells, 522,364 other bytes proven identical. Masters Skyrim.esm,
FS_BlackreachGrass.esp, Lux.esp, Northern Roads.esp. Placed above the Rovan Requiem patch mod; plugin at the end of
"Authoria - Custom Patches" (after Redcap Sleeping Giant Note, or after MCM Slot Trim in the two Requiem Reforged
profiles), which is after all four masters and before the Synthesis worldspace output in every profile. Wheeler 77/0
unchanged. Backups `*.bak-nrland-20260903`.

**Review and the v2 rebuild (09:06).** Three independent reviewers audited the file. The first build wrapped each land
record in an empty partial CELL record (flags 0x4400, no subrecords) on the strength of DynDOLOD.esp's 66 such cells.
The reviewers showed that precedent is void here: DynDOLOD's partial cells are only worldspace persistent cells, and
the Synthesis worldspace patcher never sees DynDOLOD at all (its workspace order stops at the Synthesis outputs).
Worse, a Mutagen reproduction of the patcher's exact call chain turned the empty cell into a partial record with
DATA=0 and no lighting template in the output, which would have switched off water in all 34 cells and nulled Lux's
lighting template. Fixed in v2: every cell record is now a verbatim copy of the cell that wins immediately before the
patch (Northern Roads - Lux patch x21, Northern Roads x12, the Lock Chests Have Keys patch x1), links remapped, Lux.esp
added as a master. The same harness now emits full cells (HasWater, grid, lighting template, image space) for every
cell and land records carrying the grass layer. Also fixed from the review: header record count now counts groups,
Northern Roads' version-control bytes pass through, INTV added. Check-errors clean on v2.

Two review notes kept for the record. Northern Roads' Dwemer road paint is feathered alpha, never opaque, so grass will
thin through road edges (same as its roads over grass in Tamriel); the city streets themselves are meshes, which NGIO's
raycast culls. And the blanket swap is greener than Grassreach's own hand paint, which left the Silent City floor on a
bare twin texture on purpose; `build_nr_land_patch.py --grassreach-parity` rebuilds with that mask if you prefer the
author's look. Seen in passing: the Requiem Reforged Main profile lists both Synthesis output plugins active while the
output mod folder is disabled there (pre-existing, not touched).

Overriding vanilla LCaveDirt itself was rejected: Bloated Man's Grotto and other cave-textured exteriors would sprout
Blackreach mushrooms.

What happens next, in order: the Synthesis worldspace group is re-run (it copies the winning land records into its
output, so until then the output re-asserts the grass-free version for 25 of the 34 cells), then Blackreach is re-baked
with `grass_regen_blackreach.py` under a new job name (stage, Play, collect, finish), then a look at the Silent City.

---

## Outfit Wheeler 3.0, later the same day: the unequip lock and the "cloud"

**Cannot unequip anything the wheel put on.** The 3.0 DLL equips every piece with the engine's prevent-removal flag
(the same flag a script sets with abPreventRemoval), at all six places it equips, while its own unequip calls do not
force. So nothing the wheel equips can be taken off, in the vanilla inventory or in the wheel. The 2.8 DLL never set
that flag; it is a 3.0 regression of a bug the author already fixed once in 1.2. Patched at 16:23 with
`_tools\outfit-wheeler\patch_forceequip.py` (seven bytes: the six equip sites now pass false, and the Edit Mode item
click now force-unequips so pieces already locked in a save can be freed by clicking them). Backup in
`_backups\2026-09-03 - Outfit Wheeler 3.0 forceequip patch`. Run the script with `--check` after every update.

Ruled out on evidence: the Outfit Equipment System (no outfit for Luna, hook skips the player), Item Equip Restrictor
(restricts equipping only), every script source (no prevent-removal equips on the player), the wheel's input and menu
sinks (no hooks at all).

**Cloud storage.** My 15:39 claim that the wardrobe chest never resolved was wrong: the 31 August saves hold a change
form with 33 items stashed in that chest, and the JSON field I used as proof is hard-coded to zero by the writer. The
wardrobe has worked since the 30 August ID fix. The plugin rebuild that made the chest persistent is kept (every
holding chest in the order is persistent), but it fixed nothing. Proof of life is the CLOUD tab in the wheel's
inventory panel, or a "Transferred from Wardrobe Chest" notification.

**Re-select to unequip (restored 16:5x).** The 2.6 and 2.8 wheels advertised "A: Equip / Unequip" in Play Mode;
3.0 changed the hint to "Equip Outfit" and its swap only toggles Addon slots, so re-selecting a worn outfit
re-equipped it. Restored in the mod's own UI script with `_tools\outfit-wheeler\patch_reselect_unequip.py`: selecting
the outfit you are wearing now takes every piece of it off, and with Auto-Stash on it goes straight into the wardrobe
(selecting it again pulls it back out and equips it). Addon slots keep their own toggle. Backups in
`_backups\2026-09-03 - Outfit Wheeler 3.0 reselect-unequip patch`. Both wheel patches are UI/DLL edits inside the
mod folder and will need re-checking after any Outfit Wheeler update (`--check` on both scripts).
