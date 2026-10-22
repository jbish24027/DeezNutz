Authoria - Serana UBE Face   (2026-08-17)

WHAT IT FIXES: Serana (UBE Serana - NPC Replacer, Multiform variant) showed up bald with a
dark/tan face and wrong eyes.

WHY (measured, not the Lydia mechanism):
  - Her record (winner: Requiem for the Indifferent.esp) is VANILLA Serana. The UBE look is
    applied at runtime by Serana Multiform NG: it sets her face template (faceNPC) to the
    vampire form 0x801 in SeranaMultiformNG.esp, copies race / tint layers / hair colour /
    weight, swaps ONLY the hair head part on her own record, then resets her 3D.
  - Her own record keeps its vanilla brows / vampire eyes / face marks. That does not match the
    baked UBE facegen, so the engine rebuilt her head from head parts instead of loading it.
  - A rebuilt head has no face tint (dark) and needs the hair part's mesh:
    meshes\!UBE\OriSerana\Hair.nif - which the UBE Serana mod never shipped (checked the
    archive) -> bald. Her eyes came from the runtime eye part with no texture set -> wrong eyes.

THE FIX (three layers, all in this mod):
  1. SkyPatcher  SKSE\Plugins\SkyPatcher\npc\OriSeranaUBE - Authoria Fix\OriSeranaUBE.esp.ini
     At data load: race = UBE Nord, copyVisualStyle from the vampire form 0x801 (head parts,
     tints, hair colour), skin = OriSerana skin, weight 50. Her own record now matches the baked
     head, so Multiform NG finds nothing to swap and the engine loads the baked facegen.
     Multiform's vampire<->cured switch still works (both forms use the same four head parts).
  2. Facegen keyed to HER OWN FormID (Dawnguard.esm\00002B6C.nif/.dds = byte copies of the
     installed vampire form 00000801 files, neck-pin edits included) so she is right even before
     Multiform NG runs, or if it is ever disabled.
  3. SPID ability (Authoria - Patch - Serana UBE Face.esp, ESL) -> Authoria_SeranaFaceFix.pex:
     prints a probe to the console/Papyrus log tagged [SeranaFace] (which head is on her, its
     diffuse + facetint textures, hair shapes present, her base head parts, race, weight, the
     head shape's ShaderTintColor) and, if that tint reads 0,0,0 (the Lydia RaceMenu gap),
     writes her form's skin tone as a persistent NiOverride (vampire 160,177,177 / cured
     166,160,152).

HOW TO READ THE PROBE: open the console after she loads.
  head facetint = ...FaceTint\SeranaMultiformNG.esp\00000801.dds  -> baked head loaded (good)
  _OriSeranaUBE_Hair=True                                          -> hair is there
  base headparts: [1]OriSeranaUBE_Lashes [2]OriSeranaUBE_Brows [3]... -> SkyPatcher copy applied
  tint fix: before=0,0,0 wrote=... after=...                        -> Lydia gap was present, fixed
  tint ok: key7=160,177,177                                         -> nothing needed

Requires: SkyPatcher, SPID, RaceMenu (NiOverride), ConsoleUtilSSE (print only), SKSE,
          UBE Serana - NPC Replacer (Multiform variant), Serana Multiform NG.
Do not rename the plugin: the SPID ini references its basename.

UPDATE 2026-08-17 (round 2): the first test showed the head is still runtime-rebuilt (bald =
the hair model !UBE\OriSerana\Hair.nif was never shipped by the replacer). This mod now ALSO:
  - ships Hair.nif / HairHL.nif / Hairline.nif under meshes\!UBE\OriSerana\ (the three hair
    shapes extracted from the baked facegen, one per file, structured like a normal hair model)
  - overrides _OriSeranaUBE_HL and _OriSeranaUBE_Hairline to use their own model files
    (plugin now masters OriSeranaUBE.esp - keep both active together)
  - fixed the copied facegen's embedded facetint path (slot 6) to Dawnguard.esm\00002B6C.dds
  - probe now covers LYDIA too and writes to Data\Authoria_FaceProbe.txt (MO2 overwrite):
      baked head   -> "head tex0" shows the NPC's own face texture (!UBE\OriSerana\Head\... or
                      !UBE\Lydia\Head\...) and "head tex6" a FaceGenData\FaceTint path
      rebuilt head -> "head tex0" shows the generic !UBE\Head\... texture
      Lydia only   -> LydiaHair=True (baked) vs LydiaHairRT=True (rebuilt)
