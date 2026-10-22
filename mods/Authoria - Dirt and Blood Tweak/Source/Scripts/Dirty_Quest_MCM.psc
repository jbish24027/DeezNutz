Scriptname Dirty_Quest_MCM extends SKI_ConfigBase

GlobalVariable Property Dirty_RandomDirtDuration Auto
GlobalVariable Property Dirty_PlayerHitBloodyChance Auto
GlobalVariable Property Dirty_RandomHairDuration Auto
GlobalVariable Property Dirty_RainCleans Auto
GlobalVariable Property Dirty_SoapRequired Auto
GlobalVariable Property Dirty_NPCsGetBloodyTrue Auto
GlobalVariable Property Dirty_SwimCleansCompletely Auto
GlobalVariable Property Dirty_WashingAutomaticClothes Auto
GlobalVariable Property Dirty_BanditsDirt Auto
GlobalVariable Property Dirty_ProfessionsDirt Auto
GlobalVariable Property Dirty_ShowMessages Auto
GlobalVariable Property Dirty_SoundEffect Auto
GlobalVariable Property Dirty_NPCReactions Auto
Spell Property Dirty_Spell_Clean Auto
Spell Property Dirty_Spell_Dirt1 Auto
Spell Property Dirty_Spell_Dirt2 Auto
Spell Property Dirty_Spell_Dirt3 Auto
Spell Property Dirty_Spell_Dirt4 Auto
Spell Property Dirty_Spell_Blood1 Auto
Spell Property Dirty_Spell_Blood2 Auto
Spell Property Dirty_Spell_Blood3 Auto
Spell Property Dirty_Spell_Blood4 Auto
Spell Property Dirty_Spell_Swimming Auto
Spell Property Dirty_Spell_IsRaining Auto
Spell Property Dirty_Spell_NegativeSideEffects Auto
Spell Property Dirty_Spell_PositiveSideEffects Auto
Dirty_Hair Property StartHair Auto
Dirty_Script Property StartDirt Auto
Actor Property PlayerRef Auto
Spell Property Dirty_NPCisWashingNow Auto
Spell Property Dirty_Spell_DirtForNPCs Auto
Spell Property Dirty_BloodySpellforNPCs Auto
GlobalVariable Property Dirty_PlayerBathingAnimation Auto
GlobalVariable Property Dirty_NPCBathingAnimation Auto
Formlist property Dirty_Exclusion auto
GlobalVariable Property Dirty_WaterRequired Auto
Spell Property Authoria_WashFollowersPower Auto
Spell Property Authoria_WashTogetherPower Auto
GlobalVariable Property Authoria_WashFollowersHotkey Auto
GlobalVariable Property Authoria_WashTogetherHotkey Auto
GlobalVariable Property Authoria_FreeCamBath Auto
GlobalVariable Property Authoria_BathAnimStyle Auto

int dirtsetting_M
string DirtSetting
int bloodsetting_M
string bloodsetting
int hairsetting_M
string hairsetting
int raincleans_B
int soaprequired_B
int swimcleans_B
int washingautomatic_B
int targetednpc
int banditsdirt_b
int professionsdirt_b
int showmessages_b
int soundeffect_b
int Restart
int bloodforNPCS_B
int NPCBatheAnimation_B
int PlayerBatheAnimation_B
int NPCReactions_B
int WaterRequired_b
int WadeInWaterNotFound
int FreeCamBathing_B
int WashFollowersHotkey_K
int WashTogetherHotkey_K
int bathanimstyle_M

; State
int DirtSettingIndex = 1
int bloodsettingIndex = 1
int HairSettingIndex = 1
int BathAnimStyleIndex = 1

; List
string[] DirtSettingList
string[] bloodsettinglist
string[] Hairsettinglist
string[] BathAnimStyleList

; Legacy Settings Loader
string settings_path = "..\\DirtAndBlood\\UserSettings"
bool ValidatePapyrusUtil=false


Event OnConfigInit()
	Pages = new string[2]
	Pages[0] = "Settings"
	Pages[1] = "Maintenance"
	ResolveAuthoriaProperties()
	LoadSettingsAtStart()
	SyncAuthoriaWashPowers()
EndEvent

Event OnGameReload()
	parent.OnGameReload()
	ResolveAuthoriaProperties()
	SyncAuthoriaWashPowers()
EndEvent

event OnInit()
	parent.OnInit()
	DirtSettingList = new string[4]
	DirtSettingList[0] = "Rarely - 2 to 4 days"
	DirtSettingList[1] = "Default - 1 to 2 days"
	DirtSettingList[2] = "Often - 12 to 24 hours"
	DirtSettingList[3] = "Deactivated"

	bloodsettinglist = new string[4]
	bloodsettinglist[0] = "Rarely - 1% Chance"
	bloodsettinglist[1] = "Default - 5% Chance"
	bloodsettinglist[2] = "Often - 15% Chance"
	bloodsettinglist[3] = "Deactivated"

	hairsettinglist = new string[4]
	hairsettinglist[0] = "Rarely - 12 to 24 Days"
	hairsettinglist[1] = "Default - 6 to 12 Days"
	hairsettinglist[2] = "Often - 3 to 6 Days"
	hairsettinglist[3] = "Deactivated"

	BathAnimStyleList = new string[2]
	BathAnimStyleList[0] = "Default"
	BathAnimStyleList[1] = "Malignis"

	ResolveAuthoriaProperties()
	SyncAuthoriaWashPowers()
endEvent

Event OnPageReset(string page)
	ResolveAuthoriaProperties()

	If (page == "")

		LoadCustomContent("MCM/MCM_DNB.dds", 0.0, 0.0)
		Else
		UnloadCustomContent()
	Endif

	If (page == "Settings")
		SetCursorFillMode(LEFT_TO_RIGHT)
		Actor crosshairActor = Game.GetCurrentCrosshairRef() as Actor
		AddHeaderOption("Frequency Settings")
		AddHeaderOption("Effects on NPCs")
		AddEmptyOption()
		AddEmptyOption()
		dirtsetting_M = AddMenuOption("Dirt on Player", dirtsettingList[dirtsettingIndex])
		bloodforNPCS_B = AddToggleOption("Blood on NPCs", Dirty_NPCsGetBloodyTrue.GetValue() as bool)
		bloodsetting_M = AddMenuOption("Blood on Player", bloodsettinglist[bloodsettingindex])
		professionsdirt_B = AddToggleOption("Dirt on NPCs Based on Profession", Dirty_ProfessionsDirt.GetValue() as bool)
		hairsetting_M = AddMenuOption("Hair Reminders", hairsettinglist[hairsettingindex])
		BanditsDirt_B = AddToggleOption("Dirt on Bandits", Dirty_BanditsDirt.GetValue() as bool)
			ShowMessages_B = AddToggleOption("Display Messages", Dirty_ShowMessages.GetValue() as bool)
		If crosshairActor && !crosshairActor.isdead()
			targetednpc = AddTextOption("Clean Targeted NPC", crosshairActor.GetDisplayName())
		Else
			targetednpc = AddTextOption("Clean Targeted NPC", "None", OPTION_FLAG_DISABLED)
		Endif
		AddEmptyOption()
		NPCReactions_B = AddToggleOption("NPCs React To Dirt", Dirty_NPCReactions.GetValue() as bool)
		AddEmptyOption()
		AddEmptyOption()
		AddHeaderOption("Bathing Options")
		AddHeaderOption("Rain, Swimming & Maintenance")
		AddEmptyOption()
		AddEmptyOption()
		washingautomatic_B = AddToggleOption("Unequip Clothes When Bathing", Dirty_WashingAutomaticClothes.GetValue() as bool)
		raincleans_B = AddToggleOption("Rain Washes Dirt and Blood", Dirty_RainCleans.GetValue() as bool)
		SoapRequired_B = AddToggleOption("Soap is Required for Baths", Dirty_SoapRequired.GetValue() as bool)
		swimcleans_B = AddToggleOption("Swimming is as Effective as Bathing", Dirty_SwimCleansCompletely.GetValue() as bool)
		soundeffect_B = AddToggleOption("Sound Effect for Bathing", Dirty_SoundEffect.GetValue() as bool)
		Restart = AddTextOption("Restart Player Effects", "")
		WashFollowersHotkey_K = AddKeyMapOption("Wash Followers Hotkey", Authoria_WashFollowersHotkey.GetValueInt())
		AddEmptyOption()
		NPCBatheAnimation_B = AddToggleOption("NPC Bathing Animation", Dirty_NPCBathingAnimation.GetValue() as bool)
        WashTogetherHotkey_K = AddKeyMapOption("Wash Together Hotkey", Authoria_WashTogetherHotkey.GetValueInt())
        PlayerBatheAnimation_B = AddToggleOption("Player Bathing Animation", Dirty_PlayerBathingAnimation.GetValue() as bool)
        if Authoria_FreeCamBath
            FreeCamBathing_B = AddToggleOption("Free Camera During Bathing", Authoria_FreeCamBath.GetValue() as bool)
        else
            FreeCamBathing_B = AddToggleOption("Free Camera During Bathing", false, OPTION_FLAG_DISABLED)
        endIf
		if Authoria_BathAnimStyle
			int styleIdx = Authoria_BathAnimStyle.GetValue() as int
			if styleIdx < 0 || styleIdx > 1
				styleIdx = 1
			endIf
			BathAnimStyleIndex = styleIdx
			bathanimstyle_M = AddMenuOption("Bathing Animation Style", BathAnimStyleList[BathAnimStyleIndex])
		else
			bathanimstyle_M = AddMenuOption("Bathing Animation Style", "Malignis", OPTION_FLAG_DISABLED)
		endIf
		if ! game.isPluginInstalled("WadeInWater.esp")
			WaterRequired_B = AddToggleOption("Water Required For Bathing", False, OPTION_FLAG_DISABLED)
		else
			WaterRequired_B = AddToggleOption("Water Required For Bathing", Dirty_WaterRequired.GetValue() as bool)
		endif
	ElseIf page == "Maintenance"
		SetCursorPosition(0)
		SetCursorFillMode(TOP_TO_BOTTOM)

		AddHeaderOption("Default Settings")
		AddTextOptionST("LOAD_DEFAULT_SETTINGS_STATE", "Load", "Go")

		AddEmptyOption()

		int loadSettingsFlag = OPTION_FLAG_NONE
		If ValidatePapyrusUtil
			If !JSONUtil.JsonExists(settings_path)
				loadSettingsFlag = OPTION_FLAG_DISABLED
			EndIf
		EndIf

		AddHeaderOption("User Settings")
		AddTextOptionST("LOAD_USER_SETTINGS_STATE", "Load", "Go", loadSettingsFlag)
		AddTextOptionST("SAVE_USER_SETTINGS_STATE", "Save", "Go")
	Endif
endEvent

event OnOptionMenuOpen(int option)
	if (option == dirtsetting_M)
		SetMenuDialogOptions(dirtsettingList)
		SetMenuDialogStartIndex(dirtsettingIndex)
		SetMenuDialogDefaultIndex(1)
	elseif (option == bloodsetting_M)
		SetMenuDialogOptions(bloodsettinglist)
		SetMenuDialogStartIndex(bloodsettingindex)
		SetMenuDialogDefaultIndex(1)
	elseif (option == hairsetting_M)
		SetMenuDialogOptions(hairsettinglist)
		SetMenuDialogStartIndex(hairsettingindex)
		SetMenuDialogDefaultIndex(1)
	elseif (option == bathanimstyle_M)
		SetMenuDialogOptions(BathAnimStyleList)
		SetMenuDialogStartIndex(BathAnimStyleIndex)
		SetMenuDialogDefaultIndex(1)
	endIf
endEvent


event OnOptionMenuAccept(int option, int index)
	if (option == dirtsetting_M)
		DirtSettingIndex = index
		SetMenuOptionValue(dirtsetting_M, dirtsettingList[dirtsettingIndex])
		if index == 0
			Dirty_RandomDirtDuration.SetValue(0)
		elseif index == 1
			Dirty_RandomDirtDuration.SetValue(1)
		elseif index == 2
			Dirty_RandomDirtDuration.SetValue(2)
		elseif index == 3
			Dirty_RandomDirtDuration.SetValue(3)
		endif
	endif

	if (option == bloodsetting_M)
		bloodsettingindex = index
		SetMenuOptionValue(bloodsetting_M, bloodsettinglist[bloodsettingindex])
		if index == 0
			Dirty_PlayerHitBloodyChance.SetValue(1)
		elseif index == 1
			Dirty_PlayerHitBloodyChance.SetValue(5)
		elseif index == 2
			Dirty_PlayerHitBloodyChance.SetValue(15)
		elseif index == 3
			Dirty_PlayerHitBloodyChance.SetValue(-50)
		endif
	endif

	if (option == hairsetting_M)
		hairsettingindex = index
		SetMenuOptionValue(hairsetting_M, hairsettinglist[hairsettingindex])
		if index == 0
			Dirty_RandomHairDuration.SetValue(0)
		elseif index == 1
			Dirty_RandomHairDuration.SetValue(1)
		elseif index == 2
			Dirty_RandomHairDuration.SetValue(2)
		elseif index == 3
			Dirty_RandomHairDuration.SetValue(3)
		endif
	endif

	if (option == bathanimstyle_M)
		BathAnimStyleIndex = index
		SetMenuOptionValue(bathanimstyle_M, BathAnimStyleList[BathAnimStyleIndex])
		if Authoria_BathAnimStyle
			Authoria_BathAnimStyle.SetValue(index as float)
		endif
	endif
endEvent

event OnOptionSelect(int option)
	if (option == RainCleans_B)
        ToggleGlobal(Dirty_RainCleans, RainCleans_B)
    elseif (option == NPCBatheAnimation_B)
        ToggleGlobal(Dirty_NPCBathingAnimation, NPCBatheAnimation_B)
    elseif (option == WaterRequired_B)
        ToggleGlobal(Dirty_WaterRequired, WaterRequired_B)
    elseif (option == NPCReactions_B)
        ToggleGlobal(Dirty_NPCReactions, NPCReactions_B)
    elseif (option == PlayerBatheAnimation_B)
        ToggleGlobal(Dirty_PlayerBathingAnimation, PlayerBatheAnimation_B)
	elseif (option == swimcleans_B)
        ToggleGlobal(Dirty_SwimCleansCompletely, swimcleans_B)
	elseif (option == washingautomatic_B)
        ToggleGlobal(Dirty_WashingAutomaticClothes, washingautomatic_B)
	elseif (option == BanditsDirt_B)
        ToggleGlobal(Dirty_BanditsDirt, BanditsDirt_B)
	elseif (option == ProfessionsDirt_B)
        ToggleGlobal(Dirty_ProfessionsDirt, ProfessionsDirt_B)
	elseif (option == soundeffect_B)
        ToggleGlobal(Dirty_SoundEffect, soundeffect_B)
	elseif (option == ShowMessages_B)
        ToggleGlobal(Dirty_ShowMessages, ShowMessages_B)
	elseif (option == bloodforNPCS_B)
        ToggleGlobal(Dirty_NPCsGetBloodyTrue, bloodforNPCS_B)
    elseif (option == SoapRequired_B)
        ToggleGlobal(Dirty_SoapRequired, SoapRequired_B)
	elseif (option == FreeCamBathing_B)
		if Authoria_FreeCamBath
			bool newState = !(Authoria_FreeCamBath.GetValue() as bool)
			Authoria_FreeCamBath.SetValue(newState as float)
			SetToggleOptionValue(FreeCamBathing_B, newState, false)
		endIf
	elseif option == targetednpc
        Actor crosshairActor = Game.GetCurrentCrosshairRef() as Actor
		crosshairActor.DispelAllSpells()
		ShowMessage(crosshairActor.GetDisplayName()+" is no longer covered in dirt or blood.")
		crosshairActor.Addspell(Dirty_NPCisWashingNow)
		crosshairActor.RemoveSpell(Dirty_Spell_DirtForNPCs)
		crosshairActor.RemoveSpell(Dirty_BloodySpellforNPCs)
		Utility.Wait(0.5)
		crosshairActor.Removespell(Dirty_NPCisWashingNow)
		Dirty_Exclusion.AddForm(crosshairActor.GetActorBase())

	elseif option == restart
        ShowMessage("All player related functionalities of Dirt and Blood will be restarted - Please, exit menu.")
        While (Utility.IsInMenuMode())
            Utility.Wait(0.1)
        EndWhile
        Utility.Wait(1.9)
        Debug.Notification("Restarting functionalities of Dirt & Blood...")
        PlayerRef.RemoveSpell(Dirty_Spell_Dirt1)
        PlayerRef.RemoveSpell(Dirty_Spell_Dirt2)
        PlayerRef.RemoveSpell(Dirty_Spell_Dirt3)
        PlayerRef.RemoveSpell(Dirty_Spell_Dirt4)
        PlayerRef.RemoveSpell(Dirty_Spell_Blood1)
        PlayerRef.RemoveSpell(Dirty_Spell_Blood2)
        PlayerRef.RemoveSpell(Dirty_Spell_Blood3)
        PlayerRef.RemoveSpell(Dirty_Spell_Blood4)
        PlayerRef.RemoveSpell(Dirty_Spell_Clean)
        PlayerRef.RemoveSpell(Dirty_Spell_Swimming)
        RemoveBaseWashPowers()
        PlayerRef.RemoveSpell(Dirty_Spell_NegativeSideEffects)
        PlayerRef.RemoveSpell(Dirty_Spell_PositiveSideEffects)

        Utility.Wait(2)

        PlayerRef.AddSpell(Dirty_Spell_Dirt1, false)
        PlayerRef.AddSpell(Dirty_Spell_Swimming, false)
        PlayerRef.AddSpell(Dirty_Spell_IsRaining, false)
        PlayerRef.AddSpell(Dirty_Spell_NegativeSideEffects, false)
        PlayerRef.AddSpell(Dirty_Spell_PositiveSideEffects, false)
        SyncAuthoriaWashPowers()
        StartHair.UntilNextTime()
        StartDirt.UntilNextTime()
        Debug.Notification("Done!")
	endIf
endEvent

event OnOptionDefault(int option)
	if (option == WashFollowersHotkey_K)
		ClearAuthoriaHotkey(Authoria_WashFollowersHotkey, Authoria_WashFollowersPower)
	elseif (option == WashTogetherHotkey_K)
		ClearAuthoriaHotkey(Authoria_WashTogetherHotkey, Authoria_WashTogetherPower)
	endIf
endEvent

event OnOptionKeyMapChange(int option, int keyCode, string conflictControl, string conflictName)
	if (option == WashFollowersHotkey_K)
		RemapAuthoriaHotkey(keyCode, conflictControl, conflictName, Authoria_WashFollowersHotkey, Authoria_WashFollowersPower)
	elseif (option == WashTogetherHotkey_K)
		RemapAuthoriaHotkey(keyCode, conflictControl, conflictName, Authoria_WashTogetherHotkey, Authoria_WashTogetherPower)
	endIf
endEvent

event OnKeyDown(int keyCode)
	if IsBlockedMenuOpen()
		return
	endIf

	if Authoria_WashFollowersHotkey && keyCode == Authoria_WashFollowersHotkey.GetValueInt()
		if Authoria_WashFollowersPower
			Authoria_WashFollowersPower.Cast(PlayerRef)
		endIf
	elseif Authoria_WashTogetherHotkey && keyCode == Authoria_WashTogetherHotkey.GetValueInt()
		if Authoria_WashTogetherPower
			Authoria_WashTogetherPower.Cast(PlayerRef)
		endIf
	endIf
endEvent

event OnOptionHighlight(int option)
	if (option == dirtsetting_M)
		SetInfoText("How long it takes to become dirtier by advancing to a new stage of dirt. There are 4 stages of dirt in total.\nChanges to frequency start after the already planned next stage update.")
	elseif (option == bloodsetting_m)
		SetInfoText("Chance for your character to get bloody after an unblocked hit. The chance applies\nevery time you get hit, so even though it sounds low I recommend the 5% default setting.")
	elseif (option == NPCReactions_B)
		SetInfoText("NPCs around you might comment on you being visibly dirty.\nThis only happens in the worst stages, and only certain NPCs react, such as children.")
	elseif (option == bloodforNPCS_B)
		SetInfoText("Disabling this will make it so NPCs won't get bloody anymore,\nThis only affects the blood from this mod. Default: On")
	elseif (option == hairsetting_M)
		SetInfoText("This feature will remind you to change your character's hair or beard as they grow longer.\nNot dynamic, but you won't have to use the console. Changes to frequency start after the next planned reminder.")
	elseif (option == SoapRequired_B)
		SetInfoText("Turning this on will make it so you cannot use the Wash and Rinse ability without soap.\nWhen enabled, soap can be obtained by crafting it at a cooking station. Default: Off.")
	elseif (option == RainCleans_B)
		SetInfoText("By default, standing in the rain will clean some of the dirt and blood off you. Default: On.")
	elseif (option == washingautomatic_B)
		SetInfoText("By default, the washing ability will unequip clothes and reequip them at the end of the animation.\nDisable this if you want to remain clothed or want to unequip clothes manually. Default: On.")
	elseif (option == swimcleans_B)
		SetInfoText("By default, swimming only cleans some of the dirt and blood off you.\nEnable this option if you want swimming to clean you completely and not only a little. Default: Off.")
	elseif (option == targetednpc)
		SetInfoText("This option will instantly clean the NPC and add them to an exception list.\nThis means they shouldn't get dirty or bloody again.")
	elseif (option == BanditsDirt_B)
		SetInfoText("There's a chance for bandits to have different levels of dirt on them when this option is active.\nDefault: On.")
	elseif (option == ProfessionsDirt_B)
		SetInfoText("NPCs with certain occupations have a chance to have some dirt on them. Miners, blacksmiths,\nhunters and beggars. The level of dirt changes from time to time. Default: On.")
	elseif (option == ShowMessages_B)
		SetInfoText("Turn this off if you don't want reminders that you're at highest level of dirt or blood.\nMessages about getting cleaned by rain or swimming are also affected by this setting. Default: On.")
	elseif (option == SoundEffect_B)
		SetInfoText("Turn this off if you don't want the water and washing sound effects to play when bathing.\nIf your FPS drop while using the ability, turning this off can help. Default: On.")
	elseif (option == Restart)
		SetInfoText("Clicking here will restart all functionalities of Dirt and Blood related to the player\nThis is useful if you think something isn't working the way it's supposed to.")
	elseif (option == WashFollowersHotkey_K)
		SetInfoText("Assign a hotkey for Wash Followers. If no key is assigned, the power stays in the spell menu.")
	elseif (option == WashTogetherHotkey_K)
		SetInfoText("Assign a hotkey for Wash Together. If no key is assigned, the power stays in the spell menu.")
    elseif (option == NPCBatheAnimation_B)
        SetInfoText("Turn this off if you don't want NPCs to play bathing animations")
    elseif (option == PlayerBatheAnimation_B)
        SetInfoText("Turn this off if you don't want the player to play bathing animations. Keep this off if you are a VR user :)")
	elseif (option == bathanimstyle_M)
		SetInfoText("Choose which animation set plays while bathing.\nMalignis: the immersive tub animation. Default: the original Bathing in Skyrim wash idles. Default setting: Malignis.")
	; Authoria: free camera tooltip
	elseif (option == FreeCamBathing_B)
		SetInfoText("When enabled, the camera enters free camera mode during bathing animations,\nallowing you to orbit around your character. Default: Off.")
	elseif (option == WaterRequired_b)
	      SetInfoText("Requires the mod 'Wade in Water'. You must stand in shallow waters to use soap or wash yourself.")
	endif
endevent

Function ToggleGlobal(GlobalVariable var, int option)
	bool newState = !(var.GetValue() as bool)
	var.SetValue(newState as float)
	SetToggleOptionValue(option, newState, false)
EndFunction

Function ResolveAuthoriaProperties()
	string pluginName = "Authoria - Patch - Dirt and Blood Tweaks.esp"
	if !Authoria_WashFollowersPower
		Authoria_WashFollowersPower = Game.GetFormFromFile(0x00000802, pluginName) as Spell
	endIf
	if !Authoria_WashTogetherPower
		Authoria_WashTogetherPower = Game.GetFormFromFile(0x00000803, pluginName) as Spell
	endIf
	if !Authoria_FreeCamBath
		Authoria_FreeCamBath = Game.GetFormFromFile(0x00000805, pluginName) as GlobalVariable
	endIf
	if !Authoria_BathAnimStyle
		Authoria_BathAnimStyle = Game.GetFormFromFile(0x00000808, pluginName) as GlobalVariable
	endIf
	if !Authoria_WashFollowersHotkey
		Authoria_WashFollowersHotkey = Game.GetFormFromFile(0x00000806, pluginName) as GlobalVariable
	endIf
	if !Authoria_WashTogetherHotkey
		Authoria_WashTogetherHotkey = Game.GetFormFromFile(0x00000807, pluginName) as GlobalVariable
	endIf
EndFunction

bool Function RemapAuthoriaHotkey(int keyCode, string conflictControl, string conflictName, GlobalVariable hotkeyGlobal, Spell hotkeySpell)
	if !hotkeyGlobal || !hotkeySpell
		return false
	endIf

	if conflictControl != ""
		if conflictName != ""
			if !ShowMessage("This key is already bound to " + conflictControl + " in " + conflictName + ". Assign it anyway?", true)
				return false
			endIf
		else
			ShowMessage("This key is already bound to " + conflictControl + " in Skyrim. Please select a different key.", false)
			return false
		endIf
	endIf

	UnregisterForKey(hotkeyGlobal.GetValueInt())
	hotkeyGlobal.SetValueInt(keyCode)
	SyncAuthoriaPower(hotkeyGlobal, hotkeySpell)
	ForcePageReset()
	return true
EndFunction

Function ClearAuthoriaHotkey(GlobalVariable hotkeyGlobal, Spell hotkeySpell)
	if hotkeyGlobal
		UnregisterForKey(hotkeyGlobal.GetValueInt())
		hotkeyGlobal.SetValueInt(0)
	endIf
	if PlayerRef && hotkeySpell
		PlayerRef.AddSpell(hotkeySpell, false)
	endIf
	ForcePageReset()
EndFunction

Function SyncAuthoriaWashPowers()
	RemoveBaseWashPowers()
	UnregisterForAllKeys()
	SyncAuthoriaPower(Authoria_WashFollowersHotkey, Authoria_WashFollowersPower)
	SyncAuthoriaPower(Authoria_WashTogetherHotkey, Authoria_WashTogetherPower)
EndFunction

Function SyncAuthoriaPower(GlobalVariable hotkeyGlobal, Spell powerSpell)
	if !PlayerRef || !hotkeyGlobal || !powerSpell
		return
	endIf

	int keyCode = hotkeyGlobal.GetValueInt()
	if keyCode != 0
		RegisterForKey(keyCode)
		PlayerRef.RemoveSpell(powerSpell)
	else
		PlayerRef.AddSpell(powerSpell, false)
	endIf
EndFunction

Function RemoveBaseWashPowers()
	if !PlayerRef
		return
	endIf

	Spell baseWash = Game.GetFormFromFile(0x0000082F, "Dirt and Blood - Dynamic Visuals.esp") as Spell
	Spell baseWashNPC = Game.GetFormFromFile(0x00000860, "Dirt and Blood - Dynamic Visuals.esp") as Spell
	if baseWash
		PlayerRef.RemoveSpell(baseWash)
	endIf
	if baseWashNPC
		PlayerRef.RemoveSpell(baseWashNPC)
	endIf
EndFunction

bool Function IsBlockedMenuOpen()
	return Utility.IsInMenuMode() || UI.IsMenuOpen("Console") || UI.IsMenuOpen("Dialogue Menu") || UI.IsMenuOpen("FavoritesMenu") || UI.IsMenuOpen("Book Menu") || UI.IsMenuOpen("Crafting Menu") || UI.IsMenuOpen("MessageBoxMenu") || UI.IsMenuOpen("ContainerMenu") || UI.IsMenuOpen("InventoryMenu") || UI.IsMenuOpen("Journal Menu") || UI.IsMenuOpen("StatsMenu") || UI.IsMenuOpen("Sleep/Wait Menu")
EndFunction

; === Legacy Settings Loader Functions ===

Function LoadSettingsAtStart()
	ValidatePapyrusUtil = PapyrusUtil.getVersion()>31

	if ValidatePapyrusUtil
		if JSONUtil.JsonExists(settings_path)
			Utility.Wait(10)
			LoadUserSettings()
		EndIf
	EndIf
EndFunction

state LOAD_DEFAULT_SETTINGS_STATE
	event OnSelectST()
		if ShowMessage("Do you want to load default settings?", true)
			ResetSettings()
			ShowMessage("Settings reset to default values.", false)
		endIf
	endEvent

	event OnHighlightST()
		SetInfoText("Load default settings.")
	endEvent
endState

state LOAD_USER_SETTINGS_STATE
	event OnSelectST()
		if ShowMessage("Do you want to load user settings?", true)
			if LoadUserSettings()
				ShowMessage("User settings loaded successfully.", false)
			else
				ShowMessage("Failed to load user settings.", false)
			endIf
		endIf
	endEvent

	event OnHighlightST()
		if JSONUtil.JsonExists(settings_path)
			SetInfoText("Load user settings.")
		else
			SetInfoText("User settings do not exist.")
		endIf
	endEvent
endState

state SAVE_USER_SETTINGS_STATE
	event OnSelectST()

		if JSONUtil.JsonExists(settings_path)
			if !ShowMessage("Do you want to overwrite existing user settings?", true)
				return
			endIf
		endIf
		if SaveUserSettings()
			ShowMessage("User settings saved successfully.", false)
		else
			ShowMessage("Failed to save user settings.", false)
		endIf

		ForcePageReset()
	endEvent

	event OnHighlightST()
		SetInfoText("Save user settings")
	endEvent
endState

function ResetSettings()
	DirtSettingIndex = 1
	Dirty_RandomDirtDuration.SetValue(1)
	Dirty_NPCsGetBloodyTrue.SetValue(1)
	bloodsettingIndex = 1
	Dirty_PlayerHitBloodyChance.SetValue(5)
	Dirty_ProfessionsDirt.SetValue(1)
	HairSettingIndex = 1
	Dirty_RandomHairDuration.SetValue(1)
	Dirty_BanditsDirt.SetValue(1)
	Dirty_ShowMessages.SetValue(1)

	Dirty_WashingAutomaticClothes.SetValue(1)
	Dirty_RainCleans.SetValue(1)
	Dirty_SoapRequired.SetValue(0)
	Dirty_SwimCleansCompletely.SetValue(0)
	Dirty_SoundEffect.SetValue(1)
	Dirty_NPCReactions.SetValue(1)
	Dirty_WaterRequired.SetValue(0)

	Dirty_NPCBathingAnimation.SetValue(1)
	Dirty_PlayerBathingAnimation.SetValue(1)

	; Authoria: reset free camera
	if Authoria_FreeCamBath
		Authoria_FreeCamBath.SetValue(0)
	endIf
	; Authoria: reset bathing animation style to Malignis (default)
	BathAnimStyleIndex = 1
	if Authoria_BathAnimStyle
		Authoria_BathAnimStyle.SetValue(1)
	endIf
	if Authoria_WashFollowersHotkey
		Authoria_WashFollowersHotkey.SetValueInt(0)
	endIf
	if Authoria_WashTogetherHotkey
		Authoria_WashTogetherHotkey.SetValueInt(0)
	endIf
	SyncAuthoriaWashPowers()

	ForcePageReset()
EndFunction


bool function LoadUserSettings()
	if !JSONUtil.IsGood(settings_path)
		ShowMessage("DirtAndBlood: Can't load User Settings. Errors: {" + JSONUtil.getErrors(settings_path) + "}")
		return false
	endIf

	DirtSettingIndex = JSONUtil.GetPathIntValue(settings_path, "DirtSettingIndex", DirtSettingIndex)
	Dirty_RandomDirtDuration.SetValue(DirtSettingIndex as Float)
	Bool bloodforNPCSToggle = JSONUtil.GetPathBoolValue(settings_path, "BloodForNPCSToggle", True)
	Dirty_NPCsGetBloodyTrue.SetValue(bloodforNPCSToggle as Float)
	bloodsettingIndex = JSONUtil.GetPathIntValue(settings_path, "BloodsettingIndex", bloodsettingIndex)
	if bloodsettingIndex == 0
		Dirty_PlayerHitBloodyChance.SetValue(1)
	elseif bloodsettingIndex == 1
		Dirty_PlayerHitBloodyChance.SetValue(5)
	elseif bloodsettingIndex == 2
		Dirty_PlayerHitBloodyChance.SetValue(15)
	elseif bloodsettingIndex == 3
		Dirty_PlayerHitBloodyChance.SetValue(-50)
	endif
	Bool ProfessionsDirtToggle = JSONUtil.GetPathBoolValue(settings_path, "ProfessionsDirtToggle", True)
	Dirty_ProfessionsDirt.SetValue(ProfessionsDirtToggle as Float)
	HairSettingIndex = JSONUtil.GetPathIntValue(settings_path, "HairSettingIndex", HairSettingIndex)
	Dirty_RandomHairDuration.SetValue(HairSettingIndex as Float)
	Bool BanditsDirtToggle = JSONUtil.GetPathBoolValue(settings_path, "BanditsDirtToggle", True)
	Dirty_BanditsDirt.SetValue(BanditsDirtToggle as Float)
	Bool ShowmessagesToggle = JSONUtil.GetPathBoolValue(settings_path, "ShowmessagesToggle", True)
	Dirty_ShowMessages.SetValue(ShowmessagesToggle as Float)

	Bool washingautomaticToggle = JSONUtil.GetPathBoolValue(settings_path, "WashingAutomaticToggle", True)
	Dirty_WashingAutomaticClothes.SetValue(washingautomaticToggle as Float)
	Bool RainCleansToggle = JSONUtil.GetPathBoolValue(settings_path, "RainCleansToggle", True)
	Dirty_RainCleans.SetValue(RainCleansToggle as Float)
	Bool SoapRequiredToggle = JSONUtil.GetPathBoolValue(settings_path, "SoapRequiredToggle", False)
	Dirty_SoapRequired.SetValue(SoapRequiredToggle as Float)
	Bool swimcleansToggle = JSONUtil.GetPathBoolValue(settings_path, "SwimCleansToggle", False)
	Dirty_SwimCleansCompletely.SetValue(swimcleansToggle as Float)
	Bool soundeffectToggle = JSONUtil.GetPathBoolValue(settings_path, "SoundEffectToggle", True)
	Dirty_SoundEffect.SetValue(soundeffectToggle as Float)
	Bool Dirty_NPCReactionsToggle = JSONUtil.GetPathBoolValue(settings_path, "Dirty_NPCReactions", True)
	Dirty_NPCReactions.SetValue(Dirty_NPCReactionsToggle as Float)
	Bool Dirty_WaterRequiredToggle = JSONUtil.GetPathBoolValue(settings_path, "Dirty_WaterRequired", True)
	Dirty_WaterRequired.SetValue(Dirty_WaterRequiredToggle as Float)

	if Authoria_WashFollowersHotkey
		Authoria_WashFollowersHotkey.SetValueInt(JSONUtil.GetPathIntValue(settings_path, "Authoria_WashFollowersHotkey", 0))
	endIf
	if Authoria_WashTogetherHotkey
		Authoria_WashTogetherHotkey.SetValueInt(JSONUtil.GetPathIntValue(settings_path, "Authoria_WashTogetherHotkey", 0))
	EndIf

	Dirty_NPCBathingAnimation.SetValueInt(JSONUtil.GetPathBoolValue(settings_path, "Dirty_NPCBathingAnimation", True) as Int)
	Dirty_PlayerBathingAnimation.SetValueInt(JSONUtil.GetPathBoolValue(settings_path, "Dirty_PlayerBathingAnimation", True) as Int)

	if Authoria_BathAnimStyle
		int styleVal = JSONUtil.GetPathIntValue(settings_path, "Authoria_BathAnimStyle", 1)
		if styleVal < 0 || styleVal > 1
			styleVal = 1
		endIf
		Authoria_BathAnimStyle.SetValue(styleVal as float)
		BathAnimStyleIndex = styleVal
	endIf

	SyncAuthoriaWashPowers()

	ForcePageReset()
	return true
endFunction

bool function SaveUserSettings()
	JSONUtil.SetPathIntValue(settings_path, "DirtSettingIndex", DirtSettingIndex)
	JSONUtil.SetPathIntValue(settings_path, "BloodForNPCSToggle", Dirty_NPCsGetBloodyTrue.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "BloodsettingIndex", bloodsettingIndex)
	JSONUtil.SetPathIntValue(settings_path, "ProfessionsDirtToggle", Dirty_ProfessionsDirt.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "HairSettingIndex", HairSettingIndex)
	JSONUtil.SetPathIntValue(settings_path, "BanditsDirtToggle", Dirty_BanditsDirt.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "ShowmessagesToggle", Dirty_ShowMessages.GetValueInt())

	JSONUtil.SetPathIntValue(settings_path, "WashingAutomaticToggle", Dirty_WashingAutomaticClothes.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "RainCleansToggle", Dirty_RainCleans.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "SoapRequiredToggle", Dirty_SoapRequired.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "SwimCleansToggle", Dirty_SwimCleansCompletely.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "SoundEffectToggle", Dirty_SoundEffect.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "Dirty_NPCReactions", Dirty_NPCReactions.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "Dirty_WaterRequired", Dirty_WaterRequired.GetValueInt())

	if Authoria_WashFollowersHotkey
		JSONUtil.SetPathIntValue(settings_path, "Authoria_WashFollowersHotkey", Authoria_WashFollowersHotkey.GetValueInt())
	endIf
	if Authoria_WashTogetherHotkey
		JSONUtil.SetPathIntValue(settings_path, "Authoria_WashTogetherHotkey", Authoria_WashTogetherHotkey.GetValueInt())
	endIf

	JSONUtil.SetPathIntValue(settings_path, "Dirty_NPCBathingAnimation", Dirty_NPCBathingAnimation.GetValueInt())
	JSONUtil.SetPathIntValue(settings_path, "Dirty_PlayerBathingAnimation", Dirty_PlayerBathingAnimation.GetValueInt())

	if Authoria_BathAnimStyle
		JSONUtil.SetPathIntValue(settings_path, "Authoria_BathAnimStyle", Authoria_BathAnimStyle.GetValueInt())
	endIf


	if !JSONUtil.save(settings_path)
		Debug.Trace("DirtAndBlood: Error saving user settings.")
		return false
	endIf
	return true
endFunction
