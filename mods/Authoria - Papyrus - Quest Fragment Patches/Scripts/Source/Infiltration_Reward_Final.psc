;BEGIN FRAGMENT CODE - Do not edit anything between this and the end comment
;NEXT FRAGMENT INDEX 1
Scriptname Infiltration_Reward_Final Extends TopicInfo Hidden

;BEGIN FRAGMENT Fragment_0
Function Fragment_0(ObjectReference akSpeakerRef)
Actor akSpeaker = akSpeakerRef as Actor
;BEGIN CODE
game.getPlayer().addItem(rewardBook)
game.getPlayer().addItem(reward01)

GetOwningQuest().SetStage(100)
FFRiftenThaneCount.Value += 1
;END CODE
EndFunction
;END FRAGMENT

;END FRAGMENT CODE - Do not edit anything between this and the begin comment

BOOK Property rewardBook Auto

LeveledItem Property Reward01 Auto

GlobalVariable Property FFRiftenThaneCount Auto
