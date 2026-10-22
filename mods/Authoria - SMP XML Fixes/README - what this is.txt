Authoria - SMP XML Fixes
========================
Made 2026-08-16 by Claude (SMP audit, see C:\1. AUTHORIA\_tools\smp-audit).

Six SMP physics xmls placed at the path the mesh actually asks for. In every case the mesh
was SMP-rigged but its xml sat somewhere else (author typo / moved folder / source mod
disabled), so the physics never started. Each file is a byte-identical copy of the author's own xml.

  meshes\TheMilkDrinker\Nier\2BHairHDT.xml    Ashe's 2B hair      (copy of Ashe - Crystal Heart\meshes\actors\character\ashe\outfit\TheMilkDrinker\Nier\2BHairHDT.xml)
  meshes\TheMilkDrinker\Nier\skirt.xml        Ashe's 2B skirt     (same folder)
  Meshes\LDDNPCsYsolda\Outfit\Choker.xml      Ysolda's choker     (from the disabled 'De NPCs - Ysolda Overhaul by LDD'; the NPC Merge kept the mesh but not the xml)
  meshes\527_Dark Elf Blader\BladerHair.xml   Tullius hair 491 'Dark Elf Blader' ponytail  (author wrote 527, shipped 491)
  meshes\355_Vin Pure Regina\hdtPR.xml        Tullius hair 353 'Vin Pure Regina'           (author wrote 355, shipped 353)
  Meshes\armor\[dint999]\FacePart\Female\ears\ear01\ear01HDT.xml   Chooey's Dint ears (all 5 variants; bones match dint999's ear01 xml from the M'rissi replacer)

The Tullius wig '532 DOA Tsukushi' had a typo in the MESH ('ata\...'); that was fixed in the mesh
instead (copies live in 'Authoria - SMP Restored ...', ShapeData patched too).

REVERT: delete this folder.
