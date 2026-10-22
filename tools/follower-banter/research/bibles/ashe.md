# ASHE - character sheet (for the follower-banter mod)

Built from her own plugins in the live load order (profile DEEZ CS NUTZ - PICTA), read-only, 2026-10-18:
- `Ashe - Fire and Blood.esp` (mod folder `Ashe - Crystal Heart`, "Ashe - Crystal Heart" 1.3.6a by Martimius, Nexus 135085).
- `Ashe and Serana Banter Patch.esp` (folder `Ashe - Crystal Heart - SDA`, 1.0.10, Nexus 167123). Needs Serana Dialogue Add-On.
- `Ashe Inigo Compatibility Patch.esp` (folder `Ashe - Crystal Heart - Inigo`). It has **no dialogue** (see section 5).
- `Ashe Impressionist Patches.esp`, `Ashe RCO Patch.esp`, `Ashe - SMP_Hair.esp`, `Ashe Combat Nerf Patch.esp`, `Ashe - Visual Replacer.esp`, plus Authoria's own Reqtificated, Seasons, Lux, JK, Northern Roads and Riverwood patches. None of these add Ashe dialogue.
- `Eleonora - Ashe.esp` is the **player's** DBVO voice for Ashe's dialogue menus. It is not Ashe.

A line counts as hers only when an `mm_ashevoice` file exists for it: 2,116 lines in the main BSA and 499 in the Serana patch BSA. Many lines in her plugins are spoken by Canas, Aryo, Rolen and others and are left out.

Quick warning for writers: her own mod has a boy called **Remy** (Remy Lauet, an orphan). Our follower Remi is a different person. Never let the two mix up in a line.

---

## 1. Who she is

**Race.** Her record says Breton (BretonRace), female. In the story she is **not a Breton at all**. She is a **"Cumulative Automaton"**: a human-looking machine built by a Dunmer inventor and powered by a soul gem. Her ashen-white hair gave her the name. She hides this and tells people she is "a traveler from High Rock. Ashen hair because of a... failed experiment... or something." Treat the automaton reveal as a **spoiler**: gate it on her first quest (see section 6).

**What she is, in her words.** "I'm a 'Cumulative Automaton'. Think advanced, not Dwemer scrap metal." She has no heartbeat, needs no food or sleep, and lives on **magicka**: magicka potions, Elsweyr Fondue and **dwarven oil** ("I can get 'drunk' in a matter of speaking with it"). She does eat **sweet rolls** for the taste. She "bleeds" a coolant that looks like blood. She doesn't feel cold, so she wears little armour in the snow. Her outfit is "Dwemerweave", woven metal cloth with tonal enchantment. She fights in heels.

**Her makers**
- **Aryo Avellan**, a Dunmer inventor, "a bit popular and a tad controversial in the Tamrielic Academe". He studied artificial consciousness and Dwemer machines. The Thalmor once paid him to invent a new armour cloth, and he walked away from the job.
- **Rebecca** (EditorID `MM_RebeccaAvellan`, the name shows as "Rebecca Montclair"), his wife and research partner. They found a **Time Magic Wielder's notes** (talk of a Dragon Break and other timelines) and built an empty shell they called "U.C.". Rebecca could not have children. She died in 4E 172 of a strain of Blood Rot that could not be cured. Aryo tried to move her soul into the shell. It failed.
- In 4E 175 Aryo put **a fragment of his own soul** into the shell and woke her. He named her Ashe and gave her one purpose: **to "live" and "experience."** Canas thinks her soul may be a fusion of Rebecca's and Aryo's: "A true daughter of sorts."
- **Canas the Silver**, Aryo's protégé, has kept her running ever since. They fell out, and later reconcile.

**The murder.** About a month after she woke, Aryo sent her away on an errand, knowing an assassin was coming. She came back to "an empty husk of a corpse, lying dead on the floor." She chased the killer, who wore a Dark Brotherhood mantle, and was hit by a lightning spell that **shut her down**. Canas rebuilt her, but her mind was "blank" for about **twenty years** of drifting dreams. She has been truly awake for **six years**, which she has spent training as a weapon for revenge. The dates in the mod do not agree with each other: she also says she was "born" in 4E 171. Keep lines date-free.

**Home.** Her father's **workshop in the southeast Rift, "quite near Fort Dawnguard."** Her room has a workbench, a weapon rack, books, a meditation mat, and the flowers her father gave her.

**Keepsakes**
- **Lunar Tear / Nocturne Lily** flowers ("symbols of hope and renewal"). She dreams of "a garden for my Lunar Tears."
- Her greatsword **Cruel Oath**, taken from Thorfinn.

**How the player meets her.** At **The Winking Skeever in Solitude**, a cold mercenary for hire: "The name's Ashe. If it's mercenary work you need, that'll be 200 gold." Ysolda knows her ("I helped her retrieve some stolen goods").

**Her quests, in order** (journal names, with EditorIDs)

1. *The Ashen-Haired Mercenary* (`MM_AsheIntro`): hire her.
2. *Whispers of White Hair* (`MM_FriendshipQuest`): the friendship track. While you sleep, her memories leak into your dreams (flashback quests `MM_AQ00`/`AQ01`/`AQ02`). It ends at stage 70 with the **reveal at the workshop**.
3. *A Borrowed Soul* (`MM_AMQ_01`):
   - She shows you the workshop and meets Canas.
   - She has Canas open her up, and they find Aryo and Rebecca's audio logs.
   - Canas stops the playback. She storms off to hunt the killer.
4. *All For One* (`MM_AMQ_02`):
   - She looks for Dark Brotherhood informants among innkeepers.
   - She meets **Nevas Nevelnor** at the Silver-Blood Inn in Markarth. He betrays them in an ambush.
   - His note points to the Karth River.
5. *Oath Echoes* (`MM_AMQ_03`):
   - The assassin is **Rolen Briand**, now an old woodcutter. He won't break his oath.
   - Branch: Ashe **kills him** in a duel, or the player talks her down and reads his logbook.
   - Either way the name of the man who paid for the murder comes out: **Medeus Attius**, Aryo's jealous rival and a dabbler with Molag Bal.
6. *Shadows of the Past* (`MM_AMQ_04`):
   - Calcelmo, Aryo's old friend, sees through her disguise.
   - They go to Medeus's hidden lab southeast of Whiterun. **Medeus is already dead**, killed by bandits. She is "too late. Again."
   - She sends the player away and **stays alone in the lab**: "I need some time alone. Go on without me." The epilogue then gives her "a day or two".
7. *Through Hell and High Water* (`MM_AMQ_05`):
   - She makes Canas play the rest of the logs. She learns about Rebecca's death and the failed soul transfer.
   - She fights with Canas: "Protect me? By withholding the truth?"
   - Her turning point: "Perhaps the answers I seek aren't about who I was made to be, but who I have become."
8. *One For All* (`MM_AMQ_06`), making amends. It has three parts:
   - *Shattered Orphans* (`06a`): years ago she used farmer **Pa Lauet as werewolf bait**, and he died. She helps his orphans **Lynelle and Remy** at the Riverwood Commune and teaches Remy to hunt.
   - *Binding Blade* (`06b`): she returns **Cruel Oath** to **Thorfinn the Brave**, now a drunk in Windhelm's New Gnisis Cornerclub. They clear a bandit clan together. He may let her keep the sword.
   - *Beyond the Blade* (`06cNEW`): she meets Rolen again. The Brotherhood has wounded him. Branch: **spare him** (he pays it back with supplies for the workshop) or **kill him**. Then they hunt the escaped assassin **Sazin Kurhai "Whisperfang"**.
9. *Go Beyond - Vestiges Reborn* (`MM_AMQ_07`):
   - They climb the **Throat of the World**, where she makes her ethics choice. She goes **compassion**, or "strength / ruthlessness" (which the player can soften).
   - If romance is on, she confesses.
   - They walk down the mountain, with no fast travel allowed.
10. *Bound by Flame and Crystal* (`MM_AMQ_07Epilogue`): a day later, a talk at her home. Drinks are "milk and Sujamma." This is the romance start or the friendship ending.

Side content:
- Canas reconciliation (`MM_AMQ_RNPC`).
- Aryo–Calcelmo letters.
- Campfire talks at inns and player homes (`MM_CampfireTalks`): one drink, then talk.
- Training and sparring, a blacksmith hub, spell teaching, sleeping together.
- A "BIOS mode" settings menu.

**What she wants**
- At first, revenge and "justice" for Aryo.
- Later, to know if she is "a reflection of another, or a being in my own right".
- To find "a new purpose. A reason to exist beyond vengeance".
- To live simply: "a cabin in the woods... Eat all the sweetrolls I could eat."
- To belong: "Lately, I've been contemplating what it feels to belong."

**What she fears**
- That her feelings are "just algorithms mimicking humanity".
- Being seen as "not a person" (her big fear before the reveal).
- Failing her father again.
- That vengeance will turn her into Rolen. Rolen tells her: "To become a monster like me?"
- Being alone: "Perhaps I'm destined to be alone."

**What she values**
- Strength and skill.
- Plain talk ("When you say something, you should mean it"). She hates noble flattery.
- Knowledge ("Knowledge is power").
- Later on: amends, compassion and mercy.

**Faith.** "I never was religious. I only believe in the here and now." She talks about Akatosh, Sithis and Molag Bal as facts, not as gods she follows.

**Small facts**
- **Hates snow** and rain: "Have I mentioned I don't like snow?"
- Loves sunlight, because her magicka refills faster.
- A terrible cook ("tasting like a daedra pie").
- "I've always been the 'milk' kind of girl."
- Reads a lot.
- Early-life accidents she tells as funny stories: she tried to fly off the workshop roof and left a crater, and she once ate a Dwemer history book.
- Fights with greatswords, is fair with one-handers, poor with a bow ("I don't even hit my targets half the time"), and has fists "like steel, quite literally."
- Quotes the thinker **Martimius**: "The only thing you can change about the past is how you feel about it in the present." (The mod's author is also called Martimius.)

---

## 2. How she talks

**Two registers, and the comedy is the gap between them**
- **"Machine" Ashe:** clipped, tactical, robotic jargon.
  - She talks about sensors, systems, calibrate and recalibrate, data points, "emotional matrix" or "emotional cortex", "suboptimal", "efficient", "parameters", "tactical advantage".
  - Her old catchphrase is **"Emotion is prohibited."**
- **"Real" Ashe:** emotional, hesitant, full of ellipses ("I... I don't know"), "*Sighs*", sudden tears and rage.
  - She makes fun of herself for this: "For all my 'emotion is prohibited' jargon, I can be one of the most emotional people on the continent."

**Early vs late**
- Early (friendship stage below 50): cold, curt, mercenary. "Contract!" She deflects personal questions: "Let's keep it at that."
- After the reveal and her quests: warm, teasing, reflective.
- As a lover: flirts in machine-speak ("My sensors are detecting a high probability of... interesting developments").

**Teasing**
- Dry and competitive: "Beginner my arse. I'm still better than you!" / "I'm better than you, admit it." / "*Sigh*... amateur."
- She calls the player **"you dolt!"** when caught out.
- She jokes about her robot nature: "I am an automaton beep-boop, beep-boop", "You 'Organics' have such limitations."

**How she addresses the player**
- "friend" / "my friend" by default, and "Kalin" (a name she offers, after a caretaker in the Time Wielder's notes).
- **The player can choose a name, and "Luna" is one of the voiced names** (`MM_PlayerNameInt` == 11). She has a voiced "Luna." hello and an "All right, Luna." goodbye. There is **no** "I love you, Luna" (the love-line name list skips Luna).
- "love" once she is a lover; "boss" once.

**Speech features to copy**
- Starts with "Hm," "Ugh..." or "*Sighs*".
- Repeats her father's words as a motif: **"live" and "experience"**.
- "Vengeance first."
- "Knowledge is power."
- Asks rhetorical, philosophical questions: "Am I truly myself, or just a vestige of my father?"
- Swears rarely and mildly: "my arse", "bloody Oblivion", "Gods".

### Real lines, grouped by mood (verbatim)

**Cold mercenary (early)**
1. "The name's Ashe. If it's mercenary work you need, that'll be 200 gold."
2. "Because I'm not hungry, and it's none of your business."
3. "Sorry, not interested in even a cursory conversation. If you don't want to hire me, then leave, please."
4. "Emotion is prohibited."
5. "How is this discussion productive to our mission directives?"
6. "Unecessary emotion gets in the way during battle. Not good for us, unless you'd like to end up dead."
7. "Friends? I... don't know. Guess I've never been anybody's friend before." / "No, it's just a fair contract." / "Contract!"

**Dry humour / teasing**
8. "Beginner my arse. I'm still better than you!"
9. "I'm kidding! You should have seen your face. 'Death to all Ayleids! I am an automaton beep-boop, beep-boop'."
10. "Great, now I'm malfunctioning AND leaking fluids. This 'human experience' is rather overrated, wouldn't you say?"
11. "Here is the workshop library. Strange what a scholar will collect... 'Lusty Argonian Maid'? Really?"
12. "I certainly want to short-circuit and punch you right now, but you're too adorable for that."
13. "I do not brood! I'm just... thoughtfully intense."
14. "Seeing as how I don't eat food, I'm a terrible cook. Don't ask me to cook you a mutton pie, lest you eat something that ends up tasting like a daedra pie."
15. "Last one down the mountain gets stuck with a stinky kwama egg! *Giggles*"
16. "Oh, no. Don't even think about asking me. My solution involves a sword and a lot of noise." (lockpicking)

**Tactical / travel**
17. "Have I mentioned I don't like snow?"
18. "This castle looks rather fortified. Should be able to withstand a siege for about a week."
19. "Scanner is picking up enemies ahead."
20. "I do not require breath, yet I still find myself holding it. Strange." (sneaking)
21. "If this doesn't work, we revert to plan B: Aggressive Negotiation."
22. "I've heard they have great pastries here. It would positively suit team morale to consume such treats."

**Angry / vengeful**
23. "How dare you utter my father's name! Tell me who ordered his death, assassin!"
24. "An oath?! Who in bloody Oblivion cares about oaths!? We're here because a family was cleaved apart by your blade. My family!"
25. "Robbed of the death he deserved because I was too late. Again. Gods, I was too late again!"
26. "You can't be serious. Flawed?! My parents have haunted me ever since I found my father in a pool of his own blood twenty-six years ago!"

**Sad / searching (identity)**
27. "Am I a reflection of another, or a being in my own right? The question disturbs me."
28. "Am I truly myself, or just a vestige of my father? An ember that will eventually fade away?"
29. "Mortal emotions are complex, aren't they? And to think I'm modeled after them, I have some of that complexity too!"
30. "When I see the beauty of Skyrim's landscapes, I can't help but imagine what it would be like to experience it as a living being. A real, living, girl."
31. "Afraid you'd see me as... as a mo- as... not... not a person."

**Warm / grown (late)**
32. "You know, sometimes I forget what it's like to have a friend. Thanks for reminding me."
33. "Like... a weight has shifted. Not lifted entirely, but... redistributed."
34. "Still... maybe this is what my father meant by 'living and experiencing.' Not the bloodshed- but the choice to talk, to reflect. To laugh, even."
35. "I used to see the world as a series of tactical challenges. You're teaching me to see the beauty in it, too."

**Romantic (machine-flirt)**
36. "Mind if I sit closer? The fire's heat doesn't register on my sensors. But proximity to you... oddly does."
37. "Data logged. You are now classified as a... portable heat source."
38. "Careful, friend. Offer me a heart and I may write it into my mission parameters."
39. "A- a date? Don't get any ideas. I wasn't asking you out or anything... ...but I suppose your company isn't entirely unpleasant."
40. "I love you. Truly. Deeply. It's... overwhelming, exhilarating, and utterly terrifying all at once. But... it feels right."

**Combat**
- "Incoming power move! Let's see how you like this!"
- "Let's give them a show."
- "Another fight, another victory. There's no one I'd rather have watching my back."
- "More constructs. You are soulless, lifeless.. devoid of purpose."

---

## 3. Romance with the player

**A female player is fully supported.**
- There are no gender conditions on any romance line in her own plugin.
- The epilogue script just picks a "male" or "female" message box.
- The Serana patch has separate he/she versions of each line (`GetPCIsSex` Male/Female pairs).
- Her love-greeting name list includes female names (Oona, Octavia, Marceline, Dawn...).
- She compares herself to "your kind romancing a vampire".
- So Luna (she/her) works. Ashe is female, so this is a woman–woman romance.

**How it is tracked**

| What | EditorID | FormID (runtime) |
|---|---|---|
| Romantic-interest meter, 0–7+ | `MM_RM` (GLOB) | 2F3039:Ashe - Fire and Blood.esp (942F3039) |
| Romance ON flag | `MM_AsheRomance` (GLOB, 0/1) | A5E1EF (94A5E1EF) |
| Friendship points | `MM_FP` (GLOB) | 117023 |
| Ethics points | `MM_FriendshipQuest` script var `EthicalPoints` | quest 1A9DEE |
| Automaton revealed | `MM_FriendshipQuest` var `MM_AutomatonReveal` == 1 | 1A9DEE |
| Mountain confession happened | `MM_AMQ_07Confession` (GLOB) | E67C22 |
| Romance beat quest | `MM_RomanceHandler` (stages 10–100) | 5619E0 |
| Shared sleeping unlocked | `MM_SpooningGV` | 566B14 |
| Flirt during friendship quest | `MM_FriendshipQuestFlirtGV` | 056B54 |
| Ashe + Serana "together" (poly) mode | `MM_FantasyMode` (Serana patch) | 3A9EEA:Ashe and Serana Banter Patch.esp |
| Player chose Serana instead | `MM_AsheranaSeranaChosen` (Serana patch) | 5B3EDB |

**How it goes**
1. **`MM_RM` goes up** through flirty or kind choices. A script shows the notifications "Romantic interest increases." and "...decreases."
2. Lines unlock at RM ≥ 2, then ≥ 3, ≥ 4 and ≥ 7:
   - RM ≥ 2: playful goodbyes.
   - RM ≥ 4: "I'll be right beside you. Always.", stargazing hellos.
   - RM ≥ 7: home and "sanctuary" lines, and the "you've been staring" outfit lines.
3. Small romance scenes run after each of her quests (`MM_Romance02PostAMQ01/02/03/05`), for example "Mind if I sit closer?" by the fire.
4. **The confession** happens on the Throat of the World (`MM_AMQ_07` stage 90+). It needs `MM_RM` ≥ 7 and `MM_AsheRomance` == 0. At RM 2–6 she starts to say it, then backs off: "I... um... never mind."
5. **The epilogue** (`MM_AMQ_07Epilogue`) asks the player to answer. Its fragments set **`MM_AsheRomance` = 1**, play "I love you" and unlock intimacy (`MM_IntimacyController`, which only runs when `MM_AsheRomance` == 1).
6. **Shortcut:** the **"Hearthfire Protocol"** in her BIOS menu. Aryo designed it so she would not miss out on love. It sets romance on early and skips courting. If you used it, she says on the mountain: "Do you remember... when you activated the Heartfire Protocol?"

**Banter gates to use**
- Crush and teasing: `MM_RM` ≥ 2–4.
- "Together": `MM_AsheRomance` == 1.
- Never script the confession or epilogue scenes themselves. Only talk about them after `MM_AMQ_07Epilogue` is completed.

**Jealousy and rivals (existing material).** Her only rival material is with **Serana**, and Ashe **refuses to be jealous**:
- On rivalry: "Ah. I see. You are attempting to initiate a rivalry. That seems... inefficient. Your premise assumes affection is a finite resource. A logical fallacy."
- On cooperating: "Cooperation. Why would we engage in a counter-productive rivalry when we could simply... coordinate our efforts to ensure our companion's continued happiness?" Serana answers: "you just tried to solve romance with math."
- When Serana wins the player: "Look... you're important to her. So if my being here is a... complication... I can make myself scarce. It's a logical adjustment."
- On being asked if she's jealous: Serana says "Jealous?" and the answer is "Competitive."
- In shared ("fantasy") mode: "Our lover here has got that look again."

**For our mod.** Ashe's jealousy should be **denial plus data**: she logs heart rates, calls it "inefficient", then gets "competitive" about measurable things such as combat reflexes and efficiency. She does not glare or make threats. Remember the user's rule: Luna almost always romances Kaidan. So Ashe is most often **the friend, not a rival**, unless gated on `MM_AsheRomance` == 1. With Kaidan or Val she would probably be the one who **reads the vital signs** of their crush on Luna ("Your heart rate elevated by 33%").

---

## 4. Her opinions of other followers

**None of her voiced lines mention Kaidan, Gore, Val Serano, Remiel, Xelzaz, Inigo, Lucien or Redcap.**
- I searched all 2,615 of her voiced lines.
- I also checked the other way. Inigo.esp, 0Kaidan.esp, Kaidan - Immersive Features.esp, BWB - Kaidan 2 Extra Dialogue.esp, AX ValSerano.esp, GORE.esp, BPUFXelzazFollower.esp, Lucien.esp, HLIORemi.esp, the Redcap plugin and SeranaDialogAddon.esp contain **no "Ashe"** at all.
- Everything below except Serana is new ground.

**Serana** (official banter add-on, a lot of it): see section 5.
- At first she **suspects** Serana. Serana notices Ashe "is cold" and never tires.
- They become **curious, needling friends**. Ashe analyses vampire physiology and folklore ("a genuine aversion to silver"). Serana teases her about wind-up keys in the rain, her heels, sinking in water, and "solving romance with math".
- Serana calls her "an absolute menace... It's a good thing you're cute."
- They share themes: "From one reformed monster to another", fathers who made them weapons ("I used to think I was just a key").
- Possible romance triangle or shared romance with the player.

**People from her own mod**
- Canas: "the closest thing to family I have left".
- Calcelmo: "more perceptive than I gave him credit for".
- Ysolda: an old client.
- Lynelle and Remy: she feels guilt. "Admiration is a dangerous emotion. Especially when directed at someone like me."
- Thorfinn: "It's like I'm staring at myself in a mirror."
- Rolen: sworn enemy, then "Mister Briand and I... we're fine now" (if spared).

**Guesses for our party (INVENTED, not canon; based on her character)**
- **Kaidan:** a fellow ex-weapon with a dark past and a revenge-scarred mentor (Brynjar / Aryo). She would respect his swordwork and spar him: "I'm better than you, admit it." His puns would confuse her. She has a scanner, so she would "notice" his crush on Luna.
- **Gore:** a mercenary like her early self. She would correct his technique and enjoy his bluntness. She wouldn't get his mead and bard jokes. Possible link: she taught Remy Lauet to hunt, and she could teach Gore something too.
- **Val Serano:** a relic hunter with a crossbow he built himself. She would be curious about his gear and dismissive of his charm ("inefficient"). He could be the one to give her nicknames.
- **Remi:** a **Dwemer fanatic meets a walking Dwemer-inspired machine**. This is the strongest pairing. Remi would want to examine her (or be scared to ask). Ashe would find Remi exhausting but sweet. Spoiler gate: only after the reveal (`MM_AutomatonReveal`). And Remi + **Scrap** (a spider construct) vs Ashe ("These automatons probably won't be friendly").
- **Xelzaz:** both are dry, both are alchemy-minded. He would critique her dwarven oil "diet". On necromancy, she hated using a man as bait and hates soul trapping ("an entire economy built on eternal servitude" in the Soul Cairn), so she would clash with him gently.
- **Inigo:** her father was killed by a paid assassin and she hunted the Dark Brotherhood. Inigo was **raised by assassins** (Leah and Da Vinci). That is a serious, careful topic. They share **sweet rolls**.
- **Lucien:** a scholar who loves Dwemer things, like Remi. He would lecture her about her own "lore"; she joked "I think I've already broken enough lore for one lifetime". He is scared of crypts; she is curious about Nordic ruins.
- **Redcap:** he names creatures "fa-ka". What would he call her? "Metal. Lady."? She would answer in literal data.

---

## 5. Existing cross-follower banter she is in (so we copy the method and avoid repeats)

**A. Ashe Inigo Compatibility Patch.esp: NOT banter.**
- It overrides one record: `WIFollowerCommentNode` (04C729:Skyrim.esm).
- It adds Inigo's `InigoImpressiveView` quest back into the Story Manager node that Ashe's plugin rewrote. Ashe's own commentary quests `MM_NPCCommentary01/02/03` sit in the same node.
- Authoria's `Follower SMQN Merge.esp` wins that node now and keeps both.
- **Ashe and Inigo have zero lines together.**

**B. Ashe and Serana Banter Patch.esp: quest `MM_AsheranaBanterMain` (00AA1A:Ashe and Serana Banter Patch.esp)**

Quest and aliases:
- Priority **100**. Flags: none (not start-game-enabled in the record; it is started by her mod).
- Aliases are UniqueActor `MM_Ashe` and `DLC1Serana`, plus Agmaer and the player.
- Scripts: `MM_AsheranaBanterScript`, which holds ~85 conditional "say-once" bools such as `bRadiantJealousFlirt01`, and `MM_AsheranaCooldownScript`.

**How talks start**
1. An Idle topic, **`MM_AsheranaBanterMainIdleTriggers`**. Each INFO is the opener for one talk and its fragment starts a Scene. Openers exist for **either** speaker (`GetIsID MM_Ashe` or `GetIsID DLC1Serana`).
2. Typical opener conditions:
   - `GetDistance(other alias) < 800`
   - `IsInScene == 0`
   - `IsTalking == 0` on the other one
   - `IsSneaking == 0`
   - **`GetGlobalValue MM_PlayerinDialogue (5435E9) == 0`**
   - **`MM_AsheranaBanterGV (0383BD) >= 2`** (they have met)
   - the say-once bool `::bXxx_var == 0`
   - a cooldown, written as `GetGlobalValue GameDaysPassed >= <cooldown global>`
   - plus the place, time and quest gates (`LocationHasKeyword` LocTypeDwelling/Inn/PlayerHouse, `IsInInterior`, `IsPleasant`, `GetCurrentTime`, Ashe and Dawnguard quest stages).
   - Note: the openers do **not** test "is following" themselves.
3. Combat banter comes from an alias script (`MM_AsheranaBanterTrigAlias.OnCombatStateChanged`). It runs only if **both** `IsFollowing` flags are true and **`MM_SafeLoc == 0`**. It waits 3 s, then starts `MM_AsheranaNormaltoCombatStarter` or `...CombattoNormalStarter` (cooldown globals `MM_AsheranaNormalToCombatCooldown`, `...CombatToNormalCooldown`).
4. Hello topics give one-liners. The campfire talk can hand over: "Now, I believe Serana has been waiting for her turn."

**Topics already used (do not repeat). The scenes come from 182 SCEN records.**

*Dawnguard questline (both sides, all of VQ01–VQ08):*
- They meet at Fort Dawnguard / Volkihar.
- The boat to Castle Volkihar, getting out of the cave in good and bad weather.
- The College; on the way to Dragon Bridge; the ambush.
- The Moth Priest; Dexion's lab; the Soul Cairn (Valerica, the dragon, "Soul fissures... an entire economy built on eternal servitude").
- Waiting outside; the squirrel.
- The Forgotten Vale: cave, camp, Darkfall entrance, Falmer, valley, first wayshrine, frost troll, ice dragon, waterfall, precarious bridge, spiders, temple courtyard and interior, traps.
- The final Harkon fight; the hunter or vampire invasion.

*Ashe questline reactions (Serana comments):*
- Prologue flashbacks 1 and 2.
- The AMQ01 reveal and its aftermath.
- AMQ02 (intro, "chasing a murder cult, you sound almost... giddy").
- AMQ03: hut search; Serana: "maybe we should keep him alive".
- AMQ04: outside the cave, sabre cat, more bandits, Ashe rushes in, leaving the cave, aftermath.
- AMQ05 parts 1 and 2.
- AMQ06: the children, the Nord, the village; Serana: "All the parents I've slain".
- 06b errand; 06cNEW blood trail and aftermath ("From one reformed monster to another").
- AMQ07 intro and aftermath.

*Radiant, repeatable on cooldowns:*
- Outfit x2, heels ("form and function").
- Vampire talks x2, vampire misconceptions x2 (folklore, silver).
- Automaton talks x3 ("do you ever feel... hollow?").
- Memories, dream, "robo confuse" x2 (Dwemer constructs vs her).
- Tired ("I'm dead, and even I'm feeling the drag"), sunlight drain, lake.
- Wake-up morning and evening ("Cognitive matrix... operating at 87% efficiency").
- Alchemy, sweetroll intro / "the food thing", pumping iron.
- Clean sword, book reading, "born again" (a mortal-soul hypothetical), father rebel ("I used to think I was just a key").
- Location-aware: College of Winterhold, Jorrvaskr ("musk of sweat and fur"), the Thieves Guild / Ratway ("Awfully damp"), ice caves.
- Serana humming, mead flask.
- Romantic-evening planning ("You just described a military operation").
- Group romance tease, jealous flirt / rivalry ("solve romance with math").
- Scripted suspicion x3, before the reveal ("Whoa. You're cold.", "I'm starving. What's on the menu?").

*Unused cooldown names in the plugin* (globals exist; these may be one-liners or future content): ArmsTired, DungeonDarkness, DwemerNoise, DungeonDeadEnds, DungeonStress, SleeplessNight, PackReorganization, PassionBanter, SoulValidation, BookHobbies, Longevity, PlayerRest, Slang, MemoryCatalog, Snow, EmergencyTransport, Rabbit, NightSky, ScenicWalk, Sculpture, MeadAnalysis, WalkingFatigue, NordicRuinDecor, ArmorPolish. **Avoid these topics with Serana.** They are fine with other partners if we change the angle.

*Romance-mode scenes:*
- `MM_AsheranaRadiantFantasyMode01–04`, `MM_AsheranaPostLoveMakingFantasy01–04` ("Our lover here...", "split their time evenly").
- The three-way "Things have... changed" talk when the player picks Serana (SeranaDialogAddon romance stage 25).

*Combat:* 23 start scenes, 8 end scenes, 10 taunts.

**C. Ashe's own placeholder for follower banter.**
- Her main plugin has an **empty** quest `MM_FollowerBanter` "Main Quest for all Ashe's Follower Banter" (245FFE). It is start-game-enabled, has a dialogue condition `IsFollowing == 1`, and has no lines.
- The author planned more partners. It is a clean model for our quest's conditions.

**D. Her own pacing (to avoid spam)**
- Ashe's idle one-liners (`MM_AsheGeneralHellos`) need:
  - `MM_AsheGeneralHelloTime (0EE7F1) <= GameDaysPassed`
  - `IsInDialogueWithPlayer == 0`
  - `MM_PlayerinDialogue == 0`
  - not sneaking
  - **`MM_AsheMentalModel.bConfigVarIdles == 1`**. This is her "keep my thoughts to myself" toggle in the BIOS menu. **Our mod should respect it too.**

---

## 6. Technical

| Item | Value |
|---|---|
| NPC base | `MM_Ashe` "Ashe", **005900:Ashe - Fire and Blood.esp** (runtime 94005900 today). Live winner: Requiem for the Indifferent.esp |
| Do NOT target | `MM_AsheFBActorBase` 77052C (a flashback double used in memory scenes) |
| Placed reference | **2D4A35:Ashe - Fire and Blood.esp**, in SolitudeWinkingSkeever |
| VoiceType | **`MM_AsheVoice`**, 00AA01:Ashe - Fire and Blood.esp |
| Race / flags | BretonRace; Female, Essential, Unique; class CombatBarbarian |
| Factions | `MM_AsheFaction` 0C0ED8, `MM_AsheCrimeFaction` 0C0ED7, `MM_AryoWorkshopFaction` 196271. She is **not** in CurrentFollowerFaction or PotentialFollowerFaction |
| **Is-following check** | **`GetVMQuestVariable(MM_AsheMentalModel 06FE28, "::IsFollowing_var") == 1`**. Her mod uses this 55 times, and her empty banter quest and the Serana patch use it too. When she follows, her script also calls `SetPlayerTeammate(true)` and adds `WIFollowerCommentFaction`, so `GetPlayerTeammate == 1` works as a backup. Other mental-model vars: `IsWaiting`, `IsDismissed`, `bConfigVarIdles`, `bConfigVarNPCTalks` |
| Her follower framework | `MM_AsheMentalModel` (06FE28, priority 80, script MM_AsheMentalModelScript). It is her own system, like Serana's. Don't use NFF or AFT on her |
| Mod detection | Her `MM_ModCheckScript` only checks SKSE, HDT, SleepTight, ACC and the 2B outfit. It does **not** soft-detect other followers. Our mod must find **her** with `Game.GetFormFromFile(0x005900 / 0x2D4A35, "Ashe - Fire and Blood.esp")` |
| Player name | `MM_PlayerNameInt` (2AB56F): **11 = "Luna"** (0 / default = "friend", Kalin is a separate intro choice) |

**Her personal-quest gates (put "done" gates on story talk; silence banter while these run)**

| Gate code idea | Condition |
|---|---|
| ASHE_HIRED | `MM_AsheIntro` (0A7946) completed |
| ASHE_REVEAL (automaton secret is known) | `MM_FriendshipQuest` (1A9DEE) stage ≥ 70, or var `MM_AutomatonReveal` == 1 |
| ASHE_Q1 | `MM_AMQ_01` A Borrowed Soul (756FEA) completed |
| ASHE_NEVAS | `MM_AMQ_02` (BB194C) completed |
| ASHE_ROLEN1 | `MM_AMQ_03` (BC5D8F) completed. Branch: Rolen dead or spared (ref 75C0F7 `GetDead`) |
| ASHE_MEDEUS | `MM_AMQ_04` (00AA1A:Ashe - Fire and Blood.esp) completed |
| ASHE_LOGS | `MM_AMQ_05` (056A66) completed |
| ASHE_AMENDS | `06a` C07BE9, `06b` C11E04, `06cNEW` 380306 completed. 06cNEW var `AsheKilledRolenJustice` gives the branch |
| ASHE_SUMMIT | `MM_AMQ_07` (D6A70C) completed |
| ASHE_LOVE | `MM_AsheRomance` == 1 (after `MM_AMQ_07Epilogue` E5DA07, or after the Hearthfire Protocol) |

Note: the Serana patch also has a quest **00AA1A** (the banter controller). Always write the plugin name with the FormID.

**Silence conditions: our banter must never fire during her scripted moments**
- `GetGlobalValue MM_PlayerinDialogue (5435E9) == 0`. It is set by a menu watcher whenever any dialogue menu is open.
- `IsInScene == 0` on Ashe (and on the partner).
- `MM_FlashbackRunning (4643DC) == 0`: the memory and flashback quests.
- `MM_ScriptedCombatScenePlaying (BF887E) == 0`.
- `MM_AsheranaSleepBanterPlaying (52B269) == 0` and `MM_AsheSeranaLoveBanterBlock (628708) == 0`, both from the Serana patch, when installed.
- `MM_AsheMentalModel.IsWaiting == 0`, and `bConfigVarIdles == 1`.
- Quest-running blocks:
  - **`MM_AMQ_04` (00AA1A) stages 45–80.** She is alone in Medeus's lab or "needs a day or two".
  - **`MM_AMQ_05` running.** The audio logs and the fight with Canas.
  - **`MM_AMQ_07` running.** The summit, the confession, and the walk down with no fast travel.
  - **`MM_AMQ_07Epilogue` running** (the home talk).
  - The `06a` village scenes with the orphans (stage < 80).
  - `06cNEW` stages 40–60 (deciding Rolen's fate).
  - Ashe's friendship flashback quests `MM_AQ00/01/02` running.
- Safest single rule: no banter while any `MM_AMQ_*` quest is running **and** Ashe is in that quest's location. Otherwise use the stage list above.

---

## 7. Voice reference for cloning

**Who voices her:** a **human actor, Anna Rust** (Carnival Row, Cyberpunk 2077), per the Nexus page. Her lines in the Serana patch are by the same actor (same `MM_AsheVoice`). She is not AI-voiced.

**Where the files are**
- **Main:** `C:\1. AUTHORIA\mods\Ashe - Crystal Heart\Ashe - Fire and Blood.bsa`. Inside: `sound\voice\ashe - fire and blood.esp\mm_ashevoice\`. 2,116 .fuz files.
- **Serana banter:** `C:\1. AUTHORIA\mods\Ashe - Crystal Heart - SDA\Ashe and Serana Banter Patch.bsa`. Inside: `sound\voice\ashe and serana banter patch.esp\mm_ashevoice\`. 499 .fuz files.
- There are **no loose files**. Every clip must be pulled out of a BSA first, then converted .fuz → .wav.
- Lengths below were read from each file's xWMA header. I picked them from their text and **did not listen to them**, so check them by ear.

**Five candidate clips** (calm, conversational, 4–10 s). All are inside the main BSA under `sound\voice\ashe - fire and blood.esp\mm_ashevoice\`.

| # | Length | File | Line |
|---|---|---|---|
| 1 | 9.3 s | `mm_campfir_mm_campfiretalk_002287e8_1.fuz` | "When I see the beauty of Skyrim's landscapes, I can't help but imagine what it would be like to experience it as a living being. A real, living, girl." |
| 2 | 7.8 s | `mm_friends_mm_friendshippd_0020a1a8_1.fuz` | "It's a flower that my father used to grow. I'm not sure where he got the seeds from, because they can't be found anywhere else in Tamriel." |
| 3 | 7.4 s | `mm_campfir_mm_campfiretalk_0022d8fc_1.fuz` | "In a peaceful life, I'd definitely live in a cabin in the woods, and take daily, frequent strolls nearby." |
| 4 | 7.8 s | `mm_ashecli_mm_asheclickedh_003435f0_1.fuz` | "I was just admiring the scenery. It's easy to forget the beauty around us when we're always focused on the next fight." |
| 5 | 7.1 s | `mm_ashegen_mm_rnpcgeneralh_00111f20_1.fuz` | "Besides combat and training, I do enjoy a good read every now and then. After all, knowledge is power." |

**Spares**
- `mm_amq_01_mm_amq_01act2bra_0000591d_1.fuz` (6.3 s): "He was a bit popular and a tad controversial in the Tamrielic Academe."
- `mm_campfir_mm_campfiretalk_002287f6_1.fuz` (6.3 s): "There is something about nature that allows me to appreciate life. I love new experiences."
- `mm_ashecli_mm_asheclickedh_003435f2_1.fuz` (9.7 s): "I've been considering our options for the next step in our journey..."
- `mm_friends_mm_friend_side0_0020f2ab_3.fuz` (5.2 s): "I ended up here in Skyrim as it seems like here's the best place for mercenary work."

**Bonus, real "Luna" clips** (use as pronunciation reference, or splice them):
- `mm_playern_mm_playernamehe_00552644_1.fuz`: "Luna."
- `mm_playern_mm_playernamego_00552609_1.fuz`: "All right, Luna."

For cloning, #1, #3 and #5 give her neutral, warm reading voice. Avoid these clips:
- the robotic BIOS lines (`mm_biosfg*`)
- the sobbing scene (`00594F`)
- the shouting at Rolen (`MM_AMQ_03` taunts)
- the intimacy lines (`MM_Intimacy*`)
