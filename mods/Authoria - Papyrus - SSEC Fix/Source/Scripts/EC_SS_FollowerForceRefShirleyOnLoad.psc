Scriptname EC_SS_FollowerForceRefShirleyOnLoad extends ReferenceAlias

ReferenceAlias Property Alias_Shirley Auto

Event OnLoad()
    if Game.IsPluginInstalled("Shirley.esp")
        Actor shirleyRef = Game.GetFormFromFile(0x322AA, "Shirley.esp") as Actor
        if Alias_Shirley != None && shirleyRef != None
            Alias_Shirley.ForceRefTo(shirleyRef)
        endif
    endif
EndEvent
