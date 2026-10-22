# 50 LUNA THE MAGE - trigger rows (prefix LN, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\50 LUNA THE MAGE.txt`.
Written 2026-10-18. Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-5, every bible in `research\bibles\`, and the gate codes in `triggers\20 DAWNGUARD.md`, `35 COLLEGE OF WINTERHOLD.md`, `43 WHAT LUNA DOES.md`, `48 SERANA.md` and `49 ASHE.md` (reused unchanged). Nothing in the game or the profile was touched.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana Free() and Ashe silence rows in `20 DAWNGUARD.md` / `49 ASHE.md`. Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free() test, but a talk with P lines still needs the player out of dialogue and menus).
Type: T = timer, E = event (fires on the moment, or at the first safe tick within 60 s of it; otherwise the talk waits for the next time the event happens).

## Gate codes used in this file

Reused, same meaning as before: `K_CRUSH`, `K_TOG+`, `V_FLIRT`, `G_FLIRT` (TRIGGERS.md 4); `SERANA`, `SER_VAMP`, `DG_VALERICA`, `DG_CAIRN` (20 DAWNGUARD.md); `ASHE_REVEAL`, `ASHE_LOGS` (49 ASHE.md); `ARCH`, `GORE_READING` (35 COLLEGE.md); `RC_MANOS` (Bigpig found; same use as HF24/HF51).

- `pair meets (X+Y)` = that pair's first-meeting talk or their own mod's intro has played (TRIGGERS.md section 4, "Chains"). Kaidan+Inigo = `KaiandInigo` stage >= 10, as K4. Remi+Xelzaz, Remi+Gore, Remi+Val, Remi+Redcap, Xelzaz+Lucien, Xelzaz+Redcap use their own mods' intro stages, as in files 10-49.
- `Remi and Xelzaz not fallen out` = `BPUFXelzazRemielFallingOut` 11 not done, or 13 done (TRIGGERS.md section 3 note).
- `after:CC154` = the Creation Club talk "Can... dle... light" (Luna gives Gore Candlelight in the Lost Library) has played. Every Gore-Candlelight talk here needs it.
- `after:LNn` = that talk from this file has played. `(+1 day)` = at least one in-game day later.
- `not G_FLIRT` on LN28 = Gore is not flirting with Luna (he's coaching Kaidan, not competing).

## Events used

From TRIGGERS.md section 4 / earlier files: `E INN`, `E CAMP`, `E CAMP+NIGHT`, `E CLEARNIGHT`, `E RAIN`, `E CAVE`, `E DWEMER`, `E exterior WILD` (N rows), `E store in a city` (48 SERANA.md).

New here (all on the FB_Controller player alias; signatures as in 43 WHAT LUNA DOES.md, which already registers these hooks):

| Event | How the controller sees it |
|---|---|
| `E BIGSPELL` | Player alias `OnSpellCast(Form akSpell)`: the spell's costliest effect has `MagicEffect.GetSkillLevel() >= 75` (Expert or Master, SKSE). In combat: hold it and fire 8 s after combat ends. **[UNC: confirm GetSkillLevel on modded Requiem spells; fall back to spell cost >= 150]** |
| `E BIGSPELL:fire` / `:shock` | As BIGSPELL, and that effect's `GetResistance()` is `FireResist` / `ElectricResist` (SKSE). |
| `E ALCHEMY` | `OnTrackedStatsEvent("Potions Mixed")` (same hook and spelling caveat as 43 WHAT LUNA DOES.md, PA66). |
| `E ENCHANT` | `OnTrackedStatsEvent("Magic Items Made")` (as PA72). |
| `E TOME_FOUND` | `OnItemAdded` with a Book whose SKSE `GetSpell() != None`, source container not in a LocTypeStore location (looted, not bought), and the player does not know that spell (`HasSpell == 0`). Needs `AddInventoryEventFilter` on a keyword/list of tomes **[UNC: VendorItemSpellTome 0937A5 keyword filter]**. |
| `E TOME_FOUND:corpse` | As TOME_FOUND, and `akSourceContainer` is a dead Actor. |
| `E LIBRARY` | Player enters an interior from a cell list: Arcanaeum (College), Calcelmo's Laboratory, the Bards College, Dragonsreach (Farengar's study), Septimus Signus's Outpost, the LotD library, plus any player-home library room. **[UNC: build the cell list; a "10+ bookshelf refs in cell" scan is the fallback]** |
| `E STONE:<name>` | Player within 600 units of that Guardian Stone's activator ref (Steed, Atronach, Mage, Shadow, Lover, Apprentice). First visit with the named followers following. **[UNC: the six activator ref FormIDs in Skyrim.esm]** Fires on arrival, not on activation: no talk depends on which stone the player takes. |
| `E CAMP+BOOKREAD` / `E CAMP+NIGHT+BOOKREAD` | CAMP (and NIGHT) and po3 `OnBookRead(Book)` within the last 60 s (any book that is not a spell tome). |
| `E COLLEGE` | Player in `WinterholdCollegeLocation` or any of its child locations (interior), Arch-Mage's Quarters preferred. |
| `E AFTERFIGHT (<who> below half health)` | Same mechanism as AS rows in 49 ASHE.md: the controller tracks that follower's lowest health % during the fight (OnHit on the follower alias). |
| `E exterior, not RAIN/SNOW` | Exterior, `IsRaining == 0`, `IsSnowing == 0`. |

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| LN1 | G L P | T | pair meets (G+L) |
| LN2 | G P | T | GORE_READING |
| LN3 | G K P | E STONE:Steed | pair meets (K+G) |
| LN4 | K P | E RAIN | K_CRUSH |
| LN5 | A P | T | ASHE_REVEAL |
| LN6 | C P | T | RC_MANOS (Bigpig found) |
| LN7 | I P | E INN | - |
| LN8 | V P | E store in a city | - |
| LN9 | L P | T | - |
| LN10 | L P | T | - |
| LN11 | V P | E CLEARNIGHT | - |
| LN12 | G P | T | - |
| LN13 | L K P | E CAMP | pair meets (K+L) |
| LN14 | X P | T | - |
| LN15 | K P | E exterior, not RAIN/SNOW | - |
| LN16 | R P | E DWEMER | - |
| LN17 | C I P | T | pair meets (C+I) |
| LN18 | C G P | E CAMP | after:LN17; pair meets (G+C) |
| LN19 | C P | E CAMP | after:LN18 (+1 day) |
| LN20 | I P | T | - |
| LN21 | R I P | T | after:LN20; pair meets (R+I) |
| LN22 | K I P | T | after:LN21; Kaidan and Inigo have met (KaiandInigo >= 10) |
| LN23 | K P | T | K_CRUSH |
| LN24 | K G P | T | after:CC154; pair meets (K+G) |
| LN25 | G P | T | after:LN24 |
| LN26 | V K P | T | V_FLIRT; K_CRUSH |
| LN27 | S P | T | SERANA |
| LN28 | G K | T | K_CRUSH; not G_FLIRT; after:CC154 |
| LN29 | R X P | E CAMP | Remi and Xelzaz not fallen out |
| LN30 | X R P | T | after:LN29; Remi and Xelzaz not fallen out |
| LN31 | R P | T | - |
| LN32 | X R P | T | Remi and Xelzaz not fallen out |
| LN33 | L I P | T | pair meets (L+I) |
| LN34 | L X P | T | after:LN30, LN31, LN32, LN33; pair meets (X+L) |
| LN35 | X P | E ALCHEMY | - |
| LN36 | K P | E BIGSPELL:fire | K_CRUSH |
| LN37 | C P | E BIGSPELL | - |
| LN38 | V P | E BIGSPELL:shock | - |
| LN39 | I P | E BIGSPELL | - |
| LN40 | R V P | E BIGSPELL | - |
| LN41 | C P | E ENCHANT | - |
| LN42 | K P | E ENCHANT | K_TOG+ |
| LN43 | S P | E ENCHANT | DG_CAIRN |
| LN44 | A P | E ALCHEMY | ASHE_REVEAL |
| LN45 | V P | E ALCHEMY | - |
| LN46 | S P | T | DG_VALERICA |
| LN47 | X P | T | - |
| LN48 | X P | T | - |
| LN49 | A P | T | ASHE_LOGS |
| LN50 | A P | E STONE:Atronach | ASHE_REVEAL |
| LN51 | R P | T | - |
| LN52 | R G P | E CAVE or DWEMER | after:CC154 |
| LN53 | K R P | E RAIN | pair meets (R+K) |
| LN54 | L P | E LIBRARY | - |
| LN55 | L X P | T | pair meets (X+L) |
| LN56 | R S P | T | SERANA; pair meets (S+R) |
| LN57 | S X P | T | SERANA; pair meets (S+X) |
| LN58 | R X P | T | Remi and Xelzaz not fallen out |
| LN59 | G P | E COLLEGE | ARCH |
| LN60 | L R P | T | pair meets (L+R) |
| LN61 | V K P | E exterior WILD | pair meets (K+V) |
| LN62 | K C P | T | K_CRUSH; after R1 |
| LN63 | G P | E CAMP+NIGHT | GORE_READING |
| LN64 | K P | E CAMP | K_TOG+ |
| LN65 | L P | E AFTERFIGHT (Lucien below half health) | - |
| LN66 | G P | E AFTERFIGHT (Gore below half health) | - |
| LN67 | X P | E CAMP+NIGHT | - |
| LN68 | A P | E CAMP | ASHE_LOGS |
| LN69 | K P | E CAMP+NIGHT | K_TOG+ |
| LN70 | S P | T | SERANA; SER_VAMP |
| LN71 | L P | E TOME_FOUND:corpse | - |
| LN72 | V L P | E TOME_FOUND | pair meets (L+V) |
| LN73 | R P | E LIBRARY | - |
| LN74 | S P | E LIBRARY | SERANA |
| LN75 | L P | E STONE:Mage | - |
| LN76 | I P | E STONE:Shadow | after:LN22 |
| LN77 | G K P | E STONE:Lover | G_FLIRT; K_CRUSH |
| LN78 | C P | E STONE:Apprentice | after:LN18 |
| LN79 | C R P | E CAMP+NIGHT+BOOKREAD | pair meets (R+C: FA01RemiIntroScene done) |
| LN80 | V P | E CAMP+BOOKREAD | - |

## Notes for the build
- Chains: LN17 > LN18 > LN19 (Redcap's fire), LN20 > LN21 > LN22 > LN76 (Inigo's invisibility), LN24 > LN25 (Gore), LN29 > LN30, LN30+LN31+LN32+LN33 > LN34, LN18 > LN78.
- BIGSPELL has five talks (LN36-LN40); only one plays per cast, then the normal 300 s cooldown applies.
- Rival talks: LN26 (Val + Kaidan), LN77 (Gore + Kaidan). Luna answers as a scholar both times and never notices. LN4, LN23, LN36, LN62 are Kaidan's crush with Luna oblivious; LN28 is Kaidan's crush without her. LN42, LN64, LN69 need K_TOG+ and she's openly fond of him.
- Luna's past stays vague on purpose (LN64, LN65): a book with a scorch mark and a book thrown in a first fight are the only details, and neither says where or when.
- Topics avoided because they already exist: Luna's "scenic route" line, the College talks (Kaidan's Candlelight MG70, flinching MG37, Brelyna, the Arcanaeum), learning tomes and enchanting/alchemy firsts and skill milestones (43 WHAT LUNA DOES), party rules/rotas/riddles/ghost librarian (45 PARTY LIFE), Val's Ritual-not-Lover star line (W10), Ashe's heart-rate logging, the Serana star names (SE56).
- No "Dragonborn" anywhere in the file. No Kaidan cult or Brynjar reference (LN15 says "before I could read" on purpose).
