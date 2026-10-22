# 47 KAIDAN AND LUNA DEEP - trigger rows (prefix KL, 180 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\47 KAIDAN AND LUNA DEEP.txt`.
Sources: `research\triggers\kaidan_block.md` (§2a, §2b, §5 K04 map), `TRIGGERS.md` §2-§4, `triggers\20 DAWNGUARD.md` §1 + gate codes (Serana/Ashe Free rows, S_/A_ codes), `research\bibles\*.md`.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).

## 1. Romance step gates (exact K04 ranges)

K04 = `06D900:0Kaidan.esp` (runtime 8406D900). Every KL row needs `GetStageDone K01 30 == 1` (Kaidan rescued) and Kaidan Free, even rows where he has no line (the talk is about him).

| Step | Rows | Gate | Why this range |
|---|---|---|---|
| Crush | KL1-KL60 | `GetStage K04 >= 5 AND <= 24` | Flirting stages 5/10/15/20 only. Luna is oblivious, so nothing may fire once the first date is offered (25) or the first night is available (30+). Stages 37/42/57 can't occur here. |
| Together | KL61-KL100 | `GetStage K04 >= 50 AND <= 64 AND != 57` | Past the morning-after. 57 is the awkward/platonic reply, excluded like Kaidan's own romance lines. Includes his declaration (60-62); no row mentions it. |
| In love | KL101-KL130 | `GetStage K04 >= 65 AND <= 80` (rows marked 70..80: `>= 70 AND <= 80`) | 65 = after his declaration. Rows where Luna is openly tender wait for 70 (the player has said it back). |
| In love, late | KL130 | `GetStage K04 >= 75 AND <= 80` | KaidanPreProposal is running; he's thinking about permanence. No proposal is mentioned. |
| Engaged | KL131-KL150 | `GetStage K04 >= 81 AND <= 99` | 81 = proposed/accepted; 85/87/90 = wedding type picked. No row names a venue or describes a ceremony. |
| Married | KL151-KL180 | `GetStage K04 == 100` OR `KaidanRef GetInFaction PlayerMarriedFaction == 1` | 100 is set by his post-wedding talk. |

A romance pause (ResumeRomanceScript resets K04 to 0 for 168h) fails every KL gate, which is what we want.

## 2. Other gate codes used here

Existing (TRIGGERS.md §4): `G_FLIRT`, `V_FLIRT`, `MG_JOIN`, `TG_BRYN`, `DB`, `BRYNJAR` [UNC stage, see TRIGGERS.md §6], `SERANA`. Existing (20 DAWNGUARD.md): `NOT_S_KISS`, `S_COMP`, `S_KISS`, `SER_VAMP`, `A_CRUSH`, `ASHE_REVEAL`. Serana/Ashe rows also imply their Free rows from 20 DAWNGUARD.md §1.

New in this file:
- `HONEYMOON_DONE` = `GetStageDone KaiHoneymoon (A5EA55:Kaidan - Immersive Features.esp) 150 == 1`. KL153 only, and it never says where they went.
- `DLC1VQ04 completed` = Chasing Echoes (00284F:Dawnguard.esm) completed, so Luna has seen Valerica's courtyard garden. KL159 only.
- `date m8 d3` = `GameMonth == 8 AND GameDay == 3` (Tales and Tallow, 3rd of Hearthfire), window day 3 or 4 like the other holidays. **[UNC]** whether Holidays.esp observes this day; the date check works without it.
- `E WATER + Eastmarch` = WATER while the player is in Eastmarch hold near the hot springs. **[UNC]** hold check (GetInCurrentLocation on the Eastmarch hold location, FormID to look up) and a hot-spring proxy; fall back to plain WATER in Eastmarch.
- `E LOC:Arcanaeum` = GetInCell Arcanaeum (College of Winterhold). **[UNC FormID]**
- `E INN + CITY:Windhelm` = player in Candlehearth Hall. **[UNC]** use GetInCurrentLocation CandlehearthHallLocation if it exists, else INN while in Windhelm.
- `E after dragon soul absorbed` = same hook as K9 in TRIGGERS.md.
- `after:L2`, `after:R1`, `after:K8` = those talks from the earlier batches have played.

## 3. Per-talk table

### Part 1 - CRUSH (60 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL1 | K P | T | K04 5..24 |
| KL2 | K L | T | K04 5..24 |
| KL3 | P K | E INN | K04 5..24 |
| KL4 | P S K | T | K04 5..24; SERANA; NOT_S_KISS; after:KL3 |
| KL5 | K G | T | K04 5..24; after:KL4 |
| KL6 | P K | T | K04 5..24; after:KL5 |
| KL7 | L K | T | K04 5..24; after:KL6 |
| KL8 | K P | T | K04 5..24 |
| KL9 | I K | E CAMP | K04 5..24; after:KL8 |
| KL10 | K C P | E CAMP | K04 5..24 |
| KL11 | K R | T | K04 5..24 |
| KL12 | P K R | T | K04 5..24; after:KL11 |
| KL13 | V K P | T | K04 5..24 |
| KL14 | A K | T | K04 5..24; A_CRUSH |
| KL15 | G K | T | K04 5..24; G_FLIRT |
| KL16 | V P K | T | K04 5..24; V_FLIRT |
| KL17 | K S | T | K04 5..24; SERANA |
| KL18 | K P S | T | K04 5..24; SERANA; after:KL17 |
| KL19 | K P | E CITY:Whiterun | K04 5..24 |
| KL20 | K P | E INN + CITY:Windhelm | K04 5..24 |
| KL21 | K L | E CITY:Winterhold | K04 5..24; MG_JOIN |
| KL22 | P K | E DWEMER | K04 5..24 |
| KL23 | P K | E CRYPT | K04 5..24 |
| KL24 | K P | E RAIN | K04 5..24 |
| KL25 | P K | E STORM | K04 5..24 |
| KL26 | P I K | E MORNING + CAMP | K04 5..24 |
| KL27 | P K | E AFTERFIGHT | K04 5..24 |
| KL28 | P K | E AFTERFIGHT:bandit | K04 5..24 |
| KL29 | P K | E GIANT | K04 5..24 |
| KL30 | P K | E WATER | K04 5..24 |
| KL31 | I K P | E CAVE | K04 5..24 |
| KL32 | V K P | E CAMP + NIGHT | K04 5..24 |
| KL33 | K P | T | K04 5..24; date m8 d3 |
| KL34 | P K | E MORNING | K04 5..24 |
| KL35 | P K | E INN | K04 5..24 |
| KL36 | P K | T | K04 5..24 |
| KL37 | K P | T | K04 5..24 |
| KL38 | K L | T | K04 5..24 |
| KL39 | K P | T | K04 5..24; after:KL38 |
| KL40 | R P K | T | K04 5..24 |
| KL41 | K P | T | K04 5..24; after:KL40 |
| KL42 | K X | T | K04 5..24 |
| KL43 | P K | T | K04 5..24; after:KL42 |
| KL44 | R K | T | K04 5..24 |
| KL45 | K L | T | K04 5..24; after:KL28 |
| KL46 | G K | T | K04 5..24; after:KL45; after:L2 |
| KL47 | X K | T | K04 5..24 |
| KL48 | P S K | E CAMP + NIGHT | K04 5..24; SERANA |
| KL49 | G K | T | K04 5..24 |
| KL50 | I K | T | K04 5..24 |
| KL51 | K V | E CAMP + NIGHT | K04 5..24 |
| KL52 | P K | T | K04 5..24 |
| KL53 | P G K | E AFTERFIGHT | K04 5..24 |
| KL54 | C K P | T | K04 5..24 |
| KL55 | A K | T | K04 5..24 |
| KL56 | A K P | E CAMP | K04 5..24 |
| KL57 | S K | T | K04 5..24; SERANA |
| KL58 | V G K | T | K04 5..24; G_FLIRT; V_FLIRT |
| KL59 | S K | T | K04 5..24; S_COMP; SER_VAMP |
| KL60 | A K | T | K04 5..24; A_CRUSH; ASHE_REVEAL |

### Part 2 - TOGETHER (40 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL61 | P K | E CAMP + NIGHT | K04 50..64, not 57 |
| KL62 | G K | T | K04 50..64, not 57; after:KL61 |
| KL63 | P K | T | K04 50..64, not 57 |
| KL64 | L K P | T | K04 50..64, not 57 |
| KL65 | V P K | E INN + MORNING | K04 50..64, not 57 |
| KL66 | G K | T | K04 50..64, not 57; G_FLIRT; after:KL15 |
| KL67 | V K | T | K04 50..64, not 57; V_FLIRT |
| KL68 | S P K | T | K04 50..64, not 57; SERANA; after:KL4 |
| KL69 | P L K | T | K04 50..64, not 57; after:KL7 |
| KL70 | R K | T | K04 50..64, not 57; after:KL43 |
| KL71 | A K | T | K04 50..64, not 57; A_CRUSH; ASHE_REVEAL |
| KL72 | C K P | T | K04 50..64, not 57 |
| KL73 | P K | T | K04 50..64, not 57; after:KL1 |
| KL74 | P K | T | K04 50..64, not 57; after:KL61 |
| KL75 | X K P | T | K04 50..64, not 57 |
| KL76 | I K | T | K04 50..64, not 57 |
| KL77 | G K | E CAMP + MORNING | K04 50..64, not 57 |
| KL78 | P K V | E CITY:Solitude | K04 50..64, not 57 |
| KL79 | P K | E AFTERFIGHT | K04 50..64, not 57 |
| KL80 | K P | E MORNING | K04 50..64, not 57 |
| KL81 | S P | T | K04 50..64, not 57; SERANA |
| KL82 | A S | T | K04 50..64, not 57; A_CRUSH; ASHE_REVEAL; SERANA |
| KL83 | L K | E LOC:Arcanaeum | K04 50..64, not 57; MG_JOIN |
| KL84 | K P | T | K04 50..64, not 57; after:KL8 |
| KL85 | P K | E INN | K04 50..64, not 57 |
| KL86 | K G P | T | K04 50..64, not 57 |
| KL87 | P K | E SNOW | K04 50..64, not 57 |
| KL88 | P K | T | K04 50..64, not 57 |
| KL89 | G K | T | K04 50..64, not 57; after:L2 |
| KL90 | I K | E AFTERFIGHT | K04 50..64, not 57 |
| KL91 | P K | T | K04 50..64, not 57 |
| KL92 | V G | E INN | K04 50..64, not 57; G_FLIRT; V_FLIRT |
| KL93 | A P | T | K04 50..64, not 57; A_CRUSH; ASHE_REVEAL |
| KL94 | K P | E CLEARNIGHT | K04 50..64, not 57 |
| KL95 | P K | T | K04 50..64, not 57 |
| KL96 | K R | T | K04 50..64, not 57 |
| KL97 | K P | T | K04 50..64, not 57 |
| KL98 | C K | T | K04 50..64, not 57; after:R1 |
| KL99 | X K | T | K04 50..64, not 57 |
| KL100 | S K | T | K04 50..64, not 57; S_KISS; SER_VAMP |

### Part 3 - IN LOVE (30 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL101 | K G | T | K04 65..80 |
| KL102 | P K | E HOUSE | K04 70..80 |
| KL103 | K P | E CAMP + NIGHT | K04 70..80 |
| KL104 | R K | E CITY:Riften | K04 65..80; TG_BRYN |
| KL105 | P K | T | K04 70..80 |
| KL106 | V K | T | K04 65..80 |
| KL107 | V G K | E INN | K04 65..80 |
| KL108 | K P | E WATER + Eastmarch | K04 70..80 |
| KL109 | L P | T | K04 70..80 |
| KL110 | X P | T | K04 65..80 |
| KL111 | C K P | T | K04 65..80 |
| KL112 | K P | E CLEARNIGHT | K04 70..80 |
| KL113 | G P | E INN | K04 70..80 |
| KL114 | P K | E AFTERFIGHT | K04 70..80 |
| KL115 | G V | T | K04 70..80; after:KL114 |
| KL116 | A K | T | K04 65..80 |
| KL117 | I P | T | K04 70..80 |
| KL118 | K P | E CAMP | K04 70..80; BRYNJAR |
| KL119 | K X | T | K04 65..80 |
| KL120 | K P | T | K04 70..80; after:KL46 |
| KL121 | K R | T | K04 65..80 |
| KL122 | K P | E CAMP + NIGHT | K04 70..80 |
| KL123 | K P | E AFTERFIGHT | K04 70..80 |
| KL124 | G K | E CAMP | K04 65..80 |
| KL125 | V K | E MORNING | K04 65..80 |
| KL126 | K I | E CLEARNIGHT | K04 65..80 |
| KL127 | S P | T | K04 70..80; SERANA; SER_VAMP |
| KL128 | L K | E after dragon soul absorbed | K04 65..80; DB |
| KL129 | G K P | E CAMP | K04 70..80 |
| KL130 | X K | T | K04 75..80 |

### Part 4 - ENGAGED (20 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL131 | V G | T | K04 81..99 |
| KL132 | P K | T | K04 81..99 |
| KL133 | V K | T | K04 81..99 |
| KL134 | S K | T | K04 81..99; SERANA |
| KL135 | A K | T | K04 81..99 |
| KL136 | R K P | T | K04 81..99 |
| KL137 | C K | T | K04 81..99 |
| KL138 | I K | T | K04 81..99 |
| KL139 | L K | T | K04 81..99 |
| KL140 | X K | T | K04 81..99 |
| KL141 | K G | E CAMP + NIGHT | K04 81..99 |
| KL142 | P S | T | K04 81..99; SERANA |
| KL143 | K P | T | K04 81..99 |
| KL144 | P K C | T | K04 81..99 |
| KL145 | P K | E INN + NIGHT | K04 81..99 |
| KL146 | R P | T | K04 81..99 |
| KL147 | G K | T | K04 81..99 |
| KL148 | A P | T | K04 81..99; A_CRUSH; ASHE_REVEAL |
| KL149 | L I | T | K04 81..99 |
| KL150 | K P | E CLEARNIGHT | K04 81..99 |

### Part 5 - MARRIED (30 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL151 | K G | T | K04 100 |
| KL152 | P K | T | K04 100 |
| KL153 | V K | T | K04 100; HONEYMOON_DONE |
| KL154 | K P | E AFTERFIGHT | K04 100; after:KL27 |
| KL155 | G V | T | K04 100 |
| KL156 | X P K | E MORNING + HOUSE | K04 100 |
| KL157 | I K | T | K04 100 |
| KL158 | C K | T | K04 100 |
| KL159 | S P K | T | K04 100; SERANA; DLC1VQ04 completed |
| KL160 | A K | T | K04 100; ASHE_REVEAL |
| KL161 | L K P | T | K04 100 |
| KL162 | V K | T | K04 100 |
| KL163 | G K | E WATER | K04 100 |
| KL164 | P K | E INN + NIGHT | K04 100; after:KL18; after:K8 |
| KL165 | P K | T | K04 100; after:KL80 |
| KL166 | R X | T | K04 100 |
| KL167 | K P | T | K04 100 |
| KL168 | K G | E after dragon soul absorbed | K04 100; DB |
| KL169 | K P | E AFTERFIGHT | K04 100; after:KL9 |
| KL170 | C K | E CITY:Whiterun | K04 100; after:KL167 |
| KL171 | P K | E RAIN | K04 100; after:KL24 |
| KL172 | K P | E SNOW | K04 100 |
| KL173 | V K | E INN | K04 100 |
| KL174 | P K | E CAMP + NIGHT | K04 100; after:KL10 |
| KL175 | A S | T | K04 100; SERANA; ASHE_REVEAL |
| KL176 | L K | T | K04 100; after:KL139 |
| KL177 | I K | T | K04 100 |
| KL178 | R K | T | K04 100 |
| KL179 | K P | E CAMP + NIGHT | K04 100; BRYNJAR |
| KL180 | P K | E HOUSE | K04 100; after:KL22 |

## 4. Notes for the build
- Kaidan's set pieces (kaidan_block.md §2b items 1-11) block every KL row, with or without Kaidan speaking: KaiWeddingNukeIdles, the three wedding windows, KaiHoneymoon 20..149, FirstKissScene/ProposalScene, KMD finale group, Companions showdown scenes, BlackScene, ArrestScene. Also KaiSTFUQuest running and STFUVarNPCGeneral == 1.
- Chains: KL3 > KL4 > KL5 > KL6 > KL7 (the matchmaking run) must play in order and only during the crush; if the crush ends early the rest never plays. Their payoffs KL68/KL69 need KL4/KL7 to have played.
- Payoff rows (`after:` a crush row) simply never fire if the setup row didn't play. That's intended: a callback with no setup is worse than no callback.
- Rival rows (KL14, KL15, KL16, KL58, KL59, KL60, KL66, KL67, KL71, KL82, KL92, KL93, KL100, KL148): Luna either has no line or a branch-neutral one. She never chooses anyone in them.
- KL4 and KL68 must not both qualify while Serana's own romance is past the kiss: KL4 needs NOT_S_KISS. KL100 needs S_KISS, so it can't overlap with KL4.
- Ashe rows that mention logs, steel or her matrix carry ASHE_REVEAL. KL55/KL56/KL116/KL135 don't need it (no machine reference).
- Same-event priority: on AFTERFIGHT, prefer the step's own row (KL27/KL53 crush, KL79/KL90 together, KL114/KL123 in love, KL154/KL169 married); only one fires per fight.
- Existing coverage avoided: every Kaidan line in the five Desktop scripts and the 13 files in FOLLOWER BANTER SCRIPTS (the fence post, wolf/goat/hood/mask misreads, snow or ash in her hair, fever/potion misreads, staring at reflections, the gala dance, rain dance, aurora hair, carved dragon, rock and dead-spider gifts, horker picnic/stew/breakfast, thin walls, humming, ward-theory bedtime reading, honey I'm home, blue door, bench for two, my-wife, uncle Scrap). KL164 deliberately calls back to K8's fence post; KL78 to A18's comb.
