# Triggers - 58 SURVIVAL AND NEEDS (prefix SR, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\58 SURVIVAL AND NEEDS.txt`
Written 2026-10-18. Writing only: nothing in the game, the profiles or the mods was touched. Globals and spells below were read read-only through houseCARL from the live load order (epoch e2-509d9856becc0652).

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C) plus **S = Serana**, **A = Ashe**, **P = Luna** (player line, Eleonora voice; no Free() test).
Everything obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana/Ashe Free() rows are in `20 DAWNGUARD.md` section 1. Every talk needs each speaker pair's first-meeting talk already played (TRIGGERS.md "Chains").
Gate codes reused: TRIGGERS.md section 4 (`K_CRUSH`, `K_TOG+`, `K_ANY`, `G_FLIRT`, `G_TOG+`, `V_FLIRT`, `V_TOG+`, `ANYROM`, `BRYNJAR`, `CAMP`, `NIGHT`, `MORNING`, `SNOW`, `INN`, `WILD`), `43 WHAT LUNA DOES.md` (`SERANA_F`, `S_VAMP`, `ASHE_F`, `ASHE_REVEAL`, `LUNA_VAMP`, `LUNA_WOLF`, `BEAST_BACK`), `48 SERANA.md` (`S_ROM_ON`, `S_KISS`), `49 ASHE.md` (`A_ANY`), `55 TRAVEL AND THE ROAD.md` (`WALK:n`). **[UNC]** = unconfirmed, check at build.

## 1. Which survival system answers which need

| Need | System in this load order | Status |
|---|---|---|
| Hunger, thirst, tiredness | **SunHelm** (`SunHelmSurvival.esp`; stage spells overridden by `Requiem - SunHelm.esp`, same FormIDs) | Confirmed records |
| Cold / exposure, wetness, near fire, shelter | **Frostfall** (`Frostfall.esp`, with Campfire.esm) | Confirmed records, level meanings [UNC] |
| SunHelm's own cold | **OFF**: `_SHForceDisableCold (83132C:SunHelmSurvival.esp) = 1`, set by `SunHelmForceDisableCold.esp` (read: Data = 1). Do **not** gate on `_SHColdSpell0-5` or `_SHCurrentColdLevel`. | Confirmed |
| Diseases | Vanilla disease spells, winner `Requiem - SunHelm.esp`; `_SHDiseasesEnabled (5D19F3) = 1` | Confirmed |
| Survival Mode CC | not active | per brief |

`_SHEnabled (02EB63)` reads 0 in the plugin (the MCM turns it on at runtime), so test **"player has any SunHelm hunger stage spell"** as the "SunHelm is running" check (`SH_ON`), not the global.

## 2. New gate codes for this file

**SunHelm stages (player `HasSpell`, all `SunHelmSurvival.esp`, confirmed FormIDs and names):**
- Hunger: `WELLFED` = `_SHPosHunger` 001824 "Well Fed"; `SATISFIED` = `_SHHunger00` 001825; `PECKISH` = `_SHHunger01` 001827; `HUNGRY` = `_SHHunger02` 001829; `RAVENOUS` = `_SHHunger03` 00182B; `STARVING` = `_SHHunger04` 00182D. `HUNGRY+` = HUNGRY or RAVENOUS or STARVING.
- Thirst: `QUENCHED` = `_SHThirst00` 01E850; `SATED` = `_SHThirst01` 05C47E; `THIRSTY` = `_SHThirst02` 05C47F; `PARCHED` = `_SHThirst03` 05C481; `DEHYDRATED` = `_SHThirst04` 05C483 or `_SHThirst05` 05C485. `THIRSTY+` = any of 02-05.
- Tiredness: `WELLRESTED` = `_SHFatigue00` 01E846; `RESTED` = `_SHFatigue01` 01E845; `SLTIRED` = `_SHFatigue02` 01E848; `TIRED` = `_SHFatigue03` 01E84A; `WEARY` = `_SHFatigue04` 01E84C; `EXHAUSTED` = `_SHFatigue05` 01E84E.
- `FOODPOISON` = `_SHFoodPoisoningSpell` 6410BF.
- Raw values if needed instead: `_SHCurrentHungerLevel` 00EAAE, `_SHCurrentThirstLevel` 05C472, `_SHCurrentFatigueLevel` 021E3F (GlobalFloat; stage thresholds **[UNC]**, use the spells).

**SunHelm events (controller remembers the last stage seen on its 60 s poll):**
- `ATE` = hunger stage goes from HUNGRY+ to SATISFIED or WELLFED.
- `REFILL` = thirst stage goes from THIRSTY+ to QUENCHED **while** the player is within 300 units of water (po3 `IsActorInWater` / near-shore proxy as `RIVER` in 55 TRAVEL) **[UNC: SunHelm waterskin item FormIDs not read; an OnItemAdded on the filled-skin items would be cleaner]**.
- `WOKE_WELLRESTED` = player just woke (OnSleepStop) and has WELLRESTED.
- `HOTMEAL` = player gains the effect of `_SHSoupWarmthSpell` 7B2A1F "Warm Soup". `HOTDRINK` = `_SHBeverageWarmthSpell` A1738A "Hot Beverage". Check with `HasMagicEffect` on each spell's first MGEF **[UNC: MGEF FormIDs not read]**.

**Frostfall (all `Frostfall.esp`, confirmed records):**
- `FF_ON` = `FrostfallRunning` 06DCFB == 2 **[UNC running value]**. Every cold/wet row needs it.
- Exposure: `_Frost_ExposureLevel` 068119 (GlobalShort). Assumed scale **[UNC, verify in FrostUtil before build]**: 0 Warm, 1 Comfortable, 2 Cold, 3 Very Cold, 4 Freezing, 5 Frozen. `COLD` = >= 2. `FREEZING` = >= 4. Raw meter: `_Frost_AttributeExposure` 00183D vs `_Frost_AttributeExposureMax` 07CAA4.
- Wetness: `_Frost_WetLevel` 06458D (GlobalShort). Assumed **[UNC]**: 0 Dry, 1 Damp, 2 Wet, 3 Soaked. `WET` = >= 2, `SOAKED` = 3. Raw: `_Frost_AttributeWetness` 06458C.
- `NEARFIRE` = `_Frost_NearFire` 064AFD == 1 (with `_Frost_CurrentHeatSourceSize` 064AFC, `_Frost_CurrentHeatSourceDistance` 064AFB).
- `SHELTER` = `_Frost_IsTakingShelter` 068118 == 1.

**Frostfall events:**
- `THAW` = NEARFIRE goes 0 -> 1 while exposure is COLD (`THAW:FREEZING` = while FREEZING).
- `DRIED` = WetLevel goes from >= 2 to 0 while NEARFIRE == 1.
- `AFTERCOLD` = controller saw COLD within the last 2 game hours (rides on HOTMEAL / HOTDRINK / THAW).
- `BLIZZARD_INN` = OnLocationChange into a `LocTypeInn` (01CB87) interior, and in the previous 2 game hours the controller saw exterior + `IsSnowing` + FREEZING. Once per inn visit.

**Camp (Campfire.esm + Frostfall):**
- `PITCH` = a Campfire tent is placed within 1500 units of the player **[UNC: Campfire's tent base FormList / `CampUtil` API not extracted. Fallback: `SHELTER` goes 0 -> 1 in an exterior that is not LocTypeHabitation]**.
- `TENT_NIGHT` = CAMP + NIGHT + a Campfire tent within 1500 units **[UNC same]**.
- `FIREWOOD` = OnItemAdded `Firewood01` (06F993:Skyrim.esm) **[UNC FormID]** or Campfire deadwood/kindling items **[UNC]**, in an exterior.
- `COOKPOT` = player's furniture (`GetFurnitureReference`, po3/SKSE) has keyword `CraftingCookpot` (0A5CB3:Skyrim.esm) **[UNC FormID; also check Campfire's cooking pot carries it]**.
- `ALLGOOD` = (WELLFED or SATISFIED) and (WELLRESTED or RESTED) and exposure <= 1 and WetLevel == 0 and NEARFIRE. Once per in-game week.

**Disease (player `HasSpell`, Skyrim.esm, confirmed; winner Requiem - SunHelm.esp):**
- `DISEASE:Rockjoint` = DiseaseRockjoint 0B8782. `DISEASE:Ataxia` = DiseaseAtaxia 0B877C.
- `DISEASE:any` = any of 0B877C Ataxia, 0B877E Bone Break Fever, 0B877F Brain Rot, 0B8781 Rattles, 0B8782 Rockjoint, 0B8783 Witbane. Sanguinare Vampiris 0B8780 is **excluded** (vampire talks have their own gates). Other mods may add diseases **[UNC: scan for more SPEL with the Disease type at build]**.
- `DISEASE_NEW` = a DISEASE:any spell appeared within the last 3 game hours. `DISEASE_CURED` = event: the player had one, now has none.

**Vampire / werewolf:**
- `VAMP_THIRST` = LUNA_VAMP and vampire stage >= 3: `PlayerVampireQuest` (0EAFD5:Skyrim.esm) `::VampireStatus` >= 3 **[UNC: FormID, variable name, and whether a vampire overhaul in this order replaces the staging]**. Note `_SHVampireNeedsOption` (9DF883:SunHelmSurvival.esp) reads 0.
- `BEAST_BACK` + `LUNA_WOLF` as 43 WHAT LUNA DOES. (`_SHWerewolfFeedOptions` 9DF882 = 1: feeding in beast form fills SunHelm hunger, which is what SR95/SR96 joke about.)

**Places:** `COAST` = exterior within 2000 units of sea water **[UNC proxy: a FormList of coastal map markers / Solitude, Dawnstar, Winterhold, Solstheim coast cells]**. `STILLWATER` = exterior within 500 units of water that is not flowing **[UNC proxy: any exterior water]**.

**Cooldown:** max one SR talk per 4 game hours; each stage talk fires the first time that stage is reached after the cooldown, then is spent (played bit). Hunger/thirst/fatigue talks need SH_ON; cold/wet talks need FF_ON.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| SR1 | K P | E HUNGRY + WILD, walking | SH_ON |
| SR2 | G K | E HUNGRY + WILD, walking | SH_ON; after A1 |
| SR3 | R X | E PECKISH + WILD, walking | SH_ON; Remi/Xel not fallen out |
| SR4 | I P | E HUNGRY + WILD, walking | SH_ON |
| SR5 | V L | E HUNGRY + WILD, walking | SH_ON; after C1 |
| SR6 | C G | E RAVENOUS + WILD | SH_ON; after R5 |
| SR7 | K X | E RAVENOUS + WILD | SH_ON; after C3 |
| SR8 | S P | E RAVENOUS, exterior | SH_ON; SERANA_F; S_VAMP |
| SR9 | L R | E HUNGRY+ and WALK:10 | SH_ON; after B10 |
| SR10 | K G P | E STARVING | SH_ON; after A1 |
| SR11 | A G | E HUNGRY+ | SH_ON; ASHE_F; ASHE_REVEAL |
| SR12 | X P | E STARVING | SH_ON |
| SR13 | C I | E HUNGRY + WILD | SH_ON; after R13 |
| SR14 | V P | E STARVING | SH_ON |
| SR15 | G R | E ATE -> WELLFED | SH_ON |
| SR16 | L P | E ATE | SH_ON |
| SR17 | K R | E THIRSTY | SH_ON; after B1 |
| SR18 | X P | E THIRSTY+ + STILLWATER | SH_ON; FF not needed |
| SR19 | G V | E THIRSTY | SH_ON; after A3 |
| SR20 | C L | E THIRSTY + SNOW | SH_ON; after R11 |
| SR21 | K I | E PARCHED | SH_ON; KaiandInigo stage >= 10 (as K4) |
| SR22 | S R | E REFILL | SH_ON; SERANA_F; S_VAMP |
| SR23 | V P | E THIRSTY+ + COAST | SH_ON |
| SR24 | A K | E REFILL | SH_ON; ASHE_F; ASHE_REVEAL |
| SR25 | P K | E THIRSTY + SNOW, exterior | SH_ON |
| SR26 | P K | E TIRED or WEARY | SH_ON; K_CRUSH |
| SR27 | L I | E WEARY + WALK:5 | SH_ON; after the Lucien-Inigo meet in Lucien.esp |
| SR28 | X G | E EXHAUSTED, exterior | SH_ON; after X1 |
| SR29 | R P | E EXHAUSTED + NIGHT | SH_ON |
| SR30 | V K | E WEARY | SH_ON; after A2 |
| SR31 | P A | E CAMP + NIGHT | ASHE_F; ASHE_REVEAL; K_CRUSH (Kaidan following not required) |
| SR32 | A K | E CAMP + NIGHT | ASHE_F; ASHE_REVEAL |
| SR33 | R C | E CAMP + NIGHT | — |
| SR34 | V K G | E EXHAUSTED | SH_ON; ANYROM (K_ANY or G_FLIRT/G_TOG+ or V_FLIRT/V_TOG+); after A1, A2, A3 |
| SR35 | L X | E WEARY | SH_ON; Lucien-Xelzaz intro done (BPUFXelzazAndLucienInteractions 077DC4, first scene) [UNC stage] |
| SR36 | S P | E CAMP + NIGHT + TIRED+ | SH_ON; SERANA_F; S_VAMP |
| SR37 | K I | E CAMP + NIGHT (Luna "asleep" is flavour; player sleeping NOT required, as W12) | K_ANY; KaiandInigo stage >= 10 |
| SR38 | G P | E WOKE_WELLRESTED + MORNING | SH_ON |
| SR39 | L K | E CAMP + NIGHT + COLD | FF_ON; after the Lucien-Kaidan scenes (JRLucienFollowerKaidanScene1 done) [UNC] |
| SR40 | C X | E FREEZING + SNOW | FF_ON; R18 played |
| SR41 | X P | E FREEZING | FF_ON |
| SR42 | G K | E COLD + SNOW | FF_ON; after A1 |
| SR43 | V L | E FREEZING + SNOW | FF_ON; after C1 |
| SR44 | L C | E COLD + SNOW + WALK:15 | FF_ON; after R11 |
| SR45 | K I | E FREEZING | FF_ON; KaiandInigo stage >= 10 |
| SR46 | R A | E FREEZING + SNOW | FF_ON; ASHE_F; ASHE_REVEAL |
| SR47 | P K | E FREEZING + SNOW | FF_ON; K_CRUSH |
| SR48 | V G | E FREEZING + SNOW | FF_ON; after A3 |
| SR49 | R K | E FREEZING + SNOW | FF_ON; after B1 |
| SR50 | I X | E CAMP + FREEZING | FF_ON; after X6 |
| SR51 | P K | E FREEZING + SNOW | FF_ON; K_TOG+ |
| SR52 | L P | E COLD | FF_ON |
| SR53 | C P | E FREEZING + SNOW | FF_ON |
| SR54 | R V | E SOAKED | FF_ON; after B14 or the Val-Remi intro in AX ValSerano.esp |
| SR55 | P K | E SOAKED | FF_ON; K_TOG+ |
| SR56 | G X | E SOAKED + COLD | FF_ON; after X1 |
| SR57 | X A | E SOAKED | FF_ON; ASHE_F; ASHE_REVEAL |
| SR58 | L K | E WET + WALK:5 | FF_ON; after the Lucien-Kaidan scenes [UNC] |
| SR59 | G R | E DRIED | FF_ON; after the "Gore's Feet" talk (PY319 chain) |
| SR60 | P I | E DRIED | FF_ON |
| SR61 | K X | E THAW:FREEZING | FF_ON; after C3 |
| SR62 | P G | E THAW | FF_ON |
| SR63 | R X P | E HOTMEAL + AFTERCOLD | SH_ON; FF_ON; Remi/Xel not fallen out |
| SR64 | V K | E HOTDRINK + AFTERCOLD | SH_ON; FF_ON; after A2 |
| SR65 | X C | E HOTMEAL | SH_ON; R18 played |
| SR66 | L G | E BLIZZARD_INN | FF_ON; after L1 |
| SR67 | P K | E BLIZZARD_INN | FF_ON; K_TOG+ |
| SR68 | S I | E BLIZZARD_INN | FF_ON; SERANA_F; S_VAMP |
| SR69 | X V P | E BLIZZARD_INN | FF_ON; after X4 |
| SR70 | A G | E THAW:FREEZING | FF_ON; ASHE_F; ASHE_REVEAL |
| SR71 | P K | E PITCH | — |
| SR72 | G V | E PITCH | after A3 |
| SR73 | R L | E PITCH | after B10 |
| SR74 | K G | E TENT_NIGHT | K_ANY and (G_FLIRT or G_TOG+) |
| SR75 | V G P | E TENT_NIGHT | (V_FLIRT or V_TOG+) and (G_FLIRT or G_TOG+) |
| SR76 | S A | E TENT_NIGHT | SERANA_F; S_VAMP; S_ROM_ON and S_KISS; ASHE_F; ASHE_REVEAL; A_ANY |
| SR77 | G S | E TENT_NIGHT | (G_FLIRT or G_TOG+); SERANA_F; S_VAMP; S_ROM_ON and S_KISS |
| SR78 | A K | E TENT_NIGHT | K_ANY; ASHE_F; ASHE_REVEAL; A_ANY |
| SR79 | C K | E FIREWOOD | after R1 |
| SR80 | I G | E FIREWOOD + SNOW | G_FLIRT or G_TOG+; after C2 |
| SR81 | K X | E COOKPOT | after C3 |
| SR82 | R X P | E COOKPOT | Remi/Xel not fallen out; Remi's "Real Nord Food" quest done [UNC: HLIORemi quest EditorID] |
| SR83 | A L | E COOKPOT | ASHE_F; ASHE_REVEAL |
| SR84 | I C | E CAMP (NEARFIRE) | after R13 |
| SR85 | K P | E CAMP + NIGHT (NEARFIRE) | BRYNJAR |
| SR86 | R X P | E DISEASE:Rockjoint | Remi/Xel not fallen out |
| SR87 | R G | E DISEASE:Ataxia | after the Gore-Remi meet (B15 chain or GORE.esp intro) |
| SR88 | K X | E DISEASE_NEW | K_ANY; after C3 |
| SR89 | I P | E DISEASE_NEW (first 3 game hours) | — |
| SR90 | L X | E DISEASE_CURED | Lucien-Xelzaz intro done [UNC stage] |
| SR91 | C A | E DISEASE:any | ASHE_F; ASHE_REVEAL |
| SR92 | G V P | E FOODPOISON | SH_ON; after A3 |
| SR93 | S P | E VAMP_THIRST | LUNA_VAMP; SERANA_F; S_VAMP |
| SR94 | K S | E VAMP_THIRST | LUNA_VAMP; K_ANY; SERANA_F; S_VAMP |
| SR95 | G I | E BEAST_BACK | LUNA_WOLF; after C2 |
| SR96 | C P | E BEAST_BACK | LUNA_WOLF |
| SR97 | X S | E HOTMEAL or COOKPOT | SERANA_F; S_VAMP |
| SR98 | S G | E MORNING after CAMP + NIGHT | SERANA_F; S_VAMP |
| SR99 | R A P | E CAMP + NIGHT | ASHE_F; ASHE_REVEAL |
| SR100 | P K | E ALLGOOD | SH_ON; FF_ON; K_TOG+ |

## 4. Open items for the build
- Frostfall `_Frost_ExposureLevel` and `_Frost_WetLevel` value meanings, and `FrostfallRunning` "running" value: read FrostUtil.psc / `_Frost_ConfigQuest` before wiring.
- SunHelm stage spells: the controller can test `Player.HasSpell()`; confirm SunHelm adds them as spells (not as abilities applied via a hidden quest) on a live save.
- MGEF FormIDs behind `_SHSoupWarmthSpell` 7B2A1F and `_SHBeverageWarmthSpell` A1738A for the HOTMEAL / HOTDRINK checks.
- Campfire tent detection (PITCH / TENT_NIGHT) and cooking-pot keyword; Firewood01 FormID.
- `PlayerVampireQuest` staging under this load order's vampire setup.
- Lucien pair intro stages (SR27, SR35, SR39, SR58, SR90) and Remi's Real Nord Food quest (SR82).
