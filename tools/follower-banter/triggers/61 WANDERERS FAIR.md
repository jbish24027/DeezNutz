# 61 WANDERERS FAIR - trigger rows (prefix WF, WF1-WF60, 60 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\61 WANDERERS FAIR.txt`. Luna speaks in 21 (35%) of talks.
Mod: The Wanderer's Fair 2.0.1.3, `SkyrimFair.esp` (mod folder `The Wanderer's Fair`), read-only through houseCARL on 2026-10-21 (epoch e2-c72542933548abed): its NPC_, QUST, CELL, WRLD, ACTI, BOOK, GLOB records and all 92 INFO lines, plus the mod's `SkyrimFair - Credits.md`. Authoria's own fair patches matter here: the stage trim (5 dancers in one ring, singers lead + left only, band = lute + drum, no orchestra; memory `wanderers-fair-stage-trim-20261016`) and `Authoria - Fair Companion Guard` (the fair's companion finder). Nothing was written to the game.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), the Serana/Ashe Free rows in `20 DAWNGUARD.md` section 1 and Gore's `G_OK`. Rival codes as `53 RIVALRY.md` (`K_CRUSH`, `K_TOG+`, `G_FLIRT`, `V_FLIRT`, `S_ACT`, `A_CRUSH`, `STEP0`, ...). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna.

## 1. What the fair really has (verified)

- Worldspace **SkyrimFairWorld 000A16:SkyrimFair.esp** "The Wanderer's Fair" (99 cells, plus sandbox cell SkyrimFairSandbox 0009E1). Entered through a gate from Tamriel; map marker FairSiteMapMarker (Tamriel, Camp icon via the Authoria patch). A "Whiterun Fair" welcome sign stands by the path outside the gate. There is **no LCTN record** in the plugin, so location-change keywords cannot see the fair: use the worldspace.
- **33 stall keepers** with counters ("Browse <stall>", script SkyrimFairStallCounter): Imperial Armourer, Stormcloak / Nord Armourer, Sweetroll Stall, Fruit & Produce Stall, Hot Pie Stall, Mead & Ale Stall, Cheese & Dairy Stall, Bakery Stall, Roast Meat Stall, Spiced / Hot Drinks Stall, Honey & Beekeeping Stall, Spice & Imported Foods Trader, Iron & Steel Smith, Hunter & Leatherworker, Elven Goods Trader, Dwemer Curios Stall, Mage Supplies Stall, Alchemy Stall, Books & Scrolls Stall, Jeweller, General Trinkets & Curios, Fur Trader, Herbalist / Apothecary, Fishmonger / Smoked Fish, Bowyer & Fletcher, Clothing & Fine Fabrics, Woodworker / Carpenter, Pottery & Household Goods, Festival Toys & Gifts, Fortune Teller / Mystic Curios, Rare Goods / Travelling Merchant, Candle & Tallow Maker, Bard & Instrument Merchant.
- **Stage** (quest SkyrimFairAudioQuest 0014BD "Wanderer's Fair Stage"): band (lute 0014C1, drum 0014C5; flute and orchestra disabled in Authoria), singers (lead 0016B3, left 0016B6), a ring of five dancers, two folk dancers (paired folk dance). Songs: "The Wanderer's Fair", "Round the Green", "Hey-Ho, Skyrim", "Fiddle", "Dragonborn-Approved", "Raise Your Cups".
- **Archery**: four Fair Archers (base 001436); a fairgoer line talks about visitors trying the archery. **Whether the player or followers can actually shoot is [UNC]**; the talks treat it as "having a go" and never claim a prize from it.
- **Cameos** (quest SkyrimFairCameos 06000A): **Claudius Vale** (060004), the Fair Inspector (complaints, crowd estimates, lantern counts, "verifying" pies), and **Garrick Sol V** (060001), the cheerful showman who keeps the crowd dancing and denies all knowledge of the horse. **The horse on the roof** (060008), a running joke on the palisade notices ("Reward", "Witnesses Required", "Official Notice", "Case Update", and "A Statement from Garrick Sol V" behind the stage).
- **The Fair Passport** (SkyrimFairPassport 0B0006, stages 0/10/15/20; book 0B0002): stamps = watch a whole song (objective 10), talk to Garrick (20), chat with five visitors (40, global SkyrimFairPassportChats 0B0000), witness the horse on the roof (50), return it to Claudius (60). Reward: his Seal of Approval and the **Deed to the Roof Horse** (0B0003). The passport's terms include "not to be folded" and "Cabbages are not a stamp".
- Also: paper lanterns (tall red, round blue, other colours), scaffold light towers, bunting, palisade walls, an outhouse, a horse pen, chickens (020159), goats (020160), dogs (020164), fair children (001631), and ten voiced fairgoers.
- **Not in the mod (so not in the talks):** rides, a prize booth, games of chance, a contest with a trophy. Fireworks: a global `SkyrimFairFireworks` exists but nothing confirms a show, so no talk uses it.

## 2. Gate codes (this file)

- `FAIR` = player `GetInWorldspace SkyrimFairWorld (000A16:SkyrimFair.esp) == 1`. Alternative: global `SkyrimFairAtFair (0016B0:SkyrimFair.esp) == 1` **[UNC: meaning inferred from its name]**.
- `FAIR_ARRIVE` = event: first controller tick in SkyrimFairWorld after being outside it (fires once per visit; at most one arrival talk per visit). `FAIR_FIRST` = the first arrival ever. Give the fair's own arrival logic ~60 s before any talk (the arrival script flood and crowd cull, see memory `wanderers-fair-fps-20261014`).
- `FAIR_LEAVE` = event: player goes from SkyrimFairWorld back to Tamriel after at least one in-game hour inside.
- `SIGN` = player in Tamriel within ~1500 units of FairSiteMapMarker, before the first FAIR_ARRIVE **[UNC: the welcome-sign ref FormID was not pulled; the marker is near it]**.
- `NEAR:<stall>` = FAIR and player within ~600 units of either counter activator of that stall (FormIDs 090084-0900BA:SkyrimFair.esp, e.g. Sweetroll 090086/090087, Dwemer 09009B, Toys 0900B1/0900B2, Fortune 0900B3/0900B4, Jeweller 0900A1/0900A2, Honey 090094, Books 09009F/0900A0, Mage 09009C, Alchemy 09009D/09009E, Hot drinks 090092/090093, Mead 09008C/09008D, Roast 090090/090091, Fish 0900A8/0900A9, Clothing 0900AC, Fletcher 0900AA/0900AB, Bard 0900B9/0900BA, Candles 0900B7/0900B8, Rare 0900B5/0900B6, Bakery 09008F, Imperial 090084 + Stormcloak 090085).
- `NEAR:Stage` = FAIR and player within ~1500 units of the lute player ref (0014C1) **and** `SkyrimFairAudioMusicEnabled (0014AF) == 1`. `SONG` = NEAR:Stage while a song is playing **[UNC: SkyrimFairAudioScript exposes no public "playing" flag; fall back to NEAR:Stage]**. A talk naming a song title only plays on SONG and its line stays true for any song **[UNC: track detection]** (WF19 and WF20 are written so the title is a request or a memory, not a claim about what is on).
- `NEAR:Folk` (folk dancers, base 0016AB), `NEAR:Ring` (the dancers' ring by the stage), `NEAR:Archery` (any Fair Archer, base 001436), `NEAR:Claudius` (060004), `NEAR:Garrick` (060001), `NEAR:RoofHorse` (060008), `NEAR:Chicken` (020159), `NEAR:Goat` (020160), `NEAR:Dog` (020164), `NEAR:Child` (001631), `NEAR:Notices` (the palisade posters), `NEAR:Outhouse` = within ~600 units of a loaded actor/ref of that base **[UNC: placed-ref FormIDs for posters and the outhouse not pulled; actors via GetIsID on nearby actors]**.
- `PP_HAVE` = SkyrimFairPassport (0B0006) stage >= 10 and stage 20 not done **[UNC: 10 = passport handed over]**. `PP_GARRICK` = objective 20 completed. `PP_CHATS1` = SkyrimFairPassportChats >= 1. `PP_HORSE` = objective 50 completed. `PP_DONE` = stage 20 done (as OM115 in 59 OTHER QUEST MODS).
- `FAIR_NIGHT` = FAIR and hour >= 20 or < 5 (the lanterns are lit). `FAIR_RAIN` = FAIR and IsRaining **[UNC: the fair worldspace's weather follows Tamriel's? check in game]**.
- `FAIR_LOST` = event: in FAIR, the player has been more than ~2500 units from every follower for 60+ real seconds, and the talk's speakers are now back within 600 units. At most one FAIR_LOST talk per visit **[UNC: needs the controller to track it]**.
- `FAIR_VISITS>=n` = the controller counts FAIR_ARRIVE events.
- **Companions at the fair:** the fair's own companion finder brings up to six followers through the gate with you, by CurrentFollowerFaction (fixed for Gore's Vigilant doubles by `Authoria - Fair Companion Guard`). Val, Inigo, Serana and Ashe are not in that faction **[UNC: whether the finder carries them; their own frameworks may teleport them after you]**. Every talk still needs all speakers Free and within 1000 units, so a follower left outside simply never talks.
- Talks with a fair NPC nearby never interrupt that NPC's lines: also require `IsInDialogueWithPlayer == 0` on Claudius and Garrick.

## 3. Per-talk table

### Arriving (WF1-WF4)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF1 | P L | E SIGN | not FAIR_FIRST yet; LK_MET or any L talk played |
| WF2 | C K P | E FAIR_ARRIVE | FAIR_FIRST; after R1 |
| WF3 | R G | E FAIR_ARRIVE | FAIR_FIRST; HLIOGoreBanter intro done |
| WF4 | A X | E FAIR_ARRIVE | not FAIR_FIRST; ASHE_HIRED; after:WF2 or WF3 |

### Lost on the fairground (WF5-WF9)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF5 | G P | E FAIR_LOST | FAIR; after A1 |
| WF6 | C P | E FAIR_LOST | FAIR; RC_MET |
| WF7 | K P | E FAIR_LOST | FAIR; K_TOG+ |
| WF8 | A P | E FAIR_LOST | FAIR; ASHE_REVEAL |
| WF9 | I X | E FAIR_LOST | PP_GARRICK; after X6 |

### Redcap at the fair (WF10-WF15)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF10 | C X | E NEAR:Honey | FAIR; R18 played |
| WF11 | C R | E NEAR:Toys | FAIR; RC_MET |
| WF12 | C G | E NEAR:Outhouse | FAIR; after R5 |
| WF13 | C V | E NEAR:Goat | FAIR; RC_MANOS; after R8 |
| WF14 | C L | E SONG | FAIR; after R11 |
| WF15 | C P | T | FAIR; RC_STAY; one per visit |

### Inigo at the fair (WF16-WF20)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF16 | I L | E NEAR:Sweetroll | FAIR; LI_RANK2 |
| WF17 | I S | E NEAR:Chicken | FAIR; SE8 played |
| WF18 | I P | E NEAR:Folk | FAIR |
| WF19 | I K | E NEAR:Archery | FAIR; KI_MET |
| WF20 | G I | E NEAR:Child | FAIR; after C2 |

### The stalls (WF21-WF33)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF21 | R V | E NEAR:Dwemer | FAIR; HLIOValBanter stage >= 10 |
| WF22 | X R | E NEAR:Alchemy | FAIR; RX_OK; not RX_SULK |
| WF23 | P L | E NEAR:Books | FAIR; LK_MET or any L talk played |
| WF24 | P X | E NEAR:Mage | FAIR; MG_JOIN |
| WF25 | G K | E NEAR:Imperial | FAIR; after A1 |
| WF26 | G K | E NEAR:Roast | FAIR; after A1 |
| WF27 | X I | E NEAR:Hotdrinks | FAIR; X6 played |
| WF28 | G C | E NEAR:Fishmonger | FAIR; after R5 |
| WF29 | V L | E NEAR:Clothing | FAIR; after C1 |
| WF30 | S L | E NEAR:Fortune | FAIR; SE34 played |
| WF31 | V G | E NEAR:Bard | FAIR; after A3 |
| WF32 | R S | E NEAR:Bakery | FAIR; SDA Remiel intro done [UNC: Creme Treat props are at the fair; which stall shows them] |
| WF33 | L C | E NEAR:Rare | FAIR; after R11 [UNC: stall stock; the line is the merchant's claim] |

### The stage (WF34-WF40)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF34 | L G | E SONG | FAIR; after L1 |
| WF35 | X L | E SONG | FAIR; XL_MET |
| WF36 | K G P | E NEAR:Stage | FAIR; DB; after A1 |
| WF37 | V R | E SONG | FAIR; HLIOValBanter stage >= 10 |
| WF38 | S P | E SONG | PP_HAVE; SE34 played |
| WF39 | A G | E NEAR:Ring | FAIR; ASHE_REVEAL; after C2 |
| WF40 | K P | E SONG | FAIR; K_TOG+ |

### Claudius, Garrick and the horse on the roof (WF41-WF49)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF41 | R P | T | PP_HAVE; B6 played or any R talk played |
| WF42 | C P | T | PP_HAVE; RC_MET |
| WF43 | L G | T | PP_GARRICK; after L1 |
| WF44 | K X | E NEAR:Claudius | FAIR; after C3 |
| WF45 | L S | E NEAR:Notices | FAIR; SE34 played |
| WF46 | R A | E NEAR:RoofHorse | FAIR; not PP_HORSE; ASHE_REVEAL; after:any A+R talk |
| WF47 | V P | E NEAR:Notices | FAIR; after A2 |
| WF48 | I P | E after Claudius line 0B000B plays [UNC: detect the INFO via a controller check on the topic]; I near |  |
| WF49 | C K | E NEAR:RoofHorse | FAIR; after R1 |

### The rivals and the prize (WF50-WF56)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF50 | V K P | E NEAR:Archery | FAIR; STEP0; after A2 [UNC: whether visitors can shoot; the talk works as banter either way] |
| WF51 | K P | E NEAR:Toys | FAIR; K_CRUSH [UNC: stall stock; the toy is flavour] |
| WF52 | G V | T | FAIR; G_FLIRT; V_FLIRT |
| WF53 | V K | E NEAR:Jeweller | FAIR; V_FLIRT; K_CRUSH |
| WF54 | S K | E NEAR:Mead | FAIR; S_ACT; K_CRUSH |
| WF55 | G A | E NEAR:Archery | FAIR; A_CRUSH; G_FLIRT; ASHE_REVEAL |
| WF56 | G K | T | FAIR; K_TOG+; G_PAST |

### Night and leaving (WF57-WF60)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| WF57 | R G | E FAIR_NIGHT | FAIR; HLIOGoreBanter intro done |
| WF58 | V S | E FAIR_RAIN | FAIR; SE15 played |
| WF59 | K P | E NEAR:Dog | FAIR |
| WF60 | L C P | E FAIR_LEAVE | after R11 |

