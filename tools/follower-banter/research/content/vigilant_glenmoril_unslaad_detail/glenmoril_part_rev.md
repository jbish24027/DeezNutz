# GLENMORIL - the "Revenant" act (zzzRev*, Act 4)

Sources: dlgc.txt lines 4311-6014, glen_story.txt (zzzRev* sections), the decompiled Rev scripts in glen_misc\scripts\source, and NPC names read from the live load order.
All FormIDs below are XXXXXX:Glenmoril.esm. "UA" means the unique actor in that alias.
The mod reports itself as version 0.96. The act ends on a "To be Continued. Wait V0.97" message.

---

## 0. Quick answers

- **What is "Revenant"?** It is the developer's label for Act 4. The Departure quest sets `gCurrentAct = 4`. The word "Revenant" never appears in spoken lines. It only shows up as "Generic Revenant", the shared dialogue quest. The name fits the act's theme: the player is "one who returns". The Black Owl says the journey will repeat "until your wish comes true". The act also saves a "dejavu" flag to a JSON file so that a replay remembers it. (The meaning is my reading. Unsure.)
- **Where is it?** In the worldspace **Svartibrunnr** (000D62, `zRevNamiraRealm`; location 006FFC). Old Norse for "black well". In dialogue it is called **the Black Spring**. It is a dream-sea land filled with Alduin's black sludge. Cities and ruins from many times and places have washed up there, all under a **Blue Star** that never sets. It is always night.
- **The hub** is **Pailune** (location 006FFD), a city Yelem built in an Anequina oasis. Inside the city are:
  - **the Square (Plaza)**, guarded by the musketeers. This is the safe zone where the rescued citizens set up shop.
  - **Pailune Church** (the "Brunnr Church"), where Boltzmer preaches.
  - The citizens: Pawnbroker Emil (016129), Alchemist Hands-of-Rock (016128), Innkeeper Gonzo (01612A), Charlatan Joel (01612B), Blacksmith Roland (016127). Also Musketeer Wilmer (016126) and Mayor Ra'scon (36C629).
- **Who is Hamah?** Hamah (base NPC 007BBF; she has an extra copy at each guide spot) is the **"Daughter of Kyne"**, a Kyne priestess.
  - She was a **Snow Elf girl**, reborn by the Nede sorceress **Anem**. Her parents were storytellers who served Jephre (Y'ffre).
  - **Lalanoah**, from the earlier acts, was **her duplicate**, one of her "daughters". Hamah made those daughters "to be loved and to attract those around them".
  - Yelem caught her in Skyrim, showed her in a freak show, and kept her as a specimen in his research tower.
  - She is acid-tongued and calls the player a "spineless coward" and a "cheeky little brat". She swears she never loved her daughters, yet underneath she is lonely and quietly kind. She calls the player "good child", and the player can call her "mom".
  - After the transfusion she becomes the player's **voice-guide**. Copies of her stand at the Plaza, the Church, the Orchard, the Port and the Gate, and she comments on each area.
  - In VIGILANT, the Holy Pipers' creed is "the extermination of Hamah and her bloodline". This is a direct link back to that mod.
- **The Blue Star.** The Black Owl promises that if the player can "stand on" the Blue Star, their wish comes true. That is the goal of the whole act.
- **Blood curses** are the act's main mechanic. The player collects them by devouring things: Hamah's blood, Ja'bal, Ja'zel, Anatomancy, Yelem, Lalanoah, plus optional extras such as the Worm of Alduin and the cheese. The final scene reacts to how many the player carries (`CountBloodCurse`).
- **Hidden scores.** Choices also add to three hidden values: **Humanhood**, **Beasthood** and **Mnemoli/Detachment** (`zzzRevGHumanHood`, `zzzRevGBeastHood`, `zzzRevGDetachment`). Devouring raises Beasthood and Mnemoli. Refusing raises Humanhood.

---

## 1. Story summary, in order

**Departure (from the end of Act 3).**
- When "Lice and Maggots" (zzzLaMMq05) reaches stage 150, Ja'zel has been chased down in Hinnom. That stage starts Departure.
- The Black Owl, **Jhunal the Black** (012C70), waits by a boat. He is calm and cryptic, and treats everything as a game his "lord" is watching. He admits the witch hunt was all to bring the player here. He says Ja'zel's wish came true: "You were his wish." He also says the Holy Pipers began as a wish of a boy named **Malmanius**, and that their story "began rewriting itself" without him.
- They sail into the Black Spring. He drops the player off and vanishes.

**Arrival: Pailune.**
- Pailune is in chaos.
  - The "followers of Hircine", the **Chick Traders** of ancient Anequina, are turning citizens into beasts and hunting them for pelts.
  - Rioters fill the main street.
  - A plague is spreading, and pointy-headed **Radiance cultists** (ex-Meridia worshippers) rip out people's guts.
- **Musketeer Wilmer** holds the Square and asks the player to send sane survivors there. This is the "Musketeer's Hope" chain, which leads to the five citizen quests.
- **Chaplain Master Boltzmer** (008824) is Yelem's former assistant. He wears an iron mask because "he blew his own head off". He hides in the church, and the beasts avoid him. He is polite, creepy and long-winded. Everyone distrusts him.
- **Yelem** is a Dwemer survivor, banished from Arkngthamz for experimenting on sentient beings. He built Pailune, went mad and vanished toward the rotting port to the southwest.

**The player's goal.**
- The player is looking for a "Daughter of Kyne", which is Hamah.
- **Robin the Shortstrider**, a thief who sells information, points the player to Boltzmer and then to Yelem's study in the research tower.

**The main threads.** They are open-world and can be done in any order.
1. **East: the forest of Hircine (Kaan Feykro, the Orchard, Hangman's Island).** Werewolf "Lycanthropy" boss fights with the shaman Zan'zar.
   - Moonlit Hunt ends at the church. Boltzmer gives the player a key to all of Pailune.
   - In Mark of the Hunter the player breaks the Seal of Hircine.
   - In **Strange Fruit**, Prince Ra'hajir and Clerk Ja'i each ask the player to kill the other. Then the player fights the mad, furless King of Anequina, the Exalted King, and the **Arcana of Ja'bal**.
   - **Ja'bal the Great Cat** is a "gardener" from another kalpa. Hircine says he "may not be from this kalpa", and Ja'zel suspects he was really an Argonian or a Hist creature. Ja'bal sowed the "Chick and Egg" myth so that the player would be his "harvest".
   - The player then devours or burns Ja'bal's remains.
2. **West: the research tower.** In **Desiccated Embryo** the player finds Hamah's dried body. The choice is to take a blood transfusion (gaining her blood curse and her voice) or destroy the syringe.
3. **Southwest: the Worm-Eaten Port, the Cannibal Hill and the Fishing Village.**
   - In **Baby of Nightmares** the player meets **Athanasius** (349865), called "the Vigilant", at the giant corpse of **Anem**. He is guilt-ridden and says he could never kill "Malmanius... my innocence". He explains that the **Sacred Anatomancer** (from VIGILANT) "was born here" as an echo of Yelem, the player and himself.
   - He dies, and the player runs the **Rite of Cannibalism**: killing "echoes" of themselves. The reward is the Baby of Nightmares, a fetus.
   - **Namira's cat** guides this road. In "To Fishing Village", Namira opens the gate.
   - Yelem has already left his body. The player searches it and takes **Yelem's Cord**.
4. **The soul chase: Yelem's blood curse.**
   - Boltzmer says: "Lord Yelem went to meet the Nerevarine. Seek Akulakhan." Ja'zel's phantom says: "Find Sotha Sil."
   - The trail goes through the Ravine of the Old Serpent, Akulakhan's Head and the **Will of Dagoth** boss. This gives the "Blood Curse of Yelem". How exactly the curse is gained is unsure; the Dagoth link is my inference.
5. **The Ja'zel thread: Stray Cat, then Sacrament of Cat.**
   - **Mar-Dro the Peddler** is a chatty, cowardly, loving Khajiit trader. He is lost here and wants to get home to his pregnant wife Tahana and their unborn son **Ja'zeri**.
   - He is also the dead father of **Ja'zel**. Ja'zeri grew up to be Ja'zel, the white lion and the player's nemesis from the earlier acts.
   - On a void ship, Mar-Dro learns that he died in a cave long ago, that Tahana died of illness, and that his son was sold to slavers. He mutates. He asks the player to "help" his son anyway and gives them a moonlight moth.
   - In **Sacrament of Cat**, the player enters **Dreamsleeve** through "Ja'zel's Neural Pathway", follows Ja'zel's ghost and kills him again: "Ja'zel, Scion of the Moon".
   - The player offers his head at the Fated Forge, and **Torvesard Replicanum** (42A6A4) appears. He is a servant of the lost Prince **Ithelia** ("my Prince... She... the Gold Road... Staff of Many Paths").
   - He reveals:
     - Ja'zel was the "Guide", a failed Owl creation that Torvesard empowered.
     - **Vaermina** has been steering this all along.
     - Ja'zel's blood curse will hide the player's soul from **Hermaeus Mora**. The Black Owl's "lord" is implied to be Mora.
   - The player either devours the curse (Ja'zel's phantom then follows them) or casts it into the Forge (the bad end). Then Torvesard either kills himself or fights the player.
6. **The Ahzidal and Kyne thread (north, "Saarthal - City of Tears").**
   - The player climbs Ahzidal's Ladder, defeats Ahzidal's three forms and talks to his remains.
   - In **The Lost Storyteller**, at the Temple of Kyne, Hamah takes **Lalanoah's remains**. She weaves her daughters' memories into a "Blood Curse of Lalanoah". She takes her mask off, reveals she looks exactly like Lalanoah, and invites the player into a coffin to dream of **Falmereth**, the Snow Elf homeland in stories.
   - The quest ends with the "To be Continued" message. This is the cliffhanger into the next act.

**The finale: Feast of Love (zzzRevMq01).**
- At the Spring or Gate (the "Gate" Hamah: "This is the end of the road"), Boltzmer judges the player by the number of curses they carry. He ranges from "your soul is only slightly stained, turn back" to "You are truly the Third Serpent".
- He tries to devour the player. He loses, and **Yelem's Vestige** (5D0FC9) bursts out of him: "Come, my dear Boltzmer. Let us go together, to the Blue Star."
- Yelem dies saying "The experiment... was a success..."
- **Twist:** Ja'zel hints that Boltzmer "devoured even a half of his very self", and Hamah calls him "the final form of all without their selves". Boltzmer and Yelem were two halves of one being.

**Endings and choices in this act.** Each is a fork that affects the hidden scores.
- Transfuse or refuse Hamah's blood.
- Kill Ra'hajir or Ja'i.
- Devour or burn Ja'bal.
- Devour or reject Ja'zel's curse.
- Torvesard dies by suicide or by combat.
- Devour or return Lalanoah's curse.
- Eat or discard the Worm of Alduin.
- Eat or discard the cheese embryo.
- Accept or refuse Sister Gaga's cocoon.
- Release Scab or not.

**Main NPCs and personalities**

| NPC | FormID (UA) | Notes |
|---|---|---|
| Jhunal the Black (the Black Owl) | 012C70 | Polite, detached manipulator, "I am only here to help". Serves an unnamed "lord", implied to be Hermaeus Mora. |
| Hamah | 007BBF (base); 5F96B2 (Kyne Temple copy) | Bitter, mocking, mother-like, secretly tender. The guide voice from Desiccated Embryo onward. |
| Chaplain Master Boltzmer | 008824 (church); 600268 (boss) | Iron-masked, unctuous preacher, "the lice were singing about you". The final boss. |
| Yelem / Yelem's Vestige | 5D0FC9 | Amoral Dwemer experimenter who seeks the Blue Star. Talked about everywhere, met only at the end. |
| Ja'zel (ghost / "Scion of the Moon") | 51BE07 / 51524A; phantoms 572FD5-572FDB | Violence as love, "Ja'zel is pleased with your growth". Speaks of himself in the third person. |
| Torvesard Replicanum | 42A6A4 | Cold, dutiful Daedric agent of the lost Prince Ithelia. Envies mortals. |
| Mar-Dro the Peddler / mutated Mar-Dro | 3D45D1 / 3D4666 | Comic, boastful, loving father. Ja'zel's dad. "Khajiit hates you... and yet, he still loves you." |
| Aisha | 2D49CE | Aloof Khajiit assassin, sarcastic ("You're such a bitch." / "You finally noticed?"). Hunts her "Prince" Ja'cobee, Ra'hajir's half-brother, and fades away to join him. |
| Robin the Shortstrider | 3B7825 | Cockney-style thief and info-broker, "mate". Charges 100 gold. Killed by Boltzmer's assassins. |
| Ruddy Man | 2DA636 | A man cursed into Dreugh shape by a red shell linked to Vivec's Sermon 28. Gentle and hopeful. He goes mad after seeing the future, and the player fights him plus the "Worm of the Deep Sea". |
| Scab | 35AF30 | Foul-mouthed city executioner who hunts Radiance cultists. Ends as a talking remnant: "Turn these talking sacks of shit into silent sacks of shit." |
| Sister Gaga (the moth man) | 41930B | Shy ex-nun turned into an ancestor moth. Weaves a swaddling cloth from fjyron song for a cocoon, a gift from Emperor Belharza. |
| Apka-Lul the Ruinach | 41EED6 | A philosophical Ruinach who wants to free Mehrunes Dagon from the "curse of words". Burns out with "hope" and becomes a boss. |
| Aushahlaas (dragon) | 2095ED | Proud, cursed dragon, loyal to Bormahu (Akatosh), calls the player "Joor". Asks the player to free his friend Briiviingrein. |
| Prince Ra'hajir / Clerk Ja'i | 0154FE / 015538 | Weary prince versus fanatical clerk of the mad King of Anequina. |
| Ja'bal the Great Cat | 016396 | Alien "gardener" who speaks in myth. |
| Athanasius ("Vigilant") | 349865 | Remorseful cannibal-rite keeper. Tied to Malmanius and the Sacred Anatomancer. |
| Malmanius the Zealot | 0160B5 | Innocent Meridia devotee who hands out a "sun" weapon. The boy whose wish made the Holy Pipers. |
| Clavicus Vile / Barbas | 17636C / 17636D | Vile is bored and refuses to name "him" (the bookworm, Hermaeus Mora). |
| Sheogorath + Skooma Cat | 5DEA0E / 5DEA0D | Two Sheogoraths bickering about cheese. |

**Daedric cats**

| Cat | FormID | Personality and role |
|---|---|---|
| Azurah (Azura) | 1C1459 | Haughty: "Know your place." Gives a weapon and a prophecy: "accumulate the curses and jump into the maw". Gives the repeatable mercy-killing of her monster followers. Explains the Hist star, House Sul, and a soul trapped in Yelem (Gen Azura 355295). |
| Hircine | 1C145A | Hunter talk. Remembers the player from Vahdin Holt (an earlier Glenmoril act). Made the beast-curse pact with the King of Anequina. |
| Mouth of Namiira (Namira) | 1C145B | Calls the player "my dear disciple" and revels in rot. Guides them to the Cannibal Hill and to devouring Yelem. |
| Blood Cat / Sangiin (Sanguine) | 33DF14 / 1C145E | Party-killer cat. Runs the Bloody Circus. |
| Skooma Cat | 5DEA0D (Rev); also zzzGHM05SkoomaCat (earlier act) | Cheshire-cat nonsense ("We are all mad here"). Turns out to be Sheogorath's cat form. |

**Links to VIGILANT and to earlier Glenmoril acts**
- **VIGILANT:**
  - The **Sacred Anatomancer** and the **Holy Pipers** both come from VIGILANT. The Black Owl says they began as **Malmanius**'s wish, and Malmanius appears here as "the Zealot".
  - The Pipers swore to exterminate Hamah's bloodline.
  - Athanasius is called "Vigilant", but I found no Athanasius in Vigilant's dialogue. Whether he is a returning character is unsure.
  - **Molag Bal and Stendarr are not mentioned** in this act's lines.
- **Earlier Glenmoril acts:**
  - Lalanoah: Hamah's duplicate. Her remains are carried into this act. The slug friends say she "missed the Chick Trader's carriage".
  - Ja'zel, killed at the end of Act 3, returns as a ghost, a boss and a phantom.
  - The Black Owl (Jhunal).
  - **Anem** and **Aradia**, witches of Hinnom: the player killed Anem earlier, and Ja'zel threw them into Hinnom.
  - Vahdin Holt.
  - The Chick Traders.
  - Ja'cobee.
  - Felix and the Sanctuary of Namira belong to the earlier GH act.

---

## 2. Quest list (Glenmoril.esm FormIDs)

### Main
| EditorID | FormID | Name | Summary | Starts | Key stages | Completes |
|---|---|---|---|---|---|---|
| zzzRevMq00 | 171135 | Departure | Talk to the Black Owl, board the boat, sail into the Black Spring. | zzzLaMMq05 stage 150 starts it at stage 0. | 0 = Owl and boat appear. 10 = departure. 20 = on the boat (water-breathing, sail scene). 21-28 = waypoints. 28 = stop. | **30** (Owl leaves, player gets the Music Box Key, and Lice and Maggots is set to stage 160). 999 = skip. Objective: "Talk to the Black Owl and get on the boat". |
| zzzRevMq01 | 60026B | Feast of Love | Final confrontation: Boltzmer, then Yelem's Vestige. | Unsure. No quest script starts it; probably a trigger at the Gate or Spring. | 10 = fast travel off, arena barrier, curse count, scene Sc01. 20 = fight Boltzmer. 30 = transformation scene. 38 = becomes Yelem. 40 = fight Yelem. | **50**. Objective: "Defeat Yelem". Beasthood +3, Mnemoli +5. |

### Story side quests
| EditorID | FormID | Name | Summary | Starts | Key stages | Completes |
|---|---|---|---|---|---|---|
| zzzRevSub01 | 015B58 | Strange Fruit | The mad King of Anequina's orchard. | Exploring the east forest. Objective 1: "Explore the forest to the east". | 10/15 = Prince asks the player to kill Ja'i, or Ja'i asks the player to kill the Prince. 20/25 = target killed. 21/26 = reported. 30 = King fight. 36 = moonlight. 37 = King scene. 38 = Exalted King. 39 = Arcana of Ja'bal. 40 = starts Communion: Ja'bal. | **50** ("Report to the Prince about the End of Madness"). 400 is the alternative end. |
| zzzRevSub01Jabal | 48BF99 | Communion: Ja'bal | Devour or burn Ja'bal's remains. | Strange Fruit stage 40. | 10 = devour (Ja'bal blood curse, blur effect). | **10** or **100** (burn). 900 clears the curse. Objective: "Choice: Devour OR burn Ja'bal's remains". |
| zzzRevSub02 | 01710D | Desiccated Embryo | Find Hamah's body in Yelem's research tower. | Objective 1: "Find the Daughter of Kyne". | 5 = choice. **10 = transfusion: knocked down, controls disabled, fade to black.** 20 = wake up, Hamah appears. | **40** after talking to Hamah (objective 20 "Talk to Hamah"). 500 = destroy the syringe. |
| zzzRevSub03 | 34980C | Baby of Nightmares | Athanasius, Anem's corpse, the cannibal rite. | Objective 1: "Retrace Yelem's footsteps". | 5 = find Athanasius. 10 = ritual marker. 20 = monologue (barrier up, fast travel off). 30 = Athanasius dies and the Rite begins. | **40**. Player gets the Fetus (Baby of Nightmares). Beasthood +3, Mnemoli +8. |
| zzzRevSub03Rush | 3ABF2B | Rite of Cannibalism | Waves of "echoes of the Player". | Baby of Nightmares stage 30. | 0 = fog. 5-46 = waves. | **60** (sets Sub03 to stage 40). Objective: "Calm the echoes of the Player". |
| zzzRevSub04 | 51525D | Sacrament of Cat | Into Dreamsleeve; kill Ja'zel again; meet Torvesard. | Mar-Dro's moon moth from Stray Cat; stage 10 takes it. | 10 = Ja'zel's remains. **20 = Dreamsleeve door opens.** 25-75 = chase the ghost through 6 spots (scenes Sc02-sc06). 100 = talk. **110 = D4C portal scene (fast travel off).** 116 = white-out. 120 = boss. 130 = win. 150 = head on altar. 200 = Torvesard arrives. 220/230 = devour the curse (starts Jazel Phantom). 300/310 = Torvesard kills himself. 400/410 = fight Torvesard. 600 = Forge, bad end. | **500** (Torvesard dead) or **610** (he leaves, bad end). |
| zzzRevSub04Jazel | 572FEC | Jazel Phantom | Ja'zel's phantoms appear at the Plaza, Church, Orchard, Port, Namirapolis and the Gate. | Sacrament of Cat stage 230. | 0 = enables all 6 phantoms. | **100** (curse fully integrated and removed). |
| zzzRevSub05Intro | 5F2B94 | The Lost Storyteller | Hamah at the Temple of Kyne makes Lalanoah's curse; Falmereth teaser. | Unsure (Temple of Kyne trigger). Needs Lalanoah's remains. | 15 = give the remains. 20 = wait 1 hour outside. 30 = scene. 40 = choice. 45 = devour (Storyteller ability, white-out, Hamah unmasks). 46 = return. 60 = seal-breaking scene. 70 = descend. 80 = Hamah's story scene. **90 = enter the coffin ("To be Continued. Wait V0.97").** | **100** ("In Falmereth"). |
| zzzRevSub06Key01 | 62F3BC | Yelem's Cord | Search Yelem's abandoned body. | Unsure (Fishing Village / Hill of Rebirth). | 0 = cord placed. | **10**. Objective: "Search Yelem's body". |
| zzzRevSqCheese | 5D7AD9 | Pale Cheese | Sheogorath's 400-year-old onion squire "cheese"; fight St. Bazura in the Cheesy Sewer. | One-Finger (Misc06) stage 100. | 10 = talk. 20 = sewer. 30 = Bazura scene. 40 = fight. 100 = cake scene. 120 = choice. 200 = eat. 300 = discard. | **900**. Objectives 120/121: "(Optional) Devour / Discard Embryo of Cheese". |

### Companion-style arcs (NPCs who travel ahead and are met again)
| EditorID | FormID | Name | Summary | Key stages | Completes |
|---|---|---|---|---|---|
| zzzRevCqAisha | 360BD2 | Snow Cat | Aisha hunts her "Prince", Ja'cobee. She moves from Church, to Research Tower, to Yelem's room, to Ja'cobee's house, to the Kanra village, to the "Lost Voice". | 30 and 40 = scenes. 60 = "Obtain an artifact associated with Kynareth/Kyne" and "Show Broken Idol of Kyne to Aisha". 70 = she fades out. | **80** (Aisha vanishes). |
| zzzRevCqPedlar | 3D45DE | Stray Cat | Rescue Mar-Dro from a werewolf (stage 7). He moves from Church, to Forest, to Kanra village, to the north bonfire, back to Church, to the Yelem School. | 53 = Ahzidal checkpoint. **80 = mutated in the Void Ship.** 85 = scene. 90 = "Help this one's child". | **100**. Leads into Sacrament of Cat. |
| zzzRevCqRobin | 3B7828 | Bad Company | Robin sells information (100 gold each) and moves from Church to Castle. | 100 = Robin dies (set by Assassin stage 0). 110 = search the corpse. Objective 110: "Open the secret door in the library". | **120**. |
| zzzRevCqRuddyman | 3B1B6D | Memory of the Deep Sea | Ruddy Man moves from Pailune, to Church, to Disposal Field, to Yelem's Library ×2. | 40 = vision scene. 50 = goes mad. **65 = scene, barrier, fast travel off.** 70 = fight. 80 = Parasite. | **90**. |
| zzzRevCqScab | 35AF3D | Stigmata Necrosis | Free Scab from his cage; he moves from Church, to Worm-Eaten Port, to the Lullaby Room. | 40 = madness scene ("Get out of my head"). 50 = only remains. 60 = his talking remains at the Church. | **70**. Journal: Scab "fell silent". |
| zzzRevCqMothMan | 579C46 | Song of Fjyron | Free Sister Gaga; she moves from the Castle rest room, to Church, to Prophet's Cave (canticle tree). | 45 = accept or refuse the cocoon (12-hour limit). 100 = deliver to the northern altar (time breach). 110 = breach closed. 120 = Gaga found dead and Apostle of Landfall scene. 130 = fight. | **140** (good end). **220** and **310** are bad ends. |
| zzzRevCqLeaper | 5872E4 | Words of Worlding | Apka-Lul's 7 talks; he moves from the Dragon Lair, to Upper Yelem, to the Altar of Twilight (Alduin's cave). Feed Leaping Pocket Munduses to Alduin's dregs. | 150 = give 3. 180 = give 6 (opens Nymic Surgery). 220 = loses sanity. 230 = mercy kill or leave. **240 = boss scene, fast travel off.** 250 = fight. 260 = ash. 270 = eat or discard the Worm of Alduin. | **300** (eat), **400** (discard), **900** (bad end). |
| zzzRevCqLeaperSurgey | 58DF4C | Nymic Surgery | Face-sculpt service with Mehrunes' Razor or a Ja'Khajiit Fang. | Words of Worlding stage 180. | **10**. Stopped at stage 100 by Leaper stage 220. |
| zzzRevCqDragon01 | 343B60 | Farewell Gift | Aushahlaas asks the player to put down Briiviingrein. | 20 = fight. 30 = report. 40 = take the sword in the Kanra village. | **50**. |
| zzzRevCqAhzidal | 38F17D | Ahzidal's Remains | Talk to the dying Ahzidal: lie that Saarthal's people escaped, or tell the truth. | Started at stage 100 of zzzRevBossQuestAhzidal (or re-checked at Lost Storyteller stage 20). | **20**. |

### Bosses
| EditorID | FormID | Name | Boss (UA) | Notes |
|---|---|---|---|---|
| zzzRevBossQuest01 | 1F73CC | Lycanthropy 01 | Beast-Possessed Hunter 1F73C5 | A musketeer turns into a beast. Done at 20, which starts BQ02. |
| zzzRevBossQuest02 | 1F73E6 | Lycanthropy 02 | Spawn of Hircine 1D321C | Follow shaman Zan'zar (2033CC). Done at 40, which starts BQ03. |
| zzzRevBossQuest03 | 30EF7D | Moonlit Hunt | Beast of Hircine 1C7388, then Zan'zar | 60 = visit the church. 70 = talk to Boltzmer. Done at **80** (key to Pailune). |
| zzzRevBossQuest04 | 33DEE3 | Mark of the Hunter | 2 Sacred Beasts, then Champion of Hircine 33DEDA | Survivor Morris the Immortal (36C5CC). Done at **60** ("Break the Seal of Hircine"). |
| zzzRevBossQuest05 | 36C620 | Undead Beast | Undead Beast Jaeva 1CD301 | Done at 30. |
| zzzRevBossQuestAhzidal | 38F141 | Ahzidal | Remembrance of Ahzidal ×2, then Ahzidal of Chaos 389471 | Curses the Snow Elves. Done at **50**; 100 starts Ahzidal's Remains. |
| zzzRevBossQuestAradia | 343BA7 | Shadow of Aradia | 3 Shadows of Aradia, then Radiance of Lyg 0D0440 | Namira's tower. Done at **40** (or 100). |
| zzzRevBossQuestAssassin | 360BC6 | Assassin | Assassin Chief Byron 360BC3 | Boltzmer's trap; kills Robin. Done at 20 or 30. |
| zzzRevBossQuestDagoth | 3CE9E4 | Will of Dagoth | Remnant of Dagoth Ur, then Beast of Dagoth | Ravine of the Old Serpent. Done at **30**. |
| zzzRevBossQuestLyg | 37DBA1 | Lyg Caller | Priestess of Mor-Galg 2DA66A | Done at 20. |
| zzzRevBossQuestPuppet | 366989 | Puppet | 2 puppets, then the Puppeteer 2E034B | Done at 40 or 50. |

### Daedric artifact / cat quests
| EditorID | FormID | Name | Summary | Completes |
|---|---|---|---|---|
| zzzRevDA01 | 176373 | Clavicus Vile | Find Barbas, bring him to Vile, then get one question answered. | 40 or 50 (Vile and Barbas banished). 999 = skip. |
| zzzRevDAAzura | 355287 | Azura | The Azura cat's prophecy; the player gets her weapon. | **10**. |
| zzzRevDANamira | 355274 | To Fishing Village | Finish Namira's rite and she opens the gate to the west. | **10**. |
| zzzRevCircusIntro | 33DF1A | Sanguine Circus | The Blood Cat invites the player and gives the Circus Key. | **10** (starts the circus manager). |

### Misc
| EditorID | FormID | Name | Summary | Completes |
|---|---|---|---|---|
| zzzRevMisc01 | 0160BA | Zealot of Meridia | Malmanius gives the player a "sun" weapon to convert people. | 20. 255 = he dies. |
| zzzRevMisc02 | 016143 | Musketeer's Hope | Wilmer's request; sets the 5 citizen quests to stage 1. | 10. |
| zzzRevCqCitizen01-05 | 016144 / 016172 / 01619B / 0161C6 / 0161F1 | The Pawnbroker / Alchemist / Innkeeper / Charlatan / Blacksmith | Talk each into moving to the Square. | 30 / 20 / 20 / 30 / 20. 255 = fail (the NPC dies). |
| zzzRevMisc03 | 016235 | Legless Friends | Cilla the slug's four friends (Asmo, Sanna, Heikki, Urmas). | 70 (after objective 60, "Report to Cilla"). |
| zzzRevMisc04 | 37226B | Je'm'ath Brandy | The mayor's moon-sugar brandy for Wilmer. | 30. |
| zzzRevMisc05 | 383800 | Ahzidal's Ladder | Activate 3 Ahzidal runes. | 40. |
| zzzRevMisc06 | 54ACC6 | One-Finger | Praise 5 One-Finger shrines; reward is a shield. | 100 (starts Pale Cheese). |

### Radiant / manager / generic quests (grouped)
- **Repeatable hunts** (all end at 10 or 20; 999 is shut-down):
  - zzzRevRq01A Child Beast 3DA23B
  - Rq01B Musketeer Hunt 3DA244
  - Rq01C Rioter Hunt 3DA258
  - Rq01D Herma Cat 3DA260
  - Rq01E Pale Sack 3DFE17
  - Rq01F Infected Hunt 3E59B9
  - Rq02A Beast Citizen 3E59D4
  - Rq02B Boss Beast 3E59EC
  - Rq02C Worshippers of Hircine 3E59FE
  - Rq02D Outlander 3E5A03
  - RqAtatami 3F1171
  - RqDragon 3EB5E6
  - RqMiniBoss "Kalpic Traveler" 5A8BC8
  - RqScab "Radiance" 3EB596
- **Bloody Circus arena rounds** (5 rounds each; done at 100): zzzRevSCq01 Meat 3F6D3A, zzzRevScq02 Bone 3F6DA7, zzzRevSCq03 Scraps 3F6DB2. Manager: zzzRevSCqMain 3F6D36.
- **Generic dialogue:** zzzRevGen 0160D6, GenAdoringFan 5F2B95 (an Adoring Fan enemy: "By Azura!"), GenAzura 355295, GenHamah 017137, GenHircine 33DEF1, GenNamira 3497FA, GenSanguine 33DF2F, GenSkoomaCat 1807C3.
- **System quests:** zzzRevMCM 015111, zzzRevSafety 015110 (version check), zzzRevqJsonManager 46F321 (cross-playthrough "dejavu" flags), zzzRevqKeyItem 123349 (hands over and takes back Lalanoah's remains, the Red Drop, the Elder Seed and the Fetus).

---

## 3. "Banter must be silent" moments

| Quest | Stages | What happens |
|---|---|---|
| Departure 171135 | **20 to 30** | Fade. Forced first person. Player controls disabled (movement, combat, sneak, camera switch, journal). Cart HUD. Player and Black Owl seated on the boat (`SetVehicle`). Forced sail scene ScSail; the Owl's monologue plays during it. Stage 30: fade, then the player is teleported to the exit marker (`PlayerRef.MoveTo`) into the Black Spring (Svartibrunnr), then a WIP message box. |
| Desiccated Embryo 01710D | **10 to 20** | Forced first person. All controls disabled. Knockdown idle. ~7 s wait, then a long fade to black (about 14 s total), then a get-up idle. Controls come back at stage 20. Silence for about 20 s. |
| Feast of Love 60026B | **10 to 50** (scenes at 10 and 30) | Boltzmer's verdict scene (Sc01) and the transformation scene (ScTrans, stages 30-38). Fast travel is locked until 50. Keep quiet through the Boltzmer and Yelem speeches; combat barks only. |
| Sacrament of Cat 51525D | **20 to 130** in Dreamsleeve (491B1B). Scenes at 25-75, **110-118** (D4C portal, white-out), 150 (head on the altar), 200-207 (Torvesard summoned), 300/400/600 (endings). | Dream world. Ja'zel's monologues play as forced scenes at each of 6 stops. Fast travel off from 110 to 130 and from 400 to 500. |
| Baby of Nightmares 34980C | **20 to 30** | Athanasius's monologue (Sc01). Barrier up, no fast travel. Then the Rite of Cannibalism (3ABF2B, stages 0-60): fog and the player's own "echoes". |
| The Lost Storyteller 5F2B94 | 30 (Sc01), 45.1 (white-out), 60 (ScSeal), **80 (Hamah's Snow Elf story)**, **90 (coffin, "To be Continued" message box)** | Keep quiet while Hamah tells her story. |
| Strange Fruit 015B58 | 37 | King scene (KingSc); Ja'i chants in Ta'agra. |
| Moonlit Hunt / Mark of the Hunter / Lycanthropy 02 | BQ03 20 and 60; BQ04 10 and 30; BQ02 10 | Shaman and Chick Trader speeches. |
| Words of Worlding 5872E4 | 50, 90, 130, 160, 190, 240 | Apka-Lul's monologues. Boss scene at 240. |
| Stray Cat 3D45DE | 85 | Mar-Dro's truth scene on the Void Ship. |
| Memory of the Deep Sea 3B1B6D | 40, 65 | The vision, then the madness. |
| Stigmata Necrosis 35AF3D | 40 | Scab's breakdown. |
| Snow Cat 360BD2 | 30, 40, 70 | Aisha's scenes, then her vanishing. |
| Song of Fjyron 579C46 | 120 | Apostle of Landfall scene. |
| Pale Cheese 5D7AD9 | 30, 100, 200, 300 | Sheogorath double-act scenes. |
| Clavicus Vile 176373 | 50 | Farewell banter between Vile and Barbas. |

**Worldspaces**
- **Svartibrunnr** (000D62) is the whole act, from Departure stage 30 onward.
- **Dreamsleeve** (491B1B) is used only by Sacrament of Cat, stage 20 onward. Its places include Ja'zel's Neural Pathway, Memospore Server, SHARMAT Quarantine Zone, Soul Purgatory and the Throne of the Soul Matron.
- **Not used by any Rev quest, as far as I can tell (unsure):**
  - Sanctuary of Namira (009598) belongs to the earlier GH act. This act's Namira content is "Namirapolis", inside Svartibrunnr.
  - The Great Hole of Hinnom (00EF8C) belongs to Act 3 (LaM).
  - The Milky Sea "???" (0109CC) belongs to GH.
- **Falmereth** is only promised. It is not built yet.

---

## 4. Followers

- **No Rev script dismisses, moves, blocks or checks followers.** A search of glen_story.txt and all Rev source scripts for Follower, Teammate, PlayerFollowerFaction, CurrentFollowerFaction, Dismiss and SetPlayerTeammate finds only two hits. Both are `IsPlayerTeammate()` checks:
  - `RevTrapCanonShotScript`: teammates can set off cannon traps.
  - `RevAbCallStandoEffectScript`: hits from teammates count, like the player's, for a boss "stand" effect.
- **The Departure boat is the main problem.**
  - Only the player and the Black Owl are seated. The boat moves with `TranslateToRef`.
  - Followers are left on the dock. They only come back if the engine pulls them to the player after the final `PlayerRef.MoveTo(SafeWarp)` at stage 30.
  - Whether they appear in Svartibrunnr on their own is unsure. Plan for "followers arrive late or not at all".
- **Other places followers probably cannot follow (unsure):**
  - Dreamsleeve, through the "Ja'zel" door at Sacrament of Cat stage 20. It is a door, so followers likely do follow, but the setting is the player's own mind.
  - Hamah's coffin into Falmereth (Lost Storyteller stage 90). Not built in v0.96.
  - Boss arenas with `BarrierRef` / `BossBarrier` (Feast of Love, Sacrament of Cat, Baby of Nightmares, Ruddy Man, Aradia, Dagoth, Puppet, Song of Fjyron). Followers already inside fight; followers outside are shut out.
  - The transfusion knockdown in Desiccated Embryo is player-only.
- **Fast travel is turned off** during most boss stages (listed in section 3). Followers walk with the player then.
- **Several story NPCs walk alongside for a moment.** Mar-Dro, Aisha, Robin, Ruddy Man, Scab and Sister Gaga each say "Follow <Alias>", but they are not teammates. They are moved ahead between meetings with `TryToMoveTo`.

---

## 5. Banter hooks (quest + stage)

1. **Departure 171135, stage 0-10:** before boarding. "Are we really getting on a boat with *him*?" Doubts about the Black Owl after he admits the witch hunt was a lure.
2. **Departure, stage 30:** arrival in the Black Spring. Endless night, black sludge, a Blue Star that will not set.
3. **Musketeer's Hope / citizen quests (016143, 016144-0161F1), stage 10 to complete:** escorting townsfolk. The Charlatan who is "not even a healer". Roland's "second blacksmith store".
4. **Moonlit Hunt 30EF7D, stage 70:** Boltzmer's welcome, "I just like your name". Followers find him creepy. Robin later says he blew his own head off.
5. **Desiccated Embryo 01710D, stage 20+:** the player now hears Hamah's voice. "Who are you talking to?" A jealous or worried follower. Hamah-versus-follower snark. Ja'zel's phantom warns against "taking her as your companion".
6. **Strange Fruit 015B58, stage 10/15:** the Prince-or-Clerk assassination choice. Debate it.
7. **Communion: Ja'bal 48BF99, stage 10 or 100:** "You *ate* that?" against the blue-ember burning.
8. **Snow Cat 360BD2, stage 30:** "You're such a bitch." / "You finally noticed?" Followers react to Aisha. Stage 80 is a quiet goodbye.
9. **Stray Cat 3D45DE, stages 15-75:** Mar-Dro chatter and his son's name, "Ja'zeri". **Stage 90 is the reveal: he is Ja'zel's father.** The heaviest beat of the act.
10. **Sacrament of Cat 51525D, stage 130:** after killing Ja'zel again. **Stage 210:** Torvesard names Vaermina and Hermaeus Mora, a strong hook for Daedra-aware followers. **Stage 230 or 600:** the devour-or-forge choice.
11. **Jazel Phantom 572FEC, stage 0+:** Ja'zel's ghost talking to the player in town. Followers cannot see him (unsure, but implied: "you only see what you wish to see").
12. **Baby of Nightmares 34980C, stage 40:** the player now carries a monstrous baby. "It looks a bit like you" (Hamah).
13. **Stigmata Necrosis 35AF3D, stage 10 and 60:** Scab's language. Then his talking remains.
14. **Song of Fjyron 579C46, stage 30:** the shy giant moth and "talking crabs" (the Ruddy Man). Stage 120: Sister Gaga found dead. Sad banter.
15. **Words of Worlding 5872E4, stages 20-110:** a philosophical Ruinach on names and free will. Good for scholarly followers. Stage 270: eat Alduin's worm or not.
16. **Farewell Gift 343B60, stage 30-40:** a dragon's gratitude. "Joor."
17. **Pale Cheese 5D7AD9, stage 10 and 120:** two Sheogoraths, and "Is that cheese safe to eat?". Light comic relief.
18. **Clavicus Vile 176373, stage 30:** "If you mention his name, he'll show up." Followers should *not* say "Hermaeus Mora".
19. **The Daedric cats, any time:**
    - Azurah: "May I pet you?" / "Know your place."
    - Hircine remembers Vahdin Holt.
    - The Mouth of Namiira's "my disciple".
20. **The Lost Storyteller 5F2B94, stage 45/46 and 50:** Hamah unmasked looks exactly like Lalanoah. Then the coffin invitation. A follower reacts to "Fine, mom."
21. **Feast of Love 60026B, stage 50:** after Yelem: "The experiment was a success...?" What did we just help happen?
22. **Hidden scores** (Humanhood / Beasthood / Mnemoli): a running hook about how "rotten" the player smells. Many NPCs comment that the player stinks of decay.
