Scriptname REQ_Installation extends Quest
{helper script which makes the necessary preparations for installing Requiem upon game start}

REQ_SetupValidation Property validator Auto

GlobalVariable Property VersionSavegame Auto

REQ_VersionController Property coreScripts Auto

Spell[] Property startingSpells Auto

DLC1_QF_Patch1_6_UpdateQuest_0100097F Property NewGameCheck Auto
{Requiem modifies this script to set a new property IsNewGame to True. Since the script only runs when starting a new game, the absence of this variable implies Requiem was installed on an existing savegame.}

Event OnInit()
    RegisterForModEvent("_Authoria_Init_RunRequiemInstall", "OnAuthoriaRunRequiemInstall")

    If VersionSavegame.Value == -1
        Float timeout = 30.0
        While !NewGameCheck.IsStopped() && timeout > 0.0
            Utility.Wait(0.5)
            timeout -= 0.5
        EndWhile
        If NewGameCheck.IsNewGame
            VersionSavegame.SetValue(0)
        Else
            VersionSavegame.SetValue(-2)
        EndIf
    EndIf
EndEvent

Event OnAuthoriaRunRequiemInstall(String eventName, String strArg, Float numArg, Form sender)
    _Authoria_RunInstall()
EndEvent

Event OnMenuClose(String Menu)
    _Authoria_RunInstall()
EndEvent

Function _Authoria_RunInstall()
    unregisterForUpdate()
    unregisterForAllMenus()
    UnregisterForModEvent("_Authoria_Init_RunRequiemInstall")

    ; one time changes before installation
    Game.AddPerkPoints(3)
    int count = 0
    While (count < startingSpells.length)
        Game.GetPlayer().removeSpell(startingSpells[count])
        count += 1
    EndWhile

    coreScripts.upgradeVersion()
    setStage(10)

    SendModEvent("_Authoria_Init_RequiemDone")
EndFunction

Event OnUpdate()
    ; don't spam the player while he cannot access menus in the Vanilla Helgen start
    If (Game.IsMenuControlsEnabled())
        setObjectiveDisplayed(0, true, true)
    EndIf
EndEvent
