# Rovan's Market Stall 1.3.1 -> 1.4.1 update, Market Stall Bag re-ported onto the kit system - 2026-09-06

Nexus 190200, archive `RovanMarketStall Release V1.4.1 190200 1.4.1 2026-09-06T07-39Z N2AYL5mFm.zip` (left in Downloads).
MO2 and the game were closed for the file work. Same mod folders, same plugin names, same placement in all six profiles.
No profile file was touched. Previous state: `MODS-ADDED-20260905-ROVAN-MARKET-STALL-131.md`.

Backups, all in `_backups\2026-09-06 - Rovan Market Stall 1.4.1\`:
- `RovanMarketStall.esp.orig-as-shipped-1.4.1` and `RovanMarketStall.seq.orig-as-shipped-1.4.1` - exactly as Nexus shipped them
- `decompiled-1.4.1\*.psc` - all ten shipped scripts decompiled, untouched. To recompile `RMS_InventoryScript.psc` from
  there, put `= None` back on `CalculateRetailPrice`'s `TenderActor` parameter (the decompiler drops defaults)
- `roundtrip-1.4.1\*.psc` - the three patch scripts decompiled back out of their compiled form, for the diff below
- `installed-1.3.1-state\mod\` and `installed-1.3.1-state\patch\` - both folders exactly as they were before this update

## What the author changed (1.4.0 and 1.4.1 together)

- **The lesser powers are gone.** Deploy and Recall no longer exist as spells. A new script on the player alias removes
  them from old saves by name.
- **Deployment is a craftable kit.** `Market Stall Deployment Kit` (a misc item, firewood-pile model) is forged from
  2 iron ingots, 4 firewood and 2 leather strips. You drop it from the inventory, the stall outline appears and follows
  where you look, and **E, R or the Shout key locks the position in** (the outline no longer needs to be activated).
  The kit is refunded on cancel, on a failed build, on pack-up and on recall.
- **Up to five stalls at once.** Each stall lives in a slot with its own chest, strongbox, ledger and location name.
  Customers only visit the stall nearest the player (within 3500 units).
- **Enterprise Vault.** From any ledger: collect the gold of every stall at once, run the follower sales of every
  remote stall, see reputation standing, and recall any stall remotely (pick a slot, confirm). Note: the author wired
  this menu to the ledger's **"View Statistics"** button.
- **Click-to-assign tender.** "Stall Tender Management" in the ledger, then aim at a companion and press E.
- **Pricing.** Player-made enchantments add an estimated power value to the item value. Tempering adds a bonus.
  The reputation bonus is now tiered: +5% at 25, +10% at 50, +15% at 75, +20% at 100. Follower wage drops with
  reputation. The Speech bonus is unchanged from 1.3.1 as shipped (flat +75% of value at Speech 100).
- The customer barks no longer leak into other NPCs' dialogue menus. Customer visits are hardened against races.
- The author renumbered every record into 0x803-0x84E (still light, header 1.71).

## What was still wrong as shipped

- The same 7 vanilla leftovers as 1.2.1 and 1.3.1. The README still claims none. WhiterunExterior01, Tamriel, the
  `AAADeleteWhenDoneTestJeremy` test cell and 4 placed references, including the dragged Civil War siege trigger
  `CWSiegeAttackTrigge6Whiterun`. Dropped again by removing the CELL and WRLD groups (86 -> 79 records).
- **The voice files are misnamed.** The author renumbered the plugin but shipped the 60 bark files under the OLD
  dialogue FormIDs (`..._00000046_1.fuz` / 47 / 48). The three lines now sit at 0x841 / 0x842 / 0x843, so as shipped every
  bark is silent. Mapped by response text and byte hash (46 = purchased, 47 = browsing, 48 = rejected) and renamed.
- The recall confirm button still said "Refund Kit". Overridden to "Return Bag".

## What was done

1. Cleaned the plugin (byte-level group drop, verified 79 records, no CELL/WRLD/REFR, header count corrected).
2. **Not re-compacted.** The author's own numbering is in the light range, so his FormIDs are kept as shipped:
   `RMS_PriceMultiplier` 0x82F, `RMS_MasterQuest` 0x803. The shipped SEQ (0x02000803) is correct and is used as is.
   `Update.esm` stays a master (unused, harmless).
3. Copied the 1.4.1 assets: 10 shipped scripts (the two dead effect scripts of 1.3.1 deleted), 9 meshes (new
   `firewoodpilesmall01.nif` for the kit), README, and the voice files renamed to 0x841/0x842/0x843.
4. Rebuilt the patch for the new IDs. The 1.75 -> 1.0 price override moved from 0x80E to 0x82F (diff against the new
   base: only the value differs). The bag effect's `MasterQuest` property was repointed 0x829 -> 0x803.
5. Two new overrides in the patch: the kit recipe loses its workbench keyword (it never appears at any forge), and the
   recall confirm button text. Both are one-field overrides, trivially reversible.
6. Re-ported the script edits onto the 1.4.1 decompiles and recompiled them into the patch folder, where they win.
   Each compiled file was decompiled again and matched against its source.

## The patch after this update - `houseCARL - Authoria - Patch - Rovan Market Stall - Requiem`

| File | What |
|---|---|
| `Authoria - Patch - Rovan Market Stall - Requiem.esp` | 5 records, light: override GLOB 0x82F `RMS_PriceMultiplier` 1.75 -> **1.0**; MGEF 0x800 `Authoria_RMS_BagEffect` (MasterQuest -> 0x803); ALCH 0x801 `Authoria_RMS_StallBag` "Market Stall Bag"; override COBJ 0x84C `RMS_RecipeStallKit` with no workbench keyword (recipe hidden); override MESG 0x84E button "Confirm Recall & Return Bag" |
| `Scripts\RMS_ControllerScript.pex` (+ source) | shipped 1.4.1 logic, one kind of change: every place the author hands the kit back now hands the bag back (5-stall refusal, cancelled placement, the four failed-build paths, pack-up, recall). New helpers `GetStallBag` / `GiveStallBag`. Same 80 properties as the quest binds |
| `Scripts\RMS_InventoryScript.pex` (+ source) | shipped 1.4.1 logic, one change applied in BOTH price paths (`CalculateRetailPrice` and `SellOneItem`): Speech bonus = multiplier x Speech/100 x 1/3, Speech capped at 100. Enchantment value, tempering bonus, hold and tiered reputation multipliers stay as the author wrote them |
| `Scripts\Authoria_RMS_BagEffectScript.pex` (+ source) | rewritten for the kit system, see below |
| `SKSE\Plugins\InventoryInjector\...json` | unchanged: camping-gear icon, label "Market Stall" |

## How the bag works now

The bag is the kit. Every rule mirrors what dropping the author's kit does.

1. Use the bag from the inventory. The bag is consumed, the menu closes, and the stall outline appears 185 units ahead
   and follows where you look.
2. Press **E, R or the Shout key** to lock the position in. The menu asks "Build Market Stall Here" or "Cancel".
   Build: the stall goes up. Cancel: the bag comes back. Using a second bag while the outline is out also locks it in,
   and that second bag comes straight back.
3. A refused use (combat, indoors, imprisoned, five stalls already out) hands the bag straight back with the mod's
   own message.
4. Pack up at the ledger ("Disassemble"), or recall from the Enterprise Vault menu (ledger -> "View Statistics" ->
   "Emergency Recall Remote Stall" -> slot -> confirm): the bag returns, with a visible "added" notification.
5. One bag per stall, up to five. Grab as many as you want stalls.
6. Nothing is granted automatically. Add the bag with SearchUI (`Authoria_RMS_StallBag`, 0x801 in the patch). The
   author's kit cannot be crafted; a kit added by console still works through the author's drop path and its stall
   also returns a bag when packed up.
7. There is no recall power any more. Recall needs a ledger (any active stall's ledger reaches every slot). With a
   single stall far away, walk back to it. Author's design.

## Pricing now

Multiplier 1.0, our Speech curve, the author's hold and tiered reputation multipliers. Percent of item value.

| Speech | Requiem vendor pays | Whiterun, rep 0 | Whiterun, rep 100 | Solitude, rep 100 | Winterhold, rep 0 |
|---|---|---|---|---|---|
| 15 | 26% | 105% | 126% | 145% | 89% |
| 50 | 29% | 117% | 140% | 161% | 99% |
| 100 | 33% | 133% | 160% | 184% | 113% |

As the author ships it (1.75 plus a flat +75% at Speech 100): Whiterun rep 0 pays 186% / 213% / 250%, and Solitude at
rep 100 tops out at 345%. Player-made enchantments and tempering now raise the item value before any multiplier, as the
author intended. Lower the global (`set RMS_PriceMultiplier to 0.5`) if the stall is still too rich; the Speech curve
scales with it.

## Verification

- `housecarl_check_errors` on both plugins: 0 dangling references, 0 missing masters.
- `housecarl_validate_scripts`: only the runtime-filled references are unbound (author's design) plus
  `PlacementGhostShader`, which the author never binds (the outline simply has no shader), and one hidden scalar.
- GLOB 0x82F: patch wins, diff against the base is the value only. MGEF property `MasterQuest` resolves to
  `RMS_MasterQuest` (0x803). COBJ and MESG overrides differ from the base in exactly one field each.
- Round-trip decompile of the three new `.pex`: sorted normalised source lines identical apart from comments and
  docstrings. Controller property list identical to the 1.4.1 decompile (80).
- Archive file set = mod folder file set (voice names mapped). Voice files: 20 x 0x841, 20 x 0x842, 20 x 0x843.
- Plugin census unchanged, both plugins light: Main 199, NSFW 208, DEEEZ 232, CS 240, CS-PBR 242, PICTA 243 of 254.
- Profile files: the only writes today were MO2's own (the Modern Wait Menu swap and Svimex from 09-04/05).

## On the next update

Drop the CELL and WRLD groups, copy the assets, keep the author's FormIDs if they stay in the light range (otherwise
compact in place as on 09-05), check the voice file names against the INFO FormIDs (map by response text), resolve
`RMS_PriceMultiplier`, `RMS_MasterQuest`, `RMS_RecipeStallKit` and `RMS_MSG_RecallConfirm` by EditorID, repoint the
patch MGEF property, diff the new controller and inventory decompiles against `decompiled-1.4.1\` before re-applying
the edits, recompile with import dirs = patch `Source\Scripts` + the decompiled folder + SKSE `Scripts\Source` + po3
`Source\scripts`, and put `= None` back on `CalculateRetailPrice`. The bag effect script depends on the controller
names `IsInPlacementMode`, `IsInFollowerTargetMode`, `LockInPlacement`, `GetActiveStallCount`, `FindAvailableSlot`,
`ValidateDeployment`, `StartPlacementMode`, `RMS_MSG_MaxStallsReached` and `GiveStallBag`.
