# 37b VANILLA SIDE QUESTS 2 - trigger rows (prefix SQ, continues at SQ151, 200 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\37b VANILLA SIDE QUESTS 2.txt`
Format and shared gate codes: `TRIGGERS.md` sections 4-5, plus the codes defined in `triggers\37 VANILLA SIDE QUESTS AND HOLDS.md`. Quest stages, journal text, objectives and quest aliases were read read-only from the live winners with houseCARL (`housecarl_records`, epoch e2-509d9856becc0652, 2026-10-18).

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe. `U` = Luna (player line, Eleonora voice; never a gate, no Free() test).
Type: T = timer, E = event (fires on the moment: arrival, quest stage or objective newly set, after a fight).

## Gate codes used in this file

From TRIGGERS.md section 4: `K_CRUSH`, `K_TOG+`, `DB` (first real dragon kill), `GREYBEARDS`, `PAARTH`, `BRYNJAR`, `GORE_BAIL`, `GORE_FATHER`, `VAL_FATHER`, `VAL_FATHIS`, `INN`, `CITY:<Name>`, `HOUSE`, `AFTERFIGHT`, `after:X`.

From part 1 (`37 VANILLA SIDE QUESTS AND HOLDS.md`): `Done(Q,s)`, `Comp(Q)`, `Run(Q)`, `LOC:<EditorID>`, `NEAR:<npc>`, `SER`, `SER_VAMP`, `ASHE`, `ASHE_HIRED`, `ASHE_REVEAL`. **[U]** = location or ref EditorID not looked up; confirm at build.

New in this file:
- `ObjD(Q,n)` = `Quest.IsObjectiveDisplayed(n)`; `ObjC(Q,n)` = `Quest.IsObjectiveCompleted(n)` (Papyrus, read by the controller). Most of these small quests log no journal stages, only objectives, so their gates read objectives.
- **Radiant favours are reused.** Favor013/017/018/019/109/110/151/153/154/157/158/204/205 and the FavorJobs chores run again for the next giver. Gate their talks on the stage newly set (an event), not on `Comp`, and let each talk play once. Quests with no stage at all (Favor017 brawls; FavorJobs chop, mine, wheat, drunks) need a script hook on the reward; marked [U].
- **MS08 branches:** stage 200 = Saadia saved and Kematu dead; 201 = Saadia handed to Kematu. Each ending talk is gated to its own branch; the mid-quest talks never say who was lying.
- **Thanes:** talks gate on `Comp(Favor25x)`. `At Your Own Pace - Thane Overhaul.esp` wins HousePurchase and the FavorJobs quests and changes how titles are earned, so the lines only react to "you are now Thane", never to how. Talks that name a Jarl (Elisif SQ270, Idgrod SQ278, Korir SQ285) need that Jarl still in the seat after the Civil War [U check]; the rest say "the Jarl".
- **Houses** (SQ171, SQ224, SQ244, SQ269, SQ297) gate on owning the house and being inside it. Housecarls are deliberately not mentioned (41 FAMOUS NPCS covers them).

Quest IDs used (EditorID FormID, all `:Skyrim.esm` unless named; live winner where it matters):
MS08 In My Time of Need 01CF25 (USSEP) · t02 The Book of Love 0211D5 · DLC1LD Lost to the Ages 005817:Dawnguard.esm · dunVolunruudQST Silenced Tongues 08ADFA · dunHillgrundsTombQST Ancestral Worship 03E897 · dunValthumeQST Evil in Waiting 03ED82 · dunBlindCliffQST The Affairs of Hagravens 039B3B · dunHighGateRuinsQST A Scroll for Anska 0443F4 · dunShipwreck04QST Trius' Trinket 043BAB · dunIronbindQST Coming of Age 06CD54 (aliases Salma, Beem-Ja) · dunYngolBarrowQST 0434A3 · dunMidden01QST Forgotten Names 055977 (alias Velehk Sain; winner AX ValSerano-USSEP.esp) · FreeformSkyhavenTempleA Rebuilding the Blades 0E38C9 (Paarthurnax QE winner) · FreeformSkyHavenTempleB Dragon Hunting 0E3E67 · FreeformSkyHavenTempleD Dragon Research 0E6DF1 · FreeformHighHrothgarA The Words of Power 0E76DE · FreeformHighHrothgarB Meditations 0E8283 · Favor013 0CA209 · Favor017 0CA210 · Favor018 03F46A · Favor019 03F4EC · Favor109 0940E0 · Favor110 0CA439 · Favor151 06C824 · Favor153 090E36 · Favor154 07172A · Favor157 0A3504 · Favor158 0940D0 · Favor204 07105B · Favor205 06FE37 · FavorJobsChopWood 0BF20F / MineOre 0A800A / GatherWheat 0A8007 (AYOP Thane Overhaul) · FavorJobsDrunks 0B026D · FavorJarlsMakeFriends 087E24 · FavorOrcsIntro 076335 · RelationshipOrcs 06819E · HousePurchase 0A7B33 (AYOP Thane Overhaul) · Favor250 Reach 0A2C86 · Favor252 Haafingar 0A2C9B · Favor254 Eastmarch 0A2CA6 · Favor255 Hjaalmarch 0A34CE · Favor256 Pale 0A34D4 · Favor257 Winterhold 0A34D7 · Favor258 Falkreath 0A34DE · FreeformRiftenThane 065BDF (Authoria - Master Patch - AYOP Thane.esp) · FreeformRiften02 053306 · 03 053307 · 05 053309 · 07 05331A · 08 05331B · 10 05331D · 11 041F91 (CRH patch) · 11b A Strong Nord Woman 000802:Caught Red Handed - Quest Expansion.esp · 12 041FD2 · 13 043E1A · 14 043E25 · 15 0557E9 · 16 0557F3 · 17 05B2DE · 18 05B3A5 · 19 065C30 · 21 09F179 · 22 0C1E07 · FreeformValdDebt 0C04BA · FreeformIvarstead03 0D9B65 · FreeformIvarstead04 0D9B66 · FreeformShorsStone02 0E49E8 (Sylgja / Verner) · FreeformMarkarthE 0753A1 · J 0790E1 · L 06099C · M 064798 · N 0647B3 · FreeformKarthwastenA 0622E8 · FreeformDushnikhYalA 09976E · MS06Start 093807 · SolitudeFreeform01 0E8BD7 (Angeline Morrard / Captain Aldis) · SolitudeFreeform03 0C7D42 (Svari / Greta / Roggvir; Miscellaneous Quests are Favors winner) · SolitudeFreeform06 0D69FB · BardsCollegePoeticEdda 0E7814 · FreeformCaravansA 0D9393 (Kharjo) · FreeformStonehillsA 064958 (Pactur / Bryling) · FreeformSalviusFarmA 0931BF (Rogatus / Leontius Salvius) · FreeformMorthalB 021896 (Gorm / Captain Aldis) · FreeformShipsDawnstar 094152 (Captain Leif Wayfinder) · FreeformShipsWindhelm 094158 (Kjar) · FreeformSoljundsSinkholeA 06136B (Perth) · FreeformSarethiFarm 0E3308 · FreeformKynesgroveA 069043 · FreeformMerryfairFarm 0E3E9B (Dravin Llanith) · FreeformHeartwoodMill 0E3EA5 (Grosta / Leifnarr) · MS11 01F7A3.

## Table

### Part 1 - Whiterun and the odd jobs of every hold
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ151 | V I | E CITY:Whiterun | Done(MS08,10); not Done(MS08,25) |
| SQ152 | K U | T | Done(MS08,25); not Done(MS08,175); MS08 not completed |
| SQ153 | C R | E LOC:DragonsreachDungeon [U] | Run(MS08); ObjD(MS08,25) shown; NEAR:Alik'r prisoner [U ref] |
| SQ154 | L K | E LOC:SwindlersDenLocation [U] | Run(MS08) |
| SQ155 | G X | T | Done(MS08,175) or Kematu talked to (ObjD 101/125) [U]; not Done(200); not Done(201) |
| SQ156 | K U | T | as SQ155 |
| SQ157 | R G | T | ObjD(MS08,175) shown (lead Saadia to the stables); not Done(200/201) |
| SQ158 | K V U | T | Done(MS08,200) |
| SQ159 | I S | T | Done(MS08,201); SER |
| SQ160 | A U | E INN (Bannered Mare) + NEAR:Saadia [U ref] | Done(MS08,200); ASHE; ASHE_HIRED |
| SQ161 | K L | E after a Favor017 brawl win [U: Favor017 has no stages; hook the brawl reward] | - |
| SQ162 | K U | E after firewood sold [U: FavorJobsChopWood 0BF20F sale event] | - |
| SQ163 | G R | E after ore sold [U: FavorJobsMineOre 0A800A sale event] | - |
| SQ164 | X C | E after crops sold [U: FavorJobsGatherWheat 0A8007 sale event] | - |
| SQ165 | V K U | E on Favor013 stage 20 newly set | - |
| SQ166 | R L | E on Favor018 completion [U: no logged stages] | - |
| SQ167 | V X | E on Favor019 stage 20 newly set | - |
| SQ168 | A G | E on Favor153 stage 20 newly set | ASHE |
| SQ169 | I C | E on Favor158 stage 20 newly set | - |
| SQ170 | X L U | E on Favor110 completion [U stage] | - |
| SQ171 | L U | E on HousePurchase objective 10 shown (Breezehome bought) [CHECK: AYOP Thane Overhaul wins HousePurchase] | - |
| SQ172 | K R | E CITY:Whiterun | Comp(MS08) |
| SQ173 | G V U | T | Run(FreeformSkyhavenTempleA); DB |
| SQ174 | I L | T | Run(FreeformSkyhavenTempleA); DB; after:SQ173 |
| SQ175 | C R | T | Run(FreeformSkyhavenTempleA); DB; after:SQ173 |
| SQ176 | C U | T | Run(FreeformHighHrothgarA); GREYBEARDS |
| SQ177 | L U | T | FreeformHighHrothgarB done [U: record has no stages/objectives; use Comp or a meditation-learned flag]; PAARTH; not Done(MQPaarthurnax,50) |
| SQ178 | X G | T | Run(FreeformSkyHavenTempleD); DB |
| SQ179 | K A | T | Run(FreeformSkyHavenTempleB); DB; ASHE |
| SQ180 | K G | T exterior | Run(FreeformHighHrothgarA); GREYBEARDS; after:SQ176 |

### Part 2 - The Rift
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ181 | V K U | T | Done(T02,10); K_CRUSH |
| SQ182 | R I | E LOC:RiftenTempleofMara [U] | - |
| SQ183 | R G | T | Run(T02); ObjD(T02,10) or ObjD(T02,20) shown; not ObjC(T02,25) |
| SQ184 | K I | T | ObjD(T02,25) shown; not ObjC(T02,25) |
| SQ185 | G U | E LOC:IvarsteadLocation [U] | ObjC(T02,25) or ObjD(T02,30) shown |
| SQ186 | R L | T | ObjD(T02,40) shown |
| SQ187 | G X | T | ObjD(T02,50) shown (Yngvar has written the poem) |
| SQ188 | V U | T | ObjC(T02,55) |
| SQ189 | K G U | T | ObjD(T02,75) shown; K_CRUSH |
| SQ190 | G L | T | ObjD(T02,80) shown; not ObjC(T02,95) |
| SQ191 | I S | T | ObjC(T02,95) or Comp(T02); SER |
| SQ192 | A V | T | Comp(T02); ASHE |
| SQ193 | X U | T | Comp(T02) |
| SQ194 | V K | T | Run(FreeformRiften11); ObjD 10/20/30 shown; not ObjD(40) |
| SQ195 | I U | T | ObjD(FreeformRiften11,40) shown |
| SQ196 | G R | T | ObjC(FreeformRiften11,50) or Comp(FreeformRiften11) |
| SQ197 | G A U | T | Done(FreeformRiften11b,100); ASHE |
| SQ198 | C K | T | Run(FreeformRiften05) |
| SQ199 | I X | T | ObjC(FreeformRiften12,10) or Comp(FreeformRiften12) |
| SQ200 | X V | T | Run(FreeformRiften08); not ObjC(10) |
| SQ201 | X U | T | ObjC(FreeformRiften08,20) or Comp [CHECK: clue content not read; lines stay vague] |
| SQ202 | C R | T | Run(FreeformRiften18); not ObjD(40) |
| SQ203 | X G | T | Run(FreeformRiften10) |
| SQ204 | L C | T | Run(FreeformRiften07) |
| SQ205 | V K | T | Run(FreeformRiften03); not ObjC(10) |
| SQ206 | R A | T | Run(FreeformRiften17); ASHE; ASHE_REVEAL |
| SQ207 | I G | T | Run(FreeformRiften16) |
| SQ208 | G K | T | ObjC(FreeformRiften19,10) |
| SQ209 | V L | T | Run(FreeformRiften22) |
| SQ210 | R X | T | Run(FreeformRiften14) |
| SQ211 | X K | T | Run(FreeformRiften13); not ObjC(10) |
| SQ212 | L R | T | Run(FreeformRiften21); not ObjD(30) |
| SQ213 | K L | E LOC:YngvildLocation [U] | Run(FreeformRiften21) |
| SQ214 | S G | T | Done(FreeformRiften21,200); SER |
| SQ215 | V I | T | ObjD(FreeformValdDebt,20) shown; not ObjC(20) |
| SQ216 | K R | T | ObjC(FreeformValdDebt,30) or Comp(FreeformValdDebt) |
| SQ217 | V U | T | Run(FreeformRiften02); not Done(200) |
| SQ218 | K I | T | Done(FreeformRiften02,200) |
| SQ219 | K C | T | Run(FreeformIvarstead03) |
| SQ220 | L K | T | Done(FreeformIvarstead04,200) |
| SQ221 | S R | T | Done(Favor109,20); SER |
| SQ222 | C G | T | Run(FreeformShorsStone02); not ObjD(20) |
| SQ223 | I U | T | Comp(FreeformRiftenThane) [U stage] or ObjC(30) |
| SQ224 | G U | E LOC:RiftenHoneyside [U] / HOUSE | player owns Honeyside |
| SQ225 | V S | E LOC:RiftenTempleofMara [U] + NEAR:Dinya Balu | Comp(T02); SER |
| SQ226 | K U | E CITY:Riften | 3+ Rift favours done (Comp/last ObjC among FreeformRiften05,07,10,12,13,14,16,18,19,22) [U count method] |
| SQ227 | R L | E CITY:Riften (canal level) | same count as SQ226 |
| SQ228 | I C | T | ObjD(FreeformRiften18,40) shown or Comp |
| SQ229 | K G | T | Done(FreeformRiften10,200) |
| SQ230 | I U | E LOC:RiftenFishery [U] + NEAR:Wujeeta | Comp(FreeformRiften12) + 3 game days passed [U] |

### Part 3 - The Reach
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ231 | K G | T | Run(FreeformMarkarthM); not ObjC(15) |
| SQ232 | I K | T | ObjC(FreeformMarkarthM,15) or Comp |
| SQ233 | X G | T | Run(FreeformMarkarthN) |
| SQ234 | G A | T | ObjC(FreeformMarkarthL,10) or Comp; ASHE |
| SQ235 | V X | T | Run(FreeformMarkarthJ) |
| SQ236 | R V | T | Run(FreeformMarkarthE); not Done(30) |
| SQ237 | L U | T | Done(FreeformMarkarthE,30) (Lisbet dead) |
| SQ238 | K X | T | Run(FreeformKarthwastenA); not ObjD(30); not ObjD(40) |
| SQ239 | G U | T | ObjC(FreeformKarthwastenA,30) or ObjC(40) or Comp |
| SQ240 | G K | T | Run(FreeformDushnikhYalA); not ObjC(10) |
| SQ241 | R G | T | ObjC(FreeformDushnikhYalA,10) or Comp |
| SQ242 | G V | T | Run(FavorOrcsIntro); not ObjC(20) |
| SQ243 | G C U | T | player is blood-kin [U: Orc-friend faction or Comp(FavorOrcsIntro)] |
| SQ244 | R U | E LOC:MarkarthVlindrelHall [U] / HOUSE | player owns Vlindrel Hall |
| SQ245 | K L | T | Comp(Favor250) [U stage] |
| SQ246 | R K | T | Done(DLC1LD,100) or Done(DLC1LD,111); not Done(130) |
| SQ247 | L U | E in Arkngthamz [U loc] | Done(DLC1LD,111) or Done(112); not Done(120) |
| SQ248 | L I | T | DLC1LD objective 135 completed (Katria's Journal) |
| SQ249 | V I | T | Done(DLC1LD,130); not Done(190) |
| SQ250 | R C | E | Done(DLC1LD,190) newly set |
| SQ251 | K G | E AFTERFIGHT | Done(DLC1LD,210) newly set |
| SQ252 | A R | T | Done(DLC1LD,225); ASHE; ASHE_REVEAL |
| SQ253 | S U | T | Comp(DLC1LD); SER |
| SQ254 | K S | T | Done(dunBlindCliffQST,100); SER |
| SQ255 | V C | T | Done(Favor157,20) |
| SQ256 | R G | T | Run(FreeformSoljundsSinkholeA); not ObjD(20) |
| SQ257 | K I | T | ObjC(FreeformSoljundsSinkholeA,20) or Comp |
| SQ258 | X U | T exterior in the Reach [U: Reach hold location] | 3+ of: Comp(FreeformMarkarthM/N/L/J/E), FreeformKarthwastenA, FreeformDushnikhYalA, FreeformSoljundsSinkholeA |
| SQ259 | V U | E LOC:MarkarthSilverBloodInn [U] | Comp(FreeformMarkarthE) or Comp(FreeformMarkarthL) |
| SQ260 | L U | E LOC:MarkarthHallofTheDead [U] | same count as SQ258 |

### Part 4 - Haafingar, Hjaalmarch, the Pale and Winterhold
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ261 | G X | T | Done(MS06Start,50); not Done(100) |
| SQ262 | L U | T | Done(MS06Start,15) or Done(50); not Done(100) |
| SQ263 | S V | T | Run(SolitudeFreeform06); SER |
| SQ264 | R X | T | ObjC(SolitudeFreeform06,20) or Comp |
| SQ265 | L K | T | Run(SolitudeFreeform01); not ObjD(20) |
| SQ266 | L U | T | Done(SolitudeFreeform01,200) |
| SQ267 | I R | T | Run(SolitudeFreeform03); not Done(200) [CHECK: Greta/Roggvir link inferred from the objectives] |
| SQ268 | I U | T | Done(SolitudeFreeform03,200) |
| SQ269 | V K U | E LOC:SolitudeProudspireManor [U] / HOUSE | player owns Proudspire Manor |
| SQ270 | S L | T | Comp(Favor252) [U stage]; SER; Elisif is Jarl of Haafingar [U check] |
| SQ271 | L X | T | Run(BardsCollegePoeticEdda) |
| SQ272 | R C U | E INN + a bard performing [U: bard scene check] | Run(BardsCollegePoeticEdda) |
| SQ273 | I U | T | Run(FreeformCaravansA); not ObjD(15) |
| SQ274 | I C | T | Done(FreeformCaravansA,20) |
| SQ275 | V G | T | Run(FreeformStonehillsA) |
| SQ276 | V U | T | Run(FreeformSalviusFarmA); VAL_FATHIS |
| SQ277 | K V | T | Run(FreeformMorthalB) |
| SQ278 | S U | T | Comp(Favor255) [U stage]; SER; Idgrod is Jarl of Hjaalmarch [U check] |
| SQ279 | V C | T | Run(FreeformShipsDawnstar); not ObjD(15) |
| SQ280 | G U | T | Done(FreeformShipsDawnstar,20) |
| SQ281 | G K | T | Comp(Favor256) [U stage]; GORE_BAIL |
| SQ282 | L U | T | Done(dunHighGateRuinsQST,10) or Done(20); not Done(90) |
| SQ283 | K A | E LOC:HighGateRuinsLocation [U] | Done(dunHighGateRuinsQST,20); not Done(90); ASHE |
| SQ284 | X U | T | Done(dunHighGateRuinsQST,100) |
| SQ285 | X U | T | Comp(Favor257) [U stage]; Korir is Jarl of Winterhold [U check] |
| SQ286 | V L | T | Done(dunShipwreck04QST,10); not Done(100) |
| SQ287 | R U | T | Done(dunShipwreck04QST,100) |
| SQ288 | V U | E LOC:MiddenDark [U] + NEAR:Velehk Sain (MiddenVelehkREF 0B8D3D) | Run(dunMidden01QST) [U: no stages in record] |
| SQ289 | V R | E leaving the College [U] | after:SQ288 |
| SQ290 | X G | E LOC:IronbindBarrow exterior [U] | Run(dunIronbindQST); NEAR:Salma or Beem-Ja |

### Part 5 - Eastmarch, Falkreath and the old tombs
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ291 | K X | T | Run(FreeformSarethiFarm); not ObjD(20) |
| SQ292 | R K | T | Done(FreeformSarethiFarm,200) |
| SQ293 | A X | T | Run(FreeformKynesgroveA); ASHE |
| SQ294 | L U | T | ObjC(FreeformKynesgroveA,10) or Comp |
| SQ295 | V I | T | Run(FreeformShipsWindhelm); not ObjD(15) |
| SQ296 | G V | T | Done(FreeformShipsWindhelm,20); VAL_FATHER; GORE_FATHER |
| SQ297 | R I | E LOC:WindhelmHjerim [U] / HOUSE | player owns Hjerim; Comp(MS11) |
| SQ298 | K U | T | Comp(Favor254) [U stage] |
| SQ299 | I A | T | Run(FreeformMerryfairFarm); not ObjD(20); ASHE |
| SQ300 | C U | T | Done(FreeformMerryfairFarm,200) |
| SQ301 | L K | T | Run(FreeformHeartwoodMill); ObjD(10) shown; not ObjC(10); BRYNJAR |
| SQ302 | K U | T | Done(FreeformHeartwoodMill,200); K_TOG+ |
| SQ303 | R K | T | Comp(Favor258) [U stage] |
| SQ304 | K L | T | Done(dunVolunruudQST,10); not Done(20) |
| SQ305 | R V | E LOC:VolunruudLocation [U] | Done(dunVolunruudQST,20); not Done(100) |
| SQ306 | G U | T | Done(dunVolunruudQST,100) |
| SQ307 | V I | T | Done(dunHillgrundsTombQST,10); not Done(100) |
| SQ308 | X R | E AFTERFIGHT in Hillgrund's Tomb [U loc] | Run(dunHillgrundsTombQST); ObjC(10) (Vals Veran defeated) |
| SQ309 | L R | E in Hillgrund's Tomb [U loc] | ObjD(dunHillgrundsTombQST,35) shown; not ObjC(35) |
| SQ310 | K G | T | Done(dunHillgrundsTombQST,100) |
| SQ311 | L S | T | Done(dunValthumeQST,3); not Done(15); SER |
| SQ312 | C G | E in Valthume [U loc] | Done(dunValthumeQST,15); not Done(50) |
| SQ313 | V U | T | Done(dunValthumeQST,60) |
| SQ314 | K A | E in Valthume [U loc] | ObjD(dunValthumeQST,15) shown (Hevnoraak awake); not Done(50); ASHE |
| SQ315 | K U | T | Done(dunIronbindQST,200); K_TOG+ |
| SQ316 | L R | E in Yngol Barrow [U loc] | ObjD(dunYngolBarrowQST,50) shown; not ObjC(50) |
| SQ317 | L G | T | any FavorJarlsMakeFriends hold objective completed [U: Friends count globals reach the hold total] |
| SQ318 | A V | T | 3+ FavorJarlsMakeFriends hold objectives completed; ASHE |
| SQ319 | I X | T | Done(Favor154,20) |
| SQ320 | K A | T | Done(Favor151,20); ASHE |

### Part 6 - Second looks: odd jobs, aftermaths, loose ends
| ID | Speakers | Type | Gates |
|---|---|---|---|
| SQ321 | K V | T | Done(Favor109,20); after:SQ221, or Serana not following |
| SQ322 | G U | T | Done(Favor204,20) or Done(Favor205,20) |
| SQ323 | G I | E after a Favor017 brawl win [U] | after:SQ161 |
| SQ324 | V U | E after firewood sold [U] | after:SQ162 |
| SQ325 | S L | E after crops sold [U] + exterior + IsPleasant | SER; SER_VAMP |
| SQ326 | V I | E after Favor018 completion [U] | after:SQ166 |
| SQ327 | A U | E on Favor013 stage 20 newly set | after:SQ165; ASHE; ASHE_HIRED |
| SQ328 | L K | E on Favor019 stage 20 newly set | after:SQ167 |
| SQ329 | C U | E after ore sold [U] | after:SQ163 |
| SQ330 | G S | E after FavorJobsDrunks drink given [U] | SER |
| SQ331 | L U | T | Comp(FreeformSkyHavenTempleD) [U stage] or ObjC(10) |
| SQ332 | G R | E | DLC1LD objective 180 shown (Stand Clear) |
| SQ333 | R X | E LOC:ArkngthamzLocation [U], first entry | - |
| SQ334 | L X | T | Done(dunBlindCliffQST,100) |
| SQ335 | X V | T | ObjC(FreeformRiften11,10) (Bolli's mark) |
| SQ336 | I K | E LOC:RiftenHaelgasBunkhouse [U] + player rented a bed | Run or Comp(FreeformRiften11) |
| SQ337 | G L | E LOC:IvarsteadVilemyrInn [U] + NEAR:Lynly Star-Sung performing [U] | - |
| SQ338 | R U | T | ObjC(FreeformRiften13,20) or Comp |
| SQ339 | L U | T | ObjC(FreeformRiften14,40) or Comp |
| SQ340 | K G | T | Done(FreeformRiften03,200) |
| SQ341 | R I | T | Run(FreeformRiften15) |
| SQ342 | G U | T | ObjC(FreeformMarkarthN,10) or Comp |
| SQ343 | L G | T | Comp(BardsCollegePoeticEdda) [U stage] |
| SQ344 | I G | T | Done(FreeformIvarstead03,200) |
| SQ345 | I U | T | ObjC(FreeformRiften22,20) or Comp |
| SQ346 | R U | E LOC:MarkarthUnderstoneKeep [U] + NEAR:Calcelmo | Comp(T02) |
| SQ347 | K U | T | Comp(DLC1LD); an Aetherium item equipped [U: Aetherial Crown/Shield/Staff check]; K_CRUSH |
| SQ348 | G V | T | Done(MS08,201) |
| SQ349 | C L | T | ObjD(T02,90) shown; not ObjC(90) |
| SQ350 | K G U | T | 5+ FavorJarlsMakeFriends hold objectives completed |

## Open items to check at build
- Location EditorIDs marked [U] (about 30) and NEAR refs (Alik'r prisoner, Saadia, Dinya Balu, Wujeeta, Salma or Beem-Ja, Lynly Star-Sung, Calcelmo).
- Stage-less quests that need a hook or a flag: Favor017 brawls; FavorJobs chop, mine, wheat and drunks; FreeformHighHrothgarB; dunMidden01QST; RelationshipOrcs (blood-kin); BardsCollegePoeticEdda completion.
- The Riften and Markarth freeforms log no stages; `Comp()` may not be set by every one. Use the last objective's `ObjC` as the fallback given in each row.
- Jarl-named Thane talks (SQ270 Elisif, SQ278 Idgrod, SQ285 Korir) need a "who is Jarl now" check after the Civil War.
- [CHECK] lines kept general on purpose: SQ201 (what Brand-Shei's clue says), SQ267/SQ268 (why Greta stays away from the Temple; the objectives only show Svari, Greta and an item taken off Roggvir), SQ288/SQ289 (Velehk Sain's offer), SQ235 (Bothela's potion is implied, never named).
- Every Serana row implies SER; every Ashe row implies ASHE. K_CRUSH rows: SQ181, SQ189, SQ347. K_TOG+ rows: SQ302, SQ315. Story-gated rows: SQ162 none (Brynjar line removed), SQ296 VAL_FATHER + GORE_FATHER, SQ276 VAL_FATHIS, SQ281 GORE_BAIL, SQ301 BRYNJAR.
