# 49b ASHE 2 - trigger rows (prefix AS, continues AS81-AS180, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\49b ASHE 2.txt`.
Sources: `research\bibles\ashe.md` (sections 1, 3, 6), the partner bibles, `TRIGGERS.md` sections 2-4, `triggers\20 DAWNGUARD.md` and `triggers\49 ASHE.md` (part 1 codes, Ashe silence list and events, reused unchanged).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`), the **Ashe silence** list in `49 ASHE.md`, and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check).
Type: T = timer, E = event (fires on the moment).

Every AS talk also needs `ASHE_HIRED` and Ashe Free (row in `48 SERANA.md` / `20 DAWNGUARD.md`), even where the row only lists a later gate. Talks with Serana also need `SERANA` and Serana Free.

## Gate codes used in this file

Reused (TRIGGERS.md section 4, 20 DAWNGUARD.md section 3, 49 ASHE.md, 48b SERANA 2.md): `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_LOGS`, `ASHE_SUMMIT`, `ASHE_EPI`, `A_CRUSH`, `A_LOVE`, `A_ANY`, `SERANA`, `SER_VAMP`, `S_COMP`, `K_CRUSH`, `K_TOG+`, `V_FLIRT`, `ANYROM`, `BRYNJAR`, `VAL_FATHIS`, `LUC_ADMIT`.

New here (Ashe - Fire and Blood.esp; FormIDs from ashe.md section 3):
- `A_WARM` = `MM_RM` (2F3039) >= 2 and < 4, and `MM_AsheRomance` (A5E1EF) == 0. Her first warm steps (playful goodbyes).
- `A_HIGH` = `MM_RM` >= 7 and `MM_AsheRomance` == 0 (her "right beside you, always" range, not together).
- `A_CONFESSED` = `MM_AMQ_07Confession` (E67C22) == 1: she began her confession on the mountain. **[UNC: confirm the global is set for both the full and the backed-off ("never mind") version; if only the full one, the row still works]**
- `A_FRIENDEND` = `ASHE_EPI` and `MM_AsheRomance == 0` (the home talk ended in friendship).
- `ONCE_A_YEAR` (AS115) = fires on the first CAMP after each 365-day mark of GameDaysPassed counted from `ASHE_Q1`. The mod has no death date; this gives it one quiet day a year. **[UNC: needs the controller to store the ASHE_Q1 day]**

Events (TRIGGERS.md section 4, 48/49 files unless noted):
- `E CAMP`, `E CAMP+NIGHT`, `E INN`, `E INN or HOUSE`, `E MORNING`, `E RAIN`, `E CLEARNIGHT`, `E WILD`, `E CITY`, `E CITY:Solitude`, `E CRYPT`, `E DWEMER`, `E WATER`.
- `E PALACE or TEMPLE` = interior with LocTypeCastle, LocTypeJarlsHouse or LocTypeTemple.
- `E CARAVAN` = a Khajiit caravan leader (Ri'saad, Ma'dran or Ahkari) within 2000 units. **[UNC]**
- `E LOC:College` = in the College of Winterhold (any interior of WinterholdCollegeLocation).
- `E BOUNTY_PAID:Whiterun` = player's Whiterun hold crime gold goes from > 0 to 0. **[UNC: controller polls the crime faction]**
- `E AFTERFIGHT:<type>`: `dwemer`, `brotherhood` (DarkBrotherhoodFaction), `spriggan` (SprigganRace family), `lightningmage` (an enemy cast a Shock-school spell during the fight **[UNC]**). `AFTERFIGHT (<who> hurt)` = that follower's health dropped below 60% during the fight (Ashe below 50% for AS180). **[UNC: controller must track health during combat]**

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| AS81 | A P | E INN or HOUSE | ASHE_SUMMIT |
| AS82 | G A P | T | ASHE_REVEAL |
| AS83 | V A | E CITY | ASHE_REVEAL; after AS19 |
| AS84 | I A | T | ASHE_LOGS |
| AS85 | L A | E PALACE or TEMPLE | ASHE_REVEAL |
| AS86 | A K | E INN | ASHE_REVEAL |
| AS87 | R A P | E WILD | ASHE_REVEAL |
| AS88 | X A | E CAMP | ASHE_REVEAL |
| AS89 | A P | E CAMP+NIGHT | ASHE_LOGS |
| AS90 | A S | T | ASHE_REVEAL |
| AS91 | G A P | E BOUNTY_PAID:Whiterun | ASHE_REVEAL |
| AS92 | A K P | T | ASHE_REVEAL; after AS50 |
| AS93 | I A | E CAMP | ASHE_REVEAL |
| AS94 | A L | T | LUC_ADMIT; ASHE_REVEAL |
| AS95 | V A | T | after AS83 |
| AS96 | R A P | E INN | ASHE_REVEAL |
| AS97 | K A | T | ASHE_REVEAL |
| AS98 | A P | T | ASHE_Q1; after AS18 and AS97 |
| AS99 | G A | E AFTERFIGHT | ASHE_REVEAL |
| AS100 | L A P | T | ASHE_REVEAL |
| AS101 | S A | T | ASHE_REVEAL |
| AS102 | V A P | T | ASHE_REVEAL; after AS19 |
| AS103 | I A | E CAMP+NIGHT | ASHE_REVEAL |
| AS104 | X A | T | ASHE_REVEAL |
| AS105 | C A | T | after AS12 |
| AS106 | R A | T | ASHE_REVEAL; after AS101 |
| AS107 | A K | T | ASHE_Q1 |
| AS108 | L A P | T | ASHE_Q1 |
| AS109 | A P | T | ASHE_LOGS |
| AS110 | X A | T | ASHE_Q1 |
| AS111 | G A | E CAMP | ASHE_Q1; after AS13 |
| AS112 | V A | T | ASHE_LOGS; after AS19 |
| AS113 | I A | T | ASHE_REVEAL |
| AS114 | A R | T | ASHE_LOGS; after AS36 |
| AS115 | A P | E CAMP | ASHE_Q1; ONCE_A_YEAR |
| AS116 | C A | T | ASHE_Q1; after AS12 |
| AS117 | L A P | T | after AS17 |
| AS118 | A K | T | after AS25; BRYNJAR |
| AS119 | V A | T | ASHE_REVEAL; after AS19 |
| AS120 | G A P | E INN | ASHE_REVEAL |
| AS121 | A K | T | ASHE_REVEAL |
| AS122 | I A | E CARAVAN | ASHE_REVEAL |
| AS123 | A P | T | ASHE_REVEAL; after PR311 (Val braids her hair) |
| AS124 | X A | T | ASHE_REVEAL |
| AS125 | L A | T | ASHE_REVEAL |
| AS126 | R A | E CAMP+NIGHT | ASHE_REVEAL |
| AS127 | G A P | E CAMP | after AS13 |
| AS128 | S A | T | ASHE_REVEAL |
| AS129 | K A P | E CAMP | ASHE_REVEAL |
| AS130 | G A P | E INN | ASHE_REVEAL |
| AS131 | V A | T | after AS41 |
| AS132 | X A | T | ASHE_REVEAL |
| AS133 | I A | E CLEARNIGHT | ASHE_REVEAL |
| AS134 | L A | E DWEMER | ASHE_LOGS |
| AS135 | A S | E CAMP+NIGHT | ASHE_REVEAL |
| AS136 | K A | E RAIN | ASHE_REVEAL; after DG3 |
| AS137 | G A | E CAMP+NIGHT | ASHE_REVEAL |
| AS138 | V A | T | VAL_FATHIS; ASHE_LOGS; after AS19 |
| AS139 | X A | E CAMP | after AS16 |
| AS140 | L A P | E CRYPT | ASHE_SUMMIT |
| AS141 | I A P | E CITY:Solitude | after AS46 |
| AS142 | S A | T | SER_VAMP; ASHE_REVEAL |
| AS143 | G A | E INN | after AS13 |
| AS144 | X A P | E CAMP | ASHE_REVEAL |
| AS145 | R A | T | after AS38 |
| AS146 | A G R | E AFTERFIGHT (Gore hurt) | after AS38 |
| AS147 | A K | T | after AS38 |
| AS148 | R A | T | after AS38 |
| AS149 | A R P | T | after AS38 |
| AS150 | A R | T | after AS145 |
| AS151 | L A | T | after AS38 |
| AS152 | R A | E WATER | after AS38 |
| AS153 | C A P | E CAMP | after AS12 |
| AS154 | C A | E CAMP+NIGHT | after AS12 |
| AS155 | C A P | E CITY | after AS12 |
| AS156 | C A | E CAMP | after AS12 |
| AS157 | C A P | E RAIN | after AS12 |
| AS158 | C A | E AFTERFIGHT (Ashe hurt) | after AS12 |
| AS159 | C A | E LOC:College | after AS12 |
| AS160 | C A P | T | after AS12 |
| AS161 | A P | T | A_WARM; ASHE_REVEAL |
| AS162 | R A | E MORNING | A_WARM |
| AS163 | A K P | T | K_CRUSH; A_CRUSH; after AS108 |
| AS164 | A S | T | A_CRUSH; S_COMP; ASHE_REVEAL |
| AS165 | V A | T | V_FLIRT; A_CRUSH; after AS19 |
| AS166 | I A | T | A_CRUSH; ANYROM |
| AS167 | X A | T | A_CRUSH; ASHE_REVEAL |
| AS168 | L A | T | A_CRUSH; after SE69 |
| AS169 | A P | T | A_HIGH |
| AS170 | A S | T | ASHE_SUMMIT; A_CONFESSED; S_COMP |
| AS171 | R A | T | A_LOVE |
| AS172 | A P | E CAMP+NIGHT | A_LOVE |
| AS173 | A I | T | K_TOG+; MM_RM >= 4; after AS74, AS38, AS83, AS88 and AS156 |
| AS174 | A P | T | A_FRIENDEND |
| AS175 | C A | E AFTERFIGHT:dwemer | after AS12 |
| AS176 | A K P | E AFTERFIGHT + RAIN | ASHE_REVEAL |
| AS177 | G A | E AFTERFIGHT:brotherhood | ASHE_Q1 |
| AS178 | V A P | E AFTERFIGHT:lightningmage | ASHE_Q1 |
| AS179 | X A | E AFTERFIGHT:spriggan | ASHE_REVEAL |
| AS180 | I A | E AFTERFIGHT (Ashe hurt) | ASHE_REVEAL |

## Notes for the build
- Nothing in this file plays before `ASHE_REVEAL` except talks whose gate says otherwise (none do): every talk talks about what she is, so the reveal gate is the floor.
- Part 6 (Remi's kit, AS145-AS152) needs AS38 "Somebody Packed" first; AS150 needs AS145. Items mentioned are the ones from AS38 (blue coolant flask, the little oil, the cloth that doesn't shed, the tiniest file) plus the wrapping string.
- Part 7 (Redcap, AS153-AS160) needs AS12, where "Shiny. Fa-ka." becomes a friendly name. AS155 sets the rule that only Redcap may call her that. AS159 mentions Anise (Redcap's witch); no extra gate needed.
- Part 8 rivalry steps: A_WARM (AS161-162) -> A_CRUSH (AS163-168) -> A_HIGH (AS169) -> A_CONFESSED (AS170) -> A_LOVE (AS171-172); AS173 is the "Kaidan won" follow-up to AS74; AS174 is the friendship ending. Luna never flirts back or commits. In AS163 (Kaidan's crush) she misses the point completely (thinks it is a Saturalia present).
- AS118 mentions Brynjar, so it carries `BRYNJAR`. No Kaidan cult content anywhere.
- The Lauet boy is never mentioned in this file.
- No "Dragonborn" anywhere in the file.
- Topics avoided on purpose: everything in 49 ASHE and the Ashe talks in files 14b-57 (heart-rate logging, snow complaints, Lunar Tears, bows, the bench, horses, the clock story, the crater, the eaten book, Pa Lauet, whistling, the boat, the arm-wrestle, the audits and ratings in fights).
