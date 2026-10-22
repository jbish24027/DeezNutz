# 35b COLLEGE 2 - trigger rows (MG71-MG130)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\35b COLLEGE 2.txt`
Research: `research\triggers\vanilla_gates.md` (B1, B2, B3). Part 1 rows, the College silence list and every local gate code (`MG_JOIN`, `MG_LESSON`, `MG_SAARTHAL`, `MG_BOOKS`, `MG_AUGUR`, `EYE_HERE`, `MG_SAVOS`, `MG_STAFF`, `STAFF_CARRIED`, `ARCH`, `ANCANO_ALIVE`, `MIRABELLE_ALIVE`, `SAVOS_ALIVE`, `MGR_*`, `VAL_COL`, `VAL_GRAD`, `GORE_READING`, `INIGO_BV`, `LOC:*`, `NEAR:<npc>`) are defined in `triggers\35 COLLEGE OF WINTERHOLD.md` and reused unchanged. Global codes: TRIGGERS.md section 4. Serana/Ashe Free() rows and codes (`SERANA`, `SER_VAMP`, `S_ROM_ON`, `ASHE_HIRED`, `ASHE_REVEAL`, `A_CRUSH`): `triggers\20 DAWNGUARD.md` sections 1 and 3, `triggers\49 ASHE.md`.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event. `E COMBAT` = in-fight bark path, same open item as `13 WYRMSTOOTH ...md` **[UNC]**. `[UNC]` = not verified, check at build.

## Standing rules for this file
- College silence from 35 COLLEGE OF WINTERHOLD.md section 1 applies to every row (MG05 20..49, MG08 10..199, Ancano / Quaranir scenes, MG06 in the Hall of the Elements).
- Every **S** row also needs `SERANA` and Serana's Free() row; every **A** row also needs `ASHE_HIRED`, her Free() row, her `bConfigVarIdles` toggle and her silence list (49 ASHE.md). Pair "first meeting" talks from 48 SERANA / 49 ASHE must have played ("S-x met" / "A-x met").
- `after:<title>` in the script = the part-1 talk with that title. IDs are given in the table.
- Rival rows (MG119-MG124) never fire while a romance quest of that follower is running (their Free rows cover this). K_CRUSH rows stop at K_TOG.

## New gate codes for this file
- `KRALDAR_JARL` = Kraldar holds Winterhold: Kraldar's actor `GetInFaction JobJarlFaction` == 1, or the CW Winterhold hold owner is the Empire **[UNC: Kraldar NPC FormID and which check the CW scripts flip]**. `KORIR_JARL` = not KRALDAR_JARL.
- `MG_AUGUR_MET` = MG04 (01F254) completed (Good Intentions; the Augur has spoken) **[UNC completion stage]**.
- `MG_OCULORY` = MG05 (01F255) completed (Revealing the Unseen) **[UNC completion stage; must be past the 20..49 silence]**.
- `MG_ANOMALY` = MG06 (01F256) running and its "anomalies loose in Winterhold" stage done, MG06 not completed **[UNC stage]**.
- `AFTERSHOCK` = the Arch-Mage radiant "Aftershock" (Tolfdir; magic anomalies) started **[UNC EditorID/FormID in Skyrim.esm]**.
- `ALEMBIC` = "Tolfdir's Alembic" completed **[UNC EditorID/FormID]**.
- `VAL_TEACH` = Val has been offered the College teaching post in his own College line **[UNC: quest/stage in AX ValSerano.esp; val.md section 1 item 6]**.
- `LOC:Shore` = exterior, Winterhold hold, within ~3000 units of the horker colony below the College **[UNC marker]**. `LOC:Dorm` = Hall of Attainment interior (student rooms) **[UNC cell FormID]**. `LOC:LunaRoom` = the player's assigned bed in the Hall of Attainment within 500 units **[UNC: bed ref]**. `LOC:CollegeExt` = exterior College courtyard. `LOC:ShalidorMaze` = Labyrinthian exterior maze area **[UNC: trigger box / marker]**.
- `NEAR:Sergius`, `NEAR:Phinis`, `NEAR:Nirya` = same rule as part 1's NEAR (seen once, controller remembers) **[UNC FormIDs]**.
- Combat targets: `COMBAT:icewraith` (IceWraithRace), `COMBAT:anomaly` (the MG magic anomaly race / actor base **[UNC]**), `COMBAT:falmer`, `COMBAT:draugr`, `COMBAT:Morokei` (his actor ref **[UNC]**), `COMBAT:undead` (skeleton or draugr race).

## Table

### Part 1 - The shore, the town and the snow
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG71 | K P | E LOC:Shore | MG_JOIN |
| MG72 | X P | E LOC:Winterhold | KRALDAR_JARL; MG_JOIN |
| MG73 | G P | E LOC:Winterhold (Frozen Hearth interior preferred) | MG_JOIN |
| MG74 | C K | E LOC:Bridge | after MG4 (a later crossing) |
| MG75 | L I | E AFTERFIGHT:icewraith in Winterhold hold | Lucien-Inigo intro done (JRLucienInigoRank >= 2) |
| MG76 | S P | E LOC:CollegeExt + CLEARNIGHT | SERANA; S following |

### Part 2 - The Arcanaeum after hours
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG77 | L P | E LOC:Arcanaeum | MG_JOIN; after MG13 |
| MG78 | R I | E LOC:Arcanaeum | after B6 (Inigo-Remi intro) |
| MG79 | S K | E LOC:Arcanaeum + hour 0..4 | SERANA; SER_VAMP; S-K met |
| MG80 | G P | T | GORE_READING; after MG11 |
| MG81 | X P | E LOC:Arcanaeum | after MG10 |
| MG82 | A L | E LOC:Arcanaeum | ASHE_REVEAL; A-L met |
| MG83 | C P | E LOC:Arcanaeum | after MG9 |

### Part 3 - Masters and lessons, part two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG84 | A R | E LOC:College | MG_JOIN; NEAR:Sergius seen once; ASHE_REVEAL; A-R met |
| MG85 | X K | E LOC:College | MG_JOIN; NEAR:Phinis seen once; after C3 |
| MG86 | R G | T | MG_SAARTHAL; after B15 or Remi-Gore meet |
| MG87 | K P | T | ALEMBIC |
| MG88 | V P | E LOC:College | MG_JOIN; NEAR:Nirya seen once |
| MG89 | X G | E LOC:College | MIRABELLE_ALIVE; SAVOS_ALIVE; MG_JOIN; after MG25; after X1 |
| MG90 | K P | E LOC:College | MG_LESSON |
| MG91 | R L | T | MG_AUGUR_MET; after B10 |
| MG92 | V G | E LOC:Winterhold exterior | MG_ANOMALY; after A3 |

### Part 4 - Living at the College
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG93 | K G | E LOC:Dorm + NIGHT | MG_JOIN; after A1 |
| MG94 | I V | E LOC:College | MG_JOIN; after I1 |
| MG95 | C K | E LOC:College | MG_JOIN; after MG26; after R1 |
| MG96 | R P | E LOC:College | MG_JOIN; K_TOG+ |
| MG97 | X S | E LOC:CollegeExt + SNOW | SERANA; SER_VAMP; S-X met |
| MG98 | L G | E LOC:College | MG_JOIN; after L1 |
| MG99 | C P | E LOC:College | after MG38; after MG20 |
| MG100 | A C | E LOC:College | ASHE_REVEAL; A-C met; after MG38 |
| MG101 | K P | E LOC:LunaRoom | MG_JOIN; K_CRUSH |

### Part 5 - The quiet bits of the story
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG102 | A P | T | MG_SAARTHAL; ASHE_REVEAL |
| MG103 | I K | E LOC:College + NIGHT | EYE_HERE; ANCANO_ALIVE; KaiandInigo stage >= 10 |
| MG104 | R P | T | MG_OCULORY |
| MG105 | V L | T | MG_OCULORY; after MG57 |
| MG106 | I G | E LOC:Winterhold | MG_SAVOS; KORIR_JARL; after MG2 |
| MG107 | C L | E LOC:ShalidorMaze | after MG58; after R11 |
| MG108 | K P | E CAMP or INN | STAFF_CARRIED; K_TOG+ |

### Part 6 - Arch-Mage Luna, part two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG109 | R X | T | AFTERSHOCK; Remi and Xelzaz not fallen out (`BPUFXelzazRemielFallenOut != 1`) |
| MG110 | I P | T | ARCH; after MG16 |
| MG111 | V P | T | ARCH |
| MG112 | C G | E LOC:College | ARCH; after R5 |
| MG113 | L P | E LOC:College | ARCH |
| MG114 | X P | E LOC:ArchQuarters | ARCH; after MG51 |
| MG115 | K P | T | ARCH |
| MG116 | S P | T | ARCH; SERANA; S following; after MG40 |
| MG117 | V G | T | VAL_TEACH; after A3 |
| MG118 | R P | T | ARCH; MGR_ARNIEL; after MG34 |

### Part 7 - Rivals in the tower
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG119 | G V | E LOC:College | MG_JOIN; G_FLIRT; V_FLIRT; GORE_READING; after A3 |
| MG120 | A K | E LOC:College | A_CRUSH; K_CRUSH; ASHE_REVEAL; A-K met; after MG82 |
| MG121 | S G | E LOC:Arcanaeum | SERANA; S_ROM_ON; G_FLIRT; GORE_READING; S-G met |
| MG122 | K P | E LOC:Bridge + NIGHT | MG_JOIN; K_TOG+ |
| MG123 | K P | T | ARCH; K_LOVE+ |
| MG124 | V P | E LOC:College | MG_JOIN; V_FLIRT; VAL_COL not started |

### Part 8 - Fight barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG125 | G I | E COMBAT:anomaly | MG_ANOMALY or AFTERSHOCK; after C2 |
| MG126 | L K | E COMBAT:falmer in LOC:Mzulft | MG05 running, stage < 20 or > 49 (outside the Oculory silence); Lucien-Kaidan intro done |
| MG127 | S G | E COMBAT:draugr in LOC:Saarthal | MG02 running; SERANA; S-G met |
| MG128 | C X | E COMBAT:icewraith in Winterhold hold | after R18 |
| MG129 | V K | E COMBAT:Morokei in LOC:Labyrinthian | MG07 running; after A2 |
| MG130 | R P | E COMBAT:undead in LOC:Midden | — |

## Notes for the build
- Luna speaks in 28 of 60 (46%), above the usual third by request (her home ground), like part 1.
- MG72 (KRALDAR_JARL) and MG106 (KORIR_JARL) are the two Jarl branches; neither fires on the wrong Jarl.
- MG80 / MG119 / MG121 all need GORE_READING (he reads in them). MG73 does not.
- MG101 is crush-only (Luna oblivious). MG96, MG108, MG122 need K_TOG+; MG123 needs K_LOVE+. No Luna romance line in any rival row; MG124 Luna answers dryly and never flirts.
- MG79 and MG97 are vampire-Serana rows (SER_VAMP); drop them after the cure.
- MG110 assumes Tolfdir takes on Mirabelle's work after ARCH (vanilla) **[UNC: confirm his post-MG08 role]**.
- MG126: Mzulft is College business only during MG05; the row may also fire on a later visit if MG05 is completed.
- Existing coverage avoided: part 1 topics (Urag's nod, Marobar Sul, the bridge test, Tolfdir's ward lesson, Mirabelle's feet, Colette, Drevis, J'zargo's scrolls, Brelyna's spells, Onmund's amulet, Enthir, Arniel, Ancano, Savos's tower, Arch-Mage robes/bed/jars/letters), 50 / 50b LUNA THE MAGE (library card, spell lessons), 37 SQ136-SQ140 (Winterhold town, Frozen Hearth, Birna), MN eyebrows notice, LT89 / LT Urag pettiness.
