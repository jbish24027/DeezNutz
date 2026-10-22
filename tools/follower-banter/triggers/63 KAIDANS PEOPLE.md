# 63 KAIDANS PEOPLE - trigger rows (prefix KP, KP1-KP60, 60 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\63 KAIDANS PEOPLE.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4 and 8, `research\bibles\kaidan.md` (Erik = childhood friend from Rorikstead; Farkas best mate; Vilkas sparring partner; Aela teases him; KaiComp), `research\triggers\kaidan_block.md` (1 KaiComp and KaiHoneymoon rows, 2a, 2b items 6 and 8, 4 Jorrvaskr/Vargr Den), `research\triggers\vanilla_gates.md` (B1, B3), `triggers\34 COMPANIONS.md` (sections 1-3: Companions silence, KaiComp blocks A-D, `LOC:Jorrvaskr`, C_ codes), `triggers\34b COMPANIONS 2.md`, `triggers\37 VANILLA SIDE QUESTS AND HOLDS.md` (SQ34 Erik flag), `triggers\40 PLACES AND LANDMARKS.md` (PL4, `RoriksteadLocation 018A47`), `triggers\57 INNS AND TOWN LIFE.md` (`INN:Frostfruit`), `triggers\41 FAMOUS NPCS.md` (NP41).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event.

## 1. Kaidan's own content: what this file must never touch

- **Every KP row with K** carries 34 COMPANIONS.md section 2A (KaiComp 162E4A:IF not running, or stage < 30, or >= 150; plus KaiSTFUQuest not running and STFUVarNPCGeneral == 0) and section 2B (no K+P talk while KaiComp is 10..29: KP1, KP4, KP16, KP17, KP21, KP22, KP23, KP25, KP26, KP28, KP57, KP59).
- **Every KP row, with or without K**, carries 34 COMPANIONS.md section 2C (no KP talk in Vargr Den; no KP talk in `LOC:Jorrvaskr` while KaiComp is 140..149) and section 1 (the Companions silence list and the five KaiComp climax scenes).
- **Honeymoon:** no KP talk while `KaiHoneymoon (A5EA55:IF)` is running at stage 20..149 (kaidan_block.md 1 and 2b item 6). Farkas and Vilkas escort the player in that window; their scenes belong to his mod.
- **IF's travelling banter with them:** no KP talk while Farkas, Vilkas, Aela or Erik is a current follower of the player (`NO_PEOPLE_FOLLOWING` below). Kaidan's IF has its own "frathouse" and Erik travel scenes (kaidan_block.md 5D) for that.
- **Content rule:** nothing names or hints at anything in KaiComp (his trial, Wulf, the den, the hammer, the scholar or book, the sword he's given in Jorrvaskr, "my Harbinger and my love"). Kaidan is a Companion only in KP42, in general terms only (Tilma moves his blanket). IF's frathouse topics are left alone: cards and bluffing, spiders, sweet-roll theft, sparring and footwork, limericks, Farkas's crush and flirting advice, the ca-caw signal, the archery contest, wedding toasts.
- Farkas, Vilkas, Aela and Erik never speak here. They are only talked about.

## 2. Gate codes

Reused: `K_CRUSH`, `K_TOG+`, `BRYNJAR`, `HELGEN` (TRIGGERS.md section 4); `C_JOIN`, `KODLAK_DEAD`, `HARBINGER`, `LOC:Jorrvaskr`, `KCOMP_DONE` (34 COMPANIONS.md); `SERANA`, `SER_VAMP`, `ASHE_HIRED`, `ASHE_REVEAL` (20 DAWNGUARD.md); `CITY:Whiterun` (TRIGGERS.md); `INN:Frostfruit` (57 INNS AND TOWN LIFE.md); pair codes `KI`, `LK`, `RX` (11 LEGACY OF THE DRAGONBORN.md / 53b RIVALRY 2.md).

New here:
- `FARKAS_OK`, `VILKAS_OK`, `AELA_OK`, `ERIK_OK` = that NPC is alive (`GetDead == 0` on the unique actor). **[UNC: look up the Skyrim.esm FormIDs of Farkas, Vilkas, Aela the Huntress and Erik at build]**. A talk that names one of them carries their code.
- `NO_PEOPLE_FOLLOWING` = none of Farkas, Vilkas, Aela or Erik is in `CurrentFollowerFaction` right now. **On every KP row.**
- `KODLAK_ALIVE` = NOT `KODLAK_DEAD` (KP25 only).
- `SKJOR_ALIVE` = C03 (01CEF4:Skyrim.esm) not completed **[UNC: Skjor dies at Gallows Rock at the end of C03; if C03's end stage differs, use "Skjor GetDead == 0"]** (KP12 only).
- `POST_FUNERAL_ANY` = `GetStageDone C06 (01CEF6:Skyrim.esm) 10 == 1` (Kodlak's funeral has happened). KP40 also carries the C06 30..199 silence.
- `NOT_KCOMP` = NOT `KCOMP_DONE` (Kaidan is not a Companion yet: KP5, KP6).
- `JORR_FIRST_K` = event: the first time the player enters `LOC:Jorrvaskr` while Kaidan is following (controller flag). **[UNC: whether IF plays any arrival scene of its own there outside KaiComp; KaiCompJorrvaskr only kicks during KaiComp, kaidan_block.md 1]**
- `LEAVE:Whiterun` = event: the player leaves WhiterunLocation for the hold exterior, having been in `LOC:Jorrvaskr` during this visit (controller flag). **[UNC: OnLocationChange proxy]**
- `HOLD:Whiterun` = exterior in Whiterun Hold, not in a settlement, within ~8000 units of Whiterun's gate and not yet having entered Whiterun this day. **[UNC proxy]**
- `LOC:Rorikstead` = `RoriksteadLocation 018A47:Skyrim.esm` (40 PLACES AND LANDMARKS.md).
- `ERIK_SLAYER` = Erik has his father's blessing to go adventuring, the same flag as SQ34's row in 37 VANILLA SIDE QUESTS AND HOLDS.md **[UNC there: Erik in PotentialFollowerFaction / Mralki persuaded flag]**.
- `after PL4` = "Erik the Little" has played (the party knows who Erik is). `after SQ34`, `after NP41` = those talks have played.
- `after:KPn` = that KP talk already played. Chains obey TRIGGERS.md section 8.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| KP1 | P K | E JORR_FIRST_K | FARKAS_OK |
| KP2 | G K | E LOC:Jorrvaskr | FARKAS_OK; after A1 |
| KP3 | V K | E LOC:Jorrvaskr | VILKAS_OK; after A2 |
| KP4 | P K | E LOC:Jorrvaskr or CITY:Whiterun | K_CRUSH; AELA_OK |
| KP5 | R K | E LOC:Jorrvaskr | NOT_KCOMP; FARKAS_OK; after B1 |
| KP6 | I K | E LOC:Jorrvaskr | NOT_KCOMP; KI |
| KP7 | K P G | E LOC:Jorrvaskr | VILKAS_OK; after A1 |
| KP8 | V G | E LOC:Jorrvaskr | AELA_OK; after A3 |
| KP9 | C K | E LOC:Jorrvaskr | FARKAS_OK; after R1 |
| KP10 | X P | E LOC:Jorrvaskr | VILKAS_OK |
| KP11 | K L | E LOC:Jorrvaskr | FARKAS_OK; VILKAS_OK; LK |
| KP12 | A R | E LOC:Jorrvaskr | AELA_OK; SKJOR_ALIVE; ASHE_HIRED |
| KP13 | G P | E LOC:Jorrvaskr or CITY:Whiterun | AELA_OK |
| KP14 | V I | E LOC:Jorrvaskr | FARKAS_OK; after I1 |
| KP15 | G K | E LOC:Jorrvaskr | FARKAS_OK; VILKAS_OK; after A1; after A2 |
| KP16 | K P | E LOC:Jorrvaskr or CITY:Whiterun | K_CRUSH; AELA_OK |
| KP17 | P K | T | FARKAS_OK |
| KP18 | I K | T | KI; FARKAS_OK; VILKAS_OK |
| KP19 | G K | T | AELA_OK; after A1 |
| KP20 | V K | T | VILKAS_OK; after A2 |
| KP21 | P K | E LEAVE:Whiterun | K_CRUSH; FARKAS_OK |
| KP22 | P K G | E HOLD:Whiterun | FARKAS_OK; VILKAS_OK; after A1 |
| KP23 | P K | E LEAVE:Whiterun | FARKAS_OK; VILKAS_OK |
| KP24 | R K | E LOC:Jorrvaskr or T | FARKAS_OK; VILKAS_OK; after B1 |
| KP25 | P K | E LOC:Jorrvaskr | C_JOIN; KODLAK_ALIVE |
| KP26 | K P | E LOC:Jorrvaskr | VILKAS_OK |
| KP27 | R K | E CAVE or DWEMER or CRYPT | ERIK_OK; after PL4; after B1 |
| KP28 | P K | E LOC:Rorikstead | BRYNJAR; after PL4 |
| KP29 | X K | E INN:Frostfruit | after PL4; after C3 |
| KP30 | R P | E LOC:Rorikstead | ERIK_OK; after PL4 |
| KP31 | G K | E LOC:Rorikstead | after:KP30; after A1 |
| KP32 | V K | E LOC:Rorikstead | ERIK_OK; after PL4; after A2 |
| KP33 | R P | E LOC:Rorikstead | HELGEN; ERIK_OK; after PL4 |
| KP34 | K G | E LOC:Rorikstead | ERIK_SLAYER; ERIK_OK; after SQ34 |
| KP35 | G K | T | ERIK_SLAYER; ERIK_OK; after SQ34; FARKAS_OK; VILKAS_OK; AELA_OK |
| KP36 | C K | E LOC:Rorikstead | ERIK_OK; after PL4; after R1 |
| KP37 | L P | T | K_CRUSH; after:KP31; after:KP6 |
| KP38 | G K | E LOC:Jorrvaskr | C_JOIN; FARKAS_OK; VILKAS_OK |
| KP39 | P V | E LOC:Jorrvaskr | C_JOIN; VILKAS_OK |
| KP40 | G K | T | POST_FUNERAL_ANY; FARKAS_OK |
| KP41 | V K | T | HARBINGER; VILKAS_OK |
| KP42 | X K | E LOC:Jorrvaskr | KCOMP_DONE; after:KP6 |
| KP43 | G P | E LOC:Jorrvaskr | FARKAS_OK |
| KP44 | A K | E LOC:Jorrvaskr | ASHE_REVEAL; FARKAS_OK |
| KP45 | I K | E LOC:Jorrvaskr | KI; FARKAS_OK |
| KP46 | G K | E LOC:Jorrvaskr | K_CRUSH; AELA_OK; after A1 |
| KP47 | G K | E LOC:Jorrvaskr | K_TOG+; AELA_OK; after A1 |
| KP48 | X R | E LOC:Jorrvaskr | VILKAS_OK; RX |
| KP49 | L G | E LOC:Jorrvaskr | AELA_OK; after L1 |
| KP50 | C P | E LOC:Jorrvaskr or CITY:Whiterun | AELA_OK |
| KP51 | G V | E LOC:Jorrvaskr | FARKAS_OK; after A3 |
| KP52 | S K | E LOC:Jorrvaskr or CITY:Whiterun | SERANA; SER_VAMP; AELA_OK |
| KP53 | R K | E LOC:Jorrvaskr | VILKAS_OK; after B1 |
| KP54 | G P | T | AELA_OK; after NP41 |
| KP55 | I P | E LOC:Jorrvaskr | Kaidan following and in the same cell (not a speaker; he must still pass Kaidan's 2a blocks so he isn't in one of his own scenes) |
| KP56 | V K | E LEAVE:Whiterun | K_TOG+; VILKAS_OK; after A2 |
| KP57 | K P | E CITY:Whiterun | K_TOG+; FARKAS_OK; VILKAS_OK; AELA_OK; ERIK_OK |
| KP58 | R I | T | after:KP6; after:KP31; after B6 |
| KP59 | P K G | E LEAVE:Whiterun | FARKAS_OK; VILKAS_OK; after A1 |
| KP60 | G I | T | after:KP58; after C2 |

## 4. Notes for the build
- Every KP row also carries `NO_PEOPLE_FOLLOWING` and the honeymoon block from section 1.
- Nothing reveals the Circle's secret before `C_PROVEN`: no KP line mentions wolves or the beast blood.
- Kodlak is mentioned alive only in KP5 (past tense, any time) and KP25 (`KODLAK_ALIVE`). Skjor only in KP12 (`SKJOR_ALIVE`) and KP19 (an old bet, past tense).
- Light inventions, flagged for the user: how Kaidan and Farkas met (a broken table at the Bannered Mare, KP17); Tilma's stitched bench blanket (KP6, KP42); Vilkas's gloves (KP20); the six-year book loan (KP26); Farkas's lunch note that Vilkas writes down (KP23, consistent with 54 FL "Farkas cannot read" and the PY365 reply letter); Brynjar leaving Kaidan with Mralki for a winter (KP28, `BRYNJAR`, kept vague as "a job past the border" so it doesn't clash with his year in the Reach); the old sheep Lady Horker (KP30, KP31). None touches a quest record or an IF scene.
- Avoided on purpose (already written): Erik's dad and the first round (MN65), Erik the Slayer and his mudcrabs (SQ34), fence-post swords (PL4), Erik's battle cry (PL5), the scarecrow legend (PY294), "we don't talk about Rorikstead" (PY119-122), Dear Farkas and the reply (PY365 and after), the arm-wrestle rematch (TV180), the frog in the boot (WE121), Vilkas's footwork (WE122), the love letters across the plains (54), Shield-Kaidan (CP5, CP58), Aela teaching Gore the bow (NP41, only continued in KP54), Vilkas reading (NP42), Farkas helping Lucien up (NP43), Ashe sparring Vilkas (NP142).
- Luna speaks in 23 of 60 talks (38%). Nobody says "Dragonborn".
