# 57 INNS AND TOWN LIFE - trigger rows (prefix IN, 150 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\57 INNS AND TOWN LIFE.txt`. Written 2026-10-18.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` (sections 2-4), `triggers\20 DAWNGUARD.md` (Serana/Ashe Free rows and S_/A_/SER_ codes), `triggers\41 FAMOUS NPCS.md` (`NEAR:` / `TALKED:`), `triggers\43 WHAT LUNA DOES.md` (player-event hooks, `READING`, beggar coin), `triggers\45 PARTY LIFE.md` (file-wide rules copied), `research\bibles\*.md`, `research\content\00_inventory.md` (mod plugins).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build. Nothing in the game, profile or mods folder was touched.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player out of dialogue and out of menus).

## 1. File-wide rules
- **Meets first.** Every row also needs each follower pair in it to have played its "meets" talk (TRIGGERS.md chain rule). Rows that say "<A>-<B> own intro done" mean the pair's intro scene in one of their own mods (Remi's HLIO*Banter quests, Xelzaz's BPUFXelzazAnd*Interactions, Lucien's JRLucien* scenes, KaiandInigo stage >= 10) instead of one of ours.
- **Serana rows** need her Free row (20 DAWNGUARD.md section 1). `SERANA_F` = that Free row. Rows with vampire jokes add `SER_VAMP`.
- **Ashe rows** all carry `ASHE_REVEAL` (Ashe is open about being an automaton only after the reveal). Respect her `bConfigVarIdles` toggle (her Free row).
- **Low priority.** Town-life talks are filler: if a quest, place or romance talk from another file is eligible on the same event, that one wins. At most **one IN talk per inn visit** and **one IN talk per city visit outdoors**, so walking into an inn never stacks two of these.
- **Named-inn rows** (`INN:<Name>`) win over generic `INN` rows from this file on the same visit, until each named-inn row has played once.
- `ONCE` = the row never repeats even if the played bit is cleared by a reset (IN122 only; the arrow-in-the-knee joke is single-use by the user's request).
- No talk here mentions Kaidan's cult, Jo-Lee as Gore's father, Fathis, Mora, Morvic or Thorfinn's quest outcome. Brynjar appears only in IN147 (gated `BRYNJAR`). Clive appears only in rows gated `LUC_ADMIT`. Nobody says "Dragonborn".

## 2. Event and gate codes used here (new ones marked NEW)
Existing (TRIGGERS.md section 4, 20 DAWNGUARD.md, 41/43/45 trigger sheets): `INN`, `CITY:<Name>`, `NIGHT`, `MORNING`, `SNOW`, `WILD`, `K_CRUSH`, `K_TOG+`, `K_ANY`, `K_MAR`, `G_FLIRT`, `G_ANY`, `V_ANY`, `S_KISS`, `A_CRUSH`, `SERANA_F`, `SER_VAMP`, `ASHE_REVEAL`, `DB`, `GORE_BAIL`, `VAL_FATHER`, `LUC_ADMIT`, `BRYNJAR`, `RC_MANOS`, `after:X`, `NEAR:<NPC>` and `TALKED:<NPC>` (41), `READING` (43: po3 `OnBookRead` fired in the last 60 s), `BEGGAR_COIN` (43, PA39's event: player receives the vanilla beggar reward "Gift of Charity" **[UNC SPEL FormID]**).

Places and moments (NEW):
- `INN:<Name>` = player `GetInCurrentLocation` that inn's location (or a child of it), first tick after entering. Location EditorIDs to look up at build **[UNC, all of them; confirm with housecarl_records on Skyrim.esm LCTN]**:

| Code | Inn | Likely location EditorID |
|---|---|---|
| BanneredMare | Bannered Mare, Whiterun | WhiterunBanneredMareLocation |
| DrunkenHuntsman | The Drunken Huntsman, Whiterun | WhiterunDrunkenHuntsmanLocation |
| SleepingGiant | Sleeping Giant Inn, Riverwood | RiverwoodSleepingGiantInnLocation |
| WinkingSkeever | The Winking Skeever, Solitude | SolitudeWinkingSkeeverLocation |
| Candlehearth | Candlehearth Hall, Windhelm | WindhelmCandlehearthHallLocation |
| Cornerclub | New Gnisis Cornerclub, Windhelm | WindhelmNewGnisisCornerclubLocation |
| BeeAndBarb | The Bee and Barb, Riften | RiftenBeeandBarbLocation |
| SilverBlood | Silver-Blood Inn, Markarth | MarkarthSilverBloodInnLocation |
| DeadMansDrink | Dead Man's Drink, Falkreath | FalkreathDeadMansDrinkLocation |
| Moorside | Moorside Inn, Morthal | MorthalMoorsideInnLocation |
| Windpeak | Windpeak Inn, Dawnstar | DawnstarWindpeakInnLocation |
| FrozenHearth | The Frozen Hearth, Winterhold | WinterholdFrozenHearthLocation |
| Nightgate | Nightgate Inn | NightgateInnLocation |
| Braidwood | Braidwood Inn, Kynesgrove | KynesgroveBraidwoodInnLocation |
| Vilemyr | Vilemyr Inn, Ivarstead | IvarsteadVilemyrInnLocation |
| OldHroldan | Old Hroldan Inn | OldHroldanInnLocation |
| FourShields | Four Shields Tavern, Dragon Bridge | DragonBridgeFourShieldsTavernLocation |
| Frostfruit | Frostfruit Inn, Rorikstead | RoriksteadFrostfruitInnLocation |
| OlavsTapAndTack | Olav's Tap and Tack, Bruma (Beyond Skyrim Bruma, BSHeartland) | **[UNC: confirm the inn exists in the installed BS Bruma and get its LCTN; if not, drop IN25]** |

  Fallback if a location has no own LCTN: `INN` + the town's location + the inn's innkeeper (`NEAR:<innkeeper>`).
- `INN_NEW` = LocTypeInn location that is **not** in the table above and the player has never been in it before (controller keeps a small FormList of visited inn locations). Covers mod inns.
- `not first visit` (IN4) = the inn location is already in that visited list.
- `EVENING` = hour 18..22. `hour a..b` = GetCurrentTime in that range.
- `MARKET` = exterior of a hold capital or town, hour 8..20, within 1500 units of a merchant with a stall (an actor in a Job*Merchant faction whose current package is a stall/sandbox at an exterior market marker) **[UNC: simplest proxy is a hand-made FormList of market-stall merchants: Carlotta, Fralia, Anoriath (Whiterun); Brand-Shei, Grelka, Madesi, Marise, Bolli, Balimund area (Riften); Evette San, Jala, Addvar (Solitude); Hillevi, Niranye, Aval Atheron (Windhelm); Kerah, Hogni Red-Arm, Lisbet's stall (Markarth)]**. `MARKET:<City>` = MARKET in that city. `(fish stall)` / `(produce stall)` / `(meat stall)` / `(jewellery stall)` = the nearest stall merchant is in a sub-list (fish: Marise, Bolli, Addvar; produce: Carlotta, Jala, Hillevi; meat: Anoriath, Hogni; jewellery: Fralia, Madesi, Kerah) **[UNC]**.
- `BARTER` = the Barter menu just closed (SKSE `OnMenuClose("BarterMenu")`) and the player's gold changed. `BARTER:<NPC>` = with that merchant (crosshair/dialogue target when the menu opened).
- `RENT` = the player just rented an inn room: Dialogue Menu closed with an innkeeper (actor in JobInnkeeperFaction) and player gold dropped by the room price in the same second **[UNC: vanilla room rent runs through the innkeeper's RentRoom topic; if the build can read that topic's fragment firing (e.g. watching `DialogueInnkeeper`/RentRoomScript), use that instead]**. Fires inside the inn, so `INN` is implied.
- `BARD_PLAYING` = as 41 FAMOUS NPCS `NEAR:any inn bard (performing)`: an actor filling a performer alias of the vanilla `BardSongs` quest is within 1500 units and its song scene is playing **[UNC: quest FormID and how to read "performing"]**. `(song ends)` = the same scene just stopped. `NEAR:Talsgar` = Talsgar the Wanderer within 1500.
- `BAB_PERFORMED` = Become a Bard (`BecomeABard.esp`): `_LP_BardTavernQuest` (027C20) reaches its "performance done" stage **[UNC stage; read the quest at build]**.
- `BRAWL_START` / `BRAWL_END` = the vanilla brawl quest (`DGIntimidateQuest`, Skyrim.esm **[UNC FormID/stages]**) starts / stops. `BRAWL_WON` / `BRAWL_LOST` = it stopped with the opponent / the player yielding **[UNC: stage numbers]**. `BRAWL_STEEL` = during the brawl any follower alias had `IsWeaponDrawn()` true (Brawl Bugs CE should prevent the real fight; the talk is about the draw, not about a death). `BRAWL_GUARD` = during the brawl an actor with `IsGuard()` entered combat with the player or the opponent.
- `RUMOUR` = the player just finished a Dialogue Menu with an innkeeper and the vanilla innkeeper rumour topic was used (or any `DialogueGenericRumors` info) **[UNC: proxy = dialogue with an innkeeper that lasted > 5 s and set no RENT]**.
- `FORGE` = within 800 units of a blacksmith forge furniture (`CraftingSmithingForge` keyword) in a town or city, with a blacksmith (JobBlacksmithFaction) within 1500. `(cold hold)` = Eastmarch, Winterhold or the Pale hold location, or `SNOW`.
- `NEAR:Ghorza`, `NEAR:Grelka`, `NEAR:Cosnach`, `NEAR:Brenuin` = that NPC within 1000 units. `TALKED:JonBattleBorn`, `TALKED:Keerava`, `TALKED:Fultheim`, `TALKED:Angrenor` = Dialogue Menu closed with that NPC this visit.
- `TEMPLE:<name>` = GetInCurrentLocation: Kynareth = Whiterun Temple of Kynareth, Mara = Riften Temple of Mara, Dibella = Markarth Temple of Dibella, HallOfTheDead = any Hall of the Dead (LocTypeHallOfTheDead keyword if present, else the 7 vanilla Halls) **[UNC EditorIDs]**. `TEMPLE (any)` = any of those plus the Temple of the Divines (Solitude) and the Temple of Talos (Windhelm). IN117 also needs: no Kaidan/vanilla wedding scene running (`RelationshipMarriageWedding` not 10..499 is already in WorldQuiet; add Kaidan's wedding windows from kaidan_block.md 2b).
- `SHRINE:Talos` = player activated a Talos shrine (the Blessing of Talos effect was just applied) and Inigo stood within 600 units **[UNC: the "Inigo prays" part is flavour; Inigo's own mod has no prayer idle we can test]**.
- `GUARD_KNEE`, `GUARD_SWEETROLL`, `GUARD_MAGIC` = a guard just said that vanilla idle line near the player. There is no clean event for a guard's idle line **[UNC]**. Build proxy: CITY exterior, an actor with `IsGuard()` within 300 units, plus: KNEE = random, after at least 10 game days spent in cities (controller counter), ONCE; SWEETROLL = Redcap following and Val following, random; MAGIC = player has a spell equipped in either hand. If the build can hook the guard's `DialogueGeneric`/`WICommentGuard` infos via SKSE (`OnTopicInfoBegin` is not vanilla; po3 has none), use that instead.
- `GUARD_FOLLOW` = a guard actor stays within 600 units of the player for 60 s in a CITY exterior.
- `CHILD_NEAR` = an actor with `IsChild()` within 800 units in a town or city exterior, daytime.
- `NEAR:stables (city)` = within 2000 units of a hold capital's stables map marker **[UNC refs]**.
- `CITY arrival + WILD_DAYS>=5` = arrival in a hold capital after at least 5 game days in which the player was never in a CITY/town location (controller stamps the day it last saw one).
- `leave CITY + MORNING, slept at an INN` = OnLocationChange from a hold capital to the wild, hour 5..11, and the last OnSleepStop was in a LocTypeInn interior in that city.
- `E LocTypeStore (apothecary) + CITY` = an interior with LocTypeStore in a hold capital whose merchant is in JobApothecaryFaction **[UNC]**.
- `LOC:WanderersFair` = the Wanderer's Fair location from `The Wanderer's Fair` plugin **[UNC: plugin name and LCTN; while the fair is set up only]**.
- `GORE_READS` (NEW) = Gore can read: Remi's `HLIOGoreReading` (6F46A0:HLIORemi.esp) >= its last lesson value **[UNC value]**, or Gore - Vigilant `HD1MemoriesQ` completed (he says there he learned to read).
- `Redcap not in his drunk quest` = `FA01RedcapDrunkQ` != 10 (TRIGGERS.md section 3).
- `at least 40 other talks from this file played` (IN150) = count of IN played bits >= 40.

## 3. Per-talk table

### Part 1 - The inns, one by one (IN1-IN25)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN1 | C G | E INN:BanneredMare | after R5 |
| IN2 | G K P | E INN:BanneredMare + TALKED:JonBattleBorn | after A1 |
| IN3 | L I | E INN:SleepingGiant | Lucien-Inigo own intro done |
| IN4 | K P | E INN:SleepingGiant | not first visit |
| IN5 | C I | E INN:WinkingSkeever | after R13 |
| IN6 | K V P | E INN:WinkingSkeever | after A2 |
| IN7 | X G | E INN:Candlehearth | after X1 |
| IN8 | X A | E INN:Candlehearth | ASHE_REVEAL |
| IN9 | I X | E INN:BeeAndBarb + TALKED:Keerava | after X6 |
| IN10 | C R P | E INN:BeeAndBarb (first visit with Redcap) | Remi-Redcap own intro done |
| IN11 | R K P | E INN:SilverBlood | after B1 |
| IN12 | G I P | E INN:DeadMansDrink | after C2 |
| IN13 | X V | E INN:Moorside | after X4 |
| IN14 | G P | E INN:Windpeak | GORE_BAIL |
| IN15 | P G L | E INN:FrozenHearth + RENT | after L1 |
| IN16 | L I | E INN:Nightgate + TALKED:Fultheim | Lucien-Inigo own intro done |
| IN17 | K C | E INN:Braidwood | after R1 |
| IN18 | L V P | E INN:Vilemyr | after C1 |
| IN19 | L K P | E INN:OldHroldan | after SQ69 |
| IN20 | G V P | E INN:FourShields | after A3 |
| IN21 | X C | E INN:Frostfruit | after R18 |
| IN22 | G I | E INN:DrunkenHuntsman | after C2 |
| IN23 | G V | E INN:Cornerclub | VAL_FATHER; after A3 |
| IN24 | K V | E INN_NEW | after A2 |
| IN25 | L G | E INN:OlavsTapAndTack | LUC_ADMIT; after L1 |

### Part 2 - Innkeepers (IN26-IN33)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN26 | K P | E INN + RENT | — |
| IN27 | L V | E INN | after C1 |
| IN28 | X G | E INN | after X1 |
| IN29 | C K | E INN | after R1 |
| IN30 | A G | E INN | ASHE_REVEAL |
| IN31 | S L | E INN | SERANA_F |
| IN32 | I R P | E INN | after B6 |
| IN33 | G K P | E INN + not CITY | after A1 |

### Part 3 - Rooms (IN34-IN46)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN34 | X V P | E INN + RENT | after X4 |
| IN35 | P K G | E INN + RENT | K_CRUSH; G_FLIRT |
| IN36 | V R | E INN + RENT | Remi-Val own intro done |
| IN37 | I G | E INN + NIGHT | after C2 |
| IN38 | S I | E INN + RENT | SERANA_F; SER_VAMP |
| IN39 | K A | E INN + MORNING | ASHE_REVEAL |
| IN40 | C R | E INN + NIGHT | RC_MANOS; Remi-Redcap own intro done |
| IN41 | V G K | E INN + RENT | K_TOG+; G_ANY or V_ANY |
| IN42 | S K | E INN + RENT | K_ANY; S_KISS |
| IN43 | A V | E INN + RENT | A_CRUSH; V_ANY |
| IN44 | G K P | E INN + RENT | K_MAR |
| IN45 | R L I | E INN + RENT | after B6; after B10 |
| IN46 | K P | E INN + hour 1..3 | K_TOG+ |

### Part 4 - Bards and requests (IN47-IN59)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN47 | G K | E INN + BARD_PLAYING | after A1 |
| IN48 | G R | E INN + BARD_PLAYING | GORE_READS |
| IN49 | K G P | E INN + BARD_PLAYING | K_CRUSH; after A1 |
| IN50 | C G | E INN:Windpeak + BARD_PLAYING | after R5 |
| IN51 | V R | E INN + BARD_PLAYING | after PY43 |
| IN52 | C I | E INN + BARD_PLAYING | after R13 |
| IN53 | G I | E INN + BARD_PLAYING (song ends) | after C2 |
| IN54 | I S | E INN + BARD_PLAYING | SERANA_F; SER_VAMP |
| IN55 | A V | E INN + BARD_PLAYING | ASHE_REVEAL |
| IN56 | G P K | E BAB_PERFORMED | after A1 |
| IN57 | L K | E INN + NEAR:Talsgar | Lucien-Kaidan own scenes done |
| IN58 | I K | E INN + BARD_PLAYING | Kaidan-Inigo own intro done |
| IN59 | L X P | E INN + BARD_PLAYING | Xelzaz-Lucien own intro done |

### Part 5 - Drinking games (IN60-IN67)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN60 | K R P | E INN + NIGHT | after B1 |
| IN61 | K S | E INN | SERANA_F; SER_VAMP |
| IN62 | C I | E INN | after R13; Redcap not in his drunk quest |
| IN63 | R A | E INN + NIGHT | ASHE_REVEAL; after B1 |
| IN64 | V X | E INN + NIGHT | after X4 |
| IN65 | V K P | E INN + NIGHT | after A2 |
| IN66 | G I | E INN + NIGHT | after C2 |
| IN67 | L G | E INN + NIGHT | after L1 |

### Part 6 - Cards and dice (IN68-IN72)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN68 | G X | E INN | after X1 |
| IN69 | V A | E INN | ASHE_REVEAL; after PY33 |
| IN70 | K R P | E INN | after B1 |
| IN71 | S L | E INN | SERANA_F |
| IN72 | L G P | E INN | after L1 |

### Part 7 - Brawls (IN73-IN80)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN73 | K C | E BRAWL_START | after R1 |
| IN74 | K G P | E BRAWL_END + BRAWL_STEEL | after A1 |
| IN75 | V P | E BRAWL_WON | after A2 |
| IN76 | R G | E INN:SilverBlood + NEAR:Cosnach | Remi-Gore own intro done |
| IN77 | L K | E BRAWL_END + BRAWL_GUARD | Lucien-Kaidan own scenes done |
| IN78 | I P | E BRAWL_LOST | — |
| IN79 | V X | E BRAWL_END | after X4 |
| IN80 | K S | E BRAWL_END | SERANA_F; SER_VAMP |

### Part 8 - Gossip and the corner table (IN81-IN90)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN81 | R I | E INN | after B6 |
| IN82 | V X P | E INN + RUMOUR | after X4 |
| IN83 | L P | E INN + EVENING | after L1 |
| IN84 | G P | E INN + READING | after A1 |
| IN85 | R K | E INN | after B1 |
| IN86 | C X P | E INN | after R18 |
| IN87 | L R | E INN | after B10 |
| IN88 | V S | E INN | SERANA_F |
| IN89 | V K | E INN + READING | K_CRUSH; after A2 |
| IN90 | P I | E INN | — |

### Part 9 - Markets, stalls and shops (IN91-IN109)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN91 | V R | E BARTER:Belethor | Remi-Val own intro done |
| IN92 | V K | E MARKET + BARTER | after A2 |
| IN93 | V P | E BARTER | after A2 |
| IN94 | R C | E MARKET | Remi-Redcap own intro done |
| IN95 | K R | E MARKET | after B1 |
| IN96 | X G | E MARKET (fish stall) | after X1 |
| IN97 | A X | E MARKET (produce stall) | ASHE_REVEAL |
| IN98 | X L | E MARKET (meat stall) | Xelzaz-Lucien own intro done |
| IN99 | K P | E MARKET (jewellery stall) | K_CRUSH |
| IN100 | K G | E MARKET:Riften + NEAR:Grelka | after A1 |
| IN101 | I X | E MARKET | after X6 |
| IN102 | C V P | E MARKET | after R8 |
| IN103 | R V | E LOC:WanderersFair | Remi-Val own intro done |
| IN104 | L I | E MARKET | Lucien-Inigo own intro done |
| IN105 | A K | E MARKET + BARTER | ASHE_REVEAL |
| IN106 | K I | E MARKET + MORNING | Kaidan-Inigo own intro done |
| IN107 | P L | E CITY + BARTER | after L1 |
| IN108 | X S | E LocTypeStore (apothecary) + CITY | SERANA_F; after X1 |
| IN109 | P X | E MARKET (produce stall) | — |

### Part 10 - Blacksmiths (IN110-IN115)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN110 | G R | E NEAR:Ghorza | GORE_READS |
| IN111 | I V | E FORGE | after I1 |
| IN112 | K X | E FORGE + (cold hold or SNOW) | after C3 |
| IN113 | L K | E FORGE | Lucien-Kaidan own scenes done |
| IN114 | G A | E FORGE | ASHE_REVEAL |
| IN115 | R L | E FORGE | after B10 |

### Part 11 - Temples (IN116-IN121)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN116 | G K | E TEMPLE:Kynareth | after A1 |
| IN117 | R G | E TEMPLE:Mara | Remi-Gore own intro done; not during any wedding |
| IN118 | X L | E TEMPLE:HallOfTheDead | Xelzaz-Lucien own intro done |
| IN119 | G I | E SHRINE:Talos | after C2 |
| IN120 | K S P | E TEMPLE (any) | SERANA_F; SER_VAMP |
| IN121 | V P | E TEMPLE:Dibella | — |

### Part 12 - Guards (IN122-IN126)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN122 | L I P | E CITY + GUARD_KNEE | ONCE |
| IN123 | C V | E CITY + GUARD_SWEETROLL | after R8 |
| IN124 | K P | E CITY + GUARD_MAGIC | — |
| IN125 | X I | E CITY + GUARD_FOLLOW | after X6 |
| IN126 | K G | E CITY | after A1 |

### Part 13 - Town by day and night (IN127-IN137)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN127 | G R | E CITY arrival + WILD_DAYS>=5 | Remi-Gore own intro done |
| IN128 | G V | E INN + MORNING | after A3 |
| IN129 | L V | E NEAR:stables (city) | LUC_ADMIT; after C1 |
| IN130 | L P | E INN + EVENING | — |
| IN131 | L P | E CITY + NIGHT (exterior) | — |
| IN132 | K L | E CITY:Riften + NIGHT | Lucien-Kaidan own scenes done |
| IN133 | V K | E CITY:Solitude + NIGHT (exterior) | after A2 |
| IN134 | R G P | E CITY + NIGHT (exterior) | Remi-Gore own intro done |
| IN135 | I G | E CITY + NIGHT, just left an INN | after C2; Redcap following |
| IN136 | S R | E CITY:Markarth + NIGHT | SERANA_F; Remi follows |
| IN137 | X K P | E CITY:Windhelm + NIGHT (exterior) | after C3 |

### Part 14 - Children in town (IN138-IN144)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN138 | G P | E CHILD_NEAR | DB |
| IN139 | L X | E CHILD_NEAR | Xelzaz-Lucien own intro done |
| IN140 | L G | E CHILD_NEAR | after L1 |
| IN141 | K V | E CHILD_NEAR | after A2 |
| IN142 | R I | E CHILD_NEAR | after B6 |
| IN143 | C I | E CHILD_NEAR | after R13 |
| IN144 | R P | E CHILD_NEAR + READING | after B1 |

### Part 15 - Beggars (IN145-IN149)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN145 | X I | E BEGGAR_COIN | after X6 |
| IN146 | V I | E BEGGAR_COIN | after I1 |
| IN147 | K I | E TALKED:Angrenor | BRYNJAR; Kaidan-Inigo own intro done |
| IN148 | G P | E BEGGAR_COIN | — |
| IN149 | G I | E CITY:Whiterun + NEAR:Brenuin | after C2 |

### Part 16 - Leaving town (IN150-IN150)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| IN150 | G K P | E leave CITY + MORNING, slept at an INN | after A1; at least 40 other talks from this file played |

## 4. Notes for the build
- Luna speaks in 50 of 150 talks (33%). Speaker counts: Kaidan 49, Gore 47, Val 34, Remi 27, Xelzaz 25, Inigo 33, Lucien 30, Redcap 16, Serana 11, Ashe 10, Luna 50.
- Every vanilla inn has a named row: Bannered Mare (2), Sleeping Giant (2), Winking Skeever (2), Candlehearth Hall (2), Bee and Barb (2), Silver-Blood Inn (2, one is the Cosnach brawl), Windpeak (2, one is Karita), Dead Man's Drink, Moorside, Frozen Hearth, Nightgate, Braidwood, Vilemyr, Old Hroldan, Four Shields, Frostfruit, Drunken Huntsman, New Gnisis Cornerclub. The Retching Netch (Dragonborn DLC) is skipped here, as asked; DR13 already covers it. The Ragged Flagon is left to 32 THIEVES GUILD.
- Mod content in this file: Olav's Tap and Tack (Beyond Skyrim Bruma) **[UNC]**, the Wanderer's Fair **[UNC location]**, Become a Bard (`BecomeABard.esp`, in 00_inventory.md), and `INN_NEW` for any inn a city/town overhaul adds. Inns from city overhauls (JK's, ETaC and the like) are **not named** on purpose: I could not confirm which are installed, so they ride on `INN_NEW` and the generic `INN` rows.
- Existing coverage avoided (read before writing): A6, A18, P6-P8, P12, K15, KX3, X7, N7, H4, H9, B11, MQ27-28, NP24-27, NP34, NP49, NP81, NP91, NP99, NP108, NP116, NP120, SQ6, SQ17-18, SQ69, SQ87, SQ110, SQ138, PL36, PL49, PL84, PL105, PL161, MN11, MN65, MN128, DB38, DA88, CW35-36, VG18, DR13, BR15, BR18-19, WS107, CC44, PA4, PA8, PA11, PA39, PA122, PY33-35, PY43-45, PY59, PY76, PY102, PY119-122, PY139, PY165-170, KL3, KL20, KL35, KL85, KL113, SE3, SE11, SE33, SE68, LN7, W6 (Kaidan's cloak), HF46 (snore map), TG32 (Xelzaz's loaded dice: IN68 calls back to it instead of repeating it), the Remi-Xelzaz tavern food/drink reviews and bard-parody arc in Xelzaz's own mod, Kaidan-Inigo "Tavern"/"Tavern2" scenes, Remi-Gore drinking contest, Ashe's pulse-reading and dwarven-oil-as-mead bits, Lucien's telescope. Also checked against the files being written in parallel today: PY252-253 (two truths, never have I ever), PY259 (Serana's "Old Stone Walls"), PY265, PR230, PR253, LT63 (the "tactical" room grab), RV16, RV25, RV35, RV59, RV137, TV163, WE95, WE105, WE108, WE113, PL171 (Lucien and the Lady), AS13, NP110, SQ4, CW48; titles and lines that clashed were rewritten.
- Gore and bards, new angles only: the horse-holders nobody sings about (IN47), reading the lyrics (IN48), the Battle-Born rebel (IN2), Karita singing the Ravens song with the swearing taken out (IN50), bards as stray cats (IN53), Luna turning bard (IN56), kids with flutes (IN140). No thrown chairs, lutes, boots or Ragnar jokes.
- Market roles as asked: Val haggles (IN91, IN92, IN93, IN103); Remi steals (IN94, IN95, plus the scrap bin and the closed shops); Xelzaz judges produce (IN96, IN97, IN98, IN109).
- Inigo gives coin in IN145, IN146 and IN149; his skooma past is only ever "worse things" / "an old road" (IN66), never named.
- Rival rows: IN35 (K_CRUSH + G_FLIRT, Luna oblivious), IN41 (K together, G or V had feelings), IN42 (K + Serana kiss), IN43 (Ashe crush + Val). Luna never picks anyone.
