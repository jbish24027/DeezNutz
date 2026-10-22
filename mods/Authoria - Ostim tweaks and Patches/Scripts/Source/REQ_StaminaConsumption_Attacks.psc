Scriptname REQ_StaminaConsumption_Attacks extends REQ_CoreScript
{This script is responsible for the stamina drain for normal attacks for ALL actors}

Spell Property StaminaDrain Auto

; --- OStim scene compatibility (Authoria - Ostim tweaks and Patches) -----------------------------
; Skip the weapon-swing / bow-draw stamina drain for any actor that is currently in an OStim scene.
; OActor.IsInOStim is an OStim native (see OActor.psc) and is checked per-actor because OnActorAction
; fires for every actor, not just the player. OStim is a hard dependency of this NSFW profile so the
; call is always bound. This is the OStim re-expression of the SexLab faction gate the personal
; SexLab list used (per RULES.md rule 5, port-only).
; --- end OStim scene compatibility --------------------------------------------------------------

Event OnActorAction(int actionType, Actor akActor, Form source, int slot)
	If (akActor && !OActor.IsInOStim(akActor))
		akActor.AddSpell(StaminaDrain, False)
	EndIf
EndEvent

Event OnPlayerLoadGame()
    parent.OnPlayerLoadGame()
	RegisterForActorAction(5)
	RegisterForActorAction(0)
EndEvent

Function initScript(Int currentVersion, Int nevVersion)
	RegisterForActorAction(5)
	RegisterForActorAction(0)
EndFunction

Function shutdownScript(Int currentVersion, Int nevVersion)
EndFunction
