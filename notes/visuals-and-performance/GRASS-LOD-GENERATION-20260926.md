# Grass LOD generation for Grass Optimizations (DynDOLOD test build) - step sheet, 2026-09-26

Goal: keep NGIO grass at 100000 units and full density, and make the far band cheap by giving Grass Optimizations the LOD meshes it swaps in at distance. DynDOLOD's test build generates them: an atlas texture per grass model, an updated full grass NIF, an updated _LOD0.nif where one exists, and a new _LOD1.nif (crossed planes with TexGen billboards). Source: the DynDOLOD forum thread "[WiP] Community Shader - Grass Optimizations support" (sheson, 2026-09-25) and dyndolod.info/Mods/Community-Shaders. This is a work-in-progress feature: expect rough edges, and two Grass Optimizations users report periodic freezes with Mesh LOD switched on.

Who does what: the user runs TexGen and DynDOLOD (never the agent). The agent prepares files, edits the tool inis, installs the outputs into the existing output mods and flips the Grass Optimizations settings afterwards.

STATUS 2026-09-26 10:15: ALL SECTIONS DONE. DynDOLOD run 2 completed (session 08:26, Save and Exit at 10:06, no exception) and the output is installed in Authoria - Dyndolod Output (7681 files, 28.9 GB). The three plugins are back at their recorded slots in the PBR profile, Grass Optimizations EnableMeshLOD is true, the PBR texture-fix patch is retired as obsolete, and the output mod is unticked in the four profiles whose load orders lack its masters. FIRST LAUNCH UNTESTED: read CommunityShaders.log, the DynDOLOD DLL log and the frame-gen probe before any relaunch.

## 1. Downloads (done)

| Item | Where | Size | Why |
|---|---|---|---|
| DynDOLOD 3.00 Alpha-211 | Nexus 68518, main file id 798219, manager download only | 36.4 MB | current release; test files must be laid over the latest release (installed today: Alpha-205, C:\1. AUTHORIA\tools\DynDOLOD) |
| Test versions: DynDOLOD.x64.exe, TexGenx64.exe, Edit Scripts folder | dyndolod.info Downloads > Test Versions (Mega folder), files dated 2026-09-25 | about 95 MB | the build that has the CS Optimized Grass option |
| DynDOLOD DLL NG and Scripts Alpha-43 | Nexus 97720 | small | optional; installed is Alpha-41 (2026-09-09 release) |

DynDOLOD Resources SE is already at the current Alpha-59.

## 2. Install the tools (agent, MO2 closed)

1. Back up C:\1. AUTHORIA\tools\DynDOLOD whole to _backups\2026-09-26 - DynDOLOD 205 pre-211.
2. Extract Alpha-211 over the tool folder, then the three test items over that, in this order.
3. Re-apply the 11 customised keys that differ from the archive defaults in Edit Scripts\DynDOLOD\DynDOLOD_SSE.ini (the classic grass-LOD brightness keys, GrassBrightnessTop/Bottom and ComplexGrassBrightnessTop/Bottom, see the appendix). Harmless if the new option ignores them.
4. Add to Edit Scripts\DynDOLOD\TexGen_SSE.INI: CSGrassOptimizations=1
5. Add to Edit Scripts\DynDOLOD\DynDOLOD_SSE.ini: CSGrassOptimizations=1 and CSGrassOptimizationsBillboard=DynDOLOD_flat_2x2plain_lod.nif
6. Clear old logs in tools\DynDOLOD\Logs so the new run's logs are clean for any bug report.

## 3. TexGen (user) - done 06:39 to 06:47

- Run from MO2 as usual. Check HD Grass. Set Direct 0, Ambient 100, Smoothness 0. Everything else as on 2026-07-27.
- Warning from sheson: large grass textures make this much slower. This order's winning grass textures: 132 of 224 are 2048x4096 and 7 are 4096x8192. Plan for a long run.
- Output to the usual TexGen output folder; the agent then replaces the contents of the mod "Authoria - TexGen Output" (9871 files today).

## 4a. Reqtificator first (user) - added 07:25 after DynDOLOD refused

DynDOLOD refused with "Found Requiem for the Indifferent.esp. It contains DynDOLOD.esm as a master. Remove it permanently from the load order." The Reqtificator output (mod Authoria - RFTI Output, run of 2026-08-28 13:38) carries DynDOLOD.esm as master 47 of 225 because it patched 12 DynDOLOD-made copies (4 CONT, 8 DOOR, names ending _DynDOLOD_BASERECORD). sheson's rule (dyndolod.info/Messages/Found-esm-esp-esl): all patches are generated before DynDOLOD, and patch plugins that require DynDOLOD plugins become obsolete when LOD is regenerated. The Reqtificator reads only plugins before its own output, and DynDOLOD.esm is absent from the order right now, so a run now produces an output without that master; DynDOLOD then makes its container and door copies from the Requiem-patched winners itself. Master estimate for the rerun: 225 minus DynDOLOD.esm plus up to 10 new masters (Rovan Market Stall, Magic Pariah, Burlesque and its Requiem Clothing patch, Isekai Novice and its Requiem patch, Sorceress Attire with UBE patch and Reqtificated patch, Animated Bound Weapons) = about 234 of 254. The tweak build still wins (modlist line 286 above stock at 1415) and the relief patch sits at loadorder 4075 directly before the output at 4080.

Done by the agent 07:10 to 07:20 with MO2 closed: mod houseCARL - Authoria - DynDOLOD PG Texture Fix - PBR disabled in the PBR profile (backup modlist.txt.bak-pgfixmod-20260926) so its plugin leaves the data folder. A scan of 4314 plugin files in the enabled mods, overwrite and Stock Game found no other plugin with DynDOLOD.esm, DynDOLOD.esp or Occlusion.esp as a master; the Synthesis outputs are clean.

1. Open MO2. Ignore the missing-master warning on Requiem for the Indifferent.esp; it clears after the run.
2. Run Reqtificator from the executable list, click Patch, wait for "Patch Success", close it.
3. Go straight on to section 4 (DynDOLOD). If the Reqtificator reports a failure instead, stop and report it.

## 4. DynDOLOD (user) - the run

Already true, checked 07:10: Authoria - Dyndolod Output is unticked and empty, Authoria - TexGen Output holds the new textures, no earlier output with CS-updated grass NIFs exists, the PBR texture-fix plugin is unticked, DynDOLOD_SSE.ini has Wizard=0 so the tool opens in Advanced mode. The July settings are carried over in Presets\DynDOLOD_SSE_Default.ini (High preset with child worlds Medium, all 63 worldspaces, Ultra tree LOD on and standard Tree LOD off, dynamic LOD, occlusion quality 3 into its own plugin, Candles, FXGlow, Windows high, seasons WIN/SPR/SUM/AUT, large-reference workarounds, output D:\Dyndolod Output\), so the window should open filled in.

1. Open MO2, pick DynDOLOD in the executable list, Run. Any "large reference" or "Seasons" notice is informational; continue.
2. Check the window matches the list above: all worldspaces ticked, High, Ultra ticked, Tree LOD unticked, Occlusion ticked, Candles / FXGlow / Windows ticked, Generate DynDOLOD ticked, output D:\Dyndolod Output\. If anything is blank, set it to that.
3. Tick "Create assets for CS Optimized Grass" (the new option; it sits where Grass LOD used to be and may already be ticked).
4. OK / Start. Expect 2.5 to 3.5 hours; the author's run took 2 h 33 min without the grass step.
5. When it reports completed: Save and Exit (not zip). Close MO2. Tell me "dyndolod done".

## 5. After install (agent, MO2 closed) - done 10:08

- Install: robocopy D:\Dyndolod Output into mods\Authoria - Dyndolod Output, tick the mod back on in the PBR profile, and restore the three plugins at their recorded slots (MO2 dropped them from loadorder.txt, plugins.txt and plugingroups.txt when the mod was emptied): DynDOLOD.esm between PGPatcher.esp and Vanilla Eating Animation Fix.esp (group Master Files - Visuals); DynDOLOD.esp right after PG_2.esp and Occlusion.esp right after Authoria - DynDOLOD PG Texture Fix - PBR.esp, both before FWMF for Fantasy Paper Maps.esp (group Authoria - Outputs). Recorded in profiles\DEEZ CS NUTZ - PBR\loadorder.txt.bak-batch2b-20260925 lines 207, 4115, 4117.
- Authoria - DynDOLOD PG Texture Fix - PBR.esp (unticked 07:05): it put PGPatcher texture sets (MODS) on 48 DynDOLOD-made copies of statics (names ending _DynDOLOD_NOFLAG, _BASERECORD, _NOSCRIPT) because the July output pre-dated the PBR pass. The new run generates from the PG-patched winners, so the copies should carry the texture sets already. Verify on the new DynDOLOD.esm before anything is re-enabled; expect to retire the patch.
- Grass Optimizations settings: EnableMeshLOD true; keep MidLOD 8 px and FarLOD 4 px thresholds; keep RenderDistanceOverride 100000; MinDensity back toward 1.0 can be tried once the meshes carry the far band.
- NGIO GrassControl.ini unchanged: 100000 / fade 0 / DynDOLOD-Grass-Mode 0 (the author's recommendation).
- Verify on launch: CommunityShaders.log for Grass Optimizations lines about LOD meshes, no compile errors, then the frame-gen probe and hitch count against the 2026-09-26 baseline (41 to 42 fps at Helgen, 25 in heavy areas, 30 hitches per ten minutes).
- If the periodic freeze reported by other users appears with Mesh LOD on, switch EnableMeshLOD back off; the generated meshes then simply go unused.
- DynDOLOD DLL NG stays at Alpha-41. Alpha-43 (2026-09-09) only adds static linking, multithread tweaks, a duplicate-object-LOD-after-load fix (Alpha-42) and runtime 1.7 support. Not required for Alpha-211 output; optional later.

## Open questions

- Whether the CS route needs the NGIO grass cache present during generation (classic grass LOD did). Assume yes, the five seasonal caches stay enabled.
- ANSWERED 09:40: seasonal grass is swapped at the form level only. All 357 Seasons ini files use [Statics] / [Trees] / [LandTextures] / [Grass] / [Flora] etc. form swaps and none names a .dds, so every seasonal grass model is its own GRAS form with its own NIF and got its own atlas (field_snow, grass_snow, shrub_berry_snow and so on are among the 145). The updated full NIF and the _lod1.nif both point at textures\dyndolod\lod\dyndolod_grassoptimizations_<model>_<id>.dds. Still worth one look at a winter cell on the first launch.

## Appendix: options saved by the tools on 2026-07-27 (from DynDOLOD.ini and TexGen.ini in Edit Scripts\DynDOLOD)

```
--- DynDOLOD.ini
[frmMain]
pnlNavWidth=512
vstNavColumnWidth0=226
vstNavColumnWidth1=141
vstNavColumnWidth2=124
WindowState=0
Left=165
Top=132
Width=1532
Height=777
[Init]
FirstStart=1
[Options]
NoGitHubCheck=1
[SSE LOD Options]
OcclusionQuality=3
OcclusionHeight=0
OcclusionRadius=100
OcclusionMode=-Flat +Border
OcclusionMaxThreadsTerrainLOD=-1
OcclusionMaxThreadsObjectLOD=4
OcclusionNewPlugin=1
Chunk=0
--- TexGen.ini
[frmMain]
pnlNavWidth=512
vstNavColumnWidth0=226
vstNavColumnWidth1=141
vstNavColumnWidth2=124
WindowState=0
Left=190
Top=123
Width=1540
Height=785
[Init]
FirstStart=1
[Options]
NoGitHubCheck=1
```

## Run log

- 2026-09-26 06:24 to 06:26: the two output mods were emptied in MO2 and Authoria - Dyndolod Output was unticked (done by hand before the first TexGen attempt; no agent action in that window). Finding: those outputs were never generated on this machine. Their meta.ini files name Nexus 170235 uploads of 2026-07-20, and the July logs in the tool folder are the list author's run (D:\Wabbajack\Authoria-dev, DynDOLOD Alpha-205, session 2026-07-20 15:54). Nothing is in the Recycle Bin and there is no backup; the plan regenerates both anyway.
- 06:32: TexGen session 1 refused on the Einar 0x804 override (fixed 06:37, backup folder 2026-09-26 - Einar stale 0x804 override drop).
- 06:39 to 06:47: TexGen session 2 completed. Settings echoed in the output (textures\DynDOLOD\LOD\TexGen_SSE.ini): GrassHDBillboards=1, Direct 0, Ambient 100, Smoothness 0; the log says "Community Shader Grass Optimizations: enabled". 194 grass and 967 tree billboard sets (HD grass = four sides plus normal maps per model), 585 Texconv conversions, 10954 files, 2.24 GB. 31 texture-not-found errors, all pre-existing asset gaps: textures\oak\oakleafmushroom01_n.dds (29 times, NotWL rainoak05_aut via Authoria - Seasons - Markarth Trees Winter), textures\landscape\grass\ferngrass01a.dds, textures\Landscape\Grass\RedBranchesDrJ_Sn.dds. The 42 warnings are the usual "extended FormID range, Game Master first" notes.
- 06:59: installed into mods\Authoria - TexGen Output (robocopy, 10954 of 10954, byte totals equal, md5 spot-check equal). Old meta.ini backed up to _backups\2026-09-26 - TexGen Output install; a notes line was added. Raw copy left at D:\TexGen Output.
- 07:05: DynDOLOD_SSE.ini Wizard=1 changed to 0 (backup _backups\2026-09-26 - DynDOLOD wizard0). PBR profile plugins.txt: Authoria - DynDOLOD PG Texture Fix - PBR.esp unticked because its masters DynDOLOD.esm and DynDOLOD.esp no longer exist (backup plugins.txt.bak-pgfixoff-20260926). TexGen had not loaded it either.
- July options decoded from the author's logs (LODGen_SSE_Tamriel_log, Object_Report, Tree_LOD): rules file DynDOLOD_SSE_High.ini, Max Level 32, HD flag on, remove faces under terrain and water, merge meshes, 8192 atlases, ULTRA tree LOD (the carried preset Presets\DynDOLOD_SSE_Default.ini says UltraTreeLOD=1 and DoTreeLOD=0; the July log's "Generating tree LOD" line misled the first reading, the preset is authoritative), dynamic LOD on, occlusion quality 3 radius 100 mode -Flat +Border in a separate Occlusion.esp, Candles, FXGlow and Windows (high) on, seasons Default/WIN/SPR/SUM/AUT, large-reference workarounds on, child worlds Medium, Level32 off, DoGrass=1 in the preset although the July log shows no grass LOD pass. That preset also carries OutputPath=D:\Dyndolod Output\ and all 63 worldspaces, so the GUI opens pre-filled. MO2 launches both tools with only -sse and the data path; no output argument.
- 07:12: DynDOLOD refused at start (Found Requiem for the Indifferent.esp, DynDOLOD.esm master). Only two DynDOLOD dependants exist (that output and the PBR texture fix). PBR texture-fix mod disabled 07:20; order changed to Reqtificator first, then DynDOLOD (section 4a). Rule recorded in memory reqtificator-before-dyndolod-authoria.
- 07:35: Reqtificator rerun 07:26 to 07:28, Patching Result SUCCESS, new output 227 masters, no DynDOLOD master. DynDOLOD Advanced window opened with the carried preset and Create assets for CS Optimized Grass already ticked. Settings recommended for 4K on the RTX 5090 (32 GB): tick every worldspace (Coldspire Canyon from Improved Companions was unticked), untick Large (trees as large references; the preset value was 0) and untick Upgrade NearGrid large references to FarGrid (sheson: uncheck when the large reference system is in use), Max tile size LOD 2048 / full 512 / billboard 2048 (sheson: match 2160p, quarter for full), keep Ultra, Glow windows High, Occlusion quality 3 + Plugin, Seasons + Snow, Parent > child, Child > parent Medium, Level32 off (map only), Fake lights off, Terrain underside off, Downgrade FarGrid off.
- 08:03 to 08:13: DynDOLOD run 1 (session 07:29, generation started about 07:42) CRASHED. The CS grass step had completed at 07:54 (145 full grass NIFs updated, 145 _lod1.nif, 145 per-model atlases, LODGen_SSE_ComplexGrass_log Code 0), Tamriel object LOD plus the four season passes and the child-world copies completed. At [20:44] Gathering CELL and LAND records for DLC2SolstheimWorld -> [21:18] EAccessViolation (offset 2DA58, inner EInvalidPointer from BrainMM in UnicodeFromLocaleChars <- TwbRecord.GetName <- GetElementByName <- TwbWrldCellsData.Add <- DoObjectLOD), then a second AV (offset C4957, read of -1) after the summary; the user exited. Memory was not the limit (24.6 GB allocated, 15 GB free). No WHEA or application event at that time (last fatal WHEA 09-13). A parse of all 4300 plugins found no malformed LAND record in Solstheim (14 plugins, 915 cells won by the Synthesis Worldspace output). Logs, bugreport.txt, the summary pages and a zip for the forum are in _backups/2026-09-26 - DynDOLOD crash 0803 logs (draft post sheson-report-draft.md). The failed output was moved to D:/Dyndolod Output - failed 0803 (23 GB, keep until a good run exists). Rerun 2 started with identical settings to test reproducibility.
- 09:40: run 2 (started 08:26, generation from about 08:33) passed the Solstheim point at 08:55 with no exception; all 110 LODGen passes done by 09:04; occlusion phase running. The non-power-of-2 trunk texture errors (1960 of 2072 TexGen tree textures, NotWL trunks) also appear in the author July log (670 lines): pre-existing, not new.
- 10:07: run 2 completed: [1:11:46] Occlusion.esp completed successfully, Save and Exit at [1:31:26], DynDOLOD.esm (6.2 MB, 42 masters), DynDOLOD.esp (5.0 MB, 107 masters), Occlusion.esp (17 MB, ESL, 39 masters); 7681 files, 28.9 GB; no exception in the session. The crash of run 1 did not reproduce with identical settings.
- 10:08: installed by robocopy into mods/Authoria - Dyndolod Output (7681 of 7681, bytes equal), meta.ini note added, old meta.ini in _backups/2026-09-26 - DynDOLOD Output install. Raw copy kept at D:/Dyndolod Output; the failed run 1 output at D:/Dyndolod Output - failed 0803 (23 GB) can be deleted.
- 10:08: PBR profile: mod ticked (modlist line 31), DynDOLOD.esm after PGPatcher.esp (loadorder 207, group Master Files - Visuals), DynDOLOD.esp after PG_2.esp (4116) and Occlusion.esp after it (4117), both group Authoria - Outputs, before FWMF for Fantasy Paper Maps.esp; plugins.txt 147 / 4056 / 4057; lockstep verified; backups *.bak-dyndolod-20260926.
- 10:08: overwrite SettingsUser.json Grass Optimizations EnableMeshLOD false -> true (backup .bak-meshlod-20260926); MinDensity 0.35 and RenderDistanceOverride 100000 unchanged.
- 10:08: texture-fix verdict: all 50 records the PBR DynDOLOD texture fix overrode exist in the new output by EditorID and every one already carries MODS, so houseCARL - Authoria - DynDOLOD PG Texture Fix - PBR stays disabled for good (folder kept).
- 10:08: the new plugins list masters that only the PBR profile and PICTA have (PGPatcher.esp, MagpieManor.esp, ImprovedCompanionsBoogaloo.esp, FA01RedcapFollower.esp, 3DNPC.esp), so Authoria - Dyndolod Output was unticked in Main, NSFW, DEEEZ NUTTZZZ and DEEZ CS NUTZ (backups modlist.txt.bak-dyndolod-otherprofiles-20260926). Those profiles have no object LOD until they get their own generation. PICTA keeps the tick.
- 10:32 to 10:41: Synthesis 0.36.6 rerun by the user (build blocked inside MO2 at 10:32 - Mo2BuildBlockedException, VFS incompatible with .NET SDK builds - so a build pass outside MO2 at 10:38, then the run from MO2 at 10:38:41). All 10 patchers ran, no [ERR] in the run log. Outputs rewritten in place: Authoria - Output - Synthesis Gameplay.esp (79 masters) and Worldspace.esp (87 masters), neither with a DynDOLOD or Occlusion master, so DynDOLOD stays regenerable. Profile files intact (DynDOLOD plugins still at 207 / 4117 / 4118, nothing appended).
- 10:50: verified that the Synthesis Worldspace rerun finally carries Authoria - Patch - Grassreach Northern Roads Land.esp (built 09-03 09:06, buried by the 09-03 06:04 Synthesis copies until now): of its 34 LAND cells, 24 are copied with identical base layers, additional layers, alpha maps and heights (only vertex colours changed, which is that patcher's job) and 10 have no Synthesis copy so the patch wins directly. Blackreach Northern Roads grass should show for the first time since 09-03.
- 10:21 to 10:22 (found at 10:55): the user re-ran the Reqtificator a second time AFTER the DynDOLOD install, so Requiem for the Indifferent.esp carries DynDOLOD.esm again (master 47 of 228; the 12 container and door copies). Fine for play: it is built against the NEW DynDOLOD.esm. Synthesis ran after it at 10:38 and its outputs still have no DynDOLOD master. Consequence: before the NEXT LOD generation, untick Authoria - Dyndolod Output, rerun the Reqtificator, then Synthesis, then DynDOLOD. The non-PBR profiles show missing masters for the shared Reqtificator and Synthesis outputs as they did before today; they need their own outputs and are out of scope.
- 13:41 to 14:03 LAUNCH 7 (first with the new LOD): CommunityShaders 1.9.0 log clean (only devbench warnings); Grass Optimizations hooks installed, HiZ cull active, 26 grass LOD1 meshes loaded on demand, cached feature valid; DynDOLOD DLL NG 3.0.41 initialised; Dynamic Wind alive (813 tree configs, wind targets updated); deformation log still 2 lines (logging off). Frame-gen probe: 612 samples, median 26.4 real fps, per 2 min 60 (menu) 40 33 33 31 26 then 22 22 22 22 22 in the open - worse than launch 5 (median 34.6, floor 26). User: fps still not great, trees still not swaying, fresnel looks weird (no screenshot yet). Logs backed up to _backups/2026-09-26 - logs launch 7 (grass LOD + synthesis).
- 14:20: staged launch 8 as a two-lever test with MO2 closed: Dynamic Terrain Deformation SKSE flipped OFF in DEEZ CS NUTZ - PBR and DEEZ CS NUTZ (plan_dtd_off.json, backups *.bak-dtdoff-20260926; plan_dtd_on.json restores) to settle the tree-sway suspect and measure its cost; DynamicShaderFrameGen.ini NRRenderScale 1.00 -> 0.75 (the author sweet spot; backup .bak-nr075-20260926 in the DSFG mod folder). Asked for an F10 overlay screenshot at a low-fps spot and a screenshot of the fresnel issue.
- 15:29 to 15:47 LAUNCH 8 (DTD off, NRRenderScale 0.75): WORSE. Probe median 20.4, floor 15 to 18 real fps in the open (launch 7: 22, launch 5: 26). The DSFG log shows why: the render resolution stayed native (Render scale 1.000 -> 3840x2160; QualityMode 0 + RenderResolutionScale 1.00, and the ini notes say any DLSS upscaling level draws a small image top-left on the CS profiles), while NRRenderScale only shrank the neural-rendering guide buffers to 2880x1620 and added a full-resolution copy path, so it cost frames instead of saving them. Reverted to 1.00 at 15:55 (backup .bak-nr075-revert-20260926). CS log clean, HiZ active, mesh LOD setting still true (no per-mesh load lines this time, disk cache). Tree sway with DTD off: not yet reported. Logs backed up to _backups/2026-09-26 - logs launch 8 (DTD off, NR 0.75). Native 4K is a hard constraint here, so the remaining levers are feature costs: neural rendering itself, grass mesh LOD vs pixel culling, and the CS exterior features; the F10 overlay is the only per-feature timing source.
- 16:00 to 16:35: user refused further test launches; a 10-agent read-only investigation (5 lanes + 5 adversarial verifiers, transcripts under the session workflows folder wf_557a9607-34b) worked from the three log backups, every settings file, the LOD output and the tool logs. Verified conclusions: the frame is GPU/render-bound and location-bound (no leak, no periodic hitch); the main menu alone runs 40-44 real fps once the frame-gen + neural-rendering present path is chained (60 before), so that path is at least 8 ms of every frame; the render thread sits in the CPU fence poll 80-95 percent of the time (FenceWaitBusy=1 signature); the new object LOD is lighter per level than the July output (LOD4 8.1 MB vs 24.2 MB per block) and measured +1.2 ms at the one shared spot; the engine LOD distances in SkyrimPrefs are overwritten at runtime by the DynDOLOD Settings Loader (MCM\Settings\DynDOLOD.ini: fBlockLevel0Distance 62048, fBlockLevel1Distance 100975) and by SSE FPS Stabilizer (ten [Level] blocks), so SkyrimPrefs edits to them are no-ops; iNumFocusShadow is forced by Community Shaders itself.
- THE FINDING: the DynDOLOD test build wrote all 145 Grass Optimizations atlases (2214 MB, BC7, 96 at 4096x4096, 8 at 8192x8192) with a SINGLE mip level (texconv -m 1 in the debug log) and rewrote 142 of the 145 full grass meshes plus all 145 _lod1 meshes to sample them. Unmipped 4K textures on distant grass = texture-cache thrash and specular shimmer; it is the only near-field change between the 34.6 and 26.4 sessions and a likely source of the weird sparkly look. Fix applied 16:40 with MO2 closed: originals copied to _backups/2026-09-26 - grass atlases no-mip originals, then Texconvx64 -gpu 0 -m 0 -f BC7_UNORM -sepalpha in place (verification below). Report this to sheson (draft updated).
- 16:42 applied, all with .bak-perf-20260926 backups, MO2 closed: Community Shaders Skylighting OcclusionUpdateInterval 33 -> 66 ms and OcclusionDistanceCulling 0 -> 0.5 (estimated 0.7-3 ms, small props stop occluding sky light at distance); DSFG FenceWaitBusy 1 -> 0 (the author's queue-side wait; documented 8.4-9.9 ms at 2K on his rig, estimated 1.5-5 ms here; the 09-25 freeze that prompted mode 1 happened during the first-launch shader compile storm, which is over - if a loading screen ever freezes again, set it back to 1); ReShade PerformanceMode 0 -> 1 (uniforms compiled as constants, 0.3-1 ms, no look change); Northman II preset GloomAO SSDO_MipSampling 0 -> 4 (the shader default, cheaper AO sampling, look mostly kept).
- USER CHOICES left open with numbers: (1) DLSS Neural Rendering off (NeuralRenderingEnabled=0): the author documents about half the render rate at full resolution; estimated 8-15 ms of the ~40 ms frame - the single largest lever; (2) ReShade Northman II: remove SSDO_Plus@GloomAO.fx, PCGI_One@RadiantGI.fx and MagicDOF@DOF.fx from Techniques= (a second screen-space AO, a screen-space GI and a bokeh depth of field on top of Community Shaders): estimated 4-7 ms; (3) uLargeRefLODGridSize 11 -> 9 in SkyrimPrefs (0.3-1 ms, large rocks and buildings 3.5-5.5 cells out switch to LOD); (4) Grass Optimizations FarLODPixelSize 4 -> 6 or 8 (0.5-1.5 ms, grass beyond about 2.5 cells becomes billboards sooner); (5) SimpleShadingPixelSize 6 -> 8 (under 0.5 ms). Rejected by verification: MinDensity / MinPixelSize / FullDetailPixelSize changes (contradict the 100000-unit dense grass), volumetric grid cuts, Light Limit Fix cuts (no effect in daylight), water SSR, particle cap, fBlockLevel edits in SkyrimPrefs (overwritten at runtime).
- 16:55: user decision - Neural Rendering stays on (the main thing they want). All other applied changes stand; the ReShade extras removal remains open.
- 09-27: user decision - ReShade stays in full (no effect removal). Fps work complete with the applied set; first launch with it still untested.
- 09-27 05:25 launch 9 (first with the applied set): ReShade banner 'errors loading some effects'. Log compared with the 09-26 session: the only new failure is METEOR\MartysMods_LONGEXPOSURE.fx (X3524 duplicate attribute flatten under PerformanceMode=1); it is NOT in the Northman II preset, and all 13 preset effects compiled. ReShade compiles all 496 .fx files at every launch (MotionFocus.fx alone 20 s). Plan: with the game and MO2 closed, add EffectLoadSkipping=1 to ReShade.ini [GENERAL] so only the 13 enabled effects compile (banner gone, faster launches, performance mode kept); fallback = PerformanceMode back to 0.
- 09-27 05:29: launch 9 was a 3-minute main-menu quit (no crash, no in-world data; fence mode 0 live, CS clean). After the game and MO2 closed the watcher set ReShade.ini SkipLoadingDisabledEffects=1 (backup .bak-skipdisabled-20260927): only the 13 preset effects compile from now on, so no banner and no 496-effect compile wait. PerformanceMode stays 1, SSDO_MipSampling 4 survived the preset auto-save. Still owed: one real outdoor session for the numbers.
- 09-27 05:38 to 05:47 launch 10 (all applied changes live): MEASURED real fps median 36.9, p10 32.6, floor about 34-35 in the open (was 22 two sessions ago; 60 in-world positions visited). User: better, but a weird flicker on the main menu and in gameplay. Logs: no NR skips, no bypasses, no duplicated frames, silent p50/p90 12/25 ms (was 15-20/36-40); large frame-to-frame brightness jumps (|dLum|>3) 5.6 percent of probes vs 1.5-2.1 before. 05:55 reverted the low-value suspects with .bak-flicker-revert-20260927 backups: ReShade PerformanceMode 1 -> 0, GloomAO SSDO_MipSampling 4 -> 0, Skylighting OcclusionUpdateInterval 66 -> 33 and OcclusionDistanceCulling 0.5 -> 0. Kept: grass atlas mips, FenceWaitBusy 0, SkipLoadingDisabledEffects 1. Logs in _backups/2026-09-27 - logs launch 10 (flicker).
- 09-27 06:05: user describes the flicker as an occasional white flash = a frame presented before the neural-rendering work wrote it, the race the CPU-poll fence prevents. FenceWaitBusy 0 -> 1 (backup .bak-flash-revert-20260927); the author docs list no other fix. Final standing set: grass atlas mips, SkipLoadingDisabledEffects=1, everything else at its original value; DTD still off pending the sway answer.
- 09-27 06:30 launch 11 (fence back to 1): no flashes; real fps median 33.1, per 2 min 41 33 26 20 - back near the old floor. User: fps awful, not close to usable. FACTS: DSFG 0.57 has no upscaler at all (DLL note: DLSS upscaling removed in v0.48; EnableUpscale/QualityMode are dead keys); Bottled CS 1.9 carries its own Upscaling feature (DLL strings, settings persisted: upscaleMethod 3 = DLSS, qualityMode 1 = Quality, frameGenerationMode 1 = FSR3 FG - the pre-08-29 config that gave 40-60 fps) but its shader files are parked in _backups/2026-09-24 - Bottled Shaders Upscaling parked and Disable at Boot/Upscaling = true; Bottled has no neural rendering. Investigation launched: can CS Upscaling (DLSS Quality + FG) run with DSFG in NR-only mode without the corner-image bug.
