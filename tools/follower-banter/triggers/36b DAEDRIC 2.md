# 36b DAEDRIC 2 - trigger rows (DA101-DA180)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\36b DAEDRIC 2.txt`
Sources: `triggers\36 DAEDRIC QUESTS.md` (quest records, stages, every `DA_*` code, `GORE_NOT_RESCUED`, `WIELD:<item>`, `LOC:*` places, silence windows), `research\triggers\vanilla_gates.md`, `kaidan_block.md`, `others_block.md`. Reused codes from other sheets: `KMD_DONE` / `NOT_KMD` (14 CREATION CLUB.md), `SERANA`, `SER_VAMP`, `SER_CURED`, `ASHE_HIRED`, `ASHE_REVEAL` (20 DAWNGUARD.md), `MG_JOIN` (TRIGGERS.md), `RC_WEREPIG`, `RC_REDGOD` (TRIGGERS.md), `VAL_FATHIS`.
Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check).
Shorthand: `Done(Q,s)` = GetStageDone Q s == 1. `Comp(Q)` = GetQuestCompleted. **[UNC]** = not verified, check at build.

## Standing rules for this file
- Every part-1 silence window applies (36 DAEDRIC QUESTS.md section 3), including: **no talk with Kaidan in it while `In(ShrineofMehrunesDagon 0240E6)`**, and Gore in no DA talk while `HD1GoreFearAndLoathing` runs.
- Gore never mentions the House of Horrors; his Molag Bal jokes (DA129) need `GORE_NOT_RESCUED` to be **false** (his Coldharbour arc is done).
- Kaidan's Dagon rows: `NOT_KMD` rows (DA118, DA119, DA172) never play after his quest is done; `KMD_DONE` rows (DA120, DA156, DA167, DA169) never before.
- Every **S** row also needs `SERANA`, "S following" and Serana's Free() row; every **A** row also needs `ASHE_HIRED`, her Free() row and her silence list (49 ASHE.md). Pair "first meeting" talks from 48 SERANA / 49 ASHE must have played ("S-x met" / "A-x met").
- Nobody names an ending the talk does not need: each artifact row is gated on the ending that gives that artifact, and the Oghma row (DA112) never says which path Luna took.

## New gate codes for this file
**Artifacts held / used** (artifact FormIDs from Skyrim.esm / Dawnguard.esm, pull at build **[UNC all]**)
- `HAS:<item>` = player `GetItemCount <item> >= 1`. `WEAR:<item>` = player `GetEquipped <item> == 1` (or WornHasKeyword for the armour pieces). `WIELD:<item>` as in part 1 (equipped during the fight just ended).
- Items: `AzurasStar`, `BlackStar`, `EbonyMail`, `Masque` (Masque of Clavicus Vile), `SaviorsHide`, `RingOfHircine`, `Volendrung`, `Razor` (Mehrunes' Razor), `EbonyBlade`, `Dawnbreaker`, `Mace` (Mace of Molag Bal), `NamiraRing`, `Spellbreaker`, `SanguineRose`, `Wabbajack`, `Skull` (Skull of Corruption).
- `MACE_HELD` = HAS:Mace. This is the "Vigilant took the Mace" guard: if the Vigilant story removes the Mace, every Mace row stops by itself.
- `ARTIFACTS>=n` = the controller counts HAS: over the 16 items above (Star and Black Star count once).
- `DA_COUNT>=n` = number of DA01..DA16 (plus DA06 via `CT_END`) completed (controller counts Comp).
- `DA_REFUSALS>=2` = at least two of: `DA_RAZOR_REFUSED`, `DA_BLADE_GONE`, `DA_ALTAR_DOWN`, `DA_NAMIRA_NO`, `Done(DA13,102)`, `DA_SINDING_SPARED`, `DA_ERANDUR`.
- `WEREWOLF_NOW` = `PlayerIsWerewolf (0ED06C:Skyrim.esm) == 1`.

**Artifact moments** (events the controller must detect **[UNC all; build the detection or drop the row]**)
- `E STAR_RECHARGE` = player recharges a weapon and Azura's Star / the Black Star loses its soul in the same tick (OnItemRemoved of the soul from the Star, or Star charge drops from filled to empty while the weapon's charge rises).
- `E SNEAK_END` = first tick after the player stops sneaking, having sneaked >= 20 seconds. This is an exception to the global sneak block (the talk plays after the sneak, never during it).
- `E NAMIRA_FEED` = the Ring of Namira's "feed on a corpse" activation fires (its MGEF applied to the player).
- `E ROSE_SUMMON` = AFTERFIGHT and the Sanguine Rose's summon effect was active on the player during the fight.
- `E WABBA:<result>` = AFTERFIGHT, WIELD:Wabbajack, and the last Wabbajack hit had that result: `gore` (the Wabbajack effect landed on Gore), `gold` (target turned into a gold pile), `heal` (target healed), `rabbit` (target turned into a rabbit). Wabbajack results are scripted (`WabbajackScript`); read the chosen branch **[UNC]**. Fallback: drop the row.
- `E RAZOR_KILL` = AFTERFIGHT, WIELD:Razor, and a target died from the Razor's instant-kill effect.
- `E SPELL_BOUNCE` = AFTERFIGHT, WEAR:Spellbreaker, and a Xelzaz spell hit the Spellbreaker ward **[UNC: very hard to detect; fallback AFTERFIGHT + WEAR:Spellbreaker + Xelzaz cast a Destruction spell this fight]**.
- `E DA_DONE` = first tick after any DA01..DA16 quest completes.

**Places and encounters** **[UNC all LCTN / quest FormIDs]**
- `LOC:Meridia` (Statue to Meridia exterior, Mount Kilkreath), `LOC:Sacellum` (Sacellum of Boethiah), `LOC:ShrinePeryite`, `LOC:Dagon` (`ShrineofMehrunesDagon 0240E6`), `LOC:BloatedGrotto` (Bloated Man's Grotto), `LOC:HircineAltar` (any minor Hircine altar inside a cave or ruin; list to build), `LOC:Store` (LocTypeStore 01CB86 inside a LocTypeCity).
- `ENC:Vaermina` = the Vaermina devotee world encounter has spoken to the player. `ENC:Hircine` = a Hircine hunter world encounter has spoken to the player. `ENC:Vigilant` = a Vigilant of Stendarr road encounter has spoken to the player.
- `AFTERFIGHT:afflicted` = last target in Peryite's Afflicted faction. `AFTERFIGHT:cultist` as DA94. `AFTERFIGHT:mage` = last target is a mage-class NPC (warlock / conjurer / necromancer factions). `AFTERFIGHT:troll`, `:draugr`, `:vampire`, `:dremora`, `:bandit` by race/faction.
- `VR_PARTNERS` = Val and Remi are business partners: `HLIOValRemiFriendshipTracker (HLIORemi.esp) >= 2` **[UNC which value marks the partnership]**.

## Table

### Part 1 - Azura's Star, full and empty
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA101 | G X | E STAR_RECHARGE | DA_STAR_PURE or DA_STAR_BLACK; after X1 |
| DA102 | I P | E STAR_RECHARGE | DA_STAR_PURE |
| DA103 | S P | E STAR_RECHARGE | DA_STAR_BLACK |
| DA104 | L V | T | DA_STAR_PURE or DA_STAR_BLACK; after C1 |

### Part 2 - The Ebony Mail
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA105 | K P | E SNEAK_END | DA_BOE; WEAR:EbonyMail |
| DA106 | R G | E AFTERFIGHT | DA_BOE; WEAR:EbonyMail; after B15 or Remi-Gore meet |
| DA107 | L V | T | DA_BOE; after C1 |

### Part 3 - The Masque of Clavicus Vile
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA108 | V P | E LOC:Store | DA_MASQUE; WEAR:Masque |
| DA109 | L P | E LOC:Arcanaeum (35 COLLEGE OF WINTERHOLD.md) | DA_MASQUE; WEAR:Masque; MG_JOIN |
| DA110 | C G | T | DA_MASQUE; WEAR:Masque; after R5 |

### Part 4 - Hermaeus Mora: the book that left
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA111 | L R | T | DA_OGHMA; at least 2 game days after DA04 100 **[UNC day counter]**; after B10 |
| DA112 | V P | T | DA_OGHMA; VAL_FATHIS; at least 2 game days after DA04 100 |

### Part 5 - Hircine: the pelt and the ring
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA113 | C I | T | DA_SINDING_KILLED; WEAR:SaviorsHide; after R13 |
| DA114 | K G | T | DA_SINDING_SPARED; WEAR:RingOfHircine; after A1 |
| DA115 | I P | T | DA_SINDING_SPARED; WEAR:RingOfHircine; WEREWOLF_NOW |

### Part 6 - Malacath: Volendrung
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA116 | K A | E AFTERFIGHT | Done(DA06,200); WIELD:Volendrung; ASHE_REVEAL; A-K met |
| DA117 | C G | T | Done(DA06,200); HAS:Volendrung; after DA39; after R5 |

### Part 7 - Mehrunes' Razor
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA118 | A P | T | DA_RAZOR; HAS:Razor; NOT_KMD; ASHE_REVEAL; after DA9 |
| DA119 | K P | E AFTERFIGHT | DA_RAZOR; WIELD:Razor; NOT_KMD; not In(0240E6) |
| DA120 | K G | T | DA_RAZOR; HAS:Razor; KMD_DONE; after DA48 |
| DA121 | I X | T | DA_RAZOR; after X6 |
| DA122 | L P | T | DA_RAZOR_REFUSED; at least 3 game days after DA07 150 **[UNC day counter]** |

### Part 8 - Mephala: the Ebony Blade
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA123 | I L | E AFTERFIGHT:bandit | DA_BLADE_KEPT; WIELD:EbonyBlade; Lucien-Inigo intro done (JRLucienInigoRank >= 2) |
| DA124 | V K | T | DA_BLADE_KEPT; WEAR:EbonyBlade; K_TOG+; after DA51 |

### Part 9 - Meridia: Dawnbreaker
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA125 | S R | T | DA_DAWN; HAS:Dawnbreaker; SER_VAMP; S-R met |
| DA126 | S P | T | DA_DAWN; HAS:Dawnbreaker; SER_CURED |
| DA127 | G L | E AFTERFIGHT:draugr | DA_DAWN; WIELD:Dawnbreaker; after L1 |

### Part 10 - Molag Bal: the Mace
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA128 | S P | T | DA_MACE; MACE_HELD |
| DA129 | G V | T | DA_MACE; MACE_HELD; GORE_NOT_RESCUED false (HD1MemoriesRestored == 1); after A3 |
| DA130 | R X | T | DA_MACE; MACE_HELD; Remi and Xelzaz not fallen out (`BPUFXelzazRemielFallenOut != 1`) |

### Part 11 - Namira's Ring
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA131 | X P | E INN or CAMP | DA_NAMIRA_ATE; WEAR:NamiraRing |
| DA132 | R I | E NAMIRA_FEED | DA_NAMIRA_ATE; after B6 |
| DA133 | S K | E NAMIRA_FEED | DA_NAMIRA_ATE; S-K met (priority below DA132 if both speakers sets are present; one per feed) |
| DA134 | C G | T | DA_NAMIRA_ATE; WEAR:NamiraRing; after DA69; after R5 |

### Part 12 - Peryite: Spellbreaker
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA135 | L P | E AFTERFIGHT:mage | DA_PERYITE; WEAR:Spellbreaker |
| DA136 | I A | T | DA_PERYITE; WEAR:Spellbreaker; ASHE_REVEAL; A-I met |

### Part 13 - Sanguine: the Rose
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA137 | C P | T | DA14; HAS:SanguineRose; RC_REDGOD |
| DA138 | L K | E ROSE_SUMMON | DA14; MG_JOIN; after MG22 (the atronach wink); Lucien-Kaidan intro done |
| DA139 | G V | E ROSE_SUMMON | DA14; after A3 |

### Part 14 - Sheogorath: the Wabbajack, continued
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA140 | G R P | E WABBA:gore | DA_WABBA; after B15 or Remi-Gore meet |
| DA141 | V X | E WABBA:gold | DA_WABBA; after X4 |
| DA142 | K A | E WABBA:heal, last target a troll | DA_WABBA; ASHE_REVEAL; A-K met |
| DA143 | L P | E CAMP + NIGHT | DA_WABBA; HAS:Wabbajack |

### Part 15 - Vaermina: the Skull of Corruption
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA144 | I L | E CAMP + NIGHT | DA_SKULL; HAS:Skull; Lucien-Inigo intro done |
| DA145 | K P | E AFTERFIGHT | DA_SKULL; WIELD:Skull |

### Part 16 - Nocturnal
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA146 | C I | T | Comp(TG09 021555); after DA73 |

### Part 17 - The bag of artifacts
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA147 | G P | T | ARTIFACTS>=5 including HAS:Volendrung, HAS:Masque, HAS:Spellbreaker, HAS:Wabbajack (all named); after DA140 |
| DA148 | L X | E CAMP + NIGHT | ARTIFACTS>=4 including HAS:Wabbajack and MACE_HELD (both named); Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| DA149 | K P | E CAMP | ARTIFACTS>=3; K_TOG+; after DA60 |
| DA150 | V R | T | ARTIFACTS>=3 including HAS:Masque; VR_PARTNERS |
| DA151 | A P | T | DA_REFUSALS>=2; ASHE_REVEAL |
| DA152 | K X | T | DA_COUNT>=6; after DA2 |

### Part 18 - Shrines in the wild
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA153 | R G P | E LOC:Meridia | DA_DAWN; SERANA (named); after B15 or Remi-Gore meet |
| DA154 | V I | E LOC:Sacellum | DA_BOE; DA02 not running; after I1 |
| DA155 | I X | E LOC:ShrinePeryite | DA_PERYITE; after X6 |
| DA156 | G L | E LOC:Dagon | Comp(DA07); KMD_DONE; Kaidan not following (he is named, not present); after L1 |
| DA157 | S R | E LOC:HircineAltar | DA_ANY; S-R met |
| DA158 | K X | E LOC:BloatedGrotto | Comp(DA05); after C3 |

### Part 19 - Worshippers on the road
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA159 | S I | E AFTERFIGHT:afflicted | DA_ANY or Done(DA13,10); S-I met |
| DA160 | L G | E ENC:Vaermina | after L1 |
| DA161 | K C | E ENC:Hircine | RC_WEREPIG; after R1 |
| DA162 | V P | E in a LocTypeTown or LocTypeCity exterior, hour 8..18 | DA_COUNT>=3 |
| DA163 | R X | E AFTERFIGHT:cultist | DA_ANY; Remi and Xelzaz not fallen out |
| DA164 | L K | E ENC:Vigilant | ARTIFACTS>=3 including HAS:Wabbajack (named); Lucien-Kaidan intro done |

### Part 20 - The Princes, after
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA165 | G P | T | DA14 |
| DA166 | L P | T | DA_WABBA; after DA1 |
| DA167 | V K | T | DA_TWO; KMD_DONE; after A2 |
| DA168 | C S | T | RC_REDGOD; S-C met |
| DA169 | A K | T | KMD_DONE; after DA9; A-K met |
| DA170 | R P | T | DA_COUNT>=5 |
| DA171 | G X | T | DA_TWO; after X1 |
| DA172 | I K | E DA_DONE | DA_ANY; NOT_KMD; after DA2; KaiandInigo stage >= 10 |

### Part 21 - Short barks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| DA173 | G C | E ROSE_SUMMON | DA14; after R5 |
| DA174 | I V | E RAZOR_KILL | DA_RAZOR; after I1 |
| DA175 | X L | E SPELL_BOUNCE | DA_PERYITE; Xelzaz-Lucien intro done |
| DA176 | R V | E AFTERFIGHT | Done(DA06,200); WIELD:Volendrung; after Val-Remi intro (HLIOValBanter stage 10) |
| DA177 | S G | E AFTERFIGHT, a target died while hit by the Mace | DA_MACE; WIELD:Mace; S-G met |
| DA178 | I C | E WABBA:rabbit | DA_WABBA; after R13 |
| DA179 | L K | E AFTERFIGHT:vampire | DA_DAWN; WIELD:Dawnbreaker; Lucien-Kaidan intro done |
| DA180 | A G | E AFTERFIGHT:dremora | ASHE_REVEAL; A-G met |

## Open items for build
- The artifact-moment events (STAR_RECHARGE, NAMIRA_FEED, ROSE_SUMMON, WABBA:<result>, RAZOR_KILL, SPELL_BOUNCE) all need controller detection. If one cannot be built, drop that row rather than firing it on a plain AFTERFIGHT: the talks describe the exact thing that happened.
- DA103 says the last soul was "a necromancer who raised his own sister"; it reads as one specific soul. If that feels wrong on a random recharge, gate it to the first STAR_RECHARGE after AFTERFIGHT:mage.
- DA105 is the only row in the file that rides on sneaking; it plays after the sneak ends, never during.
- DA132 and DA133 share NAMIRA_FEED; play only one per feed.
- DA156 is the only row at the Shrine of Mehrunes Dagon and needs Kaidan absent, matching the part-1 silence.
- DA129 (Gore swinging the Mace) needs Gore past his Coldharbour arc; DA177 (Gore offering Serana a walk) does not mention Molag Bal and has no Gore arc gate.
- Artifact, LCTN, encounter and faction FormIDs marked [UNC].
- No script change was needed: every talk can be gated.
