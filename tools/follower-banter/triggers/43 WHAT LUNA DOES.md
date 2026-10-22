# Triggers - 43 WHAT LUNA DOES (prefix PA, 160 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\43 WHAT LUNA DOES.txt`
Written 2026-10-18. Event signatures checked against the bundled Papyrus corpus (vanilla, SKSE, po3 Papyrus Extender). Nothing in the game or profile was touched.

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C) plus **S = Serana**, **A = Ashe**, **U = Luna** (player line, Eleonora voice; no Free() test).
Gate codes as TRIGGERS.md section 4. Every talk in this file is **E** (fires on the moment, or at the first safe moment after it: WorldQuiet() and Free() always apply, so "right after a fight" means when the combat-end 8 s delay passes, and "right after you steal" means the next safe tick within 60 s, else drop the talk until the event happens again).

## How the controller sees what Luna does

All of these live on the controller's **player alias script** (FB_Controller). Signatures confirmed in the corpus unless marked.

| Hook | What it gives us | Used for |
|---|---|---|
| `RegisterForTrackedStatsEvent()` + `OnTrackedStatsEvent(string arStatName, int aiStatValue)` (vanilla) | fires whenever a tracked player stat changes | steals, pickpockets, locks, jail, fines, bribes, assaults, murders, potions, poisons, enchants, books, skill books, shouts, souls, artifacts, horses, houses, investing, diseases |
| `Game.QueryStat(string)` (vanilla) | current value of a stat | thresholds and "since last time" deltas (controller keeps last values in an int array) |
| po3 `OnLevelIncrease`, `OnSkillIncrease(int aiSkill)`, `OnSpellLearned(Spell)`, `OnBookRead(Book)`, `OnItemCrafted(ObjectReference akBench, Location, Form akCreatedItem)`, `OnSoulTrapped(Actor, Actor)`, `OnActorKilled(Actor akVictim, Actor akKiller)`, `OnDragonSoulGained`, `OnShoutAttack(Shout)`, `OnLocationDiscovery`, `OnMagicEffectApplyEx`, `OnMagicHit` | po3 Papyrus Extender events (register with the matching `RegisterFor...` po3 call) | level/skill milestones, new spells, books, crafting bench type, soul trap, kills, shouts, discoveries |
| `OnPlayerFastTravelEnd(float afTravelGameTimeHours)` (vanilla/SKSE) | game hours the trip took | fast travel and carriage talks |
| `RegisterForSleep()` + `OnSleepStart` / `OnSleepStop(bool abInterrupted)` (vanilla) | sleep start/stop, interrupted flag | sleeping rough, woken by an attack, morning-after talks |
| `OnRaceSwitchComplete()` (vanilla) + `Player.GetRace()` | race changed | werewolf / Vampire Lord in and out |
| `OnVampireFeed(Actor akTarget)` (vanilla) | player fed | PA104 |
| `OnObjectEquipped(Form akBaseObject, ObjectReference)` / `OnObjectUnequipped` (vanilla) | worn items, eaten food, drunk drinks | armour, helmet, nothing worn, amulet, masks, raw food, alcohol, sweet rolls |
| `OnItemAdded` / `OnItemRemoved(..., ObjectReference akDestContainer)` (vanilla) with `AddInventoryEventFilter(FormList)` | skooma in pack; items dropped (dest = None) | PA124/125, PA142/143, lockpick breaks |
| `OnMagicEffectApply(ObjectReference akCaster, MagicEffect akEffect)` (vanilla) on player and on follower aliases | healing received, healing given | PA150-153 |
| `OnHit` (vanilla) + `GetActorValuePercentage("Health")` | health dipped low in a fight | LOWHP close-call talks |
| polls on the 60 s tick: `IsSwimming()`, po3 `IsActorUnderwater`, `IsOnMount()`, `GetGoldAmount()`, `GetTotalItemWeight()` (SKSE) vs `GetActorValue("CarryWeight")`, `GetWornForm(0x4)` (SKSE), `Faction.GetCrimeGold()` per hold crime faction | swimming, riding, gold, overencumbered, naked, bounty | Parts 2, 4, 9, 11 |

**Stat names** used below are the vanilla tracked-stat strings as I remember them: "Items Stolen", "Pockets Picked", "Locks Picked", "Times Jailed", "Days Jailed", "Jail Escapes", "Fines Paid", "Bribes", "Assaults", "Murders", "Horses Stolen", "Horses Owned", "Houses Owned", "Stores Invested In", "Potions Mixed", "Poisons Mixed", "Ingredients Eaten", "Magic Items Made", "Weapons Made", "Armor Improved", "Books Read", "Skill Books Read", "Times Shouted", "Shouts Mastered", "Words Of Power Learned", "Shouts Learned", "Dragon Souls Collected", "Daedric Artifacts Found", "Diseases Contracted", "Necks Bitten", "Sneak Attacks", "Total Lifetime Bounty", "Potions Used". **[UNCONFIRMED spellings: print every `arStatName` from OnTrackedStatsEvent in a test save and correct the table before build.]**

## New gate codes for this file

- `STAT:<name> +1` = that stat just rose. `STAT:<name> >= n` = threshold reached this tick for the first time (controller remembers it fired).
- `CRIME` = sum of `GetCrimeGold()` over the hold crime factions (CrimeFactionWhiterun, ...Rift, ...Haafingar, ...Eastmarch, ...Reach, ...Pale, ...Hjaalmarch, ...Falkreath, ...Winterhold, DLC2CrimeRavenRockFaction). `CLEAN` = CRIME did not rise within 5 s of the action. `CAUGHT` = it did.
- `SEEN` = every follower speaker in the talk was within 1500 units of the player and `HasLOS(Player)` at the moment of the action.
- `JAIL_OUT` = player leaves a jail cell and is released or pardoned: `STAT:Times Jailed +1` remembered, fires on the first `OnLocationChange` out of the jail interior where all speakers are Free (followers do not follow into jail; they stand outside the jail door, which is the "reunion"). **[UNCONFIRMED: which followers' own frameworks move them to the jail exterior; if a follower is not within 1000 units, Free() fails and the talk waits]**.
- `LOWHP` = player health below 15% at any point in the fight that just ended. `NEARDEATH_N` = controller counter of LOWHP fights, with a 30-game-day window for PA156.
- `NAKED` = `GetWornForm(0x00000004) == None` (body slot 32) for 30 s, exterior, not LocTypeInn / LocTypePlayerHouse / LocTypeDwelling, not swimming, not in a werewolf/vampire-lord race.
- `MARA` = player just equipped Amulet of Mara (`AmuletofMara` 0C891B:Skyrim.esm). `UNWED` = not K_MAR, not V_MAR, not G_OATH, `SDA_IsSeranaMarried == 0`, and vanilla `RelationshipMarriageFIN` not past its wedding stage **[UNCONFIRMED stage]**. Kaidan never speaks in a MARA talk (his own mod has the line).
- `SERANA_F` = `DLC1VQ02` completed and `DLC1NPCMentalModel::IsFollowing_var == 1`, `SDA_PlayerInDialogue == 0`. `S_VAMP` = Serana HasKeyword Vampire (0A82BB). `S_ROM` = `SDA_SeranaRomance == 1` and `SDA_SeranaRomance04` stage >= 20 **[UNCONFIRMED stage; from serana.md suggestion]** and not refused at Romance04.
- `ASHE_F` = `MM_AsheMentalModel::IsFollowing_var == 1`, `bConfigVarIdles == 1`, `MM_PlayerinDialogue == 0`, `MM_FlashbackRunning == 0`. `ASHE_REVEAL`, `ASHE_AMENDS` as ashe.md section 6. `A_CRUSH` = `MM_RM >= 4` and `MM_AsheRomance == 0`. `A_TOG` = `MM_AsheRomance == 1`. `A_ANY` = A_CRUSH or A_TOG.
- `G_ANY` = G_FLIRT or G_TOG+. `V_ANY` = V_FLIRT or V_TOG+.
- `K_I` = KaiandInigo (000842:Kaidan and Inigo Meet.esp) stage >= 10.
- `VAMP` = player has the vampire keyword / PlayerVampireQuest running. `WOLF` as TRIGGERS.md. `WILD` as TRIGGERS.md section 5 (exterior, not LocTypeHabitation).
- `INNOCENT` = victim was not hostile to the player, not in combat with the player or a follower before the player's first hit, `IsGuard() == false` (except PA30), not a creature, and **no Dark Brotherhood / Morag Tong contract was the reason**: skip if the victim fills an alias in any running DB / DBContract / DLC2 Morag Tong quest **[UNCONFIRMED method; fallback: skip while any DB0x / DBRadiant / DLC1 / DLC2 contract quest is running]**. Also skip if the victim was under a Frenzy/Wabbajack effect from the player.
- `DB` = TRIGGERS.md (real Watchtower kill). All shout/soul talks carry it.

## Table

### Part 1 - Light fingers
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA1 | R V | E `STAT:Items Stolen +1` and CLEAN and SEEN | first time ever with R and V both following |
| PA2 | I U | E `STAT:Items Stolen +1`, CLEAN; item is food (`VendorItemFood` keyword) taken in a LocTypeDwelling interior | — |
| PA3 | L U | E `STAT:Items Stolen +1`, CLEAN; `OnItemAdded` of a Book (not a spell tome) in the same second | — |
| PA4 | R K | E `STAT:Items Stolen +1`, CLEAN, LocTypeStore; the store's merchant (vendor faction member) is within 800 units | after B1 |
| PA5 | C G | E `STAT:Items Stolen +1`, CLEAN; item base value <= 2 | after R5 |
| PA6 | V S | E `STAT:Pockets Picked +1`, CLEAN | SERANA_F |
| PA7 | I L | E `STAT:Pockets Picked +1`, CLEAN | `STAT:Pockets Picked >= 2`; after PA2 |
| PA8 | K U | E pickpocket CAUGHT: `CRIME` rises while ContainerMenu was in pickpocket mode / `STAT:Pockets Picked` unchanged **[UNCONFIRMED: no direct "pickpocket failed" event; SM Event "Crime Gold" + target in combat with player afterwards is the fallback]** | — |
| PA9 | R U | E `STAT:Locks Picked +1` and the lock's `GetLockLevel() >= 75` (Expert/Master) | — |
| PA10 | G K | E 3+ Lockpick (00000A:Skyrim.esm) items removed in 60 s with no lock opened | after A1 |
| PA11 | I V | E `STAT:Items Stolen +1`, CLEAN; the item's owner actor is in the same cell within 600 units and not detecting the player | after I1 |
| PA12 | L R | E `STAT:Items Stolen +1`, CLEAN; item is in our FormList of Dwemer clutter/misc items | after B10 |
| PA13 | A R | E `STAT:Items Stolen +1`, CLEAN; item is a SoulGem or has `VendorItemSoulGem` / is an enchanted item | ASHE_F; ASHE_HIRED |
| PA14 | G C | E `STAT:Horses Stolen +1`, fires at first dismount | after R5 |
| PA15 | X I | E `STAT:Items Stolen +1`, CLEAN, location has LocTypeTemple | — |
| PA16 | R V U | E `STAT:Items Stolen >= 25` | after PA1 |

### Part 2 - The law
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA17 | K V | E any single hold crime faction `GetCrimeGold() >= 1000` (first time) | after A2 |
| PA18 | L K | E `STAT:Fines Paid +1` | after Lucien-Kaidan intro (Lucien's JRLucienFollowerKaidanScene1 played) **[UNCONFIRMED flag]** |
| PA19 | G V | E `STAT:Fines Paid +1` | GORE_BAIL; after A3 |
| PA20 | K U | E JAIL_OUT | first JAIL_OUT ever; K_CRUSH |
| PA21 | R I | E JAIL_OUT | first JAIL_OUT ever and PA20 did not play (not K_CRUSH or Kaidan absent); after B6 |
| PA22 | V C | E `STAT:Jail Escapes +1`, first safe tick outside the jail | after R8 |
| PA23 | S G | E JAIL_OUT | `STAT:Times Jailed >= 2`; SERANA_F |
| PA24 | X U | E JAIL_OUT | `STAT:Times Jailed >= 2` |
| PA25 | L U | E JAIL_OUT and any skill's base value dropped during the stay (controller snapshots skills at `STAT:Times Jailed +1`) | — |
| PA26 | R U | E JAIL_OUT and the jail removed stolen items (count of stolen-flagged items fell) **[UNCONFIRMED check; fallback: Items Stolen > 0 before jail]** | after PA5 |
| PA27 | V G | E `STAT:Bribes +1` while a guard (`IsGuard`) is within 500 units | after A3 |
| PA28 | L K | E 2+ hold crime factions have `GetCrimeGold() > 0` at once | K_CRUSH; after PA18 |
| PA29 | C I | E a guard within 600 units and `STAT:Total Lifetime Bounty >= 1000`, in CITY | after R13 |

### Part 3 - Where they draw the line (serious; event-gated)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA30 | K I | E po3 `OnActorKilled` killer == Player, victim `IsGuard()`, victim was not in combat with the player before the player's first hit; fires at the first safe moment (usually after the guard fight) | K_I |
| PA31 | G U | E `OnActorKilled` killer == Player, victim INNOCENT | not G murderer branch (`HD1GoreMurdererVar == 0`) |
| PA32 | L X | E `STAT:Assaults +1` and the victim is alive 30 s later, victim INNOCENT | — |
| PA33 | I U | E second INNOCENT kill or assault (controller counter = 2) | after PA31 or PA32 or PA37 |
| PA34 | A S | E `OnActorKilled` killer == Player, victim INNOCENT, LocTypeHabitation, a child actor (`IsChild`) within 2000 units **[UNCONFIRMED: fallback = any INNOCENT kill in a town]** | ASHE_AMENDS; SERANA_F |
| PA35 | V U | E INNOCENT kill counter reaches 3 | — |
| PA36 | G K | E AFTERFIGHT where at least one hostile was `IsGuard()` | after A1 |
| PA37 | R U | E `STAT:Assaults +1`, victim INNOCENT | — |
| PA38 | I G | E player kills a Chicken (race `ChickenRace`) in LocTypeHabitation and `CRIME` rises; fires after combat ends | after C2 |
| PA39 | K U | E player receives the Gift of Charity effect (vanilla beggar reward spell) **[UNCONFIRMED FormID; find "Gift of Charity" SPEL at build]** | — |

### Part 4 - Money and property
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA40 | G C | E `GetGoldAmount() >= 1000` first time | after R5 |
| PA41 | V R | E `GetGoldAmount() >= 5000` first time | `HLIOValRemiFriendshipTracker >= 2` (business talks done) **[nice-to-have; drop if unavailable]** |
| PA42 | K U | E `GetGoldAmount() >= 10000` first time | — |
| PA43 | I X | E `GetGoldAmount() >= 25000` first time | — |
| PA44 | G K | E `STAT:Houses Owned` reaches 1 | after A1 |
| PA45 | R X | E po3 `OnSkillIncrease` Speech reaching 50 while BarterMenu open (or within 60 s of it closing) | Remi/Xel not fallen out |
| PA46 | V U | E `STAT:Stores Invested In +1` | — |
| PA47 | G U | E `STAT:Horses Owned +1` from a purchase (not Horses Stolen) | — |
| PA48 | L K | E 3+ game days after PA47 | LUC_ADMIT; after PA47 |
| PA49 | S I | E gold drops by >= 1000 in one BarterMenu session and a spell tome (Book with `GetSpell() != None`, SKSE) was added | SERANA_F |

### Part 5 - Getting stronger
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA50 | K G | E po3 `OnLevelIncrease`, level 10 | after A1 |
| PA51 | V K | E level 20 | K_CRUSH and V_FLIRT |
| PA52 | S A | E level 30 | S_ROM and A_ANY; SERANA_F, ASHE_F |
| PA53 | R I | E level 5 | after B6 |
| PA54 | G U | E level 40 | G_ANY |
| PA55 | K I | E level 50 | K_TOG+; K_I |
| PA56 | V U | E `OnSkillIncrease` Destruction reaching 50 | — |
| PA57 | S U | E level 35 | SERANA_F |
| PA58 | C X | E level 15 | Redcap-Xelzaz own intro done (as R18) |
| PA59 | K G V | E level 25 | ANYROM; after A1, A2, A3 |
| PA60 | A G | E level 20 (if PA51 also qualifies, PA51 plays first and PA60 waits for the next safe tick) | ASHE_F |
| PA61 | K U | E level 45 | K_LOVE+ |

### Part 6 - Forge, cauldron and rune
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA62 | K G | E po3 `OnItemCrafted`, bench is a forge (`CraftingSmithingForge` keyword on akBench's base), first time | after A1 |
| PA63 | V U | E `STAT:Armor Improved +1`, first time | — |
| PA64 | X I | E `OnItemCrafted`, created item has `ArmorMaterialDaedric` or `WeapMaterialDaedric` | — |
| PA65 | G C | E `OnSkillIncrease` Smithing reaching 100 | after R5 |
| PA66 | X U | E `STAT:Potions Mixed` reaches 1 | — |
| PA67 | R X | E `STAT:Potions Mixed >= 10` | Remi/Xel not fallen out |
| PA68 | X U | E `OnSkillIncrease` Alchemy reaching 50 | after PA66 |
| PA69 | L U | E `STAT:Poisons Mixed` reaches 1 | — |
| PA70 | K X | E Alchemy reaching 100 | after C3 |
| PA71 | K U | E `STAT:Ingredients Eaten >= 20` | — |
| PA72 | R U | E `STAT:Magic Items Made` reaches 1 | — |
| PA73 | L R | E po3 `OnSoulTrapped` killer == Player, first time | after B10 |
| PA74 | V R | E Enchanting reaching 50 | after B14-era Val/Remi intro (Remi's HLIOValBanter stage 10) **[nice-to-have]** |
| PA75 | R U | E Enchanting reaching 100 | after PA72 |
| PA76 | X G | E `OnItemCrafted`, bench has `CraftingCookpot` keyword | after X1 |
| PA77 | S X | E `STAT:Potions Mixed +1` with Alchemy >= 50 | SERANA_F; DLC1VQ04 completed |

### Part 7 - The mage
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA78 | L U | E po3 `OnSpellLearned`, spell's first effect school = Destruction (`GetAssociatedSkill() == "Destruction"`) | — |
| PA79 | K U | E `OnSpellLearned` from a tome (po3 `OnBookRead` with `GetSpell()` in the same second), school Restoration | K_CRUSH |
| PA80 | R I | E `OnSpellLearned` from a tome | after B6 |
| PA81 | G L | E `OnSpellLearned`, spell summons a Dremora or flame atronach (FormList of vanilla Conjure Dremora Lord / Conjure Flame Atronach / Flame Thrall SPELs) | after L1 |
| PA82 | R U | E `OnSpellLearned`, a reanimate spell (effect archetype Reanimate) | — |
| PA83 | G V | E `STAT:Books Read` rises by 5 within 24 game hours | after A3 |
| PA84 | L U | E po3 `OnBookRead`, book is The Lusty Argonian Maid v1 or v2 | — |
| PA85 | I U | E `STAT:Skill Books Read +1` | — |
| PA86 | V U | E `OnBookRead`, book in our FormList of history books (Brief History of the Empire, Biography of Tiber Septim / "Arcturian Heresy", etc.) | — |
| PA87 | S U | E `OnBookRead` at NIGHT, CAMP or INN | SERANA_F |
| PA88 | X L | E arrival in a Jarl's palace (CITY + interior with a court wizard NPC within 2000 units) with any magic skill >= 75 | Xelzaz-Lucien intro done (their own quest) **[UNCONFIRMED stage]** |
| PA89 | C I | E `OnSpellLearned` Invisibility | after R13 |
| PA90 | G A | E AFTERFIGHT where the player cast a spell with a Paralysis effect (po3 `OnSpellCast` / `OnMagicHit` source check) | ASHE_F |
| PA91 | K G U | E `OnSpellLearned` of a master-level Destruction spell (Fire Storm / Blizzard / Lightning Storm) | after A1 |

### Part 8 - The voice, the beast and the relics
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA92 | L U | E `STAT:Words Of Power Learned +1` (wall), not the first word | DB |
| PA93 | C G | E `STAT:Shouts Mastered +1` | DB; after R5 |
| PA94 | V K | E `STAT:Times Shouted >= 100` | DB; after A2 |
| PA95 | X U | E po3 `OnDragonSoulGained` with `STAT:Dragon Souls Collected >= 5` | DB |
| PA96 | G V | E `OnDragonSoulGained` with souls >= 10 | DB; after A3 |
| PA97 | L I | E po3 `OnActorKilled`, victim race is a dragon priest race (`DragonPriestRace` and the DLC2 priest races) **[UNCONFIRMED FormIDs]** | — |
| PA98 | K U | E `OnObjectEquipped` of an item in our FormList of dragon priest masks (vanilla 9 + Konahrik + DLC2) | — |
| PA99 | G X | E `STAT:Daedric Artifacts Found >= 5` | after X1 |
| PA100 | A I | E `STAT:Daedric Artifacts Found >= 10` | ASHE_REVEAL |
| PA101 | G K | E `OnRaceSwitchComplete` to WerewolfBeastRace (0CDD84:Skyrim.esm), WILD; fires after 20 s if not in combat | WOLF; after A1 |
| PA102 | C U | E `OnRaceSwitchComplete` back from WerewolfBeastRace, WILD | WOLF |
| PA103 | V I | E `OnRaceSwitchComplete` to DLC1VampireBeastRace (0283A3:Dawnguard.esm), WILD | VAMP; after I1 |
| PA104 | S L | E `OnVampireFeed` (player is the feeder, target asleep) | VAMP; SERANA_F |
| PA105 | C K | E AFTERFIGHT where the Wabbajack was fired and the player's sweet roll count rose by 2+ during the fight **[UNCONFIRMED: detect Wabbajack use via po3 `OnMagicHit`/`OnSpellCast` source == DA03 Wabbajack WEAP; sweetroll outcome inferred from inventory]** | after R1 |
| PA106 | S K | E po3 `OnShoutAttack` in a CITY or LocTypeTown, no combat for 10 s | DB; SERANA_F |
| PA107 | G L | E `STAT:Shouts Learned >= 8` (or Words Of Power Learned >= 8 as fallback) | DB; after L1 |

### Part 9 - What she wears
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA108 | V L | E `OnObjectEquipped` of body-slot (32) Armor never worn before (controller FormList of seen bodies) | after C1; max once per 7 days |
| PA109 | K G | E first `OnObjectEquipped` of an Armor with `ArmorHeavy` keyword in slot 32 | after A1 |
| PA110 | V U | E first `OnObjectEquipped` of a helmet (`ArmorHelmet` keyword or slot 30/31 armour that is not a circlet) | — |
| PA111 | G L | E NAKED | after L1 |
| PA112 | V K | E NAKED | K_CRUSH and V_FLIRT |
| PA113 | S U | E NAKED and SNOW | SERANA_F |
| PA114 | G R | E MARA | UNWED; G_ANY |
| PA115 | V I | E MARA | UNWED; V_FLIRT and `Val00A` stage < 26 (so Val's own amulet beat isn't stepped on) |
| PA116 | S A | E MARA | UNWED; S_ROM and A_ANY; S_VAMP; ASHE_REVEAL |
| PA117 | G V | E MARA (Kaidan not a speaker; his mod reacts itself) | UNWED; K_CRUSH; after A3 |
| PA118 | C U | E MARA | UNWED; plays only if none of PA114-117 qualified this time |
| PA119 | R X | E `OnObjectEquipped` of clothing with `ClothingRich` keyword, in CITY | Remi/Xel not fallen out |

### Part 10 - What she eats and drinks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA120 | K X | E `OnObjectEquipped` (eat) of a Potion with `VendorItemFoodRaw` that is a vegetable (FormList: leek, carrot, cabbage, potato, gourd) | after C3 |
| PA121 | C I | E eat raw meat (FormList of raw meats, or `VendorItemFoodRaw` minus the vegetable list) | after R13 |
| PA122 | G V | E 4+ alcoholic drinks eaten within 1 game hour (FormList of vanilla ales, meads, wines, Sujamma, Flin, Shein, Mazte + Requiem/food-mod alcohol keyword if present), INN | after A3 |
| PA123 | X U | E first safe MORNING tick after PA122's condition was met | — |
| PA124 | I U | E `OnItemAdded` of Skooma (057A7A:Skyrim.esm) or Double-Distilled Skooma, first time | — |
| PA125 | K I | E skooma added again | after PA124; K_I |
| PA126 | C U | E eat Sweetroll (064B3D:Skyrim.esm) | — |
| PA127 | V R | E eat Sweetroll | after B14-era Val/Remi intro; plays if PA126 did not qualify (no Redcap) |

### Part 11 - Getting around
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA128 | X L | E player `IsSwimming()` for 20+ s, then stops swimming (on shore) | Xelzaz-Lucien intro done |
| PA129 | K U | E as PA128, in a snowy hold or `GetTemperature`-style survival check cold **[UNCONFIRMED cold check: use worldspace region list (Pale, Winterhold, Eastmarch, Solstheim north) or Frostfall/Survival exposure if present]** | K_CRUSH |
| PA130 | V R | E po3 `IsActorUnderwater(Player)` for 45+ s, then surfaces | after B14-era Val/Remi intro |
| PA131 | G U | E `IsOnMount()` 120+ s on a road (exterior, moving) | — |
| PA132 | I C | E third separate ride after PA47 | after PA47; after R13 |
| PA133 | L V | E `OnPlayerFastTravelEnd` and the trip started from a carriage (player was in CarriageSystem's driver dialogue in the 30 s before travel) **[UNCONFIRMED: carriage detection method]** | after C1 |
| PA134 | R K | E as PA133 | after B1 |
| PA135 | G R | E `OnPlayerFastTravelEnd(afTravelGameTimeHours >= 24)` not by carriage | — |
| PA136 | L U | E `OnPlayerFastTravelEnd(afTravelGameTimeHours >= 48)` | — |
| PA137 | K U | E po3 `OnLocationDiscovery` three times within 1 game hour, WILD | — |
| PA138 | R K | E SNEAKING (the A9 exception: allowed while the player sneaks), player sneaking 20+ s | after B1 |
| PA139 | A U | E AFTERFIGHT that began with a sneak attack (`STAT:Sneak Attacks +1` before combat state changed) | ASHE_F |
| PA140 | L G | E overencumbered (`GetTotalItemWeight() > CarryWeight`) for the first time | after L1 |
| PA141 | G K | E overencumbered again, 3+ days after PA140 | after PA140 |
| PA142 | R U | E 3+ items dropped to the world (`OnItemRemoved` with `akDestContainer == None`) within 30 s | — |
| PA143 | V C | E any item dropped to the world | after R8 |
| PA144 | I G | E `OnSleepStop(false)` with the bed furniture exterior (bedroll/tent), not LocTypeHabitation, MORNING | after C2 |
| PA145 | A U | E CAMP + NIGHT, player has slept outdoors at least once before (controller flag) | ASHE_REVEAL; ASHE_F |

### Part 12 - Close calls
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA146 | K U | E AFTERFIGHT + LOWHP | K_CRUSH |
| PA147 | G V | E AFTERFIGHT + LOWHP | G_ANY or V_ANY; after A3 |
| PA148 | S U | E AFTERFIGHT + LOWHP | S_ROM; SERANA_F |
| PA149 | A K | E AFTERFIGHT + LOWHP | K_CRUSH; ASHE_REVEAL |
| PA150 | X G | E `OnMagicEffectApply` on the player, effect has `MagicRestoreHealth` keyword, akCaster == Xelzaz | after X1 |
| PA151 | L U | E same, akCaster == Lucien (needs his Healing Hands toggle on) | — |
| PA152 | K G | E `OnMagicEffectApply` on Kaidan's alias, restore-health effect, akCaster == Player | K_CRUSH; after A1 |
| PA153 | R X | E same on Remi's alias, akCaster == Player | Remi/Xel not fallen out |
| PA154 | V U | E `OnSleepStop(false)` outdoors as PA144, and it was raining at sleep start | — |
| PA155 | C K | E `OnSleepStop(true)` outdoors (sleep interrupted), first safe tick after the fight | after R1 |
| PA156 | I U | E NEARDEATH_N >= 3 within 30 game days | — |
| PA157 | R X | E AFTERFIGHT and `STAT:Potions Used` rose by 5+ during the fight | Remi/Xel not fallen out |
| PA158 | K L | E `OnSleepStop(false)` in a location with LocTypeDraugrCrypt that is cleared (`Location.IsCleared()`) | Lucien-Kaidan intro done |
| PA159 | I X | E `STAT:Diseases Contracted +1` | — |
| PA160 | I K U | E CAMP + NIGHT | 40+ PA talks played; K_I |

## Open items to verify at build
- Exact tracked-stat strings (see the note above).
- JAIL_OUT: where each follower framework parks the follower while the player is jailed; reunion only plays if they are actually outside.
- PA8 failed pickpocket detection; PA26 confiscation check; PA39 Gift of Charity FormID; PA97 dragon priest races; PA105 Wabbajack detection; PA129 cold check; PA133/134 carriage detection.
- INNOCENT filter vs Dark Brotherhood and Morag Tong contract kills (must never fire Part 3 for a contract).
- S_ROM Romance04 stage; Val00A stage window for PA115; RelationshipMarriageFIN stage for UNWED.
- po3 Papyrus Extender must be installed and paired (check with houseCARL `housecarl_skse findings='pairing' filter=po3`). Without it, Parts 5-8 fall back to stat deltas only (no spell/school/bench detail).
