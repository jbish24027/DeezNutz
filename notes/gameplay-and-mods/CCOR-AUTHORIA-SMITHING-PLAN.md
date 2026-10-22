# CCOR → Authoria smithing plan (research + build plan)

Date: 2026-08-16. Profile analysed: `Authoria - Requiem Reforged - Main Profile`. Status: PLAN ONLY. Nothing in `C:\1. AUTHORIA` was changed. No MO2, game, LOOT, Reqtificator or Synthesis was launched.

Inputs examined: CCOR 2.6.4 (esp + BSA + all 37 script sources), CCOR SSEEdit Scripts 2.6.3.1 (both .pas), kryptopyr's Patch Hub 4.4.1 (all 55 CCOR patch plugins), the CCOR Nexus page/changelog/forum, articles 1467/1468/1469, the "Guide to Crafting Conditions" Google Sheet, mod 19246, mod 19518, mod 61015 (Honed Metal), Requiem.esp + addons in the Main profile, Requiem.bsa scripts, Go To Bed scripts, Honed Metal scripts, the COCKS/CraftingCategories config, and the Main profile plugin census.

Working data (FormID lists, JSON dumps, decompiled scripts) is in the session scratchpad: `C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\88b31957-faaa-48b3-9dd8-68d16673496b\scratchpad\` (`ccor_scan.json`, `agentA\`, `agentB\`, `agentC\`, `decomp\`). Copy it out if you want to keep it; it is session-scoped.

---

## 0. Read this first

### The short verdict

1. Removing WACCF from CCOR is cheap. Only 96 field references in about 40 records point at WACCF forms. The 98 `WAF_` keywords CCOR uses are injected into `Update.esm` space (`01AF01xx`) and CCOR ships its own copies. They work without WACCF.
2. Running CCOR "as a mod" under Authoria is expensive. 481 of CCOR's 487 vanilla recipe overrides collide with Requiem. 39 of them would resurrect recipes Requiem deliberately disabled (Requiem nulls 111 in total). CCOR's silver, tempering, XP and unique-item systems contradict Requiem. Its crafting-menu category tokens duplicate the COCKS categories Authoria already runs. Its ore-vein script fights the Requiem/Go To Bed script and the ParallaxGen/skymoji vein records.
3. The right shape is a curated, ESL-flagged "Authoria Smithing (CCOR-derived)" layer. Keep CCOR's additive content and mechanics. Drop its vanilla overrides. Let Requiem own balance. Let COCKS own the menu.
4. Both custom features are independent of CCOR. Mining XP by ore rarity is a script job (Papyrus). Player-crafted +20% needs a small SKSE plugin to be done properly. A Papyrus-only version exists but has a real data-loss hazard.
5. Two things must be re-run by you after any build: the Reqtificator (the current `Requiem for the Indifferent.esp` even masters CS-profile-only plugins, so Main needs a fresh run anyway) and, only if ore-vein records are touched, ParallaxGen. The plan avoids touching vein records so PG can stay as is.

### Decisions log (answered 2026-08-16 by the Authoria authors)

1. Distribution: Authoria is a published Wabbajack list. Packaging must be distro-safe. LOCKED: Option A (unmodified CCOR from Nexus + our own empty stub master + our ESL patch layer + our own loose scripts). No modified CCOR.esp, no CCOR assets copied.
2. Scope: Curated was chosen first. Under discussion since Aaronavich proposed "mechanics package + a CCOR-inspired recipe complexity pass" (no CCOR install). That is written up as Option D in section 6B. Decide A-Curated vs D.
3. Menu: keep the current COCKS categories as the filters. CCOR's token filters are disabled by the patch. LOCKED.
4. Breakdown: keep Requiem/Authoria recycling as it is. CCOR breakdown recipes are disabled by the patch; PRUFEI stays inert. LOCKED.
5. Player-crafted bonus semantics: OPEN (head-start temper vs permanent). See section 6.2 and the comparison in section 6.5. Everything else can proceed while this is decided.
6. Tools: see section 12. Nothing to buy. Two optional Nexus downloads and one network fetch by me.

Consequences of the locked decisions:

1. CCOR.esp stays a full plugin (about 3880 records; cannot be compacted while unmodified). One full slot. Stub and patch are ESL. Main has about 55 free full slots.
2. The CCOR MCM keeps its pages. Options for filters, breakdown, tempering tweaks and leveled items become no-ops because the patch disables the recipes and overrides the global defaults. This is cosmetic clutter, accepted for distro safety.
3. The CCOR Compatibility Script (xEdit) is not needed. Requiem and mod recipes get no CCO conditions because the COCKS categories are the filter.
4. All curation is done as override records in the ESL patch (overrides do not count against the 4096 new-record limit).
5. Asset and record use (confirmed with the authors 2026-08-16): our patch masters CCOR.esp and may override or reference any CCOR record and point new records at CCOR's meshes/textures by path, because CCOR ships in the list from Nexus and its BSA loads with its plugin. Nothing from CCOR is copied. The line not crossed: CCOR's own files (esp, BSA, scripts) are never modified, because Wabbajack would ship those as binary patches of CCOR's archive. The stub master is still needed because the WACCF dependency lives inside CCOR.esp's header. Our vein script is our own implementation that reads CCOR's globals; it does not reuse CCOR's script text.

---

## 1. What CCOR is (as measured)

Plugin `complete crafting overhaul_remastered.esp` (v2.6.4, HEDR 1.70, full ESP, not ESL-flagged).
Masters: Skyrim, Update, Dawnguard, HearthFires, Dragonborn, USSEP, WACCF.
5243 records in 26 types.

Record ownership:

| Class | Count | Meaning |
|---|---|---|
| New (CCOR FormIDs) | 3613 | CCOR's own content |
| Injected (`Update.esm` space, `01AF…`/`01CC…`/`01DE…`/`01E8…`) | 267 | Shared "API" records other mods can reference without mastering CCOR |
| Overrides of vanilla/DLC/USSEP/WACCF | 1363 | Records that will collide with Requiem |

By type (new / injected / override):
COBJ 1846/23/487 · ARMA 561/0/57 · ACTI 0/0/583 (all ore veins) · GLOB 197/199/8 · ARMO 324/0/28 · MISC 203/15/60 · LVLI 227/9/30 · KYWD 2/7/98 · FLST 75 · REFR 49/1 · TXST 44/3 · WEAP 39/0/2 · PERK 22/3/2 · MESG 13/4 · plus BOOK 1/0/3, CONT 3/1, INGR 0/2, LIGH 1/0/1, CELL 1/0/1, FURN 0/0/2, OTFT 0/0/1, QUST 2, MGEF 1, SPEL 1, STAT 1.

What the 1846 new recipes are: 465 breakdown, 274 jewelry/circlet/gem, 257 crafting-menu tokens, 162 tempering for CCOR items, 119 smelter, 75 tanning, 46 replicas, 33 unenchanted faction gear, 415 "missing" recipes for vanilla items (Blades, bandit, Companions, Falmer, Forsworn, guard, Nightingale, Skyforge, Draugr, silver, arrows, tools, torches, lockpicks, learning tokens).

BSA: 1495 files. 900 meshes, 100+ textures, 37 scripts with sources, 9 translations, SEQ.

How it works:

1. Every recipe carries `GetGlobalValue CCO_… == 1` conditions. 8514 such conditions exist. The MCM flips the globals. This is how filters, "recipe origin" toggles, complexity, and options work. Recipes without CCO conditions always show, so unpatched mod recipes leak into every filter view.
2. Menu filters are recipes that create token items with keyword `CCO_MenuCategory`. Crafting a token runs a script that flips category globals. This is not SkyUI-specific.
3. Smithing XP: while the player sits at a forge/smelter/tanning rack, a perk (`CCO_SmithingXPMultPerk`, ModSkillUse ×0) zeroes engine XP and the script awards XP itself: `(3 × value^0.65 + Flat) × rate × bonuses`, or the alternate formula (`+ ((value/3 × 53)^0.5) × 3/2/1` for the first three crafts). Detection is `OnItemAdded` with no source container while seated. It needs the crafting furniture animation.
4. Mining: CCOR's own `MineOreScript.pex` reads its injected globals through `Game.GetFormFromFile(0x01CC0xxx, "Update.esm")`. It grants a flat `CCO_MiningSkillIncreaseGV` (01CC0450) per drop. It needs the 583 ACTI overrides only for per-vein flags (Stalhrim, geode, shellbug, Hearthfire clay/stone) and to point veins at CCOR's gem list.
5. Breakdown recipes are protected by PRUFEI: favourited items are mirrored into a hidden chest; recipes check that chest. The mirror loop walks the whole inventory when you favourite something.
6. Runtime record edits: `SetWorkbenchKeyword` on formlists of recipes to disable them. Those lists are empty in 2.6.4. One USSEP recipe is disabled at runtime.
7. Mod detection by `Game.GetModByName` for CACO, Campfire, Cloaks, IA/IW, Bruma etc.
8. Tempering/enchanting "adjustments" are ModTemperingHealth ×0.5–0.95 tiers by item type. Silver/gold armour perks. Unique-item level-up swaps (Chillrend 001→005 etc.).

Permissions (README): no re-upload, no collection packaging, no asset reuse without permission. Keywords, globals, conditions and "other functions needed for compatibility" may be included in other mods. Patches are allowed. This matters for decision 1.

---

## 2. The WACCF dependency, exactly

Direct references to WACCF forms: 96, in these records.

| CCOR record(s) | What points at WACCF | Fix without WACCF |
|---|---|---|
| 10 vanilla circlet ARMO overrides (`JewelryCirclet_*`, 0166D6…016731) | `MODL` → WACCF circlet ARMAs (062E8659…062E8662) | Drop the overrides. In Authoria these records are already won by `JS Vanilla Circlets - Requiem patch.esp`. |
| 12 new ARMO (`DBArmorHelmet*NoEnch_CCO`, `ArmorThievesGuildVariant*_CCO`, `ArmorStormcloakGeneral*_CCO`) | `MODL`/`MO2S`/`MO4S` → WACCF ARMAs and texture sets | Repoint to vanilla ARMAs where a vanilla equivalent exists (DB helmet). Delete the mask-less DB hood, TG variant helmet 02, TG sleeveless cuirass and Stormcloak general variants (WACCF-only meshes). |
| 12 COBJ (`DLC1RecipeArmorVampireCirclet_CCO`, `DLC1TemperArmorSeranaHood_CCO`, `BreakdownDLC1ArmorSeranaHood_CCO`, `RecipeArmorIronHelmetAlt*`, `RecipeArmorDraugrHelmetAlt*`, `Breakdown*HelmetAlt_CCO`, `RecipeArmorIronAltCirclet_CCO`, `RecipeArmorIronHelmetAltBYOH_CACO`) | created object / ingredient = WACCF items 061730E2, 061730E7, 062E8557 | Delete these recipes. |
| LVLI `WACCF_NewItems` (074727C8) | 29 WACCF items | Delete the list. Nothing else needs it. |
| LVLI `DLC1LItemGuardCrossbowAndBolts_CCO` (070CE1CC) | 062E856F | Repoint to vanilla DLC1 crossbow/bolts or delete. |
| 5 LVLI overrides of WACCF-defined lists (`DLC1LItemVendorCrossbow_CCO`, `…CrossbowBolts_CCO`, `…WeapGuardRangedCCO_PRIMARY`, `…WeapImperialRangedCCO_PRIMARY`, `LItemBuckles_CCO`) | records live in WACCF | Delete the overrides. |
| 5 COBJ overrides of WACCF recipes (`TemperArmorExecutioner*_WAF`, `TemperArmorDBCuirassShortSleeve_WAF`) | records live in WACCF | Delete the overrides. |
| ARMA `ThievesGuildLeaderCuirassSleevelessAA_CCO` | `MO3S` alt texture 06108BA1 | Remove the alternate texture entry. |
| QUST `CCO_MCMStartupQuest_V2` script property `FistsOfSteel_Light` | WACCF perk 062BAA05 | Null the property. Remove the "Fists of Steel affects light armour" MCM toggle in the edited MCM script. |

Not a dependency: the 98 `WAF_*` KYWD records. They are injected `Update.esm`-space forms and CCOR carries them. Only 8 references go to USSEP (Blackreach vein messages) and USSEP is in Authoria.

Hidden dependency: CCOR's 1363 overrides were authored on top of WACCF's versions of vanilla records. In Authoria those records are won by Requiem, its patches, JS Circlets, LOTD, USSEP or the Reqtificator (checked record by record, section 4.6). So the WACCF-flavoured data in CCOR's overrides never reaches the game as long as CCOR loads before Requiem. Under the recommended architecture those overrides are deleted anyway.

Conclusion: a no-WACCF CCOR is about 60 record edits. It is not the hard part.

---

## 3. What "CCOR" would collide with in Authoria (measured)

### 3.1 Recipes (COBJ)

1. Requiem.esp touches 2263 recipes: 1191 new, 1072 overrides. Its patches (Weapons and Armor Redone, Magic Redone, ATweaks, New Legion, Alchemy Redone, Sons of Skyrim, Trad S&S, USMP, Minor Arcana) win a further 184 of them.
2. 481 of CCOR's 487 vanilla recipe overrides are also overridden by Requiem (455 won by Requiem.esp, 16 by WAR, 8 by ATweaks, 1 New Legion, 1 USMP). The other 6 are WACCF-only or a Hearthfire trophy.
3. Requiem disables 111 recipes by setting the workbench to `REQ_DisableRecipe` (AD3B01:Requiem.esp) and renaming them `REQ_NULL_*`. CCOR overrides 39 of these (Elven light/gilded tempering, Miraak masks, Amulet of Articulation, Chillrend, Akaviri katana, Aetherial Crown, steel plate shield, steel boots/gauntlets B, and more). If CCOR wins, they come back.
4. Requiem gates recipes with `HasPerk` on the vanilla perk FormIDs. Requiem's tree (won by `Requiem - Reading teaches smithing perks.esp`): 0CB40D Craftsmanship, 0CB40E Dwarven, 0CB40F Elven, 0CB410 Orcish, 0CB411 Glass, 0CB412 Ebony, 0CB413 Daedric, 0CB414 Advanced Light Armors, 05218E Advanced Blacksmithing (Smithing ≥ 50, plate and jewellery), 052190 Draconic, 17B8BF:Requiem.esp Legendary Blacksmithing (artifacts), 309D25:Requiem.esp Arcane Craftsmanship (elemental ammo). CCOR gates 437 recipe conditions on 05218E (vanilla Arcane Blacksmith = temper enchanted/unique gear). Under Requiem that means "needs Advanced Blacksmithing", not "Legendary". These need re-gating.
5. Requiem drops the vanilla `EPTemperingItemIsEnchanted` + Arcane Blacksmith condition from tempering. CCOR forwards it. Any CCOR temper recipe kept for Requiem items must use Requiem's conditions.
6. Requiem already has 496 smelter (recycling) recipes, 104 tanning recipes, and its own MCM toggle `REQ_Skills_HideClutterRecipes`. CCOR's 465 breakdown recipes duplicate that. Requiem's Requiem-MCM "Recycling" switch exists.
7. 134 of CCOR's new forge/temper recipes create an item Requiem already has a new recipe for (silver sword/greatsword, hunting bow, long bow, headsman's axe, pickaxe, woodcutter's axe, 11 circlets, ingot bulk/scrap smelting, lunar weapon upgrades, Kahvozein's Fang temper). List: scratchpad `dup_ccor_requiem_created_objects.txt`.
8. CCOR's other "missing" recipes (Blades, bandit, Companions, Falmer, Forsworn, guard, Nightingale, Skyforge steel, Draugr, DB/TG unenchanted, replicas) have no Requiem counterpart. Requiem intentionally leaves many of these uncraftable. Each set is a design choice, not a merge task.
9. Fletching + `Authoria - Master Patch - Fletching Recipes.esp` (174 recipes) and CCE recipes (10, won by `Authoria - Reqtificated - Common Clothing Expansion.esp`) do not collide with CCOR but would need CCO conditions if CCOR's filters were kept.

### 3.2 Perks, silver, GMSTs, XP

1. `SilverPerk` (10D685) is `REQ_NULL_SilverPerk` in Requiem (effects emptied). CCOR overrides it and both silver swords (re-attaching `SilverSwordScript`). CCOR must not win these three. Requiem's silver is keyword-based and fixed at its own value; CCOR's silver slider would do nothing.
2. `DLC2StalhrimEnchanting` (026233) is Requiem's `REQ_Player_StalhrimEnchanting`. CCOR overrides it. Requiem must win.
3. GMSTs in Authoria: `fSmithingArmorMax` = 60, `fSmithingWeaponMax` = 60 (Requiem; vanilla 10). `fConstructibleSkillUseMult` = 0.5, `Exp` = 1, `Const` = 0 (Requiem; vanilla 3 / 0.65 / 25). AVIF Smithing: UseMult 1, ImproveMult 0.25, ImproveOffset 300. So Requiem's crafting XP is linear in item value. CCOR's script replaces it with a vanilla-shaped curve times a slider. Keeping CCOR's forge-XP takeover would silently change Requiem's smithing progression.
4. Requiem's smithing perks all carry `ModTemperingHealth` multipliers (1.6–2.0, Legendary +1.5). CCOR's tempering "adjustments" (×0.5–0.95 by item type) would stack on top. Keep them off.

### 3.3 Mining and ore veins

1. 621 `MineOre*` ACTI in the load order; 590 contested. Winners: `PG_1.esp` (ParallaxGen output, 550), `skymojibase.esl` (Oblivion Interaction Icons, 40; changes activate text), BSAssets/BSHeartland (Bruma veins), Extended Cut, Wyrmstooth, Olenveld. Requiem.esp touches none. All keep the vanilla `MineOreScript` and vanilla properties. Record-level: Stalhrim sets Strikes 2 / AttackStrikes 6 / Total 3.
2. The winning `mineorescript.pex` is the loose file in `Go To Bed - Requiem` (Main line 1265). It is Requiem's script (`ResourceCountTotal = 6`, USSEP fixes) plus Go To Bed's Cidhna Mine change (bed activation removed, only `SetStage(45)`). Requiem.bsa and USSEP.bsa also carry the script but lose to the loose file. `mineorefurniturescript.pex` comes from UOSC.bsa (an optimised recompile).
3. CCOR's `MineOreScript.pex` would replace all of that. Its default per-vein count comes from its global (MCM), not 6. Its Cidhna handling is the vanilla one (breaks Go To Bed's flow). Its Stalhrim/geode/Hearthfire flags need the 583 ACTI overrides, which lose to PG_1/skymoji unless PG is regenerated and a skymoji patch is written.
4. Ore items present: 10 vanilla/DLC ores, Heart Stone, CC Amber/Madness ore, Bruma Tin/Copper/Zinc/Meteoric Iron/Adamantium, Aetherium Ore (Tools of Kagrenac), Mithril Ore (Olenveld), Wyrmstone/Brimstone (Wyrmstooth). Requiem re-values Gold (100), Stalhrim (200/2 wt), Ebony sample, Amber. Full list: `agentB\ores_filtered.csv`.
5. No mod grants mining XP today. Experience.dll runs with `bEnableSkillXP=false` and no skill caps; skill XP rates are untouched.

### 3.4 Crafting menu

1. Authoria runs COCKS (`CraftingCategories.dll` 1.1.1, "Constructible Object Custom Keyword System") with the Authoria config `mods\Authoria - Crafting Catergories\SKSE\Plugins\CraftingCategories\Authoria - CraftingCategories.json` (sections Armour/Weapons/Exotic/Clothing/Jewellry/Backpacks/Factions/Fishing/Wigs/Lanterns; material categories keyed on vanilla and `REQ_ArmorSet_*` / `REQ_WeaponType_*` keywords) plus KID lines that create `AuthoriaCC_*` keywords. `Authoria - CraftingCategories.esp` is an empty carrier.
2. Vel'dun UI wins `interface\craftingmenu.swf` and `constructibleobjectmenu.swf`. SkyUI 6.11 is present. Menu look = Vel'dun over COCKS.
3. CCOR's token filters would appear as items inside COCKS categories. Its material/style filters duplicate COCKS material categories. Its recipes lack `AuthoriaCC_*`/REQ keywords only where they create CCOR-new items; those need KID lines or JSON entries.

### 3.5 Honed Metal (NPC crafting)

1. Mods present: Honed Metal 1.26.1 (DLL locked to 1.6.1170), Settings Loader, `Requiem - MR Honed Metal Patch.esp`, `Authoria - Patch - Honed Metal Speech Gate.esp`. Winning MCM settings: `Authoria - Honed Metal Rebalance\MCM\Settings\HonedMetal.ini` with `bSkillBasedSmithing=0`, `bNPCSkillRebalance=1`, `bNPCAbilityBoost=0`, `iNPCMinimumSkillLevel=15`, cost modifiers 2.0/0.4/1.0/2.0.
2. Mechanism: the player crafts in the vanilla crafting menu with the vendor's skill and perks temporarily swapped in (`HM_Actor.modifySkillLevel`, perk `HM_SkillControl` 000810:HonedMetal.esp with ModSkillUse ×0). Products are moved out on menu close (`transferProducedItems`) and delivered later through hidden containers as tokens (`OnItemAdded` from `item_storage`/`transition_container`/mannequin 000813). Tempering of NPC-crafted gear happens only if `bSkillBasedSmithing=1` (`quality = 1 + min(skill/100,1) × (fSmithingArmorMax×0.005+0.2)` = up to 1.5 under Requiem's 60). Today it is 0, so NPC-crafted gear arrives untempered.
3. Hooks to tell player-forge from HM: mod events `HMServiceStarted`/`HMServiceFinished`; perk `HM_SkillControl` on the player during a session; delivered items arrive from a container. Items carry no marker.
4. Requiem also tempers NPC-worn armour at spawn (`REQ_TemperedEquipment`, tier tables). Looted armour can already be above base.

### 3.6 Everything else CCOR overrides (winner in Authoria today)

| CCOR override set | Winner now | Action |
|---|---|---|
| 28 jewellery ARMO | JS Vanilla Circlets - Requiem patch (10), Authoria - Master Patch - Armors Merge (16), Requiem - ISC (2) | Drop CCOR's. |
| 60 MISC (ores, ingots, gems, hides, claws, firewood) | Requiem (values/weights), Requiem - ISC (gems), Requiem - Vendor tweaks (dragon bone/scale), USSEP (claws), vanilla (ores, chitin) | Drop CCOR's. Requiem's values stand. |
| 25 vanilla LVLI (jewellery, gems, minerals) | Requiem.esp (16), Authoria - Reqtificated - LOTD (8), Dragonborn (4) | Merge CCOR's new jewellery/gems into the winners in a patch. RFTI does not currently win any of these 25 (only one plugin touches each today), so plan a hand merge and check after the Reqtificator run whether it merged them itself; keep whichever result is correct. |
| 2 WEAP silver, 2 PERK, 3 BOOK (LOTD wins), 1 CELL (Synthesis output wins), 1 OTFT, 1 LIGH, 8 GLOB (job values, uncontested) | see above | Drop, except keep the two FURN below. |
| 2 FURN (`CraftingSmelterMarker1`, `CraftingTanningRackMarker`) uncontested | vanilla | Keep. CCOR sets `WorkbenchData.UsesSkill = Smithing`. That alone makes the engine grant Smithing XP at the smelter and tanning rack using Requiem's own XP formula. No script needed. |
| 583 ACTI ore veins | PG_1 / skymoji | Do not ship. Use a vein script that infers Stalhrim/geode/clay from the ore item instead (section 8). |
| 57 ARMA (circlets, rings, amulets) | mostly uncontested vanilla/USSEP | Only needed for CCOR's own jewellery meshes; keep only what CCOR's kept items reference. |
| 98 `WAF_` KYWD, 199 injected GLOB, 15 injected MISC, 7 injected KYWD, 23 injected COBJ, 9 injected LVLI, 3 injected PERK, 4 MESG, 1 CONT/REFR (PRUFEI chest) | only CCOR defines them | Keep. They are the "API" and cost nothing. |

### 3.7 Housekeeping facts

1. Runtime is Skyrim SE 1.6.1170. HEDR 1.71 ESLs (4096 records) are fine.
2. Main profile census: 3690 resolved active plugins, 184 full + 5 base + about 7 full CC ESMs ≈ 196 full. Roughly 55 full slots free. Two active plugins are missing files in Main (`Authoria - Output - Synthesis Gameplay.esp`, `…Worldspace.esp`).
3. `Requiem for the Indifferent.esp` masters CS-only plugins (3DNPC, GORE, SearchUI, Elmlock…). Main needs a Reqtificator re-run regardless of this project.
4. CCOR needs crafting-furniture animations for its `OnSit`-based detection. Authoria uses crafting animations (Crafting Camera Fix is OAR-only). Verify no "no crafting animation" mod is active before relying on any seated-detection script.
5. Nexus: no CCOR patch exists for Requiem 6. The Requiem 5.4.5 patch (mod 31758, requires WACCF) documents the reconciliation rules its author used: weapons/armour keep Requiem values; clothing/jewellery/misc keep CCOR values; disable Requiem recycling; hide Requiem's mineorescript; unenchanted variations off; Daedric-at-night on. Requiem 6 has WACCF/ACE patches only (mod 162261).
6. Ars Metallica is incompatible with CCOR by design. Not present in Authoria. Nothing else in Authoria edits smithing recipes at runtime (no SkyPatcher COBJ folders, KID cannot touch COBJ).

---

## 4. Feature matrix (what to keep from CCOR under Authoria)

Legend: KEEP = keep as CCOR ships it. ADAPT = keep, but re-gate/re-wire for Requiem. OFF = disable (MCM default off + recipes disabled or deleted). DROP = delete from the build.

| CCOR feature | Under Authoria | Recommendation |
|---|---|---|
| Crafting-menu material/style/type filters (257 token recipes, thread scripts) | Duplicates COCKS; tokens show inside COCKS categories | OFF (Curated). Keep COCKS. Add CCOR's new items to the COCKS JSON/KID so they sort. |
| "Recipe origin" toggles, complexity, generic fur plate, declutter | Only meaningful for CCOR's own recipes now | KEEP for CCOR-owned recipes; irrelevant for Requiem recipes |
| Reworked vanilla recipes (487 overrides) | Requiem owns these; 111 are REQ_NULL | DROP all 487 |
| Missing recipes for vanilla items (415) | 134 duplicate Requiem; the rest change Requiem availability | ADAPT: delete duplicates; keep quest/ownership-gated sets; re-gate to Requiem perks; per-set decision list (section 9, Phase 1 step 6) |
| Jewellery, 5 gemstones, cut-gem recipes, circlets (274 recipes, ~250 items) | Additive; needs Requiem values and vendor-list merges | KEEP (Curated). Reqtificator handles ARMO stats by keyword. Merge into 25 LVLI. Jewellery gold value = Requiem's silver/gold ring values as reference. |
| Armored circlets (matching-set circlets) | Additive; helmet-slot AR by material keyword | KEEP but verify Reqtificator output; check Requiem's "full set" perks count a circlet with `ArmorHelmet` |
| Unenchanted faction gear, artifact replicas | Additive; CCOR gates on quests/holding the item | KEEP behind CCOR's own gates; drop the WACCF-mesh variants; re-gate replica tempering from 05218E to Legendary Blacksmithing (17B8BF) |
| Breakdown at smelter/tanning rack (465) + PRUFEI | Duplicates Requiem recycling (496 smelter, 104 rack) | Decision 4. Default: OFF, keep Requiem recycling. Alternative: keep CCOR breakdown, turn Requiem's `REQ_Skills_HideClutterRecipes` on. Never both. |
| Learning system (Falmer/Draugr/Forsworn tokens) | Flavour; touches sets Requiem does not let you craft | OFF unless the corresponding "missing recipe" set is enabled |
| Upgrade unique leveled items (74 recipes, spell, script) | Requiem delevels uniques | DROP |
| Smithing XP takeover at the forge (perk ×0 + script formula) | Replaces Requiem's linear XP | OFF. Keep Requiem's engine XP for crafting. |
| Smelter/tanning XP | Requiem gives none | KEEP via the two FURN records (`UsesSkill = Smithing`). Engine formula. Optional multiplier perk later. |
| Mining XP | Wanted, but flat | ADAPT into the rarity-scaled script (section 8) |
| Mining speed / ore per vein / drops per vein MCM | Wanted; must default to Requiem's 6 per vein | ADAPT (defaults 6 total, 1 per drop, strikes 1) |
| Firewood per chop, chopping options (`ResourceFurnitureScript`) | Campfire's `Campfire collectable wood` and Campfire's chopping-block edits are present | ADAPT only if no conflict; else OFF |
| Silver/gold armour perks, silver weapon slider | Requiem silver system | DROP silver weapon slider; silver/gold armour perk optional (off) |
| Tempering/enchanting adjustments | Requiem perks own tempering | OFF |
| Rename materials (Corundum→Copper etc.) | Runtime `SetName`; harmless | KEEP (off by default) |
| Daedric only at night | Flavour | KEEP (Requiem patch author had it on) |
| Gem chance / flawless chance in veins | Wants CCOR's `lItemGems10` list | KEEP by overriding the vanilla `lItemGems10` list winner (LOTD-Reqtificated) in the patch |
| Calcinium/Galatite alloys, dyed leather, buckles, sinew | Additive; Bruma has its own metals | KEEP (Curated) or DROP (Mechanics-only) |
| Mod-support toggles (IA, IW, Cloaks, Bandoliers, JaySuS, WIC, Book of Silence, Campfire, Bruma, CACO) | Only Campfire and Bruma exist in Authoria | Keep Campfire and Bruma hooks; the rest inert |
| PRUFEI favourite protection | Only used by breakdown | Follows decision 4 |
| SRD yaml (AOS/ISC) | Authoria has both AOS and ISC via Requiem patches | KEEP if SRD is installed; else convert to a 4-record WEAP override |

Scope presets:

1. Full: everything above except DROP rows. Most work; most collisions to manage; keeps CCOR filters alongside COCKS.
2. Curated (recommended): KEEP + ADAPT rows; menu filters OFF; breakdown per decision 4.
3. Mechanics-only: mining XP, smelter/tanning XP, mining MCM, player-crafted bonus, no CCOR content. This does not need CCOR at all (a 2-FURN + script + DLL package).

---

## 5. Architecture options

### Option A. Unmodified CCOR.esp + stub master + Authoria patch layer

1. Install CCOR from Nexus as is.
2. Add an empty ESL-flagged plugin named `weapons armor clothing & clutter fixes.esp` (TES4 header only) so the master resolves. It contains no WACCF data.
3. Load CCOR before Requiem so Requiem wins every collision by default.
4. An ESL patch after the Requiem stack overrides the ~40 WACCF-referencing records, disables the token/breakdown/duplicate/leveled-item recipes (about 800 workbench-keyword overrides), fixes perk gates, merges 25 LVLI, adds COCKS/KID entries.
5. Loose-file script overrides replace CCOR's `mineorescript.pex` and `cco_altsmithingexpplayerscript.pex` with Authoria versions.
6. Costs: 1 full plugin slot (CCOR is 3880 records, not compactable while patches reference it), the stub hack, ~900 patch records, and CCOR's MCM still shows options that do nothing.
7. Benefit: redistribution-safe (only patches and our own files are shipped).

### Option B. Edited standalone "Authoria Smithing (CCOR-derived).esp" (recommended if the list is private or WJ-binary-patched)

1. Copy CCOR.esp, remove the WACCF master, delete the 1363 overrides except the two FURN, delete DROP/OFF content, repoint the ~40 WACCF references, re-gate perks, keep the injected API records.
2. Compact to ESL (new records fall well under 4096; injected `Update.esm` records are untouched by compaction). Rename plugin and BSA together, or keep CCOR's BSA name loaded through `sResourceArchiveList2` in the profile `Skyrim.ini` (Authoria already manages profile INIs).
3. Edit and recompile the MCM/alt-XP/mining scripts (sources ship in the BSA; SKSE/SkyUI headers needed).
4. Costs: any Patch Hub patch needs FormID remapping (only Bruma, Campfire, Cloaks&Capes SMP, Nordic Jewelry, Dawnguard Arsenal, New Legion, S&S, Scout Armor are candidates; several of those require WACCF and would be rebuilt anyway). Updating to a future CCOR needs the cut list re-applied (scriptable with houseCARL; CCOR churn is low).
5. Benefit: one ESL, no stub, no dead MCM options, cleanest load order.

### Option C. Mechanics-only package (no CCOR)

1. `Authoria - Smithing Mechanics.esp` (ESL): 2 FURN overrides (smelter/tanning XP), mining globals/formlists, MCM Helper config, our vein script, LVLI gem tweaks.
2. Player-crafted DLL.
3. Costs: none of CCOR's content. Benefit: no permission questions, smallest surface.

Recommendation: Option B with the Curated scope if Authoria is private (or you accept a Wabbajack binary patch of CCOR.esp). Option A if it must be redistribution-clean. Option C is the fallback if content is not the point. The two custom features are identical in all three.

DECIDED 2026-08-16: Option A, Curated scope. The rest of this document assumes Option A. Concretely, the layer is:

1. `Complete Crafting Overhaul Remastered` installed from Nexus, unmodified (esp + BSA + yaml). Sound Record Distributor is already in Authoria, so the AOS/ISC yaml files work.
2. `Authoria - WACCF Stub` mod: one ESL-flagged plugin named exactly `weapons armor clothing & clutter fixes.esp` with a TES4 header only. Loads before CCOR. It exists only so CCOR's master resolves. Every CCOR record that references a WACCF form is overridden by the patch, so no live record points into the stub.
3. `Authoria - Patch - CCOR - Requiem.esp` (ESL): the curation layer. About 950 override records plus a few dozen new records (mining tier formlists/globals, merged leveled lists). Loads after the Requiem stack.
4. `Authoria - Smithing Scripts` mod: our own `mineorescript.pex` (+ source) placed above `Go To Bed - Requiem` in the modlist so it wins the loose-file contest over Go To Bed, Requiem.bsa, USSEP.bsa and CCOR's BSA. Optionally an MCM Helper page for the mining tiers.
5. `Authoria - Crafted Gear` mod (Phase 3): our SKSE plugin DLL + INI. Independent of CCOR.
6. COCKS/KID additions live in the existing `Authoria - Crafting Catergories` mod (JSON + KID ini).

---

## 6. Feature 1: player-crafted items are 20% stronger

### 6.1 Facts that shape the design

1. The engine has no "crafted by" flag. The only per-instance strength channel is tempering health (`ExtraHealth`).
2. Tempering is additive: bonus = (health − 1) × `fSmithingWeaponMax`/`fSmithingArmorMax` (60 in Requiem), cuirasses ×2. Health after tempering ≈ 1 + (Smithing/200) × product of ModTemperingHealth multipliers (Requiem: 1.6–2.0, Legendary ×1.5).
3. Vendor gear is health 1.0. Honed Metal gear is health 1.0 today (`bSkillBasedSmithing=0`). Looted NPC armour may be tempered by Requiem's `REQ_TemperedEquipment`.
4. Honed Metal crafts through the same crafting menu. Any "crafted" hook must ignore HM sessions (perk `HM_SkillControl` on the player, or the `HMServiceStarted/Finished` mod events).
5. Papyrus can detect a craft (`OnItemAdded` with no source container while seated, PO3 `OnItemCrafted`, Dylbill `OnItemCraftedGlobal`). Papyrus cannot set health on an unequipped inventory stack. It can only set it on a world reference or a worn item.

### 6.2 What "20% stronger" means (choose one)

1. Head start: a crafted item is created at the health that equals +20% of its base damage/AR: `h = 1 + 0.2 × base / (60 × [2 if cuirass])`. Example: base 48 → h 1.16 ("Fine"). Later tempering overwrites this once skill × perks exceed it (at Craftsmanship 1.6 that is Smithing ≈ 20). Cheap; early-game only.
2. Permanent: same head start, and every later temper of a player-crafted item gets its temper delta multiplied by 1.2. Needs a persistent marker (`ExtraUniqueID` + co-save) and a temper hook. Only the SKSE route can do this.
3. Relative to Honed Metal: keep `bSkillBasedSmithing=0` so NPC-crafted gear stays 1.0. If you ever enable it, cap `fNPCSkillModifier` so NPC output stays below the crafted head start.

### 6.3 Implementation routes

Route S (recommended): small SKSE plugin (CommonLibSSE-NG, 1.6.1170, Address Library).

1. Listen for `TESContainerChangedEvent` (new container = player, old container = none, no reference) while `CraftingMenu` is open and the bench is a forge/Skyforge (bench keyword check on the furniture the player is using). This is the same signal CCOR uses in Papyrus.
2. Skip if the player has `HM_SkillControl` (000810:HonedMetal.esp) or an HM session flag is set.
3. Split `count` items off the plain stack into a new stack with `ExtraHealth = h(item)` and, for the permanent variant, `ExtraUniqueID` recorded in the co-save.
4. Permanent variant: on the temper event (the native item-crafted event PO3 exposes as `OnItemCrafted`, or a hook on the smithing menu's temper function), if the tempered instance is marked, multiply the temper delta by 1.2.
5. Config INI/JSON: percent, weapon/armour/ammo toggles, exclude jewellery/clothing, exclude Skyforge or not, HM exclusion on/off.
6. Effort: 1–2 sessions to scaffold and build once the toolchain exists (vcpkg cache is present on this machine; the `skse-plugin-authoring` skill has the template), 1 session of in-game testing by you.

Route P (prototype only): Papyrus with PO3 `OnItemCrafted`.

1. On craft, queue the item. On leaving the bench, `DropObject(item, count)` → `SetItemHealthPercent(h)` → `AddItem(ref)`.
2. Hazard: `DropObject`/`RemoveItem` pick any instance of that base item. If you already carry a tempered copy, it can be the one dropped and its health is overwritten downward. This is data loss. Mitigation (skip when you own other copies) makes the feature inconsistent.
3. Only acceptable as a proof of feel, not as the shipped mechanic.

Route D (data-only, not recommended): duplicate every craftable weapon/armour as a "crafted" record with +20% stats. Breaks quests that check base FormIDs (Adrianne's iron dagger, Companions' Skyforge tasks), doubles tempering recipes, needs re-application after each Reqtificator run.

### 6.5 Choosing the semantics (decision 5, still open)

| | Head-start only | Permanent (+20% base and +20% of every temper) |
|---|---|---|
| What the player sees | New crafted item shows a quality tag ("Fine"-class) and +20% base damage/AR | Same at creation; every temper on that item lands 20% higher than the same temper on a bought item, for the life of the item |
| When it stops mattering | As soon as your own tempering exceeds the head start (Craftsmanship 1.6 at Smithing ~20 for most items) | Never; the gap stays proportional |
| vs vendor gear (health 1.0) | +20% until you temper either | Always ahead by 20% of base + 20% of temper |
| vs Honed Metal (health 1.0 today) | Same as vendor | Same as vendor |
| vs looted Requiem-tempered armour | Loot can still be better | Loot can still be better early; crafted overtakes with skill |
| Engineering | DLL: container-changed hook + stack split, no co-save | DLL: adds `ExtraUniqueID` marker, co-save, temper hook |
| Risk | Low | Medium (temper hook must be verified against Requiem perks and Honed Metal tempering orders) |
| Fits "player craft is worthwhile" | Early game only | Whole game |

If you want the feeling that smithing your own gear matters at level 40 too, choose permanent. If you mainly want early-game identity, head-start is cheaper and safer. Either way the first build is the head-start core; the permanent variant is an addition on top.

### 6.4 Interactions to test

1. Requiem tempering perks and Legendary Blacksmithing.
2. Honed Metal delivery path (items must not get the bonus).
3. Enchanting a crafted item (health survives enchanting).
4. Followers equipping crafted gear (Requiem's NPC temper script only runs on spawn; fine).
5. Skyforge steel and Aetherium forge (bench keyword list).
6. Ammo and staffs (probably exclude).

---

## 6B. Option D (proposed by Aaronavich 2026-08-16): mechanics package + CCOR-inspired recipe complexity pass, no CCOR install

### 6B.1 What it is

1. Do not install CCOR at all. No stub master, no CCOR full plugin slot, no dead MCM pages, no 950 neutralising overrides, no permission questions.
2. Ship the mechanics package (section 5, Option C): smelter and tanning-rack Smithing XP (two FURN overrides setting `WorkbenchData.UsesSkill = Smithing`, our own records), the rarity-scaled mining XP script with its tier formlists and sliders (section 7), the player-crafted bonus DLL (section 6), and optional flavour rules such as Daedric crafting only at night.
3. Add a recipe complexity pass: rewrite the ingredient lists of Requiem's forge recipes to CCOR's formula pattern (primary material + secondary material + leather + leather strips per item part) using vanilla materials only, while keeping Requiem's perk gates, workbench, created count and every non-ingredient field exactly as Requiem has them.
4. Cost: CCOR's content is not included (five gemstones, new jewellery, armored circlets, replicas, unenchanted faction gear, alloys). Option A can still be layered on later; nothing in D conflicts with it.

### 6B.2 What "CCOR-inspired complexity" means, concretely

CCOR's published pattern (article 1468) per part:

| Part | Primary | Secondary | Leather | Leather strips |
|---|---|---|---|---|
| Gauntlets | 2 | 1 | 1 | 2 |
| Boots | 3 | 1 | 1 | 2 |
| Helmet | 3 | 1 | 1 | 1 |
| Cuirass | 5 | 2 | 2 | 4 |
| Shield | 4 | 1 | 0 | 2 |
| Dagger | 1 | 1 | 0 | 1 |
| Sword | 2 | 1 | 0 | 1 |
| War axe | 2 | 1 | 0 | 2 |
| Mace | 3 | 1 | 0 | 2 |
| Greatsword | 3 | 1 | 0 | 2 |
| Battleaxe | 3 | 2 | 0 | 3 |
| Warhammer | 4 | 2 | 0 | 3 |
| Bow | 3 | 1 | 0 | 2 |
| Arrows ×24 | 1 | 2 firewood | 0 | 1 |

CCOR's actual material pairs (read from its recipe records; CCOR's own alloys replaced by the vanilla ingot in brackets):

| Material | Primary | Secondary | Notes from CCOR's records |
|---|---|---|---|
| Iron | Iron ingot | goat hide (cuirass) / none (weapons) | iron cuirass = 4 iron, 1 goat hide, 2 leather, 4 strips |
| Steel | Steel ingot | iron ingot | steel cuirass uses 1 [ingredient 0003AD74] as the secondary; Requiem already does 2 iron + 5 steel + 4 strips |
| Dwarven | Dwarven ingot | steel ingot | 5 dwarven, 2 steel, 2 leather, 4 strips |
| Orcish | Orichalcum | corundum | 5 orichalcum, 2 corundum, 2 leather, 4 strips |
| Elven | Calcinium [moonstone] | quicksilver | 5 calcinium, 2 quicksilver, 2 leather, 4 strips |
| Glass | Malachite | Calcinium [moonstone] | 5 malachite, 2 calcinium, 2 leather, 4 strips |
| Ebony | Ebony | quicksilver | 5 ebony, 2 quicksilver, 2 dark leather, 4 strips |
| Daedric | Ebony | daedra heart ×1 | 5 ebony, 1 heart, 2 dark leather, 4 strips |
| Dragonplate | Dragon bone | ebony + 1 scale | 4 bone, 1 scale, 2 ebony, 2 leather, 4 strips |
| Dragonscale | Dragon scale | dragon bone + quicksilver | 3 scale, 2 bone, 2 quicksilver, 2 leather, 4 strips |
| Steel plate | Steel | corundum | 5 steel, 2 corundum, 2 leather, 4 strips |
| Scaled | Steel + leather | (hide) | 2 steel, 4 leather, 4 strips + 1 hide |
| Leather | Leather | iron ingot ×1 | 4 leather, 5 strips, 1 iron |
| Hide | Leather | deer hide + iron ×1 | 3 leather, 1 hide, 1 iron, 4 strips |
| Nordic (Quicksilver set) | Galatite [quicksilver] | orichalcum | weapon: 2 galatite, 1 orichalcum, 1 strip |
| Stalhrim | Stalhrim | Galatite [quicksilver] (light) / ebony (heavy) | heavy cuirass: 5 stalhrim, 2 galatite, 2 leather, 4 strips |
| Bonemold | Bone meal ×10 | netch leather + iron | 10 bone meal, 2 iron, 2 netch leather, 4 strips |
| Silver | Silver ingot ×1 | steel ×2 | sword: 1 silver, 2 steel, 1 strip |
| Skyforge steel | Steel | (Skyforge) | Nord hero cuirass: 4 steel + 2 special items |

Requiem already carries part of this pattern (steel = iron secondary, elven bow = moonstone + quicksilver, iron cuirass 5 iron + 4 strips). The pass would apply the pattern to every craftable armour part and weapon consistently.

### 6B.3 How the pass would be built

1. Scope: Requiem's forge recipes for craftable weapons and armour: about 503 `REQ_Forge_*` in Requiem.esp plus WAR's 313 (bows/crossbows) and the WAR/ATweaks/New Legion/Sons of Skyrim overrides that currently win. Out of scope: tempering recipes (1 ingot, unchanged), Requiem's `REQ_Smelter_*` recycling, `REQ_Rack_*`, cooking, Fletching's 174 ammo recipes (already Authoria-curated; arrows could join later using the ×24 formula), CCE clothing, artifact/unique/special recipes (`REQ_Forge_Special_*`, `REQ_Crafting_*`, `REQ_Skyforge_*` reviewed by hand), and Creation Club recipes in a first pass.
2. Method: for each recipe, classify the created item by its keywords (armour part: `ArmorCuirass/Boots/Gauntlets/Helmet/Shield`; weapon type: `WeapType*`; material: vanilla `ArmorMaterial*`/`WeapMaterial*` or Requiem's `REQ_ArmorSet_*`), look up the part row and the material pair, and rewrite only the ingredient list. Rare components keep Requiem's count (daedra hearts, dragon bone/scale, stalhrim) unless you decide otherwise. Everything else follows the table.
3. Output first, apply second: a review CSV per recipe (Requiem's ingredients → proposed ingredients, material, part, and any "no rule" rows) for you to tick. Then an ESL patch (`Authoria - Patch - Requiem - Recipe Complexity.esp`) with pure overrides of the winning records, loading after WAR/ATweaks/New Legion/Sons of Skyrim in the Authoria patch band.
4. Verification: no condition, bench, created object or count changes (diff report); every ingredient resolves; the Reqtificator does not touch COBJ, so no re-run is needed for this part (it is still needed for the DLL/mining? no; only for the Main profile's stale RFTI in general).
5. Balance notes for your call: CCOR's pattern raises material counts on some pieces and adds a secondary metal that Requiem's smiths and vendors already stock (`Requiem - Vendor tweaks`, Honed Metal material lists). Leather demand goes up (2 leather + 4 strips per cuirass). Requiem's economy tolerates this. Honed Metal costs scale with materials (`fMaterialsCostMultiplier=2.0`), so NPC crafting gets a little pricier.
6. Effort: one session to script and emit the CSV, one review round with you, one session to apply and verify. Zero in-game dependency until you test.

### 6B.4 What D loses versus A-Curated, and how to get it back

1. Lost: CCOR's five gemstones and jewellery set, cut-gem recipes, armored circlets, artifact replicas, unenchanted faction gear, alloys, dyed leather. Also CCOR's gem-per-vein chance sliders (vanilla `lItemGems10` remains, our script can still honour a gem-chance slider of our own).
2. Get it back later: install CCOR + stub + a reduced patch (the content half of Phase 1). D's mechanics package and recipe pass do not conflict with that; the recipe pass simply wins over CCOR's vanilla recipe overrides by load order.

### 6B.5 My read

D is the smaller, cleaner build and it matches what was said in chat: mechanics plus intricate recipes. It removes every CCOR-side complication in section 3 at once. The only reason to prefer A-Curated is wanting CCOR's item content now. If the honest goal is "smithing feels worthwhile and less flat", D delivers that with fewer moving parts and can be extended to A later.

---

## 7. Feature 2: mining gives Smithing XP scaled by ore rarity

### 7.1 Design

1. Replace the winning `mineorescript.pex` with an Authoria version merged from three sources: Requiem's script (6 ore per vein, USSEP fixes), Go To Bed's Cidhna change (no bed activation, `SetStage(45)` only), and CCOR's mining logic (globals for strikes/ore per drop/total, Stalhrim strike doubling, geode/shellbug/Hearthfire caps, mining noise, XP).
2. Do not depend on ACTI script properties for the special-vein flags. Infer them from the `Ore` / `lItemGems10` properties the vanilla records already carry: Stalhrim = `DLC2OreStalhrim` (02B06B:Dragonborn.esm); geodes = no `Ore` and a gem list; Hearthfire clay/quarried stone = `BYOHMaterialClay`/`BYOHMaterialStoneBlock`; shellbug = `DLC1ShellbugChitin`. That keeps PG_1/skymoji winners intact and needs zero ACTI overrides.
3. Keep Requiem's balance as the default: 6 ore per vein, 1 per drop, strikes as vanilla. Expose CCOR's sliders in the MCM.
4. XP: `xp = BaseXP × TierMult(ore) × count`, granted per drop with `Game.AdvanceSkill("Smithing", xp)`. Requiem's AVIF UseMult is 1, so `xp` is direct skill XP. Requiem needs ≈386 XP for a level at skill 20, ≈812 at 50, ≈1575 at 80 (0.25 × level^1.95 + 300).
5. Tier table (defaults; all editable):

| Tier | Ores | Mult |
|---|---|---|
| 1 | Iron, Corundum, Bruma Tin | ×1 |
| 2 | Silver, Gold, Quicksilver, Moonstone, Orichalcum, Heart Stone, Bruma Copper/Zinc, geode gems | ×2 |
| 3 | Malachite, Ebony, Bruma Meteoric Iron, Wyrmstone, Brimstone | ×3 |
| 4 | Stalhrim, Adamantium, Aetherium Ore, Mithril Ore, CC Amber/Madness | ×4 |

Base XP 3 → an iron vein (6 ore) ≈ 18 XP (5% of an early level); an ebony vein ≈ 54; a Stalhrim deposit ≈ 72. Unknown modded ores fall back to a value-based guess (`value ≥ 100` → tier 4, `≥ 30` → tier 3, `≥ 20` → tier 2) so new mods work without edits.

6. Storage of the table: four FormLists (one per tier) + four multiplier globals + base global. FormLists are extendable by patches without script changes. Alternative: a PapyrusUtil JSON keyed by `0xFormID~Plugin.esp` (never EditorIDs; Requiem renames EditorIDs).
7. MCM: extend the edited CCOR MCM (Option A/B) or a small MCM Helper page (Option C).

### 7.2 Conflicts to handle

1. `Go To Bed - Requiem` and `Go to bed - Patches` loose scripts must be beaten by ours (place our script mod above them) and their Cidhna change must be preserved.
2. UOSC's `mineorefurniturescript.pex` is API-compatible; leave it.
3. Skymoji ACTI (activate text) and PG_1 ACTI (model paths) stay winners. No PG re-run needed for this feature.
4. Bruma/Wyrmstooth/Olenveld/S&S veins use the vanilla script, so they get XP automatically.
5. "Mining Makes Noise" (CCOR global) can stay off by default; Requiem's stealth is its own system.

---

## 8. Build plan (phased, with gates)

All record work is done offline with houseCARL/xEdit scripts. MO2 and the game must be closed before any write into `profiles\`, `mods\` or `ModOrganizer.ini` (workspace rule). Every write gets a delta backup first (existing runbook). Nothing below is executed until you approve the decisions in section 11.

### Phase 0. Decisions and inventory (this document)

Gate: decisions 1–6 answered.

### Phase 1. Build the plugin layer offline (Option A; no MO2 changes yet)

Working folder for everything in this phase: the session scratchpad (or a folder you name). Nothing is copied into `mods\` until Phase 2.

1. Stub master: create `weapons armor clothing & clutter fixes.esp` with a TES4 header only, ESL flag set, no masters, no records. Verify CCOR.esp opens with it present (houseCARL read_plugin_file shows no missing master).
2. Patch skeleton: create `Authoria - Patch - CCOR - Requiem.esp` (ESL, HEDR 1.71) with masters Skyrim/Update/DLCs/USSEP/stub/CCOR/Requiem (+ Requiem addons and `Authoria - Reqtificated - LOTD.esp` only if a merged list needs them).
3. WACCF cut, as overrides in the patch (section 2 table): the 10 circlet ARMO → forward the current winner (`JS Vanilla Circlets - Requiem patch.esp`) so CCOR's WACCF-ARMA versions never win; the 12 new CCOR ARMO → repoint MODL to vanilla ARMAs or hide their recipes; the 12 WACCF-item COBJ → replace WACCF items with vanilla equivalents and set bench to `CraftingDisabledRecipe_CCO` (0702BEA9:CCOR); `WACCF_NewItems` LVLI → empty; `DLC1LItemGuardCrossbowAndBolts_CCO` → vanilla DLC1 crossbow/bolts; the 5 WACCF-defined LVLI and 5 WACCF-defined COBJ overrides in CCOR → cannot be patched (their FormIDs live in the stub); they resolve to nothing and are unused. ARMA alt texture → override without it. Verify with the scanner that no winning record references master index 6.
4. Neutralise CCOR's collisions by load order, not by records: CCOR loads before Requiem, so Requiem and its patches win the 481 recipe overrides, the silver perk/swords, Stalhrim enchanting perk, jewellery ARMO, MISC values, books, cell. Verify with a winner report over CCOR's 1363 override FormIDs after Phase 2 (script already exists: batch winner check).
5. Ore veins: CCOR's 583 ACTI overrides would beat `skymojibase.esl` (Main plugins.txt line 20) and, after the next ParallaxGen run, PG_1.esp would forward CCOR's version and lose the skymoji "Mine" icon text. So the patch forwards the CURRENT pre-CCOR winner of all 583 vein records (skymoji / USSEP-skymoji / BSAssets etc.) verbatim. Result: veins are exactly as today; PG regen stays safe; our script does not need CCOR's properties.
6. Menu filters off: override the 257 token recipes with bench `CraftingDisabledRecipe_CCO`. Override the GLOB defaults `CCO_OptionCraftingMenuBreakdown`, `CCO_OptionCraftingMenuInventoryCond` to 0. (The player-alias script forces the Categories/Options globals to 1; harmless once the token recipes are gone.)
7. Breakdown off: override the 465 breakdown recipes with the disabled bench. Override GLOB defaults `CCO_OptionBreakdownEquipmentatSmelter` and `CCO_OptionBreakdownEquipmentatTanningRack` to 0. Requiem recycling stays as it is. PRUFEI keeps running but protects nothing; acceptable, or set its two protect globals to 0.
8. Leveled-item upgrades off: override GLOB defaults `LevelUpUniqueItems_CCO`, `LevelUpSpellAutoRun_CCO` and the "upgrade via crafting" global to 0; override the 74 upgrade recipes with the disabled bench.
9. XP: override perk `CCO_SmithingXPMultPerk` (062105:CCOR) to remove the ModSkillUse ×0 entry, so Requiem's engine XP flows normally at all benches. Override GLOB defaults `SmithingXPForge_CCO`, `SmithingXPSmelter_CCO`, `SmithingXPTanningRack_CCO` to 0 so CCOR's script adds nothing (its sliders then act as optional bonus XP). Keep CCOR's two FURN overrides (`CraftingSmelterMarker1`, `CraftingTanningRackMarker`, `UsesSkill = Smithing`); nothing else touches them, so smelting and tanning now give Requiem-formula XP. Set the silver-weapon and tempering/enchanting adjustment globals to 0.
10. Recipe curation pass over CCOR's remaining new recipes (about 700 after steps 6–8) with a script that emits a review CSV: (a) disable the 134 duplicates of Requiem recipes; (b) per faction/unique set, apply your keep/drop decision (default: keep only quest/ownership-gated sets); (c) re-gate perk conditions to Requiem's tree (05218E → 17B8BF Legendary Blacksmithing for artifact/unique tempering; keep 05218E where CCOR means plate/jewellery; material perks 1:1); (d) replace vanilla-forwarded temper conditions with Requiem's; (e) everything hidden gets `CraftingDisabledRecipe_CCO`. You tick the CSV before it is applied.
11. Leveled lists: merge CCOR's new gems/jewellery into the 25 vanilla LVLI at their current winners (Requiem.esp / `Authoria - Reqtificated - LOTD.esp`), forwarding the winner's other changes. Inject CCOR gems into `lItemGems10` so veins drop them.
12. Reqtificator readiness: verify every kept CCOR ARMO/WEAP carries the material/type keywords the Reqtificator keys on. Decide which Requiem armour-set keyword each armored circlet gets. Log anything the Reqtificator would skip.
13. Sorting: add KID lines / COCKS JSON entries so CCOR items land in the right COCKS categories (jewellery already matches `ClothingCirclet`/`ClothingRing`/`ClothingNecklace`; add rough gems, alloys, armored circlets by material).
14. Scripts: Authoria `mineorescript.psc` per section 7 (vanilla + SKSE headers from the toolkit; validate and compile; keep the source in the mod). Mining tier formlists/globals live in the patch; the MCM Helper page is optional (needs the MCM Helper SDK, section 12). No CCOR script is edited.
15. Verify: `housecarl_check_errors` on stub + patch, masters list, no unresolved references, `housecarl_write_seq` if the patch gains a start-enabled quest (it should not).
16. Package the four mod folders (section 5, "DECIDED" list) with READMEs listing every override and why.

Gate: error check clean; scanner shows no live WACCF references; recipe review CSV approved by you.

### Phase 2. Install into the Main profile

1. MO2 closed. Delta backup of `profiles\Authoria - Requiem Reforged - Main Profile\` and the touched `mods\` folders.
2. Install mod folders in MO2 priority: `Authoria - WACCF Stub` and `Complete Crafting Overhaul Remastered` near Honed Metal (modlist ~line 1401 region), `Authoria - Smithing Scripts` above `Go To Bed - Requiem` (line 1265), the patch mod in the Authoria patch block, the COCKS/KID additions inside the existing `Authoria - Crafting Catergories` mod.
3. Plugins: stub then CCOR before `Requiem.esp` (Main plugins.txt line 1503; the Honed Metal/Fletching band at 410–412 is a natural slot; keep both after `skymojibase.esl` line 20 and USSEP). Patch ESL after `Requiem - Dirt and Blood.esp` (line 1682) inside the `Authoria - Patch - Requiem - *` band (3467–3503) and after `Authoria - Patch - Skymoji - USSEP.esp` (3401) because it forwards vein records. Never below the `Authoria - Outputs` block. Update `plugins.txt`, `loadorder.txt` and `plugingroups.txt` together.
4. Reqtificator: you run it (Main profile). Confirm the new plugin appears in the RFTI masters and that circlets/replicas/unenchanted sets got Requiem stats.
5. ParallaxGen: not needed if no ACTI records were shipped. If you later choose CCOR's ACTI overrides, PG must be regenerated and a skymoji forward patch added.
6. In-game smoke test (you): new game or a clean save. Checklist: forge shows Requiem recipes plus CCOR content in COCKS categories; no REQ_NULL recipe visible; smelter and tanning rack give Smithing XP; mining gives tiered XP with 6 ore per vein; Cidhna Mine mining still sets stage 45 without bed activation; Honed Metal order works; jewellery vendors stock new gems; MCM opens with only live options.

Gate: smoke test passes; Papyrus log clean of `[CCO_` / `MineOreScript` errors.

### Phase 3. Player-crafted +20% (SKSE plugin)

1. Toolchain: CMake + vcpkg + CommonLibSSE-NG (the `skse-plugin-authoring` skill has the scaffold; vcpkg cache exists at `%LOCALAPPDATA%\vcpkg`).
2. Implement Route S per section 6.3 with an INI. Log every application at debug level.
3. Test matrix from section 6.4. You run the game.
4. Ship as its own mod folder (DLL + INI + optional MCM Helper toggle).

Gate: crafted iron sword shows "(Fine)"-class health with +20% base damage; HM order arrives at 1.0; tempering behaves per the chosen semantic.

### Phase 4. Balance and documentation

1. Tune XP sliders against Requiem's curve using a short mining/crafting session log.
2. Decide the smelter/tanning XP multiplier.
3. Update `AGENTS.md`/README with the new plugins, their slots and the "re-run Reqtificator after CCOR-layer changes" rule.
4. Save a project memory note (done by me once you approve the plan).

---

## 9. Risks and caveats

1. Permissions: CCOR forbids re-upload/collection packaging and asset reuse. Option B modifies and effectively re-packages CCOR. Fine for private use; use Option A or a WJ binary patch if the list is shared.
2. Requiem update churn: Requiem 6.0.2 "Unbroken Road" and its addons are the balance owners. Every Requiem update needs the recipe curation script re-run (it is scriptable; keep the review CSV).
3. CCOR update churn: low (2.6.4 is June 2026), but any update re-applies the cut list.
4. Reqtificator: must be re-run after the CCOR layer lands and after every change to it (new ARMO/WEAP records).
5. Save safety: adding the layer mid-save is fine (new records, MCM). Removing it later leaves orphaned CCOR items and quest aliases (`CCO_MCMStartupQuest_V2` etc.). Treat it as a new-game feature for release, mid-save for testing only.
6. Menu detection: any seated-detection script (CCOR's or ours) fails if crafting animations are disabled. Verify.
7. PRUFEI cost: the favourite-mirror loop walks the inventory on the favourite key. With big inventories this stutters. Only relevant if CCOR breakdown is kept.
8. Vein script ownership: three mods now compete for `mineorescript.pex`. Ours must be documented as the single owner. Requiem updates that change the script must be diffed against ours.
9. Papyrus route for the crafted bonus can destroy tempering on existing items. Do not ship it.
10. Honed Metal DLL is version-locked to 1.6.1170; our SKSE plugin should target the same runtime only.
11. Two missing Synthesis outputs are already active in Main plugins.txt; unrelated but noticed.
12. `Requiem for the Indifferent.esp` in `Authoria - RFTI Output` was built against the CS profile. Main needs its own run before any test.

---

## 10. Effort estimate

| Phase | Work | Who |
|---|---|---|
| 1 | Plugin cut/curation scripts, script edits, packaging: 3–4 working sessions | me, with your review of the recipe CSV |
| 2 | Install + Reqtificator + smoke test: 1 session | me (files), you (Reqtificator, game) |
| 3 | SKSE plugin: 1–2 sessions build, 1 session test | me (code), you (game) |
| 4 | Balance + docs: 1 session | both |

---

## 11. Decisions (status)

1. Distribution: DECIDED. Published Wabbajack list → Option A (distro-safe).
2. Scope: REOPENED. A-Curated (CCOR content + mechanics) vs D (mechanics + recipe complexity pass, no CCOR). See section 6B. My recommendation is D, extendable to A later.
3. Menu: DECIDED. COCKS categories are the filters; CCOR token filters off; CCOR items added to the COCKS JSON.
4. Breakdown: DECIDED. Requiem/Authoria recycling stays; CCOR breakdown off.
5. Crafted-bonus semantics: OPEN. See section 6.5. The head-start core is built first either way.
6. SKSE plugin build: DECIDED as "get me what I need". Tools are listed in section 12; nothing to buy.
7. Per-set keep list for CCOR's "missing recipes" (Blades, bandit, Companions, Falmer, Forsworn, guard, Nightingale, Skyforge steel, Draugr, DB/TG unenchanted, replicas): OPEN until the Phase 1 review CSV. Default: keep only sets CCOR gates on quest progress or on owning the original.

---

## 12. Tools and inputs (checked on this machine 2026-08-16)

Already present, nothing to do:

1. Visual Studio Build Tools 2022 (MSVC 14.44, Windows SDK 10.0.26100) at `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`.
2. CMake at `C:\Program Files\CMake`.
3. Python 3.12, 7-Zip, Git (Git Bash).
4. Papyrus toolchain in `D:\1. MOD STUFF\- ARR STUFF\CLAUDE\spooky\spookys-automod-toolkit`: Champollion decompiler, papyrus compiler, 14302 vanilla CK headers, 124 SKSE headers, 12 SkyUI headers.
5. In Authoria: Address Library (`versionlib-1-6-1170-0.bin`), PapyrusUtil, JContainers, PO3 Papyrus Extender (with sources), MCM Helper (runtime), Sound Record Distributor, COCKS.
6. houseCARL and its Mutagen record tools.

I will fetch myself (needs internet, no purchase, no game/MO2 launch): a vcpkg checkout (`git clone`) so CommonLibSSE-NG resolves for the SKSE plugin build. The vcpkg binary cache at `%LOCALAPPDATA%\vcpkg` already exists from earlier work.

You download (Nexus, manager or manual):

1. MCM Helper SDK (optional file on the MCM Helper page, mod 53000). Needed only for the mining-tier MCM page (`MCM.psc` header). If you skip it, the tiers are edited in a JSON and CCOR's own MCM mining sliders still work.
2. Optional: "Honed Metal Materials - CCOR" (mod 95502). Adds CCOR's alloys and gems to Honed Metal's material lists so NPC smiths can use them. Only relevant if the Curated scope keeps Calcinium/Galatite (default yes).

Not needed: WACCF (never), Automation Tools / mteFunctions (the CCOR compatibility script is not used), Smithing Perks Overhaul (incompatible with Requiem's tree), the Patch Hub's WACCF-mastered CCOR patches (Dawnguard Arsenal, New Legion, S&S, Scout Armor: rebuilt in our patch if wanted).

Wabbajack notes for the maintainer: CCOR is manager-download-only on Nexus (fine for WJ). The stub master, the patch, the scripts mod and the DLL mod are our own files (inline in the list). No CCOR asset is copied or modified.

---

## 13. Reference data

1. CCOR record scan: `scratchpad\ccor_scan.json` (per-record class, per-reference master, WACCF/USSEP reference rows), scanner `scratchpad\esp_scan.py`.
2. CCOR overrides not touched by Requiem: `scratchpad\ccor_cobj_overrides_not_requiem.txt` (6). Overlap list: `scratchpad\overlap_ccor_requiem_cobj.txt` (481).
3. Duplicate created-object list (CCOR-new vs Requiem-new): `scratchpad\dup_ccor_requiem_created_objects.txt`.
4. Requiem COBJ dump: `scratchpad\agentA\requiem_cobj.json`; WAR/Fletching/CCE dumps alongside; perks: `agentA\requiem_smithing_perks.json`.
5. Ore veins/ores/scripts: `scratchpad\agentB\` (oreveins.json, ores_filtered.csv, gotobed_mineorescript.psc, honedmetal\ sources).
6. Decompiled Requiem/Go To Bed scripts: `scratchpad\decomp\`.
7. CCOR docs: `scratchpad\agentC\` (article1467.txt compatibility guide, article1468 recipe formulas, article1469 alt XP, the four Google Sheet CSVs with every `CCO_` global and FormID, Nexus description/changelog, forum compatibility notes, patch hub notes).
8. Main profile plugin census: `scratchpad\census_Authoria_-_Requiem_Reforged_-_Main_Profile.txt`.
9. Injected mining globals: `CCO_MiningSkillIncreaseGV` 01CC0450, `ResourceCountGV_CCO` 01CC0501, `ResourceCountTotalGV_CCO` 01CC0502, `StrikesBeforeCollectionGV_CCO` 01CC0503, `AttackStrikesBeforeCollectionGV_CCO` 01CC0504, `MiningMakesNoise_CCO` 01CC0508 (all `Update.esm` space).
10. Requiem gates: `REQ_DisableRecipe` AD3B01:Requiem.esp; `REQ_Skills_HideClutterRecipes` 3BA1F3:Requiem.esp; Legendary Blacksmithing 17B8BF:Requiem.esp; Arcane Craftsmanship 309D25:Requiem.esp; Honed Metal session perk `HM_SkillControl` 000810:HonedMetal.esp.
