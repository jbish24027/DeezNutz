# 33b DARK BROTHERHOOD 2 - trigger rows (prefix DB, DB81-DB140, 60 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\33b DARK BROTHERHOOD 2.txt`.
Part one and its gate codes: `triggers\33 DARK BROTHERHOOD.md` (sections 1-2 apply here unchanged). Sources: `research\triggers\vanilla_gates.md` (B1, B3), `research\triggers\kaidan_block.md` (KDBro), `research\bibles\*.md`. Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana / Ashe Free rows and S_/A_ codes are in `triggers\20 DAWNGUARD.md` sections 1 and 3. Marks: **[UNC]** = unconfirmed, check at build.

Note: the talk-ID prefix "DB" is unrelated to the TRIGGERS.md gate code `DB` (Dragonborn). No talk in this file uses that gate, and no line says "Dragonborn".

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player; no Free check, but player must not be in dialogue).

## 1. Silence

Same as part one (33 DARK BROTHERHOOD.md section 1): DB02 10..39 (shack), DB04 10..49 (eavesdrop), DB10 running (fire), DB11 5..199 (Emperor), DB05 in the Solitude Temple [UNC], and Kaidan's KDBro scenes via Free(K) (IsInScene + the STFU globals KaiDBShutdownScript raises).

Kaidan rule kept from part one: no K talk names a Sanctuary family member, the Gourmet, Gaius Maro or Commander Maro's kill, and no K line says whether he joined. K talks here: DB85, DB86, DB89, DB103, DB106, DB111, DB114, DB116, DB118, DB123, DB127, DB136, DB137. DB118 and DB123 name Nazir / the family only on the **Destroy** path (DB_PURGE), where KDBro has no scenes.

## 2. New gate codes (this file)

Reused from part one: `DB_JOIN`, `DB_ASTRID`, `DB_EITHER`, `DB_HOME`, `CICERO`, `DB_LISTENER`, `DB_FIRE`, `DB_SITHIS`, `DB_FIRSTCONTRACT`, `DB_PURGE`, `LOC:BlackDoorFalkreath`, `LOC:SanctuaryOutside`, `CITY:Falkreath`, `AFTERFIGHT:dbassassin`, `SHROUDED`, `ASHE_REVEAL`, `ASHE_ROLEN1`, `SERANA`, `VAL_FATHER`, `K_CRUSH`, `K_TOG+`, `K_LOVE+`, `K_ANY`, `V_ANY`, `G_ANY`.

Joined path (Skyrim.esm unless noted):
- `DB_SENTENCED_E` = Ennodius Papius dead while DB03 "Sentenced to Death" (01EA52) is running or done (`GetDead` on the unique actor Ennodius Papius **[UNC FormID]**).
- `DB_SENTENCED_N` = Narfi dead, same rule (unique actor Narfi **[UNC FormID]**). Also require DB_JOIN so a random Narfi death never fires it.
- `VEEZARA_ALIVE` = DB_FIRE not done (as part one DB17). `ASTRID_ALIVE` = DB_FIRE not done.
- `DB_MOURNING` = "Mourning Never Comes" (Muiri's contract) completed **[UNC EditorID; a Night Mother contract quest in the DB05-DB09 block]**.
- `DBSC:<target>` = Nazir's side contract for that target completed. Targets used: Lurbuk, Hern, Maluril, Agnis, Anoriath **[UNC: DBSideContract* EditorIDs/FormIDs; fall back to the target actor GetDead == 1 with DB_LISTENER]**.
- `SHROUDED_HOOD` = player wearing the Shrouded Cowl or Shrouded Hood **[UNC base FormIDs]**.
- `CICERO_JOURNAL` = player has read Cicero's Journal (any volume) **[UNC book FormIDs; fallback CICERO + DB_LISTENER]**.
- `CICERO_ALIVE` (part one) = Cicero GetDead == 0.
- `SHADOWMERE_RIDE` = event: player first mounts Shadowmere **[UNC actor FormID]**. Remembered as a flag; T talks below need it set.
- `CAST:spectral` = event: combat ends in which the player cast the Spectral Assassin summon (Lucien Lachance) **[UNC spell FormID]**.
- `DB_CONTRACTS>=3` = DB_LISTENER and 3+ contracts done (count DBSC:* plus DB_BRIDE / DB_GAIUS) **[UNC; fallback DB_LISTENER + 5 in-game days]**.
- `LOC:DawnstarSanctuary` = player inside the Dawnstar Sanctuary interior **[UNC cell/location FormID]**.
- `BABETTE_ALIVE` = Babette GetDead == 0 (part one has BABETTE_DEAD).
- `DAWNSTAR_REBUILD` = DB_SITHIS and the Dawnstar restoration quest ("Where You Hang Your Enemy's Head") started **[UNC EditorID; fallback DB_SITHIS + 2 in-game days]**.

Either path:
- `BLADEOFWOE` = player has the Blade of Woe in inventory **[UNC FormID]** (Astrid gives it on the joined path; it is on her body on the destroy path).
- `GORE_READING` = Remi-Gore reading lessons started (HLIOGoreReading >= 1) **[UNC]**, as in 32b TG82.

Ashe: `ASHE_ROLEN1` (part one) = MM_AMQ_03 completed (she has found Rolen, her father's killer).

Places / events: `INN`, `CAMP`, `NIGHT`, `HOUSE` as TRIGGERS.md section 4.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| DB81 | G R | T | DB_EITHER; GORE_READING |
| DB82 | R S | T | BLADEOFWOE; SERANA |
| DB83 | X P | T (exterior) | DB_EITHER |
| DB84 | L P | T | DB_EITHER |
| DB85 | V K | T | DB_EITHER; VAL_FATHER |
| DB86 | K I | T | DB_EITHER |
| DB87 | V L | T | DB_JOIN; DB_SENTENCED_E |
| DB88 | I P | T | DB_JOIN; DB_SENTENCED_N; after NP208 |
| DB89 | K P | T | DB_HOME; K_CRUSH; VEEZARA_ALIVE |
| DB90 | V R | T (interior, not Sanctuary) | DB_JOIN; SHROUDED_HOOD |
| DB91 | L P | T | CICERO; DB_JOIN; CICERO_JOURNAL |
| DB92 | G L | T | DB_HOME; after DB10 or DB36 if played |
| DB93 | I R | T | DB_HOME; VEEZARA_ALIVE; after DB16 |
| DB94 | S V | T | DB_HOME; ASTRID_ALIVE; SERANA |
| DB95 | R P | T | DB_MOURNING |
| DB96 | G V | T | DBSC:Lurbuk; after NP108 if played |
| DB97 | S P | T | DBSC:Hern; SERANA |
| DB98 | R A | T | DBSC:Maluril; ASHE_REVEAL |
| DB99 | C I | T | DBSC:Agnis |
| DB100 | X L | T | DBSC:Anoriath |
| DB101 | V R | T | DB_LISTENER; ASTRID_ALIVE |
| DB102 | C L | T | DB_LISTENER; CICERO_ALIVE |
| DB103 | K P | T | DB_FIRSTCONTRACT; K_TOG+ |
| DB104 | V G | T | SHADOWMERE_RIDE; V_ANY; G_ANY |
| DB105 | L P | T | SHADOWMERE_RIDE; after PA258 if played |
| DB106 | K I | T | SHADOWMERE_RIDE; K_ANY |
| DB107 | C G | T | SHADOWMERE_RIDE |
| DB108 | L V | E CAST:spectral | DB_JOIN; after DB105 |
| DB109 | X L | T | DB_CONTRACTS>=3 |
| DB110 | V P | T | DB_SITHIS |
| DB111 | G K | T | DB_SITHIS |
| DB112 | R I P | E LOC:DawnstarSanctuary | DB_SITHIS |
| DB113 | G R | T | DB_FIRE; BABETTE_ALIVE; after DB112 or after entering LOC:DawnstarSanctuary |
| DB114 | K P | T | DB_SITHIS; K_LOVE+ |
| DB115 | X A | T | DAWNSTAR_REBUILD; ASHE_REVEAL; after DB56 if played |
| DB116 | K P | T | DB_ASTRID; K_CRUSH; after DB57 |
| DB117 | L C | E LOC:BlackDoorFalkreath (any visit) | DB_PURGE |
| DB118 | G K | T | DB_PURGE |
| DB119 | V P | T | DB_PURGE |
| DB120 | X L | T | DB_PURGE; after DB59 |
| DB121 | L P | T | DB_PURGE; DB_PAID or DB_PURGE + 1 in-game day |
| DB122 | A R | T | DB_PURGE; ASHE_ROLEN1 |
| DB123 | C K | T | DB_PURGE; after DB7 if played |
| DB124 | G X | T | DB_PURGE |
| DB125 | S P | E LOC:SanctuaryOutside | DB_PURGE; SERANA |
| DB126 | L V | E AFTERFIGHT:dbassassin | DB_EITHER |
| DB127 | R K | E AFTERFIGHT:dbassassin | DB_EITHER |
| DB128 | C S | E AFTERFIGHT:dbassassin | DB_EITHER; SERANA |
| DB129 | A G | E AFTERFIGHT:dbassassin | DB_EITHER; ASHE_ROLEN1 |
| DB130 | X G | E AFTERFIGHT:dbassassin | DB_EITHER; after DB66 or DB109 if played |
| DB131 | I P | E AFTERFIGHT:dbassassin | DB_EITHER |
| DB132 | I R | E INN | DB_EITHER |
| DB133 | C V P | T | DB_EITHER |
| DB134 | G L | T | DB_EITHER |
| DB135 | R V | E HOUSE | DB_EITHER |
| DB136 | K R | E CITY:Falkreath | DB_EITHER; after DB75 if played |
| DB137 | K P | E CAMP + NIGHT | DB_EITHER; K_TOG+ |
| DB138 | A L | T | DB_EITHER; ASHE_REVEAL |
| DB139 | S I | E CAMP + NIGHT | DB_EITHER; SERANA; SER_VAMP |
| DB140 | X P | E CAMP | DB_EITHER; 10+ in-game days after DB_EITHER; after DB6 |

## 4. Notes for the build

- **Branch safety:** DB87-DB115 all carry a joined gate (DB_JOIN / DB_HOME / a joined quest / a side contract, which only exists on the joined path). DB116-DB125 carry DB_ASTRID or DB_PURGE. DB81-DB86 and DB126-DB140 are DB_EITHER (or an item gate both paths can reach) and their lines fit both roads. DB140 has Luna say "whatever you chose" and nothing else about the branch.
- **Shadowmere** (DB104-DB107): only reachable on the joined path in vanilla, so SHADOWMERE_RIDE doubles as a joined gate. If a mod gives Shadowmere on the destroy path, the lines still fit (none of them names the Sanctuary family).
- **Same-event priority:** AFTERFIGHT:dbassassin fires one talk per fight; part one's DB71-DB74 first, then DB126-DB131 in ID order on later fights.
- **Death checks:** DB89/DB93 need Veezara alive; DB94/DB101 need Astrid (and Arnbjorn) alive; DB102 needs Cicero alive; DB113 needs Babette alive.
- **Romance:** DB89 and DB116 are K_CRUSH (Luna oblivious: heart rate / frost spell). DB103, DB137 K_TOG+; DB114 K_LOVE+. DB106 K_ANY (Kaidan's slip, no Luna line). DB104 is a Val/Gore rival talk: Luna has no line.
- **Ashe:** DB98/DB115/DB138 need ASHE_REVEAL. DB122/DB129 need ASHE_ROLEN1 (she names Rolen). No talk mentions Medeus or Whisperfang (FL193/FL194 cover that).
- **Existing coverage avoided:** part one (Sithis/Void, Maven, shack candles/knots, Babette sweet roll, Festus notes, Veezara burial words, Gourmet, Gaius letter, Penitus "paperwork"), NP208 (Narfi - DB88 calls back), NP108 (Lurbuk singing - DB96 calls back), NP174 (Muiri kindness - DB95 is the contract angle), NP230 (Beitild - not used), PA258 (first Shadowmere ride), IN16 (Fultheim - hostages not named), OM34-OM37 (Penitus Oculatus jobs - not used), WE74/WE87/WE131.
- No line uses "Dragonborn", Kaidan's cult, or a beard. Redcap lines are one word per sentence.
