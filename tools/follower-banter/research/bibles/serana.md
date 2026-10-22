# SERANA - character sheet (for the follower-banter mod)

Read on 2026-10-18 from the live load order (MO2 `C:\1. AUTHORIA`, profile "DEEZ CS NUTZ - PICTA"). Nothing in the game or the profile was changed.

What was read:
- All 7,055 dialogue lines in **Serana Dialogue Add-On** (SDA, `SeranaDialogAddon.esp`, version 4.3.2 by Martimius).
- The SDA patches in this profile: Remiel Banter, Campfire, House of Horrors, CC Umbra, Sweets and Such, SDA-AA, the Amulets of Mara patch, Maker Stones and Race Compatibility.
- **Ashe and Serana Banter Patch.esp**: 982 lines, about 200 scenes.
- The 584 SDA scenes, rebuilt into full transcripts.
- SDA's 223 globals and its romance and banter scripts, decompiled.
- Serana's vanilla Dawnguard lines.
- Every line that names Serana in the plugins of Kaidan, Gore, Val, Remi, Xelzaz, Inigo, Lucien, Redcap and Ashe.

The working dumps are in my scratchpad and are not needed again.

**Already in the profile, not part of SDA:** `Vampire Lines Expansion.esp` (+ Orc Addon) is generic combat barks for enemy vampires. It does not touch Serana.

---

## 1. Who she is

### Vanilla Dawnguard

**Basics**
- She is a pure-blood vampire, a **Daughter of Coldharbour**. Her family received the "gift" straight from **Molag Bal** in a ritual she calls "degrading".
- She is a Nord by look. The record in this load order uses the UBE Nord race.
- She was born in the First Era. Her family are the **Volkihar** nobility of Castle Volkihar, on an island west of Solitude.

**Her parents**
- **Harkon**, her father, is the clan lord. He became obsessed with the **Tyranny of the Sun** prophecy: an Elder Scroll and Auriel's Bow would blot out the sun. "My father... after all these years, that's the first thing he asks me. 'I trust you have the Scroll?'"
- **Valerica**, her mother, is a master alchemist and necromancer. She sealed Serana in a coffin in **Dimhollow Crypt** with an Elder Scroll to keep both from Harkon. Valerica then fled into the **Soul Cairn**, the realm of the Ideal Masters, where trapped souls are harvested.

**The Dawnguard quest line, in order**
1. **Awakening** (DLC1VQ01): Luna wakes her in Dimhollow.
2. **Bloodline** (DLC1VQ02): Luna takes her home to Castle Volkihar.
3. **Prophet** (DLC1VQ03Hunter / Vampire): finding a Moth Priest to read the scroll.
4. **Chasing Echoes** (DLC1VQ04): searching Valerica's courtyard and lab.
5. **Beyond Death** (DLC1VQ05): the Soul Cairn and **Durnehviir**.
6. **Unseen Visions** (DLC1VQ06): the Ancestor Glade.
7. **Touching the Sky** (DLC1VQ07): the Forgotten Vale and Auriel's Bow.
8. **Kindred Judgment** (DLC1VQ08): **Harkon dies**.

Her family wound is the heart of her character: "I want us to be a family again. But I don't know if we can ever have that." After Harkon dies: "I think my father really died a long time ago. This was just... the end of something else."

**The cure.** In vanilla, Falion in Morthal can cure her with a filled black soul gem. **SDA changes this.** Serana decides on her own ("Hey, so about my vampirism... I've made a decision"). She goes to Falion alone and meets Luna "back home" a day later (`SDA_CureQuestTimer`). After the cure:
- She talks about being "human again".
- She gets tired at night: "I feel as fragile as a skeleton."
- She hopes her soul now escapes Coldharbour.

The game checks whether she is cured with **Serana HasKeyword Vampire == 0**.

### What SDA adds to her character

**Childhood**
- She played with the castle rats in the **undercroft** by an unused jetty, looking out at the sea. That was her hideout.
- She tended her **mother's garden** with Valerica in the courtyard. She calls it "nurtured by a master for centuries".
- She was "quite the bookworm". She read Redguard pirate tales, and her childhood hero is **Jyaik Talonwood**.
- She sang to feel less lonely.
- She sometimes went to Skyrim with Harkon "on business". She describes that as "intimidation, scheming, bribery, blackmail, an execution or two".

**Tastes**
- Drink: she likes **mead, especially Black-Briar**. Colovian vintage is "my favorite".
- Food: blood-spiked ale, the Boiled Creme Treat.
- She loves books and the College of Winterhold.
- She admires **Breton culture**.
- She wants a pet Bantam Guar.
- Her favourite song is "The Tale of the Tongues". SDA gives her an original song, "Old Stone Walls", which she sings.

**Hunger and feeding**
- She can go long without blood ("Daughters of Coldharbour have more control").
- Resting helps her hunger.
- She carries **blood potions** made from enemies' blood. Cow blood works too.
- Garlic is a myth. Stakes are not the only weapon that works on her.

**Faith and Daedra**
- She "detests the ceremony, and Molag Bal". "And Molag, he can eat horse dung for all I care."
- She worries about her soul going to Coldharbour, and thinks about worshipping Magnus, Zenithar or Akatosh instead.
- She warns Luna about every Daedric pact (Nocturnal, Sanguine, Hircine).

**Age.** She says she remembers the **Aetherium Wars**, which makes her about 4,500 years old (her Remi banter, scene 8). Vanilla only says she was sealed away for "a few centuries" to "thousands of years".

**Trust secret** (`SDA_SeranaRomance10Trust`). She confesses that at their first meeting she **manipulated** Luna to survive: "I manipulated you. I really just wanted to survive then and there."

**Mother after the quest line.** She can go back to the **Soul Cairn** to visit Valerica (SDA_ValericaBranch*, SDA_SoulCairnPost). She worries Valerica will see she is "human again" or "together with you".

**Other SDA features**
- She comments on almost every quest line: Main Quest, Companions, College, Thieves Guild, Dark Brotherhood, Daedric quests, Dragonborn, Hearthfire.
- She keeps her own **friendship timer**.
- Drinking Buddies: she orders drinks and talks at the inn.
- She has gifts, a horse, cooking, sleeping, outfits, teleport, training and spell-teaching systems.

**What she values**
- Freedom and choosing for herself: "you don't get to make this decision for me."
- Honesty between friends.
- Books and history.
- Her mother's memory, despite everything.

**What she fears**
- Being caged or sealed again.
- Being underground too long ("It's getting to my head").
- Coldharbour.
- Being seen as a monster.

---

## 2. How she talks

**Overall tone**
- Dry, sardonic, a little posh-aristocratic, and quick to tease.
- She hides feelings behind jokes, then drops the guard in short, quiet bursts.
- She is less sweary than Kaidan or Gore. "Gods", "Shor's bones" and "By the Nine" are her strongest, with a rare "fucking" in combat.

**Sentence shape**
- Usually short to medium.
- Lots of "Ugh...", "*Sighs*", "Hmph", "Heh" and "*Chuckles*".
- Trailing "...", and self-interruptions ("I... I like you. As a friend... and as aaa...").

**Oaths and fillers:** "Gods", "Gods-cursed", "By the Nine", "Shor's bones", "Divines", "Ugh", "Wow...", "Well...", "Anyway".

**Address**
- She uses Luna's **name** through SDA's custom-name system. **"Luna" is already recorded:** "Hey Luna!", "All right Luna!", "Come here, Luna. Now and forever."
- In romance: "my love", "love".
- In teasing: "numbskull", "numbnut", "horker", "s'wit", "pile of talking scrib jelly".
- Inigo: "pretty kitty", "kitty-cat". Remiel: "Remi". Ashe: "Ashe".

**Running bits**
- Mock offers to drink a friend's blood ("Your blood, please." / "Maybe I'm not kidding."), always followed by "I'm not going to feed on you."
- Myths about vampires (garlic, stakes, bats).
- Calling herself a "dusty old relic" or "this old relic".
- She hates being treated as a pack mule.
- She orders drinks at every inn.
- Smell complaints (Jorrvaskr "reeks of dogs", the Ratway).
- The sun: "Try to stay warm out there. Or in my case, stay shaded."

**What makes her soft**
- Being accepted as a person rather than "it" or a monster.
- Kindness about her family.
- Talk of her mother's garden.
- Stars, the sea and beaches.
- Someone noticing that she is hurting.

**When pushed about family.** She deflects first ("Let's not revisit that."). Then she gets short-tempered ("you don't get to make this decision for me."). Then she cries and apologises (the Trust and Determination quests).

### Real lines by mood (verbatim)

**Dry / teasing**
1. "Oh, wonderful. A war of succession. Good to know the world didn't get boring while I was gone." (vanilla)
2. "You can be a real horker sometimes, you know that?"
3. "Maybe you're a pile of talking scrib jelly."
4. "I may be... out of the loop on the whole romance thing, but that pickup line is just bad. Abysmally bad."
5. "Ugh... I swear, sometimes it feels like you take courtship tips from Sheogorath..."
6. "Ah, Jorrvaskr. Who would have thought you could make a mead hall out of an overturned boat?"
7. "So, are you here more to buy something, or dump all your junk to the shopkeep?"
8. "Please don't treat me like a pack mule."
9. "Hey... don't sniff me too much, all right?"
10. "Well, I personally prefer to feed off of Bretons who know too much about the Dwemer." (to Remi)
11. "I was almost afraid it would cause your heart to fail. Judging by your face, I'm still concerned that might be the case." (to Remi)
12. "Sure thing, pretty kitty." (to Inigo)

**Warm / wonder**
13. "Wow... you really gotta hand it to the Divines. Nirn truly is beautiful. Miles better than Coldharbour, that's for sure."
14. "I was just looking at the stars... The constellations, they're so... mesmerizing."
15. "You know what I've always wanted... a pet Bantam Guar. I've heard their cuteness is legendary!"
16. "Hey... thanks again, for everything. You made the world a better place... for me."
17. "Don't worry. We won't let that happen." (to Remi, about dying before she has learned everything)
18. "I think both of our parents have failed us. Just you and me against the world, now." (vanilla)

**Family / sad**
19. "The ceremony was... degrading. Let's not revisit that."
20. "My father... after all these years, that's the first thing he asks me. 'I trust you have the Scroll?'"
21. "I was lonely most of my childhood. My mother, at least for a time, was the only friend I really had."
22. "I want us to be a family again. But I don't know if we can ever have that." (vanilla)
23. "I think my father really died a long time ago. This was just... the end of something else." (vanilla)
24. "I get it, Remi. I appreciate your intentions, but I don't feel much like talking right now."
25. "Let's not hang around here for too long. It just saddens me... to be in places like this."

**Romance (SDA, only if gated)**
26. "Here goes. I... I like you. As a friend... and as aaa... ...travelling companion."
27. "Gods. I am a terrible liar."
28. "Do you... like me? Not just as a friend, but as... something else."
29. "You are my savior. My sole reason to keep living. I love you."
30. "Come here, Luna. Now and forever."
31. "I love you. I really do. In the thousands of years I've walked on Nirn... you are the best thing that's happened to me."

**Combat**
32. "Fighting a Daughter of Coldharbour, well, you've made a big mistake."
33. "'The enemy of my enemy is my friend.' I think that when I'm raising corpses."
34. "Back to dust!"
35. "Oh, it's on."
36. "Took care of them in style, didn't I?"
37. "If you lay one finger on my sweetheart... you're gonna get what's coming to you!"

**Cured**
38. "Now that I'm not a vampire anymore, I think we should take it more easy with the adventuring things... I feel as fragile as a skeleton."

---

## 3. Romance with the player (SDA)

**How it is tracked.** There is no faction rank. The romance is a chain of separate quests plus a few globals. Each quest's opening line only plays at that quest's stage 0 or 5, so they play once and in order. Most are hooked to Dawnguard progress. Romance 04 and 09 are started by Story Manager nodes (`SDA_SeranaRomance4QuestNode` 5279B7, `SDA_SeranaRomance9QuestNode` 52CABB).

| What | EditorID | FormID (SeranaDialogAddon.esp) |
|---|---|---|
| Romance on or off | `SDA_SeranaRomance` (GLOB, default 1) | A2D563 |
| Friendship unlocked | `SDA_Friendship` (GLOB, 0 then 1) | 4162C4 |
| Days-together timer | `SDA_RelationshipTimer` / quest `SDA_TimerQuest` (script SDA_RelationshipTimerScript) | 401EB9 / E4A90F |
| Radiant romance (kisses, cuddles, "in the mood") | quest `SDA_RadiantLoveConvo`, global `SDA_SeranaRadiantLove` | A5AE9F / A5AEA2 |
| Married | `SDA_IsSeranaMarried` (GLOB) + `SDA_MarriageFaction` added to the player | GLOB in SDA |
| Trust talk timers | `SDA_TrustTimer`, `SDA_TrustTimerInit` | 46C3ED / 46C3F1 |

**How the romance opens**
- `SDA_Friendship` becomes 1 after about **7 days of following** (the timer script), or when **Beyond Death (DLC1VQ05) completes**.
- When DLC1VQ05 completes, a message box (`SDA_RomanceFailsafeScript`) asks whether the player wants the romance.
  - **Yes:** `SDA_SeranaRomance = 1` and the radiant romance starts.
  - **No:** `SDA_SeranaRomance = 0` and the radiant romance stops.

**The romance chain.** Stage meanings are worked out from the lines each quest plays.

| Quest (EditorID, FormID) | Name | When / what happens |
|---|---|---|
| SDA_SeranaRomance01 A2D564 | An Unexpected Meeting | Bloodline, on the way home. "Why are you doing this for me?" She is not sure yet whether she can trust Luna. |
| SDA_SeranaRomance02 A37773 | Pressing On | At the castle, after Harkon's cold welcome. "I'm glad you're here with me." |
| SDA_SeranaRomance03 A3777F | Companionship | Soul Cairn. "I... I like you. As a friend... and as aaa... travelling companion." The courtyard flirt. |
| SDA_SeranaRomance04 A929B9 | A Confession | After the Soul Cairn: "Do you... like me?" If yes: **first kiss** (Romance4Kiss / PostKiss). If no: "Still, thanks for being there. As a friend." |
| SDA_SeranaRomance05 AD97E6 | La Panne | Rest stop. They sleep together; she sings "Old Stone Walls". "I'm not exactly the marrying type." |
| SDA_SeranaRomance06 B16416 | L'étreinte | Before the bow hunt. Teasing about Durnehviir as Luna's "soulmate". |
| SDA_SeranaRomance07 B2A82D | Coruscation in the Vale | Forgotten Vale. "I really wouldn't be head over heels for you." |
| SDA_SeranaRomance08 B2A83E | Determination | Before the final fight. She breaks down: "I'm just trying to run away from all these... feelings." |
| SDA_SeranaRomance09 B2A842 | A New Family | After Harkon dies. "You are my savior... **I love you.**" She asks for a date "someplace beautiful". |
| SDA_SeranaRomance10 B2F967 | A New Covenant | The date: a drinks menu and a token "to tie the knot". "I love you... For eternity." This is effectively the marriage (`SDA_IsSeranaMarried`). |
| SDA_SeranaRomance10Trust 46C3EC | Trust Conversation | She confesses she manipulated Luna at their first meeting, and asks forgiveness. |
| SDA_SeranaRomance11 C73A4A | A Date at the Bannered Mare | An evening date in Whiterun with Ysolda serving. Stages 10, 20, 40, 50, 55. She pays, kisses Luna and gives an enchanted amulet. |
| SDA_SeranaRomance12 56E84B | Friendship Conversation | "I chose you, and you chose me." Her nightmares about Molag Bal. |
| SDA_SeranaRomance13 347A07 | Undying Love | Beach date on the northern coast. "A vampire and a vampire hunter... now enjoying drinks and kisses by the beach." |

**For our mod: keep this optional.**
- The user almost always romances **Kaidan**, so the default Serana should be a friend.
- Gate any romance line on Serana's own quests. Example: `GetStageDone SDA_SeranaRomance04 >= 20` and `SDA_SeranaRomance == 1`.
- Never fire romance lines when Kaidan's K04 romance is active, unless the user later asks for that.
- If the player said **no** at Romance04, she says "As a friend." From then on, friendship-only lines are the right register.

**Jealousy reactions she already has.** These are mild. **No SDA line reacts to Kaidan or any other romanced follower.**
- **The player is married to someone else** (`DLC1NPCMentalModelYesAnd` and `AdulteryZOMG`):
  - "Don't you already have someone at home waiting for you?"
  - "I'm not going to be the one to destroy a marriage."
- **Someone hits on her**:
  - To Sybille: "Can't you see my lover here?"
  - To Mikael: "I haven't given you anything, and it'll stay that way."
- **Combat, protective:** "If you lay one finger on my sweetheart... you're gonna get what's coming to you!"
- **The Ashe patch (only in a three-way romance)**:
  - Ashe says "Jealous?" and Serana answers "Competitive." (FantasyMode03).
  - Group-romance teases (GroupRomanceTease01, FantasyMode01-04).
- **Flirt refusal while not romanced:** "...sorry, I'm not interested."

For our cast this is new ground. A jealousy beat would have to be written fresh and gated on both romances.

---

## 4. Her opinions of other followers

**Where each of our cast stands**

| Follower | Real lines? | What they show |
|---|---|---|
| Inigo | **Yes**, a lot (SDA) | Warm. She teases him ("pretty kitty", "kitty-cat"; "Do you ever purr when you're happy?"), buys his mead ("It'll be my treat"), makes kill wagers, and confides the Molag Bal ceremony to him. Drinking Buddies opinion: "Inigo always finds a way to lift our spirits... If there's someone - besides me - to always keep by your side, I think it should be him." |
| Remiel | **Yes**, a lot (SDA) | Friends. Remi studies her in notebooks and Serana lets her. They argue once about necromancy. They share desserts. Opinion: "Oh, Remiel! She's great!... I can jest freely with her, for one. And she's the booky type." From Remi's side: "I like Serana. Her dry humour gets me." |
| Ashe | **Yes**, the most (Ashe patch) | Close friend and foil (section 5C). |
| Kaidan | Kaidan side only | From Kaidan's mods: protective, unafraid ("I'm not afraid of you, or your curse"), asks about her family, "Oi, Serana?". **SDA has no line about Kaidan.** |
| Gore | Gore side only | Distrust first: "Hey, between you and me... I don't trust this 'Serana.'" Later sympathy: "I definitely felt there was some kind of hurt there when she talked about her family." She has no lines about him. |
| Xelzaz | Xelzaz side only | Suspicious: "Is Serana perhaps a spy?" Ambivalent at the end, but hopes for her: "perhaps there is hope for Serana. If she returns to the fold of the living..." He fears for Luna being turned into a vampire. She has no lines about him. |
| Val Serano | None | No line either way. |
| Lucien | One line, patron-only | "Inigo and Lucien are like the brothers I never had." It sits in a patron custom conversation (Selene) and only plays for that custom player, so it is **not live for Luna**. |
| Redcap | None | No line either way. |

**Other followers she has real opinions on (not our cast)**
- **Auri:** "a good person", but the sacred tree belief and fermented pig milk are "a bit weird".
- **Sofia:** "Ugh... what is it with her and having just about everything be sexual?"
- **Lydia:** "it seems like everything is based off of duty."
- **Recorder:** "a bit too bookish". **Vilja:** "doesn't like me very much". **Aurlyn:** "priggish". **Mirai:** "only seventeen?".

**Invented guesses (NOT canon, for writers).** These follow from her character.
- **Kaidan:** she would like his bluntness and tease him about the "brooding" and the horker sandwiches. He is a former Thalmor prisoner and she was a coffin prisoner, so they share being caged. His hatred of Daedra lines up with her loathing of Molag Bal. Keep his cult past out until it is gated.
- **Gore:** she would answer his early distrust with dry amusement ("blood" is a funny word to call a vampire). She would warm up when he is sincere, and might help him with reading the way Remi does.
- **Val:** two vain, witty aristocrat types. She would needle his hair and his age ("you're practically young"). She would respect his Hermaeus Mora history as a fellow Daedra survivor, without asking.
- **Xelzaz:** a friction pair. He distrusts vampires; she finds his food snobbery hilarious. They agree on hating Daedra worship (he hates it, she suffered it). They would trade alchemy notes, since her mother was a master alchemist.
- **Lucien:** she would adore the scholar. She is a bookworm who missed thousands of years of history. She would teach him First Era trivia and enjoy scaring him in crypts.
- **Redcap:** she would be amused that he names her something like "Bite fa-ka". She has no hunger for a Riekling: "I'd rather drink a horker."

---

## 5. Existing cross-follower banter (copy the method, avoid the topics)

### A. SDA_FollowerBanter (E96818:SeranaDialogAddon.esp) - Serana's own banter quest

**The quest**
- Flags: StartGameEnabled, RunOnce, priority 15.
- Scripts: `SDA_FollowerBanterProperties` and `SDA_DaegonCommentScript`.
- Quest-level dialogue conditions:
  - **DLC1VQ02 Bloodline completed**
  - `GetVMQuestVariable(DLC1NPCMentalModel, ::IsFollowing_var) == 1`
  - `SDA_AlternateVoice == 1`

**Aliases**
- `SeranaAlias` is an external alias from **DLC1NPCMentalModel** (002B6E:Dawnguard.esm).
- `PlayerAlias`.
- One optional alias per partner: InigoAlias, SofiaAlias, AuriAlias, RemielAlias, ViljaAlias, RecorderAlias, MiraiAlias, AurlynAlias, and DaegonAlias (ID 12).

**How partners are found**
- `SDA_ModCheck` runs `SDA_ModCheckScript`. Its source ships as `scripts\sda_modcheckscript.psc` in SeranaDialogAddon.bsa.
- On OnInit and on every load it calls `ModScan(alias, formID, "Plugin.esp", SDA_<X>Installed)`, which runs `GetFormFromFile` and then `ForceRefTo`.
- Partner references:
  - Inigo: `0x8AE9` in Inigo.esp
  - Remiel: `0x33226` in HLIORemi.esp
  - Auri: `0x12DB` and `0x3139C8` in 018Auri.esp
  - Sofia: `0x1827` in SofiaFollower.esp
  - Vilja: `0x12C4` in EMCompViljaSkyrim.esp
  - Recorder: `0x2306` in Recorder Follower Base.esp
  - Mirai: `0xD65` in zMirai.esp
  - Aurlyn: `0x5903` in Aurlyn.esp
- **This is the same soft-dependency method Remi and Xelzaz use.**

**Trigger**
- The engine idle-chatter roll picks an INFO in the Idle topic **`SDA_FollowerBanterIdleTriggers`**. There are 98 of them, one opener per talk, for both speakers.
- The INFO's fragment starts the Scene and sets a cooldown. For example `SDA__TIF__05EDD63E` runs `SDA_InigoBanterRadiant2.Start()` and then `InigoCooldown()`.
- The cooldown is **`SDA_BanterCooldown<Name> = GameDaysPassed + 2`**, so each partner gets at most one talk every 2 game days.

**Conditions on a typical opener** (Inigo, INFO EDD63E):
- `GetIsID DLC1Serana`
- `GameDaysPassed >= SDA_BanterCooldownInigo`
- `SDA_Friendship == 1`
- `IsInScene == 0` on Serana and on the partner
- `IsTalking == 0`
- `GetInSameCell(partner)`
- `GetDistance(partner) < 600`. Remi uses ≤ 450.
- Not sneaking
- **`SDA_BanterTracker<Name> >= N`**, a counter that steps the talks in order
- **`SDA_BanterToggle<Name> == 1`**, an MCM switch
- **`SDA_PlayerInDialogue == 0`**
- Not LocTypeDungeon (on most)
- `HasKeyword Vampire` on Serana, for the vampire-themed talks

There is no GetRandomPercent on these openers. Pacing comes from the 2-day cooldown and the tracker.

**Inigo** (scenes SDA_InigoBanter*; Serana is a0, Inigo a1)
| Talk | Topic |
|---|---|
| Introduction | He smells that she is a vampire; "I hope you do not want to suck my blood." |
| R1 | "I'm not that kind of vampire." |
| R2 | How it feels to be a vampire; she holds something back. |
| R3 | Nords drink; she treats him to mead. |
| R4 | His father's saying, "alcohol is not the answer...". |
| R5 | "kitty-cat" / "pretty kitty" teasing. |
| R6 | "Your blood, please." joke. |
| R7 | Does he purr; she tries a back-scratch. |
| R8 | The degrading vampire ceremony. |
| R9 | Kill-count wager. |
| R10 | Bow and sword versus mage. |
| R11 | Drink order (Black-Briar). |
| R12 | Nord warriors versus "blue abomination". |
| BloodPotion01 | Her blood potions; cow blood. |
| VampiresWerewolves | They both hate draugr ("they would also have the time to take some much needed showers"). |
| VampireSpiders | "Smells like vampires and spiders in here." |
| VampireBats | Turning into bats; the Vampire Lord form she despises. |
| Books01 | She works out an alchemy formula. |
| PlayerHome01 | His bandit taunts. |
| PlayerHome02 | "How are you feeling?" |
| Cooking01/02 | Cooking at a spit. These play when `ScanCookingSpit()` finds one and rolls 5% or 15%. |

**Remiel** (scenes SDA_RemielBanter*; Serana a0, Remi a5)
| Talk | Topic |
|---|---|
| Introduction | A flood of questions about blood. |
| R1 | How drinking blood works. |
| R2 | Garlic and stakes myths; the elder vampire who was "allergic". |
| R3 | Remi's notebooks studying her. |
| R4 | "Your blood, please." joke. |
| R5 | Liquid diet means no teeth problems. |
| R6 | **Necromancy argument**; she tells Remi "you're free to leave". |
| R7 | Blood taste, diseases, detecting Sanguinare Vampiris. |
| R8 | **Aetherium Wars**; she is about 4,500 years old. |
| R9 | Hating being underground. |
| R10 | Falmer and the Snow Prince. |
| R11 | Spellbreaker and the Rourken clan. |
| R12 | Food at the inn; ale; sharing a Boiled Creme Treat. |
| R13 | "Order me a wine"; "You're not trivial, Serana." |
| R14 | Comforting her after Harkon. |

**Auri** (13 talks + intro)
- The Green Pact and warmth without fires.
- Both of them "eat enemies".
- Rotmeth; drinks.
- Do Valenwood trees move?
- Bosmer cities without wood.
- Feeding on living prey.
- The "liquid diet".
- Auri eating corpses.
- "So... that was your mother."
- The drunken Bosmer joke.

**Sofia** (13 talks + intro + force-greet after 20 days together)
- Drinking.
- Bards College humour.
- Milk drinker.
- Smooth talker.
- Steak and garlic.
- Plus a player chat about Sofia being "too much".

**Daegon** (intro + 31 talks)
- A custom witch follower travelling with "Kaeserius". Topics: Prince and Princess, Korpse, blood in the mead, Snow Elves, shadow magic.

**Hello one-liners only:** Vilja, Recorder, Mirai, Aurlyn.

### B. SDA town NPC banter (not followers; avoid the same jokes)

`SDA_NPCBanterMain` (8983B9), `SDA_NPCBanterAux` and one quest per NPC:
- Ysolda: inn dreams; she flirts with Serana.
- Belethor.
- Gunmar.
- Carlotta: "my Whiterun Rose"; Mikael has proposed ten times.
- Hod.
- Lisette.
- Grelka.
- Sybille: "Do you take your blood straight up, or on the rocks?"
- Sorine.
- Jarl Balgruuf.
- Mikael: she rebuffs him.
- Nazeem.
- Elisif.
- Taarie.
- Mjoll.
- Talen-Jei.
- Maven.
- Camilla.
- Orgnar.
- Delphine.

### C. Ashe and Serana Banter Patch (MM_AsheranaBanterMain 00AA1A:Ashe and Serana Banter Patch.esp)

**The quest**
- Aliases: AsheAlias (UniqueActor Ashe), SeranaAlias (UniqueActor DLC1Serana), Agmaer, Player.
- Event conditions: Serana `IsFollowing_var == 1` **OR** Ashe `IsFollowing_var == 1`.

**Trigger method**
- Quest script `MM_AsheranaBanterScript` keeps one Conditional bool per talk, so each talk plays once.
- `MM_AsheranaCooldownScript` keeps cooldown globals (`StartCooldown(gv, delay)` sets `GameDaysPassed + delay`):
  - a master cooldown
  - Radiant, Inn/Home, Sleep, LocAware, FantasyMode, Scripted, Suspicion, Wine, Campfire, Soul Cairn
  - NormaltoCombat, CombatTaunt, CombatEnd
- Combat talks come from the alias script `MM_AsheranaBanterTrigAlias.OnCombatStateChanged`. It fires when both are following, the location is not marked safe, and Ashe is not already in a scene. It waits 3 s and then starts `MM_AsheranaNormaltoCombatStarter` or `MM_AsheranaCombattoNormalStarter`.

**Topics covered**
- **Dawnguard story beats:**
  - VQ01: meeting Agmaer; Ashe's "experimental Muffle" heartbeat cover story.
  - VQ02: the boat home; the corrupt air.
  - VQ03: the College; the Moth Priest; the ambush.
  - VQ04: the lab and the hook.
  - VQ05: the Soul Cairn; Valerica: "I hate her for what she did. And I missed her so much"; the undead dragon "crush"; post-love-making awkwardness.
  - VQ06: the Ancestor Glade, squirrel, waiting outside.
  - VQ07, the whole Forgotten Vale: cave, camp, Darkfall, Falmer, wayshrine, frost troll, ice dragon, waterfall swim, bridge, spiders, temple, traps, Gelebor.
  - VQ08: start on either side; the hunter invasion; Harkon; after Harkon.
- **Ashe's own quest beats:** the prologue flashbacks, the AMQ01 automaton reveal, and AMQ02 to AMQ07 (Calcelmo, Rolen, the saber cat den, the blood trail, the Throat of the World).
- **Radiant talks:**
  - outfits ("boob window")
  - vampire hunger
  - automaton existence and taste
  - memories
  - vampire misconceptions (garlic, stakes)
  - is she waterproof
  - dreams
  - sunlight (she is "a creature of the night and a daughter of the sun")
  - the lake / swimming
  - morning brandy, evening grumpiness
  - alchemy (her mother)
  - sweet roll
  - "pumping iron"
  - sword cleaning
  - reading A Gentleman's Guide to Whiterun
  - reborn as
  - humming
  - a romantic evening
  - fathers and rebellion
  - location talks: College, Jorrvaskr, Thieves Guild, ice cave
  - group romance and FantasyMode
  - Ashe's suspicious breathing / metabolism (Suspicion01-03)
- **Combat:** about 23 combat-start, 10 taunt and 8 combat-end exchanges.

### D. Remi's own Serana lines (HLIORemi.esp)

- **Hellos:** "I like Serana. Her dry humour gets me." / "Do you think Serana is doing alright? With all this sun?"
- **Attack barks:** "Serana, if you want to drink their blood, I won't tell anyone!"
- **Idle lines:** about the Moth Priest and the Arch-Curate.
- **Quest `HLIOSeranaPotions` (283FA3):** Remi brews potions with Serana. There is also "Serana, your parents aren't exactly... conventional, are they?"
- **SDA Remiel Banter Patch.esp** adds `GetGlobalValue(SDA_Disabled) == 0` to 9 of Remi's own Serana idle lines. `SDA_Disabled` defaults to **1**, so those 9 are **off**, and SDA's version plays instead.

### E. Lines about her in other mods (not two-way banter)

- **Kaidan:** see kaidan.md section 4.
- **Gore:** the HD1GoreIdles distrust line, plus the Dawnguard reflection.
- **Xelzaz:** about 14 Dawnguard commentary lines in BPUFXelzazDawnguard* (spy suspicion, Valerica's journal, the Soul Cairn, the ending verdict).
- **Val, Lucien, Redcap, Inigo.esp:** none.

---

## 6. Technical

| Item | Value |
|---|---|
| NPC base | `DLC1Serana`, **002B6C:Dawnguard.esm** (runtime 02002B6C). The live winner is Authoria - Patch - Serana UBE Face.esp (7 overrides). Race 00UBE_NordRace. Flags: Female, Unique. |
| Placed reference | `DLC1SeranaRef`, **002B74:Dawnguard.esm**. SDA also places two extra copies, 217CCD and 217CCE (scene helpers); never use those. |
| VoiceType | **`DLC1SeranaVoice`**, 002B6F:Dawnguard.esm. |
| Factions | DLC1SeranaFaction 0183A5, DLC1SeranaCrimeFaction 0137BA. |
| Follower quest (vanilla) | **`DLC1NPCMentalModel`**, 002B6E:Dawnguard.esm, script `DLC1_NPCMentalModelScript`. Live winner: Authoria - Haberdashery.esp. |
| **Is-following check** | **`GetVMQuestVariable(002B6E:Dawnguard.esm, ::IsFollowing_var) == 1`**. Both SDA and the Ashe patch use this. Other ways: `DLC1SeranaRef.IsPlayerTeammate()` in script, or **GetPlayerTeammate == 1**. Neither SDA nor the Ashe patch tests CurrentFollowerFaction for her. I did not check whether she is in it, so use IsFollowing_var instead. |
| Can-follow check | `::CanFollow_var == 1` on the same quest. It is false while the story has taken her (castle stays, scenes). SDA's main quests require it. |
| Story gates | DLC1VQ01 Awakening 00352A · **DLC1VQ02 Bloodline 002F65** (all SDA banter needs it completed) · DLC1VQ03Hunter 0098CB / DLC1VQ03Vampire 004C3D · DLC1VQ04 Chasing Echoes 00284F · **DLC1VQ05 Beyond Death 002850** (opens friendship and the romance prompt) · DLC1VQ06 002852 · DLC1VQ07 002853 · **DLC1VQ08 Kindred Judgment 007C25** (Harkon dead) · DLC1VQ08Post 01A1C1. |
| Vampire or cured | `HasKeyword Vampire (0A82BB:Skyrim.esm)` on Serana: 1 means vampire, 0 means cured. The SDA cure timer quest is `SDA_CureQuestTimer` 5EE3E9. |
| SDA busy / silence globals to respect | **`SDA_PlayerInDialogue`** 9EB814 must be 0. `SDA_AlternateVoice` 5CE511 must be 1 (all SDA banter needs it). Per-partner `SDA_BanterToggle*` (Inigo 741CC6, Remiel 741CC7, Auri 741CC5, Sofia 741CC8). Cooldowns `SDA_BanterCooldown*` (Inigo ABD796, Remiel AC289E). `SDA_DaegonBanterCooldown`. `SDA_Talkie`, `SDA_Humming`, `SDA_Sneeze` (idle-chatter toggles, all 1 by default). |
| Scenes to stay out of | `IsInScene == 0` on Serana; SDA uses it on every opener. SDA's many scripted quest scenes all run through SDA_* quests, so IsInScene covers them. The romance quests SDA_SeranaRomance01-13 while running. Drinking Buddies (`SDA_DrinkingBuddies` 61AB00, `SDA_DrinkingBuddiesWaiting`). Sleeping (`SDA_SleepingQuest` D29EB8). Horse riding (`SDA_SeranaRideHorse`). The cure absence (between the cure talk and her return home). |
| Banter-quest model to copy | An Idle-topic opener with conditions, a fragment that starts the Scene and sets a `GameDaysPassed + 2` cooldown, a tracker global to keep order, and an MCM toggle. Partner aliases filled with GetFormFromFile, exactly like SDA_ModCheckScript. |

**Suggested opener conditions for a Serana talk in our mod**
- `GetIsID DLC1Serana` (or `GetIsAliasRef`)
- `GetQuestCompleted DLC1VQ02 == 1`
- `GetVMQuestVariable DLC1NPCMentalModel ::IsFollowing_var == 1`
- `IsInScene == 0` on both speakers
- `SDA_PlayerInDialogue == 0`
- Partner distance < 600, same cell, partner GetPlayerTeammate == 1
- Story gates per line:
  - DLC1VQ05 done for Valerica talk
  - DLC1VQ08 done for "Harkon dead"
  - Vampire keyword 0 for "cured"

---

## 7. Voice reference (for OmniVoice)

**Important: two actresses, plus a usage restriction.**

**1. SDA is not AI.**
- SDA's Serana is voiced by a human actress, **Kerstyn Unger** (mod page credits).
- She re-voiced Serana's vanilla Dawnguard lines too: the mod page says "Dawnguard Quest Revoice = 100%".
- That is why the SDA archive replaces **816** of the 1,008 vanilla Serana files. In this load order Serana mostly sounds like Kerstyn. Only **202** vanilla lines still play in the original actress's voice (Laura Bailey).

**2. The SDA author bans AI use of the recordings.** The SDA mod page says: "Use of the voice recordings included in this Mod for artificial intelligence training or generation is strictly prohibited." Cloning from SDA files would break that rule.

**3. Cloning from vanilla means a mismatch.** Cloning from the vanilla Bethesda files (Laura Bailey's performance) avoids the SDA restriction, but the result will **not** match the Kerstyn voice heard in-game. Cloning a real actress from game files is the user's call.

Both options are listed below. **I recommend not using the SDA files.**

**Where her voice files are**

| Source | Location | Files | Actress |
|---|---|---|---|
| Vanilla | `C:\1. AUTHORIA\Stock Game\Data\Skyrim - Voices_en0.bsa`, inside `sound\voice\dawnguard.esm\dlc1seranavoice\` | 1,008 | Laura Bailey (original). 816 are replaced by SDA in-game. |
| SDA new lines | `C:\1. AUTHORIA\mods\Serana Dialogue Add-On\SeranaDialogAddon.bsa`, inside `sound\voice\seranadialogaddon.esp\dlc1seranavoice\` | 8,226 | Kerstyn Unger (no AI use allowed) |
| SDA re-voice of vanilla | the same BSA, inside `sound\voice\dawnguard.esm\dlc1seranavoice\` | 816 | Kerstyn Unger (no AI use allowed) |
| SDA patches | `C:\1. AUTHORIA\mods\Serana Dialogue Add-On Patch Hub - rerun\Sound\` (loose) | - | Kerstyn Unger |
| Ashe banter | `C:\1. AUTHORIA\mods\Ashe - Crystal Heart - SDA\Ashe and Serana Banter Patch.bsa` | - | Serana lines presumably Kerstyn; not checked |

**Five calm clips, all from the original voice (vanilla, not replaced by SDA).**
- Archive: `C:\1. AUTHORIA\Stock Game\Data\Skyrim - Voices_en0.bsa`
- Folder inside it: `sound\voice\dawnguard.esm\dlc1seranavoice\`
- Format: .fuz (lip data + xWMA); unpack to .wav before cloning.
- Lengths were read from the audio headers. I picked them by text and length and **did not listen to them**; check by ear.

| # | Length | File | Line |
|---|---|---|---|
| 1 | 8.2 s | `dlc1npcmen_dlc1npcmentalmo_00004abf_1.fuz` | "My father... no, not really. I did spend a lot of time with my mother, but she saw me more like a protege than a daughter." |
| 2 | 7.5 s | `dlc1npcmen_dlc1npcmentalmo_00004a26_1.fuz` | "I know how that feels. I mean... I know it isn't the same thing. But I was a pretty lonely child, myself." |
| 3 | 6.3 s | `dlc1npcmen_dlc1npcmentalmo_00004a11_1.fuz` | "You've already seen my father's obsession. My mother's not a whole lot better, but you'll see that soon enough." |
| 4 | 5.2 s | `dlc1npcmen_dlc1npcmentalmo_00004a32_1.fuz` | "We didn't all get to have parents like yours. Sometimes this is just... how it is." |
| 5 | 5.2 s | `dlc1npcmen_dlc1npcmentalmo_00004a31_1.fuz` | "I think both of our parents have failed us. Just you and me against the world, now." |

**For reference only, not for cloning.** These calm lines play in **Kerstyn's** voice in-game, because SDA replaces them. They let you hear what the game actually sounds like:
- `...\dlc1vq04__0000d7e5_1.fuz` (9.0 s): "This was my mother's garden..."
- `...\dlc1vq05_dlc1vq05hellos_00008389_1.fuz` (7.3 s): "I'd heard stories about the Soul Cairn..."
- `...\dlc1rnpcge_dlc1rnpcgeneral_00004b65_1.fuz` (6.1 s): "From the castle, you used to just be able to see Solitude..."

Find them inside `SeranaDialogAddon.bsa` under `sound\voice\dawnguard.esm\dlc1seranavoice\`.

**Cloning advice.**
- Clips 1, 2 and 5 together give a quiet, reflective, natural voice.
- Avoid the combat barks, the vampire-lord taunts and the "*Sighs*" or sobbing romance lines.
- If the clone should match what the user hears in-game, the user has to decide about the SDA restriction first.
