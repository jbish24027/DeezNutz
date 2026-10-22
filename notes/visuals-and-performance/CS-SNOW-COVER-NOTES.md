# CS Snow Cover — realtime snow accumulation and melting

Investigated 2026-08-17. Read-only. Nothing changed yet.

Symptom reported: snow does not melt around a lit campfire, and a fire spell cast at
snowy ground leaves scorch decals but no cleared snow.

---

## 1. What the system is

The feature is **Snow Cover**, a Community Shaders feature. It is not a separate mod.

Provider (uncontested, no other mod ships or overrides any of its files):

    C:\1. AUTHORIA\mods\[NoDelete] Community Shaders AIO\
        Shaders\Features\SnowCover.ini            (Version = 1-1-1)
        Shaders\SnowCover\SnowCover.hlsli         (the shader math)
        Shaders\SnowCover\Skyrim.dds              (snow-line height map)
        Shaders\SnowCover\Tamriel.json            (per-worldspace config)
        Shaders\SnowCover\WhiterunWorld.json
        Shaders\SnowCover\WindhelmWorld.json
        Shaders\SnowCover\MarkarthWorld.json
        Shaders\SnowCover\RiftenWorld.json
        Shaders\SnowCover\SolitudeWorld.json
        Shaders\SnowCover\whitelist.txt / blacklist.txt
        Shaders\SnowCover\default\main.dds, main_n.dds, main_rmaos.dds

AIO build: CS Discord dev build, `CommunityShaders_AIO-2026-08-09T15-51Z.7z`,
settings version `1-8-0-0`. Installed 2026-08-10 12:50.

User settings live in:

    C:\1. AUTHORIA\overwrite\SKSE\Plugins\CommunityShaders\SettingsUser.json

"Snow Cover" block (byte-identical to SettingsDefault.json — never customised):

    AffectHavok            0
    EnableExpensiveFoliage 1
    EnableFireMelt         1
    FireInnerScale         0.35
    FireMaxDistance        12288.0
    FireRadiusScale        3.0
    SnowHeightOffset       0.0

### How the snow amount is computed

From `SnowCover.hlsli`, `ApplySnowBase()`:

    env_mult = saturate( max( GetEnvironmentalMultiplier(p) + disp*5 , weatherMult ) ) - waterDist
    mult     = distMult * skylight * env_mult * smoothstep(minAngle, maxAngle, worldNormal.z)
    mult    *= GetFireAttenuation(p)          // line 133 (objects/landscape), line 104 (foliage)

where

    GetEnvironmentalMultiplier(p) = ( GetHeightMult(p) + SeasonalAltitude ) / BlendSmoothness
    GetHeightMult(p)              = p.z - SnowHeightOffset + (SnowMap.Sample(uv) - 0.5) * MapZscale

So there are exactly **two** sources of snow, combined with `max()`:

1. **Altitude / season term** — ground above the current snow line gets snow.
   `SeasonalAltitude` is derived from `SummerHeightOffset` / `WinterHeightOffset`,
   lerped by the in-game month between `MaxWinterMonth` and `MaxSummerMonth`.
   Effective snow line = `SnowHeightOffset - SeasonalAltitude`.
2. **Weather term** — `weatherMult`, driven by `TimeSnowing`, an accumulator that
   rises while it is snowing and falls when it is not. `SnowingSpeed` and
   `MeltingSpeed` set the two rates.

Fire melt is **not** a third source. It is a final multiplier on the result.
If the result is already zero, the multiply does nothing.

### Tooltip text pulled from CommunityShaders.dll (authoritative)

    SummerHeightOffset  "What is the snow line altitude in summer?"
    WinterHeightOffset  "What is the snow line altitude in winter?"
    MaxSummerMonth      "In which month is the snow line highest?"
    MaxWinterMonth      "In which month is the snow line lowest?"
    MeltingSpeed        "How fast snow (under snow line) disappears when it is not snowing."
    EnableFireMelt      "Clears snow around campfires, torches and braziers."
    (fire detection)    "Fires are recognised as additive flame draws using fire-themed textures."
    FireRadiusScale     "Melt radius as a multiple of the flame's bounding radius."
    FireMaxDistance     "Fires beyond this camera distance are ignored. At most 16 fires are tracked."
    AffectHavok         "Moving objects (Havok rigidbodies) ... receive snow when they are not moving."
    (note)              "Seasonal and altitude snow is never distance-faded."

Hard-coded fire keyword list found in the DLL, adjacent to the Snow Cover settings block:

    ember   flame   fire   candle

A Snow Cover **Debug Info** readout exists in the CS menu. Format strings in the DLL:

    "SnowingDensity: %f"   "TimeSnowing: %f"   "Month: %f"   "Debug text: %s"

---

## 2. Root cause — CONFIRMED

**All six worldspace configs were hand-edited after install, and the edit switches the
altitude/season snow term completely off.**

Installed values (all six files identical on these two keys):

    SummerHeightOffset = 9999999.0
    WinterHeightOffset = 9999999.0

Shipped values, extracted from the original installer still on disk at
`C:\1. AUTHORIA\downloads\CommunityShaders_AIO-2026-08-09T15-51Z.7z`:

    SummerHeightOffset =  20000.0
    WinterHeightOffset = -20000.0

Timestamps in `...\Shaders\SnowCover\`:

    blacklist.txt      2026-08-10 12:50:21   (install)
    Skyrim.dds         2026-08-10 12:50:21   (install)
    SnowCover.hlsli    2026-08-10 12:50:21   (install)
    whitelist.txt      2026-08-10 12:50:21   (install)
    MarkarthWorld.json 2026-08-11 06:20:59   <-- edited
    RiftenWorld.json   2026-08-11 06:20:59   <-- edited
    SolitudeWorld.json 2026-08-11 06:20:59   <-- edited
    Tamriel.json       2026-08-11 06:20:59   <-- edited
    WhiterunWorld.json 2026-08-11 06:20:59   <-- edited
    WindhelmWorld.json 2026-08-11 06:20:59   <-- edited

No `.bak` was left for any of the six, unlike the other CS edits made that same day
(`SettingsUser.json.bak-pre-sdr-20260811`, `Astralite_GrassLighting.json.bak-pre-sss-test-20260811`,
`ApplyVolumetricRaysPS.hlsl.bak-pre-clamp-20260811`).

Effect: snow line sits at ~10,000,000 units in both summer and winter. Nothing in
Skyrim is anywhere near that. The altitude/season term therefore contributes nothing,
in every month, in every worldspace. `max()` always picks the weather term.

Consequence for the reported symptom: in clear weather there is **no Snow Cover snow on
the ground at all**, so there is nothing for a campfire to melt. The white ground in the
screenshots is the world's own snow — landscape textures, static snow meshes, and
whatever Seasons of Skyrim / Unfrozen paint. Fire melt cannot touch any of that; it only
scales the shader's own snow layer.

### The texture repoint in the same edit was CORRECT — do not revert it

The same 08-11 edit also changed, in all six files:

    MainTexture: textures/pbr/landscape/snow01           ->  Shaders/SnowCover/default/main
    AltTexture (Tamriel): textures/pbr/landscape/snow02  ->  Shaders/SnowCover/default/main
    AltTexture (cities): textures/pbr/landscape/frozenmarshice01 -> Shaders/SnowCover/default/main

Verified: **none of the three original texture paths exist in this build.** They are not
loose in `mods\`, and the AIO archive does not ship them (its only `textures\` content is
`textures\heightmaps\` and `textures\terrain\HeightMaps\`). This build has
`textures\landscape\snow01/snow02/frozenmarshice01.dds` from
`Vanaheimr - Landscapes - AIO - Complex Material`, but those are Complex Material, not
PBR, and Snow Cover wants a PBR set (diffuse + `_n` + `_rmaos`).

`Shaders\SnowCover\default\main*.dds` IS shipped by the AIO and is the intended fallback.
So the repoint fixed a genuinely broken reference. Leave it. It is cosmetic only — a
plain-looking snow rather than no snow.

### Other keys added to Tamriel.json in the same edit (additions, not corruption)

    ObjectFadeStart   6144.0
    ObjectFadeEnd     9192.0
    ObjectFadeAmount  0.5
    WeatherFadeStart  60000.0
    WeatherFadeEnd    150000.0
    AffectTreeTint    0 -> 1

Shipped `Tamriel.json` has 29 keys; the installed one has more. These look like a
deliberate tuning pass. Keep or drop as one set.

---

## 3. Ruled out — do not chase these

Every one of these was checked and cleared:

- Snow Cover failing to load. `CommunityShaders.log` (2026-08-17 15:13 session, the same
  session both screenshots came from) lines 148-150, 240, 363-365: feature loaded,
  `SnowCover.ini 1-1-1 successfully loaded`, `[SnowCover] Installed hooks`,
  `Installed version and cached version match`, `Cached feature is valid`.
  `C:\1. AUTHORIA\overwrite\ShaderCache\Info.ini` lines 210-212: `[SnowCover]` /
  `Enabled = true` / `Version = 1-1-1`.
- Shader compile errors. The log has 604 `[I]` and 29 `[W]` lines, zero `[E]`. No warning
  mentions SnowCover.
- The fire-melt master switch being off. `EnableFireMelt = 1` in the live SettingsUser.json.
- A mod overwriting CS files. Only one `SnowCover.ini` exists in `mods\`, in the enabled AIO.
  Only two `CommunityShaders.dll` exist; the second is in the DISABLED
  `[NoDelete] Community Shaders` (modlist line 54). No DLL in `overwrite\SKSE\Plugins`.
- A weather-mod override changing snow settings. The CS log shows exactly 5 overrides
  loaded, all from Astralite: CloudShadows, GrassLighting, Skylighting, SkySync,
  WetnessEffects. None for SnowCover.
- Effects11 being off. It loaded (`Effects11.ini 1-0-0`), hooked
  `Sky::SetDirectionalAmbientColors`, compiled and applied `enbbloom.fx`,
  `enbadaptation.fx`, `enbeffect.fx`, `enbeffectpostpass.fx`, and read the preset from
  `Stock Game\Data\enbseries.ini` (provided by `[NoDelete] Soul Core ENB - Data`,
  modlist line 3090, enabled). Its `[FIRE]` section is present at line 822.
  Note: the comment on `SnowCover.hlsli` line 47 says fire sources come from Effects11's
  FIRE classification. Disassembly during this investigation indicates the fire collector
  is Snow Cover's own render hook, not an Effects11 hand-off. Either way both are running.
- The disabled `[NoDelete] Effects 11` standalone mod. Irrelevant; Effects11 is bundled in
  the AIO.
- Better Dynamic Snow / Seasons of Skyrim overwriting the feature. They apply their own
  materials and swaps. They do not touch CS files. They do, however, mean the ground is
  often already white for reasons that have nothing to do with this feature.

---

## 4. Still unknown — needs a live check, cannot be read from disk

1. **The per-worldspace enable flag.** The DLL raises an internal `EnableSnowCover` flag
   only when a config is successfully matched to the current worldspace/cell. Its compiled
   default is off. It is not a config key and not saved to disk. Several code paths,
   including the fire collector and the per-frame update, early-out when it is off.
   Read it in the CS menu: Snow Cover -> `Enable Snow Cover`.
2. **Whether a campfire actually registers as a tracked fire.** The draw must be additive,
   carry two shader flags, be inside `FireMaxDistance`, have a bounding radius under a
   limit, and have a texture name containing `ember` / `flame` / `fire` / `candle`.
   The name test passes: the campfire mesh the game loads,
   `FYX - Campfire Reacts to the Wind - EmbersXD Edition\meshes\clutter\woodfires\campfire01landburning.nif`,
   uses `textures\EmbersHD\mx_fireatlas02.dds`. The shader-flag test can only be checked
   at runtime, via the tracked-fire count in the Snow Cover menu.
3. **Whether melting works once there IS feature snow.** It has never had any snow to act
   on in the frames we have.
4. **Who made the 08-11 edit, and whether it was deliberate.** Setting the snow line out of
   range is a coherent choice if the intent was "let Seasons of Skyrim own permanent snow,
   let CS Snow Cover do live snowfall only." There is no note or backup recording intent.

---

## 5. Fix options

### Option A — restore the shipped snow line (permanent snow above a line, plus weather)

In all six files under `C:\1. AUTHORIA\mods\[NoDelete] Community Shaders AIO\Shaders\SnowCover\`:

    SummerHeightOffset:  9999999.0 -> 20000.0
    WinterHeightOffset:  9999999.0 -> -20000.0

Leave `MainTexture` / `AltTexture` pointing at `Shaders/SnowCover/default/main`.

Result: high ground gets snow in summer; in winter the line drops to sea level and the
whole province gets a CS snow layer on top of the world's own snow. Campfires then carve
a visible ring. Biggest visual change; overlaps with Seasons of Skyrim's winter.

### Option B — keep weather-only, and verify it works

Change nothing. Confirm in game that snow builds during a snowstorm and recedes after,
and that a campfire clears a ring while that weather snow is present.

Result: matches "realtime accumulation and melting" literally. No permanent CS snow.
Nothing to melt in clear weather, which is by design under this config.

### Either way

No shader-cache clear is needed. These are runtime config values, not shader code.
`C:\1. AUTHORIA\overwrite\ShaderCache` only needs clearing if a `.hlsl` / `.hlsli` under
the AIO's `Shaders\` folder is edited.

MO2 must be closed before editing files in `mods\`.

---

## 6. DECISION — 2026-08-17

**Option B chosen by the user: keep snowfall-only. No config files changed.**

Nothing under `mods\[NoDelete] Community Shaders AIO\Shaders\SnowCover\` has been touched.
The 9999999 snow line stays. The snow-line half of the feature remains off by choice, and
Seasons of Skyrim keeps ownership of permanent seasonal snow.

Under this config the expected, CORRECT behaviour is:

- Clear weather, anywhere: the feature draws no snow. A campfire clears nothing. This is
  not a bug.
- During snowfall: snow builds over roughly 1-2 game hours, on upward-facing surfaces,
  on top of whatever the world already looks like.
- While that snowfall snow is present: a campfire, torch or brazier clears a ring in it.
- After snowfall stops: the snow recedes at `MeltingSpeed` (1.0), twice as fast in rain.

If the in-game test below shows any of those four not happening, the fault is real and is
one of the two unknowns in section 4.

---

## 7. In-game verification procedure

Keys, read from `SettingsUser.json` -> `Menu`:

    CS menu toggle       Shift + Enter      ("ToggleKey": [16, 13])
    Performance overlay  F10                ("OverlayToggleKey": 121)
    Effects11 toggle     Shift + Numpad *   ("Effects11ToggleKey": [16, 106])

Snowstorm weather for the console (winner is `Astralite ENB.esp`, override depth 5):

    SkyrimStormSnow          000C8221      fw 000C8221
    SkyrimStormSnowBlizzard  <Astralite ENB.esp 000826>

`fw` forces instantly and sticks. Release it afterwards with `sw` on a clear weather, or
by re-entering an interior.

### Exact Snow Cover menu labels (extracted from CommunityShaders.dll — these are real)

Settings section:

    "Melt Snow Near Fire"       -> EnableFireMelt          ("Clears snow around campfires, torches and braziers.")
    "Fire Melt Radius"          -> FireRadiusScale         ("Melt radius as a multiple of the flame's bounding radius.")
    "Fire Melt Softness"        -> FireInnerScale          ("Fraction of the radius that is fully clear.")
    "Fire Melt Max Distance"    -> FireMaxDistance         ("...At most 16 fires are tracked.")
    "Tracked fires: %u"         -> LIVE COUNTER, sits with the fire settings, NOT in Debug Info
    "Snow on Mobile Objects"    -> AffectHavok
    "Enable Nicer Foliage"      -> EnableExpensiveFoliage
    "Snow Offset"               -> SnowHeightOffset        ("Moves the altitude that snow appears at. For testing purposes.")

Worldspace Config section:

    "Config status: %s"
    "Current worldspace/cell: %s"
    "Each config applies to one worldspace or interior cell."
    "Saved config will be applied when you enter the worldspace."

Debug Info block — exactly three readouts, nothing else:

    "SnowingDensity: %f"   "TimeSnowing: %f"   "Month: %f"

Per-worldspace config section labels: "Weather and Seasons", "Material", "Snow Map".
Note the tooltip on Snowing speed: "How fast snowy weather accumulates snow.
**Also depends on the weather settings.**" — so `TimeSnowing` only climbs if CS classifies
the active weather as snowy. With Astralite / NAT / Helios weathers in play that
classification is worth confirming before blaming the fire path.

`Snow Offset` CANNOT rescue the snow line. Effective snow line =
`SnowHeightOffset - SeasonalAltitude` = `SnowHeightOffset + 9999999`, so it would need
about -10,000,000 to reach ground level. It is a fine-tuning slider, not a fix.

### 2026-08-17 second observation from the user

Reported: `Month: 1`, still no melt at the campfire and none from flame spells.
Screenshots show visible snowfall and fully white ground.

Month 1 is a WINTER month. `po3_SeasonsOfSkyrim.ini` maps Morning Star = 1 (winter) and
Sun's Dawn = 1 (winter), Season Type = 5 (seasonal). So Seasons of Skyrim is in winter and
has swapped the whole province to snow variants.

**This makes the melt ring invisible even if every part of the feature works.** Snow Cover
paints its own snow on top of ground that Seasons has already made white. Clearing that
layer near a fire reveals... more white. There is no colour underneath to expose.

So a winter month at a snowy settlement is the worst possible place to test this. It cannot
produce a visible result either way.

Steps:

1. Stand outdoors on snowy ground. Press Shift+Enter, go to Snow Cover.
2. Confirm `Enable Snow Cover` is ON. If it is OFF while standing outdoors in Skyrim, the
   worldspace config is not being matched and that is the real fault — stop here and say so.
3. Toggle the feature off and on while watching the ground. Expected right now: nothing
   changes, because none of the visible snow belongs to this feature in clear weather.
4. Read the Debug Info block: `TimeSnowing`, `SnowingDensity`, `Month`. Expected in clear
   weather: `TimeSnowing` at or near zero.
5. Stand at a lit campfire and read the tracked-fire count. Above zero means fire detection
   works and the only missing piece was the snow itself. Zero at a lit campfire is the
   second unknown from section 4 and IS a real fault.
6. Console `fw 000C8221`, wait 1-2 game hours. Snow should build on flat upward surfaces.
   Toggle the feature off and on again — now the ground SHOULD visibly change.
7. With that snow present, walk back to the campfire. A cleared ring confirms fire melt.
8. Return the weather to clear and wait. The snow should recede on its own.

---

## 8. 2026-08-17 — ROOT CAUSE OF THE MISSING MELT: a bug in the CS build

User reading, standing at the lit Rorikstead campfire outside the Frostfruit Inn:

    Current worldspace/cell: Tamriel
    Config status: Loaded.
    Enable Snow Cover     [ticked]
    Melt Snow Near Fire   [ticked]
    Fire Melt Radius      3.0x
    Fire Melt Softness    0.35
    Fire Melt Max Distance 12288
    Tracked fires: 0
    Month: 1

Flames cast from the hand also produce no melt. So nothing at all registers as a fire.

### The defect

Binary: `mods\[NoDelete] Community Shaders AIO\SKSE\Plugins\CommunityShaders.dll`
(md5 a9cd79c4022a6ba9e3e0e79563cc8b07, modlist line 39, the only enabled copy; the shipped
`CommunityShaders.pdb` matches it — RSDS GUID BABB750E-FE75-4C9C-8A2C-81E332DAB355, age 1).
Image base 0x180000000. Upstream: github.com/community-shaders/skyrim-community-shaders,
commit 3cb762e ("Bottled Shaders", author InTheBottle).

`SnowCover::FireSource` (from the PDB type stream) is:

    +0x00  position      NiPoint3
    +0x0C  radius        float
    +0x10  strength      float
    +0x14  lastSeenTick  uint32

`SnowCover::CheckFireSource` (RVA 0x4CD4F0) writes `strength` as a LITERAL ZERO on every path
that creates or replaces an entry, and never writes it anywhere else:

    0x1804cd773  movss dword ptr [rsp+0x3c], xmm7   ; radius = worldBound radius * FireRadiusScale
    0x1804cd779  mov   dword ptr [rsp+0x40], 0      ; strength = 0      <-- append path
    0x1804cd781  mov   eax, dword ptr [rip+...]     ; fireTick
    0x1804cd787  mov   dword ptr [rsp+0x44], eax    ; lastSeenTick
    ...
    0x1804cd82f  movss dword ptr [rax+0x0c], xmm7   ; radius
    0x1804cd834  mov   dword ptr [rax+0x10], 0      ; strength = 0      <-- evict-weakest path

The merge path at 0x1804cd7B4 only maxes `radius` at +0x0C and stamps `lastSeenTick` at +0x14.
Nothing in the image ever writes a non-zero value to +0x10.

`SnowCover::GetCommonBufferData` (RVA 0x4CFEA0) then filters the list into the GPU buffer:

    0x1804d028c  mov    dword ptr [rip+0xf03cea], 0   ; FireCount = 0        (RVA 0x13D3F80)
    ...
    0x1804d0359  movss  xmm6, dword ptr [rbx+0x10]    ; strength
    0x1804d035e  mulss  xmm6, dword ptr [rbx+0x0c]    ; * radius
    0x1804d0363  comiss xmm6, xmm8                    ; xmm8 = 1.0f
    0x1804d0367  jb     0x1804d03bb                   ; FAILS -> entry skipped, edi NOT incremented
    ...
    0x1804d03af  movss  dword ptr [r14+rcx*8+0x1dc], xmm6  ; the shader's fire.w = strength*radius
    0x1804d03b9  inc    edi
    0x1804d03c4  mov    dword ptr [rip+0xf03bb6], edi ; FireCount = survivors  (RVA 0x13D3F80)

`strength` is always 0, so `strength * radius` is always 0, so `comiss 0.0, 1.0` always takes the
`jb`, so `edi` never increments, so `FireCount` is written as 0 every frame.

`Tracked fires:` prints exactly that post-filter number: `DrawSettings` (RVA 0x4CD870) does
`mov edx, dword ptr [rsi+0x1c0]` where SnowCover+0x100 = perFrame and PerFrame+0xC0 = FireCount.

**Conclusion: no fire can ever be counted in this build, for anyone, under any settings.**
It is unconditional and independent of meshes, weather, season, the snow line, ParallaxGen,
Embers XD, Effects11 and Light Limit Fix. `fire.w` reaching the shader would also be 0 even if the
count were forced, so `GetFireAttenuation` could not produce a ring anyway.

### Everything else checked out

- All seven live Snow Cover settings are correct. `EnableFireMelt` (settings+0x10 = RVA 0x13D3E20) = 1
  and `EnableSnowCover` (SnowCover+0x70 = RVA 0x13D3E30) = 1. Both gates at the top of
  CheckFireSource pass. Menu-offset mapping proved from DrawSettings: Enable Nicer Foliage
  [rsi+0x50], Snow on Mobile Objects [rsi+0x58], Melt Snow Near Fire [rsi+0x60],
  Enable Snow Cover [rsi+0x70]; singleton base RVA 0x13D3DC0.
- ParallaxGen changed exactly ONE shape in the winning campfire mesh — the ground "Dirt" shape.
  Every fire, glow and smoke shape in `Authoria - PG Output\meshes\clutter\woodfires\campfire01landburning.nif`
  is field-for-field identical to the FYX source. Not a mesh problem.
- The keyword test would have passed. The matcher is a lambda at RVA 0x4CD400: case-insensitive
  substring search over a 4-entry `string_view` table at RVA 0x709100 = {"fire","flame","ember","candle"},
  run against the effect material's base texture path and then its second texture path. The flame
  uses `textures\EmbersHD\mx_fireatlas02.dds`, which contains "fire".
- No global CS switch is off. Light Limit Fix `EnableParticleLights` = true, Replace Original
  Shaders Effect/Particle = true, zero [E] lines in the CS log.

### A probable SECOND gate, behind the first

CheckFireSource also requires, at 0x1804cd565:

    and esi, 0x80400 ; cmp esi, 0x80400 ; jne exit

From the PDB type stream, `SIE::ShaderCache::EffectShaderFlags` gives AddBlend = 0x400 and
GrayscaleToColor = 0x80000. So a draw must be BOTH additively blended AND using the old
greyscale-texture-plus-palette path. Vanilla Skyrim fire is built that way. Embers XD flames use
full-colour atlas textures. So even with the strength bug fixed, Embers XD campfires may still not
register. NOT independently confirmed at the mesh level here — flag it in any upstream report.

### What can be done

Nothing from config. There is no setting, ini, mesh edit or load-order change that makes a
zero-strength fire pass a `>= 1.0` filter. The fix is a one-line change in `SnowCover.cpp` upstream.
Options: report it to the Bottled Shaders author, or wait for a newer AIO build and re-test with the
`Tracked fires` counter.

Re-test after any CS update: stand at a lit campfire, open Snow Cover, read `Tracked fires`.
Above zero means the build is fixed.


---

## 9. 2026-08-17 — SECTION 8 IS RETRACTED. The DLL is not broken.

The user has seen fire melt work in this build. That is the hypothesis, and it survives.

Section 8's "strength is never raised" claim rested on "SnowCover::Reset is never called".
That came from a direct-call scan. `Reset` is a VIRTUAL override; `State::Reset` (RVA 0x5DC300)
calls every loaded feature's Reset through the vtable at `0x1805dc39c call [rax+0xa0]`, once per
frame. `SnowCover::Reset` (RVA 0x4C8B00) does exactly the fade the design implies:

    fireTick++
    for each FireSource:
        seen within 4 ticks -> target 1.0, rate 1.6/sec   (0x1804c8bb5..0x1804c8be4)
        else                -> target 0.0, rate 0.02/sec
        strength moves toward target by rate * dt          (0x1804c8bec..0x1804c8c0c)
    erase entries with strength <= 0 that are stale        (0x1804c8c2d..0x1804c8cb0)

So any fire that gets INTO the list is counted within a fraction of a second. Section 8's
"structural zero" is wrong. Everything downstream of that in section 8 is withdrawn.

### The real gate, correctly read

The hooked thunk (`SnowCover::Hooks::BSEffectShader_SetupGeometry::thunk`, RVA 0x4C7530) reads
`globals::state->currentPixelDescriptor` (State+0x3C, confirmed from the PDB type stream) — the
RAW game technique for the current effect-shader draw — and requires:

    bit 10  AddBlend            (0x400)      additive draw
    bit 19  GrayscaleToColor    (0x80000)    greyscale flame texture coloured by a palette/gradient

then the RTTI check (BSEffectShaderProperty exactly), then the keyword test on the source texture
path OR the greyscale texture path (case-insensitive substring of fire/flame/ember/candle), then
bound radius in (0, 512], then camera distance <= FireMaxDistance.

`GrayscaleToColor` comes from the mesh's **BSEffectShaderProperty shaderFlags1 bit 4 (0x10)**
= SLSF1_Greyscale_To_PaletteColor. (My earlier "bit 28" was wrong; bit 28 is Parallax_Occlusion.)

### What qualifies in THIS build (flags read from the winning meshes)

    Flames spell  Flame VFX Edit (KittyVFX 1.23) meshes\magic\firesprayfx01.nif
                  sf1 0xc0000010 / 0x80000078 / 0xc0000030 -> bit 4 SET,
                  gradients\GradFlame01.dds assigned, names contain fire/flame  -> QUALIFIES

    Embers XD campfire / logs flames  (3.1.9 AND 3.2.6, FYX, PG Output — all identical here)
                  sf1 0x80000000 / 0xc0000000 / 0xc0000008 -> bit 4 CLEAR, full-colour atlas
                  mx_fireatlas02.dds, no palette                               -> NEVER qualifies

    Candle Flame VFX Edit  meshes\mps\mpscandleflame01.nif  sf1 0x80000000     -> does not qualify

`Tracked fires: 0` at the Rorikstead campfire is therefore correct behaviour for an Embers XD
flame, on any version of Embers XD, and always has been. It is not evidence of a broken detector.

### So what changed between "it worked" and now

1. The 2026-08-11 snow-line edit (section 2). With the shipped snow line, in a winter-ish month the
   whole province carried a CS snow layer, so every recognised fire (the Flames spell, any
   vanilla-flame fire) carved a visible ring. With the snow line at 9999999 there is NO CS snow
   outside active snowfall, so there is nothing to melt, anywhere, in clear weather. This is the
   most likely reason "melting stopped".
2. Nothing on the fire side changed. Embers campfires never registered; the spell still should.

### Fix paths

A. Restore the snow line (section 5, Option A). Required for melt to be visible in normal play.
   The user's 08-17 "keep snowfall-only" choice was made without this consequence being proven.
B. Make campfires register. Two routes:
   B1. Content: switch Embers XD's flame style to "Vanilla Flames" (FOMOD step "Flames And
       Lights Customization" -> group "Flames Style"). Also swap FYX to its vanilla-flames edition
       (installed one is "FYX - CRTTW - 1 EmbersXD Flames") and remove/redo the ParallaxGen copies
       of the campfire meshes in "Authoria - PG Output", or they keep re-asserting Embers flames.
       Changes the look of every fire. Embers 3.2.6 archive is no longer in downloads.
   B2. Upstream: ask the Bottled Shaders author to drop the GrayscaleToColor requirement in
       SnowCover's fire test — AddBlend + keyword already identify flames; the palette requirement
       excludes every full-colour flame replacer (Embers XD, Inferno, etc.).

### The decisive live check (30 seconds)

Cast Flames for ~3 seconds, then open the CS menu -> Snow Cover and read `Tracked fires`.
Fires linger in the list after they stop being drawn (strength decays at 0.02/sec), so the count
stays > 0 long enough to read. > 0 proves detection works and the campfire is purely the
Embers-flame limitation. 0 means something else and I keep digging.


### 2026-08-17 live result: `Tracked fires: 4` with the Flames spell equipped/cast (Heljarchen area).
Detector CONFIRMED working. No visible melt because there is no CS snow layer to melt (snow line
at 9999999 => no CS snow outside active snowfall). Remaining fix is the snow line, nothing else.
Live no-file-edit route: Snow Cover panel -> Worldspace Config -> "Weather and Seasons" ->
Summer Height Offset 20000, Winter Height Offset -20000 (slider clamps to +/-20000), then Save.


## 10. 2026-08-17 — RESOLVED IN GAME. The feature works end to end.

Live sequence at Lemkil's Farm / Rorikstead, Month 1.55 (Seasons WINTER), TimeSnowing 0:
1. Panel: Summer/Winter Height Offset both -20000, Snow Map Z Scale 0.1 -> SeasonalAltitude = +20000
   in every month (DLL: SeasonalAltitude = -lerp(offsetA, offsetB, monthFrac), GetCommonBufferData
   0x1804d0265..0x1804d0284) -> layer saturates on every upward surface.
2. Material -> Main Tint red: ENTIRE world red. Layer confirmed drawing. White = decals only
   (footprints, scorch) which are blacklisted (blacklist.txt "Decal").
3. Fire Melt Radius max + Flames cast: large soft-edged CLEARED circle around the player, red only
   survives beyond ~1024 units. FIRE MELT CONFIRMED (radius = min(bound*scale, 1024), inner = 0.35*r).
4. User observation: "red goes away but the white snow stays underneath" = Seasons of Skyrim's
   winter landscape/static swaps. Snow Cover melts ONLY its own layer. In Seasons winter months
   (Evening Star, Morning Star, Sun's Dawn = 12,1,2 per po3_SeasonsOfSkyrim.ini) melt is white-on-white.

Why the default looked dead: (a) snow line at 9999999 => no layer to melt outside snowfall;
(b) Embers XD flames never qualify (no palette flag) => campfires read Tracked fires 0;
(c) Flames spell's qualifying pieces are hand-sized => 3x radius = a circle up at the hands.

Embers XD flame styles tested from the 3.1.9 archive (assets\core\meshes\<style>\...campfire01landburning.nif):
    ehd      (Embers HD Flames)  QUALIFIES  (5 of 7 flame shapes palette-flagged)
    vanilla  (Vanilla Flames)    QUALIFIES
    inferno  (Inferno Flames)    QUALIFIES  (needs Inferno)
    new (XD default) / orange / yellow      NO
=> "Embers HD Flames" keeps an Embers-family look AND registers. FYX (line 347) and PG Output
   (line 36) copies of campfire meshes still override with XD flames and must be swapped/redone.

To SEE melt in normal play the ground under the layer must not already be white:
  - non-winter Seasons months with CS snow present (shoulder months, or snowfall), or
  - console `set gamemonth to 4`, enter/exit an interior so Seasons re-evaluates, then test, or
  - po3_SeasonsOfSkyrim.ini [Winter] Skip Land Textures = true (let CS own ground snow in winter;
    look trade-off: CS default snow texture is a flat placeholder).

Open decisions for the user: restore snow line (shipped 20000/-20000, Z scale 75000 = regional
mask; tune) — flame style switch for campfires (Embers HD) — Seasons winter land textures.


---

## 11. 2026-08-18 — DISTANT GREEN GRASS IN WINTER (separate from Snow Cover). FIXED (fix 1).

Symptom: in Seasons winter, grass beyond a fixed distance is summer-green in every direction; near grass is
correct winter grass. Not CS (all CS grass features off = no change). Not a texture patch. Not LOD.

Cause: two grass loaders. Inside the loaded cell grid the vanilla loader runs and Grass Cache Helper NG 1.0.1
(`mods\Grass Cache Helper NG\SKSE\Plugins\GrassCacheHelperNG.dll`, hook at RVA 0x1F960) rewrites the request to
`<cell>.WIN.cgid` (no fallback). Beyond the grid, NGIO-NG 1.6.8's extended-distance subsystem
(`GrassControl::DistantGrass::*`, `cell_info::checkHasFile`, `UpdateGrassGridNow_LoadOnly`, own
`Data/Grass/` path builder) loads the plain `<cell>.cgid` = the DEFAULT cache generated with seasons off =
summer-green tundra. NGIO-NG contains no season strings/API use in any version through 1.6.10 (changelog checked).
GCH's page: NGIO "would overwrite the hooks of this mod".

Fix applied 2026-08-18 11:49 (MO2 closed, verified no MO2/game process):
  `mods\Authoria - MCM and INI Settings\SKSE\Plugins\GrassControl.ini`
      Extend-grass-distance = true  ->  false     (line 53; CRLF preserved)
  backup: GrassControl.ini.bak-extend-off-20260818 (byte-identical original).
  DynDOLOD-Grass-Mode left 0, Only-load-from-cache true, Overwrite-grass-distance 100000 (= no fade to grid edge).
Far grass now = DynDOLOD seasonal grass LOD (GrassLODMode 1, density 30, generated 2026-07-20/27 with the
seasonal caches present; per-season LOD grass textures exist in the DynDOLOD output).

Alternatives not taken: per-season plain-named cache mods (feed NGIO DistantGrass the right files);
NGIO-NG feature request (make DistantGrass query the Seasons API for the suffix).

Still open (separate): winter grass cache 5010/8184 Tamriel cells (autumn 6293/8184); holes = bare near grass
in winter/autumn and no LOD grass there. Fix = Updating-Cache=true precache passes (Season Type 1 then 4)
+ DynDOLOD rerun. Isolated green PATCHES (a land texture with no winter swap) — audit workflow wf_462638f4 running.


## 12. 2026-08-18 — THE GREEN FAR GRASS IN WINTER IS DYNDOLOD GRASS LOD. Root cause found.

User: "it's still there. it is happening like almost right on the beginning edge of where dyndolod takes over."
That is the diagnosis and it is correct.

PROOF (both from the 2026-07-20 DynDOLOD run, tools\DynDOLOD):
1. The Tamriel grass-LOD billboard map `Edit Scripts\Export\LODGen_SSE_Grass_Map_Tamriel.txt` has 61 entries and
   there is exactly ONE per worldspace — no `_WIN` / `_SPR` / `_SUM` / `_AUT` variant exists. The WIN export
   (`LODGen_SSE_Export_Tamriel_WIN.txt`) points at that SAME file: `GrassMap=...LODGen_SSE_Grass_Map_Tamriel.txt`.
   (Its AltTextures and VC lines ARE seasonal: `..._WIN.txt`. Grass is not.)
2. All 61 billboards are green/brown/dry vegetation. ZERO snow or winter grass:
   Field_Green x4, Grass_Green, Grass_Green_Brush, Grass_Green_Marsh, Fern_Green x2, Shrub_Berry_Green x2,
   Flower_Lupine_Blue, Flower_Dandelion, Flower_Paintbrush, Weed_Green, Field_Dry, Grass_Brown, ... and no snowgrass.
3. `grep -c "WIN\.cgid"` over the 869 MB `Logs\DynDOLOD_SSE_Debug_log.txt` = **0**. DynDOLOD never read a single
   seasonal grass cache file. It read the base `.cgid` (the DEFAULT/summer cache) for every season pass.

=> The grass baked into the LOD meshes is SUMMER grass in every season, including the `.WIN.bto` tiles.
   Winter BTOs differ from default only in object/tree swaps, not grass.
   This is why it starts exactly at the LOD boundary, and why it is green rather than bare.

Why the earlier fix did not solve it: turning off NGIO `Extend-grass-distance` removed a SECOND green source
(NGIO's DistantGrass reading the default cache) and exposed this one at the LOD boundary. The setting change is
still correct and stays; it just was not the whole story.

NOTE this also re-frames the grass-cache gaps: a MISSING cache file yields BARE ground, never green grass.
The gaps were never the cause of the green. (User made this point; they were right.)

OPTIONS (none applied):
A. Regenerate DynDOLOD grass LOD seasonally — needs seasonal grass caches actually consumed by DynDOLOD AND
   snow-grass billboards in the map. Biggest job; also depends on completing the winter/autumn caches, and the
   partial-regen route failed (see [[grass-cache-partial-regen-method]]).
B. Regenerate DynDOLOD with grass LOD OFF — no far grass in any season. Consistent, no green in winter, less lush
   summer distance.
C. Strip grass shapes from only the `*.WIN.bto` / `*.AUT.bto` tiles — surgical, no regeneration, winter distance
   becomes bare snow terrain LOD (arguably correct-looking) while summer keeps its grass LOD. Untested; mesh surgery.
D. Accept it.

### 2026-08-18 — Option C (strip grass from *.WIN.bto) ATTEMPTED AND REVERTED: IT CRASHES THE GAME

Method tried: in each level-4 `*.WIN.bto`, set the root NiNode children[] entries that point at the
`grasspassthru` BSMultiBoundNode groups to -1 (null link). Length-preserving, no renumbering.
Applied to 618 tiles / 2919 grass groups / 5.51 GB of geometry unlinked. Every file re-parsed cleanly
(header, block table, footer) and all non-grass shapes survived — i.e. it was VALID NIF.

**The game crashed on launch.** Skyrim's object-LOD loader walks the root children array without
null-checking, so a None entry is fatal. Valid NIF != accepted by the LOD renderer.

REVERTED in full from `D:\AUTHORIA-DynDOLOD-WIN-BTO-Backup-20260818` (618 files, 0 size mismatches,
2919 grass groups relinked, 0 null refs remaining). User confirmed the game launches fine.

LESSON (same one as the grass-cache pilots, third time today): structural validation is not behavioural
validation. Prove ONE tile IN GAME before scaling.

If retried, the ONLY viable form is a true block removal: drop the grass BSMultiBoundNode/BSSubIndexTriShape
(and any blocks referenced solely by them — texture sets ARE shared, 10 sets for 21 shapes, so reference
analysis is required), shrink numChildren, and renumber every block reference in the file. Then test one
tile in game before the second.

### 2026-08-18 — WINTER LOD GRASS STRIP: DONE AND CONFIRMED GOOD IN GAME

Working method (replaces the crashing null-link attempt): in each level-4 `*.WIN.bto`, REMOVE the
`grasspassthru` entries from the root NiNode children[] array, decrement numChildren, and update that block's
entry in the block-size table. Block indices are unchanged, so NO renumbering is needed. Grass blocks remain in
the file as unreferenced data (harmless, keeps file size ~identical, keeps the edit trivially reversible).
Script: scratchpad `btotest\strip2.py` (`parse` / `children_span` / `grass_slots` / `strip`), re-validates the
rebuilt file before writing.

Applied: 618 winter level-4 tiles, 2919 grass groups removed. Verified afterwards across all 732 winter tiles:
0 grass still linked, 0 null refs, 0 structural failures. Backup of every original:
`D:\AUTHORIA-DynDOLOD-WIN-BTO-Backup-20260818`.

Tested one tile in game FIRST (Tamriel.4.-28.4) -> no crash; then scaled. User verdict after the full batch:
"WAAAAY better", summer also checked and fine.

AUTUMN NOT DONE (deliberate - its LOD grass is greenish-brown and reads acceptably).
WARNING: this edit lives in the DynDOLOD output. A DynDOLOD re-run WIPES it. Re-apply strip2.py afterwards.
