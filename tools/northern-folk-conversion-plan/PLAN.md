# Northern Folk: 3BA, OBody and loose SMP conversion plan

Prepared 2026-10-19. Planning only; no outfit meshes, plugins or distribution rules changed by this plan.

## Intended result

Consolidated priorities and current requirements are maintained in [MASTER-PLAN.md](MASTER-PLAN.md).

**Mandatory output rule:** every 3BA refit must use its SMP project/version in our outputs. Verify both the selected BodySlide project and the final MO2 mesh winner retain cloth physics and OBody morphs. Static builds must not overwrite SMP builds. Where no SMP version exists, creating and validating it remains required work before the refit is complete.

Keep Northern Folk's original clothes, colours, coverage and NPC assignments. Convert female garments to the installed CBBE 3BA reference, provide complete BodySlide projects and OBody morphs, and give hanging skirts/aprons free cloth movement inspired by the user's Helga dress. Prove one garment in game before expanding the pack.

## Verified local starting point

- Source: `mods/Clothes of the Northern Folk`, Nexus 179901, installed version 1. It has meshes, textures and a plugin, but no BodySlide projects.
- 2,479 NIF files on disk; 281 names end in `_f_1.nif` and 292 in `_m_1.nif`. These are filename counts, NOT unique garments or conversion counts. Ground meshes, accessories and recolours need classification.
- Eight named regional folders occur in each of the Bunad and Viking families: Beltestakk, Hardanger, Nordland, Romerike, Setesdal, Sigdal, Telemark and Valdres. Geometry equivalence remains to be measured.
- Fralia receives CNFVikingHardangerBlack, using `Viking_Hardanger_black_f_1.nif`. Its surveyed skirt is part of the torso; it has no SMP link or moving bones.
- Installed Outfit Studio reports 5.7.1.0. Current upstream documentation includes automation and physics-preview capabilities; do not assume these exist in this executable. Verify capability before choosing automation. A separate pinned tool build is preferable to replacing the working installation if newer features are needed.
- Installed 3BA reference project: `mods/CBBE 3BA (3BBB)/CalienteTools/BodySlide/SliderSets/SE 3BBB Amazing.osp`.
- BodySlide's current output directory points to `Authoria - Bodyslide Output - UBE - My Builds`. This conversion needs its own explicit output directory so 3BA builds are not mixed into that UBE-labelled output.
- Authoria's OBody body-type filter blocks UBE from normal distribution. Ysolda uses a UBE race; 3BA conversion alone cannot repair her missing outfit.
- Current FSMP config uses automatic skeleton budgeting, maximumActiveSkeletons=5 and budgetMs=3. Cloth performance and whether an actor is being simulated must be checked separately from rig correctness. Do not raise global budgets blindly.

## 1. Inventory and establish reproducible inputs

Map every relevant ARMO/ARMA to worn male/female meshes, texture swaps, weight pairs and NPC distribution. Use houseCARL for records and virtual-file winners. Hash original assets and record the 3BA reference version.

Group variants only after comparing vertex positions/order, triangles, shape names, partitions, UVs and weights. A shared filename pattern is insufficient. Keep a manifest mapping every original output path to a conversion family and validation status. Preserve individual textures/materials and beast-race variants. Accessories receive fitting/morph work where needed, not automatic skirt rigs.

## 2. Prototype Fralia's complete outfit

Start with Black Hardanger Viking attire and its stockings/boots. Fit the garment to the actual installed 3BA neutral reference, using an appropriate vanilla-to-CBBE conversion reference as a starting point if available. Preserve the loose silhouette and closed coverage. Replace exposed vanilla body sections with the matching 3BA body; eliminate duplicate bodies and check neck, wrists and ankles.

Finalize necessary skirt subdivision and shape separation before producing final morph data. Preserve texture-swap shape names/index mappings; when a shape must be split, account for every new piece in any ARMA alternate-texture mapping. Otherwise colour variants can silently break.

Use Outfit Studio's conform workflow to generate the 3BA sliders, then correct individual slider shapes. Copy skeletal weights selectively for the fitted torso/sleeves; skirt movement is authored separately. Save full .osp, source .nif, .osd and group files, not just a prebuilt mesh.

## 3. OBody compatibility

Build the prototype with the correct 3BA Zeroed Sliders preset and Build Morphs enabled. Keep both weight endpoints, a matching .tri and the correct BODYTRI link. Verify morph names, vertex counts and paths against the final topology. Do not bake one NPC's curvy/slim preset into everyone's base garment.

Test with presets actually distributed by this installation: slim, average, heavy/curvy, muscular and the largest relevant hip/thigh/bust combinations. Include weight 0, intermediate weight and weight 100. Switch presets live in OBody while clothed, then unequip/re-equip and save/reload. Clothes and exposed body must track together without doubled shaping or seams.

## 4. Helga-style loose skirt physics

Resolve and inspect the Helga mesh/XML currently winning in Authoria; record its actual movement as the reference. Adapt its feel, not its bone coordinates or numerical settings blindly.

Anchor the waist and fitted bodice; transition over a short band to freely moving skirt chains. Give the hem useful forward/back/side swing, little leg-follow weighting below the transition, controlled wind and enough damping to settle when stopped. Fit hidden thigh/calf/pelvis colliders with no intersection at rest. Layered aprons must move coherently without pushing each other apart.

Build the rig into BodySlide ShapeData and regenerate all slider data affected by topology changes. Morph the hidden colliders with the body as well as morphing the visible garment. Do not assume runtime morphs also reposition every custom physics bone: verify larger bodies in game, adjusting the rig or limiting supported extremes only with explicit documentation.

Keep matching topology and rig structure across _0/_1. Check normalized weights, influence/bone limits, declared XML bones, valid HDT links and shader-less hidden colliders. BodySlide rebuilds must preserve physics and morph links.

## 5. Acceptance before batching

Offline: compare neutral source/conversion renders, all relevant slider extremes, texture variants, weights, partitions, XML and mesh links, rest collisions and posed clipping. Current upstream physics preview may help if available, but it does not establish in-game OBody/FSMP behaviour.

In game: Fralia walks, turns, runs, sits, climbs stairs and stops; test a jump on a controllable wearer. Repeat on several OBody shapes. Pass means visible loose skirt motion, stable waist, no persistent clipping, exploding cloth, floor snagging or idle jitter, and acceptable performance near several clothed NPCs. User confirms the feel before conversion is propagated.

## 6. Expand and complete integration

After the prototype passes, convert the remaining distinct female geometry families and verified recolours, then matching boots/stockings/accessories. Use saved Outfit Studio automation only where supported and review each family, rather than treating automatic conforming as finished work.

Required parallel body coverage: HIMBO projects for applicable male clothing, plus a separate UBE mesh/slider and race-addon route for Ysolda and other UBE users. Keep UBE out of the 3BA OBody distribution pool. Track these as required completion work, not implicitly completed by the 3BA prototype.

Audit the existing Northern Folk content for the outstanding Requiem integration using `C:/Users/User/.codex/skills/requiem-patching/SKILL.md` and its domain skills before record edits. Geometry-only replacements do not themselves alter balance. Preserve existing Seasons behaviour; no new seasonal swaps are necessary solely for morph/physics changes. There are no new spoken lines in a mesh conversion, so Eleonora/DBReV generation is inapplicable unless dialogue is added.

## 7. Package, install and handoff

Deliver separate source projects, reproducible conversion scripts/manifest, SMP XMLs, build instructions and built outputs. Proposed project mod: `Authoria - Northern Folk - 3BA OBody SMP`; proposed build output: `Authoria - Bodyslide Output - Northern Folk 3BA SMP`.

Use original authored inputs, never copied generated patcher records or assets. Keep source mods enabled. Check MO2 and Skyrim are closed immediately before any write under mods/profiles or to ModOrganizer.ini, back up touched files, and place mods at recorded appropriate slots. If plugin changes are required, edit plugins.txt/loadorder.txt together and preserve the terminal Outputs block. No LOOT sorting.

Verify final virtual-file winners after BodySlide and any necessary downstream processing. Synthesis and Reqtificator remain manual user actions; do not require reruns for mesh-only changes. Any later record integration must state exactly which regeneration is required.

## Sources

- https://github.com/ousnius/BodySlide-and-Outfit-Studio
- https://github.com/ousnius/BodySlide-and-Outfit-Studio/wiki/Conversion-references-and-using-them
- https://github.com/ousnius/BodySlide-and-Outfit-Studio/wiki/Creating-a-BodySlide-project
- https://github.com/ousnius/BodySlide-and-Outfit-Studio/wiki/Copying-bone-weights
- https://github.com/ousnius/BodySlide-and-Outfit-Studio/wiki/Automation-Dialog
- Local SMP toolkit: `C:/1. AUTHORIA/_tools/coat-smp/skill/`.

## Other reported issues retained

Only the stamina-wheel removal has been installed from the earlier issue list (PICTA; base wheel, reskin and TrueHUD-bar-hiding override disabled; backed up). Ysolda's outfit repair, Hulda's barkeeper outfit, Eldawyn/Arghus robe physics, Olfrid hair/beard mismatch, distant gray skin and Lydia pre-thanedom voice investigation remain unfinished. Muiri/Olfina faces were confirmed good by the user. This plan does not claim those fixes are complete.
