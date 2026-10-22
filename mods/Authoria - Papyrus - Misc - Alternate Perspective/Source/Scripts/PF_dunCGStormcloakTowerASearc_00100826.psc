;BEGIN FRAGMENT CODE - Do not edit anything between this and the end comment
;NEXT FRAGMENT INDEX 3
Scriptname PF_dunCGStormcloakTowerASearc_00100826 Extends Package Hidden

;BEGIN FRAGMENT Fragment_2
Function Fragment_2(Actor akActor)
;BEGIN CODE
If IsVanillaHelgenStart() && akActor
	akActor.SetRestrained(True)
EndIf
;END CODE
EndFunction
;END FRAGMENT

;BEGIN FRAGMENT Fragment_1
Function Fragment_1(Actor akActor)
;BEGIN CODE
If IsVanillaHelgenStart() && akActor
	akActor.SetRestrained(False)
EndIf
;END CODE
EndFunction
;END FRAGMENT

;END FRAGMENT CODE - Do not edit anything between this and the begin comment

; ARR: true only on a genuine vanilla Helgen prisoner start. The package subject akActor can
; be a dead/unbound handle on an Alternate Perspective alt-start (every native call on it --
; SetRestrained, Is3DLoaded, IsDisabled -- throws "no native object bound"), so we gate on the
; player carrying the prisoner tunic (Skyrim.esm 0003C9FE = REQ_Cloth_Prisoner_Body), a native
; call on the always-valid player, and never touch akActor on an alt-start. The && short-circuits.
Bool Function IsVanillaHelgenStart()
	Actor playerRef = Game.GetPlayer()
	Return playerRef && playerRef.GetItemCount(Game.GetFormFromFile(0x0003C9FE, "Skyrim.esm")) > 0
EndFunction
