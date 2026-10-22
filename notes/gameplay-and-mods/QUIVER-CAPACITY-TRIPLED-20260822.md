# Quiver capacity tripled — Skyrim Arrow Overhaul

Date: 2026-08-22
Profile touched: none (plugin content only; all four profiles inherit it)
Plugin edited: `Authoria - Patch - Skyrim Arrow Overhaul - Requiem.esp` (existing patch, still ESL-flagged)
Backup: `...esp.bak-quivercap-20260822` in the same mod folder

## What changed

Every scripted quiver's `baseCapacity` property (SAO_QuiverData) multiplied by exactly 3.
Nothing else about the quivers was changed — armor rating, value, weight, name, model,
bolt/arrow flag and the quiver-management link are all untouched.

| Quiver | Was | Now |
|---|---|---|
| Arrow Bag | 35 | 105 |
| Bolt Bag | 35 | 105 |
| Leather Quiver | 40 | 120 |
| Forsworn Quiver | 40 | 120 |
| Falmer Quiver | 40 | 120 |
| Leather Bolt Quiver | 40 | 120 |
| Draugr Quiver | 41 | 123 |
| Steel Quiver | 42 | 126 |
| Nordic Quiver | 43 | 129 |
| Orcish Quiver | 44 | 132 |
| Dwemer Quiver | 45 | 135 |
| Dwemer Bolt Quiver | 45 | 135 |
| Elven Quiver | 46 | 138 |
| Glass Quiver | 47 | 141 |
| Ebony Quiver | 48 | 144 |
| Stahlrim Quiver | 49 | 147 |
| Daedric Quiver | 50 | 150 |

Bound Quiver was skipped on purpose: it carries no capacity script at all, and bound
arrows are excluded from the count by the manager script anyway.

## How the cap works

`SAO_QuiverManager` computes `maxCapacity = baseCapacity * capacityFactor`.

- `baseCapacity` is the per-quiver number in the table above (plugin data).
- `capacityFactor` is the MCM slider "Quiver Capacity Factor" (range 1.0-5.0, default 1.0).

The two stack. Leaving the slider at 1.0 gives exactly the "Now" column. Pushing the
slider to 2.0 on top of this would give 240 on a leather quiver, and so on.

Arrows over the cap are dropped on the ground by `DropSurplusAmmo`, so the cap is hard,
not a soft warning. Wearing no quiver at all sets the cap to 0 and drops everything.

## Why the patch, and why it needs a Reqtificator run

The Reqtificator (`Requiem for the Indifferent.esp`) currently wins 16 of the 17 quiver
records, so it is the plugin the game actually reads. It adds exactly one thing to each
quiver: a Requiem tempering keyword derived from the quiver's material.

The change was written UPSTREAM of the Reqtificator instead of downstream, so no
generated data gets frozen into a hand-made patch. To keep the patch a clean input, each
overridden record's keyword list was copied back from Skyrim Arrow Overhaul's own version
— the patch carries the mod's original 3 keywords and no Reqtificator output. The next
Reqtificator run re-derives the tempering keyword exactly as before and carries the new
capacity through.

Consequence: **16 of the 17 take effect only after the next Reqtificator run.** The Draugr
Quiver is the exception — the Reqtificator never touched that record, so the patch wins it
outright and it is live now. After the run all 17 are consistent.

## Verification done

- All 17 records read back from the patch: capacity exactly 3x, bolt/arrow flags intact,
  quiver-management link intact, keyword lists back to the mod's original 3.
- Patch record count 311 -> 328 (the 17 new armor overrides, nothing else moved).
  Ammo 105, recipes 101, projectiles 101, game settings 3, actor value 1 — all unchanged.
- `check_errors` on the patch: 0 dangling references, 0 missing masters.
- Master list unchanged (9 masters, no new dependency added).
- ESL flag confirmed still set — no full plugin slot consumed.
- No load order, modlist, plugingroups or profile file was touched.

## To undo

Restore `...esp.bak-quivercap-20260822` over the plugin and re-run the Reqtificator.

---

# Quiver slot moved off the jacket slot — same day

Backup taken before this second pass: `...esp.bak-quiverslot-20260822`

## The conflict

- Arrow quivers were on biped slot **57**. So are the five Corsican Raider Jackets
  and the Vindictor Pauldrons. Equipping a quiver stripped the jacket.
- Bolt quivers were on slot **49**. So are the Corsican pants, the Cute Adventurer
  and Confident Adventurer shorts, the Sparrows Mage pants and the Vindictor Apron.
  Same bug, waiting on the first crossbow.

## Slot survey

All sixteen modder slots (44-49, 52-60) were scanned across the whole load order.
**None is unoccupied.** Item counts:

| Slot | Armor records | What lives there in this list |
|---|---|---|
| 44 | 138 | Wet and Cold hoods (auto-equipped), Dint999 hair, Hal's casual outfit |
| 45 | 200 | mixed; Vindictor Collar |
| 46 | 438 | cloaks |
| 47 | 259 | backpacks (Campfire/Frostfall, LOTD, Cuyi) |
| 48 | 174 | mixed; Vindictor Harness |
| 49 | 245 | pants and shorts — **was the bolt quiver** |
| 52 | 242 | SOS pelvis, skirts |
| 53 | 100 | legwear: garterbelts, stockings, kneepads, legwarmers; an SOS skeleton item |
| 54 | 95 | mixed; Vindictor Cuisses |
| 55 | 154 | earrings and accessories |
| 56 | 134 | tops; Vindictor Cuirass |
| 57 | 152 | jackets and pauldrons — **was the arrow quiver** |
| 58 | 64 | corsets |
| 59 | 71 | Sparrows Mage Jacket, Vindictor Vambraces |
| 60 | 173 | mostly horse and creature gear — **chosen** |

Slot 60 was chosen because its occupancy is dominated by horse skins, horse armor
and creature packs, none of which the player wears. User chose to put arrows AND
bolts both on 60.

## What changed

All 17 scripted quivers plus all 16 quiver armor addons moved to slot 60.
Both the armor record and its addon must carry the same slot or the mesh does not
render, so both were changed together.

The Bound Quiver's armor record was left alone. It has no biped slot at all by
design, so it never conflicts with anything. Its addon was moved to 60 with the
rest purely for tidiness — with no slot on the armor record, nothing renders from
it either way.

## Known trade — this slot is not free either

Equipping a quiver will now unequip, if worn:

- Karlstein / Kokoro / Elendil Belt (Ninirim)
- the three Witchy Lore-Friendly Accessories masks
- the four Modular Mage pasties
- **Ashlander Warrior Armor, Hearthguard Armor and Ash Reader Robes** (Armors of
  the Velothi Pt2) — these sit on the body slot AND slot 60, so a quiver takes the
  whole cuirass off. Worth watching on NPCs, since quivers are distributed by SPID.
- a Tullius Wig 3 accessory and the Bonesaint Banner
- the 3BBB SMP helper objects

If the Velothi armors turn out to matter, the fix is to drop the slot-60 bit from
those five records — they only need the body slot — after checking their addons
don't need 60.

## Timing

The armor addons are won by this patch immediately. The armor records are still
won by the Reqtificator for 16 of the 17, so **until the Reqtificator is re-run the
armor record says slot 57 while its addon says slot 60, and the quiver mesh will not
draw at all.** Run the Reqtificator before playing. The Draugr Quiver is the one
exception and is already fully consistent.

## Verification done

- All 17 armor records read back at slot 60 with their tripled capacities intact
  and keyword lists still the mod's original three.
- All 16 armor addons read back at slot 60 and win the load order now.
- Patch record count 328 -> 344 (16 new armor addon overrides, nothing else moved).
- `check_errors`: 0 dangling references, 0 missing masters.
- Master list unchanged at 9. ESL flag confirmed still set.
- No load order, modlist, plugingroups or profile file touched.
