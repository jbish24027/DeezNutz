# 51 SEASONS WEATHER TIME MORE - trigger rows (prefix WT, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\51 SEASONS WEATHER TIME MORE.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4 and the "Seasons, holidays, lost" block, `triggers\48 SERANA.md` and `triggers\49 ASHE.md` (Free() rows and Serana/Ashe gate codes reused unchanged), the bibles.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana and Ashe use the Free() rows in `20 DAWNGUARD.md` section 1. Every row with S also needs `SERANA`; every row with A also needs `ASHE_HIRED`. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment; the 60 s weather/time poll in TRIGGERS.md section 1 drives every weather, hour and date check here).

## Gate codes used in this file

Reused (TRIGGERS.md section 4, 48 SERANA.md, 49 ASHE.md, same meaning): `K_CRUSH`, `K_ANY`, `K_TOG+`, `V_FLIRT`, `BRYNJAR`, `SERANA`, `SER_VAMP`, `SER_CURED`, `DG_HARKON`, `DG_CAIRN`, `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, and pair-intro chains `after:<ID>`.

Calendar (vanilla globals `GameMonth` 0 = Morning Star .. 11 = Evening Star, `GameDay`; same rule as the S/H rows in TRIGGERS.md):
- `SEASON:<name> start` = first 5 days of the season's first month, else any day of that season if missed; once per season per year. Spring = months 2-4 (first month 2), summer 5-7 (5), autumn 8-10 (8), winter 11, 0, 1 (11).
- `SEASON:<name> any` = any day in that season's months.
- `date mM dD` = `GameMonth == M` and `GameDay` is D or D+1. Holidays used here (standard TES calendar, same as Holidays.esp `_HolidayQuestScript.CheckDate`):
  - South Wind's Prayer `m0 d15`; New Life `m0 d1`; Heart's Day `m1 d16`; Jester's Day `m3 d28`; Second Planting `m4 d7`; Mid Year `m5 d16`; Merchant's Festival `m6 d10`; Sun's Rest `m6 d20`; Harvest's End `m7 d27`; Tales and Tallow `m8 d3`; Witches Festival `m9 d13`; Warriors Festival `m10 d20`; North Wind's Prayer `m11 d15`; Saturalia `m11 d25`; Old Life `m11 d30`.
  - **[UNC]** whether Holidays.esp stages an event on South Wind's Prayer, Second Planting, Sun's Rest, Tales and Tallow and North Wind's Prayer. The date check works without it, and no line refers to anything the mod would place.

Weather (existing codes from TRIGGERS.md: `RAIN`, `SNOW`, `STORM`, `WIND` (31 CIVIL WAR.md), `AURORA`, `CLEARNIGHT`, `CAMP`, `INN`, `WILD`, `MORNING`, `PREDAWN`, `NIGHT`). New here:
- `THUNDER` = `STORM` with `IsRaining` (current weather classification Rain and wind >= 0.6). **[UNC: same proxy as STORM; a weather FormList with lightning is better if the weather mod has one]**
- `BLIZZARD` = `STORM` with `IsSnowing`.
- `FOG` = exterior and the current weather is in a new FormList `FB_FogWeathers`. **[UNC: build the list from the load order's weather mod (fog-type WTHRs, plus vanilla SkyrimFog / SkyrimMistyFog families); no vanilla condition]**
- `RAINSTART` = poll sees `IsRaining` go from 0 to 1 this tick (weather transition into rain), exterior.
- `AFTERRAIN` = exterior, `IsRaining == 0` now, `IsPleasant` or cloudy, and the poll saw rain within the last 1 game hour.
- `HEAT` = summer months (5-7), exterior, hour 12..16, `IsPleasant`, player not in a snowy region: in Whiterun Hold, Falkreath Hold, the Rift or the Reach (hold location GetInCurrentLoc), or in a Cyrodiil/Elsweyr worldspace. **[UNC: hold-location list; Sun's Height/Last Seed only would also be fine]**
- `FROST1` = first `MORNING` (hour 5..9) in an exterior on or after 1st of Frostfall (m9) each year; once per year (`FB_FrostYear` global stores the year it played). **[UNC: no frost check; the date is the proxy]**
- `COLDNIGHT` = `NIGHT` and (winter months or `SNOW` or player in Winterhold/the Pale/Eastmarch hold, or Solstheim north).

Time of day (`GetCurrentTime`, exterior unless noted):
- `SUNSET` = hour 18.5..20.5, not raining or snowing. `SUNRISE` = hour 5.5..7.5, not raining or snowing. `DUSK` = hour 19..22.
- `MIDNIGHT` = hour 23.5..1.5. `LATENIGHT` = hour 1.5..4 (interior allowed). `AFTERNOON` = hour 13..16.
- `CLEARDAY` = hour 9..17, `IsPleasant`.

Other:
- `ANNIV` = `GameDaysPassed >= FB_FirstTalkDay + 365`, where `FB_FirstTalkDay` is a new global set by the controller the first time any banter talk plays. **[UNC: new global]**
- `after:<ID>` = talk ID already played. `after:<ID>+7d` = and at least 7 game days since it played.
- Pair intros named in rows: `KaiandInigo>=10` (Kaidan and Inigo Meet.esp, as K4), `Luc-Kai intro` (Lucien's own Kaidan scene 1 played, as K5), `Luc-Inigo intro` (`JRLucienInigoRank` 7638C2:Lucien.esp >= 2), `Remi-Gore intro` (HLIOGoreBanter stage >= 1), `Remi-Xel intro` (BPUFXelzazAndRemielInteractions stage 11 done), `Xel-Luc intro` (BPUFXelzazAndLucienInteractions intro done, as DR122), `Remi-Redcap intro` (`FA01RemiIntroScene` 2B6EA1:FA01RedcapFollower.esp == 1), `R18` (Redcap-Xelzaz apology, as TRIGGERS.md).

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| WT1 | A K | T | SEASON:spring start; ASHE_REVEAL; after:AS1 |
| WT2 | S P | T | SEASON:spring start; SERANA |
| WT3 | C V | T | SEASON:spring start; after:R8 |
| WT4 | R K | T | SEASON:spring start; BRYNJAR; after:B1 |
| WT5 | I A | T | SEASON:summer start; ASHE_REVEAL; after:AS6 |
| WT6 | S G | T | SEASON:summer start; SER_VAMP; after:SE2 |
| WT7 | L P | E CLEARDAY | SEASON:summer start |
| WT8 | X A | T | SEASON:autumn start; after:AS7 |
| WT9 | C K | E exterior WILD | SEASON:autumn start; after:R1 |
| WT10 | R P | T | SEASON:autumn start |
| WT11 | S K | T | SEASON:winter start; SER_VAMP; after:SE1 |
| WT12 | V A | E exterior | SEASON:winter start; ASHE_REVEAL; after:AS3 |
| WT13 | I X | T | SEASON:winter start; after:X6 |
| WT14 | K P | T | SEASON:winter start; K_CRUSH |
| WT15 | K X | T | date m0 d15; after:C3 |
| WT16 | R P | T | date m0 d15 |
| WT17 | V X | E MORNING | date m0 d1; after:X4 |
| WT18 | I P | T | date m0 d1 |
| WT19 | L I | T | date m1 d16; Luc-Inigo intro |
| WT20 | K P | T | date m1 d16; K_TOG+ |
| WT21 | L P | T | date m3 d28 |
| WT22 | A K | T | date m3 d28; ASHE_REVEAL; after:AS1 |
| WT23 | C G | E exterior | date m4 d7; after:R5 |
| WT24 | V S | T | date m5 d16; after:SE3 |
| WT25 | R A | E CITY (any) | date m6 d10; ASHE_REVEAL; after:AS4 |
| WT26 | V K P | E WILD | date m6 d20; after:A2 |
| WT27 | I R | E CLEARDAY | date m6 d20; after:B6 |
| WT28 | X S | E CAMP or INN | date m7 d27; SER_CURED; after:SE4 |
| WT29 | I C | E NIGHT | date m8 d3; after:R13 |
| WT30 | L S P | E NIGHT | date m8 d3; DG_CAIRN; after:SE5 |
| WT31 | R G P | T | date m9 d13; Remi-Gore intro |
| WT32 | L K | E CITY (any) | date m10 d20; Luc-Kai intro |
| WT33 | G L | T | date m11 d15; after:L1 |
| WT34 | C A | T | date m11 d15; after:AS12 |
| WT35 | A G | T | date m11 d25; after:AS2 |
| WT36 | C S | T | date m11 d25; SER_VAMP; after:SE6 |
| WT37 | K S | E NIGHT | date m11 d30; BRYNJAR; DG_HARKON; after:SE1 |
| WT38 | V P | E THUNDER | — |
| WT39 | C L | E THUNDER | after:R11 |
| WT40 | K A | E THUNDER | ASHE_Q1; after:AS1 |
| WT41 | R G P | E THUNDER | Remi-Gore intro |
| WT42 | V I | E WIND | after:I1 |
| WT43 | L X | E WIND | Xel-Luc intro |
| WT44 | A C | E FOG | after:AS12 |
| WT45 | G K P | E FOG | K_TOG+; after:A1 |
| WT46 | S K | E FOG | SER_VAMP; K_ANY; after:SE1 |
| WT47 | R C | E BLIZZARD | Remi-Redcap intro |
| WT48 | I P | E BLIZZARD | — |
| WT49 | C S | E SNOW | after:SE6 |
| WT50 | L X A | E SNOW | after:WT8; Xel-Luc intro; after:AS8 |
| WT51 | L G | E HEAT | after:L1 |
| WT52 | I K | E HEAT | KaiandInigo>=10 |
| WT53 | X P | E HEAT | — |
| WT54 | R L | E FROST1 | after:B10 |
| WT55 | I P | E AFTERRAIN | — |
| WT56 | C R | T | SEASON:summer any; after:WT23+7d; Remi-Redcap intro |
| WT57 | V K P | E SUNSET | after:A2 |
| WT58 | V S | E SUNSET | SER_VAMP; after:SE3 |
| WT59 | V K P | E SUNSET | V_FLIRT; K_CRUSH; after:WT57 |
| WT60 | K G | E PREDAWN + CAMP | after:A1 |
| WT61 | X G | E SUNRISE + IsPleasant | after:X1 |
| WT62 | I C | E CLEARNIGHT | after:R13 |
| WT63 | X P | E DUSK | — |
| WT64 | R G P | E CLEARNIGHT | Remi-Gore intro |
| WT65 | L S | E CLEARNIGHT | after:SE5 |
| WT66 | A G | E AURORA | after:AS2 |
| WT67 | R I | E MIDNIGHT + (CAMP or INN) | after:B6 |
| WT68 | X K | E MIDNIGHT + (CAMP or INN) | after:C3 |
| WT69 | G P | E LATENIGHT + (CAMP or INN) | — |
| WT70 | C S | E SUNRISE + CAMP | SER_VAMP; after:SE6 |
| WT71 | K P | E MORNING after CAMP or INN | K_TOG+ |
| WT72 | V L | E AFTERNOON | after:C1 |
| WT73 | G K | E CAMP+NIGHT | SEASON:winter any; after:A1 |
| WT74 | X C K | E CAMP + COLDNIGHT | after:C3; after:R1; R18 |
| WT75 | V A K | E RAINSTART | ASHE_REVEAL; after:AS3; after:AS1; after:A2 |
| WT76 | K P | E SNOW | K_TOG+ |
| WT77 | G V | E CAMP + RAIN | after:A3 |
| WT78 | L K P | E RAIN + WILD | Luc-Kai intro |
| WT79 | R X I | E WILD + (RAIN or SNOW or STORM) | Remi-Xel intro; after:B6; after:X6 |
| WT80 | G K P | E SNOW | ANNIV; after:A1 |

## Notes for the build
- WT56 is the pay-off to WT23 (the sweet roll Redcap planted); never play it without WT23.
- WT50 is the pay-off to WT8 (Xelzaz and Ashe's anti-snow pact); WT59 calls back WT57.
- WT64 and WT65 do not need a real meteor on screen: the lines say it has already gone, and Luna missing it is the joke.
- WT46 is Serana teasing Kaidan's crush; it is not a Serana romance line and needs no Serana romance gate.
- WT59 is the only rival talk here (Val and Kaidan); Luna stays branch-neutral and oblivious.
- Speaker counts: Kaidan 26, Luna 26, Gore 16, Redcap 14, Lucien 14, Val 13, Remi 13, Xelzaz 13, Inigo 13, Serana 13, Ashe 13.
