# Starting-area lantern investigation — 2026-10-20

User observation: lanterns appear to try to glow but do not properly glow or illuminate surroundings. Happens with RaceMenu light both ON and OFF; investigate area lighting, not RaceMenu.

Active profile verified: DEEZ CS NUTZ - PICTA. Read-only investigation; no installed mods/profile edits.
Actual replacement area: Through the Woods - Alternate Perspective Addon / AlternatePerspective - Sev Cut.esp, CELL 000002 (SEVAPstartcell). Original APStartCell is replaced; its Lux conflict is not evidence of this issue.

Verified:
- Red lantern REFR 00023F, base STAT 00023E (Sev Cut), position 459.10547,946.11444,349.61603.
- Blue lantern REFR 0001E6, base STAT 0001E5, position 866.32605,668.9494,271.9547.
- Winning meshes: meshes/Oaristys/The Witcher/Lamps/Lantern02_red.nif and Lantern02_blue.nif, both from Through the Woods. Both single-shape EnvironmentMap shaders; emissive RGB 0,0,0; no own-emission/glow shader flags and no particle-light blocks. This supports lack of visible self-glow; do not indiscriminately make the whole metal lantern emissive.
- Separate placed lights exist and are not initially disabled.
- Red light REFR 000241 (Sev Cut): Lux Orbis patch changes base from 0B15EE:Skyrim.esm to 000891:Lux Orbis.esp; moves from 457.13602,942.2465,407.81232 to 494.6499,788.21204,403.03952; removes LightData including FadeOffset 1.65. Base falloff exponent changes 1 to 5, radius remains 512, base fade 1.35 to 1.5. Likely contributor to weak/misplaced illumination, not in-game confirmed.
- Blue light REFR 0001EA: patch changes base from 0E2172:Skyrim.esm to 000B61:Lux Orbis.esp. Current radius 425, fade 1, falloff 1, Dynamic/Flicker/PortalStrict. No proven explanation yet for complete absence of blue spill lighting.

Evidence: start-room-lighting-records.jsonl (old room), sev-start-lighting-records.jsonl (actual area), both in _tools.
Next: controlled local patch trial restoring red light placement/appropriate reach, investigate glow-mask-capable lantern mesh treatment; assess blue light in game before claiming complete fix. Avoid global Lux edits, whole lantern glow, blind load-order changes. User approved focused investigation, not a large rebuild. Check MO2/game closed immediately before every mods/profiles write. No Synthesis/Reqtificator/LOOT.
