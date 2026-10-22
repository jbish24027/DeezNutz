# 31b CIVIL WAR 2 - trigger rows (prefix CW, CW71-CW150, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\31b CIVIL WAR 2.txt`.
Part one and its gate codes: `triggers\31 CIVIL WAR.md` (sections 1-2 apply here unchanged). Sources: `research\triggers\vanilla_gates.md` (B1, B3), `research\content\00_inventory.md` (CW quest FormIDs), the bibles. Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana / Ashe Free rows are in `triggers\20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but player must not be in dialogue).

## 1. Silence

Same as part one (31 CIVIL WAR.md section 1): CWSiege / CWSiegeObj running, CWFortSiegeFort running, CWFinale running (whole window), CW01A/CW01B 160..199, CW03 at 20/100/225. Add: `CWFortSiegeCapital (087C21)` running (treat like a fort battle) **[UNC whether it runs separately from CWFortSiegeFort]**.

## 2. Gate codes

Reused from part one: `CW_IMP`, `CW_SONS`, `CW_ANY`, `CW_NONE`, `CW_ON`, `CW_WR`, `CW_END`, `CW_END_IMP`, `CW_END_SONS`, `MILCAMP`, `LOC:CastleDour`, `LOC:PalaceKings`, `CITY:<name>`, `AFTERFIGHT:cwfort`, `AFTERFIGHT:cwpatrol`, `AFTERFIGHT:cwfinale`. From TRIGGERS.md: `ALDUIN`, `HELGEN`, `K_CRUSH`, `K_TOG+`, `K_LOVE+`, `K_ANY`, `G_FLIRT`, `G_TOG+`, `INN`, `SNOW`, `NIGHT`, `RIVERWOOD`. From other files: `ASHE_REVEAL`, `ASHE_HIRED`, `S following`, `HLIOGoreReading >= 1` (32b TG82).

New (all Skyrim.esm):
- `Q:CWMission03` = event: `CWMission03` A False Front (03BCC4) just completed (first time). `CW_FALSEFRONT` = it has completed once. **[UNC: radiant per hold; it can repeat - fire once only]**
- `Q:CWMission04` = event: `CWMission04` Rescue from <fort> (035A23) just completed. Legion version = Fort Kastav, Stormcloak version = Fort Neugrad **[UNC: fort names from memory; if the alias fort differs, the CW80/CW88 lines name the wrong fort - check the AttackPoint alias at build, or gate on that location]**.
- `Q:CWMission07` = event: `CWMission07` Compelling Tribute (0504F0) just completed.
- `AFTERFIGHT:cwcourier` = combat ends while CWMission03 is running and its courier alias is dead **[UNC: courier alias name]**.
- `AFTERFIGHT:cwrescue` = combat ends while CWMission04 is running, at the prisoners' fort, before the quest completes **[UNC]**.
- `CW_FORT1` = CWFortSiegeFort has completed at least once (controller counter of AFTERFIGHT:cwfort events). `CW_FORT3` = three or more. **[UNC: no vanilla counter; keep a controller int]**
- `CW_RANK_SONS1` = player has the Unblooded rank = `CW_SONS` (it is the join rank). No further rank checks are used; CW86/CW87 only name ranks as a ladder.
- `CW_WINSPEECH` = CW_END_SONS, first tick after CWFinale stops (Ulfric's Solitude speech has played) **[UNC: speech is inside CWFinale; the first tick after it stops is the safe moment]**.
- `IMP_ARMOR` = player wears a Legion cuirass (as part one, optional) **[UNC form list]**.
- `LOC:WarTable` = within 600 units of the war map table in a CW camp tent, Castle Dour war room or the Palace of the Kings war room **[UNC: table base/refs]**.
- `NEAR:WindhelmDocks` not used. `LOC:Windhelm` = CITY:Windhelm, any visit.
- `LOC:Belethor` = in Belethor's General Goods (WhiterunBelethorsGeneralGoodsLocation) **[UNC FormID]**.
- `KIDS_PLAY` = in Whiterun or Riverwood within 1000 units of two or more child NPCs, exterior **[UNC; fallback = E CITY:Whiterun or RIVERWOOD, exterior, daytime]**.
- `CW_IDLE10` = CW_ANY, not CW_END, and 10+ in-game days since the last CW quest stage change **[UNC: controller stamps GameDaysPassed on each CW stage event]**.
- `SER_VAMP` = Serana is still a vampire (not cured via DLC1VQ08 cure branch) **[UNC; same note as 32b TG125]**.
- `DRAGONS_LEFT` = not ALDUIN.

## 3. Per-talk table

### Part 1 - The Legion
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW71 | V P | T | CW_IMP |
| CW72 | R K | T (or E LOC:CastleDour) | CW_IMP; after B1 |
| CW73 | C I | T | CW_IMP; after R13 |
| CW74 | S L | T | CW_IMP; S following |
| CW75 | L G P | T (exterior, not CITY, player moving) | CW_IMP; after L1; after CW11 if played |
| CW76 | K V P | T | CW_IMP; K_CRUSH; IMP_ARMOR [UNC, optional]; after A2; after CW9 |
| CW77 | A L | E leaving LOC:CastleDour | CW_IMP; ASHE_REVEAL; CW02A stage 10 done (Tullius has briefed you) |
| CW78 | C X | E MILCAMP or LOC:CastleDour | CW_IMP; after R18 |
| CW79 | R L | T | CW_WR; CW_IMP; not CW_END; after B10 |
| CW80 | K I | E Q:CWMission04 | CW_IMP; KaiandInigo stage >= 10 |
| CW81 | K G | T | CW_IMP; CW_FORT1; after A1 |
| CW82 | G I | T | CW_END_IMP; after C2 |
| CW83 | K P | T | CW_END_IMP |
| CW84 | I P | T | CW_END_IMP; after CW12 |
| CW85 | L K P | T | CW_END_IMP; Lucien-Kaidan intro done (Lucien's own scenes); after CW13 |

### Part 2 - The Stormcloaks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW86 | G P | T | CW_SONS |
| CW87 | C K | T | CW_SONS; after R1; after CW86 |
| CW88 | X G | E Q:CWMission04 | CW_SONS; after X1 |
| CW89 | G V | E MILCAMP | CW_SONS; after A3 |
| CW90 | R A | E LOC:PalaceKings | CW_SONS; ASHE_REVEAL |
| CW91 | X K | E LOC:WarTable in the Palace of the Kings | CW_SONS; after C3 |
| CW92 | S K | E LOC:Windhelm | CW_SONS; S following |
| CW93 | V L | T | CW_END_SONS; after C1; after CW27 |
| CW94 | K P | T | CW_END_SONS |
| CW95 | C L | E CW_WINSPEECH | CW_END_SONS; after R11 |
| CW96 | I R | E CITY:Whiterun | CW_END_SONS; after B6; after CW25 if played |
| CW97 | V A | T | CW_END_SONS; ASHE_HIRED |
| CW98 | X P | E LOC:Windhelm | CW_END_SONS |
| CW99 | S P | T | CW_END_SONS; S following |
| CW100 | G C | T | CW_END_SONS; after R5 |

### Part 3 - Either side
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW101 | S P | T | CW_NONE; S following |
| CW102 | G V P | T | CW_NONE; ALDUIN; after A3; after CW29 |
| CW103 | R V | E Q:CWMission03 | CW_ANY; Remi-Val own intro done (HLIOValBanter stage 10) |
| CW104 | X P | E Q:CWMission07 | CW_ANY; Kaidan following (the line mentions him) |
| CW105 | K P | T (first tick after the first AFTERFIGHT:cwfort) | CW_ANY; CW_FORT1 |
| CW106 | X I | T | CW_ANY; CW_FORT1; after X6 |
| CW107 | G S | T | CW_ANY; CW_FORT1; S following |
| CW108 | L A | T | CW_ANY; CW_FORT1; ASHE_REVEAL |
| CW109 | R C | T | CW_ANY; CW_FORT1; Remi-Redcap own intro done (Remi's mod) |
| CW110 | K V | E AFTERFIGHT:cwfort | CW_ANY; after A2; not the first fort (CW105 plays first) |
| CW111 | L P | T | CW_ANY; CW_FORT1 |
| CW112 | G K | E AFTERFIGHT:cwfort | CW_ANY; K_ANY; G_FLIRT or G_TOG+; after A1 |
| CW113 | I P | T | CW_ANY; CW_FORT3 |
| CW114 | G L | E MILCAMP | CW_ANY; HLIOGoreReading >= 1 [UNC]; after L1 |
| CW115 | V I | E MILCAMP + NIGHT | CW_ANY; after I1 |
| CW116 | K L | E MILCAMP | CW_ANY; Lucien-Kaidan intro done |
| CW117 | C V | E MILCAMP | CW_ANY; after R8 |
| CW118 | A I | E MILCAMP | CW_ANY; ASHE_REVEAL |
| CW119 | S X | E MILCAMP | CW_ANY; S following; SER_VAMP [UNC] |
| CW120 | K P | E LOC:WarTable | CW_ANY |
| CW121 | A X | T (exterior) | CW_ON; HELGEN; SNOW; ASHE_REVEAL |
| CW122 | I L | E KIDS_PLAY [UNC] | CW_ON; HELGEN; JRLucienInigo intro stage >= 30 |
| CW123 | G P | T | CW_ANY |
| CW124 | I R | E LOC:Belethor | CW_ON; HELGEN; after B6 |
| CW125 | R S | T | CW_ON; HELGEN; S following |
| CW126 | I G | T | CW_ON; HELGEN; after C2 |
| CW127 | A K | T | CW_ON; HELGEN; ASHE_REVEAL |
| CW128 | C A | T | CW_ANY; ASHE_HIRED |
| CW129 | V P | T | CW_IDLE10 [UNC] |
| CW130 | A P | T (NIGHT, CAMP or INN preferred) | CW_ANY; ASHE_REVEAL |

### Part 4 - After the war
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW131 | R P | T | CW_END |
| CW132 | X V | E AFTERFIGHT:bandit | CW_END; after X4 |
| CW133 | L P | E INN (bard playing, if checkable) | CW_END |
| CW134 | K P | T | CW_END; K_TOG+ |
| CW135 | V G | T | CW_END; DRAGONS_LEFT (not ALDUIN); after A3 |
| CW136 | S I | T | CW_END; S following |
| CW137 | K P | T | CW_END; K_LOVE+; after CW134 |
| CW138 | G K | E INN | CW_END; CW_FORT1; after A1 |
| CW139 | C I | T (exterior, on a road) | CW_END; after R13 |
| CW140 | L V | T | CW_END; after C1 |

### Part 5 - After the fight (barks; the normal 8 s post-combat delay, never during the battle)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW141 | G V | E AFTERFIGHT:cwfort | after A3 |
| CW142 | K P | E AFTERFIGHT:cwfort | player Health < 75% at combat end [UNC] |
| CW143 | A L | E AFTERFIGHT:cwfort | ASHE_REVEAL; Ashe Health < 90% at combat end [UNC] |
| CW144 | C R | E AFTERFIGHT:cwfort | — |
| CW145 | X I | E AFTERFIGHT:cwfort | after X6 |
| CW146 | S G | E AFTERFIGHT:cwfort | S following; SER_VAMP [UNC] |
| CW147 | V R | E AFTERFIGHT:cwcourier [UNC] | Remi-Val own intro done |
| CW148 | G P | E AFTERFIGHT:cwrescue [UNC] | — |
| CW149 | L K | E AFTERFIGHT:cwpatrol | CW_ON; Lucien-Kaidan intro done |
| CW150 | R A | E AFTERFIGHT:cwpatrol | CW_ON; CW_ANY |

## 4. Notes for the build

- **Side safety:** Part 1 rows all carry CW_IMP, Part 2 rows CW_SONS. The endings (CW82/83/84/85, CW93/94/95/96-100) never say who struck the last blow, so they fit the player killing Ulfric/Tullius or letting the general do it.
- **Fort names:** CW80 names Fort Kastav (Legion rescue), CW88 Fort Neugrad (Stormcloak rescue). If the mission's AttackPoint alias in this load order is a different fort, drop the name or gate on the location. **[UNC]**
- **Galmar** dies in the Battle for Windhelm on the Legion side (CW82); on the Stormcloak side he is alive after Solitude (CW100). **Rikke** is already covered in part one (CW27).
- **Ranks:** Legion ranks named: Auxiliary (CW71), Legate (CW85). Stormcloak ranks named: Unblooded, Ice-Veins (CW86), Bone-Breaker (CW87), Stormblade (CW100). No line claims which quest gave which promotion.
- **Kaidan:** CW76 is his crush beat (Luna thinks he's checking her buckles); never at K_TOG or later. CW134 is K_TOG+, CW137 K_LOVE+ (general "quiet autumn", no home or wedding content). No Ulfric jealousy (his own mod has it). CW80 mentions his Thalmor cell only. No cult, no beard.
- **Rivalry:** CW112 is the only rivalry talk (Gore vs Kaidan, both romancing). Luna has no line in it.
- **Gore:** CW114 needs his reading lessons started; CW107/CW123 mention the Ravens only (no Jo-Lee). CW89 "milk drinker" is his own word.
- **Val:** CW89/CW97/CW132 Navy references fit his bible (one year, deckhand then bosun). CW117 keeps his dislike of rieklings. CW140 "relic hunter, not a pirate".
- **Ashe:** every Ashe talk except CW97/CW128 carries ASHE_REVEAL (sensors, coolant, logging). CW127 mentions the Thalmor approaching her father (bible: they paid him for armour cloth, he walked away) - keep if the build is happy with father content after the reveal.
- **Serana:** CW119 and CW146 need her still a vampire.
- **Same-event priority:** first AFTERFIGHT:cwfort fires part one's CW65/66/67 or CW141-146 (bark pool, one per fight); CW105 then plays as the first T after CW_FORT1. Q:CWMission04 fires CW80 (Legion) or CW88 (Stormcloak); AFTERFIGHT:cwrescue fires CW148 before them. CW147 fires on the courier kill; CW103 on completion.
- **Existing coverage avoided:** part one's boots, pay, flags in the war room, pamphlets, betting pool, Kyne, Concordat itemised, crown history, both bard songs, the soldiers' stew, Rikke's death, High King/High Queen jokes, Grey Quarter nod. 41/41b (Tullius "frozen rock", Lucien's mother at Tullius, Rikke, Ulfric insults, Galmar's bear and "proper Nord arm", the new Jarls, Elisif's horn, Ulfric as a "git with a crown"). 56 road encounters (patrols, couriers, prisoners). 30 Season Unending. No "Dragonborn".
