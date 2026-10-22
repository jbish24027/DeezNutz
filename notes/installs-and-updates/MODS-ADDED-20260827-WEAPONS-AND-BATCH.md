# Batch install 2026-08-27 — updates, new mods, weapons Requiem-patched
Profile: DEEZ CS NUTZ · All work verified with houseCARL check_errors (0 dangling, 0 missing masters).
Profile-file backups: `*.bak-batch-20260827` and `*.bak-batch2-20260827` in the profile folder.

## Updates completed
- **Canidae 2.24** (earlier today): pelt plugin lost its custom red-pelt item + wolf NPC overrides (upstream compat fix).
  `Authoria - Patch - Canidae - Requiem.esp` adapted: dead item override removed, red wolf drop → vanilla wolf pelt,
  Canidae master auto-pruned. Backup `_backups\2026-08-27 - Canidae 2.23 pre-2.24`.
- **BackPocket 0.2.0**: pocket/unpocket button, controller support, menu guards. Backup kept.
- **Outfit Wheeler 2.8**: CLEAN update per user. ESP now ESL (author's own chest-bug fix; frees a full slot →
  252/254). Old outfit JSON moved aside (`_backups\2026-08-27 - Wheeler json pre-2.8`) — outfits rebuild in-game.
  Auto-stash stays OFF in our settings INI until the in-game stash/retrieve test passes. Chest ref in 2.8 is local
  0x000002 (not the 0x800 the 2.7 DLL wanted) — assume new DLL matches; test stash manually before trusting it.
  Angarvunde dirty CELL still present, still inert under Lux.
- **Embers XD 3.2.7**: fingerprint proved the installed 3.2.6 folder is BYTE-IDENTICAL to a 3.2.7 install under our
  exact FOMOD choices (CS flames, LP embers-only, esm+esp, forges/craters/STAC/9 patches/Solitude braziers, torch
  atlas fix = 3.2.7's own file, LP Add-On files = already installed). Version stamp only; zero file changes; all 52
  dependent patches untouched by construction. Rest-By-Campfire patch skipped (targets a mod we don't run).

## New mods installed (14 folders, 13 plugins — all ESL/light)
Weapons block (modlist above Vindicator): Vibrant Weapons (esl+DLL+BSAs+SEQ), VW Expansion (see surgery below),
VW - No Shock Lights (ESL-flagged by us), VWE - Reduced Effect (loose dds, wins over VWE), Witcher SilverSword
(ESL-flagged by us — record range was legal), Witcher Steel - Silver swords, Ancient Hoplite Kopis, Imperial Chefs
Knife. Elsewhere: DiegeticTravel (after CFTO), Publican's Perch + Samples of Stools (after Diverse Campfires BOS),
Aspens Ablaze Animations Add-On (base plugin only; wins its 3 vanilla aspen TREE overrides at depth 5),
Dynamic Wind High Quality Ivy (JSON configs; content keys `0x…~Ivy Replacer BOS.esp` — filename irrelevant),
Furnitures Height Size Fix (after Golden Claw).
- **NOT installed:** "Aspens Ablaze - Seasons - Animated.esp" (masters 4 Aspens variant esps we don't run) and the
  whole "Dynamic Wind For Aspens Ablaze Anim Seasons 2x" mod (all 9 JSONs key those absent variant plugins — inert).
  Both stay in Downloads if the seasons-variant lane is ever adopted.
- Publican's Perch had a STALE enabled plugins.txt/loadorder line from an earlier try (removed; today's position kept).
- Furnitures Height Fix caveat: its Default Object Manager override loses to 3BBB + SunHelm (pre-existing singleton
  chain); its script-side fix still runs. If sit-height still misbehaves, this is why.

## Vibrant Weapons Expansion surgery (shipped broken; fixed in place)
1. Declared 2 CC masters absent from this instance (chrysamere, advcyrus) with ZERO actual references (verified:
   every VMAD/FLST/CTDA hit was byte-noise). Swapped the dead MAST strings to always-present free-CC
   (curios, advdsgs) — header-only edit, no remap needed.
2. ESL-flagged with 2 records OUTSIDE the light range (0x5BFD, 0x15051) → houseCARL compact_plugin in place:
   654 records renumbered into 0x800–0xFFF, clean external scan (nothing referenced it yet — fresh install).
3. NO SEQ file for 4 start-enabled quests → its FX registration would NEVER have fired. Wrote
   `SEQ\VibrantWeaponsExpansion.seq` (in the VWE folder) + `SEQ\Vibrant weapons.seq` (in the VW folder).
VW first-run notes (README): effects appear after an on-screen notice + re-equip; NPCs need re-equip or cell reload;
"Reboot Potion" via console fixes a lost library.

## Requiem patch: `Authoria - Patch - New Weapons - Requiem.esp` (ESL, loads directly above RFTI)
Masters: Skyrim, Update, Dragonborn, Vikings Weaponry, the 4 weapon esps, Requiem.esp, Starting Choices.esp.
Live-comparable derivations (winners incl. RFTI; note Requiem crit = FULL damage, not half):
| Weapon | Class | Dmg/Crit | Value | Wt | Spd/Reach | Notes |
|---|---|---|---|---|---|---|
| Hoplite Kopis | steel 1H sword | 48/48 | 45 | 10 | 1.0/0.7 | + curved FX (VW addon) |
| Hoplite Dagger | steel dagger | 30/30 | 20 | 2.5 | 1.3/0.49 | small-draw sound |
| Witcher silver sword (186980) | SILVER greatsword | 102/102 | 180 | 17 | 0.75/0.91 | +WeapMaterialSteel (Requiem silver pattern) |
| Steel Witcher Sword (+_s twin) | steel greatsword | 102/102 | 90 | 17 | 0.75/0.91 | both variants statted |
| Zireael | SILVER greatsword | 102/102 | 180 | 17 | 0.75/0.91 | +WeapMaterialSteel; named, vendor-only |
| Imperial Chefs Knife | steel dagger | 30/30 | 20 | 2.5 | 1.3/0.49 | **re-tiered ebony→steel (judgment)** |
Recipes: all 14 craft/temper COBJs KEPT and overridden to comparable shapes (correct ingots incl. silver 4/1/2
greatsword shape, Craftsmanship perk gate on all); witcher-silver forge recipe normalized Skyforge→standard forge.
Leveled lists (additive Add on winners, Level 1 Count 1, single entries as exotic imports):
kopis → Loot/Town/Blacksmith/Bandit sword pools; hoplite dagger → Loot/Town/Blacksmith dagger; chef's knife →
Town dagger only; steel witcher (main variant) → Loot/Town/Blacksmith/Bandit greatsword; witcher silver →
LItemSilverHandWeapon + REQ_CLI_VendorStocks_Silverweapons; Zireael → silver vendor pool only.
Requiem.esp master present → Reqtificator merge-eligible. Faction-flavored pools (vampire/civil-war) deliberately
skipped for these exotics. The Reqtificator-generated Quality* lists untouched (build outputs).
Starting Choices: 6 new exchange-station entries at **0 tokens** (no Items; GetItemCount(SC_Token)>0 visibility
condition = offer exists only during the start sequence). The "_s" scabbard twin skipped (duplicate menu name).

## VW addon: `Authoria - Vibrant Weapons - New Blades.esp` (ESL, above RFTI)
Kopis appended to `_JGFX_WeaponExtensionsCurved` → curved-sword FX when enchanted (same treatment as the scimitar).
All other new blades get correct FX automatically via their type keywords (greatsword/dagger). Exact-fit bespoke FX
meshes per blade would need Blender work per the bundled guide (`scratchpad adds\vw-guide\instructions.pdf`) — the
record-level ceiling is reached.

## Still pending / held
- Reqtificator rerun REQUIRED before play (user runs it — new weapon patch, LVLI merges, Canidae patch change).
- Holds: SH2 core 1.15 (permanent), Animated Ships Bobbing 1.1.2 (no benefit), Minotaur's Fury 1.2 + Wounds Legs 3.0
  (user call), DW-Aspens seasons JSONs (inert without variant esps).
- Snow: NOTHING installed; plan doc gate still open (DYNAMICSNOW-INSTALL-PLAN.md §7 has the Nexus-vs-Alpha comparison).
