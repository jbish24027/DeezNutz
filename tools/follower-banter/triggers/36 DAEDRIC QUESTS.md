# Triggers - 36 DAEDRIC QUESTS (prefix DA, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\36 DAEDRIC QUESTS.txt`
Sources: quest stage lists and journal text read with houseCARL `housecarl_records` (read-only, epoch e2-5803f1efeca3405a, 2026-10-18); `research\triggers\vanilla_gates.md`, `kaidan_block.md`, `others_block.md`; bibles.
Format and base gate codes: `TRIGGERS.md` sections 4-5. Reused codes from other sheets: `KMD_DONE` / `NOT_KMD` (14 CREATION CLUB.md), `S_*`, `SER_VAMP`, `DG_END`, `DG_CAIRN`, `ASHE_REVEAL`, `ASHE_Q1` (20 DAWNGUARD.md), `CT_END` (13 ...md).
Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check).
Shorthand: `Done(Q,s)` = GetStageDone Q s == 1. `Comp(Q)` = GetQuestCompleted. `In(L)` = player in location L. **[UNC]** = not verified, check at build.

## 1. Quest records (all Skyrim.esm unless noted) and the stages used

Stages and log text are from the live winner of each quest record.

| Quest | FormID | Winner | Stages used (journal meaning) |
|---|---|---|---|
| DA01 The Black Star | 028AD6 | USSEP | 10 met Aranea · 30 Nelacar names Malyn Varen · 50 have the corrupted Star · 70/75 inside the Star (Azura/Nelacar) · **100** Azura's Star cleansed (complete) · **110** Black Star made (complete) |
| DA02 Boethiah's Calling | 04D8D6 | USSEP | 1 book · 5 found shrine · 7 told to sacrifice someone at the Pillar · 10 Boethiah possesses the corpse, cultists fight · 12 kill the old champion · **50** made champion (complete) |
| DA03 A Daedra's Best Friend | 01BFC4 | USSEP | 25/50 met Barbas · 70 Clavicus agrees (fetch the Rueful Axe) · 150 have the axe, the choice · 155 chose to kill Barbas · **200** reunited, Masque (complete) · **205** complete, axe kept [UNC: 205 assumed to be the kill-branch completion; 155 carries the kill log] |
| DA04 Discerning the Transmundane | 02D512 | USSEP | 20 met Septimus · 35 lexicon delivered · 40 collect elven blood · **100** Oghma Infinium (complete) · 105 killed Septimus (fail flag) · 200 complete |
| DA05 Ill Met by Moonlight | 02A49A | CH_IMBMDialougeAddon.esp | 10 rumour · 20 met Sinding, ring given · 50 Hircine asks for Sinding's death · 70 defending Sinding · **100** killed Sinding, Savior's Hide · **101** "justice" ending (addon) · **105** spared Sinding · 205 left him (fail) |
| DA06 The Cursed Tribe | 03B681 | The Cursed Tribe - Quest Expansion.esp | see 13 ...md: `CT_END` = 200 or 210 done; 200 = Volendrung |
| DA07 Pieces of the Past | 0240B8 | Update.esm | 10 Silus's job · 13 fetch the three pieces · 50 all pieces, go to the shrine · 70 Dagon asks you to kill Silus · **100** Razor (complete) · **150** refused (complete) · 200 Silus dead otherwise (fail) |
| DA08 The Whispering Door | 04A37B | The Whispering Door - Quest Expansion.esp | 10 Balgruuf asks · 25 Mephala's task · 45 decide what to do with the Blade · **50** got rid of the Blade (complete) · **60** received the Blade (complete) · 80 Blade fully powered |
| DA09 The Break of Dawn | 04E4E1 | Authoria - Patch - SRC - Requiem.esp | 50 voice from Kilkreath · 100 beacon found · 300 enter Kilkreath Ruins, guide the light · **500** Dawnbreaker (complete) |
| DA10 The House of Horrors | 022F08 | Authoria - Patch - SRC - House of Horrors Quest Expansion.esp | 10 Tyranus · 80 met Molag Bal (caged, lure Logrolf) · **200** Mace (complete) · **210** helped Tyranus destroy the altar (complete) · 500/550 fail |
| DA11 The Taste of Death | 02C358 | USSEP | 10 Eola's invitation · 30 lure Verulus · 50 Verulus dead, feast offered · **100** feasted, Namira's Ring (complete) · **250** killed Eola (fail) · **500** killed Verulus outside the shrine (fail) |
| DA13 The Only Cure | 08998D | Authoria - Master Patch - USSEP Dialogue Merge.esp | 10 Kesh's offering · 20 learned of Orchendor · 40 Peryite asks for Orchendor's death · **100** killed Orchendor for Peryite (complete, Spellbreaker) · **101** refused Peryite (fail) · **102** killed Orchendor and destroyed the altar (complete) |
| DA14 A Night to Remember | 01BB9B | USSEP | 5/10 woke in the Temple of Dibella · **200** complete (Sanguine Rose) |
| DA15 The Mind of Madness | 02AC68 | USSEP | 10 Dervenin · 100 in Pelagius' mind · **200** complete (Wabbajack) |
| DA16 Waking Nightmare | 0242AF | Dawnguard.esm | 20 heard of the nightmares · 50 Erandur reveals the Skull · 100 Dreamstride plan · 140 Torpor in hand · 160 in the priest's dream · 180 awake, barrier down · 197 Vaermina's choice · **200** Erandur lived, Skull destroyed (complete) |
| TG09 Darkness Returns | 021555 | Authoria - Haberdashery.esp | Comp = has met Nocturnal |

## 2. Gate codes used in this file (new)

| Code | Test |
|---|---|
| `DA_ANY` | at least one of DA01..DA16 completed (Comp) |
| `DA_TWO` | at least two of DA01..DA16 completed (controller counts; Comp is enough) |
| `DA_STAR_PURE` | Done(DA01,100) |
| `DA_STAR_BLACK` | Done(DA01,110) |
| `DA_BOE` | Done(DA02,50) |
| `DA_BARBAS` | Done(DA03,70) and not Done(DA03,155) and not Comp(DA03) (Barbas following) |
| `DA_MASQUE` | Done(DA03,200) |
| `DA_AXE` | Done(DA03,155) or Done(DA03,205) [UNC] |
| `DA_OGHMA` | Done(DA04,100) |
| `DA_SINDING_KILLED` | Done(DA05,100) |
| `DA_SINDING_SPARED` | Done(DA05,105) |
| `DA_RAZOR` | Done(DA07,100) |
| `DA_RAZOR_REFUSED` | Done(DA07,150) |
| `DA_BLADE_KEPT` | Done(DA08,60) |
| `DA_BLADE_GONE` | Done(DA08,50) |
| `DA_DAWN` | Done(DA09,500) |
| `DA_MACE` | Done(DA10,200) |
| `DA_ALTAR_DOWN` | Done(DA10,210) |
| `DA_HOH_END` | Comp(DA10) or Done(DA10,500) or Done(DA10,550) |
| `DA_NAMIRA_ATE` | Done(DA11,100) |
| `DA_NAMIRA_NO` | Done(DA11,250) or Done(DA11,500) |
| `DA_PERYITE` | Done(DA13,100) |
| `DA_WABBA` | Comp(DA15) |
| `DA_ERANDUR` | Done(DA16,200) |
| `DA_SKULL` | Comp(DA16) and not Done(DA16,200) [UNC: kill-Erandur completion stage not traced; fallback Erandur actor `GetDead`, NPC FormID to look up] |
| `GORE_NOT_RESCUED` | `HD1MemoriesRestored (0AF3FA:Gore - Vigilant.esp) == 0` (Gore not yet past his Coldharbour arc; after it he mocks Bal openly, VG72) |
| `WIELD:<item>` | player has the item equipped during the fight (GetEquipped). Dawnbreaker / Wabbajack FormIDs to pull at build [UNC] |

Locations (all [UNC] FormIDs, look up at build): `LOC:ShrineAzura`, `LOC:SilusHouse` (Mythic Dawn Museum, Dawnstar), `LOC:Kilkreath` (Kilkreath Ruins interiors), `LOC:HoH` (Markarth abandoned house, `MarkarthAbandonedHouse`), `LOC:Bthardamz`, `LOC:Dawnstar` (`DawnstarLocation`), `LOC:AnyDaedricShrine` = any of: Shrine of Azura, Sacellum of Boethiah, Shrine of Peryite, Shrine of Namira (Reachcliff Cave), Statue to Meridia, Shrine of Mehrunes Dagon (excluded whenever Kaidan is in the talk; see silence).

## 3. Silence windows (add to WorldQuiet while true)

- DA01 stage 70..99 (inside Azura's Star; followers are not there).
- DA02 stage 7..12 while in the Sacellum of Boethiah location (pillar, possession, cultist brawl).
- DA05 stage 70..99 in Bloated Man's Grotto (the hunt).
- DA07 stage 70..99, and **any talk with Kaidan in it** while `In(ShrineofMehrunesDagon 0240E6)` (kaidan_block.md §2a / §4; his KMD quest owns that place).
- DA10 stage 80..199 while `In(LOC:HoH)` (caged, Logrolf).
- DA11 stage 50..99 in Reachcliff Cave (the feast).
- DA15 stage 100..199 (Pelagius' mind; player is alone).
- DA16 stage 140..179 (Dreamstride) and 190..199 (Vaermina's choice, the ritual).
- Gore never appears in a DA talk while `GetQuestRunning HD1GoreFearAndLoathing (AFF592:GORE.esp)`; no DA talk mentions Gore at the House of Horrors.

## 4. Table

### Part 1 - What the party thinks of Daedra
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA1 | G L P | T | DA_ANY |
| DA2 | X K | T | DA_ANY |
| DA3 | A G P | T | DA_ANY; ASHE_REVEAL |
| DA4 | V X | T | DA_TWO |
| DA5 | P K I | T | DA_ANY |
| DA6 | L S | T | DA_TWO; DG_END; S following |
| DA7 | C G | T | DA_TWO; GORE_NOT_RESCUED; after R5 |
| DA8 | R A | T | DA_TWO; ASHE_REVEAL |
| DA9 | A K | T | DA_ANY; NOT_KMD |
| DA10 | G I P | T | DA_TWO |

### Part 2 - Azura
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA11 | V P | E LOC:ShrineAzura | Done(DA01,10) |
| DA12 | R L | T | Done(DA01,30); not Done(DA01,70) |
| DA13 | K P | T | DA_STAR_PURE or DA_STAR_BLACK |
| DA14 | A R P | T | DA_STAR_PURE; ASHE_REVEAL |
| DA15 | X S | T | DA_STAR_BLACK; DG_CAIRN; S following; after DG40 if it exists [UNC] |

### Part 3 - Boethiah
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA16 | G V | T | Done(DA02,5); not Done(DA02,50); after A22 |
| DA17 | K X | T | Done(DA02,7); not Done(DA02,10); not in the Sacellum location |
| DA18 | A G P | T | DA_BOE |
| DA19 | I L | T | DA_BOE (play at least 1 game day after stage 50) |
| DA20 | K G | T | Done(DA02,10); not in the Sacellum location |

### Part 4 - Clavicus Vile and Barbas
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA21 | K G | T | DA_BARBAS |
| DA22 | C P | T | DA_BARBAS |
| DA23 | V P | T | Done(DA03,70) |
| DA24 | K R | T | DA_MASQUE |
| DA25 | V S | T | DA_MASQUE; S following |
| DA26 | K G | T | DA_AXE |
| DA27 | R X P | T | Comp(DA03); Remi and Xelzaz not fallen out |

### Part 5 - Hermaeus Mora
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA28 | V A P | T | Done(DA04,40); not Done(DA04,100); ASHE_REVEAL |
| DA29 | L K P | T | DA_OGHMA |
| DA30 | R K | T | Done(DA04,100) or Done(DA04,105) |
| DA31 | V P | T | DA_OGHMA; VAL_FATHIS |
| DA32 | A X | T | DA_OGHMA |

### Part 6 - Hircine
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA33 | C P | T | Done(DA05,20); not Comp(DA05); not Done(DA05,205); RC_WEREPIG |
| DA34 | L I | T | Done(DA05,20); not Comp(DA05) |
| DA35 | G K | T | Comp(DA05) (100, 101 or 105) |
| DA36 | A P | T | DA_SINDING_KILLED |
| DA37 | S K | T | DA_SINDING_SPARED; S following |
| DA38 | R L | T | Comp(DA05); RC_WEREPIG |

### Part 7 - Malacath
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA39 | G A | T | Done(DA06,200) (Volendrung) |
| DA40 | G K | T | CT_END |
| DA41 | C P | T | CT_END; Done(DA06,100) (giant killed) |

### Part 8 - Mehrunes Dagon
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA42 | L R P | E LOC:SilusHouse | Done(DA07,10); not Comp(DA07) |
| DA43 | G K | T | Done(DA07,13); not Done(DA07,50); NOT_KMD |
| DA44 | K P | T | Done(DA07,50); not Done(DA07,70); not In(0240E6); NOT_KMD |
| DA45 | X V | T | DA_RAZOR |
| DA46 | I K | T | DA_RAZOR_REFUSED; not In(0240E6) |
| DA47 | L K P | T | Comp(DA07); KMD_DONE; after CC20 if Lucien has played it [optional] |
| DA48 | G K | T | DA_RAZOR; KMD_DONE |

### Part 9 - Mephala
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA49 | V R | T | Done(DA08,10); not Done(DA08,45) |
| DA50 | G I | T | Done(DA08,25) |
| DA51 | V K P | T | DA_BLADE_KEPT; after A2 |
| DA52 | L P | T | DA_BLADE_GONE |
| DA53 | S V | T | DA_BLADE_KEPT or DA_BLADE_GONE; S following |
| DA54 | A X | T | Done(DA08,25) |

### Part 10 - Meridia
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA55 | S P | T | Done(DA09,50); not DA_DAWN; SER_VAMP; S following |
| DA56 | R L | E LOC:Kilkreath | Done(DA09,300); not DA_DAWN |
| DA57 | K S | T | DA_DAWN; SER_VAMP; S following |
| DA58 | X P | T | DA_DAWN |
| DA59 | C G | T | Done(DA09,100); not Done(DA09,300) |
| DA60 | K P | T | DA_DAWN; K_TOG+ |

### Part 11 - Molag Bal (Gore never speaks here)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA61 | L R | E LOC:HoH | Done(DA10,10); not Done(DA10,80) |
| DA62 | K X P | T | DA_HOH_END; not In(MarkarthLocation) |
| DA63 | R S | T | DA_HOH_END; S following; Serana was following during DA10 80 [UNC: controller snapshot; else drop that check] |
| DA64 | V I | T | DA_MACE; VAL_FATHIS |
| DA65 | K L | T | DA_ALTAR_DOWN |
| DA66 | K P | T | DA_HOH_END; not In(MarkarthLocation) |

### Part 12 - Namira
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA67 | I X | T | Done(DA11,10); not Done(DA11,50) |
| DA68 | L K | T | Done(DA11,30); not Done(DA11,50) |
| DA69 | C X | T | DA_NAMIRA_ATE |
| DA70 | G R | T | DA_NAMIRA_NO |
| DA71 | X V P | T | Done(DA11,50) or Done(DA11,500); not in Reachcliff Cave |

### Part 13 - Nocturnal
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA72 | V R | T | TG_JOIN |
| DA73 | C I | T | Comp(TG09 021555) |

### Part 14 - Peryite
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA74 | I P | T | Done(DA13,10); not Comp(DA13); not Done(DA13,101) |
| DA75 | R V | T | Done(DA13,20) or Done(DA13,40); not Comp(DA13) |
| DA76 | R I | E LOC:Bthardamz | Done(DA13,40); not Comp(DA13) |
| DA77 | K X | T | DA_PERYITE |

### Part 15 - Sanguine
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA78 | G V P | T | DA14 |
| DA79 | R A | T | DA14; ASHE_REVEAL |
| DA80 | K P | T | Done(DA14,10); not Comp(DA14) (followers rejoin after the temple) |
| DA81 | G K | T | DA14; after Gore's own DA14 reaction (`GoreDA14VAR ABA0A0:GORE.esp` back to 0) [UNC] |

### Part 16 - Sheogorath
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA82 | V P | T | Done(DA15,10); not Done(DA15,100) |
| DA83 | I P | T | DA_WABBA (WS123 calls back to this talk: keep it before WS123 if both are eligible) |
| DA84 | I G | E AFTERFIGHT | DA_WABBA; WIELD:Wabbajack during the fight; after C2 |
| DA85 | C L | T | DA_WABBA |
| DA86 | L A | T | DA_WABBA; ASHE_REVEAL |
| DA87 | X P | T | DA_WABBA |

### Part 17 - Vaermina
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA88 | G I | E LOC:Dawnstar | Done(DA16,20); not Comp(DA16) |
| DA89 | L K | T | Done(DA16,100); not In(Nightcaller Temple) ; NOT_KMD |
| DA90 | K P | T | DA_ERANDUR; KMD_DONE |
| DA91 | S X | T | DA_SKULL; S following |
| DA92 | G A | T | Done(DA16,180); ASHE_Q1 |

### Part 18 - Barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA93 | L K | E AFTERFIGHT:dremora | DA_ANY |
| DA94 | X V | E AFTERFIGHT:cultist (target in a Daedric cultist faction: Namira coven, Boethiah, Vaermina, Peryite Afflicted, Mythic Dawn) [UNC faction IDs] | DA_ANY |
| DA95 | C V | E AFTERFIGHT:atronach | after R8 |
| DA96 | K S | E AFTERFIGHT:undead | DA_DAWN; WIELD:Dawnbreaker; SER_VAMP; S following |
| DA97 | I A | E AFTERFIGHT | DA_WABBA; WIELD:Wabbajack; ASHE_REVEAL |
| DA98 | L R | E LOC:AnyDaedricShrine | DA_ANY or first shrine arrival |
| DA99 | I K | E AFTERFIGHT:werewolf | — |
| DA100 | C G | E AFTERFIGHT:dremora or daedra (LocTypeOblivion / any Daedra race) | GORE_NOT_RESCUED; after R5 |

## 5. Open items
- DA03 205 vs 155 as the "Barbas killed" marker.
- DA16 kill-Erandur completion stage (stage 200 may carry a second log entry; read `Stages[...].LogEntries[1]` at build).
- DA05 101 (the CH_IMBM "justice" ending): treated as "Sinding dead" only for DA35; DA36 needs 100 (the Savior's Hide).
- Location and faction FormIDs marked [UNC] above.
- DA63's "Serana was there" snapshot is optional; the talk reads fine without it.
