# Triggers - 41 FAMOUS NPCS (prefix NP, 120 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\41 FAMOUS NPCS.txt`
NPC FormIDs read-only through houseCARL (`housecarl_records`, NPC_ records defined in Skyrim.esm / HearthFires.esm), epoch e2-582cd110870e529e, 2026-10-18. All base records below are confirmed by EditorID + name.

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C), plus **S = Serana, A = Ashe, U = Luna** (player line, Eleonora voice; no Free() test).
Gate codes as TRIGGERS.md section 4. Codes used only in this file are defined below.

## Event codes for this file

- `TALKED:<NPC>` = the player has just closed a Dialogue Menu whose speaker's base is that NPC (controller watches `MenuClose "Dialogue Menu"` and remembers the last dialogue target; fire within ~10 s, WorldQuiet and Free() still apply). A note in brackets narrows it (first time, a topic, barter closed) — build as a per-talk flag or the quest stage named in the gate.
- `NEAR:<NPC>` = a loaded, enabled, alive reference of that NPC within 1000 units of the player, player not in dialogue. `NEAR:A + NEAR:B` = both. Poll on the 60 s tick and on cell change; each NEAR talk once only.
- `HOUSE:<House> with <Housecarl> present` = player in that house's location and the housecarl's ref is in the same cell. Houses: Breezehome (WhiterunBreezehomeLocation), Proudspire, Vlindrel Hall, Hjerim, Honeyside.
- `CITY:<Name>`, `HELGEN_LOC`, `HOUSE` as TRIGGERS.md.
- Leaving Cidhna Mine (NP65) = OnLocationChange from CidhnaMineLocation to Markarth.

## Gate codes for this file

- `THANE:<Hold>` = player is Thane of that hold. **[UNCONFIRMED: use the vanilla Thane flag for each hold, i.e. the hold's `FavorJarlsMakeFriends` stage / housecarl alias filled, or the player in the hold's Thane faction; look up at build]**. `THANE count >= 5` = five or more of those true.
- `ASHE_HIRED`, `ASHE_REVEAL` as ashe.md section 6 (MM_AsheIntro completed; MM_FriendshipQuest var MM_AutomatonReveal == 1). Ashe following = `MM_AsheMentalModel ::IsFollowing_var == 1`.
- `SERANA` as TRIGGERS.md (DLC1VQ02 done) plus Serana following (`DLC1NPCMentalModel ::IsFollowing_var == 1`). NP107 also needs Serana still a vampire (`HasKeyword Vampire 0A82BB` on her).
- `KAI_INIGO` = KaiandInigo 000842:Kaidan and Inigo Meet.esp stage >= 10.
- `KAI_LUC` = Lucien's own Kaidan intro has played (JRLucienFollowerKaidanScene1 in JRLucienFollower 00591E:Lucien.esp) **[UNCONFIRMED flag; fallback: both following, any time]**.
- `XEL_LUC` = Xelzaz's own Lucien intro done (BPUFXelzazAndLucienInteractions 077DC4:BPUFXelzazFollower.esp, first stage done) **[UNCONFIRMED stage]**.
- `LUC_INIGO` = JRLucienInigoRank 7638C2:Lucien.esp >= 2.
- `HELGEN; escaped with Hadvar / Ralof` = which side the player followed in MQ101 **[UNCONFIRMED: the MQ101 branch stage or the MQ102A/MQ102B split; check at build]**. NP44 also needs the player to have gone through the real Helgen intro (no alternate start), i.e. `AP_StartCellQ` did not skip MQ101.
- `Missing in Action` = the Gray-Mane quest (Thorald) **[UNCONFIRMED EditorID]**; NP38 needs it completed with Thorald (ThoraldGrayMane 01C241) alive.
- `Grimsever returned`, `Kharjo's amulet returned` **[UNCONFIRMED quest EditorIDs]**.
- `MS02` = No One Escapes Cidhna Mine (Madanach met = an early stage **[UNCONFIRMED stage]**; NP66 = completed, any branch).
- `DA15` The Mind of Madness, `DA16` Waking Nightmare, `DA11` The Taste of Death (Verulus), `TG06` Speaking With Silence, `MQ204` Alduin's Wall — vanilla EditorIDs; stage use as stated.
- `not adopted` = Lucia (03003F5F) not yet adopted (BYOHRelationshipAdoption).
- `Kaidan not following` / `Kaidan not in the talk`: the Farkas and Brynjolf talks must never play with Kaidan in the party (his own mod owns those relationships).

## NPC base records used

| NPC | EditorID | FormID |
|---|---|---|
| Balgruuf the Greater | BalgruuftheGreater | 013BBD:Skyrim.esm |
| Hrongar | Hrongar | 013BBC:Skyrim.esm |
| Proventus Avenicci | ProventusAvenicci | 013BBA:Skyrim.esm |
| Irileth | Irileth | 013BB8:Skyrim.esm |
| Farengar Secret-Fire | FarengarSecretFire | 013BBB:Skyrim.esm |
| Lydia | HousecarlWhiterun | 0A2C8E:Skyrim.esm |
| Nazeem | Nazeem | 013BBF:Skyrim.esm |
| Ahlam | Ahlam | 013BBE:Skyrim.esm |
| Belethor | Belethor | 013BA1:Skyrim.esm |
| Carlotta Valentia | CarlottaValentia | 013B99:Skyrim.esm |
| Mikael | Mikael | 01A670:Skyrim.esm |
| Hulda | Hulda | 013BA3:Skyrim.esm |
| Uthgerd the Unbroken | Uthgerd | 0918E2:Skyrim.esm |
| Heimskr | Heimskr | 013BAC:Skyrim.esm |
| Ysolda | Ysolda | 013BAB:Skyrim.esm |
| Olava the Feeble | OlavatheFeeble | 013BAE:Skyrim.esm |
| Adrianne Avenicci | AdrianneAvenicci | 013BB9:Skyrim.esm |
| Ulfberth War-Bear | Ulfberth | 013B9F:Skyrim.esm |
| Lucia | BYOHUrchin_Lucia | 003F5F:HearthFires.esm |
| Danica Pure-Spring | DanicaPureSpring | 013BA5:Skyrim.esm |
| Eorlund Gray-Mane | EorlundGrayMane | 013B9D:Skyrim.esm |
| Avulstein Gray-Mane | AvulsteinGrayMane | 013B9A:Skyrim.esm |
| Thorald Gray-Mane | ThoraldGrayMane | 01C241:Skyrim.esm |
| Ria | Ria | 01A6D7:Skyrim.esm |
| Aela the Huntress | AelaTheHuntress | 01A696:Skyrim.esm |
| Vilkas | Vilkas | 01A694:Skyrim.esm |
| Farkas | Farkas | 01A692:Skyrim.esm |
| Haming (Helgen boy, named only) | Haming | 013642:Skyrim.esm |
| Hadvar | Hadvar | 02BF9F:Skyrim.esm |
| Ralof | Ralof | 02BF9D:Skyrim.esm |
| Camilla Valerius | CamillaValerius | 01347B:Skyrim.esm |
| Lucan Valerius | LucanValerius | 01347A:Skyrim.esm |
| Sven | Sven | 01347F:Skyrim.esm |
| Elisif the Fair | ElisifTheFair | 01326A:Skyrim.esm |
| Falk Firebeard | FalkFirebeard | 013274:Skyrim.esm |
| Bryling | Bryling | 013265:Skyrim.esm |
| Sybille Stentor | SybilleStentor | 0132AA:Skyrim.esm |
| General Tullius | GeneralTullius | 01327E:Skyrim.esm (battle copy CWBattleTullius 0D0577) |
| Legate Rikke | Rikke | 0132A1:Skyrim.esm (battle copy 0D0573) |
| Viarmo | Viarmo | 0132AD:Skyrim.esm |
| Erikur | Erikur | 013272:Skyrim.esm |
| Vittoria Vici | VittoriaVici | 01327A:Skyrim.esm |
| Jordis the Sword-Maiden | HousecarlSolitude | 0A2C8F:Skyrim.esm |
| Roggvir | Roggvir | 0A3BDB:Skyrim.esm |
| Igmund | Igmund | 01339F:Skyrim.esm |
| Ondolemar | Ondolemar | 0133AF:Skyrim.esm |
| Thonar Silver-Blood | Thonar | 0133BA:Skyrim.esm |
| Madanach | Madanach | 0133A7:Skyrim.esm |
| Calcelmo | Calcelmo | 01338E:Skyrim.esm |
| Aicantar | Aicantar | 01402E:Skyrim.esm |
| Brother Verulus | BrotherVerulus | 01338C:Skyrim.esm |
| Argis the Bulwark | HousecarlMarkarth | 0A2C8C:Skyrim.esm |
| Ulfric Stormcloak | Ulfric | 01414D:Skyrim.esm (battle copy CWBattleUlfric 0D0575) |
| Galmar Stone-Fist | Galmar | 014128:Skyrim.esm (battle copy 0D0570) |
| Brunwulf Free-Winter | Brunwulf | 014149:Skyrim.esm |
| Viola Giordano | ViolaGiordano | 014129:Skyrim.esm |
| Calder | HousecarlWindhelm | 0A2C90:Skyrim.esm |
| Ri'saad / Ma'dran / Ahkari (caravan leaders) | Risaad / Madran / Ahkari | 01B1DB / 01B1D1 / 01B1D6:Skyrim.esm |
| Kharjo | Kharjo | 01B1D2:Skyrim.esm |
| M'aiq the Liar | MaiqTheLiar | 0954BF:Skyrim.esm |
| Maven Black-Briar | Maven | 01336A:Skyrim.esm |
| Ingun Black-Briar | Ingun | 013364:Skyrim.esm |
| Sibbi Black-Briar | Sibbi | 01337B:Skyrim.esm |
| Laila Law-Giver | Laila | 013366:Skyrim.esm |
| Brynjolf | Brynjolf | 01B07D:Skyrim.esm |
| Mercer Frey | MercerFrey | 01B07C:Skyrim.esm |
| Mjoll the Lioness | Mjoll | 01336B:Skyrim.esm |
| Aerin | Aerin | 013346:Skyrim.esm |
| Constance Michel | ConstanceMichel | 013350:Skyrim.esm |
| Talen-Jei | TalenJei | 013373:Skyrim.esm |
| Wujeeta | Wujeeta | 013382:Skyrim.esm |
| Iona | HousecarlRiften | 0A2C91:Skyrim.esm |
| Klimmek | Klimmek | 0136C2:Skyrim.esm |
| Siddgeir | Siddgeir | 013653:Skyrim.esm |
| Dengeir of Stuhn | Dengeir | 01365A:Skyrim.esm |
| Idgrod Ravencrone | IdgrodRavencrone | 0135EB:Skyrim.esm |
| Falion | Falion | 0135E9:Skyrim.esm |
| Lurbuk | Lurbuk | 01AA63:Skyrim.esm |
| Skald the Elder | SkaldtheElder | 013620:Skyrim.esm |
| Korir | Korir | 01C188:Skyrim.esm |
| Tolfdir | Tolfdir | 01C19E:Skyrim.esm |
| Urag gro-Shub | UraggroShub | 01C193:Skyrim.esm |
| J'zargo | Jzargo | 01C195:Skyrim.esm |
| Arngeir | Arngeir | 02C6C7:Skyrim.esm |
| Delphine | Delphine | 013478:Skyrim.esm |
| Esbern | Esbern | 013358:Skyrim.esm |
| Sheogorath (DA15) | DA15Sheogorath | 02AC69:Skyrim.esm (named only) |

Several live winners are Requiem for the Indifferent.esp or Authoria output plugins; the trigger only needs the base FormID (GetFormFromFile on Skyrim.esm / HearthFires.esm), never a copy of those records.

Covered elsewhere on purpose (no talk here): Paarthurnax, Cicero, Babette, Astrid, the Gourmet, Barbas, Ancano, Karliah, Savos Aren, Enthir, Mirabelle, Kodlak, and Farengar's Dragonstone errand. Kaidan's own mod owns his Brynjolf/Ulfric jealousy and his Farkas/Vilkas/Aela/Lydia/Mjoll/Sven/Erik scenes; Remi and Xelzaz's gossip owns Nazeem, Elisif, Belethor, Mikael, Sven/Faendal, Brynjolf and the others in remiel.md, so none of those angles are reused with that pair.

## Table

### PART 1 - WHITERUN HOLD
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP1 | V G U | E TALKED:Balgruuf | - |
| NP2 | R K | E NEAR:Proventus + NEAR:Hrongar | - |
| NP3 | K X | E TALKED:Hrongar | - |
| NP4 | I V | E TALKED:Irileth | after V-I meet (I1) |
| NP5 | A K | E NEAR:Irileth | ASHE_HIRED |
| NP6 | K X | E NEAR:Irileth | DB |
| NP7 | L G | E TALKED:Proventus | - |
| NP8 | X U | E TALKED:Proventus | after NP7 |
| NP9 | R G | E NEAR:Farengar | Gore and Remi both following |
| NP10 | L U | E TALKED:Farengar (first time) | - |
| NP11 | R U | E TALKED:Farengar | DB; after NP10 |
| NP12 | G U K | E TALKED:Balgruuf (Thane ceremony) | DB; THANE:Whiterun |
| NP13 | G U | E Lydia joins as follower (first time) | THANE:Whiterun |
| NP14 | C R | E NEAR:Lydia | THANE:Whiterun |
| NP15 | L X | E HOUSE:Breezehome with Lydia resident | THANE:Whiterun |
| NP16 | V R U | E HOUSE:Breezehome with Lydia present | THANE:Whiterun |
| NP17 | K G U | E TALKED:Nazeem (his greeting) | - |
| NP18 | I V | E NEAR:Nazeem | after NP17 |
| NP19 | A G | E NEAR:Nazeem in WhiterunCloudDistrict | ASHE_HIRED |
| NP20 | K V | E NEAR:Ahlam + NEAR:Nazeem | after NP17 |
| NP21 | U I | E TALKED:Nazeem | THANE:Whiterun; after NP17 |
| NP22 | C V | E TALKED:Belethor | after R8 |
| NP23 | L U | E TALKED:Belethor (barter menu closed) | - |
| NP24 | V U | E TALKED:Carlotta | - |
| NP25 | A K | E TALKED:Mikael | ASHE_HIRED |
| NP26 | G I | E TALKED:Hulda | after C2 |
| NP27 | G K | E TALKED:Uthgerd | after A1 |
| NP28 | G K | E NEAR:Heimskr (preaching) | after A1 |
| NP29 | I X | E NEAR:Heimskr | after X6 |
| NP30 | K V | E TALKED:Ysolda (tusk request) | after A2 |
| NP31 | R I U | E TALKED:Olava | after B6 |
| NP32 | G K U | E TALKED:Adrianne | after A1 |
| NP33 | C I | E NEAR:Ulfberth | after R13 |
| NP34 | K C | E TALKED:Lucia | not adopted (BYOHRelationshipAdoption); after R1 |
| NP35 | R L | E TALKED:Lucia or NEAR:Lucia | not adopted; after NP34 |
| NP36 | X U | E TALKED:Danica | - |
| NP37 | K U | E NEAR:Avulstein or NEAR:Eorlund | Missing in Action not completed |
| NP38 | R G | E CITY:Whiterun | Missing in Action completed, Thorald alive |
| NP39 | G I | E TALKED:Ria | after C2 |
| NP40 | A V | E NEAR:Aela | ASHE_HIRED |
| NP41 | G V | E TALKED:Aela | after A3 |
| NP42 | L G | E NEAR:Vilkas (sitting, interior Jorrvaskr) | after L1 |
| NP43 | L I | E TALKED:Farkas | Kaidan not following |
| NP44 | U G | E HELGEN_LOC | HELGEN; Luna came through the Helgen attack (not an alternate start) |
| NP45 | K U | E TALKED:Hadvar | HELGEN; escaped with Hadvar |
| NP46 | V U | E TALKED:Ralof | HELGEN; escaped with Ralof |
| NP47 | K V | E TALKED:Camilla | after A2 |
| NP48 | R L | E TALKED:Lucan (Golden Claw topic) | after B10 |
| NP49 | C L | E NEAR:Sven (performing) | after R11 |

### PART 2 - HAAFINGAR AND SOLITUDE
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP50 | L U | E TALKED:Elisif (Elisif's Tribute given) | - |
| NP51 | V K | E NEAR:Elisif + NEAR:Falk | after A2 |
| NP52 | A R | E NEAR:Falk + NEAR:Bryling | ASHE_REVEAL |
| NP53 | S G | E NEAR:Sybille | SERANA |
| NP54 | L K | E TALKED:Tullius | KAI_LUC |
| NP55 | G U | E NEAR:Tullius | after A1 (Gore following) |
| NP56 | I G | E TALKED:Rikke | after C2 |
| NP57 | G V | E TALKED:Viarmo | after A3 |
| NP58 | K X | E TALKED:Erikur or NEAR:Erikur | after C3 |
| NP59 | L V | E NEAR:Vittoria | after C1 |
| NP60 | R K | E HOUSE:Proudspire with Jordis present | THANE:Haafingar; after B1 |
| NP61 | I U | E CITY:Solitude after Roggvir's execution scene ends (Roggvir dead) | - |

### PART 3 - THE REACH
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP62 | K U | E TALKED:Igmund | - |
| NP63 | R K | E NEAR:Ondolemar | after B1 |
| NP64 | R L | E TALKED:Thonar | after B10 |
| NP65 | I K | E leaving CidhnaMineLocation | MS02 Madanach met [UNCONFIRMED stage]; KAI_INIGO [CHECK] |
| NP66 | K X U | T | MS02 completed (any branch) |
| NP67 | R U L | E TALKED:Calcelmo | after B10 |
| NP68 | C R | E in MarkarthDwemerMuseum (or NEAR:Calcelmo) | after R1; Remi following |
| NP69 | V R | E NEAR:Aicantar | - |
| NP70 | R U | E TALKED:Verulus | Verulus alive; DA11 not running |
| NP71 | L G | E HOUSE:VlindrelHall with Argis present | THANE:Reach; after L1 |

### PART 4 - EASTMARCH, THE CARAVANS AND THE ROADS
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP72 | K G U | E TALKED:Ulfric (first time) | after A1 |
| NP73 | X V | E CITY:Windhelm after TALKED:Ulfric | after X4 |
| NP74 | S I | E TALKED:Ulfric | SERANA |
| NP75 | C L | E NEAR:Galmar | after R11 |
| NP76 | G K | E TALKED:Galmar | after A1 |
| NP77 | V G | E TALKED:Brunwulf | after A3 |
| NP78 | R U | E TALKED:Viola | - |
| NP79 | C G | E HOUSE:Hjerim with Calder present | THANE:Eastmarch; after R5 |
| NP80 | I U | E NEAR:Ri'saad or NEAR:Ma'dran or NEAR:Ahkari (caravan camp, exterior) | - |
| NP81 | V I | E TALKED:Ri'saad or Ma'dran or Ahkari (barter closed) | after I1 |
| NP82 | G I | E TALKED:Kharjo | after C2 |
| NP83 | I U | E TALKED:Kharjo | Kharjo's amulet returned [UNCONFIRMED quest EditorID]; after NP82 [CHECK] |
| NP84 | X I | E TALKED:Ri'saad or Ma'dran or Ahkari (barter closed) | after X6 |
| NP85 | L U C | E TALKED:M'aiq (first time) | - |
| NP86 | I V | E TALKED:M'aiq | after NP85; different hold from the first meeting |

### PART 5 - THE RIFT
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP87 | G K | E TALKED:Maven | after A1 |
| NP88 | V A | E NEAR:Maven | ASHE_HIRED |
| NP89 | X V | E TALKED:Ingun | after X4 |
| NP90 | L X | E TALKED:Laila | XEL_LUC |
| NP91 | L I | E NEAR:Brynjolf (market stall scene) | Kaidan not in the talk |
| NP92 | C G | E TALKED:Brynjolf | after R5 |
| NP93 | V R | E NEAR:Mercer | TG_JOIN; TG06 not started |
| NP94 | R G | E TALKED:Mjoll (Grimsever topic) | Gore and Remi both following |
| NP95 | L U | E NEAR:Mjoll | - |
| NP96 | R U | E TALKED:Mjoll | Grimsever returned [UNCONFIRMED quest EditorID]; after NP94 [CHECK] |
| NP97 | V S | E NEAR:Aerin + NEAR:Mjoll | SERANA |
| NP98 | I G | E NEAR:Constance | after C2 |
| NP99 | K X | E TALKED:Talen-Jei | after C3 |
| NP100 | X I | E TALKED:Wujeeta | after X6 |
| NP101 | L I | E NEAR:Sibbi | LUC_INIGO |
| NP102 | L K | E HOUSE:Honeyside with Iona present | THANE:Rift; KAI_LUC |
| NP103 | G L | E TALKED:Klimmek | after L1 |

### PART 6 - FALKREATH, HJAALMARCH, THE PALE AND WINTERHOLD
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP104 | K V U | E TALKED:Siddgeir | after A2 |
| NP105 | L K | E TALKED:Dengeir | KAI_LUC |
| NP106 | L U | E TALKED:Idgrod | - |
| NP107 | S U | E TALKED:Falion | SERANA; Serana HasKeyword Vampire == 1 |
| NP108 | X G | E NEAR:Lurbuk (performing) | after X1 |
| NP109 | R K | E TALKED:Skald | DA16 (Waking Nightmare) not completed; after B1 |
| NP110 | K U | E TALKED:Korir | - |
| NP111 | I U | E TALKED:Tolfdir | MG_JOIN |
| NP112 | L U | E TALKED:Urag | MG_JOIN |
| NP113 | C R | E TALKED:J'zargo | MG_JOIN; after R1; Remi following |

### PART 7 - THE GREYBEARDS, THE BLADES AND EVERYWHERE ELSE
| ID | Speakers | Type | Gates |
|---|---|---|---|
| NP114 | K L | E TALKED:Arngeir | GREYBEARDS; KAI_LUC |
| NP115 | A U | E TALKED:Arngeir | GREYBEARDS; ASHE_REVEAL |
| NP116 | V K | E in RiverwoodSleepingGiantInn | DELPHINE; after A2 |
| NP117 | X U | E NEAR:Esbern in SkyHavenTempleLocation | MQ204 started (Esbern at Sky Haven) |
| NP118 | C L | T | DA15 completed; after R11 |
| NP119 | V U G | E HOUSE (any) | THANE count >= 5; after A3 |
| NP120 | G L U | E NEAR:any inn bard (performing) | DB; after L1 |
