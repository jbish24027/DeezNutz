# Story-beat blocks, follow/wait checks and "done" gates — 7 followers

Read live from the load order (houseCARL, profile DEEZ CS NUTZ - PICTA, epoch e2-52b2b71e586571f0) on 2026-10-18.
Quest fragments and controller scripts were decompiled to `triggers\work\psc\`. Nothing in the instance was written.

Notation: `Q:Plugin` FormIDs are plugin-local (use these in GetFormFromFile / soft deps). CFF = `CurrentFollowerFaction 05C84E:Skyrim.esm`.
**[CONFIRMED]** = read from records/fragments. **[INFERRED]** = journal text or naming, not proven. **[UNCONFIRMED]** = could not verify.

## 0. Cross-cutting findings (read first)

1. **Most of these quests are Start Game Enabled** (flags 273/281/17). `GetQuestRunning` is TRUE all game for them, so it means nothing. Use stage windows (`GetStage >= A` AND `GetStageDone(end) == 0`) instead. Only RunOnce-without-StartEnabled quests below can use `GetQuestRunning`.
2. **CFF is NOT a universal "following" test here**:
   - Val is **never** in CFF (his alias adds `PlayerFollowerFaction` + `AX_ValRecruitedFaction`; his `SetFollower` never touches CFF). [CONFIRMED]
   - Inigo is **removed from CFF on every game load** by `InigoStatusQuestScript.OnInit` (he also clears himself out of DialogueFollower). [CONFIRMED]
   - Gore adds CFF in script; Remi, Xelzaz, Lucien, Redcap get CFF from their follower alias (alias faction list). [CONFIRMED]
   - CFF/teammate stays set while a follower is told to wait, so **every "following" test must also check `GetActorValue WaitingForPlayer == 0`**.
3. Universal "not busy" set to put on every opener for both speakers (on top of the per-follower blocks): `IsInScene == 0`, `IsInDialogueWithPlayer == 0`, `GetCombatState == 0`, `GetDead == 0`, `GetUnconscious == 0`, `IsBleedingOut == 0` (or `GetActorValue ... ` equivalent), `GetSleeping == 0`. Most forcegreets and story scenes are scenes, so `IsInScene == 0` already kills a lot.
4. Runtime prefixes in this order (all full plugins, none ESL): GORE 25, Gore - Vigilant 26, AX ValSerano 23, HLIORemi 8E, BPUFXelzazFollower 8F, Inigo 83, Lucien 8D, FA01RedcapFollower 99.

---

## 1. GORE (GORE.esp + Gore - Vigilant.esp)

### 1a. Ready-made "Gore is free to chat" block [CONFIRMED]
Gore's own follower-chatter quest **HD1GoreFollows 066722:GORE.esp** (winner Gore - Vigilant.esp) carries this quest-level DialogConditions block. Copy it as the Gore-side block. All `on Subject` = on Gore.

| Condition | Global/target |
|---|---|
| GetGlobalValue != 1 | HD1PermanentDismiss 1BB9E1:GORE.esp |
| GetQuestCompleted == 1 | HD1GorePostThalmor 534312:GORE.esp |
| GetGlobalValue == 0 | HD1GoreQuest2ScenesVar 617FB4:GORE.esp (Blood Ties scenes) |
| GetGlobalValue == 0 | HD1GoreJailed 61307D:GORE.esp (in Dawnstar cell) |
| GetGlobalValue == 0 | HD1GoreJailing 650E80:GORE.esp (walking to jail) |
| GetGlobalValue == 0 | HD1GoreMurdererVar 6738F5:GORE.esp (left after the murder) |
| GetGlobalValue == 0 | HD1PostBailVar 6DDFF2:GORE.esp |
| GetGlobalValue == 0 | HD1PostJuneVar 6DDFF3:GORE.esp (Come, the Crows pending) |
| GetGlobalValue != 1 | HD1YoureDB 8EB057, HD1MQ04Var 8E397E, HD1SCConv 876ABC, HD1GoreVampAnger 831586, HD1DawnGuarded 842AD1, HD1GoreDBKNSVar 90DAE4, HD1GoreThalmorEmbassySurprise 944230, HD1GoreMQGLHFVar 95A6D6, HD1GoreWWTurnVar 984823, HD1FALSFear B044E2 (all :GORE.esp) |
| GetGlobalValue == 0 | GoreDA14VAR ABA0A0:GORE.esp |
| GetStage != 5 / != 10 / != 20 | HD1Interlude2 89E472:GORE.esp (Nest Left Empty waterfall/ambush) |
| GetInCell != 1 | MarkarthAbandonedHouse 018BE9:Skyrim.esm |
| GetGlobalValue == 0 | HD1WTCHVar 02AE4E:Gore - Vigilant.esp |
| GetGlobalValue != 3 | HD1VAct2Var 251CCC:Gore - Vigilant.esp |
| GetInCell == 0 | Vigilant.esm cells 16E303, 004102, 00185B, 03289E, 031BE5, 035441, 0302D8, 034E12, 24ABFB, 24D519, 252537, 036E7E, 033B80 |
| GetInWorldspace == 0 | zAoMWitchWorld 166857:Vigilant.esm |

Also skip when relaxing if you want: `HD1RelaxVar 3E3CC7:GORE.esp == 1` (told to relax — his tavern scenes use it).

### 1b. Personal quests with scenes/forcegreets and their "beat in progress" test
None of these is Start-Enabled except where noted, so GetQuestRunning works for them.

| Quest | FormID | Beat in progress |
|---|---|---|
| Raven's Flight HD1GoreMeet | 066720:GORE.esp | GetQuestRunning == 1 (pre-recruit) |
| Wanted HD1GoreEscort | 1517F2:GORE.esp | GetQuestRunning == 1 |
| The Drunken Hunted HD1GoreDH | 3E8DC9:GORE.esp | GetQuestRunning == 1 |
| Blood Ties HD1GoreQuest2 | 5A610A:GORE.esp | GetQuestRunning == 1 AND GetStage >= 10 (stage 0 = "get to know Gore", can idle long). Plus HD1GoreQuest2ScenesVar == 1 |
| The Apple from the Tree HD1GoreMurderer | 6738F7:GORE.esp | GetQuestRunning == 1 |
| To Free a Raven HD1GoreJailtime | 6245B4:GORE.esp | GetQuestRunning == 1 (stages 0-40; 50 = complete). Plus HD1GoreJailing/HD1GoreJailed == 1 |
| Come, the Crows HD1GoreComeTheCrows | 6EA61E:GORE.esp | GetQuestRunning == 1 |
| Where We Stand HD1GoreInterlude | 7752FD:GORE.esp | GetQuestRunning == 1 AND GetStage >= 10 |
| Nest Left Empty HD1Interlude2 | 89E472:GORE.esp | GetStage == 5/10/20 (as above) |
| A New Coat HD1ArmorUpgrades | 10A083:GORE.esp | GetQuestRunning == 1 (Taarie errand; low risk) |
| Count Fleet HD1GoreHorse1 | 2EADD8:GORE.esp | GetQuestRunning == 1 (low risk) |
| Fear and Loathing HD1GoreFearAndLoathing | AFF592:GORE.esp | GetQuestRunning == 1 |
| Fading Memories HD1MemoriesQ | 0C6188:Gore - Vigilant.esp | GetQuestRunning == 1 (Coldharbour) |
| Oath trip HD1RomanceTracker | C34C94:GORE.esp | **HD1GoreRomance3 6EA61C == 2** (oath accepted, travelling to Heide's shrine = tracker stage 20). Scene HD1OathsSworn D99611 at the shrine. |
| HD1GoreDawnguard | 7FADBA:GORE.esp | GetQuestRunning == 1 [INFERRED meaning] |

### 1c. Following / waiting [CONFIRMED from HD1GoreController]
- Following: `GetInFaction CFF == 1` AND `GetActorValue WaitingForPlayer == 0` on Gore (ref 00B4B1). Alternative: `IsPlayerTeammate == 1`.
- Recruited global: `HD1GoreRecruited 00B4B8:GORE.esp == 1` (the controller's FollowerRecruited; 0 on dismiss, stays 1 while waiting).
- Waiting: `GetActorValue WaitingForPlayer == 1`. Relaxing: `HD1RelaxVar 3E3CC7 == 1`.

### 1d. "Done" gates
| Talk needs | Condition |
|---|---|
| Bailed out of Dawnstar jail | `GetQuestCompleted HD1GoreJailtime 6245B4 == 1` (stage 50, after the Windpeak Inn talk). Bail itself = `GetStageDone 6245B4, 30 == 1` [INFERRED: 20 "speak to guard", 30 "speak to Gore"]. |
| Learned Jo-Lee is his father | `GetQuestCompleted HD1GoreQuest2 5A610A == 1` (stage 60). Also exclude the murder branch: `HD1GoreMurdererVar 6738F5 == 0`. |
| Swore the oath at his mother's shrine | `GetGlobalValue HD1GoreRomance3 6EA61C >= 3` [CONFIRMED: TIF D99613 sets it to 3 and sets tracker stage 30 at the shrine; TIF DAAB4B sets 4 on the "That was perfect" reply, so do not test == 4]. Equivalent: `GetStageDone HD1RomanceTracker C34C94, 30 == 1`. |
| Romance tiers | Interest `HD1Romance 6D6924 == 1`; tier 1 `HD1GoreRomance1 6EA61A == 1` (hand-holding); tier 2 `HD1GoreRomance2 6EA61B == 1` (lovers); tier 3 `HD1GoreRomance3 6EA61C >= 1` (committed; 1 = unlocked, 2 = travelling to shrine, 3/4 = oath sworn). Breakup `HD1Breakup C0D2F2 == 1` should veto romance talks. |

### 1e. Soft dependency
`Game.GetFormFromFile(0x00B4B1, "GORE.esp")` → HD1GoreRef (base HD1Gore 000D63).

---

## 2. VAL SERANO (AX ValSerano.esp + addons)

### 2a. His own "don't chatter" globals [CONFIRMED, used as quest DialogConditions across his quests]
- `AX_ValSightlessPit 9B244D == 0` (he is captive in the Sightless Pit, Val00B)
- `AX_ValSleepy 3D336D == 0`
- `AX_ValNoTeleport BE10CD == 0`
- His story quests also require `AX_LieHiding 1F6168 == 0` and `AX_LiePirate 1F6165 == 0` (lie branches during Val002/Val003).
- NPC-comment cooldown: `AX_RandomNPCBanterCD 2AEF93`.
- `ValCatchUp 2A2884` is **not** a story gate. It is his teleport-to-player helper (`AX_ValCatchUpFunctionsScript.ValCatchUp()`). Ignore it for blocking.

### 2b. Personal quests and "beat in progress" (all :AX ValSerano.esp)
| Quest | FormID | Beat in progress |
|---|---|---|
| Val001 Between the Daedra and the Deep Blue Sea | 2EE9A6 | GetQuestRunning == 1 (pre-recruit) |
| Val002 He Runs a Tight Shipwreck | 33AAF4 | GetQuestRunning == 1 AND GetStage >= 20 (10 = startup "he promised to answer questions") |
| Val003 But You Have Heard of Me (Morag Tong/Tarek) | 3AA4A7 | GetStage >= 10 AND GetStage < 200 (0 = dormant until the ambush) |
| ValTarek Dead Reckoning | 0A0A24 | GetStage >= 10 AND GetStageDone 199 == 0 AND GetStageDone 200 == 0 |
| Val005 Drink and the Daedra... | 49DC31 | GetStage >= 3 AND GetStage < 200 |
| Val005SB Sailor's Bargain (Apocrypha) | AAFF95 | GetQuestRunning == 1 (also GetInCurrentLoc 652304 == 1) |
| Val006 Safe Harbor | 49DC32 | GetStage == 20 (boat bought, low risk) |
| Val00A Romancing the Rogue (Start-Enabled) | 3AA4A5 | romance-beat stages 5,6,7,22,32,42,24,34,44,26,36,46 [INFERRED: these are the date/ask stages]. Plus the date quests below. |
| Date quests | Val00ALakeDate D73448, Val00ASpringsDate E80A0E, Val00AViewDate B7B6D5 | GetQuestRunning == 1 on any |
| Val00B Wicked Game (kidnap) | 49DC33 | GetStage >= 15 AND GetStage < 200 (also AX_ValSightlessPit == 1) |
| Val00C Making an Honest Man of Him (wedding) | 9B2444 | GetStage >= 40 AND GetStage < 200 [ceremony stages 40-50 / 110-130] |
| Val00D Wing and Wing | 49DC34 | GetStage >= 15 AND GetStage < 90 |
| Val00E Several Nights to Remember | 22FFC1 | GetStage >= 10 AND GetStage < 200 |
| ValCOLGrad The Daedra to Pay | 6682E2 | GetStage >= 70 AND GetStage < 198 (injury, Sigil Stone, Storm Golem) |
| ValCOLGradPres Seafaring by the Stars | 356D21 | GetStage >= 60 AND GetStage < 200 (stargazing camp) |
| ValEnd The Bitter End | B5FA4C | GetStage >= 10 (betrayed; he is hostile) |

### 2c. Following / waiting [CONFIRMED from AX_ValController]
- Following, not waiting: `GetGlobalValue AX_ValRecruited 08E466 == 1` (1 follow, 2 wait, 0 dismissed).
- Belt and braces on Val's ref: `GetInFaction AX_ValRecruitedFaction E0938C == 1` AND `GetActorValue WaitingForPlayer == 0` (his own quest DialogConditions use exactly this pair on Reference 07A065).
- **Do not use CFF for Val.** (Remiel's own Morvic forcegreet uses CFF on Val, so it can never fire. Not our bug, but do not copy it.)

### 2d. "Done" gates
| Talk needs | Condition |
|---|---|
| Confronted his father | `GetQuestCompleted Val003 3AA4A7 == 1` (200 = Tarek spared, 201 = Tarek slain). Fine-grained: `GetStageDone Val003, 70 == 1` (spared) / `GetStageDone Val003, 71 == 1` (slain); globals `AX_TarekAlive` / `AX_TarekDead` (FormIDs not pulled). |
| Saved Fathis | `GetQuestCompleted Val005 49DC31 == 1` (stage 200 "rescued Fathis... brothers reconciled"). Val005SB alone completes at 200/201 (Apocrypha journal), it is a sub-step, so gate on Val005. |
| Romance: flirting only | `GetStage Val00A 3AA4A5 >= 10` AND `AX_Love 577EB8 == 0` AND `AX_FriendZone 4D5987 == 0`. Tone: `AX_Mild 3E2152` / `AX_Hot 3E2153` / `AX_Spicy 3E2154` == 1. |
| Romance: lovers | `AX_Love 577EB8 == 1` (set at Val00A 200/300/400). "Rough waters" = Val00A 201/301/401 done and AX_Love == 0. Just friends = `AX_FriendZone == 1`. |
| Engaged / married | `AX_ValEngaged A2205B == 1`; `AX_ValMarried A22094 == 1` (Val00C 200 Dark Rose / 201 Mara; 202 = committed, no marriage). |
| College graduate | `AX_ValCollegeGraduated 087342 == 1` (his own dialogue gates on it). [UNCONFIRMED which script sets it: not in the ValCOLGrad stage fragments; ValCOLGrad's VMAD references it]. Alternative: `GetQuestCompleted ValCOLGrad 6682E2 == 1` (master Conjuration arc) or `GetQuestCompleted ValCOLGradPres 356D21 == 1` (graduation present). |

### 2e. Soft dependency
`Game.GetFormFromFile(0x07A065, "AX ValSerano.esp")` → AX_ValSeranoREF (base 00AA0F).

---

## 3. REMIEL (HLIORemi.esp)

### 3a. Her own "don't chatter" globals [CONFIRMED, quest DialogConditions on her banter quests]
- `HLIOScrapAttackMode 5E73DD == 0` (combat mode; every one of her banter quests requires 0)
- `HLIOPuzzleTime 82F1DD != 1` (Arkngchal lever puzzles)
- Not in Markarth Cidhna Mine: `GetInCurrentLoc 018C91:Skyrim.esm == 0` (used by her follower quest)

### 3b. Personal quests and "beat in progress" (all :HLIORemi.esp)
| Quest | FormID | Beat in progress |
|---|---|---|
| The Dwemer Specialist HLIOStartingQuest (Start-Enabled) | 0E4852 | GetStage >= 5 AND GetStage < 110 (pre-follower intro) |
| Reunion of the Fallen HLIOMQ1 (Start-Enabled) | 46FA55 | GetStage >= 10 AND GetStageDone 220 == 0 AND GetStageDone 230 == 0. 180/185 = Remi meets Morvic alone; 200/210 = she stays at Arkngchal (not following). |
| Exploring Arkngchal HLIOArkngchalManager | 6A304E | GetStage >= 1 AND GetStage < 60 (also HLIOPuzzleTime) |
| Upgrades HLIOScrapUpgrades | 08E59F | GetStage == 50 (the "ask her about our adventures" talk) |
| Remi's Crossbow Crucible HLIORPCrossbow | 22DCD3 | GetStage >= 10 AND GetStage < 40 |
| Picking Remi's Brain HLIORPLock | 237EE7 | GetStage >= 20 AND GetStage < 70 |
| We Who Challenge the Sun HLIORPLantern | 8486EB | GetStage >= 10 AND GetStage < 50 |
| Attuned Assassination HLIOADQuest | 62E259 | GetStage >= 20 AND GetStage < 70 |
| Real Nord Food HLIOChaurusPieQuest | 59B47F | GetStage >= 30 AND GetStage < 80 |
| Marriage HLIORemiMarriage | 3211E5 | GetStage == 10 (wedding pending) |
| Romance HLIORemiRomance | 3262FF | forcegreets at HLIORomanceGlobal 326314 thresholds 3/6/9/12 — not stage-blockable; rely on IsInScene/IsInDialogueWithPlayer |

The craft-project quests (crossbow, lock, lantern, tuning fork, pie) are errand chains, not tense story beats. Block them only if a talk would contradict them.

### 3c. Following / waiting [CONFIRMED]
- Following: `GetInFaction CFF == 1` (from her `Remi` alias on HLIORemiFollower 014C11) AND `GetActorValue WaitingForPlayer == 0`.
- Recruited global: `HLIORemiRecruited 014C10:HLIORemi.esp`.
- Never put her through NFF/AFT.

### 3d. "Done" gates
| Talk needs | Condition |
|---|---|
| Morvic killed | `GetStageDone HLIOMQ1 46FA55, 190 == 1` (journal: "we managed to kill him"). **Do not use GetQuestCompleted**: stage 230 also completes the quest and is the branch where the player talks her out of revenge. Workshop set up: `GetStageDone 46FA55, 220 == 1`. |
| Scrap at the steam level | `GetStageDone HLIOScrapUpgrades 08E59F, 50 == 1` [CONFIRMED: stage 50 fragment gives her HLIOConjureScrapLvl3; HLIOScrapLvl3 005904 carries "Steam Breath" HLIOcrDwarvenSpiderSteamBreath 08E5A0]. Ladder: 10 lvl1, 20 lvl1.5, 30 lvl2 (shock spit), 40 lvl2.5 (shock spit), 50 lvl3 (steam). 60/70/80 = arc done (70 = romance available, 80 = she was sent away). |
| Intro done | `GetQuestCompleted HLIOStartingQuest 0E4852 == 1` (all her banter uses this) |

### 3e. Soft dependency
`Game.GetFormFromFile(0x033226, "HLIORemi.esp")` → Remi's placed ref (base 005900). Scrap banter ref: `0x885448` (base HLIOChillScrap 885444).

---

## 4. XELZAZ (BPUFXelzazFollower.esp)

### 4a. His own "don't chatter" gates [CONFIRMED, quest DialogConditions on nearly every quest]
- `IsUndead == 0` on his ref 0893E1 (vampire branch)
- `GetStageDone BPUFXelzazFollower 014C05, 100 == 1` (intro done)
- `IsScenePlaying BPUFXelzazDawnguardSnowElfFightScene 272932 == 0`
- Remi falling-out: `BPUFXelzazRemielFallingOut 5E67BB` stage 11 = one-week sulk timer, 12 = can make up, 13 = made up. Block Remi+Xelzaz talks when `GetStageDone 11 == 1 AND GetStageDone 13 == 0`.
- Long wait: `BPUFXelzazWaitingQuest 6A1FC7` stage 12 = he left the party after 3+ days waiting.

### 4b. Personal quests and "beat in progress" (all Start-Enabled unless noted; :BPUFXelzazFollower.esp)
| Quest | FormID | Beat in progress |
|---|---|---|
| Intro BPUFXelzazIntro / BPUFXelzazFollower | 07F1C3 / 014C05 | BPUFXelzazFollower GetStage < 100 (Riften / Bee and Barb intro) |
| An Unwanted Scion BPUFXelzazTheSleepingTree | 79F4DA | GetStageDone 20 == 1 AND GetQuestCompleted == 0 AND GetStageDone 80 == 0 (ends 54/57/60/66) |
| A Lawman's Ambition BPUFXelzazEscortQuest | 1BE431 | GetStage >= 20 AND GetStage < 50 (Hammerfell gate). Stage 10 is the long "get to know him" state, do not block it. Leaving endings: 60, 65, 444, 555, 666, 777. |
| Quid Pro Quo BPUFXelzazArmorQuest (RunOnce) | 40D29D | GetQuestRunning == 1 |
| Lost and Found BPUFXelzazLostHistLeaf (RunOnce) | E408E2 | GetQuestRunning == 1 |
| What is in a Name? BPUFXelzazKhashNameQuest (RunOnce) | 497E93 | GetQuestRunning == 1 |
| Beast of Burden BPUFXelzazGuarQuest | 7A4615 | GetStage >= 13 AND GetStage < 17 |
| Of Crimson BPUFXelzazCrimsonNirnroot | C6E975 | GetStage >= 12 AND GetStage < 23 (14 = he is off in Blackreach alone) |
| When Friends Fly (with Remi + Redcap, RunOnce) | 481CF6 | GetQuestRunning == 1 |
| Daedric commentary quests DA01-DA16 | e.g. Molag Bal 0B6D35 | not personal; leave to IsInScene |

### 4c. Following / waiting [CONFIRMED]
- Following: `GetInFaction CFF == 1` on 0893E1 (CFF comes from his follower alias; `SetFollower` does not add it in script) AND `GetActorValue WaitingForPlayer == 0`.
- Recruited global: `BPUFXelzazRecruited 00FB04 == 1`.
- His banter also uses `GetDistance Player < 500` on the listener.

### 4d. "Done" gate
- Intro done: `GetStageDone BPUFXelzazFollower 014C05, 100 == 1` ("Xelzaz gives the player Telvanni Bug Musk"). [CONFIRMED]

### 4e. Soft dependency
`Game.GetFormFromFile(0x0893E1, "BPUFXelzazFollower.esp")` → Xelzaz placed ref (base 00AA00).

---

## 5. INIGO (Inigo.esp)

### 5a. Gates his own content uses
- Banter from other mods waits for `GetQuestCompleted InigoBadVibrations 0695C5 == 1` and excludes Riften Jail (`GetInCurrentLoc RiftenJailLocation 0A8C86 == 0`).
- No dedicated "shut up" global found in Inigo.esp. [UNCONFIRMED that none exists in Inigo's MCM]

### 5b. Personal quest
**Bad Vibrations InigoBadVibrations 0695C5:Inigo.esp** (flags 17 = Start-Enabled, so GetQuestRunning is useless). [CONFIRMED from fragments]
- Stages 10/30/50/80 start the vision **scenes** InigoBV1 069B34, InigoBV2 069B41, InigoBV3 069B50, InigoBV4 06B0F0 (stage 100 starts InigoBV5 06B65C; stage 170 starts InigoBVEnd 071E70). `IsInScene == 0` on Inigo covers the seizures themselves.
- Investigation in progress (Snowpoint Beacon, Langley, eggs, Summon spell): `GetStage InigoBadVibrations >= 70 AND GetQuestCompleted InigoBadVibrations == 0` (completes at 230 or 250).
- Broader "visions have started": `GetStageDone 0695C5, 10 == 1 AND GetQuestCompleted == 0`.

### 5c. Following / waiting [CONFIRMED from InigoFollowerDialogue + InigoStatusQuestScript]
- **Following: `IsPlayerTeammate == 1` AND `GetActorValue WaitingForPlayer == 0` on InigoREF 008AE9.**
- WaitingForPlayer values: 0 follow, 1 wait, 2 relax, -1 dismissed (back to his Riften cell).
- **Do not use CFF**: InigoStatus OnInit removes him from CFF on every load. (The character sheet and the Auri patch say CFF; that is wrong for this version.) `GetStage InigofollowerDialogue 0012DF == 30` is what the Auri patch uses, meaning not confirmed. [UNCONFIRMED]
- Possible exception: if the Authoria Requiem follower bridge (`_Authoria_REQ_MajorFollowerBridge`) adds CFF at runtime. Not checked. [UNCONFIRMED]

### 5d. "Done" gate
- Bad Vibrations done: `GetQuestCompleted InigoBadVibrations 0695C5 == 1`. [CONFIRMED: stages 230 and 250 both carry CompleteQuest]

### 5e. Soft dependency
`Game.GetFormFromFile(0x008AE9, "Inigo.esp")` → InigoREF (base Inigounique 000D62).

---

## 6. LUCIEN (Lucien.esp)

### 6a. Gates his own content uses
- Hired: `GetStage JRLucienIntro 005903 >= 30`.
- Paarthurnax fallout: `GetInFaction JRLucienBetrayedFaction 277B82 == 0`. `JRLucienPaarthurnax 1171E9` stage 10 = he left, 15 = rejoined; block when `GetStageDone 10 == 1 AND GetStageDone 15 == 0`.

### 6b. Personal quests and "beat in progress" (both Start-Enabled; :Lucien.esp)
| Quest | FormID | Beat in progress |
|---|---|---|
| The Oblivion Engine JRLucienPersonal1 | 2B13ED | GetStage >= 35 AND GetStageDone 800 == 0 (inside Dumzbthar). Stage 30 = letter received, "visit at your convenience", can sit for a long time, so start the block at 35. |
| Intruders JRLucienGetHorseQuest | 62424C | GetStage >= 10 AND GetStage < 200 (sphere alarm, Daedra, Dumzbthar reveal, Clive). Its confrontation topics run while stage is 60-209. |

### 6c. Following / waiting [CONFIRMED from LucienController]
- Following: `GetInFaction CFF == 1` (alias faction on JRLucienFollower 00591E alias 0) AND `GetActorValue WaitingForPlayer == 0` on 00591F.
- Recruited global: `JRLucienRecruited 4A2D8B == 1`.

### 6d. "Done" gates
| Talk needs | Condition |
|---|---|
| Oblivion Engine done | `GetStageDone JRLucienPersonal1 2B13ED, 800 == 1` (CompleteQuest; stages 900-1000 exist after it, so do not test `GetStage == 800`). `GetQuestCompleted 2B13ED == 1` also works. |
| Admitted rebuilding the machine | `GetStageDone JRLucienGetHorseQuest 62424C, 40 == 1` (journal: "Dumzbthar, who Lucien has reactivated") [INFERRED]. Whole arc settled: `GetStageDone 62424C, 200 == 1` (Clive joins). `JRLucienHadConfrontation 65BEBE == 1` only marks that the player chose to confront him (the confrontation topics need it == 0 and stage 60-209), so it is optional, not a "he admitted it" flag. |

### 6e. Soft dependency
`Game.GetFormFromFile(0x00591F, "Lucien.esp")` → Lucien placed ref (base JRLucien 005900). Clive ref 60FE04.

---

## 7. REDCAP (FA01RedcapFollower.esp)

### 7a. Gates his own content uses
- Intro done: `GetStage FA01RedcapIntroductionQ 04C796 == 10`; Anise quest done: `GetQuestCompleted FA01RedcapAniseQ 0DFB5A == 1`.
- `FA01ContentLocked 60ED92` gates his question menu and college lines [meaning UNCONFIRMED].
- Drunk: `GetStage FA01RedcapDrunkQ 056A7D == 10`. Relaxing: `FA01RedcapRelax 581093 == 1`.

### 7b. Personal quests and "beat in progress" (RunOnce, not Start-Enabled, so GetQuestRunning works; :FA01RedcapFollower.esp)
| Quest | FormID | Beat in progress |
|---|---|---|
| The Cabin in the Woods FA01RedcapAniseQ | 0DFB5A | GetQuestRunning == 1 (pre-recruit) |
| Back to the Rock FA01RedcapSolstheimStartQ | 0D0784 | GetStage >= 10 AND < 20 (low risk) |
| The Village FA01RedcapSolstheimVillageQ | 0D079B | GetStage >= 20 AND GetQuestRunning == 1 |
| The Hands of Fate FA01RedcapSolstheimManosQ | 0D58E3 | GetQuestRunning == 1 |
| The Red God FA01RedcapRedGodQ | 135DED | Sanguine on stage: GetStage 10-20, 50-60, 90 (5/30/40/70/80 are "go drink later" waits). Simple version: GetQuestRunning == 1 AND GetStage >= 10. |
| Bloodmoon Rising FA01RedcapWereboarQ | 18C066 | GetQuestRunning == 1 |
| Wereboar Art Thou FA01RedcapSkaalQ | 1D2F75 | GetQuestRunning == 1 |
| King of All Rieklings FA01RedcapMQParty | 065E29 | GetQuestRunning == 1 |
| You Can Be a Bigpig, Too FA01BigpigIntroQ | 0D58D2 | GetQuestRunning == 1 (low risk) |

### 7c. Following / waiting [CONFIRMED from FA01RedcapController]
- Following: `GetInFaction CFF == 1` (alias faction on FA01RedcapFollowerQ 00FB03 alias 0) AND `GetActorValue WaitingForPlayer == 0` on 019D16. His own banter adds `GetIsID 005900` on the speaker.
- Recruited global: `FA01RedcapRecruited 00AA02 == 1`.

### 7d. "Done" gates
| Talk needs | Condition |
|---|---|
| Tribe freed / Manos dead | `GetStageDone FA01RedcapSolstheimManosQ 0D58E3, 40 == 1` (Manos killed); tribe freed `GetStageDone 0D58E3, 70 == 1`. |
| Chose to stay with the player | `GetQuestCompleted FA01RedcapSolstheimManosQ 0D58E3 == 1` (stage 100, the only ending; journal: he returns to the village only when dismissed) [INFERRED: no separate "stay" flag exists]. |
| Red God (Sanguine) done | `GetQuestCompleted FA01RedcapRedGodQ 135DED == 1` (stage 100, Redcap's Rose). `FA01RedcapMetSanguine 130CE0` marks first meeting. |
| Werepig quest done | `GetQuestCompleted FA01RedcapWereboarQ 18C066 == 1` (Bloodmoon Rising, stage 130, Ring of the Wereboar). Follow-up Skaal quest: `GetQuestCompleted FA01RedcapSkaalQ 1D2F75 == 1`. |
| Thirsk chief | `GetGlobalValue FA01RedcapThirskChief 0DFC37 == 1` (his "Redcap. Chief!" idles gate on it; set by INFO 04C781 "Friend! Redcap chief!" [INFERRED setter]). |

### 7e. Soft dependency
`Game.GetFormFromFile(0x019D16, "FA01RedcapFollower.esp")` → Redcap placed ref (base 005900). Riding variant base 4E922F.

---

## 8. Not confirmed / open
- Val: which script sets `AX_ValCollegeGraduated`; FormIDs of `AX_TarekAlive/AX_TarekDead` not pulled.
- Inigo: meaning of InigofollowerDialogue stages; whether any runtime layer re-adds CFF.
- Redcap: meaning of `FA01ContentLocked`; the Thirsk chief setter (inferred from the INFO that references the global).
- Lucien: "admitted rebuilding" mapped to GetHorseQuest stage 40 from journal text only.
- Gore: HD1GoreDawnguard 7FADBA stage meanings; Romance tier 4 global (6EA61D) unused.
- Remi: craft-project quest stage windows taken from journal text, fragments not decompiled.
