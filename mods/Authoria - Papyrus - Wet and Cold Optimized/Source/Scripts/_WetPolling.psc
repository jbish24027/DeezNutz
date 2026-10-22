Scriptname _WetPolling extends activemagiceffect

;====================================================================================


FormList Property _WetWTTreeList Auto

Form CurrentWorld


GlobalVariable Property _WetIsIndoors Auto
GlobalVariable Property _WetIsInTheCold Auto
GlobalVariable Property _WetIsInTheColdTimed Auto
GlobalVariable Property DIST_WCRegionCold Auto
GlobalVariable Property DIST_WCRegionVariable Auto
GlobalVariable Property DIST_WCRegionWarm Auto

_WetQuestScript Property _WetQuest Auto

Keyword Property _WetSMEvent Auto
Bool ChangedLoc

Actor targ

;====================================================================================

Bool Function HasForm(Form[] MyArray, Form MyForm)
	Int i = 0
	While i < MyArray.Length
		If MyArray[i] == MyForm
			Return True
		Else
			i += 1
		Endif
	EndWhile
	Return False
EndFunction

Bool Function IsInTrueInterior()
	If Weather.GetSkyMode() != 3
		Return True
	ElseIf HasForm(_WetQuest.WorldInterior, CurrentWorld)
		Return True
	EndIf
	Return False
EndFunction

Function SetColdGlobals(Int InCold, Int InColdTimed, Bool IsInCold = False)
	_WetIsInTheCold.SetValue(InCold)
	_WetIsInTheColdTimed.SetValue(InColdTimed)
	_WetQuest.IsInCold = IsInCold
	;Debug.Notification(targ.GetPositionX() + ", " + targ.GetPositionY() + ", " + targ.GetPositionZ())					;DEBUG
EndFunction

;====================================================================================

Function CheckExterior()
	If _WetQuest.InVanillaCold
		SetColdGlobals(1, 0, true)
	ElseIf _WetQuest.InVanillaColdTimed
		SetColdGlobals(1, 1)
	ElseIf _WetQuest.DGColdWorld && HasForm(_WetQuest.DGColdWorld, CurrentWorld)
		SetColdGlobals(1, 0, true)
	ElseIf _WetQuest.WTColdWorld && HasForm(_WetQuest.WTColdWorld, CurrentWorld)
		Int CurrentTime = _WetQuest.CurrentTime
		If !Game.FindClosestReferenceOfAnyTypeInListFromRef(_WetWTTreeList, targ, 5120.0)
			SetColdGlobals(1, 0, true)
		ElseIf CurrentTime < 5 || CurrentTime > 22
			SetColdGlobals(1, 1)
		Else
			SetColdGlobals(0, 0)
		EndIf
	; Start Edits by AndrealphusVIII
	ElseIf _WetQuest.ColdBSHeartland && HasForm(_WetQuest.ColdBSHeartland, CurrentWorld)
		If (_WetQuest.PlayerRef as ObjectReference).IsInLocation(_WetQuest.CountyBruma)
			SetColdGlobals(1, 0, true)
		EndIf
	; End Edits by AndrealphusVIII
	Else
		SetColdGlobals(0, 0)
	EndIf
	_WetQuest.CurrentTime = _WetQuest.GameHour.GetValue() as Int
	_WetQuest.ScanArea()
EndFunction

;====================================================================================

Function SetInteriorVars()
	SetColdGlobals(0, 0)
	_WetIsIndoors.SetValue(1)
	_WetQuest.IsIndoorsStart = True
	_WetQuest.InVanillaCold = False
	_WetQuest.InVanillaColdTimed = False
EndFunction

Function CheckInteriorStart()
	CurrentWorld = targ.GetWorldSpace() as Form
	If !IsInTrueInterior()
		_WetIsIndoors.SetValue(0)
		If _WetQuest.IsIndoorsStart
			_WetQuest.IsIndoorsUpdate = False
		Else
			_WetQuest.IsIndoorsStart = False
		EndIf
		CheckExterior()
	Else
		SetInteriorVars()
	EndIf
EndFunction

Function CheckInteriorUpdate()
	CurrentWorld = targ.GetWorldSpace() as Form
	If !IsInTrueInterior()
		_WetIsIndoors.SetValue(0)
		_WetQuest.IsIndoorsUpdate = False
		CheckExterior()
	Else
		SetInteriorVars()
		Utility.Wait(1.0)
	EndIf
	_WetQuest.IsIndoorsStart = _WetQuest.IsIndoorsUpdate
EndFunction

;====================================================================================



;====================================================================================

Event OnEffectStart(Actor akTarget, Actor akCaster)
	targ = akTarget

	GoToState("Polling")

EndEvent

;====================================================================================

State Polling

	Event OnBeginState()
		CheckInteriorStart()
		RegisterForSingleUpdate(10.0)
	EndEvent

	Event OnUpdate()
		If !ChangedLoc
			CheckInteriorUpdate()
		EndIf
		If GetState() == "Polling"		; AUTHORIA: effect finished during the update (Utility.Wait) - don't re-register on a dead effect
			RegisterForSingleUpdate(9.0)
		EndIf
	EndEvent

	Event OnLocationChange(Location akOldLoc, Location akNewLoc)
		ChangedLoc = True

		Utility.Wait(0.075)
		CheckInteriorUpdate()
		ChangedLoc = False

	EndEvent

	Event OnEffectFinish(Actor akTarget, Actor akCaster)
		SetInteriorVars()
		_WetQuest.IsIndoorsUpdate = True
		GoToState("Dead")
	EndEvent

EndState

;====================================================================================



State Dead
EndState
