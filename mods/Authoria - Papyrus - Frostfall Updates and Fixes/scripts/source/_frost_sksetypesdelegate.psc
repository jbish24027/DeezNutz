ScriptName _Frost_SKSETypesDelegate Extends Quest
{ The intention of this script is to provide a common way to access objects that require
accessing types that will make the game blow up if SKSE is not available through the
use of Mod Events. }

;-- Variables ---------------------------------------
String CONFIG_PATH = "../FrostfallData/"

;-- Properties --------------------------------------
_frost_exposuremeterinterfacehandler Property ExposureMeterHandler Auto
_frost_skyuiconfigpanelscript Property FrostConfig Auto
_frost_wetnessmeterinterfacehandler Property WetnessMeterHandler Auto
GlobalVariable Property _Frost_AttributeExposureMeter Auto
GlobalVariable Property _Frost_Setting_MeterExposureColor Auto
GlobalVariable Property _Frost_Setting_MeterExposureColorWarm Auto

;-- Functions ---------------------------------------

; Skipped compiler generated GetState

; Skipped compiler generated GotoState

Event OnInit()
  If !Self.IsRunning() ; #DEBUG_LINE_NO:19
    Self.Start() ; #DEBUG_LINE_NO:20
  EndIf
  Self.RegisterForAllEvents() ; #DEBUG_LINE_NO:22
EndEvent

Function RegisterForAllEvents()
  Self.RegisterForModEvent("Frostfall_Upgrade_3_2", "Upgrade_3_2") ; #DEBUG_LINE_NO:26
  Self.RegisterForModEvent("Frostfall_Upgrade_3_2_1", "Upgrade_3_2_1") ; #DEBUG_LINE_NO:27
  Self.RegisterForModEvent("Frostfall_LoadProfileOnStartup", "LoadProfileOnStartup") ; #DEBUG_LINE_NO:28
  Self.RegisterForModEvent("Frostfall_SaveSettingToCurrentProfile", "SaveSettingToCurrentProfile") ; #DEBUG_LINE_NO:29
  Self.RegisterForModEvent("Frostfall_ApplyMeterPreset", "ApplyMeterPreset") ; #DEBUG_LINE_NO:30
  Self.RegisterForModEvent("Frostfall_RegisterForKeysOnLoad", "RegisterForKeysOnLoad") ; #DEBUG_LINE_NO:31
  Self.RegisterForModEvent("Frostfall_CheckInterfacePackage", "Compatibility_CheckInterfacePackage") ; #DEBUG_LINE_NO:32
EndFunction

Function Upgrade_3_2()
  ski_widgetmanager manager = (Game.GetFormFromFile(2084, "SkyUI_SE.esp") as Quest) as ski_widgetmanager ; #DEBUG_LINE_NO:36
  Int id = ((ExposureMeterHandler as Quest) as _frost_meter).WidgetID ; #DEBUG_LINE_NO:37
  manager.CreateWidget(id, "frostfall/meterIndicator.swf") ; #DEBUG_LINE_NO:38
  ExposureMeterHandler.meter_inversion_value = -1.0 ; #DEBUG_LINE_NO:39
  ExposureMeterHandler.improvement_display_delta_threshold = 2.0 ; #DEBUG_LINE_NO:40
  ExposureMeterHandler.SetMeterColors(_Frost_Setting_MeterExposureColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:41
  WetnessMeterHandler.improvement_display_delta_threshold = 30.0 ; #DEBUG_LINE_NO:43
EndFunction

Function Upgrade_3_2_1()
  ExposureMeterHandler.AttributeValue = _Frost_AttributeExposureMeter ; #DEBUG_LINE_NO:48
  ExposureMeterHandler.contextual_display_thresholds = new Float[5] ; #DEBUG_LINE_NO:49
  ExposureMeterHandler.contextual_display_thresholds[0] = 0.0 ; #DEBUG_LINE_NO:50
  ExposureMeterHandler.contextual_display_thresholds[1] = 20.0 ; #DEBUG_LINE_NO:51
  ExposureMeterHandler.contextual_display_thresholds[2] = 40.0 ; #DEBUG_LINE_NO:52
  ExposureMeterHandler.contextual_display_thresholds[3] = 60.0 ; #DEBUG_LINE_NO:53
  ExposureMeterHandler.contextual_display_thresholds[4] = 80.0 ; #DEBUG_LINE_NO:54
  _Frost_Setting_MeterExposureColorWarm.SetValueInt(13369344) ; #DEBUG_LINE_NO:55
EndFunction

Function LoadProfileOnStartup()
  FrostConfig.LoadProfileOnStartup() ; #DEBUG_LINE_NO:59
EndFunction

Function SaveSettingToCurrentProfile(String asKey, Int aiValue)
  FrostConfig.SaveSettingToCurrentProfile(asKey, aiValue) ; #DEBUG_LINE_NO:63
EndFunction

Function ApplyMeterPreset(Int aiValue)
  FrostConfig.ApplyMeterPreset(aiValue) ; #DEBUG_LINE_NO:67
EndFunction

Function RegisterForKeysOnLoad()
  FrostConfig.RegisterForKeysOnLoad() ; #DEBUG_LINE_NO:71
EndFunction

Function Compatibility_CheckInterfacePackage()
  Int ui_package_version_installed = jsonutil.GetIntValue(CONFIG_PATH + "interface_package_version", "installed_package_version", 0) ; #DEBUG_LINE_NO:75
  If ui_package_version_installed == 6 ; #DEBUG_LINE_NO:76
    ski_main skyui = Game.GetFormFromFile(2068, "SkyUI_SE.esp") as ski_main ; #DEBUG_LINE_NO:77
    If !skyui ; #DEBUG_LINE_NO:78
      skyui = Game.GetFormFromFile(2068, "SkyUI.esp") as ski_main ; #DEBUG_LINE_NO:79
    EndIf
    Int skyui_version = skyui.ReqSWFRelease ; #DEBUG_LINE_NO:81
    If skyui_version >= 1026 ; #DEBUG_LINE_NO:82
      frostutil.GetCompatibilitySystem().isUIPackageInstalled = True ; #DEBUG_LINE_NO:83
      Debug.trace((("[Frostfall] Detected optional SkyUI Interface Package version " + ui_package_version_installed as String) + " and SkyUI version " + skyui_version as String) + ", success!", 0) ; #DEBUG_LINE_NO:84
    Else
      frostutil.GetCompatibilitySystem().isUIPackageInstalled = False ; #DEBUG_LINE_NO:86
      frostutil.GetCompatibilitySystem().FatalErrorSkyUIPackage(5) ; #DEBUG_LINE_NO:87
    EndIf
  ElseIf ui_package_version_installed == 5 ; #DEBUG_LINE_NO:89
    frostutil.GetCompatibilitySystem().FatalErrorSkyUIPackageOld() ; #DEBUG_LINE_NO:90
  Else
    frostutil.GetCompatibilitySystem().isUIPackageInstalled = False ; #DEBUG_LINE_NO:92
  EndIf
EndFunction
