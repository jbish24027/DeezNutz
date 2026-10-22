# Triggers - 42 CREATURES AND LOOT (prefix CR, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\42 CREATURES AND LOOT.txt`
Written 2026-10-18. Nothing in the game, profile or mods was touched. Creature facts Luna quotes come from The Dragonborn's Bestiary 1.5.2 entry text (`mods\The Dragonborn's Bestiary\interface\creatures\*\*.json`, read-only). Snow bear / cave bear names come from `Bears of the North.esp` (races BearSnowRace / "Snow Bear", "Cave Bear").

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C) plus **S = Serana**, **A = Ashe**, **U = Luna** (player line, no Free() test).
Gate codes as TRIGGERS.md section 4 and the sheets they come from: `DB`, `KYNES` (30 MAIN QUEST DEEP.md), `SOLST`, `BRYNJAR`, `K_CRUSH`, `K_TOG+`, `G_FLIRT`, `V_FLIRT`, `DG_CAIRN` (20 DAWNGUARD.md), `SERANA_F`, `S_VAMP`, `ASHE_F`, `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_MEDEUS` (49 ASHE.md / 43 WHAT LUNA DOES.md). Every S talk carries `SERANA_F`; every A talk carries `ASHE_F`. **[UNC]** = not verified, check at build.

Every talk here is **E** and **once ever** (played bit). WorldQuiet() and Free() always apply.

## New gate / event codes

- `SIGHT:<what>` = first time ever a live actor matching `<what>` is within 3000 units (exterior) or 1500 (interior) of the player, `Player.HasLOS(actor)`, and not yet in combat with the player or a follower. Polled on the controller's 60 s tick plus `OnLocationChange`, using a cell actor scan (SKSE `Cell.GetNumRefs(62)` / `GetNthRef`, or po3 `FindAllReferencesWithKeyword` / `GetActorsByProcessingLevel` **[UNC which call; po3 is preferred]**). If combat starts before the talk can play, the controller keeps the event and fires it as `AFTERFIGHT:<what>` once, at the normal 8 s combat-end delay. "First sight" talks are short so a scene that gets cut by a fight just ends (scene flag CombatEnd).
- `<what>` by race EditorID where one exists; **by display name** (`GetDisplayName` / base `GetName`, case-insensitive contains) where the variant shares a race. Name matching is safe with Deadly Dragons only if it keeps the vanilla names **[UNC: check Deadly Dragons' renamed variants]**.
- `NOFIGHT:<what>` = matching actor seen (as SIGHT) and still not in combat with the party 20 s later, then leaves 5000 units or loses LOS.
- `AFTERFIGHT:<what>` = TRIGGERS.md; the last combat target (or any killed actor this fight, via po3 `OnActorKilled`) matched `<what>`.
- `ITEM:<form>` = player `OnItemAdded` of that base form (or any form in a FormList), with `AddInventoryEventFilter`. `FROMCONT` = `akSourceContainer != None`. `FROMDEAD` = source container is an Actor with `IsDead()`. First time ever unless noted.
- `READ:<kind>` = po3 `OnBookRead(Book)` of a note that came in under `FROMDEAD`. `<kind>` is decided by a hand-made FormList of vanilla letters / journals **[UNC: build needs the list; fallback: book name contains "Letter" (love) / "Journal" or "Diary" (bandit) and the corpse was in BanditFaction for the journal]**.
- `OPEN:<form>` = Container menu opened on a container ref (SKSE `OnMenuOpen("ContainerMenu")` + `Game.GetCurrentCrosshairRef()`), and that ref `GetItemCount(<form>) > 0` **[UNC: crosshair ref can be None on activation by key; fallback = ITEM with FROMCONT]**.
- `LOC:crypt` = LocTypeDraugrCrypt; `LOC:hive` = LocTypeFalmerHive; `LOC:cave` = LocTypeDungeon interior.
- `NEAR:<obj>` = player within the given units of a ref whose base is in a FormList (`Game.FindClosestReferenceOfAnyTypeInListFromRef`).
- `DRAGONS_KILLED >= n` = controller counter (po3 `OnActorKilled`, victim has ActorTypeDragon) **[UNC: or vanilla stat "Dragon Souls Collected", which misses souls not absorbed]**.
- `BESTIARY >= n` = number of bestiary pages. **[UNC: the Bestiary's SKSE plugin may not expose a count to Papyrus. Fallback: controller counts distinct races (plus the named variants above) killed by the party via `OnActorKilled`.]**
- `BESTIARY_NEW:<what>` = the fallback counter above just added `<what>` for the first time.
- `DUSK` = hour 18..21. `NIGHT`, `CAMP`, `WILD`, `WATER`, `SNOW`, `TOWN` as TRIGGERS.md / 30 MAIN QUEST DEEP.md.

### Match table for `<what>`

| Code | Match |
|---|---|
| dragon | keyword ActorTypeDragon **[UNC FormID]**, any |
| dragon:blood / frost / elder / ancient / revered / legendary | ActorTypeDragon and name contains "Blood Dragon" / "Frost Dragon" / "Elder Dragon" / "Ancient Dragon" / "Revered Dragon" / "Legendary Dragon" |
| dragon:flying | dragon and `IsFlying()` (SKSE Actor) **[UNC function name]** |
| dragon:wall | dragon not flying, not in combat, within 1500 of a word wall ref (base list: the vanilla word wall activators **[UNC FormIDs]**) |
| dragon:perched | dragon not flying, not in combat, 3000..8000 units away, not dragon:wall |
| dragon:vsgiant | dragon whose `GetCombatTarget()` has GiantRace |
| priest | DragonPriestRace **[UNC FormID]**, not in combat |
| giant | GiantRace (with a MammothRace actor within 2000 for CR24) |
| mammoth | MammothRace, 3+ within 3000 for CR25 |
| trollfrost | TrollFrostRace |
| sabrecat | SabreCatRace or SabreCatSnowyRace |
| bear:snow / bear:cave | name contains "Snow Bear" / "Cave Bear" (Bears of the North) |
| bear | BearBrownRace / BearBlackRace / BearSnowRace |
| elk | ElkRace or DeerRace |
| horker / mudcrab / slaughterfish | HorkerRace / MudcrabRace / SlaughterfishRace (incl. DLC variants) |
| fox / hare / chicken / dog / hawk / skeever / wolf | FoxRace / HareRace / ChickenRace / DogRace (not a follower, not in PlayerFaction) / HawkRace **[UNC: confirm hawks are actors]** / SkeeverRace / WolfRace |
| wisp / wispmother | name "Wisp" / "Wispmother" **[UNC race EditorID]** |
| chaurus / reaper | ChaurusRace / ChaurusReaperRace |
| falmer | FalmerRace |
| deathlord | DraugrRace and name contains "Deathlord" |
| deathhound | DLC1DeathHoundRace |
| icewraith / spriggan / hagraven / centurion | IceWraithRace / SprigganRace / HagravenRace / DwarvenCenturionRace |
| netch | DLC2NetchRace **[UNC EditorID]** |

### Items used (all **[UNC FormIDs]** unless marked; confirm with housecarl_records at build)

DragonBone (Skyrim.esm 03ADA4 [UNC]), DragonScales (03ADA3 [UNC]), the masks Krosis / Vokun / Nahkriin / Morokei / Hevnoraak / Konahrik (match by name), MammothCheese bowl, GiantToe, MammothTusk, HorkerMeat, HorkerTusk, Pearl + SmallPearl (Dragonborn.esm), ChaurusEggs, Taproot, BoneMeal, VampireDust, SoulGemBlackFilled (filled black gem), SoulGemBlack (empty), SoulGemGrand / SoulGemGrandFilled, TGCrownGemInventory (unusual gem / Stone of Barenziah), GemSapphireFlawless, Gold001, SweetRoll, MeadBlackBriar, Skooma, the vanilla treasure maps (TreasMap01..11 books), the dragon claws other than the Golden Claw (Ivory, Coral, Diamond, Ebony, Emerald, Glass, Iron, Ruby, Sapphire), Dwemer gears / cogs misc list (DwarvenGear, DwarvenCog... misc scrap), weapons by keyword WeapMaterialDaedric / WeapMaterialGlass.

## Table

### Part 1 - Dragons in the sky
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR1 | K L U | E `NOFIGHT:dragon:flying` (first ever) | DB |
| CR2 | G U | E `NOFIGHT:dragon:flying`, hour 5..7 or 18..20, distance > 4000 | DB; after CR1 |
| CR3 | X R | E `NOFIGHT:dragon:flying` | DB; after CR1 |
| CR4 | L U | E `SIGHT:dragon:wall` | DB |
| CR5 | R U | E `SIGHT:dragon:blood` | DB |
| CR6 | X A | E `SIGHT:dragon:frost` | DB; ASHE_REVEAL |
| CR7 | V U | E `SIGHT:dragon:elder` | DB |
| CR8 | C K | E `SIGHT:dragon:revered` | DB |
| CR9 | S L | E `SIGHT:dragon:ancient` | DB; SERANA_F |
| CR10 | K G | E `SIGHT:dragon:legendary` | DB; BRYNJAR |
| CR11 | I C | E `SIGHT:dragon:perched` | DB |
| CR12 | X U | E `AFTERFIGHT:dragon` | DB; `DRAGONS_KILLED >= 2` **[UNC: no hook for "the dragon spoke first"; any dragon fight after the first]** |
| CR13 | V C | E `SIGHT:dragon:vsgiant` (fires while the two fight; party not yet engaged) | DB **[UNC: fires mid-combat between NPCs; WorldQuiet only checks the player's combat, so OK if the player hasn't drawn]** |
| CR14 | I U | E dragon soul absorbed (`SOUL`, as 30 MAIN QUEST DEEP.md) | DB |
| CR15 | V I | E `NEAR:dragon mound (opened)` 1000 | KYNES **[UNC: base FormIDs of the opened-mound static/activator; fallback: any dragon mound map marker location after KYNES]** |
| CR16 | L X | E CAMP | `DRAGONS_KILLED >= 10` |

### Part 2 - The dragon cult
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR17 | X S | E `SIGHT:priest` (before combat) | SERANA_F |
| CR18 | K U | E `ITEM:` Krosis | — |
| CR19 | V I | E `ITEM:` Vokun | — |
| CR20 | A U | E `ITEM:` Nahkriin | ASHE_REVEAL; ASHE_Q1 (her vengeance story is known) |
| CR21 | L U | E `ITEM:` Morokei | — |
| CR22 | G V | E `ITEM:` Hevnoraak | — |
| CR23 | K G U | E `ITEM:` Konahrik | — |

### Part 3 - Giants, mammoths and big fur
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR24 | V L | E `SIGHT:giant` with a mammoth near, distance > 2000, not hostile yet | — |
| CR25 | C X | E `SIGHT:mammoth` (3+), distance < 1500, not in combat | — |
| CR26 | X S | E `ITEM:` mammoth cheese | SERANA_F |
| CR27 | L X | E `ITEM:` GiantToe | — |
| CR28 | G R | E `ITEM:` MammothTusk | — |
| CR29 | C U | E `SIGHT:trollfrost` | — |
| CR30 | I K | E `SIGHT:sabrecat` | — |
| CR31 | A G | E `SIGHT:sabrecat` (first after the gate) | ASHE_MEDEUS |
| CR32 | G K U | E `AFTERFIGHT:sabrecat` | K_CRUSH and G_FLIRT |
| CR33 | K U | E `SIGHT:bear:snow` | — |
| CR34 | L G | E `SIGHT:bear:cave` in LOC:cave | — |
| CR35 | G I | E `SIGHT:bear` while that bear `IsInWater` or within 300 of water **[UNC: no "fishing" check; po3 `IsActorInWater` on the bear, or a WATER-tagged cell]** | — |
| CR36 | I V | E bear within 2500 and `Player.HasLOS(bear) == false`, not in combat | — |
| CR37 | R K | E `SIGHT:elk` within 1500, then its distance grows by 1000+ within 5 s and no combat **[UNC: flee detection]** | — |

### Part 4 - Shore and stream
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR38 | K V U | E `SIGHT:horker` (alive, not in combat) | — |
| CR39 | A K | E `ITEM:` HorkerMeat | K_CRUSH; ASHE_REVEAL |
| CR40 | X V | E `AFTERFIGHT:mudcrab` | — |
| CR41 | G U | E `AFTERFIGHT:slaughterfish` while player `IsSwimming()` or in WATER | — |
| CR42 | V K U | E `ITEM:` Pearl or SmallPearl | V_FLIRT and K_CRUSH |
| CR43 | K R | E `ITEM:` HorkerTusk | K_TOG+ |

### Part 5 - Small and suspicious
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR44 | I U | E `SIGHT:fox` within 1500 | — |
| CR45 | I X | E `SIGHT:hare` within 1500 | — |
| CR46 | I A | E `BESTIARY_NEW:chicken` (or first chicken killed by the party) | ASHE_HIRED |
| CR47 | K C U | E `SIGHT:dog` (not a follower, not hostile) stays within 800 of the player for 60 s while WILD and player moving | — |
| CR48 | S C | E dog (any, not a follower) within 600 of Serana and in alarm/bark state **[UNC: no bark hook; fallback = dog within 600 of Serana in TOWN]** | S_VAMP |
| CR49 | I R | E `NEAR:` dragonfly critter activators 800 **[UNC: critter base FormIDs; vanilla dragonflies are Critter activators, not actors]** | — |
| CR50 | K L U | E `NEAR:` luna moth critters 800, DUSK or NIGHT **[UNC same]** | K_CRUSH |
| CR51 | C L | E NIGHT, WILD, `SIGHT:wolf` at 2500..5000 and no combat for 30 s **[UNC: no howl hook]** | — |
| CR52 | S R | E `SIGHT:skeever` | — |
| CR53 | G R | E `SIGHT:hawk` | — |
| CR54 | G I | E WILD and `NEAR:` gibbet / hanging cage statics 1200 **[UNC base FormIDs; crows are not actors]** | — |
| CR55 | G C | E `NEAR:` bear trap 400 (BearTrap activator base **[UNC]**) | — |

### Part 6 - In the dark
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR56 | I L | E `SIGHT:wisp`, NIGHT, distance > 1500 | — |
| CR57 | V L | E `SIGHT:chaurus` | — |
| CR58 | V A | E `SIGHT:reaper` | after CR57 |
| CR59 | X V | E `ITEM:` ChaurusEggs | — |
| CR60 | K L | E `SIGHT:chaurus` in LOC:hive, not in combat **[UNC: no "pen" check; LOC:hive is the proxy]** | — |
| CR61 | S I | E `SIGHT:falmer` | SERANA_F |
| CR62 | A R | E `SIGHT:deathlord` | ASHE_REVEAL |
| CR63 | C U | E `AFTERFIGHT:deathlord`, and the player was hit by a shout that fight (po3 `OnMagicHit` with a Shout source, or the deathlord cast a VoicePower) **[UNC]** | DB |
| CR64 | K S | E `SIGHT:deathhound` | SERANA_F |
| CR65 | G X | E `AFTERFIGHT:wispmother` | — |
| CR66 | A U | E `AFTERFIGHT:icewraith` | ASHE_REVEAL |
| CR67 | I S | E `SIGHT:spriggan` | SERANA_F |
| CR68 | X A | E `ITEM:` Taproot, FROMDEAD | ASHE_REVEAL |
| CR69 | C A | E `SIGHT:hagraven` | ASHE_REVEAL |
| CR70 | R G | E `SIGHT:centurion` | — |
| CR71 | R U | E `ITEM:` Dwemer gear/cog misc list, FROMCONT or loose pickup, in LocTypeDwarvenAutomatons | — |

### Part 7 - Loot
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR72 | X K | E `ITEM:` DragonBone | DB |
| CR73 | R A | E `ITEM:` DragonBone (any later one) | DB; ASHE_REVEAL |
| CR74 | C L | E `ITEM:` DragonScales, exterior and SNOW or snow region **[UNC: snow-ground check; fallback any exterior]** | DB |
| CR75 | K U | E `ITEM:` weapon with WeapMaterialDaedric, FROMDEAD, not in the Daedric artifact list | — |
| CR76 | A S U | E `ITEM:` SoulGemBlackFilled, FROMCONT (not filled by the player: controller ignores gems that were already in the player's inventory as empty) | DG_CAIRN; ASHE_Q1; SERANA_F |
| CR77 | X I | E `ITEM:` SoulGemBlack (empty) | NOT DG_CAIRN |
| CR78 | R C | E `ITEM:` SoulGemGrand or SoulGemGrandFilled | — |
| CR79 | V U | E `ITEM:` TGCrownGemInventory | — |
| CR80 | G K U | E `ITEM:` GemSapphireFlawless | K_CRUSH |
| CR81 | G L | E `ITEM:` Gold001 count >= 100 FROMCONT in LOC:crypt | — |
| CR82 | V S | E `ITEM:` Gold001 count >= 500 in one pickup | SERANA_F |
| CR83 | L R | E `OPEN:` any container within 2000 of a word wall ref, exterior | DB **[UNC: lair chest = nearest container to the wall]** |
| CR84 | S K | E `ITEM:` any dragon claw except the Golden Claw | SERANA_F |
| CR85 | S L | E `ITEM:` VampireDust | SERANA_F |
| CR86 | X C | E `ITEM:` BoneMeal | — |
| CR87 | C V | E `ITEM:` weapon with WeapMaterialGlass | — |

### Part 8 - On bodies and in chests
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR88 | I R | E `OPEN:` Skooma (container, not a corpse) | — (distinct from PA124: that one is skooma entering the pack) |
| CR89 | C S | E `ITEM:` SweetRoll FROMCONT in LOC:crypt | SERANA_F |
| CR90 | S K | E `ITEM:` MeadBlackBriar FROMCONT in LOC:crypt | SERANA_F |
| CR91 | V G | E `READ:love letter` | — (letter text in the talk is flavour; Val paraphrases) |
| CR92 | U K R | E `READ:bandit journal` | — |
| CR93 | V A | E `ITEM:` any, FROMCONT where the container is a coffin, or taken from an altar/ritual container in LocTypeWarlockLair / LocTypeVampireLair **[UNC: coffin container base list]** | ASHE_HIRED |
| CR94 | V U | E `ITEM:` any treasure map | — |
| CR95 | A L | E `OPEN:` a dead NPC the party did not kill (not in the controller's kill log), in LOC:cave or LOC:crypt, carrying 2+ healing potions (keyword MagicAlchRestoreHealth) **[UNC: "adventurer" = any non-hostile-faction dead NPC placed dead]** | ASHE_HIRED |

### Part 9 - Luna's bestiary
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CR96 | A U | E CAMP | `BESTIARY >= 25`; ASHE_REVEAL |
| CR97 | C U | E CAMP | `BESTIARY_NEW:` any of spriggan / draugr / falmer / centurion / giant / skeleton (Redcap has fa-ka names for these) |
| CR98 | L U | E CAMP or INN | `BESTIARY >= 40` |
| CR99 | I U | E CAMP | after CR98 |
| CR100 | R U | E `SIGHT:netch` | SOLST |

## Open items to check at build
- Every `[UNC]` FormID and race EditorID in the match table and item list.
- `IsFlying()` availability for CR1-3 (SKSE vs po3).
- Word wall, dragon mound, gibbet, bear trap and critter base-form lists for the `NEAR:` events.
- Whether the Dragonborn's Bestiary exposes its page count; otherwise use the kill-count fallback.
- CR13 and CR83 fire close to dragons; make sure the 8 s combat-end delay and WorldQuiet() don't let them overlap a live dragon attack on the party.
