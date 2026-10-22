# 37 VANILLA SIDE QUESTS AND HOLDS - trigger rows (prefix SQ, 150 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\37 VANILLA SIDE QUESTS AND HOLDS.txt`
Format and shared gate codes: `TRIGGERS.md` sections 4-5. Quest stages below were read read-only from the live winners with houseCARL (`housecarl_records`, epoch e2-e2f00b3b2d1720b4, 2026-10-18): journal log entries and objectives of every quest used. Winners that change a vanilla quest are noted where it matters (Forsworn Conspiracy QE, GoldenLie, BOTI, Infiltration QE, Nilheim QE, Miscellaneous Quests are Favors).

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe. `U` = Luna (player line, Eleonora voice; never a gate, no Free() test).
Type: T = timer, E = event (fires on the moment: arrival, quest stage newly set, after a fight).

## Gate codes used in this file

From TRIGGERS.md section 4: `K_CRUSH`, `K_TOG+`, `ANYROM`, `BRYNJAR`, `HELGEN` (MQ101 145 done), `GORE_BAIL`, `VAL_FATHIS`, `NIGHT`, `SNOW`, `INN`, `RIVERWOOD`, `CITY:<Name>`, `HELGEN_LOC` (HelgenLocation 018A4A), `AFTERFIGHT[:enemy]`.

From `21 HEARTHFIRE AND HOME.md` / `20 DAWNGUARD.md` (same definitions):
- `SER` = Serana following (`GetVMQuestVariable(DLC1NPCMentalModel 002B6E:Dawnguard.esm, ::IsFollowing_var) == 1`, DLC1VQ02 completed, `SDA_PlayerInDialogue == 0`). Every row with S implies SER.
- `SER_VAMP` = Serana `HasKeyword Vampire (0A82BB:Skyrim.esm) == 1` and `SDA_CureQuestTimer` not running.
- `ASHE` = Ashe following (`GetVMQuestVariable(MM_AsheMentalModel 06FE28:Ashe - Fire and Blood.esp, ::IsFollowing_var) == 1`, `bConfigVarIdles == 1`, `MM_PlayerinDialogue == 0`, `MM_FlashbackRunning == 0`, her quest-running blocks). Every row with A implies ASHE.
- `ASHE_HIRED` = MM_AsheIntro 0A7946 completed. `ASHE_REVEAL` = MM_FriendshipQuest 1A9DEE stage >= 70 or `MM_AutomatonReveal == 1`. `ASHE_NEVAS` = MM_AMQ_02 BB194C completed (all `:Ashe - Fire and Blood.esp`).

New in this file:
- `Done(Q,s)` = GetStageDone Q s. `Comp(Q)` = GetQuestCompleted Q. `Run(Q)` = GetQuestRunning Q. `Q a..b` = current stage in that range. All quest FormIDs are `:Skyrim.esm` unless another plugin is named.
- `LOC:<EditorID>` = player GetInCurrentLoc that location (or a child of it). **[U] = location EditorID not looked up; confirm at build.** Whiterun/Solitude/Windhelm/Riften/Markarth/Morthal/Falkreath/Winterhold use the hold-capital locations behind `CITY:<Name>`.
- `NEAR:<npc>` = that NPC's persistent ref within 1500 units of the player and alive. **[U ref]** unless a FormID is given.
- `NOT_HELGEN` = MQ101 (03372B) stage 145 **not** done AND MQ101 stage < 3 (Helgen still standing, intro not running; see vanilla_gates.md A1/A4).
- `GRELOD_DEAD` = Grelod the Kind ref GetDead (as 21 HEARTHFIRE).
- `MS_FC_FRAMED` = Comp(MS01) OR Done(aaMS01New 000800:Forsworn Conspiracy Quest Expansion.esp, 10). The QE lets the player resist arrest instead of going into Cidhna.
- `CIDHNA_OUT` = (Comp(MS02 040A5E) OR Comp(aaMS02New 000814:Forsworn Conspiracy Quest Expansion.esp)) AND player not in CidhnaMineLocation.
- `MADANACH_FREE` = Done(MS02,100) OR Done(aaMS02New,60). `MADANACH_DEAD_PARDON` = Done(MS02,250).

Silence add-on (put in WorldQuiet while relevant): player in CidhnaMineLocation [U EditorID] = no talks (followers are not there; Remi's Free() already blocks it).

Quest IDs used (EditorID FormID, live winner):
MS09 Missing in Action 01CF26 (USSEP) · T03 Blessings of Nature 01C48E · FreeformWhiterunQuest01 Braith/Lars 0934F9 · FreeformWhiterunQuest03 Proventus sword 0946FD · FreeformWhiterunQuest04 Andurs' amulet 094E3C · Favor204Whiterun 000DB9:Favor Quests Seperated.esp (Amren's sword **[U: that this is Amren's]**) · MS13 Golden Claw 039645 (GoldenLie.esp: Camilla can be the giver; stages 100/110 returned, 120/130 kept, 200 both dead) · FreeformRiverwood01 A Lovely Letter 074A83 (LovelyLetter.esp; objectives 10-220, no log) · MQ101 03372B · FreeformFalkreathQuest03 0B83C3 / 03B 0D6986 Dark Ancestor (Vighar) · FreeformFalkreathQuest02 Runil's Dark Past 09375A (no stages/objectives in record) · dunHunterQST Kyne's Sacred Trials 018601 · BardsCollegeDrum 0D944F · BardsCollegeFlute 0D9431 · BardsCollegeLute 0D93FA · MS01 018B4B / MS02 040A5E (winner Forsworn Conspiracy Quest Expansion.esp) · aaMS01New 000800 / aaMS02New 000814 (:Forsworn Conspiracy Quest Expansion.esp) · FreeformCidhnaMineA Shiv 0DB851 · T01 Heart of Dibella 023B6C · FreeformKolskeggrA 01FD72 · dunNchuandZelQst Lost Expedition 0C3709 · FreeformMarkarthO Nimhe 053804 · dunDarklightQST Repentance 03FA89 · FreeformOldHroldanB 06819A · MS06Start 093807 / MS06 026C4D Wolf Queen · MS07 Lights Out! 023A64 · MS05 Tending the Flames 053511 · SolitudeFreeform02 Fit for a Jarl 0C7D1C · SolitudeOpening 0B2FD9 · MS11 Blood on the Ice 01F7A3 (BOTI.esp; 100 = Wuunferth, 250 = Calixto) · MS12 White Phial 02C258 / MS12b Repairing the Phial 02499C · MS10 Rise in the East 01DBFC · MS03 Promises to Keep 01DA3C · FreeformRiften01 Supply and Demand 053305 · FreeformRiften04 Few and Far Between 053308 · FreeformRiften06 Sealing the Deal 053318 · FreeformRiften09 Grimsever's Return 05331C · FreeformRiften20 The Raid 085D40 · FreeformIvarstead01 Lifting the Shroud 0D9B63 · FreeformShorsStone01 Mine or Yours 0E49E7 · dunForelhostQST 035354 · MS04 Unfathomable Depths 0209CA · dunNilheimQST 01BAEC (Nilheim QE) · MS14 Laid to Rest 025F3E · FreeformMorthalA Falion's Secret 021891 · FreeformWinterholdC Drowned Sorrows 064EA8 · dunGauldursonQST Forbidden Legend 0E4D31 · dunTrevasWatchQST Infiltration 04B2A1 (Infiltration QE) · dunFrostmereCryptQST The Pale Lady 0CF915 · NN01 A Return To Your Roots 0C9BA0.

## Table

### Part 1 - Whiterun Hold, Riverwood, Helgen, Rorikstead
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ1 | V L U | E CITY:Whiterun | Done(MS09,10) not required; MS09 not completed (Done 200/201 == 0) |
| SQ2 | G K | T | Done(MS09,30); not Done(MS09,110) |
| SQ3 | K I | T | Done(MS09,110) |
| SQ4 | G U | T | Comp(MS09) (200 or 201) |
| SQ5 | V K U | E CITY:Whiterun | Done(MS09,10); NEAR:Olfina Gray-Mane or NEAR:Jon Battle-Born |
| SQ6 | G K U | E LOC:WhiterunBanneredMare [U] | K_CRUSH; NEAR:Mikael |
| SQ7 | K V | T | Comp(Favor204Whiterun) [U Amren]; BRYNJAR (he has talked about his past) |
| SQ8 | V G | T | Comp(FreeformWhiterunQuest03) |
| SQ9 | L X | T | Done(T03,20); T03 not completed |
| SQ10 | G R | T | Done(T03,20); Maurice Jondrelle met [U: Maurice alias filled / NEAR:Maurice]; T03 not completed |
| SQ11 | I U | E LOC:EldergleamSanctuary [U] | Run(T03) |
| SQ12 | S I | E CITY:Whiterun | Comp(T03) (100 or 105); SER |
| SQ13 | G I | E CITY:Whiterun | NEAR:Heimskr (near the Talos shrine) |
| SQ14 | I G | T | Comp(FreeformWhiterunQuest01) |
| SQ15 | L S | T | Comp(FreeformWhiterunQuest04); SER; SER_VAMP |
| SQ16 | V C U | E LOC:WhiterunBelethorsGeneralGoods [U] | — |
| SQ17 | A G | E CITY:Whiterun | NEAR:Ysolda; ASHE; ASHE_HIRED |
| SQ18 | G A U | E INN (Bannered Mare) | Uthgerd beaten in her brawl [U: Uthgerd brawl quest/flag]; ASHE |
| SQ19 | K L | E LOC:BleakFallsBarrowLocation [U], first entry | — |
| SQ20 | R K | T | Done(MS13,10); MS13 not completed |
| SQ21 | L U | E in Bleak Falls Sanctum near the claw door [U loc] | Run(MS13) stage >= 12; player has the Golden Claw [U item] |
| SQ22 | I V | E AFTERFIGHT in Bleak Falls Barrow (web room) | Run(MS13); NEAR:Arvel the Swift |
| SQ23 | K V | T | Done(MS13,100) or Done(MS13,110) |
| SQ24 | V U | T | Done(MS13,120) or Done(MS13,130) |
| SQ25 | R V | E LOC:RiverwoodTrader [U] | VAL_FATHIS; Lucan and Camilla alive |
| SQ26 | G V U | E RIVERWOOD | Run(FreeformRiverwood01); ANYROM |
| SQ27 | K R | E RIVERWOOD | Run(FreeformRiverwood01); K_CRUSH |
| SQ28 | G S | E RIVERWOOD | NEAR:Sven; SER |
| SQ29 | A K | T | Comp(FreeformRiverwood01); ANYROM; ASHE |
| SQ30 | G U | E HELGEN_LOC | NOT_HELGEN |
| SQ31 | K V | E HELGEN_LOC | HELGEN; Done(MQ101,1000) |
| SQ32 | I L | E HELGEN_LOC, near the headsman's block [U ref] | HELGEN; Done(MQ101,1000) |
| SQ33 | C L | E HELGEN_LOC | HELGEN; Done(MQ101,1000) |
| SQ34 | K G | T | Erik allowed to adventure [U: Erik in PotentialFollowerFaction / Mralki persuaded flag]; after MN65 not required |
| SQ35 | X L U | E LOC:RoriksteadLocation [U] | — |

### Part 2 - Falkreath Hold
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ36 | S K | T | Run(FreeformFalkreathQuest03B) (objective 10); SER |
| SQ37 | G S U | T | Comp(FreeformFalkreathQuest03) (200) or Comp(03B); SER |
| SQ38 | X U | T | Comp(FreeformFalkreathQuest02) [CHECK: quest has no stages in the record; may need a script flag or Runil's journal returned] |
| SQ39 | V I | E LOC:FalkreathJarlsLonghouse [U] | — |
| SQ40 | K G | T | Done(dunHunterQST,21); not completed |
| SQ41 | C I | T | dunHunterQST 21..49 |
| SQ42 | A G | T | Comp(dunHunterQST); ASHE; ASHE_REVEAL |
| SQ43 | K U | T | Done(dunHunterQST,80); BRYNJAR |
| SQ44 | L G | T | Done(BardsCollegeDrum,20); not Done(200) |
| SQ45 | V R U | E LOC:PinewatchLocation [U] | — |

### Part 3 - The Reach
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ46 | R K | T | Done(MS01,15); MS01 not completed |
| SQ47 | V R | T | Done(MS01,20); MS01 not completed |
| SQ48 | L K | T | MS_FC_FRAMED |
| SQ49 | K G U | T | CIDHNA_OUT |
| SQ50 | R X | T | MADANACH_FREE; CIDHNA_OUT |
| SQ51 | V K | T | MADANACH_DEAD_PARDON |
| SQ52 | G I | T | Done(aaMS01New,49) |
| SQ53 | R L | T | Done(aaMS02New,20) |
| SQ54 | I U | T | Comp(FreeformCidhnaMineA); CIDHNA_OUT |
| SQ55 | L X | E AFTERFIGHT:Forsworn with a Briarheart among the dead [U: BriarheartRace/keyword check; fallback LocTypeForswornCamp 0130EE] | — |
| SQ56 | C K | E LOC:DruadachRedoubtLocation [U] | MADANACH_FREE |
| SQ57 | R S | T | Done(T01,80); T01 not completed; SER |
| SQ58 | R V | T | Done(T01,205) |
| SQ59 | K U | T | Done(T01,200); K_CRUSH |
| SQ60 | R K | T | Comp(FreeformKolskeggrA) |
| SQ61 | R L U | T | Done(dunNchuandZelQst,20); not Done(100) |
| SQ62 | U R | T | Done(dunNchuandZelQst,100) |
| SQ63 | A L | E LOC:NchuandZelLocation [U] | Done(dunNchuandZelQst,100); ASHE; ASHE_REVEAL |
| SQ64 | I R | T | Comp(FreeformMarkarthO) |
| SQ65 | A R | E CITY:Markarth | ASHE; ASHE_NEVAS |
| SQ66 | C U | T | Done(dunDarklightQST,10); not completed |
| SQ67 | C G | T | Comp(dunDarklightQST) (40 or 50); after SQ66 |
| SQ68 | L C U | T | Run(BardsCollegeFlute); not Done(200) |
| SQ69 | I G U | E LOC:OldHroldanInnLocation [U] | after SQ13 (callback; drop the gate if SQ13 can't play) |

### Part 4 - Haafingar
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ70 | I K | E CITY:Solitude, first arrival | SolitudeOpening execution scene running or just finished [U stage]; Roggvir dead |
| SQ71 | K C U | T | Done(MS06Start,100) |
| SQ72 | L U | T | Done(MS06,50); not Done(150) |
| SQ73 | S L | E LOC:PotemasCatacombs [U] | MS06 100..149; SER |
| SQ74 | G X | T | Done(MS06,150) |
| SQ75 | V K U | T | Comp(MS06) (250) |
| SQ76 | V X | T | Done(MS07,10) or Done(MS07,50); not Done(MS07,100) |
| SQ77 | V G U | T | Done(MS07,125); not Done(MS07,65) |
| SQ78 | I V | T | Done(MS07,330) |
| SQ79 | G L | T | Done(MS05,75); not Done(125) |
| SQ80 | V R U | T | Done(MS05,225) or Done(MS05,254); not Done(255) |
| SQ81 | G C | E festival in the Bards College courtyard | Done(MS05,255); not Done(300) (or MS05KingOlafsFestival 06C0EA running [U]) |
| SQ82 | G K U | T | Done(MS05,300) |
| SQ83 | L U | T | Done(MS05,300); after SQ82 |
| SQ84 | R I | T | Done(BardsCollegeLute,20); not Done(200) |
| SQ85 | L S | E LOC:SolitudeBluePalace [U] | DA15 (The Mind of Madness) not started [U FormID]; SER |
| SQ86 | X L | E LOC:SolitudeBluePalace [U] | NEAR:Falk Firebeard |
| SQ87 | A V | E LOC:SolitudeWinkingSkeever [U] | ASHE; ASHE_HIRED |
| SQ88 | V A | T | Comp(SolitudeFreeform02); ASHE |
| SQ89 | L C U | E LOC:DragonBridgeLocation [U] | — |
| SQ90 | K I | E LOC:DragonBridgeLocation, near the Penitus Oculatus Outpost [U] | — |

### Part 5 - Eastmarch
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ91 | I C | E on the Windhelm bridge (exterior, approaching the gate) [U loc/trigger box] | — |
| SQ92 | X I | T | Done(MS11,15); MS11 not completed |
| SQ93 | V R | E LOC:WindhelmCalixtosHouse [U] | — |
| SQ94 | L U | T | Done(MS11,60); MS11 not completed |
| SQ95 | K G U | T | Done(MS11,250) |
| SQ96 | X L | T | Done(MS11,100) |
| SQ97 | S I | E CITY:Windhelm + NIGHT | MS11 15..99; SER; SER_VAMP |
| SQ98 | R I | E CITY:Windhelm | Comp(MS11); NEAR:Torbjorn Shatter-Shield |
| SQ99 | V S | E Windhelm Gray Quarter [U loc] | SER |
| SQ100 | K X | E CITY:Windhelm | NEAR:Brunwulf Free-Winter |
| SQ101 | X R | T | Done(MS12,10); MS12 not completed |
| SQ102 | X U | T | Run(MS12b) [U first stage]; MS12b not completed |
| SQ103 | X L | T | Comp(MS12b) |
| SQ104 | V K | T | Done(MS10,10); not Done(100) |
| SQ105 | V U | T | Done(MS10,100) |
| SQ106 | R L | E CITY:Windhelm | NEAR:Viola Giordano |
| SQ107 | X S | E LOC:SarethiFarmLocation [U] | SER |

### Part 6 - The Rift
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ108 | I R | E LOC:RiftenOrphanage (Honorhall) [U] | Grelod alive |
| SQ109 | K G | E LOC:RiftenOrphanage [U] | GRELOD_DEAD |
| SQ110 | S K | E INN in CITY:Riften | SER |
| SQ111 | R G | T | Done(MS03,5) or Done(MS03,10); not Done(200); GORE_BAIL |
| SQ112 | V C | T | Done(MS03,25); not Done(200) |
| SQ113 | I K | T | Run(FreeformRiften20); objective 10..40 not complete |
| SQ114 | I U | T | Comp(FreeformRiften01) |
| SQ115 | K G | T | Comp(FreeformRiften09) |
| SQ116 | L K | E LOC:RiftenMistveilKeep [U] | Laila Law-Giver is Jarl (Rift not handed to the Imperials) [U check] |
| SQ117 | X V | T | Run(FreeformRiften06) [CHECK: Talen-Jei's amethysts] |
| SQ118 | X K U | T | Run or Comp(FreeformRiften04) [CHECK: Ingun's ingredients] |
| SQ119 | L U | T | Comp(FreeformIvarstead01) |
| SQ120 | V R | E LOC:ShroudHearthBarrowLocation [U] | — |
| SQ121 | I L | T | Run(FreeformShorsStone01) [CHECK: Redbelly Mine spiders] |
| SQ122 | K L | T | Done(dunForelhostQST,10); not Done(60) |
| SQ123 | R G | E LOC:ForelhostLocation [U] | Done(dunForelhostQST,20) |
| SQ124 | K G U | T | Done(dunForelhostQST,150); after SQ122 |
| SQ125 | X R | T | Done(MS04,10); not Done(900) |
| SQ126 | R L U | T | Done(MS04,900) |
| SQ127 | G V | T | Done(dunNilheimQST,30) |

### Part 7 - Hjaalmarch, Winterhold and the wild places
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ128 | S K | T | Done(MS14,30); not Done(70); SER; SER_VAMP |
| SQ129 | G I | T | Done(MS14,30); not Done(70) |
| SQ130 | S U | T | Done(MS14,95); MS14 not completed; SER |
| SQ131 | G S | E LOC:MovarthsLairLocation [U] | Run(MS14); SER; SER_VAMP |
| SQ132 | I L U | T | Comp(MS14) |
| SQ133 | L R | E LOC:MorthalHighmoonHall [U] | NEAR:Idgrod the Elder |
| SQ134 | S X | E CITY:Morthal | SER; SER_VAMP |
| SQ135 | L U | T | Done(FreeformMorthalA, objective 5 shown) [U stage] |
| SQ136 | U K | E LOC:WinterholdLocation [U], not in CollegeOfWinterholdLocation | — |
| SQ137 | A L | E LOC:WinterholdLocation [U] + SNOW | ASHE |
| SQ138 | K I | T | Done(FreeformWinterholdC,10); not Done(40) |
| SQ139 | V U | T | Done(FreeformWinterholdC,40) |
| SQ140 | R C U | E LOC:WinterholdBirnasOddments [U] | — |
| SQ141 | L G | E LOC:YngolBarrowLocation [U] | — |
| SQ142 | L U | T | Done(dunGauldursonQST,20) |
| SQ143 | L G | E LOC:FolgunthurLocation [U] | Done(dunGauldursonQST,20) |
| SQ144 | G V | T | Done(dunGauldursonQST,30) |
| SQ145 | K I U | T | Done(dunGauldursonQST,150) |
| SQ146 | A R | T | Done(dunGauldursonQST,255) / Comp; ASHE; ASHE_REVEAL |
| SQ147 | G A | T | Done(dunTrevasWatchQST,10); not Done(60); ASHE |
| SQ148 | K U | T | Done(dunTrevasWatchQST,100); K_TOG+ |
| SQ149 | I R | T | Comp(dunFrostmereCryptQST) |
| SQ150 | X C | E GetInWorldspace Blackreach [U] | Run(NN01) |

## Open items to check at build
- Location EditorIDs marked [U] (about 30). NEAR refs for Mikael, Heimskr, Ysolda, Olfina/Jon, Sven, Arvel, Falk, Torbjorn, Brunwulf, Viola, Idgrod.
- Amren's sword = Favor204Whiterun? Erik's "allowed to adventure" flag. Uthgerd brawl flag. SolitudeOpening execution stage. MS12b first stage. FreeformMorthalA stage for "followed Falion". DA15 FormID.
- [CHECK] quests with no log text in the record: Runil's Dark Past (SQ38), Sealing the Deal (SQ117), Few and Far Between (SQ118), Mine or Yours (SQ121). Lines stay general; confirm the quest giver matches.
- SQ81 needs the festival scene to be over or not playing a scripted speech; add IsInScene on Viarmo if the festival uses a scene.
