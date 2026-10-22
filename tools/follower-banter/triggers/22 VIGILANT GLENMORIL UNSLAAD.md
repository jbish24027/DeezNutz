# Triggers - 22 VIGILANT GLENMORIL UNSLAAD (VG1-VG190)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\22 VIGILANT GLENMORIL UNSLAAD.txt`
Research: `research\content\vigilant_glenmoril_unslaad.md` (+ `_detail\`). Section numbers below (A3, B3, C3, D5, D6) point there.
Format as TRIGGERS.md section 5. Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, **SE Serana, AS Ashe**. Luna (player voice) is not listed; she needs no Free() check.
All FormIDs are `<id>:Vigilant.esm`, `:Glenmoril.esm` or `:Unslaad.esm` by the quest's own prefix (zzzAoM/BM/CO/CH = Vigilant, zzzLrh/GH/LaM/Rev = Glenmoril, zzzCrb = Unslaad) unless another plugin is written. "done N" = `GetStageDone(quest, N) == 1`. "stage a..b" = `GetStage` in that range while running.

## 1. Gate codes local to this file

### Start / story
- `VG_ON` = zzzAoMMq00 005CE2 stage >= 5 (Delayed Start already needs level 25 + zDcdMq05 00CA1E:DAc0da.esm completed)
- `VG_JOINED` = zzzAoMMq00 done 10 (or 9999) · `VG_TEMPLE` = zzzAoMMq00 done 40 (or 9999)
- `OWL_OFFER` = zzzAoMqOwl 4419E5 done 5 or 7, not done 20, zzzAoMMq00 stage < 15
- `KEEPER` = zzzAoMMq10 011B75 done 39 OR zzzAoMMqGoodEnd 4D0376 done 120
- `CH_BACK` = zzzCHMQ01 1363DB done 70 OR done 180, player GetInWorldspace Tamriel (or a Tamriel child world), and every speaker is near the player again. "first time ... after CH_BACK" = once per speaker set.
- `CH_GOOD` = zzzCHMQ01 done 70 · `CH_BAD` = zzzCHMQ01 done 180
- `MARTYR` = zzzCOMq01 065932 done 200. **From that stage on, block every talk in this file** (the player is a new character; Luna's voice and history no longer apply). No martyr talks were written.
- `GL_ON` = zzzLrhBypass 012EAD done 10 (Delayed Start: level 40, change-location)
- `UN_ON` = zzzCrbMq01 01D8FF done 10 (doll touched). Stage 0 only enables the doll.
- `DB`, `ALDUIN`, `RC_WEREPIG`, `VAL_FATHER`, `VAL_FATHIS`, `GORE_FATHER`, `K_*`, `G_FLIRT`, `G_TOG+`, `V_FLIRT`, `V_TOG+`: as TRIGGERS.md section 4.

### Gore - Vigilant.esp (research D2, D5, D6). Globals are `:Gore - Vigilant.esp` unless marked.
- `G_OK` (Gore may speak) = HD1MainBoxed 0316BA == 0 AND HD1GoreRef 00B4B1:GORE.esp not disabled AND HD1MBR 183378 != 3 AND HD1VAct2Var 251CCC not 3/4 AND HD1WTCHVar 02AE4E != 2 AND GetQuestRunning HD1MemoriesQ 0C6188 == 0 AND Gore not in cell HD1GorsePrison 43DD6A:GORE.esp AND Gore IsInScene == 0. Applies to **every** talk with G in it, in all three parts.
- `G_PRE` (before his rescue: Molag Bal = fear) = HD1VAct3 052081 == 0
- `G_GONE` (vanished in the mansion) = HD1VAct3 == 1 AND HD1MainBoxed == 1 AND player not in Coldharbour. **No Gore lines**; others may notice.
- `G_BACK` (rescued) = HD1VAct3 == 1 AND HD1MainBoxed == 0 AND HD1MemoriesRestored 0AF3FA >= 3 AND CH_BACK AND HD1GoreRef enabled AND GameDaysPassed >= (day CH_BACK became true) + 2. [unconfirmed: no "his own ending talk was had" flag exists, so the 2-day wait lets HD1EndingVig / the "Are you okay?" talk (HD1WTCHVar == 2) land first; also require HD1WTCHVar != 2]
- `G_LOST` (lost to Coldharbour) = CH_BACK AND HD1MemoriesRestored < 3 AND HD1GoreRef IsDisabled AND not MARTYR
- Never fire any talk in the collision places of research D6: Windpeak Inn after zzzAoMMq00 10, the Stuhn Ravine entrance trigger, Candlehearth Hall at zzzAoMMq03 20, the Altar of Molag Bal / Beacon Underground 038521 after Old Regrets, Witch's Pond 166857 during zzzAoMMq08, the Altano chase (zzzAoMMq09 running), the Temple entrance while zzzBMMq01 is at 10, every Blood Matron dungeon cell (Windhelm Dungeon, Hidden Passage, Old Windhelm Slums/City, Bloody Well, Asylum, Enchantress' Palace 033B80, Matron's Chamber 034E12), Witch Island, cell COBruiantEntrance 047CFD, Coldharbour, the ending.

### Serana / Ashe (from serana.md, ashe.md)
- `SE_F` = GetVMQuestVariable DLC1NPCMentalModel 002B6E:Dawnguard.esm ::IsFollowing_var == 1 AND DLC1VQ02 002F65 completed AND SDA_PlayerInDialogue 9EB814:SeranaDialogAddon.esp == 0. Required on every SE talk even where not repeated.
- `SE_VAMP` = Serana HasKeyword Vampire 0A82BB == 1 (talks where she speaks as a living vampire)
- `AS` speaker always needs MM_AsheMentalModel 06FE28:Ashe - Fire and Blood.esp ::IsFollowing_var == 1, bConfigVarIdles == 1, IsWaiting == 0, MM_PlayerinDialogue 5435E9 == 0, MM_FlashbackRunning 4643DC == 0, and no MM_AMQ_* quest running in its own location.
- `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_ROLEN1`: as ashe.md section 6.

## 2. Silence this file adds to WorldQuiet()
- VIGILANT (research A3): player in Coldharbour 06D275 (location 06D7EA), Lamae's Dream 035457, Jealousy 0619A2, White Wasteland, Elder Field, Arena, Old Forest, Whale Graveyard; memory cells / Memory location 26C06B; Jo'vanni's Dream Theater cell 00185C; Dark Tunnel 4419CE; Aetherius 1353E4/136194; Abyss 064F28. Stage windows: Mq06 30..59, Mq07 30..40, Mq08 20..30 and 220..230, Mq09 running, Mq10 0..30, GoodEnd 0..30 and 50..70, both Owl quests 20..40, BMMq03 20..100 and 200..220, COMq01 60..90, COSubQ01 0..20, any CHMQ00/01/02 or CHMemoryQuest01-13 running, CHqSAExile 0..10 and 999, AoMSubQ02 100..130, AoMSubQ03 5..10.
- GLENMORIL (research B3 + detail files): Quagmire 00FDFA, Dreamsleeve 491B1A, Milky Sea 0109CC, Svartibrunnr 000D62 while zzzRevMq00 not done 30, Sanctuary of Namira 009598 during zzzGHMq01 90..130; the dream cells of B3-B (Old Well 007A50 always); every game-over window (LrhMq01 500+, LrhMq03 200+, LrhMq05 500..520, GHMq01 255+, Ithelia Call 01/02 and zzzGHEndingOwl running); the cutscene table of B3-C; while the player is in any scene (the mod's scene-skip system jumps stages, so the talks key on the stage after).
- UNSLAAD (research C3): Joy-Snow Sky 3F7859, Frozen Abyss 42AF9C and the Atmora interiors; the stage table of C3-B; Boss Rush 18F113 running; any VS boss quest running; Owl Flies at Dusk 30..40 (hard gate) and >= 600 (bad end).

## 3. Per-talk table


### PART 1 - VIGILANT  (80 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| VG1 | K | T | VG_JOINED; not in Stuhn Ravine 023E7E; not Windpeak Inn (Gore scene) |
| VG2 | V R | T | VG_TEMPLE |
| VG3 | L X | T | VG_TEMPLE |
| VG4 | R L | T | VG_TEMPLE |
| VG5 | I K | T | OWL_OFFER; not in Windpeak Inn |
| VG6 | G C | E CAMP in Stuhn Ravine 023E7E | VG_TEMPLE; G_OK; not in Stuhn entrance trigger area (Gore STUHN scene) |
| VG7 | G K | T | VG_TEMPLE; G_OK; G_PRE |
| VG8 | AS K | T | VG_JOINED; ASHE_ROLEN1 |
| VG9 | AS L | T | VG_JOINED; ASHE_REVEAL |
| VG10 | R V | T | VG_JOINED; Gore recruited at least once (HD1GoreRecruited 00B4B8:GORE.esp == 1); G_PRE |
| VG11 | G V | T | VG_JOINED; G_FLIRT or G_TOG+; G_OK |
| VG12 | V C | T | zzzAoMMq01 005CE3 stage 20..39 |
| VG13 | SE K | T | zzzAoMMq01 done 50; SE_F; SE_VAMP |
| VG14 | L I | T | zzzAoMMq02 006271 done 30 |
| VG15 | G X | T | zzzAoMMq03 00627F done 40; G_OK; not in Candlehearth Hall |
| VG16 | K L | T | zzzAoMMq04 0082EA done 50 |
| VG17 | X R | T | zzzAoMMq04 stage 38 or 39 done |
| VG18 | V R | T | zzzAoMMq05 0098C9 stage 30..49 |
| VG19 | G I | T | zzzAoMMq05 done 60; zzzAoMMq07 00A3FE not done 80; G_OK |
| VG20 | I K | T | zzzAoMMq06 009E68 done 90 or 999 |
| VG21 | R V | T | zzzAoMMq06 done 90 or 999; HD1CatDream 19D4FD:Gore - Vigilant.esp == 1; Gore not boxed |
| VG22 | SE I | T | zzzAoMMq06 done 60; SE_F |
| VG23 | V K | T | zzzAoMMq07 00A3FE done 80; VAL_FATHIS |
| VG24 | L X | T | zzzAoMMq07 done 80 |
| VG25 | X R | T | zzzAoMMq07 done 80; HD1MBR 183378:Gore - Vigilant.esp >= 1 and != 3; G_PRE; not in Beacon Underground 038521 |
| VG26 | SE K | T | HD1MBR >= 1 and != 3; G_PRE; SE_F; not in Beacon Underground |
| VG27 | I R | T | HD1MBVisions 1F9BDF:Gore - Vigilant.esp >= 1; G_PRE; Gore following |
| VG28 | K R | T | HD1MBR == 3; Gore not following |
| VG29 | V G | T | zzzAoMMq08 00EA8A stage 0..19; G_OK; not in Witch's Pond 166857 |
| VG30 | K SE | T | zzzAoMMq08 done 20 and not done 230; zzzAoMMq09 00EFF7 not running; SE_F |
| VG31 | R L | T | zzzAoMMq08 done 230; zzzAoMMq09 not running |
| VG32 | C L | T | zzzAoMMq09 done 50; not in Temple of Stendarr (wait for Mq10 40) |
| VG33 | K I | T | zzzAoMMq10 011B75 done 40 |
| VG34 | SE X | T | zzzAoMMq10 done 40; SE_F |
| VG35 | K G | T | zzzAoMMq10 done 40; K_ANY; G_OK; G_PRE |
| VG36 | V C | T | zzzAoMMqGoodEnd 4D0376 done 120 |
| VG37 | G K | T | KEEPER; G_OK; not at the Temple entrance (Gore recap scene) |
| VG38 | R L | T | KEEPER |
| VG39 | C X | T | zzzAoMSubQ01 17576E stage >= 10; not at Witch Island (Gore Reyda scene) |
| VG40 | V I | T | zzzBMMq01 038524 stage 20..59; not in Windhelm Dungeon or the Blood Matron cells (Gore scenes) |
| VG41 | R K | T | zzzBMMq01 stage 30..59; not in Windhelm Dungeon cells |
| VG42 | L X | T | zzzBMMq01 stage 50..99 |
| VG43 | SE R | T | zzzBMMq02 038525 done 100; SE_F; SE_VAMP; not in Blood Matron cells |
| VG44 | SE L | T | zzzBMMq03 038526 done 100; SE_F |
| VG45 | K V | T | zzzBMMq03 done 100; K_CRUSH |
| VG46 | AS V | T | zzzBMMq03 done 100; V_FLIRT or V_TOG+; ASHE_REVEAL |
| VG47 | C I | T | zzzBMMq03 done 100 |
| VG48 | L V | T | zzzCOMq01 065932 stage 20..29; not in cell COBruiantEntrance 047CFD (Gore scene) |
| VG49 | I C | E arrival in Bruiant Estate 047CFA | zzzCOMq01 stage 20..30; not in COBruiantEntrance cell [unconfirmed: followers may not ride the carriage] |
| VG50 | R X | E in Bruiant mansion cells | zzzCOGuide 43CBAE stage 10..59; zzzCOMq01 stage 30..59 |
| VG51 | K V | E in Bruiant mansion cells | G_GONE; zzzCOMq01 stage 30..59 |
| VG52 | R SE | E in cursed cells zzzCONobleMansion01/02/03/04BE, zzzCOCursedRoom01/02/04, zzzCONobleMansionBasement | G_GONE; zzzCOMq01 stage 30..59; SE_F |
| VG53 | K | E first time Kaidan near player after CH_BACK | CH_BACK; K_ANY; not MARTYR |
| VG54 | R I | E first time both near player after CH_BACK | CH_BACK; not MARTYR |
| VG55 | L R | T | CH_BACK; not MARTYR |
| VG56 | X SE | T | CH_BAD; SE_F; not MARTYR |
| VG57 | I C | T | zzzCHEpilogueQuest01 2D35CE started (stage >= 10); not MARTYR |
| VG58 | L K | T | CH_GOOD; not MARTYR |
| VG59 | L SE | T | CH_BAD; SE_F; not MARTYR |
| VG60 | V I | T | CH_BACK; not MARTYR |
| VG61 | I L | T | CH_BACK; after VG14; not MARTYR |
| VG62 | K V | T | CH_BACK; K_ANY; not MARTYR |
| VG63 | AS K | T | CH_BACK; K_CRUSH; ASHE_REVEAL; not MARTYR |
| VG64 | C R | T | CH_BACK; not MARTYR |
| VG65 | X L | T | CH_BACK; not MARTYR |
| VG66 | SE R | T | zzzBMMq03 done 220; CH_BACK; SE_F; not MARTYR |
| VG67 | X R | T | zzzCHMQ01 1363DB done 255; zzzAoMSubQ02 4D4C3D not completed |
| VG68 | V R | T | G_BACK; Gore following |
| VG69 | G K | T | G_BACK |
| VG70 | G R | T | G_BACK |
| VG71 | G L | T | G_BACK; zzzCHMemoryQuest08 080E91 completed |
| VG72 | V G | T | G_BACK; after VG69 |
| VG73 | K R | T | G_LOST; not MARTYR |
| VG74 | C I | T | G_LOST; after VG73; not MARTYR |
| VG75 | K V | E AFTERFIGHT:daedra | VG_JOINED; any zzzAoMMq01..08 running |
| VG76 | C R | E AFTERFIGHT | zzzAoMMq02 stage 10..30 |
| VG77 | SE I | E AFTERFIGHT:vampire | zzzAoMMq01 running or zzzBMMq01/02 running; not in Blood Matron cells; SE_F |
| VG78 | X V | E AFTERFIGHT | zzzAoMMq05 stage 25..30 |
| VG79 | AS L | E AFTERFIGHT | zzzAoMMq08 done 310 |
| VG80 | G C | E AFTERFIGHT | G_BACK; once |

### PART 2 - GLENMORIL  (60 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| VG81 | G R | T | zzzLrhMq01 007733 done 20; not stage 500..999; G_OK |
| VG82 | V C | T | zzzLrhMq01 done 130 |
| VG83 | K L | E first entry into Blessed Glen 006F1A | GL_ON |
| VG84 | I X | T | zzzLrhMq02 007835 done 20 |
| VG85 | K AS | T | zzzLrhMq02 done 70 |
| VG86 | R L | T | zzzLrhMq03 00790A done 40 |
| VG87 | X | T | zzzLrhMq03 done 40; not in Blessed Glen 006F1A |
| VG88 | V L | T | zzzLrhMq05 007F1F done 150 |
| VG89 | K X | T | zzzLrhMq06 0082EE done 160 |
| VG90 | I R | T | zzzLrhMq07 0083AC done 50; not stage 90..100 (White Owl scene) |
| VG91 | X G | T | zzzLrhMq07 done 60; G_OK |
| VG92 | K R | T | zzzLrhMq07 done 100 or 105; K_CRUSH |
| VG93 | V K | T | zzzLrhMq08 008431 done 10 |
| VG94 | K G | T | zzzLrhMq08 done 90; G_OK |
| VG95 | C I | T | zzzLrhMq09 0085BD stage 30..79 |
| VG96 | R L | T | zzzLrhMq09 done 40 |
| VG97 | X SE | T | zzzLrhMq09 done 60; SE_F |
| VG98 | R I | T | zzzLrhMq10 008685 done 170; not stage 190..220 |
| VG99 | G V | T | zzzLrhMq10 done 220; G_OK |
| VG100 | SE | T | zzzLrhMq10 done 220; SE_F |
| VG101 | L X | T | zzzLrhSqRoadRoller 614517 done 170 |
| VG102 | C R | T | zzzLrhSqRoadRoller done 40 |
| VG103 | SE L | T | zzzGHMq01 009B59 done 155; SE_F |
| VG104 | K V | T | zzzGHMq01 done 140; not stage 255 |
| VG105 | K G | T | zzzGHMq01Captive 06EDB0 done 10; Kaidan ref is in a Captive alias [unconfirmed: alias names Captive01-03]; G_OK |
| VG106 | L R | T | zzzGHMq01 done 140 |
| VG107 | R AS | T | zzzGHMq02 00E3EC done 20; ASHE_Q1 |
| VG108 | I V | T | zzzGHMq02 done 30; not stage 30..60 (briefing and flight scenes) |
| VG109 | G C | T | zzzGHMq02 done 310; G_OK [unconfirmed: followers aboard the airship] |
| VG110 | R K | T | zzzGHMq02Nazeem 06EDAF done 10 |
| VG111 | X V | T | zzzGHMq02GoodEnd 00EEFA done 70 |
| VG112 | V K | T | zzzGHMq02 done 310 and zzzGHMq02GoodEnd never started |
| VG113 | G R | T | zzzGHMq02Sub01 00FD2C done 50; not stage 70..130; G_OK |
| VG114 | I K | T | zzzGHMq03 01230D done 50; not in the slaughterhouse cell |
| VG115 | V C | T | zzzGHMq03Sub01 012962 stage 20..49 |
| VG116 | K AS | T | zzzGHMq04 0147BD done 35; not stage 30..50 (eavesdrop and briefing) |
| VG117 | C I | T | zzzGHMq04 done 100; not in Ysmir's Howl 00BC78 sewer scenes |
| VG118 | L R | T | zzzGHMq04 done 210 |
| VG119 | K X | T | zzzGHMq05 01719C done 220; zzzGHMq05Joint 017530 running |
| VG120 | V R | E in Lalanoah's house | zzzGHmq06Sub01 02C265 stage 30..55 |
| VG121 | C G | T | zzzGHMq06 017733 done 240; RC_WEREPIG; G_OK |
| VG122 | SE K | T | zzzGHMq06 done 240; SE_F |
| VG123 | L X | T | zzzLaMMq01 0B1758 done 20; not stage 10..30 (airship briefing); zzzCHMQ01 1363DB:Vigilant.esm done 255 |
| VG124 | K G | T | zzzLaMMq01 done 120; VG_JOINED; G_OK |
| VG125 | R X | T | zzzLaMMq02 0E9E2A done 150 |
| VG126 | G I | E rest after zzzLaMMq02 done 150 | zzzLaMMq03 103B86 stage 10..30 or LaMMq03 done; G_OK [unconfirmed: followers aboard] |
| VG127 | K V | T | zzzLaMMq04 11E085 done 50; not stage 80..155 |
| VG128 | SE AS | T | zzzLaMMq04 done 140; not done 145 or 150; SE_F |
| VG129 | K R | T | zzzLaMMq04 done 145 or 155; not in Svartibrunnr 000D62 |
| VG130 | V I | T | zzzLaMMq05 1329BD done 150; not in Great Hole of Hinnom 00EF8C |
| VG131 | K I | E near the Departure boat | zzzRevMq00 171135 stage 0..19 |
| VG132 | X C | T | zzzRevMq00 done 30; both speakers GetInWorldspace Svartibrunnr 000D62 [unconfirmed: followers may never arrive] |
| VG133 | R K | T | zzzRevSub02 01710D done 20; both speakers in 000D62 [unconfirmed] |
| VG134 | L G | T | zzzRevSub01Jabal 48BF99 done 10; both speakers in 000D62 [unconfirmed]; G_OK |
| VG135 | G V | T | zzzRevCqPedlar 3D45DE done 90; both speakers in 000D62 [unconfirmed]; GORE_FATHER; VAL_FATHER; G_OK |
| VG136 | R G | E AFTERFIGHT:ghoul | GL_ON; G_OK |
| VG137 | I L | E AFTERFIGHT | zzzLrhMq08 stage 50..70 |
| VG138 | I C | E AFTERFIGHT | zzzLrhMq10 stage 30..40 |
| VG139 | K V | E AFTERFIGHT:Thalmor | zzzGHMq04 stage 100..150 |
| VG140 | AS X | E AFTERFIGHT | zzzLaMMq05 done 40 or 45 |

### PART 3 - UNSLAAD  (50 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| VG141 | L K | E HighHrothgar exterior | zzzCrbMq01 01D8FF running, stage < 10; MQ105 not in its silent windows |
| VG142 | V C | T | zzzCrbMq01 stage 15 exactly; not in a scene [unconfirmed: research marks 10..19 as an optional quiet window] |
| VG143 | K G | E first time both speakers in Unslaad 004E70 | zzzCrbMq01 done 50; G_OK |
| VG144 | I C | T | zzzCrbMq01 done 50; in Unslaad 004E70 |
| VG145 | V R | T | zzzCrbMq02 02299D done 20 |
| VG146 | AS X | T | in Unslaad 004E70 or Lost Unslaad 064266 or Northern Sanctuary 0A750C; SNOW or exterior |
| VG147 | C R | T | in Unslaad 004E70; exterior |
| VG148 | R SE | T | zzzCrbMq01 done 50; SE_F |
| VG149 | K SE | T | zzzCrbMq02 done 110; DLC1VQ05 002850:Dawnguard.esm completed; SE_F |
| VG150 | G R | T | zzzCrbMq02 done 210; zzzCrbSqResurrection 11023D not done; G_OK |
| VG151 | V I | T | zzzCrbMq02 done 320; zzzCrbSqResurrection not done |
| VG152 | R L | T | zzzCrbSqResurrection done 10 |
| VG153 | V K | E in Bell Tower cell 0576E4 | zzzCrbMq03 112A83 stage 20..22 |
| VG154 | L | T | zzzCrbMq03 done 40 |
| VG155 | AS | T | zzzCrbMq03 done 30; ASHE_REVEAL |
| VG156 | AS G | T | zzzCrbMq01 done 50; in Unslaad 004E70; ASHE_HIRED; G_OK |
| VG157 | X I | E in Hidden Hot Springs 320187 | zzzCrbMq01 done 50 |
| VG158 | G L | T | zzzCrbMq01 done 50; in Unslaad 004E70; G_OK |
| VG159 | K R | E in Chow-Chow Tavern 32CD2F | zzzCrbMq01 done 50 |
| VG160 | K C | T | zzzCrbMq01 done 50; Moff met (topic 32A4C9 said) [unconfirmed check] |
| VG161 | V K | T | zzzCrbMq01 done 50 |
| VG162 | K X | E first entry into Lost Unslaad 064266 | zzzCrbMq04 117B3E stage 0..29 |
| VG163 | G C | T | zzzCrbMq04 done 30; not stage 55..90; G_OK |
| VG164 | K L | T | zzzCrbMq04 done 70; not stage 70 (Owl scene) or 90 |
| VG165 | SE V | T | zzzCrbMq04 done 90; DB; DLC1VQ04 00284F:Dawnguard.esm completed; SE_F |
| VG166 | K V | T | zzzCrbMq05 117B3F done 40; not stage 20..40 or 80..110; DB; K_TOG+ |
| VG167 | R G | T | zzzCrbMq05 done 40; in Northern Sanctuary 0A750C or Unslaad; not stage 80..110, 140..150, 160..190, 240..250; G_OK |
| VG168 | K | T | zzzCrbMq05 done 150; not stage 160..190; DB |
| VG169 | L SE | T | zzzCrbMq05 done 100; not stage 101..110 or 160..190; SE_F |
| VG170 | I X | T | zzzCrbMq05 stage 191..219 |
| VG171 | G K | E near the epilogue family in Unslaad | zzzCrbMq05 done 250; zzzCrbEpilogue 1EC845 scene not playing; G_OK |
| VG172 | V C | T | zzzCrbMq06 1DFDFA done 40 |
| VG173 | I X | T | zzzCrbMq06 done 40; zzzLrhMq02 007835:Glenmoril.esm done 80 |
| VG174 | X L | T | zzzCrbMq07 1DFDFB done 120 |
| VG175 | AS R | T | zzzCrbSq05 376B99 done 130; not stage 150..160; ASHE_REVEAL |
| VG176 | K L | T | zzzCrbSqMankar 411777 done 10; KMDQuest (0Kaidan.esp) completed |
| VG177 | K G | E in Dragon's Peak 32F628 | zzzCrbSq05 done 160; zzzCrbMq08 465EBF not started; G_OK |
| VG178 | R L | T | zzzCrbMq09 47A32B done 901; in Tamriel |
| VG179 | G I | T | zzzCrbMq09 done 901; after VG178; G_OK |
| VG180 | K SE | T | zzzCrbMq09 done 140 and done 901; K_ANY; SE_F |
| VG181 | V G | T | zzzCrbMq08 done 195; zzzCrbMq09 done 901; VAL_FATHIS; G_OK |
| VG182 | R I | T | zzzCrbMq08 done 310; zzzCrbMq09 done 901 |
| VG183 | C L | T | zzzCrbMq08 done 210; zzzCrbMq09 done 901 |
| VG184 | AS | T | zzzCrbMq08 done 195 or 210; zzzCrbMq09 done 901; DB; ASHE_HIRED |
| VG185 | X V | T | zzzCrbMq09 done 901; VG_ON; GL_ON; VAL_FATHIS |
| VG186 | R I | T | zzzCrbSqReopen 2904BE done 10 |
| VG187 | K G | E AFTERFIGHT | zzzCrbMq04 done 45; not stage 55..60; G_OK |
| VG188 | C R | E AFTERFIGHT | zzzCrbMq04 done 60; not stage 70 |
| VG189 | I V | E AFTERFIGHT | in Lost Unslaad 064266 |
| VG190 | K AS | E AFTERFIGHT | zzzCrbMq04 done 40 |
