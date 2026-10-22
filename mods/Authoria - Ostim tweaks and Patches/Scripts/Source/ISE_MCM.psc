Scriptname ISE_MCM extends SKI_ConfigBase

string PluginName = "OImprovedSexExpression.esp"
ISE_MainQuestScript Property MainScript Auto

;MCM option
int MCM_UpdateISE
int MCM_CachePlayerLimbs
int MCM_EnableAutoScaleLimbs
Event OnConfigInit()
    ModName = "OImproved OStim Scene"
    Pages = new string[1]
    Pages[0] = "Settings"
    MainScript = Game.GetFormFromFile(0x000800, "OImprovedSexExpression.esp") as ISE_MainQuestScript
EndEvent

Event OnPageReset(string a_page)
    SetCursorPosition(0)
	;Debugger
    MCM_UpdateISE = AddTextOption("Update Mod", "")
    MCM_CachePlayerLimbs = AddTextOption("Update Player's Limbs Length", "")
    MCM_EnableAutoScaleLimbs = AddToggleOption("Enable Auto Scale Limbs", GetExternalBool(PluginName, 0x000801))
EndEvent

event OnOptionSelect(int option)
    If (option == MCM_UpdateISE)
        ;MainScript.OnInit()
        MainScript.MCM_UpdateMod()
        
    Elseif (option == MCM_CachePlayerLimbs)
        MainScript.GetPlayerLimbsLength()

    ElseIf (option == MCM_EnableAutoScaleLimbs)
        SetExternalBool(PluginName, 0x000801, !GetExternalBool(PluginName, 0x000801))
		SetToggleOptionValue(MCM_EnableAutoScaleLimbs, GetExternalBool(PluginName, 0x000801))
    EndIf
EndEvent

event OnOptionHighlight(int option)
    If (option == MCM_CachePlayerLimbs)
        SetInfoText("Save player's legs and spine length in order to use auto scale limbs feature for OStim")
    EndIf
EndEvent

int Function GetExternalInt(string modesp, int id) Global
	return (game.GetFormFromFile(id, modesp) as GlobalVariable).GetValueInt()
endfunction

bool Function GetExternalBool(string modesp, int id) Global
	return (game.GetFormFromFile(id, modesp) as GlobalVariable).GetValueInt() == 1
endfunction

Function SetExternalBool(string modesp, int id, bool val)
	int set = 0
	if val
		set = 1
	endif 
	(game.GetFormFromFile(id, modesp) as GlobalVariable).SetValueInt(set)
endfunction