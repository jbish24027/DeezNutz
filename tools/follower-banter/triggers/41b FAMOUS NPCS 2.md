# Triggers - 41b FAMOUS NPCS 2 (prefix NP, 150 talks, NP121-NP270)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\41b FAMOUS NPCS 2.txt`. Written 2026-10-18.
Continues `triggers\41 FAMOUS NPCS.md` (NP1-NP120) and uses all of its codes (`TALKED:`, `NEAR:`, `HOUSE:`, `THANE:`, `ASHE_HIRED`, `ASHE_REVEAL`, `KAI_INIGO`, `KAI_LUC`, `XEL_LUC`, `LUC_INIGO`, `MS02`, `DA15` and so on). NPC base FormIDs read read-only through houseCARL `housecarl_records` (NPC_ records defined in Skyrim.esm / HearthFires.esm), epoch e2-509d9856becc0652. Nothing in the game, profile or mods folder was touched.

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C), plus **S = Serana, A = Ashe, U = Luna** (player line, Eleonora voice; no Free() test, but the player must be out of dialogue and menus).
Everything obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

## 1. File-wide rules (same as 41)
- `TALKED:<NPC>` fires within ~10 s of a Dialogue Menu closing on that NPC; `NEAR:<NPC>` = loaded, alive ref within 1000 units, polled on the 60 s tick and on cell change. Each talk once only.
- Low priority: a quest, place or romance talk eligible on the same event wins. At most one NP talk per NPC visit.
- **Kaidan never appears with Lydia, Vilkas or Farkas** (his own mod owns those). NP129, NP130 and NP142 are written without him, and NP142 also needs him not following.
- Nobody says "Dragonborn". Brynjar appears only in NP242 (`BRYNJAR`). No Kaidan cult, no Jo-Lee-as-father, no Fathis, no Mora, no Morvic outcome.
- Serana rows need her Free row (`SERANA_F`, 20 DAWNGUARD.md); vampire jokes add `SER_VAMP`. Ashe rows that mention what she is carry `ASHE_REVEAL`; the rest `ASHE_HIRED`. Respect Ashe's `bConfigVarIdles` toggle.
- "<A> and <B> own intro done" = the pair's intro scene in one of their own mods (Remi's HLIO*Banter, Xelzaz's BPUFXelzazAnd*Interactions, Lucien's JRLucien*, KaiandInigo stage >= 10).

## 2. New codes in this file
- `JARLNOW:<NPC>` (NEW) = that NPC is in `JobJarlFaction` (vanilla Skyrim.esm faction; the civil war moves Jarls in and out of it). Covers Vignar (Whiterun), Thongvor (Markarth), Brunwulf (Windhelm), Maven (Riften), Sorli (Morthal), Brina Merilis (Dawnstar), Kraldar (Winterhold), Dengeir (Falkreath). **[UNC: confirm JobJarlFaction is the faction the CW scripts swap; fallback = the hold's Jarl alias in the CW ownership quest]**
- `CW_END_IMP` / `CW_END_SONS`, `SERANA_F`, `SER_VAMP`, `GORE_READS` = as defined in `triggers\31 CIVIL WAR.md`, `20 DAWNGUARD.md` and `57 INNS AND TOWN LIFE.md`.
- `UTHGERD_BEATEN` (NEW) = Uthgerd's brawl won and her follower offer open (vanilla FavorUthgerd / brawl quest) **[UNC EditorID]**.
- `BRAITH_OPEN` (NEW) = the Lars/Braith bullying favour not yet completed **[UNC EditorID: vanilla Whiterun favour quest]**.
- `VAL_002` (NEW) = Val002 "He Runs a Tight Shipwreck" completed (AX ValSerano.esp).
- `DERKEETHUS_SAFE` (NEW) = Derkeethus rescued and back at Darkwater Crossing (vanilla Darkwater Pass favour) **[UNC EditorID/stage]**.
- `ALL_JARLS` (NEW) = the controller has seen `TALKED:` on each of the nine original Jarls at least once (Balgruuf, Elisif, Igmund, Ulfric, Laila, Siddgeir, Idgrod, Skald, Korir), kept as nine flags.
- `MG_JOIN`, `DB`, `BRYNJAR`, `GREYBEARDS`, `after:X`, `CITY:<Name>` = TRIGGERS.md section 4. `after NP14` / `after NP199` = that talk has played.
- Shop/location triggers (`in SolitudeTempleOfTheDivines`, `in WindhelmSadrisUsedWaresLocation`, `in MorthalThaumaturgistsHut`, `in WinterholdBirnasOddments`, `in FalkreathGraveConcoctions`, `in MarkarthSilverBloodInn`, `in FalkreathDeadMansDrink`, `in CollegeOfWinterholdArcanaeum`, `in BardsCollege`) = GetInCurrentLocation on that place **[UNC: location EditorIDs; look up the LCTN at build]**.
- Hearthfire houses: `HOUSE:LakeviewManor` / `WindstadManor` / `HeljarchenHall` with the housecarl's ref in the same cell (BYOH housecarl NPCs below).
- Hire offers (`TALKED:<hireling> (hire offer)`) = the hireling's dialogue closed while they are not following; no need to detect the exact line.

## 3. NPC base records used (new in this file; the rest are in 41's table)
| NPC | EditorID | FormID |
|---|---|---|
| Arcadia | Arcadia | 013BA4:Skyrim.esm |
| Ysolda | Ysolda | 013BAB:Skyrim.esm |
| Adrianne Avenicci | AdrianneAvenicci | 013BB9:Skyrim.esm |
| Eorlund Gray-Mane | EorlundGrayMane | 013B9D:Skyrim.esm |
| Lydia | HousecarlWhiterun | 0A2C8E:Skyrim.esm |
| Uthgerd the Unbroken | Uthgerd | 0918E2:Skyrim.esm |
| Jenassa | HirelingJenassa | 0B9982:Skyrim.esm |
| Braith | Braith | 013BA9:Skyrim.esm |
| Lars Battle-Born | LarsBattleBorn | 013BAF:Skyrim.esm |
| Dagny | Dagny | 01434B:Skyrim.esm |
| Frothar | Frothar | 01434C:Skyrim.esm |
| Danica Pure-Spring | DanicaPureSpring | 013BA5:Skyrim.esm |
| Torvar | Torvar | 01A6DB:Skyrim.esm |
| Njada Stonearm | NjadaStonearm | 01A6D9:Skyrim.esm |
| Athis | Athis | 01A6D5:Skyrim.esm |
| Vilkas | Vilkas | 01A694:Skyrim.esm |
| Idolaf Battle-Born | IdolafBattleBorn | 013BB2:Skyrim.esm |
| Mila Valentia | MilaValentia | 013BAD:Skyrim.esm |
| Balgruuf the Greater | BalgruuftheGreater | 013BBD:Skyrim.esm |
| Vignar Gray-Mane | VignarGrayMane | 013BB5:Skyrim.esm |
| Alvor | Alvor | 013475:Skyrim.esm |
| Sigrid | Sigrid | 013476:Skyrim.esm |
| Dorthe | Dorthe | 013477:Skyrim.esm |
| Gerdur | Gerdur | 01347C:Skyrim.esm |
| Frodnar | Frodnar | 01347E:Skyrim.esm |
| Hilde | Hilde | 035533:Skyrim.esm |
| Embry | Embry | 03550B:Skyrim.esm |
| Fralia Gray-Mane | FraliaGrayMane | 013B9C:Skyrim.esm |
| Proventus Avenicci | ProventusAvenicci | 013BBA:Skyrim.esm |
| Irileth | Irileth | 013BB8:Skyrim.esm |
| Farengar Secret-Fire | FarengarSecretFire | 013BBB:Skyrim.esm |
| Sybille Stentor | SybilleStentor | 0132AA:Skyrim.esm |
| Endarie | Endarie | 01326F:Skyrim.esm |
| Taarie | Taarie | 0132AB:Skyrim.esm |
| Jala | Jala | 01328C:Skyrim.esm |
| Evette San | EvetteSan | 013273:Skyrim.esm |
| Angeline Morrard | AngelineMorrard | 013260:Skyrim.esm |
| Rorlund | Rorlund | 0132A2:Skyrim.esm |
| Beirand | Beirand | 013261:Skyrim.esm |
| Minette Vinius | MinetteVinius | 01329B:Skyrim.esm |
| Ahtar | Ahtar | 01325F:Skyrim.esm |
| Captain Aldis | CaptainAldis | 041FB8:Skyrim.esm |
| Bolgeir Bearclaw | BolgeirBearclaw | 013264:Skyrim.esm |
| Belrand | HirelingBelrand | 0B9981:Skyrim.esm |
| Elisif the Fair | ElisifTheFair | 01326A:Skyrim.esm |
| Noster Eagle-Eye | NosterOneEye | 01329C:Skyrim.esm |
| Fihada | Fihada | 013275:Skyrim.esm |
| Giraud Gemane | GiraudGemane | 013281:Skyrim.esm |
| Viarmo | Viarmo | 0132AD:Skyrim.esm |
| Pantea Ateia | PanteaAteia | 01329F:Skyrim.esm |
| Raerek | Raerek | 0133B2:Skyrim.esm |
| Faleen | Faleen | 013397:Skyrim.esm |
| Moth gro-Bagol | MothgroBagol | 055A5E:Skyrim.esm |
| Ghorza gra-Bagol | GhorzaGraBagol | 01339A:Skyrim.esm |
| Bothela | Bothela | 01338B:Skyrim.esm |
| Muiri | Muiri | 01406B:Skyrim.esm |
| Hroki | Hroki | 01339E:Skyrim.esm |
| Lisbet | Lisbet | 0133A5:Skyrim.esm |
| Ainethach | Ainethach | 013B69:Skyrim.esm |
| Banning | Banning | 09A7A8:Skyrim.esm |
| Hogni Red-Arm | HogniRedArm | 0284AC:Skyrim.esm |
| Vorstag | HirelingVorstag | 0B997F:Skyrim.esm |
| Thongvor Silver-Blood | Thongvor | 0133BB:Skyrim.esm |
| Igmund | Igmund | 01339F:Skyrim.esm |
| Kerah | Kerah | 0133A2:Skyrim.esm |
| Jorleif | Jorleif | 014135:Skyrim.esm |
| Oengul War-Anvil | Oengul | 014142:Skyrim.esm |
| Sofie | BYOHUrchin_Sofie | 00403B:HearthFires.esm |
| Revyn Sadri | RevynSadri | 01413A:Skyrim.esm |
| Niranye | Niranye | 014123:Skyrim.esm |
| Rolff Stone-Fist | Rolff | 03EFE9:Skyrim.esm |
| Scouts-Many-Marshes | ScoutsManyMarshes | 01412E:Skyrim.esm |
| Nurelion | Nurelion | 014148:Skyrim.esm |
| Quintus Navale | QuintusNavale | 01414C:Skyrim.esm |
| Stenvar | HirelingStenvar | 0B9983:Skyrim.esm |
| Wuunferth the Unliving | Wuunferth | 014146:Skyrim.esm |
| Brunwulf Free-Winter | Brunwulf | 014149:Skyrim.esm |
| Ulfric Stormcloak | Ulfric | 01414D:Skyrim.esm |
| Galmar Stone-Fist | Galmar | 014128:Skyrim.esm |
| Dravynea the Stoneweaver | Dravynea | 01365F:Skyrim.esm |
| Annekke Crag-Jumper | Annekke | 013666:Skyrim.esm |
| Derkeethus | Derkeethus | 01403E:Skyrim.esm |
| Elgrim | Elgrim | 013357:Skyrim.esm |
| Hafjorg | Hafjorg | 013360:Skyrim.esm |
| Wylandriah | Wylandriah | 019DEF:Skyrim.esm |
| Dinya Balu | Dinya | 013352:Skyrim.esm |
| Maramal | Maramal | 01335B:Skyrim.esm |
| Runa Fair-Shield | Runa | 013378:Skyrim.esm |
| Marcurio | HirelingMarcurio | 0B9980:Skyrim.esm |
| Bolli | Bolli | 01334E:Skyrim.esm |
| Maven Black-Briar | Maven | 01336A:Skyrim.esm |
| Anuriel | Anuriel | 013349:Skyrim.esm |
| Unmid Snow-Shod | Unmid | 0371D7:Skyrim.esm |
| Narfi | Narfi | 0136C0:Skyrim.esm |
| Temba Wide-Arm | TembaWideArm | 0658D2:Skyrim.esm |
| Mjoll the Lioness | Mjoll | 01336B:Skyrim.esm |
| Laila Law-Giver | Laila | 013366:Skyrim.esm |
| Maul | Maul | 0371D6:Skyrim.esm |
| Lynly Star-Sung | Lynly | 0136BC:Skyrim.esm |
| Nenya | Nenya | 013659:Skyrim.esm |
| Lod | Lod | 013650:Skyrim.esm |
| Narri | Narri | 013654:Skyrim.esm |
| Tekla | Tekla | 013656:Skyrim.esm |
| Dengeir of Stuhn | Dengeir | 01365A:Skyrim.esm |
| Zaria (shop trigger is by location) | Zaria | 03A19A:Skyrim.esm |
| Rayya | BYOHHousecarlFalkreath | 005215:HearthFires.esm |
| Valdimar | BYOHHousecarlHjaalmarch | 00521B:HearthFires.esm |
| Gregor | BYOHHousecarlPale | 00521E:HearthFires.esm |
| Joric | Joric | 0135EE:Skyrim.esm |
| Idgrod the Younger | IdgrodTheYounger | 0135EC:Skyrim.esm |
| Idgrod Ravencrone | IdgrodRavencrone | 0135EB:Skyrim.esm |
| Aslfur | Aslfur | 0135E7:Skyrim.esm |
| Gorm | Gorm | 0135EA:Skyrim.esm |
| Benor | Benor | 0135E8:Skyrim.esm |
| Sorli the Builder | Sorli | 013606:Skyrim.esm |
| Brina Merilis | BrinaMerilis | 01A6B7:Skyrim.esm |
| Madena | Madena | 01361D:Skyrim.esm |
| Jod | Jod | 013618:Skyrim.esm |
| Horik Halfhand | HorikHalfhand | 01A6B9:Skyrim.esm |
| Rustleif | Rustleif | 01361E:Skyrim.esm |
| Seren | Seren | 01361F:Skyrim.esm |
| Beitild | Beitild | 013612:Skyrim.esm |
| Leigelf | Leigelf | 01361B:Skyrim.esm |
| Frida | Frida | 013614:Skyrim.esm |
| Skald the Elder | SkaldtheElder | 013620:Skyrim.esm |
| Malur Seloth | MalurSeloth | 01C182:Skyrim.esm |
| Kraldar | Kraldar | 01C180:Skyrim.esm |
| Korir | Korir | 01C188:Skyrim.esm |
| Assur | Assur | 01C18A:Skyrim.esm |
| Birna (shop only, by location) | Birna | 01C187:Skyrim.esm |
| Tolfdir | Tolfdir | 01C19E:Skyrim.esm |
| Urag gro-Shub | UraggroShub | 01C193:Skyrim.esm |
| Borgakh the Steel Heart | Borgakh | 019959:Skyrim.esm |
| Saadia | Saadia | 013BA2:Skyrim.esm |
| Kematu | MS08Kematu | 021601:Skyrim.esm |
| Esbern | Esbern | 013358:Skyrim.esm |
| Ralof | Ralof | 02BF9D:Skyrim.esm |
| Hadvar | Hadvar | 02BF9F:Skyrim.esm |
| Siddgeir (named in NP270 only) | Siddgeir | 013653:Skyrim.esm |

Several live winners are Requiem for the Indifferent.esp or Authoria output plugins; the trigger only needs the base FormID (GetFormFromFile on Skyrim.esm / HearthFires.esm), never a copy of those records.

## 4. Table

### PART 1 - WHITERUN HOLD
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP121 | X U | E TALKED:Arcadia (barter closed) | - |
| NP122 | R K | E TALKED:Arcadia | after B1 |
| NP123 | V R | E TALKED:Ysolda | - |
| NP124 | I U | E TALKED:Ysolda | - |
| NP125 | I U | E TALKED:Adrianne | - |
| NP126 | A K | E NEAR:Adrianne | ASHE_REVEAL |
| NP127 | R A | E NEAR:Eorlund (at the Skyforge) | ASHE_REVEAL; Remi following |
| NP128 | V K U | E TALKED:Eorlund | after A2 |
| NP129 | V R | E NEAR:Lydia | THANE:Whiterun; Kaidan not in the talk |
| NP130 | L X | E HOUSE:Breezehome with Lydia present | THANE:Whiterun; XEL_LUC |
| NP131 | G I | E TALKED:Uthgerd | after C2 |
| NP132 | G U | E TALKED:Uthgerd (follower offer after the brawl) | UTHGERD_BEATEN |
| NP133 | X V | E TALKED:Jenassa (hire offer) | after X4 |
| NP134 | A G | E NEAR:Jenassa | ASHE_HIRED |
| NP135 | K G | E NEAR:Braith | BRAITH_OPEN; after A1 |
| NP136 | L V U | E NEAR:Lars | after C1 |
| NP137 | C V | E NEAR:Dagny | after R8 |
| NP138 | G L | E NEAR:Frothar | after L1 |
| NP139 | K U | E TALKED:Danica | - |
| NP140 | G R | E NEAR:Torvar + NEAR:Njada (interior Jorrvaskr) | Gore and Remi own intro done |
| NP141 | V I | E TALKED:Athis | after I1 |
| NP142 | A V | E NEAR:Vilkas (interior or exterior Jorrvaskr) | ASHE_HIRED; Kaidan not following |
| NP143 | K L | E TALKED:Idolaf | KAI_LUC |
| NP144 | V C | E NEAR:Mila | after R8 |
| NP145 | X G | E TALKED:Balgruuf | after X1; not CW_END |
| NP146 | K G | E TALKED:Vignar or NEAR:Vignar in Dragonsreach | JARLNOW:Vignar; after A1 |
| NP147 | R K | E TALKED:Alvor | after B1 |
| NP148 | X C | E TALKED:Sigrid | after R18 |
| NP149 | C G | E NEAR:Dorthe | after R5 |
| NP150 | V I | E TALKED:Gerdur | after I1 |
| NP151 | G S | E NEAR:Frodnar | SERANA_F |
| NP152 | L U | E NEAR:Hilde | - |

### PART 2 - HAAFINGAR AND SOLITUDE
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP153 | X U | E TALKED:Sybille | - |
| NP154 | S U | E TALKED:Endarie | SERANA_F |
| NP155 | V A | E NEAR:Taarie | ASHE_HIRED |
| NP156 | K X | E NEAR:Jala (stall) | after C3 |
| NP157 | S V | E TALKED:Evette (barter closed) | SERANA_F |
| NP158 | L U | E TALKED:Angeline (daughter topic) | - |
| NP159 | R V U | E in SolitudeTempleOfTheDivines | Remi and Val own intro done |
| NP160 | I K | E NEAR:Rorlund | KAI_INIGO |
| NP161 | C L | E in SolitudeTempleOfTheDivines | after R11 |
| NP162 | K A U | E TALKED:Beirand (barter closed) | ASHE_HIRED |
| NP163 | G U | E NEAR:Minette | after A1 |
| NP164 | K X | E TALKED:Ahtar (hire offer) | after C3 |
| NP165 | I V | E TALKED:Aldis | VAL_002; after I1 |
| NP166 | R I | E NEAR:Bolgeir | after B6 |
| NP167 | V U | E TALKED:Belrand (hire offer) | - |
| NP168 | K U | E TALKED:Elisif or NEAR:Elisif in the Blue Palace | CW_END_IMP |

### PART 3 - THE REACH
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP169 | K X | E TALKED:Raerek | after C3 |
| NP170 | G A | E NEAR:Faleen | ASHE_HIRED |
| NP171 | G V | E TALKED:Moth | after A3 |
| NP172 | L G | E TALKED:Ghorza (book request) | GORE_READS; after L1 |
| NP173 | X U | E TALKED:Bothela | - |
| NP174 | I L | E NEAR:Muiri | LUC_INIGO |
| NP175 | V K U | E TALKED:Hroki | after A2 |
| NP176 | R L | E TALKED:Lisbet | after B10 |
| NP177 | K I | E TALKED:Ainethach | KAI_INIGO |
| NP178 | K C | E NEAR:Banning | after R1 |
| NP179 | C I | E NEAR:Hogni | after R13 |
| NP180 | R S | E NEAR:Vorstag (in MarkarthSilverBloodInn) | SERANA_F |
| NP181 | R L | E TALKED:Thongvor or NEAR:Thongvor in Understone Keep | JARLNOW:Thongvor; after B10 |
| NP182 | R I | E TALKED:Igmund | after B6 |

### PART 4 - EASTMARCH
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP183 | L K | E TALKED:Jorleif | KAI_LUC |
| NP184 | V G | E TALKED:Oengul (barter closed) | after A3 |
| NP185 | K S | E TALKED:Sofie | SERANA_F; Sofie not adopted |
| NP186 | R V | E in WindhelmSadrisUsedWaresLocation | Remi and Val own intro done |
| NP187 | I C | E NEAR:Niranye | after R13 |
| NP188 | G I | E NEAR:Rolff | after C2 |
| NP189 | X L | E TALKED:Scouts-Many-Marshes | XEL_LUC |
| NP190 | X U | E NEAR:Nurelion + NEAR:Quintus | White Phial quest not completed |
| NP191 | K G U | E TALKED:Stenvar (hire offer) | after A1 |
| NP192 | L A | E TALKED:Wuunferth | ASHE_HIRED; Blood on the Ice not completed |
| NP193 | X V | E TALKED:Brunwulf or NEAR:Brunwulf in the Palace of the Kings | JARLNOW:Brunwulf; after X4 |
| NP194 | K G U | E CITY:Windhelm | CW_END_SONS; after A1 |
| NP195 | U K | E TALKED:Dravynea | - |
| NP196 | K I | E TALKED:Annekke | KAI_INIGO |
| NP197 | R X | E NEAR:Derkeethus at Darkwater Crossing | DERKEETHUS_SAFE; Remi and Xelzaz not fallen out |

### PART 5 - THE RIFT
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP198 | X U | E NEAR:Elgrim + NEAR:Hafjorg | - |
| NP199 | L U | E TALKED:Wylandriah (lost items) | - |
| NP200 | R U | E TALKED:Dinya | - |
| NP201 | G I | E TALKED:Maramal | after C2 |
| NP202 | V U | E TALKED:Runa | - |
| NP203 | U L | E TALKED:Marcurio (hire offer) | - |
| NP204 | G X | E TALKED:Bolli | after X1 |
| NP205 | G R U | E TALKED:Maven or NEAR:Maven in Mistveil Keep | JARLNOW:Maven; Gore and Remi own intro done |
| NP206 | A V | E TALKED:Anuriel | ASHE_HIRED |
| NP207 | X I | E NEAR:Unmid | after X6 |
| NP208 | I U | E NEAR:Narfi | - |
| NP209 | G L | E TALKED:Temba (bear pelts) | after L1 |
| NP210 | I U | E NEAR:Maven | not JARLNOW:Maven (she is not yet Jarl) |
| NP211 | C I | E TALKED:Mjoll | after R13 |
| NP212 | I L | E TALKED:Laila | LUC_INIGO; not JARLNOW:Maven |

### PART 6 - FALKREATH, HJAALMARCH, THE PALE AND WINTERHOLD
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP213 | A V | E TALKED:Nenya | ASHE_HIRED |
| NP214 | K L U | E TALKED:Lod | KAI_LUC |
| NP215 | V L | E NEAR:Narri (in FalkreathDeadMansDrink) | after C1 |
| NP216 | K X | E TALKED:Dengeir or NEAR:Dengeir in the Falkreath longhouse | JARLNOW:Dengeir; after C3 |
| NP217 | G U | E HOUSE:LakeviewManor with Rayya present | - |
| NP218 | X U | E HOUSE:WindstadManor with Valdimar present | - |
| NP219 | C K | E HOUSE:HeljarchenHall with Gregor present | after R1 |
| NP220 | L I | E NEAR:Joric | LUC_INIGO |
| NP221 | A U | E TALKED:IdgrodTheYounger | ASHE_REVEAL |
| NP222 | R X | E in MorthalThaumaturgistsHut (Lami's shop) | Remi and Xelzaz not fallen out |
| NP223 | V S | E TALKED:Aslfur | SERANA_F |
| NP224 | G A | E TALKED:Benor (challenge) | ASHE_HIRED |
| NP225 | R C | E TALKED:Sorli or NEAR:Sorli in Highmoon Hall | JARLNOW:Sorli; after R1 |
| NP226 | L U | E TALKED:Brina or NEAR:Brina in the White Hall | JARLNOW:Brina |
| NP227 | R U | E TALKED:Madena | - |
| NP228 | C G | E NEAR:Horik | after R5 |
| NP229 | G I | E NEAR:Rustleif + NEAR:Seren (forge) | after C2 |
| NP230 | R V | E NEAR:Beitild or NEAR:Leigelf | Remi and Val own intro done |
| NP231 | V X | E TALKED:Malur | after X4 |
| NP232 | S U | E TALKED:Kraldar or NEAR:Kraldar in the Jarl's Longhouse | JARLNOW:Kraldar; SERANA_F |
| NP233 | V U | E TALKED:Korir | - |

### PART 7 - JARLS, HIRELINGS AND EVERYONE ELSE
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP234 | G I | E TALKED:Borgakh (follower offer) | after C2 |
| NP235 | K V | E TALKED:Kematu | In My Time of Need started, not completed; after A2 |
| NP236 | G K | E NEAR:Maul | after A1 |
| NP237 | L U | E TALKED:Giraud (lesson) | - |
| NP238 | S U | E NEAR:Balgruuf + NEAR:Dagny or NEAR:Frothar | SERANA_F |
| NP239 | C X | E TALKED:Ulfric | DB; R18 Xelzaz-Redcap apology done |
| NP240 | A U | E TALKED:Elisif | ASHE_REVEAL |
| NP241 | R K | E NEAR:Fralia (market stall) | Missing in Action not completed; after B1 |
| NP242 | L K | E NEAR:Noster | BRYNJAR; KAI_LUC |
| NP243 | X I | E TALKED:Frida (barter closed) | after X6 |
| NP244 | G R | E TALKED:Lynly | Gore and Remi own intro done |
| NP245 | C K | E NEAR:Proventus | after NP14; after R1 |
| NP246 | C V | E NEAR:Irileth | after R8 |
| NP247 | C U | E TALKED:Farengar | - |
| NP248 | A U | E TALKED:Tolfdir or NEAR:Tolfdir | ASHE_REVEAL; MG_JOIN |
| NP249 | S L | E NEAR:Urag in CollegeOfWinterholdArcanaeum | SERANA_F; MG_JOIN |
| NP250 | L U | E NEAR:Esbern in SkyHavenTempleLocation | MQ204 started |
| NP251 | L I | E TALKED:Viarmo | LUC_INIGO |
| NP252 | K I | E TALKED:Ralof | DB; KAI_INIGO |
| NP253 | L G | E TALKED:Hadvar | after L1 |
| NP254 | C L | E TALKED:Idgrod | after R11 |
| NP255 | X G | E TALKED:Skald | after X1 |
| NP256 | G U | E TALKED:Adrianne | Gore following |
| NP257 | G I | E NEAR:Tekla | after C2 |
| NP258 | R K | E NEAR:Assur | after B1 |
| NP259 | S K | E NEAR:Gorm | SERANA_F; SER_VAMP |
| NP260 | V U | E TALKED:Jod | - |
| NP261 | C R | E in WinterholdBirnasOddments | after R1 (Remi-Redcap own intro done) |
| NP262 | R U | E TALKED:Wylandriah (Remi following) | after NP199 |
| NP263 | V G | E TALKED:Fihada (barter closed) | after A3 |
| NP264 | S I | E NEAR:Embry | SERANA_F |
| NP265 | R L | E in FalkreathGraveConcoctions (Zaria's shop) | after B10 |
| NP266 | V S | E TALKED:Kerah (barter closed) | SERANA_F; SER_VAMP |
| NP267 | K L | E NEAR:Pantea in BardsCollege | KAI_LUC |
| NP268 | G A | E TALKED:Galmar | ASHE_HIRED; after A1 |
| NP269 | A U | E TALKED:Sybille | ASHE_REVEAL |
| NP270 | L K U | T | ALL_JARLS; KAI_LUC |
