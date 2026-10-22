# 12b BRUMA AND MOONPATH 2 - trigger rows (BR151-BR230)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\12b BRUMA AND MOONPATH 2.txt`
Research: `research\content\bruma_moonpath_wyrmstooth_etc.md` sections 1 and 2. Part 1 rows and every local gate code (CYR, COUNTY, CITY:Bruma, ELS, RIVERHOLD_S, OASIS, DESERT, TENMAR, PP_*, K_AKAVIRI, GORE_TIES, AA, DS, AC, SR, ALV, UMH, SIC, UL, UU, WM, COUR, WH, FF, AWP, DEEP, WATER, MPC, STE, INC, RTP, DG, DSTY) are defined in `triggers\12 BRUMA AND MOONPATH.md` and reused unchanged. Global codes: TRIGGERS.md section 4. Serana/Ashe Free() rows and codes: `triggers\20 DAWNGUARD.md` sections 1 and 3, `triggers\48 SERANA.md`, `triggers\49 ASHE.md`.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, +Lu = Luna (player line, no Free check).
Type: T = timer, E = event. `[unconfirmed]` = stage, cell or FormID not proven from the records; check at build or in game.

## Standing rules for this file
- Every **S** row also needs `SERANA` (DLC1VQ02 5 done) and Serana's Free() row; every **A** row also needs `ASHE_HIRED` (`MM_AsheIntro 0A7946:Ashe - Fire and Blood.esp` completed), her Free() row, her `bConfigVarIdles` toggle and her silence list (49 ASHE.md). Pair "first meeting" talks from 48 SERANA / 49 ASHE must have played (written below as "S-x met" / "A-x met").
- `K_AKAVIRI` is now confirmed in 14b as `GetStageDone KINV(0B3032:0Kaidan.esp) 50`.
- Branch talks: each ending gets its own row; never let both rows of a pair fire.
- Follow-up rows (`after:BRnn`) need the part-1 talk to have played.

## New gate codes for this file
**Bruma quest endings** (all `BSHeartland.esm`, from the research table)
- `UMH_TRUTH` = `0C7E4C` stage 100 done. `UMH_HID` = `0C7E4C` stage 110 done.
- `ALV_RETURN` = `003A58` stage 30 done. `ALV_REPORT` = `003A58` stage 50 done.
- `SIC_LEGATE` = post handler `0CE135` stage 100 done (sided with the Legate). `SIC_FREED` = `0CE135` stage 150 or 200 done (rescued the prisoner).
- `COUR_OLAF` = `0C9BE1` stage 360 done. `COUR_REFUSED` = `0C9BE1` stage 399 or 400 done.
- `UL_DONE` = `08AE84` completed (any ending) `[unconfirmed: completion stage; use GetQuestCompleted]`.
- `TOAK` = Two of a Kind `0E5911` stage 80 done (Ervig rescued).
- `DEEP_DONE` = `0E5912` stage 200 done.
- `WATER_DONE` = Water Run Dry `CYRGreenwoodMeaderyFF01` completed `[unconfirmed FormID]`.
- `FF_GUARDIAN` = `06C0DE` stage 100 done (Glade Guardian dead).
- `FROSTFIRE` = player in the Frostfire Glade worldspace `[unconfirmed WRLD FormID]` and `06C0DE` stage 150..199 not running (the banishing silence).
- `ALESWELL` = arrival at Aleswell `[unconfirmed LCTN]`. `CLOUDRULER` = in Cloud Ruler Temple `[unconfirmed LCTN]`. `GREENWOOD` = at Greenwood Meadery `[unconfirmed LCTN]`. `SYNOD_HALL` = Synod conclave cell in Bruma `[unconfirmed]`. `FG_HALL` = Fighters Guild hall, Bruma `[unconfirmed]`. `CATHEDRAL` = Cathedral of St. Martin interior `[unconfirmed]`. `AYLEID_CB` = any Ayleid ruin interior in County Bruma `[unconfirmed list]`. `FORT_CUTPURSE` = Fort Cutpurse `[unconfirmed]`. `MOUNTAINWATCH` = Mountain Watch `[unconfirmed]`.
- `ARMION_HERE` = proxy as BR31: in CITY:Bruma and SR 50 not done `[unconfirmed proxy]`.

**Moonpath places and moments** (all `moonpath.esp`)
- `ESTUARY` = GetInCell `01DAD1` (Elsweyr Estuary). `TOPAL` = GetInCell `03A854` or `03E4CB` (Topal Sea Island). `PILLARFALLS` = GetInCell `023EFB`. `TENMAR_HIDE` = GetInCell `000D62` (Tenmar Forest Hideout) or `01D079` after INC 40 `[unconfirmed which cell holds the drums/cooks]`.
- `PAHMAR_OK` = `06A8CA` stage 55 done and `01EE82` stage 20 done (the Pahmar have accepted you).
- `MERVAR_OK` = `01ED3C` past the stage where Qa'mel vouches for you `[unconfirmed stage; fallback INC 40 done]`.
- `ELS_SUN` = in ELS, daytime (hour 8..18), cell has a sky, not raining `[unconfirmed: interior-sky cells may not report weather; use hour only if needed]`.
- `ELS_LEAVE` = event: player leaves ELS for a non-ELS location with INC 150 done, first time only.
- `FONDUE` = player or Ashe eats Elsweyr Fondue in ELS (OnItemRemoved/eat event on the fondue ALCH `[unconfirmed]`), or E INN/CAMP in ELS as fallback.
- `DUNE_DAY` = DESERT and at least 4 game hours spent there `[unconfirmed proxy for "a day in the desert"]`.

**Serana / Ashe** (from 20 DAWNGUARD.md, 49 ASHE.md)
- `SER_VAMP`, `SER_CURED`, `ASHE_REVEAL`, `ASHE_Q1` as defined there.

## Silence zones
Unchanged from `triggers\12 BRUMA AND MOONPATH.md` (border gate, mass, wedding, castle audience/arrest, Ugly Love killing, Whispers teleport, Frostfire banishing, Fort Pale Pass assault, carriage legs, airship flights/boarding, Sload scenes), plus Serana's and Ashe's own silence lists.

## Table

### Part 1 - Loose ends in County Bruma
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR151 | K R | T | UMH_TRUTH; after B1 |
| BR152 | X V | T | UMH_HID; after X4 |
| BR153 | V R | T | ALV_RETURN; Inigo following (named in the talk) |
| BR154 | X +Lu | T | ALV_REPORT |
| BR155 | G X | T | SIC_LEGATE; after X1 |
| BR156 | L K +Lu | T | SIC_FREED; Kaidan-Lucien intro done |
| BR157 | G +Lu | T | COUR_OLAF; after BR78 |
| BR158 | V R | T | COUR_REFUSED |
| BR159 | I G | T | UL_DONE; after C2 |
| BR160 | L I +Lu | T | TOAK; Lucien-Inigo intro done |
| BR161 | G K | T | WATER_DONE; after BR76 |
| BR162 | L C +Lu | E ALESWELL first arrival | after R11 |
| BR163 | G K +Lu | T | CYR; GORE_TIES; after A1 |
| BR164 | G L +Lu | T | CYR; after L1 |
| BR165 | L K | T | CYR; Kaidan-Lucien intro done |
| BR166 | L X +Lu | T | CYR; UU 60 or 65/80 done (either ending); Xelzaz-Lucien intro done |
| BR167 | V I | E FORT_CUTPURSE after AC 100 set, else T | AC 100 done; after I1 |
| BR168 | R C | T | DEEP_DONE; after BR75; after R15-chain not required (Remi-Redcap intro in Remi's mod done) |

### Part 2 - Serana and Ashe in Cyrodiil
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR169 | S V | E INN in CITY:Bruma | SERANA; S-V met; after BR18 (no-coffee callback) |
| BR170 | S +Lu | E CATHEDRAL | SERANA; SER_VAMP; not MASS running |
| BR171 | S L | E exterior just outside Bruma walls, else T CITY:Bruma | SERANA; S-L met; after BR84 |
| BR172 | S K | E CLOUDRULER | SERANA; S-K met; K_AKAVIRI |
| BR173 | S G | E GREENWOOD | SERANA; S-G met |
| BR174 | S X | T | SERANA; SER_VAMP (Xelzaz calls her a vampire); S-X met; ARMION_HERE |
| BR175 | A S | T | SR 20 done; SERANA; ASHE_HIRED; S-A met (their own patch intro) |
| BR176 | A +Lu | E SYNOD_HALL, else T CITY:Bruma | ASHE_Q1 |
| BR177 | A K | E FG_HALL | ASHE_HIRED; A-K met; after BR29 |
| BR178 | A X | E FROSTFIRE | ASHE_HIRED; A-X met |
| BR179 | A L | E AYLEID_CB | ASHE_REVEAL; A-L met |
| BR180 | R A | T | WM 60 done, 250 not done; ASHE_REVEAL; A-R met |

### Part 3 - Bruma fight barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR181 | A K | E AFTERFIGHT:ogre in MOUNTAINWATCH | DEEP 90 done; ASHE_HIRED; A-K met |
| BR182 | L S | E AFTERFIGHT, FF_GUARDIAN just set | SERANA; S-L met |

### Part 4 - Khajiit ways
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR183 | L I | T | ELS; STE 0 done (Yura met); Lucien-Inigo intro done |
| BR184 | G R +Lu | T | ELS; after B15-chain not required (Gore-Remi intro in Remi's mod done) |
| BR185 | C I | E TENMAR_HIDE | PAHMAR_OK; after R13 |
| BR186 | +Lu I X | E CLEARNIGHT in ELS | after X6 |
| BR187 | G I | E TENMAR_HIDE | PAHMAR_OK; after C2 |
| BR188 | I +Lu | T | DG 95 done |
| BR189 | G V | E ESTUARY | after A3 |
| BR190 | R X +Lu | T | TENMAR; Remi and Xelzaz not fallen out |
| BR191 | C G | E DESERT | after R5 |
| BR192 | X C | E DESERT + NIGHT | after BR114; after R18 |
| BR193 | V I | T | ELS; after I1 |
| BR194 | L I | E TENMAR_HIDE + NIGHT | Lucien-Inigo intro done |
| BR195 | R G | E TENMAR_HIDE | PAHMAR_OK |

### Part 5 - Inigo and Kaidan's Elsweyr, part two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR196 | K I | E DESERT | KaiandInigo stage >= 10 (they have met) |
| BR197 | K +Lu | E ELS_SUN | BRYNJAR |
| BR198 | I K +Lu | E DESERT or ELS exterior | KaiandInigo >= 10 |
| BR199 | +Lu K I | E TENMAR_HIDE | KaiandInigo >= 10; after BR108 (the goat) |
| BR200 | K I | E TENMAR_HIDE | KaiandInigo >= 10; INC 40 done (some days spent at the hideout) |
| BR201 | I K | T | after BR103; at least 3 game days in ELS since first arrival `[unconfirmed counter]` |
| BR202 | +Lu I C | T | TENMAR; after R13 |
| BR203 | K +Lu | E TENMAR + NIGHT | K_TOG+ |
| BR204 | I K +Lu | E ELS_LEAVE | INC 150 done; KaiandInigo >= 10 |

### Part 6 - Serana and Ashe in Elsweyr
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR205 | S I | E ELS_SUN | SERANA; SER_VAMP; S-I met |
| BR206 | S +Lu | E ELS_SUN | SERANA; SER_CURED |
| BR207 | S V | E TOPAL + NIGHT | SERANA; SER_VAMP; S-V met |
| BR208 | S K | E TENMAR_HIDE | SERANA; S-K met; PAHMAR_OK |
| BR209 | S X | T | DG 30 done, DG 95/100 not done; SERANA; S-X met |
| BR210 | A X | E ELS_SUN | ASHE_REVEAL; A-X met |
| BR211 | R A +Lu | E FONDUE | ASHE_REVEAL; A-R met |
| BR212 | A K | T | INC 100 done; ASHE_Q1 `[unconfirmed which Ashe quest reveals the Thalmor cloth offer; ASHE_LOGS is the safe fallback]`; A-K met |
| BR213 | A G | E DUNE_DAY | ASHE_REVEAL; A-G met |
| BR214 | A +Lu | T | INC 40 done; ASHE_HIRED |
| BR215 | I A | E TENMAR_HIDE | ASHE_REVEAL; A-I met; STE 10 done (Ameir and the moon sugar) |
| BR216 | C S | E ELS_SUN | SERANA; SER_VAMP; S-C met; after BR115 |
| BR217 | S K +Lu | E CLEARNIGHT in ELS | SERANA; S-K met; K_CRUSH |

### Part 7 - The rebellion goes on
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR218 | L G | E TENMAR_HIDE | INC 150 done; GORE_FATHER; after L1 |
| BR219 | +Lu L | T | RTP 60 done |
| BR220 | V +Lu | T | INC 150 done; after BR130 |
| BR221 | X K | T | INC 150 done; after C3 |
| BR222 | C G | E TENMAR_HIDE | after BR118; after R5 |
| BR223 | L R | T | DG 95 done; after B10 |
| BR224 | X G +Lu | E PILLARFALLS | INC 70 done; after X1 |
| BR225 | V C | E TENMAR_HIDE | MERVAR_OK; after BR120; after R8 |
| BR226 | C L | T | ELS; after BR126 by >= 2 game days `[unconfirmed counter]`; after R11 |
| BR227 | G V | T | DSTY 30 done; after A3 |

### Part 8 - Elsweyr fight barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR228 | R A | E AFTERFIGHT:dwarven automaton in TOPAL `[unconfirmed: automatons at the supply post]` | RTP 10 done; ASHE_REVEAL; A-R met |
| BR229 | S K | E AFTERFIGHT:Thalmor in DESERT | SERANA; S-K met |
| BR230 | G I | E AFTERFIGHT:bandit on the caravan road (`06A8CA` 20..30 or the canyon cells) | after C2 |

## Open items for build
- All `[unconfirmed]` items above, especially the County Bruma place LCTNs (shared with part 1), the Frostfire Glade worldspace, Tenmar hideout cell split, and the two day-counters (BR201, BR226).
- BR170/BR174/BR205/BR207/BR216 are vampire-Serana rows; BR206 is the cured row. Never let BR205 and BR206 both play in one visit (they share the ELS_SUN trigger).
- BR203 is Kaidan-romance gated; BR217 is crush-only and must stop once K_TOG+ is reached.
- BR212: if testing shows the Thalmor cloth story is only told in a later Ashe quest, move the gate to ASHE_LOGS.
