# Triggers - 15 MISSIVES BOUNTIES INTERESTING NPCS (prefix MN, 130 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\15 MISSIVES BOUNTIES INTERESTING NPCS.txt`
Research: `research\content\dlc_cc_missives_3dnpc.md` sections E and F, plus a read-only houseCARL pass over 3DNPC.esp quest names, objectives, stage lists and NPC races (2026-10-18, epoch e2-7eff4aec5b0aebd6).

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C), plus **U = Luna** (player line, Eleonora voice; no Free() test).
Gate codes as TRIGGERS.md section 4. Extra codes used only in this file are defined below.

## New gate codes for this file

Missives (generic jobs; EditorID pattern `_M_Quest<Region><Type><Tier>`, expansion `_ME_Quest*`; stages 0 = taken, 100 = [COMPLETE] and paid, 105 = [FAIL]):
- `MS_BOARD` = player within ~300 units of a Missives notice-board activator. **[UNCONFIRMED: board ACTI FormIDs not looked up; find them in Missives.esp, Missives - Solstheim.esp, MissivesExpansion.esp at build]**
- `MS_BOARD:<Hold>` = MS_BOARD and the player is in that hold's location (WhiterunHoldLocation, ReachHoldLocation, WinterholdHoldLocation, EastmarchHoldLocation, RiftHoldLocation, HaafingarHoldLocation, HjaalmarchHoldLocation, FalkreathHoldLocation, PaleHoldLocation) or `WS(DLC2SolstheimWorld)` for Solstheim.
- `MS_RUN:<Type>` = any quest of that family running, stage 100 not done. Families (substring of the EditorID): Courier (all), CourierLetter / CourierWeapon / CourierPotion **[UNCONFIRMED exact substrings]**, CourierDistant, GatherOre, GatherIngr, GatherSoulGem, GatherInnFood **[UNCONFIRMED]**, KillAnimal / KillPest (`_ME_`), TrackThief, TrackFugitive, TrackVampire, Recover/Retrieve Ruin / Hideout **[UNCONFIRMED]**, FindBook / FindSpellTome / FindToy / FindDog (`_ME_`), CatchFish (`_ME_`), HealSick (`_ME_`), GatherMead (`_ME_`), GatherSteelSword (`_ME_`). Keep a script FormList per family.
- `MS_DONE[:<Type>]` = stage 100 newly done on a quest of that family (poll; controller remembers the last count). No type = any Missives quest.
- `MS_COUNT >= n` = controller's own int of Missives stage-100 completions.
- `BQ_DONE:<n>` = GetQuestCompleted of BQ01 095125 (bandit boss), BQ02 0BD77F (Forsworn), BQ03 0BD78C (giant), BQ04 0CBA9A (dragon), all Skyrim.esm, as overridden by Bounties Redone.
- `BOUNTY_DONE` = MS_DONE on KillBandit / KillGiant / KillForsworn / KillDragon / Track* families, or any BQ_DONE newly set.
- `MG_JOIN`, `GORE_BAIL`, `BRYNJAR`, `SOLST`, `DB`, `K_*`, `RC_WEREPIG`, `VAL_FATHIS` as TRIGGERS.md.

Interesting NPCs (all FormIDs `:3DNPC.esp`):
- `Done(Q,s)` = GetStageDone; `Comp(Q)` = GetQuestCompleted. Most 3DNPC quests use objectives, not journal text, so stage meanings below come from objective text and stage order. Where the stage that sets an objective was not traced, the row says **[UNCONFIRMED stage]** and gives the safe fallback.
- `KAI_INIGO` = KaiandInigo 000842:Kaidan and Inigo Meet.esp stage >= 10.

**Silence zones (add to WorldQuiet for this file, research F3):** 3DNPCMQ7 20..50; any 3DMCue4PartyViola* scene quest running (1F13F3, 1F142D, 1F143B, 1F144F); warrensquest 80..90 and 300..370; DJGQuest2 100..130; AsteriaQuest 80..90. Track-quest fights are covered by the combat gate.

## Table

### Part 1 - Missives and bounties
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MN1 | L C U | E MS_DONE (first ever) | MS_COUNT == 1 |
| MN2 | V I C | E MS_BOARD | — |
| MN3 | K G U | E MS_RUN:Courier (just taken) | — |
| MN4 | X K | E exterior while MS_RUN:CourierDistant | after MN3 not required |
| MN5 | R L U | T | MS_RUN:CourierLetter [UNCONFIRMED family] |
| MN6 | G V | T | MS_RUN:CourierWeapon [UNCONFIRMED family] |
| MN7 | C X | T | MS_RUN:CourierPotion [UNCONFIRMED family] |
| MN8 | R G | T | MS_RUN:GatherOre |
| MN9 | X C | T | MS_RUN:GatherIngr |
| MN10 | L I U | T | MS_RUN:GatherSoulGem |
| MN11 | X K | T | MS_RUN:GatherInnFood [UNCONFIRMED family] |
| MN12 | K I | E MS_DONE:KillAnimal or KillPest | — |
| MN13 | K G | E BOUNTY_DONE (KillBandit) or BQ_DONE:01 | — |
| MN14 | C G | E MS_DONE:KillGiant or BQ_DONE:03 | — |
| MN15 | K R | E MS_DONE:KillForsworn or BQ_DONE:02 | — |
| MN16 | V G U | E MS_DONE:KillDragon or BQ_DONE:04 | DB |
| MN17 | V R | T | MS_RUN:TrackThief |
| MN18 | K I U | T | MS_RUN:TrackFugitive; after MN13 |
| MN19 | C I | T | MS_RUN:TrackVampire |
| MN20 | V L U | T | MS_RUN:Recover (ruin) [UNCONFIRMED family] |
| MN21 | R K | T | MS_RUN:Recover (hideout) [UNCONFIRMED family] |
| MN22 | U L | T | MS_RUN:FindBook or FindSpellTome |
| MN23 | G I | T | MS_RUN:FindToy |
| MN24 | C K | T | MS_RUN:FindDog |
| MN25 | G X U | E WATER while MS_RUN:CatchFish | — |
| MN26 | R K U | T | MS_RUN:HealSick; K_CRUSH |
| MN27 | G C L | T | MS_RUN:GatherMead; after MN1 |
| MN28 | K G | T | MS_RUN:GatherSteelSword |
| MN29 | V G R | E MS_DONE | MS_COUNT >= 1 (first paid hand-in after the party is >= 3) |
| MN30 | V X U | E MS_DONE | after MN29; MS_COUNT >= 3 |
| MN31 | G K U | E MS_DONE | after MN29; MS_COUNT >= 8 |
| MN32 | K G | E BOUNTY_DONE | BRYNJAR |
| MN33 | V K | E BOUNTY_DONE | after A2 |
| MN34 | V C | E MS_BOARD in a hold capital (CITY) | after R8 |
| MN35 | L V | E MS_BOARD | after MN34; after C1 |
| MN36 | G C | E MS_BOARD | after R5 |
| MN37 | C X | E MS_BOARD:Solstheim | SOLST |
| MN38 | G L U | E MS_BOARD:Whiterun | after MN1 |
| MN39 | R K | E MS_BOARD:Reach | after B1 |
| MN40 | L U | E MS_BOARD:Winterhold | MG_JOIN |
| MN41 | X V | E MS_BOARD:Eastmarch | after X4 |
| MN42 | I K | E MS_BOARD:Rift | KAI_INIGO |
| MN43 | V R | E MS_BOARD:Haafingar | — |
| MN44 | K X | E MS_BOARD:Hjaalmarch | after C3 |
| MN45 | K L | E MS_BOARD:Falkreath | Kaidan-Lucien intro done (Lucien's own scene 1) |
| MN46 | G V | E MS_BOARD:Pale | GORE_BAIL; after A3 |
| MN47 | X L | E MS_BOARD:Solstheim | SOLST |
| MN48 | L C U | E MS_DONE | after MN1, MN16, MN27 and MN24-style dog job done (MS_DONE:FindDog) |
| MN49 | K V U | E BOUNTY_DONE | after MN13, MN18 |
| MN50 | G V U | E CAMP | MS_COUNT >= 5 |

### Part 2 - Interesting NPCs
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MN51 | L U | T | Done(3DNPCMQ1 196D2D, 1); not Done(3DNPCMQ1, 20) |
| MN52 | V K | T | Done(3DNPCMQ1, 20) |
| MN53 | U K | E exit Castle Dour (Solitude) | Done(3DNPCMQ1, 50) |
| MN54 | G R | T | Done(3DNPCMQ1, 80) |
| MN55 | G K U | T | Done(3DNPCMQ1, 177); DB |
| MN56 | C G | T | Done(3DNPCMQ1, 200) |
| MN57 | L G U | T | Done(3DNPCMQ1, 270) |
| MN58 | R L | T | Comp(3DNPCMQ2 19B9CD) (stage 250) |
| MN59 | V I | T | Done(3DNPCMQ2, 40) |
| MN60 | X U | T | Done(3DNPCMQ3 1A63C4, 60) |
| MN61 | K G | T | Comp(3DNPCMQ3) (stage 100) |
| MN62 | V G | T | Done(3DNPCMQ4 1A0BD4, 10); not Done(3DNPCMQ4, 20) |
| MN63 | V R | T | Done(3DNPCMQ4, 150) |
| MN64 | U L | T | Done(3DNPCMQ4, 250) |
| MN65 | K G | E arrival Frostfruit Inn (Rorikstead) | Done(3DNPCMQ5 1ADAFB, 6) |
| MN66 | U X | T | Done(3DNPCMQ5, 130) |
| MN67 | L K | T | Done(3DNPCMQ6 1B2911, 40) |
| MN68 | C I | T | Done(3DNPCMQ6, 92); RC_WEREPIG |
| MN69 | G V | T | Done(3DNPCMQ7 1B462D, 50) (party over; 20..50 is a silence zone) |
| MN70 | I C U | T | Comp(3DNPCMQ7) (200 or 500; lines are branch-neutral) [UNCONFIRMED which end is the sacrifice] |
| MN71 | K V | T | Done(3DNPCMQ7, 80) |
| MN72 | G I | T | Done(3DMCue 1D40F8, 5) |
| MN73 | K G | T | Done(3DMCue, 80); combat over |
| MN74 | X I | T | Done(3DMCue, 150) |
| MN75 | V U | T | Comp(3DMCue) (stage 320) |
| MN76 | X V | T | Comp(3dmcue2 1D96ED) (stage 200) |
| MN77 | R K | T | Done(3DMCue3 1E8C3C, 60) |
| MN78 | L V | T | Done(3DMCue4 1F05C2, 50); no 3DMCue4PartyViola* scene quest running |
| MN79 | V K | T | Done(3DMCue4, 80) |
| MN80 | X K | T | Done(3DMCue5 1F8527, 140); not Done(3DMCue5, 170) (keeps it before the Tikrid poisoning branch) |
| MN81 | R V U | T | Done(3dmcue6 203932, 50) |
| MN82 | L U | T | Comp(3dmcue6) (stage 90); after MN81 |
| MN83 | R G | T | Done(warrensquest 1C0F1E, 30); not in 80..90 |
| MN84 | X V | T | Done(warrensquest, 90); not in 300..370 |
| MN85 | L K | T | Done(warrensquest, 200) |
| MN86 | C G | T | Done(warrensquest, 370) (escape done; 300..370 is a silence zone) |
| MN87 | X I | T | Done(DJGQuest2 2CF48B, 100) [UNCONFIRMED: first stage after accepting Na'ir's contract; 100 is the safe one]; not in 100..130 |
| MN88 | C G U | T | Done(DJGQuest2, 125); DJGQuest2 stage > 130 |
| MN89 | V K | T | Done(DJGQuest2, 194) |
| MN90 | G V | T | Done(AsteriaQuest 15E47E, 20) |
| MN91 | R V | T | Done(AsteriaQuest, 41) |
| MN92 | R K U | T | Done(AsteriaQuest, 90) and stage >= 95 (out of the 80..90 window) [UNCONFIRMED end stage ~97] |
| MN93 | X G | E in New Gnisis Cornerclub (Windhelm) | Done(ViranyaQuest 17A1F7, 90) |
| MN94 | I C | T | Done(ViranyaQuest, 65) |
| MN95 | V G K | T | Done(GorrQuest 171FD5, 81) |
| MN96 | G I | T | Done(GorrQuest, 140) or Comp(GorrQuest); after C2 |
| MN97 | K L | T | Done(ArilwaenQuest 2838D9, 20) |
| MN98 | I U | T | Done(ArilwaenQuest, 80) |
| MN99 | L U | T | Done(blackrobesquest 242E87, 70) |
| MN100 | R I | T | Done(blackrobesquest, 30); after B6 |
| MN101 | X G | T | Comp(AnumLaQuest 1413D9) (stage 100); after X1 |
| MN102 | X R | T | Comp(FjonaAnumLa 14D230 "Tears of the Hist") [UNCONFIRMED quest content; lines generic]; Remi/Xelzaz not fallen out |
| MN103 | I K | T | Comp(RDQuest 12A16A) (100 or 200); KAI_INIGO |
| MN104 | L U | T | Comp(CWQQ2 038120 "Forgotten Lore") (stage 200) |
| MN105 | X I | T | Comp(SvashniQuest 14E08B) (110 or 200) |
| MN106 | U L | T | Comp(RumarinQuest 145C24) (stage 100) |
| MN107 | C R | T | Comp(RumarinQuest2 185B23 "The Sleeping Giant") [UNCONFIRMED quest content; joke is only the name] |
| MN108 | R G | T | Comp(ZoraQuest 147D05) (100 or 150) |
| MN109 | K G U | T | HorkerQuest 12E107 objective "Salvage the Meat and Speak to Callen" shown [UNCONFIRMED stage, ~20; stages are 0,4,5,10,15,17,20,24,25,30...] |
| MN110 | X K | T | HorkerQuest objective "Gather a Lavender, Tomato, Fire Salts, Carrot, Resist Frost, and a Repel or Bane Undead Scroll" shown [UNCONFIRMED stage, ~35-40]; quest not completed |
| MN111 | V K | T | Comp(HorkerQuest) (250 or 100); K_CRUSH [UNCONFIRMED: assumes the stew is Callen courting Gorr, from quest title + "Bring the Horker Stew to Gorr"] |
| MN112 | C L | E on the High Hrothgar steps path | DialogueDarRakki 002912 running, objective "Count the Steps" active [UNCONFIRMED stage ~10]; not Done(DialogueDarRakki, 100) |
| MN113 | V U | T | Comp(DialogueDarRakki) (100 or 110) |
| MN114 | R L | T | Done(DialogueTheRelic 044B3C, 10) |
| MN115 | R K | T | Done(DialogueTheRelic, 20) or Done(.., 30); after B1, after B2 |
| MN116 | C R | T | Done(AldiQuest 18BAC1, 10) |
| MN117 | L U | T | Done(AldiQuest, 60) [UNCONFIRMED: "Find the Artifact in Blackreach" objective ~stage 40-60] |
| MN118 | G K U | T | AldiQuest objective "Pull the Lever" completed [UNCONFIRMED stage ~150-160]; after MN13 |
| MN119 | R X | T | Comp(AldiQuest) (stage 200; branch-neutral) |
| MN120 | C K U | E in AnisesCabin cellar | BookQuest3DNPC 191004 stage 1 done; stage 10 not done |
| MN121 | U L | T | BookQuest3DNPC objective "Read Volume III of The Paper Mirror" completed [UNCONFIRMED stage ~70] |
| MN122 | K G | T | Done(DialogueTikrid 07A023, 10) [objective "Speak to Tikrid in Dawnstar"; UNCONFIRMED exact stage] |
| MN123 | K U | T | Comp(DialogueTikrid) (stage 500); K_ANY |
| MN124 | G R | T | Comp(BeatriceQuest 15A1BD "Mogo's Mead") (stage 500) |
| MN125 | G X | T | Comp(LurgokQuest 1BD1F8) (400 or 500; branch-neutral) |
| MN126 | I K U | T | Comp(KjoliQuest 1626B4 "To Warm Sands") (stage 500); K_TOG+; KAI_INIGO |
| MN127 | V K | T | Comp(RaynesGriffithQuest 164D86 "Brother and Keeper") (stage 500); VAL_FATHIS; KAI_INIGO [UNCONFIRMED quest content; lines use the brothers theme only] |
| MN128 | X G | E INN | LuaffynsBand 136303 running and band members in the player's cell [UNCONFIRMED: band ref check; scene quests LuaffynBandScene* 0E5BDC..0E8230] |
| MN129 | I V | T | Comp(GlathrielsBow 157064) (stage 100) [UNCONFIRMED quest content; lines generic]; after I1 |
| MN130 | K R U | E 3DNPC follower recruited | any 3DNPC follower newly in CurrentFollowerFaction (DialogueFollower3DNPC 13184C alias; Zora 0EF4A6, Rumarin 0AB6D5, Anum-La, Morndas 0BB994 etc.); after B1 |

## Open items for build
- Missives board activator FormIDs and the exact type substrings in `_M_Quest*` EditorIDs (letter / weapon / potion couriers, inn food, recover jobs).
- 3DNPC stages marked [UNCONFIRMED stage]: map each objective index to the stage that sets it (read the quest fragments).
- MN70: which of 3DNPCMQ7 200 / 500 is the self-sacrifice end. Lines are written to fit both.
- MN111: confirm Callen is courting Gorr with the stew.
- MN102, MN107, MN127, MN129: quest stories not read; the talks only lean on the quest names.
- Anum-La's NPC record was not found by name (likely spelled differently); MN101/MN102 avoid pronouns for Anum-La on purpose.
