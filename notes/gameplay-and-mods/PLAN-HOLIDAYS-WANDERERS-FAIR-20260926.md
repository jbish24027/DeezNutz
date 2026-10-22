# Plan: Holidays + The Wanderer's Fair (2026-09-26)

Status: EXECUTED 2026-09-30 (as-built ledger: `MODS-ADDED-20260930-HOLIDAYS-WANDERERS-FAIR.md`). Written 2026-09-26 as the analysis; the numbers below are from that probe. Profile probed: `DEEZ CS NUTZ - PBR`
(houseCARL 2.0.0, epoch e2-f136132fb1c6f29f), MO2 and the game closed at probe time.

Scratch analysis (record census, conflict geometry, cell provider matrix) lives in the session scratchpad;
the durable numbers are in this file.

---

## 1. Verdict

Both mods fit the instance. Two full plugin slots, two new Reqtificator masters, one new MCM. The real work
is not Requiem (almost nothing needs a record edit) but three side issues:

1. **The known freeze at the fair.** Seven SPID lines in five installed mods hand every NPC a scripted or
   cloak ability; the fair puts ~120 NPCs in one place and the script engine drowns about a minute after
   arrival. Fix = add `-SkyrimFairNPC` to those seven lines (the author's own recipe, extended to the four
   extra mods this list has).
2. **Holidays decorations vs the city overhauls.** Holidays hangs ~3,500 lanterns, ropes, banners and
   pumpkins into 136 vanilla cells from 2017 geometry. This list rebuilds nearly every settlement. No
   patches exist for these overhauls except one (Whiterun Circle Trellis REMOVED). Expect clipping; audit
   in game, then I build move/disable patches per settlement.
3. **The MCM ceiling.** The list registered 127 menus this morning (cap 128; 137 menus competed). Holidays
   adds one menu, Professional Dancer another.

---

## 2. The 14 downloads

| # | Archive | Use? | Why |
|---|---|---|---|
| 1 | SkyrimFair 2.0.1.2 (The Wanderer's Fair, Nexus 193042) | **Install** | The fair. 4,551 own records, full plugin (cannot be light). Master: Holidays.esp. |
| 2 | SkyrimFair 1.0.0 Compatibility Patch | **Use as recipe, not a mod** | README + `skyrimfair_spid_patcher.py`. Its target list covers Stealth Detection Fixes only on this list; I extend the same one-word edit to four more mods (section 5a). |
| 3 | Holidays v2.20 Alpha 1 (Nexus 1533) | **Install** | 4,256 own records, full plugin. Masters Skyrim + Update only. Overrides 136 cells, 76 refs, 6 worldspaces. |
| 4 | Holidays 4K (74609) | **Install** above Holidays | 99 BC7 textures, replaces the BSA textures. |
| 5 | Fixed Script for Holidays (88254) | **Install** above Holidays | Replaces `_holidayfreeinn.pex` (infinite recursion in inns with <7 beds). Needs po3 Papyrus Extender: present. |
| 6 | Descriptions for Various Mods 2.6.1 (106229) | **Install ONE file** | Only `Holidays_DESC.ini` (3 lines: gift satchels + lucky coin) applies. Goes in a tiny addon folder above Holidays. Description Framework is present. |
| 7 | Lil Patches 2.3.6 (105436) | **Skip** | Its only Holidays patch targets the *HS* Candlehearth Hall. This list runs JK's Candlehearth Hall. Nothing else in it is Holidays-related. |
| 8 | JK's Interiors Patch Collection 5.29.1 (35910) | **Extract one ESP** | Installed is 5.28.1; the 5.29/5.29.1 changes touch nothing this list runs. Only `JKs Palace of the Kings - Holidays Patch.esp` applies (JK's Palace of the Kings is installed). `JKs Winking Skeever - Holidays patch.esp` needs JK's The Winking Skeever: not installed, skip. |
| 9 | HSF Holiday Dancing (172341) | **Install** | OAR replacers for the Cicero jig on Holidays' dance packages (11 package FormIDs, 40% random per dance). Needs OAR + Holidays. |
| 10 | slightly Better Bunting 1.1 from **Festival Rings - Animated** (149031) | **Install** | Animated ring + rope mesh, SBB-compatible variant. |
| 11 | slightly Better Bunting - FYX 3D Sighpost 1.2 (142315) | **Install** above FYX - 3D Solitude SighPost | The SBB rope mesh + flag texture for the FYX signposts already in use. |
| 12 | Holidays - slightly Better Bunting FOMOD 1.1 (156872) | **Install, option "I DO use this mod"** | ESL-flagged patch (13 STAT overrides + 2 texture sets) + 15 per-hold rope textures. The AnimatedRings variant pairs with #10. |
| 13 | Holidays -x- Light Placer (160128) | **Install** above Holidays | Two Light Placer jsons (lantern colours by fabric, pumpkins). Light Placer 4.2.1 present. |
| 14 | Professional Dancer 1.5.0 (124608) | **Install, plugin unticked for now** | Optional crowd dances for the fair. FNIS-style behaviour file (`FNIS_Dance_Behavior.hkx`); it does nothing until the behaviour cache is next rebuilt with it. With `Dance.esp` active the fair *detects* it and would hand its dancers animations that have no behaviour yet, so the plugin stays off until then. Adds an MCM (menu-only; every setting is a global with a console equivalent). Masters SkyUI_SE + UIExtensions: present. |

### Extra downloads worth fetching (manager-only pages, so they are yours to click)

- **mwee's Holidays Patches (189598)** → file "Whiterun Circle Trellis REMOVED Holidays Patch" (disables the lanterns where the trellis was). This list runs Whiterun Circle Trellis REMOVED.
- **Holidays - Random Start Date Fix (179002)** → the MCM's random start-date option is broken in 2.20A1; this re-implements it. Optional, tiny.
- Not applicable (checked): SFO patch, Happy Little Trees patch, Dawn of Skyrim, Great Cities of JK's North, Minor Cities Dawnstar, Shor's Stone / Ivarstead (this list runs RedBag's / Thuldor's), Open Cities.

---

## 3. Budgets

| Budget | Now | After | Cap |
|---|---|---|---|
| Full plugins, PBR profile | 240 | 242 (Holidays.esp, SkyrimFair.esp) | 254 |
| Full plugins, other profiles | CS 240 · PICTA 241 · DEEEZ 230 · Reforged 197/206 | +2 each | 254 |
| Reqtificator masters | 225 | 227 | 254 |
| MCM menus (last session, Papyrus log 05:11 today) | 127 registered, 137 competing | +1 (Holidays); +2 once Dance.esp goes live | 128 |

Every other new plugin is ESL-flagged and costs nothing: `Dance.esp`, `JKs Palace of the Kings - Holidays
Patch.esp`, `Holidays - better bunting patch.esp`, the Authoria patch I build.

**MCM decision needed.** Holidays' menu holds the toggles (Go Celebrate, Gear, Decorations are plain globals)
and the start-date/birthday randomiser (only the menu does that). Professional Dancer's menu is toggles only,
all mirrored by globals. Options:
- (a) Keep Holidays' menu, leave Dance.esp off until the behaviour rebuild; when it goes live, cut its menu
  with the existing MCM Slot Trim patch (new game only). Net +1 menu. **Recommended.**
- (b) Keep both menus. Net +2 in the lottery; two more menus miss the list at each new game.
- (c) Cut Holidays' menu too (set its three globals by SkyPatcher; lose the randomiser). Net 0.

---

## 4. Where everything goes (all six profiles, same neighbours)

Modlist is descending priority (line 1 = bottom of the MO2 pane). "Above X" below means *higher priority
than X*, the way every existing patch here sits (e.g. `Cities of the North - Falkreath - Hotfix` above
`Cities of the North - Falkreath`).

### Mod folders

| Block (MO2 header) | Order top→bottom in the pane | Notes |
|---|---|---|
| Gameplay - Immersion (head of block) | **Holidays** → Holidays 4K → Fixed Script for Holidays → Holidays - Random Start Date Fix (if fetched) → Holidays -x- Light Placer → Holidays - slightly Better Bunting Patch → Descriptions - Holidays (ini only) → Whiterun Circle Trellis REMOVED - Holidays Patch (if fetched) → **houseCARL - Authoria - Patch - Holidays and Fair - Requiem** | One stack, base at the top. |
| Quests and Newlands - Misc (head of block) | **The Wanderer's Fair** | Its assets (meshes\SkyrimFair, textures\barry_*, its own voice folder, OAR folders, Scripts\SkyrimFair*) collide with nothing. |
| Animations - Idles and Actions, next to HSF Female Cross Legged Animations | HSF Holiday Dancing → Professional Dancer | Same author's other packs live here. |
| City Stuff - Patches, directly above JK's Interiors Patch Collection - rerun | JK's Interiors Patch Collection - Holidays (PotK) | The single ESP from 5.29.1. |
| FYX Meshes, directly above FYX - 3D Solitude SighPost | slightly Better Bunting - FYX 3D Sighpost → Festival Rings - Animated (SBB) | Beats Mesh Improvement Compilation (line ~3274, currently wins the rope mesh). |

### Plugins (loadorder.txt / plugins.txt / plugingroups.txt)

| Plugin | After | Group |
|---|---|---|
| `Holidays.esp` | `WetAndColdSPIDPatch.esp` (isoku's other mod) | Gameplay - Early Loaders |
| `Holidays - better bunting patch.esp` (light) | `Holidays.esp` | Gameplay - Early Loaders |
| `SkyrimFair.esp` | `ImperialMail - Bruma.esp` (end of the group) | Quests and Newlands - Misc |
| `Dance.esp` (light, **unticked**) | `SkyrimFair.esp` | Quests and Newlands - Misc |
| `JKs Palace of the Kings - Holidays Patch.esp` (light) | `JKs Palace of the Kings - Sons of Skyrim patch.esp` | Visuals - Cities and Towns |
| `Authoria - Patch - Holidays and Fair - Requiem.esp` (light) | `Authoria - Reqtificated - Sorceress Attire.esp` (Authoria - Reqtificated block) | Authoria - Reqtificated |
| Trellis Holidays patch (if fetched) | after both its masters, beside `Whiterun Circle Trellis REMOVED.esp` | Visuals - Cities and Towns |

Why Holidays loads early: its 136 cell overrides carry 2017 lighting/water/imagespace/music subrecords and
its 76 vanilla-ref edits are enable-parents on market props and Solitude's flags. Loading before every city
overhaul, Lux/Lux Orbis and Northern Roads means those win the cell record and the prop positions, and
Holidays only contributes its own placed decorations. The fair loads after Holidays (master) and before
the city/road blocks; its 4 Tamriel cell overrides lose to Synthesis Worldspace as intended, its 37 shrub
and rock disables are contested by nothing but USSEP (which it correctly out-loads).

---

## 5. Things I build or edit

### 5a. Fair crowd exclusion for SPID (the freeze fix)

Scan of every `*_DISTR.ini` in mods\ (mod-root files): 5 mods hand *every* NPC a spell with no other filter.

| Mod | File | Effect type | Edit |
|---|---|---|---|
| Stealth Detection Fixes | `StealthKillDetectionFix_Attack_DISTR.ini` | two **Cloak** effects | `NONE` → `-SkyrimFairNPC` (author's line) |
| Stealth Detection Fixes | `StealthKillDetectionFix_DISTR.ini` | Script effect | `ActorTypeNPC` → `ActorTypeNPC,-SkyrimFairNPC` (author's line) |
| Stealth Detection Fixes | `StealthKillDetectionFix_Killmove_DISTR.ini` | value modifier | `NONE` → `-SkyrimFairNPC` (author's line) |
| Brawling - No Hitting Bystanders | `Brawling - No Hitting Bystanders_DISTR.ini` | Script effect | `ActorTypeNPC` → `ActorTypeNPC,-SkyrimFairNPC` |
| Ash Nomad - Bedrolls - Use Those Blankets patch | `Ash Nomad - BOS Use Those Blankets Patch_DISTR.ini` | Script effect | same |
| Simply Order Summons | `talkToSummons_DISTR.ini` | Script effect, no filter at all | append `\|-SkyrimFairNPC` |
| Swiftly Order Squad | `Quick Follower Commands_DISTR.ini` | Script effect, no filter at all | append `\|-SkyrimFairNPC` |

Left alone: Functional Fearsome Fists (a plain stat effect, no script, no cloak). Maximum Destruction and
Strange Runes are not installed.

Method: in place, per the author's tool, with a `.skyrimfair-backup` beside each file; a local copy of the
patcher with the extended target list goes to `_tools\skyrimfair-spid\` and its `--dry-run` is the
`--check`. Register all seven in the patched-third-party-files register. Verify after first launch from
`po3_SpellPerkItemDistributor.log` (the fair NPCs must not appear under those spells).

### 5b. `houseCARL - Authoria - Patch - Holidays and Fair - Requiem.esp` (light, override-only)

- **4 Holidays skeleton bases** (`_WetHolidayEncSkeleton01Melee1H / Melee1Hshield / Melee2H / Missile`,
  level 1, SkeletonRace, no template): give them Requiem's comparable as template with Stats + SpellList +
  AttackData flags (`EncSkeleton01Melee1H 02D1DE`, `...Melee1Hshield 02D1FD`, `...Melee2H 02D1E0`,
  `...Missile 02D1FC`). Requiem's skeletons are level 1 too but carry HealthOffset 150, DoesNotBleed and the
  Requiem spell kit; the Holidays ones have offset 0. Own traits, outfit (hooded skeleton), factions,
  packages and the spooky script stay. The Reqtificator then stamps perks as for any skeleton.
- **12 Holidays clothing pieces with a stray armor rating** (3 Tales and Tallows hoods AR 2, Witches masks
  AR 4–6, 4 Jester hats AR 9): set AR 0. They carry ArmorClothing + ClothingHead etc. already; values are
  in Requiem's clothing range.
- **3 Update.esm tundra shrubs at the fair gate** (`000F91`, `000F92`, `000F97:Update.esm`, 33–204 units
  from the gate furniture): disable. The fair only masters Skyrim.esm, so it never touched them.

Nothing else in either plugin needs a record edit (section 6).

### 5c. Small file work

- Delete `Authoria - PG Output - PBR\meshes\architecture\solitude\clutter\sropefestivalring.nif` (the
  ParallaxGen copy that would shadow the animated ring; only the PBR output has it).
- Add `SkyrimFairWorld` to `Only-pregenerate-world-spaces` in
  `Authoria - MCM and INI Settings\SKSE\Plugins\GrassControl.ini`, so the next grass-cache build includes the
  fair (see section 8).
- Extract `JKs Palace of the Kings - Holidays Patch.esp` from the 5.29.1 rar into its own folder.
- Build the Descriptions addon folder with just `Holidays_DESC.ini`.
- Copy every archive to `D:\1. MOD STUFF\1. SKYRIM FILES\gameplay and quests\` (fair, Holidays and fixes)
  and `...\animation\` (HSF, Professional Dancer).

---

## 6. Requiem disposition (every enumerated record has one)

Freshness: houseCARL on `C:\1. AUTHORIA`, profile PBR, Iron Sword chain includes Requiem.esp and
Requiem for the Indifferent.esp (live winner). Plugins enumerated with a full record walk of the archives
(the mods are not installed yet, so `cross_plugin_query` runs again after install as the reconciliation).

### Holidays.esp — 4,256 own + 219 overrides

| Type | Count | Lane | Disposition |
|---|---|---|---|
| NPC_ | 9 | npc | 4 skeleton bases → patch (5b). Goat, Eorlkar (guard-templated), witches + atronach (vanilla LVLN-templated, already Requiemised) → no edit. |
| ARMO | 24 | armor | clothing frames, correct keywords; 12 AR fixes (5b). |
| BOOK 44, MISC 10, OTFT 2, KYWD 1, GLOB 7, FLST 9 | | economy / plumbing | flyers value 0, Carol books 50, Festivals 55, lucky coin 25, mortar packets 5 → leave. |
| LVLI 18, LVLN 3 | | leveled-list | gift lists hold vanilla items (the birthday list uses LItemEnch*Special: level-matched vanilla enchanted gear, items themselves Requiem-overridden). Mod-internal lists, never merged, leave. |
| SPEL 37, MGEF 42 | | magic | 29 script-carrier abilities (holiday controllers, gear equip, free inn, discounts); 8 firework projectiles (cost 14, fire-keyworded, fired by mortar packets, no tome, never player-learnable) → leave. |
| PERK 2 | | perk / economy | Merchant's Festival / Warriors Festival discount days → leave. |
| QUST 32, PACK 61, SCEN 1, DIAL 4, INFO 23, MESG 33, LSCR 12, ACTI 28, STAT 61, MSTT 12, TXST 49, ARMA 62, LIGH 9, PROJ 9, EXPL 9, SOUN 18, SNDR 18, IMAD 2, SPGD 1, VTYP 1, DLBR 3, CELL 1 (marker storage), NAVM 1, REFR 3498, ACHR 99 | | cosmetic / plumbing | no Requiem meaning. |
| WTHR 1 | | visuals | `_WetHolidayOvercastSnow`, forced during Saturalia; a 2017 vanilla-style weather under the CS stack. Later polish: point it at an Astralite snow weather. |
| Overrides: CELL 136, REFR 76, WRLD 6, NAVI 1 | | placement | handled by the early slot (section 4). NAVI: standard last-wins, harmless. |

### SkyrimFair.esp — 4,551 own + 44 overrides

| Type | Count | Lane | Disposition |
|---|---|---|---|
| NPC_ | 120 | npc | 115 civilians level 5 fixed, class Citizen, protected, no combat style, no own perks/spells; faces from two LVLN lists of vanilla NPCs (Traits only) so the list's replacers apply; 12 children Traits-templated on vanilla kids (RS Children applies); 2 archers level 10 with a Requiem hunting bow + 100 iron arrows; 5 uniques with shipped facegen (3 singers, Garrick, Claudius); chicken/goat/dog/horse on vanilla races. All standard inputs → **no edit**; the Reqtificator stamps racial traits and global perks. |
| FACT 33 (vendor), CONT 33, FLST 35 | | economy | Per-stall vendor factions + merchant chests with vanilla goods (food, drink, ingredients, clothing, clutter, and singles of Dwarven/Elven/Imperial gear, glass/ebony at the Rare stall) and 100–250 gold. Vanilla items are Requiem-valued already; "Fair Prices" perk makes the gear stalls 20× → treat, not shortcut. Chests get the Requiem lockpick script at the next build. → leave. |
| PERK 2 | | perk | Fair Prices (buy-price entry point), Fair Talk (cameo script) → runtime plumbing, leave. |
| SPEL 3, MGEF 3 | | magic | firework FX (cost 0, aimed, MG01FireEffectScript visual) → leave. |
| DOOR 2, ACTI 55, QUST 4 (+ .seq shipped), DIAL 51, INFO 77, GLOB 18, KYWD 3, LVLN 2, SNCT 2, SOPM 4, SOUN 19, SNDR 19, VTYP 5, PACK 17, STAT 215, TXST 23, LTEX 5, GRAS 3, CLMT 1, WRLD 1, CELL 123, LAND 121, NAVM 9, REFR 3290, ACHR 247 | | plumbing / worldspace | no Requiem meaning. |
| Overrides: CELL 4 + persistent cell, REFR 37 (shrub/rock disables), WRLD Tamriel, NAVI | | placement | section 4 and 5b. |

### Dance.esp (43), bunting patch (15), JK PotK Holidays patch (63)

Two lesser powers (cost 0), one ability, three scripted effects, three quests, 23 globals, MCM; tips of 1–2
gold. Statics / texture sets. Placed refs + one cell. No Requiem meaning.

### Gap mechanics touched

Economy (vendors, discount days): record-driven, within Requiem's ranges, nothing to change. Food/drink at
the stalls: vanilla items, Food and Beverages Redone already wins them. No vampirism, disease, shout, stone
or perk-tree content. No `REQ_NULL_*` anywhere (the patch copies no perk/spell lists).

Balance for the 120 fair NPCs, 33 chests and 2 doors, and the 9 Holidays actors, arrives with the next
Reqtificator build; until then they are un-Requiemised civilians and props, which is harmless.

---

## 7. Placement findings

### The fair's site (west of Whiterun, cells (-2,-4), (-2,-3), (-3,-4), (-3,-3))

362 new placed objects in Tamriel (gate at x −7050 / y −10800, palisade x −9246…−5043 / y −15786…−10785,
fireworks sites at y ≈ −16240). Measured against every plugin that places objects in those four cells:

- Northern Roads (15 live refs, plus its patches), Lux Via (23), Fort Greymoor (12), Imperial Castles (6),
  Nature of the Wild Lands (6), Vigilant + Gore (3): **nothing within 600 units** of a fair object. Clean.
- Update.esm: three tundra shrubs 33/165/204 units from the gate furniture → patch (5b).
- USSEP-moved shrubs: the fair's own disables win. Fine.
- Staff of Hasedoki Creation: its dead-bandit scene sits ~500 units east of the gate, outside the wall. No
  overlap; you will see it from the entrance.

### Holidays decorations vs the city overhauls (cells where both place objects)

| Settlement | Holidays cells | Overhauls that also place objects there |
|---|---|---|
| Whiterun | 7 | Whiterun Has Walls (7), GreenThumb Whiterun (7), Witcherun (6), City Trees Whiterun (6), The Gildergreen Grows (4), Whiterun Market Archway (3), Circle Trellis REMOVED (patch exists) |
| Solitude | 10 | Grand Solitude (9), City Trees Solitude (8), Blue Palace Terrace (4), Val Serano (3), Snazzy Grand Solitude (3) |
| Windhelm | 11 | Spaghetti's Windhelm (10) + Clutter Addons (7), Simply Snowy Windhelm (9), Little Touches (8), City Trees Windhelm (8), Windhelm Well (2), ALT Walls Tower (3) |
| Riften | 8 | Riften Expansion (8), City Trees Riften (6), Ivy Riften Docks (3), Icy Waterways (3) |
| Markarth | 5 | Markarth Side (5), City of Stone (5), Mossy AF (4), Ancient City of Markarth (4) |
| Villages (Tamriel) | 62 | Northern Roads (32), Nature of the Wild Lands (25), Aspens Ablaze (12), COTN Dawnstar (8) + Falkreath (7), City Trees Dawnstar/Falkreath (7 each), Threads of the North (9), CFTO (9) |
| Interiors (inns, temples) | 33 | EEKs Whiterun Interiors (8), COTN Falkreath (6), JK's Candlehearth Hall (5), Snazzy Dawnstar (4), Val Serano (12) |

AI Overhaul, Laundry, Sounds of Towns, Mists of Tamriel, Missives, 3DNPC, Immersive Encounters and LotD
also appear but place markers/NPCs, not geometry.

Lantern ropes are strung building-to-building and tree-to-post from vanilla positions, so the tree
replacers (City Trees, Nature of the Wild Lands) and the wall/market rebuilds are the likely offenders.
Phase 2 = force the decorations on (MCM toggle or the `_WetHolidayIsHolidayDecorations` global), walk each
settlement with screenshots, then I build `Authoria - Patch - Holidays - <settlement>` move/disable patches
with houseCARL. The JK Palace of the Kings patch and the Trellis patch are the two ready-made ones.

---

## 8. Consequences that only the generators resolve (stated, not scheduled)

- **Grass at the fair.** `GrassControl.ini` runs `Use-grass-cache = true` and `Only-load-from-cache = true`;
  the fair's worldspace has no cache, so its ground is bare until the cache is next rebuilt. I add the
  worldspace to the pregenerate list now so that rebuild picks it up.
- **Distant view.** The palisade and light towers have no LOD; they appear at loaded-cell range. The
  current DynDOLOD output predates the fair.
- **Professional Dancer** stays inert until the behaviour cache is rebuilt with it; the fair's crowd uses
  vanilla dances meanwhile.
- **Requiem balance** for the new NPCs and chests arrives with the next Reqtificator build.
- **Weather at the fair.** Its own climate cycles four vanilla weather records (clear, cloudy, two tundra);
  Astralite's overrides of those apply, the seasonal region weather does not. In-game look.
- **Voices.** The three singers carry 147 recorded song lines; the two cameo travellers 28 lines as
  xwm+lip; the 33 keepers use vanilla barter lines for whatever voice their random face brought. Nothing to
  fix, just what to expect.

---

## 9. Verification I run after the install (none of it yours)

1. Unscoped `housecarl_check` errors family: `0 missing master(s)`.
2. `cross_plugin_query` on both plugins + the patch: counts match section 6; every patch FormID resolves.
3. `facegen` family on SkyrimFair.esp: the five uniques resolve mesh + tint + record to the fair's files.
4. Full-plugin census per profile (MO2 closed): 242 / 242 / 243 / 232 / 199 / 208.
5. Plugin-group header check: 0 duplicated headers, 0 ungrouped, all six profiles.
6. `housecarl_skse config` on Light Placer: the two Holidays jsons' model names resolve.
7. Asset winners: SBB rope mesh, animated ring, Holidays lantern mesh, fixed inn script (loose beats BSA).
8. After your first launch: SPID log (fair NPCs absent from the seven spells), Papyrus log (menu count,
   no `_Holiday`/`SkyrimFair` errors), the Holidays MCM present.

---

## 10. Sequence

1. Copy archives to D:, then install the twelve mod folders (section 2) and place them in all six
   profiles (section 4), plugins inserted with `plugingroups.txt` updated.
2. SPID edits (5a) — after your yes.
3. Build the Authoria patch (5b), verify (9.1–9.3), place it.
4. File work (5c).
5. Your launch: gate + fair walk-through, then a decorated holiday in one city for the clipping audit.
6. Phase 2 patches per settlement from the screenshots.
