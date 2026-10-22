# 30 MAIN QUEST DEEP - trigger rows (prefix MQ, 120 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\30 MAIN QUEST DEEP.txt`.
Sources: `research\triggers\vanilla_gates.md` Part A (A1-A4) and B1, `research\triggers\kaidan_block.md` (KINV), `research\bibles\*.md` (serana, ashe, lucien), TRIGGERS.md sections 2-5, the DG gate codes in `triggers\20 DAWNGUARD.md` section 3.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`, which already holds every MQ silence window from vanilla_gates A4) and section 3 (`Free`), plus the Serana/Ashe Free rows in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player line, Eleonora voice; no Free test, but the player must not be in dialogue).
Type: T = timer, E = event (fires on the moment). A T row whose stage is reached inside a silence window simply waits for the first tick after the window ends.

## 1. Load-order notes for the main quest

- **Alternate Perspective**: Helgen may still be standing for weeks. Only `HELGEN` (MQ101 145) means it burned. AP "skip to MQ105" fakes MQ104 90/160/200 but never 80.
- **At Your Own Pace** (MQ103, MQ105Ustengrav, MQ106; break globals AYOPMQ103Break / 104Break / 105Break / 301Break): delays steps, keeps stage numbers. No gate below assumes one step follows another quickly.
- **Paarthurnax Quest Expansion** (MQPaarthurnax 03FA16:Skyrim.esm): 50 = killed; 99/100 = Blades talked round; 150 = Greybeards angry. Branch talks are gated per branch; demand talks are neutral.
- **Storm the Thalmor Embassy** (wins MQ201): stage shape is vanilla, but it adds a forced-entry route. The "you went to the party alone / reunion" rows use `EMB_PARTY` (MQ201 35 done = Delphine took the followers away). **[UNC: confirm the storm route never sets 35; if it does, find the storm-route flag and exclude it]**.
- **Lucien** leaves (or turns hostile, JRLucienBetrayedFaction 277B82:Lucien.esp) if Paarthurnax is killed. Every Lucien row after the Blades' demand carries `LUC_OK`. His own mod also has him part ways before the Odahviing flight; Free() handles whether he is back.
- **Kaidan's Akaviri secret**: only MQ59 names it, and only after his own KINV quest is done (`K_AKAVIRI`). MQ58 is the "before" version and never names it.

## 2. Gate codes used in this file

Existing (TRIGGERS.md section 4): `HELGEN`, `DB`, `SHOUT1`, `HH`, `GREYBEARDS`, `DELPHINE`, `PAARTH`, `ALDUIN`, `BRYNJAR`, `K_CRUSH`, `K_TOG+`, `K_ANY`, `G_FLIRT`, `G_TOG+`, `V_FLIRT`, `V_TOG+`, `ANYROM`, `CITY:<name>`, `AFTERFIGHT[:enemy]`.
Existing (20 DAWNGUARD.md section 3): `SERANA` (DLC1VQ02 5 done; Serana following per her Free row), `S_KISS`, `A_ANY`, `ASHE_REVEAL`.

New, story (Skyrim.esm unless noted):
- `DBX` = `DB` OR GetStageDone MQ106(032926) 150. The "Dragonborn" word gate for late talks: AP skip-to-MQ105 players never get MQ104 80 but have truly taken Sahloknir's soul by Kynesgrove. Every row whose lines say "Dragonborn" carries `DB` or `DBX`.
- `MQ103_RUN` = GetQuestRunning MQ103 ("Bleak Falls Barrow"). **[UNC FormID: look up MQ103 in Skyrim.esm; AYOP overrides it, stages unchanged]**
- `MQ103_DONE` = GetQuestCompleted MQ103.
- `STONE` = player GetItemCount Dragonstone >= 1 (first time). **[UNC FormID of the Dragonstone MISC item]**
- `CLAW` = player GetItemCount Golden Claw >= 1. **[UNC FormID]**
- `ARVEL_DEAD` = Arvel the Swift ref GetDead == 1. **[UNC ref FormID]**
- `THANE` = GetStageDone MQ104(02610C) 160. [CONFIRMED stage]
- `SUMMONS` = DB AND GetQuestRunning MQ105(0242BA) AND GetStageDone MQ105 20 == 0 (called to High Hrothgar, not there yet). **[UNC: AYOP's AYOPMQ104Break delays the summons shout; if MQ105 can start before the shout plays, add MQ104 stage 130 done]**
- `TRIALS` = GetStageDone MQ105 160 (Greybeard trials over; Whirlwind Sprint learned by then). **[UNC: exact Borri/Wuld stage; vanilla_gates gives the trials window 20..159]**
- `WAY_DONE` = GetQuestCompleted MQ105 (horn returned, stage 300). [CONFIRMED]
- `HORN_NOTE` = GetStageDone MQ106 5 (note found, told to rent the attic). [CONFIRMED]
- `KYNES` = GetStageDone MQ106 150 (saw Alduin raise Sahloknir). [CONFIRMED]
- `DELPH_CONV` = GetQuestCompleted MQ106 (Delphine convinced). **[UNC: vanilla_gates says stage 50 is "convinced her"; if 50 is set after 150 in this order, use 50]**
- `EMB_PLAN` = GetQuestRunning MQ201 AND GetStage MQ201 < 35 (party planned, not yet inside). **[UNC: MQ201 start stage]**
- `EMB_PARTY` = GetStageDone MQ201 35 (Delphine took the followers; party route). **[UNC with Storm the Thalmor Embassy, see section 1]**
- `EMB_DONE` = GetQuestCompleted MQ201. **[UNC end stage; vanilla_gates silence is 35..249]**
- `EMB_REUNION` = event: first controller tick after EMB_DONE where 2+ party members are Free near the player. One talk only (MQ41 or MQ44).
- `RATWAY_HUNT` = GetQuestRunning MQ202(036191) AND not ESBERN.
- `ESBERN` = GetStageDone MQ202 150 OR GetStageDone MQ203(036192) 10. **[UNC exact stage, per vanilla_gates A3]**
- `SKYHAVEN` = GetStageDone MQ203 230. [CONFIRMED]
- `WALL` = GetQuestCompleted MQ203 (Alduin's Wall read; stages 210..280 silenced).
- `BLADES_RECRUIT` = FreeformSkyHavenTempleA started. **[UNC FormID; PQE overrides FreeformSkyHavenTemple A/C/D]**
- `SCROLL_HUNT` = GetQuestRunning MQ205(02D516) AND GetStageDone MQ205 10.
- `ESCROLL` = player GetItemCount Elder Scroll (Dragon) >= 1 OR GetQuestCompleted MQ205. **[UNC: scroll FormID; MQ205 may complete on pickup]**
- `DRAGONREND` = GetStageDone MQ206(036193) 100. [CONFIRMED]
- `ALDUIN_FLED` = GetQuestCompleted MQ206 (Alduin flees the Throat; silence 20..219).
- `PQ_DEMAND` = GetQuestRunning MQPaarthurnax(03FA16) AND GetStageDone 50 == 0 AND 99 == 0 AND 100 == 0. **[UNC: MQPaarthurnax start stage (Delphine's demand); add it as a lower bound]**
- `PAARTH_DEAD` = GetStageDone MQPaarthurnax 50. [CONFIRMED]
- `PAARTH_SPARED` = GetStageDone MQPaarthurnax 99 OR 100 (PQE). [CONFIRMED]
- `GB_ANGRY` = GetStageDone MQPaarthurnax 150 (PQE). [CONFIRMED stage; which branch sets it is not traced, so MQ81 is written cause-neutral]
- `LUC_OK` = NOT PAARTH_DEAD (and Lucien Free, not in JRLucienBetrayedFaction).
- `COUNCIL` = GetQuestCompleted MQ302(045923). [CONFIRMED]. Never fires if the civil war ended first (no council); that is fine.
- `TRAPPED` = GetQuestCompleted MQ301 OR GetStageDone MQ303 5 (Odahviing caught in Dragonsreach). **[UNC: MQ301 trap stage; silence 200..219]**
- `ALDUIN_HOME` = GetQuestCompleted MQ305(046EF2) AND GetQuestRunning MQ306(046EF3) == 0 (back from Sovngarde, dragons' gathering over).
- `REUNION` = event: first controller tick with ALDUIN_HOME where 2+ party members are Free near the player. Fires MQ94 only; the rest of Part 13 are T rows `after:MQ94`.
- `K_AKAVIRI` = GetStageDone KINV(0B3032:0Kaidan.esp) 50 (his "All of this Past" quest done). `NOT_K_AKAVIRI` = the opposite.

New, places and events:
- `LOC:BFB` = in BleakFallsBarrowLocation **[UNC FormID]**.
- `LOC:Watchtower` = in WhiterunWatchtowerLocation 0D9079.
- `PATH:HH` = the 7000 Steps event used by Q4 (TRIGGERS.md Quests table).
- `LOC:HH` = in HighHrothgarLocation 018E34, outside MQ105 20..159 and 240..299.
- `LOC:Ustengrav` **[UNC FormID]**. `LOC:Ratway` = Riften Ratway / Ratway Warrens / Ratway Vaults locations **[UNC FormIDs]**. `LOC:Karthspire` **[UNC FormID]**. `LOC:SkyHaven` = SkyHavenTempleLocation 018E42, outside MQ203 210..280. `LOC:Septimus` = Septimus Signus's Outpost **[UNC]**. `LOC:Mzark` = Tower of Mzark (Blackreach) **[UNC]**.
- `SOUL` = event: player absorbs a dragon soul (same hook as K9 in Kaidan and Luna).
- `DREND_USED` = player cast Dragonrend during the fight (OnSpellCast / shout VoiceDragonrend) **[UNC: needs a script hook]**.
- `AFTERFIGHT:dragon` = last combat target has ActorTypeDragon **[UNC keyword FormID]**. `:draugr`, `:Thalmor`, `:forsworn` as TRIGGERS.md.
- `TOWN` = player location has LocTypeCity / LocTypeTown / LocTypeSettlement.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| MQ1 | L P | T | MQ103_RUN |
| MQ2 | V K | T | MQ103_RUN |
| MQ3 | G X | E LOC:BFB | not HELGEN (Helgen still standing; works with or without MQ103) |
| MQ4 | R K | T | MQ103_RUN; HELGEN; not STONE |
| MQ5 | I R | E CLAW picked up | LOC:BFB [UNC CLAW FormID] |
| MQ6 | G V | E LOC:BFB | ARVEL_DEAD [UNC] |
| MQ7 | C L P | E STONE picked up | LOC:BFB (the word wall plays right after; fire after the wall's own lock ends) [UNC] |
| MQ8 | X A | T | MQ103_RUN; STONE; not in LOC:BFB |
| MQ9 | K P | T | MQ103_DONE |
| MQ10 | L P | T | DB |
| MQ11 | X P | T | DB |
| MQ12 | K G | T | DB |
| MQ13 | V G | T | THANE |
| MQ14 | R I | E LOC:Watchtower | DB; THANE (outside the watchtower silence) |
| MQ15 | C K | E CITY:Whiterun | DB |
| MQ16 | A P | E SOUL | DB; ASHE_REVEAL |
| MQ17 | S P | E SOUL | DB; SERANA |
| MQ18 | V C | T | SUMMONS |
| MQ19 | P X | E PATH:HH | DB (plays on a different climb from Q4 if Q4 took the first one) |
| MQ20 | G R | E LOC:HH | TRIALS |
| MQ21 | K A | E LOC:HH | GREYBEARDS |
| MQ22 | I C | T | TRIALS |
| MQ23 | A G | T | GREYBEARDS |
| MQ24 | K V | E LOC:Ustengrav | GREYBEARDS; GetQuestRunning MQ105; not HORN_NOTE |
| MQ25 | K P | E LOC:HH | HH; K_CRUSH |
| MQ26 | R V P | T | HORN_NOTE |
| MQ27 | G I | T | HORN_NOTE; not DELPHINE |
| MQ28 | K P | T | DELPHINE |
| MQ29 | L X | T | DELPHINE |
| MQ30 | C P | T | DELPHINE (map shown in the secret room) [UNC: map stage; MQ106 30 is enough] |
| MQ31 | A K | T | WAY_DONE |
| MQ32 | S G | T | GREYBEARDS; SERANA |
| MQ33 | R L | T | KYNES |
| MQ34 | K G | T | KYNES; DBX |
| MQ35 | P X | T | KYNES |
| MQ36 | K V | T | KYNES; K_ANY |
| MQ37 | G P | T | DELPH_CONV |
| MQ38 | A R | T | KYNES |
| MQ39 | V R | T | EMB_PLAN |
| MQ40 | K P | T | EMB_PLAN |
| MQ41 | I P | E EMB_REUNION | EMB_DONE; EMB_PARTY |
| MQ42 | K P | T | EMB_DONE |
| MQ43 | L P | T | EMB_DONE |
| MQ44 | G K | T or E EMB_REUNION | EMB_DONE; EMB_PARTY |
| MQ45 | X V | T | EMB_DONE |
| MQ46 | G V | T | EMB_DONE |
| MQ47 | K G V | T | EMB_DONE; EMB_PARTY; ANYROM |
| MQ48 | S A | T | EMB_DONE; EMB_PARTY; SERANA |
| MQ49 | C G | E LOC:Ratway | RATWAY_HUNT |
| MQ50 | I K | T | ESBERN |
| MQ51 | L P | T | ESBERN; DBX |
| MQ52 | A X | T | ESBERN |
| MQ53 | K P | T | ESBERN |
| MQ54 | R G | T | ESBERN; not SKYHAVEN |
| MQ55 | G X | E LOC:Karthspire | GetQuestRunning MQ203; not SKYHAVEN |
| MQ56 | R P | T | SKYHAVEN; DBX |
| MQ57 | L V | E LOC:SkyHaven | SKYHAVEN |
| MQ58 | K I | E LOC:SkyHaven | SKYHAVEN; NOT_K_AKAVIRI |
| MQ59 | K P | E LOC:SkyHaven | SKYHAVEN; K_AKAVIRI |
| MQ60 | C P | T | WALL |
| MQ61 | G V | T | BLADES_RECRUIT; DBX [UNC FormID] |
| MQ62 | S P | T | WALL; SERANA |
| MQ63 | V X | E LOC:Septimus | SCROLL_HUNT |
| MQ64 | L R | E LOC:Mzark | SCROLL_HUNT; not ESCROLL |
| MQ65 | G I | T | ESCROLL; not DRAGONREND |
| MQ66 | L P | T | DRAGONREND |
| MQ67 | K P | T | ALDUIN_FLED; DBX |
| MQ68 | G C | T | ALDUIN_FLED |
| MQ69 | A P | T | DRAGONREND; ASHE_REVEAL |
| MQ70 | S P | T | ALDUIN_FLED; SERANA; S_KISS |
| MQ71 | A K | T | ALDUIN_FLED; A_ANY |
| MQ72 | K G | T | PQ_DEMAND |
| MQ73 | X I | T | PQ_DEMAND |
| MQ74 | V P | T | PQ_DEMAND |
| MQ75 | G I | T | PAARTH_DEAD |
| MQ76 | K P | T | PAARTH_DEAD |
| MQ77 | C R | T | PAARTH_DEAD |
| MQ78 | V G P | T | PAARTH_SPARED |
| MQ79 | L P | T | PAARTH_SPARED (LUC_OK implied) |
| MQ80 | A V | T | PAARTH_SPARED |
| MQ81 | G V | T | GB_ANGRY |
| MQ82 | K P | T | COUNCIL |
| MQ83 | G I | T | COUNCIL [UNC: Elenwen is present at the start in both seat outcomes; line says she "walked in"] |
| MQ84 | R V | T | COUNCIL |
| MQ85 | C X | T | COUNCIL |
| MQ86 | G K | T | COUNCIL |
| MQ87 | L S | T | COUNCIL; SERANA; LUC_OK |
| MQ88 | A G | T | COUNCIL |
| MQ89 | V G | T | TRAPPED |
| MQ90 | P K | T | TRAPPED |
| MQ91 | R C | T | TRAPPED |
| MQ92 | I X | T | ALDUIN_HOME; after:MQ94 |
| MQ93 | K G | T | TRAPPED; K_ANY |
| MQ94 | K G | E REUNION | ALDUIN_HOME |
| MQ95 | R P | T | ALDUIN_HOME; after:MQ94 |
| MQ96 | G P | T | ALDUIN_HOME; after:MQ94 |
| MQ97 | K P | T | ALDUIN_HOME; BRYNJAR; after:MQ94 |
| MQ98 | X V | T | ALDUIN_HOME; after:MQ94 |
| MQ99 | I P | T | ALDUIN_HOME; after:MQ94 |
| MQ100 | S P | T | ALDUIN_HOME; SERANA; after:MQ94 |
| MQ101 | C V | T | ALDUIN_HOME; after:MQ94 |
| MQ102 | L P | T | ALDUIN_HOME; LUC_OK; after:MQ94 |
| MQ103 | K G V | T | ALDUIN_HOME; ANYROM; after:MQ94 |
| MQ104 | A S | T | ALDUIN_HOME; SERANA; S_KISS or A_ANY; after:MQ94 |
| MQ105 | G R | T | ALDUIN_HOME |
| MQ106 | K P | T | ALDUIN_HOME; K_TOG+ |
| MQ107 | L I | T | ALDUIN_HOME; DBX; LUC_OK |
| MQ108 | K X | T | ALDUIN_HOME |
| MQ109 | C G | T | ALDUIN_HOME |
| MQ110 | G V | T | ALDUIN_HOME; PAARTH_DEAD or PAARTH_SPARED (Esbern still allied) |
| MQ111 | G K | E AFTERFIGHT:dragon | DBX |
| MQ112 | I K | E AFTERFIGHT:dragon + DREND_USED | DRAGONREND [UNC hook] |
| MQ113 | L R | E AFTERFIGHT:draugr | LOC:BFB |
| MQ114 | K V | E AFTERFIGHT:Thalmor | LOC:Ratway; RATWAY_HUNT or ESBERN |
| MQ115 | K X | E AFTERFIGHT:forsworn | LOC:Karthspire; GetQuestRunning MQ203 |
| MQ116 | R C | E AFTERFIGHT:dragon | KYNES |
| MQ117 | S A | E AFTERFIGHT:dragon | DBX; SERANA |
| MQ118 | L V | E AFTERFIGHT:dragon | DBX; TOWN; LUC_OK when PQ_DEMAND or later |
| MQ119 | G K | E AFTERFIGHT:Thalmor | EMB_DONE; not LOC:Ratway |
| MQ120 | K P | E AFTERFIGHT:dragon | DBX; K_TOG+ |

## 4. Open items to verify at build
- FormIDs: MQ103, Dragonstone, Golden Claw, Arvel ref, Elder Scroll (Dragon), FreeformSkyHavenTempleA, BleakFallsBarrowLocation, Ustengrav, Ratway set, Karthspire, Septimus's Outpost, Tower of Mzark, ActorTypeDragon.
- Stages: MQ105 trials end (160), MQ106 "convinced" (50 vs completion), MQ201 start/end and the Storm route, MQ202 Esbern met, MQPaarthurnax demand stage, which branch sets 150, MQ301 trap stage.
- Hooks: SOUL (dragon soul absorbed), DREND_USED, EMB_REUNION, REUNION.
