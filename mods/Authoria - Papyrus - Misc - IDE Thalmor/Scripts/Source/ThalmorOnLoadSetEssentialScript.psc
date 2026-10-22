Scriptname ThalmorOnLoadSetEssentialScript extends ReferenceAlias

Event OnInit()
	Actor MyRef = Self.GetActorRef()
	if MyRef && MyRef.IsDead() == 0
		MyRef.Enable()
	endif
EndEvent

Event OnLoad()
	Actor MyRef = Self.GetActorRef()
	if MyRef && QuestEssential.GetStage() < Stage && MyRef.GetActorBase().IsEssential() == 0
		MyRef.GetActorBase().SetEssential()
	elseif MyRef && QuestEssential.GetStage() >= Stage && MyRef.GetActorBase().IsEssential() == 1
		MyRef.GetActorBase().SetEssential(0)
	endif
EndEvent

Quest Property QuestEssential  Auto  

Int Property stage  Auto  
