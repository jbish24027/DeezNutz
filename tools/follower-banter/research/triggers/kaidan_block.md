# Kaidan block list for the follower-banter mod

Read from the live load order (profile DEEZ CS NUTZ - PICTA, houseCARL epoch e2-52b2b71e586571f0). The quest-stage fragment sources were read from `mods\Immersive Kaidan AIO - rerun\scripts\source` and `mods\Kaidan 2\Source`. The KR2 Deadlands scripts were extracted and decompiled from KR2_Deadlands.bsa into the scratchpad. Nothing in the instance was written.

FormIDs are given as `XXXXXX:Plugin`. "IF" means `Kaidan - Immersive Features.esp`. Unless a row says otherwise, every condition below is **run on Subject** and must **pass for the talk to be allowed**.

How Skyrim reads condition lists: conditions marked **OR** join with the next line into one group, and the last line of the group carries no OR flag. Groups are joined by AND. "Window" means the span of stages during which the beat can be playing.

> GetStage on a quest that never started returns 0. Stopped or completed quests keep their last stage. For that reason every quest window below is written as `GetQuestRunning == 0 OR stage below window OR stage at/after window end`. This passes outside the window and fails inside it.

---

## 1. Kaidan quests that have scenes, forcegreets or scripted beats

Stages were checked against the quest's fragments, both the VMAD stage-to-fragment map and the .psc code. "Active" means a beat can be in progress.

| Quest (EditorID) | FormID | What it is | Active window | Finished / safe |
|---|---|---|---|---|
| K01 "A Bounty for the Hunter" | 002F9D:0Kaidan.esp (winner: Alternate Start Quest) | Rescue from the Abandoned Prison. Scene KaiToCyrelian. | 1–25 (stage 1 is StartUp) | 30 = rescued, CompleteQuest, sets K03 10. 6 = player left him (never a follower). |
| KNewStart "Transgressions Unknown" | 000805:Kaidan - Alternate Start Quest.esp | Alt lead-in to K01 (see §6) | 10–50 | K01 30 sets it to 50 and completes it |
| KINV "All of this Past" | 0B3032:0Kaidan.esp | Akaviri relic hunt. Dialogue only, **no scenes**. | 1–40 | 50 complete |
| KMD (no name) | 09F2C0:0Kaidan.esp | Dagon-shrine dialogue tracker. Stage 20 waits 24h then sets 30. Stage 40 starts KMDQuest. | 20–45 (dialogue only) | 50 complete |
| **KMDQuest "Blood and Fire"** | 1CD8FD:0Kaidan.esp (winner KR2_Deadlands_IF_Patch.esp) | Deadlands arc: Dremora attack, shrine, Icy Cave, Rosalind, Deadland temple | 1–50 | 200 (ShutDownStage, set by Rosalind's death script) |
| KMDChangeLocation | 1D009C:0Kaidan.esp | Dremora spawns behind the player. Scene KaiDremoraConfront 1D2839. Started by KMDChangeLocationKicker E7E6FD:IF (CLOC). | whole run (0–100) | 200 ShutDown |
| KMDRosalindScene | 1FA23A:0Kaidan.esp | Rosalind confrontation, non-angst version. Scene KaiRosSC 1FA23C. Started by SM. | whole run | — |
| KMDRosalindSceneAngst | 8E1EA7:IF | Same confrontation, angst version. Scene KaiRosSCAngst 8E1EA9. | whole run | — |
| KR2KMDDeathQuest | 2C45D8:KR2_Deadlands.esp | **StartGameEnabled**. Holds Dagon's speech, scene KR2KMDDagonScene 2ED02E:KR2_Deadlands.esp. Stopped after Rosalind dies. | Do **not** use GetQuestRunning here (it is always running before the finale). Use IsScenePlaying 2ED02E. | — |
| KR2BDAttack | 24553B:KR2_Deadlands.esp | Blooded Dawn cultist ambush. CLOC event, needs KMDQuest ≥ 50. Script Stop()s itself once the cultists aggro. | whole run | stops itself |
| **KMDNightmares "Ashes of His Past"** | 8E7001:IF | Angst arc: brooding, nightmares, pushing the player away. Chained 24–48h timers. Started 24h after KMDQuest 1 when AngstSwitchRos == 1. | 0–42 | 50 (CompleteQuest only, **no Stop**). It stays "running", so use the stage. |
| **KMDRosalindScenePost "Absolution by Dragon Fire"** | 8E1EEB:IF | Aftermath. 5 = KaiTentFGScene. 10 → 48h → 20/25 talks. 30 → letter (72h). 40 → 48h → 50. 60 = Shadowgreen. | 0–70 | 80 = CompleteQuest + Stop() |
| **KaiComp "Vengeance and Honor"** | 162E4A:IF | Companions trial. Scenes KaiComp30/40/65/75Scene, Showdown Part1/2/Kill/NoKill, ZZKaiCompCeremony. 85 starts KaiSTFUQuest. | 30–145 (10 = asked, 48h timer; 20 = 2nd talk) | 150 complete, 200 Stop() |
| KaiCompJorrvaskr | 1D3383:IF | CLOC kicker for the Jorrvaskr leg | whole run | — |
| KDBro | FE62C9:IF (StartGameEnabled) | Kaidan in the Dark Brotherhood. 31 scenes (Astrid/Babette/Nazir/Arnbjorn/Gabriella/Festus, GourmetGuard, PostCoffinFG, MaroKill, KaiKillTarget). 20 = evil switch, 30 = gourmet scene, 60 = post-coffin forcegreet, 70 = Maro kill (KaiDBShutdownScript sets STFU globals). | Scenes only; the quest is always running | — |
| **KaiJail "(Another) Bounty for the Hunter"** | 31506F:IF (RunOnce) | Arrest in Riften. 0 = ArrestScene. 10 = KaiJailedVar=1 (WigOnly). 20–90 = investigation, MavenScene. Started by KaiJailKicker DEB860:IF (CLOC). | 0–90 | 100 = released, KaiJailedVar=0, then 24h → 110 |
| KaiJailNPC | 333736:IF | Riften NPC comments. Scenes BrynKai, FratpackJail. | scenes only | — |
| KaiSandwich | 2DD53E:IF | Horker-sandwich fetch quest. **No scenes.** | (no block needed) | 200 ShutDown |
| KaiSparQst | 22970E:IF | Sparring. Scenes KaiSparPlayerScene, KaiSparIdles. | whole run | 200 ShutDown |
| WEKaiThalmor | 35EE2E:IF | Thalmor ambush world encounter (CLOC). 22 confrontation scenes, then combat at 200. | 0–199 | 255 Stop() |
| KBountyAI "Kaidy Takes A Bounty" | 55EDDE:IF | Kaidan leaves to hunt a bounty. Innkeeper and hand-in scenes. | whole run | 255 Stop() |
| K04 "Romance Progression" | 06D900:0Kaidan.esp | Scenes FirstKissScene 27FB8D, ProposalScene 44A3BA. Most beats run through SceneAnimScript (see §3). | see §5 | — |
| KaidanPreProposal "All the spice" | 0C8EF0:IF | Started at K04 75. Dialogue chain that sets K04 80. | dialogue-gated | — |
| AnimScriptQuest | 8E6CB6:IF | Proposal line ("I know what I want now", which sets K04 81). Scenes WalkOver, HealingSceneHands/Other. | scenes | — |
| **HFSmallWedding "Blood of my Blood"** | 217E07:0Kaidan.esp | Forest wedding at **Myriah's Camp**. 1 = offered, 5 = "need time", 10 = ready (SmallWeddingPreFG), 11 = forcegreet done (KaiWalk, KaiWeddingNukeIdles=1), 15 = altar, 16 = handfasting, 20 = vow (MyriahFGScene), 30 = married, 35 = KaiFGSceneSmallWedding, 36 = idles back on. | 10–36 | 40 ShutDown |
| **HFBigWeddingIF** | 0EC87C:IF | Big wedding at the **Solitude Temple of the Divines** (Rorlund/Silana). 1, 5 → 10, 11 = guests moved + KaiWedding scene + KaiWeddingNukeIdles=1, 30 = married, 35 = hands off to HFWRWedding at stage 32 (reception). | 10–35 | 40 CompleteQuest (no Stop) |
| HFBigWedding (legacy) | 23A8BD:0Kaidan.esp | Old 0Kaidan big wedding, scene BigWed. K04 no longer starts it. | 1–30 | 40 |
| **HFWRWedding** | 46DB25:IF | Whiterun wedding on the **Dragonsreach Great Porch** (worldspace WhiterunDragonsreachWorld). 10 = guests moved, 11 = WeddingScene + Nuke=1, 30 = married + WedScenePartTwo, 32 = FPWRSpeech, 34 = FPGifts, 35, 36 = Nuke=0 → 40. Also used as the reception after HFBigWeddingIF. | 10–36 | 40 CompleteQuest (no Stop) |
| **KaiHoneymoon "With You All The Way"** | A5EA55:IF | 10 = "head to Whiterun" (free roam). 20 = Kaidan leaves. 30–70 = Vilkas/Farkas forcegreets and escort. 80 = KaidanTellsWTTY scene. 100 = MakeTheTrip (fade/teleport). 120 = StoreVars (mutes STFU). 150 complete → 24h → 200 Stop. | 20–149 | 150 / 200 |
| KNPCAddy (Adalyn arc) + KNPCAddyKicker/Enabler, KNPCAddyErikurScene, KNPCAddyKaiScene60, KNPCAddyKaiScene80 | B8F6E2, B8F6E0, B9EB90, B8F706, B8F70A, BB81E3 (all IF) | Addy scenes (AddyKaiIntro, Addy10/20/40/70, AddyErikurScene, AddyKaiScene60, KaiAddyBreakup). Starts on entering the Blue Palace. | scenes / sub-quests running | KNPCAddy 200 |
| KSGRingScene | F6C7EF:IF | Shadowgreen ring scene RingScene F6C7F6 | scene | — |
| MeetBrynQuest | 8B401B:IF | Brynjolf meet scene BrynIsSpicy | scene | 40 |
| KNPCKarisiff | A5EA4E:IF | Bard quest with Kaidan/Vilkas/Brynjolf scenes | scenes | 110 |
| KaiSTFUQuest | F532A2:IF | **Global mute timer.** 100 = store, 200 = NukeVars (sets STFUVarNPCGeneral/Other etc. to 1), 300 = restore + stop. Started by KaiComp 85 and others. | whole run | stops at 300 |
| K02 "Follower Functions" | 0232AB:0Kaidan.esp | ShoppingScene 9ACEF8, SpooningScene EC9019 | scenes | — |
| KIF | 17A9F8:IF | Equipped, FGKiss D862BA, PostWWTransform | scenes | — |

---

## 2a. Conditions to AND onto every talk that involves Kaidan

All are run on Subject unless the "Run on" column says otherwise. `KaidanRef` = 002F9C:0Kaidan.esp and `PlayerRef` = 000014:Skyrim.esm.

**Baseline: is Kaidan available?**

| # | Function | Parameter | Op | Value | Run on |
|---|---|---|---|---|---|
| 1 | GetStageDone | K01 002F9D:0Kaidan.esp, stage 30 | == | 1 | Subject |
| 2 | GetInFaction | CurrentFollowerFaction 05C84E:Skyrim.esm | == | 1 | KaidanRef |
| 3 | GetDisabled | — | == | 0 | KaidanRef |

**Short-beat guards (scene, animation, dialogue)**

| # | Function | Parameter | Op | Value | Run on |
|---|---|---|---|---|---|
| 4 | IsInScene | — | == | 0 | KaidanRef |
| 5 | GetIsCurrentPackage | KaidanDoNothingPkg 098648:IF | == | 0 | KaidanRef |
| 6 | GetIsCurrentPackage | KaidanDoNothingPostSmash 8DCA39:IF | == | 0 | KaidanRef |
| 7 | GetIsCurrentPackage | KaidanJailed 31F288:IF | == | 0 | KaidanRef |
| 8 | GetIsCurrentPackage | KaiReadAI 1B2441:0Kaidan.esp | == | 0 | KaidanRef |
| 9 | GetRestrained | — | == | 0 | KaidanRef |
| 10 | IsInDialogueWithPlayer | — | == | 0 | KaidanRef |
| 11 | IsInCombat | — | == | 0 | KaidanRef |
| 12 | IsInFurnitureState | Lay | == | 0 | KaidanRef |
| 13 | GetInFaction | AnimationFaction 9A2BB9:IF | == | 0 | PlayerRef |
| 14 | IsInFurnitureState | Lay | == | 0 | PlayerRef |

Note on #5: SceneAnimScript and WallLeanAnimScript (via a property named KaiDoNothing) apply KaidanDoNothingPkg as a package override. So does the HSF_DialogueAnims magic effect. GetIsCurrentPackage still sees it.

Note on #9: SceneAnimScript calls SetRestrained and SetDontMove on Kaidan during hugs, kisses and the proposal.

**Global switches (IF.esp)**

| # | Function | Parameter | Op | Value | What it marks |
|---|---|---|---|---|---|
| 15 | GetGlobalValue | STFUVarNPCGeneral F49096:IF | == | 0 | MCM "General NPC convos" toggle. Also nuked to 1 by KaiSTFUQuest, the honeymoon and KDBro. |
| 16 | GetGlobalValue | STFUVarOther F49097:IF | == | 0 | Same mechanism |
| 17 | GetGlobalValue | KNPCStart 932E54:IF | == | 0 | Kill switch, set to 1 when an incompatible Kaidan EE is detected |
| 18 | GetGlobalValue | KaiWeddingNukeIdles 4913A8:IF | == | 0 | 1 during wedding stages 11–36 |
| 19 | GetGlobalValue | KaiJailedVar 31F28D:IF | == | 0 | 1 while he is in Riften jail |
| 20 | GetGlobalValue | AubrieandVaelHateYou 8F1275:IF | == | 0 | 1 = estranged phase of KMDNightmares. Cleared by AshesPostSceneScript. |
| 21 | GetGlobalValue | denialisntjustariver EE8C9B:IF | == | 0 | 1 = his "denial" phase of the angst arc |
| 22 | GetGlobalValue | BlackScene 6E77C5:IF | == | 0 | 1 while a fade-to-black animation scene runs |
| 23 | GetQuestRunning | KaiSTFUQuest F532A2:IF | == | 0 | Timed mute |

**Story-quest windows.** Each block is one OR group. The last line of each group has no OR flag.

| # | Function | Parameter | Op | Value | Flag |
|---|---|---|---|---|---|
| 24 | GetStage | K01 002F9D:0Kaidan.esp | >= | 30 | (AND; a duplicate of #1 written as a stage check, so keep either one) |
| 25a | GetQuestRunning | KMDQuest 1CD8FD:0Kaidan.esp | == | 0 | (single, AND). Blocks the whole Deadlands arc. Use 25b instead if you only want to block the finale. |
| 25b-1 | GetQuestRunning | KMDQuest 1CD8FD:0Kaidan.esp | == | 0 | OR |
| 25b-2 | GetStage | KMDQuest 1CD8FD:0Kaidan.esp | < | 30 | — |
| 26 | GetQuestRunning | KMDChangeLocation 1D009C:0Kaidan.esp | == | 0 | AND |
| 27 | GetQuestRunning | KMDRosalindScene 1FA23A:0Kaidan.esp | == | 0 | AND |
| 28 | GetQuestRunning | KMDRosalindSceneAngst 8E1EA7:IF | == | 0 | AND |
| 29 | IsScenePlaying | KR2KMDDagonScene 2ED02E:KR2_Deadlands.esp | == | 0 | AND |
| 30 | GetQuestRunning | KR2BDAttack 24553B:KR2_Deadlands.esp | == | 0 | AND |
| 31-1 | GetQuestRunning | KMDNightmares 8E7001:IF | == | 0 | OR |
| 31-2 | GetStage | KMDNightmares 8E7001:IF | >= | 50 | — |
| 32 | GetQuestRunning | KMDRosalindScenePost 8E1EEB:IF | == | 0 | AND. IF's own KaiHoneymoon and KaidanPreProposal use this same gate. |
| 33-1 | GetQuestRunning | KaiComp 162E4A:IF | == | 0 | OR |
| 33-2 | GetStage | KaiComp 162E4A:IF | < | 30 | OR |
| 33-3 | GetStage | KaiComp 162E4A:IF | >= | 150 | — |
| 34-1 | GetQuestRunning | KaiJail 31506F:IF | == | 0 | OR |
| 34-2 | GetStage | KaiJail 31506F:IF | >= | 100 | — |
| 35 | GetQuestRunning | KaiSparQst 22970E:IF | == | 0 | AND |
| 36-1 | GetQuestRunning | WEKaiThalmor 35EE2E:IF | == | 0 | OR |
| 36-2 | GetStage | WEKaiThalmor 35EE2E:IF | >= | 255 | — |
| 37 | GetQuestRunning | KBountyAI 55EDDE:IF | == | 0 | AND |
| 38-1 | GetQuestRunning | HFSmallWedding 217E07:0Kaidan.esp | == | 0 | OR |
| 38-2 | GetStage | HFSmallWedding 217E07:0Kaidan.esp | < | 10 | OR |
| 38-3 | GetStage | HFSmallWedding 217E07:0Kaidan.esp | >= | 40 | — |
| 39-1 | GetStage | HFBigWeddingIF 0EC87C:IF | < | 10 | OR |
| 39-2 | GetStage | HFBigWeddingIF 0EC87C:IF | >= | 40 | — |
| 40-1 | GetStage | HFWRWedding 46DB25:IF | < | 10 | OR |
| 40-2 | GetStage | HFWRWedding 46DB25:IF | >= | 40 | — |
| 41-1 | GetStage | HFBigWedding 23A8BD:0Kaidan.esp | < | 1 | OR |
| 41-2 | GetStage | HFBigWedding 23A8BD:0Kaidan.esp | >= | 40 | — |
| 42-1 | GetQuestRunning | KaiHoneymoon A5EA55:IF | == | 0 | OR |
| 42-2 | GetStage | KaiHoneymoon A5EA55:IF | < | 20 | OR |
| 42-3 | GetStage | KaiHoneymoon A5EA55:IF | >= | 150 | — |
| 43 | GetQuestRunning | KNPCAddyErikurScene B8F706:IF | == | 0 | AND |
| 44 | GetQuestRunning | KNPCAddyKaiScene60 B8F70A:IF | == | 0 | AND |
| 45 | GetQuestRunning | KNPCAddyKaiScene80 BB81E3:IF | == | 0 | AND |

Rows 43–45 are the same as IF's own KNPCBrelkas blocks.

**Scripted places.** Any of these on Subject, all `== 0`, AND. The full list is in §4.

- GetInCell 021594:Skyrim.esm (AbandonedPrison01)
- GetInCell 0C1E4B:0Kaidan.esp (Icy Cave)
- GetInCell 0C1FF5:0Kaidan.esp (Deadland Temple)
- GetInWorldspace 00AA4C:KR2_Deadlands.esp (Deadlands)
- GetInCurrentLoc 0240E6:Skyrim.esm (Dagon shrine)
- GetInCell 0A8B23:Skyrim.esm (Riften Jail)
- GetInCurrentLoc 2101CD:IF (Vargr Den)
- GetInCurrentLoc 018E34:Skyrim.esm (High Hrothgar)

**Vanilla scenes Kaidan's own mods pause for.** Taken verbatim from KaiandInigo, KNPCBrelkas and KNPCWolfTwins.

- IsScenePlaying C01AmbushScene 0A6F59:Skyrim.esm == 0
- IsScenePlaying MQ106AlduinScene 032DA3:Skyrim.esm == 0
- IsScenePlaying MQ104DragonDeathScene 05A6BD:Skyrim.esm == 0
- GetStage MQ104 02610C:Skyrim.esm != each of 60, 65, 70, 80, 90, 92, 95, 100, 105 (nine AND lines)
- GetStage C02 06E804:Skyrim.esm != 10 and != 20
- GetStage C04 01CEF5:Skyrim.esm != 30
- GetQuestRunning C05 06E805:Skyrim.esm == 0
- GetQuestRunning C06 01CEF6:Skyrim.esm == 0
- GetQuestRunning CWSiegeObj 096E71:Skyrim.esm == 0
- IsScenePlaying BalgruufKaiScene 33D98B:IF == 0
- IsScenePlaying ShoppingScene 9ACEF8:IF == 0

**What KaiandInigo's DialogConditions already have, verbatim (29 lines)**

- Globals == 0: STFUVarNPCGeneral, KaiJailedVar, KNPCStart, KaiWeddingNukeIdles, AubrieandVaelHateYou, denialisntjustariver
- Places == 0: GetInCurrentLoc ShrineofMehrunesDagon; GetInCell 00DeadlandCave and 00DeadlandTemple; GetInCell AbandonedPrison01; GetInCurrentLoc HighHrothgar
- GetInFaction AnimationFaction on PlayerRef == 0
- IsScenePlaying C01AmbushScene == 0 and MQ106AlduinScene == 0
- C04 != 30; C05 not running; C06 not running; C02 != 10 and != 20
- MQ104 != 60/65/70/80/90/92/95/100/105
- GetIsCurrentPackage KaidanDoNothingPkg on KaidanRef != 1

**What it lacks, and this list adds:**

- KMDQuest, KMDNightmares and KMDRosalindScenePost windows
- The Rosalind and Dagon scenes, and the Deadlands worldspace
- Wedding stage windows outside the Nuke global (stages 10–11 and 36)
- Honeymoon
- KaiComp, KaiSTFUQuest, WEKaiThalmor, KBountyAI, KaiSparQst
- Riften Jail cell, the BlackScene global, GetRestrained, IsInDialogueWithPlayer, IsInScene

## 2b. Shorter list for talks that do not involve Kaidan

Use these when the player is at one of his big set pieces. Run on Subject, AND unless marked.

1. GetGlobalValue KaiWeddingNukeIdles 4913A8:IF == 0
2. HFSmallWedding window, OR group 38-1..38-3
3. HFBigWeddingIF window, OR group 39-1/39-2
4. HFWRWedding window, OR group 40-1/40-2
5. GetInCell SolitudeTempleoftheDivines 016A02:Skyrim.esm == 0. Optional; it is a vanilla temple, so only do this while 39 is in its window.
6. Honeymoon, OR group: GetQuestRunning KaiHoneymoon == 0 OR GetStage KaiHoneymoon < 80 OR GetStage >= 150. Stages 80–149 cover the surprise scene and the trip.
7. KMD finale:
   - GetStage KMDQuest 1CD8FD:0Kaidan.esp < 50 OR GetQuestRunning KMDQuest == 0
   - GetQuestRunning KMDRosalindScene 1FA23A == 0
   - GetQuestRunning KMDRosalindSceneAngst 8E1EA7:IF == 0
   - IsScenePlaying KR2KMDDagonScene 2ED02E:KR2_Deadlands.esp == 0
   - GetInWorldspace KR2Deadlands 00AA4C:KR2_Deadlands.esp == 0
   - GetInCell 0C1FF5:0Kaidan.esp == 0
   - GetInCell 0C1E4B:0Kaidan.esp == 0
8. Companions climax: IsScenePlaying ShowdownPart1 1D3389:IF, ShowdownPart2 1DD5BC:IF, ShowdownKill 1E26EE:IF, ShowdownNoKill 1E26EF:IF and ZZKaiCompCeremony 1EC940:IF, each == 0
9. Proposal and first kiss: IsScenePlaying ProposalScene 44A3BA:IF == 0 and FirstKissScene 27FB8D:IF == 0
10. Romance animations: GetInFaction AnimationFaction 9A2BB9:IF == 0 on PlayerRef, and GetGlobalValue BlackScene 6E77C5:IF == 0
11. Arrest: IsScenePlaying ArrestScene 315075:IF == 0

## 3. Is IsInScene(Kaidan) + GetIsCurrentPackage KaidanDoNothingPkg enough for short beats?

**No.** It catches every running Scene that has Kaidan as an actor. That covers about 1,400 scenes: IF ambient scenes, NPC banter, forcegreet scenes, wedding scenes and the Rosalind scene. It also catches the dialogue-animation and wall-lean lock.

What it misses (verified in the scripts):

1. **SceneAnimScript and HSF_Kabedon animations**: hugs, kisses, the proposal (K04 81) and the tent kiss. These are not Scenes. They:
   - add the player to AnimationFaction 9A2BB9
   - call SetRestrained/SetDontMove on Kaidan
   - sometimes set BlackScene and fade to black

   AnimationFaction covers them. Add GetRestrained and BlackScene as backups. The "post-smash" lock uses a second package, **KaidanDoNothingPostSmash 8DCA39**.
2. **Forcegreets that are alias packages, not scenes.** Examples: the KaiComp 85 dungeon forcegreet, the KaiComp 110 Wulf forcegreet, the honeymoon Vilkas/Farkas forcegreets (30–70), KaidanCaveFG BF9692 in the Deadlands. Kaidan is walking at the player with no scene running. Only the quest-stage windows catch these.
3. **Gaps between scene phases** inside a set piece:
   - wedding stage 10 → 11 (guests teleported, waiting at the altar), and 36 → 40 (60-second wait)
   - honeymoon stages 20–70 (Kaidan has left and the twins escort the player)
   - the nightmare and Rosalind-post arc (days of mood with no scene running)
4. **Fade, teleport and disable beats** with no actor in a scene: honeymoon MakeTheTrip at 100, and the Dagon fade sequence. The Dagon fade disables player controls, kills the cultists and plays the Dagon scene, and Kaidan is not one of its actors.
5. **Jail.** Kaidan sits in the Riften Jail cell on the KaidanJailed package with no scene running (KaiJailedVar).
6. **Player-Kaidan dialogue menus** (IsInDialogueWithPlayer). **Combat**: Thalmor ambush, Wulf showdown, cultists.
7. **Sleeping or lying in bed**: KaiSpoonQst, KaidanSleep.
8. **IF's own mute windows** (KaiSTFUQuest, STFUVarNPCGeneral), which IF raises during the honeymoon and KDBro moments.

## 4. Scripted locations and cells to exclude

| Place | Condition | FormID | Used by |
|---|---|---|---|
| Abandoned Prison (interior) | GetInCell | 021594:Skyrim.esm | K01 rescue. Also location AbandonedPrisonLocation 0ECF4C:Skyrim.esm; exterior cell 009627:Skyrim.esm. |
| Shrine of Mehrunes Dagon | GetInCurrentLoc | 0240E6:Skyrim.esm | KMD / KMDQuest |
| Icy Cave (00DeadlandCave) | GetInCell | 0C1E4B:0Kaidan.esp (location DeadlandCave 1FCA04:0Kaidan.esp) | KMDQuest 30–40 |
| Deadland Temple | GetInCell | 0C1FF5:0Kaidan.esp (location DeadlandTempleLOC 1FA263:0Kaidan.esp) | Rosalind fight |
| KR2 Deadlands worldspace | GetInWorldspace | 00AA4C:KR2_Deadlands.esp (location KR2DeadlandsLocation 00AFC4:KR2_Deadlands.esp) | KR2 finale |
| Blooded Dawn cells | GetInCell | KR2BDCELL01 1841C0, KR2BDCELL02 18420D, KR2BDCELL03 193665 (all KR2_Deadlands.esp) | KR2 cultist content |
| Myriah's Camp (small/forest wedding) | GetInCurrentLoc | KaiMyriahCampLoc 22E2AC:0Kaidan.esp (cell 00984F:Skyrim.esm) | HFSmallWedding |
| Forest Wedding Renewal location | GetInCurrentLoc | KaiForestWeddingLoc 00011C:Kaidan - IF - Forest Wedding Renewal.esp | same venue, re-dressed |
| Solitude Temple of the Divines | GetInCell | 016A02:Skyrim.esm | HFBigWeddingIF. Gate it on the wedding window; it is a vanilla temple. |
| Dragonsreach Great Porch | GetInWorldspace | WhiterunDragonsreachWorld 046033:Skyrim.esm | HFWRWedding. IF's banter blocks this always. |
| Riften Jail | GetInCell | 0A8B23:Skyrim.esm (location 0A8C86) | KaiJail |
| Vargr Den | GetInCurrentLoc / GetInCell | VargrDenLocation 2101CD:IF / VargrDen 15DBD8:IF | KaiComp 85–120 |
| Jorrvaskr | GetInCurrentLoc | 01F877:Skyrim.esm | KaiComp ceremony. Gate on the window only. |
| The Underforge | GetInCell | 0165A6:Skyrim.esm | IF blocks frathouse banter here |
| High Hrothgar | GetInCurrentLoc / GetInCell | 018E34 / 087764:Skyrim.esm | Greybeards scenes |
| Blue Palace | GetInCurrentLoc | 020086:Skyrim.esm | Adalyn scenes. Gate on the KNPCAddy quests. |
| Kaidan's Tent interior | GetInCell | KaiTentCell 636392:IF | Intimate and sleep beats. Optional. |
| Palace of the Kings, Castle Dour Emperor's Tower, Bronze Water Cave | GetInCell | 01677C, 019454, 054226:Skyrim.esm | IF's own NPC-banter exclusions (Ulfric scenes, K04 blocks) |

KR2_KaidanAlternateAIO.esp has **no quests, scenes or packages**. It is 194 placed objects in 6 cells plus one worldspace edit, so it is cosmetic. Nothing in it needs blocking.

## 5. K04 romance stage map (from fragment comments and condition use)

Sources: the comments in the K04 fragments (QF_K04_0406D900) mapped to stages through the VMAD, which TIFs set which stage, and a census of 1,826 INFO conditions that test K04.

| Stage | Meaning (verified) | Phase for banter gating |
|---|---|---|
| 0 | not started. Also 0 again after ResumeRomanceScript Reset()/Stop() pauses the romance for 168h. | none |
| 5 | asked about the Amulet → "ever thought about marriage" talk | crush / flirting |
| 10 | asked about marriage (timer) | flirting |
| 15 | "surprised you're not taken" (timer → 20) | flirting |
| 20 | "ever been in love" talk | flirting |
| 25 | timer before first night (ResumeRomance re-enters here) | courting |
| 30 | first night available | courting |
| 35 / 36 / 37 | night choice: spicy / shy / **platonic** (timer → 40/41/42) | intimate |
| 40 / 41 / 42 | morning-after talk: spicy / shy / **platonic** | intimate |
| 45, 50 | marked "Unused?" in the source. Lines still test `>= 50` (43 lines, e.g. danger sense), so ≥ 50 effectively means "past the morning-after". | together |
| 55 / 56 / 57 | post-night reply: spicy / shy / **awkward**. The Amulet becomes available. | together |
| 60 / 61 / 62 | Kaidan's love declaration: steamy / sweet / awkward | in love (his confession) |
| 65 | holding timer after he declares → 70 | in love |
| 70 | the player declares love back | lovers (Inigo "Relationship" ≥ 70) |
| 75 | timer; **starts KaidanPreProposal** | committed (pet names, Inigo MetMatch ≥ 75) |
| 80 | proposal available (set by KaidanPreProposal dialogue) | pre-engaged |
| 81 | proposed / accepted (KaiAnimScript proposal animation, KaiProposalLineTopic) | engaged |
| 85 | big wedding chosen → starts HFBigWeddingIF | engaged, wedding pending |
| 87 | Whiterun wedding chosen → starts HFWRWedding. The source comment wrongly says "85". | engaged, wedding pending |
| 90 | small wedding chosen → starts HFSmallWedding | engaged, wedding pending |
| 100 | married. Set by the post-wedding talk (PostWedB3/PostWedB4 TIFs); the wedding quests do not set it. | married (Inigo wedding scene ≥ 100) |

**Correction to the character sheet:** 85 is not "married". 85/87/90 are the three "wedding type picked" stages, and only 100 is married. PlayerMarriedFaction is added at wedding stage 30, so `GetInFaction PlayerMarriedFaction` on KaidanRef also marks married.

**Platonic branch:** 37 → 42 → 57. About 45–53 romance lines each test `!= 37`, `!= 42` and `!= 57`. A banter gate meant for "in a romance" should copy those three exclusions.

**Thresholds most used in conditions:** ≥ 5 (69 lines), ≥ 30 (55), ≥ 60 (166), ≥ 65 (202), ≥ 75 (325), < 75 (138), ≥ 80 (129), ≥ 100 (62).

**Suggested gates:**
- flirting: ≥ 5 AND < 30
- together: ≥ 50 AND not 57
- in love: ≥ 65 (or ≥ 60 for his side only)
- engaged: ≥ 81 AND < 100
- married: == 100

## 6. Alternate start (`Kaidan - Alternate Start Quest.esp`)

- **It does not skip Helgen** and the player does **not** start with Kaidan. Its masters are only the vanilla files and the three Kaidan plugins (no Alternate Start - Live Another Life). It touches no Helgen records other than exterior cells for placed objects.
- It adds quest **KNewStart "Transgressions Unknown"** 000805:Kaidan - Alternate Start Quest.esp. That quest is StartGameEnabled and RunOnce, with DialogConditions `GetDisabled == 0 on KaidanRef` and `GetStage K01 < 10`. It is a lead-in investigation that ends at the Abandoned Prison:
  - 10: rumour of a big bounty
  - 15: an innkeeper hands over the letter
  - 20: the Thalmor are hunting a man in Falkreath Hold
  - 30: the Falkreath innkeeper says he was taken toward Ivarstead
  - 40: the Ivarstead innkeeper points to the prison near Fort Amol
  - 50: screams heard at the prison
- It adds 16 "Thalmor Bounty Notice" books (KaiBounty02–16) and a KaidanScreamMarker NPC. It overrides K01, which stays the rescue quest, and Kaidan's Meet01, Meet06, MeetBad and MeetWait topics.
- K01 stage 30 (rescue complete) sets KNewStart to 50 and completes it.
- `Kaidan - IF - Alt Bounty Start.esp` (master: Alternate Start Quest) adds an activator, 00KaiBountyAct "Bounty", on notice boards. BountyScript gives the player a KaiBounty book and disables the poster. It is just another way to pick up the lead.
- **For banter:** Kaidan is not available until K01 stage 30. Gate with `GetStageDone K01 30 == 1`. Alternatively use `GetQuestCompleted K01 == 1` together with `GetStage K01 >= 30`, because stage 6 ("left him to his fate") also completes K01.

---

### Facts that were verified rather than assumed

- **KR2KMDDeathQuest is StartGameEnabled.** Only Rosalind's death script stops it, so do not gate on it being "running".
- **Kaidan does not die in the KR2 branch.** Player death at KMDQuest 40 only plays Dagon's laugh, and at stage > 40 it stops the death quest. Rosalind's death plays the Dagon scene.
- **The weddings, KMDNightmares and HFWRWedding never call Stop().** Those windows use stage bounds, not GetQuestRunning alone.
- **WEKaiThalmor and KBountyAI Stop() at 255. KR2BDAttack Stop()s itself after the ambush.** GetQuestRunning is safe for those three.
