# Story gates and silence rules for the follower-banter mod

This is based on the live load order (profile "DEEZ CS NUTZ - PICTA", 4,166 active plugins). I checked it read-only on 2026-10-18.

Stage numbers come from the winning QUST record. What each stage does was confirmed by reading the stage scripts, using the vanilla sources (CK Platform Extended Scripts.zip), Alternate Perspective's own source, and the overriding mods' sources.

- **[CONFIRMED]**: checked against the records or scripts in this load order.
- **[UNCONFIRMED]**: inferred from vanilla knowledge, or not traced end to end. Test these in game.

All FormIDs are written as `XXXXXX:DefiningMaster`. Never hard-code runtime IDs, because several of these masters are light or late-loading plugins.

---

## PART A: The start, Helgen and the main quest

### A1. Which alternate start is running [CONFIRMED]

- **Alternate Perspective** (`AlternatePerspective.esp`, mod "Alternate Perspective - Alternate Start") is the start mod.
  - Add-ons: `AP - USSEP patch`, `AP - Missile Additional Starts`, `AP - Missile Additional Bruma Starts`, `Alternate Perspective - Gate to Sovngarde Edition`, `AP Solstheim Fix`, `AlternatePerspective - Sev Cut` (+ Voiced / Why I Came To Skyrim / Music / NOTWL / Pocket of Sovngarde / Lux Orbis patches).
  - Authoria script fixes: `Authoria - Papyrus - Misc - Alternate Perspective` (an MQ101 messenger guard and Helgen-end guards; behaviour is unchanged).
- These are **not** active: Live Another Life, Realm of Lorkhan, Skyrim Unbound.
- `Kaidan - Alternate Start Quest.esp` is a Kaidan recruitment quest (`KNewStart`), not a game start.
- `CauseTweakAlternateStart.esp` only changes The Cause (Creation Club).
- `Talos' Tease - Starting Quest` and `Gray Fox Cowl - House of the Thief Start` are side-quest starts.

**How Alternate Perspective works.** AP takes over vanilla **MQ101 `03372B:Skyrim.esm`** itself. MQ101 still starts at game start (stage 0), but the player spawns in AP's start cell (`AP_StartCellQ 4246F9:AlternatePerspective.esp`). From there she picks a start (inns, docks, houses, guilds, Wanted, Left for Dead, Shipwrecked, vampire lairs, and so on).

**Helgen is NOT destroyed at the start.** In AP, Helgen is a living town, with an inn and civilians such as Gunnar, Torolf, Vilod and Matlara, until the player triggers the intro. Helgen only burns through one of these paths:

| Path | Script | Stages set |
|---|---|---|
| Vanilla cart intro (APS_VanillaStart, or sleeping in the Helgen inn bed) | `APMQ101.knockoutPlayer()` | MQ101 3 or 4 → … → **145** → 150 → 160 → 180/190/195 → keep → 900 → 1000 |
| "Skip to Helgen Keep" (shrine or messenger, APS_MQSkipKeep) | MQ101 stage 6 (Imperial) or 7 (Sons) → `QuickStartKeep` → `destroyHelgen()` | **145**, 150, 180, 190, 195 |
| "Helgen Keep (end)" (APS_MQSkipKeepEnd) | `destroyHelgen()` | **145** … 200+(10/20), 250, 550, 700–725 |
| "Skip to MQ105" (APS_MQSkipMQ105Hadvar/Ralof) | `destroyHelgen()` | **145**, 200, 210/220, 250, 500, 800, **1000**, CompleteQuest, then **MQ105 stage 1** |
| APSkipIntro activator | `PrepHelgen()` | **145**, 180, 190, 195, 720 |

#### "Helgen has been destroyed" (works in every path) [CONFIRMED]

```
GetStageDone MQ101(03372B:Skyrim.esm) 145 == 1
```

Every AP route that burns Helgen calls `SetStage(145)`. Stage 145 also turns on AP's "destroyed" swap marker (`APMarker`). Before stage 145, Helgen is intact and populated.

- Do **not** use `GetQuestCompleted MQ101` for this. Most routes never reach stage 1000 until the keep escape is finished.
- "Escaped Helgen / intro fully over" = `GetStageDone MQ101 1000 == 1`.
  - Stage 900 means "escaped", and its script immediately sets 1000.
  - The skip-to-MQ105 path sets 1000 directly.
  - The Helgen-Keep-(end) path reaches 1000 only when the cave exit is finished.
- "Player chose the Imperial side in Helgen" = `GetStageDone MQ101 210` (Imperial) or `220` (Sons). The quickstarts also set these. [CONFIRMED in the AP scripts]

### A2. Main-quest overhauls present [CONFIRMED]

- **At Your Own Pace - Main Quest** (`At Your Own Pace - Main Quest.esp`) overrides MQ103, MQ105Ustengrav and MQ106. It adds `AYOPMQQuest` and the break globals `AYOPMQ103Break`, `AYOPMQ104Break`, `AYOPMQ105Break`, `AYOPMQ301Break` and `AYOPMQBreezehome`.
  - It **delays the next step** (the dragon attack, the Greybeards' summons, and so on). It does **not** renumber any stages, so stage-based gates stay valid. They just fire later.
- **Paarthurnax Quest Expansion** overrides `MQPaarthurnax 03FA16:Skyrim.esm` and the FreeformSkyHavenTemple A/C/D quests.
  - It adds a "talk the Blades round" path: stages 75 / 76 / 99 / 100 / 150.
  - It does **not** touch MQ204, MQ205 or MQ206 (their winners are vanilla or USSEP).
- **Storm the Thalmor Embassy** overrides MQ201. Stages stay vanilla-shaped.
- `Requiem.esp` wins MQ104 and MQ202. The stage list is vanilla, so this is harmless.
- `Delphine's Map Reveals Dragon Mounds.esp` only touches the map.
- Not present: Main Quest Overhaul, Sovngarde overhauls, or Blades-replacer quests.

### A3. Main-quest milestones

| Meaning | Condition | Status |
|---|---|---|
| Learned she is Dragonborn (absorbed the first soul) | `GetStageDone MQ104(02610C:Skyrim.esm) 90 == 1`. The stage 90 script unlocks Fus and sets AllowPlayerShout = 1; its log reads "I absorbed some kind of power". | CONFIRMED |
| …and actually *fought* at the Western Watchtower (not a quickstart) | add `GetStageDone MQ104 80 == 1` (dragon killed). The AP skip-to-MQ105 route runs MQ105 stage 1, which sets MQ104 1/10/30/90/120/150/160/180/200 but **never 80**. | CONFIRMED |
| Western Watchtower done / Thane of Whiterun | `GetStageDone MQ104 160` (log: "I am now a Thane of Whiterun") or `GetQuestCompleted MQ104` (stage 200) | CONFIRMED |
| First shout | `GetStageDone MQ104 90` (Fus taught and unlocked here as a failsafe). Greybeard training: `GetStageDone MQ105(0242BA:Skyrim.esm) 70` (Ro taught) / 76 (Ro unlocked) | CONFIRMED |
| Reached / visited High Hrothgar | `GetStageDone MQ105 20` (stage 20 = "player enters High Hrothgar") | CONFIRMED |
| Greybeards called her Dragonborn | `GetStageDone MQ105 30` (log: Arngeir "believes that I am Dragonborn") | CONFIRMED |
| Way of the Voice finished (Horn of Jurgen returned) | `GetQuestCompleted MQ105` / stage 300 | CONFIRMED |
| Met Delphine (Sleeping Giant) | `GetStageDone MQ106(032926:Skyrim.esm) 30` (log: "Delphine, the innkeeper … is more than she seems"). Stage 5 = told to rent the attic. Stage 50 = "convinced her I'm Dragonborn" after Kynesgrove. | CONFIRMED (AYOP wins MQ106; same stages) |
| Saw Alduin raise a dragon (Kynesgrove) | `GetStageDone MQ106 150` | CONFIRMED |
| Met Esbern | `GetStageDone MQ202(036191:Skyrim.esm) 150`, or MQ203 started (stage 10) | UNCONFIRMED exact stage |
| Found Sky Haven Temple | `GetStageDone MQ203(036192:Skyrim.esm) 230` (stage 230 starts the Alduin's Wall scene) | CONFIRMED |
| Met Paarthurnax | `GetStageDone MQ204(02D515:Skyrim.esm) 95` (Paarthurnax scene starts) or `GetStageDone MQ205(02D516) 10` (log: "I met the master of the Greybeards, the dragon Paarthurnax") | CONFIRMED |
| Learned Dragonrend | `GetStageDone MQ206(036193:Skyrim.esm) 100` | CONFIRMED |
| Paarthurnax killed (Blades' demand) | `GetStageDone MQPaarthurnax(03FA16:Skyrim.esm) 50` | CONFIRMED |
| PQE: refused and convinced the Blades | `GetStageDone MQPaarthurnax 99` or `100` (the player is added back to BladesFaction) | CONFIRMED |
| PQE: Greybeards angry | `GetStageDone MQPaarthurnax 150` | CONFIRMED |
| Peace council held | `GetQuestCompleted MQ302(045923:Skyrim.esm)` / stage 300 | CONFIRMED |
| Entered Sovngarde | `GetStageDone MQ304(046EF1:Skyrim.esm) 10` | CONFIRMED |
| **Alduin defeated** | `GetStageDone MQ305(046EF2:Skyrim.esm) 200` (log: "We fought…"). Use `GetQuestCompleted MQ305` (stage 300) for "back home". MQ306 is the dragons' gathering on the Throat. | CONFIRMED |

---

### A4. Main-quest scenes where banter must be silenced

**The general guard comes first.** It covers about 90% of cases without any quest list. Banter should not fire when:

- the speaking follower `IsInScene == 1`; or
- `IsInDialogueWithPlayer == 1`; or
- player `IsInCombat == 1`; or
- player `IsPCSleeping == 1`; or
- (Papyrus) `Game.IsMovementControlsEnabled() == false` or `Game.IsFightingControlsEnabled() == false`.

Almost every scripted MQ scene disables the player's controls (MQ101, MQ105 270, MQ302 60, MQ303 50/55, MQ305 250, the wedding at stage 20, TG08A 55, DLC1VQ02 8, DLC2MQ06 330 and others).

| Scene | Silence while | Status |
|---|---|---|
| AP start room | `GetQuestRunning AP_StartCellQ(4246F9:AlternatePerspective.esp)` | CONFIRMED |
| Helgen intro (cart, execution, Alduin) | `GetStage MQ101 >= 3` AND `GetStageDone MQ101 145 == 0`. Stage 3 = bed intro; 4 = vanilla start; 6/7 = keep quickstart. | CONFIRMED |
| Helgen escape (town and keep) | `GetStageDone MQ101 145 == 1` AND `GetStageDone MQ101 1000 == 0`. Optionally also require `GetInCurrentLocation HelgenLocation(018A4A:Skyrim.esm)`, but the keep interiors use their own location, so the stage pair alone is safer. | CONFIRMED |
| Western Watchtower dragon | MQ104 `GetStage >= 48 AND < 90` (48 = attack intro; 55 = attack; 60 = dragon; 80 = dead; 85/90 = absorb scene), plus the outro shout 90–130, OR be in `WhiterunWatchtowerLocation(0D9079:Skyrim.esm)` while MQ104 < 160 | CONFIRMED |
| Greybeards' trials | MQ105 `GetStage >= 20 AND < 160` (Einarth / push / Borri / sprint trials) and `>= 240 AND < 300` (outro, Dah taught, controls locked at 270), all in `HighHrothgarLocation(018E34:Skyrim.esm)` | CONFIRMED |
| Kynesgrove (Alduin raises Sahloknir) | MQ106 `GetStage >= 60 AND < 170` | CONFIRMED |
| Thalmor Embassy party | MQ201 `GetStage >= 35 AND < 250` (Delphine takes the follower away; scenes at 35, 140, 180, 200, 220) | CONFIRMED stages / UNCONFIRMED end |
| Sky Haven: Riverwood, Karthspire, puzzle, Alduin's Wall | MQ203 stages 30–65, 110–140, 210–280, and in `SkyHavenTempleLocation(018E42)` | CONFIRMED |
| Throat of the World (Clear Skies, Paarthurnax talk) | MQ204 `GetStage >= 20 AND < 210` while in `ThroatoftheWorldLocation(0192BB)` | CONFIRMED |
| Elder Scroll vision and Alduin fight (Alduin's Bane) | MQ206 `GetStage >= 20 AND < 220` | CONFIRMED |
| Season Unending peace council | MQ302 `GetStage >= 40 AND < 300` and in HighHrothgarLocation (CouncilScene starts at 40; controls lock at 60) | CONFIRMED |
| Dragonsreach trap | MQ301 `GetStage >= 200 AND < 220` | UNCONFIRMED stage range |
| Odahviing talk and flight to Skuldafn | MQ303 `GetStage >= 5 AND < 100`, and 180 (portal scene) | CONFIRMED |
| Sovngarde | `GetQuestRunning MQ304` OR `GetQuestRunning MQ305`, or `GetInWorldspace Sovngarde(02EE41:Skyrim.esm)` | CONFIRMED |
| Return to the Throat (dragons gather) | `GetQuestRunning MQ306(046EF3:Skyrim.esm)` | CONFIRMED |

---

## PART B: Faction, DLC and world gates

### B1. Faction and DLC gates

| Gate | Condition | Status |
|---|---|---|
| Joined the **Imperial Legion** | `GetStageDone CW01A(0D517A:Skyrim.esm) 200`. The stage 200 script says "player has taken oath", then CW02A 10, `CWs.PlayerTookOath(1)` and stop(). `Devotion.esp` wins the record but has no stage-level change. Alternative: `GetStageDone CW02A(02D75C) 10`. | CONFIRMED |
| Joined the **Stormcloaks** | `GetStageDone CW01B(0E2D29:Skyrim.esm) 200` (same CW01 script). Alternative: `GetStageDone CW02B(02610B) 10`. | CONFIRMED |
| Civil War side, faction-based alternative | `GetInFaction CWImperialFaction(02BF9A)` / `CWSonsFaction(02BF9B)` | UNCONFIRMED that the player herself is added; prefer the stage checks above |
| Met **Brynjolf** | `GetStageDone TG00(021556:Skyrim.esm) 8` (log: "Brynjolf … has convinced me to take part"). Earliest possible: TG00 5. | CONFIRMED |
| Joined the **Thieves Guild** | `GetStageDone TG02(02154E:Skyrim.esm) 10`. The stage 10 script adds the player to the TG faction; stage 20 log: "welcomed into the Thieves Guild by Mercer Frey". `thieves guild requirements.esp` wins but keeps the stages. | CONFIRMED |
| Joined the **Dark Brotherhood** | `GetStageDone DB02(01EA51:Skyrim.esm) 50`. Stage 50 runs `AddToFaction(DarkBrotherhoodFaction 01BDB3)`; stage 200 = "officially welcomed by Astrid". Stage 220 = killed Astrid instead (the DBDestroy path). | CONFIRMED |
| **Cicero arrived** at the Sanctuary | `GetStageDone DB03(01EA52:Skyrim.esm) 10` (the stage 10 script starts `pCiceroEndArriveScene`). In DB04 he is fully in residence (`DBScript.CiceroArrive = 3`). He was met earlier on the road at Loreius Farm, through DB01Misc, which is not traced. | CONFIRMED (arrival) |
| Joined the **Companions** | `GetStageDone C00(04B2D9:Skyrim.esm) 100` (`PlayerJoin()`; log: "I have joined the Companions"). Full member (Proving Honor done): `GetStageDone C01(06E803:Skyrim.esm) 200`. Note: FormID `06E803` is the quest with EditorID **C01**. | CONFIRMED |
| Became a **werewolf** | `GetStageDone C03(01CEF4:Skyrim.esm) 25` (log: "…now share their blood as a werewolf"). The C03 script also sets `PlayerIsWerewolf(0ED06C:Skyrim.esm) = 1`. Use the global for "is a werewolf *now*", since the cure quest resets it. | CONFIRMED |
| Harbinger | `GetQuestCompleted C06(01CEF6:Skyrim.esm)` / stage 200 | CONFIRMED |
| Joined the **College** | `GetStageDone MG01(01F251:Skyrim.esm) 30`. The stage 30 script runs `SetFactionRank(CollegeFaction 01F259, 0)` (log: "allowed to join"). The winner is `Authoria - Master Patch - AYOP CoW.esp`; the stages are unchanged. | CONFIRMED |
| Became **Arch-Mage** | `GetStageDone MG08(01F258:Skyrim.esm) 200` (adds `CollegeofWinterholdArchMageFaction 103372`, CollegeFaction rank 6). Alternative: `GetInFaction CollegeofWinterholdArchMageFaction`. | CONFIRMED |
| **Serana** freed / travelling with her | Freed: `GetStageDone DLC1VQ01(00352A:Dawnguard.esm) 20`. Taking her home (she follows): `GetStageDone DLC1VQ02(002F65:Dawnguard.esm) 5`. | CONFIRMED |
| **Serana** joined as a companion for the questline | DLC1VQ03Vampire `004C3D:Dawnguard.esm` or DLC1VQ03Hunter `0098CB:Dawnguard.esm` started (stage 10?). These FormIDs come from the script names. | UNCONFIRMED stage |
| Serana currently following | on Serana: `GetInFaction CurrentFollowerFaction(05C84E:Skyrim.esm) >= 0`, or `IsPlayerTeammate`, with subject `GetIsID DLC1Serana(002B6C:Dawnguard.esm)` | CONFIRMED form IDs |
| Chose a Dawnguard side | Vampire: `GetStageDone DLC1VQ02 40`. Dawnguard: `GetStageDone DLC1VQ02 25` / 30. | CONFIRMED |
| **Arrived on Solstheim** | `GetStageDone DLC2MQ01(017F8E:Dragonborn.esm) 20` (stage 20 script: "player has arrived on Solstheim"). Live check: `GetInWorldspace DLC2SolstheimWorld(000800:Dragonborn.esm)`. | CONFIRMED |
| **First Black Book read** | `GetStageDone DLC2MQ02(017F8F:Dragonborn.esm) 60` (log: "When I read it, I was transported…"). Apocrypha live check: `GetInWorldspace DLC2ApocryphaWorld(01C0B2:Dragonborn.esm)`. | CONFIRMED |
| Miraak defeated | `GetStageDone DLC2MQ06(0179D7:Dragonborn.esm) 550` | CONFIRMED |
| Finished **A Night to Remember** | `GetQuestCompleted DA14(01BB9B:Skyrim.esm)` / stage 200 (log: "'Sam' turned out to be … Sanguine") | CONFIRMED |
| Married | `GetStageDone RelationshipMarriage(074793:Skyrim.esm) 100`, or `GetInFaction PlayerMarriedFaction(0C6472)` on the spouse | UNCONFIRMED (stage 100 is set from the wedding stage 100) |

### B2. Location, weather, time, camp and water checks

**Location keywords.** Use the condition `LocationHasKeyword <kw>` on the player (it reads the current location). All of these are from Skyrim.esm and confirmed:

| Place | Keyword |
|---|---|
| Inn | `LocTypeInn 01CB87` (modded inns usually carry it; AP inns are vanilla locations) |
| City | `LocTypeCity 013168` (the five hold capitals and Riverwood?). Also `LocTypeTown 013166`, `LocTypeSettlement 013167`, `LocTypeHoldCapital 0868E2`, `LocTypeHabitation 039793` |
| Dungeon | `LocTypeDungeon 0130DB`; `LocTypeClearable 0F5E80` |
| Dwemer ruin | `LocTypeDwarvenAutomatons 0130E3` (there is no "DwarvenRuin" keyword in this order); `LocTypeFalmerHive 0130E4` for the deep ones |
| Crypt / barrow | `LocTypeDraugrCrypt 0130E2`; `LocTypeDragonPriestLair 0130E1`; `LocTypeCemetery 01CD58` |
| Others | `LocTypeBanditCamp 0130DF`, `LocTypeVampireLair 0130EB`, `LocTypeWarlockLair 0130EC`, `LocTypeForswornCamp 0130EE`, `LocTypeHagravenNest 0130E6`, `LocTypeGiantCamp 0130E5`, `LocTypeAnimalDen 0130DE`, `LocTypeMilitaryFort 0130E7`, `LocTypeDragonLair 0130E0`, `LocTypeOrcStronghold 0130E9`, `LocTypeTemple 01CD56`, `LocTypeCastle 01CD57`, `LocTypeJail 01CD59`, `LocTypeGuild 01CD5A`, `LocTypeShip 01CD5B`, `LocTypeStore 01CB86`, `LocTypeHouse 01CB85`, `LocTypePlayerHouse 0FC1A3`, `LocTypeMine 018EF1`, `LocTypeFarm 018EF0` |

**Interior or exterior.** Use `IsInInterior`.

**Weather:**
- Use `IsRaining`, `IsSnowing`, `IsPleasant` and `IsCloudy` (no parameters). They follow the current weather's classification.
- Storms: there is no vanilla "storm" flag. Use `IsRaining == 1 AND GetWindSpeed >= 0.6`. The threshold is UNCONFIRMED; tune it in game.
- Picta, Seasonal Weathers Framework, Dynamic Wind and BDS change the weathers but keep their classifications. Winter rain is suppressed by the Picta seasonal patch, so in winter snow conditions fire instead of rain.
- Frostfall's live `_Frost_WetLevel(06458D:Frostfall.esp)` can serve as a "soaked" proxy. Gate it on `FrostfallRunning(06DCFB:Frostfall.esp) == 2`; the running value is UNCONFIRMED. Note that `SunHelmForceDisableCold.esp` is also active, so check which cold system is actually running before relying on Frostfall.

**Time:** `GetCurrentTime` (0–24, game hour). Night is roughly `>= 20 OR < 5`. Global `GameHour 000038:Skyrim.esm` also works.

**At camp:**
- Campfire (`Campfire.esm`) and Frostfall are active. SunHelm (`SunHelmSurvival.esp`) and `Kaidan - Survival` tents are also active.
- Near a lit fire: `_Frost_NearFire(064AFD:Frostfall.esp) == 1`, with `_Frost_CurrentHeatSourceSize(064AFC)` and `_Frost_CurrentHeatSourceDistance(064AFB)` alongside it.
- Sheltered or in a tent: `_Frost_IsTakingShelter(068118:Frostfall.esp)`.
- Campfire's own Papyrus API (`CampUtil.GetCurrentTent()` and similar) ships inside Campfire.bsa. I did not extract it, so its exact functions are UNCONFIRMED.
- A simple, robust option: in an exterior, not in a habitation location, and `_Frost_NearFire == 1`. UNCONFIRMED that `_Frost_NearFire` updates when Frostfall's exposure system is off.

**Near water:**
- There is no vanilla condition for this. Use `IsSwimming` for in-water.
- PO3 Papyrus Extender is installed. It offers `PO3_SKSEFunctions.IsActorInWater(actor)`, `IsActorUnderwater` and `IsRefInWater`; use these from a Papyrus poll.
- Wade In Water / WadeInWaterRedone are active too.

---

### B3. Quest states where **all** follower chatter should pause

| Situation | Condition | Status |
|---|---|---|
| **Wedding ceremony** | `GetQuestRunning RelationshipMarriageWedding(07404E:Skyrim.esm)` AND `GetStage >= 10 AND < 500` (10 = ceremony set up; 20 = controls locked; 100/150/200 = vows or outcomes; 500/1000 = cleanup) | CONFIRMED |
| **Civil War city siege** | `GetQuestRunning CWSiege(0954E1:Skyrim.esm)` (the umbrella quest for Whiterun, Markarth, Riften, Solitude and Windhelm battles), or `CWSiegeObj(096E71)` running | CONFIRMED form IDs / UNCONFIRMED that CWSiege stops right after the battle |
| Civil War fort battles | `GetQuestRunning CWFortSiegeFort(083042:Skyrim.esm)` | CONFIRMED form ID |
| Civil War finale (Ulfric/Tullius death scene) | `GetQuestRunning CWFinale(0D1444:Skyrim.esm)` AND `GetStage >= 300 AND < 500` (scenes at 330 and 340) | CONFIRMED scenes / UNCONFIRMED range start |
| Civil War oath scene | CW01A/CW01B `GetStage >= 160 AND < 200` | CONFIRMED |
| Message to Whiterun war scenes | CW03(0D661C) stages 20, 100 and 225 | CONFIRMED |
| **Thieves Guild: Snow Veil betrayal** | TG05(021551) `GetStage >= 10 AND < 200` | CONFIRMED |
| TG: vault reveal / Mercer chase | TG07(021553) `GetStage >= 10 AND < 40` (Flagon vault scene); TG07 40–60 is the Riftweald search | UNCONFIRMED exact scene stage |
| TG: Nightingale oath | TG08A(057F99) `GetStage >= 40 AND < 60` (oath scene at 55; controls locked) | CONFIRMED |
| TG: Mercer fight (Irkngthand) | TG08B(021554) `GetStage >= 40 AND < 60` | CONFIRMED |
| TG: Twilight Sepulcher / Nocturnal | TG09(021555) `GetStage >= 30 AND < 200` | CONFIRMED |
| TG leadership ceremony | TGLeadership(0D7D69) `GetStage >= 30 AND < 200` | CONFIRMED |
| **DB: abandoned shack** | DB02(01EA51) `GetStage >= 10 AND < 40` (the player is kidnapped; followers are not present) | CONFIRMED |
| DB: eavesdropping on Cicero / Night Mother | DB04(01EA53) `GetStage >= 10 AND < 50` | CONFIRMED |
| DB: Sanctuary burning | DB10(03CEDA) `GetQuestRunning` (winner is `Kaidan - Immersive Features.esp`; stages are vanilla) | CONFIRMED |
| **DB: Emperor** | DB11(01EA59) `GetStage >= 5 AND < 200` (Katariah) | CONFIRMED |
| DB: wedding assassination | DB05(01EA54) running AND in the Solitude Temple of the Divines | UNCONFIRMED (no scene lock) |
| **Companions: Underforge blood ritual** | C03(01CEF4) `GetStage >= 15 AND < 25` | CONFIRMED |
| Companions: induction ceremony | C02(06E804) `GetStage >= 10 AND < 200` | CONFIRMED stages / UNCONFIRMED scene span |
| Companions: Glenmoril witches | C04(01CEF5) `GetStage == 20` and in the Glenmoril Coven location. There is no scripted scene; just suppress lighthearted banter. | UNCONFIRMED (loc) |
| Companions: Kodlak funeral and Ysgramor's tomb | C06(01CEF6) stage 10 (funeral) and `>= 30 AND < 200` (tomb ritual) | CONFIRMED |
| College: Ancano / Eye of Magnus | MG05(01F255) `GetStage >= 20 AND < 50`; MG08(01F258) `GetStage >= 10 AND < 200` | CONFIRMED |
| **Dawnguard: Harkon's offer** | DLC1VQ02 `GetStage >= 8 AND < 20` (controls locked at 8) | CONFIRMED |
| Dawnguard: final battle | DLC1VQ08(007C25) running | CONFIRMED form ID |
| Soul Cairn | DLC1VQ05(002850) running | CONFIRMED form ID |
| **Dragonborn: Miraak finale** | DLC2MQ06(0179D7) `GetStage >= 330` and not completed | CONFIRMED |
| Dragonborn: Apocrypha | `GetInWorldspace DLC2ApocryphaWorld` (solo areas) | CONFIRMED form ID |
| OStim scene | OStim (`OStim.esp`) is active; check `OActor.IsInOStim(actor)` (the API name is UNCONFIRMED) | UNCONFIRMED |

---

### Notes and caveats

1. **AP keeps Helgen alive.** Any banter about "Helgen burned" must gate on MQ101 145, not on game start. A player can be weeks into a playthrough with Helgen intact and the main quest not started.
2. **AP skip-to-MQ105 fakes MQ104.** It sets MQ104 90/160/200 without the watchtower fight. Use MQ104 80 for "she saw the first dragon die".
3. **AYOP delays only.** Do not assume MQ105 follows MQ104 quickly.
4. **Paarthurnax QE** adds the "spare him and keep the Blades" ending (MQPaarthurnax 99/100). Write the Blades banter for both branches.
5. **Other banter systems are present.** Inigo, Kaidan (with Auri↔Kaidan banter), Auri, Lucien, Serana Dialogue Add-on, Ashe and others. Add `IsInScene == 0` on **every** participant, so lines do not collide with their own scenes.
6. **Load-order winners for the gate quests:**
   - USSEP: most quests.
   - `Authoria - Haberdashery.esp`: C01, TG09, DLC1NPCMentalModel.
   - `Authoria - Master Patch - AYOP CoW.esp`: MG01–MG04, MG08.
   - `TG Alternative Endings.esp`: TG08A, TGLeadership.
   - `Authoria - Output - Synthesis Gameplay.esp`: MQ101, MQ102.
   - All of them keep the vanilla stage indices, which I checked.
