# 12 BRUMA AND MOONPATH - trigger rows (BR1-BR150)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\12 BRUMA AND MOONPATH.txt`
Research: `research\content\bruma_moonpath_wyrmstooth_etc.md` sections 1 and 2. Gate codes not listed here are from TRIGGERS.md section 4.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, +Lu = Luna (player line, no gate).
Type: T = timer, E = event. `[unconfirmed]` = stage, cell or FormID not proven from the records; check at build or in game.

## New gate codes for this file

All FormIDs plugin-qualified. BSH = `BSHeartland.esm`, MP = `moonpath.esp`.

**Places**
- `CYR` = in Cyrodiil: location chain under `000F21:BSH` (Cyrodiil). First-arrival event = `0D3F2C:BSH` CYRSkyrimBorderGateTopLevelQuest stage 600 set (or `0C9B1A:BSH` stage 35).
- `COUNTY` = location chain under `000F17:BSH` (County Bruma).
- `CITY:Bruma` = GetInCurrentLoc `000F18:BSH` (Bruma city; it sits inside the BSHeartland worldspace).
- Named places in County Bruma (Applewatch, Cloud Ruler Temple, Frostcrag Spire, Greenwood Meadery, Fort Cutpurse, Fort Pale Pass, Ayleid ruins Sedor/Anga/Moranda/Piukanda/Rielle/Garlas Ture, the Cathedral of St. Martin, the Fighters Guild hall, the shack village, Synod conclave): use their LCTN or cell. `[unconfirmed: LCTN/cell IDs not in the research; look them up in BSHeartland.esm at build]`.
- `ELS` = GetInCurrentLoc `017872:MP` ("Elsweyr"; all 15 Moonpath cells point to it).
- `RIVERHOLD_S` = GetInCell `06AE2D:MP` (South of Riverhold).
- `OASIS` = GetInCell `0424C0:MP` (Botanist's Oasis). `DESERT` = GetInCell `02CEE1:MP` (Desert Caravan Supply Post) or `01ED3C:MP` stage 110 done and 130 not done.
- `TENMAR` = `06A8CA:MP` stage 60 done and in ELS.

**Border routes** (`0D3F2C:BSH` Welcome to Cyrodiil)
- `PP_TALK` = stage 30 done (convinced the Legate). `PP_KILL` = stage 31 done, or `0C9B1A:BSH` stage 70 done. `PP_TRAIL` = stage 20 or 22 done (Mirich Ran / Serpent's Trail).

**Personal**
- `K_AKAVIRI` = Kaidan's KINV "All of this Past" (Akaviri relics) completed. `[unconfirmed: KINV FormID and completion stage; kaidan bible says he only learns his mother's race in this quest]`.
- `GORE_TIES` = Gore has told the player his past (the Thalmor raid near Bruma). Blood Ties `HD1GoreQuest2` past-telling stage. `[unconfirmed stage; safe fallback = HD1GoreQuest2 completed]`. Never mention Jo-Lee/Mattias under this gate; that needs `GORE_FATHER`.

**Bruma quests** (all BSH)
- `AA` Absent Antiquity `086207`: 10 started, 60 thief named Atienne, 120 done.
- `DS` A Delicate Situation `086208`: 10 started; 100 complete. Three ending stages, one per log: `DS_QUIET` (lie low), `DS_STOP` (stop entirely), `DS_OPEN` (continue openly). Record says use GetStageDone on the individual ending stages. `[unconfirmed: ending stage numbers]`.
- `AC` Against the Cutters `08650F`: 20 drinks at the Jerall View, 100 Thorina dead.
- `SR` Service Rewarded `07F0FA`: 20 audience/Hvitbrand/house rights, **50 Adius arrested**, **100 warm farewell**.
- `ALV` Alammu's Veil `003A58`: 20 skooma ruse revealed.
- `UMH` Upon My Honor `0C7E4C`: 30 body found; 100 truth told; 110 hid it.
- `SIC` A Stormcloak in Chains `0CE0F1`: 5/6 started; 200 interrogated; 210-250 assault (silence); 250 Penitus Oculatus arrive. Post handler `0CE135`.
- `UL` Ugly Love `08AE84`: 10 started; 50 castle confrontation. Dumrag follower = post-quest `0C9CBD` stage 40.
- `UU` Undeath at Underpall `08BF0C`: 60 sister killed; 65/80 spared and reunited.
- `WM` Whispers of the Mountain `083A17`: 60 to Frostcrag; 220-250 portal test; 250 flung.
- `COUR` The Courier `0C9BE1`: 250 documents found; 360 gave to Olaf; 399/400 refused.
- `WH` The Way Home `06F9B8`: completed `[unconfirmed completion stage]`.
- `FF` Frostfire Unleashed `06C0DE`: 202 complete.
- `AWP` All the Wrong Places `047FAA`: 60 they get along; 80 wedding attended.
- `SONG` The Screeching Songman `067841`: 10 started.
- `DEEP` The Deepiron Problem `0E5912`: 10 started; 70 gold vein.
- `DOG` Missing Dog `CYRBrumaFF12` completed `[unconfirmed FormID]`.
- `FGADS` Fighter's Guild Advertising `CYRBrumaFF10` started `[unconfirmed FormID]`.
- `WATER` Water Run Dry `CYRGreenwoodMeaderyFF01` (Greenwood Meadery) `[unconfirmed FormID]`.
- `SANG` Sanguine Revelers `CYRWE14` (revelers turn into Dremora) `[unconfirmed FormID/stage]`.
- `MASS` = scene quest `06507B:BSH` CYRDialogueBrumaCathedralMassScene has run at least once `[unconfirmed: needs a played flag; quest has no "done" stage]`.

**Moonpath quests** (all MP)
- `MPC` By the Light of the Moon `06A8CA`: 10 joined caravan; 15 northern edge of Elsweyr; 20-30 canyon blockade; 40-50 broken bridge/ford; 55 Pahmar invitation; 60 Tenmar Forest.
- `STE` The Sweet Taste of Elsweyr `01EE82`: 0 arrived; 10 Ameir and moon sugar; 20 done.
- `INC` Incursion `01ED3C`: 40 Tenmar Den cleared; 60-70 Pillar Falls; 100 airship; 110 desert near Dune; 130 boarding; 150 Lenial dead.
- `RTP` Rebuilding the Past `03C6E1`: 20 Dwemer supply post; 30 Jo'ran freed; 60 base finished.
- `DG` The Dinner Guest `0589C5`: 30 Malsato's blackmail; 50 poisoned meat; 70 infected beast; 95 forest saved; **100 FAIL plague released**.
- `DSTY` Desert Style `0440C0`: 10 Shil'ara.
- `SKULL` = player has talked to Skullcat (`085C5D` has no stages; use a dialogue-said check on its topic) `[unconfirmed]`.

## Silence zones (add to WorldQuiet while these run)

- Border gate scene and move: `0C9B1A` stages 25..34. No CYR talk before `0C9B1A` 35 or `0D3F2C` 600.
- Cathedral mass: `06507B` running. Wedding: `047FAA` 70..79.
- Castle audience / Adius arrest: `07F0FA` 10..49 and the 50/100 scene itself (fire SR talks on the next tick after the stage is set).
- Ugly Love castle killing: `08AE84` 50..99.
- Whispers teleport: `083A17` 240..249 and handler `0CC08B` 2..10.
- Frostfire banishing: `06C0DE` 150..199.
- Fort Pale Pass assault: `0CE0F1` 210..249.
- Moonpath carriage legs: `06A8CA` 10..14, 35..39, 55..59.
- Airship flights and boarding: `01ED3C` 100..104 and 130..134; cells `0403B5` Thalmor Airship and `042474` Waning Moon Captain's Cabin.
- Sload: `0589C5` stage 30 scene, and 80..90.
- Bruma ambient scenes: the normal IsInScene check on every speaker.

## Table

### Part 1 - Over Pale Pass
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR1 | K +Lu | E first arrival in Cyrodiil (`0D3F2C` 600 set) | — (once) |
| BR2 | V L +Lu | E arrival in Cyrodiil, or T in CYR | PP_TALK; after C1 |
| BR3 | X G | E arrival in Cyrodiil, or T in CYR | PP_KILL; after X1 |
| BR4 | R I | E arrival in Cyrodiil (exiting Serpent's Trail) | PP_TRAIL; after B6 |
| BR5 | +Lu K L | E in Pale Pass / Fort Pale Pass area [LCTN unconfirmed], else T in COUNTY | K_AKAVIRI; Kaidan-Lucien intro done |
| BR6 | X +Lu | T | COUNTY, first visit; after C3 not required |
| BR7 | C G | T | CYR; after R5 |
| BR8 | C L | E at Fort Pale Pass [LCTN unconfirmed] | SIC started (5/6), not 200, no post-handler 100/150/200; after R11 |
| BR9 | L G +Lu | T | SIC 250 done; after L1 |
| BR10 | G K | T | CYR, at least 1 game day after first arrival; after A1 |
| BR11 | R V +Lu | T | CYR; after B14 not required (Remi-Val intro in Remi's mod done) |
| BR12 | I X | T | CYR, not CITY; after X6 |

### Part 2 - Bruma
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR13 | L K +Lu | E CITY:Bruma first arrival (`CYRBrumaFF00 0D6996` stage 1 set) | Kaidan-Lucien intro done |
| BR14 | G V | T | CITY:Bruma; after A3 |
| BR15 | X +Lu | E INN in COUNTY | — |
| BR16 | R G | T | CITY:Bruma; GORE_FATHER |
| BR17 | X G | E near Bruma shack village [cell unconfirmed], else T CITY:Bruma | after X1 |
| BR18 | V I | E INN in CITY:Bruma | after I1 |
| BR19 | L C | E INN in CITY:Bruma | after R11 |
| BR20 | L K +Lu | E inside the Cathedral of St. Martin [cell unconfirmed] | not MASS running |
| BR21 | I +Lu | E inside the Cathedral of St. Martin | DB; after BR20 not required |
| BR22 | X R | T | MASS (has played); Remi/Xel not fallen out |
| BR23 | V R +Lu | T | AA >= 10, AA 120 not done |
| BR24 | K +Lu | T | AA >= 10; K_AKAVIRI |
| BR25 | R I | T | AA 60 done; after B6 |
| BR26 | L X +Lu | E Synod conclave in Bruma [cell unconfirmed], else T CITY:Bruma | Xelzaz-Lucien intro done (their own mod) |
| BR27 | L R | T | COUNTY; WM >= 30 or any College of Whispers dialogue heard [unconfirmed proxy: WM started]; after B10 |
| BR28 | G V +Lu | T | CITY:Bruma; after A3 |
| BR29 | G K | E Fighters Guild hall, Bruma [cell unconfirmed] | after A1 |
| BR30 | K C | T | FGADS started, not completed; after R1 |
| BR31 | K R | T | CITY:Bruma; DS or SR not done (Armion still around) [unconfirmed proxy]; after B1 |
| BR32 | L +Lu | T | CITY:Bruma; HELGEN |
| BR33 | V R | T | CYR |
| BR34 | +Lu L V | T | CYR; after C1 |

### Part 3 - Home, and what it cost
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR35 | G K | T | COUNTY, not CITY; GORE_TIES; after A1 |
| BR36 | G +Lu | E arrival Applewatch [LCTN unconfirmed] | GORE_TIES |
| BR37 | L G | T | CYR; GORE_TIES; after L1 |
| BR38 | G I | T | COUNTY; GORE_FATHER; after C2 |
| BR39 | G K | T | CYR; G_FLIRT; after A1 |
| BR40 | V K | T | CYR; V_FLIRT; after A2 |
| BR41 | I +Lu | T | CYR, not CITY |
| BR42 | K +Lu | E SNOW in COUNTY | K_CRUSH |

### Part 4 - Captain Adius and the Devout
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR43 | G K | T | AA >= 10; after A1 |
| BR44 | G +Lu | T | DS >= 10, no DS ending stage done; GORE_TIES |
| BR45 | L K | T | DS >= 10, no DS ending stage done; Kaidan-Lucien intro done |
| BR46 | X V | T | DS >= 10, no DS ending stage done; after X4 |
| BR47 | G R | T | DS_QUIET |
| BR48 | G K | T | DS_STOP |
| BR49 | G V | T | DS_OPEN |
| BR50 | V I +Lu | E INN Jerall View, or T | AC 20 done; after I1 |
| BR51 | K R | T | AC 100 done; after B1 |
| BR52 | L K | T | SR 20 done |
| BR53 | K +Lu | T | SR 20 done; K_TOG+ |
| BR54 | V X | T | SR 50 done; after X4 |
| BR55 | G K +Lu | T | SR 50 done (implies DS_OPEN); after A1 |
| BR56 | C K | T | SR 50 done; after R1 |
| BR57 | G L | T | SR 100 done; after L1 |

### Part 5 - Around County Bruma
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR58 | I K | T | ALV 20 done; ALV not completed; KaiandInigo stage >= 10 |
| BR59 | L V +Lu | T | UMH 30 done, 100 and 110 not done; after C1 |
| BR60 | G R | T | UL 10..49 |
| BR61 | V +Lu | T | UU 65 or 80 done; VAL_FATHIS |
| BR62 | V G | T | UU 60 done; after A3 |
| BR63 | I L | T | WH completed |
| BR64 | L R +Lu | E arrival Cloud Ruler Temple [LCTN unconfirmed] | after B10 |
| BR65 | X +Lu | E arrival Frostcrag Spire [LCTN unconfirmed] | — |
| BR66 | C R | T | WM 250 done (and handler `0CC08B` past 10) |
| BR67 | R X | T | WM 60..239; Remi/Xel not fallen out |
| BR68 | R +Lu | T | FF 202 done |
| BR69 | L R +Lu | E arrival at any Ayleid ruin in COUNTY (exterior) [LCTN unconfirmed] | after B10 |
| BR70 | V K +Lu | T | AWP 80 done; K_CRUSH |
| BR71 | R L | T | AWP 60..79; after B10 |
| BR72 | I G | T | SONG 10.., not completed; after C2 |
| BR73 | C K | T | DOG completed; after R1 |
| BR74 | C V | T | DEEP >= 10, < 70; after R8 |
| BR75 | R K | T | DEEP 70 done; after B1 |
| BR76 | G V | E arrival Greenwood Meadery [LCTN unconfirmed] | WATER not completed, or never started; after A3 |
| BR77 | C X | T or E AFTERFIGHT:dremora in COUNTY | SANG done; RC_REDGOD; R18 done |
| BR78 | K G | T | COUR 250 done, 360/399/400 not done; after A1 |
| BR79 | C L | E inside an Ayleid ruin in COUNTY (interior) [cells unconfirmed] | after R11 |
| BR80 | V R | E arrival Fort Cutpurse [LCTN unconfirmed] | AC 100 not done |
| BR81 | X L +Lu | T | CYR; Xelzaz-Lucien intro done |
| BR82 | G V K | T | COUNTY, not CITY; after A1, A2, A3 |
| BR83 | G K | T | Dumrag following (`0C9CBD` 40 done) [unconfirmed: Dumrag ref and follow check]; after A1 |
| BR84 | L I +Lu | E exterior just outside Bruma walls [no marker; proxy = COUNTY exterior within ~4000 units of the Bruma gate] | after BR13 |

### Part 6 - Bruma fight barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR85 | G K | E AFTERFIGHT:bandit in COUNTY | — |
| BR86 | K L | E AFTERFIGHT:Thalmor in CYR | — |
| BR87 | I G | E AFTERFIGHT:ogre (race check) [unconfirmed race ID] | — |
| BR88 | C R | E AFTERFIGHT:goblin (CC/BSH goblin race) [unconfirmed race ID] | — |
| BR89 | V +Lu | E AFTERFIGHT:dremora in COUNTY | — |
| BR90 | R X | E AFTERFIGHT:necromancer at Underpall (UU >= 10, in Underpall) [LCTN unconfirmed] | Remi/Xel not fallen out |

### Part 7 - The caravan south
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR91 | I K +Lu | E MPC 15 set (fire after the carriage fade) | KaiandInigo stage >= 10 |
| BR92 | I G | T | ELS; MPC 15..59; after C2 |
| BR93 | V R | T | ELS; MPC 15..59 |
| BR94 | L C | T | ELS; MPC 15..30; after R11 |
| BR95 | L +Lu | T | ELS; LUC_ADMIT |
| BR96 | G V X | T | MPC 20 done, 30 not done |
| BR97 | K +Lu | T | MPC 30 done |
| BR98 | R L | T | MPC 40..54; after B10 |
| BR99 | I C | E AFTERFIGHT:spider in ELS, or T | MPC 40..54; after R13 |
| BR100 | X G | E AFTERFIGHT in ELS, or T | MPC 40..54; after X1 |
| BR101 | I K | E MPC 55 set, or T | KaiandInigo stage >= 10 |
| BR102 | C +Lu | E MPC 60 set (TENMAR) | — |

### Part 8 - Inigo's Elsweyr
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR103 | I K +Lu | E RIVERHOLD_S first entry | KaiandInigo stage >= 10. Burial near Riverhold is from the research hook, not a quoted Inigo line [unconfirmed] |
| BR104 | I R | T | ELS; after BR103, B6 |
| BR105 | I L | T | ELS; after BR103 |
| BR106 | I X | E NIGHT in ELS | after X6 |
| BR107 | I +Lu | T | ELS; after BR103 |
| BR108 | K I | T | ELS; KaiandInigo stage >= 10 |
| BR109 | K I | T | ELS; STE 10 done; KaiandInigo stage >= 10 |
| BR110 | I G +Lu | E DESERT (INC 110 set) | after C2 |
| BR111 | I V | T | ELS; INC 105 done (after first flight); after I1 |
| BR112 | K I +Lu | E NIGHT in ELS | K_CRUSH; KaiandInigo stage >= 10 |

### Part 9 - Tenmar Forest
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR113 | L +Lu | E MPC 60 set (TENMAR), or T | — |
| BR114 | X C | T | TENMAR; R18 done |
| BR115 | R C | T | ELS; after BR114 |
| BR116 | R I | T | STE 10 done; after B6 |
| BR117 | L I | T | STE 10 done; Lucien-Inigo intro done (JRLucienInigoRank >= 2) |
| BR118 | G +Lu | T | STE >= 0 (met Yura at the hideout) |
| BR119 | X G | T | ELS; after X1 |
| BR120 | V K | T | INC < 40 and Mervar still hostile-gated [unconfirmed: Mervar's distrust state is dialogue only; proxy = INC 0..39]; after A2 |
| BR121 | X R +Lu | E CAMP or INN-type cell in ELS (Tenmar hideout) | Remi/Xel not fallen out |
| BR122 | V C | T | ELS; SKULL; after R8 |
| BR123 | G K | T | ELS; after A1 |
| BR124 | K +Lu | T | ELS; K_TOG+ |
| BR125 | K +Lu | T | ELS; K_MAR |
| BR126 | L V | T | ELS (daytime, exterior-sky cell); after C1 |
| BR127 | +Lu L C | E CLEARNIGHT in ELS | after R11 |

### Part 10 - The rebellion
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR128 | G K | T | INC 40 done; after A1 |
| BR129 | R L | T | INC 60..99 (Pillar Falls, before the flight) |
| BR130 | V +Lu | T | INC 105 done, not in the airship cells during 130..134 |
| BR131 | C V | T | INC 105 done; after R8 |
| BR132 | +Lu X | E DESERT (INC 110 set) | — |
| BR133 | K G | T | INC 110 done, 130 not done (Lenial's log read) [unconfirmed exact log stage]; after A1 |
| BR134 | K +Lu | E INC 150 set, next tick | — |
| BR135 | G L | T | INC 150 done; GORE_TIES; after L1 |
| BR136 | V R | T | INC 150 done |
| BR137 | R L | T | RTP 20 done; after B10 |
| BR138 | V X | T | RTP 10..29 (before Jo'ran freed); after X4 |
| BR139 | X L | T | DG 30 done (after the scene), DG 95/100 not done |
| BR140 | R I | T | DG 30 done, DG 95/100 not done; after B6 |
| BR141 | X G | T | DG 50..69; after X1 |
| BR142 | I C | T | DG 70..94; after R13 |
| BR143 | L +Lu | T | DG 95 done |
| BR144 | L X | T | DG 100 done (fail branch) |
| BR145 | X +Lu | E OASIS first entry | DSTY 10 done |
| BR146 | R K | T | RTP 60 done; after B1 |

### Part 11 - Elsweyr fight barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| BR147 | I L | E AFTERFIGHT:spider in ELS | Lucien-Inigo intro done |
| BR148 | K G | E AFTERFIGHT:Thalmor in ELS | — |
| BR149 | X V | E AFTERFIGHT:Argonian pirate (Topal Sea Island cells `03A854` / `03E4CB`) | — |
| BR150 | C R | E AFTERFIGHT:hyena in ELS [unconfirmed race/creature ID] | — |

## Open items for build
- All `[unconfirmed]` items above, especially DS ending stages, KINV, GORE_TIES stage, and County Bruma place LCTNs.
- Followers crossing: border failsafe `0D6E80:BSH` moves followers to Cyrodiil; Moonpath carriages act as doors. Check every follower arrives (Val uses his own framework, Inigo uses IsPlayerTeammate).
- BR55 is meant for the arrest branch only. SR 50 only happens after DS_OPEN, so it is safe; add DS_OPEN as a belt-and-braces gate.
- BR53/BR124/BR125 are Kaidan-romance gated; BR39/BR40 are rival flirts and must not fire once the player is together with someone else (add `not K_TOG+` for BR39/BR40 if the user wants strict rivalry steps).
