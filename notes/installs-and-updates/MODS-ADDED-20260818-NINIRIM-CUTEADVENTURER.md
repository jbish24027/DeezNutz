# Ninirim Collection 6.0 + Cute Adventurer — install, Requiem patch, Frostfall, BodySlide, UBE

Date: 2026-08-18. Profile: **DEEZ CS NUTZ** (enabled here; added but **disabled** in the other 3 profiles).
Profile-file backups: `*.bak-ninirim-20260818`.

## Mods added (5 folders)

| Mod folder | Contents |
|---|---|
| `[SunJeong] Ninirim Collection` | Core files + the **Remove Museum** ESP (craft-only, vanilla footsteps) |
| `[SunJeong] Ninirim Collection - 3BA Patch` | 545 sliderSets + 4 group files; overrides the core's CBBE sets |
| `Cute Adventurer Outfit` | Base + UBE option + 4K textures merged |
| `Cute Adventurer Outfit - SMP` | SMP patch (**archive bug fixed** — see below) |
| `Authoria - Ninirim and Cute Adventurer - Requiem Clothing` | 2 ESL patches (Requiem + Frostfall) |
| `Authoria - Ninirim and Cute Adventurer - BodySlide Groups` | 2 conflict-free Ninirim groups |

### Install choices
- **Remove-Museum ESP** chosen over both FOMOD variants. It has no worldspace, cells, navmesh or
  containers — 2493 records vs 3554. Its 1148 crafting recipes were **later stripped too** at the
  user's instruction — see *No museum, no recipes* below.
- Vanilla footsteps. The Remove-Museum file has no `Heels Sound.esm` master, so the heel-sound
  variant was not available with it.
- **Music folder deliberately skipped** (316 MB). It holds only the 6 museum tracks, and the
  MusicType/MusicTrack records that referenced them are absent from this ESP.
- Cute Adventurer: took the base ESP + UBE patch ESP. The two `Misc\...Light.esp` files were
  **not** installed — they exist to make the outfit light armour, which the Requiem patch overrides
  anyway.
- Install verified by reconciliation: archive reports 5336 files; 5321 installed + 6 music
  + 8 fomod scaffolding + 2 unused ESP variants = 5336. Nothing dropped.

### Archive bug fixed on install
`Cute Adventurer SMP patch.7z` ships its sliderSets at `CalienteTools\SliderSets\`, one level too
high. BodySlide would never have seen them. Relocated to `CalienteTools\BodySlide\SliderSets\`.

## Plugin slots

Measured by diffing the census against the pre-change backups (apples-to-apples):

- **before: 224 starred full · after: 225** — exactly +1, the Ninirim ESP. Nothing else reclassified.
- Total including implicit: **237 / 254**. 17 full slots free.
- Ninirim cannot be ESL-flagged: it defines 2493 records, over the 2048 light window.
- The other 4 plugins are all ESL and cost no slot.

> An earlier reading of "253/254" was taken while MO2 still had `modlist.txt` open mid-session and
> was wrong. The backup-diff figure above is the real one.

## Requiem patch — 618 armours to clothing frames

Two ESL plugins, authored by copying each source record verbatim and rewriting only the balance
subrecords. Master lists were chosen so every FormID index in the copied payload still resolves to
the same plugin, so **no FormID remapping was needed** and armature/texture links survive intact.

- `Authoria - Ninirim - Requiem Clothing.esp` — 609 records
- `Authoria - Cute Adventurer - Requiem Clothing.esp` — 9 records (built on the UBE patch's versions,
  so both the UBE and base armatures are preserved)

Per record: armour rating → **0**, body template → **Clothing**, and the armour keywords stripped.

**1658 keywords removed**, of these classes:

- `ArmorHeavy` / `ArmorLight`
- `ArmorCuirass` / `ArmorBoots` / `ArmorHelmet` / `ArmorGauntlets`
- `VendorItemArmor`
- 11 distinct `REQ_ArmorSet_*` (Leather, Steel, Ebony, Elven, Scale, Hide, Forsworn, SteelPlate,
  Dragonplate, DwarvenHeavy, OrcishHeavy)
- 6 distinct `PerkFists*` (free unarmed damage that was riding on outfit gloves)

Replaced with `ArmorClothing` + `VendorItemClothing` + the matching `Clothing<Part>` by slot;
30 jewellery-slot pieces got `ArmorJewelry` + `VendorItemJewelry` instead.

Why this mattered: the source records carried vanilla material keywords, which Requiem renames to
its own armour-set keywords. The Reqtificator would have assigned ranged resistance and tempering
from them — e.g. `00bs_belt`, a **belt on slot 49**, carried `ArmorHeavy` + `ArmorCuirass` +
`REQ_ArmorSet_Steel`, so it would have stacked steel-cuirass ranged resistance on top of the actual
cuirass. 191 pieces carried the cuirass keyword; 86 sit on slot 49 alone.

### Verification
All 618 records re-parsed from the written files and checked against five invariants — armour
rating zero, type Clothing, no stripped keyword surviving, a clothing/jewellery keyword present,
and no Frostfall tag on a slot Frostfall ignores. **Zero failures.** houseCARL `check_errors` on all
five plugins: 0 dangling refs, 0 missing masters.

## Frostfall

Rated by slot and name, in the same patch:

| | count |
|---|---|
| Warmth/Coverage **Poor** | 284 |
| **Fair** | 117 |
| **Good** (fur / winter / christmas named) | 4 |
| Untagged — accessory slots Frostfall does not read | 213 |

Body pieces default to Fair; anything named slutty / damaged / nude / topless / bikini / lingerie
and similar drops to Poor. Hands, feet and head are Poor warmth, with Fair coverage for named boots.
Only slots 30, 31, 32, 33 and 37 are tagged — Frostfall ignores the rest, so tagging them would be
noise.

## BodySlide groups

The mod's own group covers **535 of 545** sliderSets. The 10 orphans are the 3BA-specific meshes
from the 3BA patch. They are not additions — each writes to the **same output path** as its CBBE
twin, so building both in one batch means one silently overwrites the other. Ten more pairs collide
the same way between `[SMP]` and plain CBBE variants: 545 sets resolve to only **525 distinct output
paths**.

Two conflict-free groups written, 525 members each, one set per output path:

- **`[SunJeong] Ninirim Collection - Authoria (3BA + SMP)`** — prefers the author's 3BA-specific mesh
  where one exists (10), then the SMP variant (10), then plain CBBE. **Use this one.**
- `[SunJeong] Ninirim Collection - Authoria (3BA, no SMP)` — same, but plain CBBE for the 10 SMP
  pairs. For A/B if an SMP piece misbehaves.

Cute Adventurer needed no work — its groups already cover everything, and the SMP patch's
sliderSets correctly win over the base.

## UBE — converted

BodySlide was built by the user into `Authoria - Bodyslide Output - UBE` (1045 nifs). Converted with
`--mod` + `--out` into its own mod, **`Authoria - UBE Converter Output - Ninirim`** (3.2 GB, 1032
meshes, `[SunJeong] Ninirim Collection UBE patch.esp` — 610 records, ESL, form 44, 0 dangling refs).
The big hand-curated `Authoria - UBE Converter Output` was never touched.

### The 18 blocked units — a real bug in the mod

The first run reported 18 units `blocked … winning female mesh not found as a loose file (BSA-only or
missing)`. The meshes were plainly on disk, so that message was misleading. Cause, from
`conversion_report.json` → `mesh_actions[*].source`:

- the 529 that converted have paths like `ninistuff\Linkle\belt_1.nif`
- the 18 that blocked have `Meshes\ninistuff\Linkle\belt_1.nif`

Model paths are already relative to `Data\Meshes\`, so the redundant prefix makes the converter look
for `Meshes\Meshes\…`. Skyrim tolerates it at runtime; the converter does not. Exactly **18 of 1877**
ARMA model paths in the plugin carried it — a precise match with the blocked list. Stripped from
`MOD2`/`MOD3`/`MOD4`/`MOD5` in place (backup `.bak-meshprefix-20260818`) and re-run. Affected sets:
Linkle (10), Elendil (4), Elwing (4).

### 53 zero-filled meshes — the important one

After the run reported `blocked: 0` and everything reused, a spot check found the converted
ShiningWill meshes were **entirely zero bytes**. A whole-output header scan found **53 corrupt nifs
across 9 outfits** (CharlesRene, DeathLady, Gotha Rensa RedGold + Nature, ShiningWill, Karlstein,
Bless RB 0007, Orwen, Sister).

Cause: the first run was killed mid-write. The tool's incremental reuse checks only that an output
file *exists*, never that it is valid, so every later run counted the wrecked files as
`reused_incremental` and reported a clean summary.

Deleted the 53 and re-ran with `--reconvert`. Final state: **1066 nifs, 0 corrupt**, 539 genuinely
converted, 0 blocked, 0 errors.

**Standing check after any conversion** — a real mesh begins with the ASCII `Gamebryo`:

```python
with open(p, "rb") as f: ok = f.read(16).startswith(b"Gamebryo")
```

The tool's own summary will not tell you. `housecarl_nif_inspect` is the other tell — it refuses the
file with "NiflySharp could not parse this mesh (Load returned 1)".

Swept the pre-existing outputs too — `Authoria - UBE Converter Output` (3020), `Bodyslide Output -
UBE` (3853) and `- 3BA` (1586): **all clean**, the damage was confined to this run.

### SMP survived

All 10 Ninirim SMP outfits keep their `HDT Skinned Mesh Physics Object` link through conversion
(Ananta, Bless 0022 ×2, Damaged Feather, DragonRises, ShiningWill ×2, Summer Casual ×3). The two
that first read as "physics lost" were simply the zero-filled files.

### Two gotchas re-running the converter

1. **A re-run no-ops once the previous output is enabled.** It scans active SkyPatcher armour INIs
   and skips any ARMA already covered — its "converter-output roots excluded" rule doesn't recognise
   a custom `--out` folder. Symptom: `minted: 0`, `skipped (already patched): 610`, done in ~15s.
   Disabling the mod in `modlist.txt` is **not** enough; the INI has to be physically moved out of
   the output folder.
2. **The tool registers its own output mod at the top of `modlist.txt`, disabled** — above the
   FWMF/LOD blocks, breaking the "nothing above the outputs" rule, and inert until enabled. Removed
   and re-inserted enabled beside `Authoria - UBE Converter Output`. It also pruned a modlist entry
   whose folder no longer existed (`houseCARL_SpellHotbarMCM_read`) — verified against the backup,
   not damage.

Cute Adventurer needs no conversion — it ships native `!UBE` meshes and its own UBE patch ESP.

## UBE — original dry run

Dry run (`--mod` single-plugin mode, writes nothing): **610 units in scope, 610 mintable, 0 skipped,
0 races-only fallbacks**, output would be `[SunJeong] Ninirim Collection UBE patch.esp`, ESL-flagged.

**The real run is deliberately not done yet, because order matters.** The converter reads the
load-order-winning loose mesh. `Authoria - Bodyslide Output - 3BA` sits at priority 118 and the
outfit sources at 1685+, so once BodySlide builds the group the built meshes win and become the
conversion source. Converting now would bake the mod's default CBBE shape into the UBE meshes
instead of your preset, and the whole run would have to be redone.

The existing `Authoria - UBE Converter Output` (8.1 GB, hand-curated — it has a
`_removed-from-skypatcher` folder) will **not** be touched: the run uses `--mod` + `--out` to write
Ninirim into its own separate output mod.

Command to use once BodySlide has built:

```
"C:\1. AUTHORIA\tools\CBBE to UBE\Authoria-DaysTool.exe" "C:\1. AUTHORIA" --profile "DEEZ CS NUTZ" --mod "[SunJeong] Ninirim Collection.esp" --out "C:\1. AUTHORIA\mods\Authoria - UBE Converter Output - Ninirim" --esp-name "Authoria - Output - UBE Ninirim.esp" --reconvert --yes
```

Cute Adventurer needs no conversion — it ships native `!UBE` meshes and its own UBE patch ESP.

## No museum, no recipes (second pass)

Source plugins edited **in place**, backups kept beside them (`.bak-norecipes-20260818`,
`.bak-pretemper-20260818`). Master lists deliberately untouched — the Requiem patches align their
own master list to the source's, so dropping a master would shift every FormID index.

| Plugin | Dropped | Records left |
|---|---|---|
| `[SunJeong] Ninirim Collection.esp` | all **1148** crafting recipes | 2493 → 1345 |
| `Cute Adventurer Outfit.esp` | 9 forge recipes + the whole WRLD tree (4 records) | 45 → 32 |

The Cute Adventurer WRLD tree was a Riften cell + landscape + a placed **crafting manual**. Removing
it also kills a `RiftenOrigin` CELL override that existed only to carry that one book — the classic
way a patch quietly steals lighting from a city overhaul.

**Ninirim now has 1345 records, under the 2048 light window**, so it *could* be ESL-flagged and give
back its full slot. Not done: compaction renumbers FormIDs and would break the Requiem patch, which
would then need rebuilding. Say so if you want it.

### Cute Adventurer: tempering kept, boots are light armour

The 6 armour-table tempering recipes were kept; the 9 forge recipes went. Each tempering recipe was
re-gated behind **Craftsmanship**, with the condition bytes lifted verbatim out of Requiem's own
`REQ_Temper_Light_Leather_Feet` so the encoding is right by construction. Material was already 1
leather, matching Requiem.

The three boots are now real light armour, derived live from `REQ_Light_Leather_Feet`: **armour 45,
value 30, weight 1.5**, keywords `ArmorLight` + `REQ_ArmorSet_Leather` + `ArmorBoots` +
`VendorItemArmor`. The tempering keyword is left for the Reqtificator to assign.

> Caught on the first attempt: the boots kept their old clothing keywords *alongside* the new armour
> ones. The builder now strips the clothing class whenever a piece is restored to armour.

Final tally across both patches: **618 records — 615 clothing, 3 light armour, zero invariant
failures.**

Still clothing: the 3 dresses and 3 shorts. Their tempering recipes are therefore **inert** (nothing
to temper at zero armour) — kept because tempering was asked for wholesale.

### Header form version

Both hand-written patches shipped **form version 0**, which MO2 reports as an unported Oldrim form
43 plugin. Only the header stamp was blank — every record inside was already form 44. Fixed in the
writer (offset 20 → 44) and re-verified on all four plugins. This was *not* a houseCARL fault; its
own patches in this order all measure 44.

## Nibenean Strider — conversion confirmed

Asked separately. **Fully converted**: all 11 of `NibeneanStriderbyXtudo.esp`'s armours are covered
by a UBE SkyPatcher line, the minted ARMAs are in the conversion report, and the `!UBE` meshes exist
on disk. The conversion sourced `Authoria - Bodyslide Output - 3BA`, i.e. a real BodySlide-built
mesh rather than the mod's BSA — which is the good outcome, since BSA-only sources come out as
`blocked` units that keep their source mesh.

## Open Waist — older conversion kept (user's call)

Ninirim Collection contains the Open Waist outfit that the standalone `[NINI] Open Waist` mod also
provides, so there are now two UBE conversions writing the same `!UBE\ninistuff\Open Waist\` paths.

**Decision: keep the older one.** No change was needed — `Authoria - UBE Converter Output`
(priority 167) already outranks `Authoria - UBE Converter Output - Ninirim` (168), so the older
conversion wins every shared path. It also ships `ribbon_0/1.nif`, which the new run never produced
(the ribbon belongs to the standalone mod, not the Collection's copy). `lower` and `shoes` are
byte-identical between the two; only `upper` / `upper slutty` differ.

⚠ This rests purely on mod priority. If the two output mods are ever reordered, the Open Waist look
silently changes. The 8 shadowed nifs in the Ninirim output could be deleted to make the intent
explicit — not done, since that would leave Open Waist without a UBE mesh if the older output is
ever disabled.

The stale `Authoria - Bodyslide Output - NSFW` build (21 July) that wins `meshes\ninistuff\Open
Waist\` is **not** relevant to the player: UBE actors read the `!UBE\` path. It only feeds non-UBE
actors and the conversion source. Left alone.

## Superseded — stale Open Waist build (resolved above)

`Authoria - Bodyslide Output - NSFW` (priority 107) holds 10 `ninistuff\Open Waist` meshes from
**2026-07-21** that outrank the fresh build in `Authoria - Bodyslide Output - UBE` (priority 115).
Ninirim Collection ships that outfit too, so the old build wins and the new one never shows. Left
alone — deleting from the NSFW output was not authorised.

## Load order placement

- Outfit plugins after `[NINI] Open Waist.esp`; the Cute Adventurer UBE patch in the UBE-patch block.
- Both Requiem patches after `Authoria - Patch - Serana UBE Face.esp` — after
  `Requiem for the Indifferent.esp`, and above the PG/DynDOLOD/FWMF output block.
- `plugingroups.txt` updated: outfits → `Gameplay - Armors and Weapons`, UBE patch →
  `Visuals - Character Visuals`, Requiem patches → `Authoria - Late Custom Patches`.

## Still open

1. BodySlide batch-build of the new group (must run under MO2).
2. UBE conversion run, then register its output mod + ESL plugin.
3. After conversion, re-check SMP node trees — the UBE converter flattens them, and 10 Ninirim
   outfits are SMP variants.
4. Reqtificator re-run is *not* required for these records — they now carry no armour-set keyword,
   so the build pass has nothing to assign. It is safe to re-run whenever convenient.
