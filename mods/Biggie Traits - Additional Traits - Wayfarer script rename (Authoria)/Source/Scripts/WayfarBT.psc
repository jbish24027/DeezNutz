Scriptname WayfarBT extends activemagiceffect  

Event OnInit()
	RegisterForMenu("MapMenu")
EndEvent

Event OnPlayerLoadGame()
	RegisterForMenu("MapMenu")
EndEvent

Event OnMenuOpen(String MenuItem)
	SetFastTravel()
	RegisterForSingleUpdate(1.0) ;cause skyrim is dumb
EndEvent

Event OnUpdate()
	SetFastTravel()
EndEvent

Function SetFastTravel()
	Game.EnableFastTravel(False)
EndFunction