# Rovan's Market Stall 1.2.1 -> 1.3.1 update, Market Stall Bag re-ported - 2026-09-05

Nexus 190200, archive `RovanMarketStall Release V1.3.1 190200 1.3.1 2026-09-04T22-16Z Yj6wQRi2R.zip` (left in Downloads).
MO2 and the game were closed the whole time. Same mod folders, same plugin names, same placement in all six profiles.
No profile file was touched. Previous state: `MODS-ADDED-20260903-ROVAN-MARKET-STALL.md`.

Backups, all in `_backups\2026-09-05 - Rovan Market Stall 1.3.1\`:
- `RovanMarketStall.esp.orig-as-shipped-1.3.1` and `RovanMarketStall.seq.orig-as-shipped-1.3.1` - exactly as Nexus shipped them
- `decompiled-1.3.1\*.psc` - all nine shipped scripts decompiled, untouched. To recompile `RMS_InventoryScript.psc` from
  there, put `= None` back on `CalculateRetailPrice`'s `TenderActor` parameter (the decompiler drops defaults)
- `installed-1.2.1-state\mod\` and `installed-1.2.1-state\patch\` - both folders exactly as they were before this update

## What the author changed (1.3.0 and 1.3.1 together)

- **Placement is now two casts.** The first cast puts a translucent stall outline 185 units ahead that follows where you
  look. The second cast opens a "Build Market Stall Here / Cancel" menu. The old 4-second re-cast lock is gone.
- **Voiced customer barks.** Three lines (browsing, bought, too expensive) for 20 vanilla voice types, 60 `.fuz` files.
  1.3.1 fixed the barks leaking into every NPC's dialogue menu.
- **Pricing.** Price = value x (multiplier + Speech bonus) x hold multiplier x reputation multiplier.
  Hold: Haafingar and Reach 1.15, Whiterun and Rift 1.0, Eastmarch and Falkreath 0.95, Pale, Hjaalmarch and
  Winterhold 0.85. Reputation is a new global `rms_StallReputation` (0-100, +0.2 per sale, +1 per deploy) worth up to +15%.
- **Follower tender.** The tender's own Speech is used when a follower mans the stall.
- **Speech XP.** Each sale awards 3-45 Speech XP (square-root of the sale value). Follower sales award 15% of that.
- Customer slots abort cleanly on pack-up and recall. A Papyrus race condition on pack-up was fixed.
- The author flagged the plugin ESL (header 1.71, FormIDs 0x03-0x4A).

## What was still wrong as shipped

- The same 7 vanilla leftovers as 1.2.1. The README still claims none. WhiterunExterior01, Tamriel, the
  `AAADeleteWhenDoneTestJeremy` test cell and 4 placed references, including the dragged Civil War siege trigger
  `CWSiegeAttackTrigge6Whiterun`. Dropped again by removing the CELL and WRLD groups (81 -> 74 records).
- A SEQ ships this time, but it holds the uncompacted quest ID (0x02000004). Regenerated.

## What was done

1. Cleaned the plugin (byte-level group drop, verified 74 records, no CELL/WRLD/REFR).
2. Compacted in place with houseCARL: 74 records at 0x800-0x849, light flag kept, unused `Update.esm` master dropped.
   houseCARL carried the 60 voice files to the new INFO FormIDs (0x824, 0x826, 0x828) and rewrote the SEQ (quest 0x829).
   The old-name voice files it left behind were deleted.
3. Copied the 1.3.1 assets: 9 shipped scripts, 9 meshes (new `rms_marketstall_nocollision.nif`), README, the
   `Sound\Voice` tree.
4. Rebuilt the patch for the new IDs. `RMS_PriceMultiplier` landed on 0x80E again, so the 1.75 -> 1.0 override still
   fits (diff against the new base: only the value differs). The bag effect's `MasterQuest` property was repointed
   0x820 -> 0x829 (0x820 is now a Static). The patch is still light. houseCARL added `Skyrim.esm` and `Update.esm` to
   its master list on the rewrite, which is harmless.
5. Re-ported the script edits onto the 1.3.1 decompiles and recompiled them into the patch folder, where they win.
   Each compiled file was decompiled again and matched against its source.

## The patch after this update - `houseCARL - Authoria - Patch - Rovan Market Stall - Requiem`

| File | What |
|---|---|
| `Authoria - Patch - Rovan Market Stall - Requiem.esp` | 3 records, unchanged in role: override GLOB 0x80E 1.75 -> **1.0**; MGEF 0x800 `Authoria_RMS_BagEffect` (MasterQuest -> 0x829); ALCH 0x801 `Authoria_RMS_StallBag` "Market Stall Bag" |
| `Scripts\RMS_ControllerScript.pex` (+ source) | shipped 1.3.1 logic, five changes: deploy power removed instead of granted; `GetStallBag` / `GiveStallBag` / `TakeStallBag` helpers; the placement hint names the bag; a spare bag is taken when the stall goes up; the bag returns on pack-up and on recall. Same 74 properties as the quest binds |
| `Scripts\RMS_InventoryScript.pex` (+ source) | shipped 1.3.1 logic, one change: Speech bonus = multiplier x Speech/100 x 1/3, Speech capped at 100. The hold and reputation multipliers stay as the author wrote them |
| `Scripts\Authoria_RMS_BagEffectScript.pex` (+ source) | rewritten for the two-step placement, see below |
| `SKSE\Plugins\InventoryInjector\...json` | unchanged: camping-gear icon, label "Market Stall" |

## How the bag works now

The bag is the power. Every rule below mirrors what the power does when cast.

1. Use the bag. The stall outline appears in front of you and follows where you look. The bag comes straight back.
2. Use the bag again. The menu asks "Build Market Stall Here" or "Cancel". Build: the stall goes up and the bag is gone.
   Cancel: the bag comes back.
3. A refused deploy (combat, indoors, imprisoned, stall already out) hands the bag straight back.
4. Pack up at the ledger, or cast Recall Market Stall: the bag returns. Recall with no stall out does nothing extra.
5. Pressing E on the outline does nothing. The outline mesh has no collision, so it cannot be activated. The author's own
   power path has the same limit; the second use is the only way to lock the position.
6. Nothing is granted automatically. Add the bag with SearchUI (`Authoria_RMS_StallBag`, 0x801 in the patch). The deploy
   power is removed if a save has it. The recall power is still granted at game start.

## Pricing now

Multiplier 1.0, our Speech curve, the author's hold and reputation multipliers. Percent of item value.

| Speech | Requiem vendor pays | Whiterun, rep 0 | Whiterun, rep 100 | Solitude, rep 100 | Winterhold, rep 0 |
|---|---|---|---|---|---|
| 15 | 26% | 105% | 121% | 139% | 89% |
| 50 | 29% | 117% | 134% | 154% | 99% |
| 100 | 33% | 133% | 153% | 176% | 113% |

As the author ships it (1.75 plus a flat +75% at Speech 100): Whiterun rep 0 pays 186% / 213% / 250%, and Solitude at
rep 100 tops out at 331%. Lower the global (`set RMS_PriceMultiplier to 0.5`) if the stall is still too rich; the Speech
curve scales with it.

## Verification

- `housecarl_check_errors` on both plugins: 0 dangling references, 0 missing masters.
- `housecarl_validate_scripts`: only the runtime-filled references are unbound (author's design) plus 3 hidden scalars.
- All 74 controller properties on the compacted quest resolve to the intended records. INFO 0x824 links to the
  browsing topic. Both effect scripts' `MasterQuest` point at 0x829. The deploy spell points at MGEF 0x813.
- Round-trip decompile of the three new `.pex`: bodies identical to source. Only declaration order and the baked
  default differ, which is the decompiler's known behaviour.
- Plugin census unchanged: nothing added or removed, both plugins light, patch folder still above the mod folder.

## On the next update

Same recipe. Drop the CELL and WRLD groups, copy the assets, compact in place (houseCARL now carries the voice files
and the SEQ), resolve `RMS_PriceMultiplier` and `RMS_MasterQuest` by EditorID, repoint the patch MGEF property, diff the
new controller and inventory decompiles against `decompiled-1.3.1\` before re-applying the edits, recompile with import
dirs = patch `Source\Scripts` + the decompiled folder + SKSE `Scripts\Source`, and put `= None` back on
`CalculateRetailPrice`. The bag effect script only depends on the names `IsInPlacementMode`, `StartPlacementMode`,
`LockInPlacement`, `IsStallDeployed` and `GiveStallBag`.
