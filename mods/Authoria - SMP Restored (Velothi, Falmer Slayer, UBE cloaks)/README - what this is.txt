Authoria - SMP Restored (Velothi, Falmer Slayer, UBE cloaks)
============================================================
Made 2026-08-16 by Claude after an instance-wide audit (C:\1. AUTHORIA\_tools\smp-audit).

WHAT
  Meshes that had an SMP version somewhere in the load order but were being beaten by a
  static copy sitting in a generated-output mod. The static copies were deleted from the
  outputs (backup below) and these SMP copies now win.

  1. Armors of the Velothi (12 files) - YOUR HIMBO/3BA BodySlide builds, unchanged geometry,
     with the "HDT Skinned Mesh Physics Object" link re-added (the conversion sets had dropped
     only the link; HDT_BS/HDT_FS bones + CollisionLegs/VirtualGround shapes were still there):
       meshes\pulcharmsolis\indoril wayfarer\helmet_0/1.nif, helmetwithscarfm_0/1.nif -> TSXML.xml
       meshes\pulcharmsolis\ashlander seer\bootsm_0/1.nif, bootsf_0/1.nif             -> RedoranExile\REXML.xml
       meshes\pulcharmsolis\camonnatong\steelglovesf_0/1.nif                          -> camonnatong\data.xml
       meshes\pulcharmsolis\ashlanderwarrior\steelbodyf_0/1.nif                        -> ashlanderwarrior\data.xml
     They still reference the .tri files that stayed in the output mods (BodySlide/OBody morphs keep working).
  2. Falmer Slayer helmet + faceguard, UBE copies (2 files): your Bodyslide Output - UBE builds
     (geometry identical to the SMP source) with the link re-added -> meshes\falmerslayer\hood.xml
  3. Cloaks and Capes fluffy cloak + hooded cloak, UBE copies (3 files): the SMP source nif
     (HDT-SMP for Cloaks and Capes, with VirtualBody/VirtualFeet collision) carrying the
     UBE-Converter geometry, because the converter had dropped both the link and the collision
     shapes -> data\Meshes\clothes\volsCloaks\hdtCloakF.xml

  Also deleted (no file needed here): the 2 static Einar backpack builds in
  Authoria - Bodyslide Output - NSFW; the identical SMP build in Bodyslide Output - UBE wins.

REBUILD WARNING
  A BodySlide batch build of the Velothi / Falmer Slayer sets, or a UBE Converter run, will
  recreate static copies in the outputs and bury these again. The conversion sets' ShapeData
  nifs were patched 2026-08-16 (see _tools\smp-audit) so BodySlide rebuilds now keep the link;
  the UBE Converter cannot be fixed at the source - re-run _tools\smp-audit\build_restores.py.

REVERT
  Delete this folder and restore the static copies from
  _backups\2026-08-16 - SMP restored - static output copies.

ADDED LATER ON 2026-08-16 - UBE Converter hierarchy repairs
  The UBE Converter flattens the node tree of the meshes it converts: every node becomes a child of
  the root and skeleton-bone nodes are zeroed. Harmless for ordinary armor, but custom PHYSICS bones
  that hung under a skeleton bone (spine, upper arm, forearm) end up under the root, and some chain
  root nodes are dropped outright, so their cloth hangs from the wrong place / never simulates.
  Repaired with _source - scripts\nif_reparent.py (reference = the same mesh's 3BA build, which has
  the correct tree): nodes moved back under their real parents, missing nodes recreated, transforms
  copied. Geometry, weights, shaders, .tri and xml links of the UBE copies are untouched.
    meshes\!UBE\Mage's Daily Outfit\shawl_0/1.nif        4 shawl chain roots -> NPC Spine2 / L+R UpperArm  ("ends sunk in the floor" report)
    meshes\!UBE\Kreis\KSA\ksws03\BodyAF_0/1.nif, BodyBF_0/1.nif   Wild Witch sleeves: 6 missing chain roots recreated under the forearms + 63-69 nodes re-parented
  Static/broken converter copies deleted (backup in _backups\2026-08-16 - SMP restored - static output copies).
  Every other UBE-converted SMP outfit checked (525 files): only these two had custom physics bones detached.
  A UBE Converter re-run recreates the broken copies - re-run nif_reparent.py against the 3BA builds.

2026-09-06 - Mage's Daily shawl (meshes\!UBE\Mage's Daily Outfit\shawl_0/1.nif): purple square under the player after a cell change.
  The UBE Converter had given the six collision-only shapes (bodyC, VirtualGround, shawlC, shawlFC, shawlBeltC, shawlF) a
  placeholder BSLightingShaderProperty with an EMPTY texture set and relied on the Hidden flag (0x8000F) to keep them off screen.
  The game stops honouring that flag once the outfit is rebuilt on a cell load, so the empty material drew as purple; VirtualGround
  is the flat square at the feet. The author's own ShapeData / BodySlide build and the Sons cloaks give these shapes NO shader at all
  (a shape without a shader property is never drawn). Fix: shader + texture set removed from the six shapes, flags back to the plain
  0x8000E, header rebuilt (163 -> 151 blocks). Geometry, skinning, partitions, xml link and BODYTRI link byte-identical.
  Script: _source - scripts\strip_collision_shaders.py. Originals: _backups\2026-09-06 - Mage's Daily shawl UBE collision shaders.
  A UBE Converter re-run recreates the bad copies - re-run nif_reparent.py and then this script.
