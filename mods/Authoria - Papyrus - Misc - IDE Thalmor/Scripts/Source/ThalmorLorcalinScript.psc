Scriptname ThalmorLorcalinScript extends ReferenceAlias  

Event OnLoad()
	Actor MyRef = Self.GetActorRef()
	if MyRef && (SolitudeFreeform07.GetStage() < 10 || SolitudeFreeform07.GetStage() > 20)
		MyRef.SetAV("Aggression", 0)
		MyRef.RemoveFromFaction(WEPlayerEnemy)
	endif
EndEvent

Quest Property SolitudeFreeform07  Auto  

Faction Property WEPlayerEnemy  Auto  
