Scriptname _WS_PlayerAlias extends ReferenceAlias
{Rolls the proposition (cost + 80/20 outcome + line variation) every time the
dialogue menu opens, so the wench's conditioned reply is decided before the click.}

Event OnInit()
    Register()
EndEvent

Event OnPlayerLoadGame()
    Register()   ; RegisterForMenu does not persist across save/load
EndEvent

Function Register()
    RegisterForMenu("Dialogue Menu")
    (GetOwningQuest() as _WS_Main).RollProposition()
EndFunction

Event OnMenuOpen(String asMenuName)
    If asMenuName == "Dialogue Menu"
        (GetOwningQuest() as _WS_Main).RollProposition()
    EndIf
EndEvent
