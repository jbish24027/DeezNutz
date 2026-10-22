# Triggers - 42b CREATURES AND LOOT 2 (prefix CR, CR101-CR200, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\42b CREATURES AND LOOT 2.txt`
Written 2026-10-18. Writing only: nothing in the game, profiles or mods was touched.

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C) plus **S = Serana**, **A = Ashe**, **U = Luna** (player line, no Free() test).
Every talk here is **E** and **once ever** (played bit). WorldQuiet() and Free() always apply. Every S talk also carries `SERANA_F`; every A talk carries `ASHE_F`.

Event and gate codes reuse part 1 (`triggers\42 CREATURES AND LOOT.md`): `SIGHT:<what>`, `NOFIGHT:<what>`, `AFTERFIGHT:<what>`, `ITEM:<form>`, `FROMCONT`, `FROMDEAD`, `READ:<kind>`, `OPEN:<form>`, `NEAR:<obj>`, `LOC:crypt/hive/cave`, `DRAGONS_KILLED >= n`, `BESTIARY >= n`, `BESTIARY_NEW:<what>`, `DUSK`, `NIGHT`, `PREDAWN`, `CAMP`, `WILD`, `WATER`, `SNOW`, `RAIN`, `TOWN`, and the gates `DB`, `SOLST`, `PAARTH`, `K_CRUSH`, `K_TOG+`, `S_VAMP`, `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `LUC_ADMIT`, `VAL_FATHIS`, `INIGO_BV`, `RC_MANOS`. **[UNC]** = not verified, check at build.

## New codes

- `AFTERFIGHT:dragon:<kind>` (first time) = part 1's name match on the killed dragon (po3 `OnActorKilled`), first kill of that kind ever. `<kind>` adds `skeletal` (race `DLC1SkeletalDragonRace` **[UNC EditorID; confirm skeletal dragons spawn in this order]**) and `serpentine` (name contains "Serpentine Dragon", Dragonborn.esm **[UNC]**).
- `DRAGONS_IN_FIGHT >= 2` = two or more ActorTypeDragon actors were in combat with the party during one player combat. Controller keeps a set during combat **[UNC: needs combat-target polling or po3 OnCombatStateChanged on the dragons]**.
- `DRAGON:crashed` = a dragon killed while `IsFlying()` was true at the hit that killed it **[UNC: poll IsFlying on the 60 s tick is too slow; fallback = any dragon kill, talk lines still fit]**.
- `DRAGON:vsmammoth` = a dead MammothRace actor within 2000 of a dragon that is in combat or dead, with no party hits on the mammoth **[UNC; fallback: dead mammoth seen within 2 game hours of a dragon kill nearby]**.
- `SOULS >= n` = dragon souls absorbed (vanilla stat "Dragon Souls Collected" or the controller's SOUL counter).
- `CITYDRAGON` = AFTERFIGHT:dragon while the player is in, or within 3000 units of, a hold capital location and at least one guard (GuardFaction / IsGuard) was in combat with the dragon.
- `SEEN:<list>` = the bestiary fallback counter (part 1) holds every kind in the list.
- `HERD:elk` = 3+ ElkRace actors within 3000, all fleeing or running, no combat.
- `STAG` = SIGHT:elk where the elk is male **[UNC: ElkRace male check; fallback any elk that stays 20 s within 2500 with no combat and no flee]**.
- `CLIFFGOAT` = SIGHT of GoatRace where the goat's Z is 400+ units above the player and within 2500 **[UNC: crude, but cliff goats sit high]**.
- `RIDERLESS` = a horse with a saddle, no rider, not the player's or a follower's, within 1500 of a dead actor (vanilla WEJS24 encounter is the main source) **[UNC]**.
- `CRITTER:<kind>` = `NEAR:` critter activator base list: butterflies (monarch, blue), dragonflies (blue, orange dartwing), luna moth, torchbug, salmon (jumping fish critters) **[UNC: critter base FormIDs]**.
- `CATCH:torchbug` = `ITEM:` TorchbugThorax while a torchbug critter was within 300 a moment before (i.e. caught, not bought).
- `FARM:<animal>` = SIGHT of ChickenRace / CowRace within 1500, in a location with LocTypeFarm or LocTypeHabitation exterior.
- `STEAMVENT` = in LocTypeDwarvenAutomatons, player within 300 of a steam vent hazard ref **[UNC: steam trap/vent base list]**.
- `DORMANT:centurion` = Dwarven centurion actor that is not yet active (still in its ambush furniture/alcove) within 1500 **[UNC: check AI state, e.g. `GetSitting` or package]**.
- `SPHERE:unfold` = SIGHT of a Dwarven sphere actor that just left its pipe (first combat start with a sphere) **[UNC; fallback AFTERFIGHT:sphere, line still fits]**.
- `SLEEPBEAR` = `bear:cave` actor with `GetSleepState() == 3` and not in combat while the player is sneaking. **This talk overrides the WorldQuiet sneak block, like A9 (SNEAKING).**
- `WEBROOM` = interior cell (LOC:cave) with 3+ web statics within 2000 and a frostbite spider race present **[UNC: web static base list]**.
- `COCOON` = `NEAR:` web-wrapped corpse static or cocoon container 800 **[UNC base list]**.
- `TROPHYPILE` = LocTypeAnimalDen interior with a troll or bear present or dead, and 4+ loose helmets/shields lying in the cell **[UNC: fallback = any LocTypeAnimalDen with a troll]**.
- `SKELPAIR` = two skeleton statics or dead skeleton actors within 150 of each other, in LOC:cave or LOC:crypt **[UNC: needs a hand-made static list; fallback: drop the talk if no list]**.
- `BONESWORD` = `NEAR:` dragon skeleton static with an embedded sword (several vanilla dragon-skeleton set pieces have one) 1000 **[UNC base list]**.
- `MAMMOTHGRAVE` = `NEAR:` mammoth skeleton / mammoth skull static 1000, exterior.
- `RAREBOOK` = `ITEM:` a book with gold value >= 100 that is not a spell tome or skill book **[UNC: value threshold]**. `RAREBOOKS >= 3` counts these.
- `DWEMERBOOK` = `ITEM:` a book from a hand list of Dwemer-subject books, in LocTypeDwarvenAutomatons **[UNC list]**.
- `NECROBOOK` = `ITEM:` any book FROMCONT in LocTypeWarlockLair, from a container within 500 of a necromancer altar or with a necromancer corpse nearby **[UNC]**.
- `TOMEFROMDEAD` = `ITEM:` any spell tome FROMDEAD, victim not in the controller's kill log.
- `LASTLETTER` / `DOORWARNING` / `VAMPDIARY` / `TORNBOOK` = `READ:` of a note from a hand list **[UNC lists; letter and journal text in the talks is flavour, Luna and Lucien paraphrase]**.
- `CURSEDRING` = `ITEM:` a ring FROMCONT or FROMDEAD in LOC:crypt whose enchantment has a hostile or Damage effect **[UNC: needs a list; vanilla has few]**.
- `TOY` = `ITEM:` HearthFires Doll or Wooden Sword picked up in a dungeon location **[UNC: these are rarely placed in dungeons; may need our plugin to place one doll in a vanilla tomb, or drop the talk]**.
- `GIANTGOLD` = `OPEN:` a container in LocTypeGiantCamp holding Gold001.
- `TREASUREDUG` = `OPEN:` a container whose ref is one of the vanilla treasure-map chests **[UNC ref list, 11 maps]**.
- `LUTE` = `ITEM:` Lute (or Lute misc variants) FROMCONT or loose in a dungeon location.
- `K_AKAVIRI` = Kaidan's KINV "All of this Past" quest completed (he knows his mother's Akaviri line and has her letter) **[UNC: completion stage]**.
- `GORE_READS` = HLIOGoreReading (6F46A0:HLIORemi.esp) >= 1, or HD1MemoriesQ completed (he says he learned to read in the Vigilant arc) **[UNC which value means "started"]**.
- `REMI_XEL_OK` = BPUFXelzazRemielFallenOut (5EB8BC) != 1 and the falling-out quest not between stages 11 and 13.

## Table

### Part 1 - Dragons, the second time
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR101 | R G | E `AFTERFIGHT:dragon:blood` (first) | DB |
| CR102 | X K | E `AFTERFIGHT:dragon:frost` (first) | DB |
| CR103 | V U | E `AFTERFIGHT:dragon:elder` (first) | DB |
| CR104 | A G | E `AFTERFIGHT:dragon:ancient` (first) | DB; ASHE_REVEAL |
| CR105 | L U | E `AFTERFIGHT:dragon:revered` (first) | DB |
| CR106 | K U | E `AFTERFIGHT:dragon:legendary` (first) | DB |
| CR107 | S C | E `SIGHT:dragon:skeletal` | SERANA_F |
| CR108 | I G | E `NOFIGHT:dragon:flying` while RAIN | DB; after CR1 |
| CR109 | V X | E AFTERFIGHT with `DRAGONS_IN_FIGHT >= 2` | DB |
| CR110 | K C U | E `AFTERFIGHT:dragon` + `DRAGON:crashed` | DB |
| CR111 | R U | E CAMP | DB; `SOULS >= 20` |
| CR112 | V G | E `CITYDRAGON` | DB |
| CR113 | C G | E `DRAGON:vsmammoth` | DB |
| CR114 | V A | E `SIGHT:dragon:serpentine` | DB; SOLST; ASHE_REVEAL |
| CR115 | G K U | E CAMP | DB; `DRAGONS_KILLED >= 25` |
| CR116 | A U | E CAMP | DB; `SEEN:` any 3 of dragon:blood/frost/elder/ancient/revered/legendary; ASHE_REVEAL |

### Part 2 - Cold country
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR117 | A I | E `SIGHT:` ice wolf (name contains "Ice Wolf", WolfRace) in SNOW or snow region | ASHE_Q1 (Canas met) |
| CR118 | I L | E `WEBROOM` (first) | — |
| CR119 | R V | E `COCOON` (first) | — |
| CR120 | X U | E `ITEM:` FrostbiteVenom (first) | — |
| CR121 | C L | E `SLEEPBEAR` in LOC:cave | — (sneak override) |
| CR122 | K X U | E CAMP | `SEEN:` bear:snow, bear:cave, and BearBrownRace |
| CR123 | S U | E `HERD:elk`, exterior | SERANA_F |
| CR124 | G I | E `STAG` | — |
| CR125 | C K | E `CLIFFGOAT` | — |
| CR126 | L V | E `RIDERLESS` | LUC_ADMIT |
| CR127 | K U | E PREDAWN (hour 4..6), `SIGHT:` DeerRace within 1500, no flee for 10 s | K_TOG+ |
| CR128 | X S | E `ITEM:` ice wolf pelt (first) **[UNC FormID: confirm the pelt exists in this order]** | SERANA_F |

### Part 3 - Wings, fins and farmyards
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR129 | A R | E `CRITTER:butterfly` 800, not RAIN/SNOW | ASHE_Q1 (Canas met) |
| CR130 | I C | E `CRITTER:dragonfly` 800 near WATER | RC_MANOS; after CR49 |
| CR131 | I L | E `CATCH:torchbug`, NIGHT | — |
| CR132 | G X | E `CRITTER:lunamoth` 800, DUSK or NIGHT | GORE_READS |
| CR133 | K G U | E `SIGHT:hawk` | after CR53 |
| CR134 | I X | E `FARM:chicken` | — |
| CR135 | S R | E `FARM:cow` | S_VAMP |
| CR136 | V X | E `AFTERFIGHT:slaughterfish` | — |
| CR137 | G U | E `CRITTER:salmon` 1500 (jumping salmon at falls) | — |

### Part 4 - Dwemer machines
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR138 | R L | E `SPHERE:unfold` (first) | — |
| CR139 | C K | E `AFTERFIGHT:sphere` (DwarvenSphereRace, first) | — |
| CR140 | X C | E `STEAMVENT` | — |
| CR141 | A V | E `DORMANT:centurion` | ASHE_Q1 |
| CR142 | I R | E `SIGHT:` DwarvenSpiderRace (first) | — |
| CR143 | K L | E `AFTERFIGHT:centurion` (first) | — |
| CR144 | C L U | E `ITEM:` any Dwarven helmet (ArmorDwarven keyword + ArmorHelmet) | — |

### Part 5 - Blades with names
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR145 | V G | E `ITEM:` Wuuthrad | — |
| CR146 | X U | E `ITEM:` Chillrend | — |
| CR147 | K U | E `ITEM:` Dragonbane | K_AKAVIRI |
| CR148 | K I | E `ITEM:` Bolar's Oathblade | — |
| CR149 | G L | E `ITEM:` Eduj | — |
| CR150 | V S | E `ITEM:` any of the Gauldurson weapons (Gauldur Blackblade / Blackbow / Blacksword **[UNC exact list]**) | VAL_FATHIS; SERANA_F |
| CR151 | S I | E `ITEM:` Ghostblade | SERANA_F |
| CR152 | V A | E `ITEM:` Valdr's Lucky Dagger | ASHE_HIRED |
| CR153 | G K | E `ITEM:` Notched Pickaxe | PAARTH |
| CR154 | I U | E `ITEM:` Zephyr (Dawnguard.esm) | — |

### Part 6 - Ore and stones
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR155 | K V | E `ITEM:` IngotEbony (first) | — |
| CR156 | R G | E `ITEM:` IngotDwarven in LocTypeDwarvenAutomatons | — |
| CR157 | S V | E `ITEM:` GemDiamondFlawless (first) | SERANA_F |
| CR158 | C X | E `ITEM:` GemEmerald or GemEmeraldFlawless (first) | — |
| CR159 | C R | E `ITEM:` GemGarnet or GemGarnetFlawless (first) | — |
| CR160 | S A | E `ITEM:` IngotSilver (first after both gates) | S_VAMP; ASHE_REVEAL |
| CR161 | R S | E `ITEM:` aetherium shard (DLC1 Lost to the Ages) | SERANA_F |

### Part 7 - Found in the dark
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR162 | R L | E `DWEMERBOOK` | — |
| CR163 | R U | E CAMP | `RAREBOOKS >= 3` |
| CR164 | V U | E `RAREBOOK` | — |
| CR165 | L U | E `TOMEFROMDEAD` | — |
| CR166 | K U | E `NECROBOOK` | — |
| CR167 | G U | E `READ:` "Kolb and the Dragon" | GORE_READS |
| CR168 | V C | E `TREASUREDUG` | — (part 1 CR94 is the map pickup; this is the dig) |
| CR169 | R K | E `CURSEDRING` | — |
| CR170 | A U | E `LASTLETTER` | ASHE_REVEAL |
| CR171 | S I | E `TOY` | SERANA_F |
| CR172 | I U | E `SKELPAIR` | INIGO_BV (he has met Langley, who found his parents) |
| CR173 | A L | E `NEAR:` Nirnroot / Crimson Nirnroot plant 600 | ASHE_REVEAL |
| CR174 | X K | E `ITEM:` WispWrappings | — |
| CR175 | R X | E `ITEM:` BriarHeart | REMI_XEL_OK |
| CR176 | S L | E `ITEM:` Ectoplasm | SERANA_F |
| CR177 | C A | E `ITEM:` DragonsTongue (harvested) | ASHE_HIRED |
| CR178 | V K | E `ITEM:` ElvesEar (harvested) | — |
| CR179 | G L U | E `DOORWARNING` | — |
| CR180 | K A | E `TROPHYPILE` | ASHE_HIRED |

### Part 8 - The bestiary, volume two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR181 | L U | E CAMP or INN | `BESTIARY >= 80`; after CR98 |
| CR182 | K U | E CAMP | K_CRUSH; `BESTIARY >= 30` |
| CR183 | R U | E CAMP | `BESTIARY_NEW:` Dwarven spider |
| CR184 | C U | E CAMP | after CR97 (at least 2 game days later) |
| CR185 | X U | E CAMP | `BESTIARY >= 50` |

### Part 9 - Old beasts, new angles
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR186 | G R U | E `MAMMOTHGRAVE` | — |
| CR187 | C V | E `ITEM:` HagravenFeathers (first) | — |
| CR188 | L X | E `ITEM:` FalmerEar (first) | — |
| CR189 | V L | E `SIGHT:` chaurus hunter (DLC1 ChaurusHunterRace **[UNC EditorID]**) | after CR58 |
| CR190 | I R | E `ITEM:` SpiderEgg (first) | — |
| CR191 | C G | E `ITEM:` BeeHoneycomb or a bee-hive harvest **[UNC: honeycomb vs hive husk form]** | — |
| CR192 | A S | E `SIGHT:` SabreCatSnowyRace (first) | ASHE_HIRED; SERANA_F |
| CR193 | K I | E `CRITTER:dragonfly` 800 near WATER | after CR49 |

### Part 10 - Last finds
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR194 | K S | E `BONESWORD` | DB; SERANA_F |
| CR195 | S G | E `TORNBOOK` | GORE_READS; SERANA_F |
| CR196 | G I | E `LUTE` | — |
| CR197 | A I | E `ITEM:` any flawed gem (GemAmethyst, GemGarnet, GemRuby, GemSapphire, GemEmerald, GemDiamond base forms, not the flawless ones) | ASHE_REVEAL |
| CR198 | S U | E `VAMPDIARY` in LocTypeVampireLair | SERANA_F |
| CR199 | C I | E `GIANTGOLD` | — |
| CR200 | C K U | E CAMP | K_TOG+; after CR181 |

## Notes for the build
- CR197 fires on the first flawed gem; CR159 (garnet) and CR158 (emerald) fire on their own first pickups. If one pickup qualifies for two talks, the controller plays only one and keeps the other for the next qualifying pickup.
- CR130 and CR193 share the dragonfly event; they need different played bits and the 300 s cooldown between them.
- CR121 needs the same sneak-block override as A9; keep the talk short (it is).
- CR147: Luna's lines are branch-neutral; nobody takes the sword from her.
- CR172 and CR171 are serious; skip if the drunk flag or any comic talk played in the last 60 s.
- Open items: every `[UNC]` list and FormID above; whether skeletal dragons spawn in this load order (if not, CR107 never fires and that is fine); Deadly Dragons renames (part 1 note) also affect CR101-CR106.
