# skywim batch - install plan (2026-10-12)

Source: the 68 files in `C:\Users\User\Downloads\skywim`. Catalogue (per archive: contents, plugins, masters, body lane,
Requiem needs): session scratchpad `s11_catalog\CATALOG.md` + `catalog.json`. This plan is the readable version.

Standing rules for the whole batch:
- Nothing is installed until the stability test of Bottled 1.0.11 has passed (user: "test performance and stability before
  any further additions").
- Every change is made identically in `DEEZ CS NUTZ - PICTA` and `Authoria - Preset Studio - HPH`; other profiles get the
  mod lines disabled.
- MO2 and the game closed before any write; backups before every write; the four profile files (modlist, plugins,
  loadorder, plugingroups) change in lockstep; the batch load-order write is shown to the user before it runs.
- Plugin census (full vs ESL) is taken with MO2 closed before phase 2: this batch adds 3 full plugins (Dynamic Follower
  Banter, NPC Situational Reactions, Ophelia) against the 254 cap.

Correction to the catalogue: CBBE 3BA IS installed and enabled here (it is the vanilla-race outfit lane); UBE actors use
the converted `!UBE` lane. So 3BA BodySlide sets are useful for the vanilla-race lane; UBE needs the converter run.

## 0. Your picks (decide these; everything else is routine)

| # | Question | Recommended | The other way |
|---|---|---|---|
| P1 | Eli's Coffee: which build? | **Survival build** + SunHelm patch + stress keywords + ElSopa remodel + alt textures (SunHelm and CC Survival are installed) | No-Survival build + eating-animation patch |
| P2 | Ophelia wreaths: which plugin? | **Original 1.3 + UBE patch** (the UBE patch and the outfit distribution only work with the original) | "Ophelia Fixes" rebuild (breaks both; would need re-targeting) |
| P3 | Spell Hotbar NG 1.9.1 replaces the old Spell Hotbar? | **Yes** (old Spell Hotbar + its Veldun Fit patch + White option go off; NG is pure SKSE + OAR, no plugin) | Keep the old one, skip NG |
| P4 | MCM Bridge (lifts the 128-MCM cap, fast MCM loading) | **Defer to its own test** - it replaces the same SkyUI scripts as MCM Recorder and the Authoria MCM Recorder fix | Install now and lose MCM Recorder |
| P4 update 2026-10-14 | User's call: MCM Bridge goes IN. Needs 1.2.0 + its MCMRecorder Patch (beta), FLICK 1.6.0 as frontend; Authoria MCM Recorder Fix retired; init sequence rebuilt without the MCM rebuild step. Full write-up: `HORSE-SC-PLAN.md` section 6. | | |
| P5 | Snow: Simplicity of Snow + XPMF (replaces Better Dynamic Snow) | **Defer** - this is a visuals change and the visuals stack is locked | Install now |
| P6 | Dynamic Terrain Deformation 1.2 (installed 1.0 is disabled since the late-September fps work) | **Update the folder, keep it disabled** until a visuals A/B | Enable with the update |
| P7 | Cloaks of Skyrim group (physics, 4K retexture, mesh update, Campfire cloaks) | **Skip** - the base mod Cloaks of Skyrim is not installed and not in the folder; the list uses Cloaks and Capes | Download Cloaks of Skyrim and add the whole group later |
| P8 | Dwemer Research Squad (5 female outfit sets) | **Include** with a UBE conversion run (shipped bodies are BHUNP; the 3BA set serves the vanilla-race lane) | Skip |
| P9 | Kaidan AIO (reduced) | **Defer** - overlaps the installed Immersive Kaidan AIO and ships a different copy of a plugin already installed; needs a record-by-record compare | Install the jewelry + weapons parts only |
| P10 | Movement: FreeClimb (+ alt sounds), FluidMotion | **FreeClimb yes; FluidMotion defer** (0.1.1 experimental, overlaps SkyParkour/Better Jumping/Horse Behaviour) | Both now |
| P11 | Female bleedout: Zodd's on-back vs installed Crawling Bleedout | **Keep Crawling Bleedout, skip Zodd's** (same animation slot; one wins) | Zodd's for women |
| P12 | HSF Child Expression Overhaul | **Skip** - it replaces the same child head files as the installed high-poly Younglings | Install over Younglings |
| P13 | Dynamic Khajiit Fur Shaders | **Defer** (no UBE female option; Fluffy Khajiit 3 mesh fur is installed; visuals) | Install for males/vanilla-race Khajiit now |
| P14 | LDD RFAOS skin maps (Advanced Skin) | **Defer** (vanilla female texture path, so UBE women would not use it; visuals) | Install now |
| P15 | NPC Situational Reactions + the combined Voice Pack 1 | **Yes**, with the Address Library v13 download first (I fetch it with your OK) | Skip (saves 2 plugin slots and 2 GB) |

## 1. Group A - install, no Requiem patching, no body work

| Mod | What it adds | Needs | Notes |
|---|---|---|---|
| Cinematic Conversation Camera 1.5.0 + Cinematic preset pack | Cinematic dialogue camera (cuts, angles), two presets | SKSE Menu Framework (have) | Turn OFF "Switch Camera During Dialogue" (installed, enabled). Keep SmoothCam. |
| Dynamic NPC Thinking Animations | Two OAR idle variants | OAR (have) | - |
| Animated Poisons Redone 1.3 | Poison-apply animation, SKSE | OAR, Pandora | The ONLY item needing a Pandora run (Nemesis-format patch). |
| Dynamic Underwater Fish | CC fish spawn around you underwater | CC Fishing (have) | Turn its spawn logging off; fish cap 100 is a performance knob. |
| Fight With Me 0.1.0 | Follower combat roles and orders | SKSE Menu Framework | Pairs with Walk With Me 0.3.0. |
| FreeClimb 0.5.0 + alt sounds | Climbing, wall run, mantle | ImGui Icons (have) | Jump-key overlap with SkyParkour and Better Jumping - settle in its menu. |
| Ride Along 1.2.1 (added to the folder 2026-10-12; use it, not 1.1.0) | Follower rides pillion | - | 1.2.1 adds a small plugin (RideAlong.esp) and a "princess seat" option; the 1.1.0 archive is superseded. |
| Selective Looting 1.1.0 | "Take all" leaves chosen item types | - | Test with QuickLoot. |
| Inventory Interface Information Injector Improved | I4 icon cache, favorites CTD fix | I4 (have) | Loads beside I4; the installed Alchemy Fix becomes redundant. |
| Dear Dragonborn | Follow-up letters after quests | - | Courier based. ESL. |
| Dynamic Follower Banter 1.1 | Banter between voiced followers | SPID (have) | FULL plugin (slot). 18,773 voice lines. |
| Scarecrows of Skyrim (BOS) | Scarecrows at crop fields | Base Object Swapper (have) | Placement check against farm overhauls before enabling; no LOD regen needed. |
| XPMF 0.7.1 | Projected-material framework | - | Only needed if P5 goes ahead; install together with Simplicity of Snow, not alone (its default snow profile alone changes snow). |
| Spell Hotbar NG 1.9.1 | Spell/shout/item hotbar, OAR casting | OAR, SKSE Menu Framework | FOMOD: core + Apocalypse + Triumvirate icon packs. Replaces the old Spell Hotbar trio (P3). The "1.6" copy is older (1.4.0) - delete. |
| NPC Situational Reactions 12.0 + "Voice Pack 1" (added 2026-10-12: the combined MAIN file, 10 of 42 voice types in one 1.9 GB archive with one loader plugin; it replaces the six separate per-voice packs, which are skipped) | 300+ NPC reactions, Living World idles | Address Library v13 (have v11) | P15. 2 plugins (1 full + 1 empty ESL loader). Archive root is a sub-folder. |

## 2. Updates

| Mod | From -> to | What to carry over |
|---|---|---|
| FLICK NG | 1.2.0 -> 1.5.0 | Settings ini (scale 0.85, toggle key) - re-apply after the update. Drop the stray pdb. |
| Walk With Me | 0.2.5 -> 0.3.0 | The Wayfarer script-rename patch for Biggie Traits stays required (0.3.0 still ships Wayfarer.pex). Command Gestures 0.3.0 is NOT in the folder - fetch or keep 0.2.2 and test. |
| The Wanderer's Fair (SkyrimFair) | 2.0.1.2 -> 2.0.1.3 | Re-diff the three Authoria hand patches (Holidays and Fair Requiem, No Reseat, Picta Climate) against the new plugin before enabling. Fair worldspaces: check whether DynDOLOD output covers them. |
| Dynamic Terrain Deformation | 1.0 -> 1.2 | P6: folder updated, stays disabled. Surface profiles match landscape texture file names - PBR packs may need their own. |
| Sunhelm Follower Needs | - | Hans Edit in the folder is byte-identical to the installed one: nothing to do. The stock 1.6.0 zip would overwrite Hans' DLL - do not install. |
| FLICK "(1)" copy | - | Duplicate download, ignore. |

## 3. Group B - content that needs Requiem patching and body-lane work

Patching is done with the requiem-patching skill after the plugins are placed; one Authoria patch per set, extend never
replace. Body work: vanilla-race lane = BodySlide (user) with the 3BA sets; UBE lane = converter run (mine) + validation
(zero-filled mesh check) + minted ARMAs + SkyPatcher lines.

| Set | Pieces (install order) | Requiem patching | Body lane |
|---|---|---|---|
| Clothes of the Northern Folk | assets (12) -> ESL plugin + SkyPatcher list insert (11) -> Immersive Distribution (05) -> Grand Solitude add-on (37) | 387 clothing records (value, weight, keywords); the SkyPatcher leveled-list insert bypasses the Reqtificator merge - decide keep or move into the patch | Vanilla-shape fits, no BodySlide; eyeball on UBE, convert if needed |
| Pelts 'o' Plenty | Fur Pelt Gear (53) -> hotfix esp (35); Resources (54) redundant - skip | 120 cloak records + 110 recipes (the existing "fur pelts" Requiem patch targets a different mod - verify, do not reuse blindly) | Vanilla-body cloaks worn over the body; 3BA BodySlide set for the vanilla lane; UBE: test clipping first, convert only if it shows |
| Ophelia (P2) | Original 1.3 (50) -> UBE patch (52) | 22 enchanted circlets + 22 recipes; the UBE patch must stay the last word on model fields | UBE patch = the UBE lane, done |
| Dwemer Research Squad (P8) | 4K main (13) -> GND meshes fix (32); 3BA set (15) for the vanilla lane | 22 armours + 32 recipes + leveled list + keywords | BHUNP shipped meshes; 3BA BodySlide for vanilla lane; converter run for UBE |
| Eli's Coffee (P1) | Survival build (25) -> SunHelm patch (24) -> SkyPatcher keywords (26) -> ElSopa remodel (22) -> alt textures (23) | 4 drinks + 1 ingredient + 3 recipes; 2 vanilla leveled-list overrides go through the Reqtificator merge; the SunHelm patch and the Requiem patch must be merged (same records) | - |
| IHarvestNG | 1.0.7 in folder; Nexus has 1.0.8 - fetch with your OK | 2 spells, 3 effects, staff, tome, recipe (magic patching) | - |

## 4. Skipped or deferred (with the reason)

- Cloaks of Skyrim group (P7): base mod absent.
- Simplicity of Snow + XPMF (P5), Dynamic Khajiit Fur Shaders (P13), LDD RFAOS (P14), DTD enable (P6): visuals changes - after the stability pass and as their own A/B.
- Kaidan AIO reduced (P9): overlaps installed Kaidan content; needs a compare first.
- MCM Bridge (P4): script collision with MCM Recorder; own test.
- FluidMotion (P10): experimental; overlaps installed movement mods.
- Zodd's bleedout (P11), HSF Child Expressions (P12): direct asset conflicts with installed mods.
- Spell Hotbar NG "1.6" copy, FLICK duplicate, Pelts Resources, Sunhelm stock 1.6.0: superseded or redundant.
- HKX Conversion Tool exe: a tool, not a mod; not run. houseCARL 2.0.4: tooling update, separate.

## 5. Order of work

Phase 0 (user): play the 1.0.11 build; I read the logs. No installs before this passes.

Phase 1 (me, after your picks): Group A + Updates. Mod folders built from the archives (FOMOD picks recorded in each
mod's notes), placed in the modlists, plugins/loadorder/plugingroups in lockstep, Switch Camera During Dialogue and the
old Spell Hotbar trio disabled. Address Library v13 and the newer Ride Along / IHarvestNG files fetched only with your OK.

Phase 2 (me): Group B placement, then the Requiem patches via the requiem-patching skill, then the UBE converter run
with the zero-filled-mesh validation.

Phase 3 (user, in this order; I prepare and verify each):
1. BodySlide: build the 3BA sets for Pelts and Dwemer Research Squad with your usual preset (vanilla-race lane).
2. Pandora: regenerate behaviours (Animated Poisons Redone).
3. Synthesis: re-run the list's pipeline (new plugins with leveled lists and outfits).
4. Reqtificator: always after plugin changes in Requiem (after Synthesis, before DynDOLOD).
5. DynDOLOD: only if the Wanderer's Fair update changes its worldspace statics (I check first); otherwise skip.

Phase 4 (user, in game): Cinematic camera preset choice, Fight With Me keys, Selective Looting rules, NSR MCM, FreeClimb
jump-key settings. I read the logs after the first session.

## 6. Open items that can change the plan

- Friend's repository (part 3): his adds may join Phase 1 or 2 once chosen.
- Plugin census with MO2 closed (full-plugin headroom for the 3 new full plugins).
- Walk With Me Command Gestures 0.3.0 file (not in the folder).

## Proposed additions 2026-10-12 (evening) - for the same full tool run (PG Patcher + TexGen/DynDOLOD)

User asks (10-12 evening): a carriage "replacer"; the Whiterun main gate "should be metallic and reflective".
Findings: the carriage's odd panels are farmhouse WoodWall01 and Riften canal planks with no PBR source (interim fix:
`Authoria - Carriage PBR Wood Fix`); the Whiterun main gate door is GDOS's plain env-mapped mesh (`textures\architecture\hype\`),
no PBR version installed. Picks (not yet chosen):
- P16 CHOSEN 2026-10-12 evening: Glorious Doors of Skyrim (GDOS) SE PBR - Nexus 150727 (v3.5.1, 2026-05-26) - PBR conversion of the installed GDOS; needs the PG rerun.
- P17 CHOSEN 2026-10-12 evening ("PBR version is fine for riften"): Tomato's Riften PBR - 2k v1.2 (Nexus 157340, 2026-06-23) REPLACES the installed Complex Parallax 2K v1.0 (same artwork, PBR flavour). Manager-only download. Install in the tool-run batch (PG + TexGen rerun).
- P18 DECLINED for farmhouses (walls are BH's Rustic + Riton; any PBR pack changes the look). The carriage wall panel stays on the mesh fix (Markarth PBR wood); optional later: carriage-only wall texture from a PBR pack. Was: Vanaheimr - Farmhouses - II - PBR (Nexus 158524 v3.0) OR
  TomatoRim - Farmhouses PBR and CM (Nexus 135774).
After P17/P18 + PG rerun: delete `Authoria - Carriage PBR Wood Fix`. TexGen/DynDOLOD rerun for the farmhouse/Riften LOD textures.

Fetch status 2026-10-12 evening ("fetch"): `Downloads\skywim\_fetched\Medieval Towers Roof swap\Medieval Towers - Roof texture swap-175989-1-0-1774827505.7z`
(175,181 bytes, OK). Tomato's Riften PBR - 2k v1.2 (file 767020) could NOT be fetched by the Nexus session tool: the v1.1/v1.2 uploads use
Nexus's new file storage (uuid URIs, no size) and the download endpoint returns no CDN link; v1.0 (file 658020, 292 MB, old storage)
would fetch but lacks the v1.1 FOMOD (edge fixer default, new wood/roof options). Plan: the user clicks "Mod Manager Download" on
https://www.nexusmods.com/skyrimspecialedition/mods/157340?tab=files&file_id=767020 with MO2 open at batch time.
