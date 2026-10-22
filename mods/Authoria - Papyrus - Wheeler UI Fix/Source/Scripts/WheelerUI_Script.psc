Scriptname WheelerUI_Script extends Quest

Import PapyrusIniManipulator

WheelerUI_SkyInteractScript Property WheelerPrompt Auto
WheelerUI_MCM Property Config Auto
String[] Property PositionValues Auto

String sWheelerIni = "Data/SKSE/Plugins/Wheeler/Controls.ini"
String sConfigIni = "Data/Wheeler - UI.ini"

String[] Keys
String[] Labels
Int[] KBMValues
Int[] GamePadValues
Bool[] Enabled

Int iToggleKey
Int iToggleKeyGamePad
String sTarget
String sCurrentMenu
Bool bGamepad
Bool bWheelerClosed

Event OnInit()
    Init()
EndEvent

; pull and cache Wheeler keys from sWheelerIni, based on the settings set in sConfigIni
Function Setup()
    iToggleKey = PullIntFromIni(sWheelerIni, "InputBindings.MKB", "toggleWheel")
    iToggleKeyGamePad = PullIntFromIni(sWheelerIni, "InputBindings.GamePad", "toggleWheel")
    Keys = Utility.CreateStringArray(13)
    Labels = Utility.CreateStringArray(13)
    KBMValues = Utility.CreateIntArray(13)
    GamePadValues = Utility.CreateIntArray(13)
    Enabled = Utility.CreateBoolArray(13)
    Int i = 0
    While i < Enabled.Length
        Enabled[i] = PullBoolFromIni(sConfigIni, "Main", "bEnabled_" + i)
        If Enabled[i]
            Keys[i] = PullStringFromIni(sConfigIni, "Main", "sConfigKey_" + i)
            Labels[i] = PullStringFromIni(sConfigIni, "Main", "sLabel_" + i)
            KBMValues[i] = PullIntFromIni(sWheelerIni, "InputBindings.MKB", Keys[i])
            GamePadValues[i] = PullIntFromIni(sWheelerIni, "InputBindings.GamePad", Keys[i])
        EndIf
        i += 1
    EndWhile
EndFunction

Function Init()
    If PapyrusIniManipulator.GetVersion()
        Setup()
        Config.OnSettingChange("") ; update settings
        RegisterForMenu("MagicMenu")
        RegisterForMenu("InventoryMenu")
    EndIf
EndFunction

Event OnMenuOpen(String asMenuName)
    sCurrentMenu = asMenuName
    bGamepad = Game.UsingGamepad()
    bWheelerClosed = True
    string[] args = new string[2]
    Int toggleKey = iToggleKey
    If bGamepad
        toggleKey = iToggleKeyGamePad
    EndIf
    args[0] = "Wheeler_" + toggleKey
    args[1] = Utility.RandomInt(9000, 13000)
    UI.InvokeStringA(asMenuName, "_root.createEmptyMovieClip", args)
    sTarget = "_root." + args[0]
    UI.InvokeString(asMenuName, sTarget + ".loadMovie", "wheelerui_inject.swf")

    RegisterForKey(toggleKey)
EndEvent

Event OnKeyDown(Int iKeycode)
    If ! UI.IsTextInputEnabled()
        Utility.WaitMenuMode(0.1) ; wait for Wheeler to run first
        ShowPrompts()
        UI.Invoke(sCurrentMenu, sTarget + ".Menu_mc.waitForWheeler")
        RegisterForModEvent("WheelerUI_Close", "OnWheelerClose")
    EndIf
EndEvent

Event OnWheelerClose(string eventName, string strArg, float numArg, Form formArg)
    UnregisterForModEvent("WheelerUI_Close")
    ClearPrompts()
EndEvent

Function ShowPrompts()
    bWheelerClosed = False
    WheelerPrompt.SetScale(Config.iScale)
    WheelerPrompt.SetPosition(PositionValues[Config.iPosition], Config.iInlineMargin, Config.iBlockMargin)

    Int[] Values
    If bGamepad
        Values = GamePadValues
    Else
        Values = KBMValues
    EndIf

    Int i
    While i < Enabled.Length
        If Enabled[i] && Values[i]
            WheelerPrompt.Add("wheelerui" + i, Labels[i], Values[i])
        EndIf
        i += 1
    EndWhile
EndFunction

Function ClearPrompts()
    WheelerPrompt.Clear()
    bWheelerClosed = True
EndFunction

Event OnMenuClose(String asMenuName)
    UnregisterForAllKeys()
    If ! bWheelerClosed
        ClearPrompts()
    EndIf
EndEvent
