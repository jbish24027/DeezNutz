Scriptname TIF__WS_Scene extends TopicInfo Hidden

Function Fragment_0(ObjectReference akSpeakerRef)
    (Game.GetFormFromFile(0x806, "Authoria - Basic Wenches OStim.esp") as _WS_Main).StartWenchScene(akSpeakerRef as Actor)
EndFunction
