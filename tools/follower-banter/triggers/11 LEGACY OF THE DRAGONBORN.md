# 11 LEGACY OF THE DRAGONBORN - trigger rows (prefix LT, 140 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\11 LEGACY OF THE DRAGONBORN.txt`
Research: `research\content\lotd.md` (all stage numbers and FormIDs below come from it; plugin = LegacyoftheDragonborn.esm, runtime slot 14).
Gate codes from `TRIGGERS.md` section 4. Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap; "+Luna" = the player line (Eleonora voice), no extra gate.

## Local codes (this file only)

**Global for every LT talk:** `WorldQuiet()` + `Free(x)` from TRIGGERS.md sections 2-3, plus **`LT_QUIET`** = none of these is true (lotd.md section 3):
- DBM_LALStart 15 done and 20 not done (arrival tour)
- DBM_MuseumIntroTour (124FC4) running; any radiant tour quest 08F978..08F97D running
- DBM_MuseumGala (0F0DC8) 10 done and 100 not done [check in game that 10 is the start]
- DBM_ExplorerGuildHouse (3431C3) 15 done and 30 not done (Guildhouse tour)
- DBM_hauntedMuseumQuest (7AC75C) 65 done and 80 not done (nightmare: **hard silent**); 15..104 = only LT110 may play, at low chance
- DBM_MuseumHeist (33D940) 33 done and 45 not done
- DBM_VigilantsQuest1 (0F0D34) 2 done, not completed, AND player in MUSEUM
- DBM_MuseumIndarysQuest (371C28) 55 done and 100 not done
- DBM_Excavation01 (4D1811) 142 done and 150 not done
- DBM_Excavation02 (58B96A) 90 done and 140 not done while in Rkund cells (504BBE, 505676, 50A049, 50F330, 50FE29, 50FE28)
- DBM_Excavation03Prelude (2702DC) 1 done and 15 not done
- DBM_MuchAdoAboutSnowElves (5C7E75) 310 done and 400 not done
- DBM_Excavation03A (2702EE) 61 done and 75 not done (**hard silent**); 75..79 = only LT93 may play; 140 done and 175 not done; 300 done and 350 not done
- DBM_EchosOfMadness (4E0D3F) 30 done and 45 not done
- DBM_ShatteredLegacy (121573) 225 done and 250 not done; 260 done and 265 not done; 280 done and 300 not done
- DBM_PlanetariumQuest (5867FC) 46 done and 50 not done
- DBM_WaystoneQuest (16658E) 10 done and 20 not done
- any LOTD staff/explorer NPC within 1000 units `IsInScene` (DBM_ExplorerScene## / DBM_MuseumScene##), or the player in dialogue with Auryen, Avram or an explorer

**Places** (`GetInCurrentLocation` unless a cell is named):
- `MUSEUM` = DBM_DragonbornGalleryLocation 1432E2 (children count; if not, OR the room list)
- `M_HOH` Hall of Heroes 5D2D83 · `M_LIB` Library 5D2D88 · `M_NAT` Natural Science 5D2D87 · `M_ARM` Armory 5D7E90 · `M_DBH` Dragonborn Hall 5D7E94 · `M_HOS` Hall of Secrets 5D7E95 · `M_SAFE` Safehouse 139074 · `M_PLAN` Planetarium 5D7E92
- `M_DAED`, `M_ODD`, `M_HOLE` = East Exhibit Halls 5D2D82, split by wing. **[unconfirmed]** all three share cell 125C71; needs trigger boxes or distance to tour markers TourDG / TourHOO / TourStopHOLE. Fallback: any of the three wing talks may fire anywhere in 5D2D82.
- `GUILD` Guildhouse 5D7E91 · `DEEPHOLME` 66B745 · `AIRSHIP` Dev Aveza 66B743 · `FS_NORTH` Northern field station 34D523
- `NEAR:<npc>` = GetDistance < 1500 to that LOTD NPC's ref while in MUSEUM. **[unconfirmed]** patron ref FormIDs (Henry, Asterion/Asterell, Radcliff, Gordrak, Lolette, Cedric/Verna, Marcus Flynn) not looked up yet; fallback = timer talk in M_HOH.

**Story:**
- `LT_HIRED` = GetQuestCompleted DBM_MuseumIntro (17211B) OR DBM_LALStart (3F14FC) 35 done
- `LT_EARLY` = not LT_HIRED (museum still mostly empty)
- `EXPL` = DBM_ExplorerGuildmembers (34D50B) completed (10 or 100)
- Quest names are shortened: MuchAdo = DBM_MuchAdoAboutSnowElves, Exc01/02/03A, SL = DBM_ShatteredLegacy, Haunt = DBM_hauntedMuseumQuest, Heist = DBM_MuseumHeist, Vig1 = DBM_VigilantsQuest1, EoM = DBM_EchosOfMadness, HoG = DBM_HandofGloryQuest, Gala = DBM_MuseumGala.
- Pair meet chains: `after A1/A2/...` = that batch talk already played. `KI` = KaiandInigo stage >= 10. `LI` = JRLucienInigoRank >= 2. `LX` = Lucien-Xelzaz intro in BPUFXelzazAndLucienInteractions done. `RX` = Remi/Xelzaz not fallen out (BPUFXelzazRemielFallenOut != 1). `RG_SIS` = Remi-Gore "sister" scene (HLIOGoreBanter Scene8) done **[stage unconfirmed]**.

## Table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| LT1 | L C +Luna | E MUSEUM (entry) | LT_EARLY; after R11 |
| LT2 | G V +Luna | E MUSEUM (entry, first with Val) | after A3 |
| LT3 | G K +Luna | T | DBM_MuseumIntro 20 done and not completed; after A1 |
| LT4 | X I | T | LT_HIRED; after X6 |
| LT5 | I K | E M_HOH | KI |
| LT6 | G X | E M_HOH | after X1 |
| LT7 | L V | E MUSEUM | LUC_ADMIT; after C1 |
| LT8 | R I +Luna | E MUSEUM | LT_HIRED; after B6 |
| LT9 | G C | E MUSEUM | DBM_MuseumIntroTour ran and is stopped [needs a "tour seen" flag, unconfirmed]; after R5 |
| LT10 | K V +Luna | E MUSEUM | K_CRUSH; after A2 |
| LT11 | G L | E M_HOH | after L1, L2 |
| LT12 | C K +Luna | E M_HOH | after R1 |
| LT13 | I X | E MUSEUM | after X6 |
| LT14 | L G X | E M_DAED | after L1, X1; LX |
| LT15 | G K | E M_DAED | DA10 completed (Mace obtained; proxy for "on display") [unconfirmed]; after A1 |
| LT16 | C X | E M_DAED | after R18 |
| LT17 | V I | E M_DAED | after I1 |
| LT18 | L +Luna | E M_DAED or M_HOH | - |
| LT19 | I L | E M_ODD | LI |
| LT20 | C I K | E M_ODD | after R1, R13; KI |
| LT21 | I X | E M_ODD | after X6 |
| LT22 | R L +Luna | E M_HOLE | after B10 |
| LT23 | R G | E M_HOLE | RG_SIS |
| LT24 | G K | E M_HOLE | after A1 |
| LT25 | L I | E M_HOLE | LI |
| LT26 | L I +Luna | E M_LIB | LI |
| LT27 | L G +Luna | E M_LIB | after L1 |
| LT28 | K X | E M_LIB | after C3 |
| LT29 | V K +Luna | E M_LIB | K_TOG+; after A2 |
| LT30 | X G +Luna | E M_LIB | after X1 |
| LT31 | X R | E M_NAT | RX |
| LT32 | G X | E M_NAT | after X1 |
| LT33 | C L | E M_NAT | after R11 |
| LT34 | C V +Luna | E M_NAT | after R9 |
| LT35 | V G K | E M_NAT | after A1, A2, A3 |
| LT36 | R I +Luna | E M_NAT | after B6 |
| LT37 | G L +Luna | E M_NAT | after L1 |
| LT38 | K X | E M_NAT | winter (GameMonth 11, 0, 1) or SNOW outside; after C3 |
| LT39 | G K +Luna | E M_ARM | after A1 |
| LT40 | K +Luna | E M_ARM | K_TOG+ |
| LT41 | I G | E M_ARM | after C2 |
| LT42 | G V K | E M_DBH | DB; after A1, A2, A3 |
| LT43 | L X +Luna | E M_DBH | DB; LX |
| LT44 | I K C | E M_HOS | DBM_HOSDiscoveryQST (0A9247) completed; KI; after R1, R13 |
| LT45 | L R +Luna | E M_HOS | DBM_HOSDiscoveryQST completed; after B10 |
| LT46 | L X +Luna | E M_PLAN | DBM_PlanetariumQuest completed (50 or 100); LX |
| LT47 | C I | E M_PLAN | DBM_PlanetariumQuest completed; after R13 |
| LT48 | K G +Luna | E after a display is placed [no display hook found; fallback T in MUSEUM, LT_HIRED] | after A1 |
| LT49 | L V | T exterior | LT_HIRED [ideally: player carries a displayable relic, unconfirmed]; after C1 |
| LT50 | X +Luna | E MUSEUM + hour 1..4 | LT_HIRED |
| LT51 | G C +Luna | T in MUSEUM | LT_HIRED; after R5 |
| LT52 | K R +Luna | T in MUSEUM | LT_HIRED; after B1 |
| LT53 | C K | E NEAR:Henry | after R1 |
| LT54 | G R | E NEAR:Asterion/Asterell | RG_SIS |
| LT55 | G X | E NEAR:Radcliff | after X1 |
| LT56 | G K | E NEAR:Gordrak gro-Shor | after A1 |
| LT57 | I V +Luna | E NEAR:Lolette Astrada | after I1 |
| LT58 | R L | E NEAR:Cedric/Verna | after B10 |
| LT59 | X I | T in MUSEUM + MORNING (after-meal check unconfirmed) | after X6 |
| LT60 | G V | T in MUSEUM | GORE_BAIL; after A3 |
| LT61 | C I | E M_HOH | after R13 |
| LT62 | K I | E NEAR:Marcus Flynn | KI |
| LT63 | K V G | E M_SAFE (first entry with all three) | K_CRUSH; after A1, A2, A3 |
| LT64 | C I | E M_SAFE | after R13 |
| LT65 | I R | E M_SAFE | DBM_ImbuningMachine (16658A) 15 done; after B6 |
| LT66 | I G | E M_SAFE, first night the player sleeps there | after C2 |
| LT67 | V R +Luna | E M_SAFE | HLIOValRemiFriendshipTracker >= 2 (business partners) |
| LT68 | R K +Luna | E M_SAFE | after B1 |
| LT69 | C X | E MUSEUM + NIGHT | after R18 |
| LT70 | G K +Luna | T | DBM_ExplorerGuildHouse completed (30 or 100); after A1 |
| LT71 | X I | E GUILD + hour 18..21, exterior balcony if checkable | DBM_ExplorerGuildHouse completed; after X6 |
| LT72 | L G | T | DBM_ExplorerGuildmembers 5 done and not completed; after L1 |
| LT73 | X R | E GUILD | EXPL; RX |
| LT74 | I K | E GUILD | EXPL; KI |
| LT75 | V I | E GUILD | EXPL; after I1 |
| LT76 | K G | E GUILD | EXPL; after A1 |
| LT77 | C I | E GUILD | Exc01 150 done; after R13 |
| LT78 | X K | E FS_NORTH | DBM_ExplorerFieldStation01 (2AD9CD) 15 done; after C3 |
| LT79 | G K | E GUILD + hour 18..23 | EXPL; after A1 |
| LT80 | G L | E GUILD | EXPL; Exc03A 61 NOT done; after L1 |
| LT81 | K L | T | Exc01 47 done and 150 not done |
| LT82 | I G | T | Exc01 141 done and 142 not done (or 150 done); after C2 |
| LT83 | G K +Luna | T | Exc01 150 done; after A1 |
| LT84 | K X G | T | Exc02 80 done; after A1, C3, X1 |
| LT85 | G L | T | Exc02 140 done; after L1 |
| LT86 | L R | T | Exc02 140 done; after B10 |
| LT87 | I R +Luna | T | Exc02 140 done; after B6 |
| LT88 | I K | T | MuchAdo 102 done; KI |
| LT89 | L G +Luna | T | MuchAdo 200 done and 207 not done [loop end stage unconfirmed]; after L1 |
| LT90 | L X | T | MuchAdo 410 done; LX |
| LT91 | V K +Luna | T | Exc03Prelude 15 done and Exc03A 61 not done; K_TOG+; after A2 |
| LT92 | G C | T | Exc03A 5 done and 61 not done; after R5 |
| LT93 | K +Luna | T (once, first tick after 75) | Exc03A 75 done (allowed inside the 75..79 grief window) |
| LT94 | G I X | E M_HOH | Exc03A 80 done; after C2, X1, X6 |
| LT95 | R G | E CAVE or DWEMER | Exc03A 80 done; RG_SIS |
| LT96 | C L | T | Exc03A 80 done; after R11 |
| LT97 | G X | T | Exc03A 175 done; after X1 |
| LT98 | K G +Luna | T | Exc03A 350 done; after A1 |
| LT99 | C L | T | Exc03A 350 done; after R11 |
| LT100 | K V | T | DBM_PhynasterRingQST (2A36E4) 10 done; after A2 |
| LT101 | X I | T | DBM_SpearofthSnowPrinceQuest (289BEA) completed (10 or 30); after X6 |
| LT102 | X K | T | SL 10 done; after C3 |
| LT103 | X C G | T | SL 75 done; after X1, R5, R18 |
| LT104 | K G | E Pale Pass 45CC3C, else T | SL 50 done; after A1 |
| LT105 | L R +Luna | T | SL 250 done; after B10 |
| LT106 | I X K | E first NIGHT tick | SL 250 done; KI; after C3, X6 |
| LT107 | K G | T | SL 265 done; after A1 |
| LT108 | L K +Luna | T | SL 300 done |
| LT109 | C I | T | SL 300 done; after R13 |
| LT110 | L R | E MUSEUM + NIGHT, 1-in-4 roll | Haunt 15 done and 60 not done; after B10 |
| LT111 | G I C | T | Haunt 80 done; after C2, R5, R13 |
| LT112 | K X | T | Haunt completed (110); after C3 |
| LT113 | C L +Luna | E MUSEUM + NIGHT | Haunt completed; after R11 |
| LT114 | C V R | E MUSEUM | Heist 10 done and 33 not done; after R8 |
| LT115 | I K | T | Heist 45 done; KI |
| LT116 | G X | T | Heist completed (60); GORE_FATHER; after X1 |
| LT117 | L G +Luna | E MUSEUM | Heist 50 done; after L1 |
| LT118 | G K | T, NOT in MUSEUM | Vig1 2 done and not completed; after A1 |
| LT119 | X V I | T | Vig1 completed AND any of 180..192 done (accidents branch); after X4, X6, I1 |
| LT120 | R L | T | Vig1 completed AND 120 done (originals handed over); after B10 |
| LT121 | V K | T | Vig1 completed AND (40 done OR any 150..159 done) AND none of 180..192 / 250..253 done; after A2 |
| LT122 | G C | T | Vig1 any of 250..253 done (fight branch); after R5 |
| LT123 | X I | E MUSEUM | EoM 10 done and 30 not done; after X6 |
| LT124 | C L +Luna | T | EoM 100 done; after R11 |
| LT125 | G L I | E at a survey dig marker (DBM_SurveyorHandler 1C6621 running) [marker proximity unconfirmed] | after C2, L1; LI |
| LT126 | C V | E WATER + coast, Merrian's Spyglass owned (Beachcombing) [unconfirmed check] | after R9 |
| LT127 | G V | E DEEPHOLME | DBM_DHQuest (9211FD) 10 done; after A3 |
| LT128 | G X C | E AIRSHIP | DBM_MuseumIndarysQuest completed (100); after X1, R5, R18 |
| LT129 | L I +Luna | E AIRSHIP | DBM_MuseumIndarysQuest completed; LI |
| LT130 | I K | T | HoG 30 done (or 50); KI |
| LT131 | G X +Luna | T | HoG 20 done AND DBM_HOGCleanseQuest (08F9D7) not completed; after X1 |
| LT132 | C K | T | DBM_OngarKegbreaker (33D941) 30 done; RC_REDGOD; after R1 |
| LT133 | L G +Luna | T | DBM_ExplorerRelicFindQST (7BFED0) 10 done [Deano's pack item check unconfirmed]; after L1 |
| LT134 | X L | T | Auryen's Notes quest for the Bloodworm Helm 30 or 50 done [which DBM_AMJournalQST## is unconfirmed]; LX |
| LT135 | R G +Luna | T | Auryen's Notes, Tools of Kagrenac, 45 or 50 done [journal number unconfirmed]; RG_SIS |
| LT136 | V X +Luna | T | DBM_KOTNQuest (9211C7) 7 done; after X4 |
| LT137 | K R | T | Gala 5 done and 10 not done; K_CRUSH; after B1 |
| LT138 | G X +Luna | T | Gala 100 done; after X1 |
| LT139 | V K +Luna | T | Gala 100 done; K_TOG+; after A2 |
| LT140 | G K I | E MUSEUM | Exc01 150, Exc02 140, Exc03A 350 and SL 300 all done; after A1, C2; KI |

## Open items
- Room split inside the East Exhibit Halls (M_DAED / M_ODD / M_HOLE) needs trigger boxes or tour-marker distances.
- Patron NPC refs for NEAR: checks.
- "Display placed" (LT48), "tour seen" (LT9), "after a meal" (LT59), Beachcombing (LT126) and dig-marker (LT125) checks have no confirmed hook; fallbacks noted in the rows.
- Which Auryen's Notes quest is the Bloodworm Helm and which is Kagrenac (DBM_AMJournalQST01..10).
- DBM_MuseumGala stage 10 as the start of the gala scene: confirm in game.
- LT15: confirm the Mace of Molag Bal display can be read (DA10 completed is only a proxy).
