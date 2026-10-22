# 50b LUNA THE MAGE 2 - trigger rows (prefix LN, LN81-LN180, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\50b LUNA THE MAGE 2.txt`.
Written 2026-10-18. Writing only: nothing in the game, `profiles\`, `mods\` or `ModOrganizer.ini` was touched.
Sources: `STYLE-GUIDE.md`, `MANIFEST.md` (EXPANSION), `TRIGGERS.md` sections 2-5, every bible in `research\bibles\`, the part-1 sheet `triggers\50 LUNA THE MAGE.md` (all its hooks and gate codes are reused unchanged), plus gate codes from `20 DAWNGUARD.md`, `35 COLLEGE OF WINTERHOLD.md`, `43 WHAT LUNA DOES.md`, `43b WHAT LUNA DOES 2.md`, `49 ASHE.md` and `57 INNS AND TOWN LIFE.md`.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana and Ashe Free rows (`SERANA_F`, `ASHE_F`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free() test, but the player must be out of dialogue and menus).
Type: T = timer, E = event (fires on the moment, or at the first safe tick within 60 s of it; otherwise the talk waits for the next time the event happens).

## Gate codes used in this file

Reused, same meaning as before: `K_CRUSH`, `K_TOG+`, `K_I`, `G_FLIRT` (TRIGGERS.md 4 / 43 sheet); `SERANA_F`, `DG_HARKON` (20 DAWNGUARD.md); `ASHE_F`, `ASHE_REVEAL`, `ASHE_LOGS` (49 ASHE.md); `GORE_READING` (35 COLLEGE.md); `CHILD_NEAR`, `TOWN` (57 INNS AND TOWN LIFE.md); `LOWHP` (43 sheet); `READ:<book>` (43b sheet: po3 `OnBookRead` against a title FormList); `pair meets (X+Y)` and `Remi and Xelzaz not fallen out` (50 LUNA THE MAGE.md). Every S row also needs `SERANA_F`; every A row also needs `ASHE_F`.

- `after:LNn` = that talk has played. `(+N day)` = at least N in-game days later.
- `after:CC154` = "Can... dle... light" (Gore gets Candlelight). `after:PA272`-style references are not used; Redcap's sweet-roll debt is self-contained here (LN140 then LN169).

## Events used

From earlier sheets: `E CAMP`, `E CAMP+NIGHT`, `E CAMP+MORNING` (CAMP and MORNING), `E RAIN`, `E SNOW`, `E STORM`, `E CRYPT`, `E HOUSE`, `E RIVERWOOD`, `E exterior`, `E exterior WILD`, `E exterior, not RAIN/SNOW`, `E AFTERFIGHT`, `E AFTERFIGHT (<who> below half health)`, `E AFTERFIGHT + LOWHP`, `E ALCHEMY`, `E ENCHANT`, `E BIGSPELL:<element>`, `E READ:<book>`, `E CAMP+NIGHT+READ:<book>`.

New here (all on the FB_Controller player alias):

| Event | How the controller sees it |
|---|---|
| `E CAST:<spell>` | Player alias `OnSpellCast(Form akSpell)`, akSpell in that spell's FormList. Lists: **DetectLife** (Detect Life, Detect Dead not included), **SoulTrap**, **Equilibrium**, **LightningStorm**, **Paralyze** (Paralyze, Mass Paralysis), **flesh** (Oakflesh excluded; Stoneflesh, Ironflesh, Ebonyflesh, Dragonhide), **Transmute**, **Invisibility**. In combat: hold and fire 8 s after combat ends. **[UNC: Requiem / Magic Redone may rename or replace these spells; build the lists from the live load order, by MGEF archetype where possible]** |
| `E BIGSPELL:frost` | As BIGSPELL in the part-1 sheet, effect resistance `FrostResist`. |
| `E AFTERFIGHT:mage` | AFTERFIGHT, and at least one enemy in the fight had a Destruction or Conjuration spell equipped (`GetEquippedSpell` polled on combat targets) or was in a mage faction FormList (warlocks, necromancers, hagravens, Thalmor mages). **[UNC: build the list]** |
| `E AFTERFIGHT:calm` | AFTERFIGHT, and the player cast a Calm / Pacify / Harmony spell during the fight (OnSpellCast, archetype Calm). |
| `E AFTERFIGHT:summon` | AFTERFIGHT, and the player had a summoned familiar or spectral wolf (po3 `GetCommandedActors(Player)`, race in a FormList) during the fight. |
| `E AFTERFIGHT:lucien_atronach` | AFTERFIGHT, and Lucien had a Flame Atronach commanded during the fight (po3 `GetCommandedActors(Lucien)`). **[UNC: Lucien's summon toggle must be on]** |
| `E AFTERFIGHT:bystander` | AFTERFIGHT, and an actor who was not hostile to the player, not a follower and not a summon died within 2000 units during the fight (po3 `OnActorKilled` / death event on nearby actors, `IsHostileToActor(Player) == false`). **[UNC: event coverage; fallback = guard or hunter corpse within 1500 units at combat end that was alive at combat start]** |
| `E AFTERFIGHT:healer` | AFTERFIGHT, and the player cast Restoration healing spells 5 or more times during the fight (OnSpellCast counter, MGEF archetype ValueModifier on Health, school Restoration). |
| `E SNEAKDONE` | Player stops sneaking after 30+ continuous seconds of sneaking with Kaidan following. Overrides the global sneak block only for the moment after sneaking ends. |
| `E MAGIC100` | Sticky milestone (43b `SKILL:` hook): the first time any of Alteration, Conjuration, Destruction, Illusion or Restoration reaches base 100. Stays eligible until it plays. |
| `E FOREST` | `E exterior WILD`, current hold is Falkreath, the Rift or Hjaalmarch (wooded holds). **[UNC: hold check by `GetCurrentLocation().GetParent` chain]** |
| `E DISENCHANT` | Player disenchants an item at an arcane enchanter: po3 `OnItemRemoved` / inventory count drop of an enchanted item while the Crafting Menu (enchanter) is open, with no new item made. **[UNC; fallback `E ENCHANT`]** |
| `E RAIN+CAMP` | CAMP and RAIN at the same time. |
| `E CAMP+NIGHT late` | CAMP and hour 0..4. |
| `E ALCHEMY+COLD` | ALCHEMY, and (SNOW or GameMonth in 11, 0, 1). |
| `E CHILD_NEAR+RIVERWOOD` | RIVERWOOD and CHILD_NEAR, Dorthe (Alvor's daughter) alive and within 1500 units (`NEAR:Dorthe`). |
| `E DETECT_TOWN` | `E CAST:DetectLife` while in TOWN or a farm (LocTypeFarm). |

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| LN81 | C I P | T | after:LN19; pair meets (C+I) |
| LN82 | C G P | E CAMP | after:LN81; pair meets (G+C) |
| LN83 | C P | E AFTERFIGHT:mage | after:LN82 |
| LN84 | I P | T | after:LN22 |
| LN85 | K I P | E exterior | after:LN84; K_I |
| LN86 | G K P | E AFTERFIGHT (Kaidan below half health) | after:LN25; pair meets (K+G) |
| LN87 | G R P | E AFTERFIGHT | after:LN86 (+2 day); pair meets (G+R) |
| LN88 | G P | E AFTERFIGHT + LOWHP | after:LN86 |
| LN89 | R P | T | - |
| LN90 | R X P | E CAMP | after:LN89; Remi and Xelzaz not fallen out |
| LN91 | R P | T | after:LN90 (+1 day) |
| LN92 | V P | T | - |
| LN93 | V K P | E exterior, not RAIN/SNOW | after:LN92; after:LN15; pair meets (K+V) |
| LN94 | V P | E AFTERFIGHT | after:LN92 |
| LN95 | K P | E SNEAKDONE | K_TOG+ |
| LN96 | K I P | E CAMP | after:LN95; K_TOG+; K_I |
| LN97 | K P | E CAMP+MORNING | after:LN96 (+2 day); K_TOG+ |
| LN98 | X P | E RAIN or SNOW | - |
| LN99 | G K P | E RAIN | after:LN98; pair meets (K+G) |
| LN100 | K V P | E CAMP | after:LN99; pair meets (K+V) |
| LN101 | L I P | E RAIN | after:LN100; pair meets (L+I) |
| LN102 | V R P | E CAMP, not RAIN/SNOW | after:LN101, LN92; pair meets (R+V) |
| LN103 | R P | T | after:LN102 (+1 day) |
| LN104 | X A P | E SNOW | after:LN103; ASHE_REVEAL |
| LN105 | K X P | E RAIN | after:LN103; K_CRUSH |
| LN106 | I P | E STORM | after:LN103 |
| LN107 | S P | T | after:LN106 (+1 day); SERANA_F |
| LN108 | G C P | E RAIN+CAMP | after:LN106 (+1 day); pair meets (G+C) |
| LN109 | C V P | T | after:LN108; pair meets (C+V) |
| LN110 | L X P | E CAMP | after:LN109; pair meets (X+L) |
| LN111 | K P | E exterior | after:LN109 |
| LN112 | C P | E CAMP+NIGHT+READ:The Pig Children | after:LN6 |
| LN113 | S P | E READ:2920 (any volume) | SERANA_F; DG_HARKON |
| LN114 | A P | E READ:Notes on Racial Phylogeny | ASHE_REVEAL |
| LN115 | G P | E READ:Children of the Sky | GORE_READING |
| LN116 | R P | E READ:The Lunar Lorkhan | - |
| LN117 | X K P | E READ:The Red Kitchen Reader | pair meets (X+K: C3) |
| LN118 | I P | E READ:Fire and Darkness: The Brotherhoods of Death | - |
| LN119 | L P | E READ:The Mystery of Talara (any volume) | after:LN108 |
| LN120 | K P | E READ:The Monomyth | - |
| LN121 | L S P | E READ:Darkest Darkness | SERANA_F; pair meets (S+L) |
| LN122 | G P | T | after:LN88 |
| LN123 | K I P | E CAST:DetectLife | K_CRUSH; K_I |
| LN124 | A P | E CAST:SoulTrap | ASHE_REVEAL |
| LN125 | X L P | E AFTERFIGHT:lucien_atronach | pair meets (X+L) |
| LN126 | L P | E CRYPT (on arrival) | - |
| LN127 | K P | E CAST:Equilibrium | K_TOG+ |
| LN128 | V G P | E CAST:LightningStorm | pair meets (G+V) |
| LN129 | X P | E BIGSPELL:frost | after:LN109 |
| LN130 | S P | E CAST:Paralyze | SERANA_F; DG_HARKON |
| LN131 | C P | E CAST:flesh | - |
| LN132 | R I P | E CRYPT | pair meets (R+I) |
| LN133 | L G P | E CAMP | pair meets (L+G) |
| LN134 | I P | E CAST:Invisibility | after:LN22; after:LN98 |
| LN135 | K P | T | - |
| LN136 | R P | E CAST:Transmute | - |
| LN137 | I L P | E DETECT_TOWN | pair meets (L+I) |
| LN138 | K G P | E CAMP+MORNING | pair meets (K+G) |
| LN139 | V P | E AFTERFIGHT:calm | - |
| LN140 | C P | E AFTERFIGHT:summon | - |
| LN141 | G K P | E FOREST | pair meets (K+G) |
| LN142 | C P | E CAMP | after:LN141 |
| LN143 | R X P | T | after:LN142; Remi and Xelzaz not fallen out |
| LN144 | V L P | T | after:LN143; pair meets (L+V) |
| LN145 | R P | E ENCHANT | - |
| LN146 | A R P | E ENCHANT | after:LN91; ASHE_REVEAL |
| LN147 | L P | E DISENCHANT | - |
| LN148 | V P | E ENCHANT | after:LN108 |
| LN149 | X P | E READ:Herbalist's Guide to Skyrim | - |
| LN150 | X P | E ALCHEMY | - |
| LN151 | C X P | E ALCHEMY | pair meets (C+X: R18) |
| LN152 | X R P | E READ:Song of the Alchemists | Remi and Xelzaz not fallen out |
| LN153 | X G P | E ALCHEMY+COLD | pair meets (X+G) |
| LN154 | G P | E HOUSE | GORE_READING |
| LN155 | K L P | E HOUSE | pair meets (K+L) |
| LN156 | V P | E HOUSE | - |
| LN157 | C P | E HOUSE + NIGHT | - |
| LN158 | A P | E HOUSE | ASHE_REVEAL |
| LN159 | C P | E CHILD_NEAR | - |
| LN160 | G P | E CHILD_NEAR | after:CC154 |
| LN161 | L P | E CHILD_NEAR | - |
| LN162 | K P | E CHILD_NEAR+RIVERWOOD | - |
| LN163 | V K P | E MAGIC100 | pair meets (K+V) |
| LN164 | L P | T | after:LN110 (+2 day) |
| LN165 | I P | E AFTERFIGHT:bystander | - |
| LN166 | X P | T | - |
| LN167 | A P | E AFTERFIGHT:healer | ASHE_LOGS |
| LN168 | K P | E CAMP+NIGHT late | K_TOG+ |
| LN169 | C P | E CAMP | after:LN140 |
| LN170 | S P | E CAMP+NIGHT | SERANA_F |
| LN171 | R P | E CAMP | after:LN108, LN83, LN86, LN84 |
| LN172 | G C P | E CAMP | after:LN88, LN83; pair meets (G+C) |
| LN173 | K P | E exterior WILD | after:LN144; K_CRUSH |
| LN174 | G K | T | K_CRUSH; not G_FLIRT; pair meets (K+G) |
| LN175 | K V P | T | after:LN102; K_CRUSH |
| LN176 | K P | T | after:LN60; K_CRUSH |
| LN177 | K I P | E CAMP | K_CRUSH; K_I |
| LN178 | S P | T | SERANA_F; DG_HARKON |
| LN179 | A P | E CAMP | ASHE_REVEAL |
| LN180 | L I P | E CAMP | after:LN110, LN91, LN144; pair meets (L+I) |

## Notes for the build

- **Chains.**
  - Redcap's ward: LN19 > LN81 > LN82 > LN83.
  - Inigo's telekinesis: LN22 > LN84 > LN85.
  - Gore's healing: LN25 > LN86 > LN87 / LN88 > LN122.
  - Remi's sparks: LN89 > LN90 > LN91 > LN146.
  - Val's storms: LN92 > LN93 / LN94, and LN92 feeds LN102.
  - Kaidan's Muffle (K_TOG+ only): LN95 > LN96 > LN97.
  - The rain-ward spine: LN98 > LN99 > LN100 > LN101 > LN102 > LN103 > LN106 > LN108 > LN109 > LN110 > LN164. Side talks hang off it and never block it: LN104 (Ashe), LN105 (Kaidan crush), LN107 (Serana), LN111, LN119, LN129, LN134, LN148, LN171, LN175.
  - The staff: LN141 > LN142 > LN143 > LN144 > LN173.
  - Redcap's sweet-roll debt: LN140 > LN169.
  - Wrap-ups: LN171 and LN172 need the lessons; LN180 needs the rain-ward paper, Remi's paper and the staff.
- **The spine needs most of the party.** It uses Xelzaz, Gore, Kaidan, Val, Lucien, Inigo, Remi and Redcap at different steps. If one of them is never recruited, the chain stops at that step. **[Build option: let a spine talk be skipped (marked played) after 10 in-game days of waiting, so the next step can fire.]**
- **Weather talks** (LN98, LN99, LN101, LN104-LN106, LN108) need real rain, snow or a storm. STORM uses the TRIGGERS.md proxy, unconfirmed.
- **Kaidan's crush talks** (LN105, LN123, LN173-LN177): Luna never notices. LN174 has no Luna line: Kaidan and Gore talk about her. The Muffle lessons (LN95-LN97), LN127 and LN168 need K_TOG+, and she is openly fond of him there.
- **Rivals:** none of these talks is a rival talk. LN174 keeps `not G_FLIRT` so Gore is teasing, not competing. Val in LN175 teases Kaidan but makes no move on Luna.
- **Spoilers:** Ashe talks that mention her being a machine all carry ASHE_REVEAL. Serana's father is named only with DG_HARKON. No Kaidan cult, Rosalind or Brynjar reference anywhere (LN141's firewood line is about his own work, on purpose). Nobody says "Dragonborn".
- **Topics avoided because they already exist:** Val's floating sweetroll (PR298) and Luna's ladle theft (PA198) for telekinesis; Kaidan's Candlelight at the College (MG70) and his quiet-walking lesson from Val (PA172) - the Muffle lessons are their pay-off, not a repeat; Sparky's name (PA187) and Val's Candlelight (PA197); Luna's warming and frost wards (PA129, PA113) - the rain-ward is a new spell, not a ward test; the staff that knows her hand (PA281); the Lusty Argonian Maid (many files); the goat (PA123, PA227).
- **Luna's past stays vague.** The only hints are "a good student who read a lot" (LN171) and that she once had a first fight and a first book (part 1). Nothing says where or when.
