# GLENMORIL - Act 1 (zzzLrh / zzzLRH quests)

Source: dlgc.txt (lines 2680-4310), glen_story.txt, q_Glenmoril.txt, plus the quest fragment sources in glen_scripts\scripts\source.
All FormIDs are in Glenmoril.esm unless noted.

---

## 1. Story summary, in order

### Setting
Act 1 takes place around Falkreath. It is civil-war time. The town has too many war orphans.
The jarl has called in the "Chick Traders" to take orphans away. Officially they are adoption brokers. Really they are slavers, or worse.
A little Nord girl, Lalanoah, lives in a hidden valley south of town, up the hill. This valley is the **Blessed Glen** (worldspace zzzLrhLalanoaRealm 006F1A, location 006F1B).
A ward stops outsiders from seeing or entering the glen. It is anchored on an old altar of Jhunal (an old Nord rune god, linked to Julianos). Only invited people can find the door.
The glen holds Lalanoah's House, the Old Well (the "debug room", home of the Black Owl), the Crypts of Kyne (Kalka), and many graves, all named "Hamah".

### Main cast (personality and how they talk)
- **Lalanoah** (UA 006F14). Small Nord orphan girl. She is cheerful and food-obsessed: bread, apples, apple pie, sweet rolls. She says "Yep!", "Hooray!" and "Promise?" a lot, and makes up sing-song rhymes ("Apple, apple, apple pie!"). She knows a simple healing spell from her mother and wants to become a healer at the Temple of Kynareth. Underneath she has a hard edge. If you tease her too much she says "I'm really scary when I'm angry!", and she means it: she kills the player with a killmove (game-over fail states). She calls the troll "Grolly" and the guard "Uncle Brandt". She insists "I didn't cry. I'm my dad's daughter."
  Her family: her mother **Laelnoah** was a skilled healer. She was accused of witchcraft and taken by the **Holy Pipers**, an excommunicated, extremist Vigilant of Stendarr branch. Her father **Gerhard** was the strongest warrior in Falkreath. He became an Imperial Legion Quaestor, then went missing on patrol, and the Legion calls him a deserter.
  Kalka calls Lalanoah "Ms. Hamah". The graves in the glen are all "Hamah", "splendid ladies", and Kalka says the girl will become like them. This hints that she is the heir of an old line of witch-priestesses (Glenmoril / Kyne).
- **Brandt** (UA 006F0A). Falkreath guard. He has "my men", so he is probably an officer (unsure of his rank). He is gruff and rude: he calls you "outsider", "milk drinker" and "bootlicker", and calls Lalanoah "the brat". He loves "true Nord" talk ("True Nords never retreat", "Shor and Talos are perfectly enough for true Nords"). His battle plan is "we just strike at it". He is secretly soft. He feeds Lalanoah through the player, pays you 100 gold to check on her, and helped hide her from the Chick Trader. He is obsessed with his custom Skyforge axe and names it Hati ("Garm... no, Hati"). At the end he quits the guard to raise Lalanoah.
- **Skoll** (UA 006ED8). Lalanoah's dog. "Skoll's name isn't dog, it's Skoll."
- **Groll / Goroll** (UA 006EE2; the alias is called Troll, Goron or Goroll). A rock troll. Someone hired her, paid in "glowing stones", to "guard" Lalanoah. She is the "big bad monster" blocking the way home. At first she speaks broken troll talk ("Ooooh! I Groll. I like talk." "You dumb bunny."). She is "Not female. Maiden." In Ah, Apple Pie! she puts on a fallen monocle and becomes fluent, gentle, motherly and a great cook ("cooking is my life"). She tells the player "you smell a little. Are you bathing regularly?"
- **Kanra** (UA 007711). An earless fox, which Lalanoah insists is a raccoon. She found it hurt in the forest. The Psijic says kanras are rare luck animals and must not be eaten.
- **Ja'zel** (UA 006F0B; other copies are 47AB23 in Ithelia Call 01 and 4806FE in Ithelia Call 02). Khajiit leader of the Chick Traders. He is polite, purring and menacing. He speaks in the third person ("Ja'zel", "this one", "Khajiit") and ends lines with "yes?" and "no?". He promises "Ja'zel decided to collect six chicks... This is a cat's promise." His nose is very sharp: he notices you walking in and out of a doorway that should not exist. He is protected by the story. Attacking him starts a game-over sequence (see section 3).
- **Rolls-On-Roads** (alias Monk, UA 61451C). Argonian Psijic "temporary advisor" who investigates a time breach in Falkreath. He is dry, careful and a little preachy. He hands out chocolate milk for "space-time sickness". He can levitate, and the guards first shot at him thinking he was a dragon. He was born a slave of House Telvanni. He loves fish pie and is courting a female Argonian Behemoth named Heart-Gnawer. He admits he "mixed in a few lies".
- **The Augur of the Obscure** (alias Skull, UA 61451E). A talking skull who sees non-linear time. He calls the player "meat-brain" and "mate". He is obsessed with beavers ("little bundles of hatred"), pee-and-memory jokes, and "brain-billies", the memory-stinging spirit jellies that give the side quest its name. He also says a garbled Ithelia line.
- **Torvesard** (UA 474EC3). Met in a dream. He is a "maligraphy", a living-ink replica of the Dremora from ESO. He is formal and cold: "There is no such thing as equal trust between mortals and Daedra." He serves a Prince whose name you cannot perceive (Ithelia).
- **White Owl / Jhunal the White** (UA 006EDD). A spirit owl. He tells you "You are blessed. But you must remain pure." Later: "You are no longer pure."
- **Black Owl / Jhunal the Black** (UA 007B80; the merchant voice is zzzLrhJhunalBlackMerchant). A riddling owl merchant in the Old Well. Later the Psijic thinks it is a Daedric imitation of Jhunal: black, with gold goat-slit eyes.
- **Kalka** (UA 0085B5). Keeper of the Crypts of Kyne. Soft-spoken. She calls Lalanoah "Ms. Hamah" and gives her a cure potion.
- **Sheo** (UA 0085B8). The "walking Shivering Mushroom". Only says "Strawberry torte! Ta ta!" (a Sheogorath wink).
- **Maria** (UA 008686). Broken Markarth prostitute who was raised by the Chick Traders. She prays to Kyne ("We are cursed...") and treats a doll as her lost baby.
- **Orland / Orlando** (UA 008688). A cruel Markarth informant. "Faith" means gold to him. He laughs at Maria's story.
- **Ozwald** (UA 0083AD). A Witch Hunter, seen whispering with Ja'zel in Act 1. Gruff ("I don't care for idle chatter"). He becomes important in Act 2.
- Minor: **Nostos** (UA 0176B3), a sad old man at the roadside who remembers "the Blue Star" and begs you to "help that girl". **Algos** (UA 0176B5) is paired with him. The five chick orphans are Chick01-05 (UA 007744-007748). **PaleChick** is UA 0087DE.

### Quest by quest

**Mod start.** zzzLrhBypass (012EAD; its winner is "Glenmoril - Delayed Start.esp") starts The Way is Blocked, The Black Owl (Old Well), Nostos G and The Chick Trader's Shadow at stage 10. At stage 10.1 it also starts Brain-Billy's Sting and the Torvesard dream check. Without the Delayed Start plugin, I am unsure what starts The Way is Blocked (probably a start-game-enabled flag).

1. **The Way is Blocked (Mq01).** Outside Falkreath, Lalanoah begs Brandt for bread and has no gold. Brandt sends her away and says he will "dirty my axe with a brat's blood" if she enters town. The player buys bread from Brandt for 2 gold and gives it to her. If you take it back, she gets angrier three times and then kills you (fail state). She can't go home because a "big bad monster" growled at her and Skoll. She leads you through the forest, chattering about a giant snail, bees, mushrooms and a bird's nest. At the door she has lost her key, and you search the route for it. The monster is Groll, a rock troll who was "ordered" by unnamed people, paid in glowing stones, to "guard" "Lala". You talk her down. Lalanoah befriends her ("Can you be my friend?"), asks your name, and makes you her friend too. Brandt turns up: the Chick Traders are coming. He wants Lalanoah kept away from town.
2. **The Chick Trader (Mq02).** You tell Lalanoah to stay away from town. In town, Ja'zel counts five orphans ("chicks"). The letter said six. Brandt lies that one ran off during a "werewolf incident". Ja'zel promises he will collect six. Brandt sends a bag of food to Lalanoah. She gives you a giant apple from mysteriously big apple trees. She tells you her mother was taken by "Sten or something" and her father went to war. Brandt asks you to look after her for 100 gold.
3. **A Curious Animal (Mq03).** Groll offers Lalanoah meat. Lalanoah heals the hurt "raccoon" Kanra instead. A naming joke follows (raccoon / fox / "Kanra is kanra"). If you taunt her about eating Kanra as emergency rations, she kills you (fail state).
4. **Weary of Waiting (Mq04).** Brandt drags you on a "peddler hunt". The peddler Radcliffe's cart is wrecked: claw marks, a slashed horse, cheap iron daggers. A blood trail leads to a ghoul lair (Orphan's Hideout). The peddler is dead. Brandt grumbles about the letter to the family and paperwork.
5. **Ah, Apple Pie! (Mq05).** A shining "flying ship" passes like a shooting star and something falls on Lalanoah's roof: a cube holding a **monocle**. If you refuse to show her three times, she kills you (fail state). Lalanoah tries the monocle and gets a headache. Groll puts it on and becomes fluent and refined (she is cast with Julianos' blessing). She bakes apple pie. Lalanoah asks you to take a slice to Brandt and invite him next time. This quest pauses while Cleaning Up Falkreath runs.
6. **Cleaning Up Falkreath (Mq06).** You and Brandt clear another ghoul nest, Death Stench Cave, full of corpses. A **beast-possessed soul** (a Hircine beast, "worse than werewolves") drops in. You flee. Then you deliver Lalanoah's pie. Brandt: "You and that brat are both so carefree... You're making me a little jealous." You hunt the beast in its Beast Lair with Brandt and two guards. The body wears a broken Imperial Legion amulet. They think the Reachmen made a prisoner into a monster (the Psijic later names him Tauresius Mevid). The cave has a stone statue with an owl. Brandt can't remember which god it is.
7. **The Blessing (Mq07).** Optional: outside Falkreath you can overhear Ja'zel and the Witch Hunter Ozwald. Ozwald is hunting his lost friend "Felix", whose mind is "too far gone". Lalanoah sees you are hurt ("I took an arrow to the knee" is an option). She heals you by the fireplace: "Just look into the fire... close your eyes." The screen fades and you wake in bed at 7 am. Groll serves stew. You get the **Lalanoah's blessing** spell and become "blessed". Leaving, the **White Owl** appears: "You are blessed. But you must remain pure. Unless you remain pure, the blood curse will crawl towards you."
8. **My Precious (Mq08).** Ja'zel loiters near the glen entrance. He smells flowers on you and wonders about the "secret garden" door. He warns: "the Owl walks here. If he whispers something to you, you should obey him." Brandt "rewards" you with two years' worth of iron daggers (a running joke). His Skyforge axe courier is late. You find the courier killed by a **cockatrice** (giant feathers) and recover the axe. Brandt is overjoyed ("Oh Shor, thank you for this axe!") and names it Hati.
9. **Ta Ta! (Mq09).** A walking mushroom made Kanra giant. You meet the mushroom ("Strawberry torte! Ta ta!"). It explodes and you are turned into a **sweet-roll man**. Lalanoah: "You look like a sweet roll!... Your body looks delicious. Someone will eat you." Skoll tracks the smell past cheese, a copy of The Lusty Argonian Maid Vol. 2 that Lalanoah thinks is a baking book, and a creepy rune stone, to the **Crypts of Kyne**. Kalka calls Lalanoah "Ms. Hamah" and gives a potion. Both of you are restored. Groll is embarrassed by the "cookbook" and they bake sweet rolls instead. Kalka: "you're blessed. I envy you." The graves are all Hamah's. Ja'zel was at the Jhunal statue doing "archaeology". He says the owl statue is missing and the rune stone hides precious things from bad people.
10. **The Cat and the Chick (Mq10).** Ja'zel left gold "for the sixth chick". You and Brandt hunt a "killer rabbit". It is another beast-possessed victim, carrying a Solitude shield and a letter to "Edvard, the bunny lover". Brandt tells you Lalanoah's family story (above). He admits the jarl ordered the orphans sold, and he cheated Ja'zel out of Lalanoah. Skoll brings Ja'zel's letter. In a storm, Ja'zel has broken into the glen and holds Lalanoah hostage at her house. Groll is knocked out and Kalka is gone. Ja'zel offers a swap: bring him a "special chick", the **tainted baby** of Maria and the noble Marcus Bruiant in Markarth, "a baby that never grows". In Markarth, Orland sells you the story for 100 gold. Guards threw the cursed baby in the river, and Maria's doll has her umbilical cord sewn inside. Taking the doll sends Maria into a frenzy and she attacks. Maria ends up dead either way, because the script kills her at stage 170. Ja'zel takes the doll ("grasp all, lose all") and frees Lalanoah. She says "I am fine... I am strong..." Brandt decides to quit the guard and raise her. Brandt and Lalanoah share a scene: "I'll be a super-strong healer! I'll beat them to a pulp and then I'll heal them again!" / "By Shor, you're scaring me, kid..." The altar in the glen was befouled with blood ("This place has been seriously befouled" - Kalka). Finally the White Owl: "A blood curse is wandering in the forest. So be careful. You are no longer pure..." Act 2 (zzzGHMq01, Witch Hunters) starts.

**Side threads running alongside:**
- **Brain-Billy's Sting (RoadRoller).** Rolls-On-Roads and the Augur sit outside Falkreath, investigating a "time breach" that someone stitched shut. They suspect a Daedric Prince. You drink chocolate milk for your headaches and lost memories. Then you report each Act 1 event to him: orphans, the troll, the Chick Traders, kanra, ghouls, the beast, the owl, the cockatrice, the mushroom, and Hamah. In return you get a lot of lore. He also teaches a teleport spell back to the Augur. The thread runs on through Act 2 and ends with an escape plan to Artaeum via Alcaire.
- **Ghost in the Mirror (TorvesardContact).** In a dream, at the Shattered Mirror, you meet Torvesard. He says Hermaeus Mora keeps wiping your memories. You keep coming back here by instinct. A "Guide" waits in Falkreath. Kill Miraak (the First Servant) before Mora learns about him. Later: "the Guide will blossom in the sea of ink. Enter his dream... kill him... offer his head on the altar."
- **The Black Owl (SubQuest01).** A riddle in the Old Well: "If pure is foul, then what is foul?"

---

## 2. Quest reference

### zzzLrhGeneric - 007B92:Glenmoril.esm - "LRH Generic Dialogue"
- Summary: Not a real quest. It is a holder for ambient lines: Jhunal the Black (Black Owl merchant), Nostos, Jhunal the White, and Act 2 Witch Hunter base folk (Ozwald, Romion, FL-4N).
- Starts: unsure (no stage code). No stages, no completion.

### zzzLrhMq01 - 007733:Glenmoril.esm - "The Way is Blocked"
- Summary: Feed Lalanoah, walk her home, find her key, and talk the troll Groll into friendship.
- Starts: zzzLrhBypass 012EAD stage 10 (Delayed Start plugin). Otherwise probably at game start (unsure).
- Key stages:
  - 0-5: actors placed. Scene Sc01 force-plays (Brandt refuses Lalanoah bread).
  - 20: you buy bread (2 gold).
  - 40: Sc02 force-plays (she leads you home, chattering).
  - 50: lost key. Catch-up MoveTo the ravine if you are far away.
  - 60-70: key hunt. BlessedDoor is blocked at 70 and unblocked at 80.
  - 80-90: talk to the troll.
  - 100: Sc03 force-plays (Lalanoah befriends Groll).
  - 110: Lalanoah asks your name. Catch-up MoveTo the troll.
  - 120: Sc04 force-plays. Brandt is moved to the entrance.
  - 125: Brandt warns about the Chick Traders.
  - 500 FAIL (you took the bread back): controls disabled, third person forced.
  - 510: Lalanoah killmove on the player. ScDeathCheck plays.
  - 520.1: "anim error" message, then **QuitToMainMenu**.
- Completion: 130 (CompleteQuest). Starts Mq02. Final objective: OBJ125 "Talk to Brandt". 999 is the skip/complete stage.

### zzzLrhMq02 - 007835:Glenmoril.esm - "The Chick Trader"
- Summary: Ja'zel collects five orphans. You run messages and food between Brandt and Lalanoah.
- Starts: Mq01 stage 130.
- Key stages:
  - 10: tell Lalanoah to stay away from town.
  - 20: chicks disabled, Chick cart appears. Sc01 force-plays (Ja'zel and Brandt argue over the sixth chick).
  - 35: you get the food bag.
  - 40-50: the giant apple.
  - 65: talk with Lalanoah about her parents.
  - 70: Ja'zel leaves.
  - 75: Brandt offers 100 gold to watch over her.
- Completion: 80 (CompleteQuest). Gives 100 gold and adds the player to LalanoahFaction. Starts Mq03. Final objective: OBJ75 "Talk to Brandt".

### zzzLrhMq03 - 00790A:Glenmoril.esm - "A Curious Animal"
- Summary: Lalanoah heals Kanra and adopts him.
- Starts: Mq02 stage 80.
- Key stages:
  - 1: ScHeal force-plays (Groll offers meat; Lalanoah heals Kanra).
  - 10: talk.
  - 200 FAIL (you taunt her): controls disabled.
  - 210: Lalanoah killmove.
  - 220.1: **QuitToMainMenu**.
- Completion: 40 (CompleteQuest). Starts Mq04. Final objective: OBJ10 "Talk to Lalanoah".

### zzzLrhMq04 - 007E5E:Glenmoril.esm - "Weary of Waiting"
- Summary: The peddler hunt with Brandt. The trail leads to a ghoul lair and a dead peddler.
- Starts: Mq03 stage 40.
- Key stages:
  - 10: sc1 force-plays (walk to the wreck).
  - 11: catch-up MoveTo the wreck site.
  - 30: sc2 force-plays (Brandt reads the clues).
  - 50: clear the ghoul lair. Brandt becomes a player teammate.
  - 60: sc3 force-plays (body found). Brandt is no longer a teammate.
  - 80: time is set to 8 am.
- Completion: 80 (CompleteQuest). Starts Mq05. Final objective: OBJ70 "Talk to Brandt".

### zzzLrhMq05 - 007F1F:Glenmoril.esm - "Ah, Apple Pie!"
- Summary: The fallen monocle makes Groll smart. Apple pie is baked.
- Starts: Mq04 stage 80.
- Key stages:
  - 10: investigate the roof.
  - 20: show the monocle (refuse three times and you get 500).
  - 30: sc1 force-plays (the monocle scene). Julianos blessing cast on Goroll.
  - 50: starts Mq06; this quest waits.
  - 100: resumed by Mq06 stage 80. Pie ready.
  - 110-120: eat the pie.
  - 130: sc2 force-plays (the sweetroll promise; take pie to Brandt).
  - 500 BAD END: controls disabled.
  - 510: Lalanoah killmove.
  - 520: stop. No quit-to-menu here.
- Completion: 150 (CompleteQuest). Sets Mq06 to stage 100. Final objective: OBJ120 "Talk to Lalanoah".

### zzzLrhMq06 - 0082EE:Glenmoril.esm - "Cleaning Up Falkreath"
- Summary: A ghoul nest, then a beast-possessed soul ambush and escape. You deliver the pie, then kill the beast in its lair.
- Starts: Mq05 stage 50.
- Key stages:
  - 10: sc1 force-plays.
  - 20: catch-up MoveTo the ghoul cave.
  - 30: clear the cave. Brandt is a teammate.
  - 40: sc3 force-plays.
  - 50: the beast falls in. Beast music.
  - 60: sc4 force-plays. The beast attacks and Brandt is set ghost (unkillable). Objective "Escape from the cave".
  - 70: escaped.
  - 80: Mq05 is set to 100.
  - 100: give the pie (optional OBJ105).
  - 110: sc5 force-plays (helpers called).
  - 120: catch-up MoveTo Beast Lair.
  - 130: fight the beast with Brandt and two helpers.
  - 140: sc6 force-plays (identify the body).
- Completion: 160 (CompleteQuest). Starts Mq07. Final objective: OBJ150 "Talk to Brandt".

### zzzLrhMq07 - 0083AC:Glenmoril.esm - "The Blessing"
- Summary: Lalanoah heals you and blesses you. The White Owl warns you to stay pure.
- Starts: Mq06 stage 160.
- Key stages:
  - 0: Ozwald and Ja'zel placed outside Falkreath (optional eavesdrop, sc1).
  - 30: healing.
  - 40: sc2 force-plays. Lalanoah is set don't-move. The room door is locked.
  - 44: you get the LalanoahBless spell (gBlessed=1). **FadeOutGame**, then the player is **MoveTo SleepMarker** (bed). Time is set to 7 am.
  - 50: fade in, player forced into sneak, controls re-enabled. Mq06 is set to 170.
  - 60: eat the stew.
  - 70: talk to Lalanoah.
  - 90: starts Mq08. The White Owl appears and sc3 force-plays.
  - 100: the owl teleports away.
  - 105: the owl was ignored (Mq08 stage 5 sets this).
- Completion: 100 or 105 (both CompleteQuest). The next quest starts at 90. Final objective: OBJ90 "???".

### zzzLrhMq08 - 008431:Glenmoril.esm - "My Precious"
- Summary: Ja'zel's sniffing. Then the courier, the cockatrice, and Brandt's Skyforge axe.
- Starts: Mq07 stage 90.
- Key stages:
  - 0: Ja'zel at the glen entrance. Optional talk (5/7). sc1 is his line about the flower smell.
  - 10: you get two iron daggers from Brandt as the reward.
  - 20: sc3 force-plays (walk to the site).
  - 21: catch-up MoveTo.
  - 40: corpse scene.
  - 50: cockatrice fight. Brandt is a teammate.
  - 60-70: find the axe.
  - 80: Brandt equips the new axe.
- Completion: 90 (CompleteQuest). Starts Mq09. Final objective: OBJ80 "Talk to Brandt".

### zzzLrhMq09 - 0085BD:Glenmoril.esm - "Ta Ta!"
- Summary: The Shivering Mushroom turns you into a sweet-roll man and Kanra into a giant. Kalka's potion cures you both.
- Starts: Mq08 stage 90.
- Key stages:
  - 0: Kanra scaled x10. Ja'zel at the Jhunal statue (optional talk).
  - 10: Mq08 is set to 100.
  - 20: the mushroom (Sheo) appears.
  - 25: explosion. **Forced first person, controls disabled, FadeOutGame, knock-out idle.**
  - 30: you wake as a sweet-roll man (SweetRollman equipped). Controls back, third person.
  - 40: sc2 force-plays (Skoll tracks the scent).
  - 50: catch-up MoveTo the cave entrance. sc3 force-plays (Kalka).
  - 70: sc4 force-plays (the potion).
  - 80: **catch-up MoveTo RecoveryMarker, forced first person, controls disabled, fade, knock-out and get-up idles**. Kanra and the player are restored.
  - 100: cooking (sc5, sweet rolls).
- Completion: 90 (CompleteQuest). Starts Mq10. Final objective: OBJ80 "Talk to Lalanoah".

### zzzLrhMq10 - 008685:Glenmoril.esm - "The Cat and the Chick"
- Summary: Killer rabbit, then Ja'zel takes Lalanoah hostage. The Markarth doll trade frees her. Brandt adopts her. The owl says you are no longer pure.
- Starts: Mq09 stage 90.
- Key stages:
  - 0-1: sc1 (Ja'zel leaves gold with Brandt).
  - 20: sc2 force-plays.
  - 21: catch-up MoveTo the beast lair.
  - 30: killer rabbit fight. Brandt is a teammate.
  - 40: sc3 force-plays.
  - 45-50: Brandt's story about the family.
  - 60: sc4 force-plays (Skoll's letter).
  - 70: **storm weather forced**. Ja'zel holds Lalanoah. Goroll stunned and disabled, Kalka disabled. ScLalaBlock started. sc5 force-plays.
  - 75: **MoveTo LalanoahHouseMarker** for the player (if far), Brandt and Skoll.
  - 80: negotiate.
  - 90: go to Markarth (Maria, Orland).
  - 110: pay Orland 100 gold.
  - 140: take the doll.
  - 150: Maria frenzies, turns non-essential and attacks.
  - 155: doll given to Ja'zel.
  - 160: sc6 force-plays (release).
  - 170: Ja'zel gone, Maria killed, storm cleared.
  - 180: wait 6 hours outside.
  - 190: sc7 force-plays (Brandt's decision; Brandt and Lalanoah talk).
  - 200: talk to Lalanoah.
  - 210: the owl statue and the dirt rune are disabled. White Owl appears. sc8 force-plays ("You are no longer pure").
- Completion: 220 (CompleteQuest). The owl teleports away. Stage 225 starts **zzzGHMq01** (Act 2). Final objective: OBJ210 "???".

### zzzLrhQTorvesardContact - 474F0F:Glenmoril.esm - "Ghost in the Mirror"
- Summary: Dream meeting with Torvesard at the Shattered Mirror. He sets you against Hermaeus Mora and asks you to kill Miraak.
- Starts: Probably from zzzLrhQCheckDreamTorvesard (474F10, "Check Sleep"), which zzzLrhBypass starts at 10.1. Most likely this fires when you sleep. Exact trigger unsure; the player-alias script was not decompiled.
- Key stages:
  - 0: **ReturnMarker placed at the player, then player MoveTo PlayerMarker** (the dream cell zzzLRHDreamMirror 474E9E, under the "???" world location 0109CD).
  - 10: approach the mirror.
  - 20: Sc01 force-plays (Torvesard appears).
  - 30-60: talk.
  - 70: **MoveTo ReturnMarker** (wake up). Sets gHasTovesardMemory=1.
- Completion: 70 (CompleteQuest). Final objective: OBJ60 "Exit the dream".
- Note: Torvesard's dialogue changes if Miraak is already dead ("Too late. Hermaeus Mora has already dealt with Miraak.").

### zzzLrhSqRoadRoller - 614517:Glenmoril.esm - "Brain-Billy's Sting"
- Summary: The Psijic Rolls-On-Roads and the Augur investigate the Falkreath time breach. You report each Act 1 and Act 2 event to them.
- Starts: zzzLrhBypass stage 10.1 (qRoadRoller.Start). A starter quest, zzzLRHSqRoadRollerStarter 614513, also exists. Stage 0.1 means "skipped" and jumps to 999.
- Key stages:
  - 0: Monk and Skull placed. "Search for Falkreath's new visitors". The opening scene (scBegin) is them talking about the time breach, chocolate milk and beavers.
  - 20: you get chocolate milk.
  - 30: memory talk.
  - 35: offer to help.
  - 40: accept. You get the teleport spell SpTeleport (back to the Augur, outdoors only, not inside wards).
  - 100: Act 1 reports open.
  - 110-190: one report stage per Act 1 quest (Mq01-Mq09).
  - 195-200: Rolls-On-Roads vanishes with summon FX (off to the Reach).
  - 210: back. Mq10 report (the glen was attacked).
  - 220-270: Act 2 reports (blood curse, Witch Hunters, Ebonwall, Cradle Woods, Zuzu, the Oneiromancer, Jhunal).
  - 280: the escape plan (Red Drop, Piper's Hill, Alcaire, Artaeum).
  - 290: ScEnd force-plays ("I'll be waiting for you in Alcaire"). Teleport spell removed.
- Completion: 300 (CompleteQuest). Monk and Skull disabled. Final objective: OBJ280 "Talk to <Monk>".

### zzzLrhSubQuest01 - 007B93:Glenmoril.esm - "The Black Owl"
- Summary: The Black Owl riddle in the Old Well. Answer "Pure" and he says he will grant knowledge anytime. Answer "Foul" or "Abracadabra" and he dismisses you.
- Starts: zzzLrhBypass stage 10.
- Key stages: 10 gives the Foul Key. It is unsure which answer triggers 10, probably "Pure".
- Completion: 20 (CompleteQuest). zzzLrhSubQuest03 017A03 "The Black Owl Flies" forces it complete and brings the owl back in Act 3.

### zzzLrhqItheliaCall01 - 47AAEF:Glenmoril.esm - "Jazel Call Ithelia 01"
- Summary: The game-over sequence if you stray from Ja'zel's path (attack him). He reveals Ithelia's name, and Hermaeus Mora "censors" you.
- Starts: zzzLrhqChickTraderRevenge 0087DF ("The Chick Trader's Shadow") stage 10, "Protect Ja'zel". That quest is started by Bypass. The exact hit trigger is unsure (alias script not decompiled).
- Key stages:
  - 0: Ja'zel stops combat. **Forced first person, controls disabled, knock-out idle, blackout imagespace. Player MoveTo PlayerMarker** (a "hidden altar of the Snow Elves", probably Unala-Se Ruin 47AB12/47AB18). Followers are knocked down (see section 4).
  - 0.1: JSON event flags gItheliaCall and gTimeBreach saved.
  - 8: end music.
  - 10: Hermaeus Mora faces appear.
  - 30: explosion.
  - 40: "Censorship" message, then **QuitToMainMenu**.
- Completion: none. It ends in a quit to the main menu.

### zzzLrhqItheliaCall02 - 4806FD:Glenmoril.esm - "Grasping at Straws"
- Summary: The game-over sequence if you refuse the Witch Hunters (Act 2 entry, zzzGHMq01 stage 255 "Hunter Bad End"). Listed here because of its prefix.
- Starts: zzzGHMq01 stage 255 (qItheliaCall.Start()).
- Key stages:
  - 0: **fast travel disabled**, exit door blocked. "Escape the Witch Hunter".
  - 10: Ja'zel summoned and Sc01 force-plays.
  - 10.2: **MoveTo PlayerMarker, controls disabled**, Mnemoli weather forced.
  - 10.3: flags gRefuseWH and gTimeBreach.
  - 40: explosion.
  - 50: "Censorship" message, then **QuitToMainMenu**.
- Completion: none. Objective OBJ0 "Escape the Witch Hunter" is failed at 10.

### Small helper quests (no dialogue)
- zzzLrhBypass 012EAD (winner Glenmoril - Delayed Start.esp): starts Act 1. 10 starts Mq01, SubQuest01, SubQuest02 and ChickTraderRevenge. 10.1 starts RoadRoller and the Torvesard dream check. Completes at 999.
- zzzLrhQCheckDreamTorvesard 474F10 "Check Sleep": a running sleep watcher. Completes at 999.
- zzzLRHSqRoadRollerStarter 614513 "Starter: Rolls-On-Roads": completes at 999 (stop). Start trigger unsure.
- zzzLrhSubQuest02 0176B8 "Nostos G": moves Nostos and Algos to a TeleportMarker and disables a Boss. No completion flag.
- zzzLrhSubQuest03 017A03 "The Black Owl Flies": disables the Black Owl and re-enables him in Act 3. Completes at 20.
- zzzLrhqChickTraderRevenge 0087DF "The Chick Trader's Shadow": stage 10 "Protect Ja'zel" starts Ithelia Call 01 (CompleteQuest). Stage 255 stops it in Episode 3. zzzGHMq01-era code sets 255 when the Hinnom gate opens.
- Radiant fetch/kill jobs. Giver unsure. The fetch jobs share collection container 08D992. Each completes at its CompleteQuest stage, and 999 is abort:
  - zzzLRHrqChicken 092BA7 "Chicken Extermination": kill a cockatrice. Completes at 10.
  - zzzLRHrqCookingRecipe 092B9C "Cooking Recipe": completes at 20.
  - zzzLRHrqKanraRescue 092BBC "Kanra Rescue": rescue a kanra and take it to the Blessed Glen. Sc01 force-plays at 10. Completes at 20.
  - zzzLRHrqMushroom 092BAC "Mushroom": kill a Shivering Mushroom. Completes at 10.
  - zzzLRHrqNutrient 092BA1 "Nutritional Potion": completes at 20.
  - zzzLRHrqRogueHunt 092BB4 "Ruffian Hunt": beat up a ruffian. Completes at 10.
  - zzzLRHrqSweetroll 092B8C "Sweet Roll": completes at 20.

---

## 3. "Banter must be silent" moments

Force-played scenes (Sc..ForceStart). Most of these can be skipped through the mod's scene-skip system.
- Mq01: stages 5-10 (Sc01, bread), 40-50 (Sc02, walk home), 100-110 (Sc03, troll friendship), 120-125 (Sc04, Brandt).
- Mq02: stages 20-30 (Sc01, Ja'zel counts the chicks).
- Mq03: stages 1-10 (ScHeal, Kanra healing).
- Mq04: stages 10-20 (sc1), 30-40 (sc2), 60-70 (sc3, the body).
- Mq05: stages 30-40 (sc1, monocle), 130-140 (sc2, pie promise).
- Mq06: stages 10-20 (sc1), 40-50 (sc3), 60-70 (sc4, beast ambush and escape), 110-120 (sc5), 140-150 (sc6, the body).
- Mq07: stage 0-10 (optional sc1, Ozwald and Ja'zel), 40-50 (sc2, healing), 90-100 (sc3, White Owl).
- Mq08: stage 0-10 (sc1, Ja'zel), 20-30 (sc3), 40 (corpse activation).
- Mq09: stages 40-50 (sc2, scent trail), 50-60 (sc3, Kalka), 70-80 (sc4, potion), 90-100 (sc5, cooking).
- Mq10: stages 0-10 (sc1), 20-30 (sc2), 40-45 (sc3), 60-70 (sc4), 70-80 (sc5, hostage), 160-170 (sc6, release), 190-195 (sc7, Brandt and Lalanoah), 210-220 (sc8, White Owl).
- Torvesard: stages 20-30 (Sc01).
- RoadRoller: the opening scene near stage 0-10, and 290-300 (ScEnd).
- Kanra Rescue: stage 10 (Sc01).

Player controls disabled, fades and killmoves:
- Mq01 500-520.1: controls off, Lalanoah killmove, **QuitToMainMenu** (fail state).
- Mq03 200-220.1: same, **QuitToMainMenu**.
- Mq05 500-520: controls off, killmove (no quit).
- Mq07 44-50: **FadeOutGame**, player moved to bed, time set to 7 am, then forced sneak on waking.
- Mq09 25-30: forced first person, controls off, fade, knock-out (mushroom blast). Player becomes a sweet roll.
- Mq09 80: the same knock-out sequence for the cure.
- Ithelia Call 01, 0-40: knock-out, blackout, teleport, **QuitToMainMenu**.
- Ithelia Call 02, 10-50: teleport, controls off, **QuitToMainMenu**.

Teleports / MoveTo:
- Catch-up teleports only fire if the player is far away. They follow scene skips: Mq01 50 and 110, Mq04 11, Mq06 20 and 120, Mq08 21, Mq09 50 and 80, Mq10 21 and 75.
- Dream: Torvesard 0 (into the Shattered Mirror) and 70 (back).
- Mq10 75: player, Brandt and Skoll pulled to Lalanoah's house.
- Time skips: Mq04 80 sets 8 am. Mq07 44 sets 7 am. Mq10 180 is a 6-hour wait.

Forced weather: Mq10 70-170 (storm), Ithelia Call 02 10.2 (Mnemoli weather).

---

## 4. Followers

Scripts that touch followers:
- **Ithelia Call 01 (47AAEF)** has aliases Follower01-05 and calls KnockDownFollower on each of them at stage 0. Up to five current followers are knocked down before the player is teleported to the Snow Elf altar. This is the only explicit follower code in Act 1.
- Brandt is temporarily made a **player teammate** during fights: Mq04 50-60, Mq06 30-40, Mq08 50-60, Mq10 30-40. He also gets IgnoreFriendlyHits. In Mq06 60-70 he is set ghost (unkillable).
- The player is put in and taken out of **EscortFaction** while following Brandt (removed at Mq04 55 and Mq06 40).
- Lalanoah, Skoll, Brandt and Kanra are repeatedly moved with MoveTo / MoveToPackageLocation to keep them with the player. Your own followers are never moved by these scripts.
- I found no script in Act 1 that dismisses, blocks or checks the player's own followers. Unsure: the "Check Sleep" player-alias script was not decompiled.

Places followers cannot follow:
- **The Shattered Mirror dream** (Torvesard, 474E9E, under the "???" location 0109CD). This is a pure player teleport.
- **Ithelia Call altar** (Ithelia Call 01, probably Unala-Se Ruin, inside the Blessed Glen). The player is teleported and the followers are knocked down where they stand.
- **Ithelia Call 02**: player-only teleport.
- **Mq07 healing sleep**: the player is moved to a bed inside Lalanoah's house. Followers stay put, probably in the same house.
- **The RoadRoller teleport spell** (SpTeleport, from stage 40): a player self-teleport to the Augur and back. Followers likely do not travel with it (unsure).
- **Blessed Glen** (worldspace 006F1A): lore says only invited people can see or enter it. The scripts do not stop followers going through the door, so followers can probably walk in (unsure). Story-wise their presence there is odd.
- **Mq09 sweet-roll transformation**: the player is knocked out where they stand. Followers stay but are not scripted.

---

## 5. Banter hooks

- Mq01 20-30: buying a starving child bread from a guard who says "don't feed the orphans".
- Mq01 40-50: Lalanoah's nature tour (giant snail, bees, "Don't steal them").
- Mq01 85-120: a troll guarding a child, paid in "glowing stones". "Not female. Maiden."
- Mq01 125 / Mq02 20: first mention and first sight of the Chick Traders. Five chicks, "there should be six".
- Mq02 40-50: giant apples from apple trees that "are rare around here".
- Mq02 65: Lalanoah's mother taken by "Sten or something", her father "at war". "I can adopt you" gets a refusal.
- Mq02 75: gruff Brandt paying you to babysit.
- Mq03 10-30: the raccoon/fox/kanra naming argument. "Emergency rations" is a deadly joke.
- Mq04 20-70: crime-scene reading of the peddler's wreck (iron daggers, untouched gold, claw marks). Ghoul stench.
- Mq05 10-40: a "flying ship" in the sky and a magic monocle that makes a troll eloquent.
- Mq05 40-50: the troll tells the player they smell.
- Mq06 50-70: the beast-possessed soul and the retreat. "Worse than werewolves."
- Mq06 140-150: a Legion soldier turned into a monster, maybe by the Reachmen. Brandt can't name Jhunal's statue.
- Mq06 100: Brandt receives the pie ("You're making me a little jealous").
- Mq07 0: optional eavesdrop on the Witch Hunter and the Khajiit trader.
- Mq07 44-60: waking in a stranger's bed, healed by a child. "Did you carry me to bed?"
- Mq07 90-100: a talking White Owl. "Remain pure... the blood curse will crawl towards you."
- Mq08 0-7: Ja'zel noticing the hidden door and smelling flowers on the player.
- Mq08 10: yet more iron daggers as a reward.
- Mq08 80-90: Brandt cradling his axe and naming it.
- Mq09 30-80: the player as a delicious sweet roll ("Someone will eat you"), giant Kanra, a walking mushroom shouting "Ta ta!"
- Mq09 40: The Lusty Argonian Maid as a "bread baking book".
- Mq09 50-60: Kalka calling Lalanoah "Ms. Hamah". Many graves with the same name.
- Mq10 30-45: the "killer rabbit" that is just a dead white rabbit. The letter to "Edvard, the bunny lover".
- Mq10 50: Brandt's confession that the jarl sold the orphans.
- Mq10 70-80: Ja'zel threatening a child in a storm.
- Mq10 90-150: Markarth's cruelty (Orland's laughter, the river baby, the doll with an umbilical cord). Maria attacks and dies.
- Mq10 170-200: Brandt quits the guard to raise her. "Super-strong healer."
- Mq10 210: the owl says "You are no longer pure." Lead-in to Act 2 and the blood curse.
- RoadRoller 20-40: a flying Argonian Psijic offering 500-gold chocolate milk. A skull ranting about beavers.
- RoadRoller 110: "the Psijic Order will not lend a hand" to orphans. Good moral friction.
- RoadRoller 170: Rolls-On-Roads was a Telvanni slave orphan.
- RoadRoller 240: his Argonian Behemoth girlfriend, Heart-Gnawer.
- Torvesard 70 (on waking): the player "remembers" a Dremora deal from a dream. Followers could notice the player acting strange.
- Ambient: Nostos at the roadside ("Do you remember the Blue Star?").
