Scriptname TIF__WS_Accept extends TopicInfo Hidden
{Shared fragment on the 4 success proposition lines: pay the wench, she follows.}

Function Fragment_0(ObjectReference akSpeakerRef)
    (Game.GetFormFromFile(0x806, "Authoria - Basic Wenches OStim.esp") as _WS_Main).AcceptProposition(akSpeakerRef as Actor)
EndFunction
