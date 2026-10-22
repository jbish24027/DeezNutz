Scriptname DA08EbonyBladeTrackingScript extends Quest conditional

int Property FriendsKilled auto conditional
int Property MaxFriendsKilled auto

Scene Property GratsScene auto

REQ_ReapplyNonPersistentChanges Property ReapplyNonPersistentChanges Auto

Quest Property myQuest auto
Weapon Property EbonyBlade auto

Function FriendKilled()
	if (FriendsKilled < MaxFriendsKilled)
		FriendsKilled += 1
; 		Debug.Trace("EBONY BLADE: Killed a friend, current count: " + FriendsKilled)
		ReapplyNonPersistentChanges.EbonyBladeScript.ReapplyNonPersistentChanges()

		if (FriendsKilled == 4)
			myQuest.SetStage(20)
		endif

		if (FriendsKilled == 6)
			myQuest.SetStage(30)
		endif

		if (FriendsKilled == 8)
			myQuest.SetStage(40)
			if Game.IsPluginInstalled("EbonyBladeCurse_QuestObject_WDQE.esp")
				Game.GetPlayer().RemoveItem(EbonyBlade, 1, true)
				Game.GetPlayer().AddItem(EbonyBlade, 1, true)
			endif
			if Game.IsPluginInstalled("EbonyBladeCurse_QuestObject.esp")
				Game.GetPlayer().RemoveItem(EbonyBlade, 1, true)
				Game.GetPlayer().AddItem(EbonyBlade, 1, true)
			endif
		endif

		GratsScene.Start()
	endif
EndFunction
