# 33 DARK BROTHERHOOD - trigger rows (prefix DB, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\33 DARK BROTHERHOOD.txt`.
Sources: `research\triggers\vanilla_gates.md` (B1 DB02/DB03 gates, B3 DB silences), `research\triggers\kaidan_block.md` (KDBro), `research\bibles\*.md` (ashe.md 6 for Ashe gates, serana.md 6, val.md, xelzaz.md).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana/Ashe Free rows in `triggers\20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Note: the talk-ID prefix "DB" is unrelated to the TRIGGERS.md gate code `DB` (Dragonborn = real Watchtower kill). No talk in this file uses that gate, and no line says "Dragonborn".

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player).

## 1. Silence (already in WorldQuiet, repeated here)
- DB02 (01EA51:Skyrim.esm) stage 10..39 - the abandoned shack. [CONFIRMED]
- DB04 (01EA53) stage 10..49 - eavesdropping on Cicero / the Night Mother. [CONFIRMED]
- DB10 (03CEDA) running - the Sanctuary burning. Winner is `Kaidan - Immersive Features.esp`, stages vanilla. [CONFIRMED]
- DB11 (01EA59) stage 5..199 - the Emperor job (Katariah). [CONFIRMED]
- DB05 (01EA54) running AND in the Solitude Temple of the Divines - the wedding. [UNC, no scene lock]
- Kaidan's KDBro (FE62C9:Kaidan - Immersive Features.esp) scenes: covered by Kaidan's Free (IsInScene + STFU globals that KaiDBShutdownScript raises). No talk in this file names a KDBro beat for Kaidan (Astrid/Babette/Nazir/Arnbjorn/Gabriella/Festus scenes, GourmetGuard, PostCoffinFG, MaroKill): Kaidan is kept out of the Gourmet, Gaius Maro and family-member talks, and his lines never say whether he joined.

## 2. Gate codes used in this file (new)

Branch:
- `DB_JOIN` (existing, tightened) = DB02 (01EA51) stage 50 done AND stage 220 NOT done. Stage 50 = AddToFaction DarkBrotherhoodFaction (01BDB3). [CONFIRMED stage 50; UNC that 50 never fires on the kill-Astrid path, hence the 220 guard]
- `DB_ASTRID` = DB02 stage 220 done (killed Astrid; the Destroy path). [CONFIRMED]
- `DB_EITHER` = DB_JOIN or DB_ASTRID.
- `DB_SHACKBACK` = E event: first controller tick where DB_EITHER is true and the party is Free near the player (they were left behind during the kidnap). Fires once; only DB1 uses it.

Joined path (all Skyrim.esm; DB06-DB09 EditorID-to-quest mapping is [UNC], FormIDs to look up at build, expected 01EA55..01EA58):
- `DB_HOME` = DB02 stage 200 done ("officially welcomed by Astrid"). [CONFIRMED]
- `CICERO` (existing) = DB03 (01EA52) stage 10 done. [CONFIRMED]
- `DB_LISTENER` = DB04 (01EA53) completed (Night Mother has spoken; player is Listener). [UNC completion stage, likely 200]
- `DB_BRIDE` = DB05 (01EA54) completed ("Bound Until Death", Vittoria Vici). [UNC stage]
- `DB_GAIUS` = "Breaching Security" completed (Gaius Maro killed, letter planted). [UNC quest DB06?]
- `DB_CURE` = "The Cure for Madness" completed. [UNC quest DB07?] Branch: `CICERO_ALIVE` = Cicero actor (unique NPC `Cicero`, Skyrim.esm [UNC FormID]) GetDead == 0; `CICERO_DEAD` = GetDead == 1.
- `DB_GOURMET` = "Recipe for Disaster" stage where the Gourmet is dead (or quest completed). [UNC quest DB08? / stage]
- `DB_DOUR` = "To Kill an Empire" completed (Castle Dour feast, the decoy Emperor). [UNC quest DB09?]
- `DB_FIRE` = DB10 (03CEDA) completed ("Death Incarnate"). [CONFIRMED FormID; UNC completion stage]
- `DB_SITHIS` = DB11 (01EA59) completed / stage 200 ("Hail Sithis!"). [CONFIRMED FormID]
- `DB_FIRSTCONTRACT` = any of DB_BRIDE, or Nazir side-contract quest (DBSideContract*, [UNC]) completed once.
- `DB_NAZIRPAY` = E event: Nazir side-contract reward handed over (DBSideContract* reward stage set). [UNC quest/stage]

Destroy path:
- `DB_MARO` = DBDestroy ("Destroy the Dark Brotherhood!", Skyrim.esm [UNC FormID]) stage where the player has spoken to Commander Maro. [UNC stage]
- `DB_PURGE` = DBDestroy stage where the Sanctuary is cleared (Astrid's family dead). [UNC stage; fall back to quest completed]
- `DB_PAID` = DBDestroy completed (Maro's reward given). [UNC]
- `BABETTE_DEAD` = Babette actor GetDead == 1. [UNC FormID]

Ashe (ashe.md section 6, `Ashe - Fire and Blood.esp`):
- `ASHE_HIRED` = MM_AsheIntro (0A7946) completed.
- `ASHE_REVEAL` = MM_FriendshipQuest (1A9DEE) stage 70 done (or var MM_AutomatonReveal == 1).
- `ASHE_Q1` = MM_AMQ_01 (756FEA) completed ("A Borrowed Soul"; she has told Luna about Aryo's murder).
- `ASHE_ROLEN1` = MM_AMQ_03 (BC5D8F) completed (she has found the assassin).

Others (existing codes): `SERANA` (DLC1VQ02 5), `SER_VAMP` (Serana HasKeyword Vampire == 1), `VAL_FATHER` (Val003 completed), `K_CRUSH`, `K_TOG+`, `K_LOVE+` (TRIGGERS.md section 4), `after:Q14`.

Places / events:
- `LOC:BlackDoorFalkreath` = player within ~800 units of the Falkreath Sanctuary Black Door, exterior (Falkreath Sanctuary location `DarkBrotherhoodSanctuaryLocation` [UNC FormID]; door ref [UNC]). First time only.
- `LOC:SanctuaryOutside` = exterior, within ~2000 units of that door (the pond). Repeatable until played.
- `LOC:DawnstarSanctuaryDoor` = player within ~800 units of the Dawnstar Sanctuary door, exterior (`DawnstarSanctuaryLocation` [UNC FormID]). First time only.
- `CITY:Falkreath` = arrival in FalkreathLocation (hold capital) [existing pattern].
- `AFTERFIGHT:dbassassin` = player combat ends and the last combat target was in DarkBrotherhoodFaction (01BDB3) or wore Shrouded armor (base `ArmorDBCuirass`* [UNC]) and is dead. [UNC best test]
- `SHROUDED` = player wearing any Shrouded cuirass (keyword or base list [UNC]).
- `INN`, `CAMP`, `NIGHT` as TRIGGERS.md section 4.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| DB1 | K G P | E DB_SHACKBACK | DB_EITHER |
| DB2 | K P | T | DB_EITHER; after DB1 |
| DB3 | L P | T | DB_EITHER |
| DB4 | R V | T | DB_EITHER |
| DB5 | A I | T | DB_EITHER; ASHE_REVEAL |
| DB6 | X P | T | DB_EITHER |
| DB7 | C K | E INN | DB_EITHER |
| DB8 | S G | T | DB_EITHER; SERANA |
| DB9 | L P | E LOC:BlackDoorFalkreath | DB_JOIN |
| DB10 | X G | E LOC:SanctuaryOutside | DB_HOME |
| DB11 | V K P | T | DB_JOIN; K_CRUSH; SHROUDED (player wearing it) |
| DB12 | R S | T | DB_HOME; SERANA |
| DB13 | I S | T | DB_HOME; SERANA |
| DB14 | L X | T | DB_HOME; after DB10 |
| DB15 | C G | T | DB_HOME |
| DB16 | I L | T | DB_HOME |
| DB17 | X P | T | DB_HOME; DB_FIRE NOT done (Veezara alive) |
| DB18 | G V | T | DB_HOME; VAL_FATHER; DB_FIRE NOT done (Gabriella alive) |
| DB19 | G K | T | DB_HOME |
| DB20 | L R | T | DB_HOME; DB_FIRE NOT done (Festus alive) |
| DB21 | R V P | T | DB_HOME |
| DB22 | A P | E LOC:SanctuaryOutside | DB_HOME; ASHE_Q1 |
| DB23 | A I | T | DB_HOME; ASHE_Q1; ASHE_ROLEN1 NOT done |
| DB24 | K P | T | DB_HOME; K_TOG+ |
| DB25 | C R | T | CICERO; DB_JOIN |
| DB26 | L S | T | CICERO; DB_JOIN; SERANA |
| DB27 | K P | T | DB_LISTENER; DB_JOIN |
| DB28 | C X | T | DB_LISTENER; DB_JOIN |
| DB29 | L K P | T | CICERO; DB_JOIN |
| DB30 | I G | T | DB_CURE; CICERO_ALIVE; after:Q14 |
| DB31 | R L P | T | DB_CURE; CICERO_DEAD |
| DB32 | X V | T | DB_LISTENER; DB_JOIN |
| DB33 | R P | T | DB_LISTENER; DB_JOIN |
| DB34 | A S | T | DB_LISTENER; DB_JOIN; ASHE_REVEAL; SERANA |
| DB35 | V R | T | DB_BRIDE |
| DB36 | G P | T | DB_BRIDE |
| DB37 | X P | T | DB_DOUR |
| DB38 | R L | T | DB_GOURMET |
| DB39 | S X | T | DB_DOUR; SERANA |
| DB40 | L V | T | DB_DOUR; DB_SITHIS NOT done |
| DB41 | L A | T | DB_GAIUS; ASHE_Q1 |
| DB42 | C R | E DB_NAZIRPAY | DB_JOIN |
| DB43 | S G | T | DB_FIRSTCONTRACT; SERANA; after DB36 if DB_BRIDE |
| DB44 | K X | T | DB_FIRSTCONTRACT |
| DB45 | V P | T | DB_HOME |
| DB46 | G A | T | DB_JOIN; ASHE_HIRED; ASHE_Q1 NOT done |
| DB47 | I P | T | DB_FIRE |
| DB48 | S V | T | DB_FIRE; SERANA |
| DB49 | X G | T | DB_FIRE |
| DB50 | L C P | E LOC:DawnstarSanctuaryDoor | DB_FIRE |
| DB51 | K P | T | DB_FIRE; K_TOG+ |
| DB52 | L I | T | DB_SITHIS |
| DB53 | K V | T | DB_SITHIS; after DB52 (Lucien already upset) |
| DB54 | S P | T | DB_SITHIS; SERANA |
| DB55 | C I | T | DB_SITHIS |
| DB56 | X A | T | DB_SITHIS; ASHE_Q1; after DB10 and DB22 |
| DB57 | G K P | T | DB_ASTRID |
| DB58 | L V | T | DB_ASTRID; DB_MARO |
| DB59 | X P | T | DB_PURGE |
| DB60 | A P | T | DB_PURGE; ASHE_Q1 |
| DB61 | S I | T | DB_PURGE; BABETTE_DEAD; SERANA |
| DB62 | C G | T | DB_PURGE |
| DB63 | R V P | E in Falkreath Sanctuary interior | DB_PURGE |
| DB64 | G R | T | DB_PURGE |
| DB65 | L P | T | DB_PURGE |
| DB66 | S X | T | DB_PURGE; SERANA |
| DB67 | I K | T | DB_PURGE |
| DB68 | K V | T | DB_PAID |
| DB69 | A K | T | DB_PURGE |
| DB70 | S G | E CAMP or INN, NIGHT | DB_PURGE; SERANA; SER_VAMP |
| DB71 | K G | E AFTERFIGHT:dbassassin | DB_EITHER |
| DB72 | X P | E AFTERFIGHT:dbassassin | DB_EITHER |
| DB73 | C R | E AFTERFIGHT:dbassassin | DB_EITHER |
| DB74 | A S | E AFTERFIGHT:dbassassin | DB_EITHER; SERANA |
| DB75 | L G P | E CITY:Falkreath | DB_EITHER |
| DB76 | R L | T | DB_EITHER |
| DB77 | I G | E INN | DB_EITHER |
| DB78 | V A | T | DB_EITHER |
| DB79 | S C | E LOC:SanctuaryOutside | DB_EITHER; SERANA |
| DB80 | K P | E CAMP | DB_EITHER; K_LOVE+; after DB2 |

## 4. Notes for the build
- Branch safety: every Part 2-5 row carries a joined gate (DB_JOIN / DB_HOME or a later joined quest); every Part 6 row carries DB_ASTRID or a DBDestroy gate. Parts 1 and 7 are DB_EITHER only, and their lines fit both roads.
- Death checks: DB17, DB18, DB20 require the named Sanctuary member still alive (DB_FIRE not done). DB61 needs BABETTE_DEAD. DB30/DB31 branch on Cicero's death state.
- Ashe: anything naming Aryo's murder needs ASHE_Q1. DB46 is the pre-Q1 "shut door" talk and must NOT play after ASHE_Q1. DB23 must not play after ASHE_ROLEN1 (she knows the killer then).
- Romance: DB11 is K_CRUSH (Luna oblivious, misreads the stare as the stitching). DB24/DB51 K_TOG+, DB80 K_LOVE+ (Kaidan says "I love you"; Luna never says it). DB78 Val/Ashe is friendly rivalry, ungated.
- Existing coverage avoided: Q13 (Xelzaz/Inigo "complicated", "I will stay for her"), Q14 (Gore "can we keep him" - DB30 calls back to it), Xelzaz/Remi DBBanter1/2 and Served Cold (no Xelzaz/Remi pair here), the many Inigo "my parents were assassins" talks with Xelzaz (no Xelzaz/Inigo pair here), HF75/HF76 (Grelod, Aventus), Gore's 200-septim gag.
- No line uses "Dragonborn", Kaidan's cult, or a beard.
