# 53b RIVALRY 2 - trigger rows (prefix RV, RV201-RV300, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\53b RIVALRY 2.txt`.
Part one and its gate codes: `triggers\53 RIVALRY.md` (S_/A_ codes, RIV2, pacing rule). Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4 and 8, `research\triggers\kaidan_block.md`, `others_block.md`, `vanilla_gates.md`, `triggers\20 DAWNGUARD.md` (Serana/Ashe Free rows and codes), `triggers\57 INNS AND TOWN LIFE.md` (`BARD_PLAYING`), `triggers\45b PARTY LIFE 2.md` (`E FARM`), `triggers\11 LEGACY OF THE DRAGONBORN.md` (pair codes `KI`, `LI`, `RX`).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, S Serana, A Ashe, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment).

Every row with S also needs `SERANA` (DLC1VQ02 stage 5 done) and Serana Free. Every row with A also needs `ASHE_HIRED` (MM_AsheIntro 0A7946 completed) and Ashe Free, plus her silence list (49 ASHE.md).

## Gate codes used in this file

Reused unchanged: `STEP0`, `K_CRUSH`, `K_TOG+`, `G_FLIRT`, `G_TOG+`, `V_FLIRT`, `V_TOG+`, `BRYNJAR` (TRIGGERS.md section 4); `S_ACT`, `A_LOVE` (53 RIVALRY.md / 20 DAWNGUARD.md); `S_KISS`, `SERANA`, `ASHE_HIRED` (20 DAWNGUARD.md / 33 DARK BROTHERHOOD.md); `BARD_PLAYING` (57 INNS AND TOWN LIFE.md); `E FARM` (45b PARTY LIFE 2.md).

Pair codes (11 LEGACY OF THE DRAGONBORN.md): `KI` = KaiandInigo stage >= 10. `LI` = JRLucienInigoRank >= 2. `RX` = Remi and Xelzaz own intro done (BPUFXelzazAndRemielInteractions stage 11 done) and not in the falling-out window (others_block.md 4a). `LK` = Lucien-Kaidan intro done (Lucien's own scene 1, as K5's row) **[UNC: JRLucienFollowerKaidanScene1 played flag]**.

New here:
- `EARLY` = nobody is together with Luna: NOT `K_TOG+`, NOT `G_TOG+`, NOT `V_TOG+`, NOT `A_LOVE`, and NOT (`S_ACT` and `S_KISS`). **Every row in this file carries `EARLY`** (STEP0 rows are a stricter version of it). These are the light "early days" talks; the jealousy talks of part one take over from the "together" steps.
- `NOT_G_ANY` = NOT `G_FLIRT` and NOT `G_TOG+` (Gore is not courting Luna; RV267, where Gore plays wingman).
- `ANY_EARLY_ROM` = `K_CRUSH` or `G_FLIRT` or `V_FLIRT` (at least one of the three has started).
- `LUNA_HORSE` = the player owns a horse: `Game.GetPlayersLastRiddenHorse() != None` and that horse is player-owned **[UNC: ownership check; fallback = any last-ridden horse]**.
- `REDCAP_REC` = `FA01RedcapRecruited (00AA02:FA01RedcapFollower.esp) == 1` (RV231 only mentions Redcap; he need not be in the party).
- `REMI_REC` = `HLIORemiRecruited (014C10:HLIORemi.esp) == 1` and Remi following (RV285, RV300 mention Scrap).
- `REMI_VAL_MET` = `HLIOValBanter (9BA4FD:HLIORemi.esp)` stage >= 10.
- `after:RVn` = that RV talk already played. Chains obey TRIGGERS.md section 8 (unblocked after 10 in-game days if the predecessor can never play).

Events (TRIGGERS.md section 4 unless noted): `E CAMP`, `E CAMP+NIGHT`, `E INN`, `E INN + BARD_PLAYING`, `E MORNING` (at a CAMP), `E RAIN`, `E SNOW`, `E WATER`, `E CAVE`, `E CRYPT`, `E DWEMER`, `E exterior`, `E CITY` (any hold capital), `E CITY:Solitude`, `E AFTERFIGHT`, `E AFTERFIGHT:bandit`, `E AFTERFIGHT:troll` (53 RIVALRY.md), `E STORE` = player in a location with `LocTypeStore 01CB86` (vanilla_gates.md B2), `E FARM`, `E exterior, IsCloudy` (RV267, clouds before rain).

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| RV201 | G K P | T | STEP0; after A1 |
| RV202 | V G P | E MORNING (at CAMP) | STEP0; after A3 |
| RV203 | K G P | E CRYPT | STEP0; after A1 |
| RV204 | V G P | E exterior (not in a settlement) | STEP0; after A3 |
| RV205 | G K | E AFTERFIGHT:bandit | STEP0; after A1 |
| RV206 | V K | E AFTERFIGHT | STEP0; after A2 |
| RV207 | V G | T | STEP0; LUNA_HORSE; after A3 |
| RV208 | V G P | E STORE | STEP0; after A3 |
| RV209 | K G P | E WATER | STEP0; after A1 |
| RV210 | K V | E CAMP | STEP0; after A2 |
| RV211 | K V P | E MORNING (at CAMP) | STEP0; after A2 |
| RV212 | V K P | T | STEP0; after A2 |
| RV213 | G V | E INN | STEP0; after A3 |
| RV214 | K G P | E RAIN | STEP0; after A1 |
| RV215 | V G K | E AFTERFIGHT | STEP0; after A1, A2, A3 |
| RV216 | V K G | T | STEP0; after A1, A2, A3 |
| RV217 | K G V | E CITY:Solitude | STEP0; after A1, A2, A3 |
| RV218 | G K P | T | STEP0; after A1 |
| RV219 | G V | T | STEP0; after A3 |
| RV220 | K G | E CAVE or CRYPT or DWEMER | STEP0; after A1 |
| RV221 | G K | E AFTERFIGHT | STEP0; after A1 |
| RV222 | G V P | T | STEP0; after A3 |
| RV223 | V K P | E AFTERFIGHT (exterior) | EARLY; after A2 |
| RV224 | V K | E exterior | EARLY; after A2 |
| RV225 | G V | T | EARLY; after A3 |
| RV226 | K V P | E INN (arrival) | EARLY; after A2 |
| RV227 | P G V | T | EARLY; after A3 |
| RV228 | V G | E CAMP | EARLY; after A3 |
| RV229 | G K | E AFTERFIGHT:troll | EARLY; after A1 |
| RV230 | V K P | E SNOW (exterior) | EARLY; after A2 |
| RV231 | V K | T | EARLY; REDCAP_REC; after A2 |
| RV232 | V G P | T | EARLY; after A3 |
| RV233 | G V K | E CAMP+NIGHT | EARLY; after A1, A2, A3; after:RV215, RV216 |
| RV234 | V K | T | K_CRUSH; EARLY; after A2 |
| RV235 | K G P | T | K_CRUSH; EARLY; after A1 |
| RV236 | G K | E AFTERFIGHT | K_CRUSH; EARLY; after A1 |
| RV237 | P K V | T | K_CRUSH; EARLY; after A2 |
| RV238 | G K | E FARM | K_CRUSH; EARLY; after A1 |
| RV239 | K X | T | K_CRUSH; EARLY; after C3 |
| RV240 | P G K | E CAMP | K_CRUSH; EARLY; after:RV239; after A1 |
| RV241 | V K | T | K_CRUSH; EARLY; after A2 |
| RV242 | P K | E exterior | K_CRUSH; EARLY |
| RV243 | V K | E AFTERFIGHT | K_CRUSH; EARLY; after A2 |
| RV244 | G K | T | K_CRUSH; EARLY; after A1 |
| RV245 | P K V | T | K_CRUSH; EARLY; after A2 |
| RV246 | K P G | E WATER (exterior) | K_CRUSH; EARLY; after A1 |
| RV247 | V K | E SNOW | K_CRUSH; EARLY; after A2 |
| RV248 | G K | T | K_CRUSH; EARLY; after A1 |
| RV249 | P G K | E INN + BARD_PLAYING | K_CRUSH; EARLY; after A1 |
| RV250 | K V | E MORNING | K_CRUSH; EARLY; after A2 |
| RV251 | V K | E CAMP+NIGHT | K_CRUSH; EARLY; after A2 |
| RV252 | G K | E CITY | K_CRUSH; EARLY; after A1 |
| RV253 | K I | T | K_CRUSH; EARLY; KI |
| RV254 | P K G | T | K_CRUSH; EARLY; after A1 |
| RV255 | V K | T | K_CRUSH; EARLY; after A2 |
| RV256 | G K | E CAMP+NIGHT | K_CRUSH; EARLY; after A1 |
| RV257 | P K | T | K_CRUSH; EARLY |
| RV258 | V K | T | K_CRUSH; EARLY; LUNA_HORSE; after A2 |
| RV259 | G K P | E CRYPT | K_CRUSH; EARLY; after A1 |
| RV260 | K P G | T | K_CRUSH; EARLY; after A1 |
| RV261 | V K | E CAMP | K_CRUSH; EARLY; after A2 |
| RV262 | V K | T | K_CRUSH; EARLY; after A2 |
| RV263 | P G K | E exterior | K_CRUSH; EARLY; after A1 |
| RV264 | V K | T | K_CRUSH; EARLY; after A2 |
| RV265 | G K | E CAMP+NIGHT | K_CRUSH; EARLY; after A1 |
| RV266 | G K | E AFTERFIGHT | K_CRUSH; EARLY; BRYNJAR; after A1 |
| RV267 | G K P | E exterior, IsCloudy | K_CRUSH; NOT_G_ANY; EARLY; after A1 |
| RV268 | K V | E INN + BARD_PLAYING | K_CRUSH; EARLY; after A2 |
| RV269 | G K | E CAMP or INN | G_FLIRT; EARLY; after A1 |
| RV270 | V G | E SNOW | G_FLIRT or V_FLIRT; EARLY; after A3 |
| RV271 | G V | T | V_FLIRT; EARLY; after A3 |
| RV272 | G V | T | G_FLIRT; EARLY; after A3 |
| RV273 | V P G | T | V_FLIRT; EARLY; after A3 |
| RV274 | V G | T | G_FLIRT; EARLY; after A3 |
| RV275 | V G | E exterior | G_FLIRT; EARLY; after A3 |
| RV276 | K V | T | K_CRUSH; V_FLIRT; EARLY; after A2 |
| RV277 | V P | T | V_FLIRT; EARLY; Kaidan and Gore both following and Free (they are named and "stand up straighter"); after A2, A3 |
| RV278 | R K | T | K_CRUSH; EARLY; after B1 |
| RV279 | R V | T | EARLY; after A1, A2, A3; REMI_VAL_MET |
| RV280 | X P | T | ANY_EARLY_ROM; EARLY |
| RV281 | I R | T | EARLY; after A1, A2, A3; after B6 |
| RV282 | L I | T | ANY_EARLY_ROM; EARLY; LI |
| RV283 | C G | T | EARLY; after R5; after A1 |
| RV284 | S P | T | K_CRUSH; EARLY; SERANA |
| RV285 | A K | T | K_CRUSH; EARLY; REMI_REC |
| RV286 | G R | T | G_FLIRT; EARLY |
| RV287 | V I | T | V_FLIRT or STEP0; EARLY; after I1 |
| RV288 | G X | T | G_FLIRT; EARLY; after X1 |
| RV289 | P R | T | ANY_EARLY_ROM; EARLY |
| RV290 | C K | E CAMP | K_CRUSH; EARLY; after R1 |
| RV291 | X R | T | EARLY; after A1, A2, A3; RX |
| RV292 | I K | E MORNING (at CAMP) | K_CRUSH; EARLY; KI |
| RV293 | V X | T | V_FLIRT or STEP0; EARLY; after X4 |
| RV294 | L K | T | K_CRUSH; EARLY; LK |
| RV295 | P I | E CAMP | K_CRUSH or G_FLIRT; EARLY |
| RV296 | X K | T | K_CRUSH; EARLY; after C3 |
| RV297 | C P | T | ANY_EARLY_ROM; EARLY; after R1 |
| RV298 | V L | T | V_FLIRT or STEP0; EARLY; after C1 |
| RV299 | R K | E INN+NIGHT or CAMP+NIGHT | K_CRUSH; EARLY; after B1 |
| RV300 | P K G | T | K_CRUSH or G_FLIRT; EARLY; REMI_REC; after:RV284 |

## Notes for the build
- Pacing: these share part one's rival cooldown (at most one RV talk per in-game day), so the early rivalry runs underneath the rest of the banter.
- Every row carries `EARLY`. Once Luna is together with anyone, the whole file goes quiet and part one's later steps take over.
- Every row with K also carries Kaidan's standard blocks (kaidan_block.md 2a). Nothing here touches his scripted romance beats (first date, first night, kiss, proposal, wedding); `K_CRUSH` rows stop at K04 50.
- Luna never notices Kaidan's crush in any `K_CRUSH` row (she reads it as a fever, a spider, a bounty, a sweetheart in Riverwood). She never flirts back and never picks anyone. Gore and Val flirting rows (Part 3) keep her lines neutral too.
- No "Dragonborn", no Brynjar except RV266 (`BRYNJAR`), no cult, no Fathis, no Jo-Lee.
- Topics avoided on purpose (already in 53 RIVALRY and batch 1): the cloak in the snow, the inn doorway, the potion for hooves, the map with the horker, moss versus stars, the bog, the burnt rabbit, the arm-wrestle for the pack, the flowers, the hat, the scars, the treaty, the betting pool and Redcap's info market, plus KL41 (Mysticism), KL94 (the stars) and Kaidan and "The Lusty Argonian Maid" (KL file).
- Luna speaks in 37 of 100 talks (37%).
