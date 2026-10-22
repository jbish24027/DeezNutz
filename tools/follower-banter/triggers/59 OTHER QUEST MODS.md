# 59 OTHER QUEST MODS - trigger rows (prefix OM, 120 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\59 OTHER QUEST MODS.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4, `research\content\00_inventory.md` (sections 4-5), the bibles, and the quest records (names, stages, journal text, objectives, NPC names) read read-only through houseCARL `housecarl_records` on 2026-10-18 (epoch e2-509d9856becc0652, profile DEEZ CS NUTZ - PICTA).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Serana and Ashe use the Free() rows in `20 DAWNGUARD.md` section 1. Every row with S also needs `SERANA` plus Serana following; every row with A also needs `ASHE_HIRED` plus Ashe following. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment).

## Soft dependencies

Every quest below is resolved with `Game.GetFormFromFile` from its own plugin, so a missing mod just means its rows never fire. No new masters.

## Event and gate codes (new in this file)

- `QD:<EditorID>` = that quest `IsCompleted()` turns true this tick (E) / is completed (gate).
- `QS:<EditorID> N` = `GetStageDone(N)` turns true this tick (E) / is done (gate). `QS!` = stage N **not** done.
- `QR:<EditorID>` = quest `IsRunning()`.
- `OBJ:<EditorID> "<text>"` = the objective with that display text is displayed and not completed (`IsObjectiveDisplayed && !IsObjectiveCompleted`); `OBJDONE` = it was just completed. Objective indexes were not traced, so the build matches by text **[UNC index]**.
- `IN:<place>` = player is inside that mod's worldspace or location (location keyword / worldspace FormID from the plugin **[UNC FormID]**).
- `NOT_VAL_FATHIS` = Val005 not completed (Val still says "Mora and I have history").
- `PC_VAMP` = player `HasKeyword Vampire (0A82BB:Skyrim.esm)`.
- `ORIGIN:<EditorID>` = that Book of Origins quest was the one started this playthrough (`GetStageDone(10)`).
- `ONCE_PER_MEET` = for the repeat-meeting road mods (Slays-Many-Beasts, Walks-Distant-Sands, Dar'balag, Once We Were Here): fire after any encounter stage that ends a meeting; only once in total.

Reused codes: `AFTERFIGHT`, `CAMP`, `CITY`, `HELGEN`, `K_ANY`, `K_CRUSH`, `BRYNJAR`, `MG_JOIN`, `SOLST`, `DB_EITHER` (TRIGGERS.md section 4); `K_AKAVIRI` (Kaidan KINV 0B3032:0Kaidan.esp stage 50 done); `SERANA`, `DG_CAIRN` (20 DAWNGUARD.md); `ASHE_HIRED`, `ASHE_REVEAL` (49 ASHE.md). Pair chains `after <ID>` as TRIGGERS.md "Chains" (A1 G-K, A2 V-K, A3 G-V, B1 R-K, B6 I-R, B10 L-R, C1 L-V, C2 G-I, C3 X-K, R1 K-C, R5 G-C, R11 L-C, R13 C-I, R18 X-C, X1 G-X, X4 X-V, X6 I-X, L1 G-L). Pairs whose meeting lives in the follower mods name that mod's intro.

## Quests used (EditorID, FormID)

- **DAc0da.esm:** zDcdMq00 The Call of Landfall 00AA0C · zDcdMq01 The Sea of Causality 004475 · zDcdMq02 Negative Legacy 004931 · zDcdMq03 Patchwork 004981 · zDcdMq04 Numidium Tertius 00B21B · zDcdMqBoss01 VS Nchunak 00B265 · zDcdMqBoss02 VS GC9 00B3A8 · zDcdMqBoss04 VS Zurin Arctus 00B5EE · zDcdMqBoss05 VS Dumac 00B6DC · zDcdMqCheeseEnd Rella Mozzarella 00C9F1 · zDcdSqYngol Drowned Nighthawk 004B1C · zDcdSqWorm Echoes of Mnemolichite 0052C2 · zDcdSqWormSub04 The Sea of Radiance 006134. NPCs: Rolls-On-Roads (Psijic monk), Akashiya-Samon 003152, Yngol 00316B, Vanus Galerion 005183, Vigilant Athanasius 005251, Crabbimarco 0048A0, Lokir of These Parts 00AA00, Nchunak the Evangelist 006B69, Zurin Arctus 00AF11, Dumac's Tonalframe 00B1F8.
- **Olenveld.esp:** OlenveldWarmWelcome 5162BC · OlenveldEtherealComplications 5162B7 · OlenveldFromBelowWeGrow 516258 · OlenveldHarshWinds 5162C8 · OlenveldCityRenovations 516253 · OlenveldBigWood 516252 · OlenveldSewerMaintenance 516263 · OlenveldPhase2 51636C · OlenveldBOTE 50FC4D · OlenveldAsAboveSoBelow 516251.
- **Penitus_Oculatus.esp:** zzzPO00 0012D1 · zzzPO01Informant 00A9C4 · zzzPORadiant01 003884 · zzzPO02Babette 004E19 · zzzPO03Cicero 008968 · zzzPO04Sanctuary 00CA4B · zzzPO05AmaundMotierre 00DFE9 · zzzPORadiant02 01B2C2 · zzzPORadiant03 01B2CB · zzzPORadiant04 01BD9F · zzzPORadiant05 01CDD1.
- **Tools of Kagrenac.esp:** TOK_QUST_KagrenacTools 21F221 · TOK_QUST_DialogueVonos 21F230 · TOK_QUST_DialogueYassour 21F231 · TOK_QUST_SunderVault 24CBF6.
- **MrissiTailOfTroubles.esp:** MRTstage1 17229C · MRTstage2 1A9E06 · MRTstage3 260646 · MRTstage5 2CBD17 · MRTstage6 2D5F8D · MRTstage7 2F4705 · MRTstage8 30DCA3. **Never** fire any OM row if MRTstage3Bad (554AD5) has started.
- **TheGiftofSaturalia.esp:** Sat_TheGiftofSaturalia 000D61 · Sat_Orphanage 0008AA · Sat_Laugh 0008D3 · Sat_Dog 0009A4 · Sat_Music 0009D2.
- **Lunar Guard Integrated - A Worldspace Addition.esp:** LGIKharriQuest 000805 (2 stages, no journal); K'harri 000801.
- **Immersive Encounters.esp:** SetteSoldiers01ImpObjA F6E6A8, ImpObjB F788D9, SonsObjA 0A3649, SonsObjB 0A876E · SetteBard01 A970B4 · WI_SetteCL02FollowUp 111FC8.
- **ksws07_quest.esm:** ksws07MainQuest 002086 · ksws07BookQuest 000BBA. **ksws03_quest.esp:** ksws03_main_quest 000AA2 · ksws03_tarot_quest 000AC8.
- **FalkreathShades.esp:** GRVEMainQuest02 4D2AF7. **Siege at Icemoth.esp:** HYORdunIcemothQST 5A079F · HYORBlackBook08Quest 59F97E.
- **Fists of Fury - Skyrim.esp:** FOFMorthalBrawlerQuest 149C95 · FOFRiftenBrawlerQuest 04C991.
- **College Of Winterhold - Quest Expansion.esp:** Cow_Breathing 000801 · Cow_Conjuration 00086F · Cow_Reading 000870.
- **Innocence Lost - Quest Expansion.esp:** DB01_OptionalObjectives 000836. **Caught Red Handed - Quest Expansion.esp:** FreeformRiften11b 000802. **TG Alternative Endings.esp:** TGAEDestroy 00083D. **Civil War Champions - Reduced Cut.esp:** CWCRQuest 000800. **EbonyBladeCurse.esp:** DA08MephalaHunt 000807. Vanilla DA08 04A37B and DA13 08998D (objectives from The Whispering Door / Only Cure expansions). **TasteOfDeath_Addon_Dialogue.esp:** madNamiraAddonQuest 000050.
- **CJ03Elroy.esp:** CJ03RotBelowMQ 02DA43. **Tree Contract Mod.esp:** TCMSheoTreeQuest 000009. **Hunt for the Spectre.esp:** HSHuntForSpectreQuest 000800. **Sithis Mod - Lovecraftian Inspired Quest.esp:** SMQuest 000892. **It Came from Akavir.esp:** KMMKamalQuest 000001.
- **Talos' Tease - Starting Quest.esp:** TT_TalosTease_QST 000001. **Slays-Many-Beasts Quest Mod.esp:** SMBMainQuest 000001. **Walks-Distant-Sands Quest Mod.esp:** WDSMainQuest 000003. **Darbalag - Quest Mod.esp:** DBQDarbalagQuest 000002. **Once We Were Here - Quest Mod.esp:** OWWHMainQuest 000002. **SaveTheIcerunner.esp:** STIJareeRaJailQuest 00082C · STIJareeRaRevengeQuest 000836. **PrisonerMod.esp:** PMAradellQuest 000007. **Dungeon Delver Mod.esp:** DDPikeQuest 000000.
- **Morskom.esp:** MEQuestMain 15A7F1. **An Evening With Angi.esp:** RES_AngiQuest 000800. **BecomeABard.esp:** _LP_BardSpyJobQuest 034EB7. **BardsRebornStudentofSong.esp:** BardsRebornBardsCollegeQuest 06673B. **Riften Expansion.esp:** RTBearheartVampireQuest 37F320. **Ivy Riverwood Overhaul.esp:** IvyAelaraMissingQuest 000006. **RiverwoodBandits.esp:** RWBGerdurQuest01 00090D. **Everdamned.esp:** ED_Mechanics_BlueBlood_Quest 47F5D9. **SkyrimFair.esp:** SkyrimFairPassport 0B0006. **SexLab-AmorousAdventures.esp:** SexLabAmorousAdventuresYsolda 057E2C. **The Book of Origins.esp:** Why_JoinCollegeQuest 000074 · Why_VisitorQuest_Stones 0000AB · Why_RecoverFromDwemerDungeon 000054. **SRC - All In One.esp:** SRC_IBH_SQ01 0A2982.

## Rows

### PART 1 - DAC0DA (20)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM1 | R L P | E OBJ:zDcdMq00 "Ask about the Dwemer giant at the Bards College theater" | after B10 |
| OM2 | X P | E OBJDONE:zDcdMq00 "Talk to <Alias=Monk>" (first one) | - |
| OM3 | K V P | E OBJDONE:zDcdMq00 "Enter the portal" (player now in the Sea of Causality) | after A2 |
| OM4 | G X | E OBJDONE:zDcdMq01 "Defeat <Alias=Sload>" | after X1 |
| OM5 | I L | E OBJDONE:zDcdMq01 "Defeat brainwashed people" | Lucien-Inigo intro done (JRLucienInigo) |
| OM6 | L P | E OBJ:zDcdMq02 "Eliminate time breaches" (after 2 min in the area) | - |
| OM7 | R P | E QD:zDcdMqBoss01 | - |
| OM8 | R K | E OBJDONE:zDcdMq03 "Break into the Numidium" | after B1 |
| OM9 | A R | E OBJDONE:zDcdMq04 "Avoid OR fight Ghost Choir 9" or "Avoid OR activate Mantella's defenses" | ASHE_REVEAL; one talk per run |
| OM10 | V R | E QD:zDcdMqBoss04 | Remi-Val intro done (HLIOValBanter Intro) |
| OM11 | X R | E QD:zDcdMqBoss05 | Remi-Xelzaz met (BPUFXelzazFollower Remi intro) and not fallen out (TRIGGERS.md section 3) |
| OM12 | K P | E zDcdSqYngol: first combat with Akashiya-Samon (003152/004B1D) ends, or OBJ "Talk to <Alias=Samon>" done | K_AKAVIRI |
| OM13 | G K | E zDcdSqYngol: first time Yngol (00316B) within 1500 units, after the "(Optional) Listen to the conversation" objective | after A1 |
| OM14 | C I | E OBJDONE:zDcdSqYngol "Build a fire to warm up Yngol" | after R13 |
| OM15 | P X | E OBJDONE:zDcdSqWorm first "(Optional) Talk to <Alias.ShortName=Vanus>", or Vanus Galerion 005183 first within 1000 units | - |
| OM16 | R L | E OBJDONE:zDcdSqWorm "Defeat Mannimarco's legion" | after B10 |
| OM17 | G C | E Crabbimarco (0048A0) first within 1000 units **[UNC: quest context]** | after R5 |
| OM18 | K A | E OBJDONE:zDcdSqWorm "Heal <Alias.ShortName=Vigil>" | ASHE_REVEAL |
| OM19 | X V | E QD:zDcdMqCheeseEnd, then player back in Tamriel | after X4 |
| OM20 | G K P | E Lokir of These Parts (00AA00) first within 1500 units | HELGEN; after A1 |

### PART 2 - OLENVELD (12)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM21 | L R | E QS:OlenveldWarmWelcome 50 | after B10 |
| OM22 | K G | E QS:OlenveldWarmWelcome 120 | after A1 |
| OM23 | V P | E QS:OlenveldEtherealComplications 100 | - |
| OM24 | S K | E QS:OlenveldFromBelowWeGrow 30 (in the Soul Cairn) | SERANA; DG_CAIRN |
| OM25 | V I | E QS:OlenveldHarshWinds 60 | - |
| OM26 | G R | E OBJ:OlenveldCityRenovations "Restore houses" (QS 60 done, 70 not) | Remi-Gore intro done (HLIOGoreBanter MarkarthIntro) |
| OM27 | C X | E QS:OlenveldBigWood 40 | after R18 |
| OM28 | X I | E QS:OlenveldSewerMaintenance 40 | after X6 |
| OM29 | A G | E QS:OlenveldSewerMaintenance 90, or OlenveldPhase2 stage 0 (map room) | ASHE_HIRED |
| OM30 | S P | E QS:OlenveldBOTE 60 | SERANA |
| OM31 | K P | E QS:OlenveldCityRenovations 120 (horn blown) | - |
| OM32 | L P | E QS:OlenveldAsAboveSoBelow 20 | - |

### PART 3 - PENITUS OCULATUS (8)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM33 | K L P | E QS:zzzPO00 1 | Kaidan-Lucien intro done (JRLucienFollowerKaidanScene1) |
| OM34 | X I | E QS:zzzPORadiant01 2 or QS:zzzPO01Informant 12 (first of either) | after X6 |
| OM35 | S G | E QD:zzzPO02Babette (or QS 2) | SERANA |
| OM36 | G I | E QS:zzzPO03Cicero 2 | after C2 |
| OM37 | R V | E QS:zzzPO04Sanctuary 3 | Remi-Val intro done (HLIOValBanter Intro) |
| OM38 | L P | E QS:zzzPO05AmaundMotierre 2 | - |
| OM39 | K V | E QS:zzzPORadiant03 2, zzzPORadiant04 2 or zzzPORadiant05 2 (first of any) | after A2 |
| OM40 | X A | E QS:zzzPORadiant02 2 | ASHE_REVEAL |

### PART 4 - TOOLS OF KAGRENAC (6)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM41 | R L | E QS:TOK_QUST_KagrenacTools 10 | after B10 |
| OM42 | X P | E OBJ:TOK_QUST_DialogueVonos "Find Vonos's Missing Ring" | - |
| OM43 | V C | E TOK_QUST_KagrenacTools QS 25 done or OBJ "Acquire Wraithguard" displayed, player on Solstheim | SOLST; Val-Redcap met **[UNC: no Val-Redcap meet talk traced; use first shared Free tick]** |
| OM44 | K P | E QS:TOK_QUST_KagrenacTools 40 | - |
| OM45 | L X | E QR:TOK_QUST_SunderVault and OBJ "Find the three Stanzas of Kagrenac" displayed, player inside the vault | Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| OM46 | X V | E QS:TOK_QUST_KagrenacTools 80 | after X4 |

### PART 5 - M'RISSI (7)  (all rows: MRTstage3Bad 554AD5 never started)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM47 | I K | E QS:MRTstage1 250, or OBJDONE "Kill the Thalmor soldiers!" | KaiandInigo stage >= 10 |
| OM48 | R P | E QS:MRTstage2 90 | - |
| OM49 | I G | E QS:MRTstage3 90 | after C2 |
| OM50 | G R | E QS:MRTstage5 20 (her first books read) | Remi-Gore intro done (HLIOGoreBanter MarkarthIntro); Gore reading arc started in Remi's mod **[UNC global]** |
| OM51 | C I | E QS:MRTstage6 220 (Lirry named) | after R13 |
| OM52 | S P | E QS:MRTstage7 90 | SERANA |
| OM53 | K P | E QS:MRTstage8 250 (kinship ceremony) | MRTstage8 125 NOT done and 999 NOT done |

### PART 6 - THE GIFT OF SATURALIA (5)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM54 | L C | E QS:Sat_TheGiftofSaturalia 5 | after R11 |
| OM55 | G K | E QS:Sat_Orphanage 12 | after A1 |
| OM56 | K P | E QR:Sat_Laugh, any stage 1..6 just set | K_ANY |
| OM57 | C G | E QS:Sat_Dog 5 | after R5 |
| OM58 | G X | E QS:Sat_Music 21 or 25 | after X1 |

### PART 7 - LUNAR GUARD (2)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM59 | K P | E IN:Lunar Guard worldspace, first arrival **[UNC worldspace FormID]** | K_ANY |
| OM60 | I C | E K'harri (000801) first within 1000 units, or LGIKharriQuest first stage set | after R13 |

### PART 8 - IMMERSIVE WORLD ENCOUNTERS, THE REST (3)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM61 | L G | E QS 30 or 40 on SetteSoldiers01ImpObjA/ImpObjB/SonsObjA/SonsObjB (first of any) | after L1 |
| OM62 | G R | E QS:SetteBard01 100 or 110, or quest completed | Remi-Gore intro done |
| OM63 | R V | E QS:WI_SetteCL02FollowUp 10 (before 100/200/210) | Remi-Val intro done |

### PART 9 - FROZEN HEART, BABA YAGA, GRAVEWIND (7)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM64 | V R | E QS:ksws07MainQuest 200 | Remi-Val intro done |
| OM65 | L P | E QS:ksws07MainQuest 340 | - |
| OM66 | X P | E QS:ksws07BookQuest 100 | - |
| OM67 | C K | E QS:ksws03_main_quest 300 (hut found), or Witch's Hut actor 000816 first within 2000 units | after R1 |
| OM68 | V P | E QS:ksws03_tarot_quest 300 | - |
| OM69 | S I | E QS:GRVEMainQuest02 10 | SERANA |
| OM70 | K P | E QS:GRVEMainQuest02 50 | - |

### PART 10 - ICEMOTH, FISTS OF FURY, COLLEGE (7)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM71 | V G | E QS:HYORdunIcemothQST 10, then 2 min later on the road | after A3 |
| OM72 | V P | E QS:HYORBlackBook08Quest 10, after the player leaves Apocrypha | NOT_VAL_FATHIS |
| OM73 | G L | E QS:FOFMorthalBrawlerQuest 20 (first ghost) | after L1 |
| OM74 | K R | E QS:FOFRiftenBrawlerQuest 50 | after B1 |
| OM75 | R P | E QS:Cow_Breathing 30 | MG_JOIN |
| OM76 | L P | E QS:Cow_Conjuration 20 | MG_JOIN |
| OM77 | G P | E QS:Cow_Reading 20 | MG_JOIN |

### PART 11 - VANILLA QUESTS, EXPANDED (12)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM78 | X K | E DB01_OptionalObjectives objective "Witness Grelod's arrest" completed | after C3 |
| OM79 | G V | E QD:FreeformRiften11b | after A3 |
| OM80 | S V | E QD:TGAEDestroy with its optional "Bring the Skeleton Key to Vigilant Tarelon" objective completed **[UNC objective index]** | SERANA |
| OM81 | K G | E QD:CWCRQuest | after A1 |
| OM82 | R V | E QS:DA08MephalaHunt 30 | Remi-Val intro done |
| OM83 | I P | E QS:DA08MephalaHunt 20 | - |
| OM84 | L G | E DA08 objective "Speak to Nelkir OR warn the Jarl" completed by the warn branch (player talked to Balgruuf about the door before Nelkir) **[UNC: branch stage]** | after L1 |
| OM85 | I X | E DA13 objective "Kill or Talk to Orchendor" completed with Orchendor still alive at that moment **[UNC branch flag]** | after X6 |
| OM86 | G C | E QS:madNamiraAddonQuest 20 | after R5 |
| OM87 | K P | E QS:madNamiraAddonQuest 40 | - |
| OM88 | G R | E QS:CJ03RotBelowMQ 30 | Remi-Gore intro done |
| OM89 | X L | E QS:CJ03RotBelowMQ 130 | Xelzaz-Lucien intro done |

### PART 12 - SMALL QUESTS ON THE ROAD (18)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM90 | I K | E QS:TCMSheoTreeQuest 15 | KaiandInigo stage >= 10 |
| OM91 | C G | E QS:TCMSheoTreeQuest 45 | after R5; after OM90 |
| OM92 | A V | E QS:HSHuntForSpectreQuest 25 or 31 (amulet hunt running) | ASHE_HIRED |
| OM93 | K I | E QS:HSHuntForSpectreQuest 45 or 50 (quest over, any ending), next CAMP | BRYNJAR; KaiandInigo stage >= 10 |
| OM94 | P X | E QS:SMQuest 5 | - |
| OM95 | L S | E QS:SMQuest 35 | SERANA |
| OM96 | L K | E QS:KMMKamalQuest 5 | K_AKAVIRI; Kaidan-Lucien intro done |
| OM97 | G A | E QS:KMMKamalQuest 15 | ASHE_REVEAL |
| OM98 | V G | E QS:TT_TalosTease_QST 10 | after A3 |
| OM99 | X G | E SMBMainQuest stage 15 or 25 or 35 set (ONCE_PER_MEET) | after X1 |
| OM100 | V I | E WDSMainQuest stage 15, 25 or 35 set, player in a CITY (ONCE_PER_MEET) | - |
| OM101 | I R | E DBQDarbalagQuest any meeting stage after 5 (ONCE_PER_MEET) **[UNC stages]** | after B6 |
| OM102 | L R | E OWWHMainQuest stage 15, 25 or 35 set (ONCE_PER_MEET) | after B10 |
| OM103 | V I | E STIJareeRaJailQuest started or STIJareeRaRevengeQuest completed (first of either) **[UNC stages]** | - |
| OM104 | K P | E QS:PMAradellQuest 5 | - |
| OM105 | G L | E DDPikeQuest stage 5 set | after L1 |
| OM106 | S R | E QS:MEQuestMain 25 | SERANA |
| OM107 | R K | E MEQuestMain completed (ghost vanquished) | after B1 |

### PART 13 - BARDS, TOWNS AND HOMES (8)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM108 | I K | E QS:RES_AngiQuest 10, after the player leaves Angi's cabin | KaiandInigo stage >= 10 |
| OM109 | V P | E _LP_BardSpyJobQuest objective "Tell <Alias=Handler> what you learned" completed (first time) | - |
| OM110 | L P | E QR:BardsRebornBardsCollegeQuest, stage 20..110 set this tick, player in the Bards College | - |
| OM111 | X S | E QS:RTBearheartVampireQuest 30 or 35 (first of either) | SERANA |
| OM112 | C R | E QS:IvyAelaraMissingQuest 0 or 10, player within 3000 units of Anise's cabin | Remi-Redcap met (Redcap's Remi intro) **[UNC quest]** |
| OM113 | G I | E QS:RWBGerdurQuest01 40 | after C2 |
| OM114 | S P | E QS:ED_Mechanics_BlueBlood_Quest 100 | PC_VAMP; SERANA |
| OM115 | K G | E QS:SkyrimFairPassport 20 | after A1 |

### PART 14 - ORIGINS AND THE REST (5)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| OM116 | R V | E SexLabAmorousAdventuresYsolda first stage set, player in Whiterun | Remi-Val intro done |
| OM117 | K P | T | ORIGIN:Why_JoinCollegeQuest; MG_JOIN |
| OM118 | L P | T WILD | ORIGIN:Why_VisitorQuest_Stones; at least 7 standing stone objectives done **[UNC objective count]** |
| OM119 | R P | E ORIGIN:Why_RecoverFromDwemerDungeon stage 10, first Free tick with Remi | - |
| OM120 | A L | E QS:SRC_IBH_SQ01 50 or 100 | ASHE_HIRED |
