Scriptname EC_SS_ThoronSpellScalingScript extends ReferenceAlias

Float Property RetrySeconds = 5.0 Auto

Event OnInit()
	RegisterForSingleUpdate(RetrySeconds)
EndEvent

Event OnUpdate()
	If TryScaleThoron()
		RegisterForUpdateGameTime(24)
	Else
		RegisterForSingleUpdate(RetrySeconds)
	EndIf
EndEvent

Event OnUpdateGameTime()
	If TryScaleThoron() == False
		RegisterForSingleUpdate(RetrySeconds)
	EndIf
EndEvent

Bool Function TryScaleThoron()
	Actor thoron = GetActorReference()
	If thoron == None
		Return False
	EndIf

	ApplyScaleThoron(thoron)
	Return True
EndFunction

Function ScaleThoron()
	TryScaleThoron()
EndFunction

Function ApplyScaleThoron(Actor thoron)
	If thoron.IsInCombat() == False
		CurrentLevel = thoron.GetLevel()
		If CurrentLevel > LastLevel
			If CurrentLevel >= Stage3
				LastLevel = Stage3

			ElseIf CurrentLevel >= Stage2
				thoron.RemoveSpell(SparksRightHand)
				thoron.RemoveSpell(FastHealingLeftHand)

				thoron.AddSpell(EC_SS_WallOfStormsRightHand)
				thoron.AddSpell(CloseWoundsLeftHand)

			ElseIf CurrentLevel >= Stage1
				thoron.AddSpell(SparksRightHand)
				thoron.AddSpell(FastHealingLeftHand)
			EndIf

			LastLevel = CurrentLevel
		EndIf
	EndIf
EndFunction

Int Property CurrentLevel Auto
Int Property LastLevel Auto

Int Property Stage1 = 20 Auto
Int Property Stage2 = 30 Auto
Int Property Stage3 = 99 Auto

Spell Property SparksRightHand Auto
Spell Property EC_SS_WallOfStormsRightHand Auto
Spell Property FastHealingLeftHand Auto
Spell Property CloseWoundsLeftHand Auto
