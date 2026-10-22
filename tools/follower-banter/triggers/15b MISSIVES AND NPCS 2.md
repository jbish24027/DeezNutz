# Triggers - 15b MISSIVES AND NPCS 2 (prefix MN, MN131-MN250, 120 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\15b MISSIVES AND NPCS 2.txt`
Part 1 (gate vocabulary and silence zones this file reuses): `triggers\15 MISSIVES BOUNTIES INTERESTING NPCS.md`.
Research: `research\content\dlc_cc_missives_3dnpc.md` sections E and F, plus a read-only houseCARL pass 2026-10-18 (epoch e2-509d9856becc0652): every `_M_Quest*` / `_ME_Quest*` EditorID in Missives.esp, Missives - Solstheim.esp, Missives - Wyrmstooth.esp, Missives - Heartland.esp, Missives - Gray Cowl Patch.esp and MissivesExpansion.esp; Bounties Redone objective text (BQ01-04 and the Kill* families); 3DNPC.esp quest names and objective text for 55 quests not used in part 1.

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C), plus **U = Luna** (player line, Eleonora voice; no Free() test), **S = Serana**, **A = Ashe**.

## Gate codes added in this file

Everything in file 15's "New gate codes" section applies (`MS_BOARD`, `MS_BOARD:<Hold>`, `MS_RUN:<Type>`, `MS_DONE[:<Type>]`, `MS_COUNT`, `BQ_DONE:<n>`, `BOUNTY_DONE`, `Done(Q,s)`, `Comp(Q)`, `KAI_INIGO`). Families are now **confirmed** from the EditorIDs; the substring after the region names the family:

| Family substring | Board name | Plugins |
|---|---|---|
| `CourierLetter{Low,Med,High}` / `CourierWeapon*` / `CourierPotion{Low,Med,High}` | Deliver a letter / weapon / potion, Near / Medium / Distant or Far | all regions |
| `GatherIngr{Low,Med,High}` | Common / Uncommon / Rare ingredients | all |
| `GatherOre{Low,Med,High,VeryHigh}` | Common ... Very Rare ore | all |
| `GatherSoulGem{Low,Med,High}` | Weak / Standard gems; High = "Find a Powerful Soul Gem" | all |
| `GatherInn` | Collect Some Food | all |
| `KillAnimal` | Kill Some Things | all |
| `KillBandit`, `KillGiant`, `KillDragon`, `KillForsworn` (Reach) | bounties (Bounties Redone overrides) | Missives, Solstheim, Wyrmstooth, Heartland, Alik'r |
| `KillRieklings` | Solstheim only | Missives - Solstheim |
| `KillOgre` | Bruma only | Missives - Heartland |
| `RetrieveHideout`, `RetrieveRuins`, `RetrieveWilderness` | recover jobs | all |
| `TrackThief`, `TrackFugitive`, `TrackVampire` | tracking | Missives (Skyrim holds) |
| `_ME_Quest*` `FindBook{Common,Uncommon,Rare}`, `Find{Apprentice,Adept,Expert}Tome`, `Find{Common,Rare}Accessory`, `CatchFish`, `FindToy`, `SolstheimItem`, `GatherFirewood`, `GatherNordMead`, `GatherSteelSwords`, `FindDwemerRarity`, `KillUndead`, `FindTheDog`, `FindTheGoat`, `KillPests`, `HealTheSick` | expansion jobs (the live quest is `_ME_QuestWhiterun<Family>`; the `...Location` / `...Board` quests are helpers, ignore them) | MissivesExpansion |

Regions: Whiterun, Eastmarch, Falkreath, Haafingar, Hjaalmarch, Pale, Reach, Rift, Winterhold (Missives.esp), Solstheim, Wyrmstooth, Bruma (Heartland), AlikrBasin (Gray Cowl Patch).

New codes:
- `MS_RUN:<Region><Family>` / `MS_DONE:<Region><Family>` = the family limited to that region's quests (e.g. `MS_DONE:WyrmstoothKillBandit`).
- `BR_CAPTURE` = the bounty quest's "Bring the captured ... to a guard" objective is shown/completed (Bounties Redone capture branch). **[UNCONFIRMED objective index; read the BountiesRedone fragments at build]**
- `BR_HEAD` = the "Take the head ... as proof" objective completed. `BR_SKULL` = the "Take the dragon's skull as proof" objective completed. `BR_GIANT_LEFT` = BQ03 / `*KillGiant` completed with the giant alive ("convince him to leave" / "scare away"). **[UNCONFIRMED: detect with giant ref IsDead == 0 at stage 100]**
- `BR_STEWARD_OR_JARL` = the "Collect bounty from <Steward/Jarl>" objective is the active one, player in dialogue range.
- `SERANA_F` = SERANA gate (DLC1VQ02 done) and `DLC1NPCMentalModel ::IsFollowing_var == 1`. `SERANA_VAMP` = Serana HasKeyword Vampire == 1. `SOULCAIRN` = Comp(DLC1VQ05).
- `ASHE_F` = Ashe hired (MM_AsheIntro completed) and following **[UNCONFIRMED follow test, see research\bibles\ashe.md section 6]**. `ASHE_REVEAL` = MM_FriendshipQuest var `MM_AutomatonReveal == 1`. Ashe talks without ASHE_REVEAL never mention what she is.
- `GORE_READS` = HLIOGoreReading (6F46A0:HLIORemi.esp) >= 1 (Remi's reading lessons started).
- `KINV_NOT_DONE` = Kaidan's Akaviri cache quest KINV not completed (MN223 says his mother's past is still a question).
- `CYRODIIL_BRUMA` = player in the Bruma map (Beyond Skyrim Bruma worldspace). `ALIKR` = player in the Gray Cowl Alik'r worldspace **[UNCONFIRMED worldspace EditorID; MN164 only plays if that region exists]**.
- `RR_OWNED` = robbersrefuge3dnpc 1F5362 objective 80 "Talk to Ortheim About Modifying the Tavern" shown or later **[UNCONFIRMED stage ~80]**.

Silence zones: as file 15 (3DNPCMQ7 20..50, Viola's party scenes, warrensquest 80..90 / 300..370, DJGQuest2 100..130, AsteriaQuest 80..90). Add: `AmaleeQuest` 25 (the bard duel itself) and `ErevanQuest` 85 while the Kynesgrove defence fight runs (combat gate covers most of it).

## Table

### Part 1 - Missives and bounties
| ID | Speakers | Type | Gates |
|---|---|---|---|
| MN131 | X G U | T | MS_RUN:GatherFirewood |
| MN132 | C I | T | MS_RUN:FindTheGoat |
| MN133 | R V | T | MS_RUN:FindDwemerRarity |
| MN134 | L I U | E CRYPT | MS_RUN:KillUndead |
| MN135 | X G | E MS_DONE:KillPests | after X1 |
| MN136 | I V | T | MS_RUN:CourierPotionHigh (any region); after I1 |
| MN137 | R K U | T | MS_RUN:FindRareAccessory or FindCommonAccessory; K_CRUSH |
| MN138 | L X | T | MS_RUN:GatherSoulGemLow |
| MN139 | S U | T | MS_RUN:GatherSoulGemHigh; SERANA_F; SOULCAIRN |
| MN140 | G A | T | MS_RUN:GatherOreVeryHigh; ASHE_F |
| MN141 | X U | T | MS_RUN:GatherIngrLow |
| MN142 | K C | E exterior | MS_RUN:RetrieveWilderness; after R1 |
| MN143 | I U | T | MS_RUN:HealTheSick |
| MN144 | C V | T | MS_RUN:SolstheimItem; after R8 |
| MN145 | L U | T | MS_RUN:FindExpertTome (or FindAdeptTome) |
| MN146 | G U | T | MS_RUN:FindApprenticeTome; GORE_READS |
| MN147 | K G U | E BOUNTY_DONE with BR_CAPTURE | after MN13 |
| MN148 | K V | E BOUNTY_DONE with BR_HEAD | after MN13; after A2 |
| MN149 | G C U | E BQ_DONE:03 or MS_DONE:KillGiant with BR_GIANT_LEFT | after R5 |
| MN150 | L U | E BQ_DONE:04 or MS_DONE:KillDragon with BR_SKULL | DB |
| MN151 | V R | E BR_STEWARD_OR_JARL | — |
| MN152 | I K | T | BR_CAPTURE objective active (prisoner escorted); KAI_INIGO |
| MN153 | K A | E BOUNTY_DONE | ASHE_F; after MN13 |
| MN154 | X G | E SNOW | MS_RUN:WinterholdKillBandit; after X1 |
| MN155 | K X | E BOUNTY_DONE | BQ_DONE:02 or MS_DONE:ReachKillForsworn, with BR_CAPTURE; after C3 |
| MN156 | I R | E BOUNTY_DONE | player in RiftHoldLocation; after B6 |
| MN157 | C X | E MS_DONE:SolstheimKillDragon | DB; SOLST |
| MN158 | K C U | E exterior | MS_RUN:SolstheimCourier* (any); SOLST; after R1 |
| MN159 | V G | E MS_DONE:WyrmstoothKillBandit | BR_CAPTURE; after A3 |
| MN160 | K L U | E MS_DONE:WyrmstoothKillDragon | DB |
| MN161 | G K | E MS_BOARD | CYRODIIL_BRUMA; after A1 |
| MN162 | C I | E MS_DONE:BrumaKillOgre | after R13 |
| MN163 | L V | T | MS_RUN:BrumaCourier* (any); after C1 |
| MN164 | G K | E MS_BOARD | ALIKR [CHECK]; after A1 |
| MN165 | L C A | E MS_DONE | after MN1; ASHE_F |
| MN166 | C L U | E MS_DONE | after MN48 |
| MN167 | L G | E MS_DONE:KillPests (or KillAnimal in an interior) | after MN1 |
| MN168 | L R | E CAMP | after MN48; MS_COUNT >= 15 |
| MN169 | S L | E MS_DONE | after MN1; SERANA_F |
| MN170 | L I U | E MS_DONE | after MN48; MS_COUNT >= 100 (or the build's highest tracked count, see note) |
| MN171 | V G | E MS_DONE | after MN30 |
| MN172 | V U | E MS_DONE | after MN30 |
| MN173 | V C | E MS_DONE | after MN29; after R8 |
| MN174 | L V | E CAMP | after MN30; MS_COUNT >= 12 |
| MN175 | V G U | E MS_DONE | after MN31 and MN171 |
| MN176 | U K | E CAMP | after MN49 and MN147; BRYNJAR |
| MN177 | G K | E CAMP | after MN49; GORE_READS |
| MN178 | K I | E exterior after BOUNTY_DONE | BRYNJAR; KAI_INIGO |
| MN179 | X K | E BOUNTY_DONE | after MN13; after C3 |
| MN180 | R I | E CITY (any town with a board) | after B6 |
| MN181 | A G | E MS_BOARD | ASHE_F; GORE_READS |
| MN182 | S K | T | MS_RUN:TrackVampire; SERANA_F; SERANA_VAMP |
| MN183 | K V U | E MS_BOARD | K_CRUSH; after A2 |
| MN184 | X I | E MS_DONE | after X6 [UNCONFIRMED: no "paid in food" flag exists; fire on any MS_DONE:GatherInn or KillAnimal on a farm, or drop the condition] |
| MN185 | L K | E MS_BOARD + RAIN | Kaidan-Lucien intro done |
| MN186 | U K G | E MS_RUN:Courier*Low (just taken) | K_TOG+ |
| MN187 | U X | E MS_DONE | MS_COUNT >= 5 |
| MN188 | R L | E CRYPT | MS_RUN:RetrieveRuins; after B10 |
| MN189 | G I | E exterior, dusk (hour 18..20) | any MS_RUN:Courier*; after C2 |
| MN190 | V C | E MS_BOARD + NIGHT | after R8 |

### Part 2 - Interesting NPCs (all quest FormIDs `:3DNPC.esp`)
Most of these quests write no journal text; stages below are the **objective indexes** read from the records (objective index = the stage that shows it, by 3DNPC's usual pattern) and are marked [UNCONFIRMED stage] where that pattern was not proven.

| ID | Speakers | Type | Gates |
|---|---|---|---|
| MN191 | L U | T | DialogueJasparGaerston 025759 Done 17; not Done 30 [UNCONFIRMED stage] |
| MN192 | R V | E in Winking Skeever (Solitude) | DialogueJasparGaerston Done 25, not Done 30 |
| MN193 | G L | T | DialogueJasparGaerston Done 40; after L1 |
| MN194 | V U | T | DialogueJasparGaerston Done 80 or completed |
| MN195 | U L | T | Cassockquest 23D691 Done 40, not Done 60 (four names in) [UNCONFIRMED stage] [CHECK: lines don't claim who is behind it] |
| MN196 | G K | T | Comp(Cassockquest) (Uvra dead, objective 90); after A1 |
| MN197 | V X | T | Herranquest 24CEAA Done 20; after X4 |
| MN198 | I U | E in Winterfrost Cottage | Herranquest Done 60, not Done 80 |
| MN199 | R V | T | PaintingQuest 271DB3 Done 40 |
| MN200 | G L | T | Comp(PaintingQuest) or PaintingQuest_Post 272FA0 running; after L1 |
| MN201 | G X | T | DialogueDaenlyn 274031 Done 40 (lute retrieved); after X1 |
| MN202 | C I | T | DialogueMithrilan 2C904D running, not completed; after R13 |
| MN203 | K L U | T | DialogueThriceBitten 27CF33 Done 12 (race won) [UNCONFIRMED: race-won flag vs race-lost] |
| MN204 | R X | T | DialogueThriceBitten Done 50; Remi/Xelzaz not fallen out |
| MN205 | I G | T | DialogueCassius 28CDD8 Done 20 or completed; after C2 |
| MN206 | X V | T | MorndasArgonianQuest 29844E Done 40; after X4 |
| MN207 | U L | T | DialogueAzzarian 29BB83 Done 46, not Done 40-complete (safe not yet open) [UNCONFIRMED: objectives 40/46 order] |
| MN208 | R K | T | Comp(DialogueAzzarian); after B1 |
| MN209 | G U | E in Dawnstar Barracks | Arielequest 306C12 Done 40 shown, not Done 45; GORE_BAIL |
| MN210 | X V | E WATER | DialogueTreads 312F72 running; after X4 |
| MN211 | R U | T | TerynneQuest 377D79 Done 30 (tome found), not Done 70 |
| MN212 | G V U | T | robbersrefuge3dnpc 1F5362 Done 60 (tavern cleared); after A3 |
| MN213 | R K | T | RR_OWNED; after B1 |
| MN214 | X I | E in Robber's Refuge | RobbersRefugeSevenSeptimSingAlong 2BA8E4 running; after X6 |
| MN215 | I G | E near the shrine | DialogueMeresine 25EABA Done 1, not Done 20; after C2 |
| MN216 | C X | E arrival at the cottage | hagquest 1D094E Done 10, not Done 20; after R18 |
| MN217 | G L | T | Comp(hagquest) (branch-neutral); after L1 |
| MN218 | A L | E exterior, escort active | HagCurseQuest 2F282F Done 50 shown, quest not completed; ASHE_F |
| MN219 | V R | E in the Bannered Mare | hwsquest 219068 Done 15 |
| MN220 | K U | T | Comp(hwsquest) (objective 80 done) |
| MN221 | G K | T | DialogueJilkmar 20EE6C Done 10, not Done 30; after A1 |
| MN222 | X U | T | DialogueJilkmar Done 45 |
| MN223 | K U | T | VartheimQuest 18A9BD Done 10 (sword returned to Pelgurt); BRYNJAR; KINV_NOT_DONE |
| MN224 | V G | T | VartheimQuest Done 50; after A3 |
| MN225 | L C | T | Comp(Notice3DNPC 235909); after MN1; after R11 |
| MN226 | L X | T | DialogueYtharil 0CB644 Done 10 (camp found), not Done 20-complete |
| MN227 | V R | E CITY:Riften | DialogueSkjel 0D54B6 Done 10 |
| MN228 | R G | T | skjelquest 2BB973 Done 60 (necromancer altar) |
| MN229 | G V | T | AmaleeQuest 16E34D Done 50 (after the duel at 25); after A3 |
| MN230 | V U | T | AmaleeQuest Done 70 or 80 |
| MN231 | G K | E exterior | ErevanQuest 182E37 Done 80 shown, not Done 85; after A1 |
| MN232 | I U | T | Comp(ErevanQuest) |
| MN233 | X L | T | Comp(DialogueRaynes 09F11B) (Falmer cave cleared, objective 20 done); Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| MN234 | G R | T | Comp(DialogueGriffith 066092 "Runaways") [CHECK: the squatters' story not read; lines say "runaways"] |
| MN235 | G K | T | DialogueBrakh 0C2D72 Done 50 (Lagdu tracked) or completed; BRYNJAR |
| MN236 | I L | T | dialoguemorviah 070058 Done 4 (flower left) or completed |
| MN237 | L U | T | Comp(DialogueIorel 087EFD) [CHECK: only "Kill Iorel" objective read; lines say she was already undead/ancient] |
| MN238 | S X | T | Comp(DialogueSalumEi 09A517) [CHECK: Boulderfall vampire story not read]; SERANA_F |
| MN239 | I X | T | DialogueAnumla 0294CA Done 6 or later (marsh noises investigated); after X6 |
| MN240 | R L | E in Mzinchaleft | Mzinchaleft3DNPC 2AB582 Done 10 [CHECK]; after B10 |
| MN241 | X V | T | Mzinchaleft3DNPC Done 26 [CHECK]; after X4 |
| MN242 | A R | E DWEMER | ASHE_F; ASHE_REVEAL; MS_RUN:FindDwemerRarity or in Mzinchaleft |
| MN243 | S U | T | Comp(CarmellaSkjarnQuest 2A993F) (branch-neutral); SERANA_F; SOULCAIRN |
| MN244 | V R | T | Comp(DialogueGeelJah 28C7E2 "Treasure Hunters") [CHECK: story not read; no objectives in record] |
| MN245 | G K U | T | Comp(3DNPCMQ7 1B462D) + 3 game days; after MN55 |
| MN246 | C I | T | two of: Done(GorrQuest,81), Done(warrensquest,370), Comp(DialogueCassius); after MN86 and MN205 |
| MN247 | L U | E CAMP | after MN170; at least three 3DNPC quests completed |
| MN248 | R K U | T | any 3DNPC rescue quest completed (warrensquest, GorrQuest, DialogueCassius, ErevanQuest); K_TOG+; after B1 |
| MN249 | X G | E in Robber's Refuge, bard playing | RR_OWNED; after MN212 |
| MN250 | L C U | E CAMP + NIGHT | after MN170; at least two MS_DONE this game day |

## Notes for build
- MN170 wants a hundredth job. If the controller can't count that high cheaply, use the largest MS_COUNT it tracks (e.g. 50) and keep the line "one hundred" as a round boast.
- Bounties Redone capture/head/skull objectives: map each objective index to its stage in BountiesRedone_MissivesExtension.esp, _Missives_Solstheim and _Missives_Wyrmstooth before wiring BR_CAPTURE / BR_HEAD / BR_SKULL.
- MN164 (Alik'r) and the Bruma talks only fire where those worldspaces exist.
- [CHECK] talks (MN195, MN234, MN237, MN238, MN240, MN241, MN244) lean on quest names and objective text only.
- Ashe talks MN140, MN153, MN165, MN181, MN218 are written to be safe before her reveal; MN242 needs ASHE_REVEAL.
