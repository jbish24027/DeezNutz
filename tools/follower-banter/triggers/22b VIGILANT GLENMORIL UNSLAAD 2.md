# Triggers - 22b VIGILANT GLENMORIL UNSLAAD 2 (VG191-VG310)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\22b VIGILANT GLENMORIL UNSLAAD 2.txt`
Research: `research\content\vigilant_glenmoril_unslaad.md` (+ `_detail\`).
Format as TRIGGERS.md section 5. Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, SE Serana, AS Ashe. Luna (player voice) needs no Free() check.
FormIDs are `<id>:Vigilant.esm`, `:Glenmoril.esm` or `:Unslaad.esm` by quest prefix (zzzAoM/BM/CO/CH = Vigilant, zzzLrh/LRH/GH/LaM/Rev = Glenmoril, zzzCrb = Unslaad) unless another plugin is named. "done N" = `GetStageDone(quest, N) == 1`. "stage a..b" = `GetStage` in range while running.

## 1. Gate codes

**Every gate code from part 1 (`triggers\22 VIGILANT GLENMORIL UNSLAAD.md` section 1) applies unchanged:** `VG_ON`, `VG_JOINED`, `VG_TEMPLE`, `OWL_OFFER`, `KEEPER`, `CH_BACK`, `CH_GOOD`, `CH_BAD`, `MARTYR`, `GL_ON`, `UN_ON`, `G_OK`, `G_PRE`, `G_GONE`, `G_BACK`, `G_LOST`, `SE_F`, `SE_VAMP`, the AS following block, `ASHE_*`. Section 2 of that file (extra WorldQuiet silence for all three mods, plus the Gore - Vigilant collision places) also applies to every talk here.

Global rules for this file:
- **`not MARTYR` on every VG talk** (zzzCOMq01 065932 done 200 blocks the whole file).
- **`G_OK` on every talk with G.** Gore never speaks while `G_GONE`.
- Every Coldharbour story talk (VG201, VG202, VG208, VG214-VG231) needs `CH_BACK`: the player is back in Tamriel and the speakers are near her again. The story event inside the talk is gated by the quest named in its row.
- Every Atmora story talk (VG304-VG308) needs `UN_BACK` (below).

New local codes:
- `CH_SUB(q, s)` = CH_BACK AND `GetStageDone(q, s)`. Quest FormIDs from research A2 "Act 4 side quests" / "memories".
- `UN_BACK` = zzzCrbMq09 47A32B done 901 AND player in Tamriel (worldspace Tamriel or a Tamriel child) AND speakers near the player.
- `KMD_DONE` = KMDQuest (0Kaidan.esp) completed (same check as part 1's VG176).
- `RAD(q)` = radiant quest q done 20 or done 30 [unconfirmed which stage each one completes on; research says "All complete at stage 20 or 30"]. Fire once, on the first completion.
- `IN_UNSLAAD` = player GetInWorldspace Unslaad 004E70.
- `IN_BLACKSPRING(x)` = player AND every speaker x GetInWorldspace Svartibrunnr 000D62 [unconfirmed: followers may never arrive].
- `MG_JOIN`, `DB`, `SHOUT1`, `VAL_FATHIS`, `K_CRUSH`, `K_ANY`: as TRIGGERS.md section 4.

## 2. Collisions avoided (in addition to part 1)
- No talk fires inside Jo'vanni's dream (Mq06 30..59), the Lamae dream, the Jealousy room, Coldharbour, the Black Spring dreams, the Old Well, or the Atmora chain. Post-realm talks key on the stage after.
- Bruiant mansion talks (VG209, VG210, VG240) contain no Gore; they are fine while Gore is vanishing/vanished. VG212 and VG213 are explicitly `G_GONE` and have no Gore lines.
- VG233 and VG234 are Gore-afraid talks (`G_PRE`) and never mention Gore reading by himself (he can't until Act 3).
- VG235/VG236/VG307 use `G_BACK` (already waits 2 days after the return and HD1WTCHVar != 2).
- Hoarfrost 30..60 and Lingering Snow 80..110 are silent; no barks were written for Austella or the Gray Owl fights for that reason.

## 3. Per-talk table

### PART 1 - VIGILANT (VG191-VG240)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| VG191 | V R | T | zzzAoMqOwl 4419E5 running and not done 20; zzzAoMMq00 005CE2 stage < 15; player in Dawnstar location; not in Windpeak Inn (Gore ALTANO scene) |
| VG192 | X K | T | VG_TEMPLE; player in Stuhn Ravine 023E7E; not in the Stuhn entrance trigger area (Gore STUHN scene); zzzAoMMq09 00EFF7 not running |
| VG193 | V I | T | zzzAoMMq05 0098C9 done 41; zzzAoMMq07 00A3FE not done 80 |
| VG194 | I | T | zzzAoMMq06 009E68 done 60 (back from the dream) |
| VG195 | R X | T | zzzAoMMq06BadEnd 4CDF8D done 100 |
| VG196 | L I | T | zzzAoMMqGoodEnd 4D0376 done 20 OR zzzAoMMq10 011B75 done 40 [unconfirmed: the stage where Taranis is named; both are safely after the reveal] |
| VG197 | K SE | T | zzzAoMMqGoodEnd done 120; SE_F; not at the Temple entrance while zzzBMMq01 038524 is at 10 (Gore recap scene) |
| VG198 | R I | T | zzzAoMMqGoodEnd done 120 AND not done 50 (Carene spared) |
| VG199 | V X | T | zzzAoMMq08 00EA8A done 310 |
| VG200 | SE | T | zzzAoMMq08 done 20 AND not done 230; zzzAoMMq10 done 40; after VG30; SE_F |
| VG201 | K | E first time Kaidan near player after CH_BACK | CH_BACK; zzzAoMMq09 done 999; plays before VG53 if both qualify |
| VG202 | R V | T | CH_BACK; zzzAoMqOwl done 20 |
| VG203 | L | T | KEEPER |
| VG204 | I X | T | Vigilant radiant "Bounty Chick Trader" completed [FormID unconfirmed: research lists it in the grouped bounty quests]; zzzLrhMq02 007835:Glenmoril.esm not done 20 (Ja'zel not yet met) |
| VG205 | K | E AFTERFIGHT:bandit | zzzAoMMq10 done 40; K_CRUSH |
| VG206 | K V | T | zzzAoMMq10 done 40; KMD_DONE |
| VG207 | C | T | KEEPER |
| VG208 | R K | T | CH_BACK; zzzBMMq03 038526 done 220 |
| VG209 | SE V | E in Bruiant mansion cells (zzzCONobleMansion01 04A8B9 etc.) | zzzCOMq01 065932 stage 30..39; SE_F; SE_VAMP |
| VG210 | I R | E in Bruiant mansion cells, not Jealousy worldspace 0619A2 | zzzCOMq01 stage 40..59 |
| VG211 | L | T | zzzCOMq01 stage 20..59; zzzLrhMq10 008685:Glenmoril.esm done 170; not in cell COBruiantEntrance 047CFD (Gore scene) |
| VG212 | C I | E in Bruiant Estate 047CFA exterior | G_GONE; zzzCOMq01 stage 30..59; not in COBruiantEntrance 047CFD |
| VG213 | X R | T | G_GONE; player in Tamriel or a Tamriel child world (not Bruiant interiors); after VG25 |
| VG214 | L | T | CH_SUB(zzzCHMemoryQuest01 12C4F4, 20 or 100) |
| VG215 | K V | T | CH_SUB(zzzCHSubQuest07 1265FB, 100) |
| VG216 | C V | T | CH_SUB(zzzCHSubQuest08 1306FA, 40) |
| VG217 | I X | T | CH_SUB(zzzCHSubQuest09 1C1EA1, 20 or 30) |
| VG218 | K | T | CH_SUB(zzzCHSubQuest11 21ED0C, 60) |
| VG219 | L C | T | CH_SUB(zzzCHSubQuest13 51ADBF, 60) |
| VG220 | K L | T | CH_SUB(zzzCHSubQuest14 51FD3E, 40) |
| VG221 | V X | T | CH_SUB(zzzChSubQuest15 55AA72, 140) |
| VG222 | R X | T | CH_SUB(zzzCHSubQuest03 129061, 30) |
| VG223 | I | T | CH_SUB(zzzCHSubQuest04 129BCA, 50) |
| VG224 | K I | T | CH_SUB(zzzCHMemoryQuest10 2A532E, 180) (mercy ending; 300 = bad) |
| VG225 | L K | T | CH_SUB(zzzCHMQ01 1363DB, 8) |
| VG226 | X | T | CH_SUB(zzzCHMemoryQuest04 140225, 60 or 100) |
| VG227 | R L | T | CH_SUB(zzzCHMQ00 12F24E, 90) |
| VG228 | V I | T | CH_SUB(zzzCHGreymarchQuest 13AEE3, 20); after VG227 |
| VG229 | X | T | CH_SUB(zzzCHMQ00, 60); zzzGHMq01 009B59:Glenmoril.esm done 110 |
| VG230 | SE K | T | CH_SUB(zzzCHMQ02 08F2F4, 40); SE_F |
| VG231 | C K | T | CH_BACK |
| VG232 | V C | T | zzzAoMSubQ03 51EAC1 done 30 |
| VG233 | L G | T | KEEPER; G_OK; G_PRE; zzzCOMq01 not started |
| VG234 | AS G | T | HD1MBR 183378:Gore - Vigilant.esp >= 1 and != 3; G_OK; G_PRE; ASHE_REVEAL; ASHE_Q1; not in Beacon Underground 038521 |
| VG235 | SE G | T | G_BACK; SE_F |
| VG236 | I G | E CAMP+NIGHT | G_BACK; after VG69 |
| VG237 | V X | E WATER (exterior river/shore) | G_LOST; after VG73 |
| VG238 | I R | E AFTERFIGHT | zzzAoMMq07 stage 40..59 (Bal defeated, before the mace hand-over) |
| VG239 | AS K | E AFTERFIGHT:daedra | KEEPER; any Vigil bounty radiant running |
| VG240 | R SE | E AFTERFIGHT in Bruiant mansion cells | zzzCOMq01 stage 30..59; zzzCOGuide 43CBAE stage 10..59; SE_F |

### PART 2 - GLENMORIL (VG241-VG280)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| VG241 | R C | T | zzzLrhMq01 007733 done 50; not stage 500..999 |
| VG242 | G X | T | zzzLrhMq02 007835 done 50; G_OK |
| VG243 | K | T | zzzLrhMq02 done 65 |
| VG244 | V I | T | zzzLrhMq02 done 80 |
| VG245 | AS L | T | zzzLrhMq04 007E5E done 30; not stage 30 scene (Brandt reads the clues); ASHE_REVEAL |
| VG246 | G K | T | zzzLrhMq06 0082EE done 70; not stage 100..140 scenes; G_OK |
| VG247 | I X | T | zzzLrhMq08 008431 stage >= 8 [unconfirmed: Ja'zel's door scene is stages 0..7] |
| VG248 | L I | T | zzzLrhMq10 008685 done 45; not stage 70..80 |
| VG249 | G K | T | zzzLrhMq10 done 50; not stage 70..80, 160..170; G_OK |
| VG250 | L X | T | zzzLrhSqRoadRoller 614517 done 110 |
| VG251 | R V | T | zzzLrhSqRoadRoller done 240 |
| VG252 | K | T | zzzLrhQTorvesardContact 474F0F done 70 |
| VG253 | L | T | zzzLrhSubQuest01 007B93 done 20; player not in Old Well 007A50 |
| VG254 | C R | T | zzzGHMq01 009B59 stage 10..29 |
| VG255 | G K | T | zzzGHMq01 done 20; G_OK |
| VG256 | V K | T | zzzGHMq01 done 40 |
| VG257 | AS SE | T | zzzGHMq01 done 55; not stage 90..130; SE_F; ASHE_REVEAL |
| VG258 | L I | T | zzzGHMq01 done 150 |
| VG259 | SE | T | zzzGHMq01 done 140; not stage 255+; SE_F |
| VG260 | X I | T | zzzGHMq01 done 180 |
| VG261 | V X | T | zzzGHMq02 00E3EC done 50; not stage 30..60 (briefing and flight scenes) [unconfirmed: followers aboard] |
| VG262 | R SE | T | zzzGHMq02 done 310; SE_F |
| VG263 | K | T | zzzGHMq02 done 170; not stage 280..300 |
| VG264 | V G | T | zzzGHMq06 017733 done 240; G_OK |
| VG265 | G I | T | zzzGHMq03 01230D done 130; not stage 280..290; G_OK |
| VG266 | R C | T | zzzGHMq03 done 150; not stage 280..290 |
| VG267 | L K | T | zzzGHMq03 done 260; not stage 280..290 |
| VG268 | R AS | T | zzzGHMq03 done 310; ASHE_HIRED |
| VG269 | R X | T | zzzGHMq03 done 310; after VG266 |
| VG270 | L | T | zzzGHMq03Sub01 012962 stage 30..84 or done 140; MG_JOIN |
| VG271 | V K | T | zzzGHMq03Sub01 done 110; K_CRUSH |
| VG272 | C R | T | zzzGHMq04Sub01 014C39 done 45; not stage 90 (Black Owl offer) |
| VG273 | L V | T | zzzGHmq06Sub01 02C265 done 10; VAL_FATHIS |
| VG274 | R | T | zzzGHmq06Sub01 done 70 |
| VG275 | L K | T | zzzLaMMq01 0B1758 done 30 |
| VG276 | I V | T | zzzLaMMq02 0E9E2A done 70; not stage 100..150; after VG108 |
| VG277 | X | E rest after Ozwald's death | zzzLaMMq02 done 150; zzzLaMMq03 103B86 stage 10..30 [unconfirmed: followers aboard] |
| VG278 | V G | T | zzzLaMMq05 1329BD done 35; not stage 100..110, 130..150; G_OK |
| VG279 | R L | T | zzzLaMMq05 done 70; not stage 100..110, 130..150 |
| VG280 | I | T | zzzRevDAAzura 355287 done 10; IN_BLACKSPRING(I) |

### PART 3 - UNSLAAD (VG281-VG310)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| VG281 | X | T | zzzCrbMq01 01D8FF done 50; zzzCrbMq02 02299D done 20; IN_UNSLAAD; not Hoarfrost stage 30..60 |
| VG282 | L K | T | zzzCrbsq01 022986 running or done; DB |
| VG283 | R G | T | RAD(Amaranth Flower 3533FE); G_OK |
| VG284 | V I | T | zzzCrbSq02 05268B done 20 |
| VG285 | L X | T | zzzCrbMq03 112A83 done 30 (after the 23..25 ghost scene) |
| VG286 | L C | T | RAD(Picture Book 350B7F) |
| VG287 | R SE | T | zzzCrbMq05 117B3F done 10; not stage 20..40; SE_F; SE_VAMP |
| VG288 | AS SE | T | zzzCrbMq05 done 70 (not during 80..110); DLC1VQ08 completed; ASHE_LOGS; SE_F |
| VG289 | I | T | zzzCrbMq05 done 130 (after the ghost walk); not stage 140..150 or 160..190 |
| VG290 | K | T | zzzCrbMq05 done 40; not stage 80..110, 140..150, 160..190; DB |
| VG291 | R K | T | zzzCrbMq05 done 250; zzzCrbEpilogue 1EC845 scene not playing |
| VG292 | L | T | zzzCrbMq07 1DFDFB done 120 |
| VG293 | G K | T | zzzCrbSq04 364E2B done 20; SHOUT1; G_OK |
| VG294 | I K | T | RAD(Dregs of Alduin 34E336) |
| VG295 | V AS | T | zzzCrbSq05 376B99 started; IN_UNSLAAD; not stage 110..120, 150..160; ASHE_HIRED |
| VG296 | C R | T | RAD(Lost Kanra 3441D4); zzzLrhMq03 00790A:Glenmoril.esm done 40 |
| VG297 | L X | T | zzzCrbMq01 done 50; IN_UNSLAAD; Sina met [unconfirmed check: no quest for Sina; use a talked-to flag on Sina's ref if one exists, else player within 1000 units of Sina] |
| VG298 | C AS | T | zzzCrbMq01 done 50; IN_UNSLAAD; Soul Gem Pot merchant met [unconfirmed check, as VG297]; ASHE_REVEAL |
| VG299 | R L | T | zzzCrbSq03 33F0E0 done 10; zzzGHMq04 0147BD:Glenmoril.esm done 210 |
| VG300 | V K | T | RAD(Briarheart Brandy 3676B2) |
| VG301 | V I | T | RAD(Intruder 350BA7); Aisha alive (not zzzCrbMq02 done 320 unless zzzCrbSqResurrection 11023D done 10) |
| VG302 | G C | T | zzzCrbBqStuhnTsun 3C8752 done 20; G_OK |
| VG303 | V | T | zzzCrbSq05 done 160 |
| VG304 | R X | T | UN_BACK |
| VG305 | L C | T | UN_BACK; zzzCrbMq08 465EBF done 140 |
| VG306 | K | T | UN_BACK; zzzCrbMq09 done 40 AND not done 140 (small offering) |
| VG307 | G | T | UN_BACK; G_BACK; G_OK |
| VG308 | R X | T | zzzCrbMq10 47A38C done 50 |
| VG309 | C K | E AFTERFIGHT | Woodland Man Hunt 48E803 running |
| VG310 | G X | E AFTERFIGHT | Infected 3676A3 running; G_OK |

## 4. Open items
- VG196: exact stage where Carene's husband is named (both gates used are safely after it).
- VG204: FormID of Vigilant's "Bounty Chick Trader" radiant.
- VG247: Ja'zel's hidden-door scene end stage.
- VG297 / VG298: "has met" checks for Sina and the Soul Gem Pot merchant.
- Radiant completion stages (RAD): 20 vs 30 per quest.
- Followers aboard the airship (VG261, VG277) and in the Black Spring (VG280), as in part 1.
