# Mods added 2026-09-30 (batch 3): Walk With Me, IVBOS + Voiced Books, Follower Idles, Ice is Slick, Sunhelm Follower Needs, UBE YI presets, Bottled Shaders 1.0.4

Executed 2026-09-30 (afternoon) with MO2 and the game closed; every writer re-checked the process list first.
Profile backups: `profiles/<p>/*.bak-batch3-20260930` (all four files, all six profiles), plus
`*.bak-batch3fix-20260930` (Wayfarer.esp re-anchor in three profiles) and `*.bak-batch3-wayfarerfix-20260930`
(modlist only). Pre-state copy of the profile files + SettingsUser.json: `_backups/2026-09-30 - Batch3 pre-state`.
Tools: `place.py`, `write_meta.py`, `batch3/install_batch3.py` in the session scratchpad.

## Mod folders (9 new + 1 Authoria fix), all six profiles, all enabled

| Folder | Source (Nexus id / version) | MO2 placement (above = higher priority) | Notes |
|---|---|---|---|
| Ice is Slick | 190881 / 1.0.3.2 AIO | above SkyParkour v3 | SKSE DLL + ini, no plugin |
| Walk With Me | 191283 / 0.2.5 | above Offset Movement Animation- Modders Resource | Wayfarer.esp (light), Wayfarer.dll, 7 scripts, OAR clasp anims, SKSE Menu Framework UI |
| Walk With Me - Command Gestures | 191283 / 0.2.2 | above Walk With Me | Nemesis patch `gpma` + OAR "Walk With Me Signals" + 7 GPMAOffsetAnimation.hkx; needs Pandora with GP Offset Movement Animation ticked |
| Sunhelm Follower Needs - Hans Edit | friend share | above SunHelm Survival - Compatibility Patches | DLL + json only |
| Follower Idles | friend share (hsf) | above Kaidan 2 | FollowerIdles.esp (FULL), DLL + ini (Kaidan-only defaults), FNIS list + behaviour hkx for Pandora |
| UBE YI PRESET HUB | 193309 / 1.1 | above Anita - UBE Face Preset | 25 jslot + 17 BodySlide presets |
| Voiced Books of Skyrim | 94436 / 2.2.7 + audio 2.1.7 | above Dragonborn Voice Over | parts 1 + 2 merged into one folder (esp light, BSA 1 GB, VBoS Extension Plugin.dll) |
| IVBOS - Immersively Voiced Books of Skyrim | 191219 / 1.2 | above Voiced Books of Skyrim | FOMOD: Female Narrator (Vampira) + NPC Voices, USSEP installed, TCIY not installed; `!VanillaBooks_VBOS.ini` at Data root |
| IVBOS - Mod Patches | 191219 / 1.1 | above IVBOS main | 3DNPC, Quest Patch, DAc0da, Vigilant, Glenmoril, Unslaad, Follower Patch (11 dummy light esps + BSAs + 7 `*_VBOS.ini`); Beyond Reach skipped (not installed) |
| Biggie Traits - Additional Traits - Wayfarer script rename (Authoria) | built here | above Additional Traits for Biggie Traits | see "Wayfarer script collision" |

Skipped on purpose: Bottled Shaders 1.0.3 archive (superseded by 1.0.4, left in Downloads); Beyond Reach IVBOS patch.

Archives filed on D: (`1. SKYRIM FILES`): `gameplay and quests` (Ice is Slick, both Walk With Me, Sunhelm Follower Needs),
`animation` (Follower Idles), `racemenu` (UBE YI PRESET HUB), `voice and dialogue` (VBoS parts 1 + 2, IVBOS main + patches),
root (Bottled 1.0.4, beside 1.0.0 and 1.0.1).

## Plugins (all six profiles; groups written to plugingroups.txt)

| Plugin | After | Group | State |
|---|---|---|---|
| Wayfarer.esp (light) | dk_ThograEGGFlint_Banter.esp in CS / PBR / PICTA; KW_ValSeranoRefined.esp (Main), SM_Astrid - OStim.esp (NSFW), GORE - Fishing CC Patch.esp (DEEEZ) = last of the group there | Quests and Newlands - Followers | active |
| FollowerIdles.esp (FULL, max FormID 0x182F so not light-able) | Use Special Markers.esp | -- Animations -- | active |
| Voiced Books of Skyrim.esp (light) | Bloodrush.esp | Audio - Core | active |
| 13 IVBOS dummy esps (light, no masters) | chained after Voiced Books of Skyrim.esp in FOMOD order | Audio - Core | active |

BSAs load in plugin order, so the IVBOS esps sit after the VBoS esp on purpose (IVBOS must overwrite VBoS, as its page says).

Full-plugin census after (MO2 closed, same method as the Holidays ledger of this morning): Main 200 · NSFW 209 · DEEEZ 233 ·
CS 243 · PBR 245 · PICTA 246 (of 254). This batch cost exactly 1 per profile (FollowerIdles.esp).

Verified: `place.py` VERIFY OK in all six profiles (plugins.txt / loadorder.txt lockstep, every new plugin exactly once,
every modlist name exactly once); head (Testing / FWMF / LOD outputs) and tail (Authoria - Outputs) of every profile untouched;
every active plugin resolves to a file in an enabled mod.

## Wayfarer script collision (real conflict, fixed)

Walk With Me and "Additional Traits for Biggie Traits" both ship `Scripts\Wayfarer.pex`. Walk With Me's is the native class its
DLL binds to (cannot be renamed). The trait's is a 5-line `activemagiceffect` script (disables fast travel while the map is open)
bound by one VMAD on MGEF `Traits_Wayfarer` with no properties. Walk With Me wins the file, so the trait would have silently broken.
Fix mod contents: a byte-patched copy of `Biggie Traits - Additional Traits.esp` (VMAD script name `Wayfarer` -> `WayfarBT`, equal
length), `Scripts\WayfarBT.pex` (class + source name patched, string table re-parsed OK), `Source\Scripts\WayfarBT.psc`, README.
No other plugin has the trait esp as a master. Other loose conflicts found by the scan: only root-level `LICENSE` files (harmless).

## Bottled Shaders 1.0.0 -> 1.0.4 (`[NoDelete] Bottled Shaders`)

Archive `Bottled Shaders 192816 1.0.4 2026-09-29T15-16Z FpnkHZjR4.7z` (428 files). Diff vs installed 1.0.0: 330 same, 74 changed,
24 added, 0 removed upstream. Done:

- Full 1.0.0 folder backup: `_backups/2026-09-30 - Bottled 1.0.0 pre-1.0.4` (414 files).
- 7 hand-edited SnowCover files kept live (Skyrim.dds + Tamriel / Markarth / Riften / Solitude / Whiterun / Windhelm jsons): the
  1.0.4 stock copies equal the `.bak-stock-bottled100` copies by md5, so upstream did not touch them.
- `Shaders/Effects11/ApplyVolumetricRaysPS.hlsl`: 1.0.4 stock already carries the `max(0.0, ...)` clamp on line 81. The new stock
  file is live and the local edit is retired (stale `.bak-stock-bottled100` removed; copy in the folder backup).
- `Shaders/Upscaling/*` + `Shaders/Features/Upscaling.ini` (20 files) parked again: `_backups/2026-09-30 - Bottled 1.0.4 Upscaling parked`.
- overwrite `SKSE/Plugins/CommunityShaders/SettingsDefault.json` and `overwrite/ShaderCache` moved aside as `.stale-bottled100-20260930`.
  SettingsUser.json and its Disable-at-Boot lock untouched.
- meta.ini version 1.0.4 + installationFile; `LOCAL-SHADER-EDITS.md` got a dated update section.
- Feature ini versions bumped: DynamicCubemaps 2-6-0, Effects11 1-0-1, ExponentialHeightFog 1-4-0, ExtendedMaterials 1-6-0,
  HDRDisplay 1-2-2, LightLimitFix 3-4-0, ScreenSpaceGI 4-3-0, Skin 0-2-1, SnowCover 1-3-0, TerrainShadows 1-3-0.

FIRST LAUNCH UNTESTED. Launch once, quit, then edit settings only inside full blocks (the settings ritual).

## Owed by the user

1. Pandora: tick "GP Offset Movement Animation" (Command Gestures) and run. Follower Idles' FNIS list is picked up automatically.
2. Launch once for the Bottled 1.0.4 shader recompile and settings regeneration.
