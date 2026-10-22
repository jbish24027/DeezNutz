# Bottled Shaders (CS fork) - Advanced Skin sweat notes (2026-08-17)

Data behind the chat summary. Nothing here has been changed in the load order.

## How the sweat value is computed (from the CS dev-branch source, `src/Features/Skin.cpp`, `Skin::GetWetness`)

The build in use: Bottled Shaders 1.8.0 `pre-dev-merge-20260805-60-g3cb762e4d`
(installed as mod `[NoDelete] Community Shaders AIO`, DLL `SKSE\Plugins\CommunityShaders.dll`).
The DLL exposes exactly the same Skin settings as the CS dev source: `StartSweat`, `FullSweat`,
`WetFadeTime`, `ExtraSkinWetness`, `UseDynamicWetness`. There is NO player-only / NPC toggle in this build.

Per rendered actor (player AND every NPC, `formType == ActorCharacter`), once per frame:

```
stamina      = GetActorValue(Stamina)                       // current
maxStamina   = max(GetPermanentActorValue(Stamina) + TemporaryModifier(Stamina), 1)
pct          = IsDead ? 1.0 : stamina / maxStamina
sweatRange   = StartSweat - FullSweat
sweat        = |sweatRange| < 1e-5 ? 0
             : pct >= StartSweat   ? 0
             : pct <= FullSweat    ? 1
             : (StartSweat - pct) / sweatRange              // linear ramp
```

* Slider "Stamina Threshold for Sweat" = `StartSweat`. Slider "Full Sweat Threshold" = `FullSweat`.
* Sweat rises INSTANTLY. It fades at `1 / WetFadeTime` per second, so full-to-dry takes
  `WetFadeTime` seconds (9.16 s in the screenshot). The same fade time is shared with water wetness.
* Setting `StartSweat = 0` disables stamina sweat (pct can never be below 0).
  Setting both sliders equal also disables it (sweatRange ~ 0 branch).
* An actor with a max stamina of 0 (mannequins, statue actors, anything with 0 base stamina)
  divides by the clamp value 1 -> pct = 0 -> permanent FULL sweat at any threshold above 0.
* An actor whose current stamina is stuck near 0 shows full sweat at any threshold above 0.
  Lowering the slider does not help those; only 0.00 hides them, or fix the actor's stamina.
* Water wetness (swimming) is a separate channel (`wetness.y/.w`) and is unaffected by the sweat sliders.
* Rain wetness on skin is the separate "Wetness Effects" feature (`SkinWetness` = 0.95 there),
  not this slider.

## Saved settings vs. the screenshot

File: `C:\1. AUTHORIA\overwrite\SKSE\Plugins\CommunityShaders\SettingsUser.json` (written 2026-08-17 05:18)

| key            | on disk | screenshot |
|----------------|---------|------------|
| StartSweat     | 0.75    | 0.26       |
| FullSweat      | 0.15    | 0.15       |
| WetFadeTime    | 10.0    | 9.16       |
| Translucency   | 0.10    | 0.19       |
| sssWidth       | 0.20    | 0.24       |

The 0.26 in the screenshot was never saved. `SettingsDefault.json` also has StartSweat 0.75, so a
"reset to defaults" lands on 0.75 too. No mod ships a Skin override file (`*_Skin.json`), so nothing
else is forcing the value.

## Why an NPC can sit below the threshold at rest (this load order)

1. Requiem "Physical Exertion (Attacking)" — `REQ_Stress_Attacking` `6AA964:Requiem.esp`,
   effect `REQ_Effect_Mechanics_Stress_Attacking_` `6AD103:Requiem.esp` (Damage Stamina, constant
   effect ability put on any attacking actor). Known "stuck exhaustion / no stamina recovery" bug:
   the ability stays on the actor after combat and drains stamina forever.
   Installed mitigations: `Requiem - Exhaustion and Stamina Fix` (Nexus 170787) and
   `Authoria - Exhaustion and Stamina Fix - Optimization` (script `REQ_AttackStaminaDrain`).
   The optimized script strips the drain when the effect finishes / on cell detach, but an actor
   that got stuck BEFORE those were installed (or in a save state) can still be stuck.
2. Normal exertion: NPC fought, sprinted, power-attacked (SCAR stamina limitation makes NPC attacks
   cost stamina). Temporary; clears when they regen past the threshold, plus the fade time.
3. Zero max stamina actors (mannequins etc.) — permanent full sweat, see above.
4. `houseCARL - Authoria - Run Stamina Drain` is PLAYER ONLY (checked the script) — not an NPC cause.

## In-game check (proves the mechanism on a specific NPC)

1. Open console, click the sweaty NPC.
2. `getavinfo stamina` — shows base, permanent mods, temporary mods, damage, current.
   Sweat is on when current / (base + perm + temp) < StartSweat.
3. `getav stamina` again after ~30 s standing still. If it does not climb, the NPC is stuck.
4. To find the Requiem exertion ability's runtime ID: `help "Physical Exertion" 4`.
   To strip it from the selected NPC: `removespell <that id>`; stamina then regenerates by itself.

## Override-file option (pins the value across saves/updates)

Bottled Shaders merges `Data\SKSE\Plugins\CommunityShaders\Overrides\{ModName}_{FeatureShortName}.json`
over the user settings at every launch. For Advanced Skin the short name should be `Skin`
(its feature ini is `Shaders\Features\Skin.ini`; confirm in the in-game Overrides tab after adding).

```json
{
    "StartSweat": 0.10,
    "FullSweat": 0.03,
    "_metadata": {
        "modName": "Authoria - Skin Sweat Tuning",
        "version": "1.0.0",
        "description": "Sweat only when nearly exhausted",
        "enabled": true
    }
}
```

Put it in a small mod (e.g. `Authoria - CS Skin Sweat Override`) so it survives a CS AIO reinstall.
Downside: while the override is enabled, the two in-game sliders are re-overridden at each launch.

## Code-level option (player-only sweat)

One line in `Skin::GetWetness` after the sweat is computed:

```cpp
if (!actor->IsPlayerRef()) wetness.x = 0.0f;   // or gate on a new setting
```

Needs a rebuild of the Bottled Shaders fork (its source must be public — CS is GPL) or a
feature request to the fork author ("NPC sweat" toggle / player-only sweat).
