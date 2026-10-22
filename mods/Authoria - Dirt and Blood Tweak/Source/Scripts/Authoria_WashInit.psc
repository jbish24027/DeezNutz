Scriptname Authoria_WashInit extends ReferenceAlias

Event OnInit()
    AddPowers()
EndEvent

Event OnPlayerLoadGame()
    AddPowers()
EndEvent

Function AddPowers()
    Actor player = GetActorReference()
    if !player
        return
    endIf

    Spell baseWash = Game.GetFormFromFile(0x0000082F, "Dirt and Blood - Dynamic Visuals.esp") as Spell
    Spell baseWashNPC = Game.GetFormFromFile(0x00000860, "Dirt and Blood - Dynamic Visuals.esp") as Spell
    Spell washFollowers = Game.GetFormFromFile(0x00000802, "Authoria - Patch - Dirt and Blood Tweaks.esp") as Spell
    Spell washTogether = Game.GetFormFromFile(0x00000803, "Authoria - Patch - Dirt and Blood Tweaks.esp") as Spell
    GlobalVariable washFollowersHotkey = Game.GetFormFromFile(0x00000806, "Authoria - Patch - Dirt and Blood Tweaks.esp") as GlobalVariable
    GlobalVariable washTogetherHotkey = Game.GetFormFromFile(0x00000807, "Authoria - Patch - Dirt and Blood Tweaks.esp") as GlobalVariable

    if baseWash
        player.RemoveSpell(baseWash)
    endIf
    if baseWashNPC
        player.RemoveSpell(baseWashNPC)
    endIf

    if washFollowers
        if washFollowersHotkey && washFollowersHotkey.GetValueInt() != 0
            player.RemoveSpell(washFollowers)
        elseif !player.HasSpell(washFollowers)
            player.AddSpell(washFollowers, false)
        endIf
    endIf
    if washTogether
        if washTogetherHotkey && washTogetherHotkey.GetValueInt() != 0
            player.RemoveSpell(washTogether)
        elseif !player.HasSpell(washTogether)
            player.AddSpell(washTogether, false)
        endIf
    endIf
EndFunction
