# 32 THIEVES GUILD - trigger rows (prefix TG, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\32 THIEVES GUILD.txt`.
Sources: `research\triggers\vanilla_gates.md` (B1, B3), `research\content\00_inventory.md` (Vanilla TG quest list, TG Alternative Endings), `research\bibles\*.md`, plus a read of the follower plugins' own TG lines (Val `ValTG*`, Gore `HD1FactionScenes`/`HD1GoreFollows` TG topics, Kaidan `KMQ` TG topics, Inigo `InigofollowerDialogue` TG lines) so we don't repeat or contradict them.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana / Ashe Free rows are in `triggers\20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but player must not be in dialogue).

## 1. Thieves Guild silence (already in WorldQuiet, repeated here)

No TG talk (and no other banter) while (vanilla_gates B3, all Skyrim.esm):
- TG05 Speaking With Silence (021551) stage 10..199 (Snow Veil Sanctum, Mercer's betrayal). [CONFIRMED]
- TG07 The Pursuit (021553) stage 10..39 (empty vault reveal in the Flagon). [UNC exact scene stage]
- TG08A Trinity Restored (057F99) stage 40..59 (Nightingale oath; winner TG Alternative Endings.esp, stages kept). [CONFIRMED]
- TG08B Blindsighted (021554) stage 40..59 (Mercer fight in Irkngthand). [CONFIRMED]
- TG09 Darkness Returns (021555) stage 30..199 (Pilgrim's Path, Twilight Sepulcher, Nocturnal). [CONFIRMED]
- TGLeadership Under New Management (0D7D69) stage 30..199 (Guild Master ceremony). [CONFIRMED]
- Also respect Kaidan's `KaiJailedVar` (31F28D:Kaidan - Immersive Features.esp) == 0 and KaiJail ArrestScene not playing (TRIGGERS.md §2 Kaidan set pieces) - Riften is where his arrest quest fires.
- Val: his own `ValTG*` scenes run as dialogue / IsInScene, so `Free(V)` already blocks them. Also skip any talk with Val while `ValTGCrow` (290776:AX ValSerano.esp) or `ValTGAgent` (23A085) is running **[UNC: whether those hold him in scenes]**.

## 2. Gate codes used in this file (new)

Story (all Skyrim.esm unless noted; "done" = GetQuestCompleted, or the stage as given):
- `TG_BRYN` (existing) = TG00 stage 8 done. `TG_JOIN` (existing) = TG02 stage 10 done.
- `TG_RING` = TG00 A Chance Arrangement (021556) completed. **[UNC: completion requires the ring plant in vanilla; `thieves guild requirements.esp` wins TG00 - check it doesn't add another way]**
- `TG_DEBTS` = TG01 Taking Care of Business (01F326) completed.
- `TG_URN` = TG01 Bersi objective done **by smashing the urn** (Dwemer urn in the Pawned Prawn destroyed). **[UNC: find the TG01 stage/var set by the urn smash; else check the urn ref `IsDisabled`/destroyed state]**
- `TG_GOLDEN` = TG02 Loud and Clear (02154E) completed.
- `TG_HONNING` = TG03 Dampened Spirits (02154F) completed.
- `TG_GULUM` = TG04 Scoundrel's Folly (021550) completed.
- `TG_MERCER_MET` = TG02 stage 20 done ("welcomed into the Thieves Guild by Mercer Frey", vanilla_gates B1).
- `TG_SNOWVEIL` = TG05 (021551) completed (stage 200).
- `TG_GALLUS` = TG06 Hard Answers (021552) completed.
- `TG_VAULT` = TG07 (021553) stage 40 done (after the vault silence). **[UNC: stage 40 = Riftweald search start per vanilla_gates]**
- `TG_RIFTWEALD` = TG07 running, stage 40..59.
- `TG_OATH` = TG08A (057F99) completed. `TG_PREOATH` = TG08A not completed.
- `TG_IRK` = TG08B (021554) running and stage < 40.
- `TG_MERCERDEAD` = TG08B completed.
- `TG_KEY` = TG_MERCERDEAD and TG09 not completed and player `GetItemCount TG08SkeletonKey > 0` **[UNC FormID of the Skeleton Key item; TG Alternative Endings lets the player keep it - this gate still works because it reads the item]**.
- `TG_SEPULCHER` = TG09 (021555) completed. **[UNC: TG Alternative Endings "keep the Key" path may never complete TG09; then TG55-57 never play - acceptable]**
- `TG_CITY:<n>` = TGTQ01 Silver Lining (0799DF, Markarth) / TGTQ02 The Dainty Sload (0799E0, Solitude) / TGTQ03 Imitation Amnesty (0799E1, Whiterun) / TGTQ04 Summerset Shadows (0799E2, Windhelm) completed. `TG_CITY4` = all four completed.
- `TG_GM` = TGLeadership (0D7D69) completed **and the player is Guild Master** (`GetFactionRank ThievesGuildFaction >= <GM rank>` **[UNC rank]**). Excludes the Brynjolf-as-Guild-Master branch from `ValTGLeadership` (623B0B:AX ValSerano.esp) / TG Alternative Endings.
- `TG_LARCENY` = TGLarceny (04C6C2) started (stage > 0).
- `TG_CROWN_ON` = TGCrown (09DD77) started. `TG_CROWN` = TGCrown completed. (`thieves guild requirements.esp` wins TGCrown; stages kept.)
- `TG_CARAVAN` = TGFenceCaravan (0D8E40) started. **[UNC: confirm it starts when the Khajiit fences unlock]**
- `TG_SHADOWMARKS` = player has read the book "Shadowmarks" (Delvin's gift) or TG02 completed as fallback. **[UNC book FormID / read check]**
- `TG_ARMOR` = event: player first equips the Thieves Guild Cuirass (ArmorThievesGuildCuirass) **[UNC FormID; controller polls GetEquipped on its 60 s tick]**.
- `TG_TONILIA` = player has sold to Tonilia (`QueryStat "Items Fenced"` or similar > 0 while TG_JOIN) **[UNC stat name; fallback = TG_JOIN]**.
- `LOCKS` = `QueryStat "Locks Picked" >= 5` (vanilla misc stat). **[UNC exact stat string]**

Radiant jobs (event = the radiant quest just completed; poll stage 200 / completion on the 60 s tick) **[UNC: all TGR* quests restart; detect "just completed" by watching each quest's stage or the Delvin/Vex job-count globals]**:
- `JOB:numbers` TGRFO (06098E), `JOB:fishing` TGRGF (028922), `JOB:shill` TGRDU (015D24), `JOB:bedlam` TGRNT (060990), `JOB:heist` TGRSL (02893E), `JOB:burglary` TGRBE (02893B).

Places (`E LOC:<name>` = arrival; first time unless noted) **[UNC: all location FormIDs to look up at build]**:
- `LOC:Riften` = RiftenLocation (hold capital, `CITY:Riften`). `LOC:Ratway` = RiftenRatwayLocation (any Ratway cell). `LOC:Flagon` = RiftenRaggedFlagonLocation (Ragged Flagon / Cistern). `LOC:Goldenglow` = GoldenglowEstateLocation. `LOC:Riftweald` = RiftenRiftwealdManorLocation. `LOC:Irkngthand` = IrkngthandLocation.

Fights (`E AFTERFIGHT:<type>`, controller saw player combat end):
- `ratway` = in LOC:Ratway. `goldenglow` = in LOC:Goldenglow. `falmer` = last target FalmerRace and in LOC:Irkngthand. `summerset` = TGTQ04 running and last target in the Summerset Shadows faction **[UNC faction]**. `skeever` = TG03 running and last target SkeeverRace (Honningbrew cellar). `riftweald` = TG_RIFTWEALD and in LOC:Riftweald.

Other events:
- `CAUGHT` = player's bounty in CrimeFactionRift rose this tick (poll `GetCrimeGold`) and TG_JOIN.
- `PICKPOCKET` = `QueryStat "Pockets Picked"` rose this tick and TG_JOIN. **[UNC stat string]**

Romance / people: K/G/V codes as TRIGGERS.md §4; `S_COMP`, `A_ANY`, `G_ANY`, `ASHE_REVEAL`, `ASHE_Q1`, `DG_HARKON` as `triggers\20 DAWNGUARD.md` §3. `ASHE_HUNT` = MM_AMQ_02 (BB194C:Ashe - Fire and Blood.esp) started (she is chasing her father's killer) - falls back to `ASHE_Q1`.

Chains: `after:X` = talk X already played. "meets" = that pair's first-meeting talk (A1 G-K, A2 V-K, A3 G-V, B1 R-K, B6 I-R, B10 L-R, C1 L-V, C2 G-I, C3 X-K, R1 C-K, R5 G-C, R8 V-C, R11 L-C, R13 C-I, X1 G-X, X4 X-V, X6 I-X, I1 V-I, L1 G-L; pairs with their own mod intros: K-I, R-V, R-G, R-X, R-C, X-L, X-C, L-K, L-I; Serana/Ashe pairs: their meets in 48 SERANA / 49 ASHE **[UNC IDs, not written yet]**).

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| TG1 | I R P | T | TG_RING; meets |
| TG2 | L S | E LOC:Ratway | first visit; S following |
| TG3 | C G | E LOC:Flagon | first visit; meets |
| TG4 | K I | E LOC:Flagon | TG_BRYN; any visit after TG3 played or skipped |
| TG5 | I P | T | TG_JOIN |
| TG6 | L R | T | TG_JOIN; meets |
| TG7 | K G P | T | TG_JOIN; meets |
| TG8 | R P | T | TG_JOIN; LOCKS |
| TG9 | A R P | E TG_ARMOR | ASHE_REVEAL |
| TG10 | X A | T | TG_MERCER_MET; TG05 not started (before Snow Veil); ASHE_REVEAL |
| TG11 | R V | E LOC:Flagon or T | TG_JOIN |
| TG12 | A V | E LOC:Flagon or T | TG_JOIN; ASHE_REVEAL; K_ANY |
| TG13 | I K | T | TG_DEBTS |
| TG14 | R P | T | TG_URN [UNC] |
| TG15 | C G | E LOC:Goldenglow | first visit; TG02 running; after TG3 |
| TG16 | X P | T | TG_GOLDEN |
| TG17 | L K | T | TG_HONNING; meets |
| TG18 | S K | T | TG_HONNING; DG_HARKON; S following |
| TG19 | R X | T | TG_GULUM; Remi/Xel not fallen out (TRIGGERS.md §3) |
| TG20 | A R | T | TG_GULUM |
| TG21 | R V | T | TG_JOIN; TG_TONILIA [UNC] |
| TG22 | C K P | T | TG_JOIN; after R1 |
| TG23 | V C | E LOC:Riften or T in Riften | TG_JOIN; after R8 |
| TG24 | I V P | T | TG_JOIN; after I1 |
| TG25 | L A | E JOB:numbers | — |
| TG26 | G K | E JOB:fishing | after A1 |
| TG27 | K X | E JOB:shill | after C3 |
| TG28 | C S | E JOB:bedlam | S following |
| TG29 | A V | E JOB:heist | — |
| TG30 | K P | E JOB:burglary | K_CRUSH |
| TG31 | L R P | T | TG_SHADOWMARKS [UNC]; after B10 |
| TG32 | X K | T | TG_JOIN; TG_PREOATH; after C3 |
| TG33 | I V | T | TG_CARAVAN [UNC]; after I1 |
| TG34 | L P | T | TG_JOIN |
| TG35 | K P | T | TG_SNOWVEIL; K_TOG+ |
| TG36 | G V | T | TG_SNOWVEIL; after A3 |
| TG37 | A I | T | TG_SNOWVEIL; ASHE_HUNT (or ASHE_Q1) |
| TG38 | L X | T | TG_GALLUS |
| TG39 | R S | T | TG_GALLUS; S following |
| TG40 | X I | T | TG_GALLUS; after X6 |
| TG41 | C G P | T | TG_VAULT; after TG3 |
| TG42 | L R | E LOC:Riftweald | TG_RIFTWEALD; first visit |
| TG43 | G P | T | TG_OATH |
| TG44 | X K P | T | TG_OATH; after C3 |
| TG45 | L S P | T | TG_OATH; S following |
| TG46 | R V | T | TG_OATH |
| TG47 | L P | T | TG_OATH |
| TG48 | R G | T | TG_OATH |
| TG49 | S V | T | TG_OATH; DG_HARKON; S following; VAL_FATHIS not required (Val's line stays "history") |
| TG50 | L R | E LOC:Irkngthand | TG_IRK (outside the 40..59 silence) |
| TG51 | L C | T | TG_MERCERDEAD; after R11 |
| TG52 | K G | T | TG_MERCERDEAD; after A1 |
| TG53 | R P | T | TG_KEY |
| TG54 | A K P | T | TG_KEY |
| TG55 | K P | T | TG_SEPULCHER; K_TOG+ |
| TG56 | I L | T | TG_SEPULCHER |
| TG57 | R X | T | TG_SEPULCHER; Remi/Xel not fallen out |
| TG58 | X V | T | TG_CITY:TGTQ02; after X4 |
| TG59 | G L | T | TG_CITY:TGTQ03; after L1 |
| TG60 | K X | T | TG_CITY:TGTQ04; after C3 |
| TG61 | A P | T | TG_CITY4 |
| TG62 | K S | E LOC:Flagon | TG_CITY4; S following |
| TG63 | G V P | T | TG_GM; after A3 |
| TG64 | R L | T | TG_LARCENY |
| TG65 | L V P | T | TG_CROWN_ON; after C1 |
| TG66 | C P | T | TG_CROWN |
| TG67 | I K | T | TG_GM; after TG5 or TG13 (Inigo's "mostly" worry) |
| TG68 | L K | T | TG_CITY:TGTQ03; after TG42 |
| TG69 | X P | T | TG_GM |
| TG70 | V K | T in Riften | TG_JOIN; K_ANY; after A2 |
| TG71 | G A | T | TG_JOIN; A_ANY or G_ANY |
| TG72 | S K | T in Riften | TG_JOIN; K_ANY; S_COMP |
| TG73 | G C | E AFTERFIGHT:ratway | after R5 |
| TG74 | K V | E AFTERFIGHT:goldenglow | after A2 |
| TG75 | K L | E AFTERFIGHT:falmer | TG08B running (outside 40..59) |
| TG76 | V P | E CAUGHT | in Riften |
| TG77 | A G | E AFTERFIGHT:summerset | — |
| TG78 | I C | E AFTERFIGHT:skeever | after R13 |
| TG79 | S K | E AFTERFIGHT:riftweald | S following |
| TG80 | R C | E PICKPOCKET | Remi + Redcap scene flag `FA01RemiIntroScene` done (they've met) [UNC] |

## 4. Notes for the build

- **Collisions checked (do not reuse these topics in later files either):**
  - Gore's own TG scenes: can't sneak / "wait behind", reading the bills of sale, regroup after Snow Veil and his guilt, Karliah admiration, "Karliah stole your afterlife", first time before a Daedra (Nocturnal), Guild Master "how's it feel". TG7 only has him admit clanking, consistent with his own line.
  - Kaidan's KMQ TG lines: Goldenglow pun, loves Honningbrew mead, distrusts Mercer, keeps Luna warm after the poison, Daedra/loophole Nightingale line, Vex and Delvin / Vipir rumours. KNPCBrynjolfMercer (Brynjolf's feelings, Mercer's bounty, Vex) and KaiJail (Riften arrest) untouched.
  - Inigo's own: "Nightingale = bird", Nocturnal's robes, Mercer smells fishy, Vex turned him away. Riften jail jokes are overused in other files; TG1 has only a light nod.
  - Val's ValTG storyline: Brynjolf "his type", Vex crush ("Is that jealousy I hear?"), Delvin as an old contact, Maven like his father, Gallus, the Snow Veil door, the Agent of Nocturnal path, waterbreathing ring at Irkngthand, crown gem, sneak/lock/pickpocket training. Nothing here says Val refused or took Nocturnal's deal, or where he was at Snow Veil.
  - Gray Cowl of Nocturnal (Creation Club) is in file 14; nothing here mentions it.
- **Branch-neutral:** no talk says who was at Snow Veil or who carried Luna out. TG_KEY reads the item, so it works if TG Alternative Endings lets her keep the Key. TG_GM excludes the Brynjolf-as-Guild-Master endings.
- **Luna lines:** reactive only; the oath and returning the Key are mandatory story beats, not her choices (TG54's "giving it back" is a joke list, said while the quest requires it).
- Stage directions: only Xelzaz `*Sigh*`. Strip before TTS as usual.
