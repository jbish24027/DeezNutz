# 47b KAIDAN AND LUNA DEEP 2 - trigger rows (prefix KL, KL181-KL380, 200 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\47b KAIDAN AND LUNA DEEP 2.txt`.
Sources: `triggers\47 KAIDAN AND LUNA DEEP.md` (step gates and codes, reused unchanged), `research\triggers\kaidan_block.md` (§2a, §2b, §5 K04 map), `TRIGGERS.md` §2-§4, `triggers\20 DAWNGUARD.md` (Serana/Ashe Free rows and S_/A_ codes), `triggers\40 PLACES AND LANDMARKS.md` (hot-springs proxy).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).

## 1. Romance step gates (same as part 1)

K04 = `06D900:0Kaidan.esp`. Every KL row needs `GetStageDone K01 30 == 1` and Kaidan Free, even rows where he has no line (the talk is about him).

| Step | Rows | Gate |
|---|---|---|
| Crush | KL181-KL240 | `K04 5..24` (late-crush rows KL238, KL240: `15..24`) |
| Together | KL241-KL285 | `K04 50..64 AND != 57` (KL284: `50..59`, before his declaration at 60-62) |
| In love | KL286-KL320 | `K04 65..80`; rows where Luna is openly tender: `70..80`; pre-proposal rows KL301, KL312, KL320: `75..80` |
| Engaged | KL321-KL345 | `K04 81..99` |
| Married | KL346-KL380 | `K04 == 100` OR `KaidanRef GetInFaction PlayerMarriedFaction == 1` |

A romance pause (K04 reset to 0) fails every KL gate, which is what we want.

## 2. Gate codes used here

Existing (TRIGGERS.md §4 and part 1): `G_FLIRT`, `V_FLIRT`, `DB`, `SERANA`, `S_COMP`, `A_CRUSH`, `ASHE_REVEAL`, `INN`, `RAIN`, `SNOW`, `CAMP`, `NIGHT`, `MORNING`, `PREDAWN`, `CLEARNIGHT`, `CRYPT`, `DWEMER`, `FALMER`, `CAVE`, `WATER`, `HOUSE`, `WILD`, `CITY`, `CITY:<Name>`, `AFTERFIGHT`, `AFTERFIGHT:Thalmor`, `E after dragon soul absorbed`, `SEASON:<name> any`, `date mM dD` (holiday window day D or D+1), `after:X`.

New in this file:
- `AFTERFIGHT:hurt` = AFTERFIGHT where the player's health dipped below 25% during the fight (same hook as K19).
- `AFTERFIGHT:kaidanhurt` = AFTERFIGHT where Kaidan's health dipped below 25% or he entered bleedout. **[UNC]** poll Kaidan's health % on the controller's combat watch.
- `AFTERFIGHT:chaurus` = last combat target was ChaurusRace / ChaurusHunter (DLC1). **[UNC FormIDs]**
- `HOTSPRING` = the Eastmarch hot-springs proxy from PL52 (player swimming/in water, exterior, inside EastmarchHoldLocation 01676A, near a placed XMarker). **[UNC]**
- `MARKET` = `CITY` during daytime (hour 8..20) and within 1500 units of a market-stall merchant ref (Whiterun, Riften, Solitude, Windhelm, Markarth). **[UNC refs]** Fallback: CITY in daytime.
- `COAST` = exterior within 2000 units of a horker-colony marker on the northern coast (Solitude to Dawnstar to Winterhold shore). **[UNC]** Fallback: WATER in Haafingar, Pale or Winterhold hold.
- `hour a..b` = GameHour range.
- `G_EVER` = Gore's romance started at some point: `HD1Romance (6D6924:GORE.esp) == 1` (the global stays set after Kaidan wins). **[UNC]** if a breakup resets it.
- `V_EVER` = Val's flirt started at some point: `Val00A >= 10`. **[UNC]**
- `A_EVER` = Ashe was sweet on Luna at some point: `MM_RM (2F3039:Ashe - Fire and Blood.esp) >= 4`.
- `V_BOAT` = Val006 "Safe Harbor" stage 20 done (the Spring Rain bought; same check as A17).
- `date m5 d17` = the morning after Mid Year (KL315).

## 3. Per-talk table

### Part 1 - CRUSH (60 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL181 | V G | T | K04 5..24 |
| KL182 | A V | T | K04 5..24; after:KL181 |
| KL183 | P V K | T | K04 5..24; after:KL181 |
| KL184 | C G | T | K04 5..24; after:KL181 |
| KL185 | R X | T | K04 5..24; after:KL181 |
| KL186 | L I | T | K04 5..24; after:KL181 |
| KL187 | S V | T | K04 5..24; SERANA; after:KL181 |
| KL188 | K C | T | K04 5..24 |
| KL189 | R K | T | K04 5..24 |
| KL190 | I K | T | K04 5..24 |
| KL191 | P K | T | K04 5..24; after:KL190 |
| KL192 | K P G | E CAMP | K04 5..24 |
| KL193 | P K G | T | K04 5..24; date m1 d16 |
| KL194 | P L K | E CRYPT | K04 5..24 |
| KL195 | P K | E WILD | K04 5..24 |
| KL196 | P K | T | K04 5..24 |
| KL197 | K P | E SNOW | K04 5..24 |
| KL198 | K P | T | K04 5..24 |
| KL199 | P X K | E CAMP | K04 5..24 |
| KL200 | G K P | T | K04 5..24 |
| KL201 | K P | E MARKET | K04 5..24 |
| KL202 | P K | E INN | K04 5..24 |
| KL203 | K P | E INN + RAIN | K04 5..24 |
| KL204 | K P R | T | K04 5..24 |
| KL205 | P K C | E CAMP | K04 5..24 |
| KL206 | P K | T | K04 5..24 |
| KL207 | K P | E CAMP + NIGHT | K04 5..24 |
| KL208 | P K | E HOTSPRING | K04 5..24; player in the water |
| KL209 | P K | E CAMP + RAIN | K04 5..24 |
| KL210 | K P G | T | K04 5..24; SEASON:spring any |
| KL211 | K X | T | K04 5..24 |
| KL212 | K L | T | K04 5..24 |
| KL213 | V K | E AFTERFIGHT:hurt | K04 5..24 |
| KL214 | P K | T | K04 5..24; date m0 d1 |
| KL215 | P K | T | K04 5..24; date m11 d25 |
| KL216 | R V | T | K04 5..24; after:KL215 (next day) |
| KL217 | K P | T | K04 5..24; SEASON:autumn any |
| KL218 | K P | T | K04 5..24; date m5 d16 |
| KL219 | G K | E WATER | K04 5..24; G_FLIRT |
| KL220 | V P K | E INN | K04 5..24; V_FLIRT |
| KL221 | S K | T | K04 5..24; SERANA; S_COMP |
| KL222 | A K P | E MORNING + CAMP | K04 5..24; A_CRUSH |
| KL223 | P G K | T | K04 5..24; G_FLIRT |
| KL224 | K P | E AFTERFIGHT:hurt | K04 5..24 |
| KL225 | P K | E DWEMER | K04 5..24 |
| KL226 | P K | E FALMER | K04 5..24 |
| KL227 | K V | T | K04 5..24 |
| KL228 | K P | E INN | K04 5..24 |
| KL229 | G K | T | K04 5..24; SEASON:summer any |
| KL230 | I P | T | K04 5..24 |
| KL231 | L P | T | K04 5..24 |
| KL232 | R K | T | K04 5..24 |
| KL233 | C P | T | K04 5..24 |
| KL234 | G V | T | K04 5..24; after:KL182, KL190 |
| KL235 | P K | E CAMP + NIGHT | K04 5..24 |
| KL236 | P K | E MORNING + CAMP | K04 5..24 |
| KL237 | P K | E CAMP | K04 5..24 |
| KL238 | I K | T | K04 15..24 |
| KL239 | P G K | T | K04 5..24; date m7 d27 |
| KL240 | A S | T | K04 15..24; SERANA; after:KL182 |

### Part 2 - TOGETHER (45 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL241 | V P K | T | K04 50..64, !=57; after:KL183 |
| KL242 | C P | T | K04 50..64, !=57; after:KL184 |
| KL243 | R K | T | K04 50..64, !=57; after:KL204 |
| KL244 | P K | T | K04 50..64, !=57; after:KL203 |
| KL245 | P I K | T | K04 50..64, !=57; after:KL191 |
| KL246 | P K | E CRYPT | K04 50..64, !=57; after:KL194 |
| KL247 | P K | E WILD | K04 50..64, !=57; after:KL195 |
| KL248 | P K | T | K04 50..64, !=57; after:KL200 |
| KL249 | P K | T | K04 50..64, !=57; after:KL196 |
| KL250 | P K | E MORNING + CAMP | K04 50..64, !=57; after:KL236 |
| KL251 | P K | T | K04 50..64, !=57 |
| KL252 | K P | E CAMP + NIGHT | K04 50..64, !=57 |
| KL253 | P K | E AFTERFIGHT:Thalmor | K04 50..64, !=57 |
| KL254 | K P | E CITY:Windhelm | K04 50..64, !=57 |
| KL255 | V K | T | K04 50..64, !=57 |
| KL256 | L K | T | K04 50..64, !=57 |
| KL257 | K P | E AFTERFIGHT:hurt | K04 50..64, !=57 |
| KL258 | G K V | E HOTSPRING | K04 50..64, !=57 |
| KL259 | P K | E INN + RAIN | K04 50..64, !=57 |
| KL260 | K P | E COAST + (PREDAWN or MORNING) | K04 50..64, !=57 |
| KL261 | K P | E CAMP + NIGHT | K04 50..64, !=57 |
| KL262 | G K | T | K04 50..64, !=57; G_EVER; after:KL219 |
| KL263 | V S | T | K04 50..64, !=57; SERANA; V_EVER |
| KL264 | A K | T | K04 50..64, !=57; A_EVER |
| KL265 | V K | T | K04 50..64, !=57; V_BOAT |
| KL266 | I K | T | K04 50..64, !=57 |
| KL267 | I K | T | K04 50..64, !=57 |
| KL268 | C K | E CAMP + NIGHT | K04 50..64, !=57 |
| KL269 | R P | T | K04 50..64, !=57 |
| KL270 | S P | E MORNING + CAMP | K04 50..64, !=57; SERANA |
| KL271 | A P | T | K04 50..64, !=57; ASHE_REVEAL |
| KL272 | L P | T | K04 50..64, !=57 |
| KL273 | X K | E CITY | K04 50..64, !=57 |
| KL274 | R K | E SNOW | K04 50..64, !=57 |
| KL275 | K X | T | K04 50..64, !=57; SEASON:spring any |
| KL276 | P K | T | K04 50..64, !=57; date m1 d16; after:KL193 |
| KL277 | P K | T | K04 50..64, !=57; SEASON:autumn any; after:KL217 |
| KL278 | P K | E AFTERFIGHT:hurt | K04 50..64, !=57 |
| KL279 | G K | E MORNING | K04 50..64, !=57; hour 10..13 |
| KL280 | P K | T | K04 50..64, !=57 |
| KL281 | C P | T | K04 50..64, !=57; after:KL188 |
| KL282 | G K | E WILD | K04 50..64, !=57 |
| KL283 | L X | E CAMP | K04 50..64, !=57; hour 10..18 |
| KL284 | V A | T | K04 50..59; after:KL182 |
| KL285 | K P | T | K04 50..64, !=57; after:KL12 |

### Part 3 - IN LOVE (35 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL286 | V A | T | K04 65..80; after:KL284 |
| KL287 | P K | T | K04 70..80; after:KL207 |
| KL288 | K I | T | K04 65..80 |
| KL289 | X P K | E AFTERFIGHT:chaurus | K04 65..80 |
| KL290 | G V | E CAMP | K04 65..80 |
| KL291 | V K G | T | K04 65..80 |
| KL292 | P K | T | K04 70..80; SEASON:autumn any |
| KL293 | P K | E CAMP + SNOW | K04 65..80 |
| KL294 | K R | E CITY | K04 65..80; date m6 d10 |
| KL295 | P K | E CLEARNIGHT | K04 70..80 |
| KL296 | P V K | E INN | K04 70..80 |
| KL297 | P G K | E CAMP | K04 65..80 |
| KL298 | X P | T | K04 70..80 |
| KL299 | G P | T | K04 65..80 |
| KL300 | C K | T | K04 65..80 |
| KL301 | K X | T | K04 75..80 |
| KL302 | R K | T | K04 65..80 |
| KL303 | S P | T | K04 70..80; SERANA |
| KL304 | A P | T | K04 70..80; ASHE_REVEAL |
| KL305 | C K | T | K04 65..80; after:KL72 |
| KL306 | K P | E after dragon soul absorbed | K04 70..80; DB |
| KL307 | V K | E CITY | K04 65..80 |
| KL308 | K P | E INN + RAIN | K04 70..80 |
| KL309 | I K | E CLEARNIGHT | K04 65..80 |
| KL310 | L K | T | K04 65..80 |
| KL311 | G S | E INN | K04 65..80; SERANA |
| KL312 | R X | T | K04 75..80 |
| KL313 | K G | E AFTERFIGHT:hurt | K04 65..80 |
| KL314 | K P | T | K04 70..80; date m11 d25; after:KL37 |
| KL315 | L P K | E MORNING | K04 65..80; date m5 d17 |
| KL316 | I K | E CRYPT | K04 65..80 |
| KL317 | P K | E CAMP + NIGHT | K04 70..80 |
| KL318 | V G | E AFTERFIGHT:kaidanhurt | K04 65..80 |
| KL319 | P K | E MORNING | K04 70..80; after:KL80 |
| KL320 | K P | T | K04 75..80 |

### Part 4 - ENGAGED (25 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL321 | L K | T | K04 81..99; after:KL190 |
| KL322 | V A | T | K04 81..99 |
| KL323 | P K | T | K04 81..99 |
| KL324 | P K | T | K04 81..99 |
| KL325 | P K | E SNOW | K04 81..99 |
| KL326 | G V | T | K04 81..99 |
| KL327 | X K | T | K04 81..99 |
| KL328 | I K | E CAMP | K04 81..99 |
| KL329 | C P | T | K04 81..99 |
| KL330 | S P | T | K04 81..99; SERANA; after:KL146 |
| KL331 | A G | T | K04 81..99 |
| KL332 | K P | E AFTERFIGHT | K04 81..99; after:KL327 |
| KL333 | V K | E CITY:Solitude | K04 81..99 |
| KL334 | P K | E INN + RAIN | K04 81..99 |
| KL335 | L K P | E INN | K04 81..99; date m1 d16 |
| KL336 | R K | T | K04 81..99 |
| KL337 | X L | T | K04 81..99; after:KL7 |
| KL338 | C K | T | K04 81..99 |
| KL339 | V P K | T | K04 81..99; V_EVER |
| KL340 | P K | T | K04 81..99 |
| KL341 | S K | T | K04 81..99; SERANA |
| KL342 | R I | T | K04 81..99 |
| KL343 | K P | E CLEARNIGHT | K04 81..99 |
| KL344 | G K | T | K04 81..99 |
| KL345 | X K | T | K04 81..99 |

### Part 5 - MARRIED (35 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| KL346 | P K | T | K04 100 |
| KL347 | V P | T | K04 100 |
| KL348 | K P | T | K04 100; after:KL243 |
| KL349 | R G | E INN + MORNING | K04 100 |
| KL350 | P K | E AFTERFIGHT | K04 100; after:KL114 |
| KL351 | P K | E CAMP + NIGHT | K04 100; after:KL303 |
| KL352 | L K | E INN + RAIN | K04 100 |
| KL353 | G K | E HOTSPRING | K04 100 |
| KL354 | I A | E CAVE or CRYPT | K04 100 |
| KL355 | X K | E HOUSE | K04 100; after:KL130 |
| KL356 | P K | T | K04 100; after:KL103 |
| KL357 | A K | T | K04 100; ASHE_REVEAL |
| KL358 | K I | T | K04 100 |
| KL359 | R X | T | K04 100 |
| KL360 | L P | T | K04 100; after:KL193 |
| KL361 | C K | T | K04 100; after:KL268 |
| KL362 | G P | T | K04 100 |
| KL363 | P K | T | K04 100; date m11 d25; after:KL215 |
| KL364 | S P | T | K04 100; SERANA; after:KL159 |
| KL365 | K P | E WATER | K04 100; SEASON:summer any |
| KL366 | R K | E HOUSE | K04 100; SEASON:spring any |
| KL367 | K P | T | K04 100 |
| KL368 | V A | T | K04 100; after:KL347 |
| KL369 | G K | T | K04 100; G_EVER; after:KL219 |
| KL370 | P K | T | K04 100; date m7 d27; after:KL239 |
| KL371 | I P | T | K04 100; after:KL316 |
| KL372 | P K | E HOUSE + SNOW | K04 100 |
| KL373 | V K | E MORNING | K04 100; after:KL125 |
| KL374 | X S | E HOUSE + NIGHT | K04 100; SERANA |
| KL375 | K P | E INN + NIGHT | K04 100; after:KL145 |
| KL376 | C I | T | K04 100 |
| KL377 | V G | E CAMP + NIGHT | K04 100; after:KL181 |
| KL378 | L K | T | K04 100 |
| KL379 | K X | E CAMP or HOUSE or INN | K04 100 |
| KL380 | K P | E MARKET | K04 100 |

## 4. Notes for the build
- Kaidan's set pieces (kaidan_block.md §2b items 1-11) block every KL row, with or without Kaidan speaking. Also KaiSTFUQuest running and STFUVarNPCGeneral == 1.
- Nothing here retells his scripted beats. KL286 (after his declaration) has Luna refuse to give details. KL301, KL312 and KL320 only hint that he is saving for something (75..80, KaidanPreProposal running); no proposal is described. Engaged rows talk about planning only; no venue is named and no vows are quoted.
- Payoff rows (`after:` a crush row) never fire if the setup didn't play. Chains: KL181 opens the betting book and gates KL182-KL187, KL234, KL240; KL183 > KL241; KL184 > KL242; KL284 > KL286; KL347 > KL368; KL181 > KL377. Practice: KL190 > KL191 > KL245; KL188 > KL281; KL190 > KL321.
- Misread pairs (crush setup > together payoff): KL194 > KL246, KL195 > KL247, KL196 > KL249, KL200 > KL248, KL203 > KL244, KL204 > KL243 > KL348, KL236 > KL250, KL193 > KL276, KL215 > KL363, KL217 > KL277, KL239 > KL370, KL207 > KL287, KL268 > KL361, KL303 > KL351, KL316 > KL371.
- Part 1 payoffs: KL12 > KL285, KL37 > KL314, KL72 > KL305, KL80 > KL319, KL103 > KL356, KL114 > KL350, KL125 > KL373, KL130 > KL355, KL145 > KL375, KL146 > KL330, KL159 > KL364, KL7 > KL337.
- Rival rows (KL219-KL223, KL262-KL264, KL284, KL339, KL369): Luna has no line or a branch-neutral one and never chooses anyone. KL219/KL223 need G_FLIRT live; KL262/KL369 only need Gore's romance to have started once (G_EVER).
- KL240's Ashe bet and KL222 imply Ashe's interest; KL240 itself needs only SERANA (Ashe's line is about prediction, not a confession).
- Same-event priority: on AFTERFIGHT:hurt prefer this step's row (KL213/KL224 crush, KL257/KL278 together, KL313 in love); only one fires per fight. Combined with part 1's list (KL27/KL53, KL79/KL90, KL114/KL123, KL154/KL169).
- Hot springs: KL208 (crush) must not fire in the same visit as PL53 (also crush at the springs).
- Heart's Day: KL193 (crush), KL276 (together), KL335 (engaged) can only fire in their own step, so at most one per year.
- Existing coverage avoided: part 1 (KL1-KL180), the Desktop "SCRIPT KAIDAN AND LUNA" file (K1-K33) and the Kaidan romance rows in the other scripts (fence post, wolf/goat/hood misreads, steam at the springs, Heart's Day improvising, Saturalia snowberries, the gala and inn dances, horker picnic/stew/breakfast, thin walls, honey-I'm-home, bench for two, my-wife, uncle Scrap). `dup_scan.py` shows no repeated 6+ word line and no repeated title involving KL181-KL380.
