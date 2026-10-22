# 31 CIVIL WAR - trigger rows (prefix CW, 70 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\31 CIVIL WAR.txt`.
Sources: `research\triggers\vanilla_gates.md` (B1 faction gates, B3 silence), `TRIGGERS.md` sections 2-4, `triggers\20 DAWNGUARD.md` (Serana/Ashe Free rows), `triggers\12 BRUMA AND MOONPATH.md` (`GORE_TIES`), the bibles.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana and Ashe Free rows in `20 DAWNGUARD.md` section 1. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but the player must not be in dialogue).

## 1. Civil War silence (add to WorldQuiet; vanilla_gates B3)

No CW talk (and no other banter) while:
- `CWSiege (0954E1:Skyrim.esm)` running, or `CWSiegeObj (096E71)` running (all city battles, incl. Whiterun). [CONFIRMED FormIDs; UNC that CWSiege stops right after the battle - the AFTERFIGHT rows below wait for it to stop]
- `CWFortSiegeFort (083042)` running (fort battles).
- `CWFinale (0D1444)` running. vanilla_gates gives 300..499 for the death scenes; **use the whole running window** to keep the final battle silent. [UNC start of the scene range]
- `CW01A (0D517A)` or `CW01B (0E2D29)` stage 160..199 (oath scene). [CONFIRMED]
- `CW03 (0D661C)` at stage 20, 100 or 225 (Message to Whiterun scenes). [CONFIRMED]

## 2. Gate codes used in this file

Existing (TRIGGERS.md section 4): `CW_IMP` = CW01A 200 done; `CW_SONS` = CW01B 200 done; `HELGEN`; `GREYBEARDS`; `BRYNJAR`; `SERANA`; `K_CRUSH`; `STEP0`; `G_FLIRT`; `V_FLIRT`. From 12 BRUMA: `GORE_TIES`.

New:
- `CW_ANY` = CW_IMP or CW_SONS.
- `CW_NONE` = HELGEN and not CW_IMP and not CW_SONS (war under way, Luna hasn't picked).
- `CW_ON` = `GetQuestCompleted CWFinale (0D1444) == 0` (war not finished; present-tense talks). Also true if the player never touches the war; that is fine.
- `CW_CROWN_IMP` = `GetQuestCompleted CW02A (02D75C)`; `CW_CROWN_SONS` = `GetQuestCompleted CW02B (02610B)`; `CW_CROWN` = either. **[UNC: completion stage; vanilla_gates only confirms these FormIDs and stage 10 as the join alternative. If they complete only after the follow-on hand-off, use the "give the crown" stage instead]**
- `CW_MSG` = `GetQuestCompleted CW03 (0D661C)` (Message to Whiterun done). **[UNC: CW03 may hand straight into the siege; any stage after Balgruuf's answer works]**
- `CW_WR` = Battle for Whiterun won by Luna's side. **[UNC: vanilla tracks this in the CW script (`CWs` CW quest script) hold ownership. Candidates: (a) first completion of `CWSiege` with Whiterun as the siege city; (b) Sons: Vignar Gray-Mane in `JobJarlFaction`; Imp: CWSiege completed while CW_IMP. Pick one at build and keep it]**
- `CW_END` = `GetQuestCompleted CWFinale (0D1444)`. `CW_END_IMP` = CW_END and CW_IMP (Battle for Windhelm). `CW_END_SONS` = CW_END and CW_SONS (Battle for Solitude).
- `EMBASSY` = the Ulfric dossier found in the Thalmor Embassy (MQ201 "Diplomatic Immunity"). **[UNC: exact MQ201 stage for reading the Ulfric file; safe fallback = MQ201 completed]**

Places (`E LOC:<name>` = arrival or first time inside, once):
- `LOC:CastleDour` CastleDourLocation; `LOC:PalaceKings` WindhelmPalaceoftheKingsLocation; `LOC:BluePalace` SolitudeBluePalaceLocation; `LOC:TempleTalos` WindhelmTempleofTalosLocation; `LOC:GreyQuarter` Windhelm Grey Quarter (vanilla has no separate location; use player in the Gray Quarter cells / within 1500 units of New Gnisis Cornerclub door) ; `LOC:Cidhna` within 1500 units of the Cidhna Mine entrance in Markarth or in CidhnaMineLocation. **[UNC: all location FormIDs to look up at build]**
- `CITY:Solitude`, `CITY:Markarth` as TRIGGERS.md (arrival). `INN_WS` = LocTypeInn and current hold is Eastmarch or Haafingar (Candlehearth Hall / Winking Skeever). `BARDS_COLLEGE` existing.
- `MILCAMP` = within 2000 units of a Civil War camp (the CW camp locations: Imperial camps in the Pale/Rift/Reach/Hjaalmarch/Falkreath, Stormcloak camps likewise). **[UNC: no LocTypeMilitaryCamp keyword confirmed; use the CW camp Location records or their map markers]**
- `CWFORT` = in a `LocTypeMilitaryFort (0130E7)` location that has had a CWFortSiegeFort run there (controller remembers the fort's location when CWFortSiegeFort stops). **[UNC]**
- `CARAVAN` = within 1500 units of Ri'saad, Ma'dran or Ahkari (or their caravan members) outside a city. **[UNC base IDs]**
- `TALOS_SHRINE` = within 600 units of a Talos shrine activator (TempleBlessingTalos shrine base) outdoors. **[UNC base]**
- `GIANT` existing. `WIND` = exterior and `GetWindSpeed >= 0.6` **[UNC threshold; same as STORM without rain]**.

Fights (`E AFTERFIGHT:<type>`):
- `cwwhiterun` = CWSiege just stopped after the Whiterun battle (first CW_WR moment).
- `cwfort` = CWFortSiegeFort just stopped (won).
- `cwfinale` = CWFinale just completed (first moment it is not running).
- `cwpatrol` = last combat target in CWImperialFaction (02BF9A) or CWSonsFaction (02BF9B), and no CWSiege / CWFortSiegeFort running.
- `thalmorescort` = a Thalmor escort world encounter ended with the prisoner alive (Thalmor + bound prisoner WE). **[UNC: WE quest EditorID; fallback = AFTERFIGHT:Thalmor where a non-hostile bound NPC is within 1000 units]**

Other:
- `IMP_ARMOR` (optional, CW3) = player wearing a Legion cuirass. **[UNC: form list of Imperial cuirasses; if skipped, CW3 still works after CW_IMP]**

## 3. Per-talk table

### Part 1 - The Legion
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW1 | G K | T | CW_IMP |
| CW2 | L V | E LOC:CastleDour | CW_IMP; after C1 |
| CW3 | R P | T (or E CITY any) | CW_IMP; IMP_ARMOR optional [UNC] |
| CW4 | A K | T | CW_IMP |
| CW5 | G L P | T | CW_IMP; after L1 |
| CW6 | I G | T | CW_CROWN_IMP; after C2 |
| CW7 | X V | T | CW_MSG; CW_IMP; after X4 |
| CW8 | G K | T | CW_WR; CW_IMP; not CW_END |
| CW9 | K P | T | CW_IMP |
| CW10 | S R | T | CW_IMP; SERANA |
| CW11 | C L | T (exterior, not CITY, player moving) | CW_IMP; after R11 |
| CW12 | X I | T | CW_END_IMP; after X6 |
| CW13 | L G P | T | CW_END_IMP; after L1 |
| CW14 | K A | T | CW_END_IMP; after CW13 (Lucien "so happy") |

### Part 2 - The Stormcloaks
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW15 | C G | T | CW_SONS; after R5 |
| CW16 | V K | T | CW_SONS; after A2 |
| CW17 | G K P | E LOC:PalaceKings | CW_SONS; K_CRUSH |
| CW18 | L P | T | CW_SONS |
| CW19 | G A | T | CW_SONS |
| CW20 | X R P | T | CW_SONS; Remi/Xelzaz not fallen out (Free) |
| CW21 | I K | T | CW_CROWN_SONS |
| CW22 | V R | T | CW_MSG; CW_SONS; Remi-Val own intro done (HLIOValBanter stage 10) |
| CW23 | G K | T | CW_WR; CW_SONS; not CW_END |
| CW24 | R I | T | CW_WR; CW_SONS; after B6 |
| CW25 | I C | E LOC:TempleTalos | CW_SONS; after R13 |
| CW26 | L P | T | CW_SONS; GREYBEARDS |
| CW27 | L K P | T | CW_END_SONS |
| CW28 | G S | T | CW_END_SONS; SERANA |

### Part 3 - Either side
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW29 | V K P | T | CW_NONE; after A2 |
| CW30 | L P | T | CW_ON |
| CW31 | L A | T | CW_NONE |
| CW32 | K P | T | CW_ON |
| CW33 | G I | T | HELGEN; after C2 |
| CW34 | G V | T | CW_ANY; STEP0 or G_FLIRT or V_FLIRT; after A3 |
| CW35 | L G | E INN_WS | after L1 |
| CW36 | R P | E BARDS_COLLEGE | — |
| CW37 | L P | E CITY:Solitude | — |
| CW38 | A R | E leaving LOC:BluePalace after talking to Elisif (player was in dialogue with Elisif this visit) [UNC] | — |
| CW39 | X V | E LOC:GreyQuarter | after X4 |
| CW40 | R I | E CARAVAN | after B6 |
| CW41 | G X P | E CITY:Markarth | after X1 |
| CW42 | R V | E CITY:Markarth (second visit or later, so it does not race CW41/P5) | Remi-Val own intro done (HLIOValBanter stage 10) |
| CW43 | C K | E LOC:Cidhna | after R1 |
| CW44 | L K | T | EMBASSY [UNC]; Lucien-Kaidan intro done (Lucien's own scenes) |
| CW45 | G P | E AFTERFIGHT:thalmorescort | GORE_TIES [UNC] |
| CW46 | C S | T | SERANA; after DG8 |
| CW47 | R P | T | — |
| CW48 | K P | T | BRYNJAR [UNC] |
| CW49 | V G | E MILCAMP | after A3 |
| CW50 | X C | E MILCAMP | after R18 (Redcap-Xelzaz own apology done) |
| CW51 | L P | T | CW_CROWN |
| CW52 | S V | E CITY:Solitude | SERANA |
| CW53 | C G | E GIANT | after R5 |
| CW54 | G A | T | CW_ON |
| CW55 | G K | E WIND | after A1 |
| CW56 | A K P | T (first tick after CW_WR) | CW_WR |
| CW57 | I K | T | CW_END; Kaidan+Inigo intro done (KaiandInigo stage >= 10) |
| CW58 | L R | E CWFORT (arrival, not the battle itself) | after B10 |
| CW59 | R K P | T | after B1 |
| CW60 | G I | E TALOS_SHRINE | after C2 |
| CW61 | X P | T | CW_ON |
| CW62 | R V | T | Remi-Val own intro done (HLIOValBanter stage 10) |

### Part 4 - After the battle (barks; the normal 8 s post-combat delay, never during the battle)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| CW63 | K G | E AFTERFIGHT:cwwhiterun | CW_IMP |
| CW64 | G P | E AFTERFIGHT:cwwhiterun | CW_SONS |
| CW65 | R I | E AFTERFIGHT:cwfort | — |
| CW66 | C K | E AFTERFIGHT:cwfort | — |
| CW67 | A V | E AFTERFIGHT:cwfort | — |
| CW68 | X K | E AFTERFIGHT:cwfinale | CW_IMP |
| CW69 | L P | E AFTERFIGHT:cwfinale | CW_SONS |
| CW70 | K I | E AFTERFIGHT:cwpatrol | CW_ON |

## 4. Notes for the build
- Side talks: Part 1 rows all carry CW_IMP, Part 2 rows all carry CW_SONS. A player can only take the oath for one side, so the two parts never both play.
- CW8/CW23 (Whiterun aftermath, by side) and CW56 (the count, either side) may all be eligible after CW_WR; the 300 s cooldown spaces them. CW63/CW64 fire first as barks.
- CW12/CW13/CW14/CW57/CW68 (Legion win) and CW27/CW28/CW57/CW69 (Stormcloak win) play after the finale; the finale itself is silent (section 1).
- CW17 is Kaidan's crush beat: Luna misses the point (thinks he is glaring at the throne carving). Never fire it at K_TOG or later.
- CW34 is the Gore/Val "sizing up" rivalry beat; Luna has no line in it.
- CW38 needs Ashe following while Luna talked to Elisif; if the "talked to Elisif" check is too fiddly, fire on leaving the Blue Palace after the first visit. [UNC]
- CW45 mentions Gore's mother dying in a Thalmor raid: keep it behind GORE_TIES. It never mentions Jo-Lee.
- CW48 is behind BRYNJAR (Kaidan's Brynjar story).
- No line in this file says "Dragonborn". CW26 has Luna joke about shouting; it is gated GREYBEARDS, so she can shout.
- Lore used: Fort Hraggstad (Legion test), Serpent's Bluff ice wraith (Stormcloak test), Ulfric's axe (Message to Whiterun, Stormcloak side), Vignar Gray-Mane as Jarl after a Stormcloak Whiterun, Brunwulf Free-Winter after an Imperial Windhelm, Rikke dying in the Battle for Solitude, Borgas as the last wearer of the Jagged Crown, the Markarth Incident, the Concordat terms, the banned Burning of King Olaf, Age of Aggression / Age of Oppression. Check any of these against the live load order if a quest mod changes them.
- Existing coverage avoided: Q9/Q10 (joining), BR45 (Lucien/Kaidan Concordat argument), BR37 and MN97 (Lucien's mother at the Red Ring), LT5 (Inigo praying to Talos, "a man once"), P3 (Grey Quarter walls), P5 (Forsworn), CC Champions talks, the Remi/Xelzaz Elisif gossip.
