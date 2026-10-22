# 44 IN THE FIGHT - trigger rows (prefix CB, 150 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\44 IN THE FIGHT.txt`.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`, except the player-in-combat rule for COMBAT rows) and section 3 (`Free`, except `GetCombatState()==0` for COMBAT rows). Serana and Ashe Free() rows are in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check).
Every row also needs its pair's meets talk already played (TRIGGERS.md section 4, Chains). `after <ID>` names it where the pair has one in our files; `<x> intro done` names the follower mods' own intro.

## Two lanes

- **COMBAT rows (CB1-CB95, CB97): COMBAT (scene must not end on combat).** In-fight barks. Start them from the controller while the player IS in combat (first 3-20 s of a fight, or on the named moment). Their scenes must NOT carry the CombatEnd flag (keep DeathEnd and DialogueEnd), must bypass the player-in-combat quiet rule and the speakers' `GetCombatState()==0` test, and must keep every other quiet rule. One bark per fight. No 300 s cooldown is set by a bark, and a bark does not reset the 5-minute timer. [UNC: same lane as DR126 / WS56 in 10 and 13]
- **AFTERFIGHT rows (CB96, CB98-CB150).** Normal post-combat event: controller sees player combat end, waits 8 s (TRIGGERS.md section 1), enemy type = last combat target.

## Enemy codes (current combat target for COMBAT, last target for AFTERFIGHT)

All `:Skyrim.esm` unless noted. [UNC] = FormID to confirm at build.
- `bandit` BanditFaction (01BCC0) [UNC]. `draugr` DraugrRace (00D53A) or ActorTypeUndead + LocTypeDraugrCrypt [UNC]. `falmer` FalmerRace (0131F4) [UNC]. `forsworn` ForswornFaction (043599) [UNC]. `thalmor` ThalmorFaction (039F26) [UNC]; TRIGGERS.md section 4.
- `vampire` target HasKeyword Vampire (0A82BB). `necromancer` target in a necromancer/warlock faction or casting reanimate (as `48 SERANA.md`). `spriggan` SprigganRace (013204) / SprigganMatronRace / SprigganEarthMotherRace [UNC]. `troll` TrollRace / TrollFrostRace (+ DLC1 armoured) [UNC]. `giant` GiantRace (0131F9) [UNC]. `mammoth` MammothRace [UNC]. `bear` BearBrownRace / BearBlackRace / BearSnowRace [UNC]. `sabrecat` SabreCatRace / SabreCatSnowyRace [UNC]. `wolf` WolfRace [UNC]. `skeever` SkeeverRace / SkeeverWhiteRace [UNC]. `spider` FrostbiteSpiderRace family (as `49 ASHE.md`). `dragon` ActorTypeDragon / DragonRace (as `30 MAIN QUEST DEEP.md`). `dwemer` DwarvenAutomaton race keyword ActorTypeDwarven (01397A) [UNC]. `hagraven` HagravenRace (as TRIGGERS.md D8). `dremora` DremoraRace (0131F0) [UNC]. `atronach` AtronachFlame/Frost/Storm races [UNC]; CB50/CB51 need AtronachStormRace.
- `any` = any hostile.

## Moment conditions used in COMBAT rows

- `<x> below half health` = that follower's Health percent < 0.5 during this fight (controller polls GetActorValuePercentage on its combat tick). [UNC: needs a 1-2 s combat poll]
- `friendly hit: A on B` = B was hit by A this fight (OnHit on the follower alias, aggressor = A). [UNC]
- `player heals Gore` = Gore's health rises while the player casts a Restoration spell on him. [UNC]
- `player casting a master or expert spell` = player's equipped/cast spell is Expert or Master level (MagicSkillLevel >= 75 perk-keyword on the spell, or a short list of FormIDs: Fire Storm, Blizzard, Lightning Storm, Chain Lightning, Incinerate, Icy Spear, Thunderbolt, Mayhem, Frenzy). [UNC]
- `player holding a ward` = player has a ward magic effect active. [UNC]
- `Lucien summons` = Lucien has a commanded summon active. [UNC]

## Gate codes

From TRIGGERS.md section 4: `SHOUT1`, `DB`, `K_CRUSH`, `K_TOG+`, `K_ANY`, `G_FLIRT`, `G_TOG+`, `V_FLIRT`, `V_TOG+`, `BRYNJAR`, `NIGHT`. From `20 DAWNGUARD.md` section 3: `SER` (Serana following), `SER_VAMP`, `S_COMP`, `A_ANY`, `ASHE_REVEAL`, `G_ANY`, `V_ANY`. `ASHE` = Ashe following + `ASHE_HIRED` (`49 ASHE.md`).

Part 3 (the kill-count chain) plays in order: each row needs the one before it. The `after CBxx` gates do this.

## Table

### PART 1 - FIGHT STARTS, BY ENEMY  (51 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB1 | K V P | E COMBAT:bandit - COMBAT (scene must not end on combat) | after A2 |
| CB2 | C G | E COMBAT:bandit - COMBAT (scene must not end on combat) | after R5 |
| CB3 | R P | E COMBAT:bandit - COMBAT (scene must not end on combat) | — |
| CB4 | I K | E COMBAT:bandit - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |
| CB5 | G K P | E COMBAT:draugr - COMBAT (scene must not end on combat) | SHOUT1; after A1 |
| CB6 | I C | E COMBAT:draugr - COMBAT (scene must not end on combat) | after R13 |
| CB7 | L X | E COMBAT:draugr - COMBAT (scene must not end on combat) | Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| CB8 | S R | E COMBAT:draugr - COMBAT (scene must not end on combat) | SER |
| CB9 | L K | E COMBAT:falmer - COMBAT (scene must not end on combat) | Lucien-Kaidan intro done (JRLucienFollowerKaidanScene1) |
| CB10 | V R P | E COMBAT:falmer - COMBAT (scene must not end on combat) | Val-Remi intro done (HLIOValBanter 10) |
| CB11 | C I | E COMBAT:falmer - COMBAT (scene must not end on combat) | after R13 |
| CB12 | G K | E COMBAT:forsworn - COMBAT (scene must not end on combat) | after A1 |
| CB13 | C L | E COMBAT:forsworn - COMBAT (scene must not end on combat) | after R11 |
| CB14 | S P | E COMBAT:forsworn - COMBAT (scene must not end on combat) | SER |
| CB15 | V G | E COMBAT:thalmor - COMBAT (scene must not end on combat) | after A3 |
| CB16 | L I | E COMBAT:thalmor - COMBAT (scene must not end on combat) | Lucien-Inigo intro done (JRLucienInigo) |
| CB17 | P K | E COMBAT:thalmor - COMBAT (scene must not end on combat) | — |
| CB18 | X S | E COMBAT:vampire - COMBAT (scene must not end on combat) | SER; SER_VAMP; Xelzaz following |
| CB19 | I V | E COMBAT:vampire - COMBAT (scene must not end on combat) | after I1 |
| CB20 | R A | E COMBAT:vampire - COMBAT (scene must not end on combat) | ASHE_REVEAL; Remi following |
| CB21 | L R | E COMBAT:necromancer - COMBAT (scene must not end on combat) | after B10 |
| CB22 | G S | E COMBAT:necromancer - COMBAT (scene must not end on combat) | SER; Gore following |
| CB23 | I X P | E COMBAT:spriggan - COMBAT (scene must not end on combat) | after X6 |
| CB24 | C P | E COMBAT:spriggan - COMBAT (scene must not end on combat) | — |
| CB25 | K G | E COMBAT:troll - COMBAT (scene must not end on combat) | after A1 |
| CB26 | L P | E COMBAT:troll - COMBAT (scene must not end on combat) | — |
| CB27 | C G | E COMBAT:giant - COMBAT (scene must not end on combat) | after R5 |
| CB28 | V K | E COMBAT:giant - COMBAT (scene must not end on combat) | after A2 |
| CB29 | I X | E COMBAT:mammoth - COMBAT (scene must not end on combat) | after X6 |
| CB30 | A G | E COMBAT:bear - COMBAT (scene must not end on combat) | ASHE |
| CB31 | R X | E COMBAT:bear - COMBAT (scene must not end on combat) | Remi and Xelzaz not fallen out (TRIGGERS.md §3) |
| CB32 | K I | E COMBAT:sabrecat - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |
| CB33 | C P | E COMBAT:wolf - COMBAT (scene must not end on combat) | — |
| CB34 | S V | E COMBAT:wolf - COMBAT (scene must not end on combat) | SER; Val following; NIGHT |
| CB35 | R G | E COMBAT:skeever - COMBAT (scene must not end on combat) | Remi-Gore intro done (HLIOGoreBanter) |
| CB36 | K C | E COMBAT:skeever - COMBAT (scene must not end on combat) | after R1 |
| CB37 | I P | E COMBAT:spider - COMBAT (scene must not end on combat) | — |
| CB38 | G I | E COMBAT:spider - COMBAT (scene must not end on combat) | after C2 |
| CB39 | R I | E COMBAT:spider - COMBAT (scene must not end on combat) | after B6 |
| CB40 | K G | E COMBAT:dragon - COMBAT (scene must not end on combat) | DB; K_CRUSH; after A1 |
| CB41 | V P | E COMBAT:dragon - COMBAT (scene must not end on combat) | DB; SHOUT1 |
| CB42 | C X | E COMBAT:dragon - COMBAT (scene must not end on combat) | DB; after R18 |
| CB43 | R L | E COMBAT:dwemer - COMBAT (scene must not end on combat) | after B10 |
| CB44 | K R | E COMBAT:dwemer - COMBAT (scene must not end on combat) | after B1 |
| CB45 | A R P | E COMBAT:dwemer - COMBAT (scene must not end on combat) | ASHE_REVEAL |
| CB46 | C K | E COMBAT:hagraven - COMBAT (scene must not end on combat) | after R1 |
| CB47 | P C | E COMBAT:hagraven - COMBAT (scene must not end on combat) | after R11 or Redcap following |
| CB48 | X K P | E COMBAT:dremora - COMBAT (scene must not end on combat) | after C3 |
| CB49 | L I | E COMBAT:dremora - COMBAT (scene must not end on combat) | Lucien-Inigo intro done |
| CB50 | G L | E COMBAT:atronach - COMBAT (scene must not end on combat) | after L1 |
| CB51 | V X | E COMBAT:atronach - COMBAT (scene must not end on combat) | after X4 |

### PART 2 - IN THE THICK OF IT  (44 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB52 | G P | E COMBAT:any (Gore below half health) - COMBAT (scene must not end on combat) | — |
| CB53 | L I | E COMBAT:any (Lucien below half health) - COMBAT (scene must not end on combat) | Lucien-Inigo intro done |
| CB54 | X R | E COMBAT:any (Remi below half health) - COMBAT (scene must not end on combat) | Remi and Xelzaz not fallen out |
| CB55 | K P | E COMBAT:any (Kaidan below half health) - COMBAT (scene must not end on combat) | K_TOG+ |
| CB56 | V A | E COMBAT:any (Val below half health) - COMBAT (scene must not end on combat) | ASHE; Val following |
| CB57 | G S | E COMBAT:any (Serana below half health) - COMBAT (scene must not end on combat) | SER; SER_VAMP; Gore following |
| CB58 | G C | E COMBAT:any (Redcap below half health) - COMBAT (scene must not end on combat) | after R5 |
| CB59 | I K | E COMBAT:any (Inigo hit by an arrow) [UNC] - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |
| CB60 | L G | E COMBAT:any (friendly hit: Lucien on Gore) [UNC] - COMBAT (scene must not end on combat) | after L1 |
| CB61 | K V | E COMBAT:any (Val's bolt kills an enemy next to Kaidan) [UNC] - COMBAT (scene must not end on combat) | after A2 |
| CB62 | R P | E COMBAT:any (friendly hit: player on Remi) - COMBAT (scene must not end on combat) | — |
| CB63 | R K | E COMBAT:any (friendly hit: Scrap on Kaidan) [UNC] - COMBAT (scene must not end on combat) | after B1 |
| CB64 | X G | E COMBAT:any (friendly hit: Gore on Xelzaz) [UNC] - COMBAT (scene must not end on combat) | after X1 |
| CB65 | L A | E COMBAT:any - COMBAT (scene must not end on combat) | ASHE; Lucien following |
| CB66 | G P | E COMBAT:any - COMBAT (scene must not end on combat) | G_FLIRT or G_TOG+ |
| CB67 | V K | E COMBAT:any - COMBAT (scene must not end on combat) | K_ANY and (V_FLIRT or V_TOG+) |
| CB68 | K P | E COMBAT:any - COMBAT (scene must not end on combat) | K_CRUSH |
| CB69 | S A | E COMBAT:any - COMBAT (scene must not end on combat) | S_COMP; A_ANY |
| CB70 | K A | E COMBAT:any - COMBAT (scene must not end on combat) | A_ANY; K_ANY; ASHE_REVEAL |
| CB71 | V G P | E COMBAT:any - COMBAT (scene must not end on combat) | G_ANY or V_ANY; after A3 |
| CB72 | K G | E COMBAT:any - COMBAT (scene must not end on combat) | K_TOG+; after A1 |
| CB73 | G P | E COMBAT:any (player heals Gore) - COMBAT (scene must not end on combat) | — |
| CB74 | V I | E COMBAT:any - COMBAT (scene must not end on combat) | after I1 |
| CB75 | V G | E COMBAT:any - COMBAT (scene must not end on combat) | after A3 |
| CB76 | C K | E COMBAT:any - COMBAT (scene must not end on combat) | after R1 |
| CB77 | S K | E COMBAT:any - COMBAT (scene must not end on combat) | SER; SER_VAMP; Kaidan following |
| CB78 | L S | E COMBAT:any - COMBAT (scene must not end on combat) | SER; SER_VAMP; Lucien following |
| CB79 | A G | E COMBAT:any - COMBAT (scene must not end on combat) | ASHE; Gore following |
| CB80 | A V | E COMBAT:any - COMBAT (scene must not end on combat) | ASHE; Val following |
| CB81 | X I | E COMBAT:any - COMBAT (scene must not end on combat) | after X6 |
| CB82 | L K | E COMBAT:any - COMBAT (scene must not end on combat) | Lucien-Kaidan intro done |
| CB83 | L P | E COMBAT:any (Lucien summons) - COMBAT (scene must not end on combat) | — |
| CB84 | I G P | E COMBAT:any - COMBAT (scene must not end on combat) | after C2 |
| CB85 | R C | E COMBAT:any - COMBAT (scene must not end on combat) | Remi-Redcap intro done (Redcap's Remi scenes) |
| CB86 | R G | E COMBAT:any - COMBAT (scene must not end on combat) | Remi-Gore intro done |
| CB87 | P G L | E COMBAT:any (player casting a master or expert spell) [UNC] - COMBAT (scene must not end on combat) | after L1 |
| CB88 | P K | E COMBAT:any (player casting a master or expert spell) [UNC] - COMBAT (scene must not end on combat) | — |
| CB89 | V P | E COMBAT:any (player casting a master spell) [UNC] - COMBAT (scene must not end on combat) | — |
| CB90 | P I | E COMBAT:any (player casting lightning) - COMBAT (scene must not end on combat) | — |
| CB91 | R P | E COMBAT:any (player casts an illusion frenzy spell) [UNC] - COMBAT (scene must not end on combat) | — |
| CB92 | X P | E COMBAT:any (player holding a ward) - COMBAT (scene must not end on combat) | after C3 |
| CB93 | P A | E COMBAT:any - COMBAT (scene must not end on combat) | ASHE |
| CB94 | S P | E COMBAT:any - COMBAT (scene must not end on combat) | SER |
| CB95 | K I | E COMBAT:any - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |

### PART 3 - THE TALLY: GORE VERSUS KAIDAN  (8 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB96 | G K | E AFTERFIGHT | after A1 |
| CB97 | G K | E COMBAT:any - COMBAT (scene must not end on combat) | after CB96 |
| CB98 | G K V | E AFTERFIGHT | after CB97; Val following |
| CB99 | G K C | E AFTERFIGHT:skeever | after CB97; Redcap following |
| CB100 | A G | E AFTERFIGHT | after CB97; ASHE |
| CB101 | K I | E AFTERFIGHT:spider | after CB97; KaiandInigo stage >= 10 |
| CB102 | G K P | E AFTERFIGHT | after CB98 |
| CB103 | G K | E AFTERFIGHT | after CB102 |

### PART 4 - SOUND OFF  (12 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB104 | K G C | E AFTERFIGHT | after R1; after A1 |
| CB105 | P V L | E AFTERFIGHT | after C1 |
| CB106 | A R I | E AFTERFIGHT | ASHE; Remi following; Inigo following |
| CB107 | P S X | E AFTERFIGHT | SER; SER_VAMP; Xelzaz following |
| CB108 | G L | E AFTERFIGHT | after L1 |
| CB109 | K P | E AFTERFIGHT | K_CRUSH |
| CB110 | V R | E AFTERFIGHT | Val-Remi intro done |
| CB111 | I C | E AFTERFIGHT | after R13 |
| CB112 | X G P | E AFTERFIGHT | after X1 |
| CB113 | L P | E AFTERFIGHT (Lucien got a kill) [UNC] | — |
| CB114 | K I | E AFTERFIGHT (player below a quarter health during the fight) | KaiandInigo stage >= 10; not K19 in the same session |
| CB115 | A K | E AFTERFIGHT | ASHE; after Lucien-Kaidan intro |

### PART 5 - LOOTING SQUABBLES  (10 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB116 | R V | E AFTERFIGHT:bandit | Val-Remi intro done |
| CB117 | C I | E AFTERFIGHT | after R13 |
| CB118 | G X P | E AFTERFIGHT | after X1 |
| CB119 | L K | E AFTERFIGHT:bandit | Lucien-Kaidan intro done |
| CB120 | G P | E AFTERFIGHT | after A1 or Gore following |
| CB121 | V K | E AFTERFIGHT | after A2 |
| CB122 | A R | E AFTERFIGHT:dwemer | ASHE_REVEAL; Remi following |
| CB123 | S P | E AFTERFIGHT:bandit | SER |
| CB124 | V C | E AFTERFIGHT | after R8 |
| CB125 | L I | E AFTERFIGHT:bandit | Lucien-Inigo intro done; INIGO_BV not required |

### PART 6 - AFTER THE FIGHT, BY ENEMY  (25 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB126 | G I | E AFTERFIGHT:bandit | after C2 |
| CB127 | L K | E AFTERFIGHT:draugr | Lucien-Kaidan intro done |
| CB128 | R I P | E AFTERFIGHT:draugr | after B6; Remi following; Luna also present |
| CB129 | V G | E AFTERFIGHT:falmer | after A3 |
| CB130 | K P | E AFTERFIGHT:forsworn | BRYNJAR |
| CB131 | R V | E AFTERFIGHT:thalmor | Val-Remi intro done |
| CB132 | C S | E AFTERFIGHT:vampire | SER; SER_VAMP; Redcap following |
| CB133 | R G | E AFTERFIGHT:necromancer | Remi-Gore intro done |
| CB134 | X P | E AFTERFIGHT:spriggan | after C3 |
| CB135 | I G P | E AFTERFIGHT:troll | after C2 |
| CB136 | C G | E AFTERFIGHT:giant | after R5 |
| CB137 | K X | E AFTERFIGHT:mammoth | after C3 |
| CB138 | L A | E AFTERFIGHT:bear | ASHE; Lucien following |
| CB139 | S I | E AFTERFIGHT:sabrecat | SER; Inigo following |
| CB140 | R X | E AFTERFIGHT:skeever | Remi and Xelzaz not fallen out |
| CB141 | L I | E AFTERFIGHT:spider | Lucien-Inigo intro done |
| CB142 | L P | E AFTERFIGHT:dragon | DB; Lucien following |
| CB143 | R G P | E AFTERFIGHT:dwemer | Remi-Gore intro done |
| CB144 | L C P | E AFTERFIGHT:hagraven | after R11 |
| CB145 | X I | E AFTERFIGHT:dremora | after X6 |
| CB146 | K R | E AFTERFIGHT:atronach | after B1 |
| CB147 | K P | E AFTERFIGHT (player below half health during the fight) | K_TOG+ |
| CB148 | X V | E AFTERFIGHT | after X4 |
| CB149 | P R | E AFTERFIGHT | Remi following; Val following |
| CB150 | G A | E AFTERFIGHT (NIGHT) | ASHE_REVEAL; Gore following |
