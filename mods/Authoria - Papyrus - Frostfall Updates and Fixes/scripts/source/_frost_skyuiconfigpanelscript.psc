ScriptName _Frost_SkyUIConfigPanelScript Extends SKI_ConfigBase

;-- Variables ---------------------------------------
Int Advanced_EnduranceSkillRespec_OID
Int Advanced_EnduranceSkillRestoreSlider_OID
Int Advanced_EnduranceSkillRestore_OID
Int Advanced_TutorialsResetText_OID
Int Advanced_TutorialsToggle_OID
String[] AnimationList
Armor[] ArmorMenuEntries
Int ArmorPage_cursor_position = 0
Bool ArmorPage_loading = True
Bool ArmorPage_updated_msg = False
Int[] ArmorTypeIDs
Int[] Armor_CoverageSliderOIDs
Int Armor_DefaultAllArmorOID
Int[] Armor_DefaultArmorEntryOIDs
Int Armor_DefaultWornArmorOID
Int[] Armor_GearTypeOIDs
Int[] Armor_ModifyPartsOIDs
Int Armor_RepairDefaultsOID
Int[] Armor_SetProtectionOIDs
Int Armor_ShowTutorialOID
Int[] Armor_WarmthSliderOIDs
Float CHARGE_METER_HEIGHT = 22.0
Float CHARGE_METER_HEIGHT_INV = -22.0
Float CHARGE_METER_WIDTH = 292.0
String CONFIG_PATH = "../FrostfallData/"
Float EXPOSURE_METER_BOTTOMLEFT_16_10_X = 64.199996948
Float EXPOSURE_METER_BOTTOMLEFT_16_10_Y = 628.0
Float EXPOSURE_METER_BOTTOMLEFT_16_9_X = 69.199996948
Float EXPOSURE_METER_BOTTOMLEFT_16_9_Y = 618.0
Float EXPOSURE_METER_BOTTOMLEFT_4_3_X = 69.199996948
Float EXPOSURE_METER_BOTTOMLEFT_4_3_Y = 645.0
Int EXPOSURE_METER_BOTTOMLEFT_FILLDIR = 1
Int EXPOSURE_METER_BOTTOMLEFT_HANCHOR = 0
Int EXPOSURE_METER_BOTTOMLEFT_VANCHOR = 1
Float EXPOSURE_METER_BOTTOMRIGHT_16_10_X = 1216.0
Float EXPOSURE_METER_BOTTOMRIGHT_16_10_Y = 628.0
Float EXPOSURE_METER_BOTTOMRIGHT_16_9_X = 1211.0
Float EXPOSURE_METER_BOTTOMRIGHT_16_9_Y = 618.0
Float EXPOSURE_METER_BOTTOMRIGHT_4_3_X = 1218.0
Float EXPOSURE_METER_BOTTOMRIGHT_4_3_Y = 645.0
Int EXPOSURE_METER_BOTTOMRIGHT_FILLDIR = 0
Int EXPOSURE_METER_BOTTOMRIGHT_HANCHOR = 1
Int EXPOSURE_METER_BOTTOMRIGHT_VANCHOR = 1
Float EXPOSURE_METER_TOPLEFT_16_10_X = 64.199996948
Float EXPOSURE_METER_TOPLEFT_16_10_Y = 113.0
Float EXPOSURE_METER_TOPLEFT_16_9_X = 69.199996948
Float EXPOSURE_METER_TOPLEFT_16_9_Y = 113.0
Float EXPOSURE_METER_TOPLEFT_4_3_X = 65.199996948
Float EXPOSURE_METER_TOPLEFT_4_3_Y = 113.0
Int EXPOSURE_METER_TOPLEFT_FILLDIR = 1
Int EXPOSURE_METER_TOPLEFT_HANCHOR = 0
Int EXPOSURE_METER_TOPLEFT_VANCHOR = 0
Float EXPOSURE_METER_TOPRIGHT_16_10_X = 1216.0
Float EXPOSURE_METER_TOPRIGHT_16_10_Y = 113.0
Float EXPOSURE_METER_TOPRIGHT_16_9_X = 1211.0
Float EXPOSURE_METER_TOPRIGHT_16_9_Y = 113.0
Float EXPOSURE_METER_TOPRIGHT_4_3_X = 1218.0
Float EXPOSURE_METER_TOPRIGHT_4_3_Y = 113.0
Int EXPOSURE_METER_TOPRIGHT_FILLDIR = 0
Int EXPOSURE_METER_TOPRIGHT_HANCHOR = 1
Int EXPOSURE_METER_TOPRIGHT_VANCHOR = 0
String[] FILL_DIRECTIONS
String[] FillDirectionList
String[] FillDirectionListLimited
Int Gameplay_DisableFT_OID
Int Gameplay_DisableWaiting_OID
Int Gameplay_ExposurePauseCombat_OID
Int Gameplay_ExposurePauseDialogue_OID
Int Gameplay_ExposureRate_OID
Int Gameplay_FrigidWater_OID
Int Gameplay_MaxExposureMode_OID
Int Gameplay_MovementPenalty_OID
Int Gameplay_VampirismMode_OID
Int Gameplay_WeathersenseHotkey_OID
String[] GearTypeList
String[] HORIZONTAL_ANCHORS
String[] HorizontalAnchorList
Int Interface_Animation_OID
Int Interface_ConditionMessages_OID
Int Interface_DisplayAttributeValuesInWeathersense_OID
Int Interface_DisplayAttributesInWeathersense_OID
Int Interface_FollowerAnimation_OID
Int Interface_ForceFeedback_OID
Int Interface_FrostShaderOn_OID
Int Interface_FullScreenEffects_OID
Int Interface_Notifications_EquipmentSummary_OID
Int Interface_Notifications_EquipmentValues_OID
Int Interface_SoundEffects_OID
Int Interface_WeatherMessages_OID
Int Interface_WeathersenseDisplayMode_OID
Int Interface_WetShaderOn_OID
Int METER_BEING_CONFIGURED_EXPOSURE = 1
Int METER_BEING_CONFIGURED_NONE = 0
Int METER_BEING_CONFIGURED_WEATHERSENSE = 3
Int METER_BEING_CONFIGURED_WETNESS = 2
String[] MaxExposureModeList
String[] MeterDisplayModeList
String[] MeterLayoutList
Int Meters_UIExposureMeterShowAdvanced_OID
Int Meters_UIMeterColorAlt_OID
Int Meters_UIMeterColor_OID
Int Meters_UIMeterDisplayTime_OID
Int Meters_UIMeterDisplay_OID
Int Meters_UIMeterFillDirection_OID
Int Meters_UIMeterFlipped_OID
Int Meters_UIMeterHAnchor_OID
Int Meters_UIMeterLayout_OID
Int Meters_UIMeterOpacity_OID
Int Meters_UIMeterScale_OID
Int Meters_UIMeterVAnchor_OID
Int Meters_UIMeterXPos_OID
Int Meters_UIMeterYPos_OID
Int Meters_UIWeathersenseMeterShowAdvanced_OID
Int Meters_UIWetnessMeterShowAdvanced_OID
Float NORMAL_METER_HEIGHT = 25.200000763
Float NORMAL_METER_WIDTH = 292.799987793
Int Overview_CoverageStatusText_OID
Int Overview_ExposureStatusText_OID
Int Overview_InfoLine1_OID
Int Overview_InfoLine2_OID
Int Overview_InfoLine3_OID
Int Overview_InfoLine4_OID
Int Overview_InfoLine5_OID
Int Overview_InfoLine6_OID
Int Overview_InfoLine7_OID
Int Overview_InfoLine8_OID
Int Overview_RunStatusText_OID
Int Overview_RunSubStatusText_OID
Int Overview_WarmthStatusText_OID
Int Overview_WetnessStatusText_OID
String[] ProfileList
String[] ProtectionList
Int[] ProtectionListCoverageIndex
Int[] ProtectionListWarmthIndex
Int SaveLoad_DefaultProfile_OID
Int SaveLoad_Enable_OID
Int SaveLoad_ProfileHelp_OID
Int SaveLoad_RenameProfile_OID
Int SaveLoad_SelectProfile_OID
String[] VERTICAL_ANCHORS
String[] VampirismModeList
String[] VerticalAnchorList
Float WEATHERSENSE_METER_BOTTOMLEFT_16_10_X = 657.5
Float WEATHERSENSE_METER_BOTTOMLEFT_16_10_Y = 726.5
Float WEATHERSENSE_METER_BOTTOMLEFT_16_9_X = 657.5
Float WEATHERSENSE_METER_BOTTOMLEFT_16_9_Y = 726.5
Float WEATHERSENSE_METER_BOTTOMLEFT_4_3_X = 657.5
Float WEATHERSENSE_METER_BOTTOMLEFT_4_3_Y = 724.5
Int WEATHERSENSE_METER_BOTTOMLEFT_FILLDIR = 2
Int WEATHERSENSE_METER_BOTTOMLEFT_HANCHOR = 2
Int WEATHERSENSE_METER_BOTTOMLEFT_VANCHOR = 1
Float WEATHERSENSE_METER_BOTTOMRIGHT_16_10_X = 657.5
Float WEATHERSENSE_METER_BOTTOMRIGHT_16_10_Y = 726.5
Float WEATHERSENSE_METER_BOTTOMRIGHT_16_9_X = 657.5
Float WEATHERSENSE_METER_BOTTOMRIGHT_16_9_Y = 726.5
Float WEATHERSENSE_METER_BOTTOMRIGHT_4_3_X = 657.5
Float WEATHERSENSE_METER_BOTTOMRIGHT_4_3_Y = 724.5
Int WEATHERSENSE_METER_BOTTOMRIGHT_FILLDIR = 2
Int WEATHERSENSE_METER_BOTTOMRIGHT_HANCHOR = 2
Int WEATHERSENSE_METER_BOTTOMRIGHT_VANCHOR = 1
Float WEATHERSENSE_METER_TOPLEFT_16_10_X = 916.75
Float WEATHERSENSE_METER_TOPLEFT_16_10_Y = 14.0
Float WEATHERSENSE_METER_TOPLEFT_16_9_X = 916.75
Float WEATHERSENSE_METER_TOPLEFT_16_9_Y = 16.0
Float WEATHERSENSE_METER_TOPLEFT_4_3_X = 916.75
Float WEATHERSENSE_METER_TOPLEFT_4_3_Y = 12.0
Int WEATHERSENSE_METER_TOPLEFT_FILLDIR = 2
Int WEATHERSENSE_METER_TOPLEFT_HANCHOR = 2
Int WEATHERSENSE_METER_TOPLEFT_VANCHOR = 0
Float WEATHERSENSE_METER_TOPRIGHT_16_10_X = 916.75
Float WEATHERSENSE_METER_TOPRIGHT_16_10_Y = 14.0
Float WEATHERSENSE_METER_TOPRIGHT_16_9_X = 916.75
Float WEATHERSENSE_METER_TOPRIGHT_16_9_Y = 16.0
Float WEATHERSENSE_METER_TOPRIGHT_4_3_X = 916.75
Float WEATHERSENSE_METER_TOPRIGHT_4_3_Y = 12.0
Int WEATHERSENSE_METER_TOPRIGHT_FILLDIR = 2
Int WEATHERSENSE_METER_TOPRIGHT_HANCHOR = 2
Int WEATHERSENSE_METER_TOPRIGHT_VANCHOR = 0
Float WETNESS_METER_BOTTOMLEFT_16_10_X = 80.5
Float WETNESS_METER_BOTTOMLEFT_16_10_Y = 613.299987793
Float WETNESS_METER_BOTTOMLEFT_16_9_X = 85.5
Float WETNESS_METER_BOTTOMLEFT_16_9_Y = 601.200012207
Float WETNESS_METER_BOTTOMLEFT_4_3_X = 85.5
Float WETNESS_METER_BOTTOMLEFT_4_3_Y = 632.400024414
Int WETNESS_METER_BOTTOMLEFT_FILLDIR = 1
Int WETNESS_METER_BOTTOMLEFT_HANCHOR = 0
Int WETNESS_METER_BOTTOMLEFT_VANCHOR = 1
Float WETNESS_METER_BOTTOMRIGHT_16_10_X = 1232.0
Float WETNESS_METER_BOTTOMRIGHT_16_10_Y = 613.299987793
Float WETNESS_METER_BOTTOMRIGHT_16_9_X = 1227.0
Float WETNESS_METER_BOTTOMRIGHT_16_9_Y = 601.200012207
Float WETNESS_METER_BOTTOMRIGHT_4_3_X = 1234.0
Float WETNESS_METER_BOTTOMRIGHT_4_3_Y = 632.400024414
Int WETNESS_METER_BOTTOMRIGHT_FILLDIR = 0
Int WETNESS_METER_BOTTOMRIGHT_HANCHOR = 1
Int WETNESS_METER_BOTTOMRIGHT_VANCHOR = 1
Float WETNESS_METER_TOPLEFT_16_10_X = 340.5
Float WETNESS_METER_TOPLEFT_16_10_Y = 147.5
Float WETNESS_METER_TOPLEFT_16_9_X = 345.5
Float WETNESS_METER_TOPLEFT_16_9_Y = 151.600006104
Float WETNESS_METER_TOPLEFT_4_3_X = 340.5
Float WETNESS_METER_TOPLEFT_4_3_Y = 142.0
Int WETNESS_METER_TOPLEFT_FILLDIR = 0
Int WETNESS_METER_TOPLEFT_HANCHOR = 0
Int WETNESS_METER_TOPLEFT_VANCHOR = 0
Float WETNESS_METER_TOPRIGHT_16_10_X = 1491.0
Float WETNESS_METER_TOPRIGHT_16_10_Y = 147.5
Float WETNESS_METER_TOPRIGHT_16_9_X = 1486.400024414
Float WETNESS_METER_TOPRIGHT_16_9_Y = 151.600006104
Float WETNESS_METER_TOPRIGHT_4_3_X = 1493.0
Float WETNESS_METER_TOPRIGHT_4_3_Y = 142.0
Int WETNESS_METER_TOPRIGHT_FILLDIR = 1
Int WETNESS_METER_TOPRIGHT_HANCHOR = 1
Int WETNESS_METER_TOPRIGHT_VANCHOR = 0
String[] WeathersenseDisplayList
Bool config_is_open = False
Int meter_being_configured = 0
Bool must_exit = False

;-- Properties --------------------------------------
_frost_compatibility Property Compatibility Auto
GlobalVariable Property EndurancePerkPointProgress Auto
GlobalVariable Property EndurancePerkPoints Auto
GlobalVariable Property EndurancePerkPointsEarned Auto
GlobalVariable Property EndurancePerkPointsTotal Auto
_frost_meter Property ExposureMeter Auto
_frost_exposuremeterinterfacehandler Property ExposureMeterHandler Auto
_frost_main Property FrostfallMain Auto
GlobalVariable Property FrostfallRunning Auto
Actor Property PlayerRef Auto
GlobalVariable Property StartFrostfall Auto
_frost_meter Property WeathersenseMeter Auto
_frost_weathermeterinterfacehandler Property WeathersenseMeterHandler Auto
_frost_meter Property WetnessMeter Auto
_frost_wetnessmeterinterfacehandler Property WetnessMeterHandler Auto
Keyword Property _FrostData_ArmorPrecache Auto
GlobalVariable Property _Frost_AttributeCoverage Auto
GlobalVariable Property _Frost_AttributeExposure Auto
GlobalVariable Property _Frost_AttributeWarmth Auto
GlobalVariable Property _Frost_AttributeWetness Auto
GlobalVariable Property _Frost_Calc_MaxCoverage Auto
GlobalVariable Property _Frost_Calc_MaxWarmth Auto
GlobalVariable Property _Frost_DS_Body_InitProgress Auto
GlobalVariable Property _Frost_DS_Cloak_InitProgress Auto
GlobalVariable Property _Frost_DS_Feet_InitProgress Auto
GlobalVariable Property _Frost_DS_Hands_InitProgress Auto
GlobalVariable Property _Frost_DS_Head_InitProgress Auto
GlobalVariable Property _Frost_DatastoreInitialized Auto
GlobalVariable Property _Frost_HelpDone_Cold Auto
GlobalVariable Property _Frost_HelpDone_Exposure Auto
GlobalVariable Property _Frost_HelpDone_Wet Auto
GlobalVariable Property _Frost_HotkeyWeathersense Auto
GlobalVariable Property _Frost_PerkRank_Adaptation Auto
GlobalVariable Property _Frost_PerkRank_FrostWarding Auto
GlobalVariable Property _Frost_PerkRank_GlacialSwimmer Auto
GlobalVariable Property _Frost_PerkRank_InnerFire Auto
GlobalVariable Property _Frost_PerkRank_WellInsulated Auto
GlobalVariable Property _Frost_PerkRank_Windbreaker Auto
GlobalVariable Property _Frost_Setting_1PAnimationAllowed Auto
{ This setting is deprecated as of Frostfall 3.0.1. }
GlobalVariable Property _Frost_Setting_Animation Auto
GlobalVariable Property _Frost_Setting_AutoSaveLoad Auto
GlobalVariable Property _Frost_Setting_ConditionMessages Auto
GlobalVariable Property _Frost_Setting_CurrentProfile Auto
GlobalVariable Property _Frost_Setting_DisplayAttributeValuesInWeathersense Auto
GlobalVariable Property _Frost_Setting_DisplayAttributesInWeathersense Auto
GlobalVariable Property _Frost_Setting_DisplayTutorials Auto
GlobalVariable Property _Frost_Setting_ExposurePauseCombat Auto
GlobalVariable Property _Frost_Setting_ExposurePauseDialogue Auto
GlobalVariable Property _Frost_Setting_ExposureRate Auto
GlobalVariable Property _Frost_Setting_FollowerAnimation Auto
GlobalVariable Property _Frost_Setting_ForceFeedback Auto
GlobalVariable Property _Frost_Setting_FrigidWaterIsLethal Auto
GlobalVariable Property _Frost_Setting_FrostShaderOn Auto
GlobalVariable Property _Frost_Setting_FullScreenEffects Auto
GlobalVariable Property _Frost_Setting_MaxExposureMode Auto
GlobalVariable Property _Frost_Setting_MeterAspectRatio Auto
{ This setting is deprecated as of Frostfall 3.1. }
GlobalVariable Property _Frost_Setting_MeterDisplayMode Auto
GlobalVariable Property _Frost_Setting_MeterDisplayTime Auto
GlobalVariable Property _Frost_Setting_MeterExposureColor Auto
GlobalVariable Property _Frost_Setting_MeterExposureColorWarm Auto
GlobalVariable Property _Frost_Setting_MeterExposureFillDirection Auto
GlobalVariable Property _Frost_Setting_MeterExposureHAnchor Auto
GlobalVariable Property _Frost_Setting_MeterExposureHeight Auto
GlobalVariable Property _Frost_Setting_MeterExposureOpacity Auto
GlobalVariable Property _Frost_Setting_MeterExposureVAnchor Auto
GlobalVariable Property _Frost_Setting_MeterExposureWidth Auto
GlobalVariable Property _Frost_Setting_MeterExposureXPos Auto
GlobalVariable Property _Frost_Setting_MeterExposureYPos Auto
GlobalVariable Property _Frost_Setting_MeterOpacity Auto
{ This setting is deprecated as of Frostfall 3.1. }
GlobalVariable Property _Frost_Setting_MeterWeathersenseColor Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseFillDirection Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseHAnchor Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseHeight Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseOpacity Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseVAnchor Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseWidth Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseXPos Auto
GlobalVariable Property _Frost_Setting_MeterWeathersenseYPos Auto
GlobalVariable Property _Frost_Setting_MeterWetnessColor Auto
GlobalVariable Property _Frost_Setting_MeterWetnessFillDirection Auto
GlobalVariable Property _Frost_Setting_MeterWetnessHAnchor Auto
GlobalVariable Property _Frost_Setting_MeterWetnessHeight Auto
GlobalVariable Property _Frost_Setting_MeterWetnessOpacity Auto
GlobalVariable Property _Frost_Setting_MeterWetnessVAnchor Auto
GlobalVariable Property _Frost_Setting_MeterWetnessWidth Auto
GlobalVariable Property _Frost_Setting_MeterWetnessXPos Auto
GlobalVariable Property _Frost_Setting_MeterWetnessYPos Auto
GlobalVariable Property _Frost_Setting_MovementPenalty Auto
GlobalVariable Property _Frost_Setting_NoFastTravel Auto
GlobalVariable Property _Frost_Setting_NoWaiting Auto
GlobalVariable Property _Frost_Setting_Notifications_EquipmentSummary Auto
GlobalVariable Property _Frost_Setting_Notifications_EquipmentValues Auto
GlobalVariable Property _Frost_Setting_SoundEffects Auto
GlobalVariable Property _Frost_Setting_VampireMode Auto
GlobalVariable Property _Frost_Setting_WeatherMessages Auto
GlobalVariable Property _Frost_Setting_WeathersenseDisplayMode Auto
GlobalVariable Property _Frost_Setting_WetShaderOn Auto
GlobalVariable Property _Frost_SettingsProfileVersion Auto
Spell Property _Frost_Weathersense_Spell Auto

;-- Functions ---------------------------------------

; Skipped compiler generated GetState

; Skipped compiler generated GotoState

Function OnConfigInit()
  Pages = new String[7] ; #DEBUG_LINE_NO:227
  Pages[0] = "$FrostfallOverviewPage" ; #DEBUG_LINE_NO:228
  Pages[1] = "$FrostfallGameplayPage" ; #DEBUG_LINE_NO:229
  Pages[2] = "$FrostfallEquipmentPage" ; #DEBUG_LINE_NO:230
  Pages[3] = "$FrostfallInterfacePage" ; #DEBUG_LINE_NO:231
  Pages[4] = "$FrostfallMetersPage" ; #DEBUG_LINE_NO:232
  Pages[5] = "$FrostfallSaveLoadPage" ; #DEBUG_LINE_NO:233
  Pages[6] = "$FrostfallAdvancedPage" ; #DEBUG_LINE_NO:234
  MaxExposureModeList = new String[3] ; #DEBUG_LINE_NO:236
  MaxExposureModeList[0] = "$FrostfallMaxExposureNothing" ; #DEBUG_LINE_NO:237
  MaxExposureModeList[1] = "$FrostfallMaxExposureRescue" ; #DEBUG_LINE_NO:238
  MaxExposureModeList[2] = "$FrostfallMaxExposureDeath" ; #DEBUG_LINE_NO:239
  VampirismModeList = new String[3] ; #DEBUG_LINE_NO:241
  VampirismModeList[0] = "$FrostfallVampirismHuman" ; #DEBUG_LINE_NO:242
  VampirismModeList[1] = "$FrostfallVampirismSuperhuman" ; #DEBUG_LINE_NO:243
  VampirismModeList[2] = "$FrostfallVampirismImmortal" ; #DEBUG_LINE_NO:244
  WeathersenseDisplayList = new String[3] ; #DEBUG_LINE_NO:246
  WeathersenseDisplayList[0] = "$FrostfallWeathersenseDisplayMessageOnly" ; #DEBUG_LINE_NO:247
  WeathersenseDisplayList[1] = "$FrostfallWeathersenseDisplayMetersOnly" ; #DEBUG_LINE_NO:248
  WeathersenseDisplayList[2] = "$FrostfallWeathersenseDisplayMessageMeters" ; #DEBUG_LINE_NO:249
  AnimationList = new String[3] ; #DEBUG_LINE_NO:251
  AnimationList[0] = "$FrostfallOff" ; #DEBUG_LINE_NO:252
  AnimationList[1] = "$FrostfallAnimationAuto" ; #DEBUG_LINE_NO:253
  AnimationList[2] = "$FrostfallAnimationPrompt" ; #DEBUG_LINE_NO:254
  MeterLayoutList = new String[4] ; #DEBUG_LINE_NO:256
  MeterLayoutList[0] = "$FrostfallMeterLayoutList1" ; #DEBUG_LINE_NO:257
  MeterLayoutList[1] = "$FrostfallMeterLayoutList2" ; #DEBUG_LINE_NO:258
  MeterLayoutList[2] = "$FrostfallMeterLayoutList3" ; #DEBUG_LINE_NO:259
  MeterLayoutList[3] = "$FrostfallMeterLayoutList4" ; #DEBUG_LINE_NO:260
  MeterDisplayModeList = new String[3] ; #DEBUG_LINE_NO:262
  MeterDisplayModeList[0] = "$FrostfallOff" ; #DEBUG_LINE_NO:263
  MeterDisplayModeList[1] = "$FrostfallAlwaysOn" ; #DEBUG_LINE_NO:264
  MeterDisplayModeList[2] = "$FrostfallContextual" ; #DEBUG_LINE_NO:265
  FillDirectionList = new String[3] ; #DEBUG_LINE_NO:267
  FillDirectionList[0] = "$FrostfallLeft" ; #DEBUG_LINE_NO:268
  FillDirectionList[1] = "$FrostfallRight" ; #DEBUG_LINE_NO:269
  FillDirectionList[2] = "$FrostfallBoth" ; #DEBUG_LINE_NO:270
  FillDirectionListLimited = new String[2] ; #DEBUG_LINE_NO:272
  FillDirectionListLimited[0] = "$FrostfallLeft" ; #DEBUG_LINE_NO:273
  FillDirectionListLimited[1] = "$FrostfallRight" ; #DEBUG_LINE_NO:274
  HorizontalAnchorList = new String[3] ; #DEBUG_LINE_NO:276
  HorizontalAnchorList[0] = "$FrostfallLeft" ; #DEBUG_LINE_NO:277
  HorizontalAnchorList[1] = "$FrostfallRight" ; #DEBUG_LINE_NO:278
  HorizontalAnchorList[2] = "$FrostfallCenter" ; #DEBUG_LINE_NO:279
  VerticalAnchorList = new String[3] ; #DEBUG_LINE_NO:281
  VerticalAnchorList[0] = "$FrostfallTop" ; #DEBUG_LINE_NO:282
  VerticalAnchorList[1] = "$FrostfallBottom" ; #DEBUG_LINE_NO:283
  VerticalAnchorList[2] = "$FrostfallCenter" ; #DEBUG_LINE_NO:284
  GearTypeList = new String[8] ; #DEBUG_LINE_NO:286
  GearTypeList[0] = "$FrostfallArmorGearTypeList0" ; #DEBUG_LINE_NO:287
  GearTypeList[1] = "$FrostfallArmorGearTypeList1" ; #DEBUG_LINE_NO:288
  GearTypeList[2] = "$FrostfallArmorGearTypeList2" ; #DEBUG_LINE_NO:289
  GearTypeList[3] = "$FrostfallArmorGearTypeList3" ; #DEBUG_LINE_NO:290
  GearTypeList[4] = "$FrostfallArmorGearTypeList4" ; #DEBUG_LINE_NO:291
  GearTypeList[5] = "$FrostfallArmorGearTypeList5" ; #DEBUG_LINE_NO:292
  GearTypeList[6] = "$FrostfallArmorGearTypeList6" ; #DEBUG_LINE_NO:293
  GearTypeList[7] = "$FrostfallCancel" ; #DEBUG_LINE_NO:294
  ProtectionList = new String[28] ; #DEBUG_LINE_NO:296
  ProtectionList[0] = "$FrostfallArmorProtectionList0" ; #DEBUG_LINE_NO:297
  ProtectionList[1] = "$FrostfallArmorProtectionList1" ; #DEBUG_LINE_NO:298
  ProtectionList[2] = "$FrostfallArmorProtectionList2" ; #DEBUG_LINE_NO:299
  ProtectionList[3] = "$FrostfallArmorProtectionList3" ; #DEBUG_LINE_NO:300
  ProtectionList[4] = "$FrostfallArmorProtectionList4" ; #DEBUG_LINE_NO:301
  ProtectionList[5] = "$FrostfallArmorProtectionList5" ; #DEBUG_LINE_NO:302
  ProtectionList[6] = "$FrostfallArmorProtectionList6" ; #DEBUG_LINE_NO:303
  ProtectionList[7] = "$FrostfallArmorProtectionList7" ; #DEBUG_LINE_NO:304
  ProtectionList[8] = "$FrostfallArmorProtectionList8" ; #DEBUG_LINE_NO:305
  ProtectionList[9] = "$FrostfallArmorProtectionList9" ; #DEBUG_LINE_NO:306
  ProtectionList[10] = "$FrostfallArmorProtectionList10" ; #DEBUG_LINE_NO:307
  ProtectionList[11] = "$FrostfallArmorProtectionList11" ; #DEBUG_LINE_NO:308
  ProtectionList[12] = "$FrostfallArmorProtectionList12" ; #DEBUG_LINE_NO:309
  ProtectionList[13] = "$FrostfallArmorProtectionList13" ; #DEBUG_LINE_NO:310
  ProtectionList[14] = "$FrostfallArmorProtectionList14" ; #DEBUG_LINE_NO:311
  ProtectionList[15] = "$FrostfallArmorProtectionList15" ; #DEBUG_LINE_NO:312
  ProtectionList[16] = "$FrostfallArmorProtectionList16" ; #DEBUG_LINE_NO:313
  ProtectionList[17] = "$FrostfallArmorProtectionList17" ; #DEBUG_LINE_NO:314
  ProtectionList[18] = "$FrostfallArmorProtectionList18" ; #DEBUG_LINE_NO:315
  ProtectionList[19] = "$FrostfallArmorProtectionList19" ; #DEBUG_LINE_NO:316
  ProtectionList[20] = "$FrostfallArmorProtectionList20" ; #DEBUG_LINE_NO:317
  ProtectionList[21] = "$FrostfallArmorProtectionList21" ; #DEBUG_LINE_NO:318
  ProtectionList[22] = "$FrostfallArmorProtectionList22" ; #DEBUG_LINE_NO:319
  ProtectionList[23] = "$FrostfallArmorProtectionList23" ; #DEBUG_LINE_NO:320
  ProtectionList[24] = "$FrostfallArmorProtectionList24" ; #DEBUG_LINE_NO:321
  ProtectionList[25] = "$FrostfallArmorProtectionList25" ; #DEBUG_LINE_NO:322
  ProtectionList[26] = "$FrostfallArmorProtectionList26" ; #DEBUG_LINE_NO:323
  ProtectionList[27] = "$FrostfallCancel" ; #DEBUG_LINE_NO:324
  ProtectionListWarmthIndex = new Int[24] ; #DEBUG_LINE_NO:326
  ProtectionListWarmthIndex[0] = -1 ; #DEBUG_LINE_NO:327
  ProtectionListWarmthIndex[1] = 0 ; #DEBUG_LINE_NO:328
  ProtectionListWarmthIndex[2] = 1 ; #DEBUG_LINE_NO:329
  ProtectionListWarmthIndex[3] = 2 ; #DEBUG_LINE_NO:330
  ProtectionListWarmthIndex[4] = -1 ; #DEBUG_LINE_NO:331
  ProtectionListWarmthIndex[5] = 2 ; #DEBUG_LINE_NO:332
  ProtectionListWarmthIndex[6] = 3 ; #DEBUG_LINE_NO:333
  ProtectionListWarmthIndex[7] = 4 ; #DEBUG_LINE_NO:334
  ProtectionListWarmthIndex[8] = -1 ; #DEBUG_LINE_NO:335
  ProtectionListWarmthIndex[9] = 1 ; #DEBUG_LINE_NO:336
  ProtectionListWarmthIndex[10] = 1 ; #DEBUG_LINE_NO:337
  ProtectionListWarmthIndex[11] = 2 ; #DEBUG_LINE_NO:338
  ProtectionListWarmthIndex[12] = -1 ; #DEBUG_LINE_NO:339
  ProtectionListWarmthIndex[13] = 0 ; #DEBUG_LINE_NO:340
  ProtectionListWarmthIndex[14] = 1 ; #DEBUG_LINE_NO:341
  ProtectionListWarmthIndex[15] = 2 ; #DEBUG_LINE_NO:342
  ProtectionListWarmthIndex[16] = 3 ; #DEBUG_LINE_NO:343
  ProtectionListWarmthIndex[17] = 4 ; #DEBUG_LINE_NO:344
  ProtectionListWarmthIndex[18] = -1 ; #DEBUG_LINE_NO:345
  ProtectionListWarmthIndex[19] = 1 ; #DEBUG_LINE_NO:346
  ProtectionListWarmthIndex[20] = 0 ; #DEBUG_LINE_NO:347
  ProtectionListWarmthIndex[21] = 1 ; #DEBUG_LINE_NO:348
  ProtectionListWarmthIndex[22] = 1 ; #DEBUG_LINE_NO:349
  ProtectionListWarmthIndex[23] = 4 ; #DEBUG_LINE_NO:350
  ProtectionListCoverageIndex = new Int[24] ; #DEBUG_LINE_NO:352
  ProtectionListCoverageIndex[0] = -1 ; #DEBUG_LINE_NO:353
  ProtectionListCoverageIndex[1] = -2 ; #DEBUG_LINE_NO:354
  ProtectionListCoverageIndex[2] = 5 ; #DEBUG_LINE_NO:355
  ProtectionListCoverageIndex[3] = 5 ; #DEBUG_LINE_NO:356
  ProtectionListCoverageIndex[4] = -1 ; #DEBUG_LINE_NO:357
  ProtectionListCoverageIndex[5] = 6 ; #DEBUG_LINE_NO:358
  ProtectionListCoverageIndex[6] = 6 ; #DEBUG_LINE_NO:359
  ProtectionListCoverageIndex[7] = 7 ; #DEBUG_LINE_NO:360
  ProtectionListCoverageIndex[8] = -1 ; #DEBUG_LINE_NO:361
  ProtectionListCoverageIndex[9] = 7 ; #DEBUG_LINE_NO:362
  ProtectionListCoverageIndex[10] = 8 ; #DEBUG_LINE_NO:363
  ProtectionListCoverageIndex[11] = 9 ; #DEBUG_LINE_NO:364
  ProtectionListCoverageIndex[12] = -1 ; #DEBUG_LINE_NO:365
  ProtectionListCoverageIndex[13] = 5 ; #DEBUG_LINE_NO:366
  ProtectionListCoverageIndex[14] = 6 ; #DEBUG_LINE_NO:367
  ProtectionListCoverageIndex[15] = 7 ; #DEBUG_LINE_NO:368
  ProtectionListCoverageIndex[16] = 8 ; #DEBUG_LINE_NO:369
  ProtectionListCoverageIndex[17] = 9 ; #DEBUG_LINE_NO:370
  ProtectionListCoverageIndex[18] = -1 ; #DEBUG_LINE_NO:371
  ProtectionListCoverageIndex[19] = 5 ; #DEBUG_LINE_NO:372
  ProtectionListCoverageIndex[20] = 6 ; #DEBUG_LINE_NO:373
  ProtectionListCoverageIndex[21] = 6 ; #DEBUG_LINE_NO:374
  ProtectionListCoverageIndex[22] = 9 ; #DEBUG_LINE_NO:375
  ProtectionListCoverageIndex[23] = 6 ; #DEBUG_LINE_NO:376
  FILL_DIRECTIONS = new String[3] ; #DEBUG_LINE_NO:378
  FILL_DIRECTIONS[0] = "Left" ; #DEBUG_LINE_NO:379
  FILL_DIRECTIONS[1] = "Right" ; #DEBUG_LINE_NO:380
  FILL_DIRECTIONS[2] = "Both" ; #DEBUG_LINE_NO:381
  HORIZONTAL_ANCHORS = new String[3] ; #DEBUG_LINE_NO:383
  HORIZONTAL_ANCHORS[0] = "Left" ; #DEBUG_LINE_NO:384
  HORIZONTAL_ANCHORS[1] = "Right" ; #DEBUG_LINE_NO:385
  HORIZONTAL_ANCHORS[2] = "Center" ; #DEBUG_LINE_NO:386
  VERTICAL_ANCHORS = new String[3] ; #DEBUG_LINE_NO:388
  VERTICAL_ANCHORS[0] = "Top" ; #DEBUG_LINE_NO:389
  VERTICAL_ANCHORS[1] = "Bottom" ; #DEBUG_LINE_NO:390
  VERTICAL_ANCHORS[2] = "Center" ; #DEBUG_LINE_NO:391
EndFunction

Int Function GetVersion()
  Return 3 ; #DEBUG_LINE_NO:395
EndFunction

Function OnVersionUpdate(Int a_version)
  Self.OnConfigInit() ; #DEBUG_LINE_NO:399
EndFunction

Function OnPageReset(String page)
  If page == "" ; #DEBUG_LINE_NO:403
    Self.LoadCustomContent("frostfall/frostfall_splash.swf", 0.0, 0.0) ; #DEBUG_LINE_NO:404
  Else
    Self.UnloadCustomContent() ; #DEBUG_LINE_NO:406
  EndIf
  If page == "$FrostfallOverviewPage" ; #DEBUG_LINE_NO:409
    Self.PageReset_Overview() ; #DEBUG_LINE_NO:410
  ElseIf page == "$FrostfallGameplayPage" ; #DEBUG_LINE_NO:411
    Self.PageReset_Gameplay() ; #DEBUG_LINE_NO:412
  ElseIf page == "$FrostfallEquipmentPage" ; #DEBUG_LINE_NO:413
    Self.PageReset_Equipment() ; #DEBUG_LINE_NO:414
  ElseIf page == "$FrostfallInterfacePage" ; #DEBUG_LINE_NO:415
    Self.PageReset_Interface() ; #DEBUG_LINE_NO:416
  ElseIf page == "$FrostfallMetersPage" ; #DEBUG_LINE_NO:417
    Self.PageReset_Meters() ; #DEBUG_LINE_NO:418
  ElseIf page == "$FrostfallSaveLoadPage" ; #DEBUG_LINE_NO:419
    Self.PageReset_SaveLoad() ; #DEBUG_LINE_NO:420
  ElseIf page == "$FrostfallAdvancedPage" ; #DEBUG_LINE_NO:421
    Self.PageReset_Advanced() ; #DEBUG_LINE_NO:422
  EndIf
EndFunction

Function OnConfigOpen()
  If FrostfallRunning.GetValueInt() == 2 && _Frost_DatastoreInitialized.GetValueInt() != 2 ; #DEBUG_LINE_NO:427
    must_exit = True ; #DEBUG_LINE_NO:428
  Else
    must_exit = False ; #DEBUG_LINE_NO:430
  EndIf
  config_is_open = True ; #DEBUG_LINE_NO:433
EndFunction

Function OnConfigClose()
  Self.UnregisterForAllModEvents() ; #DEBUG_LINE_NO:437
  meter_being_configured = METER_BEING_CONFIGURED_NONE ; #DEBUG_LINE_NO:438
  config_is_open = False ; #DEBUG_LINE_NO:439
EndFunction

Function PageReset_Overview()
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:443
  Self.AddHeaderOption("$FrostfallOverviewHeaderStatus", 0) ; #DEBUG_LINE_NO:445
  If FrostfallRunning.GetValueInt() == 2 ; #DEBUG_LINE_NO:446
    If _Frost_DatastoreInitialized.GetValueInt() == 2 ; #DEBUG_LINE_NO:447
      If !must_exit ; #DEBUG_LINE_NO:448
        Overview_RunStatusText_OID = Self.AddTextOption("$FrostfallOverviewCtrlStatus", "$FrostfallEnabled", 0) ; #DEBUG_LINE_NO:449
      Else
        Overview_RunStatusText_OID = Self.AddTextOption("$FrostfallOverviewCtrlStatus", "$FrostfallEnabled", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:451
      EndIf
      Overview_RunSubStatusText_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:453
    Else
      Overview_RunStatusText_OID = Self.AddTextOption("$FrostfallOverviewCtrlStatus", "$FrostfallStartingUp", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:455
      Overview_RunSubStatusText_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:456
    EndIf
  ElseIf Game.IsFightingControlsEnabled() ; #DEBUG_LINE_NO:459
    If !must_exit ; #DEBUG_LINE_NO:460
      Overview_RunStatusText_OID = Self.AddTextOption("$FrostfallOverviewCtrlStatus", "$FrostfallDisabled", 0) ; #DEBUG_LINE_NO:461
    Else
      Overview_RunStatusText_OID = Self.AddTextOption("$FrostfallOverviewCtrlStatus", "$FrostfallDisabled", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:463
    EndIf
    Overview_RunSubStatusText_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:465
  Else
    Overview_RunStatusText_OID = Self.AddTextOption("$FrostfallOverviewCtrlStatus", "$FrostfallDisabled", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:467
    Overview_RunSubStatusText_OID = Self.AddTextOption("$FrostfallCantStart", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:468
  EndIf
  Self.AddHeaderOption("$FrostfallOverviewHeaderInfo", 0) ; #DEBUG_LINE_NO:472
  If FrostfallRunning.GetValueInt() == 2 ; #DEBUG_LINE_NO:473
    If _Frost_DatastoreInitialized.GetValueInt() == 2 ; #DEBUG_LINE_NO:474
      Overview_InfoLine1_OID = Self.AddTextOption("$FrostfallOverviewRunning", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:475
      Overview_InfoLine2_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:476
      Overview_InfoLine3_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:477
      Overview_InfoLine4_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:478
      Overview_InfoLine5_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:479
      Overview_InfoLine6_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:480
      Overview_InfoLine7_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:481
      Overview_InfoLine8_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:482
    Else
      Overview_InfoLine1_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:484
      Overview_InfoLine2_OID = Self.AddTextOption("$FrostfallStartUpProgress", "$FrostfallGeneralExitMenuPrompt", 0) ; #DEBUG_LINE_NO:485
      Overview_InfoLine3_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:486
      Overview_InfoLine4_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:487
      Overview_InfoLine5_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:488
      Overview_InfoLine6_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:489
      Overview_InfoLine7_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:490
      Overview_InfoLine8_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:491
    EndIf
  Else
    Overview_InfoLine1_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:494
    Overview_InfoLine2_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:495
    Overview_InfoLine3_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:496
    Overview_InfoLine4_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:497
    Overview_InfoLine5_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:498
    Overview_InfoLine6_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:499
    Overview_InfoLine7_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:500
    Overview_InfoLine8_OID = Self.AddTextOption("", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:501
  EndIf
  Self.SetCursorPosition(1) ; #DEBUG_LINE_NO:504
  Self.AddHeaderOption("$FrostfallOverviewHeaderPlayerAttributes", 0) ; #DEBUG_LINE_NO:506
  If frostutil.GetExposureSystem().IsSystemRunning() ; #DEBUG_LINE_NO:507
    String exp_val
    Int exposure = Math.Floor(frostutil.GetPlayerExposure()) - 20 ; #DEBUG_LINE_NO:509
    If exposure < 0 ; #DEBUG_LINE_NO:510
      exp_val = "+" + (Math.Abs(exposure as Float) as Int) as String ; #DEBUG_LINE_NO:511
    Else
      exp_val = exposure as String ; #DEBUG_LINE_NO:513
    EndIf
    Overview_ExposureStatusText_OID = Self.AddTextOption("$FrostfallOverviewExposureValue", exp_val, 0) ; #DEBUG_LINE_NO:515
  Else
    Overview_ExposureStatusText_OID = Self.AddTextOption("$FrostfallOverviewExposureValue", "", 0) ; #DEBUG_LINE_NO:517
  EndIf
  If frostutil.GetWetnessSystem().IsSystemRunning() ; #DEBUG_LINE_NO:519
    Overview_WetnessStatusText_OID = Self.AddTextOption("$FrostfallOverviewWetnessValue", (((_Frost_AttributeWetness.GetValueInt() as Float / 750.0) * 100.0) as Int) as String + "%", 0) ; #DEBUG_LINE_NO:520
  Else
    Overview_WetnessStatusText_OID = Self.AddTextOption("$FrostfallOverviewWetnessValue", "", 0) ; #DEBUG_LINE_NO:522
  EndIf
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:525
  Self.AddHeaderOption("$FrostfallOverviewHeaderPlayerStats", 0) ; #DEBUG_LINE_NO:527
  If frostutil.GetWarmthSystem().IsSystemRunning() ; #DEBUG_LINE_NO:528
    Overview_WarmthStatusText_OID = Self.AddTextOption("$FrostfallOverviewWarmthValue", _Frost_AttributeWarmth.GetValueInt() as String, 0) ; #DEBUG_LINE_NO:529
  Else
    Overview_WarmthStatusText_OID = Self.AddTextOption("$FrostfallOverviewWarmthValue", "", 0) ; #DEBUG_LINE_NO:531
  EndIf
  If frostutil.GetCoverageSystem().IsSystemRunning() ; #DEBUG_LINE_NO:533
    Overview_CoverageStatusText_OID = Self.AddTextOption("$FrostfallOverviewCoverageValue", _Frost_AttributeCoverage.GetValueInt() as String, 0) ; #DEBUG_LINE_NO:534
  Else
    Overview_CoverageStatusText_OID = Self.AddTextOption("$FrostfallOverviewCoverageValue", "", 0) ; #DEBUG_LINE_NO:536
  EndIf
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:538
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:539
EndFunction

Function PageReset_Gameplay()
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:543
  If FrostfallRunning.GetValueInt() != 2 || must_exit ; #DEBUG_LINE_NO:544
    Self.AddTextOption("$FrostfallNotRunningError", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:545
    Return  ; #DEBUG_LINE_NO:546
  EndIf
  Self.AddHeaderOption("$FrostfallGameplayHeaderPlayer", 0) ; #DEBUG_LINE_NO:549
  Gameplay_ExposureRate_OID = Self.AddSliderOption("$FrostfallGameplaySettingExposureRate", _Frost_Setting_ExposureRate.GetValue(), "{1}x", 0) ; #DEBUG_LINE_NO:550
  Gameplay_MaxExposureMode_OID = Self.AddMenuOption("$FrostfallGameplaySettingPlayerExposureMode", MaxExposureModeList[_Frost_Setting_MaxExposureMode.GetValueInt() - 1], 0) ; #DEBUG_LINE_NO:551
  If _Frost_Setting_FrigidWaterIsLethal.GetValueInt() == 2 ; #DEBUG_LINE_NO:552
    Gameplay_FrigidWater_OID = Self.AddToggleOption("$FrostfallGameplaySettingExposureWaterLethality", True, 0) ; #DEBUG_LINE_NO:553
  Else
    Gameplay_FrigidWater_OID = Self.AddToggleOption("$FrostfallGameplaySettingExposureWaterLethality", False, 0) ; #DEBUG_LINE_NO:555
  EndIf
  If _Frost_Setting_ExposurePauseDialogue.GetValueInt() == 2 ; #DEBUG_LINE_NO:557
    Gameplay_ExposurePauseDialogue_OID = Self.AddToggleOption("$FrostfallGameplaySettingExposureDialoguePause", True, 0) ; #DEBUG_LINE_NO:558
  Else
    Gameplay_ExposurePauseDialogue_OID = Self.AddToggleOption("$FrostfallGameplaySettingExposureDialoguePause", False, 0) ; #DEBUG_LINE_NO:560
  EndIf
  If _Frost_Setting_ExposurePauseCombat.GetValueInt() == 2 ; #DEBUG_LINE_NO:562
    Gameplay_ExposurePauseCombat_OID = Self.AddToggleOption("$FrostfallGameplaySettingExposureCombatPause", True, 0) ; #DEBUG_LINE_NO:563
  Else
    Gameplay_ExposurePauseCombat_OID = Self.AddToggleOption("$FrostfallGameplaySettingExposureCombatPause", False, 0) ; #DEBUG_LINE_NO:565
  EndIf
  If _Frost_Setting_MovementPenalty.GetValueInt() == 2 ; #DEBUG_LINE_NO:567
    Gameplay_MovementPenalty_OID = Self.AddToggleOption("$FrostfallGameplaySettingPlayerMovement", True, 0) ; #DEBUG_LINE_NO:568
  Else
    Gameplay_MovementPenalty_OID = Self.AddToggleOption("$FrostfallGameplaySettingPlayerMovement", False, 0) ; #DEBUG_LINE_NO:570
  EndIf
  Gameplay_VampirismMode_OID = Self.AddMenuOption("$FrostfallGameplaySettingPlayerVampirism", VampirismModeList[_Frost_Setting_VampireMode.GetValueInt()], 0) ; #DEBUG_LINE_NO:572
  Self.AddHeaderOption("$FrostfallGameplayHeaderFastTravel", 0) ; #DEBUG_LINE_NO:574
  If _Frost_Setting_NoWaiting.GetValueInt() == 2 ; #DEBUG_LINE_NO:575
    Gameplay_DisableFT_OID = Self.AddToggleOption("$FrostfallGameplaySettingFTToggle", True, Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:576
  ElseIf _Frost_Setting_NoFastTravel.GetValueInt() == 2 ; #DEBUG_LINE_NO:578
    Gameplay_DisableFT_OID = Self.AddToggleOption("$FrostfallGameplaySettingFTToggle", True, 0) ; #DEBUG_LINE_NO:579
  Else
    Gameplay_DisableFT_OID = Self.AddToggleOption("$FrostfallGameplaySettingFTToggle", False, 0) ; #DEBUG_LINE_NO:581
  EndIf
  If _Frost_Setting_NoWaiting.GetValueInt() == 2 ; #DEBUG_LINE_NO:584
    Gameplay_DisableWaiting_OID = Self.AddToggleOption("$FrostfallGameplaySettingFTWaiting", True, 0) ; #DEBUG_LINE_NO:585
  Else
    Gameplay_DisableWaiting_OID = Self.AddToggleOption("$FrostfallGameplaySettingFTWaiting", False, 0) ; #DEBUG_LINE_NO:587
  EndIf
  Self.SetCursorPosition(1) ; #DEBUG_LINE_NO:590
  Self.AddHeaderOption("$FrostfallGameplayHeaderWorld", 0) ; #DEBUG_LINE_NO:592
  Self.AddTextOption("$FrostfallComingSoon", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:593
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:594
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:595
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:596
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:597
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:598
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:599
  Self.AddHeaderOption("$FrostfallGameplayHeaderHotkeys", 0) ; #DEBUG_LINE_NO:601
  Gameplay_WeathersenseHotkey_OID = Self.AddKeyMapOption("$FrostfallHotkeyWeathersense", _Frost_HotkeyWeathersense.GetValueInt(), 0) ; #DEBUG_LINE_NO:602
EndFunction

Function PageReset_Equipment()
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:607
  If FrostfallRunning.GetValueInt() != 2 || must_exit ; #DEBUG_LINE_NO:608
    Self.AddTextOption("$FrostfallNotRunningError", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:609
    Return  ; #DEBUG_LINE_NO:610
  EndIf
  If ArmorPage_loading == True ; #DEBUG_LINE_NO:613
    Self.AddTextOption("$FrostfallArmorLoadingPage", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:614
    ArmorPage_loading = False ; #DEBUG_LINE_NO:615
    Self.ForcePageReset() ; #DEBUG_LINE_NO:616
  Else
    Self.GenerateEquipmentPage() ; #DEBUG_LINE_NO:618
    ArmorPage_loading = True ; #DEBUG_LINE_NO:619
  EndIf
  If ArmorPage_updated_msg ; #DEBUG_LINE_NO:622
    Self.ShowMessage("$FrostfallArmorUpdatingPage", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:623
    ArmorPage_updated_msg = False ; #DEBUG_LINE_NO:624
  EndIf
EndFunction

Function PageReset_Interface()
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:629
  If FrostfallRunning.GetValueInt() != 2 || must_exit ; #DEBUG_LINE_NO:630
    Self.AddTextOption("$FrostfallNotRunningError", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:631
    Return  ; #DEBUG_LINE_NO:632
  EndIf
  Self.AddHeaderOption("$FrostfallInterfaceHeaderEffects", 0) ; #DEBUG_LINE_NO:635
  If _Frost_Setting_FrostShaderOn.GetValueInt() == 2 ; #DEBUG_LINE_NO:636
    Interface_FrostShaderOn_OID = Self.AddToggleOption("$FrostfallInterfaceSettingFrostShader", True, 0) ; #DEBUG_LINE_NO:637
  Else
    Interface_FrostShaderOn_OID = Self.AddToggleOption("$FrostfallInterfaceSettingFrostShader", False, 0) ; #DEBUG_LINE_NO:639
  EndIf
  If _Frost_Setting_WetShaderOn.GetValueInt() == 2 ; #DEBUG_LINE_NO:641
    Interface_WetShaderOn_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWetShader", True, 0) ; #DEBUG_LINE_NO:642
  Else
    Interface_WetShaderOn_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWetShader", False, 0) ; #DEBUG_LINE_NO:644
  EndIf
  If _Frost_Setting_SoundEffects.GetValueInt() == 2 ; #DEBUG_LINE_NO:646
    Interface_SoundEffects_OID = Self.AddToggleOption("$FrostfallInterfaceSettingSoundEffects", True, 0) ; #DEBUG_LINE_NO:647
  Else
    Interface_SoundEffects_OID = Self.AddToggleOption("$FrostfallInterfaceSettingSoundEffects", False, 0) ; #DEBUG_LINE_NO:649
  EndIf
  If _Frost_Setting_FullScreenEffects.GetValueInt() == 2 ; #DEBUG_LINE_NO:651
    Interface_FullScreenEffects_OID = Self.AddToggleOption("$FrostfallInterfaceSettingImagespaceModifiers", True, 0) ; #DEBUG_LINE_NO:652
  Else
    Interface_FullScreenEffects_OID = Self.AddToggleOption("$FrostfallInterfaceSettingImagespaceModifiers", False, 0) ; #DEBUG_LINE_NO:654
  EndIf
  If _Frost_Setting_ForceFeedback.GetValueInt() == 2 ; #DEBUG_LINE_NO:656
    Interface_ForceFeedback_OID = Self.AddToggleOption("$FrostfallInterfaceSettingForceFeedback", True, 0) ; #DEBUG_LINE_NO:657
  Else
    Interface_ForceFeedback_OID = Self.AddToggleOption("$FrostfallInterfaceSettingForceFeedback", False, 0) ; #DEBUG_LINE_NO:659
  EndIf
  Interface_Animation_OID = Self.AddMenuOption("$FrostfallInterfaceSettingAnimation", AnimationList[_Frost_Setting_Animation.GetValueInt() - 1], 0) ; #DEBUG_LINE_NO:661
  If _Frost_Setting_FollowerAnimation.GetValueInt() == 2 ; #DEBUG_LINE_NO:662
    Interface_FollowerAnimation_OID = Self.AddToggleOption("$FrostfallInterfaceSettingFollowerAnimation", True, 0) ; #DEBUG_LINE_NO:663
  Else
    Interface_FollowerAnimation_OID = Self.AddToggleOption("$FrostfallInterfaceSettingFollowerAnimation", False, 0) ; #DEBUG_LINE_NO:665
  EndIf
  Self.SetCursorPosition(1) ; #DEBUG_LINE_NO:668
  Self.AddHeaderOption("$FrostfallInterfaceHeaderNotifications", 0) ; #DEBUG_LINE_NO:670
  If _Frost_Setting_ConditionMessages.GetValueInt() == 2 ; #DEBUG_LINE_NO:671
    Interface_ConditionMessages_OID = Self.AddToggleOption("$FrostfallInterfaceSettingCondition", True, 0) ; #DEBUG_LINE_NO:672
  Else
    Interface_ConditionMessages_OID = Self.AddToggleOption("$FrostfallInterfaceSettingCondition", False, 0) ; #DEBUG_LINE_NO:674
  EndIf
  If _Frost_Setting_WeatherMessages.GetValueInt() == 2 ; #DEBUG_LINE_NO:676
    Interface_WeatherMessages_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWeather", True, 0) ; #DEBUG_LINE_NO:677
  Else
    Interface_WeatherMessages_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWeather", False, 0) ; #DEBUG_LINE_NO:679
  EndIf
  Interface_WeathersenseDisplayMode_OID = Self.AddMenuOption("$FrostfallInterfaceSettingWeathersenseDisplayMode", WeathersenseDisplayList[_Frost_Setting_WeathersenseDisplayMode.GetValueInt()], 0) ; #DEBUG_LINE_NO:681
  If _Frost_Setting_DisplayAttributesInWeathersense.GetValueInt() == 2 ; #DEBUG_LINE_NO:683
    Interface_DisplayAttributesInWeathersense_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWeathersense", True, 0) ; #DEBUG_LINE_NO:684
    If _Frost_Setting_DisplayAttributeValuesInWeathersense.GetValueInt() == 2 ; #DEBUG_LINE_NO:685
      Interface_DisplayAttributeValuesInWeathersense_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWeathersenseDetail", True, 0) ; #DEBUG_LINE_NO:686
    Else
      Interface_DisplayAttributeValuesInWeathersense_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWeathersenseDetail", False, 0) ; #DEBUG_LINE_NO:688
    EndIf
  Else
    Interface_DisplayAttributesInWeathersense_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWeathersense", False, 0) ; #DEBUG_LINE_NO:691
    Interface_DisplayAttributeValuesInWeathersense_OID = Self.AddToggleOption("$FrostfallInterfaceSettingWeathersenseDetail", False, Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:692
  EndIf
  If Compatibility.isUIPackageInstalled ; #DEBUG_LINE_NO:695
    
  Else
    If _Frost_Setting_Notifications_EquipmentValues.GetValueInt() == 2 ; #DEBUG_LINE_NO:698
      Interface_Notifications_EquipmentValues_OID = Self.AddToggleOption("$FrostfallInterfaceSettingEquipmentValues", True, 0) ; #DEBUG_LINE_NO:699
    Else
      Interface_Notifications_EquipmentValues_OID = Self.AddToggleOption("$FrostfallInterfaceSettingEquipmentValues", False, 0) ; #DEBUG_LINE_NO:701
    EndIf
    If _Frost_Setting_Notifications_EquipmentSummary.GetValueInt() == 2 ; #DEBUG_LINE_NO:703
      Interface_Notifications_EquipmentSummary_OID = Self.AddToggleOption("$FrostfallInterfaceSettingEquipmentSummary", True, 0) ; #DEBUG_LINE_NO:704
    Else
      Interface_Notifications_EquipmentSummary_OID = Self.AddToggleOption("$FrostfallInterfaceSettingEquipmentSummary", False, 0) ; #DEBUG_LINE_NO:706
    EndIf
  EndIf
EndFunction

Function PageReset_Meters()
  If FrostfallRunning.GetValueInt() != 2 || must_exit ; #DEBUG_LINE_NO:712
    Self.AddTextOption("$FrostfallNotRunningError", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:713
    Return  ; #DEBUG_LINE_NO:714
  EndIf
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:717
  Self.AddHeaderOption("$FrostfallInterfaceHeaderMetersGeneral", 0) ; #DEBUG_LINE_NO:718
  Meters_UIMeterDisplay_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterDisplay", MeterDisplayModeList[_Frost_Setting_MeterDisplayMode.GetValueInt()], 0) ; #DEBUG_LINE_NO:719
  Meters_UIMeterDisplayTime_OID = Self.AddSliderOption("$FrostfallInterfaceSettingMeterDisplaytime", _Frost_Setting_MeterDisplayTime.GetValue() * 2 as Float, "{0}", 0) ; #DEBUG_LINE_NO:720
  Meters_UIMeterLayout_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterLayout", "$FrostfallSelect", 0) ; #DEBUG_LINE_NO:721
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:722
  Self.AddHeaderOption("$FrostfallInterfaceHeaderMetersExposureName", 0) ; #DEBUG_LINE_NO:723
  Meters_UIExposureMeterShowAdvanced_OID = Self.AddToggleOption("$FrostfallInterfaceSettingUIMeterShowAdvanced", meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE, 0) ; #DEBUG_LINE_NO:724
  Self.AddHeaderOption("$FrostfallInterfaceHeaderMetersWetnessName", 0) ; #DEBUG_LINE_NO:725
  Meters_UIWetnessMeterShowAdvanced_OID = Self.AddToggleOption("$FrostfallInterfaceSettingUIMeterShowAdvanced", meter_being_configured == METER_BEING_CONFIGURED_WETNESS, 0) ; #DEBUG_LINE_NO:726
  Self.AddHeaderOption("$FrostfallInterfaceHeaderMetersWeathersenseName", 0) ; #DEBUG_LINE_NO:727
  Meters_UIWeathersenseMeterShowAdvanced_OID = Self.AddToggleOption("$FrostfallInterfaceSettingUIMeterShowAdvanced", meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE, 0) ; #DEBUG_LINE_NO:728
  Self.SetCursorPosition(1) ; #DEBUG_LINE_NO:730
  If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:733
    Self.AddHeaderOption("$FrostfallInterfaceHeaderMetersAdvanced", 0) ; #DEBUG_LINE_NO:734
    Self.AddTextOption("$FrostfallInterfaceSettingUIMeterConfiguring", "$FrostfallInterfaceHeaderMetersExposureName", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:735
    Meters_UIMeterColor_OID = Self.AddColorOption("$FrostfallInterfaceSettingUIColorExposure", _Frost_Setting_MeterExposureColor.GetValueInt(), 0) ; #DEBUG_LINE_NO:736
    Meters_UIMeterColorAlt_OID = Self.AddColorOption("$FrostfallInterfaceSettingUIColorExposureAlt", _Frost_Setting_MeterExposureColorWarm.GetValueInt(), 0) ; #DEBUG_LINE_NO:737
    Meters_UIMeterOpacity_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterOpacity", _Frost_Setting_MeterExposureOpacity.GetValue(), "{0}%", 0) ; #DEBUG_LINE_NO:738
    Meters_UIMeterFillDirection_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterFillDirection", FillDirectionListLimited[_Frost_Setting_MeterExposureFillDirection.GetValueInt()], 0) ; #DEBUG_LINE_NO:739
    Meters_UIMeterScale_OID = Self.AddSliderOption("$FrostfallScale", Self.GetMeterScale(_Frost_Setting_MeterExposureWidth.GetValue(), NORMAL_METER_WIDTH), "{2}", 0) ; #DEBUG_LINE_NO:740
    Meters_UIMeterXPos_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterXPos", _Frost_Setting_MeterExposureXPos.GetValue(), "{1}", 0) ; #DEBUG_LINE_NO:741
    Meters_UIMeterYPos_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterYPos", _Frost_Setting_MeterExposureYPos.GetValue(), "{1}", 0) ; #DEBUG_LINE_NO:742
    Meters_UIMeterHAnchor_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterHAnchor", HorizontalAnchorList[_Frost_Setting_MeterExposureHAnchor.GetValueInt()], 0) ; #DEBUG_LINE_NO:743
    Meters_UIMeterVAnchor_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterVAnchor", VerticalAnchorList[_Frost_Setting_MeterExposureVAnchor.GetValueInt()], 0) ; #DEBUG_LINE_NO:744
  ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:745
    Self.AddHeaderOption("$FrostfallInterfaceHeaderMetersAdvanced", 0) ; #DEBUG_LINE_NO:746
    Self.AddTextOption("$FrostfallInterfaceSettingUIMeterConfiguring", "$FrostfallInterfaceHeaderMetersWetnessName", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:747
    Meters_UIMeterColor_OID = Self.AddColorOption("$FrostfallInterfaceSettingUIColor", _Frost_Setting_MeterWetnessColor.GetValueInt(), 0) ; #DEBUG_LINE_NO:748
    Meters_UIMeterOpacity_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterOpacity", _Frost_Setting_MeterWetnessOpacity.GetValue(), "{0}%", 0) ; #DEBUG_LINE_NO:749
    Meters_UIMeterFillDirection_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterFillDirection", FillDirectionListLimited[_Frost_Setting_MeterWetnessFillDirection.GetValueInt()], 0) ; #DEBUG_LINE_NO:750
    Meters_UIMeterScale_OID = Self.AddSliderOption("$FrostfallScale", Self.GetMeterScale(_Frost_Setting_MeterWetnessWidth.GetValue(), CHARGE_METER_WIDTH), "{2}", 0) ; #DEBUG_LINE_NO:751
    Meters_UIMeterFlipped_OID = Self.AddToggleOption("$FrostfallFlipped", _Frost_Setting_MeterWetnessHeight.GetValue() < 0 as Float, 0) ; #DEBUG_LINE_NO:752
    Meters_UIMeterXPos_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterXPos", _Frost_Setting_MeterWetnessXPos.GetValue(), "{1}", 0) ; #DEBUG_LINE_NO:753
    Meters_UIMeterYPos_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterYPos", _Frost_Setting_MeterWetnessYPos.GetValue(), "{1}", 0) ; #DEBUG_LINE_NO:754
    Meters_UIMeterHAnchor_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterHAnchor", HorizontalAnchorList[_Frost_Setting_MeterWetnessHAnchor.GetValueInt()], 0) ; #DEBUG_LINE_NO:755
    Meters_UIMeterVAnchor_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterVAnchor", VerticalAnchorList[_Frost_Setting_MeterWetnessVAnchor.GetValueInt()], 0) ; #DEBUG_LINE_NO:756
  ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:757
    Self.AddHeaderOption("$FrostfallInterfaceHeaderMetersAdvanced", 0) ; #DEBUG_LINE_NO:758
    Self.AddTextOption("$FrostfallInterfaceSettingUIMeterConfiguring", "$FrostfallInterfaceHeaderMetersWeathersenseName", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:759
    Meters_UIMeterColor_OID = Self.AddColorOption("$FrostfallInterfaceSettingUIColor", _Frost_Setting_MeterWeathersenseColor.GetValueInt(), 0) ; #DEBUG_LINE_NO:760
    Meters_UIMeterOpacity_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterOpacity", _Frost_Setting_MeterWeathersenseOpacity.GetValue(), "{0}%", 0) ; #DEBUG_LINE_NO:761
    Meters_UIMeterFillDirection_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterFillDirection", FillDirectionList[_Frost_Setting_MeterWeathersenseFillDirection.GetValueInt()], 0) ; #DEBUG_LINE_NO:762
    Meters_UIMeterScale_OID = Self.AddSliderOption("$FrostfallScale", Self.GetMeterScale(_Frost_Setting_MeterWeathersenseWidth.GetValue(), CHARGE_METER_WIDTH), "{2}", 0) ; #DEBUG_LINE_NO:763
    Meters_UIMeterFlipped_OID = Self.AddToggleOption("$FrostfallFlipped", _Frost_Setting_MeterWeathersenseHeight.GetValue() < 0 as Float, 0) ; #DEBUG_LINE_NO:764
    Meters_UIMeterXPos_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterXPos", _Frost_Setting_MeterWeathersenseXPos.GetValue(), "{1}", 0) ; #DEBUG_LINE_NO:765
    Meters_UIMeterYPos_OID = Self.AddSliderOption("$FrostfallInterfaceSettingUIMeterYPos", _Frost_Setting_MeterWeathersenseYPos.GetValue(), "{1}", 0) ; #DEBUG_LINE_NO:766
    Meters_UIMeterHAnchor_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterHAnchor", HorizontalAnchorList[_Frost_Setting_MeterWeathersenseHAnchor.GetValueInt()], 0) ; #DEBUG_LINE_NO:767
    Meters_UIMeterVAnchor_OID = Self.AddMenuOption("$FrostfallInterfaceSettingUIMeterVAnchor", VerticalAnchorList[_Frost_Setting_MeterWeathersenseVAnchor.GetValueInt()], 0) ; #DEBUG_LINE_NO:768
  EndIf
EndFunction

Function PageReset_SaveLoad()
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:773
  If FrostfallRunning.GetValueInt() != 2 || must_exit ; #DEBUG_LINE_NO:774
    Self.AddTextOption("$FrostfallNotRunningError", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:775
    Return  ; #DEBUG_LINE_NO:776
  EndIf
  Self.AddHeaderOption("$FrostfallSaveLoadHeaderProfile", 0) ; #DEBUG_LINE_NO:779
  If _Frost_Setting_AutoSaveLoad.GetValueInt() == 2 ; #DEBUG_LINE_NO:780
    SaveLoad_SelectProfile_OID = Self.AddMenuOption("$FrostfallSaveLoadCurrentProfile", Self.GetProfileName(_Frost_Setting_CurrentProfile.GetValueInt()), 0) ; #DEBUG_LINE_NO:781
  Else
    SaveLoad_SelectProfile_OID = Self.AddMenuOption("$FrostfallSaveLoadCurrentProfile", Self.GetProfileName(_Frost_Setting_CurrentProfile.GetValueInt()), Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:783
  EndIf
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:785
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:786
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:787
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:788
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:789
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:790
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:791
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:792
  SaveLoad_ProfileHelp_OID = Self.AddTextOption("$FrostfallSaveLoadAboutProfiles", "", 0) ; #DEBUG_LINE_NO:793
  If _Frost_Setting_AutoSaveLoad.GetValueInt() == 2 ; #DEBUG_LINE_NO:794
    SaveLoad_Enable_OID = Self.AddToggleOption("$FrostfallSaveLoadEnable", True, 0) ; #DEBUG_LINE_NO:795
  Else
    SaveLoad_Enable_OID = Self.AddToggleOption("$FrostfallSaveLoadEnable", False, 0) ; #DEBUG_LINE_NO:797
  EndIf
  Self.SetCursorPosition(1) ; #DEBUG_LINE_NO:800
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:802
  If _Frost_Setting_AutoSaveLoad.GetValueInt() == 2 ; #DEBUG_LINE_NO:803
    ski_main skyui = Game.GetFormFromFile(2068, "SkyUI_SE.esp") as ski_main ; #DEBUG_LINE_NO:804
    If !skyui ; #DEBUG_LINE_NO:805
      skyui = Game.GetFormFromFile(2068, "SkyUI.esp") as ski_main ; #DEBUG_LINE_NO:806
    EndIf
    Int version = skyui.ReqSWFRelease ; #DEBUG_LINE_NO:808
    If version >= 1026 ; #DEBUG_LINE_NO:809
      SaveLoad_RenameProfile_OID = Self.AddInputOption("", "$FrostfallSaveLoadRenameProfile", 0) ; #DEBUG_LINE_NO:810
    Else
      SaveLoad_RenameProfile_OID = Self.AddTextOption("$FrostfallSkyUI51Required", "$FrostfallSaveLoadRenameProfile", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:812
    EndIf
    SaveLoad_DefaultProfile_OID = Self.AddTextOption("", "$FrostfallSaveLoadDefaultProfile", 0) ; #DEBUG_LINE_NO:814
  EndIf
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:816
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:817
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:818
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:819
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:820
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:821
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:822
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:823
  If _Frost_Setting_AutoSaveLoad.GetValueInt() == 2 ; #DEBUG_LINE_NO:824
    Self.AddTextOption("$FrostfallSaveLoadSettingsSaved", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:825
  EndIf
EndFunction

Function PageReset_Advanced()
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:830
  If FrostfallRunning.GetValueInt() != 2 || must_exit ; #DEBUG_LINE_NO:831
    Self.AddTextOption("$FrostfallNotRunningError", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:832
    Return  ; #DEBUG_LINE_NO:833
  EndIf
  Self.AddHeaderOption("$FrostfallAdvancedHeaderEnduranceSkill", 0) ; #DEBUG_LINE_NO:836
  Advanced_EnduranceSkillRespec_OID = Self.AddTextOption("$FrostfallAdvancedEnduranceSkillRespec", "", 0) ; #DEBUG_LINE_NO:837
  Advanced_EnduranceSkillRestore_OID = Self.AddToggleOption("$FrostfallAdvancedEnduranceSkillRestore", False, 0) ; #DEBUG_LINE_NO:838
  Advanced_EnduranceSkillRestoreSlider_OID = Self.AddSliderOption("$FrostfallAdvancedEnduranceSkillRestoreAmount", 0 as Float, "{0}", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:839
  Self.SetCursorPosition(1) ; #DEBUG_LINE_NO:841
  Self.AddHeaderOption("$FrostfallAdvancedHeaderTutorials", 0) ; #DEBUG_LINE_NO:843
  If _Frost_Setting_DisplayTutorials.GetValueInt() == 2 ; #DEBUG_LINE_NO:844
    Advanced_TutorialsToggle_OID = Self.AddToggleOption("$FrostfallAdvancedSettingTutorialsShow", True, 0) ; #DEBUG_LINE_NO:845
  Else
    Advanced_TutorialsToggle_OID = Self.AddToggleOption("$FrostfallAdvancedSettingTutorialsShow", False, 0) ; #DEBUG_LINE_NO:847
  EndIf
  Advanced_TutorialsResetText_OID = Self.AddTextOption("", "$FrostfallAdvancedSettingTutorialsReset", 0) ; #DEBUG_LINE_NO:849
EndFunction

Function OnOptionSelect(Int option)
  If option == Overview_RunStatusText_OID ; #DEBUG_LINE_NO:854
    If FrostfallRunning.GetValueInt() == 2 ; #DEBUG_LINE_NO:855
      Bool b = Self.ShowMessage("$FrostfallOverviewShutDownPrompt", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:856
      If b ; #DEBUG_LINE_NO:857
        must_exit = True ; #DEBUG_LINE_NO:858
        FrostfallRunning.SetValue(1 as Float) ; #DEBUG_LINE_NO:859
        Self.ForcePageReset() ; #DEBUG_LINE_NO:860
        FrostfallMain.RegisterForModEvents() ; #DEBUG_LINE_NO:861
        Self.SendEvent_StopFrostfall() ; #DEBUG_LINE_NO:862
      EndIf
    Else
      Bool b = Self.ShowMessage("$FrostfallOverviewStartUpPrompt", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:865
      If b ; #DEBUG_LINE_NO:866
        must_exit = True ; #DEBUG_LINE_NO:867
        FrostfallRunning.SetValue(2 as Float) ; #DEBUG_LINE_NO:868
        Self.ForcePageReset() ; #DEBUG_LINE_NO:869
        FrostfallMain.RegisterForModEvents() ; #DEBUG_LINE_NO:870
        Self.SendEvent_StartFrostfall() ; #DEBUG_LINE_NO:871
      EndIf
    EndIf
  ElseIf option == Gameplay_FrigidWater_OID ; #DEBUG_LINE_NO:874
    If _Frost_Setting_FrigidWaterIsLethal.GetValueInt() == 2 ; #DEBUG_LINE_NO:875
      _Frost_Setting_FrigidWaterIsLethal.SetValueInt(1) ; #DEBUG_LINE_NO:876
      Self.SetToggleOptionValue(Gameplay_FrigidWater_OID, False, False) ; #DEBUG_LINE_NO:877
    Else
      _Frost_Setting_FrigidWaterIsLethal.SetValueInt(2) ; #DEBUG_LINE_NO:879
      Self.SetToggleOptionValue(Gameplay_FrigidWater_OID, True, False) ; #DEBUG_LINE_NO:880
    EndIf
    Self.SaveSettingToCurrentProfile("frigid_water_is_lethal", _Frost_Setting_FrigidWaterIsLethal.GetValueInt()) ; #DEBUG_LINE_NO:882
  ElseIf option == Gameplay_ExposurePauseDialogue_OID ; #DEBUG_LINE_NO:883
    If _Frost_Setting_ExposurePauseDialogue.GetValueInt() == 2 ; #DEBUG_LINE_NO:884
      _Frost_Setting_ExposurePauseDialogue.SetValueInt(1) ; #DEBUG_LINE_NO:885
      Self.SetToggleOptionValue(Gameplay_ExposurePauseDialogue_OID, False, False) ; #DEBUG_LINE_NO:886
    Else
      _Frost_Setting_ExposurePauseDialogue.SetValueInt(2) ; #DEBUG_LINE_NO:888
      Self.SetToggleOptionValue(Gameplay_ExposurePauseDialogue_OID, True, False) ; #DEBUG_LINE_NO:889
    EndIf
    Self.SaveSettingToCurrentProfile("exposure_pause_dialogue", _Frost_Setting_ExposurePauseDialogue.GetValueInt()) ; #DEBUG_LINE_NO:891
  ElseIf option == Gameplay_ExposurePauseCombat_OID ; #DEBUG_LINE_NO:892
    If _Frost_Setting_ExposurePauseCombat.GetValueInt() == 2 ; #DEBUG_LINE_NO:893
      _Frost_Setting_ExposurePauseCombat.SetValueInt(1) ; #DEBUG_LINE_NO:894
      Self.SetToggleOptionValue(Gameplay_ExposurePauseCombat_OID, False, False) ; #DEBUG_LINE_NO:895
    Else
      _Frost_Setting_ExposurePauseCombat.SetValueInt(2) ; #DEBUG_LINE_NO:897
      Self.SetToggleOptionValue(Gameplay_ExposurePauseCombat_OID, True, False) ; #DEBUG_LINE_NO:898
    EndIf
    Self.SaveSettingToCurrentProfile("exposure_pause_combat", _Frost_Setting_ExposurePauseCombat.GetValueInt()) ; #DEBUG_LINE_NO:900
  ElseIf option == Gameplay_MovementPenalty_OID ; #DEBUG_LINE_NO:901
    If _Frost_Setting_MovementPenalty.GetValueInt() == 2 ; #DEBUG_LINE_NO:902
      _Frost_Setting_MovementPenalty.SetValueInt(1) ; #DEBUG_LINE_NO:903
      Self.SetToggleOptionValue(Gameplay_MovementPenalty_OID, False, False) ; #DEBUG_LINE_NO:904
    Else
      _Frost_Setting_MovementPenalty.SetValueInt(2) ; #DEBUG_LINE_NO:906
      Self.SetToggleOptionValue(Gameplay_MovementPenalty_OID, True, False) ; #DEBUG_LINE_NO:907
    EndIf
    Self.SaveSettingToCurrentProfile("movement_penalty", _Frost_Setting_MovementPenalty.GetValueInt()) ; #DEBUG_LINE_NO:909
  ElseIf option == Gameplay_DisableFT_OID ; #DEBUG_LINE_NO:910
    If _Frost_Setting_NoFastTravel.GetValueInt() == 2 ; #DEBUG_LINE_NO:911
      _Frost_Setting_NoFastTravel.SetValueInt(1) ; #DEBUG_LINE_NO:912
      Self.SetToggleOptionValue(Gameplay_DisableFT_OID, False, False) ; #DEBUG_LINE_NO:913
    Else
      _Frost_Setting_NoFastTravel.SetValueInt(2) ; #DEBUG_LINE_NO:915
      Self.SetToggleOptionValue(Gameplay_DisableFT_OID, True, False) ; #DEBUG_LINE_NO:916
    EndIf
    Self.SaveSettingToCurrentProfile("no_fast_travel", _Frost_Setting_NoFastTravel.GetValueInt()) ; #DEBUG_LINE_NO:918
  ElseIf option == Gameplay_DisableWaiting_OID ; #DEBUG_LINE_NO:919
    If _Frost_Setting_NoWaiting.GetValueInt() == 2 ; #DEBUG_LINE_NO:920
      _Frost_Setting_NoWaiting.SetValueInt(1) ; #DEBUG_LINE_NO:921
      Self.SetToggleOptionValue(Gameplay_DisableWaiting_OID, False, False) ; #DEBUG_LINE_NO:922
      Self.ForcePageReset() ; #DEBUG_LINE_NO:923
    Else
      _Frost_Setting_NoWaiting.SetValueInt(2) ; #DEBUG_LINE_NO:925
      Self.SetToggleOptionValue(Gameplay_DisableWaiting_OID, True, False) ; #DEBUG_LINE_NO:926
      Self.ForcePageReset() ; #DEBUG_LINE_NO:927
    EndIf
    Self.SaveSettingToCurrentProfile("no_waiting", _Frost_Setting_NoWaiting.GetValueInt()) ; #DEBUG_LINE_NO:929
  ElseIf option == Interface_FrostShaderOn_OID ; #DEBUG_LINE_NO:930
    If _Frost_Setting_FrostShaderOn.GetValueInt() == 2 ; #DEBUG_LINE_NO:931
      _Frost_Setting_FrostShaderOn.SetValueInt(1) ; #DEBUG_LINE_NO:932
      Self.SetToggleOptionValue(Interface_FrostShaderOn_OID, False, False) ; #DEBUG_LINE_NO:933
    Else
      _Frost_Setting_FrostShaderOn.SetValueInt(2) ; #DEBUG_LINE_NO:935
      Self.SetToggleOptionValue(Interface_FrostShaderOn_OID, True, False) ; #DEBUG_LINE_NO:936
    EndIf
    Self.SaveSettingToCurrentProfile("frost_shader_on", _Frost_Setting_FrostShaderOn.GetValueInt()) ; #DEBUG_LINE_NO:938
  ElseIf option == Interface_WetShaderOn_OID ; #DEBUG_LINE_NO:939
    If _Frost_Setting_WetShaderOn.GetValueInt() == 2 ; #DEBUG_LINE_NO:940
      _Frost_Setting_WetShaderOn.SetValueInt(1) ; #DEBUG_LINE_NO:941
      Self.SetToggleOptionValue(Interface_WetShaderOn_OID, False, False) ; #DEBUG_LINE_NO:942
    Else
      _Frost_Setting_WetShaderOn.SetValueInt(2) ; #DEBUG_LINE_NO:944
      Self.SetToggleOptionValue(Interface_WetShaderOn_OID, True, False) ; #DEBUG_LINE_NO:945
    EndIf
    Self.SaveSettingToCurrentProfile("wet_shader_on", _Frost_Setting_WetShaderOn.GetValueInt()) ; #DEBUG_LINE_NO:947
  ElseIf option == Interface_SoundEffects_OID ; #DEBUG_LINE_NO:948
    If _Frost_Setting_SoundEffects.GetValueInt() == 2 ; #DEBUG_LINE_NO:949
      _Frost_Setting_SoundEffects.SetValueInt(1) ; #DEBUG_LINE_NO:950
      Self.SetToggleOptionValue(Interface_SoundEffects_OID, False, False) ; #DEBUG_LINE_NO:951
    Else
      _Frost_Setting_SoundEffects.SetValueInt(2) ; #DEBUG_LINE_NO:953
      Self.SetToggleOptionValue(Interface_SoundEffects_OID, True, False) ; #DEBUG_LINE_NO:954
    EndIf
    Self.SaveSettingToCurrentProfile("sound_effects", _Frost_Setting_SoundEffects.GetValueInt()) ; #DEBUG_LINE_NO:956
  ElseIf option == Interface_FullScreenEffects_OID ; #DEBUG_LINE_NO:957
    If _Frost_Setting_FullScreenEffects.GetValueInt() == 2 ; #DEBUG_LINE_NO:958
      _Frost_Setting_FullScreenEffects.SetValueInt(1) ; #DEBUG_LINE_NO:959
      Self.SetToggleOptionValue(Interface_FullScreenEffects_OID, False, False) ; #DEBUG_LINE_NO:960
    Else
      _Frost_Setting_FullScreenEffects.SetValueInt(2) ; #DEBUG_LINE_NO:962
      Self.SetToggleOptionValue(Interface_FullScreenEffects_OID, True, False) ; #DEBUG_LINE_NO:963
    EndIf
    Self.SaveSettingToCurrentProfile("full_screen_effects", _Frost_Setting_FullScreenEffects.GetValueInt()) ; #DEBUG_LINE_NO:965
  ElseIf option == Interface_ForceFeedback_OID ; #DEBUG_LINE_NO:966
    If _Frost_Setting_ForceFeedback.GetValueInt() == 2 ; #DEBUG_LINE_NO:967
      _Frost_Setting_ForceFeedback.SetValueInt(1) ; #DEBUG_LINE_NO:968
      Self.SetToggleOptionValue(Interface_ForceFeedback_OID, False, False) ; #DEBUG_LINE_NO:969
    Else
      _Frost_Setting_ForceFeedback.SetValueInt(2) ; #DEBUG_LINE_NO:971
      Self.SetToggleOptionValue(Interface_ForceFeedback_OID, True, False) ; #DEBUG_LINE_NO:972
    EndIf
    Self.SaveSettingToCurrentProfile("force_feedback", _Frost_Setting_ForceFeedback.GetValueInt()) ; #DEBUG_LINE_NO:974
  ElseIf option == Interface_FollowerAnimation_OID ; #DEBUG_LINE_NO:975
    If _Frost_Setting_FollowerAnimation.GetValueInt() == 2 ; #DEBUG_LINE_NO:976
      _Frost_Setting_FollowerAnimation.SetValueInt(1) ; #DEBUG_LINE_NO:977
      Self.SetToggleOptionValue(Interface_FollowerAnimation_OID, False, False) ; #DEBUG_LINE_NO:978
    Else
      _Frost_Setting_FollowerAnimation.SetValueInt(2) ; #DEBUG_LINE_NO:980
      Self.SetToggleOptionValue(Interface_FollowerAnimation_OID, True, False) ; #DEBUG_LINE_NO:981
    EndIf
    Self.SaveSettingToCurrentProfile("follower_animation", _Frost_Setting_FollowerAnimation.GetValueInt()) ; #DEBUG_LINE_NO:983
  ElseIf option == Interface_DisplayAttributesInWeathersense_OID ; #DEBUG_LINE_NO:984
    If _Frost_Setting_DisplayAttributesInWeathersense.GetValueInt() == 2 ; #DEBUG_LINE_NO:985
      _Frost_Setting_DisplayAttributesInWeathersense.SetValueInt(1) ; #DEBUG_LINE_NO:986
      Self.SetToggleOptionValue(Interface_DisplayAttributesInWeathersense_OID, False, False) ; #DEBUG_LINE_NO:987
    Else
      _Frost_Setting_DisplayAttributesInWeathersense.SetValueInt(2) ; #DEBUG_LINE_NO:989
      Self.SetToggleOptionValue(Interface_DisplayAttributesInWeathersense_OID, True, False) ; #DEBUG_LINE_NO:990
    EndIf
    Self.SaveSettingToCurrentProfile("display_attributes_in_weathersense", _Frost_Setting_DisplayAttributesInWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:992
    Self.ForcePageReset() ; #DEBUG_LINE_NO:993
  ElseIf option == Interface_DisplayAttributeValuesInWeathersense_OID ; #DEBUG_LINE_NO:994
    If _Frost_Setting_DisplayAttributeValuesInWeathersense.GetValueInt() == 2 ; #DEBUG_LINE_NO:995
      _Frost_Setting_DisplayAttributeValuesInWeathersense.SetValueInt(1) ; #DEBUG_LINE_NO:996
      Self.SetToggleOptionValue(Interface_DisplayAttributeValuesInWeathersense_OID, False, False) ; #DEBUG_LINE_NO:997
    Else
      _Frost_Setting_DisplayAttributeValuesInWeathersense.SetValueInt(2) ; #DEBUG_LINE_NO:999
      Self.SetToggleOptionValue(Interface_DisplayAttributeValuesInWeathersense_OID, True, False) ; #DEBUG_LINE_NO:1000
    EndIf
    Self.SaveSettingToCurrentProfile("display_attribute_values_in_weathersense", _Frost_Setting_DisplayAttributeValuesInWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:1002
  ElseIf option == Interface_ConditionMessages_OID ; #DEBUG_LINE_NO:1003
    If _Frost_Setting_ConditionMessages.GetValueInt() == 2 ; #DEBUG_LINE_NO:1004
      _Frost_Setting_ConditionMessages.SetValueInt(1) ; #DEBUG_LINE_NO:1005
      Self.SetToggleOptionValue(Interface_ConditionMessages_OID, False, False) ; #DEBUG_LINE_NO:1006
    Else
      _Frost_Setting_ConditionMessages.SetValueInt(2) ; #DEBUG_LINE_NO:1008
      Self.SetToggleOptionValue(Interface_ConditionMessages_OID, True, False) ; #DEBUG_LINE_NO:1009
    EndIf
    Self.SaveSettingToCurrentProfile("condition_messages", _Frost_Setting_ConditionMessages.GetValueInt()) ; #DEBUG_LINE_NO:1011
  ElseIf option == Interface_WeatherMessages_OID ; #DEBUG_LINE_NO:1012
    If _Frost_Setting_WeatherMessages.GetValueInt() == 2 ; #DEBUG_LINE_NO:1013
      _Frost_Setting_WeatherMessages.SetValueInt(1) ; #DEBUG_LINE_NO:1014
      Self.SetToggleOptionValue(Interface_WeatherMessages_OID, False, False) ; #DEBUG_LINE_NO:1015
    Else
      _Frost_Setting_WeatherMessages.SetValueInt(2) ; #DEBUG_LINE_NO:1017
      Self.SetToggleOptionValue(Interface_WeatherMessages_OID, True, False) ; #DEBUG_LINE_NO:1018
    EndIf
    Self.SaveSettingToCurrentProfile("weather_messages", _Frost_Setting_WeatherMessages.GetValueInt()) ; #DEBUG_LINE_NO:1020
  ElseIf option == Interface_Notifications_EquipmentValues_OID ; #DEBUG_LINE_NO:1021
    If _Frost_Setting_Notifications_EquipmentValues.GetValueInt() == 2 ; #DEBUG_LINE_NO:1022
      _Frost_Setting_Notifications_EquipmentValues.SetValueInt(1) ; #DEBUG_LINE_NO:1023
      Self.SetToggleOptionValue(Interface_Notifications_EquipmentValues_OID, False, False) ; #DEBUG_LINE_NO:1024
    Else
      _Frost_Setting_Notifications_EquipmentValues.SetValueInt(2) ; #DEBUG_LINE_NO:1026
      Self.SetToggleOptionValue(Interface_Notifications_EquipmentValues_OID, True, False) ; #DEBUG_LINE_NO:1027
    EndIf
    Self.SaveSettingToCurrentProfile("notification_equipmentvalues", _Frost_Setting_Notifications_EquipmentValues.GetValueInt()) ; #DEBUG_LINE_NO:1029
  ElseIf option == Interface_Notifications_EquipmentSummary_OID ; #DEBUG_LINE_NO:1030
    If _Frost_Setting_Notifications_EquipmentSummary.GetValueInt() == 2 ; #DEBUG_LINE_NO:1031
      _Frost_Setting_Notifications_EquipmentSummary.SetValueInt(1) ; #DEBUG_LINE_NO:1032
      Self.SetToggleOptionValue(Interface_Notifications_EquipmentSummary_OID, False, False) ; #DEBUG_LINE_NO:1033
    Else
      _Frost_Setting_Notifications_EquipmentSummary.SetValueInt(2) ; #DEBUG_LINE_NO:1035
      Self.SetToggleOptionValue(Interface_Notifications_EquipmentSummary_OID, True, False) ; #DEBUG_LINE_NO:1036
    EndIf
    Self.SaveSettingToCurrentProfile("notification_equipmentsummary", _Frost_Setting_Notifications_EquipmentSummary.GetValueInt()) ; #DEBUG_LINE_NO:1038
  ElseIf option == Meters_UIExposureMeterShowAdvanced_OID ; #DEBUG_LINE_NO:1039
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1040
      meter_being_configured = METER_BEING_CONFIGURED_NONE ; #DEBUG_LINE_NO:1041
    Else
      meter_being_configured = METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1043
    EndIf
    Self.ForcePageReset() ; #DEBUG_LINE_NO:1045
  ElseIf option == Meters_UIWetnessMeterShowAdvanced_OID ; #DEBUG_LINE_NO:1046
    If meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1047
      meter_being_configured = METER_BEING_CONFIGURED_NONE ; #DEBUG_LINE_NO:1048
    Else
      meter_being_configured = METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1050
    EndIf
    Self.ForcePageReset() ; #DEBUG_LINE_NO:1052
  ElseIf option == Meters_UIWeathersenseMeterShowAdvanced_OID ; #DEBUG_LINE_NO:1053
    If meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1054
      meter_being_configured = METER_BEING_CONFIGURED_NONE ; #DEBUG_LINE_NO:1055
    Else
      meter_being_configured = METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1057
    EndIf
    Self.ForcePageReset() ; #DEBUG_LINE_NO:1059
  ElseIf option == Meters_UIMeterFlipped_OID ; #DEBUG_LINE_NO:1060
    If meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1061
      Float scale = Self.GetMeterScale(_Frost_Setting_MeterWetnessWidth.GetValue(), CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:1062
      If _Frost_Setting_MeterWetnessHeight.GetValue() > 0 as Float ; #DEBUG_LINE_NO:1063
        _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV * scale) ; #DEBUG_LINE_NO:1064
        Self.SetToggleOptionValue(Meters_UIMeterFlipped_OID, True, False) ; #DEBUG_LINE_NO:1065
      Else
        _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT * scale) ; #DEBUG_LINE_NO:1067
        Self.SetToggleOptionValue(Meters_UIMeterFlipped_OID, False, False) ; #DEBUG_LINE_NO:1068
      EndIf
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1070
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_height", _Frost_Setting_MeterWetnessHeight.GetValue()) ; #DEBUG_LINE_NO:1071
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1072
      Float scale = Self.GetMeterScale(_Frost_Setting_MeterWeathersenseWidth.GetValue(), CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:1073
      If _Frost_Setting_MeterWeathersenseHeight.GetValue() > 0 as Float ; #DEBUG_LINE_NO:1074
        _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV * scale) ; #DEBUG_LINE_NO:1075
        Self.SetToggleOptionValue(Meters_UIMeterFlipped_OID, True, False) ; #DEBUG_LINE_NO:1076
      Else
        _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT * scale) ; #DEBUG_LINE_NO:1078
        Self.SetToggleOptionValue(Meters_UIMeterFlipped_OID, False, False) ; #DEBUG_LINE_NO:1079
      EndIf
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1081
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_height", _Frost_Setting_MeterWeathersenseHeight.GetValue()) ; #DEBUG_LINE_NO:1082
    EndIf
  ElseIf option == SaveLoad_DefaultProfile_OID ; #DEBUG_LINE_NO:1084
    Bool b = Self.ShowMessage("$FrostfallSaveLoadDefaultProfileConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1085
    If b ; #DEBUG_LINE_NO:1086
      Self.GenerateDefaultProfile(_Frost_Setting_CurrentProfile.GetValueInt()) ; #DEBUG_LINE_NO:1087
      Self.SwitchToProfile(_Frost_Setting_CurrentProfile.GetValueInt()) ; #DEBUG_LINE_NO:1088
      Self.ForcePageReset() ; #DEBUG_LINE_NO:1089
    EndIf
  ElseIf option == SaveLoad_Enable_OID ; #DEBUG_LINE_NO:1091
    If _Frost_Setting_AutoSaveLoad.GetValueInt() == 2 ; #DEBUG_LINE_NO:1092
      _Frost_Setting_AutoSaveLoad.SetValueInt(1) ; #DEBUG_LINE_NO:1093
      Self.SetToggleOptionValue(SaveLoad_Enable_OID, False, False) ; #DEBUG_LINE_NO:1094
      jsonutil.SetIntValue(CONFIG_PATH + "common", "auto_load", 1) ; #DEBUG_LINE_NO:1095
      jsonutil.Save(CONFIG_PATH + "common", False) ; #DEBUG_LINE_NO:1096
    ElseIf _Frost_Setting_AutoSaveLoad.GetValueInt() == 1 ; #DEBUG_LINE_NO:1097
      _Frost_Setting_AutoSaveLoad.SetValueInt(2) ; #DEBUG_LINE_NO:1098
      Self.SetToggleOptionValue(SaveLoad_Enable_OID, True, False) ; #DEBUG_LINE_NO:1099
      jsonutil.SetIntValue(CONFIG_PATH + "common", "auto_load", 2) ; #DEBUG_LINE_NO:1100
      jsonutil.Save(CONFIG_PATH + "common", False) ; #DEBUG_LINE_NO:1101
      Self.SaveAllSettings(_Frost_Setting_CurrentProfile.GetValueInt()) ; #DEBUG_LINE_NO:1102
    EndIf
    Self.ForcePageReset() ; #DEBUG_LINE_NO:1104
  ElseIf option == SaveLoad_ProfileHelp_OID ; #DEBUG_LINE_NO:1105
    Self.ShowProfileHelp() ; #DEBUG_LINE_NO:1106
  ElseIf option == Advanced_EnduranceSkillRespec_OID ; #DEBUG_LINE_NO:1107
    Bool b = Self.ShowMessage("$FrostfallAdvancedEnduranceSkillRespecConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1108
    If b ; #DEBUG_LINE_NO:1109
      Self.RefundEnduranceSkillPoints() ; #DEBUG_LINE_NO:1110
      Self.ShowMessage("$FrostfallAdvancedEnduranceSkillRestoreDone", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1111
    EndIf
  ElseIf option == Advanced_EnduranceSkillRestore_OID ; #DEBUG_LINE_NO:1113
    Bool b = Self.ShowMessage("$FrostfallAdvancedEnduranceSkillRestoreConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1114
    If b ; #DEBUG_LINE_NO:1115
      Self.ShowMessage("$FrostfallAdvancedEnduranceSkillRestoreSelect", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1116
      Self.SetToggleOptionValue(Advanced_EnduranceSkillRestore_OID, True, True) ; #DEBUG_LINE_NO:1117
      Self.SetOptionFlags(Advanced_EnduranceSkillRestoreSlider_OID, Self.OPTION_FLAG_NONE, False) ; #DEBUG_LINE_NO:1118
    EndIf
  ElseIf option == Advanced_TutorialsToggle_OID ; #DEBUG_LINE_NO:1120
    If _Frost_Setting_DisplayTutorials.GetValueInt() == 2 ; #DEBUG_LINE_NO:1121
      _Frost_Setting_DisplayTutorials.SetValueInt(1) ; #DEBUG_LINE_NO:1122
      Self.SetToggleOptionValue(Advanced_TutorialsToggle_OID, False, False) ; #DEBUG_LINE_NO:1123
    Else
      _Frost_Setting_DisplayTutorials.SetValueInt(2) ; #DEBUG_LINE_NO:1125
      Self.SetToggleOptionValue(Advanced_TutorialsToggle_OID, True, False) ; #DEBUG_LINE_NO:1126
    EndIf
    Self.SaveSettingToCurrentProfile("display_tutorials", _Frost_Setting_DisplayTutorials.GetValueInt()) ; #DEBUG_LINE_NO:1128
  ElseIf option == Advanced_TutorialsResetText_OID ; #DEBUG_LINE_NO:1129
    Bool b = Self.ShowMessage("$FrostfallTutorialResetPrompt", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1130
    If b ; #DEBUG_LINE_NO:1131
      _Frost_HelpDone_Exposure.SetValueInt(1) ; #DEBUG_LINE_NO:1132
      _Frost_HelpDone_Wet.SetValueInt(1) ; #DEBUG_LINE_NO:1133
      _Frost_HelpDone_Cold.SetValueInt(1) ; #DEBUG_LINE_NO:1134
    EndIf
  ElseIf option == Armor_ShowTutorialOID ; #DEBUG_LINE_NO:1136
    Self.ShowTutorial_ArmorPage(True) ; #DEBUG_LINE_NO:1137
  ElseIf option == Armor_RepairDefaultsOID ; #DEBUG_LINE_NO:1138
    Self.RepairArmorDefaults() ; #DEBUG_LINE_NO:1139
  ElseIf option == Armor_DefaultWornArmorOID ; #DEBUG_LINE_NO:1140
    Self.DefaultWornArmor() ; #DEBUG_LINE_NO:1141
  ElseIf option == Armor_DefaultAllArmorOID ; #DEBUG_LINE_NO:1142
    Self.DefaultAllArmor() ; #DEBUG_LINE_NO:1143
  EndIf
EndFunction

Function OnOptionDefault(Int option)
  If option == Interface_Animation_OID ; #DEBUG_LINE_NO:1148
    _Frost_Setting_Animation.SetValueInt(2) ; #DEBUG_LINE_NO:1149
    Self.SetMenuOptionValue(Interface_Animation_OID, AnimationList[1], False) ; #DEBUG_LINE_NO:1150
    Self.SaveSettingToCurrentProfile("animation", _Frost_Setting_Animation.GetValueInt()) ; #DEBUG_LINE_NO:1151
  ElseIf option == Interface_FollowerAnimation_OID ; #DEBUG_LINE_NO:1152
    _Frost_Setting_FollowerAnimation.SetValueInt(2) ; #DEBUG_LINE_NO:1153
    Self.SetToggleOptionValue(Interface_FollowerAnimation_OID, True, False) ; #DEBUG_LINE_NO:1154
    Self.SaveSettingToCurrentProfile("follower_animation", _Frost_Setting_FollowerAnimation.GetValueInt()) ; #DEBUG_LINE_NO:1155
  ElseIf option == Interface_ConditionMessages_OID ; #DEBUG_LINE_NO:1156
    _Frost_Setting_ConditionMessages.SetValueInt(2) ; #DEBUG_LINE_NO:1157
    Self.SetToggleOptionValue(Interface_ConditionMessages_OID, True, False) ; #DEBUG_LINE_NO:1158
    Self.SaveSettingToCurrentProfile("condition_messages", _Frost_Setting_ConditionMessages.GetValueInt()) ; #DEBUG_LINE_NO:1159
  ElseIf option == Interface_DisplayAttributesInWeathersense_OID ; #DEBUG_LINE_NO:1160
    _Frost_Setting_DisplayAttributesInWeathersense.SetValueInt(1) ; #DEBUG_LINE_NO:1161
    Self.SetToggleOptionValue(Interface_DisplayAttributesInWeathersense_OID, False, False) ; #DEBUG_LINE_NO:1162
    Self.SaveSettingToCurrentProfile("display_attributes_in_weathersense", _Frost_Setting_DisplayAttributesInWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:1163
    Self.ForcePageReset() ; #DEBUG_LINE_NO:1164
  ElseIf option == Interface_DisplayAttributeValuesInWeathersense_OID ; #DEBUG_LINE_NO:1165
    _Frost_Setting_DisplayAttributeValuesInWeathersense.SetValueInt(1) ; #DEBUG_LINE_NO:1166
    Self.SetToggleOptionValue(Interface_DisplayAttributeValuesInWeathersense_OID, False, False) ; #DEBUG_LINE_NO:1167
    Self.SaveSettingToCurrentProfile("display_attribute_values_in_weathersense", _Frost_Setting_DisplayAttributeValuesInWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:1168
  ElseIf option == Interface_Notifications_EquipmentValues_OID ; #DEBUG_LINE_NO:1169
    _Frost_Setting_Notifications_EquipmentValues.SetValueInt(2) ; #DEBUG_LINE_NO:1170
    Self.SetToggleOptionValue(Interface_Notifications_EquipmentValues_OID, True, False) ; #DEBUG_LINE_NO:1171
    Self.SaveSettingToCurrentProfile("notification_equipmentvalues", _Frost_Setting_Notifications_EquipmentValues.GetValueInt()) ; #DEBUG_LINE_NO:1172
  ElseIf option == Interface_Notifications_EquipmentSummary_OID ; #DEBUG_LINE_NO:1173
    _Frost_Setting_Notifications_EquipmentSummary.SetValueInt(2) ; #DEBUG_LINE_NO:1174
    Self.SetToggleOptionValue(Interface_Notifications_EquipmentSummary_OID, True, False) ; #DEBUG_LINE_NO:1175
    Self.SaveSettingToCurrentProfile("notification_equipmentsummary", _Frost_Setting_Notifications_EquipmentSummary.GetValueInt()) ; #DEBUG_LINE_NO:1176
  ElseIf option == Gameplay_ExposurePauseCombat_OID ; #DEBUG_LINE_NO:1177
    _Frost_Setting_ExposurePauseCombat.SetValueInt(2) ; #DEBUG_LINE_NO:1178
    Self.SetToggleOptionValue(Gameplay_ExposurePauseCombat_OID, True, False) ; #DEBUG_LINE_NO:1179
    Self.SaveSettingToCurrentProfile("exposure_pause_combat", _Frost_Setting_ExposurePauseCombat.GetValueInt()) ; #DEBUG_LINE_NO:1180
  ElseIf option == Gameplay_ExposurePauseDialogue_OID ; #DEBUG_LINE_NO:1181
    _Frost_Setting_ExposurePauseDialogue.SetValueInt(2) ; #DEBUG_LINE_NO:1182
    Self.SetToggleOptionValue(Gameplay_ExposurePauseDialogue_OID, True, False) ; #DEBUG_LINE_NO:1183
    Self.SaveSettingToCurrentProfile("exposure_pause_dialogue", _Frost_Setting_ExposurePauseDialogue.GetValueInt()) ; #DEBUG_LINE_NO:1184
  ElseIf option == Interface_ForceFeedback_OID ; #DEBUG_LINE_NO:1185
    _Frost_Setting_ForceFeedback.SetValueInt(2) ; #DEBUG_LINE_NO:1186
    Self.SetToggleOptionValue(Interface_ForceFeedback_OID, True, False) ; #DEBUG_LINE_NO:1187
    Self.SaveSettingToCurrentProfile("force_feedback", _Frost_Setting_ForceFeedback.GetValueInt()) ; #DEBUG_LINE_NO:1188
  ElseIf option == Interface_FrostShaderOn_OID ; #DEBUG_LINE_NO:1189
    _Frost_Setting_FrostShaderOn.SetValueInt(2) ; #DEBUG_LINE_NO:1190
    Self.SetToggleOptionValue(Interface_FrostShaderOn_OID, True, False) ; #DEBUG_LINE_NO:1191
    Self.SaveSettingToCurrentProfile("frost_shader_on", _Frost_Setting_FrostShaderOn.GetValueInt()) ; #DEBUG_LINE_NO:1192
  ElseIf option == Interface_FullScreenEffects_OID ; #DEBUG_LINE_NO:1193
    _Frost_Setting_FullScreenEffects.SetValueInt(2) ; #DEBUG_LINE_NO:1194
    Self.SetToggleOptionValue(Interface_FullScreenEffects_OID, True, False) ; #DEBUG_LINE_NO:1195
    Self.SaveSettingToCurrentProfile("full_screen_effects", _Frost_Setting_FullScreenEffects.GetValueInt()) ; #DEBUG_LINE_NO:1196
  ElseIf option == Gameplay_MovementPenalty_OID ; #DEBUG_LINE_NO:1197
    _Frost_Setting_MovementPenalty.SetValueInt(2) ; #DEBUG_LINE_NO:1198
    Self.SetToggleOptionValue(Gameplay_MovementPenalty_OID, True, False) ; #DEBUG_LINE_NO:1199
    Self.SaveSettingToCurrentProfile("movement_penalty", _Frost_Setting_MovementPenalty.GetValueInt()) ; #DEBUG_LINE_NO:1200
  ElseIf option == Gameplay_DisableFT_OID ; #DEBUG_LINE_NO:1201
    _Frost_Setting_NoFastTravel.SetValueInt(1) ; #DEBUG_LINE_NO:1202
    Self.SetToggleOptionValue(Gameplay_DisableFT_OID, False, False) ; #DEBUG_LINE_NO:1203
    Self.SaveSettingToCurrentProfile("no_fast_travel", _Frost_Setting_NoFastTravel.GetValueInt()) ; #DEBUG_LINE_NO:1204
  ElseIf option == Gameplay_DisableWaiting_OID ; #DEBUG_LINE_NO:1205
    _Frost_Setting_NoWaiting.SetValueInt(1) ; #DEBUG_LINE_NO:1206
    Self.SetToggleOptionValue(Gameplay_DisableWaiting_OID, False, False) ; #DEBUG_LINE_NO:1207
    Self.SaveSettingToCurrentProfile("no_waiting", _Frost_Setting_NoWaiting.GetValueInt()) ; #DEBUG_LINE_NO:1208
  ElseIf option == Interface_WeatherMessages_OID ; #DEBUG_LINE_NO:1209
    _Frost_Setting_WeatherMessages.SetValueInt(2) ; #DEBUG_LINE_NO:1210
    Self.SetToggleOptionValue(Interface_WeatherMessages_OID, True, False) ; #DEBUG_LINE_NO:1211
    Self.SaveSettingToCurrentProfile("weather_messages", _Frost_Setting_WeatherMessages.GetValueInt()) ; #DEBUG_LINE_NO:1212
  ElseIf option == Interface_WeathersenseDisplayMode_OID ; #DEBUG_LINE_NO:1213
    _Frost_Setting_WeathersenseDisplayMode.SetValueInt(2) ; #DEBUG_LINE_NO:1214
    Self.SetMenuOptionValue(Interface_WeathersenseDisplayMode_OID, WeathersenseDisplayList[2], False) ; #DEBUG_LINE_NO:1215
    Self.SaveSettingToCurrentProfileFloat("weathersense_display_mode", 2 as Float) ; #DEBUG_LINE_NO:1216
  ElseIf option == Interface_WetShaderOn_OID ; #DEBUG_LINE_NO:1217
    _Frost_Setting_WetShaderOn.SetValueInt(2) ; #DEBUG_LINE_NO:1218
    Self.SetToggleOptionValue(Interface_WetShaderOn_OID, True, False) ; #DEBUG_LINE_NO:1219
    Self.SaveSettingToCurrentProfile("wet_shader_on", _Frost_Setting_WetShaderOn.GetValueInt()) ; #DEBUG_LINE_NO:1220
  ElseIf option == Gameplay_FrigidWater_OID ; #DEBUG_LINE_NO:1221
    _Frost_Setting_FrigidWaterIsLethal.SetValueInt(2) ; #DEBUG_LINE_NO:1222
    Self.SetToggleOptionValue(Gameplay_FrigidWater_OID, True, False) ; #DEBUG_LINE_NO:1223
    Self.SaveSettingToCurrentProfile("frigid_water_is_lethal", _Frost_Setting_FrigidWaterIsLethal.GetValueInt()) ; #DEBUG_LINE_NO:1224
  ElseIf option == Interface_SoundEffects_OID ; #DEBUG_LINE_NO:1225
    _Frost_Setting_SoundEffects.SetValueInt(2) ; #DEBUG_LINE_NO:1226
    Self.SetToggleOptionValue(Interface_SoundEffects_OID, True, False) ; #DEBUG_LINE_NO:1227
    Self.SaveSettingToCurrentProfile("sound_effects", _Frost_Setting_SoundEffects.GetValueInt()) ; #DEBUG_LINE_NO:1228
  ElseIf option == Gameplay_ExposureRate_OID ; #DEBUG_LINE_NO:1230
    _Frost_Setting_ExposureRate.SetValue(1.0) ; #DEBUG_LINE_NO:1231
    Self.SetSliderOptionValue(Gameplay_ExposureRate_OID, 1.0, "{1}x", False) ; #DEBUG_LINE_NO:1232
    Self.SaveSettingToCurrentProfileFloat("exposure_rate", _Frost_Setting_ExposureRate.GetValue()) ; #DEBUG_LINE_NO:1233
  ElseIf option == Gameplay_MaxExposureMode_OID ; #DEBUG_LINE_NO:1235
    _Frost_Setting_MaxExposureMode.SetValueInt(2) ; #DEBUG_LINE_NO:1236
    Self.SetMenuOptionValue(Gameplay_MaxExposureMode_OID, MaxExposureModeList[1], False) ; #DEBUG_LINE_NO:1237
    Self.SaveSettingToCurrentProfile("max_exposure_mode", _Frost_Setting_MaxExposureMode.GetValueInt()) ; #DEBUG_LINE_NO:1238
  ElseIf option == Gameplay_VampirismMode_OID ; #DEBUG_LINE_NO:1239
    _Frost_Setting_VampireMode.SetValueInt(1) ; #DEBUG_LINE_NO:1240
    Self.SetMenuOptionValue(Gameplay_VampirismMode_OID, VampirismModeList[1], False) ; #DEBUG_LINE_NO:1241
    Self.SaveSettingToCurrentProfile("vampire_mode", _Frost_Setting_VampireMode.GetValueInt()) ; #DEBUG_LINE_NO:1242
  ElseIf option == Gameplay_WeathersenseHotkey_OID ; #DEBUG_LINE_NO:1244
    Self.UnregisterForKey(_Frost_HotkeyWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:1245
    _Frost_HotkeyWeathersense.SetValue(0 as Float) ; #DEBUG_LINE_NO:1246
    Self.ForcePageReset() ; #DEBUG_LINE_NO:1247
    PlayerRef.AddSpell(_Frost_Weathersense_Spell, False) ; #DEBUG_LINE_NO:1248
    Self.SaveSettingToCurrentProfile("hotkey_weathersense", 0) ; #DEBUG_LINE_NO:1249
  ElseIf option == Meters_UIMeterDisplay_OID ; #DEBUG_LINE_NO:1251
    Self.SetMenuOptionValue(Meters_UIMeterDisplay_OID, MeterDisplayModeList[2], False) ; #DEBUG_LINE_NO:1252
    _Frost_Setting_MeterDisplayMode.SetValueInt(2) ; #DEBUG_LINE_NO:1253
    Self.SaveSettingToCurrentProfile("meter_display_mode", 2) ; #DEBUG_LINE_NO:1254
    Self.RemoveAllMeters() ; #DEBUG_LINE_NO:1255
  ElseIf option == Meters_UIMeterDisplayTime_OID ; #DEBUG_LINE_NO:1256
    _Frost_Setting_MeterDisplayTime.SetValueInt(4) ; #DEBUG_LINE_NO:1257
    Self.SetSliderOptionValue(Meters_UIMeterDisplayTime_OID, _Frost_Setting_MeterDisplayTime.GetValueInt() as Float, "{0}", False) ; #DEBUG_LINE_NO:1258
    Self.SaveSettingToCurrentProfile("meter_display_time", 4) ; #DEBUG_LINE_NO:1259
  ElseIf option == Meters_UIMeterColor_OID ; #DEBUG_LINE_NO:1260
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1261
      _Frost_Setting_MeterExposureColor.SetValueInt(9687295) ; #DEBUG_LINE_NO:1262
      Self.SetColorOptionValue(option, _Frost_Setting_MeterExposureColor.GetValueInt(), False) ; #DEBUG_LINE_NO:1263
      If !Self.IsMeterInverted(ExposureMeterHandler as commonmeterinterfacehandler) ; #DEBUG_LINE_NO:1264
        ExposureMeterHandler.SetMeterColors(_Frost_Setting_MeterExposureColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:1265
      EndIf
      Self.SaveSettingToCurrentProfile("exposure_meter_color", _Frost_Setting_MeterExposureColor.GetValueInt()) ; #DEBUG_LINE_NO:1267
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1268
      _Frost_Setting_MeterWetnessColor.SetValueInt(2386420) ; #DEBUG_LINE_NO:1269
      Self.SetColorOptionValue(option, _Frost_Setting_MeterWetnessColor.GetValueInt(), False) ; #DEBUG_LINE_NO:1270
      WetnessMeterHandler.SetMeterColors(_Frost_Setting_MeterWetnessColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:1271
      Self.SaveSettingToCurrentProfile("wetness_meter_color", _Frost_Setting_MeterWetnessColor.GetValueInt()) ; #DEBUG_LINE_NO:1272
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1273
      _Frost_Setting_MeterWeathersenseColor.SetValueInt(16630567) ; #DEBUG_LINE_NO:1274
      Self.SetColorOptionValue(option, _Frost_Setting_MeterWeathersenseColor.GetValueInt(), False) ; #DEBUG_LINE_NO:1275
      WeathersenseMeterHandler.SetMeterColors(_Frost_Setting_MeterWeathersenseColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:1276
      Self.SaveSettingToCurrentProfile("weathersense_meter_color", _Frost_Setting_MeterWeathersenseColor.GetValueInt()) ; #DEBUG_LINE_NO:1277
    EndIf
  ElseIf option == Meters_UIMeterColorAlt_OID ; #DEBUG_LINE_NO:1279
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1280
      _Frost_Setting_MeterExposureColorWarm.SetValueInt(13369344) ; #DEBUG_LINE_NO:1281
      Self.SetColorOptionValue(option, _Frost_Setting_MeterExposureColorWarm.GetValueInt(), False) ; #DEBUG_LINE_NO:1282
      If Self.IsMeterInverted(ExposureMeterHandler as commonmeterinterfacehandler) ; #DEBUG_LINE_NO:1283
        ExposureMeterHandler.SetMeterColors(_Frost_Setting_MeterExposureColorWarm.GetValueInt(), -1) ; #DEBUG_LINE_NO:1284
      EndIf
      Self.SaveSettingToCurrentProfile("exposure_meter_color_warm", _Frost_Setting_MeterExposureColorWarm.GetValueInt()) ; #DEBUG_LINE_NO:1286
    EndIf
  ElseIf option == Meters_UIMeterOpacity_OID ; #DEBUG_LINE_NO:1288
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1289
      _Frost_Setting_MeterExposureOpacity.SetValue(100.0) ; #DEBUG_LINE_NO:1290
      Self.SetSliderOptionValue(Meters_UIMeterOpacity_OID, 100.0, "{0}%", False) ; #DEBUG_LINE_NO:1291
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1292
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_opacity", 100.0) ; #DEBUG_LINE_NO:1293
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1294
      _Frost_Setting_MeterWetnessOpacity.SetValue(100.0) ; #DEBUG_LINE_NO:1295
      Self.SetSliderOptionValue(Meters_UIMeterOpacity_OID, 100.0, "{0}%", False) ; #DEBUG_LINE_NO:1296
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1297
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_opacity", 100.0) ; #DEBUG_LINE_NO:1298
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1299
      _Frost_Setting_MeterWeathersenseOpacity.SetValue(100.0) ; #DEBUG_LINE_NO:1300
      Self.SetSliderOptionValue(Meters_UIMeterOpacity_OID, 100.0, "{0}%", False) ; #DEBUG_LINE_NO:1301
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1302
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_opacity", 100.0) ; #DEBUG_LINE_NO:1303
    EndIf
  ElseIf option == Meters_UIMeterScale_OID ; #DEBUG_LINE_NO:1305
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1306
      _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:1307
      _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:1308
      Self.SetSliderOptionValue(Meters_UIMeterScale_OID, 1.0, "{2}", False) ; #DEBUG_LINE_NO:1309
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1310
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_height", NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:1311
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_width", NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:1312
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1313
      If _Frost_Setting_MeterWetnessHeight.GetValue() > 0 as Float ; #DEBUG_LINE_NO:1314
        _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:1315
      Else
        _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:1317
      EndIf
      _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:1319
      Self.SetSliderOptionValue(Meters_UIMeterScale_OID, 1.0, "{2}", False) ; #DEBUG_LINE_NO:1320
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1321
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_height", CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:1322
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_width", CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:1323
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1324
      If _Frost_Setting_MeterWeathersenseHeight.GetValue() > 0 as Float ; #DEBUG_LINE_NO:1325
        _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:1326
      Else
        _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:1328
      EndIf
      _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:1330
      Self.SetSliderOptionValue(Meters_UIMeterScale_OID, 1.0, "{2}", False) ; #DEBUG_LINE_NO:1331
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1332
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_height", CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:1333
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_width", CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:1334
    EndIf
  ElseIf option == Meters_UIMeterXPos_OID ; #DEBUG_LINE_NO:1336
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1337
      _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:1338
      Self.SetSliderOptionValue(Meters_UIMeterXPos_OID, EXPOSURE_METER_TOPRIGHT_16_9_X, "{1}", False) ; #DEBUG_LINE_NO:1339
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1340
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_xpos", EXPOSURE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:1341
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1342
      _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:1343
      Self.SetSliderOptionValue(Meters_UIMeterXPos_OID, WETNESS_METER_TOPRIGHT_16_9_X, "{1}", False) ; #DEBUG_LINE_NO:1344
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1345
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_xpos", WETNESS_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:1346
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1347
      _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:1348
      Self.SetSliderOptionValue(Meters_UIMeterXPos_OID, WEATHERSENSE_METER_TOPRIGHT_16_9_X, "{1}", False) ; #DEBUG_LINE_NO:1349
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1350
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_xpos", WEATHERSENSE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:1351
    EndIf
  ElseIf option == Meters_UIMeterYPos_OID ; #DEBUG_LINE_NO:1353
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1354
      _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:1355
      Self.SetSliderOptionValue(Meters_UIMeterYPos_OID, EXPOSURE_METER_TOPRIGHT_16_9_Y, "{1}", False) ; #DEBUG_LINE_NO:1356
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1357
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_ypos", EXPOSURE_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1358
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1359
      _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1360
      Self.SetSliderOptionValue(Meters_UIMeterYPos_OID, WETNESS_METER_TOPRIGHT_16_9_Y, "{1}", False) ; #DEBUG_LINE_NO:1361
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1362
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_ypos", WETNESS_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1363
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1364
      _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1365
      Self.SetSliderOptionValue(Meters_UIMeterYPos_OID, WEATHERSENSE_METER_TOPRIGHT_16_9_Y, "{1}", False) ; #DEBUG_LINE_NO:1366
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1367
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_ypos", WEATHERSENSE_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1368
    EndIf
  EndIf
EndFunction

Function OnOptionHighlight(Int option)
  If option == Overview_RunStatusText_OID ; #DEBUG_LINE_NO:1374
    Self.SetInfoText("$FrostfallOptionHighlightRunStatus") ; #DEBUG_LINE_NO:1375
  ElseIf option == Overview_ExposureStatusText_OID ; #DEBUG_LINE_NO:1376
    Self.SetInfoText("$FrostfallOptionHighlightStatExposure") ; #DEBUG_LINE_NO:1377
  ElseIf option == Overview_WetnessStatusText_OID ; #DEBUG_LINE_NO:1378
    Self.SetInfoText("$FrostfallOptionHighlightStatWetness") ; #DEBUG_LINE_NO:1379
  ElseIf option == Overview_WarmthStatusText_OID ; #DEBUG_LINE_NO:1380
    Self.SetInfoText("$FrostfallOptionHighlightStatWarmth") ; #DEBUG_LINE_NO:1381
  ElseIf option == Overview_CoverageStatusText_OID ; #DEBUG_LINE_NO:1382
    Self.SetInfoText("$FrostfallOptionHighlightStatCoverage") ; #DEBUG_LINE_NO:1383
  ElseIf option == Gameplay_ExposureRate_OID ; #DEBUG_LINE_NO:1384
    Self.SetInfoText("$FrostfallOptionHighlightSettingExposureRateSlider") ; #DEBUG_LINE_NO:1385
  ElseIf option == Gameplay_MaxExposureMode_OID ; #DEBUG_LINE_NO:1386
    Self.SetInfoText("$FrostfallOptionHighlightSettingMaxExposure") ; #DEBUG_LINE_NO:1387
  ElseIf option == Gameplay_FrigidWater_OID ; #DEBUG_LINE_NO:1388
    Self.SetInfoText("$FrostfallOptionHighlightSettingExposureWaterText") ; #DEBUG_LINE_NO:1389
  ElseIf option == Gameplay_ExposurePauseDialogue_OID ; #DEBUG_LINE_NO:1390
    Self.SetInfoText("$FrostfallOptionHighlightSettingExposureDialogueText") ; #DEBUG_LINE_NO:1391
  ElseIf option == Gameplay_ExposurePauseCombat_OID ; #DEBUG_LINE_NO:1392
    Self.SetInfoText("$FrostfallOptionHighlightSettingExposureCombatText") ; #DEBUG_LINE_NO:1393
  ElseIf option == Gameplay_MovementPenalty_OID ; #DEBUG_LINE_NO:1394
    Self.SetInfoText("$FrostfallOptionHighlightSettingMovementText") ; #DEBUG_LINE_NO:1395
  ElseIf option == Gameplay_VampirismMode_OID ; #DEBUG_LINE_NO:1396
    Self.SetInfoText("$FrostfallOptionHighlightSettingVampirism") ; #DEBUG_LINE_NO:1397
  ElseIf option == Interface_WeathersenseDisplayMode_OID ; #DEBUG_LINE_NO:1398
    Self.SetInfoText("$FrostfallInterfaceSettingWeathersenseDisplayModeHighlight") ; #DEBUG_LINE_NO:1399
  ElseIf option == Gameplay_DisableFT_OID ; #DEBUG_LINE_NO:1400
    Self.SetInfoText("$FrostfallOptionHighlightSettingFTToggleText") ; #DEBUG_LINE_NO:1401
  ElseIf option == Gameplay_DisableWaiting_OID ; #DEBUG_LINE_NO:1402
    Self.SetInfoText("$FrostfallOptionHighlightSettingWaitToggleText") ; #DEBUG_LINE_NO:1403
  ElseIf option == Gameplay_WeathersenseHotkey_OID ; #DEBUG_LINE_NO:1404
    Self.SetInfoText("$FrostfallOptionHighlightHKWeathersense") ; #DEBUG_LINE_NO:1405
  ElseIf option == SaveLoad_SelectProfile_OID ; #DEBUG_LINE_NO:1406
    Self.SetInfoText("$FrostfallOptionHighlightSettingSelectProfile") ; #DEBUG_LINE_NO:1407
  ElseIf option == SaveLoad_RenameProfile_OID ; #DEBUG_LINE_NO:1408
    Self.SetInfoText("$FrostfallOptionHighlightSettingRenameProfile") ; #DEBUG_LINE_NO:1409
  ElseIf option == SaveLoad_DefaultProfile_OID ; #DEBUG_LINE_NO:1410
    Self.SetInfoText("$FrostfallOptionHighlightSettingDefaultProfile") ; #DEBUG_LINE_NO:1411
  ElseIf option == SaveLoad_Enable_OID ; #DEBUG_LINE_NO:1412
    Self.SetInfoText("$FrostfallOptionHighlightSettingEnableSaveLoad") ; #DEBUG_LINE_NO:1413
  ElseIf option == Interface_FrostShaderOn_OID ; #DEBUG_LINE_NO:1414
    Self.SetInfoText("$FrostfallOptionHighlightSettingFrostShaderToggle") ; #DEBUG_LINE_NO:1415
  ElseIf option == Interface_WetShaderOn_OID ; #DEBUG_LINE_NO:1416
    Self.SetInfoText("$FrostfallOptionHighlightSettingWetShaderToggle") ; #DEBUG_LINE_NO:1417
  ElseIf option == Interface_SoundEffects_OID ; #DEBUG_LINE_NO:1418
    Self.SetInfoText("$FrostfallOptionHighlightSoundEffects") ; #DEBUG_LINE_NO:1419
  ElseIf option == Interface_FullScreenEffects_OID ; #DEBUG_LINE_NO:1420
    Self.SetInfoText("$FrostfallOptionHighlightSettingFullScreenEffectsToggle") ; #DEBUG_LINE_NO:1421
  ElseIf option == Interface_ForceFeedback_OID ; #DEBUG_LINE_NO:1422
    Self.SetInfoText("$FrostfallOptionHighlightForceFeedback") ; #DEBUG_LINE_NO:1423
  ElseIf option == Interface_Animation_OID ; #DEBUG_LINE_NO:1424
    Self.SetInfoText("$FrostfallOptionHighlightAnimation") ; #DEBUG_LINE_NO:1425
  ElseIf option == Interface_FollowerAnimation_OID ; #DEBUG_LINE_NO:1426
    Self.SetInfoText("$FrostfallOptionHighlightFollowerAnimation") ; #DEBUG_LINE_NO:1427
  ElseIf option == Interface_ConditionMessages_OID ; #DEBUG_LINE_NO:1428
    Self.SetInfoText("$FrostfallOptionHighlightSettingConditionMsgToggle") ; #DEBUG_LINE_NO:1429
  ElseIf option == Interface_WeatherMessages_OID ; #DEBUG_LINE_NO:1430
    Self.SetInfoText("$FrostfallOptionHighlightSettingWeatherMsgToggle") ; #DEBUG_LINE_NO:1431
  ElseIf option == Interface_DisplayAttributesInWeathersense_OID ; #DEBUG_LINE_NO:1432
    Self.SetInfoText("$FrostfallOptionHighlightSettingExpValueMsgToggle") ; #DEBUG_LINE_NO:1433
  ElseIf option == Interface_DisplayAttributeValuesInWeathersense_OID ; #DEBUG_LINE_NO:1434
    Self.SetInfoText("$FrostfallOptionHighlightSettingExpValueMsgDetailToggle") ; #DEBUG_LINE_NO:1435
  ElseIf option == Interface_Notifications_EquipmentValues_OID ; #DEBUG_LINE_NO:1436
    Self.SetInfoText("$FrostfallOptionHighlightSettingEquipValuesMsgToggle") ; #DEBUG_LINE_NO:1437
  ElseIf option == Interface_Notifications_EquipmentSummary_OID ; #DEBUG_LINE_NO:1438
    Self.SetInfoText("$FrostfallOptionHighlightSettingEquipSummaryMsgToggle") ; #DEBUG_LINE_NO:1439
  ElseIf option == Advanced_EnduranceSkillRespec_OID ; #DEBUG_LINE_NO:1440
    Self.SetInfoText("$FrostfallOptionHighlightSettingRespec") ; #DEBUG_LINE_NO:1441
  ElseIf option == Advanced_EnduranceSkillRestore_OID ; #DEBUG_LINE_NO:1442
    Self.SetInfoText("$FrostfallOptionHighlightSettingRestore") ; #DEBUG_LINE_NO:1443
  ElseIf option == Armor_RepairDefaultsOID ; #DEBUG_LINE_NO:1444
    Self.SetInfoText("$FrostfallOptionHighlightArmorRepairDefaults") ; #DEBUG_LINE_NO:1445
  ElseIf option == Armor_DefaultWornArmorOID ; #DEBUG_LINE_NO:1446
    Self.SetInfoText("$FrostfallOptionHighlightArmorDefaultWornArmor") ; #DEBUG_LINE_NO:1447
  ElseIf option == Armor_DefaultAllArmorOID ; #DEBUG_LINE_NO:1448
    Self.SetInfoText("$FrostfallOptionHighlightArmorDefaultAllArmor") ; #DEBUG_LINE_NO:1449
  ElseIf option == Armor_ShowTutorialOID ; #DEBUG_LINE_NO:1450
    Self.SetInfoText("$FrostfallOptionHighlightArmorShowTutorial") ; #DEBUG_LINE_NO:1451
  ElseIf option == Meters_UIMeterDisplay_OID ; #DEBUG_LINE_NO:1452
    Self.SetInfoText("$FrostfallOptionHightlightUIMeterDisplay") ; #DEBUG_LINE_NO:1453
  ElseIf option == Meters_UIMeterLayout_OID ; #DEBUG_LINE_NO:1454
    Self.SetInfoText("$FrostfallMeterLayoutHighlight") ; #DEBUG_LINE_NO:1455
  ElseIf option == Meters_UIMeterOpacity_OID ; #DEBUG_LINE_NO:1456
    Self.SetInfoText("$FrostfallMeterOpacityHighlight") ; #DEBUG_LINE_NO:1457
  ElseIf option == Meters_UIMeterDisplayTime_OID ; #DEBUG_LINE_NO:1458
    Self.SetInfoText("$FrostfallOptionHightlightUIMeterDisplayTime") ; #DEBUG_LINE_NO:1459
  ElseIf option == Meters_UIMeterFillDirection_OID ; #DEBUG_LINE_NO:1460
    Self.SetInfoText("$FrostfallMeterFillDirectionHighlight") ; #DEBUG_LINE_NO:1461
  ElseIf option == Meters_UIMeterScale_OID ; #DEBUG_LINE_NO:1462
    Self.SetInfoText("$FrostfallMeterScaleHighlight") ; #DEBUG_LINE_NO:1463
  ElseIf option == Meters_UIMeterFlipped_OID ; #DEBUG_LINE_NO:1464
    Self.SetInfoText("$FrostfallMeterFlippedHighlight") ; #DEBUG_LINE_NO:1465
  ElseIf option == Meters_UIMeterColor_OID || option == Meters_UIMeterColorAlt_OID ; #DEBUG_LINE_NO:1466
    Self.SetInfoText("$FrostfallMeterColorHighlight") ; #DEBUG_LINE_NO:1467
  ElseIf option == Meters_UIMeterXPos_OID ; #DEBUG_LINE_NO:1468
    Self.SetInfoText("$FrostfallMeterXPosHighlight") ; #DEBUG_LINE_NO:1469
  ElseIf option == Meters_UIMeterYPos_OID ; #DEBUG_LINE_NO:1470
    Self.SetInfoText("$FrostfallMeterYPosHighlight") ; #DEBUG_LINE_NO:1471
  ElseIf option == Meters_UIMeterHAnchor_OID ; #DEBUG_LINE_NO:1472
    Self.SetInfoText("$FrostfallMeterHAnchorHighlight") ; #DEBUG_LINE_NO:1473
  ElseIf option == Meters_UIMeterVAnchor_OID ; #DEBUG_LINE_NO:1474
    Self.SetInfoText("$FrostfallMeterVAnchorHighlight") ; #DEBUG_LINE_NO:1475
  Else
    Bool found_armor_entry_oid = False ; #DEBUG_LINE_NO:1477
    Int idx = -1 ; #DEBUG_LINE_NO:1478
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1480
      idx = Armor_WarmthSliderOIDs.find(option, 0) ; #DEBUG_LINE_NO:1481
      If idx != -1 ; #DEBUG_LINE_NO:1482
        Self.SetInfoText("$FrostfallOptionHighlightArmorWarmthSlider") ; #DEBUG_LINE_NO:1483
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1484
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1488
      idx = Armor_CoverageSliderOIDs.find(option, 0) ; #DEBUG_LINE_NO:1489
      If idx != -1 ; #DEBUG_LINE_NO:1490
        Self.SetInfoText("$FrostfallOptionHighlightArmorCoverageSlider") ; #DEBUG_LINE_NO:1491
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1492
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1496
      idx = Armor_GearTypeOIDs.find(option, 0) ; #DEBUG_LINE_NO:1497
      If idx != -1 ; #DEBUG_LINE_NO:1498
        Self.SetInfoText("$FrostfallOptionHighlightArmorTypeMenu") ; #DEBUG_LINE_NO:1499
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1500
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1504
      idx = Armor_SetProtectionOIDs.find(option, 0) ; #DEBUG_LINE_NO:1505
      If idx != -1 ; #DEBUG_LINE_NO:1506
        Self.SetInfoText("$FrostfallOptionHighlightArmorEditProtectionMenu") ; #DEBUG_LINE_NO:1507
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1508
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1512
      idx = Armor_ModifyPartsOIDs.find(option, 0) ; #DEBUG_LINE_NO:1513
      If idx != -1 ; #DEBUG_LINE_NO:1514
        Self.SetInfoText("$FrostfallOptionHighlightArmorExtraPartsMenu") ; #DEBUG_LINE_NO:1515
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1516
      EndIf
    EndIf
  EndIf
EndFunction

Function OnOptionSliderOpen(Int option)
  If option == Gameplay_ExposureRate_OID ; #DEBUG_LINE_NO:1523
    Self.SetSliderDialogStartValue(_Frost_Setting_ExposureRate.GetValue()) ; #DEBUG_LINE_NO:1524
    Self.SetSliderDialogDefaultValue(1.0) ; #DEBUG_LINE_NO:1525
    Self.SetSliderDialogRange(0.0, 3.0) ; #DEBUG_LINE_NO:1526
    Self.SetSliderDialogInterval(0.100000001) ; #DEBUG_LINE_NO:1527
  ElseIf option == Advanced_EnduranceSkillRestoreSlider_OID ; #DEBUG_LINE_NO:1528
    Self.SetSliderDialogStartValue(0.0) ; #DEBUG_LINE_NO:1529
    Self.SetSliderDialogDefaultValue(0.0) ; #DEBUG_LINE_NO:1530
    Self.SetSliderDialogRange(0 as Float, EndurancePerkPointsTotal.GetValue()) ; #DEBUG_LINE_NO:1531
    Self.SetSliderDialogInterval(1.0) ; #DEBUG_LINE_NO:1532
  ElseIf option == Meters_UIMeterDisplayTime_OID ; #DEBUG_LINE_NO:1533
    Self.SetSliderDialogStartValue((_Frost_Setting_MeterDisplayTime.GetValueInt() * 2) as Float) ; #DEBUG_LINE_NO:1534
    Self.SetSliderDialogDefaultValue(8.0) ; #DEBUG_LINE_NO:1535
    Self.SetSliderDialogRange(4.0, 20.0) ; #DEBUG_LINE_NO:1536
    Self.SetSliderDialogInterval(2.0) ; #DEBUG_LINE_NO:1537
  ElseIf option == Meters_UIMeterOpacity_OID ; #DEBUG_LINE_NO:1538
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1539
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterExposureOpacity.GetValue()) ; #DEBUG_LINE_NO:1540
      Self.SetSliderDialogDefaultValue(100.0) ; #DEBUG_LINE_NO:1541
      Self.SetSliderDialogRange(0.0, 100.0) ; #DEBUG_LINE_NO:1542
      Self.SetSliderDialogInterval(1.0) ; #DEBUG_LINE_NO:1543
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1544
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterWetnessOpacity.GetValue()) ; #DEBUG_LINE_NO:1545
      Self.SetSliderDialogDefaultValue(100.0) ; #DEBUG_LINE_NO:1546
      Self.SetSliderDialogRange(0.0, 100.0) ; #DEBUG_LINE_NO:1547
      Self.SetSliderDialogInterval(1.0) ; #DEBUG_LINE_NO:1548
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1549
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterWeathersenseOpacity.GetValue()) ; #DEBUG_LINE_NO:1550
      Self.SetSliderDialogDefaultValue(100.0) ; #DEBUG_LINE_NO:1551
      Self.SetSliderDialogRange(0.0, 100.0) ; #DEBUG_LINE_NO:1552
      Self.SetSliderDialogInterval(1.0) ; #DEBUG_LINE_NO:1553
    EndIf
  ElseIf option == Meters_UIMeterScale_OID ; #DEBUG_LINE_NO:1555
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1556
      Self.SetSliderDialogStartValue(Self.GetMeterScale(_Frost_Setting_MeterExposureWidth.GetValue(), NORMAL_METER_WIDTH)) ; #DEBUG_LINE_NO:1557
      Self.SetSliderDialogDefaultValue(1.0) ; #DEBUG_LINE_NO:1558
      Self.SetSliderDialogRange(0.0, 1.0) ; #DEBUG_LINE_NO:1559
      Self.SetSliderDialogInterval(0.050000001) ; #DEBUG_LINE_NO:1560
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1561
      Self.SetSliderDialogStartValue(Self.GetMeterScale(_Frost_Setting_MeterWetnessWidth.GetValue(), CHARGE_METER_WIDTH)) ; #DEBUG_LINE_NO:1562
      Self.SetSliderDialogDefaultValue(1.0) ; #DEBUG_LINE_NO:1563
      Self.SetSliderDialogRange(0.0, 1.0) ; #DEBUG_LINE_NO:1564
      Self.SetSliderDialogInterval(0.050000001) ; #DEBUG_LINE_NO:1565
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1566
      Self.SetSliderDialogStartValue(Self.GetMeterScale(_Frost_Setting_MeterWeathersenseWidth.GetValue(), CHARGE_METER_WIDTH)) ; #DEBUG_LINE_NO:1567
      Self.SetSliderDialogDefaultValue(1.0) ; #DEBUG_LINE_NO:1568
      Self.SetSliderDialogRange(0.0, 1.0) ; #DEBUG_LINE_NO:1569
      Self.SetSliderDialogInterval(0.050000001) ; #DEBUG_LINE_NO:1570
    EndIf
  ElseIf option == Meters_UIMeterXPos_OID ; #DEBUG_LINE_NO:1572
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1573
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterExposureXPos.GetValue()) ; #DEBUG_LINE_NO:1574
      Self.SetSliderDialogDefaultValue(EXPOSURE_METER_BOTTOMRIGHT_16_9_X) ; #DEBUG_LINE_NO:1575
      Self.SetSliderDialogRange(0.0, 1280.0) ; #DEBUG_LINE_NO:1576
      Self.SetSliderDialogInterval(0.100000001) ; #DEBUG_LINE_NO:1577
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1578
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterWetnessXPos.GetValue()) ; #DEBUG_LINE_NO:1579
      Self.SetSliderDialogDefaultValue(WETNESS_METER_BOTTOMRIGHT_16_9_X) ; #DEBUG_LINE_NO:1580
      Self.SetSliderDialogRange(0.0, 1800.0) ; #DEBUG_LINE_NO:1581
      Self.SetSliderDialogInterval(0.100000001) ; #DEBUG_LINE_NO:1582
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1583
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterWeathersenseXPos.GetValue()) ; #DEBUG_LINE_NO:1584
      Self.SetSliderDialogDefaultValue(WEATHERSENSE_METER_BOTTOMRIGHT_16_9_X) ; #DEBUG_LINE_NO:1585
      Self.SetSliderDialogRange(0.0, 1800.0) ; #DEBUG_LINE_NO:1586
      Self.SetSliderDialogInterval(0.100000001) ; #DEBUG_LINE_NO:1587
    EndIf
  ElseIf option == Meters_UIMeterYPos_OID ; #DEBUG_LINE_NO:1589
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1590
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterExposureYPos.GetValue()) ; #DEBUG_LINE_NO:1591
      Self.SetSliderDialogDefaultValue(EXPOSURE_METER_BOTTOMRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1592
      Self.SetSliderDialogRange(0.0, 720.0) ; #DEBUG_LINE_NO:1593
      Self.SetSliderDialogInterval(0.100000001) ; #DEBUG_LINE_NO:1594
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1595
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterWetnessYPos.GetValue()) ; #DEBUG_LINE_NO:1596
      Self.SetSliderDialogDefaultValue(WETNESS_METER_BOTTOMRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1597
      Self.SetSliderDialogRange(0.0, 726.5) ; #DEBUG_LINE_NO:1598
      Self.SetSliderDialogInterval(0.100000001) ; #DEBUG_LINE_NO:1599
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1600
      Self.SetSliderDialogStartValue(_Frost_Setting_MeterWeathersenseYPos.GetValue()) ; #DEBUG_LINE_NO:1601
      Self.SetSliderDialogDefaultValue(WEATHERSENSE_METER_BOTTOMRIGHT_16_9_Y) ; #DEBUG_LINE_NO:1602
      Self.SetSliderDialogRange(0.0, 726.5) ; #DEBUG_LINE_NO:1603
      Self.SetSliderDialogInterval(0.100000001) ; #DEBUG_LINE_NO:1604
    EndIf
  Else
    Bool found_armor_entry_oid = False ; #DEBUG_LINE_NO:1607
    Int idx = -1 ; #DEBUG_LINE_NO:1608
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1610
      idx = Armor_WarmthSliderOIDs.find(option, 0) ; #DEBUG_LINE_NO:1611
      If idx != -1 ; #DEBUG_LINE_NO:1612
        Self.SetWarmthSlider(idx) ; #DEBUG_LINE_NO:1613
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1614
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1618
      idx = Armor_CoverageSliderOIDs.find(option, 0) ; #DEBUG_LINE_NO:1619
      If idx != -1 ; #DEBUG_LINE_NO:1620
        Self.SetCoverageSlider(idx) ; #DEBUG_LINE_NO:1621
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1622
      EndIf
    EndIf
  EndIf
EndFunction

Function OnOptionSliderAccept(Int option, Float value)
  If option == Gameplay_ExposureRate_OID ; #DEBUG_LINE_NO:1630
    _Frost_Setting_ExposureRate.SetValue(value) ; #DEBUG_LINE_NO:1631
    Self.SetSliderOptionValue(Gameplay_ExposureRate_OID, value, "{1}x", False) ; #DEBUG_LINE_NO:1632
    Self.SaveSettingToCurrentProfileFloat("exposure_rate", _Frost_Setting_ExposureRate.GetValue()) ; #DEBUG_LINE_NO:1633
  ElseIf option == Advanced_EnduranceSkillRestoreSlider_OID ; #DEBUG_LINE_NO:1634
    EndurancePerkPointProgress.SetValue(0.0) ; #DEBUG_LINE_NO:1635
    EndurancePerkPoints.SetValue(value) ; #DEBUG_LINE_NO:1636
    EndurancePerkPointsEarned.SetValue(value) ; #DEBUG_LINE_NO:1637
    Self.ClearEndurancePerks() ; #DEBUG_LINE_NO:1638
    Self.ShowMessage("$FrostfallAdvancedEnduranceSkillRestoreDone", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1639
    Self.SetOptionFlags(Advanced_EnduranceSkillRestoreSlider_OID, Self.OPTION_FLAG_DISABLED, True) ; #DEBUG_LINE_NO:1640
    Self.SetToggleOptionValue(Advanced_EnduranceSkillRestore_OID, False, False) ; #DEBUG_LINE_NO:1641
  ElseIf option == Meters_UIMeterDisplayTime_OID ; #DEBUG_LINE_NO:1642
    _Frost_Setting_MeterDisplayTime.SetValue(value / 2 as Float) ; #DEBUG_LINE_NO:1643
    Self.SetSliderOptionValue(Meters_UIMeterDisplayTime_OID, value, "{0}", False) ; #DEBUG_LINE_NO:1644
    Self.SaveSettingToCurrentProfile("meter_display_time", _Frost_Setting_MeterDisplayTime.GetValueInt()) ; #DEBUG_LINE_NO:1645
  ElseIf option == Meters_UIMeterOpacity_OID ; #DEBUG_LINE_NO:1646
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1647
      _Frost_Setting_MeterExposureOpacity.SetValue(value) ; #DEBUG_LINE_NO:1648
      Self.SetSliderOptionValue(Meters_UIMeterOpacity_OID, value, "{0}%", False) ; #DEBUG_LINE_NO:1649
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1650
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_opacity", value) ; #DEBUG_LINE_NO:1651
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1652
      _Frost_Setting_MeterWetnessOpacity.SetValue(value) ; #DEBUG_LINE_NO:1653
      Self.SetSliderOptionValue(Meters_UIMeterOpacity_OID, value, "{0}%", False) ; #DEBUG_LINE_NO:1654
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1655
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_opacity", value) ; #DEBUG_LINE_NO:1656
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1657
      _Frost_Setting_MeterWeathersenseOpacity.SetValue(value) ; #DEBUG_LINE_NO:1658
      Self.SetSliderOptionValue(Meters_UIMeterOpacity_OID, value, "{0}%", False) ; #DEBUG_LINE_NO:1659
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1660
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_opacity", value) ; #DEBUG_LINE_NO:1661
    EndIf
  ElseIf option == Meters_UIMeterScale_OID ; #DEBUG_LINE_NO:1663
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1664
      _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT * value) ; #DEBUG_LINE_NO:1665
      _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH * value) ; #DEBUG_LINE_NO:1666
      Self.SetSliderOptionValue(Meters_UIMeterScale_OID, value, "{2}", False) ; #DEBUG_LINE_NO:1667
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1668
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_height", _Frost_Setting_MeterExposureHeight.GetValue()) ; #DEBUG_LINE_NO:1669
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_width", _Frost_Setting_MeterExposureWidth.GetValue()) ; #DEBUG_LINE_NO:1670
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1671
      If _Frost_Setting_MeterWetnessHeight.GetValue() > 0 as Float ; #DEBUG_LINE_NO:1672
        _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT * value) ; #DEBUG_LINE_NO:1673
      Else
        _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV * value) ; #DEBUG_LINE_NO:1675
      EndIf
      _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH * value) ; #DEBUG_LINE_NO:1677
      Self.SetSliderOptionValue(Meters_UIMeterScale_OID, value, "{2}", False) ; #DEBUG_LINE_NO:1678
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1679
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_height", _Frost_Setting_MeterWetnessHeight.GetValue()) ; #DEBUG_LINE_NO:1680
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_width", _Frost_Setting_MeterWetnessWidth.GetValue()) ; #DEBUG_LINE_NO:1681
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1682
      If _Frost_Setting_MeterWeathersenseHeight.GetValue() > 0 as Float ; #DEBUG_LINE_NO:1683
        _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT * value) ; #DEBUG_LINE_NO:1684
      Else
        _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV * value) ; #DEBUG_LINE_NO:1686
      EndIf
      _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH * value) ; #DEBUG_LINE_NO:1688
      Self.SetSliderOptionValue(Meters_UIMeterScale_OID, value, "{2}", False) ; #DEBUG_LINE_NO:1689
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1690
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_height", _Frost_Setting_MeterWeathersenseHeight.GetValue()) ; #DEBUG_LINE_NO:1691
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_width", _Frost_Setting_MeterWeathersenseWidth.GetValue()) ; #DEBUG_LINE_NO:1692
    EndIf
  ElseIf option == Meters_UIMeterXPos_OID ; #DEBUG_LINE_NO:1694
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1695
      _Frost_Setting_MeterExposureXPos.SetValue(value) ; #DEBUG_LINE_NO:1696
      Self.SetSliderOptionValue(Meters_UIMeterXPos_OID, value, "{1}", False) ; #DEBUG_LINE_NO:1697
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1698
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_xpos", value) ; #DEBUG_LINE_NO:1699
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1700
      _Frost_Setting_MeterWetnessXPos.SetValue(value) ; #DEBUG_LINE_NO:1701
      Self.SetSliderOptionValue(Meters_UIMeterXPos_OID, value, "{1}", False) ; #DEBUG_LINE_NO:1702
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1703
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_xpos", value) ; #DEBUG_LINE_NO:1704
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1705
      _Frost_Setting_MeterWeathersenseXPos.SetValue(value) ; #DEBUG_LINE_NO:1706
      Self.SetSliderOptionValue(Meters_UIMeterXPos_OID, value, "{1}", False) ; #DEBUG_LINE_NO:1707
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1708
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_xpos", value) ; #DEBUG_LINE_NO:1709
    EndIf
  ElseIf option == Meters_UIMeterYPos_OID ; #DEBUG_LINE_NO:1711
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1712
      _Frost_Setting_MeterExposureYPos.SetValue(value) ; #DEBUG_LINE_NO:1713
      Self.SetSliderOptionValue(Meters_UIMeterYPos_OID, value, "{1}", False) ; #DEBUG_LINE_NO:1714
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1715
      Self.SaveSettingToCurrentProfileFloat("exposure_meter_ypos", value) ; #DEBUG_LINE_NO:1716
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1717
      _Frost_Setting_MeterWetnessYPos.SetValue(value) ; #DEBUG_LINE_NO:1718
      Self.SetSliderOptionValue(Meters_UIMeterYPos_OID, value, "{1}", False) ; #DEBUG_LINE_NO:1719
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1720
      Self.SaveSettingToCurrentProfileFloat("wetness_meter_ypos", value) ; #DEBUG_LINE_NO:1721
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1722
      _Frost_Setting_MeterWeathersenseYPos.SetValue(value) ; #DEBUG_LINE_NO:1723
      Self.SetSliderOptionValue(Meters_UIMeterYPos_OID, value, "{1}", False) ; #DEBUG_LINE_NO:1724
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1725
      Self.SaveSettingToCurrentProfileFloat("weathersense_meter_ypos", value) ; #DEBUG_LINE_NO:1726
    EndIf
  Else
    Bool found_armor_entry_oid = False ; #DEBUG_LINE_NO:1729
    Int idx = -1 ; #DEBUG_LINE_NO:1730
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1732
      idx = Armor_WarmthSliderOIDs.find(option, 0) ; #DEBUG_LINE_NO:1733
      If idx != -1 ; #DEBUG_LINE_NO:1734
        Self.ModifyGearWarmth(idx, value as Int) ; #DEBUG_LINE_NO:1735
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1736
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1740
      idx = Armor_CoverageSliderOIDs.find(option, 0) ; #DEBUG_LINE_NO:1741
      If idx != -1 ; #DEBUG_LINE_NO:1742
        Self.ModifyGearCoverage(idx, value as Int) ; #DEBUG_LINE_NO:1743
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1744
      EndIf
    EndIf
  EndIf
EndFunction

Function OnOptionMenuOpen(Int option)
  If !config_is_open
    Return
  EndIf
  If option == Gameplay_MaxExposureMode_OID ; #DEBUG_LINE_NO:1751
    Self.SetMenuDialogOptions(MaxExposureModeList) ; #DEBUG_LINE_NO:1752
    Self.SetMenuDialogStartIndex(_Frost_Setting_MaxExposureMode.GetValueInt() - 1) ; #DEBUG_LINE_NO:1753
    Self.SetMenuDialogDefaultIndex(0) ; #DEBUG_LINE_NO:1754
  ElseIf option == Gameplay_VampirismMode_OID ; #DEBUG_LINE_NO:1755
    Self.SetMenuDialogOptions(VampirismModeList) ; #DEBUG_LINE_NO:1756
    Self.SetMenuDialogStartIndex(_Frost_Setting_VampireMode.GetValueInt()) ; #DEBUG_LINE_NO:1757
    Self.SetMenuDialogDefaultIndex(0) ; #DEBUG_LINE_NO:1758
  ElseIf option == Interface_WeathersenseDisplayMode_OID ; #DEBUG_LINE_NO:1759
    Self.SetMenuDialogOptions(WeathersenseDisplayList) ; #DEBUG_LINE_NO:1760
    Self.SetMenuDialogStartIndex(_Frost_Setting_WeathersenseDisplayMode.GetValueInt()) ; #DEBUG_LINE_NO:1761
    Self.SetMenuDialogDefaultIndex(2) ; #DEBUG_LINE_NO:1762
  ElseIf option == Interface_Animation_OID ; #DEBUG_LINE_NO:1763
    Self.SetMenuDialogOptions(AnimationList) ; #DEBUG_LINE_NO:1764
    Self.SetMenuDialogStartIndex(_Frost_Setting_Animation.GetValueInt() - 1) ; #DEBUG_LINE_NO:1765
    Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1766
  ElseIf option == SaveLoad_SelectProfile_OID ; #DEBUG_LINE_NO:1767
    String[] profile_list = new String[10] ; #DEBUG_LINE_NO:1768
    Int i = 0 ; #DEBUG_LINE_NO:1769
    While i < 10 ; #DEBUG_LINE_NO:1770
      String pname = Self.GetProfileName(i + 1) ; #DEBUG_LINE_NO:1771
      profile_list[i] = pname ; #DEBUG_LINE_NO:1772
      i += 1 ; #DEBUG_LINE_NO:1773
    EndWhile
    Self.SetMenuDialogOptions(profile_list) ; #DEBUG_LINE_NO:1775
    Self.SetMenuDialogStartIndex(_Frost_Setting_CurrentProfile.GetValueInt() - 1) ; #DEBUG_LINE_NO:1776
    Self.SetMenuDialogDefaultIndex(0) ; #DEBUG_LINE_NO:1777
  ElseIf option == Meters_UIMeterDisplay_OID ; #DEBUG_LINE_NO:1778
    Self.SetMenuDialogOptions(MeterDisplayModeList) ; #DEBUG_LINE_NO:1779
    Self.SetMenuDialogStartIndex(_Frost_Setting_MeterDisplayMode.GetValueInt()) ; #DEBUG_LINE_NO:1780
    Self.SetMenuDialogDefaultIndex(0) ; #DEBUG_LINE_NO:1781
  ElseIf option == Meters_UIMeterLayout_OID ; #DEBUG_LINE_NO:1782
    Self.SetMenuDialogOptions(MeterLayoutList) ; #DEBUG_LINE_NO:1783
    Self.SetMenuDialogStartIndex(0) ; #DEBUG_LINE_NO:1784
    Self.SetMenuDialogDefaultIndex(0) ; #DEBUG_LINE_NO:1785
  ElseIf option == Meters_UIMeterFillDirection_OID ; #DEBUG_LINE_NO:1786
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1787
      Self.SetMenuDialogOptions(FillDirectionListLimited) ; #DEBUG_LINE_NO:1788
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterExposureFillDirection.GetValueInt()) ; #DEBUG_LINE_NO:1789
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1790
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1791
      Self.SetMenuDialogOptions(FillDirectionListLimited) ; #DEBUG_LINE_NO:1792
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterWetnessFillDirection.GetValueInt()) ; #DEBUG_LINE_NO:1793
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1794
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1795
      Self.SetMenuDialogOptions(FillDirectionList) ; #DEBUG_LINE_NO:1796
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterWeathersenseFillDirection.GetValueInt()) ; #DEBUG_LINE_NO:1797
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1798
    EndIf
  ElseIf option == Meters_UIMeterHAnchor_OID ; #DEBUG_LINE_NO:1800
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1801
      Self.SetMenuDialogOptions(HorizontalAnchorList) ; #DEBUG_LINE_NO:1802
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterExposureHAnchor.GetValueInt()) ; #DEBUG_LINE_NO:1803
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1804
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1805
      Self.SetMenuDialogOptions(HorizontalAnchorList) ; #DEBUG_LINE_NO:1806
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterWetnessHAnchor.GetValueInt()) ; #DEBUG_LINE_NO:1807
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1808
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1809
      Self.SetMenuDialogOptions(HorizontalAnchorList) ; #DEBUG_LINE_NO:1810
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterWeathersenseHAnchor.GetValueInt()) ; #DEBUG_LINE_NO:1811
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1812
    EndIf
  ElseIf option == Meters_UIMeterVAnchor_OID ; #DEBUG_LINE_NO:1814
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1815
      Self.SetMenuDialogOptions(VerticalAnchorList) ; #DEBUG_LINE_NO:1816
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterExposureVAnchor.GetValueInt()) ; #DEBUG_LINE_NO:1817
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1818
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1819
      Self.SetMenuDialogOptions(VerticalAnchorList) ; #DEBUG_LINE_NO:1820
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterWetnessVAnchor.GetValueInt()) ; #DEBUG_LINE_NO:1821
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1822
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1823
      Self.SetMenuDialogOptions(VerticalAnchorList) ; #DEBUG_LINE_NO:1824
      Self.SetMenuDialogStartIndex(_Frost_Setting_MeterWeathersenseVAnchor.GetValueInt()) ; #DEBUG_LINE_NO:1825
      Self.SetMenuDialogDefaultIndex(1) ; #DEBUG_LINE_NO:1826
    EndIf
  Else
    Bool found_armor_entry_oid = False ; #DEBUG_LINE_NO:1829
    Int idx = -1 ; #DEBUG_LINE_NO:1830
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1832
      idx = Armor_GearTypeOIDs.find(option, 0) ; #DEBUG_LINE_NO:1833
      If idx != -1 ; #DEBUG_LINE_NO:1834
        Self.SetMenuDialogOptions(GearTypeList) ; #DEBUG_LINE_NO:1835
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1836
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1840
      idx = Armor_SetProtectionOIDs.find(option, 0) ; #DEBUG_LINE_NO:1841
      If idx != -1 ; #DEBUG_LINE_NO:1842
        Self.SetMenuDialogOptions(ProtectionList) ; #DEBUG_LINE_NO:1843
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1844
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1848
      idx = Armor_ModifyPartsOIDs.find(option, 0) ; #DEBUG_LINE_NO:1849
      If idx != -1 ; #DEBUG_LINE_NO:1850
        Self.SetMenuDialogOptions(Self.GetExtraPartChoiceList(idx)) ; #DEBUG_LINE_NO:1851
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1852
      EndIf
    EndIf
  EndIf
EndFunction

Function OnOptionMenuAccept(Int option, Int index)
  If option == Gameplay_MaxExposureMode_OID ; #DEBUG_LINE_NO:1859
    Self.SetMenuOptionValue(Gameplay_MaxExposureMode_OID, MaxExposureModeList[index], False) ; #DEBUG_LINE_NO:1860
    _Frost_Setting_MaxExposureMode.SetValueInt(index + 1) ; #DEBUG_LINE_NO:1861
    Self.SaveSettingToCurrentProfile("max_exposure_mode", _Frost_Setting_MaxExposureMode.GetValueInt()) ; #DEBUG_LINE_NO:1862
  ElseIf option == Interface_WeathersenseDisplayMode_OID ; #DEBUG_LINE_NO:1863
    Self.SetMenuOptionValue(Interface_WeathersenseDisplayMode_OID, WeathersenseDisplayList[index], False) ; #DEBUG_LINE_NO:1864
    _Frost_Setting_WeathersenseDisplayMode.SetValueInt(index) ; #DEBUG_LINE_NO:1865
    Self.SaveSettingToCurrentProfile("weathersense_display_mode", _Frost_Setting_WeathersenseDisplayMode.GetValueInt()) ; #DEBUG_LINE_NO:1866
  ElseIf option == Interface_Animation_OID ; #DEBUG_LINE_NO:1867
    Self.SetMenuOptionValue(Interface_Animation_OID, AnimationList[index], False) ; #DEBUG_LINE_NO:1868
    _Frost_Setting_Animation.SetValueInt(index + 1) ; #DEBUG_LINE_NO:1869
    Self.SaveSettingToCurrentProfile("animation", _Frost_Setting_Animation.GetValueInt()) ; #DEBUG_LINE_NO:1870
  ElseIf option == Gameplay_VampirismMode_OID ; #DEBUG_LINE_NO:1871
    Self.SetMenuOptionValue(Gameplay_VampirismMode_OID, VampirismModeList[index], False) ; #DEBUG_LINE_NO:1872
    _Frost_Setting_VampireMode.SetValueInt(index) ; #DEBUG_LINE_NO:1873
    Self.SaveSettingToCurrentProfile("vampire_mode", _Frost_Setting_VampireMode.GetValueInt()) ; #DEBUG_LINE_NO:1874
  ElseIf option == SaveLoad_SelectProfile_OID ; #DEBUG_LINE_NO:1875
    Bool b = Self.ShowMessage("$FrostfallSaveLoadConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1876
    If b ; #DEBUG_LINE_NO:1877
      Self.SwitchToProfile(index + 1) ; #DEBUG_LINE_NO:1878
      Self.ForcePageReset() ; #DEBUG_LINE_NO:1879
    EndIf
  ElseIf option == Meters_UIMeterDisplay_OID ; #DEBUG_LINE_NO:1881
    Self.SetMenuOptionValue(Meters_UIMeterDisplay_OID, MeterDisplayModeList[index], False) ; #DEBUG_LINE_NO:1882
    _Frost_Setting_MeterDisplayMode.SetValueInt(index) ; #DEBUG_LINE_NO:1883
    If index == 1 ; #DEBUG_LINE_NO:1884
      Self.ForceAllMeters() ; #DEBUG_LINE_NO:1885
    Else
      Self.RemoveAllMeters() ; #DEBUG_LINE_NO:1887
    EndIf
    Self.SaveSettingToCurrentProfile("meter_display_mode", _Frost_Setting_MeterDisplayMode.GetValueInt()) ; #DEBUG_LINE_NO:1889
  ElseIf option == Meters_UIMeterLayout_OID ; #DEBUG_LINE_NO:1890
    Bool result = Self.ShowMessage("$FrostfallInterfaceSettingUIMeterLayoutConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1891
    If result == True ; #DEBUG_LINE_NO:1892
      Self.ApplyMeterPreset(index) ; #DEBUG_LINE_NO:1893
      Self.ShowMessage("$FrostfallInterfaceSettingUIMeterLayoutConfirmDone", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:1894
      Self.SaveAllSettings(_Frost_Setting_CurrentProfile.GetValueInt()) ; #DEBUG_LINE_NO:1895
      Self.ForcePageReset() ; #DEBUG_LINE_NO:1896
    EndIf
  ElseIf option == Meters_UIMeterFillDirection_OID ; #DEBUG_LINE_NO:1898
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1899
      _Frost_Setting_MeterExposureFillDirection.SetValueInt(index) ; #DEBUG_LINE_NO:1900
      Self.SetMenuOptionValue(Meters_UIMeterFillDirection_OID, FillDirectionListLimited[index], False) ; #DEBUG_LINE_NO:1901
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1902
      Self.SaveSettingToCurrentProfile("exposure_meter_fill_direction", index) ; #DEBUG_LINE_NO:1903
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1904
      _Frost_Setting_MeterWetnessFillDirection.SetValueInt(index) ; #DEBUG_LINE_NO:1905
      Self.SetMenuOptionValue(Meters_UIMeterFillDirection_OID, FillDirectionListLimited[index], False) ; #DEBUG_LINE_NO:1906
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1907
      Self.SaveSettingToCurrentProfile("wetness_meter_fill_direction", index) ; #DEBUG_LINE_NO:1908
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1909
      _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(index) ; #DEBUG_LINE_NO:1910
      Self.SetMenuOptionValue(Meters_UIMeterFillDirection_OID, FillDirectionList[index], False) ; #DEBUG_LINE_NO:1911
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1912
      Self.SaveSettingToCurrentProfile("weathersense_meter_fill_direction", index) ; #DEBUG_LINE_NO:1913
    EndIf
  ElseIf option == Meters_UIMeterHAnchor_OID ; #DEBUG_LINE_NO:1915
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1916
      _Frost_Setting_MeterExposureHAnchor.SetValueInt(index) ; #DEBUG_LINE_NO:1917
      Self.SetMenuOptionValue(Meters_UIMeterHAnchor_OID, HorizontalAnchorList[index], False) ; #DEBUG_LINE_NO:1918
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1919
      Self.SaveSettingToCurrentProfile("exposure_meter_hanchor", index) ; #DEBUG_LINE_NO:1920
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1921
      _Frost_Setting_MeterWetnessHAnchor.SetValueInt(index) ; #DEBUG_LINE_NO:1922
      Self.SetMenuOptionValue(Meters_UIMeterHAnchor_OID, HorizontalAnchorList[index], False) ; #DEBUG_LINE_NO:1923
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1924
      Self.SaveSettingToCurrentProfile("wetness_meter_hanchor", index) ; #DEBUG_LINE_NO:1925
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1926
      _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(index) ; #DEBUG_LINE_NO:1927
      Self.SetMenuOptionValue(Meters_UIMeterHAnchor_OID, HorizontalAnchorList[index], False) ; #DEBUG_LINE_NO:1928
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1929
      Self.SaveSettingToCurrentProfile("weathersense_meter_hanchor", index) ; #DEBUG_LINE_NO:1930
    EndIf
  ElseIf option == Meters_UIMeterVAnchor_OID ; #DEBUG_LINE_NO:1932
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1933
      _Frost_Setting_MeterExposureVAnchor.SetValueInt(index) ; #DEBUG_LINE_NO:1934
      Self.SetMenuOptionValue(Meters_UIMeterVAnchor_OID, VerticalAnchorList[index], False) ; #DEBUG_LINE_NO:1935
      Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:1936
      Self.SaveSettingToCurrentProfile("exposure_meter_vanchor", index) ; #DEBUG_LINE_NO:1937
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1938
      _Frost_Setting_MeterWetnessVAnchor.SetValueInt(index) ; #DEBUG_LINE_NO:1939
      Self.SetMenuOptionValue(Meters_UIMeterVAnchor_OID, VerticalAnchorList[index], False) ; #DEBUG_LINE_NO:1940
      Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:1941
      Self.SaveSettingToCurrentProfile("wetness_meter_vanchor", index) ; #DEBUG_LINE_NO:1942
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1943
      _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(index) ; #DEBUG_LINE_NO:1944
      Self.SetMenuOptionValue(Meters_UIMeterVAnchor_OID, VerticalAnchorList[index], False) ; #DEBUG_LINE_NO:1945
      Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:1946
      Self.SaveSettingToCurrentProfile("weathersense_meter_vanchor", index) ; #DEBUG_LINE_NO:1947
    EndIf
  Else
    Bool found_armor_entry_oid = False ; #DEBUG_LINE_NO:1950
    Int idx = -1 ; #DEBUG_LINE_NO:1951
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1953
      idx = Armor_GearTypeOIDs.find(option, 0) ; #DEBUG_LINE_NO:1954
      If idx != -1 ; #DEBUG_LINE_NO:1955
        Self.ModifyGearType(idx, index) ; #DEBUG_LINE_NO:1956
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1957
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1961
      idx = Armor_SetProtectionOIDs.find(option, 0) ; #DEBUG_LINE_NO:1962
      If idx != -1 ; #DEBUG_LINE_NO:1963
        Self.ModifyGearProtection(idx, index) ; #DEBUG_LINE_NO:1964
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1965
      EndIf
    EndIf
    If !found_armor_entry_oid ; #DEBUG_LINE_NO:1969
      idx = Armor_ModifyPartsOIDs.find(option, 0) ; #DEBUG_LINE_NO:1970
      If idx != -1 ; #DEBUG_LINE_NO:1971
        Self.ModifyGearExtraParts(idx, index) ; #DEBUG_LINE_NO:1972
        found_armor_entry_oid = True ; #DEBUG_LINE_NO:1973
      EndIf
    EndIf
  EndIf
EndFunction

Function OnOptionColorAccept(Int option, Int color)
  If option == Meters_UIMeterColor_OID ; #DEBUG_LINE_NO:1980
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:1981
      _Frost_Setting_MeterExposureColor.SetValueInt(color) ; #DEBUG_LINE_NO:1982
      Self.SetColorOptionValue(option, color, False) ; #DEBUG_LINE_NO:1983
      If !Self.IsMeterInverted(ExposureMeterHandler as commonmeterinterfacehandler) ; #DEBUG_LINE_NO:1984
        ExposureMeterHandler.SetMeterColors(_Frost_Setting_MeterExposureColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:1985
      EndIf
      Self.SaveSettingToCurrentProfile("exposure_meter_color", color) ; #DEBUG_LINE_NO:1987
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WETNESS ; #DEBUG_LINE_NO:1988
      _Frost_Setting_MeterWetnessColor.SetValueInt(color) ; #DEBUG_LINE_NO:1989
      Self.SetColorOptionValue(option, color, False) ; #DEBUG_LINE_NO:1990
      WetnessMeterHandler.SetMeterColors(color, -1) ; #DEBUG_LINE_NO:1991
      Self.SaveSettingToCurrentProfile("wetness_meter_color", color) ; #DEBUG_LINE_NO:1992
    ElseIf meter_being_configured == METER_BEING_CONFIGURED_WEATHERSENSE ; #DEBUG_LINE_NO:1993
      _Frost_Setting_MeterWeathersenseColor.SetValueInt(color) ; #DEBUG_LINE_NO:1994
      Self.SetColorOptionValue(option, color, False) ; #DEBUG_LINE_NO:1995
      WeathersenseMeterHandler.SetMeterColors(color, -1) ; #DEBUG_LINE_NO:1996
      Self.SaveSettingToCurrentProfile("weathersense_meter_color", color) ; #DEBUG_LINE_NO:1997
    EndIf
  ElseIf option == Meters_UIMeterColorAlt_OID ; #DEBUG_LINE_NO:1999
    If meter_being_configured == METER_BEING_CONFIGURED_EXPOSURE ; #DEBUG_LINE_NO:2000
      _Frost_Setting_MeterExposureColorWarm.SetValueInt(color) ; #DEBUG_LINE_NO:2001
      Self.SetColorOptionValue(option, color, False) ; #DEBUG_LINE_NO:2002
      If Self.IsMeterInverted(ExposureMeterHandler as commonmeterinterfacehandler) ; #DEBUG_LINE_NO:2003
        ExposureMeterHandler.SetMeterColors(color, -1) ; #DEBUG_LINE_NO:2004
      EndIf
      Self.SaveSettingToCurrentProfile("exposure_meter_color", color) ; #DEBUG_LINE_NO:2006
    EndIf
  EndIf
EndFunction

Function OnOptionKeyMapChange(Int option, Int keyCode, String conflictControl, String conflictName)
  If option == Gameplay_WeathersenseHotkey_OID ; #DEBUG_LINE_NO:2013
    Bool success = Self.RemapHotkey(option, keyCode, conflictControl, conflictName, _Frost_HotkeyWeathersense, _Frost_Weathersense_Spell) ; #DEBUG_LINE_NO:2014
    If success ; #DEBUG_LINE_NO:2015
      Self.SaveSettingToCurrentProfile("hotkey_weathersense", keyCode) ; #DEBUG_LINE_NO:2016
    EndIf
  EndIf
EndFunction

Bool Function RemapHotkey(Int option, Int keyCode, String conflictControl, String conflictName, GlobalVariable akHotkeyGlobal, Spell akHotkeySpell)
  _camp_strings cs = _campinternal.GetCampfireStrings() ; #DEBUG_LINE_NO:2022
  If conflictControl != "" ; #DEBUG_LINE_NO:2023
    If conflictName != "" ; #DEBUG_LINE_NO:2024
      Bool b = Self.ShowMessage(cs.HotkeyConflict1 + conflictControl + cs.HotkeyConflict2 + conflictName + cs.HotkeyConflict3_mod, True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2026
      If b ; #DEBUG_LINE_NO:2027
        akHotkeyGlobal.SetValueInt(keyCode) ; #DEBUG_LINE_NO:2028
        Self.RegisterForKey(akHotkeyGlobal.GetValueInt()) ; #DEBUG_LINE_NO:2029
        Self.ForcePageReset() ; #DEBUG_LINE_NO:2030
        Game.GetPlayer().RemoveSpell(akHotkeySpell) ; #DEBUG_LINE_NO:2031
        Return True ; #DEBUG_LINE_NO:2032
      EndIf
    Else
      Self.ShowMessage(cs.HotkeyConflict1 + conflictControl + cs.HotkeyConflict3_game, False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2036
      Return False ; #DEBUG_LINE_NO:2037
    EndIf
  Else
    akHotkeyGlobal.SetValueInt(keyCode) ; #DEBUG_LINE_NO:2040
    Self.RegisterForKey(akHotkeyGlobal.GetValueInt()) ; #DEBUG_LINE_NO:2041
    Self.ForcePageReset() ; #DEBUG_LINE_NO:2042
    Game.GetPlayer().RemoveSpell(akHotkeySpell) ; #DEBUG_LINE_NO:2043
    Return True ; #DEBUG_LINE_NO:2044
  EndIf
EndFunction

Function OnOptionInputOpen(Int option)
  If option == SaveLoad_RenameProfile_OID ; #DEBUG_LINE_NO:2049
    Self.SetInputDialogStartText(Self.GetProfileName(_Frost_Setting_CurrentProfile.GetValueInt())) ; #DEBUG_LINE_NO:2050
  EndIf
EndFunction

Function OnOptionInputAccept(Int option, String str)
  If option == SaveLoad_RenameProfile_OID ; #DEBUG_LINE_NO:2055
    If str != "" ; #DEBUG_LINE_NO:2056
      String profile_path = CONFIG_PATH + "profile" + _Frost_Setting_CurrentProfile.GetValueInt() as String ; #DEBUG_LINE_NO:2057
      jsonutil.SetStringValue(profile_path, "profile_name", str) ; #DEBUG_LINE_NO:2058
      jsonutil.Save(profile_path, False) ; #DEBUG_LINE_NO:2059
      Self.ForcePageReset() ; #DEBUG_LINE_NO:2060
    Else
      Self.ShowMessage("$FrostfallSaveLoadRenameErrorBlank", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2062
    EndIf
  EndIf
EndFunction

Function SaveSettingToCurrentProfile(String asKeyName, Int aiValue)
  If _Frost_Setting_AutoSaveLoad.GetValueInt() == 2 ; #DEBUG_LINE_NO:2068
    Int current_profile_index = _Frost_Setting_CurrentProfile.GetValueInt() ; #DEBUG_LINE_NO:2069
    jsonutil.SetIntValue(CONFIG_PATH + "profile" + current_profile_index as String, asKeyName, aiValue) ; #DEBUG_LINE_NO:2070
    jsonutil.Save(CONFIG_PATH + "profile" + current_profile_index as String, False) ; #DEBUG_LINE_NO:2071
  EndIf
EndFunction

Function SaveSettingToCurrentProfileFloat(String asKeyName, Float afValue)
  If _Frost_Setting_AutoSaveLoad.GetValueInt() == 2 ; #DEBUG_LINE_NO:2076
    Int current_profile_index = _Frost_Setting_CurrentProfile.GetValueInt() ; #DEBUG_LINE_NO:2077
    jsonutil.SetFloatValue(CONFIG_PATH + "profile" + current_profile_index as String, asKeyName, afValue) ; #DEBUG_LINE_NO:2078
    jsonutil.Save(CONFIG_PATH + "profile" + current_profile_index as String, False) ; #DEBUG_LINE_NO:2079
  EndIf
EndFunction

Int Function LoadSettingFromProfile(Int aiProfileIndex, String asKeyName)
  Return jsonutil.GetIntValue(CONFIG_PATH + "profile" + aiProfileIndex as String, asKeyName, -1) ; #DEBUG_LINE_NO:2084
EndFunction

Float Function LoadSettingFromProfileFloat(Int aiProfileIndex, String asKeyName)
  Return jsonutil.GetFloatValue(CONFIG_PATH + "profile" + aiProfileIndex as String, asKeyName, -1 as Float) ; #DEBUG_LINE_NO:2088
EndFunction

Function LoadProfileOnStartup()
  Int auto_load = jsonutil.GetIntValue(CONFIG_PATH + "common", "auto_load", 0) ; #DEBUG_LINE_NO:2092
  If auto_load == 2 ; #DEBUG_LINE_NO:2093
    _Frost_Setting_AutoSaveLoad.SetValueInt(2) ; #DEBUG_LINE_NO:2094
    Int last_profile = jsonutil.GetIntValue(CONFIG_PATH + "common", "last_profile", 0) ; #DEBUG_LINE_NO:2095
    If last_profile != 0 ; #DEBUG_LINE_NO:2096
      _Frost_Setting_CurrentProfile.SetValueInt(last_profile) ; #DEBUG_LINE_NO:2097
      Self.SwitchToProfile(last_profile) ; #DEBUG_LINE_NO:2098
    Else
      _Frost_Setting_CurrentProfile.SetValueInt(1) ; #DEBUG_LINE_NO:2101
      jsonutil.SetIntValue(CONFIG_PATH + "common", "last_profile", 1) ; #DEBUG_LINE_NO:2102
      jsonutil.Save(CONFIG_PATH + "common", False) ; #DEBUG_LINE_NO:2103
      Self.SwitchToProfile(1) ; #DEBUG_LINE_NO:2104
    EndIf
  ElseIf auto_load == 1 ; #DEBUG_LINE_NO:2106
    _Frost_Setting_AutoSaveLoad.SetValueInt(1) ; #DEBUG_LINE_NO:2107
  ElseIf auto_load == 0 ; #DEBUG_LINE_NO:2108
    _Frost_Setting_AutoSaveLoad.SetValueInt(2) ; #DEBUG_LINE_NO:2111
    _Frost_Setting_CurrentProfile.SetValueInt(1) ; #DEBUG_LINE_NO:2112
    jsonutil.SetIntValue(CONFIG_PATH + "common", "auto_load", 2) ; #DEBUG_LINE_NO:2113
    jsonutil.SetIntValue(CONFIG_PATH + "common", "last_profile", 1) ; #DEBUG_LINE_NO:2114
    jsonutil.Save(CONFIG_PATH + "common", False) ; #DEBUG_LINE_NO:2115
    Self.SwitchToProfile(1) ; #DEBUG_LINE_NO:2116
  EndIf
EndFunction

Function OnKeyDown(Int keyCode)
  If ui.IsMenuOpen("Console") || ui.IsMenuOpen("Book Menu") || ui.IsMenuOpen("BarterMenu") || ui.IsMenuOpen("ContainerMenu") || ui.IsMenuOpen("Crafting Menu") || ui.IsMenuOpen("Dialogue Menu") || ui.IsMenuOpen("FavoritesMenu") || ui.IsMenuOpen("InventoryMenu") || ui.IsMenuOpen("Journal Menu") || ui.IsMenuOpen("Lockpicking Menu") || ui.IsMenuOpen("MagicMenu") || ui.IsMenuOpen("MapMenu") || ui.IsMenuOpen("MessageBoxMenu") || ui.IsMenuOpen("Sleep/Wait Menu") || ui.IsMenuOpen("StatsMenu") || ui.IsMenuOpen("UITextEntryMenu") ; #DEBUG_LINE_NO:2121,2122,2123,2124,2125,2126,2127,2128,2129,2130,2131,2132,2133,2134,2135,2136
    Return  ; #DEBUG_LINE_NO:2137
  EndIf
  If keyCode == _Frost_HotkeyWeathersense.GetValueInt() ; #DEBUG_LINE_NO:2139
    _Frost_Weathersense_Spell.Cast(PlayerRef as ObjectReference, None) ; #DEBUG_LINE_NO:2140
  EndIf
EndFunction

String Function GetCustomControl(Int keyCode)
  If keyCode == _Frost_HotkeyWeathersense.GetValueInt() ; #DEBUG_LINE_NO:2145
    Return "Survival Skill: Weathersense" ; #DEBUG_LINE_NO:2146
  Else
    Return "" ; #DEBUG_LINE_NO:2148
  EndIf
EndFunction

String Function GetProfileName(Int aiProfileIndex)
  Return jsonutil.GetStringValue(CONFIG_PATH + "profile" + aiProfileIndex as String, "profile_name", "Profile " + aiProfileIndex as String) ; #DEBUG_LINE_NO:2153
EndFunction

Function SwitchToProfile(Int aiProfileIndex)
  _Frost_Setting_CurrentProfile.SetValueInt(aiProfileIndex) ; #DEBUG_LINE_NO:2157
  jsonutil.SetIntValue(CONFIG_PATH + "common", "last_profile", aiProfileIndex) ; #DEBUG_LINE_NO:2158
  jsonutil.Save(CONFIG_PATH + "common", False) ; #DEBUG_LINE_NO:2159
  String pname = jsonutil.GetStringValue(CONFIG_PATH + "profile" + aiProfileIndex as String, "profile_name", "") ; #DEBUG_LINE_NO:2161
  If pname == "" ; #DEBUG_LINE_NO:2162
    Self.GenerateDefaultProfile(aiProfileIndex) ; #DEBUG_LINE_NO:2163
  EndIf
  Self.CleanProfile(aiProfileIndex) ; #DEBUG_LINE_NO:2165
  Int val = Self.LoadSettingFromProfile(aiProfileIndex, "animation") ; #DEBUG_LINE_NO:2167
  If val != -1 ; #DEBUG_LINE_NO:2168
    _Frost_Setting_Animation.SetValueInt(val) ; #DEBUG_LINE_NO:2169
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "follower_animation") ; #DEBUG_LINE_NO:2171
  If val != -1 ; #DEBUG_LINE_NO:2172
    _Frost_Setting_FollowerAnimation.SetValueInt(val) ; #DEBUG_LINE_NO:2173
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "condition_messages") ; #DEBUG_LINE_NO:2175
  If val != -1 ; #DEBUG_LINE_NO:2176
    _Frost_Setting_ConditionMessages.SetValueInt(val) ; #DEBUG_LINE_NO:2177
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "display_attributes_in_weathersense") ; #DEBUG_LINE_NO:2179
  If val != -1 ; #DEBUG_LINE_NO:2180
    _Frost_Setting_DisplayAttributesInWeathersense.SetValueInt(val) ; #DEBUG_LINE_NO:2181
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "display_attribute_values_in_weathersense") ; #DEBUG_LINE_NO:2183
  If val != -1 ; #DEBUG_LINE_NO:2184
    _Frost_Setting_DisplayAttributeValuesInWeathersense.SetValueInt(val) ; #DEBUG_LINE_NO:2185
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "notification_equipmentvalues") ; #DEBUG_LINE_NO:2187
  If val != -1 ; #DEBUG_LINE_NO:2188
    _Frost_Setting_Notifications_EquipmentValues.SetValueInt(val) ; #DEBUG_LINE_NO:2189
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "notification_equipmentsummary") ; #DEBUG_LINE_NO:2191
  If val != -1 ; #DEBUG_LINE_NO:2192
    _Frost_Setting_Notifications_EquipmentSummary.SetValueInt(val) ; #DEBUG_LINE_NO:2193
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "exposure_pause_combat") ; #DEBUG_LINE_NO:2195
  If val != -1 ; #DEBUG_LINE_NO:2196
    _Frost_Setting_ExposurePauseCombat.SetValueInt(val) ; #DEBUG_LINE_NO:2197
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "exposure_pause_dialogue") ; #DEBUG_LINE_NO:2199
  If val != -1 ; #DEBUG_LINE_NO:2200
    _Frost_Setting_ExposurePauseDialogue.SetValueInt(val) ; #DEBUG_LINE_NO:2201
  EndIf
  Float fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "exposure_rate") ; #DEBUG_LINE_NO:2203
  If fval != -1 as Float ; #DEBUG_LINE_NO:2204
    _Frost_Setting_ExposureRate.SetValue(fval) ; #DEBUG_LINE_NO:2205
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "force_feedback") ; #DEBUG_LINE_NO:2207
  If val != -1 ; #DEBUG_LINE_NO:2208
    _Frost_Setting_ForceFeedback.SetValueInt(val) ; #DEBUG_LINE_NO:2209
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "frost_shader_on") ; #DEBUG_LINE_NO:2211
  If val != -1 ; #DEBUG_LINE_NO:2212
    _Frost_Setting_FrostShaderOn.SetValueInt(val) ; #DEBUG_LINE_NO:2213
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "full_screen_effects") ; #DEBUG_LINE_NO:2215
  If val != -1 ; #DEBUG_LINE_NO:2216
    _Frost_Setting_FullScreenEffects.SetValueInt(val) ; #DEBUG_LINE_NO:2217
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "max_exposure_mode") ; #DEBUG_LINE_NO:2219
  If val != -1 ; #DEBUG_LINE_NO:2220
    _Frost_Setting_MaxExposureMode.SetValueInt(val) ; #DEBUG_LINE_NO:2221
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "meter_display_mode") ; #DEBUG_LINE_NO:2224
  If val != -1 ; #DEBUG_LINE_NO:2225
    _Frost_Setting_MeterDisplayMode.SetValueInt(val) ; #DEBUG_LINE_NO:2226
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "meter_display_time") ; #DEBUG_LINE_NO:2228
  If val != -1 ; #DEBUG_LINE_NO:2229
    _Frost_Setting_MeterDisplayTime.SetValueInt(val) ; #DEBUG_LINE_NO:2230
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "exposure_meter_color") ; #DEBUG_LINE_NO:2233
  If val != -1 ; #DEBUG_LINE_NO:2234
    _Frost_Setting_MeterExposureColor.SetValueInt(val) ; #DEBUG_LINE_NO:2235
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "exposure_meter_color_warm") ; #DEBUG_LINE_NO:2237
  If val != -1 ; #DEBUG_LINE_NO:2238
    _Frost_Setting_MeterExposureColorWarm.SetValueInt(val) ; #DEBUG_LINE_NO:2239
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "exposure_meter_fill_direction") ; #DEBUG_LINE_NO:2241
  If val != -1 ; #DEBUG_LINE_NO:2242
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(val) ; #DEBUG_LINE_NO:2243
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "exposure_meter_hanchor") ; #DEBUG_LINE_NO:2245
  If val != -1 ; #DEBUG_LINE_NO:2246
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(val) ; #DEBUG_LINE_NO:2247
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "exposure_meter_vanchor") ; #DEBUG_LINE_NO:2249
  If val != -1 ; #DEBUG_LINE_NO:2250
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(val) ; #DEBUG_LINE_NO:2251
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "wetness_meter_color") ; #DEBUG_LINE_NO:2253
  If val != -1 ; #DEBUG_LINE_NO:2254
    _Frost_Setting_MeterWetnessColor.SetValueInt(val) ; #DEBUG_LINE_NO:2255
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "wetness_meter_fill_direction") ; #DEBUG_LINE_NO:2257
  If val != -1 ; #DEBUG_LINE_NO:2258
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(val) ; #DEBUG_LINE_NO:2259
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "wetness_meter_hanchor") ; #DEBUG_LINE_NO:2261
  If val != -1 ; #DEBUG_LINE_NO:2262
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(val) ; #DEBUG_LINE_NO:2263
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "wetness_meter_vanchor") ; #DEBUG_LINE_NO:2265
  If val != -1 ; #DEBUG_LINE_NO:2266
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(val) ; #DEBUG_LINE_NO:2267
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "weathersense_meter_color") ; #DEBUG_LINE_NO:2269
  If val != -1 ; #DEBUG_LINE_NO:2270
    _Frost_Setting_MeterWeathersenseColor.SetValueInt(val) ; #DEBUG_LINE_NO:2271
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "weathersense_meter_fill_direction") ; #DEBUG_LINE_NO:2273
  If val != -1 ; #DEBUG_LINE_NO:2274
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(val) ; #DEBUG_LINE_NO:2275
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "weathersense_meter_hanchor") ; #DEBUG_LINE_NO:2277
  If val != -1 ; #DEBUG_LINE_NO:2278
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(val) ; #DEBUG_LINE_NO:2279
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "weathersense_meter_vanchor") ; #DEBUG_LINE_NO:2281
  If val != -1 ; #DEBUG_LINE_NO:2282
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(val) ; #DEBUG_LINE_NO:2283
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "movement_penalty") ; #DEBUG_LINE_NO:2286
  If val != -1 ; #DEBUG_LINE_NO:2287
    _Frost_Setting_MovementPenalty.SetValueInt(val) ; #DEBUG_LINE_NO:2288
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "no_fast_travel") ; #DEBUG_LINE_NO:2290
  If val != -1 ; #DEBUG_LINE_NO:2291
    _Frost_Setting_NoFastTravel.SetValueInt(val) ; #DEBUG_LINE_NO:2292
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "no_waiting") ; #DEBUG_LINE_NO:2294
  If val != -1 ; #DEBUG_LINE_NO:2295
    _Frost_Setting_NoWaiting.SetValueInt(val) ; #DEBUG_LINE_NO:2296
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "sound_effects") ; #DEBUG_LINE_NO:2298
  If val != -1 ; #DEBUG_LINE_NO:2299
    _Frost_Setting_SoundEffects.SetValueInt(val) ; #DEBUG_LINE_NO:2300
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "weather_messages") ; #DEBUG_LINE_NO:2302
  If val != -1 ; #DEBUG_LINE_NO:2303
    _Frost_Setting_WeatherMessages.SetValueInt(val) ; #DEBUG_LINE_NO:2304
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "weathersense_display_mode") ; #DEBUG_LINE_NO:2306
  If val != -1 ; #DEBUG_LINE_NO:2307
    _Frost_Setting_WeathersenseDisplayMode.SetValueInt(val) ; #DEBUG_LINE_NO:2308
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "wet_shader_on") ; #DEBUG_LINE_NO:2310
  If val != -1 ; #DEBUG_LINE_NO:2311
    _Frost_Setting_WetShaderOn.SetValueInt(val) ; #DEBUG_LINE_NO:2312
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "frigid_water_is_lethal") ; #DEBUG_LINE_NO:2314
  If val != -1 ; #DEBUG_LINE_NO:2315
    _Frost_Setting_FrigidWaterIsLethal.SetValueInt(val) ; #DEBUG_LINE_NO:2316
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "vampire_mode") ; #DEBUG_LINE_NO:2318
  If val != -1 ; #DEBUG_LINE_NO:2319
    _Frost_Setting_VampireMode.SetValueInt(val) ; #DEBUG_LINE_NO:2320
  EndIf
  val = Self.LoadSettingFromProfile(aiProfileIndex, "display_tutorials") ; #DEBUG_LINE_NO:2322
  If val != -1 ; #DEBUG_LINE_NO:2323
    _Frost_Setting_DisplayTutorials.SetValueInt(val) ; #DEBUG_LINE_NO:2324
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "exposure_meter_opacity") ; #DEBUG_LINE_NO:2326
  If fval != -1.0 ; #DEBUG_LINE_NO:2327
    _Frost_Setting_MeterExposureOpacity.SetValue(fval) ; #DEBUG_LINE_NO:2328
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "exposure_meter_height") ; #DEBUG_LINE_NO:2330
  If fval != -1.0 ; #DEBUG_LINE_NO:2331
    _Frost_Setting_MeterExposureHeight.SetValue(fval) ; #DEBUG_LINE_NO:2332
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "exposure_meter_width") ; #DEBUG_LINE_NO:2334
  If fval != -1.0 ; #DEBUG_LINE_NO:2335
    _Frost_Setting_MeterExposureWidth.SetValue(fval) ; #DEBUG_LINE_NO:2336
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "exposure_meter_xpos") ; #DEBUG_LINE_NO:2338
  If fval != -1.0 ; #DEBUG_LINE_NO:2339
    _Frost_Setting_MeterExposureXPos.SetValue(fval) ; #DEBUG_LINE_NO:2340
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "exposure_meter_ypos") ; #DEBUG_LINE_NO:2342
  If fval != -1.0 ; #DEBUG_LINE_NO:2343
    _Frost_Setting_MeterExposureYPos.SetValue(fval) ; #DEBUG_LINE_NO:2344
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "wetness_meter_opacity") ; #DEBUG_LINE_NO:2346
  If fval != -1.0 ; #DEBUG_LINE_NO:2347
    _Frost_Setting_MeterWetnessOpacity.SetValue(fval) ; #DEBUG_LINE_NO:2348
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "wetness_meter_height") ; #DEBUG_LINE_NO:2350
  If fval != -1.0 ; #DEBUG_LINE_NO:2351
    _Frost_Setting_MeterWetnessHeight.SetValue(fval) ; #DEBUG_LINE_NO:2352
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "wetness_meter_width") ; #DEBUG_LINE_NO:2354
  If fval != -1.0 ; #DEBUG_LINE_NO:2355
    _Frost_Setting_MeterWetnessWidth.SetValue(fval) ; #DEBUG_LINE_NO:2356
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "wetness_meter_xpos") ; #DEBUG_LINE_NO:2358
  If fval != -1.0 ; #DEBUG_LINE_NO:2359
    _Frost_Setting_MeterWetnessXPos.SetValue(fval) ; #DEBUG_LINE_NO:2360
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "wetness_meter_ypos") ; #DEBUG_LINE_NO:2362
  If fval != -1.0 ; #DEBUG_LINE_NO:2363
    _Frost_Setting_MeterWetnessYPos.SetValue(fval) ; #DEBUG_LINE_NO:2364
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "weathersense_meter_opacity") ; #DEBUG_LINE_NO:2366
  If fval != -1.0 ; #DEBUG_LINE_NO:2367
    _Frost_Setting_MeterWeathersenseOpacity.SetValue(fval) ; #DEBUG_LINE_NO:2368
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "weathersense_meter_height") ; #DEBUG_LINE_NO:2370
  If fval != -1.0 ; #DEBUG_LINE_NO:2371
    _Frost_Setting_MeterWeathersenseHeight.SetValue(fval) ; #DEBUG_LINE_NO:2372
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "weathersense_meter_width") ; #DEBUG_LINE_NO:2374
  If fval != -1.0 ; #DEBUG_LINE_NO:2375
    _Frost_Setting_MeterWeathersenseWidth.SetValue(fval) ; #DEBUG_LINE_NO:2376
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "weathersense_meter_xpos") ; #DEBUG_LINE_NO:2378
  If fval != -1.0 ; #DEBUG_LINE_NO:2379
    _Frost_Setting_MeterWeathersenseXPos.SetValue(fval) ; #DEBUG_LINE_NO:2380
  EndIf
  fval = Self.LoadSettingFromProfileFloat(aiProfileIndex, "weathersense_meter_ypos") ; #DEBUG_LINE_NO:2382
  If fval != -1.0 ; #DEBUG_LINE_NO:2383
    _Frost_Setting_MeterWeathersenseYPos.SetValue(fval) ; #DEBUG_LINE_NO:2384
  EndIf
  Int i = 0 ; #DEBUG_LINE_NO:2388
  While !ExposureMeter.Ready && i < 50 ; #DEBUG_LINE_NO:2389
    Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:2390
    i += 1 ; #DEBUG_LINE_NO:2391
  EndWhile
  If !Self.IsMeterInverted(ExposureMeterHandler as commonmeterinterfacehandler) ; #DEBUG_LINE_NO:2393
    ExposureMeterHandler.SetMeterColors(_Frost_Setting_MeterExposureColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:2394
  Else
    ExposureMeterHandler.SetMeterColors(_Frost_Setting_MeterExposureColorWarm.GetValueInt(), -1) ; #DEBUG_LINE_NO:2396
  EndIf
  Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:2398
  i = 0 ; #DEBUG_LINE_NO:2400
  While !WetnessMeter.Ready && i < 50 ; #DEBUG_LINE_NO:2401
    Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:2402
    i += 1 ; #DEBUG_LINE_NO:2403
  EndWhile
  WetnessMeterHandler.SetMeterColors(_Frost_Setting_MeterWetnessColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:2405
  Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:2406
  i = 0 ; #DEBUG_LINE_NO:2408
  While !WeathersenseMeter.Ready && i < 50 ; #DEBUG_LINE_NO:2409
    Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:2410
    i += 1 ; #DEBUG_LINE_NO:2411
  EndWhile
  WeathersenseMeterHandler.SetMeterColors(_Frost_Setting_MeterWeathersenseColor.GetValueInt(), -1) ; #DEBUG_LINE_NO:2413
  Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:2414
  Self.ForceAllMeters() ; #DEBUG_LINE_NO:2416
  val = Self.LoadSettingFromProfile(aiProfileIndex, "hotkey_weathersense") ; #DEBUG_LINE_NO:2418
  If val != -1 && val != 0 ; #DEBUG_LINE_NO:2419
    Self.RegisterForKey(val) ; #DEBUG_LINE_NO:2420
    _Frost_HotkeyWeathersense.SetValueInt(val) ; #DEBUG_LINE_NO:2421
    PlayerRef.RemoveSpell(_Frost_Weathersense_Spell) ; #DEBUG_LINE_NO:2422
  Else
    Self.UnregisterForKey(_Frost_HotkeyWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:2424
    _Frost_HotkeyWeathersense.SetValue(0 as Float) ; #DEBUG_LINE_NO:2425
    PlayerRef.AddSpell(_Frost_Weathersense_Spell, False) ; #DEBUG_LINE_NO:2426
  EndIf
  _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:2430
  clothing.RefreshWornGearData(clothing.WornGearMainForms, clothing.WornGearForms, clothing._Frost_WornGearData) ; #DEBUG_LINE_NO:2431
  clothing.SendEvent_UpdateWarmthAndCoverage(False) ; #DEBUG_LINE_NO:2432
EndFunction

Function GenerateDefaultProfile(Int aiProfileIndex)
  String profile_path = CONFIG_PATH + "profile" + aiProfileIndex as String ; #DEBUG_LINE_NO:2436
  jsonutil.SetStringValue(profile_path, "profile_name", "Profile " + aiProfileIndex as String) ; #DEBUG_LINE_NO:2437
  jsonutil.SetIntValue(profile_path, "profile_version", _Frost_SettingsProfileVersion.GetValueInt()) ; #DEBUG_LINE_NO:2438
  jsonutil.SetIntValue(profile_path, "animation", 2) ; #DEBUG_LINE_NO:2439
  jsonutil.SetIntValue(profile_path, "follower_animation", 2) ; #DEBUG_LINE_NO:2440
  jsonutil.SetIntValue(profile_path, "condition_messages", 2) ; #DEBUG_LINE_NO:2441
  jsonutil.SetIntValue(profile_path, "display_attributes_in_weathersense", 1) ; #DEBUG_LINE_NO:2442
  jsonutil.SetIntValue(profile_path, "display_attribute_values_in_weathersense", 1) ; #DEBUG_LINE_NO:2443
  jsonutil.SetIntValue(profile_path, "notification_equipmentvalues", 2) ; #DEBUG_LINE_NO:2444
  jsonutil.SetIntValue(profile_path, "notification_equipmentsummary", 2) ; #DEBUG_LINE_NO:2445
  jsonutil.SetIntValue(profile_path, "exposure_pause_combat", 2) ; #DEBUG_LINE_NO:2446
  jsonutil.SetIntValue(profile_path, "exposure_pause_dialogue", 2) ; #DEBUG_LINE_NO:2447
  jsonutil.SetFloatValue(profile_path, "exposure_rate", 1.0) ; #DEBUG_LINE_NO:2448
  jsonutil.SetIntValue(profile_path, "force_feedback", 2) ; #DEBUG_LINE_NO:2449
  jsonutil.SetIntValue(profile_path, "frost_shader_on", 2) ; #DEBUG_LINE_NO:2450
  jsonutil.SetIntValue(profile_path, "full_screen_effects", 2) ; #DEBUG_LINE_NO:2451
  jsonutil.SetIntValue(profile_path, "max_exposure_mode", 2) ; #DEBUG_LINE_NO:2452
  jsonutil.SetIntValue(profile_path, "meter_display_mode", 2) ; #DEBUG_LINE_NO:2453
  jsonutil.SetIntValue(profile_path, "meter_display_time", 4) ; #DEBUG_LINE_NO:2454
  jsonutil.SetFloatValue(profile_path, "exposure_meter_opacity", 100.0) ; #DEBUG_LINE_NO:2455
  jsonutil.SetIntValue(profile_path, "exposure_meter_color", 9687295) ; #DEBUG_LINE_NO:2456
  jsonutil.SetIntValue(profile_path, "exposure_meter_color_warm", 13369344) ; #DEBUG_LINE_NO:2457
  jsonutil.SetIntValue(profile_path, "exposure_meter_fill_direction", EXPOSURE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:2458
  jsonutil.SetFloatValue(profile_path, "exposure_meter_height", NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:2459
  jsonutil.SetFloatValue(profile_path, "exposure_meter_width", NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:2460
  jsonutil.SetFloatValue(profile_path, "exposure_meter_xpos", EXPOSURE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:2461
  jsonutil.SetFloatValue(profile_path, "exposure_meter_ypos", EXPOSURE_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:2462
  jsonutil.SetIntValue(profile_path, "exposure_meter_hanchor", EXPOSURE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:2463
  jsonutil.SetIntValue(profile_path, "exposure_meter_vanchor", EXPOSURE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:2464
  jsonutil.SetFloatValue(profile_path, "wetness_meter_opacity", 100.0) ; #DEBUG_LINE_NO:2465
  jsonutil.SetIntValue(profile_path, "wetness_meter_color", 2386420) ; #DEBUG_LINE_NO:2466
  jsonutil.SetIntValue(profile_path, "wetness_meter_fill_direction", WETNESS_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:2467
  jsonutil.SetFloatValue(profile_path, "wetness_meter_height", CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:2468
  jsonutil.SetFloatValue(profile_path, "wetness_meter_width", CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:2469
  jsonutil.SetFloatValue(profile_path, "wetness_meter_xpos", WETNESS_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:2470
  jsonutil.SetFloatValue(profile_path, "wetness_meter_ypos", WETNESS_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:2471
  jsonutil.SetIntValue(profile_path, "wetness_meter_hanchor", WETNESS_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:2472
  jsonutil.SetIntValue(profile_path, "wetness_meter_vanchor", WETNESS_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:2473
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_opacity", 100.0) ; #DEBUG_LINE_NO:2474
  jsonutil.SetIntValue(profile_path, "weathersense_meter_color", 16630567) ; #DEBUG_LINE_NO:2475
  jsonutil.SetIntValue(profile_path, "weathersense_meter_fill_direction", WEATHERSENSE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:2476
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_height", CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:2477
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_width", CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:2478
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_xpos", WEATHERSENSE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:2479
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_ypos", WEATHERSENSE_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:2480
  jsonutil.SetIntValue(profile_path, "weathersense_meter_hanchor", WEATHERSENSE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:2481
  jsonutil.SetIntValue(profile_path, "weathersense_meter_vanchor", WEATHERSENSE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:2482
  jsonutil.SetIntValue(profile_path, "movement_penalty", 2) ; #DEBUG_LINE_NO:2483
  jsonutil.SetIntValue(profile_path, "no_fast_travel", 1) ; #DEBUG_LINE_NO:2484
  jsonutil.SetIntValue(profile_path, "no_waiting", 1) ; #DEBUG_LINE_NO:2485
  jsonutil.SetIntValue(profile_path, "sound_effects", 2) ; #DEBUG_LINE_NO:2486
  jsonutil.SetIntValue(profile_path, "weather_messages", 2) ; #DEBUG_LINE_NO:2487
  jsonutil.SetIntValue(profile_path, "weathersense_display_mode", 2) ; #DEBUG_LINE_NO:2488
  jsonutil.SetIntValue(profile_path, "wet_shader_on", 2) ; #DEBUG_LINE_NO:2489
  jsonutil.SetIntValue(profile_path, "frigid_water_is_lethal", 2) ; #DEBUG_LINE_NO:2490
  jsonutil.SetIntValue(profile_path, "vampire_mode", 1) ; #DEBUG_LINE_NO:2491
  jsonutil.SetIntValue(profile_path, "display_tutorials", 2) ; #DEBUG_LINE_NO:2492
  jsonutil.SetIntValue(profile_path, "hotkey_weathersense", 0) ; #DEBUG_LINE_NO:2493
  jsonutil.Save(profile_path, False) ; #DEBUG_LINE_NO:2495
EndFunction

Function SaveAllSettings(Int aiProfileIndex)
  String profile_path = CONFIG_PATH + "profile" + aiProfileIndex as String ; #DEBUG_LINE_NO:2499
  jsonutil.SetIntValue(profile_path, "profile_version", _Frost_SettingsProfileVersion.GetValueInt()) ; #DEBUG_LINE_NO:2500
  jsonutil.SetIntValue(profile_path, "animation", _Frost_Setting_Animation.GetValueInt()) ; #DEBUG_LINE_NO:2501
  jsonutil.SetIntValue(profile_path, "follower_animation", _Frost_Setting_FollowerAnimation.GetValueInt()) ; #DEBUG_LINE_NO:2502
  jsonutil.SetIntValue(profile_path, "condition_messages", _Frost_Setting_ConditionMessages.GetValueInt()) ; #DEBUG_LINE_NO:2503
  jsonutil.SetIntValue(profile_path, "display_attributes_in_weathersense", _Frost_Setting_DisplayAttributesInWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:2504
  jsonutil.SetIntValue(profile_path, "display_attribute_values_in_weathersense", _Frost_Setting_DisplayAttributeValuesInWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:2505
  jsonutil.SetIntValue(profile_path, "notification_equipmentvalues", _Frost_Setting_Notifications_EquipmentValues.GetValueInt()) ; #DEBUG_LINE_NO:2506
  jsonutil.SetIntValue(profile_path, "notification_equipmentsummary", _Frost_Setting_Notifications_EquipmentSummary.GetValueInt()) ; #DEBUG_LINE_NO:2507
  jsonutil.SetIntValue(profile_path, "exposure_pause_combat", _Frost_Setting_ExposurePauseCombat.GetValueInt()) ; #DEBUG_LINE_NO:2508
  jsonutil.SetIntValue(profile_path, "exposure_pause_dialogue", _Frost_Setting_ExposurePauseDialogue.GetValueInt()) ; #DEBUG_LINE_NO:2509
  jsonutil.SetFloatValue(profile_path, "exposure_rate", _Frost_Setting_ExposureRate.GetValue()) ; #DEBUG_LINE_NO:2510
  jsonutil.SetIntValue(profile_path, "force_feedback", _Frost_Setting_ForceFeedback.GetValueInt()) ; #DEBUG_LINE_NO:2511
  jsonutil.SetIntValue(profile_path, "frost_shader_on", _Frost_Setting_FrostShaderOn.GetValueInt()) ; #DEBUG_LINE_NO:2512
  jsonutil.SetIntValue(profile_path, "full_screen_effects", _Frost_Setting_FullScreenEffects.GetValueInt()) ; #DEBUG_LINE_NO:2513
  jsonutil.SetIntValue(profile_path, "max_exposure_mode", _Frost_Setting_MaxExposureMode.GetValueInt()) ; #DEBUG_LINE_NO:2514
  jsonutil.SetIntValue(profile_path, "meter_display_mode", _Frost_Setting_MeterDisplayMode.GetValueInt()) ; #DEBUG_LINE_NO:2515
  jsonutil.SetIntValue(profile_path, "meter_display_time", _Frost_Setting_MeterDisplayTime.GetValueInt()) ; #DEBUG_LINE_NO:2516
  jsonutil.SetFloatValue(profile_path, "exposure_meter_opacity", _Frost_Setting_MeterExposureOpacity.GetValue()) ; #DEBUG_LINE_NO:2517
  jsonutil.SetIntValue(profile_path, "exposure_meter_color", _Frost_Setting_MeterExposureColor.GetValueInt()) ; #DEBUG_LINE_NO:2518
  jsonutil.SetIntValue(profile_path, "exposure_meter_color_warm", _Frost_Setting_MeterExposureColorWarm.GetValueInt()) ; #DEBUG_LINE_NO:2519
  jsonutil.SetIntValue(profile_path, "exposure_meter_fill_direction", _Frost_Setting_MeterExposureFillDirection.GetValueInt()) ; #DEBUG_LINE_NO:2520
  jsonutil.SetFloatValue(profile_path, "exposure_meter_height", _Frost_Setting_MeterExposureHeight.GetValue()) ; #DEBUG_LINE_NO:2521
  jsonutil.SetFloatValue(profile_path, "exposure_meter_width", _Frost_Setting_MeterExposureWidth.GetValue()) ; #DEBUG_LINE_NO:2522
  jsonutil.SetFloatValue(profile_path, "exposure_meter_xpos", _Frost_Setting_MeterExposureXPos.GetValue()) ; #DEBUG_LINE_NO:2523
  jsonutil.SetFloatValue(profile_path, "exposure_meter_ypos", _Frost_Setting_MeterExposureYPos.GetValue()) ; #DEBUG_LINE_NO:2524
  jsonutil.SetIntValue(profile_path, "exposure_meter_hanchor", _Frost_Setting_MeterExposureHAnchor.GetValueInt()) ; #DEBUG_LINE_NO:2525
  jsonutil.SetIntValue(profile_path, "exposure_meter_vanchor", _Frost_Setting_MeterExposureVAnchor.GetValueInt()) ; #DEBUG_LINE_NO:2526
  jsonutil.SetFloatValue(profile_path, "wetness_meter_opacity", _Frost_Setting_MeterWetnessOpacity.GetValue()) ; #DEBUG_LINE_NO:2527
  jsonutil.SetIntValue(profile_path, "wetness_meter_color", _Frost_Setting_MeterWetnessColor.GetValueInt()) ; #DEBUG_LINE_NO:2528
  jsonutil.SetIntValue(profile_path, "wetness_meter_fill_direction", _Frost_Setting_MeterWetnessFillDirection.GetValueInt()) ; #DEBUG_LINE_NO:2529
  jsonutil.SetFloatValue(profile_path, "wetness_meter_height", _Frost_Setting_MeterWetnessHeight.GetValue()) ; #DEBUG_LINE_NO:2530
  jsonutil.SetFloatValue(profile_path, "wetness_meter_width", _Frost_Setting_MeterWetnessWidth.GetValue()) ; #DEBUG_LINE_NO:2531
  jsonutil.SetFloatValue(profile_path, "wetness_meter_xpos", _Frost_Setting_MeterWetnessXPos.GetValue()) ; #DEBUG_LINE_NO:2532
  jsonutil.SetFloatValue(profile_path, "wetness_meter_ypos", _Frost_Setting_MeterWetnessYPos.GetValue()) ; #DEBUG_LINE_NO:2533
  jsonutil.SetIntValue(profile_path, "wetness_meter_hanchor", _Frost_Setting_MeterWetnessHAnchor.GetValueInt()) ; #DEBUG_LINE_NO:2534
  jsonutil.SetIntValue(profile_path, "wetness_meter_vanchor", _Frost_Setting_MeterWetnessVAnchor.GetValueInt()) ; #DEBUG_LINE_NO:2535
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_opacity", _Frost_Setting_MeterWeathersenseOpacity.GetValue()) ; #DEBUG_LINE_NO:2536
  jsonutil.SetIntValue(profile_path, "weathersense_meter_color", _Frost_Setting_MeterWeathersenseColor.GetValueInt()) ; #DEBUG_LINE_NO:2537
  jsonutil.SetIntValue(profile_path, "weathersense_meter_fill_direction", _Frost_Setting_MeterWeathersenseFillDirection.GetValueInt()) ; #DEBUG_LINE_NO:2538
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_height", _Frost_Setting_MeterWeathersenseHeight.GetValue()) ; #DEBUG_LINE_NO:2539
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_width", _Frost_Setting_MeterWeathersenseWidth.GetValue()) ; #DEBUG_LINE_NO:2540
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_xpos", _Frost_Setting_MeterWeathersenseXPos.GetValue()) ; #DEBUG_LINE_NO:2541
  jsonutil.SetFloatValue(profile_path, "weathersense_meter_ypos", _Frost_Setting_MeterWeathersenseYPos.GetValue()) ; #DEBUG_LINE_NO:2542
  jsonutil.SetIntValue(profile_path, "weathersense_meter_hanchor", _Frost_Setting_MeterWeathersenseHAnchor.GetValueInt()) ; #DEBUG_LINE_NO:2543
  jsonutil.SetIntValue(profile_path, "weathersense_meter_vanchor", _Frost_Setting_MeterWeathersenseVAnchor.GetValueInt()) ; #DEBUG_LINE_NO:2544
  jsonutil.SetIntValue(profile_path, "movement_penalty", _Frost_Setting_MovementPenalty.GetValueInt()) ; #DEBUG_LINE_NO:2545
  jsonutil.SetIntValue(profile_path, "no_fast_travel", _Frost_Setting_NoFastTravel.GetValueInt()) ; #DEBUG_LINE_NO:2546
  jsonutil.SetIntValue(profile_path, "no_waiting", _Frost_Setting_NoWaiting.GetValueInt()) ; #DEBUG_LINE_NO:2547
  jsonutil.SetIntValue(profile_path, "sound_effects", _Frost_Setting_SoundEffects.GetValueInt()) ; #DEBUG_LINE_NO:2548
  jsonutil.SetIntValue(profile_path, "weather_messages", _Frost_Setting_WeatherMessages.GetValueInt()) ; #DEBUG_LINE_NO:2549
  jsonutil.SetIntValue(profile_path, "weathersense_display_mode", _Frost_Setting_WeathersenseDisplayMode.GetValueInt()) ; #DEBUG_LINE_NO:2550
  jsonutil.SetIntValue(profile_path, "wet_shader_on", _Frost_Setting_WetShaderOn.GetValueInt()) ; #DEBUG_LINE_NO:2551
  jsonutil.SetIntValue(profile_path, "frigid_water_is_lethal", _Frost_Setting_FrigidWaterIsLethal.GetValueInt()) ; #DEBUG_LINE_NO:2552
  jsonutil.SetIntValue(profile_path, "vampire_mode", _Frost_Setting_VampireMode.GetValueInt()) ; #DEBUG_LINE_NO:2553
  jsonutil.SetIntValue(profile_path, "display_tutorials", _Frost_Setting_DisplayTutorials.GetValueInt()) ; #DEBUG_LINE_NO:2554
  jsonutil.SetIntValue(profile_path, "hotkey_weathersense", _Frost_HotkeyWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:2555
  jsonutil.Save(profile_path, False) ; #DEBUG_LINE_NO:2556
EndFunction

Function CleanProfile(Int aiProfileIndex)
  String profile_path = CONFIG_PATH + "profile" + aiProfileIndex as String ; #DEBUG_LINE_NO:2560
  Bool result = jsonutil.UnsetIntValue(profile_path, "1P_animation_allowed") ; #DEBUG_LINE_NO:2563
  result = jsonutil.UnsetIntValue(profile_path, "meter_opacity") ; #DEBUG_LINE_NO:2564
  result = jsonutil.UnsetIntValue(profile_path, "meter_aspect_ratio") ; #DEBUG_LINE_NO:2565
  jsonutil.Save(profile_path, False) ; #DEBUG_LINE_NO:2566
EndFunction

Function ShowProfileHelp()
  Self.ShowMessage("$FrostfallSaveLoadTopic", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2570
  Self.ShowMessage("$FrostfallSaveLoadTopicCont", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2571
  Self.ShowMessage("$FrostfallSaveLoadTopicCont2", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2572
EndFunction

Function SendEvent_StartFrostfall()
  Int handle = modevent.Create("Frost_StartFrostfall") ; #DEBUG_LINE_NO:2576
  If handle ; #DEBUG_LINE_NO:2577
    modevent.PushBool(handle, False) ; #DEBUG_LINE_NO:2578
    modevent.Send(handle) ; #DEBUG_LINE_NO:2579
  EndIf
EndFunction

Function SendEvent_StopFrostfall()
  Int handle = modevent.Create("Frost_StopFrostfall") ; #DEBUG_LINE_NO:2584
  If handle ; #DEBUG_LINE_NO:2585
    modevent.Send(handle) ; #DEBUG_LINE_NO:2586
  EndIf
EndFunction

Function RegisterForKeysOnLoad()
  If _Frost_HotkeyWeathersense.GetValueInt() != 0 ; #DEBUG_LINE_NO:2591
    Self.RegisterForKey(_Frost_HotkeyWeathersense.GetValueInt()) ; #DEBUG_LINE_NO:2592
  EndIf
EndFunction

Function ClearEndurancePerks()
  _Frost_PerkRank_Adaptation.SetValueInt(0) ; #DEBUG_LINE_NO:2597
  _Frost_PerkRank_FrostWarding.SetValueInt(0) ; #DEBUG_LINE_NO:2598
  _Frost_PerkRank_GlacialSwimmer.SetValueInt(0) ; #DEBUG_LINE_NO:2599
  _Frost_PerkRank_InnerFire.SetValueInt(0) ; #DEBUG_LINE_NO:2600
  _Frost_PerkRank_WellInsulated.SetValueInt(0) ; #DEBUG_LINE_NO:2601
  _Frost_PerkRank_Windbreaker.SetValueInt(0) ; #DEBUG_LINE_NO:2602
EndFunction

Function RefundEnduranceSkillPoints()
  Self.ClearEndurancePerks() ; #DEBUG_LINE_NO:2606
  EndurancePerkPoints.SetValueInt(EndurancePerkPointsEarned.GetValueInt()) ; #DEBUG_LINE_NO:2607
  EndurancePerkPointProgress.SetValue(0.0) ; #DEBUG_LINE_NO:2608
EndFunction

Function GenerateEquipmentPage()
  Self.SetCursorFillMode(Self.TOP_TO_BOTTOM) ; #DEBUG_LINE_NO:2612
  Self.SetCursorPosition(0) ; #DEBUG_LINE_NO:2614
  ArmorPage_cursor_position = 0 ; #DEBUG_LINE_NO:2615
  _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:2617
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2618
  Armor[] worn_armor = Self.GetAllWornArmor() ; #DEBUG_LINE_NO:2619
  ArmorMenuEntries = new Armor[128] ; #DEBUG_LINE_NO:2621
  ArmorTypeIDs = new Int[128] ; #DEBUG_LINE_NO:2622
  Armor_WarmthSliderOIDs = new Int[128] ; #DEBUG_LINE_NO:2623
  Armor_CoverageSliderOIDs = new Int[128] ; #DEBUG_LINE_NO:2624
  Armor_GearTypeOIDs = new Int[128] ; #DEBUG_LINE_NO:2625
  Armor_ModifyPartsOIDs = new Int[128] ; #DEBUG_LINE_NO:2626
  Armor_SetProtectionOIDs = new Int[128] ; #DEBUG_LINE_NO:2627
  Armor_DefaultArmorEntryOIDs = new Int[128] ; #DEBUG_LINE_NO:2628
  Int armor_count = commonarrayhelper.ArrayCountArmor(worn_armor) ; #DEBUG_LINE_NO:2630
  Int i = 0 ; #DEBUG_LINE_NO:2632
  Int j = 0 ; #DEBUG_LINE_NO:2633
  If armor_count == 0 ; #DEBUG_LINE_NO:2635
    Self.AddTextOption("$FrostfallArmorNoGear", "", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:2636
    ArmorPage_cursor_position += 2 ; #DEBUG_LINE_NO:2637
  EndIf
  While i < armor_count ; #DEBUG_LINE_NO:2640
    Int[] armor_data = handler.GetArmorProtectionData(worn_armor[i]) ; #DEBUG_LINE_NO:2641
    Int disable_if_ignored = 0 ; #DEBUG_LINE_NO:2643
    If armor_data[0] == handler.GEARTYPE_IGNORE ; #DEBUG_LINE_NO:2644
      disable_if_ignored = Self.OPTION_FLAG_DISABLED ; #DEBUG_LINE_NO:2645
    EndIf
    Self.GenerateEquipmentPageEntry(j, worn_armor[i], armor_data[0], armor_data[1], armor_data[2], True, disable_if_ignored, handler) ; #DEBUG_LINE_NO:2649
    j += 1 ; #DEBUG_LINE_NO:2650
    If armor_data[3] > 0 || armor_data[4] > 0 ; #DEBUG_LINE_NO:2653
      Self.GenerateEquipmentPageEntry(j, worn_armor[i], handler.GEARTYPE_BODY, armor_data[3], armor_data[4], False, disable_if_ignored, handler) ; #DEBUG_LINE_NO:2654
      j += 1 ; #DEBUG_LINE_NO:2655
    EndIf
    If armor_data[5] > 0 || armor_data[6] > 0 ; #DEBUG_LINE_NO:2659
      Self.GenerateEquipmentPageEntry(j, worn_armor[i], handler.GEARTYPE_HEAD, armor_data[5], armor_data[6], False, disable_if_ignored, handler) ; #DEBUG_LINE_NO:2660
      j += 1 ; #DEBUG_LINE_NO:2661
    EndIf
    If armor_data[7] > 0 || armor_data[8] > 0 ; #DEBUG_LINE_NO:2665
      Self.GenerateEquipmentPageEntry(j, worn_armor[i], handler.GEARTYPE_HANDS, armor_data[7], armor_data[8], False, disable_if_ignored, handler) ; #DEBUG_LINE_NO:2666
      j += 1 ; #DEBUG_LINE_NO:2667
    EndIf
    If armor_data[9] > 0 || armor_data[10] > 0 ; #DEBUG_LINE_NO:2671
      Self.GenerateEquipmentPageEntry(j, worn_armor[i], handler.GEARTYPE_FEET, armor_data[9], armor_data[10], False, disable_if_ignored, handler) ; #DEBUG_LINE_NO:2672
      j += 1 ; #DEBUG_LINE_NO:2673
    EndIf
    If armor_data[11] > 0 || armor_data[12] > 0 ; #DEBUG_LINE_NO:2677
      Self.GenerateEquipmentPageEntry(j, worn_armor[i], handler.GEARTYPE_CLOAK, armor_data[11], armor_data[12], False, disable_if_ignored, handler) ; #DEBUG_LINE_NO:2678
      j += 1 ; #DEBUG_LINE_NO:2679
    EndIf
    If armor_data[13] > 0 || armor_data[14] > 0 ; #DEBUG_LINE_NO:2683
      Self.GenerateEquipmentPageEntry(j, worn_armor[i], handler.GEARTYPE_MISC, armor_data[13], armor_data[14], False, disable_if_ignored, handler) ; #DEBUG_LINE_NO:2684
      j += 1 ; #DEBUG_LINE_NO:2685
    EndIf
    i += 1 ; #DEBUG_LINE_NO:2687
  EndWhile
  Self.GenerateEquipmentPageFooter() ; #DEBUG_LINE_NO:2690
EndFunction

Function GenerateEquipmentPageEntry(Int aiArrayIndex, Armor akArmor, Int aiType, Int akWarmth, Int akCoverage, Bool abIsMainPart, Int aiDisableIfIgnored, _frost_armorprotectiondatastorehandler akHandler)
  Self.SetCursorPosition(ArmorPage_cursor_position) ; #DEBUG_LINE_NO:2696
  ArmorMenuEntries[aiArrayIndex] = akArmor ; #DEBUG_LINE_NO:2698
  If aiDisableIfIgnored as Bool ; #DEBUG_LINE_NO:2700
    akWarmth = 0 ; #DEBUG_LINE_NO:2701
    akCoverage = 0 ; #DEBUG_LINE_NO:2702
  EndIf
  String display_name = akArmor.GetName() ; #DEBUG_LINE_NO:2705
  If display_name == "" ; #DEBUG_LINE_NO:2706
    display_name = Self.GetUnnamedTypeString(akArmor, aiType, akHandler) ; #DEBUG_LINE_NO:2707
  EndIf
  If abIsMainPart ; #DEBUG_LINE_NO:2710
    Self.AddHeaderOption(display_name, 0) ; #DEBUG_LINE_NO:2711
    ArmorTypeIDs[aiArrayIndex] = 0 ; #DEBUG_LINE_NO:2712
  Else
    Self.AddHeaderOption(display_name + Self.GetExtraPartTypeString(aiType, akHandler), 0) ; #DEBUG_LINE_NO:2714
    ArmorTypeIDs[aiArrayIndex] = aiType ; #DEBUG_LINE_NO:2715
  EndIf
  If abIsMainPart ; #DEBUG_LINE_NO:2718
    Armor_GearTypeOIDs[aiArrayIndex] = Self.AddMenuOption("$FrostfallArmorType", Self.GetTypeString(aiType, akHandler), 0) ; #DEBUG_LINE_NO:2719
  Else
    Armor_GearTypeOIDs[aiArrayIndex] = Self.AddMenuOption("$FrostfallArmorType", Self.GetTypeString(aiType, akHandler), Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:2721
  EndIf
  Armor_WarmthSliderOIDs[aiArrayIndex] = Self.AddSliderOption("$FrostfallOverviewWarmthValue", akWarmth as Float, "{0}", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:2724
  Armor_CoverageSliderOIDs[aiArrayIndex] = Self.AddSliderOption("$FrostfallOverviewCoverageValue", akCoverage as Float, "{0}", Self.OPTION_FLAG_DISABLED) ; #DEBUG_LINE_NO:2725
  Armor_SetProtectionOIDs[aiArrayIndex] = Self.AddMenuOption("$FrostfallArmorSetProtection", "", aiDisableIfIgnored) ; #DEBUG_LINE_NO:2726
  If abIsMainPart ; #DEBUG_LINE_NO:2728
    Armor_ModifyPartsOIDs[aiArrayIndex] = Self.AddMenuOption("$FrostfallArmorExtraParts", "", aiDisableIfIgnored) ; #DEBUG_LINE_NO:2729
  Else
    Self.AddEmptyOption() ; #DEBUG_LINE_NO:2731
  EndIf
  If commonhelperfunctions.IsEven(ArmorPage_cursor_position) ; #DEBUG_LINE_NO:2735
    ArmorPage_cursor_position += 1 ; #DEBUG_LINE_NO:2736
  Else
    ArmorPage_cursor_position += 11 ; #DEBUG_LINE_NO:2738
  EndIf
EndFunction

Function GenerateEquipmentPageFooter()
  If !commonhelperfunctions.IsEven(ArmorPage_cursor_position) ; #DEBUG_LINE_NO:2743
    ArmorPage_cursor_position += 11 ; #DEBUG_LINE_NO:2744
  EndIf
  Self.SetCursorPosition(ArmorPage_cursor_position) ; #DEBUG_LINE_NO:2747
  Self.SetCursorFillMode(Self.LEFT_TO_RIGHT) ; #DEBUG_LINE_NO:2748
  Self.AddHeaderOption("$FrostfallArmorHeaderOptions", 0) ; #DEBUG_LINE_NO:2749
  Self.AddHeaderOption("$FrostfallArmorHeaderInfo", 0) ; #DEBUG_LINE_NO:2750
  Armor_RepairDefaultsOID = Self.AddTextOption("$FrostfallArmorRepairDefaultData", "", 0) ; #DEBUG_LINE_NO:2751
  Armor_ShowTutorialOID = Self.AddTextOption("$FrostfallArmorTutorial", "", 0) ; #DEBUG_LINE_NO:2752
  Armor_DefaultWornArmorOID = Self.AddTextOption("$FrostfallArmorDefaultWorn", "", 0) ; #DEBUG_LINE_NO:2753
  Self.AddEmptyOption() ; #DEBUG_LINE_NO:2754
  Armor_DefaultAllArmorOID = Self.AddTextOption("$FrostfallArmorDefaultAll", "", 0) ; #DEBUG_LINE_NO:2755
EndFunction

Function ModifyGearProtection(Int aiOidIndex, Int aiChoice)
  If aiChoice == 27 || aiChoice == -1 ; #DEBUG_LINE_NO:2760
    Return  ; #DEBUG_LINE_NO:2761
  EndIf
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:2764
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2765
  If aiChoice == 27 ; #DEBUG_LINE_NO:2768
    Return  ; #DEBUG_LINE_NO:2770
  ElseIf aiChoice == 26 ; #DEBUG_LINE_NO:2771
    Bool confirmed = Self.ShowMessage("$FrostfallArmorDefaultConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2773
    If confirmed ; #DEBUG_LINE_NO:2774
      handler.RestoreDefaultArmorData(the_armor) ; #DEBUG_LINE_NO:2775
      Self.ArmorPageReset(True) ; #DEBUG_LINE_NO:2776
      Self.RefreshSingleItemValues(the_armor) ; #DEBUG_LINE_NO:2777
      Return  ; #DEBUG_LINE_NO:2778
    EndIf
  ElseIf aiChoice == 25 ; #DEBUG_LINE_NO:2780
    Self.SetOptionFlags(Armor_WarmthSliderOIDs[aiOidIndex], 0, False) ; #DEBUG_LINE_NO:2782
    Self.SetOptionFlags(Armor_CoverageSliderOIDs[aiOidIndex], 0, False) ; #DEBUG_LINE_NO:2783
    Return  ; #DEBUG_LINE_NO:2784
  Else
    Int new_warmth = 0 ; #DEBUG_LINE_NO:2786
    Int new_coverage = 0 ; #DEBUG_LINE_NO:2787
    Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:2789
    Int type = armor_data[0] ; #DEBUG_LINE_NO:2790
    If aiChoice == 23 ; #DEBUG_LINE_NO:2792
      new_warmth = 40 ; #DEBUG_LINE_NO:2793
      new_coverage = 12 ; #DEBUG_LINE_NO:2794
    ElseIf aiChoice == 22 ; #DEBUG_LINE_NO:2795
      new_warmth = 12 ; #DEBUG_LINE_NO:2796
      new_coverage = 40 ; #DEBUG_LINE_NO:2797
    ElseIf aiChoice == 21 ; #DEBUG_LINE_NO:2798
      new_warmth = 12 ; #DEBUG_LINE_NO:2799
      new_coverage = 12 ; #DEBUG_LINE_NO:2800
    ElseIf aiChoice == 20 ; #DEBUG_LINE_NO:2801
      new_warmth = 6 ; #DEBUG_LINE_NO:2802
      new_coverage = 12 ; #DEBUG_LINE_NO:2803
    ElseIf aiChoice == 19 ; #DEBUG_LINE_NO:2804
      new_warmth = 12 ; #DEBUG_LINE_NO:2805
      new_coverage = 6 ; #DEBUG_LINE_NO:2806
    Else
      Int wdx = ProtectionListWarmthIndex[aiChoice] ; #DEBUG_LINE_NO:2808
      Int cdx = ProtectionListCoverageIndex[aiChoice] ; #DEBUG_LINE_NO:2809
      If wdx == -1 ; #DEBUG_LINE_NO:2811
        Self.ShowMessage("$FrostfallArmorInvalidOption", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:2812
        Return  ; #DEBUG_LINE_NO:2813
      EndIf
      If type == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:2816
        new_warmth = handler.StandardBodyValues[wdx] ; #DEBUG_LINE_NO:2817
        If cdx == -2 ; #DEBUG_LINE_NO:2818
          new_coverage = 0 ; #DEBUG_LINE_NO:2819
        Else
          new_coverage = handler.StandardBodyValues[cdx] ; #DEBUG_LINE_NO:2821
        EndIf
      ElseIf type == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:2823
        new_warmth = handler.StandardHeadValues[wdx] ; #DEBUG_LINE_NO:2824
        If cdx == -2 ; #DEBUG_LINE_NO:2825
          new_coverage = 0 ; #DEBUG_LINE_NO:2826
        Else
          new_coverage = handler.StandardHeadValues[cdx] ; #DEBUG_LINE_NO:2828
        EndIf
      ElseIf type == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:2830
        new_warmth = handler.StandardHandsValues[wdx] ; #DEBUG_LINE_NO:2831
        If cdx == -2 ; #DEBUG_LINE_NO:2832
          new_coverage = 0 ; #DEBUG_LINE_NO:2833
        Else
          new_coverage = handler.StandardHandsValues[cdx] ; #DEBUG_LINE_NO:2835
        EndIf
      ElseIf type == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:2837
        new_warmth = handler.StandardFeetValues[wdx] ; #DEBUG_LINE_NO:2838
        If cdx == -2 ; #DEBUG_LINE_NO:2839
          new_coverage = 0 ; #DEBUG_LINE_NO:2840
        Else
          new_coverage = handler.StandardFeetValues[cdx] ; #DEBUG_LINE_NO:2842
        EndIf
      ElseIf type == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:2844
        new_warmth = handler.StandardCloakValues[wdx] ; #DEBUG_LINE_NO:2845
        If cdx == -2 ; #DEBUG_LINE_NO:2846
          new_coverage = 0 ; #DEBUG_LINE_NO:2847
        Else
          new_coverage = handler.StandardCloakValues[cdx] ; #DEBUG_LINE_NO:2849
        EndIf
      ElseIf type == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:2851
        new_warmth = handler.StandardMiscValues[wdx] ; #DEBUG_LINE_NO:2852
        If cdx == -2 ; #DEBUG_LINE_NO:2853
          new_coverage = 0 ; #DEBUG_LINE_NO:2854
        Else
          new_coverage = handler.StandardMiscValues[cdx] ; #DEBUG_LINE_NO:2856
        EndIf
      Else
        Return  ; #DEBUG_LINE_NO:2860
      EndIf
    EndIf
    If ArmorTypeIDs[aiOidIndex] == 0 ; #DEBUG_LINE_NO:2865
      armor_data[1] = new_warmth ; #DEBUG_LINE_NO:2866
      armor_data[2] = new_coverage ; #DEBUG_LINE_NO:2867
    ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:2868
      armor_data[3] = new_warmth ; #DEBUG_LINE_NO:2869
      armor_data[4] = new_coverage ; #DEBUG_LINE_NO:2870
    ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:2871
      armor_data[5] = new_warmth ; #DEBUG_LINE_NO:2872
      armor_data[6] = new_coverage ; #DEBUG_LINE_NO:2873
    ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:2874
      armor_data[7] = new_warmth ; #DEBUG_LINE_NO:2875
      armor_data[8] = new_coverage ; #DEBUG_LINE_NO:2876
    ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:2877
      armor_data[9] = new_warmth ; #DEBUG_LINE_NO:2878
      armor_data[10] = new_coverage ; #DEBUG_LINE_NO:2879
    ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:2880
      armor_data[11] = new_warmth ; #DEBUG_LINE_NO:2881
      armor_data[12] = new_coverage ; #DEBUG_LINE_NO:2882
    ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:2883
      armor_data[13] = new_warmth ; #DEBUG_LINE_NO:2884
      armor_data[14] = new_coverage ; #DEBUG_LINE_NO:2885
    EndIf
    handler.UpdateArmorDataA(the_armor, armor_data) ; #DEBUG_LINE_NO:2888
    Self.SetSliderOptionValue(Armor_WarmthSliderOIDs[aiOidIndex], new_warmth as Float, "{0}", True) ; #DEBUG_LINE_NO:2891
    Self.SetSliderOptionValue(Armor_CoverageSliderOIDs[aiOidIndex], new_coverage as Float, "{0}", False) ; #DEBUG_LINE_NO:2892
    Self.RefreshSingleItemValues(the_armor) ; #DEBUG_LINE_NO:2895
  EndIf
EndFunction

Function SetWarmthSlider(Int aiOidIndex)
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:2900
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2901
  Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:2902
  Float start_value = 0.0 ; #DEBUG_LINE_NO:2904
  If ArmorTypeIDs[aiOidIndex] == 0 ; #DEBUG_LINE_NO:2905
    start_value = armor_data[1] as Float ; #DEBUG_LINE_NO:2906
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:2907
    start_value = armor_data[3] as Float ; #DEBUG_LINE_NO:2908
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:2909
    start_value = armor_data[5] as Float ; #DEBUG_LINE_NO:2910
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:2911
    start_value = armor_data[7] as Float ; #DEBUG_LINE_NO:2912
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:2913
    start_value = armor_data[9] as Float ; #DEBUG_LINE_NO:2914
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:2915
    start_value = armor_data[11] as Float ; #DEBUG_LINE_NO:2916
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:2917
    start_value = armor_data[13] as Float ; #DEBUG_LINE_NO:2918
  EndIf
  Self.SetSliderDialogStartValue(start_value) ; #DEBUG_LINE_NO:2921
  Self.SetSliderDialogDefaultValue(start_value) ; #DEBUG_LINE_NO:2922
  Self.SetSliderDialogRange(1.0, _Frost_Calc_MaxWarmth.GetValue()) ; #DEBUG_LINE_NO:2923
  Self.SetSliderDialogInterval(1.0) ; #DEBUG_LINE_NO:2924
EndFunction

Function SetCoverageSlider(Int aiOidIndex)
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:2928
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2929
  Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:2930
  Float start_value = 0.0 ; #DEBUG_LINE_NO:2932
  If ArmorTypeIDs[aiOidIndex] == 0 ; #DEBUG_LINE_NO:2933
    start_value = armor_data[2] as Float ; #DEBUG_LINE_NO:2934
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:2935
    start_value = armor_data[4] as Float ; #DEBUG_LINE_NO:2936
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:2937
    start_value = armor_data[6] as Float ; #DEBUG_LINE_NO:2938
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:2939
    start_value = armor_data[8] as Float ; #DEBUG_LINE_NO:2940
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:2941
    start_value = armor_data[10] as Float ; #DEBUG_LINE_NO:2942
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:2943
    start_value = armor_data[12] as Float ; #DEBUG_LINE_NO:2944
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:2945
    start_value = armor_data[14] as Float ; #DEBUG_LINE_NO:2946
  EndIf
  Self.SetSliderDialogStartValue(start_value) ; #DEBUG_LINE_NO:2949
  Self.SetSliderDialogDefaultValue(start_value) ; #DEBUG_LINE_NO:2950
  Self.SetSliderDialogRange(1.0, _Frost_Calc_MaxCoverage.GetValue()) ; #DEBUG_LINE_NO:2951
  Self.SetSliderDialogInterval(1.0) ; #DEBUG_LINE_NO:2952
EndFunction

Function ModifyGearWarmth(Int aiOidIndex, Int aiValue)
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:2956
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2957
  Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:2958
  If ArmorTypeIDs[aiOidIndex] == 0 ; #DEBUG_LINE_NO:2961
    armor_data[1] = aiValue ; #DEBUG_LINE_NO:2962
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:2963
    armor_data[3] = aiValue ; #DEBUG_LINE_NO:2964
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:2965
    armor_data[5] = aiValue ; #DEBUG_LINE_NO:2966
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:2967
    armor_data[7] = aiValue ; #DEBUG_LINE_NO:2968
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:2969
    armor_data[9] = aiValue ; #DEBUG_LINE_NO:2970
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:2971
    armor_data[11] = aiValue ; #DEBUG_LINE_NO:2972
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:2973
    armor_data[13] = aiValue ; #DEBUG_LINE_NO:2974
  EndIf
  handler.UpdateArmorDataA(the_armor, armor_data) ; #DEBUG_LINE_NO:2977
  Self.SetSliderOptionValue(Armor_WarmthSliderOIDs[aiOidIndex], aiValue as Float, "{0}", False) ; #DEBUG_LINE_NO:2980
  Self.RefreshSingleItemValues(the_armor) ; #DEBUG_LINE_NO:2983
EndFunction

Function ModifyGearCoverage(Int aiOidIndex, Int aiValue)
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:2987
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2988
  Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:2989
  If ArmorTypeIDs[aiOidIndex] == 0 ; #DEBUG_LINE_NO:2992
    armor_data[2] = aiValue ; #DEBUG_LINE_NO:2993
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:2994
    armor_data[4] = aiValue ; #DEBUG_LINE_NO:2995
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:2996
    armor_data[6] = aiValue ; #DEBUG_LINE_NO:2997
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:2998
    armor_data[8] = aiValue ; #DEBUG_LINE_NO:2999
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:3000
    armor_data[10] = aiValue ; #DEBUG_LINE_NO:3001
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:3002
    armor_data[12] = aiValue ; #DEBUG_LINE_NO:3003
  ElseIf ArmorTypeIDs[aiOidIndex] == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:3004
    armor_data[14] = aiValue ; #DEBUG_LINE_NO:3005
  EndIf
  handler.UpdateArmorDataA(the_armor, armor_data) ; #DEBUG_LINE_NO:3008
  Self.SetSliderOptionValue(Armor_CoverageSliderOIDs[aiOidIndex], aiValue as Float, "{0}", False) ; #DEBUG_LINE_NO:3011
  Self.RefreshSingleItemValues(the_armor) ; #DEBUG_LINE_NO:3014
EndFunction

Function ModifyGearType(Int aiOidIndex, Int aiChoice)
  If aiChoice == 7 || aiChoice == -1 ; #DEBUG_LINE_NO:3018
    Return  ; #DEBUG_LINE_NO:3019
  EndIf
  Bool confirmed = Self.ShowMessage("$FrostfallArmorTypeConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3022
  If !confirmed ; #DEBUG_LINE_NO:3023
    Return  ; #DEBUG_LINE_NO:3024
  EndIf
  Self.SetMenuOptionValue(Armor_GearTypeOIDs[aiOidIndex], GearTypeList[aiChoice], False) ; #DEBUG_LINE_NO:3027
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:3028
  Int chosen_type = aiChoice + 1 ; #DEBUG_LINE_NO:3029
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:3030
  Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:3031
  armor_data[0] = chosen_type ; #DEBUG_LINE_NO:3033
  If chosen_type == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:3036
    armor_data[3] = 0 ; #DEBUG_LINE_NO:3037
    armor_data[4] = 0 ; #DEBUG_LINE_NO:3038
  ElseIf chosen_type == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:3039
    armor_data[5] = 0 ; #DEBUG_LINE_NO:3040
    armor_data[6] = 0 ; #DEBUG_LINE_NO:3041
  ElseIf chosen_type == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:3042
    armor_data[7] = 0 ; #DEBUG_LINE_NO:3043
    armor_data[8] = 0 ; #DEBUG_LINE_NO:3044
  ElseIf chosen_type == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:3045
    armor_data[9] = 0 ; #DEBUG_LINE_NO:3046
    armor_data[10] = 0 ; #DEBUG_LINE_NO:3047
  ElseIf chosen_type == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:3048
    armor_data[11] = 0 ; #DEBUG_LINE_NO:3049
    armor_data[12] = 0 ; #DEBUG_LINE_NO:3050
  ElseIf chosen_type == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:3051
    armor_data[13] = 0 ; #DEBUG_LINE_NO:3052
    armor_data[14] = 0 ; #DEBUG_LINE_NO:3053
  EndIf
  handler.UpdateArmorDataA(the_armor, armor_data) ; #DEBUG_LINE_NO:3056
  Self.ArmorPageReset(True) ; #DEBUG_LINE_NO:3057
  Self.RefreshSingleItemValues(the_armor) ; #DEBUG_LINE_NO:3058
EndFunction

String[] Function GetExtraPartChoiceList(Int aiOidIndex)
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:3062
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:3063
  Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:3064
  Int type = armor_data[0] ; #DEBUG_LINE_NO:3065
  String[] choice_list = new String[7] ; #DEBUG_LINE_NO:3067
  If type == handler.GEARTYPE_BODY ; #DEBUG_LINE_NO:3069
    choice_list[0] = "..." ; #DEBUG_LINE_NO:3070
  ElseIf armor_data[3] > 0 || armor_data[4] > 0 ; #DEBUG_LINE_NO:3072
    choice_list[0] = "$FrostfallArmorExtraPartsRemoveBody" ; #DEBUG_LINE_NO:3073
  Else
    choice_list[0] = "$FrostfallArmorExtraPartsAddBody" ; #DEBUG_LINE_NO:3075
  EndIf
  If type == handler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:3079
    choice_list[1] = "..." ; #DEBUG_LINE_NO:3080
  ElseIf armor_data[5] > 0 || armor_data[6] > 0 ; #DEBUG_LINE_NO:3082
    choice_list[1] = "$FrostfallArmorExtraPartsRemoveHead" ; #DEBUG_LINE_NO:3083
  Else
    choice_list[1] = "$FrostfallArmorExtraPartsAddHead" ; #DEBUG_LINE_NO:3085
  EndIf
  If type == handler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:3089
    choice_list[2] = "..." ; #DEBUG_LINE_NO:3090
  ElseIf armor_data[7] > 0 || armor_data[8] > 0 ; #DEBUG_LINE_NO:3092
    choice_list[2] = "$FrostfallArmorExtraPartsRemoveHands" ; #DEBUG_LINE_NO:3093
  Else
    choice_list[2] = "$FrostfallArmorExtraPartsAddHands" ; #DEBUG_LINE_NO:3095
  EndIf
  If type == handler.GEARTYPE_FEET ; #DEBUG_LINE_NO:3099
    choice_list[3] = "..." ; #DEBUG_LINE_NO:3100
  ElseIf armor_data[9] > 0 || armor_data[10] > 0 ; #DEBUG_LINE_NO:3102
    choice_list[3] = "$FrostfallArmorExtraPartsRemoveFeet" ; #DEBUG_LINE_NO:3103
  Else
    choice_list[3] = "$FrostfallArmorExtraPartsAddFeet" ; #DEBUG_LINE_NO:3105
  EndIf
  If type == handler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:3109
    choice_list[4] = "..." ; #DEBUG_LINE_NO:3110
  ElseIf armor_data[11] > 0 || armor_data[12] > 0 ; #DEBUG_LINE_NO:3112
    choice_list[4] = "$FrostfallArmorExtraPartsRemoveCloak" ; #DEBUG_LINE_NO:3113
  Else
    choice_list[4] = "$FrostfallArmorExtraPartsAddCloak" ; #DEBUG_LINE_NO:3115
  EndIf
  If type == handler.GEARTYPE_MISC ; #DEBUG_LINE_NO:3119
    choice_list[5] = "..." ; #DEBUG_LINE_NO:3120
  ElseIf armor_data[13] > 0 || armor_data[14] > 0 ; #DEBUG_LINE_NO:3122
    choice_list[5] = "$FrostfallArmorExtraPartsRemoveMisc" ; #DEBUG_LINE_NO:3123
  Else
    choice_list[5] = "$FrostfallArmorExtraPartsAddMisc" ; #DEBUG_LINE_NO:3125
  EndIf
  choice_list[6] = "$FrostfallCancel" ; #DEBUG_LINE_NO:3129
  Return choice_list ; #DEBUG_LINE_NO:3130
EndFunction

Function ModifyGearExtraParts(Int aiOidIndex, Int aiChoice)
  If aiChoice == 6 || aiChoice == -1 ; #DEBUG_LINE_NO:3134
    Return  ; #DEBUG_LINE_NO:3135
  EndIf
  Bool confirmed = Self.ShowMessage("$FrostfallArmorExtraPartsConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3138
  If !confirmed ; #DEBUG_LINE_NO:3139
    Return  ; #DEBUG_LINE_NO:3140
  EndIf
  Armor the_armor = ArmorMenuEntries[aiOidIndex] ; #DEBUG_LINE_NO:3143
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:3144
  Int[] armor_data = handler.GetArmorProtectionData(the_armor) ; #DEBUG_LINE_NO:3145
  Int type = armor_data[0] ; #DEBUG_LINE_NO:3146
  If aiChoice + 1 == type ; #DEBUG_LINE_NO:3148
    Self.ShowMessage("$FrostfallArmorInvalidOption", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3149
    Return  ; #DEBUG_LINE_NO:3150
  EndIf
  If aiChoice == 0 ; #DEBUG_LINE_NO:3153
    If armor_data[3] > 0 || armor_data[4] > 0 ; #DEBUG_LINE_NO:3154
      armor_data[3] = 0 ; #DEBUG_LINE_NO:3155
      armor_data[4] = 0 ; #DEBUG_LINE_NO:3156
    Else
      armor_data[3] = 1 ; #DEBUG_LINE_NO:3158
    EndIf
  ElseIf aiChoice == 1 ; #DEBUG_LINE_NO:3160
    If armor_data[5] > 0 || armor_data[6] > 0 ; #DEBUG_LINE_NO:3161
      armor_data[5] = 0 ; #DEBUG_LINE_NO:3162
      armor_data[6] = 0 ; #DEBUG_LINE_NO:3163
    Else
      armor_data[5] = 1 ; #DEBUG_LINE_NO:3165
    EndIf
  ElseIf aiChoice == 2 ; #DEBUG_LINE_NO:3167
    If armor_data[7] > 0 || armor_data[8] > 0 ; #DEBUG_LINE_NO:3168
      armor_data[7] = 0 ; #DEBUG_LINE_NO:3169
      armor_data[8] = 0 ; #DEBUG_LINE_NO:3170
    Else
      armor_data[7] = 1 ; #DEBUG_LINE_NO:3172
    EndIf
  ElseIf aiChoice == 3 ; #DEBUG_LINE_NO:3174
    If armor_data[9] > 0 || armor_data[10] > 0 ; #DEBUG_LINE_NO:3175
      armor_data[9] = 0 ; #DEBUG_LINE_NO:3176
      armor_data[10] = 0 ; #DEBUG_LINE_NO:3177
    Else
      armor_data[9] = 1 ; #DEBUG_LINE_NO:3179
    EndIf
  ElseIf aiChoice == 4 ; #DEBUG_LINE_NO:3181
    If armor_data[11] > 0 || armor_data[12] > 0 ; #DEBUG_LINE_NO:3182
      armor_data[11] = 0 ; #DEBUG_LINE_NO:3183
      armor_data[12] = 0 ; #DEBUG_LINE_NO:3184
    Else
      armor_data[11] = 1 ; #DEBUG_LINE_NO:3186
    EndIf
  ElseIf aiChoice == 5 ; #DEBUG_LINE_NO:3188
    If armor_data[13] > 0 || armor_data[14] > 0 ; #DEBUG_LINE_NO:3189
      armor_data[13] = 0 ; #DEBUG_LINE_NO:3190
      armor_data[14] = 0 ; #DEBUG_LINE_NO:3191
    Else
      armor_data[13] = 1 ; #DEBUG_LINE_NO:3193
    EndIf
  EndIf
  handler.UpdateArmorDataA(the_armor, armor_data) ; #DEBUG_LINE_NO:3197
  Self.ArmorPageReset(True) ; #DEBUG_LINE_NO:3198
  Self.RefreshSingleItemValues(the_armor) ; #DEBUG_LINE_NO:3199
EndFunction

Function RepairArmorDefaults()
  Bool confirmed = Self.ShowMessage("$FrostfallArmorRepairDefaultDataConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3203
  If !confirmed ; #DEBUG_LINE_NO:3204
    Return  ; #DEBUG_LINE_NO:3205
  EndIf
  Compatibility.PopulateDefaultArmorData() ; #DEBUG_LINE_NO:3208
  Compatibility.RunCompatibilityArmors() ; #DEBUG_LINE_NO:3209
  Self.ArmorPageReset(True) ; #DEBUG_LINE_NO:3210
  _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:3211
  clothing.RefreshWornGearData(clothing.WornGearMainForms, clothing.WornGearForms, clothing._Frost_WornGearData) ; #DEBUG_LINE_NO:3212
  clothing.SendEvent_UpdateWarmthAndCoverage(False) ; #DEBUG_LINE_NO:3213
EndFunction

Function DefaultWornArmor()
  Bool confirmed = Self.ShowMessage("$FrostfallArmorDefaultWornConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3217
  If !confirmed ; #DEBUG_LINE_NO:3218
    Return  ; #DEBUG_LINE_NO:3219
  EndIf
  _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:3222
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:3223
  Armor[] worn_armor = Self.GetAllWornArmor() ; #DEBUG_LINE_NO:3225
  Int armor_count = commonarrayhelper.ArrayCountArmor(worn_armor) ; #DEBUG_LINE_NO:3226
  Int i = 0 ; #DEBUG_LINE_NO:3228
  While i < armor_count ; #DEBUG_LINE_NO:3229
    handler.RestoreDefaultArmorData(worn_armor[i]) ; #DEBUG_LINE_NO:3230
    i += 1 ; #DEBUG_LINE_NO:3231
  EndWhile
  Self.ArmorPageReset(True) ; #DEBUG_LINE_NO:3234
  clothing.RefreshWornGearData(clothing.WornGearMainForms, clothing.WornGearForms, clothing._Frost_WornGearData) ; #DEBUG_LINE_NO:3236
  clothing.SendEvent_UpdateWarmthAndCoverage(False) ; #DEBUG_LINE_NO:3237
EndFunction

Function DefaultAllArmor()
  Bool confirmed = Self.ShowMessage("$FrostfallArmorDefaultAllConfirm", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3241
  If !confirmed ; #DEBUG_LINE_NO:3242
    Return  ; #DEBUG_LINE_NO:3243
  EndIf
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:3246
  handler.RestoreAllDefaultArmorData() ; #DEBUG_LINE_NO:3247
  Self.ArmorPageReset(True) ; #DEBUG_LINE_NO:3249
  _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:3250
  clothing.RefreshWornGearData(clothing.WornGearMainForms, clothing.WornGearForms, clothing._Frost_WornGearData) ; #DEBUG_LINE_NO:3251
  clothing.SendEvent_UpdateWarmthAndCoverage(False) ; #DEBUG_LINE_NO:3252
EndFunction

Function RefreshSingleItemValues(Armor akArmor)
  _frostinternal.TryToRemoveArmorFromPrecache(akArmor as Form, _FrostData_ArmorPrecache) ; #DEBUG_LINE_NO:3257
  _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:3258
  Bool b = clothing.RemoveWornGearEntryForArmorUnequipped(akArmor, clothing.WornGearMainForms, clothing.WornGearForms, clothing._Frost_WornGearData) ; #DEBUG_LINE_NO:3259
  b = clothing.AddWornGearEntryForArmorEquipped(akArmor, clothing.WornGearMainForms, clothing.WornGearForms, clothing._Frost_WornGearData) as Bool ; #DEBUG_LINE_NO:3260
  clothing.RecalculateProtectionData(clothing.WornGearMainForms, clothing.WornGearForms, clothing.WornGearValues, clothing._Frost_WornGearData) ; #DEBUG_LINE_NO:3261
  clothing.SendEvent_UpdateWarmthAndCoverage(False) ; #DEBUG_LINE_NO:3262
EndFunction

Function ArmorPageReset(Bool abShowUpdatedMessage)
  If abShowUpdatedMessage ; #DEBUG_LINE_NO:3266
    ArmorPage_updated_msg = True ; #DEBUG_LINE_NO:3267
  EndIf
  Self.ForcePageReset() ; #DEBUG_LINE_NO:3269
EndFunction

Armor[] Function GetAllWornArmor()
  Armor[] wornArmor = new Armor[29] ; #DEBUG_LINE_NO:3274
  Int slotsChecked = slotsChecked + 1048576 ; #DEBUG_LINE_NO:3277
  slotsChecked += 2097152 ; #DEBUG_LINE_NO:3278
  slotsChecked += -2147483648 ; #DEBUG_LINE_NO:3279
  Int thisSlot = 1 ; #DEBUG_LINE_NO:3281
  While thisSlot < -2147483648 ; #DEBUG_LINE_NO:3282
    If Math.LogicalAnd(slotsChecked, thisSlot) != thisSlot ; #DEBUG_LINE_NO:3283
      Armor thisArmor = PlayerRef.GetWornForm(thisSlot) as Armor ; #DEBUG_LINE_NO:3284
      If thisArmor ; #DEBUG_LINE_NO:3285
        wornArmor[index] = thisArmor ; #DEBUG_LINE_NO:3286
        Int index = index + 1 ; #DEBUG_LINE_NO:3287
        slotsChecked += thisArmor.GetSlotMask() ; #DEBUG_LINE_NO:3288
      Else
        slotsChecked += thisSlot ; #DEBUG_LINE_NO:3290
      EndIf
    EndIf
    thisSlot *= 2 ; #DEBUG_LINE_NO:3293
  EndWhile
  Return wornArmor ; #DEBUG_LINE_NO:3295
EndFunction

String Function GetTypeString(Int aiType, _frost_armorprotectiondatastorehandler akHandler)
  If aiType == akHandler.GEARTYPE_BODY ; #DEBUG_LINE_NO:3299
    Return "$FrostfallBody" ; #DEBUG_LINE_NO:3300
  ElseIf aiType == akHandler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:3301
    Return "$FrostfallHead" ; #DEBUG_LINE_NO:3302
  ElseIf aiType == akHandler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:3303
    Return "$FrostfallHands" ; #DEBUG_LINE_NO:3304
  ElseIf aiType == akHandler.GEARTYPE_FEET ; #DEBUG_LINE_NO:3305
    Return "$FrostfallFeet" ; #DEBUG_LINE_NO:3306
  ElseIf aiType == akHandler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:3307
    Return "$FrostfallCloak" ; #DEBUG_LINE_NO:3308
  ElseIf aiType == akHandler.GEARTYPE_MISC ; #DEBUG_LINE_NO:3309
    Return "$FrostfallAccessory" ; #DEBUG_LINE_NO:3310
  ElseIf aiType == akHandler.GEARTYPE_IGNORE ; #DEBUG_LINE_NO:3311
    Return "$FrostfallNoProtection" ; #DEBUG_LINE_NO:3312
  Else
    Return "$FrostfallNA" ; #DEBUG_LINE_NO:3314
  EndIf
EndFunction

String Function GetExtraPartTypeString(Int aiType, _frost_armorprotectiondatastorehandler akHandler)
  _frost_strings str = _frostinternal.GetFrostfallStrings() ; #DEBUG_LINE_NO:3319
  If aiType == akHandler.GEARTYPE_BODY ; #DEBUG_LINE_NO:3320
    Return str.FrostfallBodyExtraPartDesc ; #DEBUG_LINE_NO:3321
  ElseIf aiType == akHandler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:3322
    Return str.FrostfallHeadExtraPartDesc ; #DEBUG_LINE_NO:3323
  ElseIf aiType == akHandler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:3324
    Return str.FrostfallHandsExtraPartDesc ; #DEBUG_LINE_NO:3325
  ElseIf aiType == akHandler.GEARTYPE_FEET ; #DEBUG_LINE_NO:3326
    Return str.FrostfallFeetExtraPartDesc ; #DEBUG_LINE_NO:3327
  ElseIf aiType == akHandler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:3328
    Return str.FrostfallCloakExtraPartDesc ; #DEBUG_LINE_NO:3329
  ElseIf aiType == akHandler.GEARTYPE_MISC ; #DEBUG_LINE_NO:3330
    Return str.FrostfallAccessoryExtraPartDesc ; #DEBUG_LINE_NO:3331
  EndIf
EndFunction

String Function GetUnnamedTypeString(Armor akArmor, Int aiType, _frost_armorprotectiondatastorehandler akHandler)
  _frost_strings str = _frostinternal.GetFrostfallStrings() ; #DEBUG_LINE_NO:3336
  If aiType == akHandler.GEARTYPE_BODY ; #DEBUG_LINE_NO:3337
    Return str.FrostfallBodyUnnamed ; #DEBUG_LINE_NO:3338
  ElseIf aiType == akHandler.GEARTYPE_HEAD ; #DEBUG_LINE_NO:3339
    Return str.FrostfallHeadUnnamed ; #DEBUG_LINE_NO:3340
  ElseIf aiType == akHandler.GEARTYPE_HANDS ; #DEBUG_LINE_NO:3341
    Return str.FrostfallHandsUnnamed ; #DEBUG_LINE_NO:3342
  ElseIf aiType == akHandler.GEARTYPE_FEET ; #DEBUG_LINE_NO:3343
    Return str.FrostfallFeetUnnamed ; #DEBUG_LINE_NO:3344
  ElseIf aiType == akHandler.GEARTYPE_CLOAK ; #DEBUG_LINE_NO:3345
    Return str.FrostfallCloakUnnamed ; #DEBUG_LINE_NO:3346
  ElseIf aiType == akHandler.GEARTYPE_MISC ; #DEBUG_LINE_NO:3347
    If akArmor.IsShield() ; #DEBUG_LINE_NO:3348
      Return str.FrostfallShieldUnnamed ; #DEBUG_LINE_NO:3349
    Else
      Return str.FrostfallAccessoryUnnamed ; #DEBUG_LINE_NO:3351
    EndIf
  ElseIf aiType == akHandler.GEARTYPE_IGNORE ; #DEBUG_LINE_NO:3353
    Return str.FrostfallNoProtectionUnnamed ; #DEBUG_LINE_NO:3354
  EndIf
EndFunction

Function ShowTutorial_ArmorPage(Bool abForceDisplay)
  Self.ShowMessage("$FrostfallArmorTutorial1", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3359
  Self.ShowMessage("$FrostfallArmorTutorial2", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3360
  Self.ShowMessage("$FrostfallArmorTutorial3", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3361
  Self.ShowMessage("$FrostfallArmorTutorial4", False, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3362
EndFunction

Function ApplyMeterPreset(Int aiPresetIdx)
  Int w = Utility.GetINIInt("iSize W:Display") ; #DEBUG_LINE_NO:3505
  Int h = Utility.GetINIInt("iSize H:Display") ; #DEBUG_LINE_NO:3506
  Float ratio = w as Float / h as Float ; #DEBUG_LINE_NO:3507
  Debug.trace(((("[Frostfall] Detected display resolution " + w as String) + "x" + h as String) + " (" + ratio as String) + " aspect ratio).", 0) ; #DEBUG_LINE_NO:3508
  If ratio > 1.700000048 && ratio < 1.799999952 ; #DEBUG_LINE_NO:3509
    Debug.trace("[Frostfall] Loading 16:9 aspect ratio meter preset.", 0) ; #DEBUG_LINE_NO:3510
  ElseIf ratio == 1.600000024 ; #DEBUG_LINE_NO:3511
    Debug.trace("[Frostfall] Loading 16:10 aspect ratio meter preset.", 0) ; #DEBUG_LINE_NO:3512
    aiPresetIdx += 4 ; #DEBUG_LINE_NO:3513
  ElseIf ratio > 1.299999952 && ratio < 1.399999976 ; #DEBUG_LINE_NO:3514
    Debug.trace("[Frostfall] Loading 4:3 aspect ratio meter preset.", 0) ; #DEBUG_LINE_NO:3515
    aiPresetIdx += 8 ; #DEBUG_LINE_NO:3516
  ElseIf config_is_open
    Bool result = Self.ShowMessage("$FrostfallMeterLayoutProblem", True, "$Accept", "$Cancel") ; #DEBUG_LINE_NO:3519
    If result == False ; #DEBUG_LINE_NO:3520
      Return  ; #DEBUG_LINE_NO:3521
    EndIf
  Else
    Debug.trace("[Frostfall] The display aspect ratio wasn't supported. Defaulting to 16:9.", 0) ; #DEBUG_LINE_NO:3524
  EndIf
  If aiPresetIdx == 0 ; #DEBUG_LINE_NO:3528
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3530
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3531
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3532
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_BOTTOMLEFT_16_9_X) ; #DEBUG_LINE_NO:3533
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_BOTTOMLEFT_16_9_Y) ; #DEBUG_LINE_NO:3534
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3535
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3536
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3537
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3538
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3539
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_BOTTOMLEFT_16_9_X) ; #DEBUG_LINE_NO:3540
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_BOTTOMLEFT_16_9_Y) ; #DEBUG_LINE_NO:3541
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3542
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3543
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3544
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3545
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3546
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_BOTTOMLEFT_16_9_X) ; #DEBUG_LINE_NO:3547
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_BOTTOMLEFT_16_9_Y) ; #DEBUG_LINE_NO:3548
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3549
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3550
  ElseIf aiPresetIdx == 1 ; #DEBUG_LINE_NO:3551
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3553
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3554
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3555
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_BOTTOMRIGHT_16_9_X) ; #DEBUG_LINE_NO:3556
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_BOTTOMRIGHT_16_9_Y) ; #DEBUG_LINE_NO:3557
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3558
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3559
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3560
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3561
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3562
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_BOTTOMRIGHT_16_9_X) ; #DEBUG_LINE_NO:3563
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_BOTTOMRIGHT_16_9_Y) ; #DEBUG_LINE_NO:3564
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3565
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3566
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3567
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3568
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3569
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_BOTTOMRIGHT_16_9_X) ; #DEBUG_LINE_NO:3570
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_BOTTOMRIGHT_16_9_Y) ; #DEBUG_LINE_NO:3571
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3572
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3573
  ElseIf aiPresetIdx == 2 ; #DEBUG_LINE_NO:3574
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3576
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3577
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3578
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_TOPLEFT_16_9_X) ; #DEBUG_LINE_NO:3579
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_TOPLEFT_16_9_Y) ; #DEBUG_LINE_NO:3580
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3581
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3582
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3583
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3584
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3585
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_TOPLEFT_16_9_X) ; #DEBUG_LINE_NO:3586
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_TOPLEFT_16_9_Y) ; #DEBUG_LINE_NO:3587
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3588
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3589
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3590
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3591
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3592
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_TOPLEFT_16_9_X) ; #DEBUG_LINE_NO:3593
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_TOPLEFT_16_9_Y) ; #DEBUG_LINE_NO:3594
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3595
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3596
  ElseIf aiPresetIdx == 3 ; #DEBUG_LINE_NO:3597
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3599
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3600
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3601
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:3602
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:3603
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3604
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3605
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3606
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3607
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3608
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:3609
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:3610
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3611
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3612
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3613
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3614
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3615
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_16_9_X) ; #DEBUG_LINE_NO:3616
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_16_9_Y) ; #DEBUG_LINE_NO:3617
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3618
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3619
  ElseIf aiPresetIdx == 4 ; #DEBUG_LINE_NO:3620
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3622
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3623
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3624
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_BOTTOMLEFT_16_10_X) ; #DEBUG_LINE_NO:3625
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_BOTTOMLEFT_16_10_Y) ; #DEBUG_LINE_NO:3626
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3627
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3628
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3629
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3630
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3631
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_BOTTOMLEFT_16_10_X) ; #DEBUG_LINE_NO:3632
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_BOTTOMLEFT_16_10_Y) ; #DEBUG_LINE_NO:3633
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3634
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3635
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3636
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3637
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3638
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_BOTTOMLEFT_16_10_X) ; #DEBUG_LINE_NO:3639
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_BOTTOMLEFT_16_10_Y) ; #DEBUG_LINE_NO:3640
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3641
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3642
  ElseIf aiPresetIdx == 5 ; #DEBUG_LINE_NO:3643
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3645
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3646
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3647
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_BOTTOMRIGHT_16_10_X) ; #DEBUG_LINE_NO:3648
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_BOTTOMRIGHT_16_10_Y) ; #DEBUG_LINE_NO:3649
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3650
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3651
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3652
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3653
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3654
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_BOTTOMRIGHT_16_10_X) ; #DEBUG_LINE_NO:3655
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_BOTTOMRIGHT_16_10_Y) ; #DEBUG_LINE_NO:3656
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3657
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3658
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3659
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3660
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3661
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_BOTTOMRIGHT_16_10_X) ; #DEBUG_LINE_NO:3662
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_BOTTOMRIGHT_16_10_Y) ; #DEBUG_LINE_NO:3663
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3664
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3665
  ElseIf aiPresetIdx == 6 ; #DEBUG_LINE_NO:3666
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3668
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3669
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3670
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_TOPLEFT_16_10_X) ; #DEBUG_LINE_NO:3671
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_TOPLEFT_16_10_Y) ; #DEBUG_LINE_NO:3672
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3673
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3674
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3675
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3676
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3677
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_TOPLEFT_16_10_X) ; #DEBUG_LINE_NO:3678
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_TOPLEFT_16_10_Y) ; #DEBUG_LINE_NO:3679
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3680
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3681
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3682
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3683
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3684
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_TOPLEFT_16_10_X) ; #DEBUG_LINE_NO:3685
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_TOPLEFT_16_10_Y) ; #DEBUG_LINE_NO:3686
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3687
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3688
  ElseIf aiPresetIdx == 7 ; #DEBUG_LINE_NO:3689
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3691
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3692
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3693
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_TOPRIGHT_16_10_X) ; #DEBUG_LINE_NO:3694
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_TOPRIGHT_16_10_Y) ; #DEBUG_LINE_NO:3695
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3696
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3697
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3698
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3699
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3700
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_TOPRIGHT_16_10_X) ; #DEBUG_LINE_NO:3701
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_TOPRIGHT_16_10_Y) ; #DEBUG_LINE_NO:3702
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3703
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3704
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3705
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3706
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3707
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_16_10_X) ; #DEBUG_LINE_NO:3708
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_16_10_Y) ; #DEBUG_LINE_NO:3709
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3710
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3711
  ElseIf aiPresetIdx == 8 ; #DEBUG_LINE_NO:3712
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3714
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3715
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3716
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_BOTTOMLEFT_4_3_X) ; #DEBUG_LINE_NO:3717
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_BOTTOMLEFT_4_3_Y) ; #DEBUG_LINE_NO:3718
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3719
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3720
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3721
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3722
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3723
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_BOTTOMLEFT_4_3_X) ; #DEBUG_LINE_NO:3724
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_BOTTOMLEFT_4_3_Y) ; #DEBUG_LINE_NO:3725
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3726
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3727
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_FILLDIR) ; #DEBUG_LINE_NO:3728
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_HANCHOR) ; #DEBUG_LINE_NO:3729
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMLEFT_VANCHOR) ; #DEBUG_LINE_NO:3730
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_BOTTOMLEFT_4_3_X) ; #DEBUG_LINE_NO:3731
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_BOTTOMLEFT_4_3_Y) ; #DEBUG_LINE_NO:3732
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3733
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3734
  ElseIf aiPresetIdx == 9 ; #DEBUG_LINE_NO:3735
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3737
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3738
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3739
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_BOTTOMRIGHT_4_3_X) ; #DEBUG_LINE_NO:3740
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_BOTTOMRIGHT_4_3_Y) ; #DEBUG_LINE_NO:3741
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3742
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3743
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3744
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3745
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3746
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_BOTTOMRIGHT_4_3_X) ; #DEBUG_LINE_NO:3747
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_BOTTOMRIGHT_4_3_Y) ; #DEBUG_LINE_NO:3748
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3749
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3750
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3751
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3752
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_BOTTOMRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3753
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_BOTTOMRIGHT_4_3_X) ; #DEBUG_LINE_NO:3754
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_BOTTOMRIGHT_4_3_Y) ; #DEBUG_LINE_NO:3755
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT) ; #DEBUG_LINE_NO:3756
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3757
  ElseIf aiPresetIdx == 10 ; #DEBUG_LINE_NO:3758
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3760
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3761
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3762
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_TOPLEFT_4_3_X) ; #DEBUG_LINE_NO:3763
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_TOPLEFT_4_3_Y) ; #DEBUG_LINE_NO:3764
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3765
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3766
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3767
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3768
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3769
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_TOPLEFT_4_3_X) ; #DEBUG_LINE_NO:3770
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_TOPLEFT_4_3_Y) ; #DEBUG_LINE_NO:3771
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3772
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3773
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_TOPLEFT_FILLDIR) ; #DEBUG_LINE_NO:3774
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_TOPLEFT_HANCHOR) ; #DEBUG_LINE_NO:3775
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_TOPLEFT_VANCHOR) ; #DEBUG_LINE_NO:3776
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_TOPLEFT_4_3_X) ; #DEBUG_LINE_NO:3777
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_TOPLEFT_4_3_Y) ; #DEBUG_LINE_NO:3778
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3779
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3780
  ElseIf aiPresetIdx == 11 ; #DEBUG_LINE_NO:3781
    _Frost_Setting_MeterExposureFillDirection.SetValueInt(EXPOSURE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3783
    _Frost_Setting_MeterExposureHAnchor.SetValueInt(EXPOSURE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3784
    _Frost_Setting_MeterExposureVAnchor.SetValueInt(EXPOSURE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3785
    _Frost_Setting_MeterExposureXPos.SetValue(EXPOSURE_METER_TOPRIGHT_4_3_X) ; #DEBUG_LINE_NO:3786
    _Frost_Setting_MeterExposureYPos.SetValue(EXPOSURE_METER_TOPRIGHT_4_3_Y) ; #DEBUG_LINE_NO:3787
    _Frost_Setting_MeterExposureHeight.SetValue(NORMAL_METER_HEIGHT) ; #DEBUG_LINE_NO:3788
    _Frost_Setting_MeterExposureWidth.SetValue(NORMAL_METER_WIDTH) ; #DEBUG_LINE_NO:3789
    _Frost_Setting_MeterWetnessFillDirection.SetValueInt(WETNESS_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3790
    _Frost_Setting_MeterWetnessHAnchor.SetValueInt(WETNESS_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3791
    _Frost_Setting_MeterWetnessVAnchor.SetValueInt(WETNESS_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3792
    _Frost_Setting_MeterWetnessXPos.SetValue(WETNESS_METER_TOPRIGHT_4_3_X) ; #DEBUG_LINE_NO:3793
    _Frost_Setting_MeterWetnessYPos.SetValue(WETNESS_METER_TOPRIGHT_4_3_Y) ; #DEBUG_LINE_NO:3794
    _Frost_Setting_MeterWetnessHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3795
    _Frost_Setting_MeterWetnessWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3796
    _Frost_Setting_MeterWeathersenseFillDirection.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_FILLDIR) ; #DEBUG_LINE_NO:3797
    _Frost_Setting_MeterWeathersenseHAnchor.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_HANCHOR) ; #DEBUG_LINE_NO:3798
    _Frost_Setting_MeterWeathersenseVAnchor.SetValueInt(WEATHERSENSE_METER_TOPRIGHT_VANCHOR) ; #DEBUG_LINE_NO:3799
    _Frost_Setting_MeterWeathersenseXPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_4_3_X) ; #DEBUG_LINE_NO:3800
    _Frost_Setting_MeterWeathersenseYPos.SetValue(WEATHERSENSE_METER_TOPRIGHT_4_3_Y) ; #DEBUG_LINE_NO:3801
    _Frost_Setting_MeterWeathersenseHeight.SetValue(CHARGE_METER_HEIGHT_INV) ; #DEBUG_LINE_NO:3802
    _Frost_Setting_MeterWeathersenseWidth.SetValue(CHARGE_METER_WIDTH) ; #DEBUG_LINE_NO:3803
  EndIf
  Self.UpdateMeterConfiguration(0) ; #DEBUG_LINE_NO:3806
  Self.UpdateMeterConfiguration(1) ; #DEBUG_LINE_NO:3807
  Self.UpdateMeterConfiguration(2) ; #DEBUG_LINE_NO:3808
EndFunction

Function ConfigureMeter(Int aiMeterIdx, Int aiFillDirectionIdx, Int aiHAnchorIdx, Int aiVAnchorIdx, Float afPositionX, Float afPositionY, Float afHeight, Float afWidth)
  common_ski_meterwidget MyMeter = None ; #DEBUG_LINE_NO:3813
  commonmeterinterfacehandler MyMeterHandler = None ; #DEBUG_LINE_NO:3814
  If aiMeterIdx == 0 ; #DEBUG_LINE_NO:3815
    MyMeter = ExposureMeter as common_ski_meterwidget ; #DEBUG_LINE_NO:3816
    MyMeterHandler = ExposureMeterHandler as commonmeterinterfacehandler ; #DEBUG_LINE_NO:3817
  ElseIf aiMeterIdx == 1 ; #DEBUG_LINE_NO:3818
    MyMeter = WetnessMeter as common_ski_meterwidget ; #DEBUG_LINE_NO:3819
    MyMeterHandler = WetnessMeterHandler as commonmeterinterfacehandler ; #DEBUG_LINE_NO:3820
  ElseIf aiMeterIdx == 2 ; #DEBUG_LINE_NO:3821
    MyMeter = WeathersenseMeter as common_ski_meterwidget ; #DEBUG_LINE_NO:3822
    MyMeterHandler = WeathersenseMeterHandler as commonmeterinterfacehandler ; #DEBUG_LINE_NO:3823
  EndIf
  If !MyMeter ; #DEBUG_LINE_NO:3826
    Return  ; #DEBUG_LINE_NO:3827
  EndIf
  MyMeter.FillDirection = FILL_DIRECTIONS[aiFillDirectionIdx] ; #DEBUG_LINE_NO:3830
  MyMeter.HAnchor = HORIZONTAL_ANCHORS[aiHAnchorIdx] ; #DEBUG_LINE_NO:3831
  MyMeter.VAnchor = VERTICAL_ANCHORS[aiVAnchorIdx] ; #DEBUG_LINE_NO:3832
  MyMeter.x = afPositionX ; #DEBUG_LINE_NO:3833
  MyMeter.Y = afPositionY ; #DEBUG_LINE_NO:3834
  MyMeter.Height = afHeight ; #DEBUG_LINE_NO:3835
  MyMeter.Width = afWidth ; #DEBUG_LINE_NO:3836
  MyMeterHandler.ForceMeterDisplay(False) ; #DEBUG_LINE_NO:3837
EndFunction

Function UpdateMeterConfiguration(Int aiMeterIdx)
  If aiMeterIdx == 0 ; #DEBUG_LINE_NO:3841
    Self.ConfigureMeter(0, _Frost_Setting_MeterExposureFillDirection.GetValueInt(), _Frost_Setting_MeterExposureHAnchor.GetValueInt(), _Frost_Setting_MeterExposureVAnchor.GetValueInt(), _Frost_Setting_MeterExposureXPos.GetValue(), _Frost_Setting_MeterExposureYPos.GetValue(), _Frost_Setting_MeterExposureHeight.GetValue(), _Frost_Setting_MeterExposureWidth.GetValue()) ; #DEBUG_LINE_NO:3843,3844,3845,3846,3847,3848,3849
  ElseIf aiMeterIdx == 1 ; #DEBUG_LINE_NO:3850
    Self.ConfigureMeter(1, _Frost_Setting_MeterWetnessFillDirection.GetValueInt(), _Frost_Setting_MeterWetnessHAnchor.GetValueInt(), _Frost_Setting_MeterWetnessVAnchor.GetValueInt(), _Frost_Setting_MeterWetnessXPos.GetValue(), _Frost_Setting_MeterWetnessYPos.GetValue(), _Frost_Setting_MeterWetnessHeight.GetValue(), _Frost_Setting_MeterWetnessWidth.GetValue()) ; #DEBUG_LINE_NO:3852,3853,3854,3855,3856,3857,3858
  ElseIf aiMeterIdx == 2 ; #DEBUG_LINE_NO:3859
    Self.ConfigureMeter(2, _Frost_Setting_MeterWeathersenseFillDirection.GetValueInt(), _Frost_Setting_MeterWeathersenseHAnchor.GetValueInt(), _Frost_Setting_MeterWeathersenseVAnchor.GetValueInt(), _Frost_Setting_MeterWeathersenseXPos.GetValue(), _Frost_Setting_MeterWeathersenseYPos.GetValue(), _Frost_Setting_MeterWeathersenseHeight.GetValue(), _Frost_Setting_MeterWeathersenseWidth.GetValue()) ; #DEBUG_LINE_NO:3861,3862,3863,3864,3865,3866,3867
  EndIf
EndFunction

Function RemoveAllMeters()
  Self.SendEvent_FrostfallRemoveExposureMeter() ; #DEBUG_LINE_NO:3872
  Self.SendEvent_FrostfallRemoveWetnessMeter() ; #DEBUG_LINE_NO:3873
  Self.SendEvent_FrostfallRemoveWeathersenseMeter() ; #DEBUG_LINE_NO:3874
EndFunction

Function ForceAllMeters()
  Self.SendEvent_ForceExposureMeterDisplay(False) ; #DEBUG_LINE_NO:3878
  Self.SendEvent_ForceWetnessMeterDisplay(False) ; #DEBUG_LINE_NO:3879
  Self.SendEvent_ForceWeathersenseMeterDisplay(False) ; #DEBUG_LINE_NO:3880
EndFunction

Float Function GetMeterScale(Float afCurrentWidth, Float afBaseWidth)
  Return afCurrentWidth / afBaseWidth ; #DEBUG_LINE_NO:3884
EndFunction

Bool Function IsMeterInverted(commonmeterinterfacehandler handler)
  If handler.meter_inversion_value != -1.0 ; #DEBUG_LINE_NO:3888
    If handler.lower_is_better && handler.AttributeValue.GetValue() < handler.meter_inversion_value ; #DEBUG_LINE_NO:3889
      Return True ; #DEBUG_LINE_NO:3890
    ElseIf !handler.lower_is_better && handler.AttributeValue.GetValue() > handler.meter_inversion_value ; #DEBUG_LINE_NO:3891
      Return True ; #DEBUG_LINE_NO:3892
    Else
      Return False ; #DEBUG_LINE_NO:3894
    EndIf
  Else
    Return False ; #DEBUG_LINE_NO:3897
  EndIf
EndFunction

Function SendEvent_FrostfallRemoveExposureMeter()
  Int handle = modevent.Create("Frostfall_RemoveExposureMeter") ; #DEBUG_LINE_NO:3902
  If handle ; #DEBUG_LINE_NO:3903
    modevent.Send(handle) ; #DEBUG_LINE_NO:3904
  EndIf
EndFunction

Function SendEvent_FrostfallRemoveWetnessMeter()
  Int handle = modevent.Create("Frostfall_RemoveWetnessMeter") ; #DEBUG_LINE_NO:3909
  If handle ; #DEBUG_LINE_NO:3910
    modevent.Send(handle) ; #DEBUG_LINE_NO:3911
  EndIf
EndFunction

Function SendEvent_FrostfallRemoveWeathersenseMeter()
  Int handle = modevent.Create("Frostfall_RemoveWeathersenseMeter") ; #DEBUG_LINE_NO:3916
  If handle ; #DEBUG_LINE_NO:3917
    modevent.Send(handle) ; #DEBUG_LINE_NO:3918
  EndIf
EndFunction

Function SendEvent_ForceExposureMeterDisplay(Bool abFlash)
  Int handle = modevent.Create("Frostfall_ForceExposureMeterDisplay") ; #DEBUG_LINE_NO:3923
  If handle ; #DEBUG_LINE_NO:3924
    modevent.PushBool(handle, abFlash) ; #DEBUG_LINE_NO:3925
    modevent.Send(handle) ; #DEBUG_LINE_NO:3926
  EndIf
EndFunction

Function SendEvent_ForceWetnessMeterDisplay(Bool abFlash)
  Int handle = modevent.Create("Frostfall_ForceWetnessMeterDisplay") ; #DEBUG_LINE_NO:3931
  If handle ; #DEBUG_LINE_NO:3932
    modevent.PushBool(handle, abFlash) ; #DEBUG_LINE_NO:3933
    modevent.Send(handle) ; #DEBUG_LINE_NO:3934
  EndIf
EndFunction

Function SendEvent_ForceWeathersenseMeterDisplay(Bool abFlash)
  Int handle = modevent.Create("Frostfall_ForceWeathersenseMeterDisplay") ; #DEBUG_LINE_NO:3939
  If handle ; #DEBUG_LINE_NO:3940
    modevent.PushBool(handle, abFlash) ; #DEBUG_LINE_NO:3941
    modevent.Send(handle) ; #DEBUG_LINE_NO:3942
  EndIf
EndFunction
