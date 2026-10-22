Scriptname Fur_Morph_Effect extends ActiveMagicEffect
;==============================================================
; NEUTERED STUB.
; The runtime fur-morph logic now lives in DynamicFurMorphNG.dll (SKSE).
; This empty override replaces Dynamic Fur Morph's Papyrus driver so the two
; do not both write the "Fur_Morph_Key" body morph. The ability/magic effect is
; kept only as an inert marker on the Khajiit / Half-Khajiit races.
; Properties are declared (but unused) so the magic effect's VMAD bindings
; resolve without "property cannot be bound" log warnings.
;==============================================================

GlobalVariable Property TempArmorMorphMapID Auto
Bool Property EnableDebug = False Auto
Keyword Property NeckMorphKeyword Auto
