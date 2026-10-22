# Authoria - Magpie Manor Rooster Fix

Built 2026-08-20. Fixes the manor rooster rendering with a scrambled/misplaced texture (head on torso).

## Cause

MagpieManor.bsa bundles Mihail's **old-generation** rooster:

- mesh `meshes\aproco\magpie\Mihail Monsters and Animals\Chicken\chicken\mihailrooster.nif` (shape `rdmobj00`, plain NiSkinInstance, no alpha)
- matched textures in `MagpieManor0 - Textures.bsa` at Mihail's ORIGINAL path `textures\mihail monsters and animals\chicken\chicken\rooster.dds` (174,928 bytes, md5 367B9123...) + `rooster_n.dds` (43,856 bytes)

The installed mod `mihail - Roosters (se-ae)` provides a **remastered** `rooster.dds` (22,369,776 bytes, md5 CFCF5894...) + `rooster_n.dds` (5,592,560 bytes) **loose** at that same path. Its UV layout pairs with the current-generation mesh (`grp020`, provided loose by MMOP with BSDismember + alpha-tested feathers) that Mihail's own roosters use.

Loose beats BSA, so the Magpie rooster rendered old mesh + new texture = misplaced pattern. Broken since install day; only manifests when a Mihail rooster/remaster mod is installed. Skeleton, record chain (`_mag_RoosterNPC` → `_mag_SkinRooster` → `_mag_NakedRooster`), and Reqtificator output were all verified healthy.

## Fix (asset-only, no plugin)

1. `meshes\aproco\magpie\...\mihailrooster.nif` — byte-identical copy of the bundled mesh except its two embedded texture paths, byte-patched **same-length in place** (no offsets/block sizes touched) to:
   - `textures\aproco\magpie\rooster_magpie_bundled_oldgen_pair_v1.dds`
   - `textures\aproco\magpie\rooster_magpie_bundled_oldgen_pair_v1_n.dds`
   (src md5 d101151e... → patched 98ddc514..., 115,497 bytes both)
2. Those two textures = the matched old-gen copies extracted from `MagpieManor0 - Textures.bsa`, renamed. This mod is their **sole provider**; nothing can override them.

The loose mesh here beats Magpie's BSA copy regardless of mod priority. Mihail's own roosters (remaster pair) are untouched.

## Audited, clean

All 1,350 meshes in MagpieManor.bsa scanned for foreign `textures\mihail*` references. Only three: this rooster, plus a chair and a clock from the Mihail Dungeons "toxin doctor laboratory" series — those textures have **no loose challenger** (Magpie BSA is sole provider), so they stay matched. No other fix needed.

## If the rooster breaks again later

1. Check who wins `meshes\aproco\magpie\Mihail Monsters and Animals\Chicken\chicken\mihailrooster.nif` — this mod must win it loose. A future **ParallaxGen** run may emit its own processed copy of that path into its output mod; if so, that copy was generated from whichever file won at generation time and should carry these repathed textures forward. If PG output wins with the OLD Mihail paths embedded, re-run PG or hide that one file in the PG output.
2. Enabled state: this mod belongs in **DEEZ CS NUTZ** only (Magpie Manor is profile-exclusive to it).
