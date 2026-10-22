# Picta on Bottled Shaders + DLSS 5 Neural Rendering via dlss-unlocked + the friend's Picta fixes — the plan

Written 2026-09-30, revised twice the same day: after the source reading, and after a 15-agent
adversarial pass that refuted or qualified every load-bearing claim against the live source, the
Extender binary, the OptiScaler source and this instance's files. **Workstream A was BUILT on
2026-10-01** (see "As built" directly below; it supersedes sections 0, 1 and 3 wherever they differ).
Every other step carries the evidence so it can be checked before it is taken.

Three jobs:

- **A.** Get the Picta ENB preset rendering through Bottled Shaders' Effects 11.
- **B.** Replace DynamicShaderFrameGen with the dlss-unlocked route for DLSS 5 Neural Rendering.
- **C.** Take in `Picta - Authoria Fixes - 2026-09-30.zip` (the friend's package).

Built and tested separately, one variable per launch, then merged.

---

## As built 2026-10-01 (workstream A) — read this first

**Decisions, final.** Lane = new profile `DEEZ CS NUTZ - PICTA` (copy of PBR's live lists). Picta AS
SHIPPED, nothing from August. Shader core 1.10. Bottled accepted as shipped. Frame generation XeFG 2x.
Upscaling DLSS **Quality** from the first upscaled launch ("lets go more fps"). The friend's list-wide
record changes are held ("go with shipped fixes from bottled first"). Unticks: the interior-fog remover
is off in the Picta profile now; the Bruma weather-compatibility plugin goes off when his Bruma patch
goes in. ReShade (Northman II) stays on: standing user decision of 09-27.

**New mods (all enabled in the Picta profile only).**
| Mod | Content |
|---|---|
| `[NoDelete] Picta ENB 1.0.1 - Data (shipped)` | the ENB 1.0.1 archive, byte for byte, in Data form (`enbseries.ini` + `enbseries\`), minus `enblocal.ini` and the `KreatE` folder. ONE generated file: `enbseries\_weatherlist.ini` = the shipped `Picta - Weatherlists\01_Skyrim.ini` sections (91 with an existing file) + the 9 shipped interior sections, in the one file Effects 11 reads; shipped original kept as `_weatherlist.ini.shipped-original`. Picta ships its routing for the ENB Worldspace Weatherlists plugin, which Effects 11 never reads. |
| `[NoDelete] Picta - Weathers of Aurbis 1.0.1 (shipped)` | esm, esp, ini from the Plugins 1.0.1 archive |
| `Authoria - ENB Extender 1.6.0 - KiENBExtender only` | `KiLoader\Plugins\KiENBExtender.dll` (Legacy build), no helper DLL |
| `Authoria - Picta ENB - Root twin` | `Root\enbseries.ini`, the four `.fx.ini`, `enbfxcompiler.ini` (SH2 keys + grafting off + both caches off); sits directly above the SH2 root core |

`[NoDelete] Picta - Assets 4K`: shipped `clouds.nif` restored (the August edit kept beside it).
`houseCARL - Authoria - Picta over NAT`: reused, verified equal to the shipped esm's records.

**Profile switch (four files in lockstep; backups `*.bak-picta-lane-20261001`, `modlist.txt.bak-picta-kreate-20261001`).**
On: SH2 Data, SH2 root core, KiLoader, the four new mods, the 4K pack, Picta over NAT.
Off: NAT plain Effects 11 core, Soul Core ENB Data, Soul Core Plugin and Assets, Soul Core ECSS and
Wyrmstooth patches, Astralite Weathers + 4K Clouds, the Gray Cowl / Dawn Warmth / Snowy Holds Astralite
patches (Snowy Holds masters Astralite), Extender 1.4.3, `[NoDelete] Soul Core - KreatE Templates` and
`KreatE` (the Soul Core KreatE preset zeroes fog on 52 Lux templates at runtime, which would undo the
interior-fog untick; KreatE is off until Picta's own shipped KreatE preset is installed and its
selection tested: `overwrite\KreatE\UserSettings.ini` ActivePreset is shared by every profile).
Plugins: 8 removed with their mods, `Helios_Astralite.esp`, `Helios_Astralite_Seasonal.esp` and
`Authoria - Patch - Remove Interior Fog - Lux.esp` deactivated, `Picta - Weathers of Aurbis.esm` after
`VweaponsALL.esl` (before the output masters), `Picta - Weathers of Skyrim.esp` + `Authoria - Picta over
NAT.esp` after `Mists of Tamriel.esp`. The four parked Picta lines left the top of the modlist.
Result: 4,040 enabled mods, 4,145 live plugins, 246 of 254 full, 0 missing masters, output tail unchanged.
`overwrite\Root\enbcache` (Extender 1.4.x caches, Jul-Aug) moved to `_backups\2026-10-01 - overwrite Root
enbcache (Extender 1.4.x, Jul-Aug)`. `SettingsUser.json.bak-pre-picta-bridge-20261001` taken; file untouched.
Tool: `_tools\picta-bridge\sync_root_twin.py` (re-sync the twin after any editor save).

**Verified by a 14-agent read-only pass (2026-10-01):** every new file equals its archive; the bridge
layout satisfies every file open on both sides of the source; Tamriel, Whiterun tundra, the Rift and
Solstheim roll 100% Picta-native, routed weathers (64 of 65 Picta regions and all 9 climates win; all
185 Picta weathers uncontested); no masked weather-ID collision on any routed ID.

**Known, accepted for A1 (all shipped state or inherited order):**
- Every save in the profile sits in the Alternate Perspective start forest, whose one weather is NOT
  routed. Unrouted weathers use the shipped base `enbseries.ini`, whose `[SKY]` values (gradient 50,
  clouds 40) model as white. The SKY reading counts only in a Tamriel exterior. Unrouted too: Soul Cairn,
  Apocrypha, Skuldafn, Labyrinthian maze, Karthspire, Volkihar isle, most mod worldspaces (workstream C).
- The shipped base ini has adaptation ON, volumetric rays ON, `DisableWrongSkyMath=true`. The sky model
  has no adaptation term: pumping or dim exposure is adaptation, not the bridge.
- Cloudy-Windy weathers show magenta mirrored lettering (five placeholder cloud textures in the 4K
  archive itself); five main-quest cloud textures are missing from the archive. Fix = the friend's
  textures, step C1.
- Picta's interior profiles do not apply as shipped (`EnableLocationWeather=false`). Interiors are out
  of scope for A1. Seasonal weather gating and Helios twins are gone in this lane.
- ReShade's Northman II grade sits on top of the picture (F7 overlay toggles techniques).
- The shipped esp has 12 dangling weather entries (Soul Cairn, Mind of a Madman, a few small regions).
- A1 runs at today's native 4K + FSR3 frame generation (DSFG). The fps work lands in B0/B1.

**Launch A1 (the user's part).** 1. Launch PBR once first (L0: main menu, quit) so Bottled 1.0.4's own
first run is not mixed into the bridge test. 2. In MO2 pick `DEEZ CS NUTZ - PICTA`, launch. If the
game closes within seconds, launch again (KiLoader satellite). 3. From the main menu console:
`coc WhiterunExterior01` (or load a save, accept the missing-content prompt, and get outdoors in Skyrim).
4. Stand a minute, look at the sky, open the Effects 11 editor once, do NOT press Save, quit normally.

**Log checklist after A1 (mine; compare timestamps with the launch first).**
- `C:\Users\User\AppData\Local\KiLoader\SkyrimSE\Logs\KiLoader.log` + `KiENBExtender.log`: fresh,
  `[1.6.0]`, "ENB unavailable" + standalone init, which ini it parsed, no "Unable to open/read file";
  no fresh `ENBHelperSE.log` / `ENBWorldspaceWeatherlists.log`.
- `C:\Users\User\Documents\My Games\Skyrim Special Edition\SKSE\CommunityShaders.log`: pass = four
  "Loaded encrypted FX file through ENB Extender", four "Successfully applied effect", one "Preset loaded
  from ... Data\enbseries", no "Weather file not found". Expected and benign: "Effect file not found,
  skipping" for enbdepthoffield.fx and enblens.fx; "[WeatherManager] Failed to read sections from
  _locationweather.ini" (shipped file has its headers commented out). A successful list load logs nothing.
  UI-variable ceiling (compile-time keys can never appear): enbeffect 524, postpass 1150, bloom 427,
  adaptation 69; within about 10% = full fidelity.
- Same folder: `DynamicShaderFrameGen.log`, `skse64.log`. `ReShade.log` syncs back to the ReShade mod.
- Hygiene: `Stock Game` = Data + 12 files; no `BuildData.json` under `plugins\data\rootbuilder\...`; no
  new `enbcache` in the game root or `overwrite\Root` (if one appears, the Extender ignored the twin's
  cache keys: record it, move it out); `overwrite\SKSE\Plugins\CommunityShaders` (new SettingsDefault,
  rewritten SettingsUser expected); re-hash the Data mod against the archive and the twin against it.

**Launch A1 result, 2026-10-01 07:53 (main menu only; the user quit before going in-game).**
BRIDGE PROVEN: KiLoader loaded the Extender 1.6 with no dialog; the Extender initialised standalone; all
four Silent Horizons effects compiled through it and applied; preset loaded from Data; weather data for
103 weathers per effect. Picta's compile-time options are honoured (read from the root twin): proven by
decoding the variable names in the Extender's cache against the ini keys (counts match the log exactly:
162 / 31 / 191 / 220). The Extender ignored the cache-off keys and wrote `enbcache\extexternal.sc`; it now
lives in the root twin mod. DSFG frame generation and NR initialised; the five batch-3 DLLs loaded.
STILL OWED: the sky reading in a Tamriel exterior (launch A1b), then B0/B1.

**Fixes after the first session, and the fps stage (BUILT 2026-10-01 afternoon, Picta profile only; launch owed).**
User: "1. go 2. yes 3. yeah i want to drastically improve the fps. it used to be so good" (it used to be
Community Shaders' own DLSS Quality + FSR3 frame generation, before 08-29).
- New mods: `[NoDelete] Picta - Cloudy Windy panoramas 11-15 (2K originals)` (above the 4K pack);
  `Authoria - Picta - Bottled raindrop` (`enbseries\enbraindrops.png`, switches Bottled's rain branch on);
  `houseCARL - Authoria - Patch - Wanderers Fair - Picta Climate` (ESL, CLMT 000A15:SkyrimFair.esp ->
  Picta tundra weathers 1A0091-1A0096; plugin after `Authoria - Patch - Holidays and Fair - Requiem.esp`);
  `[WEATHER901]` appended to the lane's `_weatherlist.ini` (10A240, 10E1EE, 10A243, 10E1ED -> Whiterun
  tundra lightly cloudy; still used by Olenveld regions). Backups `*.bak-picta-fixes-20261001`.
- fps stage: `-DynamicShaderFrameGen` in the Picta profile; `+Bottled - Upscaling runtime 1.0.4` (the 20
  parked files, directly above the Bottled mod); `+Authoria - dlss-unlocked 0.9.32 (OptiScaler NR)` (Root:
  `winmm.dll`, `OptiScaler.ini`, genuine `nvngx_dlssnr.dll`, `OptiScaler\nvngx_dlss.dll` + XeSS/XeFG/XeLL
  DLLs); `SettingsUser.json` "Disable at Boot"/"Upscaling" false (backup `.bak-pre-upscaling-20261001`),
  `streamlineLogLevel` 1 for the first launch (back to 0 after). Existing Upscaling block = DLSS, Quality
  (2560x1440 render), FSR3 FG, frame limiter 82.5 real / 165 shown. Both stages enabled in ONE launch
  (the plan's B0-alone launch was skipped to save the user a launch). Backups `*.bak-picta-fps-20261001`.
  OptiScaler.ini vs package: 28 lines (the section 4 keys + `[Menu]` FGShortcutKey / FpsShortcutKey /
  FpsCycleShortcutKey = -1, ShortcutKeyRequireAlt=true (overlay = Alt+Insert; End, PageUp/Down and Insert
  are taken by Bottled, KreatE, dMenu, Display Tweaks), ShowFps=true, `[Hotfix]` CheckForUpdate=false).
- Verified by a 5-agent pass: no blocker. Confirmed risks: (1) a runtime XeFG/XeLL failure is a CRASH at
  device creation, not a silent no-FG (Bottled's DX12SwapChain.cpp dereferences the failed context);
  (2) if DLSS is not reported available Bottled silently falls back to FSR 3.1 upscaling = normal picture,
  no NR; (3) refraction shimmer returns under upscaling (ice, glass, wards, heat haze); (4) the Picta post
  chain still runs at 4K after the upscale.
- PASS lines. `CommunityShaders.log`: "Upscaling.ini 1-4-0 successfully loaded", "[Streamline]
  Successfully initialized Streamline", "[Streamline] DLSS is available", "[FidelityFX] Loader DLL loaded
  from", "[Frame Generation] Frame Generation enabled, using D3D12 proxy", "dynRes ratio 0.667x0.667",
  "[Effects11] Loaded raindrop texture"; NOT "[FidelityFX] Created FSR3 context" (= FSR fallback, no NR),
  NOT "slEvaluateFeature failed", NOT "[FidelityFX] Failed to create swap chain context!".
  `C:\1. AUTHORIA\logs\OptiScaler.log` (Info level: "UiResource found" and "nvngx_dlss.dll found at" may
  be absent): "working as winmm.dll", "Enabling DLSS", "Creating new DLSS w/Dx12 feature", "DLSS-NR:
  feature created", "XeFG swapchain created", "XEFG_SWAPCHAIN_RESULT_SUCCESS"; NOT "disabling DLSS", NOT
  "External frame generation: leaving".
- FALLBACK LADDER (one flip per relaunch, MO2 and game closed): 1. `SettingsUser.json` Upscaling
  `frameGenerationMode` 0 (DLSS + NR, no frame generation; the only step proven from source; shared file).
  2. restore mode 1, `OptiScaler.ini` FGInput=nofg + FGOutput=nofg (Bottled's own FSR3 FG with NR;
  unverified pass-through). 3. `-Authoria - dlss-unlocked ...` (DLSS Quality + FSR3 FG, no NR).
  4. full rollback: both new mods off, `+DynamicShaderFrameGen`, boot lock Upscaling true.
  ReShade trouble on the new swap chain: the fork's documented layout is ReShade as `ReShade64.dll` +
  `[Plugins] LoadReshade=true`.
- Noted, not done: `overwrite\Root` holds 3.4 GB of old screenshots that Root Builder copies into the game
  root on every launch (the user's files; ask before moving); SSE Display Tweaks SwapBufferCount auto (3)
  vs Bottled's proxy accepting only 2 on a later resize.

**Session 2 (2026-10-01 10:40-11:06) results, and fixes built 2026-10-02.** User: "FPS is better but not great.
looks like no NR. clouds are fixed, rain is fixed, the fair FPS is ass and NPCs keep disappearing and reappearing".
Verified (5 investigators + 3 skeptics; digests in the session scratchpad wf4_digest.txt / wf5_digest.txt; memory
picta-bottled-first-session-findings-20261001.md "Session 2"): every PASS line above held; real fps forest 39 / Riverwood
31-32 / inn ~24 / fair 24-25 (XeFG doubles it in play; off in menus/pause/load by design); NR ran every frame but pre-SR at
1440p (invisible to the user); ReShade sits after XeFG (runs twice per real frame). LOG CLOCK TRAP: the proxy's "Frame count
jumped" warning = every 2nd real frame; the NR timing line = every ~601 frames.
User picks 2026-10-02: "1. yes, patch the fair 2. what? no just fucking get NR working nicely 3. um, I think you should be
able to get any of that data already" (no split-screen proof, no user-side measuring).
- BUILT: `houseCARL - Authoria - Patch - Wanderers Fair - No Reseat` -> `Authoria - Patch - Wanderers Fair - No Reseat.esp`
  (ESL, masters Skyrim.esm + SkyrimFair.esp; quest 0014BD:SkyrimFair.esp verbatim with SkyrimFairAudioScript property
  SeatLayoutVersion 4 -> 0; byte-compare vs SkyrimFair.esp = exactly one byte in VMAD). Skips the re-entrant seat reset on
  new games (the 39-sitter disable/enable loop). Picta profile: mod enabled directly above the climate patch, plugin right
  after `Authoria - Patch - Wanderers Fair - Picta Climate.esp`, group Authoria - Reqtificated; disabled line in DEEEZ
  NUTTZZZ / DEEZ CS NUTZ / PBR / PICTA EXPERIMENT (Reforged Main/NSFW have no anchor outside the protected block: untouched).
  Live 4,147 / full 246 / missing 0. Backups `*.bak-picta-noreseat-20261002`. Watch: Papyrus "SkyrimFairAudio: re-seated"
  must NOT appear; doubled "song N playing" lines = the show path is re-entrant too (then A2: recompiled script with a
  whole-OnUpdate busy guard).
- `streamlineLogLevel` back to 0 (backup `.bak-pre-s3-20261002`).
- NR ON THE FINISHED PICTURE (built 2026-10-02 after a 3-approach design pass + judge; digest wf6_digest.txt). The proxy's
  finished-picture route is refused for a DX11 upscaler bridge on a DX12 swap chain, although here bridge and swap chain
  share one D3D12 device (log 227 vs 17851). `Root\winmm.dll` PATCHED, 3 bytes (sha256 7c4897a0...e3c ->
  08e563b44b930f5fbd4dd98ffca33f92547dee2c9f370bab0d27c46e8aac1792): file 0x3186E2 75->EB (RVA 0x3192E2 jne->jmp, skips the
  refusal that loads "This finished-picture route requires DirectX 12 or the DirectX 11 bridge."); 0x32234D and 0x32235C
  59->10 (RVA 0x322F4A / 0x322F59 mulss->movss: model MV scale = the game's 2560x1440 instead of x workWidth/width, which
  would be 1706.7 at WorkingScale 0.6667). Ini [DlssNr]: RunBeforeSR = false, FinishedPicture = true, WorkingScale = 0.6667
  (model 2560x1440 = DLSS Quality render size; the MV fix is exact only while model size = render size). Originals in
  `_backups\2026-10-02 - dlss-unlocked 0.9.32 originals (pre NR finished-picture patch)`. ANY proxy update silently drops
  the patch: re-check the hash. PASS lines: no "requires DirectX 12" line; "feature created at 2560x1440"; "after SR ...
  already tone-mapped so the colour transform is off"; "finished picture: Applying NR to the finished picture."; "finished
  picture: N frames, 3840x2160, OptiScaler FG true, same producer queue true" every 300 frames; GPU window ~4.3-5.3 ms; no
  "PrepareDlssNrInput"/"before SR". FALLBACK (same patched DLL): RunBeforeSR = true, FinishedPicture = false, WorkingScale =
  1.0, WhitePointSource = 3, AutoExposureTrim = 2.0. Device-removed crash -> restore the original DLL. Too soft -> WorkingScale
  0.75 (+~1.4 ms).
  SESSION 3 (2026-10-02 07:50-07:57): the route ran on every frame, same queue, no errors, NR 5.5 ms model - but the
  frame came out near-black with speckles (ReShade shot 94.5% luma <= 8/255; normal shots 0-4.5%). Diagnosis (wf7_digest):
  in SDR passthrough the resolve adds (model answer - model input) with only a 0.5x..2x code-value guard, so a model answer
  ~2x too dark passes through; leading suspect = the model gets Bottled's 10-bit R10G10B10A2 back buffer as input AND output
  texture (the fork converts only HDR10/scRGB to FP16 on DX12; DSFG used RGBA8, session 2 FP16). NOT the 3-byte patch.
  SESSION 4 build (2026-10-04, user picked "1"): [DlssNr] SpatialCompression = true, SpatialCenterX/Y = 98, SpatialWorkX/Y =
  99 (the only ini switch that gives the model FP16 textures; near-uniform layout, model 2536x1426; MVs ~1/3 short in the
  spatial pack -> possible trailing on fast turns). Ini backup `OptiScaler.ini.session3-finished-20261002` in the _backups
  folder. PASS: "feature created at 2536x1426" (2560x1440 = spatial did not engage); no spatial "did not run"/fallback
  lines; a screenshot's near-black share in single digits. FAIL (black again) -> clean session-2 state: original DLL,
  RunBeforeSR = true, FinishedPicture = false, WorkingScale = 1.0, Spatial* = auto; then tell the user visible NR has only
  worked through DSFG.
- Background logger (mine): scratchpad `s2\fps\fps_logger2.ps1` (one-shot nvidia-smi per row, BelowNormal, thread IDs,
  waits up to 12 h for SkyrimSE.exe, stops when it exits).

**PICTA 1.1.0 / BOTTLED 1.0.7 (2026-10-06).** User: "okay so picta got a huge update. I want to look at these files and
figure out updating and getting the FPS under control". 5 investigators + planner + skeptic (scratchpad wf8_digest.txt, p110\).
Findings: Picta 1.1.0 = 23 shared master weathers (19FA01-19FE14), Falkreath regionals deleted; ENB + Weather Mod must go in
together with a rebuilt list (shipped list has wrong storm IDs WEATHER442-446 and the E02 file-name typo; corrected draft in
p110\enb\draft); no new core (only postpass KiSuite Extend Time Separation false->true -> refresh the root twin, move
extexternal.sc aside); Bottled 1.0.7 = 38 changed + 7 added files, Upscaling byte-identical, Extender bridge unchanged, log renamed
BottledShaders.log, three new features ON by default. Skipped: Global Particle Normaliser (1.5.97 only), XPMF + Simplicity of Snow
(snow look; would force PGPatcher/DynDOLOD reruns). FPS: GPU-bound (98-99% at the 575 W cap, main thread ~35%).
User picks 2026-10-06: "1. yes, lets peel back some of the heavier reshade features but keep depth of field thats my fave
2. corrected 3. fix all 4. use the seams correction 5. sure".
- STAGE 1 BUILT 2026-10-06 (launch owed): `[NoDelete] Bottled Shaders` -> 1.0.7 (45 files; 424 files; SnowCover edits kept;
  backup `_backups\2026-10-06 - Bottled 1.0.4 pre-1.0.7`; meta.ini version keys repaired). SettingsUser.json Disable at Boot +
  FurShells true, HairBacklighting true; LandscapeSeams left ON (user). SettingsDefault.json and ShaderCache moved aside
  `.stale-bottled104-20261006` (full recompile). New mod `Authoria - ReShade - Picta lane preset` (Root\Northman II.ini without
  SSDO_Plus and PCGI_One, MagicDOF kept; Root\ReShade.ini PerformanceMode=1): `+` at line 87 in the Picta profile above Northman II
  and Reshade - DLL, `-` in PBR / DEEZ CS NUTZ / PICTA EXPERIMENT / DEEEZ NUTTZZZ. NR session-4 spatial build rides along unchanged.
  Archives copied to D:\1. MOD STUFF\1. SKYRIM FILES. Checks after launch: BottledShaders.log (Effects11.ini 1-1-0, Upscaling.ini
  1-4-0, no FurShells/HairBacklighting load, 4 encrypted FX, raindrop, DLSS available, FG D3D12 proxy, 107 weathers, no FSR3
  context); OptiScaler.log spatial PASS lines; ReShade.log no GloomAO/RadiantGI compile.
- STAGE 1 RESULT (launch 2026-10-06 06:34-06:43): Bottled 1.0.7 healthy (its main log is STILL CommunityShaders.log;
  BottledShaders.log holds one line). FurShells/HairBacklighting disabled at boot, LandscapeSeams loaded, 4 encrypted FX,
  raindrop, DLSS available, FG proxy, 107 weathers. FPS: start forest ~55-58 real (~110 shown) vs 36.5-40 before (ReShade cut
  + Bottled 1.0.7). GPU still 97-98% at ~560-575 W. NR spatial finished-picture route engaged (2536x1426) but the picture was
  near-black and blotchy again -> the finished route is DEAD on this proxy. REVERTED 2026-10-06: original winmm.dll
  (7c4897a0...72e3c) + [DlssNr] identical to the 10-02 pre-patch ini (pre-SR, WorkingScale 1.0); patched DLL and the session-5
  ini kept in the _backups folder. Two new Effects 11 errors to check: KiSU SMAAAreaTexDX10.dds / SMAASearchTex.dds not found.
  Stage 2 found an AUGUST patch still active: "Authoria - Picta over NAT.esp" (24 vanilla WTHR + 2 GMST forwarded from Picta
  1.0.1 over NAT-ENB.esp) - must be rebuilt for 1.1.0 (design workflow wf_3348793c-58e).
- B19 TRIAL BUILT 2026-10-06 (launch owed; user: "1. yes 2. NR two 3. yes 4. yes"). PureDark Skyrim Upscaler AIO Build 19
  Hotfix1 (plugin 1.0.2.0) as mod `Skyrim Upscaler AIO Build 19 Hotfix1` (+ at Picta line 45; - in PBR; other profiles have no
  upscaler section). Community Shaders mode: Bottled keeps DLSS Quality (Disable at Boot Upscaling stays false, runtime mod on);
  B19 does DLSS-G (Dynamic MFG target 60) + DLSS NR after the upscale on the hudless finished picture, 2 passes (Intensity 1.0
  cap per pass, style 2, tone 0.75, structure 0.9, autoskin), HUD fix method 0, ReShade before its FG. DLL renamed
  SkyrimUpscalerNew.dll + SkyrimUpscalerNew_preload.txt (Bottled blacklists SkyrimUpscaler.dll). Keys F6/F3/F8. dlss-unlocked
  proxy `-` in Picta. SettingsUser.json + SettingsDefault.json Upscaling frameGenerationMode 1 -> 0 (backups .bak-pre-b19trial-20261006).
  Old 09-16 PureDark log kept as SkyrimUpscaler.log.b13-goodstate-20260916. Genuine NR dll staged as nvngx_dlssnr.dll.genuine.
  RISK: NR device routine identical to B14H2 (posterized 09-02) - check the main menu. ROLLBACK: B19 mod off, proxy on,
  frameGenerationMode 1 in both json files. Picks 3+4 (stage 2): fix the reused-ID links in the four story-scene weathers; add
  the extra fallback block to the corrected weather list. Nordic Winds 10-06 patch (ESL, 68 SNDR, masters Skyrim/Picta esm/
  Nordic Winds.esp) goes in with stage 2. Stage-2 design: scratchpad wf9_digest.txt (21-step sequence).
- B19 TRIAL RESULT (launch 2026-10-06 11:39-11:43): constant flicker on main menu, loading screen and in game. Logs: B19
  "DLSSNR Init: adapterIndex=-1 onCompanion=1 ... NR will run on companion/FG GPU" (the B14H2 path); CommunityShaders.log
  "[E] Legacy jitter/SetCameraData functions do not match ... camera-projection adapters not installed" (B19 AsyncLook camera
  hooks load first via the preloader and break Bottled's jitter hooks); B19 found MV/depth "3840 x 2160" (treats Bottled's
  1440p sub-rect as native). GPU ~30% in the main menu. ROLLED BACK 2026-10-06: B19 `-`, dlss-unlocked `+` (original DLL),
  frameGenerationMode 1 in SettingsUser.json + SettingsDefault.json (backups .bak-pre-b19rollback-20261006). B19 folder kept.
  User then supplied research sources (dlss-unlocked + XeMFG guide, Nexus 192945, OptiScaler v10.0.0-dev screenshots,
  OpenShaders DLSSNR 0.3.0, DSFG 1.0/experimental/MFG root, DSFG SSE Display Tweaks ini): research workflow wf_4867ca96-d35.
- STAGE 2 (next, new game): Picta 1.1.0 pair + corrected list + root twin refresh + fair/Tamriel climate patch rebuild + Clear Mist
  copy + the four vanilla weather overrides' dangling links (user: "fix all") + Nordic Winds 10-06 patch if clean.
- STAGE 3 (user "sure", after stage 2 numbers): DLSS Performance + NR WorkingScale 0.5, skylighting 66/0.5, shadow samples 4,
  skin samples 8 (VL High = Custom here, no gain; DLSS preset K optional).

- SESSION 6 BUILT 2026-10-06 (NR after DLSS at 4K, the guide author's placement): proxy ini [DlssNr] RunBeforeSR false,
  Style 0, Intensity 1.0, LocalStructure 1.0, LocalTone 1.0, SkinStructure -1.0 (user pick "Guide author's"). No Compare wipe.
  Original DLL. Logger capture_s6_postsr_20261006. If NR is still invisible: check with the user before the DSFG lane (user pick).

- SESSION 6 RESULT 2026-10-06: NR after SR at 4K worked as designed (8.0-8.5 ms; 46 real / 92 shown) but a half-speed GPU
  state (99% util, ~345 W, +20-23 ms per real frame, 22.6 real) hit in RaceMenu and from 15:25:57 to quit. Cause unknown
  (scratch wf12_digest.txt). User: "FPS was SOOOOO bad".
- SESSION 7 BUILT 2026-10-07: proxy WorkingScale 1.0 -> 0.6667 + 3-byte patched winmm.dll (motion-scale fix), stage-3 trims
  pulled forward in SettingsUser.json (OcclusionUpdateInterval 66, OcclusionDistanceCulling 0.5, LocalShadowSamples 4,
  BurleySamples 8). Backups *.bak-pre-s7-20261007. Logger v3 capture_s7_20261007. Expect ~52-60 real normal, ~24-26 if the
  half-speed state returns. Next if under 50: stage-3 DLSS Performance with WorkingScale 0.5.

- SESSION 7 RESULT (launch 2026-10-08 04:47): NR after SR at 2560x1440 = 4.1 ms as designed. Inn 39 real / 78 shown
  (XeFG on); 150 s load with Windows Update running; crash 04:55:27 in nvgpucomp64 (NVIDIA shader compiler worker) 5 s after
  Bottled compiled a 328 KB Lighting pixel permutation (LANDSCAPE_SEAMS + wetness + water + volumetric shadows ...) in 15.9 s
  on stepping outside the inn. No hardware capture (logger died with the 10-07 reboot). Diagnosis workflow wf_06c51599.

- PEELED BACK 2026-10-11 (user): proxy OFF in PICTA + Preset Studio, Bottled FG mode 0; test Picta + Bottled only. DLSS
  Quality upscaling, ReShade lane preset, stage-3 trims and Picta 1.0.1 stay. The proxy mod folder and its ini/DLL are kept.
  Also installed: BnP - UBE Skin - Freckles (player skin) above Sayble Skin in both profiles.

**Follow-ups parked (not for A1):** Picta's shipped KreatE preset (17 interior weather files) as a
lane mod + per-profile preset selection; the 8 stale `plugingroups.txt` lines; `stars.nif` and mist
meshes where other mods beat the Picta pack; Forgotten Vale / Darkfall Passage climate forwards in the
FWMF master patch; a Picta seasonal REGN patch if the lane is kept.

---

## 0. The short version

**Net is right about the mechanism. Nobody has run it yet, and one thing about it cannot be known
without a launch.**

- Bottled 1.0.2 added a bridge for encrypted shader cores; the shipped 1.0.4 DLL has it. For each
  of the four core files it asks ENB Extender 1.6.0's own compiler (loaded by KiLoader) for the
  bytecode. Picta runs on the Silent Horizons 2 core, which is that encrypted core.
- It needs **Extender 1.6.0** (we have 1.4.3, no compiler API; the right 1.6.0 archive is on D:),
  **KiLoader on**, the helper DLL left out, and the core deployed to the **game root** by Root
  Builder, because the Extender's compiler reads only from there (disassembled). Effects 11 keeps
  reading the Data copy.
- The one thing only a launch can tell: Picta's ~55 compile-time shader options (the `|::` keys:
  tonemapper choice, weather separation, bloom pass count, dither) may not reach the Extender's
  compiler in this standalone mode. If they do not, the render is "Picta's runtime values on SH2's
  default compile-time configuration". The first launch's "Loaded N UI variables" counts decide it.
  Bottle himself only says "it seems to load".
- The GitHub file you sent is the August version of that code. The live source is Bottle's repo,
  branch `Bottle-Compendium`.

**The sky under Bottled: keep Picta as shipped.** Bottled now renders the ENB sky-scattering
section with its own formula. The verification pass caught an error in my first model: Picta's
shipped gradient dimmers (0.025 × 0.075) times its shipped air glow (1000) model to a **blue sky,
dimmer than Soul Core at the zenith and hot at the horizon toward the sun**. What goes white is the
August regrade (gradient 1.0, top 2.0) combined with the new scattering. So the August gradient
repairs come back out, key by key, the shipped scattering stays, and the horizon is dialed only
from an in-game reading. Nothing in the sky applies at all until the encrypted preset compiles.

**The DLSS 5 route fits, with three fixes the readme does not mention.** The dlss-unlocked package
ships its ini with a flag that forces frame generation off; the proxy looks for its DLSS core on the
physical disk before MO2's virtual file system exists and would silently fall back to FSR 2.2 with
no neural rendering; and without a process filter it also loads into the SKSE loader. All three are
one-line fixes. The proxy must be `winmm.dll`. Bottled's own upscaling first, alone, then the proxy.

**The friend's package**: a full Picta rollout on real ENB, 160 files, manifest clean. Fifteen of
his 28 patches have their masters here, twelve do not, one needs a rebuild. His routing lists must
be merged into ours, not dropped over them. His 25 profiles need the same Effects 11 treatment as
Picta's own files. Section 5.

---

## 1. Where things stand today (verified 2026-09-30)

### Profiles
| Profile | Renderer | Frame gen / NR | ReShade | Weather look |
|---|---|---|---|---|
| DEEZ CS NUTZ - PBR (play) | Bottled 1.0.4, **first launch owed** | DynamicShaderFrameGen 0.57 | on (dxgi.dll) | Astralite + Soul Core data, NAT plain core |
| PICTA EXPERIMENT | Bottled 1.0.4 | none | off | Picta data + SH2 Data copy, Extender 1.4.3 on, KiLoader off |

PICTA is the August fork of the non-PBR CS profile, 171 lines behind PBR. Fine for a sky test.

### Facts that decide the layout
- **Effects 11** reads the preset from `Data\enbseries` when `Data\enbseries.ini` + `Data\enbseries`
  exist (Picta's Data mod), sniffs the KIEFX header there, and applies the `.fx.ini` values from the
  Data copy (`Effect::Load`). Bottled's own `SettingsPatches.json` then force-disables the postpass
  AA / sharpen / blur / border / vignette switches of any preset.
- **The Extender** (1.6.0, disassembled) compiles `<game root>\enbseries\<slot file>` only, resolves
  the KiSU/UI includes from there, and reads its `[EXTENDER]` settings from the root
  `enbfxcompiler.ini`. Its compile core builds a `<root fx>.ini` path (uppercased section), so if
  compile-time options are read at all, they come from a **root** `.fx.ini`. Three readers of the
  binary disagree on whether they are read; the launch decides.
- **Effects 11 applies nothing until the preset compiles** (`IsPresetLoaded` gates the sky
  gradient, the scattering, the grading). Today on PICTA it logs "Encrypted preset: requires
  KiLoader and ENB Extender", so everything the August ledger recorded is currently inert.
- **`ENBHelperSE.dll`** demands the ENB loading point unconditionally; KiLoader refuses it with a
  dialog when no ENB is present. The Extender 1.6.0 asks for it only when ENB exists, otherwise logs
  "ENB unavailable" and initialises standalone. 1.6.0 dropped the 15 static d3d11 imports 1.4.3 had.
- **KiLoader** loads its plugins synchronously during SKSE plugin load; Effects 11 compiles later,
  at render-target creation. "Reload Shaders" re-runs the bridge. KiLoader keeps its ENB satellite
  file inside the root `enbseries` (the SH2 root mod ships it, byte-identical); without it KiLoader
  installs one and quits the game for a restart.
- Logs: `C:\Users\User\AppData\Local\KiLoader\SkyrimSE\Logs\` (`KiLoader.log`, `KiENBExtender.log`).
- **Sky**: `[SKYSCATTERING]` is registered with every key Picta uses; every gradient band is
  multiplied by `GradientTopIntensity × GradientIntensity` (and Horizon/Middle likewise); air glow
  multiplies that gradient. `[PROCEDURALSUN]` is **not** a registered category in 1.0.4: Picta's
  sun keys and the August sun repairs are dead text; the sun is Bottled's own Procedural Sun feature
  in `SettingsUser.json`.
- **Weather lists**: IDs masked to the low 24 bits on read and at lookup. Any section starting with
  `WEATHER` loads (no 001–499 range); a duplicated section name is silently ignored (first wins); an
  ID listed again under a new name is re-mapped (last wins); a `WeatherIDs` line over 1023 characters
  is cut mid-token. `_worldspaceweatherlist.ini` is never read. `_locationweather.ini` is: sections
  are worldspace IDs, entries `location = fakeWeatherID`, exact match on the cell's own location,
  both current and previous weather replaced (no transitions), gated on `[WEATHER]
  EnableLocationWeather`. Lists are re-read by "Reload Shaders". Masking frees full plugins from the
  load index; **ESL-flagged plugins keep their light slot in the masked bits** (six light plugins
  define weathers here: Helios, Supernova, ksws03, Lux Forgotten City, Dragon Tweaks, AP Sev Cut).
- **Bottled's Upscaling feature**: DLSS through Streamline 2.10.3 loaded from
  `Data\Shaders\Upscaling\Streamline` inside its device hook; FSR3 FG through
  `amd_fidelityfx_loader_dx12.dll` + `amd_fidelityfx_framegeneration_dx12.dll` on its own D3D12
  device and swap chain, only when windowed, `frameGenerationMode` on, refresh ≥ 120 Hz (or
  `frameGenerationForceEnable`). UI handed to FidelityFX as a premultiplied texture, no HUD-less
  colour. Reflex forced off under FG. Reverse Z honoured. A feature whose
  `Shaders\Features\<name>.ini` is missing never loads, independent of the JSON. Blacklist = 11
  `Data/SKSE/Plugins/*.dll` names, nothing in the game root. `qualityMode` 0 = DLAA, 1 = Quality.
- **What the exe imports**: `dxgi`, `d3d11`, `DINPUT8`, `WINHTTP`, `WINMM`, `d3dx9_42`. Not
  `version.dll`. ReShade's `dxgi.dll`, `skse64_loader.exe`, `SkyrimSELauncher.exe` and the Creation
  Kit do import `version.dll`.
- **Root Builder** v5.0.5, copy mode, active profile's enabled mods only, plus `overwrite\Root`
  appended to **every** build; on a clean exit it syncs changed or new root files back (mod or
  `overwrite\Root`) and clears; on a crash nothing clears and the next build merges. A zero-filled
  `BuildData.json` from 09-01 proves the crash path is real on this machine.

### The pieces on disk
| Piece | State |
|---|---|
| Extender 1.6.0 archive | `D:\1. MOD STUFF\1. SKYRIM FILES\ENB Extender and Helper Legacy (1.6.629-1.6.1179) 99406 1.6.0 …7z` (the build for game 1.6.1170; `KiENBExtender.dll` exports the three `ENBExt_` functions, verified). |
| `KiLoader for Skyrim` | 1.2.0, off in the CS profiles. Config lists 1.6.1170. |
| SH2 core 1.10 | Data copy on in PICTA; Root Builder copy (`Silent Horizons 2 - Shader Core`, incl. the ENB satellite file) off everywhere. |
| Picta ENB data | 185 live files with the 23 August repairs; shipped per-weather values in `_backups\2026-08-25 - pre-regrade` (125 files). Its `enbpresetoverlays.ini` is 206 zero bytes: a crash artefact, harmless to E11, to be removed. |
| DynamicShaderFrameGen | live on PBR; ships Streamline 2.13 + FidelityFX DLLs in the same `Data\Shaders\Upscaling\` paths Bottled loads from. |
| Bottled Upscaling runtime | not in the Bottled mod; parked (20 files) in `_backups\2026-09-30 - Bottled 1.0.4 Upscaling parked`, plus the `Disable at Boot` lock. |
| NR dll | Build 13 copy and the live DSFG copy = the fork's required original signed 310.8 (SHA-256 verified, signature Valid). |
| Game-root proxies | ReShade `dxgi.dll` (PBR), xSHADOWMANx `DINPUT8.dll`, Engine Fixes `d3dx9_42.dll`. No `winmm.dll` anywhere. |
| Display | borderless 4K, 165 Hz per the DSFG log (one probe read 73 Hz remotely; confirm before assuming FG runs). |
| dlss-unlocked | NR-v0.9.32 (2026-09-26). Ships `OptiScaler.ini` with `External=true` and `AmpereMfgUnlock=true` (both must go false), a patched NR dll and an obsolete forwarder (both replaced), and **no** `nvngx_dlss.dll`. |

### The shared surfaces (not one, five)
1. `overwrite\SKSE\Plugins\CommunityShaders\SettingsUser.json` — the whole file, saved back by
   whichever profile saved last.
2. `overwrite\Root` — every new game-root file a session leaves is synced there and deployed into
   every profile's root afterwards.
3. The game root itself after an abnormal exit (Root Builder clears only on a clean exit).
4. Mods enabled in both profiles: `[NoDelete] Bottled Shaders`, `ENB Extender and Helper` 1.4.3.
5. `overwrite\ShaderCache` (benign, content-addressed).

The plan removes 1 and 4 for the parts that matter (a PBR-only upscaling runtime mod, a PICTA-only
Extender mod) and adds hygiene for 2 and 3.

---

## 2. Decisions before anything is written

Status after the user's answers on 2026-09-30 (evening):

1. **DECIDED: the Picta lane is a fresh copy of the PBR profile.** `profiles\DEEZ CS NUTZ - PICTA`
   was created 2026-09-30 16:15 by copying `DEEZ CS NUTZ - PBR` (all four list files, the three
   game inis, archives/initweaks/lockedorder/settings, the CRDW folder, the 14 live saves; the
   `.bak` files and the 88 save backups were not copied). The four Picta mods in it are still
   unticked and the Astralite/Soul Core lane is still ticked: the lane transplant (A1-A3) applies
   to this profile. `PICTA EXPERIMENT` is retired as a base: it is 173 modlist lines and 56 plugin
   lines behind PBR (no Everdamned, Isekai, Vibrant Weapons, MFO, the 09-24/25/30 batches; different
   mod order). Merge into PBR later, as before.
2. **DECIDED 2026-10-01:** XeFG at 2x first; native DLSS-G on the 5090 later (second
   Streamline runtime, untested).
3. **DECIDED 2026-10-01 ("lets go more fps"): DLSS Quality from the first upscaled launch.** Superseded text: DLAA first, Quality later as the fps lever (NR runs before the
   upscale, on the render-size image, by the fork's default).
4. **DECIDED: Picta as SHIPPED, nothing from August.** Consequences (verified 2026-09-30 evening):
   - `[NoDelete] Picta ENB - Data` has 141 August-edited files (of the 180 the shipped archive
     carries), plus 1,133 backups/notes: it is NOT reused. A new Data mod is built from the
     shipped ENB 1.0.1 archive (root layout `enbseries.ini` + `enbseries\`, 220 files: the
     `KreatE\` preset-manager folder and `enblocal.ini` are ENB-only and stay out). E11 reads
     Data, so the archive's root layout is placed under `Data\` as `enbseries.ini` + `enbseries\`.
     The base ini goes in as shipped (its [SKY] and cloud/volumetric values that August called
     placeholders included: user decision; dial in the editor after an in-game reading).
   - `[NoDelete] Picta - Weathers of Aurbis` holds an August-edited esm (102 of 218 Picta WTHR
     records changed by cloud-alpha 08-25 / curtain-raise 08-26) and esp (4 of 4): NOT reused. New
     mod from the shipped Plugins 1.0.1 archive: the esm, the esp, the `.ini` only (its KiLoader
     AELAS settings, EVLaS.cfg and ParticleWind.ini are ENB-side and stay out).
   - `houseCARL - Authoria - Picta over NAT` (24 vanilla WTHR + 2 aurora GMST forwarded above NAT)
     is CLEAN: its bodies equal the shipped esm's (shipped == August for all 24), and the esp is
     byte-identical to its own pre-curtain-raise backup. Reused as is.
   - `[NoDelete] Picta - Assets 4K` = the archived 4K pack byte for byte EXCEPT `meshes\sky\clouds.nif`
     (August 27 "feather" edit): the shipped mesh is restored from the freshly downloaded archive
     (939 MB, size matches Nexus). The archive itself carries the five Cloudy_Windy 11-15
     placeholders (131,220 bytes each, same CRC as the unused 16-20 slots), so the friend's five 2K
     originals are still needed: that is an archive defect, not an August change.
   - A4 becomes "nothing to restore": no key-level surgery, no repairs kept. The sky model still
     says the shipped pair lands blue; dials only after an in-game reading.
5. **DECIDED: shader core stays 1.10.**
6. **DECIDED: accept Bottled as shipped.** Verified: Bottled 1.0.4 has NOTHING Picta-specific
   (no "Picta"/"Silent Horizons" string in the DLL, no json/ini/hlsl mention, nothing in the live
   source). Its only preset shaping is the generic `SettingsPatches.json`: on the postpass it hides
   and force-disables the SH2 groups AA (SMAA/FXAA), KiSharp, Blur Suite, KiGrain, CinBorders,
   Vignette; on the lens the chromatic aberration; on enbeffect letterbox, sharpening, grain, lens
   distortion, vignette, clarity. So Picta's AA and sharpening are off under Bottled (AA comes from
   DLAA/DLSS in workstream B); the json is not edited.
7. **DECIDED 2026-10-01: both held back ("go with shipped fixes from bottled first"); revisit after A1.** Background: the friend's two changes that alter Picta's OWN Tamriel skies,
   not just uncovered worldspaces: (a) `Picta - Storm Rain Cloud Layer Fix.esp`, one vanilla WTHR
   (SkyrimStormRain): the zenith-cap cloud layer counter-scrolls against three layers drawing the
   same texture ("two overlapping skies"), his fix flips the layer's speed sign; (b) inside
   `Picta - Realm Weathers.esp`, eight shared vanilla weathers byte-patched (two cloud layers
   disabled = his "line cloud", plus others). Recommendation: take (a) after A1 is green; hold (b)
   until Picta is seen on Bottled (tuned on real ENB).
8. **DECIDED 2026-10-01 ("just do the logical thing"): interior-fog remover deactivated in the Picta profile now; the Bruma plugin stays on until the friend's Bruma patch is installed.** Background: the two unticks in the PICTA profile only: the Bruma
   Universal Weather Compatibility plugin (8 REGN overrides that push Bruma's regions back to
   vanilla weather IDs and beat the friend's Bruma patch when loaded later) and
   `Authoria - Patch - Remove Interior Fog - Lux.esp` (20 Lux lighting templates with fog zeroed,
   authored for the NAT/Astralite lane; Picta's interior profiles expect that fog and go
   pitch-black without it). Both still ticked in the new profile.

---

## 3. Workstream A — Picta on Bottled (BUILT 2026-10-01 in `DEEZ CS NUTZ - PICTA`; the "As built" block at the top governs; the text below is the pre-build plan, kept for its evidence)

Goal of A1: the four SH2 effects compile through the Extender, Picta's runtime values attach, the
UI-variable counts are sane, the sky is blue and not white. Nothing else is judged.

### A0. Backups (mine)
PICTA `modlist.txt` → `.bak-picta-bridge-20260930`; full copy of `[NoDelete] Picta ENB - Data` to
`_backups\2026-09-30 - Picta pre-bridge`; `SettingsUser.json` copy. MO2 and the game closed,
checked immediately before each write.

### A1. Extender 1.6.0, PICTA only (mine)
- New mod `Authoria - ENB Extender 1.6.0 - KiENBExtender only`: `KiLoader\Plugins\KiENBExtender.dll`
  from the Legacy 1.6.0 archive (export table verified), **without** `ENBHelperSE.dll`. `meta.ini`
  mod id 99406, version 1.6.0, note on the omission. Enabled in PICTA only.
- `ENB Extender and Helper` 1.4.3 → **disabled in PICTA** (MO2 cannot hide its helper DLL from a
  lower mod; its Extender build has 15 ENB imports that fail without ENB). It stays as it is in PBR.
- After the write: the virtual `Data\KiLoader\Plugins` must contain exactly one file, the 1.6.0 DLL.

### A2. KiLoader on, PICTA only (mine)
- `+KiLoader for Skyrim`. `ENB Worldspace Weatherlists` stays off (needs ENB; unread by E11).
  `ENB Binary Files` stays off. `Enhanced Volumetric Lighting and Shadows` stays off (on Bottled's
  incompatible list). KiLoader must never run in a profile whose root carries a `version.dll`
  proxy (it imports it); B uses `winmm.dll`, so this never arises.

### A3. The core in the game root, and Picta's inis beside it (mine)
- `+Silent Horizons 2 - Shader Core` (the Root Builder copy, 1.10, 2.8 MB): the four encrypted
  `.fx`, the KiSU and UI includes, `enbfxcompiler.ini`, and the ENB satellite file (keep it).
- Keep `+[NoDelete] Silent Horizons 2 - Data` (E11 must see the encrypted `enbeffect.fx` in Data).
- New mod `Authoria - Picta ENB - Root twin`, above the core mod: `Root\enbseries.ini` +
  `Root\enbseries\enb{effect,bloom,adaptation,effectpostpass}.fx.ini` (Picta's four) +
  `Root\enbseries\enbfxcompiler.ini` = SH2's three keys plus `EnableShaderGrafting=false`,
  `EnableExternalShaderCache=false`, `EnableFallthroughShaderCaching=false` (first test: an
  un-stripped blob, no `enbcache` folder). A one-line script re-syncs the four inis from the Data
  copy before every launch (E11 saves only the Data copy).
- Remove the zero-filled `enbpresetoverlays.ini` from the Data mod (backup kept).

### A4. The sky: Picta as shipped, key by key (mine)
Model (the refuters' corrected one, `r1_skymodel.py`; pre-tonemap radiance, 1 = white; the SH2
tonemapper is encrypted and unmodelled):

| Grade | Scattering | Zenith | Horizon away | Horizon toward sun |
|---|---|---|---|---|
| **Picta shipped** (0.025 × 0.075) | **Picta shipped** (glow 1000, int 10) | 0.43–0.85 blue | 2.2–4.1 | 3.5–6.3 |
| August regrade (1.0 × 2.0) | Picta shipped | 200–740 (white) | 120–410 | 180–600 |
| Picta shipped | cut to Soul magnitudes | 0.001 (black) | 0.01 | 0.02 |
| August regrade | cut to Soul magnitudes | 0.5–1.0 flat | 0.5–0.9 | 0.5–0.9 |
| Soul Core reference | Soul Core | 0.69–1.35 | 0.56–1.1 | 0.64–1.2 |

So: **key-level restore of the shipped values** in the 117 routed per-weather files and the base
ini, keeping every repair that is not a gradient compensation:

| Key set | Action |
|---|---|
| `[SKY]` `GradientIntensity*`, `GradientTopIntensity*`, `GradientHorizonIntensity*`, `GradientMiddleIntensity*`, `GradientDesaturation*` (six exterior periods) | restore shipped (Repairs 2 and 14 out) |
| `[SKY]` `CloudsIntensity` Dawn/Dusk/Night, `[ENVIRONMENT]` `FogColorMultiplier` Dawn/Dusk/Night | restore shipped (Repairs 12, 13b out: they compensated the regrade) |
| `[BLOOM]` Amount cap 0.5 | restore shipped 1.0 with the gradient; first dial if the sunward band blooms |
| `[ENVIRONMENT]` `FogAmountMultiplier` cap 3.0 (Repair 13a) | keep |
| `[ENVIRONMENT]` 0.92 direct-light dim (Repair 4b) | keep for A1 (scene, not dome); decision 8 |
| base `enbseries.ini` | keep the live file (adaptation off, volumetric rays off, `DisableWrongSkyMath` false, base cloud and fog placeholder fixes); set only its `[SKY]` gradient keys to the shipped structure (0.025 / 0.075 / 0.5); never copy the backup base ini back |
| `[SKYSCATTERING]` everywhere | untouched |
| `[PROCEDURALSUN]` | dead under Bottled; leave; the sun is `SettingsUser.json` Procedural Sun (disk radius 0.00925, disk 6.0, halo 0.4) |
| the 14 non-Picta stub files (interiors, main-quest, `Base_Weather.ini`) | leave; not Picta's authoring |

Byte-diffed, colour filters verified identical, backups first. Dials only after an in-game
reading: `AirGlowIntensity` 1000 → 300–500 for the whole dome; `Intensity` 10 → ~4 and
`SunGlowIntensity` 1.0 → 0.5 for the sunward band (Intensity also lights the cloud paintings, so
never Soul-Core-sized). Night is modelled separately before A1 (air glow 1000 at range 0.15 on the
0.02 × 0.0625 night gradient).

### A5. Settings (mine)
`SettingsUser.json` unchanged for A1. No plugin changes.

### A6. Launch A1 — yours, then mine
Yours: activate `DEEZ CS NUTZ - PICTA`, launch (see the "As built" launch steps). If the game closes itself within seconds, that is
KiLoader installing its satellite; launch again. Load an exterior save, noon if you can, stand a
minute, open the Effects 11 editor once (its Shader Parameters panel), quit.

Mine, before any relaunch:
- `KiLoader.log`: "Initialized plugin 'KiENBExtender.dll' (ENB Extender) [1.6.0]", only the
  Default and SKSE loading points, no "Needs [ENB] loading point", no dialog.
- `KiENBExtender.log`: "[WARNING] ENB unavailable" (expected), "Running standalone initialization",
  "Successfully initialized"; no "Unable to open/read file" (= root not deployed); which ini it
  parsed (decides the root-twin question).
- `CommunityShaders.log`: four "[EFFECTS11] Loaded encrypted FX file through ENB Extender:", four
  "Successfully applied effect", "[EFFECTS11] Preset loaded from '…Data\enbseries'", the
  `[WeatherManager]` file list; and the **"Loaded N UI variables for effect"** counts against
  Picta's key counts (enbeffect 546, postpass 1174, bloom 433, adaptation 72). Small N = the
  compile-time options did not survive. The "Recovered groups" line is optional, not a marker.
- Failure strings, exactly: "Encrypted preset: requires KiLoader and ENB Extender",
  "ENB Extender compile failed", "Failed to create effect from ENB Extender output",
  "has no ENB Extender compile slot", surfacing as "[EFFECTS11] No preset in use: … failed to load".
- The sky from your clip: zenith, horizon away, horizon toward the sun, noon and sunset.

### A7. What each outcome means
| Result | Meaning | Next |
|---|---|---|
| "requires KiLoader and ENB Extender" | Extender not in the process | KiLoader.log plugin list; the 1.4.3 mod still on |
| "Unable to open/read file" | root not deployed | Root Builder log; the core mod's enabled state |
| loaded, UI counts near the key counts | full fidelity | judge the sky |
| loaded, UI counts small | compile-time options lost | Picta on SH2 defaults; decide whether that look is acceptable |
| sky white | scattering hot | the A4 dials, air glow first |
| sky black by day | gradient restore incomplete or preset not compiled | check both logs |
| sunward horizon blown, zenith fine | expected from the model | Intensity / SunGlow dial |

### A8. Rollback (mine)
Flip the PICTA lines back; restore the Picta folder from the pre-bridge backup. PBR untouched.

---

## 4. Workstream B — DLSS 5 NR via dlss-unlocked (PBR)

Two launches: **B0** proves Bottled's own upscaling and frame generation alone (the article's
precondition, never met here); **B1** adds the proxy.

### B0. Bottled's own DLSS + FSR3 FG, PBR only (mine, then yours)
1. `-DynamicShaderFrameGen - FSR3 FG and DLSS5 NR` in PBR (folder kept). Its Streamline 2.13 and
   FidelityFX DLLs sit in the paths Bottled loads from; they must not be in the VFS.
2. New mod `Bottled - Upscaling runtime (PBR only)` = the 20 parked files, byte-identical, placed
   directly above `[NoDelete] Bottled Shaders`, `+` in PBR, `-` in PICTA. **Never back into the
   shared Bottled folder.** With its `Shaders\Features\Upscaling.ini` absent from PICTA, the feature
   cannot load there whatever the JSON says.
3. Only then `Disable at Boot → Upscaling: false` in `SettingsUser.json`.
4. Launch B0 (yours). Mine: `CommunityShaders.log` shows `Loading Feature: 'Upscaling'`,
   "[Streamline] Interposer loaded", "sl.interposer.dll version: 2.10.3.0", "DLSS … available",
   "[Frame Generation] Frame Generation enabled, using D3D12 proxy", no "Invalid settings for
   Upscaling"; then set inside the block the build wrote: DLSS, **Quality** (decision of 2026-10-01; `qualityMode` 1), FG on. PICTA's next log
   must show "Upscaling.ini failed to load, feature disabled".

### B1. The proxy (mine)
Downloads (yours, one file): `dlss-unlocked-standalone-NR-v0.9.32.zip` from the ShyVortex
GitHub releases page into `D:\1. MOD STUFF\1. SKYRIM FILES\tools and frameworks\`. Standalone zip,
not the installer.

Root Builder mod `Authoria - dlss-unlocked 0.9.32 (OptiScaler NR)`, PBR only:
```
Root\winmm.dll               <- the zip's dxgi.dll renamed
Root\OptiScaler.ini          <- written by me (below)
Root\nvngx_dlssnr.dll        <- our genuine signed 310.8 copy (the zip's patched one and its forwarder are NOT used)
Root\OptiScaler\nvngx_dlss.dll   <- byte-identical copy of Bottled's DLSS core (54.8 MB), so the proxy finds it on the physical disk at attach
Root\OptiScaler\libxess_fg.dll, libxell.dll, libxess*.dll   <- the XeFG runtime from the zip
Root\Licenses\
```
Left out of the mod: `OptiScaler\streamline`, `dlssg_sm86`, `nvfp4`, `dlss-enabler-headless.dll`,
`dlssg_to_fsr3_amd_is_better.dll`, `nvsmooth30.dll` (unused by fsrfg→xefg on a 5090; ~400 MB of
copy per launch), `OptiScaler\plugins` (the 3x+ unlock), and the zip's `amd_fidelityfx_*.dll`
(so Bottled's own FidelityFX build is the one hooked; if the log shows the FG context failing,
adding them back is the A/B).

- **`winmm.dll`**: the exe imports it at process start, so the proxy is in the process before
  Bottled loads Streamline (the proxy only wraps an already-loaded NGX module instead of
  re-pointing it). `version.dll` would load only as ReShade's dependency and also into the SKSE
  loader. `winhttp.dll` and `dinput8.dll` are taken.

`OptiScaler.ini`:
```
[ProcessFilter] TargetProcessName=SkyrimSE.exe      ; else it also initialises inside skse64_loader.exe / the launcher / CK
[Upscalers]     Dx11Upscaler=dlss_12                ; DLSS on a background D3D12 device; native 'dlss' has no NR path
[FrameGen]      Enabled=true  FGInput=fsrfg  FGOutput=xefg  DrawUIOverFG=true  External=false
[DLSSG]         AmpereMfgUnlock=false               ; either of these two true = FG forced off and Streamline unhooked
[XeFG]          InterpolationCount=1
[DlssNr]        Enabled=true  RunBeforeSR=true  FinishedPicture=false  Passes=1  WorkingScale=1.0
                Intensity=2.0  Style=2  LocalTone=0.75  LocalStructure=0.9  SkinStructure=1.03  AutoMask=true  Preset=0
[Plugins]       LoadAsiPlugins=false
[Menu]          Insert (default); FG shortcut default End, rebind if it collides
[Log]           LogToFile=true  LogLevel=2  LogFileName=C:\1. AUTHORIA\logs\OptiScaler.log   ; outside the game root, so it never lands in overwrite\Root
```
`[FrameGen] DisableUI` stays at auto (never true). `[Hotfix] ManualInputPolling=true` only if the
overlay opens but ignores input. ReShade stays on; `frameGenerationForceEnable=1` in the
Upscaling block is optional insurance if the refresh probe is in doubt.

### B2. Launch B1 — yours, then mine
Yours: PBR, launch, main menu, a save, one minute, Insert once, quit.

Mine, before any relaunch: `C:\1. AUTHORIA\logs\OptiScaler.log` must show "OptiScaler working as
winmm.dll, system dll loaded", "nvngx_dlss.dll found at …" and "Enabling DLSS" (**not** "nvngx_dlss
not found, disabling DLSS" = silent FSR 2.2 without NR), no "External frame generation: leaving …",
"nvngx call: …, returning this dll!", "Captured D3D12 device from command queue", "Creating new
DLSS w/Dx12 feature" + "Render Resolution", "DLSS-NR: feature created at WxH through NVIDIA NGX
driver", "DLSS-NR: the D3D11 bridge reached the hand-off (upscale ok: true, enabled: true)", "UiResource
found", "XeFG swapchain created", "Max supported interpolations", "SetEnabled: true, result:
XEFG_SWAPCHAIN_RESULT_SUCCESS (0)". `CommunityShaders.log` as in B0 with no "[FidelityFX] Failed to
create swap chain context!" or "Failed to configure UI composition!". `ReShade.log`: "Recreated
runtime environment" on a CreateSwapChainForHwnd. Then `overwrite\Root` for anything the session
left (must be nothing), and the game root for the 12 vanilla files only.

### B3. What each outcome means
| Symptom | Meaning | Next |
|---|---|---|
| no OptiScaler.log | winmm.dll not deployed | Root Builder log |
| "disabling DLSS" | DLSS core not found on disk | the `Root\OptiScaler\nvngx_dlss.dll` copy; `[Libraries] NvngxDlssPath` as the alternative |
| "External frame generation" | the two flags still true | fix the ini |
| DLSS runs, no "DLSS-NR: feature created" | dll or driver | hash again, `LogLevel=1` |
| FG runs but no "XeFG swapchain created" | FSR-FG input not hooked | `FGOutput=fsrfg` control, then the FFX DLL A/B |
| menus invisible or doubled | UI path | `DrawUIOverFG`, `UIPremultipliedAlpha`, `frameGenerationAllowInMenus` A/B |
| ReShade effects gone | expected for depth effects on the D3D12 swap chain | the wiki's `LoadReshade` route as the A/B |
| TDR / freeze at load | same class as 09-25 | NR off → ReShade off → FG off |

### B4. Rollback (mine)
`+DynamicShaderFrameGen`, `-` the two new mods, `Disable at Boot → Upscaling: true`.

---

## 5. Workstream C — the friend's package

Package `Picta - Authoria Fixes - 2026-09-30.zip`: 160 files, manifest verified clean, extracted
read-only into my scratchpad. His list is a sibling of this one, on **real ENB**, and his Picta
lane has been off since 09-13; the package is his last verified state. The tuned profiles carry
Picta's own values (his redistribution caveat).

### 5.1 What applies
| Part | Verdict here |
|---|---|
| 5 cloud textures (`Cloudy_Windy` 11–15) | **Yes.** Our 4K pack has the same five magenta placeholders. Small override mod above the 4K pack. |
| 28 patches | 15 have their masters active here (Bruma, Wyrmstooth, Coldharbour, Soul Cairn Climate Fix, Apocrypha, Siege at Icemoth, LOTD, Sovngarde Volumetric Restore, Unslaad, Olenveld ring fix, Storm Rain Cloud Layer Fix, plus Glenmoril and Frozen Heart which he keeps disabled); a houseCARL missing-master sweep confirms each before it goes in. 12 are for mods we do not run. |
| `Picta - Realm Weathers.esp` (full) | rebuild: two masters absent (Drez'kth'ar, Extended Cut). Its new weather IDs 800/802/803/810 are free in our masked census. Stays full. |
| `Picta - Water for ENB LOD Patch.esp` | not needed: on our order the FWMF tail wins every worldspace Picta touches (checked). |
| `Worldspace Climate Restore - FWMF.esp` | our own FWMF master patch drops Vigilant's climate link too; nothing may load below it, so the field is forwarded inside our patch instead. |
| `enbeffect.fx.ini` dither off | yes, as-is (a dither-stage artefact he measured on dark realm skies). |
| his 11 routing lists, 18 realm profiles, 6 fallback profiles | yes, after the Effects 11 treatment (5.3). |
| `enblocal.ini`, `_worldspaceweatherlist.ini`, `Picta - Weatherlists\*.ini` | inert under Effects 11; not installed. |
| profile snapshot, tools, 34 notes | reference. |

### 5.2 Profile-state fixes he needed (both live here; decision 8)
Untick `Beyond Skyrim Bruma - Universal Weather Compatibility.esp` (its vanilla-ID region
rewrites fight the Bruma patch; the Snowy Holds seasonal patch is the other REGN contender, checked
with houseCARL) and `Authoria - Patch - Remove Interior Fog - Lux.esp` (zeroes fog on 20 Lux
templates; made Picta interiors pitch-black) in the PICTA lane.

### 5.3 The ENB side under Effects 11
- **Lists: merge, never replace.** His 502-section global list dropped over ours would remove six
  of our live mappings and re-map five (the four main-quest weathers and the heavy snow storm to a
  Wheels-of-Lull interior recipe). Keep our 90 sections; append his realm entries under new unique
  names; every `WeatherIDs` line under 1023 characters; drop the obsolete "regenerate if the ESM
  moves" header; drop his 8 dead entries; drop the 19 IDs for mods we lack; re-derive any ID that
  comes from an ESL-flagged plugin from our own runtime FormID.
- **His patches that only retarget regions and climates to Picta natives need no list edits at
  all** (every native they roll is already mapped). That covers Bruma, Wyrmstooth, Coldharbour,
  Soul Cairn, Apocrypha, Icemoth, LOTD, Unslaad, Glenmoril, Frozen Heart.
- **The 34 per-worldspace conflicts**: Solstheim's remap of Rift and Snow Tundra natives (20 IDs;
  those fire in Tamriel too, so the Tamriel mapping stays and Solstheim keeps Tamriel's grades
  unless a later phase duplicates records for it); realm overrides of shared natives (9 IDs: Soul
  Cairn, Apocrypha, Coldharbour, Deadlands, Desert, Whitehorn, Baelmore) go through
  `_locationweather.ini` with fake IDs from a free range, one look per realm, no transitions, in
  cells that carry a location; tested first with one Bruma line to learn whether the engine falls
  back to the worldspace's own location (readers of the exe disagree) — the editor's weather row
  in a wilderness cell decides; main-quest routing in his storm list dropped.
- **His 24 profiles** are Picta natives tuned on real ENB. Re-apply his delta against the stock
  native onto **our** copy of that native (which, after A4, is the shipped one plus the kept
  repairs), into `Z_Custom_Realms` in our Data mod. Their `[SKYSCATTERING]` blocks stay as he
  tuned them, same regime as A4.

### 5.4 His notes that change how we work
Keep Picta unchanged (restore what it dropped, never re-grade what it authored; scope counts);
masked IDs collide across plugins; the modded-realm ring bug is cloud layers on Picta's panorama
meshes (proven by an all-off bisect, not the upper dome, not sky statics); never ESL-flag Realm
Weathers; his user parked five items, do not reopen; DynDOLOD was regenerated with Picta active on
his side (a fact for the merge stage, not a step).

### 5.5 Intake steps, in order (mine, after A1 is green)
1. Textures. 2. The 13 usable patches (two disabled), one folder each, placed in the PICTA lane
above the output block after `Authoria - Picta over NAT.esp`, four profile files in lockstep,
houseCARL 0 missing / 0 late masters, the Bruma REGN winner check. 3. List merge + the Bruma
`_locationweather.ini` test. 4. Profiles via delta re-application. 5. Dither off. 6. The Vigilant
climate field in our FWMF patch + the two unticks (decision 8). 7. Realm Weathers rebuild
(decision 7 stays open). 8. Ledger section in `PICTA-EFFECTS11-REPAIRS.md`.

---

## 6. Order of launches, and who does what

| # | Profile | What changes | Proves |
|---|---|---|---|
| L0 | PBR | nothing new (owed Bottled 1.0.4 first launch) | settings migration; Soul Core's scattering now rendering; DSFG still fine |
| A1 | DEEZ CS NUTZ - PICTA | A1–A5 (built 2026-10-01) | the bridge compiles Picta; UI counts; the shipped sky under Bottled |
| B0 | PBR | DSFG off, PBR-only upscaling runtime, lock off | Bottled's own DLSS + FSR3 FG alone |
| B1 | PBR | the proxy mod | NR + XeFG 2x through the proxy |
| C1 | PICTA | 5.5 steps 1–5 | the friend's realms route and grade |
| M1 | PBR | Picta block into PBR | Picta + NR together |

**Before every profile switch, and after any crash, freeze or reboot (mine):** the game root must
hold only the 12 vanilla files; Root Builder's `BuildData.json` must not exist (if it does, the last
run did not clear: Root Builder's Clear tool from the MO2 menu is yours to click, game closed); and
`overwrite\Root` must carry nothing a proxy or the Extender created (`OptiScaler*`, `enbcache\`).

Every launch is yours; every log and file check is mine, before you relaunch.

---

## 7. Open unknowns (honest list)

- Whether Picta's compile-time shader options survive the Extender's API compile (the fidelity
  question; A1's UI counts decide).
- Whether the Extender reads a root `.fx.ini` (the twin covers both cases; `KiENBExtender.log`
  tells).
- Whether the engine falls back to the worldspace's location for `_locationweather.ini` (the
  Bruma test).
- ReShade's effects on the D3D12 swap chain under the proxy: documented nowhere; the `LoadReshade`
  route is the fallback.
- XeFG accepting Bottled's 10-bit SDR swap chain: a runtime check.
- The sky numbers are a pre-tonemap model; the SH2 tonemapper is encrypted. A1 corrects them.
- Two Streamline runtimes if DLSS-G output is ever chosen.

## 2026-10-12 - Bottled 1.0.7 -> 1.0.11, compile-burst trim, crash assessment

**Crash evidence (two nvgpucomp64.dll crashes, 10-08 and 10-11).** Both exception records are impossible for correct
hardware: 10-08 reports a WRITE access violation on `test al, al` (a register-only instruction that cannot write memory);
10-11 has the instruction pointer two bytes INSIDE a real instruction (`test rax, rax` at +0x4088B55, RIP at +0x4088B57, the
return address of the preceding `call r8`), and the computed operand address does not match the faulting address. On-disk
bytes of the driver DLL confirm both. All 25 suspect shader blobs (incl. the two giant Lighting permutations and forced
recompile variants) create cleanly on the RTX 5090 (hw_results.csv, HWPASS DONE); all 3112 blobs hash/WARP-valid. The
NVIDIA DXCache file is preallocated (zero tail only), not corrupt. Conclusion unchanged: CPU/memory instability
(14900K + 4x DDR5-6400 above IMC rating, BIOS 1801/microcode 0x12B, 14 distinct kernel bugcheck signatures since 09-13),
triggered by all-core shader-compile bursts. User declined BIOS/XMP steps (not confident) - hardware steps stay theirs.

**Done today (both PICTA and Preset Studio - same mod folders):**
- `[NoDelete] Bottled Shaders` 1.0.7 -> 1.0.11 (84 overwritten, 6 added, 3 removed; 7 hand-edited files kept; DLL 1.9.0.0
  dated 2026-10-10, 23,005,696 bytes). Backup `_backups\2026-10-12 - Bottled 1.0.7 pre-1.0.11`.
- `Bottled - Upscaling runtime 1.0.4` now holds the 1.0.11 Upscaling files (Streamline 2.14.1, DLSS 310.9.1; 7 of 20 changed);
  folder name kept, meta.ini says 1.0.11. Backup `_backups\2026-10-12 - Bottled Upscaling runtime 1.0.4 pre-1.0.11`.
- overwrite: SettingsDefault.json + ShaderCache moved aside (`.stale-bottled107-20261012`) -> full recompile on first launch.
- SettingsUser.json (`.bak-pre-bottled1011-20261012`): Compiler Threads 30 -> 16 (startup), Background Compiler Threads 8 -> 4
  (gameplay) to shrink the all-core burst; `Disable at Boot` += HiZOcclusion (new beta draw-call culler, default ON upstream;
  kept OFF until A/B'd). FG mode stays 0, DLSS Quality upscaling stays, ReShade stays, proxy stays OFF.
- Archive copied to `D:\1. MOD STUFF\1. SKYRIM FILES\`.

**Next launch checklist (user launches; I read logs):** BottledShaders.log -> version line, "Invalid settings for" lines
(Terrain Shadows block is 1.0.7-shaped and may be rejected -> edit inside the block 1.0.11 writes at quit), compile count/time,
Very slow entries; fps_logger3 capture; crash log folder. Offered user-side diagnostic (no BIOS): power plan Maximum processor
state 100 -> 99 (disables turbo; big fps cost; reversible) - if the crashes stop, hardware is confirmed. NVIDIA 616.56 -> 617.42
WHQL is also theirs.

**Addendum 2026-10-12 (user diagnosis: "almost certainly something else we did").** Timeline supports it: the nvgpucomp64 crash type
exists ONLY on 10-08 and 10-11 (20 earlier crash logs since August are game code / other DLLs); Bottled 1.0.7 arrived 10-06 with the
terrain-shadows "LOD shadow capture" (EnableLODShadow defaults TRUE in 1.0.7 source, author called it buggy and turned it off in
1.0.8); both crash logs show a capture 1-3 s before the crash (10-08: captures 1/2/3 at 04:55:09/19/27.8, crash 04:55:27; 10-11:
"LOD shadows: active" 15:02:50, capture 1 at 15:02:52.2, crash 15:02:53). The 1.0.11 DLL contains ZERO LOD-shadow strings - the
feature is gone, so the 1.0.11 update already removes this trigger. Landscape Seams stays ON (user pick); it is the next
candidate if 1.0.11 still crashes (the 10-08 crash followed a 15.9 s LANDSCAPE_SEAMS Lighting compile).

## 2026-10-12 (later) - Picta 1.0.1 -> 1.1.1 / 1.1.2, Nordic Winds patch, wind floor, ReShade toggle

**User decisions:** "wind floor should be maybe 12%"; "updates and such now please I want to lock this in before proceeding".

**Done (both PICTA and Preset Studio; other profiles carry the new folders disabled):**
- `[NoDelete] Picta - Weathers of Aurbis 1.1.1 (shipped)` (600 files: esm/esp/ini, meshes, textures, sounds, DynDOLOD config; left out as
  in the 1.0.1 build: KiLoader AELAS kfg, EVLaS.cfg, ParticleWind.ini). Placed BELOW `[NoDelete] Picta - Assets 4K` (4K textures keep
  winning; 449 meshes identical to the pack) and ABOVE `Picta Series - Improved Sky Meshes` (2021 mod). The pack's `meshes\sky\clouds.nif`
  updated to the 1.1.1 mesh (1.0.1 kept as `.shipped-101.bak-picta111-20261012`). 1.0.1 shipped folder kept, disabled.
- `[NoDelete] Picta ENB 1.1.2 - Data (shipped)` (221 files; enblocal.ini + KreatE left out as before). Generated `enbseries\_weatherlist.ini`
  from the shipped routing list: 34 sections / 40 weather IDs (the author's list has 44, 10 reference ini files not shipped and IDs not in
  the esm - listed in `enbseries\NOTES-weatherlist.txt`; left out exactly like the 1.0.1 build). Base ini changes vs 1.0.1: underwater
  shader on, animated stars on (+220 other lines). 1.0.1 Data folder kept, disabled. Root twin re-synced (5 files in sync; the sync tool
  now points at the 1.1.2 folder).
- `[NoDelete] Picta Aurbis - Nordic Winds - Patch 1.1.1 (shipped)`: ESL-flagged esp + SRD yaml; plugin right after `Nordic Winds.esp`
  (PICTA plugins 328 / loadorder 383 / group Audio - Core; Studio 321 / 381).
- **Picta 1.1.1 is a rebuild, not a tweak:** esm 704 -> 475 records, 461 old FormIDs gone, 53 reused for other records. Only three
  active plugins master Picta: its own esp (new), the Nordic patch (built for 1.1.1), and `Authoria - Patch - Wanderers Fair - Picta Climate`
  whose six Whiterun-tundra weathers were all gone -> rebuilt: the fair climate now carries the 1.1.1 Whiterun tundra region's 17-entry
  MASTER weather list (same weathers and chances Picta uses on the tundra); backup `.bak-picta101-20261012` beside it.
- Known-accepted (author's own 1.1.1 defects, left as shipped): the esp still references 21 weather IDs the esm no longer has (Soul Cairn
  climate/regions -> 1B0043/1B0045, the Dawnguard and Apocrypha uniques); those cells fall back to engine defaults until the author fixes it.
- Dynamic Wind `fMinWindStrength` 0.2 -> 0.12 (backup beside the ini). ReShade: `KeyEffects` = Scroll Lock (145) in the Picta-lane
  ReShade.ini so the user can A/B the UI smear in game (backup `.bak-toggle-20261012`).
- Archives filed in `D:\1. MOD STUFF\1. SKYRIM FILES\`. Profile file backups: `.bak-picta111-20261012` on modlist (6 profiles) and
  plugins/loadorder/plugingroups (PICTA, Studio).

**Launch checklist:** CommunityShaders.log -> Loaded encrypted FX lines, weather list load count (34), any 'missing file' warnings
beyond the 10 known; Tamriel sky under a MASTER weather (not the AP start forest); fair worldspace weather; Nordic Winds gusts;
Scroll Lock A/B for the UI smear.

## 2026-10-12 (evening) - carriage PBR wood fix, lush grass back, UI smear findings

**User decisions:** "grass, give me the lushhhhh grass"; carriage "a or b are fine" -> A built (quick override, B = PBR sources + PG rerun
folded into the later full tool run).

**Carriage (all carriages, not only the animated one).** Every carriage mesh in the 2026-08-28 PG output mixes PBR panels with two
non-PBR wood materials PG Patcher could not convert (no PBR source exists in the instance): `textures\architecture\farmhouse\woodwall01`
(Parallax type) and `textures\architecture\riften\riftencanalplanks01` (EnvMap type + dynamic cubemap). Under the PBR renderer those
panels read light and flat. New mod `Authoria - Carriage PBR Wood Fix` (12 meshes: the 8 Witcher-horse carriage nifs incl. `_shadow`, the
3 vanilla prisoner carriage nifs, the `_pgpatcher_dups\1` static) re-points those 33 shapes at a byte copy of the same mesh's
`PrisonerCarriage:2` material (Markarth PBR wood `mrkwood01` d/n/p/rmaos, SLSF2 PBR flag, PBR gloss), keeping each shape's own
vertex-colour flag; blocks replaced in place, block count/indices/strings/type table unchanged. Placed directly above
`Authoria - PG Output - PBR` (between it and `Authoria - Embers XD PBR Revert`) in all 8 modlists, enabled where the PBR output is
enabled (PICTA, Preset Studio, PBR), disabled elsewhere; backups `modlist.txt.bak-carriagefix-20261012`. Remove after any PG Patcher
rerun that has PBR farmhouse/Riften wood sources. The Snazzy Diverse Carriages statics (`GM_PrisonerCarriage01Static_A-D`) are
entirely non-PBR (consistent, untouched). Script: scratchpad `s15_carriage_fix.py` (+ `s15_carriage_scan.py`).

**Grass:** `SettingsUser.json` Grass Optimizations back to the 2026-09-24 lush values (MinDensity 1.0, MeshCostBias 0.0,
SimpleShadingPixelSize 4); backup `.bak-pre-lushgrass-20261012`.

**UI smear investigation (no fix yet):** the six ReShade screenshots of the day (`overwrite\Root\SkyrimSE 2026-10-12 *.png`) all show a
crisp compass, date and text at 1:1, so the smear is not a constant blur and is not in a still frame. ReShade WAS running on the 08:48
launch (ReShade.log: 6.7.3, preset compiled, no temporal effect in the preset). The Picta-lane `ReShade.ini` (Scroll Lock toggle) outranks
the `Reshade - DLL` copy (modlist 88 vs 90) but Root Builder's BuildData cache is corrupt (since 09-01) so the deployed copy cannot be
proven; the user reports Scroll Lock did nothing in RaceMenu. Driver profile (DRS dump of 617.42): no frame interpolation / Smooth Motion
setting in the base or Skyrim profile; VSync forced on, tear control off. Next step given to the user: take a ReShade screenshot
(Print Screen) WHILE the compass is moving and smearing; crisp file = out-of-frame (monitor overdrive / driver), smeared file = in-frame.

## 2026-10-12 (evening, 2) - smear is not in the frame; brightness lever; gate; grass season

- **UI smear:** the user pressed Print Screen while the compass was smearing. BOTH files of that instant are crisp at 1:1 -
  the game's own `ScreenShot330.png` (before ReShade) and ReShade's `SkyrimSE 2026-10-12 09-56-12_215.png` (after effects).
  The smear therefore happens AFTER the frame leaves the game: display path. Display = ASUS ROG XG32UCWG, 3840x2160 @ 164 Hz
  (plus the HYTE Y70 case screen); no streaming software running; driver profile: VSync forced on, tear control off, no frame
  interpolation. Prime suspects are the monitor's own motion settings (ELMB strobing = double images; OverDrive too high =
  ghost trails on bright HUD over dark). User-side checks given. No further in-game work on the smear until that is ruled out.
- **Brightness:** today's screenshots are not clipped (0% at >=240); what changed today is Post Processing ON ->
  `ppsettings.DisableVanillaTonemapping=1` finally applies (while PP was disabled at boot the key was inert), so the game's own
  HDR tone curve was removed. A/B for the next launch: `DisableVanillaTonemapping` 1 -> 0 with PP still ON
  (`SettingsUser.json`, backup `.bak-pre-vanillatonemap-20261012`). If that is the look the user had before, keep it.
- **Whiterun main gate:** the door is Glorious Doors of Skyrim's `wrdoormaingate01.nif` (plain env-map, `textures\architecture\hype\`,
  iron cubemap from Custom Cubemaps) - not PBR, PG never touched it; under the PBR renderer its reflection is the live cubemap, dull
  under grey weather. Replacer exists: GDOS SE PBR (Nexus 150727, needs PG rerun). Added to the skywim plan as P16.
- **Grass:** Witchy Wilderness (modular grass overhaul, Frolique) IS active (6 plugins) and in the 2026-08-21 grass cache; the game
  date is 17 Last Seed = SUMMER in `po3_SeasonsOfSkyrim.ini` (Season Type 5, Last Seed -> 3), so the SUMMER set (green) shows.
  The witchy mix (yellow/red tundra, dead grass + ferns + mushroom meadows) is the autumn/default set: from 1 Hearthfire. Picks:
  wait for autumn / permanent autumn (Season Type 4, changes trees and snow too) / leave.
- **Carriage replacer:** none fits a PBR list (WiZkiD Carriages is a plain retexture of the main carriage texture, which is already PBR
  here, and it does not touch the farmhouse/Riften panels). Real fix = PBR sources: Tomato's Riften PBR file (P17) + Vanaheimr
  Farmhouses II PBR or TomatoRim Farmhouses PBR (P18), then PG + TexGen rerun; the interim mesh fix stays until then.

## 2026-10-12 (evening, 3) - corrections: smear IS on screen, brightness = 1.0.11 light falloff, grass cache is from July

- **Smear - correction.** The user's DESKTOP capture (Snipping tool, RaceMenu, 10:27) shows the artifact: 'Freeze'/'Play'/'Sliders'
  rendered as two offset copies while neighbouring buttons are sharp; the game's own and ReShade's captures of 09:56 were crisp.
  So the monitor theory is dropped. Frame generation is OFF (no '[Frame Generation] ... D3D12 proxy' line; DLSS-G was removed in
  1.0.11; the Smooth-Motion detection line is absent). Next launch: 'Disable at Boot' Upscaling=true (whole feature off: no DLSS,
  no Streamline, no FSR) - backup `SettingsUser.json.bak-pre-upscaling-off-20261012`; `upscaleMethod` left at 3 for its return.
- **Brightness - cause found.** Bottled 1.0.11 REMOVED Inverse Square Lighting outright: the 10-11 (1.0.7) log shows
  'Loading Feature: InverseSquareLighting ... Installed hooks'; the 1.0.11 log has no such line, the Features ini is gone and the
  shader side is gone too (1.0.7 had INVERSE_SQUARE hooks in Lighting/Particle/RunGrass/Water/Effect .hlsl; 1.0.11 has none - only
  LightLimitFix per-light flags InverseSquare/Linear, set by hand in the light editor). Every point light therefore fell back to the
  vanilla-style falloff = lit scenes brighter and flatter than the look the user tuned on 1.0.7. Dropping the old ini back in is NOT
  valid (CPU hooks without shader support). The `DisableVanillaTonemapping` 1->0 guess did not help and was restored to 1.
  Settings blocks were NOT rejected by 1.0.11 (no 'Invalid settings' lines). Options given: roll Bottled back to 1.0.7 (+ Upscaling
  runtime 1.0.4 + pre-1.0.11 settings; all backed up under `_backups\2026-10-12 - *`) or compensate point-light intensity in the
  Picta E11 ini on 1.0.11.
- **Grass - the user was right.** `po3_SeasonsOfSkyrim.ini` seasons were NOT the issue. The Tamriel grass cache files are dated
  2026-07-18 (8089 of 8159 Summer cells; same for every season) = generated BEFORE Witchy Wilderness was installed (07-27); only
  Magpie Manor / Morskom cells (x6-11,y24-32; x19-21,y-3..1) were re-baked 08-19/20 with WW. The cache stores grass by FormID
  (e.g. FE3E8805 in the Whiterun file = light index 1000 on 07-18, which is now `SM_Astrid - OStim.esp`, a non-grass record) and
  NGIO runs `Only-load-from-cache = true`, so everywhere outside those two areas the game shows July's grass set. Also every plugin
  index moved since 08-21 (103 added, 15 removed; WW Resources FE441 -> FE468 by the script's count). FIX = full grass cache
  regeneration (5 passes, user presses Play; driver to prepare), AFTER all plugin changes and terrain patches of the tool run and
  BEFORE DynDOLOD. The 08-19 corrupt-file issue (98 files) gets cleaned by the same regen.
- **Carriage / gate picks:** gate = GDOS PBR (P16, user: yes). Carriage: Riften PBR file = same Tomato artwork, PBR flavour (safe);
  farmhouse walls today are BH's Rustic 4K + Riton parallax, NOT Vanaheimr, so any PBR farmhouse pack changes the farmhouse look -
  offered instead: carriage-only extraction of the one wall set (needs a download OK), or keep the mesh fix.

## 2026-10-12 (evening, 4) - A/B STATE ACTIVE: Picta lanes rolled to 1.0.1 + Upscaling off for ONE test launch

Both PICTA and Preset Studio lanes are temporarily on `[NoDelete] Picta - Weathers of Aurbis 1.0.1 (shipped)` + `[NoDelete] Picta ENB
1.0.1 - Data (shipped)`; the 1.1.1 weathers, the 1.1.2 ENB data and the Nordic Winds patch mod are disabled, the Nordic patch esp is
inactive (line kept), the fair patch esp and the 4K pack's clouds.nif are their 1.0.1 versions, the Root twin is re-synced to 1.0.1
(scratchpad `s15_picta_ab.py to101`; `to111` restores everything; backups `.bak-pictaab-20261012` / `.bak-picta111-ab` / `.shipped-111.bak-ab`).
`SettingsUser.json`: `Disable at Boot: Upscaling=true` (no DLSS/Streamline/FSR), `DisableVanillaTonemapping` back to 1.
Read the result as: sharp again -> the 1.0.11 upscaling path is the smear; normal brightness -> Picta 1.1.x is the brightness.
Then restore one change at a time. Timeline that drove this: 06:58 run (1.0.11 + Picta 1.0.1) = "okay"; 07:2x run (after the driver
update) = UI blur reported; 08:48 run (Picta 1.1.1/1.1.2) = "really bright" reported.

## 2026-10-12 (evening, 5) - A/B RESULT (10:59 launch, upscaling off + Picta 1.0.1): "brightness better, blurriness [gone] now, grass is fixed"

- Log confirms the state: 'Upscaling' disabled at boot, E11 loaded 107 weathers (= the 1.0.1 set). User report: brightness better,
  the blur gone, grass "fixed" (sharp, dense - the DLSS 4.5 path had been mushing thin grass, which is why it "looked vanilla"),
  "maybe too many flowers" (the July cache's flower-field grass type in that area; the planned cache rebuild replaces it with
  Witchy Wilderness' own mix; WW's installer has a lower-flower tundra option).
- Conclusions: BRIGHTNESS = the Picta 1.1.1/1.1.2 rework (1.0.1 restores the look). BLUR / mushy grass = Bottled 1.0.11's upscaling
  path (Streamline 2.14.1 + DLSS 310.9.1 "4.5" model); no DLSS = sharp. Decisions pending: keep upscaling off (native 4K, check fps)
  vs retry DLSS with another preset / FSR4; stay on Picta 1.0.1 vs tune 1.1.x darker.
- Parallel session (7b213a74, 11:02) replaced the carriage fix with `Authoria - Skyking Carriages - Over Outputs` and updated
  Animated Carriage 1.2.1 + routes (its own ledger: CARRIAGE-UPDATE-PLAN-20261012.md). `Authoria - Carriage PBR Wood Fix` is
  disabled in all 8 profiles (folder kept). Riften PBR 2K (P17) stays a user pick for Riften itself.

## 2026-10-12 (late) - UI SMEAR SOLVED: ReShade (the user's call from the start)

ReShade off for one launch -> "crisp ui - as I said, I fucking knew it was reshade". Cause inside the Picta-lane preset
(`Authoria - ReShade - Picta lane preset\Root\Northman II.ini`): FOUR depth-of-field techniques enabled at once (MagicDOF, MatsoDOF,
RingDOF, GP65CJ042DOF from DOF.fx; autofocus, 6 samples) plus GaussianBlur - the original Northman II preset in the other mod has NO
DOF at all. The HUD writes no depth, so autofocus DOF blurs it whenever the focus is near, and the stacked low-sample DOF draws
doubled copies; static text looked sharp only when the focus sat far. Fix: those entries removed from Techniques/TechniqueSorting
(backup `Northman II.ini.bak-noblur-20261012`); ReShade DLL mod back on in both lanes. "A tiny bit too dark" without ReShade =
the preset's grade missing; it returns with ReShade. Upscaling stays OFF and Picta stays 1.0.1 until the next steps.
Built in advance: `Authoria - Picta 1.1.2 - Darkened to 1.0.1` (scratchpad s15_picta_darken.py; 30 brightness keys scaled to the
1.0.1 average, see its README; registered DISABLED in all 8 modlists directly above the 1.1.2 Data mod). Next launches: (2) Picta
1.1.2 + the darkened override (`s15_picta_ab.py to111` then `s15_picta_darken.py --write --enable`), (3) DLSS 5 NR via the parked
dlss-unlocked proxy (config A), each with its own launch.

## 2026-10-12 (late, 2) - ReShade fix confirmed ("ui crisp - brightness okay"); lanes now on Picta 1.1.x + darkened override

- Both lanes switched back to Picta 1.1.1 weathers + 1.1.2 ENB data (`s15_picta_ab.py to111`), with
  `Authoria - Picta 1.1.2 - Darkened to 1.0.1` ENABLED directly above the 1.1.2 Data mod (PICTA line 3332, Studio 3332;
  disabled in PBR / DEEZ CS NUTZ / PICTA EXPERIMENT; absent from the three profiles that carry no Picta entries). 181 weather
  inis, 5334 values, 30 keys scaled to the 1.0.1 averages (README in the mod); root-level fx inis left alone (Root-twinned).
  Fair patch = 1.1.1 build, clouds.nif = 1.1.1, Root twin synced to 1.1.2, Nordic patch esp active. Upscaling still OFF,
  ReShade ON without the DOF/blur passes. This launch judges the darkening only.
- **Trap hit and repaired:** disabling the Nordic patch MOD for the 1.0.1 test made MO2 (opened by the user for the 12:4x launch)
  drop `Picta Aurbis - Nordic Winds - Patch.esp` from PICTA's plugins.txt, loadorder.txt AND plugingroups.txt. Restored to its
  recorded slot right after `Nordic Winds.esp` (plugins 328 active, loadorder 383, plugingroups 2947 Audio - Core; backups
  `.bak-nordicfix-20261012`). The A/B script now keeps that mod enabled in both states and only stars/unstars the esp.
  Other PICTA plugin-list changes seen in the same diff and NOT mine: `Rite of Arcana.esp` -> `DEST_ISL.esp` at the same slot,
  the carriage session's six Animated Carriage plugins and two Authoria carriage patches, VweaponsALL.esl moved up five lines.

## 2026-10-12 (late, 3) - darkening v1 failed ("now it's much brighter?"); v2 = the 1.0.1 GRADE on 1.1.2

Launch 13:23 (Picta 1.1.x + v1 override, upscaling off, ReShade without DOF): E11 loaded 34 weathers (the routed list), no new errors.
Why v1 failed: it only scaled lighting/sky/bloom-intensity keys. The full diff of the files E11 actually reads (each version's own
routed weather inis + root fx inis; scratchpad s16_picta_fulldiff.py / s16_grade_map.py) shows the brightness lives in the GRADE,
per weather (day medians 1.0.1 -> 1.1.2): UC2 tone curve Linear White 10 -> 30, Shoulder 0.45 -> 0.3, Linear Angle 0.5 -> 0.125,
Toe Strength 2.0 -> 1.25, Toe Numerator 0.05 -> 0.03; CG.HDR Gamma 1.3 -> 1.0, Gamma Correction 1.5 -> 1.8; Adaptation Lightness
Attenuation 10 -> 4, Darkness Attenuation 3.3 -> 2.0. CG.HDR Exposure (EV) is 1.2 in both (per weather); the root fx inis' +1.2 EV
only matters for unrouted weathers. The fx SHADER is the same file for both versions (Silent Horizons 2 Data), so 1.0.1's values
reproduce 1.0.1's response exactly.
v2 (`\_tools\picta-bridge\picta_darken_v2_grade.py --write`, layered on v1): Tonemap.*, CG.HDR.* (not Saturation), Adaptation.*,
Bloom Mixing/Blending (not colour) copied per weather from category-matched 1.0.1 weathers (clear/lightly cloudy/cloudy/overcast/
storm + rain/snow/fog flags; 2-12 donors each), root enbeffect/enbadaptation fx inis = 1.0.1 exterior medians, CG.AGIS and
Adaptation.Advanced = 1.0.1 root values. 6895 values in 107 files; colours, skies, clouds, weathers, fixes stay 1.1.2. v1 copy in
`_backups\2026-10-12 - Picta darkened v1 (before v2)`. sync_root_twin.py now mirrors the override when it is enabled in PICTA
(precedence overwrite > override > Data mod; backup .bak-override-20261012); twin re-synced (2 files).
The A/B / darkening / ReShade / slot-fix scripts were copied from the session scratchpads into `_tools\picta-bridge\`
(picta_ab_switch.py, picta_darken_v1_lighting.py, picta_darken_v2_grade.py, reshade_ab_switch.py, nordic_patch_slot_fix.py).
Next launch judges v2 only (upscaling still off, ReShade on without DOF/blur).

## 2026-10-12 (late, 4) - user: "still bright wtf go back" -> both lanes BACK ON PICTA 1.0.1

v2 (the 1.0.1 grade copied onto 1.1.2) was still too bright, so the remaining brightness is not in the ENB grade at all; most likely
the 1.1.1 weather RECORDS themselves (the game's own light colours in the rebuilt esm), which no ini can undo. Done: darkened override
disabled (PICTA + Studio, line 3332, kept built), `picta_ab_switch.py to101`: 1.0.1 weathers + 1.0.1 ENB data on, 1.1.1/1.1.2 off,
Nordic Winds patch MOD kept enabled with its esp UNCHECKED (line kept, no slot loss), fair patch + clouds.nif at 1.0.1, Root twin
synced to 1.0.1 (5 files). Upscaling still off, ReShade on without DOF/blur. Backups `modlist.txt.bak-goback-20261012`.

## 2026-10-12 (late, 5) - user: "nooooo I want the new picta you are not trying hard enough" -> full sweep + v3 + record patch

6-lane workflow (wf_43f22efe-fcd, 12 agents, each lane re-verified by a skeptic; digest scratchpad s17_digest.py / s17_bright.txt) found
the 1.1.x brightness in ~15 places, not 2. Confirmed causes: E11 [TIMEOFDAY] (dawn 2 h earlier, Day peak 12h: up to +1.5 EV mornings);
climate PIC_CLMT_Skyrim full day 08-18 instead of 09-17; VOLI PhaseFunctionScattering lowered (daytime god-ray veil off-sun x5);
[GAMEVOLUMETRICRAYS] x1.25-1.67; E11 [VOLUMETRICRAYS] x5 (sky/far terrain); [RAYS] sun shafts x10; DLI/ALI dawn/dusk + storm ambient;
fog colour multipliers/curves; mist weathers 10x fog + 3x bloom + 3x denser record fog + new density VOLIs; interior bloom thresholds;
[WATER] brightness x2; night sky gradient/scattering; WTHR FogFar, haze-band cloud layers 27/28 (+ layer 27 alpha), night sky colours,
DALC +22-45% in cloudy/overcast/storm/snow; dropped fVolumetricLightingIntensity=0.0 (engine fallback 2.0 for any weather/slot without
a VOLI: Bruma, Wyrmstooth, Olenveld, MQ scenes incl. the Helgen intro whose VOLI links point at missing records).
BUILT: (1) override v3 (`\_tools\picta-bridge\picta_darken_v3_full.py`): 25652 values, every non-colour number = 1.0.1 (category
medians per weather, 1.0.1 root/base values, [TIMEOFDAY] 3.5/9/10/17/3.5/20.5), colours stay 1.1.2; + the 1.0.1 'Picta - Weathers of
Aurbis.ini'. Backups `_backups\2026-10-12 - Picta darkened v1 (before v2)` and `... v2 (before v3)`. (2) ESL record patch
`Authoria - Patch - Picta 1.1.1 - Darkened to 1.0.1.esp` (`picta_darken_records_patch.py`): CLMT 000812 TNAM 06/09/17/20, 21 VOLI = 1.0.1
bodies, 23 MASTER WTHR (FogFar, night sky 75, cloud 27/28 colours + 27 alpha 0, DALC x k, mist fog distances + VOLI relink). Masters
Skyrim/Dragonborn/Update/Dawnguard/Picta esm. Placed: plugins.txt after `Authoria - Picta over NAT.esp` (PICTA 1258, Studio 1256),
loadorder 1318/1316, plugingroups after the same line; mod line above the override in 5 modlists (+ PICTA/Studio, - elsewhere).
houseCARL: 0 errors, patch wins every record, values read back (CLMT 06/09/17/20, VOLI g 0.999, C03 fog 150000/0.9, DALC scaled).
Lanes switched back to 1.1.x (`picta_ab_switch.py to111`) with the override ON; Root twin synced from the override (4 files).
Not done on purpose (content, not scene brightness): region weather frequencies (1.1.1 has clear 2x as often), climate fallback WLST.

## 2026-10-12 (late, 6) - v3 + record patch CONFIRMED ("THERE WE GO ... still a tiny bit too DARK but so much better")

- Exposure trim: picta_darken_v3_full.py TRIM_EV = 0.2 adds +0.2 EV to every Adaptation Exposure Compensation (1134 values; e.g. Day 2.5 -> 2.7)
  in the override weather inis + root enbadaptation.fx.ini (adaptation-side, so the eye adaptation does not normalise it away). Change
  TRIM_EV and rerun the builder + sync_root_twin.py to nudge. [TIMEOFDAY] lines now written without a space before '='.
- ReShade: what the user misses = the removed MagicDOF/Matso/Ring/GP65 DOF + GaussianBlur. Picta 1.1.2 ships enbdepthoffield.fx.ini, but
  Silent Horizons 2 (1.10 installed, 1.15 on Nexus) has NO depth-of-field shader, so E11 logs 'Effect file not found, skipping
  enbdepthoffield.fx'. Option: an E11 DOF (draws before the UI) from an installed plain-HLSL ENB DOF (Cabbage / Berserkyr ship one).
- Brynjolf (GAB's Brynjolf Replacer, Nexus 170105): hair renders auburn, but the beard (FacialHair HDPT BrynBeards, HairTint + Decal flags)
  and brows render untinted: beardshort01.dds is pale brown (mean 100,81,67) -> reads blond/white. Facegen tint in the nif is dark
  (0.289,0.219,0.211); TSOS's Brynjolf facegen uses (0.51,0.235,0.188) red. Fix options: recolour the beard/brow textures auburn (texconv
  available in tools\xEdit\Edit Scripts) or use TSOS. User decision pending.

## 2026-10-13 - ReShade effects back without UI smear + Brynjolf beard (user picks: beard 1a; ReShade "you can figure it out")

- WHY the UI was crisp before: PureDark ran ReShade before the UI (mRenderReShadeBeforeUpscaling), and in the Picta lane until
  10-11 ReShade sat on a frame-gen D3D12 swap chain with no depth (MagicDOF inert). Bottled 1.0.11 has no frame gen, so ReShade got
  real depth on the D3D11 chain and its DOF ran AFTER the UI. The extra Matso/Ring/GP65 DOFs also drew the distant double vision.
- BUILT: `_tools/reshade-before-ui` -> mod `Authoria - ReShade Before UI` (+ PICTA / Studio, - in the 4 other profiles with the
  Picta-lane preset) = SKSE + ReShade add-on DLL; wraps ID 82084 +0x17A (1.6.1170, bytes verified on a SteamStub-decrypted copy)
  and calls render_effects there, the SSE ReShade Helper method (the original is on CS's incompatible-DLL list by file name).
  Picta-lane `Northman II.ini` Techniques back to the 10-06 set: + GaussianBlur + MagicDOF (no Matso/Ring/GP65); backup
  `.bak-beforeui-20261013`. Modlist backups `.bak-beforeui-20261013`.
- Brynjolf: hair is tinted in game, beard and brows render their raw textures; brows are dark already, beard texture pale ->
  mod `Authoria - Brynjolf Auburn Beard` above GAB (+ PICTA / Studio, - elsewhere) with beardshort01.dds scaled to mean 49,34,21.
- Next launch checks (mine): `SKSE/AuthoriaReShadeBeforeUI.log` (hook installed / registered / first pass), ReShade.log add-on line.

## 2026-10-13 (later) - original Northman II restored in the Picta lane (user: "restore the original settings from northman but keep our UI fix")

- First test launch 04:28: AuthoriaReShadeBeforeUI log = hook installed, registered (ReShade.log "Registered add-on ... API 18"),
  first pre-UI pass done. The user then edited DOF in the overlay (Matso/Ring/GP65 back on, blur radius 2.0) - saved as
  `Northman II.ini.bak-useredits-20261013-0443`.
- Lane preset = byte copy of the Nexus 159125 v1.0 file (md5 1fd04722...; pristine copy `Northman II.ini.original-159125-1.0`):
  Pirate_Bloom, LUT pack, CAS, Curves, Clarity, AmbientLight, Vibrance (-0.10), GloomAO SSDO_Plus, RadiantGI PCGI_One, Vignette,
  Technicolor, GaussianBlur, Colourfulness; MagicDOF OFF at start (Scroll Lock toggles it), Ctrl+Delete toggles GloomAO + RadiantGI.
  Lane ReShade.ini KeyEffects back to none (the 10-12 test toggle sat on Scroll Lock too). Archive copied to D:\1. MOD STUFF\1. SKYRIM FILES\CS.
- Note: with the pre-UI plugin ReShade has real scene depth, so GloomAO + RadiantGI now actually run in this lane (before 10-12 they
  had no depth here) - fps and the look (AO darkening, GI bounce, bloom) can shift. Script: `_tools/reshade-before-ui/restore_northman_original.py`.

## 2026-10-13 (later, 2) - "the July look" = Northman + the automatic DOF -> AMON ENB's ADOF in the Picta lane

- Finding: July profile DEEEZ NUTTZZZ ran AMON ENB REBORN (EnableDepthOfField=true, ADOF Kitsuune Edition, autofocus) under the
  stock Northman II (MagicDOF off). User 08-31: DOF "was automatic" in July; MagicDOF on = "overblown and just wrong".
- Built: mod `Authoria - Picta - July Depth of Field (AMON ADOF)` above the darkening override (+ PICTA / Studio, - DEEZ CS NUTZ / PBR /
  PICTA EXPERIMENT; backups modlist.txt.bak-julydof-20261013): AMON's enbdepthoffield.fx with includes inlined, its July
  enbdepthoffield.fx.ini, white Textures/BokehMaskAtlas.png placeholder. Override rebuilt with EnableDepthOfField=true +
  [DEPTHOFFIELD] FocusingTime 0.5 / ApertureTime 5.0 (forced in picta_darken_v3_full.py); Root twin re-synced. Installer:
  _tools/picta-bridge/install_july_dof.py. MO2's process hung windowless after exit (files written 05:18) and was ended at ~05:24.
- Verification 10-13 (workflow wf_3c3bb9f6-c46, 9 agents, 0 confirmed defects): see memory july-look-was-amon-enb-dof. Side note (older,
  display only, not from this change): PICTA plugingroups split 3 group headers ('Essential - BugFixes', 'Lighting - Lux Patches',
  'Visuals - Seasons and Landscape') around the Helios_Astralite* plugins; tidy later by regrouping those 3 lines if the user wants.

## 2026-10-16 - lighting tune: interiors by location, summer sunny variants, A/B-master nudge (LIVE, in-game check owed)

User ask (10-15): interiors (not the start room) more reliant on windows/candles/fires without more bloom; summer warm on sunny
days; a tiny bit more Cabbage/AMON without leaving Picta. Designed by a 3-designer / 2-judge / 10-verifier workflow, built with
MO2 + game closed. Backup: `_backups\2026-10-15 - Picta lighting tune (pre)`.

- INTERIORS: Effects 11 location weather turned on (`[WEATHER] EnableLocationWeather=true`); `enbseries\_locationweather.ini`
  section `[0]` maps 961 interior LOCATIONS (43 inns -> AA004, 530 house-like -> AA001, 388 dungeon-like -> AA007) to three
  MINIMAL files `Authoria - Interiors\{House,Inn,Dungeon}.ini` (56 keys each; everything else inherits the live base/root).
  House / Inn / Dungeon: ambient 0.86/0.51 - 0.84/0.50 - 0.82/0.485 (base 0.97/0.575), adaptation EC 2.23 - 2.19 - 2.16
  (root 2.402 + log2 of the ambient cut), point 1.15/0.27 - 1.18/0.275 - 1.15/0.27 curves 2.3/3.6, fire 1.30 - 1.35 - 1.30
  curve 3.3, particle day 1.1/1.1/1.0, bloom mixing 0.09, glow saturation 1.05/1.05/1.0, teal CG tint 0.08/0.08/0.09,
  dungeon contrast 1.03. Start room (no Location) and 786 keyword-less interiors keep the base ini exactly.
- SUMMER: five weathers PIC_WTHR_SUMMER_A01/A02/A03/B01/B02 injected into the Picta esm FormID space (5AFA01-03, 5AFB01-02)
  by `Authoria - Patch - Picta Seasonal.esp` (still ESL, 98 records, no new plugin, masked ids index-free). Record: sunlight
  255,241,220, sun disc 255,250,236, far fog 127,124,120 (Day only). E11: `Authoria - Summer\*.ini` = nudged masters with
  DirectLightingDesaturationDay 1.0 -> 0.6, direct x1.06, CG Day saturation +0.025 capped 1.15, contrast 1.03, balance
  1.01/1/0.99, KiSuite Day midtone tint 0.98,0.955,0.925 @0.1. 39 regions: each sunny Common entry -> Spring/Summer(variant)/
  Autumn/Winter entries, same lane and chance (odds identical, proven from SeasonsFrameworkMain.psc). Helios exit script
  returns the summer variant in months 5-7.
- NUDGE: CG contrast +0.02 and Bloom Mixing saturation +0.1 on Sunrise/Day/Sunset of A01_Clear, A02_Clear_Mist,
  B01_Lightly_Cloudy, B02_Lightly_Cloudy_Misty_Fog only.
- Tools: `_tools\picta-bridge\picta_authoria_overlay.py` (stage at the end of picta_darken_v3_full.py), `overlay\tune_values.json`,
  `overlay\interior_locations.json`, `verify_lighting_tune.py` (API read-back of the location section = 961 entries, VERIFY OK).
  Rebuild = --write, sync_root_twin.py --write, verify_lighting_tune.py. houseCARL check on the patch: 0 dangling.
- Not covered: Preset Studio HPH (shares the override mod, not the Seasonal patch / exit mod), the Wanderer's Fair climate,
  Bruma/Wyrmstooth static sunny entries, the friend package / 'No Fair' variant (now stale).
- First launch checklist: CommunityShaders.log "[WeatherManager] Loaded location weather for 1 worldspaces"; start room unchanged;
  Bannered Mare / Breezehome 12:00 + 22:00 vs the start room (EC +-0.05 if darker/brighter, never ambient first); Whiterun
  plains noon; a June clear day on the tundra (grass hue - fix = desat 0.6 -> 0.8, not grass).
