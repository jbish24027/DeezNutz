# 40 PLACES AND LANDMARKS - trigger rows (prefix PL, 180 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\40 PLACES AND LANDMARKS.txt`.

Sources: TRIGGERS.md sections 2-4, `research\triggers\vanilla_gates.md` B2, `research\bibles\*.md`, and the gate codes already defined in `triggers\20 DAWNGUARD.md`, `35 COLLEGE OF WINTERHOLD.md` and `15 MISSIVES BOUNTIES INTERESTING NPCS.md`. Location EditorIDs and FormIDs were read read-only from the live load order with houseCARL (LCTN records defined in Skyrim.esm and Dawnguard.esm; parent holds checked). Everything obeys TRIGGERS.md section 2 (`WorldQuiet`) and section 3 (`Free`), plus the Serana and Ashe Free rows in `20 DAWNGUARD.md` section 1. **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, U Luna (the player, Eleonora voice; no Free check, but the player must not be in dialogue).

## 1. How these fire

- `E arrival:<Location>` = the controller's `OnLocationChange` on the player, test `GetInCurrentLoc <Location> == 1` (or `IsChild` of it for sub-locations). Wait about 5 s after the change so the party has caught up, then run `WorldQuiet()` and `Free()` as usual.
- `FIRST` = the controller keeps one "visited" bit per location in this table, set the first time the player enters it. A FIRST talk plays on that first entry; if it was blocked (quiet window, a speaker missing) it stays eligible on later entries until it plays once. The lines are written as "first time here".
- `any visit` = location matches and the talk has not played, whatever the visited bit says.
- A second talk at the same place carries `after:<ID>`; the 300 s cooldown keeps two talks apart within one visit.
- All locations are vanilla Skyrim.esm unless the row says otherwise. Where a hold could not be confirmed, the place sits in Part 9.

## 2. Gate codes used here

Existing (TRIGGERS.md section 4 and the files named above): `HELGEN` (MQ101 145 done), `BRYNJAR`, `K_CRUSH`, `K_TOG+`, `K_MAR`, `G_TOG+`, `V_FLIRT`, `GORE_BAIL`, `VAL_FATHER`, `REMI_MORVIC`, `SERANA` (DLC1VQ02 5 done, and her Free row), `ASHE_HIRED` (MM_AsheIntro 0A7946 completed), `ASHE_REVEAL` (MM_FriendshipQuest 1A9DEE stage 70 or MM_AutomatonReveal == 1), `ASHE_Q1` (MM_AMQ_01 756FEA completed), `A_CRUSH` (MM_RM >= 4 and MM_AsheRomance == 0), `KAI_INIGO` (KaiandInigo 000842:Kaidan and Inigo Meet.esp stage >= 10).

New in this file:
- `RX_OK` = Remi and Xelzaz not mid falling-out: NOT (BPUFXelzazRemielFallingOut 5E67BB:BPUFXelzazFollower.esp stage 11 done and 13 not done). Same rule as TRIGGERS.md section 3, repeated because these talks are Remi plus Xelzaz.
- `CX_OK` = Redcap and Xelzaz past their own apology scene, the same gate as batch-2 talk R18 (BPUFXelzazAndRedcapInteractions apology stage **[UNC, see TRIGGERS.md section 6]**). Fallback: `after:R18`.
- `after:P2`, `after:P11` (batch 3 city talks), `after:R10` (batch 2 "Twenty Yards", the Val-threw-a-Riekling callback), `after:MG1` (College file "Five Houses and a Jarl"), `after:B1` (Remi meets Kaidan).
- Mammoth graveyards, the hot springs, Narfi's house, the Dawnstar shore and the three caravan leaders have no Location record of their own. Use a distance check from the player to a reference (an XMarker placed at build, or the caravan leader's actor ref) in the 60 s poll. All marked **[UNC]**.
- Silence: nothing new. Ustengrav, the Throat of the World and the Thalmor Embassy are already covered by the main-quest windows in TRIGGERS.md section 2; the Embassy talks are exterior-only.

## 3. Table

### Part 1 - Whiterun Hold

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL1 | K R | E arrival:RiverwoodLocation 013163:Skyrim.esm | after:B1 |
| PL2 | K G U | E arrival:RiverwoodLocation 013163:Skyrim.esm | K_MAR; after:P11; any visit |
| PL3 | C I U | E arrival:AnisesCabinLocation 0D9537:Skyrim.esm | FIRST |
| PL4 | K G U | E arrival:RoriksteadLocation 018A47:Skyrim.esm | FIRST |
| PL5 | I K U | E arrival:RoriksteadLocation 018A47:Skyrim.esm | K_TOG+; after:PL4; any visit |
| PL6 | K V U | E arrival:SilentMoonsCampLocation 0192A9:Skyrim.esm | FIRST |
| PL7 | V G U | E arrival:ValtheimKeepLocation 0192C1:Skyrim.esm | FIRST |
| PL8 | X V | E arrival:RedoransRetreatLocation 019295:Skyrim.esm | FIRST |
| PL9 | G X U | E arrival:WhiterunHonningbrewMeaderyLocation 0DAB88:Skyrim.esm | FIRST |
| PL10 | L I U | E arrival:PelagiaFarmLocation 018E3F:Skyrim.esm | FIRST |
| PL11 | G L U | E arrival:BleakwindBasinLocation 018EEB:Skyrim.esm | FIRST |
| PL12 | G S | E arrival:GuldunRockLocation 01918E:Skyrim.esm | FIRST; SERANA |
| PL13 | C I U | E arrival:SleepingTreeCampLocation 0192AD:Skyrim.esm | FIRST |
| PL14 | G X | E arrival:SleepingTreeCampLocation 0192AD:Skyrim.esm | after:PL13; any visit |
| PL15 | L V | E arrival:FortGreymoorLocation 01917D:Skyrim.esm | FIRST |
| PL16 | L C | E arrival:mammoth graveyard on the Whiterun tundra (unmarked, no LCTN): player within ~1500 units of a placed XMarker [UNC] | FIRST |
| PL17 | R V U | E arrival:HaltedStreamCampLocation 019193:Skyrim.esm | FIRST |
| PL18 | A G | E arrival:WhitewatchTowerLocation 0E66A0:Skyrim.esm | FIRST; ASHE_HIRED |
| PL19 | R L | E arrival:SwindlersDenLocation 018EE2:Skyrim.esm | FIRST |
| PL20 | K V | E arrival:SilentMoonsCampLocation 0192A9:Skyrim.esm | K_TOG+; after:PL6; any visit |

### Part 2 - Falkreath Hold

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL21 | G K U | E arrival:FalkreathCemeteryLocation 0200BB:Skyrim.esm | FIRST; BRYNJAR |
| PL22 | L C U | E arrival:FalkreathCemeteryLocation 0200BB:Skyrim.esm | after:PL21 |
| PL23 | X L | E arrival:HelgenLocation 018A4A:Skyrim.esm | HELGEN; first visit after HELGEN |
| PL24 | S C | E arrival:HalfmoonMillLocation 018E3E:Skyrim.esm | FIRST; SERANA |
| PL25 | I V U | E arrival:AngisCampLocation 0F5BA2:Skyrim.esm | FIRST |
| PL26 | G R | E arrival:CrackedTuskKeepLocation 01918D:Skyrim.esm | FIRST |
| PL27 | C X | E arrival:EvergreenGroveLocation 019174:Skyrim.esm | FIRST; CX_OK |
| PL28 | G I | E arrival:OrphanRockLocation 019287:Skyrim.esm | FIRST |
| PL29 | L R U | E arrival:HalldirsCairnLocation 019192:Skyrim.esm | FIRST |
| PL30 | A L | E arrival:FortNeugradLocation 019183:Skyrim.esm | FIRST; ASHE_HIRED |
| PL31 | G V U | E arrival:DragonLair02Location 019166:Skyrim.esm (Ancient's Ascent) | FIRST; HELGEN |
| PL32 | V R | E arrival:IlinaltasDeepLocation 01919C:Skyrim.esm | FIRST |
| PL33 | S R | E arrival:FalkreathCorpselightFarmLocation 0200BD:Skyrim.esm | FIRST; SERANA |
| PL34 | G I | E arrival:ClearspringTarnLocation 019157:Skyrim.esm | FIRST |

### Part 3 - The Rift

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL35 | K I | E arrival:IvarsteadLocation 018A4B:Skyrim.esm + player within ~800 units of Narfi's ruined house (ref not looked up) [UNC] | FIRST |
| PL36 | C S | E arrival:IvarsteadVilemyrInnLocation 0226AA:Skyrim.esm | FIRST; SERANA |
| PL37 | G V | E arrival:ShorsStoneLocation 018A4C:Skyrim.esm | FIRST |
| PL38 | K A | E arrival:DragonLair04Location 019168:Skyrim.esm (Autumnwatch Tower) | FIRST; ASHE_REVEAL |
| PL39 | I R | E arrival:GiantsGroveLocation 0C33AF:Skyrim.esm | FIRST |
| PL40 | S V | E arrival:RiftenBlackBriarMeaderyLocation 022482:Skyrim.esm | FIRST; SERANA; VAL_FATHER |
| PL41 | C L U | E arrival:DragonLair07Location 01916A:Skyrim.esm (Lost Tongue Overlook) | FIRST; HELGEN |
| PL42 | S K U | E arrival:DragonLair10Location 019164:Skyrim.esm (Eldersblood Peak) | FIRST; SERANA; HELGEN |
| PL43 | K R | E arrival:RoadsideRuinsLocation 04787B:Skyrim.esm | FIRST; BRYNJAR |
| PL44 | G C | E arrival:IvarsteadFellstarFarmLocation 0226A7:Skyrim.esm | FIRST |
| PL45 | C X U | E arrival:HoneystrandCaveLocation 019199:Skyrim.esm | FIRST; CX_OK |
| PL46 | I X | E arrival:LostProspectMineLocation 0D566B:Skyrim.esm | FIRST |
| PL47 | K I U | E arrival:DragonLair04Location 019168:Skyrim.esm (Autumnwatch Tower) | K_TOG+; any visit |

### Part 4 - Eastmarch and Windhelm

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL48 | K G U | E arrival:KynesgroveLocation 018A4E:Skyrim.esm | FIRST |
| PL49 | I R | E arrival:KynesgroveBraidwoodInnLocation 020A02:Skyrim.esm | FIRST |
| PL50 | V K | E arrival:DarkwaterCrossingLocation 018A4D:Skyrim.esm | FIRST; K_CRUSH |
| PL51 | V K | E arrival:DarkwaterCrossingLocation 018A4D:Skyrim.esm | K_TOG+; after:PL50; any visit |
| PL52 | X I | E arrival:hot springs of Eastmarch: player IsSwimming or PO3 IsActorInWater, exterior, inside EastmarchHoldLocation 01676A:Skyrim.esm, in the volcanic tundra (Region record not looked up) [UNC] | first time |
| PL53 | K R U | E arrival:hot springs, as PL52 [UNC] | K_CRUSH; player in the water |
| PL54 | S L | E arrival:hot springs, as PL52 [UNC] | SERANA; first time with Serana |
| PL55 | G K U | E arrival:MarasEyePondLocation 0ECF53:Skyrim.esm | FIRST; K_CRUSH |
| PL56 | S V | E arrival:MarasEyePondLocation 0ECF53:Skyrim.esm | SERANA; V_FLIRT; any visit |
| PL57 | V I | E arrival:CragslaneCavernLocation 019159:Skyrim.esm | FIRST |
| PL58 | S X | E arrival:MorvunskarLocation 01927D:Skyrim.esm | FIRST; SERANA |
| PL59 | C R | E arrival:WitchmistGroveLocation 0192C7:Skyrim.esm | FIRST |
| PL60 | K C | E arrival:FortAmolLocation 01917C:Skyrim.esm | FIRST |
| PL61 | G C | E arrival:NarzulburLocation 019282:Skyrim.esm | FIRST |
| PL62 | A X | E arrival:NarzulburLocation 019282:Skyrim.esm | ASHE_HIRED; after:PL61 |
| PL63 | X V | E arrival:WindhelmArgonianAssemblageLocation 0209E4:Skyrim.esm | FIRST |
| PL64 | X R U | E arrival:WindhelmArgonianAssemblageLocation 0209E4:Skyrim.esm | after:PL63; RX_OK |
| PL65 | I A | E arrival:Ahkari's caravan: player within ~1500 units of Ahkari (actor ref not looked up) [UNC] | ASHE_HIRED; first time near her with Ashe |
| PL66 | V G | E arrival:WinterWarLocation 0192A4:Skyrim.esm | FIRST |
| PL67 | G A | E arrival:mammoth graveyard in Eastmarch (unmarked, XMarker proximity) [UNC] | FIRST; ASHE_Q1 |
| PL68 | G X | E arrival:MixwaterMillLocation 018E3D:Skyrim.esm | FIRST |
| PL69 | X G | E arrival:SteamcragCampLocation 01916D:Skyrim.esm | FIRST |
| PL70 | R I | E arrival:GloomboundMineLocation 018E31:Skyrim.esm | FIRST |
| PL71 | G V | E arrival:MarasEyePondLocation 0ECF53:Skyrim.esm | G_TOG+; any visit |
| PL72 | X C | E arrival:hot springs, as PL52 [UNC] | CX_OK; first time with both |

### Part 5 - Winterhold and the Pale

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL73 | S V | E arrival:WinterholdLocation 018A51:Skyrim.esm | SERANA; after:MG1 |
| PL74 | G K | E arrival:DawnstarLocation 018A50:Skyrim.esm | GORE_BAIL; first visit after GORE_BAIL |
| PL75 | C X U | E arrival:DawnstarLocation 018A50:Skyrim.esm, exterior near the shore [UNC] | FIRST; CX_OK |
| PL76 | A K | E arrival:FortFellhammerLocation 01917F:Skyrim.esm | FIRST; ASHE_REVEAL |
| PL77 | X K U | E arrival:JaphetsFollyLocation 019178:Skyrim.esm | FIRST |
| PL78 | V S | E arrival:FrostflowLighthouseLocation 019186:Skyrim.esm | FIRST; SERANA |
| PL79 | X R | E arrival:PrideofTelVosLocation 0192A3:Skyrim.esm | FIRST; RX_OK |
| PL80 | X V U | E arrival:PilgrimsTrenchLocation 0192A2:Skyrim.esm | FIRST |
| PL81 | X A | E arrival:MountAnthorLocation 01927F:Skyrim.esm | FIRST; ASHE_REVEAL; HELGEN |
| PL82 | V L | E arrival:BrinehammerLocation 0192A0:Skyrim.esm | FIRST |
| PL83 | G I | E arrival:BlizzardRestLocation 018EEE:Skyrim.esm | FIRST |
| PL84 | A L | E arrival:NightgateInnLocation 020054:Skyrim.esm (or NightgateInnExteriorLocation 018A4F) | FIRST; ASHE_REVEAL |
| PL85 | K C U | E arrival:mammoth graveyard in the Pale (unmarked, XMarker proximity) [UNC] | after:PL16 |
| PL86 | R X | E arrival:DawnstarQuicksilverMineLocation 02DE25:Skyrim.esm | FIRST; RX_OK |

### Part 6 - Hjaalmarch

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL87 | X V U | E arrival:MorthalLocation 018A53:Skyrim.esm | FIRST |
| PL88 | G C | E arrival:StonehillsLocation 018A52:Skyrim.esm | FIRST |
| PL89 | G R | E arrival:RavenscarHollowLocation 019291:Skyrim.esm | FIRST |
| PL90 | K G | E arrival:MeekosShackLocation 0F6F13:Skyrim.esm | FIRST; BRYNJAR |
| PL91 | R K | E arrival:YngvildLocation 0192CA:Skyrim.esm | FIRST |
| PL92 | R X | E arrival:FortSnowhawkLocation 019184:Skyrim.esm | FIRST; RX_OK |
| PL93 | A L | E arrival:TalkingStoneCampLocation 0192BA:Skyrim.esm | FIRST; ASHE_HIRED |
| PL94 | K X U | E arrival:SkybornAtlarLocation 019165:Skyrim.esm | FIRST; HELGEN |
| PL95 | C L | E arrival:FourSkullLookoutLocation 0B23AC:Skyrim.esm | FIRST |

### Part 7 - Haafingar and Solitude

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL96 | S K | E arrival:DragonBridgeLocation 018A46:Skyrim.esm | SERANA; BRYNJAR |
| PL97 | V K | E arrival:SolitudeDocksLocation 0358B9:Skyrim.esm | after:P2 |
| PL98 | G V | E arrival:SolitudeRadiantRaimentsLocation 02009E:Skyrim.esm | FIRST |
| PL99 | V R | E arrival:BrokenOarGrottoLocation 019153:Skyrim.esm | FIRST |
| PL100 | S A | E arrival:ShadowgreenCavernLocation 01929C:Skyrim.esm | FIRST; SERANA; ASHE_HIRED |
| PL101 | G X | E arrival:NorthwatchKeepLocation 019285:Skyrim.esm (exterior approach, IsInInterior == 0) | FIRST |
| PL102 | K A | E arrival:ThalmorEmbassyLocation 018C92:Skyrim.esm (exterior only, IsInInterior == 0) | FIRST; ASHE_Q1 |
| PL103 | K S | E arrival:ThalmorEmbassyLocation 018C92:Skyrim.esm (exterior only) | FIRST; SERANA |
| PL104 | I V | E arrival:KatlasFarmLocation 018E38:Skyrim.esm | FIRST |

### Part 8 - The Reach

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL105 | R G | E arrival:KarthwastenLocation 018A54:Skyrim.esm | FIRST |
| PL106 | K A U | E arrival:MarkarthShrineofTalosLocation 06E830:Skyrim.esm | FIRST; ASHE_HIRED |
| PL107 | L V U | E arrival:MarkarthTempleofDibellaLocation 01F317:Skyrim.esm | FIRST |
| PL108 | A R | E arrival:MarkarthTempleofDibellaLocation 01F317:Skyrim.esm | ASHE_HIRED; A_CRUSH; any visit |
| PL109 | C A | E arrival:LostValleyRedoubtLocation 019268:Skyrim.esm | FIRST; ASHE_REVEAL |
| PL110 | X L U | E arrival:BardsLeapSummitLocation 018EE7:Skyrim.esm | FIRST |
| PL111 | A R U | E arrival:RedEagleRedoubtLocation 019170:Skyrim.esm | FIRST; ASHE_Q1; REMI_MORVIC |
| PL112 | L G U | E arrival:DragonLair01Location 019163:Skyrim.esm (Dragontooth Crater) | FIRST; HELGEN |
| PL113 | C V U | E arrival:DragonLair08Location 01916B:Skyrim.esm (Bonestrewn Crest) | FIRST; HELGEN; after:R10 |
| PL114 | G X | E arrival:DushnikhYalLocation 019171:Skyrim.esm | FIRST |
| PL115 | G K U | E arrival:DushnikhYalLocation 019171:Skyrim.esm | after:PL114 |
| PL116 | G I | E arrival:MorKhazgurLocation 01927C:Skyrim.esm | FIRST |
| PL117 | G L U | E arrival:MorKhazgurLocation 01927C:Skyrim.esm | after:PL116 |
| PL118 | I S | E arrival:Ma'dran's caravan: player within ~1500 units of Ma'dran (actor ref not looked up) [UNC] | SERANA; first time near him with Serana |
| PL119 | I C | E arrival:Ri'saad's caravan: player within ~1500 units of Ri'saad (actor ref not looked up) [UNC] | first time near him |
| PL120 | R X U | E arrival:CradlecrushRockLocation 019158:Skyrim.esm | FIRST; RX_OK |
| PL121 | V K | E arrival:LiarsRetreatLocation 019264:Skyrim.esm | FIRST |
| PL122 | C X | E arrival:MarkarthHagsCureLocation 01F30F:Skyrim.esm (or MarkarthLocation 018A59 near its door) | first time; CX_OK |
| PL123 | G V | E arrival:BardsLeapSummitLocation 018EE7:Skyrim.esm | after:PL110 |

### Part 9 - Wonders and wild places

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL124 | K G U | E arrival:ThroatoftheWorldLocation 0192BB:Skyrim.esm | FIRST (WorldQuiet already blocks MQ204 20..209 here) |
| PL125 | C V | E arrival:ThroatoftheWorldLocation 0192BB:Skyrim.esm | after:PL124; after:R10 |
| PL126 | S R U | E arrival:ThroatoftheWorldLocation 0192BB:Skyrim.esm | SERANA; first visit with Serana |
| PL127 | X R | E arrival:EldergleamSanctuaryLocation 0192AC:Skyrim.esm | FIRST; RX_OK |
| PL128 | C S | E arrival:EldergleamSanctuaryLocation 0192AC:Skyrim.esm | SERANA |
| PL129 | R G U | E arrival:ShrineofAzuraLocation 092497:Skyrim.esm | FIRST |
| PL130 | S V | E arrival:ShrineofAzuraLocation 092497:Skyrim.esm | SERANA |
| PL131 | K I U | E arrival:ShrineofAzuraLocation 092497:Skyrim.esm | after:PL129; KAI_INIGO |
| PL132 | R L U | E arrival:BlackreachLocation 018EE8:Skyrim.esm | FIRST |
| PL133 | V S | E arrival:BlackreachLocation 018EE8:Skyrim.esm | SERANA |
| PL134 | R K | E arrival:BlackreachLocation 018EE8:Skyrim.esm | after:PL132 |
| PL135 | C A | E arrival:BlackreachLocation 018EE8:Skyrim.esm | ASHE_REVEAL |
| PL136 | G L U | E arrival:DragonLair09Location 01916C:Skyrim.esm (Shearpoint) | FIRST; HELGEN |
| PL137 | K R | E arrival:RiversideShackLocation 0ECF4D:Skyrim.esm | FIRST; BRYNJAR |
| PL138 | K C | E arrival:PeaksShadeTowerLocation 047886:Skyrim.esm | FIRST |
| PL139 | C S | E arrival:SilverdriftLairLocation 0192AA:Skyrim.esm | FIRST; SERANA |
| PL140 | G S | E arrival:WidowsWatchRuinsLocation 0EF0A9:Skyrim.esm | FIRST; SERANA; after:PL12 |
| PL141 | X K | E arrival:DrelasCottageLocation 0E66AB:Skyrim.esm | FIRST |
| PL142 | K V U | E arrival:WaywardPassLocation 0C2EFC:Skyrim.esm | FIRST; K_TOG+ |

### Part 10 - Dwemer ruins

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL143 | R L U | E arrival:AlftandLocation 018EE1:Skyrim.esm | FIRST |
| PL144 | A R | E arrival:AlftandLocation 018EE1:Skyrim.esm | ASHE_REVEAL |
| PL145 | V L | E arrival:MzinchaleftLocation 019280:Skyrim.esm | FIRST |
| PL146 | R X | E arrival:MzinchaleftLocation 019280:Skyrim.esm | after:PL145; RX_OK |
| PL147 | K X U | E arrival:RaldbtharLocation 090576:Skyrim.esm | FIRST |
| PL148 | G V U | E arrival:RaldbtharLocation 090576:Skyrim.esm | after:PL147 |
| PL149 | R S | E arrival:BthardamzLocation 019152:Skyrim.esm | FIRST; SERANA |
| PL150 | L A | E arrival:DLC1ArkngthamzLocation 004D6D:Dawnguard.esm | FIRST; ASHE_REVEAL |
| PL151 | R V U | E arrival:DLC1ArkngthamzLocation 004D6D:Dawnguard.esm | after:PL150, or FIRST if Ashe was never hired |
| PL152 | V C | E arrival:KagrenzelLocation 0233EE:Skyrim.esm | FIRST; after:R10 |
| PL153 | K L | E arrival:AvanchnzelLocation 018EE5:Skyrim.esm | FIRST |
| PL154 | A I | E arrival:HarmugstahlLocation 019194:Skyrim.esm | FIRST; ASHE_REVEAL |
| PL155 | A X | E arrival:BthalftLocation 0D566F:Skyrim.esm | FIRST; ASHE_REVEAL |
| PL156 | G R | E arrival:DeepFolkCrossingLocation 0B2391:Skyrim.esm | FIRST |
| PL157 | L R | E arrival:KagrenzelLocation 0233EE:Skyrim.esm | after:PL152 |

### Part 11 - Nordic barrows

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL158 | K R U | E arrival:UstengravLocation 0192BF:Skyrim.esm (exterior, IsInInterior == 0) | FIRST; the 300 s cooldown puts it after the main-quest arrival talk in 30 |
| PL159 | G A | E arrival:ForelhostLocation 01917A:Skyrim.esm | FIRST; ASHE_HIRED |
| PL160 | S G | E arrival:RagnvaldLocation 01928F:Skyrim.esm | FIRST; SERANA |
| PL161 | S L | E arrival:VolunruudLocation 0192C3:Skyrim.esm | FIRST; SERANA |
| PL162 | I A | E arrival:ValthumeLocation 033DA0:Skyrim.esm | FIRST; ASHE_Q1 |
| PL163 | X S | E arrival:AnsilvundLocation 01BDFD:Skyrim.esm | FIRST; SERANA |
| PL164 | I C | E arrival:VolskyggeLocation 0192C2:Skyrim.esm | FIRST |
| PL165 | G X | E arrival:HighGateRuinsLocation 019195:Skyrim.esm | FIRST |
| PL166 | K L | E arrival:IronbindBarrowLocation 0350BC:Skyrim.esm | FIRST |
| PL167 | K G U | E arrival:HillgrundsTombLocation 019196:Skyrim.esm | FIRST |
| PL168 | L V | E arrival:ArcwindPointLocation 0FD685:Skyrim.esm | FIRST |

### Part 12 - The standing stones

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL169 | G R U | E arrival:DoomstoneGuardianStoneLocation 10FE43:Skyrim.esm | FIRST |
| PL170 | K A U | E arrival:DoomstoneGuardianStoneLocation 10FE43:Skyrim.esm | ASHE_REVEAL |
| PL171 | L I U | E arrival:DoomstoneLadyLocation 0D5676:Skyrim.esm | FIRST |
| PL172 | S L U | E arrival:DoomstoneLadyLocation 0D5676:Skyrim.esm | SERANA; after:PL171 |
| PL173 | K S | E arrival:DoomstoneLordLocation 0D5677:Skyrim.esm | FIRST; SERANA |
| PL174 | C V | E arrival:DoomstoneSteedLocation 0D567D:Skyrim.esm | FIRST; after:R10 |
| PL175 | R X U | E arrival:DoomstoneApprenticeLocation 0D5673:Skyrim.esm | FIRST; RX_OK |
| PL176 | X L U | E arrival:DoomstoneAtronachLocation 0D5675:Skyrim.esm | FIRST |
| PL177 | S R U | E arrival:DoomstoneRitualLocation 0D567A:Skyrim.esm | FIRST; SERANA |
| PL178 | V I U | E arrival:DoomstoneSerpentLocation 0D567B:Skyrim.esm | FIRST |
| PL179 | C G | E arrival:DoomstoneShadowLocation 0D567C:Skyrim.esm | FIRST |
| PL180 | C L | E arrival:DoomstoneTowerLocation 0D567E:Skyrim.esm | FIRST |

## 4. Open items for the build

- Place or look up refs for: mammoth graveyards (PL16, PL67, PL85), the Eastmarch hot springs (PL52-54, PL72), Narfi's ruined house in Ivarstead (PL35), the Dawnstar shore (PL75), and the caravan leaders Ahkari, Ma'dran and Ri'saad (PL65, PL118, PL119).
- Gloombound Mine (PL70): the exterior is GloomboundMineLocation 018E31; GloomboundMineMineLocation 10FE2D is the interior.
- Confirm the CX_OK stage (shared with R18), and whether ASHE_Q1 is the right gate for Ashe's "twenty lost years" lines (PL67, PL111).
- Some places are also used by quest talks in other files (Ancient's Ascent in 13, Orphan Rock and Hunter's Rest in 15, Nightgate Inn in 33, Ustengrav in 30, Valthume and High Gate in 42, Halldir's Cairn and Cragslane in 37). Those are quest-gated; ours are arrival-only and on different topics. The cooldown keeps them from stacking.
