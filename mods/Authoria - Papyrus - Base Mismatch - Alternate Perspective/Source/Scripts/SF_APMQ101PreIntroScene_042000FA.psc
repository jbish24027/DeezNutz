;BEGIN FRAGMENT CODE - Do not edit anything between this and the end comment
;NEXT FRAGMENT INDEX 7
Scriptname SF_APMQ101PreIntroScene_042000FA Extends Scene Hidden

;BEGIN FRAGMENT Fragment_4
Function Fragment_4()
;BEGIN CODE
Actor matlaraActor = GetQuestActor(53)
If matlaraActor
	matlaraActor.EvaluatePackage()
EndIf
;END CODE
EndFunction
;END FRAGMENT

;BEGIN FRAGMENT Fragment_1
Function Fragment_1()
;BEGIN CODE
MoveQuestActorToMarker(53, MatlaraStartMarker)
MoveQuestActorToMarker(52, TorriStartMarker)
MoveQuestActorToMarker(51, TorolfStartMarker)

Quest owningQuest = GetOwningQuest()
If owningQuest
	owningQuest.SetStage(5)
EndIf
;END CODE
EndFunction
;END FRAGMENT

;END FRAGMENT CODE - Do not edit anything between this and the begin comment

ObjectReference Property TorriStartMarker Auto

ObjectReference Property TorolfStartMarker Auto

ObjectReference Property MatlaraStartMarker Auto

Actor Function GetQuestActor(Int aliasId)
	Quest owningQuest = GetOwningQuest()
	If !owningQuest
		Return None
	EndIf

	ReferenceAlias actorAlias = owningQuest.GetAlias(aliasId) As ReferenceAlias
	If !actorAlias
		Return None
	EndIf

	Return actorAlias.GetActorRef()
EndFunction

Function MoveQuestActorToMarker(Int aliasId, ObjectReference markerRef)
	If !markerRef
		Return
	EndIf

	Actor actorRef = GetQuestActor(aliasId)
	If actorRef
		actorRef.MoveTo(markerRef)
	EndIf
EndFunction
