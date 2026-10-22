# Triggers - 43b WHAT LUNA DOES 2 (prefix PA, PA161-PA310, 150 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\43b WHAT LUNA DOES 2.txt`
Written 2026-10-18. Writing only: nothing in the game, `profiles\`, `mods\` or `ModOrganizer.ini` was touched.

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C) plus **S = Serana**, **A = Ashe**, **U = Luna** (player line, Eleonora voice; no Free() test).
Gate codes as TRIGGERS.md section 4 and the part-1 sheet `triggers\43 WHAT LUNA DOES.md` (STAT, CRIME, CLEAN, JAIL_OUT, LOWHP, SERANA_F, S_VAMP, ASHE_F, ASHE_REVEAL, ASHE_AMENDS, K_I, WILD, INNOCENT, DB, the po3 / vanilla hook table). Everything below reuses those hooks; only the new gates are defined here.
Every talk is **E** (event). WorldQuiet() and Free() always apply.

## New hooks and gate codes for this file

| Code | Meaning / how the controller sees it |
|---|---|
| `SKILL:<AV> >= n` | **Sticky milestone.** po3 `OnSkillIncrease` (fallback: 60 s poll of `GetBaseActorValue`) sees the base skill first reach n. The controller sets a "reached" bit and the talk stays eligible **until it plays** (any later safe tick where the speakers are Free). Never fires again. AV names: Smithing, Alchemy, Enchanting, Marksman (Archery), Sneak, Speechcraft, Lockpicking, Pickpocket, Destruction, Conjuration, Restoration, Alteration, Illusion, OneHanded, TwoHanded, Block, HeavyArmor, LightArmor. |
| `SKILL... + RIGHT_AFTER:<x>` | Sticky skill bit is set AND event x happened in the last 60 s (talk waits for the next x if the bit is set but x hasn't happened). |
| `ALL5_50` | Alteration, Conjuration, Destruction, Illusion, Restoration base values all >= 50. Sticky. |
| `FIRST100` | Any of the 18 skills first reaches base 100. Sticky. |
| `LEGENDARY` | 60 s poll: a skill base value fell from >= 100 to <= 15 since the last poll, and `STAT:Times Jailed` did not rise in the last game hour. |
| `LEVEL n` | po3 `OnLevelIncrease` / `GetLevel()` first reaches n. Sticky. |
| `DUALCAST` | AFTERFIGHT; the player owns any of the five dual-casting perks; during the fight both hands held the same spell (`GetEquippedSpell(0) == GetEquippedSpell(1)`, polled each 2 s in combat) and at least one cast happened (`OnSpellCast` on the player alias). First time only. |
| `AVOIDDEATH` | AFTERFIGHT + LOWHP; player has the Restoration death-cheating perk; health rose by >= 25% within 1 s while LOWHP with no potion used (`STAT:Potions Used` unchanged) **[UNCONFIRMED: Authoria runs Requiem, which replaces vanilla perks; map every PERK gate in this file to the Requiem equivalent at build]**. |
| `TWINSOULS` | po3 `GetCommandedActors(Player)` holds 2+ summoned atronachs at once (actor race in a FormList of atronach races). First time. |
| `QUIETCAST` | `HasPerk(<Illusion quiet-casting perk>)` true; first AFTERFIGHT after it became true. |
| `PURE_POTION` | po3 `OnItemCrafted` at an alchemy bench (`CraftingAlchemyWorkbench` keyword) where every effect of the created Potion is non-hostile (`IsHostile() == false` on each `GetNthEffectMagicEffect`) and the purity perk is owned. First time. |
| `DAGGER_SNEAK_15` | controller counter: `STAT:Sneak Attacks +1` while the right hand weapon has `WeapTypeDagger`; reaches 15. |
| `UNDEAD_ILLUSION` | po3 `OnMagicHit` / `OnMagicEffectApplyEx` on an actor with the `ActorTypeUndead` keyword, source caster Player, effect archetype Calm or Frenzy-fear (`Calm`, `Demoralize`) **[UNCONFIRMED event coverage for non-alias targets; fallback: poll draugr within 1500 units for `HasMagicEffectWithKeyword(MagicInfluenceFear/Calm)`]**. First time. |
| `SHOUT:<x> FIRST` | po3 `OnShoutAttack(Shout akShout)` with akShout == the vanilla shout record, first time ever. Shout EditorIDs: `VoiceWhirlwindSprint`, `VoiceBecomeEthereal`, `VoiceUnrelentingForce`, `VoiceSlowTime`, `VoiceStormCall`, `VoiceCallDragon`, `VoiceFireBreath`, `VoiceMarkedForDeath`, `VoiceAnimalAllegiance`, `VoiceKynesPeace`, `VoiceThrowVoice`, `VoiceAuraWhisper`, `VoiceDismay`, `VoiceIceForm`, Dawnguard Soul Tear **[check all EditorIDs at build]**. |
| `GOAT_UF` | `SHOUT:UnrelentingForce` and at that moment an actor of `GoatRace` / `GoatDomesticsRace` is within 1200 units and within 30 degrees of the player's heading (po3 `GetHeadingAngle`). |
| `DRAGONKILL:<how>` | po3 `OnActorKilled`, victim has `ActorTypeDragon`. `FIREBREATH_FROST` = the player's last `OnShoutAttack` within 5 s was Fire Breath and the victim's base actor is in a FormList of frost dragon bases (vanilla Frost Dragon, Revered/Legendary use frost too) **[check list]**. `SLOWTIME` = player has the Slow Time magic effect active. `STORMCALL` = Storm Call effect active and the player landed no hit/spell on the dragon in the last 3 s (lightning got the kill) **[heuristic]**. `UF_CLIFF` = Unrelenting Force hit the dragon in the last 8 s and its Z position dropped >= 1500 units since then (1 s position samples during dragon fights) **[heuristic]**. |
| `ALDUIN` | MQ305 stage 200 done (TRIGGERS.md). |
| `VOLUNTARY_JAIL` | `STAT:Times Jailed +1` while the player's gold at arrest >= that hold's crime gold (snapshot on `CRIME` read just before the jail teleport). |
| `RIFTEN_JAIL_OUT` | JAIL_OUT where the jail interior is in `RiftenJailLocation` (or the Riften Mistveil Keep prison cell) **[check location record]**. |
| `EVIDENCE_BACK` | `STAT:Jail Escapes +1`, then within 10 min `OnItemAdded` from a container whose base is the hold's prisoner-belongings / evidence chest **[find base IDs at build]**. |
| `SMALL_FINE` | `STAT:Fines Paid +1` and gold fell by < 20 in that dialogue. |
| `RR_FINE` | `STAT:Fines Paid +1` inside `DLC2RavenRockLocation` (crime faction `DLC2CrimeRavenRockFaction`). |
| `THANE_OFF` | that hold's crime gold fell to 0 during dialogue with a guard (`IsGuard`), the player's gold did not change, and the player is Thane of that hold **[UNCONFIRMED Thane check: vanilla `FavorJarlsMakeFriends` stage per hold or the housecarl alias; pick at build]**. |
| `LONG_JAIL` | JAIL_OUT and `STAT:Days Jailed` rose by >= 5 during that stay. |
| `HOUSE_FIRST:<loc>` | first `OnLocationChange` into the house location while the player owns it (house key in inventory or the house's purchase stage done). Locations: `BreezehomeLocation`, `HoneysideLocation`, `ProudspireManorLocation`, `VlindrelHallLocation`, `HjerimLocation`, `DLC2SeverinManorLocation` **[check EditorIDs / key records at build]**. |
| `HORSES>=2` | `STAT:Horses Owned` reaches 2. |
| `HORSE_DIED` | po3 `OnActorKilled` victim == `Game.GetPlayersLastRiddenHorse()` and that horse was owned (in `PlayerHorseFaction`) **[check faction name]**. Fires at the first safe tick after combat. |
| `ARVAK_FIRST` | vanilla `OnSpellCast` on the player alias with the Summon Arvak spell, first time (or GetPlayersLastRiddenHorse == Arvak). |
| `SHADOWMERE_FIRST` | `Game.GetPlayersLastRiddenHorse()` == Shadowmere's ref while mounted, first time. |
| `DOG_BANNING` | the vanilla animal-follower alias (`DialogueFollower` quest, Animal alias) gets filled with Banning's dog in Markarth **[find the dog's ref at build]**. `DOG_ANY` = that alias holds any actor with `DogRace` / `DLC1HuskyArmoredRace` etc. `VIGILANCE` = alias holds Vigilance. |
| `CHILD_PET_CRAB` | Hearthfire adoption: the child's pet ref enabled at a player house is a mudcrab **[find the BYOH pet quest/alias at build]**. |
| `SPOUSE_OUT` | player is married (vanilla `RelationshipMarriageFIN` past the wedding stage) and the spouse alias ref is **not** Kaidan, Val, Gore, Serana, Remi, Ashe or any of our cast. Never fires for K_MAR, V_MAR, G_OATH or SDA marriage. |
| `HOMEMEAL` | `OnItemAdded` of the vanilla Home-Cooked Meal food while in dialogue with the spouse alias **[find FormID]**. |
| `SPOUSE_GOLD` | `OnItemAdded` Gold001 >= 100 while in dialogue with the spouse alias **[UNCONFIRMED; the spouse store hand-over]**. |
| `LOVERS_COMFORT` | after `OnSleepStop(false)` in a player house, the player gains the vanilla Lover's Comfort spell effect **[find SPEL]**. Fires at the first safe MORNING tick. |
| `COOKED:<food>` | po3 `OnItemCrafted`, bench has `CraftingCookpot` (or the Hearthfire oven keyword for SWEETROLL_OVEN), created item EditorID in: `FoodHorkerStew`, `FoodElsweyrFondue`, Sweetroll (oven only), salmon steak, `FoodAppleCabbageStew`, mammoth steak **[check all EditorIDs]**. |
| `SWEETROLL_AGAIN` | eat Sweetroll (as PA126) with Redcap Free, after PA126 played. |
| `GIVE:<who>:<what>` | `OnItemRemoved(..., akDestContainer)` where akDestContainer is that follower's ref (gift or trade menu). What: Book; any item; rare ingredient FormList (Deathbell, Nirnroot, Crimson Nirnroot, Daedra Heart, Jarrin Root etc.); Sweetroll; Dwemer misc FormList (as PA12); armour with `ArmorHelmet` or head slot 30/31 non-circlet; gem/jewelry (`VendorItemGem`, `VendorItemJewelry`). |
| `DRINKS5:<where>` | PA122's alcohol FormList, 5+ consumed within 1 game hour. `WILD` = WILD and CAMP; `SOLSTHEIM` = in `DLC2SolstheimWorld` (any building); `ANY` = anywhere with SERANA_F. |
| `SLEPT24` | `OnSleepStart` stores GameDaysPassed; `OnSleepStop(false)` with a difference >= 1.0. |
| `WAITED24` | 60 s poll sees GameDaysPassed rise by >= 1.0 since the last poll, "Sleep/Wait Menu" was open in between, and no `OnSleepStart` / `OnPlayerFastTravelEnd` happened. |
| `STAFF_MADE n` | po3 `OnItemCrafted`, bench base has the Dragonborn staff enchanter workbench keyword **[check: DLC2StaffEnchanter]**; controller counter n. |
| `BLACKGEM_ENCH` | "Crafting Menu" open at an enchanter (`CraftingEnchanter`), a filled black soul gem leaves the inventory (`OnItemRemoved`, base = the filled black soul gem) and `STAT:Magic Items Made +1` within 2 s. |
| `NIRN n` | `OnItemAdded` of Nirnroot (the plain one, not Crimson) from a harvest (akSourceContainer == None); counter n. |
| `SCROLLS>=2` | summed `GetItemCount` over a FormList of the Elder Scroll items (main-quest scroll, the two Dawnguard scrolls) >= 2. `SCROLL_INN` = >= 1 and INN. |
| `READ:<book>` | po3 `OnBookRead`. Lusty Argonian Maid v1/v2; skill books by SKSE `Book.GetSkill()` plus title FormList: "The Black Arrow" (Marksman), "The Locked Room" (Lockpicking), "Heavy Armor Forging" (Smithing), "Breathing Water" (Alteration) **[check the title-to-skill pairs at build]**. |
| `GOLD_DROP` | `OnItemRemoved` of Gold001 with `akDestContainer == None`. |
| `CHARITY:<who>` | the Gift of Charity effect (part-1 PA39 open item) is applied and the nearest NPC within 300 units is Noster Eagle-Eye / Silda the Unseen **[find refs]**. `CHARITY>=10` = controller counter of charity effects. |
| `G_READ` | Remi's `HLIOGoreReading >= 1` (reading lessons started) or Gore - Vigilant `HD1MemoriesRestored` (he can read by then). |
| `LUC_ADMIT` | TRIGGERS.md (Clive). |
| `SOULCAIRN` | `DLC1VQ05` completed. |
| `ASHE_LOGS` | Ashe's `MM_AMQ_01` completed (workshop shown, logs heard). |
| `XR_OK` | Remi/Xelzaz not fallen out (TRIGGERS.md section 3). |

## Table

### Part 1 - Skills, one number at a time
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA161 | G U | E | `SKILL:Smithing >= 25` |
| PA162 | K G | E | `SKILL:Smithing >= 50`; after A1 |
| PA163 | K U | E | `SKILL:Smithing >= 75`; K_CRUSH |
| PA164 | R X | E | `SKILL:Alchemy >= 25`; XR_OK |
| PA165 | X U | E | `SKILL:Alchemy >= 75`; after PA68 |
| PA166 | A R | E | `SKILL:Enchanting >= 25`; ASHE_F; ASHE_REVEAL |
| PA167 | A U | E | `SKILL:Enchanting >= 75`; ASHE_F; ASHE_LOGS |
| PA168 | I U | E | `SKILL:Marksman >= 25` |
| PA169 | K I | E | `SKILL:Marksman >= 50`; K_I |
| PA170 | V I | E | `SKILL:Marksman >= 75`; after I1 |
| PA171 | K I U | E | `SKILL:Marksman >= 100`; K_I; after PA169 |
| PA172 | V K | E | `SKILL:Sneak >= 25`; after A2 |
| PA173 | R V | E | `SKILL:Sneak >= 50`; Val/Remi intro done (`HLIOValBanter` stage 10) |
| PA174 | A U | E | `SKILL:Sneak >= 75`; ASHE_F; ASHE_REVEAL |
| PA175 | V U | E | `SKILL:Sneak >= 100` |
| PA176 | V G | E | `SKILL:Speechcraft >= 25`; fires within 10 min of a BarterMenu close; after A3 |
| PA177 | V L | E | `SKILL:Speechcraft >= 75`; INN; after C1 |
| PA178 | S U | E | `SKILL:Speechcraft >= 100`; SERANA_F |
| PA179 | R U | E | `SKILL:Lockpicking >= 25`; `STAT:Locks Picked +1` with lock level >= 50 (Adept) and no lockpick lost on it |
| PA180 | I R | E | `SKILL:Lockpicking >= 50`; after B6 |
| PA181 | V R | E | `SKILL:Lockpicking >= 75`; Val/Remi intro done |
| PA182 | R U | E | `SKILL:Lockpicking >= 100` |
| PA183 | V R | E | `SKILL:Pickpocket >= 50`; Val/Remi intro done (`HLIOValPickpocket` set is a nice-to-have) |
| PA184 | V U | E | `SKILL:Pickpocket >= 100` |
| PA185 | L I | E | `SKILL:Destruction >= 25`; Lucien-Inigo intro done (`JRLucienInigoRank >= 2`) |
| PA186 | C G | E | `SKILL:Destruction >= 75` + RIGHT_AFTER: a frost spell cast while `IsSwimming`-capable water within 500 units (po3 `OnSpellCast` frost school + `GetWaterLevel`) **[heuristic; fallback: any frost spell cast near water in WILD]**; after R5 |
| PA187 | V U | E | `SKILL:Destruction >= 100` |
| PA188 | L U | E | `SKILL:Conjuration >= 25` + RIGHT_AFTER: player summons a familiar (Conjure Familiar / Spectral wolf SPEL via `OnSpellCast`) |
| PA189 | G U | E | `SKILL:Conjuration >= 50` + RIGHT_AFTER: a bound weapon spell cast |
| PA190 | X S | E | `SKILL:Conjuration >= 75` + RIGHT_AFTER: Conjure Storm Atronach cast; SERANA_F |
| PA191 | X U | E | `SKILL:Conjuration >= 100` |
| PA192 | K U | E | `SKILL:Restoration >= 25`; K_TOG+ |
| PA193 | R G | E | `SKILL:Restoration >= 50`; after Remi-Gore intro (`HLIOGoreBanter` stage >= 1) |
| PA194 | I L | E | `SKILL:Restoration >= 75` + AFTERFIGHT:dragon and the player cast a Ward during it; Lucien-Inigo intro done |
| PA195 | S U | E | `SKILL:Restoration >= 100`; SERANA_F; S_VAMP |
| PA196 | A G | E | `SKILL:Alteration >= 25`; CAVE or DWEMER or CRYPT; player cast Magelight in this location; ASHE_F |
| PA197 | V U | E | `SKILL:Alteration >= 50`; CAMP |
| PA198 | X L | E | `SKILL:Alteration >= 75`; CAMP; Xelzaz-Lucien intro done |
| PA199 | L U | E | `SKILL:Alteration >= 100` + AFTERFIGHT where 3+ enemies had a Paralysis effect at once (Mass Paralysis) |
| PA200 | I C | E | `SKILL:Illusion >= 25` + RIGHT_AFTER: Calm-archetype spell hit an animal (`ActorTypeAnimal`); after R13 |
| PA201 | C U | E | `SKILL:Illusion >= 50` |
| PA202 | G L | E | `SKILL:Illusion >= 75` + AFTERFIGHT where the player cast a Frenzy spell; after L1 |
| PA203 | S U | E | `SKILL:Illusion >= 100` + RIGHT_AFTER: Harmony cast (or any area Calm hitting 3+ actors); SERANA_F |
| PA204 | K A | E | `SKILL:OneHanded >= 50`; ASHE_F |
| PA205 | G A | E | `SKILL:TwoHanded >= 50`; ASHE_F |
| PA206 | K G | E | `SKILL:Block >= 50`; after A1 |
| PA207 | K V | E | `SKILL:HeavyArmor >= 50`; exterior; after A2 |
| PA208 | V I | E | `SKILL:LightArmor >= 50`; after I1 |
| PA209 | L U | E | ALL5_50 |
| PA210 | K U | E | FIRST100 |
| PA211 | L R | E | LEGENDARY; after B10 |
| PA212 | G K | E | LEVEL 60; after A1 |
| PA213 | S K | E | LEVEL 70; SERANA_F |
| PA214 | R X | E | LEVEL 75; XR_OK |

### Part 2 - The knack
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA215 | L U | E | DUALCAST |
| PA216 | K X | E | AVOIDDEATH; after C3 |
| PA217 | C G | E | TWINSOULS; after R5 |
| PA218 | V R | E | QUIETCAST; Val/Remi intro done |
| PA219 | X U | E | PURE_POTION |
| PA220 | I A | E | DAGGER_SNEAK_15; ASHE_F; ASHE_LOGS |
| PA221 | L U | E | UNDEAD_ILLUSION; CRYPT |

### Part 3 - The voice (all need DB)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA222 | G C | E | SHOUT:WhirlwindSprint FIRST; DB; after R5 |
| PA223 | S I | E | SHOUT:BecomeEthereal FIRST; DB; SERANA_F; SOULCAIRN |
| PA224 | I G U | E | GOAT_UF; DB; after C2 |
| PA225 | L U | E | SHOUT:SlowTime FIRST; DB |
| PA226 | V X | E | SHOUT:StormCall FIRST; DB; after X4 |
| PA227 | K U | E | SHOUT:CallDragon FIRST (Odahviing arrives); DB; ALDUIN |
| PA228 | C X | E | SHOUT:FireBreath FIRST; DB; Redcap-Xelzaz intro done (as R18) |
| PA229 | G V | E | SHOUT:MarkedForDeath FIRST; DB; after A3 |
| PA230 | I R | E | SHOUT:AnimalAllegiance FIRST; DB; after B6 |
| PA231 | K G | E | SHOUT:KynesPeace FIRST; DB; after A1 |
| PA232 | R L | E | SHOUT:ThrowVoice FIRST; DB; after B10 |
| PA233 | A U | E | SHOUT:AuraWhisper FIRST; DB; ASHE_F; ASHE_REVEAL |
| PA234 | C I | E | SHOUT:Dismay FIRST; DB; after R13 |
| PA235 | X S | E | SHOUT:IceForm FIRST; DB; SERANA_F |
| PA236 | S R | E | Soul Tear shout used and the victim rises as a thrall (victim dies within 30 s of `OnShoutAttack(SoulTear)` and a Reanimate effect from the player appears on it); DB; SOULCAIRN; SERANA_F |
| PA237 | K G | E | DRAGONKILL:FIREBREATH_FROST; DB; after A1 |
| PA238 | A L | E | DRAGONKILL:SLOWTIME; DB; ASHE_F |
| PA239 | V K | E | DRAGONKILL:STORMCALL; DB; after A2 |
| PA240 | G U | E | DRAGONKILL:UF_CLIFF; DB |

### Part 4 - The law, again
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA241 | G K | E | VOLUNTARY_JAIL, plays at JAIL_OUT; GORE_BAIL; after A1 |
| PA242 | I U | E | RIFTEN_JAIL_OUT; Inigo following (IsPlayerTeammate) |
| PA243 | R V | E | EVIDENCE_BACK; Val/Remi intro done |
| PA244 | K L | E | `STAT:Jail Escapes >= 2`, first safe tick outside; after PA22; Lucien-Kaidan intro done |
| PA245 | X L | E | SMALL_FINE; Xelzaz-Lucien intro done |
| PA246 | X C | E | RR_FINE; Redcap-Xelzaz intro done |
| PA247 | V U | E | THANE_OFF |
| PA248 | C K | E | LONG_JAIL; after R1 |

### Part 5 - Houses, horses, hounds and home
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA249 | X U | E | HOUSE_FIRST:Breezehome |
| PA250 | R I | E | HOUSE_FIRST:Honeyside; after B6 |
| PA251 | V L | E | HOUSE_FIRST:Proudspire; after C1 |
| PA252 | R K | E | HOUSE_FIRST:VlindrelHall; after B1 |
| PA253 | S G | E | HOUSE_FIRST:Hjerim; `MS11` (Blood on the Ice) completed; SERANA_F |
| PA254 | X C | E | HOUSE_FIRST:SeverinManor; Redcap-Xelzaz intro done |
| PA255 | G U | E | HORSES>=2, fires on first dismount after the purchase |
| PA256 | K I | E | HORSE_DIED; K_I |
| PA257 | S L | E | ARVAK_FIRST; SERANA_F; LUC_ADMIT |
| PA258 | X I | E | SHADOWMERE_FIRST; DB_JOIN; after X6 |
| PA259 | K U | E | DOG_BANNING |
| PA260 | C G | E | DOG_ANY for 10+ min; after R5 |
| PA261 | L R | E | VIGILANCE; after B10 |
| PA262 | C X | E | CHILD_PET_CRAB; HOUSE; Redcap-Xelzaz intro done |
| PA263 | X G | E | HOMEMEAL; SPOUSE_OUT; after X1 |
| PA264 | V R | E | SPOUSE_GOLD; SPOUSE_OUT; Val/Remi business talks done (`HLIOValFirstProfitDone`) **[nice-to-have]** |
| PA265 | I L | E | LOVERS_COMFORT; SPOUSE_OUT; MORNING; Lucien-Inigo intro done |

### Part 6 - The kitchen and the cup
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA266 | K U | E | COOKED:HorkerStew |
| PA267 | A I | E | COOKED:ElsweyrFondue; ASHE_F; ASHE_REVEAL |
| PA268 | C R | E | COOKED:Sweetroll at a Hearthfire oven; HOUSE |
| PA269 | G X | E | COOKED:SalmonSteak; after X1 |
| PA270 | X L | E | COOKED:AppleCabbageStew; Xelzaz-Lucien intro done |
| PA271 | G C | E | COOKED:MammothSteak; after R5 |
| PA272 | C U | E | SWEETROLL_AGAIN; after PA126 |
| PA273 | C I | E | GIVE:Redcap:Sweetroll; after R13 |
| PA274 | K C | E | DRINKS5:WILD; CAMP; after R1 |
| PA275 | X U | E | DRINKS5:SOLSTHEIM |
| PA276 | S V | E | DRINKS5:ANY; SERANA_F; not INN-only (any place) |

### Part 7 - Lost hours
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA277 | R G | E | SLEPT24, first safe tick after waking; after Remi-Gore intro |
| PA278 | X U | E | SLEPT24 (plays only if PA277 did not play this time) |
| PA279 | V I | E | WAITED24; after I1 |
| PA280 | L K | E | WAITED24 (only if PA279 did not play this time); Lucien-Kaidan intro done |

### Part 8 - Staves, souls, roots and scrolls
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA281 | X U | E | STAFF_MADE 1 |
| PA282 | L R | E | 1+ game day after PA281; after B10 |
| PA283 | G K | E | STAFF_MADE 3; after A1 |
| PA284 | S U | E | BLACKGEM_ENCH; SERANA_F; after LN43 |
| PA285 | X R | E | BLACKGEM_ENCH; XR_OK |
| PA286 | A U | E | BLACKGEM_ENCH; ASHE_F; ASHE_LOGS |
| PA287 | X U | E | NIRN 1 |
| PA288 | I X | E | NIRN 10; after X6 |
| PA289 | L U | E | SCROLLS>=2 |
| PA290 | V G | E | SCROLL_INN; after A3 |
| PA291 | X U | E | READ:LustyArgonianMaid (v1 or v2); after PA84 |
| PA292 | A S | E | READ:LustyArgonianMaid; ASHE_F; ASHE_LOGS; SERANA_F |
| PA293 | I K | E | READ:skill book Marksman ("The Black Arrow"); K_I |
| PA294 | R V | E | READ:skill book Lockpicking ("The Locked Room"); Val/Remi intro done |
| PA295 | G U | E | READ:skill book Smithing ("Heavy Armor Forging" or any Smithing skill book); G_READ |
| PA296 | X L | E | READ:skill book Alteration ("Breathing Water"); Xelzaz-Lucien intro done |

### Part 9 - Open hands
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PA297 | R V | E | GOLD_DROP; Val/Remi intro done |
| PA298 | C K | E | GOLD_DROP (only if PA297 did not qualify); after R1 |
| PA299 | G R | E | GIVE:Gore:Book; G_READ; after Remi-Gore intro |
| PA300 | K V | E | GIVE:Kaidan:any; K_CRUSH; after A2 |
| PA301 | X R | E | GIVE:Xelzaz:rare ingredient; XR_OK |
| PA302 | I L | E | GIVE:Inigo:Sweetroll; Lucien-Inigo intro done |
| PA303 | R U | E | GIVE:Remi:Dwemer part |
| PA304 | V K | E | GIVE:Val:helmet/hat; after A2 |
| PA305 | A S | E | GIVE:Ashe:Sweetroll; ASHE_F; ASHE_REVEAL; SERANA_F |
| PA306 | K G | E | CHARITY:Noster Eagle-Eye; after A1 |
| PA307 | I R | E | CHARITY:Silda the Unseen; after B6 |
| PA308 | L U | E | CHARITY>=10 |
| PA309 | C G | E | GIVE:Redcap:gem or jewelry; after R5 |
| PA310 | I K U | E | CAMP + NIGHT; 40+ talks from this file played; after PA160, PA224, PA165, PA242; K_I |

## Open items to verify at build
- **Requiem perks.** Authoria runs Requiem, which replaces the vanilla perk trees. Every perk-based gate (DUALCAST, AVOIDDEATH, TWINSOULS, QUIETCAST, PURE_POTION, UNDEAD_ILLUSION) must be mapped to the Requiem perk that gives the same ability, or fall back to the behaviour checks described.
- Shout EditorIDs (incl. Dawnguard Soul Tear), frost-dragon base list, the STORMCALL and UF_CLIFF kill heuristics.
- House location and key records; Banning's dog ref; Vigilance ref; Hearthfire child-pet aliases; Home-Cooked Meal, Lover's Comfort and the spouse gold hand-over.
- Staff enchanter workbench keyword; filled black soul gem base; Nirnroot FormID; Elder Scroll item list; skill book title-to-skill pairs.
- Gift of Charity (PA39) FormID, Noster Eagle-Eye and Silda the Unseen refs.
- THANE_OFF Thane check; EVIDENCE_BACK chest bases; VOLUNTARY_JAIL gold snapshot timing.
- Food EditorIDs for COOKED (horker stew, fondue, oven sweet roll, salmon steak, apple cabbage stew, mammoth steak), plus Authoria's food mods (Requiem food overhaul may rename or replace them).
