# Magic Pariah (Meadowlark physics), Burlesque Dress, BodySlide group, Requiem patch — 2026-09-03

MO2 was closed the whole time. Nothing in the profile files was touched: the four new mod
folders are on disk and unlisted until MO2 is refreshed and they are enabled.

## Mods added (4 folders)
| Mod folder | Contents |
|---|---|
| `Magic Pariah - Meadowlark Physics` | Magic Pariah Fit (Nexus 155585, v1.0) with the skirt re-rigged to Meandering Meadowlark's (181245, v1.101) physics; ESP compacted + ESL |
| `Burlesque Dress` | Burlesque Dress (Nexus 171116, v1) straight from the archive; ESP already ESL |
| `Authoria - BodySlide Group - Magic Pariah and Burlesque` | one group, 13 members, one per output mesh |
| `Authoria - Magic Pariah and Burlesque - Requiem Clothing` | one ESL patch for Burlesque (Magic Pariah needed none) |

Not installed: the Meandering Meadowlark archives themselves (only its skirt rig was borrowed),
the Dingy retexture, the MM/MP texture and Blender resources.

## 1. Magic Pariah with Meadowlark physics
The user wanted the old outfit's look (corset top, knee-length skirt) with the new mod's physics.
Both mods are by blickRARRI; the old one's page marks it deprecated with open permissions.

What actually differed: the hat physics xml is byte-identical in both mods, and the top already
has its own sleeve physics. The whole gap was the skirt. Meadowlark = 12-column x 6-row bone
chain under the pelvis, tuned constraints, thigh/calf/feet colliders and an invisible collision
skirt. Magic Pariah = 8 x 5 chain with zero-stiffness constraints and an xml that names shapes
(`skirt_top`/`skirt_bottom`) that do not exist in its mesh, so its skirt never collided.

Done in code (`_tools\magic-pariah-mm-rig\`: nifrw.py block-level NIF rewriter, graft.py,
make_xml.py, verify.py, assemble.py), all byte-exact round-trip tested:
- Meadowlark chain rows 1-4 (the MP hem sits at z 38, between rows 3 and 4) + CollThigh +
  CollCalves + the collision skirt cut below z 36 copied into the MP skirt mesh; skinning bind
  transforms agreed to 0.0009 across the two files, so the bone tree copied verbatim.
- Skirt Lower / Skirt Upper re-weighted to the new chain by nearest neighbour from Meadowlark's
  own skirt layers (mean source distance 1.1 units). Positions, UVs, triangles untouched, so the
  BodySlide .osd data still applies. Partitions set to slot 49 to match the skirt ARMA.
- Removed from the skirt: the old chain, the rigid `Cube` hip collider, and **`UniButt`, a full
  3BA body that shipped inside the slot-49 skirt** (the slot-32 top carries its own body, so the
  stock mod double-rendered the body).
- New `MagicPariahSkirtHDT.xml` = Meadowlark's numbers, rows 1-4, no dangles/feet collider; two
  MM typos fixed (`sk_back6` in the row-4 threshold list, `NPC R Thigh [LThg]`).
- houseCARL's nifly parser (BodySlide's own library) reads the result clean: 141 blocks, no
  unknown blocks, all 7 shapes/partitions/bones as intended.
- `Magic Pariah.esp` compacted to ESL in place (FormIDs 0x800-0x807), check_errors clean.

## 2. Burlesque Dress
19 pieces in two colours (corset 32, skirt 52, bustle 57, sleeves 58, gloves 34, bracelet 60,
necklace 35, hat 42, boots 37). Red variants reuse the meshes with texture sets. Plugin already
ESL, form 44, no changes needed.

## 3. BodySlide group
"Authoria - Magic Pariah + Burlesque 3BA": 4 Magic Pariah + 9 Burlesque projects, 13 distinct
output paths. Burlesque ships two skirt projects writing the SAME file (static vs SMP); only the
SMP one is in the group. Every plugin model path matches a project output and none carries a
leading `meshes\` prefix (the converter trap from 08-18). Converter is single-plugin mode, so the
later UBE run is two scoped runs (`--mod` per plugin, own `--out` folder each).

## 4. Requiem
Freshness probe: Iron Sword chain Skyrim → USSEP → Requiem.esp → Requiem for the Indifferent.esp.
**Magic Pariah: no patch.** All four pieces already ship Clothing / AR 0 / clothing keywords /
no armor-set keyword — the Reqtificator's scaler skips Clothing and no keyword rule fires.
**Burlesque: `Authoria - Burlesque Dress - Requiem Clothing.esp`** (ESL, 57 records, masters
Skyrim/Update/Dawnguard/Dragonborn/Burlesque/Requiem; written by verbatim record copy with the
master-order trick, so no FormID remap):
| Records | Change |
|---|---|
| 19 ARMO | Clothing frames per the Armor Folder convention: AR 0 (corsets were 10), `REQ_ArmorSet_Iron` stripped from 15 pieces, body 20/1.0, hands+hats 10/0.5, boots+accessories 10/1.0, necklace+bracelet at Requiem's silver-garnet tier 440/0.25 with jewelry keywords. Red bracelet lost a stray vanilla GoldAmuletAA armature link (mod bug). |
| 19 COBJ temper | workbench → `REQ_DisableRecipe` (Requiem disables every clothing temper recipe the same way) |
| 15 COBJ forge (clothing) | inputs kept (1 iron ingot + 2 leather strips, book-gated) + `HasPerk(Craftsmanship)` |
| 4 COBJ forge (jewelry) | 2 leather strips → 1 silver ingot + 2 flawless garnets + `HasPerk(Advanced Blacksmithing)`, cloned from `REQ_Forge_Amulet_SilverGarnet`; book gate kept |
| 1 COBJ book, 1 BOOK, 19 ARMA, 10 TXST | left alone (cosmetic / plain book) |
Reconciliation: 88 enumerated = 19 + 38 patched + 1 + 1 + 19 + 10 dispositioned. No REQ_NULL,
no Reqtificator outputs hand-stamped. check_errors off-order: the only findings are the 38
links into Burlesque.esp, which is simply not enabled yet; every target exists in that file.
The patch is an input to the Reqtificator pass, like every armor patch here.

## 5. Enabled in MO2 (user's ask, MO2 closed)
`_tools\requiem-clothing-patch\enable_mods.py --apply`; backups `*.bak-pariah-20260903` beside all
four files in every profile. Same neighbours in all six profiles:
- `Magic Pariah - Meadowlark Physics` + `Burlesque Dress` directly below `Sera's Armor` in the
  "Armor and Weapons - Modded" block (Main/NSFW park Sera's Armor at the top, so there the pair
  sits at the head of that block instead).
- `Authoria - BodySlide Group - Magic Pariah and Burlesque` next to the Ninirim BodySlide Groups mod.
- `Authoria - Magic Pariah and Burlesque - Requiem Clothing` next to the Ninirim Requiem Clothing
  patch in "Authoria - Custom Patches".
- Enabled in DEEEZ NUTTZZZ, DEEZ CS NUTZ, DEEZ CS NUTZ - PBR, PICTA EXPERIMENT (where Sera's Armor
  is enabled); added disabled in the two Requiem Reforged profiles. The four stray disabled lines
  that had appeared at the very top of the PBR modlist (above Testing_separator) were removed.
- Plugins (four enabled profiles): `Magic Pariah.esp` + `Burlesque.esp` after `KW_SerasArmor.esp`
  (group Gameplay - Armors and Weapons); the Requiem patch after
  `Authoria - Reqtificated - Armor Folder.esp` (group Authoria - Reqtificated, before RftI).
  plugingroups.txt updated; header-run count unchanged in every profile.
- Checks: modlist lines 1-37 and the loadorder tail from Synthesis Gameplay carry no new name;
  houseCARL sees all four mods enabled and three plugins active; check_errors on the three
  plugins: 0 dangling, 0 missing masters. Outfit Wheeler reindexed (21 rawIDs rewritten for the
  light-index shift), calibrate 77 match / 0 mismatch.

## 6. UBE conversion (run by me at the user's request, after their BodySlide build)
The user built the group into `Authoria - Bodyslide Output - UBE` (24 nifs, all valid; the
grafted skirt came through with its 48 rig bones, 7 shapes and physics link). Two scoped runs of
`tools\CBBE to UBE\Authoria-DaysTool.exe` (dry run first, both clean):
| Run | Output mod | Result |
|---|---|---|
| `--mod "Magic Pariah.esp"` | `Authoria - UBE Converter Output - Magic Pariah` | 4 units, 4 UBE ArmorAddons minted, 6 meshes (top/skirt/boots x2), `Magic Pariah UBE patch.esp` ESL, 4-line SkyPatcher ini |
| `--mod "Burlesque.esp"` | `Authoria - UBE Converter Output - Burlesque` | 19 units, 19 minted, 16 meshes, `Burlesque UBE patch.esp` ESL, 19-line ini |
Both outputs validated: every nif starts with `Gamebryo` and parses; the 3BA bodies inside the
tops/corset/boots were replaced by (or dropped for) the UBE body; the converted skirt keeps the
Meadowlark rig; physics links re-pointed to xml copies beside the converted meshes; VirtualGround
survived in both Burlesque xmls (the 08-21 trap did not fire); the corset alt-texture index was
remapped by the tool itself; check_errors on both patches 0/0; the converter changed nothing in
any profile file this time (no top-of-list registration, no pruning).
**New converter defect found:** it re-encodes the UTF-8 BOM of a copied SMP xml as the three
characters `ï»¿`, so the copy starts with junk before `<?xml`. Fixed on the two Burlesque
copies (`*.bak-bom-20260903` beside them). The big hand-curated `Authoria - UBE Converter
Output` carries 18 xml files with the same defect from earlier runs — reported, not touched.
Also: the tool logs freshly converted meshes as "incremental ... reused" (accounting quirk; the
worker lines above the log header are the real conversions).
Registered with `enable_ube.py` (backups `*.bak-ube-20260903`): both output mods directly above
`Authoria - UBE Converter Output - Sera` in every profile (enabled where that one is), both
plugins after `KW_SerasArmor UBE patch.esp` in the "Authoria - Outputs" block of the four enabled
profiles, plugin groups updated, header runs unchanged, protected head/tail clean. Outfit Wheeler
reindex: 0 rewritten (the new plugins load after every outfit plugin), calibrate 77/0.

## 7. Skirt physics tune v2 (user after testing: top good, sleeves good, "skirt smp too rigid")
Two causes: (a) the weight transfer kept Meadowlark's hip-region thigh/pelvis weighting, which on
a knee-length skirt reaches the middle of the skirt (10-25 % thigh share between z 48 and 66);
(b) Meadowlark's joints are tuned for a heavy floor-length skirt (per-link freedom x -0.03..0.3,
y +-0.03, z +-0.05, springs 60, damping 0.9, ring springs 50-100, bone angular damping 1.0).
Fix, `_tools\magic-pariah-mm-rig\retune.py` + make_xml.py v2:
- Weights: body/thigh weight fades out between z 68 and 60 and goes to the chain; below z 60 the
  skirt and its collision proxy are 100 % chain-driven. Applied to the ShapeData mesh, both
  BodySlide-built meshes and (via a converter re-run) both !UBE meshes; positions untouched.
- Joints: per-link freedom now x -0.25..0.4 / y,z +-0.2 (row 2), -0.3..0.45 / +-0.25 (row 3),
  -0.35..0.5 / +-0.3 (row 4); springs 15/10/6 (was 60/60/50), damping 0.5/0.4/0.3; ring springs
  20/15/12-20 with +-0.08-0.2 angular play; bone angular damping 0.5, gravity 0.9/1.0.
- Converter re-run trap 3 confirmed again: with the output enabled the re-run skipped all 4 units
  ("already covered by an active SkyPatcher INI"); moved the INI aside, `--reconvert`, and the
  tool rewrote a byte-identical INI + ESP and 6 fresh meshes. Profiles untouched. xml copy in the
  output equals the v2 mod xml. check_errors clean. Backups: `*.bak-stiff-20260903` beside the
  three meshes and the xml.

## Verification summary
- Skirt mesh: byte-exact re-serialize, all refs valid, positions unchanged, packed weights ==
  NiSkinData, bone-band picture sane, nifly parse clean.
- Group: 13 member names all exist, 13 distinct outputs, xml parses.
- Patch: 57 records re-read with invariants (0 failures), Mutagen read of corset / jewelry
  recipe / red bracelet matches, ESL + form 44 stamped.
