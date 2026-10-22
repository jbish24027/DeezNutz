# Triggers - 13 WYRMSTOOTH SIRENROOT FORGOTTEN CITY SAINTS (prefix WS, 160 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\13 WYRMSTOOTH SIRENROOT FORGOTTEN CITY SAINTS.txt`
Research: `research\content\bruma_moonpath_wyrmstooth_etc.md` sections 3-7. Global gate codes: `TRIGGERS.md` section 4. All FormIDs are plugin-qualified; never use runtime IDs.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, **U = Luna (the player, voiced by Eleonora)**. Luna is never a Free() check; she is the player.
Type: T = timer, E = event. `E COMBAT` = a short fight bark that plays DURING combat; this needs a combat-bark path (the normal talk scenes use CombatEnd) - **[unconfirmed: build a separate bark scene without CombatEnd, or play on combat start]**.
"[unconfirmed]" = could not be proven from the records; check in game or at build.
Every row also obeys `WorldQuiet()` and `Free(x)` from TRIGGERS.md sections 2-3.

## 1. Local gate codes

### Wyrmstooth (`Wyrmstooth.esp`, ESM-flagged)
| Code | Condition |
|---|---|
| WT_HUNT | `WTDragonHunt 022528:Wyrmstooth.esp` stage 10 done, 100 not done. **[unconfirmed]** which stage the mercenaries join you on the Falkreath road; use "mercenary aliases filled / within 2000 units" if available |
| WT_FLED | `022528` stage 110 done (the dragon fled to Wyrmstooth) |
| WT_ARRIVED | `WTBarrowOfTheWyrm 028F01:Wyrmstooth.esp` stage 50 done ("We've arrived at Wyrmstooth.") |
| WT_ISLAND | GetInWorldspace `WyrmstoothWorld 000D62:Wyrmstooth.esp` (or location `WTWyrmstoothLocation 2CEC4A`); WT_ARRIVED |
| WT_STONEHOLLOW | `028F01` stage 70 done |
| WT_GOREDUSTER | `028F01` stage 100 done |
| WT_ALBERTHOR | `028F01` stage 120 done |
| WT_POSSESSED | `028F01` stage 160 done (the draugr-possession window 135..159 is over) |
| WT_DIMFROST | GetInWorldspace `Dimfrost 0825E1:Wyrmstooth.esp` |
| WT_DEAD | `028F01` stage 260 done |
| WT_DONE | `028F01` stage 270 done |
| WT_FORT | `WTPlayerHome 28D0B5:Wyrmstooth.esp` stage 20 done (Fort Valus deed bought). Fort Valus location FormID **[unconfirmed]** |
| Side quests | `WTTheNakedNord C651DA`, `WTUberEncounter 2F1A74`, `WTPricelessCommodity 48F992`, `WTWolfFollower 2E49AF`, `WTKillThalmor 3943A0`, `WTWrapMeUp 3920D5`, `WTAthirFavor 3A1467`, `WTShargamFavor 3A1468`, `WTDaenlitFavor 3A1469`, `WTElmeraFavor 3A146A`, `WTSignyFavor B5DA18`, bounties `4B9DED..4B9DF0` (all `:Wyrmstooth.esp`) |
| Named places | Stonehollow, Hag's Perch, Abandoned Lighthouse, Fort Moonwatch, Krakevisa, Bloodfrost Burrow, Wyrmstooth Barrow, the island's Dark Brotherhood sanctuary, the Ascend hidden peaks: location FormIDs **[unconfirmed]**; resolve by EditorID at build |

**Wyrmstooth silence:** `028F01` stages 10..49 (boat crossing), 135..159 (player's mind in a draugr), 230..269 (Stonehollow defence and reward; only WS56 and WS57 barks may play in 230..259). Wyrmstooth moves followers itself inside the barrow; never start a talk if a speaker is not within 1000 units.

**Xelzaz:** his own `BPUFXelzazFollowerWyrmstooth.esp` has ~60 lines (courier, gold split, trap, EEC, Helgen, Goreduster as a key, Alberthor, riddle, dead Thalmor, the Oblivion gate and Dagon, Dimfrost vs Blackreach, spiddal sticks). The WS talks with Xelzaz (WS31, WS43, WS50, WS54) stay off those topics.

### Sirenroot (`evgSIRENROOT.esm`)
| Code | Condition |
|---|---|
| SR_HIRED | `EVGSirenrootQuest 026BC5:evgSIRENROOT.esm` stage 5 done |
| SR_CAMP | stage 10 done, 15 not done (team found, before the dive). Dive camp is north of the Riften docks by Merryfair Farm: exterior, near the camp marker **[unconfirmed marker FormID]** |
| SR_BACK | stage 140 done (escaped the flooding ruins) AND the follower is within 1000 units of the player AND the player is not in any `evgSIRENROOT.esm` cell. "Reunion" talks (WS69-WS75) fire the first time each follower meets this condition, once only |
| SR_PAID | stage 150 done |

**Sirenroot silence:** stage 15 until 140 = **silence for every follower talk**. Stage 20 moves only the player (followers stay behind on the shore); 45 = trance cell `01750A` (EVGSirenDaydream); NPC-control sections; 130..139 flooding escape. No WS talk is set inside the Honrich cells (`025FD4, 000D61, 009086, 0162FC, 02B77F, 031168, 075AB5, 0845FD, 014076, 0A625E, 12DC10, 01750A`).

**Xelzaz:** has ~150 Sirenroot lines of his own (diving, the plant, the team, Krill, his reunion, trance, soul gem, Peletius, Ayleid vs Dwemer, Morag Tong, faux flora, no more diving). He is in **no** WS Sirenroot talk.

### The Forgotten City (`ForgottenCity.esp`, location in the light plugin `Liv_ForgottenCity_AddLocations.esp`)
| Code | Condition |
|---|---|
| FC_EDGE | player in cell `Forgotten Ruins 000D62:ForgottenCity.esp` AND `000FCQuest01 012BB9:ForgottenCity.esp` stage 15 or 30 done AND stage 100 NOT done (before the leap of faith) |
| FC_END | the story is over and the player is back outside: player NOT in `ForgottenCityLocation 000800:Liv_ForgottenCity_AddLocations.esp` AND any of: `012BB9` stage 3000 or 4000 or 4050 done; `012BB9` completed or failed; `000FCQuestStatusCreditsPlayed 0E5786` stage > 0 **[unconfirmed which ending sets what; check each ending in game]** |
| FC_GOOD | `012BB9` stage 4050 done (Altrius returned to Cassia; she entered the city) |

**Forgotten City silence (the most important rule here): the whole `ForgottenCityLocation` is a NO-TALK ZONE from `012BB9` stage 100 (leap of faith) until FC_END**, including the past (`000FCQuest02 05965B` stage 400 done and 6000 not done), the loop resets (5000..5500), the Law-broken status (`0A7AE8`), the credits (`0E5786`) and the quarry/Arbiter window (`094809` 20..30). The mod has no follower code and the author designed it solo; followers did not live the loop, so none of their lines claim to remember it. The only FC talks are FC_EDGE (before the jump) and FC_END (after).
**Golden Rule chain:** WS103 must play before WS105-WS108 (the party learns the rule from Luna first).

### Saints and Seducers, Extended Cut (`Skyrim Extended Cut - Saints and Seducers.esp`, below written "SEC")
| Code | Condition |
|---|---|
| SS_ISLES | GetInWorldspace `ECSSShiveringIsles C2BFF8:SEC` (or location `EC_SS_ShiveringIslesLocation 0A5165:SEC`); `EC_SS_MQ100Int 099D18:SEC` stage 100 done |
| SS_DONE | `EC_SS_MQ102 09EF5F:SEC` stage 100 done |
| Others | `EC_SS_MQ101 099D19`, `EC_SS_MQ102 09EF5F`, `EC_SS_TheodorQuest 099D1A`, `EC_SS_LizardQuest 099D1B`, elytra pets `0010C3 / 0010C0:ccBGSSSE025-AdvDSGS.esm`. Mania vs Dementia side and Borogove: location/region FormIDs **[unconfirmed]** |

**SEC silence:** before `099D18` completes (Gore's own patch owns the sickness intro); `099D19` 30..39 (torture and rescue); `09EF5F` 80..99 (Well of Inversion and Staada's ending talk). Gore (34 lines) and Val (43 lines) already have SEC lines; WS talks avoid their topics (under Solitude, Sheogorath alarm, Root Canal pun, purple lady, smells, tomatoes, no-cheese, girlboss, Drinks-the-Skooma, Theodor's fashion, soul tomato, Joker taunts).

### The Cursed Tribe (`DA06 03B681:Skyrim.esm`, winning record from `The Cursed Tribe - Quest Expansion.esp`)
| Code | Condition |
|---|---|
| CT_START | DA06 stage 10 done; player in `LargashburLocation 019263:Skyrim.esm` for arrival events |
| CT_END | DA06 stage 200 or 210 done (either ending; every WS line is branch-neutral) |

**Cursed Tribe silence:** DA06 60..69 (ritual, Malacath speaks), 100..109 (Malacath at Fallowstone). 65..66 = ghost battle on the Bane of the Undead route: only the WS160 bark.

## 2. Per-talk table

### PART 1 - WYRMSTOOTH: THE HUNT AND THE BARROW
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS1 | G K | T | WT_HUNT; after A1 |
| WS2 | K U | E stage set 022528 110 (or next tick) | WT_FLED |
| WS3 | L K | T | WT_FLED; WT_ARRIVED not done; after K5 or Lucien-Kaidan intro |
| WS4 | R U | T | WT_FLED; WT_ARRIVED not done |
| WS5 | C I | E arrival (028F01 stage 50 set, or first exterior tick in WyrmstoothWorld) | WT_ARRIVED; after R13 |
| WS6 | V G | E arrival | WT_ARRIVED; after A3 |
| WS7 | C K | T | WT_ISLAND exterior; after R1 |
| WS8 | R U | E exterior + SNOW or near shore | WT_ISLAND |
| WS9 | G K | E stage set 028F01 70 (or arrival in Stonehollow) | WT_STONEHOLLOW |
| WS10 | G V | T | WT_GOREDUSTER |
| WS11 | R L U | T | WT_GOREDUSTER; after B10 |
| WS12 | L K | T | WT_ALBERTHOR; after K5 or Lucien-Kaidan intro |
| WS13 | K U | E stage set 028F01 160 (or next tick) | WT_POSSESSED |
| WS14 | C U | E stage set 028F01 160 | WT_POSSESSED; after WS13 not required |
| WS15 | L U | T | WT_POSSESSED |
| WS16 | G I | T | WT_POSSESSED; after C2 |
| WS17 | R U | E arrival in Dimfrost worldspace | WT_DIMFROST; after WS4 |
| WS18 | I K | T | WT_DIMFROST; KaiandInigo stage >= 10 |
| WS19 | L G | E AFTERFIGHT:dragon priest, in Wyrmstooth Barrow | WT_GOREDUSTER; WT_DONE not done; after L1 |
| WS20 | V L | E near the gate in Wyrmstooth Barrow [unconfirmed ref] | WT_ALBERTHOR; after C1 |
| WS21 | R G | E after the flood room [unconfirmed stage/trigger box] | WT_ALBERTHOR; after B15 or Remi-Gore meet |
| WS22 | K I | E stage set 028F01 260 (next tick after combat) | WT_DEAD; KaiandInigo stage >= 10 |
| WS23 | L U | T | WT_DEAD |
| WS24 | V G U | E stage set 028F01 270 | WT_DONE |
| WS25 | V K | T | WT_ARRIVED; WT_DONE not done; after A2 |
| WS26 | I R | E Stonehollow location | WT_DEAD; after B6 |

### PART 2 - WYRMSTOOTH: FORT VALUS AND THE ISLAND'S JOBS
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS27 | V R I | E arrival at Fort Valus | WT_FORT; after B6 |
| WS28 | K G | E at Fort Valus | WT_FORT; after A1 |
| WS29 | K U | E at Fort Valus exterior | WT_FORT; K_TOG+ |
| WS30 | L G | T | WT_FORT; WTRebuild running [unconfirmed]; after L1 |
| WS31 | X K | E at Fort Valus | WT_FORT; after C3 |
| WS32 | V I | T | WTTheNakedNord stage 10 done, < 70; after I1 |
| WS33 | L K | T | WTTheNakedNord stage 30 done; after K5 or Lucien-Kaidan intro |
| WS34 | C G | T | WTTheNakedNord stage 10 done; after R5 |
| WS35 | L R | E stage set 2F1A74 40 (or next tick) | WTUberEncounter stage 40 done; after B10 |
| WS36 | C U | T | WTUberEncounter stage 20 done, 40 not done; after R1 |
| WS37 | G I | T | WTPricelessCommodity stage 10 done, 15 and 40 not done; after C2 |
| WS38 | R V U | T | WTPricelessCommodity stage 10 done, 15 and 40 not done |
| WS39 | C I | T | WTWolfFollower stage 40 done (Faelor following [unconfirmed check]); after R13 |
| WS40 | K U | T | WTWolfFollower stage 30 done |
| WS41 | G K | T | WTKillThalmor stage 10 done, 30 not done; after A1 |
| WS42 | L U | T | WTWrapMeUp stage 10 done, 30 not done |
| WS43 | X U | E AFTERFIGHT in Krakevisa or WTBounty (warlock) stage 20 | warlock bounty done or Krakevisa cleared |
| WS44 | R K | T | WTBounty (vampire) running; after B1 |
| WS45 | C G | E near Hag's Perch location | WT_ISLAND; after R5 |
| WS46 | V U | E arrival at the Abandoned Lighthouse | WT_ISLAND |
| WS47 | K U | E on a hidden peak [Ascend - Hidden Peaks; unconfirmed check] | K_CRUSH |
| WS48 | L I | E at Fort Moonwatch + NIGHT | WT_ISLAND; after Lucien-Inigo intro (JRLucienInigoRank >= 2) |
| WS49 | G V | E exterior, near shore | WT_ISLAND; after A3 |
| WS50 | G X | E SNOW, exterior | WT_ISLAND; after X1 |
| WS51 | G R | T | WTDaenlitFavor stage 10 done, 30 not done; after B15 or Remi-Gore meet |
| WS52 | G K | T | any of WTAthirFavor / WTShargamFavor / WTDaenlitFavor / WTElmeraFavor / WTSignyFavor stage 10 done; after A1 |
| WS53 | K U | T | WTAthirFavor stage 10 done |
| WS54 | X I | E near the sanctuary door [unconfirmed location] | WT_ISLAND; after X6 |
| WS55 | I U | E exterior + NIGHT on WT_ISLAND | WT_DONE |

### PART 3 - WYRMSTOOTH: FIGHT BARKS  (short, during fights)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS56 | K G | E COMBAT (in-fight bark path [unconfirmed]); 028F01 stage 230..259 | WT stage 230..259 |
| WS57 | L I | E COMBAT vs undead; 028F01 stage 230..259 | WT stage 230..259 |
| WS58 | R V | E COMBAT with a player-raised thrall nearby [unconfirmed check] | WT_GOREDUSTER; after Val-Remi intro (HLIOValBanter stage 10) |
| WS59 | I K | E COMBAT in Dimfrost | WT_DIMFROST; KaiandInigo stage >= 10 |
| WS60 | C G | E COMBAT vs vampire, in Bloodfrost Burrow | WT_ISLAND; after R5 |

### PART 4 - SIRENROOT: BEFORE THE DIVE
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS61 | K V | T | SR_HIRED; SR_BACK not done; after A2 |
| WS62 | L G U | E at the dive camp (near Merryfair Farm) [unconfirmed marker] | SR_CAMP; after L1 |
| WS63 | R C | E at the dive camp | SR_CAMP; after Redcap-Remi intro (FA01RemiIntroScene) |
| WS64 | G V | T | SR_CAMP; after A3 |
| WS65 | G I | E at the dive camp, near WATER | SR_CAMP; after C2 |
| WS66 | K U | E at the dive camp | SR_CAMP; K_CRUSH |
| WS67 | I K | E at the dive camp + NIGHT | SR_CAMP; KaiandInigo stage >= 10 |
| WS68 | R K | E at the dive camp | SR_CAMP; after B1 |

### PART 5 - SIRENROOT: YOU CAME BACK  (reunions after the cave-in)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS69 | K U | E reunion: SR_BACK and Kaidan within 1000 for the first time | SR_BACK; K_CRUSH |
| WS70 | K U | E reunion | SR_BACK; K_TOG+ |
| WS71 | R U | E reunion | SR_BACK |
| WS72 | I G | E reunion | SR_BACK; after C2 |
| WS73 | C U | E reunion | SR_BACK |
| WS74 | V G | E reunion or first tick after | SR_BACK; after A3 |
| WS75 | L U | E reunion | SR_BACK |
| WS76 | K V | T (first tick after reunion) | SR_BACK; after A2 |
| WS77 | L I | T | SR_BACK; Lucien-Inigo intro done |
| WS78 | L K | T | SR_BACK; after K5 or Lucien-Kaidan intro |

### PART 6 - SIRENROOT: WHAT HAPPENED DOWN THERE
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS79 | R G | T | SR_BACK; after B15 or Remi-Gore meet |
| WS80 | L U | T | SR_BACK |
| WS81 | R U | T | SR_BACK |
| WS82 | K U | T | SR_BACK |
| WS83 | L R | T | SR_BACK; after B10 |
| WS84 | V I | T | SR_BACK; after I1 |
| WS85 | G U | T | SR_BACK; evgSR05yineelstartcontrol1 ran [unconfirmed flag]; after X1 |
| WS86 | V C | T | SR_BACK; after R8 |
| WS87 | L U | T | SR_BACK |
| WS88 | V U | T | SR_BACK; VAL_FATHER |
| WS89 | R U | T | SR_BACK |
| WS90 | G K | E stage set 026BC5 150 (or next tick) | SR_PAID; after A1 |
| WS91 | C G | E exterior near Lake Honrich (WATER, Riften hold) | SR_BACK; after R5 |
| WS92 | V R | T | SR_BACK; after Val-Remi intro (HLIOValBanter stage 10) |
| WS93 | K U | E exterior near Lake Honrich | SR_BACK; K_TOG+ |
| WS94 | R U | T | SR_BACK |
| WS95 | R K | T | SR_BACK; after B1 |

### PART 7 - THE FORGOTTEN CITY: AT THE EDGE  (before you jump; nobody can follow you in)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS96 | R U | E arrival in Forgotten Ruins cell | FC_EDGE |
| WS97 | K U | E in Forgotten Ruins cell | FC_EDGE; K_ANY |
| WS98 | I U | E in Forgotten Ruins cell | FC_EDGE |
| WS99 | G V | E in Forgotten Ruins cell | FC_EDGE; after A3 |
| WS100 | L R | E in Forgotten Ruins cell | FC_EDGE; after B10 |

### PART 8 - THE FORGOTTEN CITY: THE DEBRIEF  (after you come back up for good)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS101 | R U | E first tick outside ForgottenCityLocation after FC_END | FC_END |
| WS102 | L U | T | FC_END |
| WS103 | G U | T (plays before WS105-WS108) | FC_END |
| WS104 | V U | T | FC_END |
| WS105 | R C | T | FC_END; after WS103; after Redcap-Remi intro |
| WS106 | K G | E INN or CAMP | FC_END; after WS103; after A1 |
| WS107 | I V | E INN | FC_END; after WS103; after I1 |
| WS108 | L U | T | FC_END; after WS103 |
| WS109 | L C | T | FC_END; after R11 |
| WS110 | L G | T | FC_END; after L1 |
| WS111 | X G | T | FC_END; after X1 |
| WS112 | K I | T | FC_END; KaiandInigo stage >= 10 |
| WS113 | K U | T | FC_END; K_TOG+ |
| WS114 | R L | T | FC_END; after B10 |
| WS115 | X U | T | FC_END |
| WS116 | R V | T | FC_END; player has Immaculate Dwarven Armour [FormID unconfirmed]; after Val-Remi intro |
| WS117 | R I | T | FC_GOOD; after B6 |
| WS118 | I U | T | FC_END |
| WS119 | L I | T | FC_END; Lucien-Inigo intro done |
| WS120 | K U | T | FC_END |

### PART 9 - SAINTS AND SEDUCERS: THE SHIVERING ISLES
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS121 | I L | E exterior in the Isles, Mania side [unconfirmed region check] | SS_ISLES; Lucien-Inigo intro done |
| WS122 | G U | E exterior in the Isles, Dementia side [unconfirmed region check] | SS_ISLES |
| WS123 | I U | E arrival in ECSSShiveringIsles worldspace | SS_ISLES |
| WS124 | C G | T | SS_ISLES; after R5 |
| WS125 | K U | T | SS_ISLES; K_CRUSH |
| WS126 | K V | T | SS_ISLES; after A2 |
| WS127 | L U | T | SS_ISLES; 099D19 stage 10 done |
| WS128 | G K | E stage set 099D19 40 (next tick after the silence window) | 099D19 stage 40 done; after A1 |
| WS129 | V G | T | 099D19 stage 10 done; 09EF5F stage 90 not done; after A3 |
| WS130 | V X | T | 09EF5F stage 52 done, 70 not done; after X4 |
| WS131 | R L | T | 09EF5F stage 52 done; after B10 |
| WS132 | R X | T | 09EF5F stage 52 done; Remi and Xelzaz not fallen out |
| WS133 | G U | T | 09EF5F stage 64 done |
| WS134 | V R | T | 099D1A stage 10 done, 255 not done; after Val-Remi intro |
| WS135 | L U | T | 099D1A stage 10 done |
| WS136 | R I | E stage set 099D1B 255 (or next tick) | 099D1B stage 255 done; after Inigo-Remi intro (B6) |
| WS137 | C I | T | EC_SS_ElytraPetAcquisition_Mania or _Dementia stage 25 done; after R13 |
| WS138 | K U | T | 09EF5F stage 100 done (after the 80..99 silence) |
| WS139 | X R | T | 09EF5F stage 100 done; Remi and Xelzaz not fallen out |
| WS140 | G K | T | 09EF5F stage 100 done; after A1 |
| WS141 | K U | T | 09EF5F stage 100 done; K_TOG+ |
| WS142 | C L | E arrival in Borogove [location FormID unconfirmed] | SS_ISLES; after R11 |
| WS143 | I G | T | SS_ISLES; 099D19 stage 10 done; GORE_BAIL; after C2 |
| WS144 | V U | E stage set 09EF5F 100 (next tick) | SS_DONE |
| WS145 | K G | E first exterior tick in Tamriel after SS_DONE | SS_DONE; after A1 |
| WS146 | I U | T | SS_ISLES; 099D19 stage 40 done |

### PART 10 - SAINTS AND SEDUCERS: FIGHT BARKS  (short, during fights)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS147 | C G | E COMBAT in a root cave (LocType EC_SS_LocTypeRootCave 0A516C) | SS_ISLES; after R5 |
| WS148 | V K | E COMBAT in the Asylum / Isles | SS_ISLES; 09EF5F stage 90 not done; after A2 |
| WS149 | L I | E COMBAT in a root cave | SS_ISLES; Lucien-Inigo intro done |
| WS150 | R X | E COMBAT in the Isles | SS_ISLES; Remi and Xelzaz not fallen out |

### PART 11 - THE CURSED TRIBE: LARGASHBUR
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS151 | G U | E arrival in LargashburLocation | CT_START |
| WS152 | C I | E arrival at Largashbur (DA06 stage 10..20) or AFTERFIGHT:giant there | CT_START; after R13 |
| WS153 | G V | T | DA06 stage 30 done; DA06 not 200/210 yet; after A3 |
| WS154 | K U | T | DA06 stage 30 done; DA06 not 200/210 yet |
| WS155 | L C | T | DA06 stage 45 done, 60 not done; after R11 |
| WS156 | R X | T | DA06 stage 50 done, 60 not done; Remi and Xelzaz not fallen out |
| WS157 | L R | T | DA06 stage 20 done; after B10 |
| WS158 | I G | T | DA06 stage 70 done; after C2 |
| WS159 | G X | E CAMP | CT_END; after X1 |
| WS160 | K G | E COMBAT; DA06 stage 65 done, 66 not done | DA06 stage 65..66 (ghost route only) |
