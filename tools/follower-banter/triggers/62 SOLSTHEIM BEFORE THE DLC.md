# 62 SOLSTHEIM BEFORE THE DLC - trigger rows (prefix SL, SL1-SL60, 60 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\62 SOLSTHEIM BEFORE THE DLC.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4 and 8, `research\triggers\vanilla_gates.md` (B1 "Arrived on Solstheim"), `research\content\dlc_cc_missives_3dnpc.md` (DLC2MQ01 stage list, Dragonborn silence zones), `research\triggers\others_block.md` (Redcap 7b/7d, Lucien 6b, Remi 3, Xelzaz 4), `triggers\10 DRAGONBORN SOLSTHEIM.md`, `triggers\31 CIVIL WAR.md` (`LOC:GreyQuarter`), `triggers\57 INNS AND TOWN LIFE.md` (Cornerclub location), `triggers\10b DRAGONBORN 2.md` (`GORE_READS`), `triggers\20 DAWNGUARD.md` (Serana/Ashe codes).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event.

Every row with S also needs `SERANA` and Serana Free; every row with A needs `ASHE_HIRED` and Ashe Free (20 DAWNGUARD.md, 49 ASHE.md).

## 1. The file-wide gate: before the Dragonborn DLC starts

**Every SL row carries `PRE_DLC2`.**
- `PRE_DLC2` = `GetStageDone DLC2MQ01 (017F8E:Dragonborn.esm) 5 == 0` (the masked cultists have not attacked yet) AND `GetStageDone DLC2MQ01 20 == 0` (never arrived on Solstheim) AND player `GetInWorldspace DLC2SolstheimWorld (000800:Dragonborn.esm) == 0`.
  - Stage 5 = cultist attack, 7 = note read, 20 = arrived on Solstheim: CONFIRMED in dlc_cc_missives_3dnpc.md (DLC2MQ01 row) and vanilla_gates.md B1 (stage 20).
  - **[UNC]** What starts DLC2MQ01 in vanilla (the ambush trigger's own conditions) was not traced, and whether sailing on the Northern Maiden before the ambush sets stage 20 without 5. The `20 not done` and worldspace checks cover both cases, so the file goes quiet the moment either happens. Stages never roll back, so these talks can never return later.
- The Dragonborn silence zones (10 DRAGONBORN SOLSTHEIM.md extra rules) cannot overlap this file, because they all start at DLC2MQ01 5 or later.

## 2. Other gate codes

Reused: `K_CRUSH` (TRIGGERS.md section 4), `SERANA`, `SER_VAMP`, `ASHE_HIRED`, `ASHE_Q1` (20 DAWNGUARD.md / 33 DARK BROTHERHOOD.md), `GORE_READS` (10b DRAGONBORN 2.md, [UNC] there), pair codes `KI`, `LI`, `LX`, `RX`, `LK` (11 LEGACY OF THE DRAGONBORN.md; `LK` as in 53b RIVALRY 2.md).

New here:
- `RC_HOMESICK` = Redcap has not started his own trip home: `GetStageDone FA01RedcapSolstheimStartQ (0D0784:FA01RedcapFollower.esp) 10 == 0` AND `GetQuestCompleted 0D0784 == 0`. That quest is RunOnce and not start-enabled (others_block.md 7b), so this is "Back to the Rock" not begun. **[UNC: that 10 is its first real stage; others_block lists its window as 10..19]**
- `LUC_LETTER` = Lucien has his father's letter but has not gone into the ruin: `GetStage JRLucienPersonal1 (2B13ED:Lucien.esp) >= 30 AND < 35` (others_block.md 6b: 30 = letter received, 35+ = inside Dumzbthar, which is blocked).
- `REMI_VAL_BIZ` = Remi and Val have gone into business: `HLIOValFirstProfitDone (9D8D47:HLIORemi.esp) == 1` (val.md 5A).
- `REDCAP_REC` = `FA01RedcapRecruited (00AA02:FA01RedcapFollower.esp) == 1`.

Locations and events:
- `LOC:WindhelmDocks` = player in the Windhelm docks exterior (the stretch with the Northern Maiden and the Argonian Assemblage). **[UNC: vanilla location FormID; fallback = in Windhelm's exterior worldspace cell block and within 2500 units of Gjalund Salt-Sage or the Northern Maiden ship reference]**
- `LOC:GreyQuarter` = as 31 CIVIL WAR.md (vanilla has no separate location; proxy defined there).
- `LOC:Cornerclub` = `WindhelmNewGnisisCornerclubLocation` (57 INNS AND TOWN LIFE.md). `AFTER:Cornerclub` = the player has been in it this game (controller flag), talk fires within the next in-game day.
- `CITY:Windhelm` (TRIGGERS.md section 4). `AFTER:Windhelm` = the player has been in Windhelm this game (controller flag).
- `EASTMARCH` = exterior in Eastmarch hold (`EastmarchHoldLocation`), not in a settlement. **[UNC FormID]**
- `COAST:North` = exterior, in Winterhold or Eastmarch hold, within ~1500 units of the northern sea shore. **[UNC proxy: no vanilla condition; use a short list of coast location/marker refs, or player Y coordinate north of Windhelm plus `IsSwimming`-free shoreline check]**
- `WINDY` = `GetWindSpeed >= 0.5` **[UNC threshold, as STORM in TRIGGERS.md]**.
- `GREY_MORNING` = `MORNING` and `IsCloudy`.
- `E SNOW`, `E CAMP`, `E exterior`, `E CAVE`, evening = hour 18..21 exterior.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| SL1 | P X | E LOC:WindhelmDocks | PRE_DLC2 |
| SL2 | G V | E LOC:WindhelmDocks | PRE_DLC2; after A3 |
| SL3 | I K | E LOC:WindhelmDocks | PRE_DLC2; KI |
| SL4 | V X | E LOC:GreyQuarter | PRE_DLC2; after X4 |
| SL5 | G V | E LOC:GreyQuarter | PRE_DLC2; after A3 |
| SL6 | P K | E CITY:Windhelm + SNOW | PRE_DLC2 |
| SL7 | G K | E CITY:Windhelm | PRE_DLC2; after A1 |
| SL8 | G R | E LOC:WindhelmDocks | PRE_DLC2; GORE_READS |
| SL9 | A G | E LOC:WindhelmDocks | PRE_DLC2; ASHE_Q1 |
| SL10 | G V | E LOC:GreyQuarter | PRE_DLC2; after A3 |
| SL11 | G K | E LOC:WindhelmDocks | PRE_DLC2; after A1 |
| SL12 | R V | E LOC:GreyQuarter | PRE_DLC2; REMI_VAL_BIZ |
| SL13 | K V | E CITY:Windhelm | PRE_DLC2; after A2 |
| SL14 | P K | E LOC:WindhelmDocks | PRE_DLC2; K_CRUSH |
| SL15 | S X | E CITY:Windhelm | PRE_DLC2; SERANA |
| SL16 | K P | T | PRE_DLC2; AFTER:Cornerclub |
| SL17 | C P | E LOC:WindhelmDocks | PRE_DLC2; RC_HOMESICK |
| SL18 | C G | E CAMP | PRE_DLC2; RC_HOMESICK; after R5 |
| SL19 | C X | T | PRE_DLC2; RC_HOMESICK; after R18 |
| SL20 | C P | E exterior, evening | PRE_DLC2; RC_HOMESICK |
| SL21 | C I | T | PRE_DLC2; RC_HOMESICK; after R13 |
| SL22 | R C | T | PRE_DLC2; RC_HOMESICK; Remi-Redcap intro done (FA01RemiIntroScene 2B6EA1 == 1) |
| SL23 | V C | E CAMP | PRE_DLC2; RC_HOMESICK; after R8 |
| SL24 | C K | T | PRE_DLC2; RC_HOMESICK; after R1; after:SL20 |
| SL25 | I C | T | PRE_DLC2; RC_HOMESICK; after R13 |
| SL26 | L C | T | PRE_DLC2; RC_HOMESICK; after R11 |
| SL27 | C P | T | PRE_DLC2; RC_HOMESICK |
| SL28 | C S | T | PRE_DLC2; RC_HOMESICK; SERANA; SER_VAMP |
| SL29 | A C | T | PRE_DLC2; RC_HOMESICK; ASHE_HIRED |
| SL30 | C P K | E LOC:WindhelmDocks | PRE_DLC2; RC_HOMESICK; after:SL17; after R1 |
| SL31 | X P | T | PRE_DLC2 |
| SL32 | R X | T | PRE_DLC2; RX |
| SL33 | V P | T | PRE_DLC2; AFTER:Windhelm |
| SL34 | L X | T | PRE_DLC2; LX |
| SL35 | V X | T | PRE_DLC2; after X4 |
| SL36 | P X | T | PRE_DLC2 |
| SL37 | G X | T | PRE_DLC2; after X1 |
| SL38 | A X | T | PRE_DLC2; ASHE_Q1 |
| SL39 | R X | T | PRE_DLC2; RX |
| SL40 | K X | T | PRE_DLC2; after C3 |
| SL41 | P I | T | PRE_DLC2 |
| SL42 | P V | E EASTMARCH | PRE_DLC2 |
| SL43 | R L | T | PRE_DLC2; after B10 |
| SL44 | L P | T | PRE_DLC2; LUC_LETTER |
| SL45 | R L | T | PRE_DLC2; LUC_LETTER; after B10 |
| SL46 | S P | T | PRE_DLC2; SERANA |
| SL47 | L I | T | PRE_DLC2; LI |
| SL48 | G K | T | PRE_DLC2; after A1 |
| SL49 | I P | E COAST:North + WINDY | PRE_DLC2 |
| SL50 | G P | T | PRE_DLC2 |
| SL51 | R P | T | PRE_DLC2 |
| SL52 | V K | E COAST:North or CITY:Windhelm, GREY_MORNING | PRE_DLC2; after A2 |
| SL53 | L K | T | PRE_DLC2; LK |
| SL54 | G L | T | PRE_DLC2; after L1 |
| SL55 | G P | E CAMP | PRE_DLC2; AFTER:Windhelm |
| SL56 | L V | E COAST:North | PRE_DLC2; after C1 |
| SL57 | R K | T | PRE_DLC2; after B1 |
| SL58 | P A | T | PRE_DLC2; ASHE_HIRED |
| SL59 | P R | T | PRE_DLC2 |
| SL60 | G V P | E COAST:North | PRE_DLC2; after A3 |

## 4. Notes for the build
- Nothing here names Miraak, the cultists, the Black Books, the sleepwalkers in Raven Rock, the All-Maker Stones' trouble, or Neloth's quests: the party only knows what a Skyrim traveller could hear on the Windhelm docks or read in a book. Neloth and Tel Mithryn are known to Xelzaz by reputation only (SL31, SL34).
- Redcap's talks (Part 2) never assume his tribe is safe, captured or free; he doesn't know yet. Manos is "the Bad Man", only as a fear (SL21).
- Lucien's letter talks (SL44, SL45) stop at JRLucienPersonal1 35, where his own quest takes over (others_block.md 6b).
- Light inventions, flagged for the user: Xelzaz has heard Aryo Avellan's name (SL38, only as a reputation); Kaidan once chased a bounty to the Windhelm docks (SL57); Val's mother read his father's letters (SL42). None touches a quest record.
- Avoided on purpose (covered elsewhere): the sea crossing itself (55 TRAVEL), Val's father and the Cornerclub (57 IN), "which half of me" (37 SQ), Brunwulf (37/41), Sadri's vase and Scouts-Many-Marshes (41b), Mzinchaleft refugees (15b MN241), the cultists' note before sailing (DR2), Skaal horker words (DR219), "close your mouth" in the ash (DR79).
- Luna speaks in 22 of 60 talks (36%). Nobody says "Dragonborn".
