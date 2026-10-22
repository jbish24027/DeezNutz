# Flora colour — root cause found, 2026-08-19

Status: **root cause identified and verified on disk.** Not yet confirmed in game.
Investigation was evidence-only. Nothing was changed. Baseline from 2026-08-17 is untouched.

---

## 1. The answer in one paragraph

The renderer rewrites the colour of blue and purple flowers before it lights them.
It does this inside the Snow Cover feature.
Snow Cover converts a foliage pixel to hue, and if the hue is above 198 degrees it **doubles the hue and wraps it**.
Hues below 198 degrees pass through untouched.
Green leaves are below the line. Blue and purple petals are above it.
That is why one texture can have correct leaves and wrong flowers in the same draw call.

This is a bug in the shader. At zero snow the function is supposed to do nothing. The branch for hues below 198 correctly does nothing. The branch for hues above 198 does not.

---

## 2. Where it lives

File: `mods\[NoDelete] Community Shaders AIO\Shaders\SnowCover\SnowCover.hlsli`, lines 77-87.

```hlsl
void ApplyFoliageColor(inout float3 color, float env_mult)
{
    float gmult = saturate(env_mult - SharedData::snowCoverSettings.FoliageHeightOffset / 5000);
    float3 hsv = Color::RGBtoHSV(color);
    if (hsv.x > 0.55)
        hsv.x = frac(lerp(hsv.x, 1.1, gmult) * 2);   // <-- NOT identity at gmult 0
    else
        hsv.x = lerp(hsv.x, 0.1, gmult);             // <-- identity at gmult 0
    hsv.y *= lerp(1, 0.25, 4.0 * gmult * (1.0 - gmult));
    color = Color::HSVtoRGB(hsv);
}
```

`gmult` is 0 in this setup, because the snow line was pushed to infinity on 2026-08-11
(`WinterHeightOffset` and `SummerHeightOffset` are both 9999999 in the worldspace configs).

At `gmult = 0` the function reduces to:

- hue <= 0.55 (198 deg): unchanged.
- hue > 0.55 (198 deg): `frac(hue * 2)`.
- saturation: multiplied by exactly 1.0, i.e. unchanged.

It is called before the "no snow, return early" check, so it runs even when no snow is drawn.

### Call sites (all verified)

| Path | File | What it hits |
|---|---|---|
| Grass | `Shaders\RunGrass.hlsl:579-581` -> `ApplySnowFoliage` | witchy wilderness lupine and flax |
| Static flora / trees | `Shaders\Lighting.hlsl:2125-2126` (inside `#if defined(TREE_ANIM)`) | mountain flowers, nightshade, lavender |
| Tree LOD | `Shaders\DistantTree.hlsl:234-236` | distant billboards |

---

## 3. The per-worldspace switches — this is the Whiterun answer

`Shaders\SnowCover\*.json`, one per worldspace:

| Worldspace | AffectGrassTint | AffectTreeTint |
|---|---|---|
| Tamriel (the open world) | 1 | **1** |
| WhiterunWorld | 1 | **0** |
| MarkarthWorld | 1 | 0 |
| RiftenWorld | 1 | 0 |
| SolitudeWorld | 1 | 0 |
| WindhelmWorld | 1 | 0 |

Consequences:

1. Mountain flowers, nightshade and lavender are rewritten in the **open world only**. Inside the five walled cities they render exactly as painted.
2. Grass flowers are rewritten **everywhere**, cities included.

This resolves several things that were previously blamed on lighting:

- "Good in Morthal sun but pink/purple in Whiterun" was never a sun-versus-shade effect. Morthal is Tamriel, so the flowers are doubled to blue. Whiterun is its own worldspace, so the painted violet shows as painted violet.
- The 2026-08-16 measurement that concluded "hue transfer is essentially IDENTITY" was taken in Whiterun. Identity is the correct answer for Whiterun. That measurement was then used to retire the rotation model and repaint to azure, which was the regression.
- The 2026-08-17 note "nothing Whiterun-specific exists" was wrong. There is a Whiterun-specific config file.

---

## 4. The doubling reproduces the calibration history

Painted hue -> rendered hue is `frac(2h)` above 198 degrees.

| Painted | Predicted | Observed in game | Match |
|---|---|---|---|
| 205 azure | 50 yellow | "renders YELLOW" | yes |
| 239 true blue | 118 green | "more green now" / mint | yes |
| 270 violet, full sat | 180 cyan | "corner-violet test STILL rendered cyan" | yes |
| 288 violet | 216 blue | "natural blue", user approved | yes |
| 70-100 green leaves | unchanged | leaves always correct | yes |
| saturation | unchanged | rendered sat tracked painted sat | yes |

The "roughly minus 85 degrees" model was a straight-line fit to a doubling. That is why it never fit both the azure point and the violet point at the same time.

Two older data points do not fit: painted 300 and painted 304 were reported as rendering purple. Both were lavender readings. Worth re-measuring, in Tamriel, before trusting.

---

## 5. How it got here

- 2026-08-09: the weather and renderer swap. Official Community Shaders 1.8.3 and Effects 11 1.0.0 were installed.
- 2026-08-10: those four official mods were switched off and replaced with an unofficial all-in-one Discord dev build (`CommunityShaders_AIO-2026-08-09T15-51Z.7z`, mod folder `[NoDelete] Community Shaders AIO`, branded "Bottled Shaders").
- Snow Cover **does not exist in official Community Shaders 1.8.3.** It is one of 13 feature folders that exist only in the dev build.
- 2026-08-11: first flora colour complaint. Same day, the snow line was pushed to infinity, which pins `gmult` at 0 and puts the buggy branch in its identity-violating state.

Shader tree diff, official 1.8.3 versus the AIO: 146 files versus 238, 92 AIO-only, 35 differing.

---

## 6. Ruled out, with the reason

| Suspect | Verdict | Why |
|---|---|---|
| Astralite weather records | Excluded | A light colour multiplies. It can never change which channel is largest. The symptom requires exactly that. 347 daytime sunlight colours checked. |
| Imagespaces / tonemap white point | Excluded | A tonemap applies the same curve to all three channels, so channel order is preserved. Daytime tint and saturation are neutral. |
| Soul Core preset direct-light filters | Excluded | All 21 weather files read. Every direct-light colour filter is 1,1,1 with amount 0. |
| Effects 11 code | Excluded | 7 of its 8 shader files are byte-identical to the Nexus release. The 8th differs only by a clamp added locally on 2026-08-11. Its only albedo touch is a power function whose exponent is 1.0 here. |
| Preset `[VEGETATION]` / `[OBJECT]` / `[COMPLEXGRASS]` | Irrelevant | Those key names do not appear in the renderer binary at all. It never reads them. |
| ParallaxGen mesh output | Excluded | Its only change to these flowers is one soft-lighting value, 1.0 to 0.6. The same edit was applied to green ferns and to red and yellow flax, all of which render correctly. |
| Soft lighting / subsurface as the transform | Excluded by code | The soft-light term is multiplied through the petal's own albedo (`color += diffuseColor * BaseColor`). It cannot move a hue. |
| Grass caches, LOD output, No Grass In Objects | Excluded | These decide where grass exists, not its colour. |
| Wetness, skylighting, texture headers, mips, alpha, HDR colour space | Excluded | Checked and clean. |
| Extended Translucency | Excluded | `SkinnedOnly` is true, so it never touches flora. |
| Astralite's grass-lighting override | Not the hue cause | Its two values are a brightness scale and a subsurface amount. Both are colourless. It IS still forcing grass subsurface to 1.0 (see section 8). |

### The old "Effects 11 is the culprit" inference was unsound

Toggling Effects 11 off does three things at once, so it cannot isolate anything:
1. It unloads the entire ENB preset — shader code and settings both.
2. It removes a hook on the game's directional ambient lighting, so it changes the light the flowers sit in.
3. Its own passes stop.

An albedo that has already been hue-doubled will read completely differently under two different illuminants. That is the most likely reason the toggle looked like a fix.

Separately, the Effects-11-off screenshots are around half clipped to white, with up to 97 percent of petal pixels clipped. They are not usable as a colour reference.

---

## 7. The fix, once confirmed in game

Preferred, surgical, no mod changes: edit the six worldspace configs in
`mods\[NoDelete] Community Shaders AIO\Shaders\SnowCover\`.

- Set `AffectGrassTint` to 0 in all six.
- Set `AffectTreeTint` to 0 in `Tamriel.json` (it is already 0 in the five cities).

Nothing is lost. The snow line is already at infinity, so the tint has no legitimate work to do.

Alternative, blunt: turn Snow Cover off entirely in the renderer menu. That also loses fire-melt and snow shading.

Alternative, clean-room: switch off the AIO mod and switch the four official Community Shaders mods back on. Loses 13 features including Screen Space GI and Skylighting.

### After the fix

Every flora texture should be repainted to its **true** colour and the pre-rotation retired. The retint mod exists only to pre-compensate for this bug. Its locked values will over-rotate once the bug is gone.

This should also be reported upstream. At zero snow the function must be identity for all hues.

---

## 8. Separate, still-open item: grass subsurface

Independent of the above, `Astralite Weathers` ships a Community Shaders override that forces grass subsurface scattering to 1.0 and sets `OverrideComplexGrassSettings`. Confirmed applied at runtime in the game log ("Applied override from Astralite to GrassLighting").

A prior session measured that dropping this to 0.0 restored the violet and blue hue bins on grass lupines from 0 pixels to about 10,000, and settled on 0.35. The 2026-08-17 baseline pullback restored it to Astralite's shipped 1.0.

So grass flowers currently have **two** faults stacked: the hue doubling and the maxed subsurface. Fix the hue doubling first, then re-judge whether 0.35 is still wanted.

---

## 9. Gaps still open

- The direct-light gating is now mostly explained by the worldspace split rather than by lighting. The residual sun-versus-shade difference is unproven and is probably just that a dim petal in shade does not show its hue clearly.
- Whether the bug existed on 2026-08-09 under the official build cannot be established from disk. The earliest flora artifact is 2026-08-11, after the AIO landed.
- No pre-migration screenshot shows these flowers in direct light. The `DEEEZ NUTTZZZ` fallback profile is the only way to close that, and note it is missing 65 mod entries, so Mod Organizer will add them on next refresh — do not assume it is a clean one-click A/B.
- The Effects 11 ambient hook was not disassembled. What it writes is unknown.
- Silent Horizons' LUT registration file is rejected nine times at every launch. Compilation continues without it. Harmless for this bug, but it means the LUT may never be bound.

---

## 10. Falsifiable prediction

If the doubling model is right, a test petal painted at hue 210 must render orange at about hue 60, in the open world, and unchanged inside Whiterun. Anything else kills the model.
