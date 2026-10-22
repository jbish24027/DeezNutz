# Spell Hotbar — size and Vel'dun fit (2026-08-18)

All numbers below were read from the mod's own source and from your co-save, not estimated.

## Your live state (read out of the newest co-save, proven not assumed)

Spell Hotbar stores its settings in the SKSE co-save, per savegame. There is no settings file on disk.
Parsed record 'HOTB' (plugin id 0xE219D7E9) from
`profiles\DEEZ CS NUTZ\saves\Save4_..._20260818090425_1_1.skse`:

| setting | live value |
|---|---|
| number_of_slots | 12 |
| slot_scale | 1.0 |
| slot_spacing | 8 |
| offset_x / offset_y | 0 / 0 |
| show bar text | Fade |
| hud show mode | Combat or Drawn |
| vampire lord / werewolf | Combat / Never |
| ctrl / shift / alt bars | off / off / off |

Every per-bar record in the co-save is 6 bytes with one non-zero byte, and 'GDAT' is four zero bytes.
Nothing is bound — no spells in slots, no keybinds. Confirmed across all three newest co-saves.

Display: 3840 x 2160 (`SkyrimPrefs.ini` iSize W/H). Independently corroborated by
`SpellHotbar.log` line "Loading Fonts with sizes 48, 72", which is only consistent with H=2160.

## Why it looked too big

Slot size is derived from screen height, not from a fixed pixel constant:

```
slot_px      = floor(screen_height / 13 * slot_scale)
slot_row_px  = N * slot_px + (N-1) * slot_spacing
row_left     = screen_w/2 - slot_row_px/2 + offset_x     (auto-recentres)
row_top      = 0.8 * screen_h + offset_y + 8             (TOP-anchored)
keybind_px   = (slot_scale + 0.25) * round(24 * screen_h / 1080)
```

At H=2160, slot_scale 1.0 gives **166 px per slot** and a **2080 px** slot row — 54.2% of your
screen width. That is the whole problem. The mod's shipped presets were authored at 1080p.

## What was changed

New mod: **`Authoria - Spell Hotbar Veldun Fit`**, placed directly above `Spell Hotbar` in all four profiles.
It contains exactly one file:
`SKSE\Plugins\SpellHotbar\presets\Authoria Veldun Fit.json`

It is a byte-clone of Spell Hotbar's own `Default.json` with three values changed:

| key | stock | new | effect at 3840x2160 |
|---|---|---|---|
| settings.slot_scale | 1.0 | **0.7735** | slot 166 px -> 128 px |
| settings.slot_spacing | 8 | **12** | restores the author's intended ~9% gap |
| settings.offset_y | 0 | **19** | holds the bar's optical centre |

Result: slot row 2080 px -> **1668 px**, i.e. 54.2% -> **43.4%** of screen width. About 23% smaller
linearly, 41% smaller by area.

Verified before writing: `Default.json`'s values are byte-equal to your live co-save values, so loading
this preset changes ONLY those three numbers. All 14 keybind entries in it are -1, matching your
current unbound state, so nothing is lost.

### Why 0.7735 and not a round number

Every texture that renders inside a slot is natively 128 x 128:
- `default_icons.png` 1024x1024 on a 0.125 UV grid = 128 px cells
- `icons_cooldown.png` 1024x1024 on 0.125 = 128 px
- `icons_vanilla.png` on a 0.0625 grid = 128 px
- Vel'dun's `default_icons_veldun.png` 256x256 on a 0.5 grid = 128 px

At slot_scale 1.0 on a 2160p screen every one of them is bilinearly **magnified 166/128 = 1.298x**.
That is a measurable cause of the hotbar looking soft next to Vel'dun's crisp Flash UI.
slot_scale in the band [0.77037, 0.77639) yields exactly 128 px = 1:1 texel, zero resampling.
The MCM slider steps in 0.01 and cannot reach it (0.77 -> 127 px, 0.78 -> 129 px). A preset file can,
because the native setter `set_slot_scale` is unclamped (`papyrus_functions.cpp:122-125`).

### How to apply it

MCM -> Spell Hotbar -> **Presets** page -> **Load Config** -> `Authoria Veldun Fit` -> confirm.

Nothing can be applied purely from disk: `presets\*.json` is read ONLY by `SpellHotbarMCM.psc`
(`loadSettingsFromPreset`, line 364), whose single caller is the `LoadPresetState` MCM entry.
The DLL never reads the presets folder — proven by grepping all 31 source files for preset/json/ifstream/
directory_iterator; the only paths it opens are images\, fonts\, spelldata\, effectdata\, transformdata\.
`Default.json` is a manual template, not a startup config.

**Caveat:** loading any preset also rewrites every keybind and per-bar flag from that file. Harmless now
(nothing is bound). If you bind keys first and load the preset later, you lose the bindings. Load it first.

Equivalent by hand if you prefer sliders (cannot hit 128 px exactly): Settings page -> Slot Scale 0.77,
Slot Spacing 12, Offset Y 19.

## Why it does not match Vel'dun — measured, ranked

Vel'dun's Spell Hotbar patch defines **exactly two** icon keys. Its `default_icons_veldun.csv` is three
lines: BAR_EMPTY and BAR_OVERLAY. Everything else in a slot is still stock Spell Hotbar art.
Load order confirmed in `SpellHotbar.log`: default_icons.png, then default_icons_veldun.png, then
icons_cooldown.png, then icons_vanilla.png — so Vel'dun does win its two keys.

Decoded palettes (opaque pixels, PNG decoded with zlib/struct):

| element | source | palette |
|---|---|---|
| BAR_EMPTY (Vel'dun) | veldun | black panel @ 50% alpha; border #2B231B, #7D7565, #1C1C14, #6D6555 — warm olive/gold, 30 colours |
| BAR_OVERLAY (Vel'dun) | veldun | hollow, 8 px border, same warm palette, 48 colours |
| BAR_EMPTY (stock) | stock | same structure, border **#9D9D9D / #ABABAB — neutral grey** |
| **BAR_HIGHLIGHT (stock, NOT overridden)** | stock | **#375C69 / #325662 / #40707E — teal-blue**, 4062 colours, painterly |
| UNKNOWN (stock) | stock | **#E71A14 bright red**, 5845 colours, painterly |
| UNBIND_SLOT (stock) | stock | **#C60500 bright red**, 726 colours |

**1. The selection/cast highlight is teal-blue on a gold frame.** Vel'dun never overrides BAR_HIGHLIGHT.
Highest visible impact, because it fires every time you highlight or cast from a slot. Fixable cheaply:
ship a `default_icons_zveldun.csv`/`.png` pair (sorting after `default_icons_veldun` so it wins) carrying a
BAR_HIGHLIGHT recoloured into Vel'dun's warm palette. This is new art, so it was NOT done unilaterally.

**2. The keybind numbers use the wrong typeface.** Spell Hotbar hardcodes
`fonts\9_$ConsoleFont_Futura Condensed.ttf` (`render_manager.cpp:311`). Vel'dun's `fontconfig.txt` maps
`$ConsoleFont` to Arial and uses **Lato** for start menu, dialogue and everywhere text. Because the DLL
loads that TTF by exact filename, dropping a Lato TTF renamed to that filename in an override mod would
switch the hotbar numbers to Vel'dun's typeface. Vel'dun already ships a real Lato TTF
(`Vel'dun UI Overhauls - Patches\Interface\ImGuiIcons\Fonts\Lato-Regular.ttf`, 641 KB). Cheap, reversible.

**3. The spell icons are AI-painterly.** `icons_vanilla.png` is full-bleed painted art; Vel'dun is flat,
dark, low-colour line work. This is the largest stylistic gap and the one that cannot be fixed by
configuration. Options:
- The **SpellHotbar2 - Icon Packs Hub** (Nexus 185689) has 173 packs, but it hard-requires **SpellHotbar2**
  and ships **DXT5 DDS**. Spell Hotbar 0.1.2's loader is **PNG-only** — it derives the image path by
  replacing the csv's last three characters with "png" — so those packs cannot load on your version.
- Vel'dun already ships a **Spell Hotbar 2** patch (in the same Vel'dun Patches FOMOD), and its Vel'dun
  frame art is a far richer 87 KB DDS versus the 3 KB PNG for Spell Hotbar 1. Moving to SpellHotbar2 would
  improve the Vel'dun match and unlock the 173 packs. It is a different mod, so it is a deliberate swap,
  not an update.

**4. The cooldown sweep is stock art** (`icons_cooldown.png`), drawn over Vel'dun's frame at slot size.
No Vel'dun equivalent exists. Low impact — it only shows while a slot is cooling down.

## Things that are NOT the problem

- Vel'dun's frame IS winning. Verified through the VFS and in the load log.
- `slot_spacing` is raw unscaled pixels, never resolution-corrected. Stock 8 px is 4.8% of a 166 px slot,
  where at the 1080p it was authored for it was 9.6%. This made the slots read as crowded. Hence 12.
- `offset_x` never needs compensation. The row is exactly centred every frame from its own width.
- The bar is TOP-anchored at 0.8 x screen height, so shrinking pulls the bottom edge up by the slot
  delta. offset_y 19 splits that difference; 38 would pin the old bottom edge.
- The keybind glyph scales as (slot_scale + 0.25), i.e. sub-proportionally, so it grows slightly relative
  to the slot as you shrink: 36.1% of slot height at 1.0, 38.6% at 0.7735. Mild, and a reason not to go as
  low as the shipped Minimal preset's 0.70.
- Slot count is capped at 12 in code, and you are already at 12.

## Unverified

Nothing here was tested in game — MO2 and Skyrim were never launched. Every pixel figure is computed from
the source formulas plus your confirmed resolution. That the 1.298x upscale is specifically what you were
reacting to is inference; the teal highlight, the stock typeface and the painterly icons are equally
plausible contributors, and none of those three are fixed by any slot_scale value.
