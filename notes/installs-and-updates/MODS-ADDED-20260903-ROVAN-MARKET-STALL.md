# Rovan's Market Stall 1.2.1 - install + Requiem patch + Market Stall Bag - 2026-09-03

Nexus 190200, archive `RovanMarketStall Release V1.2.1 190200 1.2.1 2026-09-01T05-45Z Z3mWyIRct.zip` (kept in Downloads).
MO2 and the game were closed the whole time. Requires SKSE (1.6.1170 here) and po3 Papyrus Extender (installed 6.0.0;
the scripts never actually call it).

Three passes the same day: (1) install + clean + record patch, (2) decompile the scripts, fix the Speech curve,
ESL-compact the plugin, (3) replace the deploy power with a Market Stall Bag item. This file describes the final state.

Backups, all in `_backups\2026-09-03 - Rovan Market Stall\`:
- `RovanMarketStall.esp.orig-as-shipped-1.2.1` - the plugin exactly as Nexus shipped it
- `RovanMarketStall.esp.cleaned-full-pre-compact` - after the clean, before compaction (full plugin, old FormIDs)
- `Authoria - Patch - Rovan Market Stall - Requiem.esp.pre-compact` - the patch as it was against the old FormIDs
- `decompiled-1.2.1\*.psc` - all eight scripts decompiled from the shipped .pex files (the untouched originals)
- Profile files: `*.bak-rms-20260903` in all six profiles (pre-session state). Outfit Wheeler: dated backups in `_backups\`.

## What the mod is

A portable market stall. You stock a chest, nearby townsfolk walk up and buy things, gold lands in a strongbox, a
ledger tracks it. A follower can tend the stall while you are away and takes a 20% cut. Everything is spawned at
runtime; the mod places nothing in the world itself.

## How you use it in this build

- Nothing is handed out automatically. Add the **Market Stall Bag** yourself with SearchUI (item name "Market Stall
  Bag", EditorID `Authoria_RMS_StallBag`, FormID 0x801 in `Authoria - Patch - Rovan Market Stall - Requiem.esp`).
  It weighs 15, is worth nothing, sits under Potions with a camping-gear icon and the label "Market Stall", and can be
  favourited and hotkeyed.
- **Use the bag** outdoors: the stall assembles 200 units in front of you and the bag is gone while the stall is out.
  If the deploy is refused (combat, indoors, no room, already deployed, used twice within 4 seconds) the bag comes
  straight back.
- **Pack up** at the ledger (chest and strongbox must be empty) or cast **Recall Market Stall** from anywhere: the
  stall vanishes and the bag returns to your inventory.
- Casting Recall with no stall out only shows the mod's "no active stall" message; it never creates a bag.
- The shipped "Deploy Market Stall" power is no longer granted (and is removed if a save already has it). The
  recall power is still granted at game start, as shipped.

## What was wrong with the plugin as shipped

**Dirty vanilla overrides.** The README says the mod edits no vanilla cells. The plugin carried 7 vanilla records
left behind by the author's Whiterun test session:

| Record | What it is | Diff vs vanilla | Would it have won here? |
|---|---|---|---|
| REFR 0009B95E `CWSiegeAttackTrigge6Whiterun` | the Civil War siege stage trigger outside Whiterun | **dragged 265 units**, script properties differ | **yes** - nothing else touches it |
| REFR 000745B6 | a CWThreatTrigger outside Whiterun | nudged 5 units, enable-parent bytes zeroed | **yes** - nothing else touches it |
| CELL 0000961B `WhiterunExterior01` | the Whiterun exterior cell | junk-dword only (ITM) | no - 30 overriders, Occlusion.esp wins |
| WRLD 0000003C `Tamriel` | the worldspace | ITM | no - FWMF map patch wins |
| CELL 0006C3B6 `AAADeleteWhenDoneTestJeremy` + 2 REFRs | a Bethesda test cell and two refs in it | positions nudged | irrelevant (test cell) |

Fix: the CELL and WRLD top-level groups were dropped (exactly those 7 records; none of the mod's own live there).

**No SEQ file.** The master quest is start-game-enabled and lives in an .esp, and the archive ships no
`SEQ\RovanMarketStall.seq`. Without it the engine never starts the quest, so nothing would ever have been handed to
the player. The SEQ is now in the mod folder (FormID 0x01000820 = the compacted quest).

**A script that does not exist.** The stall activator record attaches a script named `RMS_Stall_Activator`, and no
such .pex is in the archive. Harmless (one Papyrus log line per load), left alone.

## Compaction

`RovanMarketStall.esp` is ESL-flagged: 62 records renumbered to 0x800-0x83D, index 01, houseCARL also dropped the
unused `Update.esm` master. Safe because the decompiled scripts hard-code only vanilla FormIDs (XMarker 0x34,
XMarkerHeading 0x3B, Gold 0xF, the DialogueFollower quest). Costs no full slot; census Main 199, NSFW 208,
DEEEZ 232, CS 240, CS-PBR 242, PICTA 243.

## What the scripts actually do (decompiled)

- **Price** = item base value x (`RMS_PriceMultiplier` + Speech bonus), truncated, minimum 1. Shipped Speech bonus =
  Speech / 100 x 0.75, a flat +75% of value at Speech 100 regardless of the multiplier.
- Value comes from the BASE form: Requiem's rebalanced values apply, but enchantments and tempering are ignored. Gold
  is conjured into the strongbox, like vanilla vendor gold.
- **Customers**: any actor within 1500 units that is not dead, essential, a guard, a child, in combat, in a scene or
  dialogue, unconscious, arrested, one of the last four customers, or behind the stall. No race, hostility or creature
  check. Author's design, not touched.
- **Stall tender**: the vanilla follower alias first, then any teammate within 500 units, then ANY non-guard adult
  within 300 units of the stall. Author's design, not touched.
- **Stolen goods**: `rms_AllowIllicitGoods` = 0 calls `SetContainerAllowStolenItems(false)` on the chest - a real
  SKSE native (added for game 1.6.1126, present on the 1.6.1170 build here), so stolen items cannot be stocked. The
  chest script also declares contraband keywords the plugin never defines - inert. Stolen loot still goes through a
  Requiem fence. Correct as is.
- Quest: start-game-enabled, no level gate, 13 aliases filled by script, priority 60. Nothing the Reqtificator
  processes anywhere in the plugin.

## The Requiem patch - `houseCARL - Authoria - Patch - Rovan Market Stall - Requiem`

ESL-flagged, enabled in all six profiles, plugin after `Authoria - Patch - Mirele Price.esp` (Authoria - Custom
Patches). Its mod folder is HIGHER priority than the stall mod in every profile, so its scripts win. Contents:

| File | What |
|---|---|
| `Authoria - Patch - Rovan Market Stall - Requiem.esp` | 3 records: override GLOB 0x80E `RMS_PriceMultiplier` 1.75 -> **1.0**; new MGEF 0x800 `Authoria_RMS_BagEffect` (Script archetype, script below, property MasterQuest -> the mod's quest); new ALCH 0x801 `Authoria_RMS_StallBag` "Market Stall Bag" (knapsack model, weight 15, value 0, no keywords, no consume sound, one effect: the MGEF) |
| `Scripts\RMS_InventoryScript.pex` (+ source) | shipped logic, one change: Speech bonus = multiplier x Speech/100 x 1/3, Speech capped at 100 |
| `Scripts\RMS_ControllerScript.pex` (+ source) | shipped logic, three changes: no deploy power at start (removed if present), the consumed bag returned on pack-up, the consumed bag returned on recall. Nothing is granted automatically. Same property list, so the quest's bindings in the mod's plugin still fit |
| `Scripts\Authoria_RMS_BagEffectScript.pex` (+ source) | fires when the bag is used: deploy through the controller; if the stall is not up afterwards, hand the bag back |
| `SKSE\Plugins\InventoryInjector\...json` | icon-injector rule: camping-gear icon, label "Market Stall", for the bag |

Every compiled script was decompiled back and checked against its source.

### Why the price change

Requiem's live barter settings are `fBarterMax` 4 / `fBarterMin` 3 (Requiem.esp wins both; vanilla is 3.3 / 2.0).
A Requiem shopkeeper pays you a quarter of value at Speech 0 and a third at Speech 100 - a +33% gain over the
skill. The shipped stall paid 2.5x value at Speech 100, seven and a half times a Requiem merchant. Now it tracks the
merchants' curve at a constant 4x their payout:

| Speech | Requiem vendor pays | Stall shipped | Stall now |
|---|---|---|---|
| 15 (new character) | 26% | 186% | 105% |
| 50 | 29% | 213% | 117% |
| 100 | 33% | 250% | 133% |

Trade and Barter (preset 5) is deliberately not read by the stall: it rewrites the barter settings per merchant, so
a stall reading them would follow whichever shop you visited last. Lower the global (0.5 = 2x a vendor) if 4x is
still too rich; the Speech curve scales with it. `set RMS_PriceMultiplier to <n>` works in game (globals are saved).

### How the bag works, technically

The bag is an Ingestible (potion record type) with one scripted effect. Using it from the inventory consumes it and
runs the effect on the player; the effect script calls the mod's own `DeployStall()`. The controller keeps the bag's
FormID via `GetFormFromFile(0x801, "Authoria - Patch - Rovan Market Stall - Requiem.esp")`, so no property had to be
added to the quest record. No Reqtificator involvement (it never touches consumables), no armour slot, no outfit-tool
interaction. Any SunHelm / Taberu / potion-hotkey mod ignores it because it carries no food or potion keyword.

## Requiem disposition (69 records enumerated, 62 kept + 7 removed)

| Type | Count | Disposition |
|---|---|---|
| GLOB | 18 | 1 patched (price). 6 runtime counters, 11 pacing knobs at author defaults. Illicit goods OFF matches Requiem's fence-only rule. |
| SPEL / MGEF | 2 + 2 | 0-cost lesser powers, Script archetype, no keywords. Deploy power no longer granted (script); recall kept. Neither Magic Redone nor the Reqtificator touches them. |
| CONT | 2 | empty, no respawn, no leveled loot. |
| QUST / PACK | 1 + 4 | script and AI layer; Speech scaling and bag behaviour patched at the script. |
| ACTI / STAT / MESG | 4 + 4 + 25 | cosmetic / UI. |
| CELL / WRLD / REFR | 2 + 1 + 4 | removed. |

## Where it landed (same in all six profiles)

- Mod folder `Rovan's Market Stall`: next to `Trade and Barter`. Zero file conflicts.
- Plugin `RovanMarketStall.esp` (light): after `COINMerchantExchange.esp`, before `Missives.esp`, "Gameplay - Early Loaders".
- Patch folder: next to `houseCARL - Authoria - Patch - Requiem - Warm Drinks`. Patch plugin (light): after
  `Authoria - Patch - Mirele Price.esp`, before `Authoria - Patch - USSEP - TGAE.esp`, "Authoria - Custom Patches".
- All four profile files CRLF; header-split check 0 duplicated headers, 0 ungrouped rows; Outfit Wheeler
  calibrates 77 match, 0 mismatch.

## On a mod update

Re-clean (drop CELL + WRLD groups), re-compact, re-SEQ, then re-resolve by EditorID: the price global (patch
override), the quest (the MGEF property `MasterQuest` and the SEQ). Re-diff the new controller and inventory scripts
against `decompiled-1.2.1\` before re-applying the three script edits; the bag effect script needs no change unless
the controller's function names change.
