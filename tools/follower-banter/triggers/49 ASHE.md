# 49 ASHE - trigger rows (prefix AS, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\49 ASHE.txt`.
Sources: `research\bibles\ashe.md` (sections 1, 3 and 6), the other bibles for each partner, `TRIGGERS.md` sections 2-4, and `triggers\20 DAWNGUARD.md` (Free() rows and the shared Ashe/Serana gate codes).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check).
Type: T = timer, E = event (fires on the moment).

Ashe Free() is the row in `20 DAWNGUARD.md` section 1. Serana Free() likewise (AS27, AS72).
Every AS talk also needs `ASHE_HIRED` and Ashe Free, even where the row only lists a later gate.

## Ashe silence (add to WorldQuiet while any of these hold; ashe.md section 6)
- `MM_AMQ_04` (00AA1A:Ashe - Fire and Blood.esp) stage 45..80 (alone in Medeus's lab, "a day or two").
- `MM_AMQ_05` (056A66) running (the logs, the fight with Canas).
- `MM_AMQ_07` (D6A70C) running (summit, confession, walk down).
- `MM_AMQ_07Epilogue` (E5DA07) running (the home talk).
- `MM_AMQ_06a` (C07BE9) running and stage < 80 (the orphans' village scenes).
- `MM_AMQ_06cNEW` (380306) stage 40..60 (deciding Rolen's fate).
- `MM_AQ00` / `MM_AQ01` / `MM_AQ02` running (her memory flashbacks).
Note: the Serana patch also has a quest 00AA1A. Always use the plugin name with the FormID.

## Gate codes used in this file

Reused (TRIGGERS.md section 4 and 20 DAWNGUARD.md section 3): `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_LOGS`, `A_CRUSH`, `A_LOVE`, `A_ANY`, `S_KISS`, `SER_VAMP`, `DG_VALERICA`, `K_CRUSH`, `K_ANY`, `K_TOG+`, `K_LOVE+`, `G_FLIRT`, `G_TOG+`, `V_FLIRT`, `V_ANY`, `GORE_FATHER`, `VAL_FATHIS`, `LUC_ADMIT`.

New here (all Ashe - Fire and Blood.esp unless noted; IDs from ashe.md section 6):
- `ASHE_HIRED` = `MM_AsheIntro` (0A7946) completed.
- `NOT_REVEAL` = ASHE_HIRED and NOT ASHE_REVEAL (`MM_FriendshipQuest` 1A9DEE stage 70 not done and var `MM_AutomatonReveal` != 1). Part 1 only.
- `ASHE_NEVAS` = `MM_AMQ_02` (BB194C) completed.
- `ASHE_ROLEN1` = `MM_AMQ_03` (BC5D8F) completed.
- `ROLEN_DEAD` = ASHE_ROLEN1 and Rolen ref (75C0F7) `GetDead == 1`. `ROLEN_ALIVE` = ASHE_ROLEN1 and `GetDead == 0`. **[UNC: confirm 75C0F7 is the Rolen ref used in 03 and 06cNEW]**
- `ASHE_MEDEUS` = `MM_AMQ_04` (00AA1A) completed. AS25 fires on the first tick after the 45..80 silence ends.
- `ASHE_ORPHANS` = `MM_AMQ_06a` (C07BE9) completed. `ASHE_OATH` = `MM_AMQ_06b` (C11E04) completed. `ASHE_FANG` = `MM_AMQ_06cNEW` (380306) completed.
- `ASHE_SUMMIT` = `MM_AMQ_07` (D6A70C) completed. `ASHE_EPI` = `MM_AMQ_07Epilogue` (E5DA07) completed.
- `first A+K talk in this file` (and A+R, A+C, A+I, A+X, A+L) = no other AS talk with that pair has played yet.
- Rival talks with A_CRUSH use the shared code: `MM_RM` (2F3039) >= 4 and `MM_AsheRomance` (A5E1EF) == 0.

Events (TRIGGERS.md section 4 unless noted):
- `E CAMP`, `E CAMP+NIGHT`, `E CAMP or INN`, `E INN`, `E INN+NIGHT`, `E RAIN`, `E CITY:Markarth`.
- `E NIGHT (HOUSE or INN)` = NIGHT and the player is in LocTypePlayerHouse or LocTypeInn.
- `E 7000 steps (as Q4)` = same detection as Q4 in TRIGGERS.md (High Hrothgar path).
- `E LOC:Workshop` = arrival at Aryo's workshop in the south-east Rift. **[UNC: location / cell FormID not traced; the workshop cell is in Ashe - Fire and Blood.esp]**
- `E AFTERFIGHT:<type>`: `dwemer` (last target LocTypeDwarvenAutomatons race / DwarvenAutomaton keyword), `Thalmor` (as TRIGGERS.md), `bandit`, `spider` (FrostbiteSpiderRace family), `necromancer` (as 48 SERANA.md), `forsworn` (ForswornFaction). `AFTERFIGHT (Kaidan below half health)` = Kaidan's health dropped under 50% during the fight (same mechanism as K19's player-health check). **[UNC: needs the controller to track Kaidan's health during combat]**

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| AS1 | K A | T | ASHE_HIRED; NOT_REVEAL; first A+K talk in this file |
| AS2 | G A | E CAMP+NIGHT | NOT_REVEAL |
| AS3 | V A P | T | NOT_REVEAL |
| AS4 | R A | T | NOT_REVEAL; first A+R talk in this file |
| AS5 | C A | T | NOT_REVEAL; first A+C talk in this file |
| AS6 | I A | T | NOT_REVEAL; first A+I talk in this file |
| AS7 | X A | E CAMP or INN | NOT_REVEAL; first A+X talk in this file |
| AS8 | L A | T | NOT_REVEAL; first A+L talk in this file |
| AS9 | A P | T | NOT_REVEAL |
| AS10 | K A P | E 7000 steps (as Q4) | NOT_REVEAL |
| AS11 | R A | T | ASHE_REVEAL; after AS4 |
| AS12 | C A | T | ASHE_REVEAL; after AS5 |
| AS13 | G A | T | ASHE_REVEAL |
| AS14 | A K | T | ASHE_REVEAL; after AS4 |
| AS15 | I A | T | ASHE_REVEAL; after AS6 |
| AS16 | X A P | E CAMP or INN | ASHE_REVEAL; after AS7 |
| AS17 | L A | T | ASHE_Q1 |
| AS18 | A P | T | ASHE_Q1 |
| AS19 | V A | T | ASHE_REVEAL |
| AS20 | A V | T | ASHE_NEVAS; after AS19 |
| AS21 | A K | T | ASHE_ROLEN1 |
| AS22 | G A | T | ROLEN_DEAD; GORE_FATHER; after AS13 |
| AS23 | A I | T | ASHE_ROLEN1; ROLEN_ALIVE |
| AS24 | R A P | T | ASHE_MEDEUS |
| AS25 | K A P | T | ASHE_MEDEUS |
| AS26 | A L | T | ASHE_LOGS; LUC_ADMIT |
| AS27 | A S | T | ASHE_LOGS; DG_VALERICA |
| AS28 | X A | T | ASHE_Q1 |
| AS29 | A G | T | ASHE_OATH; after AS13 |
| AS30 | I A | T | ASHE_FANG |
| AS31 | A K P | T | ASHE_SUMMIT |
| AS32 | X A P | T | ASHE_EPI |
| AS33 | L A | T | ASHE_SUMMIT |
| AS34 | C A | T | ASHE_ORPHANS; after AS12 |
| AS35 | R A P | E LOC:Workshop | ASHE_Q1; after AS11 |
| AS36 | A R | T | ASHE_LOGS; after AS11 |
| AS37 | R A | T | ASHE_Q1; after AS11 |
| AS38 | R A | T | ASHE_LOGS; after AS36 |
| AS39 | A R | T | ASHE_REVEAL |
| AS40 | A L | T | ASHE_REVEAL; LUC_ADMIT |
| AS41 | V A | T | ASHE_REVEAL |
| AS42 | A K P | T | ASHE_REVEAL |
| AS43 | A X | T | ASHE_Q1 |
| AS44 | C A | T | ASHE_REVEAL; after AS12 |
| AS45 | A I | T | ASHE_REVEAL |
| AS46 | I A P | T | ASHE_REVEAL |
| AS47 | L A | T | ASHE_REVEAL |
| AS48 | G A | E CAMP | ASHE_REVEAL |
| AS49 | G A P | E INN | ASHE_REVEAL; after AS13 |
| AS50 | K A P | T | ASHE_HIRED |
| AS51 | A P | T | ASHE_REVEAL |
| AS52 | C A P | T | ASHE_REVEAL; after AS12 |
| AS53 | X A | E RAIN | ASHE_REVEAL |
| AS54 | A R | T | ASHE_REVEAL |
| AS55 | A L P | T | ASHE_REVEAL |
| AS56 | V A | T | VAL_FATHIS; after AS19 |
| AS57 | R A | E AFTERFIGHT:dwemer | ASHE_REVEAL |
| AS58 | G A | E AFTERFIGHT:Thalmor | ASHE_Q1 |
| AS59 | V A P | E AFTERFIGHT:bandit | ASHE_HIRED |
| AS60 | I A | E AFTERFIGHT:spider | ASHE_HIRED |
| AS61 | X A | E AFTERFIGHT:necromancer | ASHE_Q1; after AS43 |
| AS62 | C A | E AFTERFIGHT:forsworn | ASHE_HIRED |
| AS63 | A K P | E AFTERFIGHT (Kaidan below half health) | ASHE_HIRED |
| AS64 | A K P | T | K_CRUSH; A_CRUSH |
| AS65 | K A | T | K_ANY; A_CRUSH |
| AS66 | A K P | T | K_TOG+; A_CRUSH; after AS64 or AS65 |
| AS67 | K A | T | K_LOVE+; A_ANY |
| AS68 | G A P | T | G_FLIRT; A_CRUSH; ASHE_REVEAL |
| AS69 | A G | T | G_TOG+; A_ANY; after AS13 |
| AS70 | V A | T | V_FLIRT; A_CRUSH; after AS19 |
| AS71 | V A | E INN+NIGHT | V_ANY; A_ANY; after AS19 |
| AS72 | S A | E NIGHT (HOUSE or INN) | A_ANY; S_KISS; SER_VAMP; ASHE_REVEAL |
| AS73 | R A | T | A_CRUSH; ASHE_REVEAL |
| AS74 | A I | T | K_TOG+; A_CRUSH; ASHE_REVEAL |
| AS75 | A L | T | A_CRUSH |
| AS76 | A P | T | A_LOVE |
| AS77 | C A P | E CAMP | ASHE_REVEAL; after AS12 |
| AS78 | X A | E CAMP | ASHE_REVEAL |
| AS79 | L A P | T | ASHE_SUMMIT |
| AS80 | A P | T | ASHE_SUMMIT; after AS1 |

## Notes for the build
- Part 1 (AS1-AS10) must never play after the reveal; Part 2 callbacks (AS11, AS12, AS14, AS15, AS16) need their Part 1 partner talk first.
- The Lauet orphans: the boy is only ever "the Lauet boy". His first name is never spoken anywhere in the file, so he can't be confused with our Remi.
- Remi's interest in how Ashe works is always permission-first: AS11 (holds her questions back), AS35 (looks, touches nothing), AS36 (Ashe says yes, hands only), AS37 (changes Scrap for her), AS38 (a care kit). Keep that order. It sits fine alongside PY133/PY134 in 45 PARTY LIFE (the panel and the apology) in either order.
- Rolen branch: AS21 is branch-neutral; AS22 only if he died; AS23 only while he lives.
- Rival talks: Luna never flirts back or commits. In AS64 (Kaidan's crush) she misses the point completely.
- Topics avoided on purpose: everything in the Ashe and Serana patch, and every Ashe talk in files 20, 21, 22, 30-37, 43 and 45 (heart-rate logging, snow complaints with Xelzaz, Lunar Tears garden, bow lessons with Inigo, Remi and her pipes, chores, the bench, the Pa Lauet bait talk with Kaidan, Brotherhood faces).
- No "Dragonborn" anywhere in the file.
