# Crafting Pulls Resources From Containers - Legacy of the Dragonborn ini - 2026-09-06

Nexus 137693 (file 759616, v1.1.3). Archive `Crafting Pulls Resources from Containers LotD ini-137693-1-1-3-1780604313.7z`,
filed to `D:\1. MOD STUFF\1. SKYRIM FILES\gameplay and quests\`.
Base mod: `Crafting Pulls Resources From Containers` 1.1.1 (Nexus 135613), already installed and enabled in all six profiles.
Legacy of the Dragonborn V6 6.10.1, enabled in all six profiles.
MO2 and the game were closed for the writes.

## What it is

One file, `SKSE\Plugins\CraftingPullFromContainers.ini`. It adds 20 Legacy storage containers as permanent links, so every
crafting station in the game can use what sits in the Safehouse sorting storage: ingots and ore, ingredients, leather,
potions, poisons, gems, soul gems, firewood, building materials, cooked and raw food, liquor, scrolls (Library), clutter,
treasury, archaeology fragments, fossils, heartstones, spider pods, and the writing supplies box in the Hall of Heroes.

## Save safety

No new save needed. The DLL reads the ini once at game launch (SKSE kDataLoaded, before any save is loaded) and keeps the
list in memory. It writes nothing to the save or the co-save and registers no serialization. Source checked
(github.com/JerryYOJ/CraftingPullFromContainer-SKSE, matches the 1.1.1 DLL's strings).
All 20 references are persistent in the ESM (persistent children of their cells), which the mod needs to reach them from
anywhere.

## How it was installed

New mod `Crafting Pulls Resources From Containers - LotD ini`, placed directly above the base mod in all six profiles.
Only `modlist.txt` changed (no plugin, so `plugins.txt`, `loadorder.txt` and `plugingroups.txt` are untouched).
Backups `modlist.txt.bak-cpfc-lotd-20260906` in every profile. This install added exactly one line (+54 bytes) per file
at 11:39. A separate process then added `+Authoria - No Banner Wind Sound` to five of the six profiles at 11:40:49
(not the Main profile); that line is not part of this install and both lines are intact.
The insert script is kept at `_backups\2026-09-06 - CPFC LotD ini\apply_cpfc_lotd_profiles.py` (idempotent, re-run if MO2
ever parks the mod unchecked at the top of the list).

The ini in the new mod is a MERGE, not the shipped file. Both originals are in `_backups\2026-09-06 - CPFC LotD ini\`.

- Shipped LotD ini: `Range=1`, `IgnoreOwnership=true`, no `IncludeMerchantChest` line. Range=1 would switch off pulling
  from nearby containers everywhere (only the linked Legacy storage would count), and IgnoreOwnership=true would let
  stations use containers you do not own.
- Kept the Authoria values, which are also the base mod's shipped defaults: `Range=500`, `IgnoreOwnership=false`,
  `IncludeMerchantChest=false`. Verified against the source that the Legacy containers pass the ownership check with
  IgnoreOwnership=false: the Safehouse, Gallery Library and Hall of Heroes cells are owned by PlayerFaction, the
  `Utility Cell - LOTD` is unowned, 18 refs have no owner of their own and 2 (fragments, fossils) are owned by the Player.
- Kept the existing link `0x6363F7~Kaidan - Immersive Features.esp` (the chest in Kaidan's tent, added in game on
  2026-08-02). This link has never loaded: the mod's ini parser deletes every space from a line before reading it, so it
  looks up `Kaidan-ImmersiveFeatures.esp` and fails (log: `Failed to lookup form 0x6363F7:Kaidan-ImmersiveFeatures.esp`,
  `permaLinksCount:0`). Harmless, kept as-is. No plugin with spaces in its name can be permalinked by this mod.
- The list is written without the shipped file's stray space and trailing comma. The parser tolerates both (the trailing
  comma only logs one error line).

## Verification

- `housecarl_skse_inventory`: the ini resolves to the new mod, the DLL still to the base mod.
- After the next launch the DLL's own log should read
  `[LoadConfig] Range:500  bIncludeMerchantChest:false  bIgnoreOwnership:false  permaLinksCount:20`
  (the Kaidan line stays as one error). Log: `Documents\My Games\Skyrim Special Edition\SKSE\CraftingPullFromContainer.log`.
- In game: at any forge, cooking pot or alchemy table away from the Safehouse, the crafting menu should list what is in
  the Legacy sorting storage.

## Follow-up the same day: player-home containers

The user asked for permalinks to every container in player homes. `_tools\home-containers\scan_home_containers.py`
(read-only, 3 s) lists every container reference in every player-house cell of the active profile:
`permalinks_candidates.txt` (2653 linkable), `permalinks_recommended.txt` (821 storage chests and furniture in the
real homes; 461 persistent, 360 temporary), `home_containers_report.md` (per-home counts). Two limits found in the
mod's source: a link to a temporary reference is silently skipped while that home is unloaded, so most vanilla, CC and
mod home chests need a persistence override patch first; and plugins with spaces in their file name cannot be linked
at all (Mirele Tower, Talos' Tease, Riftweald Manor, Black-Briar Lodge, Kaidan's tent, Gray Fox Cowl homes, Kynesby,
Riverside Shack). Nothing was written to the ini or the load order for this; the user decides the set.
`list_playerhouse_chests.py` narrows it to the vanilla safe chest base `PlayerHouseChest` (`playerhouse_chests.txt`,
127 refs load-order-wide); the two IDs the user read off the in-game console (Proudspire 09DA07, Honeyside 0D721E)
match the scan. Of the vanilla five only Breezehome's second chest is persistent as shipped; the three Hearthfire
manors' chests are persistent.

## On the next update

Nexus 137693 ships only this ini. Re-merge rather than overwrite: keep `Range`, `IgnoreOwnership` and
`IncludeMerchantChest` from the current file, replace the Legacy entries with the new list, and keep any links added in
game (the DLL writes AddLink results back into whichever ini wins, i.e. this mod's).
