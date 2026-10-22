Scriptname ksws03HouseActorScript extends ReferenceAlias

Int InitMoveAttempts = 0

Event OnInit()
	MoveToSpawnWhenReady()
EndEvent

Event OnUpdate()
	MoveToSpawnWhenReady()
EndEvent

Function MoveToSpawnWhenReady()
	ObjectReference spawnRef = None

	If HouseSpawnAlias
		spawnRef = HouseSpawnAlias.GetRef()
	EndIf

	If spawnRef && TryToMoveTo(spawnRef)
		InitMoveAttempts = 0
	ElseIf InitMoveAttempts < 10
		InitMoveAttempts += 1
		RegisterForSingleUpdate(1.0)
	EndIf
EndFunction

ReferenceAlias Property HouseSpawnAlias Auto
