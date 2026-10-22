# 20 DAWNGUARD - trigger rows (prefix DG, 120 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\20 DAWNGUARD.txt`.
Sources: `research\content\dlc_cc_missives_3dnpc.md` section A (quest stages), `research\triggers\vanilla_gates.md` (B1, B3), `research\bibles\serana.md` section 3 + 6, `research\bibles\ashe.md` section 3 + 6.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, **S Serana, A Ashe**, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).

## 1. New Free() rows

| Who | Following test | Busy blocks |
|---|---|---|
| Serana | `GetVMQuestVariable DLC1NPCMentalModel(002B6E:Dawnguard.esm) ::IsFollowing_var == 1` and `::CanFollow_var == 1` (serana.md 6; do not use CurrentFollowerFaction) | `IsInScene == 0`; `SDA_PlayerInDialogue (9EB814:SeranaDialogAddon.esp) == 0`; not running: SDA_SeranaRomance01..13, SDA_DrinkingBuddies (61AB00), SDA_DrinkingBuddiesWaiting, SDA_SleepingQuest (D29EB8), SDA_SeranaRideHorse; not during the cure absence (`SDA_CureQuestTimer` 5EE3E9 running) |
| Ashe | `GetVMQuestVariable MM_AsheMentalModel(06FE28:Ashe - Fire and Blood.esp) ::IsFollowing_var == 1`, `::IsWaiting == 0`, `::bConfigVarIdles == 1` | `MM_PlayerinDialogue (5435E9) == 0`, `MM_FlashbackRunning (4643DC) == 0`, `MM_ScriptedCombatScenePlaying (BF887E) == 0`, `MM_AsheranaSleepBanterPlaying (52B269) == 0`, `MM_AsheSeranaLoveBanterBlock (628708) == 0`; ashe.md 6 quest blocks (AMQ_04 45-80, AMQ_05, AMQ_07, Epilogue running) |

Serana alias: fill from `GetFormFromFile(0x002B74, "Dawnguard.esm")` (DLC1SeranaRef); never the SDA helper copies 217CCD/217CCE. VoiceType `DLC1SeranaVoice` 002B6F. Ashe: `GetFormFromFile(0x2D4A35, "Ashe - Fire and Blood.esp")`, VoiceType `MM_AsheVoice` 00AA01.

## 2. Dawnguard silence (add to WorldQuiet)

From dlc research A3 + vanilla_gates B3. No DG talk (and no other banter) while:
- DLC1VQ02 (002F65) stage 8..19 (Harkon's offer). [CONFIRMED]
- DLC1VQ03Hunter (0098CB) or DLC1VQ03Vampire (004C3D) stage 100..130 (Dexion's reading).
- DLC1VQ04 (00284F) stage 90..100 (portal / soul-trap choice).
- DLC1VQ05 (002850) running, or player in worldspace DLC01SoulCairn (001408) or Boneyard (00528D). [CONFIRMED FormID]
- DLC1VQ06 (002852) stage 50..60, or in DLC1AncestorsGladeWorld (0048C7) during those stages.
- DLC1VQ07 (002853) stage 110 done and 200 not done (Inner Sanctum, Vyrthur).
- DLC1VQ08 (007C25) running (final battle). [CONFIRMED FormID]
- any DLC1EclipseAttack1-6 (01629F...01764C) running; their AFTERFIGHT waits until the quest stops.
- player `GetRace == DLC1VampireBeastRace (00283A)` (Vampire Lord form).

## 3. Gate codes used in this file (new)

Story (all Dawnguard.esm):
- `DG_FREED` = DLC1VQ01 (00352A) stage 40 done (research A2 "40 Serana freed"). **[UNC: vanilla_gates B1 says 20; use 40, fall back to 20]**
- `SERANA` (existing) = DLC1VQ02 5 done.
- `DG_HARKON` = DLC1VQ02 20 done (met Harkon; after the 8..19 silence).
- `DG_VAMP` = DLC1VQ02 180 done (accepted the gift). Alt: 40. `DG_HUNT` = DLC1VQ02 190 done (refused). Alt: 25/30.
- `DG_NEWORDER` = DLC1HunterBaseIntro (004E24) completed (Sorine + Gunmar recruited). **[UNC: Gunmar/Sorine individual stages not traced; 70 may be enough]**
- `DG_SERFORT` = DLC1VQ03Hunter 10 done (Serana arrives at Fort Dawnguard; research says 7/10).
- `DG_CHALICE` = DLC1VampireBaseIntro (00594C) completed.
- `DG_MOTHHUNT` = DLC1VQ03Hunter 45 done or DLC1VQ03Vampire 10 done, and Prophet not completed (hunting Dexion). **[UNC: Vampire-side stage for "hunting" not traced]**
- `DG_THRALLBROKEN` = DLC1VQ03Hunter 70 done (hunter side only).
- `DG_SCROLL_CARRIED` = DG_FREED and DLC1VQ03Hunter/Vampire 100 not done (Serana still has her scroll).
- `DG_PROPHET` = DLC1VQ03Hunter 200 or DLC1VQ03Vampire 200 (plan to blot out the sun is known).
- `DG_BLIND` = DLC1VQElder (005DA9) completed (Dexion blind).
- `DG_GARDEN` = DLC1VQ04 stage 50 done (courtyard garden). **[UNC: research gives 35/50/60 for courtyard/lab without saying which; 50 picked]**
- `DG_CAIRN` = DLC1VQ05 completed (200). `DG_VALERICA` = DLC1VQ05 30 done.
- `DG_CAIRN_BACK` = event: first controller tick with DG_CAIRN and player outside both Soul Cairn worldspaces. Only ONE talk fires on it (pick from the E rows marked so); the rest of Part 5 are T rows gated `DG_CAIRN`.
- `DG_TRAPPED` = player was **not** a vampire when DLC1VQ05 stage 10 was set (so Serana soul-trapped her). Needs the controller to snapshot `PlayerIsVampire` (Skyrim.esm global, **[UNC FormID]**) or player `HasKeyword Vampire (0A82BB)` when VQ05 10 fires.
- `DG_JIUB` = DLC1VQSaint (01400B) stage 20 done.
- `DG_DURN` = DLC1VQDragon (00C73A) stage 30 done. `DG_SOULTEAR` = DLC1VQDragon 60 done.
- `DG_GLADE` = DLC1VQ06 completed (200).
- `DG_GELEBOR` = DLC1VQ07 50 done. `DG_BOW` = DLC1VQ07 completed (200).
- `DG_END` = DLC1VQ08 completed (200) (Harkon dead, both sides).
- `DG_FLORENTIUS` = DLC1HunterBaseStage2 (013F1F) completed.
- `DG_FORGE` = DLC1LD (005817) stage 150 done (shards collected). **[UNC: research gives 130/150 for shards]**
- `RV06_RUN` = `GetQuestRunning DLC1RV06` ("The Gift"). **[UNC FormID; inside 004C1B...019938 range]**
- `VAL_FATHER` (existing) = Val003 completed.

Vampire state:
- `SER_VAMP` = Serana `HasKeyword Vampire (0A82BB:Skyrim.esm) == 1`. `SER_CURED` = `== 0` and `SDA_CureQuestTimer` not running.
- `LUNA_VAMP` = player HasKeyword Vampire == 1. `LUNA_CURED` = event: player goes from Vampire keyword 1 to 0 (controller remembers last value).
- `VL_BACK` = event: player race changes from DLC1VampireBeastRace (00283A) back to her normal race (controller polls GetRace on its 60 s tick and on OnRaceSwitchComplete if SKSE event available). First time only.

Romance (rivals):
- `S_ROM_ON` = `SDA_SeranaRomance (A2D563:SeranaDialogAddon.esp) == 1`. `S_ROMOFF` = `== 0`.
- `S_COMP` = S_ROM_ON and SDA_SeranaRomance03 (A3777F) completed ("travelling companion"). **[UNC: completion stage]**
- `S_KISS` = S_ROM_ON and SDA_SeranaRomance04 (A929B9) yes-branch stage done (serana.md example uses `>= 20`). **[UNC stage]**
- `S_LOVE` = S_ROM_ON and SDA_SeranaRomance09 (B2A842) completed ("I love you").
- `NOT_S_KISS` = not S_KISS (S_ROMOFF or romance below the kiss).
- `A_CRUSH` = `MM_RM (2F3039:Ashe - Fire and Blood.esp) >= 4` and `MM_AsheRomance (A5E1EF) == 0`. `A_LOVE` = `MM_AsheRomance == 1`. `A_ANY` = A_CRUSH or A_LOVE.
- `ASHE_REVEAL` = MM_FriendshipQuest (1A9DEE) stage 70 done (or var MM_AutomatonReveal == 1). `ASHE_Q1` = MM_AMQ_01 (756FEA) completed. `ASHE_LOGS` = MM_AMQ_05 (056A66) completed.
- `G_ANY` = G_FLIRT or G_TOG+. `V_ANY` = V_FLIRT or V_TOG+. K/G/V codes as TRIGGERS.md section 4.

Places (`E LOC:<name>` = arrival, first time unless noted; location FormIDs Dawnguard.esm, research A4):
- `LOC:Fort` Fort Dawnguard 0128FE (interior) / Dayspring Canyon 004C1F. `LOC:Volkihar` Castle Volkihar 004C20 / Volkihar Keep 00357D (courtyard WRLD 007202). `LOC:Jetty` Icewater Jetty 012409 (+ player in a boat / heading out; **[UNC]** use arrival at the jetty while VQ02 5..7). `LOC:Redwater` 004D6F. `LOC:Glade` 003583 (outside the VQ06 50..60 silence). `LOC:Darkfall` 00A87A / 0162AC. `LOC:Vale` 00A87C (first entry). `LOC:Wayshrine` = in Vale and within 600 units of a Chantry wayshrine activator **[UNC base IDs]**.

Fights (`E AFTERFIGHT:<type>`, enemy by last combat target):
- `deathhound` race DLC1DeathHoundRace; `gargoyle` race DLC1GargoyleRace; `vampire` target HasKeyword Vampire or in VampireFaction; `thrall` target in DLC1VampireFaction-led thrall faction or `DLC1Thrall*` **[UNC: all race/faction FormIDs to look up]**; `armoredtroll` base DLC1TrollArmored* **[UNC]**; `chaurushunter` race DLC1ChaurusHunterRace **[UNC]**; `dawnguard` target in DLC1HunterFaction (003375) / DLC1DawnguardFaction (014217); `falmer` FalmerRace while in LOC:Vale; `eclipse` = a DLC1EclipseAttack quest just stopped.
- `raisedcorpse` = Serana cast a reanimate spell during the fight (poll Serana `GetCommandedActors`/summon check) **[UNC: needs a script check]**.
- `aurielsbow` = player had DLC1AurielsBow equipped during the fight **[UNC FormID]**.

## 4. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| DG1 | G K | T | DG_FREED; SERANA running/following (S Free not needed, she is the subject); not DG_HARKON |
| DG2 | L S P | T | DG_FREED; S following |
| DG3 | K S | E exterior, IsPleasant, hour 9..17 | DG_FREED; S following; SER_VAMP |
| DG4 | V S P | E LOC:Jetty | SERANA; DLC1VQ02 < 8 (first trip out) [UNC jetty detection] |
| DG5 | G I | T | DG_HARKON (fires after the 8..19 silence) |
| DG6 | K S | T | SERANA; after DG3 |
| DG7 | V S P | T | SERANA |
| DG8 | C S | T | SERANA; after Q19 (Redcap's garlic talk) |
| DG9 | V K P | E LOC:Fort | first visit |
| DG10 | G C | E LOC:Fort | DG_HUNT; DG_NEWORDER |
| DG11 | R L P | E LOC:Fort | DG_HUNT; DG_NEWORDER |
| DG12 | S K | E LOC:Fort | DG_HUNT; DG_SERFORT |
| DG13 | S P | E LOC:Fort | DG_HUNT; DG_SERFORT |
| DG14 | G S | E LOC:Fort | DG_HUNT; DG_SERFORT; after DG1 |
| DG15 | I K | T | DG_FLORENTIUS |
| DG16 | C I | E LOC:Fort | DG_HUNT |
| DG17 | A G | E LOC:Fort | ASHE_Q1 |
| DG18 | V G | E LOC:Fort | DG_HUNT |
| DG19 | K P | E LOC:Fort | K_TOG+ |
| DG20 | S K | E LOC:Volkihar | DG_HARKON (fires on first arrival after the offer silence ends; if missed, next visit) |
| DG21 | G K | E LOC:Volkihar | DG_VAMP |
| DG22 | V P | E LOC:Volkihar | DG_VAMP |
| DG23 | S L | E LOC:Volkihar | DG_VAMP; S following |
| DG24 | I K | E LOC:Redwater | INIGO_BV not required; any visit (first) |
| DG25 | R P | T | DG_CHALICE |
| DG26 | S G | T or E LOC:Volkihar | DG_GARDEN; after DG14 or DG1 |
| DG27 | S V | T | DG_GARDEN; after DG4 |
| DG28 | X K P | T | DG_PROPHET |
| DG29 | L S P | T | DG_SCROLL_CARRIED; S following |
| DG30 | P L | T | DG_MOTHHUNT |
| DG31 | G I | T | DG_THRALLBROKEN (Dawnguard side only) |
| DG32 | R P | T | DG_BLIND |
| DG33 | X L P | T | DG_BLIND |
| DG34 | A L | T | DG_BLIND; ASHE_LOGS |
| DG35 | K S P | E DG_CAIRN_BACK | DG_TRAPPED (priority 1 on the event) |
| DG36 | I C P | E DG_CAIRN_BACK | DG_CAIRN (priority 2 on the event; else T) |
| DG37 | V G | T | DG_CAIRN |
| DG38 | K G P | T | DG_CAIRN |
| DG39 | X S | T | DG_CAIRN; SER_VAMP not required |
| DG40 | X K | T | after DG39 (at least 1 game day later) |
| DG41 | I S | T | DG_VALERICA (and DG_CAIRN) |
| DG42 | I S | T | DG_CAIRN; after DG41 |
| DG43 | S P | T | DG_CAIRN |
| DG44 | R S | T | DG_CAIRN |
| DG45 | P L | T | DG_JIUB and DG_CAIRN |
| DG46 | L C | T | DG_DURN |
| DG47 | G K | T | DG_DURN |
| DG48 | V S | T | DG_DURN |
| DG49 | X P | T | DG_SOULTEAR |
| DG50 | I G | E LOC:Glade | DG_BLIND; not in VQ06 50..60 |
| DG51 | L P | T | DG_GLADE |
| DG52 | K P | T | DG_GLADE |
| DG53 | V P | T | DG_GLADE; DLC1VQ07 10 not done (before reaching Darkfall) [UNC] |
| DG54 | R K | E LOC:Darkfall | DLC1VQ07 running |
| DG55 | I P | E LOC:Vale | first entry |
| DG56 | R L | E LOC:Vale | after DG55 or 2nd Vale tick |
| DG57 | X A | E LOC:Vale + SNOW | ASHE_REVEAL |
| DG58 | L S | T | DG_GELEBOR; S following |
| DG59 | S G | T | DG_GELEBOR; not DG_BOW |
| DG60 | V R P | E LOC:Wayshrine | in Vale [UNC wayshrine detection; fallback E LOC:Vale] |
| DG61 | I P | T | DG_BOW |
| DG62 | L X P | T | DG_BOW |
| DG63 | S K | T | DG_END |
| DG64 | V S I | T | DG_END; VAL_FATHER |
| DG65 | K G | E MORNING | DG_END; first morning after (GameDaysPassed snapshot at DLC1VQ08 200) |
| DG66 | S P | T | DG_END |
| DG67 | V K | T | DG_END; DG_HUNT |
| DG68 | C G | T | DG_END; DG_VAMP |
| DG69 | X S | T | DG_END |
| DG70 | C S | T | DG_END; after DG8 |
| DG71 | X S | E CAMP or INN | SERANA; SER_VAMP |
| DG72 | L S P | T | SERANA; SER_VAMP |
| DG73 | L S | T | after DG72 |
| DG74 | L S P | E CLEARNIGHT | after DG72; SER_VAMP |
| DG75 | S V | T | SERANA; after DG7 |
| DG76 | S R | T | SERANA |
| DG77 | G S | T | SERANA; after DG14 or DG1 |
| DG78 | K S | T | SERANA; SER_VAMP; after DG6 |
| DG79 | S C | E CLEARNIGHT | SERANA; after DG8 |
| DG80 | S X | T | after DG71 |
| DG81 | K S | T | SERANA; after DG6 |
| DG82 | R L P | T | DG_FORGE; DLC1LD not completed |
| DG83 | C G P | E VL_BACK | DG_VAMP (first transformation only) |
| DG84 | C P | T | LUNA_VAMP; after DG8 or Q19 |
| DG85 | I K | T | DG_VAMP; LUNA_VAMP |
| DG86 | X P | E CAMP or INN | LUNA_VAMP |
| DG87 | K P | T | RV06_RUN; K_MAR |
| DG88 | C K P | E LUNA_CURED | after DG84 |
| DG89 | X S | E CAMP or INN | SER_CURED; after DG71 |
| DG90 | A S | T | SER_CURED; ASHE_REVEAL |
| DG91 | K S | E NIGHT exterior | SER_CURED |
| DG92 | G S P | E MORNING exterior + IsPleasant | SER_CURED |
| DG93 | L S | T | SER_CURED; after DG72 |
| DG94 | S K P | T | K_CRUSH; NOT_S_KISS; SERANA |
| DG95 | S G | T | G_FLIRT; NOT_S_KISS; SERANA |
| DG96 | S V | T | V_FLIRT; NOT_S_KISS; SERANA |
| DG97 | S A | T | A_CRUSH; ASHE_REVEAL; NOT_S_KISS; SERANA |
| DG98 | S K | T | S_ROMOFF; K_CRUSH or K_TOG |
| DG99 | K S | T | S_COMP; not S_KISS; K_ANY |
| DG100 | G S | E CAMP | S_KISS; G_ANY |
| DG101 | S K | T | S_KISS; K_TOG+; not S_LOVE |
| DG102 | V S | T | S_KISS; V_ANY; not S_LOVE |
| DG103 | A S | T | S_KISS; A_ANY; ASHE_REVEAL; not S_LOVE |
| DG104 | V K P | T | S_KISS; K_ANY |
| DG105 | S K | T | S_LOVE; K_LOVE+; after DG101 |
| DG106 | G S | E CAMP | S_LOVE; G_TOG+; after DG100 |
| DG107 | V S | T | S_LOVE; V_TOG+; after DG102 |
| DG108 | A S | T | S_LOVE; A_LOVE; after DG103 |
| DG109 | C I | E AFTERFIGHT:deathhound | — |
| DG110 | L G P | E AFTERFIGHT:gargoyle | — |
| DG111 | K S | E AFTERFIGHT:eclipse (or vampire, outdoors) | SERANA |
| DG112 | X S | E AFTERFIGHT:vampire | SER_VAMP |
| DG113 | G V | E AFTERFIGHT:armoredtroll | — |
| DG114 | I K | E AFTERFIGHT:thrall | — |
| DG115 | V R | E AFTERFIGHT:chaurushunter | — |
| DG116 | G S | E AFTERFIGHT:vampire | after DG14 or DG77 |
| DG117 | C S | E AFTERFIGHT:raisedcorpse | after DG8 |
| DG118 | I K P | E AFTERFIGHT:aurielsbow | DG_BOW |
| DG119 | V K | E AFTERFIGHT:dawnguard | DG_VAMP |
| DG120 | R L | E AFTERFIGHT:falmer (in LOC:Vale) | after DG56 |

## 5. Notes for the build
- All DG "after the fight" rows are normal post-combat events (8 s delay, controller sees combat end); none needs the in-combat lane.
- "On the Dawnguard side" = DG_HUNT; "on the vampire side" = DG_VAMP. A talk with neither works on both.
- Rival talks (DG94-DG108): Luna has no romance line in any of them. Never fire a Serana rival talk while an SDA romance quest is running (her Free row already blocks this).
- Existing coverage avoided: SDA Serana x Inigo / x Remi topics (serana.md 5A), Ashe x Serana patch topics (ashe.md 5B), Kaidan/Xelzaz/Remi/Gore quest commentary (these are party-to-party only), Q19 garlic.
- Kaidan's cult never referenced. No "Dragonborn" anywhere in the file.
