# Authoria - Vindicator DDV Backpack - Requiem — patch ledger

Date: 2026-08-21. Profile: DEEZ CS NUTZ (enabled; added disabled in the other 3).
Plugin: `Authoria - Vindicator DDV Backpack - Requiem.esp` — ESPFE, 3 originating records + 97 overrides.
Position: immediately BEFORE `Requiem for the Indifferent.esp` (group: Authoria - Late Custom Patches),
so the next Reqtificator run folds tempering/resist assignments over these values. Do NOT move it
after RFTI — that would bury the build pass's assignments.
Masters: Skyrim, Update, UBE_AllRace, VindictorArmor, DDV - Arcane fencer, _Fuse00_Backpack,
VindictorArmor UBE patch, _Fuse00_Backpack UBE patch. No Requiem.esp master — every referenced
REQ perk/keyword lives in Skyrim.esm FormID space (Requiem overrides vanilla records); load-after
Requiem is guaranteed by the hand-curated order.

## Vindicator Armor (VindictorArmor.esp — Heavy + heel-sounds FOMOD variant)

The author shipped it Requiem-aware: REQ_ArmorSet_OrcishHeavy on all 14 pieces, part keywords on
exactly one piece each (ArmorCuirass on the slot-56 plate, ArmorHelmet on the slot-42 brooches,
gauntlets/boots standard), PerkFistsOrcish on the gauntlets, Survival_ArmorWarm, and temper recipes
already gated behind a Requiem perk. Only the armor ratings were vanilla-scale.

**Decision: ×10 the author's own AR distribution** (preserves the modular layered design; full
14-piece stack = 990 vs Requiem's Orcish 4-piece 900; every piece far under the Reqtificator's
per-slot caps). Values/weights kept (set totals ≈ REQ Orcish set). Keywords untouched except
Frostfall warmth/coverage added to the three standard-slot pieces.

| Piece (slot) | AR old → new | Frostfall |
|---|---|---|
| Leotard (32) | 10 → 100 | Fair/Fair |
| Gauntlets (33) | 10 → 100 | Poor/Poor |
| Sabatons (37) | 15 → 150 | Poor/Fair |
| Cuirass overlay (56) | 16 → 160 | — |
| Pauldrons (57) | 10 → 100 | — |
| Greaves (38) | 6 → 60 | — |
| Cuisses (54), Apron (49) | 6 → 60 | — |
| Brooches L/R (42) | 4 → 40 | — |
| Collar (45) | 4 → 40 | — |
| Wristguard (34), Vambraces (59) | 3 → 30 | — |
| Harness (48) | 2 → 20 | — |

Recipes: all 14 forge recipes keep the crafting-manual gate (manual placed in Castle Dour) and gained
`HasPerk REQ_Smithing_OrcishSmithing`. All 5 temper recipes re-gated to Orcish Smithing alone
(replacing the enchanted-check OR Advanced Blacksmithing pattern) with 1 orichalcum ingot input
(was 1 steel), matching REQ_Temper_Heavy_Orcish_* verbatim.

Castle Dour CELL override checked: 41 plugins touch it, winner is a late Authoria patch; Vindicator's
copy is deeply buried — no lighting clobber. The placed manual REFR survives regardless.

Dispositions (60 records): 14 ARMO + 19 COBJ patched; 14 ARMA cosmetic-skip; 9 KYWD (B.O.O.B.I.E.S.
icon keywords) skip; 1 BOOK (manual) skip; 1 STAT skip; 1 CELL + 1 REFR checked-skip. 33+27=60 ✓.
UBE patch esp (14 ARMO overrides + 14 ARMA): armature carriers, preserved via winner-derived copies.

## DDV - Arcane Fencer (male outfit, HIMBO; SAM variants unused)

Light armor at **leather tier** for the functional pieces (derived live from REQ_Light_Leather_*),
clothing frames for the rest. Author's keyword soup (ClothingBody+ArmorCuirass mixed, jewelry
keywords on belt accessories, VendorItemAnimalHide everywhere) replaced with coherent Requiem sets.

| Piece | Treatment | AR / Val / Wt |
|---|---|---|
| Top, Top Black (leather version, 32+34+38) | light cuirass, leather set | 150 / 100 / 5 |
| Top 2 ×2 (cloth version) | clothing frame + ClothingBody | 0, values kept |
| Boots ×2 (37) | light boots, leather | 45 / 30 / 1.5 |
| Gloves ×2 (33) | light gauntlets, leather (no fist perk — light) | 45 / 30 / 1.5 |
| Hood ×2 (31+41) | light helmet, leather (comparable: REQ Leather Hood) | 60 / 40 / 2 |
| Hat ×2 (42) | clothing frame + ClothingCirclet | 0 |
| Pants ×2 (44) | clothing frame | 0 |
| Cape ×2 (51) | clothing frame + FrostfallIsCloakCloth | 0 |
| Accessories ×4 (47) | clothing frame | 0 |

Frostfall: tops Fair/Fair, boots Poor/Fair, gloves+hood Poor/Poor.
Recipes: all 39 (20 forge + 19 temper) gated behind `HasPerk REQ_Smithing_Craftsmanship`
(author shipped them condition-free). Tempers on clothing frames are inert by design.

Female ARMA models are vanilla bandit-gear placeholders (author's stub) — the outfit is male-only in
practice; a female wearing it renders bandit pieces. UBE conversion deliberately NOT done (it would
mint ARMAs rendering bandit meshes).

Dispositions (88): 20 ARMO + 39 COBJ patched; 20 ARMA + 9 TXST cosmetic-skip. 59+29=88 ✓.

## Traveler's Backpack stack

Active plugin = the All Colors ESPFE replacer (4 color ARMOs). Extra Color rars are byte-identical
to the patch's own prefixed textures → installed as 3 DISABLED one-color replacer mods (enabling one
recolors the DEFAULT backpack only; not needed with the All Colors patch).

- 4 ARMOs: keywords normalized to the Reqtificated-Campfire backpack pattern
  [ArmorClothing, VendorItemClothing, MagicDisallowEnchanting, WAF_ClothingPouch]
  (dropped: REQ_ArmorSet_Leather — was pulling a pointless tempering assignment — and ClothingBody).
- Carry enchantment: **+100 → +35**, matched to Requiem's own Campfire backpack (its Requiem patch
  sets 35). Single ENCH edit covers all 4 colors. Revert = delete the ObjectEffect override.
- **UBE patch ghost fixed**: `_Fuse00_Backpack UBE patch.esp` overrode FormID D514 from the ORIGINAL
  full esp — a FormID that cannot exist in the light All Colors replacer (injected ghost). Removed
  in place (backup `.bak-ghostfix-20260821` beside it); the esp now carries only the UBE ARMA.
- **UBE for all 4 colors**: 3 new ARMAs minted in this patch (_Fuse00_BackP_UBE_W / _BL / _G) —
  clones of the UBE ARMA (15 UBE races, !UBE meshes) carrying each color's texture swaps. Verified
  the !UBE mesh has identical shape order to the original (swap indices 0/1/2 line up). Armature
  adds: default ARMO → original UBE ARMA; W/BL/G ARMOs → the minted color ARMAs.

Dispositions (19 + UBE patch 2): 4 ARMO + 1 ENCH patched; 1 MGEF, 4 ARMA, 9 TXST skip; ghost ARMO
removed; UBE ARMA kept. ✓

## ORF keywords (in `Authoria - ORF Patches`)

- `ORF - Vindicator Armor_ORF_KID.ini`: Leotard (the slot-32 outer) = Black + Sturdy + Tight.
  Colour read by eye off the winning texture: dark blackened plate, brass trim.
- `ORF - DDV Arcane Fencer_ORF_KID.ini`: default tops = Blue (navy w/ silver embroidery) + Classy;
  black tops = Black + Classy; leather-version tops also Leather; hoods = Hooded; skirt-bearing
  accessory (mesh has a Skirt shape; Accessories 2 does not) = ShortSkirt.
- Backpack: NO keywords — slot 47, and colour/character are slot-32-outer-only by the build rule.
- FormID-addressed, zero-padded, matching the existing pack format.

## BodySlide groups (mod `Authoria - Vindicator DDV Backpack - BodySlide Groups`)

One XML, 5 groups, one member per output path, split per body lane so each builds under its preset:
- Vindicator 3BA / UBE / HIMBO (12 members each) — **Low Heels** sabatons+greaves chosen (the
  high-heel twins write the same output paths; no Heels Fix SKSE mod is installed).
- DDV Arcane Fencer HIMBO (11 members) — non-SAM sets only (SAM twins share output paths).
- Fuse00 Backpack UBE (1 member).
Dint999 Combined sliders deliberately excluded from any group — its sets write the reference body
paths (femalebody/hands/feet) and would overwrite the 3BA body build if batch-built.

## Post-build follow-up (2026-08-21, after Reqtificator + BodySlide runs)

- RFTI fold verified: Vindicator/DDV winners keep the patch's values and gained
  REQ_Armor_Resistance_Ranged_Tier5/Tier1 + tempering keywords; UBE armatures preserved. Backpack
  records were not copied by the Reqtificator (no set keyword) — this patch still wins them. Correct.
- All 4 backpack UBE ARMAs (original + 3 color mints) repointed: WorldModel.Female.File now reads the
  user's BodySlide-built mesh at `meshes\!UBE\armor\[UBE]_Fuse00_Backpack\` — the author's .osp
  builds there, NOT at the prebuilt `!UBE\Fuse00\Armor\Backpack\` path the ARMA originally read.
  Future rebuilds of the "Authoria - Fuse00 Backpack (UBE)" group land in the right place now.
  Built-mesh shape order verified identical to the prebuilt (index swaps safe).
- Vindicator ships NO prebuilt body meshes (only brooches + ground models) — every piece requires its
  BodySlide build. 3BA + UBE + DDV + backpack groups were built (into "Authoria - Bodyslide Output -
  UBE"); the **Vindicator HIMBO group was NOT built** — male world models (`VA_*_m`) missing, so the
  set is invisible on male wearers until that group is built.
- Vindicator/DDV ARMAs carry no FirstPersonModel overrides — no raw-path first-person trap here.

## Verification

check_errors across all 8 touched/new plugins: 0 dangling refs, 0 missing masters (the 2 excluded
plugins are the known pre-existing broken DBVO fixes). Census after: DEEZ CS NUTZ 240/254 —
unchanged; every new plugin is light. Minted ARMAs re-verified by EditorID post-ESL-compaction.
