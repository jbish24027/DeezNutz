# Content research: Bruma, Moonpath, Wyrmstooth, Sirenroot, Forgotten City, Saints and Seducers Extended Cut, Cursed Tribe Quest Expansion

Read-only research, 2026-10-18. Profile "DEEZ CS NUTZ - PICTA". Nothing in the game was changed.

Sources: quest records (names, stages, journal text, objectives) read straight from the live plugins; worldspace, location and cell records; the mods' own Nexus descriptions (from MO2's meta.ini); compiled quest scripts for Moonpath, Sirenroot, Wyrmstooth and Forgotten City (string search plus two decompiles); and every dialogue line in our 8 followers' plugins and patches (58,566 lines searched).

How to read the conditions:
- "GetStageDone Q N" means the stage has been set. A "journal" line is the text the player sees in the quest log at that stage.
- FormIDs are written as `XXXXXX:Plugin`. Always use the plugin-qualified form. Do not use runtime IDs: the load-order index can shift.
- "Unsure" means I could not prove it from the records, so check it in-game.

---

## Quick table: "where are we" conditions

| Place | Best condition | Worldspace | Location (LCTN) | "Arrived" quest beat |
|---|---|---|---|---|
| Cyrodiil (any) | GetInCurrentLocation / location chain under Cyrodiil | `0A764B:BSHeartland.esm` (EDID BSHeartland, in-game name "Tamriel") | `000F21:BSHeartland.esm` Cyrodiil | `0D3F2C:BSHeartland.esm` CYRSkyrimBorderGateTopLevelQuest stage 600 ("I've reached Cyrodiil, arriving in Pale Pass") |
| County Bruma | location | same | `000F17:BSHeartland.esm` County Bruma | same |
| Bruma city | location | same (the city is inside the BSHeartland worldspace, not its own world) | `000F18:BSHeartland.esm` Bruma | `0D6996:BSHeartland.esm` CYRBrumaFF00 "Visit Bruma" stage 1 (completes) |
| Elsweyr (Moonpath) | GetInCurrentLocation | none. Every Moonpath area is an interior cell with a sky. | `017872:moonpath.esp` AnvilLocation "Elsweyr" (all 15 Moonpath cells point to it) | `06A8CA:moonpath.esp` stage 15 (reach Elsweyr's edge) or 60 (dropped in Tenmar Forest); `01EE82:moonpath.esp` stage 0 ("I have arrived in Elsweyr.") |
| Wyrmstooth island | GetInWorldspace | `000D62:Wyrmstooth.esp` WyrmstoothWorld; underground `0825E1:Wyrmstooth.esp` Dimfrost | `2CEC4A:Wyrmstooth.esp` WTWyrmstoothLocation | `028F01:Wyrmstooth.esp` WTBarrowOfTheWyrm stage 50 ("We've arrived at Wyrmstooth.") |
| Forgotten City | GetInCurrentLocation | none (interior cells) | `000800:Liv_ForgottenCity_AddLocations.esp` ForgottenCityLocation (a light plugin, so always use this qualified form). It covers all 27 FC cells, including the entrance "Forgotten Ruins". | `012BB9:ForgottenCity.esp` 000FCQuest01 stage 200 (inside the city); `05965B:ForgottenCity.esp` 000FCQuest02 stage 400 (sent back in time) |
| Sirenroot ruins | GetInCell (no location on these cells) | none | none | `026BC5:evgSIRENROOT.esm` EVGSirenrootQuest stage 20 (cave collapse, trapped below) |
| Shivering Isles (SEC) | GetInWorldspace | `C2BFF8:Skyrim Extended Cut - Saints and Seducers.esp` ECSSShiveringIsles | `0A5165:Skyrim Extended Cut - Saints and Seducers.esp` EC_SS_ShiveringIslesLocation | `099D19:...Saints and Seducers.esp` EC_SS_MQ101 stage 10 |
| Largashbur (Cursed Tribe) | location | Tamriel | `019263:Skyrim.esm` LargashburLocation; `0C33AF:Skyrim.esm` GiantsGroveLocation (renamed "Sanctum of Malacath" by TCTQE) | `03B681:Skyrim.esm` DA06 stage 20 |

Sirenroot cells (all in `evgSIRENROOT.esm`): `025FD4` Honrich Lake Cave (EVGSiren01), `000D61` Honrich Ruins (02), `009086` Honrich Atasel (03), `0162FC` Honrich Varlorsel (04), `02B77F` Honrich Welkeseli (05), `031168` Honrich Gordarseli (06), `075AB5` Honrich Buroseli (07), `0845FD` Honrich Gardens (08), `014076` Honrich Morbalseli (09), `0A625E` Honrich Aranseli (10), `12DC10` Honrich Ruins (11), `01750A` EVGSirenDaydream (the trance/dream cell, in-game name "Skyrim").

Moonpath cells (all `moonpath.esp`, all Location `017872`): `06AE2D` South of Riverhold, `01DAD1` Elsweyr Estuary, `06BF20` North of Tenmar Forest, `000D62` Tenmar Forest Hideout, `01D079` Tenmar Den, `049CEA` Tenmar Cathedral, `05101B` Sload's Lair, `023EFB` Pillar Falls, `031322` The Skies Above Elsweyr, `042474` Waning Moon Captain's Cabin, `0403B5` Thalmor Airship, `02CEE1` Desert Caravan Supply Post, `0424C0` Botanist's Oasis, `03A854` and `03E4CB` Topal Sea Island.

Forgotten City key cells (all `ForgottenCity.esp`): `000D62` Forgotten Ruins (entrance, in the present), `01791E` The Forgotten City (main), `01AC64` Citadel, `018803` Lakehouse (the time portal), `072356` Underground tunnels, `081DE2` Abandoned Palace, `0798F3` Dwarven Dome, `020849` The Golden Sentinel Tavern, `09BB9E` Cave.

---

# 1. Beyond Skyrim: Bruma

Plugins: `BSAssets.esm` + `BSHeartland.esm` (251 quest records), plus many add-ons. These include `BSHeartland - No Custom Map Markers.esp`, `Moonpath ... JRMoonpathBrumaPatch.esp`, and our own `Authoria - Master Patch - Bruma.esp`.

## Plain summary

**Premise.** The player crosses the southern border of Skyrim into Cyrodiil, the old Imperial heartland, and reaches County Bruma. This is the snowy, mostly Nord county in the Jerall Mountains. It is 4E 201, about 200 years after Oblivion. The Empire is weak, the Thalmor enforce the White-Gold Concordat (no Talos worship), and the Great War has left scars. Bruma is a city of Nords and Imperials living side by side. It has bandit trouble, Talos worship in secret, and old Oblivion-era landmarks. The tone is grounded and political, a lot like Skyrim's own holds. It has many small human stories, a few dark ones, and some comedy (a terrible bard, a lonely farmer). There is no single epic plot. The spine is the Bruma Guard captain's story.

**How to start.** You go to the Pale Pass border gate (south of Helgen/Falkreath) and get through in one of three ways:
- talk your way past the Legate, Centos Durius;
- kill him;
- pay the shady "hunter" Mirich Ran for the smugglers' cave route, Serpent's Trail.

Quest "Welcome to Cyrodiil" (`0D3F2C`) tracks this. The gate route moves the player to Cyrodiil with a script (MoveTo). A failsafe quest, `0D6E80:BSHeartland.esm` CYRBrumaBordersNativeFollowerMove "Failsafe to move followers across border", brings followers along.

**Places.** Pale Pass and Fort Pale Pass (Legion border fort), Serpent's Trail (smugglers' cave), Bruma city (Castle Bruma, Great Chapel / Cathedral of St. Martin, the inns Jerall View and Restful Watchman, the slums "shack village"), Applewatch, Greenwood (meadery), Snowstone Rest (inn), Mountain Watch (mining village), Aleswell. Also Cloud Ruler Temple (old Blades fortress, ruined and haunted), Frostcrag Spire (the Oblivion player's wizard tower, now used by the College of Whispers), Frostfire Glade (Ayleid magic glade with its own worldspace), Fort Cutpurse (bandit base), Underpall (necromancer fort) and Ayleid ruins (Sedor, Anga, Moranda, Piukanda, Rielle, Garlas Ture).

**Factions and guilds.**
- **Bruma Guard** under Captain Adius Vilius, a decent man who quietly shields Talos worshippers.
- **Count Desilus Carvain**, a vain noble who collects Akaviri artifacts.
- **The Synod**, Cyrodiil's establishment mages' guild that replaced the Mages Guild. It has a Bruma conclave led by First Adjunct Cadius Venucius.
- **The College of Whispers**, a rival, more secretive mage order. Their man Astor experiments with Frostcrag's portals.
- **Fighters Guild** (Bruma hall). There is a poster-hanging job.
- **Imperial Legion** at Pale Pass (Legate Precilius Varro). The **Penitus Oculatus** turn up too.
- **The Thalmor**, led by the Justiciar **Armion**, who harasses the priest Neremus and the guard.
- **Thorina's Cutters**, an organised bandit gang.
- **The Cathedral of St. Martin**. Bruma worships Martin Septim, the hero of the Oblivion Crisis ("Praise Martin" mass scene).

**Main quest chain (Adius arc):**
1. **Absent Antiquity** (`086207`). Find Count Carvain's stolen Akaviri artifacts. The thief is the Breton Atienne Guilette, who wants to impress the Cutters.
2. **A Delicate Situation** (`086208`). Adius sends you to the Talos worshippers at the Camp of the Devout (Aera the Devout). You choose:
   - make them worship quietly (what Adius wants);
   - make them stop altogether;
   - let them carry on openly.
3. **Against the Cutters** (`08650F`). Drinks with Adius at the Jerall View, then you storm Fort Cutpurse and kill Thorina.
4. **Service Rewarded** (`07F0FA`). The Count rewards you with gold, the right to buy a house and the blade Hvitbrand. **Twist:** if Aera's people kept worshipping openly, Armion and Thalmor agents arrest Adius for shielding them and send him to Blue River Prison (stage 50). Otherwise Adius gives you a warm farewell (stage 100).

**Other major quests:**
- **Alammu's Veil** (`003A58`). A Dunmer woman's "heirloom" is skooma. It's a smuggling ring and she is blackmailing you.
- **Upon My Honor** (`0C7E4C`). A Legion soldier's wife, Lassinia Iron-Heart, wants news of her husband Harran. He is dead in Serpent's Trail, and he had deserted to the Stormcloaks. Do you tell the family?
- **A Stormcloak in Chains** (`0CE0F1`). At Fort Pale Pass you interrogate or free the Stormcloak prisoner Bjarni Shatter-Stone. A Stormcloak raid hits the fort and the Penitus Oculatus arrive.
- **Ugly Love** (`08AE84`). An Orc mercenary, Dumrag gro-Morrg, thinks a Bruma noble set up his wife's kidnapping. It ends with an accusation, a murder in the castle, or Dumrag killing Simund Gautierre. He can become suicidal, or turn up later as a follower.
- **Undeath at Underpall** (`08BF0C`). Necromancer fort. The High Necromancer is Alavva, Cadius's sister. Kill her or reunite the siblings.
- **Whispers of the Mountain** (`083A17`). Random objects, even a zombie, appear in the Synod conclave. College of Whispers mages at Frostcrag are misfiring portals. You get flung through space as the test subject.
- **The Courier** (`0C9BE1`). Starts when you sleep at the Restful Watchman. Olaf Cold-Heart's "friend" in Sedor is a Stormcloak courier with documents.
- **The Way Home** (`06F9B8`). Cloud Ruler Temple. The ghosts of Blades (Raaslan, Alina) are still fighting their last war. You bring Glenroy's Akaviri katana and lay them to rest.
- **Frostfire Unleashed** (`06C0DE`). Kill the Glade Guardian, then banish a magical blizzard with the knight-ghost Garridan by reciting the Chant of Mara.
- **All the Wrong Places** (`047FAA`). Matchmaking a lonely farmer and a failed Synod applicant. Ends in a wedding at St. Martin's.
- **The Screeching Songman** (`067841`). A horrible bard, Renod-Even-Toned. Get his lute back, or send him to "perform" for bandits.
- **Two of a Kind / The Deepiron Problem** (`0E5911` / `0E5912`). Mountain Watch: ogres, goblins and a gold vein.
- Many small favours and radiant jobs.

**Tone.** Snowbound, homely and political. The Empire's decline is felt everywhere, the Thalmor are a looming bureaucratic menace, and moral greys are everywhere.

## Named quests (Bruma)

| EditorID | FormID | Name | Summary | Started | Key moment | Completed |
|---|---|---|---|---|---|---|
| CYRSkyrimBorderGateTopLevelQuest | 0D3F2C:BSHeartland.esm | Welcome to Cyrodiil | Getting across the border | St 1: "Cyrodiil, the Imperial Heartland, is a land scarred by the horrors of the Great War..." | 20/22 Mirich Ran's "special services" and Serpent's Trail; 30 convinced the Legate; 31 killed the Legate | 600: "I've reached Cyrodiil, arriving in Pale Pass, the northmost region in County Bruma." |
| CYRSkyrimBorderGateQuest | 0C9B1A:BSHeartland.esm | (hidden) gate | Gate mechanics | 10 talked to Centos Durios | 25-30 gate open scene, player moved by script | 35 entered Cyrodiil for the first time; 60 threatened (guards hostile); 70 killed Centos |
| CYRBrumaFF00 | 0D6996:BSHeartland.esm | Visit Bruma | Misc pointer | - | - | 1 completes |
| CYRBrumaMS07 | 086207:BSHeartland.esm | Absent Antiquity | Recover the Count's Akaviri artifacts | 10: "I was approached in Castle Bruma by... Adius Vilius" | 60 thief is "Atienne"; 80 thug in Botram's house; 90 Atienne arrested, go through the trap door | 120 (complete) |
| CYRBrumaMS08 | 086208:BSHeartland.esm | A Delicate Situation | Talos worshippers at the Camp of the Devout | 10 | Endings are separate stages (the record says to use GetStageDone on the individual ending stages) | 100: one of three logs (lie low / stop entirely / allowed to continue) |
| CYRBrumaMS09 | 08650F:BSHeartland.esm | Against the Cutters | Kill Thorina at Fort Cutpurse | 10 | 20 drinks at the Jerall View, go to Fort Cutpurse | 100 Thorina dead; 160 complete |
| CYRBrumaMS10 | 07F0FA:BSHeartland.esm | Service Rewarded | Reward, then the Adius twist | 0 | 20 Count's audience, Hvitbrand, house rights | **50: Adius arrested by Armion and the Thalmor, sent to Blue River Prison**; **100: heartfelt farewell** |
| CYRBrumaMS01 | 003A58:BSHeartland.esm | Alammu's Veil | Skooma smuggling blackmail | 10 | 20 Neldam Beloth reveals the ruse; 27 return / report / open it | 30 returned contraband ("spared my life"); 50 reported, arrested; 100/150 fail |
| CYRBrumaMS02 | 0C7E4C:BSHeartland.esm | Upon My Honor | Harran Iron-Heart's fate | 10 | 20 Serpent's Trail tip; 30 body found, he had joined the Stormcloaks | 100 told the family the truth; 110 hid it; 200 fail |
| CYRFortPalePassMS01New | 0CE0F1:BSHeartland.esm | A Stormcloak in Chains | Interrogate or free Bjarni | 5/6 | 200 interrogated; 210 Stormcloaks breach the fort; 231 reached Varro; 250 Penitus Oculatus arrive | post-quest handler `0CE135` stage 100 sided with the Legate / 150, 200 rescued the prisoner |
| CYRBrumaMS05 | 08AE84:BSHeartland.esm | Ugly Love | Dumrag's kidnapped wife | 10 | 50 accusation, Dumrag storms the castle; 110-190 evidence, then Simund killed | 100 (noble killed, Dumrag killed by guards) or later stages; post-quest `0C9CBD`: 40 Dumrag becomes a follower, 4 suicidal Dumrag |
| CYRBrumaMS06 | 08BF0C:BSHeartland.esm | Undeath at Underpall | Necromancers; Cadius's sister | 10 | 30 servant leads you to the "mistress"; 60 killed, she was his sister; 65/80 spared, reunited | 100 |
| CYRFrostcragMS01 | 083A17:BSHeartland.esm | Whispers of the Mountain | Portal misfires into the Synod hall | 30 | 60 to Frostcrag Spire; 220-250 portal test, you get flung across space | 100 / 260 |
| CYRBrumaMS11 | 0C9BE1:BSHeartland.esm | The Courier | Olaf, Sedor and Stormcloak documents | 100 (after sleeping at the Restful Watchman, prestart `0D3820`) | 199 attacked; 250 documents found | 360 gave documents to Olaf; 399/400 refused |
| CYRCloudRulerFF01 | 06F9B8:BSHeartland.esm | The Way Home | Blades ghosts at Cloud Ruler | 5: "Nestled high in the Jerall Mountains, I found the ruins of Cloud Ruler Temple..." | 20 Alina is a skeleton, fetch Glenroy's katana; 30 West Wing last stand | (later stage, completes) |
| CYRdunFrostfireQST | 06C0DE:BSHeartland.esm | Frostfire Unleashed | Glade blizzard | 100 Glade Guardian dead | 110 Garridan appears; 150 Chant of Mara returned | 202 |
| CYRBrumaMS03 | 047FAA:BSHeartland.esm | All the Wrong Places | Matchmaking | 10 | 60 they get along; 70 wedding invite (St Martin's, 9am) | 80 attended; 85 missed; 100/105 fail |
| CYRBrumaMS04 | 067841:BSHeartland.esm | The Screeching Songman | Terrible bard | 10 | 30 lute thief; 40/50 bard sent to the bandits | 160/170 lute returned; 100 bard killed by the bandits (fail) |
| CYRMountainWatchMS01 | 0E5911:BSHeartland.esm | Two of a Kind | Rescue Ervig from ogres | 1/2 | 10 caged | 80 |
| CYRMountainWatchMS02 | 0E5912:BSHeartland.esm | The Deepiron Problem | Goblins in the mine, ogre raid | 10 | 70 gold vein; 90 ogres raid the village | 200 |

Smaller ones (all `BSHeartland.esm`): CYRBrumaFF01-13, CYRApplewatchFF01-03, CYRJerallsFF01/02/04, CYRSnowstoneRestFF01/02, CYRGreenwoodMeaderyFF01 "Water Run Dry", CYRBrumaWatchtowersFF01 "Blade of the Cutpurse", CYRFortPalePassFF01 "Within the Ruins", CYRAleswellFF01 "Studying", CYRMountainWatchFF01/02, CYRBQ01/02 bounties, CYRWE14 "Sanguine Revelers" (the revelers turn into Dremora), CYRBrumaFF10 "Fighter's Guild Advertising", CYRBrumaFF12 "Missing Dog" (Scruffy).

## Silence zones (Bruma)

- **Border gate opening:** `0C9B1A` stages 25 to 35 (a scene, then the player is moved by script). Don't fire banter until stage 35 or `0D3F2C` stage 600 is done.
- **Cathedral mass:** scene quest `06507B:BSHeartland.esm` CYRDialogueBrumaCathedralMassScene. Use GetQuestRunning. Also the wedding (`047FAA` stage 70 up to 80).
- **Castle audience / Adius arrest:** `07F0FA` stages 10 to 50/100 (Service Rewarded runs scripted scenes).
- **Ugly Love confrontation:** `08AE84` stage 50 to 100 (castle killing).
- **Whispers teleport:** `083A17` stages 240 to 250, and the handler `0CC08B` stages 2 to 10 (the player is flung through space and gets a fall-damage safety perk).
- **Frostfire banishing:** `06C0DE` stages 150 to 200.
- **Fort Pale Pass assault:** `0CE0F1` stages 210 to 250 (combat and Oculatus scene).
- Bruma has dozens of ambient NPC scenes (CYRDialogueBruma*Scene quests). Use the normal "not in scene" check (`IsInScene`) on the speaker and the listener.

## Existing follower lines (Bruma), topics only

- **Kaidan.** `BWB - Kaidan 2 Beyond Skyrim Bruma Patch.esp`, 60 lines (topic KBSB plus KaidanBrumaNaked1-3):
  - "I've been here before, or woke up drunk here"
  - the monks who might recognise him (the monastery naked story)
  - Jerall View ale and food
  - the terrible bard
  - hating the Thalmor
  - one-liners for nearly every Adius-arc quest, Alammu, The Courier, Songman, The Way Home (Cloud Ruler, the Akaviri katana, wants to borrow Glenroy's blade), Ugly Love, Upon My Honor
  - The Way Home line compares freeing the ghosts with the player rescuing him from prison.
  - Also, elsewhere: his first kill happened in Bruma at 16 (looking for Brynjar), his "Synod in Cyrodiil" opinion, and that he was trying to cross into Cyrodiil at Pale Pass when the Thalmor caught him.
- **Gore.** No Bruma-specific lines. But his mother Heide was killed in a Thalmor raid on a Talos-worshipping farm village near Bruma, he was raised across Cyrodiil by the Band of the Raven, and he has "We are very close to the border of Cyrodiil... wonder if we could pop up on the other side and see home" (Falkreath idle).
- **Val.** Cyrodiil/Imperial City childhood; "As long as we stay out of Anvil, I shouldn't have too many problems in Cyrodiil"; Solitude is "the only decent food this side of the Jerall Mountains".
- **Lucien.** Imperial City, White-Gold Tower, Arena, "The woodlands here remind me of home. Ah, Cyrodiil." No Bruma-specific lines.
- **Inigo.** Sellsword years "from the Gold Coast to the Jerall Mountains"; Fergus buried near Greenmead Cave on the road to Skingrad; no Bruma-specific lines.
- **Xelzaz, Remi, Redcap.** Only general "Cyrodiil" mentions. Redcap: redcap mushrooms were shipped in from Cyrodiil.

## 12 banter hooks (Bruma)

1. **Kaidan at Pale Pass.** This is the border he was trying to cross when the Thalmor took him. Finally walking through it, with the player who freed him. Gate stage 35.
2. **Kaidan vs the monastery.** Party members tease him about the naked-monk story as they pass. Lucien wants the scholarly version, Inigo wants the funny one.
3. **Gore and the Camp of the Devout.** His mother died in a Thalmor raid on a Talos farm village near Bruma. A Delicate Situation (`086208`) is the exact dilemma that killed her. Strong emotional beat, and his choice sides with "let them worship".
4. **Adius's arrest** (`07F0FA` stage 50). The whole party reacts. Gore blames himself or the player, Kaidan swears, Val shrugs "the Empire eats its own", Xelzaz delivers a cold political read.
5. **Kaidan the Akaviri.** Count Carvain's Akaviri artifact collection (Absent Antiquity) and the Blades at Cloud Ruler. "These are my mother's people's things, and a Nord count keeps them in a cabinet."
6. **Lucien and Val, homesick Imperials.** Bruma is the closest either has been to home in years. Val stole Lucien's lunch money for a year at school. A schoolboy reunion in a Cyrodilic tavern.
7. **St. Martin's Cathedral.** Lucien lectures on Martin Septim and the Oblivion Crisis. Kaidan, Akaviri and raised by a Concordat-hating Nord, has opinions on Dragonborn emperors. Inigo asks whether the player is "a Martin".
8. **Synod vs College vs Winterhold.** Kaidan already calls the Synod "power-scavengers". Xelzaz (Telvanni) and Lucien (Imperial-educated) debate which order is worse.
9. **The Screeching Songman.** Inigo, a bard himself (Skyrim's Got Talent), offers to give Renod lessons. Kaidan already wants to sew his mouth shut. The party rates performances.
10. **Inigo's Cyrodiil memories.** He and Fergus worked "from the Gold Coast to the Jerall Mountains". In County Bruma he recognises a road and tells a Fergus story, softly.
11. **Ugly Love.** Gore, raised by Orc "Fathers", backs Dumrag. Remi wants evidence first. The party splits on vigilante justice. Pay it off if Dumrag later joins as a follower.
12. **Frostcrag Spire portals.** Remi and Xelzaz argue Ayleid/Synod teleport tech versus Dwemer and Telvanni methods. Redcap, flung across space with the player, is not amused.

---

# 2. Moonpath to Elsweyr

Plugin: `moonpath.esp` (7 quests). Patches: `JRMoonpathtoElsweyrPatch.esp`, `JRMoonpathBrumaPatch.esp` (Bruma route patch), `JKJ - Moonpath.esp` and `Project ja-Kha'jay - Moonpath` (Khajiit visual overhaul), `Moonpath Music - Sky and Lighting fix - merged.esp`, `Authoria - Reqtificated - Moonpath.esp`.

## Plain summary

**Premise.** A Khajiit caravan offers to take you from Skyrim, through the Imperial heartland, to Elsweyr. Elsweyr is under the Thalmor's thumb. Its people are starving, some have turned bandit, and a Khajiit rebellion is growing in Tenmar Forest, the southern jungle. You become the rebellion's outside friend and base guest. The "Pahmar" (big tiger-like Khajiit) guard you. It is jungle and desert adventure with a resistance-movement tone: airships, pirates, a Sload, a Thalmor Justiciar hunt. The whole place is a set of interior "outdoor" cells, not an open world.

**How to start.** Hear rumours of a caravan in Falkreath leaving for Elsweyr (quest `06A8CA` stage 0). Find it, pack your gear on the carriage, and leave Skyrim (stage 10).

**The journey ("By the Light of the Moon", `06A8CA`):**
- A long, boring ride through Cyrodiil (stage 10).
- The northern edge of Elsweyr at night (15).
- Ku'rana asks you to clear a canyon blockade of starving Khajiit bandits (20 to 30).
- The jungle, a collapsed bridge, and you scout a ford through giant spiders and aggressive lizards (40 to 50).
- The Pahmar invite you (55).
- Dropped in Tenmar Forest (60).

The carriages are scripted activators that work like doors.

**Main quests:**
- **The Sweet Taste of Elsweyr** (`01EE82`). Arrive at the hideout. The girl Yura sends you to Ameir (moon sugar trader faction) deep in the waterways. Aleyt explains the Pahmar. You hear about refugees and Thalmor rule.
- **Incursion** (`01ED3C`). The big Khajiit door guard Mervar distrusts you until Qa'mel vouches for you. Clear the Thalmor from Tenmar Den with Dervar (a deadly fighter) and Deepclaw. Destroy the Thalmor base at Pillar Falls and seize their transport. Fly on the airship "Waning Moon" with Khulan to a desert caravan post near the city of Dune, hunting Justiciar Lenial. His log shows he fled. His ship rams yours, there is a boarding battle, and he dies. Ending: "A rebellion is growing, and soon all of Tamriel will be ablaze."
- **Rebuilding the Past** (`03C6E1`). Rescue the rebel mage Jo'ran from Argonian pirates whose base is an old **Dwemer supply post** on an island in the Topal Sea. He rebuilds it as a rebel base.
- **The Dinner Guest** (`0589C5`). Erid'or tests you, then reveals a **Sload**, Malsato, in Tenmar Cathedral (a Khajiit burial site). He planted a plague and blackmails you into bringing him new "tastes" (fifty years preparing a necromantic culinary tour). Poisoned hyena meat weakens him, Silkskin tracks the infected animal near the mammoth skeleton, then you kill him. If you kill him early, the Thrassian Plague is released (fail stage 100).
- **Desert Style** (`0440C0`). Shil'ara, an Argonian botanist who turned an oasis into a garden, makes Siligonder chitin armour.
- **What Shall We Do with the Drunken Sailor?** (`085C5D`). Dialogue only (Skullcat).

**NPCs:** Ku'rana (caravan leader), Yura (girl), Ameir (moon sugar faction), Aleyt (Pahmar lore), Mervar (gruff guard), Qa'mel, Dervar and Deepclaw (fighters), Khulan (rebel leader / airship), Erid'or, Silkskin (Pahmar tracker), Jo'ran (rebel mage), Shil'ara (Argonian botanist), Jelikirr (smith), Justiciar Lenial (villain), Malsato the Sload (villain).

**Tone.** Warm, exotic, rebellious. "This is a land in just as much turmoil as Skyrim." Thalmor occupation is the main theme.

## Named quests (Moonpath)

| EditorID | FormID | Name | Started | Key | Completed |
|---|---|---|---|---|---|
| AnvilMoonpathQuest | 06A8CA:moonpath.esp | By the Light of the Moon | 0 rumour; 10 joined the caravan | 15 Elsweyr's northern edge; 20-30 blockade; 40-50 broken bridge; 55 Pahmar invitation | 60: "I've arrived in Tenmar Forest." |
| AnvilQuestameir | 01EE82:moonpath.esp | The Sweet Taste of Elsweyr | 0: "I have arrived in Elsweyr." | 10 Ameir, moon sugar, Thalmor overlords | 20 (Pahmar accept you) |
| AnvilDenQuest | 01ED3C:moonpath.esp | Incursion | 0 | 40 Tenmar Den cleared; 60-70 Pillar Falls base; 100 airship Waning Moon; 110 desert near Dune; 130 Justiciar rams and boards | 150: "The Justiciar is dead. A rebellion is growing..." |
| Anvil_buildquest | 03C6E1:moonpath.esp | Rebuilding the Past | 0/10 | 20 pirate base is a Dwemer supply post; 30 Jo'ran freed | 60 base finished |
| AnvilSloadquest | 0589C5:moonpath.esp | The Dinner Guest | 5 | 30 Malsato's blackmail; 50 poisoned meat; 70 infected beast | 95 forest saved; **100 FAIL: plague released** |
| Anvil_armorquest | 0440C0:moonpath.esp | Desert Style | 0 | 10 Shil'ara | 30 |
| Anvil_skullcatdialogue | 085C5D:moonpath.esp | What Shall We Do with the Drunken Sailor? | (no stages) | | |

## Silence zones (Moonpath)

- **Carriage legs:** `06A8CA` stage 10 until 15, 35 until 40, and 55 until 60 (each "get back in the carriage" leg is a fade-to-black move). Followers travel through the carriage activators like a door. Unsure: check that followers arrive with you.
- **Airship flights and boarding fight:** `01ED3C` stages 100 to 105 and 130 to 135; cells `0403B5` Thalmor Airship and `042474` Waning Moon Captain's Cabin.
- **Sload confrontation:** `0589C5` stage 30 (dialogue blackmail) and 80 to 90.

## Existing follower lines (Moonpath / Elsweyr)

There are no Moonpath-specific lines for any of our followers. Related:
- **Inigo:**
  - born in the Elsweyr desert (a blue baby was a "bad moon omen" in his devout village)
  - raised in Riverhold
  - "I even travelled to Riverhold. I found your parents shortly after they died" (to a Riverhold-born player)
  - moon sugar / Elsweyr fondue line
  - "You and I were born to leave Elsweyr I reckon."
- **Kaidan:**
  - youth in Elsweyr
  - KaiDrunkStory: a trip to an Elsweyr inn where "those Khajiit put [something] in our drinks"
  - "Elsweyr is an arid land of deserts and rocky canyons, where the sun shines warmly, always."
  - moon sugar fondue line
  - "Kaidan and Inigo Meet.esp": they bond over Elsweyr ("This land couldn't be more different to Elsweyr's deserts and jungles")
- **Remi:** loves Elsweyr cuisine and sweets ("Grand Champion" of fondue eating); wonders about rainforest alchemy ingredients.
- **Xelzaz:**
  - a Sload story (`BPUFXelzazFollowerStoryTharsis`)
  - "the Dominion in Elsweyr" in a slavery line
  - Elsweyr shop etiquette
- **Gore:** wants to see Elsweyr (with Hammerfell and Valenwood), the homelands the Ravens described.

## 12 banter hooks (Moonpath)

1. **"South of Riverhold"** (cell `06AE2D`). The caravan passes Inigo's childhood town, where his foster parents Leah and Da Vinci are buried. Quiet, heavy Inigo moment. Kaidan, who knows him, steps in.
2. **Inigo and Kaidan, homecoming duo.** They knew Elsweyr together. Who remembers which inn drugged whom.
3. **The Pahmar.** Inigo, a small blue Khajiit cursed as a "bad moon omen", meets giant tiger-Khajiit who revere the moons. Does he feel judged or at home?
4. **Gore finally sees Elsweyr.** His dream from the Ravens' stories. Wide-eyed Gore with Kaidan as tour guide.
5. **Starving bandits at the blockade** (`06A8CA` stage 20-30). Gore (an ex-mercenary "borderline bandit") argues mercy. Val, a pirate, understands them. Xelzaz is pragmatic.
6. **Airships.** Val, a sea captain, on a flying ship: professional jealousy, wants to steer, nautical terms for clouds. Redcap screams at the height ("Great Water... up?").
7. **Topal Sea pirates in a Dwemer post** (`03C6E1`). Remi and Lucien spot Dwemer work in Elsweyr. Remi: "I thought the Dwemer never came this far south!" Val defends pirates in general.
8. **The Sload.** Xelzaz has a real Sload story and despises them. Lucien wants to study it. Remi is horrified by the "tastes" menu. Inigo jokes about the dinner party.
9. **Thrassian Plague.** Lucien knows the history (the Sload plague of the First Era). He frets if the player kills Malsato early (fail stage 100).
10. **Moon sugar economy.** Ameir's trade. Kaidan and Inigo on skooma (Kaidan's drug history, Inigo's sobriety). Remi just wants the candy.
11. **Justiciar Lenial dies** (`01ED3C` stage 135/150). Kaidan, a Thalmor torture survivor, gets real catharsis. Gore (mother killed by the Thalmor) too. "Soon all of Tamriel will be ablaze": who wants that fire?
12. **Desert heat.** Redcap, from Solstheim ash and ice, wilts. Xelzaz, cold-blooded, finally warm and smug. Lucien sunburns. Food talk: Xelzaz versus Remi on Elsweyr fondue "my way".

---

# 3. Wyrmstooth (+ Karura's Refined, Ascend Hidden Peaks)

Plugin: `Wyrmstooth.esp` (80 quests, ESM-flagged). Add-ons: `Karura's Wyrmstooth Refined.esp` (no new quests; a refinement / NPC visual pass), `Ascend - Hidden Peaks of Wyrmstooth.esp` (climbable hidden peaks; no quests), `Wyrmstooth Dragonborn Compatibility Patch.esp`, `LydiaPatchForWyrmstooth.esp`, `Requiem - Wyrmstooth.esp`, Lux, Seasons and others.

## Plain summary

**Premise.** A dragon, Vulthurkrah, is wrecking trade routes. The Imperial agent Lurius Liore hires the Dragonborn (with a band of mercenaries) to kill it for 10,000 gold. The dragon flees to Wyrmstooth, a big, fully voiced island north of Solitude across the Sea of Ghosts. There you find a destroyed Imperial mining settlement, an enormous barrow, and an underground world.

**How to start.** By default: level 10 and "The Way of the Voice" completed. This can be changed in Wyrmstooth's MCM settings menu. The Imperial courier Theodyn Bienne tracks you down starting at the Bannered Mare.

**Act 1, "Wyrmstooth"** (`022528`). Meet Lurius at the Bannered Mare. Join the mercenaries (Athir and others) on the Falkreath road. Confront the dragon at Ancient's Ascent. It escapes to "a place called Wyrmstooth".

**Act 2, "Barrow of the Wyrm"** (`028F01`):
- Meet Lurius at the Solitude docks and sail to the island (stage 10 to 50).
- Stonehollow (the mining town) has been burned by the dragon (70).
- The barrow is sealed. The key is the sword **Goreduster**, which raises the ones it kills (90 to 110).
- The shady old mage **Alberthor** guides you (120). He casts a spell that puts **your mind into a Draugr** to open a gate (135 to 160).
- Down into the dragon's den in **Dimfrost**, a Blackreach-like underground ecosystem (Xelzaz compares it).
- Dragon Priest, an ancient Oblivion gate, a flooding room.
- Vulthurkrah escapes and raises the dead. You defend the survivors at Stonehollow (230). He dies (260). Reward from Lurius (270).

**After:**
- **Reclaiming the Past** (`28D0B5`): buy and rebuild **Fort Valus** as your castle (Rebuilding Wyrmstooth `11E1D3`).
- Mercenary favours: Athir ("Retrieving Embersunder"), Shargam ("Repaying a Debt", kill Ulfgar in Markarth), Daenlit ("Robbed Blind", steal Erikur's necklace), Elmera ("Stickler in the Mud", Deadlands spiddal sticks), Signy ("A Debt Unpaid").
- **The Naked Nord** (`C651DA`): comedic. Gjalrunn is paralysed and pantsless by a witch, warlocks try to enchant his trousers, and he may take revenge later.
- **Someone with Backbone** (`2F1A74`): the voice of Vulom asks you to gather his bones. He is a lich.
- **A Priceless Commodity** (`48F992`): miners versus a Spriggan Matriarch (side with Kyne's grove or the miners).
- **A Howl Load of Trouble** (`2E49AF`): Dunyick dies; his wolf Faelor can join you.
- **Unwanted Guests** (`3943A0`): Thalmor spies on the island. **Wrap Me Up**: Alberthor's wisp wrappings.
- Bounties: bear, Marauder Clanlord, Master Vampire at Bloodfrost Burrow, warlock at Krakevisa.

**Locations:** Stonehollow (with Longhouse, Hall of the Dead, Frostvein Mine), Fort Valus, Fort Moonwatch, Twinpeak Tower, Wyrmstooth Barrow, Dimfrost, Krakevisa (warlocks), Bloodfrost Burrow (vampires), Cragwater Cavern (marauders), Gronndal Grove (spriggans), Tomb of Vulom, Hag's Perch, a Dark Brotherhood Sanctuary, Abandoned Lighthouse, Chillwater Mill. Kazmalgur is on the mainland.

**Tone.** Classic Nordic dungeon epic, salt-and-snow island, mercenary camaraderie, a bit of comedy.

## Named quests (Wyrmstooth)

| EditorID | FormID | Name | Started | Key | Completed |
|---|---|---|---|---|---|
| WTDragonHunt | 022528:Wyrmstooth.esp | Wyrmstooth | 10 courier, go to Lurius | 100 Ancient's Ascent; 110/120 the dragon fled to Wyrmstooth | 130 |
| WTBarrowOfTheWyrm | 028F01:Wyrmstooth.esp | Barrow of the Wyrm | 10 Solitude docks | 50 arrived; 70 Stonehollow destroyed; 100 Goreduster; 135 draugr possession; 160 switch found; 230 defend Stonehollow; 260 dragon dead | 270 |
| WTPlayerHome | 28D0B5:Wyrmstooth.esp | Reclaiming the Past | 10 | 20 deed bought | 40 |
| WTRebuild | 11E1D3:Wyrmstooth.esp | Rebuilding Wyrmstooth | (no journal) | | |
| WTTheNakedNord | C651DA:Wyrmstooth.esp | The Naked Nord | 1/10 | 30 warlocks; 40/50/55/56 pants decisions | 70-79 (many endings) |
| WTUberEncounter | 2F1A74:Wyrmstooth.esp | Someone with Backbone | 5/10 | 20 bones; 40 Vulom is a lich | 50 |
| WTPricelessCommodity | 48F992:Wyrmstooth.esp | A Priceless Commodity | 1/10 | 15 kill the Matriarch / 40 kill the miners | 30, 47 (miners' side); 60 (spriggans' side) |
| WTWolfFollower | 2E49AF:Wyrmstooth.esp | A Howl Load of Trouble | 1/10 | 30 Dunyick dead | 40 (Faelor can follow) |
| WTKillThalmor | 3943A0:Wyrmstooth.esp | Unwanted Guests | 10 | 20 | 30 |
| WTWrapMeUp | 3920D5:Wyrmstooth.esp | Wrap Me Up | 10 | 20 | 30 |
| WTAthirFavor | 3A1467:Wyrmstooth.esp | Retrieving Embersunder | 10 | 20 | 30 |
| WTShargamFavor | 3A1468:Wyrmstooth.esp | Repaying a Debt | 10 | 15/20 | 30 |
| WTDaenlitFavor | 3A1469:Wyrmstooth.esp | Robbed Blind | 10 | 20 | 30 |
| WTElmeraFavor | 3A146A:Wyrmstooth.esp | Stickler in the Mud | 10 | 20 | 30 |
| WTSignyFavor | B5DA18:Wyrmstooth.esp | A Debt Unpaid | 10 | 20 | 30 |
| WTBlindRobbersCache | 46DA2A:Wyrmstooth.esp | Blind Robber's Cache | 10 | 20 | 30 |
| WTBounty* | 4B9DED / 4B9DEE / 4B9DEF / 4B9DF0 | Bandit / Animal / Warlock / Vampire Bounty | | | 20 |

## Silence zones (Wyrmstooth)

- **Boat crossing:** `028F01` stage 10 until 50.
- **Draugr possession:** `028F01` stages 135 to 160. The player's mind is in a Draugr and the body is left behind. Mute all follower banter.
- **Dragon escape and Stonehollow defence:** stages 230 to 260 (combat; allow only combat barks).
- **Reward scene:** 260 to 270.
- Wyrmstooth's own scripts mention followers (barrow refectory move script and others), so it manages follower positions itself in the barrow.

## Existing follower lines (Wyrmstooth)

- **Xelzaz.** `BPUFXelzazFollowerWyrmstooth.esp`, about 60 lines covering the whole main quest:
  - the courier, the 10,000 gold split, "a trap" suspicion, the East Empire Company running theme
  - "like Helgen all over again"
  - Goreduster ("a glorified key")
  - Alberthor not to be trusted, the "children's riddle"
  - dead Thalmor, the Oblivion gate (Mehrunes Dagon), Dimfrost "just like Blackreach", spiddal sticks
  - "Lurius was carrying around 10,000 gold all this time?"
  - Combat: "It's an ambush! Clever bastards!"
- **Others:** none found for Wyrmstooth.

## 12 banter hooks (Wyrmstooth)

1. **Sea of Ghosts crossing.** Val, the captain, critiques the boat and crew. Redcap: the "Great Water" was the end of the world to him, and now he is crossing it again.
2. **Redcap and the island.** A cold, ashy, salty island feels like "Big Ash Rock" (Solstheim). Homesick Riekling.
3. **10,000 gold split.** Xelzaz already worries about sharing. Val wants a pirate's share. Gore, an ex-mercenary, knows how merc contracts really go. Inigo: "I would do it for free."
4. **Draugr possession.** When the player comes back, everyone asks what being a Draugr felt like. Lucien takes notes, Kaidan is disturbed, Redcap pokes the player to check.
5. **Alberthor.** Xelzaz distrusts him. Lucien admires his scholarship. Kaidan's Brynjar rule: "If you're not a little afraid, you're not understanding the situation."
6. **Dimfrost.** Remi and Lucien compare it to Blackreach. Remi wants Dwemer bits; none here, and she is disappointed.
7. **Stonehollow burned.** Xelzaz: "like Helgen". Kaidan, a Helgen-adjacent survivor of the Thalmor, and Gore talk about towns they saw burn (the Ravens' war camps).
8. **The Oblivion gate.** Lucien and Val (Imperial City kids) on the Oblivion Crisis legends their grandparents told. Martin, the Dragonfires.
9. **The Naked Nord.** Comedy gold. Val ("at least I have my pants on this time"), Inigo and Kaidan on pants-based enchantment. Who would fight a witch for trousers?
10. **Fort Valus as a home.** Val wants a dock, Remi a workshop, Inigo a garden, Kaidan a tavern. Party "room assignments".
11. **Spriggan Matriarch versus the miners** (`48F992`). Gore and Inigo side with Kyne's grove. Lucien and Val side with the miners' livelihoods. Remi just wants the ore.
12. **Faelor the wolf.** Inigo, Kaidan and Redcap (who loves his boar Bigpig) adopt the wolf emotionally. Redcap introduces Faelor to Bigpig in his head.

---

# 4. SIRENROOT: Deluge of Deceit

Plugin: `evgSIRENROOT.esm` (one quest). Patches: `evgSIRENROOTtraversalpatch.esp`, `SIRENROOT - HD Texture Pack.esp`, `Requiem - Sirenroot.esp`, `Threads of The North - Sirenroot - Requiem.esp`, `DBVO Fix - Sirenroot.esp`, Lux patches.

## Plain summary

**What it is.** A 2 to 5 hour, dialogue-heavy, voiced **Ayleid ruin dungeon dive** under **Lake Honrich, Riften**. It is built around water, swimming, platforming and puzzles. The author compares it to Tomb Raider and Dragon Age. There are no level requirements and it suits early characters (about level 3 to 15).

**Start.** The Black-Briars post a notice for diving work. Speak to **Frissa Black-Briar at Elgrim's Elixirs in Riften**. A mysterious singing plant has been found at the bottom of the lake.

**Story:**
- You join a hired dive team camped north of the Riften docks by Merryfair Farm:
  - **Tilael**, a Maormer (Sea Elf) mage
  - **Yineel**, an Argonian, Ingun's assistant, resourceful
  - **Peletius**, a greedy Imperial treasure-hunter
  - **Cayrice**, a mage who loses her documents and book
- You dive to the lowest point of the lake and pull up the singing plant. The cavern collapses and you are trapped in Ayleid ruins below (stage 20).
- You find the team members one by one. Puzzles: four Varla stones raise the water level in the Atasel Hall, mirrored puzzles, possessing or controlling the other characters.
- A **ghostly Ayleid woman** puts people into a trance and tries to talk them into giving their souls (Tilael's soul gem). The earlier diver **Crilduin**, a Maormer, already fell for it.
- A hint about a Morag Tong assassin chasing someone.
- Put all four Varla stones in, go through the portal (100), lay the Ayleid spirit to rest (130), escape as the ruins flood (140), and get paid by Frissa (150).
- Each team member can live or die depending on your choices and persuasion.

**Tone.** Claustrophobic, wet, eerie and character-driven. The "Deceit" is that the plant is magic, not real flora ("faux flora", in Xelzaz's patch), and the spirit lies.

## Named quest

| EditorID | FormID | Name | Started | Key | Completed |
|---|---|---|---|---|---|
| EVGSirenrootQuest | 026BC5:evgSIRENROOT.esm | Deluge of Deceit | 1 notice; 5 Frissa hired you | 10 team found; 15 dive; **20 collapse, trapped**; 25 main hall, Tilael rests; 35 first flood; **45 trance, ghostly woman**; 80 third stone; 100 portal; 130 spirit laid to rest, flooding; 140 escaped | **150 (CompleteQuest)**: "I spoke with Frissa Black-Briar about the Ayleid ruins, and she compensated me..." |

Optional objectives: 70 convince Cayrice to leave, 75 help Peletius, 80 convince Tilael, 85 convince Yineel, 81/82 Crilduin's body and Tilael's soul gem.

## Silence zones (Sirenroot)

- **The collapse:** stage 15 until 20. Stage 20's script moves **only the player** (MoveTo to a marker, wake-up animation, then a 10-second wait before controls return). Followers are left behind. Xelzaz's patch has a whole "PlayerAlive" reunion topic because of this. **Unsure:** whether other followers reappear after a cell change. Treat stage 20 until the reunion as "follower may be absent". Gate banter on GetInSameCell/distance.
- **Trance / daydream:** stage 45, cell `01750A:evgSIRENROOT.esm` (EVGSirenDaydream). The player is alone in a dream, so mute.
- **NPC-control sections:** the player controls Tilael, Yineel or Peletius (scripts evgSR05tilaelcontroldialogue, evgSR05yineelstartcontrol1, evgsr06controlpelscd1). Mute during them. Stage ranges are not cleanly bounded; use "player in Honrich Atasel/Welkeseli/Gordarseli + controls disabled". Unsure, check in-game.
- **Escape:** stages 130 to 140 (flooding countdown, combat only).

## Existing follower lines (Sirenroot)

- **Xelzaz.** `BPUFXelzazFollowerSirenroot.esp`, about 150 lines covering the full quest:
  - diving work (his Tel Sul diving days), the singing plant, the diverse team
  - "That Saxhleel piques my interest", "Crilduin... Krill" joke
  - the reunion after the collapse (Roovi can't connect)
  - the shared trance ("Many years in Morrowind has taught me not to trust long dead elves")
  - Tilael's soul gem, Peletius's greed ("Typical")
  - Ayleid construction versus the Dwemer
  - the Morag Tong joke, faux-flora theory
- **Others:** none.

## 12 banter hooks (Sirenroot)

1. **Diving.** Who can swim? Xelzaz (Argonian, a natural), Val (sailor), Redcap (Riekling, terrified of the "Great Water"), Lucien (bookish, holds his breath dramatically).
2. **Ayleid ruins.** Gore says Cyrodiil's ruins were all Ayleid (his existing lore). Lucien and Val grew up near them. Remi, who hates history, is bored without Dwemer.
3. **Black-Briars.** Val and Kaidan on Maven's family as employers. Xelzaz says take the coin and stay wary.
4. **Separated after the collapse.** The reunion: each follower reacts to the player turning up alive. Kaidan's protectiveness, Inigo's relief joke.
5. **Peletius's greed.** Val, a pirate who loves loot, defends him half-heartedly. Gore despises it.
6. **The soul-gem bargain.** Remi (soul gems power animunculi, and she feels guilty about it) versus Lucien on the ethics of trapped souls.
7. **The ghostly woman's trance.** Followers ask whether the player listened to her. Mirrors Xelzaz's existing beat for the others.
8. **Tilael the Maormer.** Val and Xelzaz on Sea Elves and their pirate history versus Val's navy past.
9. **Cayrice's lost book.** Lucien bonds with a fellow bookworm and is delighted to help find a book.
10. **Faux flora.** Remi (amateur alchemist) and Xelzaz (alchemy snob) argue whether the Sirenroot sample is alchemically worthless.
11. **Morag Tong rumour.** Xelzaz, a Morrowind lawman, explains the Tong. Kaidan, an ex-assassin (Blooded Dawn), has a dark take.
12. **Afterwards, in Riften.** Who wants never to swim again (Xelzaz's existing "avoid more diving work" line), and who wants to go back for the loot.

---

# 5. The Forgotten City

Plugin: `ForgottenCity.esp` (58 quest records). Add-ons: `Forgotten City Music Fix.esp`, `Forgotten City - Hidden Map Marker.esp`, `ForgottenCity - Good Ending Tweaks.esp`, `ForgottenCity - Immaculate Dwemer Armor patch by Xtudo.esp`, `Liv_ForgottenCity_AddLocations.esp` (adds the location record we gate on), `SunHelm_ForgottenCity.esp`, `Project ja-Kha'jay - Forgotten City - Patch.esp`, `RSC Forgotten City Patch.esp`, `Authoria - Reqtificated - Forgotten City.esp`, Water/Lux/Northern Roads patches.

## Plain summary

**Premise.** An award-winning (Writers' Guild) 6 to 8 hour murder-mystery and time-loop story in a hidden underground **Dwemer city**, settled by a small community of people about 20 years before the present.

**Start.** At level 5 or above a courier brings Cassia's letter (quest `012BB9` stage 10), or you find the "Forgotten Ruins" in **the Reach** on your own (stage 15). Cassia, an Imperial woman, asks you to find her brother **Altrius**, who went into the ruins. You take a "leap of faith" down into the city (stages 100 and 110).

**Present day (stage 200).** The city is dead. The settlers are gone and the golden Dwemer statues stand everywhere. An old man has hanged himself (too old to be Altrius). A ghost on the Citadel balcony guards the Lakehouse key. The Lakehouse door works as a portal.

**The Golden Rule (the Dwarves' Law).** Dwemer inscriptions in the Citadel say **"The many shall suffer for the sins of the one."** If anyone commits a crime, the golden statues (the Arbiter's guardians) come alive and kill everyone, and the city is destroyed. Everyone lives in fear of it ("Hey, keep your voice down! Do you want to get us all killed?").

**The past and the loop (quest "Forget-me-not", `05965B`):**
- Through the Lakehouse you arrive **20 years in the past, 1 Last Seed 4E 180** (stage 400).
- **Jarl Metellus**, the city's founder, whose magic made the portal, asks you to find out who will doom the city (600).
- You investigate the residents. Each has a secret.
- When the city is about to be destroyed (someone breaks the Law), Metellus goes to the Lakehouse and **kills himself to open a portal back in time** (5000/5200). You can go through again. **That is the time loop:** every time you go through, the day resets and you keep your knowledge.
- Paradox: if Metellus dies before making the portal, you couldn't have used it, so you are thrown back to the present (5500).
- **The Arbiter**, the Dwemer machine-mind that enforces the Law, can send you back (6000). There is a **statue of the player** in the city ("You... you're the one from the statue!"), a bootstrap paradox.

**Endings (`012BB9`):**
- **Best/good:** convince the Arbiter to wind back the Dwarves' Law (4000). You prevent the disaster and return to the present to find Altrius alive (2000). You reunite him with Cassia (4030/4050), and Cassia enters the city.
- **Escape ending:** break open the cracked bathroom wall in the Citadel so everyone can flee (2015/2020/3000; status `0A8055` "The bathroom wall has been broken open").
- **Grim outcomes:**
  - kill your suspect at Metellus's request (`0A7AE7` stage 20)
  - fail the quest by refusing (1500)
  - Altrius escapes but Cassia is missing or dead (`0A02A5` stages 1000/1500)

**Residents (key personalities and secrets):**
- **Metellus**: the Jarl, an idealist. He wanted to "create order... prove to the world such a thing is possible". He has a locked room where he hides Ulrin's missing wife **Maisi**.
- **Brol the Scholar**: translates the Dwemer inscriptions and needs proof the Law is real.
- **Ulrin**: missing wife; suspected of killing her.
- **Gulvar**, **Marius**, **Deglund** (alchemist who sells a defective Elixir of Acrobatics), **Domitus** (aggressive, all hot air) and **Safira** (from the Markarth Warrens).
- **Rykas** (paranoid, wears Immaculate Dwarven armour, sends threatening notes to **Vernon** the produce seller; a hidden sexuality subplot).
- **Habiq and Miranda** (a lost ring under a door), **Dwemora** (asks for skooma, wants you to break into her father's locked room) and **Asanshi** (skooma addict).
- **Luki** (cares for the dying **Brandas**), **Guul** (Dooley's hidden fortune), **Gaia** (wants the Immaculate armour), **Hjormund** (tension with the workers), and **the Hermit** (lures you into a trap).
- There is also a radioactive quarry where Brol went missing.

**Tone.** Smart, melancholic, philosophical (collective punishment, utilitarian ethics), with paradox and moral dilemmas. The author: "designed to be played solo."

## Named quests (Forgotten City)

| EditorID | FormID | Name | Started | Key | Completed |
|---|---|---|---|---|---|
| 000FCQuest01 | 012BB9:ForgottenCity.esp | The Forgotten City | 10 letter / 15 found the ruins / 20 / 30 Cassia | 100/110 leap of faith; 200 explore; 250 hanged man; 300 ghost has the key; 375 Lakehouse door; 2000 Altrius alive; 2015-2020 bathroom wall; 3000 escorted Altrius out; 3100; 4000 Arbiter wound back the Law | **4050 (CompleteQuest)**: "Cassia has rewarded me for returning Altrius to her, and has entered the city." |
| 000FCQuest02 | 05965B:ForgottenCity.esp | Forget-me-not | 400: "I appear to have travelled 20 years into the past, to 1 Last Seed 180E." | 550/575 Metellus; 600 investigate; 1100 lure the suspect; 5000 follow Metellus to the Lakehouse | 1500 refused (fail path); **5200 FailQuest** (Metellus killed himself, the loop); 5500 paradox return; **6000** "The Arbiter has returned me to my own time." |
| 000FCQuestStart | 0DCFA3:ForgottenCity.esp | The Forgotten City | (starter) | | |
| 000FCQuestStatusExodus | 0A8055:ForgottenCity.esp | (status) | | 1: the bathroom wall broken | |
| 000FCQuestStatusLawBrokenOnce | 0A7AE8:ForgottenCity.esp | (status) | | objective 10: "Broken the Dwarves' Law at least once." | |
| 000FCQuestStatusLakehouse | 0A6FF5:ForgottenCity.esp | (status) | | objective 10: "Been through the portal at least once" | |
| 000FCQuestStatusQuarryArmor | 094809:ForgottenCity.esp | (status) | | 20 radiation exposure; 30 reached the Arbiter | |
| 000FCQuestStatusCreditsPlayed | 0E5786:ForgottenCity.esp | (status) | | credits roll | |
| 000FCQuestMetellusDialogue | 05ECD0:ForgottenCity.esp | (dialogue) | | 100-150 the suspect named; 200 confronted Metellus about Maisi | |
| 000FCQuestAltriusDialogue | 0A02A5:ForgottenCity.esp | (dialogue) | | 1000 Cassia missing; 1500 Cassia dead | |

Per-resident dialogue-state quests (all 000FCQuest*Dialogue) track the side mysteries: Ulrin `072D0A`, Rykas `096940`, Vernon `0B658C`, Dwemora `097450`, Guul `0BACC6`, Habiq `0B8BD7`, Luki `0C0737`, Hermit `0BD00A`, Deglund `07646C`, Asanshi `0C5941`, Gaia `0A18AC`, Domitus `0C123C`.

## Silence zones (Forgotten City), the most important section

- **Followers and the city.** The author says to play solo. I searched all 461 of its compiled scripts and found **no follower handling at all** (no follower/teammate code). The time jumps move the player by script.
  - **Unsure:** followers may jump in after the leap of faith, but they will **not** reliably come with the player through the Lakehouse into the past.
  - **Recommendation:** treat the whole location `000800:Liv_ForgottenCity_AddLocations.esp` as a **no-ambient-banter zone** from `012BB9` stage 100 (leap of faith) until stage 4050, or until `05965B` stage 6000 / `012BB9` 3000.
  - Allow at most one "waiting at the Forgotten Ruins" line and one "you're back, what happened down there?" debrief.
- **Leap of faith:** `012BB9` stages 100 to 200.
- **The past:** `05965B` running with stage 400 done and 6000 not done. A follower who "remembers" events here would break the loop logic. They did not live it.
- **Portal/paradox resets:** stages 5000 to 5500. Every loop resets the residents' state.
- **Law broken:** when the statues wake (`0A7AE8` objective 10 shown), mute.
- **Credits:** `0E5786`.
- **The quarry radiation and the Arbiter chamber:** `094809` stages 20 to 30.

## Existing follower lines (Forgotten City)

None. No follower of ours has Forgotten City lines. (Remi has "I wish I could time travel" in a dragon idle, a perfect setup line.)

## 12 banter hooks (Forgotten City). Use them at the entrance and in the debrief, not inside the loop.

1. **Remi at the Forgotten Ruins entrance.** A hidden Dwemer city that nobody has catalogued! She has to be talked out of jumping first.
2. **Remi's "I wish I could time travel" line comes true** for the player, not for her. Debrief: she is jealous and furious she was left behind. "You saw a working Arbiter and I was up here eating a sweetroll?"
3. **Lucien and Remi argue the Dwarves' Law.** Was it ethics or machinery? Lucien (Neramo's student) versus Remi ("they built a judge, of course they did").
4. **"The many shall suffer for the sins of the one."** Gore (raised by a mercenary band, "blood is a covenant") versus Xelzaz (Telvanni lawman, who likes rules). A real argument about collective punishment.
5. **Kaidan and Inigo on time loops.** "If you could go back and stop Helgen / Fergus's death / the Thalmor raid?" An emotional pair.
6. **Val the pirate in a city where theft ends the world.** "I'd last about four minutes."
7. **The statue of the player.** The debrief reveal: "There's a statue of you down there? Older than you?" Lucien is fascinated by the paradox, Redcap thinks the player is a god.
8. **Metellus's utopia.** Lucien (Imperial idealism) versus Xelzaz (hierarchy) versus Gore (anti-authority) on whether order can be imposed.
9. **Skooma subplot** (Dwemora and Asanshi). Kaidan's addiction history; Inigo's sobriety.
10. **Rykas's secret and the threatening notes.** Inigo, warm and non-judging, and Lucien on hidden love. Gentle.
11. **Altrius and Cassia reunited.** Siblings: Inigo (Fergus), Remi (her sister), Lucien (only child) all react differently.
12. **Immaculate Dwarven armour.** Remi and Lucien beg to examine it. Lucien's existing vamidium-and-crown mania (Forgotten Seasons patch) shows he gets obsessive. Use that energy.

---

# 6. Skyrim Extended Cut: Saints and Seducers (+ SaintsAndSeducersSECOverhaul.esp)

Plugins: Creation Club `ccbgssse025-advdsgs.esm` (its original quests "Balance of Power" `000912` and "Restoring Order" `000913` are **emptied by SEC**: zero stages, zero objectives in the winning version), `Skyrim Extended Cut - Saints and Seducers.esp` (the real quests), and `SaintsAndSeducersSECOverhaul.esp` (no quests of its own; a balance/record overhaul). Other: `Lucien-SaintsAndSeducers-Patch.esp`, `Gore - SaSEC.esp`, `AX ValSerano-SSEC.esp`, DBVO fixes, Requiem patches.

## Plain summary

**Premise.** A fully voiced Daedric quest that continues **after "The Mind of Madness"**. A prisoner revolt in the **Asylum**, a prison region on the fringe of Sheogorath's **Shivering Isles**, is leaking into Nirn through "the Root". You go to the Isles: sunny Mania and grim Dementia, a homage to the Oblivion expansion.

**Start.** Level 20 or above and The Mind of Madness done. Sleep 6 hours or re-enter Solitude. The player gets sick or visionary (Gore's patch: "Blood? Are you sick or something?"). A quake follows: "The Route of Madness" (`099D18`), "Investigate the source of the quake", "Investigate the strange tunnel". You find the cell **"Solitude Wasteworks"** (Root to Nirn, `0EC526`) under Solitude.

**"The Isle of Madness"** (`099D19`). **Staada**, a Golden Saint (Aureal, the order side), takes you to the Asylum to put down the riot. Her counterpart **Dylora**, a Dark Seducer (Mazken), has been captured and tortured by **Thoron**, the prisoners' leader (an Exile) (stage 30). You rescue her. Thoron wants to seize the Root to force his way back into the Isles (51).

**"The Roots of Madness"** (`09EF5F`):
- Get an Isles artifact (Nerveshatter, optional) to break Thoron's amber barrier.
- Optional sabotage between two rival factions: **Priests** (Grove of Insanity, soul tomatoes) and **Apostles** (laboratory, void essence). You can burn either one and frame the other.
- Break into the Root Nexus. Thoron flees into the **Well of Inversion** and makes mirror copies of Staada and Dylora to fight you.
- He calls out to **his master** before being turned to crystal (90). That is a cliffhanger.
- Staada thanks you, and you can come back any time (100).

**Side quests:**
- **The Merchant's Masterpiece** (`099D1A`): the "strangely familiar" merchant **Theodor Gorlash** wants Sheogorath-shaped amber from the Root Canal; reward is amber smithing.
- **The Lunatic's Treasure** (`099D1B`): an Argonian, **Sees-the-Moon**, sends you for a "treasure". He only wanted the cast iron pot it was under; reward is madness-ore smithing.
- Elytra pets (Mania and Dementia nymphs).

**Places:** Borogove and Borogove Outgrabe (towns), Xedex, Stopgap, Root Canal, Glimmering Hollow, Root Nexus, Grove of Reflection, The Near Corgi Shop, Decrepit House, Sees-the-Moon's Shack. Root caves have keyword `0A516C` EC_SS_LocTypeRootCave.

**Tone.** Absurd, colourful and dark-funny, true to Sheogorath (cheese, butterflies, tomatoes made of souls).

## Named quests (SEC)

| EditorID | FormID | Name | Started | Key | Completed |
|---|---|---|---|---|---|
| EC_SS_MQ100Int | 099D18:Skyrim Extended Cut - Saints and Seducers.esp | The Route of Madness | objective 10 quake | objective 20 strange tunnel | 100 |
| EC_SS_MQ101 | 099D19:... | The Isle of Madness | 0/1 Staada's request | 10 Asylum, Dylora captured; 30 Dylora tortured; 40 rescued; 51 Thoron's plan | 52 (CompleteQuest) |
| EC_SS_MQ102 | 09EF5F:... | The Roots of Madness | 52 | 64 weapon found; 70 barrier broken; 80 Well of Inversion copies; 90 Thoron crystallised, calls his master | 100 |
| EC_SS_TheodorQuest | 099D1A:... | The Merchant's Masterpiece | 10 | 20/40 | 255 |
| EC_SS_LizardQuest | 099D1B:... | The Lunatic's Treasure | 10 | 20/40 | 255; 300/301 fail (Sees-the-Moon killed) |
| EC_SS_AsylumEpilogueQuest | 5BDB5C:... | (epilogue) | | | |
| EC_SS_ElytraPetAcquisition_Mania / _Dementia | 0010C3 / 0010C0:ccBGSSSE025-AdvDSGS.esm | My Pet Elytra | | objective 10 free the nymph | 25 |

## Silence zones (SEC)

- **Intro sickness / vision:** before `099D18` completes (Gore's patch has the "What's gotten into you?" beat). Let Gore have it and mute the rest.
- **Torture and rescue scene:** `099D19` stages 30 to 40.
- **Well of Inversion:** `09EF5F` stages 80 to 90 (mirror fight).
- **Ending talk with Staada:** stages 90 to 100.
- **Followers are allowed in the Isles.** SEC itself ships idle lines for Lucien (`5BDAA6` EC_SS_LucienDialogueQuest, in-cell lines such as "I didn't mean into a sewer filled with creepy crawlies") and for the follower Shirley.

## Existing follower lines (SEC)

- **Gore.** `Gore - SaSEC.esp`, 34 lines:
  - "Are we still under Solitude?", "Never knew all of this was just below Solitude"
  - Sheogorath alarm ("He's the Daedric Prince of Madness, blood... turning around and leaving now")
  - the "Root Canal" pun ("It's funny!")
  - "I like the purple lady more" (Dylora)
  - stench and squeaky boots
  - "Daedra and tomatoes?"
  - the player's sickness intro
- **Val.** `AX ValSerano-SSEC.esp`, 43 lines (ValAddon01):
  - "We're not in Solitude anymore, Meeko", no cheese
  - "Staada... Gaslight, gatekeep, girlboss personified"
  - Dylora and Staada hate each other
  - "More like Drinks-the-Skooma" (Sees-the-Moon), Theodor's "familiar" bad fashion
  - soul tomato
  - Joker/Batman-style combat taunts ("Why so serious?", "I am the night!")
  - intrusive-thoughts apology
- **Lucien.**
  - SEC's own `EC_SS_LucienDialogueQuest` (in-cell idles).
  - `Lucien-SaintsAndSeducers-Patch.esp`, 98 lines written for the **original CC questline**: Ri'saad's caravan, Kinthal, Svarig, Thoron in the Solitude sewers, the Half Moon Mill smith, Crystaldrift Cave, the Sword of Jyggalag.
  - **Many of these are probably dead under SEC**, because SEC emptied the CC quests they key off. Unsure; check conditions.
  - His item and armour comments and his Staada lines ("I really don't think Staada likes me") still fit.
- **Xelzaz.** Sheogorath / Mind of Madness (DA15) lines ("chef of honor" banquet story, the fork memento).
- **Inigo.** "You met Sheogorath and he did not turn you into a block of cheese."
- **Kaidan.** A Hircine-versus-Sheogorath tale.

## 12 banter hooks (SEC)

1. **Xelzaz's Sheogorath kitchen trauma.** He already cooked for the Mad God once. Back in his realm, he is visibly twitchy. Remi wants the whole story.
2. **Soul tomatoes.** Remi (soul gems power her machines) and Lucien ("a tomato that's also somehow a soul gem... I love it") have a giddy science moment. Gore: "Daedra and tomatoes?"
3. **Golden Saint versus Dark Seducer.** Gore likes "the purple lady", Val makes the girlboss joke, Lucien feels Staada glaring at him. The party picks sides.
4. **Priests versus Apostles sabotage.** Val loves a good frame-up. Xelzaz (a lawman) objects. Kaidan, an ex-assassin, is quietly good at it.
5. **Redcap in the Shivering Isles.** A Riekling who already thinks the world is mad finds a place madder than him and loves it. Bliss bugs.
6. **Inigo's cheese line callback.** "You promised me no cheese transformations."
7. **Theodor Gorlash, "strangely familiar".** Lucien and Val, Imperial City kids, half-recognise the Oblivion-era legend, and Val's fashion jab lands.
8. **Thoron's "master" cliffhanger.** Lucien explains Jyggalag (from his patch: "Prince of Order... also Sheogorath... it's complicated"). Xelzaz and Lucien speculate.
9. **Thoron tortures Dylora.** Kaidan's own Thalmor torture. Quiet anger, and he doesn't want to talk about it, then does.
10. **The Root under Solitude.** Val (Solitude navy past) and Gore ("never knew all of this was just below Solitude") on what's under their city.
11. **Mania versus Dementia mood.** Inigo, a natural optimist, loves Mania. Lucien prefers the bookish gloom of Dementia ("curl up with a book"). Remi wants both for the ingredients.
12. **Sees-the-Moon's "treasure" was a pot.** Inigo understands perfectly. Remi is outraged. Val: "Drinks-the-Skooma."

---

# 7. The Cursed Tribe: Quest Expansion (TCTQE)

Plugin: `The Cursed Tribe - Quest Expansion.esp` (light plugin). It edits the vanilla quest **DA06 "The Cursed Tribe"** (`03B681:Skyrim.esm`) and wins the record. It adds a new shrine location route near Avanchnzel, the ghost NPCs (Shagrol `000075`/`000076`, Haunting Ghost), named Orcs (Yahakh, Gruslong, Ghoguk), and renames the giant to **Gorak Longstride** (`0C0BE5:Skyrim.esm`) and "Giant's Grove" to **Sanctum of Malacath** (`0C33AF:Skyrim.esm`).

## Plain summary

**Premise.** The Orc stronghold **Largashbur** (southwest of Riften) is besieged by giants. Restored cut content explains why. Chief **Yamarz** killed the previous chief **Shagrol** in a probably-rigged duel. Shagrol, through Malacath, cursed him: **ghosts haunt Yamarz**, he can't sleep, the tribe weakens, and the giants smell weakness.

**Start (changed by TCTQE).** Level 10 or above. You must be an Orc or **Blood-Kin** of the Orcs, and ask any *other* stronghold's chief for rumours. You get a letter (objective 5).

**Normal route:**
- Kill the giant at the gate.
- The wise woman **Atub** sends you to Yamarz (20). He explains the ghosts (30).
- Atub points to a **Malacath shrine** northwest of the stronghold (40). There you find an Orc skeleton (a Shagrol loyalist) with a note: Yamarz should "listen with the ears of the wind" (45).
- Bring troll fat and a Daedra heart (50). **Ritual: the whole tribe gathers and prays while Malacath speaks** (60/70). He is angry his shrine was desecrated and orders Yamarz to retake it himself.
- Yamarz instead pays you to escort him to Fallowstone Cave and kill the giant (80/100). He dies there or proves useless.
- Malacath makes **Gularzob** chief and **you** his champion. You carry Shagrol's Hammer back and receive **Volendrung** (110 to 200).

**Alternate route (new).** If you know **Bane of the Undead** (or have the scroll), cast it inside Largashbur (35/65). Ten ghosts appear, including Shagrol, and you fight them with the tribe. Yamarz lives. Atub gives a dual-enchanted amulet instead of Volendrung (66/67, 210). This angers Malacath (lower favour if Wintersun is installed).

**Tone.** Harsh Orc honour, Daedric contempt for weakness; the alternate ending is mercy.

## Named quest

| EditorID | FormID | Name | Started | Key | Completed |
|---|---|---|---|---|---|
| DA06 | 03B681:Skyrim.esm (winner: TCTQE) | The Cursed Tribe | 10 rumour (objective 5 letter); 20 Atub | 30 ghosts explained; 35 resto route; 45 shrine note; 50 ingredients; 60/70 ritual, Malacath speaks; 80 escort; 100 kill Gorak; 110 Shagrol's Hammer | **200** Malacath names Gularzob chief, you his champion (Volendrung); **210** ghosts banished (amulet); 255 fail |

## Silence zones (Cursed Tribe)

- **Ritual:** stage 60 until 70. The whole tribe prays and Malacath speaks, so mute everything.
- **Malacath at Fallowstone:** stage 100 until 110 (his voice).
- **Ghost battle:** stage 65 until 66 (combat barks only).

## Existing follower lines (Cursed Tribe)

- **Xelzaz:** `BPUFXelzazDA06Idle` and others ("the most pathetic display by an Orc chieftain", "we did the tribe a favor by ridding them of Yamarz", Malacath's curse keeps them subservient, "Why must we be present for the ritual?").
- **Kaidan:** "No wonder Malacath is pissed off, this Orc is fucking useless" (BWB Extra), and an IF line ("killing the giant for him as well? ... Malacath knows").
- **Val:** ValS04Malacath01/02A ("They're not cursed. Bad things happen to everyone, especially when you follow Malacath"; "Just like the Orc chief").
- **Gore:** raised by mostly-Orc "Fathers" in the Band of the Raven; taunt "Malacath welcomes you, dog"; Trinimac/Malacath lore line. Nothing quest-specific.
- **Remi, Inigo, Lucien, Redcap:** none quest-specific found.
- Note: these existing lines were written for the vanilla ending (Yamarz dies). They may misfire on TCTQE's ghost-banishing route (stage 210, Yamarz alive).

## 12 banter hooks (Cursed Tribe)

1. **Gore among Orcs.** His "Fathers" were mostly Orcs. He speaks the tribe's language of honour and is ashamed of Yamarz on their behalf.
2. **Rigged duel.** Gore (honour) versus Val ("everybody cheats, the trick is not getting caught").
3. **Ghost-banishing route** (stage 210). Lucien and Remi cheer the clever magical solution. Gore worries Malacath will hold a grudge. Xelzaz's existing "favour" line is wrong here, so fix it with a new beat.
4. **"Listen with the ears of the wind."** Lucien loves the riddle. Redcap thinks the wind talks to him too.
5. **Troll fat and a Daedra heart.** Remi and Xelzaz alchemy shopping banter.
6. **The tribe prays together** (after 70). Inigo, raised in a devout village that wanted to sacrifice him, gets uneasy around communal devotion.
7. **Giants.** Redcap's tribe feared big things, and he hides behind Gore. Inigo, the spider-killer since Riverhold, rates giants against giant spiders.
8. **Volendrung.** Who gets to carry the hammer: Gore begs, Redcap can't lift it.
9. **Yamarz's sleepless nights.** Kaidan, who has nightmares from Thalmor torture, has unexpected sympathy for the cowardly chief.
10. **Malacath as the god of outcasts.** Gore's Trinimac lore versus Xelzaz's Dunmer view of Boethiah eating Trinimac. A theology argument by the fire.
11. **Atub the wise woman.** Remi (Breton, amateur alchemist) bonds with her; Lucien wants to record Orc ritual practice.
12. **The new chief Gularzob.** Val and Kaidan on succession by murder; Gore says "that's just how it's done".

---

## Notes and unsure items

- Forgotten City follower behaviour is not proven. There is no follower code. Plan for followers to be absent from the leap of faith until the final quest stages, and check in-game.
- Sirenroot: after the stage-20 collapse the player is moved alone. Xelzaz's patch handles the reunion. For others, check whether they reappear.
- Moonpath carriages work like doors. Followers should come along, but check.
- Lucien's CC Saints and Seducers patch lines are probably dead under SEC (their source quests are emptied). Check his patch's conditions before relying on them.
- The Bruma border failsafe quest `0D6E80` moves followers across the border, so followers are expected in Cyrodiil.
- `ForgottenCityLocation` lives in a light plugin (`Liv_ForgottenCity_AddLocations.esp`, runtime index FE). Always reference it plugin-qualified.
