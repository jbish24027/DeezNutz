# 20b DAWNGUARD 2 - trigger rows (prefix DG, DG121-DG220, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\20b DAWNGUARD 2.txt`.
Sources: `research\content\dlc_cc_missives_3dnpc.md` section A (A2 quest table incl. DLC1RH01-08 / DLC1RV01-10, A3 silence, A4 locations), `research\bibles\serana.md` (3, 6), `research\bibles\ashe.md` (6), and part 1 `triggers\20 DAWNGUARD.md`.
**Everything in part 1's sections 1-3 still applies**: the Serana and Ashe `Free()` rows, the Dawnguard silence list, and every gate code defined there (DG_FREED, DG_HARKON, DG_VAMP, DG_HUNT, DG_NEWORDER, DG_CHALICE, DG_FLORENTIUS, DG_CAIRN, DG_DURN, DG_BOW, DG_END, SER_VAMP, SER_CURED, LUNA_VAMP, VL_BACK, S_ROM_ON/S_ROMOFF/S_COMP/S_KISS/S_LOVE/NOT_S_KISS, A_CRUSH/A_LOVE/A_ANY, ASHE_REVEAL, G_ANY, V_ANY, LOC:Fort, LOC:Volkihar, LOC:Redwater, AFTERFIGHT types). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna.

## 1. New gate codes (this file)

Places:
- `LOC:Dimhollow` = player in Dimhollow Crypt `004EE8:Dawnguard.esm`.
- `DIM_FIRST` = LOC:Dimhollow while DLC1VQ01 (00352A) running and DG_FREED not done.
- `DIM_BACK` = LOC:Dimhollow and DG_FREED (any later visit).
- `REDWATER_LEFT` = event: first controller tick after the player leaves LOC:Redwater (004D6F) having been inside it (controller remembers `VisitedRedwater`). `REDWATER_DONE` = that flag set (for T rows).
- `REDWATER_UP` = in LOC:Redwater and in the upstairs den cell (not the lower Redwater Spring cells) **[UNC: cell IDs; fallback any LOC:Redwater]**.

Fort Dawnguard people:
- `DG_SORINE` = DG_NEWORDER, or DLC1HunterBaseIntro (004E24) stage that sets Sorine recruited **[UNC stage; fallback DG_NEWORDER]**. `DG_GUNMAR` same for Gunmar.
- `DG_RECRUITS` = Celann, Beleval, Durak and Ingjard enabled at the fort. **[UNC: base/ref IDs and the enabling quest not traced; fallback DLC1VQ03Hunter (0098CB) completed]**
- `SORINE_PLANS` = DLC1RH05 "Ancient Technology" completed, or the player knows the Dawnguard crossbow schematics **[UNC: which stage/perk/recipe unlock to test; fallback DG_SORINE + DLC1VQ03Hunter 10]**.
- `DG_TROLLALLY` = the last combat had an allied armoured troll (DLC1TrollArmored* actor in DLC1HunterFaction / player ally, alive) **[UNC]**.

Jobs (radiant, all Dawnguard.esm; FormIDs inside 005E4A...015017 for RH and 004C1B...019938 for RV, **[UNC per-quest IDs]**):
- `RH_RUN:<name>` = `GetQuestRunning` and not completed (stage 10 done, 255 not done). `RH_DONE:<name>` = stage 255 done (RH07 also 300).
  Names: Hide and Seek (RH01), Cleansing Light (RH02), Preemptive Strike (RH03), Hunting the Monster (RH04), Ancient Technology (RH05), Rescue (RH06), A Jarl's Justice (RH07), Lost Relic (RH08). **[UNC: the RH number per name is from the research table order; verify by quest name at build]**
- `RH_COUNT>=3` = at least three RH quests with 255 done (controller counter or sum of GetStageDone).
- `RV_RUN:<name>` / `RV_ANY` = any DLC1RV01-10 running (10 done, 255 and 300 not done). Names: The Hunt (RV01), New Allegiances (RV07), Rings of Blood Magic (RV08), Amulets of Night Power (RV09), Destroying the Dawnguard (RV10). **[UNC numbering as above]**

Arvak / Durnehviir / bow:
- `ARVAK` = player `HasSpell` Summon Arvak (DLC1 spell, **[UNC FormID]**). `E SUMMON_ARVAK` = Arvak actor (base **[UNC]**) enabled within 2000 units of the player (first time for the E rows; T rows need ARVAK).
- `E SUMMON_DURN` = Durnehviir's summoned actor (Tamriel version, **[UNC base; not 0030D8 which is the Soul Cairn one]**) enabled near the player outdoors. First summon = first time the controller sees it.
- `E BOW_DRAW` = player equips DLC1AurielsBow (**[UNC FormID]**) for the first time after DG_BOW.
- `E BOW_SUN` = player fires a sunhallowed or bloodcursed arrow at the sky (the sun-blast / bow-eclipse effect starts) **[UNC: detect via the DLC1 sun-blast explosion or the eclipse imagespace; fallback E AFTERFIGHT:aurielsbow from part 1]**.
- `SUNHALLOWED` = player has Sunhallowed Elven Arrows in inventory **[UNC FormID]**. `BLOODCURSED` = player has Bloodcursed Elven Arrows **[UNC FormID]** (vampire side only; needs Serana's blood).

Vampire Luna:
- `LUNA_HUNGRY` = player vampire stage 3 or 4 (Skyrim.esm `VampireStatus`/stage spell present) **[UNC: which global/spell to test; Requiem may change it]**.
- `VL_BACK2` = VL_BACK but not the first time (2nd+ change back from Vampire Lord).
- `AFTERFIGHT` + `LUNA_VAMP` for DG199.
- `NIGHT_READING` = NIGHT and player not in combat (flavour; any exterior or interior).

Serana cured:
- `SUMMER` = GameMonth 5..7 (TRIGGERS.md seasons). `SUNNY` = exterior, IsPleasant, hour 9..17.

## 2. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| DG121 | R L | E LOC:Dimhollow | DIM_FIRST |
| DG122 | L K P | E LOC:Dimhollow | DIM_FIRST; after DG121 or 2nd Dimhollow tick |
| DG123 | S G | E LOC:Dimhollow | DIM_BACK; S following |
| DG124 | C S | E LOC:Dimhollow | DIM_BACK; S following; after DG8 |
| DG125 | V K P | E LOC:Dimhollow | DIM_BACK |
| DG126 | R V | E LOC:Fort | DG_HUNT; DG_SORINE |
| DG127 | V P | T | DG_HUNT; SORINE_PLANS |
| DG128 | R G | E LOC:Fort | DG_HUNT; DG_SORINE; after DG11 |
| DG129 | G K | E LOC:Fort | DG_HUNT; DG_GUNMAR |
| DG130 | I X | E LOC:Fort | DG_HUNT; DG_GUNMAR |
| DG131 | C K | E LOC:Fort | DG_HUNT; DG_GUNMAR; after DG10 |
| DG132 | R P | T | DG_HUNT; DG_FLORENTIUS |
| DG133 | X L | T or E LOC:Fort | DG_HUNT; DG_FLORENTIUS |
| DG134 | L P | T | DG_HUNT; DG_FLORENTIUS |
| DG135 | G I | E LOC:Fort | DG_HUNT; after DG18 |
| DG136 | K P | E LOC:Fort | DG_HUNT; any RH_DONE |
| DG137 | L C | E LOC:Fort | DG_HUNT; DG_RECRUITS |
| DG138 | G R | E LOC:Fort | DG_HUNT; DG_RECRUITS |
| DG139 | V K | E LOC:Fort | DG_HUNT; DG_RECRUITS (any romance stage; line is neutral) |
| DG140 | X K P | E LOC:Fort (evening, hour >= 17) | DG_HUNT; after DG130 |
| DG141 | A R | E LOC:Fort | DG_HUNT; DG_SORINE; ASHE_REVEAL |
| DG142 | V L | E CITY (any) | RH_RUN:Hide and Seek |
| DG143 | K P | T | RH_RUN:Cleansing Light |
| DG144 | G C | T | RH_RUN:Preemptive Strike |
| DG145 | I R | T | RH_RUN:Hunting the Monster |
| DG146 | R V P | T or E DWEMER | RH_RUN:Ancient Technology |
| DG147 | G L | T | RH_DONE:Rescue |
| DG148 | X P | T | RH_RUN:A Jarl's Justice |
| DG149 | V I | T | RH_RUN:Lost Relic |
| DG150 | V K P | T or E LOC:Fort | DG_HUNT; RH_COUNT>=3 |
| DG151 | V P | E LOC:Volkihar | DG_VAMP |
| DG152 | G K | E LOC:Volkihar | DG_VAMP |
| DG153 | C I | E LOC:Volkihar | DG_VAMP |
| DG154 | I S | E LOC:Volkihar | DG_VAMP; DG_CHALICE; S following |
| DG155 | R X | E LOC:Volkihar | DG_VAMP; Remi/Xel not fallen out (TRIGGERS.md 3) |
| DG156 | L P | E LOC:Volkihar | DG_VAMP |
| DG157 | V X | E LOC:Volkihar | DG_VAMP |
| DG158 | S K | E LOC:Volkihar | DG_VAMP; S following |
| DG159 | L S | E LOC:Volkihar | DG_VAMP; S following |
| DG160 | S G | T or E LOC:Volkihar | DG_VAMP; DG_END; S following |
| DG161 | K P | E LOC:Volkihar | DG_VAMP; DG_END |
| DG162 | L P | T | RV_RUN:New Allegiances |
| DG163 | R V | T | RV_RUN:Destroying the Dawnguard; after DG128 or DG11 |
| DG164 | V X | T | RV_RUN:Rings of Blood Magic |
| DG165 | R C | T | RV_RUN:Amulets of Night Power |
| DG166 | G I | T | DG_VAMP; RV_ANY |
| DG167 | S P | T | DG_VAMP; RV_ANY; S following |
| DG168 | I K | T | RV_RUN:The Hunt |
| DG169 | I R | E LOC:Redwater | first visit |
| DG170 | I L | E LOC:Redwater | REDWATER_UP; after DG169 or DG24 |
| DG171 | I P | E REDWATER_LEFT | first exit (priority 1 on the event) |
| DG172 | I S | T | REDWATER_DONE; DG_CHALICE; S following |
| DG173 | X I | E REDWATER_LEFT or T | REDWATER_DONE; after DG171 |
| DG174 | K I | E NIGHT (CAMP or INN) | REDWATER_DONE; after DG24 |
| DG175 | I P | E SUMMON_ARVAK | ARVAK (first summon) |
| DG176 | G C | E SUMMON_ARVAK or T | ARVAK |
| DG177 | K S | T | ARVAK; S following |
| DG178 | X R | T | ARVAK; Remi/Xel not fallen out |
| DG179 | C L P | E SUMMON_DURN | DG_DURN; after DG46 |
| DG180 | K G | E SUMMON_DURN or T | DG_DURN; after DG47 and one summon seen |
| DG181 | X P | E SUMMON_DURN or T | DG_DURN; one summon seen |
| DG182 | V S | T | DG_DURN; one summon seen; after DG48; S following |
| DG183 | A I | T | DG_DURN; one summon seen; ASHE_REVEAL |
| DG184 | K P | E BOW_DRAW | DG_BOW |
| DG185 | V G | E BOW_SUN | DG_BOW |
| DG186 | S P | T | DG_BOW; SUNHALLOWED; SER_VAMP; S following |
| DG187 | G S | T | DG_BOW; DG_VAMP; BLOODCURSED; S following |
| DG188 | R I | T | DG_BOW |
| DG189 | C P | T | LUNA_VAMP |
| DG190 | R P | T | LUNA_VAMP |
| DG191 | K L | T | LUNA_VAMP; LUNA_HUNGRY |
| DG192 | S P | T | LUNA_VAMP; S following |
| DG193 | V P | E NIGHT_READING | LUNA_VAMP |
| DG194 | X P | T | LUNA_VAMP |
| DG195 | I G | T | LUNA_VAMP |
| DG196 | A P | E CAMP or INN | LUNA_VAMP; ASHE_REVEAL |
| DG197 | R C | E VL_BACK2 | DG_VAMP |
| DG198 | K P | T | LUNA_VAMP; K_TOG+ |
| DG199 | L V | E AFTERFIGHT | LUNA_VAMP |
| DG200 | G S | T | SER_CURED |
| DG201 | C S | E exterior + SUMMER | SER_CURED |
| DG202 | X S | T | SER_CURED |
| DG203 | S P | T | SER_CURED |
| DG204 | R S | T | SER_CURED |
| DG205 | S V | E AFTERFIGHT | SER_CURED |
| DG206 | L S | E INN | SER_CURED |
| DG207 | K S | E SUNNY | SER_CURED; after DG3 |
| DG208 | K S P | T | K_CRUSH; S_COMP; NOT_S_KISS |
| DG209 | G S | T | G_FLIRT; S_COMP; NOT_S_KISS |
| DG210 | V S | T or E LOC:Jetty / LOC:Volkihar | S_KISS; V_ANY; not S_LOVE |
| DG211 | A S | T | S_KISS; A_ANY; ASHE_REVEAL; not S_LOVE |
| DG212 | S K | T | S_KISS; K_TOG+; not S_LOVE; after DG101 |
| DG213 | G K | T | S_KISS; K_ANY; G_ANY |
| DG214 | S V C | T | S_ROMOFF; K_CRUSH |
| DG215 | S K P | E SNOW exterior | S_KISS; K_TOG+ |
| DG216 | G S | T | LUNA_VAMP; S_COMP; SER_VAMP; G_ANY |
| DG217 | C G | E AFTERFIGHT | DG_HUNT; DG_TROLLALLY; after DG131 |
| DG218 | V R | E AFTERFIGHT:vampire | — |
| DG219 | R P | E AFTERFIGHT:dawnguard | DG_VAMP; after DG11 or DG126 |
| DG220 | C X | E AFTERFIGHT:gargoyle | — |

## 3. Notes for the build
- Side split: Dawnguard-side rows carry DG_HUNT; vampire-side rows carry DG_VAMP. RH/RV job rows are side-exclusive by nature (the quests only run on their side).
- Job rows fire only while the job is running (or right after, for RH_DONE:Rescue). One job talk per job instance; never repeat when the same radiant quest restarts.
- DG171 is the priority event on REDWATER_LEFT; DG173 only takes the event if DG171 already played, else it waits for the timer.
- DG208 keeps Luna oblivious (K_CRUSH): her line is about books only. DG215: Luna refuses both helpers equally. No Luna romance line anywhere in Part 12.
- DG214 has no Luna line and must never fire with Luna in dialogue; it is a bet between three followers about Kaidan's crush (K_CRUSH only, so it retires once she notices).
- Durnehviir summons only work outdoors; SUMMON_DURN rows are exterior by nature.
- No "Dragonborn" in the file. No Kaidan cult reference. Kaidan uses no pet names in ungated rows.
- Existing coverage avoided (checked): part 1 DG1-DG120; PA236/PA257 (Soul Tear, first Arvak summon with Lucien/Clive); PA103/PA104 (Vampire Lord form, feeding); RIVALRY RV-series Serana topics; FL161-FL179 (cure aftermath, Valerica visits); PY281/PY386/PY422 (cured Serana's cold, first sunrise); NP70 (Remi + Arkay consecration); the CC crossbow and skooma talks.
