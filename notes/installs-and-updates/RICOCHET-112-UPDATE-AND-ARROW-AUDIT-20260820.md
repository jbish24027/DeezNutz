# Ricochet 1.1.2 Update + Arrow Adjustments Audit — 2026-08-20

## 1. Update installed

- RicochetFramework 1.1.1 → **1.1.2** (Nexus mod 160603, file "Ricochet Framework - Latest Version", 2026-08-16).
- DLL-only update: `RicochetFramework.ini` is byte-identical between 1.1.1 and 1.1.2 (verified with fc). DLL 2,875,904 → 2,889,216 bytes; PDB 47,517,696 → 47,714,304 bytes.
- Replaced in place: `mods\RicochetFramework\SKSE\Plugins\` (MO2 was closed). INI left untouched.
- meta.ini updated: modid=160603, version=1.1.2, installationFile → the new zip.
- **Rollback**: the original 1.1.1 zip was gone from Downloads, so the installed 1.1.1 files were zipped first:
  `C:\Users\User\Downloads\RicochetFramework 1.1.1 (installed-files backup) 2026-08-20.zip` (3 entries, 50,400,568 bytes total — matches 1.1.1 sizes exactly). Restore = extract over the mod folder.
- 1.1.2 changelog (relevant to this stack):
  - Unified collision pipeline + projectile collision/processing fixes.
  - **Bound Arrow exclusion support** — SAO adds Bound Arrow / Bound Bodkin Arrow; conjured arrows should no longer be physicalized/retrievable.
  - **Accurate Projectile Collision API support** — APC is live in this order since 2026-08-18.
  - Impact/sound effect reliability in unloaded cells.
- Companion versions checked live on Nexus: **Broken Feathers 1.0.1 = current** (no update paired with 1.1.2), **Skyrim Arrow Overhaul 1.3 = current** (latest file 2023-11-28).
- The Ricochet stack (RicochetFramework, Broken Feathers, SAO, ALD, the patch) is enabled **only in the DEEZ CS NUTZ profile**.

## 2. How arrow breakage works (mechanism, verified from files)

- Fracture is **opt-in per exact AMMO FormID** via JSON packs in `SKSE\RicochetFramework\`. Only one pack is installed: Broken Feathers (`...\BrokenFeathers\Arrows\*.json`).
- Broken Feathers maps exactly **18 vanilla ammo types** (Daedric/Dragonbone/Draugr/Dwarven/Ebony/Elven/Falmer/Forsworn/Glass/Iron/NordHero/Nordic/Orcish/RieklingSpear/Stalhrim/Steel arrows + Dwarven/Steel bolts). Mapping = FractureMapping (filter `Ammunitions` by FormID → `Fracture: true`) + AmmoMapping (AmmoBase → AmmoBroken MISC template, Durability, BrokenStates with bent/head/tail ProjectileSwap).
- JSONs are **FormID-keyed** (`Skyrim.esm:0x...`), so our AMMO overrides don't unhook them (EditorID-rename trap does not apply).
- Broken items are **MiscItems** (BF_*Broken_Ammo), not AMMO → the Reqtificator/Requiem never rebalances them and they can't be fired. Runtime naming: `%s [broken]` from the live arrow name; price ×0.5, weight ×0.5; reforgeable (`bAmmoCanBeReforged=true`).
- **Anything unmapped** takes `[Fracture] iDefaultRecoveryChance = 50`: vanilla-style 50% unrecoverable, no broken visuals, no pieces. It is impossible by construction for an unmapped arrow to show a wrong/generic broken model.
- FractureExclusion.json disables fracture vs one material and 8 hit-object bases (practice-target class objects).
- Base.json adds break sound (BF SNDR 0x801) + wood-chip impact effect to all fractures.

## 3. Special-tip arrows — current handling (the question asked)

- SAO defines **74 ammo records** (bodkin/broadhead/crescent/hammerhead per material, fire/frost/shock, whistle, baskethead, bomb bolt, practice, silver, stone, Auriel's blood, bound bodkin…). **None are in any fracture pack** → none ever appear broken; they take the 50% default-recovery path instead.
- This matches the deliberate deferral recorded at integration time (session 4 ledger: "BF fracture JSONs for AO's 74 arrows (50% default recovery meanwhile)").
- Consequence check (still true today):
  - No wrong-tip broken model can appear anywhere.
  - Plain vanilla arrows are effectively cheaper to sustain (pieces reforge ~losslessly) while special tips eat a flat 50% attrition — acceptable since tips are the premium, Requiem-gated ammo.
- **Optional upgrade (not built)**: a JSON-only "Authoria" pack mapping each special-tip arrow to its material's existing BF broken pieces (reuse BF MISC + bent projectiles; one AmmoMapping entry per arrow, own ID, AmmoBase = the SAO arrow). No plugin slot needed. Broken name auto-generates from the real arrow name ("Iron Bodkin Arrow [broken]"). Reforge would return **plain** arrows of the material (tip lost on break — recraft tips via SAO recipes). Exclude: fire/frost/shock/whistle/bomb/baskethead (mechanisms/explosives), bound (now excluded by the framework), Auriel's, practice.

## 4. Audit of the Requiem arrow patch (live, post-Reqtificator-08-19)

- Patch `Authoria - Patch - Skyrim Arrow Overhaul - Requiem.esp`: 311 overrides — 105 AMMO, 101 COBJ, 101 PROJ, 3 GMST, 1 AVIF.
- **308/311 win.** The 3 losses are exactly the planned Reqtificator inputs: dunGeirmundSigdisArrowsIllusion, DwarvenSphereArrow, DwarvenSphereBolt02 — RFTI rescales ×4 from our vanilla inputs (verified live: sphere arrow 20 → 80) and keeps the SAO head keyword (005908). Working as designed.
- GMSTs verified live in the winner: fAutoAimMaxDegrees3rdPerson=0, iArrowInventoryChance=0, fAttachedArrowAgeMax=40 (deliberate SAO/Ricochet synergy).
- Broken Feathers recipe bug-fixes verified live as winners:
  - BF_DragonboneArrow_Recipe: input corrected BF_IronBroken (0x80C) → BF_DragonboneBroken (0x803).
  - BF_NordicArrow_Recipe: input corrected BF_DaedricBroken (0x802) → BF_NordicBroken (0x80E).
- All 88 Broken Feathers records: only those 2 recipes are overridden (by us); everything else wins untouched.
- Reqtificator rerun required by the integration **has happened** (RFTI output 2026-08-19 13:47 > patch 2026-08-14) and included the arrow stack (RFTI records reference SAO forms).

## 5. FINDING — leveled-list merge did not materialize

- Expectation from the 08-14 integration: the Reqtificator rerun "merges AO's 123 leveled-list versions so AO arrows enter loot/vendors".
- **Live truth**: RFTI contains **zero** overrides of vanilla-defined leveled lists. Its 1102 LVLI touches are all lists defined in Requiem.esp (1005) / WAR (72) / VampireCollection (25) — its own distribution rebuild. No RFTI list references SAO forms (spot-checked the iron variants sub-list 12B3F7).
- Of SAO's 158 LVLI overrides: **53 win** (lists Requiem doesn't touch — e.g. LootBanditArrows100, LootDraugrArrows100/15, BaseArrowDraugr75, BaseArrowFalmer75, BaseArrowForsworn75) and **105 are buried by Requiem.esp** (e.g. the eight BaseArrow<material>75 pools, LootBanditArrows15) because the AO cluster deliberately loads before the Requiem stack.
- Example (BaseArrowIron75): vanilla = Iron Arrow; SAO = its variants sub-list, ChanceNone 0; Requiem (winner) = Iron Arrow, ChanceNone 0.25. No merge exists.
- **Net in-game effect**: special tips reach the world via SPID-equipped NPCs (SAO_DISTR.ini), the 53 winning lists, and crafting. The 105 Requiem-won lists hand out plain arrows per Requiem.
- Options:
  - A) Accept — Requiem-pure loot in those pools; tips still circulate via the other channels. Zero work.
  - B) Extend the patch with hand-merged overrides for the meaningful subset of the 105 (SAO sub-list + Requiem chances) so tips appear in general loot too. Records job via the bulk workflow; patch position (above Requiem, RFTI doesn't touch these) makes our versions final winners. Needs an explicit go-ahead.

## 6. In-game test list (CS profile)

1. Plain arrows (iron/steel): shoot stone at a hard angle — expect snap sound + bent/broken pieces; " [broken]" pieces in inventory; reforge 5 pieces at a forge.
2. Special tips (any bodkin/broadhead): confirm they never show broken pieces; stuck ones pull out intact or vanish (~50%).
3. Bound bow: fire bound arrows — expect no lingering retrievable world arrows (new 1.1.2 exclusion).
4. Dragonbone + Nordic reforge recipes: confirm they consume their own material's broken pieces.
5. General feel vs APC: point-blank and near-wall shots should register cleanly (new unified pipeline + APC API).
