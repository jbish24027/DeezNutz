Scriptname SeranaEyeFixScript extends ReferenceAlias

Int Property Max3DWaitAttempts = 20 Auto Hidden
Float Property EyeTextureWaitSeconds = 0.25 Auto Hidden

Bool EyeTextureUpdateInProgress = False

Event OnLoad()
	ApplyHumanEyesWhenReady()
EndEvent

Event OnObjectEquipped(Form akBaseObject, ObjectReference akReference)
	ApplyHumanEyesWhenReady()
EndEvent

Event OnObjectUnequipped(Form akBaseObject, ObjectReference akReference)
	ApplyHumanEyesWhenReady()
EndEvent

Function ApplyHumanEyesWhenReady()
	If EyeTextureUpdateInProgress
		Return
	EndIf

	EyeTextureUpdateInProgress = True
	GoToState("busy")

	If DLC1SeranaRef && DLC1SeranaHumanEyes && ActorTypeUndead && !DLC1SeranaRef.HasKeyword(ActorTypeUndead)
		Int Attempts = 0
		While !DLC1SeranaRef.Is3DLoaded() && Attempts < Max3DWaitAttempts
			Utility.Wait(EyeTextureWaitSeconds)
			Attempts += 1
		EndWhile

		If DLC1SeranaRef.Is3DLoaded()
			DLC1SeranaRef.SetEyeTexture(DLC1SeranaHumanEyes)
			Utility.Wait(1.0)

			If DLC1SeranaRef.Is3DLoaded()
				DLC1SeranaRef.SetEyeTexture(DLC1SeranaHumanEyes)
			EndIf
		EndIf
	EndIf

	GoToState("")
	EyeTextureUpdateInProgress = False
EndFunction

State Busy
	Event OnLoad()
	EndEvent

	Event OnObjectEquipped(Form akBaseObject, ObjectReference akReference)
	EndEvent

	Event OnObjectUnequipped(Form akBaseObject, ObjectReference akReference)
	EndEvent
EndState

Actor Property DLC1SeranaRef Auto
TextureSet Property DLC1SeranaHumanEyes Auto
Keyword Property ActorTypeUndead Auto
