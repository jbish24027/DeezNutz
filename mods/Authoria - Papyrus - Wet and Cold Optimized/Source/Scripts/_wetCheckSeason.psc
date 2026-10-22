Scriptname _wetCheckSeason extends activemagiceffect

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

Function RegUpdate()
	UpdateWinterState()
EndFunction

Event OnEffectStart(Actor akTarget, Actor akCaster)
	UpdateWinterState()
EndEvent
