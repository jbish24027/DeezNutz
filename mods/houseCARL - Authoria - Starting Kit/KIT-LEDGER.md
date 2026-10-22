# Authoria - Starting Kit — ledger

Built 2026-08-27 (expanded same day from 80 to 1433 entries at user request; same day again:
conditions stripped + "Closet Kit" bundle added after the user saw NO free entries in game).
Profile: DEEZ CS NUTZ (enabled; disabled entries in the other 4 profiles).
Plugin: `Authoria - Starting Kit.esp` — ESL-flagged, **1436 records**: 1434 COBJ (000800–000D98 +
000D9B) + 1 LVLI (000D99) + 1 MISC (000D9A). Zero overrides, 47 masters. Position: directly above
`Requiem for the Indifferent.esp`, right after `Authoria - Vibrant Weapons - New Blades.esp`
(group: Authoria - Late Custom Patches). Position is cosmetic — the plugin overrides nothing.
Verification: check_errors clean (0 dangling, 0 missing masters); full-fidelity audit of all 1433
catalog entries against the generation list = CLEAN (every editorid's hex suffix equals its item's
local FormID — a self-checking invariant); "Conditions exists" sweep = 0 matches (see fix below).
Profile-file backups: `*.bak-startkit-20260827`.

## What it is

Every entry is a **Starting Choices exchange-station offer at 0 tokens**: COBJ on
`SC_ExchangeStationKWYD (00080C:Starting Choices.esp)`, NO Items, **NO conditions**.
The 6 free weapon entries (kopis, hoplite dagger, witcher silver/steel, Zireael, chef's knife) stay
in the weapons patch — not duplicated here.

## 2026-08-27 fix: the vanishing-entries condition (user report: "didn't see the kit or the witcher swords")

The original pattern (inherited from the weapons patch) gated every free entry with
`GetItemCount(SC_Token) > 0`. The user's own working kits are gated `>= cost` and stay visible while
tokens are held — but the moment the player spends their LAST token (e.g. buying a Sparkle kit),
every `>0` free entry vanishes from the menu while the base cost-gated catalog stays. The gate was
also redundant: the exchange station only exists during the start sequence (SC_MainSCRIPT places it
and deletes it in Clean()), so "offer only during the start" is guaranteed by the station's
lifecycle, not the condition. **Fix: Conditions cleared to empty on ALL 1433 kit entries AND the 6
weapon entries in `Authoria - Patch - New Weapons - Requiem.esp`.** Verified: a `Conditions exists`
query over both plugins returns 0.

## "Closet Kit" (000D99–000D9B)

One STARTER KITS-tab entry named **Closet Kit** that grants all 42 outfit pieces in one craft,
cloned from the Sparkle-kit pattern in `Authoria - Initialization - Starting Choices Tweaks.esp`:

- `A_SCK_ClosetKitItems` (LVLI, UseAll, ChanceNone 0): the 42 outfit pieces, Level 1 Count 1 each.
- `A_SCK_ClosetKit` (MISC "Closet Kit", large-sack model, Value/Weight 0): keywords
  `StarterKitKeyword` + `StarterKitPhysical` (files it into the STARTER KITS crafting-menu section
  per the CraftingCategories config), script `StarterKitEquipScript` (the Starter Kits addon's
  compiled pex, reused — Kit→self, StarterKitItems→the LVLI). On pickup it unpacks into the player's
  inventory and removes itself.
- `A_SCK_Recipe_ClosetKit` (COBJ): CreatedObject = the kit MISC, 0 cost, no conditions.
- Description Framework text in `Authoria - Starting Kit_DESC.ini` (this folder).
- New master: `Starter Kits - Starting Choices Addon.esp` (the two keywords + the script ship there).

## Entry roster (1433 as first built; see the 2026-08-28 expansion below)

**Original 80** (EditorID prefix `Authoria_SC_Kit_`): the 42 previous-Wheeler outfit pieces
(union of `_tools\outfit-wheeler\outfits.known-good.json` and the pre-2.8 `PrismaOutfitWheel.json`
backup — they differ only in "heavier romper") + Vindicator 14 + DDV Arcane Fencer 20 + Fuse00
backpack 4.

**Expansion 1353** (EditorID `A_SCK_<TAG>_<localID hex>` — the suffix IS the item's local FormID):
full playable ARMO/WEAP catalogs of every user-added armor/weapon mod, found by (a) enabled-state
diff DEEZ CS NUTZ vs Main Profile (the delta-backup method) and (b) the masters of the
`Authoria - Reqtificated - *` armor patches (catches early-wave mods enabled in both profiles).
Deduped against the original 80; 0 unnamed and 0 NonPlayable-flagged records found.

| Tag | Mod (plugin) | Entries |
|---|---|---|
| MM | Modular Mage | 377 |
| SER | Sera's Armor | 248 |
| FUR | FurArmorSet (keung) | 224 |
| H2P | H2135 Pirate Series2 (43 armo + 10 weap) | 53 |
| WCH | Witchy Lore-Friendly Accessories | 52 |
| ELV | Elmlock Color Variants | 43 |
| ATN | Adventurer's Tunic | 34 |
| FVO | DD FVO Cloth (31 armo + 1 axe) | 32 |
| COR | Corsican Raider | 31 |
| VJ1 | DD Vergi jewelry I | 25 |
| SYN | Shining Nikki feathersuit | 21 |
| EWD | DD Einar Wardrobe | 19 |
| SIG | Sigrin Silver Fox | 18 |
| VJ3 | DD Vergi jewelry III | 18 |
| RGM | Roaming Girl's Attire Modularized | 18 |
| VJ2 | DD Vergi jewelry II | 16 |
| RBS | RB's Scout | 13 |
| CVD | Adventurers Magical Bag (CVDN) | 11 |
| VWA | DD Vergi Armoury (2 armo + 8 weap incl. Einar Bow, Sydona Staff) | 10 |
| NIB | Nibenean Strider | 10 |
| BMA/BMS | BIMDO Armor + Separated | 16 |
| TRM | Traveler's Romper | 8 |
| FAD | Fuse00 Adventurer Armor | 8 |
| RGA | Roaming Girl's Attire (base) | 7 |
| HEL | Fuse00 Helga | 7 |
| ELM | Elmlock base (5 armo + Elmlock Blade) | 6 |
| MAC | Mac's Socks | 5 |
| GTR/GTO | Girl's Travel Outfit + Recolors | 8 |
| BNY | Bunny Slippers | 5 |
| DAI | DA Isabella (4 armo + dagger) | 5 |
| MDO | Mage's Daily Outfit Separated | 4 |
| DBL | Dibella's Grace | 1 |

## 2026-08-28 expansion: +129 entries (1434 -> 1563)

Added with the same pattern (COBJ on `SC_ExchangeStationKWYD`, no Items, **no conditions**),
FormIDs 000D9C-000E1C. Highest local FormID is now 0xE1C against the ESL ceiling 0xFFF, so ~480
slots remain. Masters 47 -> 49.

| Tag | Mod (plugin) | Added | Tag total |
|---|---|---|---|
| SER | Sera's Armor 1.4 - the 90 new armors (thighguards, chain + buckled pauldrons, simple chestguard, kneepads 2/3, Isabela choker + pauldron, simple tops, belt bag 2, arm guard metals, two flats, the 32 "Repaired" dress/sundress variants) | 90 | 338 |
| LIL | LDD - Lili Collection (Lilac and Gooseberries + Toussaint Meadow, all 33 pieces) | 33 | 33 |
| KAT | Katari Armor (Xtudo plugin: 3 armored + 3 clothing variants) | 6 | 6 |

Nothing was excluded: all 129 candidates were named and none carried the NonPlayable flag.

Re-audited after the write: **0 entries carry conditions**, and the editorid-suffix ==
item-local-FormID invariant holds for every `A_SCK_*` catalog entry (the only name that does not
follow it is `A_SCK_Recipe_ClosetKit`, which never did - it points at the kit MISC).
check_errors clean: 0 dangling, 0 missing masters.

Session record: `MODS-ADDED-20260828-ARMORS-COLLISION.md`.

## Deliberately NOT included (decisions to revisit on request)

- **Ninirim Collection, NINI Open Waist, Cute Adventurer, all 4 Caenarvon Cosplay packs, both
  Sonders Cosplay addons** — user instruction ("exclude ninirim & cosplay"); their outfit-config
  pieces ARE in via the original 80.
- **Wig/hair packs** (Tullius Wigs, Fuse00 hairpacks, Dint999, Evg Modular Wigs, takuya) — judged
  "not armor"; only the outfit-config Swan wig is in.
- **Skyrim Arrow Overhaul** quivers/arrows — ammo pack; only the outfit-config Dwemer Quiver is in.
- **Sanguine's Trade Brenna/Vesyra outfits, An Evening With Angi** — NPC-replacer outfit plugins.
- **Authoria - Lucien Traveler Outfit** — follower-specific authored clones of Girl's Travel Outfit.
- The 4 curated weapon esps (kopis/witcher/chef) — already offered by the weapons patch's 6 entries;
  the "_s" scabbard twin stays skipped (duplicate menu name).

## Traps

- Adding/removing this ESL shifts light indexes → Wheeler rawIDs die
  ([[wheeler-rawids-die-on-esl-change]]). Run the calibrate/reindex before launch after toggling it.
- Disabling any of the 44 item-source masters breaks the plugin (missing master); check_errors names
  the offender.
- COBJ-only: not Reqtificator-relevant; no rerun required by THIS plugin.
- The exchange-station menu is now VERY long (1433 + curated base entries). Crafting-menu search
  (SearchUI is installed) filters it by name.
- Generation pipeline (for refreshes): `scratchpad\kitgen\build_kit.py` + chunked
  housecarl_bulk_create into this esp; audit with `audit_kit.py` (regenerate the dump query first).
