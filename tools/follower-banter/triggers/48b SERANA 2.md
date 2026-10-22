# 48b SERANA 2 - trigger rows (prefix SE, continues SE81-SE180, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\48b SERANA 2.txt`.
Sources: `research\bibles\serana.md` (sections 1, 3, 6), the partner bibles, `TRIGGERS.md` sections 2-4, `triggers\20 DAWNGUARD.md` (Free() rows, silence list, gate codes) and `triggers\48 SERANA.md` (part 1 codes and events, reused unchanged).
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`), the Dawnguard silence in `20 DAWNGUARD.md` section 2, and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment).

Every SE talk also needs `SERANA` (DLC1VQ02 stage 5 done) and Serana Free (row in `48 SERANA.md`), even where the row only lists a later gate. Ashe talks also need Ashe Free and `ASHE_HIRED`.

## Gate codes used in this file

Reused (TRIGGERS.md section 4, 20 DAWNGUARD.md section 3, 48 SERANA.md, 49 ASHE.md): `SERANA`, `HELGEN`, `DG_HARKON`, `DG_CAIRN`, `DG_DURN`, `DG_END`, `SER_VAMP`, `SER_CURED`, `S_ROM_ON`, `S_ROMOFF`, `S_COMP`, `S_KISS`, `NOT_S_KISS`, `S_LOVE`, `A_ANY`, `ASHE_REVEAL`, `K_CRUSH`, `BRYNJAR`, `LUC_ADMIT`, `INIGO_BV`, `ANYROM`.

New here (all SeranaDialogAddon.esp, FormIDs from serana.md section 3; every one also needs `S_ROM_ON`):
- `S_PANNE` = SDA_SeranaRomance05 "La Panne" (AD97E6) completed: the rest stop where she sings "Old Stone Walls". **[UNC completion stage]**
- `S_VALE` = SDA_SeranaRomance07 "Coruscation in the Vale" (B2A82D) completed. **[UNC]**
- `S_DETERM` = SDA_SeranaRomance08 "Determination" (B2A83E) completed: her breakdown before the last fight. **[UNC]**
- `S_COVENANT` = SDA_SeranaRomance10 "A New Covenant" (B2F967) completed, or `SDA_IsSeranaMarried == 1`. **[UNC]**
- `S_TRUST` = SDA_SeranaRomance10Trust (46C3EC) completed: she confessed she manipulated Luna at first. **[UNC]**
- `S_FRIENDTALK` = SDA_SeranaRomance12 "Friendship Conversation" (56E84B) completed ("I chose you, and you chose me"). **[UNC]**
- `S_BEACH` = SDA_SeranaRomance13 "Undying Love" (347A07) completed (beach date). **[UNC]**
- `LUNA_SUNSPELL` = player knows a sun-damage spell (vanilla Vampire's Bane / Stendarr's Aura, Dawnguard Sun Fire / Vampire's Bane): `HasSpell` on any of them. **[UNC FormIDs]**
- `RC_BIGPIG` = Redcap can call his boar (his totem/boar power is unlocked in his mod). **[UNC: quest/global not traced; fall back to RC_MANOS]**

Events (TRIGGERS.md section 4, 48 SERANA.md unless noted):
- `E INN`, `E CAMP`, `E CAMP+NIGHT`, `E CAMP or INN`, `E MORNING`, `E PREDAWN`, `E RAIN`, `E CLEARNIGHT`, `E NIGHT`, `E CRYPT`, `E CITY`, `E CITY:<Name>`, `E HELGEN_LOC`, `E WATER (sea coast)`, `E NIGHT (HOUSE or INN)`, `E WILD`.
- `E MORNING after INN` = MORNING while the player is in LocTypeInn (she woke there).
- `E SUNNY` = exterior, IsPleasant, hour 9..17 (same as DG3).
- `E SUMMER SUNNY` = SUNNY and GameMonth 5..7.
- `E WATER (Solitude coast)` = same check as RV106 (coast near Solitude with Castle Volkihar in view). **[UNC]**
- `E AFTERFIGHT:<type>` as in 48 SERANA.md. New types: `vampire` (as 20 DAWNGUARD.md), `spider`, `vigilant` (target in a Vigil of Stendarr faction **[UNC]**), `bear` (BearRace family), `draugr`, `wolf` (WolfRace), `slaughterfish` (SlaughterfishRace) or Serana swam during the fight, `troll`, `dragonpriest` (DragonPriestRace), `argonian` (any dead target ArgonianRace), `raisedcorpse` (as 20 DAWNGUARD.md). `AFTERFIGHT (Serana hurt)` = Serana health dropped below 75% during the fight. `AFTERFIGHT (player near death)` = player health below 15% during the fight (same mechanism as K19). **[UNC: controller must track health during combat]**

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| SE81 | K S | T | SERANA |
| SE82 | K S P | T | SERANA |
| SE83 | K S | E MORNING after INN | SER_CURED |
| SE84 | G S | E HELGEN_LOC | HELGEN; SERANA |
| SE85 | G S P | E CITY (any hold capital) | SERANA |
| SE86 | G S | E CAMP | after SE41 |
| SE87 | V S P | E INN | SERANA |
| SE88 | V S | T | SER_CURED |
| SE89 | V S | T | SERANA |
| SE90 | R S P | T | DG_END |
| SE91 | R S | T | SERANA |
| SE92 | R S | T | after SE74 |
| SE93 | L S P | E CAMP | SERANA |
| SE94 | L S | T | LUC_ADMIT; after SE47 |
| SE95 | L S | E CRYPT | SERANA |
| SE96 | X S P | E INN | SER_CURED |
| SE97 | X S P | T | SERANA |
| SE98 | S A P | E NIGHT (HOUSE or INN) | ASHE_REVEAL |
| SE99 | A S | E CAMP+NIGHT | ASHE_REVEAL |
| SE100 | S P | T | after DG2 |
| SE101 | S L | T | SERANA |
| SE102 | S K | T | DG_END |
| SE103 | G S | E CAMP+NIGHT | SERANA |
| SE104 | V S | E WATER (sea coast) | SERANA |
| SE105 | X S | T | SERANA |
| SE106 | R S P | T | SERANA |
| SE107 | S P | E CAMP | SERANA |
| SE108 | S V | E WATER (Solitude coast) | SERANA |
| SE109 | S P | T | DG_END |
| SE110 | K S | T | SERANA; BRYNJAR |
| SE111 | G S P | E CAMP | SERANA |
| SE112 | L S | T | SERANA |
| SE113 | S P | E CLEARNIGHT + WATER (sea coast) | SERANA |
| SE114 | G S | E SUNNY | SER_VAMP |
| SE115 | S P | T | SER_VAMP; LUNA_SUNSPELL |
| SE116 | S K | E PREDAWN (exterior) | DG_END; SER_VAMP |
| SE117 | X S P | E SUMMER SUNNY | SER_CURED |
| SE118 | S I | E NIGHT (exterior) | SER_VAMP |
| SE119 | R S | T | SER_VAMP |
| SE120 | S P | E MORNING | SER_CURED |
| SE121 | I S | T | DG_END; SER_VAMP |
| SE122 | X S | T | DG_END; SER_VAMP |
| SE123 | S P | T | DG_END; SER_VAMP |
| SE124 | K S | T | DG_END; SER_VAMP |
| SE125 | R S | T | DG_END; SER_VAMP |
| SE126 | A S | T | DG_END; SER_VAMP; ASHE_REVEAL |
| SE127 | L S P | T | DG_END; SER_VAMP |
| SE128 | G S | T | SER_CURED; after SE28 |
| SE129 | V S | E CITY or HOUSE | SER_CURED |
| SE130 | I S | E RAIN | SER_CURED; after SE50 |
| SE131 | K S | E AFTERFIGHT (Serana hurt) | SER_CURED |
| SE132 | S P | E CLEARNIGHT | SER_CURED |
| SE133 | S P | E INN or HOUSE | SER_CURED |
| SE134 | C S | T | SER_CURED; after SE24 |
| SE135 | X S | E CAMP | after SE36 |
| SE136 | X S P | T | after SE135 |
| SE137 | R S X | E CAMP+NIGHT | after SE135 |
| SE138 | X S | E AFTERFIGHT:raisedcorpse | after SE36 |
| SE139 | S X | E CAMP | after SE49 and SE135 |
| SE140 | X S | T | SER_CURED; after SE135 |
| SE141 | X S | E AFTERFIGHT:argonian | SERANA |
| SE142 | X S P | E CAMP | after SE139 |
| SE143 | I S | T | SERANA |
| SE144 | I S | E INN | SERANA |
| SE145 | I S P | E WILD | SERANA |
| SE146 | I S | T | INIGO_BV |
| SE147 | I S | T | SERANA |
| SE148 | C S | T | SER_VAMP |
| SE149 | C S P | E AFTERFIGHT | SERANA |
| SE150 | C S P | T | RC_BIGPIG |
| SE151 | C S I | E INN | SERANA |
| SE152 | C S | E CAMP or INN | SER_CURED; after SE24 |
| SE153 | S P | T | S_COMP; NOT_S_KISS |
| SE154 | R S | T | S_COMP; NOT_S_KISS |
| SE155 | S I | T | S_KISS |
| SE156 | S P | E MORNING | S_KISS; not S_PANNE (soon after the kiss) |
| SE157 | G S | E CAMP | S_PANNE |
| SE158 | S P | E CAMP+NIGHT | S_PANNE |
| SE159 | S V P | T | S_KISS; DG_DURN |
| SE160 | S L | T | S_VALE |
| SE161 | S K | T | S_DETERM; DG_END |
| SE162 | S P | T | S_DETERM; DG_END |
| SE163 | C S | T | S_LOVE |
| SE164 | V S | T | S_COVENANT |
| SE165 | S I | T | S_TRUST |
| SE166 | S P | T | S_FRIENDTALK |
| SE167 | A S | T | S_BEACH; A_ANY; ASHE_REVEAL |
| SE168 | G S | T | S_ROMOFF; DG_CAIRN |
| SE169 | S K | E AFTERFIGHT:vampire | SERANA |
| SE170 | I S | E AFTERFIGHT:spider | SERANA |
| SE171 | G S | E AFTERFIGHT:vigilant | SER_VAMP |
| SE172 | S P | E AFTERFIGHT:bear | SER_CURED |
| SE173 | X S | E AFTERFIGHT:draugr | SERANA |
| SE174 | L S | E AFTERFIGHT:necromancer | SERANA |
| SE175 | C S | E AFTERFIGHT:wolf | SERANA |
| SE176 | V S | E AFTERFIGHT:slaughterfish | SERANA |
| SE177 | A S | E AFTERFIGHT:bandit | SER_VAMP; ASHE_REVEAL |
| SE178 | R S | E AFTERFIGHT:troll | SER_VAMP |
| SE179 | S K | E AFTERFIGHT:dragonpriest | SERANA |
| SE180 | S P | E AFTERFIGHT (player near death) | SERANA |

## Notes for the build
- Part 4 has two sides. SE121-SE127 need `DG_END` + `SER_VAMP` (she has not taken the cure yet); SE128-SE134 need `SER_CURED`. Lines are worded "not yet", so nothing contradicts a later cure.
- Part 7 is one talk per SDA romance step (S_COMP, S_KISS, S_PANNE, S_VALE, S_DETERM, S_LOVE, S_COVENANT, S_TRUST, S_FRIENDTALK, S_BEACH) plus one S_ROMOFF talk. Never fire them while any SDA_SeranaRomance quest is running (Serana's Free row already blocks this). Luna has no romance line anywhere: she is kind and dry, never promises, never says "I love you". SE163 talks about Serana saying it and never says what Luna answered.
- SE156 should fire soon after the kiss; "not S_PANNE" keeps it before the next step.
- Callbacks: SE86 needs SE41 (the song, "you'll cry"); SE92 needs SE74 (necromancer fight); SE94 needs SE47 (Clive scared); SE128 needs SE28 ("sword stays"); SE130 needs SE50 (two old friends in the rain); SE134 and SE152 need SE24 (first sweet roll); SE135-SE142 continue SE36 ("later, not in front of Remi") and SE49 (the formulae).
- SE110 mentions Brynjar, so it carries `BRYNJAR`. No Kaidan cult content anywhere.
- No "Dragonborn" anywhere in the file (Durnehviir's "qahnaarin" is used instead in SE159).
- Topics avoided on purpose: everything in 48 SERANA and the Serana talks in files 14b-57 (sunburn, hats, parasols, cure smells, nightmares, the Bannered Mare date, the beach date with Val, Valerica visits, the garden, Talonwood, the undercroft rats, the jetty, Molag Bal ceremony details).
