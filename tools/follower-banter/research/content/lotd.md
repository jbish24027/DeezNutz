# Legacy of the Dragonborn (LOTD) - banter research

Source: LegacyoftheDragonborn.esm (LOTD V6, mod "Legacy of the Dragonborn V6"), read from the live load order of profile DEEZ CS NUTZ - PICTA on 2026-10-18. Every quest name, stage number and journal line below comes from the plugin itself. FormIDs are written `XXXXXX` = `XXXXXX:LegacyoftheDragonborn.esm` (it loads at runtime slot 14, so the in-game console form is `14XXXXXX`).

Spoilers throughout.

---

## 1. The story, plainly

### The premise
An Altmer scholar, **Auryen Morellus**, has built a museum in Solitude called the **Dragonborn Gallery**. It sits right next to the Blue Palace, on the spot where a Temple of Talos was being built before the Thalmor ban. He wants rare relics and artifacts for display, and he hires the player as his relic hunter. Everything the player finds can go on a display case, and the museum slowly fills up. The museum, not a villain, is the "main quest". It's a collector's power fantasy with a cast of scholars around it.

How the player gets in:
- **An Interesting Prospect** (`17211B`): the player finds an advert for relic hunters, or gets a letter from the curator after selling him an artifact. Auryen sets a test: bring three relics (a Sixth House hammer from Broken Helm Hollow, Denstagmer's Ring from Silent Moon's Camp, a jade statue somewhere in the Reach). Deliver them and you're in.
- **Dragonborn Gallery** (`3F14FC`) is the alternate-start version. The player arrives by ship to help Auryen, gets the tour, then follows his notes: urns held by Borgoth in Helgen (destroyed when Helgen is attacked), Bleak Falls Barrow (the Dragonstone), and Silent Moon's Camp.

### Auryen Morellus and the staff
- **Auryen Morellus** (Altmer, `12537E`): curator. Polite, scholarly, generous, a bit grand, and old enough to know everyone. He runs tours, hosts galas, writes theories, funds everything, and judges character well (by his own account). He studied at Gwylin University with Marassi and Darnette. He keeps a portrait of Hermaeus Mora in his office (Val notices it). He leaves research journals all over the library ("Auryen's Notes" quests). He takes a "nobody asks, nobody tells" line on the player's shady items.
- **Avram Shazir** (Redguard, `0AEEAD`): the museum's security captain. He was a dock warehouse guard in Dawnstar who answered Auryen's notice. He has a criminal past in Hammerfell that comes back in the heist quest: his brother Jelal robs the museum. He is forgiven or demoted, and gives the player his father Hagram's sword.
- **Millie Lauven** (Breton, `0F0C93`): housekeeper, cook and supply orderer. Darnette's older sister. She once served near the Pelagius wing of the Blue Palace, and the Amulet of Pelagius affects her in *Echoes of Madness*.
- **Hagar** and the guards (Sieglinde, Siegmund, Ger'Trune, Gunther the Orc, Eringoth, Yolanda, Egriss): Avram's hired security. Some of them patrol Deepholme.
- **Patrons** (the museum's regular visitors, who have little scenes with each other):
  - Lorna and her son Henry: a widow and a fatherless boy who climbs the shelves.
  - Cedric Aldrus and his daughter Verna: they sold their home so Verna could study art.
  - Marcus Flynn: all bravado.
  - Tulvan Ironbear.
  - Lolette Astrada: quiet, researching maps, listing places to travel.
  - Radcliff the Troubadour: a fly-on-the-wall bard.
  - Gordrak gro-Shor: an Orc blacksmith from High Rock studying the weapons.
  - Asterion and Asterell: entitled Altmer twins, children of the diplomat Anderon.
  - Jerrin and Malakai: tour patrons.

### The Explorers Society
Once the museum is going, Auryen and the player found a guild of explorers and archaeologists. The player becomes its Guildmaster.
- **A Room with a View** (`3431C3`): the player builds the Guildhouse, an extension behind the reception hall that cuts through the city wall and has a grand view.
- **Digging Up Explorers** (`34D50B`): the player recruits five members.
  - **Professor Patero Marassi** (Bosmer): the chief of archaeology. Enthusiastic, a "trouble-maker" in his university days, a terrible dresser. He loves digging and dies in a cave-in.
  - **Madras** (Dunmer): obsessed with the Dwemer and decodes their schematics. He has a little automaton called Eggelman and builds the Planetarium.
  - **Kyre Oldenson** (Nord): a former miner and a fast learner. He sets off every trap in Karagas' Maze. He becomes chief of archaeology after Marassi dies.
  - **Latoria** (Khajiit): a mage once at the College. She frightens easily, deciphers ruined books, and has her tail pulled.
  - **Eriana** (Imperial): the quartermaster and fence, with a hinted thieving past. She will take the cursed Hand of Glory off the player.
  - **Darnette Lauven** (Breton) also lives at the Guildhouse: a fossil scholar, rough around the edges and good at cards.
- **Fafnir** is a raccoon picked up in Windcaller Pass and now the guild mascot.
- **Field stations**: *Branching Out*, *...Again* and *...Ever More* build Northern (Winterhold), Western (Reach) and Eastern (Eastmarch) field stations. They cost lumber, stone, clay and 2,000 gold of jarl's tax each.

### The big questlines
1. **The Excavation of Windcaller Pass** (`4D1811`): the guild's first dig, north of the Throat of the World.
   - The player clears creatures and then two dragons.
   - They find a Nordic claw key and a lockbox with the Windcaller ring and amulet.
   - Latoria is robbed by a "terrible creature", which turns out to be a raccoon with its paw stuck. It then saves the player from a gas trap by hitting a switch.
   - The raccoon is named Fafnir.
2. **The Excavation of the Ruins of Rkund** (`58B96A`): a Dwemer dig.
   - Three survey attempts dig in the wrong spots. The entrance was "right behind us the whole time".
   - Inside are cog keys, Karagas' Maze (Kyre comes along), Karagas' Tower and a transmutation forge.
   - A teleport device brings the explorers through. Karagas' "treasure" was his daughter's tomb.
   - It leads into **A Path to the Heavens** (`5867FC`): building the Planetarium with Madras. It projects Nirn and its moons from Dwemer cubes.
3. **Much Ado About Snow Elves** (`5C7E75`): Calcelmo writes asking for help researching Falmer relics.
   - It's a comic wild-goose chase. Freir at the Temple of the Divines tries to extort the player (her "Pookie Bear" teddy hides skooma). Urag hands out useless books, and a Synod mage lost a book at Mzulft.
   - The player then finds three ancient Snow Elf staves in the Temple of Xrib, Alftand and Irkngthand refugee annexes.
   - A **Snow Elf ghost** guides the player, then turns into a shade and traps them in a freezing chamber.
   - Ending: "The Falmer betrayed, their souls screaming for vengeance... A Snow Elf ghost, now vanished."
4. **The Visage** (`2702DC`) and **Trial of Trinimac** (`2702EE`): the third excavation and the emotional core.
   - Chimes in the player's head and the returning Snow Elf ghost lead to Lost Ruins under Fort Greenwall.
   - The team builds scaffolding, finds a giant chalice that fits a Phynaster shrine, and recovers a Falmer tome.
   - **A cave-in kills Marassi** (stage 70), and the player barely escapes; Val's "Coma" lines refer to the player being knocked out.
   - Auryen mourns. The player picks Kyre as the new chief of archaeology.
   - The translated tome speaks of **Tulrin Deathweaver**, a Falmer rebel lord tied to Mauloch/Trinimac.
   - The team digs out a Temple of Trinimac in the southwest. The Spear of the Snow Prince (*Legacy of the Snow Prince*, `289BEA`, from Jolgeirr Barrow) opens the door.
   - Tulrin escapes. The trail runs through Darkfall Passage to the **Temple of the Venerable Ones** in a glacial crevice.
   - The puzzle uses magical chimes, Phynaster's Ring (`2A36E4`, held by the Thalmor) and the Warlock's Ring (`2A87EE`, Syrabane's). A split Harmonic Touchstone has to be rejoined. A Y'ffre shrine gives the code "seven, five, six, one, three, two".
   - Finale: kill Tulrin and claim the blade **Neb-Crescen**.
5. **Shattered Legacy** (`121573`): the Amulet of Kings questline.
   - A dying man, Byron, flees the Morag Tong and hands the player a shard of the **Chim-el Adabal**.
   - "Guardians" of the shards meet at High Hrothgar: Argus Fenneric, paranoid Ezra and Ulgarg the Orc. Ulgarg swallowed his shard before he died.
   - At Fort Pale Pass, in the middle of a battle, the player finds the shield of Reman Cyrodiil.
   - Argus and Ezra turn out to be mercenaries and double-cross the player.
   - Auryen's Ayleid Waystone sends the player to **Sancre Tor**, where a dark force binds them. They must defeat **Zurin Arctus, the Underking**, and meet the **Herald of Akatosh**, a dragon.
   - The player gathers three Shor/Lorkhan relics: the Lord's Mail, Zurin Arctus' ring, and Ysmir Wulfharth's boots (from Dragon's Fall above Windhelm).
   - The player fights off a Shadow Hunter agent, and the Amulet of Kings is re-formed in the Sanctum of Akatosh.
6. **Night at the Museum** (`7AC75C`): the museum is closed because of a haunting.
   - Brother Ikard, a priest of Arkay, investigates with the player overnight. Furniture ends up on the ceiling and mannequins walk.
   - Clues point to the ghost of the building's former owner, **Lord Niles Macnarian**, heartbroken over his wife Orellia.
   - The player has a **nightmare**: the museum is on fire, Ikard is dead and the player "awakens" into a dream.
   - Fix: hang Macnarian's portrait, then find and pay for the lost statue of his wife (sculptor Morgaine Olfstead).
   - Players who refuse can leave it to Ikard. Ghosts walk the halls at night afterwards.
7. **Shadows of One's Past** (`33D940`): the museum is robbed and the displays are empty.
   - The player chases the thieves to Windcaller Pass, stops a caravan heading for Hammerfell, then goes to Engelmann's Rest.
   - The leader **Jelal** is Avram's brother. Avram is forced to kill him, stays behind to bury him, and later gives the player their father's sword.
8. **The Price of Vigilants** (`0F0D34`) and **Faltering Light** (`0E1595`): five Vigilants of Stendarr come to destroy the Daedric relics. They are Astrian, Tylende, Burondis, Morgi and Cindra.
   - The player can hand over replicas or the real relics.
   - They can bribe or persuade each Vigilant: Mythic Dawn Commentaries for Astrian, a weapon for Tylende, a house and the chance to smash a Molag Bal altar for Cindra. Morgi can stay on as the relics' watchman.
   - They can fight them openly.
   - Or they can arrange "accidents": Astrian reads a Daedric book, Tylende is caught in Dwemer machinery, Burondis is pushed off the balcony, Morgi is locked in a portal, Cindra is poisoned through a cup.
   - Survivors may come back later as ambushers (Faltering Light, Stendarr's Refuge).
9. **Echoes of Madness** (`4E0D3F`): Millie acts strangely. The Amulet of Pelagius is to blame.
   - The player goes back into Pelagius' mind, with Sheogorath scenes, and kills the Demon of Camlorn for the Eye of Camlorn gem.
   - Restoring the amulet ends the curse on the Septim line.
10. **The Vaults of Deepholme** (`9211FD`): an Atmoran prison on an island in the Sea of Ghosts. It held Elven prisoners and relics when Ysgramor rose.
    - The player kills a sealed Elven lich.
    - Auryen proposes turning it into a secret vault: real relics go there and replicas stay on display. It costs 10,000 gold, which Val calls "a bottomless pit for gold".
11. **Guardians of the Divine** (`9211C7`): a dead Knight of the Nine's notes lead to the eight relics of Pelinal Whitestrake, the Divine Crusader, plus Sir Amiel's ring. The Thalmor were hunting them.
12. **The Hand of Glory** (`42E8D4`): Greigor, a Dark Brotherhood member, sends the player to make a Hand of Glory.
    - The ingredients are a hanged man's hand from Glacial Cave on Solstheim and the essence of the wrongly executed Roggvir.
    - The player kills Greigor at his request. The Hand is cursed and slowly drains life.
    - **Breaking the curse** (`08F9D7`): give it to Eriana or kill Ahtar.
13. **Smaller artifact quests**:
    - **It Belongs in a Museum** (`371C28`): the Khajiit Rakis delivers the Staff of Indarys and a Thalmor assassin attacks. Rakis then **gives the player the airship Dev Aveza**.
    - **Eternal Ice** (`4F0624`): six shards of Hrormir's Icestaff, reforged at the Coldforge.
    - **Ongar's Kegbreaker** (`33D941`): a drunk at the Nightgate Inn trades Sanguine's "Inebriator" warhammer for a new hammer.
    - **The Book of Wonders** (`79C613`): Malrus' Codex under Silent Moon's Camp.
    - **The Ayleid Crossroads** (`16658E`): the Waystone amulet opens a pocket realm of Oblivion with portals.
    - **Back to the Drawing Board** (`16658A`): rebuild the spider imbuing machine in the Safehouse workshop.
    - **Ancient Power** (`0854C5`): five ancient vampire remains destroyed at Stendarr's Beacon.
    - **Ancient Technology** (`3F33E3`): Madras decodes Dwemer schematics.
    - **Tools of the Trade** (`7BFED0`): the dead explorers' tools, including Schneider's Sextant, Sands' Torch, Deano's Bottomless Pack, Luca's Pickaxe, Merrian's Spyglass and Sanamia's Journals.
    - **Sanamia's Journals** (Mzulft, Valthume, Fort Frostmoth, Lake Ilinalta, a burial ruin): "excavate the hidden chamber" dungeon add-ons.
    - **The Phantom Cache** (`2E566D`): a teleporting chest.
    - **Lord's Mail** (`125B25`): the Penitus Oculatus chase a renegade, Praefect Torbal, to Steepfall Burrow.
    - **Auryen's Notes** (ten quests, `148479` to `14D59B`): his library journals point to relics. The Dagger of Symmachus, Cyrus' Saber (the Brinehammer wreck), Orgnum's Coffer, the Ice Blade of the Monarch (Olaf One-Eye), Shalidor's Stone, the Bloodworm Helm, the Warlock's Ring, the Dragonmail Cuirass, the Fists of Randagulf (bribe, steal or persuade at the Blue Palace) and the Tools of Kagrenac (Sunder, Wraithguard, Keening).
14. **Radiant and repeatable**:
    - *Finders Keepers* (`06B90A`, Auryen's leads)
    - *Research Project* (`740A17`)
    - *One Man's Junk* (`5A94C3`, ruined books for Latoria)
    - *Rebuilding The Past* (`0F0D35`, restoring artifact orders, which can be delegated to an explorer)
    - *Relic Hunt* (sextant) and *The Dig* (surveyor) markers
    - *Beachcombing* (spyglass sea shells, which Val collects)
    - *Museum Gala* (`0F0DC8`, an evening event)
    - Museum tours (six radiant tours plus the *Ten Septim Tour*).

### The building, in rooms
- **Reception and Hall of Heroes**: magical and historical artifacts, Auryen's office, the upper hallway, the gala space, a memorial to Marassi, the Explorers' dome.
- **East Exhibit Halls**: the **Daedric Gallery** (relics held "between planes" by Auryen's barrier enchantments), the **Hall of Oddities** and the **Hall of Lost Empires** (Nord, Dwemer and Falmer, with the dungeon-clearing displays).
- **Gallery Library**: a printing press, a restricted section, and the rare books where the haunting starts.
- **Gallery of Natural Science**: fauna dioramas, a planted flora garden, a gem exhibit, a living tidepool, an aquarium, an upstairs fossil hall and a chaurus display that Val hates.
- **Armory** (East and West wings): mannequins and weapon racks, plus a wine-store/storeroom.
- **Dragonborn Hall**: the Dragonborn's own story and trophies.
- **Hall of Secrets**: a dusty panic room under the floor of the Dragonborn Hall, built for Pelagius under the Blue Palace's Pelagius wing. It's the player's private room for questionable items.
- **Safehouse**: the player home inside the museum. It has a vault, workshop and crafting stations, holding cells, guest and spare rooms for followers, a garden, transport pads, a sale box and the spider machine.
- **Planetarium**: Madras' machine.
- **Storeroom**: where the Macnarian painting hides and where Morgi can be locked in a portal.
- **Hall of Wonders**: Creation Club displays, added by `DBM_CC_HallOfWonders.esp`.
- Off-site:
  - Explorers Society **Guildhouse**
  - **Deepholme** vault
  - Dev Aveza airship cabin
  - Three field stations
  - The Wayward Rest (an LOTD inn interior)

### Memorable moments (banter gold)
- Walking into the empty museum on day one.
- Every display case filling.
- The raccoon thief who saves the player's life.
- The Rkund entrance being right behind the team the whole time.
- The upside-down haunted museum and the fire nightmare.
- Marassi crushed in the cave-in.
- Avram killing his own brother.
- Bribing or "accidenting" the Vigilants.
- Being given an airship.
- Meeting the Herald of Akatosh.
- Wearing the Amulet of Kings.
- Sheogorath again.
- A Dark Brotherhood man who asks to be killed.

---

## 2. Quest reference (stages for conditions)

How to read this:
- "Started" means the earliest stage that sets the journal.
- Many LOTD quests are **Start Game Enabled**. They run from a new game with no journal entry, so `GetQuestRunning` is useless for them. Gate on the stage instead.
- Quests with several endings say **use `GetQuestCompleted`**. That condition function covers every CompleteQuest stage at once.

| EditorID | FormID | Name | Summary | Started | Key moments | Completed |
|---|---|---|---|---|---|---|
| DBM_MuseumIntro | 17211B | An Interesting Prospect | Prove yourself to Auryen with 3 relics (regular start). | 5 (advert) or 10 (letter); 20 = three relics assigned | 35/45/55 = relic delivered | 100 (all delivered); quest ends 110/200, so use GetQuestCompleted |
| DBM_LALStart | 3F14FC | Dragonborn Gallery | Alternate start: arrive, tour, follow Auryen's notes. | 5 | 15 arrived at museum; 20 tour done; 30 Helgen urns destroyed; 31 Bleak Falls tablet; 32 Silent Moons | 35 |
| DBM_MuseumIntroTour | 124FC4 | Ten Septim Tour | Auryen's paid tour (scene quest). | quest running | - | - |
| DBM_ExplorerGuildHouse | 3431C3 | A Room with a View | Build the Guildhouse; found the Society. | 5 | 10 built; 15 tour with Auryen | 30 (or 100) |
| DBM_ExplorerGuildmembers | 34D50B | Digging Up Explorers | Recruit Eriana, Marassi, Kyre, Madras, Latoria. | 5 | - | 10 (or 100) |
| DBM_ExplorerFieldStation01 | 2AD9CD | Branching Out | Northern field station, Winterhold. | 5 | 15 built | 16 |
| DBM_ExplorerFieldStation02 | 2D1170 | Branching Out... Again | Western field station, Reach. | 5 or 6 | 7 paid gold; 15 built | 16 or 17 |
| DBM_ExplorerFieldStation03 | 2D1178 | Branching Out... Ever More | Eastern field station, Eastmarch. | 0 or 5 | 15 built | 16 |
| DBM_Excavation01 | 4D1811 | The Excavation of Windcaller Pass | First dig; dragons; Fafnir. | 5 | 20 met team; 47 two dragons slain; 62 Windcaller relics; 131 relics stolen; 141 raccoon found; 142-144 gas trap/raccoon saves you | 150 |
| DBM_Excavation02 | 58B96A | The Excavation of the Ruins of Rkund | Dwemer dig, maze, tower. | 5 | 11/20/55 surveys; 80/90 broke through; 105 cog door; 110 maze with Kyre; 115 Karagas' Tower; 125 teleporter | 140 |
| DBM_PlanetariumQuest | 5867FC | A Path to the Heavens | Build the Planetarium with Madras. | 0 | 10 materials list; 20 delivered; 30 help build | 50 (or 100) |
| DBM_DwarvenTech | 3F33E3 | Ancient Technology | Madras decodes Dwemer schematics (repeatable). | 5 | 7 first decoded | 20 |
| DBM_MuchAdoAboutSnowElves | 5C7E75 | Much Ado About Snow Elves | Calcelmo's Falmer staves hunt. | 5 | 101 bribed Freir; 102 Pookie Bear skooma; 200-207 Urag book loop; 310 ghost leads to blue key; 398 ghost turns into a shade and traps you; 399 vision | 450 (410 = all 3 staves returned; 500 = staves donated to the museum) |
| DBM_Excavation03Prelude | 2702DC | The Visage | Chimes and the Snow Elf ghost lead to Fort Greenwall ruins. | 1 | 5 follow ghost; 10 ruin found | 15 |
| DBM_Excavation03A | 2702EE | Trial of Trinimac | Greenwall dig, Marassi's death, Tulrin, Neb-Crescen. | 5 | 50 cup on dais; 55 Falmer tome; **70 Marassi killed in cave-in**; 75 mourning; 80 Kyre appointed; 95 tome translated; 135 temple cave found; 155 Spear opens door; 175 Tulrin flees; 180 glacial temple found; 230 Temple of the Venerable Ones opened; 275 Touchstone rebuilt; 300 final chime code | 350 |
| DBM_SpearofthSnowPrinceQuest | 289BEA | Legacy of the Snow Prince | Fetch the Spear (Jolgeirr Barrow). | 5 (or 20 if already owned) | - | 10 or 30 |
| DBM_PhynasterRingQST | 2A36E4 | Relic of Phynaster | Get Phynaster's ring from the Thalmor. | 5 | - | 10 |
| DBM_SyrabaneRingQST | 2A87EE | Relic of Syrabane | Get the Warlock's Ring. | 5 | - | 10 |
| DBM_ShatteredLegacy | 121573 | Shattered Legacy | Amulet of Kings rebuilt. | 10 (Byron's shard) | 30 shard authentic; 35 Argus at High Hrothgar; 50 Reman's shield at Pale Pass; 70-75 Ulgarg's body; 90 Argus/Ezra betrayal; 220 Waystone to Sancre Tor; 225 bound at Sancre Tor; 234 Underking defeated; **245 Herald of Akatosh**; 255-265 Wulfharth tomb; 280 Shadow Hunter agent fought | 300 |
| DBM_LordsMailQuest | 125B25 | Lord's Mail | Penitus Oculatus vs Praefect Torbal, Steepfall Burrow. | 10 | 30 Torbal dead; 40 bloody note | 100 |
| DBM_hauntedMuseumQuest | 7AC75C | Night at the Museum | Haunting by Lord Macnarian. | 6 or 10 | 15 night investigation begins; 35 haunting intensifies; 45 ghost identified; 60 portrait hung; **65-75 nightmare (museum on fire, Ikard dead)**; 80 woke up; 95 statue lead (Morgaine) | 110 |
| DBM_HauntedMuseumQuest2 | 0F0D33 | Recurring Nightmare | Stub sequel (one stage, one scene). | 5 | - | - |
| DBM_MuseumHeist | 33D940 | Shadows of One's Past | Museum robbed; Avram's brother Jelal. | 10 (or 11 = Avram sent alone) | 25 caravan chase; 30-32 caravan stopped; **35 Jelal is Avram's brother, killed**; 45 Avram buries him; 50 relics returned | 60 |
| DBM_VigilantsQuest1 | 0F0D34 | The Price of Vigilants | Vigilants demand the Daedric relics. | 2 | 40 talked down; 120 handed originals; 150-159 private talks; 180-192 "accidents"; 250-253 fight | many endings (116, 210, 254, 255, 500, 600, 900, 1000), so use GetQuestCompleted |
| DBM_VigilantsQuest2 | 0E1595 | Faltering Light | Surviving Vigilant cell strikes back. | 30 or 70 | 40 hideout note; 75 lackeys beaten | 50 or 100 |
| DBM_EchosOfMadness | 4E0D3F | Echos of Madness | Millie, Pelagius' amulet, Demon of Camlorn. | 10 | 25 amulet locator; 30-40 inside Pelagius' mind; 45 Demon slain | 100 |
| DBM_DHQuest | 9211FD | The Vaults of Deepholme | Atmoran prison becomes a secret vault. | 5 | 10 inside; 25 vault opened; 30 lich slain; 35 agreed to pay; 40 paid 10,000 | 50 |
| DBM_KOTNQuest | 9211C7 | Guardians of the Divine | Relics of the Divine Crusader. | 5 | 6 Sir Amiel's ring; 7 first relic; 10 lore book read | 50 |
| DBM_HOSDiscoveryQST | 0A9247 | Auryen Morellus and the Chamber of Secrets | Find the Hall of Secrets. | 5 | 10 Auryen agrees | 15 |
| DBM_HandofGloryQuest | 42E8D4 | The Hand of Glory | Greigor's cursed relic. | 5 | 10 both parts found; 20 Hand created; 25 Greigor asks to die | 30 (50 = failed, Greigor killed early) |
| DBM_HOGCleanseQuest | 08F9D7 | Breaking the curse | Pass the Hand to Eriana or kill Ahtar. | 5 | 20 Eriana interested | 40 (Eriana takes it) or 50 (Ahtar killed) |
| DBM_MuseumIndarysQuest | 371C28 | It Belongs in a Museum | Rakis, Staff of Indarys, Thalmor assassin; reward: Dev Aveza airship. | 50 | 56 assassin fight | 100 |
| DBM_HrormirStaffQuest | 4F0624 | Eternal Ice | Six icy shards, Coldforge. | 5 | 20 all six found | 40 |
| DBM_OngarKegbreaker | 33D941 | Ongar's Kegbreaker | Sanguine's Inebriator. | 20 | 30 traded; 100/150 Ongar dead or hammer stolen | 35 |
| DBM_MalrusCodexQST | 79C613 | The Book of Wonders | Malrus' Codex. | 5 | 10 three keys lit | 100 |
| DBM_WaystoneQuest | 16658E | The Ayleid Crossroads | Waystone, pocket realm portals. | 5 | 10 attuned | 20 |
| DBM_ImbuningMachine | 16658A | Back to the Drawing Board | Spider imbuing machine in the Safehouse. | 10 | 15 built | 20 |
| DBM_VampireParts | 0854C5 | Ancient Power | Five ancient vampire remains. | 5 | 10 Fort Dawnguard notes; 20 all found | 200 |
| DBM_ExplorerRelicFindQST | 7BFED0 | Tools of the Trade | Kamahl's map of explorer relics. | 5 | - | 10 |
| DBM_GhostChestQST | 2E566D | The Phantom Cache | Teleporting chest. | 10 | - | 20 |
| DBM_JournalDungeon01QST to 05QST | 1D5C18, 2703F9, 275562, 27FDB5, 27FDD3 | Sanamia's Journals (Mzulft, Valthume, Fort Frostmoth, Lake Ilinalta, Burial Ruin) | Excavate a sealed chamber. | 5 | - | 10 |
| DBM_AMJournalQST01 to 10 | 148479, 14846F, 14D594-14D59B | Auryen's Notes: (relic) | Journal leads to a famous artifact. | 10 | Kagrenac: 20 Sunder, 30 Wraithguard, 40 Keening | 30 (found after reading) or 50 (already owned); Randagulf 15/20/30 (bribe/steal/persuade); Kagrenac 45/50 |
| DBM_RadiantFindersKeepers | 06B90A | Finders Keepers | Auryen's radiant lead (repeatable). | 10 | 20 relic found | 30 |
| DBM_RadiantResearch | 740A17 | Research Project | Researched lead (repeatable). | 5 | - | 10 (20 = abandoned) |
| DBM_RadiantRuinedBooks | 5A94C3 | One Man's Junk | Ruined books for Latoria. | 0 | 10 handed in | 30 |
| DBM_ArtifactOrderQuest | 0F0D35 | Rebuilding The Past | Restore artifacts for a buyer. | 5 | 10 delegated | 100 |
| DBM_MuseumGala | 0F0DC8 | Museum Gala | Evening gala in the reception hall. | 5 | 10/20 (gala underway; check this in game) | 100 |
| DBM_SextantHandler / DBM_SurveyorHandler | 18DDE8 / 1C6621 | Relic Hunt / The Dig | Sextant / survey markers (repeatable). | 5 | - | 6 |

Helper and handler quests to ignore for writing (never journal): DBM_SKSEHandler, DBM_SafehouseSupportAPI, DBM_DialogueQuest, DBM_MatchMakerQuest, DBM_Explorer/MuseumScene## (about 130 ambient NPC-pair scene quests), DBM_SellChestHandler, and similar.

---

## 3. When banter must stay silent

Rule of thumb: be silent whenever an LOTD scene is talking, the player is in a dream or vision space, or the quest is in a death or grief beat.

| Beat | Simple condition | Notes |
|---|---|---|
| Arrival tour (alt start) | DBM_LALStart `GetStageDone 15 = 1` AND `GetStageDone 20 = 0` | Auryen walking the player round |
| Paid tour | `GetQuestRunning DBM_MuseumIntroTour (124FC4)` | scene DBM_MuseumIntroTourScene |
| Radiant museum tours | any of `GetQuestRunning` 08F978 (Daedric Gallery), 08F979 (Library), 08F97A (Hall of Lost Empires), 08F97B (Hall of Oddities), 08F97C (Hall of Heroes), 08F97D (Natural Science) | Auryen and patrons talk |
| Museum Gala | DBM_MuseumGala `GetStageDone 10 = 1` AND `GetStageDone 100 = 0` | scene DBM_MuseumGalaScene; check in game that stage 10 is the start |
| Guildhouse tour | DBM_ExplorerGuildHouse stage 15 done AND 30 not done | DBM_ExplorerGuildHouseTourScene |
| Haunted night (whole) | DBM_hauntedMuseumQuest stage 15 done AND 105 not done; or player in cell 1ABB45 / 17CBFE / 0F1B91 (haunted variants) | low-frequency, spooky-only lines at most |
| Fire nightmare (dream) | DBM_hauntedMuseumQuest stage 65 done AND 80 not done | **hard silent**: player is alone in a dream |
| Heist confrontation | DBM_MuseumHeist stage 33 done AND 45 not done | Avram vs his brother; Windcaller and Engelmann scenes |
| Vigilants at the museum | DBM_VigilantsQuest1 stage 2 done AND `GetQuestCompleted` = 0 AND player in museum | 7 scenes (intro, hammer, deaths, portal) |
| Indarys assassin | DBM_MuseumIndarysQuest stage 55 done AND 100 not done | assassin scene on the Guildhouse patio |
| Windcaller gas trap and raccoon | DBM_Excavation01 stage 142 done AND 145 not done | scripted rescue |
| Windcaller end scene | DBM_Excavation01 stage 145 done AND 150 not done | |
| Rkund guided exploration | DBM_Excavation02 stage 90 done AND 140 not done; player in Rkund cells | 16 scenes with the explorers talking; keep banter rare |
| Chimes vision and ghost lead | DBM_Excavation03Prelude stage 1 done AND 15 not done | ghost-follow scene |
| Snow Elf ghost sequences | DBM_MuchAdoAboutSnowElves stage 310 done AND 400 not done (ghost transform 398, vision 399) | 15 ghost scenes |
| Cave-in and Marassi's death | DBM_Excavation03A stage 61 done AND 80 not done | **hard silent** until 75; then grief lines only |
| Trinimac / Tulrin / temple finale | DBM_Excavation03A stage 140 done AND 175 not done; and 300 done AND 350 not done | 35 scenes in this quest |
| Echoes of Madness (Pelagius' mind) | DBM_EchosOfMadness stage 30 done AND 45 not done | Sheogorath scenes 01-05 plus End |
| Sancre Tor binding and Herald | DBM_ShatteredLegacy stage 225 done AND 250 not done; and 280 done AND 300 not done (Sanctum of Akatosh, cell 014DD0) | Herald of Akatosh speeches |
| Wulfharth tomb scenes | DBM_ShatteredLegacy stage 260 done AND 265 not done | DBM_SLYsmir01-04 |
| Planetarium reveal | DBM_PlanetariumQuest stage 46 done AND 50 not done | DBM_PQSTG46Scene |
| Waystone jump | DBM_WaystoneQuest stage 10 done AND 20 not done | teleport into the pocket realm |
| Ambient staff and patron scenes | any DBM_ExplorerScene## / DBM_MuseumScene## running | Too many to list. Easiest guard: the follower's `IsInScene` = 0, plus a check that no LOTD staff NPC within about 1,000 units `IsInScene`. |

Hard silent anywhere: the player is in dialogue with Auryen, Avram or any explorer (`IsInDialogueWithPlayer` on the follower's own target, or `GetDialogueTarget`).

---

## 4. Places (for "player is in X" triggers)

The whole museum is location **DBM_DragonbornGalleryLocation `1432E2`** (Dragonborn Gallery, child of Solitude `018A5A:Skyrim.esm`). Most rooms are child locations of it. `GetInCurrentLocation 1432E2` should be true in every child room, because child locations count. If testing shows otherwise, OR the child list below.

| Room | Location (LCTN) | Cell(s) (use GetInCell for room-level) |
|---|---|---|
| Reception and Hall of Heroes (office, upper hallway, gala area, Marassi memorial, Explorers dome) | DBM_HallOfHeroesLocation `5D2D83` | DBMDGHallofHeroes `125EE6`; haunted variant `1ABB45`; heist (emptied) variant `2AE7D5`; Museum Storeroom `12517D` |
| East Exhibit Halls: **Daedric Gallery + Hall of Oddities + Hall of Lost Empires** | DBM_EastExhibitHallsLocation `5D2D82` | DBMDGEastExhibitHalls `125C71`. All three halls share one cell. Room-level split needs position checks or trigger boxes. Tour markers TourDG / TourHOO / TourStopHOLE mark each wing. |
| Gallery Library | DBM_LibraryLocation `5D2D88` | DBMDGLibrary `2F8D08` |
| Gallery of Natural Science | DBM_NaturalScienceLocation `5D2D87` | DBMDGNaturalScience `1256C8`; haunted variant `17CBFE` |
| Armory | DBM_ArmouryLocation `5D7E90` | Armory `168884`; East Wing `167B25`; West Wing `2B487A` |
| Dragonborn Hall | DBM_DragonbornHallLocation `5D7E94` | DBMDGDragonbornHall `741ACF` |
| Hall of Secrets | DBM_HallOfSecretsLocation `5D7E95` | finished `18F4FB`; bare (pre-quest) `0A9278` |
| Safehouse (player home, guest/follower rooms) | DBM_SafeHouseLocation `139074` | DBMDGSafehouse `0AEACE`; haunted variant `0F1B91` |
| Planetarium | DBM_PlanetariumLocation `5D7E92` | DBMDGPlanetarium `18F863` |
| Hall of Wonders (CC patch) | DBM_HallofWondersLocation `0062AF:DBM_CC_HallOfWonders.esp` | `0104C9:DBM_CC_HallOfWonders.esp` |
| Explorers Society Guildhouse | DBM_GuildHouseSolitudeLocation `5D7E91` (no parent; not under the museum) | DBMGuildhouse `062832` |
| Vaults of Deepholme | DBM_DeepholmeLocation `66B745` (child of museum) | DBMDeepholme `005955` |
| Dev Aveza airship | DBM_DevAvezaLocation `66B743` (child of museum) | DBMAirshipCabin `37BF27` |
| Field stations | North `34D523`, Reach `2BB744`, Eastmarch `2BB745` | `1D5A02`, `28EE1E`, `2F4A2E` |
| The Wayward Rest (inn) | DBM_WaywardRestLocation `0F0B20` | `0F2220` |

Quest and excavation sites:

| Site | Location | Cells |
|---|---|---|
| Windcaller Pass | - | North `1942FA`, South `1943CD` |
| Ruins of Rkund | Skyrim `0D5667` | `504BBE`, Magma Silo `505676`, Hall of Puzzles `50A049`, Sepulcher `50F330`, Karagas' Maze `50FE29`, Karagas' Tower `50FE28` |
| Greenwall Lost Ruins | Fort Greenwall `019180:Skyrim` | `23CBD8` |
| Trinimac's Temple | - | Ruins `25B8EF`, Temple `26FFAD` |
| Temple of the Venerable Ones | - | `22C23C` |
| Jolgeirr Barrow | - | `11CBAA` |
| Sancre Tor | `66B744` | Entry Halls `121BAC`, Prisons `122369`, Sealed Halls `122587`, Catacombs `1226BD`, Hall of Judgement `1226BE`, Tiber Septim's Shrine `122DA7` |
| Sanctum of Akatosh | - | `014DD0` |
| Ayleid pocket realm | - | `166D76` |
| Dragon's Fall (Wulfharth) | - | `1265AB`, Depths `1266B1`, Sanctum `127B84` |
| Fort Pale Pass | Pale Pass `45CC3C` | `128F86`, Storeroom `01B3CB`, Vaults `01A5E9`, West Tower `01AF0D`, Pale Cave `02055D` |
| Raven's Rest (Morag Tong) | - | `120EE1` |
| Engelmann's Rest | - | `1938C0`, Sanctuary `1938DC` |
| Stendarr's Refuge | - | `021C84` |
| Vigilant hideouts | `1901B1` | Mzuhlac `0F221E`, Bromgolt `0F2221`, White Bluff `0F2222` |
| Snow Elf annexes | - | Alftand `5C7EE3`, Xrib `5C7EE4`, Irkngthand `5C7EE5` / `5C7EE6` |
| Others | - | Dregas Volar's Sanctuary `125A26`, Rains's Shelter `064F7D`, Sargruunde `27F80F`, Mzulft sealed chamber `1D5B20` |

---

## 5. What our followers already say about LOTD (topics only, so we don't repeat them)

**Val Serano.** His LOTD content lives in `AX ValSerano.esp` (quest ValAddon02 "Legacy of the Dragonborn", `D1004D`). `AX ValSerano-LOTD.esp` patches and enables it. He covers almost everything.
- **Backstory hook**: Auryen hired Captain Serano to find the Ayleid "Star of Solitude", and the delivery is overdue. Auryen himself gives the "overdue shipment" quest. Auryen defends Val to an investigator ("academic institution").
- **Explorers**: asks to join. Toasts "to the Explorers" and "to absent friends". Opinion topics on Darnette (mislabels fossils, cards, rough edges), Eriana, Latoria, Kyre (scorch marks from the Rkund maze), Madras, Marassi (bad dresser, university trouble-maker, grief), Avram (forgiveness, his father demoting him off the Dark Rose), Auryen (Gwylin University trio), Millie and the staff ("growing on me").
- **Quest reactions**:
  - Haunting: the nightmare-comfort scene, the Macnarian statue money, "never get married".
  - Heist: "professional job", and a Jelal/Tarek mirror talk.
  - Windcaller ("no one died", happy) and the raccoon.
  - Malrus' Codex (Apocrypha suspicion).
  - Dev Aveza (in love with the airship, piracy jokes, a captain offer).
  - Calcelmo fanboying.
  - Deepholme ("bottomless pit for gold").
  - Visage chimes, the Guardians (distrusts Argus, Ezra dislikes you), the Herald ("above my pay grade"), coma relief after the cave-in, and Auryen's Snow Elves manuscript.
  - Vigilant outcomes (Morgi, Astrian, Tylende, forgery).
- **Dig, puzzle and travel**: dig help, puzzle advice for Rkund, ice and chimes, sea-shell collecting for the spyglass display.
- **Backpack**: "belongs in a museum, not my backpack".
- **133 idle lines** covering:
  - each hall
  - chaurus hate
  - the Hermaeus Mora portrait in Auryen's office
  - Hall of Secrets skulls
  - the restricted section, and kicking Urag out
  - Remi's projects
  - mannequins
  - dragon-claw displays
  - Karagas' daughter's tomb
  - the Pale Pass blood
  - the crusader armor
  - spider machine threats
- His daughter **Ravani** has kid lines: wants a dragon model, likes Natural Science, wants to play with Henry, hopes Chompy gets a display.

**Remiel (Remi).** `HLIIRemiLOTD.esp`, about 725 lines.
- **Stay-home system**: she lives at the museum or Guildhouse and has her own Dwemer-themed room with Scrap's statue, a Nchuand-Zel painting, a stone bed and gleam blossoms.
- **Commentary** on nearly every LOTD quest beat:
  - intro relics; Hall of Secrets ("stash evidence of your crimes")
  - the haunting (a ghost-hunting fan); the heist
  - Waystone/Crossroads; Deepholme
  - every Windcaller, Rkund and Planetarium beat (she begs to stay with Madras)
  - Much Ado (despises Calcelmo; Freir's skooma)
  - Phynaster/Syrabane rings, the Spear, Greenwall
  - Marassi's death and Kyre's appointment
  - Trinimac and the glacial temple, the Neb-Crescen ("avenged Marassi")
  - field stations; Tools of Kagrenac (jealous of Auryen)
- **General museum musings**:
  - thieves, guards, patrons' money
  - Auryen's age; Pelagius' room
  - the Talos temple site; civil war
  - Henry climbing shelves
  - Latoria scared, Eriana a thief, Madras her best friend, Eggelman vs Scrap
- **Explorer banter scenes**: about 30 two-way scenes with Madras, Eriana, Marassi, Kyre and Latoria.
- **Quest "An Unlikely Teacher"**: an Ancient Falmer apprenticeship under Calcelmo.
- **Fragment exchange**: she turns fragments into keystones.
- **Artifact lore** on request (Thornblade, Skullcrusher, St. Felms, Eliedon's Ward, and others).
- **Dev Aveza** idles.

**Kaidan.** `Kaidan - LotD Patch.esp` (quest KLOTD "Kaidan LotD Commentary").
- One line per room: Dragonborn Hall, library, Hall of Heroes, armory, storeroom "wine room", ale making, Deepholme, Planetarium, Natural Science "tent in here", Guildhouse, Hall of Secrets, Safehouse, garden.
- Running jokes:
  - "museum is huge / testament to your ego"
  - the moving mannequin and mushrooms
  - the "Legacy of Kaidan wing"
  - meat closet / horker
  - the Orc guard
- Beats: guildmaster congratulations, haunting relief, heist outrage then relief, Symmachus paralysis, Marassi excavation start, Fafnir, Greenwall, the Rkund "terrible creature", Eggelman, the Book of Wonders quill, Schneider's sextant.
- Topics on the East Hall, the Waystone ("can I come?") and the Amulet of Kings ("looks great on you").
- Staff opinions: likes Auryen and his tours, Madras eccentric, Latoria the Khajiit exception.
- A last-conversation "honoured to have made it this far".
- `Kaidan - LotD Patch - Museum Shipment Crate.esp` has **no dialogue**. It only adds a crate.
- Base Kaidan (BWB Extra Dialogue) mentions "relic hunter" in a love-life line and Calcelmo's Dwemer museum. These are not LOTD.

**Xelzaz, Lucien, Inigo, Gore, Redcap: no LOTD dialogue at all.** I searched every dialogue line in their plugins for museum, Auryen, gallery, explorer, curator and the staff names; nothing hit.
- `DBM_Xelzaz_Patch.esp`, `LOTD_TCC_Xelzaz.esp` and `DBM_Remiel_Patch.esp` only add display and checklist support for their gear.
- Lucien has an "Enora the Explorer" ditty that is unrelated.
- Gore and Lucien mention Jurgen Windcaller only in vanilla context.
- This is open ground: write freely for these five.

---

## 6. Twenty-five banter hooks (situations, not lines)

1. **The empty museum.** The first walk through empty display cases. Each follower imagines what *they* would put on the plinth with their name on it. Redcap wants a whole case for a shiny spoon.
2. **Who's the real Dragonborn Hall.** Standing in the Dragonborn Hall, the party argues over who did the actual work on each trophy. Kaidan has already claimed credit, so the others pile on.
3. **The Daedric Gallery hum.** Xelzaz, Lucien and Gore each feel the "between planes" barrier differently. One is fascinated, one is nervous, one wants to smash it. Gore's Vigilant ties make it personal.
4. **Taxonomy fight in Natural Science.** Lucien (fauna and flora cataloguer) corrects the dioramas. Redcap is offended by how a riekling or a boar is shown. Inigo asks if anything here is edible.
5. **The chaurus display.** Val hates it, so the others tease him. Someone moves it a little each visit.
6. **Library rules.** Remi and Lucien race for the restricted section. Inigo picks the lock "for them". Val offers his own lock opinions.
7. **The Hall of Secrets inventory.** A party vote on what goes in the panic room. Gore's dark trophies, Inigo's past, Kaidan's Akaviri secrets.
8. **Avram and second chances.** After the heist, the followers with brothers or criminal pasts each speak to Avram's choice. Inigo carries the most guilt and gets the quietest line.
9. **Marassi's memorial.** At the Hall of Heroes memorial after stage 70, a round of toasts. Each follower remembers one small thing Marassi did on a dig.
10. **Fafnir's fan club.** Redcap and the raccoon as rivals or allies: two small chaotic thieves. Remi's Scrap and Madras' Eggelman get dragged in.
11. **Digging duty.** At the "help dig" prompts, who actually holds a shovel? Gore digs alone in two minutes. Lucien supervises. Inigo "finds" the coins.
12. **The Rkund entrance was behind us.** A blame round after stage 80: who said "try the other spot"?
13. **Haunted night watch.** During the haunting window, a short campfire-in-a-museum ghost-story round. Gentle, not during the dream stages. Lucien is terrified and Remi delighted.
14. **The fire nightmare after-talk.** After stage 80 the player woke from a dream where everyone burned. Each follower reassures in character: Val already has "I'm right here", so others take different angles (Gore blunt, Inigo poetic, Redcap literal).
15. **The Vigilants accident review.** If the player chose "accidents", the party grades the murders like a heist crew. Gore is torn if he has Vigilant faith.
16. **The airship.** The Dev Aveza gift. Who gets to steer? Val has already claimed captaincy, so Xelzaz and Inigo bid for navigator, Redcap for "lookout up the mast", Gore refuses to fly.
17. **Sheogorath again.** After Echoes of Madness, followers who met Sheogorath elsewhere compare notes. The ones who didn't think the player has gone mad.
18. **The Herald of Akatosh.** The night after stage 245, a quiet "what did the dragon say to you" round. Faith versus scepticism split across the party.
19. **Wearing the Amulet of Kings.** Imperial Lucien is overwhelmed. Kaidan the Akaviri has his own feelings about the Septims. Redcap asks whether it is food.
20. **The Hand of Glory.** While the cursed hand is carried, each follower notices the player paling. Who suggests giving it to Eriana?
21. **Deepholme's lich.** Inside the old Atmoran prison, followers react to elves being jailed there by Ysgramor's people. The Nord Gore and the elf-sympathetic Remi disagree.
22. **Patron gossip.** In the reception hall, the party comments on the patrons. The entitled Altmer twins, Henry the shelf-climber, Radcliff writing them all into a song.
23. **Guildhouse balcony at sunset.** The guild's grand view over Solitude's wall: a "what are we doing with our lives" moment. Ends with someone pushing someone else near the edge (the Burondis joke).
24. **Kagrenac's tools on display.** Remi warns everyone off Sunder. Gore wants to try it anyway. Lucien reads the plaque aloud too long.
25. **The last case filled.** When the museum is near complete, a party retrospective. Each follower names their favourite relic they personally carried. Val: "half the payment".
