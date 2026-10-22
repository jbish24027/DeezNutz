# 13b WYRMSTOOTH ETC 2 - trigger rows (WS161-WS240)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\13b WYRMSTOOTH ETC 2.txt`
Research: `research\content\bruma_moonpath_wyrmstooth_etc.md` sections 3-7, `research\triggers\vanilla_gates.md`. Part 1 rows, silence lists and every local gate code (`WT_*`, `SR_*`, `FC_*`, `SS_*`, `CT_*`) are defined in `triggers\13 WYRMSTOOTH SIRENROOT FORGOTTEN CITY SAINTS.md` and reused unchanged. Global codes: TRIGGERS.md section 4. Serana/Ashe Free() rows and codes (`SERANA`, `SER_VAMP`, `DG_CAIRN`, `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_LOGS`): `triggers\20 DAWNGUARD.md` sections 1 and 3, `triggers\48 SERANA.md`, `triggers\49 ASHE.md`. `K_AKAVIRI` = `GetStageDone KINV(0B3032:0Kaidan.esp) 50` (confirmed in 14b).

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, +Lu = Luna (player line, no Free check).
Type: T = timer, E = event. `E COMBAT` = in-fight bark path (same open item as part 1). `[unconfirmed]` = stage, cell or FormID not proven from the records; check at build or in game.

## Standing rules for this file
- All part-1 silences apply: Wyrmstooth boat crossing (`028F01` 10..49), draugr possession (135..159), Stonehollow defence and reward (230..269); Sirenroot 15..140; the whole Forgotten City location from `012BB9` 100 until FC_END; SEC 099D18 intro, 099D19 30..39, 09EF5F 80..99; Cursed Tribe DA06 60..69 and 100..109.
- Xelzaz is in no Sirenroot row (his own mod covers it). His Wyrmstooth rows (WS161, WS186) stay off his mod's topics.
- Every **S** row also needs `SERANA` and Serana's Free() row; every **A** row also needs `ASHE_HIRED`, her Free() row, her `bConfigVarIdles` toggle and her silence list (49 ASHE.md). Pair "first meeting" talks from 48 SERANA / 49 ASHE must have played ("S-x met" / "A-x met").
- Follow-up rows (`after:WSnn`) need the part-1 talk to have played.
- Reunion rows (WS188-WS192) are once-only per follower, same rule as part 1's SR_BACK reunions.

## New gate codes for this file
**Wyrmstooth** (all `Wyrmstooth.esp`, from the research table)
- `WT_SHARGAM` = `WTShargamFavor 3A1468` stage 10 done, 30 not done.
- `WT_ELMERA` = `WTElmeraFavor 3A146A` stage 10 done.
- `WT_CACHE` = `WTBlindRobbersCache 46DA2A` stage 10 done, 30 not done.
- `WT_BOUNTY_BANDIT` / `WT_BOUNTY_BEAR` / `WT_BOUNTY_VAMP` = the matching `WTBounty*` quest (`4B9DED` bandit, `4B9DEE` animal, `4B9DF0` vampire) running, stage 20 not done **[unconfirmed which of 4B9DED..4B9DF0 is which; the research lists Bandit / Animal / Warlock / Vampire in FormID order]**.
- `WT_NAKED_END` = `WTTheNakedNord C651DA` completed (any of stages 70..79).
- `WT_WRAP_DONE` = `WTWrapMeUp 3920D5` stage 30 done.
- `WT_SPIES_DONE` = `WTKillThalmor 3943A0` stage 30 done.
- `WT_FAELOR` = `WTWolfFollower 2E49AF` stage 40 done and Faelor is following (teammate check on his ref) **[unconfirmed check, as WS39]**.
- `WT_MINERS` = `WTPricelessCommodity 48F992` stage 15 done (the miners' side: kill the Matriarch).
- Places **[all unconfirmed LCTN/marker FormIDs; resolve by EditorID at build]**: `LOC:Twinpeak` (Twinpeak Tower), `LOC:Chillwater` (Chillwater Mill), `LOC:Frostvein` (Frostvein Mine, or within 2000 units of its door), `LOC:StonehollowHall` (Stonehollow Hall of the Dead), `LOC:Stonehollow`, `LOC:FortValus`, `LOC:HiddenPeak` (an Ascend hidden peak, as WS47), `LOC:Gronndal` (Gronndal Grove), `LOC:Cragwater` (Cragwater Cavern).

**Sirenroot**
- `SR_BACK_S`, `SR_BACK_A`, `SR_BACK_K`, `SR_BACK_G`, `SR_BACK_V` = the part-1 SR_BACK reunion condition, checked for that follower (first time they are within 1000 units after stage 140, once only).
- `SR_SNAPSHOT:<x>` = follower x was a teammate when `026BC5` stage 15 was set (controller snapshot) **[unconfirmed: needs the controller to record the party at the dive; if not built, drop the check and accept the small risk]**.
- `HONRICH` = exterior near Lake Honrich (WATER, Riften hold), as WS91/WS93.

**The Forgotten City** (`ForgottenCity.esp`)
- `FC_EXODUS` = `000FCQuestStatusExodus 0A8055` stage 1 done (the bathroom wall broken open).
- `FC_MAISI` = `000FCQuestMetellusDialogue 05ECD0` stage 200 done (confronted Metellus about Maisi) **[unconfirmed that 200 survives the loop reset; fallback Ulrin `072D0A` past his "wife found" stage]**.
- `FC_DEGLUND` = `000FCQuestDeglundDialogue 07646C` past the elixir-sold stage **[unconfirmed stage]**.
- `FC_RING` = `000FCQuestHabiqDialogue 0B8BD7` past the ring stage **[unconfirmed stage]**.
- `FC_GUUL` = `000FCQuestGuulDialogue 0BACC6` past the "Dooley's fortune" stage **[unconfirmed stage]**.
- `FC_QUARRY` = `000FCQuestStatusQuarryArmor 094809` stage 20 done.

**Saints and Seducers** (`Skyrim Extended Cut - Saints and Seducers.esp`, "SEC")
- `SS_MANIA` = SS_ISLES and the player is on the Mania side **[unconfirmed region check, as WS121]**.
- `SS_NEARCORGI` = in The Near Corgi Shop **[unconfirmed LCTN/cell]**.
- `SS_DYLORA` = `EC_SS_MQ101 099D19` stage 40 done.
- `SS_AMBER` = `EC_SS_TheodorQuest 099D1A` stage 255 done.
- `COMBAT:exile` = combat target in Thoron's Exiles faction **[unconfirmed faction FormID]**.

**The Cursed Tribe** (`DA06 03B681:Skyrim.esm`, winner TCTQE)
- `CT_HERE` = CT_START; player in `LargashburLocation 019263`; DA06 not 200/210 yet.
- `CT_RITUAL_DONE` = DA06 stage 70 done.
- `CT_GORAK` = DA06 stage 80 done (the giant named; normal route only).
- `CT_HAMMER` = DA06 stage 110 done.
- `LOC:Sanctum` = in the Sanctum of Malacath (renamed Giant's Grove, `0C33AF:Skyrim.esm`) **[unconfirmed that 0C33AF is the LCTN and not the map marker]**.
- `CT_GATE_GIANT` = DA06 stage 10 done, 20 not done, combat target is a giant, in or next to LargashburLocation.

## Table

### Part 1 - Wyrmstooth: the island's jobs and oddities
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS161 | X +Lu | T | WT_SHARGAM |
| WS162 | L R | T | WT_ELMERA; after B10 |
| WS163 | V I | T | WT_CACHE; after I1 |
| WS164 | G K | T | WT_BOUNTY_BANDIT; WT_ISLAND; after A1 |
| WS165 | A C | T | WT_BOUNTY_BEAR; WT_ISLAND; ASHE_REVEAL; A-C met |
| WS166 | V G | E LOC:Twinpeak | WT_ISLAND; after A3 |
| WS167 | G +Lu | E LOC:Chillwater | WT_ISLAND |
| WS168 | R K | E LOC:Frostvein | WT_STONEHOLLOW; after B1 |
| WS169 | S I | E LOC:StonehollowHall | WT_DEAD; S-I met |
| WS170 | S +Lu | E LOC:FortValus | WT_FORT |
| WS171 | S K | T | WT_POSSESSED; S-K met |
| WS172 | A +Lu | T | WT_POSSESSED; ASHE_LOGS |
| WS173 | S L | T | WT_DEAD; S-L met |
| WS174 | S V | T | WT_ALBERTHOR; S-V met; `AX_TarekDead != 1` (Val says "ask my father" in the present tense) |
| WS175 | A I | T | WT_FAELOR; ASHE_REVEAL; A-I met |
| WS176 | K R | T | WT_NAKED_END; after B1 |
| WS177 | L +Lu | T | WT_WRAP_DONE; after WS42 |
| WS178 | A K | T | WT_SPIES_DONE; K_AKAVIRI; A-K met |
| WS179 | L C | E WT_DIMFROST | after R11 |
| WS180 | A G | E arrival on WT_ISLAND (first exterior tick after `028F01` 50); fallback first T tick after arrival if WS5/WS6 took the event | WT_ARRIVED; ASHE_REVEAL; A-G met; SR_SNAPSHOT-style check that Ashe was a teammate at `028F01` stage 10 **[unconfirmed]** |
| WS181 | K +Lu | E LOC:Stonehollow | WT_DONE; K_TOG+ |
| WS182 | A K | E LOC:HiddenPeak | WT_ISLAND; ASHE_REVEAL; A-K met |
| WS183 | C G | E LOC:FortValus | WT_FORT; after WS27; after R5 |
| WS184 | A V | E LOC:Stonehollow | WT_DONE; ASHE_REVEAL; A-V met |
| WS185 | G V | E LOC:Stonehollow + CAMP or NIGHT | WT_DONE; after WS99; after A3 |
| WS186 | X I | E LOC:FortValus | WT_FORT; after WS27; after X6 |
| WS187 | S C | T | WT_BOUNTY_VAMP; SER_VAMP; S-C met |

### Part 2 - Sirenroot: you came back, part two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS188 | S +Lu | E reunion (SR_BACK_S) | SR_BACK |
| WS189 | A +Lu | E reunion (SR_BACK_A) | SR_BACK; ASHE_REVEAL |
| WS190 | K +Lu | E reunion (SR_BACK_K), priority 1 over WS70 | SR_BACK; K_MAR |
| WS191 | G +Lu | E reunion (SR_BACK_G); if WS72 already used Gore's reunion, first T tick after it | SR_BACK |
| WS192 | V +Lu | E reunion (SR_BACK_V); if WS74 already used Val's reunion, first T tick after it | SR_BACK; Redcap recruited (named in the talk) |
| WS193 | C S | T | SR_BACK; after WS73; SR_SNAPSHOT:Serana and SR_SNAPSHOT:Redcap |
| WS194 | S L | T | SR_BACK; DG_CAIRN; S-L met |
| WS195 | A R | T | SR_PAID; ASHE_REVEAL; A-R met |
| WS196 | I K | E HONRICH + NIGHT | SR_BACK; after WS67; KaiandInigo stage >= 10 |

### Part 3 - The Forgotten City: edge and debrief, part two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS197 | S +Lu | E in Forgotten Ruins cell | FC_EDGE |
| WS198 | A +Lu | E in Forgotten Ruins cell | FC_EDGE; ASHE_REVEAL |
| WS199 | A +Lu | T | FC_END; ASHE_Q1 |
| WS200 | S +Lu | T | FC_END |
| WS201 | V G | T | FC_END; FC_EXODUS; after A3 |
| WS202 | K +Lu | T | FC_END; FC_MAISI |
| WS203 | R +Lu | T | FC_END; FC_DEGLUND |
| WS204 | C +Lu | T | FC_END; FC_RING |
| WS205 | L R +Lu | T | FC_END; FC_QUARRY; after B10 |
| WS206 | V +Lu | T | FC_END; FC_GUUL |
| WS207 | A L | T | FC_END; ASHE_REVEAL; A-L met |
| WS208 | S G | T | FC_GOOD; S-G met |
| WS209 | A K | T | FC_END; after WS103; ASHE_REVEAL; A-K met |
| WS210 | S L | T | FC_END; S-L met |
| WS211 | C G | E CAMP (Luna's bedroll nearby) | FC_END; after WS109; after R5 |

### Part 4 - Saints and Seducers: the Isles, part two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS212 | S +Lu | T | SS_ISLES |
| WS213 | S K | T | SS_ISLES; S-K met |
| WS214 | A L | E exterior, SS_MANIA | SS_ISLES; ASHE_REVEAL; A-L met |
| WS215 | A +Lu | T | SS_ISLES; ASHE_REVEAL |
| WS216 | X R | T | SS_ISLES; Remi and Xelzaz not fallen out |
| WS217 | C G | E SS_NEARCORGI | SS_ISLES; after R5 |
| WS218 | S R | T | SS_DYLORA; S-R met |
| WS219 | A V | T | SS_AMBER; ASHE_REVEAL; A-V met |
| WS220 | I S | E exterior, SS_MANIA | SS_ISLES; SER_VAMP; S-I met |
| WS221 | A G | T | SS_ISLES; ASHE_REVEAL; A-G met |
| WS222 | X L | T | SS_ISLES or SS_DONE; after WS135; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| WS223 | C A | T | SS_ISLES; ASHE_REVEAL; A-C met |
| WS224 | K +Lu | T | SS_ISLES; K_TOG+ |
| WS225 | S A | T | SS_ISLES; ASHE_REVEAL; S-A met |
| WS226 | R +Lu | E exterior, SS_MANIA | SS_ISLES |

### Part 5 - The Cursed Tribe: Largashbur, part two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS227 | G S | E arrival in LargashburLocation (a later arrival than WS151) | CT_START; DA06 not 200/210; SER_VAMP; after WS151; S-G met |
| WS228 | S +Lu | T | CT_RITUAL_DONE |
| WS229 | A G | E in LargashburLocation | CT_HERE; ASHE_REVEAL; A-G met |
| WS230 | L G | E in LargashburLocation | CT_HERE; after L1 |
| WS231 | C R | T | CT_GORAK; after Redcap-Remi intro (FA01RemiIntroScene) |
| WS232 | X I | E in LargashburLocation interior (longhouse), player eating or at the cooking pot **[unconfirmed eat event; fallback E INN-style tick in the longhouse]** | CT_HERE; after X6 |
| WS233 | K +Lu | T | after WS154; at least 2 game days since WS154 played **[unconfirmed day counter]** |
| WS234 | I L | E in LargashburLocation + NIGHT | CT_HERE; DA06 stage 30 done; Lucien-Inigo intro done |
| WS235 | V R | E LOC:Sanctum | CT_GORAK; after BR80; after Val-Remi intro (HLIOValBanter stage 10) |
| WS236 | G C | T | CT_HAMMER; DA06 210 not done; after R5 |

### Part 6 - Fight barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WS237 | S G | E COMBAT vs spriggan in LOC:Gronndal | WT_MINERS; S-G met |
| WS238 | A K | E COMBAT in LOC:Cragwater | WT_ISLAND; ASHE_REVEAL; A-K met |
| WS239 | S L | E COMBAT:exile in the Isles | SS_ISLES; `09EF5F` stage 90 not done; S-L met |
| WS240 | A C | E COMBAT | CT_GATE_GIANT; ASHE_REVEAL; A-C met |

## Open items for build
- All `[unconfirmed]` items above, especially the Wyrmstooth place LCTNs, which WTBounty FormID is which bounty, and the Forgotten City per-resident stages (WS202-WS206). If a resident stage cannot be found, the fallback is FC_END only, but then the talk can play for a player who never met that resident; prefer dropping the talk.
- WS190 (K_MAR) and WS70 (K_TOG+) share Kaidan's reunion event. When K_MAR is true, WS190 takes the event and WS70 is skipped. WS69/WS70 stay as they are for every other stage.
- WS191 / WS192 share Gore's and Val's reunion with WS72 / WS74; whichever fires first takes the event, the other plays as the next T tick.
- WS193 needs both Serana and Redcap to have been at the lake while Luna was under it. Without the snapshot check it can claim they dug when they were not there.
- WS180 claims Ashe was on the boat; without a snapshot it is still mostly safe (the boat crossing moves the party), but check that followers really cross with you.
- WS174's "ask my father" assumes Tarek is alive; the `AX_TarekDead` check keeps it off the Tarek-dead branch.
- No script change was needed: every talk can be gated.
