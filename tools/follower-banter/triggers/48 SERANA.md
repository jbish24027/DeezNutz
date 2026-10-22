# 48 SERANA - trigger rows (prefix SE, 80 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\48 SERANA.txt`.
Sources: `research\bibles\serana.md` (sections 3 and 6), the other bibles for each partner, `TRIGGERS.md` sections 2-4, and `triggers\20 DAWNGUARD.md` (its Free() rows, silence list and gate codes are reused here unchanged).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`), the Dawnguard silence in `20 DAWNGUARD.md` section 2, and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment).

## Free() for Serana and Ashe (copied from 20 DAWNGUARD.md section 1, unchanged)

| Who | Following test | Busy blocks |
|---|---|---|
| Serana | `GetVMQuestVariable DLC1NPCMentalModel(002B6E:Dawnguard.esm) ::IsFollowing_var == 1` and `::CanFollow_var == 1` | `IsInScene == 0`; `SDA_PlayerInDialogue (9EB814:SeranaDialogAddon.esp) == 0`; not running: SDA_SeranaRomance01..13, SDA_DrinkingBuddies (61AB00), SDA_DrinkingBuddiesWaiting, SDA_SleepingQuest (D29EB8), SDA_SeranaRideHorse; not during the cure absence (`SDA_CureQuestTimer` 5EE3E9 running) |
| Ashe | `GetVMQuestVariable MM_AsheMentalModel(06FE28:Ashe - Fire and Blood.esp) ::IsFollowing_var == 1`, `::IsWaiting == 0`, `::bConfigVarIdles == 1` | `MM_PlayerinDialogue (5435E9) == 0`, `MM_FlashbackRunning (4643DC) == 0`, `MM_ScriptedCombatScenePlaying (BF887E) == 0`, `MM_AsheranaSleepBanterPlaying (52B269) == 0`, `MM_AsheSeranaLoveBanterBlock (628708) == 0`; ashe.md 6 quest blocks |

Every SE talk also needs `SERANA` (DLC1VQ02 stage 5 done) and Serana Free, even where the row only lists a later gate.

## Gate codes used in this file

Reused from TRIGGERS.md section 4 and 20 DAWNGUARD.md section 3 (same meaning):
`SERANA`, `DG_HARKON`, `DG_GARDEN`, `DG_VALERICA`, `DG_CAIRN`, `DG_END`, `SER_VAMP`, `SER_CURED`, `S_ROM_ON`, `S_ROMOFF`, `S_COMP`, `S_KISS`, `S_LOVE`, `A_CRUSH`, `A_ANY`, `ASHE_REVEAL`, `ASHE_Q1`, `K_CRUSH`, `K_TOG`, `K_TOG+`, `K_LOVE+`, `G_FLIRT`, `V_FLIRT`, `V_ANY`, `ANYROM`, `BRYNJAR`, `GORE_FATHER`, `VAL_FATHIS`, `LUC_ADMIT`, `INIGO_BV`.

New here:
- `KINV` = Kaidan's Akaviri cache quest ("All of this Past", EditorID `KINV`, 0Kaidan.esp) completed: he has read his mother's letter and knows he is Akaviri. **[UNC: FormID and final stage not traced; bible gives only the EditorID]**
- `Val006 stage 20` = Val's "Safe Harbor": the Spring Rain has been bought (same check as A17 in TRIGGERS.md). **[UNC stage]**
- `first S+K talk in this file` (and S+X) = no other SE talk with those two speakers has played yet. These open their pair, so the controller picks them before the pair's later SE talks.
- Romance gates are always on Serana's side *and* the other suitor's side. All Serana rival talks also need `S_ROM_ON`, except SE58 (`S_ROMOFF`).

Events used (TRIGGERS.md section 4 unless noted):
- `E INN`, `E INN+NIGHT`, `E CAMP`, `E CAMP+NIGHT`, `E CAMP or INN`, `E MORNING`, `E SNOW`, `E RAIN`, `E CLEARNIGHT`, `E CITY:Windhelm`.
- `E exterior WILD` = TRIGGERS N-row WILD (exterior, not LocTypeHabitation, player moving).
- `E store in a city` = player enters an interior with LocTypeStore whose parent location is a hold capital. **[UNC: books-for-sale check; any store is acceptable]**
- `E WATER (sea coast)` / `E WATER (beach)` = WATER proxy plus player in a coastal exterior cell (Sea of Ghosts shore: north coast from Solitude to Winterhold, or Solstheim). **[UNC: no keyword; needs a cell list or a z-height + worldspace-edge check]**
- `E AFTERFIGHT:<type>` as in TRIGGERS.md and 20 DAWNGUARD.md. New types: `necromancer` (last target in a necromancer faction / class Conjurer-Necromancer **[UNC]**), `dragon` (last target race is a dragon race), `hunter` (vampire-hunter encounter: DLC1HunterFaction 003375 while Serana is a vampire), `werewolf` (WerewolfBeastRace), `bandit+raisedcorpse` (bandit fight in which Serana had a reanimated actor, see `raisedcorpse` in 20 DAWNGUARD.md). `raisedcorpse` reused **[UNC]**.

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| SE1 | S K P | T | SERANA; SER_VAMP; first S+K talk in this file |
| SE2 | G S | T | SERANA; after DG77 |
| SE3 | S V P | E INN | SERANA |
| SE4 | X S | T | SERANA; first S+X talk in this file |
| SE5 | L S P | T | SERANA; after DG2 |
| SE6 | C S | T | SERANA; after Q19 and DG8 |
| SE7 | R S | T | SERANA; SER_VAMP |
| SE8 | S I | T | SERANA; SER_VAMP |
| SE9 | S L P | E store in a city | SERANA; after DG2 |
| SE10 | S K | T | SERANA; KINV |
| SE11 | G S P | E INN | SERANA |
| SE12 | S C | T | SERANA; after DG8 |
| SE13 | S X | E CITY:Windhelm | SERANA |
| SE14 | R S P | T | SERANA |
| SE15 | S V | E WATER (sea coast) | SERANA; after DG27 |
| SE16 | G S | T | DG_HARKON; GORE_FATHER |
| SE17 | S V | T | SERANA; VAL_FATHIS |
| SE18 | R S | T | SERANA |
| SE19 | L S | T | DG_GARDEN |
| SE20 | I S | T | DG_END |
| SE21 | K S | E CAMP | SERANA; BRYNJAR |
| SE22 | S X | E CAMP+NIGHT | SERANA |
| SE23 | I S | T | SERANA; SER_VAMP |
| SE24 | C S | T | SER_CURED; after DG70 |
| SE25 | V S P | E MORNING | SER_CURED |
| SE26 | K S P | E CAMP or INN | SER_CURED |
| SE27 | L S P | T | SER_VAMP |
| SE28 | G S | T | DG_END; SER_VAMP; after DG1 |
| SE29 | S X | E SNOW | SER_CURED |
| SE30 | R S P | T | SER_VAMP |
| SE31 | S P | E CAMP+NIGHT | SER_CURED; after SE26 |
| SE32 | S P | T | DG_VALERICA |
| SE33 | S C P | E INN+NIGHT | SERANA |
| SE34 | S L P | T | SERANA |
| SE35 | I S P | T | SERANA |
| SE36 | X S | E AFTERFIGHT:raisedcorpse | SERANA |
| SE37 | S P | T | DG_CAIRN |
| SE38 | S V P | T | SERANA |
| SE39 | G S | T | SERANA; after SE2 |
| SE40 | G S | E CAMP | SERANA |
| SE41 | G S | E CAMP+NIGHT | SERANA |
| SE42 | S K | T | SER_VAMP |
| SE43 | K S P | T | SERANA |
| SE44 | V S | E WATER (sea coast) | SERANA; Val006 stage 20 (boat bought) [UNC]; after DG27 |
| SE45 | V S | T | SER_VAMP |
| SE46 | L S P | T | SERANA |
| SE47 | S L | T | LUC_ADMIT; SER_VAMP |
| SE48 | C S | T | SERANA; after DG8 |
| SE49 | X S P | E CAMP | DG_VALERICA; after SE19 |
| SE50 | I S | E RAIN | SER_VAMP |
| SE51 | I S | T | INIGO_BV; DG_END |
| SE52 | R S | T | SER_VAMP |
| SE53 | A S | T | SERANA; ASHE_REVEAL |
| SE54 | S A | T | SERANA; ASHE_Q1 |
| SE55 | S P | E WATER (beach) | SERANA |
| SE56 | S P | E CLEARNIGHT | SERANA |
| SE57 | S K | T | K_CRUSH; S_COMP |
| SE58 | S K P | T | K_CRUSH; S_ROMOFF |
| SE59 | S K | E MORNING | K_TOG; S_KISS; after SE57 |
| SE60 | S K | T | K_LOVE+; S_LOVE; SER_VAMP |
| SE61 | K S | E MORNING | K_LOVE+; S_LOVE; SER_CURED |
| SE62 | G S | E CAMP | G_FLIRT; S_COMP; after SE40 |
| SE63 | G S | T | G_FLIRT; S_KISS; after SE39 |
| SE64 | V S P | E CAMP+NIGHT | V_FLIRT; S_COMP |
| SE65 | V S | T | V_ANY; S_KISS |
| SE66 | S A | T | A_CRUSH; S_COMP; ASHE_REVEAL |
| SE67 | R S | T | S_COMP |
| SE68 | S I | E INN | S_KISS |
| SE69 | L S | T | ANYROM; S_COMP |
| SE70 | C S | T | ANYROM; S_COMP |
| SE71 | X S | T | ANYROM; S_KISS |
| SE72 | S K P | E INN | K_TOG+; S_KISS |
| SE73 | L S P | E AFTERFIGHT:draugr | SERANA |
| SE74 | R S | E AFTERFIGHT:necromancer | SERANA |
| SE75 | S K | E AFTERFIGHT:Thalmor | SERANA |
| SE76 | V S P | E AFTERFIGHT:dragon | SERANA |
| SE77 | X S | E AFTERFIGHT:hunter | SER_VAMP |
| SE78 | C S | E AFTERFIGHT:hagraven | SERANA |
| SE79 | G S | E AFTERFIGHT:bandit+raisedcorpse | SERANA |
| SE80 | I S | E AFTERFIGHT:werewolf | SERANA |

## Notes for the build
- Luna has no romance line anywhere in Part 7. In SE58 (Kaidan's crush) she misses the point completely, as the style guide asks.
- SE24 and SE26 are cure talks; SE31 waits for SE26 so "Kaidan's sandwiches" has a setup.
- SE59 follows SE57 (the sunrise/midnight deal) and borrows the star names from SE56. SE62 follows SE40 (the pirate book). SE63 follows SE39 ("sister"), which follows SE2 (the feather).
- Never fire a Part 7 talk while any SDA_SeranaRomance quest is running (her Free row already blocks this).
- Topics avoided on purpose: SDA's own Serana x Inigo and Serana x Remi talks, the Ashe and Serana patch, and every Serana talk in files 20, 21, 22, 30-37, 43 and 45 (cloak, cage, garden, jetty, Talonwood, Breton culture, age jokes, juniper sauce, cure smells and sun, cellar, key, Molag Bal horse dung).
- Kaidan's tattoo (SE42) is only "a bad time"; nothing about where it came from.
- No "Dragonborn" anywhere in the file.
