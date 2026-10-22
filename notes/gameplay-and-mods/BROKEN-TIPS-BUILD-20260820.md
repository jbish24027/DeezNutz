# Authoria - Broken Feathers - Special Tips — Build Log 2026-08-20

Special-tip arrows from Skyrim Arrow Overhaul now break like vanilla arrows do under Ricochet Framework + Broken Feathers.

## What was built

**New mod**: `mods\houseCARL - Authoria - Broken Feathers - Special Tips`
- `Authoria - Broken Feathers - Special Tips.esp` — ESL-flagged (light master), 64 new records, no overrides.
  Masters: Skyrim, Update, Dawnguard, Skyrim Arrow Overhaul, Broken Feathers.
- 32 MiscItem "pieces" records (0x800–0x81F, in build order after ESL compaction): one per covered arrow, named "<Arrow> [broken]",
  reusing Broken Feathers' per-material bag models, VendorItemArrow + BF_BrokenAmmo_Keyword,
  arrow vs bolt pickup sounds. Name/value/weight are runtime-overwritten by the framework
  (it renames the authored record from the live arrow name — proven from the DLL/PDB, which also
  proves it never duplicates forms, hence dedicated 1:1 pieces per arrow).
- 32 reforge recipes (0x820–0x83F, same order): Firewood ×2 + own pieces ×5 → 5 of the exact special arrow,
  at the forge, gated per material with the same Requiem smithing perks Broken Feathers uses
  (iron tier perkless; steel/silver = Craftsmanship; then Dwarven/Elven/Glass/Orcish/Ebony/Daedric).
- 32 JSON fracture configs in `SKSE\RicochetFramework\AuthoriaSpecialTips\Arrows\` — FormID-keyed
  (update-safe), each: FractureMapping (ammo → Fracture true) + AmmoMapping (durability + broken-state
  projectiles reused from Broken Feathers per material). Every JSON key verified against the key table
  mined from the Ricochet 1.1.2 DLL parser.

## Coverage (32 of 74 SAO ammo)

- **Arrows (23)**: bodkin/crescent/hammerhead in iron, steel, elven, orcish (plus glass/ebony bodkin+hammer,
  daedric bodkin), dwarven bodkin/crescent/hammer, both basketheads (steel + dwarven, unlit), Silver Arrow
  (steel pieces — silver is a steel shaft; its own keywords say so).
- **Bolts (9)**: all dwarven-material tips → dwarven bolt pieces; all steel-material tips + Silver Bolt →
  steel bolt pieces.
- **Durability copied per material from Broken Feathers** (iron 25 … daedric 90), so tips break at the
  same rates as their plain siblings.

## Deliberate exclusions (42)

- Fire/frost/shock arrows+bolts (12): explosive payloads, Requiem no-recovery keyword — nothing to recover.
- Whistle arrow+bolt (2): the "explosion" is the mechanism that spawns the whistle lure at the landing
  spot; fracture would fight the feature.
- Bound bodkin (1): conjured; Ricochet 1.1.2 auto-excludes bound ammo (verified in the DLL).
- Practice bolt (1): training ammo; practice targets are already fracture-excluded.
- Bolts of materials with no Broken Feathers bolt pieces (26): iron/elven/glass/orcish/ebony/daedric/
  dragonbone/nordic/stalhrim/draugr/falmer/forsworn/silver-only-mismatches — a steel- or dwarven-textured
  bent bolt stuck in a wall would read as the wrong material. They keep the framework default
  (vanilla-style 50% recovery). Revisit only if bent-bolt meshes get retextured per material.

The adversarial design audit overturned 5 of my first-pass exclusions (steel hammerheads, steel
basketheads, Silver Bolt): their "explosions" are an inert, flag-less zero-damage ragdoll helper record,
not a payload. NOT touched: that helper's odd PlacedObject (it references the Steel Hammerhead Arrow even
from bolt records) — SAO ships a hammerhead ragdoll-knockdown script, so the record is feature-adjacent
and nulling it risks breaking the knockdown.

## Retracted mid-build: "third Broken Feathers recipe bug"

During the build I misread the vanilla Steel Arrow reforge recipe as having a null perk condition
(a shallow read showed the condition's run-on reference as Null — that field is normally null, and the
perk parameter simply wasn't displayed at that depth). Adversarial verification proved the recipe was
always correct: its gate is already the steel-tier smithing perk Requiem uses. The identical override
I had written into `Authoria - Patch - Skyrim Arrow Overhaul - Requiem.esp` was removed again; the patch
is back to its exact prior state (311 records, byte-size identical, clean error sweep). Broken Feathers'
only real recipe bugs remain the two already fixed on 08-14 (dragonbone + nordic wrong ingredients).

## Verification round-trip (what the adversarial pass caught)

Five independent verifiers ran on the finished artifacts. Coverage, profile wiring, and patch regression
passed outright. The JSON and record verifiers caught one real, game-breaking bug: **ESL compaction
renumbers records by type group**, so the pieces items ended at 0x800–0x81F and recipes at 0x820–0x83F —
while the 32 JSONs still pointed at the creation-time interleaved IDs, sending 31 of 32 broken-arrow
drops to the wrong record. All 32 JSONs were regenerated against the post-compaction layout and every
pointer re-resolved by name: 32/32 now hit exactly their own pieces item. Record content itself verified
field-by-field clean (names, models, keywords, sounds, ingredients, gates, ESL header).

## Load order / profile wiring (DEEZ CS NUTZ only, by design)

- modlist: `+houseCARL - Authoria - Broken Feathers - Special Tips` directly above `+Broken Feathers`.
- plugins/loadorder: `Authoria - Broken Feathers - Special Tips.esp` directly after `Broken Feathers.esp`,
  before `Requiem.esp`. FWMF output still last in both files (verified).
- plugingroups: added to `Authoria - Arrow Suite` (now 5 members).
- Backups: all four files `*.bak-brokentips-20260820`.
- Other 3 profiles untouched — the arrow suite exists only in the CS profile.
- check_errors: 0 dangling refs, 0 missing masters on both plugins.

## Known watch item

**Elven Bodkin Arrow** shares the VANILLA Elven Arrow projectile (an SAO data bug — it flies with the
broadhead model). Both are now fracture-mapped (ours by SAO ammo ID, Broken Feathers' by vanilla ammo ID).
All DLL evidence says the framework keys mappings by AMMO, so both should behave independently — but this
is the one entry to watch in-game. If a broken Elven Bodkin ever yields vanilla Elven pieces (or vice
versa), the fix is to point the ammo at a dedicated bodkin projectile in the Requiem patch.

## In-game test list

1. Craft or console a stack of Iron Bodkin Arrows; shoot a stone wall hard until one snaps —
   expect the snap sound, bent-arrow debris, and an "Iron Bodkin Arrow [broken]" pieces item.
2. Reforge at a forge: 5 broken pieces + 2 firewood → 5 Iron Bodkin Arrows (no perk needed for iron).
3. Repeat with a Dwarven Bodkin Bolt (needs Dwarven Smithing for the reforge).
4. Check a steel-tip reforge shows only with Craftsmanship taken.
5. Elven Bodkin Arrow: break one — pieces must say "Elven Bodkin Arrow [broken]", and reforging them
   must return bodkins, not plain elven arrows (the watch item above).
6. Fire/frost/shock and whistle arrows: confirm they still explode/whistle normally and never leave pieces.
