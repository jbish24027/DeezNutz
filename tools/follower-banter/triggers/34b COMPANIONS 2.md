# 34b COMPANIONS 2 - trigger rows (prefix CP, CP71-CP130, 60 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\34b COMPANIONS 2.txt`.
Part one and its gate codes: `triggers\34 COMPANIONS.md` (sections 1-3 apply here unchanged, including every KaiComp block). Sources: `research\triggers\vanilla_gates.md` (B1, B3), `research\triggers\kaidan_block.md` (§1 KaiComp, §2a, §2b item 8, §4), `research\bibles\*.md`. Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana / Ashe Free rows and S_/A_ codes are in `triggers\20 DAWNGUARD.md` sections 1 and 3. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but player must not be in dialogue).

## 1. Silence and Kaidan's KaiComp (unchanged from part one)

- Companions silences (34 COMPANIONS.md §1): C03 15..24, C02 10..199, C04 20 in Glenmoril, C06 10 and 30..199, player in WerewolfBeastRace, the five KaiComp climax scenes, never in the Underforge cell 0165A6.
- **Every CP talk with K** carries part one §2A (KaiComp not running OR < 30 OR >= 150, plus KaiSTFUQuest not running and STFUVarNPCGeneral == 0).
- **§2B lead-in block** (KaiComp 10..29): applies to the K+P talks in this file: CP92, CP93, CP113, CP114.
- **§2C location blocks** while KaiComp runs: no CP talk in Vargr Den (85..120), and no CP talk in `LOC:Jorrvaskr` while KaiComp is 140..149. This covers every Jorrvaskr talk below (CP72-CP74, CP100, CP107-CP111, CP114-CP116, CP122, CP125, CP126, CP129, CP130).
- **Content rule:** no talk names or hints at anything in KaiComp (his trial, Wulf, the den, the hammer, the scholar or book in it, the sword he is given in Jorrvaskr, "my Harbinger and my love"). Kaidan's lines about Farkas/Vilkas are passing mentions only (CP102, CP129) and avoid the IF "travelling frathouse" topics (cards, spiders, sweet-roll theft, sparring footwork, limericks, Farkas's crush, ca-caw signals).

## 2. New gate codes (this file)

Reused from part one: `C_JOIN`, `C_PROVEN`, `C_INDUCT`, `WOLF`, `LUNA_WOLF`, `HARBINGER`, `LOC:Jorrvaskr`, `LOC:Skyforge`, `BEAST_BACK`, `BEAST_BACK_FIRST`, `CR_BRAWL`, `CR_ANIMAL`, `CR_HEIRLOOM`, `CR_RESCUE`, `FARKAS_CURE`, `AFTERFIGHT:silverhand`, `KODLAK_DEAD`.

Story (Skyrim.esm):
- `C_NOT_PROVEN` = C_JOIN and C01 (06E803) stage 200 not done (as part one CP11).
- `UNDERFORGE_NEXT` = C02 (06E804) completed and C03 (01CEF4) running with stage < 15 (Aela has told you to come to the Underforge; before the ritual silence). **[UNC: C03 first stage; use GetStage C03 >= 1 AND < 15]**
- `KODLAK_FREE` = HARBINGER (C06 completed; the cure-and-release ritual is part of C06).
- `PURITY_VILKAS` / `PURITY_FARKAS` = the vanilla "Purity" quest completed for that twin (they are cured with a Glenmoril head) **[UNC: EditorID (C06 follow-up / CR "Purity"), and how the quest records which twin; fallback: twin `HasKeyword` / not in WerewolfFaction after HARBINGER]**.
- `AELA_HUNT` = the player has done at least one Aela radiant or Totems quest step while LUNA_WOLF (Aela talks hunting with her) **[UNC; fallback TOTEMS running or done + LUNA_WOLF]**.

Radiant jobs (event = job's fight or completion; same detection as part one) **[UNC: all CR EditorIDs/FormIDs]**:
- `CR_TROUBLE` = AFTERFIGHT:bandit while a "Trouble in Skyrim" job (Vilkas) is running.
- `CR_CRIMINAL` = the "Escaped Criminal" job's target dies (Vilkas).
- `CR_STRIKE` = Aela's "Striking the Heart" job completes (Silver Hand leader dead).
- `CR_PLANS` = Aela's "Stealing Plans" job completes (plans picked up).
- `CR_ANIMAL:sabrecat` = CR_ANIMAL where the last target race was SabreCatRace / SabreCatSnowyRace **[UNC FormIDs]**.
- `CR_HEIRLOOM_DONE` = the "Family Heirloom" job item picked up (fires after the fight).

Places / items / events:
- `LOC:JorrvaskrQuarters` = player in the Jorrvaskr living-quarters cell (the downstairs bunk room) **[UNC cell FormID]**.
- `LOC:JorrvaskrYard` = exterior, within 1500 units of Jorrvaskr's back yard (the sparring yard) **[UNC ref]**. `SPARRING` = player is in combat-sparring in the yard, or a brawl just ended there **[UNC; fallback LOC:JorrvaskrYard + player IsWeaponDrawn]**.
- `LOC:JorrvaskrSteps` = exterior, within 600 units of Jorrvaskr's front door.
- `CITY:Whiterun` (existing pattern) / `LOC:WhiterunMarket` = Whiterun exterior, plains district **[UNC]**. `NEAR:LarsBraith` = within 1500 units of Lars Battle-Born or Braith, exterior **[UNC FormIDs]**.
- `BEAST_BACK:town` = BEAST_BACK while the player's location has LocTypeTown, LocTypeCity or LocTypeSettlement (vanilla_gates B2).
- `YSGRAMOR_SHIELD` = player has the Shield of Ysgramor in inventory **[UNC FormID]**.
- `WOLF_HELM` = player wears the Companions' Wolf Armor helmet **[UNC base FormID]**.
- `RIA_MET` = player has spoken to Ria at least once **[UNC; fallback C_JOIN + NEAR:Ria once]**.
- `AELA_MET` = player has spoken to Aela at least once (C00 does this) - use C_JOIN.
- `ASHE_BRAWL` = Ashe has fought in the Jorrvaskr yard once (part one CP69 played, or NP142 played).
- `BEAST_BACK>=2` = the controller has seen BEAST_BACK at least twice.
- `SNOW`, `CAMP`, `NIGHT`, `MORNING`, `PREDAWN` as TRIGGERS.md section 4.

Others: `SERANA` (S following), `SER_VAMP`, `S_KISS`, `DG_CAIRN` (20 DAWNGUARD.md §3), `ASHE_REVEAL`, `A_ANY`, `K_CRUSH`, `K_TOG+`, `K_LOVE+`, `K_ANY`, `V_ANY`, `LUC_ADMIT`, `GORE_READING` (HLIOGoreReading >= 1 [UNC], as 32b TG82), `after:X`.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| CP71 | G P | T | C_NOT_PROVEN |
| CP72 | V L | E LOC:JorrvaskrQuarters + NIGHT | C_JOIN |
| CP73 | C G | E LOC:Jorrvaskr | C_JOIN |
| CP74 | A R | E LOC:Jorrvaskr + MORNING | C_JOIN; ASHE_REVEAL |
| CP75 | I P | T | C_JOIN |
| CP76 | R P | T | C_PROVEN |
| CP77 | A K | T | C_PROVEN |
| CP78 | X P | T | UNDERFORGE_NEXT |
| CP79 | G K | E CR_TROUBLE | C_JOIN |
| CP80 | V K | E CR_CRIMINAL | C_JOIN |
| CP81 | A G | E CR_STRIKE | C_JOIN |
| CP82 | L R | E CR_PLANS | C_JOIN |
| CP83 | C V | E AFTERFIGHT:silverhand | C_PROVEN; after CP18 |
| CP84 | S K | E AFTERFIGHT:silverhand | C_PROVEN; SERANA; SER_VAMP; after CP22 |
| CP85 | I X | E AFTERFIGHT:silverhand (in a Silver Hand location interior) | C_PROVEN |
| CP86 | G P | T | WOLF; LUNA_WOLF |
| CP87 | L P | T | WOLF; LUNA_WOLF; after CP37 |
| CP88 | V P | E BEAST_BACK:town | LUNA_WOLF; not BEAST_BACK_FIRST |
| CP89 | X P | T (exterior) | LUNA_WOLF; SNOW |
| CP90 | I P | T | LUNA_WOLF; 3+ in-game days after WOLF |
| CP91 | L G | T | LUNA_WOLF; LUC_ADMIT |
| CP92 | K P | E CAMP + NIGHT | LUNA_WOLF; K_LOVE+; after CP29; §2B |
| CP93 | K P | E BEAST_BACK | LUNA_WOLF; K_CRUSH; not BEAST_BACK_FIRST; §2B |
| CP94 | V K | T | LUNA_WOLF; V_ANY; K_ANY; BEAST_BACK>=2 |
| CP95 | S A | E CAMP | LUNA_WOLF; SERANA; S_KISS; A_ANY; ASHE_REVEAL; never while an SDA romance quest runs |
| CP96 | C A | E BEAST_BACK | LUNA_WOLF; ASHE_REVEAL; not BEAST_BACK_FIRST |
| CP97 | R P | T | LUNA_WOLF; AELA_HUNT |
| CP98 | R X | T | LUNA_WOLF; BEAST_BACK>=2; Remi/Xelzaz not fallen out |
| CP99 | L S | E CAMP + NIGHT | LUNA_WOLF; SERANA; SER_VAMP |
| CP100 | G P | E LOC:Jorrvaskr | HARBINGER |
| CP101 | R P | E CITY:Whiterun (exterior) | HARBINGER |
| CP102 | K G | T | PURITY_VILKAS |
| CP103 | S P | T | HARBINGER; SERANA; SER_VAMP |
| CP104 | L R | T | YSGRAMOR_SHIELD |
| CP105 | V P | E WOLF_HELM (first time equipped, or T while worn) | C_JOIN |
| CP106 | C R | T | PURITY_FARKAS |
| CP107 | I P | E LOC:Jorrvaskr + hour 17..21 | HARBINGER |
| CP108 | G I | E LOC:Jorrvaskr | HARBINGER |
| CP109 | X P | E LOC:Jorrvaskr | C_JOIN; after CP3; 7+ in-game days after CP3 |
| CP110 | C L | E LOC:Jorrvaskr | C_JOIN; after CP11 |
| CP111 | S A | E LOC:Jorrvaskr | C_JOIN; SERANA; ASHE_REVEAL |
| CP112 | A P | T | C_JOIN; RIA_MET; ASHE_REVEAL |
| CP113 | K P | E LOC:JorrvaskrSteps + PREDAWN | HARBINGER; K_TOG+; §2B |
| CP114 | K G P | E LOC:JorrvaskrYard + SPARRING | C_JOIN; K_CRUSH; §2B |
| CP115 | V R | E LOC:Jorrvaskr + MORNING | C_JOIN |
| CP116 | K L | E LOC:JorrvaskrYard | C_JOIN |
| CP117 | S I | T | KODLAK_FREE; SERANA; DG_CAIRN |
| CP118 | X C | E CR_ANIMAL:sabrecat | C_JOIN |
| CP119 | G R | E CR_HEIRLOOM_DONE | C_JOIN; GORE_READING; after CP65 |
| CP120 | L C | E CR_RESCUE | C_JOIN; after CP66 |
| CP121 | I R | E CR_BRAWL | C_JOIN; after CP63 |
| CP122 | I K | E LOC:Jorrvaskr | C_JOIN |
| CP123 | C G | E LOC:Skyforge | C_JOIN; after CP10 |
| CP124 | S G | E CITY:Whiterun + NEAR:LarsBraith | HARBINGER; SERANA |
| CP125 | I L | E LOC:Jorrvaskr + hour 17..21 | HARBINGER; after CP107 |
| CP126 | X V | E LOC:Jorrvaskr | C_JOIN; ASHE_BRAWL |
| CP127 | R A | T (exterior) | LUNA_WOLF; ASHE_REVEAL; BEAST_BACK>=2 |
| CP128 | C K | T | C_JOIN; after CP5 |
| CP129 | R K | E LOC:Jorrvaskr + MORNING | HARBINGER; after CP109 |
| CP130 | A G | E LOC:Jorrvaskr + NIGHT | HARBINGER; ASHE_REVEAL |

## 4. Notes for the build

- **Same-event priority:** BEAST_BACK_FIRST still fires only part one's CP27. Later BEAST_BACK events pick one of CP33/CP34/CP36/CP41 (part one) or CP93/CP96 (here). BEAST_BACK:town fires CP88 in preference to any other BEAST_BACK talk. AFTERFIGHT:silverhand plays part one's CP21/CP22 first, then CP83/CP84/CP85.
- **Romance:** CP93 and CP114 are K_CRUSH (Luna oblivious: thinks he's cold / watching Ria's footwork). CP113 K_TOG+, CP92 K_LOVE+ (no "I love you" from Luna; she promises nothing beyond "a trail"). Rival talks CP94 (Val/Kaidan) and CP95 (Serana/Ashe) have no Luna line.
- **Luna stays branch-neutral:** CP78 (before the Underforge) has Xelzaz refuse to tell her what to choose and Luna states no choice. CP103 has her say the hall chooses for itself; she does not pick the twins' cure.
- **Ashe:** CP74/CP96/CP111/CP112/CP126/CP127/CP130 need ASHE_REVEAL (sensors, counting, not eating). CP77 and CP81 are tactical only and need just Free(A).
- **Serana:** CP84/CP99/CP103 need SER_VAMP. CP117 needs DG_CAIRN (she names the Soul Cairn).
- **Existing coverage avoided:** part one (Shield-Kaidan - CP128 only borrows the title, Tilma's stew - CP109 only answers it, temperature/hearing, chickens, moons, Lady-pup, the cure smells), PA101/PA102/SR95/SR96 (werewolf boots, deer, goat - not used), NP39-NP43, NP127/NP128/NP131/NP140-NP142 (Ria, Aela, Vilkas reading, Eorlund, Uthgerd, Torvar/Njada, Athis, Vilkas spar), WE121/WE122, PL245/PL396/PL276, FL8-FL10 and FL26 (KaiComp aftermath), CR145 (Wuuthrad).
- No "Dragonborn" anywhere in the file. No Kaidan cult references. Redcap lines are one word per sentence.
