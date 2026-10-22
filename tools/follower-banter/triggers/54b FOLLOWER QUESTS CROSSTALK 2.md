# 54b FOLLOWER QUESTS CROSSTALK 2 - trigger rows (prefix FL, FL201-FL320, 120 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\54b FOLLOWER QUESTS CROSSTALK 2.txt`. Luna speaks in 40 (33%) of talks.
Part one and its gate codes: `triggers\54 FOLLOWER QUESTS CROSSTALK.md` (sections 1-2 apply here unchanged: K_FREED, K_AKAVIRI, K_COMP, K_JAIL, KMD_DONE, K_HONEY, G_WANTED, G_DH, G_CROWS, G_STAND, G_NEST, G_FEAR, GORE_VIG, V_RESCUED, V_STAR, V_BOAT, V_GRAD, V_PIT, V_RAVANI, R_SCRAP, R_STEAM, R_XBOW, R_LANTERN, R_FORK, R_PIE, X_STAYED, X_TREE, X_LEAF, L_CLIVE, L_PAARTH_BACK, RC_FREED, S_TRUST, I_TRUTH, and the pair "met" codes).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`, including the Kaidan section 2b set-piece list for talks WITHOUT Kaidan) and section 3 (`Free`), the Serana/Ashe Free rows in `20 DAWNGUARD.md` section 1, the Ashe silence in `49 ASHE.md`, and Gore's `G_OK` in `22 VIGILANT GLENMORIL UNSLAAD.md`. Rival codes (`S_ACT`, `G_PAST`, `V_PAST`, `A_PAST`, `A_CRUSH`, `A_LOVE`) as `53 RIVALRY.md`. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but player not in dialogue). Codes are in speaking order.

## 1. Rules of this file: before, during (safely), after

- **During talks** (marked `DURING` below) are timer talks that need the follower's quest to be in a quiet, scene-free state AND that follower must NOT be a speaker. Each one also carries `notin:<places>` where the follower's scripted beats happen. If a "during" window cannot be read safely at build, drop that row rather than widen it.
- The Kaidan "during" rows only use beats that kaidan_block.md lists as having **no scenes** (KINV "All of this Past", KaiSandwich) or where Kaidan has **left the party** (KBountyAI) or a **mood arc without scenes** (KMDNightmares, and that row never names the cult or the dreams). All Kaidan section 2a/2b blocks stay on.
- **Kaidan's cult past** (Dagon, the tattoo's origin, "setting fire to things") appears only in rows gated `KMD_DONE`.
- **Branch talks** carry the branch gate; everything else is written branch-neutral.
- Keep the part-one pacing: at most one FL talk per follower's quest per in-game day.

## 2. New gate codes (this file)

Kaidan (kaidan_block.md FormIDs):
- `KINV_RUN` = KINV 0B3032:0Kaidan.esp running, stage >= 1, not completed (dialogue only, no scenes). **[UNC: which stage means he has shared the Northwind clue; use >= 10 if it exists]**
- `KCOMP_ASKED` = KaiComp 162E4A:IF stage 10 or 20 done AND stage < 30 (the 48 h wait before the trial; no scenes yet).
- `KBOUNTY_AWAY` = KBountyAI 55EDDE:IF running (Kaidan has left to hunt). Kaidan is never a speaker. `KBOUNTY_BACK` = controller flag set the first tick KBountyAI goes from running to stopped **[UNC: needs a controller flag; the quest Stop()s at 255]**.
- `KSANDWICH_RUN` = KaiSandwich 2DD53E:IF running and stage < 200 (no scenes).
- `KSPAR_ONCE` = KaiSparQst 22970E:IF has stopped at least once after starting **[UNC: controller flag]**.
- `KTHALMOR_DONE` = WEKaiThalmor 35EE2E:IF stage 255 done.
- `KNIGHTMARE_MID` = KMDNightmares 8E7001:IF running and stage < 50 AND global AubrieandVaelHateYou 8F1275:IF == 0 AND denialisntjustariver EE8C9B:IF == 0 (not in his worst days). Kaidan is never a speaker.

Gore (GORE.esp):
- `GQ2_EARLY` = HD1GoreQuest2 5A610A running and stage < 10. **[UNC: stage 0 is the long "get to know him" state; the talk stays vague about where he wants to go]**
- `GORE_INCELL` = HD1GoreJailed 61307D == 1 and HD1GoreJailtime 6245B4 stage 30 not done (bail not yet paid). Gore never a speaker.
- `G_INTEREST` = HD1Romance 6D6924 == 1. `G_HEALING` = HD1Healing 777ABE == 1 **[UNC: branch meaning from the bible]**.
- `G_OATH` as TRIGGERS.md (HD1GoreRomance3 >= 3).
- `G_PREDH` = G_WANTED and HD1GoreDH 3E8DC9 not completed.

Val (AX ValSerano.esp):
- `V_MORA_SECRET` = V_RESCUED and not VAL_FATHIS (he still only says "Mora and I have history").
- `VAL5_MID` = Val005 49DC31 stage >= 3 and < 200, and player not in Apocrypha (Val005SB not running, GetInCurrentLoc 652304 == 0). Val never a speaker.
- `VAL_TAKEN` = Val00B 49DC33 stage >= 15 and < 200, and AX_ValSightlessPit 9B244D == 1. Val never a speaker; notin the Sightless Pit.
- `V_ENGAGED` = AX_ValEngaged A2205B == 1 and AX_ValMarried A22094 == 0, and Val00C 9B2444 stage < 40 (no ceremony running).
- `V_LAKE` = Val00ALakeDate D73448 completed.

Remi (HLIORemi.esp):
- `MORVIC_MID` = HLIOMQ1 46FA55 stage >= 10 and < 180, and not in Arkngchal **[UNC: Arkngchal location FormID]**. Remi never a speaker.
- `R_SHOCK` = HLIOScrapUpgrades 08E59F stage 30 done and 50 not done. `R_UPGRADES_LEFT` = stage 50 not done.
- `R_WORKSHOP` = HLIOMQ1 220 done.
- `ARK_EXPLORE` = HLIOArkngchalManager 6A304E stage 1..59, HLIOPuzzleTime 82F1DD != 1, player in Arkngchal **[UNC location]**. Remi never a speaker.
- `LANTERN_RUN` = HLIORPLantern 8486EB stage 10..49. `LOCK_RUN` = HLIORPLock 237EE7 stage 20..69. `PIE_RUN` = HLIOChaurusPieQuest 59B47F stage 30..79. Remi never a speaker in these three (her Free row blocks her anyway).

Xelzaz (BPUFXelzazFollower.esp):
- `X_ESCORT10` = BPUFXelzazEscortQuest 1BE431 stage 10..19 (long get-to-know state; not blocked).
- `X_ESCORT_MID` = stage 20..49 (walking to the Hammerfell gate). Xelzaz never a speaker.
- `X_LEFT` = stage 60 or 65 done (he went on to High Rock) **[UNC: which leaving endings are "went on"; never 444/555/666/777 if those mean dismissal or death]**. Xelzaz not present (talk needs him absent).
- `X_TREE_MID` = BPUFXelzazTheSleepingTree 79F4DA stage 20 done, not completed, 80 not done. Xelzaz never a speaker.
- `X_BLACKREACH_ALONE` = BPUFXelzazCrimsonNirnroot C6E975 stage 14 done, 23 not done.
- `X_LEAF_MID` = BPUFXelzazLostHistLeaf E408E2 running, stage 15 not done. Xelzaz never a speaker.
- `RX_SULK` = BPUFXelzazRemielFallingOut 5E67BB stage 11 done, 13 not done (Remi+Xelzaz never together in a talk then). `RX_MADEUP` = stage 13 done.

Inigo (Inigo.esp):
- `BV_FITS` = InigoBadVibrations 0695C5 stage 10 done, not completed, stage < 70. Inigo never a speaker.
- `BV_HUNT` = stage >= 70, not completed. `I_BELIEVES` = Inigo recruited and not I_TRUTH **[UNC as part one]**.

Lucien (Lucien.esp):
- `LUC_LETTER` = JRLucienPersonal1 2B13ED stage 30 done, 35 not done.
- `LUC_HIDING` = JRLucienGetHorseQuest 62424C stage 10..39. Lucien never a speaker.
- `LUC_GONE` = JRLucienPaarthurnax 1171E9 stage 10 done, 15 not done, Lucien NOT in JRLucienBetrayedFaction 277B82 and not dead (he left; he is not hostile).

Redcap (FA01RedcapFollower.esp):
- `RC_SAILING` = FA01RedcapSolstheimStartQ 0D0784 stage 10..19.
- `MANOS_MID` = FA01RedcapSolstheimManosQ 0D58E3 running. Redcap never a speaker; notin Manos's ship cell **[UNC cell]**.
- `REDGOD_WAIT5` = FA01RedcapRedGodQ 135DED stage 5 exactly (before Sanguine shows himself on stage 10) **[UNC: whether Redcap has met "Sam" by stage 5]**.
- `PIG_TAKEN` = FA01RedcapWereboarQ 18C066 running. Redcap never a speaker.
- `RC_PARTY` = FA01RedcapMQParty 065E29 completed **[UNC: what the party quest contains; the talk only names its title]**.

Serana (SeranaDialogAddon.esp):
- `S_CURE_AWAY` = SDA_CureQuestTimer 5EE3E9 running (Serana has gone to Falion alone). Serana never a speaker.
- `S_DETERMINED` = SDA_SeranaRomance08 B2A83E completed. `S_COVENANT` = SDA_SeranaRomance10 B2F967 completed.

Ashe (Ashe - Fire and Blood.esp):
- `NOT_REVEAL` as 49 ASHE.md. `ASHE_ALONE` = MM_AMQ_04 00AA1A:Ashe - Fire and Blood.esp stage 45..80; Ashe not present (she stays in the lab). `ASHE_ORPHANS`, `ASHE_EPI` as 49 ASHE.md.

Cross-quest:
- `QDONE>=n` = at least n of these are true: K_AKAVIRI, K_COMP, KMD_DONE, GORE_FATHER, GORE_BAIL, VAL_FATHER, VAL_FATHIS, REMI_MORVIC, X_STAYED, INIGO_BV, LUC_ENGINE, RC_STAY, DG_END, ASHE_SUMMIT.
- `PAARTH_ALIVE` = MQPaarthurnax not done with Paarthurnax killed (Paarthurnax ref not dead) **[UNC ref]**.

## 3. Per-talk table

### Kaidan's quests (FL201-FL218)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL201 | G V P | T DURING | KINV_RUN; K not a speaker; after A3 |
| FL202 | K P | T DURING | KINV_RUN |
| FL203 | V K P | T | K_AKAVIRI; DB; after A2 |
| FL204 | L K | T | K_AKAVIRI; DELPHINE; LK_MET |
| FL205 | I K | T BEFORE | KCOMP_ASKED; KI_MET |
| FL206 | C K | T | K_COMP; after R1 |
| FL207 | G K | T | K_COMP; after A1 |
| FL208 | L K P | T | K_JAIL; LK_MET |
| FL209 | G V P | T DURING | KBOUNTY_AWAY; K not a speaker; after A3 |
| FL210 | I K | T | KBOUNTY_BACK [UNC flag]; KI_MET |
| FL211 | X R | T DURING | KSANDWICH_RUN; RX_OK; not RX_SULK |
| FL212 | A G | T | KSPAR_ONCE [UNC flag]; ASHE_REVEAL |
| FL213 | G X | T | KTHALMOR_DONE; after X1 |
| FL214 | I G | T DURING | KNIGHTMARE_MID; K not a speaker; after C2 |
| FL215 | S K | T | KMD_DONE; SE42 played |
| FL216 | V K | T | KMD_DONE; VAL_FATHIS; after A2 |
| FL217 | L K | T | KMD_DONE; LUC_ENGINE; LK_MET |
| FL218 | A K | T | KMD_DONE; ASHE_REVEAL; AS1 played |

### Gore's quests (FL219-FL230)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL219 | K V P | T BEFORE | GQ2_EARLY; G not a speaker; after A2 |
| FL220 | R L P | T DURING | GORE_INCELL; notin Dawnstar jail cell; after B10 |
| FL221 | K G | T | G_STAND; G_INTEREST; K_CRUSH; after A1 |
| FL222 | S G | T | GORE_FATHER; SE2 played |
| FL223 | R I | T | G_OATH; B6 played |
| FL224 | L K | T | G_OATH; K_CRUSH; LK_MET |
| FL225 | G V | T | G_FEAR; VAL_FATHIS; after A3 |
| FL226 | C G P | T | GORE_BAIL; after R5 |
| FL227 | X G | T BEFORE | G_PREDH; after X1 |
| FL228 | I G | T | G_STAND; G_HEALING [UNC]; after C2 |
| FL229 | R P | T | G_FEAR; R_LANTERN |
| FL230 | G A | T | G_NEST; ASHE_ORPHANS; AS13 played |

### Val's quests (FL231-FL242)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL231 | X V P | T | V_MORA_SECRET; after X4 |
| FL232 | X V | T | VAL_FATHER; after X4 |
| FL233 | G K | T DURING | VAL5_MID; V not a speaker; after A1 |
| FL234 | G V | T | VAL_FATHIS; after A3 |
| FL235 | R K | T DURING | VAL_TAKEN; V not a speaker; notin Sightless Pit; after B1 |
| FL236 | G K | T | V_ENGAGED; K_CRUSH; after A1 |
| FL237 | S V | T | V_LAKE; S_ACT; SE3 played |
| FL238 | R V P | T | V_GRAD; HLIOValBanter stage >= 10 |
| FL239 | I V | T | V_RAVANI; after I1 |
| FL240 | A V | T | V_RESCUED; ASHE_REVEAL; AS19 played |
| FL241 | V P | T | V_GRAD; MG_JOIN |
| FL242 | V K | T | V_PIT; K_CRUSH; after A2 |

### Remi's quests (FL243-FL254)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL243 | V G | T DURING | MORVIC_MID; R not a speaker; after A3 |
| FL244 | A R | T | REMI_MORVIC; ASHE_ROLEN1; AS39 played |
| FL245 | C R P | T | R_SHOCK; RC_MET |
| FL246 | K R | E DWEMER | R_UPGRADES_LEFT; after B1 |
| FL247 | X R | T | R_WORKSHOP; RX_OK; not RX_SULK |
| FL248 | R A | T | R_STEAM; ASHE_REVEAL; AS39 played |
| FL249 | V R | T | REMI_MORVIC; HLIOValBanter stage >= 10 |
| FL250 | L X | T DURING | ARK_EXPLORE; R not a speaker; XL_MET |
| FL251 | L R P | T | R_FORK; LUC_ADMIT; after B10 |
| FL252 | K G P | T DURING | LANTERN_RUN; R not a speaker; after A1 |
| FL253 | V I | T DURING | LOCK_RUN; R not a speaker; after I1 |
| FL254 | X P | T DURING | PIE_RUN; R not a speaker |

### Xelzaz's quests (FL255-FL264)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL255 | G V P | T BEFORE | X_ESCORT10; X not a speaker; after A3 |
| FL256 | K I | T DURING | X_ESCORT_MID; X not a speaker; KI_MET |
| FL257 | R C | T | X_LEFT [UNC]; RC_MET |
| FL258 | V L P | T DURING | X_TREE_MID; X not a speaker; after C1 |
| FL259 | R G P | T DURING | X_BLACKREACH_ALONE; HLIOGoreBanter intro done |
| FL260 | C I | T DURING | X_LEAF_MID; X not a speaker; after R13 |
| FL261 | G V P | T | RX_SULK; after A3 |
| FL262 | I R | T | RX_MADEUP; B6 played |
| FL263 | S X | T | DG_END; SE4 played |
| FL264 | X P | T BEFORE | X_ESCORT10 |

### Inigo's quests (FL265-FL272)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL265 | R G | T DURING | BV_FITS; I not a speaker; HLIOGoreBanter intro done |
| FL266 | P X | T DURING | BV_HUNT; I not a speaker |
| FL267 | V K | T | I_BELIEVES [UNC]; KI_MET; after A2 |
| FL268 | G I | T | INIGO_BV; after C2 |
| FL269 | S I | T | INIGO_BV; DG_PROPHET; SE8 played |
| FL270 | C P | T DURING | BV_FITS; I not a speaker; after R13 |
| FL271 | K I | T | K_AKAVIRI; INIGO_BV; KI_MET |
| FL272 | X I | T DURING | BV_HUNT; X6 played |

### Lucien's quests (FL273-FL280)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL273 | K L | T BEFORE | LUC_LETTER; LK_MET |
| FL274 | I X | T DURING | LUC_HIDING; L not a speaker; X6 played |
| FL275 | R I | T | LUC_GONE; B6 played |
| FL276 | A L | T | LUC_ENGINE; ASHE_REVEAL; AS8 played |
| FL277 | S L | T | L_CLIVE; SE34 played |
| FL278 | L P | T | LUC_ENGINE |
| FL279 | C L | T | LUC_ENGINE; FA01RedcapSolstheimStartQ completed; after R11 |
| FL280 | K L | T | L_CLIVE; LK_MET |

### Redcap's quests (FL281-FL289)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL281 | K C | T BEFORE | RC_SAILING; after R1 |
| FL282 | V G | T DURING | MANOS_MID; C not a speaker; after A3 |
| FL283 | S C | T BEFORE | REDGOD_WAIT5 [UNC]; SE6 played |
| FL284 | I K | T DURING | PIG_TAKEN; C not a speaker; KI_MET |
| FL285 | C A | T | RC_FREED; ASHE_REVEAL; AS12 played |
| FL286 | C P | T | RC_STAY |
| FL287 | R C | T | RC_PARTY [UNC]; RC_MET |
| FL288 | G C | T | RC_WEREPIG; after R5 |
| FL289 | K C | T | RC_MANOS; after R1 |

### Serana's arcs (Serana Dialogue Add-On) (FL290-FL296)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL290 | R K | T DURING | S_CURE_AWAY; S not a speaker; after B1 |
| FL291 | X S | T | SER_CURED; SE4 played |
| FL292 | G S | T | S_DETERMINED; S_ACT; SE2 played |
| FL293 | G S | T | S_COVENANT; G_PAST; SE2 played |
| FL294 | L S | T | DG_PROPHET; SE34 played |
| FL295 | S K | T | S_TRUST; KMD_DONE; SE42 played |
| FL296 | R S | T | DG_GARDEN; SDA Remiel intro done |

### Ashe's arcs (Crystal Heart) (FL297-FL304)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL297 | I G | T | NOT_REVEAL; after C2 |
| FL298 | R V P | T DURING | ASHE_ALONE; A not a speaker; HLIOValBanter stage >= 10 |
| FL299 | R A | T | ASHE_NEVAS; AS39 played |
| FL300 | A I | T | ASHE_NEVAS; AS6 played |
| FL301 | S A | T | ASHE_MEDEUS; SE53 played |
| FL302 | L A P | T | ASHE_SUMMIT; PAARTH; PAARTH_ALIVE [UNC]; AS8 played |
| FL303 | K A | T | ASHE_EPI; A_LOVE; K_CRUSH; AS1 played |
| FL304 | A R | T | K_MAR; A_PAST; AS39 played |

### Everyone's quests at once (FL305-FL320)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL305 | R P | T | QDONE>=3; B6 played |
| FL306 | C P | T | GORE_BAIL; V_PIT; SERANA; RC_FREED |
| FL307 | L K P | T | QDONE>=4; LK_MET |
| FL308 | K P | T | QDONE>=5; K_TOG+ |
| FL309 | X G P | E CAMP | QDONE>=2; after X1 |
| FL310 | V R P | T | LUC_ENGINE; HLIOValBanter stage >= 10 |
| FL311 | A X | T | ASHE_SUMMIT; AS7 played |
| FL312 | G K P | E INN | QDONE>=5; VAL_FATHER; after A1 |
| FL313 | L I P | T | QDONE>=2; LI_RANK2 |
| FL314 | R K P | T | R_XBOW; K_COMP; after B1 |
| FL315 | I G | T | INIGO_BV; after C2 |
| FL316 | R S | T | QDONE>=5; SDA Remiel intro done |
| FL317 | X P | T | QDONE>=3 |
| FL318 | V P | T | VAL_FATHIS; QDONE>=3 |
| FL319 | A K P | T | KMD_DONE; ASHE_SUMMIT; AS1 played |
| FL320 | S G P | T | KMD_DONE; GORE_FATHER; SE2 played |

