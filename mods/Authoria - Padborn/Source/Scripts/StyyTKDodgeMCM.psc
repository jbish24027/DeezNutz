Scriptname StyyTKDodgeMCM extends MCM_ConfigBase
{MCM script for TK Dodge RE Addon - Authoria build.
Dodge Key is pinned UNBOUND (-1) and sprint-key dodge pinned ON on every load. Reason: MCM Helper
bool reads from the [General] section never deliver on this list (any spelling), so the stock
LoadSettings() re-broke sprint-dodge on every load. The MCM's two controls for those values are
inert here on purpose; tune dodge in SKSE\Plugins\TK Dodge RE.ini. Delete this .pex to get the stock
MCM behaviour back. All other settings still read the MCM Helper store.}

GlobalVariable Property DodgeKey Auto
GlobalVariable Property dodgeStaminaCost Auto
GlobalVariable Property bool_sprintDodge Auto
GlobalVariable Property useMCOrecovery Auto
GlobalVariable Property StyyUsePerkLockBoolGlobal Auto
GlobalVariable Property StyyuseCritDodgeGlobal Auto
GlobalVariable Property StyyPercentCost Auto

Function LoadSettings()
    DodgeKey.SetValue(-1.0)
    bool_sprintDodge.SetValueInt(1)
    dodgeStaminaCost.SetValue(GetModSettingFloat("fDodgeCost:General"))
    useMCOrecovery.SetValueInt(GetModSettingBool("bUseMCORecovery:General") as int)
    StyyPercentCost.SetValueInt(GetModSettingBool("bUsePercentages:General") as int)
    StyyUsePerkLockBoolGlobal.SetValueInt(GetModSettingBool("bUsePerkLock:Perk") as int)
EndFunction

Event OnConfigInit()
    LoadSettings()
EndEvent

Event OnGameReload()
    parent.OnGameReload()
    LoadSettings()
EndEvent

; iDodgeKey:General and bEnableSprintDodge:General are deliberately not handled - see header.
Event OnSettingChange(string a_ID)
    if a_ID == "fDodgeCost:General"
        dodgeStaminaCost.SetValue(GetModSettingFloat(a_ID))
    elseif a_ID == "bUseMCORecovery:General"
        useMCOrecovery.SetValueInt(GetModSettingBool(a_ID) as int)
    elseif a_ID == "bUsePercentages:General"
        StyyPercentCost.SetValueInt(GetModSettingBool(a_ID) as int)
    elseif a_ID == "bUsePerkLock:Perk"
        StyyUsePerkLockBoolGlobal.SetValueInt(GetModSettingBool(a_ID) as int)
    endif
EndEvent
