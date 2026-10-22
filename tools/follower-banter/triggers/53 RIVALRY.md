# 53 RIVALRY - trigger rows (prefix RV, 200 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\53 RIVALRY.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4, `triggers\20 DAWNGUARD.md` (Serana/Ashe Free() rows and gate codes), `triggers\48 SERANA.md`, `triggers\49 ASHE.md`, and the bibles for all eleven speakers.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`), the Dawnguard silence in `20 DAWNGUARD.md` section 2, the Ashe silence in `49 ASHE.md`, and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, S Serana, A Ashe, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment).

Every row with S also needs `SERANA` (DLC1VQ02 stage 5 done) and Serana Free. Every row with A also needs `ASHE_HIRED` and Ashe Free.

## Gate codes used in this file

Reused unchanged (TRIGGERS.md section 4, 20 DAWNGUARD.md section 3, 49 ASHE.md): `K_CRUSH`, `K_TOG+`, `K_LOVE+`, `K_ENG`, `K_ANY`, `G_FLIRT`, `G_TOG+`, `G_ANY`, `V_FLIRT`, `V_TOG+`, `V_ANY`, `S_ROM_ON`, `S_COMP`, `S_KISS`, `S_LOVE`, `NOT_S_KISS`, `SER_VAMP`, `A_CRUSH`, `A_LOVE`, `A_ANY`, `ASHE_REVEAL`, `DG_VALERICA`, `VAL_FATHER`, `MG_JOIN`.

New here:
- `S_ACT` = Serana's romance has really started: `S_ROM_ON` and `S_COMP` (SDA_SeranaRomance03 A3777F completed). `S_ROM_ON` alone is not enough, because the toggle defaults to 1 from game start.
- `S_EARLY` = `S_ACT` and `NOT_S_KISS`.
- `S_PAST` = `S_ACT` (it stays true after you pick Kaidan; Serana's quests do not reset). Rows say `not S_LOVE` where she must not have said "I love you".
- `G_PAST` = `HD1Romance (6D6924:GORE.esp) == 1`, including after `HD1Breakup == 1`. Gore was sweet on Luna at some point.
- `V_PAST` = `Val00A (3AA4A5:AX ValSerano.esp)` stage >= 10, or `AX_FriendZone == 1`. Val was courting Luna at some point. **[UNC: stage 10 is the Amulet of Dibella step; 5-7 are the Pale Lady date and would also do]**
- `A_PAST` = `MM_RM (2F3039:Ashe - Fire and Blood.esp) >= 4`. Ashe was sweet on Luna at some point.
- `RIV2` = at least two of `K_ANY`, `G_ANY`, `V_ANY`, `S_ACT`, `A_ANY` are true. `RIV3` = at least three.
- `RIV2_PAST` = at least two of `G_PAST`, `V_PAST`, `S_PAST`, `A_PAST` (the "others were sweet on you" check for Part 8 and RV186).
- `not X_TOG+` / `not A_LOVE` / `not V_TOG+` = that rival is NOT currently together with Luna. Used so a "comfort the loser" or "made peace" talk never plays on a branch where that rival actually won.
- `SNOW` on RV86 = IsSnowing in the exterior the inn belongs to (any snow weather in the hold). **[UNC: interior weather check; drop the gate if it can't be read]**
- `after:RVn` = that RV talk already played. `after:KL14`, `after:KL15`, `after:SE57`, `after:PR115`, `after:AS19` are the existing talks with those IDs.

Events (TRIGGERS.md section 4 unless noted): `E CAMP`, `E CAMP+NIGHT`, `E INN`, `E MORNING`, `E NIGHT`, `E SNOW`, `E WATER`, `E CAVE`, `E exterior`, `E CITY:Solitude`, `E AFTERFIGHT`, `E AFTERFIGHT:bandit`, `E AFTERFIGHT:troll` (last target TrollRace / FrostTrollRace), `E AFTERFIGHT (Kaidan below half health)` (49 ASHE.md), `E WATER (sea coast)` (48 SERANA.md), `E exterior, IsPleasant, hour 10..16` (sunny daytime, outdoors).

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| RV1 | G K | T | K_CRUSH; G_FLIRT |
| RV2 | K G P | E CAMP | K_CRUSH; G_FLIRT |
| RV3 | V K | T | K_CRUSH; V_FLIRT |
| RV4 | K V | T | K_CRUSH; V_FLIRT |
| RV5 | S K | T | K_CRUSH; S_EARLY; SER_VAMP |
| RV6 | S K P | T | K_CRUSH; S_EARLY |
| RV7 | A K | T | K_CRUSH; A_CRUSH |
| RV8 | K A P | T | K_CRUSH; A_CRUSH |
| RV9 | V G | T | G_FLIRT; V_FLIRT |
| RV10 | G V P | T | G_FLIRT; V_FLIRT |
| RV11 | G S P | T | G_FLIRT; S_EARLY |
| RV12 | S G P | T | G_FLIRT; S_EARLY |
| RV13 | A G | T | G_FLIRT; A_CRUSH |
| RV14 | G A P | E CAMP | G_FLIRT; A_CRUSH; ASHE_REVEAL |
| RV15 | V S | T | V_FLIRT; S_EARLY |
| RV16 | V S P | T | V_FLIRT; S_EARLY |
| RV17 | V A | T | V_FLIRT; A_CRUSH; ASHE_REVEAL; after:AS19 |
| RV18 | A V P | T | V_FLIRT; A_CRUSH; ASHE_REVEAL |
| RV19 | S A P | E CAMP | S_EARLY; SER_VAMP; A_CRUSH; ASHE_REVEAL |
| RV20 | S A | T | S_EARLY; A_CRUSH; ASHE_REVEAL |
| RV21 | K G P | E SNOW | K_CRUSH; G_FLIRT |
| RV22 | K G P | T | K_CRUSH; G_FLIRT |
| RV23 | G K | E CAMP+NIGHT | K_CRUSH; G_FLIRT |
| RV24 | V K P | E exterior | K_CRUSH; V_FLIRT |
| RV25 | V K P | E INN | K_CRUSH; V_FLIRT |
| RV26 | V K P | E CAMP | K_CRUSH; V_FLIRT |
| RV27 | K S | T | K_CRUSH; S_EARLY |
| RV28 | S K P | E SNOW | K_CRUSH; S_EARLY |
| RV29 | K S P | T | K_CRUSH; S_EARLY |
| RV30 | A K | E CAMP+NIGHT | K_CRUSH; A_CRUSH; ASHE_REVEAL |
| RV31 | K A P | E MORNING | K_CRUSH; A_CRUSH; ASHE_REVEAL |
| RV32 | A K P | T | K_CRUSH; A_CRUSH |
| RV33 | V G P | E INN | G_FLIRT; V_FLIRT |
| RV34 | V G P | T | G_FLIRT; V_FLIRT |
| RV35 | G V P | T | G_FLIRT; V_FLIRT |
| RV36 | G S | E CAMP+NIGHT | G_FLIRT; S_EARLY |
| RV37 | S G P | T | G_FLIRT; S_EARLY |
| RV38 | G S P | E exterior, IsPleasant, hour 10..16 | G_FLIRT; S_EARLY; SER_VAMP |
| RV39 | G A P | T | G_FLIRT; A_CRUSH |
| RV40 | G A P | E AFTERFIGHT:bandit | G_FLIRT; A_CRUSH |
| RV41 | A G | E MORNING | G_FLIRT; A_CRUSH; ASHE_REVEAL |
| RV42 | V S P | E INN | V_FLIRT; S_EARLY |
| RV43 | V S | T | V_FLIRT; S_EARLY |
| RV44 | V S P | T | V_FLIRT; S_EARLY |
| RV45 | V A | E INN | V_FLIRT; A_CRUSH |
| RV46 | V A P | T | V_FLIRT; A_CRUSH |
| RV47 | V A P | E CAMP | V_FLIRT; A_CRUSH; ASHE_REVEAL |
| RV48 | S A P | T | S_EARLY; SER_VAMP; A_CRUSH; ASHE_REVEAL |
| RV49 | A S P | T | S_EARLY; A_CRUSH |
| RV50 | A S | T | S_EARLY; A_CRUSH; ASHE_REVEAL |
| RV51 | G K | T | K_CRUSH; G_FLIRT |
| RV52 | G K P | T | K_CRUSH; G_FLIRT |
| RV53 | V K P | E MORNING | K_CRUSH; V_FLIRT |
| RV54 | V K P | T | K_CRUSH; V_FLIRT |
| RV55 | S K P | T | K_CRUSH; S_EARLY |
| RV56 | K S | E MORNING | K_CRUSH; S_EARLY; after:SE57 |
| RV57 | K A | T | K_CRUSH; A_CRUSH |
| RV58 | K A P | T | K_CRUSH; A_CRUSH |
| RV59 | G V P | E INN | G_FLIRT; V_FLIRT |
| RV60 | V G | T | G_FLIRT; V_FLIRT |
| RV61 | S G | T | G_FLIRT; S_EARLY; SER_VAMP |
| RV62 | G S P | E MORNING | G_FLIRT; S_EARLY |
| RV63 | A G P | T | G_FLIRT; A_CRUSH |
| RV64 | G A P | E exterior | G_FLIRT; A_CRUSH; ASHE_REVEAL |
| RV65 | V S P | T | V_FLIRT; S_EARLY |
| RV66 | V S | T | V_FLIRT; S_EARLY |
| RV67 | A V | E WATER | V_FLIRT; A_CRUSH; ASHE_REVEAL |
| RV68 | A V | T | V_FLIRT; A_CRUSH |
| RV69 | S A | T | S_EARLY; SER_VAMP; A_CRUSH; ASHE_REVEAL |
| RV70 | S A P | T | S_EARLY; A_CRUSH; ASHE_REVEAL |
| RV71 | K G | E AFTERFIGHT | K_CRUSH; G_FLIRT |
| RV72 | G K | T | K_CRUSH; G_FLIRT |
| RV73 | V K P | E CAMP+NIGHT | K_CRUSH; V_FLIRT |
| RV74 | K V | T | K_CRUSH; V_FLIRT |
| RV75 | S K | T | K_CRUSH; S_EARLY |
| RV76 | K S | T | K_ANY; S_ACT; SER_VAMP |
| RV77 | A K | T | K_CRUSH; A_CRUSH; after:KL14 |
| RV78 | A K | E AFTERFIGHT | K_ANY; A_ANY |
| RV79 | V G | E INN | G_FLIRT; V_FLIRT |
| RV80 | G V P | E CAMP | G_FLIRT; V_FLIRT |
| RV81 | S G | T | G_FLIRT; S_ACT |
| RV82 | G S | E CAMP+NIGHT | G_FLIRT; S_ACT; SER_VAMP |
| RV83 | A G | T | G_FLIRT; A_CRUSH |
| RV84 | A G | T | G_FLIRT; A_CRUSH |
| RV85 | V S | T | V_ANY; S_ACT; VAL_FATHER |
| RV86 | S V | E INN | V_FLIRT; S_ACT; SNOW |
| RV87 | A V | T | V_FLIRT; A_CRUSH; not K_TOG+; after:PR115 |
| RV88 | V A P | E exterior | V_FLIRT; A_CRUSH |
| RV89 | S A | T | S_ACT; SER_VAMP; A_ANY; ASHE_REVEAL |
| RV90 | A S | T | S_ACT; A_ANY; ASHE_REVEAL; after:RV70 |
| RV91 | K G | E AFTERFIGHT:troll | K_ANY; G_ANY |
| RV92 | G K | T | K_ANY; G_ANY |
| RV93 | V K | T | K_ANY; V_ANY |
| RV94 | V K | E CAMP+NIGHT | K_ANY; V_ANY |
| RV95 | S K | T | K_ANY; S_KISS; SER_VAMP |
| RV96 | K S P | E AFTERFIGHT | K_ANY; S_ACT |
| RV97 | K A | T | K_ANY; A_ANY; ASHE_REVEAL |
| RV98 | A K | E AFTERFIGHT (Kaidan below half health) | K_ANY; A_ANY |
| RV99 | V G | T | G_ANY; V_ANY; after:RV10; after:RV35; after:RV64 |
| RV100 | G V | E CAMP+NIGHT | G_ANY; V_ANY |
| RV101 | G S | T | G_ANY; S_ACT; DG_VALERICA |
| RV102 | S G | T | G_ANY; S_KISS |
| RV103 | G A | T | G_ANY; A_ANY; after:RV83 |
| RV104 | A G | T | G_ANY; A_ANY |
| RV105 | S V | T | V_ANY; S_KISS |
| RV106 | V S | E WATER (sea coast) | V_ANY; S_ACT |
| RV107 | V A | T | V_ANY; A_ANY; ASHE_REVEAL; after:RV17 |
| RV108 | A V | T | V_ANY; A_ANY; ASHE_REVEAL |
| RV109 | S A | E NIGHT | S_ACT; A_ANY; ASHE_REVEAL |
| RV110 | S A | T | S_KISS; A_ANY |
| RV111 | G K | T | G_TOG+; K_CRUSH |
| RV112 | K G | E CAMP+NIGHT | K_TOG+; G_FLIRT; not G_TOG+ |
| RV113 | V K | T | V_TOG+; K_CRUSH |
| RV114 | K V | E INN | K_TOG+; V_FLIRT; not V_TOG+ |
| RV115 | S K | T | S_KISS; K_CRUSH |
| RV116 | K S | T | K_TOG+; S_ACT; NOT_S_KISS |
| RV117 | A K | T | A_LOVE; K_CRUSH; ASHE_REVEAL |
| RV118 | G V | E WATER | G_TOG+; V_FLIRT |
| RV119 | V G | T | V_TOG+; G_FLIRT |
| RV120 | G S | T | S_KISS; G_FLIRT; not G_TOG+ |
| RV121 | G S | T | G_TOG+; S_ACT; NOT_S_KISS |
| RV122 | A G | T | A_LOVE; G_FLIRT; ASHE_REVEAL |
| RV123 | V S | T | V_TOG+; S_ACT; NOT_S_KISS |
| RV124 | S V | E MORNING | S_KISS; V_FLIRT; not V_TOG+ |
| RV125 | A V | T | A_LOVE; V_FLIRT; ASHE_REVEAL |
| RV126 | V A | T | V_TOG+; A_CRUSH; ASHE_REVEAL |
| RV127 | A S | T | S_KISS; A_CRUSH |
| RV128 | S A | T | A_LOVE; S_ACT; NOT_S_KISS |
| RV129 | G V P | E INN | K_LOVE+; G_PAST; V_PAST; not G_TOG+; not V_TOG+ |
| RV130 | V K | T | S_LOVE; K_CRUSH; V_FLIRT |
| RV131 | A K S | T | K_ANY; S_ACT; A_ANY; ASHE_REVEAL |
| RV132 | V G S | E INN | G_ANY; V_ANY; S_ACT |
| RV133 | K G P | T | K_CRUSH; G_FLIRT; MG_JOIN |
| RV134 | V G S | E CITY:Solitude | G_ANY; V_ANY; S_ACT |
| RV135 | V K G | T | K_ANY; G_ANY; V_ANY |
| RV136 | S A V | T | S_ACT; A_ANY; V_ANY |
| RV137 | K A P | E INN | K_CRUSH; A_CRUSH |
| RV138 | G A P | T | G_FLIRT; A_CRUSH |
| RV139 | V K G | T | K_ANY; G_ANY; V_ANY |
| RV140 | G A K | T | K_ANY; G_ANY; A_ANY; ASHE_REVEAL; after:KL15 |
| RV141 | S A V | T | S_ACT; A_ANY; V_ANY |
| RV142 | G K V | E CAMP+NIGHT | K_CRUSH; G_FLIRT; V_FLIRT |
| RV143 | G K | T | K_LOVE+; G_PAST; not G_TOG+; after:KL15 |
| RV144 | G K P | T | K_ENG; G_PAST; not G_TOG+ |
| RV145 | G P | T | K_LOVE+; G_PAST; not G_TOG+ |
| RV146 | G K | E CAMP+NIGHT | K_LOVE+; G_PAST; not G_TOG+ |
| RV147 | V K | T | K_ENG; V_PAST; not V_TOG+ |
| RV148 | V P | T | K_LOVE+; V_PAST; not V_TOG+ |
| RV149 | V G K | T | K_ENG; G_PAST; V_PAST |
| RV150 | V K | T | K_LOVE+; V_PAST; not V_TOG+ |
| RV151 | S K | E INN | K_LOVE+; S_PAST; not S_LOVE |
| RV152 | S P | T | K_LOVE+; S_PAST; not S_LOVE |
| RV153 | S K | T | K_LOVE+; S_PAST; not S_LOVE; DG_VALERICA |
| RV154 | S K | E CAMP+NIGHT | K_LOVE+; S_PAST; not S_LOVE |
| RV155 | A K P | T | K_LOVE+; A_PAST; not A_LOVE; ASHE_REVEAL |
| RV156 | A K P | T | K_LOVE+; A_PAST; not A_LOVE; ASHE_REVEAL; after:RV155 |
| RV157 | A K | E CAMP+NIGHT | K_LOVE+; A_PAST; not A_LOVE; ASHE_REVEAL |
| RV158 | A P | T | K_LOVE+; A_PAST; not A_LOVE |
| RV159 | K G V | E INN | K_LOVE+; G_PAST; V_PAST; not G_TOG+; not V_TOG+ |
| RV160 | K G V | E CAMP+NIGHT | K_LOVE+; G_PAST; V_PAST; not G_TOG+; not V_TOG+ |
| RV161 | K P | T | K_LOVE+; RIV2_PAST |
| RV162 | V G S | T | K_ENG; G_PAST; V_PAST; S_PAST |
| RV163 | R X | T | RIV2 |
| RV164 | R K | T | K_CRUSH; RIV2; after:RV163 |
| RV165 | R I | T | RIV2; after:RV163 |
| RV166 | C R | T | RIV2; after:RV163 |
| RV167 | V R | T | V_ANY; RIV2; after:RV163 |
| RV168 | R S | T | S_ACT; RIV2; after:RV163 |
| RV169 | A R | T | A_ANY; RIV2; ASHE_REVEAL; after:RV163 |
| RV170 | R G | T | K_LOVE+; G_PAST; after:RV163 |
| RV171 | R P | T | RIV2; after:RV163 |
| RV172 | R X | T | RIV2; after:RV163 |
| RV173 | V X | T | RIV2; after:RV163 |
| RV174 | K X | T | K_CRUSH; RIV2 |
| RV175 | G X | E CAMP | G_ANY; RIV2 |
| RV176 | S X | T | S_ACT; RIV2 |
| RV177 | X P | T | RIV2 |
| RV178 | A X | T | A_ANY; RIV2; ASHE_REVEAL |
| RV179 | I K | T | K_CRUSH |
| RV180 | G I | T | G_FLIRT |
| RV181 | I V | T | V_FLIRT |
| RV182 | S I | T | S_ACT |
| RV183 | A I | T | A_ANY; ASHE_REVEAL |
| RV184 | L I | T | RIV2 |
| RV185 | I P | E CAVE | K_CRUSH; RIV2 |
| RV186 | I K | T | K_LOVE+; RIV2_PAST |
| RV187 | L K P | T | K_CRUSH |
| RV188 | L G | T | RIV3 |
| RV189 | V L | T | V_FLIRT |
| RV190 | A L | T | A_ANY |
| RV191 | L P | T | RIV3 |
| RV192 | L S | E CAMP | S_ACT |
| RV193 | L K | T | K_ENG |
| RV194 | C K P | T | K_CRUSH |
| RV195 | V C | T | V_FLIRT; RIV2 |
| RV196 | C S | T | S_ACT |
| RV197 | C G P | T | G_FLIRT |
| RV198 | A C | T | A_ANY; ASHE_REVEAL |
| RV199 | L C | T | RIV2 |
| RV200 | C P | T | RIV2 |

## Notes for the build
- Pacing: rival talks share one cooldown, separate from the general timer: at most one RV talk per in-game day, so the rivalry runs underneath the rest of the banter instead of flooding it.
- Order inside a pair: a pair's Part 1 talk plays before that pair's Part 2-5 talks; Part 3 before Part 4; Part 4 before Part 5. Cross-talk callbacks are listed as `after:` gates.
- Part 6 (RV111-RV130) is branch-locked: each row names who is together with Luna and checks the other rival is not.
- Part 8 (RV143-RV162) needs `K_LOVE+` (or `K_ENG`). It never plays if the other rival is currently together with Luna.
- Luna never commits, never picks anyone in her own lines and never says "I love you". In every `K_CRUSH` talk where she speaks she misses Kaidan's feelings completely. RV161 ("Half the Party") is the one place she realises the others were sweet on her, and only once she and Kaidan are lovers.
- Serana's vampire jokes carry `SER_VAMP`. Anything about what Ashe is carries `ASHE_REVEAL`.
- No "Dragonborn", no Brynjar, no cult, no Fathis, no wedding or proposal content (RV149, RV162 and RV193 only joke about a future day while `K_ENG` is set).
- Topics avoided on purpose (already written elsewhere): the Ravens' rules (KL15, PR6, PR7) except as callbacks, honest rivals (PR13/14), sunrise and midnight (SE57/59), the treaty (KL14) except its amendment, the mead bet (PR20), the Val-Ashe truce (PR115) except its renewal, heart-rate logging, the fish, the logs, the wooden dragon, cloaks, chairs, "who saved her", the We Also Fancied Her club, the file on Luna, the losers' toasts (PR109, PR210, PR47), and the rival side talks written alongside this file in 46b PAIR ARCS 2 (PR225-PR390: the dawn watch, the very small log, page nine, the trophy, the truce extended indefinitely; RV87 is gated `not K_TOG+` so it can never follow PR313).
- Luna speaks in 67 of 200 talks (33%).
