# 54 FOLLOWER QUESTS CROSSTALK - trigger rows (prefix FL, 200 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\54 FOLLOWER QUESTS CROSSTALK.txt`. Luna speaks in 71 (35%) of talks.
Sources: TRIGGERS.md sections 2-5, `research\triggers\kaidan_block.md`, `others_block.md`, all ten bibles, and the quests' own journal/objective text read read-only through houseCARL on 2026-10-18 (KINV, KaiComp, KaiJail, KNPCAddy dialogue, KMDQuest, KMDNightmares, KMDRosalindScenePost, KaiHoneymoon, the Gore/Val/Remi/Xelzaz/Redcap/Lucien/Inigo quests).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana/Ashe `Free` rows in `20 DAWNGUARD.md` section 1 and Gore's `G_OK` in `22 VIGILANT GLENMORIL UNSLAAD.md`. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but player not in dialogue). Codes are in speaking order.

## 1. The one rule of this file: after, never during

- Every FL talk is a **timer talk (T)** (FL69 is the only event talk: SNOW) gated on a **"done"** condition for the beat it talks about. None can play while the beat is running, because (a) the done gate is only true after the beat ends and (b) each speaker's `Free` row and the Kaidan section 2b set-piece blocks are still applied on top.
- **Branch talks** carry the branch gate (Tarek spared/slain, Rolen alive/dead, Remi's Morvic kill vs talked-down, Paarthurnax kept vs Lucien came back, Serana romance on/off). All other talks are written branch-neutral (Sleeping Tree poisoned or burned, Wulf killed or died of wounds, Evesa's Kynesgrove job done by threat, talk or sword, Rolen's second meeting either way).
- **Kaidan's cult past** (Rosalind, Blooded Dawn, the Leyawiin farm, the tattoo's origin) appears only in FL18-FL23 and FL189, all gated `KMD_DONE`. No other FL talk says anything more than "dealings I'd rather forget".
- **Weddings/honeymoon** (FL24-FL26, FL63): talked about after, no ceremony content invented. Luna's honeymoon answer stays "somewhere with a view".
- **Luna and Kaidan's crush:** Luna never notices the crush in this file. FL16, FL17 (Adalyn's rejection is because of Luna) are gated `K_TOG+`.
- Recommend: at most **one FL talk per follower's quest per in-game day**, so a finished quest doesn't trigger a flood. Talks about the same beat may play in any order.

## 2. Gate codes (new in this file; everything else as TRIGGERS.md section 4)

Kaidan (FormIDs from kaidan_block.md):
- `K_FREED` = K01 002F9D:0Kaidan.esp stage 30 done (Kaidan's baseline anyway).
- `K_AKAVIRI` = KINV 0B3032:0Kaidan.esp completed (stage 50). Journal confirms: Northwind Summit cache, Viinturuth's burial mound, the letter from "Mei", "his mother was a Blade".
- `K_COMP` = KaiComp 162E4A:IF stage 150 done (both Wulf endings reach it: 25 slain / 26 "succumbed to his injuries").
- `K_JAIL` = KaiJail 31506F:IF stage 110 done (the "we've talked about what happened" stage; 100 = released). **[UNC: 110 is the post-talk stage per kaidan_block; use 100 + 24h if 110 is never set]**
- `K_ADDY` = KNPCAddy B8F6E2:IF stage 200 done (Kaidan has said goodbye to Adalyn; her letter says she went home and "would wait"). **[UNC: 200 = end per kaidan_block; confirm it is only set after the KaiAddyBreakup scene]**
- `KMD_DONE` = KMDQuest 1CD8FD:0Kaidan.esp stage 200 done (as 14 CREATION CLUB). FL22 adds KMDNightmares 8E7001:IF stage 50 done; FL23 adds KMDRosalindScenePost 8E1EEB:IF stage 80 done (Shadowgreen visit over).
- `K_MAR` as TRIGGERS.md. `K_HONEY` = KaiHoneymoon A5EA55:IF stage 150 done.
- `KI_MET`, `LK_MET`, `LI_RANK2`, `XL_MET`, `RX_OK`, `RC_MET` as `46 PAIR ARCS.md` section 2.

Gore (FormIDs GORE.esp):
- `G_WANTED` = HD1GoreEscort 1517F2 completed. `G_DH` = HD1GoreDH 3E8DC9 completed.
- `GORE_FATHER`, `GORE_BAIL` as TRIGGERS.md (GORE_FATHER already requires HD1GoreMurdererVar == 0, i.e. Pate's family spared - FL30 depends on that).
- `G_CROWS` = HD1GoreComeTheCrows 6EA61E completed. `G_STAND` = HD1GoreInterlude 7752FD completed. `G_NEST` = HD1Interlude2 89E472 completed (or stage > 20 and quest stopped) **[UNC end stage]**.
- `G_COAT` = HD1ArmorUpgrades 10A083 completed. `G_FLEET` = HD1GoreHorse1 2EADD8 completed. `G_FEAR` = HD1GoreFearAndLoathing AFF592 completed.
- `GORE_VIG` as `46 PAIR ARCS.md` (rescued from Coldharbour). `HLIOGoreReading` >= 1 = Remi's reading lessons began.

Val (FormIDs AX ValSerano.esp):
- `V_RESCUED` = Val001 2EE9A6 completed. `V_STAR` = Val002 33AAF4 completed.
- `VAL_FATHER`, `VAL_FATHIS` as TRIGGERS.md. Branches: Val003 3AA4A7 stage 70 done = Tarek spared (FL51); 71 done = Tarek slain (FL52).
- FL53: Val004 "I killed my brother" topic heard **[UNC: Val004 has no stage for it; fall back to VAL_FATHER and Val005 not started]**.
- `V_BOAT` = Val006 49DC32 stage 20 done. `V_GRAD` = ValCOLGrad 6682E2 completed.
- `V_PIT` = Val00B 49DC33 stage 200, 201 or 211 done. `V_MAR` as TRIGGERS.md. `V_RAVANI` = Val00D 49DC34 stage 90 or 200 done. `V_PANTS` = Val00E 22FFC1 completed.

Remi (FormIDs HLIORemi.esp):
- `R_SCRAP` = HLIOStartingQuest 0E4852 completed. `R_STEAM` = HLIOScrapUpgrades 08E59F stage 50 done.
- `R_XBOW` = HLIORPCrossbow 22DCD3 stage 40 done. `R_LOCK` = HLIORPLock 237EE7 stage 70 done and not the refusal ending **[UNC: refusal stage number; journal has a separate "I refused to help" entry]**. `R_LANTERN` = HLIORPLantern 8486EB stage 50 done. `R_FORK` = HLIOADQuest 62E259 stage 70 done. `R_PIE` = HLIOChaurusPieQuest 59B47F stage 80 done and not the "no time" ending **[UNC stage]**.
- `REMI_MORVIC` = HLIOMQ1 46FA55 stage 190 done (Morvic killed). FL83 = HLIOMQ1 230 done (player talked her out of taking it further) **[UNC: whether 230 and 190 can both be set; if so FL83 is still correct]**. FL84 = HLIOMQ1 220 done (workshop). FL86 = HLIOArkngchalManager 6A304E stage 60 done.
- `HLIOValBanter stage >= 10`, `HLIOGoreBanter intro done`, `SDA Remiel intro done`, `B6 played` = the existing pair meets.

Xelzaz (FormIDs BPUFXelzazFollower.esp):
- `X_STAYED` = BPUFXelzazEscortQuest 1BE431 stage 50 done (journal: "decided he wanted to travel with me for a while longer"). Never if 60/65/444/555/666/777 done.
- `X_TREE` = BPUFXelzazTheSleepingTree 79F4DA stage 54, 57 or 60 done (tree dead by poison or fire; 57 = he did it over the player's objection and came back). Never if 66 (player killed him).
- `X_ARMOR` = BPUFXelzazArmorQuest 40D29D stage 100 done (Evesa Omavel's armour).
- `X_LEAF` = BPUFXelzazLostHistLeaf E408E2 stage 15 done (note "A Most Prized Possesion" from Alarvyne, New Gnisis Cornerclub). **[UNC: the quest has no journal text; that 15 = leaf recovered is inferred]**
- `X_KHASH` = BPUFXelzazKhashNameQuest 497E93 stage 40 or 50 done (Khash = "Guardian").
- `X_KEEKO` = BPUFXelzazGuarQuest 7A4615 stage 17 done (guar named Keeko).
- `X_CRIMSON` = BPUFXelzazCrimsonNirnroot C6E975 stage 23 or 30 done (Nirnroot conversion in batches of ten).
- `X1`, `X4`, `X6`, `C3`, `R18` played = existing Xelzaz pair meets.

Inigo (Inigo.esp):
- `INIGO_BV` as TRIGGERS.md. `I_TRUTH` = InigoPlayerJourney 06CB85 stage where he admits "We never shared a past" **[UNC: stage not mapped]**.

Lucien (Lucien.esp):
- `LUC_ENGINE`, `LUC_ADMIT` as TRIGGERS.md. `L_CLIVE` = JRLucienGetHorseQuest 62424C stage 200 done.
- `L_PAARTH_BACK` = JRLucienPaarthurnax 1171E9 stage 15 done (rejoined after leaving). FL137 also needs `GAP3` = 3+ in-game days since stage 15 was set.
- FL138 = JRLucienPaarthurnax stage 1 done ("agreed not to kill") AND Paarthurnax alive AND MQPaarthurnax over **[UNC: stage numbering - the record lists stages as 1/2/3/4 notes, others_block uses 10/15]**.

Redcap (FA01RedcapFollower.esp):
- `RC_FREED` = FA01RedcapAniseQ 0DFB5A completed. FL143 = FA01RedcapSolstheimStartQ 0D0784 completed. FL144/FL145 = FA01RedcapSolstheimVillageQ 0D079B completed (Bigpig found).
- `RC_MANOS`, `RC_STAY`, `RC_REDGOD`, `RC_WEREPIG`, `RC_CHIEF` as TRIGGERS.md. `RC_SKAAL` = FA01RedcapSkaalQ 1D2F75 completed. FL160 = FA01BigpigIntroQ 0D58D2 completed.

Serana (SeranaDialogAddon.esp unless noted):
- `SE_F`, `SER_CURED`, `SER_VAMP`, `SERANA`, `DG_CAIRN`, `S_ROM_ON`, `S_ROMOFF`, `S_LOVE` as `20 DAWNGUARD.md` section 3 / `48 SERANA.md`.
- `S_CAIRN_VISIT` = SDA_SoulCairnPost completed (her return visit to Valerica) **[UNC: FormID and completion stage not pulled; serana.md names SDA_ValericaBranch* / SDA_SoulCairnPost]**.
- `S_TRUST` = SDA_SeranaRomance10Trust 46C3EC completed. FL172/173 = SDA_SeranaRomance11 C73A4A completed (Bannered Mare date). FL174/175 = SDA_SeranaRomance12 56E84B completed (Molag Bal nightmares). FL176 = SDA_SeranaRomance13 347A07 completed (beach date). FL179 = SDA_DrinkingBuddies 61AB00 has completed at least once **[UNC: it is repeatable; needs a controller flag]**.

Ashe (Ashe - Fire and Blood.esp), as ashe.md section 6:
- `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_NEVAS`, `ASHE_ROLEN1` (+ Rolen ref 75C0F7 GetDead for FL183/FL184), `ASHE_MEDEUS`, `ASHE_LOGS`, `ASHE_AMENDS` (06a C07BE9 / 06b C11E04 / 06cNEW 380306 completed, per row), `ASHE_SUMMIT`, `ASHE_LOVE`.
- FL196 = MM_AMQ_RNPC completed (Canas reconciliation) **[UNC FormID]**. FL200 = MM_AMQ_07Epilogue E5DA07 completed.
- `ASn` / `SEn` played = talks in `49 ASHE` / `48 SERANA` (their pair meets).

## 3. Per-talk table

### Kaidan's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL1 | G K P | T | K_FREED; after A1 |
| FL2 | R K | T | K_FREED; not K_AKAVIRI; after B1 |
| FL3 | L P | T | K_AKAVIRI |
| FL4 | X K P | T | K_AKAVIRI; after C3 |
| FL5 | V K | T | K_AKAVIRI; after A2 |
| FL6 | C K | T | K_AKAVIRI; after R1 |
| FL7 | G K | T | K_AKAVIRI; after A1 |
| FL8 | G K | T | K_COMP; after A1 |
| FL9 | I P | T | K_COMP; KI_MET |
| FL10 | V K | T | K_COMP; after A2 |
| FL11 | R G P | T | K_JAIL; GORE_BAIL; HLIOGoreBanter intro done |
| FL12 | V P | T | K_JAIL; after A2 |
| FL13 | X K | T | K_JAIL; after C3 |
| FL14 | R I | T | K_ADDY; B6 played |
| FL15 | G K P | T | K_ADDY; after A1 |
| FL16 | V K | T | K_ADDY; K_TOG+; after A2 |
| FL17 | P K | T | K_ADDY; K_TOG+ |
| FL18 | K I | T | KMD_DONE; KI_MET |
| FL19 | R K | T | KMD_DONE; after B1 |
| FL20 | X K | T | KMD_DONE; after C3 |
| FL21 | G V | T | KMD_DONE; after A3 |
| FL22 | C K | T | KMD_DONE; KMDNightmares 50 done; after R1 |
| FL23 | L K | T | KMD_DONE; KMDRosalindScenePost 80 done; LK_MET |
| FL24 | V G P | T | K_MAR; after A3 |
| FL25 | R P | T | K_HONEY |
| FL26 | X K | T | K_HONEY; after C3 |

### Gore's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL27 | V K P | T | G_WANTED; after A2 |
| FL28 | L G | T | G_DH; after L1 |
| FL29 | I G | T | GORE_FATHER; after C2 |
| FL30 | K P | T | GORE_FATHER; after A1 |
| FL31 | V G | T | GORE_FATHER; after A3 |
| FL32 | C G | T | GORE_BAIL; after R5 |
| FL33 | R V P | T | GORE_BAIL; HLIOValBanter stage >= 10 |
| FL34 | S G | T | G_CROWS; GORE_FATHER; SERANA |
| FL35 | V K | T | G_STAND; after A3 |
| FL36 | G K | T | G_NEST; after A1 |
| FL37 | L P | T | G_NEST; after L1 |
| FL38 | V G P | T | G_COAT; after A3 |
| FL39 | C G P | T | G_COAT; after R5 |
| FL40 | L G | T | G_FLEET; L_CLIVE; after L1 |
| FL41 | I G | T | G_FLEET; after C2 |
| FL42 | G P | T | G_FLEET |
| FL43 | X G | T | G_FEAR; after X1 |
| FL44 | K G | T | G_FEAR; after A1 |
| FL45 | K P | T | GORE_VIG; after A1 |
| FL46 | R G | T | GORE_VIG; HLIOGoreReading >= 1 |

### Val's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL47 | G V P | T | V_RESCUED; after A3 |
| FL48 | R V P | T | V_STAR; HLIOValBanter stage >= 10 |
| FL49 | K P | T | V_STAR; after A2 |
| FL50 | I V | T | VAL_FATHER; after I1 |
| FL51 | L V | T | VAL_FATHER; Val003 70 done; after C1 |
| FL52 | K V | T | VAL_FATHER; Val003 71 done; after A2 |
| FL53 | C V | T | VAL_FATHER; Val004 Fathis topic heard [UNC]; not VAL_FATHIS; after R8 |
| FL54 | X V | T | VAL_FATHIS; after X4 |
| FL55 | K V | T | VAL_FATHIS; after A2 |
| FL56 | R V | T | VAL_FATHIS; HLIOValBanter stage >= 10 |
| FL57 | G V P | T | V_BOAT; after A3 |
| FL58 | V P | T | V_BOAT |
| FL59 | L V P | T | V_GRAD; after C1 |
| FL60 | P V | T | V_GRAD |
| FL61 | K G | T | V_PIT; after A3 |
| FL62 | I V | T | V_PIT; after I1 |
| FL63 | R G | T | V_MAR; HLIOGoreBanter intro done |
| FL64 | X V | T | V_RAVANI; after X4 |
| FL65 | L V | T | V_PANTS; after C1 |
| FL66 | R I | T | V_STAR; B6 played |

### Remi's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL67 | K R | T | R_SCRAP; after B1 |
| FL68 | L R | T | R_STEAM; after B10 |
| FL69 | X R | E SNOW | R_STEAM; RX_OK |
| FL70 | K R | T | R_XBOW; after B1 |
| FL71 | I P | T | R_XBOW; B6 played |
| FL72 | V R P | T | R_LOCK; HLIOValBanter stage >= 10 |
| FL73 | R A | T | R_LOCK; ASHE_HIRED |
| FL74 | L R P | T | R_LANTERN; after B10 |
| FL75 | S R | T | R_LANTERN; SER_VAMP; SDA Remiel intro done |
| FL76 | G R P | T | R_FORK; HLIOGoreBanter intro done |
| FL77 | A R | T | R_FORK; ASHE_REVEAL |
| FL78 | X R | T | R_PIE; RX_OK |
| FL79 | C R P | T | R_PIE; RC_MET |
| FL80 | I R | T | REMI_MORVIC; B6 played |
| FL81 | L R | T | REMI_MORVIC; after B10 |
| FL82 | X R | T | REMI_MORVIC; RX_OK |
| FL83 | G R | T | HLIOMQ1 230 done [UNC: branch meaning]; HLIOGoreBanter intro done |
| FL84 | C R | T | HLIOMQ1 220 done; RC_MET |
| FL85 | S R | T | REMI_MORVIC; SDA Remiel intro done |
| FL86 | L P | T | HLIOArkngchalManager 60 done; after B10 |

### Xelzaz's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL87 | G X P | T | X_STAYED; after X1 |
| FL88 | R P | T | X_STAYED; RX_OK |
| FL89 | K X | T | X_STAYED; after C3 |
| FL90 | I X | T | X_TREE; X6 played |
| FL91 | V X | T | X_TREE; after X4 |
| FL92 | P X | T | X_TREE |
| FL93 | R X | T | X_TREE; RX_OK |
| FL94 | V X | T | X_ARMOR; after X4 |
| FL95 | G P | T | X_ARMOR; after X1 |
| FL96 | L X | T | X_ARMOR; XL_MET |
| FL97 | K X | T | X_LEAF; after C3 |
| FL98 | R X | T | X_LEAF; RX_OK |
| FL99 | I P | T | X_LEAF; X6 played |
| FL100 | L X P | T | X_KHASH; XL_MET |
| FL101 | G X | T | X_KHASH; GORE_FATHER; after X1 |
| FL102 | C X | T | X_KHASH; R18 played |
| FL103 | L X P | T | X_KEEKO; XL_MET |
| FL104 | S X | T | X_KEEKO; SERANA |
| FL105 | K X | T | X_CRIMSON; after C3 |
| FL106 | P X | T | X_CRIMSON |

### Inigo's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL107 | K I | T | INIGO_BV; KI_MET |
| FL108 | L I P | T | INIGO_BV; LI_RANK2 |
| FL109 | R P | T | INIGO_BV; B6 played |
| FL110 | G I P | T | INIGO_BV; after C2 |
| FL111 | K P | T | INIGO_BV; after A1 |
| FL112 | V I P | T | INIGO_BV; after I1 |
| FL113 | S P | T | INIGO_BV; SERANA |
| FL114 | I P | T | INIGO_BV |
| FL115 | G I | T | I_TRUTH [UNC: InigoPlayerJourney stage for the confession]; after C2 |
| FL116 | K I | T | I_TRUTH [UNC]; KI_MET |
| FL117 | R I | T | INIGO_BV; B6 played |
| FL118 | C P | T | INIGO_BV; after R13 |
| FL119 | X I | T | INIGO_BV; X6 played |
| FL120 | V I | T | INIGO_BV; after I1 |
| FL121 | A I | T | INIGO_BV; ASHE_REVEAL |
| FL122 | L I | T | INIGO_BV; LI_RANK2 |

### Lucien's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL123 | G L P | T | LUC_ENGINE; after L1 |
| FL124 | K L | T | LUC_ENGINE; LK_MET |
| FL125 | R L | T | LUC_ENGINE; after B10 |
| FL126 | X L | T | LUC_ENGINE; XL_MET |
| FL127 | P L | T | LUC_ENGINE |
| FL128 | C L | T | LUC_ENGINE; after R11 |
| FL129 | V L P | T | LUC_ADMIT; after C1 |
| FL130 | I L | T | LUC_ADMIT; LI_RANK2 |
| FL131 | K P | T | LUC_ADMIT; LK_MET |
| FL132 | R L | T | LUC_ADMIT; after B10 |
| FL133 | X L | T | LUC_ADMIT; XL_MET |
| FL134 | K L | T | L_PAARTH_BACK; LK_MET |
| FL135 | I L | T | L_PAARTH_BACK; LI_RANK2 |
| FL136 | G P | T | L_PAARTH_BACK; after L1 |
| FL137 | L P | T | L_PAARTH_BACK; GAP3 since he rejoined |
| FL138 | V L | T | Paarthurnax alive; JRLucienPaarthurnax stage 1 done [UNC]; after C1 |
| FL139 | S L | T | LUC_ENGINE; SERANA |
| FL140 | K L | T | LUC_ADMIT; LK_MET |

### Redcap's quests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL141 | K C | T | RC_FREED; after R1 |
| FL142 | L P | T | RC_FREED; after R11 |
| FL143 | G C | T | FA01RedcapSolstheimStartQ completed; after R5 |
| FL144 | R C | T | FA01RedcapSolstheimVillageQ completed; RC_MET |
| FL145 | V C | T | FA01RedcapSolstheimVillageQ completed; after R8 |
| FL146 | X C | T | RC_MANOS; R18 played |
| FL147 | K C | T | RC_MANOS; after R1 |
| FL148 | I C | T | RC_STAY; after R13 |
| FL149 | G C | T | RC_STAY; after R5 |
| FL150 | V C P | T | RC_REDGOD; after R9 |
| FL151 | S C | T | RC_REDGOD; SERANA |
| FL152 | R C | T | RC_REDGOD; RC_MET |
| FL153 | P C | T | RC_REDGOD |
| FL154 | K C | T | RC_WEREPIG; after R1 |
| FL155 | L C P | T | RC_WEREPIG; after R11 |
| FL156 | I C | T | RC_SKAAL; after R13 |
| FL157 | K G P | T | RC_SKAAL; after A1 |
| FL158 | C V | T | RC_CHIEF; after R9 |
| FL159 | P C | T | RC_CHIEF |
| FL160 | A C | T | FA01BigpigIntroQ completed; ASHE_HIRED; AS5 played |

### Serana's arcs (Serana Dialogue Add-On)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL161 | K S | T | SER_CURED; SE_F; SE42 played |
| FL162 | G S P | T | SER_CURED; SE2 played |
| FL163 | X P | T | SER_CURED; SE_F |
| FL164 | R S | T | SER_CURED; SDA Remiel intro done |
| FL165 | I S | T | SER_CURED; SE8 played |
| FL166 | C S | T | SER_CURED; SE6 played |
| FL167 | L S | T | S_CAIRN_VISIT [UNC: SDA_SoulCairnPost FormID/stage]; SE_F; LK_MET |
| FL168 | K S | T | S_CAIRN_VISIT [UNC]; K_AKAVIRI; SE10 played |
| FL169 | S P | T | S_CAIRN_VISIT [UNC]; SE_F |
| FL170 | V S | T | S_TRUST [SDA_SeranaRomance10Trust completed]; S_ROM_ON; SE3 played |
| FL171 | G P | T | S_TRUST [UNC]; SE2 played |
| FL172 | R S | T | SDA_SeranaRomance11 completed; S_ROM_ON; SDA Remiel intro done |
| FL173 | K S | T | SDA_SeranaRomance11 completed; S_ROM_ON; K_ANY; SE57 or SE58 played |
| FL174 | X S | T | SDA_SeranaRomance12 completed; S_ROM_ON; SE4 played |
| FL175 | G S | T | SDA_SeranaRomance12 completed; G_FEAR; SE39 played |
| FL176 | V S | T | SDA_SeranaRomance13 completed; S_ROM_ON; SE15 played |
| FL177 | I S | T | S_ROMOFF; DG_CAIRN; SE8 played |
| FL178 | L S | T | S_LOVE; SE34 played |
| FL179 | C S | T | SDA_DrinkingBuddies completed once [UNC]; SE6 played |
| FL180 | R I | T | SER_CURED; B6 played |

### Ashe's arcs (Crystal Heart)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| FL181 | G P | T | ASHE_Q1; AS13 played |
| FL182 | K A | T | ASHE_NEVAS; AS1 played |
| FL183 | L A | T | ASHE_ROLEN1; Rolen alive; AS8 played |
| FL184 | X A | T | ASHE_ROLEN1; Rolen dead; AS7 played |
| FL185 | G A | T | ASHE_MEDEUS; GORE_FATHER; AS13 played |
| FL186 | I P | T | ASHE_MEDEUS; AS6 played |
| FL187 | V P | T | ASHE_LOGS; AS19 played |
| FL188 | A K | T | ASHE_LOGS; AS14 played |
| FL189 | A K | T | ASHE_AMENDS 06a; KMD_DONE; AS21 played |
| FL190 | L A P | T | ASHE_AMENDS 06a; AS8 played |
| FL191 | V A | T | ASHE_AMENDS 06b; AS19 played |
| FL192 | C A | T | ASHE_AMENDS 06b; AS12 played |
| FL193 | X A | T | ASHE_AMENDS 06c; AS7 played |
| FL194 | G P | T | ASHE_AMENDS 06c; AS2 played |
| FL195 | S A P | T | ASHE_SUMMIT; SE53 played |
| FL196 | R A | T | MM_AMQ_RNPC completed [UNC]; AS39 played |
| FL197 | P K | T | ASHE_REVEAL; after AS10 or AS14 |
| FL198 | A P | T | ASHE_SUMMIT; ASHE_REVEAL |
| FL199 | R S | T | ASHE_LOVE; SDA Remiel intro done; SE18 played |
| FL200 | I A | T | MM_AMQ_07Epilogue completed; AS6 played |
