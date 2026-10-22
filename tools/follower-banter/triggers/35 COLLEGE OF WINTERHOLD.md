# 35 COLLEGE OF WINTERHOLD - trigger rows (prefix MG, 70 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\35 COLLEGE OF WINTERHOLD.txt`.
Sources: `research\triggers\vanilla_gates.md` (B1, B3), `research\bibles\*.md` (val.md section 1 item 6 for ValCOL / ValCOLGrad; serana.md 6; ashe.md 3 + 6), TRIGGERS.md sections 2-4, `triggers\20 DAWNGUARD.md` (Serana / Ashe Free rows and S_/A_ codes).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana and Ashe Free rows in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).

## 1. College silence (add to WorldQuiet)

- MG05 (01F255:Skyrim.esm) stage 20..49 (Revealing the Unseen: the Mzulft / Oculory stretch). [CONFIRMED, vanilla_gates B3]
- MG08 (01F258:Skyrim.esm) stage 10..199 (The Eye of Magnus: from Mirabelle's call to Arch-Mage). [CONFIRMED, vanilla_gates B3]
- Ancano scenes: any MG quest scene with Ancano as an actor running (`Ancano.IsInScene() == 1`; Ancano ref from Skyrim.esm **[UNC FormID]**). Also MG06 (01F256 **[UNC]**) running and player in the Hall of the Elements (Ancano's barrier / Savos's death).
- MG02 (01F252 **[UNC]**) Psijic time-stop in Saarthal: while Quaranir is in a scene (`IsInScene` on his ref **[UNC FormID]**) or MG02 stage of the vision **[UNC stage]**.
- `Authoria - Master Patch - AYOP CoW.esp` wins MG01-MG04 and MG08 and keeps the vanilla stage numbers (vanilla_gates B1 / note 6). At Your Own Pace delays the College chain, so never assume one MG quest follows another quickly: every story talk below uses a "done" gate, not a time offset.

## 2. Gate codes used in this file (new)

Story (Skyrim.esm; MG01/MG05/MG08 FormIDs confirmed, the others follow the 01F251..01F258 run **[UNC]**):
- `MG_JOIN` (existing) = MG01 (01F251) stage 30 done.
- `MG_LESSON` = MG01 completed (First Lessons, Tolfdir's ward lesson). **[UNC completion stage]**
- `MG_SAARTHAL` = MG02 (01F252) completed (Under Saarthal; Eye found, Psijic spoke).
- `MG_BOOKS` = MG03 (01F253) completed (Hitting the Books; Orthorn / Fellglow Keep).
- `MG_AUGUR` = MG04 (01F254) started and stage 10 done (Ancano asks you to see the Augur). **[UNC stage]**
- `EYE_HERE` = MG_SAARTHAL and MG06 not started and MG08 not completed (the Eye sits in the Hall of the Elements). **[UNC: stage the Eye appears in the Hall]**
- `MG_SAVOS` = MG06 (01F256) completed (Containment; Savos Aren dead). Alt: Savos Aren ref `GetDead == 1` **[UNC FormID]**.
- `MG_STAFF` = MG07 (01F257) completed (The Staff of Magnus).
- `STAFF_CARRIED` = MG_STAFF done and MG08 stage < 10 (staff found, final fight not started).
- `ARCH` (existing) = MG08 stage 200 done. Mirabelle and Ancano are dead; the Psijics have taken the Eye.
- `ANCANO_ALIVE` = MG08 not completed. `MIRABELLE_ALIVE` = MG08 stage < 10. `SAVOS_ALIVE` = MG06 not completed.

College side quests (Skyrim.esm; EditorIDs/FormIDs to look up at build **[UNC all]**):
- `MGR_JZARGO` = "J'zargo's Experiment" completed.
- `MGR_BRELYNA` = "Brelyna's Practice" completed.
- `MGR_ONMUND` = "Onmund's Request" completed.
- `MGR_ARNIEL` = "Arniel's Endeavor" final part completed (Arniel vanished).

Follower / other mods:
- `VAL_COL` = Val's own College quest ValCOL started (he has enrolled). **[UNC: FormID and enrol stage in AX ValSerano.esp]**
- `VAL_GRAD` = ValCOLGrad completed (he has graduated). **[UNC FormID]**
- `GORE_READING` = `HLIOGoreReading (6F46A0:HLIORemi.esp) >= 1` (Remi's reading lessons started). **[UNC value meaning]**
- `INIGO_BV` (existing) = InigoBadVibrations completed (Langley known).
- `ASHE_HIRED` = MM_AsheIntro (0A7946:Ashe - Fire and Blood.esp) completed. `ASHE_REVEAL`, `ASHE_Q1`, `A_CRUSH` as in `20 DAWNGUARD.md` section 3.
- `S_COMP` as in `20 DAWNGUARD.md` section 3 (Serana romance on and "travelling companion" reached). `SERANA` (existing) for any Serana talk.
- `AFTER Q18` = Quests talk Q18 ("A Telvanni Takes a Room") has played.

Places (`E LOC:<name>` = arrival, first time unless the row says otherwise; location / cell FormIDs from Skyrim.esm **[UNC all]**):
- `LOC:Winterhold` WinterholdLocation (town exterior + its interiors). `LOC:Longhouse` the Jarl's Longhouse. 
- `LOC:Bridge` = exterior, inside the College bridge trigger area (between Faralda's gate and the courtyard) **[UNC: no keyword; use a distance check to the bridge gate marker]**.
- `LOC:College` CollegeOfWinterholdLocation and its children (Hall of the Elements, Hall of Attainment, Hall of Countenance, Arcanaeum). `LOC:Arcanaeum`, `LOC:Elements`, `LOC:Midden` (the Midden + Midden Dark), `LOC:ArchQuarters` (Arch-Mage's Quarters).
- `LOC:Saarthal`, `LOC:Mzulft`, `LOC:Labyrinthian`.
- `NEAR:<npc>` = that NPC's ref within 1500 units of the player (Colette, Ancano, Atronach Forge activator) **[UNC FormIDs]**. Used where the talk is about meeting someone; there is no vanilla "met" flag, so "after you've met X" = MG_JOIN and the NPC has been NEAR once (controller remembers).

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| MG1 | K G P | E LOC:Winterhold | first visit |
| MG2 | I G | E LOC:Winterhold | after MG1 (a later visit) |
| MG3 | X K | E LOC:Longhouse | — |
| MG4 | I C | E LOC:Bridge | first crossing with Redcap following |
| MG5 | K P | T or E LOC:Bridge | MG_JOIN; K_CRUSH |
| MG6 | S G P | E LOC:Winterhold | SERANA; S following |
| MG7 | L A | E LOC:Winterhold | ASHE_HIRED |
| MG8 | G K P | E LOC:Arcanaeum | first visit |
| MG9 | C G | E LOC:Arcanaeum | after MG8 or first visit with Redcap |
| MG10 | X P | E LOC:Arcanaeum | — |
| MG11 | G R P | E LOC:Arcanaeum | GORE_READING; after MG8 |
| MG12 | V I P | T | MG_JOIN; player has been in LOC:Arcanaeum [UNC: "bought from Urag" = flavour, no check] |
| MG13 | R L P | E LOC:Arcanaeum | — |
| MG14 | K P | E LOC:Arcanaeum | after MG8 (a later visit) |
| MG15 | S X | T | MG_BOOKS; S following |
| MG16 | I K | E LOC:College | MG_JOIN; INIGO_BV |
| MG17 | G K | T | MG_LESSON |
| MG18 | G V | E LOC:College | MIRABELLE_ALIVE; MG_JOIN |
| MG19 | G P | T | ARCH; after MG18 |
| MG20 | C P | E LOC:College + NEAR:Colette | after MG38 |
| MG21 | K R | E LOC:College | MG_JOIN; NEAR:Colette seen once |
| MG22 | C L | E LOC:College | MG_JOIN |
| MG23 | K P | E LOC:College | MG_JOIN; NEAR:Faralda seen once |
| MG24 | I C | E LOC:College | MG_JOIN; after MG38 |
| MG25 | X V | E LOC:College | MG_JOIN; SAVOS_ALIVE |
| MG26 | I K | E LOC:College | MG_JOIN |
| MG27 | G R | T | MGR_JZARGO |
| MG28 | V P | T | ARCH; after MG26 |
| MG29 | X V | E LOC:College | MG_JOIN |
| MG30 | K P | T | MGR_BRELYNA |
| MG31 | K V | T | MGR_ONMUND |
| MG32 | R V | E LOC:College | MG_JOIN |
| MG33 | R L | E LOC:College | MG_JOIN; MGR_ARNIEL not done |
| MG34 | R L P | T | MGR_ARNIEL; after MG33 |
| MG35 | G K P | E LOC:College | after MG8 |
| MG36 | K I | T | MG_JOIN; K_CRUSH |
| MG37 | K P | E LOC:College | K_TOG+ |
| MG38 | C I P | E LOC:College | first visit with Redcap following |
| MG39 | X L | T | MG_JOIN |
| MG40 | S X P | E LOC:College | SERANA; S following |
| MG41 | A R P | E LOC:College | ASHE_REVEAL; MG_JOIN |
| MG42 | I V | T | MG_JOIN |
| MG43 | G V | T | VAL_COL; VAL_GRAD not done |
| MG44 | V K | T | VAL_GRAD |
| MG45 | A X | E LOC:Midden + NEAR:Atronach Forge | ASHE_REVEAL |
| MG46 | G K P | E LOC:Saarthal | first visit |
| MG47 | L K P | T | MG_SAARTHAL |
| MG48 | L R P | T | EYE_HERE |
| MG49 | R K | E LOC:Elements | EYE_HERE; MG_AUGUR [UNC: Eye placement stage] |
| MG50 | S L | T | MG_SAARTHAL; S following |
| MG51 | X V | T | MG_SAVOS; after MG25 |
| MG52 | K G P | E LOC:College + NEAR:Ancano | MG_JOIN; ANCANO_ALIVE; first time |
| MG53 | K V | T | MG_AUGUR; ANCANO_ALIVE |
| MG54 | L X | T | MG_JOIN; ANCANO_ALIVE |
| MG55 | K P | T | ARCH |
| MG56 | A K | E LOC:College | ASHE_Q1; ANCANO_ALIVE |
| MG57 | R L | E LOC:Mzulft | MG05 running and stage < 20 (arrival), else first later visit |
| MG58 | L K P | E LOC:Labyrinthian | first visit |
| MG59 | I G | T | MG_STAFF |
| MG60 | V R K | T | STAFF_CARRIED |
| MG61 | G V P | T | ARCH |
| MG62 | K P | E LOC:ArchQuarters | ARCH; K_TOG+ |
| MG63 | X R P | E LOC:ArchQuarters | ARCH; AFTER Q18 |
| MG64 | L P | T | ARCH |
| MG65 | R I P | T | ARCH |
| MG66 | V K P | E LOC:Arcanaeum or T | MG_JOIN; V_FLIRT and K_CRUSH |
| MG67 | S K | E LOC:College | S_COMP; K_ANY; S following |
| MG68 | A G | E LOC:College | A_CRUSH |
| MG69 | G V | E LOC:College | G_FLIRT |
| MG70 | K I P | E LOC:College | K_TOG+ |

## 4. Notes for the build
- Luna speaks in 33 of 70 (47%), above the usual third by request: she is a mage and this is her ground.
- Rival talks: MG5, MG36 (Kaidan's crush, Luna oblivious), MG37, MG62, MG70 (K_TOG+, Luna fond), MG66 (Val vs Kaidan), MG67 (Serana vs Kaidan), MG68 (Ashe), MG69 (Gore). Luna has no romance line in any rival talk and never notices the crush in K_CRUSH rows.
- Val's College story (ValCOL / ValCOLGrad) is never narrated; MG43 / MG44 only react to "enrolled" and "graduated". MG25 ("give me a term") is fine either side of VAL_COL.
- Everything after ARCH assumes the vanilla ending (Mirabelle and Ancano dead, Psijics take the Eye, Tolfdir lives). There are no branches.
- Existing coverage avoided: Q17 (Lucien's library dream / entrance test), Q18 (Xelzaz's room), LT89 (Urag the pettiest librarian), MN "lost eyebrows" notice, TG Enthir-as-fence joke, VG Psijic on the road, Ashe x Serana College location talk (no Ashe+Serana pairing here).
- No "Dragonborn", no Kaidan cult reference, no Brynjar (MG16 needs INIGO_BV only).
