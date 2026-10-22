# VAL SERANO — character sheet (for the follower-banter mod)

Sources read (read-only): `AX ValSerano.esp` (all 5,408 dialogue lines dumped and sampled across every quest), quest records and decompiled quest scripts from `AX ValSerano.bsa`, and Remiel's `HLIORemi.esp` (the full HLIOValBanter quest: 32 scenes, 301 lines, and the scripts that fill its aliases). Where something is my inference rather than something the files say, it is marked *(inferred)* or *(unsure)*.

---

## 1. Who he is

**Name.** Val Serano. His full name is **Valerius** and he hates it ("Please for the love of the Nine do not call me that name."). Remi guesses "Valentino" in the banter. When pushed he calls himself a "relic hunter", not a pirate.

**Race / what he is: half-Nord, half-Dunmer.** This is why he doesn't know how long he'll live.
- His NPC record uses the **Nord** race, and he looks and passes as a Nord. He says himself, "people tend to have certain expectations of me since I'm a Nord."
- His father **Tarek Serano is a Dunmer** (the record uses DarkElfRace). Val: "My father was a Dunmer, and he raised me as one."
- His mother **Elin is a Nord** (the record uses NordRace). She translates books for academics in the Imperial City.
- So he has an elf parent and a human parent. In Remi's banter he says: *"Over thirty doesn't seem that old, does it? I'm not entirely sure how long my lifespan is, now that I think on it..."* Mer can live for centuries. Nothing in the files says whether he ages like a Nord or a Dunmer, so he doesn't know either *(the link to his mixed parentage is inferred, but it is the only explanation the data supports)*.
- Other half-elf hints: he was raised in the Dunmer New Temple faith. Azura, Boethiah and Mephala are his gods, and "By Mephala" is one of his oaths. He wonders whether the Ashlander Wise Women would see him as an Outlander. His grandparents supposedly served House Indoril.

**Age.** Just over thirty *(inferred)*. He was about 18 and First Mate during the corsair raid on Wayrest "back in one eighty-eight" (Remi's Corsairs scene), and he says he's "over thirty".

**Origin.**
- He was born at sea and doesn't know exactly where: "My mother always said that must be why I couldn't wait to get back."
- He grew up in the Imperial City with only his mother. His father was away, because his mother had left Tarek. She told him romantic stories about his father, and that backfired: he ran away to join Tarek's crew.
- He dropped out of school as a boy and taught himself afterwards. He reads a lot ("I read too many stories as a kid").

**Family.**
- **Tarek Serano** (father, Dunmer pirate captain, born in Windhelm). Ruthless and manipulative. He set his sons against each other and "made him what he is". Val spent his life trying to win his approval. Tarek was behind the mutiny that marooned Val, sent the Morag Tong after him, and later kidnapped him (see the key events below). The player decides whether Tarek lives or dies; the globals are `AX_TarekAlive` / `AX_TarekDead`.
- **Elin** (mother, Nord, follows Mara). They are close but she lectures him. Every birthday she sends him strawberry danishes, which are his favourite food and which he refuses to share (from the "Val Fact" jokes).
- **Fathis Indaryn** (Dunmer, his half-brother through different mothers; Tarek never acknowledged him). They grew up together on the ship and were best friends, then rivals. Fathis was Val's First Mate for about 20 years, betrayed him (the mutiny), and died in Solitude when Val stabbed him in self-defence. Fathis's soul was then trapped by a Molag Bal relic. Val bargains with Hermaeus Mora to save him, Fathis is resurrected and reconciles with Val, and Val gives him the Dark Rose. He calls Val a "snowback pretty boy".
- **Ravani** (an orphaned Dunmer girl from the Windhelm market). Val and the player can adopt her in Val00D "Wing and Wing".

**Ship and crew.**
- **The Dark Rose**: his father's ship, taken over by Val around age 20. After the reconciliation it is captained by Fathis.
- **The Spring Rain**: a small boat with blue sails that the player can buy him as a gift (Val006 "Safe Harbor"). His home anchorage is Safe Harbor.
- Later he talks about "my growing fleet. To my captains, Fathis and Velehk!" (Velehk Sain).
- His horse is **Windward** (a blue roan). The **Cheesy Pirate Hat** is a talking Dremora hat that tells "Val Facts".
- The crew were "corsairs and cutthroats". He served a year in the **Imperial Navy** (deckhand, then bosun on the *Bendu Olo*) after Tarek abandoned him in port at 15 for being a "pain in the ass".

**Key quest events, in order.**
1. **Val001 "Between the Daedra and the Deep Blue Sea".** The player finds him marooned on an island, bearded and half-starved, after the mutiny. Auryen Morellus (Dragonborn Gallery) is his buyer for the *Star of Solitude*.
2. **Val002 "He Runs a Tight Shipwreck".** He admits he stole the Star from a draugr tomb. He sweet-talks Captain Aldis and has a forgery made. Then the trust talk: "Honesty doesn't come easily to me."
3. **Val003 "But You Have Heard of Me".** Morag Tong assassins come after him. It turns out Tarek planned the mutiny. Val confronts his father, who lives or dies by the player's choice. "Sticking with you has been the first good decision I've made in a long time."
4. **Val004 "Stand by Me".** Optional "get to know him" topics: journal, faith, houses, jobs, Fathis's death ("I killed my brother..."), magic, clothes.
5. **Val005 / Val005SB "Drink and the Daedra…" / "Sailor's Bargain".** Fathis's journal leads to Molag Bal cultists and soul-gem fragments holding Fathis's soul. Val reads a Black Book and walks through **Apocrypha built from his own memories**. He "used to serve Hermaeus Mora" and once burned Mora's books to spite him; Mora's "gift" means he always knows when he is lying to himself. He confronts his first kill: a merchant captain's son of about 13, when Val was the same age. Fathis is saved and the brothers reconcile.
6. **College line (ValCOL, ValCOLGrad).** He enrols at the College of Winterhold despite himself, graduates, and is later offered a teaching post. He is a self-taught storm and lightning mage (Ball Lightning "Sparky", a Storm Golem) and "hopeless at Alteration".
7. **Thieves Guild, Legacy of the Dragonborn (Explorers Society), Creation Club, and Saints and Seducers add-on quests**, plus hundreds of location and quest comments.
8. **Romance: Val00A, then Val00B, then Val00C (wedding), then Val00D (children / Ravani).** See section 3.

**What he wants.** Freedom, the open sea and adventure, but without the killing. He wants to be a better man than his father ("I'm not that guy. But I'm trying to be."). He wants to belong somewhere: with the player, the Explorers, the College. He wants to be loved for himself.

**What he fears.**
- Being abandoned or dying alone in the dark. He was marooned, and in Val00B Mora whispered that he'd "die alone down here".
- Turning into Tarek, and being a bad father (Val00D).
- Hermaeus Mora calling in his favour ("he'll call in that favor eventually").
- Dragging the player into his trouble ("happy moments don't change the kind of trouble I bring").
- As running jokes: chaurus, the Falmer, hats, and losing his pants.

**What he values.**
- His own moral code: "No murder. No torture. No harm to noncombatants." He never dealt in slaves or animal fighting rings, and he despises senseless cruelty.
- Loyalty, because he has been betrayed so often.
- Competence and cleverness. He respects Remi's brilliance.
- Knowledge and history ("the only difference between tomb robbing and archaeology is writing it down").
- Choice ("There is always a choice." "Everyone has a choice.").

---

## 2. How he talks

**Tone.** Wry, flirtatious and self-mocking. He is quick with a comeback and deflects with humour, then drops into sudden quiet honesty when something real is at stake. Smooth when he's working a mark; blunt and profane under stress. He laughs a lot ("Ha ha ha!", "heh heh").

**Sentence length.** Mostly short to medium. Quips are one line. When he opens up, he speaks in two to four longer sentences full of hesitations ("I- I...", "ahem", "uh", "(sigh)"). He drops g's ("lookin'", "freezin'", "y'know", "somethin'").

**Swearing and oaths.**
- Dunmer and sailor flavour: "By Mephala", "by Azura", "Azura bless you", "for the love of Azura", "Kynareth save me", "Praise Kynareth", "Daedra take you", "What in Dagon's name", "I'll see him in Oblivion", "a cold day in Oblivion".
- Insults: "s'wit", "fetcher", "n'wah", "Filthy n'wah".
- Real swearing: "Godsdamnit", "shit", "son of a bitch", "ass", and one "fucking" (the chaurus-hatchling line).

**Pet names for the player.**
- Romanced: "love" (the main one; the quest log notes "Val calls me 'love'"), "darling", "gorgeous", "beautiful" / "handsome", "princess" (teasing), "my better half".
- Friendship: "my friend", "partner", "hero", "college boy/gal". He also says the player's first name when it matches one of the ~23 names voiced in the mod (Aelyn, Alannah, Aris, Bree, Cyr, Dahlia, Elise, Luna, Rathas, ...).
- Remi: "my new friend", "my friend", "favourite business partner".

**Catchphrases.**
- "As you wish, love."
- "Fair winds and following seas."
- "We'll be wing and wing."
- "Watch and learn, my friend."
- "I'll owe you one."
- "I'm only leaving so you'll miss me."
- "I'm alive and I'm free, so it's a start." (Fathis says Val always used to say this.)
- "Chart your course with me."
- "the only difference between tomb robbing and archaeology is writing it down"
- "If you can't dazzle them with brilliance, confound them with bullshit."
- "The tide and good weather wait for no one."

**Recurring jokes and bits.**
- Steals and hoards **sweetrolls** (and gets his own stolen by Remi).
- Desperate for **coffee** ("I'd literally kill for a coffee").
- Keeps finding **chaurus eggs** in his pockets.
- **Hates hats and helmets** ("They mess up my hair"); vain about his hair (the Hat: "It takes him hours to get those 'effortless' beachy waves").
- Loses his **pants** (Val00E scavenger hunt for his clothes).
- Calls Riekling "blue vermin" / "blue goblins".
- Insists he's a "relic hunter, not a pirate".
- Hates the name Valerius.
- Not a morning person ("I'll rise, but I won't shine").
- Sailor weather sayings.

**What he teases about.** The player's armour and outfits (flirty), the player's ego, the Dragonborn fame ("the Dragonborn and... dubious pirate friend"), Remi's absent-mindedness, mages and the College, the Imperial Legion, Nords and Nord pride.

**What makes him soft.**
- Being given thoughtful gifts: a ship in a bottle, the Spring Rain ("I never imagined that anyone would understand me so well").
- Someone coming back for him ("you came for me! I knew you would").
- Fathis, kids (Ravani), Scrap the spider.
- Being told he's good enough.
- Morning-after breakfasts ("I've never made anyone breakfast before").
- Starlight and the open water.

**Representative lines (verbatim).**

*Charming / flirty*
- "Darling, a chance is all I ever needed."
- "I never said I was everyone's cup of tea... but I could be your shot of whiskey."
- "Ah, you're lucky you're cute. Give me that key."
- "You adore me. I'm a delight!"
- "Oh come on, you keep me around because I'm fun. You'd be hopelessly bored without me."
- "Cheers to us! The Dragonborn and the dashing pirate- I mean relic hunter."

*Wry / roguish*
- "If you can't dazzle them with brilliance, confound them with bullshit."
- "Well it's not stealing if the things don't have an owner."
- "Hey, on my honor, the next time I'm gonna break the law, I will let you maintain plausible deniability."
- "These bandits are just pirates who can't sail. Worthless."
- "You know where to find me- NO, not the Solitude jail."
- "Well... I wouldn't *kill* anyone to rob a city now. I have standards." (Remi banter)

*Idle / sailor*
- "There's an old sailor's saying: if you don't like the weather, just wait a minute."
- "I love looking at the stars. They're as beautiful in Skyrim as they are at sea."
- "Not that the sunrise isn't beautiful (yawn) but I'm more of a sunset kind of guy."
- "I'll rise, but I won't shine."
- "Chaurus... why did it have to be chaurus?"

*Combat*
- "Enemy closing!"
- "Die, you ankle-biting blue vermin!"
- "I'll sell you for parts!"
- "I'm only mostly dead... still slightly alive."
- "To the victor goes the spoils."
- "Well, that wasn't a complete disaster."

*Vulnerable / honest*
- "Honesty doesn't come easily to me."
- "I knew better. I just... hoped differently."
- "I've been trying to please him my whole damn life."
- "I've had to hide who I am for so long, I'm not sure I trust who's in there anymore."
- "Tomorrow is never guaranteed to anyone. That doesn't make today any less beautiful."
- "I killed my brother..."

*Love (romance)*
- "I can't give you what's already been stolen. You know, you made off with my heart a while ago, love."
- "Then chart your course with me, and you'll never feel the cold at night."
- "I used to love being at sea, but your hands in my hair feel better than the wind."
- "Hermaeus Mora was whispering in my head that I was going to die alone down here. But I was never alone, because I have you."

*Angry*
- "Well Daedra take you, then!"
- "A favor?! You left me to die!"
- "Godsdamnit! You think so little of me?"

---

## 3. Romance with the player

**Main quest: Val00A "Romancing the Rogue", `3AA4A5:AX ValSerano.esp`.** Its scripts are `AX_V_QF_Val00A_053AA4A5` and `AX_Val00AFunctionsScript`.

| Stage | What it means |
|---|---|
| 0 | Startup |
| 5 / 6 / 7 | The Pale Lady date. 5 = go to Frostmere Crypt, 6 = talk after the crypt, 7 = Lake Ilinalta date (starts `Val00ALakeDate`) |
| 10 | Wear an Amulet of Dibella in the evening to get his attention |
| **20 / 30 / 40** | The morning-after reaction sets the **tone track**. 20 = **Mild** (he got the wrong idea; sets `AX_Mild`=1), 30 = **Hot** (spent the night; sets `AX_Hot`=1), 40 = **Spicy** (player calls him an arrogant ass; sets `AX_Spicy`=1) |
| 22 / 32 / 42 | Whiterun market outing (the Nazeem prank scene), one per track |
| 24 / 34 / 44 | "Ask Val about past loves", one per track |
| 26 / 36 / 46 | "What about us?": wear an Amulet of Mara |
| **199** | Just friends. Sets `AX_FriendZone`=1 and `AX_EarlyFlirt`=0, starts Val00E |
| **200 / 300 / 400** | "Chart our course together" = **in love**. Sets `AX_Love`=1 and starts Val00B |
| 201 / 301 / 401 | "Rough waters": he loves the player but it isn't returned. Starts Val00B without setting `AX_Love` |

**Globals** (all from `AX ValSerano.esp`):
- `AX_Love` `577EB8` = 1 means lovers. **This is the key global for "romanced".** `AX_ValController` also raises his relationship rank to the player to 4 when it is set (3 otherwise).
- `AX_FriendZone` `4D5987`, `AX_EarlyFlirt` `ABA285`, `AX_Mild` `3E2152`, `AX_Hot` `3E2153`, `AX_Spicy` `3E2154`.
- `AX_ValEngaged` `A2205B`, `AX_ValMarried` `A22094`.
- Flirt tracking: `AX_FlirtGlances` `5CE233`, `AX_FlirtTouch` `5CE234`.
- Options: `AX_KissEnabled` `47D308`, `AX_HugsEnabled` `463CD8`.

**Faction.** No dedicated romance faction. The factions are `AX_ValFaction` `3DD028` ("What's Mine Is Yours", rank 0, item sharing), `AX_ValRecruitedFaction` `E0938C`, `AX_ValAllyFaction` `9B4486` and `AX_ValEnemyFaction` `B6EE39`.

**Follow-on quests.**
- **Val00B "Wicked Game"** `49DC33`. Val vanishes from Safe Harbor. Tarek and Jena Avarix (now Hermaeus Mora's thrall) throw him into the Sightless Pit, unarmed and with his hand broken. Stage 200 = rescued and together; 201/211 = he loved the player, it wasn't returned, they stay friends (the heartbreak scene: "Do you feel nothing for me?").
- **Val00C "Making an Honest Man of Him"** `9B2444`. Proposal and wedding, held on the Dark Rose (stage 200) or at the Temple of Mara (201). Stage 202 = the player declines marriage but they stay committed.
- **Val00D "Wing and Wing"** `49DC34`. Talking about children; he fears he'd be a bad father. Stage 90/200 = they adopt Ravani; 199 = no kids.
- **Date quests:** `Val00ALakeDate` D73448 "Hidden Depths", `Val00ASpringsDate` E80A0E "If You Can't Take the Heat", `Val00AViewDate` B7B6D5 "Take in the View".
- **Val00E "Several Nights to Remember"** `22FFC1`: the scavenger hunt for his lost clothes.

**Jealousy and rival reactions.** There is **no jealousy mechanic** and he makes no rival reactions to other followers. The closest material:
- Joking about "a small army of rival suitors" and "We don't have to be rivals. There's plenty of me to go around!"
- The player can tease him with "Is that jealousy, Captain?"
- To Vex: "Is that jealousy I hear? I thought you weren't interested."

He is open and secure rather than possessive. Before the player he was a serial non-committer ("It was always easier to sail away").

---

## 4. Opinions of other followers

- **Remiel (Remi)**, in both mods. Affectionate big-brother and business partner.
  - In Remi's banter: he respects her brilliance ("You're brilliant. Don't let anyone tell you otherwise."), teases her for being absent-minded, and starts a junk-flipping business and a pickpocket partnership with her.
  - He is uneasy that she ordered the Morvic killing ("I'm not a killer for hire"), but he forgives her.
  - He grows fond of Scrap.
  - In Val's own mod (driven by `AX_FollowerRemi`): "Is it just my imagination, or is Remi freakishly strong?" and "Keep an eye on Remi... I'm not sure she can hold her mead." Remi also shows up at his rescue (scene `RemiValMeetA`, gated on `AX_RemiMetVal`) and asks "So... Are you a murderer?"
- **Inigo**: one line, driven by `AX_FollowerInigo` `B5FA59`: "I never met a blue Khajiit before. At least the fur blends in with my clothes."
- **Lucien**: no direct line. The Cheesy Hat's "Val Fact" says Val stole **Lucien Flavius's** lunch money every day for a year as a schoolboy (both grew up in the Imperial City). Val's script also detects Lucien (`AX_FollowerLucien` `455071`).
- **Kaidan, Flint**: Val's script detects them (`AX_FollowerKaidan` `B88534`, `AX_FollowerFlint` `B88535`), but **no dialogue uses those globals**. He has no opinion of them on record.
- **Gore, Xelzaz**: nothing in either mod. Remi's mod tracks both, but not with Val.
- Implied attitudes *(inferred, for writing)*:
  - Mages: mixed. He was "prepared to hate" the College but came to like it.
  - Nords and Legion types: wry. "It smells like Imperial Legion in here."
  - Dunmer: warm. "The Dunmer here might take a while to warm up to you, but it's worth the effort."
  - Self-righteous types: needling. "Pht. How very 'Nord.'"
  - The Daedra: respectful but wary.

---

## 5. Existing cross-follower banter (how it is built; copy this)

### A. Remiel's `HLIORemi.esp`: HLIOValBanter `9BA4FD:HLIORemi.esp`

- **Quest.** Start Game Enabled, Run Once, priority 55. It has **no quest script**. Stage 10 = intro scene done. Its quest-level dialogue condition is `HLIOScrapAttackMode == 0`.
- **Aliases.**
  - 0 `Remi`: a forced reference to Remi's placed ref `033226:HLIORemi.esp`.
  - 1 `Val`: **empty and optional**. Its alias package list is `HLIOValForceGreet` `A2EED8`, a ForceGreet template that opens the Morvic topic. It only runs while Val is in `CurrentFollowerFaction`, within 1000 units of Remi, and `HLIOMQ1` is at stage 150.
  - 2 `Scrap`: a forced reference to `885448:HLIORemi.esp`.
- **How the Val alias gets filled.** Through quest `HLIOModChecker` `2B1B38:HLIORemi.esp`. Its player alias runs `HLIOModCheckerScript` (and `HLIOBackupChecker`) on `OnInit` and `OnPlayerLoadGame`:
  ```papyrus
  Function ModCheck(ReferenceAlias FollowerAlias, int FormID, string FileName)
      if FollowerAlias.getref() == None
          if game.GetFormFromFile(FormID, FileName)
              FollowerAlias.ForceRefTo(game.GetFormFromFile(FormID, FileName) as objectreference)
  ...
  ModCheck(ValRef, 499813, "AX ValSerano.esp")   ; 499813 = 0x07A065 = AX_ValSeranoREF
  ```
  This is a soft dependency: there is no master on Val's plugin, and the alias is just optional. `HLIOBackupChecker` also re-forces Remi into `RemiValRef` and Scrap into `ScrapValRef`.
- **Trigger.** A **Misc / Idle topic**, `HLIOValBanterIdles` `9BA4FE` (priority 50), with 29 opener lines. Each opener carries the shared gate below plus its own extras:
  - `GetRandomPercent < 1` and `< 30` *(houseCARL showed both conditions with flags 0; it is probably an OR pair, so I'm unsure of the exact odds)*.
  - `IsInDialogueWithPlayer == 0` and `IsInScene == 0`, checked on both aliases.
  - Val within 1000 units of Remi.
  - `GetPlayerTeammate == 1` on the Val alias, and Remi in `CurrentFollowerFaction`. **This pair is the "both following" check.**
  - `GetIsAliasRef(0 or 1)` on the subject, which decides who speaks the opener.
  - `IsSneaking == 0`.
  - `HLIOValTalkedAboutMorvic != 1`.

  Most openers have **Reset Hours 24**, so each repeats at most once a day.

  The opener INFO's **OnEnd fragment** (`HLIO_TIF__05xxxxxx`, with a `Scene` property) calls `Scene.Start()`. The scene then plays through phases, with each Dialog action naming the alias as ActorID 0 = Remi, 1 = Val, 2 = Scrap.
- **Progression globals** (HLIORemi.esp):
  - `HLIOValRemiFriendshipTracker` `9D3C40` (0 to 4; the scenes gate on 1, 2, 3, 4).
  - `HLIOValShopSceneDone` `9BA522`, `HLIOValFirstProfitDone` `9D8D47`, `HLIOValLikesScrap` `9D8D43`, `HLIOValWayrestDone` `9D8D44`, `HLIOValTalkedAboutMorvic` `9D8D45`, `HLIOValPickpocket` `9D3C42`.
  - Remi's main quests are `HLIOStartingQuest` `0E4852` and `HLIOMQ1` `46FA55`.
- Hello/Goodbye topics also add **player-directed lines about each other**: `HLIOValBanterHellos` 9BF6A2 and `HLIOValBanterByes` 9BF6AD.
- Player branches: `HLIOValBanterP`, `RP`, `PlayerP`, `PlayerPr` (the business venture), `PP` / `PPA` (the ring-pickpocket practice), `Morvic`.

**The 32 scenes, one line each** (V = Val, R = Remi):
1. **Intro.** V grumbles about "mercenary work for two hundred gold"; R mocks him; "I'm not a mercenary."
2. **RemiQuest1.** Killing Falmer as a "public service". "All's fair in love and war, my new friend."
3. **RemiQuest2.** R reprograms an automaton. V can't follow the soul-gem wiring, but teaches her a sailor's knot that won't slip.
4. **RemiQuest3.** Hiding salvage from Calcelmo. R pocketed fifteen soul gems; "Leave a guy some soul gems next time."
5. **RemiQuest4.** V wants to sell to Calcelmo; R hates him. V likes that she cares about what a thing *could be*.
6. **Dwemer1.** V: animunculi are just machinery, maybe slaves. R: "Scrap is *not* a slave! He's my... friend."
7. **Dwemer2.** "The pipes sound like screaming." V: "Sometimes there's actual screaming. Bandits... prior expeditions... me..."
8. **Combat1.** One line: "I don't think they're gonna listen to reason, Remi!"
9. **Business1.** R stops V selling a dynamo and hands him junk to pass off instead; V smells a business opportunity.
10. **Business2.** V proposes a partnership: R makes junk look valuable, V sells it, and they split the profits.
11. **Profits1.** First payout. R wants to buy a house; V says spend some on good memories. Drinks for the party on him.
12. **RPS (repeatable payday).** V hands R her share with one of four variants ("Who's got two thumbs and a bag of Septims...").
13. **ChaurusPie.** R warns V privately that her chaurus pie could kill him; he passes "for the good of the group".
14. **Piracy1.** R: "you might as well call yourself a pirate." V explains reputation, leaving survivors, and fear as profit. R: "You've mixed politics into thievery." V: "considering a career change."
15. **SweetRoll.** R ate V's stolen sweetroll. "I stole that fair and square! Rude."
16. **Name.** "Valentino?" "My full name is... Valerius." His Anvil bounty: piracy, smuggling, kidnapping, extortion, blackmail... "and lollygagging." R wants to turn him in.
17. **Smart.** R asks if all pirates are this smart. V: school dropout, "You're brilliant." Then "eccentric", "tall", and machines distracting her.
18. **Crossbow1.** R grabs V's custom crossbow. He built the fast-reload gearing himself, inspired by ship block-and-tackle.
19. **Crossbow2a.** Comparing designs: his speed against her Dwemer-ballista punch; "We're unstoppable, Val!"
20. **Crossbow2b.** His oil is taproot extract mixed with Dwemer oil, and he drank it to test it ("I seem to be able to eat just about anything").
21. **Steal1.** R gives V tiny gears lifted from Lisbet in Markarth, perfect for his crossbow.
22. **Steal2.** V slips a rare vintage into R's backpack; they plan to celebrate that night.
23. **Pets1.** R makes V pet Scrap. "I feel ridiculous... It is pretty cute when his soul gem glows."
24. **Pets2.** V praises Scrap's loyalty, then admits he's glad to adventure with R. R: "You talked about feelings! Are you well?"
25. **Fence1.** R gets moon sugar from her (smuggler) father and bakes with it; V volunteers as taste-tester.
26. **Pickpocket1.** Trading hauls (384 Septims against three rings). V teaches the spill-and-grab ring lift; they plan to practise on the player.
27. **Pickpocket2.** R spots a mark; V plans the "ask for directions" distraction. "I know what I'm doing."
28. **Food.** Grim food at sea, Blacklight kwama eggs, mudcrab cakes with marshmerrow, R's love of Brewet, "a tour of Tamriel".
29. **Corsairs.** V's ship raided Wayrest in '188 when R was a child; R: "You're old!" V: "no one's as surprised as I am that I've lived this long."
30. **Necromancy.** V gently asks about R's father's body being raised by necromancers. "Everyone has a choice." "If you ever want to go kill everyone responsible, I'm on your side."
31. **Morvic1.** R calls him "Valerius" and tells him to stay behind if he objects to the Morvic job; "Try not to get killed, okay?"
32. **Morvic2.** R apologises. "I'm not a killer for hire." He says she started issuing orders "like a captain taking her ship into battle"; apology accepted.

Plus the Hello lines: V on "Remi called me old... I'm not entirely sure how long my lifespan is", "Remi might be the most brilliant person I've ever met", the missing compass, and R not being able to cook.

### B. Val's own `AX ValSerano.esp`

- `AX_Val000FunctionsScript.CheckAllFollowers()` on quest Val000 detects other followers with `Game.GetModByName` / `GetFormFromFile` and stores the result in a global and an alias:
  - Remi `209446` "HLIORemi.esp"
  - Inigo `35561` "Inigo.esp"
  - Kaidan `12188` "KW-Kaidan.esp"
  - Flint `-1840677955` "Flint9.esp"
  - Lucien `22815` "Lucien.esp"
- Only the Remi and Inigo globals are actually used in dialogue conditions (ValNPC hello/idle/goodbye topics, plus ValAddon02 idles for LOTD).
- There is a cooldown global `AX_RandomNPCBanterCD` `2AEF93` for his NPC-comment banter.
- Val's mod even contains **Remi's lines** (her intro at his island, the `RemiValMeetA` scene, `AX_RemiMetVal`), using a "Fake Remi" placeholder NPC `F4BFAE`.

**Method to copy.** Use a start-enabled quest with optional, empty aliases. Fill them from a player-alias `OnInit`/`OnPlayerLoadGame` script using `GetFormFromFile(0x07A065, "AX ValSerano.esp")`, so there is no hard master. Use a Misc/Idle opener topic with these conditions:
- both partners in the scene are teammates and following (`GetPlayerTeammate` / `CurrentFollowerFaction`);
- they are within 1000 units of each other;
- neither is in dialogue or a scene;
- random-percent gating, Reset Hours 24, and progression globals.

The opener's OnEnd fragment starts the Scene.

---

## 6. Technical

- **NPC base:** `AX_ValSerano`, `00AA0F:AX ValSerano.esp` (runtime 2300AA0F in this load order).
  - Flags: Essential, Unique, AutoCalc, PC-level-mult. Race NordRace.
  - Overridden by `KW_ValSeranoRefined.esp`, the Authoria Reqtificated patch and Requiem for the Indifferent.
- **Placed reference:** `AX_ValSeranoREF`, `07A065:AX ValSerano.esp`. Its home cell is SolitudeWinkingSkeever.
- **VoiceType:** `AX_ValVoice` `093578:AX ValSerano.esp`. The young-Val voice is `AX_ValYoungVoice` `AF21F4`.
- **Follower framework:** a custom one, in quest `Val000` `093567` with script `AX_ValController`.
  - `SetFollower` sets the player teammate, fills the FollowerAlias, and sets `AX_ValRecruited` `08E466` = 1.
  - Waiting sets `AX_ValRecruited` = 2. Dismissed sets it to 0.
  - Membership in `AX_ValRecruitedFaction` `E0938C`.
- **"Is following" check, best to worst:**
  1. `GetGlobalValue AX_ValRecruited == 1` (following, not waiting).
  2. `GetPlayerTeammate == 1` on Val (what Remi's mod uses).
  3. `GetInFaction CurrentFollowerFaction` is used by Remi's mod for Remi, and for Val in the Morvic force-greet. Val's own controller doesn't call SetFollower on the vanilla DialogueFollower, so don't rely on CurrentFollowerFaction for Val *(unsure whether a framework adds it)*.
- **Other plugins:** `AX ValSerano-*.esp` add-ons (AbyssalTides, CoWQE, DaedricShrinesAIO, FavorQuestsSeparated, JK patches, LOTD, RaceCompatibility, SSEC, USSEP). There is no separate voice plugin.

---

## 7. Voice reference clips for cloning

Voice files live inside `C:\1. AUTHORIA\mods\Val Serano - Pirate Follower and Quest Adventure\AX ValSerano.bsa` under `sound\voice\ax valserano.esp\ax_valvoice\`. I extracted these candidates to the scratchpad folder below; each is a .fuz (lip data plus xwm audio) and must be converted to WAV before cloning. All five are calm, reflective, conversational lines with no shouting or whispering. Durations are measured from the audio headers.

Extracted folder: `C:\Users\User\AppData\Local\Temp\claude\C--Users-User--claude-spares-spare-XiLrYV\a1586ffc-8b2d-4e13-b3d0-8ad688001b28\scratchpad\val_voice\sound\voice\ax valserano.esp\ax_valvoice\`

| # | File | Length | Line |
|---|---|---|---|
| 1 | `val003_val003life02b_00ed711f_1.fuz` | 8.0 s | "I try to appreciate the good moments, when I find them. Put enough of those together, and it's something like happiness..." |
| 2 | `val004_val004daedra01_004cb733_1.fuz` | 7.8 s | "Azura, Boethiah, and Mephala I know well. My father worships in the New Temple faith and raised me the same." |
| 3 | `val004_val004journal07_00419e4f_1.fuz` | 6.7 s | "My father was a Dunmer, and he raised me as one. I was taught that we're meant to struggle and to survive by any means." |
| 4 | `val004_val004house03_0054b806_1.fuz` | 7.2 s | "Most of the Dunmer I sailed with were Houseless. Some had been kicked out in disgrace, or at least their families had been." |
| 5 | `val002_val002lies02a2_0033aafb_2.fuz` | 6.8 s | "I grew up on land in Cyrodiil, though. Imperial City. It was just me and my mother back then when my father was away." |

Backups in the same folder:
- `val004_val004journal05_00419e47_1.fuz` (7.8 s): "I don't want to romanticize the life I've led. I could have made different choices. I saw how my parents both struggled..."
- `val004_val004jobs06b_007220d5_2.fuz` (7.9 s): "With a ship like the Dark Rose and a good crew, I can get to locations that most others can't and I can do it faster than the competition."
- `val002_val002lies02a2_0033aafb_1.fuz` (5.9 s): "I was born at sea, not quite sure where..."

I haven't listened to the clips. Clip 3 ends on an emotional subject, so check its delivery. The texts are matched to the files by FormID and response number (_1, _2...).
