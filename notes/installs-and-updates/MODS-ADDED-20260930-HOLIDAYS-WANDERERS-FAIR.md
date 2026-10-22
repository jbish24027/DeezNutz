# Mods added 2026-09-30: Holidays + The Wanderer's Fair (and their patches)

Plan: `PLAN-HOLIDAYS-WANDERERS-FAIR-20260926.md` (the analysis; this file is the as-built ledger).
Executed 2026-09-30 10:05-10:25 with MO2 and the game closed. Every write was verified afterwards.
Profile backups: `profiles/<p>/*.bak-holidays-20260930` (all four files, all six profiles).

## Mod folders (12 new + 1 houseCARL patch), all six profiles, all enabled

| Folder | Source (Nexus id / file id) | MO2 block, neighbour | Notes |
|---|---|---|---|
| Holidays | 1533 / 36459 (2.20A1) | Gameplay - Immersion, first under the header | ESP + 2 BSAs. Full plugin. |
| Holidays 4K | 74609 / 312960 | above Holidays | 99 BC7 textures, textures only |
| Fixed Script for Holidays | 88254 / 374081 | above Holidays 4K | `_holidayfreeinn.pex` (loose beats the BSA copy: verified) |
| Holidays -x- Light Placer | 160128 / 669880 | above Fixed Script | 2 Light Placer jsons |
| Holidays - slightly Better Bunting Patch | 156872 / 656298 | above Light Placer | FOMOD option "I DO use this mod" (AnimatedRings esp) + 15 rope textures |
| Descriptions for Various Mods - Holidays | 106229 / 590850 | above Bunting Patch | ONLY `Holidays_DESC.ini` (3 lines) |
| The Wanderer's Fair | 193042 / 810623 (2.0.1.2) | Quests and Newlands - Misc, first under the header | Full plugin, master Holidays.esp. 552 files |
| HSF Holiday Dancing | 172341 / 720598 | Animations - Idles and Actions, below HSF Female Cross Legged | OAR only |
| Professional Dancer | 124608 / 768566 (1.5.0) | below HSF Holiday Dancing | behaviour file + Dance.esp (UNTICKED, see below) |
| JK's Interiors Patch Collection - Holidays | 35910 (5.29.1) | City Stuff - Patches, above JK's Interiors Patch Collection - rerun | ONLY `JKs Palace of the Kings - Holidays Patch.esp`; the installed collection stays 5.28.1 |
| slightly Better Bunting - FYX 3D Sighpost | 142315 / 597903 | FYX Meshes, above FYX - 3D Solitude SighPost | rope mesh + flag texture |
| Festival Rings - Animated - slightly Better Bunting | 149031 / 706216 | above slightly Better Bunting - FYX 3D Sighpost | animated ring + rope; wins both meshes (verified) |
| houseCARL - Authoria - Patch - Holidays and Fair - Requiem | built here | Authoria - Custom Patches, above the Rovan Market Stall Requiem patch | see below |

Skipped on purpose: Lil Patches (its Holidays patch targets the HS Candlehearth Hall, not the JK's one in use);
JK's Winking Skeever Holidays patch (JK's The Winking Skeever not installed); the rest of JK's Interiors PC 5.29.1
(nothing it changes is in use); the "(1)" re-download of the fair (byte-identical, left in Downloads).

Archives filed on D: `gameplay and quests` (Holidays, 4K, Fixed Script, Light Placer, Bunting FOMOD, Descriptions,
SkyrimFair + its Compatibility Patch, JK's Interiors PC 5.29.1, Lil Patches), `animation` (HSF Holiday Dancing,
Professional Dancer), `world and homes` (the two slightly Better Bunting archives).

## Plugins (all six profiles; groups written to plugingroups.txt)

| Plugin | After | Group | State |
|---|---|---|---|
| Holidays.esp (FULL) | WetAndColdSPIDPatch.esp | Gameplay - Early Loaders | active |
| Holidays - better bunting patch.esp (light) | Holidays.esp | Gameplay - Early Loaders | active |
| SkyrimFair.esp (FULL) | ImperialMail - Bruma.esp | Quests and Newlands - Misc | active |
| Dance.esp (light) | SkyrimFair.esp | Quests and Newlands - Misc | **inactive** until the behaviour cache is rebuilt with Professional Dancer |
| JKs Palace of the Kings - Holidays Patch.esp (light) | JKs Palace of the Kings - Sons of Skyrim patch.esp | Visuals - Cities and Towns | active |
| Authoria - Patch - Holidays and Fair - Requiem.esp (light) | Authoria - Reqtificated - Sorceress Attire.esp | Authoria - Reqtificated | active |

Full-plugin census after (MO2 closed): Main 199 · NSFW 208 · DEEEZ 232 · CS 242 · PBR 244 · PICTA 245 (of 254).
This batch cost exactly 2 per profile (Holidays.esp, SkyrimFair.esp — diffed against the backups). The other +2 in
PBR/PICTA since the 09-26 count are DynDOLOD.esm / DynDOLOD.esp / Occlusion.esp from the 09-26 LOD install.
Reqtificator masters: 225 today; Holidays.esp and SkyrimFair.esp join at the next build (227).

Verified: head of every modlist (Testing / FWMF / LOD outputs) untouched; tail of every loadorder from
`Authoria - Output - Synthesis Gameplay.esp` untouched; 0 duplicated group headers, ungrouped count unchanged (1
pre-existing); whole-order missing masters = 0 (4136 plugins); the three light patches: 0 dangling, 0 missing.

## The houseCARL patch: `Authoria - Patch - Holidays and Fair - Requiem.esp` (ESL-flagged, 22 override records)

Masters Skyrim.esm, Update.esm, Holidays.esp. Built with housecarl_apply (dry-run first), flag-only ESL lane.

- 4 Holidays "Spooky Skeleton" bases (`_WetHolidayEncSkeleton01Melee1H / Melee1Hshield / Melee2H / Missile`):
  HealthOffset 0 → 150 and DoesNotBleed added — the two fields Requiem's own EncSkeleton01* carry that these lacked.
  Their own spell (the spooky script), outfit (hooded skeleton), factions and packages untouched. The Reqtificator
  stamps the racial skeleton traits and global perks itself at the next build.
- `_WetHolidayLvlFoDSpeaker` (Eorlkar Bjanssen, the Festival of Discord speaker): Traits template flag added. He is
  templated on LCharGuardSons for everything except looks, ships NO facegen (houseCARL facegen sweep: bake_absent),
  and would have spawned grey-faced. With Traits he wears a Sons guard's face.
- 12 festival clothing pieces: ArmorRating → 0 (3 Tales and Tallows hoods had 2, the 5 Witches masks 4–6, the 4
  Jester hats 9). Clothing keywords were already correct.
- 3 Update.esm tundra shrubs 33/165/204 units from the fair's gate furniture: InitiallyDisabled (the fair only
  masters Skyrim.esm and never touched them).

Everything else in both plugins needs no record edit — see the plan's section 6 for the per-type disposition.
Counts reconciled live: Holidays.esp 4256 own records, SkyrimFair.esp 4551 own records.

## Third-party files edited (register these)

| File | Edit | Check |
|---|---|---|
| Stealth Detection Fixes: `StealthKillDetectionFix_Attack_DISTR.ini`, `StealthKillDetectionFix_DISTR.ini`, `StealthKillDetectionFix_Killmove_DISTR.ini` | `-SkyrimFairNPC` added to the string filter (author's recipe) | `_tools\skyrimfair-spid\skyrimfair_spid_patcher.py "C:\1. AUTHORIA\mods" --dry-run` → "already done" ×7 |
| Brawling - No Hitting Bystanders: `Brawling - No Hitting Bystanders_DISTR.ini` | `ActorTypeNPC,-SkyrimFairNPC` | same |
| Ash Nomad - Bedrolls BOS patch: `Ash Nomad - BOS Use Those Blankets Patch_DISTR.ini` | `ActorTypeNPC,-SkyrimFairNPC` | same |
| Simply Order Summons: `talkToSummons_DISTR.ini` | `\|-SkyrimFairNPC` appended | same |
| Swiftly Order Squad: `Quick Follower Commands_DISTR.ini` | `\|-SkyrimFairNPC` appended | same |
| Authoria - MCM and INI Settings: `SKSE\Plugins\GrassControl.ini` | `SkyrimFairWorld` appended to `Only-pregenerate-world-spaces` | grep; backup `GrassControl.ini.bak-fair-20260930` |
| Authoria - PG Output - PBR: `meshes\architecture\solitude\clutter\sropefestivalring.nif` | moved to `_backups\2026-09-30 - Holidays and Fair\` (the ParallaxGen copy shadowed the animated ring) | asset_status winner = Festival Rings |

Backups of the seven SPID files: `<file>.skyrimfair-backup` beside each (SPID ignores them: the name no longer ends
in `_DISTR.ini`). `--undo` on the patcher restores them.

Why: the fair's ~120 NPCs plus a per-NPC scripted/cloak ability from every one of these mods floods the script
engine about a minute after arrival (documented by the fair's author for Stealth Detection Fixes; the other four
were found by scanning every `*_DISTR.ini` for lines that give every NPC a spell). Functional Fearsome Fists also
hands every NPC an ability but it is a plain stat effect, so it was left alone.

## Consequences that only the generators resolve (not scheduled here)

- The fair's own worldspace has NO grass until the grass cache is rebuilt (`Only-load-from-cache = true`);
  its worldspace is now on the pregenerate list so that rebuild includes it.
- The palisade and light towers have no LOD (the 09-26 DynDOLOD output predates the fair).
- Professional Dancer is inert until the behaviour cache is rebuilt with it; the fair's crowd uses vanilla dances
  meanwhile. When Dance.esp goes live, cut its menu-only MCM with the MCM Slot Trim patch (the list sat at 127/128
  on 09-26; Holidays adds one menu now).
- Requiem balance for the fair's 120 NPCs, 33 chests and 2 doors, and Holidays' 9 actors, arrives at the next
  Reqtificator build (two new masters, 227/254).

## Open (phase 2)

- Holidays decorations vs the city overhauls: no patches exist for Grand Solitude, Spaghetti's Windhelm, Riften
  Expansion, the Markarth mods, Whiterun Has Walls, Northern Roads, the city tree replacers or Cities of the North.
  Force decorations on (MCM toggle or `set _WetHolidayIsHolidayDecorations to 1`), screenshot each town, then build
  `Authoria - Patch - Holidays - <town>` move/disable patches. Ready-made: the JK Palace of the Kings patch
  (installed) and mwee's "Whiterun Circle Trellis REMOVED Holidays Patch" (Nexus 189598, not yet fetched).
- Optional: Holidays - Random Start Date Fix (Nexus 179002).
- After the first launch: read `po3_SpellPerkItemDistributor.log` (fair NPCs absent from the seven spells) and the
  Papyrus log (menu count, no `_Holiday*` / `SkyrimFair*` errors).
- Saturalia weather: `_WetHolidayOvercastSnow` is a 2017 vanilla-style weather; point it at an Astralite snow
  weather if it looks wrong under the CS stack.

## Addendum 12:02 - the two optional extras (installed, all six profiles)

| Folder | Source | Placement | Notes |
|---|---|---|---|
| Whiterun Circle Trellis REMOVED - Holidays Patch | 189598 / 794987 | mod: above Descriptions for Various Mods - Holidays (in the Holidays stack); plugin `Whiterun Circle Trellis REMOVED Holidays Patch.esp` (light) after `Holidays - better bunting patch.esp`, Gameplay - Early Loaders | masters Skyrim.esm + Holidays.esp only (the trellis mod itself has no plugin). 12 Holidays lanterns disabled in four Whiterun cells. It also carries stale bodies of those four CELL records and WhiterunWorld, so it MUST stay this early: verified the live winners are still Occlusion.esp (cells) and the FWMF map plugin (worldspace). |
| Holidays - Random Start Date Fix | 179002 / 747817 | mod: above Fixed Script for Holidays | loose `_holidayquestscript.pex` + `_holidayskyuiconfig.pex` (sources included) win over the BSA copies (verified); does not touch the inn script fix. |

Whole-order missing masters after: 0 (4153 plugins). Archives filed under D:\...\gameplay and quests.

Note: between the 10:10 and 12:02 writes another Claude session added Voiced Books of Skyrim + 13 IVBOS plugins,
Wayfarer.esp, FollowerIdles.esp and the folders UBE YI PRESET HUB, Ice is Slick, Walk With Me (+ Command Gestures),
Sunhelm Follower Needs - Hans Edit, Biggie Traits Wayfarer rename, Follower Idles, IVBOS x2, Voiced Books. The
profile library re-reads fresh before every write, and the diff against the 10:10 backups shows 0 lines removed on
either side, so both batches coexist.

## 2026-10-15 - fair map marker icon
- `Authoria - Patch - Holidays and Fair - Requiem.esp` gained one override: SkyrimFair.esp FairSiteMapMarker (000800) MapMarker.Type Pass -> Camp (user pick). Patch now has 24 records and SkyrimFair.esp as a master; fair loads before it in all 8 profiles; houseCARL errors sweep 0.
- Not live until Synthesis (Worldspace group) is re-run: `Authoria - Output - Synthesis Worldspace.esp` (NoStartingMapMarkers) still wins the marker with Pass.
