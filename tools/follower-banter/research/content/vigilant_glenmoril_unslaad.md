# VIGILANT, GLENMORIL, UNSLAAD - content research for follower banter

Written 2026-10-18. Read-only research. Nothing in MO2, the profiles or the mods was changed.
Live profile: DEEZ CS NUTZ - PICTA (MO2 instance `C:\1. AUTHORIA`).

All three mods are by Vicn and form one trilogy. English translations by Aelarr are installed.
Each mod's text is the live winner, so every quote here is the English text the player sees.

## Contents
- 0. Quick facts: installed plugins, Delayed Start conditions, one silence rule, follower teleports
- A. VIGILANT
- B. GLENMORIL
- C. UNSLAAD
- D. Gore - Vigilant.esp (Gore's own chapter)
- E. Our 8 followers: who can come along, and lines they already have

Each mod section has: 1 spoiler summary, 2 quest table, 3 when banter must be silent, 4 can followers come, 5 fifteen banter hooks.
Extra notes: the worldspaces Stuhn Ravine (023E7E), Bruiant Estate (047CFA) and Witch's Pond (166857) of VIGILANT are child worldspaces of Skyrim, so a `GetInWorldspace Tamriel` test is false there even though followers can walk in. The Arena (0B2AEE) is a child of Coldharbour.

## 0. Quick facts

### What is installed

| Mod | Main plugin | Delayed Start plugin | Voice and extra add-ons that are on |
|---|---|---|---|
| VIGILANT | Vigilant.esm (load slot 94) | Vigilant - Delayed Start.esp (ESL) | VIGILANT ElvenLabs voiced.esp, IVBOS VIGILANT - Female Narrator - Vampira.esp, IVBOS VIGILANT - NPC Voices.esp, Vigilant NPCs Refined.esp, Vigilant Immersion Tweaks - All in One.esp, VIGILANT - Anreme Add-On.esp (new statues and creature looks, no new story) |
| GLENMORIL | Glenmoril.esm (slot 95) | Glenmoril - Delayed Start.esp (ESL) | IVBOS GLENMORIL - Female Narrator - Vampira.esp, Foamimi's Glenmoril NPC Visual Overhaul.esp, GLENMORIL - Anreme Add-On.esp, GLENMORIL - No Stormcloak Volunteers.esp |
| UNSLAAD | Unslaad.esm (slot 96) | Unslaad - Delayed Start.esp (ESL) | Unslaad ElevenLabs Voiced.esp, IVBOS UNSLAAD - Female Narrator - Vampira.esp, UNSLAAD - Anreme Add-On.esp (one extra Jazel dialogue quest), unslaad_elevator.esp |
| Gore's own Vigilant chapter | Gore - Vigilant.esp (slot 123) | none | DBVO Fix - Gore Vigilant.esp, Gore - Vigilant - COTN Dawnstar Patch.esp |

### How each one starts in this load order (Delayed Start conditions, read from the plugins)

| Mod | What the Delayed Start plugin does | Exact condition |
|---|---|---|
| VIGILANT | Removes "start game enabled" from the first quest **zzzAoMMq00 "Vigilant of Stendarr" (005CE2:Vigilant.esm)**. A Story Manager node `VigilantDelayedStart` (000801:Vigilant - Delayed Start.esp) starts it on a **Change Location** event. | Player level >= **25** (global zzzVigilantMinLevel 000800:Vigilant - Delayed Start.esp = 25) **AND** `GetQuestCompleted zDcdMq05 "Censored Fate" (00CA1E:DAc0da.esm) == 1`. So the player must finish Vicn's earlier mod DAc0da first. |
| GLENMORIL | Removes "start game enabled" from **zzzLrhBypass "Bypass" (012EAD:Glenmoril.esm)**, the quest that kicks off act 1. Node `GlenmorilDelayedStart` (000800:Glenmoril - Delayed Start.esp) starts it on a **Change Location** event. | Player level >= **40** (global zzzGlenmorilMinLevel 000801:Glenmoril - Delayed Start.esp = 40). No quest prerequisite. |
| UNSLAAD | Sets the Half-Dragon Doll (020130:Unslaad.esm) and its trigger (02011A:Unslaad.esm) to Initially Disabled. Node `UnslaadStart` (000801:Unslaad - Delayed Start.esp) starts **zzzCrbMq01 "Falling Cat" (01D8FF:Unslaad.esm)** on an **Increase Level** event; its stage 0 only switches the doll on. | Player level >= **40** (global zzzUnslaadMinLevel 000800:Unslaad - Delayed Start.esp = 40). The doll then waits on the ledge behind the High Hrothgar courtyard gates. The story only really begins when the player touches it (Falling Cat stage 10). |

Simple "this mod's story has begun" checks for banter:
- VIGILANT: `GetStage zzzAoMMq00 (005CE2:Vigilant.esm) >= 5` (stage 5 = "Join the Vigilants of Stendarr" shown).
- GLENMORIL: `GetStageDone zzzLrhBypass (012EAD:Glenmoril.esm) 10` (act 1 quests started). The player meets Lalanoah in Falkreath in zzzLrhMq01 (007733:Glenmoril.esm).
- UNSLAAD: `GetStageDone zzzCrbMq01 (01D8FF:Unslaad.esm) 10` (doll touched). `GetStage >= 0` alone is not enough, because stage 0 only enables the doll.

### No journal text, objectives only

None of the three mods writes journal log entries (one or two lines at most). The quest "journal" is the objective list.
Objective numbers almost always match the stage that shows them (OBJ 20 is shown at stage 20). The quest tables below give stage numbers and objective text.

### One rule that covers most of the silence

All three mods take the player to other worldspaces. The safest single rule for the banter controller:

> Banter may only run when the player is in a worldspace that the banter talk was written for. For these three mods, treat every worldspace they add as "silent unless the talk is written for it", and treat Coldharbour, the Atmora chain and the dream worlds as always silent.

The per-mod sections list every worldspace FormID, cell and stage window.

### Follower catch-up teleports (matters for "who can come along")

Some of our followers have their own "teleport to the player when far away" scripts. These can drop a follower into a realm the mod meant to be solo.
- **Gore**: `HD1GoreCatchUp` moves him to the player every 30 s when he is following, more than 1000 units away, not waiting and not relaxing. Gore - Vigilant.esp turns this off (global HD1NoTeleport B296F7:GORE.esp = 1) at the moments his story needs him gone.
- **Kaidan**: `KaidanTeleportScript` warps him when the MCM teleport option (KaiTeleport) is on. It has a hard-coded list of no-teleport locations (Soul Cairn, Apocrypha, Sovngarde, the Deadlands and others). None of the VIGILANT, GLENMORIL or UNSLAAD places are on that list.
- **Val Serano**: `ValCatchUp` helper (blocked by AX_ValNoTeleport).
- **Redcap**: `FA01RedcapCatchUpScript` moves Redcap (and Xelzaz when he is following) to a catch-up marker.
- **Inigo, Lucien, Remiel, Xelzaz (alone)**: no catch-up script was found in loose files; their scripts are packed in BSAs, so this is unsure. Assume they follow only through load doors.

So: "can a follower get there" is not the same as "should they talk there". The banter rules below go by place and story stage, not by who happens to be standing next to the player.

---

## A. VIGILANT (Vigilant.esm)

Written for a banter writer who has never played it. Full spoilers. FormIDs are `XXXXXX:Vigilant.esm` unless marked.
Sources: every Vigilant.esm dialogue line, the quest records, location and cell lists, scenes, and the decompiled quest stage scripts from Vigilant.bsa. Stage-by-stage script notes: `vigilant_glenmoril_unslaad_detail\vigilant_stage_scripts.txt`.

---

### 1. Spoiler summary

#### Premise and tone
- You join the **Vigilants of Stendarr**, the Daedra-hunting order. The mod starts as "monster of the week" jobs with a jolly mentor.
- It turns into a long horror tragedy about **Molag Bal**. Every job you did comes back to haunt you. Your "justice" killed innocent people.
- The final act is a huge, strange trip through **Coldharbour**, which is built as a ruined, dreaming copy of the First Era Imperial City. You live through other people's memories there.
- Tone: grim, cruel, sad, often grotesque (skinning, grinders, child murder, rape themes, vampire baptism). It is also dryly funny at times: lazy Daedra, an "evil" fox bandit who brags about eating snacks, a headless knight with his helmet on backwards.
- Big themes: mercy versus blind justice, guilt, "the Stone" (a fake Heart of Lorkhan that eats souls), and free will versus obedience. Molag Bal is shown as a weak, ugly, hungry thing that wants Aetherius.
- Karma matters. A hidden global (`zzzCHKarma`) goes up or down with your choices and decides the Act 4 ending.
- The mod remembers runs **across characters**. It keeps a JSON file (`ElderScroll_<name>`, via PapyrusUtil) with your "kalpic cycle", how many acts you cleared, and which endings you saw. Later runs unlock extra dialogue and shortcuts.

#### How it starts
- Normally `zzzAoMMq00` "Vigilant of Stendarr" (005CE2) starts with the game.
- **In this setup** the Delayed Start plugin removes that. The quest starts on a location change once the player is **level 25 or higher** (`zzzVigilantMinLevel`) **and** `zDcdMq05` "Censored Fate" (00CA1E:DAc0da.esm) is complete.
- At stage 0, **Altano** is moved to Dawnstar (the inn). An odd trader, **the Owl**, also appears there (`zzzAoMqOwl`).
- You ask Altano "Are you recruiting?", agree, and follow him to the **Temple of Stendarr**. It sits in its own small worldspace, **Stuhn Ravine** (023E7E, cell 025091). There you meet **Thorondir** the Keeper.

#### Act 1 - Altano and the summoner (zzzAoMMq00-10, AoMMqGoodEnd)
1. **Bloodsucker** (Mq01): a newly turned vampire in Whiterun, posing as a prostitute who sells "sweet rolls" at night.
2. **He Who Cannot Be Touched** (Mq02): **Vernaccus**, a boastful, useless Daedra outside Whiterun. His summoner (a woman) escapes.
3. **Lazy Afternoon** (Mq03): a sleepy Daedra loafing in Candlehearth Hall, Windhelm.
4. **The Eye of Madness** (Mq04): **Balor** in Kynesgrove lost a bet to "a woman". She put a stone in his eye that drives people mad. He is harmless. Altano orders you to kill him anyway ("Stendarr's mercy is not blind compassion"). A Meridia cultist offers a "cure" light staff, and the light burns Balor to ash.
5. **Dine and Dash** (Mq05): meet **Master Jacob**, Altano's old mentor, at Stendarr's Beacon. A glutton Daedra in Riften's Bee and Barb eats 1000 gold of food, and Keerava makes you pay.
6. **Thus Spoke Khajiit** (Mq06): **Jo'vanni**, a skooma addict, tried to summon his dead wife **Campaner'Ra**. You enter **his dream** as him (Jo'vanni's Dream Theater) and learn that **Mar'so** skinned Campaner'Ra and wears her pelt. If it goes badly, Mar'so drowns himself in a pond with the pelt (Mq06BadEnd).
7. **Old Regrets** (Mq07): the summoner **Bal** (a woman who looks exactly like Jacob's dead wife **Rahel**) and her ebony-armoured mercenary **Umbra** wipe out Stendarr's Beacon. Jacob confesses that he once sold Rahel's soul to Molag Bal to save his own life. Under the Beacon is an **Altar of Molag Bal**. You kill Bal. **Jacob dies.** Altano takes the **Mace of Molag Bal**.
8. **No Mercy** (Mq08): Altano, now strange and shouting, orders you to kill a "witch" and her child south of Ivarstead. They are **Carene** (an alchemist who learned from Glenmoril witches to lift her husband's curse) and her daughter **Lilian**. Her husband was **Taranis**, the mercenary you killed in Mq07.
   - **Kill them** (stage 20): Stendarr curses you. You collapse and Mq09 starts.
   - **Refuse** (stage 200+): fight Altano (210). If you lose the argument, he mind-controls you ("You will kill these witches... of your own free will", stage 220/230), and that leads to Mq09. If you beat him, he becomes **"the Ugly One"**, a Molag Bal spawn (300). Beat it (310) and you go to the **Good End** branch.
9. **The Endless Fall** (Mq09, kill branch): back at the Temple, Altano has summoned a Daedra. **Thorondir and almost everyone are dead.** Only the librarian **Gwyneth** survives. Ghosts of everyone you killed or failed taunt you: Jacob, Jo'vanni, Mar'so, Carene, Lilian, Balor, Umbra and the vampire girl. You chase Altano to the altar, and **Molag Bal manifests**.
   - Fight him: win at stage 50 and Mq10 starts.
   - **Offer him your soul**: stage 999 sends you straight to **Coldharbour** (an early bad route).
10. **The Landing** (Mq10): the dying Altano says a "sweet voice" seduced him after Bal's death. Destroy the mace. Molag Bal **curses you**: one more stain on your soul and you are dragged into his realm. Gwyneth makes you the **new Keeper**. Stage 50 starts Act 2.
- **Art of Mercy** (AoMMqGoodEnd, spare branch): Carene finds you. An "Orlando" told her you killed her husband. She attacks.
  - **Spare her**: Thorondir lives. He leaves to destroy the Beacon altar and names you acting Keeper with the **Horn of Stendarr** (stage 120). Stage 130 starts Act 2.
  - **Kill her** (stage 50): little Lilian stabs you in the back. You wake in a dream (60) and go to Coldharbour (70).
- **Side quests**: *The Witch of Ivarstead* (AoMSubQ01): the Glenmoril witch **Reyda** watched the family die and mocks you. She is tied to Molag Bal and to "Laza".
- **Owl shortcut**: during Mq00 the Owl gives you a needle. Stab Altano with it and you drop into a "dream without a dreamer" (Dark Tunnel). This **skips straight to Coldharbour**.

#### Act 2 - The Blood Matron / Lamae (zzzBMMq01-03)
- **Empty Cells** (BMMq01): Windhelm's prisoners and guards vanish from the jail and leave blood behind. It is the same thing that happened 20 years ago, which Jacob investigated. A **Maiden Statue** in a solitary cell is the way in.
- **Remnants** (BMMq02): under the statue, inside **Lamae's Dream** (worldspace 035457: Old Windhelm, Old Sewers, Asylum, Blood Mist Castle), you find the lost Vigilants turned into vampires by the **Blood Matron**. One begs for "Stendarr's Mercy".
- **The Blood Matron** (BMMq03): **Lamae Bal** is the first vampire, a Nedic maiden violated by Molag Bal and crying blood ever since. She pulls you into her dream. There you are her beloved, walking to "father's castle" at sunset, and Molag Bal blesses your "union".
  - **Refuse**: fight her (60). Her corpse is raised by the Curse (80-90). Free her from Molag Bal (100). Her servant **Facis** thanks you. Stage 110 starts Act 3.
  - **Accept the baptism** (200-220): you gain the Blood of Lamae and go to Coldharbour. In Windhelm the steward is surprised you're alive, and Gwyneth went underground after you.

#### Act 3 - Child of Oblivion / the Bruiant estate (zzzCOMq01, zzzCOSubQ01)
- **Child of Oblivion**: Gwyneth gets an old letter from Vigilant **Bartholo**, who was sent to the **Bruiant Mansion** near Chorrol (own worldspace **Bruiant Estate** 047CFA). The Khajiit Vigilant **M'que** drives you there by carriage.
  - The family (Lord Marcus, Lady Julia who burned to death, and their son **Julius**) is dead. An Ayleid butler named **Bal** greets you.
  - Break five "Blood Curses" (Shivers, Corruption, Froth, Chains, and **Jealousy**, which is its own worldspace 0619A2). Then free and defeat **Julius**, a child whose hatred burns hotter than Lamae's.
  - The mansion burns. Molag Bal offers to save you.
  - **Accept** (stage 100): you go to Coldharbour.
  - **Die as a martyr** (stage 200): your character dies, and **Successor** starts.
- **Successor** (COSubQ01): the screen fades. **You make a brand-new character in RaceMenu**, a new Vigilant. Gwyneth sends you to find "the Keeper", who is **your old character**. You find only the rusty Horn of Stendarr. M'que asks you to hide the death from Gwyneth. At stage 50 Molag Bal swallows you too, and you go to Coldharbour.
- **Owl shortcut 2** (zzzCOqOwl): the Owl at the mansion says to stab Bal with the needle. That also drops you into Coldharbour.

#### Act 4 - Coldharbour (zzzCHMQ00, CHMQ01, memories, CHMQ02)
**Every route ends here.** At CHMQ00 stage 0 a script teleports you into Coldharbour, and your Horn turns rusty.
- You wake in a sarcophagus in **Mathmalatu Priory**. A sarcastic old man, **"Pepe"**, mocks you ("Did you kill a beggar and take his clothes?").
  - He is really **Bishop Pelan, Grand Inquisitor of the Alessian Order**. He burned the healer **Mary** (called Mara) and helped **Marukh** the Imga prophet raise **the Stone** into the White-Gold Tower.
  - He keeps showing up ahead of you as a guide.
- This Coldharbour is a dead **Alessian-era Imperial City**. **Jyggalag's Army of Order** besieges it, and a silver sphere hangs in the sky. Its districts are full of ghosts of the First Era:
  - **Vernaccus** (again) and his friend **Bourlor**, the "Archer of Kyne".
  - **Menta Na**, the flying worm.
  - **Varla the Man-Hunter**, a half-Ayleid knight.
  - **Giant Knight Ritho** and **Emperor Belharza** the Man-Bull.
  - The **Black Worm**, the Owl Mage **Jhunal**, and the **Black Hand**.
  - **Mary** and her leech children, and the Thrassian Plague.
  - Dead **Knights of the Nine**, some of whom can be recruited.
  - **Laza**, a northern shepherd who gave up his humanity to hunt Molag Bal. He is fused into the barrier wall.
- **CHMQ00 "Coldharbour"** (main route):
  - Waterfront, kill the worm, the sewers to the Prison Tower.
  - Malada, the floating Ayleid temple, reached through the Marukh priory portal (an Abbot fight).
  - Kill Marukh.
  - Pepe gives up hope (90). The barrier breaks and **Greymarch** begins.
  - Get the heart and key of **Dro'Zel**, the Mad King of Senchal (100). Laza's air strike (110). An Order explosion (115).
  - Done at 120.
- **CHMQ01 "Aetherius"**:
  - Climb the Tower. Fight **Volar the Deathbringer** (5). Destroy the reanimated body of **Saint Alessia** (7-8).
  - Stage 40 checks **karma ≥ 75 + 25 x cycle (max +50)**.
  - **Good** (50-70): Stendarr's scene. You are knocked out, thrown back to Tamriel and wake in a lake. The **Epilogue "A Million Cats"** follows: Ja'zhan's son fished you out (and robbed you) and saved two Alfiq kittens from Chick Traders.
  - **Bad** (150-180): the "true" Molag Bal appears. You opened Aetherius **for him**. He says Stendarr is dead and Aetherius is his, then dumps you back under a bad sky.
  - Stage 255 is game clear. The act counter becomes 5 (post-game).
- **Memories** (CHMemoryQuest01-13, tracked by **Memory Guide** 42E0B1): you touch relics and **relive other people's pasts as them**.
  - Pelan facing "Mara" in her cell (a Grand Inquisitor parody). The Mad King and his wife Hasaama. Varla sparing an Ayleid girl. Johan, whose sister Martha was murdered, taking Bal's mace. Marukh sacrificing his wife Dulsa to the Stone. Pelan interrogated.
  - Marukh lost in the wasteland. **The Nameless Bard**: the bard who loved Lamae turns out to be the being who becomes **Molag Bal**. Sheogorath shows him he is "a pale beast of Sithis", not Shezarr.
  - Pelinal the Bloody choosing mercy. Morihaus's massacre. Alessia's ("Paravant/Periff") last night. Paravania the Man-Bull.
  - Each memory has a mercy ending and a cruelty ending (karma up or down). Most fade you into a memory cell and back.
- **CHMQ02 "Exsultate Jubilate"** (secret final fight): activate the impaled Molag Bal object. It only works if you have done **5+ dream memories**, OR the cross-save flag "sync_bard" is set, OR the cycle is above 2. You are moved to the **Abyss of Molag Bal** (cell 064F28) to fight him while he asks "Tell me who I am, who you are".
- **Post-game**: *Sacred Anatomancer* (a Riften gut-diviner, the Pipers, the "Radiance" cult). Evil choices lead to *Maggot* (people near you turn into maggots). There are also Belharza and Minotaur quests, an Arena, and boss rematches.

#### The big twists
- Your mentor **Altano** becomes Molag Bal's puppet after picking up the mace. He massacres the Temple or turns into the Ugly One.
- Every "mercy" kill in Act 1 was an innocent or a victim. They come back as ghosts in Mq09.
- **Bal** keeps coming back with different faces: Jacob's dead wife, the Bruiant butler, the bard in the memories. She or he is Molag Bal's agent or mask. Unsure if it is one person.
- **Molag Bal was once mortal.** The memories imply he was the nameless bard who loved Lamae. "The Stone" is a fake, soul-hungry imitation of the Heart of Lorkhan, and you have touched or "swallowed" it.
- The martyr route **kills your character**, and you play your successor.
- The mod remembers your other characters (the cycle).

#### Main NPCs
| NPC | Who / personality |
|---|---|
| **Altano** | Your mentor. Warm, joking, likes a drink and the brothel ("I'll go have some fun as well"). Says "novice". After the mace he turns paranoid and shrieks orders. He becomes the betrayer or the Ugly One, and dies sorry: "I gave in to temptation". |
| **Thorondir** | The old Keeper of the Temple. Kindly, wise: "You're not a true Vigilant if you only blindly do what you're told." Killed in Mq09, survives on the Good End. |
| **Gwyneth** | The librarian. Bookish and anxious: "Please don't take out too many books." She is the last survivor and makes you Keeper. She worries terribly about you. |
| **Jacob** | Altano's old master. Hearty, guilt-ridden. He sold his wife Rahel's soul. Dies in Mq07. |
| **Bal** | The summoner, the butler and the bard. Polite, smug, ominous. |
| **Carene / Lilian** | The "witch" widow and her daughter. Carene's line: "I can't forgive you." |
| **Reyda** | A Glenmoril witch. Mocking, crude. Calls Stendarr "the Old Fool". |
| **Jo'vanni / Mar'so / Campaner'Ra** | A skooma Khajiit, his skin-wearing rival, and his dead wife. |
| **Lamae Bal** | The Blood Matron. Childlike, loving, possessive: "We will be together, forever and ever." |
| **Facis** | Lamae's gentle vampire servant. |
| **M'que** | Khajiit Vigilant and carriage driver. Loyal, blunt. |
| **Julius / Bartholo** | The burning child and the missing Vigilant. |
| **Pepe (Pelan)** | Your sardonic Coldharbour guide. A broken old inquisitor waiting to die. |
| **Molag Bal** | Sneering, "generous" tempter: "I am the bread for the starving." Hates the "Aetherius inside you". |
| **The Owl (Jhunal / "Orlando")** | A friendly trader who offers shortcuts that are really traps. A dragon-obsessed old mage. |
| **Coldharbour cast** | Varla (tormented), Ritho (loyal giant), Belharza (timid emperor), Bandit Kanra (cute fox, "Mwahahaha!"), Ja'zhan (thief cat), Sir Caius, Amiel, Berich and Juncan (weary dead knights), Gaiden Shinji (Redguard swordsman), Gloriel (lonely Meridian). |

---

### 2. Quest table

Started = first stage that sets an objective or runs. Completed = stages flagged CompleteQuest (check with `GetStageDone`). Objective text is quoted when the mod has it. "(none)" means the quest has no journal objective.

#### Act 1
| EditorID | FormID | Name | Summary | Started | Key stages | Completed |
|---|---|---|---|---|---|---|
| zzzAoMMq00 | 005CE2 | Vigilant of Stendarr | Recruitment by Altano in Dawnstar, then the trip to the Temple. | 0 (Altano to Dawnstar, Owl starts); 5 "Join the Vigilants of Stendarr" | 10 "Follow Altano..." (amulet, faction); 15 "Talk to Altano" at the Temple; 20 "Talk to Thorondir"; 30 "Talk to Altano" (tour) | **40** (starts Mq01); 999 (Owl route, Altano gone); 9999 |
| zzzAoMMq01 | 005CE3 | Bloodsucker | Whiterun vampire posing as a prostitute. | 0 "Talk to Altano" | 10/15 Hall of the Dead; 20 "Find the vampire"; 30 "Defeat"; 40 "Report to Altano" | **50**, 9999 |
| zzzAoMMq02 | 006271 | He Who Cannot Be Touched | Vernaccus outside Whiterun; the summoner escapes. | 0 "Talk to Altano in the Bannered Mare" | 10 "Defeat the Daedra"; 20 "Report to Altano" | **30**, 9999 |
| zzzAoMMq03 | 00627F | Lazy Afternoon | Lazy Daedra in Candlehearth Hall. | 0 | 10/15 follow Altano; 20 "Defeat the Daedra"; 30 "Report" | **40**, 9999 |
| zzzAoMMq04 | 0082EA | The Eye of Madness | Balor's mad eye in Kynesgrove; Meridia cultist. | 0 "Talk to Altano in Candlehearth Hall" | 10 investigate; 20 report; 21 (optional) cultist; 30 "Kill Balor"; 38/39 Balor burned by the light | **50**, 9999 |
| zzzAoMMq05 | 0098C9 | Dine and Dash | Meet Jacob; the glutton Daedra in the Bee and Barb; the 1000 gold bill. | 0 | 10 Beacon; 20 Bee and Barb; 25 fight; 30 Keerava; 40 pay (41 borrow from Altano); 50 "Report to Jacob" | **60**, 9999 |
| zzzAoMMq06 | 009E68 | Thus Spoke Khajiit | Jo'vanni's dream, Mar'so and the pelt. | 0 "Talk to Altano" | 10 Ragged Flagon; 20 "Find Jo'vanni"; **30-50 dream as Jo'vanni**; 60 take the pelt from Mar'so; 79 Jo'vanni dies; 80 "Report to Altano" | **90**, 9999; 999 = **Fail** |
| zzzAoMMq06BadEnd | 4CDF8D | Mar'so Suicide | Mar'so drowns with the pelt. | 0 | - | **100** |
| zzzAoMMq07 | 00A3FE | Old Regrets | Beacon massacre; Jacob's sin; Bal; the Mace of Molag Bal. | 0 "Talk to Jacob" | 10 "Defeat Summoner's Mercenary" (Umbra/Taranis); 30 Jacob's confession; **33 "Watch over Jacob" (vision scene)**; 40 "Defeat Bal"; 60/70 give the mace to Altano | **80**, 9999 |
| zzzAoMMq08 | 00EA8A | No Mercy | Kill or spare Carene and Lilian. | 0 "Hunt down the witches" | 20 killed them (cursed, knocked down); 30 → Mq09; 200 "(Optional) Negotiate with Altano"; 210 "Defeat Altano"; 220-230 mind-control scene → Mq09; 300 "Defeat the Ugly One" | **30** (kill), **230** (forced), **310** (Ugly One dead → GoodEnd), 9999 |
| zzzAoMMq09 | 00EFF7 | The Endless Fall | Temple massacre, ghosts, Molag Bal. | 0 "Talk to Altano" | 10 "Defeat the Daedra"; 15 "Look for survivors" (Gwyneth); 20 "Chase Altano" (ghosts 21-26); 30-35 altar scene; 40 "Defeat Molag Bal" | **50** (→ Mq10); **999 = gave soul → CHMQ00**; 9999 |
| zzzAoMMq10 | 011B75 | The Landing | Altano's death; Molag's curse; you become Keeper. | 0 "Talk to Altano" | 10 "Destroy the Mace of Molag Bal"; 20 cutscene; 30 "Return to the Temple of Stendarr" (cursed); 40 | **40**, **50** (→ BMMq01), 999, 9999 |
| zzzAoMMqGoodEnd | 4D0376 | Art of Mercy | Carene's revenge; Thorondir survives. | 0 "Talk to Carene" | 10 "Stop Carene"; 20 talk; 29 "(Optional) Kill Carene"; 30 "Leave this place"; 50 Lilian's backstab → 60 dream → 70 Coldharbour; 110 "Report to Thorondir"; 120 Horn of Stendarr | **50**, **120**, 9999 (130 starts Act 2) |
| zzzAoMSubQ01 | 17576E | The Witch of Ivarstead | Reyda the Glenmoril witch who watched it all. | 10 (set by Mq09 stage 0) | 30 begs for mercy; 200-230 alternative fight; 300 closed by GoodEnd or Successor | **50**, **230**, **300** |
| zzzAoMqOwl | 4419E5 | (unnamed) | The Owl in Dawnstar offers the needle; stab Altano → shortcut. | 0 (with Mq00) | 5/7 needle; 10; **20 stabbed → dropped into the Dark Tunnel**; 40 → CHMQ00 | 255 / 999 (cancelled when you reach the Temple, Mq00 stage 15) |
| zzzBMGuide | 43B81F | Stendarr Guide | Blood-trace helper. | 0 "Trace the blood" | 10 "Trace the elder blood" | 20, 999 |

#### Act 2
| EditorID | FormID | Name | Summary | Started | Key stages | Completed |
|---|---|---|---|---|---|---|
| zzzBMMq01 | 038524 | Empty Cells | Windhelm prisoners vanish. | 0 "Talk to the Courier" (at the Temple) | 10 "Talk to Steward"; 20 dungeons; 30 Maiden Statue; 40 Temple report; 50 Jacob's note; 60 "Eliminate the vampires under Windhelm" (starts BMMq02); 100 "Report to Steward" | **110** (→ COMq01), **255** (Lamae union route), 9999 |
| zzzBMMq02 | 038525 | Remnants | Vampirised Vigilants in Lamae's Dream. | 0 | 10/30/50/90 "Defeat <vampire>"; 60 talk; 65 confession; 70 "Give Stendarr's Mercy" | **100**, 9999 |
| zzzBMMq03 | 038526 | The Blood Matron | Lamae's dream; refuse or accept the baptism. | 10 (Molag vanishes) | **20 pulled into the dream (player teleported)**; 30-50 walk with Lamae; 60 "Defeat Lamae Bal"; 70 back to the landing; 90 "Free Lamae Bal from the curse"; 200-220 union route | **100** (good), **220** (union → CHMQ00), 9999 |

#### Act 3
| EditorID | FormID | Name | Summary | Started | Key stages | Completed |
|---|---|---|---|---|---|---|
| zzzCOMq01 | 065932 | Child of Oblivion | Bruiant Mansion, Julius, the burning house. | 0 "Talk to Gwyneth" | 20 "Travel to the Bruiant Mansion" (carriage, Owl appears); 30 "Investigate..."; 40/45 Bal fight; 60 "Defeat Julius"; 70 "Escape" (Molag Bal appears); 80 "Die in flames as a martyr or accept Molag Bal's corruption"; 90 Oblivion gate | **100** (accept → CHMQ00), **200** (martyr → COSubQ01), 999, 9999 |
| zzzCOGuide | 43CBAE | Stendarr Guide | Curse-room tracker. | 0 | 10 Shivers; 20 Corruption; 22/24 rooms; 30 Froth; 35 key; 40 Chains; 50 Jealousy; 60 "Free Julius" | 70, 999 |
| zzzCOSubQ01 | 324E7E | Successor | **New character** looks for the old Keeper. | 0 (fade, teleport to NewLifeMarker, RaceMenu) | 20 "Talk to Gwyneth"; 30 "Investigate the Keeper's whereabouts"; 40 "Report to Gwyneth"; 50 swallowed → CHMQ00 | **60**, 9999 |
| zzzCOqOwl | 444115 | (unnamed) | The Owl at the mansion; stab Bal → shortcut. | 0 | 10 needle; **20 into the Dark Tunnel**; 40 → CHMQ00 | 255 / 999 |

#### Act 4 (Coldharbour) main
| EditorID | FormID | Name | Summary | Started | Key stages | Completed |
|---|---|---|---|---|---|---|
| zzzCHMQ00 | 12F24E | Coldharbour | Wake in the priory; cross the city with Pepe. | **0 (player teleported into Coldharbour)** | 10 priory; 20 worm dead / Varla's land; 40 docks / sewer; 50-58 Malada portal + Abbot; 60 Laza in the wall; 70-80 Marukh / the Stone; 90 Greymarch begins; 100 Dro'Zel's heart; 110/115 Laza strike, explosion | **120** |
| zzzCHMQ01 | 1363DB | Aetherius | The Tower, Alessia's corpse, the ending. | 3-8 (Pepe ghosts, Deathbringer, Alessia) | 10-30 Pepe; **40 karma check**; 50-70 good; 150-180 bad | **70** (good), **180** (bad), **255** (game clear) |
| zzzCHMQ02 | 08F2F4 | Exsultate Jubilate | Secret duel with Molag Bal in the Abyss. | 10 (teleport to the Abyss) | 20 scene; 30 fight | **40** |
| zzzCHEpilogueQuest01 | 2D35CE | A Million Cats | Ja'zhan Jr and the Alfiq kittens after the good end. | 10 (from CHMQ01 stage 70) | - | **10** |
| zzzCHGreymarchQuest | 13AEE3 | Greymarch | Jyggalag's army, weather. | 10 (from CHMQ00 stage 90) | - | **20** (Jyggalag dead) |
| zzzCHMemoryGuide | 42E0B1 | Memory Guide | Tracks the dreams. | 0 | 100 "Like when the dream no longer needs its dreamer"; 110 "Against the dying of the light"; 120 "Blind eyes could blaze like meteors" | 999 |

#### Act 4 memories (you play someone else inside each)
| EditorID | FormID | Name | Whose memory | Key stages | Completed |
|---|---|---|---|---|---|
| zzzCHMemoryQuest01 | 12C4F4 | The Grand Inquisitor | Mara (Mary), facing Pelan | 0 "Unfulfilled dreams drown in silence"; 10 teleport in; 30-40 return | **20** (silent / mercy), **100** (bad) |
| zzzCHMemoryQuest02 | 13712B | The Mad King | Hasaama, Dro'Zel's wife | 10; 125+ bad | **30**, **130** |
| zzzCHMemoryQuest03 | 13965A | Knight of Hounds | Varla | 20 Belharza's order; 100+ spare branch | **30**, **130** |
| zzzCHMemoryQuest04 | 140225 | Johan the Fool | Johan, Martha's brother | 10 teleport; 20 funeral; 50 the bard Bal and the mace; 70 return; 100-130 bad (take the mace) | **60**, **100** |
| zzzCHMemoryQuest05 | 05AE03 | Adabal | Dulsa (Marukh's wife) | 10 the Stone ritual; 40 Pepe | **50**, **120** |
| zzzCHMemoryQuest06 | 06A23B | Remains of the Miracle | A Colovian interrogator vs Pepe | 10-20 | **30** |
| zzzCHMemoryQuest07 | 06F53C | Temptation of Marukh | Marukh in the wasteland | 40 Al-Esh vision; 50 the vampire (Molag) | **70**, **150** |
| zzzCHMemoryQuest08 | 080E91 | The Nameless Bard | The bard / Molag Bal | 10 Lamae; 60/70 "your name?"; 200s Molag "B"; 300s you are Molag Bal commanding Volar | **90**, **230**, **350**, **370**, 999 |
| zzzCHMemoryQuest09 | 2CAE30 | Beyond the Shores of Madness | The bard with Sheogorath | transforms the player; Whale Graveyard | **150**, **200**, 999 |
| zzzCHMemoryQuest10 | 2A532E | Pelinal the Bloody | Pelinal (Umaril, Mary, Bal) | 70 Umaril; 90-160 the captive; 300 bad | **180**, **300** |
| zzzCHMemoryQuest11 | 2B9BAB | After the Storm | Morihaus after Pelinal's death | - | **50**, **340** |
| zzzCHMemoryQuest12 | 2BC395 | The Final Night | Alessia's last night | - | **50**, **310** |
| zzzCHMemoryQuest13 | 51C038 | Paravania the Man-Bull | Belharza's origin | - | **30**, **40**, 999 |

#### Act 4 side quests (short)
| EditorID | FormID | Name | Summary | Completed |
|---|---|---|---|---|
| zzzCHSubQuest01 | 1273E0 | More Skooma | Free the thief Ja'zhan from the prison. | 20 (255 fail) |
| zzzCHSubQuest02 | 1279A1 | Archer of Kyne | Return Bourlor's bow; he joins against Vernaccus. | 30 (255 fail) |
| zzzCHSubQuest03 | 129061 | The Black Worm | Free the Black Worm (a necromancer). | 30, 255 |
| zzzCHSubQuest04 | 129BCA | Funeral | Ghost Martha seeks the graves of her brothers Johan, Simon and Tlass. | 50 (255 fail) |
| zzzChSubQuest04GoodEnd | 55985A | Martha Becomes Follower | Martha offers to follow you. | 20 |
| zzzCHSubQuest05 | 12AD04 | Madness | Dro'Zel the Mad King kills "the bard" over and over. | 50 |
| zzzCHSubQuest06 | 052F4A | Pitier | A survivor recognises "the monster of Molag Bal" (you). | 30, 40 |
| zzzCHSubQuest07 | 1265FB | Knight of Julianos | Rescue the drunk knight Henrik again and again. | 100 (999 fail) |
| zzzCHSubQuest08 | 1306FA | Knight of Zenithar | The headless Dunmer knight's helmet gag. | 40 (999 fail) |
| zzzCHSubQuest09 | 1C1EA1 | Paladin Melus | Melus, who talks to his dead love Vena. | 20, 30 |
| zzzCHSubQuest10 | 1C31F2 | Knight of Arkay | A self-mutilating "path to divinity" knight. | 20 |
| zzzCHSubQuest11 | 21ED0C | Kyne's Dragon | A wingless dragon; give it the Feather of Kyne. | 60 (999 fail) |
| zzzCHSubQuest12 | 334C8F | Knight of Kynareth | Sir Juncan and Sir Gregory. | 50 |
| zzzCHSubQuest13 | 51ADBF | Broken Horns | Restore Emperor Belharza (Belharza's Horn / Morihaus' Nose Ring). | 60, 999 |
| zzzCHSubQuest14 | 51FD3E | Bald Man-Ape | A Thalmor theosophist wants Jhunal's Library. | 40, 999 |
| zzzChSubQuest15 | 55AA72 | The Saint's Corpse | Gather Vivec's mortal body parts for a funeral. | 140 |
| zzzCHqSAExile | 4EC7F3 | Maggot | Radiance aftermath: get your name back. **Teleports you to an exile spot.** | 999, 9999 |
| zzzAoMSubQ02 | 4D4C3D | Sacred Anatomancer | Post-game Riften gut-diviner. Good: kill him (200-220). Evil: feed him a child (20-130, Piper Temple, teleport at 100). | 220, 310, 9999 |
| zzzAoMSubQ03 | 51EAC1 | Legacy of Belharza | Minotaurs take you to their hidden village (teleport); **Mordog** can follow you. | 30 |

#### Grouped (skip for banter)
- **Managers / MCM**: zzzVigMCM, zVigJsonManager, zzzVigSafety, zzzVigMusicManager, zzzVigWeapTrail, zzzCHQuestManager, zzzCHColosseumManager, zzzCHqWeatherControl, zzzAoMRestoreTemple, the Generic dialogue quests.
- **Radiant / bounty**: Bounty Horn / Book / Witch / Piper / Summoner / Vampire / Daedric Relic / Chick Trader; Radiance in the Vampire / Spawn / Dead / Duplicate / Witch Hunter; "Send the Vigil to <city>" x9; zzzCHrqSoulShriven.
- **Coldharbour boss duels** (zzzCHBossQuest*): Laza 01/02, Varla, Selector, Jyggalag, Pelinal, Morihaus, Menta-Na, Gorieus, Grey Prince, Maram, Abbot, Bloodsucker, Mara Knight, Deathbringer, Ritho, Shoggoth Mother, Warden.

---

### 3. Where follower banter must be silent

The mod moves the player with script `MoveTo` (after fade-to-black) for every realm change and every memory. Simple gates:

**A. Whole worldspaces: always silent.** Gate on `GetInWorldspace`:
- 06D275 Coldharbour (all of Act 4, including the Imperial City districts and Malada)
- 035457 Lamae's Dream
- 0619A2 Blood Curse of Jealousy
- 06C8A8 White Wasteland
- 078779 Elder Field
- 0B2AEE Arena
- 2C5DB1 Old Forest
- 2DA92A Whale Graveyard
- Location gates if easier: Coldharbour root **06D7EA** (every CH district and the memory root sit under it), Lamae's Dream **26D3BA**, White Wasteland 06C8A9, Elder Field 07877A, Old Forest 2C6035, Whale Graveyard 2DA92B.

**B. Dream, memory and cutscene interiors: always silent.**
- Memory root location **26C06B** "Memory" and its children: 38366D, 38366E, 38366F, 383673-383679, 295516, 51ADC5, 51D5D4.
- Memory cells: 136F82, 06A202, 13F449, 083681, 05426A, 2BC266, 2B8757, 138F9A, 28A47A, 088A8D, 295515, 297C76, 137C97, 140815, 12BE8C, 51D5D5, 51ADC4.
- Jo'vanni's Dream Theater: locations 37FBBC / 37FBBE, cell 00185C.
- Dark Tunnel (Owl shortcut): location 4419CF, cell 4419CE.
- Aetherius: cells 1353E4 (good) and 136194 (bad), locations 26C059 / 3822F8.
- Abyss of Molag Bal: cell 064F28, location 26C05A.
- Dev cells (never speak): Actor Room 001845, Storage Room 35DCAF.

**C. Quest-stage windows in Skyrim** (followers may be present but should stay quiet). These are the mod's cutscenes and skippable scenes:
- zzzAoMMq06 stage **30-59** (you are Jo'vanni in his dream).
- zzzAoMMq07 stage **30-39** (Jacob's confession and vision scene) and stage 40 (Bal fight banter is fine, but not talk).
- zzzAoMMq08 stage **20-30** (curse collapse) and **220-230** (Altano's mind-control scene).
- zzzAoMMq09: **running at all**. Silent from stage 0 to 50 (temple massacre, ghosts, Molag Bal). Strictly silent at 30-35 (altar scene) and 40-50.
- zzzAoMMq10 stage **0-30** (Altano dying, curse cutscene).
- zzzAoMMqGoodEnd stage **0-30** (Carene confrontation) and **50-70** (backstab, dream).
- zzzAoMqOwl / zzzCOqOwl stage **20-40** (inside the Dark Tunnel).
- zzzBMMq03 stage **20-100** and **200-220** (inside Lamae's Dream and the baptism).
- zzzCOMq01 stage **60-90** (Julius, Molag Bal's offer, burning) and the curse rooms. The Jealousy room is its own worldspace.
- zzzCOSubQ01 stage **0-20** (death and new character; RaceMenu at stage 10).
- zzzCHMQ00, zzzCHMQ01, zzzCHMQ02, all CHMemoryQuest01-13 while running: silent (they all take place in A/B).
- zzzCHqSAExile stage 0-10 and 999 (exile teleport); zzzAoMSubQ02 stage **100-130** (Piper Temple, evil end scene); zzzAoMSubQ03 stage 5-10 ("close your eyes" teleport to the Minotaur village).
- Generic: suppress while `IsInScene` on the player or the speaker, and while player controls are disabled. The mod disables controls in nearly every cutscene.

**D. Forced transport (followers left behind)**
| Trigger | Player moved to |
|---|---|
| zzzCHMQ00 stage 0 | Coldharbour (TravelMarker); Horn swapped for a rusty one |
| zzzBMMq03 stage 20 | Lamae's Dream (DreamMarker); stage 70 back to the landing |
| zzzAoMMq06 stage 30 / 60 | Jo'vanni's dream / back to Mar'so (CatMarker) |
| zzzAoMMq08 stage 230 | RitualMarker (Beacon) |
| zzzAoMMqGoodEnd stage 60 | dream |
| zzzAoMqOwl / zzzCOqOwl stage 20 | Dark Tunnel |
| zzzCOSubQ01 stage 0 | NewLifeMarker, as a **new character** |
| zzzCHMQ01 stage 70 / 180 | back to Tamriel (ReturnMarker) |
| zzzCHMQ01 stage 170 | bad-end Aetherius |
| zzzCHMQ02 stage 10 | the Abyss |
| Every CHMemoryQuest | stage ~10 in, return stage out |

---

### 4. Can ordinary followers come along?

- **No script in Vigilant handles your followers.** I searched all 607 scripts in Vigilant.bsa. Nothing adds, removes, waits or teleports player followers. The only follower code is for the mod's **own** followers.
- **Exception: Gore.** Gore - Vigilant.esp (section D) has its own scripts. It takes the real Gore away in the Bruiant mansion, gives the player soul-shriven copies of him in Coldharbour, and brings the real Gore back as a follower at the final memory in the tower Sancremor Angasel, so Gore is with the player for the end of Coldharbour.
- Every realm change is a **player-only `MoveTo`**. This is the same pattern as Apocrypha's black books, where followers stay behind. So expect followers to be **left where they stood** in Skyrim for: Coldharbour, Lamae's Dream, the dreams and memories, the Dark Tunnel, Aetherius and the Abyss. Unsure if some framework (Nether's Follower Framework etc.) re-teleports them. Check in game.
- **Coldharbour is designed for its own companions.** It has native, karma-gated recruits:
  - Sir Amiel (karma > 0), Sir Berich (karma ≥ 20), Sir Caius, Sir Juncan, Gaiden Shinji
  - Bourlor (after you return his bow), Al the hound, Mordog the Man-Bull, Martha
  - The mod even checks `CurrentFollowerFaction` on them.
  This strongly implies your outside party is not expected there.
- **The Successor route replaces the player character.** Old followers would meet a stranger. Treat it as "Keeper missing" for the party.
- **Followers CAN come** wherever you walk through normal doors in Skyrim:
  - Temple of Stendarr (Stuhn Ravine world 023E7E). Ordinary load doors, so followers can follow.
  - Every Act 1 job site (Whiterun, Windhelm inns, Kynesgrove, Riften Ratway, Stendarr's Beacon and Beacon Underground 038521).
  - Ivarstead / Witch's Pond (166857).
  - Windhelm dungeon (unsure whether Lamae's Dream is entered by the Maiden Statue door in BMMq02; if so followers may follow into Remnants, but BMMq03 stage 20 is a forced teleport).
  - Bruiant Estate (047CFA, reached by M'que's carriage; unsure whether followers ride along).

---

### 5. Fifteen banter hooks (D&D-party feel)

1. **The new recruit** (zzzAoMMq00 stage 10-30, Temple of Stendarr 025091). The party sizes up the Vigil: robes, a cheerful mentor, and Thorondir's "think with your own head". Someone already doubts the "mercy" motto.
2. **Sweet rolls at night** (zzzAoMMq01 stage 20-40). A rogue type teases the player about the prostitute vampire. Afterwards: "So that's why you look refreshed."
3. **The worst Daedra ever** (zzzAoMMq02 / Mq03 done). The party mocks Vernaccus and the napping Daedra. Light comic relief to set up the later horror. Callback when Vernaccus shows up again in Coldharbour.
4. **Paying the Daedra's tab** (zzzAoMMq05 stage 40). An argument over who pays Keerava 1000 gold. The miser vs the honourable one.
5. **Balor didn't have to die** (zzzAoMMq04 completed via 30/38/39). The party splits on Altano's order and the Meridia "cure". The first real moral argument.
6. **What we saw in his dream** (zzzAoMMq06 completed, or Mq06BadEnd running). Talking it out after Jo'vanni and the skinned wife. The squeamish one versus the cynic. Only after stage 80, never inside the dream.
7. **Jacob's confession** (zzzAoMMq07 completed). "He traded his wife's soul." The party wonders what each of them would trade. And Altano just took the mace.
8. **Altano is acting wrong** (zzzAoMMq08 stage 0-10, before reaching the shack). The party notices the mentor yelling. A warning hook: "That isn't the man who bought us drinks."
9. **We killed a mother and her child** (zzzAoMMq08 stage 30 done, or GetStageDone 20). The party's conscience. Some blame Altano, some blame the player. Payoff for the Mq09 ghosts.
10. **Mercy shown** (zzzAoMMqGoodEnd stage 120 done). Relief and pride: "We said no to him." Thorondir alive, the Horn handed over. The party jokes about the player as "Keeper".
11. **Last ones standing** (zzzAoMMq10 completed). The Temple is a graveyard. Gwyneth alone. The party grieves and pledges to stay. Also the player is now cursed: "one more stain and he takes you".
12. **Prison break in Windhelm** (zzzBMMq01 stage 20-50, Windhelm dungeon). Detective banter about missing prisoners and the creepy Maiden Statue. Debate: should we really go in?
13. **She wanted to marry you** (zzzBMMq03 completed at stage 100). Teasing and unease about Lamae's proposal. Pity for the first vampire. Facis forgiving you.
14. **The Bruiant job** (zzzCOMq01 stage 20-30, M'que's carriage, Bruiant Estate 047CFA). Ghost-story banter on the road and suspicion of the polite Ayleid butler Bal. "Another Bal?" Callback to the summoner from Mq07.
15. **You came back** (zzzCHMQ01 stage 255 done, or zzzCHEpilogueQuest01 running, back in Tamriel). A reunion with the followers who were left behind. "Where were you?" The player can't explain Coldharbour. Branch on the ending: good (karma, stage 70 done) = relief; bad (stage 180 done) = dread, "the sky looks wrong". If zzzCOSubQ01 ran, the followers knew the *old* Keeper. Treat the new character as a stranger wearing the Horn.

Bonus hooks if needed: the Owl's "friendly" needle offer in Dawnstar (zzzAoMqOwl stage 0-10, party distrust); the Chick Trader bounty (buy the orphan for 500 or kill the trader); the Sacred Anatomancer rumour in Riften after the game is cleared (zzzAoMRumor, after CHMQ01 255).

---

## B. GLENMORIL (Glenmoril.esm)

Mod: Glenmoril.esm by Vicn, v0.96 Alpha, English translation. It is the sequel to VIGILANT.
Every FormID below is `XXXXXX:Glenmoril.esm` unless it names another plugin.
Stage numbers come from the quest records and from the decompiled stage scripts.
"Unsure" means I could not prove it from the data.

Detail files (folder `vigilant_glenmoril_unslaad_detail` next to this file):
- glenmoril_part_act1.md, glenmoril_part_act2a.md, glenmoril_part_act2b.md, glenmoril_part_rev.md (per-act notes)
- glenmoril_stage_scripts.txt (every quest's stages, objectives and stage code)

---

### 1. Spoiler summary

#### Premise
- The setting is Falkreath during the civil war. The town is full of war orphans.
- The jarl quietly lets the **Chick Traders** take the orphans away. The Chick Traders are Khajiit "adoption brokers" who are really slavers, or worse.
- One orphan, **Lalanoah**, lives in a hidden valley called the **Blessed Glen**.
- The player befriends her. Then the player is cursed with a **Blood Curse**.
- The player is forced to serve the **Witch Hunters**, who are run by the Chick Trader **Ja'zel**.
- From there the player falls through a chain of Daedric dream realms. Behind it all is the **Black Owl**, a "kind" puppet-master who is writing the player's story.
- **Tone.** It starts as a cosy, sweet, comic village story with bread, apple pie and a talking troll. It slides slowly into grimdark body horror: child trafficking, cannibalism, mutation and grief. It is full of jokes the whole way (iron-dagger memes, sweet-roll man, Nazeem prank call), and it has meta-fiction about loops and replays.

#### How it starts
- The base mod starts the quest **zzzLrhBypass "Bypass" (012EAD)** as soon as the game starts.
- **Glenmoril - Delayed Start.esp** removes that game-start flag. Instead it starts Bypass from a Story Manager Change Location event once the player is level 40 or higher (global zzzGlenmorilMinLevel).
- Stage 0 of Bypass waits 1 second, then sets stage 10.
- **Stage 10** starts these quests:
  - zzzLrhMq01 "The Way is Blocked" (007733)
  - zzzLrhSubQuest01 "The Black Owl" (007B93; the Old Well riddle and the debug/skip room)
  - zzzLrhSubQuest02 "Nostos G" (0176B8)
  - zzzLrhqChickTraderRevenge "The Chick Trader's Shadow" (0087DF), which protects Ja'zel. Attacking him triggers a game-over.
  - It then sets stage 999, which completes the quest.
- A second fragment on **stage 10** also starts:
  - zzzLRHSqRoadRollerStarter (614513), the Psijic side story "Brain-Billy's Sting"
  - zzzLrhQCheckDreamTorvesard (474F10), a sleep watcher that leads to the Torvesard dream
- The Old Well (cell 007A50) has activators that skip Act 1, skip each Act 2 mission, skip Act 3, or start Act 4. This means a save can be in any act without the earlier acts having been played.

#### The acts, in order
The global `gCurrentAct` tracks the act number.

**Act 1: Falkreath / Lalanoah ("Lrh" quests, Mq01-Mq10).** gCurrentAct = 1.
- The player buys bread for Lalanoah, walks her home, and befriends **Groll**, the rock troll who blocks her door.
- Ja'zel arrives to collect "six chicks" and finds only five, because Brandt hid Lalanoah.
- Episodes in the village:
  - Kanra the "raccoon".
  - Ghoul nests.
  - A beast-possessed Legion soldier.
  - A monocle falls from a flying ship and makes Groll eloquent.
  - Brandt's Skyforge axe "Hati".
  - The player is turned into a sweet-roll man.
- Lalanoah heals the player and gives them a **blessing**. The **White Owl (Jhunal)** warns: "You must remain pure."
- At the end, Ja'zel takes Lalanoah hostage. To free her, the player must bring him a cursed doll-baby from Markarth. Maria, its broken mother, dies.
- Brandt quits the guard to raise Lalanoah.
- The owl: "You are no longer pure."

**Act 2: The Witch Hunters ("GH" quests, Mq01-Mq06).** gCurrentAct = 2.
- **The Blue Bird.**
  - The player searches for Lalanoah's father, Gerhard, and finds him dying in a cave.
  - The cave leads into the **Sanctuary of Namira** realm. There the mutated Witch Hunter **Felix** (the "blue bird") is killed.
  - The **Black Owl** gives the player a chalice, and the player is cursed with the **Blood Curse**.
  - **Ozwald** shoots the owl, then shoots the player.
  - The player wakes in **Romion's Workshop**, under the **Abandoned Chapel of Julianos**. They are told: join the Witch Hunters or die. Refusing twice ends the game.
- **Ebonwall.**
  - The team flies Romion's airship to **Wulfharth's Ebonwall**, an Ashlander town being massacred by Nord militia.
  - Missions: kill the Ashkhan, then find the Glenmoril witch **Tabiah**.
  - **Choice:** spare Tabiah AND assassinate the militia leader Magni. That gives the good ending and the follow-up **Embers**, where an orphan is reunited with Tabiah in Windhelm.
- **Tainted Orphan.**
  - Ja'zel's slaughterhouse in Markarth.
  - Then the team hunts the ghoul-spawning stillborn "orphan" in the **Cradle Woods**, among the ghosts of Cuhlecain's rebels. Ja'zel takes the baby.
- **The Bronze Key.**
  - A raid on **Ysmir's Howl**, a Thalmor-wrecked temple city of Talos.
  - The "key" is the mage **Arkved**, who has been reduced to a brain in a tank.
- **Oneiromancer.**
  - The team enters **Quagmire** (Vaermina's realm) in the flesh and kills **Zuzu**, a giant witch who was secretly protecting witches.
  - Optional memory dreams show:
    - Ja'zel's past
    - the last true Chick Trader, Ja'cobee
    - the Black Owl plotting the whole story
  - The player is pulled into Jhunal's library and the "Room of Love". They wake a week later.
  - The White Owl Jhunal is now forgotten by everyone except the player.
- **Or the Gospel.**
  - An assault on Hela's Kyne temple at **Vahdin Holt**. The player kills Hircine's avatar.
  - Ozwald learns he has about three months to live.

**Act 3: The Pipers ("LaM" quests).** gCurrentAct = 3.
- At **Piper's Hill**, the team kills the **Sacred Anatomancer**, a VIGILANT villain, and the Holy Pipers.
- Lalanoah's mother is found butchered. The Red Drop inside her is dead. It now "prefers her daughter's blood".
- Ozwald is shot in the head and turns into a flying monster.
- Thalmor airships shoot down the Witch Hunters' airship.
- Brandt dies defending the glen. The player kills the mutated Ozwald to get the Red Drop.
- Ja'zel offers two "antidote" pills. Both are poison. **Choice:**
  - Give the pill to Lalanoah: she dies, and the player descends **Hinnom** and kills Ja'zel.
  - Take it yourself: the player is dragged through a secret sanctuary and dropped into Hinnom.
- Either way Lalanoah is dead and Ja'zel is gone.

**Act 4: The Black Spring ("Rev" quests).** gCurrentAct = 4.
- The Black Owl sails the player to **Svartibrunnr**, a sunken dream land where it is always night under a **Blue Star**.
- The hub is the city of **Pailune**. It has beast plague, rioters and Radiance cultists. Musketeers guard a safe Square.
- The player looks for the **Daughter of Kyne**. She is **Hamah**: a Snow Elf girl reborn, who made "daughters" to be loved. Lalanoah was one of them.
- After a blood transfusion, Hamah becomes the player's sardonic voice-guide.
- The act is open-world, with Daedric cats (Azura, Hircine, Namira, Sanguine, Sheogorath) and many side arcs.
- Key reveals:
  - Ja'zel's lost father is the peddler Mar-Dro.
  - In **Dreamsleeve**, the player kills Ja'zel's ghost again.
  - **Torvesard** (servant of Ithelia) reveals that **Vaermina** steered everything. He also implies that the Black Owl's lord is **Hermaeus Mora**.
- The player collects blood curses by "devouring". Hidden Humanhood / Beasthood / Mnemoli scores track their choices.
- **Finale, Feast of Love:** the Chaplain **Boltzmer** judges the player by the number of curses they carry, then turns into **Yelem's Vestige** and is killed.
- **The Lost Storyteller:** Hamah unmasks; she looks exactly like Lalanoah. She invites the player into a coffin to dream of **Falmereth**. The message reads "To be Continued. Wait V0.97". The story is unfinished.

#### Main NPCs
| NPC | FormID (UA) | Personality / voice |
|---|---|---|
| Lalanoah | 006F14 | Cheerful Nord orphan, food-obsessed. Says "Yep!", "Hooray!", "Promise?". Wants to be a healer. Has a hard edge: tease her and she kills you (game-over). Hamah's "daughter". |
| Brandt | 006F0A | Gruff Falkreath guard. Says "outsider", "milk drinker", "true Nords". Secretly soft. Adopts Lalanoah. Dies in Act 3 (Little Red, stage 20). |
| Groll / Goroll | 006EE2 | Rock troll ("Not female. Maiden."). The monocle makes her a refined cook. |
| Skoll / Kanra | 006ED8 / 007711 | Lalanoah's dog / her earless fox ("raccoon"). |
| Ja'zel | 006F0B | Khajiit Chick Trader. Polite menace, says "yes? no?", speaks of himself in the third person. Holds the player's leash. Calls the player his "Chick". Dies in Hinnom, then returns as a ghost. |
| Ozwald | 0083AD | Veteran Witch Hunter with a Dwemer rifle. Clipped and gruff ("rookie", "sleepyhead"). Grieving Felix. Dreams of a Breton inn. Dies in Act 3. |
| Romion | 008826 | Elf Dwemer scholar and airship pilot. Ex-Thalmor (Eton Nir), former Psijic hopeful. Polite, nerdy, frightened. |
| FL-4N "DweGear" | 009DC7 | Cheerful Dwemer spider automaton. Insists it is the player's "senior". Loves soul gems. Comic relief. |
| Cedric | 0147BF | Easygoing veteran hunter. Hunts the player in Act 3. |
| The Chaplain (Boltzmer) | 008820 / 008824 | Pops out of the ground with a bell, singing "O little louse..." warnings. In Act 4 he is Yelem's iron-masked assistant and the final boss. |
| White Owl / Jhunal the White | 006EDD | Lalanoah's mother's owl; really the old Nordic rune god. Speaks only to the player: "remain pure". Later forgotten by everyone else. |
| Black Owl / Jhunal the Black | 007B80 / 009BB1 / 012C70 | Sweet, "kind" tempter. Says "I am always on your side." Gives the curse, visits dreams, writes the plot. |
| Rolls-On-Roads + the Augur | 61451C / 61451E | Argonian Psijic and a talking skull ("meat-brain", beaver rants). They investigate a time breach in Falkreath. |
| Torvesard | 474EC3 / 42A6A4 | Cold Dremora servant of the forgotten Prince Ithelia. Meets the player in dreams. |
| Orlando / Orland | 008688 / 014C27 | Curio dealer who turns up across every era of the story. Probably an agent of the Owl (unsure). |
| Hamah | 007BBF | Daughter of Kyne. Acid-tongued ("spineless coward"), secretly lonely. The player can call her "mom". |
| Mar-Dro | 3D45D1 | Comic, loving Khajiit peddler. He is Ja'zel's dead father. |

#### Locations and realms (worldspaces)
| Worldspace | FormID | Parent | Used in |
|---|---|---|---|
| Blessed Glen | 006F1A | child of Tamriel (UseMapData) | Lalanoah's home valley. Acts 1-3. Reached by a door south of Falkreath. |
| Sanctuary of Namira | 009598 | child of Tamriel | Felix boss fight (The Blue Bird, stages 90-116), reached through the cave. |
| Abandoned Chapel of Julianos | 00981E | child of Tamriel | Witch Hunter HQ exterior. Romion's Workshop (cell 0088E9) and the Airship (cell 00D9C7) are under its location. |
| Wulfharth's Ebonwall | 009DE8 | none | Ebonwall mission. |
| Cradle Woods | 00AA1A | none | Tainted Orphan mission. |
| Ysmir's Howl | 00BC78 | none | The Bronze Key mission. |
| Quagmire | 00FDFA | none | Oneiromancer (Vaermina's realm). Its dream interiors have location parent 00F817. |
| Vahdin Holt | 00DE4D | none | Or the Gospel. |
| Piper's Hill | 00CA16 | none | The Pipers / In Plain Sight. |
| Airship Deck | 0FE734 | child of Tamriel | Falling Sky. |
| Great Hole of Hinnom | 00EF8C | none | Lice and Maggots / Skip Hinnom (Act 3 finale). |
| Svartibrunnr ("Black Spring") | 000D62 | none | All of Act 4. Also the Black Owl dreams in Act 2 (the dream start marker 012C30 is here). |
| Dreamsleeve | 491B1A | none | Sacrament of Cat (Act 4). |
| ??? (Milky Sea) | 0109CC | none | Dream space. Location 0109CD is the parent of the Shattered Mirror (Torvesard dream). |
| Northern Forbidden Land | 01159E | none | No quest use found (unsure). |

#### Twists
- The Black Owl is the real author of events. It is implied to serve Hermaeus Mora.
- The witch hunt existed only to lure the player.
- Lalanoah is a "duplicate daughter" of Hamah. The Red Drop wants her blood.
- Ja'zel deliberately caused the Ebonwall massacre to harvest a heart stone.
- Ja'zel is an impostor Chick Trader and was raised as a "Guide". His father Mar-Dro is met in Act 4.
- Ozwald was kept alive because Felix's curse "lives in" the player.
- Both "antidote" pills are poison.
- Boltzmer and Yelem are two halves of one being.
- The mod saves meta flags to JSON (`zzzRevqJsonManager`, "dejavu", "EndJhunal"). Endings remember earlier playthroughs: "How many times do we have to repeat the same ending?"

#### Endings and choices
- **Game-over states.** Each one disables controls and ends with QuitToMainMenu.
  - Refusing or teasing Lalanoah (Mq01 stage 500, Mq03 stage 200).
  - Attacking Ja'zel (Ithelia Call 01).
  - Refusing the Witch Hunters (Blue Bird stage 255, then Ithelia Call 02).
  - Lingering in the Old Well ("To Dust").
- **Ebonwall:** good ending (Magni dead, Tabiah spared) or bad ending (no survivors).
- **Lie to Lalanoah** that her father is "fine", or tell her the truth.
- **Cedric:** persuade him or kill him.
- **Ja'zel:** finish him or let him die.
- **The pill:** give it to Lalanoah (Little Red 150, then Lice and Maggots) or drink it yourself (Little Red 145, then Skip Hinnom).
- **Act 4 devour-or-refuse choices**, each feeding the hidden scores: Hamah's blood, Ja'bal, Ja'zel's curse, Lalanoah's curse, the Worm of Alduin, the cheese. Plus the Torvesard outcome and the Prince-or-Clerk choice.

#### Links back to VIGILANT
- The **Holy Pipers** are an extremist inquisition cast out of the Vigil of Stendarr. Stendarr cursed them, and they kidnapped Lalanoah's mother.
  - Ozwald: "Must have been the work of Molag Bal. He treats Vigilants of Stendarr like his toys."
  - In VIGILANT their creed is "the extermination of Hamah and her bloodline".
- The **Sacred Anatomancer** is a VIGILANT side-quest villain. Vigilant.esm even has a quest "GLENMORIL: Delete Anatomancer" (4EFDFB:Vigilant.esm).
  - In Romion's briefing the Anatomancer's biography keeps rewriting itself: Chorrol mansion, Lake Illinalta, Ja'zhan, Stendarr's Beacon, the Dawnguard, "he was the Dragonborn". These read as echoes of the VIGILANT hero's possible pasts.
- **Ja'zel and the Chick Traders** are foreshadowed in VIGILANT ("Beware of the cat called Ja'zel").
- **Laza** and the **witches of Hinnom** come from VIGILANT. The player's curse is "Laza, the shepherd trapped in the past".
- **Molag Bal** gets only two lines: Ja'zel's "Molag Bal plays a strange game..." and Ozwald's line above.
- No VIGILANT companion returns as a speaking character in Glenmoril. Athanasius "the Vigilant" in Act 4 may be new (unsure).

---

### 2. Story quest table

Notes for the table:
- "Done" is the stage with the CompleteQuest flag. That is the stage to test with `GetStageDone(quest, X) == 1`.
- **999 on almost every main quest is the "skip" stage.** The Old Well skip menu uses it. It also completes the quest, so test it too if you want to catch skipped saves.
- The objective text is the last objective shown before completion.

#### Act 1 (Falkreath)
| EditorID | FormID | Name | Summary | Started by | Key stages | Done (objective) |
|---|---|---|---|---|---|---|
| zzzLrhBypass | 012EAD | Bypass | Starter (Delayed Start: level 40 or higher on a location change). | SM node / game start | 10 starts Act 1 | 999 |
| zzzLrhMq01 | 007733 | The Way is Blocked | Bread for Lalanoah, walk her home, befriend Groll the troll. | Bypass 10 | 20 bread bought; 40-50 walk home; 85-110 troll friendship; 125 Brandt warns of Chick Traders; 500-520 killmove game-over | **130** ("Talk to Brandt"); 999 skip |
| zzzLrhMq02 | 007835 | The Chick Trader | Ja'zel counts five chicks. Food bag and giant apple. | Mq01 130 | 20 Ja'zel scene; 65 talk about her parents; 75 Brandt pays you to watch her | **80** ("Talk to Brandt") |
| zzzLrhMq03 | 00790A | A Curious Animal | Lalanoah heals Kanra. | Mq02 80 | 1 heal scene; 200-220 game-over | **40** ("Talk to Lalanoah") |
| zzzLrhMq04 | 007E5E | Weary of Waiting | Peddler hunt with Brandt; ghoul lair. | Mq03 40 | 50 ghoul lair (Brandt is a teammate); 60 body found | **80** ("Talk to Brandt") |
| zzzLrhMq05 | 007F1F | Ah, Apple Pie! | Monocle from a flying ship; Groll gets smart; apple pie. | Mq04 80 | 30 monocle scene; 50 pauses for Mq06; 100 pie ready; 500-520 killmove | **150** ("Talk to Lalanoah") |
| zzzLrhMq06 | 0082EE | Cleaning Up Falkreath | Ghoul nest; beast-possessed soul; pie for Brandt; kill the beast. | Mq05 50 | 50-70 beast ambush and escape; 100 pie delivered; 130 beast fight; 140 Legion amulet | **160** ("Talk to Brandt") |
| zzzLrhMq07 | 0083AC | The Blessing | Lalanoah heals and blesses the player; White Owl warning. | Mq06 160 | 44 fade, wake in bed (7 am), blessing spell; 90 White Owl "remain pure" | **100** or **105** ("???") |
| zzzLrhMq08 | 008431 | My Precious | Ja'zel sniffs the glen; cockatrice; Brandt's axe Hati. | Mq07 90 | 0-7 Ja'zel at the hidden door; 50 cockatrice; 80 axe equipped | **90** ("Talk to Brandt") |
| zzzLrhMq09 | 0085BD | Ta Ta! | Shivering Mushroom: the player becomes a sweet-roll man; Kalka's cure. | Mq08 90 | 25 explosion knock-out; 30 sweet-roll form; 50 Crypts of Kyne; 80 cure | **90** ("Talk to Lalanoah") |
| zzzLrhMq10 | 008685 | The Cat and the Chick | Killer rabbit; Ja'zel's hostage swap; Maria's doll; Brandt adopts her. | Mq09 90 | 50 Brandt confesses; 70 storm, hostage; 90-150 Markarth, Maria dies (170); 190 Brandt quits; 210 "no longer pure" | **220** ("???"); 225 starts Act 2 |
| zzzLrhSqRoadRoller | 614517 | Brain-Billy's Sting | Psijic Rolls-On-Roads and the Augur investigate the time breach. Report each event to them. | Bypass 10 (via starter 614513) | 40 teleport spell; 110-190 Act 1 reports; 220-270 Act 2 reports; 280 escape plan (Artaeum) | **300** ("Talk to <Monk>") |
| zzzLrhQTorvesardContact | 474F0F | Ghost in the Mirror | Dream meeting with Torvesard; kill Miraak. | Sleep check 474F10 (unsure exact trigger) | 0 MoveTo dream; 20 scene; 70 wake | **70** ("Exit the dream") |
| zzzLrhSubQuest01 | 007B93 | The Black Owl | Old Well riddle "If pure is foul...". | Bypass 10 | 10 Foul Key | **20** |
| zzzLrhqItheliaCall01 | 47AAEF | Jazel Call Ithelia 01 | Game-over for attacking Ja'zel. | ChickTraderRevenge 10 | 0 teleport, followers knocked down; 40 quit to menu | none |
| zzzLrhqItheliaCall02 | 4806FD | Grasping at Straws | Game-over for refusing the Witch Hunters. | GHMq01 255 | 10 teleport; 50 quit to menu | none |

#### Act 2 (Witch Hunters)
| EditorID | FormID | Name | Summary | Started by | Key stages | Done (objective) |
|---|---|---|---|---|---|---|
| zzzGHMq01 | 009B59 | The Blue Bird | Find Gerhard; Felix boss; Blood Curse; join the Witch Hunters. | LrhMq10 225 | 0 waits 72 hours; 30 bribe gold, Agrippa; 55 Ja'zel; 80 Gerhard dies; 90-97 Felix (Sanctuary of Namira); 110 cursed; 116 shot; 120 wake in Romion's Workshop; 130 join or die; 150-160 sword and hair ornament home | **180** ("???", the owl); 190 starts Mq02; 255 refusal game-over |
| zzzGHMq01Captive | 06EDB0 | Captive | Ja'zel's threat letter naming hostages (spouse, current follower). | Refusal topic at Mq01 130 | 0 letter | **10** |
| zzzGHMq02 | 00E3EC | Ebonwall | Airship to Ebonwall; Gulakhans, Thalmor, Ashkhan; Tabiah. | Mq01 190 | 40 board airship; 80 drop into Ebonwall; 155 Magni killed (optional); 190 prank call; 230-240 Ashkhan; 255 Tabiah; 275 kill Tabiah (optional); 280 Black Owl dream; 290 wake in HQ bed | **310** ("Talk to Ozwald") |
| zzzGHMq02GoodEnd | 00EEFA | Embers | Reunite orphan Cruviah with Tabiah in Windhelm. | Mq02 310 if 155 done and 275 not | 20 orphan; 40 escort; 50 reunion | **70** ("Talk to Cruviah") |
| zzzGHMq02Nazeem | 06EDAF | Nazeem | "I'm Nazeem" prank: the Thalmor kill Nazeem. | Communicator topic | 0 kill | **10** |
| zzzGHMq02Sub01 | 00FD2C | Percussive Maintenance | Broken music box; Lalanoah runs to the Crypts of Kyne. | Mq02 310 or GoodEnd 70 | 40 Romion fixes the box; 70 she is gone; 100 found with Kalka ("Ms. Hamah"); 130 owl | **140** ("???"); 150 starts Mq03 |
| zzzGHMq03 | 01230D | Tainted Orphan | Slaughterhouse execution for Ja'zel; the Cradle Woods ghoul "baby". | Mq02Sub01 150 | 10-50 Markarth slaughterhouse; 90 airship; 130 Cradle Woods; 160 Ozwald missing; 240-250 Artur and Anem; 260 Ja'zel takes the baby; 280 dream | **310** ("Talk to Ozwald") |
| zzzGHMq03Sub01 | 012962 | A Thousand Daggers | Brandt's bounty on an iron-dagger factory (Thalmor smuggler). | Mq03 320 | 40 factory (Brandt is a teammate); 70 Kodaavkiin; 95 explosion knock-out; 100 wake at Lalanoah's | **140** ("???", the owl); probably starts Mq04 (unsure) |
| zzzGHMq04 | 0147BD | The Bronze Key | Raid on Ysmir's Howl; steal Arkved's brain. | Mq03Sub01 140 (unsure) | 40 airship briefing; 60 arrival; 140-145 Brass Gear Queen, Alfilion; 160 Arkved found; 180-190 black-out dream; 200 wake on airship | **210** ("Talk to Ozwald") |
| zzzGHMq04Sub01 | 014C39 | Shop of Curiosities | Orlando's shop; mother's staff leads to Piper's Hill. | Mq04 210 | 45 the staff; 70 walk home; 90 Black Owl offer | **100** ("???"); 110 starts Mq05 |
| zzzGHMq05 | 01719C | Oneiromancer | Into Quagmire; kill Zuzu; Jhunal's library; Room of Love. | Mq04Sub01 110 | 30 gate opens; 40 enter Quagmire; 100-107 bosses; 140-150 dragged into library; 170 Forgotten Vessel; 190 Room of Love; 220 +168 hours, back in Falkreath | **210** ("???"); 230 starts Mq05Joint |
| zzzGHMq05Joint | 017530 | Broken Egg | Jhunal is missing; mutated hunter Ulrik. | Mq05 230 | 70 Brandt, Lalanoah and Skoll are teammates; 85 Ulrik | **100** ("Talk to Brandt") |
| zzzGHMq05Sub01-07 | 00C946, 00C9D7, 014A42, 014AFA, 014B4A, 017654, 06492E | Dream Within a Dream, The Last Chick Trader, The Night of Tears, Louse, The Owls, Confined, Lucid Dream | Optional memory dreams inside Quagmire. | Triggers in Quagmire (unsure) | Sub07: 20/40/60/80/100 loop the player | Sub07 **120**; others: last stage |
| zzzGHMq06 | 017733 | Or the Gospel | Vahdin Holt assault; avatar of Hircine. | Mq05Joint 100 | 50 sleep on the airship; 60 arrive; 115 heart stone; 150 blood moon; 180 Hircine; 220 HQ (3 months left) | **240** ("Talk to Ozwald") |
| zzzGHmq06Sub01 | 02C265 | St. Bazura | Effigy party at Lalanoah's; Jhunal forgotten; last mission called. | Mq06 240 | 30 party; 56 burn the effigy; 70 Lalanoah's fears; 90 FL-4N | **100** ("Talk to FL-4N") |

#### Act 3 (The Pipers)
| EditorID | FormID | Name | Summary | Started by | Key stages | Done (objective) |
|---|---|---|---|---|---|---|
| zzzLaMMq01 | 0B1758 | The Pipers | Piper's Hill; the Sacred Anatomancer. | After St. Bazura (unsure exact) | 20 briefing (VIGILANT echoes); 30 arrival; 60-90 apparitions; 105-115 bosses | **120** ("Slay the Radiance Seeker") |
| zzzLaMMq02 | 0E9E2A | In Plain Sight | Mother's corpse; dead Red Drop; Eyes of Hinnom; Ozwald shot. | LaMMq01 120 | 5 body; 30-70 Eyes of Hinnom; 110 Ozwald dies; 140 he mutates | **150** ("Search the watchtower") |
| zzzLaMMq03 | 103B86 | Falling Sky | Thalmor airship battle; crash. | LaMMq02 150 | 20 rest; 40 deck battle; 70/100 timed escapes; 130 crash teleport | **135** ("Defeat Thalmor automatons") |
| zzzLaMMq04 | 11E085 | Little Red | Brandt dies; kill mutated Ozwald; the two pills. | LaMMq03 135 | 20 Brandt dies; 40-50 knock-out; 110 Red Drop; 140 pills | **145** (drink it yourself) or **155** (gave it to Lalanoah at 150) |
| zzzLaMMq05 | 1329BD | Lice and Maggots | Black Owl; Cedric; descent into Hinnom; kill Ja'zel. | LaMMq04 155 | 20-45 Cedric; 70 hunters hostile; 100-106 chick bombs; 120 Ja'zel boss; 130 fall; 145 finish him (optional) | **150** ("(Optional) End Ja'zel"); starts Departure |
| zzzLaMMqAlt | 4863FC | Skip Hinnmon | Pill-on-yourself path: dragged and dropped into Hinnom. | LaMMq04 145 | 0-60 controls locked; 35 Ja'zel, Orlando, Torvesard | **90** ("Read Letter from Ja'zel"); starts Departure |

#### Act 4 (Svartibrunnr / "Revenant")
| EditorID | FormID | Name | Summary | Started by | Key stages | Done (objective) |
|---|---|---|---|---|---|---|
| zzzRevMq00 | 171135 | Departure | The Black Owl's boat into the Black Spring. | LaMMq05 150 / LaMMqAlt 90 / Old Well activator | 20 boat (controls off); 30 arrive | **30** ("Talk to the Black Owl and get on the boat") |
| zzzRevMisc02 | 016143 | Musketeer's Hope | Wilmer's safe Square; starts the five citizen quests. | Wilmer | | **10** |
| zzzRevSub02 | 01710D | Desiccated Embryo | Hamah's body; transfusion or destroy the syringe. | Exploration ("Find the Daughter of Kyne") | 10 knock-out transfusion; 20 Hamah's voice | **40** ("Talk to Hamah"); 500 destroy |
| zzzRevSub01 | 015B58 | Strange Fruit | Prince versus Clerk; mad King; Arcana of Ja'bal. | East forest | 10/15 choice; 30-39 King bosses; 40 starts Communion | **50** ("Report to the Prince..."); 400 alt |
| zzzRevSub01Jabal | 48BF99 | Communion: Ja'bal | Devour or burn Ja'bal. | Sub01 40 | | **10** devour / **100** burn |
| zzzRevSub03 | 34980C | Baby of Nightmares | Athanasius at Anem's corpse; the Rite of Cannibalism. | "Retrace Yelem's footsteps" | 20 monologue; 30 rite (zzzRevSub03Rush 3ABF2B, done at 60) | **40** |
| zzzRevCqPedlar | 3D45DE | Stray Cat | Mar-Dro the peddler; he is Ja'zel's father. | Rescue at stage 7 | 80 mutates on the void ship; 90 "help this one's child" | **100** |
| zzzRevSub04 | 51525D | Sacrament of Cat | Dreamsleeve; kill Ja'zel's ghost; Torvesard. | Moon moth from Stray Cat | 20 Dreamsleeve door; 25-75 chase; 120 boss; 200 Torvesard; 230 devour; 600 Forge (bad) | **500** or **610** |
| zzzRevSub04Jazel | 572FEC | Jazel Phantom | Ja'zel's phantoms haunt the hub. | Sub04 230 | | **100** |
| zzzRevSub05Intro | 5F2B94 | The Lost Storyteller | Hamah makes Lalanoah's curse; unmasks; Falmereth coffin. | Temple of Kyne (unsure) | 45 devour; 80 Hamah's story; 90 "To be Continued" | **100** ("In Falmereth") |
| zzzRevSub06Key01 | 62F3BC | Yelem's Cord | Search Yelem's body. | Fishing Village (unsure) | | **10** |
| zzzRevMq01 | 60026B | Feast of Love | Boltzmer's verdict; he becomes Yelem's Vestige. | Gate trigger (unsure) | 10 verdict scene; 20 fight; 30-38 transformation; 40 Yelem | **50** ("Defeat Yelem") |
| zzzRevCqAisha | 360BD2 | Snow Cat | Assassin Aisha hunts her prince Ja'cobee. | | 60 Kyne idol; 70 fades | **80** |
| zzzRevCqRobin | 3B7828 | Bad Company | Robin the info-broker; killed by Boltzmer's assassins. | | 100 Robin dies | **120** |
| zzzRevCqRuddyman | 3B1B6D | Memory of the Deep Sea | Dreugh-cursed Ruddy Man goes mad. | | 65 boss | **90** |
| zzzRevCqScab | 35AF3D | Stigmata Necrosis | Foul-mouthed executioner Scab. | | 40 madness | **70** |
| zzzRevCqMothMan | 579C46 | Song of Fjyron | Sister Gaga, the moth nun. | | 45 cocoon; 120 she dies | **140** (good); 220/310 bad |
| zzzRevCqLeaper | 5872E4 | Words of Worlding | Apka-Lul the Ruinach; Alduin's dregs. | | 240 boss; 270 the worm | **300** / **400** / **900** |
| zzzRevCqDragon01 | 343B60 | Farewell Gift | Aushahlaas asks the player to put down his friend. | | 20 fight | **50** ("Take <Dragon01>'s Sword") |
| zzzRevBossQuestAhzidal + zzzRevCqAhzidal | 38F141 + 38F17D | Ahzidal / Ahzidal's Remains | Saarthal's Ahzidal; lie or tell the truth. | | | **50**; remains **20** |
| zzzRevBossQuest01-05 | 1F73CC, 1F73E6, 30EF7D, 33DEE3, 36C620 | Lycanthropy 01/02, Moonlit Hunt, Mark of the Hunter, Undead Beast | Hircine beast chain. | chained | | 20 / 40 / **80** (key to Pailune) / **60** (Seal of Hircine) / 30 |
| zzzRevBossQuestDagoth | 3CE9E4 | Will of Dagoth | Ravine of the Old Serpent. | | | **30** |
| zzzRevDA01 / DAAzura / DANamira | 176373 / 355287 / 355274 | Clavicus Vile / Azura / To Fishing Village | Daedric cat errands. | | | 40-50 / 10 / 10 |
| zzzRevSqCheese | 5D7AD9 | Pale Cheese | Two Sheogoraths; St. Bazura in the sewer. | One-Finger (54ACC6) 100 | 200 eat / 300 discard | **900** |

#### Grouped (no story weight)
- **Radiant jobs.**
  - Act 1 (zzzLRHrq*): 092B8C, 092B9C, 092BA1, 092BA7, 092BAC, 092BB4, 092BBC.
  - Act 2 (zzzGHRq*): 083565, 083570, 088763, 088768, 088774, 08877D, 088786, 08878F.
  - Act 4 (zzzRevRq*): 3DA23B to 3E5A03, 3EB596, 3EB5E6, 3F1171, 5A8BC8.
- **Arena rounds:** Bloody Circus zzzRevSCq01, 02, 03 (3F6D3A, 3F6DA7, 3F6DB2), manager 3F6D36, intro 33DF1A.
- **Citizen quests:** zzzRevCqCitizen01-05 (016144 to 0161F1). Misc: 0160BA, 016235, 37226B, 383800, 54ACC6.
- **Replays** ("Sleep inside the EGG"; boss re-runs):
  - Hub: zzzGHReplayGen 0124E3.
  - One per mission: ReplayMq02 010323, Mq03 012587, Mq04 014B78, Mq05 0175E7, Mq06 03B8F6, Mq07 1763BA.
- **Dream / skit / helper quests:**
  - Black Owl dreams: 012C78, 012C8D, 0149C9.
  - Other dream and scene quests: Charm 0172FB, Subject 015407, Radio 014E3F, Skits 01479D, 014749, 0146C0.
  - Chaplain's Song 1: 009B83.
  - Helpers: Blood Curse tracker 012C8A, Skip Ep02 010144, To Dust 014DDD.
- **System quests:** MCM 015111, Safety 015110, JSON 46F321, Key Items 123349, Generic dialogue 007B92 / 0160D6 / 017137 / 00EDEA, and the Gen* cat quests.

---

### 3. When follower banter must be silent

#### A. Whole worldspaces to mute or restrict
These are dream or Daedric spaces where ordinary followers would be odd or absent. Use `GetInWorldspace` on the player.
- **Quagmire 00FDFA.** A Vaermina dream realm entered "in the flesh". Mute it, or allow only a few lines.
- **Dreamsleeve 491B1A.** The inside of Ja'zel's mind. Mute.
- **??? 0109CC.** A dream sea. Mute.
- **Svartibrunnr 000D62.** This is all of Act 4, so do not mute the whole worldspace. In Acts 2-3 it is only reached by the Black Owl dreams. So mute it **only while** `GetStageDone(zzzRevMq00 171135, 30) == 0`.
- **Sanctuary of Namira 009598.** Felix's realm. Mute while zzzGHMq01 (009B59) is between stages 90 and 130.

#### B. Interior cells to mute (pure dream, vision or loop spaces)
Use `GetInCell` on the player.
- 474E9E Shattered Mirror (Torvesard dream)
- 016B2A Jhunal's library ("???")
- 014F23 Room of Love
- 05F6B1 Dwemer Water Purifier (Lucid Dream loop)
- 0175FD Room of Confinement
- 014B12 "M"
- 0149D6 Saarthal (dream)
- 011261 Mausoleum of Anequina
- 00F966 Chick Room
- 00F911 Cattle Shed
- 00FAE3 Nomad Tent
- 014A6F Research Tower (dream)
- 01507A Dream Surface
- 48071E Secret Sanctuary (Skip Hinnom drag)
- 515264 Ja'zel's Neural Pathway
- 007A50 **Old Well**. This is the debug/skip room and the "To Dust" game-over. Mute it always.
- 010E73 Create Actor Room, 007653 Actor Room, 002C11 TEST Room (developer rooms).

#### C. Quest stage windows to mute
"A-B" means mute while `GetStageDone(Q, A) == 1` and `GetStageDone(Q, B) == 0`. Quest-local `GetStage` ranges work too while the quest is running.

**Game-over sequences.** Always mute.
- zzzLrhMq01 007733: 500-999.
- zzzLrhMq03 00790A: 200-999.
- zzzLrhMq05 007F1F: 500-520.
- zzzLrhqItheliaCall01 47AAEF and zzzLrhqItheliaCall02 4806FD: whenever running.
- zzzGHMq01 009B59: 255 onward.
- zzzGHEndingOwl 014DDD: whenever running.

**Forced cutscenes, fades, knock-outs and teleports.**
| Quest | Window | Why |
|---|---|---|
| zzzLrhMq07 0083AC | 40-60 | Healing trance, fade, wake in bed |
| zzzLrhMq09 0085BD | 20-30, 80-90 | Mushroom knock-out; cure knock-out |
| zzzLrhMq10 008685 | 70-80, 160-170, 190-200, 210-220 | Hostage, release, Brandt and Lalanoah, owl |
| zzzLrhQTorvesardContact 474F0F | 0-70 | Dream |
| zzzGHMq01 009B59 | 90-130 | Felix, curse, shot, wake (controls off 110-130) |
| zzzGHMq02 00E3EC | 280-300 | Black Owl dream, then wake in HQ |
| zzzGHMq02BO 012C78 | running | Dream |
| zzzGHMq03 01230D | 280-290 | Dream, then medical scene |
| zzzGHMq03BO 012C8D | running | Dream |
| zzzGHMq03Sub01 012962 | 85-110 | Blast knock-out, wake |
| zzzGHMq04 0147BD | 160-210 | Arkved scene, mind burn, dream, wake on airship |
| zzzGHMq04BO 0149C9 | running | Dream |
| zzzGHMq05 01719C | 130-230 | Library, Room of Love, a week lost |
| zzzGHMq05Sub01-07 | while running | Dream vignettes (Sub07 loops the player) |
| zzzGHMq06 017733 | 50-60, 200-230 | Sleep and Chaplain dream; end scene and medic |
| zzzLaMMq02 0E9E2A | 100-150 | Ozwald's death and mutation. The worst place for chatter. |
| zzzLaMMq03 103B86 | 125-135 | Beam and crash |
| zzzLaMMq04 11E085 | 20-60, 140-155 | Brandt dies, knock-out; Lalanoah's death |
| zzzLaMMq05 1329BD | 100-110, 130-150 | Chick-bomb fall; Ja'zel's death |
| zzzLaMMqAlt 4863FC | 0-90 | The whole drag |
| zzzRevMq00 171135 | 20-30 | Boat (controls off) |
| zzzRevSub02 01710D | 10-20 | Transfusion knock-out |
| zzzRevSub03 34980C | 20-30 | Athanasius monologue |
| zzzRevSub04 51525D | 20-500 | Dreamsleeve; Torvesard |
| zzzRevSub05Intro 5F2B94 | 80-100 | Hamah's story, the coffin |
| zzzRevMq01 60026B | 10-50 | Final verdict and boss |

**Mission briefings and the Chaplain's songs.**
- Mute while any `Sc*` scene is playing (`GetIsSceneActionComplete` is impractical). The simplest test is the player's `IsInScene`, or the banter scene's own "pause during other scenes" setting.
- The mod's own scene-skip system (zzzRevSafety + RevSceneManagerQuestScript) can jump a scene straight to the next stage. So key "after" lines on the next stage, not on the scene ending.

#### D. Forced transports (player-only MoveTo)
Followers are left where they stand at each of these.
- **Act 1:**
  - Catch-up teleports: LrhMq01 50/110, Mq04 11, Mq06 20/120, Mq08 21, Mq09 50/80, Mq10 21/75.
  - Mq07 44 (into bed).
  - Torvesard dream 0/70.
  - Ithelia calls.
  - The RoadRoller teleport spell.
- **Act 2:**
  - GHMq01 116/120 (into Romion's Workshop).
  - Dreams: Mq02BO/Mq03BO/Mq04BO 0 (into Svartibrunnr marker 012C30).
  - Wake-ups: Mq02 290 (HQ bed), Mq03 285, Mq04 200 (airship bed).
  - Mq03Sub01 95/100 (into Lalanoah's House).
  - Mq04Sub01 75.
  - Mq05 140/145/150/190/220.
  - Mq06 80/220.
  - Every replay (in and out).
- **Act 3:**
  - LaMMq03 130 (crash site, Blessed Glen).
  - LaMMq04 40/50.
  - LaMMq05 106/130 (Hinnom).
  - LaMMqAlt 0/45/60.
- **Act 4:**
  - Departure 30 (boat to Svartibrunnr; followers are left on the dock).

---

### 4. Can ordinary followers come along?

**Evidence.**
- No Glenmoril script dismisses, disables, blocks or checks the player's own followers.
- Only three scripts touch them:
  - **zzzLrhqItheliaCall01** has aliases Follower01-05 and calls `KnockDownFollower` (bleedout) on them. Followers are expected to be present and are just knocked down.
  - **GHWarpOnFallTriggerScritp** warps the player, `CurrentFollowerFaction` members and teammates back if they fall, and kills anyone else. Followers are expected in mission realms.
  - **GHPoisonTrigger**, **LaMTrapSniperTrigger** and **RevTrapCanonShot** treat `IsPlayerTeammate()` actors like the player. Traps hit followers.
- The mod's own allies (Ozwald, Brandt, Lalanoah, Skoll, OwlDog) are switched with `SetPlayerTeammate`. They fight beside the player's followers; they do not replace them.

**Realm by realm**
| Realm | Way in | Followers? |
|---|---|---|
| Blessed Glen 006F1A | Load door | Yes (no block). Story-wise it is hidden from "outsiders". |
| Sanctuary of Namira 009598 | Cave door in Mq01 | Yes, until stage 116. The player is then teleported out alone. |
| Chapel of Julianos / Romion's Workshop / Airship interior | Doors | Yes. First arrival (Mq01 120) is a solo teleport. |
| Ebonwall 009DE8, Cradle Woods 00AA1A, Ysmir's Howl 00BC78, Vahdin Holt 00DE4D, Piper's Hill 00CA16 | Airship door | Probably yes (door travel; the warp trigger includes followers). Each mission ends with a player-only fade or teleport, so followers must catch up. |
| Quagmire 00FDFA | Dwemer gate in the Analysis Room | Unsure. Even Ozwald is split off. Treat it as "maybe", and keep lines dreamlike. |
| Jhunal's library, Room of Love, Quagmire dream rooms | Teleports | No (player only). |
| Svartibrunnr dreams in Acts 2-3 | Teleport | No. |
| Airship Deck 0FE734 | Door from the airship | Probably yes. Ends in a crash teleport. |
| Hinnom 00EF8C | Gate, then forced falls | Partly. Followers walk in, but the falls at LaMMq05 106 and 130 strand them. |
| Svartibrunnr in Act 4 | Boat, then MoveTo | Unsure. Followers are left on the dock and may only appear if the follower framework teleports them. All the mod's doors back are one-way story doors (unsure). |
| Dreamsleeve 491B1A | Door at Sacrament of Cat stage 20 | Physically possible, but it is the inside of a mind. Prefer silence. |
| Shattered Mirror, Ithelia altar, Old Well endings | Teleports | No. |

**Writing advice.**
- Assume followers are present in Acts 1-3 missions, but write as if they may be missing after any teleport.
- Gate Act 4 lines on the follower actually being in Svartibrunnr: `GetInWorldspace 000D62` on the follower itself.
- Story NPCs say "you're alone now" after Ozwald dies (In Plain Sight 110). A follower contradicting that is a good hook.

---

### 5. Fifteen banter hooks (D&D-party feel)

1. **"Don't feed the orphans."** zzzLrhMq01 at stage 20 (player bought bread). The party argues about the guard who sells bread to a starving child for 2 gold.
2. **The troll who guards a child.** zzzLrhMq01 stage 110-130. "She's not female, she's a *maiden*." The party votes on whether Groll is the best NPC they have met.
3. **Sweet-roll man.** zzzLrhMq09, stages 30 to 80 (the player is a walking sweet roll). Every hungry follower gets a line. "Someone will eat you."
4. **The White Owl talks only to you.** zzzLrhMq07 stage 90 / zzzLrhMq10 stage 210 done. "Who were you talking to? It was an owl." Pure versus no longer pure.
5. **Woke up in a stranger's workshop, cursed.** zzzGHMq01 stage 130 done (joined the Witch Hunters). "Your new boss *shot* you." The party debates running away while the player has a tracking device in their body (zzzGHMq02 stage 20).
6. **A follower named in Ja'zel's letter.** zzzGHMq01Captive stage 10 done. The letter can name the current follower as a hostage. Outrage, fear, or "let him try."
7. **First airship flight.** zzzGHMq02 stage 50-70. Dwemer flight, a talking spider insisting it is "senior", Nords getting airsick.
8. **The prank call.** zzzGHMq02Nazeem stage 10 done. "Did you just get Nazeem killed by the Thalmor?" The party splits between horror and applause.
9. **Ebonwall mercy.** zzzGHMq02 stage 310 done, plus GetStageDone 275 (Tabiah killed) or zzzGHMq02GoodEnd 70 done. Good-aligned and mercenary followers clash over the massacre.
10. **The slaughterhouse.** zzzGHMq03 stage 50 done. "Cat and bear meat", children in the mines. The darkest beat. A paladin-type follower wants to kill Ja'zel now.
11. **The iron-dagger factory.** zzzGHMq03Sub01 stage 20-40. "Are you saying making lots of iron daggers is bad?!" A blacksmith follower takes it personally.
12. **A week lost, and nobody remembers the owl.** zzzGHMq05Joint stage 0-30 (zzzGHMq05 220 done). The party "remembers no statue" either. The player is gaslit by reality.
13. **St. Bazura's feast.** zzzGHmq06Sub01 stage 30-70. Party night at Lalanoah's. Followers argue whether "Bazura" is just "By Azura", and the bard sings. The calm before Act 3.
14. **Two pills, one choice.** zzzLaMMq04 stage 140 done, 145/150 not done. Every follower gives their vote: give it to the child, take it yourself, or smash both. Then an aftermath line on 145 or 155.
15. **The Black Spring.** zzzRevMq00 stage 30 done and the follower is in worldspace 000D62. Endless night, a Blue Star that never sets, and a new disembodied voice the player answers (zzzRevSub02 stage 20 done: "Who is *Hamah* and why are you calling her mom?").

Bonus hooks:
- Ozwald's death (zzzLaMMq02 150 done): a quiet "he was a good partner" line at the next rest (zzzLaMMq03 stage 20).
- Ja'zel's father (zzzRevCqPedlar 90 done).
- "Don't say the bookworm's name" (zzzRevDA01 30).

---

## C. UNSLAAD (Unslaad.esm)

Mod: Unslaad.esm by Vicn (version 3.05 in the script). English voice add-on installed.
Third part of the VIGILANT / GLENMORIL / UNSLAAD trilogy.
All FormIDs are `XXXXXX:Unslaad.esm` unless another plugin is named.
Sources: every Unslaad.esm dialogue line, the quest records, and the mod's own quest scripts (source files ship inside Unslaad.bsa). Stage-by-stage code: `vigilant_glenmoril_unslaad_detail\unslaad_stage_scripts.txt`.

---

### 1. Spoiler summary

#### Premise in one paragraph

Unslaad is a hidden, snowbound land "outside" normal time. A cliff wind behind High Hrothgar carries the Dragonborn into it.
A lonely half-dragon girl, **Ulliss**, lives there in a ruined castle with her white cat **Aisha** and a greedy talking snowball-Khajiit called **Fluffy**.
Ulliss was made, not born. Her mother **Austella** sealed dragon souls in ice. The **Gray Owl** (a man who has called himself "Jhunal" for thousands of years) shaped that ice into a child.
The story is about Ulliss, her later daughter **Lizz**, time travel into Unslaad's ruined future, and finally a journey to frozen Atmora to face the **Black Owl** and its master, a Woodland Man of Hermaeus Mora.
Tone: a sad fairy tale. Cute snow spirits, talking pots and foxes, sudden grief, heavy Elder Scrolls myth (Shor, Ysgramor, Pelinal, Herma-Mora, Lyg, Merid-Nunda, Akatosh).

#### How it starts

- Normal mod: a **Half-Dragon Doll** sits on a ledge behind the High Hrothgar courtyard gates. Touching it starts **Falling Cat** (01D8FF).
- Delayed Start plugin (`Unslaad - Delayed Start.esp`): the doll ref 020130 and its trigger ref 02011A start disabled.
  A Story Manager node (`UnslaadStart`, 000801:Unslaad - Delayed Start.esp) starts Falling Cat on player level-up when level >= 40 (global zzzUnslaadMinLevel).
  **Stage 0** of Falling Cat (Fragment_16) enables the doll and its trigger. Nothing else happens at stage 0.
- Touching the doll sets **stage 10**. Aisha the cat appears near High Hrothgar and dares you to jump ("Won't you jump too?").
- **Stage 15** ("Jump off") enables an entrance marker. That marker is the enable parent of a fall-catch trigger (04ACF1) and a cliff door (020129), both just below the ledge.
- You jump. The fall trigger teleports you into the Unslaad worldspace. **Stage 20** fires when you land on the bridge start (trigger 022967, cell CrbUnslaadBridgeStart).
- Aisha walks you to the castle (scene 022976, stage 30). You meet Ulliss (stage 40). She gives you the **Ring of Chillbite** (stage 50).
  Stage 50 adds you to UnslaadFaction and starts **Hoarfrost** (02299D) and the **Dragon Souls** service (022986).
- After that the cliff door 020129 (Skyrim) <-> 020128 (Unslaad) is a normal two-way load door. A map marker (309312) appears in Skyrim.

#### The acts, in order

**Act 1 - Falling Cat (01D8FF).** Dare, jump, land, meet Ulliss. Aisha mentions an earlier visitor, "a terrible flirt" from Alcaire. That is Hjalti (young Talos), a GLENMORIL link.

**Act 1 - Hoarfrost (02299D).** Ulliss's mother Austella is "ill" and has frozen the inner castle.
You buy the castle key from Fluffy for 1000 gold (stage 20), enter, and fight **Austella**, now an ice monster (stage 40).
At stage 50 you "Decide Ulliss' fate" with Austella's doll. Three outcomes (from the doll script, 0229F1):
- **Keep the doll and give it to Ulliss (good end):** stage 100 -> 110 -> 120. Ulliss learns her mother loved her. ("This is the first time I've felt such... warmth.")
- **Tear the doll's tail off ("Man End"):** stage 200 -> 210 -> 220. Ulliss turns human and freezes to death in the snow. A grave appears.
- **Burn the doll ("Dragon End"):** stage 300 -> 310 -> 320. Ulliss becomes a full dragon, Aisha dies, you must kill Ulliss.
- Both bad ends can be undone later by **Revive** (11023D): use the twinkle star with the Dragon Ring and one dragon soul.

**Act 2 - When You Wish Upon a Star (112A83).** Started by **Fluffy's Secret** (05268B) stage 20 (Fluffy shows you his "twinkle star" and remembers snowmen, gold and an Egg).
Buy the Bell Tower key from Fluffy (100 gold, stage 20). Inside, a ghost scene shows Austella making a deal with the **Gray Owl** (stage 23-25). You find a **dragon ring** and gain a dragon soul (stage 30).
You wish on the star (stage 40). This opens a door into **Lost Unslaad** - Unslaad's future - and starts Long Winter.

**Act 3 - Long Winter (117B3E).** Hundreds of years later. The **Blades** tracked the Dragonborn's trail here and invaded. The castle is in ruins.
Aisha is dying after a last fight (stage 20-25). She dies at stage 30. You kill the Blades Grandmaster and the Three-Headed Priest (stages 40/45), then **Dragon Pus** (Pus of Alduin) (stages 55-60).
The Gray Owl appears (stage 70). He tells you to pour 10 dragon souls into the fallen Ulliss (stage 80). Something "like a life" starts growing inside her (stage 90).
Stage 100 completes, opens the way to the **Northern Sanctuary** and starts Lingering Snow.

**Act 4 - Lingering Snow (117B3F).** A thousand years later still. Ulliss is bones in "Mother's Tomb".
Her daughter **Lizz** (part made from your dragon soul - "in a way, also your child") lives with Fluffy, who now remembers his real name: **Ja'cobee**.
- Lizz guides you over icy bridges to Ja'cobee (stages 20-40). Ja'cobee asks you to check a new tower in the north (stage 50).
- The Gray Owl waits at Owl's Ridge (stages 60-70). He wants Lizz as a vessel. You refuse.
- **Boss Rush** (18F113) runs during stages 80-90: waves of monsters while the Owl monologues. His real dream: to become a dragon and fly.
- You beat the Owl (stage 90 -> 100). He begs, then sets off a replica "fire of Magnus" (stages 101-105). The blast knocks you out (controls disabled, you are moved).
  You walk with ghosts of Ulliss and Aisha (stage 105-110). You find the wounded Owl. Killing him is optional (stage 120).
- "See one of the fates of the Dragonslayer" (stage 130-150): the corpse of a long-dead Dragonborn rises as **Dov-Ah-Kiin** and you must defeat it. This is the twist that Dragonborns end as monsters.
- Ja'cobee asks you to take Lizz to her mother in the past (stages 150-190). He stays behind ("there are two Ja'cobees").
- You lead Lizz through a time portal to the present (stage 210-220). Lizz meets Ulliss (stages 230-250). Quest completes at 250. Epilogue scenes unlock (stage 260).

**Act 5 - Stairway to Llesw'er (1DFDFA).** Starts at Lingering Snow 250. Fluffy (present-day Ja'cobee) says goodbye. He dissolves like an absorbed dragon soul and walks "Khenarthi's path" (stages 10-30).
You pick up his remains and get the **Lucky Coin** ability (stage 40, completes).

**Act 5 - The Owl Flies at Dusk (1DFDFB).** Starts at the same time. Examine the Mural of Jhunal. The **Black Owl** gives you the key to Dragon's Cradle (stage 10). You go to the cradle in Lost Unslaad (stage 20) and send the ice doll into the future (stage 30).
- **Game-over trap:** at stage 40, if Stairway to Llesw'er is NOT completed, the quest jumps to the **Bad End** (stages 600-666). The player is transformed, knocked out, shown a nightmare scene, then the game **quits to the main menu**.
- Normal path: Ja'cobee's spirit stops you. You light the brazier (stages 50-60) and fight the **Gray Owl** in four phases inside his own dream (stages 70-110). He babbles ("Drowning... Help...?").
  Stage 110 kills him for good. Ja'cobee: "Khajiit has seen one last good dream, thanks to you. Now we are even." Stage 120 completes.

**After Act 5 - side quests that gate the finale**
- **Reopen the Gate** (2904BE): after Owl Flies at Dusk, if you carry the Gray Egg or the Loveletter, the time doors reopen and **Orlando the Knowledgeable** appears.
- **Snow Guardian** (364E2B): Jokul guards a block of Atmoran ice. Shout it apart (stage 10). Completes at 20.
- **Liturgy of I** (376B99): needs Owl Flies at Dusk and Snow Guardian done. Gather 7 letter fragments (Naghu, Fluffy for 100 gold, Kanra, Jokul, the rat, Lizz...). The Hermit restores a **Loveletter From the Fifth Era** (stages 110-130). Read it. You say what you will do with your life (stage 140). The Black Owl appears and taunts you (150-160). Completes at 160.
- **Arkved** (33F0E0): after Owl Flies at Dusk, entering a trigger clears the skies over **Dragon's Peak** and gives a Dragon Staff.
- **Road to Atmora** (3C0D01): light a brazier to open map markers for Dragon's Peak and Unslaad.

**Act 6 - The Final Journey (465EBF).** On Dragon's Peak a trigger (3CB45C, base 3CB45A) teleports **the player only** into the sky over Atmora, but only if Liturgy of I is complete. Otherwise it bounces you back with a message.
You fall and are caught by **snow whales**. **Herkel the Fool**, a Clever Man from Ysgramor's age, scolds you ("Did you forget you don't have wings?") and becomes your guide. He calls you "Ysmir".
- Shout away the clouds (stage 20-30, needs Clear Skies). Enter the mouth of a colossus. Explore the **Frozen Tomb** (40). Beat the **Idol of Magnar** (VS quest 409CE1 sets stage 50).
- Shout the ice off a mirror (60-80). Walk through it into **Lyg**, a drowned dream-world of Dreugh. Meet the **Dreugh King / Khev**, "a mirror of Vehk", and his sermons (90-100).
- Break **Ysgrim's Seal** by beating Ysgramor and his bear (VS 419232, which sets stage 110). Enter the **Frozen Abyss** - Atmora soaked in Apocrypha's forgotten memories (110-130). Herkel's memory starts to fail. A strange boy keeps leaving messages (125).
- At the Coma Pipe, fight **Pelinal** ("Hans the Fox"), now a cursed dragon prisoner (stages 130-140). Herkel asks you to free him.
- Herkel sees **Ysgramor** return and starts to lose himself (170). You shout open the ship **World-Eater's-Waking** and face **Oohoo'Laf**, a Woodland Man and Demi-Prince of Hermaeus Mora - the root of the Black Owl (180-185).
- **Three endings** (stage 185 choice):
  - **Unrelenting Force** (190 -> 195): you blast him to dust. He curses you with your dragon name, **Ysmaalithax** ("Northerly Dragon", the name Ysgramor shed, once given to Miraak).
  - **Summon Alduin** (200 -> 210): Alduin's mouth opens and devours him. Same curse.
  - **Forgive him** (300 -> 310): he is freed. You get the Fox Spear. This route alone unlocks Under the Elder Tree.
  - Every route gives the mask and starts Loveletter to the Fifth Era.

**Act 7 - Loveletter to the Fifth Era (47A32B).** Use the ship's control unit. Enter **The Cave** where Ysmir "was born". Herkel speaks of Shor's wound.
Choose an offering to the **Shadow of Shor** (stage 30):
- a small offering -> stage 40-60 ("today you have accomplished something small, yet great"), or
- your own heart -> stage 140-160. The player's heart is torn out (controls disabled, knock-out). You gain the "Shor body" ability. Herkel: "you loved the people too much... everyone will forget you. Truly, you are a King among Kings."
Herkel is banished (50 or 150). Return to Skyrim (60/160). The cave exit (47A37C) leads out near High Hrothgar (47A380). Stage 900 -> **901 completes** when you are back.

**Epilogue - Under the Elder Tree (47A38C).** Only if you forgave the Woodland Man (Final Journey stage 310). Oohoo'Laf sits by a cairn under clear sky (stage 10). He gives you a secret story book his lord told him to hide (30). You read it and tell him what you thought (40). He envies the world (50, completes). "In time, your ladder will hang at the sky's rim."

**Epilogue Scenes (1EC845):** small ambient scenes once Lingering Snow is done: Lizz with Ulliss ("Mom, mom!"), Lizz with Fluffy, Lizz with Aisha. Snowballs, snowmen, swear words ("dovahshit").

#### Main NPCs

| Name | Who they are | Personality |
|---|---|---|
| **Ulliss** (zzzCrbCrossbreed) | Half-dragon girl. Made from dragon souls sealed in ice. | Gentle, shy, self-blaming ("with my horns and tail and all"). Grows braver. Offers to turn your dragon souls into stats (Dragon Souls 022986). |
| **Aisha** (zzzCrbWhiteCat) | Ulliss's white cat, a Khajiit-cat. Came "on a white ship" from "a white city by the sea". Also in GLENMORIL. | Rude, lazy, fiercely protective. Claws men she dislikes. "I'm an adult. Definitely." Rolls Fluffy in the snow. |
| **Fluffy / Ja'cobee** (zzzCrbKedamaSenpai) | A living snowball. Really Ja'cobee, last of the Chick Traders (prince of Anequina) from GLENMORIL, reborn with no memory. | Greedy merchant who loves "shiny coins", talks in third person, secretly soft. Raises Lizz. Sacrifices himself. |
| **Lizz** (zzzCrbCrossbreedDaugther_Child) | Ulliss's daughter from the far future, partly your dragon soul. | Proud, chatty child. "Lizz is the best snowball maker!" Says "Dovahkiin is an ignorant Dovah!", picks up bad words. |
| **Austella** | Ulliss's mother. A Nord girl of rumoured elven blood, chosen as a sacrifice "because of the frost". | Cold, regretful. Turned into an ice monster. |
| **Gray Owl** | A man who wore the name "Jhunal" for thousands of years. Made Ulliss. Main villain of acts 3-5. | Smug, "kind", grieving his "old companions". His dream: become a dragon and fly. |
| **Black Owl** | Offshoot of a Woodland Man of Hermaeus Mora. Also stalks GLENMORIL. | Cheerful tempter. "Such a happy ending. Wonderful, isn't it?" |
| **Herkel the Fool** | Clever Man from Ysgramor's time, your guide in Atmora. | Grumpy old lecturer, kind underneath. Slowly loses his mind to Apocrypha. |
| **Oohoo'Laf** | Woodland Man, Demi-Prince of Hermaeus Mora. | Proud, then tired and envious of the world. |
| **Jokul** | Snow Guardian (and the Last Atronach in the future). | Bored soldier, loyal. |
| **Orlando the Knowledgeable** | Trilogy-wide mysterious watcher (also in VIGILANT and GLENMORIL). | "We've met many times before." |
| Locals | Naghu the Gardener (tree-ent), Mudcrab Baron (hot springs), Tsua the Rat (tavern), Pot Baba / Pot Brat / Soul Gem Pot Merchant, Lord of Over Here and Snow Kanra (fox spirits), Mifa Xanadu (smith, making armor for "a little boy called Hjalti"), Wulf the Veteran (an avatar of Talos), the Hermit (painter, Austella's old advisor), Cawk the Dirtbird, whale children, Sina the Snow Mushroom, Arkved the Dreamer, Moff the dog (recruitable animal follower, topic 32A4C9). | Whimsical, sad-sweet. |

#### Places and realms

| Worldspace | FormID | What it is |
|---|---|---|
| Unslaad | 004E70 | Present-day hidden land. Castle Unslaad, hot springs, tavern, pot houses, Hermit's Tower, Cave of Radiance. Location 004E72. |
| Lost Unslaad | 064266 | Unslaad's future (Long Winter): ruins, Withered Forest, Dragon's Cradle. Location 064268. |
| Northern Sanctuary | 0A750C | Far future (Lingering Snow): Lizz's home, Mother's Tomb, Owl's Ridge, Haven, Frostwood. Location 0A750E. |
| Dragon's Peak | 32F628 | Mountain reached through Dragon's Throat. Location 32F629. |
| Joy-Snow Sky | 3F7859 | Sky above Atmora, snow whales. Location 3F785A. Start cell CrbAtmSkyStart 3FA0B2. |
| Frozen Abyss | 42AF9C | Atmora flooded by Apocrypha: Pillared City of H-Ram, Breeder Reactor Ruins, Mindoraan of Jhunal, Coma Pipe. Location 42AF9D. |

Key interiors: Castle Unslaad 00B86D, Chapel of Kyne 01370A, Bell Tower 0576E4, Guest Room 04FD2B, Dragon's Cradle 1C409A, Frozen Tomb 3C5DFB, Coldsalt Ruin 3D2F5E and Old City of Chains 3D8526 (both "Lyg"), Ysgrim's Seal 3FA243, Ysmir's Hearth 44E877, World-Eater's-Waking 453B00, The Cave 45662B.

#### Big twists
- Ulliss is a manufactured being: ice plus dragon souls, shaped by the Gray Owl.
- Fluffy is Ja'cobee from GLENMORIL. He chose Unslaad, raised Lizz, and gives his life to close the loop.
- Lizz is part your child (your dragon souls).
- The Blades who ruin Unslaad followed **your** trail.
- The undead Dov-Ah-Kiin is "one of the fates of the Dragonslayer".
- The Owls are offshoots of a Woodland Man of Hermaeus Mora sealed by Ysgramor. Your dragon name is Ysmaalithax, once given to Miraak.
- Mankar Camoran watches you through the Mysterium Xarxes (Watcher from the Third Era, 411777).

#### Links to the trilogy
- GLENMORIL: Ja'cobee, Aisha, young Ulliss ("I was walking with Aisha and there was a booming noise"), the Black Owl, Jhunal the owl, Hjalti from Alcaire, the Broken Egg.
- VIGILANT and GLENMORIL: Orlando the Knowledgeable ("in a lonely inn, in the Warrens, when you stood on the 'Blue Star'").
- Unsure: deeper VIGILANT plot links beyond Orlando.

---

### 2. Quest table

"Started" = how the quest begins. "Done" = the stage to test with `GetStageDone(quest, X) == 1` for a "this has happened" check. Objective text is from the OBJ list.

#### Main story

| EditorID | FormID | Name | Summary | Started | Key moments (stage) | Completed stage(s) |
|---|---|---|---|---|---|---|
| zzzCrbMq01 | 01D8FF | Falling Cat | Doll, cat dare, jump into Unslaad, meet Ulliss. | Delayed Start SM node at level 40 (stage 0 enables doll). Touch doll -> 10. | 10 "Talk to Aisha"; 15 "Jump off"; 20 landed in Unslaad, "Talk to Aisha"; 30 "Follow Aisha"; 40 "Talk to Ulliss" | **50** (also 9999 skip) |
| zzzCrbMq02 | 02299D | Hoarfrost | Enter castle, fight Austella, decide Ulliss's fate. | Falling Cat stage 50. | 10 "Find a way into the castle"; 20 key bought; 30 "Meet Ulliss' Mother"; 40 "Defeat Austella"; 50 "Decide Ulliss' fate"; 100 "Give the doll to Ulliss"; 200 "Check on Ulliss" (human end); 300 "Check on Ulliss"/310 "Defeat Ulliss" (dragon end) | **110** good end; **210** human end; **320** dragon end; 9999 skip (all lead on to 120/220) |
| zzzCrbSq02 | 05268B | Fluffy's Secret | Fluffy's twinkle star; his lost memories. | Talking to Fluffy (after Hoarfrost). | 20 starts Mq03 | **100** (set by Mq03 stage 30) |
| zzzCrbMq03 | 112A83 | When You Wish Upon a Star | Bell Tower, ghost scene, dragon ring, wish. | Fluffy's Secret stage 20. | 10 "Get the key to the Bell Tower"; 20 "Explore the Bell Tower"; 23-25 ghost scene; 30 "Wish upon a star" | **40** |
| zzzCrbMq04 | 117B3E | Long Winter | Ruined future, Aisha dies, Blades, Dragon Pus, souls into Ulliss. | Mq03 stage 40. | 0 "Travel to Unslaad's future"; 10 "Talk to Fluffy"; 15 "Find Aisha"/"Find Ulliss"; 30 Aisha dies; 40 "Defeat Blades Grandmaster"; 45 "Defeat Three-Headed Priest"; 55 "Defeat Dragon Pus"; 70 "Talk to the Owl"; 80 "Pour 10 Dragon Souls into Ulliss"; 90 "Talk to Fluffy" | **100** |
| zzzCrbMq05 | 117B3F | Lingering Snow | Far future, Lizz, Gray Owl, Dov-Ah-Kiin, bring Lizz home. | Mq04 stage 100. | 0 "Travel to distant future"; 10 "Talk to the child"; 20 "Follow Lizz"; 40 "Talk to Ja'cobee"; 50 "Head north"; 60 "Talk to the Gray Owl"; 80 "Survive the Gray Owl's attack"; 90 "Defeat the Gray Owl"; 105 blast; 110 "Find the Gray Owl"; 120 "(Optional) Kill the Gray Owl"; 130 "See one of the fates of the Dragonslayer"; 140 "Defeat Dov-Ah-Kiin"; 150 "Return to Ja'cobee"; 170 "Wait for Lizz"; 180 "Return to the present with Lizz"; 220 "Find Lizz"; 230 "Introduce Lizz to Ulliss" | **250** (journal: "Lizz was finally able to meet her mother. Ja'cobee's promise has been fulfilled.") |
| zzzCrbMq05Rush | 18F113 | Boss Rush | Monster waves + Owl monologues. | Mq05 stage 70; set to 1 at Mq05 stage 80. | 1/20/40/60/80 monologues; 70 big boss | **90** (sets Mq05 to 90) |
| zzzCrbMq06 | 1DFDFA | Stairway to Llesw'er | Fluffy's farewell and death. | Mq05 stage 250. | 0 "Return to Ja'cobee"; 10 farewell scene; 20 he dissolves; 30 "Retrieve Ja'cobee's remains" | **40** (Lucky Coin ability) |
| zzzCrbMq07 | 1DFDFB | The Owl Flies at Dusk | Black Owl's key, Dragon's Cradle, final fight with the Gray Owl. | Mq05 stage 250. | 0 "Examine the Mural of Jhunal"; 10 "Talk to the Black Owl"; 20 "Investigate Dragon's Cradle"; 30 "Send the ice doll into the future"; 50 "Light the brazier"; 70 "Defeat the Gray Owl" (phases 70-105); 110 Owl dead | **120**. Bad end 600-666 = game over, never "completed". |
| zzzCrbMq08 | 465EBF | The Final Journey | Atmora, Herkel, Lyg, Ysgrim's seal, Frozen Abyss, Pelinal, Woodland Man. | Player-only teleport from Dragon's Peak (needs Liturgy of I done); trigger 46873D sets stage 10. | 10 "Talk to Herkel"; 20 "Shout away the clouds"; 30 "Enter the mouth of the colossus"; 40 "Explore the Frozen Tomb"; 50 "Examine the ice seal"; 70 "Break the ice covering the mirror"; 90 "Bypass the seal of ice via the mirror" (Lyg); 105 "Break Ysgrim's seal of ice"; 110 "Explore the Frozen Abyss"; 135 "Defeat Pelinal"; 160 "Shout open the way to the ship's interior"; 180 "Search the ship's interior"; 185 "Settle the score with the Black Owl"; 190 "Finish off Oohoo'Laf with Unrelenting Force" | **195** Unrelenting route; **210** Alduin route; **310** forgive route |
| zzzCrbMq09 | 47A32B | Loveletter to the Fifth Era | The Cave, Shadow of Shor, offering, Herkel leaves, home. | Any Mq08 ending (195/210/310). | 0 "Examine the ship's control unit"; 10 "Search the Cave"; 20 "Talk to Herkel"; 30 "Choose an offering to the Shadow of Shor"; 40 small offering / 140 heart offering; 50 or 150 Herkel gone; 60 "Return to Skyrim" | **901** (900 when back in Skyrim) |
| zzzCrbMq10 | 47A38C | Under the Elder Tree | Forgiven Woodland Man shares a hidden story. | Mq09 stage 50 or 150, only if Mq08 stage 310 done. | 10 "Talk to Oohoo'Laf"; 30 "Read" the book; 40 "Talk to Oohoo'Laf" | **50** |

#### Side quests

| EditorID | FormID | Name | Summary | Started | Completed |
|---|---|---|---|---|---|
| zzzCrbsq01 | 022986 | Dragon Souls | Ulliss trades dragon souls for +10 Health/Magicka/Stamina or a perk point. | Falling Cat 50 | 10 |
| zzzCrbSqResurrection | 11023D | Revive | Undo a bad Hoarfrost ending. | Twinkle star + Dragon Ring + 1 dragon soul | 10 |
| zzzCrbSq03 | 33F0E0 | Arkved | Clear skies on Dragon's Peak. Arkved the Dreamer explains the Atmoran dreams. | Trigger after Mq07 done | 10 |
| zzzCrbSq04 | 364E2B | Snow Guardian | Shout apart Atmoran ice for Jokul. | Talk to Jokul | 20 |
| zzzCrbSq05 | 376B99 | Liturgy of I | 7 fragments, Loveletter, life choice, Black Owl taunt. Gate to the finale. | Hermit, after Mq07 + Sq04 | 160 |
| zzzCrbSqReopen | 2904BE | Reopen the Gate | Time doors reopen, Orlando appears. | Trigger after Mq07, carrying Gray Egg or Loveletter | 10 |
| zzzCrbSqRoadAtmora | 3C0D01 | Road to Amora | Light brazier; map markers to Dragon's Peak and Unslaad. | Brazier activator 3C0D02 | 10 |
| zzzCrbSqApoSafeRoom | 453AFA | Saferoom Unlock: Frozen Abyss | Rest rooms in the Frozen Abyss; pushes Mq08 to 120/125. | Ysgramor VS stage 40 | 30 / 40 |
| zzzCrbSqMankar | 411777 | Watcher from the Third Era | Mankar Camoran's projection hails you as Dagon's angel. | unsure (placed encounter) | 10 |
| zzzCrbqLessonKhev | 4073F0 | Sermon of Khev | Dreugh King's sermons in Lyg. | Activators in Lyg cells | 255 |
| zzzCrbEpilogue | 1EC845 | Epilogue Scenes | Family scenes after Lingering Snow. | Start-game enabled; trigger near the family | n/a (repeatable) |

#### Radiant jobs (repeatable, low story weight)
Rare Coin 350B8B (Fluffy), Intruder 350BA7 (Aisha), Amaranth Flower 3533FE (Ulliss, for her mother's grave), Picture Book 350B7F (Lizz), Ember of Atmora 34BAD8 (Mifa), Ice Tree 34926B (Naghu), Lost Kanra 3441D4 (Lord of Over Here), Infected 3676A3 (Jokul), Briarheart Brandy 3676B2 (Mudcrab Baron), Rogue Rat 369EFB (Tsua), Memento Collection 3719C1 (Pot Baba), Raging Pot 3719D3 (Soul Gem Pot), Dregs of Alduin 34E336 (Wulf), Woodland Man Hunt 48E803.
All complete at stage 20 or 30 (and 999 = cancelled/closed).

#### Boss "VS" quests (arenas; each locks a barrier and usually disables fast travel)
VS Idol of Magnar 409CE1 (Frozen Tomb, sets Mq08 50), VS Ysgramor 419232 (Ysgrim's Seal, sets Mq08 110), Trial of the Gods 3C8752 (Stuhn and Tsun, a falling bear), VS Dreugh King 407436 (Lyg), VS Jhunal Priest 47F4A9, VS Leopard 40C580, VS Snake 40C58A, VS Jill 01/02 40C5F1/40EE61, VS Giant of Jhunal 40C576.
Done = stage 20 (Ysgramor 40, Dreugh King 30, Jill01 30). While any of these is running, the player is in a boss fight.

Utility quests (never banter on these): MCM 2D441B, Safety 2F28B1, Generic 02012D, Training Mode 2E87A7, Act Skip 2D6C97 (an altar can skip whole acts - so do not assume every middle stage happened; prefer "quest completed" checks).

---

### 3. When follower banter must be silent

#### Simple rule set

Be silent when ANY of these is true:

**A. Worldspaces where an ordinary follower is almost never present** (see section 4):
- `GetInWorldspace 3F7859` (Joy-Snow Sky)
- `GetInWorldspace 42AF9C` (Frozen Abyss)
- Interior cells of the Atmora journey: Frozen Tomb 3C5DFB, Coldsalt Ruin 3D2F5E, Old City of Chains 3D8526, Ysgrim's Seal 3FA243, Ysmir's Hearth 44E877, World-Eater's-Waking 453B00, The Cave 45662B.
  Simpler: `GetQuestRunning 465EBF == 1` (Final Journey) or `GetQuestRunning 47A32B == 1` (Loveletter) **and** not in Tamriel.

**B. Cutscenes and scripted moments (quest stage windows):**

| Quest | Silent while stage is | Why |
|---|---|---|
| Falling Cat 01D8FF | 10-19 at High Hrothgar | Aisha's dare; the jump. Optional. |
| Falling Cat 01D8FF | == 30 | Aisha leads you to the castle (scene 022976). |
| Hoarfrost 02299D | 30-60 | Austella's boss room and the doll choice. |
| Hoarfrost 02299D | 200-220 and 300-320 | Ulliss dies / dragon fight. |
| When You Wish 112A83 | 23-25 | Bell Tower ghost scene (cell 0576E4). |
| Long Winter 117B3E | 55-60, 70, 90 | Dragon Pus fight, Owl scene, Fluffy scene. |
| Lingering Snow 117B3F | 5, 20-40 | Grave scene, Lizz's guided walk, Ja'cobee scene. |
| Lingering Snow 117B3F | 80-110 | Boss Rush, Owl fight, Magnus blast, **controls disabled**, ghost walk. |
| Lingering Snow 117B3F | 140-150 | Dov-Ah-Kiin fight. |
| Lingering Snow 117B3F | 160-190, 240-250 | Prepare/farewell scenes; reunion. |
| Boss Rush 18F113 | running | Waves plus monologue scenes. |
| Stairway 1DFDFA | 10-30 | Fluffy ascends. |
| Owl Flies at Dusk 1DFDFB | 60-120 | Brazier, 4-phase dream fight, farewell. |
| Owl Flies at Dusk 1DFDFB | >= 600 | Bad end: controls off, then the game quits. |
| Final Journey 465EBF | 130-140, 170, 180-210, 300-310 | Pelinal fight, Ysgramor vision, Woodland Man choice, Alduin cutscene (controls off at 200). |
| Loveletter 47A32B | 20, 140-150 | Herkel scene; heart torn out (**controls disabled**). |
| Under the Elder Tree 47A38C | 10-20 | Oohoo'Laf monologue (scene starts on quest start). |
| Liturgy of I 376B99 | 110-120, 150-160 | Letter restoration scene; Black Owl appearance. |
| Snow Guardian 364E2B | == 20 | Short scene. |
| Any VS boss quest | running | Arena fight. |

**C. Dream sequences**
- The Gray Owl fight in Owl Flies at Dusk (stages 70-110) happens "inside his dream".
- The bad-end nightmare (stage 610, scene 208513).
- The whole Atmora/Lyg/Frozen Abyss journey is dream-memory ("frozen dreams of the Atmorans").

**D. Forced transports (player moved, follower may be left or warp in late)**
- Falling Cat 15 -> 20: the jump. Fall trigger 04ACF1 moves the player AND any follower (CurrentFollowerFaction, teammate or UnslaadFaction) that **enters the trigger**. A follower who does not jump stays on the ledge.
- Lingering Snow 30: if far away, the player is moved to Ja'cobee.
- Lingering Snow 105: player moved to the survive marker after the blast.
- Lingering Snow 220: through the time portal with Lizz.
- Dragon's Peak -> Joy-Snow Sky: trigger 3CB45C (CrbDragonPeak00) moves **only the player** to marker 3FA222.
- Loveletter 140: player moved to a knock-out marker.
- Owl Flies at Dusk 600: player moved to the bad-end marker.
- Safety fall triggers in Lyg, the Frozen Abyss, Dragon's Throat and Northern Sanctuary catch falling player/followers and move them back up.

**E. Hard gate**
Never let a banter line fire between Owl Flies at Dusk stage 30 and 40 that could distract the player. Stage 40 decides bad end vs good end. (The decision is automatic, but it is a tense moment.)

---

### 4. Can ordinary followers come along?

| Place | Can a normal follower get there? | Evidence |
|---|---|---|
| **Unslaad** (004E70), first visit | **Only if they fall too.** Usually no. | Entry is a cliff jump. Trigger 04ACF1 (base zzzCrbSafetyFallTrg 04ACF0, script CrbActSafetyFallingScript) teleports the player and any actor in CurrentFollowerFaction, teammate or UnslaadFaction who touches it. Vanilla followers do not jump off cliffs. Unsure for framework followers that teleport to the player. |
| **Unslaad**, later visits | **Yes.** | Normal load door 020129 (Skyrim, below the High Hrothgar ledge) <-> 020128 (Unslaad), enabled at Falling Cat stage 15. Followers use load doors. |
| Unslaad interiors (castle, tavern, pot houses, trials) | Yes. | All normal load doors. |
| **Lost Unslaad** (064266) | Yes. | Normal door 0F1BA9 in the Guest Room <-> 0F1BA8 (opened at When You Wish stage 40). |
| **Northern Sanctuary** (0A750C) | Yes. | Doors 1AFD8D <-> 16E445 and 0F1BA1 <-> 0F1B9C. Safety fall triggers there list followers. A "time paradox" door blocker (0AC755) only blocks Lizz. |
| **Dragon's Peak** (32F628) | Yes. | Door 334999 (Unslaad) -> Dragon's Throat -> 33499C. |
| **Joy-Snow Sky** (3F7859) | **No (normally).** | The only way in is trigger 3CB45C, script CrbTeleportToEndActTrgScript: `if Target == Game.GetPlayer() ... MoveTo(TeleportMarker)`. Player only. Followers are left on Dragon's Peak. |
| **Frozen Tomb, Lyg, Ysgrim's Seal, Frozen Abyss** (42AF9C), the ship, The Cave | **No (normally).** | Reached only from Joy-Snow Sky. The mod still placed follower-aware safety triggers there, so a follower that is somehow present will not be killed by falls. The final exit (47A37C -> 47A380) returns you near High Hrothgar, so a follower left on Dragon's Peak is not with you at the end. |

Short version: followers can share acts 1-5 and the side quests. The jump in act 1 and the whole act 6-7 finale are player-only.
Also: the mod has its own recruitable animal follower, Moff the dog (vanilla animal follower system).

---

### 5. Fifteen banter hooks (D&D-party feel)

Each line: situation -> trigger.

1. **"You want us to jump?"** The party stares at the cat on the ledge. -> Falling Cat stage == 10 or 15, follower near the doll.
2. **The reunion at the door.** A follower who stayed behind finally walks into Unslaad: "You JUMPED. Off a mountain. For a cat." -> First time follower `GetInWorldspace 004E70` and Falling Cat completed (GetStageDone 01D8FF 50).
3. **The 1000-gold key.** Party treasurer outrage at Fluffy's price. -> Hoarfrost GetStageDone 02299D 20.
4. **What did you do to her?** Choice fallout. Good end: warm; tail torn: grief and blame; burned: horror. -> GetStageDone 02299D 110 / 210 / 320.
5. **Haunted bell tower.** The rogue-type wants to loot, the cleric wants to leave. -> When You Wish stage 20, in Bell Tower cell 0576E4.
6. **"How long were we gone?"** Shock at the ruined future. -> Long Winter stage 10-15, in Lost Unslaad 064266.
7. **The Blades came because of us.** Guilt argument; a Blades-friendly follower gets defensive. -> GetStageDone 117B3E 70 (Owl's explanation), or Long Winter completed.
8. **Aisha's grave.** The party remembers the rude cat kindly. -> GetStageDone 117B3E 30.
9. **"Is that kid yours?"** Teasing the Dragonborn about Lizz. -> Lingering Snow stage 40-100 (Lizz and Ja'cobee in Northern Sanctuary 0A750C).
10. **Babysitting duty.** Lizz chews things, is a restless sleeper; the party splits chores. -> Lingering Snow stage 190-220 (escorting Lizz).
11. **Looking at a dead Dragonborn.** "That could be you." Deep talk about fate. -> GetStageDone 117B3F 150.
12. **Fluffy's goodbye.** Toast to the stingiest friend they ever had; someone flips the Lucky Coin. -> GetStageDone 1DFDFA 40.
13. **Snowball fight.** Lizz hands out snowballs; competitive follower wants a rematch. -> Lingering Snow completed and near the epilogue family (Epilogue quest scenes not playing).
14. **"You're going up there alone?"** At the Dragon's Peak summit, the follower realises they cannot follow. -> Liturgy of I completed (GetStageDone 376B99 160), in Dragon's Peak 32F628.
15. **What happened up there?** On return the follower asks; lines differ by ending: Unrelenting Force (195), Alduin (210), forgiveness (310); and by Loveletter heart offering (GetStageDone 47A32B 140: "You seem... emptier"). -> Loveletter completed (GetStageDone 47A32B 901) and back in Tamriel.

Bonus small hooks: the 1000-septim Fluffy jokes, Pot Brat calling the follower "wimp", Mudcrab Baron boiling himself in the hot springs (Hidden Hot Springs 320187), the rat's tavern under the bridge (Chow-Chow Tavern 32CD2F).

---

### Unsure list
- Exact location of Watcher from the Third Era (Mankar) encounter.
- Whether follower frameworks with "teleport to player" pull followers into Joy-Snow Sky or Frozen Abyss.
- Exact physical trigger for Lingering Snow stage 101/102/103 (three bomb scene variants; likely dialogue choices to the Owl).
- Exact meaning of Loveletter stage 40 offering (the non-heart choice); dialogue for it is not in the dump.

---

## D. Gore - Vigilant.esp (Gore's own VIGILANT chapter)

Plugin: `Gore - Vigilant.esp` (C:\1. AUTHORIA\mods\Gore). It is Gore's author's add-on that writes Gore into VIGILANT.
It does **not** change any VIGILANT quest. It runs on its own: one start-game quest, 76 scenes, about 100 trigger boxes placed in VIGILANT's cells, and 3 extra "Gore" NPCs for Coldharbour.
FormIDs below are `XXXXXX:Gore - Vigilant.esp` unless another plugin is named. Runtime prefix is 26.

### D1. Its two quests

| EditorID | FormID | Name | What it is | Started | Done |
|---|---|---|---|---|---|
| HD1GoreVigilant | 00704E | (no name) | Holder for all of Gore's VIGILANT scenes and lines. Start-game enabled, only stage 0. Its script `HD1GoreCH1Controller` runs the three Coldharbour Gores. | At game start. Never completes. | never. Do not test its stage. |
| HD1MemoriesQ | 0C6188 | Fading Memories | Coldharbour: find Gore's lost memories. Journal stage 0: "I awoke in Coldharbour and found that Gore has come as well... speaking with him seems to be useless. I may be able to restore some of his memory..." Stage 10: "I have restored some of Gore's memories, but it seems as though I have one more..." | When the player meets the soul-shriven Gore in Coldharbour. | **Stage 20** (quest completes; set when the player reaches Aetherius). Objectives 0, 10, 20 = "Find Gore's first / second / third memory", 30 = "Find Gore's final memory". |

It also overrides Gore's own quests HD1GoreFollows (066722:GORE.esp), HD1GoreDawnguard (7FADBA:GORE.esp) and HD1GoreFearAndLoathing (AFF592:GORE.esp). Gore - Vigilant.esp is the live winner of HD1GoreFollows, so its version of Gore's follower quest is the one running.

### D2. Story-state globals it uses (GlobalShort, all in Gore - Vigilant.esp)

| Global | FormID | Meaning (from the scripts and dialogue conditions) |
|---|---|---|
| HD1VAct3 | 052081 | 1 = Act 3 began: Gore vanished in the Bruiant mansion (he is held off-stage). Stays 1 afterwards. |
| HD1MainBoxed | 0316BA | 1 = the real Gore is boxed away (in his holding cell). 0 = he is back. |
| HD1CH1Boxed / HD1CH2Boxed / HD1CH3Boxed | 0316BB / 0316BC / 0316BD | 0 = that Coldharbour copy of Gore is out and following. 1 = put away. Default 1. |
| HD1MemoriesRestored | 0AF3FA | Count of memories restored in Coldharbour. 3 or more when the final memory is touched = Gore is saved. 0-2 = Gore is lost (see D5). |
| HD1CHMet | 10A941 | 1 = player has talked to the soul-shriven Gore. |
| HD1WTCHVar | 02AE4E | Used at the end: == 2 is "we made it" / the after-Coldharbour talk. |
| HD1VAct2Var | 251CCC | Act 2 (Blood Matron): 1 = talk before the Matron's room, 3 = "let's talk when we get back", 4 = the Act 2 wrap-up talk. |
| HD1Act2Start | 217173 | 1 = Act 1 recap talk is available ("Congrats on the whole... leader of the Vigilants thing"). |
| HD1MBVisions | 1F9BDF | 1-5 = Molag Bal's vision attacks on Gore during Act 1 (he groans, sees a mother and daughter, flaying). |
| HD1MBR | 183378 | Molag Bal realization at the shrine. 1 = talk pending. 3 = **player told Gore to go** ("Go, then.") and he left; later he apologises ("I abandoned you"). |
| HD1VWitches | 17FF3F | 1 = Gore's "I am not a murderer any more" talk about the witches is pending. |
| HD1CatDream | 19D4FD | 1 = Gore also lived Jo'vanni's death dream. |
| HD1VWitchKilled | 20D4F8 | Reyda the hagraven killed (1) or spared. |
| HD1WitchesAlerted, HD1WitchToCH, HD1CowerInFear, HD1MetBrokenGore, HD1WTCHVar2, HD1WTCHVar3 | 1F67B4, 1B767A, 2A14BD, 01DDAB, 03169F, 0316A0 | Small helper flags. HD1CowerInFear = Gore is cowering at the shrine. |
| HD1NoTeleport | B296F7:GORE.esp | 1 = Gore's catch-up teleport is off. |

### D3. What Gore's chapter does, beat by beat

Every scene below starts only if **Gore is following** (CurrentFollowerFaction) when the player walks into a trigger. Most also need a VIGILANT quest at an exact stage. Each fires once.

**Act 1 - the Vigil and Altano (VIGILANT main quests zzzAoMMq00-10)**
- Windpeak Inn, Dawnstar, after zzzAoMMq00 stage 10: scene HD1GoreVigilantALTANO. Gore: "Something's not right about that guy... we do not want to get mixed up with these people."
- Entering Stuhn Ravine: HD1GoreVigilantSTUHN. "Guess I can't talk you out of this, then? Alright. Vigilants, then."
- Temple entrance, zzzAoMMq01 stage 10: ASSIGNMENT. Whiterun Wind District at stage 20: VAMPIRE ("A vampire, huh? In Whiterun...? We should go get drinks and tell him we couldn't find anything"). Hall of the Dead: VAMPIRE2.
- zzzAoMMq02 stage 10: HOMESTEAD ("Hasn't this home been through enough?").
- Candlehearth Hall, zzzAoMMq03 stage 20: CANDLEHEARTH. Outside Candlehearth, zzzAoMMq04 stage 40: EYES. Bee and Barb, zzzAoMMq05 stage 22: BARFIGHT ("Oh, for Mara's sake... at least this one's awake!").
- zzzAoMMq06: Gore does not enter Jo'vanni's Dream Theater (HD1NoTeleScr), but he **shares the dream**: back in the Ratway Warrens at stage 60 (HD1CatDreamReturn) he wakes from "the most horrible dream... I think I died". Later: "I dream through the eyes of a Khajiit being skinned".
- Molag Bal's visions (HD1MBVision1-5): Gore groans "Ngh..." and sees "a Mother and Daughter... I feel like he's marked me".
- Altar of Molag Bal under the temple, after zzzAoMMq07 is done and zzzAoMMq08 has started: HD1GoreDontWalkAway / HD1GoreMBShrineTopic. "A bonafide shrine to Molag tusking Bal, located conveniently right underneath the beacon of tusking Stendarr!" Then HD1GoreVMOLAGREALIZATION: he panics ("please don't make me go in there"). Player choices: reassure him, say "we can't walk away", or **"Go, then."** (he leaves for a while; HD1MBR = 3).
- Witch's Pond (zzzAoMMq08): entry and fog scenes, then the witch house. Gore refuses to kill: "I am not a murderer, anymore. I will not keep doing Molag Bal's bidding on your behalf." Sparing the witches: "Blood, thank the Gods you have senses. Those were not witches, no chance. Altano has some explaining to do..." Killing them: "Oh, Gods... what have we done?! I told you..."
- zzzAoMMq09: stage 20 HD1ChaseAltano in the temple; stage 32 HD1ChaseAltanoCHamber ("We are here to kill Altano... Steel yourself, blood"); at stage 40 Gore fights the shade of Molag Bal ("You... you did this! I will never kneel to the defiler...").
- zzzAoMMq10: stage 10 HD1MaceDestroyer, stage 30 HD1ItIsSoOverBros ("you and I just defeated a shade of Molag... Molag Bal himself...!"). Art of Mercy route (zzzAoMMqGoodEnd) stage 0 and 110: the Mother (Carene) scenes ("Thank you... for sparing her. I know what it's like to lose both of your parents").
- Act 1 recap talk (HD1Act2Start == 1, at the temple entrance when zzzBMMq01 is at stage 10): dream, shrine, the witches, Altano, "We killed Molag Bal!" ("We most certainly... did not"), and Reyda.

**Act 2 - The Blood Matron (zzzBMMq01-03, Windhelm)**
- zzzBMMq01 stage 10 HD1GoreVBMStart ("are we really about to rush headfirst into the next crisis?"); stage 40 HD1GVBMLibrary ("I still don't quite know how to read"); stage 60 HD1GVBMReturnToWH.
- Windhelm Dungeon, Hidden Passage, Old Windhelm Slums and City, Bloody Well, Asylum: about a dozen walk-and-talk scenes (dungeon entry, the reeking statue, skeevers, the maze, "abominations", a mercy kill). Inside these cells Gore uses special combat and hello lines ("Tusk, you scared the piss out of me").
- Enchantress' Palace: he gets **locked out** of a shrine room and pounds on the door ("Blood! ... I'm coming! ... don't die...!"); HD1GVBMFG talk before the Matron (HD1VAct2Var 1): "they suffered... Whatever is in that room, blood, it is the reason."
- Matron's Chamber: HD1GVBMMatronIntro ("It's... a young woman... she's dead... Blood?!"). zzzBMMq03 stage 70: "I saw... Lamae was a victim... never speak of it again." Then HD1GVBMEndRespects at Lamae's coffin ("Rest, please. You deserve peace.").
- Back at the temple entrance after zzzBMMq03: HD1GVAct2EndingConvScene ("It's not my story to tell... I'm ready for whatever comes next").
- Side beat: once zzzAoMMq10 or Art of Mercy is done and zzzBMMq01 is at 10+, at Witch Island he confronts the hagraven **Reyda** (HD1VWitchRevenge). Kill: "Good riddance... one less hagraven in the world." Spare: "Seriously?! Why... Why let her live?! What is wrong with you?!"

**Act 3 - Child of Oblivion and Coldharbour**
- Bruiant Estate gate (cell COBruiantEntrance 047CFD:Vigilant.esm): HD1GVCOOOutside. "Got a really bad feeling about this place, blood... Look at how much we've accomplished... I'm so proud of you."
- **Inside Bruiant Mansion South Wing (cell zzzCONobleMansion01 04A8B9:Vigilant.esm), trigger 052082: Gore vanishes.** Script HD1VigilAct3Scr dismisses him, moves him to the holding cell HD1GorsePrison (43DD6A:GORE.esp), turns his teleport off, sets HD1VAct3 = 1 and HD1MainBoxed = 1, and arms the martyr trap in the Temple of Stendarr. From here the real Gore is gone until Coldharbour. In the cursed mansion rooms the player hears Gore's voice as echoes (HD1EchoPlayerScr in cells zzzCONobleMansion01/02/03/04BE, zzzCOCursedRoom01/02/04, zzzCONobleMansionBasement).
- His later explanation (HD1GoreVE2): "You went off into the mansion, I followed right behind you, and you were just... gone... I exhausted every book in the Vigilant's possession... I learned to read, blood. It took me months... The Defiler came to me, made me an offer. All I had to do was follow."
- **Coldharbour.** At Mathmalatu Priory (cell zzzCHWaterFrontChapel 07FB11:Vigilant.esm) the player finds a **soul-shriven Gore** (a separate NPC, HD1GoreCH1 0316AE, ref 0316B1). He follows as a dazed companion ("Cold... harbour... blood, we died... I died. I'm sorry..."). Fading Memories starts.
- Memories (each a short memory-chamber scene with player controls taken):
  - Fort Welkynd (zzzCHFortWelkynd01 0E2693:Vigilant.esm) -> chamber "Strategies" (0753AC): young Gore humiliated by Jo-Lee ("You're 'Gore,' not a cavalry lieutenant"), Pate's "whipped pup", and the officers' pay scene.
  - Chapel of Arkay Cemetery (zzzCHArkayChurchyard 0C8FCF:Vigilant.esm) -> "Religion" (0C611C): J'hul the Khajiit tells him Hircine was once an Aedra; Gore gets drunk and sick.
  - Coldharbour Slums (zzzCHSlum01 0EDDF6:Vigilant.esm) -> "Blame" (0C6133): the Pate memory.
  - Other chambers: "Blooded" (0C614A), "Love" (0C6161), final "Mother" (08EA52).
  - After each memory the follower copy changes: CH2 (0316AF) is a cadet ("Drills in the morning... get some rest"), CH3 (0316B0) thinks the player is Pate ("Stop it, Pate").
- Final memory in the Coldharbour tower Sancremor Angasel (zzzCHTowerSM04 121AA2:Vigilant.esm): his mother **Heidi** sings to him. If enough memories were restored, the **real Gore comes back** (HD1GoreRestoredScr): "Blood...! You saved me! That was my Mother... I'm so sorry that I followed you here... but I'm not afraid any more!" He is a normal follower again for the rest of Coldharbour (teleport back on).
- Aetherius (cells zzzCHAetheriusGood 1353E4 / zzzCHAetheriusBad 136194:Vigilant.esm): HD1Aeth, Gore says "Aetherius..."; Fading Memories completes (stage 20).
- After the ending: HD1EndingVig ("I've never been so happy to see the sun setting... Gods, it's over.") and the long "Are you okay?" talk (HD1WTCHVar == 2): his personal hell, his mother's song, "I would have died for you", "I love you, blood. Truly", "We keep going."

### D4. Things banter must never contradict

- Gore **dislikes the Vigilants** from the first minute ("wack-jobs", "milk-drinkers", "bad at their jobs") and suspects Altano early. He never becomes a Vigilant fan, even after the player leads them.
- He is **terrified of Molag Bal**. Before Coldharbour, any Molag Bal talk from Gore should be fear. After his rescue he says he is "not afraid any more" and "stronger from it". Keep that change.
- He refuses to kill people who may be innocent ("I am not a murderer, anymore"). He wanted Reyda dead, though. He is not a pacifist about monsters.
- He **cannot read during Act 2** ("I still don't quite know how to read"), and **learns during the months he searches** for the player (Act 3). Do not have him read anything before Act 3.
- He knows the player saw his worst memories (Jo-Lee, Pate, his mother).
- He **shared Jo'vanni's death dream** and was in Lamae's nightmare.
- Inside Coldharbour the real Gore is **not** with the party until the final memory; a different NPC stands in.

### D5. The two ways to lose Gore for good (banter must handle both)

1. **Martyr ending.** If the player picks "Die in flames as a martyr" in Child of Oblivion (zzzCOMq01 stage 200; the player's character dies and the player continues as a new character in Successor, see section A), a trigger in the Temple of Stendarr (1903F6, armed at Act 3 start) disables every Gore and enables a broken Gore at the Dragon Bridge lumber mill (placed ref 1903F7, base HD1GoreBroken 01A96D). Message: "Your Dragonborn is now dead. Gore will no longer be a part of your game..." The broken Gore does not believe the player is who they claim ("You are not... [name]. You need to leave"), blames the Vigilants for killing his best friend, and has lost his sword arm.
2. **Memories not restored.** If the player touches the final memory with fewer than 3 memories restored (HD1MemoriesRestored 0-2), the real Gore is disabled and a "Soul-Shriven" Gore (HD1GoreSoulShrivenState 0C61A1, ref 0C95C9) is enabled instead. Gore is lost to Coldharbour.

Simple check for both: the real Gore ref **HD1GoreRef 00B4B1:GORE.esp IsDisabled() == true** -> treat Gore as gone, no Gore talks, and other followers may mourn him (carefully: in case 1 they do not know what happened; in case 2 they saw it).

### D6. Gore - Vigilant states to block (add to Gore's busy rules; matches others_block.md section 1)

Block **all** banter (not only Gore's) when:
- Any HD1GoreVigilant scene is playing. Easiest: Gore `IsInScene() == true` or the player is in a scene. All 76 scenes are in quest 00704E.
- `GetQuestRunning HD1MemoriesQ (0C6188) == 1` (Coldharbour memory hunt).
- Player in a memory chamber: cells 0753AC, 0C611C, 0C6133, 0C614A, 0C6161, 08EA52, 057E29 (all Gore - Vigilant.esp).
- Player in Matron's Chamber 034E12 or Enchantress' Palace 033B80 (Vigilant.esm) while zzzBMMq03 is not completed (Gore's palace scenes and boss fight).

Block **Gore as a speaker** when:
- `HD1MainBoxed == 1` or `HD1VAct3 == 1 and Gore not in CurrentFollowerFaction` (he is in the holding cell).
- `HD1MBR == 3` until he is following again.
- Gore is in cell HD1GorsePrison 43DD6A:GORE.esp.
- HD1GoreRef is disabled (D5).
- `HD1VAct2Var == 3` ("Let's talk when we get back. Give me a minute") and `HD1VAct2Var == 4` before the wrap-up talk was had.
- `HD1WTCHVar == 2` until the ending talk was had (let his own "Are you okay?" talk land first). There is no "talk done" flag, so use a cooldown after Child of Oblivion completes (see VIGILANT section).

Do **not** write banter for these moments, because Gore already has a scene there (collision list):
Windpeak Inn after Vigilant start; Stuhn Ravine entrance; each AoM quest at the stages listed in D3; the Altar of Molag Bal after Old Regrets; Witch's Pond; Altano chase; Mace destroyed; Mother spared; Act 1 recap at the temple entrance; every Blood Matron dungeon cell; Reyda at Witch Island; Bruiant Estate gate; Bruiant mansion; Coldharbour from the Priory to Aetherius; the ending.

Good gaps that Gore's chapter leaves open (safe for new banter): travel between assignments, Stuhn Ravine camp life, the days between Act 1 and Act 2, other followers reacting to **Gore's** fear of Molag Bal, and other followers noticing Gore is **missing** during Act 3 (while HD1VAct3 == 1 and HD1MainBoxed == 1, outside Coldharbour). Keep them consistent with his own later story: he was "just gone", searched for months, learned to read, and was lured by a dream.

---

## E. Our 8 followers and these mods

### E1. Who can actually come along (all three mods together)

| Place | Kaidan | Gore | Val | Remiel | Xelzaz | Inigo | Lucien | Redcap |
|---|---|---|---|---|---|---|---|---|
| VIGILANT Skyrim job sites, Temple of Stendarr (Stuhn Ravine), Witch's Pond, Windhelm dungeon, Bruiant Estate grounds | yes | yes (and he has his own scenes) | yes | yes | yes | yes | yes | yes |
| VIGILANT dreams (Jo'vanni's Dream Theater, Lamae's Dream from stage 20 of The Blood Matron, Dark Tunnel), Coldharbour, memories, Aetherius, the Abyss | no (left in Skyrim; only if his MCM teleport is on could he warp in) | **special**: the real Gore is taken away in the Bruiant mansion. A soul-shriven copy follows in Coldharbour. The real Gore rejoins at the final memory (tower Sancremor Angasel) and follows to the end. | no (catch-up could warp him, unsure) | no | no | no | no | no (catch-up could warp him, unsure) |
| VIGILANT Successor route (new character) | they knew the old Keeper | Gore is gone for good (see D5) | as Kaidan | as Kaidan | as Kaidan | as Kaidan | as Kaidan | as Kaidan |
| GLENMORIL Falkreath, Blessed Glen, Witch Hunter HQ, airship missions (Ebonwall, Cradle Woods, Ysmir's Howl, Vahdin Holt, Piper's Hill) | yes by door, but each mission ends with a player-only teleport, so they must catch up | yes | yes | yes | yes | yes | yes | yes |
| GLENMORIL dreams (Black Owl dreams, Quagmire dream rooms, Jhunal's library, Room of Love, Dreamsleeve, Shattered Mirror), the Hinnom falls, the Act 4 boat to Svartibrunnr | no (player-only teleports; Svartibrunnr arrival unsure, so gate on the follower's own worldspace) | no | no | no | no | no | no | no |
| UNSLAAD: first jump | only if he jumps into the same trigger (rare) | same | same | same | same | same | same | same |
| UNSLAAD later visits, Lost Unslaad, Northern Sanctuary, Dragon's Peak | yes (load doors) | yes | yes | yes | yes | yes | yes | yes |
| UNSLAAD Joy-Snow Sky, Atmora, Frozen Abyss, the ship, The Cave | no (player-only teleport) | no | no | no | no | no | no | no |

Rule of thumb: in the mods' own realms, assume the party is **not** there, even if a catch-up teleport put one of them there by accident. Write "where were you?" banter for the return instead.

### E2. Lines our followers already have about these mods

Searched every dialogue line in GORE.esp, Gore - SaSEC.esp, 0Kaidan.esp, BWB - Kaidan 2 Extra Dialogue.esp, Kaidan - Immersive Features.esp, Kaidan and Inigo Meet.esp, AX ValSerano.esp, HLIORemi.esp, HLIIRemiLOTD.esp, BPUFXelzazFollower.esp, Xelzaz - Inigo Patch.esp, Inigo.esp, Lucien.esp and FA01RedcapFollower.esp (58,775 lines) for Vigilant, Glenmoril, Unslaad, Stendarr, Molag Bal, Coldharbour, soul-shriven, Namira, Hircine, Atmora, High Hrothgar and the main NPC names.

**Result: none of these plugins conditions a single line on Vigilant.esm, Glenmoril.esm or Unslaad.esm.** The only follower content that knows about these mods is Gore - Vigilant.esp (section D). Everything else is general lore or the vanilla Vigilants. Topics only:

| Follower | Existing topics that touch these mods' themes |
|---|---|
| **Gore** (GORE.esp, outside the Vigilant add-on) | Dislikes Stendarr's "obnoxious vigilants"; a joke about a Vigilant's locked-up house; fear and hatred of Molag Bal ("the prince of rape, torture"); "Don't let them send you to Coldharbour... I'd venture there myself and drag you from Bal's clutches" (this comes true in Gore - Vigilant); Coldharbour as the vampire's fate (Dawnguard talks); Namira is foul; the Khajiit tale that Hircine was once an Aedra (same story J'hul tells in his Coldharbour memory); Fear and Loathing (House of Horrors, Molag Bal). Two idle lines use the word "Unslaad" ("Season Unending is upon us, Unslaad", "Not a good omen of Unslaad, blood") as a seasonal or omen word, not about the mod. |
| **Kaidan** (0Kaidan, Kaidan 2 Extra Dialogue, Immersive Features) | "Not like those Vigilants I hope? ... Stendarr is a God of merciful justice. They're using him to validate their hunting of Daedra" (his view of the Vigilants); Dawnguard-era Vigilant attack comments; "Molag Bal is the god of schemes"; oaths "Stendarr's mercy on me", "Stendarr's nuts", "Molag's balls"; Atmora and Ysgramor musings; wanting to make the High Hrothgar pilgrimage. |
| **Val Serano** | His own Molag Bal story (Fathis's soul in Molag Bal's cursed soul gems, the cursed amulet); "These Vigilants just can't hold their liquor"; "lucky the Vigilants of Stendarr don't have a guild hall in Solitude"; oath "Molag's Balls"; Namira/Sheogorath cheese joke. |
| **Remiel** | Shock at the player's dealings with Molag Bal in the House of Horrors; "Molag Bal is the father of vampires"; the Stendarr-worshipping Vigilant in Markarth "aggressive in his questioning"; "By Stendarr" oaths; the song "The Coldharbour Compact". |
| **Xelzaz** | Full House of Horrors commentary (the Vigilant Tyranus, the shrine, "I do not want to do his bidding"); his own past brush with a Molag Bal shrine on a Telvanni expedition; worry about Serana's vampirism and Molag Bal; "Seems we've stumbled upon a Vigil of Stendarr" (Rift); "The fires of Coldharbour await!"; Namira's faithful. |
| **Inigo** | Only "I hope Molag Bal doesn't mind me using his mace." No Vigilant, Coldharbour or Stendarr opinions. |
| **Lucien** | Lore: Molag Bal's Planemeld in the Second Era, his ancestor Octavius who "wasn't the best of friends" with Molag Bal; Reachmen helping Molag Bal; casting Stendarr's Aura in training; Hircine and werewolf lore; Atmoran hero Morihaus naming Morthal (Morihaus is also a VIGILANT memory character). |
| **Redcap** | Only Hircine (Skaal and wereboar quests). Nothing about Vigilants, Molag Bal or Coldharbour. |

Writing notes from this:
- Kaidan and Gore both start out **anti-Vigilant**, for different reasons (Kaidan: they misuse a merciful god; Gore: they are fools who draw Daedra). Good pairing for VIGILANT act 1.
- Val, Xelzaz, Remiel and Gore all have **personal Molag Bal history**. Lucien knows the lore. Inigo and Redcap have none, so they can be the ones asking.
- Gore's old line "I'd venture there myself and drag you from Bal's clutches" is paid off in Gore - Vigilant (he follows the player to Coldharbour). Other followers can tease or honour that after the Vigilant ending.
