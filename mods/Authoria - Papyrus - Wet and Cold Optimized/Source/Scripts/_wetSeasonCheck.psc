Scriptname _wetSeasonCheck extends ReferenceAlias

GlobalVariable Property GameMonth Auto
GlobalVariable Property _WetIsSeasonWinter Auto

Function UpdateWinterState()
	If !GameMonth || !_WetIsSeasonWinter
		Return
	EndIf
	Int GameMonthCurrent = GameMonth.GetValueInt()
	If GameMonthCurrent == 0 || GameMonthCurrent == 1 || GameMonthCurrent == 11
		_WetIsSeasonWinter.SetValueInt(1)
	Else
		_WetIsSeasonWinter.SetValueInt(0)
	EndIf
EndFunction

Event OnInit()
	UpdateWinterState()
	RegisterForSingleUpdate(60.0)
EndEvent

Event OnUpdate()
	UpdateWinterState()
	RegisterForSingleUpdate(60.0)
EndEvent
