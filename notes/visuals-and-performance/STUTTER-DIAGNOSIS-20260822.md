# Stutter diagnosis - 2026-08-22

Profile: DEEZ CS NUTZ. Session examined: 13:26 -> 14:53 (~85 min).
Hardware: RTX 5090, i9-14900K, 64 GB RAM. Output 3840x2160.
Nothing was changed by this investigation. Read-only.

---

## 1. Frame pacing - Frame Generation blocks Reflex, and three limiters disagree

### Evidence

`CommunityShaders.log`, this session:

    [13:27:23.398] [Streamline] sl.reflex.dll version: 2.10.3
    [13:27:23.901] [FidelityFX] amd_fidelityfx_framegeneration_dx12.dll version: 4.0.1
    [13:27:23.909] [Frame Generation] Frame Generation enabled, using D3D12 proxy
    [13:27:24.811] [Streamline] Reflex is available

CS's own menu strings (`Translations/en.json`):

    feature.upscaling.frame_generation_available => AMD FSR Frame Generation is available.
    feature.upscaling.frame_generation_tech      => Uses AMD FSR Frame Generation technology
    feature.upscaling.frame_generation_proxy_note=> Requires a D3D11 to D3D12 proxy which can
                                                    create compatibility issues
    feature.upscaling.reflex_blocked_by_fg       => Reflex is unavailable while the DX12
                                                    frame-generation swapchain is active.

So this CS build has no DLSS Frame Generation. FG is AMD FSR only, and enabling it
forcibly disables Reflex. Reflex loads and reports available, then goes unused.

`overwrite\SKSE\Plugins\CommunityShaders\SettingsUser.json` -> `Upscaling`:

| Key                      | Value | Meaning                          |
|--------------------------|-------|----------------------------------|
| frameGenerationMode      | 1     | FG ON                            |
| upscaleMethod            | 3     | DLSS                             |
| qualityMode              | 1     | (preset)                         |
| reflexLowLatencyMode     | False | Reflex off (blocked by FG)       |
| reflexLowLatencyBoost    | False | off                              |
| reflexUseFPSLimit        | False | CS frame cap NOT applied         |
| reflexFPSLimit           | 60.0  | cap configured but inactive      |
| frameLimitMode           | 1     | VRR limit mode                   |
| frameGenerationAllowInMenus | False |                               |

### The three-way disagreement

| Source                | VSync | Frame cap | Notes                              |
|-----------------------|-------|-----------|------------------------------------|
| SSE Display Tweaks    | true  | 240       | Borderless, MaxFrameLatency 0      |
| SkyrimPrefs.ini       | off   | -         | `iVSyncPresentInterval = 0`        |
| Community Shaders     | -     | none live | 60 stored, `reflexUseFPSLimit` off |

Two copies of `SSEDisplayTweaks.ini` exist; both carry the same values, so the
VFS winner does not change the outcome:

    mods\Authoria - MCM and INI Settings\SKSE\Plugins\   (modlist line 176, wins)
    mods\SSE Display Tweaks\SKSE\Plugins\                (modlist line 4086)

Display Tweaks' VSync and 240 cap target the original D3D11 present path. FG
installs a D3D11->D3D12 proxy swapchain and presents through that instead. The
limiter and the presenter are no longer the same object.

### Why this reads as "stuttery" and not "slow"

On a 5090 at 4K the frame *rate* is high. With FG interpolating, Reflex absent,
VSync disagreeing between two sources and no live cap, the frame *spacing* is
uneven. High FPS + uneven delivery is exactly the "feels stuttery" signature.

### Options

1. Turn FG off. Reflex becomes usable again. Simplest test of the theory.
2. Keep FG on, but make one thing own presentation: set the CS FPS Limit on
   (2-3 below refresh, per CS's own tooltip) and set Display Tweaks
   `EnableVSync = false` + `FramerateLimit = 0`.
3. Keep FG on and let Display Tweaks own it: leave its VSync/cap, leave CS's
   limiter off. Weaker - Display Tweaks is not hooking the presenting swapchain.

Option 1 first, because it is one toggle and it isolates the cause.

---

## 2. Papyrus VM overload - Rite of Arcana, plus logging left on

### Evidence

`Papyrus.0.log` for this session: 55,407 lines / 3.7 MB.

Nine "Suspended stack count is over our warning threshold" events:

    01:48:00PM  01:49:47PM  01:50:53PM  01:52:07PM  (+5 more)

Each one freezes the VM and writes its whole suspended queue to disk
synchronously. That is a visible hitch every time.

Summed event frequency across all nine dumps:

| Stuck jobs | Dumps | Source                                  |
|-----------:|------:|-----------------------------------------|
|       3984 |     9 | `roa_refaliasscript.OnMagicEffectApply` |
|        115 |     7 | `critterspawn.OnUpdate`                 |
|         43 |     9 | `roa_refaliasscript.OnSpellCast`         |
|         12 |     6 | `roa_refaliasscript.OnObjectUnequipped`  |
|          5 |     3 | `_Frost_BaseSystem.OnUpdate`            |
|     (rest) |       | single digits                           |

Rite of Arcana is 4,039 of ~4,200 - about 95%. Peak was 270 queued
`OnMagicEffectApply` calls in one dump window.

### Mechanism

`ROA_RefAliasScript` is attached to the Player alias on `ROA_ArcanaMainQuest`.
In the `ActiveWatching` state it forwards every magic effect applied to the
player:

    State ActiveWatching
        Event OnMagicEffectApply(ObjectReference akCaster, MagicEffect akEffect)
            ROA_ForwardMagicEffectApply(akCaster, akEffect)
        EndEvent

    Function ROA_ForwardMagicEffectApply(ObjectReference akCaster, MagicEffect akEffect)
        ROA_QuestScript brain = GetBrain()
        if brain == None
            ...
            return
        endif
        if !brain.ROA_IsRitualRunning()
            return
        endif
        ...
        brain.ROA_AliasSyncPlayer(GetActorReference())
        brain.ROA_HandleMagicEffectApply(akCaster, akEffect)
    EndFunction

The early-out on `ROA_IsRitualRunning()` is cheap, but it runs *after* the VM
has already created and queued a stack for the event. In a Requiem load order
the player receives magic effects continuously, so the queue grows regardless
of whether a ritual is active. The dumps show frame count 0 and state
"Waiting on other stack for call" - these are queued, not executing.

Note the `Active` (auto) state declares the same event empty. Declaring it at
all still subscribes the alias; an empty handler still costs a dispatch.

Rite of Arcana was installed 2026-08-19 and is still marked test-pending in
`RITE-OF-ARCANA-INSTALL-PLAN.md`.

### Papyrus logging is fully on

`profiles\DEEZ CS NUTZ\Skyrim.ini`:

    [Papyrus]
    bEnableLogging=1
    bEnableTrace=1
    bLoadDebugInformation=1
    bEnableProfiling=0
    fPostLoadUpdateTimeMS=2000
    iMaxAllocatedMemoryBytes=500000

Enabled for diagnostics on 08-16 and again 08-21; never turned back off.
Backups confirming this sit beside it:

    Skyrim.ini.bak-pre-papyruslog-20260816
    Skyrim.ini.bak-playerdirt-log-20260821

`bLoadDebugInformation=1` is what makes each stack dump write full script names
and line info. Turning the three off does not fix the ROA subscription, but it
removes the disk-write cost of every dump.

---

## 3. Grass cache is in runtime-update mode, with holes in two seasons

### Evidence

`mods\Authoria - MCM and INI Settings\SKSE\Plugins\GrassControl.ini`:

    Use-grass-cache      = true
    Only-load-from-cache = true
    Updating-Cache       = true      <-- leftover from the partial regen
    Extend-grass-distance = true
    Overwrite-grass-distance = 100000
    Overwrite-min-grass-size = 40
    DynDOLOD-Grass-Mode = 1

`NGIO-NG.log` this session confirms the mode is live:

    [13:28:22:788][info] Cache Updating Mode Enabled.

Per-season cache file counts:

| Season  | .cgid files | vs Default |
|---------|------------:|-----------:|
| Default |      20,925 |          - |
| Spring  |      20,922 |         -3 |
| Summer  |      20,900 |        -25 |
| Autumn  |      17,135 |     -3,790 |
| Winter  |      14,950 |     -5,975 |

With `Updating-Cache = true`, a cell with no `.cgid` has its grass built at
runtime on entry, which hitches. NGIO's own docs list this as the expected cost.

### But it did not fire last session

`overwrite\Grass\` is empty, last touched 2026-08-21 16:16. No cache files were
written during the 13:26-14:53 session, so every cell visited was already
cached. This is a landmine for Autumn/Winter travel, not the current driver.

Caveat: some of the Autumn/Winter shortfall is legitimate - cells whose grass is
swapped out seasonally produce no `.cgid`. The gap has not been proven to be all
missing work.

---

## Checked and cleared

- **Shader cache is valid.** CS log: "Installed version and cached version
  match" x40, "Cached feature is valid" x40. No mass recompile this session.
  `ShaderCache\Info.ini` PluginVersion 1-8-0-0 matches the running build.
  New permutations were written mid-session (13:32, 13:33, 13:59, 14:22) but
  that is normal incremental compilation, not invalidation.
- **Screen Space GI: off.** `EnableGI False`, `Enabled False`. Still pinned as
  intended.
- **Screen Space Reflections: off.** `Enabled False`.
- **Light Limit Fix contact shadows: off.** `EnableContactShadows False`.
- **Unified Water: disabled at boot** (the Mirele change, 08-22).
- **Papyrus errors other than ROA** are ordinary modlist noise - highest single
  shape is 199 "Assigning None to a non-object variable".

## Worth noting, low impact

- 71 x `[Advanced Skin] SetupExtraTexture : No specular or normal texture found
  in texture set from material: <id>` this session. CS Skin feature, per-material.
  Not a pacing cost, but it is 71 real misses.
- CS `Advanced -> Compiler Threads = 30`, `Background Compiler Threads = 8`.
  30 is close to the 14900K's full thread count. With `Enable Async = True`
  in-game compiles use the background pool, so this mostly affects load-time
  bursts rather than gameplay.
- 9 x `[ENBEXTENDER] Include path escapes base directory` - the known Effects 11
  `#include` rejection, already recorded.
- `Parsec Virtual Display Adapter` is present as a second display adapter. Idle
  during this session as far as the logs show, but it is a capture/streaming
  surface worth ruling out if pacing work does not land.
