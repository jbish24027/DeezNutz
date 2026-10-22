ScriptName DynamicActivationKeyMCMScript Extends MCM_ConfigBase

;--- Imports --------------------------------------------------------------
import DynamicActivationKey

;--- Properties -----------------------------------------------------------
Quest Property DAK_AddonsCollectionQuest Auto
GlobalVariable Property DAK_HarvestRange Auto
GlobalVariable Property DAK_PlanterShowMessages Auto
GlobalVariable Property DAK_WeaponDraw Auto
GlobalVariable Property DAK_ScrollDraw Auto
GlobalVariable Property DAK_MerchantMustBeAtWork Auto
FormList Property DAK_FollowersList Auto
FormList Property DAK_MerchantTradeBlacklist Auto
FormList Property DAK_TrainerBlacklist Auto

;--- Private Variables ----------------------------------------------------
ReferenceAlias MainQuest

;--- Functions ------------------------------------------------------------

; Returns version of this script.
Int Function GetVersion()
    return 2 ;MCM Helper
EndFunction

; Called when this config menu is initialized.
Event OnConfigInit()
    parent.OnConfigInit()
    MainQuest = DAK_AddonsCollectionQuest.GetAliasByName("Player") as ReferenceAlias
    LoadSettings()
EndEvent

; Called when game is reloaded.
Event OnGameReload()
    parent.OnGameReload()
    MainQuest = DAK_AddonsCollectionQuest.GetAliasByName("Player") as ReferenceAlias
    If GetModSettingBool("bLoadSettingsonReload:Maintenance")
        LoadSettings()
        VerboseMessage("OnGameReload: Settings autoloaded!")
    EndIf
EndEvent

; Called when setting changed to different value.
Event OnSettingChange(String a_ID)
    parent.OnSettingChange(a_ID)
    If a_ID == "iHotkey:General"
        SetModKeySetting(GetModSettingInt("iHotkey:General"))
    ElseIf a_ID == "iAssignKey:Controller"
        SetModControllerKeySetting(265 + GetModSettingInt("iAssignKey:Controller"))
    ElseIf a_ID == "bTrade:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bTrain:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bFollower:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bPlants:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bHorseInventory:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bBooks:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bArmor:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bWeapon:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bFood:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bIngredient:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "bScroll:Addons"
        MainQuest.OnPlayerLoadGame()
    ElseIf a_ID == "iHarvestRange:AddonsSettings"
        DAK_HarvestRange.SetValue(GetModSettingInt("iHarvestRange:AddonsSettings") as Float)
    ElseIf a_ID == "bShowPlanerMessages:AddonsSettings"
        DAK_PlanterShowMessages.SetValue(GetModSettingBool("bShowPlanerMessages:AddonsSettings") as Float)
    ElseIf a_ID == "bDrawWeapon:AddonsSettings"
        DAK_WeaponDraw.SetValue(GetModSettingBool("bDrawWeapon:AddonsSettings") as Float)
    ElseIf a_ID == "bDrawScroll:AddonsSettings"
        DAK_ScrollDraw.SetValue(GetModSettingBool("bDrawScroll:AddonsSettings") as Float)
    ElseIf a_ID == "bMerchanttradewhenworking:AddonsSettings"
        DAK_MerchantMustBeAtWork.SetValue(GetModSettingBool("bMerchanttradewhenworking:AddonsSettings") as Float)
    EndIf
EndEvent

; Called when a new page is selected, including the initial empty page.
Event OnPageSelect(String a_page)
    parent.OnPageSelect(a_page)
EndEvent

Function Default()
    SetModSettingInt("iHotkey:General", 42)
    SetModSettingInt("iAssignKey:Controller", 9)
    SetModSettingBool("bTrade:Addons", True)
    SetModSettingBool("bTrain:Addons", True)
    SetModSettingBool("bFollower:Addons", True)
    SetModSettingBool("bPlants:Addons", True)
    SetModSettingBool("bHorseInventory:Addons", True)
    SetModSettingBool("bBooks:Addons", True)
    SetModSettingBool("bArmor:Addons", True)
    SetModSettingBool("bWeapon:Addons", True)
    SetModSettingBool("bFood:Addons", True)
    SetModSettingBool("bIngredient:Addons", True)
    SetModSettingBool("bScroll:Addons", True)
    SetModSettingInt("iHarvestRange:AddonsSettings", 2000)
    SetModSettingBool("bShowPlanerMessages:AddonsSettings", True)
    SetModSettingBool("bDrawWeapon:AddonsSettings", True)
    SetModSettingBool("bDrawScroll:AddonsSettings", True)
    SetModSettingBool("bMerchanttradewhenworking:AddonsSettings", True)
    SetModSettingBool("bEnabled:Maintenance", True)
    SetModSettingInt("iLoadingDelay:Maintenance", 0)
    SetModSettingBool("bLoadSettingsonReload:Maintenance", True)
    SetModSettingBool("bVerbose:Maintenance", False)
    SetModSettingBool("bDebug:Maintenance", False)
    VerboseMessage("Settings reset!")
    Load()
EndFunction

Function Load()
    SetModKeySetting(GetModSettingInt("iHotkey:General"))
    SetModControllerKeySetting(265 + GetModSettingInt("iAssignKey:Controller"))
    MainQuest.OnPlayerLoadGame()
    DAK_HarvestRange.SetValue(GetModSettingInt("iHarvestRange:AddonsSettings") as Float)
    DAK_PlanterShowMessages.SetValue(GetModSettingBool("bShowPlanerMessages:AddonsSettings") as Float)
    DAK_WeaponDraw.SetValue(GetModSettingBool("bDrawWeapon:AddonsSettings") as Float)
    DAK_ScrollDraw.SetValue(GetModSettingBool("bDrawScroll:AddonsSettings") as Float)
    DAK_MerchantMustBeAtWork.SetValue(GetModSettingBool("bMerchanttradewhenworking:AddonsSettings") as Float)
    VerboseMessage("Settings applied!")
EndFunction

Function LoadSettings()
    If GetModSettingBool("bEnabled:Maintenance") == false
        return
    EndIf
    Utility.Wait(GetModSettingInt("iLoadingDelay:Maintenance"))
    VerboseMessage("Settings autoloaded!")
    Load()
EndFunction

Function VerboseMessage(String m)
    Debug.Trace("[Dynamic Activation Key] " + m)
    If GetModSettingBool("bVerbose:Maintenance")
        Debug.Notification("[Dynamic Activation Key] " + m)
    EndIf
EndFunction
