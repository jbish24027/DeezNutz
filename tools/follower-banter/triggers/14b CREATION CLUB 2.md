# Triggers - 14b CREATION CLUB 2 (prefix CC, CC181-CC330, 150 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\14b CREATION CLUB 2.txt`.
Continues `triggers\14 CREATION CLUB.md` (CC1-CC180). Every gate code, FormID, silence window and note in that file applies here unchanged (`CAUSE`, `CAUSE2`, `DEADLANDS`, `GOT`, `FISH:<q>`, `FISHSTART`, `GC`, `KMD_DONE`, `NOT_KMD`, `LUC_PRESENT`, `CC_ITEM:<x>`, `Done/Run/Comp/In/WS`).
Sources: `research\content\dlc_cc_missives_3dnpc.md` section D, `research\content\00_inventory.md` section 3, `research\bibles\*.md`, `triggers\20 DAWNGUARD.md` (Serana/Ashe Free rows and the `SERANA`, `SER_VAMP`, `SER_CURED`, `ASHE_REVEAL`, `ASHE_Q1` codes), `TRIGGERS.md` sections 2-4.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`), section 3 (`Free`) and the CC silence list in `14 CREATION CLUB.md`. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but a talk with P lines needs the player not in dialogue).
Type: T = timer, E = event.

## 1. File-wide rules
- **Serana rows** (S) need `SERANA` and her Free row (20 DAWNGUARD.md section 1). Rows marked `SER_VAMP` need her still a vampire; `SER_CURED` needs her cured.
- **Ashe rows** (A) need `ASHE_HIRED`, `ASHE_REVEAL` and her Free row, even where the row lists only a later gate. Respect her `bConfigVarIdles` toggle and her silence list (49 ASHE.md).
- **Kaidan and The Cause:** CC185, CC191 carry `NOT_KMD`; CC195, CC196, CC197 carry `KMD_DONE`. No other row here touches his past.
- **Lucien:** he speaks only on Creations he has no patch for (CC186, CC192, CC204, CC211, CC212, CC218, CC257, CC284, CC316). Rows marked `LUC_PRESENT` are the others talking about his own CC lines; he must be Free but does not speak.
- **Gore and Stendarr / the Vigilants:** no Gore row on Stendarr's Hammer or Vigil Enforcer (Gore - Vigilant collision).
- **Redcap:** no row has anyone call him a goblin.
- **Inactive Creations:** Bloodchill Manor, Gallows Hall, Hendraheim, Myrwatch, Nchuanthumz, Chrysamere, Arcane Archer, Pets of Skyrim are not in the load order: no rows. Survival Mode is disabled: no rows.
- **Fishing:** obey 14 CREATION CLUB.md's fishing silence (only between casts). Fishing rows here are T or WATER, never mid-cast.
- **Deadlands barks** (CC186-CC190) are added to the `DEADLANDS` allow-list (with CC10-CC12): only these may fire in the Deadlands while `Run(CAUSE2)`.

## 2. New codes used here
| Code | Test |
|---|---|
| `ALT:<nn>` | alternative-armour quest `ccBGSSSE0nn_Quest` in `ccbgssse0nn-ba_<set>.esl` (FormIDs in 00_inventory.md section 3). `ALT:<nn> done` = `Comp(ccBGSSSE0nn_Quest)`. [UNC: completion stages not traced; use GetQuestCompleted] |
| `WEAR:<set>` | player wears a piece of the set (WornHasKeyword or GetEquipped on the set's cuirass record from that plugin). [UNC: FormIDs to pull at build] |
| `GORE_SASEC` | Gore's own Sheogorath quest `HD1Madness` (Gore - SaSEC.esp) completed. [UNC FormID/stage] |
| `HORSE_ARMOR` | player's current horse wears an item from `ccbgssse011-hrsarmrelvn.esl` or `ccbgssse012-hrsarmrstl.esl`. [UNC: check via the horse ref's GetEquipped / the CC's own horse-armour script] |
| `CURIOS` | `Rare Curios` startup quest `00084D:ccbgssse037-curios.esl` running and the player has bought at least one curio ingredient. [UNC item list] |
| `SATURALIA_M` | `Done(ccVSVSSE001_MainQuest 00082B:ccvsvsse001-winter.esl,10)` and `GameMonth == 11` (Evening Star). |
| `NOT_K_AKAVIRI` | as TRIGGERS rows: `GetStageDone KINV(0B3032:0Kaidan.esp) 50 == 0`. |

## 3. Table

### Part 1 - The Cause, round two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC181 | G V | T | `Done(CAUSE,130)` lich dead / stone taken; not `Done(CAUSE,170)` [UNC: stage the Great Welkynd Stone is taken] |
| CC182 | A R P | E in Rielle `015889:ccbgssse067-daedinv.esm` | `Run(CAUSE)`; `ASHE_REVEAL` |
| CC183 | P R I | E in Red Scar Cavern `033F35` or T after leaving it | `Run(CAUSE)`, `Done(CAUSE,110)` [UNC: stage for the cavern papers] |
| CC184 | S X | T | `Done(CAUSE,60)`; `SERANA` |
| CC185 | S K | T | `Done(CAUSE,20)`; `NOT_KMD`; `SERANA` |
| CC186 | S L | E AFTERFIGHT | in `DEADLANDS`; `SERANA` |
| CC187 | A G | E AFTERFIGHT | in `DEADLANDS`; `ASHE_REVEAL` |
| CC188 | C I | E AFTERFIGHT | in `DEADLANDS` |
| CC189 | V R | E AFTERFIGHT | in `DEADLANDS` |
| CC190 | G K | E AFTERFIGHT | in `DEADLANDS` (Kaidan line is neutral; no gate on KMD) |
| CC191 | R K P | T | `Done(CAUSE,50)`; `NOT_KMD` |
| CC192 | L P | T | `Done(CAUSE,60)`; Lucien Free (no patch for The Cause) |
| CC193 | X V P | T | `Done(CAUSE,240)` gate open |
| CC194 | C R P | T | `Done(CAUSE,230)` gate closed; after:CC13 |
| CC195 | K P | T or E CAMP | `Comp(CAUSE)`; `KMD_DONE` |
| CC196 | X K | T | `Comp(CAUSE)`; `KMD_DONE`; after:CC19 |
| CC197 | I K | E CAMP+NIGHT | `Comp(CAUSE)`; `KMD_DONE`; after:CC17 |

### Part 2 - Ghosts of the Tribunal, round two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC198 | V P | T or E CITY Raven Rock | `Done(GOT,10)`; after:CC21 |
| CC199 | S X | E in temple `000C82:ccasvsse001-almsivi.esm` | `Done(GOT,10)`; not `GOT` 200..250; `SERANA` |
| CC200 | A X | T | `Done(GOT,10)`; after:CC25 [UNC: stage where the Masks are named]; `ASHE_REVEAL` (Q1 not required) |
| CC201 | G I | T | `Done(GOT,300)`; not `Done(GOT,120)` |
| CC202 | K I | T | `Done(GOT,120)` |
| CC203 | R P | T | `Done(QuestD 00117A,100)`; after:CC30 +2 days |
| CC204 | L X | E AFTERFIGHT or T | `Run(QuestD 00117A)` after the ash-zombie attack [UNC stage, same as CC29] |
| CC205 | X R | T | `Done(QuestE 0990EF,100)`; after:CC31 |
| CC206 | R I | T | `Comp(GOT)`; after:CC25 [UNC: Remi "saw" the mask only if the Sotha Sil mask is shown in the quest; keep if the mask appears on either branch] |
| CC207 | K P | E CAMP, MORNING | `Comp(GOT)`; `K_TOG+` |

### Part 3 - Fishing, round two (ccBGSSSE001-Fish.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC208 | G R | T or E WATER | `Done(Fish_MQ1 0009DE,200)` Catch of the Day; after:CC95 |
| CC209 | A G | T | `Done(Crab_MQ2 0009DA,200)` Crustacean Extermination; `ASHE_REVEAL` |
| CC210 | V K | T | `Done(Crab_MQ3 0009D6,200)` End of the Line |
| CC211 | X L | T | `Done(Radiant_2 000C2F,200)` Further Study [UNC stage] |
| CC212 | C L | T | player has caught any rare fish (`FISH` rare-fish formlist count > 0) [UNC formlist] |
| CC213 | S G | E WATER | `FISHSTART`; `SERANA` |
| CC214 | K P | E WATER | `FISHSTART`; `K_TOG+`; after:CC53 if it played (else fine alone) |
| CC215 | R V P | E in Riften Fishery [UNC LCTN] or T | `Done(Misc_Dwarven 000AD6,200)`; after:CC47 |
| CC216 | G P | E in Riften Fishery or T | `Done(Fish_MQ5 0009DC,200)`; after:CC42 |
| CC217 | I K | E WATER | `FISHSTART` |

### Part 4 - The Gray Cowl of Nocturnal, round two (Gray Fox Cowl.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC218 | L C | T | `Comp(manny_GF_BuryValenDreth 01E072)` |
| CC219 | V P | T | `Comp(manny_GF_Books 0026F4)` or its last stage [UNC] |
| CC220 | S P | T | `Done(GC,700)`; `SERANA` |
| CC221 | V G | T | `Done(GC,700)`; `CC_ITEM:Gray Cowl worn` |
| CC222 | I K | T | `Done(manny_GF_MiscQuestShantaFilibb 050159,200)` |
| CC223 | S G | T | `Done(GC,160)`; back in Skyrim; `SERANA`; after:CC55 |
| CC224 | K P | T | `Done(GC,700)`; `CC_ITEM:Gray Cowl worn`; after:CC59 |
| CC225 | C I | T | `Done(GC,999)` |

### Part 5 - Saints and Seducers, round two (ccBGSSSE025-AdvDSGS.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC226 | K S P | T | `Done(QuestA 000912,2000)`; `SERANA` |
| CC227 | R A | T | player has any Amber or Madness item from the plugin [UNC formlist]; `ASHE_REVEAL` |
| CC228 | A C | T | `Done(QuestB 000913,200)`; after:CC68; `ASHE_REVEAL` |
| CC229 | I S | T or E near Ri'saad's caravan | `Done(QuestA 000912,2000)`; `SERANA` |
| CC230 | K I | T | `Done(QuestB 000913,200)`; `LUC_PRESENT` |

### Part 6 - Forgotten Seasons, round two (cctwbsse001-puzzledungeon.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC231 | A R | E AFTERFIGHT in Vardnknd `003901` | `ASHE_REVEAL` |
| CC232 | S G | E in winter room `0038FF` | `SERANA` |
| CC233 | K R | T | `Comp(DLCDwarvenPuzzleDungeonHorseQuest 0038DA)`; after:CC75 |
| CC234 | C P | T | `Comp(DLCDwarvenPuzzleDungeonCrownQuest 0038DB)`; `CC_ITEM:Dwarven Crown worn` [UNC FormID] |
| CC235 | G X | E in Vardnknd or T | `Done(Quest01 0038D9,1)`; `LUC_PRESENT` |
| CC236 | V X | T | `Comp(DLCDwarvenPuzzleDungeonQuest01 0038D9)` [UNC complete stage, see CC73] |

### Part 7 - Goblins, round two (ccbgssse040-advobgobs.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC237 | V G | T | `Run(0009B6)` after the Gromm's Pass arena `000D13` [UNC stage, same as CC81] |
| CC238 | A C P | T | `Done(0009B6,8)`; after:CC79; `ASHE_REVEAL` |
| CC239 | X I | T | `Done(0009B6,200)`; `LUC_PRESENT` |
| CC240 | C K | T | `Done(0009B6,200)`; after:CC84 |
| CC241 | P R C | T or E CAMP | `Done(0009B6,200)` |

### Part 8 - Umbra, round two (ccbgssse016-umbra.esm)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC242 | A I | T | `Done(0021B6,200)`; `CC_ITEM:Umbra`; after:CC89; `ASHE_REVEAL` |
| CC243 | I K | T | after:CC91 +1 day |
| CC244 | V X | T | `Done(0021B6,200)`; after:CC90 if it played |
| CC245 | V R | T | `Done(0021B6,200)`; `CC_ITEM:Umbra` |

### Part 9 - Plague of the Dead, round two (ccbgssse003-zombies.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC246 | A G | E AFTERFIGHT:risen dead | `Done(00083D,10)`; `LUC_PRESENT`; `ASHE_REVEAL` |
| CC247 | C K | E AFTERFIGHT:risen dead | `Done(00083D,10)` |
| CC248 | V P | T | `Done(00083D,40)` |
| CC249 | R G | T or E CITY | `Done(00083D,10)` +2 days; after:CC92 |

### Part 10 - Bittercup, round two (cckrtsse001_altar.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC250 | S K P | T | first cup drunk (as CC101); `SERANA` |
| CC251 | I G | T | `Done(ccKRTSSE001_QuestFortune 000A90,1000)` |
| CC252 | A K | T | `Done(ccKRTSSE001_QuestPower 000A5E,100)`; not `In(000F54)`; `K_ANY`; `ASHE_REVEAL` |
| CC253 | R P | T | `Done(ccKRTSSE001_zQuest 000D63,200)` |
| CC254 | C X | T | first cup drunk (as CC101) |

### Part 11 - Wild Horses, round two (ccbgssse034-mntuni.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC255 | G R C | T | `Done(UnicornQuest 000DE8,20)` |
| CC256 | S P | T | `Done(000DE8,20)`; `SERANA`; `SER_VAMP` |
| CC257 | L V | T | `Done(000DE8,20)`; `LUC_ADMIT`; after:CC104 if it played |
| CC258 | I K | T | as CC103 (first wild horse tamed) |
| CC259 | V A | T | as CC103; `ASHE_REVEAL` |
| CC260 | K P | T, player riding | `Done(000DE8,20)`; player mounted on the unicorn [UNC: GetPlayersLastRiddenHorse base = unicorn]; `K_TOG+` |

### Part 12 - Divine Crusader, round two (ccmtysse001-knightsofthenine.esl)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC261 | I P | T | `CC_ITEM:Crusader's Relics worn` |
| CC262 | V G | T | `Run(000865)` and after:CC113 (a second Pilgrim's Path) [UNC: confirm the quest restarts on a new crime] |
| CC263 | C I | E at any of the nine shrines | `Run(000865)` [UNC shrine refs] |
| CC264 | A K | E at a Shrine of Kynareth | `Run(000865)`; `ASHE_REVEAL`; not after:CC114 in the same visit |
| CC265 | K R P | T | `CC_ITEM:Crusader's Relics worn`; `K_CRUSH` |

### Part 13 - Homes and the farm, round two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC266 | S V | E HOUSE Tundra Homestead | `SERANA` |
| CC267 | A P | E HOUSE Tundra Homestead | `ASHE_REVEAL` |
| CC268 | X G | E HOUSE Tundra Homestead | `LUC_PRESENT` |
| CC269 | G P | E HOUSE Tundra Homestead | after:CC115 +1 day |
| CC270 | C R P | E in Shadowfoot Sanctum `000D41` | `Done(00082A,100)` |
| CC271 | X R | E in Shadowfoot Sanctum | `Done(00082A,100)` |
| CC272 | R K | E at farm `000D36` | `Done(000D28,1000)`; after:CC124 |
| CC273 | S P | E at farm `000D36` exterior, daytime | `SERANA`; `SER_CURED` |
| CC274 | I P | E at farm `000D36` | `Done(000EB7,500)`; after:CC272 |
| CC275 | V G | E at farm `000D36` or T | `Done(000EB7,500)` |

### Part 14 - Smaller quests, round two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC276 | S R | T | `Done(00080C,1000)` Ruin's Edge; `SERANA` |
| CC277 | K G | T | `Done(00080C,1000)`; after:CC131 +2 days; `LUC_PRESENT` |
| CC278 | A P | T | `Comp(00081C:ccbgssse018-shadowrend.esl)`; `ASHE_REVEAL` |
| CC279 | C G | T | `Comp(00081C:ccbgssse018-shadowrend.esl)` |
| CC280 | G V | T | `CC_ITEM:Staff of Sheogorath`; `GORE_SASEC` |
| CC281 | K R | T | `CC_ITEM:Lord's Mail`; `LUC_PRESENT` |
| CC282 | S K | T | `Done(000805:ccbgssse006-stendarshammer.esl,1000)`; `SERANA`; `SER_VAMP` |
| CC283 | A R | T | `Done(000805:ccbgssse006-stendarshammer.esl,1000)`; `ASHE_Q1` (soul-fragment line); `ASHE_REVEAL` |
| CC284 | L P | E in Hob's Fall Cave or T | `Done(00083C:ccbgssse014-spellpack01.esl,10)` |
| CC285 | X K | T | as CC284 |
| CC286 | G C | E CAMP+NIGHT | after:CC154 |
| CC287 | S I | T | `CC_ITEM:Dawnfang` equipped (daytime form) [UNC FormID]; `SERANA`; `SER_VAMP` |
| CC288 | K G | T | `Done(00088C:ccedhsse003-redguard.esl,20)`; `NOT_K_AKAVIRI` |
| CC289 | A I | E AFTERFIGHT in Cronvangr Cave | `Run(000805:ccbgssse069-contest.esl)` or `Done(...,100)`; `ASHE_REVEAL` |
| CC290 | S V | T | `Done(000926:ccmtysse002-ve.esl,100)`; `CC_ITEM:Vigil Enforcer worn`; `SERANA`; `SER_VAMP` |
| CC291 | X A | T | Necromantic Grimoire read (as CC173); `ASHE_Q1` |
| CC292 | R G | T or E near the Saturalia merchant [UNC ref] | `Done(ccVSVSSE001_MainQuest 00082B,10)` |
| CC293 | C S | T | `SATURALIA_M`; `SERANA` |
| CC294 | K P | T or E CAMP | `SATURALIA_M`; `K_TOG+` |
| CC295 | I P | T | `HORSE_ARMOR` |
| CC296 | G V | T | `HORSE_ARMOR` |
| CC297 | R P | T | `Done(000800:ccedhsse002-splkntset.esl,1500)` or `Done(...,2000)` |
| CC298 | G K | T | `Done(000927:ccffbsse001-imperialdragon.esl,170)` or `Done(...,270)` (branch-neutral) |
| CC299 | V C | T | `Done(000819:ccpewsse002-armsofchaos.esl,1000)` |
| CC300 | R I P | T | `Done(000823:ccbgssse045-hasedoki.esl,200)`; after:CC148 +2 days |

### Part 15 - Armour, trinkets and curios
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CC301 | K I | T | `Run(ccBGSSSE064_Quest 000819:ccbgssse064-ba_elven.esl)` (Once a Hunter started) [UNC stage where the bounty is read] |
| CC302 | V P | T | `WEAR:Elven Hunter` |
| CC303 | G R | T | `WEAR:Elven Hunter`; `LUC_PRESENT` |
| CC304 | A P | T | `WEAR:Elven Hunter`; `ASHE_REVEAL` |
| CC305 | G S | T | `WEAR:Silver` (ccbgssse056-ba_silver.esl); `SERANA`; `SER_VAMP` |
| CC306 | I P | T | `ALT:56 done` (When the Cat's Away 000814) |
| CC307 | C X | T | `WEAR:Silver`; `LUC_PRESENT` |
| CC308 | R P | T | `WEAR:Dwarven Plate` (ccbgssse061-ba_dwarven.esl) |
| CC309 | R K | T | `WEAR:Dwarven Mail` (ccbgssse062-ba_dwarvenmail.esl) |
| CC310 | V I | T | `WEAR:Dwarven Mail`; `LUC_PRESENT` |
| CC311 | G K | T | `ALT:52 done` (Brothers in Irons 000822:ccbgssse052-ba_iron.esl) |
| CC312 | I P | T | `WEAR:Iron` (ccbgssse052-ba_iron.esl) |
| CC313 | V R | T | `ALT:53 done` (Double-Edged 000826:ccbgssse053-ba_leather.esl) |
| CC314 | G P | T | `WEAR:Orcish Plate` (ccbgssse054-ba_orcish.esl); `ALT:54 done` |
| CC315 | V K | T or E INN | `ALT:55 done` (Gambler's Edge 000830:ccbgssse055-ba_orcishscaled.esl) |
| CC316 | L K | T | `WEAR:Steel Soldier` (ccbgssse058-ba_steel.esl); `ALT:58 done` |
| CC317 | V X | T | `WEAR:Ebony Plate` (ccbgssse063-ba_ebony.esl); `ALT:63 done` |
| CC318 | K P | T | `WEAR:Daedric Plate` (ccbgssse050-ba_daedric.esl) |
| CC319 | C G | T | `WEAR:Daedric Mail` (ccbgssse051-ba_daedricmail.esl) |
| CC320 | X P | T | `WEAR:Daedric Plate` or `WEAR:Daedric Mail` |
| CC321 | C P | T | `WEAR:Stalhrim Fur` (ccbgssse057-ba_stalhrim.esl) |
| CC322 | V R | T | `WEAR:Dragonplate` (ccbgssse059-ba_dragonplate.esl) |
| CC323 | I C | T | `WEAR:Dragonscale` (ccbgssse060-ba_dragonscale.esl) |
| CC324 | G P | T | `Run` or `Comp(ccEDHSSE001_CraftsmanEncounterQuest 00082F:ccedhsse001-norjewel.esl)` (craftsman met) |
| CC325 | V X | T | as CC324 |
| CC326 | R P | T | `Comp(00082F)`; after:CC180 |
| CC327 | X I | E near a Khajiit caravan merchant | `CURIOS`; after:CC127 |
| CC328 | X P | E at an alchemy table [UNC: furniture-in-use check] or T | `CURIOS`; after:CC61 (Xelzaz's "stands closest" rule) |
| CC329 | K X | E CAMP | `CURIOS` |
| CC330 | R I | E CAMP | `CURIOS`; after:CC50 |

## 4. Notes for the build
- CC195 has Kaidan name the Blooded Dawn: `KMD_DONE` is mandatory. qa_check's cult filter passes it because the When line says "Blood and Fire".
- CC191 plays only `NOT_KMD`; if KMD finishes before it fires, drop it (it would read as him hiding again).
- CC243 needs CC91 to have played (Umbra slept in a chest); otherwise it never fires.
- CC260 and CC214, CC207, CC294 are `K_TOG+`; CC265 is `K_CRUSH` (Luna oblivious). CC252 needs `K_ANY` (Ashe reads his heart rate around Luna).
- Serana rows with blood/sun/silver/holy-weapon jokes carry `SER_VAMP` (CC256, CC282, CC287, CC290, CC305); CC273 carries `SER_CURED`.
- The alternative-armour quest stories were not traced in the strings files; the talks only use the journal names and the armour itself, so they are safe on any outcome.
