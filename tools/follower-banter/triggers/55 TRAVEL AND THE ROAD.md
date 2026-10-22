# Triggers - 55 TRAVEL AND THE ROAD (prefix TV, 200 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\55 TRAVEL AND THE ROAD.txt`
Written 2026-10-18. Writing only: nothing in the game, the profiles or the mods was touched. Northern Roads object names below were read (read-only) from `mods\Northern Roads\Northern Roads.esp` EditorIDs.

Speaker codes as TRIGGERS.md section 5 (K G V R X I L C) plus **S = Serana**, **A = Ashe**, **U = Luna** (player line, Eleonora voice; no Free() test).
Gate codes as TRIGGERS.md section 4, plus the follower gates defined in `triggers\43 WHAT LUNA DOES.md` (SERANA_F, S_VAMP, ASHE_F, ASHE_REVEAL) and the new ones below.
**Every talk in this file is E** (fires on the moment, or at the first safe tick after it; WorldQuiet() and Free() always apply). Every talk also needs each speaker pair's first-meeting talk already played (TRIGGERS.md "Chains").
**Cooldown note:** this file adds a lot of outdoor triggers. Suggest one TV talk per in-game hour at most, and Part 1 (HOLD) talks at most one per hold entry. Luna's navigation talks (TV190-TV200) max one per in-game day, shared with the N-section "lost" talks.

## How the controller sees the road

| Hook | What it gives us | Used for |
|---|---|---|
| `OnLocationChange(Location akOld, Location akNew)` + `akNew.IsChild(<Hold>HoldLocation)` / `GetInCurrentLoc` | which hold the player is in | HOLD:<Name> |
| 60 s poll: `Player.IsInInterior()`, `GetCurrentLocation().HasKeyword(LocTypeHabitation/LocTypeCity/LocTypeTown)`, `IsOnMount()`, `IsSwimming()`, `GetPositionZ()`, `Weather.GetCurrentWeather().GetClassification()`, `IsRaining/IsSnowing` equivalents as TRIGGERS.md | walking time, riding time, climbs, weather | WALK, RIDING, CLIMB, RAIN/SNOW/STORM |
| `Game.FindClosestReferenceOfAnyTypeInListFromRef(FormList, Player, radius)` (vanilla) | nearest object from a FormList of base forms | NR:<object>, SHRINE:<god>, HUNTERCAMP, farm/coast/waterfall markers |
| `OnPlayerFastTravelEnd(float afTravelGameTimeHours)` | fast travel / carriage / ship arrival | CARRIAGE_END, BOAT:Sea arrival |
| `Player.GetSitState()` + `GetFurnitureReference()` (SKSE/po3) on the 60 s poll | player seated in a moving carriage | CARRIAGE |

## New gate codes for this file

**Places**
- `HOLD:<Name>` = player exterior, not in a City/Town/Habitation location, and the current location is (a child of) `WhiterunHoldLocation`, `ReachHoldLocation`, `RiftHoldLocation`, `EastmarchHoldLocation`, `PaleHoldLocation`, `HjaalmarchHoldLocation`, `HaafingarHoldLocation`, `FalkreathHoldLocation` or `WinterholdHoldLocation` (Skyrim.esm). "(first entry from another hold)" = the previous hold seen by the controller was a different one. **[UNCONFIRMED: check every exterior wilderness location in this load order is parented to its hold location; Northern Roads and city overhauls may add unparented ones]**
- `SIGHT:<Place>` = exterior, distance from the place's map-marker ref between 6000 and 20000 units, player moving towards it (distance falling over two ticks), first time this game for that place. Markers: Whiterun, Solitude, Markarth, Riften, Windhelm, College of Winterhold, High Hrothgar, Falkreath, Morthal map markers **[pick refs at build]**. `SIGHT:any town` = same test against any LocTypeTown/City marker.
- `CLIFFROAD` = on foot, exterior, with a drop of 1500+ units within 600 units of the player (sample terrain with a short ray/`GetPositionZ` of nearby refs) **[proxy; cheaper fallback: a hand-picked list of cliff-road and gorge markers per hold]**.
- `RIVER` = `IsSwimming()` or water up to the waist (po3 `IsActorInWater`) in an exterior that is not a lake/sea cell **[proxy: any exterior water]**.
- `CLIMB` = on foot, exterior, Z rose 1500+ within 3 real minutes. `CLIMB_TOP` = after CLIMB, Z stopped rising for 30 s. `DESCENT` = Z fell 1500+ within 3 minutes on foot.

**Time on the road**
- `WALK:n` = player on foot outdoors (exterior, not City/Town/Habitation location, not mounted, not sitting) for **n real minutes in a row**. Timer resets on: entering an interior or a town, fast travel, sleeping, combat, mounting.
- `RIDING:n` = player `IsOnMount()` for n real minutes in a row ("RIDING" alone = 2 minutes). "X mounted" = that follower's `IsOnMount()` is true on the same tick.

**Northern Roads objects** (`NR:<name>`): build one FormList per name from these Northern Roads.esp base EditorIDs (all confirmed present):
- SignPost: `COTN_RoadSignPost` (+ vanilla signpost statics). Runestone: `COTN_Runestone01-04`, `COTN_Runestone01Snow/02Snow`.
- DragonTotem: `COTN_DragonTotemOld01/02` (+Snow, _Blue, Long variants), `COTN_DragonTotemWR01/02/WRLong01`.
- NordTotem: `COTN_NordTotem01/02` (+Snow), `COTN_WHTotem01`, `COTN_WHTotemLong`. DeerSkullTotem: `COTN_DeerSkullTotem01/02`.
- ForswornTotem: `COTN_MammothSkullForsworn`, `COTN_ForswornBanner/02/03`. HoldBanner: `COTN_BannerPost`, `COTN_*BannerThin*`.
- RiftBorderPost / RiftStockade: `COTN_RTBorderGate01`, `COTN_RTStockade01`, `COTN_RTWatchtower01`, `COTN_RTGuardHouse`, `COTN_RTWall01`, `COTN_RTWallGate`.
- AbandonedCart: `COTN_Cart01`, `COTN_Cart01Snow` (crates: `COTN_CratesCovered01/02`). WaysideStop: `COTN_TentNord01`.
- BoatBridge: `COTN_BridgeRowBoat01Anim/02Anim/03Anim`. StoneBridge: `COTN_BridgeStone*`, `COTN_SBridge01RoadStone`, `COTN_RockBridge01/02`. RopeBridge: `COTN_Rope01-03` near `COTN_BridgeWood*` pieces **[confirm the rope bridges are NR objects; else use vanilla rope-bridge statics]**.
- FishRack: `COTN_Fishrack01/02`. LobsterCage: `COTN_LobsterCage`. SnowShipwreck: `COTN_ShipwreckLarge01Snow`.
- Plank walkways in Hjaalmarch: `COTN_BridgeWoodSmallMid01`, `COTN_BridgeWoodMid01-03` within HOLD:Hjaalmarch.

**Roadside events**
- `SHRINE:<god>` = a vanilla wayside shrine activator of that god within 800 units (TempleShrine/roadside shrine bases for Kynareth, Arkay, Julianos, Dibella, Stendarr, Akatosh) **[FormList at build]**. Never fires inside temples.
- `CORPSE_TRAVELLER` = a dead actor within 1500 units, exterior, not in a hostile faction (not BanditFaction, ForswornFaction, VampireFaction, Thalmor, DragonPriest, creature race), not killed by the player or a follower in the last 5 minutes. **Do not stack with 56 WORLD ENCOUNTERS dead-body talks (WE53, WE67, WE76): if a WE encounter quest is running at that spot, skip TV120-TV122.**
- `HUNTERCAMP` = a bedroll or tent plus a campfire within 1500 units, no live NPC within 2000, not a bandit camp location (no LocTypeBanditCamp) **[vanilla unmarked hunter camps; FormList of bedroll/tent bases]**.

**Riding and travel**
- `KIAI` = Kaidan has his horse Kiai **[UNCONFIRMED: find which plugin/global gives Kaidan the horse named Kiai (IF horse system or the user's own patch) and test "Kiai's ref is enabled and owned by Kaidan"]**.
- `G_HORSE` = `HD1GoreHorse1` (Count Fleet) completed.
- `WINDWARD` = Val has his horse Windward **[UNCONFIRMED: Val's horse alias/global in AX ValSerano.esp]**.
- `BIGPIG` = Redcap has found Bigpig ("The Village" done; FL144 uses the same moment) and Bigpig travels with him **[UNCONFIRMED stage in Redcap's village quest]**.
- `LUC_ADMIT` as TRIGGERS.md (Clive). `SERANA_HORSE` = `SDA_GetHorseQuest` completed.
- `KAI_AKAVIRI` = Kaidan's Akaviri cache quest (KINV "All of this Past") completed, so he knows his mother's people **[confirm stage]**.
- `GORE_READS` = Gore has learned to read: `HLIOGoreReading` (6F46A0:HLIORemi.esp) at its last value, or `HD1MemoriesRestored` (Gore - Vigilant) == 1.
- `V_BOAT` = Val006 "Safe Harbor" stage 20 done (Spring Rain bought).
- `CARRIAGE` = player seated in a moving Animated Carriage for 60 s (furniture keyword/base from Animated Carriage; **[confirm the seat furniture base]**), with at least the talk's followers in the carriage or within 1000 units. `CARRIAGE_END` = `OnPlayerFastTravelEnd` after a carriage fare, or the Animated Carriage arrival.
- `BOAT:Sea` = arriving at Raven Rock docks from Windhelm or back (Gjalund / Northern Maiden) — `OnPlayerFastTravelEnd` with the worldspace changing between Tamriel and DLC2SolstheimWorld. `BOAT:Row` = player activating or sitting in a rowing boat (Icewater Jetty and other rowboat travel) **[confirm which rowboat mods are active]**. `BOAT:SpringRain` = player aboard Val's Spring Rain (Val006 sailing scene). `BOAT:any` = any of these.

## Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| TV1 | G V U | E HOLD:Whiterun (first entry from another hold) | — |
| TV2 | X I | E HOLD:Whiterun + windy (GetWindSpeed >= 0.5) | — |
| TV3 | K L | E HOLD:Whiterun + WALK:3 | — |
| TV4 | R C | E HOLD:Whiterun, giant or mammoth within 4000 | — |
| TV5 | K U | E HOLD:Whiterun, within 4000 of a Whiterun farm (Pelagia, Chillfurrow, Battle-Born, Loreius) [farm marker list at build] | — |
| TV6 | R X | E on the Dwemer-paved road near Markarth (proxy: within 5000 of the Markarth exterior gate, exterior) | Remi/Xel not fallen out |
| TV7 | G I | E NR:ForswornTotem (COTN_MammothSkullForsworn / COTN_ForswornBanner* within 800) | — |
| TV8 | V L | E HOLD:Reach, within 3000 of a Karth River waterfall [marker list at build] | — |
| TV9 | C K | E HOLD:Reach + (fog weather or hour 18..21) | — |
| TV10 | S U | E HOLD:Reach + CLIFFROAD | SERANA_F |
| TV11 | K U | E HOLD:Rift (first entry from another hold) | K_CRUSH |
| TV12 | V G | E NR:RiftBorderPost (COTN_RTBorderGate01 / COTN_RTStockade01 / COTN_RTWatchtower01 within 1500) | — |
| TV13 | I R | E HOLD:Rift + WALK:5 | — |
| TV14 | L X | E HOLD:Rift, within 3000 of the Lake Honrich shore, MORNING, fog weather | — |
| TV15 | A U | E HOLD:Rift, within 8000 of Ashe's workshop exterior | ASHE_F; ASHE_REVEAL (MM_AMQ_01 started) |
| TV16 | X V | E HOLD:Eastmarch (first entry from another hold), near steam vents [hot-spring marker list] | — |
| TV17 | C G | E HOLD:Eastmarch, within 2000 of a hot spring or steam vent | — |
| TV18 | I K | E HOLD:Eastmarch + snow on the ground (snow region) + WALK:5 | — |
| TV19 | L K | E HOLD:Eastmarch, within 1500 of a hot spring | — |
| TV20 | R U | E HOLD:Eastmarch volcanic tundra road (proxy: HOLD:Eastmarch + WALK:5, not snow region) | — |
| TV21 | G K | E HOLD:Pale + STORM or blizzard weather | — |
| TV22 | R C | E HOLD:Pale + SNOW | — |
| TV23 | L U | E HOLD:Pale (first entry from another hold) | — |
| TV24 | X S | E HOLD:Pale + SNOW | SERANA_F; S_VAMP |
| TV25 | I V | E HOLD:Pale, within 4000 of the north coast (Sea of Ghosts in view) [coast marker list] | — |
| TV26 | X R | E HOLD:Hjaalmarch (first entry from another hold) (marsh) | Remi/Xel not fallen out |
| TV27 | L K | E HOLD:Hjaalmarch + fog weather | — |
| TV28 | G C | E HOLD:Hjaalmarch, on a plank walkway (NR wood bridge piece within 300) | — |
| TV29 | U X | E HOLD:Hjaalmarch + WALK:3, nirnroot or deathbell within 1500 | — |
| TV30 | I S | E HOLD:Hjaalmarch + NIGHT | SERANA_F |
| TV31 | V U | E HOLD:Haafingar coast road (within 4000 of Solitude harbour / Karth estuary) [marker] | — |
| TV32 | G K | E HOLD:Haafingar, within 6000 of the Thalmor Embassy exterior | — |
| TV33 | L R | E on the bridge at Dragon Bridge (within 800 of the bridge centre) | — |
| TV34 | I R | E HOLD:Haafingar + windy + clear weather | — |
| TV35 | A G | E HOLD:Haafingar + WALK:3 in a gorge (CLIFFROAD) | ASHE_F |
| TV36 | L U | E HOLD:Falkreath (first entry from another hold) | JRLucienIntro >= 30 |
| TV37 | K I | E HOLD:Falkreath, within 3000 of a lake shore [marker list] | Kaidan-Inigo intro done (KaiandInigo >= 10) |
| TV38 | R G | E HOLD:Falkreath + WALK:3 | — |
| TV39 | S K | E HOLD:Falkreath + sunny (IsPleasant, hour 8..18) | SERANA_F; S_VAMP |
| TV40 | X U | E HOLD:Falkreath, within 3000 of the Lake Ilinalta shore | — |
| TV41 | K C | E HOLD:Winterhold coast, horker within 3000 | — |
| TV42 | R A | E HOLD:Winterhold, on glacier ice (NR glacier landscape; proxy: north-coast markers) | ASHE_F |
| TV43 | L U | E within 3000 of the Winterhold cliff edge (town exterior) | MG_JOIN |
| TV44 | I X | E HOLD:Winterhold + SNOW + WALK:3 | — |
| TV45 | V G | E HOLD:Winterhold coast, ice floes in view [coast marker] | — |
| TV46 | C U | E WALK:10 | — |
| TV47 | L K | E WALK:15 | — |
| TV48 | R V U | E WALK:10 | — |
| TV49 | C X | E WALK:10 | after PY53 |
| TV50 | U K | E WALK:10 | — |
| TV51 | L X | E WALK:10 | — |
| TV52 | V G U | E WALK:10 | — |
| TV53 | A I U | E WALK:10 | ASHE_F; ASHE_REVEAL |
| TV54 | L G | E WALK:10 | — |
| TV55 | V K U | E WALK:3 + CLIFFROAD | K_CRUSH |
| TV56 | R X G | E WALK:10 | — |
| TV57 | I X | E WALK:10 | — |
| TV58 | R V | E WALK:10 | — |
| TV59 | L S | E WALK:10 | SERANA_F |
| TV60 | G I | E WALK:10 | — |
| TV61 | K U | E WALK:15 with no talk in the last 10 min | K_TOG+ |
| TV62 | L I | E WALK:10 | — |
| TV63 | V X | E WALK:10 | — |
| TV64 | G A | E WALK:10 | ASHE_F; ASHE_REVEAL |
| TV65 | U X | E WALK:10 | — |
| TV66 | R K | E WALK:10 | — |
| TV67 | L R C | E WALK:10 | — |
| TV68 | V I | E WALK:10 | — |
| TV69 | U G | E WALK:10 | — |
| TV70 | V K | E WALK:10 | — |
| TV71 | L U | E WALK:10 | — |
| TV72 | R X | E WALK:10 | — |
| TV73 | C G | E WALK:10 | — |
| TV74 | C I | E WALK:10 on open ground (HOLD:Whiterun or HOLD:Hjaalmarch) | — |
| TV75 | G V | E WALK:10 | — |
| TV76 | G K U | E WALK:10 | — |
| TV77 | S U | E WALK:10 | SERANA_F |
| TV78 | L A | E WALK:20 | ASHE_F; ASHE_REVEAL |
| TV79 | R I | E WALK:10 | — |
| TV80 | V K | E WALK:10 | BRYNJAR (Kaidan quotes "me old man") |
| TV81 | C L | E CLIFFROAD (gorge or canyon) | — |
| TV82 | G K U | E WALK:20 | — |
| TV83 | K U | E WALK:10 | K_LOVE+ |
| TV84 | X K | E WALK:15 | — |
| TV85 | R U | E WALK:10 | — |
| TV86 | V U | E RAIN + WALK:3 | — |
| TV87 | U R | E RAIN | after TV86, 3+ game days later |
| TV88 | L C | E RAIN + WALK:3 | — |
| TV89 | K I | E STORM, exterior | — |
| TV90 | G R | E RIVER | — |
| TV91 | X L | E RIVER (fast water) | — |
| TV92 | K S | E RIVER | SERANA_F; S_VAMP |
| TV93 | C I | E RIVER (shallow stream) | — |
| TV94 | L K | E CLIMB | — |
| TV95 | C G | E CLIMB, high (player Z above 20000 or near a drop) | — |
| TV96 | R X | E CLIMB, high | Remi/Xel not fallen out |
| TV97 | A U | E CLIMB_TOP | ASHE_F |
| TV98 | R I | E DESCENT in a snow region | — |
| TV99 | V G | E RAIN + WALK:10 | — |
| TV100 | C L | E SNOW + WALK:3 | — |
| TV101 | L V | E windy (GetWindSpeed >= 0.7), exterior | — |
| TV102 | V U | E STORM with lightning (thunderstorm weather) | — |
| TV103 | K G | E STORM (hail or sleet weather where the weather mod has it, else STORM) | — |
| TV104 | R X | E RAIN stopped within the last game hour + WALK:3 | Remi/Xel not fallen out |
| TV105 | I U | E RAIN just stopped and the sky is clearing | — |
| TV106 | U L | E NR:SignPost (COTN_RoadSignPost or a vanilla signpost within 500) | — |
| TV107 | I K | E NR:SignPost (another signpost) | Kaidan-Inigo intro done |
| TV108 | U X | E NR:Runestone (COTN_Runestone* within 600) | — |
| TV109 | L G | E NR:DragonTotem (COTN_DragonTotem* within 600) | — |
| TV110 | C I | E NR:DeerSkullTotem (COTN_DeerSkullTotem* within 600) | — |
| TV111 | R V | E NR:HoldBanner (COTN_BannerPost or *BannerThin* within 600) | — |
| TV112 | U K | E SHRINE:Kynareth | K_TOG+ |
| TV113 | G X | E SHRINE:Arkay or a roadside grave within 800 | — |
| TV114 | L U | E SHRINE:Julianos | — |
| TV115 | S V | E SHRINE:Dibella | SERANA_F |
| TV116 | I R | E SHRINE:Stendarr | — |
| TV117 | S U | E SHRINE:Akatosh | SERANA_F |
| TV118 | R G | E NR:AbandonedCart (COTN_Cart01 / COTN_Cart01Snow within 600) | — |
| TV119 | V K | E NR:AbandonedCart with COTN_CratesCovered* within 600 of it | — |
| TV120 | L I | E CORPSE_TRAVELLER | — |
| TV121 | G U | E CORPSE_TRAVELLER | — |
| TV122 | R X | E CORPSE_TRAVELLER | Remi/Xel not fallen out |
| TV123 | K I | E HUNTERCAMP | Kaidan-Inigo intro done |
| TV124 | L S | E HUNTERCAMP | SERANA_F |
| TV125 | G C | E HUNTERCAMP with a lit campfire | — |
| TV126 | V X | E NR:BoatBridge (COTN_BridgeRowBoat* within 400) | — |
| TV127 | K R | E NR:RopeBridge (approaching a rope/plank bridge within 600) | — |
| TV128 | U L | E NR:StoneBridge (COTN_BridgeStone* / COTN_SBridge01RoadStone within 600) | — |
| TV129 | G K V | E NR:WaysideStop (COTN_TentNord01 within 800, no NPC) | — |
| TV130 | I X | E NR:FishRack (COTN_Fishrack* within 800) | — |
| TV131 | C V | E NR:LobsterCage (COTN_LobsterCage within 600) | — |
| TV132 | A K | E NR:RiftStockade (COTN_RTStockade01 / COTN_RTWatchtower01 / COTN_RTGuardHouse within 1000) | ASHE_F; ASHE_REVEAL |
| TV133 | L G | E NR:Runestone or NR:SignPost (any roadside marker) | GORE_READS |
| TV134 | I S | E NR:NordTotem (COTN_NordTotem* within 800) or roadside cairn | SERANA_F |
| TV135 | V C | E NR:SnowShipwreck (COTN_ShipwreckLarge01Snow within 1500) | — |
| TV136 | G K | E RIDING:2, Kaidan and Gore mounted | KIAI; G_HORSE |
| TV137 | R K | E RIDING:2, Kaidan mounted | KIAI; KAI_AKAVIRI; after TV136 |
| TV138 | V K | E RIDING:2, Kaidan and Val mounted | KIAI; WINDWARD |
| TV139 | K I | E RIDING:2, Kaidan mounted | KIAI; Kaidan-Inigo intro done |
| TV140 | G U | E RIDING:2, Gore mounted | G_HORSE |
| TV141 | R G | E RIDING:2, Gore mounted | G_HORSE |
| TV142 | S V | E RIDING:2, Val mounted | WINDWARD; SERANA_F |
| TV143 | V L | E RIDING:2, Val and Lucien mounted | WINDWARD; LUC_ADMIT |
| TV144 | G C | E RIDING:2, Redcap on Bigpig | BIGPIG |
| TV145 | C V | E RIDING:3, Redcap on Bigpig, Val mounted | BIGPIG; WINDWARD; after PL174 |
| TV146 | I X | E RIDING:3, Xelzaz and Inigo on foot | — |
| TV147 | K U | E RIDING + player casts a Destruction spell while mounted | — |
| TV148 | L G | E RIDING:2, Lucien mounted, within 7 game days of LUC_ADMIT | LUC_ADMIT |
| TV149 | R V | E RIDING:2, Val mounted, Remi along (Remi riding pillion is flavour; no mount check) | WINDWARD |
| TV150 | K U | E RIDING:2, Kaidan mounted | KIAI; K_TOG+ |
| TV151 | G U | E RIDING:2 | after PA48 |
| TV152 | S G | E RIDING:2, Serana mounted | SERANA_HORSE |
| TV153 | K A | E RIDING:2, Ashe on foot | ASHE_F; ASHE_REVEAL; KIAI |
| TV154 | G K U | E RIDING at a gallop for 30 s, Gore and Kaidan mounted | G_HORSE; KIAI |
| TV155 | R L | E RIDING up a steep slope (Z +800 within 30 s while mounted) | — |
| TV156 | I U | E player mounts own horse after 3+ game days without riding | — |
| TV157 | U X | E RIDING:3 | after PA48 |
| TV158 | G K U | E CARRIAGE | — |
| TV159 | V K U | E CARRIAGE | K_CRUSH |
| TV160 | L C | E CARRIAGE | — |
| TV161 | I X | E CARRIAGE | — |
| TV162 | X V | E CARRIAGE | — |
| TV163 | L G | E CARRIAGE | — |
| TV164 | R U | E CARRIAGE | — |
| TV165 | S K | E CARRIAGE + sunny | SERANA_F; S_VAMP |
| TV166 | G A | E CARRIAGE | ASHE_F; ASHE_REVEAL |
| TV167 | G C | E CARRIAGE | — |
| TV168 | R I | E CARRIAGE_END | — |
| TV169 | V U | E CARRIAGE_END | — |
| TV170 | G V | E BOAT:Sea arrival (Northern Maiden) | — |
| TV171 | C U | E BOAT:Sea to or from Solstheim | SOLST |
| TV172 | V L | E BOAT:Sea arrival (Gjalund's ship) | — |
| TV173 | R K | E BOAT:Row | — |
| TV174 | I X | E BOAT:Row | — |
| TV175 | L S | E BOAT:Sea | SERANA_F |
| TV176 | V U | E BOAT:SpringRain | V_BOAT |
| TV177 | V I | E BOAT:any + CLEARNIGHT | — |
| TV178 | C R | E BOAT:Row | — |
| TV179 | G K U | E BOAT:Sea arrival (stepping onto the dock) | — |
| TV180 | K U | E SIGHT:Whiterun | — |
| TV181 | L V | E SIGHT:Solitude | — |
| TV182 | R X | E SIGHT:Markarth | Remi/Xel not fallen out |
| TV183 | I G | E SIGHT:Riften | — |
| TV184 | X V | E SIGHT:Windhelm | — |
| TV185 | U L | E SIGHT:College | MG_JOIN |
| TV186 | C G | E SIGHT:HighHrothgar | — |
| TV187 | L K | E SIGHT:Falkreath (town edge, from the road) | — |
| TV188 | R S | E SIGHT:Morthal + fog weather | SERANA_F |
| TV189 | G K U | E SIGHT:any town after WALK:15 | — |
| TV190 | V U | E CLEARNIGHT + (WALK:5 or RIDING) | — |
| TV191 | U K | E WALK:5, Throat of the World in view (proxy: HOLD Whiterun, Rift, Eastmarch or Falkreath, clear weather) | — |
| TV192 | L U | E WALK:5 while a quest objective is active | — |
| TV193 | L U | E RIDING at a road fork (NR:SignPost within 800) | LUC_ADMIT |
| TV194 | R U | E WALK:3 within one game hour of leaving a DWEMER location | — |
| TV195 | C U | E outdoors within 3000 of an INN exterior | — |
| TV196 | U K | E at a road fork (NR:SignPost within 800) | K_TOG+ |
| TV197 | A U G | E WALK:5 | ASHE_F; ASHE_REVEAL |
| TV198 | V U | E WALK:5 in the mountains (player Z above 15000), off the road | — |
| TV199 | S U | E WALK:5 within 2000 of a signpost | SERANA_F |
| TV200 | V G K | E WALK:10 | 5+ of TV190-TV199 played |

## Open items to verify at build
- KIAI, WINDWARD, BIGPIG: where each follower mod stores the horse/pig and whether it travels with the follower.
- KAI_AKAVIRI stage (KINV) for TV137.
- HOLD parenting of wilderness locations; SIGHT marker refs and distance band per city (Markarth sits in a gorge: use 4000-12000).
- CLIFFROAD / RIVER / CLIMB proxies: cost of terrain sampling vs a hand-placed marker list.
- Animated Carriage seat furniture base and arrival event; rowboat travel mods in the order.
- SHRINE FormList and HUNTERCAMP bedroll/tent FormList.
- CORPSE_TRAVELLER must not overlap World Encounters (56) dead-body talks or fire on bodies the party just killed.
- TV149: Remi riding behind Val is flavour only (no pillion mechanic).
