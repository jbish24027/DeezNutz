# 56 WORLD ENCOUNTERS - trigger rows (prefix WE, 150 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\56 WORLD ENCOUNTERS.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4, `triggers\20 DAWNGUARD.md` (Serana/Ashe Free() rows), `triggers\48 SERANA.md`, `triggers\49 ASHE.md`, the bibles, `research\content\00_inventory.md` (Immersive World Encounters section), and the WE quest records read read-only through houseCARL on 2026-10-18 (epoch e2-1279b2cbd7971d8f, profile DEEZ CS NUTZ - PICTA).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Serana and Ashe use the Free() rows in `20 DAWNGUARD.md` section 1. Every row with S also needs `SERANA` plus Serana following; every row with A also needs `ASHE_HIRED` plus Ashe following. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment).

## Encounter quiet rule (the user's "never during scripted dialogue")

Added to WorldQuiet for this file only, checked on every WE row:
- no actor filling any alias of the named WE / IE quest is `IsInScene`, `IsInDialogueWithPlayer`, or has the player as its dialogue target;
- the player is not in the Dialogue Menu, and no encounter actor is within 600 units while that actor's quest has a forcegreet or scene package running [UNC: read the package type off the alias PackageData at build];
- player not in combat (the normal rule); an E row that lands during combat waits for the 8 s AFTERFIGHT delay.

## Event codes (new in this file)

The controller keeps a short list of the WE quests below (resolved with `Game.GetFormFromFile`, so Dawnguard/Dragonborn/Immersive Encounters are soft dependencies) and polls `IsRunning()` on the 60 s tick, plus on `OnLocationChange` and on combat end. [UNC: a Story Manager node watching the WE start events would be cheaper; the poll is the fallback.]

- `WE_NEAR:<EditorID>` = **before**. The quest is running, its first actor alias is loaded, 1500..4000 units from the player, nobody in the encounter has spoken to the player yet (no alias actor has `GetDialogueTarget == player` this run; controller flag), and the encounter quiet rule passes. Fires once per run of that quest. If the player gets within 1500 first, the row is skipped for this run.
- `WE_DONE:<EditorID>` = **after**. Either the quest has stopped after the player was within 2000 units of it, or every hostile alias actor is dead and combat has ended (8 s delay), or the player was within 1000 units and is now more than 3000 units away. Fires once per run.
- `QUEST_DONE:<EditorID>` = `IsCompleted()` turns true this tick (Immersive Encounters quests have journal stages).
- `<EditorID> objective N completed / current` = `IsObjectiveCompleted(N)` / `IsObjectiveDisplayed(N) && !IsObjectiveCompleted(N)`.
- `song scene ended` = the bard's performance scene in that IE quest has stopped [UNC: scene EditorIDs not traced; fallback QUEST_DONE].
- `COURIER` = `WICourier` (039F82:Skyrim.esm) has just finished a delivery: the courier alias was within 300 units and has started walking off [UNC: stage numbers not traced; fallback = WICourier stops running after having its courier alias loaded near the player].
- `TOLL` = combat with a `BanditFaction` actor (01BCC0 [UNC]) started within 60 s after that actor said a line from the vanilla bandit toll topic [UNC: topic not traced; fallback = AFTERFIGHT:bandit, exterior, player in a cell with a road, at most once per game day].
- `DRAGON_TOWN` = player combat ends, last target `ActorTypeDragon`, and the player's current location has LocTypeCity, LocTypeTown, LocTypeSettlement or LocTypeHabitation [UNC: keyword FormIDs].
- `DOG_FOLLOW:WEJS18` = WEJS18 has run and its dog alias is following the player (`IsPlayerTeammate` on the dog alias ref, or the vanilla animal-follower faction) [UNC: which follower path the WEJS18 dog uses].
- `CARAVAN_NEAR` = exterior, not LocTypeCity, a member of the Khajiit caravan faction (CaravanFaction [UNC FormID]; Ri'saad, Ma'dran, Ahkari and their guards) within 2500 units, once per caravan per game week.
- `WE_COUNT` = controller int: +1 on every WE_DONE or QUEST_DONE of a quest in the list below. `TOLL_OR_AMBUSH_COUNT`: +1 on each TOLL and each WE_DONE of WE17, WERJ02, WE36, WEJS28.
- `WE_LATE` = a WE_DONE for one of WEJS01, WEJS16, WEJS18, WEJS24, DLC1WEJS01, WE100 (encounters that are already over when you arrive), set until the next CAMP talk.
- `one talk per encounter (X or Y)` = when two rows share the same run of a quest, play only one (random pick).

Reused codes: `AFTERFIGHT`, `CAMP`, `CAMP+NIGHT`, `NIGHT`, `CITY`, `WILD` (TRIGGERS.md); `K_CRUSH`, `K_ANY`, `K_TOG+`, `V_FLIRT`, `BRYNJAR`, `DELPHINE`, `WOLF`, `DB_JOIN`, `SOLST`, `LUC_ADMIT`, `RC_WEREPIG` (TRIGGERS.md section 4); `SERANA`, `SER_VAMP`, `DG_HARKON`, `DG_CAIRN` (20 DAWNGUARD.md); `ASHE_HIRED`, `ASHE_REVEAL` (49 ASHE.md); pair chains `after <ID>` (TRIGGERS.md "Chains": A1 G-K, A2 V-K, A3 G-V, B1 R-K, B6 I-R, B10 L-R, C1 L-V, C2 G-I, C3 X-K, R1 K-C, R5 G-C, R11 L-C, R13 C-I, R18 X-C, X1 G-X, X4 X-V, X6 I-X, L1 G-L). Pairs whose meeting lives in the follower mods themselves name that mod's intro.

## The encounters this file uses (EditorIDs read from the load order)

Vanilla (Skyrim.esm): WE03 Dragon vs Giant (09A9C9) · WE05 Orcs Fighting Forsworn (098B52) · WE06 Animals attacking bandit (09CABF) · WE07 Giants fending off bandits (09CAC2) · WE08 Dragon fly by (09CB5B) · WE09 Imperials with Stormcloak Prisoner (09D5A0) · WE11 Sabre cats hunting mammoths (09F329) · WE12 Wolves hunting deer (09F32C) · WE13 Spriggans fighting trolls (09F32F) · WE14 Skeevers fighting dogs (09F332) · WE15 Atronach mis-summoned (09F337) · WE16 Orcs hunting deer (09F801) · WE17 Bandits dressed as Imperial Soldiers (09F7E9) · WE18 Witch fighting Atronach (09F80A) · WE20 Warlock fighting off bandits (09F813) · WE22 Imperials vs Stormcloaks (05E93E) · WE23 Scavenger (062103) · WE24 A Good Death (062119; the old Orc and the sabre cats) · WE25 "Hey you there, take this" (062131) · WE27 / WE28 Imperial / Stormcloak Scout Patrol (074928 / 07492B) · WE29 Courier on the Run (07492E) · WE31 College Application Denied (0753CA) · WE32 Thalmor with Prisoner (0B80F3) · WE33 Thalmor vs Stormcloaks (0BA0B4) · WE34 Thalmor vs Player (0BA0BC) · WE36 Bounty hunters vs Player (0BC09D) · WE100 Dead Treasure Hunter with instructions (0A17AE) · WEBountyCollectorQST (0F8A80) · WERoad01 Farmer refugees after dragon attack (1034DF) · WERoad02 Nobles with Bodyguard (1027A5) · WERoad03 Thalmor travelling (105170) · WERoad05 Imperials on the Road (105173) · WERoad06 Adventurer on the way to a dungeon (105D1D) · WERoad07 Taunting Adventurer (105D15) · WEJS26 Aggressive Adventurer (105D12) · WERoad09 Skooma Dealer (1065FA) · WERoad10 / WERoad11 Giant / Farmer leading a painted cow (106A59 / 106A5E) · WERoad12 Headless Horseman (10BF8E) · WEJS01 Dead woman with bandits (0B1179) · WEJS03 / WEJS04 Forsworn attacking merchant / Imperial soldiers (0B5D46 / 0B5D5E) · WEJS09 Travelling merchant attacked by bandits (0B5D5F) · WEJS10 Dunmer pilgrim to Azura's Shrine (0B85B8) · WEJS11 Namira cultist, "the first bite" (0B85BD) · WEJS12 Necromancers attack (0BA2FF) · WEJS13 Pilgrim to the Gildergreen (0BC037) · WEJS14 Afflicted refugee to High Rock (0BED92) · WEJS16 Spriggan and dead hunter (0E8921) · WEJS18 Dragon-attack corpses, dog left behind (0E8929) · WEJS19 Roaming ice wraiths (0E892B) · WEJS20 Spriggan vs Hagraven (0E892D) · WEJS21 Hunter and dog (0E892E) · WEJS22 Ice wraiths vs bandits (0E8931) · WEJS23 Dog fending off wolves (0E8933) · WEJS24 Bandit killed, horse left (0E8924) · WEJS25 Wizard Duel (0E8941) · WEJS28 Dark Brotherhood assassin (105D19) · WEDL01b Bard attacked by bandits (0BFB61) · WEDL02 Bard on the road (0B813F) · WEDL03 On the way to the wedding (0B8143; Husband, Wife, Bodyguard, to Solitude) · WEDL04 Lost after the wedding (0B91D8) · WEDL05 / WEDL06 Louis Letrush's thug (0B91AE / 0B91C1) · WEDL07 Ramblings of a madman (0B91E3) · WEDL08 The drunken dare (0BBD9D) · WEDL10 Spriggan vs lumberjacks (0BD750) · WEDL12 Bitten by a vampire (0BD753) · WEDL13 / WEDL14 Looking to join the Imperials / Stormcloaks (0BD757 / 0BD758) · WEDLVigilOfStendarr01 / 02 / 04 Vigilants vs atronach / vs vampire / patrol (0B328F / 0B329E / 0B32F2) · WERJ01 Mistwatch escapee (0B1C79) · WERJ02 Thieves Guild holdup (0B8169) · WERJ03 Alik'r accusation (0B85AA) · WERJ04 Dwemer junk peddlers (0B94AB) · WERJ05 Blood Horker revenge (0BC5AA) · WERJ06 Drinking companions (0BC5BD) · WERJ07 Vampire trick (0BF31C) · WERJ09 Vampire attack (0C1A1D) · WERJ10 Companions hunting, Vilkas and Ria (0C1A1F) · WERJ12 Companions hunting, Farkas, Athis and Torvar (0F5186) · WICourier (039F82, the courier; not a WE quest).

Dawnguard.esm: DLC1_WESC01 Vigilants pursuing a vampire (0034DE) · DLC1_WESC02 Vampire Masquerade (0034EA) · DLC1_WESC03 Bats! (0034D0) · DLC1_WESC05 Dawnguard vampire hunters (0034DA) · DLC1WE02 Human changing into a werewolf (008771) · DLC1WE03 Gargoyles (017861) · DLC1WE04 / DLC1WE05 Death hounds / Vampire and death hound (017863 / 017865) · DLC1WE06 Vampires vs bandits (017867) · DLC1WEJS01 Vampire feeding on a Vigilant (00F7F0) · DLC1WEJS02 Vampire seeking shelter from the sun (010AE7; winner Immersive Encounters.esp) · DLC1WEJS04 Babette on the road near a body (010AEB) · DLC1WEJS05 / 06 Giant spider / Dueling giant spiders (0127EE / 0127F0) · DLC1WEDB02 Werewolf kills loved one (01420F) · DLC1WEDB03 Dawnguard vampire hunting (014215).

Dragonborn.esm: DLC2WE02 Animals attacking bandit (01F981) · DLC2WE03 Hunter and dog (01F989) · DLC2WE04 Ice wraiths vs bandits (01F98C) · DLC2WE07 Werebears (027E92) · DLC2WE08 Morag Tong competition (027E9D).

Immersive Encounters.esp (in this profile; inventory section "Immersive World Encounters"): SetteAdventurer01 Fellowship of Fighters (77A9C3) · SetteAdventurer02 Show Me The Way (5956AB) · SetteAdventurer03 Into the Deep (692B80) · SetteBard01 We're Out of the Woods (A970B4) · SetteBard02Evelyna (A970B9) · SetteBard03Neddvir Yours Truly (B9EA51) · SetteBard04Roxelle Two Sisters (06346F) · SetteBard05 The Touring Bard (341AB6) · SetteBladesDragonHunt Dragon Hunters (9333F8) · SetteBoy00 Boy's Endeavor (6B51AC; objectives 20 fight bandits, 25 escort home, 30 report his death, 40 speak to his mother) · SetteBoy01 Bring Me Home (6B51AD) · SetteCitizen03 A Fellow Traveler (65B02E) · SetteDA06 Stronghold Celebration (6DDA14) · SetteGiftOfCharityFollowUp01-04 O, Help Me Kind One (E78043 / E7D14D / 1932FF / 6F9F38) · SetteHusky01 Without A Trace (59055F; objectives 10 follow the dog, 15 into the dungeon, 30 search the boss, 40 show the ring to the dog) · SetteHusky02 The Pilgrim (614103; 10 read the book, 15 find the dog's master, 16 optional take the dog, 30 vanquish, 40 check up on the dog) · SetteNord01 When the Night Falls Down (6140E8) · SetteWERoad06Cont Bounty Hunt (77FAC5) · SetteBountyHunter01 Suspect of Misfortune (C0C928) · SetteWR01 Outbreak (49237A; giant and mammoth on a farm) · SetteWR02 Roadside Dispute (9BBE88) · WE_SetteDLC2Wilderness01 Werewolf vs Werebear (1866F4) · WEJS_SetteNecromancersForest Necromancers (075013) · WERJ_SetteMG01 Mis-Summoned Atronach (A9ABBC) · WERJ_SetteMG03 Nelacar and Fantastic Beasts (37BBE3) · WI_SetteCLSiegeWhiterun / Solitude / Markarth / Windhelm, the raids (6C04FC / 7E10E6 / 7BD9A3 / 780D0B).

Not used, on purpose: M'aiq (WE35, already in 41 FAMOUS NPCS), WE01, WE04/DLC2WE10 (dragon vs player, covered by fight files), WEJS02 (Dark Brotherhood hook), WEDA02 and DLC2WE06 (Daedric/Black Book hooks; DLC2WE06 is overridden by AX ValSerano), DLC2WE05 (overridden by AX ValSerano), WERJ11 (Skjor; dies in Companions), WERJ13 (Cragslane, covered in 37), Plague of the Dead CC (14 CREATION CLUB scope), SetteSoldiers01* (Civil War files).

## Notes for the build
- WE90 and WE133 share WEDL03; WE40/WE46 share WE15; WE78/WE79 share WERJ07; WE43/WE120 share the necromancer encounters: one talk per run.
- The dog chain: WE62 (dog picks Kaidan), WE63 (dog picks Redcap), WE92 (a hunter's dog leaves Gore), WE100 (pilgrim's dog picks Gore, needs WE63 and WE92), WE141 (all three).
- WE10 needs W11 ("The Headless Horse", batch 3) for the callback.
- No Dragonborn word anywhere in this file; no Kaidan cult content; Kaidan's Brynjar line in WE109 is gated BRYNJAR.

### PART 1 - STRANGERS AND MESSENGERS  (14 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE1 | V K P | E COURIER | - |
| WE2 | R L | E COURIER | after WE1; Lucien-Remi: after B10 |
| WE3 | G V | E WE_DONE:WE25 | after A3 |
| WE4 | K G P | E WE_NEAR:WERoad02 | after A1 |
| WE5 | V R P | E WE_DONE:WEBountyCollectorQST | Remi-Val intro done (HLIOValBanter Intro) |
| WE6 | G I | E WE_DONE:WEDL08 | after C2 |
| WE7 | X L | E WE_DONE:WEDL07 | Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| WE8 | A K | E WE_DONE:WERoad07 or WE_DONE:WEJS26 | ASHE_HIRED |
| WE9 | L I | E WE_NEAR:WERoad06 | Lucien-Inigo intro done (JRLucienInigo) |
| WE10 | G V P | E WE_NEAR:WERoad12 (NIGHT) | after W11; after A3 |
| WE11 | R V | E WE_DONE:WERJ04 | Remi-Val business talk done (HLIOValBanter Business2 scene) [UNC: which flag it sets] |
| WE12 | C G P | E WE_DONE:WERJ06 | after R5 |
| WE13 | P L | E WE_DONE:WE31 | - |
| WE14 | C K | E WE_NEAR:WERoad10 or WE_NEAR:WERoad11 | after R1 |

### PART 2 - SOLDIERS, THALMOR AND THE WAR  (17 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE15 | K P | E WE_NEAR:WE32 | - |
| WE16 | G K | E WE_DONE:WE32 (all Thalmor dead) | after A1 |
| WE17 | I K | E WE_DONE:WE32 (prisoner alive and out of sight) | KaiandInigo stage >= 10 |
| WE18 | X G P | E WE_NEAR:WE33 | after X1 |
| WE19 | V P R | E AFTERFIGHT, WE34 running (Thalmor vs Player) | Remi-Val intro done (HLIOValBanter Intro) |
| WE20 | K L | E WE_DONE:WE22 | Kaidan-Lucien intro done (JRLucienFollowerKaidanScene1) |
| WE21 | R G P | E WE_DONE:WE22, a soldier alive and below half health [UNC: health check on the WE22 survivors] | Remi-Gore intro done (HLIOGoreBanter MarkarthIntro) |
| WE22 | V X | E WE_NEAR:WE09 | after X4 |
| WE23 | K I | E WE_DONE:WE27 or WE_DONE:WE28 | KaiandInigo stage >= 10 |
| WE24 | L G P | E WE_DONE:WE29 | after L1 |
| WE25 | G K | E WE_DONE:WEDL13 or WE_DONE:WEDL14 | after A1 |
| WE26 | V R | E WE_DONE:WE17 | Remi-Val intro done (HLIOValBanter Intro) |
| WE27 | K X | E WE_DONE:WEJS03 or WE_DONE:WEJS04 | after C3 |
| WE28 | G K P | E QUEST_DONE:WI_SetteCLSiegeWhiterun | after A1 |
| WE29 | S V | E QUEST_DONE:WI_SetteCLSiegeSolitude | SERANA; DG_HARKON |
| WE30 | R L | E QUEST_DONE:WI_SetteCLSiegeMarkarth | after B10 |
| WE31 | X I | E QUEST_DONE:WI_SetteCLSiegeWindhelm | after X6 |

### PART 3 - FAITH ON THE ROAD  (7 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE32 | S K | E WE_DONE:WEDLVigilOfStendarr04 or WE_DONE:DLC1_WESC01 | SERANA; SER_VAMP |
| WE33 | L P | E WE_DONE:WEDLVigilOfStendarr01 | - |
| WE34 | V X | E WE_DONE:WEDLVigilOfStendarr02 | after X4 |
| WE35 | L I | E WE_DONE:WEJS13 | Lucien-Inigo intro done (JRLucienInigo) |
| WE36 | V X P | E WE_DONE:WEJS10 | after X4 |
| WE37 | G R | E WE_DONE:WEJS11 | Remi-Gore intro done (HLIOGoreBanter MarkarthIntro) |
| WE38 | X K | E WE_DONE:WEJS14 | after C3 |

### PART 4 - MAGIC GONE WRONG  (8 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE39 | P K | E WE_DONE:WE18 | - |
| WE40 | R L | E WE_DONE:WE15 or QUEST_DONE:WERJ_SetteMG01 | after B10 |
| WE41 | P V | E WE_DONE:WEJS25 | - |
| WE42 | G A | E WE_DONE:WE20 | ASHE_HIRED |
| WE43 | R X | E WE_DONE:WEJS12 or QUEST_DONE:WEJS_SetteNecromancersForest | BPUFXelzazRemielFallingOut stage 13 done, or never started; Remi-Xelzaz intro done (BPUFXelzaz Remi chain stage 11); one talk per encounter (WE43 or WE120) |
| WE44 | X K P | E WE_DONE:WEJS19 or WE_DONE:WEJS22 or WE_DONE:DLC2WE04 | after C3 |
| WE45 | P L | E QUEST_DONE:WERJ_SetteMG03 | - |
| WE46 | R A | E WE_DONE:WE15 or QUEST_DONE:WERJ_SetteMG01 | ASHE_REVEAL; one talk per encounter (WE40 or WE46) |

### PART 5 - THE WILD GETS BUSY  (12 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE47 | C G P | E WE_DONE:WE07 | after R5 |
| WE48 | I K | E WE_NEAR:WE11 | KaiandInigo stage >= 10 |
| WE49 | L G | E WE_DONE:WE03 | after L1 |
| WE50 | R V P | E WE_DONE:WE08 (dragon out of sight) | Remi-Val intro done (HLIOValBanter Intro) |
| WE51 | C L | E WE_DONE:WE13 | after R11 |
| WE52 | C X | E WE_DONE:WEJS20 | after R18 |
| WE53 | K G | E WE_DONE:WEJS16 | after A1 |
| WE54 | C I | E WE_DONE:WE12 | after R13 |
| WE55 | G A | E WE_NEAR:WE16 | ASHE_HIRED |
| WE56 | G K P | E WE_DONE:WE24 | after A1 |
| WE57 | C R | E WE_DONE:WE14 | Redcap-Remi intro done (FA01RedcapAndRemiInteractionsQ first scene) |
| WE58 | G I P | E WE_DONE:WE06 or WE_DONE:DLC2WE02 | after C2 |

### PART 6 - DRAGONS OVER THE TOWNS  (5 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE59 | K P | E DRAGON_TOWN | - |
| WE60 | R G | E DRAGON_TOWN | Remi-Gore intro done (HLIOGoreBanter MarkarthIntro); not on the same attack as WE59 or WE134 |
| WE61 | I K | E WE_NEAR:WERoad01 | KaiandInigo stage >= 10 |
| WE62 | C K P | E DOG_FOLLOW:WEJS18 | after R1 |
| WE63 | G C | E WE_DONE:WEJS23 (dog alive) | after R5 |

### PART 7 - BANDITS, THIEVES AND HUNTERS  (14 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE64 | A K P | E TOLL | ASHE_HIRED |
| WE65 | V G | E TOLL | after A3; not on the same toll as WE64 |
| WE66 | R I | E WE_DONE:WEJS09 (merchant alive) | after B6 |
| WE67 | S K | E WE_DONE:WEJS01 | SERANA |
| WE68 | G V P | E WE_DONE:WEJS24 | after A3 |
| WE69 | R V | E WE_DONE:WERJ02 | Remi-Val intro done (HLIOValBanter Intro) |
| WE70 | K V P | E WE_DONE:WERJ03 | after A2 |
| WE71 | V G | E WE_DONE:WERJ05 | after A3 |
| WE72 | L I | E WE_DONE:WEDL05 or WE_DONE:WEDL06 | LUC_ADMIT; Lucien-Inigo intro done (JRLucienInigo) |
| WE73 | K A | E WE_DONE:WE36 | ASHE_HIRED; K_ANY |
| WE74 | A I | E WE_DONE:WEJS28 | ASHE_REVEAL |
| WE75 | X C | E WE_DONE:WE23 | after R18 |
| WE76 | L R P | E WE_DONE:WE100 (note read) [UNC: book-read check on the WE100 note] | after B10 |
| WE77 | G K | E WE_DONE:WERJ01 | after A1 |

### PART 8 - VAMPIRES AND THINGS IN THE DARK  (10 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE78 | S I | E WE_DONE:WERJ07 | SERANA |
| WE79 | L P | E WE_DONE:DLC1_WESC02 or WE_DONE:WERJ07 | one talk per encounter (WE78 or WE79) |
| WE80 | X R | E WE_DONE:WEDL12 | Remi-Xelzaz intro done (BPUFXelzaz Remi chain stage 11) |
| WE81 | S K | E WE_DONE:WERJ09 or WE_DONE:DLC1WE06 (NIGHT) | SERANA |
| WE82 | X S | E WE_DONE:DLC1WEJS02 | SERANA; SER_VAMP |
| WE83 | S V | E WE_DONE:DLC1_WESC05 or WE_DONE:DLC1WEDB03 | SERANA; SER_VAMP |
| WE84 | C K | E WE_DONE:DLC1WE02 | WOLF; after R1 |
| WE85 | L I | E WE_DONE:DLC1WEDB02 | Lucien-Inigo intro done (JRLucienInigo) |
| WE86 | C S | E AFTERFIGHT:death hound, or WE_DONE:DLC1WE04 / DLC1WE05 | SERANA; DG_HARKON |
| WE87 | X G P | E WE_NEAR:DLC1WEJS04 | DB_JOIN; after X1 |

### PART 9 - PEOPLE WHO NEED A HAND  (10 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE88 | I K | E WE_DONE:WERoad09 | KaiandInigo stage >= 10 |
| WE89 | X I | E WE_DONE:WERoad09 (a later run of it) | after WE88; after X6 |
| WE90 | K P | E WE_NEAR:WEDL03 | K_CRUSH; one talk per encounter (WE90 or WE133) |
| WE91 | V G P | E WE_DONE:WEDL04 | after A3 |
| WE92 | G K | E WE_DONE:WEJS21 or WE_DONE:DLC2WE03 | after A1 |
| WE93 | C I | E CARAVAN_NEAR | after R13 |
| WE94 | R A | E CARAVAN_NEAR, or barter menu closed with a caravan merchant | ASHE_HIRED |
| WE95 | G L P | E WE_NEAR:WEDL02 or WE_NEAR:SetteBard05 | after L1 |
| WE96 | X R | E WE_DONE:WEDL01b (bard alive) | Remi-Xelzaz intro done (BPUFXelzaz Remi chain stage 11) |
| WE97 | V L | E QUEST_DONE:SetteCitizen03 | after C1 |

### PART 10 - DOGS  (3 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE98 | C K | E SetteHusky01 objective 10 or 15 current, exterior | after R1 |
| WE99 | K P | E SetteHusky01 objective 40 completed | - |
| WE100 | G C P | E SetteHusky02 objective 40 completed | after R5; after WE63 and WE92 |

### PART 11 - IMMERSIVE WORLD ENCOUNTERS  (20 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE101 | G K P | E QUEST_DONE:SetteAdventurer01 | after A1 |
| WE102 | X L | E SetteAdventurer01 objective 15 completed | Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| WE103 | R I | E QUEST_DONE:SetteAdventurer02 | after B6 |
| WE104 | R K | E SetteAdventurer03 running and player inside its Dungeon alias location | after B1 |
| WE105 | G V P | E SetteBard02Evelyna song scene ended, or QUEST_DONE | after A3 |
| WE106 | R L | E SetteBard03Neddvir song scene ended, or QUEST_DONE | after B10 |
| WE107 | S P | E SetteBard04Roxelle song scene ended, or QUEST_DONE | SERANA |
| WE108 | I K | E SetteBard01 or SetteBard05 song scene ended | KaiandInigo stage >= 10 |
| WE109 | K G | E SetteBladesDragonHunt objective 0 current (travelling with the Blades) | BRYNJAR; DELPHINE; after A1 |
| WE110 | G R | E QUEST_DONE:SetteBoy00 with objective 25 completed and 30 not | Remi-Gore intro done (HLIOGoreBanter MarkarthIntro) |
| WE111 | I K P | E SetteBoy00 objective 40 completed after objective 30 | KaiandInigo stage >= 10 |
| WE112 | C P | E SetteBoy01 running (taking the boy home) | - |
| WE113 | V X | E QUEST_DONE:SetteGiftOfCharityFollowUp01..04 (any) | after X4 |
| WE114 | C R | E QUEST_DONE:SetteWR01 | Redcap-Remi intro done (FA01RedcapAndRemiInteractionsQ first scene) |
| WE115 | A V P | E QUEST_DONE:SetteWR02 | ASHE_HIRED |
| WE116 | X P | E SetteNord01 objective 0 current, QuestGiver not in dialogue or a scene | - |
| WE117 | C L | E QUEST_DONE:WE_SetteDLC2Wilderness01 | RC_WEREPIG; after R11 |
| WE118 | G X | E SetteDA06 running and player in its stronghold | after X1 |
| WE119 | V K | E SetteWERoad06Cont or SetteBountyHunter01 started | after A2 |
| WE120 | R S | E QUEST_DONE:WEJS_SetteNecromancersForest | SERANA; DG_CAIRN |

### PART 12 - MORE OF THE ROAD  (14 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE121 | K G | E WE_NEAR:WERJ12 | after A1 |
| WE122 | A K | E WE_DONE:WERJ10 | ASHE_HIRED |
| WE123 | R K P | E WE_NEAR:WERoad03 (no combat) | after B1 |
| WE124 | G L | E WE_NEAR:WERoad05 | after L1 |
| WE125 | G K | E WE_NEAR:WE05 | after A1 |
| WE126 | X S | E WE_DONE:WEDL10 | SERANA |
| WE127 | I L | E WE_DONE:DLC1WEJS06 or WE_DONE:DLC1WEJS05 | Lucien-Inigo intro done (JRLucienInigo) |
| WE128 | L S | E WE_DONE:DLC1_WESC03 (NIGHT) | SERANA |
| WE129 | R S | E WE_DONE:DLC1WE03 | SERANA |
| WE130 | G S | E WE_DONE:DLC1WEJS01 | SERANA |
| WE131 | A X | E WE_DONE:DLC2WE08 | SOLST; ASHE_HIRED |
| WE132 | C G | E WE_DONE:DLC2WE07 | SOLST; after R5 |
| WE133 | V R | E WE_NEAR:WEDL03 | Remi-Val intro done (HLIOValBanter Intro); one talk per encounter (WE90 or WE133) |
| WE134 | K P | E DRAGON_TOWN | K_TOG+; after WE59 |

### PART 13 - WHAT THE ROAD MAKES OF US  (16 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WE135 | V K P | E WE_DONE:WEDL02, or song scene ended in SetteBard01/05 | K_CRUSH and V_FLIRT |
| WE136 | S G | E COURIER within 60 s of leaving a dungeon interior | SERANA |
| WE137 | K P | E COURIER | K_CRUSH; not on the same delivery as WE1 or WE2 |
| WE138 | X K P | T WILD | WE_COUNT >= 10; after C3 |
| WE139 | L I | T WILD | WE_COUNT >= 15; Lucien-Inigo intro done (JRLucienInigo); after WE7 and WE61 (the cheese, the goat) |
| WE140 | A G | T WILD | WE_COUNT >= 20; ASHE_HIRED |
| WE141 | C K | T WILD | after WE62, WE63 and WE100 |
| WE142 | V P | T WILD | WE_COUNT >= 10; after WE10 and WE14 |
| WE143 | R S | E CITY (any hold capital, arrival) | WE_COUNT >= 10; SERANA |
| WE144 | K I P | E CAMP+NIGHT | WE_LATE since the last camp; KaiandInigo stage >= 10 |
| WE145 | G R | T WILD | TOLL_OR_AMBUSH_COUNT >= 5; Remi-Gore intro done (HLIOGoreBanter MarkarthIntro) |
| WE146 | L P | T WILD | WE_COUNT >= 20 |
| WE147 | C I | E CAMP | WE_COUNT >= 15; after R13 |
| WE148 | L K | T | 3 game days after WE101; Kaidan-Lucien intro done (JRLucienFollowerKaidanScene1) |
| WE149 | A S | T WILD | WE_COUNT >= 20; SERANA; ASHE_HIRED |
| WE150 | G K P | E CAMP+NIGHT | WE_COUNT >= 30; after A1 |
