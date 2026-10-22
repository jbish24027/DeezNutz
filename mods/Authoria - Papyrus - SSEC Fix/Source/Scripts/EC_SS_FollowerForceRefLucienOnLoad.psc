Scriptname EC_SS_FollowerForceRefLucienOnLoad extends ReferenceAlias

ReferenceAlias Property Alias_Lucien Auto

Event OnLoad()
    if Game.IsPluginInstalled("Lucien.esp")
        Actor lucienRef = Game.GetFormFromFile(0x591F, "Lucien.esp") as Actor
        if Alias_Lucien != None && lucienRef != None
            Alias_Lucien.ForceRefTo(lucienRef)
        endif
    endif
EndEvent
