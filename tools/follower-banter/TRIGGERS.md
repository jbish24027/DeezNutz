# Follower Banter - trigger design and per-talk table

Built 2026-10-18 from the research in `research\triggers\` (kaidan_block.md, others_block.md, vanilla_gates.md) and `research\bibles\`.
Script source of truth: the five `FOLLOWER BANTER - SCRIPT *.txt` files on the user's Desktop.
User-facing summary: `Notes and Files\FOLLOWER BANTER - WHEN TALKS PLAY.txt`.

## 1. Architecture

- One new plugin, ESL-flagged if it fits (override-free, new records only). **No masters beyond Skyrim/Update/DLC.** Every follower form is pulled with `Game.GetFormFromFile` (soft dependency, same as Remiel's `HLIOModCheckerScript`). A missing follower mod = that follower's talks never run.
- **Controller quest** `FB_Controller` (StartGameEnabled). The player alias script:
  - `OnInit` / `OnPlayerLoadGame`: re-resolve all follower refs, story quests and globals via GetFormFromFile; force refs into aliases `Kaidan, Gore, Val, Remi, Xelzaz, Inigo, Lucien, Redcap` (+ `Scrap` 885448:HLIORemi.esp).
  - `RegisterForSingleUpdate(300)` real seconds = the 5-minute timer (user pick). Re-registers after each tick.
  - `OnLocationChange`, `OnCombatStateChanged` (end of player combat, 8 s delay), and a 60 s weather/time poll fire the **event** talks.
- Each talk = one Scene in a per-pair quest (`FB_Pair_KG`, `FB_Pair_KV`, ...), actors via the controller's aliases (alias-to-alias: per-pair quest aliases use `External` alias pointing at `FB_Controller`). Scene flags: CombatPause? NO, use **DeathEnd + CombatEnd + DialogueEnd** (talks are disposable; never resume mid-fight).
- Picking: build candidate list = talks whose speakers are all `Free(x)` and whose gates pass and not played; pick random; `Scene.Start()`; set played bit (int arrays in script, 32 bits each).
- Cooldown: after any talk ends, no new talk for 300 s even on events (prevents back-to-back).
- **Voice:** INFOs in our plugin; files at `sound\voice\<ourplugin>.esp\<VoiceTypeEditorID>\`. VoiceTypes: KaiVoice, HD1GoreVoice, AX_ValVoice, HLIORemiVoice, BPUFXelzazVoice, Inigofollowervoice, JRLucienVoice, FA01RedcapVoice. Voice type is read from the actor at runtime, so no master needed. Check each EditorID in-game folder name casing at build.

## 2. Global quiet rules (`WorldQuiet()`, checked before anything)

Fail = no talk. From vanilla_gates.md A4 + B3 and kaidan_block.md 2b.

- Player: IsInCombat, IsInDialogueWithPlayer-equivalent (`UI.IsMenuOpen("Dialogue Menu")`), sneaking, sleeping, `Game.IsMovementControlsEnabled()==false`, `Game.IsFightingControlsEnabled()==false`, in AnimationFaction 9A2BB9:Kaidan - Immersive Features.esp, OStim scene (API unconfirmed; fallback: player in any scene/package lock).
- `AP_StartCellQ` running; MQ101 stage >= 3 and 1000 not done (Helgen intro + escape).
- MQ104 48..129; MQ105 20..159 and 240..299 in HighHrothgarLocation; MQ106 60..169; MQ201 35..249; MQ203 30-65,110-140,210-280; MQ204 20..209 in ThroatoftheWorldLocation; MQ206 20..219; MQ302 40..299; MQ301 200..219 [unconfirmed]; MQ303 5..99 and 180; MQ304/MQ305/MQ306 running; Sovngarde worldspace.
- RelationshipMarriageWedding 10..499.
- CWSiege / CWSiegeObj / CWFortSiegeFort running; CWFinale 300..499; CW01A/B 160..199; CW03 at 20/100/225.
- TG05 10..199; TG07 10..39; TG08A 40..59; TG08B 40..59; TG09 30..199; TGLeadership 30..199.
- DB02 10..39; DB04 10..49; DB10 running; DB11 5..199.
- C03 15..24; C02 10..199; C06 stage 10 and 30..199.
- MG05 20..49; MG08 10..199.
- DLC1VQ02 8..19; DLC1VQ08 running; DLC1VQ05 running.
- DLC2MQ06 >= 330 and not completed; in DLC2ApocryphaWorld.
- **Kaidan big set pieces (apply even when Kaidan is not in the talk):** kaidan_block.md §2b items 1-11 (KaiWeddingNukeIdles, three wedding windows, honeymoon 80..149, KMD finale group, Companions showdown scenes, ProposalScene/FirstKissScene, BlackScene, ArrestScene).

## 3. Per-speaker `Free(x)` (all must pass for every speaker in the talk)

Common to all: ref resolved, not disabled, not dead, `IsInScene()==false`, not in dialogue with player, `GetCombatState()==0`, not bleeding out, not sitting/sleeping (`GetSleepState()==0`), `GetActorValue("WaitingForPlayer")==0`, within 1000 units of the player and of each other speaker, same cell/worldspace.

| Who | Following test | Busy blocks |
|---|---|---|
| Kaidan | K01 stage 30 done; CurrentFollowerFaction | kaidan_block.md §2a rows 4-45 + §4 places |
| Gore | CFF (or IsPlayerTeammate) | HD1GoreFollows DialogConditions block (others_block.md §1a) + §1b quests; `HD1GoreRomance3 == 2` (shrine trip) |
| Val | `AX_ValRecruited 08E466 == 1` (NOT CFF) | AX_ValSightlessPit, AX_ValSleepy, AX_ValNoTeleport == 0; §2b windows; ValEnd >= 10 = never |
| Remi | CFF | HLIOScrapAttackMode == 0, HLIOPuzzleTime != 1, not in Cidhna Mine; §3b windows |
| Xelzaz | CFF; BPUFXelzazFollower stage 100 done | IsUndead == 0; §4b windows; BPUFXelzazWaitingQuest stage 12 = gone |
| Inigo | **IsPlayerTeammate** (NOT CFF) + WaitingForPlayer == 0 | InigoBadVibrations 70..(not completed); not in RiftenJailLocation |
| Lucien | CFF; JRLucienIntro >= 30 | not in JRLucienBetrayedFaction; JRLucienPaarthurnax 10 done & 15 not; Personal1 35..(800 not done); GetHorseQuest 10..199 |
| Redcap | CFF | §7b quests running; FA01RedcapDrunkQ == 10 (drunk) = skip serious talks only |

Remi+Xelzaz talks also blocked while `BPUFXelzazRemielFallingOut` 11 done and 13 not.

## 4. Gate codes used in the table

Romance (from kaidan_block.md §5, others_block.md §1d/§2d):
- `K_CRUSH` = K04 >= 5 and < 50 and K04 not in {37, 42}  (user: early stages = his crush, not real romance yet)
- `K_TOG+` = K04 >= 50 and != 57; `K_TOG` = 50..64 (!=57)
- `K_LOVE+` = K04 >= 65; `K_LOVE` = 65..80
- `K_ENG` = 81..99; `K_MAR` = 100 (or PlayerMarriedFaction on Kaidan)
- `K_ANY` = K_CRUSH or K_TOG+
- `G_FLIRT` = HD1Romance == 1, HD1GoreRomance2 == 0, HD1Breakup == 0; `G_TOG+` = HD1GoreRomance2 == 1, Breakup == 0; `G_OATH` = HD1GoreRomance3 >= 3
- `V_FLIRT` = Val00A >= 10, AX_Love == 0, AX_FriendZone == 0; `V_TOG+` = AX_Love == 1; `V_MAR` = AX_ValMarried == 1
- `STEP0` = not K_ANY, not G_FLIRT/G_TOG+, not V_FLIRT/V_TOG+
- `ANYROM` = K_ANY or G_FLIRT or G_TOG+ or V_FLIRT or V_TOG+

Story:
- `HELGEN` = MQ101 stage 145 done
- `DB` = MQ104 stage 80 done AND 90 done (real Watchtower kill; AP skip fakes 90 only)
- `SHOUT1` = MQ104 90 done
- `HH` = MQ105 20 done; `GREYBEARDS` = MQ105 30 done
- `DELPHINE` = MQ106 30 done; `PAARTH` = MQ204 95 or MQ205 10 done; `ALDUIN` = MQ305 200 done
- `CW_IMP` = CW01A 200; `CW_SONS` = CW01B 200
- `TG_BRYN` = TG00 8; `TG_JOIN` = TG02 10; `DB_JOIN` = DB02 50; `CICERO` = DB03 10
- `C_JOIN` = C00 100; `WOLF` = C03 25; `MG_JOIN` = MG01 30; `ARCH` = MG08 200
- `SERANA` = DLC1VQ02 5; `SOLST` = DLC2MQ01 20; `BLACKBOOK` = DLC2MQ02 60; `DA14` = DA14 completed
- `BRYNJAR` = K03 >= 50 [UNCONFIRMED: Brynjar story told at K03 40-50 per bible]
- Personal: `GORE_BAIL` = HD1GoreJailtime completed; `GORE_FATHER` = HD1GoreQuest2 completed & HD1GoreMurdererVar 0; `VAL_FATHER` = Val003 completed; `VAL_FATHIS` = Val005 completed; `REMI_MORVIC` = HLIOMQ1 190 done; `LUC_ENGINE` = JRLucienPersonal1 800 done; `LUC_ADMIT` = JRLucienGetHorseQuest 40 done [inferred]; `INIGO_BV` = InigoBadVibrations completed; `RC_MANOS` = FA01RedcapSolstheimManosQ 70 done; `RC_STAY` = ManosQ completed; `RC_REDGOD` = FA01RedcapRedGodQ completed; `RC_WEREPIG` = FA01RedcapWereboarQ completed; `RC_CHIEF` = FA01RedcapThirskChief == 1

Events / places (player location keywords and checks):
- `INN` LocTypeInn; `CITY:<Name>` GetInCurrentLoc <hold capital location> on arrival; `RIVERWOOD`; `TEMPLE_MARA_RIFTEN`; `BARDS_COLLEGE`; `HELGEN_LOC` HelgenLocation 018A4A
- `DWEMER` LocTypeDwarvenAutomatons; `CRYPT` LocTypeDraugrCrypt; `FALMER` LocTypeFalmerHive; `GIANT` LocTypeGiantCamp nearby; `CAVE` LocTypeDungeon interior
- `RAIN` IsRaining; `SNOW` IsSnowing; `NIGHT` hour >= 20 or < 5; `PREDAWN` hour 4..6; `MORNING` 5..9; `CLEARNIGHT` NIGHT and IsPleasant; `AURORA` = CLEARNIGHT + exterior [no aurora check; unconfirmed]
- `CAMP` exterior, not LocTypeHabitation, `_Frost_NearFire == 1` or Campfire tent [unconfirmed which works]; `WATER` PO3 IsActorInWater or near shore [unconfirmed]
- `AFTERFIGHT[:enemy]` controller saw player combat end; enemy type by last combat target race/faction (Thalmor, hagraven, bandit, draugr)
- `SNEAKING` player sneaking (allowed only for A9; overrides the global sneak block)
- `HOUSE` LocTypePlayerHouse; `STORM` RAIN/SNOW + GetWindSpeed >= 0.6 [unconfirmed]

Chains: `after:X` = talk X already played. Every pair's "meets" talk must play before that pair's other talks.

## 5. Per-talk table

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap.
Type: T = timer, E = event (fires on the moment).

### Batch 1
| ID | Speakers | Type | Gates |
|---|---|---|---|
| A1 | G K | T | first meeting |
| A2 | V K | T | first meeting |
| A3 | G V | T | first meeting |
| A4 | V G K | E exterior | STEP0; after A1,A2,A3 |
| A5 | K G V | T | STEP0; after A1,A2,A3 |
| A6 | G V K | E INN | STEP0 or K_CRUSH/G_FLIRT/V_FLIRT; after meets |
| A7 | V G K | E AFTERFIGHT | STEP0; after meets |
| A8 | G K | E CAMP | BRYNJAR; after A1 |
| A9 | V K | E SNEAKING | STEP0; after A2 |
| A10 | V G | T | K_CRUSH |
| A11 | K G | T | V_FLIRT |
| A12 | V K | T | G_FLIRT |
| A13 | V K G | T | K_TOG |
| A14 | V K | T | V_TOG+ |
| A15 | K G V | T | G_TOG+ |
| A16 | G K V | E AFTERFIGHT:draugr | ANYROM (K_CRUSH/K_TOG, G_*, V_*) |
| A17 | V G K | T | ANYROM; Val6 boat bought (Val006 stage 20) for Val's line [else swap line] |
| A18 | V G K | E INN | K_MAR |
| A19 | K V G | T | V_MAR |
| A20 | V G K | T | G_OATH |
| A21 | K V G | T | K_CRUSH or K_TOG |
| A22 | G V | E AFTERFIGHT | STEP0; after A3 |
| A23 | G K V | T | ANYROM; after meets |
| A24 | G K V | E CAMP+NIGHT | STEP0 or K_CRUSH or G_FLIRT or V_FLIRT |
| B1 | R K | T | first meeting |
| B2 | R K | T | after B1 |
| B3 | K R | T | after B1 |
| B4 | R K | T | after B3; not CITY |
| B5 | R K | T | K_CRUSH or K_TOG; V also following not required |
| B6 | I R | T | first meeting |
| B7 | I R | T | after B6 |
| B8 | R I | T | after B6 |
| B9 | R I | E CAVE or CRYPT | after B6 |
| B10 | L R | T | first meeting |
| B11 | R L | E CITY (any) | after B10 |
| B12 | L R | T | after B10 |
| B13 | L R | E DWEMER | after B10 |
| B14 | R V | T | V_FLIRT or V_TOG+ |
| B15 | G R | T | G_FLIRT |
| B16 | R X | T | ANYROM; Remi/Xel not fallen out |
| C1 | L V | T | first meeting |
| C2 | G I | T | first meeting; not CITY |
| C3 | X K | T or E CAMP | first meeting |

### Kaidan and Luna
| ID | Speakers | Type | Gates |
|---|---|---|---|
| K1 | G K | T | K_CRUSH; after A1 |
| K2 | V K | T | K_CRUSH; after A2 |
| K3 | R K | T | K_CRUSH; after B1 |
| K4 | I K | T | K_CRUSH; Kaidan+Inigo intro done (KaiandInigo stage >= 10) |
| K5 | L K | T | K_CRUSH; Lucien-Kaidan intro done (Lucien's own) |
| K6 | X K | T | K_CRUSH; after C3 |
| K7 | R K | T | K_CRUSH; after K3 |
| K8 | V K | T | K_CRUSH; after K2 |
| K9 | K G | E after dragon soul absorbed | K_CRUSH or K_TOG+; DB |
| K10 | L K | E after player shout in combat | K_CRUSH or K_TOG+; SHOUT1 and DB |
| K11 | G V | T | K_CRUSH; after A3 |
| K12 | G K | T | K_TOG |
| K13 | V K | T | K_TOG+ |
| K14 | K I | T | K_TOG |
| K15 | L K | E INN+MORNING | K_TOG+ |
| K16 | K X | E CAMP | K_TOG+ |
| K17 | R K | T | K_TOG |
| K18 | K G | T | K_TOG+ |
| K19 | K I | E AFTERFIGHT (player health dipped < 25% during fight) | K_TOG+ |
| K20 | V K | T | K_LOVE+ (K04 >= 65) and < 81 |
| K21 | L K | T | K_LOVE |
| K22 | V G | T | K04 75..80 |
| K23 | K G | T | K04 80..81 |
| K24 | V K | T | K04 80..81 |
| K25 | R K | T | K04 80..81 |
| K26 | X K | T | K04 80..81 |
| K27 | L K | T | K_ENG |
| K28 | G K | T | K_MAR |
| K29 | V K | T | K_MAR |
| K30 | R K | T | K_MAR |
| K31 | I K | T | K_MAR |
| K32 | X K | E MORNING | K_MAR |
| K33 | R X | T | K_MAR |

### Batch 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| R1 | K C | E CAMP | first meeting |
| R2 | C K | T | after R1 |
| R3 | C K | T | K_CRUSH; after R1 |
| R4 | C K | T | K_TOG+; after R1 |
| R5 | G C | T | first meeting |
| R6 | G C | T | RC_MANOS; after R5 |
| R7 | G C | E WATER | after R5 |
| R8 | V C | E CAMP | first meeting |
| R9 | C V | T | after R8 |
| R10 | C V | T | after R9 |
| R11 | L C | T | first meeting |
| R12 | L C | T | after R11 |
| R13 | C I | T | first meeting (Inigo-Redcap has own lines in Redcap's mod; this is not an intro) |
| R14 | C I | T | after R13 |
| R15 | R C | T | RC_WEREPIG |
| R16 | C R | T | RC_REDGOD |
| R17 | R C | T | RC_CHIEF |
| R18 | X C | T | Redcap-Xelzaz own intro done (BPUFXelzazAndRedcapInteractions apology stage) [find stage at build] |
| R19 | X C | T | after R18 |
| R20 | C V G | T | ANYROM; after R5, R8 |
| X1 | G X | T | first meeting |
| X2 | G X | E AFTERFIGHT | after X1 |
| X3 | G X | E WATER | after X1 |
| X4 | X V | T | first meeting |
| X5 | V X | E MORNING | after X4 |
| X6 | I X | T | first meeting |
| X7 | X I | E CAMP or INN | after X6 |
| X8 | X K | E STORM or RAIN | after C3 |
| I1 | V I | T | first meeting |
| I2 | I V | T | after I1 |
| I3 | I V | T | VAL_FATHIS; after I1 |
| I4 | G I | E CAVE (spider kill) | after C2 |
| L1 | G L | T | first meeting |
| L2 | G L | T | after L1 |
| L3 | L G | E CRYPT | after L1 |
| L4 | V L | T | after C1 |
| M1 | R I | T | after B6 |
| M2 | R L | T | LUC_ADMIT; after B10 |
| G1 | R G I | E MORNING after CAMP | — |
| G2 | L X C | E DWEMER or any ruin | — |
| G3 | V I C | T | after I1, R8, R13 |

### Quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| Q1 | G K | E on GREYBEARDS set (MQ105 30) or next tick | GREYBEARDS |
| Q2 | R L | E after dragon soul | DB |
| Q3 | G V | E HELGEN_LOC | HELGEN; not in Helgen intro window |
| Q4 | G I | E on 7000 Steps (Ivarstead→HH road; GetInCurrentLoc HighHrothgar exterior path or MQ105 stage 10..19) | SHOUT1 |
| Q5 | G L | T | DELPHINE |
| Q6 | L X | T | PAARTH; MQPaarthurnax 50 not done |
| Q7 | C K | T | SHOUT1 |
| Q8 | V G K | T | ALDUIN |
| Q9 | G K | T | CW_SONS |
| Q10 | L K | T | CW_IMP |
| Q11 | R V | T | TG_JOIN |
| Q12 | K R | T | TG_BRYN; K_CRUSH or K_TOG+ |
| Q13 | X I | T | DB_JOIN |
| Q14 | G K | T | CICERO |
| Q15 | K V | E CITY:Whiterun or T | C_JOIN |
| Q16 | C R | T | WOLF |
| Q17 | L R | E in Winterhold College | MG_JOIN |
| Q18 | X V | T | ARCH |
| Q19 | C K | T | SERANA |
| Q20 | C G | E arrival | SOLST (first time in DLC2SolstheimWorld) |
| Q21 | C K | T | DA14; K_CRUSH or K_TOG+ |
| Q22 | L V | T | BLACKBOOK |
| Q23 | V K | T | GORE_BAIL |
| Q24 | G V | T | VAL_FATHER and GORE_FATHER |
| Q25 | K R | T | REMI_MORVIC |
| Q26 | G L | T | LUC_ADMIT |
| Q27 | C I | T | INIGO_BV |
| Q28 | V C | T | RC_MANOS; after A22 (tall half callback) |
| Q29 | K C | T | RC_STAY |
| Q30 | X I | T | INIGO_BV |

### Batch 3
| ID | Speakers | Type | Gates |
|---|---|---|---|
| P1 | C L | E CITY:Whiterun | after R11 |
| P2 | V K | E CITY:Solitude | after A2 |
| P3 | X G | E CITY:Windhelm | after X1 |
| P4 | I G | E CITY:Riften | GORE_BAIL; after C2 |
| P5 | R K | E CITY:Markarth | after B1 |
| P6 | L R | E CITY:Falkreath | after B10 |
| P7 | G V K | E INN | K_CRUSH or K_TOG+ |
| P8 | V G | E INN | after A3 |
| P9 | K V | E PREDAWN | after A2 |
| P10 | R K | E in Temple of Mara (Riften) | K04 65..80 |
| P11 | G K | E RIVERWOOD | after A1 |
| P12 | L G | E BARDS_COLLEGE | after L1 |
| W1 | X K | E RAIN | after C3 |
| W2 | V K | E RAIN | K_TOG+ |
| W3 | I C | E RAIN | after R13 |
| W4 | K G | E SNOW | after A1 |
| W5 | V C | E SNOW | after R8 |
| W6 | R X | E SNOW | K_ANY |
| W7 | G I | E AURORA | after C2 |
| W8 | L K | E AURORA | K_ANY |
| W9 | K I | E PREDAWN | — |
| W10 | L V | E CLEARNIGHT | after C1 |
| W11 | V G K | E CAMP+NIGHT | after meets |
| W12 | G K | E CAMP+NIGHT, player sleeping NOT required (Luna "asleep" is flavour) | K_TOG+; after K18 |
| W13 | C G | E CAMP+NIGHT | after R5 |
| D1 | R K | E DWEMER | K_ANY; after B1 |
| D2 | L C | E DWEMER | after R11 |
| D3 | R K | E CRYPT | after B1 |
| D4 | G V | E CRYPT | after A3 |
| D5 | L G | E FALMER | after L1 |
| D6 | C K | E GIANT | after R1 |
| D7 | G K | E AFTERFIGHT:Thalmor | after A1 |
| D8 | C G | E AFTERFIGHT:hagraven | after R5 |
| D9 | V X | E AFTERFIGHT:bandit | after X4 |
| KX1 | K X | T | K04 30..49 (late crush) |
| KX2 | K I | T | K_LOVE+ |
| KX3 | G K | E CAMP or INN | K_TOG+ |
| KX4 | C K | T | K_TOG+; after R1 |
| KX5 | G V | T | K_TOG+ |
| KX6 | R K | T | K_TOG |
| KX7 | V K | E AFTERFIGHT (player took a big fall / troll) | K_CRUSH |
| KX8 | X K | E HOUSE | K_MAR |

## 6. Open items to verify at build / in test
- BRYNJAR gate stage (K03 40 vs 50).
- Inigo CFF: is he re-added by `_Authoria_REQ_MajorFollowerBridge`? (use IsPlayerTeammate regardless)
- AURORA, CAMP, WATER, STORM proxies.
- LUC_ADMIT stage 40 (journal-only).
- R18 Redcap-Xelzaz apology stage.
- Exact VoiceType folder names (EditorIDs above; build uses lowercase).
- Line text with `*Sigh*` and stage directions: strip before TTS, keep as subtitle-free.

### Seasons, holidays, lost (file: SCRIPT SEASONS HOLIDAYS LOST.txt)
Date gates use vanilla globals GameMonth (0 = Morning Star) and GameDay. Holiday window = day D or D+1. Season talk window = first 5 days of the season's first month, else any day of the season if missed (once only).
Seasons: spring = months 2-4, summer 5-7, autumn 8-10, winter 11,0,1. Holidays mod (`Holidays.esp`, isoku) uses the standard TES calendar; its `_HolidayQuestScript.CheckDate` keys off the same globals.

| ID | Speakers | Type | Gates |
|---|---|---|---|
| S1 | G R | T | spring start |
| S2 | X V | T | summer start |
| S3 | G K | E WATER | summer; after A1 |
| S4 | K L | T | autumn start |
| S5 | V K | E exterior | autumn; K_ANY |
| S6 | C X | E SNOW | winter, first snow seen this winter |
| S7 | G V | E SNOW exterior | winter |
| H1 | G K | T | New Life, Morning Star 1 (m0 d1) |
| H2 | R I | E NIGHT | m0 d1 |
| H3 | R K | T | Heart's Day m1 d16; K_ANY |
| H4 | V G | E INN | m1 d16; K_TOG+ |
| H5 | R V | T | Jester's Day m3 d28 |
| H6 | K C | E MORNING | m3 d28 |
| H7 | X G | T | First Planting m2 d7 |
| H8 | V I | T | Mid Year m5 d16 |
| H9 | R V | E CITY | Merchant's Festival m6 d10 |
| H10 | G K | T | Harvest's End m7 d27; BRYNJAR |
| H11 | L C | T | Witches Festival m9 d13 |
| H12 | G K | E CITY | Warriors Festival m10 d20 |
| H13 | R K | T | Saturalia m11 d25; K_ANY |
| H14 | V G C | T | m11 d25 |
| H15 | I G | E NIGHT | Old Life m11 d30 |
| N1 | V K | T | WILD (exterior, LocTypeHabitation false, player moving) |
| N2 | R X | T | WILD |
| N3 | C G | T | WILD |
| N4 | L K | T | WILD |
| N5 | G K | T | WILD; K_TOG+ |
| N6 | V I | T | WILD |
| N7 | R K | T | WILD |
| N8 | X G | T | WILD |
| N9 | I C | T | WILD |
| N10 | V G K | T | WILD; K_TOG+ |
Lost talks: max one per in-game day.

## 7. "What does everyone think?" (user approved 10-18)
- New player dialogue topic on every follower in the party (top-level, conditioned: speaker is one of our 8 and is Free; at least one other party member Free).
- Choosing it asks the controller for the best talk for RIGHT NOW: priority 1 an unplayed event/quest talk whose gates pass at this location/moment (ignoring the timer and the "must be the moment" part of E talks, but never the safety gates), priority 2 any unplayed timer talk that includes the follower you asked, priority 3 a short "nothing new" reply from that follower (8 one-liners per follower, e.g. Kaidan: "We've said all we've got for now, love. Ask me after the next fight.").
- Still obeys WorldQuiet() and Free(); if blocked, the follower gives a "not now" one-liner (8 per follower).
- Resets the 5-minute timer so the party doesn't immediately start another.
- Needs: 8 x (topic line variants) + 8 x 8 "nothing new" + 8 x 4 "not now" lines = extra writing in the party-life batch.

## 8. Chain safety (decided 10-18)
Any talk gated `after:X` whose own speakers are Free but whose predecessor X can never play (a speaker of X not recruited / dead / gone) is unblocked once X has been eligible-but-unplayable for 10 in-game days. Chains never stall the story.
