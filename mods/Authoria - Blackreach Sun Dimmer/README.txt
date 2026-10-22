Authoria - Blackreach Sun Dimmer
================================
One file: meshes\Clutter\Blackreach\BlackreachSun01.nif

WHAT IT IS
  A byte-for-byte copy of the winning BlackreachSun01.nif (from
  "Dwemer Metals Retexture SE") with ONE value changed: the sun sphere's
  emissive multiple on shape BlackreachSun01:20 (BSLightingShaderProperty,
  block 19) is 4.0 instead of 8.0. Emissive colour is untouched
  (1.0, 0.851, 0.247). Only 2 bytes differ from the source file.

WHY
  Vanilla ships the sphere at x8. Lux ships its own copy of this mesh at x3
  ("Lux (patch hub) - rerun\meshes\Clutter\Blackreach\BlackreachSun01.nif"),
  but the Dwemer Metals Retexture copy sits above Lux in the mod list, so the
  x8 version was winning and the sun bloomed out. 4.0 is halfway between the
  vanilla and Lux values. Requested 2026-08-16: "decrease the brightness
  coming off of that a bit".

WHERE IT SITS
  Directly above "Dwemer Metals Retexture SE - Patches" / "Dwemer Metals
  Retexture SE" in every profile's modlist, so it beats that copy and keeps
  the retexture's own material set-up (Bronze cubemap on the ring/wings).

TO RETUNE
  python <scratch>\nifshader.py set-emissive "<this mesh>" 19 <value>
  Lower = dimmer. Lux uses 3.0. Vanilla is 8.0. Or delete this mod folder
  and its modlist lines to go back to x8.

WHAT THIS DOES NOT TOUCH (further dials if the sun is still too bright)
  1. The orange halo around it is SEVEN vanilla FXGlowFillRoundMid glow-fill
     billboards (Skyrim.esm refs 0DB9D4/D8/D9/DA/DB/DC/DD, scale 5.33) tinted
     by their emittance light FalmerCityLight01NS (238,83,17). They are haze
     only - GlowSoft01.dds is not a registered CS particle-light texture - so
     they add glow but no light. Reducing them means overriding those seven
     placed refs (a plugin), which also carries the parent-cell override risk.
  2. The actual light: Lux.esp ref 2B3C73 = Lux_DwemerRuinsBlackreachSun
     (255,171,102, shadow-casting) at the sphere, radius 2509, base fade 1.0
     + FadeOffset 1.5, plus two NS fill lights (2B8EC1 r468, C9A730 r1033).
     Not blacklisted by Lux CS (its blacklist covers skyrim.esm / USSEP only).
  3. If ParallaxGen is re-run and processes this mesh, "Authoria - PG Output"
     will win again with the x8 copy - re-apply the edit to the PG copy or
     re-copy this file over it.

Created 2026-08-16.
