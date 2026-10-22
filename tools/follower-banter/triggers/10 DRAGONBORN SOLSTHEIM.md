# Triggers - 10 DRAGONBORN SOLSTHEIM (DR1-DR140)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\10 DRAGONBORN SOLSTHEIM.txt`
Format and gate codes: TRIGGERS.md sections 4-5. Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap. "+Luna" = the player speaks (no Free() check; she is always there).
All quests/locations are `Dragonborn.esm` unless stated. "N done" = `GetStageDone <quest> N == 1`.

Extra rules for this file:
- `SOLST` everywhere means the talk also needs the player in `DLC2SolstheimWorld` (000800) unless the event says otherwise (DR2, DR125).
- Add the Dragonborn silence zones from dlc_cc_missives_3dnpc.md B3 to WorldQuiet(): DLC2MQ01 5..7; DLC2RRArrivalScene running; DLC2MQ02 20 done and 25 not done; Apocrypha (WS 01C0B2 or In 016E2B); DLC2MQ03 50..60; DLC2MQ05 340 done to DLC2MQ06 10 done; DLC2MQ06 200..550 (dragon flight); DLC2dunKolbjornQST 449..490.
- Val talks marked `not VAL_FATHIS` must never play after Val005 completes; their `VAL_FATHIS` twins (DR85/DR86, DR109 vs DR101/DR96) replace them.
- Kaidan crush talks (`K_CRUSH`) must stop once K04 >= 50.
- "In-fight bark" rows (DR126, DR128, DR130, DR132, DR134, DR136, DR138-DR140) play DURING combat: their scenes must NOT carry CombatEnd and must bypass the player-in-combat quiet rule (but keep every other quiet rule). One bark per fight, 2-4 lines.
- `AFTERFIGHT:<enemy>` races: ash spawn = DLC2AshSpawnRace, Lurker = DLC2LurkerRace, Seeker = DLC2SeekerRace, Riekling = DLC2RieklingRace, netch = DLC2NetchRace, ash hopper = DLC2AshHopperRace, werebear = DLC2WerebearBeastRace, burnt spriggan = DLC2SprigganBurntRace, bristleback = DLC2BoarRace, Miraak cultist = faction DLC2CultistFaction [all race/faction EditorIDs unconfirmed - check at build].

| ID | Speakers | Type | Gates |
|---|---|---|---|
| DR1 | K +Luna | E on DLC2MQ01 stage 7 set (note read), after combat ends | DLC2MQ01 7 done; DB |
| DR2 | L X | T | DLC2MQ01 7 done; DLC2MQ01 20 not done; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| DR3 | C V | E first arrival in DLC2SolstheimWorld, after DLC2RRArrivalScene stops running | SOLST; after R8 |
| DR4 | G K | E first time in Raven Rock (0143B9:Dragonborn.esm) | SOLST; after A1 |
| DR5 | K +Luna | E exterior Solstheim, outside Raven Rock | K_CRUSH; SOLST |
| DR6 | V X | E first time in Raven Rock (0143B9) | SOLST; after X4 |
| DR7 | I +Luna | E first time in Solstheim exterior outside Raven Rock | SOLST |
| DR8 | L +Luna | E Solstheim exterior, south coast, IsPleasant [no Red Mountain sight check; proxy unconfirmed] | SOLST |
| DR9 | K X | E in Bulwark location (019A25:Dragonborn.esm) | SOLST; after C3 |
| DR10 | G V | E Raven Rock exterior (0143B9) | SOLST; after A3 |
| DR11 | R I +Luna | E Raven Rock + NIGHT | DLC2MQ01 30 done; Earth Stone not yet freed (DLC2MQ03B not completed) [Earth Stone stage unconfirmed]; after B6 |
| DR12 | X +Luna | E after the Earth Stone is freed (Bend Will on it) | DLC2MQ03B running or completed, Earth Stone freed [exact stage unconfirmed]; DB |
| DR13 | X C | E Retching Netch (019A24:Dragonborn.esm) | SOLST; after R18 |
| DR14 | K X | E Retching Netch (019A24) | SOLST; after DR13; after C3 |
| DR15 | V I | T | DLC2TT1b completed (300/310/320); after I1 |
| DR16 | G C | E leaving Morvayn Manor [location ID unconfirmed] | DLC2MQ01 30 done [stage of meeting Morvayn unconfirmed]; after R5 |
| DR17 | V X | E Raven Rock Temple interior [location ID unconfirmed] | SOLST; after X4 |
| DR18 | G K +Luna | E Retching Netch (019A24) | SOLST; Teldryn Sero alive and not following [EditorID unconfirmed]; after A1 |
| DR19 | R K | E Raven Rock Mine (01429A:Dragonborn.esm) | SOLST; after B1 |
| DR20 | G +Luna | T | DLC2RR03 200 done |
| DR21 | L I | T | DLC2RR03 200 done; JRLucienInigoRank >= 2 |
| DR22 | L V | T or E Fort Frostmoth (014293:Dragonborn.esm) | DLC2RR01 90 done; after C1 |
| DR23 | I C | E AFTERFIGHT:ash spawn | SOLST; after R13 |
| DR24 | L X +Luna | E on DLC2RR02 stage 90 set, or next tick | DLC2RR02 90 done; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| DR25 | V X | T | DLC2RR02 90 done; VAL_FATHER; after X4 |
| DR26 | I X | T | DLC2RR02 200 done; after X6 |
| DR27 | K X | T | DLC2RR02 90 done; after C3 |
| DR28 | R V | E in Severin Manor (019A20:Dragonborn.esm) | DLC2RR02 running; HLIOValBanter stage >= 10 |
| DR29 | I V | E Raven Rock (0143B9) | after DR6; after I1 |
| DR30 | K X | E approaching Tel Mithryn (0143BC:Dragonborn.esm), first time | SOLST; after C3 |
| DR31 | X +Luna | E Tel Mithryn (0143BC), first time | after DR30 if Kaidan present, else first visit |
| DR32 | R X | T | DLC2MQ04 10 done; BPUFXelzazAndRemielInteractions stage 11 done |
| DR33 | L X | T | DLC2MQ04 10 done; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| DR34 | I K | E Tel Mithryn (0143BC) | DLC2MQ04 10 done; KaiandInigo stage >= 10 |
| DR35 | X I | T | DLC2TT1 running or completed (Varona dead) [stage unconfirmed]; after X6 |
| DR36 | L +Luna | T | DLC2TTF1 300 done |
| DR37 | G K | T | DLC2TT1 running; after A1 |
| DR38 | R C +Luna | T | DLC2TTR4a 200 done (agreed to be the test subject; 400 = refused, never); Remi-Redcap intro done (FA01RemiIntroScene) |
| DR39 | R X | T | DLC2TT2 500 done; BPUFXelzazAndRemielInteractions stage 11 done |
| DR40 | G X | E leaving Tel Mithryn (0143BC) | after DR31; after X1 |
| DR41 | R L +Luna | E Nchardak (0142B4:Dragonborn.esm) | DLC2MQ04 10 done; DLC2MQ04 550 not done; after B10 |
| DR42 | K V | E Nchardak (0142B4) | DLC2MQ04 10 done; DLC2MQ04 550 not done; after A2 |
| DR43 | V X | E Tel Mithryn (0143BC) | any DLC2TTR1-8 300 done; after X4 |
| DR44 | X +Luna | E Tel Mithryn Tower (01CDEA:Dragonborn.esm) | SOLST |
| DR45 | K +Luna | E Tel Mithryn Tower (01CDEA) | K_CRUSH; DLC2MQ04 10 done |
| DR46 | X K | T | DLC2TTF2 500 done; after C3 |
| DR47 | X +Luna | E CAMP or NIGHT on Solstheim | SOLST |
| DR48 | G K | E first time in Skaal Village (0143BB:Dragonborn.esm) | SOLST; after A1 |
| DR49 | L +Luna | E Skaal Village (0143BB) | SOLST |
| DR50 | C K | E Skaal Village (0143BB) | SOLST; after R1 |
| DR51 | G K +Luna | T | DLC2MQ02 30 done; after A1 |
| DR52 | I C | T | DLC2MQ03 10 done; after R13 |
| DR53 | K +Luna | T | K_CRUSH; DLC2MQ03 70 done [first Stone freed; stage unconfirmed]; DB |
| DR54 | G X | E on DLC2MQ03 60 set (Lurker dead), after combat | DLC2MQ03 60 done (never during 50..60); after X1 |
| DR55 | C +Luna | T | DLC2MQ03B 200 done; DB |
| DR56 | L V | T | DLC2SV01 200 done; after C1 |
| DR57 | G K | T | DLC2SV02 200 done; after A1 |
| DR58 | R X | T | DLC2SV02 200 done; BPUFXelzazAndRemielInteractions stage 11 done |
| DR59 | C I | T | DLC2WB01 100 done or 205 done; after R13 |
| DR60 | X +Luna | E Skaal Greathall (01D92C:Dragonborn.esm) + SNOW | SOLST |
| DR61 | K V +Luna | T | K_TOG+; DLC2MQ03 30 done [Bend Will first word; stage unconfirmed]; after A2 |
| DR62 | K C | T | SOLST; after an AFTERFIGHT:Riekling on Solstheim; after R1 |
| DR63 | G C | E arrival Thirsk (0143BA:Dragonborn.esm) | DLC2MH01 25 not done; DLC2MH01 210 not done; DLC2MH02 200 not done; after R5 |
| DR64 | K G C | T | DLC2MH01 25 done OR DLC2MH02 200 done; after A1; after R1; after R5 |
| DR65 | C I | T | DLC2MH01 25 done (Nords retook the hall); after R13 |
| DR66 | V C | T | DLC2MH01 210 done OR DLC2MH02 200 done (Riekling side); after R8 |
| DR67 | C G | T | DLC2MH02 200 done [chief turning on you per research, unconfirmed]; GORE_BAIL; after R5 |
| DR68 | C X | T | RC_CHIEF; after R18 |
| DR69 | K C | E AFTERFIGHT:Riekling boar rider | SOLST; after R1 |
| DR70 | L C | T | LUC_ADMIT; RC_MANOS [Bigpig reunion stage unconfirmed]; SOLST; after R11 |
| DR71 | C +Luna | T | RC_STAY; SOLST |
| DR72 | C K +Luna | T | K_CRUSH; RC_MANOS; DB; after R1 |
| DR73 | L C | E CAMP on Solstheim | SOLST; after R11 |
| DR74 | C G | E AFTERFIGHT:Riekling | SOLST; once; after R5 |
| DR75 | I C | T | SOLST exterior; after R13 |
| DR76 | C X | E netch nearby (Solstheim exterior) [no netch-proximity check; proxy: exterior Solstheim] | SOLST; after R18 |
| DR77 | V X | E STORM on Solstheim (ash storm weather) [ash-storm weather ID unconfirmed] | SOLST; after X4 |
| DR78 | C V | T | SOLST; after DR77; after R8 |
| DR79 | K X | E STORM on Solstheim (ash storm) | SOLST; after C3 |
| DR80 | G V +Luna | E STORM on Solstheim (ash storm) | SOLST; after A3 |
| DR81 | R L | T | DLC2MQ02 25 done; after B10 |
| DR82 | K G +Luna | T | DLC2MQ02 30 done; DELPHINE; DB; after A1 |
| DR83 | X K | T | DLC2MQ02 30 done; after C3 |
| DR84 | L +Luna | T | DLC2MQ02 40 done; DLC2MQ02 60 not done |
| DR85 | K V | T | DLC2MQ02 60 done; not VAL_FATHIS; after A2 |
| DR86 | K V | T | DLC2MQ02 60 done; VAL_FATHIS; after A2 |
| DR87 | G R | E first return from Apocrypha (DLC2MQ02 60 set, player back in DLC2SolstheimWorld) | BLACKBOOK; once; HLIOGoreBanter intro done |
| DR88 | R +Luna | E return from Apocrypha (any Black Book) | BLACKBOOK; after DR87 |
| DR89 | I +Luna | E return from Apocrypha (any Black Book) | BLACKBOOK |
| DR90 | X +Luna | E return from Apocrypha (any Black Book) | BLACKBOOK |
| DR91 | K G V | E return from Apocrypha (any Black Book) | BLACKBOOK; ANYROM; after A1; after A2; after A3 |
| DR92 | K +Luna | E return from Apocrypha (any Black Book) | BLACKBOOK; K_CRUSH |
| DR93 | K +Luna | E return from Apocrypha (any Black Book) | BLACKBOOK; K_TOG+ |
| DR94 | G I | E return from Apocrypha (any Black Book) | BLACKBOOK; after C2 |
| DR95 | R +Luna | T | DLC2MQ04 550 done |
| DR96 | V +Luna | T | DLC2MQ06 10 done; VAL_FATHIS |
| DR97 | K C | T | DLC2MQ06 10 done; after R1 |
| DR98 | I +Luna | T | DLC2MQ06 10 done |
| DR99 | C R | E after player dismounts a dragon on Solstheim [dragon-riding detection unconfirmed] | DLC2MQ06 550 done; Remi-Redcap intro done (FA01RemiIntroScene) |
| DR100 | K +Luna | T | DLC2MQ06 550 done |
| DR101 | V +Luna | T | DLC2MQ06 550 done; VAL_FATHIS |
| DR102 | X L G | T | DLC2MQ06 550 done; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions); after X1; after L1 |
| DR103 | C +Luna | T | DLC2MQ06 550 done; DB |
| DR104 | G K | E Raven Rock (0143B9) | DLC2MQ06 550 done; after A1 |
| DR105 | G +Luna | T | DLC2MQ06 550 done; after DR100 |
| DR106 | X I | T | DLC2MQ05 1000 done; after X6 |
| DR107 | L K | T | DLC2MQ06 550 done; Lucien-Kaidan intro done (Lucien's own scene 1) |
| DR108 | L +Luna | E return from Apocrypha via an optional Black Book | any DLC2BlackBook03-07Quest 20 done |
| DR109 | V +Luna | E return from Apocrypha via an optional Black Book | any DLC2BlackBook03-07Quest 20 done; not VAL_FATHIS |
| DR110 | V R | T | DLC2dunKolbjornQST 100 done; HLIOValBanter stage >= 10 |
| DR111 | I K | E near Kolbjorn Barrow (0142BB:Dragonborn.esm) | DLC2dunKolbjornQST 300 done; 449 not done [dig-phase stage unconfirmed]; KaiandInigo stage >= 10 |
| DR112 | V +Luna | T | DLC2dunKolbjornQST 490 done |
| DR113 | L +Luna | T | DLC2dunKolbjornQST 490 done |
| DR114 | G X | E arrival Castle Karstaag Ruins (01429E:Dragonborn.esm) | SOLST; after X1 |
| DR115 | C +Luna | E AFTERFIGHT:Karstaag [Karstaag death check unconfirmed] | SOLST |
| DR116 | R L | E Kagrumez (0142A2:Dragonborn.esm) | DLC2KagrumezQST not completed; after B10 |
| DR117 | L X | T | LUC_ENGINE; SOLST; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| DR118 | L +Luna | T | LUC_ADMIT; DLC2MQ04 10 done |
| DR119 | V G | T | DLC2dunHaknirTreasureQST 100 done [completion stage unconfirmed]; after A3 |
| DR120 | I K | E near Frostmoon Crag (0142CB:Dragonborn.esm) | SOLST; KaiandInigo stage >= 10 |
| DR121 | G K | T | DLC2EbonyWarriorQuest 100 done; DB; after A1 |
| DR122 | L X | E after STORM ends on Solstheim | SOLST; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| DR123 | K +Luna | E PREDAWN on Solstheim, exterior | K_TOG+; SOLST |
| DR124 | G R | E WATER on Solstheim | SOLST; HLIOGoreBanter intro done |
| DR125 | V G +Luna | E first arrival at Windhelm docks after leaving DLC2SolstheimWorld | SOLST; after A3 |
| DR126 | I C | E COMBAT:ash spawn (in-fight bark) | SOLST; after R13 |
| DR127 | X G | E AFTERFIGHT:ash spawn | SOLST; after X1 |
| DR128 | G K | E COMBAT:Lurker (in-fight bark) | DLC2MQ03 60 done; after A1 |
| DR129 | X +Luna | E AFTERFIGHT:Lurker | DLC2MQ03 60 done |
| DR130 | L +Luna | E COMBAT:Seeker (in-fight bark) | DLC2MQ02 10 done |
| DR131 | R K | E AFTERFIGHT:Seeker | DLC2MQ02 10 done; after B1 |
| DR132 | V K | E COMBAT:Miraak cultist (in-fight bark) | DLC2MQ01 5 done; DLC2MQ06 not completed; after A2 |
| DR133 | G C | E AFTERFIGHT:Miraak cultist | DLC2MQ01 7 done; after R5 |
| DR134 | C K | E COMBAT:Riekling (in-fight bark) | SOLST; after R1 |
| DR135 | V C | E AFTERFIGHT:Riekling | SOLST; after R8 |
| DR136 | L C | E COMBAT:bristleback boar (in-fight bark) | SOLST; after R11 |
| DR137 | R X | E AFTERFIGHT:netch | SOLST; after DR76; BPUFXelzazAndRemielInteractions stage 11 done |
| DR138 | G +Luna | E COMBAT:ash hopper (in-fight bark) | SOLST |
| DR139 | G I | E COMBAT:werebear (in-fight bark) | SOLST; after C2 |
| DR140 | X V | E COMBAT:burnt spriggan (in-fight bark) | SOLST; after X4 |
