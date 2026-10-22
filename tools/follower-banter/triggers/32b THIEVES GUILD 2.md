# 32b THIEVES GUILD 2 - trigger rows (prefix TG, TG81-TG140, 60 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\32b THIEVES GUILD 2.txt`.
Part one and its gate codes: `triggers\32 THIEVES GUILD.md` (sections 1-2 apply here unchanged). Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana / Ashe Free rows are in `triggers\20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but player must not be in dialogue).

## 1. Silence

Same as part one (32 THIEVES GUILD.md section 1): TG05 10..199, TG07 10..39, TG08A 40..59, TG08B 40..59, TG09 30..199, TGLeadership 30..199, Kaidan's KaiJail window and `KaiJailedVar`, Val's `ValTG*` scenes via Free(V).

## 2. New gate codes (this file)

Reused from part one: `TG_JOIN`, `TG_RING`, `TG_HONNING`, `TG_GULUM`, `TG_OATH`, `TG_SEPULCHER`, `TG_CITY:<quest>`, `TG_CITY4`, `TG_GM`, `LOC:Flagon`, `LOC:Riften`, `LOC:Ratway`, `JOB:<type>`, `AFTERFIGHT:ratway`.

Radiant jobs (event = quest just completed; same detection as part one):
- `JOB:sweep` = the Sweep Job radiant quest **[UNC EditorID/FormID; expected in the TGR* block next to TGRBE/TGRSL]**.
- `JOB:bedlam:Whiterun` = JOB:bedlam whose target hold was Whiterun **[UNC: read the job's city alias / location at completion]**.
- `JOB_COUNT>=N` = Vex + Delvin radiant completions **[UNC: TG radiant counter globals; fall back to "TG_JOIN and 5+ in-game days"]**.

City jobs and their fences:
- `TG_SILVER` = TGTQ01 Silver Lining (0799DF) completed (Endon becomes a fence).
- `TG_NIRANYE` = TGTQ04 Summerset Shadows (0799E2) completed (Niranye becomes a fence).
- `TG_ARN` = TGTQ03 Imitation Amnesty (0799E1) completed (Arn freed).
- `TG_MALLUS` = TG03 completed and Mallus Maccius owns Honningbrew (vanilla does this at TG03 end) **[UNC: check Mallus/Sabjorn state]**.
- `TG_VALD` = Vald's Quick Fix (Maven's quill from Lake Honrich) completed **[UNC: EditorID; it is a TG07 side objective/quest]**.

Flagon people (event = player within ~600 units of that NPC in LOC:Flagon unless noted; **[UNC all NPC FormIDs]**):
- `NEAR:Vekel`, `NEAR:Dirge` (Flagon door), `NEAR:VexDelvin` (their table).
- `TG_GROWN` = the new members (Cynric Endell, Etienne Rarnis, Garthar, etc.) are enabled in the Flagon **[UNC: they appear after the city-job influence; test with Cynric `GetDisabled == 0`]**.
- `RUNE_TALK` = player has heard Rune's "where I come from" dialogue **[UNC; fall back to TG_JOIN + NEAR:Rune]**.
- `CYNRIC_IN` = Cynric Endell enabled in the Flagon. `GARTHAR_IN` = Garthar enabled. `NIRUIN_TALK` = Niruin greeting heard **[UNC; fallback NEAR:Niruin]**. `SAPPHIRE_SNAP` = TG_JOIN + NEAR:Sapphire (her greeting is the snap). `THRYNN_MET` = NEAR:Thrynn once.
- `ETIENNE_IN` = MQ201 (Diplomatic Immunity) completed **and** Etienne Rarnis alive **and** enabled in the Flagon **[UNC: confirm he moves there after rescue]**.
- `TONILIA_ASHE` = TG_JOIN + ASHE_REVEAL + player has bartered with Tonilia once **[UNC; fallback NEAR:Tonilia]**.
- `BEGGARS` = TG_CITY4 (beggar network active) **[UNC; part one used TG_GM for TG67]**.
- `BRANDSHEI_BACK` = TG_RING and Brand-Shei is in Riften market (not in RiftenJail cell) **[UNC FormID]**.

Guild Master (all need `TG_GM`, which excludes the Brynjolf-leads branch):
- `TG_GMARMOR` = event: player first equips the Guild Master's cuirass **[UNC FormID]**.
- `MAVEN_GM` = TG_GM and in Riften, after the first in-game day as Guild Master **[UNC: no scripted summons traced; this is flavour timing]**.
- `VAULT_FULL` = TG_GM and TG_CITY4 (vault gold piles enabled) **[UNC: vault-pile enable flags]**.
- `ARCH` (existing) = MG08 stage 200.
- `LOC:Cistern` = Ragged Flagon Cistern cell (part of RiftenRaggedFlagonLocation; check `GetInCell`) **[UNC cell FormID]**. `NEAR:GMDesk` = within 500 units of the Guild Master's desk in the Cistern.

Nightingale powers (event after a fight in which the player cast that power; player alias `OnSpellCast` sets a flag, cleared after the talk or the next fight) **[UNC spell FormIDs]**:
- `CAST:shadow` = Shadowcloak of Nocturnal (Agent of Shadow). `CAST:subterfuge` = Agent of Subterfuge. `CAST:strife` = Nightingale Strife (Agent of Strife).
- `NG_ARMOR` = event: first time player equips the Nightingale cuirass outside the Cistern/Nightingale Hall.
- `NG_BOW` = event: combat ends while the Nightingale Bow is equipped **[UNC FormID]**.
- `NG_SNEAKPAST` = event: player passes within 600 units of 3+ hostile actors while sneaking without combat starting, with any Nightingale power active **[UNC; simpler fallback = CAST:shadow without combat]**.
- `LOC:NightingaleHall` = approach (exterior, within 1500 units) **[UNC]**.

Cistern life:
- `SLEPT:Cistern` = event: player wakes (OnSleepStop) in LOC:Cistern. `MORNING`, `PREDAWN` as TRIGGERS.md section 4.
- `REMI_LESSONS` = after TG80 played (Remi and Redcap pickpocket bark) **[soft chain; flavour only]**.

Others: `GORE_BAIL`, `K_CRUSH`, `K_TOG+`, `ASHE_REVEAL`, `SERANA` (S following), `after:X` as TRIGGERS.md / 20 DAWNGUARD.md.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| TG81 | X P | E JOB:numbers | TG_JOIN; after TG25 or TG25 skipped |
| TG82 | G R | E JOB:numbers | TG_JOIN; Remi-Gore reading lessons started (HLIOGoreReading >= 1) [UNC]; after TG81 |
| TG83 | C I | E JOB:fishing | TG_JOIN; after R13 |
| TG84 | S L | E JOB:fishing | TG_JOIN; S following; after TG83 |
| TG85 | K G P | E JOB:bedlam:Whiterun | TG_JOIN; after A1 |
| TG86 | R V | E JOB:shill | TG_JOIN |
| TG87 | I P | E JOB:shill | TG_JOIN; JOB_COUNT>=5; after TG86 |
| TG88 | A C | E JOB:burglary | TG_JOIN; ASHE_REVEAL |
| TG89 | X V | E JOB:sweep | TG_JOIN; after X4 |
| TG90 | G L | E JOB:heist | TG_JOIN; after L1 |
| TG91 | G R | E LOC:Flagon or T | TG_JOIN; JOB_COUNT>=3 |
| TG92 | L P | E LOC:Flagon | TG_JOIN; JOB_COUNT>=3 |
| TG93 | K R P | T | TG_SILVER |
| TG94 | V X | T or E CITY:Windhelm | TG_NIRANYE; after X4 |
| TG95 | G K | T | TG_ARN; GORE_BAIL; after A1 |
| TG96 | K S | T | TG_MALLUS; S following |
| TG97 | L A | T | TG_VALD; ASHE_REVEAL |
| TG98 | K R | E LOC:Flagon | TG_GROWN; after B1 |
| TG99 | G K | E LOC:Flagon + NEAR:Vekel | TG_JOIN; after A1 |
| TG100 | C G | E LOC:Flagon + NEAR:Dirge | TG_JOIN; after R5 |
| TG101 | I P | E LOC:Flagon | RUNE_TALK |
| TG102 | R L | E LOC:Flagon | CYNRIC_IN; after B10 |
| TG103 | A I | E LOC:Flagon | NIRUIN_TALK; ASHE_REVEAL |
| TG104 | G P | E LOC:Flagon | SAPPHIRE_SNAP |
| TG105 | L G | E LOC:Flagon | THRYNN_MET; after L1 |
| TG106 | K P | E LOC:Flagon | ETIENNE_IN |
| TG107 | X V | E LOC:Flagon | GARTHAR_IN; after X4 |
| TG108 | R A | T | TONILIA_ASHE; after TG9 if played |
| TG109 | L I | E LOC:Flagon + NEAR:VexDelvin | TG_JOIN |
| TG110 | C P | E LOC:Riften | BEGGARS |
| TG111 | S R | E LOC:Riften (market) | TG_JOIN; S following |
| TG112 | I P | E LOC:Riften (market) | BRANDSHEI_BACK; after TG1 |
| TG113 | V P | E TG_GMARMOR | TG_GM |
| TG114 | S P | T in Riften | MAVEN_GM; S following |
| TG115 | R C | E LOC:Cistern | VAULT_FULL |
| TG116 | K P | E LOC:Flagon | TG_GM; K_CRUSH |
| TG117 | X G | T | TG_GM; 2+ in-game days after TG_GM |
| TG118 | L P | T | TG_GM; ARCH |
| TG119 | I V | E LOC:Flagon | TG_GM; after I1; after TG62 if played |
| TG120 | G A | E LOC:Flagon | TG_GM; ASHE_REVEAL |
| TG121 | R P | E LOC:Cistern + NEAR:GMDesk | TG_GM |
| TG122 | S K | E LOC:Cistern + NIGHT (hour 0..3) | TG_GM; K_TOG+; S following |
| TG123 | G K | E CAST:shadow | TG_OATH; after A1 |
| TG124 | C V | E CAST:subterfuge | TG_OATH; after R8 |
| TG125 | S X | E CAST:strife | TG_OATH; S following |
| TG126 | L P | E NG_ARMOR | TG_OATH |
| TG127 | I P | E NG_BOW | TG_SEPULCHER |
| TG128 | K P | E NG_SNEAKPAST | TG_OATH; K_TOG+ |
| TG129 | L X | E LOC:NightingaleHall | TG_OATH |
| TG130 | A P | T | TG_SEPULCHER; ASHE_REVEAL |
| TG131 | L G | E SLEPT:Cistern | TG_JOIN; after L1 |
| TG132 | R C | E LOC:Cistern | TG_JOIN; after TG80 |
| TG133 | G I | E LOC:Cistern | TG_JOIN; after C2 |
| TG134 | L V | E LOC:Cistern | TG_JOIN; after C1 |
| TG135 | K P | E LOC:Cistern + PREDAWN | TG_JOIN; K_TOG+ |
| TG136 | X I | E LOC:Cistern | TG_JOIN; after X6 |
| TG137 | C V | E AFTERFIGHT:ratway | TG_GM; after R8 |
| TG138 | A L | E CAST:shadow (in a fight) | TG_OATH; ASHE_REVEAL; after TG123 |
| TG139 | I R | E AFTERFIGHT:bandit while any TGTQ0x city quest is running | TG_JOIN; after B6 |
| TG140 | R P | E player opens the vault door (cell enter of vault) [UNC] | TG_GM |

## 4. Notes for the build

- **Branch safety:** Part 4 (TG113-TG122) all carry TG_GM, which excludes Brynjolf-as-Guild-Master (Val's `ValTGLeadership`, TG Alternative Endings). TG137 and TG140 too. Part 5 follows the Agent the player actually chose because each talk is fired by casting that power (CAST:*). TG126/TG127/TG129/TG130 are power-neutral.
- **Kaidan:** no talk pairs Kaidan with Brynjolf, Vex/Delvin gossip, Vipir or the Riften arrest. TG95 mentions his Thalmor cell only (fine to mention). TG116 is K_CRUSH (Luna misreads his blush as the stew); TG122/TG128/TG135 are K_TOG+.
- **Val:** nothing about his Vex crush, Delvin as his old contact, or whether he took the Agent path. TG113 hats, TG119 "visiting talent" (he's not a Guild member in our framing; fine with his own storyline either way).
- **Gore:** TG82 and TG105 only touch his reading as an ongoing thing (no repeat of the lessons themselves). TG95 needs GORE_BAIL (his own Dawnstar cell).
- **Ashe:** every Ashe talk carries ASHE_REVEAL (talks about sensors, logging, not floating). No father content in this file.
- **Serana:** TG125 is about Nightingale Strife only; she calls herself "the only monster" (still a vampire works; if cured the line still reads as a joke) - optional `SER_VAMP` if the build wants it strict.
- **Same-event priority:** JOB:numbers fires TG81 first, TG82 on a later numbers job; JOB:fishing TG83 then TG84; JOB:shill TG86 then TG87. CAST:shadow fires TG123 first, TG138 on a later one.
- **Existing coverage avoided:** part one's fishing pun, flourished ledger, backwards burglary, dimples heist, Bedlam "collect"; Q11/Q12; Remi-Xelzaz Riften pickpocket and Olfrid cons (no Remi-Xelzaz pair here); Lucien-Inigo Riften smells (TG109 is about Vex and Delvin). No "Dragonborn", no cult, no beard.
