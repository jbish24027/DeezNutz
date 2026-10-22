# 34 COMPANIONS - trigger rows (prefix CP, 70 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\34 COMPANIONS.txt`.
Sources: `research\triggers\vanilla_gates.md` (B1, B3), `research\triggers\kaidan_block.md` (§1 KaiComp, §2a, §2b, §4), `triggers\20 DAWNGUARD.md` §1 + §3 (Serana/Ashe Free rows and S_/A_ gate codes), `research\bibles\*.md`.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).

## 1. Companions silence (already in WorldQuiet; repeated here so nothing in this file fights it)

From vanilla_gates.md B3 + kaidan_block.md §2a/§2b. No CP talk (and no other banter) while:
- C03 (01CEF4:Skyrim.esm) stage 15..24 (Underforge blood ritual). [CONFIRMED]
- C02 (06E804) stage 10..199 (induction ceremony). [CONFIRMED stages / UNC span]
- C04 (01CEF5) stage 20 **and** player in Glenmoril Coven location (no scripted scene; suppress all CP talks there). [UNC loc FormID]
- C06 (01CEF6) stage 10 (Kodlak's funeral) and stage 30..199 (Ysgramor's Tomb ritual). [CONFIRMED]
- Player `GetRace == WerewolfBeastRace (0CDD84:Skyrim.esm)` (in beast form; talks wait until she changes back). [UNC FormID]
- Kaidan's Companions climax scenes (kaidan_block.md §2b item 8): IsScenePlaying ShowdownPart1 1D3389:IF, ShowdownPart2 1DD5BC:IF, ShowdownKill 1E26EE:IF, ShowdownNoKill 1E26EF:IF, ZZKaiCompCeremony 1EC940:IF, each == 0. Applies to every CP talk, with or without Kaidan.
- Never in the Underforge cell `0165A6:Skyrim.esm` (IF blocks frathouse banter there too).

## 2. Kaidan's KaiComp "Vengeance and Honor" blocks (162E4A:Kaidan - Immersive Features.esp)

KaiComp is Kaidan's own Companions trial (asked at 10 with a 48 h timer, second talk at 20, active 30..145, 85 starts KaiSTFUQuest, 150 complete, 200 Stop). Our file never retells or anticipates it.

**A. On every CP talk with K (Kaidan) in it** (kaidan_block.md §2a row 33, one OR group):
| # | Function | Parameter | Op | Value | Flag |
|---|---|---|---|---|---|
| 33-1 | GetQuestRunning | KaiComp 162E4A:IF | == | 0 | OR |
| 33-2 | GetStage | KaiComp 162E4A:IF | < | 30 | OR |
| 33-3 | GetStage | KaiComp 162E4A:IF | >= | 150 | — |
Plus `GetQuestRunning KaiSTFUQuest (F532A2:IF) == 0` (row 23) and `STFUVarNPCGeneral (F49096:IF) == 0` (row 15), which KaiComp 85 raises.

**B. Extra for this file (not in TRIGGERS.md): keep CP talks off KaiComp's lead-in.** While `GetStage KaiComp >= 10 AND < 30` (he has asked, the 48 h timer / second talk is pending), block CP talks that put K and P together (CP5, CP16, CP33, CP50, CP51, CP58) so they can't land between his two KaiComp talks. [UNC: whether stage 10..29 has a forcegreet window]

**C. Location blocks while KaiComp is active** (kaidan_block.md §4): no CP talk in `VargrDenLocation 2101CD:IF` / cell `VargrDen 15DBD8:IF` (KaiComp 85..120), and no CP talk in `GetInCurrentLoc Jorrvaskr (01F877:Skyrim.esm)` while KaiComp stage is 140..149 (ceremony leg). [UNC exact ceremony stage]

**D. After it:** `KCOMP_DONE` = `GetStageDone KaiComp 150 == 1`. Only CP57 and CP58 use it, and they speak in general terms only (no names, places or events from his trial).

Note: Kaidan's own banter quests (KaiandInigo etc.) pause while C05/C06 run. Our K talks don't copy that; CP45 (after Kodlak dies, C05 running) is allowed because nothing of Kaidan's is scripted then. Revisit if a KaiComp beat is found to start during C05. [UNC]

## 3. Gate codes used in this file (new)

Companions story (all Skyrim.esm):
- `C_JOIN` (existing) = C00 (04B2D9) stage 100 done.
- `C_PROVEN` = C01 (06E803) stage 200 done (Dustman's Cairn finished; Farkas seen in wolf form). [CONFIRMED per vanilla_gates B1 "full member"]
- `C_INDUCT` = C02 (06E804) completed (induction ceremony over). **[UNC: completion stage; use GetQuestCompleted]**
- `WOLF` (existing) = C03 (01CEF4) stage 25 done.
- `LUNA_WOLF` = `PlayerIsWerewolf (0ED06C:Skyrim.esm) == 1` (she still has the beast blood now).
- `C_SKJOR` = C03 completed (Skjor found dead at Gallows Rock). **[UNC: 200]**
- `C_GLEN` = C04 (01CEF5) stage 20 done and C04 not completed (sent to Glenmoril).
- `LEAVE_GLEN` = event: player leaves the Glenmoril Coven location while C04 is running and stage >= 20, and has at least one Glenmoril Witch Head in inventory. **[UNC: location FormID, head MISC FormID, heads-collected stage]**
- `KODLAK_DEAD` = C04 completed (Jorrvaskr attack; Kodlak dead). **[UNC: or C05 (06E805) stage >= 1]**
- `PRE_FUNERAL` = KODLAK_DEAD and C06 stage 10 not done.
- `C_REVENGE` = C05 (06E805) completed (Driftshade; Wuuthrad fragments). **[UNC: 200]**
- `POST_FUNERAL` = C06 stage 10 done, C06 GetStage >= 20 and < 30 (after the pyre, before the tomb ritual). **[UNC: first stage after 10]**
- `LOC:Tomb` = event: arrival in Ysgramor's Tomb exterior location while C06 running and GetStage < 30. **[UNC: location FormID]**
- `HARBINGER` (vanilla_gates B1) = C06 completed.
- `LOC:Jorrvaskr` = `GetInCurrentLoc 01F877:Skyrim.esm` (kaidan_block §4). Never the Underforge cell.
- `LOC:Skyforge` = Whiterun, player within 1500 units of the Skyforge (Eorlund's forge, in WhiterunWorld). **[UNC: forge ref FormID]**
- `BEAST_BACK` = event: player race goes from WerewolfBeastRace (0CDD84) back to her own race (poll on the 60 s tick, or OnRaceSwitchComplete if available). `BEAST_BACK_FIRST` = first time ever. **[UNC FormID]**
- `CURED` = event: PlayerIsWerewolf goes 1 -> 0, **and** HARBINGER, **and** player `HasKeyword Vampire (0A82BB) == 0` (so a Vampire Lord gift, which also removes lycanthropy, never fires the "flame" talks). Controller remembers the last value.
- `FARKAS_CURE` = the vanilla "Purity" quest offered by Farkas has started (Farkas has asked for the cure). **[UNC: EditorID/FormID; if not found, fall back to HARBINGER only]**

Companions jobs (vanilla radiant CR quests, Skyrim.esm). **[UNC: all CR EditorIDs/FormIDs not traced; look up at build]**
- `CR_BRAWL` = event: "Hired Muscle" brawl job's target yields (CR quest stage done after the brawl).
- `CR_ANIMAL` = AFTERFIGHT while an "Animal Extermination" CR job is running and the last target was an animal.
- `CR_HEIRLOOM` = AFTERFIGHT:draugr while a "Family Heirloom" CR job is running.
- `CR_RESCUE` = event: a "Rescue Mission" CR job completes.
- `TOTEMS` = Aela's "Totems of Hircine" quest running.

Others (from earlier files):
- `SERANA`, `SER_VAMP`, `S_KISS` (S_ROM_ON and SDA_SeranaRomance04 yes-branch done), `DG_HARKON` = 20 DAWNGUARD.md §3.
- `ASHE_REVEAL`, `ASHE_Q1`, `A_CRUSH`, `A_LOVE`, `A_ANY` = 20 DAWNGUARD.md §3.
- `ASHE_AMENDS` = MM_AMQ_06a "Shattered Orphans" (C07BE9:Ashe - Fire and Blood.esp) completed (ashe.md §6).
- `K_CRUSH`, `K_TOG+`, `K_ANY`, `G_ANY` (= G_FLIRT or G_TOG+), `V_ANY` (= V_FLIRT or V_TOG+), `LUC_ADMIT` = TRIGGERS.md §4 / 20 DAWNGUARD.md.
- `after:Q16` = Redcap and Remi's "Lady-pup" talk (Quests file) has played.
- `CAMP`, `NIGHT`, `MORNING`, `AFTERFIGHT:<enemy>` = TRIGGERS.md §4. `AFTERFIGHT:silverhand` = last combat target in SilverHandFaction **[UNC FormID]**.

## 4. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| CP1 | G P | E LOC:Jorrvaskr (first entry) | — |
| CP2 | G V | T | C_JOIN |
| CP3 | X I | E LOC:Jorrvaskr | C_JOIN |
| CP4 | C R | E LOC:Jorrvaskr + MORNING | C_JOIN |
| CP5 | K P | T | C_JOIN; K_CRUSH; §2B |
| CP6 | V A | T or E LOC:Jorrvaskr | C_JOIN; ASHE_REVEAL |
| CP7 | L I | E LOC:Jorrvaskr | C_JOIN |
| CP8 | S P | E LOC:Jorrvaskr | C_JOIN; S following |
| CP9 | G K | T | C_JOIN |
| CP10 | R X | E LOC:Skyforge | C_JOIN |
| CP11 | C I | T | C_JOIN; not C_PROVEN |
| CP12 | R K | T | C_JOIN |
| CP13 | L G | E LOC:Jorrvaskr | C_JOIN; after L2 (Batch 2 "Reading practice") |
| CP14 | V P | T | C_JOIN |
| CP15 | L P | T | C_JOIN; not KODLAK_DEAD |
| CP16 | K G P | T | C_JOIN; §2B |
| CP17 | I K | T | C_PROVEN |
| CP18 | V A | T | C_PROVEN |
| CP19 | L R P | T | C_INDUCT |
| CP20 | G K | T | C_SKJOR |
| CP21 | C I | E AFTERFIGHT:silverhand | C_PROVEN |
| CP22 | S X | E AFTERFIGHT:silverhand | C_PROVEN; S following; SER_VAMP |
| CP23 | V R P | T | C_PROVEN; not WOLF |
| CP24 | I K | E first tick after WOLF set | WOLF |
| CP25 | R X | T | WOLF; LUNA_WOLF; after:Q16 |
| CP26 | S P | T | WOLF; LUNA_WOLF; S following; SER_VAMP |
| CP27 | G P | E BEAST_BACK_FIRST (priority 1) | WOLF |
| CP28 | C P | T | WOLF; after:Q16 |
| CP29 | L G | T | WOLF; LUNA_WOLF |
| CP30 | A P | T | WOLF; LUNA_WOLF; ASHE_REVEAL |
| CP31 | A K | T | WOLF; LUNA_WOLF; ASHE_AMENDS |
| CP32 | S K | T | WOLF; LUNA_WOLF; SER_VAMP; S_KISS; K_TOG+; never while an SDA romance quest runs |
| CP33 | K P | E BEAST_BACK (any time) | K_TOG+; LUNA_WOLF; §2B |
| CP34 | G K | E BEAST_BACK (any time) or T after it | K_CRUSH; not G_ANY; after CP27 |
| CP35 | G K | T | LUNA_WOLF; K_ANY; G_ANY; after a BEAST_BACK |
| CP36 | V R | E BEAST_BACK (any time) | LUNA_WOLF; after CP27 |
| CP37 | L P | T | WOLF; LUNA_WOLF |
| CP38 | I C | T | WOLF; LUNA_WOLF |
| CP39 | K I | E CAMP+NIGHT | LUNA_WOLF |
| CP40 | G S | T | LUNA_WOLF; S following; SER_VAMP |
| CP41 | V A | E BEAST_BACK (any time) | LUNA_WOLF; V_ANY; A_ANY; ASHE_REVEAL; after CP27 |
| CP42 | C G | T | C_GLEN; not in Glenmoril location |
| CP43 | X P | E LEAVE_GLEN (priority 1) | C_GLEN |
| CP44 | C R | T | after CP43; C04 still running |
| CP45 | G K | T | PRE_FUNERAL |
| CP46 | V L | T | KODLAK_DEAD |
| CP47 | I P | T | POST_FUNERAL |
| CP48 | A G | T | KODLAK_DEAD; not HARBINGER; ASHE_Q1 |
| CP49 | L R P | T | C_REVENGE |
| CP50 | P K | E LOC:Tomb | C06 running, stage < 30; §2B |
| CP51 | K P | T (first tick after) | HARBINGER; §2B |
| CP52 | G V | T | HARBINGER |
| CP53 | L P | T | HARBINGER |
| CP54 | C I | T | HARBINGER; after:Q16 |
| CP55 | S P | E LOC:Jorrvaskr + NIGHT | HARBINGER; S following; DG_HARKON |
| CP56 | X R | T | HARBINGER; Remi/Xelzaz not fallen out |
| CP57 | I G | T | KCOMP_DONE (K Free not needed; K not a speaker) |
| CP58 | K P | T | KCOMP_DONE; after CP5; §2B |
| CP59 | I P | E CURED (priority 1) | CURED |
| CP60 | L G | T | CURED; LUC_ADMIT; after CP29 |
| CP61 | G K | T | CURED; after CP27 |
| CP62 | S P | T | CURED; S following; SER_VAMP |
| CP63 | V G | E CR_BRAWL | C_JOIN |
| CP64 | R K | E CR_ANIMAL | C_JOIN |
| CP65 | L X | E CR_HEIRLOOM | C_JOIN |
| CP66 | A I | E CR_RESCUE | C_JOIN; ASHE_REVEAL |
| CP67 | L P | T (while TOTEMS) | TOTEMS; LUNA_WOLF |
| CP68 | K R | T | HARBINGER; FARKAS_CURE [UNC] |
| CP69 | A K | E LOC:Jorrvaskr | C_JOIN; ASHE_REVEAL; after CP6 |
| CP70 | C P | E LOC:Jorrvaskr + NIGHT (hour 23..4) | HARBINGER |

## 5. Notes for the build
- Same-event priority: on BEAST_BACK_FIRST only CP27 fires; CP33/CP34/CP36/CP41 wait for a later change-back. On LEAVE_GLEN only CP43 fires; CP44 follows as a timer talk. On CURED only CP59 fires; CP60-CP62 are timer talks.
- CP34 and CP35 can't both qualify for the same romance state (CP34 needs not G_ANY; CP35 needs G_ANY).
- Rival talks (CP32, CP35, CP41): Luna has no line in any of them.
- CP11 must play before C_PROVEN or never (it's the "nobody knows yet" smell talk).
- CP23 must play before WOLF or never.
- Existing coverage avoided: Q15 (Kaidan introduces Jorrvaskr; "best mate / grumpy git" not reused), Q16 ("Lady-pup" and blood samples are only called back), SDA's Jorrvaskr lines ("overturned boat", "reeks of dogs"), the Ashe/Serana patch's Jorrvaskr line ("sweat and fur"), Kaidan IF's travelling-frathouse topics with Farkas/Vilkas (cards, spiders, sweet-roll theft, sparring footwork, limericks, Farkas's crush, ca-caw signals), and everything in KaiComp (the scholar, the book, the hammer, the den, the trial itself).
- No "Dragonborn" anywhere in the file. No Kaidan cult references.
- Every CP talk with Luna lines (P) stays branch-neutral: she never chooses for the Circle, the cure, or a romance.
