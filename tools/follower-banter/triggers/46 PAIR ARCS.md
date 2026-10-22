# 46 PAIR ARCS - trigger rows (prefix PR, 220 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\46 PAIR ARCS.txt`.
Sources: `research\bibles\*.md` (all ten), TRIGGERS.md sections 2-5, `triggers\20 DAWNGUARD.md` sections 1 + 3 (Serana / Ashe `Free` rows, the `DG_*`, `SER_*`, `S_*`, `A_*`, `ASHE_*` codes), `triggers\33 DARK BROTHERHOOD.md` (`ASHE_HIRED`), ashe.md section 6 (`ASHE_LOGS`, `ASHE_AMENDS`).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana and Ashe `Free` rows in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue). Codes are listed in speaking order.

## 1. How the arcs play (new controller rules)

- **One chain per pair.** Each PART is one chain. Its talks play strictly in file order: `after:PRn` = talk PRn has played (or was skipped, see below). The first talk of a chain waits for the pair's existing meeting talk where there is one (`after:A1`, `after:B10`, `after:R13`...).
- `GAP2` = at least **2 in-game days** (`GameDaysPassed`) since the previous talk in the same chain played. The controller stores the day each PR talk played. Stops a whole friendship from playing out in one afternoon.
- `SKIPPABLE` = the talk has a one-way gate that can stop being true forever (`SER_VAMP` once Serana is cured, `not LUC_ADMIT` once Lucien has Clive). When the chain reaches it and that gate can no longer pass, mark it played without playing it, so the chain carries on. The next talk's `after:` and `GAP2` then count from the last talk that actually played.
- **Side talks** (IDs listed in section 4) hang off a chain with `after:` but are **not** in the chain: nothing waits for them. They need their romance gates. Luna has no lines in any of them.
- Timer talks (`T`) join the normal 5-minute pool. Event talks (`E ...`) fire on the moment. A chain's event talk simply waits for its event; it does not block other chains.
- One PR talk per pair per day at most, on top of `GAP2` (keeps side talks from landing on the same day as the chain step they hang off).

## 2. Gate codes used in this file (new)

Pair "met" gates (where no batch-1/2 meeting talk exists):
- `LK_MET` = Lucien's own Kaidan scenes have started: `JRLucienKaidanPast (540041:Lucien.esp)` set, or JRLucienFollower Kaidan scene 1 played. **[UNC which flag scene 1 sets]**
- `KI_MET` = `KaiandInigo (000842:Kaidan and Inigo Meet.esp)` stage >= 10 (same as K4).
- `LI_RANK2` = `JRLucienInigoRank (7638C2:Lucien.esp)` >= 2.
- `XL_MET` = `BPUFXelzazAndLucienInteractions (077DC4:BPUFXelzazFollower.esp)` intro stage done. **[UNC stage]**
- `RX_OK` = `BPUFXelzazAndRemielInteractions (3E67AF)` stage 11 done, `BPUFXelzazRemielFallenOut (5EB8BC)` != 1, and `BPUFXelzazRemielFallingOut` not between 11 and 13.
- `RV_BIZ` = `HLIOValRemiFriendshipTracker (HLIORemi.esp)` >= 2 (Business2 played). **[UNC value]**
- `RG_READ` = `HLIOGoreReading (6F46A0:HLIORemi.esp)` >= 1 (reading lessons started). **[UNC value]**
- `RC_MET` = `FA01RedcapAndRemiInteractionsQ (2B6E9E)` intro stage done, or `HLIORedcapBanter (57CB7D)` stage >= 1. **[UNC stages]**

Story and state:
- `PRE_REVEAL`: not used any more (see section 5).
- `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_LOGS`, `ASHE_AMENDS`: as ashe.md section 6 / `20 DAWNGUARD.md` section 3.
- `SERANA` (Serana is travelling with you; her `Free` row covers following), `SER_VAMP`, `DG_GARDEN`, `DG_PROPHET`, `DG_VALERICA`, `DG_END`, `S_COMP`, `A_CRUSH`: as `20 DAWNGUARD.md` section 3.
- `GORE_VIG` = `HD1GoreVigilant` completed / `HD1MemoriesQ` ("Fading Memories") completed: Gore has been rescued from Coldharbour. **[UNC: exact quest + stage in Gore - Vigilant.esp]**
- `GORE_FATHER`: as TRIGGERS.md section 4 (Gore knows Jo-Lee is his father).
- `INIGO_BV`: as TRIGGERS.md section 4.
- `not married` = player not married to anyone (`PlayerMarriedFaction` / Kaidan K04 < 100 / `AX_ValMarried` 0 / Gore not `G_OATH` / `SDA_IsSeranaMarried` 0).
- `after:DG8`, `after:AS12`, `after:AS19`, `after:SE46` = those talks (in 20 DAWNGUARD, 49 ASHE, 48 SERANA) have played, so a nickname or a pitch exists before it is used here.
- `VAL_FATHER`, `VAL_FATHIS`, `GORE_BAIL`, `BRYNJAR`, `HELGEN`, `LUC_ADMIT`, `K_*`, `G_*`, `V_*`: as TRIGGERS.md section 4. `Val00A >= 10` = Val's flirting has started at some point (`V_FLIRT` without the "still single" parts). `K04 >= 5` = Kaidan had his crush at some point.

Events:
- `SUNNY` = exterior, `IsPleasant`, hour 9..17 (same test as DG3).
- `SEA` = player in a coastal location or within 2000 units of the Sea of Ghosts shoreline. **[UNC: no clean coast keyword; fall back to Solitude/Dawnstar/Winterhold/Windhelm/Solstheim worldspace exteriors + WATER]**
- `E AFTERFIGHT:riekling` = player combat just ended and the last target was `DLC2RieklingRace`. **[UNC FormID]** Fires only on Solstheim in practice.
- `BIGPIG` = Redcap's Bigpig is following and within 1000 units. **[UNC: Bigpig ref/alias in Redcap's plugin]**
- `E exterior` = any exterior cell, player not in combat.
- `WATER+NIGHT` = `WATER` and `NIGHT` together (by a river or lake after dark).
- `WILD` = as the Lost talks: exterior, not `LocTypeHabitation`, player moving.
- `E AFTERFIGHT:bandit` = combat just ended, last target in `BanditFaction`.
- `not CITY` = not `LocTypeCity` / `LocTypeTown` (a quiet place).

## 3. Per-talk table

### Part 1 - Kaidan And Gore
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR1 | G K | T | after:A1 |
| PR2 | K G P | E CAMP | after:PR1; GAP2 |
| PR3 | G K | E CAMP+NIGHT | after:PR2; GAP2 |
| PR4 | K G P | E AFTERFIGHT | after:PR3; GAP2 |
| PR5 | G K | T | after:PR4; GAP2; GORE_BAIL |
| PR6 | G K | T | after:PR2; K_CRUSH; not G_TOG+ |
| PR7 | G K | E CAMP+NIGHT | after:PR6; K_TOG+ |

### Part 2 - Kaidan And Val
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR8 | V K P | T | after:A2 |
| PR9 | K V | T | after:PR8; GAP2 |
| PR10 | V K | E CAMP | after:PR9; GAP2; BRYNJAR |
| PR11 | V K P | E WATER | after:PR10; GAP2 |
| PR12 | V K | T | after:PR11; GAP2; VAL_FATHER |
| PR13 | V K | T | after:PR9; K_CRUSH; V_FLIRT |
| PR14 | K V | T | after:PR13; V_TOG+ |

### Part 3 - Gore And Val
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR15 | V G | T | after:A3 |
| PR16 | V G P | T | after:PR15; GAP2 |
| PR17 | G V | E CAMP | after:PR16; GAP2 |
| PR18 | G V P | T | after:PR17; GAP2 |
| PR19 | G V | T | after:PR18; GAP2 |
| PR20 | V G | T | after:PR16; G_FLIRT or V_FLIRT |
| PR21 | V G | T | after:PR20; G_TOG+ |

### Part 4 - Kaidan And Remi
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR22 | R K P | T | after:B1 |
| PR23 | R K P | T | after:PR22; after:B3; GAP2 |
| PR24 | R K | E AFTERFIGHT | after:PR23; GAP2 |
| PR25 | R K P | T | after:PR24; GAP2 |
| PR26 | K R | T | after:PR25; GAP2; not CITY |

### Part 5 - Kaidan And Xelzaz
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR27 | K X P | T | after:C3 |
| PR28 | X K | E SNOW | after:PR27; GAP2 |
| PR29 | X K | E CAMP | after:PR28; GAP2 |
| PR30 | K X P | E CAMP | after:PR29; GAP2 |
| PR31 | X K | T | after:PR30; GAP2; not CITY |

### Part 6 - Kaidan And Lucien
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR32 | L K | T | LK_MET |
| PR33 | L K P | T | after:PR32; GAP2 |
| PR34 | K L | T | after:PR33; GAP2; not LUC_ADMIT; SKIPPABLE |
| PR35 | L K P | E INN | after:PR34; GAP2 |
| PR36 | K L | T | after:PR35; GAP2; BRYNJAR |

### Part 7 - Kaidan And Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR37 | K C | T | after:R1 |
| PR38 | C K P | T | after:PR37; GAP2 |
| PR39 | K C P | T | after:PR38; GAP2 |
| PR40 | C K P | T | after:PR39; GAP2 |
| PR41 | C K | T | after:PR40; GAP2 |

### Part 8 - Kaidan And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR42 | K S | E CAMP | SERANA; SER_VAMP; SKIPPABLE |
| PR43 | S K | E INN | after:PR42; GAP2; SERANA |
| PR44 | S K | T | after:PR43; GAP2; BRYNJAR |
| PR45 | S K P | E INN | after:PR44; GAP2 |
| PR46 | S K | T | after:PR45; GAP2; SER_VAMP; SKIPPABLE |
| PR47 | S K | E INN | after:PR43; G_TOG+; K04 >= 5; S_COMP |

### Part 9 - Kaidan And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR48 | K A | E AFTERFIGHT:bandit | ASHE_HIRED |
| PR49 | A K | T | after:PR48; GAP2; ASHE_REVEAL |
| PR50 | K A P | T | after:PR49; GAP2 |
| PR51 | A K | T | after:PR50; GAP2; ASHE_Q1 |
| PR52 | A K | E CAMP+NIGHT | after:PR51; GAP2; ASHE_LOGS |
| PR53 | A K | T | after:PR49; A_CRUSH; K_TOG+ |

### Part 10 - Gore And Xelzaz
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR54 | G X | T | after:X1 |
| PR55 | X G P | T | after:PR54; GAP2 |
| PR56 | G X | E CAMP | after:PR55; GAP2 |
| PR57 | G X P | E CAMP | after:PR56; GAP2 |
| PR58 | G X | E AFTERFIGHT | after:PR57; GAP2 |

### Part 11 - Gore And Inigo
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR59 | I G | T | after:C2 |
| PR60 | G I P | T | after:PR59; GAP2 |
| PR61 | I G | T | after:PR60; GAP2; not CITY |
| PR62 | G I P | E CAMP | after:PR61; GAP2 |
| PR63 | G I | T | after:PR62; GAP2 |

### Part 12 - Gore And Lucien
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR64 | L G | T | after:L1 |
| PR65 | G L P | T | after:PR64; GAP2 |
| PR66 | L G | E CAMP+NIGHT | after:PR65; GAP2 |
| PR67 | P G L | T | after:PR66; GAP2 |
| PR68 | G L | T | after:PR67; GAP2; HELGEN |

### Part 13 - Gore And Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR69 | C G | T | after:R5 |
| PR70 | G C P | T | after:PR69; GAP2 |
| PR71 | C G | E CAMP | after:PR70; GAP2 |
| PR72 | G C P | E CITY | after:PR71; GAP2 |
| PR73 | G C | T | after:PR72; GAP2 |

### Part 14 - Gore And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR74 | G S | E WATER+NIGHT | SERANA; SER_VAMP; SKIPPABLE |
| PR75 | G S | E AFTERFIGHT | after:PR74; GAP2; SER_VAMP; SKIPPABLE |
| PR76 | G S | T | after:PR75; GAP2; SERANA |
| PR77 | G S P | T | after:PR76; GAP2 |
| PR78 | G S | T | after:PR77; GAP2; GORE_VIG; GORE_FATHER |

### Part 15 - Gore And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR79 | G A P | T | ASHE_HIRED |
| PR80 | A G | E exterior | after:PR79; GAP2; ASHE_REVEAL |
| PR81 | G A P | E AFTERFIGHT | after:PR80; GAP2 |
| PR82 | A G | T | after:PR81; GAP2; ASHE_Q1 |
| PR83 | A G | T | after:PR80; A_CRUSH; G_FLIRT; ASHE_REVEAL |

### Part 16 - Val And Xelzaz
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR84 | X V P | T | after:X5 |
| PR85 | V X | T | after:PR84; GAP2 |
| PR86 | X V | T | after:PR85; GAP2 |
| PR87 | V X P | T | after:PR86; GAP2 |
| PR88 | X V | T | after:PR87; GAP2 |

### Part 17 - Val And Inigo
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR89 | I V | T | after:I2 |
| PR90 | V I P | T | after:PR89; GAP2 |
| PR91 | V I | E CAMP+NIGHT | after:PR90; GAP2 |
| PR92 | V I P | T | after:PR91; GAP2 |
| PR93 | I V | T | after:PR92; GAP2; VAL_FATHIS |

### Part 18 - Val And Lucien
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR94 | V L P | T | after:C1 |
| PR95 | L V | T | after:PR94; GAP2 |
| PR96 | L V | T | after:PR95; GAP2 |
| PR97 | V L P | T | after:PR96; GAP2 |
| PR98 | L V | T | after:PR97; GAP2; VAL_FATHIS |

### Part 19 - Val And Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR99 | V C P | T | after:R9 |
| PR100 | C V P | T | after:PR99; GAP2 |
| PR101 | C V | E WATER | after:PR100; GAP2 |
| PR102 | V C P | E CAMP | after:PR101; GAP2 |
| PR103 | V C | T | after:PR102; GAP2 |

### Part 20 - Val And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR104 | S V | T | SERANA |
| PR105 | S V | E SUNNY | after:PR104; GAP2; SER_VAMP; SKIPPABLE |
| PR106 | V S | E CAMP+NIGHT | after:PR105; GAP2 |
| PR107 | V S P | T | after:PR106; GAP2; SER_VAMP; SKIPPABLE |
| PR108 | S V P | E SUNNY | after:PR107; GAP2; SER_VAMP; SKIPPABLE |
| PR109 | S V | E INN | after:PR104; K_TOG+; Val00A >= 10; S_COMP |

### Part 21 - Val And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR110 | V A | T | ASHE_HIRED |
| PR111 | V A P | T | after:PR110; GAP2; ASHE_REVEAL; WILD |
| PR112 | V A | E WATER | after:PR111; GAP2 |
| PR113 | V A P | E CAMP | after:PR112; GAP2 |
| PR114 | V A | T | after:PR113; GAP2; VAL_FATHIS |
| PR115 | V A | T | after:PR112; after:AS19; A_CRUSH; V_FLIRT; K_ANY |

### Part 22 - Remi And Inigo
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR116 | R I P | T | after:B6 |
| PR117 | I R | T | after:PR116; GAP2 |
| PR118 | R I | T | after:PR117; GAP2 |
| PR119 | I R P | E CAVE | after:PR118; GAP2 |
| PR120 | R I | E CAVE | after:PR119; GAP2 |

### Part 23 - Remi And Lucien
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR121 | L R | T | after:B10 |
| PR122 | L R P | T | after:PR121; GAP2 |
| PR123 | R L | T | after:PR122; GAP2 |
| PR124 | R L P | T | after:PR123; GAP2 |
| PR125 | L R | T | after:PR124; GAP2 |

### Part 24 - Remi And Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR126 | R C P | T | RC_MET |
| PR127 | C R | T | after:PR126; GAP2 |
| PR128 | R C P | T | after:PR127; GAP2 |
| PR129 | R C P | E AFTERFIGHT | after:PR128; GAP2 |
| PR130 | R C | E CAMP | after:PR129; GAP2 |

### Part 25 - Remi And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR131 | R S | T | SERANA |
| PR132 | R S | T | after:PR131; GAP2; SER_VAMP; SKIPPABLE |
| PR133 | R S | T | after:PR132; GAP2; DG_PROPHET |
| PR134 | R S P | E CITY | after:PR133; GAP2 |
| PR135 | R S | T | after:PR134; GAP2; DG_END |

### Part 26 - Remi And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR136 | R A | T | ASHE_HIRED |
| PR137 | R A | E CAMP | after:PR136; GAP2 |
| PR138 | P A R | E CAMP | after:PR137; GAP2 |
| PR139 | R A | T | after:PR138; GAP2 |
| PR140 | R A | E CAVE | after:PR139; GAP2; ASHE_REVEAL |

### Part 27 - Xelzaz And Inigo
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR141 | X I P | T | after:X6 |
| PR142 | I X | T | after:PR141; GAP2 |
| PR143 | I X | E CAMP+NIGHT | after:PR142; GAP2 |
| PR144 | X I P | E CAMP | after:PR143; GAP2 |
| PR145 | X I | T | after:PR144; GAP2 |

### Part 28 - Xelzaz And Lucien
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR146 | X L | T | XL_MET |
| PR147 | X L P | T | after:PR146; GAP2 |
| PR148 | L X | T | after:PR147; GAP2 |
| PR149 | L X P | T | after:PR148; GAP2 |
| PR150 | X L | T | after:PR149; GAP2 |

### Part 29 - Xelzaz And Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR151 | C X | T | after:R18 |
| PR152 | X C P | E AFTERFIGHT | after:PR151; GAP2 |
| PR153 | C X | E CAMP | after:PR152; GAP2 |
| PR154 | C X P | T | after:PR153; GAP2 |
| PR155 | C X | T | after:PR154; GAP2 |

### Part 30 - Xelzaz And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR156 | S X | T | SERANA |
| PR157 | X S | T | after:PR156; GAP2; SER_VAMP; SKIPPABLE |
| PR158 | X S | T | after:PR157; GAP2 |
| PR159 | S X P | E CAMP | after:PR158; GAP2 |
| PR160 | X S | T | after:PR159; GAP2 |

### Part 31 - Xelzaz And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR161 | X A | T | ASHE_REVEAL |
| PR162 | A X | E CAMP+NIGHT | after:PR161; GAP2 |
| PR163 | X A P | T | after:PR162; GAP2 |
| PR164 | X A | T | after:PR163; GAP2 |
| PR165 | A X | T | after:PR164; GAP2 |

### Part 32 - Inigo And Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR166 | I C | T | after:R13 |
| PR167 | I C P | E CAVE | after:PR166; GAP2 |
| PR168 | C I | E CAMP+NIGHT | after:PR167; GAP2 |
| PR169 | C I P | T | after:PR168; GAP2; BIGPIG |
| PR170 | C I | T | after:PR169; GAP2 |

### Part 33 - Inigo And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR171 | I S | E NIGHT | SERANA |
| PR172 | S I P | E MORNING | after:PR171; GAP2 |
| PR173 | I S | T | after:PR172; GAP2 |
| PR174 | I S P | E CAMP | after:PR173; GAP2 |
| PR175 | I S | T | after:PR174; GAP2; DG_END |

### Part 34 - Inigo And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR176 | I A | T | ASHE_REVEAL |
| PR177 | A I | T | after:PR176; GAP2; INIGO_BV |
| PR178 | I A P | T | after:PR177; GAP2; not married |
| PR179 | I A | E CLEARNIGHT | after:PR178; GAP2 |
| PR180 | P I A | E CAMP+NIGHT | after:PR179; GAP2 |

### Part 35 - Lucien And Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR181 | L C | T | after:R11 |
| PR182 | L C P | E CAMP | after:PR181; GAP2 |
| PR183 | L C | T | after:PR182; GAP2 |
| PR184 | L C P | T | after:PR183; GAP2 |
| PR185 | L C | T | after:PR184; GAP2 |

### Part 36 - Lucien And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR186 | L S P | T | SERANA |
| PR187 | L S | E CRYPT | after:PR186; GAP2 |
| PR188 | L S | E CAMP | after:PR187; GAP2 |
| PR189 | L S P | E MORNING | after:PR188; GAP2 |
| PR190 | S L | T | after:PR189; after:SE46; GAP2; DG_END |

### Part 37 - Lucien And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR191 | A L | T | ASHE_HIRED |
| PR192 | L A | E CLEARNIGHT | after:PR191; GAP2; ASHE_REVEAL |
| PR193 | L A | T | after:PR192; GAP2; ASHE_Q1 |
| PR194 | L A P | T | after:PR193; GAP2 |
| PR195 | A L | T | after:PR194; GAP2; ASHE_LOGS |

### Part 38 - Redcap And Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR196 | C S | T | SERANA; after:DG8 |
| PR197 | C S | T | after:PR196; GAP2; SER_VAMP; SKIPPABLE |
| PR198 | C S | E NIGHT | after:PR197; GAP2 |
| PR199 | C S P | E NIGHT exterior | after:PR198; GAP2 |
| PR200 | C S | T | after:PR199; GAP2 |

### Part 39 - Redcap And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR201 | C A | T | ASHE_HIRED |
| PR202 | C A | T | after:PR201; after:AS12; GAP2 |
| PR203 | C A P | E exterior | after:PR202; GAP2 |
| PR204 | C A | T | after:PR203; GAP2 |
| PR205 | C A | T | after:PR204; GAP2; BIGPIG |

### Part 40 - Serana And Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR206 | S A | E INN | SERANA; ASHE_HIRED; SER_VAMP; SKIPPABLE |
| PR207 | A S P | T | after:PR206; GAP2; SERANA; ASHE_REVEAL |
| PR208 | S A | T | after:PR207; GAP2; DG_END |
| PR209 | P S A | E CAMP | after:PR208; GAP2 |
| PR210 | S A | E INN | after:PR207; K_TOG+; S_COMP or A_CRUSH |

### Part 41 - Kaidan And Inigo (Fresh Callbacks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR211 | K I | T | KI_MET; BRYNJAR |
| PR212 | I K P | T | after:PR211; GAP2 |

### Part 42 - Lucien And Inigo (Fresh Callbacks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR213 | L I | E CRYPT | LI_RANK2 |
| PR214 | I L | T | after:PR213; GAP2 |

### Part 43 - Remi And Xelzaz (Fresh Callbacks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR215 | R X | T | RX_OK; after:B16 |
| PR216 | R X | T | after:PR215; GAP2; RX_OK |

### Part 44 - Remi And Val (Fresh Callbacks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR217 | V R P | T | RV_BIZ |
| PR218 | R V | E WATER | after:PR217; GAP2; SEA |

### Part 45 - Remi And Gore (Fresh Callbacks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR219 | R G | E CAMP | RG_READ |
| PR220 | G R | T | after:PR219; GAP2 |


## 4. Side talks (romance-gated, outside the chains)

PR6, PR7, PR13, PR14, PR20, PR21, PR47, PR53, PR83, PR109, PR115, PR210

Each needs its romance gate at the moment it fires. The `K_*`, `G_*`, `V_*`, `S_*`, `A_*` checks are the same as everywhere else. Luna has no line in any of them, and none of them has Luna choose anyone.

## 5. Notes for the build

- Talks that wait on a quest the player may never do (`GORE_BAIL`, `GORE_VIG`, `VAL_FATHER`, `VAL_FATHIS`, `HELGEN`, `BRYNJAR`, `INIGO_BV`, `DG_*`, `ASHE_*`) are almost always a chain's later steps, so each friendship still gets its first talks. A chain just waits there until the gate opens. Exceptions: PR211 (needs `BRYNJAR`) and the Ashe/Serana openers (need her hired / travelling).
- `SER_VAMP` talks are skipped if Serana is already cured when the chain reaches them (section 1). Nothing later in those chains needs her to still be a vampire.
- `PRE_REVEAL` is no longer used: 49 ASHE covers Ashe's secret with every follower, so no talk here plays before or around the reveal except PR201, PR79, PR110, PR136, PR191 and PR48, which work either way.
- No "Dragonborn" anywhere in the file. No Kaidan cult references: PR26 mentions the tattoo only as "who I was when I got it" (same level as B4); PR5 and PR46 only say he has done things / has a temper.
- Brynjar is named only in PR44 and PR211, both behind `BRYNJAR`. PR10, PR36 and PR43 mention "the man who raised me" and are gated the same way where the detail matters.
- Written alongside 45 PARTY LIFE, 48 SERANA and 49 ASHE, which landed mid-way. Their topics were checked and avoided (see the script header). PR202, PR115 and PR190 wait for AS12, AS19 and SE46 so nicknames and pitches exist first.
- Remi/Xelzaz talks (PR215, PR216) also need Remi and Xelzaz on good terms (`RX_OK`).
