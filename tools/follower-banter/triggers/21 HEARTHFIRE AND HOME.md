# 21 HEARTHFIRE AND HOME - trigger rows (prefix HF, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\21 HEARTHFIRE AND HOME.txt`
Format and shared gate codes: `TRIGGERS.md` sections 4-5. Hearthfire records: `research\content\dlc_cc_missives_3dnpc.md` section C.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, **S Serana, A Ashe** (new codes). `+Luna` = Luna (player, Eleonora voice) has lines; she is never a gate.
Type: T = timer, E = event.

## New gate codes used here

[U] = unconfirmed, verify at build.

**Places**
- `HOUSE` = LocTypePlayerHouse (0FC1A3) on the player's current location (any owned house, Hearthfire or bought).
- `HF_AT` = player in a Hearthfire plot location or its child interior: Lakeview `00308A` (interior `003092`), Windstad `005209` (`00BE0A`), Heljarchen `00520A` (`00BE1D`), all HearthFires.esm. `HF_LAKE` / `HF_WIND` / `HF_HELJ` = that plot only. Add `ext` or `int` for exterior/interior.
- `HOUSE_RETURN` = entered a `HOUSE` after 7+ game days without being in one. Needs a controller float `FB_LastHouseDay` set on every HOUSE exit. [U, new global]
- `HOUSE_LEAVE` = OnLocationChange from a `HOUSE` location to a non-house location, with the party following.
- `DUSK` = hour 18..20. `NIGHT`, `PREDAWN`, `MORNING`, `RAIN`, `SNOW`, `CAMP` as TRIGGERS.md section 4.

**Building progress** (globals `BYOHHouse{1,2,3}Room*` in HearthFires.esm; 1 = Lakeview, 2 = Windstad, 3 = Heljarchen is the research guess; which Room number is which wing is **[U]**, read it from the BYOH building script before relying on any of these)
- `HF_OWN` = owns at least one plot: `BYOHHouseBuilding` 00305D running, or `BYOHHouseFalkreath 00305E` / `Hjaalmarch 00BE09` / `Pale 010BEE` stage 10 done. [U stage]
- `HF_ALL3` = all three plot quests at stage 10+. [U stage]
- `HF_SMALL` = small house finished at the current plot (`Room01` == 1). [U]
- `HF_HALL` = main hall finished (`Room01B`?). [U]
- `HF_CELLAR` = cellar finished. [U which global]
- `HF_W:<wing>` = that wing finished at the current plot. Wings: east = ALCHEMY / ENCHANTER / KITCHEN; north = LIBRARY / ARMORY / TROPHY; west = BEDROOMS / GREENHOUSE / STORAGE. [U global map]
- `HF_NOT:<east|north|west>` = no option of that wing built yet at this plot.
- `HF_DONE` = all three wings finished at the current plot.
- `HF_BUILDING` = `HF_AT` and not `HF_DONE`.
- `HF_APIARY` (Lakeview), `HF_HATCHERY` (Windstad) = player within 1500 units of that exterior addition. [U which plot has which; U the furniture/activator ref to measure from]

**Household**
- `HF_STEWARD` = `BYOHHouseStewardOffer` 00308B stage 200 done.
- `HF_BARD`, `HF_CHICKENS`, `HF_COW` = the steward has hired a bard / bought chickens / bought a cow at the current plot. [U, find the purchase globals or alias fills in the BYOHHouse* quest]
- `HF_ATTACK:<giant|bandit|wolf|skeever>` = AFTERFIGHT at `HF_AT` while/just after `BYOHHouseGiantAttack 000C3E` / `BanditAttack 005207` or `0008A8` / `WolfAttack 000C39` / `SkeeverInfestation 010A44` stopped (completed within the last game hour). [U, quests are combat-silent while running]

**Children** (check the child refs, not the player)
- `HF_KID` = at least one NPC in `BYOHRelationshipAdoptionChildOwnedFaction` 0183A8. Controller scans the BYOHRelationshipAdoption child aliases on load. [U method]
- `HF_KID_FIRST` = first HOUSE visit after `HF_KID` became true (say-once).
- `HF_KIDS3` = 3+ adopted children (only possible with HearthfireMultiKid / _Expanded). [U, count MultiKid's extra aliases]
- `KID_NEAR` = an adopted child within 1000 units of the player. **Only talks marked `KS` (kid-safe) may play while KID_NEAR.** Every row without `KS` carries `not KID_NEAR`.
- `KID_AWAY` = no adopted child within 2000 units (talks about a child's dark past).
- `KID:<name>` = that child is adopted, e.g. `KID:Sofie`, `KID:Aventus` (Aventus Aretino), `KID:Honorhall` (any of the Riften orphanage children). [U refs]
- `HF_PET:rabbit` = the child's pet is the rabbit/bunny. [U that a rabbit is one of the Hearthfire child pets; drop HF70 if not]
- `GRELOD_DEAD` = Grelod the Kind ref `GetDead`.

**Serana** (from serana.md section 6)
- `SER` = Serana following: `GetVMQuestVariable(DLC1NPCMentalModel 002B6E:Dawnguard.esm, ::IsFollowing_var) == 1` AND `GetQuestCompleted DLC1VQ02` AND `SDA_PlayerInDialogue == 0`. Every Serana row implies SER.
- `SER_VAMP` = Serana `HasKeyword Vampire` (0A82BB) == 1 (not cured).
- `SER_GARDEN` = DLC1VQ04 (00284F) completed (she has seen Valerica's garden).
- `SER_NOTWED` = `SDA_IsSeranaMarried` == 0.

**Ashe** (from ashe.md section 6)
- `ASHE` = Ashe following: `GetVMQuestVariable(MM_AsheMentalModel 06FE28, ::IsFollowing_var) == 1`, `MM_AsheMentalModel.bConfigVarIdles == 1`, `MM_PlayerinDialogue == 0`, `MM_FlashbackRunning == 0`, and her quest-running blocks. Every Ashe row implies ASHE.
- `ASHE_REVEAL` = `MM_FriendshipQuest` 1A9DEE stage >= 70 or `MM_AutomatonReveal == 1`. Required for anything that says she is a machine (joints, no breath, built, woke up grown).

**Romance / marriage**
- `K_MAR` as TRIGGERS.md (K04 == 100, or PlayerMarriedFaction on Kaidan). Global quiet rule already blocks `RelationshipMarriageWedding` 10..499 and Kaidan's wedding/honeymoon windows.
- Married talks avoid children and Kaidan's own 85+ home/kids topics, so they need no kid gate beyond `not KID_NEAR` where they swear.

## Per-talk table

### Part A - Breaking ground
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF1 | G V +Luna | E arrival at HF_AT (first visit to that plot) | HF_OWN; HF_BUILDING; not KID_NEAR |
| HF2 | A G | T | HF_AT; HF_BUILDING; not HF_SMALL; not KID_NEAR |
| HF3 | K +Luna | E HF_AT (first visit after HF_SMALL) | HF_SMALL; KS |
| HF4 | V R | T | HF_AT; HF_BUILDING; KS |
| HF5 | L G | T | HF_AT; HF_BUILDING; not KID_NEAR |
| HF6 | A K | T | HF_AT; HF_BUILDING; KS |
| HF7 | C R | T | HF_AT ext; HF_BUILDING; KS |
| HF8 | L I | T | HF_AT; HF_BUILDING; KS |
| HF9 | I S | T | HF_AT ext; HF_BUILDING; SER; KS |
| HF10 | K I +Luna | E NIGHT at HF_AT int | HF_SMALL; not HF_HALL; KS |
| HF11 | L +Luna | E HF_AT int (first visit after HF_HALL) | HF_HALL; KS |
| HF12 | G R X +Luna | E HF_AT (first visit after HF_DONE) | HF_DONE; after:HF4; KS |

### Part B - Everyone wants a room
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF13 | R X | T | HF_AT; HF_HALL; KS |
| HF14 | A R | T | HF_AT; HF_HALL; ASHE_REVEAL; after:HF13; KS |
| HF15 | X +Luna | T | HF_AT; HF_HALL; HF_NOT:east; KS |
| HF16 | C X | T | HF_AT; HF_NOT:east; after:HF15; KS |
| HF17 | L +Luna | T | HF_AT; HF_HALL; HF_NOT:north; KS |
| HF18 | L S +Luna | T | HF_AT int; HF_W:LIBRARY; SER; KS |
| HF19 | K +Luna | T | HF_AT; HF_HALL; HF_NOT:north; KS |
| HF20 | C S | T | HF_AT int; HF_CELLAR; SER; KS |
| HF21 | S +Luna | T | HF_AT; HF_CELLAR; SER; after:HF20; KS |
| HF22 | I A | T | HF_AT ext; HF_HALL; ASHE_REVEAL; KS |
| HF23 | V G | T | (HF_LAKE or HF_WIND) ext; KS |
| HF24 | G C | T | HF_AT; HF_HALL; HF_NOT:north; RC_MANOS (Bigpig found) [U: Bigpig is found in Back to the Rock; RC_MANOS is later and safe]; KS |
| HF25 | A S | T | HF_AT; (HF_NOT:west or HF_W:GREENHOUSE); ASHE_REVEAL; SER_GARDEN; KS |
| HF26 | V +Luna | E NIGHT at HF_AT int | HF_W:ENCHANTER; KS |
| HF27 | R C | T | HF_AT int; HF_W:STORAGE; KS |
| HF28 | C I | E HF_LAKE ext near HF_APIARY | HF_LAKE; KS |
| HF29 | K G | T | HF_AT int; HF_W:BEDROOMS; KS |
| HF30 | V R +Luna | T | HF_AT; HF_HALL; KS |

### Part C - The three homesteads
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF31 | I +Luna | E DUSK at HF_LAKE ext | HF_LAKE; KS |
| HF32 | A G | E WATER at HF_LAKE ext | HF_LAKE; KS |
| HF33 | L K | T | HF_LAKE ext; not KID_NEAR |
| HF34 | X C | E arrival HF_WIND ext | HF_WIND; KS |
| HF35 | I X | E HF_WIND ext near HF_HATCHERY | HF_WIND; KS |
| HF36 | L S | E NIGHT at HF_WIND ext | SER; SER_VAMP; not KID_NEAR |
| HF37 | X A | E SNOW at HF_HELJ ext | HF_HELJ; ASHE_REVEAL; KS |
| HF38 | G K | T | HF_HELJ; GORE_BAIL; not KID_NEAR |
| HF39 | V +Luna | T | HF_ALL3; HOUSE or HF_AT; KS |

### Part D - The party's tavern
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF40 | X V C | T | HOUSE; KS |
| HF41 | G +Luna | T | HOUSE; hour >= 18; KS |
| HF42 | C K +Luna | E HOUSE_RETURN | HOUSE; KS |
| HF43 | L X | T | HOUSE; KS |
| HF44 | K V | T | HOUSE; KS |
| HF45 | I L +Luna | T | HOUSE; hour >= 18; KS |
| HF46 | R V | E MORNING in HOUSE | HOUSE; KS |
| HF47 | A L | T | HOUSE; KS |
| HF48 | S X | T | HOUSE; hour >= 18; SER; KS |
| HF49 | V +Luna | E MORNING in HOUSE (hour 5..8) | HOUSE; KS |
| HF50 | I X | E RAIN while in HOUSE | HOUSE; KS |
| HF51 | L C | T | HOUSE; RC_MANOS (Bigpig); KS |
| HF52 | G X | T | HOUSE; hour >= 18; KS |
| HF53 | I +Luna | T | HOUSE; KS |
| HF54 | S +Luna | T | HOUSE; SER; KS |
| HF55 | L V | T | HOUSE; after:C1 (lunch-money talk); KS |

### Part E - Stewards, chickens and uninvited guests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF56 | V X | T | HF_AT; HF_STEWARD; KS |
| HF57 | G L | T | HF_AT; HF_BARD; not KID_NEAR |
| HF58 | I V | E HF_AT ext | HF_CHICKENS; KS |
| HF59 | C K | E HF_AT ext | HF_COW; KS |
| HF60 | G K I | E AFTERFIGHT HF_ATTACK:giant | HF_AT; KS |
| HF61 | S C | E AFTERFIGHT HF_ATTACK:skeever | HF_AT; SER; after:HF20; KS |
| HF62 | A V | E AFTERFIGHT HF_ATTACK:bandit | HF_AT; KS |
| HF63 | C A +Luna | E AFTERFIGHT HF_ATTACK:wolf | HF_AT; ASHE_REVEAL; KS |

### Part F - The little ones
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF64 | G +Luna | E HF_KID_FIRST | HOUSE; HF_KID; KID_AWAY |
| HF65 | I X | T | HOUSE; HF_KID; KS |
| HF66 | R A | T | HOUSE; HF_KID; ASHE_REVEAL; KS |
| HF67 | C I | T | HOUSE; KID_NEAR; KS |
| HF68 | R G | T | HOUSE; HF_KID; KS |
| HF69 | L +Luna | E NIGHT in HOUSE | KID_NEAR; KS |
| HF70 | I +Luna | T | HOUSE; HF_PET:rabbit [U]; KS |
| HF71 | G K | T | HOUSE; KID_NEAR; KS (the joke is that they swallow the swears) |
| HF72 | R S | T | HOUSE; KID_NEAR; SER; KS |
| HF73 | L A | T | HOUSE; KID_NEAR; KS |
| HF74 | X +Luna | E NIGHT in HOUSE | KID_NEAR; KS |
| HF75 | R V | T | HOUSE; KID:Honorhall; GRELOD_DEAD; KID_AWAY |
| HF76 | L X | T | HOUSE; KID:Aventus; KID_AWAY |
| HF77 | V +Luna | T | HOUSE; KID:Sofie; KS |
| HF78 | R X L | T | HOUSE; HF_KIDS3 (HearthfireMultiKid) [U]; KS |
| HF79 | G V | T | HOUSE; KID_NEAR; KS |
| HF80 | S +Luna | T | HOUSE; HF_KID; SER; KS |

### Part G - Married life at home (K_MAR)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF81 | V K | T | K_MAR; HOUSE or HF_AT; KS |
| HF82 | G K | T | K_MAR; BRYNJAR; HF_AT ext; KS |
| HF83 | K +Luna | E PREDAWN at HF_AT ext (or HOUSE ext) | K_MAR; KS |
| HF84 | I K | E NIGHT in HOUSE | K_MAR; KS |
| HF85 | R K | T | K_MAR; HOUSE; KS |
| HF86 | K +Luna | E MORNING in HOUSE | K_MAR; KS |
| HF87 | K L +Luna | T | K_MAR; HOUSE; KS |
| HF88 | C K +Luna | T | K_MAR; HOUSE; after:HF10 (woodbox) preferred, not required; KS |
| HF89 | L V | T | K_MAR; HOUSE; KS |
| HF90 | K G +Luna | E arrival HOUSE | K_MAR; not KID_NEAR |

### Part H - The rivals come round (K_MAR)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF91 | R G | T | K_MAR; HOUSE or HF_AT; KS |
| HF92 | V S | T | K_MAR; HOUSE; hour >= 18; SER; SER_NOTWED; not KID_NEAR |
| HF93 | A K | T | K_MAR; HF_AT ext; KS |
| HF94 | S K | T | K_MAR; HOUSE; SER; SER_VAMP; SER_NOTWED; not KID_NEAR |
| HF95 | V G A | T | K_MAR; HF_AT ext; hour >= 18; not KID_NEAR |
| HF96 | K G | T | K_MAR; HOUSE; not KID_NEAR |
| HF97 | S A +Luna | T | K_MAR; HOUSE; SER; after:HF89 preferred (humming callback); KS |

### Part I - Home
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF98 | X +Luna | T | HF_AT; HF_DONE; after:HF10 (woodbox); KS |
| HF99 | L I | E HOUSE_LEAVE | after any 3 Part D talks; KS |
| HF100 | G R C +Luna | E HOUSE, hour 17..20 | HOUSE; all three speakers Free; say-once; KS |

## Notes for the build
- Kid-safe audit: rows marked `not KID_NEAR` contain "Tusk yourself", "Mara's tits", "Bloody hell", drinking, vampire-bite jokes, or a child's dark past. All other rows are clean enough to play with kids in the room.
- Kaidan's own 85+ home and children lines: none of HF81-HF97 touch children, kid names, nurseries or "our family" talk, so they cannot contradict his mod. Kaidan's only kid-room talk here (HF71) is about swearing, not fatherhood.
- Val00D (Ravani) and Val's own house comments (`Val000BYOH*`) are not echoed. Remi's own kid banter (`HLIOKidBanterChecker`, married-to-Remi only) is not echoed.
- Hearthfire wing contents (east = alchemy/enchanter/kitchen, north = library/armory/trophy, west = bedrooms/greenhouse/storage) are from memory of vanilla Hearthfire. [U] confirm before wiring HF15-HF27.
- HF25 assumes Ashe's Lunar Tears are a flower Serana can call "night lilies" (Nocturne Lily). Flavour only.
