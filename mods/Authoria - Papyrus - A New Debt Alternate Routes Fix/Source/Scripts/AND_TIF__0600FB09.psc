ScriptName AND_TIF__0600FB09 extends TopicInfo Hidden

actor Property Jailedboi Auto

actor Property Thug Auto

actor Property Debtcollector Auto

alias Property Mogrul Auto

Function Fragment_0(ObjectReference akSpeakerRef)
    actor akSpeaker = (akSpeakerRef as actor)
    GetOwningQuest().SetStage(310)
    Debtcollector.Disable(false)
    Thug.Disable(false)
    Jailedboi.enable(false)
    game.FadeOutGame(false, true, 2.0, 1.0)
EndFunction
