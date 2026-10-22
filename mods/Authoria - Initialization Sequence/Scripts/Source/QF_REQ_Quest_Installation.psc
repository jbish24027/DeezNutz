Scriptname QF_REQ_Quest_Installation Extends Quest Hidden

Function Fragment_0()
    ; Authoria master sequence owns Requiem startup prompts.
EndFunction

Function Fragment_10()
    kmyQuest.completeAllObjectives()
    kmyQuest.completeQuest()
    kmyQuest.stop()
EndFunction

Quest Property kmyQuest Auto
