Authoria - Blue Flower Soft Light Fix
=====================================
Created 2026-08-16. Meshes only, no plugin. Save-safe.

THE PROBLEM
The blue mountain flowers (the blue lupine spikes) render TAN/CREAM in direct
sun and only look blue in shade or overcast. Every texture repaint failed to
fix this, because the cause is not the texture.

WHY (measured, not guessed)
- On disk the petal texture IS deep blue (blue_lupin01.dds, petals ~RGB 77,83,144).
- In a sunny frame the petals render warm tan (~RGB 156,111,65) while the
  neutral dirt right next to them is only mildly warm. The petals get an EXTRA
  warm term the ground does not - so it is petal-specific, not the color grade.
- The flower mesh has the "Soft Lighting" shader flag set. Soft Lighting wraps
  the DIRECT SUNLIGHT (which is warm) through the thin petals as translucency.
  In sun that warm wash swamps the blue albedo -> tan. In shade there is no warm
  sun to wrap, so the blue shows -> that is why it was "blue in Whiterun / shade,
  tan in sunny Morthal."
- The warm term is NOT driven by the subsurface map (_sk). Darkening that map on
  2026-08-16 changed nothing in game, which proved it. Community Shaders' own
  Subsurface Scattering feature is skin-only here, so it is not that either.
- The only lever that removes a petal-specific warm term is the mesh's own
  Soft Lighting flag.

WHAT THIS MOD DOES
Clears ONLY the Soft Lighting flag (SF2 bit 25) on the blue-lupine shapes of
these meshes. One bit per shader block; nothing else in the mesh is touched
(verified: 1-2 bytes changed per file, all inside the SF2 word). Base copies are
Reimagined Mountain Flowers' own meshes (structurally identical to the PG output,
so no parallax is lost). Files:
    plants\floramountainflower01blue.nif        + AUT
    plants\floramountainflower02blue.nif        + AUT
    plants\mountainflower01blue.nif             (JK's static decorations)
    Seasonal Alchemy\floramountainflower01blue-noflower.nif   + 02
    _byoh\plants\byohhouseingrdmtflblue01.nif   + switchnode child
The four WINTER variants (...WIN / ..._winter) already had Soft Lighting off on
the petal shape, so they were left alone.

TRADE-OFF - READ THIS
Soft Lighting is what gave the petals their translucent glow. With it off the
petals are matte blue instead of glowing. You cannot have a warm glow AND blue -
the glow IS the warm sun bleeding through, so any glow here is warm/tan. Blue and
flat is the only way to blue. If the flowers now look too flat rather than tan,
that is the trade; tell me and I can instead LEAVE a little glow by lowering the
soft-lighting strength (LE1) rather than clearing the flag - it will be a bit
warm in strong sun but less matte.

If this did NOT fix the tan (still tan in sun after a fresh cell load), then the
warmth is coming from the ENB grade after all, not the mesh - revert this (just
disable the mod) and the next place to look is Effects 11 vegetation, not another
texture.

PRIORITY
Must sit ABOVE "Authoria - PG Output" and "Reimagined Mountain Flowers" in MO2
so these meshes win. It is inserted right above PG Output.

REVERT
Disable or delete this mod. Nothing else changes.

TEST
Load a save, go to the sunny Morthal flower patch, and leave+re-enter the cell
(or wait a bit) so the meshes reload fresh. The flowers should read blue in sun,
not cream.
