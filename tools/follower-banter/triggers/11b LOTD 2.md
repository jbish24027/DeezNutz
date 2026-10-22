# 11b LOTD 2 - trigger rows (prefix LT, LT141-LT240, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\11b LOTD 2.txt`
Part 1 (all local codes, places and silences reused unchanged): `triggers\11 LEGACY OF THE DRAGONBORN.md`.
Research: `research\content\lotd.md` (quest table section 2, silences section 3, places section 4). Serana/Ashe Free() and gate codes: `triggers\48 SERANA.md`, `triggers\49 ASHE.md`, `triggers\20 DAWNGUARD.md` section 3.
Gate codes from `TRIGGERS.md` section 4. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe; "+Luna" = player line (Eleonora voice), no Free check.

## Global for every row
- `WorldQuiet()` + `Free(x)` (TRIGGERS.md sections 2-3) + **`LT_QUIET`** exactly as in file 11 (tours, gala, nightmare 65..80 hard silent, cave-in 61..75 hard silent, Rkund guided stretch, Pelagius' mind, Sancre Tor / Herald, Wulfharth tomb, Planetarium reveal, Waystone jump, Indarys assassin, Heist confrontation, Vigilants in the museum, any LOTD staff/patron scene, player in dialogue with Auryen/Avram/an explorer).
- Rows with **S** also need `SERANA` + Serana Free (48 SERANA.md). Rows with **A** also need `ASHE_HIRED` + Ashe Free and Ashe silence (49 ASHE.md).
- Haunt 15..104: none of these rows may play (file 11 lets only LT110 play there).

## New local codes (this file)
- `FULL:<wing>` = that wing's display set is complete. **[UNC: LOTD keeps per-section display counts; the global/formlist was not looked up.]** Fallback for each: fire on room entry with `LT_HIRED` and Exc02 (58B96A) 140 done (late game, most cases filled).
  - `FULL:DAED` (M_DAED), `FULL:DWE` (M_HOLE, Dwemer wing), `FULL:MASKS` (M_HOH, dragon priest mask wall), `FULL:ARM` (M_ARM), `NEAR_FULL` (whole museum; fallback Exc01 150 + Exc02 140 + Exc03A 350 + SL 300 done, as LT140).
- `DISP:<who>` = that follower's gear display exists and is filled in the Hall of Heroes. `DBM_Xelzaz_Patch.esp` / `DBM_Remiel_Patch.esp` add them **[UNC: display ref and filled check]**. Fallback: E M_HOH with the patch plugin loaded (`Game.GetModByName`).
- `SCROLL_SHOWN` = Elder Scroll (Blood) on its LOTD display **[UNC]**. Fallback: `DG_END` and player no longer carries DLC1ElderScrollBlood.
- `VISITORS` = MUSEUM, hour 9..18, at least one patron ref enabled and within 2000 **[UNC: patron refs, same open item as file 11 NEAR:]**. Fallback: E M_HOH daytime.
- `NIGHT_M` = MUSEUM and hour >= 22 or < 4. `SHIFT` = NIGHT_M and Heist (33D940) completed (the party helps Avram's short-handed watch).
- `AMJ:<relic>` = the matching Auryen's Notes quest (DBM_AMJournalQST01..10, 148479 / 14846F / 14D594-14D59B) completed (30 or 50). **[UNC: which number is which relic]**. Randagulf: `AMJ_RUN:Randagulf` = started (10 done) and completed == 0.
- `SANAMIA:<site>` = DBM_JournalDungeon01..05QST (1D5C18 Mzulft, 2703F9 Valthume, 275562 Fort Frostmoth, 27FDB5 Lake Ilinalta, 27FDD3 Burial Ruin) stage 5 done. **[UNC: number-to-site order assumed from lotd.md's list order]**
- `HOW` = player in DBM_HallofWondersLocation (0062AF:DBM_CC_HallOfWonders.esp) and that plugin loaded.
- `RC_GOGH` = Redcap's CC Goblins quest done (FARGRedcapCCGoblinsPatch.esp present; Spear of Bitter Mercy received) **[UNC stage]**.
- `VAL_BOTTLE` = Val has been given the ship in a bottle (Val's gift system) **[UNC flag]**. Fallback: VAL_FATHER.
- `RX` (file 11) = Remi/Xelzaz not fallen out. `KI` = KaiandInigo >= 10. `LI` = JRLucienInigoRank >= 2. `LX` = Lucien-Xelzaz intro done. `RG_SIS` as file 11.
- `played:LTnnn` = that talk already played.

## Table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| LT141 | S G | E M_DAED | Mace displayed (proxy DA10 completed, as LT15); played:LT15 |
| LT142 | X I +Luna | E M_DAED | FULL:DAED; after X6 |
| LT143 | R A | E M_HOLE | ASHE_REVEAL; FULL:DWE or LT_HIRED |
| LT144 | L R +Luna | E M_HOLE | FULL:DWE; after B10 |
| LT145 | S V | E M_HOLE | LT_HIRED; played:LT176 |
| LT146 | C X | E M_HOLE | MuchAdo (5C7E75) 500 done; after R18 |
| LT147 | K L +Luna | E M_HOH | FULL:MASKS |
| LT148 | C G | E M_HOH + NIGHT_M | FULL:MASKS; after R5 |
| LT149 | A I | E M_ARM | FULL:ARM |
| LT150 | V L | E M_ARM | LT_HIRED; after C1 |
| LT151 | X K | E M_HOH | DISP:Xelzaz; after C3 |
| LT152 | R V | E M_HOH | DISP:Remi; HLIOValRemiFriendshipTracker >= 1 |
| LT153 | S +Luna | E MUSEUM | SCROLL_SHOWN; DG_END; played:LT176 |
| LT154 | K G +Luna | T in M_HOH | LT_HIRED; EXPL; after A1 |
| LT155 | C V | E HOW | RC_GOGH; after R8 |
| LT156 | I +Luna | T in MUSEUM | NEAR_FULL |
| LT157 | G +Luna | T in MUSEUM | LT_HIRED; GORE_FATHER (he has faced his past) |
| LT158 | V K +Luna | T in MUSEUM | VAL_BOTTLE; after A2 |
| LT159 | C I | T in MUSEUM | RC_MANOS; LT_HIRED; after R13 |
| LT160 | R X | T in MUSEUM | LT_HIRED; RX |
| LT161 | X +Luna | T in MUSEUM | LT_HIRED |
| LT162 | I K +Luna | E M_ARM | LT_HIRED; KI |
| LT163 | L K | T in MUSEUM | LUC_ADMIT; LT_HIRED |
| LT164 | K G | T in MUSEUM | BRYNJAR; played:LT157; after A1 |
| LT165 | S +Luna | T in MUSEUM | DG_END; played:LT176 |
| LT166 | A V | T in MUSEUM | LT_HIRED |
| LT167 | K V +Luna | E M_HOH + VISITORS | LT_HIRED; after A2 |
| LT168 | G R +Luna | E MUSEUM, first tick after DBM_MuseumIntroTour or a radiant tour (08F978..08F97D) stops | LT_HIRED; RG_SIS |
| LT169 | G I | E NEAR:Cedric/Verna | after C2 |
| LT170 | C L | E NEAR:Henry | after R11 |
| LT171 | S I | E VISITORS | SER_VAMP; played:LT176 |
| LT172 | X G +Luna | T in M_HOH | LT_HIRED; after X1 |
| LT173 | R V +Luna | T in MUSEUM | DBM_DHQuest (9211FD) 40 done; HLIOValRemiFriendshipTracker >= 2 |
| LT174 | A K | E VISITORS | ASHE_HIRED |
| LT175 | L K | E M_HOLE + VISITORS | LT_HIRED |
| LT176 | S K +Luna | E MUSEUM (first entry with Serana following) | SERANA. Plays before every other S row in this file |
| LT177 | A L | E GUILD | EXPL; ASHE_REVEAL |
| LT178 | G +Luna | T | DBM_RadiantRuinedBooks (5A94C3) 10 done |
| LT179 | A X | E M_HOH | Exc03A (2702EE) 80 done; played:LT94 |
| LT180 | G K | T | Exc03A 80 done; after A1 |
| LT181 | S C | E GUILD | SER_VAMP; Exc01 (4D1811) 150 done |
| LT182 | L +Luna | E GUILD | DBM_ExplorerGuildHouse (3431C3) completed; EXPL |
| LT183 | X K +Luna | E GUILD | EXPL; after C3 |
| LT184 | X G | E FS_EAST (2BB745) | DBM_ExplorerFieldStation03 (2D1178) 15 done; after X1; played:LT78 if possible |
| LT185 | K V | E FS_WEST (2BB744) | DBM_ExplorerFieldStation02 (2D1170) 15 done; after A2 |
| LT186 | R G | E GUILD | EXPL; RG_SIS |
| LT187 | A C | T | DBM_HrormirStaffQuest (4F0624) 5 done and 20 not done |
| LT188 | S X | T | DBM_VampireParts (0854C5) 10 done and 200 not done |
| LT189 | S R | T | DBM_WaystoneQuest (16658E) 20 done |
| LT190 | C K | T | DBM_GhostChestQST (2E566D) 10 done and 20 not done; after R1 |
| LT191 | V I | T | AMJ:Cyrus' Saber; after I1 |
| LT192 | V G | T | AMJ:Orgnum's Coffer; after A3 |
| LT193 | G L | T | AMJ:Ice Blade of the Monarch; after L1 |
| LT194 | R I +Luna | T | AMJ_RUN:Randagulf; after B6 |
| LT195 | S +Luna | T | AMJ:Shalidor's Stone |
| LT196 | V +Luna | T exterior | DBM_SextantHandler (18DDE8) 5 done and 6 not done |
| LT197 | C K | E Fort Frostmoth (DLC2 location) | SANAMIA:Fort Frostmoth; after R1 |
| LT198 | L I | E Mzulft sealed chamber cell 1D5B20 | SANAMIA:Mzulft; LI |
| LT199 | S L +Luna | E MUSEUM | played:LT176 |
| LT200 | L K | T | DBM_LordsMailQuest (125B25) 100 done |
| LT201 | G S | T | DBM_VigilantsQuest2 (0E1595) 75 done; SER_VAMP |
| LT202 | K +Luna | T | DBM_ArtifactOrderQuest (0F0D35) 10 done and 100 not done |
| LT203 | S K | E exterior at Windcaller Pass (1942FA/1943CD), IsPleasant | Exc01 20 done and 150 not done; SER_VAMP |
| LT204 | A G | E exterior at Windcaller Pass | Exc01 20 done and 150 not done |
| LT205 | R X | T | Exc02 (58B96A) 140 done; RX |
| LT206 | C R | E Rkund cells (504BBE etc.) | Exc02 140 done (outside the 90..140 guided silence) |
| LT207 | I L | E Greenwall dig (23CBD8) | Exc03A 50 done and 61 not done; LI |
| LT208 | R +Luna | T, NIGHT | Exc03A 80 done and 95 not done |
| LT209 | S I | E Darkfall Passage on Tulrin's trail | Exc03A 175 done and 180 not done; DG_END |
| LT210 | L G | T | Exc03A 275 done and 300 not done; after L1 |
| LT211 | C I | E M_HOH | Exc03A 350 done; played:LT96; after R13 |
| LT212 | G I | E Rkund exterior | Exc02 140 done; after C2 |
| LT213 | S V | E AIRSHIP, IsPleasant | DBM_MuseumIndarysQuest (371C28) completed; SER_VAMP |
| LT214 | A I | E AIRSHIP, RAIN | DBM_MuseumIndarysQuest completed |
| LT215 | K I +Luna | E AIRSHIP | DBM_MuseumIndarysQuest completed; KI |
| LT216 | R L | E AIRSHIP | DBM_MuseumIndarysQuest completed; after B10 |
| LT217 | V C +Luna | E AIRSHIP | DBM_MuseumIndarysQuest completed; after R9 |
| LT218 | X V | E AIRSHIP | DBM_MuseumIndarysQuest completed; after X4 |
| LT219 | C L +Luna | E M_SAFE (garden) | after R11. [UNC: Bigpig present; if not, line still reads as a story] |
| LT220 | X K | E M_SAFE | after C3 |
| LT221 | G I +Luna | T in M_SAFE | after C2 |
| LT222 | L R | E M_SAFE | after B10 |
| LT223 | K V +Luna | E M_SAFE | after A2 |
| LT224 | S L | E M_SAFE | DG_END; played:LT222 |
| LT225 | G R | T in M_SAFE | RG_SIS |
| LT226 | X V G | T in M_SAFE, hour 17..21 | after X1, X4, A3 |
| LT227 | I V | E M_SAFE | after I1 |
| LT228 | R K +Luna | E M_SAFE | after B1 |
| LT229 | G K | E SHIFT | after A1 |
| LT230 | S I | E M_LIB + NIGHT_M | played:LT176 |
| LT231 | A +Luna | E NIGHT_M | ASHE_REVEAL |
| LT232 | V R | E NIGHT_M | HLIOValRemiFriendshipTracker >= 1 |
| LT233 | L X | E NIGHT_M | Haunt (7AC75C) completed (110); LX |
| LT234 | K +Luna | E NIGHT_M | K_LOVE+ |
| LT235 | C I | E NIGHT_M | after R13 |
| LT236 | L G +Luna | E MUSEUM, hour 5..7, after a SHIFT night | Heist completed; after L1 |
| LT237 | X I | E NIGHT_M in M_HOH | after X6 |
| LT238 | V C | E SHIFT | after R8 |
| LT239 | R K | E NIGHT_M | Haunt completed; after B1 |
| LT240 | S A +Luna | E NIGHT_M | Exc01 150, Exc02 140, Exc03A 350 and SL 300 all done; ASHE_REVEAL; played:LT176 |

## Pacing
- At most one LT141-LT240 talk per in-game day inside the museum, and never two talks from the same Part in a row.
- Keepsake talks (LT157-LT166) at most one per three in-game days, so the donations feel like separate decisions.
- Night-shift talks (LT229-LT240) at most one per night.

## Open items
- Every `FULL:` check, `DISP:` check, `SCROLL_SHOWN`, `VISITORS` and `HOW` need their LOTD records looked up (see the fallbacks above).
- Auryen's Notes and Sanamia's Journals number-to-relic/site mapping.
- `VAL_BOTTLE` and `RC_GOGH` flags.
- LT209 Darkfall Passage location for the Trinimac trail (cell not listed in lotd.md; use Exc03A 175..180 alone if no cell check).
