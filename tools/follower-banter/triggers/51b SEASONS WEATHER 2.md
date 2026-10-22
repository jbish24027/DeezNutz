# 51b SEASONS WEATHER 2 - trigger rows (prefix WT, WT81-WT180, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\51b SEASONS WEATHER 2.txt`.
Part 1 (read in full first): `51 SEASONS WEATHER TIME MORE.txt` / `triggers\51 SEASONS WEATHER TIME MORE.md`. Every code defined there is reused here unchanged (calendar `date mM dD`, `SEASON:<name> start|any`, `THUNDER`, `BLIZZARD`, `FOG`, `RAINSTART`, `AFTERRAIN`, `HEAT`, `FROST1`, `COLDNIGHT`, `SUNSET`, `SUNRISE`, `DUSK`, `MIDNIGHT`, `LATENIGHT`, `AFTERNOON`, `CLEARDAY`, `ANNIV`, pair intros).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana and Ashe use the Free() rows in `20 DAWNGUARD.md` section 1. Every row with S also needs `SERANA`; every row with A also needs `ASHE_HIRED`. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (the 60 s weather/time poll in TRIGGERS.md section 1 drives every weather, hour, region and date check here).

## Gate codes used in this file

Reused, same meaning as before: `K_CRUSH`, `K_TOG+`, `SERANA`, `SER_VAMP`, `SER_CURED`, `DG_GARDEN`, `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `MG_JOIN`, `VAL_FATHIS`, `CITY`, `CAMP`, `INN`, `WILD`, `WATER`, `NIGHT`, `MORNING`, `PREDAWN`, `CLEARNIGHT`, `AURORA`, `RAIN`, `SNOW`, `WIND`, `after:<ID>`, and the pair intros `KaiandInigo>=10`, `Luc-Kai intro`, `Remi-Gore intro`, `Remi-Xel intro`, `Xel-Luc intro`.

New in this file:
- `MONTH:mN` = `GameMonth == N` (0 = Morning Star .. 11 = Evening Star). `MONTH:mN d>=X` adds `GameDay >= X`. Every talk plays once, so a month talk fires once, in the first year that month comes round with its other gates true.
- `YEAR2:<ID>` = `ANNIV` (part 1) AND talk `<ID>` has played AND `GameDaysPassed >= (day <ID> played) + 300`. Makes every second-year callback land on the NEXT turn of the calendar after the talk it remembers, never the same festival or season. Needs the controller's per-talk play-day stamp (already required by `after:X+Nh` in 45 PARTY LIFE.md).
- `REGION:<Hold>` = exterior and `GetInCurrentLoc <Hold>HoldLocation` (Reach, Pale, Whiterun, Rift, Eastmarch, Falkreath, Haafingar). **[UNC: hold-location FormIDs; the vanilla `*HoldLocation` records are the parents of every town/dungeon location in the hold]**
- `NEAR:Markarth` = exterior, `REGION:Reach`, and `GetInCurrentLoc MarkarthLocation` or within 4000 units of the Markarth gate marker. **[UNC]**
- `HONRICH` = `REGION:Rift` and within 3000 units of Lake Honrich's shore (a placed XMarker in our plugin, or the Riften docks area). **[UNC]**
- `HOTSPRINGS` = `REGION:Eastmarch`, exterior, in the hot-springs basin south of Windhelm (a new FormList of those exterior cells, or distance to an XMarker at the springs). **[UNC]**
- `HAAF_COAST` = `REGION:Haafingar`, exterior, `FOG`, and below 1000 units of sea level / within the Solitude coast cells. **[UNC]**
- `FARM` = player within 3000 units of a location with `LocTypeFarm` (vanilla keyword), exterior. **[UNC: farm detection by nearest location keyword]**
- `NOON` = hour 11..13. `EVENING` = hour 17..20. `LATEEVE` = hour 20..22.5 (used only in Sun's Height, when it is still light).
- `OVERCAST` = exterior, `IsRaining == 0`, `IsPleasant == 0` (cloudy weather classification). **[UNC: classification flags of the weather mod]**
- `GORE_READS` = `Remi-Gore intro` AND Remi's reading-lesson global `HLIOGoreReading` (6F46A0:HLIORemi.esp) >= 1. **[UNC: which value means the lessons have started; fallback: HLIOGoreBanter Scene4 done]**
- `Remi-Val intro` = HLIOValBanter (9BA4FD:HLIORemi.esp) stage 10 done (their own intro scene).
- `NOT_FALLOUT` = Remi+Xelzaz not in the falling-out window (BPUFXelzazRemielFallingOut 11 done and 13 not) - already in TRIGGERS.md section 3, repeated here for the three R+X rows.

Holiday dates (same table as part 1, plus First Planting from TRIGGERS.md): New Life `m0 d1`; South Wind's Prayer `m0 d15`; Heart's Day `m1 d16`; First Planting `m2 d7`; Jester's Day `m3 d28`; Second Planting `m4 d7`; Mid Year `m5 d16`; Merchant's Festival `m6 d10`; Sun's Rest `m6 d20`; Harvest's End `m7 d27`; Tales and Tallow `m8 d3`; Witches Festival `m9 d13`; Warriors Festival `m10 d20`; North Wind's Prayer `m11 d15`; Saturalia `m11 d25`; Old Life `m11 d30`. All 16 Holidays-mod festivals get at least two talks here.

## Per-talk table

### Part 1 - festivals
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WT81 | K A | T | date m0 d1; ASHE_REVEAL; after:AS1 |
| WT82 | G V | T | date m0 d1; YEAR2:WT17; after:A3 |
| WT83 | I A P | T | date m0 d1; YEAR2:WT18; after:AS6 |
| WT84 | V G | T | date m0 d15; after:A3 |
| WT85 | R P | T | date m0 d15; YEAR2:WT16 |
| WT86 | V A | T | date m1 d16; ASHE_REVEAL; after:AS3 |
| WT87 | L I | T | date m1 d16; YEAR2:WT19 |
| WT88 | R X P | T | date m2 d7; Remi-Xel intro; NOT_FALLOUT |
| WT89 | S X | T | date m2 d7; DG_GARDEN; after:SE4 |
| WT90 | G P | T | date m3 d28; MG_JOIN; GORE_READS |
| WT91 | A K | T | date m3 d28; YEAR2:WT22; ASHE_REVEAL |
| WT92 | C R | E exterior | date m4 d7; YEAR2:WT56 |
| WT93 | I X | T | date m4 d7; after:X6 |
| WT94 | L X P | E NOON + CLEARDAY | date m5 d16; Xel-Luc intro |
| WT95 | S G | T | date m5 d16; after:SE2 |
| WT96 | V P | E CITY (any) | date m6 d10 |
| WT97 | G X | E CITY (any) | date m6 d10; GORE_READS; after:X1 |
| WT98 | X A | E WILD + CLEARDAY | date m6 d20; ASHE_REVEAL; after:AS7 |
| WT99 | G I R | E CLEARDAY | date m6 d20; YEAR2:WT27; Remi-Gore intro; after:C2 |
| WT100 | L G | E FARM | date m7 d27; after:L1 |
| WT101 | S X | E CAMP or INN | date m7 d27; YEAR2:WT28; SER_CURED |
| WT102 | X P | E NIGHT | date m8 d3 |
| WT103 | A G | E NIGHT | date m8 d3; ASHE_Q1; after:AS2 |
| WT104 | V C | T | date m9 d13; after:R8 |
| WT105 | K P | T | date m9 d13; YEAR2:WT31; K_TOG+ |
| WT106 | K L | E CITY (any) | date m10 d20; YEAR2:WT32 |
| WT107 | I V | E CITY (any) | date m10 d20; after:I1 |
| WT108 | X I | T | date m11 d15; after:WT15; after:X6 |
| WT109 | G P | T | date m11 d15; YEAR2:WT33; GORE_READS |
| WT110 | G A | T | date m11 d25; YEAR2:WT35; ASHE_REVEAL |
| WT111 | L C | T | date m11 d25; after:R11 |
| WT112 | R X | E NIGHT | date m11 d30; Remi-Xel intro; NOT_FALLOUT |
| WT113 | V P | E NIGHT | date m11 d30; VAL_FATHIS |

### Part 2 - the months
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WT114 | K G | T | MONTH:m0 d>=10; after:H1 |
| WT115 | L P | T | MONTH:m0 d>=4 |
| WT116 | C S | T | MONTH:m0; after:SE6 |
| WT117 | L P | E MORNING + CAMP | MONTH:m1 |
| WT118 | I G | E exterior | MONTH:m1; after:H14; after:C2 |
| WT119 | K P | E FARM | MONTH:m2; K_TOG+ |
| WT120 | G C | E WATER | MONTH:m2; after:R5 |
| WT121 | V A | E AFTERRAIN | MONTH:m3; after:AS3 |
| WT122 | R X | E exterior | MONTH:m3; Remi-Xel intro; NOT_FALLOUT |
| WT123 | C P | E exterior | MONTH:m3 |
| WT124 | C K | E exterior | MONTH:m4; after:R1 |
| WT125 | X P | E WILD | MONTH:m4 |
| WT126 | G V | E HEAT | MONTH:m5; after:A3 |
| WT127 | A R | E HEAT | MONTH:m5; ASHE_REVEAL; after:AS11 |
| WT128 | C K | E exterior + LATEEVE | MONTH:m6; after:R1 |
| WT129 | I P | E CAMP + LATEEVE | MONTH:m6 |
| WT130 | V R | E FARM | MONTH:m7; Remi-Val intro |
| WT131 | X K | E CAMP or INN | MONTH:m7; after:C3 |
| WT132 | K P | E CAMP + EVENING | MONTH:m8; K_CRUSH |
| WT133 | S I | E exterior + EVENING, within 3000 units of a CITY or FARM location | MONTH:m8; after:SE8 |
| WT134 | K A | E WILD | MONTH:m9; ASHE_REVEAL; after:AS1 |
| WT135 | I X | E MORNING + CAMP | MONTH:m9; after:X6 |
| WT136 | L P | E hour 15..17 | MONTH:m10 |
| WT137 | R I | E exterior, hour 16..19 | MONTH:m10; after:B6 |
| WT138 | X P | E (CAMP or INN), hour 15..17 | MONTH:m10 |
| WT139 | I K | E CAMP + NIGHT | MONTH:m11; KaiandInigo>=10 |
| WT140 | V G | E (CAMP or INN) + NIGHT | MONTH:m11; after:A3 |
| WT141 | A C | T | MONTH:m11 d>=22; after:AS5 |

### Part 3 - weather by the hold
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WT142 | K X | E RAIN | REGION:Reach; after:C3 |
| WT143 | R P | E RAIN | NEAR:Markarth |
| WT144 | V I | E BLIZZARD | REGION:Pale; after:I1 |
| WT145 | X K P | E BLIZZARD | REGION:Pale; after:C3 |
| WT146 | R K | E WIND + FARM | REGION:Whiterun; after:B1 |
| WT147 | V P | E WIND + WILD | REGION:Whiterun |
| WT148 | K R P | E FOG | REGION:Rift; after:B1 |
| WT149 | L C | E FOG | HONRICH; after:R11 |
| WT150 | X A | E SNOW | HOTSPRINGS; ASHE_REVEAL; after:AS7 |
| WT151 | G V P | E exterior | HOTSPRINGS; after:A3 |
| WT152 | L S | E RAIN | REGION:Falkreath; after:SE5 |
| WT153 | V K | E FOG | HAAF_COAST; after:A2 |

### Part 4 - the party's clock
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WT154 | G P | E MORNING after CAMP or INN | — |
| WT155 | R P | E MORNING + (CAMP or INN) | — |
| WT156 | X P | E MORNING + CAMP | — |
| WT157 | K P | E MORNING + CAMP | K_CRUSH |
| WT158 | K C | E PREDAWN + CAMP | after:R1 |
| WT159 | K L | E PREDAWN + CAMP | Luc-Kai intro |
| WT160 | V R | E SUNSET | Remi-Val intro |
| WT161 | C V | E SUNSET | after:WT160; after:R8 |
| WT162 | S G | E MIDNIGHT + CAMP | after:SE2 |
| WT163 | S P | E MIDNIGHT + CAMP | — |
| WT164 | S X | E MIDNIGHT + (CAMP or INN) | DG_GARDEN; after:SE4 |
| WT165 | C P | E CLEARNIGHT | — |
| WT166 | C L | E CLEARNIGHT | after:WT62; after:R11 |

### Part 5 - the second year
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WT167 | G R | T | SEASON:spring start; YEAR2:S1 |
| WT168 | K A | T | SEASON:spring start; YEAR2:WT1; after:PY357 |
| WT169 | V C | T | SEASON:spring start; YEAR2:WT3 |
| WT170 | G S | T | SEASON:summer start; YEAR2:WT6; SER_VAMP |
| WT171 | C K | E WILD | SEASON:autumn start; YEAR2:WT9 |
| WT172 | G R P | T | SEASON:autumn start; YEAR2:WT10 |
| WT173 | I X | T | SEASON:winter start; YEAR2:WT13 |
| WT174 | K P | T | SEASON:winter start; YEAR2:WT14; K_TOG+ |
| WT175 | R G P | E CLEARNIGHT | YEAR2:WT64 |
| WT176 | A G | E AURORA | YEAR2:WT66 |
| WT177 | G K | E CAMP + NIGHT | SEASON:winter any; YEAR2:WT73 |
| WT178 | V K | E OVERCAST | YEAR2:WT75 |
| WT179 | G K P | E SNOW | YEAR2:WT76; K_TOG+ |
| WT180 | C X | E SNOW (first snow of winter, as S6) | YEAR2:S6 |

## Notes for the build
- Callback pairs (never play the second without the first): WT82<-WT17, WT83<-WT18, WT85<-WT16, WT87<-WT19, WT91<-WT22, WT92<-WT56, WT99<-WT27, WT101<-WT28, WT105<-WT31, WT106<-WT32, WT108<-WT15, WT109<-WT33, WT110<-WT35, WT114<-H1, WT118<-H14, WT161<-WT160, WT166<-WT62, WT167<-S1, WT168<-WT1+PY357, WT169<-WT3, WT170<-WT6, WT171<-WT9, WT172<-WT10, WT173<-WT13, WT174<-WT14, WT175<-WT64, WT176<-WT66, WT177<-WT73, WT178<-WT75, WT179<-WT76, WT180<-S6.
- WT108 needs only `after:WT15` (Xelzaz's first prayer to Kyne in South Wind's Prayer of any earlier year); North Wind's Prayer always falls later in the same year, so no YEAR2 is needed.
- WT174 calls back a K_CRUSH talk (WT14) from the K_TOG+ side: Luna now knows, which is correct after K_TOG. WT132 and WT157 are K_CRUSH talks where Luna stays oblivious (airflow; ink in her hair).
- WT113 needs Val005 done (`VAL_FATHIS`): it names Fathis alive and the first kill Val faced in Apocrypha.
- WT89 and WT164 need `DG_GARDEN` (Chasing Echoes, Valerica's courtyard/lab) because Serana has her mother's seeds and notes.
- WT103 uses Ashe's "twenty years" (same open question as PL67/PL111 on whether `ASHE_Q1` is the right gate).
- WT119's line "when you find somewhere to stay" is deliberately not a promise from Luna; no romance commitment.
- No line says "Dragonborn", no Kaidan cult content, Brynjar is not named (WT142 mentions only his childhood year in the Reach).
- Speaker counts (talks): Kaidan 26, Gore 25, Xelzaz 22, Val 19, Remi 17, Redcap 17, Ashe 14, Inigo 14, Lucien 12, Serana 10, Luna 34 (34%).
- QA: `qa_check.py` 0 flags; `dup_scan.py` shows no repeated 6+ word line or title involving WT81-WT180.
