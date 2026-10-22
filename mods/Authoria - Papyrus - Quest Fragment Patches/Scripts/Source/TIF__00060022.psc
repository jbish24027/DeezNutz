;BEGIN FRAGMENT CODE - Do not edit anything between this and the end comment
;NEXT FRAGMENT INDEX 1
Scriptname TIF__00060022 Extends TopicInfo Hidden

;BEGIN FRAGMENT Fragment_0
Function Fragment_0(ObjectReference akSpeakerRef)
Actor akSpeaker = akSpeakerRef as Actor
;BEGIN CODE
Game.GetPlayer().RemoveItem(Gold, 10)
Game.GetPlayer().PlayIdle(IdleGive)
akSpeaker.AddItem(Gold, 10)
Utility.Wait(0.8)

If akSpeaker.GetSitState() == 0
	Debug.SendAnimationEvent(akSpeaker, "AO_IdleTake")
	Utility.Wait(0.5)
	Debug.SendAnimationEvent(akSpeaker, "OffsetStop")
EndIf

FavorJobsBeggarsAbility.Cast(Game.GetPlayer(), Game.GetPlayer())
FavorJobsBeggarsMessage.Show()

If TODisableSimpleFavors.Value == 0
	If akSpeaker.GetRelationshipRank(Game.GetPlayer()) == 0
		akSpeaker.SetRelationshipRank(Game.GetPlayer(), 1)
	EndIf
EndIf
;END CODE
EndFunction
;END FRAGMENT

;END FRAGMENT CODE - Do not edit anything between this and the begin comment

MiscObject Property Gold Auto

Spell Property FavorJobsBeggarsAbility Auto

Idle Property IdleGive Auto

Message Property FavorJobsBeggarsMessage Auto

GlobalVariable Property TODisableSimpleFavors Auto
