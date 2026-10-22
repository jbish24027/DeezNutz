# Batch install 2026-09-24 - Bottled Shaders, DSFG experimental, grass distance, terrain deformation, and ten smaller mods

Session ledger. Everything below was done with MO2 and the game closed. Pre-state backup of all six
profiles' four files plus the key settings files: `_backups\2026-09-24 - Batch install pre-state\`.
Per-file backups beside every profile file: `*.bak-batch-20260924`. Nothing was launched.

## 1. Renderer: Bottled Shaders 1.0.0 replaces the Community Shaders AIO dev build

- New mod `[NoDelete] Bottled Shaders` (Nexus 192816 file 809627). Enabled in the three CS profiles at
  the AIO's slot (directly above it); `[NoDelete] Community Shaders AIO` (2026-08-24 Discord build of the
  same fork) is now DISABLED and kept whole as the rollback (flip the two lines back). The three non-CS
  profiles carry the new line disabled at the top (they never had the CS block).
- Bottled is a full CS replacement (author: "don't have both installed"). It bundles Effects 11, Snow
  Cover, Grass Optimizations, Reverse Z, Footstep Particles, Post Processing, Linear Lighting.
- Local edits forwarded (ledger inside the mod: `LOCAL-SHADER-EDITS.md`): valley-clamped Snow Cover
  altitude map (straight copy, upstream unchanged); the volumetric-ray negative clamp re-applied on its
  moved line 81; the six worldspace configs re-pinned (snow line 9999999 = snowfall-only, grass and tree
  tint OFF, the shipped `default/main` snow textures). The AIO's Sky.hlsl was stock, nothing to carry.
- `Shaders\Upscaling` + `Features\Upscaling.ini` parked in `_backups\2026-09-24 - Bottled Shaders
  Upscaling parked\` (DynamicShaderFrameGen owns the swap chain). JSON lock `Disable at Boot ->
  Upscaling: true` kept.
- overwrite: `SettingsDefault.json` -> `.stale-aio0824-20260924`; `ShaderCache` ->
  `ShaderCache.stale-aio0824-20260924` (first launch = full recompile, ~12 min last time).
- `SettingsUser.json` (backup `.bak-pre-bottled-20260924`) edited only inside verified-identical blocks:
  - `Disable at Boot` += `ScreenSpaceGI` (its schema moved in Bottled; the saved off-block would be
    rejected and SSGI would run ON = the recorded exterior colour cast) and `ReverseZ` (first launch
    without it; DSFG's depth copy is from a non-reverse-Z branch); `ProceduralGrass` key dropped.
  - `Grass Optimizations`: MinDensity 1.0, EdgeFadeStart 0.85, InvisibleFadeCull 0.05, MeshCostBias 0,
    SimpleShadingPixelSize 4, RenderDistanceOverride 100000.
- Blocks whose key set moved run at compiled defaults on the FIRST launch (Light Limit Fix - contact
  shadows were off; Grass Lighting; Volumetric Lighting; Wetness Effects; Sky Sync). New features with no
  block run at defaults (Foliage Lighting, Footstep Particles, Procedural Sun). After the first launch +
  quit, the regenerated file gets its values re-pinned - Claude's job, not the user's.
- No fire melt exists in this build (zero fire-melt strings in DLL and shader; removed upstream before
  08-24). The `frac(hue*2)` foliage branch is still in the shader but never runs with both tints off.
- Fallback set refreshed, all DISABLED everywhere: `[NoDelete] Community Shaders` 1.8.3 -> 1.9.1
  (file 810029), `[NoDelete] Effects 11` 179824 -> 192760 1.0.0 (file 809741), new `[NoDelete] Grass
  Optimizations` 188628 1.0.0 (file 809750). Old folders in the pre-state backup. Never enable the
  standalone Effects 11 or Grass Optimizations over Bottled: the standalone E11 shaders are OLDER than
  Bottled's (no sky-scattering path) and GO lacks the Reverse-Z branches.

## 2. DynamicShaderFrameGen: updated in place to the Experimental branch (file 809721)

- Only three payload files differ from v1.0: plugin DLL 0.48 -> 0.57 (parked as
  `DynamicShaderFrameGen.dll.v0.48-20260911`, one-file rollback), the depth-guide shader (scale-aware),
  and the ini. Every Streamline/FidelityFX DLL is byte-identical. The archive's `nvngx_dlssnr.dll` is the
  same patched HashMismatch copy as v1.0 - the genuine signed copy (md5 5b944399...) was KEPT.
- Ini rewritten as a full 35-key file (the shipped one is the author's 4x DLSS-G test bench, kept as
  `.shipped-exp-20260922`): Provider 0 (FSR3 2x), FrameGeneration 1, QualityMode 0 +
  RenderResolutionScale 1.00 (native), DLSSGFramesToGenerate 1, MFGMaxFramesOverride 0, PixelProbe 0,
  ForceBackBufferCopy 1 (author's readme: 0 freezes the picture), NeuralRenderingEnabled 1,
  NRAllowWithFrameGen 1 (without it NR is SUPPRESSED while FG runs), NR intensity 2.0 / style 2 / auto
  mask / UI correction / render scale 1.00 (the accepted PureDark NR look), InteropFenceWait 1,
  FenceWaitBusy 0, FpsOverlay 1, ToggleKey 0xC7 (Home).
- Known from the author: this branch has a 4K camera-turn edge blur he has not fixed ("2K usable").
  Judge in play; rollback is the parked DLL.
- `DynamicShaderFrameGen - MFG Game Root File` staged DISABLED in all profiles: it is DLSSG-Transfusion
  1.4.1 (an RTX 40 kernel unlocker) as `Root/dinput8.dll` + a json forcing 6x. It would replace the
  game root's existing dinput8.dll proxy (xSHADOWMANx DLL Loader - mutually exclusive), is dead weight
  on FSR3, and 6x smears at 4K. Do not enable.
- The author's optional SSE Display Tweaks ini (file 804392) NOT applied: it is his 2K/165 Hz test
  config (VSync on, tearing off, MaxFrameLatency 1, 300 caps) with no rationale; the tuned copy keeps
  VSync off / tearing on. A/B recipe if wanted: change only EnableVSync/EnableTearing/MaxFrameLatency.
- Backups: `_backups\2026-09-24 - DSFG exp update\`.

## 3. Grass: dense and seasonal as far as the eye can see

- `GrassControl.ini` (Authoria - MCM and INI Settings; backup `.bak-grassopt-20260924`):
  Overwrite-grass-distance 28000 -> 100000, Overwrite-grass-fade-range 14000 -> 0. Extend on, cache
  only, DynDOLOD grass mode 0 unchanged. NGIO grid goes 11 -> 25 cells (529 -> 2601 resident cells,
  ~4.9x the cull work; ~555 MB of cache data streamed around Whiterun in spring/summer vs ~128 MB).
  Expect `ChosenGrassSettings: grid: 25, dist: 100000, range: 0` in NGIO-NG.log.
- CS Grass Optimizations block set as in section 1 (thinning off, fade only over the last 15%).
- Seasonality needs nothing new: the five per-season caches already cover radius 25.
- Fallback if fps suffers: 60000 / 0 (grid 15) and MinDensity 0.5. If grass ends in a hard wall, set
  the fade range back to 14000 and let EdgeFadeStart 0.85 do the visible fade.

## 4. Dynamic Terrain Deformation SKSE (Nexus 192402) replaces the DynamicSnow trial

- New mod enabled in PBR and DEEZ CS NUTZ (where the trial was), disabled elsewhere. The trial trio
  `DynamicShader-DynamicSnow`, `DynamicShader Core`, `Authoria - Smooth Terrain - Snow Trial Profile`
  flipped OFF in those two profiles (folders kept). Smooth Terrain therefore returns to the tuned
  2 / 20 / 3 / 2 settings. Never run both deformation systems.
- Standalone SKSE, no swap-chain hook, no plugin, save-safe. Ini live-reloads on save. Perf lever:
  `TessellationTargetSpacing` 2.0 -> 4.0 halves its cost.
- Added `SKSE\plugins\NMN_DeformableTerrain\Authoria - Seasons and Landscapes\Surfaces.ini`: the DLL
  matches landscape textures by exact file name, and 489 of this list's 561 land textures (Bruma,
  Elsweyr, Witchy Wilderness, Seasonal Landscapes, Vigilant, Northern Roads winter roads...) were not in
  its shipped lists. The file assigns them by class (snow / dirt / mud / grass / sand / ash / rock
  blacklist) with the author's own values. Optional block left commented: treat `grasssnow01` (the
  Seasons winter ground on most of Skyrim) as deep snow instead of thin grass - the author's default is
  thin.

## 5. Ten smaller mods

| Mod | Placement | Notes |
|---|---|---|
| Animated Bound Weapons 1.3.1 (192288) | above Bound Weapon Fix; `AnimatedBoundWeapons.esp` (light) after Requiem - Survival Spells.esp, group Gameplay - Late Loaders | Page asks for SKSE Menu Framework 3.17+; the DLL resolves 32 framework exports and all 32 exist in the installed 3.8, so no framework update. Conjuration Limit Fix not installed (weapons use the normal summon limit). Adds four helper NPC records (an NPC input for the Requiem process). |
| Dynamic Bloodpool for Dismembering Framework (192574) | above Dynamic Bloodpool Framework; both light ESPs after DF - Xtudo Creature Pack - Wolves of Skyrim.esp, group Gameplay - Early Loaders | Both DF asset packs are active in every profile, so both options installed. 768 severed-limb records gain the bloodpool script; no other plugin touches them. |
| Use Special Markers 1.0 (32748) | above Modern Female Sitting Animations Overhaul; `Use Special Markers.esp` (already light) after Unique Jarl Throne Sitting Animation.esp, group -- Animations -- | 34 furniture-marker overrides, all uncontested. Its Breezehome CELL override loads ~1300 slots before Lux, so Lux lighting wins. Four of its marker meshes lose to loose files (Kaidan AIO, Skyrim 3D Furniture, PG output) - the find-spell route still works. |
| HSF Female Cross Legged Animations (192210) | above Modern Female Sitting Animations Overhaul | OAR-only; priority 998888222+ beats Take a Seat / Male Furniture Pack for females. |
| Oblivion Interaction Icons - Patch Collection 1.1.1.0 (191709) | above Oblivion Interaction Icons | 30 of 103 options match (all active in every profile), 183 new prompts; zero collisions with the installed icon set (Vel'dun UI's tinted copies still win the originals; the new prompts are untinted). |
| QuickLoot Redesigned 1.1 (192433) | enabled ONLY in the two Requiem Reforged profiles above Dragonborn Reskin - Quickloot; DISABLED in the four controller profiles | It is a QuickLoot IE 4.x reskin; the play profiles run the 3.4.1 controller downgrade (15 dead MCM rows, modifier keys mis-encoded on that DLL). Using it on the play profile means moving that profile to QuickLoot IE 4.x - the reason for the downgrade is unrecorded. |
| BH's Rustic Farmhouse Retexture 4K (191807) | directly above Riton Farmhouse parallax III, BELOW Nordic Stonewalls | 33 BC7 textures (24 at 4K, 9 at 8K). Nordic Stonewalls keeps its matched diffuse+normal+height set for stonewall01/stonefloor01 (TruePBR shapes in the PBR profile anyway); BH replaces the Riton-owned stems (farmhouse01, stonewall02, thatch, thatch interior, wood posts, walkways, walls). Caveat: those meshes are parallax-typed and keep sampling Riton's heightmaps under BH's albedo (BH ships only complex-material masks, which parallax shapes ignore), so seams or floating detail are possible until the mesh shader types are reconciled by the generator pass. The stray "Nova pasta" folder (256 MiB, unreferenced) was left out; Thatch01 is referenced by nothing. |
| BH's Rustic Brick Windmills 4K Op3 v2 (190518) | PARKED DISABLED above Skyrim 3D Windmill (all six profiles) | Cannot show anywhere: its 12 textures are BH-invented names referenced only by its own two meshes, and in every profile the winning windmill and silo meshes are the generator's processed copies of Skyrim 3D Windmill (both output folders carry the same file), which sample other textures. Its own meshes also reference a missing mask and foreign Whiterun masks. Installed and parked; enable only if the mesh winners change. |
| `[NoDelete] Community Shaders` 1.9.1, `[NoDelete] Effects 11` 1.0.0, `[NoDelete] Grass Optimizations` 1.0.0 | disabled everywhere | The official-CS fallback set. |
| DynamicShaderFrameGen - MFG Game Root File | disabled everywhere | See section 2. |

Full-plugin census unchanged: every new plugin is light-flagged.

## First-launch protocol (unchanged rules)

1. Launch the PBR profile once, reach the main menu, quit. Full shader recompile.
2. Claude reads BEFORE any relaunch: CommunityShaders.log (build 1.9.0.0 / "Bottled", features loaded,
   Effects 11 preset, `Invalid settings for ...` lines), DynamicShaderFrameGen.log (`[DLSSNR]
   initialized`, `FPS probe`, `D3D12 proxy active`, provider), NGIO-NG.log (grid 25), skse64.log
   (NMN_DeformableTerrain, AnimatedBoundWeapons loaded), CrashLogger if any.
3. Then re-pin the moved blocks in the regenerated SettingsUser.json and decide Reverse Z as an A/B.

## Launch 1 result (2026-09-25 15:01-15:07): GPU timeout on the loading screen, never reached the menu

- Timeline from the logs: Community Shaders 1.9.0.0 accepted every settings block (the 1.8 file was migrated, no `Invalid settings` lines; SSGI, Reverse Z, Upscaling, Unified Water, HDR disabled at boot as planned). The disk cache was stale, so ~13,000 shader permutations went into a 30-thread async compile at 15:02:27. Frame generation (FSR3 2x) and Neural Rendering came up at 15:02:18-15:02:40 and ran fine for ~30 s.
- 15:02:47: the frame-gen watchdog shows the render thread entering the D3D12 Present and never returning; the on-screen picture froze (watchdog FROZEN detector), went black at 15:02:51. 15:02:56.9: Windows logged nvlddmkm 153 `Resetting TDR occurred on GPUID:100`, then `Reset TDR` / `Restarting TDR` at 15:03:07. Device removed. Frame-gen then logged `Present exception ... 88760870` (D3DERR_DEVICEREMOVED) on every frame, Community Shaders logged hundreds of `Failed to create pixel shader` (creation on the dead device), NR logged `BeginD3D12 failed`.
- 15:07:45 DataLoaded: the Detection Meter plugin created its meter textures on the dead device, got E_INVALIDARG, and dereferenced the null texture (its known missing null check) -> the access violation in the crash log. It is the victim, not the cause.
- Not the CPU: no WHEA record, no LiveKernelReports file, no minidump today; the WER LiveKernelEvent/BlueScreen floods in the Application log are periodic re-uploads of the August/September reports (every few hours all month).
- No Community Shaders compiled shader was in use when the GPU stalled (the first one finished at 15:02:50, after the stall began), so Bottled's shaders are not implicated in this hang.
- Root-cause candidate with the author's own backing: the frame-gen ini was on `FenceWaitBusy=0` (queue-side D3D11 wait on the shared D3D12 fence). The shipped ini says of mode 0: 'can stall the D3D11 QUEUE if the fence is never signalled (the 2026-09-18 18:23 failure)... If the game freezes on 0, set this back to 1'. The watchdog was parked on `stage=d3d11 Signal(fence)` in 1008 of ~1150 samples. The 30-thread compile storm (real frame rate 3 fps at 15:02:56) made the queue ordering irregular.
- Second candidate, untested: ReShade (dxgi proxy, Northman II preset) hooked the frame-gen D3D12 device, both of its command queues and the D3D12 swap chain this launch (ReShade.log), so its effects ran inside the frame-gen present path. Left unchanged for launch 2 so only one thing changes.
- Change made: `FenceWaitBusy=1` (backup `_backups\2026-09-25 - DSFG fence mode after launch-1 TDR\`). Everything else unchanged. The shader cache was saved (3554 files); the compile was not finished (~3,100 permutations remained), so launch 2 still compiles for a while.
- Grass and deformation remain untested (no cell was ever loaded; NGIO never printed its grid line, the deformation plugin never received DataLoaded).
- If launch 2 freezes on the loading screen again: next lever is `NeuralRenderingEnabled=0`, then ReShade off (untick `Reshade - DLL` and `Northman II - Reshade Preset`), one at a time. A larger TDR timeout (TdrDelay) is a system setting the user would have to set; not applied.

## Launch 2 (2026-09-25 16:20): reached the main menu; Effects 11 preset cannot load under Bottled

- Frame-gen fence mode 1 held: no device loss, no errors in the frame-gen log through the loading screen and menu.
- Community Shaders overlay: `ERROR: 4 effect(s) failed to compile` - enbbloom.fx, enbadaptation.fx, enbeffect.fx, enbeffectpostpass.fx from `[NoDelete] Silent Horizons 2 - Data`. These files are KIEFX-encrypted (Silent Horizons 2 core 1.10). The old AIO DLL decrypted them (ENB Extender KIEFX key extraction); the Bottled DLL has no decryption at all, so the compiler sees cipher text. Effects 11 logs `No preset in use` - the Soul Core ENB-style pass is not applied on this profile under Bottled. Same lines were in the launch-1 log; only visible now because the game reached the menu.
- Plain-text ENB shader sets on disk: Rudy ENB, Berserkyr ENB, AMON ENB Reborn. Encrypted: Silent Horizons 2 core, Cabbage (tweaked), E L D E R. Soul Core is a preset for the SH2 core; it does not carry shaders of its own.
- Decision put to the user: (A) roll back to the AIO build (rollback files kept: `[NoDelete] Community Shaders AIO`, `SettingsUser.json.bak-pre-bottled-20260924`, `SettingsDefault.json.stale-aio0824-20260924`, `ShaderCache.stale-aio0824-20260924`); (B) keep Bottled and re-base Effects 11 on a plain-text shader core (re-tune); (C) keep Bottled without an Effects 11 preset and use CS Post Processing.

### Launch 2 follow-up (2026-09-25 evening): the Effects 11 error is by design, not a config fault

Re-checked after the user pushed back ("Effects 11 is in the Bottled build and should work with nearly any ENB effects"). Both halves are true, and this preset is the documented exception:

- The Community Shaders sticky of 26 Aug 2026 states "Support for ENB extender and sh2 shaders has been removed" (1.8.4 dropped every ENB reference). The official Effects 11 page (Nexus 192760, 23 Sep 2026) states "Encrypted presets: Effects 11 does not decrypt shaders ... This includes presets built on Silent Horizons 2 - Shader Core" and that KiLoader must not be installed. The older Effects 11 page (179824) no longer exists on Nexus.
- The August fork build decoded the four Silent Horizons files with a key it read out of the Extender DLL. Bottled 1.0.0 and 1.0.1 follow upstream and have no such code; neither does any public source tree. A third party posted a rebuilt official 1.8.4 DLL with that step put back (Dwemer Mods 4506, 21 Sep 2026). It is for official 1.8.4 only and is not usable with Bottled.
- The only new, author-side development: ENB Extender and Helper 1.6.0 (20 Sep 2026) added "a compiler API to allow development of third party (developer) tools" with an example file. Unverified whether it can serve a renderer. Request draft in the instance root rewritten to ask Bottle about that route.

Routes that keep Bottled: (1) swap the four SH2 effect files and their .fx.ini for a plain-text core and re-tune the post chain, keeping enbseries.ini and the weather inis (Effects 11 applies those natively); (2) wait for a build that uses the Extender API; (3) interim, disable Effects 11 at boot to remove the overlay. Rollback to the AIO was declined by the user.

### Effects 11 follow-up 2 (2026-09-25, later): Extender API read, Bottled 1.0.1 scanned, core swap staged

- ENB Extender and Helper 1.6.0 (the Legacy build for game 1.6.629 to 1.6.1179) exports three new functions: ENBExt_Compile, ENBExt_RegisterForENBCompileCallback and ENBExt_UnregisterFromENBCompileCallback. The author's example links them from an SKSE plugin after the Extender is loaded. The DLL also carries a "standalone initialization" path, so it can run without ENB. This is the author-side route for a renderer to compile the locked Silent Horizons files without touching the key. It needs KiLoader present and reads the game-root enbseries folder.
- Bottled 1.0.1 does not use it: its DLL has no reference to those exports and no decoder. Archive diff against 1.0.0: 41 files changed (DLL, symbols, translations, ten Feature ini files, about 25 shaders), nothing added or removed. Our three local shader edits (volumetric rays clamp, heightmap valley clamp, the six Snow Cover worldspace files) are untouched by the update.
- Core swap staged in the session scratchpad, not placed: "Authoria - Effects 11 Core - NAT (plain)" (Bottle's NAT Effect 11 preset shaders, identical to NAT III's, with Bottle's ini values) and "Authoria - Effects 11 Core - AMON (plain)" (AMON ENB Reborn's four effects with its include tree and ini files). Neither carries an enbseries.ini, a weather list or weather files: Soul Core's stay in charge, so no plugin, region, weather record or Helios twin is touched.

### Effects 11 core swap PLACED (2026-09-25 evening, user's go)

Two new mod folders, both authored from files already on this instance, placed directly above `[NoDelete] Soul Core ENB - Data` in every profile (backups `modlist.txt.bak-e11core-20260925`):

- `Authoria - Effects 11 Core - AMON (plain)`: the four effects of AMON ENB Reborn with its include tree and ini files. ENABLED in DEEZ CS NUTZ - PBR and DEEZ CS NUTZ.
- `Authoria - Effects 11 Core - NAT (plain)`: enbeffect, enbbloom, enbadaptation from Bottle's NAT Effect 11 preset (shaders identical to NAT III 3.1.1C) with Bottle's ini values and the five menu images. DISABLED everywhere; flip it on and AMON off to compare.
- `[NoDelete] Silent Horizons 2 - Data` flipped OFF in those two profiles. PICTA EXPERIMENT untouched (its own preset), the three non-CS profiles carry both cores disabled.

Neither core mod ships enbseries.ini, a weather list or weather files, so Soul Core's stay in charge and no plugin, region, weather record or Helios twin is touched. Rule: only one Effects 11 Core mod enabled at a time. FIRST LAUNCH UNTESTED: expect "[EFFECTS11] Preset loaded" and no red overlay; Effects 11 menu saves land in the enabled core's ini files.

### Launch 3 (2026-09-25 18:02, AMON core): sub-folder includes rejected; NAT made active; AMON rebuilt include-free

- Result: enbbloom.fx and enbeffectpostpass.fx failed (unrecognized UI_WHITESPACE, undeclared TEMP) because Bottled's Effects 11 logged "Include path escapes base directory" for every sub-folder include (UI/, Helper/ and the rest). Same defect as the August build. Under MO2 the include resolver apparently canonicalises the virtual path to the real mod folder and then judges it outside the enbseries base. NAT's three effects have no includes, so they are unaffected.
- Action 1 (automatic, after the game and MO2 closed): NAT core flipped ON and AMON OFF in DEEZ CS NUTZ - PBR and DEEZ CS NUTZ (backups modlist.txt.bak-e11nat-20260925).
- Action 2: AMON's four effects rebuilt with every include pasted inline (44 includes in bloom, 30 in post pass, none left), the Effects 11 bloom-UI shader patch mirrored, and each file test-compiled here as an fx_5_0 effect with zero errors. The rebuilt files replaced the originals in the AMON core mod; originals kept in _backups\2026-09-25 - AMON core inlined\. AMON stays disabled until a deliberate flip and launch.

### Launch 4 (2026-09-25 18:14, NAT core): preset loaded, picture washed out; per-core enbseries.ini added

- Log: all three NAT effects compiled and applied, "Preset loaded", HDR off, Post Processing off. So the wash-out was a settings mismatch: Soul's enbseries.ini drives the new chain with values tuned for the Silent Horizons chain. Differences that matter for exposure: [EFFECT] EnableAdaptation false (NAT's tonemap reads AdaptationMin/Max, confirmed in its shader), [COLORCORRECTION] Brightness 1.0 against Bottle's 0.333 for this chain, [ADAPTATION] Min/Max/Sensitivity/Time/ForceMinMaxValues all different, [BLOOM] amounts about double.
- Fix: each core mod now carries its own enbseries.ini = a byte-for-byte copy of Soul's file with only those chain keys set to that core's values (NAT: 16 keys, Bottle's NAT Effect 11 values; AMON: 13 keys, AMON's own values). The core mod sits above Soul Core ENB - Data, so its copy wins while it is enabled, and Soul's original is untouched. Weather files, weather list and every other section stay Soul's. Effects 11 menu saves of enbseries.ini now land in the active core's copy.
- Untested until the next launch. If still bright: the next levers are [ADAPTATION] AdaptationMax and [COLORCORRECTION] Brightness in the active core's ini, or the same in the Effects 11 menu.

### Launch 5 (2026-09-26 04:07-04:17, NAT core, first in-world session): awful frame rate; grass cost addressed without shrinking it

- Measured: the frame-gen plugin's probe put the real frame rate at 40 to 44 fps; the watchdog counted about 30 hitches over 100 ms and 10 over 500 ms in ten minutes. Shader cache was already full (13 new entries), no grass cache was generated at runtime, no errors.
- The friend's export (August 20 seed) runs Grass Optimizations at its default thinning (MinDensity 0.069, MeshCostBias 0.4) with the pre-Wednesday grass distance, i.e. the configuration this instance had before 09-24. The current setup (100000 units, thinning off) draws every blade out to the far band, which at 4K is millions of one-to-five-pixel slivers.
- Applied with the game and MO2 closed: Grass Optimizations MinDensity 1.0 -> 0.35, MeshCostBias 0 -> 0.25, SimpleShadingPixelSize 4 -> 6; distance, FullDetailPixelSize, EdgeFadeStart and InvisibleFadeCull unchanged (backup SettingsUser.json.bak-grassthin-20260926). Deformation tessellation trimmed per its own ini advice: MaxFactor 64 -> 32, TargetSpacing 2.0 -> 4.0 (backup _backups\2026-09-26 - DTD tessellation trim\). The deformation plugin still logs only "loading"; whether it is active is unknown.
- Not changed: the 51 cache files streamed per cell crossing at grid 25 are the hitch source and only the radius reduces them. Next step if hitching stays: 60000 to 80000 units plus DynDOLOD grass mode 1 so the baked grass billboards take over beyond, which needs a DynDOLOD rerun.

### Launch 6 (2026-09-26 05:07-05:20) and the grass research

- Numbers: same 41 to 42 fps at the start location as launch 5, so the far-band thinning bought little there; later in the session the real rate sat at 25 to 26 in a heavier area, with 30 hitches over 100 ms and 8 over 500 ms. The far grass is not the dominant cost. Per-pass attribution is needed: the Community Shaders performance overlay (hotkey F10 in this install, VK code 121) shows FPS, draw calls, VRAM and CS pass timings as an in-game HUD; it cannot log to file, so one screenshot (Win+PrintScreen lands in Pictures\Screenshots) is the cheapest measurement.
- Trees not swaying: Dynamic Wind is alive (813 tree configs loaded, wind targets set at 05:10 and 05:15), Bottled's lighting shader still carries the tree wind code, no report of this on the Bottled or CS pages. Prime suspect is the deformation plugin's lighting/utility shader geometry hooks, new since 09-24. Test = one launch with it off (flip plans staged in the scratchpad: plan_dtd_off.json / plan_dtd_on.json). The plugin also has undocumented ini keys EnableLogging, LogDraws, LogGeneratedShaders, ProfileInterval that would make it print its own cost to its log.
- Grass Optimizations author (Nexus 188628, posts 09-24 to 09-26): 100000 with fade 0 and DynDOLOD mode 0 is his recommended visual setting, the cap is about 140000 (34 cells), thinning at the feature's defaults is what makes it cheap, loading time grows with distance, and a user reported 20000 + fade 23000 as a good compromise. Mid and far mesh LOD tiers only work with meshes named *_LOD0.nif / *_LOD1.nif under meshes\LOD\Grass, none exist yet; two users report periodic freezes with Mesh LOD enabled.
- DynDOLOD can generate those meshes: test builds (DynDOLOD.x64.exe and TexGenx64.exe dated 2026-09-25 plus Edit Scripts, on the dyndolod.info Test Versions folder) over release Alpha-211; TexGen with HD Grass (Direct 0, Ambient 100, Smoothness 0) and CSGrassOptimizations=1 in TexGen_SSE.ini; DynDOLOD_SSE.ini with CSGrassOptimizations=1 and CSGrassOptimizationsBillboard=DynDOLOD_flat_2x2plain_lod.nif, Advanced mode, "Create assets for CS Optimized Grass". Output = atlas texture, updated full grass NIFs, _LOD0 and new _LOD1. Installed DynDOLOD is Alpha-205 (June); the author recommends regenerating LOD without classic grass LOD when using this. User-run tools only.
- Frame-gen ini note: NRRenderScale 1.00 is full-resolution neural-rendering analysis; the ini comment names 0.75 as the author's sweet spot when base fps is too low. Not changed.

### DynDOLOD updated to Alpha-211 (2026-09-26) for the grass LOD generation

- Tool folder C:\1. AUTHORIA\tools\DynDOLOD backed up whole to _backups\2026-09-26 - DynDOLOD 205 pre-211\ (2294 files). Alpha-211 (Nexus 68518 file 798219, from Downloads) extracted over it; both executables now report 3.0.0.211.
- The archive ships DynDOLOD_SSE.ini, TexGen_SSE.INI and LODGen_flat_lod.nif but not the GUI state files, so DynDOLOD.ini and TexGen.ini were restored from the backup. The eleven customised grass-brightness keys were re-applied into the new DynDOLOD_SSE.ini (11/11). Added CSGrassOptimizations=1 under [DynDOLOD] plus CSGrassOptimizationsBillboard=DynDOLOD_flat_2x2plain_lod.nif, and CSGrassOptimizations=1 under [TexGen] in TexGen_SSE.INI.
- Still missing: the test build (DynDOLOD.x64.exe, TexGenx64.exe, Edit Scripts, dated 2026-09-25, Mega folder) that carries the "Create assets for CS Optimized Grass" option. After it lands, re-check the two ini files and the eleven keys, because its Edit Scripts folder may overwrite them again.

### DynDOLOD test build installed (2026-09-26 06:15) - tools ready for the grass LOD run

- "Test Versions.zip" (95.4 MB, dyndolod.info Mega folder, user's yes) downloaded through the browser pane to Downloads. Contents: DynDOLOD.x64.exe, TexGenx64.exe, Edit Scripts with three LODGen executables, six updated GLSL shaders and the new DynDOLOD_flat_2x2plain_lod.nif template. No ini files, so the grass lines and the eleven customised keys survived the overlay.
- Installed over the Alpha-211 tool folder: the two executables copied under the names MO2 launches (DynDOLODx64.exe, TexGenx64.exe; the 211 release copies kept as .211 in the backup folder), Edit Scripts overlaid. Both test executables report file version 3.0.0.211, which matches sheson's note that the feature "will be part of the next alpha".
- Next: the user runs TexGen (HD Grass, Direct 0 / Ambient 100 / Smoothness 0) and then DynDOLOD in Advanced mode with "Create assets for CS Optimized Grass" checked and classic Grass LOD unchecked, per GRASS-LOD-GENERATION-20260926.md.

### TexGen refused the mixed folder (2026-09-26): tool folder rebuilt clean

- TexGen showed "Installation Error. DynDOLOD Standalone might have been installed over an older version. Unpack into a new and empty directory." The 211 archive had been laid over the Alpha-205 folder, which DynDOLOD's own check rejects (dyndolod.info/Updating: always install into a new or empty folder; carry over only the settings of the last generation and customised ini values).
- Done: the mixed folder renamed to tools\DynDOLOD.old-mixed-20260926 (kept), a fresh tools\DynDOLOD unpacked from the 211 archive, the test build overlaid (executables under the MO2 names, Edit Scripts), DynDOLOD.ini and TexGen.ini carried over from the July folder, the eleven grass-brightness keys re-applied into the fresh DynDOLOD_SSE.ini, the grass lines re-added to both ini files. MO2's shortcuts point at the same path, so nothing changed there.

CORRECTION to the entry above: the rename of the mixed folder was refused by Windows (a handle on the folder), so no fresh folder was created and the script's later steps ran on the mixed folder, duplicating the grass lines. Fixed in the next pass: the grass lines deduplicated, the two July preset files (Presets\DynDOLOD_SSE_Default.ini and DynDOLOD_SSE_TexGen.ini) carried over as the update page allows, and every file not belonging to the 211 archive, the test build or the carried-over settings deleted from tools\DynDOLOD, with old logs and the caches removed. The folder now equals a fresh unpack plus the settings, which is what DynDOLOD's installation check wants. No folder was renamed.

### Plugin fault found by TexGen and fixed (2026-09-26 06:37): stale Einar Wardrobe belt override

- TexGen's loader: "Record [ARMA:FE26A804] in file DD - Einar Wardrobe.esp is being overridden by record [ARMO:FE26A804] in file DD - Einar Wardrobe UBE patch.esp". The base mod (v5.5, installed 2026-07-15) reuses local ID 0x804 for the armour addon of the Idun tunic 2; the TOTOxDD UBE patch (2025-08-17) still overrides that ID as the removed belt armour, and Authoria - Patch - Reqtificator Masterlist Relief.esp (2026-08-27) had copied that stale record. The only error of this kind in the whole load order per the TexGen log. In game the winner for that ID was an armour body over an armour-addon form: Idun Wardrobe 2 broken or crash-prone on equip.
- Fix, applied with MO2 closed by a watcher: the stale ARMO record (273 bytes) removed from both plugins and the enclosing group size shrunk; nothing else changed. Backups: _backups\2026-09-26 - Einar stale 0x804 override drop\ (both originals, .before). Record counts 34 -> 33 and 892 -> 891.
- Coverage note for later: 5.5's new Idun and Robe3 armours (0x843, 0x845, 0x847) have no UBE overrides; UBE actors get the vanilla-lane meshes for them.
