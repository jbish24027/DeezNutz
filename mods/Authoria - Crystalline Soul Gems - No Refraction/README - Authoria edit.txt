Authoria - Crystalline Soul Gems - No Refraction  (2026-08-16)

WHY: under Community Shaders upscaling (DLSS/FSR + Frame Generation) the refraction-normals
buffer is upsampled per frame with no temporal accumulation (Shaders/Upscaling/DepthRefractionUpscalePS.hlsl),
so any SF1 Refraction shape shimmers/'vibrates'. Crystalline Soul Gems puts a refraction shell on every gem.

WHAT: each mesh below is a copy of the file that would otherwise win, with the refraction shell shape's
NiAVObject flags bit 0 (Hidden) set: 0xC000E -> 0xC000F. One byte per file. Nothing else changed.
Gems keep the MultiLayer-Parallax crystal, glow, and particle billboard; they lose the glassy shell.

REVERT: disable or delete this mod. Pristine sources: _backups/2026-08-16 - Crystalline No Refraction pristine/

FILES (file, source, hidden shape):
  soulgempetty01.nif           <- CS Adapted Modest              hidden 'SoulGemPetty01:11'
  soulgempetty01_full.nif      <- CS Adapted Modest              hidden 'SoulGemPetty01:11'
  soulgemlesser01.nif          <- CS Adapted Modest              hidden 'SoulGemLesser:11'
  soulgemlesser01_full.nif     <- CS Adapted Modest              hidden 'SoulGemLesser:11'
  soulgemcommon01.nif          <- CS Adapted Modest              hidden 'SoulGemCommon:11'
  soulgemcommon01_full.nif     <- CS Adapted Modest              hidden 'SoulGemCommon:11'
  soulgemgreater01.nif         <- CS Adapted Modest              hidden 'SoulGemGreat:11'
  soulgemgreater01_full.nif    <- CS Adapted Modest              hidden 'SoulGemGreat:11'
  soulgemgrand01.nif           <- CS Adapted Modest              hidden 'SoulGemGrand:11'
  soulgemgrand01_full.nif      <- CS Adapted Modest              hidden 'SoulGemGrand:11'
  soulgemblack01.nif           <- Crystalline Soul Gems 1.0.1    hidden 'SoulGemBlack01:20'
  soulgemblack01_full.nif      <- Crystalline Soul Gems 1.0.1    hidden 'SoulGemBlack01:20'
  soulgempiece01.nif           <- Crystalline Soul Gems 1.0.1    hidden 'SoulGemPiece01:9'
  soulgempiece02.nif           <- Crystalline Soul Gems 1.0.1    hidden 'SoulGemPiece02:9'
  soulgempiece03.nif           <- Crystalline Soul Gems 1.0.1    hidden 'SoulGemPiece03:9'
  soulgempiece04.nif           <- Crystalline Soul Gems 1.0.1    hidden 'SoulGemPiece04:9'
  soulgempiece05.nif           <- Crystalline Soul Gems 1.0.1    hidden 'SoulGemPiece05:9'
