# Triggers - 14 CREATION CLUB (prefix CC, 180 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\14 CREATION CLUB.txt`
Sources: `research\content\dlc_cc_missives_3dnpc.md` section D, `research\content\00_inventory.md` section 3, `research\triggers\kaidan_block.md`, Gray Cowl journal text read with houseCARL (read-only, 2026-10-18).
Format and base gate codes: `TRIGGERS.md` sections 4-5. Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, + Luna (player; no actor check).

Shorthand (from the research file): `Done(Q,s)` = GetStageDone Q s == 1. `Run(Q)` = GetQuestRunning. `Comp(Q)` = GetQuestCompleted. `In(L)` = player IsInLocation L. `WS(W)` = GetInWorldspace W.
**[unconfirmed]** = stage/record not verified against the journal text or record at build; check before shipping.

## New gate codes used in this file

| Code | Test |
|---|---|
| `KMD_DONE` | Kaidan's own Dagon arc is over: `GetStageDone KMDQuest 1CD8FD:0Kaidan.esp 200 == 1` (ShutDownStage set by Rosalind's death). Fallback `Comp(KMDQuest)`. **Required on every talk where Kaidan speaks about the Blooded Dawn.** [unconfirmed: confirm 200 is reached on every KMD branch, incl. KR2] |
| `NOT_KMD` | `KMD_DONE` false. Kaidan deflects only, says nothing about his past. |
| `CAUSE` | quest `ccBGSSSE067_Quest 06BFC1:ccbgssse067-daedinv.esm` |
| `CAUSE2` | `ccBGSSSE067_Quest2 19952A:ccbgssse067-daedinv.esm` (The Consequences) |
| `DEADLANDS` | `WS(ccBGSSSE067DeadlandsWorld 0E1592:ccbgssse067-daedinv.esm)` or `In(033F39)` |
| `GOT` | `ccASVSSE001_Quest 000CC3:ccasvsse001-almsivi.esm` (Ghosts of the Tribunal); side jobs QuestA 000CA0, QuestB 000F19, QuestC 000F1A, QuestD 00117A, QuestE 0990EF |
| `FISH:<q>` | quest in `ccBGSSSE001-Fish.esm` (IDs per row) |
| `FISHSTART` | `Done(ccBGSSSE001_Start_MQ1 0009D3,200)` [unconfirmed: complete stage] |
| `GC` | `manny_GF_MQ 001E61:Gray Fox Cowl.esm`. Journal: 10 vision · 160 escaped Coldharbour · 170 desert, met Arenar · 300 in Hammerfell (Lady Syloria) · 310 inside the Mausoleum of the Champion of Cyrodiil · 700 got the Cowl · 999 "the legendary Gray Cowl" |
| `LUC_PRESENT` | Lucien is Free (talk is about Lucien's own CC reaction; he does not speak) |
| `CC_ITEM:<x>` | player has / wears the item (GetItemCount or WornHasKeyword). FormIDs to be pulled at build [unconfirmed] |

## Silence windows for this file (add to WorldQuiet while in these states)
- `DEADLANDS` while `Run(CAUSE2)`: only CC10, CC11, CC12 may fire (AFTERFIGHT barks).
- `CAUSE` stage 220 until 230 or 240 is done (the Sigil/Welkynd choice).
- `BGSSSE018_ShadowrendQuest 00081C:ccbgssse018-shadowrend.esl` stages 15..20 (shadow duel).
- `ccKRTSSE001_QuestPower 000A5E:cckrtsse001_altar.esl` running and `In(000F54)` (Bittercup pit, followers absent).
- `ccBGSSSE001_FishingSystemQuest 033A57` active cast state: only short fishing talks (CC52, CC53), and only between casts [unconfirmed proxy].
- `ccBGSSSE025_QuestB 000913:ccBGSSSE025-AdvDSGS.esm` 30..40 (Thoron's ritual).
- `ccFFBSSE001_Quest 000927:ccffbsse001-imperialdragon.esl` 150..160 and 250..260 (champion duel).
- `GOT` stages 200..250 (posing as Her Hands inside the temple).
- Gray Cowl: player in Coldharbour or the Hammerfell worldspace of `Gray Fox Cowl.esm` (followers are not there) [unconfirmed worldspace IDs].

## Table

### Part 1 - The Cause
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC1 | L K I | T | `Done(CAUSE,20)` courier letter; `NOT_KMD` |
| CC2 | G V | T | `Done(CAUSE,30)` Skorvild found dead [unconfirmed: murder may be logged at 50] |
| CC3 | R X | E arrival `In(Rielle 015889:ccbgssse067-daedinv.esm)` | `Run(CAUSE)` |
| CC4 | C I | E AFTERFIGHT | `Done(CAUSE,130)` lich dead |
| CC5 | G K | T or E CAMP | `Done(CAUSE,60)` "the Mythic Dawn have reemerged"; `NOT_KMD` |
| CC6 | V I | E AFTERFIGHT | `Done(CAUSE,50)` assassins |
| CC7 | X R | E arrival `In(Red Scar Cavern 033F35:ccbgssse067-daedinv.esm)` | `Run(CAUSE)` |
| CC8 | L K | E on stage set | `Done(CAUSE,170)` gate opened (Vonos dead); `CAUSE` < 220; not `DEADLANDS`; `NOT_KMD` |
| CC9 | C G | E on stage set | `Done(CAUSE,170)`; not yet in `DEADLANDS` |
| CC10 | V G | E AFTERFIGHT | in `DEADLANDS` |
| CC11 | X I | E AFTERFIGHT | in `DEADLANDS` |
| CC12 | K | E AFTERFIGHT | in `DEADLANDS`; `K_TOG+` |
| CC13 | R X | T | `Done(CAUSE,230)` gate closed |
| CC14 | V K G | T | `Done(CAUSE,240)` gate open |
| CC15 | R V | T | `Comp(CAUSE2)` / `Done(CAUSE2,1000)` Scourge and Torment |
| CC16 | I G | E on stage set or AFTERFIGHT | `CAUSE2` Valkynaz killed (210..300 range) [unconfirmed stage] |
| CC17 | I K | E CAMP | `Comp(CAUSE)` (250 summary); `NOT_KMD` |
| CC18 | K | T | `Comp(CAUSE)`; `K_TOG+`; `NOT_KMD` |
| CC19 | G K | T | `Comp(CAUSE)`; `KMD_DONE` |
| CC20 | L K | T | `Comp(CAUSE)`; `KMD_DONE`; after:CC1 |

### Part 2 - Ghosts of the Tribunal
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC21 | X V | T or E CITY Raven Rock | `Done(GOT,10)` |
| CC22 | X R | E arrival `In(000C82:ccasvsse001-almsivi.esm)` temple | `Done(GOT,10)`; not `GOT` 200..250 |
| CC23 | C I | E AFTERFIGHT (Ordinator ghost) | `Done(GOT,10)` |
| CC24 | C X | T, `SOLST` worldspace | `Done(GOT,10)` |
| CC25 | V R | T | `Done(GOT,10)`; after:CC22 [unconfirmed: stage where the Masks are named] |
| CC26 | V G | T | `Done(QuestA 000CA0,1000)` Buyer Beware |
| CC27 | X | T | `Done(QuestB 000F19,1000)` Her Word Against Theirs |
| CC28 | I X | T | `Done(QuestC 000F1A,40)` Careless Curation |
| CC29 | K X | E AFTERFIGHT | `Run(QuestD 00117A)` after ash-zombie attack [unconfirmed stage] |
| CC30 | X V | T | `Done(QuestD 00117A,100)` Mask of Dagoth Ur |
| CC31 | R C | T | `Done(QuestE 0990EF,100)` Trueflame |
| CC32 | X G | T | `Done(GOT,120)` attacked the Matriarch |
| CC33 | X V | T | `Done(GOT,300)` played Her Hands to the end; not `Done(GOT,120)` |
| CC34 | R K | T | `K_CRUSH`; `CC_ITEM:Ordinator armour worn` [unconfirmed FormIDs] |
| CC35 | I G | T | `Comp(GOT)` / `Done(GOT,1000)` |
| CC36 | X | E NIGHT | `Comp(GOT)` |

### Part 3 - Fishing (all quests in ccBGSSSE001-Fish.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC37 | G I | T | `FISHSTART` (Start_MQ1 0009D3 "First Catch") |
| CC38 | I X | T | `Done(Start_MQ2 0009DB,?)` Angler Acquaintances, met Swims-In-Deep-Water [unconfirmed stage] |
| CC39 | K G | T or E RAIN | `Done(Fish_MQ2 0009EB,200)` Caught in the Rain |
| CC40 | X C | T or E SNOW | `Done(Fish_MQ3 0009E8,200)` Frozen Fish |
| CC41 | I R | T | `Done(Fish_MQ4 0009DD,200)` Darkest Depths |
| CC42 | G K | E on stage set | `Done(Fish_MQ5 0009DC,200)` Fishing Legend |
| CC43 | C K | T | `Done(Crab_MQ1 0009D4,200)` In A Pinch |
| CC44 | V I | T | `Done(Crab_MQ4 0009E9,2000)` Wave Breaker |
| CC45 | K R | T | `Done(Misc_Windhelm 0009D5,200)` Tusked Terror |
| CC46 | G X | T | `Done(Misc_Morthal 0009E4,200)` No Contest |
| CC47 | R | T | `Done(Misc_Dwarven 000AD6,200)` Beneath Bronze Waters |
| CC48 | I X | T | `Done(Misc_Khajiit 0009E2,200)` Spirits Away |
| CC49 | I G | T | `Done(Misc_WhiterunPartTwo 0009D7,200)` Mila's goldfish [unconfirmed which Whiterun part is Mila] |
| CC50 | I K | T | `Done(Misc_Falkreath 0009EC,200)` Clear-Headed |
| CC51 | X V | T | `Done(Misc_Solitude 0009E3,200)` The Ultimate Feast [unconfirmed quest-to-name match] |
| CC52 | G | E WATER | `FISHSTART` |
| CC53 | G K | E WATER | `FISHSTART`; `K_CRUSH` |

### Part 4 - The Gray Cowl of Nocturnal (Gray Fox Cowl.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC54 | I R | T | `Done(GC,10)` vision |
| CC55 | G K | T | `Done(GC,160)` or `Done(manny_GF_ColdharbourQuest 01F56B,255)` escaped Coldharbour; back in Skyrim |
| CC56 | G V | T | `Done(GC,300)`; back in Tamriel worldspace |
| CC57 | L I | T | `Done(GC,310)` Mausoleum of the Champion of Cyrodiil; back in Skyrim |
| CC58 | V R | T | `Done(GC,999)` |
| CC59 | K R | T | `Done(GC,999)`; `CC_ITEM:Gray Cowl worn` |
| CC60 | G I | T | `Done(manny_GF_Sadraaka 026AE8,30)` |
| CC61 | X | T | `Done(manny_GF_IrlavExperiment 03039F,100)` |
| CC62 | V | E CITY:Solitude or T | `Done(manny_GF_Farewell 01CFA7,20)` escorted Seviana and Luvien |
| CC63 | G C | T | `Done(manny_GF_MiscQuestShantaFilibb 050159,200)`; after:CC56 |

### Part 5 - Saints and Seducers (ccBGSSSE025-AdvDSGS.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC64 | I K | T | `Done(QuestA 000912,100)` rumour |
| CC65 | C X | E AFTERFIGHT | `Run(QuestA 000912)` stage 400..560 |
| CC66 | V G | T | `Done(QuestA 000912,2000)` |
| CC67 | V X | T | `Done(QuestB 000913,10)` Thoron identified [unconfirmed stage] |
| CC68 | R C | T | `Done(QuestB 000913,200)` Sword of Jyggalag |
| CC69 | R I | T | `Comp(EC_SS_ElytraPetAcquisition_Dementia 0010C0)` or `Comp(..._Mania 0010C3)` |
| CC70 | G V | T | `StaadaQuest 198277` met Staada [unconfirmed stage] |

### Part 6 - Forgotten Seasons (cctwbsse001-puzzledungeon.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC71 | R G | E arrival `In(Vardnknd 003901)` | — |
| CC72 | X I | E arrival `In(0038FF winter)` or `In(003902 summer)` | — |
| CC73 | R | T | `Done(DLCDwarvenPuzzleDungeonQuest01 0038D9,5)` [unconfirmed; research shows journal 1-11, complete at 5] |
| CC74 | K R | E in Vardnknd | `LUC_PRESENT` |
| CC75 | C G | T | `Comp(DLCDwarvenPuzzleDungeonHorseQuest 0038DA)` [unconfirmed stage 3] |
| CC76 | V R | T | `Comp(DLCDwarvenPuzzleDungeonCrownQuest 0038DB)` |
| CC77 | X | T | `Run(Quest01 0038D9)` after the journal is read [unconfirmed stage] |
| CC78 | R K | T | `Comp(Quest01 0038D9)`; `K_TOG+` |

### Part 7 - Goblins (ccbgssse040-advobgobs.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC79 | G C | E AFTERFIGHT:goblin or first sight | `Done(ccBGSSSE040_Quest 0009B6,8)` |
| CC80 | V C | T | `Done(0009B6,8)`; after:CC79 |
| CC81 | I C | T | `Run(0009B6)` after the arena at Gromm's Pass `000D13` [unconfirmed stage] |
| CC82 | G | T | `Done(0009B6,200)` (Orc shaman dealt with) |
| CC83 | C X | T | `Done(0009B6,200)`; `RC_REDGOD` |
| CC84 | C K | T | `Done(0009B6,200)`; player has a goblin totem [unconfirmed item] |
| CC85 | K C | T | `Done(0009B6,200)`; `LUC_PRESENT` |
| CC86 | R C | T | Redcap's own Goblins patch quest done (`FARGRedcapCCGoblinsPatch.esp`, Spear of Bitter Mercy) [unconfirmed quest ID] |

### Part 8 - Umbra (ccbgssse016-umbra.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC87 | K G | E arrival `In(Champion's Rest 006C48)` | — |
| CC88 | V | T | `Done(ccBGSSSE016_UmbraMainQuest 0021B6,40)` |
| CC89 | I R | T | `Done(0021B6,200)`; `CC_ITEM:Umbra` |
| CC90 | X C | T | `Done(0021B6,200)`; `LUC_PRESENT` |
| CC91 | K X | T | `Done(0021B6,200)`; `K_TOG+` |

### Part 9 - Plague of the Dead (ccbgssse003-zombies.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC92 | R K | T | `Done(ccBGSSSE003_ZombieQuestStartEncounter 00083D,10)` letter |
| CC93 | I G | E AFTERFIGHT:risen dead | `Done(00083D,10)` |
| CC94 | X C | T | `Done(00083D,10)` |
| CC95 | R | T | `Done(00083D,40)` |
| CC96 | V I | E AFTERFIGHT:risen dead (B003_WE encounter) | `Done(00083D,10)` |

### Part 10 - Bittercup (cckrtsse001_altar.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC97 | C K | T | `Run(ccKRTSSE001_zQuest 000D63)` after first drink [unconfirmed stage] |
| CC98 | V R | T | `Done(ccKRTSSE001_QuestFortune 000A90,1000)` |
| CC99 | G K | T | `Done(ccKRTSSE001_QuestPower 000A5E,100)`; not `In(000F54)` |
| CC100 | I | T | `Done(000D63,200)` [unconfirmed: island branch] |
| CC101 | X | T | first cup drunk (any of the three started) |
| CC102 | L G | T | `Done(000D63,200)` |

### Part 11 - Wild Horses (ccbgssse034-mntuni.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC103 | G | T | any `ccBGSSSE034_Misc_Horse0x` complete or `Run(WildHorsesQuest 000D65)` past first tame [unconfirmed] |
| CC104 | I L | T | as CC103; `LUC_ADMIT` |
| CC105 | C V | T | as CC103 |
| CC106 | R K | E on stage set | `Done(ccBGSSSE034_UnicornQuest 000DE8,20)` |
| CC107 | X R | T | `Done(000DE8,20)` |
| CC108 | V K | T | `Done(000DE8,20)`; `K_CRUSH` |

### Part 12 - Divine Crusader (ccmtysse001-knightsofthenine.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC109 | I K | T | `Run(ccMTYSSE001_StartupQuest_Alt 00083C)` stage 0..99 |
| CC110 | G V | T | `CC_ITEM:Crusader's Relics worn` |
| CC111 | R | T | `Run(ccMTYSSE001_Quest 000865)` stage 10..99 |
| CC112 | X I | T | `Run(000865)` stage 10..99 |
| CC113 | V K | T | `Done(000865,100)` |
| CC114 | G K | E arrival at a Shrine of Kynareth | `Run(000865)` [unconfirmed shrine refs] |

### Part 13 - Homes and the farm
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC115 | G K | E arrival Tundra Homestead `001022`/`000F1E:cceejsse001-hstead.esm` | first visit |
| CC116 | K | E HOUSE Tundra Homestead | `K_TOG+` |
| CC117 | C I | E HOUSE Tundra Homestead | — |
| CC118 | X V | E HOUSE Tundra Homestead | — |
| CC119 | R V | E arrival `000D41:cceejsse003-hollow.esl` | `Done(ccEEJSSE003_HouseQuest 00082A,100)` |
| CC120 | K I | E in Shadowfoot Sanctum | `Done(00082A,100)` |
| CC121 | L G | E in Shadowfoot Sanctum | `Done(00082A,100)` |
| CC122 | V K | T | `Run(ccVSVSSE004_MainQuest 000D28)` after meeting the ghosts; `BRYNJAR` (Kaidan's line) |
| CC123 | G I | T | `Run(000D28)` after the son's fate is known [unconfirmed stage] |
| CC124 | R | T | `Done(000D28,1000)` |
| CC125 | G K | E at farm `000D36` | `Done(ccVSVSSE004_RestoreFarmQuest 000EB7,500)` |
| CC126 | X C | E at farm `000D36` | `Done(000D28,1000)` |

### Part 14 - Smaller Creations
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC127 | X I | E near a Khajiit caravan merchant | Rare Curios active (`00084D:ccbgssse037-curios.esl` running) |
| CC128 | R | T | as CC127; player has any curio ingredient [unconfirmed list] |
| CC129 | I V | E near a Khajiit caravan | as CC127 |
| CC130 | I G | T | `Done(ccBGSSSE004_Quest 00080C,1000)` Ruin's Edge |
| CC131 | V X | T | `Done(00080C,1000)`; `LUC_PRESENT` |
| CC132 | G | T | `Done(00080C,100)` map; < 1000 |
| CC133 | I | T | `Done(BGSSSE018_ShadowrendQuest 00081C,5)`; < 15 |
| CC134 | G K | T | `Comp(00081C)` (stage 20) |
| CC135 | V R | T | `Comp(00081C)` |
| CC136 | X | T | `Comp(00081C)` |
| CC137 | K | T | `CC_ITEM:Staff of Sheogorath` (`ccbgssse019-staffofsheogorath.esl`, quest 000822 has no journal) |
| CC138 | C G | T | as CC137 |
| CC139 | I R | T | as CC137 (equipped) |
| CC140 | K X | T | `CC_ITEM:Lord's Mail` (`ccbgssse021-lordsmail.esl`, quest 000813 no journal) |
| CC141 | V | T | as CC140 |
| CC142 | R I | T | as CC140; `LUC_PRESENT` |
| CC143 | G V | T | `Done(ccBGSSSE006_Quest 000805:ccbgssse006-stendarshammer.esl,1000)` |
| CC144 | R K | T or E CITY:Markarth | `Done(000805,100)`; < 1000 |
| CC145 | I X | E at the hammer crater [unconfirmed location] | `Done(000805,100)` |
| CC146 | V R | T | `Done(ccBGSSSE045_Quest 000823:ccbgssse045-hasedoki.esl,5)` ledger |
| CC147 | K I | E arrival Brittleshin Pass | `Run(000823)` |
| CC148 | X | T | `Done(000823,200)` |
| CC149 | K G | E arrival Skytemple Ruins | `Run(ccPEWSSE002_Quest 000819:ccpewsse002-armsofchaos.esl)` |
| CC150 | L R | T | `Run(000819)` after the third Sigil Stone [unconfirmed stage] |
| CC151 | X C | E AFTERFIGHT at Skytemple Ruins | `Run(000819)` |
| CC152 | R | E in Hob's Fall Cave | `Done(ccBGSSSE014_SpellPack_StartupQuest 00083C:ccbgssse014-spellpack01.esl,10)` |
| CC153 | K | E in Hob's Fall Cave | as CC152; `K_CRUSH` |
| CC154 | G | T | as CC152; Gore can read (`GORE_BAIL` or Vigilant reading done) [unconfirmed] |
| CC155 | I V | T | `Done(ccBGSSSE013_AquisitionQuest 000F18:ccbgssse013-dawnfang.esl,200)` |
| CC156 | R K | T | `Done(000F18,0..130)` met the ghost woman [unconfirmed stage] |
| CC157 | G X | T | `Comp(ccBGSSSE013_BloodthirstQuest 000CA6)` |
| CC158 | G | T | `Done(ccEDHSSE003_Quest 00088C:ccedhsse003-redguard.esl,20)` brawl |
| CC159 | K X | T | `Done(00088C,110)` caravan assault |
| CC160 | V I | T | `Done(00088C,62)` spies |
| CC161 | I G | T | `Done(ccBGSSSE069_Quest 000805:ccbgssse069-contest.esl,1)`; < 100 |
| CC162 | I C | E AFTERFIGHT in Cronvangr Cave | `Done(000805,100)` |
| CC163 | X V | E AFTERFIGHT in Cronvangr Cave | `Done(000805,100)` |
| CC164 | R V | T | `Done(ccBGSSSE043_VampireHunterQuest 00089E:ccbgssse043-crosselv.esl,200)` |
| CC165 | R K | T | player has an elite/enhanced crossbow [unconfirmed item list] |
| CC166 | V G | T | `Done(00089E,200)` |
| CC167 | X I | T | `Run(ccMTYSSE002_Quest 000926:ccmtysse002-ve.esl)` stage 10..99; **never pair with Gore here (Gore - Vigilant collision)** |
| CC168 | V C | T | `Done(000926,100)`; `CC_ITEM:Vigil Enforcer worn` |
| CC169 | R I | T | `Done(ccEDHSSE002_Quest 000800:ccedhsse002-splkntset.esl,10)` |
| CC170 | K | T | `Done(000800,1500)` or `Done(000800,2000)` |
| CC171 | X | T | `Done(ccFFBSSE001_Quest 000927,270)` + `CW_SONS` [unconfirmed which of 170/270 is the Stormcloak side] |
| CC172 | V L | T | `Done(000927,170)` + `CW_IMP` [unconfirmed side mapping] |
| CC173 | R | T | Necromantic Grimoire read (`0008B7:ccvsvsse003-necroarts.esl`) [unconfirmed stage] |
| CC174 | K X | T | as CC173; after:CC173 |
| CC175 | K G | E in Rebel's Cairn | `cccbhsse001-gaunt.esl` quest `000834` running/done [unconfirmed] |
| CC176 | C G | T | `CC_ITEM:Red Eagle gauntlets` [unconfirmed] |
| CC177 | C X | T in `SOLST` | `Run(ccBGSSSE041_Quest 00081C:ccbgssse041-netchleather.esl)` |
| CC178 | V | T | `Comp(00081C:ccbgssse041-netchleather.esl)` |
| CC179 | R K | T | any `ccBGSSSE05x/06x_Quest` alt-armour quest complete + set worn [unconfirmed] |
| CC180 | I | T | `Comp(ccEDHSSE001_CraftsmanEncounterQuest 00082F:ccedhsse001-norjewel.esl)` |

## Notes for the build
- Kaidan and The Cause: CC1, CC5, CC8, CC17, CC18 carry `NOT_KMD` so they never play after he has told his story (they would read as him hiding it again). CC19 and CC20 carry `KMD_DONE`. No other CC talk mentions his past.
- Dead Man's Dread (`ccBGSSSE031-AdvCyrus.esm`) is listed in Skyrim.ccc but is not in the active implicit CC list, so it has no talks. Same for Gallows Hall, Bloodchill Manor, Myrwatch, Hendraheim, Gray Cowl CC (`ccBGSSSE020`); the Gray Cowl talks are for the big mod `Gray Fox Cowl.esm`.
- Survival Mode is disabled by the Authoria patch: no survival talks.
- Lucien has his own CC patches for Stendarr's Hammer, Lord's Mail, Plague, Saturalia, Umbra, Forgotten Seasons, Goblins, Rare Curios, Ruin's Edge, S&S, Shadowrend, Staff of Sheogorath, Tundra Homestead. Here he only speaks in CC1, CC8, CC20 (The Cause), CC57 (Gray Cowl), CC102 (Bittercup), CC104 (Wild Horses), CC121 (Shadowfoot), CC150 (Arms of Chaos), CC172 (CW Champions); on his covered CCs the others react to him (CC68, CC74, CC85, CC90, CC131, CC142).
