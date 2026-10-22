# Triggers - 10b DRAGONBORN 2 (DR141-DR240)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\10b DRAGONBORN 2.txt`
Part 1: `triggers\10 DRAGONBORN SOLSTHEIM.md` (DR1-DR140). **Everything in part 1's "Extra rules" applies here unchanged**: `SOLST` also needs the player in `DLC2SolstheimWorld` (000800); the Dragonborn silence zones (DLC2MQ01 5..7, DLC2RRArrivalScene running, DLC2MQ02 20..25, Apocrypha, DLC2MQ03 50..60, DLC2MQ05 340 to DLC2MQ06 10, DLC2MQ06 200..550, DLC2dunKolbjornQST 449..490) stay in WorldQuiet(); `K_CRUSH` talks stop at K04 >= 50; in-fight barks bypass the player-in-combat quiet rule, carry no CombatEnd, one bark per fight.

Format and gate codes: TRIGGERS.md sections 4-5. Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe. "+Luna" = the player speaks (no Free() check).
All quests/locations are `Dragonborn.esm` unless stated. "N done" = `GetStageDone <quest> N == 1`. **[UNC]** = unconfirmed, check at build.

Serana and Ashe:
- Free() rows for Serana and Ashe: `triggers\20 DAWNGUARD.md` section 1, unchanged. Every S talk also needs `SERANA` (DLC1VQ02 5 done); every A talk also needs `ASHE_HIRED` (`MM_AsheIntro` 0A7946:Ashe - Fire and Blood.esp completed). Respect Ashe's silence list (`triggers\49 ASHE.md`).
- Gate codes reused from `20 DAWNGUARD.md` section 3: `SER_VAMP` (Serana HasKeyword Vampire 0A82BB == 1), `DG_GARDEN`, `ASHE_REVEAL`, `ASHE_LOGS`.
- Every Serana and Ashe talk here also needs `SOLST`.

New gate codes in this file:
- `RR_ADRIL` = DLC2RR01 (018B13) 10 done OR DLC2RR02 (018B14) 10 done (Adril Arano has given you work). [UNC: both quests are given by Adril per vanilla; first stage numbers from research B2]
- `RR_FAVOR` = any of DLC2RRFavor01-07 (024DDE...02BAC6) 200 done. `RR_NETCH` = "Fetch the Netch" favour 200 done; `RR_FIRSTED` = "First Edition" favour 200 done. **[UNC: which DLC2RRFavor0N is which; research lists names in order Recipe for Distraction, Fetch the Netch, Clean Sweep, It's All In The Taste, Pain in the Necklace, Feeding the Addiction, First Edition = 01..07, so Fetch the Netch = 02, First Edition = 07; verify]**
- `PAID_IN_FULL` = DLC2TGQuest (02AD26) 200 done.
- `SEVERIN_OWNED` = DLC2RR02 200 done AND the player owns Severin Manor (019A20). **[UNC: ownership check; the manor is bought from Morvayn after Served Cold - test the house key in inventory or the BYOH-style "owned" flag on the location; fall back to DLC2RR02 200 + player has entered 019A20 after 200]**
- `NELOTH_JOBS2` = at least two of DLC2TTR1-8 300 done.
- `GORE_READS` = Gore's reading lessons have begun. **[UNC: no single flag traced in gore.md; fall back to "after any talk in which Gore reads", e.g. after DR196 if it played, else no extra gate]**

Event checks new to this file (all [UNC] where noted):
- `LOC:<name>` = player `IsInLocation` (child locations count): Morvayn Manor **[UNC FormID, child of Raven Rock 0143B9]**; Glover Mallory's forge = Raven Rock exterior within 800 units of Glover's smithing forge ref **[UNC ref]**; Raven Rock docks = Raven Rock exterior, within 1500 units of the Northern Maiden's mooring **[UNC ref]**; Isinfier Plains **[UNC: no location record; use player in DLC2SolstheimWorld north of the Skaal Village latitude AND IsSnowing or cell in the northern snow region]**; Benkongerike **[UNC location FormID; it is a Riekling camp map marker]**; Fahlbtharz 0142A0; Saering's Watch **[UNC location FormID]**; Redcap's village **[UNC: Redcap mod location, FA01 plugin]**; giant mushrooms near Tel Mithryn = exterior within 4000 units of Tel Mithryn 0143BC; ash wastes = DLC2SolstheimWorld exterior south of Raven Rock's latitude **[UNC]**; northern coast/ice = DLC2SolstheimWorld exterior in the north third + SNOW region **[UNC]**.
- `COMBAT:<enemy>` (in-fight bark) and `AFTERFIGHT:<enemy>`: Reaver = faction DLC2ReaverFaction **[UNC]**; Ebony Warrior = DLC2EbonyWarrior actor **[UNC]**; Karstaag = DLC2Karstaag actor **[UNC]**; ice wraith = IceWraithRace (Skyrim.esm) on Solstheim; Ash Guardian = DLC2AshGuardianRace **[UNC]**; Dwemer centurion = DwarvenCenturionRace in DLC2SolstheimWorld or Solstheim interiors; dragon priest = DragonPriestRace in a Solstheim location; horker = HorkerRace in DLC2SolstheimWorld.
- `ASHSTORM` = part 1's ash-storm weather check (STORM on Solstheim) **[UNC weather ID]**. `ASHSKY` = exterior Solstheim, daytime, ash weather but not a storm (the sun is hidden) **[UNC]**.

| ID | Speakers | Type | Gates |
|---|---|---|---|
| DR141 | V G | E Retching Netch (019A24) | SOLST; after DR13 (or third visit to 019A24); after A3 |
| DR142 | K G | T | DLC2TT1b completed (300/310/320); after A1 |
| DR143 | R V | E LOC: Glover Mallory's forge | TG_JOIN; SOLST; HLIOValBanter stage >= 10 |
| DR144 | K R | E LOC: Glover Mallory's forge | SOLST; after B1 |
| DR145 | R +Luna | T | PAID_IN_FULL |
| DR146 | X +Luna | T | RR_ADRIL |
| DR147 | I L | E LOC: Morvayn Manor | RR_ADRIL; JRLucienInigoRank >= 2. [UNC: Cindiri Arano is Adril's wife living in Morvayn Manor - verify NPC; if wrong, swap the name] |
| DR148 | L V | T | DLC2RR01 30 done (Frostmoth visited) [UNC stage]; DLC2MQ01 30 done; after C1 |
| DR149 | V R +Luna | E LOC: Severin Manor (019A20) | SEVERIN_OWNED; HLIOValBanter stage >= 10 |
| DR150 | G L | E Raven Rock Mine (01429A) or Raven Rock exterior | DLC2RR03 200 done; after L1 |
| DR151 | K G +Luna | T | RR_NETCH (or any RR_FAVOR - Gore's "netch jelly" line fits Fetch the Netch best); after A1 |
| DR152 | X I | T | DLC2RR01 10 done (spawn attacks begun); DLC2RR01 90 not done; after X6 |
| DR153 | C R | T | DLC2RR01 90 done; Remi-Redcap intro done (FA01RemiIntroScene) |
| DR154 | G +Luna | E Tel Mithryn (0143BC) | DLC2MQ04 10 done; Talvas alive [UNC ref] |
| DR155 | X L | E Tel Mithryn (0143BC) | DLC2TTF1 300 done; Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |
| DR156 | S X | E Tel Mithryn (0143BC) | SERANA; DG_GARDEN; DLC2MQ04 10 done |
| DR157 | X V | E Tel Mithryn (0143BC) | NELOTH_JOBS2; after DR43; after X4 |
| DR158 | X +Luna | E Tel Mithryn Tower (01CDEA) | DLC2MQ04 10 done |
| DR159 | S K | E first Tel Mithryn visit with Serana following | SER_VAMP; DLC2MQ04 10 done |
| DR160 | A R | E first Tel Mithryn arrival with Ashe following | ASHE_REVEAL; DLC2MQ04 10 done; DLC2TTR6 (Briarheart Necropsy) 100 done [UNC which TTR index; the line names the Briarheart job]; Remi-Ashe first meeting done (49 ASHE.md) |
| DR161 | A +Luna | T | ASHE_REVEAL; DLC2TTR2 "Heart Stones" 300 done [UNC index] |
| DR162 | X L | T | DLC2MQ04 550 done; NELOTH_JOBS2; Xelzaz-Lucien intro done |
| DR163 | C +Luna | T | DLC2TTR6 "Briarheart Necropsy" 300 done [UNC index] |
| DR164 | R L | T | DLC2TTR1 "Lost Knowledge" 300 done; after B10. User asked for "Hidden Knowledge": no Dragonborn quest of that name is in the research list; mapped here to Lost Knowledge [UNC] |
| DR165 | V I | T | DLC2TT1 500 done; after I1 |
| DR166 | X +Luna | E leaving Neloth's study / Tel Mithryn Tower (01CDEA) | NELOTH_JOBS2 |
| DR167 | G K | E WATER near Skaal Village (0143BB) | SOLST; after A1 |
| DR168 | G R | T | DLC2MQ03 200 done; HLIOGoreBanter intro done |
| DR169 | C G | E Skaal Village (0143BB) | DLC2MQ03B 200 done; after R5 |
| DR170 | L V | E Skaal Village (0143BB) | DLC2MQ03B 200 done; after C1 |
| DR171 | S L | E Skaal Village (0143BB) | SERANA; SOLST |
| DR172 | G S | E Skaal Village (0143BB) | SER_VAMP; Gore-Serana first talk done (48 SERANA.md) |
| DR173 | K +Luna | E Skaal Village (0143BB) | DLC2MQ06 10 done; DLC2MQ06 550 not done (keep it near the loss) |
| DR174 | L +Luna | T | DLC2SV01 200 done; after DR56 |
| DR175 | A K | T | DLC2SV02 200 done; ASHE_REVEAL; Kaidan-Ashe first meeting done (49 ASHE.md) |
| DR176 | G V | T | DLC2SV02 200 done; SOLST; after A3 |
| DR177 | L +Luna | T | DLC2SV02 200 done; player has crafted or holds a stalhrim item [UNC: GetItemCount on any DLC2 stalhrim weapon/armour keyword; else drop this check] |
| DR178 | G I | E Skaal Greathall (01D92C), hour 18..23 | SOLST; after C2 |
| DR179 | K +Luna | E Skaal Village (0143BB) | K_ENG or K_MAR |
| DR180 | G L | E LOC: ash wastes | SOLST; after L1 |
| DR181 | X A | E LOC: northern ice + SNOW | ASHE_REVEAL; Xelzaz-Ashe first meeting done (49 ASHE.md) |
| DR182 | I K | E LOC: Isinfier Plains | SOLST; KaiandInigo stage >= 10 |
| DR183 | S +Luna | E LOC: northern coast + CLEARNIGHT | SERANA; SOLST |
| DR184 | K +Luna | T Solstheim exterior, far from Raven Rock / Skaal Village / Tel Mithryn | SOLST (any romance stage; no romance content) |
| DR185 | C V | E LOC: Benkongerike (approach) | SOLST; after R8 |
| DR186 | C +Luna | E Solstheim exterior, coast | RC_MANOS (Redcap has been home: "Back to the Rock" done) [UNC stage] |
| DR187 | C K | T | RC_STAY (tribe freed and Redcap stayed); after R1 |
| DR188 | V C | E LOC: Redcap's village | RC_MANOS; after R8 |
| DR189 | C L | E Fahlbtharz (0142A0) approach | SOLST; after R11 |
| DR190 | C X | E CAMP on Solstheim | SOLST; after R18 |
| DR191 | R I | E LOC: giant mushrooms near Tel Mithryn | SOLST; after B6 |
| DR192 | A L | E after ASHSTORM ends on Solstheim | ASHE_REVEAL; Lucien-Ashe first meeting done (49 ASHE.md) |
| DR193 | A K +Luna | E ASHSTORM on Solstheim | K_CRUSH; ASHE_REVEAL; Kaidan-Ashe first meeting done |
| DR194 | K +Luna | T | K_TOG+; Saering's Watch word learned [UNC: no quest; use player has the Dragon Aspect word or visited the Saering's Watch location]; DB |
| DR195 | S +Luna | E ASHSKY on Solstheim | SER_VAMP |
| DR196 | G V | T | DLC2dunHaknirTreasureQST 29 done [first map found; UNC stage meaning]; after A3 |
| DR197 | R V | T | DLC2dunHaknirTreasureQST 70 done [UNC: two chests opened]; HLIOValBanter stage >= 10 |
| DR198 | K +Luna | T | DLC2dunHaknirTreasureQST 100 done; K_TOG+ |
| DR199 | V X | T | DLC2dunKolbjornQST 200 done; DLC2dunKolbjornQST 449 not done; after X4 |
| DR200 | R A | E near Kolbjorn Barrow (0142BB) | DLC2dunKolbjornQST 300 done; 449 not done; ASHE_REVEAL; Remi-Ashe first meeting done |
| DR201 | R +Luna | T | DLC2MQ05 1000 done |
| DR202 | G R | T | DLC2RR03 200 done; HLIOGoreBanter intro done |
| DR203 | S I | T | DLC2EbonyWarriorQuest 200 done; SERANA; Serana-Inigo SDA intro done (SDA_BanterTrackerInigo >= 1) [UNC] |
| DR204 | A G | T | DLC2EbonyWarriorQuest 200 done; Gore-Ashe first meeting done (49 ASHE.md) |
| DR205 | S V | T | BLACKBOOK; VAL_FATHIS; SERANA; Serana-Val first talk done (48 SERANA.md) |
| DR206 | A +Luna | E return from Apocrypha (any DLC2BlackBook03-07Quest 20 newly done, or DLC2MQ04 550 newly done) | ASHE_LOGS |
| DR207 | G +Luna | T | SOLST; GORE_READS |
| DR208 | V K | E LOC: Raven Rock docks | VAL_FATHER; after A2 |
| DR209 | I +Luna | T Solstheim exterior | SOLST |
| DR210 | R K | E Kolbjorn Barrow interior (0142BB, interior cell) | DLC2dunKolbjornQST 400 done [UNC: barrow open]; 449 not done; after B1 |
| DR211 | A V | T | DLC2TT1b completed; Val-Ashe first meeting done (49 ASHE.md) |
| DR212 | C A | E DWEMER on Solstheim (Nchardak 0142B4, Kagrumez 0142A2, Fahlbtharz 0142A0, or any Solstheim Dwemer interior) | ASHE_REVEAL; after PR205 (Redcap-Ashe "Metal. Lady." arc) |
| DR213 | C S | E LOC: Redcap's village | RC_STAY; SER_VAMP; after PR379-ish Redcap-Serana "Star. Lady." talk (46b) [UNC ID - use the first Redcap+Serana pair talk] |
| DR214 | S A | E Retching Netch (019A24) | SERANA; ASHE_REVEAL; Serana and Ashe both following |
| DR215 | I A | E LOC: Isinfier Plains, rest (player not moving 20 s) [UNC] | Inigo-Ashe first meeting done (49 ASHE.md) |
| DR216 | G X | E Thirsk Mead Hall (016FFE) | DLC2MH01 25 done; after X1 |
| DR217 | V +Luna | T | RR_FIRSTED |
| DR218 | K +Luna | T | DLC2MQ04 550 done; K_ANY |
| DR219 | K L | E Skaal Village (0143BB) or its shore | DLC2MQ03B 200 done; Lucien-Kaidan intro done (Lucien's own scene 1) |
| DR220 | R +Luna | T | DLC2KagrumezQST 250 done |
| DR221 | I C | E Retching Netch (019A24) | SOLST; after R13 |
| DR222 | S R | T | DLC2MQ03B 200 done; SERANA; Serana-Remi SDA intro done (SDA_BanterTrackerRemiel >= 1) [UNC] |
| DR223 | S +Luna | T | DLC2MQ06 550 done; SERANA |
| DR224 | K +Luna | E LOC: Severin Manor (019A20) | K_MAR; SEVERIN_OWNED |
| DR225 | G +Luna | E WATER on Solstheim | DLC2MQ03B 200 done; DB |
| DR226 | C X +Luna | E leaving Solstheim on the Northern Maiden (player leaves DLC2SolstheimWorld by boat) | DLC2MQ06 550 done; after R18; once |
| DR227 | K G | E COMBAT:Reaver (in-fight bark) | SOLST; after A1 |
| DR228 | V C | E AFTERFIGHT:Reaver | SOLST; after R8 |
| DR229 | A G | E AFTERFIGHT:Reaver, 8+ Reavers killed in the fight [UNC count; else any Reaver fight] | ASHE_HIRED; Gore-Ashe first meeting done |
| DR230 | K +Luna | E COMBAT:Ebony Warrior (in-fight bark) | DLC2EbonyWarriorQuest 100 done |
| DR231 | C K | E COMBAT:Karstaag (in-fight bark) | SOLST; after R1 |
| DR232 | L S | E COMBAT:ice wraith on Solstheim (in-fight bark) | SERANA; SOLST |
| DR233 | R X | E AFTERFIGHT:ice wraith on Solstheim | SOLST; BPUFXelzazAndRemielInteractions stage 11 done |
| DR234 | R I | E COMBAT:Ash Guardian (in-fight bark) | SOLST; after B6 |
| DR235 | X +Luna | E AFTERFIGHT:Ash Guardian | SOLST |
| DR236 | R A | E COMBAT:Dwemer centurion on Solstheim (in-fight bark) | ASHE_HIRED; Remi-Ashe first meeting done |
| DR237 | K L | E COMBAT:dragon priest on Solstheim (in-fight bark) | SOLST; Lucien-Kaidan intro done |
| DR238 | L +Luna | E AFTERFIGHT:dragon priest on Solstheim | SOLST |
| DR239 | I K | E COMBAT:horker on Solstheim (in-fight bark) | SOLST; KaiandInigo stage >= 10 |
| DR240 | S K | E COMBAT:ash spawn (in-fight bark) | SERANA; SOLST |

## Notes for the build
- Branch safety: DR149 says only "the last owners plotted a murder in this house", true on every Served Cold outcome. DR216 is Nord-side only (DLC2MH01 25). DR201 does not say what the secrets were. DR204 assumes the Ebony Warrior quest completes on his death (stage 200).
- Romance: no Serana or Ashe romance lines in this file. DR193 is Kaidan's crush with Ashe as witness; Luna stays oblivious. DR179/DR224 are Kaidan K_ENG/K_MAR and stay general (no scripted wedding content).
- Facts to verify at build: Cindiri Arano (DR147); which RRFavor index is "Fetch the Netch" and "First Edition" (DR151, DR217); TTR indices for Heart Stones, Briarheart Necropsy and Lost Knowledge (DR160, DR161, DR163, DR164); Redcap village location and "Back to the Rock" stage (DR186, DR188, DR213); Saering's Watch location (DR194).
