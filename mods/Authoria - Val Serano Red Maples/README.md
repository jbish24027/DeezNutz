# Authoria - Val Serano Red Maples

Created 2026-08-20. Keeps the Val Serano quest mod's red maples RED all year.

## Why this mod exists

The user wants the Val Serano maples red. The red override originally lived in
`Authoria - RMF Purple Retint` ("round 9", 2026-08-15). That hub was disabled on
2026-08-17 for the flora-color investigation and retired permanently on 2026-08-19
after the CS Snow Cover hue bug was fixed at the shader level. Retiring the hub
also silently retired the maples, so the trees reverted to
`Val Serano - Seasons`' green summer leaves. This mod carries ONLY the maple
files so the two concerns can never be coupled again.

## Contents

`textures/Axarien/Val Serano/items/redmaple/`
- `treefloweringbranch02.dds` (base - autumn reads this; also overrides the copy in `AX ValSerano - Textures.bsa`)
- `treefloweringbranch02_SPR.dds` (spring)
- `treefloweringbranch02_SUM.dds` (summer - this is the file that fixes the reported green)

All three are byte-identical (md5 `acde50a799167d3d356834e241159609`), copied
unmodified from the retint hub's round-9 output: original screaming-red atlas
dimmed by S x0.70, V x0.62 (user: "much less bright"). Measured mean: H0 S0.63 V0.14.
Locked source PNG: `Authoria - RMF Purple Retint/_source-pngs-locked/treefloweringbranch02_round9_medium.png`.

## Deliberately NOT included

- `treefloweringbranch02_WIN.dds` - winter stays seasonal (Val Serano - Seasons' variant), matching round-9 scope.
- Normal map - untouched, color lives in the diffuse.

## Placement

Must load ABOVE (lower priority line than) `Val Serano - Seasons` in the left pane.
It is inserted directly above the disabled `Authoria - RMF Purple Retint` line,
the exact spot from which these files used to win.

## Known follow-up

`Authoria - TexGen Output` still holds tree-LOD billboards baked from the OLD
bright-red atlas, so distant maples render brighter red than near ones until
TexGen + DynDOLOD are rerun (pre-existing gap from round 9).
