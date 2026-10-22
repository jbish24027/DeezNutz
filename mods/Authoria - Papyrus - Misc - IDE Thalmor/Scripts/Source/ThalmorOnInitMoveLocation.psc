Scriptname ThalmorOnInitMoveLocation extends ReferenceAlias   

Event OnInit()
	Actor MyRef = Self.GetActorRef()
	if MyRef && QuestToDie.GetStage() < Stage
		MyRef.Enable()
		if enemyFaction != None
			MyRef.RemoveFromFaction(enemyFaction)
		endif
		MyRef.MoveTo(Home)
	endif
EndEvent

ObjectReference Property Home  Auto  

ObjectReference Property OriginalPlace  Auto  

Faction Property enemyFaction  Auto  

Quest Property QuestToDie  Auto  

Int Property stage  Auto  
