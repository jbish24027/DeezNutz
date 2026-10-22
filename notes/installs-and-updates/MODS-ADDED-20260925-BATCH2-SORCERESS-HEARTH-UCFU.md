# Mods added 2026-09-25 (batch 2): Ufok Sorceress Attire set, High Quality Hearth PBR, Upper Class Furniture Upgrade

Installed by Claude with MO2 closed. Six archives from Downloads. Per-file backups of every profile file: `*.bak-batch2-20260925` (placement) and `*.bak-batch2b-20260925` (the Requiem patch plugin). Extra backups: `_backups\2026-09-25 - Sorceress Attire batch\`.

## What went in

| Mod folder | Nexus | Version / file | Enabled in | Placed |
|---|---|---|---|---|
| Ufok Sorceress Attire | 191276 | 1.1 / 806230 | all six | directly above `Shanoa Armor - UBE` |
| Ufok Sorceress Attire - UBE | 191276 | 1.0 / 803645 | all six | above the main mod |
| Ufok Sorceress Attire - Skirt Fix | 191276 | 1.31 / 806613 | all six | above the UBE mod |
| Ufok Sorceress Attire - PBR 4K | 191276 | 1.0 / 803635 | DEEZ CS NUTZ - PBR only | top of the stack |
| houseCARL - Authoria - Reqtificated - Sorceress Attire | (authored) | ESL, 6 ARMO overrides | all six | above `houseCARL - Authoria - Reqtificated - Armor Folder` |
| High Quality Hearth - 3D Farmhouse Firepit - PBR | 190237 | 1.2 / 804396 | DEEZ CS NUTZ - PBR only | directly above the 1.1 non-PBR mod |
| Upper Class Furniture Upgrade - 4k | 192991 | 1 / 810306 | all six | directly above `The Royal Seat - AIO` |

Plugins (all six profiles, all ESL-flagged, full-plugin count unchanged):
- `ufokSorceress.esp` after `Shanoa Armor.esp`, group Gameplay - Armors and Weapons.
- `ufokSorceress UBE patch.esp` after `Shanoa Armor UBE patch.esp`, group Visuals - Character Visuals.
- `Authoria - Reqtificated - Sorceress Attire.esp` after `Authoria - Reqtificated - Shanoa Armor.esp`, group Authoria - Reqtificated. Loads after both its masters and before Requiem for the Indifferent.

## Ufok Sorceress Attire (the outfit)

- FOMOD choice: the Clothing plugin. It is a mage outfit and the list's Requiem convention keeps cosmetics as Clothing. The Light Armor plugin and its Nexus fix were not installed.
- The 3BA/CBBE archive ships no built outfit meshes. Only the 3BA BodySlide set was installed. The CBBE set writes the same output paths as the 3BA set and this list runs 3BA plus UBE, so it was left out.
- The UBE archive is a native UBE lane: six `SorceressXxxAA_UBE` armor addons for the UBE races only, world models under `meshes\!UBE\Ufok\TSorceress\`, and overrides of the six ARMO records that add those addons. Its BodySlide set ("ufokSorceress UBE 2.0") outputs to `meshes\!UBE\ufok\TSorceress\`. The installed body is UBE 2.0 (update 0.7). The reference body inside the outfit set is the UBE 2.0 body shape with the `!UBE` texture paths.
- Both skirts point at `meshes\Ufok\TSorceress\Skirt.xml`. The Skirt Fix 1.31 replaces that file and its CBBE twin with a corrected bone list. FSMP 3.5.0.0 is installed.
- Ground objects reference the outfit's `_m` masks plus `ore_iron_e` / `ore_gold_e` cubemaps.
- The crafting book (Book of Sorceress Attire) is placed in seven cells (College of Winterhold starting room and court wizard rooms per the author). Recipes need the book, leather and leather strips at a forge.

### Requiem convention patch

`Authoria - Reqtificated - Sorceress Attire.esp` forwards the six ARMO records from the UBE patch (so the UBE armatures stay) and applies the list's clothing table: body value 20 weight 1 (was 150 / 2), hood, hood without hair, boots, gloves, skirt value 10 (were 60). Two author slips fixed: the gloves carried ClothingFeet (now ClothingHands), the skirt carried ClothingFeet (dropped). It also forwards the two UBE armor addons that carry first-person models (body, gloves) and repoints their first-person meshes from the vanilla-lane `Ufok\TSorceress\` files to the `!UBE\Ufok\TSorceress\` files, so a UBE player sees the UBE body and hands in first person instead of the 3BA skin (the same defect the converter had on the crop top). Masters: Skyrim, Update, UBE_AllRace, the outfit esp, its UBE patch. Light-flagged; the flag survived houseCARL's later rewrites. Armor type Clothing and rating 0 were already right, so the Reqtificator's armor transformers do not fire on these records and the plugin should not become a master of the Reqtificator output (225 masters today, cap 254).

## High Quality Hearth PBR 1.2

- The archive ships only PBR textures, the eight PBRNifPatcher jsons and two meshes that still reference the 1.1 texture names. The 1.1 mod stays enabled directly below and supplies those textures.
- `farmintlhfirepit03.nif` is byte-identical to 1.1. `farmintlhfirepit02.nif` is new in 1.2 (the second inn and hall pit) and stays shadowed by `Authoria - PG Output - PBR` until the next PGPatcher run, because the output holds a patched copy of the Assorted Mesh Fixes mesh from 2026-08-28.
- Nothing changes visibly before that run. After it, the PBR profile gets the 3D pit in the 02 placements (Moorside Inn, Highmoon Hall, the White Hall, Dawnstar houses, Gala's Stead and others) and PBR shading on the inn hearths.
- No emissive shapes, so the Embers-white problem cannot hit these meshes. Nexus also has a non-PBR 1.2 (file 804395) for the other profiles; not installed.

## Upper Class Furniture Upgrade - 4k

- 16 meshes, 9 textures. Winner scan across all enabled mods in the PBR and DEEEZ NUTTZZZ profiles:
  - Placed above `The Royal Seat - AIO`, so it now wins the three benches from that mod and everything else from Weathered Furniture - Common and Rally's Upper Furniture. Swap the two lines to give the benches back to The Royal Seat.
  - Still outranked on purpose: `Rally's Jorrvaskr Carpetry` (the jarl-table cloth), `Lux (main) - rerun` (the jarl table `uppertable01custom01`), and in the PBR profile the eleven patched copies inside `Authoria - PG Output - PBR` (cupboard, dresser, both end tables, table01, table01custom01, both table benches, wardrobe, chest, nightstand) until PGPatcher is re-run.
  - Benches, shelves, square table and the cloth are visible immediately in the PBR profile; the rest after the PGPatcher run. The non-PBR profiles see the whole set now.
- All meshes except the cloth carry collision. The vanilla furniture records still point at these model paths (no plugin repoints them). Not covered by the mod: chair, nightstand, chest, round table, bed.

## Not done / caveats

- No BodySlide build was run (never mine to run). Until the user builds both groups the outfit has no meshes and is invisible when worn.
- No PGPatcher run (never mine to run). The PBR firepit, the PBR outfit textures and eleven of the furniture meshes wait on it.
- UBE 2.0 vertex parity between the outfit's reference body and the installed body was not measured; the version and texture paths match. Look for neck and wrist seams on the first wear.
- The Lux and Jorrvaskr Carpetry copies of the jarl table and its cloth were left winning; the jarl table keeps its old look under the new set.

## Owed by the user

1. BodySlide: build group "Ufok Sorceress Attire 3BA" into the 3BA output and group "UfokTravelingSorceress UBE 2.0" into the UBE output.
2. PGPatcher for the PBR profile (hearth 02 pit, PBR outfit textures, furniture set).
3. Read the Nexus book placement or craft at a forge with the book in the inventory.

## Update 2026-09-25 evening: Upper Class Furniture Upgrade - 4k 1.1

Nexus 192991 file 1.1 (changelog: "Fixed collision mesh and disabled vertex colors flag on uppershelf02"). CRC diff against the installed 1.0: one file changed, nothing added or removed. Applied in place with MO2 closed: `meshes\clutter\upperclass\uppershelf02.nif` replaced (CRC 1BCB76A0 verified), meta.ini set to 1.1 with the new archive name. Backups in `_backups\2026-09-25 - UCFU 1.1 update\` (the 1.0 mesh and meta.ini). The shelf is not among the eleven meshes shadowed by the PG output, so the fix is live in the PBR profile without a patcher rerun.
