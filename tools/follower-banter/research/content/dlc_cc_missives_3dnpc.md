# Content research: Dawnguard, Dragonborn, Hearthfire, Creation Club, Missives, 3DNPC

Built 2026-10-18 from the live load order (MO2 `C:\1. AUTHORIA`, profile `DEEZ CS NUTZ - PICTA`, houseCARL epoch e2-6f1c37c9b1e44807). Read-only: nothing in the game was changed.

How it was read:
- Quest names, stage numbers and journal text come straight from the records. Dawnguard, Dragonborn, 3DNPC and Missives text was read with houseCARL.
- The Creation Club plugins are "localized" (their text lives in separate string files). For those I pulled the English string files out of each CC archive and matched them to the quest records, so the CC quest names and journal lines below are the real in-game ones.
- "Existing lines" were found by searching every follower plugin for dialogue whose conditions point at a DLC or CC quest. That gives topics only, no line text.

FormID style: `XXXXXX:Plugin.esp`. A stage marked **[COMPLETE]** or **[FAIL]** carries that journal flag. "Start" means the first stage that writes a journal line.

Gate shorthand used in the hooks: `Done(Q,s)` = `GetStageDone Q s == 1`. `Run(Q)` = `GetQuestRunning Q`. `In(L)` = player `IsInLocation L` (child locations count). `WS(W)` = player `GetInWorldspace W`.

---

## 0. Quick facts that change how you write

1. **Followers do not go everywhere.** In the vanilla game nobody but Serana enters the **Soul Cairn**, and nobody follows you into **Apocrypha** through a Black Book. The party waits outside. That makes the return the best banter moment: "you were gone, and you came back smelling of ink / of grave dust".
2. **Two Dawnguard paths.** The player either joins Harkon (vampire path, `DLC1VQ03Vampire`) or refuses (Dawnguard path, `DLC1VQ03Hunter`). Both use the same later quests. Gate path-specific lines on which Prophet quest ran.
3. **Solstheim is home turf for two of ours.** Redcap is a Riekling born on Solstheim. Xelzaz is a Telvanni Lawman, so Tel Mithryn, Neloth and Raven Rock are his world. Val once served Hermaeus Mora and has already walked an Apocrypha built from his own memories (his quest Val005).
4. **Ghosts of the Tribunal, a CC quest, is set at a hidden temple near Raven Rock.** It is a second Solstheim/Morrowind storyline for Xelzaz.
5. **The Cause, a CC quest, is a Mehrunes Dagon / Mythic Dawn plot that ends in the Deadlands.** Kaidan's whole past is a Dagon cult (the Blooded Dawn) and he has his own Deadlands questline. This is the strongest single hook in the CC set.
6. **Survival Mode CC is present but switched off by an Authoria patch.** `CCSurvival - Disable Shrine Menu.esl` is active. The live gate is `Survival_ModeEnabled` `000826:ccQDRSSE001-SurvivalMode.esl == 1`. Don't write survival-mode banter unless that is 1.

---

## A. Dawnguard

### A1. Spoiler summary for the writer

Vampires attack the Vigilants of Stendarr. Isran, a gruff ex-Vigilant, is rebuilding the old vampire-hunter order, the **Dawnguard**, at Fort Dawnguard in Dayspring Canyon. He sends the player to **Dimhollow Crypt**, where they wake **Serana**, a pure-blooded vampire who has been sealed away for centuries with an Elder Scroll strapped to her back.

The player takes her home to **Castle Volkihar**, on an island off the north coast. Her father, **Lord Harkon**, offers the player the gift of his blood:
- **Accept:** the player becomes a Vampire Lord and joins Harkon's court.
- **Refuse:** they are thrown out and go back to Isran.

Either way, Harkon wants to fulfil a prophecy called the **Tyranny of the Sun**: use **Auriel's Bow** to blot out the sun forever. Serana turns against her father.

To read the prophecy, the party needs a **Moth Priest** (Dexion). He is kidnapped and enthralled at Forebears' Holdout. They then need two more Elder Scrolls:
- the Dragon scroll, from the College or the Throat of the World;
- Serana's mother **Valerica**'s scroll, which is in the **Soul Cairn**, a plane of trapped souls run by the Ideal Masters.

To enter the Soul Cairn the player must be part-dead: either a vampire, or soul-trapped by Serana. Inside, Valerica explains that Serana's blood (a daughter of Coldharbour) is the key to the prophecy. The undead dragon **Durnehviir** fights them, and later offers to fight alongside the player in exchange for being summoned back to Tamriel. In the Soul Cairn there is also **Jiub**, the prisoner from Morrowind's opening, who is writing his second book.

Reading the scrolls blinds Dexion. The player then reads them at the **Ancestor Glade** by drawing bark and moths, and gets a vision of **Darkfall Cave**. That leads to the **Forgotten Vale**, a hidden Snow Elf valley, where the paladin **Gelebor** asks the player to kill his corrupted brother **Vyrthur**. Vyrthur created the prophecy as revenge on Auri-El. The player gets the bow.

In the finale, **Kindred Judgment**, both paths storm Castle Volkihar and kill Harkon. A vampire player who still chose Serana over her father kills him too.

Side content:
- **Lost to the Ages:** the ghost Katria and the Aetherium Forge, under Arkngthamz. Dwemer.
- Radiant hunter and vampire jobs.
- Gargoyles and death hounds.
- Eclipse attacks on the road.
- Florentius, the slightly mad priest of Arkay.
- Sorine Jurard, the crossbow tinkerer, and Gunmar, the troll trainer.

### A2. Quests (live records)

| Quest | FormID | Name | 1-2 line summary | Start / key / complete |
|---|---|---|---|---|
| DLC1VQ01MiscObjective | 00D06C:Dawnguard.esm | Dawnguard | The rumour that the Dawnguard is recruiting. | Start 10 "I've learned of a group of vampire hunters known as the Dawnguard..." · Complete **180** |
| DLC1VQ01 | 00352A:Dawnguard.esm | Awakening | Meet Isran, go to Dimhollow Crypt, free Serana. | Start 10 "I've met Isran..." · 40 Serana freed · Complete **200** |
| DLC1VQ02 | 002F65:Dawnguard.esm | Bloodline | Escort Serana home; Harkon's offer. | Start 5 · 20 met Harkon · **25/30 refused**, **40 accepted** · Complete **180 = accepted** ("I accepted the gift and joined his court"), **190 = refused** ("I refused the gift, and was banished") |
| DLC1HunterBaseIntro | 004E24:Dawnguard.esm | A New Order | Refused path: back to Isran, recruit Sorine and Gunmar. | 20 "I've rejected Harkon's offer..." · 30 · 70 · Complete **200** |
| DLC1VampireBaseIntro | 00594C:Dawnguard.esm | The Bloodstone Chalice | Vampire path: fill the chalice at Redwater Den; Garan's loyalty test. | 10 "It is time." · 40 ambushed by Stalf and Salonia · Complete **200** |
| DLC1VQ03Hunter | 0098CB:Dawnguard.esm | Prophet (Dawnguard) | Serana comes to the Fort; hunt down the Moth Priest; Dexion reads the scroll. | 7/10 Serana arrives · 45 Winking Skeever · 60/65 Forebears' Holdout · 70 thrall broken · 100 reading · Complete **200** |
| DLC1VQ03Vampire | 004C3D:Dawnguard.esm | Prophet (Volkihar) | Same chase, but you enthrall the priest for Harkon. | 5/10 · 67 "my turn to enthrall the Moth Priest" · Complete **200** |
| DLC1VQElder | 005DA9:Dawnguard.esm | Seeking Disclosure | Find the two other scrolls; Dexion goes blind. | 10 · 40 both scrolls · Complete **200** ("...he's become blind") |
| DLC1VQElderHandler | 0181BF:Dawnguard.esm | Scroll Scouting | Ask Urag at the College about the Dragon scroll. | 20 · Complete **200** |
| DLC1VQ04 | 00284F:Dawnguard.esm | Chasing Echoes | Serana's mother; Volkihar courtyard, Valerica's lab; the portal. | 20 Serana wants Valerica · 35/50/60 · 90 portal · **100 "a hidden force... draining my life energy"** (soul-trap / turn choice) · Complete **200** |
| DLC1VQ05 | 002850:Dawnguard.esm | Beyond Death | Soul Cairn: find Valerica, kill three Keepers, Durnehviir fight. | 10 entered · 30 Valerica · 50 Keepers dead · 80 Durnehviir · Complete **200** "exited the Soul Cairn with the Elder Scroll" |
| DLC1VQSaint | 01400B:Dawnguard.esm | Impatience of a Saint | Jiub's lost pages in the Soul Cairn. | 20 · 30 · Complete **200** |
| DLC1VQDragon | 00C73A:Dawnguard.esm | Durnehviir | The pact: summon him, learn Soul Tear. | **30** pact made · **60** shout fully learned |
| DLC1VQ06 | 002852:Dawnguard.esm | Unseen Visions | Ancestor Glade ritual; read the scrolls yourself. | 10 · 50 moths gathered · 60 in the light column · Complete **200** "...a cave entrance far away on the western edge of Skyrim" |
| DLC1VQ07 | 002853:Dawnguard.esm | Touching the Sky | Darkfall Cave, the Forgotten Vale, Gelebor, Vyrthur, the bow. | 10 · **50 met Gelebor** · 100 ewer filled · 110 Inner Sanctum · Complete **200** |
| DLC1VQ08 | 007C25:Dawnguard.esm | Kindred Judgment | Assault on Castle Volkihar (or Harkon's last stand); Harkon dies. | 20 rally the Dawnguard · Complete **200** |
| DLC1HunterBaseStage2 | 013F1F:Dawnguard.esm | Bolstering the Ranks | Rescue Florentius from Ruunvald. | 10 · 20 · Complete **200** |
| DLC1LD | 005817:Dawnguard.esm | Lost to the Ages | Katria's ghost, the Aetherium shards, the Forge, the Arkngthamz tonal lock. | 100 met Katria · 120 tonal lock · 130/150 shards · 160-225 the Forge (no COMPLETE flag on the log; use 225 or `GetQuestCompleted`) |
| DLC1VampireTutorial | 01909F:Dawnguard.esm | Power of the Blood | Vampire Lord perk tree tutorial. | No journal |
| DLC1RH01-08 | 005E4A…015017:Dawnguard.esm | Hide and Seek, Cleansing Light, Preemptive Strike, Hunting the Monster, Ancient Technology, Rescue, A Jarl's Justice, Lost Relic | Dawnguard radiant jobs. | 10 start · 255 [COMPLETE] (RH07 also 300) |
| DLC1RV01-10 | 004C1B…019938:Dawnguard.esm | The Hunt, Culling the Beast, Deceiving the Herd, Protecting the Bloodline, Ancient Power, The Gift, New Allegiances, Rings of Blood Magic, Amulets of Night Power, Destroying the Dawnguard | Volkihar radiant jobs. RV06 "The Gift" = turn your **spouse**. RV10 = wipe out the Dawnguard leaders. | 10 start · 255 [COMPLETE], 300 [FAIL] on RV03/06/07 |
| DLC1EclipseAttack1-6 | 01629F…01764C:Dawnguard.esm | Eclipse Attack: Gargoyles / Vampires and thralls / Death Hounds ("Oh, my") | Road ambushes. | Run = attack in progress |

Useful NPCs: Serana `002B6C:Dawnguard.esm` (ref `002B74`), Harkon `003BA7`, Isran `00336A`, Valerica `003B8B`, Durnehviir `0030D8`, Gelebor `00A877`.

Useful factions and race:
- `DLC1DawnguardFaction 014217`
- `DLC1HunterFaction 003375`
- `DLC1VampireFaction 003376`
- `DLC1PlayerVampireLordFaction 0071D3`
- Vampire Lord race `DLC1VampireBeastRace 00283A`. Player `GetRace` == this means they are in Vampire Lord form.

### A3. Silence zones (Dawnguard)

- `DLC1VQ02` 8..19: Harkon's throne-room speech and the gift. Already in TRIGGERS.md.
- `DLC1VQ03Hunter` / `DLC1VQ03Vampire` 100..130: Dexion's reading scene.
- `DLC1VQ04` 90..100: the portal/soul-trap conversation with Serana.
- `DLC1VQ05` running: the Soul Cairn. Already a quiet rule. **Also** `WS(DLC01SoulCairn 001408:Dawnguard.esm)` or `In(DLC1SoulCairnLocation 003B8F)`. The normal party is not there anyway.
- `DLC1VQ06` 50..60: the Ancestor Glade ritual and vision. `WS(DLC1AncestorsGladeWorld 0048C7)`.
- `DLC1VQ07` stage 110 done and 200 not done: the Inner Sanctum, Vyrthur's reveal and fight.
- `DLC1VQ08` running: the castle assault. Already a quiet rule.
- `DLC1EclipseAttack*` running: combat ambush. The combat gate covers it, but block the "after-combat" talk until the quest stops.
- Player in Vampire Lord form (`GetRace == DLC1VampireBeastRace`): skip banter. The other followers would be talking to a winged monster. Better: give that its own hook (see A5).

### A4. Arrival triggers (Dawnguard)

| Place | Location / worldspace |
|---|---|
| Fort Dawnguard (interior) / Dayspring Canyon | `0128FE:Dawnguard.esm` / `004C1F` (WRLD `DLC1HunterHQWorld 001DB8`) |
| Castle Volkihar / Volkihar Keep | `004C20` / `00357D` (courtyard WRLD `007202`) |
| Dimhollow Crypt | `004EE8` |
| Redwater Den | `004D6F` |
| Forebears' Holdout | `00357F` (WRLD `002F64`) |
| Soul Cairn | `003B8F` (WRLD `001408`; Boneyard WRLD `00528D`) |
| Ancestor Glade | `003583` (WRLD `0048C7`) |
| Darkfall Cave / Darkfall Passage | `00A87A` / `0162AC` |
| Forgotten Vale / Inner Sanctum / Glacial Crevice | `00A87C` / `01379F` / `0162AF` (WRLD `DLC01FalmerValley 000BB5`) |
| Arkngthamz / Aetherium Forge | `004D6D` / `005826` |
| Ruunvald Excavation | `007B21` |
| Icewater Jetty (boat to Volkihar) | `012409` |
| Moldering Ruins | `003CFD` |

### A5. Ten banter hooks (Dawnguard)

1. **"The girl in the box."** Gate: `Done(DLC1VQ01,40)` and not `Done(DLC1VQ02,180/190)`. Gore says out loud that he doesn't trust "this Serana". Kaidan answers that he's not afraid of her or her curse. Lucien is just thrilled that she remembers the Second Era.
2. **The Elder Scroll on her back.** Gate: `Done(DLC1VQ01,40)`. Lucien's father worked with the Elder Scrolls at White-Gold Tower. He talks about them almost reverently, then catches himself asking whether he could just touch it. Val: "If it's worth that much, I know a buyer." Inigo tells him to ask the lady first.
3. **You said no to a vampire lord.** Gate: `Done(DLC1VQ02,190)`. Redcap: "Fang-man. Offer. Blood. You. Say. No? Smart." Val says he once took a deal from a Daedric Prince and wouldn't recommend it. Xelzaz praises refusing on principle.
4. **You said yes.** Gate: `Done(DLC1VQ02,180)`. A quiet worried pair: Remi and Inigo. Inigo is honest: "I will still travel with you. I will also keep garlic." Kaidan is protective, not preachy.
5. **Vampire Lord form.** Gate: the player is not that race any more, but `Done(DLC1VQ02,180)` and played once after first use (or `IsInFaction DLC1PlayerVampireLordFaction`). After the player changes back, Redcap declares the bat-form "Big. Bat. Chief!" Gore finds the wings "honestly a bit beautiful" and is embarrassed to have said it.
6. **The Moth Priest.** Gate: `Done(DLC1VQ03Hunter,70)` or `Done(DLC1VQ03Vampire,67)`. Lucien explains the Cult of the Ancestor Moth, then goes pale on hearing that reading blinds the priest. Remi, who reads constantly, says "worth it?" and immediately feels bad for asking.
7. **The party left on the doorstep of the Soul Cairn.** Gate: `Done(DLC1VQ05,200)`, first reunion after leaving `WS(DLC01SoulCairn)`. "You were gone for hours." Val: "Did it smell like old parchment or old graves? ...Graves. Good, at least it wasn't him." (Mora). Xelzaz asks clinically what soul-trapping a living person felt like.
8. **Durnehviir's pact.** Gate: `Done(DLC1VQDragon,30)`. Gore and Kaidan argue whether you should trust an undead dragon who "wants fresh air". Redcap is delighted: "Dead-dragon. Friend? Redcap. Ride!" Lucien can't stop saying "Qahnaarin".
9. **The Forgotten Vale.** Gate: `In(DLC1FalmerValleyLocation 00A87C)`, first entry. Remi and Lucien geek out over the Snow Elves and the Falmer. Remi's Dwemer-specialist side meets Lucien's history ("they were people, before the Dwemer..."). Gelebor gets mentioned. Inigo just says it's the most beautiful place he's been.
10. **After Harkon.** Gate: `Done(DLC1VQ08,200)`. A Serana-centred family talk:
    - Val reflects on Tarek, his own terrible father: "at least yours only wanted to blot out the sun".
    - Kaidan on his mother's murder.
    - Gore on the Ravens as family ("blood is a covenant").
    - A campfire-style "worst father" contest that turns sincere.

Bonus side hooks:
- **Lost to the Ages** (`Done(DLC1LD,130)`): Remi and Lucien race to the Aetherium Forge.
- **Florentius** (`Done(DLC1HunterBaseStage2,200)`): Inigo also hears voices, so to speak, and kindly defends him.
- **"The Gift"** (`Run(DLC1RV06)`): the whole party is horrified you'd bite your spouse.

### A6. Existing lines our followers already have (topics only, do not duplicate)

- **Kaidan:** the biggest coverage.
  - `0Kaidan.esp` reacts to Bloodline and Beyond Death.
  - `BWB - Kaidan 2 Extra Dialogue.esp` comments on the whole Dawnguard main quest on both paths: Awakening, Bloodline, A New Order, Bloodstone Chalice, both Prophets, Chasing Echoes, Beyond Death, Unseen Visions, Touching the Sky, Kindred Judgment. It also covers Bolstering the Ranks, Lost to the Ages and the Dawnguard recruit rumour.
  - Bible: protective toward Serana; asks after her family.
- **Xelzaz:** comments on the full main quest (VQ01-08 on both paths, Chalice, A New Order, Scroll Scouting, the Soul Cairn soul-gem handler).
- **Remi:** full main quest, plus Lost to the Ages.
- **Gore:** Awakening, Bloodline, Prophet (vampire), A New Order, Chalice, Unseen Visions, the Dawnguard rumour, the Vampire Lord tutorial. Bible: "I don't trust this 'Serana'" turning into "some kind of hurt there when she talked about her family".
- **Lucien:** Bloodline and Kindred Judgment.
- **Val:** Lost to the Ages (`ValDG02` idles and a Katria scene trigger).
- **Inigo:** nothing keyed to a Dawnguard quest in his plugins. Serana Dialogue Add-On has Serana and Inigo exchanges from her side (cooking, drinks, "you say a lot to every bandit").
- **Redcap:** none keyed to Dawnguard. His word list has "Dawn-pup / Dead-pup" for Dawnguard dogs and death hounds.
- **Serana herself** (SeranaDialogAddon.esp) references Bloodline. Gore's and others' lines about her exist, so new talks should build on them.

---

## B. Dragonborn (Solstheim)

### B1. Spoiler summary

Masked cultists ambush the Dragonborn in Skyrim, carrying a note about **Miraak**. The player sails from Windhelm on the Northern Maiden to **Raven Rock**, a Dunmer mining town on **Solstheim** under House Redoran's control. The island is ash-choked since Red Mountain erupted.

The locals are sleepwalking, building a temple to Miraak around the island's six **All-Maker Stones**. Miraak was the **First Dragonborn**, a Dragon Priest who turned on the dragons and served **Hermaeus Mora**. For thousands of years he has been trapped in **Apocrypha**, Mora's endless library realm, and he plans to come back and enslave Solstheim.

**Frea**, a Skaal warrior, and her father **Storn**, the Skaal shaman, help. The player learns the **Bend Will** shout and cleanses the Stones. The Telvanni wizard **Neloth**, at his mushroom tower **Tel Mithryn**, helps find another **Black Book** in the Dwemer ruin **Nchardak**. In Apocrypha, Hermaeus Mora demands the secrets of the Skaal. Storn gives them up and Mora kills him for it. The player tames Miraak's dragon, flies to the top of Apocrypha and kills Miraak. Mora then claims the player as his new champion.

Side content:
- **Raven Rock:** ash spawn and Falx Carius (*March of the Dead*); the Morag Tong plot against Councilor Morvayn (*Served Cold*); the Bloodskal Barrow mine (*The Final Descent*); Mogrul the loan shark; seven favour quests.
- **Tel Mithryn:** Neloth's research jobs (*Experimental Subject*, *Heart Stones*, *Briarheart Necropsy*, *Azra's Staffs*...); finding a new steward; his ex-apprentice **Ildari**, who has a heart stone in her chest (*Old Friends*); Talvas's Ash Guardian; Elynea's taproots.
- **Skaal Village:** the historian Tharstan and the Dragon Priest Vahlok (*Lost Legacy*); the Thalmor kidnapping the smith over stalhrim; Wulf and his werebear brother.
- **Thirsk Mead Hall:** either retake it for the Nords or help the **Rieklings** keep it (*The Chief of Thirsk Hall*). This one is Redcap's.
- **Kolbjorn Barrow:** fund Ralis Sedarys's dig, who falls under the Dragon Priest **Ahzidal**.
- Also: the pirate king Haknir Death-Brand's armour hunt, **The Ebony Warrior**, the Kagrumez gauntlet, the five optional Black Books, and the Dunmer sellsword **Teldryn Sero**.

### B2. Quests

| Quest | FormID | Name | Summary | Start / key / complete |
|---|---|---|---|---|
| DLC2MQ01 | 017F8E:Dragonborn.esm | Dragonborn | Cultist ambush, sail to Solstheim. | 5 attacked · 7 note · 20 arrived · 30 · Complete **200** |
| DLC2RRArrivalScene | 02ADDA:Dragonborn.esm | Raven Rock Arrival Scene | Docking scene. | Running = silence |
| DLC2MQ02 | 017F8F:Dragonborn.esm | The Temple of Miraak | First Miraak encounter; meet Frea; first Black Book. | 10 · 25 Miraak vanishes · 30 Frea · 40 the book · 60 read · Complete **200** |
| DLC2MQ03 | 017F90:Dragonborn.esm | The Fate of the Skaal | Storn; learn a Word; free the Skaal; kill the Lurker. | 10 · 30 · 50 · 60 monster · 70 · Complete **200** |
| DLC2MQ03B | 035440:Dragonborn.esm | Cleansing the Stones | Free all the Stones. | Complete **200** |
| DLC2MQ04 | 016E1F:Dragonborn.esm | The Path of Knowledge | Neloth, Nchardak. | 10 · 50 · Complete **550** |
| DLC2MQ05 | 0179DE:Dragonborn.esm | The Gardener of Men | Apocrypha; Mora's bargain; **Storn dies**. | 10 · 340 · Complete **1000** |
| DLC2MQ06 | 0179D7:Dragonborn.esm | At the Summit of Apocrypha | Tame the dragon; kill Miraak. | 10 (starts with Storn's death) · 200 · 400 · Complete **550** |
| DLC2BlackBook03-07Quest | 03216C…032170:Dragonborn.esm | Black Book: Untold Legends / The Winds of Change / The Sallow Regent / Filament and Filigree / The Hidden Twilight | Optional Apocrypha trips. | 10 read · **20 [COMPLETE]** |
| DLC2TT1 / TT1b | 017E8D / 01844E | Reluctant Steward / A New Debt | Neloth's dead steward; Drovas; Mogrul's debt. | TT1 complete **500** · TT1b complete **300/310/320** |
| DLC2TT2 | 0195A1 | Old Friends | Ildari's heart-stone attacks on Neloth. | 100 · 500 killed Ildari · Complete **600** |
| DLC2TTR1-8 | 01B65F, 01C06E, 01B65D, 01D8D1, 01B664, 01CDE1, 01C05C, 01BD18, 01F13B | Lost Knowledge, Heart Stones, Telvanni Research, Wind and Sand, Experimental Subject (a/b), Briarheart Necropsy, Azra's Staffs, Hunting and Gathering | Neloth's radiant errands. | 100 start · 300 [COMPLETE] (TTR4a 400 [FAIL] = refused to be his test subject) |
| DLC2TTF1 / TTF2 | 01AAB0 / 01AAC8 | From the Ashes / Healing a House | Talvas's Ash Guardian; Elynea's taproots. | TTF1 complete **300** · TTF2 complete **500** |
| DLC2RR01 | 018B13 | March of the Dead | Ash spawn; General Falx Carius at Fort Frostmoth. | 30 · 90 Carius slain · Complete **200** |
| DLC2RR02 | 018B14 | Served Cold | The Ulen family and the **Morag Tong** plot against Morvayn; Severin Manor. | 10 · 70 evidence · 90 Vendil dead, Morag Tong · Complete **200** |
| DLC2RR03 / RR03Intro | 018B15 / 020A1C | The Final Descent / An Axe to Find | Bloodskal Barrow, Gratian Caerellius. | 15 · 30 · Complete **200** |
| DLC2RRFavor01-07 | 024DDE…02BAC6 | Recipe for Distraction, Fetch the Netch, Clean Sweep, It's All In The Taste, Pain in the Necklace, Feeding the Addiction, First Edition | Raven Rock favours. | 200 complete |
| DLC2SV01 | 019B4A | Lost Legacy | Tharstan; Vahlok's tomb. | 10 · 50 · Complete **200** |
| DLC2SV02 | 01CAF1 | A New Source of Stalhrim | Thalmor kidnap Baldor. | 10 · Complete **200** |
| DLC2WB01 | 0209AE | Filial Bonds | Wulf's werebear brother. | Complete **100** · 205 [FAIL] |
| DLC2MH01 | 01A50B | Retaking Thirsk | Help the Nords; Bujold. | 10 · 20 agreed · **25 retaken** · Complete **100/200** · **210 [FAIL] = you helped the Rieklings keep them out** |
| DLC2MH02 | 01A50C | The Chief of Thirsk Hall | Help the Riekling chief; he turns on you. | 10 · 30 · Complete **200** · 210 [FAIL] |
| DLC2ThirskFF* | 038EBF, 038EC4, 038FBB, 038FBC | Elmus / Hilund / Halbarn Favor Quests | Thirsk favours. | 200 / 205 |
| DLC2dunKolbjornQST | 01810B | Unearthed | Fund Ralis; Ahzidal. | 40 · 100/200/300/400 dig phases · 449-490 Ralis turned · (480+ = the end) |
| DLC2dunHaknirTreasureQST | 024002 | Deathbrand | Haknir's stalhrim armour treasure maps. | 29 · 70 · 100 |
| DLC2EbonyWarriorQuest | 02C49E | The Ebony Warrior | The challenge at his last vigil. | 10 · 100 · Complete **200** |
| DLC2KagrumezQST | 03166D | The Kagrumez Gauntlet | Dwemer gem trials. | Complete **250** |
| DLC2TGQuest | 02AD26 | Paid in Full | Thieves Guild tie-in. | Complete 200 |

NPCs: Miraak `017F7D`, Neloth `01773A`, Frea `017934`, Storn `017935`. Teldryn Sero and Ralis Sedarys: EditorIDs not confirmed, check before use.

### B3. Silence zones (Dragonborn)

- `DLC2MQ01` 5..7: the cultist ambush.
- `DLC2RRArrivalScene` running: the docking scene.
- `DLC2MQ02` stage 20 done and 25 not done: Miraak's first appearance and the temple scene.
- **Apocrypha**: `WS(DLC2ApocryphaWorld 01C0B2:Dragonborn.esm)` or `In(DLC2ApocryphaLocation 016E2B)`. Covers every Black Book trip; followers do not come.
- `DLC2MQ03` 50..60: Storn's ritual and the Lurker fight.
- `DLC2MQ05` stage 340 done to MQ06 stage 10 done: the Storn-Mora bargain and Storn's death.
- `DLC2MQ06` >= 330 and not completed in Apocrypha: already in TRIGGERS.md. Also block 200..550 while flying (dragon riding).
- `DLC2dunKolbjornQST` 449..490: the Ahzidal confrontation.
- Each Stone cleansing (Bend Will on a Stone): short. The combat and scene gates handle it.

### B4. Arrival triggers (Dragonborn)

| Place | Location |
|---|---|
| Solstheim (island) | `016E2A:Dragonborn.esm` (WRLD `DLC2SolstheimWorld 000800`) |
| Raven Rock / Retching Netch / Bulwark / Severin Manor / Raven Rock Mine | `0143B9` / `019A24` / `019A25` / `019A20` / `01429A` |
| Tel Mithryn / Tower | `0143BC` / `01CDEA` |
| Skaal Village / Greathall / Shaman's Hut | `0143BB` / `01D92C` / `01D936` |
| Thirsk / Thirsk Mead Hall | `0143BA` / `016FFE` |
| Temple of Miraak | `0142B6` |
| Nchardak / Kagrumez / Fahlbtharz | `0142B4` / `0142A2` / `0142A0` |
| Kolbjorn Barrow / White Ridge / Vahlok's Tomb / Gyldenhul | `0142BB` / `0142BC` / `0142BA` / `0142A8` |
| Fort Frostmoth / Castle Karstaag Ruins / Highpoint Tower | `014293` / `01429E` / `0184FC` |
| Frostmoon Crag (werewolves) / Ashfallow Citadel / Haknir's Shoal | `0142CB` / `0142C5` / `0142C2` |
| Stones: Earth, Water, Sun, Wind, Beast | `0142A4`, `0142DE`, `0142DC`, `0142DF`, `014296` |
| Apocrypha | `016E2B` (WRLD `01C0B2`) |

### B5. Ten banter hooks (Dragonborn)

1. **Redcap comes home.** Gate: first `In(DLC2SolstheimLocation)`. Redcap: "Big. Ash. Rock!" He realises the Great Water wasn't the end of the world after all. Val, who hates Rieklings and once threw one twenty yards off a ship, is forced to admit "it's... his home. Fine." Gore keeps smelling Rieklings.
2. **Xelzaz at Tel Mithryn.** Gate: first `In(DLC2TelMithrynLocation)`. A Telvanni Lawman meeting a Telvanni Master. Xelzaz is formal and a little awestruck, explains the House's meritocracy to the party, and dreams aloud of his own mushroom tower ("a Xanmeer, restored with mushrooms"). Remi teases him; Redcap asks if he can eat the walls.
3. **Neloth, briefly.** Gate: `Done(DLC2MQ04,10)` and in Tel Mithryn. Xelzaz respects Neloth's power but is appalled by how he treats stewards ("Varona deserved better"). Lucien bristles at being called an "outlander scholar". Inigo is polite to the old man and gets ignored.
4. **Val and the Black Books.** Gate: `Done(DLC2MQ02,60)`. Val goes quiet: he has read one before and walked his own memories. "He's going to want something from you. He always does." Lucien begs the player to come back (his existing line covers that worry, so play it from Val's side). Kaidan offers to burn the book.
5. **Back from Apocrypha.** Gate: any `DLC2BlackBook0xQuest` stage 20 or `DLC2MQ05` stage 340, first reunion out of Apocrypha. The party describes what you looked like while gone: "you were reading for an hour and your eyes were black". Remi finds this fascinating; Xelzaz takes notes; Gore says Hermaeus Mora is the one Daedra he's genuinely scared of.
6. **Storn's sacrifice.** Gate: `Done(DLC2MQ06,10)`. A sombre talk:
    - Kaidan respects a man who pays the price himself.
    - Val: Mora "always collects".
    - Redcap: the Skaal were never kind to Rieklings, "but. Shaman. Brave."
    - Inigo says a prayer.
7. **Served Cold and the Morag Tong.** Gate: `Done(DLC2RR02,90)`. The Morag Tong murdered Xelzaz's master Sul. This is the one place he loses his calm. Val, whom the Tong also hunted (Val003), backs him up. Lucien, rather than Kaidan, asks the gentle question.
8. **Thirsk: which side did you pick?** Gate: `Done(DLC2MH02,200)` or `Done(DLC2MH01,210)` (helped the Rieklings) versus `Done(DLC2MH01,25)` (helped the Nords).
    - Rieklings side: Redcap is triumphant ("This. Hall. Mine!!!") and claims the chief's seat; Val is disgusted.
    - Nords side: Redcap sulks ("*sad Riekling noises*").
    - Either way, Gore and Kaidan argue about mead-hall rights.
9. **Kolbjorn Barrow and Ahzidal.** Gate: `Done(DLC2dunKolbjornQST,100)` (funded) then 490. Val the relic hunter loves Ralis's dig, then watches him fall under Ahzidal's spell. "That's what I'd look like without you."
10. **Miraak is dead; you're Mora's now.** Gate: `Done(DLC2MQ06,550)`. A heavy closing talk. Val tells the player straight what serving Mora cost him. Xelzaz notes that Telvanni would kill for that knowledge, "and some have". Lucien argues knowledge isn't evil and Gore argues it is. Kaidan: "you're still you".

Bonus:
- **Fort Frostmoth ash spawn** (`Done(DLC2RR01,90)`): Inigo's fear of the undead returns.
- **Haknir Death-Brand** (`Done(DLC2dunHaknirTreasureQST,30)`): Val the ex-pirate retells the legend wrong on purpose.
- **Experimental Subject side effects** (`Done(DLC2TTR4a,200)`): Remi wants to study the player. The spell stops working in the rain, so Redcap pours water on them.
- **The Ebony Warrior** (`Done(DLC2EbonyWarriorQuest,100)`): Kaidan and Gore get competitive about who he "really" wanted to fight.

### B6. Existing lines (topics only)

- **Val:** very wide coverage.
  - Every main quest stage (`ValDB01*`: Dragonborn, Temple of Miraak, Fate of the Skaal, Path of Knowledge, Gardener of Men, At the Summit, Cleansing the Stones).
  - Nearly every side quest (`ValDB02*`): Reluctant Steward, A New Debt, March of the Dead, Served Cold, Final Descent, Old Friends, Lost Legacy, Thirsk both sides, Healing a House, all Neloth research jobs, Stalhrim, Filial Bonds, Deathbrand, the Raven Rock favours, Kolbjorn, the Skaal Village freeform, Kagrumez, the Thirsk favours.
  - Plus ship, anchor and Vahlok's-tomb scene triggers.
  - In his own mod: the Black Book in Val005 (Apocrypha of his memories, "used to serve Hermaeus Mora").
- **Kaidan** (`BWB - Kaidan 2 Extra Dialogue.esp`): the whole main quest including the Stones, plus Reluctant Steward, A New Debt, March of the Dead, Served Cold, Final Descent, Old Friends, Lost Legacy, Thirsk, From the Ashes, Healing a House, Telvanni Research, Experimental Subject, Briarheart, Heart Stones, Stalhrim, Filial Bonds, Deathbrand, Fetch the Netch, It's All In The Taste, The Ebony Warrior, Kolbjorn. His lines are hostile to Rieklings.
- **Xelzaz:** the Raven Rock and Tel Mithryn side quests (Reluctant Steward, A New Debt, March of the Dead, **Served Cold**, Final Descent, Old Friends, From the Ashes, Healing a House, Telvanni Research, Experimental Subject, Azra's Staffs, Briarheart, Wind and Sand, the favours, Kolbjorn). **No lines keyed to the main quest (Miraak).** Plus "Solstheim ash" region chatter and his Remi scene `ChatterSolstheim` / `SolstheimAsh`.
- **Remi:** the main quest (MQ01-06, Stones), Thirsk both sides, Kagrumez.
- **Gore:** MQ01-06 and March of the Dead. Bible: scared of Hermaeus Mora.
- **Lucien:** MQ01, MQ02, MQ04, MQ06, the Stones; the Black Book worry ("please come back?"). His **personal quest "The Oblivion Engine" (JRLucienPersonal1) is set at Dumzbthar, a Dwemer ruin on Solstheim**, so he has his own Solstheim arc.
- **Redcap:** Fate of the Skaal, Gardener of Men, Retaking Thirsk, Chief of Thirsk Hall. Bible: the whole Solstheim homeland arc ("Back to the Rock", Bigpig, the vanished tribe, the Fahlbtharz tribe, chief of the Thirsk Rieklings, "King of All Rieklings"); the Tel Mithryn mushroom house, Telvanni Bug Musk, Raven Rock, ash spawn; a three-way drinking quest with Xelzaz and Remi.
- **Inigo:** nothing keyed to Dragonborn quests.

---

## C. Hearthfire

### C1. Spoiler summary

The player can buy a plot of land from a jarl and build a house on it themselves: a small house, then a main hall, then three wings. There are three plots:
- **Lakeview Manor**, Falkreath, from Jarl Siddgeir;
- **Windstad Manor**, Hjaalmarch, from Jarl Idgrod;
- **Heljarchen Hall**, the Pale, from Jarl Skald.

Buying the land makes the player Thane of that hold and gives a housecarl, who becomes the steward and can hire a bard, a carriage driver and so on. Homesteads attract wolves, giants, bandits and skeevers. Players can **adopt** up to two children (orphans like Lucia or Sofie, or kids from Honorhall), who live in a home and ask for pets, toys and food. A spouse moves in.

No villain, no big set piece. Hearthfire is about domestic life, so it is perfect for "found family" D&D-party downtime talk.

Note that this load order also has `HearthfireMultiKid.esp` / `_Expanded` (more kids) and `Hearthfires Houses Building Fix.esp`.

### C2. Quests and gates (Hearthfire records have no journal names in this order)

| What | Record | Gate |
|---|---|---|
| Building (master quest) | `BYOHHouseBuilding 00305D:HearthFires.esm` | Running = player owns at least one plot |
| Lakeview plot owned | `BYOHHouseFalkreath 00305E` | `Run()` / stage 10 done |
| Windstad plot owned | `BYOHHouseHjaalmarch 00BE09` | `Run()` / stage 10 done |
| Heljarchen plot owned | `BYOHHousePale 010BEE` | `Run()` / stage 10 done |
| Steward offer | `BYOHHouseStewardOffer 00308B` | stage 10..200 |
| Room built | Globals `BYOHHouse{1,2,3}Room01..12` and `Room01B` (e.g. `BYOHHouse1Room01B 00F9AD`, `BYOHHouse2Room01 00B0F0`, `BYOHHouse3Room01 010BF8`; the matching `...Started` globals are `000BDA`-`000C00`) | `GetGlobalValue == 1` = finished. Which number is which wing is **not verified**; check against the BYOH building script before relying on "Room01 = small house" |
| Adoption system | `BYOHRelationshipAdoption 0042B4` (+ Adoptable `004291`, Orphanage `004286`) | Player has a child: an NPC in `BYOHRelationshipAdoptionFaction 0042B0` / `BYOHRelationshipAdoptionChildOwnedFaction 0183A8` (check the kid ref, not the player) |
| Homestead attacks | `BYOHHouseWolfAttack 000C39`, `GiantAttack 000C3E`, `BanditAttack 005207` / `0008A8`, `SkeeverInfestation 010A44` | Running = attack. Combat-silent; good for an "after" talk |

Arrival locations: Lakeview `00308A` (interior `003092`), Windstad `005209` (`00BE0A`), Heljarchen `00520A` (`00BE1D`).

Also relevant: Tundra Homestead CC, Farming CC (*A Farmer's Life For Me*) and Shadowfoot Sanctum CC. See D.

### C3. Silence zones (Hearthfire)

- `BYOHRelationshipAdoption` adoption scene (child introduction): skip while the player is in dialogue. The dialogue-menu rule covers it.
- Attack quests running (combat).
- **Kaidan's wedding windows** (`RelationshipMarriageWedding` 10..499, already a rule).
- Inside the player's home with an adopted child nearby: allow talk, but prefer "kid-safe" lines. No swearing and no Kaidan crush lines in front of children.

### C4. Ten banter hooks (Hearthfire)

1. **First foundation.** Gate: `BYOHHouse{n}Room01 == 1` for any n, first time at that location. Remi wants a Dwemer workshop wing. Lucien wants a library (it is the library wing). Gore wants a fishing pond.
2. **Who gets which room.** Gate: main hall done (`Room01B`). A D&D-party squabble over bunks: Redcap claims the cellar; Val claims the room with a window "facing the sea, obviously"; Xelzaz asks for an alchemy lab "with proper ventilation".
3. **Val and kids.** Gate: player has an adopted child, and Val's own `Val00D` not done. Val fears he'd be a bad father. Kaidan, gruff, says "you'd be fine". Callback to Val adopting Ravani if `Done(Val00D,90)`.
4. **Gore and found family.** Gate: adopted child. Gore: "I got the chance to pay it forward". He adopted Meeko, and the Ravens took him in. The party teases him for being soft.
5. **Redcap and the kids.** Gate: adopted child within 1000 units. Redcap is the kids' favourite. "Small. Ones. Like. Redcap!" Inigo has to stop him teaching them the Godspeak Dance.
6. **Steward politics.** Gate: `Done(BYOHHouseStewardOffer,200)`. Xelzaz approves of a Telvanni-style household staff; Val is suspicious of the steward "counting the silver".
7. **Giants at the gate.** Gate: `BYOHHouseGiantAttack` completed, or after combat at a homestead location. Kaidan and Gore argue about whose shot dropped the giant. Inigo was "merely observing the giant's form".
8. **Lakeview views.** Gate: `In(BYOHHouse1Location)` at dusk or dawn (weather/time poll). Lucien's telescope talk; Inigo poetry; Remi falls asleep mid-sentence.
9. **Windstad's swamp.** Gate: `In(BYOHHouse2Location)`. Xelzaz, who is Argonian, finally loves a Skyrim place ("it smells almost like home"). Redcap hates it: "Wet. Bad."
10. **Heljarchen's cold.** Gate: `In(BYOHHouse3Location)`. Snow complaints: Remi only likes eating snowberries. Kaidan's yellow-snow survival tip. Val on how he'd rather be anywhere warm.

### C5. Existing lines (topics only)

- **Kaidan:** many adoption and child lines (`0Kaidan.esp` 28 INFOs keyed to `BYOHRelationshipAdoption`, family topic `BRP08Fam`; `BWB Extra Dialogue` 8; `Kaidan - Immersive Features` 7). He also has his own wedding, honeymoon and tent life.
- **Val:** comments on each house (`Val000BYOHLakeview`, `Val000BYOHWindstad`, `Val000BYOHHeljarchen`, `Val000Homes01`) and on kids (`Val00DKids02`...), plus his own adoption quest Val00D "Wing and Wing" with Ravani.
- **Gore:** a Meeko adoption theme in his bible; `RSChildren - Gore.esp` exists, so check it before writing kid lines.
- No hits for Inigo, Lucien, Remi, Xelzaz or Redcap on Hearthfire quests.

---

## D. Creation Club content present (active in this profile)

Active CC plugins (implicit list):
- almsivi, fish, zombies, ruinsedge, stendarshammer, the horse armours, spellpack01, staffofsheogorath, lordsmail, knightsofthenine, survivalmode, puzzledungeon, hstead, shadowrend, norjewel, curios, mntuni, hasedoki, imperialdragon, ve, crosselv, winter, hollow, umbra, advobgobs, the 15 alternative-armour sets, armsofchaos, netchleather, splkntset, daedinv, contest, necroarts, beafarmer, advdsgs, crossbowpack, dawnfang, redguard, altar, gaunt.

Tweak patches are also loaded: Farming T&E, Tundra Homestead T&E, Umbra Reduced Cut, Dawnfang No Forced Quest, Arcane Accessories T&E. Note that Arcane Accessories is **not** in the CC list.

Below, quests with real story first. Armour-only CCs are listed briefly.

### D1. The story CCs

| CC (folder) | Quest (FormID) | In-game name | Summary | Start / key / complete | Where |
|---|---|---|---|---|---|
| **The Cause** | ccBGSSSE067_Quest `06BFC1:ccbgssse067-daedinv.esm` | The Cause | A reformed Mythic Dawn member, Skorvild, writes for help and is murdered. The Mythic Dawn has rebuilt an Oblivion Gate and needs a Great Welkynd Stone from the Ayleid ruin Rielle (Ayleid Lich). Their leader **Vonos** is killed in Red Scar Cavern, which opens the gate. In the **Deadlands** the player chooses: take the Sigil Stone (gate closes) or place the Welkynd Stone (gate stays open for farming). | 10 rumour · 20 courier · 30 meet Skorvild · 50 assassins · 110 shards · 130 lich · 170 the gate · **220 the choice** · **230 "Gate Closed" / 240 "Gate Open"** · 250 summary (use `GetQuestCompleted`) | Rielle `015889`, Red Scar Cavern `033F35`, Deadlands `033F39` (WRLD `ccBGSSSE067DeadlandsWorld 0E1592`) |
| | ccBGSSSE067_Quest2 `19952A` | The Consequences | Inside the Deadlands: kill the Dremora Valkynaz, retrieve the weapons Scourge and Torment, return. | 210-300 · **1000 [COMPLETE]** | |
| **Ghosts of the Tribunal** | ccASVSSE001_Quest `000CC3:ccasvsse001-almsivi.esm` | Ghosts of the Tribunal | Post-Red Mountain religious upheaval on **Solstheim**. A hidden temple of Almalexia worshippers ("Her Hands") near Raven Rock, led by a Matriarch hunting the lost **Masks of Vivec and Sotha Sil**. The player can kill the heretics, or pose as one of Her Hands and do the Goddess' bidding. | 10 "investigate the Temple in Raven Rock" · 100 Fahlbtharz forge heretic · **120 [COMPLETE] = attacked the Matriarch** · 200-300 [COMPLETE] = posed as Her Hands · 1000 [COMPLETE] | Temple `000C82:ccasvsse001-almsivi.esm` (Solstheim) |
| | QuestA `000CA0` / QuestB `000F19` / QuestC `000F1A` / QuestD `00117A` / QuestE `0990EF` | Buyer Beware / Her Word Against Theirs / Careless Curation / Ashen Heart / Trueflame | Temple jobs: the Mask of Vivec in transit; propaganda letters translated; a curate's notes; ash-zombie attack, a renegade priest and **the Mask of Dagoth Ur**; restoring a Dwemer forge in Fahlbtharz. | A 1000 · B 100/1000 · C 40 · D 100 · E 100 [COMPLETE] | |
| **Umbra** | ccBGSSSE016_UmbraMainQuest `0021B6:ccbgssse016-umbra.esm` | Vile Whispers | Champion's Rest, a Nordic ruin under a silver mine near Shor's Stone. An armoured ghost wields Umbra, the soul-drinking sword. Defeat it; the sword whispers its name. | 10 · 20 · 30 arena · 40 "a single word is whispered... 'Umbra'" · **200 [COMPLETE]** | Champion's Rest `006C48` |
| **Saints & Seducers** | ccBGSSSE025_QuestA `000912:ccBGSSSE025-AdvDSGS.esm` | Balance of Power | Ri'saad's Khajiit caravan is harassed by two bandit gangs dressed as Sheogorath's Golden Saints and Dark Seducers. Pick off both leaders. | 100 rumour · 400-560 · **2000 [COMPLETE]** | |
| | QuestB `000913` | Restoring Order | The conjurer Thoron funds both gangs from Solitude; stop his ritual; **the Sword of Jyggalag**. | 0 · 10-40 · **200 [COMPLETE]** | Root dungeon `0010CF` |
| | Elytra pet quests `0010C0` / `0010C3`, StaadaQuest `198277` | (pets, Staada) | Mania/Dementia elytra pets; the Golden Saint Staada. | | |
| **Forgotten Seasons** | DLCDwarvenPuzzleDungeonQuest01 `0038D9:cctwbsse001-puzzledungeon.esm` | Forgotten Seasons | A lost Dwemer ruin, **Vardnknd**, south-west of Markarth that "lets one control the sky": season rooms (winter, summer...) and a mage's journal. Also the Dwarven Horse and the Dwarven Crown. | 0 rumour · 1-11 · [COMPLETE] 5 on the log. Watch Quest02 `126690` for the finale | Vardnknd `003901` (Winter `0038FF`, Summer `003902`) |
| **Plague of the Dead** | ccBGSSSE003_ZombieQuestStartEncounter `00083D:ccbgssse003-zombies.esl` | The Rising Dead | An anonymous letter; a necromancer ritual site; the risen dead now roam Skyrim (`B003_WE_Quest*` encounters). | 10 letter · **40 [COMPLETE]** | |
| **Ruin's Edge** | ccBGSSSE004_Quest `00080C` | The Edge of Ruin | A map to the bow Ruin's Edge (an Ayleid bow). | 100 map · **1000 [COMPLETE]** | |
| **Shadowrend** | BGSSSE018_ShadowrendQuest `00081C` | Through a Glass, Darkly | An inner voice leads to a geyser pool in Eastmarch; fight your own shadow doppelganger; win Shadowrend. | 5 · 10 · 15 · **20** (no COMPLETE flag on the log; use `GetQuestCompleted`) | |
| **Staff of Hasedoki** | ccBGSSSE045_Quest `000823` | The Staff of Hasedoki | A smuggler ledger leads to two necromancers in Brittleshin Pass. | 5 · ... · **200 [COMPLETE]** | |
| **Goblins** | ccBGSSSE040_Quest `0009B6` | Blue in the Face | Gromm's Pass goblin arena, an Orc shaman, the goblins' Blue God. | 8 · ... · **200 [COMPLETE]** | Gromm's Pass `000D13` |
| **Farming** | ccVSVSSE004_MainQuest `000D28` / RestoreFarmQuest `000EB7` | The Unquiet Dead / A Farmer's Life For Me | A haunted farm; ghost parents falsely suspect each other of killing their son; reunite the spirits, claim the farm, restore it. | Main 0 · ... · **1000 [COMPLETE]** · Restore **500 [COMPLETE]** | Farm `000D36` / interior `000D37` |
| **Bittercup** | ccKRTSSE001_zQuest `000D63`, QuestFortune `000A90`, QuestPower `000A5E` | A Dying Wish / Fortunate Son / The Pit | Hagraven altar rituals near Falkreath (Roadside Ruins). Wish for fortune and you wake with a rogue's letter about robbing a High Elf in Markarth. Wish for power and you wake in a dungeon arena. The cup "that promised nothing" sends you to an island via the Temple of Kynareth. | zQuest 0 · ... · **200 [COMPLETE]**; Fortune **1000**; Pit **100** | Pit `000F54`, Frozen Tusk `000F8D` |
| **Fishing** | Start_MQ1 `0009D3:ccBGSSSE001-Fish.esm` "First Catch" → Start_MQ2 `0009DB` "Angler Acquaintances" → Fish_MQ1-5 (`0009DE` Catch of the Day, `0009EB` Caught in the Rain, `0009E8` Frozen Fish, `0009DD` Darkest Depths, `0009DC` **Fishing Legend**); Crab_MQ1-4 (`0009D4` In A Pinch, `0009DA` Crustacean Extermination, `0009D6` End of the Line, `0009E9` **Wave Breaker**: the emperor crab spirit); misc: Heart of Gold / Two of a Kind (Mila's goldfish), Clear-Headed (Falkreath skooma guard), Spirits Away (**Ri'saad's flin**), Private Lessons (Lynea, Markarth), **Tusked Terror** (Fangtusk the vampiric horker), The Ultimate Feast (Gisli), **No Contest** (Brutius the murderous Morthal fisherman), Beneath Bronze Waters (Calcelmo's Dwemer fishing machine) | Riften Fishery, Swims-In-Deep-Water and Viriya. | Mostly **200 [COMPLETE]**; Fishing Legend 200 = "designating me a legendary fisherman"; Wave Breaker **2000** | Riften Fishery |
| **Wild Horses** | ccBGSSSE034_WildHorsesQuest `000D65`, UnicornQuest `000DE8` | Horse Whisperer / Creature of Legend | Tame wild horses; find and tame the last **Unicorn**. | Unicorn **20 [COMPLETE]** | |
| **Stendarr's Hammer** | ccBGSSSE006_Quest `000805:ccbgssse006-stendarshammer.esl` | If I had a Hammer | Rumour in the Markarth Dwarven Museum; a crater; you're "deemed worthy to lift it". | 100 · **1000 [COMPLETE]** | |
| **Spell pack** | `00083C:ccbgssse014-spellpack01.esl` | The Lost Library | Long-lost spell tomes near Winterhold, in Hob's Fall Cave. | 0 · **10 [COMPLETE]** | |
| **Staff of Sheogorath** | `000822:ccbgssse019-staffofsheogorath.esl` | Put A Fork In It | Sheogorath's staff tie-in. | (no journal in record) | |
| **Lord's Mail** | `000813:ccbgssse021-lordsmail.esl` | Gift of Kynareth | Kynareth's armour. | (no journal) | |
| **Divine Crusader** | `00083C:ccmtysse001-knightsofthenine.esl` / `000865` | Relics of the Crusader / The Pilgrim's Path | Bandits stole the Crusader's Relics; reclaim them. Commit crimes and you must walk the nine-shrine pilgrimage. | Relics 0 → 100 · Pilgrim 10 → **100 [COMPLETE]** | |
| **Dawnfang & Duskfang** | `000F18:ccbgssse013-dawnfang.esl` | A Soul Divided | A ghost woman in the Riften Ratway; the Guardian Vault; a guardian and a woman reconciled. | 0 · ... · 130 · **200 [COMPLETE]** | The Guardian Vault `000816` |
| **Arms of Chaos** | `000819:ccpewsse002-armsofchaos.esl` | The Arms of Chaos | Rituals north of Winterhold at the Skytemple Ruins; three Sigil Stones; summoned Daedra. | 10 · ... · **1000 [COMPLETE]** | |
| **Vigil Enforcer** | `000926:ccmtysse002-ve.esl` | Unholy Vigil | Missing Vigilants; three suspects; a secret cult. | 10 · ... · **100 [COMPLETE]** | |
| **Spell Knight** | `000800:ccedhsse002-splkntset.esl` | (quest) | The ghost of Breton knight Simon Rodayne; his heart stolen by Forsworn to Karthspire. | 10 · ... · **1500/2000 [COMPLETE]** | |
| **Redguard Elite** | `00088C:ccedhsse003-redguard.esl` | (quest) | Azadi brawls in Shor's Stone; the Hammerfell **Remnant** spies (Fijeh); free Rakeed from a **Thalmor** caravan. | 10 · 20 brawl · 62 spies · 110 assault · **250 [COMPLETE]** | |
| **Civil War Champions** | `000927:ccffbsse001-imperialdragon.esl` | Battle of the Champions | A champion duel for your Civil War side. | 10 · ... · **170 / 270 [COMPLETE]** | |
| **The Contest** | `000805:ccbgssse069-contest.esl` | Caught in a Web | Candlehearth Hall journal; the Web Mother in Cronvangr Cave. | 1 · **100 [COMPLETE]** | |
| **Elven Hunter** | `00089E:ccbgssse043-crosselv.esl` | (vampire hunter) | Kragrash the vampire hunter turned vampire; his cellar at Ironback Hideout. | 10 · **200 [COMPLETE]** | |
| **Saturalia** | `00082B:ccvsvsse001-winter.esl` | Saturalia Preparation | A holiday merchant near Dawnstar. | 10 | |
| **Shadowfoot Sanctum** | `00082A:cceejsse003-hollow.esl` | Shadowfoot Sanctum | Buy a Ratway home from Vekel. | 10 · 20 · **100 [COMPLETE]** | `000D41` |
| **Rare Curios** | `00084D:ccbgssse037-curios.esl` | Rare Curios | Khajiit caravans sell exotic ingredients. | startup only | |
| **Tundra Homestead** | `042D35:cceejsse001-hstead.esm` | (house) | A homestead in Whiterun Hold tundra. | no journal | `001022` / `000F1E` |
| **Necromantic Grimoire** | `0008B7:ccvsvsse003-necroarts.esl` | (quest) | Necromancy book; Bone Colossus. | not resolved in strings | |
| **Fearsome Fists** | `000834:cccbhsse001-gaunt.esl` | (quest) | Gauntlets. | not resolved | |
| Armour-only CCs | norjewel, netchleather, the alternative-armour sets, crossbowpack, horse armour, Hasedoki staff | | "Where did you get that" lines on the item only | |

### D2. Silence zones (CC)

- **The Deadlands**: `WS(0E1592:ccbgssse067-daedinv.esm)` or `In(ccBGSSSE067_DeadlandsLocation 033F39)` while `ccBGSSSE067_Quest2` is running. A hostile Oblivion plane. Followers do enter here, so allow only short "this place" barks after combat.
- **The Cause stage 220** (the Sigil Stone choice): skip until 230 or 240.
- **Shadowrend** `BGSSSE018_ShadowrendQuest` 15..20: the doppelganger duel.
- **Bittercup** `ccKRTSSE001_QuestPower` running inside the Pit (`In(000F54)`): the player wakes alone in a dungeon. Followers are not there.
- **Fishing**: while the player is fishing (`ccBGSSSE001_FishingSystemQuest 033A57` active state; there is also a `FishingFollowerIdleQuest 0D1017`). Short fishing-themed lines only; never interrupt a cast with long scenes.
- **Saints & Seducers** Thoron's ritual (`QuestB` 30..40).
- **Civil War Champions** duel (`ccFFBSSE001_Quest` 150..160 / 250..260): a one-on-one fight.
- **Ghosts of the Tribunal** stage 200..250 (posing as Her Hands inside the temple): an infiltration. Followers talking would blow the cover.

### D3. Ten banter hooks (CC)

1. **The Cause, and Kaidan.** Gate: `Done(ccBGSSSE067_Quest,60)` ("the Mythic Dawn have reemerged"). Kaidan's past in the Blooded Dawn (Dagon) comes up unprompted. He goes cold and quiet, and says he'll be the one to put Vonos down. Lucien gives the Oblivion Crisis history lecture and is completely wrong about how Kaidan feels. Inigo quietly shuts that down.
2. **Gate open or closed?** Gate: `Done(ccBGSSSE067_Quest,230)` versus `240`.
    - Closed: Xelzaz and Remi approve, and Kaidan is relieved.
    - Left open for loot: Val is delighted ("an infinite treasure room!"), Kaidan furious, Gore torn.
3. **Ghosts of the Tribunal, and Xelzaz.** Gate: `Done(ccASVSSE001_Quest,10)` and `In(000C82)`. A Telvanni scholar on the fallen Tribunal Temple, Almalexia, and the "ghosts" of the old faith. Redcap on Big Ash Rock's new god-people. Val on the Masks' resale value.
4. **Which side at the Tribunal temple.** Gate: `Done(ccASVSSE001_Quest,120)` (slaughtered them) versus `Done(...,300)` (played along). Xelzaz either respects the decisiveness or is unnerved at how well the player wore the robe. Bonus: `Done(ccASVSSE001_QuestD,100)`, the **Mask of Dagoth Ur**. Xelzaz begs the player not to wear it.
5. **Umbra whispers.** Gate: `Done(ccBGSSSE016_UmbraMainQuest,200)` and the player carries Umbra. Val warns about blades that talk (he knows Daedric whispers). Inigo would like the sword to stop "looking at him". Lucien recites Umbra lore. Lucien's own Umbra patch exists, so play it as a group follow-up.
6. **Saints & Seducers and Ri'saad's caravan.** Gate: `Done(ccBGSSSE025_QuestA,100)`. Inigo, a Khajiit, is fond of the caravan and protective of Ri'saad's people (check his bible before inventing caravan backstory). Gore (who has his own SaSEC line "I vote nay") jokes about Sheogorath. Redcap is terrified of the "Shiny. Lady. Mad. God."
7. **The Sword of Jyggalag.** Gate: `Done(ccBGSSSE025_QuestB,200)`. Lucien explains the Greymarch; Remi wonders aloud whether order is better than madness; Redcap chooses madness.
8. **Fishing Legend.** Gate: `Done(ccBGSSSE001_Fish_MQ5,200)`. Gore is genuinely proud and a little jealous ("I'm simple. I love fishing."). Kaidan wants a horker sandwich instead. Also: `Done(ccBGSSSE001_Misc_Windhelm,200)` "Tusked Terror", a vampiric horker, so Kaidan gets his horker joke.
9. **Plague of the Dead.** Gate: `Done(ccBGSSSE003_ZombieQuestStartEncounter,40)`. Inigo's fear of crypts and zombies ("if I scream, do not hold it against me"). Xelzaz explains necromantic plagues; Redcap: "Dead. Walk. Again?! No!"
10. **Bittercup's pit or fortune.** Gate: `Done(ccKRTSSE001_QuestPower,100)` or `Done(ccKRTSSE001_QuestFortune,1000)`. The party asks where the player vanished to after drinking from a hagraven's cup. Val: "you robbed an Altmer without me?!" Gore: "next time you vanish, leave a note".

Bonus hooks:
- **Forgotten Seasons and Vardnknd** (`Done(DLCDwarvenPuzzleDungeonQuest01,1)`): Remi and Lucien rapture over a Dwemer weather machine; the Dwarven Horse (`...HorseQuest 3`) delights Redcap.
- **Redguard Remnant** (`Done(ccEDHSSE003_Quest,140)`): Gore, who praises Redguards and wants to see Hammerfell, is thrilled; Xelzaz approves of humiliating the Thalmor.
- **The Unicorn** (`Done(ccBGSSSE034_UnicornQuest,20)`): everyone loses their cool.
- **Farming ghosts** (`Done(ccVSVSSE004_MainQuest,1000)`): a sad story about parents blaming each other. Val and Kaidan connect it to their own families.
- **Stendarr's Hammer** (`Done(ccBGSSSE006_Quest,1000)`): "deemed worthy" teasing.

### D4. Existing lines (topics only)

- **Lucien** has 13 dedicated CC patches in this order: Stendarr's Hammer, Lord's Mail, Plague of the Dead, Saturalia, Umbra, Forgotten Seasons, Goblins, Rare Curios, Ruin's Edge, Saints & Seducers (both quests), Shadowrend, Staff of Sheogorath, Tundra Homestead. Also Alt Armour Dwarven Mail / Elven Hunter / Silver and Expanded Crossbow. By quest reference: Forgotten Seasons Q01, Goblins, Lord's Mail, Plague, Ruin's Edge, S&S A+B, Shadowrend, Staff of Sheogorath, Stendarr's Hammer, Umbra. **Avoid duplicating those reactions; use them as other people's reactions to Lucien's.**
- **Redcap:** CC Goblins (`FARGRedcapCCGoblinsPatch.esp`: meets Gogh, gets the Spear of Bitter Mercy, the "Blue God").
- **Gore:** Saints & Seducers Extended Cut (`Gore - SaSEC.esp`, HD1Madness "I vote nay"); Fishing (`GORE - Fishing CC Patch.esp`).
- **Val:** CC and Saints & Seducers add-on quests (bible §7).
- **Kaidan:** `Kaidan - Survival.esp` (Survival Mode) and the Survival/EAS/SunHelm patches. No hit on The Cause; his Deadlands arc is his own mod's KR2/KMD line, so the CC overlap is fresh ground.
- No CC hits for Xelzaz, Remi or Inigo, so **Ghosts of the Tribunal is untouched for Xelzaz**.

---

## E. Missives (+ Bounties Redone extensions)

### E1. Summary for the writer

Missives puts **notice boards** in every hold capital and several towns. Each board shows random one-off jobs: deliver a letter, weapon or potion (near, medium or far); gather ingredients, ore, soul gems or inn food; kill animals, bandits, a giant, a dragon or Forsworn; recover an item from a ruin, hideout or the wilderness; **track** a thief, fugitive or vampire.

Add-ons in this order:
- **Missives - Solstheim**, **Wyrmstooth**, **Heartland** (Bruma) and **Gray Cowl Patch** (Alik'r Basin) add regional boards.
- **MissivesExpansion** adds jobs: find books, spell tomes, toys or accessories; gather Nord mead or steel swords; kill pests; catch fish; find the missing dog; heal the sick; items from Solstheim.
- **Bounties Redone extensions** (`BountiesRedone_MissivesExtension.esp`, `_Missives_Solstheim`, `_Missives_Wyrmstooth`) rewrite the kill-bandit / dragon / giant / Forsworn and Track-thief / fugitive jobs. They also override the vanilla `BQ01-04` bounties (Bandit Boss, Forsworn, Giant, Dragon), adding bounty-hunter style targets.
- Also active: `Missives - Bigger Trigger Box Range.esp` and `Missives - Headhunter Journal Quest Fix.esp`.

There is no story. Missives is the party's **day job**, ideal for D&D "the guild board" banter.

### E2. Quest pattern and gates

- EditorIDs: `_M_Quest<Region><Type><Tier>` (e.g. `_M_QuestWhiterunKillBandit 00F0C8:Missives.esp`, `_M_QuestRiftTrackThief 037273`, `_M_QuestEastmarchTrackVampire 0382D0`). Expansion jobs are `_ME_Quest*:MissivesExpansion.esp`.
- Regions: Whiterun, Eastmarch, Falkreath, Haafingar, Hjaalmarch, Pale, Reach, Rift, Winterhold, Solstheim, Wyrmstooth, Bruma, AlikrBasin. Tiers: Low / Med / High / VeryHigh (gather) and Near / Medium / Distant (courier).
- About 264 base quests and 60 expansion quests. The normal stage layout (checked on `_M_QuestWhiterunGatherIngrHigh`) is **0 = taken (startup), 100 [COMPLETE], 105 [FAIL]**.
- Practical gates:
  - "Has an active job": any `_M_Quest*` running. Easiest is to check a few type families with `GetQuestRunning`, or keep a script FormList of all of them.
  - "Just finished a job": `OnStoryScript` is not available, so poll for stage 100 newly done.
  - Bounties: `BQ01 095125:Skyrim.esm` (Bandit Boss), `BQ02 0BD77F` (Forsworn), `BQ03 0BD78C` (Giant), `BQ04 0CBA9A` (Dragon), as overridden by Bounties Redone.
- Silence: none special. Track-quests end in combat, which the combat gate covers.

### E3. Ten banter hooks (Missives)

1. **Reading the board.** Gate: player near a board (a Missives board activator; FormID not looked up, check `Missives.esp` ACTI). The party argues over the pinned jobs like an adventuring guild. Val wants the best pay; Inigo wants the one that helps someone; Redcap points at the dragon one.
2. **Courier work beneath us.** Gate: any `_M_Quest*Courier*` running. Kaidan grumbles about being a delivery boy; Xelzaz, who is literally walking across Tamriel, defends honest travel.
3. **Gather-ore jobs.** Gate: `_M_Quest*GatherOre*` running. Remi lectures on ore grades; Gore carries it all ("the pack mule").
4. **Ingredient runs.** Gate: `_M_Quest*GatherIngr*` running. Xelzaz the alchemist is finally useful; Redcap eats one of the ingredients.
5. **Soul gem jobs.** Gate: `_M_Quest*SoulGem*`. Lucien on soul gems in automatons; Inigo on the morality of black soul gems.
6. **Kill a dragon off a notice board.** Gate: `_M_Quest*KillDragon*` stage 100. "We killed a dragon for a flyer." The party ranks how absurd that is.
7. **Track the thief / fugitive.** Gate: `_M_Quest*TrackThief*` or `*TrackFugitive*` running. Val, a wanted man himself (an Anvil bounty), is uneasy hunting fugitives. Inigo, who was once jailed, feels the same. Kaidan has no such qualms.
8. **Track the vampire.** Gate: `_M_Quest*TrackVampire*` running and `Done(DLC1VQ02,180)` (the player is a vampire). Dark comedy as the party hunts a vampire for a vampire.
9. **Bounties Redone.** Gate: `BQ0x` complete. Kaidan was once a bounty hunter (he joined the cult via a bounty), so he gives pro tips. Remi wants to turn Val in for his bounty, a running gag.
10. **Payday split.** Gate: any Missives stage 100 newly done. A loot-split argument: Val wants a "finder's fee"; Gore wants nothing; Redcap wants "Shiny!"

---

## F. Interesting NPCs (3DNPC.esp)

### F1. Summary for the writer

3DNPC adds about 250 voiced NPCs, many with quests. This order also loads `3DNPC0.esp`, `3DNPC1.esp`, `3DNPCs_Reimagined.esp`, `3DNPC - Vigilant Patch`, `3DNPC - AI Overhaul patch` and `Kaidan - 3DNPC Patch`. Nearly all 3DNPC quests use objectives, not journal text, so key on stage numbers.

The major questlines:

- **The main questline: "From the Blood of Kings" (MQ1-7).** Rumours of a mage in Whiterun lead to a secret meeting at Hunter's Rest, a prisoner in Castle Dour, the fugitive **Morndas**, Falatild, the Axe of Kings at Orphan Rock, and an order to "Kill the Dragonborn". It continues through Zora Fair-Child and Olfrim's notes (*Faces and Names*), forging the axe and the Bloodgrass (*The Bloodsmith*, with Isobel and Cyrus), Thane Larsdon and the ruins of Angarvunde (*The Harbinger of Us All*), Eldritch, the war-teacher and a blood spell (*Blood and Bones*), and Larsdon turned into a beast (*The Beast Who Cannot Be Slain*). It ends at a party in Whiterun where the player either sacrifices themselves or saves Larsdon (*An End to Keep*).
- **Darkened Steel (the "Cue" arc, 6 quests).** Orphan's Tear, Wanderer's Rest, Tikrid and Lorne, bounty hunters, the Nightblade, Krillo in Markarth, Erevan and Viola's party (*Deathbroker*), the Shrine of Azura, the Blades of Deneris, and finally killing the immortal **Deneris** with the Trinity Blade at Shadow's Gulch (*The Face of the Ghost*).
- **Rich standalone quests:**
  - Stolen Property: the Warrens; Vardath; a slave auction at Rothvine Manor; a slave-ship revolt.
  - As You Like It: Na'ir's assassination contract on an island; archery "William Tell" with Daenlyn and Jerulith; kill the Baroness.
  - The Raven of Anvil: the bard Asteria; forged journals; a heist in Understone Keep.
  - Vigilance and Virtue: Viranya and Rinori, a vampire tunnel.
  - Pit Dogs: Zora, Gorr, J'Sharr's fight pit.
  - The Immortal Coil: Arilwaen; Thalmor black soul gems.
  - Black Robes: Anum-La; Synod mages in Riften; Mourner's Den.
  - The Radiant Dark / A New Dawn / Forgotten Lore: Olivia Meronin and Jadro'Ra.
  - Honor's Calling: Anum-La.
  - The Way of the Nine and The Hidden Blade: S'vashni.
  - A Rose Without Thorns (Erevan), Fenced In (Morndas), Transformation (Terynne), Birds of a Feather / The Curse (the hag).
  - Also: The House on the Hill, Treasure Hunters, The Gales of Guilt, Children of the Dust, Mzinchaleft, A Thousand Words (a painting), The Paper Mirror (a book), The Teleportation Machine (Aldi), The Sleeping Giant / A Spell for Rumarin.
  - Plus small favours: The Conspiracy of the 7000 Steps (Dar'Rakki counts High Hrothgar's steps), Relic's Revival (a sentient Dwemer centurion), The Milk-Drinker, The Loudest Whisper...
- **3DNPC followers** that our party already knows: Rumarin, Zora Fair-Child, Anum-La, Morndas, Jaspar, Griffith/Raynes and others. Remi already has banter with Rumarin, Zora and Anum-La.
- **The Gray Isle**: a whole separate worldspace (`3DNPCGabaniasWorld 500000:3DNPC.esp`, "The Gray Isle"). Which quest uses it was not traced; check before writing.

### F2. Major quests

| Quest | FormID | Name | Key stages (objective text) | Complete |
|---|---|---|---|---|
| 3DNPCMQ1 | 196D2D:3DNPC.esp | From the Blood of Kings | 1 investigate the Whiterun mage · 20 Hunter's Rest · 50 Castle Dour prisoner · 80 recruit Morndas · 177 "Kill the Dragonborn" · 200 Orphan Rock · 270 Axe of Kings · 300 | **400** |
| 3DNPCMQ2 | 19B9CD | Faces and Names | 1 Zora about Orphan Rock · 40 Nilheim · 55 Bilegulch Tower · 60 Snapleg Cave · 80 Olfrim | **250** |
| 3DNPCMQ3 | 1A63C4 | The Bloodsmith | 10 EEC office in Windhelm · 30 graveyard fence · 60 Bloodgrass · 80 Isobel | **100** |
| 3DNPCMQ4 | 1A0BD4 | The Harbinger of Us All | 10 wait for Thane Larsdon · 20 Falkreath hideout · 100 Heartwood Mill · 150 Angarvunde · 250 Eldritch's journal · 270 | **400** |
| 3DNPCMQ5 | 1ADAFB | Blood and Bones | 6 Frostfruit Inn · 40 Bleakcoast Cave · 100 Eldritch's body · 130 steal Falatild's blood spell | **150** |
| 3DNPCMQ6 | 1B2911 | The Beast Who Cannot Be Slain | 40 find the Beast · 90 Rorikstead · 92 return Larsdon to mortal form | **120 / 200** |
| 3DNPCMQ7 | 1B462D | An End to Keep | 20 kill or persuade Larsdon, or sacrifice yourself · 40 attend the party · 80 meet the potential housecarl | **200 / 500** |
| 3DMCue | 1D40F8 | Darkened Steel | 5 Orphan's Tear · 60 Lorne in Winterhold · 80 protect Lorne · 150 the Nightblade's corpse · 190 Wanderer's Rest | **320** |
| 3dmcue2 | 1D96ED | A Daedra in the Dark | 20 Lorne's shack · 40 Ironheart Cave · 120 Deirdre | **200** |
| 3DMCue3 | 1E8C3C | Cat and Mouse | 60 Krillo in Markarth · 120 chase the assassin | **200** |
| 3DMCue4 | 1F05C2 | Deathbroker | 25 Viola's party · 50 Hall of the Dead · 60 Blades of Deneris · 80 Shrine of Azura | **110** |
| 3DMCue5 | 1F8527 | A Path of Bones | 50 Windpeak Inn · 80 kill Deneris · 140 Black Mountain Flower · 170 poison Tikrid | **200 / 210 / 220** |
| 3dmcue6 | 203932 | The Face of the Ghost | 10 Shadow's Gulch · 50 dispel Deneris' immortality with the Trinity Blade | **90** |
| warrensquest | 1C0F1E | Stolen Property | 30 Vardath · 80 the auction · 200 kill Vardath before he executes the Imperial · 320 shivs to the slaves · 370 escape Shattered Plank Cave | **250 / 440 / 450 / 530 / 540** (branches) |
| DJGQuest2 | 2CF48B | As You Like It | 100 fire 10 arrows at Daenlyn · 125 shoot the object off Jerulith's head · 194 kill the Baroness · 303/304 kill Griffith / Raynes | (several ends) |
| AsteriaQuest | 15E47E | The Raven of Anvil | 20 steal Yngvar's journal · 41 rescue the Argonian forger · 87 steal the document · 90 flee Understone Keep | (end ~97) |
| ViranyaQuest | 17A1F7 | Vigilance and Virtue | 10 Cronvangr · 65 vampire tunnel · 90 New Gnisis Cornerclub · 96 kill / 100 talk to Rinori | |
| GorrQuest | 171FD5 | Pit Dogs | 30 J'Sharr under Fort Sungard · 81 fight the Hammerfell warriors · 140 Orotheim | |
| ArilwaenQuest | 2838D9 | The Immortal Coil | 20 Thalmor ship near Northwatch · 80 Chillwind Depths black soul gems | |
| blackrobesquest | 242E87 | Black Robes | 10 Mistwatch · 30 Riften Ratways · 70 kill the Synod mages | |
| RDQuest / DialogueOlivia / CWQQ2 | 12A16A / 036AD6 / 038120 | The Radiant Dark / A New Dawn / Forgotten Lore | Jadro'Ra's killer; Olivia Meronin | RD **100/200**, FL **200** |
| SvashniQuest / dialoguesvashni | 14E08B / 054163 | The Way of the Nine / The Hidden Blade | S'vashni killed her master; no heir to the Way of the Nine | **110 / 200** |
| AnumLaQuest | 1413D9 | Honor's Calling | An old friend at Folgunthur | **100** |
| RumarinQuest / RumarinQuest2 | 145C24 / 185B23 | A Spell for Rumarin / The Sleeping Giant | A tome for "challenged novices" at the College | **100** |
| ZoraQuest | 147D05 | The Children Fair | Zora's sister | **100 / 150** |
| HorkerQuest | 12E107 | The Way to a Big Oaf's Heart | Callen and the Legendary Horker | **100** |
| DialogueDarRakki | 002912 | The Conspiracy of the 7000 Steps | Count the steps up High Hrothgar | **100 / 110** |
| DialogueTheRelic | 044B3C | Relic's Revival | Repair a sentient Dwemer Spider Centurion | **20 / 30** |

### F3. Silence zones (3DNPC)

- `3DNPCMQ7` 20..50: the party and the choice to sacrifice yourself. There is a scene quest `3DNPCMQ7Scenes9 1B8FA1`.
- `3DMCue4PartyViola*` scene quests running (`1F13F3`, `1F142D`, `1F143B`, `1F144F`): Viola's party, a social-stealth sequence.
- `warrensquest` 80..90 (the auction) and 300..370 (the slave ship): infiltration.
- `DJGQuest2` 100..130: the archery act. Talking during the arrow volley would be bad.
- `AsteriaQuest` 80..90: the performance and the heist.

### F4. Ten banter hooks (3DNPC)

1. **"Kill the Dragonborn."** Gate: `Done(3DNPCMQ1,177)`. The party reads the letter under the counter that orders the player's death. Kaidan: "Over my dead body. Well. Theirs." Val: "Wouldn't be the first contract on one of us."
2. **The Axe of Kings.** Gate: `Done(3DNPCMQ1,270)`. Lucien the historian wants to authenticate it; Gore just wants to hold it.
3. **Larsdon the beast.** Gate: `Done(3DNPCMQ6,40)`. Werewolf-adjacent talk: Lucien's fascination with lycanthropy; Kaidan's "you don't put down a friend if there's another way".
4. **The sacrifice choice.** Gate: `Done(3DNPCMQ7,200)` versus `500`. The party reacts to how close the player came to dying for a stranger. Inigo is very emotional; Redcap "Never. Again!"
5. **Deneris the immortal.** Gate: `Done(3dmcue6,90)`. Val, who has seen Daedric bargains, dissects how Deneris cheated death. Xelzaz on Azura. Remi: "a trinity blade, a Dwemer one?" (it isn't).
6. **The slave auction (Stolen Property).** Gate: `Done(warrensquest,90)`. Val's moral code: he never dealt in slaves. Xelzaz is Argonian; slavery is the history of his people under the Dunmer. This is a serious talk. Gore is murderous.
7. **"As You Like It", the archery act.** Gate: `Done(DJGQuest2,125)`. Kaidan, Gore and Inigo argue about who'd have made the shot. Redcap volunteers to have the apple on his head next time.
8. **The Raven of Anvil.** Gate: `Done(AsteriaQuest,95)`. Val has an Anvil bounty; he says the bard got Anvil Harbor right. Inigo hums "Dusk on Anvil Harbor" badly.
9. **The 7000 Steps.** Gate: `Done(DialogueDarRakki,100)`. Lucien already jokes about "How To Utterly Destroy Your Legs, in 7000 Easy Steps", so tie it in. Redcap actually counted and got a different number.
10. **Pit Dogs.** Gate: `Done(GorrQuest,81)`. Val never dealt in animal or fighting rings. Gore and Kaidan secretly enjoyed the fight and feel guilty.

### F5. Existing lines (topics only)

- `Kaidan - 3DNPC Patch.esp` exists. It is a compatibility patch and its content was not opened. Kaidan's bible says the 3DNPC patch is among his patches.
- **Remi** has banter with 3DNPC followers Rumarin, Zora and Anum-La (her plugin).
- No 3DNPC quest-keyed lines were found for the others (the search covered DLC and CC quests only, not 3DNPC; run a 3DNPC reference search before writing if exact overlap matters).

---

## G. Follower angle cheat-sheet for this content

| Follower | Strongest content hooks here |
|---|---|
| **Kaidan** | The Cause (his Dagon cult past, the Deadlands); Serana protectiveness; bounty work (Missives / Bounties Redone); Hearthfire kids. Already very well covered on Dawnguard and Dragonborn, so write him as the responder, not the lead. |
| **Gore** | Distrusts Serana, then softens; afraid of Hermaeus Mora; fishing (Fishing CC "Fishing Legend"); found family (Hearthfire); Redguards (the Remnant CC). |
| **Val Serano** | Served Hermaeus Mora: Black Books, Apocrypha, Mora "always collects", Storn's death. Ex-pirate: Haknir, the Raven of Anvil, the Deadlands loot gate. His no-slaves / no-fight-pit code (Stolen Property, Pit Dogs). Fear of bad fathers (Harkon, Hearthfire). Already huge Solstheim coverage. |
| **Remi** | Dwemer: Nchardak, Kagrumez, the Aetherium Forge, Vardnknd (Forgotten Seasons), the Fahlbtharz forge (Ghosts of the Tribunal "Trueflame"), Relic's Revival. Snow Elves in the Forgotten Vale. |
| **Xelzaz** | Telvanni Lawman: Tel Mithryn, Neloth, Raven Rock. The Morag Tong (Served Cold; they killed his master Sul). Ghosts of the Tribunal (untouched). Windstad swamp. Slavery (Stolen Property). Has no Miraak main-quest lines. |
| **Inigo** | Fear of the undead (Plague of the Dead, ash spawn, the Soul Cairn return). Khajiit caravans (Saints & Seducers, Ri'saad's flin). Kindness hooks. No DLC-keyed lines yet, so lots of room. |
| **Lucien** | Elder Scrolls (his father worked with them at White-Gold Tower), the Moth Priest, the Oblivion Crisis (The Cause). Dwemer. His own Solstheim quest (Dumzbthar). 13 CC patches already. |
| **Redcap** | **Solstheim homecoming**; Thirsk Riekling chief; Skaal and Storn; Big Ash Rock; Neloth's "mushroom house"; "Dead-pup"; afraid of the undead and of Sheogorath; kids love him. |
