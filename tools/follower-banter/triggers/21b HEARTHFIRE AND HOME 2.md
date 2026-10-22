# 21b HEARTHFIRE AND HOME 2 - trigger rows (prefix HF, HF101-HF180, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\21b HEARTHFIRE AND HOME 2.txt`
Part one and its gate codes: `triggers\21 HEARTHFIRE AND HOME.md` (all its gate codes apply here unchanged: `HOUSE`, `HF_AT`, `HF_LAKE/WIND/HELJ`, `HF_SMALL`, `HF_HALL`, `HF_CELLAR`, `HF_W:<wing>`, `HF_DONE`, `HF_BUILDING`, `HF_STEWARD`, `HF_BARD`, `HF_KID`, `KID_NEAR`, `KID_AWAY`, `KID:<name>`, `HF_PET:<type>`, `GRELOD_DEAD`, `SER`, `SER_VAMP`, `ASHE_REVEAL`, `K_MAR`, `KS`). Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`); Serana / Ashe Free rows are in `triggers\20 DAWNGUARD.md` section 1.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe. `+Luna` = Luna (player, Eleonora voice) has lines; she is never a gate.
Type: T = timer, E = event. **[U]** = unconfirmed, verify at build.

## 1. New gate codes (this file)

**Building**
- `HF_TABLE` = player within 600 units of the plot's drafting table. `HF_ANVIL`, `HF_QUARRY`, `HF_GRIND`, `HF_GARDEN` = same, for the plot's anvil / stone quarry / grindstone / garden patch. [U the furniture refs per plot]
- `HF_LOGS` = the player has bought logs from the plot's lumber mill since the last HF_AT visit (mill purchase via `BYOHHouseBuilding` or the mill owner's vendor topic). [U; fallback: HF_BUILDING and HF_SMALL not yet done]
- `HF_GLASS` = player carries Glass (`BYOHHouseGlass` misc item, HearthFires.esm) while HF_BUILDING. [U item EditorID]
- `HF_PLOT2` = event: first time HF_BUILDING at a second plot (the player owns two plot quests at stage 10+ and the current one has no `Room01` yet).
- `HF_SMALL_NIGHT` = HF_SMALL and the player has slept in that plot's small house once (`OnSleepStop` while HF_AT int). [U; fallback `after:HF3`]
- `HF_MILL` = Heljarchen grain mill built and player within 1500 units of it. [U which global; part one listed the mill as Heljarchen's exterior addition from memory]
- `HF_STABLE` = the plot's stable built. `HF_CARRIAGE` = steward has hired a carriage driver at that plot. [U globals]
- `HF_ALL3_DONE` = HF_DONE true at all three plots. [U]

**Household**
- `HF_MANNEQUIN` = HF_W:ARMORY (mannequins placed). `HF_W:TROPHY`, `HF_W:ALCHEMY`, `HF_W:KITCHEN`, `HF_W:GREENHOUSE`, `HF_W:BEDROOMS`, `HF_W:LIBRARY` as part one.
- `SMALLHOURS` = hour 2..4. `QUIET_PM` = hour 13..16 and no combat in the last game hour.
- `HOUSE_STAY3` = HOUSE_LEAVE after the party has been inside the same HOUSE location for 3+ game days (controller float `FB_HouseEnterDay`). [U, new global]
- `HURT_HOME` = arrival in a HOUSE with player health below 40%.
- `WEDDING_1Y` = K_MAR and 365+ game days since K04 reached 100 (controller stores `FB_KMarDay` when K_MAR first goes true). [U, new global]
- `GORE_READS` as `15b MISSIVES AND NPCS 2.md` (HLIOGoreReading >= 1).

**Children** (all from part one; new ones)
- `HF_KID_30` = 30+ game days since HF_KID first became true (controller float). [U]
- `HF_PET:<mudcrab|dog|fox|skeever>` = that pet bought for a child (Hearthfire child pet list; same detection as part one's `HF_PET:rabbit`). [U]
- `KID:Lucia` = Lucia (Whiterun) adopted. [U ref]
- `KID_ASKED_GOLD` = a child has used the "Can I have some gold?" request once. [U; fallback HF_KID]

**Other**
- `DG_CAIRN` as `20 DAWNGUARD.md` (DLC1VQ05 completed).
- `SEASON:autumn any` as `51 SEASONS WEATHER TIME MORE.md`.
- `LUC_ADMIT`, `RC_MANOS`, `SER_VAMP` as TRIGGERS.md / part one.
- `STORM` as TRIGGERS.md section 4, with `SNOW`.

## 2. Per-talk table

### Part J - The second build
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF101 | V L | E near HF_TABLE | HF_BUILDING; KS |
| HF102 | R G | E HF_AT after HF_LOGS | HF_BUILDING; KS |
| HF103 | C X | E near HF_QUARRY | HF_BUILDING; after:HF10 (woodbox) preferred; KS |
| HF104 | I +Luna | T | HF_AT ext; HF_BUILDING; KS |
| HF105 | R K | E near HF_ANVIL | HF_BUILDING; KS |
| HF106 | S G | E RAIN at HF_AT ext | HF_BUILDING; SER; after:HF9; KS |
| HF107 | L X | T | HF_AT; HF_GLASS; after:HF15 (windows are optimism); KS |
| HF108 | G R | E near HF_TABLE | HF_BUILDING; GORE_READS; not KID_NEAR |
| HF109 | K +Luna | T | HF_AT; HF_SMALL_NIGHT; KS |
| HF110 | V X | E NIGHT at HF_AT ext | HF_BUILDING; KS |
| HF111 | I K +Luna | E HF_PLOT2 | say-once; KS |
| HF112 | L A | T | HF_LAKE; HF_BUILDING; KS |

### Part K - The new rooms
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF113 | R K | E near HF_MILL | HF_HELJ; KS |
| HF114 | L S | E NIGHT at HF_AT int | HF_W:ARMORY; SER; after:HF36 (fog) preferred; KS |
| HF115 | I V | T | HF_AT int; HF_W:TROPHY; KS |
| HF116 | X +Luna | T | HF_AT int; HF_W:ALCHEMY; KS |
| HF117 | G C | T | HF_AT int; HF_W:KITCHEN; after:HF16; KS |
| HF118 | R I | T | HF_AT; HF_W:GREENHOUSE; KS |
| HF119 | V L | T | HF_AT ext; HF_STABLE; LUC_ADMIT; after:HF55 preferred; KS |
| HF120 | S K | E near HF_GRIND | SER; KS |
| HF121 | C A | E near HF_GARDEN | HF_AT ext; KS |

### Part L - Snow, marsh and moonlight
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF122 | K R | E SNOW at HF_HELJ ext | KS |
| HF123 | V S | E SNOW at HF_HELJ ext | SER; DG_CAIRN; KS |
| HF124 | L +Luna | E CLEARNIGHT at HF_LAKE ext | KS |
| HF125 | I R | E PREDAWN/MORNING (hour 5..7) at HF_LAKE ext | KS |
| HF126 | L X | E WATER at HF_WIND ext | KS |
| HF127 | G V | T | HF_LAKE; HF_CARRIAGE; not KID_NEAR |

### Part M - Evenings at home
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF128 | X R | T | HF_AT int; HF_CELLAR; after:HF13; KS |
| HF129 | G X | T | HOUSE; hour >= 18; after:HF52; not KID_NEAR |
| HF130 | K V | T | HOUSE; hour >= 18; KS |
| HF131 | X C | E HOUSE entered within 2 h after RAIN stopped | RC_MANOS (Bigpig); KS |
| HF132 | L +Luna | T | HOUSE; KS |
| HF133 | L V | T | HF_AT int; HF_BARD; after:HF55 (lunch money) preferred; KS |
| HF134 | C I | E NIGHT in HOUSE | KS |
| HF135 | A K | E RAIN while in HF_AT int | after:HF6; KS |
| HF136 | S A | E SMALLHOURS in HOUSE | SER; ASHE_REVEAL; player awake (not sleeping/waiting); KS |
| HF137 | S +Luna | E NIGHT at HF_AT int | HF_W:LIBRARY; SER; KS |
| HF138 | I +Luna | T | HOUSE; KS |
| HF139 | K G V | T | HOUSE; hour >= 18; KS |
| HF140 | R S | E MORNING at HOUSE ext or HF_AT ext, IsPleasant | SER; KS |
| HF141 | K R | E MORNING in HOUSE | KS |
| HF142 | V C | T | HOUSE; after:HF40; KS |
| HF143 | G +Luna | T | HOUSE; QUIET_PM; GORE_READS; after:HF32; KS |

### Part N - The little ones, again (Kaidan is in none of these)
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF144 | G C | T | HOUSE; HF_PET:mudcrab; after:HF24; KS |
| HF145 | C +Luna | T | HOUSE; HF_PET:dog; KS |
| HF146 | I S | T | HOUSE; HF_PET:fox; SER; SER_VAMP; KS |
| HF147 | R X | T | HOUSE; HF_PET:skeever; KS |
| HF148 | L R | T | HOUSE; KID_NEAR; KS |
| HF149 | V L | T | HOUSE; KID_NEAR; after:HF79; after:HF55 preferred; KS |
| HF150 | A +Luna | T | HOUSE; HF_KID; KID_ASKED_GOLD; after:HF58 preferred; KS |
| HF151 | G I | T | HOUSE ext or HF_AT ext; KID_NEAR; KS |
| HF152 | X R | T | HOUSE; KID_NEAR; after:HF43 (Tirdas rota); KS |
| HF153 | C L | E NIGHT in HOUSE | KID_NEAR; after:HF69; KS |
| HF154 | S +Luna | E MORNING in HOUSE | HF_KID; KID_AWAY; SER; SER_VAMP |
| HF155 | A R | T | HOUSE; KID_NEAR; ASHE_REVEAL; KS |
| HF156 | L +Luna | T | HOUSE; KID:Honorhall; GRELOD_DEAD; after:HF69 preferred; KS |
| HF157 | R G | T | HOUSE; KID:Lucia; after:NP35 (Remi's coin for Lucia) preferred; KS |
| HF158 | X +Luna | T | HOUSE; KID_NEAR; KS |
| HF159 | G R +Luna | T | HOUSE; HF_KID_30; KID_NEAR; say-once; KS |
| HF160 | I +Luna | T | HOUSE; KID_NEAR; KS |
| HF161 | V G | T | HOUSE; HF_KID; HF_BARD or HF_STEWARD; KID_AWAY |

### Part O - Married life, round two (K_MAR; no children, no nursery, no "our family")
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF162 | V +Luna | T | K_MAR; WEDDING_1Y; HOUSE; say-once; after:HF89 (humming) preferred; KS |
| HF163 | R +Luna | T | K_MAR; HOUSE; KS |
| HF164 | K +Luna | T | K_MAR; HOUSE; after:HF86 preferred; KS |
| HF165 | X K | T | K_MAR; HOUSE; KS |
| HF166 | L K | E MORNING in HOUSE | K_MAR; KS |
| HF167 | I +Luna | E MORNING in HOUSE | K_MAR; KS |
| HF168 | R V | E MORNING in HOUSE | K_MAR; KS |
| HF169 | C L | T | K_MAR; HOUSE; after:HF89 preferred; KS |
| HF170 | L S | T | K_MAR; HF_AT int; HF_BARD; hour >= 18; SER; not KID_NEAR |
| HF171 | G +Luna | T | K_MAR; HOUSE; not KID_NEAR (says "idiots") |
| HF172 | X K | T | K_MAR; HF_AT int; HF_W:KITCHEN; KS |
| HF173 | A +Luna | E MORNING at HF_AT ext | K_MAR; after:HF93; KS |

### Part P - Big days at home
| ID | Speakers | Type | Gates |
|---|---|---|---|
| HF174 | R L +Luna | E HF_AT (first visit after HF_ALL3_DONE) | HF_ALL3_DONE; say-once; KS |
| HF175 | I X A | E STORM + SNOW while in HOUSE | KS |
| HF176 | R +Luna | E HURT_HOME | KS |
| HF177 | K +Luna | E HOUSE_STAY3 | after:HF120 preferred (sharpening); KS |
| HF178 | K G | T | HF_AT int; HF_W:BEDROOMS; after:HF29; KS |
| HF179 | I K | T | HF_AT ext; SEASON:autumn any; KS |
| HF180 | C K +Luna | E NIGHT (hour >= 22) in HOUSE | after:HF103 (the stone) preferred; KS |

## 3. Notes for the build

- **Kaidan's own home/kids lines (K04 85+, `0Kaidan.esp` BYOHRelationshipAdoption INFOs, `BRP08Fam`):** Kaidan appears in no Part N talk and no talk that mentions children, fatherhood, nurseries or "family". His married talks (HF164-HF166, HF172) are about books, contracts, puns and baking. HF162/HF168/HF170/HF171 talk about him without him. Nothing describes the wedding itself (HF165 says only "some vows and a lot of nerves", true of all three wedding types). No anniversary gift or scripted event is invented in HF162.
- **No pregnancy or biological children** anywhere in this file (that job is separate, gated on Beeing Female). Every child here is adopted.
- **Kid-safe audit:** rows without `KS` contain "Mara's tits", "tusk yourself", drinking, betting with mead, a vampire-bite joke, or a child's nightmare about vampires. HF139 (arm wrestle, septim bets) and HF128 (Gore without trousers) are judged clean enough for KS; drop KS if the user disagrees.
- **Branch safety:** HF123, HF146 and HF154 need Serana uncured (`SER_VAMP`) where her vampirism is the joke; HF123 also needs the Soul Cairn done. HF119 waits for `LUC_ADMIT` (Clive). HF136, HF155 need `ASHE_REVEAL` (rest not sleep, "built me").
- **Callbacks to part one:** HF103/HF180 woodbox (HF10), HF106 log (HF9), HF107 optimism (HF15), HF114 fog (HF36), HF117 kitchen vote (HF16), HF128 plumbing (HF13), HF129 Ginger Kiss (HF52), HF135 four degrees (HF6), HF142 house rules (HF40), HF143 fishing (HF32), HF144 mudcrab (HF24), HF149 Captain Val (HF79), HF152 Tirdas (HF43), HF153/HF156 dull stories (HF69), HF173 bench (HF93), HF178 long bed (HF29). Their `after:` gates are hard where the talk would not make sense alone, "preferred" where it only reads better.
- **[U] facts to verify:** the grain mill as Heljarchen's exterior addition; Hearthfire child pets include mudcrab, dog, fox and skeever; trophy room offers a frostbite spider mount; stable, carriage driver, grindstone and garden as plot additions; Glass as a building material item; Constance Michel runs Honorhall once Grelod is dead (vanilla). Drop or re-gate any row whose fact fails.
- **Existing coverage avoided:** part one's topics (hinges, beam load, chores rota, guest book, bath, snore map, coffee, rent, keys, steward silver, bard hate, chickens, Big Moo, attacks, Mama, Uncle Gore, Grelod, Aventus, Sofie). NP217-NP219 housecarl talks not echoed. Val's own Ravani/Val00D and house comments not echoed. No "Dragonborn", no cult, no beard. Duplicate-title scan clean.
