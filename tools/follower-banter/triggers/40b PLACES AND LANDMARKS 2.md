# 40b PLACES AND LANDMARKS 2 - trigger rows (prefix PL, 250 talks, PL181-PL430)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\40b PLACES AND LANDMARKS 2.txt`.

Same firing rules as `40 PLACES AND LANDMARKS.md` section 1 (`E arrival:<Location>` on the controller's OnLocationChange, `FIRST` visited-bit, `any visit`, `after:<ID>`, 300 s cooldown, WorldQuiet + Free). Location EditorIDs and FormIDs were read read-only from the live load order with houseCARL (LCTN records; parent hold and location-type keywords checked). Every location below was checked against all other trigger files and every Desktop script: none has an arrival talk elsewhere. Lost Echo Cave, Bilegulch, Snapleg, Faldar's Tooth, Boulderfall, Purewater Run, Cronvangr, Bronze Water Cave, Fort Greenwall, Windward Ruins and the Solitude lighthouse also appear in quest-gated talks in other files; ours are arrival-only and on different topics. **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, U Luna.

## Gate codes

From TRIGGERS.md section 4 and `40 PLACES AND LANDMARKS.md` section 2: `FIRST`, `any visit`, `after:<ID>`, `HELGEN`, `BRYNJAR`, `K_CRUSH`, `K_TOG+`, `V_FLIRT`, `G_FLIRT`, `WOLF` (C03 25), `VAL_FATHER`, `VAL_FATHIS`, `GORE_FATHER`, `SERANA`, `ASHE_HIRED`, `ASHE_REVEAL`, `ASHE_Q1`, `A_CRUSH`, `KAI_INIGO`, `RX_OK`, `CX_OK`, `after:R10` ("Twenty Yards").

New in this file:
- `ASHE_LOGS` = MM_AMQ_05 (056A66:Ashe - Fire and Blood.esp) completed (she has heard her father's logs, so she knows he sent her away to save her). Used by PL260.
- `S_ROM` = Serana's romance has begun: SDA_SeranaRomance (A2D563:SeranaDialogAddon.esp) == 1 AND SDA_SeranaRomance04 (A929B9) stage >= 20 **[UNC: stage that marks the 'yes' answer]**. Used by PL389.
- PL371 / PL375 (Abandoned Prison): Kaidan's rescue cell. Kaidan's own banter quests block idles while he is in this location during K01. Our talk needs K01 completed (or K03 >= 10) as well as FIRST, so it can never fire during the rescue itself **[UNC: confirm K01 completion stage]**.
- Mod-plugin locations resolve with `Game.GetFormFromFile` like the follower refs; if the plugin is missing the row simply never fires.


### PART 13 - WHITERUN HOLD, THE REST OF IT  (20 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL181 | G K U | E arrival:BarleydarkFarmLocation 018C8C:Skyrim.esm | FIRST |
| PL182 | L V | E arrival:BattleBornFarmLocation 018C8D:Skyrim.esm | FIRST |
| PL183 | X R | E arrival:ChillfurrowFarmLocation 018C90:Skyrim.esm | FIRST; RX_OK |
| PL184 | S K | E arrival:BrokenFangCaveLocation 01914D:Skyrim.esm | FIRST; SERANA |
| PL185 | I C | E arrival:GraywinterWatchLocation 01918B:Skyrim.esm | FIRST |
| PL186 | G A | E arrival:GreenspringHollowLocation 01919B:Skyrim.esm | FIRST; ASHE_HIRED |
| PL187 | L U R | E arrival:RannveigsFastLocation 019290:Skyrim.esm | FIRST |
| PL188 | R X | E arrival:ShimmermistCaveLocation 01929D:Skyrim.esm | FIRST; RX_OK |
| PL189 | G K U | E arrival:SerpentsBluffRedoubtLocation 0192C4:Skyrim.esm | FIRST |
| PL190 | V G | E arrival:WhiteRiverWatchLocation 0192C5:Skyrim.esm | FIRST |
| PL191 | X I | E arrival:ColdRockPassLocation 0BC0A3:Skyrim.esm | FIRST |
| PL192 | L K U | E arrival:LundsHutLocation 0E66A5:Skyrim.esm | FIRST |
| PL193 | C K U | E arrival:CrabbersShantyLocation 0E66A9:Skyrim.esm (in-game name "Crab Shack") | FIRST |
| PL194 | R G | E arrival:RWBRiverwoodBanditCampLocation 0008D5:RiverwoodBandits.esp (Skybound Underhang Camp) | FIRST |
| PL195 | X U | E arrival:IvyApothecaryLocation 0000C7:Ivy Riverwood Overhaul.esp | FIRST |
| PL196 | V U L | E arrival:IvyRandalfShopLocation 000515:Ivy Riverwood Overhaul.esp (Enchanted Echoes) | FIRST |
| PL197 | G I | E arrival:BattleBornFarmLocation 018C8D:Skyrim.esm | after:PL182; any visit |
| PL198 | A K | E arrival:WhiteRiverWatchLocation 0192C5:Skyrim.esm | after:PL190; ASHE_HIRED; any visit |
| PL199 | L S | E arrival:GreenspringHollowLocation 01919B:Skyrim.esm | SERANA; any visit |
| PL200 | G X | E arrival:CrabbersShantyLocation 0E66A9:Skyrim.esm (in-game name "Crab Shack") | after:PL193; any visit |

### PART 14 - FALKREATH HOLD, DEEPER IN  (29 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL201 | G K | E arrival:BearsCaveMillLocation 018C8E:Skyrim.esm | FIRST |
| PL202 | R S U | E arrival:BloodletThroneLocation 016F85:Skyrim.esm | FIRST; SERANA |
| PL203 | L I U | E arrival:DarkshadeCopseLocation 01915E:Skyrim.esm | FIRST |
| PL204 | R V | E arrival:GreywaterGrottoLocation 01918C:Skyrim.esm | FIRST |
| PL205 | K S | E arrival:HaemarsShameLocation 01918F:Skyrim.esm | FIRST; SERANA |
| PL206 | L G U | E arrival:LostEchoCaveLocation 019266:Skyrim.esm | FIRST |
| PL207 | C G | E arrival:BilegulchMineLocation 019269:Skyrim.esm | FIRST |
| PL208 | I K U | E arrival:MossMotherCavernLocation 01927E:Skyrim.esm | FIRST |
| PL209 | L S U | E arrival:SecundasShelfLocation 01929A:Skyrim.esm | FIRST; SERANA |
| PL210 | A V | E arrival:BannermistTowerLocation 047825:Skyrim.esm | FIRST; ASHE_HIRED |
| PL211 | K X | E arrival:FalkreathWatchtowerLocation 0479B3:Skyrim.esm (in-game name "Crossroads Watchtower") | FIRST |
| PL212 | R G U | E arrival:SkyboundWatchLocation 04B679:Skyrim.esm (North Skybound Watch) | FIRST |
| PL213 | L X | E arrival:SunderstoneGorgeLocation 061AE3:Skyrim.esm (in-game name "Greywater Gorge") | FIRST |
| PL214 | V I | E arrival:KnifepointRidgeLocation 08E1B7:Skyrim.esm | FIRST |
| PL215 | L S | E arrival:ShriekwindBastionLocation 0A0E30:Skyrim.esm | FIRST; SERANA |
| PL216 | R K U | E arrival:EmbershardLocation 0B712C:Skyrim.esm | FIRST |
| PL217 | C K | E arrival:BonechillPassageLocation 0FDA46:Skyrim.esm | FIRST |
| PL218 | L G U | E arrival:GraniteHillLocation 018A48:Skyrim.esm | FIRST |
| PL219 | X I | E arrival:SouthfringeSanctumLocation 01914C:Skyrim.esm | FIRST |
| PL220 | I K | E arrival:FalkreathWatchmansHutLocation 060365:Skyrim.esm | FIRST; KAI_INIGO |
| PL221 | R S U | E arrival:GRVECemeteryLocation 0CB815:FalkreathShades.esp (Pine-shrouded Cemetery) | FIRST; SERANA |
| PL222 | L G | E arrival:GRVEMausoleumLocation 3238B2:FalkreathShades.esp (Gravewind Mausoleum) | FIRST |
| PL223 | V K | E arrival:COTN_FalkreathWatchtowerLocation 0FDD35:COTN - Falkreath.esp | FIRST |
| PL224 | G V | E arrival:SRC_PSTPPinewatchCheckpointLocation 00132A:SRC - All In One.esp | FIRST |
| PL225 | K G | E arrival:BloodletThroneLocation 016F85:Skyrim.esm | after:PL202; any visit |
| PL226 | R A | E arrival:MossMotherCavernLocation 01927E:Skyrim.esm | after:PL208; ASHE_REVEAL; any visit |
| PL227 | I G | E arrival:SecundasShelfLocation 01929A:Skyrim.esm | after:PL209; any visit |
| PL228 | L V | E arrival:EmbershardLocation 0B712C:Skyrim.esm | after:PL216; any visit |
| PL229 | C I | E arrival:HaemarsShameLocation 01918F:Skyrim.esm | after:PL205; any visit |

### PART 15 - HAAFINGAR AND SOLITUDE, OUTSIDE THE WALLS  (18 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL230 | I K U | E arrival:ClearpinePondLocation 019156:Skyrim.esm | FIRST |
| PL231 | G S | E arrival:PinemoonCaveLocation 019288:Skyrim.esm | FIRST; SERANA |
| PL232 | C L | E arrival:RimerockBurrowLocation 019296:Skyrim.esm | FIRST |
| PL233 | R G | E arrival:SteepfallBurrowLocation 0192B5:Skyrim.esm | FIRST |
| PL234 | A K | E arrival:SolitudeSawmillLocation 018E44:Skyrim.esm | FIRST; ASHE_HIRED |
| PL235 | I G | E arrival:PinefrostTowerLocation 0EF0BC:Skyrim.esm | FIRST |
| PL236 | R V | E arrival:SolitudeLighthouseExteriorLocation 10FE44:Skyrim.esm | FIRST |
| PL237 | K V | E arrival:EastEmpireCompanyWarehouseLocation 02008E:Skyrim.esm | FIRST |
| PL238 | G I U | E arrival:DragonBridgeLumberCampLocation 020078:Skyrim.esm | FIRST |
| PL239 | C K | E arrival:DragonBridgeFarmLocation 020006:Skyrim.esm | FIRST |
| PL240 | L V U | E arrival:WSSquallGateLocation AB6A2E:Grand Solitude - The Walls of High King Erling.esp | FIRST |
| PL241 | C V U | E arrival:WSExquisitePastriesLocation AB6050:Grand Solitude - The Walls of High King Erling.esp | FIRST; after:R10 |
| PL242 | R V | E arrival:WSBankofHaafingarLocation AB5FEA:Grand Solitude - The Walls of High King Erling.esp | FIRST |
| PL243 | L G U | E arrival:WSANewPageLocation AB5FB6:Grand Solitude - The Walls of High King Erling.esp | FIRST |
| PL244 | X V | E arrival:BrinewaterGrottoLocation 05F428:Skyrim.esm (parent is Tamriel, hold not confirmed) [UNC] | FIRST |
| PL245 | G K | E arrival:RimerockBurrowLocation 019296:Skyrim.esm | after:PL232; WOLF; any visit |
| PL246 | X R | E arrival:WSANewPageLocation AB5FB6:Grand Solitude - The Walls of High King Erling.esp | after:PL243; RX_OK; any visit |
| PL247 | I A | E arrival:WSExquisitePastriesLocation AB6050:Grand Solitude - The Walls of High King Erling.esp | after:PL241; ASHE_REVEAL; any visit |

### PART 16 - HJAALMARCH AND THE MARSH  (10 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL248 | L I | E arrival:BroodCavernLocation 019150:Skyrim.esm | FIRST |
| PL249 | G K U | E arrival:OrotheimLocation 019286:Skyrim.esm | FIRST |
| PL250 | R V | E arrival:RobbersGorgeLocation 01929B:Skyrim.esm | FIRST |
| PL251 | V I | E arrival:FrostRiverFarmLocation 018E30:Skyrim.esm | FIRST |
| PL252 | A K | E arrival:StonehillBluffLocation 0192B7:Skyrim.esm | FIRST; ASHE_REVEAL |
| PL253 | L U R | E arrival:KjenstagRuinsLocation 0C2EF1:Skyrim.esm | FIRST |
| PL254 | L K U | E arrival:ValkyggLocation 0EAA62:Skyrim.esm | FIRST |
| PL255 | L G | E arrival:DeadMensRespiteLocation 019161:Skyrim.esm | FIRST |
| PL256 | U G K | E arrival:GjukarsMonumentLocation 0A3F49:Skyrim.esm (no parent, no Name on record; arrival = within ~1500 units of the monument) [UNC] | FIRST |
| PL257 | C X | E arrival:StonehillBluffLocation 0192B7:Skyrim.esm | CX_OK; any visit |

### PART 17 - THE PALE  (16 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL258 | G V | E arrival:AngasMillLocation 018C8B:Skyrim.esm | FIRST |
| PL259 | L K | E arrival:LoreiusFarmLocation 018E3B:Skyrim.esm | FIRST |
| PL260 | R A | E arrival:DuskglowCreviceLocation 019172:Skyrim.esm | FIRST; ASHE_REVEAL; ASHE_LOGS |
| PL261 | G X | E arrival:ForsakenCaveLocation 01917B:Skyrim.esm | FIRST |
| PL262 | K V | E arrival:FortDunstadLocation 01917E:Skyrim.esm | FIRST; BRYNJAR |
| PL263 | G I U | E arrival:FortDunstadStumblingSabrecatWorking 000351:Fort Dunstad.esp (The Stumbling Sabrecat) | FIRST |
| PL264 | V L U | E arrival:RedRoadPassLocation 019294:Skyrim.esm | FIRST |
| PL265 | S I | E arrival:ShroudedGroveLocation 0192A6:Skyrim.esm | FIRST; SERANA |
| PL266 | R G | E arrival:TumbleArchPassLocation 0192BE:Skyrim.esm | FIRST |
| PL267 | R L U | E arrival:BronzeWaterCaveLocation 046BAC:Skyrim.esm | FIRST |
| PL268 | L K U | E arrival:WeynonStonesLocation 0BC0AC:Skyrim.esm | FIRST |
| PL269 | V G | E arrival:WindwardRuinsLocation 0C2EED:Skyrim.esm | FIRST |
| PL270 | I K | E arrival:YorgrimOverlookLocation 0C3428:Skyrim.esm | FIRST; KAI_INIGO |
| PL271 | R K | E arrival:DawnstarIronBreakerMineLocation 02DE24:Skyrim.esm | FIRST |
| PL272 | A L | E arrival:FortDunstadLocation 01917E:Skyrim.esm | after:PL262; ASHE_HIRED; any visit |
| PL273 | C V | E arrival:WindwardRuinsLocation 0C2EED:Skyrim.esm | after:PL269; after:R10; any visit |

### PART 18 - WINTERHOLD AND EASTMARCH  (29 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL274 | L R | E arrival:WhistlingMineLocation 018E45:Skyrim.esm | FIRST |
| PL275 | K V U | E arrival:BleakcoastCaveLocation 018EEA:Skyrim.esm | FIRST |
| PL276 | I S | E arrival:DriftshadeSanctuaryLocation 01916E:Skyrim.esm | FIRST; SERANA |
| PL277 | G K U | E arrival:FortKastavLocation 019182:Skyrim.esm | FIRST |
| PL278 | A V | E arrival:HelasFollyLocation 0192A1:Skyrim.esm | FIRST; ASHE_HIRED |
| PL279 | R K | E arrival:StillbornCaveLocation 0192B6:Skyrim.esm | FIRST |
| PL280 | L X U | E arrival:JourneymansNookLocation 0EF54C:Skyrim.esm | FIRST |
| PL281 | R X | E arrival:DeekusCampLocation 057971:Skyrim.esm | FIRST; RX_OK |
| PL282 | G K U | E arrival:BrandyMugFarmLocation 018C8F:Skyrim.esm | FIRST |
| PL283 | V X | E arrival:HlaaluFarmLocation 018E35:Skyrim.esm | FIRST |
| PL284 | C L | E arrival:HollyfrostFarmLocation 018E36:Skyrim.esm | FIRST |
| PL285 | R K | E arrival:CragwallowSlopeLocation 01915A:Skyrim.esm | FIRST |
| PL286 | V S | E arrival:CronvangrHallLocation 01915B:Skyrim.esm | FIRST; SERANA; VAL_FATHIS |
| PL287 | G I | E arrival:LostKnifeHideoutLocation 019267:Skyrim.esm | FIRST |
| PL288 | L G | E arrival:SnaplegCaveLocation 0192AE:Skyrim.esm | FIRST |
| PL289 | V K | E arrival:UtteringHillsCampLocation 0192C0:Skyrim.esm | FIRST |
| PL290 | G L | E arrival:StonyCreekCaveLocation 080F28:Skyrim.esm | FIRST |
| PL291 | G V | E arrival:TraitorsPostLocation 0C2EE7:Skyrim.esm | FIRST; VAL_FATHER; GORE_FATHER |
| PL292 | K X | E arrival:BrokenLimbCampLocation 0ECF88:Skyrim.esm | FIRST; BRYNJAR |
| PL293 | R I | E arrival:RefugeesRestLocation 0EF572:Skyrim.esm | FIRST |
| PL294 | C R | E arrival:DarkwaterCrossingGoldenRockMineLocation 020A10:Skyrim.esm | FIRST |
| PL295 | R L U | E arrival:KynesgroveSteamscorchGullyMineLocation 020A07:Skyrim.esm | FIRST |
| PL296 | S K | E arrival:KynesgroveHallOfKyneLocationTGCoKG 16436B:The Great Village of Kynesgrove.esp | FIRST; SERANA |
| PL297 | L I | E arrival:KynesgroveKynesbyLocationTGCoKG 0E5236:The Great Village of Kynesgrove.esp (in-game name "Kymesby") | FIRST |
| PL298 | X U | E arrival:SRC_TPInteriorLocation 001C0C:SRC - All In One.esp (Refugees' Respite) | FIRST |
| PL299 | X I | E arrival:BrandyMugFarmLocation 018C8F:Skyrim.esm | after:PL282; any visit |
| PL300 | C S | E arrival:SnaplegCaveLocation 0192AE:Skyrim.esm | after:PL288; SERANA; any visit |
| PL301 | R G | E arrival:BrokenLimbCampLocation 0ECF88:Skyrim.esm | after:PL292; any visit |
| PL302 | S A | E arrival:FortKastavLocation 019182:Skyrim.esm | after:PL277; SERANA; ASHE_REVEAL; any visit |

### PART 19 - THE RIFT, ROUND THE BACK OF IT  (35 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL303 | G U K | E arrival:SnowShodFarmLocation 018E43:Skyrim.esm | FIRST |
| PL304 | R V | E arrival:MerryfairFarmLocation 018E3C:Skyrim.esm | FIRST |
| PL305 | I U K | E arrival:HeartwoodMillLocation 018E33:Skyrim.esm | FIRST |
| PL306 | C I | E arrival:AutumnshadeClearingLocation 018EE4:Skyrim.esm | FIRST |
| PL307 | V I | E arrival:BrokenHelmHollowLocation 01914E:Skyrim.esm | FIRST |
| PL308 | R X U | E arrival:CrystaldriftCaveLocation 01915C:Skyrim.esm | FIRST; RX_OK |
| PL309 | X K | E arrival:DarkwaterCavernLocation 01915F:Skyrim.esm (in-game name "Darkwater Pass") | FIRST |
| PL310 | G K U | E arrival:FaldarsToothLocation 019175:Skyrim.esm | FIRST |
| PL311 | G S | E arrival:FortGreenwallLocation 019180:Skyrim.esm | FIRST; SERANA |
| PL312 | L K U | E arrival:GeirmundsHallLocation 019188:Skyrim.esm | FIRST |
| PL313 | A K | E arrival:PinepeakCavernLocation 019289:Skyrim.esm | FIRST; ASHE_HIRED |
| PL314 | L I | E arrival:TolvaldsCaveLocation 0192BC:Skyrim.esm | FIRST |
| PL315 | G K | E arrival:RiftenMaraSquareTowerLocation 00AD40:Riften Expansion.esp (the "Guard Tower" on Mara's Square) | FIRST |
| PL316 | L V | E arrival:RiftWatchtowerLocation 0D5665:Skyrim.esm | FIRST |
| PL317 | X I | E arrival:ShorsWatchtowerLocation 0D5669:Skyrim.esm | FIRST |
| PL318 | X C U | E arrival:AlchemistsShackLocation 0D566D:Skyrim.esm | FIRST; CX_OK |
| PL319 | R A | E arrival:BoulderfallCaveLocation 0F52DA:Skyrim.esm | FIRST; ASHE_HIRED |
| PL320 | V G | E arrival:RiftenHouseofClanWaveBreakerLocation 09E689:Riften Expansion.esp | FIRST |
| PL321 | C K U | E arrival:RiftenHouseofClanBearheartLocation 19D5BC:Riften Expansion.esp | FIRST |
| PL322 | K U V | E arrival:RiftenBakeryLocation 0D6A62:Riften Expansion.esp (Honeyed Words Bakery) | FIRST; K_CRUSH |
| PL323 | X V | E arrival:RiftenDockFortLocation 4C86D1:Riften Expansion.esp | FIRST |
| PL324 | L K U | E arrival:RiftenTempleOfTalosLocation 0CC3E3:Riften Expansion.esp (Temple of Ysmir) | FIRST |
| PL325 | R V | E arrival:RiftenRethanHoldingsLocation 01F652:Riften Expansion.esp | FIRST |
| PL326 | L V | E arrival:RiftenWeaveAndThreadLocation 0CC611:Riften Expansion.esp | FIRST |
| PL327 | K R U | E arrival:RiftenMerchantsRowLocation 4C86D2:Riften Expansion.esp | FIRST |
| PL328 | C S | E arrival:DuskwatchTowerLocation 0020D2:SRC - All In One.esp | FIRST; SERANA |
| PL329 | X U | E arrival:Thuldor_LocIvarsteadBakery 013B5E:Thuldor's Ivarstead.esp (Breadsmith) | FIRST |
| PL330 | G K | E arrival:Thuldor_LocIvarsteadSmith 0135FA:Thuldor's Ivarstead.esp (The Mountain's Anvil) | FIRST |
| PL331 | C G | E arrival:Thuldor_LocIvarsteadStore 00C46A:Thuldor's Ivarstead.esp (Pilgrim's Purchases) | FIRST |
| PL332 | G K U | E arrival:RiftenBakeryLocation 0D6A62:Riften Expansion.esp (Honeyed Words Bakery) | after:PL322; K_TOG+; any visit |
| PL333 | G I | E arrival:RiftenTempleOfTalosLocation 0CC3E3:Riften Expansion.esp (Temple of Ysmir) | after:PL324; KAI_INIGO; any visit |
| PL334 | I V | E arrival:RiftenMerchantsRowLocation 4C86D2:Riften Expansion.esp | after:PL327; any visit |
| PL335 | R X | E arrival:Thuldor_LocIvarsteadBakery 013B5E:Thuldor's Ivarstead.esp (Breadsmith) | after:PL329; RX_OK; any visit |
| PL336 | I K | E arrival:RiftenHouseofClanBearheartLocation 19D5BC:Riften Expansion.esp | after:PL321; KAI_INIGO; any visit |
| PL337 | L A | E arrival:DuskwatchTowerLocation 0020D2:SRC - All In One.esp | after:PL328; ASHE_HIRED; any visit |

### PART 20 - THE REACH, MINES, REDOUBTS AND MARKARTH'S EDGE  (40 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL338 | G V | E arrival:SalviusFarmLocation 018E40:Skyrim.esm | FIRST |
| PL339 | L I U | E arrival:LeftHandMineLocation 018E3A:Skyrim.esm | FIRST |
| PL340 | C V | E arrival:BleakwindBluffLocation 018EEC:Skyrim.esm | FIRST; after:R10 |
| PL341 | R G U | E arrival:BlindCliffCaveLocation 018EED:Skyrim.esm | FIRST |
| PL342 | L U G | E arrival:BrokenTowerRedoubtLocation 01914F:Skyrim.esm | FIRST |
| PL343 | R I | E arrival:BrucasLeapRedoubtLocation 019151:Skyrim.esm | FIRST |
| PL344 | V S | E arrival:DeadCroneRockLocation 019160:Skyrim.esm | FIRST; SERANA |
| PL345 | I A | E arrival:DeepwoodRedoubtLocation 019162:Skyrim.esm | FIRST; ASHE_REVEAL |
| PL346 | X L | E arrival:HagRockRedoubtLocation 019190:Skyrim.esm | FIRST |
| PL347 | G S | E arrival:PurewaterRunLocation 01928D:Skyrim.esm | FIRST; SERANA |
| PL348 | L K U | E arrival:ReachwaterRockLocation 019293:Skyrim.esm | FIRST |
| PL349 | G V | E arrival:SoljundsSinkholeLocation 0192B1:Skyrim.esm | FIRST |
| PL350 | R A | E arrival:CliffsideRetreatLocation 0B238D:Skyrim.esm | FIRST; ASHE_HIRED |
| PL351 | G X | E arrival:DragonBridgeOverlookLocation 0B2395:Skyrim.esm | FIRST |
| PL352 | K X | E arrival:CradleStoneTowerLocation 0B239F:Skyrim.esm | FIRST |
| PL353 | C K | E arrival:ReachwindEyrieLocation 0B23A5:Skyrim.esm | FIRST |
| PL354 | G U K | E arrival:MarkarthEntranceShopLocation 0FFB24:Lux Via - Markarth Entrance and Farm Overhaul.esp (Markarth East Empire Goods) | FIRST |
| PL355 | L U R | E arrival:KarthwastenSanuarachMineLocation 01F7BF:Skyrim.esm | FIRST |
| PL356 | C L | E arrival:KarthwastenFennsGulchMineLocation 01F7BE:Skyrim.esm | FIRST |
| PL357 | X G | E arrival:DushnikhYalMineLocation 01F7FE:Skyrim.esm | FIRST |
| PL358 | V K | E arrival:MorKhazgurMineLocation 01F802:Skyrim.esm | FIRST |
| PL359 | R K U | E arrival:MarkarthEntranceLocation 0F0816:Lux Via - Markarth Entrance and Farm Overhaul.esp (Markarth Outskirts) | FIRST |
| PL360 | L I U | E arrival:MarkarthEntranceObservatoryLocation 113FC3:Lux Via - Markarth Entrance and Farm Overhaul.esp | FIRST |
| PL361 | R V | E arrival:MarkarthEntranceThievesGuildLocation 11E1FF:Lux Via - Markarth Entrance and Farm Overhaul.esp (Markarth Old Dam) | FIRST |
| PL362 | L X | E arrival:MarkarthEntranceOldTempleLocation 11E200:Lux Via - Markarth Entrance and Farm Overhaul.esp | FIRST |
| PL363 | X R | E arrival:MarkarthMushroomFarmLocation 00092D:Lux Via - Markarth Entrance and Farm Overhaul.esp | FIRST; RX_OK |
| PL364 | G V | E arrival:MarkarthEntranceWasteCollectorLocation 109D41:Lux Via - Markarth Entrance and Farm Overhaul.esp | FIRST |
| PL365 | L K U | E arrival:JELMorihausRefugeLocation 012F0D:MorihausRefugeStandalone.esp (Morihaus' Refuge, Falkreath Hold) | FIRST |
| PL366 | R I U | E arrival:KynesgrovePilgrimsHouseLocationTGCoKG 16436A:The Great Village of Kynesgrove.esp | FIRST |
| PL367 | G L | E arrival:KynesgroveGalasSteadLocationTGCoKG 164367:The Great Village of Kynesgrove.esp | FIRST |
| PL368 | R V | E arrival:KynesgroveHerleifAndRagnasFarmLocationTGCoKG 164368:The Great Village of Kynesgrove.esp | FIRST |
| PL369 | L K | E arrival:HilariusFarmhouseLocation 000A77:Lux Via - Markarth Entrance and Farm Overhaul.esp | FIRST |
| PL370 | A K U | E arrival:WSSquallGateTowerLocation AB6A2F:Grand Solitude - The Walls of High King Erling.esp | FIRST; ASHE_HIRED |
| PL371 | K G U | E arrival:AbandonedPrisonLocation 0ECF4C:Skyrim.esm | FIRST |
| PL372 | G X | E arrival:KorvanjundLocation 019261:Skyrim.esm | FIRST |
| PL373 | V K | E arrival:MarkarthEntranceShopLocation 0FFB24:Lux Via - Markarth Entrance and Farm Overhaul.esp (Markarth East Empire Goods) | after:PL354; V_FLIRT; K_CRUSH; any visit |
| PL374 | L A U | E arrival:MarkarthEntranceObservatoryLocation 113FC3:Lux Via - Markarth Entrance and Farm Overhaul.esp | after:PL360; A_CRUSH; any visit |
| PL375 | I K | E arrival:AbandonedPrisonLocation 0ECF4C:Skyrim.esm | after:PL371; KAI_INIGO; any visit |
| PL376 | R G | E arrival:MarkarthEntranceLocation 0F0816:Lux Via - Markarth Entrance and Farm Overhaul.esp (Markarth Outskirts) | after:PL359; any visit |
| PL377 | X S | E arrival:MarkarthMushroomFarmLocation 00092D:Lux Via - Markarth Entrance and Farm Overhaul.esp | after:PL363; SERANA; any visit |

### PART 21 - SECOND VISITS  (53 talks)

| ID | Speakers | Type | Gates |
|---|---|---|---|
| PL378 | R C U | E arrival:BarleydarkFarmLocation 018C8C:Skyrim.esm | after:PL181; any visit |
| PL379 | K A | E arrival:ChillfurrowFarmLocation 018C90:Skyrim.esm | after:PL183; ASHE_REVEAL; any visit |
| PL380 | L G | E arrival:BrokenFangCaveLocation 01914D:Skyrim.esm | after:PL184; any visit |
| PL381 | R I | E arrival:RannveigsFastLocation 019290:Skyrim.esm | after:PL187; any visit |
| PL382 | V L U | E arrival:ShimmermistCaveLocation 01929D:Skyrim.esm | after:PL188; any visit |
| PL383 | I A | E arrival:IvyApothecaryLocation 0000C7:Ivy Riverwood Overhaul.esp | after:PL195; ASHE_REVEAL; any visit |
| PL384 | G U | E arrival:IvyRandalfShopLocation 000515:Ivy Riverwood Overhaul.esp (Enchanted Echoes) | after:PL330; any visit |
| PL385 | X V | E arrival:WSBankofHaafingarLocation AB5FEA:Grand Solitude - The Walls of High King Erling.esp | after:PL242; any visit |
| PL386 | L R U | E arrival:DeadMensRespiteLocation 019161:Skyrim.esm | after:PL255; any visit |
| PL387 | L K U | E arrival:SolitudeLighthouseExteriorLocation 10FE44:Skyrim.esm | after:PL236; K_CRUSH; any visit |
| PL388 | G U K | E arrival:WSANewPageLocation AB5FB6:Grand Solitude - The Walls of High King Erling.esp | after:PL243; G_FLIRT; K_CRUSH; any visit |
| PL389 | S K | E arrival:WeynonStonesLocation 0BC0AC:Skyrim.esm | after:PL268; SERANA; S_ROM; K_CRUSH; any visit |
| PL390 | R A | E arrival:GeirmundsHallLocation 019188:Skyrim.esm | after:PL312; ASHE_Q1; any visit |
| PL391 | I U | E arrival:RiftenMaraSquareTowerLocation 00AD40:Riften Expansion.esp (the "Guard Tower" on Mara's Square) | after:PL315; any visit |
| PL392 | R V | E arrival:RiftenHouseofClanWaveBreakerLocation 09E689:Riften Expansion.esp | after:PL320; any visit |
| PL393 | S A | E arrival:RiftenWeaveAndThreadLocation 0CC611:Riften Expansion.esp | after:PL326; SERANA; ASHE_REVEAL; any visit |
| PL394 | R G | E arrival:Thuldor_LocIvarsteadSmith 0135FA:Thuldor's Ivarstead.esp (The Mountain's Anvil) | after:PL330; any visit |
| PL395 | L A U | E arrival:CragwallowSlopeLocation 01915A:Skyrim.esm | after:PL285; ASHE_REVEAL; any visit |
| PL396 | G K | E arrival:DriftshadeSanctuaryLocation 01916E:Skyrim.esm | after:PL276; WOLF; any visit |
| PL397 | L G U | E arrival:LostEchoCaveLocation 019266:Skyrim.esm | after:PL206; any visit |
| PL398 | C G | E arrival:BilegulchMineLocation 019269:Skyrim.esm | after:PL207; any visit |
| PL399 | L X U | E arrival:SunderstoneGorgeLocation 061AE3:Skyrim.esm (in-game name "Greywater Gorge") | after:PL213; any visit |
| PL400 | I V U | E arrival:KnifepointRidgeLocation 08E1B7:Skyrim.esm | after:PL214; any visit |
| PL401 | C K U | E arrival:DragonBridgeFarmLocation 020006:Skyrim.esm | after:PL239; any visit |
| PL402 | L R U | E arrival:KjenstagRuinsLocation 0C2EF1:Skyrim.esm | after:PL253; any visit |
| PL403 | V G | E arrival:AngasMillLocation 018C8B:Skyrim.esm | after:PL258; any visit |
| PL404 | G I U | E arrival:FortDunstadStumblingSabrecatWorking 000351:Fort Dunstad.esp (The Stumbling Sabrecat) | after:PL263; any visit |
| PL405 | G X | E arrival:ForsakenCaveLocation 01917B:Skyrim.esm | after:PL261; any visit |
| PL406 | R V U | E arrival:MerryfairFarmLocation 018E3C:Skyrim.esm | after:PL304; any visit |
| PL407 | K A U | E arrival:PinepeakCavernLocation 019289:Skyrim.esm | after:PL313; ASHE_HIRED; any visit |
| PL408 | R C U | E arrival:AlchemistsShackLocation 0D566D:Skyrim.esm | after:PL318; any visit |
| PL409 | L I | E arrival:KynesgroveKynesbyLocationTGCoKG 0E5236:The Great Village of Kynesgrove.esp (in-game name "Kymesby") | after:PL297; any visit |
| PL410 | R V U | E arrival:RiftenRethanHoldingsLocation 01F652:Riften Expansion.esp | after:PL325; any visit |
| PL411 | L C | E arrival:HollyfrostFarmLocation 018E36:Skyrim.esm | after:PL284; any visit |
| PL412 | L K U | E arrival:LundsHutLocation 0E66A5:Skyrim.esm | after:PL192; any visit |
| PL413 | G L U | E arrival:GraniteHillLocation 018A48:Skyrim.esm | after:PL218; any visit |
| PL414 | G V U | E arrival:SRC_PSTPPinewatchCheckpointLocation 00132A:SRC - All In One.esp | after:PL224; any visit |
| PL415 | C G | E arrival:MarkarthEntranceWasteCollectorLocation 109D41:Lux Via - Markarth Entrance and Farm Overhaul.esp | after:PL364; any visit |
| PL416 | I S | E arrival:ClearpinePondLocation 019156:Skyrim.esm | after:PL230; SERANA; any visit |
| PL417 | C K | E arrival:BonechillPassageLocation 0FDA46:Skyrim.esm | after:PL217; any visit |
| PL418 | G U K | E arrival:FaldarsToothLocation 019175:Skyrim.esm | after:PL310; any visit |
| PL419 | R V | E arrival:RobbersGorgeLocation 01929B:Skyrim.esm | after:PL250; any visit |
| PL420 | K X U | E arrival:FalkreathWatchtowerLocation 0479B3:Skyrim.esm (in-game name "Crossroads Watchtower") | after:PL211; any visit |
| PL421 | L U K | E arrival:JourneymansNookLocation 0EF54C:Skyrim.esm | after:PL280; any visit |
| PL422 | L R | E arrival:WhistlingMineLocation 018E45:Skyrim.esm | after:PL274; any visit |
| PL423 | L G U | E arrival:StonyCreekCaveLocation 080F28:Skyrim.esm | after:PL290; any visit |
| PL424 | G K | E arrival:FortKastavLocation 019182:Skyrim.esm | after:PL277; any visit |
| PL425 | X I U | E arrival:PurewaterRunLocation 01928D:Skyrim.esm | after:PL347; any visit |
| PL426 | K L U | E arrival:HilariusFarmhouseLocation 000A77:Lux Via - Markarth Entrance and Farm Overhaul.esp | after:PL369; any visit |
| PL427 | G A | E arrival:HeartwoodMillLocation 018E33:Skyrim.esm | after:PL305; ASHE_REVEAL; any visit |
| PL428 | X S | E arrival:KynesgroveSteamscorchGullyMineLocation 020A07:Skyrim.esm | after:PL295; SERANA; any visit |
| PL429 | V K | E arrival:COTN_FalkreathWatchtowerLocation 0FDD35:COTN - Falkreath.esp | after:PL223; any visit |
| PL430 | L G | E arrival:LoreiusFarmLocation 018E3B:Skyrim.esm | after:PL259; any visit |

## Open items for the build

- IcerunnerLocation 01929E and GjukarsMonumentLocation 0A3F49 have no Name on the record; Gjukar's Monument also has no parent location, so use a distance check to the monument ref. BrinewaterGrottoLocation 05F428 is parented straight to Tamriel (hold not confirmed).
- In-game names that differ from the EditorID: Crabber's Shanty = "Crab Shack", FalkreathWatchtowerLocation = "Crossroads Watchtower", SunderstoneGorgeLocation = "Greywater Gorge", DarkwaterCavernLocation = "Darkwater Pass", the Kynesgrove mod's KynesbyLocation = "Kymesby".
- PL309 (Darkwater Pass) only says an Argonian went missing in there (the quest setup); it never says whether he lives.
- PL245 / PL396 name Farkas as a werewolf: gated WOLF (Companions secret known).
- Confirm `S_ROM` stage and the K01 completion stage (above).
