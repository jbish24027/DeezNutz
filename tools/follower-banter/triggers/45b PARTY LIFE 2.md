# 45b PARTY LIFE 2 - trigger rows (prefix PY, PY181-PY430, 250 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\45b PARTY LIFE 2.txt`.
Continues `triggers\45 PARTY LIFE.md` (PY1-PY180). Same sources: `STYLE-GUIDE.md`, `TRIGGERS.md` (sections 2-4), `triggers\20 DAWNGUARD.md` (sections 1 and 3: Serana/Ashe Free rows and the S_/A_/SER_/DG_ gate codes), `research\bibles\*.md`.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).

## 1. File-wide rules
- All the file-wide rules of `45 PARTY LIFE.md` section 1 apply here too: meets first; Serana rows need her Free row; every Ashe row carries `ASHE_REVEAL` (already written into each row below); party-life talks are low priority against quest/place talks on the same event; at most one PY story talk per in-game night at camp.
- **Second stories** (Part 1): each cycle's first talk waits for that teller's last Part 1 story in 45 PARTY LIFE (the `after:` in its row); each later talk waits `+12h` after the one before it. At most one story talk per night, across both files.
- **Make-ups** (Part 6) use `after:X+12h` (half a day). The fight talk itself has no cooldown beyond the file's normal pacing.
- **Holidays** (Part 8) use the date window from TRIGGERS.md "Seasons, holidays, lost": day D or D+1, vanilla `GameMonth` (0 = Morning Star) and `GameDay`, and the player must be at CAMP. One holiday talk per holiday across all files: if a 51/51b or SEASONS holiday talk for the same day is eligible in town, the town one plays in town and this one plays only if the night is spent at camp.
- **Serana states:** blood/feeding/garlic rows carry `SER_VAMP`; cold, sniffles and sunrise rows carry `SER_CURED`.
- **Kaidan crush:** PY264 is `K_CRUSH` (Luna oblivious). PY274, PY350 and PY399 are `K_TOG+`.

## 2. Event and gate codes used here
Events from TRIGGERS.md section 4 and 45 PARTY LIFE.md section 2: `CAMP`, `NIGHT`, `CAMP+NIGHT`, `CAMP+RAIN`, `INN`, `CITY`, `RAIN`, `SNOW`, `MORNING`, `PREDAWN`, `WATER`, `WILD`, `CAVE`, `AFTERFIGHT[:type]`, `E MORNING, after a night at camp`.

New events (this file):
- `E FARM` = player in or within 40 m of a location with `LocTypeFarm` (exterior), not in combat. [UNC: some farms carry only LocTypeHabitation; fall back to the named farm locations near Dragon Bridge, Rorikstead, Whiterun]
- `E LOC:Rorikstead` = player in RoriksteadLocation (exterior), not first arrival required. [UNC FormID]
- `E DUNGEON_DOOR` = exterior, within 30 m of a load door into a LocTypeDungeon / LocTypeDraugrCrypt / LocTypeDwarvenAutomatons location, player not yet inside. [UNC: needs a door scan or OnLocationChange look-ahead; fallback: fire on first entry into that dungeon's first cell]
- `E CITY, after a barter menu closes` = in a CITY location, within 10 s of the player closing the BarterMenu. [UNC: SKSE menu event]
- `E CAMP+WATER` = CAMP and WATER both true.
- `AFTERFIGHT:riekling` = last combat target race DLC2RieklingRace (Dragonborn.esm) [UNC FormID]. `AFTERFIGHT:spider` = FrostbiteSpiderRace or any giant-spider race. `AFTERFIGHT:draugr` as TRIGGERS.md.
- `E CAMP+NIGHT (SNOW or cold weather)` as 45 PARTY LIFE.md section 2.

New gates (this file):
- `COUNT(PYa..PYb)>=n` = at least n of the talks PYa..PYb have played.
- `after:MN1` = MN1 "The Sweet Roll Scale" (15 MISSIVES) has played, so the scale exists.
- `DUNGEON_TODAY` = the player was inside a LocTypeDungeon / DraugrCrypt / DwarvenAutomatons location within the last 24 game hours. [UNC: controller stamps GameDaysPassed on leaving one]
- `FALMER_TODAY` = an `AFTERFIGHT:falmer` (FalmerRace target) ended within the last 24 game hours.
- `LOW_HP_TODAY` = player health fell below 25% during a fight within the last 24 game hours (same health watch as K19 in TRIGGERS.md).
- `HARDFIGHT_TODAY` = within the last 6 game hours, a fight in which the player or at least two followers fell below 50% health. [UNC: needs the controller's health watch on followers too]
- `NO_FIGHT_TODAY` = no player combat since the player last slept, and the player has been awake at least 10 game hours.
- `HARVEST` = the player picked a flora ingredient (OnItemAdded, IngredientKeyword / flora source) within the last 60 s, exterior. [UNC]
- `RAIN_ENDED` = the last weather poll was RAIN and this poll is not, and the player spent the night at camp.
- `PARTY_YEAR2` = GameDaysPassed >= (the K01 stage 30 stamp from 45 PARTY LIFE.md `PARTY_YEAR`) + 730.
- `SER_CURED`, `SER_VAMP`, `DG_CAIRN`, `ASHE_REVEAL`, `ASHE_Q1` as 20 DAWNGUARD.md section 3. `K_CRUSH`, `K_TOG+`, `BRYNJAR`, `VAL_FATHIS`, `RC_MANOS`, `RC_REDGOD`, `INIGO_BV` as TRIGGERS.md section 4.

## 3. Per-talk table

### Part 1 - Campfire stories, round two
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY181 | K L P | E CAMP+NIGHT | after:PY3 |
| PY182 | G K R | E CAMP+NIGHT | after:PY181+12h |
| PY183 | I K P | E CAMP+NIGHT | after:PY182+12h |
| PY184 | G V C | E CAMP+NIGHT | after:PY6 |
| PY185 | X G L | E CAMP+NIGHT | after:PY184+12h |
| PY186 | K G R | E CAMP+NIGHT | after:PY185+12h |
| PY187 | V I L | E CAMP+NIGHT | after:PY9 |
| PY188 | C V G | E CAMP+NIGHT | after:PY187+12h |
| PY189 | I V P | E CAMP+NIGHT | after:PY188+12h |
| PY190 | R S G | E CAMP+NIGHT | after:PY12 |
| PY191 | L R K | E CAMP+NIGHT | after:PY190+12h |
| PY192 | X R K | E CAMP+NIGHT | after:PY191+12h |
| PY193 | X I C | E CAMP+NIGHT | after:PY15 |
| PY194 | R X I | E CAMP+NIGHT | after:PY193+12h |
| PY195 | K X G | E CAMP+NIGHT | after:PY194+12h |
| PY196 | I C K | E CAMP+NIGHT | after:PY18 |
| PY197 | L I C | E CAMP+NIGHT | after:PY196+12h |
| PY198 | I G V | E CAMP+NIGHT | after:PY197+12h |
| PY199 | L R V | E CAMP+NIGHT | after:PY21 |
| PY200 | K L A | E CAMP+NIGHT | ASHE_REVEAL; after:PY199+12h |
| PY201 | L I P | E CAMP+NIGHT | after:PY200+12h |
| PY202 | C G L | E CAMP+NIGHT | after:PY24 |
| PY203 | I C R | E CAMP+NIGHT | after:PY202+12h |
| PY204 | X C V | E CAMP+NIGHT | after:PY203+12h |
| PY205 | S L P | E CAMP+NIGHT | after:PY26 |
| PY206 | K S R | E CAMP+NIGHT | after:PY205+12h |
| PY207 | A S P | E CAMP+NIGHT | ASHE_REVEAL; after:PY206+12h |
| PY208 | A G R | E CAMP+NIGHT | ASHE_REVEAL; after:PY28 |
| PY209 | L A K | E CAMP+NIGHT | ASHE_REVEAL; after:PY208+12h |
| PY210 | I A P | E CAMP+NIGHT | ASHE_REVEAL; after:PY209+12h |
| PY211 | P K R | E CAMP+NIGHT | after:PY31 |
| PY212 | V P G | E CAMP+NIGHT | after:PY211+12h |
| PY213 | L P I | E CAMP+NIGHT | after:PY212+12h |
| PY214 | R V C | E CAMP | after:PY183; after:PY186; after:PY189; after:PY198; after:PY213 |

### Part 2 - Games
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY215 | R C K | E CAMP | — |
| PY216 | A G P | E CAMP | ASHE_REVEAL; after:PY215 |
| PY217 | K I L | E CAMP | after:PY215 |
| PY218 | S R P | E CAMP | after:PY215 |
| PY219 | X L C | E CAMP | — |
| PY220 | X G I | E CAMP | after:PY219 |
| PY221 | X V A | E CAMP | ASHE_REVEAL; after:PY219 |
| PY222 | X K I | E CAMP | after:PY219 |
| PY223 | X R P | E CAMP | after:PY219 |
| PY224 | L X G | E CAMP | after:PY219; after:PY52 |
| PY225 | X C P | E CAMP | COUNT(PY220..PY224)>=3 |
| PY226 | L S C | E CAMP | — |
| PY227 | G R K | E CAMP | after:PY226 |
| PY228 | X L R | E CAMP | after:PY226 |
| PY229 | A V I | E CAMP | ASHE_REVEAL; after:PY226 |
| PY230 | V R G | E CAMP | after:PY226 |
| PY231 | C S P | E CAMP | after:PY226; COUNT(PY227..PY230)>=3 |
| PY232 | X K P | E CAMP | after:PY66; after:MN1 |
| PY233 | K X C | E CAMP | after:PY232 |
| PY234 | R X I | E CAMP | after:PY232 |
| PY235 | S X P | E CAMP | after:PY232 |
| PY236 | G X V | E CAMP | after:PY232 |
| PY237 | X G R | E CAMP | after:PY232; COUNT(PY233..PY236)>=3 |
| PY238 | G I P | E WATER (exterior, WILD) | — |
| PY239 | L I K | E WATER | after:PY238 |
| PY240 | V G C | E WATER | after:PY238; after:PY9 |
| PY241 | X G R | E WATER | after:PY238 |
| PY242 | G C V | E CAMP | COUNT(PY239..PY241)>=2 |
| PY243 | R P C | E CAMP | after:PY38; after:PY39 |
| PY244 | C P K | E CAMP | after:PY243 |
| PY245 | G L P | E CAMP | after:PY243 |
| PY246 | A R P | E CAMP | ASHE_REVEAL; after:PY243 |
| PY247 | R C P | E CAMP | COUNT(PY243..PY246)>=3 |
| PY248 | A K I | E WILD | ASHE_REVEAL |
| PY249 | R C G | E CAMP | after:PY248 |
| PY250 | G A P | E CAMP | ASHE_REVEAL; after:PY48; after:PY144 |
| PY251 | L C I | E CAMP | after:PY47 |
| PY252 | V X P | E INN | — |
| PY253 | S K G | E INN | — |

### Part 3 - Songs
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY254 | I R P | E CAMP | after:PY62 |
| PY255 | K G V | E WATER (wading, WILD) | after:PY63 |
| PY256 | I L C | E AFTERFIGHT:spider | — |
| PY257 | C X G | E CAMP+NIGHT | — |
| PY258 | X R | E CAMP+NIGHT | after:PY195 |
| PY259 | S K P | E CAMP+NIGHT | — |
| PY260 | L V G | E CAMP | after:PY61 |
| PY261 | G C K | E CAMP+NIGHT | after:PY65 |
| PY262 | L I R | E CAMP | after:PY118 |
| PY263 | A V | E WILD | ASHE_REVEAL |
| PY264 | K L P | E CAMP | K_CRUSH; after:PY57 |
| PY265 | G R V | E INN | after:PY108 |

### Part 4 - Watches, nightmares and comfort
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY266 | X I | E CAMP+NIGHT | — |
| PY267 | K G P | E CAMP+NIGHT | — |
| PY268 | L R | E CAMP+NIGHT | DUNGEON_TODAY |
| PY269 | A S | E CAMP+NIGHT | ASHE_REVEAL |
| PY270 | K I | E CAMP+NIGHT | — |
| PY271 | V L | E CAMP+NIGHT | — |
| PY272 | G I | E CAMP+NIGHT | — |
| PY273 | C X | E CAMP+NIGHT | — |
| PY274 | K P | E CAMP+NIGHT | K_TOG+ |
| PY275 | L X | E CAMP+NIGHT | — |
| PY276 | R P | E CAMP+NIGHT (WILD) | — |
| PY277 | V G C | E CAMP+NIGHT | — |
| PY278 | K L | E CAMP+NIGHT | FALMER_TODAY |
| PY279 | I G P | E CAMP+NIGHT | — |
| PY280 | A I | E MORNING, after a night at camp | ASHE_REVEAL |
| PY281 | S G C | E CAMP+NIGHT (SNOW or cold weather) | SER_CURED |
| PY282 | X R P | E CAMP+NIGHT (SNOW or cold weather) or E SNOW | — |
| PY283 | G C | E CAMP+NIGHT | — |
| PY284 | V K P | E CAMP+NIGHT | — |
| PY285 | I X P | E MORNING, after a night at camp | after:PY267+24h |

### Part 5 - Running jokes
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY286 | I C L | E FARM | after:PY118+24h |
| PY287 | I G C | E WILD | after:PY286 |
| PY288 | V L I | E WILD | after:PY287 |
| PY289 | K I C | E AFTERFIGHT | after:PY288 |
| PY290 | I R K | E FARM | after:PY289 |
| PY291 | A I | E FARM | ASHE_REVEAL; after:PY290+24h |
| PY292 | G K R | E WILD | after:PY122 |
| PY293 | V G R | E LOC:Rorikstead | after:PY292 |
| PY294 | K G I | E LOC:Rorikstead | after:PY293 |
| PY295 | A G V | E FARM | ASHE_REVEAL; after:PY120; after:PY296 |
| PY296 | L G V | E CAMP | after:PY121; after:PY170 |
| PY297 | V C K | E LOC:Rorikstead | after:PY293 |
| PY298 | X G R | E CAMP | after:PY104 |
| PY299 | V X R | E INN | after:PY99 |
| PY300 | X C G | E CAMP | after:PY100 |
| PY301 | K X I | E WILD | after:PY99 |
| PY302 | L X S | E CAMP | after:PY99 |
| PY303 | X V P | E CAMP | COUNT(PY298..PY302)>=3 |
| PY304 | L I K | E AFTERFIGHT | after:PY52; after:PY289 |
| PY305 | A L G | E CAMP | ASHE_REVEAL; after:PY51 |
| PY306 | L G X | E AFTERFIGHT | after:PY305 |
| PY307 | S L K | E AFTERFIGHT | after:PY50 |
| PY308 | L C R | E CAMP | after:PY50 |
| PY309 | L K P | E CAMP+NIGHT | COUNT(PY304..PY308)>=4 |
| PY310 | C G L | E WILD | after:MN1; after:PY63 |
| PY311 | C K X | E CAMP | after:MN1; after:PY67 |
| PY312 | X L C | E CAMP | after:MN1; after:PY232 |
| PY313 | C P R | E CAMP | after:MN1; after:PY101 |
| PY314 | A C L | E CAMP | ASHE_REVEAL; after:MN1 |
| PY315 | C I P | E CAMP+NIGHT | after:MN1; COUNT(PY310..PY314)>=3 |
| PY316 | G V S | E INN | after:PY170 |
| PY317 | K L P | E WILD | after:PY110 |
| PY318 | V I P | E WILD | after:PY317 |
| PY319 | R G A | E CAMP | ASHE_REVEAL; after:PY84 |
| PY320 | R G V | E CAMP | after:PY56 |

### Part 6 - Fights and making up
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY321 | K C G | E AFTERFIGHT:riekling | — |
| PY322 | K C | T | after:PY321+12h |
| PY323 | R V P | E CITY, after a barter menu closes | — |
| PY324 | V R | T | after:PY323+12h |
| PY325 | X L I | E CAMP | — |
| PY326 | L X | T | after:PY325+12h |
| PY327 | X S K | T | SER_VAMP |
| PY328 | S X | T | after:PY327+12h |
| PY329 | A L R | E CAMP | ASHE_REVEAL |
| PY330 | L A | T | ASHE_REVEAL; after:PY329+12h |
| PY331 | G K V | E AFTERFIGHT | — |
| PY332 | K G | T | after:PY331+12h |
| PY333 | I V C | E MORNING, after a night at camp | — |
| PY334 | V I | T | after:PY333+12h |
| PY335 | R P X | E CAMP | — |
| PY336 | P R | T | after:PY335+12h |
| PY337 | X P K | E AFTERFIGHT | — |
| PY338 | P X | T | after:PY337+12h |
| PY339 | G I R | E CAMP | — |
| PY340 | G I | T | after:PY339+12h |
| PY341 | V K L | E CAMP | — |
| PY342 | K V | T | after:PY341+12h |
| PY343 | S P I | E MORNING, after a night at camp | — |
| PY344 | S P | T | after:PY343+12h |

### Part 7 - More rules
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY345 | K G L | E CAMP | after:PY108; after:PY255 |
| PY346 | I C R | E CAMP | after:PY290 |
| PY347 | V A | E CAMP | ASHE_REVEAL |
| PY348 | X C I | E CAMP | after:PY74 |
| PY349 | S R G | E CAMP | SER_VAMP |
| PY350 | K P A | E DUNGEON_DOOR | ASHE_REVEAL; K_TOG+ |
| PY351 | V L I | E MORNING, after a night at camp | — |
| PY352 | R X I | E CAMP | — |
| PY353 | C G K | E CAMP | — |
| PY354 | L K P | E CAMP | COUNT(PY345..PY353)>=4 |

### Part 8 - Holidays at camp
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY355 | R G P | E CAMP | m0 d1 (New Life); after:PY320 |
| PY356 | C K S | E CAMP | m1 d16 (Heart's Day) |
| PY357 | X A I | E CAMP | ASHE_REVEAL; m2 d7 (First Planting) |
| PY358 | I V P | E CAMP | m3 d28 (Jester's Day) |
| PY359 | X V G | E CAMP | m5 d16 (Mid Year); after:PY99; after:PY301 |
| PY360 | I K L | E CAMP | m7 d27 (Harvest's End) |
| PY361 | C L R | E CAMP+NIGHT | m8 d3 (Tales and Tallow) |
| PY362 | L C G | E CAMP | m9 d13 (Witches Festival) |
| PY363 | A G K | E CAMP | ASHE_REVEAL; m10 d20 (Warriors Festival) |
| PY364 | S P C | E CAMP | m11 d25 (Saturalia); RC_REDGOD |

### Part 9 - Letters home
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY365 | K G P | E CAMP or INN | — |
| PY366 | G R V | E CAMP or INN | — |
| PY367 | V X P | E CAMP or INN | VAL_FATHIS |
| PY368 | R K I | E CAMP or INN | — |
| PY369 | X L C | E CAMP or INN | — |
| PY370 | I C V | E CAMP or INN | INIGO_BV |
| PY371 | L A K | E CAMP or INN | ASHE_REVEAL; after:PY330 |
| PY372 | C P G | E CAMP | RC_MANOS |
| PY373 | S K P | E CAMP+NIGHT | DG_CAIRN |
| PY374 | A R P | E CAMP | ASHE_REVEAL; ASHE_Q1 |
| PY375 | P V X | E CAMP or INN | — |
| PY376 | L K G | E CITY | after:PY365+48h |

### Part 10 - Injuries and nursing
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY377 | K G P | E AFTERFIGHT | — |
| PY378 | K X I | E CAMP | after:PY377 |
| PY379 | R L P | E CAMP | LOW_HP_TODAY |
| PY380 | L P | E CAMP | after:PY379 |
| PY381 | G R X | E CAMP+NIGHT | — |
| PY382 | G R V | E MORNING | after:PY381 |
| PY383 | L G | E AFTERFIGHT:draugr | — |
| PY384 | C I R | E WILD | HARVEST |
| PY385 | A R P | E AFTERFIGHT | ASHE_REVEAL; after:PY134 |
| PY386 | S X P | E CAMP | SER_CURED |
| PY387 | V G R | E AFTERFIGHT | — |
| PY388 | I C R | E AFTERFIGHT | — |
| PY389 | R G | E CAVE | — |
| PY390 | P K X | E CAMP | HARDFIGHT_TODAY |

### Part 11 - Rainy days in the tent
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY391 | V G P | E CAMP+RAIN | — |
| PY392 | L X P | E CAMP+RAIN | — |
| PY393 | X K R | E CAMP+RAIN | — |
| PY394 | A G I | E CAMP+RAIN | ASHE_REVEAL |
| PY395 | C K L | E CAMP+RAIN | — |
| PY396 | V C I | E CAMP+RAIN | after:PY35 |
| PY397 | V S P | E CAMP+RAIN | — |
| PY398 | L G I | E CAMP+RAIN | after:PY391+48h |
| PY399 | K P | E CAMP+RAIN | K_TOG+; BRYNJAR |
| PY400 | I G R | E CAMP+RAIN | — |
| PY401 | R X K | E CAMP+RAIN | — |
| PY402 | C I S | E MORNING | RAIN_ENDED |

### Part 12 - Camp days
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY403 | C P G | E CAMP | after:PY179 |
| PY404 | G C R | E CAMP | after:PY403 |
| PY405 | V G K | E CAMP | — |
| PY406 | X G P | E CAMP | — |
| PY407 | I L C | E CAMP+WATER | — |
| PY408 | S G R | E CAMP | after:PY97 |
| PY409 | A K R | E WATER | ASHE_REVEAL |
| PY410 | P G L | E CAMP | — |
| PY411 | K V I | E CAMP | after:PY320 |
| PY412 | R X I | E CAMP | — |
| PY413 | L S K | E CAMP | — |
| PY414 | K I | E CAMP | after:PY322 |
| PY415 | V P X | E CAMP | after:PY225 |
| PY416 | R G V | E WATER (WILD) | after:PY89 |
| PY417 | X C | E CAMP | — |
| PY418 | I P G | E CAMP | — |

### Part 13 - Quiet days
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY419 | G I P | E CAMP+NIGHT | NO_FIGHT_TODAY |
| PY420 | X P | E PREDAWN at CAMP | — |
| PY421 | K G C | E CAMP | — |
| PY422 | S K | E PREDAWN | SER_CURED |
| PY423 | A I P | E CAMP+NIGHT | ASHE_REVEAL |
| PY424 | V G R | E WATER (WILD) | — |

### Part 14 - The anniversary
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PY425 | R X I | T | PARTY_YEAR2; after:PY180 |
| PY426 | G L P | E CAMP | after:PY425+24h |
| PY427 | L V K | E CAMP | after:PY426 |
| PY428 | C R P | E CAMP | after:PY426 |
| PY429 | K G P | E CAMP+NIGHT | after:PY426 |
| PY430 | I A P | E CAMP+NIGHT | ASHE_REVEAL; after:PY429 |

## 4. Notes
- Existing coverage avoided: Gore's Gorse comment on taming a wild horse (CC103: the new story keeps "the men laughed" and the pony jibe consistent), Xelzaz's Ginger Kiss barrel (HF52: PY406 is the first taste), the egg song at home (HF74: PY258 is Remi learning the harmony that Xelzaz feared), Redcap's dislike of bees (HF28: PY384 is the sting), Gore's letter for Helgen (PR68), Val's letter to his mother (PR85), Lucien's letters to his mother (PY150, BR32), Ashe's "Dear Canas" (PR193), Gore's and Luna's rules twelve and thirteen (PR67), Kaidan's bounty rules (MN13-MN118), Ashe's "I do not float" (PR112), the overdue three-week book (RV133: PY211-213 is a different, 312-year book), the Saturalia gift draw (H14), every holiday joke in SEASONS and 51.
- No Kaidan cult content, no Jo-Lee, no Mora, no Clive. Brynjar only in PY399 (gated `BRYNJAR`). Fathis only in PY367 (gated `VAL_FATHIS`). Sanguine only in PY364 (gated `RC_REDGOD`). Nobody says "Dragonborn".
- Kaidan's "Riekling scum" line in PY321 is his own canon hostility (kaidan.md / redcap.md section 4); the make-up (PY322) is where he changes.
- PY327-328 (the ox): purely a party misunderstanding; no record is touched. The ox and farm are generic.
- PY293, PY294, PY297: Lemkil's sign, queue and hat are party flavour only; no NPC or quest record is touched. Erik's boast in PY294 is a rumour; it does not need his "Erik the Slayer" quest.
- PY350 changes the party's walking order in words only; it does not touch follower AI.
