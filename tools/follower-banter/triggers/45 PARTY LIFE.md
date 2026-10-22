# 45 PARTY LIFE - trigger rows (prefix PY, 180 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\45 PARTY LIFE.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` (sections 2-4), `triggers\20 DAWNGUARD.md` (sections 1 and 3: Serana/Ashe Free rows and S_/A_/SER_ gate codes), `research\bibles\*.md`.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).

## 1. File-wide rules
- **Meets first.** Every row also needs each follower pair in it to have played its "meets" talk (TRIGGERS.md chain rule). Not repeated per row.
- **Serana rows** need her Free row (20 DAWNGUARD.md section 1), which already means she is following. Rows with blood/feeding jokes add `SER_VAMP`.
- **Ashe rows** all carry `ASHE_REVEAL` (she is warm and open about being an automaton only after the reveal). Respect her `bConfigVarIdles` toggle (her Free row).
- **Story chains** (Part 1) and **make-ups** (Part 10) use `after:X+Nh`: X has played and at least N game hours have passed since it ended. The controller stamps `GameDaysPassed` when each talk ends.
- **Event pacing:** at most one PY talk per in-game night at camp (CAMP+NIGHT), so a story doesn't stack with another story. [design choice]
- Party-life talks are low priority: if a quest/place talk from another file is eligible on the same event, that one wins.

## 2. Event and gate codes used here
Events (TRIGGERS.md section 4): `CAMP`, `NIGHT`, `INN`, `RAIN`, `SNOW`, `MORNING` (5..9; `MORNING (hour 4..6)` = PREDAWN), `AFTERFIGHT[:type]`, `WILD`.
- `WILD` = exterior, not LocTypeHabitation/City/Town/Settlement, player moving (same proxy as the N talks in TRIGGERS.md).
- `CAMP+NIGHT` = CAMP and NIGHT together. `CAMP+RAIN` = CAMP and RAIN. `E MORNING, after a night at camp` = MORNING and the last sleep/wait was at a CAMP location [UNC: controller must remember last sleep location].
- `AFTERFIGHT:vampire` as in 20 DAWNGUARD.md. `AFTERFIGHT (in a crypt)` = AFTERFIGHT and player in LocTypeDraugrCrypt.
- `CAMP+NIGHT (SNOW or cold weather)` = CAMP+NIGHT and (SNOW or weather classification cold / Frostfall exposure) [UNC: use SNOW if no cold check].

Gates:
- `after:X` = talk X played. `after:X+6h` / `+24h` = X played at least 6 / 24 game hours ago. `after:X or after:Y` = either.
- `K_CRUSH`, `K_ANY`, `K_TOG+`, `G_FLIRT`, `V_FLIRT` as TRIGGERS.md section 4. `G_ANY` / `V_ANY` as 20 DAWNGUARD.md.
- `S_COMP`, `S_KISS`, `SER_VAMP`, `A_CRUSH`, `ASHE_REVEAL` as 20 DAWNGUARD.md section 3.
- `RIVALS2` (new) = at least two of K_ANY, G_ANY, V_ANY are true.
- `PARTY_YEAR` (new) = GameDaysPassed >= (day K01 stage 30 was set) + 365. The controller stamps the day when it first sees K01 30 done. [UNC: no vanilla stamp; for saves where K01 finished before install, stamp on first load and wait a year from there]
- `PY_COUNT>=60` (new) = at least 60 PY talks played (count the played bits in the PY block).

## 3. Per-talk table

### Part 1 - Campfire stories
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY1 | K G P | E CAMP+NIGHT | — |
| PY2 | R K V | E CAMP+NIGHT | after:PY1+6h |
| PY3 | I K P | E CAMP+NIGHT | after:PY2+6h |
| PY4 | G L X | E CAMP+NIGHT | — |
| PY5 | C G V | E CAMP+NIGHT | after:PY4+6h |
| PY6 | K G P | E CAMP+NIGHT | after:PY5+6h |
| PY7 | V R I | E CAMP+NIGHT | — |
| PY8 | L V | E CAMP+NIGHT | after:PY7+6h |
| PY9 | G V C | E CAMP+NIGHT | after:PY8+6h |
| PY10 | R S K | E CAMP+NIGHT | — |
| PY11 | X R P | E CAMP+NIGHT | after:PY10+6h |
| PY12 | G R C | E CAMP+NIGHT | after:PY11+6h |
| PY13 | X L I | E CAMP+NIGHT | — |
| PY14 | C X R | E CAMP+NIGHT | after:PY13+6h |
| PY15 | K X P | E CAMP+NIGHT | after:PY14+6h |
| PY16 | I G V | E CAMP+NIGHT | — |
| PY17 | L I C | E CAMP+NIGHT | after:PY16+6h |
| PY18 | K I P | E CAMP+NIGHT | after:PY17+6h |
| PY19 | L G R | E CAMP+NIGHT | — |
| PY20 | I L S | E CAMP+NIGHT | after:PY19+6h |
| PY21 | K L P | E CAMP+NIGHT | after:PY20+6h |
| PY22 | C R P | E CAMP+NIGHT | — |
| PY23 | K C X | E CAMP+NIGHT | after:PY22+6h |
| PY24 | V C I | E CAMP+NIGHT | after:PY23+6h |
| PY25 | S R K | E CAMP+NIGHT | — |
| PY26 | L S P | E CAMP+NIGHT | after:PY25+6h |
| PY27 | R A G | E CAMP+NIGHT | ASHE_REVEAL |
| PY28 | I A P | E CAMP+NIGHT | ASHE_REVEAL; after:PY27+6h |
| PY29 | L A X | E CAMP | ASHE_REVEAL |
| PY30 | G P K | E CAMP+NIGHT | — |
| PY31 | L P C | E CAMP+NIGHT | after:PY30+6h |
| PY32 | R V G | E CAMP | after:PY3; after:PY6; after:PY9 |

### Part 2 - Games
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY33 | V K I | E INN | — |
| PY34 | I R P | E INN | after:PY33 |
| PY35 | V K C | E INN | after:PY33 |
| PY36 | G S K | E CAMP | — |
| PY37 | L P G | E CAMP | — |
| PY38 | C P R | E CAMP | after:PY37 |
| PY39 | S P X | E CAMP | after:PY37 |
| PY40 | P S L | E MORNING | after:PY39+24h |
| PY41 | R G V | E CAMP | — |
| PY42 | L K I | E CAMP+NIGHT | — |
| PY43 | R V P | E INN | — |
| PY44 | R G K | E INN | after:PY43 |
| PY45 | R K P | E INN | K_CRUSH; after:PY43 |
| PY46 | R G L | E CAMP | — |
| PY47 | I L C | E CAMP | after:PY46 |
| PY48 | G A K | E CAMP | ASHE_REVEAL; after:PY46 |
| PY49 | R A P | E CAMP | ASHE_REVEAL; after:PY48 |
| PY50 | L K V | E AFTERFIGHT | — |
| PY51 | L G X | E AFTERFIGHT | after:PY50 |
| PY52 | L I P | E AFTERFIGHT | after:PY51 |
| PY53 | C K I | E WILD | — |
| PY54 | L K S | E WILD | SER_VAMP |
| PY55 | I A C | E CAMP | ASHE_REVEAL |
| PY56 | R V I | E CAMP | after:PY33; after:PY37; after:PY46 |

### Part 3 - Songs and rhymes
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY57 | L K P | E CAMP | — |
| PY58 | R K L | E CAMP | after:PY57 |
| PY59 | V I G | E CAMP+NIGHT | — |
| PY60 | I C X | E CAMP | — |
| PY61 | L G P | E CAMP | — |
| PY62 | R V S | E CAMP | after:PY61 |
| PY63 | K G R | E WILD | after:PY61 |
| PY64 | V C I | E RAIN | — |
| PY65 | C K G | E CAMP+NIGHT | — |

### Part 4 - Cooking
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY66 | P X K | E CAMP | — |
| PY67 | K I X | E CAMP | after:PY66 |
| PY68 | R G C | E CAMP | after:PY66 |
| PY69 | X V G | E CAMP | after:PY66 |
| PY70 | C L K | E CAMP | after:PY66 |
| PY71 | V R I | E CAMP | after:PY66 |
| PY72 | G S P | E CAMP | after:PY66 |
| PY73 | A P X | E CAMP | ASHE_REVEAL; after:PY66 |
| PY74 | X I C | E CAMP | — |
| PY75 | P R K | E CAMP | after:PY66 |
| PY76 | V G K | E INN | — |

### Part 5 - Watches, snoring and tents
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY77 | P S G | E CAMP+NIGHT | SER_VAMP |
| PY78 | L I | E CAMP+NIGHT | — |
| PY79 | K C I | E MORNING | — |
| PY80 | K A | E MORNING (hour 4..6) | ASHE_REVEAL |
| PY81 | V R K | E MORNING | — |
| PY82 | G P K | E MORNING | after:PY81 |
| PY83 | L X I | E MORNING | — |
| PY84 | L G I | E CAMP | — |
| PY85 | K I G | E MORNING | after:PY84 |
| PY86 | V K P | E CAMP+RAIN | K_CRUSH |
| PY87 | S R L | E MORNING | — |
| PY88 | X G C | E CAMP+NIGHT (SNOW or cold weather) | — |

### Part 6 - Washing up
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY89 | P G R | E WILD | — |
| PY90 | V I R | E WILD | after:PY89 |
| PY91 | R K L | E WILD | after:PY89 |
| PY92 | X G V | E WILD | — |
| PY93 | S K P | E WILD | K_CRUSH |
| PY94 | G K R | E CAMP | — |
| PY95 | L I G | E CAMP | — |
| PY96 | X P K | E CAMP | — |
| PY97 | R G S | E CAMP | — |
| PY98 | A V K | E MORNING | ASHE_REVEAL |

### Part 7 - The party fund
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY99 | P V X | E CAMP | — |
| PY100 | X R C | E CAMP | after:PY99 |
| PY101 | X K P | E CAMP | after:PY100 |
| PY102 | V X I | E INN | after:PY99 |
| PY103 | V X K | E CAMP | after:PY100 |
| PY104 | G X P | E CAMP | after:PY101 |

### Part 8 - Luna's rules and the vote
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY105 | P R K | E CAMP | — |
| PY106 | L X | E CAMP | after:PY105 |
| PY107 | P S G | E CAMP | SER_VAMP; after:PY105 |
| PY108 | G V K | E CAMP | after:PY105; after:PY63 |
| PY109 | I C | E WILD | after:PY105 |
| PY110 | L K P | E WILD | after:PY109 |
| PY111 | G R P | E WILD | — |
| PY112 | V I P | E WILD | after:PY111 |
| PY113 | L X C | E CAMP | after:PY112 |
| PY114 | A P K | E WILD | ASHE_REVEAL |

### Part 9 - Running jokes
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY115 | I G C | E WILD | — |
| PY116 | L I V | E CAMP | after:PY115 |
| PY117 | K C I | E AFTERFIGHT | after:PY116 |
| PY118 | C I P | E WILD | after:PY117+24h |
| PY119 | S G K | T | — |
| PY120 | A V R | T | ASHE_REVEAL |
| PY121 | L P I | T | after:PY119 or after:PY120 |
| PY122 | C G K | E WILD | after:PY121 |

### Part 10 - Fights and making up
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY123 | L K R | E CAMP | after:PY57 |
| PY124 | K L | T | after:PY123+6h |
| PY125 | X G V | E CAMP | — |
| PY126 | X G | E CAMP | after:PY125+6h |
| PY127 | R G I | E AFTERFIGHT | — |
| PY128 | G R | T | after:PY127+6h |
| PY129 | C V K | E MORNING | — |
| PY130 | V C | T | after:PY129+6h |
| PY131 | I K G | E MORNING | — |
| PY132 | K I | T | after:PY131+6h |
| PY133 | A R L | T | ASHE_REVEAL |
| PY134 | R A | T | ASHE_REVEAL; after:PY133+6h |
| PY135 | G S K | E AFTERFIGHT:vampire | SER_VAMP |
| PY136 | G S | E CAMP+NIGHT | SER_VAMP; after:PY135+6h |
| PY137 | L I X | T | — |
| PY138 | L I | T | after:PY137+6h |
| PY139 | L P V | E INN | — |
| PY140 | P L | T | after:PY139+6h |
| PY141 | P K G | E AFTERFIGHT | K_TOG+ |
| PY142 | K P | T | K_TOG+; after:PY141+6h |
| PY143 | A G R | T | ASHE_REVEAL |
| PY144 | A G | T | ASHE_REVEAL; after:PY143+6h |
| PY145 | X I L | T | — |
| PY146 | X I | T | after:PY145+6h |
| PY147 | V G L | E AFTERFIGHT (in a crypt) | — |
| PY148 | V L | T | after:PY147+6h |

### Part 11 - Hard nights
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY149 | R X P | E CAMP+NIGHT | — |
| PY150 | K L | E CAMP+NIGHT | — |
| PY151 | S G | E CAMP+NIGHT | — |
| PY152 | R I P | E CAMP+NIGHT | — |
| PY153 | C K | E CAMP+NIGHT | — |
| PY154 | L S P | E CAMP+NIGHT | — |
| PY155 | G K P | E CAMP+NIGHT | — |
| PY156 | I A P | E CAMP+NIGHT | ASHE_REVEAL |
| PY157 | V X | E CAMP+NIGHT | — |
| PY158 | K V I | E MORNING | — |
| PY159 | R G L | E MORNING | — |

### Part 12 - Small occasions
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY160 | R G P | E CAMP | — |
| PY161 | I V C | T | — |
| PY162 | L A P | T | ASHE_REVEAL; after:PY160 |
| PY163 | G C X | T | — |
| PY164 | K I P | T | PARTY_YEAR |

### Part 13 - The party's reputation
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY165 | V G K | E INN | — |
| PY166 | R X C | E INN | — |
| PY167 | L I | E INN | — |
| PY168 | S K G | E INN | — |
| PY169 | G V A | E INN | ASHE_REVEAL |
| PY170 | L G P | E INN | — |

### Part 14 - Little rivalries
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY171 | K V P | E MORNING | K_CRUSH; V_FLIRT |
| PY172 | G K C | E CAMP | K_ANY; G_FLIRT |
| PY173 | S P K | E CAMP | S_COMP; not S_KISS; K_CRUSH |
| PY174 | A V | T | A_CRUSH; ASHE_REVEAL; V_FLIRT |
| PY175 | G V P | E CAMP | G_FLIRT; V_FLIRT |
| PY176 | A K P | E INN | K_ANY; A_CRUSH; ASHE_REVEAL |
| PY177 | S G V | T | S_COMP; G_ANY or V_ANY |
| PY178 | V K | T | K_TOG+; V_FLIRT |
| PY179 | G V K | E INN | RIVALS2 |

### Part 15 - The fire burns low
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY180 | P I G | E CAMP+NIGHT | PY_COUNT>=60; after:PY115 |

## 4. Notes for the build
- Luna speaks in 62 of 180 talks (34%). Speaker counts: Kaidan 71, Gore 68, Val 49, Remi 48, Xelzaz 36, Inigo 52, Lucien 50, Redcap 36, Serana 23, Ashe 20, Luna 62.
- Existing coverage avoided: snoring map (HF46) and Gore's landslide snore (G1), the home cooking rota (HF43), the arm-wrestle for Luna's bags (KX3), cards at the Guildhouse (LT76) and the Forgotten City (WS99), loaded dice (TG32), the company name (MN50), ghost stories (W11), Kaidan's cloak (W6), Redcap in Val's bedroll (R8).
- No Kaidan cult content, no Brynjar, no Fathis/Mora, no Clive, no Morvic, no Jo-Lee. Nobody says "Dragonborn".
- PY123 (Lucien's limerick about Kaidan's face) only touches the tattoo as "a bad time", the same deflection Kaidan's own mod uses.
- PY119-PY122 (Rorikstead): the scarecrow belongs to Lemkil's farm. Purely a party memory; no quest or NPC record is touched.

