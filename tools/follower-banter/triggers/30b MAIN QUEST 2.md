# 30b MAIN QUEST 2 - trigger rows (prefix MQ, MQ121-MQ220, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\30b MAIN QUEST 2.txt`.
Part 1 (every gate code it defines is reused here unchanged): `triggers\30 MAIN QUEST DEEP.md`.
Sources: `research\triggers\vanilla_gates.md` Part A (A2-A4), `research\bibles\*.md` (kaidan KINV, lucien Paarthurnax, serana, ashe section 6), TRIGGERS.md sections 2-5, the DG gate codes in `triggers\20 DAWNGUARD.md` section 3.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`, which already holds every MQ silence window from vanilla_gates A4) and section 3 (`Free`), plus the Serana/Ashe Free rows in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (player line, Eleonora voice; no Free test, but the player must not be in dialogue).
Type: T = timer, E = event (fires on the moment). A T row whose gate opens inside a silence window waits for the first tick after the window ends.

## 1. Load-order notes (on top of part 1 section 1)

- **Paarthurnax Quest Expansion** branches, as used here: `PAARTH_DEAD` (MQPaarthurnax 50), `PAARTH_SPARED` (99/100, Blades talked round), `GB_ANGRY` (150, cause-neutral), and the vanilla refusal `BLADES_GONE` (below). Branch rows never take a side.
- **Lucien** leaves or turns hostile if Paarthurnax dies, and parts ways before the Skuldafn flight. Every Lucien row carries `LUC_OK`; Free() handles whether he is back.
- **Kaidan's Akaviri past**: only MQ175 names it, gated `K_AKAVIRI`. MQ169 and MQ173 (Kaidan in Blades talks) never hint at it.
- **Shout-use talks already exist** in `43b WHAT LUNA DOES 2` (first USE of each shout). The word rows here fire on LEARNING the first word, so the two sets never collide; if both would play in the same hour, the controller cooldown (300 s) plus "one talk per WORD event" keeps them apart.
- **Dragon attacks on towns**: generic town-attack talks live in `56 WORLD ENCOUNTERS` (WE59-62, WE134). The city rows here (MQ127-132) are per-city and need the city's own location, so a generic WE row and a city row can both exist; one per fight.

## 2. Gate codes added in this file

Existing (part 1 / TRIGGERS.md): `DB`, `DBX`, `KYNES`, `GREYBEARDS`, `WAY_DONE`, `PAARTH`, `DRAGONREND`, `ESBERN`, `SKYHAVEN`, `BLADES_RECRUIT`, `PQ_DEMAND`, `PAARTH_DEAD`, `PAARTH_SPARED`, `GB_ANGRY`, `LUC_OK`, `ALDUIN_HOME`, `RATWAY_HUNT`, `LOC:HH`, `LOC:SkyHaven`, `LOC:Ratway`, `LOC:Ustengrav`, `PATH:HH`, `K_AKAVIRI`, `K_TOG+`, `SERANA`, `SER_VAMP`, `ASHE_REVEAL`, `CITY:<Name>`, `TOWN`, `INN`, `NIGHT`, `SNOW`, `RAIN`, `CAMP`, `AFTERFIGHT:dragon`, `after:X`.

New, places and events:
- `LOC:Lair` = player location has `LocTypeDragonLair` (0130E0:Skyrim.esm) - the word-wall dragon lairs.
- `TOWN:<Name>` = player in that town's location (Riverwood, Dawnstar) **[UNC location FormIDs]**.
- `LocTypeFarm` = player location has LocTypeFarm (018EF0).
- `MOUND_RAISE` = event: the vanilla dragon-mound resurrection (Alduin circles a sealed mound and raises a dragon) ran near the player. Hook: the dragon-mound quest family started by Story Manager after MQ106 **[UNC: EditorIDs of the mound-resurrection quests; fallback = a dragon whose spawn point is a mound marker]**. `MOUND_RAISE then AFTERFIGHT:dragon` = the fight that follows.
- `WORD:<ShoutEditorID>` = event: the player first gains that shout (first word learned at a word wall). Hook: controller poll `PlayerRef.HasSpell(<Shout>)` flips 0 -> 1 **[UNC: Shout FormIDs - VoiceBecomeEthereal, VoiceFrostBreath, VoiceStormCall, VoiceMarkedForDeath, VoiceAuraWhisper, VoiceThrowVoice, VoiceKynesPeace, VoiceSlowTime, VoiceAnimalAllegiance, VoiceDisarm, VoiceDismay, VoiceElementalFury, VoiceIceForm]**. Fire after the word-wall absorb sequence ends (controls re-enabled).
- `WALL` = event: any word learned at a word wall (same hook, any shout or a 2nd/3rd word) **[UNC: 2nd/3rd words need a word-count check; Game.IsWordUnlocked is for unlocking, not learning]**.
- `CLEARSKIES` = the player gains VoiceClearSkies (taught by the Greybeards at the start of "The Throat of the World") **[UNC FormID]**.
- `VALOR` = the player knows VoiceCallOfValor (learned in Sovngarde) **[UNC FormID]**.
- `SHOUTS6` = the player knows 6 or more shouts (HasSpell over the shout list) **[UNC: list at build]**.
- `ODA` = `ALDUIN_HOME` AND the player knows VoiceCallDragon (Odahviing answers after MQ306).
- `ODA_SUMMON` = event: Odahviing lands within 4000 units after Call Dragon **[UNC: Odahviing summon ref from MQ306 / the Call Dragon script]**.
- `RATWAY_AGAIN` = `LOC:Ratway` AND `ESBERN` AND not `RATWAY_HUNT` (any later visit).
- `RO` = GetStageDone MQ105(0242BA) 76 (Ro unlocked). [CONFIRMED stage, vanilla_gates A3]

New, story:
- `BLADES_OK` = not `PQ_DEMAND` AND not `BLADES_GONE` (the Blades are on speaking terms with Luna).
- `BLADES_GONE` = `ALDUIN_HOME` AND MQPaarthurnax(03FA16) started AND not 50 AND not 99 AND not 100 (vanilla: Paarthurnax spared without PQE's talk-round, Delphine refuses to help) **[UNC: confirm the quest stays at its demand stage forever in this branch]**.
- `RECRUIT_SENT` = at least one recruit sent to Sky Haven (FreeformSkyHavenTempleA recruit alias filled) **[UNC FormID/alias, PQE overrides FreeformSkyHavenTemple A/C/D]**.
- `RECRUIT_DONE` = a recruit has finished training (in BladesFaction, back on the recruit list as a Blade) **[UNC]**.
- `DRAGON_HUNT_BLADES` = a "Dragon Hunting" run with Blades along completed (FreeformSkyHavenTempleC or D) **[UNC which letter]**.
- `ASHE_F` = Ashe hired (MM_AsheIntro 0A7946 completed) and following (`MM_AsheMentalModel ::IsFollowing_var == 1`).
- `ASHE_ROLEN1` = MM_AMQ_03 (BC5D8F:Ashe - Fire and Blood.esp) completed (either branch). `ASHE_SUMMIT` = MM_AMQ_07 (D6A70C) completed.
- Dragon-kill count (MQ209) = `Game.QueryStat("Dragon Souls Collected") >= 15` **[UNC stat name]**.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| MQ121 | V I | E AFTERFIGHT:dragon + LOC:Lair | DBX |
| MQ122 | X P | E AFTERFIGHT:dragon + LOC:Lair | DBX |
| MQ123 | R G | E LOC:Lair | DBX; no dragon alive nearby |
| MQ124 | K P | E MOUND_RAISE then AFTERFIGHT:dragon | KYNES; not ALDUIN; DBX |
| MQ125 | S I | E MOUND_RAISE then AFTERFIGHT:dragon | KYNES; not ALDUIN; SERANA |
| MQ126 | C L | E MOUND_RAISE then AFTERFIGHT:dragon | KYNES; not ALDUIN; LUC_OK |
| MQ127 | G V | E AFTERFIGHT:dragon + CITY:Whiterun | DBX |
| MQ128 | R K P | E AFTERFIGHT:dragon + TOWN:Riverwood | DBX |
| MQ129 | L X | E AFTERFIGHT:dragon + CITY:Solitude | DBX; LUC_OK |
| MQ130 | G S | E AFTERFIGHT:dragon + CITY:Windhelm | DBX; SERANA |
| MQ131 | R C | E AFTERFIGHT:dragon + CITY:Markarth | DBX |
| MQ132 | I K | E AFTERFIGHT:dragon + TOWN:Dawnstar | DBX |
| MQ133 | A V | E AFTERFIGHT:dragon + NIGHT | DBX; ASHE_REVEAL |
| MQ134 | X K | E AFTERFIGHT:dragon + SNOW | DBX [UNC: frost-dragon race check; the lines also work for any dragon in snow] |
| MQ135 | G I | E AFTERFIGHT:dragon + LocTypeFarm | DBX |
| MQ136 | C K | E AFTERFIGHT:dragon | DBX |
| MQ137 | L P | T | GetStageDone MQ105 76 (Ro unlocked); not in LOC:HH trials window; LUC_OK |
| MQ138 | G C | T | WAY_DONE |
| MQ139 | X P | E WORD:VoiceBecomeEthereal | LOC:Ustengrav or within 1 day after; DBX |
| MQ140 | K P | T | PAARTH; first tick after leaving ThroatoftheWorldLocation |
| MQ141 | V P | E CLEARSKIES learned | DBX; fire after the MQ204 silence window, outside ThroatoftheWorldLocation |
| MQ142 | X R | E WORD:VoiceFrostBreath | DBX |
| MQ143 | I G | E WORD:VoiceStormCall | DBX |
| MQ144 | K G | E WORD:VoiceMarkedForDeath | DBX |
| MQ145 | S P | E WORD:VoiceAuraWhisper | DBX; SERANA |
| MQ146 | V C | E WORD:VoiceThrowVoice | DBX |
| MQ147 | P K | E WORD:VoiceKynesPeace | DBX |
| MQ148 | I P | E WORD:VoiceSlowTime | DBX |
| MQ149 | C G | E WORD:VoiceAnimalAllegiance | DBX |
| MQ150 | V K | E WORD:VoiceDisarm | DBX |
| MQ151 | L R | E WORD:VoiceDismay | DBX; LUC_OK |
| MQ152 | A K | E WORD:VoiceElementalFury | DBX; ASHE_F |
| MQ153 | G P | E WORD:VoiceIceForm | DBX |
| MQ154 | R I | T | ALDUIN_HOME; VALOR; after:MQ94 |
| MQ155 | V P | T | DBX; SHOUTS6; GREYBEARDS |
| MQ156 | R A | E WALL (any word learned at a wall) | ASHE_REVEAL |
| MQ157 | X G | E LOC:HH | GREYBEARDS |
| MQ158 | G L | E LOC:HH | GREYBEARDS; LUC_OK |
| MQ159 | I C | E LOC:HH | GREYBEARDS |
| MQ160 | V P | E LOC:HH exterior courtyard | GREYBEARDS |
| MQ161 | S R | E LOC:HH | GREYBEARDS; SERANA; SER_VAMP |
| MQ162 | I K | E LOC:HH | GREYBEARDS |
| MQ163 | L P | T | GREYBEARDS; LUC_OK; after visiting LOC:HH a second time [UNC visit counter] |
| MQ164 | R P | E LOC:HH + NIGHT | GREYBEARDS |
| MQ165 | V G | E PATH:HH (descending) or T after LOC:HH | GREYBEARDS |
| MQ166 | A X | E LOC:HH | GREYBEARDS; ASHE_REVEAL |
| MQ167 | K P | E LOC:HH exterior + NIGHT | GREYBEARDS; K_TOG+ |
| MQ168 | G P | E leaving LOC:HH | GREYBEARDS |
| MQ169 | V K | T | BLADES_RECRUIT; RECRUIT_SENT; BLADES_OK |
| MQ170 | A G | E LOC:SkyHaven | BLADES_RECRUIT; RECRUIT_SENT; BLADES_OK; ASHE_F |
| MQ171 | L I | E LOC:SkyHaven + evening (hour 18..23) | BLADES_RECRUIT; RECRUIT_SENT; BLADES_OK; LUC_OK |
| MQ172 | R V | T | RECRUIT_DONE; BLADES_OK |
| MQ173 | C K | T | RECRUIT_DONE; BLADES_OK; DBX |
| MQ174 | X P | E LOC:SkyHaven | BLADES_RECRUIT; RECRUIT_SENT; BLADES_OK |
| MQ175 | K P | T | RECRUIT_DONE; BLADES_OK; K_AKAVIRI |
| MQ176 | S V | T | DRAGON_HUNT_BLADES; BLADES_OK; SERANA |
| MQ177 | G R | E LOC:SkyHaven | BLADES_RECRUIT; RECRUIT_SENT; BLADES_OK |
| MQ178 | A P | T | RECRUIT_DONE; BLADES_OK; ASHE_ROLEN1 |
| MQ179 | I R | E LOC:Ratway | RATWAY_AGAIN |
| MQ180 | G K | E LOC:Ratway | RATWAY_AGAIN; EMB_DONE not required |
| MQ181 | C X | E LOC:Ratway | RATWAY_AGAIN |
| MQ182 | V P | E leaving LOC:Ratway | RATWAY_AGAIN; SKYHAVEN |
| MQ183 | L S | E LOC:Ratway | RATWAY_AGAIN; SERANA; LUC_OK |
| MQ184 | K P | T | DRAGONREND; first tick after the MQ206 silence |
| MQ185 | L P | T | DRAGONREND; LUC_OK; after:MQ66 |
| MQ186 | S P | T | DRAGONREND; SERANA |
| MQ187 | X R | T | DRAGONREND |
| MQ188 | G I | T | DRAGONREND; exterior; at least 12 game hours after DRAGONREND |
| MQ189 | A K | E CAMP + NIGHT | DRAGONREND; ASHE_REVEAL |
| MQ190 | G X | E ODA_SUMMON | ODA |
| MQ191 | C L P | E ODA_SUMMON | ODA; LUC_OK |
| MQ192 | V P | T | ODA |
| MQ193 | I K | E AFTERFIGHT:dragon + ODA_SUMMON in the last 3 minutes | ODA |
| MQ194 | R A | E ODA_SUMMON | ODA; ASHE_REVEAL |
| MQ195 | K S | T | ODA; SERANA; DBX |
| MQ196 | G P | E ODA_SUMMON | ODA |
| MQ197 | X P | T | ODA |
| MQ198 | G K | E AFTERFIGHT:dragon | ALDUIN_HOME; first dragon fight after ALDUIN_HOME |
| MQ199 | R L | E near a sealed dragon mound [UNC: mound marker list] | ALDUIN_HOME; LUC_OK |
| MQ200 | V K | E LOC:HH | ALDUIN_HOME; not GB_ANGRY |
| MQ201 | G I | E INN | ALDUIN_HOME; DBX |
| MQ202 | L P | T | ALDUIN_HOME; not PAARTH_DEAD; LUC_OK; after a visit to ThroatoftheWorldLocation post-ALDUIN_HOME |
| MQ203 | X V | T | ALDUIN_HOME; not PAARTH_DEAD |
| MQ204 | G R | T | ALDUIN_HOME; PAARTH_SPARED |
| MQ205 | C V | E exterior with Throat of the World in view [UNC: worldspace region check] | ALDUIN_HOME; PAARTH_DEAD |
| MQ206 | K P | E LOC:HH | ALDUIN_HOME; GB_ANGRY |
| MQ207 | V G | T | ALDUIN_HOME; BLADES_GONE; DBX |
| MQ208 | K P | T | ALDUIN_HOME; K_TOG+; after:MQ106 (the "read for a month" talk) |
| MQ209 | V R | T | ALDUIN_HOME; dragons killed >= 15 [UNC: QueryStat "Dragon Souls Collected"] |
| MQ210 | A X | T | ALDUIN_HOME; BLADES_OK; ASHE_SUMMIT |
| MQ211 | K R | E AFTERFIGHT:dragon | ALDUIN_HOME; after:MQ198 |
| MQ212 | V L | T | ALDUIN_HOME; LUC_OK; after:MQ102 |
| MQ213 | P K | E INN | ALDUIN_HOME; DBX |
| MQ214 | G X | T | ALDUIN_HOME |
| MQ215 | C P | T | ALDUIN_HOME; after:MQ109 |
| MQ216 | G R | E AFTERFIGHT:dragon + LOC:Lair | DBX |
| MQ217 | V K | E AFTERFIGHT:dragon + RAIN | DBX |
| MQ218 | I X | E AFTERFIGHT:dragon + a Blades recruit within 2000 units | RECRUIT_DONE; BLADES_OK |
| MQ219 | C S | E MOUND_RAISE then AFTERFIGHT:dragon | KYNES; not ALDUIN; SERANA |
| MQ220 | K P | E AFTERFIGHT:dragon + ODA_SUMMON in the last 3 minutes | ODA; K_TOG+ |

## 4. Open items to verify at build
- Hooks: `MOUND_RAISE` (mound-resurrection quests), `WORD:` / `WALL` (shout-learned poll, 2nd/3rd words), `ODA_SUMMON`, Throat-in-view check for MQ205, sealed-mound proximity for MQ199, Blades-recruit presence for MQ218.
- FormIDs: every Voice* shout listed above, FreeformSkyHavenTempleA/C/D aliases, Riverwood and Dawnstar locations, frost-dragon race for MQ134 (optional; the lines work for any dragon in snow).
- `BLADES_GONE`: confirm the vanilla refusal branch keeps MQPaarthurnax at its demand stage.
- MQ163 "second visit" counter: a simple int the controller bumps on each LOC:HH arrival after GREYBEARDS.
