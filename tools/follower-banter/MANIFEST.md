# Follower Banter - production manifest (target ~3,800 talks)

Already written (Desktop, 221): batch 1 (A,B,C), Kaidan and Luna (K), batch 2 (R,X,I,L,M,G), quests (Q), batch 3 (P,W,D,KX), seasons/holidays/lost (S,H,N).
New scripts go to `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\`, triggers to `_tools\follower-banter\triggers\`.
Every writer reads: STYLE-GUIDE.md, TRIGGERS.md (sections 4-5), the bibles for its speakers, its research file, and skims the existing Desktop scripts so it doesn't repeat them.

| Wave | Prefix | File | Scope | Count | Research | Status |
|---|---|---|---|---|---|---|
| 1 | DR | 10 DRAGONBORN SOLSTHEIM | Dragonborn DLC: Solstheim, Raven Rock, Skaal, Thirsk, Tel Mithryn/Neloth, Miraak, Black Books, Apocrypha (reunions only), Redcap's homeland, Xelzaz's Telvanni angle, Val vs Mora | 140 | dlc_cc_missives_3dnpc.md | |
| 1 | LT | 11 LEGACY OF THE DRAGONBORN | museum rooms, Explorers Society, digs, relic quests, Auryen, haunting, robbery, gala | 140 | lotd.md | done 140 |
| 1 | BR | 12 BRUMA AND MOONPATH | Beyond Skyrim Bruma (90) + Moonpath to Elsweyr (60) | 150 | bruma_moonpath_wyrmstooth_etc.md | |
| 1 | WS | 13 WYRMSTOOTH SIRENROOT FORGOTTEN CITY SAINTS | Wyrmstooth 60, Sirenroot 35, Forgotten City 25 (entrance/after only), S&S SEC 30, Cursed Tribe 10 | 160 | bruma_moonpath_wyrmstooth_etc.md | done 160 |
| 1 | CC | 14 CREATION CLUB | every active Creation with a quest; The Cause gated after Kaidan's KMDQuest done for any cult reference | 180 | dlc_cc_missives_3dnpc.md, 00_inventory.md | |
| 1 | MN | 15 MISSIVES BOUNTIES INTERESTING NPCS | Missives/bounty jobs 50, 3DNPC 80 | 130 | dlc_cc_missives_3dnpc.md | done 130 |
| 2 | DG | 20 DAWNGUARD | with Serana as a speaker | 120 | dlc_cc_missives_3dnpc.md + serana.md | done 120 |
| 2 | HF | 21 HEARTHFIRE AND HOME | building, kids, spouse life, the party at home | 100 | dlc_cc_missives_3dnpc.md | |
| 2 | VG | 22 VIGILANT GLENMORIL UNSLAAD | 80 / 60 / 50; never collide with Gore - Vigilant | 190 | vigilant_glenmoril_unslaad.md | needs research |
| 3 | MQ | 30 MAIN QUEST DEEP | 120 | vanilla_gates.md | writing |
| 3 | CW | 31 CIVIL WAR | 70 | vanilla_gates.md | writing |
| 3 | TG | 32 THIEVES GUILD | 80 | | |
| 3 | DB | 33 DARK BROTHERHOOD | 80 | vanilla_gates.md | done 80 |
| 3 | CP | 34 COMPANIONS | 70 (Kaidan's KaiComp must not be contradicted) | | |
| 3 | MG | 35 COLLEGE | 70 (Luna is a mage - big Luna file) | | |
| 3 | DA | 36 DAEDRIC QUESTS | 100 (every prince) | | done 100 |
| 3 | SQ | 37 VANILLA SIDE QUESTS AND HOLDS | 150 | | |
| 4 | PL | 40 PLACES AND LANDMARKS | named dungeons, ruins, towns, wonders | 180 | | |
| 4 | NP | 41 FAMOUS NPCS | Ulfric, Tullius, Elisif, Balgruuf, Nazeem, Belethor, Lydia... | 120 | | done 120 |
| 4 | CR | 42 CREATURES AND LOOT | dragons by type, giants, trolls, chaurus, masks, artifacts | 100 | | done 100 |
| 4 | PA | 43 WHAT LUNA DOES | crimes, jail, wealth, levels, crafting, alchemy, enchanting, reading, swimming, horses, carriages, shouts, transformations | 160 | | done 160 |
| 4 | CB | 44 IN THE FIGHT | 2-4 line barks during/after fights | 150 | | |
| 4 | PY | 45 PARTY LIFE | campfires, games, songs, stories, arguments, apologies | 180 | | |
| 4 | PR | 46 PAIR ARCS | every pair's friendship growing in 3-5 steps, incl. Serana/Ashe | 220 | | done 220 |
| 4 | KL | 47 KAIDAN AND LUNA DEEP | crush (Luna oblivious) -> married | 180 | | |
| 4 | SE | 48 SERANA | Serana with everyone | 80 | serana.md | |
| 4 | AS | 49 ASHE | Ashe with everyone | 80 | ashe.md | |
| 4 | LN | 50 LUNA THE MAGE | Luna's books, spells, lore pedantry | 80 | | |
| 4 | WT | 51 SEASONS WEATHER TIME MORE | 80 | | done 80 |
| 4 | EV | 52 ASK THE PARTY LINES | "What does everyone think?" topic + "nothing new" + "not now" lines for each follower | ~130 lines | TRIGGERS.md §7 | done 170 lines (10 followers x 16 + 10 Luna) |

Total new: about 3,610 + 221 written = about 3,830.

## EXPANSION to ~8,500 talks (user 10-18) - waves 5-9
Part-2 files CONTINUE their prefix numbering (e.g. DR141 onward) in a new file "<nn>b <NAME> 2". Writers read their part-1 file FULLY and must not repeat its topics/jokes; they also run `python dup_scan.py` and fix any repeat involving their new IDs.

| Wave | Prefix (continue) | File | Add | Notes | Status |
|---|---|---|---|---|---|
| 5 | KL | 47b KAIDAN AND LUNA DEEP 2 | 200 | from KL181 | done 200 (KL181-KL380) |
| 5 | RV (new) | 53 RIVALRY | 200 | all five rivals, every romance stage combination | |
| 5 | PY | 45b PARTY LIFE 2 | 250 | | |
| 5 | PR | 46b PAIR ARCS 2 | 250 | next steps of every arc + new pairs incl. Luna-with-each | |
| 5 | FL (new) | 54 FOLLOWER QUESTS CROSSTALK | 200 | the party on each follower's personal quests (gated, never collide) | done 200 |
| 5 | TV (new) | 55 TRAVEL AND THE ROAD | 200 | roads, horses, carriages, boats, mountains, rivers, long walks | done 200 |
| 5 | WE (new) | 56 WORLD ENCOUNTERS | 150 | vanilla world-encounter events + Immersive Encounters | done 150 |
| 5 | IN (new) | 57 INNS AND TOWN LIFE | 150 | each inn, bards, games, rooms, markets | done 150 |
| 6 | PL | 40b PLACES AND LANDMARKS 2 | 250 | | done 250 |
| 6 | SQ | 37b VANILLA SIDE QUESTS 2 | 200 | SQ151-SQ350 | done 200 |
| 6 | CB | 44b IN THE FIGHT 2 | 200 | | |
| 6 | PA | 43b WHAT LUNA DOES 2 | 150 | from PA161 | done 150 |
| 6 | NP | 41b FAMOUS NPCS 2 | 150 | | done 150 (NP121-NP270) |
| 6 | CC | 14b CREATION CLUB 2 | 150 | CC181-CC330; Serana/Ashe added; inactive CCs skipped | done 150 |
| 6 | MN | 15b MISSIVES AND NPCS 2 | 120 | MN131-MN250 | done 120 |
| 6 | VG | 22b VIGILANT GLENMORIL UNSLAAD 2 | 120 | | done 120 (VG191-VG310) |
| 7 | DR | 10b DRAGONBORN 2 | 100 | | done 100 (DR141-DR240) |
| 7 | LT | 11b LOTD 2 | 100 | | done 100 (LT141-LT240) |
| 7 | DG | 20b DAWNGUARD 2 | 100 | DG121-DG220 | done 100 |
| 7 | MQ | 30b MAIN QUEST 2 | 100 | | done 100 (MQ121-MQ220) |
| 7 | CR | 42b CREATURES AND LOOT 2 | 100 | CR101-CR200 | done 100 |
| 7 | SE | 48b SERANA 2 | 100 | SE81-SE180 | done 100 |
| 7 | AS | 49b ASHE 2 | 100 | AS81-AS180 | done 100 |
| 7 | LN | 50b LUNA THE MAGE 2 | 100 | | done 100 (LN81-LN180) |
| 8 | WT | 51b SEASONS WEATHER 2 | 100 | | done 100 (WT81-WT180) |
| 8 | SR (new) | 58 SURVIVAL AND NEEDS | 100 | SunHelm/Frostfall/Campfire hunger, cold, tiredness | done 100 |
| 8 | OM (new) | 59 OTHER QUEST MODS | 120 | DAc0da, Olenveld, Gray Cowl (if not in CC), Immersive Encounters quests, the rest of 00_inventory | done 120 (Gray Cowl left to CC file) |
| 8 | BR | 12b BRUMA AND MOONPATH 2 | 80 | | done 80 (BR151-BR230) |
| 8 | WS | 13b WYRMSTOOTH ETC 2 | 80 | | done 80 (WS161-WS240) |
| 8 | HF | 21b HEARTHFIRE AND HOME 2 | 80 | | done 80 (HF101-HF180) |
| 8 | CW | 31b CIVIL WAR 2 | 80 | | done 80 (CW71-CW150) |
| 9 | DA | 36b DAEDRIC 2 | 80 | | done 80 (DA101-DA180) |
| 9 | TG | 32b THIEVES GUILD 2 | 60 | | done 60 (TG81-TG140) |
| 9 | DB | 33b DARK BROTHERHOOD 2 | 60 | | done 60 (DB81-DB140) |
| 9 | CP | 34b COMPANIONS 2 | 60 | | done 60 (CP71-CP130) |
| 9 | MG | 35b COLLEGE 2 | 60 | | done 60 (MG71-MG130) |
| 10 | BF (new) | 60 BEEING FEMALE FAMILY | 100 | Luna's pregnancy and children with Kaidan (Beeing Female NG); only when Kaidan is the father; BF_* gates in its trigger file | done 100 (BF1-BF100) |
| 11 | LT | 11c LOTD 3 | 150 | the whole museum journey (empty halls to the Vault); 113 talks Lucien with Remi/Xelzaz; running bits: Lucien's ledger, card wars, Finds Board, quiz; DISP_N = DBM_DisplayCount bands | done 150 (LT241-LT390) |
| 11 | FL | 54b FOLLOWER QUESTS CROSSTALK 2 | 120 | before / during (follower absent, no scenes) / after on every follower's quest line, incl. Serana (SDA) and Ashe; rivals by stage; new gate codes in its trigger file | done 120 (FL201-FL320) |
| 11 | WF (new) | 61 WANDERERS FAIR | 60 | The Wanderer's Fair (SkyrimFair.esp): stalls, stage, archery, Claudius/Garrick/roof horse, passport, Redcap overwhelmed, Inigo delighted, rivals and the 'prize', Luna lost; gate = SkyrimFairWorld | done 60 (WF1-WF60) |
| 11 | RV | 53b RIVALRY 2 | 100 | EARLY competition: Kaidan, Gore, Val before anyone is together with Luna (STEP0 best-companion contests, K_CRUSH, early G/V flirting) - packs, cooking, doors, showy fighting, directions she ignores; Luna oblivious; party notices; new code EARLY in its trigger file | done 100 (RV201-RV300) |
| 11 | SL (new) | 62 SOLSTHEIM BEFORE THE DLC | 60 | Solstheim before DLC2MQ01 starts (gate PRE_DLC2 = DLC2MQ01 5 and 20 not done, not in DLC2SolstheimWorld): Windhelm docks, Grey Quarter, Redcap homesick (RC_HOMESICK), Xelzaz on Telvanni/Redoran, Val's Dunmer half, Lucien's letter | done 60 (SL1-SL60) |
| 11 | KP (new) | 63 KAIDANS PEOPLE | 60 | Farkas, Vilkas, Aela, Erik woven in lightly (never speak); KaiComp, honeymoon and IF frathouse topics untouched; NO_PEOPLE_FOLLOWING on every row | done 60 (KP1-KP60) |
Planned add: ~4,700 -> total ~8,580.
