# 11c LOTD 3 - trigger rows (prefix LT, LT241-LT390, 150 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\11c LOTD 3.txt`
Part 1 and part 2 (all local codes, places and silences reused unchanged): `triggers\11 LEGACY OF THE DRAGONBORN.md`, `triggers\11b LOTD 2.md`.
Research: `research\content\lotd.md` (quest table section 2, silences section 3, places section 4). Serana/Ashe Free() and gate codes: `triggers\48 SERANA.md`, `triggers\49 ASHE.md`.
Gate codes from `TRIGGERS.md` section 4. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe; "+Luna" = player line (Eleonora voice), no Free check.

## Global for every row
- `WorldQuiet()` + `Free(x)` (TRIGGERS.md sections 2-3) + **`LT_QUIET`** exactly as in file 11 (tours, gala 10..100, nightmare 65..80 hard silent, cave-in 61..75 hard silent, Rkund guided stretch, Pelagius' mind, Sancre Tor / Herald, Wulfharth tomb, Planetarium reveal 46..50, Waystone jump, Indarys assassin, Heist confrontation 33..45, Vigilants in the museum, Snow Elf ghost 310..400, Visage prelude 1..15, any LOTD staff/patron scene, player in dialogue with Auryen/Avram/an explorer).
- Haunt 15..104: none of these rows may play (file 11 lets only LT110 play there). LT370 is gated before 15 on purpose.
- Rows with **S** also need `SERANA` + Serana Free (48 SERANA.md). Rows with **A** also need `ASHE_HIRED` + Ashe Free and Ashe silence (49 ASHE.md).

## New local codes (this file)
- `DISP_N` = `GetGlobalValue DBM_DisplayCount` (**124FA6:LegacyoftheDragonborn.esm**, runtime 14124FA6). The global is confirmed to exist in the plugin (read 2026-10-21). **[UNC: that it holds the number of filled displays, museum-wide, is assumed from its name; check in game with `help DBM_DisplayCount` after placing a few items.]** Bands used:
  - `D_EMPTY` = DISP_N < 10 · `D_FEW` = 1..60 · `D_MID` = DISP_N >= 150 ("a good number") · exact ranges where a row names them (1..5, 100..130, 300..340, 500..550, >= 700, >= 1000). Fallback if the global is wrong: D_EMPTY = LT_EARLY; D_MID = LT_HIRED and Exc01 150 done; >= 700/1000 = NEAR_FULL (file 11b).
- `SHIP` = `DBM_ShipmentCount` (0F0B11) >= 1 or `DBMMuseumShipmentsFirst` (1772A8) == 1 **[UNC: meaning assumed from names]**.
- `LEDGER` = played:LT242 (Lucien's Great Catalogue exists). `LEDGER2` = played:LT306 (second volume). `BOARD` = played:LT263 (the Finds Board is up).
- `GUILD_BUILT` = DBM_ExplorerGuildHouse (3431C3) 10 done.
- `RR03` = Dragonborn DLC quest DLC2RR03 completed **[UNC: EditorID inferred from the book DLC2RR03GratiansJournal 020A2F:Dragonborn.esm, which LOTD overrides; that the journal has an LOTD display is inferred from that override]**.
- `TOLFDIR_VISIT` **[UNC: nothing in LegacyoftheDragonborn.esm was found for a Tolfdir museum visit. Keep LT363 disabled unless a visit flag or scene is found.]**
- `AMJ:`, `SANAMIA:`, `HOW`, `NEAR:`, `NIGHT_M`, `LX`, `LI`, `RX`, `KI` exactly as files 11 / 11b.
- Remi-Redcap rows (LT253, LT357): no Remi-Redcap meet code exists yet in the shared tables. **[UNC]** Use the BPUFXelzazRemielRedcapInteractions intro stage if one fits, else no chain.

## Not written, and why
- **Barnabas and Elsa**: no NPC with either name exists in LegacyoftheDragonborn.esm (searched 2026-10-21). They may come from another mod; not written so nothing is invented.

## Table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| LT241 | L R +Luna | E MUSEUM (first entry) | LT_EARLY; D_EMPTY; after B10 |
| LT242 | L X +Luna | T in MUSEUM | D_EMPTY; LX |
| LT243 | L R +Luna | T | DBM_MuseumIntro (17211B) 20 done and not completed; after B10 |
| LT244 | L X | T | DBM_MuseumIntro 20 done and not completed; LX |
| LT245 | R L | T | DBM_LALStart (3F14FC) 30 done and 35 not done; after B10 |
| LT246 | R L X | E MUSEUM | LT_EARLY; LX; RX; after B10 |
| LT247 | K L | E MUSEUM, Auryen (12537E) within 1500 [UNC: ref distance] | Lucien-Kaidan intro done (as K5's row) [UNC: JRLucienFollowerKaidanScene1 played flag] |
| LT248 | V +Luna | T in MUSEUM | LT_EARLY or D_FEW; Val recruited (AX_ValRecruited == 1) |
| LT249 | I L | E MUSEUM | LT_EARLY; LI |
| LT250 | G C | E M_ARM | LT_EARLY; after R5 |
| LT251 | L R +Luna | E MUSEUM | DISP_N 1..5; LEDGER; after B10 |
| LT252 | L R X | T in MUSEUM | DISP_N 5..60; LEDGER; LX; RX |
| LT253 | R C | E MUSEUM | SHIP; Remi-Redcap meet [UNC: no chain code; see notes] |
| LT254 | X +Luna | T in MUSEUM | LT_EARLY |
| LT255 | L R | T | LT_HIRED; after B10 |
| LT256 | L X +Luna | E Solitude exterior or GUILD | DBM_ExplorerGuildHouse (3431C3) 5 done and 10 not done; LEDGER; LX |
| LT257 | L R +Luna | T | DBM_ExplorerGuildmembers (34D50B) 5 done and not completed; after B10 |
| LT258 | L R | E GUILD | EXPL; Exc03A (2702EE) 61 not done; after B10 |
| LT259 | L X | E GUILD | EXPL; LX; played:LT73 |
| LT260 | X L +Luna | T | DBM_RadiantRuinedBooks (5A94C3) running and 10 not done [UNC: stage 0 = started]; LX |
| LT261 | L V | E GUILD | EXPL; after C1 |
| LT262 | L X +Luna | E GUILD | EXPL; LX |
| LT263 | R L X | E GUILD | EXPL; GUILD_BUILT; LEDGER; LX; RX (playing it sets BOARD) |
| LT264 | R L +Luna | E GUILD | BOARD; after B10 |
| LT265 | C X | E GUILD | BOARD; Exc01 (4D1811) 150 done; after R18 |
| LT266 | L S | E FS_NORTH (34D523) | DBM_ExplorerFieldStation01 (2AD9CD) 15 done; played:LT176 |
| LT267 | X L | E FS_WEST (2BB744) | DBM_ExplorerFieldStation02 (2D1170) 15 done; LX |
| LT268 | V +Luna | T | any field station paid (2AD9CD 15, 2D1170 7, or 2D1178 15 done); Val recruited |
| LT269 | K L | E GUILD | DBM_ExplorerGuildHouse completed; Lucien-Kaidan intro done (as K5's row) [UNC: JRLucienFollowerKaidanScene1 played flag] |
| LT270 | R X L | E GUILD | EXPL; BOARD; LX; RX |
| LT271 | L X +Luna | E M_LIB | DISP_N 10..200; LX |
| LT272 | R L | E M_LIB | LT_HIRED; after B10 |
| LT273 | X L +Luna | E M_LIB | D_MID; LX |
| LT274 | L X | T in MUSEUM | BLACKBOOK; LEDGER; LX |
| LT275 | L X +Luna | E M_NAT (tidepool) | LT_HIRED; LX |
| LT276 | L R +Luna | E M_NAT | D_MID; after B10 |
| LT277 | L X R | E M_NAT (garden) | LT_HIRED; LX; RX |
| LT278 | R L +Luna | E M_NAT (fossil hall) | DISP_N 30..300; after B10 |
| LT279 | L X | E M_NAT | LT_HIRED; LEDGER; LX |
| LT280 | L G | E M_NAT (aquarium) | LT_HIRED; after L1 |
| LT281 | R L | E M_ARM | D_MID; LEDGER; after B10 |
| LT282 | L K | E M_ARM | D_MID; Lucien-Kaidan intro done (as K5's row) [UNC: JRLucienFollowerKaidanScene1 played flag] |
| LT283 | L X +Luna | E M_ARM | LT_HIRED; LX |
| LT284 | L X +Luna | E M_HOH | ARCH; LX |
| LT285 | G L | E M_HOH | CWFinale completed, either side [UNC: Jagged Crown display flag not looked up]; after L1 |
| LT286 | R L | E M_HOH | DLC1 Lost to the Ages completed [UNC: quest EditorID]; after B10 |
| LT287 | L X | E M_DAED | DA01 (Azura) completed [UNC: proxy for the Star on display]; LX |
| LT288 | L R +Luna | E M_DAED | DA09 (The Mind of Madness) completed [UNC: proxy for the Wabbajack on display]; after B10 |
| LT289 | X L | E M_DAED | DA04 completed (Oghma Infinium) [UNC: proxy for display]; LX |
| LT290 | R L | E M_HOLE | D_MID; LEDGER; after B10 |
| LT291 | L X | E M_HOLE | D_MID; LX |
| LT292 | R L X | E M_ODD | D_MID; LEDGER; LX; RX |
| LT293 | L X +Luna | E M_DBH | DB; D_MID; LX |
| LT294 | L R | E M_DBH | DB; SHOUT1; after B10 |
| LT295 | L R | E M_HOS | DBM_HOSDiscoveryQST (0A9247) 15 done; LEDGER; after B10 |
| LT296 | L R +Luna | E M_PLAN | DBM_PlanetariumQuest (5867FC) completed (50 or 100); after B10 |
| LT297 | K +Luna | E M_PLAN | DBM_PlanetariumQuest completed; K_TOG+ |
| LT298 | X L | E HOW | HOW plugin loaded; LX |
| LT299 | R L | E M_SAFE (workshop) | DBM_ImbuningMachine (16658A) 10 done and 15 not done; BOARD; after B10 |
| LT300 | X L +Luna | E M_SAFE | LT_HIRED; LX |
| LT301 | X R L | E M_SAFE (garden) | LT_HIRED; LX; RX |
| LT302 | R L +Luna | E M_SAFE | LT_HIRED; after B10 |
| LT303 | L X +Luna | T in MUSEUM | DBM_DHQuest (9211FD) 40 done; LEDGER; LX |
| LT304 | X R L | E DEEPHOLME | DBM_DHQuest 30 done; LX; RX |
| LT305 | L R X | T in MUSEUM | DISP_N 100..130; LEDGER; LX; RX |
| LT306 | L X +Luna | T in MUSEUM | DISP_N 300..340; LEDGER; LX (playing it sets LEDGER2) |
| LT307 | G L R | T in MUSEUM | DISP_N 500..550; LEDGER; after L1; after B10 |
| LT308 | L X +Luna | T in MUSEUM | DISP_N >= 1000; LEDGER; LX |
| LT309 | R L +Luna | T in MUSEUM | D_MID; after B10 |
| LT310 | X L +Luna | T in MUSEUM | D_MID; LX |
| LT311 | R A | T in MUSEUM | D_MID; ASHE_HIRED |
| LT312 | L X +Luna | T in MUSEUM | D_MID; LEDGER; LX |
| LT313 | R L X | E M_HOLE | D_MID; LX; RX |
| LT314 | R L +Luna | T in MUSEUM | D_MID; after B10 |
| LT315 | L X | T in MUSEUM | D_MID; LX |
| LT316 | L R | E GUILD | BOARD; after B10 |
| LT317 | X L +Luna | E GUILD | BOARD; LX |
| LT318 | C L | E GUILD | BOARD; after R11 |
| LT319 | R K | E GUILD | BOARD; after B1 |
| LT320 | L X G | E GUILD, hour 18..23 | EXPL; LX; after L1 |
| LT321 | L I R | E GUILD, hour 18..23 | EXPL; played:LT320; LI; after B6, B10 |
| LT322 | L R X | T in MUSEUM | D_MID; LEDGER; LX; RX |
| LT323 | X +Luna | T in MUSEUM | LEDGER2 |
| LT324 | R L | T in MUSEUM | D_MID; LEDGER; after B10 |
| LT325 | L X | T in MUSEUM | D_MID; LEDGER; LX |
| LT326 | R L +Luna | E M_HOLE, hour 5..7 | D_MID; after B10 |
| LT327 | L V | T | DBM_ExplorerRelicFindQST (7BFED0) 5 done and Merrian's Spyglass in player inventory [UNC: item FormID]; after C1 |
| LT328 | L R X | T in MUSEUM | D_MID; LEDGER; LX; RX |
| LT329 | L X | T in MUSEUM | D_MID; LEDGER; LX |
| LT330 | R L +Luna | T in MUSEUM | LEDGER2; after B10 |
| LT331 | L R | E Windcaller Pass (1942FA/1943CD) | Exc01 20 done and 47 not done; after B10 |
| LT332 | L X +Luna | E Windcaller Pass | Exc01 47 done and 131 not done; LX |
| LT333 | R L +Luna | E Windcaller Pass | Exc01 62 done and 131 not done; BOARD; after B10 |
| LT334 | L X R | E Windcaller Pass | Exc01 131 done and 141 not done; LX; RX |
| LT335 | R L | E Rkund exterior (0D5667) | Exc02 (58B96A) 11 done and 20 not done; after B10 |
| LT336 | L X +Luna | E Rkund exterior | Exc02 55 done and 80 not done; LX |
| LT337 | R L | T | Exc02 140 done; LEDGER; after B10 |
| LT338 | L X | T | Exc02 140 done; LX |
| LT339 | L R | T | DBM_PlanetariumQuest 10 done and 20 not done; after B10 |
| LT340 | R L X | E MUSEUM | DBM_PlanetariumQuest 30 done and 46 not done; LX; RX |
| LT341 | R L | T | MuchAdo (5C7E75) 5 done and 101 not done; after B10 |
| LT342 | L X +Luna | T | MuchAdo 101 done and 310 not done; LX |
| LT343 | L R | T | MuchAdo 200 done and 310 not done [UNC: stage that sends you to Mzulft for the Synod book]; after B10 |
| LT344 | L X | T | MuchAdo 410 done; LX |
| LT345 | R L | E Greenwall dig (23CBD8) | Exc03A 5 done and 50 not done; after B10 |
| LT346 | L X | E Greenwall dig | Exc03A 55 done and 61 not done; LX |
| LT347 | R L X | E GUILD | Exc03A 80 done; BOARD; LX; RX |
| LT348 | R L | T | Exc03A 80 done; after B10 |
| LT349 | L R | T | DBM_PhynasterRingQST (2A36E4) 10 done and DBM_SyrabaneRingQST (2A87EE) 10 done; BOARD; after B10 |
| LT350 | L R +Luna | E M_HOH | Exc03A 350 done; played:LT98; after B10 |
| LT351 | L I | E Valthume | SANAMIA:Valthume; LI |
| LT352 | X L +Luna | E ruin by Lake Ilinalta | SANAMIA:Lake Ilinalta; LX |
| LT353 | L X +Luna | T exterior | DBM_SurveyorHandler (1C6621) 5 done and 6 not done; LX |
| LT354 | K R | T exterior | DBM_SextantHandler (18DDE8) 5 done and 6 not done; after B1 |
| LT355 | L R X | E FS_NORTH / FS_WEST / FS_EAST, CLEARNIGHT | that station built (15 done); LX; RX |
| LT356 | G X | E RAIN, exterior | DBM_SurveyorHandler or DBM_SextantHandler 5 done and 6 not done; after X1 |
| LT357 | C R | T exterior | DBM_SurveyorHandler or DBM_SextantHandler 5 done and 6 not done; BOARD; Remi-Redcap meet [UNC: no chain code; see notes] |
| LT358 | L R | T in MUSEUM | LEDGER; D_MID; after B10 |
| LT359 | L X | T | AMJ:Dragonmail Cuirass [UNC: which DBM_AMJournalQST number]; LX |
| LT360 | L X +Luna | T | any DBM_AMJournalQST01..10 10 done and not completed; LX |
| LT361 | L X | E MUSEUM | RR03 [UNC]; LX |
| LT362 | R L | E MUSEUM | RR03 [UNC]; played:LT361; after B10 |
| LT363 | L X +Luna | E MUSEUM | MG_JOIN; TOLFDIR_VISIT [UNC: keep disabled until found]; LX |
| LT364 | R I | E M_HOH (reception) | LT_HIRED; after B6 |
| LT365 | L X +Luna | E M_SAFE (kitchen) | LT_HIRED; LX |
| LT366 | L R | E NEAR:Henry | LT_HIRED; after B10 |
| LT367 | L X | E NEAR:Asterion/Asterell | LT_HIRED; LX |
| LT368 | L R | T in MUSEUM | Heist (33D940) 10 done and 33 not done; LEDGER; after B10 |
| LT369 | R V | T in MUSEUM | Heist completed (60); HLIOValRemiFriendshipTracker >= 1 |
| LT370 | R L X | T in MUSEUM | Haunt (7AC75C) 6 or 10 done and 15 not done; LX; RX |
| LT371 | L X +Luna | E NIGHT_M | Haunt completed (110); LEDGER; LX |
| LT372 | L G | T, not in MUSEUM | Vig1 (0F0D34) 2 done and not completed; LEDGER; after L1 |
| LT373 | R L | T | EoM (4E0D3F) completed (100); LEDGER; after B10 |
| LT374 | L X +Luna | E AIRSHIP | DBM_MuseumIndarysQuest (371C28) completed; LX |
| LT375 | L R | T | Gala (0F0DC8) 5 done and 10 not done; after B10 |
| LT376 | X K | T | Gala 100 done; after C3 |
| LT377 | L K | T | SL (121573) 50 done; Lucien-Kaidan intro done (as K5's row) [UNC: JRLucienFollowerKaidanScene1 played flag] |
| LT378 | R S | T | SL 30 done and 90 not done; played:LT176 |
| LT379 | L X | T | SL completed (300); LX |
| LT380 | R L X | T | DBM_DwarvenTech (3F33E3) 7 done; LX; RX |
| LT381 | V L | T in MUSEUM | LEDGER; after C1 |
| LT382 | I R | E GUILD | BOARD; after B6 |
| LT383 | S L R | E GUILD | BOARD; played:LT176; after B10 |
| LT384 | L A R | T in MUSEUM | ASHE_REVEAL; D_MID; after B10 |
| LT385 | R K +Luna | T in MUSEUM | K_CRUSH; after B1 |
| LT386 | G L | T in MUSEUM | LEDGER; D_MID; after L1 |
| LT387 | K G +Luna | E MUSEUM | K_ANY and (G_FLIRT or G_TOG+); after A1 |
| LT388 | V A | E MUSEUM | A_CRUSH (or later Ashe romance stage) and (V_FLIRT or V_TOG+); ASHE_REVEAL |
| LT389 | X C | T in MUSEUM | D_MID; after R18 |
| LT390 | L R X | E GUILD | BOARD; DISP_N >= 700; Exc01 150, Exc02 140, Exc03A 350 and SL 300 all done; LX; RX |

## Pacing
- At most one LT241-LT390 talk per in-game day inside the museum, and never two from the same Part in a row.
- The running bits (LEDGER, card wars, BOARD, quiz) at most one per two in-game days, so they feel like a slow-burning joke, not a binge.
- Milestone rows (LT251, LT305-LT308) fire on the first museum entry after DISP_N enters their band; if the band is skipped (a big delivery), they still play once on the next entry while DISP_N is above the band's floor.

## Open items
- DISP_N meaning (see above).
- Jagged Crown, Azura's Star/Black Star, Wabbajack, Oghma Infinium, Aetherium display flags: rows use the quest-done proxy (LT285-LT289).
- Tolfdir visit (LT363) and Remi-Redcap chain (LT253, LT357).
- DLC2RR03 = The Final Descent (LT361, LT362).
