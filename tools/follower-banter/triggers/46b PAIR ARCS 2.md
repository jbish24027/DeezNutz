# 46b PAIR ARCS 2 - trigger rows (prefix PR, PR221-PR470, 250 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\46b PAIR ARCS 2.txt`.
Part 1: `46 PAIR ARCS.txt` / `triggers\46 PAIR ARCS.md` (PR1-PR220). Every rule, code and controller behaviour in that file's sections 1, 2 and 5 applies here unchanged (one chain per pair, `after:`, `GAP2`, `SKIPPABLE`, side talks, one PR talk per pair per day).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana and Ashe `Free` rows in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue). Codes are listed in speaking order.

## 1. How chapter 2 plays

- **Section 1 (PR221-PR410): second chapters.** Each of the 45 pairs gets a new chain of 4 talks. Its first talk waits for the **last chain talk of that pair's part-1 arc** (`after:PR5`, `after:PR12`, ...), plus `GAP2`. Side talks of part 1 are never waited on. If a part-1 chain is stuck behind a story gate, chapter 2 simply waits with it (same rule as part 1). One exception is written into its row: PR278 may go past PR78 after 10 game days.
- **Side talks (10, one per rival pair).** Same as part 1: they hang off that pair's part-1 side talk with `after:`, need their romance gates at the moment they fire, block nothing, and Luna never speaks in them or chooses anyone in them. List in section 4.
- **Section 2 (PR411-PR470): Luna with each follower.** Ten new chains of 6 talks, speakers = the follower + Luna. Each chain starts on `LN_MET:<x>` (below) and then runs with `after:` + `GAP2` like every other chain. These chains are **separate from the pair chains**, so a follower can be in a pair chain and a Luna chain at the same time; the "one PR talk per pair per day" rule treats Luna+X as its own pair.
- **Rival Luna chains stay friendship only.** Gore, Val, Serana and Ashe chains carry a "not together" gate on every talk (`not G_TOG+`, `not V_TOG+`, `NOT_S_KISS`, `not A_LOVE`). If you get together with that follower mid-chain, the chain pauses for good (their own mods carry the romance); if a romance ends (breakup / friend zone), it resumes. **Kaidan's chain** is two halves: PR411-PR413 are `K_CRUSH` (Luna oblivious) and `SKIPPABLE` once the crush stage has passed; PR414-PR416 need `K_TOG+`.

## 2. Gate codes new in this file

- `LN_MET:<x>` = follower `<x>` has been `Free()` on at least **10 different game days** (controller keeps a per-follower day count; a day counts once the follower was Free at any controller tick that day). **[UNC: new counter in the controller script]** For Serana also `SERANA`; for Ashe also `ASHE_HIRED`.
- `KMD_DONE` = Kaidan's KMDQuest "Blood and Fire" completed (`KMDQuest`, 0Kaidan.esp / Kaidan - Immersive Features.esp). **[UNC: FormID and completion stage]** This is the only talk in the file that names the Blooded Dawn (PR239), as the style guide requires.
- `ASHE_AMENDS` = MM_AMQ_06a (C07BE9), 06b (C11E04) and 06cNEW (380306), all `Ashe - Fire and Blood.esp`, completed (ashe.md section 6).
- `NOT_S_KISS` = as `20 DAWNGUARD.md` section 3 (Serana's romance is off, or below the kiss).
- `E AFTERFIGHT:mage` = combat just ended and the last target was a mage-class enemy or in a necromancer/warlock faction (`VampireFaction` excluded). **[UNC: use class keyword ActorTypeNPC + MagicSchool combat style, or Warlock/Necromancer factions]**
- `E SEA+SUNNY` = `SEA` (part 1 section 2) and `SUNNY` together.
- `E CAMP+CLEARNIGHT` = `CAMP` and `CLEARNIGHT` together. `E PREDAWN+CAMP` = `PREDAWN` and `CAMP` together.
- `E exterior, hour 9..17` = any exterior, daytime (Serana resting from the sun).
- Existing codes used: `K_*`, `G_*`, `V_*`, `BRYNJAR`, `HELGEN_LOC`, `GORE_BAIL`, `VAL_FATHIS`, `BLACKBOOK`, `INIGO_BV`, `LUC_ADMIT`, `RC_MANOS`, `RC_REDGOD` (TRIGGERS.md section 4); `SERANA`, `SER_VAMP`, `DG_END`, `DG_GARDEN`, `S_COMP`, `A_CRUSH`, `A_LOVE`, `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `ASHE_LOGS` (`20 DAWNGUARD.md` section 3); `RX_OK`, `RG_READ`, `BIGPIG`, `SEA`, `SUNNY`, `WILD`, `exterior`, `not CITY` (`46 PAIR ARCS.md` section 2); `Val00A >= 10`, `K04 >= 5` (as part 1).

## 3. Per-talk table


### Part 46 - Kaidan and Gore, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR221 | G K | T | after:PR5; GAP2 |
| PR222 | K G | E CAMP+NIGHT | after:PR221; GAP2 |
| PR223 | K G | T | after:PR222; GAP2 |
| PR224 | G K | E AFTERFIGHT | after:PR223; GAP2 |
| PR225 | G K | T | after:PR7; K_LOVE+; not G_TOG+ |

### Part 47 - Kaidan and Val, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR226 | K V | T | after:PR12; GAP2 |
| PR227 | V K | E WATER | after:PR226; GAP2 |
| PR228 | V K | T | after:PR227; GAP2; BRYNJAR |
| PR229 | K V P | T | after:PR228; GAP2 |
| PR230 | K V | E PREDAWN+CAMP | after:PR14; V_TOG+ |

### Part 48 - Gore and Val, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR231 | G V | T | after:PR19; GAP2 |
| PR232 | G V | E CAMP | after:PR231; GAP2 |
| PR233 | V G | E CAMP+NIGHT | after:PR232; GAP2; VAL_FATHIS |
| PR234 | G V | T | after:PR233; GAP2 |
| PR235 | V G | T | after:PR21; G_OATH |

### Part 49 - Kaidan and Remi, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR236 | R K | T | after:PR26; GAP2 |
| PR237 | R K | E CAMP+NIGHT | after:PR236; GAP2 |
| PR238 | R K P | E AFTERFIGHT | after:PR237; GAP2 |
| PR239 | K R | T | after:PR238; GAP2; KMD_DONE; not CITY |

### Part 50 - Kaidan and Xelzaz, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR240 | X K | T | after:PR31; GAP2 |
| PR241 | X K | E CAMP+NIGHT | after:PR240; GAP2 |
| PR242 | K X P | E CITY:Windhelm | after:PR241; GAP2 |
| PR243 | X K | T | after:PR242; GAP2 |

### Part 51 - Kaidan and Lucien, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR244 | L K | T | after:PR36; GAP2 |
| PR245 | L K | T | after:PR244; GAP2; LUC_ADMIT |
| PR246 | L K | T | after:PR245; GAP2 |
| PR247 | L K | E CAMP | after:PR246; GAP2 |

### Part 52 - Kaidan and Redcap, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR248 | K C | T | after:PR41; GAP2; exterior |
| PR249 | C K | E CAMP+NIGHT | after:PR248; GAP2 |
| PR250 | C K | T | after:PR249; GAP2 |
| PR251 | C K | T | after:PR250; GAP2 |

### Part 53 - Kaidan and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR252 | S K | E CAMP | after:PR46 (SKIPPABLE chain rule: after:PR45 if PR46 was skipped); GAP2 |
| PR253 | S K P | E INN | after:PR252; GAP2 |
| PR254 | S K | T | after:PR253; GAP2; DG_END; BRYNJAR |
| PR255 | S K | E AFTERFIGHT:Thalmor | after:PR254; GAP2 |
| PR256 | S K | T | after:PR47; G_TOG+; K04 >= 5; S_COMP |

### Part 54 - Kaidan and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR257 | A K P | T | after:PR52; GAP2 |
| PR258 | A K | E AFTERFIGHT | after:PR257; GAP2 |
| PR259 | A K | E CAMP+NIGHT | after:PR258; GAP2; ASHE_LOGS |
| PR260 | A K | T | after:PR259; GAP2 |
| PR261 | K A | T | after:PR53; A_CRUSH; K_LOVE+ |

### Part 55 - Gore and Xelzaz, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR262 | G X | E MORNING | after:PR58; GAP2 |
| PR263 | G X | E CAMP | after:PR262; GAP2 |
| PR264 | X G | E WATER | after:PR263; GAP2 |
| PR265 | G X | E SNOW | after:PR264; GAP2 |

### Part 56 - Gore and Inigo, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR266 | I G | T | after:PR63; GAP2 |
| PR267 | G I | T | after:PR266; GAP2; exterior |
| PR268 | I G | E CAMP+NIGHT | after:PR267; GAP2 |
| PR269 | P G I | E CAMP+NIGHT | after:PR268; GAP2 |

### Part 57 - Gore and Lucien, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR270 | G L | E HELGEN_LOC | after:PR68; GAP2 |
| PR271 | L G | E AFTERFIGHT:mage | after:PR270; GAP2 |
| PR272 | G L P | E CAMP | after:PR271; GAP2 |
| PR273 | L G | T | after:PR272; GAP2 |

### Part 58 - Gore and Redcap, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR274 | C G | T | after:PR73; GAP2 |
| PR275 | C G | E SNOW | after:PR274; GAP2 |
| PR276 | C G | E CAMP | after:PR275; GAP2 |
| PR277 | G C P | T | after:PR276; GAP2 |

### Part 59 - Gore and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR278 | S G | T | after:PR78, or after:PR77 if PR78 has waited 10+ game days for GORE_VIG/GORE_FATHER (PR78 stays eligible); GAP2 |
| PR279 | G S P | T | after:PR278; GAP2 |
| PR280 | G S | E CAMP+NIGHT | after:PR279; GAP2 |
| PR281 | G S | T | after:PR280; GAP2 |
| PR282 | G S | T | after:PR76; S_COMP; G_FLIRT; not K_TOG+, not V_TOG+, not G_TOG+, not S_KISS, not A_LOVE |

### Part 60 - Gore and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR283 | G A | E CAMP | after:PR82; GAP2 |
| PR284 | G A | T | after:PR283; GAP2 |
| PR285 | G A | T | after:PR284; GAP2; ASHE_Q1 |
| PR286 | A G | E exterior | after:PR285; GAP2 |
| PR287 | A G | T | after:PR83; G_TOG+; A_CRUSH; ASHE_REVEAL |

### Part 61 - Val and Xelzaz, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR288 | X V P | T | after:PR88; GAP2 |
| PR289 | V X | E WATER (SEA or large lake) | after:PR288; GAP2 |
| PR290 | V X | T | after:PR289; GAP2 |
| PR291 | X V | E MORNING | after:PR290; GAP2 |

### Part 62 - Val and Inigo, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR292 | V I | T | after:PR93; GAP2 |
| PR293 | I V | E CITY:Riften | after:PR292; GAP2; INIGO_BV |
| PR294 | V I P | T | after:PR293; GAP2 |
| PR295 | V I | T | after:PR294; GAP2 |

### Part 63 - Val and Lucien, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR296 | V L | T | after:PR98; GAP2 |
| PR297 | L V | E CAMP+NIGHT | after:PR296; GAP2 |
| PR298 | V L P | T | after:PR297; GAP2 |
| PR299 | L V | T | after:PR298; GAP2; BLACKBOOK |

### Part 64 - Val and Redcap, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR300 | C V | E MORNING | after:PR103; GAP2 |
| PR301 | C V | E SEA | after:PR300; GAP2 |
| PR302 | V C P | E CAMP | after:PR301; GAP2 |
| PR303 | C V | T | after:PR302; GAP2 |

### Part 65 - Val and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR304 | S V | E CAMP+NIGHT | after:PR108 (SKIPPABLE chain rule back to PR106); GAP2; DG_END |
| PR305 | V S P | E SEA+SUNNY | after:PR304; GAP2; SER_VAMP; SKIPPABLE |
| PR306 | V S | T | after:PR305; GAP2 |
| PR307 | V S | E NIGHT | after:PR306; GAP2 |
| PR308 | S V | E INN | after:PR109; K_LOVE+; Val00A >= 10; S_COMP |

### Part 66 - Val and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR309 | A V P | E WATER | after:PR114; GAP2 |
| PR310 | V A | E CAMP+NIGHT | after:PR309; GAP2 |
| PR311 | A V | T | after:PR310; GAP2; ASHE_AMENDS |
| PR312 | A V | T | after:PR311; GAP2 |
| PR313 | V A | T | after:PR115; A_CRUSH; Val00A >= 10; K_TOG+ |

### Part 67 - Remi and Inigo, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR314 | R I | T | after:PR120; GAP2 |
| PR315 | R I | E CAMP+NIGHT | after:PR314; GAP2 |
| PR316 | R I P | E CITY | after:PR315; GAP2 |
| PR317 | R I | T | after:PR316; GAP2 |

### Part 68 - Remi and Lucien, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR318 | L R | T | after:PR125; GAP2 |
| PR319 | L R | T | after:PR318; GAP2 |
| PR320 | R L P | E CITY | after:PR319; GAP2 |
| PR321 | L R | T | after:PR320; GAP2 |

### Part 69 - Remi and Redcap, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR322 | C R | T | after:PR130; GAP2 |
| PR323 | R C | E CAMP | after:PR322; GAP2 |
| PR324 | R C | T | after:PR323; GAP2; RC_MANOS |
| PR325 | R C | T | after:PR324; GAP2; BIGPIG |

### Part 70 - Remi and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR326 | R S P | E SNOW exterior | after:PR135; GAP2 |
| PR327 | S R | E INN | after:PR326; GAP2 |
| PR328 | R S | E CAMP+NIGHT | after:PR327; GAP2 |
| PR329 | S R | T | after:PR328; GAP2 |

### Part 71 - Remi and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR330 | A R | E AFTERFIGHT | after:PR140; GAP2 |
| PR331 | R A | E CITY | after:PR330; GAP2 |
| PR332 | R A | T | after:PR331; GAP2 |
| PR333 | A R P | E CAMP | after:PR332; GAP2 |

### Part 72 - Xelzaz and Inigo, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR334 | X I | T | after:PR145; GAP2 |
| PR335 | I X | E CAMP+NIGHT | after:PR334; GAP2 |
| PR336 | I X | T | after:PR335; GAP2 |
| PR337 | I X | T | after:PR336; GAP2 |

### Part 73 - Xelzaz and Lucien, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR338 | X L | T | after:PR150; GAP2 |
| PR339 | L X P | E MORNING | after:PR338; GAP2 |
| PR340 | L X | T | after:PR339; GAP2 |
| PR341 | L X | E DWEMER | after:PR340; GAP2 |

### Part 74 - Xelzaz and Redcap, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR342 | C X | T | after:PR155; GAP2 |
| PR343 | X C | E CAMP | after:PR342; GAP2 |
| PR344 | C X | T | after:PR343; GAP2; RC_MANOS |
| PR345 | C X | E CITY:Windhelm | after:PR344; GAP2 |

### Part 75 - Xelzaz and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR346 | S X | E INN | after:PR160; GAP2 |
| PR347 | S X | T | after:PR346; GAP2 |
| PR348 | X S | E CAMP+NIGHT | after:PR347; GAP2 |
| PR349 | S X P | E CITY:Whiterun | after:PR348; GAP2 |

### Part 76 - Xelzaz and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR350 | X A | T | after:PR165; GAP2 |
| PR351 | A X | E CAMP | after:PR350; GAP2 |
| PR352 | X A | E CAMP+NIGHT | after:PR351; GAP2; ASHE_LOGS |
| PR353 | A X | E SNOW | after:PR352; GAP2 |

### Part 77 - Inigo and Redcap, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR354 | C I | T | after:PR170; GAP2 |
| PR355 | I C | E CAVE | after:PR354; GAP2 |
| PR356 | I C | T | after:PR355; GAP2; exterior |
| PR357 | C I | T | after:PR356; GAP2; RC_REDGOD |

### Part 78 - Inigo and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR358 | S I | T | after:PR175; GAP2 |
| PR359 | P S I | E MORNING | after:PR358; GAP2 |
| PR360 | S I | E CAMP | after:PR359; GAP2 |
| PR361 | I S | E CAMP+NIGHT | after:PR360; GAP2 |

### Part 79 - Inigo and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR362 | A I | E CAMP+CLEARNIGHT | after:PR180; GAP2 |
| PR363 | I A P | E CAVE | after:PR362; GAP2 |
| PR364 | A I | T | after:PR363; GAP2; ASHE_AMENDS |
| PR365 | A I | T | after:PR364; GAP2 |

### Part 80 - Lucien and Redcap, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR366 | C L | T | after:PR185; GAP2 |
| PR367 | L C | T | after:PR366; GAP2 |
| PR368 | C L | E CAMP | after:PR367; GAP2 |
| PR369 | C L | E CAMP | after:PR368; GAP2 |

### Part 81 - Lucien and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR370 | L S | T | after:PR190; GAP2 |
| PR371 | S L | T | after:PR370; GAP2 |
| PR372 | S L | E CRYPT | after:PR371; GAP2 |
| PR373 | S L | E CAMP+NIGHT | after:PR372; GAP2 |

### Part 82 - Lucien and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR374 | A L | T | after:PR195; GAP2 |
| PR375 | L A | E CLEARNIGHT | after:PR374; GAP2 |
| PR376 | A L | T | after:PR375; GAP2 |
| PR377 | A L | E CAMP+NIGHT | after:PR376; GAP2; ASHE_AMENDS |

### Part 83 - Redcap and Serana, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR378 | S C | E CLEARNIGHT | after:PR200; GAP2 |
| PR379 | S C | E CAMP | after:PR378; GAP2 |
| PR380 | S C | T | after:PR379; GAP2; BIGPIG |
| PR381 | S C | E exterior, hour 9..17 | after:PR380; GAP2; SER_VAMP; SKIPPABLE |

### Part 84 - Redcap and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR382 | C A | T | after:PR205; GAP2 |
| PR383 | A C | T | after:PR382; GAP2 |
| PR384 | C A | E CAMP+NIGHT | after:PR383; GAP2 |
| PR385 | C A | E exterior | after:PR384; GAP2 |

### Part 85 - Serana and Ashe, Chapter 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR386 | A S | T | after:PR209; GAP2; DG_END |
| PR387 | S P A | E RAIN | after:PR386; GAP2 |
| PR388 | A S | E INN | after:PR387; GAP2 |
| PR389 | A S | T | after:PR388; GAP2 |
| PR390 | A S | T | after:PR210; K_LOVE+; S_COMP or A_CRUSH |

### Part 86 - Kaidan and Inigo, Fresh Callbacks 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR391 | I K | T | after:PR212; GAP2 |
| PR392 | K I | E CAMP+NIGHT | after:PR391; GAP2 |
| PR393 | K I | T | after:PR392; GAP2 |
| PR394 | I K | T | after:PR393; GAP2 |

### Part 87 - Lucien and Inigo, Fresh Callbacks 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR395 | L I | T | after:PR214; GAP2 |
| PR396 | L I | T | after:PR395; GAP2 |
| PR397 | I P L | E CRYPT | after:PR396; GAP2 |
| PR398 | I L | T | after:PR397; GAP2 |

### Part 88 - Remi and Xelzaz, Fresh Callbacks 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR399 | R X | T | after:PR216; GAP2; RX_OK |
| PR400 | R X | E CAMP+NIGHT | after:PR399; GAP2; RX_OK |
| PR401 | R X | T | after:PR400; GAP2; RX_OK |
| PR402 | X R | T | after:PR401; GAP2; RX_OK |

### Part 89 - Remi and Val, Fresh Callbacks 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR403 | V R | E WATER | after:PR218; GAP2 |
| PR404 | V R | E INN | after:PR403; GAP2 |
| PR405 | R V | E CAMP+NIGHT | after:PR404; GAP2 |
| PR406 | R V | T | after:PR405; GAP2 |

### Part 90 - Remi and Gore, Fresh Callbacks 2
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR407 | G R | E DWEMER | after:PR220; GAP2 |
| PR408 | R G P | T | after:PR407; GAP2; exterior |
| PR409 | G R | E CAMP+NIGHT | after:PR408; GAP2 |
| PR410 | R G | T | after:PR409; GAP2 |

### Part 91 - Luna and Kaidan
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR411 | K P | T | LN_MET:K; K_CRUSH; SKIPPABLE |
| PR412 | K P | E SNOW | after:PR411; GAP2; K_CRUSH; SKIPPABLE |
| PR413 | P K | E exterior | after:PR412; GAP2; K_CRUSH; SKIPPABLE |
| PR414 | P K | T | after:PR413; GAP2; K_TOG+ |
| PR415 | K P | T | after:PR414; GAP2; K_TOG+; BRYNJAR |
| PR416 | P K | E PREDAWN | after:PR415; GAP2; K_TOG+ |

### Part 92 - Luna and Gore
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR417 | G P | E WILD | LN_MET:G; RG_READ or GORE_BAIL; not G_TOG+ |
| PR418 | P G | E CAMP | after:PR417; GAP2; not G_TOG+ |
| PR419 | G P | T | after:PR418; GAP2; GORE_BAIL; not G_TOG+ |
| PR420 | P G | E WATER | after:PR419; GAP2; not G_TOG+ |
| PR421 | G P | T | after:PR420; GAP2; not G_TOG+ |
| PR422 | P G | E AFTERFIGHT | after:PR421; GAP2; not G_TOG+ |

### Part 93 - Luna and Val
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR423 | V P | T | LN_MET:V; not V_TOG+ |
| PR424 | P V | E MORNING | after:PR423; GAP2; not V_TOG+ |
| PR425 | V P | E CITY | after:PR424; GAP2; not V_TOG+ |
| PR426 | P V | T | after:PR425; GAP2; VAL_FATHIS; not V_TOG+ |
| PR427 | V P | E CAMP+NIGHT | after:PR426; GAP2; not V_TOG+ |
| PR428 | P V | T | after:PR427; GAP2; not V_TOG+ |

### Part 94 - Luna and Remi
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR429 | R P | T | LN_MET:R |
| PR430 | P R | T | after:PR429; GAP2 |
| PR431 | R P | T | after:PR430; GAP2 |
| PR432 | R P | E CAVE or DWEMER | after:PR431; GAP2 |
| PR433 | R P | E CAMP | after:PR432; GAP2 |
| PR434 | R P | T | after:PR433; GAP2 |

### Part 95 - Luna and Xelzaz
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR435 | X P | E CAMP | LN_MET:X |
| PR436 | P X | T | after:PR435; GAP2 |
| PR437 | X P | T | after:PR436; GAP2 |
| PR438 | P X | T | after:PR437; GAP2 |
| PR439 | X P | E CAMP | after:PR438; GAP2 |
| PR440 | P X | E RAIN exterior | after:PR439; GAP2 |

### Part 96 - Luna and Inigo
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR441 | I P | E CAMP | LN_MET:I |
| PR442 | I P | T | after:PR441; GAP2 |
| PR443 | I P | T | after:PR442; GAP2 |
| PR444 | P I | T | after:PR443; GAP2; INIGO_BV |
| PR445 | I P | E CAVE | after:PR444; GAP2 |
| PR446 | P I | E CAMP+NIGHT | after:PR445; GAP2 |

### Part 97 - Luna and Lucien
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR447 | L P | T | LN_MET:L |
| PR448 | P L | T | after:PR447; GAP2 |
| PR449 | L P | E CAMP | after:PR448; GAP2 |
| PR450 | P L | T | after:PR449; GAP2 |
| PR451 | L P | E CAMP+NIGHT | after:PR450; GAP2 |
| PR452 | P L | E CLEARNIGHT | after:PR451; GAP2 |

### Part 98 - Luna and Redcap
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR453 | C P | E CAMP | LN_MET:C |
| PR454 | P C | E MORNING | after:PR453; GAP2 |
| PR455 | C P | E CAMP+NIGHT | after:PR454; GAP2 |
| PR456 | C P | T | after:PR455; GAP2 |
| PR457 | C P | T | after:PR456; GAP2 |
| PR458 | P C | E WILD | after:PR457; GAP2 |

### Part 99 - Luna and Serana
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR459 | P S | T | LN_MET:S; SERANA; NOT_S_KISS |
| PR460 | S P | T | after:PR459; GAP2; NOT_S_KISS |
| PR461 | P S | E SUNNY | after:PR460; GAP2; SER_VAMP; SKIPPABLE; NOT_S_KISS |
| PR462 | S P | T | after:PR461; GAP2; DG_GARDEN; NOT_S_KISS |
| PR463 | S P | E CAMP+NIGHT | after:PR462; GAP2; NOT_S_KISS |
| PR464 | P S | T | after:PR463; GAP2; DG_GARDEN; NOT_S_KISS |

### Part 100 - Luna and Ashe
| ID | Speakers | Type | Gates |
|---|---|---|---|
| PR465 | A P | T | LN_MET:A; ASHE_HIRED; not A_LOVE |
| PR466 | P A | E CAMP | after:PR465; GAP2; not A_LOVE |
| PR467 | A P | E WILD | after:PR466; GAP2; not A_LOVE |
| PR468 | A P | E CAMP+NIGHT | after:PR467; GAP2; ASHE_Q1; not A_LOVE |
| PR469 | P A | T | after:PR468; GAP2; ASHE_REVEAL; not A_LOVE |
| PR470 | A P | E AFTERFIGHT | after:PR469; GAP2; not A_LOVE |


## 4. Side talks (romance-gated, outside the chains)

PR225, PR230, PR235, PR256, PR261, PR282, PR287, PR308, PR313, PR390

Each needs its romance gate at the moment it fires. Luna has no line in any of them, and none of them has Luna choose anyone.

## 5. Notes for the build

- Luna speaks in 86 of the 250 talks (34%): all 60 of section 2, and 26 of the 190 in section 1.
- No "Dragonborn" anywhere. The only cult reference is PR239 (Kaidan tells Remi about the Blooded Dawn), gated `KMD_DONE`. Brynjar is named only in PR254 and PR415, both behind `BRYNJAR`; PR228 also waits for `BRYNJAR` because it is about his mother's sword.
- Talks that wait on a quest the player may never do (`KMD_DONE`, `VAL_FATHIS`, `BLACKBOOK`, `ASHE_AMENDS`, `ASHE_LOGS`, `RC_MANOS`, `RC_REDGOD`, `DG_END`, `DG_GARDEN`) are late steps of their chain, so each chapter still gets its first talks. Exceptions: PR304 and PR386 (chapter openers) need `DG_END`, because their part-1 chains already end on Harkon's death.
- `SER_VAMP` talks (PR305, PR381, PR461) are `SKIPPABLE`; the talk after each one reads fine either way.
- Written alongside 45b PARTY LIFE 2, 53 RIVALRY, 54 FOLLOWER QUESTS CROSSTALK, 55 TRAVEL AND THE ROAD and 56 WORLD ENCOUNTERS. Their topics were checked and avoided where they collided (Kaidan's letter to Farkas, Luna teaching Gore Candlelight, the "Luna/tuna" rhyme, Val's new jar for Mr Dragonfly, Serana's snowball war). `dup_scan.py` shows no repeated 6+ word line involving PR221-PR470.
- Callbacks into part 1 are the point of chapter 2 (pinecones, "Lieutenant", the attempt count, "Valerius, age nine", "toward", "Kaidan Who Cannot Sneak", Kaidancap, the mead war, the stop-me promise, the horker sandwich, "Xel" on fish days, the wine cart, rule twelve, Raven/Bigpig, Heide's name, fourteen percent, the danish recipe, the room with no hats, three sweetrolls, Faelin and the figs, the bowline, the hat, the true record, the whiskers, the byline, melancholy, the missed-things list, Calculus, the egg song, "a very good day", Scalecap, the party, the three jokes, captain Bluecat, Grandmother, counting stars, R, three questions a day, boots on the moon, Star Lady, Metal Lady, the garden corner, the notches, "once a day", the tea bell, the ledger, Scrap's clicks).

