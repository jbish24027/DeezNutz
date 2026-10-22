# 44b IN THE FIGHT 2 - trigger rows (prefix CB, CB151-CB350, 200 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\44b IN THE FIGHT 2.txt`. Part 1 is `44 IN THE FIGHT.md` (CB1-CB150); everything there about lanes, enemy codes and moment conditions still applies, and this file only adds to it.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`, except the player-in-combat rule for COMBAT rows) and section 3 (`Free`, except `GetCombatState()==0` for COMBAT rows). Serana and Ashe Free() rows are in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check).
Every row also needs its pair's meets talk already played (TRIGGERS.md section 4, Chains); the Gates column names it the same way `44 IN THE FIGHT.md` does.

## Two lanes (same as part 1)

- **COMBAT rows: COMBAT (scene must not end on combat).** In-fight barks. Start them from the controller while the player IS in combat (first 3-20 s of a fight, or on the named moment). Their scenes must NOT carry the CombatEnd flag (keep DeathEnd and DialogueEnd), must bypass the player-in-combat quiet rule and the speakers' `GetCombatState()==0` test, and must keep every other quiet rule. **One bark per fight across 44 and 44b together.** A bark sets no 300 s cooldown and does not reset the 5-minute timer.
- **AFTERFIGHT rows.** Normal post-combat event: controller sees player combat end, waits 8 s, enemy type = last combat target.

COMBAT rows in this file: CB151-CB258, CB261, CB264, CB267-CB269, CB272, CB274-CB278, CB280-CB284, CB286, CB289, CB290, CB293, CB294, CB296.
AFTERFIGHT rows: CB259, CB260, CB262, CB263, CB265, CB266, CB270, CB271, CB273, CB279, CB285, CB287, CB288, CB291, CB292, CB295, CB297-CB350.

## New enemy codes (current target for COMBAT, last target for AFTERFIGHT)

All [UNC]: confirm each FormID / keyword at build. Where a code is a "boss" version of a part-1 code, the boss version wins when both match.
- `dragonpriest` DragonPriestRace (Skyrim.esm) incl. DLC2 dragon priests.
- `vampirelord` target race DLC1VampireBeastRace (00283A:Dawnguard.esm).
- `draugrboss` draugr target whose base name contains Overlord, Deathlord or Scourge, or that carries LocRefType Boss.
- `sprigganmatron` SprigganMatronRace (Skyrim.esm) and DLC2 Spriggan Earth Mother. "Sends her swarm" = she casts her insect-swarm spell; "calls an animal" = a hostile bear/wolf/sabre cat joins mid-fight.
- `frostgiant` frost giant base (DLC2 frost giant / any giant whose base name contains "Frost").
- `chaurushunter` DLC1ChaurusHunterRace (Dawnguard.esm).
- `falmershadow` Falmer whose base name contains Shadowmaster or Nightprowler. "Goes invisible" = target gains an Invisibility effect.
- `centurion` DwarvenCenturionRace. "Breathes steam" = target casts its steam breath.
- `dremoralord` DremoraRace with base name containing Markynaz, Valkynaz or Lord. "Someone summoned" = target is a commanded actor (GetCommandingActor / summon) of a hostile caster.
- `witch` HagravenRace, or a hostile in a witch/coven faction (vanilla Hagraven faction, Glenmoril.esm coven, Vigilant.esm witch factions). "In the cold" = exterior with SNOW or in a snowy region. **Never fire CB179-CB182 or CB317-CB318 inside Gore - Vigilant quest windows** (TRIGGERS.md section 3 Gore busy blocks).
- `briarheart` Forsworn with base name containing Briarheart.
- `justiciar` reuse part-1 CB17 code (Thalmor target named Justiciar).
- `banditchief` BanditFaction target carrying LocRefType Boss.
- `necromaster` necromancer target (part-1 code) that carries LocRefType Boss or base name containing Master/Adept-boss; "keeps raising the dead" = it casts Reanimate twice; "has a ward up" = target has a ward effect active.
- `wisp` WispRace / WispmotherRace (+ shades). "Splits into copies" = wispmother casts her clone spell.
- `icewraith` IceWraithRace.
- `horker` HorkerRace.
- `mudcrab` MudcrabRace with 3 or more hostile mudcrabs in this combat.
- `boss` any target with LocRefType Boss, or a Unique hostile actor, or a dragon.

## New moment conditions (for COMBAT rows unless the row says AFTERFIGHT)

All [UNC]; most need the 1-2 s combat poll part 1 already needs.
- `ambush` = in the first 5 s of combat, the first hostile that targets the player is behind her (heading angle > 120 degrees) and within 1500 units.
- `water` = player or one of the speakers `IsSwimming`, or PO3 IsActorInWater.
- `cliff` = exterior and player within 300 units of a drop of 600+ units. No vanilla check exists; use a ledge-marker list or a GetPositionZ probe, or ship these rows as rare. `highground` = more than half the hostiles are 300+ units above the player.
- `dark` = interior and player `GetLightLevel` < 35.
- `trap` = player or a speaker hit by a trap (OnHit source is a trap reference / TrapBase). Sub-kinds by source: `blade` (swinging blades), `dart`, `fire` (oil/flame).
- `spellmiss` = player fired a Destruction projectile and no hostile took damage from it within 1.5 s. `spellmiss-near-Redcap` = impact within 300 units of Redcap. `firemiss-outdoors` = Fire spell, exterior.
- `knockdown:X` = X is ragdolled/knocked down this fight (knock state, or `IsBleedingOut`).
- `block:X` = X took a melee hit from an enemy whose combat target is the player, while X is within 200 units of the player.
- `backtoback:X+Y` = X and Y within 200 units of each other, 3+ hostiles within 800.
- `fear:X` = X has an active Fear effect (MagicInfluenceFear keyword).
- `steal:X->Y` = an enemy Y damaged in the last 3 s is killed by X.
- `last` = exactly one hostile left in this combat.
- `retreat` = player below 35% health and moving away from the nearest hostile for 3 s, or player sprinting away from 3+ hostiles.
- `phase` = a `boss` target drops below 50% health this fight. `phase-second-wind` = it then heals or changes weapons/spells.
- AFTERFIGHT moment flags: the controller remembers which of the above happened during the fight (one bool each) so Part 5 rows can test them after the fight ends.
- `hardfight` = player or any speaker went below 25% health, or a follower bled out, during the fight (same as part 1 CB114).
- `master spell` / `big destruction spell` = as part 1 (`player casting a master or expert spell`).

## Gate codes

From TRIGGERS.md section 4: `SHOUT1`, `K_CRUSH`, `K_TOG+`, `K_ANY`, `G_ANY`, `V_ANY`, `NIGHT`, `SNOW`. From `20 DAWNGUARD.md` section 3: `SER` (Serana following), `SER_VAMP`, `DG_VALERICA`, `A_ANY`, `ASHE_REVEAL`. From `53 RIVALRY.md`: `S_ACT`. `ASHE` = Ashe following + `ASHE_HIRED` (`49 ASHE.md`). `REMIXEL_MADEUP` = `BPUFXelzazRemielFallingOut` completed (they fell out and made up), as used in `48 SERANA.md` / TRIGGERS.md section 3.

The running-joke sets in Part 3 play in order; each row's `after CBxx` gate does this. The kill count's season two needs part 1's last count talk (CB103).

## Table

### PART 1 - FIGHT STARTS, BY ENEMY  (54 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB151 | L P | E COMBAT:dragonpriest - COMBAT (scene must not end on combat) | — |
| CB152 | C K | E COMBAT:dragonpriest (target has a summon) - COMBAT (scene must not end on combat) | after R1 |
| CB153 | X V | E COMBAT:dragonpriest - COMBAT (scene must not end on combat) | after X4 |
| CB154 | S G | E COMBAT:dragonpriest - COMBAT (scene must not end on combat) | SER; Gore following |
| CB155 | S P | E COMBAT:vampirelord - COMBAT (scene must not end on combat) | SER |
| CB156 | C I | E COMBAT:vampirelord - COMBAT (scene must not end on combat) | after R13 |
| CB157 | K X | E COMBAT:vampirelord - COMBAT (scene must not end on combat) | after C3 |
| CB158 | G K | E COMBAT:draugrboss - COMBAT (scene must not end on combat) | after A1 |
| CB159 | L R | E COMBAT:draugrboss - COMBAT (scene must not end on combat) | after B10 |
| CB160 | V P | E COMBAT:draugrboss (target shouts) - COMBAT (scene must not end on combat) | SHOUT1 |
| CB161 | C G | E COMBAT:sprigganmatron (sends her swarm) - COMBAT (scene must not end on combat) | after R5 |
| CB162 | I P | E COMBAT:sprigganmatron (calls an animal) - COMBAT (scene must not end on combat) | — |
| CB163 | X S | E COMBAT:sprigganmatron - COMBAT (scene must not end on combat) | SER; Xelzaz following |
| CB164 | C K | E COMBAT:frostgiant - COMBAT (scene must not end on combat) | after R1 |
| CB165 | X G | E COMBAT:frostgiant - COMBAT (scene must not end on combat) | after X1 |
| CB166 | A P | E COMBAT:frostgiant - COMBAT (scene must not end on combat) | ASHE |
| CB167 | V G | E COMBAT:chaurushunter - COMBAT (scene must not end on combat) | after A3 |
| CB168 | R L | E COMBAT:chaurushunter - COMBAT (scene must not end on combat) | after B10 |
| CB169 | I K | E COMBAT:chaurushunter - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |
| CB170 | L I | E COMBAT:falmershadow (goes invisible) - COMBAT (scene must not end on combat) | Lucien-Inigo intro done (JRLucienInigo) |
| CB171 | R P | E COMBAT:falmershadow (goes invisible) - COMBAT (scene must not end on combat) | — |
| CB172 | C X | E COMBAT:falmershadow - COMBAT (scene must not end on combat) | after R18 |
| CB173 | K X | E COMBAT:centurion (breathes steam) - COMBAT (scene must not end on combat) | after C3 |
| CB174 | R G | E COMBAT:centurion - COMBAT (scene must not end on combat) | Remi-Gore intro done (HLIOGoreBanter) |
| CB175 | V P | E COMBAT:centurion - COMBAT (scene must not end on combat) | — |
| CB176 | I L | E COMBAT:dremoralord - COMBAT (scene must not end on combat) | Lucien-Inigo intro done |
| CB177 | X P | E COMBAT:dremoralord (someone summoned it) - COMBAT (scene must not end on combat) | — |
| CB178 | G K | E COMBAT:dremoralord - COMBAT (scene must not end on combat) | after A1 |
| CB179 | I C | E COMBAT:witch - COMBAT (scene must not end on combat) | after R13; not in a Gore - Vigilant window |
| CB180 | R V | E COMBAT:witch (in the cold) - COMBAT (scene must not end on combat) | Val-Remi intro done (HLIOValBanter 10) |
| CB181 | P C | E COMBAT:witch (2+ witch/hagraven hostiles) - COMBAT (scene must not end on combat) | — |
| CB182 | K S | E COMBAT:witch (HagravenRace target) - COMBAT (scene must not end on combat) | SER; SER_VAMP; Kaidan following |
| CB183 | G R | E COMBAT:briarheart - COMBAT (scene must not end on combat) | Remi-Gore intro done |
| CB184 | K P | E COMBAT:briarheart - COMBAT (scene must not end on combat) | — |
| CB185 | A V | E COMBAT:briarheart - COMBAT (scene must not end on combat) | ASHE; ASHE_REVEAL; Val following |
| CB186 | G K | E COMBAT:justiciar - COMBAT (scene must not end on combat) | after A1 |
| CB187 | V L | E COMBAT:justiciar - COMBAT (scene must not end on combat) | after C1 |
| CB188 | X P | E COMBAT:justiciar - COMBAT (scene must not end on combat) | — |
| CB189 | G V | E COMBAT:banditchief - COMBAT (scene must not end on combat) | after A3 |
| CB190 | R P | E COMBAT:banditchief - COMBAT (scene must not end on combat) | — |
| CB191 | G C | E COMBAT:banditchief - COMBAT (scene must not end on combat) | after R5 |
| CB192 | R X | E COMBAT:necromaster (keeps raising the dead) - COMBAT (scene must not end on combat) | Remi and Xelzaz not fallen out (TRIGGERS.md section 3) |
| CB193 | L P | E COMBAT:necromaster (has a ward up) - COMBAT (scene must not end on combat) | — |
| CB194 | S G | E COMBAT:necromaster - COMBAT (scene must not end on combat) | SER; DG_VALERICA; Gore following |
| CB195 | K I | E COMBAT:wisp (wispmother splits into copies) - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |
| CB196 | C L | E COMBAT:wisp - COMBAT (scene must not end on combat) | after R11 |
| CB197 | V P | E COMBAT:wisp (WispmotherRace target) - COMBAT (scene must not end on combat) | — |
| CB198 | C K | E COMBAT:icewraith - COMBAT (scene must not end on combat) | after R1 |
| CB199 | R I | E COMBAT:icewraith - COMBAT (scene must not end on combat) | after B6 |
| CB200 | G P | E COMBAT:icewraith - COMBAT (scene must not end on combat) | — |
| CB201 | K P | E COMBAT:horker - COMBAT (scene must not end on combat) | — |
| CB202 | G K | E COMBAT:horker - COMBAT (scene must not end on combat) | after A1 |
| CB203 | C K | E COMBAT:horker - COMBAT (scene must not end on combat) | after R1 |
| CB204 | L X | E COMBAT:mudcrab - COMBAT (scene must not end on combat) | Xelzaz-Lucien intro done (BPUFXelzazAndLucienInteractions) |

### PART 2 - IN THE THICK OF IT  (54 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB205 | K V | E COMBAT:any (ambush) - COMBAT (scene must not end on combat) | after A2 |
| CB206 | I P | E COMBAT:any (ambush) - COMBAT (scene must not end on combat) | — |
| CB207 | G I | E COMBAT:any (ambush) - COMBAT (scene must not end on combat) | after C2 |
| CB208 | A L | E COMBAT:any (ambush) - COMBAT (scene must not end on combat) | ASHE; Lucien following |
| CB209 | G R | E COMBAT:any (water) - COMBAT (scene must not end on combat) | Remi-Gore intro done |
| CB210 | X P | E COMBAT:any (water) - COMBAT (scene must not end on combat) | — |
| CB211 | V K | E COMBAT:any (water) - COMBAT (scene must not end on combat) | after A2 |
| CB212 | I C | E COMBAT:any (water) - COMBAT (scene must not end on combat) | after R13 |
| CB213 | L K | E COMBAT:any (cliff) - COMBAT (scene must not end on combat) | Lucien-Kaidan intro done (JRLucienFollowerKaidanScene1) |
| CB214 | G P | E COMBAT:any (cliff) - COMBAT (scene must not end on combat) | — |
| CB215 | A V | E COMBAT:any (highground) - COMBAT (scene must not end on combat) | ASHE; ASHE_REVEAL; Val following |
| CB216 | K P | E COMBAT:any (dark) - COMBAT (scene must not end on combat) | — |
| CB217 | C R | E COMBAT:any (dark) - COMBAT (scene must not end on combat) | Remi-Redcap intro done (Redcap's Remi scenes) |
| CB218 | I L | E COMBAT:any (dark) - COMBAT (scene must not end on combat) | Lucien-Inigo intro done |
| CB219 | G S | E COMBAT:any (dark) - COMBAT (scene must not end on combat) | SER; SER_VAMP; Gore following |
| CB220 | K R | E COMBAT:any (trap, set off by Remi or anyone) - COMBAT (scene must not end on combat) | after B1 |
| CB221 | V P | E COMBAT:any (trap: blade) - COMBAT (scene must not end on combat) | — |
| CB222 | L G | E COMBAT:any (trap: dart hits Lucien) - COMBAT (scene must not end on combat) | after L1 |
| CB223 | C X | E COMBAT:any (trap: fire) - COMBAT (scene must not end on combat) | after R18 |
| CB224 | P K | E COMBAT:any (spellmiss) - COMBAT (scene must not end on combat) | K_CRUSH |
| CB225 | G P | E COMBAT:any (firemiss-outdoors) - COMBAT (scene must not end on combat) | — |
| CB226 | V L | E COMBAT:any (spellmiss) - COMBAT (scene must not end on combat) | after C1 |
| CB227 | C P | E COMBAT:any (spellmiss-near-Redcap) - COMBAT (scene must not end on combat) | — |
| CB228 | G K | E COMBAT:any (knockdown:Gore) - COMBAT (scene must not end on combat) | after A1 |
| CB229 | R V | E COMBAT:any (knockdown:Val) - COMBAT (scene must not end on combat) | Val-Remi intro done |
| CB230 | L A | E COMBAT:any (knockdown:Lucien) - COMBAT (scene must not end on combat) | ASHE; Lucien following |
| CB231 | K I | E COMBAT:any (knockdown:Inigo) - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |
| CB232 | G P | E COMBAT:any (block:Gore) - COMBAT (scene must not end on combat) | G_ANY |
| CB233 | K P | E COMBAT:any (block:Kaidan) - COMBAT (scene must not end on combat) | K_CRUSH |
| CB234 | V K | E COMBAT:any (block:Val) - COMBAT (scene must not end on combat) | K_ANY; V_ANY; after A2 |
| CB235 | S P | E COMBAT:any (block:Serana) - COMBAT (scene must not end on combat) | S_ACT; SER_VAMP |
| CB236 | A G | E COMBAT:any (block:Ashe) - COMBAT (scene must not end on combat) | A_ANY; G_ANY |
| CB237 | K G | E COMBAT:any (backtoback:Kaidan+Gore) - COMBAT (scene must not end on combat) | after A1 |
| CB238 | V R | E COMBAT:any (backtoback:Val+Remi) - COMBAT (scene must not end on combat) | Val-Remi intro done |
| CB239 | I X | E COMBAT:any (backtoback:Inigo+Xelzaz) - COMBAT (scene must not end on combat) | after X6 |
| CB240 | L P | E COMBAT:any (backtoback:Lucien+player) - COMBAT (scene must not end on combat) | — |
| CB241 | R G | E COMBAT:any (fear:Remi) - COMBAT (scene must not end on combat) | Remi-Gore intro done |
| CB242 | L I | E COMBAT:any (fear:Lucien) - COMBAT (scene must not end on combat) | Lucien-Inigo intro done |
| CB243 | K P | E COMBAT:any (fear:Kaidan) - COMBAT (scene must not end on combat) | — |
| CB244 | V C | E COMBAT:any (fear:Redcap) - COMBAT (scene must not end on combat) | after R8 |
| CB245 | G C | E COMBAT:any (steal:Redcap->Gore's target) - COMBAT (scene must not end on combat) | after R5 |
| CB246 | R V | E COMBAT:any (steal:Val->Remi's target) - COMBAT (scene must not end on combat) | Val-Remi intro done |
| CB247 | I K | E COMBAT:spider (steal:Kaidan->Inigo's target) - COMBAT (scene must not end on combat) | KaiandInigo stage >= 10 |
| CB248 | S P | E COMBAT:any (steal:player->Serana's target) - COMBAT (scene must not end on combat) | SER |
| CB249 | V X | E COMBAT:any (last) - COMBAT (scene must not end on combat) | after X4 |
| CB250 | I C P | E COMBAT:any (last) - COMBAT (scene must not end on combat) | after R13 |
| CB251 | L K | E COMBAT:any (last) - COMBAT (scene must not end on combat) | Lucien-Kaidan intro done |
| CB252 | P K | E COMBAT:any (retreat) - COMBAT (scene must not end on combat) | — |
| CB253 | A G | E COMBAT:any (retreat) - COMBAT (scene must not end on combat) | ASHE; Gore following |
| CB254 | L V | E COMBAT:any (retreat) - COMBAT (scene must not end on combat) | after C1 |
| CB255 | G I | E COMBAT:boss (phase-second-wind) - COMBAT (scene must not end on combat) | after C2 |
| CB256 | R P | E COMBAT:boss (phase) - COMBAT (scene must not end on combat) | — |
| CB257 | K V | E COMBAT:boss (phase-second-wind) - COMBAT (scene must not end on combat) | after A2 |
| CB258 | A P | E COMBAT:boss (phase) - COMBAT (scene must not end on combat) | ASHE |

### PART 3 - RUNNING JOKES  (40 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB259 | G K | E AFTERFIGHT | after CB103 |
| CB260 | L G K | E AFTERFIGHT | after CB259; after L1; Lucien-Kaidan intro done |
| CB261 | G K | E COMBAT:boss - COMBAT (scene must not end on combat) | after CB260 |
| CB262 | A G K | E AFTERFIGHT | after CB260; ASHE |
| CB263 | P G K | E AFTERFIGHT (player cast a master or expert spell this fight) | after CB261 |
| CB264 | K G | E COMBAT:any (Kaidan and Gore both hit the same target within 1 s) [UNC] - COMBAT (scene must not end on combat) | after CB261 |
| CB265 | C G K | E AFTERFIGHT | after CB263; after R1; after R5 |
| CB266 | G K | E AFTERFIGHT (hardfight) | after CB265 |
| CB267 | V R | E COMBAT:any - COMBAT (scene must not end on combat) | after CB74; Val-Remi intro done |
| CB268 | V P | E COMBAT:any - COMBAT (scene must not end on combat) | after CB74; V_ANY |
| CB269 | L V | E COMBAT:any - COMBAT (scene must not end on combat) | after CB74; after C1 |
| CB270 | V I | E AFTERFIGHT:troll | after CB74; after I1 |
| CB271 | K V | E AFTERFIGHT | after CB267; after A2 |
| CB272 | C V | E COMBAT:any - COMBAT (scene must not end on combat) | after CB74; after R8 |
| CB273 | A V | E AFTERFIGHT | after CB74; ASHE; Val following |
| CB274 | C G | E COMBAT:any - COMBAT (scene must not end on combat) | after R5 |
| CB275 | C K | E COMBAT:any - COMBAT (scene must not end on combat) | after CB274; after R1 |
| CB276 | C I | E COMBAT:any - COMBAT (scene must not end on combat) | after CB275; after R13 |
| CB277 | C P | E COMBAT:any - COMBAT (scene must not end on combat) | after CB276 |
| CB278 | C L | E COMBAT:any - COMBAT (scene must not end on combat) | after CB277; after R11 |
| CB279 | G C | E AFTERFIGHT | after CB278 |
| CB280 | X C | E COMBAT:any - COMBAT (scene must not end on combat) | after CB279; after R18 |
| CB281 | L K | E COMBAT:any (Lucien casts a fire spell) [UNC] - COMBAT (scene must not end on combat) | Lucien-Kaidan intro done |
| CB282 | L P | E COMBAT:any (Lucien casts a frost spell) [UNC] - COMBAT (scene must not end on combat) | after CB281 |
| CB283 | L I | E COMBAT:draugr - COMBAT (scene must not end on combat) | after CB281; Lucien-Inigo intro done |
| CB284 | L G | E COMBAT:any (Gore below half health and Lucien casting a heal) [UNC] - COMBAT (scene must not end on combat) | after CB281; after L1 |
| CB285 | X L P | E AFTERFIGHT | after CB281; Xelzaz-Lucien intro done |
| CB286 | L P | E COMBAT:any - COMBAT (scene must not end on combat) | after CB282 |
| CB287 | A G | E AFTERFIGHT | ASHE; Gore following |
| CB288 | A K | E AFTERFIGHT | after CB287; ASHE; Kaidan following |
| CB289 | A P | E COMBAT:any (player casting a master spell) [UNC] - COMBAT (scene must not end on combat) | after CB287; ASHE |
| CB290 | A V | E COMBAT:any (2+ hostile archers; Val hit by an arrow) [UNC] - COMBAT (scene must not end on combat) | after CB287; ASHE; Val following |
| CB291 | A I | E AFTERFIGHT | after CB287; ASHE; Inigo following |
| CB292 | C A | E AFTERFIGHT | after CB287; ASHE; Redcap following |
| CB293 | S G | E COMBAT:bandit - COMBAT (scene must not end on combat) | SER; SER_VAMP; Gore following |
| CB294 | K S | E COMBAT:thalmor - COMBAT (scene must not end on combat) | SER; SER_VAMP; Kaidan following |
| CB295 | P S | E AFTERFIGHT | SER; SER_VAMP |
| CB296 | L S | E COMBAT:any (Serana casting Vampiric Drain on a hostile) [UNC] - COMBAT (scene must not end on combat) | SER; SER_VAMP; Lucien following |
| CB297 | R S | E AFTERFIGHT | SER; SER_VAMP; Remi following |
| CB298 | I S | E AFTERFIGHT (combat lasted 60 s or more) | after CB293; SER; SER_VAMP; Inigo following |

### PART 4 - AFTER THE FIGHT, BY ENEMY  (36 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB299 | R P | E AFTERFIGHT:dragonpriest | Remi following |
| CB300 | L S | E AFTERFIGHT:dragonpriest | SER; Lucien following |
| CB301 | S P | E AFTERFIGHT:vampirelord | SER; SER_VAMP |
| CB302 | X K | E AFTERFIGHT:vampirelord (Kaidan was hit) | after C3 |
| CB303 | L G | E AFTERFIGHT:draugrboss | after L1 |
| CB304 | K P | E AFTERFIGHT:draugrboss | — |
| CB305 | C R | E AFTERFIGHT:sprigganmatron | Remi-Redcap intro done |
| CB306 | X P | E AFTERFIGHT:sprigganmatron | — |
| CB307 | I G | E AFTERFIGHT:frostgiant | after C2 |
| CB308 | L P | E AFTERFIGHT:frostgiant | — |
| CB309 | V P | E AFTERFIGHT:chaurushunter | — |
| CB310 | X R | E AFTERFIGHT:chaurushunter | Remi and Xelzaz not fallen out |
| CB311 | L I | E AFTERFIGHT:falmershadow | Lucien-Inigo intro done |
| CB312 | K P | E AFTERFIGHT:falmershadow | — |
| CB313 | V R | E AFTERFIGHT:centurion | Val-Remi intro done |
| CB314 | K P | E AFTERFIGHT:centurion (Kaidan below half health during the fight) | — |
| CB315 | G X | E AFTERFIGHT:dremoralord | after X1 |
| CB316 | L P | E AFTERFIGHT:dremoralord | — |
| CB317 | C K | E AFTERFIGHT:witch (HagravenRace target) | after R1; not in a Gore - Vigilant window |
| CB318 | R P | E AFTERFIGHT:witch | after CB180 |
| CB319 | G P | E AFTERFIGHT:briarheart | — |
| CB320 | I K | E AFTERFIGHT:forsworn (a briarheart died this fight) | KaiandInigo stage >= 10 |
| CB321 | V P | E AFTERFIGHT:justiciar | — |
| CB322 | G K | E AFTERFIGHT:justiciar | after A1; after CB186 |
| CB323 | R P | E AFTERFIGHT:banditchief | after CB190 |
| CB324 | G V | E AFTERFIGHT:banditchief | after A3 |
| CB325 | X R | E AFTERFIGHT:necromaster | REMIXEL_MADEUP |
| CB326 | I P | E AFTERFIGHT:necromaster | — |
| CB327 | R G | E AFTERFIGHT:wisp | Remi-Gore intro done |
| CB328 | L S | E AFTERFIGHT:wisp (WispmotherRace) | SER; Lucien following |
| CB329 | R K | E AFTERFIGHT:icewraith | after B1 |
| CB330 | V P | E AFTERFIGHT:icewraith (2+ ice wraiths this fight) | — |
| CB331 | K P | E AFTERFIGHT:horker | — |
| CB332 | G K | E AFTERFIGHT:horker | after A1; after CB331 |
| CB333 | L P | E AFTERFIGHT:mudcrab | — |
| CB334 | I R | E AFTERFIGHT:mudcrab | after B6 |

### PART 5 - AFTER THE FIGHT, WHAT HAPPENED IN IT  (16 talks)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CB335 | K P | E AFTERFIGHT (ambush happened) | — |
| CB336 | G I | E AFTERFIGHT (water happened) | after C2 |
| CB337 | L P | E AFTERFIGHT (cliff happened) | — |
| CB338 | R K | E AFTERFIGHT (trap happened) | after CB220 |
| CB339 | X P | E AFTERFIGHT (firemiss-outdoors happened) | — |
| CB340 | R V | E AFTERFIGHT (knockdown:Val happened) | after CB229 |
| CB341 | P K | E AFTERFIGHT (block:Kaidan happened) | K_TOG+ |
| CB342 | G V | E AFTERFIGHT (block:Val happened) | G_ANY; V_ANY; after A3 |
| CB343 | I X | E AFTERFIGHT (backtoback:Inigo+Xelzaz happened) | after CB239 |
| CB344 | L I | E AFTERFIGHT (fear:Lucien happened) | after CB242 |
| CB345 | G C | E AFTERFIGHT | after CB245 (next fight after it, not the same one) |
| CB346 | K P | E AFTERFIGHT (last happened and that enemy survived 20 s or more alone) [UNC] | after CB251 |
| CB347 | A P | E AFTERFIGHT (retreat happened) | ASHE; Gore following |
| CB348 | G P | E AFTERFIGHT (retreat happened) | — |
| CB349 | V A | E AFTERFIGHT (phase-second-wind happened) | after CB258; ASHE; Val following |
| CB350 | I K P | E AFTERFIGHT (hardfight) | KaiandInigo stage >= 10; not CB114 or K19 in the same session |
