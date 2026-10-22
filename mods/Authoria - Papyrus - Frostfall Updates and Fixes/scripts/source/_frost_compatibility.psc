ScriptName _Frost_Compatibility Extends ReferenceAlias

;-- Variables ---------------------------------------
String CONFIG_PATH = "../FrostfallData/"
Float[] DLC1_FVBoss_PolyX
Float[] DLC1_FVBoss_PolyY
Float[] DLC1_FVCanyon_PolyX
Float[] DLC1_FVCanyon_PolyY
Float[] DLC1_FVGrove_PolyX
Float[] DLC1_FVGrove_PolyY
Float[] DLC1_FVIce_PolyX
Float[] DLC1_FVIce_PolyY
Float[] DLC1_FVPlayground_PolyX
Float[] DLC1_FVPlayground_PolyY
Float[] DLC2_SolstheimArctic_PolyX
Float[] DLC2_SolstheimArctic_PolyY
Float[] DNKD_Phalos_Frozen_PolyX
Float[] DNKD_Phalos_Frozen_PolyY
Float[] Wyrmstooth_Center_PolyX
Float[] Wyrmstooth_Center_PolyY
Float[] Wyrmstooth_West_PolyX
Float[] Wyrmstooth_West_PolyY
Bool added_spell_books = False
Bool datastore_update_required = False
Bool hotfix341 = False
Bool uiPackageInstalled = False

;-- Properties --------------------------------------
Armor Property ArmorBanditCuirass1 Auto
Armor Property ArmorBanditCuirass2 Auto
Armor Property ArmorBanditCuirass3 Auto
Armor Property ArmorHideCuirass Auto
Bool Property BeyondReachPresent Auto
Bool Property BrumaPresent Auto
Int Property CAMPFIRE_MIN_VERSION = 11200 AutoReadOnly
Bool Property ChanterellePresent Auto
Bool Property ClimatesOfTamrielPresent Auto
_frost_conditionvalues Property Conditions Auto
Bool Property CurseOfAkavirPhoePresent Auto
Weather Property DLC2AshStorm Auto hidden
Bool Property DarkendPresent Auto
Bool Property FalamyrrIslePresent Auto
Bool Property FalkreathCreekPresent Auto
Bool Property FalskaarPresent Auto
Bool Property FolkvangrPresent Auto
Bool Property GrayCowlOfNocturnalPresent Auto
Bool Property HangingGardensPresent Auto
Bool Property HuntersWorldPresent Auto
Bool Property HuntingGroundPresent Auto
Bool Property JehannaHaafstadPresent Auto
LeveledItem Property LItemScroll00Skill Auto
LeveledItem Property LItemScroll100Skill Auto
LeveledItem Property LItemScroll25Skill Auto
LeveledItem Property LItemScroll50Skill Auto
LeveledItem Property LItemScroll75Skill Auto
LeveledItem Property LItemSpellTOmes50AllRestoration Auto
LeveledItem Property LItemSpellTOmes50Restoration Auto
LeveledItem Property LItemSpellTomes00AllIllusion Auto
LeveledItem Property LItemSpellTomes00AllSpells Auto
LeveledItem Property LItemSpellTomes00Illusion Auto
LeveledItem Property LItemSpellTomes00Spells Auto
LeveledItem Property LItemSpellTomes100Conjuration Auto
LeveledItem Property LItemSpellTomes25AllAlteration Auto
LeveledItem Property LItemSpellTomes25AllConjuration Auto
LeveledItem Property LItemSpellTomes25AllIllusion Auto
LeveledItem Property LItemSpellTomes25Alteration Auto
LeveledItem Property LItemSpellTomes25Conjuration Auto
LeveledItem Property LItemSpellTomes25Illusion Auto
LeveledItem Property LItemSpellTomes50AllAlteration Auto
LeveledItem Property LItemSpellTomes50AllConjuration Auto
LeveledItem Property LItemSpellTomes50AllIllusion Auto
LeveledItem Property LItemSpellTomes50Alteration Auto
LeveledItem Property LItemSpellTomes50Conjuration Auto
LeveledItem Property LItemSpellTomes50Illusion Auto
LeveledItem Property LItemSpellTomes50Spells Auto
LeveledItem Property LItemSpellTomes75AllAlteration Auto
LeveledItem Property LItemSpellTomes75AllConjuration Auto
LeveledItem Property LItemSpellTomes75Alteration Auto
LeveledItem Property LItemSpellTomes75Conjuration Auto
LeveledItem Property LItemSpellTomes75Spells Auto
Bool Property LastSeedPresent Auto
LeveledItem Property LitemSpellTomes50AllDestruction Auto
LeveledItem Property LitemSpellTomes50Destruction Auto
Bool Property LothbrukVillagePresent Auto
LeveledItem Property MGRitualConjurationBooks Auto
Bool Property MidwoodIslePresent Auto
String Property NameOfMod Auto
Int Property NumberOfMods Auto
Bool Property NyhusPresent Auto
ReferenceAlias Property PlayerAlias Auto
Actor Property PlayerRef Auto
Int Property SKSE_MIN_VERSION = 10703 AutoReadOnly
Bool Property ScenicCarriagesPresent Auto
Bool Property ShumerFallOfAllagardPresent Auto
Bool Property SkyRePresent Auto
Bool Property SkygerfallPresent Auto
Bool Property SummerSetIslesPresent Auto
Bool Property TheEgyptianPalaceOfAmarnaPresent Auto
Bool Property TheHavenFromTheColdAndDarkPresent Auto
Bool Property TheIslandPresent Auto
Bool Property TheNilePresent Auto
Bool Property TheRepublicOfMasleaPresent Auto
Bool Property TheShirePresent Auto
Bool Property TheValleyOfPeacePresent Auto
Bool Property VominheimPresent Auto
Float Property WEARABLELANTERNS_MIN_VERSION = 4.019999981 AutoReadOnly
WorldSpace Property WS_AncestorsGlade Auto hidden
WorldSpace Property WS_Apocrypha Auto hidden
WorldSpace Property WS_Boneyard Auto hidden
WorldSpace Property WS_Darkend Auto hidden
WorldSpace Property WS_DayspringCanyon Auto hidden
WorldSpace Property WS_FalmerValley Auto hidden
WorldSpace Property WS_Solstheim Auto hidden
WorldSpace Property WS_SoulCairn Auto hidden
WorldSpace Property WS_VolkiharCourtyard Auto hidden
WorldSpace Property WS_Wyrmstooth Auto hidden
Bool Property WetAndColdPresent Auto
Bool Property WyrmstoothPresent Auto
Armor Property _Camp_ArmorBanditCuirass1 Auto
Armor Property _Camp_ArmorBanditCuirass2 Auto
Armor Property _Camp_ArmorBanditCuirass3 Auto
FormList Property _Camp_HeatSources_All Auto
FormList Property _Camp_HeatSources_Other Auto
GlobalVariable Property _Camp_IsSpecialEdition Auto
FormList Property _Camp_WorldspacesInteriors Auto
Keyword Property _FrostData_ArmorPrecache Auto
GlobalVariable Property _Frost_AttributeExposureMeter Auto
Message Property _Frost_CriticalError_Campfire Auto
Message Property _Frost_CriticalError_JSONReadWrite Auto
Message Property _Frost_CriticalError_SKSE Auto
Message Property _Frost_CriticalError_SkyUIInterfacePackage Auto
Message Property _Frost_CriticalError_SkyUIInterfacePackageOld Auto
Message Property _Frost_Error_WearableLanterns Auto
FormList Property _Frost_ExposureExceptions Auto
FormList Property _Frost_FastTravelExceptions Auto
Perk Property _Frost_FrostResistWarmthModPerk Auto
GlobalVariable Property _Frost_FrostfallVersion Auto
GlobalVariable Property _Frost_HotkeyWeathersense Auto
Spell Property _Frost_InspectEquipment_Spell Auto
Spell Property _Frost_LegacyConfig_Spell Auto
FormList Property _Frost_OvercastWeatherList Auto
Activator Property _Frost_PerkNodeController_Endurance Auto
GlobalVariable Property _Frost_PreviousVersion Auto
Spell Property _Frost_RegionDetect Auto
Message Property _Frost_ReleaseNotes_3_3_1 Auto
Message Property _Frost_ReleaseNotes_3_4 Auto
Scroll Property _Frost_ScrollBask Auto
Scroll Property _Frost_ScrollBearskin Auto
Scroll Property _Frost_ScrollBoundCloakGreater Auto
Scroll Property _Frost_ScrollBoundCloakLesser Auto
Scroll Property _Frost_ScrollConjureShelterGreater Auto
Scroll Property _Frost_ScrollConjureShelterLesser Auto
Scroll Property _Frost_ScrollFoxskin Auto
Scroll Property _Frost_ScrollKindle Auto
Scroll Property _Frost_ScrollRevel Auto
Scroll Property _Frost_ScrollSoothe Auto
Scroll Property _Frost_ScrollVaporBlast Auto
Scroll Property _Frost_ScrollWolfskin Auto
GlobalVariable Property _Frost_Setting_1PAnimationAllowed Auto
GlobalVariable Property _Frost_Setting_DisplayTutorials Auto
GlobalVariable Property _Frost_Setting_MeterExposureColor Auto
GlobalVariable Property _Frost_Setting_MeterExposureColorWarm Auto
GlobalVariable Property _Frost_Setting_Notifications_EquipmentSummary Auto
GlobalVariable Property _Frost_Setting_Notifications_EquipmentValues Auto
FormList Property _Frost_SevereWeatherList Auto
Book Property _Frost_SpellTomeBearskin Auto
Book Property _Frost_SpellTomeBoundCloakGreater Auto
Book Property _Frost_SpellTomeBoundCloakLesser Auto
Book Property _Frost_SpellTomeConjureShelterGreater Auto
Book Property _Frost_SpellTomeConjureShelterLesser Auto
Book Property _Frost_SpellTomeFoxskin Auto
Book Property _Frost_SpellTomeKindle Auto
Book Property _Frost_SpellTomeSoothe1 Auto
Book Property _Frost_SpellTomeSoothe2 Auto
Book Property _Frost_SpellTomeSoothe3 Auto
Book Property _Frost_SpellTomeTransmuteWood Auto
Book Property _Frost_SpellTomeVaporBlast Auto
Book Property _Frost_SpellTomeWolfskin Auto
GlobalVariable Property _Frost_Upgraded_3_0_1 Auto
GlobalVariable Property _Frost_Upgraded_3_0_2 Auto
GlobalVariable Property _Frost_Upgraded_3_1 Auto
GlobalVariable Property _Frost_Upgraded_3_2 Auto
GlobalVariable Property _Frost_Upgraded_3_2_1 Auto
GlobalVariable Property _Frost_Upgraded_3_3_1 Auto
GlobalVariable Property _Frost_Upgraded_3_4 Auto
Spell Property _Frost_Weathersense_Spell Auto
FormList Property _Frost_WorldspacesExteriorCoast Auto
FormList Property _Frost_WorldspacesExteriorFallForest Auto
FormList Property _Frost_WorldspacesExteriorOblivion Auto
FormList Property _Frost_WorldspacesExteriorPineForest Auto
FormList Property _Frost_WorldspacesExteriorReach Auto
FormList Property _Frost_WorldspacesExteriorSnowy Auto
FormList Property _Frost_WorldspacesExteriorTundraMarsh Auto
FormList Property _Frost_WorldspacesExteriorVolcanicTundra Auto
FormList Property _Frost_WorldspacesExteriorWhiterun Auto
FormList Property _Frost_WorldspacesFTException Auto
GlobalVariable Property _WetIsBlizzarding Auto hidden
Faction Property _WetIsUnderShelterFaction Auto hidden
Bool Property isAEALoaded Auto hidden
Bool Property isCOSDGLoaded Auto hidden
Bool Property isCOSLoaded Auto hidden
Bool Property isCOTLoaded Auto hidden
Bool Property isDLC1Loaded Auto hidden
Bool Property isDLC2Loaded Auto hidden
Bool Property isHDTCloaksLoaded Auto hidden
Bool Property isHFLoaded Auto hidden
Bool Property isIMALoaded Auto hidden
Bool Property isLastSeedLoaded Auto hidden
Bool Property isNFHLoaded Auto hidden
Bool Property isSCLoaded Auto hidden
Bool Property isSKSELoaded Auto hidden
Bool Property isSKYRELoaded Auto hidden
Bool Property isSKYUILoaded Auto hidden
Bool Property isUIPackageInstalled hidden
  Bool Function Get()
    Return uiPackageInstalled ; #DEBUG_LINE_NO:308
  EndFunction
  Function Set(Bool isInstalled)
    uiPackageInstalled = isInstalled ; #DEBUG_LINE_NO:311
    If isInstalled ; #DEBUG_LINE_NO:312
      _Frost_Setting_Notifications_EquipmentValues.SetValueInt(1) ; #DEBUG_LINE_NO:313
      _Frost_Setting_Notifications_EquipmentSummary.SetValueInt(1) ; #DEBUG_LINE_NO:314
    EndIf
  EndFunction
EndProperty
Bool Property isWACLoaded Auto hidden
Bool Property isWICLoaded Auto hidden

;-- Functions ---------------------------------------

Function AEALoadUp_Vanilla()
  ; Empty function
EndFunction

Function COSDGLoadUp_Vanilla()
  ; Empty function
EndFunction

Function COSLoadUp_Vanilla()
  ; Empty function
EndFunction

; Skipped compiler generated GetState

; Skipped compiler generated GotoState

Function HDTCloaksLoadUp()
  ; Empty function
EndFunction

Function NFHLoadUp_Vanilla()
  ; Empty function
EndFunction

Function RegisterForControlsOnLoad()
  ; Empty function
EndFunction

Function WACLoadUp_Vanilla()
  ; Empty function
EndFunction

Function WICLoadUp_Vanilla()
  ; Empty function
EndFunction

Function RegisterCampfireSkill()
  GlobalVariable CampfireAPIVersion = Game.GetFormFromFile(258494, "Campfire.esm") as GlobalVariable ; #DEBUG_LINE_NO:341
  If CampfireAPIVersion as Bool && CampfireAPIVersion.GetValueInt() >= 4 ; #DEBUG_LINE_NO:342
    Bool b = camputil.RegisterPerkTree(_Frost_PerkNodeController_Endurance, "Frostfall.esp") ; #DEBUG_LINE_NO:343
  Else
    Debug.trace("[Campfire] ERROR: Unable to register Campfire Skill System for Frostfall.esp. Campfire was not found or the version loaded is not compatible. Expected CampUtil API 4 or higher, got " + CampfireAPIVersion.GetValueInt() as String, 0) ; #DEBUG_LINE_NO:345
  EndIf
EndFunction

Event OnPlayerLoadGame()
  Self.RunCompatibility() ; #DEBUG_LINE_NO:357
  Self.RegisterForKeysOnLoad() ; #DEBUG_LINE_NO:358
  Self.RegisterForControlsOnLoad() ; #DEBUG_LINE_NO:359
  Self.RegisterForEventsOnLoad() ; #DEBUG_LINE_NO:360
  Self.SendEvent_FrostfallLoaded() ; #DEBUG_LINE_NO:361
EndEvent

Function RunCompatibility()
  Debug.trace("[Frostfall]======================================================================================================", 0) ; #DEBUG_LINE_NO:374
  Debug.trace("[Frostfall]                    Frostfall is now performing start-up and compatibility checks.                    ", 0) ; #DEBUG_LINE_NO:375
  Debug.trace("[Frostfall]           Errors related to missing files may follow. These are NORMAL and should be ignored.        ", 0) ; #DEBUG_LINE_NO:376
  Debug.trace("[Frostfall]======================================================================================================", 0) ; #DEBUG_LINE_NO:377
  If _Camp_IsSpecialEdition.GetValueInt() != 2 ; #DEBUG_LINE_NO:379
    Bool skse_loaded = skse.GetVersion() as Bool ; #DEBUG_LINE_NO:380
    If skse_loaded ; #DEBUG_LINE_NO:381
      Int skse_version = skse.GetVersion() * 10000 + skse.GetVersionMinor() * 100 + skse.GetVersionBeta() ; #DEBUG_LINE_NO:382
      If skse_version < Self.SKSE_MIN_VERSION ; #DEBUG_LINE_NO:383
        isSKSELoaded = False ; #DEBUG_LINE_NO:384
        Self.ErrorSKSE(skse_version) ; #DEBUG_LINE_NO:385
      Else
        isSKSELoaded = True ; #DEBUG_LINE_NO:387
        Debug.trace((("[Frostfall] Detected SKSE version " + (skse_version as Float / 10000.0) as String) + " (expected " + (Self.SKSE_MIN_VERSION as Float / 10000.0) as String) + " or newer, success!)", 0) ; #DEBUG_LINE_NO:388
      EndIf
    Else
      isSKSELoaded = False ; #DEBUG_LINE_NO:391
      Self.ErrorSKSE(0) ; #DEBUG_LINE_NO:392
    EndIf
  EndIf
  Self.VanillaGameLoadUp() ; #DEBUG_LINE_NO:397
  (PlayerAlias as _frost_playerequipmonitor).InitializeEventQueue() ; #DEBUG_LINE_NO:401
  If isSKSELoaded ; #DEBUG_LINE_NO:405
    _frostinternal.RemoveAllArmorFromPrecache(_FrostData_ArmorPrecache) ; #DEBUG_LINE_NO:406
  EndIf
  _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:409
  clothing.WornGearFormsIntegrityCheck(clothing.WornGearForms, clothing.WornGearMainForms) ; #DEBUG_LINE_NO:410
  If isSKSELoaded ; #DEBUG_LINE_NO:414
    Bool can_read_write = Self.CheckJSONReadWrite() ; #DEBUG_LINE_NO:415
    If !can_read_write ; #DEBUG_LINE_NO:416
      _Frost_CriticalError_JSONReadWrite.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:417
    EndIf
  EndIf
  If _Frost_Upgraded_3_0_1.GetValueInt() != 2 ; #DEBUG_LINE_NO:422
    Self.Upgrade_3_0_1() ; #DEBUG_LINE_NO:423
  EndIf
  If _Frost_Upgraded_3_0_2.GetValueInt() != 2 ; #DEBUG_LINE_NO:425
    Self.Upgrade_3_0_2() ; #DEBUG_LINE_NO:426
  EndIf
  If _Frost_Upgraded_3_1.GetValueInt() != 2 ; #DEBUG_LINE_NO:428
    Self.Upgrade_3_1() ; #DEBUG_LINE_NO:429
  EndIf
  If _Frost_Upgraded_3_2.GetValueInt() != 2 ; #DEBUG_LINE_NO:431
    Self.Upgrade_3_2() ; #DEBUG_LINE_NO:432
  EndIf
  If _Frost_Upgraded_3_2_1.GetValueInt() != 2 ; #DEBUG_LINE_NO:434
    Self.Upgrade_3_2_1() ; #DEBUG_LINE_NO:435
  EndIf
  If _Frost_Upgraded_3_3_1.GetValueInt() != 2 ; #DEBUG_LINE_NO:437
    Self.Upgrade_3_3_1() ; #DEBUG_LINE_NO:438
  EndIf
  If _Frost_Upgraded_3_4.GetValueInt() != 2 ; #DEBUG_LINE_NO:440
    Self.Upgrade_3_4() ; #DEBUG_LINE_NO:441
  EndIf
  If !hotfix341 ; #DEBUG_LINE_NO:443
    Self.Upgrade_3_4_1() ; #DEBUG_LINE_NO:444
  EndIf
  Self.CheckDatastore() ; #DEBUG_LINE_NO:449
  _Frost_PreviousVersion.SetValue(_Frost_FrostfallVersion.GetValue()) ; #DEBUG_LINE_NO:453
  Float campfire_version = camputil.GetCampfireVersion() ; #DEBUG_LINE_NO:455
  If campfire_version < Self.CAMPFIRE_MIN_VERSION as Float ; #DEBUG_LINE_NO:456
    Self.FatalErrorCampfire(campfire_version) ; #DEBUG_LINE_NO:457
  Else
    Debug.trace((("[Frostfall] Detected Campfire version " + campfire_version as String) + " (expected " + Self.CAMPFIRE_MIN_VERSION as String) + " or newer, success!)", 0) ; #DEBUG_LINE_NO:459
  EndIf
  Bool isWearableLanternsLoaded = Self.IsPluginLoaded(32731, "Chesko_WearableLantern.esp") ; #DEBUG_LINE_NO:464
  If isWearableLanternsLoaded ; #DEBUG_LINE_NO:465
    GlobalVariable WLVersionGlobal = Game.GetFormFromFile(125396, "Chesko_WearableLantern.esp") as GlobalVariable ; #DEBUG_LINE_NO:466
    If WLVersionGlobal ; #DEBUG_LINE_NO:467
      Float wearablelanterns_version = WLVersionGlobal.GetValue() ; #DEBUG_LINE_NO:468
      If wearablelanterns_version >= Self.WEARABLELANTERNS_MIN_VERSION ; #DEBUG_LINE_NO:469
        Debug.trace((("[Frostfall] Detected Wearable Lanterns version " + wearablelanterns_version as String) + " (expected " + Self.WEARABLELANTERNS_MIN_VERSION as String) + " or newer, success!)", 0) ; #DEBUG_LINE_NO:470
      Else
        Self.ErrorWearableLanterns() ; #DEBUG_LINE_NO:472
      EndIf
    Else
      Self.ErrorWearableLanterns() ; #DEBUG_LINE_NO:475
    EndIf
  EndIf
  If isSKYUILoaded ; #DEBUG_LINE_NO:481
    isSKYUILoaded = Self.IsPluginLoaded(16779284, "SkyUI_SE.esp") || Self.IsPluginLoaded(16779284, "SkyUI.esp") ; #DEBUG_LINE_NO:482
    If !isSKYUILoaded ; #DEBUG_LINE_NO:483
      
    EndIf
  Else
    isSKYUILoaded = Self.IsPluginLoaded(16779284, "SkyUI_SE.esp") || Self.IsPluginLoaded(16779284, "SkyUI.esp") ; #DEBUG_LINE_NO:487
    If isSKYUILoaded
      
    EndIf
  EndIf
  If isSKYUILoaded ; #DEBUG_LINE_NO:493
    Self.SendEvent_SKSE_CheckInterfacePackage() ; #DEBUG_LINE_NO:494
  EndIf
  If isSKSELoaded ; #DEBUG_LINE_NO:497
    Self.ModifyFurArmorNames() ; #DEBUG_LINE_NO:498
  EndIf
  Self.CheckIfModsAreLoaded() ; #DEBUG_LINE_NO:502
  If SummerSetIslesPresent == True ; #DEBUG_LINE_NO:506
    Form ssi_1 = Game.GetFormFromFile(11420013, "summersetisles.esp") ; #DEBUG_LINE_NO:507
    Form ssi_2 = Game.GetFormFromFile(2630364, "summersetisles.esp") ; #DEBUG_LINE_NO:508
    Form ssi_3 = Game.GetFormFromFile(2542064, "summersetisles.esp") ; #DEBUG_LINE_NO:509
    Form ssi_4 = Game.GetFormFromFile(817288, "summersetisles.esp") ; #DEBUG_LINE_NO:510
    Form ssi_5 = Game.GetFormFromFile(698744, "summersetisles.esp") ; #DEBUG_LINE_NO:511
    Form ssi_6 = Game.GetFormFromFile(668956, "summersetisles.esp") ; #DEBUG_LINE_NO:512
    If !_Frost_WorldspacesFTException.HasForm(ssi_1) ; #DEBUG_LINE_NO:515
      _Frost_WorldspacesFTException.AddForm(ssi_1) ; #DEBUG_LINE_NO:516
      _Frost_WorldspacesFTException.AddForm(ssi_2) ; #DEBUG_LINE_NO:517
      _Frost_WorldspacesFTException.AddForm(ssi_3) ; #DEBUG_LINE_NO:518
      _Frost_WorldspacesFTException.AddForm(ssi_4) ; #DEBUG_LINE_NO:519
      _Frost_WorldspacesFTException.AddForm(ssi_5) ; #DEBUG_LINE_NO:520
      _Frost_WorldspacesFTException.AddForm(ssi_6) ; #DEBUG_LINE_NO:521
    EndIf
  EndIf
  If ClimatesOfTamrielPresent == True ; #DEBUG_LINE_NO:526
    If !_Frost_SevereWeatherList.HasForm(Game.GetFormFromFile(17205786, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:527
      _Frost_SevereWeatherList.AddForm(Game.GetFormFromFile(17205786, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:528
      _Frost_SevereWeatherList.AddForm(Game.GetFormFromFile(17220953, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:529
      _Frost_SevereWeatherList.AddForm(Game.GetFormFromFile(17057850, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:530
      _Frost_SevereWeatherList.AddForm(Game.GetFormFromFile(17057848, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:531
      _Frost_SevereWeatherList.AddForm(Game.GetFormFromFile(17057846, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:532
      _Frost_SevereWeatherList.AddForm(Game.GetFormFromFile(17057842, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:533
      _Frost_SevereWeatherList.AddForm(Game.GetFormFromFile(17057841, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:534
    EndIf
    If !_Frost_OvercastWeatherList.HasForm(Game.GetFormFromFile(17057839, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:536
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057839, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:537
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057838, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:538
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057837, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:539
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057836, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:540
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057835, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:541
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057834, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:542
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057833, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:543
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057831, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:544
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057830, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:545
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057829, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:546
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17057828, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:547
      _Frost_OvercastWeatherList.AddForm(Game.GetFormFromFile(17053689, "ClimatesOfTamriel.esm")) ; #DEBUG_LINE_NO:548
    EndIf
  EndIf
  Self.RunCompatibilityArmors() ; #DEBUG_LINE_NO:553
  Debug.trace("[Frostfall]======================================================================================================", 0) ; #DEBUG_LINE_NO:556
  Debug.trace("[Frostfall]                      Frostfall start-up and compatibility checks complete.   \t\t                ", 0) ; #DEBUG_LINE_NO:557
  Debug.trace("[Frostfall]======================================================================================================", 0) ; #DEBUG_LINE_NO:558
  If isSKYUILoaded ; #DEBUG_LINE_NO:561
    Self.SendEvent_SKSE_LoadProfileOnStartup() ; #DEBUG_LINE_NO:562
  EndIf
  Self.RegisterForControlsOnLoad() ; #DEBUG_LINE_NO:566
  Self.RegisterForEventsOnLoad() ; #DEBUG_LINE_NO:567
  Self.RegisterForMenusOnLoad() ; #DEBUG_LINE_NO:568
  Self.AddStartupSpells() ; #DEBUG_LINE_NO:569
  Self.RegisterCampfireSkill() ; #DEBUG_LINE_NO:570
EndFunction

Function CheckIfModsAreLoaded()
  BeyondReachPresent = False ; #DEBUG_LINE_NO:579
  BrumaPresent = False ; #DEBUG_LINE_NO:580
  ChanterellePresent = False ; #DEBUG_LINE_NO:581
  CurseOfAkavirPhoePresent = False ; #DEBUG_LINE_NO:582
  DarkendPresent = False ; #DEBUG_LINE_NO:583
  HuntingGroundPresent = False ; #DEBUG_LINE_NO:584
  FalamyrrIslePresent = False ; #DEBUG_LINE_NO:585
  FalkreathCreekPresent = False ; #DEBUG_LINE_NO:586
  FalskaarPresent = False ; #DEBUG_LINE_NO:587
  FolkvangrPresent = False ; #DEBUG_LINE_NO:588
  JehannaHaafstadPresent = False ; #DEBUG_LINE_NO:589
  HangingGardensPresent = False ; #DEBUG_LINE_NO:590
  HuntersWorldPresent = False ; #DEBUG_LINE_NO:591
  VominheimPresent = False ; #DEBUG_LINE_NO:592
  LothbrukVillagePresent = False ; #DEBUG_LINE_NO:593
  MidwoodIslePresent = False ; #DEBUG_LINE_NO:594
  NyhusPresent = False ; #DEBUG_LINE_NO:595
  ShumerFallOfAllagardPresent = False ; #DEBUG_LINE_NO:596
  SkygerfallPresent = False ; #DEBUG_LINE_NO:597
  GrayCowlOfNocturnalPresent = False ; #DEBUG_LINE_NO:598
  SummerSetIslesPresent = False ; #DEBUG_LINE_NO:599
  TheHavenFromTheColdAndDarkPresent = False ; #DEBUG_LINE_NO:600
  TheIslandPresent = False ; #DEBUG_LINE_NO:601
  TheEgyptianPalaceOfAmarnaPresent = False ; #DEBUG_LINE_NO:602
  TheNilePresent = False ; #DEBUG_LINE_NO:603
  TheRepublicOfMasleaPresent = False ; #DEBUG_LINE_NO:604
  TheShirePresent = False ; #DEBUG_LINE_NO:605
  TheValleyOfPeacePresent = False ; #DEBUG_LINE_NO:606
  WyrmstoothPresent = False ; #DEBUG_LINE_NO:607
  LastSeedPresent = False ; #DEBUG_LINE_NO:609
  SkyRePresent = False ; #DEBUG_LINE_NO:610
  ClimatesOfTamrielPresent = False ; #DEBUG_LINE_NO:611
  WetAndColdPresent = False ; #DEBUG_LINE_NO:612
  ScenicCarriagesPresent = False ; #DEBUG_LINE_NO:613
  NumberOfMods = Game.GetModCount() ; #DEBUG_LINE_NO:616
  While NumberOfMods
    NumberOfMods -= 1 ; #DEBUG_LINE_NO:619
    NameOfMod = Game.GetModName(NumberOfMods) ; #DEBUG_LINE_NO:620
    If NameOfMod == "Dawnguard.esm" ; #DEBUG_LINE_NO:622
      isDLC1Loaded = True ; #DEBUG_LINE_NO:623
      Conditions.IsDawnguardLoaded = True ; #DEBUG_LINE_NO:624
      Self.DLC1LoadUp() ; #DEBUG_LINE_NO:625
    ElseIf NameOfMod == "Dragonborn.esm" ; #DEBUG_LINE_NO:626
      isDLC2Loaded = True ; #DEBUG_LINE_NO:627
      Conditions.IsDragonbornLoaded = True ; #DEBUG_LINE_NO:628
      Self.DLC2LoadUp() ; #DEBUG_LINE_NO:629
    ElseIf NameOfMod == "HearthFires.esm" ; #DEBUG_LINE_NO:630
      isHFLoaded = True ; #DEBUG_LINE_NO:631
      Conditions.IsHearthfireLoaded = True ; #DEBUG_LINE_NO:632
    ElseIf NameOfMod == "BSHeartland.esm" ; #DEBUG_LINE_NO:633
      BrumaPresent = True ; #DEBUG_LINE_NO:634
    ElseIf NameOfMod == "arnima.esm" ; #DEBUG_LINE_NO:635
      BeyondReachPresent = True ; #DEBUG_LINE_NO:636
    ElseIf NameOfMod == "Chanterelle World.esp" ; #DEBUG_LINE_NO:637
      ChanterellePresent = True ; #DEBUG_LINE_NO:638
    ElseIf NameOfMod == "Phoe.esm" ; #DEBUG_LINE_NO:639
      CurseOfAkavirPhoePresent = True ; #DEBUG_LINE_NO:640
    ElseIf NameOfMod == "StagPrinceBow.esp" ; #DEBUG_LINE_NO:641
      HuntingGroundPresent = True ; #DEBUG_LINE_NO:642
    ElseIf NameOfMod == "Darkend.esp" ; #DEBUG_LINE_NO:643
      DarkendPresent = True ; #DEBUG_LINE_NO:644
      Self.DRKLoadUp() ; #DEBUG_LINE_NO:645
    ElseIf NameOfMod == "FalamyrrIsle.esp" ; #DEBUG_LINE_NO:646
      FalamyrrIslePresent = True ; #DEBUG_LINE_NO:647
    ElseIf NameOfMod == "FC02.esp" ; #DEBUG_LINE_NO:648
      FalkreathCreekPresent = True ; #DEBUG_LINE_NO:649
    ElseIf NameOfMod == "Falskaar.esm" ; #DEBUG_LINE_NO:650
      FalskaarPresent = True ; #DEBUG_LINE_NO:651
    ElseIf NameOfMod == "Folkvangr.esp" ; #DEBUG_LINE_NO:652
      FolkvangrPresent = True ; #DEBUG_LINE_NO:653
    ElseIf NameOfMod == "Jehanna.esp" ; #DEBUG_LINE_NO:654
      JehannaHaafstadPresent = True ; #DEBUG_LINE_NO:655
    ElseIf NameOfMod == "bhabhilon.esp" ; #DEBUG_LINE_NO:656
      HangingGardensPresent = True ; #DEBUG_LINE_NO:657
    ElseIf NameOfMod == "HuntersWorld.esp" ; #DEBUG_LINE_NO:658
      HuntersWorldPresent = True ; #DEBUG_LINE_NO:659
    ElseIf NameOfMod == "vominheim.esp" ; #DEBUG_LINE_NO:660
      VominheimPresent = True ; #DEBUG_LINE_NO:661
    ElseIf NameOfMod == "Lothbruk Village (Snowy).esp" ; #DEBUG_LINE_NO:662
      LothbrukVillagePresent = True ; #DEBUG_LINE_NO:663
    ElseIf NameOfMod == "Midwood Isle.esp" ; #DEBUG_LINE_NO:664
      MidwoodIslePresent = True ; #DEBUG_LINE_NO:665
    ElseIf NameOfMod == "Nyhus.esp" ; #DEBUG_LINE_NO:666
      NyhusPresent = True ; #DEBUG_LINE_NO:667
    ElseIf NameOfMod == "ShumerWorld.esm" ; #DEBUG_LINE_NO:668
      ShumerFallOfAllagardPresent = True ; #DEBUG_LINE_NO:669
    ElseIf NameOfMod == "Daggerfall.esp" ; #DEBUG_LINE_NO:670
      SkygerfallPresent = True ; #DEBUG_LINE_NO:671
    ElseIf NameOfMod == "Gray Fox Cowl.esm" ; #DEBUG_LINE_NO:672
      GrayCowlOfNocturnalPresent = True ; #DEBUG_LINE_NO:673
    ElseIf NameOfMod == "summersestisles.esp" ; #DEBUG_LINE_NO:674
      SummerSetIslesPresent = True ; #DEBUG_LINE_NO:675
    ElseIf NameOfMod == "The Haven from the Cold and Dark.esp" ; #DEBUG_LINE_NO:676
      TheHavenFromTheColdAndDarkPresent = True ; #DEBUG_LINE_NO:677
    ElseIf NameOfMod == "TheIsland.esp" ; #DEBUG_LINE_NO:678
      TheIslandPresent = True ; #DEBUG_LINE_NO:679
    ElseIf NameOfMod == "Amarna.esp" ; #DEBUG_LINE_NO:680
      TheEgyptianPalaceOfAmarnaPresent = True ; #DEBUG_LINE_NO:681
    ElseIf NameOfMod == "nile.esp" ; #DEBUG_LINE_NO:682
      TheNilePresent = True ; #DEBUG_LINE_NO:683
    ElseIf NameOfMod == "Maslea.esm" ; #DEBUG_LINE_NO:684
      TheRepublicOfMasleaPresent = True ; #DEBUG_LINE_NO:685
    ElseIf NameOfMod == "TheBawbsShire.esp" ; #DEBUG_LINE_NO:686
      TheShirePresent = True ; #DEBUG_LINE_NO:687
    ElseIf NameOfMod == "valleyofpeace.esp" ; #DEBUG_LINE_NO:688
      TheValleyOfPeacePresent = True ; #DEBUG_LINE_NO:689
    ElseIf NameOfMod == "Wyrmstooth.esp" ; #DEBUG_LINE_NO:690
      WyrmstoothPresent = True ; #DEBUG_LINE_NO:691
      Self.WTHLoadUp() ; #DEBUG_LINE_NO:692
    ElseIf NameOfMod == "LastSeed.esp" ; #DEBUG_LINE_NO:695
      LastSeedPresent = True ; #DEBUG_LINE_NO:696
      Conditions.isLastSeedLoaded = True ; #DEBUG_LINE_NO:697
    ElseIf NameOfMod == "SkyRe_Main.esp" ; #DEBUG_LINE_NO:698
      SkyRePresent = True ; #DEBUG_LINE_NO:699
      Conditions.isSKYRELoaded = True ; #DEBUG_LINE_NO:700
    ElseIf NameOfMod == "ClimatesOfTamriel.esm" ; #DEBUG_LINE_NO:701
      ClimatesOfTamrielPresent = True ; #DEBUG_LINE_NO:702
    ElseIf NameOfMod == "WetandCold.esp" ; #DEBUG_LINE_NO:703
      WetAndColdPresent = True ; #DEBUG_LINE_NO:704
    ElseIf NameOfMod == "ScenicCarriages.esp" ; #DEBUG_LINE_NO:705
      ScenicCarriagesPresent = True ; #DEBUG_LINE_NO:706
    EndIf
  EndWhile
  If isDLC1Loaded == False ; #DEBUG_LINE_NO:711
    Conditions.IsDawnguardLoaded = False ; #DEBUG_LINE_NO:712
  EndIf
  If isDLC2Loaded == False ; #DEBUG_LINE_NO:714
    Conditions.IsDragonbornLoaded = False ; #DEBUG_LINE_NO:715
  EndIf
  If isHFLoaded == False ; #DEBUG_LINE_NO:717
    Conditions.IsHearthfireLoaded = False ; #DEBUG_LINE_NO:718
  EndIf
  If LastSeedPresent == False ; #DEBUG_LINE_NO:720
    Conditions.isLastSeedLoaded = False ; #DEBUG_LINE_NO:721
  EndIf
  If SkyRePresent == False ; #DEBUG_LINE_NO:723
    Conditions.isSKYRELoaded = False ; #DEBUG_LINE_NO:724
  EndIf
EndFunction

Function VanillaGameLoadUp()
  If added_spell_books == False ; #DEBUG_LINE_NO:738
    Self.AddSpellBooks() ; #DEBUG_LINE_NO:739
  EndIf
EndFunction

Function AddSpellBooks()
  If added_spell_books == False ; #DEBUG_LINE_NO:748
    LItemSpellTomes00AllIllusion.AddForm(_Frost_SpellTomeSoothe1 as Form, 1, 1) ; #DEBUG_LINE_NO:749
    LItemSpellTomes00AllSpells.AddForm(_Frost_SpellTomeSoothe1 as Form, 1, 1) ; #DEBUG_LINE_NO:750
    LItemSpellTomes00Illusion.AddForm(_Frost_SpellTomeSoothe1 as Form, 1, 1) ; #DEBUG_LINE_NO:751
    LItemSpellTomes00Spells.AddForm(_Frost_SpellTomeSoothe1 as Form, 1, 1) ; #DEBUG_LINE_NO:752
    LItemScroll00Skill.AddForm(_Frost_ScrollSoothe as Form, 1, 1) ; #DEBUG_LINE_NO:753
    LItemSpellTomes25AllAlteration.AddForm(_Frost_SpellTomeFoxskin as Form, 1, 1) ; #DEBUG_LINE_NO:754
    LItemSpellTomes25Alteration.AddForm(_Frost_SpellTomeFoxskin as Form, 1, 1) ; #DEBUG_LINE_NO:755
    LItemSpellTomes25AllIllusion.AddForm(_Frost_SpellTomeSoothe2 as Form, 1, 1) ; #DEBUG_LINE_NO:756
    LItemSpellTomes25Illusion.AddForm(_Frost_SpellTomeSoothe2 as Form, 1, 1) ; #DEBUG_LINE_NO:757
    LItemScroll25Skill.AddForm(_Frost_ScrollBask as Form, 1, 1) ; #DEBUG_LINE_NO:758
    LItemScroll25Skill.AddForm(_Frost_ScrollFoxskin as Form, 1, 1) ; #DEBUG_LINE_NO:759
    LItemSpellTomes50AllAlteration.AddForm(_Frost_SpellTomeWolfskin as Form, 1, 1) ; #DEBUG_LINE_NO:760
    LItemSpellTomes50Alteration.AddForm(_Frost_SpellTomeWolfskin as Form, 1, 1) ; #DEBUG_LINE_NO:761
    LItemSpellTomes50Spells.AddForm(_Frost_SpellTomeWolfskin as Form, 1, 1) ; #DEBUG_LINE_NO:762
    LitemSpellTomes50AllDestruction.AddForm(_Frost_SpellTomeVaporBlast as Form, 1, 1) ; #DEBUG_LINE_NO:763
    LitemSpellTomes50Destruction.AddForm(_Frost_SpellTomeVaporBlast as Form, 1, 1) ; #DEBUG_LINE_NO:764
    LItemSpellTomes50Spells.AddForm(_Frost_SpellTomeVaporBlast as Form, 1, 1) ; #DEBUG_LINE_NO:765
    LItemSpellTomes50AllIllusion.AddForm(_Frost_SpellTomeSoothe3 as Form, 1, 1) ; #DEBUG_LINE_NO:766
    LItemSpellTomes50Illusion.AddForm(_Frost_SpellTomeSoothe3 as Form, 1, 1) ; #DEBUG_LINE_NO:767
    LItemSpellTomes50Spells.AddForm(_Frost_SpellTomeSoothe3 as Form, 1, 1) ; #DEBUG_LINE_NO:768
    LItemSpellTOmes50AllRestoration.AddForm(_Frost_SpellTomeKindle as Form, 1, 1) ; #DEBUG_LINE_NO:769
    LItemSpellTOmes50Restoration.AddForm(_Frost_SpellTomeKindle as Form, 1, 1) ; #DEBUG_LINE_NO:770
    LItemSpellTomes50Spells.AddForm(_Frost_SpellTomeKindle as Form, 1, 1) ; #DEBUG_LINE_NO:771
    LItemScroll50Skill.AddForm(_Frost_ScrollRevel as Form, 1, 1) ; #DEBUG_LINE_NO:772
    LItemScroll50Skill.AddForm(_Frost_ScrollWolfskin as Form, 1, 1) ; #DEBUG_LINE_NO:773
    LItemScroll50Skill.AddForm(_Frost_ScrollVaporBlast as Form, 1, 1) ; #DEBUG_LINE_NO:774
    LItemScroll50Skill.AddForm(_Frost_ScrollKindle as Form, 1, 1) ; #DEBUG_LINE_NO:775
    LItemScroll50Skill.AddForm(_Frost_ScrollBoundCloakGreater as Form, 1, 1) ; #DEBUG_LINE_NO:776
    LItemSpellTomes75AllAlteration.AddForm(_Frost_SpellTomeTransmuteWood as Form, 1, 1) ; #DEBUG_LINE_NO:777
    LItemSpellTomes75Alteration.AddForm(_Frost_SpellTomeTransmuteWood as Form, 1, 1) ; #DEBUG_LINE_NO:778
    LItemSpellTomes75Spells.AddForm(_Frost_SpellTomeTransmuteWood as Form, 1, 1) ; #DEBUG_LINE_NO:779
    LItemSpellTomes75AllAlteration.AddForm(_Frost_SpellTomeBearskin as Form, 1, 1) ; #DEBUG_LINE_NO:780
    LItemSpellTomes75Alteration.AddForm(_Frost_SpellTomeBearskin as Form, 1, 1) ; #DEBUG_LINE_NO:781
    LItemSpellTomes75Spells.AddForm(_Frost_SpellTomeBearskin as Form, 1, 1) ; #DEBUG_LINE_NO:782
    LItemScroll75Skill.AddForm(_Frost_ScrollBearskin as Form, 1, 1) ; #DEBUG_LINE_NO:783
    added_spell_books = True ; #DEBUG_LINE_NO:785
  EndIf
EndFunction

Function AddStartupSpells()
  If isSKYUILoaded ; #DEBUG_LINE_NO:794
    PlayerRef.RemoveSpell(_Frost_LegacyConfig_Spell) ; #DEBUG_LINE_NO:795
    PlayerRef.RemoveSpell(_Frost_InspectEquipment_Spell) ; #DEBUG_LINE_NO:796
  Else
    PlayerRef.AddSpell(_Frost_LegacyConfig_Spell, False) ; #DEBUG_LINE_NO:798
    PlayerRef.AddSpell(_Frost_InspectEquipment_Spell, False) ; #DEBUG_LINE_NO:799
  EndIf
  If _Frost_HotkeyWeathersense.GetValueInt() != 0 ; #DEBUG_LINE_NO:801
    PlayerRef.RemoveSpell(_Frost_Weathersense_Spell) ; #DEBUG_LINE_NO:802
  Else
    PlayerRef.AddSpell(_Frost_Weathersense_Spell, False) ; #DEBUG_LINE_NO:804
  EndIf
  If !PlayerRef.HasPerk(_Frost_FrostResistWarmthModPerk) ; #DEBUG_LINE_NO:806
    PlayerRef.AddPerk(_Frost_FrostResistWarmthModPerk) ; #DEBUG_LINE_NO:807
  EndIf
  If PlayerRef.HasSpell(_Frost_RegionDetect as Form) ; #DEBUG_LINE_NO:809
    PlayerRef.RemoveSpell(_Frost_RegionDetect) ; #DEBUG_LINE_NO:810
  EndIf
  frostutil.GetFrostResistSystem().old_amount = 0.0 ; #DEBUG_LINE_NO:812
  frostutil.GetFrostResistSystem().CheckFrostResist() ; #DEBUG_LINE_NO:813
EndFunction

Int Function GetPlayerRegionTemp_FalmerValley(Float afPosX, Float afPosY)
  If Self.IsPointInPolygon(DLC1_FVBoss_PolyX, DLC1_FVBoss_PolyY, afPosX, afPosY) && PlayerRef.GetPositionZ() >= 8385.0 ; #DEBUG_LINE_NO:828
    Return 1 ; #DEBUG_LINE_NO:830
  ElseIf Self.IsPointInPolygon(DLC1_FVIce_PolyX, DLC1_FVIce_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:831
    Return 8 ; #DEBUG_LINE_NO:833
  ElseIf Self.IsPointInPolygon(DLC1_FVCanyon_PolyX, DLC1_FVCanyon_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:834
    Return 4 ; #DEBUG_LINE_NO:836
  ElseIf Self.IsPointInPolygon(DLC1_FVPlayground_PolyX, DLC1_FVPlayground_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:837
    Return 7 ; #DEBUG_LINE_NO:839
  ElseIf Self.IsPointInPolygon(DLC1_FVGrove_PolyX, DLC1_FVGrove_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:840
    Return 6 ; #DEBUG_LINE_NO:842
  Else
    Return -1 ; #DEBUG_LINE_NO:845
  EndIf
EndFunction

Int Function GetPlayerRegionTemp_Solstheim(Float afPosX, Float afPosY)
  If Self.IsPointInPolygon(DLC2_SolstheimArctic_PolyX, DLC2_SolstheimArctic_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:853
    Return 8 ; #DEBUG_LINE_NO:854
  Else
    Return 12 ; #DEBUG_LINE_NO:856
  EndIf
EndFunction

Int Function GetPlayerRegionTemp_Darkend(Float afPosX, Float afPosY)
  If Self.IsPointInPolygon(DNKD_Phalos_Frozen_PolyX, DNKD_Phalos_Frozen_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:864
    Return 8 ; #DEBUG_LINE_NO:865
  Else
    Return 6 ; #DEBUG_LINE_NO:867
  EndIf
EndFunction

Int Function GetPlayerRegionTemp_Wyrmstooth(Float afPosX, Float afPosY)
  If Self.IsPointInPolygon(Wyrmstooth_Center_PolyX, Wyrmstooth_Center_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:875
    Return 5 ; #DEBUG_LINE_NO:876
  ElseIf Self.IsPointInPolygon(Wyrmstooth_West_PolyX, Wyrmstooth_West_PolyY, afPosX, afPosY) ; #DEBUG_LINE_NO:877
    Return 5 ; #DEBUG_LINE_NO:878
  Else
    Return 8 ; #DEBUG_LINE_NO:880
  EndIf
EndFunction

Function DLC1LoadUp()
  Form DLC1_FalmerValley = Game.GetFormFromFile(2997, "Dawnguard.esm") ; #DEBUG_LINE_NO:894
  WS_FalmerValley = Game.GetFormFromFile(2997, "Dawnguard.esm") as WorldSpace ; #DEBUG_LINE_NO:895
  Form DLC1_SoulCairn = Game.GetFormFromFile(5128, "Dawnguard.esm") ; #DEBUG_LINE_NO:896
  WS_SoulCairn = Game.GetFormFromFile(5128, "Dawnguard.esm") as WorldSpace ; #DEBUG_LINE_NO:897
  Form DLC1_DayspringCanyon = Game.GetFormFromFile(7608, "Dawnguard.esm") ; #DEBUG_LINE_NO:898
  WS_DayspringCanyon = Game.GetFormFromFile(7608, "Dawnguard.esm") as WorldSpace ; #DEBUG_LINE_NO:899
  Form DLC1_AncestorsGlade = Game.GetFormFromFile(18631, "Dawnguard.esm") ; #DEBUG_LINE_NO:900
  WS_AncestorsGlade = Game.GetFormFromFile(18631, "Dawnguard.esm") as WorldSpace ; #DEBUG_LINE_NO:901
  Form DLC1_Boneyard = Game.GetFormFromFile(21133, "Dawnguard.esm") ; #DEBUG_LINE_NO:902
  WS_Boneyard = Game.GetFormFromFile(21133, "Dawnguard.esm") as WorldSpace ; #DEBUG_LINE_NO:903
  Form DLC1_VolkiharCourtyard = Game.GetFormFromFile(29186, "Dawnguard.esm") ; #DEBUG_LINE_NO:904
  WS_VolkiharCourtyard = Game.GetFormFromFile(29186, "Dawnguard.esm") as WorldSpace ; #DEBUG_LINE_NO:905
  If _Frost_WorldspacesExteriorOblivion && DLC1_SoulCairn && !_Frost_WorldspacesExteriorOblivion.HasForm(DLC1_SoulCairn) ; #DEBUG_LINE_NO:907
    _Frost_WorldspacesExteriorOblivion.AddForm(DLC1_SoulCairn) ; #DEBUG_LINE_NO:908
    If _Frost_WorldspacesExteriorFallForest && DLC1_DayspringCanyon
      _Frost_WorldspacesExteriorFallForest.AddForm(DLC1_DayspringCanyon) ; #DEBUG_LINE_NO:909
    EndIf
    If _Frost_WorldspacesExteriorPineForest && DLC1_AncestorsGlade
      _Frost_WorldspacesExteriorPineForest.AddForm(DLC1_AncestorsGlade) ; #DEBUG_LINE_NO:910
    EndIf
    If DLC1_Boneyard
      _Frost_WorldspacesExteriorOblivion.AddForm(DLC1_Boneyard) ; #DEBUG_LINE_NO:911
    EndIf
    If _Frost_WorldspacesExteriorCoast && DLC1_VolkiharCourtyard
      _Frost_WorldspacesExteriorCoast.AddForm(DLC1_VolkiharCourtyard) ; #DEBUG_LINE_NO:912
    EndIf
  EndIf
  If !DLC1_FVCanyon_PolyX ; #DEBUG_LINE_NO:915
    DLC1_FVCanyon_PolyX = new Float[5] ; #DEBUG_LINE_NO:916
  EndIf
  If !DLC1_FVCanyon_PolyY ; #DEBUG_LINE_NO:918
    DLC1_FVCanyon_PolyY = new Float[5] ; #DEBUG_LINE_NO:919
  EndIf
  If !DLC1_FVIce_PolyX ; #DEBUG_LINE_NO:921
    DLC1_FVIce_PolyX = new Float[8] ; #DEBUG_LINE_NO:922
  EndIf
  If !DLC1_FVIce_PolyY ; #DEBUG_LINE_NO:924
    DLC1_FVIce_PolyY = new Float[8] ; #DEBUG_LINE_NO:925
  EndIf
  If !DLC1_FVPlayground_PolyX ; #DEBUG_LINE_NO:927
    DLC1_FVPlayground_PolyX = new Float[6] ; #DEBUG_LINE_NO:928
  EndIf
  If !DLC1_FVPlayground_PolyY ; #DEBUG_LINE_NO:930
    DLC1_FVPlayground_PolyY = new Float[6] ; #DEBUG_LINE_NO:931
  EndIf
  If !DLC1_FVGrove_PolyX ; #DEBUG_LINE_NO:933
    DLC1_FVGrove_PolyX = new Float[5] ; #DEBUG_LINE_NO:934
  EndIf
  If !DLC1_FVGrove_PolyY ; #DEBUG_LINE_NO:936
    DLC1_FVGrove_PolyY = new Float[5] ; #DEBUG_LINE_NO:937
  EndIf
  If !DLC1_FVBoss_PolyX ; #DEBUG_LINE_NO:939
    DLC1_FVBoss_PolyX = new Float[5] ; #DEBUG_LINE_NO:940
  EndIf
  If !DLC1_FVBoss_PolyY ; #DEBUG_LINE_NO:942
    DLC1_FVBoss_PolyY = new Float[5] ; #DEBUG_LINE_NO:943
  EndIf
  If !DLC1_FVCanyon_PolyX[0] ; #DEBUG_LINE_NO:945
    DLC1_FVCanyon_PolyX[0] = -47273.0 ; #DEBUG_LINE_NO:946
    DLC1_FVCanyon_PolyX[1] = -4083.0 ; #DEBUG_LINE_NO:947
    DLC1_FVCanyon_PolyX[2] = 16369.0 ; #DEBUG_LINE_NO:948
    DLC1_FVCanyon_PolyX[3] = -31458.0 ; #DEBUG_LINE_NO:949
    DLC1_FVCanyon_PolyX[4] = -55597.0 ; #DEBUG_LINE_NO:950
  EndIf
  If !DLC1_FVIce_PolyX[0] ; #DEBUG_LINE_NO:952
    DLC1_FVIce_PolyX[0] = -22417.0 ; #DEBUG_LINE_NO:953
    DLC1_FVIce_PolyX[1] = 5287.0 ; #DEBUG_LINE_NO:954
    DLC1_FVIce_PolyX[2] = 17525.0 ; #DEBUG_LINE_NO:955
    DLC1_FVIce_PolyX[3] = 38431.0 ; #DEBUG_LINE_NO:956
    DLC1_FVIce_PolyX[4] = 47312.0 ; #DEBUG_LINE_NO:957
    DLC1_FVIce_PolyX[5] = 16369.0 ; #DEBUG_LINE_NO:958
    DLC1_FVIce_PolyX[6] = -4083.0 ; #DEBUG_LINE_NO:959
    DLC1_FVIce_PolyX[7] = -24967.0 ; #DEBUG_LINE_NO:960
  EndIf
  If !DLC1_FVPlayground_PolyX[0] ; #DEBUG_LINE_NO:962
    DLC1_FVPlayground_PolyX[0] = -47273.0 ; #DEBUG_LINE_NO:963
    DLC1_FVPlayground_PolyX[1] = -42686.0 ; #DEBUG_LINE_NO:964
    DLC1_FVPlayground_PolyX[2] = 24409.0 ; #DEBUG_LINE_NO:965
    DLC1_FVPlayground_PolyX[3] = 5287.0 ; #DEBUG_LINE_NO:966
    DLC1_FVPlayground_PolyX[4] = -22417.0 ; #DEBUG_LINE_NO:967
    DLC1_FVPlayground_PolyX[5] = -24967.0 ; #DEBUG_LINE_NO:968
  EndIf
  If !DLC1_FVGrove_PolyX[0] ; #DEBUG_LINE_NO:970
    DLC1_FVGrove_PolyX[0] = 24409.0 ; #DEBUG_LINE_NO:971
    DLC1_FVGrove_PolyX[1] = 46535.0 ; #DEBUG_LINE_NO:972
    DLC1_FVGrove_PolyX[2] = 58431.0 ; #DEBUG_LINE_NO:973
    DLC1_FVGrove_PolyX[3] = 17525.0 ; #DEBUG_LINE_NO:974
    DLC1_FVGrove_PolyX[4] = 5287.0 ; #DEBUG_LINE_NO:975
  EndIf
  If !DLC1_FVBoss_PolyX[0] ; #DEBUG_LINE_NO:977
    DLC1_FVBoss_PolyX[0] = -7340.0 ; #DEBUG_LINE_NO:978
    DLC1_FVBoss_PolyX[1] = -7065.0 ; #DEBUG_LINE_NO:979
    DLC1_FVBoss_PolyX[2] = -12013.0 ; #DEBUG_LINE_NO:980
    DLC1_FVBoss_PolyX[3] = -14487.0 ; #DEBUG_LINE_NO:981
    DLC1_FVBoss_PolyX[4] = -11023.0 ; #DEBUG_LINE_NO:982
  EndIf
  If !DLC1_FVCanyon_PolyY[0] ; #DEBUG_LINE_NO:984
    DLC1_FVCanyon_PolyY[0] = 15175.0 ; #DEBUG_LINE_NO:985
    DLC1_FVCanyon_PolyY[1] = -16276.0 ; #DEBUG_LINE_NO:986
    DLC1_FVCanyon_PolyY[2] = -43088.0 ; #DEBUG_LINE_NO:987
    DLC1_FVCanyon_PolyY[3] = -43787.0 ; #DEBUG_LINE_NO:988
    DLC1_FVCanyon_PolyY[4] = -18209.0 ; #DEBUG_LINE_NO:989
  EndIf
  If !DLC1_FVIce_PolyY[0] ; #DEBUG_LINE_NO:991
    DLC1_FVIce_PolyY[0] = 15633.0 ; #DEBUG_LINE_NO:992
    DLC1_FVIce_PolyY[1] = 16908.0 ; #DEBUG_LINE_NO:993
    DLC1_FVIce_PolyY[2] = -2680.0 ; #DEBUG_LINE_NO:994
    DLC1_FVIce_PolyY[3] = 10491.0 ; #DEBUG_LINE_NO:995
    DLC1_FVIce_PolyY[4] = -10372.0 ; #DEBUG_LINE_NO:996
    DLC1_FVIce_PolyY[5] = -43088.0 ; #DEBUG_LINE_NO:997
    DLC1_FVIce_PolyY[6] = -16276.0 ; #DEBUG_LINE_NO:998
    DLC1_FVIce_PolyY[7] = -6122.0 ; #DEBUG_LINE_NO:999
  EndIf
  If !DLC1_FVPlayground_PolyY[0] ; #DEBUG_LINE_NO:1001
    DLC1_FVPlayground_PolyY[0] = 15175.0 ; #DEBUG_LINE_NO:1002
    DLC1_FVPlayground_PolyY[1] = 40024.0 ; #DEBUG_LINE_NO:1003
    DLC1_FVPlayground_PolyY[2] = 50095.0 ; #DEBUG_LINE_NO:1004
    DLC1_FVPlayground_PolyY[3] = 16908.0 ; #DEBUG_LINE_NO:1005
    DLC1_FVPlayground_PolyY[4] = 15633.0 ; #DEBUG_LINE_NO:1006
    DLC1_FVPlayground_PolyY[5] = -6122.0 ; #DEBUG_LINE_NO:1007
  EndIf
  If !DLC1_FVGrove_PolyY[0] ; #DEBUG_LINE_NO:1009
    DLC1_FVGrove_PolyY[0] = 50095.0 ; #DEBUG_LINE_NO:1010
    DLC1_FVGrove_PolyY[1] = 17714.0 ; #DEBUG_LINE_NO:1011
    DLC1_FVGrove_PolyY[2] = 10491.0 ; #DEBUG_LINE_NO:1012
    DLC1_FVGrove_PolyY[3] = -2680.0 ; #DEBUG_LINE_NO:1013
    DLC1_FVGrove_PolyY[4] = 16908.0 ; #DEBUG_LINE_NO:1014
  EndIf
  If !DLC1_FVBoss_PolyY[0] ; #DEBUG_LINE_NO:1016
    DLC1_FVBoss_PolyY[0] = -7244.0 ; #DEBUG_LINE_NO:1017
    DLC1_FVBoss_PolyY[1] = -9662.0 ; #DEBUG_LINE_NO:1018
    DLC1_FVBoss_PolyY[2] = -14170.0 ; #DEBUG_LINE_NO:1019
    DLC1_FVBoss_PolyY[3] = -10432.0 ; #DEBUG_LINE_NO:1020
    DLC1_FVBoss_PolyY[4] = -7244.0 ; #DEBUG_LINE_NO:1021
  EndIf
EndFunction

Function DLC2LoadUp()
  If isDLC2Loaded == True ; #DEBUG_LINE_NO:1031
    Form DLC2_Solstheim = Game.GetFormFromFile(2048, "Dragonborn.esm") ; #DEBUG_LINE_NO:1032
    WS_Solstheim = Game.GetFormFromFile(2048, "Dragonborn.esm") as WorldSpace ; #DEBUG_LINE_NO:1033
    Form DLC2_Apocrypha = Game.GetFormFromFile(114866, "Dragonborn.esm") ; #DEBUG_LINE_NO:1034
    WS_Apocrypha = Game.GetFormFromFile(114866, "Dragonborn.esm") as WorldSpace ; #DEBUG_LINE_NO:1035
    If _Frost_WorldspacesExteriorOblivion && DLC2_Apocrypha && !_Frost_WorldspacesExteriorOblivion.HasForm(DLC2_Apocrypha) ; #DEBUG_LINE_NO:1036
      _Frost_WorldspacesExteriorOblivion.AddForm(DLC2_Apocrypha) ; #DEBUG_LINE_NO:1037
    EndIf
  EndIf
  If !DLC2_SolstheimArctic_PolyX ; #DEBUG_LINE_NO:1041
    DLC2_SolstheimArctic_PolyX = new Float[18] ; #DEBUG_LINE_NO:1042
  EndIf
  If !DLC2_SolstheimArctic_PolyY ; #DEBUG_LINE_NO:1044
    DLC2_SolstheimArctic_PolyY = new Float[18] ; #DEBUG_LINE_NO:1045
  EndIf
  If !DLC2_SolstheimArctic_PolyX[0] ; #DEBUG_LINE_NO:1048
    DLC2_SolstheimArctic_PolyX[0] = 19400.0 ; #DEBUG_LINE_NO:1049
    DLC2_SolstheimArctic_PolyX[1] = 23549.0 ; #DEBUG_LINE_NO:1050
    DLC2_SolstheimArctic_PolyX[2] = 23854.0 ; #DEBUG_LINE_NO:1051
    DLC2_SolstheimArctic_PolyX[3] = 23038.0 ; #DEBUG_LINE_NO:1052
    DLC2_SolstheimArctic_PolyX[4] = 20764.0 ; #DEBUG_LINE_NO:1053
    DLC2_SolstheimArctic_PolyX[5] = 25385.0 ; #DEBUG_LINE_NO:1054
    DLC2_SolstheimArctic_PolyX[6] = 28895.0 ; #DEBUG_LINE_NO:1055
    DLC2_SolstheimArctic_PolyX[7] = 28665.0 ; #DEBUG_LINE_NO:1056
    DLC2_SolstheimArctic_PolyX[8] = 33574.0 ; #DEBUG_LINE_NO:1057
    DLC2_SolstheimArctic_PolyX[9] = 37186.0 ; #DEBUG_LINE_NO:1058
    DLC2_SolstheimArctic_PolyX[10] = 72619.0 ; #DEBUG_LINE_NO:1059
    DLC2_SolstheimArctic_PolyX[11] = 72922.0 ; #DEBUG_LINE_NO:1060
    DLC2_SolstheimArctic_PolyX[12] = 78100.0 ; #DEBUG_LINE_NO:1061
    DLC2_SolstheimArctic_PolyX[13] = 79563.0 ; #DEBUG_LINE_NO:1062
    DLC2_SolstheimArctic_PolyX[14] = 107700.0 ; #DEBUG_LINE_NO:1063
    DLC2_SolstheimArctic_PolyX[15] = 107700.0 ; #DEBUG_LINE_NO:1064
    DLC2_SolstheimArctic_PolyX[16] = 2000.0 ; #DEBUG_LINE_NO:1065
    DLC2_SolstheimArctic_PolyX[17] = 2000.0 ; #DEBUG_LINE_NO:1066
  EndIf
  If !DLC2_SolstheimArctic_PolyY[0] ; #DEBUG_LINE_NO:1068
    DLC2_SolstheimArctic_PolyY[0] = 77192.0 ; #DEBUG_LINE_NO:1069
    DLC2_SolstheimArctic_PolyY[1] = 75957.0 ; #DEBUG_LINE_NO:1070
    DLC2_SolstheimArctic_PolyY[2] = 71695.0 ; #DEBUG_LINE_NO:1071
    DLC2_SolstheimArctic_PolyY[3] = 64635.0 ; #DEBUG_LINE_NO:1072
    DLC2_SolstheimArctic_PolyY[4] = 58523.0 ; #DEBUG_LINE_NO:1073
    DLC2_SolstheimArctic_PolyY[5] = 57941.0 ; #DEBUG_LINE_NO:1074
    DLC2_SolstheimArctic_PolyY[6] = 50985.0 ; #DEBUG_LINE_NO:1075
    DLC2_SolstheimArctic_PolyY[7] = 46571.0 ; #DEBUG_LINE_NO:1076
    DLC2_SolstheimArctic_PolyY[8] = 47793.0 ; #DEBUG_LINE_NO:1077
    DLC2_SolstheimArctic_PolyY[9] = 49747.0 ; #DEBUG_LINE_NO:1078
    DLC2_SolstheimArctic_PolyY[10] = 54769.0 ; #DEBUG_LINE_NO:1079
    DLC2_SolstheimArctic_PolyY[11] = 60439.0 ; #DEBUG_LINE_NO:1080
    DLC2_SolstheimArctic_PolyY[12] = 60496.0 ; #DEBUG_LINE_NO:1081
    DLC2_SolstheimArctic_PolyY[13] = 63665.0 ; #DEBUG_LINE_NO:1082
    DLC2_SolstheimArctic_PolyY[14] = 64000.0 ; #DEBUG_LINE_NO:1083
    DLC2_SolstheimArctic_PolyY[15] = 106000.0 ; #DEBUG_LINE_NO:1084
    DLC2_SolstheimArctic_PolyY[16] = 106000.0 ; #DEBUG_LINE_NO:1085
    DLC2_SolstheimArctic_PolyY[17] = 77200.0 ; #DEBUG_LINE_NO:1086
  EndIf
  Form Book1 = Game.GetFormFromFile(159981, "Dragonborn.esm") ; #DEBUG_LINE_NO:1090
  Form Book2 = Game.GetFormFromFile(159982, "Dragonborn.esm") ; #DEBUG_LINE_NO:1091
  Form Book3 = Game.GetFormFromFile(159983, "Dragonborn.esm") ; #DEBUG_LINE_NO:1092
  Form Book4 = Game.GetFormFromFile(159984, "Dragonborn.esm") ; #DEBUG_LINE_NO:1093
  Form Book5 = Game.GetFormFromFile(159985, "Dragonborn.esm") ; #DEBUG_LINE_NO:1094
  Form Book6 = Game.GetFormFromFile(159986, "Dragonborn.esm") ; #DEBUG_LINE_NO:1095
  Form Book7 = Game.GetFormFromFile(159987, "Dragonborn.esm") ; #DEBUG_LINE_NO:1096
  If !_Frost_FastTravelExceptions.HasForm(Book1) ; #DEBUG_LINE_NO:1097
    _Frost_FastTravelExceptions.AddForm(Book1) ; #DEBUG_LINE_NO:1098
  EndIf
  If !_Frost_FastTravelExceptions.HasForm(Book2) ; #DEBUG_LINE_NO:1100
    _Frost_FastTravelExceptions.AddForm(Book2) ; #DEBUG_LINE_NO:1101
  EndIf
  If !_Frost_FastTravelExceptions.HasForm(Book3) ; #DEBUG_LINE_NO:1103
    _Frost_FastTravelExceptions.AddForm(Book3) ; #DEBUG_LINE_NO:1104
  EndIf
  If !_Frost_FastTravelExceptions.HasForm(Book4) ; #DEBUG_LINE_NO:1106
    _Frost_FastTravelExceptions.AddForm(Book4) ; #DEBUG_LINE_NO:1107
  EndIf
  If !_Frost_FastTravelExceptions.HasForm(Book5) ; #DEBUG_LINE_NO:1109
    _Frost_FastTravelExceptions.AddForm(Book5) ; #DEBUG_LINE_NO:1110
  EndIf
  If !_Frost_FastTravelExceptions.HasForm(Book6) ; #DEBUG_LINE_NO:1112
    _Frost_FastTravelExceptions.AddForm(Book6) ; #DEBUG_LINE_NO:1113
  EndIf
  If !_Frost_FastTravelExceptions.HasForm(Book7) ; #DEBUG_LINE_NO:1115
    _Frost_FastTravelExceptions.AddForm(Book7) ; #DEBUG_LINE_NO:1116
  EndIf
EndFunction

Function DRKLoadUp()
  Form orb = Game.GetFormFromFile(754804, "Darkend.esp") ; #DEBUG_LINE_NO:1129
  If !_Camp_HeatSources_All.HasForm(orb) ; #DEBUG_LINE_NO:1130
    _Camp_HeatSources_All.AddForm(orb) ; #DEBUG_LINE_NO:1131
  EndIf
  If !_Camp_HeatSources_Other.HasForm(orb) ; #DEBUG_LINE_NO:1133
    _Camp_HeatSources_Other.AddForm(orb) ; #DEBUG_LINE_NO:1134
  EndIf
  If !WS_Darkend ; #DEBUG_LINE_NO:1136
    WS_Darkend = Game.GetFormFromFile(3426, "Darkend.esp") as WorldSpace ; #DEBUG_LINE_NO:1137
  EndIf
  If !DNKD_Phalos_Frozen_PolyX ; #DEBUG_LINE_NO:1139
    DNKD_Phalos_Frozen_PolyX = new Float[4] ; #DEBUG_LINE_NO:1140
  EndIf
  If !DNKD_Phalos_Frozen_PolyY ; #DEBUG_LINE_NO:1142
    DNKD_Phalos_Frozen_PolyY = new Float[4] ; #DEBUG_LINE_NO:1143
  EndIf
  If !DNKD_Phalos_Frozen_PolyX[0] ; #DEBUG_LINE_NO:1145
    DNKD_Phalos_Frozen_PolyX[0] = 931.0 ; #DEBUG_LINE_NO:1146
    DNKD_Phalos_Frozen_PolyX[1] = 19951.0 ; #DEBUG_LINE_NO:1147
    DNKD_Phalos_Frozen_PolyX[2] = 28261.0 ; #DEBUG_LINE_NO:1148
    DNKD_Phalos_Frozen_PolyX[3] = -4750.0 ; #DEBUG_LINE_NO:1149
  EndIf
  If !DNKD_Phalos_Frozen_PolyY[0] ; #DEBUG_LINE_NO:1151
    DNKD_Phalos_Frozen_PolyY[0] = 14542.0 ; #DEBUG_LINE_NO:1152
    DNKD_Phalos_Frozen_PolyY[1] = 6015.0 ; #DEBUG_LINE_NO:1153
    DNKD_Phalos_Frozen_PolyY[2] = 49880.0 ; #DEBUG_LINE_NO:1154
    DNKD_Phalos_Frozen_PolyY[3] = 49880.0 ; #DEBUG_LINE_NO:1155
  EndIf
EndFunction

Function WTHLoadUp()
  If !WS_Wyrmstooth ; #DEBUG_LINE_NO:1164
    WS_Wyrmstooth = Game.GetFormFromFile(16780642, "Wyrmstooth.esp") as WorldSpace ; #DEBUG_LINE_NO:1165
  EndIf
  If !_Camp_WorldspacesInteriors.HasForm(Game.GetFormFromFile(17311201, "Wyrmstooth.esp")) ; #DEBUG_LINE_NO:1167
    _Camp_WorldspacesInteriors.AddForm(Game.GetFormFromFile(17311201, "Wyrmstooth.esp")) ; #DEBUG_LINE_NO:1168
  EndIf
  If !Wyrmstooth_Center_PolyX ; #DEBUG_LINE_NO:1170
    Wyrmstooth_Center_PolyX = new Float[5] ; #DEBUG_LINE_NO:1171
  EndIf
  If !Wyrmstooth_Center_PolyY ; #DEBUG_LINE_NO:1173
    Wyrmstooth_Center_PolyY = new Float[5] ; #DEBUG_LINE_NO:1174
  EndIf
  If !Wyrmstooth_West_PolyX ; #DEBUG_LINE_NO:1176
    Wyrmstooth_West_PolyX = new Float[8] ; #DEBUG_LINE_NO:1177
  EndIf
  If !Wyrmstooth_West_PolyY ; #DEBUG_LINE_NO:1179
    Wyrmstooth_West_PolyY = new Float[8] ; #DEBUG_LINE_NO:1180
  EndIf
  If !Wyrmstooth_Center_PolyX[0] ; #DEBUG_LINE_NO:1182
    Wyrmstooth_Center_PolyX[0] = 19045.19921875 ; #DEBUG_LINE_NO:1183
    Wyrmstooth_Center_PolyX[1] = 13357.799804688 ; #DEBUG_LINE_NO:1184
    Wyrmstooth_Center_PolyX[2] = 19684.599609375 ; #DEBUG_LINE_NO:1185
    Wyrmstooth_Center_PolyX[3] = 41285.80078125 ; #DEBUG_LINE_NO:1186
    Wyrmstooth_Center_PolyX[4] = 25999.5 ; #DEBUG_LINE_NO:1187
  EndIf
  If !Wyrmstooth_Center_PolyY[0] ; #DEBUG_LINE_NO:1189
    Wyrmstooth_Center_PolyY[0] = 727.359985352 ; #DEBUG_LINE_NO:1190
    Wyrmstooth_Center_PolyY[1] = -10888.5 ; #DEBUG_LINE_NO:1191
    Wyrmstooth_Center_PolyY[2] = -18279.099609375 ; #DEBUG_LINE_NO:1192
    Wyrmstooth_Center_PolyY[3] = 3264.520019531 ; #DEBUG_LINE_NO:1193
    Wyrmstooth_Center_PolyY[4] = 8109.009765625 ; #DEBUG_LINE_NO:1194
  EndIf
  If !Wyrmstooth_West_PolyX[0] ; #DEBUG_LINE_NO:1196
    Wyrmstooth_West_PolyX[0] = -184.0 ; #DEBUG_LINE_NO:1197
    Wyrmstooth_West_PolyX[1] = -6402.0 ; #DEBUG_LINE_NO:1198
    Wyrmstooth_West_PolyX[2] = -16690.0 ; #DEBUG_LINE_NO:1199
    Wyrmstooth_West_PolyX[3] = -14528.0 ; #DEBUG_LINE_NO:1200
    Wyrmstooth_West_PolyX[4] = -10068.0 ; #DEBUG_LINE_NO:1201
    Wyrmstooth_West_PolyX[5] = -11671.0 ; #DEBUG_LINE_NO:1202
    Wyrmstooth_West_PolyX[6] = -70148.0 ; #DEBUG_LINE_NO:1203
    Wyrmstooth_West_PolyX[7] = -63280.0 ; #DEBUG_LINE_NO:1204
  EndIf
  If !Wyrmstooth_West_PolyY[0] ; #DEBUG_LINE_NO:1206
    Wyrmstooth_West_PolyY[0] = 17652.0 ; #DEBUG_LINE_NO:1207
    Wyrmstooth_West_PolyY[1] = -3939.0 ; #DEBUG_LINE_NO:1208
    Wyrmstooth_West_PolyY[2] = -8281.0 ; #DEBUG_LINE_NO:1209
    Wyrmstooth_West_PolyY[3] = -17718.0 ; #DEBUG_LINE_NO:1210
    Wyrmstooth_West_PolyY[4] = -29543.0 ; #DEBUG_LINE_NO:1211
    Wyrmstooth_West_PolyY[5] = -18706.0 ; #DEBUG_LINE_NO:1212
    Wyrmstooth_West_PolyY[6] = -29523.0 ; #DEBUG_LINE_NO:1213
    Wyrmstooth_West_PolyY[7] = 52329.0 ; #DEBUG_LINE_NO:1214
  EndIf
EndFunction

Bool Function IsPointInPolygon(Float[] polyX, Float[] polyY, Float x, Float y)
  If polyX.Length != polyY.Length ; #DEBUG_LINE_NO:1226
    Return False ; #DEBUG_LINE_NO:1227
  EndIf
  Int polySides = polyX.Length ; #DEBUG_LINE_NO:1229
  Int i = 0 ; #DEBUG_LINE_NO:1230
  Int j = polySides - 1 ; #DEBUG_LINE_NO:1231
  Bool oddNodes = False ; #DEBUG_LINE_NO:1232
  While i < polySides ; #DEBUG_LINE_NO:1233
    If (polyY[i] < y && polyY[j] >= y || polyY[j] < y && polyY[i] >= y) && (polyX[i] <= x || polyX[j] <= x) ; #DEBUG_LINE_NO:1234
      If polyX[i] + (y - polyY[i]) / (polyY[j] - polyY[i]) * (polyX[j] - polyX[i]) < x ; #DEBUG_LINE_NO:1235
        oddNodes = !oddNodes ; #DEBUG_LINE_NO:1236
      EndIf
    EndIf
    j = i ; #DEBUG_LINE_NO:1239
    i += 1 ; #DEBUG_LINE_NO:1240
  EndWhile
  Return oddNodes ; #DEBUG_LINE_NO:1242
EndFunction

Function WACLoadUp()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1305
  If frostutil.ArmorProtectionDataExistsByKey("860640___WetandCold.esp") ; #DEBUG_LINE_NO:1306
    Return  ; #DEBUG_LINE_NO:1307
  EndIf
  handler.SetArmorDataByKey("860640___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1310
  handler.SetArmorDataByKey("860649___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1311
  handler.SetArmorDataByKey("864795___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1312
  handler.SetArmorDataByKey("864791___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1313
  handler.SetArmorDataByKey("864794___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1314
  handler.SetArmorDataByKey("864796___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1315
  handler.SetArmorDataByKey("864792___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1316
  handler.SetArmorDataByKey("864793___WetandCold.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1317
  handler.SetArmorDataByKey("415000___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1318
  handler.SetArmorDataByKey("514265___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1319
  handler.SetArmorDataByKey("416384___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1320
  handler.SetArmorDataByKey("416380___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1321
  handler.SetArmorDataByKey("831666___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1322
  handler.SetArmorDataByKey("831673___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1323
  handler.SetArmorDataByKey("831674___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1324
  handler.SetArmorDataByKey("831675___WetandCold.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1325
  handler.SetArmorDataByKey("152448___WetandCold.esp", handler.GEARTYPE_HANDS, 5, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1327
  handler.SetArmorDataByKey("698278___WetandCold.esp", handler.GEARTYPE_HANDS, 5, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1328
  handler.SetArmorDataByKey("152450___WetandCold.esp", handler.GEARTYPE_HANDS, 5, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1329
  handler.SetArmorDataByKey("698279___WetandCold.esp", handler.GEARTYPE_HANDS, 5, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1330
  handler.SetArmorDataByKey("152451___WetandCold.esp", handler.GEARTYPE_HANDS, 5, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1331
  handler.SetArmorDataByKey("95879___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1333
  handler.SetArmorDataByKey("334976___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1334
  handler.SetArmorDataByKey("95880___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1335
  handler.SetArmorDataByKey("104164___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1336
  handler.SetArmorDataByKey("97267___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1337
  handler.SetArmorDataByKey("104163___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1338
  handler.SetArmorDataByKey("450851___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1339
  handler.SetArmorDataByKey("804073___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1340
  handler.SetArmorDataByKey("804074___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1341
  handler.SetArmorDataByKey("804075___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1342
  handler.SetArmorDataByKey("804076___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1343
  handler.SetArmorDataByKey("804077___WetandCold.esp", handler.GEARTYPE_HEAD, 35, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1344
  handler.SetArmorDataByKey("146916___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1345
  handler.SetArmorDataByKey("146917___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1346
  handler.SetArmorDataByKey("699670___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1347
  handler.SetArmorDataByKey("146918___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1348
  handler.SetArmorDataByKey("873070___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1349
  handler.SetArmorDataByKey("874470___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1350
  handler.SetArmorDataByKey("874471___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1351
  handler.SetArmorDataByKey("874472___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1352
  handler.SetArmorDataByKey("874473___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1353
  handler.SetArmorDataByKey("874476___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1354
  handler.SetArmorDataByKey("874481___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1355
  handler.SetArmorDataByKey("874482___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1356
  handler.SetArmorDataByKey("841332___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1357
  handler.SetArmorDataByKey("842717___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1358
  handler.SetArmorDataByKey("842718___WetandCold.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1359
EndFunction

Function NFHLoadUp()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1368
  If frostutil.ArmorProtectionDataExistsByKey("18655___Northborn Fur Hoods.esp") ; #DEBUG_LINE_NO:1369
    Return  ; #DEBUG_LINE_NO:1370
  EndIf
  handler.SetArmorDataByKey("18655___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1372
  handler.SetArmorDataByKey("18654___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1373
  handler.SetArmorDataByKey("18653___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1374
  handler.SetArmorDataByKey("18652___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1375
  handler.SetArmorDataByKey("18651___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1376
  handler.SetArmorDataByKey("18650___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1377
  handler.SetArmorDataByKey("18649___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1378
  handler.SetArmorDataByKey("18648___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1379
  handler.SetArmorDataByKey("7567___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1380
  handler.SetArmorDataByKey("8949___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1381
  handler.SetArmorDataByKey("764315___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1382
  handler.SetArmorDataByKey("7566___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1383
  handler.SetArmorDataByKey("764314___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1384
  handler.SetArmorDataByKey("8957___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1385
  handler.SetArmorDataByKey("8956___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1386
  handler.SetArmorDataByKey("764316___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1387
  handler.SetArmorDataByKey("6185___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1388
  handler.SetArmorDataByKey("18656___Northborn Fur Hoods.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1389
EndFunction

Function COSLoadUp()
  Self.AddCOSDatastoreEntries("Complete Crafting Overhaul_Remade.esp") ; #DEBUG_LINE_NO:1397
  Self.AddCOSDatastoreEntries("Cloaks.esp") ; #DEBUG_LINE_NO:1398
  Self.AddCOSDatastoreEntries("Cloaks - Player Only.esp") ; #DEBUG_LINE_NO:1399
  Self.AddCOSDatastoreEntries("Cloaks - No Imperial.esp") ; #DEBUG_LINE_NO:1400
EndFunction

Function AddCOSDatastoreEntries(String asPluginName)
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1407
  If frostutil.ArmorProtectionDataExistsByKey("58747___" + asPluginName) ; #DEBUG_LINE_NO:1408
    Return  ; #DEBUG_LINE_NO:1409
  EndIf
  handler.SetArmorDataByKey("58747___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1413
  handler.SetArmorDataByKey("53213___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1414
  handler.SetArmorDataByKey("49074___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1415
  handler.SetArmorDataByKey("33856___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1416
  handler.SetArmorDataByKey("62998___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1417
  handler.SetArmorDataByKey("62977___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1418
  handler.SetArmorDataByKey("61588___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1419
  handler.SetArmorDataByKey("28327___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1420
  handler.SetArmorDataByKey("28329___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1421
  handler.SetArmorDataByKey("53221___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1422
  handler.SetArmorDataByKey("67140___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1423
  handler.SetArmorDataByKey("58751___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1424
  handler.SetArmorDataByKey("61587___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1425
  handler.SetArmorDataByKey("75456___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1426
  handler.SetArmorDataByKey("75455___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1427
  handler.SetArmorDataByKey("76856___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1428
  handler.SetArmorDataByKey("76854___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1429
  handler.SetArmorDataByKey("76852___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1430
  handler.SetArmorDataByKey("76850___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1431
  handler.SetArmorDataByKey("74045___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1432
  handler.SetArmorDataByKey("74046___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1433
  handler.SetArmorDataByKey("74047___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1434
  handler.SetArmorDataByKey("74048___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1435
  handler.SetArmorDataByKey("74043___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1436
  handler.SetArmorDataByKey("74044___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1437
  handler.SetArmorDataByKey("68520___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1438
  handler.SetArmorDataByKey("68522___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1439
  handler.SetArmorDataByKey("62979___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1440
  handler.SetArmorDataByKey("62980___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1441
  handler.SetArmorDataByKey("62981___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1442
  handler.SetArmorDataByKey("62982___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1443
  handler.SetArmorDataByKey("62983___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1444
  handler.SetArmorDataByKey("62984___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1445
  handler.SetArmorDataByKey("62985___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1446
  handler.SetArmorDataByKey("74062___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1447
  handler.SetArmorDataByKey("74063___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1448
  handler.SetArmorDataByKey("74066___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1449
  handler.SetArmorDataByKey("74068___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1450
  handler.SetArmorDataByKey("74070___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1451
  handler.SetArmorDataByKey("74072___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1452
  handler.SetArmorDataByKey("74074___" + asPluginName, handler.GEARTYPE_CLOAK, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1453
  handler.SetArmorDataByKey("58748___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1456
  handler.SetArmorDataByKey("40785___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1457
  handler.SetArmorDataByKey("46316___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1458
  handler.SetArmorDataByKey("32476___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1459
  handler.SetArmorDataByKey("25551___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1460
  handler.SetArmorDataByKey("24169___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1461
  handler.SetArmorDataByKey("25552___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1462
  handler.SetArmorDataByKey("58749___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1463
  handler.SetArmorDataByKey("62995___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1464
  handler.SetArmorDataByKey("53223___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1465
  handler.SetArmorDataByKey("42172___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1466
  handler.SetArmorDataByKey("42170___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1467
  handler.SetArmorDataByKey("38022___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1468
  handler.SetArmorDataByKey("22786___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1469
  handler.SetArmorDataByKey("21380___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1470
  handler.SetArmorDataByKey("21390___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1471
  handler.SetArmorDataByKey("21391___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1472
  handler.SetArmorDataByKey("21392___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1473
  handler.SetArmorDataByKey("21393___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1474
  handler.SetArmorDataByKey("21394___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1475
  handler.SetArmorDataByKey("21395___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1476
  handler.SetArmorDataByKey("21396___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1477
  handler.SetArmorDataByKey("21397___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1478
  handler.SetArmorDataByKey("21379___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1479
  handler.SetArmorDataByKey("22785___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1480
  handler.SetArmorDataByKey("22784___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1481
  handler.SetArmorDataByKey("22783___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1482
  handler.SetArmorDataByKey("25557___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1483
  handler.SetArmorDataByKey("25563___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1484
  handler.SetArmorDataByKey("72658___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1485
  handler.SetArmorDataByKey("74064___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1486
  handler.SetArmorDataByKey("74065___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1487
  handler.SetArmorDataByKey("74067___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1488
  handler.SetArmorDataByKey("74069___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1489
  handler.SetArmorDataByKey("74071___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1490
  handler.SetArmorDataByKey("74073___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1491
  handler.SetArmorDataByKey("83903___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1492
  handler.SetArmorDataByKey("1066944___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1493
  handler.SetArmorDataByKey("1066945___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1494
  handler.SetArmorDataByKey("1066946___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1495
  handler.SetArmorDataByKey("1066947___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1496
  handler.SetArmorDataByKey("1066948___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1497
  handler.SetArmorDataByKey("1066949___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1498
  handler.SetArmorDataByKey("1066950___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1499
  handler.SetArmorDataByKey("1066951___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1500
  handler.SetArmorDataByKey("50454___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1503
  handler.SetArmorDataByKey("53219___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1504
  handler.SetArmorDataByKey("38016___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1505
  handler.SetArmorDataByKey("29714___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1506
  handler.SetArmorDataByKey("31094___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1507
  handler.SetArmorDataByKey("31096___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1508
  handler.SetArmorDataByKey("24170___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1509
  handler.SetArmorDataByKey("4820___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1510
  handler.SetArmorDataByKey("4822___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1511
  handler.SetArmorDataByKey("4823___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1512
  handler.SetArmorDataByKey("4821___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1513
  handler.SetArmorDataByKey("62997___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1514
  handler.SetArmorDataByKey("42171___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1515
  handler.SetArmorDataByKey("42169___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1516
  handler.SetArmorDataByKey("38021___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1517
  handler.SetArmorDataByKey("25554___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1518
  handler.SetArmorDataByKey("18617___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1519
  handler.SetArmorDataByKey("18618___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1520
  handler.SetArmorDataByKey("3435___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1521
  handler.SetArmorDataByKey("3432___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1522
  handler.SetArmorDataByKey("10340___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1523
  handler.SetArmorDataByKey("3431___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1524
  handler.SetArmorDataByKey("3430___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1525
  handler.SetArmorDataByKey("3433___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1526
  handler.SetArmorDataByKey("17235___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1527
  handler.SetArmorDataByKey("22787___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1528
  handler.SetArmorDataByKey("25562___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1529
  handler.SetArmorDataByKey("25564___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1530
  handler.SetArmorDataByKey("57362___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1531
  handler.SetArmorDataByKey("94961___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1534
  handler.SetArmorDataByKey("100481___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1535
  handler.SetArmorDataByKey("89445___" + asPluginName, handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1536
  handler.SetArmorDataByKey("94961___" + asPluginName, handler.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1537
EndFunction

Function COSDGLoadUp()
  Self.AddCOSDGDatastoreEntries("Complete Crafting Overhaul_Remade.esp") ; #DEBUG_LINE_NO:1546
  Self.AddCOSDGDatastoreEntries("Cloaks - Dawnguard.esp") ; #DEBUG_LINE_NO:1547
  Self.AddCOSDGDatastoreEntries("Cloaks - Player Only - Dawnguard.esp") ; #DEBUG_LINE_NO:1548
  Self.AddCOSDGDatastoreEntries("Cloaks - No Imperial - Dawnguard.esp") ; #DEBUG_LINE_NO:1549
EndFunction

Function AddCOSDGDatastoreEntries(String asPluginName)
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1556
  If asPluginName == "Complete Crafting Overhaul_Remade.esp" ; #DEBUG_LINE_NO:1557
    If frostutil.ArmorProtectionDataExistsByKey("22789___" + asPluginName) ; #DEBUG_LINE_NO:1558
      Return  ; #DEBUG_LINE_NO:1559
    EndIf
    handler.SetArmorDataByKey("22789___" + asPluginName, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1561
    handler.SetArmorDataByKey("22790___" + asPluginName, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1562
  Else
    If frostutil.ArmorProtectionDataExistsByKey("3428___" + asPluginName) ; #DEBUG_LINE_NO:1564
      Return  ; #DEBUG_LINE_NO:1565
    EndIf
    handler.SetArmorDataByKey("3428___" + asPluginName, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1567
    handler.SetArmorDataByKey("3429___" + asPluginName, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1568
  EndIf
EndFunction

Function WICLoadUp()
  Self.AddWICDatastoreEntries("Complete Crafting Overhaul_Remade.esp") ; #DEBUG_LINE_NO:1577
  Self.AddWICDatastoreEntries("1nivWICCloaks.esp") ; #DEBUG_LINE_NO:1578
  Self.AddWICDatastoreEntries("1nivWICCloaksNoGuards.esp") ; #DEBUG_LINE_NO:1579
  Self.AddWICDatastoreEntries("1nivWICCloaksCRAFT.esp") ; #DEBUG_LINE_NO:1580
EndFunction

Function AddWICDatastoreEntries(String asPluginName)
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1588
  If frostutil.ArmorProtectionDataExistsByKey("7639___" + asPluginName) ; #DEBUG_LINE_NO:1589
    Return  ; #DEBUG_LINE_NO:1590
  EndIf
  handler.SetArmorDataByKey("10445___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1594
  handler.SetArmorDataByKey("14581___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1595
  handler.SetArmorDataByKey("14582___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1596
  handler.SetArmorDataByKey("110288___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1597
  handler.SetArmorDataByKey("110289___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1598
  handler.SetArmorDataByKey("110290___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1599
  handler.SetArmorDataByKey("76952___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1600
  handler.SetArmorDataByKey("76953___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1601
  handler.SetArmorDataByKey("76954___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1602
  handler.SetArmorDataByKey("14586___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1603
  handler.SetArmorDataByKey("14587___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1604
  handler.SetArmorDataByKey("14588___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1605
  handler.SetArmorDataByKey("110291___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1606
  handler.SetArmorDataByKey("110292___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1607
  handler.SetArmorDataByKey("110293___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1608
  handler.SetArmorDataByKey("78336___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1609
  handler.SetArmorDataByKey("78337___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1610
  handler.SetArmorDataByKey("78338___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1611
  handler.SetArmorDataByKey("14583___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1612
  handler.SetArmorDataByKey("14584___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1613
  handler.SetArmorDataByKey("14585___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1614
  handler.SetArmorDataByKey("110294___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1615
  handler.SetArmorDataByKey("110295___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1616
  handler.SetArmorDataByKey("110296___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1617
  handler.SetArmorDataByKey("78339___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1618
  handler.SetArmorDataByKey("78340___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1619
  handler.SetArmorDataByKey("78341___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1620
  handler.SetArmorDataByKey("50540___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1621
  handler.SetArmorDataByKey("111757___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1622
  handler.SetArmorDataByKey("111756___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1623
  handler.SetArmorDataByKey("111758___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1624
  handler.SetArmorDataByKey("81140___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1625
  handler.SetArmorDataByKey("81141___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1626
  handler.SetArmorDataByKey("81142___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1627
  handler.SetArmorDataByKey("50539___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1628
  handler.SetArmorDataByKey("50541___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1629
  handler.SetArmorDataByKey("88117___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1630
  handler.SetArmorDataByKey("111754___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1631
  handler.SetArmorDataByKey("111753___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1632
  handler.SetArmorDataByKey("111755___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1633
  handler.SetArmorDataByKey("88120___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1634
  handler.SetArmorDataByKey("88119___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1635
  handler.SetArmorDataByKey("88121___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1636
  handler.SetArmorDataByKey("89500___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1637
  handler.SetArmorDataByKey("88118___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1638
  handler.SetArmorDataByKey("50543___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1639
  handler.SetArmorDataByKey("111760___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1640
  handler.SetArmorDataByKey("111759___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1641
  handler.SetArmorDataByKey("111761___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1642
  handler.SetArmorDataByKey("81143___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1643
  handler.SetArmorDataByKey("81144___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1644
  handler.SetArmorDataByKey("81145___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1645
  handler.SetArmorDataByKey("50542___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1646
  handler.SetArmorDataByKey("50544___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1647
  handler.SetArmorDataByKey("90880___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1648
  handler.SetArmorDataByKey("113156___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1649
  handler.SetArmorDataByKey("113155___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1650
  handler.SetArmorDataByKey("113157___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1651
  handler.SetArmorDataByKey("90882___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1652
  handler.SetArmorDataByKey("90883___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1653
  handler.SetArmorDataByKey("90884___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1654
  handler.SetArmorDataByKey("89501___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1655
  handler.SetArmorDataByKey("90881___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1656
  handler.SetArmorDataByKey("50546___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1657
  handler.SetArmorDataByKey("111763___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1658
  handler.SetArmorDataByKey("111762___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1659
  handler.SetArmorDataByKey("111764___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1660
  handler.SetArmorDataByKey("81146___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1661
  handler.SetArmorDataByKey("81147___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1662
  handler.SetArmorDataByKey("81148___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1663
  handler.SetArmorDataByKey("50545___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1664
  handler.SetArmorDataByKey("50547___" + asPluginName, handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1665
  handler.SetArmorDataByKey("7639___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1668
  handler.SetArmorDataByKey("56156___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1669
  handler.SetArmorDataByKey("56175___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1670
  handler.SetArmorDataByKey("9020___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1671
  handler.SetArmorDataByKey("56158___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1672
  handler.SetArmorDataByKey("56176___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1673
  handler.SetArmorDataByKey("9021___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1674
  handler.SetArmorDataByKey("56159___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1675
  handler.SetArmorDataByKey("56177___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1676
  handler.SetArmorDataByKey("9025___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1677
  handler.SetArmorDataByKey("56160___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1678
  handler.SetArmorDataByKey("56178___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1679
  handler.SetArmorDataByKey("9026___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1680
  handler.SetArmorDataByKey("56161___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1681
  handler.SetArmorDataByKey("56179___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1682
  handler.SetArmorDataByKey("9027___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1683
  handler.SetArmorDataByKey("56162___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1684
  handler.SetArmorDataByKey("56180___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1685
  handler.SetArmorDataByKey("9022___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1686
  handler.SetArmorDataByKey("56163___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1687
  handler.SetArmorDataByKey("56181___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1688
  handler.SetArmorDataByKey("9023___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1689
  handler.SetArmorDataByKey("56164___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1690
  handler.SetArmorDataByKey("56182___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1691
  handler.SetArmorDataByKey("9024___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1692
  handler.SetArmorDataByKey("56165___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1693
  handler.SetArmorDataByKey("56183___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1694
  handler.SetArmorDataByKey("9029___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1695
  handler.SetArmorDataByKey("56166___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1696
  handler.SetArmorDataByKey("56184___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1697
  handler.SetArmorDataByKey("9028___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1698
  handler.SetArmorDataByKey("56167___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1699
  handler.SetArmorDataByKey("56185___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1700
  handler.SetArmorDataByKey("9030___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1701
  handler.SetArmorDataByKey("56168___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1702
  handler.SetArmorDataByKey("56186___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1703
  handler.SetArmorDataByKey("70014___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1704
  handler.SetArmorDataByKey("70016___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1705
  handler.SetArmorDataByKey("70019___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1706
  handler.SetArmorDataByKey("70013___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1707
  handler.SetArmorDataByKey("70017___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1708
  handler.SetArmorDataByKey("70020___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1709
  handler.SetArmorDataByKey("70015___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1710
  handler.SetArmorDataByKey("70018___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1711
  handler.SetArmorDataByKey("70021___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1712
  handler.SetArmorDataByKey("9034___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1713
  handler.SetArmorDataByKey("56169___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1714
  handler.SetArmorDataByKey("56187___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1715
  handler.SetArmorDataByKey("9035___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1716
  handler.SetArmorDataByKey("56170___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1717
  handler.SetArmorDataByKey("56188___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1718
  handler.SetArmorDataByKey("9036___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1719
  handler.SetArmorDataByKey("56171___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1720
  handler.SetArmorDataByKey("56189___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1721
  handler.SetArmorDataByKey("9032___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1722
  handler.SetArmorDataByKey("56172___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1723
  handler.SetArmorDataByKey("56190___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1724
  handler.SetArmorDataByKey("9031___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1725
  handler.SetArmorDataByKey("56173___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1726
  handler.SetArmorDataByKey("56191___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1727
  handler.SetArmorDataByKey("9033___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1728
  handler.SetArmorDataByKey("56174___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1729
  handler.SetArmorDataByKey("56192___" + asPluginName, handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1730
EndFunction

Function RunCompatibilityArmors()
  If isSKSELoaded ; #DEBUG_LINE_NO:1743
    Self.RunCompatibilityArmors_SKSE() ; #DEBUG_LINE_NO:1744
  Else
    Self.RunCompatibilityArmors_Vanilla() ; #DEBUG_LINE_NO:1746
  EndIf
EndFunction

Function RunCompatibilityArmors_SKSE()
  Self.IMALoadUp() ; #DEBUG_LINE_NO:1755
  Self.NFHLoadUp() ; #DEBUG_LINE_NO:1756
  Self.WICLoadUp() ; #DEBUG_LINE_NO:1757
  Self.COSLoadUp() ; #DEBUG_LINE_NO:1758
  Self.COSDGLoadUp() ; #DEBUG_LINE_NO:1759
  Self.AEALoadUp() ; #DEBUG_LINE_NO:1760
  Self.WACLoadUp() ; #DEBUG_LINE_NO:1761
  frostutil.GetClothingDatastoreHandler().SaveDefaultArmorProfile() ; #DEBUG_LINE_NO:1762
EndFunction

Function RunCompatibilityArmors_Vanilla()
  Self.IMALoadUp_Vanilla() ; #DEBUG_LINE_NO:1770
  Self.NFHLoadUp_Vanilla() ; #DEBUG_LINE_NO:1771
  Self.WICLoadUp_Vanilla() ; #DEBUG_LINE_NO:1772
  Self.COSLoadUp_Vanilla() ; #DEBUG_LINE_NO:1773
  Self.COSDGLoadUp_Vanilla() ; #DEBUG_LINE_NO:1774
  Self.AEALoadUp_Vanilla() ; #DEBUG_LINE_NO:1775
  Self.WACLoadUp_Vanilla() ; #DEBUG_LINE_NO:1776
EndFunction

Function PopulateDefaultArmorData()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1784
  _frost_apdatastoredefaultdata defaults = (handler as Quest) as _frost_apdatastoredefaultdata ; #DEBUG_LINE_NO:1785
  defaults.SetDefaults_Body() ; #DEBUG_LINE_NO:1786
  defaults.SetDefaults_Hands() ; #DEBUG_LINE_NO:1787
  defaults.SetDefaults_Head() ; #DEBUG_LINE_NO:1788
  defaults.SetDefaults_Feet() ; #DEBUG_LINE_NO:1789
  defaults.SetDefaults_Cloak() ; #DEBUG_LINE_NO:1790
  defaults.SetDefaults_Shield() ; #DEBUG_LINE_NO:1791
  handler.SaveDefaultArmorProfile() ; #DEBUG_LINE_NO:1792
  Debug.trace("[Frostfall] Finished saving the default armor data.", 0) ; #DEBUG_LINE_NO:1793
EndFunction

Function ModifyFurArmorNames()
  _frost_strings str = _frostinternal.GetFrostfallStrings() ; #DEBUG_LINE_NO:1801
  ArmorBanditCuirass1.SetName(str.ArmorBanditCuirass1Name) ; #DEBUG_LINE_NO:1802
  _Camp_ArmorBanditCuirass1.SetName(str.ArmorBanditCuirass1Name) ; #DEBUG_LINE_NO:1803
  ArmorBanditCuirass2.SetName(str.ArmorBanditCuirass2Name) ; #DEBUG_LINE_NO:1804
  _Camp_ArmorBanditCuirass2.SetName(str.ArmorBanditCuirass2Name) ; #DEBUG_LINE_NO:1805
  ArmorBanditCuirass3.SetName(str.ArmorBanditCuirass3Name) ; #DEBUG_LINE_NO:1806
  _Camp_ArmorBanditCuirass3.SetName(str.ArmorBanditCuirass3Name) ; #DEBUG_LINE_NO:1807
EndFunction

Function AEALoadUp()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1821
  If frostutil.ArmorProtectionDataExistsByKey("20056___AesirArmor.esp") ; #DEBUG_LINE_NO:1822
    Return  ; #DEBUG_LINE_NO:1823
  EndIf
  handler.SetArmorDataByKey("20056___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1826
  handler.SetArmorDataByKey("130085___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1827
  handler.SetArmorDataByKey("98064___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1828
  handler.SetArmorDataByKey("130086___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1829
  handler.SetArmorDataByKey("98065___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1830
  handler.SetArmorDataByKey("130087___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1831
  handler.SetArmorDataByKey("233387___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1832
  handler.SetArmorDataByKey("233392___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1833
  handler.SetArmorDataByKey("233388___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1834
  handler.SetArmorDataByKey("233393___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1835
  handler.SetArmorDataByKey("233389___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1836
  handler.SetArmorDataByKey("233394___AesirArmor.esp", handler.GEARTYPE_CLOAK, 40, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1837
  handler.SetArmorDataByKey("95268___AesirArmor.esp", handler.GEARTYPE_BODY, 175, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1839
  handler.SetArmorDataByKey("125934___AesirArmor.esp", handler.GEARTYPE_BODY, 175, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1840
  handler.SetArmorDataByKey("49193___AesirArmor.esp", handler.GEARTYPE_BODY, 175, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1841
  handler.SetArmorDataByKey("247294___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1843
  handler.SetArmorDataByKey("247295___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1844
  handler.SetArmorDataByKey("247296___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1845
  handler.SetArmorDataByKey("247297___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1846
  handler.SetArmorDataByKey("10379___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1847
  handler.SetArmorDataByKey("130178___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1848
  handler.SetArmorDataByKey("18674___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1849
  handler.SetArmorDataByKey("131557___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1850
  handler.SetArmorDataByKey("18675___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1851
  handler.SetArmorDataByKey("131559___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1852
  handler.SetArmorDataByKey("18676___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1853
  handler.SetArmorDataByKey("131558___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1854
  handler.SetArmorDataByKey("211121___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1855
  handler.SetArmorDataByKey("211122___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1856
  handler.SetArmorDataByKey("211123___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1857
  handler.SetArmorDataByKey("211124___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1858
  handler.SetArmorDataByKey("211125___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1859
  handler.SetArmorDataByKey("211126___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1860
  handler.SetArmorDataByKey("211127___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1861
  handler.SetArmorDataByKey("211128___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1862
  handler.SetArmorDataByKey("211129___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1863
  handler.SetArmorDataByKey("212522___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1864
  handler.SetArmorDataByKey("211130___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1865
  handler.SetArmorDataByKey("212523___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1866
  handler.SetArmorDataByKey("211131___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1867
  handler.SetArmorDataByKey("212524___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1868
  handler.SetArmorDataByKey("211136___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1869
  handler.SetArmorDataByKey("212525___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1870
  handler.SetArmorDataByKey("211135___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1871
  handler.SetArmorDataByKey("212526___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1872
  handler.SetArmorDataByKey("211132___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1873
  handler.SetArmorDataByKey("212527___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1874
  handler.SetArmorDataByKey("211133___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1875
  handler.SetArmorDataByKey("212528___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1876
  handler.SetArmorDataByKey("211134___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1877
  handler.SetArmorDataByKey("212529___AesirArmor.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1878
  handler.SetArmorDataByKey("49195___AesirArmor.esp", handler.GEARTYPE_HANDS, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1880
  handler.SetArmorDataByKey("31538___AesirArmor.esp", handler.GEARTYPE_HANDS, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1881
  handler.SetArmorDataByKey("131561___AesirArmor.esp", handler.GEARTYPE_HANDS, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1882
  handler.SetArmorDataByKey("31541___AesirArmor.esp", handler.GEARTYPE_FEET, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1884
  handler.SetArmorDataByKey("131560___AesirArmor.esp", handler.GEARTYPE_FEET, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1885
  handler.SetArmorDataByKey("49194___AesirArmor.esp", handler.GEARTYPE_FEET, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1886
EndFunction

Function IMALoadUp()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:1897
  If frostutil.ArmorProtectionDataExistsByKey("20258___Hothtrooper44_ArmorCompilation.esp") ; #DEBUG_LINE_NO:1898
    Return  ; #DEBUG_LINE_NO:1899
  EndIf
  handler.SetArmorDataByKey("20258___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1902
  handler.SetArmorDataByKey("144010___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1903
  handler.SetArmorDataByKey("46671___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1904
  handler.SetArmorDataByKey("23132___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1905
  handler.SetArmorDataByKey("144116___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1906
  handler.SetArmorDataByKey("544585___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1907
  handler.SetArmorDataByKey("145634___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1908
  handler.SetArmorDataByKey("145637___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1909
  handler.SetArmorDataByKey("145646___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1910
  handler.SetArmorDataByKey("145653___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1911
  handler.SetArmorDataByKey("145656___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1912
  handler.SetArmorDataByKey("143594___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1913
  handler.SetArmorDataByKey("143608___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1914
  handler.SetArmorDataByKey("145723___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 160, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1915
  handler.SetArmorDataByKey("139237___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1916
  handler.SetArmorDataByKey("139238___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1917
  handler.SetArmorDataByKey("143558___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1918
  handler.SetArmorDataByKey("143557___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1919
  handler.SetArmorDataByKey("15925___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 190, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1920
  handler.SetArmorDataByKey("15926___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 190, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1921
  handler.SetArmorDataByKey("32830___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 190, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1922
  handler.SetArmorDataByKey("4820___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 190, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1923
  handler.SetArmorDataByKey("3428___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1924
  handler.SetArmorDataByKey("144118___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 190, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1925
  handler.SetArmorDataByKey("544590___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 190, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1926
  handler.SetArmorDataByKey("3478___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1927
  handler.SetArmorDataByKey("23065___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1928
  handler.SetArmorDataByKey("43878___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1929
  handler.SetArmorDataByKey("14469___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1930
  handler.SetArmorDataByKey("436741___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1931
  handler.SetArmorDataByKey("23050___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 110, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1932
  handler.SetArmorDataByKey("43874___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 0, 0, True, False) ; #DEBUG_LINE_NO:1933
  handler.SetArmorDataByKey("23151___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 110, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1935
  handler.SetArmorDataByKey("3440___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1936
  handler.SetArmorDataByKey("3441___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1937
  handler.SetArmorDataByKey("144113___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 110, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1938
  handler.SetArmorDataByKey("139149___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1939
  handler.SetArmorDataByKey("43870___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1940
  handler.SetArmorDataByKey("144117___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 35, 0, 0, 0, 0, 0, 0, 0, 0, 40, 12, 0, 0, True, False) ; #DEBUG_LINE_NO:1941
  handler.SetArmorDataByKey("53616___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1942
  handler.SetArmorDataByKey("53617___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1943
  handler.SetArmorDataByKey("436720___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 40, 12, 0, 0, True, False) ; #DEBUG_LINE_NO:1944
  handler.SetArmorDataByKey("143492___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 35, 0, 0, 0, 0, 0, 0, 0, 0, 40, 12, 0, 0, True, False) ; #DEBUG_LINE_NO:1945
  handler.SetArmorDataByKey("143498___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 35, 0, 0, 0, 0, 0, 0, 0, 0, 40, 12, 0, 0, True, False) ; #DEBUG_LINE_NO:1946
  handler.SetArmorDataByKey("3447___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 128, 106, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 0, 0, True, False) ; #DEBUG_LINE_NO:1947
  handler.SetArmorDataByKey("3449___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 128, 106, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 0, 0, True, False) ; #DEBUG_LINE_NO:1948
  handler.SetArmorDataByKey("3448___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 128, 106, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 0, 0, True, False) ; #DEBUG_LINE_NO:1949
  handler.SetArmorDataByKey("3460___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 128, 106, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1950
  handler.SetArmorDataByKey("144124___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1951
  handler.SetArmorDataByKey("50833___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1952
  handler.SetArmorDataByKey("143995___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 110, 52, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1953
  handler.SetArmorDataByKey("143996___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 90, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1954
  handler.SetArmorDataByKey("143997___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 90, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1955
  handler.SetArmorDataByKey("20284___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1956
  handler.SetArmorDataByKey("144024___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1957
  handler.SetArmorDataByKey("226058___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 109, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1958
  handler.SetArmorDataByKey("23079___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1959
  handler.SetArmorDataByKey("144028___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1960
  handler.SetArmorDataByKey("226053___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1961
  handler.SetArmorDataByKey("145736___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1962
  handler.SetArmorDataByKey("145740___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1963
  handler.SetArmorDataByKey("226045___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 140, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1964
  handler.SetArmorDataByKey("143533___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1965
  handler.SetArmorDataByKey("536248___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1966
  handler.SetArmorDataByKey("143706___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1967
  handler.SetArmorDataByKey("143701___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1968
  handler.SetArmorDataByKey("143707___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1969
  handler.SetArmorDataByKey("143702___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1970
  handler.SetArmorDataByKey("143708___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1971
  handler.SetArmorDataByKey("143703___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1972
  handler.SetArmorDataByKey("143709___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1973
  handler.SetArmorDataByKey("143704___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1974
  handler.SetArmorDataByKey("143710___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1975
  handler.SetArmorDataByKey("143705___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1976
  handler.SetArmorDataByKey("143731___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1977
  handler.SetArmorDataByKey("143726___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1978
  handler.SetArmorDataByKey("143732___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1979
  handler.SetArmorDataByKey("143727___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1980
  handler.SetArmorDataByKey("143733___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1981
  handler.SetArmorDataByKey("143728___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1982
  handler.SetArmorDataByKey("143734___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1983
  handler.SetArmorDataByKey("143729___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1984
  handler.SetArmorDataByKey("143735___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1985
  handler.SetArmorDataByKey("143730___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1986
  handler.SetArmorDataByKey("143755___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1987
  handler.SetArmorDataByKey("143756___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1988
  handler.SetArmorDataByKey("143757___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1989
  handler.SetArmorDataByKey("143758___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1990
  handler.SetArmorDataByKey("143759___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 125, 72, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, True, False) ; #DEBUG_LINE_NO:1991
  handler.SetArmorDataByKey("16070___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 75, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1992
  handler.SetArmorDataByKey("16068___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 75, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1993
  handler.SetArmorDataByKey("3466___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 175, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1994
  handler.SetArmorDataByKey("3467___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_BODY, 175, 54, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1995
  handler.SetArmorDataByKey("20259___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1997
  handler.SetArmorDataByKey("144011___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1998
  handler.SetArmorDataByKey("23133___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:1999
  handler.SetArmorDataByKey("144096___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2000
  handler.SetArmorDataByKey("544586___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2001
  handler.SetArmorDataByKey("145647___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2002
  handler.SetArmorDataByKey("145654___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2003
  handler.SetArmorDataByKey("145657___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2004
  handler.SetArmorDataByKey("145724___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 18, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2005
  handler.SetArmorDataByKey("139239___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2006
  handler.SetArmorDataByKey("143560___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2007
  handler.SetArmorDataByKey("143561___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2008
  handler.SetArmorDataByKey("143562___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2009
  handler.SetArmorDataByKey("23080___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2010
  handler.SetArmorDataByKey("144026___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2011
  handler.SetArmorDataByKey("226051___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2012
  handler.SetArmorDataByKey("15917___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2013
  handler.SetArmorDataByKey("32832___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2014
  handler.SetArmorDataByKey("4818___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2015
  handler.SetArmorDataByKey("3429___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2016
  handler.SetArmorDataByKey("144100___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 24, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2017
  handler.SetArmorDataByKey("544591___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 24, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2018
  handler.SetArmorDataByKey("3479___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2019
  handler.SetArmorDataByKey("43877___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2020
  handler.SetArmorDataByKey("23051___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2021
  handler.SetArmorDataByKey("43873___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2022
  handler.SetArmorDataByKey("3436___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2024
  handler.SetArmorDataByKey("3437___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2025
  handler.SetArmorDataByKey("6189___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2026
  handler.SetArmorDataByKey("144120___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2027
  handler.SetArmorDataByKey("53615___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2028
  handler.SetArmorDataByKey("53618___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2029
  handler.SetArmorDataByKey("436721___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2030
  handler.SetArmorDataByKey("143493___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2031
  handler.SetArmorDataByKey("3453___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2032
  handler.SetArmorDataByKey("3455___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2033
  handler.SetArmorDataByKey("3461___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2034
  handler.SetArmorDataByKey("144125___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2035
  handler.SetArmorDataByKey("50835___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2036
  handler.SetArmorDataByKey("46670___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 10, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2037
  handler.SetArmorDataByKey("143609___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2038
  handler.SetArmorDataByKey("139240___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2039
  handler.SetArmorDataByKey("20281___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2040
  handler.SetArmorDataByKey("144022___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2041
  handler.SetArmorDataByKey("226061___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2042
  handler.SetArmorDataByKey("145737___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2043
  handler.SetArmorDataByKey("145741___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2044
  handler.SetArmorDataByKey("226043___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2045
  handler.SetArmorDataByKey("139150___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2046
  handler.SetArmorDataByKey("143536___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2047
  handler.SetArmorDataByKey("536246___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2048
  handler.SetArmorDataByKey("143691___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2049
  handler.SetArmorDataByKey("143692___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2050
  handler.SetArmorDataByKey("143693___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2051
  handler.SetArmorDataByKey("143694___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2052
  handler.SetArmorDataByKey("143695___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2053
  handler.SetArmorDataByKey("143716___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2054
  handler.SetArmorDataByKey("143717___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2055
  handler.SetArmorDataByKey("143718___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2056
  handler.SetArmorDataByKey("143719___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2057
  handler.SetArmorDataByKey("143720___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2058
  handler.SetArmorDataByKey("143745___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2059
  handler.SetArmorDataByKey("143746___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2060
  handler.SetArmorDataByKey("143747___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2061
  handler.SetArmorDataByKey("143748___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2062
  handler.SetArmorDataByKey("143749___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2063
  handler.SetArmorDataByKey("145643___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2064
  handler.SetArmorDataByKey("145638___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2065
  handler.SetArmorDataByKey("143592___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2066
  handler.SetArmorDataByKey("15918___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2067
  handler.SetArmorDataByKey("23066___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2068
  handler.SetArmorDataByKey("14468___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2069
  handler.SetArmorDataByKey("16065___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2070
  handler.SetArmorDataByKey("16069___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2071
  handler.SetArmorDataByKey("23152___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2072
  handler.SetArmorDataByKey("144114___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2073
  handler.SetArmorDataByKey("143499___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2074
  handler.SetArmorDataByKey("3454___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 12, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2075
  handler.SetArmorDataByKey("436744___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2076
  handler.SetArmorDataByKey("3470___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2077
  handler.SetArmorDataByKey("3471___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HANDS, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2078
  handler.SetArmorDataByKey("20260___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2080
  handler.SetArmorDataByKey("144012___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2081
  handler.SetArmorDataByKey("46669___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2082
  handler.SetArmorDataByKey("23134___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 15, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2083
  handler.SetArmorDataByKey("144097___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2084
  handler.SetArmorDataByKey("544587___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2085
  handler.SetArmorDataByKey("145639___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2086
  handler.SetArmorDataByKey("145648___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2087
  handler.SetArmorDataByKey("145649___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2088
  handler.SetArmorDataByKey("145652___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2089
  handler.SetArmorDataByKey("139247___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2090
  handler.SetArmorDataByKey("139248___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2091
  handler.SetArmorDataByKey("139249___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2092
  handler.SetArmorDataByKey("139250___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2093
  handler.SetArmorDataByKey("139243___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2094
  handler.SetArmorDataByKey("139244___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2095
  handler.SetArmorDataByKey("139245___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2096
  handler.SetArmorDataByKey("139246___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2097
  handler.SetArmorDataByKey("139241___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2098
  handler.SetArmorDataByKey("139242___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2099
  handler.SetArmorDataByKey("543154___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2100
  handler.SetArmorDataByKey("543155___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2101
  handler.SetArmorDataByKey("543156___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2102
  handler.SetArmorDataByKey("543157___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2103
  handler.SetArmorDataByKey("543158___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2104
  handler.SetArmorDataByKey("543159___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2105
  handler.SetArmorDataByKey("543160___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2106
  handler.SetArmorDataByKey("543161___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2107
  handler.SetArmorDataByKey("543162___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2108
  handler.SetArmorDataByKey("543163___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2109
  handler.SetArmorDataByKey("143563___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2110
  handler.SetArmorDataByKey("548818___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2111
  handler.SetArmorDataByKey("3430___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2112
  handler.SetArmorDataByKey("144101___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 55, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2113
  handler.SetArmorDataByKey("544592___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 55, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2114
  handler.SetArmorDataByKey("3480___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2115
  handler.SetArmorDataByKey("23067___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2116
  handler.SetArmorDataByKey("43876___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2117
  handler.SetArmorDataByKey("436743___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2118
  handler.SetArmorDataByKey("16071___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2119
  handler.SetArmorDataByKey("16072___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2120
  handler.SetArmorDataByKey("16074___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2121
  handler.SetArmorDataByKey("16073___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2122
  handler.SetArmorDataByKey("139134___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2123
  handler.SetArmorDataByKey("15853___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2124
  handler.SetArmorDataByKey("43872___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2125
  handler.SetArmorDataByKey("139151___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2127
  handler.SetArmorDataByKey("143534___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2128
  handler.SetArmorDataByKey("536247___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2129
  handler.SetArmorDataByKey("144121___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2130
  handler.SetArmorDataByKey("53613___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2131
  handler.SetArmorDataByKey("53620___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2132
  handler.SetArmorDataByKey("436723___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2133
  handler.SetArmorDataByKey("143496___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2134
  handler.SetArmorDataByKey("143501___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2135
  handler.SetArmorDataByKey("143494___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2136
  handler.SetArmorDataByKey("143500___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2137
  handler.SetArmorDataByKey("3472___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2138
  handler.SetArmorDataByKey("3473___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2139
  handler.SetArmorDataByKey("3456___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 72, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2140
  handler.SetArmorDataByKey("3462___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2141
  handler.SetArmorDataByKey("3463___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2142
  handler.SetArmorDataByKey("144126___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2143
  handler.SetArmorDataByKey("17238___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2144
  handler.SetArmorDataByKey("18651___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2145
  handler.SetArmorDataByKey("8949___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 20, 6, 0, 0, True, False) ; #DEBUG_LINE_NO:2146
  handler.SetArmorDataByKey("18650___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2147
  handler.SetArmorDataByKey("764316___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 20, 6, 0, 0, True, False) ; #DEBUG_LINE_NO:2148
  handler.SetArmorDataByKey("18652___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2149
  handler.SetArmorDataByKey("6185___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 20, 6, 0, 0, True, False) ; #DEBUG_LINE_NO:2150
  handler.SetArmorDataByKey("18654___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2151
  handler.SetArmorDataByKey("8957___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 20, 6, 0, 0, True, False) ; #DEBUG_LINE_NO:2152
  handler.SetArmorDataByKey("18653___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2153
  handler.SetArmorDataByKey("764315___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 20, 6, 0, 0, True, False) ; #DEBUG_LINE_NO:2154
  handler.SetArmorDataByKey("18655___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2155
  handler.SetArmorDataByKey("7567___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 20, 6, 0, 0, True, False) ; #DEBUG_LINE_NO:2156
  handler.SetArmorDataByKey("145640___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2157
  handler.SetArmorDataByKey("145650___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2158
  handler.SetArmorDataByKey("145658___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2159
  handler.SetArmorDataByKey("139251___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2160
  handler.SetArmorDataByKey("543164___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2161
  handler.SetArmorDataByKey("20283___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2162
  handler.SetArmorDataByKey("144023___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2163
  handler.SetArmorDataByKey("226060___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2164
  handler.SetArmorDataByKey("23081___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2165
  handler.SetArmorDataByKey("144027___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2166
  handler.SetArmorDataByKey("226052___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2167
  handler.SetArmorDataByKey("145738___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2168
  handler.SetArmorDataByKey("145742___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2169
  handler.SetArmorDataByKey("226044___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 40, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2170
  handler.SetArmorDataByKey("15921___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 55, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2171
  handler.SetArmorDataByKey("15922___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 55, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2172
  handler.SetArmorDataByKey("32831___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 55, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2173
  handler.SetArmorDataByKey("4819___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 55, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2174
  handler.SetArmorDataByKey("18649___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2175
  handler.SetArmorDataByKey("8956___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2176
  handler.SetArmorDataByKey("18648___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2177
  handler.SetArmorDataByKey("764314___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2178
  handler.SetArmorDataByKey("18656___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2179
  handler.SetArmorDataByKey("7566___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 45, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2180
  handler.SetArmorDataByKey("23153___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 8, 20, 0, 0, True, False) ; #DEBUG_LINE_NO:2181
  handler.SetArmorDataByKey("144115___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2182
  handler.SetArmorDataByKey("143696___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2183
  handler.SetArmorDataByKey("143697___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2184
  handler.SetArmorDataByKey("143698___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2185
  handler.SetArmorDataByKey("143699___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2186
  handler.SetArmorDataByKey("143700___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2187
  handler.SetArmorDataByKey("143721___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2188
  handler.SetArmorDataByKey("143722___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2189
  handler.SetArmorDataByKey("143723___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2190
  handler.SetArmorDataByKey("143724___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2191
  handler.SetArmorDataByKey("143725___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2192
  handler.SetArmorDataByKey("143750___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2193
  handler.SetArmorDataByKey("143751___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2194
  handler.SetArmorDataByKey("143752___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2195
  handler.SetArmorDataByKey("143753___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2196
  handler.SetArmorDataByKey("143754___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 30, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2197
  handler.SetArmorDataByKey("50836___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2198
  handler.SetArmorDataByKey("3427___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2199
  handler.SetArmorDataByKey("3464___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2200
  handler.SetArmorDataByKey("3465___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2201
  handler.SetArmorDataByKey("143593___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2202
  handler.SetArmorDataByKey("143464___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 40, 12, 0, 0, True, False) ; #DEBUG_LINE_NO:2203
  handler.SetArmorDataByKey("143465___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 40, 12, 0, 0, True, False) ; #DEBUG_LINE_NO:2204
  handler.SetArmorDataByKey("4807___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2205
  handler.SetArmorDataByKey("7571___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2206
  handler.SetArmorDataByKey("145633___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2207
  handler.SetArmorDataByKey("145645___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_HEAD, 35, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2208
  handler.SetArmorDataByKey("20257___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2210
  handler.SetArmorDataByKey("144009___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2211
  handler.SetArmorDataByKey("46672___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2212
  handler.SetArmorDataByKey("23131___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2213
  handler.SetArmorDataByKey("144095___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2214
  handler.SetArmorDataByKey("544584___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2215
  handler.SetArmorDataByKey("145632___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2216
  handler.SetArmorDataByKey("145635___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2217
  handler.SetArmorDataByKey("145644___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2218
  handler.SetArmorDataByKey("145651___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2219
  handler.SetArmorDataByKey("145655___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2220
  handler.SetArmorDataByKey("143591___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2221
  handler.SetArmorDataByKey("143607___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2222
  handler.SetArmorDataByKey("145722___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 18, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2223
  handler.SetArmorDataByKey("139235___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2224
  handler.SetArmorDataByKey("139236___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2225
  handler.SetArmorDataByKey("20280___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2226
  handler.SetArmorDataByKey("144021___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2227
  handler.SetArmorDataByKey("226062___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2228
  handler.SetArmorDataByKey("143556___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2229
  handler.SetArmorDataByKey("548819___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2230
  handler.SetArmorDataByKey("23078___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2231
  handler.SetArmorDataByKey("144025___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2232
  handler.SetArmorDataByKey("226050___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2233
  handler.SetArmorDataByKey("145735___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2234
  handler.SetArmorDataByKey("145739___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2235
  handler.SetArmorDataByKey("226042___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2236
  handler.SetArmorDataByKey("15913___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2237
  handler.SetArmorDataByKey("15914___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2238
  handler.SetArmorDataByKey("3432___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2239
  handler.SetArmorDataByKey("4817___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 24, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2240
  handler.SetArmorDataByKey("3426___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2241
  handler.SetArmorDataByKey("144099___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 24, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2242
  handler.SetArmorDataByKey("544589___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 24, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2243
  handler.SetArmorDataByKey("3477___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2244
  handler.SetArmorDataByKey("23064___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2245
  handler.SetArmorDataByKey("43879___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2246
  handler.SetArmorDataByKey("14466___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2247
  handler.SetArmorDataByKey("23049___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2248
  handler.SetArmorDataByKey("16064___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2249
  handler.SetArmorDataByKey("16067___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2250
  handler.SetArmorDataByKey("43875___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2251
  handler.SetArmorDataByKey("23150___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2253
  handler.SetArmorDataByKey("3434___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2254
  handler.SetArmorDataByKey("3435___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2255
  handler.SetArmorDataByKey("144112___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2256
  handler.SetArmorDataByKey("139148___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2257
  handler.SetArmorDataByKey("6188___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2258
  handler.SetArmorDataByKey("143535___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2259
  handler.SetArmorDataByKey("536245___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2260
  handler.SetArmorDataByKey("144119___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2261
  handler.SetArmorDataByKey("53614___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2262
  handler.SetArmorDataByKey("53619___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2263
  handler.SetArmorDataByKey("436722___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2264
  handler.SetArmorDataByKey("143686___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2265
  handler.SetArmorDataByKey("143687___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2266
  handler.SetArmorDataByKey("143688___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2267
  handler.SetArmorDataByKey("143689___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2268
  handler.SetArmorDataByKey("143690___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2269
  handler.SetArmorDataByKey("143711___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2270
  handler.SetArmorDataByKey("143712___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2271
  handler.SetArmorDataByKey("143713___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2272
  handler.SetArmorDataByKey("143714___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2273
  handler.SetArmorDataByKey("143715___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2274
  handler.SetArmorDataByKey("143740___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2275
  handler.SetArmorDataByKey("143741___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2276
  handler.SetArmorDataByKey("143742___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2277
  handler.SetArmorDataByKey("143743___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2278
  handler.SetArmorDataByKey("143744___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2279
  handler.SetArmorDataByKey("143491___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2280
  handler.SetArmorDataByKey("143497___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 18, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2281
  handler.SetArmorDataByKey("3450___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2282
  handler.SetArmorDataByKey("3452___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2283
  handler.SetArmorDataByKey("3451___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2284
  handler.SetArmorDataByKey("3459___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2285
  handler.SetArmorDataByKey("144123___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2286
  handler.SetArmorDataByKey("50834___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 12, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2287
  handler.SetArmorDataByKey("436742___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 15, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2288
  handler.SetArmorDataByKey("3474___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2289
  handler.SetArmorDataByKey("3475___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_FEET, 21, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2290
  handler.SetArmorDataByKey("145642___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2292
  handler.SetArmorDataByKey("145660___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_CLOAK, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2293
  handler.SetArmorDataByKey("145641___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_CLOAK, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2294
  handler.SetArmorDataByKey("436740___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2295
  handler.SetArmorDataByKey("63308___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2296
  handler.SetArmorDataByKey("11733___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2297
  handler.SetArmorDataByKey("13097___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_CLOAK, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2298
  handler.SetArmorDataByKey("143495___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2300
  handler.SetArmorDataByKey("143502___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2301
  handler.SetArmorDataByKey("143736___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2302
  handler.SetArmorDataByKey("143737___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2303
  handler.SetArmorDataByKey("143738___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2304
  handler.SetArmorDataByKey("143739___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2305
  handler.SetArmorDataByKey("139152___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2306
  handler.SetArmorDataByKey("10329___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2307
  handler.SetArmorDataByKey("10335___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2308
  handler.SetArmorDataByKey("145659___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2309
  handler.SetArmorDataByKey("139153___Hothtrooper44_ArmorCompilation.esp", handler.GEARTYPE_IGNORE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:2310
EndFunction

Function IMALoadUp_Vanilla()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2320
  _frost_legacyarmordatastore ds = frostutil.GetLegacyArmorDatastore() ; #DEBUG_LINE_NO:2321
  If !Game.IsPluginInstalled("Hothtrooper44_ArmorCompilation.esp")
    Return
  EndIf
  Armor akaviriCuirass = Game.GetFormFromFile(20258, "Hothtrooper44_ArmorCompilation.esp") as Armor ; #DEBUG_LINE_NO:2322
  If !akaviriCuirass ; #DEBUG_LINE_NO:2323
    Return  ; #DEBUG_LINE_NO:2324
  EndIf
  Int[] protectionLevels = ds.FindBodyProtectionLevels(akaviriCuirass) ; #DEBUG_LINE_NO:2326
  If protectionLevels[2] != handler.GEARTYPE_NOTFOUND ; #DEBUG_LINE_NO:2327
    Return  ; #DEBUG_LINE_NO:2328
  EndIf
  ds.SetDefaultArmorData(20258, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2331
  ds.SetDefaultArmorData(144010, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2332
  ds.SetDefaultArmorData(46671, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2333
  ds.SetDefaultArmorData(23132, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2334
  ds.SetDefaultArmorData(144116, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2335
  ds.SetDefaultArmorData(544585, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2336
  ds.SetDefaultArmorData(145634, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2337
  ds.SetDefaultArmorData(145637, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2338
  ds.SetDefaultArmorData(145646, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2339
  ds.SetDefaultArmorData(145653, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2340
  ds.SetDefaultArmorData(145656, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2341
  ds.SetDefaultArmorData(143594, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2342
  ds.SetDefaultArmorData(143608, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2343
  ds.SetDefaultArmorData(145723, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2344
  ds.SetDefaultArmorData(139237, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2345
  ds.SetDefaultArmorData(139238, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2346
  ds.SetDefaultArmorData(143558, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2347
  ds.SetDefaultArmorData(143557, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2348
  ds.SetDefaultArmorData(15925, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2349
  ds.SetDefaultArmorData(15926, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2350
  ds.SetDefaultArmorData(32830, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2351
  ds.SetDefaultArmorData(4820, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2352
  ds.SetDefaultArmorData(3428, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2353
  ds.SetDefaultArmorData(144118, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_MAX, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2354
  ds.SetDefaultArmorData(544590, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_MAX, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2355
  ds.SetDefaultArmorData(3478, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2356
  ds.SetDefaultArmorData(23065, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2357
  ds.SetDefaultArmorData(43878, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2358
  ds.SetDefaultArmorData(14469, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2359
  ds.SetDefaultArmorData(436741, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2360
  ds.SetDefaultArmorData(23050, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2361
  ds.SetDefaultArmorData(43874, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2362
  ds.SetDefaultArmorData(23151, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2363
  ds.SetDefaultArmorData(3440, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2364
  ds.SetDefaultArmorData(3441, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2365
  ds.SetDefaultArmorData(144113, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2366
  ds.SetDefaultArmorData(139149, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2367
  ds.SetDefaultArmorData(43870, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2368
  ds.SetDefaultArmorData(144117, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKFUR) ; #DEBUG_LINE_NO:2369
  ds.SetDefaultArmorData(53616, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2370
  ds.SetDefaultArmorData(53617, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2371
  ds.SetDefaultArmorData(436720, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKFUR) ; #DEBUG_LINE_NO:2372
  ds.SetDefaultArmorData(143492, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKFUR) ; #DEBUG_LINE_NO:2373
  ds.SetDefaultArmorData(143498, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKFUR) ; #DEBUG_LINE_NO:2374
  ds.SetDefaultArmorData(3447, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2375
  ds.SetDefaultArmorData(3449, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2376
  ds.SetDefaultArmorData(3448, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2377
  ds.SetDefaultArmorData(3460, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2378
  ds.SetDefaultArmorData(144124, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2379
  ds.SetDefaultArmorData(50833, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2380
  ds.SetDefaultArmorData(143995, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2381
  ds.SetDefaultArmorData(143996, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2382
  ds.SetDefaultArmorData(143997, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2383
  ds.SetDefaultArmorData(20284, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2384
  ds.SetDefaultArmorData(144024, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2385
  ds.SetDefaultArmorData(226058, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2386
  ds.SetDefaultArmorData(23079, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2387
  ds.SetDefaultArmorData(144028, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2388
  ds.SetDefaultArmorData(226053, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2389
  ds.SetDefaultArmorData(145736, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2390
  ds.SetDefaultArmorData(145740, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2391
  ds.SetDefaultArmorData(226045, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2392
  ds.SetDefaultArmorData(143533, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2393
  ds.SetDefaultArmorData(536248, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2394
  ds.SetDefaultArmorData(143706, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2395
  ds.SetDefaultArmorData(143701, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2396
  ds.SetDefaultArmorData(143707, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2397
  ds.SetDefaultArmorData(143702, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2398
  ds.SetDefaultArmorData(143708, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2399
  ds.SetDefaultArmorData(143703, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2400
  ds.SetDefaultArmorData(143709, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2401
  ds.SetDefaultArmorData(143704, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2402
  ds.SetDefaultArmorData(143710, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2403
  ds.SetDefaultArmorData(143705, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2404
  ds.SetDefaultArmorData(143731, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2405
  ds.SetDefaultArmorData(143726, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2406
  ds.SetDefaultArmorData(143732, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2407
  ds.SetDefaultArmorData(143727, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2408
  ds.SetDefaultArmorData(143733, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2409
  ds.SetDefaultArmorData(143728, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2410
  ds.SetDefaultArmorData(143734, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2411
  ds.SetDefaultArmorData(143729, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2412
  ds.SetDefaultArmorData(143735, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2413
  ds.SetDefaultArmorData(143730, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2414
  ds.SetDefaultArmorData(143755, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2415
  ds.SetDefaultArmorData(143756, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2416
  ds.SetDefaultArmorData(143757, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2417
  ds.SetDefaultArmorData(143758, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2418
  ds.SetDefaultArmorData(143759, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2419
  ds.SetDefaultArmorData(16070, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2420
  ds.SetDefaultArmorData(16068, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2421
  ds.SetDefaultArmorData(3466, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_EXCELLENT, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2422
  ds.SetDefaultArmorData(3467, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_BODY, ds.WARMTH_EXCELLENT, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2423
  ds.SetDefaultArmorData(20259, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2424
  ds.SetDefaultArmorData(144011, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2425
  ds.SetDefaultArmorData(23133, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2426
  ds.SetDefaultArmorData(144096, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2427
  ds.SetDefaultArmorData(544586, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2428
  ds.SetDefaultArmorData(145647, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2429
  ds.SetDefaultArmorData(145654, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2430
  ds.SetDefaultArmorData(145657, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2431
  ds.SetDefaultArmorData(145724, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2432
  ds.SetDefaultArmorData(139239, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2433
  ds.SetDefaultArmorData(143560, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2434
  ds.SetDefaultArmorData(143561, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2435
  ds.SetDefaultArmorData(143562, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2436
  ds.SetDefaultArmorData(23080, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2437
  ds.SetDefaultArmorData(144026, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2438
  ds.SetDefaultArmorData(226051, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2439
  ds.SetDefaultArmorData(15917, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2440
  ds.SetDefaultArmorData(32832, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2441
  ds.SetDefaultArmorData(4818, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2442
  ds.SetDefaultArmorData(3429, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2443
  ds.SetDefaultArmorData(144100, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2444
  ds.SetDefaultArmorData(544591, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2445
  ds.SetDefaultArmorData(3479, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2446
  ds.SetDefaultArmorData(43877, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2447
  ds.SetDefaultArmorData(23051, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2448
  ds.SetDefaultArmorData(43873, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2449
  ds.SetDefaultArmorData(3436, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2450
  ds.SetDefaultArmorData(3437, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2451
  ds.SetDefaultArmorData(6189, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2452
  ds.SetDefaultArmorData(144120, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2453
  ds.SetDefaultArmorData(53615, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2454
  ds.SetDefaultArmorData(53618, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2455
  ds.SetDefaultArmorData(436721, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2456
  ds.SetDefaultArmorData(143493, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2457
  ds.SetDefaultArmorData(3453, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2458
  ds.SetDefaultArmorData(3455, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2459
  ds.SetDefaultArmorData(3461, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2460
  ds.SetDefaultArmorData(144125, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2461
  ds.SetDefaultArmorData(50835, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2462
  ds.SetDefaultArmorData(46670, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2463
  ds.SetDefaultArmorData(143609, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2464
  ds.SetDefaultArmorData(139240, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2465
  ds.SetDefaultArmorData(20281, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2466
  ds.SetDefaultArmorData(144022, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2467
  ds.SetDefaultArmorData(226061, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2468
  ds.SetDefaultArmorData(145737, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2469
  ds.SetDefaultArmorData(145741, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2470
  ds.SetDefaultArmorData(226043, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2471
  ds.SetDefaultArmorData(139150, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2472
  ds.SetDefaultArmorData(143536, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2473
  ds.SetDefaultArmorData(536246, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2474
  ds.SetDefaultArmorData(143691, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2475
  ds.SetDefaultArmorData(143692, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2476
  ds.SetDefaultArmorData(143693, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2477
  ds.SetDefaultArmorData(143694, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2478
  ds.SetDefaultArmorData(143695, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2479
  ds.SetDefaultArmorData(143716, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2480
  ds.SetDefaultArmorData(143717, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2481
  ds.SetDefaultArmorData(143718, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2482
  ds.SetDefaultArmorData(143719, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2483
  ds.SetDefaultArmorData(143720, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2484
  ds.SetDefaultArmorData(143745, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2485
  ds.SetDefaultArmorData(143746, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2486
  ds.SetDefaultArmorData(143747, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2487
  ds.SetDefaultArmorData(143748, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2488
  ds.SetDefaultArmorData(143749, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2489
  ds.SetDefaultArmorData(145643, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2490
  ds.SetDefaultArmorData(145638, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2491
  ds.SetDefaultArmorData(143592, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2492
  ds.SetDefaultArmorData(15918, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2493
  ds.SetDefaultArmorData(23066, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2494
  ds.SetDefaultArmorData(14468, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2495
  ds.SetDefaultArmorData(16065, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2496
  ds.SetDefaultArmorData(16069, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2497
  ds.SetDefaultArmorData(23152, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2498
  ds.SetDefaultArmorData(144114, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2499
  ds.SetDefaultArmorData(143499, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2500
  ds.SetDefaultArmorData(3454, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_FAIR, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2501
  ds.SetDefaultArmorData(436744, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2502
  ds.SetDefaultArmorData(3470, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_EXCELLENT, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2503
  ds.SetDefaultArmorData(3471, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HANDS, ds.WARMTH_EXCELLENT, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2504
  ds.SetDefaultArmorData(20260, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2505
  ds.SetDefaultArmorData(144012, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2506
  ds.SetDefaultArmorData(46669, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2507
  ds.SetDefaultArmorData(23134, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2508
  ds.SetDefaultArmorData(144097, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2509
  ds.SetDefaultArmorData(544587, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2510
  ds.SetDefaultArmorData(145639, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2511
  ds.SetDefaultArmorData(145648, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2512
  ds.SetDefaultArmorData(145649, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2513
  ds.SetDefaultArmorData(145652, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2514
  ds.SetDefaultArmorData(139247, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2515
  ds.SetDefaultArmorData(139248, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2516
  ds.SetDefaultArmorData(139249, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2517
  ds.SetDefaultArmorData(139250, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2518
  ds.SetDefaultArmorData(139243, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2519
  ds.SetDefaultArmorData(139244, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2520
  ds.SetDefaultArmorData(139245, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2521
  ds.SetDefaultArmorData(139246, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2522
  ds.SetDefaultArmorData(139241, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2523
  ds.SetDefaultArmorData(139242, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2524
  ds.SetDefaultArmorData(543154, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2525
  ds.SetDefaultArmorData(543155, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2526
  ds.SetDefaultArmorData(543156, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2527
  ds.SetDefaultArmorData(543157, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2528
  ds.SetDefaultArmorData(543158, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2529
  ds.SetDefaultArmorData(543159, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2530
  ds.SetDefaultArmorData(543160, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2531
  ds.SetDefaultArmorData(543161, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2532
  ds.SetDefaultArmorData(543162, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2533
  ds.SetDefaultArmorData(543163, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2534
  ds.SetDefaultArmorData(143563, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2535
  ds.SetDefaultArmorData(548818, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2536
  ds.SetDefaultArmorData(3430, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2537
  ds.SetDefaultArmorData(144101, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2538
  ds.SetDefaultArmorData(544592, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2539
  ds.SetDefaultArmorData(3480, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2540
  ds.SetDefaultArmorData(23067, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2541
  ds.SetDefaultArmorData(43876, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2542
  ds.SetDefaultArmorData(436743, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2543
  ds.SetDefaultArmorData(16071, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2544
  ds.SetDefaultArmorData(16072, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2545
  ds.SetDefaultArmorData(16074, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2546
  ds.SetDefaultArmorData(16073, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2547
  ds.SetDefaultArmorData(139134, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2548
  ds.SetDefaultArmorData(15853, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2549
  ds.SetDefaultArmorData(43872, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2550
  ds.SetDefaultArmorData(139151, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2551
  ds.SetDefaultArmorData(143534, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2552
  ds.SetDefaultArmorData(536247, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2553
  ds.SetDefaultArmorData(144121, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2554
  ds.SetDefaultArmorData(53613, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2555
  ds.SetDefaultArmorData(53620, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2556
  ds.SetDefaultArmorData(436723, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2557
  ds.SetDefaultArmorData(143496, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2558
  ds.SetDefaultArmorData(143501, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2559
  ds.SetDefaultArmorData(143494, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2560
  ds.SetDefaultArmorData(143500, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2561
  ds.SetDefaultArmorData(3472, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2562
  ds.SetDefaultArmorData(3473, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2563
  ds.SetDefaultArmorData(3456, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2564
  ds.SetDefaultArmorData(3462, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2565
  ds.SetDefaultArmorData(3463, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2566
  ds.SetDefaultArmorData(144126, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2567
  ds.SetDefaultArmorData(17238, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2568
  ds.SetDefaultArmorData(18651, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2569
  ds.SetDefaultArmorData(8949, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2570
  ds.SetDefaultArmorData(18650, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2571
  ds.SetDefaultArmorData(764316, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2572
  ds.SetDefaultArmorData(18652, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2573
  ds.SetDefaultArmorData(6185, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2574
  ds.SetDefaultArmorData(18654, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2575
  ds.SetDefaultArmorData(8957, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2576
  ds.SetDefaultArmorData(18653, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2577
  ds.SetDefaultArmorData(764315, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2578
  ds.SetDefaultArmorData(18655, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2579
  ds.SetDefaultArmorData(7567, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2580
  ds.SetDefaultArmorData(145640, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2581
  ds.SetDefaultArmorData(145650, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2582
  ds.SetDefaultArmorData(145658, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2583
  ds.SetDefaultArmorData(139251, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2584
  ds.SetDefaultArmorData(543164, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2585
  ds.SetDefaultArmorData(20283, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2586
  ds.SetDefaultArmorData(144023, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2587
  ds.SetDefaultArmorData(226060, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2588
  ds.SetDefaultArmorData(23081, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2589
  ds.SetDefaultArmorData(144027, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2590
  ds.SetDefaultArmorData(226052, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2591
  ds.SetDefaultArmorData(145738, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2592
  ds.SetDefaultArmorData(145742, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2593
  ds.SetDefaultArmorData(226044, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2594
  ds.SetDefaultArmorData(15921, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2595
  ds.SetDefaultArmorData(15922, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2596
  ds.SetDefaultArmorData(32831, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2597
  ds.SetDefaultArmorData(4819, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2598
  ds.SetDefaultArmorData(18649, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2599
  ds.SetDefaultArmorData(8956, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2600
  ds.SetDefaultArmorData(18648, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2601
  ds.SetDefaultArmorData(764314, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2602
  ds.SetDefaultArmorData(18656, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2603
  ds.SetDefaultArmorData(7566, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2604
  ds.SetDefaultArmorData(23153, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2605
  ds.SetDefaultArmorData(144115, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2606
  ds.SetDefaultArmorData(143696, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2607
  ds.SetDefaultArmorData(143697, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2608
  ds.SetDefaultArmorData(143698, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2609
  ds.SetDefaultArmorData(143699, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2610
  ds.SetDefaultArmorData(143700, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2611
  ds.SetDefaultArmorData(143721, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2612
  ds.SetDefaultArmorData(143722, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2613
  ds.SetDefaultArmorData(143723, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2614
  ds.SetDefaultArmorData(143724, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2615
  ds.SetDefaultArmorData(143725, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2616
  ds.SetDefaultArmorData(143750, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2617
  ds.SetDefaultArmorData(143751, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2618
  ds.SetDefaultArmorData(143752, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2619
  ds.SetDefaultArmorData(143753, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2620
  ds.SetDefaultArmorData(143754, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2621
  ds.SetDefaultArmorData(50836, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2622
  ds.SetDefaultArmorData(3464, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2623
  ds.SetDefaultArmorData(3465, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2624
  ds.SetDefaultArmorData(143593, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2625
  ds.SetDefaultArmorData(143464, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKFUR) ; #DEBUG_LINE_NO:2626
  ds.SetDefaultArmorData(143465, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_EXCELLENT, ds.COVERAGE_POOR, 0, 0, ds.EXTRA_CLOAKFUR) ; #DEBUG_LINE_NO:2627
  ds.SetDefaultArmorData(4807, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2628
  ds.SetDefaultArmorData(7571, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2629
  ds.SetDefaultArmorData(145633, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2630
  ds.SetDefaultArmorData(145645, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_HEAD, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2631
  ds.SetDefaultArmorData(20257, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2632
  ds.SetDefaultArmorData(144009, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2633
  ds.SetDefaultArmorData(46672, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2634
  ds.SetDefaultArmorData(23131, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2635
  ds.SetDefaultArmorData(144095, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2636
  ds.SetDefaultArmorData(544584, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2637
  ds.SetDefaultArmorData(145632, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2638
  ds.SetDefaultArmorData(145635, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2639
  ds.SetDefaultArmorData(145644, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2640
  ds.SetDefaultArmorData(145651, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2641
  ds.SetDefaultArmorData(145655, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2642
  ds.SetDefaultArmorData(143591, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2643
  ds.SetDefaultArmorData(143607, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2644
  ds.SetDefaultArmorData(145722, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2645
  ds.SetDefaultArmorData(139235, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2646
  ds.SetDefaultArmorData(139236, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2647
  ds.SetDefaultArmorData(20280, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2648
  ds.SetDefaultArmorData(144021, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2649
  ds.SetDefaultArmorData(226062, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2650
  ds.SetDefaultArmorData(143556, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2651
  ds.SetDefaultArmorData(548819, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2652
  ds.SetDefaultArmorData(23078, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2653
  ds.SetDefaultArmorData(144025, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2654
  ds.SetDefaultArmorData(226050, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2655
  ds.SetDefaultArmorData(145735, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2656
  ds.SetDefaultArmorData(145739, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2657
  ds.SetDefaultArmorData(226042, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2658
  ds.SetDefaultArmorData(15913, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2659
  ds.SetDefaultArmorData(15914, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2660
  ds.SetDefaultArmorData(3432, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2661
  ds.SetDefaultArmorData(4817, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_MAX, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2662
  ds.SetDefaultArmorData(3426, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2663
  ds.SetDefaultArmorData(144099, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2664
  ds.SetDefaultArmorData(544589, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_MAX, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2665
  ds.SetDefaultArmorData(3477, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2666
  ds.SetDefaultArmorData(23064, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2667
  ds.SetDefaultArmorData(43879, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2668
  ds.SetDefaultArmorData(14466, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2669
  ds.SetDefaultArmorData(23049, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2670
  ds.SetDefaultArmorData(16064, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2671
  ds.SetDefaultArmorData(16067, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_POOR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2672
  ds.SetDefaultArmorData(43875, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2673
  ds.SetDefaultArmorData(23150, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2674
  ds.SetDefaultArmorData(3434, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2675
  ds.SetDefaultArmorData(3435, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2676
  ds.SetDefaultArmorData(144112, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2677
  ds.SetDefaultArmorData(139148, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_EXCELLENT, 0, 0, 0) ; #DEBUG_LINE_NO:2678
  ds.SetDefaultArmorData(6188, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2679
  ds.SetDefaultArmorData(143535, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2680
  ds.SetDefaultArmorData(536245, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_POOR, 0, 0, 0) ; #DEBUG_LINE_NO:2681
  ds.SetDefaultArmorData(144119, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2682
  ds.SetDefaultArmorData(53614, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2683
  ds.SetDefaultArmorData(53619, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2684
  ds.SetDefaultArmorData(436722, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2685
  ds.SetDefaultArmorData(143686, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2686
  ds.SetDefaultArmorData(143687, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2687
  ds.SetDefaultArmorData(143688, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2688
  ds.SetDefaultArmorData(143689, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2689
  ds.SetDefaultArmorData(143690, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2690
  ds.SetDefaultArmorData(143711, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2691
  ds.SetDefaultArmorData(143712, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2692
  ds.SetDefaultArmorData(143713, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2693
  ds.SetDefaultArmorData(143714, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2694
  ds.SetDefaultArmorData(143715, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2695
  ds.SetDefaultArmorData(143740, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2696
  ds.SetDefaultArmorData(143741, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2697
  ds.SetDefaultArmorData(143742, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2698
  ds.SetDefaultArmorData(143743, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2699
  ds.SetDefaultArmorData(143744, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2700
  ds.SetDefaultArmorData(143491, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2701
  ds.SetDefaultArmorData(143497, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2702
  ds.SetDefaultArmorData(3450, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2703
  ds.SetDefaultArmorData(3452, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2704
  ds.SetDefaultArmorData(3451, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_MAX, 0, 0, 0) ; #DEBUG_LINE_NO:2705
  ds.SetDefaultArmorData(3459, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_GOOD, 0, 0, 0) ; #DEBUG_LINE_NO:2706
  ds.SetDefaultArmorData(144123, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2707
  ds.SetDefaultArmorData(50834, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_FAIR, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2708
  ds.SetDefaultArmorData(436742, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_GOOD, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2709
  ds.SetDefaultArmorData(3474, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_EXCELLENT, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2710
  ds.SetDefaultArmorData(3475, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_FEET, ds.WARMTH_EXCELLENT, ds.COVERAGE_FAIR, 0, 0, 0) ; #DEBUG_LINE_NO:2711
  ds.SetDefaultArmorData(145642, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_CLOAK, 0, 0, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2712
  ds.SetDefaultArmorData(145660, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_CLOAK, 0, 0, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2713
  ds.SetDefaultArmorData(145641, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_CLOAK, 0, 0, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2714
  ds.SetDefaultArmorData(436740, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_CLOAK, 0, 0, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2715
  ds.SetDefaultArmorData(63308, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_CLOAK, 0, 0, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2716
  ds.SetDefaultArmorData(11733, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_CLOAK, 0, 0, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2717
  ds.SetDefaultArmorData(13097, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_CLOAK, 0, 0, 0, 0, ds.EXTRA_CLOAKCLOTH) ; #DEBUG_LINE_NO:2718
  ds.SetDefaultArmorData(3427, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2719
  ds.SetDefaultArmorData(143495, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2720
  ds.SetDefaultArmorData(143502, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2721
  ds.SetDefaultArmorData(143736, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2722
  ds.SetDefaultArmorData(143737, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2723
  ds.SetDefaultArmorData(143738, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2724
  ds.SetDefaultArmorData(143739, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2725
  ds.SetDefaultArmorData(139152, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2726
  ds.SetDefaultArmorData(10329, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2727
  ds.SetDefaultArmorData(10335, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2728
  ds.SetDefaultArmorData(145659, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2729
  ds.SetDefaultArmorData(139153, "Hothtrooper44_ArmorCompilation.esp", ds.GEARTYPE_IGNORE, 0, 0, 0, 0, 0) ; #DEBUG_LINE_NO:2730
EndFunction

Function RegisterForKeysOnLoad()
  Self.SendEvent_SKSE_RegisterForKeysOnLoad() ; #DEBUG_LINE_NO:2744
EndFunction

Function RegisterForEventsOnLoad()
  frostutil.GetExposureSystem().RegisterForEvents() ; #DEBUG_LINE_NO:2760
  frostutil.GetWetnessSystem().RegisterForEvents() ; #DEBUG_LINE_NO:2761
  frostutil.GetClimateSystem().RegisterForEvents() ; #DEBUG_LINE_NO:2762
  frostutil.GetWarmthSystem().RegisterForEvents() ; #DEBUG_LINE_NO:2763
  frostutil.GetCoverageSystem().RegisterForEvents() ; #DEBUG_LINE_NO:2764
  frostutil.GetRescueSystem().RegisterForEvents() ; #DEBUG_LINE_NO:2765
  frostutil.GetInterfaceHandler().RegisterForEvents() ; #DEBUG_LINE_NO:2766
  frostutil.GetExposureMeterHandler().RegisterForEvents() ; #DEBUG_LINE_NO:2767
  frostutil.GetWetnessMeterHandler().RegisterForEvents() ; #DEBUG_LINE_NO:2768
  frostutil.GetWeathersenseMeterHandler().RegisterForEvents() ; #DEBUG_LINE_NO:2769
EndFunction

Function RegisterForMenusOnLoad()
  (PlayerAlias as _frost_playerdialoguemonitor).RegisterForMenus() ; #DEBUG_LINE_NO:2777
  frostutil.GetInterfaceHandler().RegisterForMenus() ; #DEBUG_LINE_NO:2778
EndFunction

Bool Function CheckJSONReadWrite()
  String path = "../FrostfallData/startup_test_file" ; #DEBUG_LINE_NO:2786
  String test_key = "test_key" ; #DEBUG_LINE_NO:2787
  jsonutil.IntListResize(path, test_key, 7, 0) ; #DEBUG_LINE_NO:2788
  jsonutil.IntListSet(path, test_key, 0, 0) ; #DEBUG_LINE_NO:2789
  jsonutil.IntListSet(path, test_key, 1, 1) ; #DEBUG_LINE_NO:2790
  jsonutil.IntListSet(path, test_key, 2, 100) ; #DEBUG_LINE_NO:2791
  jsonutil.IntListSet(path, test_key, 3, 1000) ; #DEBUG_LINE_NO:2792
  jsonutil.IntListSet(path, test_key, 4, 5555) ; #DEBUG_LINE_NO:2793
  jsonutil.IntListSet(path, test_key, 5, -1) ; #DEBUG_LINE_NO:2794
  jsonutil.IntListSet(path, test_key, 6, 123456) ; #DEBUG_LINE_NO:2795
  Bool save_success = jsonutil.Save(path, False) ; #DEBUG_LINE_NO:2796
  If !save_success ; #DEBUG_LINE_NO:2797
    Debug.trace("[Frostfall][ERROR] Could not save test JSON file. Check that you have folder read/write permissions to Skyrim/Data/SKSE/FrostfallData (or, for Mod Organizer users, Mod Organizer/overwrite/SKSE/FrostfallData).", 0) ; #DEBUG_LINE_NO:2798
    Return False ; #DEBUG_LINE_NO:2799
  EndIf
  Bool load_success = jsonutil.Load(path) ; #DEBUG_LINE_NO:2801
  If !load_success ; #DEBUG_LINE_NO:2802
    Debug.trace("[Frostfall][ERROR] Could not load test JSON file. Check that you have folder read/write permissions to Skyrim/Data/SKSE/FrostfallData (or, for Mod Organizer users, Mod Organizer/overwrite/SKSE/FrostfallData).", 0) ; #DEBUG_LINE_NO:2803
    Return False ; #DEBUG_LINE_NO:2804
  EndIf
  Int val0 = jsonutil.IntListGet(path, test_key, 0) ; #DEBUG_LINE_NO:2806
  Int val1 = jsonutil.IntListGet(path, test_key, 1) ; #DEBUG_LINE_NO:2807
  Int val2 = jsonutil.IntListGet(path, test_key, 2) ; #DEBUG_LINE_NO:2808
  Int val3 = jsonutil.IntListGet(path, test_key, 3) ; #DEBUG_LINE_NO:2809
  Int val4 = jsonutil.IntListGet(path, test_key, 4) ; #DEBUG_LINE_NO:2810
  Int val5 = jsonutil.IntListGet(path, test_key, 5) ; #DEBUG_LINE_NO:2811
  Int val6 = jsonutil.IntListGet(path, test_key, 6) ; #DEBUG_LINE_NO:2812
  If val0 == 0 && val1 == 1 && val2 == 100 && val3 == 1000 && val4 == 5555 && val5 == -1 && val6 == 123456 ; #DEBUG_LINE_NO:2813
    jsonutil.IntListClear(path, test_key) ; #DEBUG_LINE_NO:2814
    Return True ; #DEBUG_LINE_NO:2815
  Else
    Debug.trace("[Frostfall][ERROR] Could not read from test JSON file. Check that you have folder read/write permissions to Skyrim/Data/SKSE/FrostfallData (or, for Mod Organizer users, Mod Organizer/overwrite/SKSE/FrostfallData).", 0) ; #DEBUG_LINE_NO:2817
    Return False ; #DEBUG_LINE_NO:2818
  EndIf
EndFunction

Function CheckDatastore()
  If camputil.GetSKSELoaded() ; #DEBUG_LINE_NO:2827
    Self.CheckDatastore_SKSE() ; #DEBUG_LINE_NO:2828
  Else
    Self.CheckDatastore_Vanilla() ; #DEBUG_LINE_NO:2830
  EndIf
EndFunction

Function CheckDatastore_SKSE()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2839
  Int[] armor_data = handler.GetDefaultArmorData("80145___Skyrim.esm") ; #DEBUG_LINE_NO:2840
  If armor_data[0] == handler.GEARTYPE_NOTFOUND ; #DEBUG_LINE_NO:2841
    Self.PopulateDefaultArmorData() ; #DEBUG_LINE_NO:2842
  EndIf
EndFunction

Function CheckDatastore_Vanilla()
  _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:2851
  _frost_legacyarmordatastore legacyDatastore = frostutil.GetLegacyArmorDatastore() ; #DEBUG_LINE_NO:2852
  Int[] protectionLevels = legacyDatastore.FindBodyProtectionLevels(ArmorHideCuirass) ; #DEBUG_LINE_NO:2853
  If protectionLevels[2] == handler.GEARTYPE_NOTFOUND ; #DEBUG_LINE_NO:2854
    legacyDatastore.PopulateDefaultArmorData() ; #DEBUG_LINE_NO:2855
  EndIf
EndFunction

Bool Function IsPluginLoaded(Int iFormID, String sPluginName)
  If isSKSELoaded ; #DEBUG_LINE_NO:2864
    Int i = Game.GetModByName(sPluginName) ; #DEBUG_LINE_NO:2865
    If i != 255 ; #DEBUG_LINE_NO:2866
      Debug.trace("[Frostfall] Loaded: " + sPluginName, 0) ; #DEBUG_LINE_NO:2867
      Return True ; #DEBUG_LINE_NO:2868
    Else
      Return False ; #DEBUG_LINE_NO:2870
    EndIf
  Else
    Bool b = Game.IsPluginInstalled(sPluginName) && Game.GetFormFromFile(iFormID, sPluginName) as Bool ; #DEBUG_LINE_NO:2873
    If b ; #DEBUG_LINE_NO:2874
      Debug.trace("[Frostfall] Loaded: " + sPluginName, 0) ; #DEBUG_LINE_NO:2875
      Return True ; #DEBUG_LINE_NO:2876
    Else
      Return False ; #DEBUG_LINE_NO:2878
    EndIf
  EndIf
EndFunction

Function SendEvent_FrostfallLoaded()
  fallbackeventemitter emitter = frostutil.GetEventEmitter_FrostfallLoaded() ; #DEBUG_LINE_NO:2888
  Int handle = emitter.Create("Frostfall_Loaded") ; #DEBUG_LINE_NO:2889
  If handle ; #DEBUG_LINE_NO:2890
    Bool sent = emitter.Send(handle) ; #DEBUG_LINE_NO:2891
  EndIf
EndFunction

Function SendEvent_SKSE_LoadProfileOnStartup()
  If isSKSELoaded ; #DEBUG_LINE_NO:2899
    Int handle = modevent.Create("Frostfall_LoadProfileOnStartup") ; #DEBUG_LINE_NO:2900
    If handle ; #DEBUG_LINE_NO:2901
      modevent.Send(handle) ; #DEBUG_LINE_NO:2902
    EndIf
  EndIf
EndFunction

Function SendEvent_SKSE_ApplyMeterPreset(Int aiValue)
  If isSKSELoaded ; #DEBUG_LINE_NO:2911
    Int handle = modevent.Create("Frostfall_ApplyMeterPreset") ; #DEBUG_LINE_NO:2912
    If handle ; #DEBUG_LINE_NO:2913
      modevent.PushInt(handle, aiValue) ; #DEBUG_LINE_NO:2914
      modevent.Send(handle) ; #DEBUG_LINE_NO:2915
    EndIf
  EndIf
EndFunction

Function SendEvent_SKSE_CheckInterfacePackage()
  If isSKSELoaded ; #DEBUG_LINE_NO:2924
    Int handle = modevent.Create("Frostfall_CheckInterfacePackage") ; #DEBUG_LINE_NO:2925
    If handle ; #DEBUG_LINE_NO:2926
      modevent.Send(handle) ; #DEBUG_LINE_NO:2927
    EndIf
  EndIf
EndFunction

Function SendEvent_SKSE_RegisterForKeysOnLoad()
  If isSKSELoaded ; #DEBUG_LINE_NO:2936
    Int handle = modevent.Create("Frostfall_RegisterForKeysOnLoad") ; #DEBUG_LINE_NO:2937
    If handle ; #DEBUG_LINE_NO:2938
      modevent.Send(handle) ; #DEBUG_LINE_NO:2939
    EndIf
  EndIf
EndFunction

Function SendEvent_SKSE_SaveSettingToCurrentProfile(String asKey, Int aiValue)
  If isSKSELoaded ; #DEBUG_LINE_NO:2948
    Int handle = modevent.Create("Frostfall_SaveSettingToCurrentProfile") ; #DEBUG_LINE_NO:2949
    If handle ; #DEBUG_LINE_NO:2950
      modevent.PushString(handle, asKey) ; #DEBUG_LINE_NO:2951
      modevent.PushInt(handle, aiValue) ; #DEBUG_LINE_NO:2952
      modevent.Send(handle) ; #DEBUG_LINE_NO:2953
    EndIf
  EndIf
EndFunction

Function SendEvent_SKSE_Upgrade_3_2_1()
  If isSKSELoaded ; #DEBUG_LINE_NO:2962
    Int handle = modevent.Create("Frostfall_Upgrade_3_2_1") ; #DEBUG_LINE_NO:2963
    If handle ; #DEBUG_LINE_NO:2964
      modevent.Send(handle) ; #DEBUG_LINE_NO:2965
    EndIf
  EndIf
EndFunction

Function ErrorSKSE(Int version)
  Debug.trace((("[Frostfall][Warning] Detected SKSE version " + (version as Float / 10000.0) as String) + ". Expected " + (Self.SKSE_MIN_VERSION as Float / 10000.0) as String) + " or newer. Using Fallback Mode.", 0) ; #DEBUG_LINE_NO:2979
  _Frost_CriticalError_SKSE.Show(version as Float / 10000.0, Self.SKSE_MIN_VERSION as Float / 10000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:2980
EndFunction

Function FatalErrorCampfire(Float version)
  Float version_formatted = version / 10000.0 ; #DEBUG_LINE_NO:2988
  Float min_version_formatted = Self.CAMPFIRE_MIN_VERSION as Float / 10000.0 ; #DEBUG_LINE_NO:2989
  Debug.trace((("[Frostfall][ERROR] Detected Campfire version " + version_formatted as String) + ", out of date! Expected " + min_version_formatted as String) + " or newer.", 0) ; #DEBUG_LINE_NO:2990
  While true
    _Frost_CriticalError_Campfire.Show(version_formatted, min_version_formatted, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:2992
    Utility.wait(3.0) ; #DEBUG_LINE_NO:2993
  EndWhile
EndFunction

Function FatalErrorSkyUIPackage(Int skyui_version)
  Debug.trace("[Frostfall][ERROR] Detected optional Frostfall SkyUI Interface Package, but the wrong version of SkyUI is installed!", 0) ; #DEBUG_LINE_NO:3002
  While true
    _Frost_CriticalError_SkyUIInterfacePackage.Show(skyui_version as Float, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:3004
    Utility.wait(3.0) ; #DEBUG_LINE_NO:3005
  EndWhile
EndFunction

Function FatalErrorSkyUIPackageOld()
  Debug.trace("[Frostfall][ERROR] Detected optional Frostfall SkyUI Interface Package, but it is out of date!", 0) ; #DEBUG_LINE_NO:3014
  While true
    _Frost_CriticalError_SkyUIInterfacePackageOld.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:3016
    Utility.wait(3.0) ; #DEBUG_LINE_NO:3017
  EndWhile
EndFunction

Function ErrorWearableLanterns()
  Debug.trace(("[Frostfall][ERROR] Detected Wearable Lanterns 4.01 or earlier, out of date! Expected " + Self.WEARABLELANTERNS_MIN_VERSION as String) + " or newer.", 0) ; #DEBUG_LINE_NO:3025
  _Frost_Error_WearableLanterns.Show(Self.WEARABLELANTERNS_MIN_VERSION, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:3026
EndFunction

Function Upgrade_3_0_1()
  _Frost_Setting_1PAnimationAllowed.SetValueInt(0) ; #DEBUG_LINE_NO:3040
  Debug.trace("[Frostfall] Upgraded to 3.0.1.", 0) ; #DEBUG_LINE_NO:3041
  _Frost_Upgraded_3_0_1.SetValueInt(2) ; #DEBUG_LINE_NO:3042
EndFunction

Function Upgrade_3_0_2()
  LItemSpellTomes75AllConjuration.AddForm(_Frost_SpellTomeConjureShelterLesser as Form, 1, 1) ; #DEBUG_LINE_NO:3050
  LItemSpellTomes75Conjuration.AddForm(_Frost_SpellTomeConjureShelterLesser as Form, 1, 1) ; #DEBUG_LINE_NO:3051
  LItemSpellTomes75Spells.AddForm(_Frost_SpellTomeConjureShelterLesser as Form, 1, 1) ; #DEBUG_LINE_NO:3052
  LItemScroll75Skill.AddForm(_Frost_ScrollConjureShelterLesser as Form, 1, 1) ; #DEBUG_LINE_NO:3053
  LItemSpellTomes100Conjuration.AddForm(_Frost_SpellTomeConjureShelterGreater as Form, 1, 1) ; #DEBUG_LINE_NO:3054
  MGRitualConjurationBooks.AddForm(_Frost_SpellTomeConjureShelterGreater as Form, 1, 1) ; #DEBUG_LINE_NO:3055
  LItemScroll100Skill.AddForm(_Frost_ScrollConjureShelterGreater as Form, 1, 1) ; #DEBUG_LINE_NO:3056
  Debug.trace("[Frostfall] Upgraded to 3.0.2.", 0) ; #DEBUG_LINE_NO:3057
  _Frost_Upgraded_3_0_2.SetValueInt(2) ; #DEBUG_LINE_NO:3058
EndFunction

Function Upgrade_3_1()
  If isSKSELoaded ; #DEBUG_LINE_NO:3066
    _frost_armorprotectiondatastorehandler handler = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:3067
    handler.CreateProtectionKeywordValueMaps() ; #DEBUG_LINE_NO:3068
    Int cleared_count = 0 ; #DEBUG_LINE_NO:3069
    If _Frost_PreviousVersion.GetValue() < 3.099999905 ; #DEBUG_LINE_NO:3070
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "0") ; #DEBUG_LINE_NO:3071
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "1") ; #DEBUG_LINE_NO:3072
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "2") ; #DEBUG_LINE_NO:3073
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "3") ; #DEBUG_LINE_NO:3074
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "4") ; #DEBUG_LINE_NO:3075
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "5") ; #DEBUG_LINE_NO:3076
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "6") ; #DEBUG_LINE_NO:3077
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "7") ; #DEBUG_LINE_NO:3078
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "8") ; #DEBUG_LINE_NO:3079
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorBody as Form, "9") ; #DEBUG_LINE_NO:3080
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "0") ; #DEBUG_LINE_NO:3081
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "1") ; #DEBUG_LINE_NO:3082
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "2") ; #DEBUG_LINE_NO:3083
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "3") ; #DEBUG_LINE_NO:3084
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "4") ; #DEBUG_LINE_NO:3085
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "5") ; #DEBUG_LINE_NO:3086
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "6") ; #DEBUG_LINE_NO:3087
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "7") ; #DEBUG_LINE_NO:3088
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "8") ; #DEBUG_LINE_NO:3089
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHead as Form, "9") ; #DEBUG_LINE_NO:3090
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "0") ; #DEBUG_LINE_NO:3091
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "1") ; #DEBUG_LINE_NO:3092
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "2") ; #DEBUG_LINE_NO:3093
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "3") ; #DEBUG_LINE_NO:3094
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "4") ; #DEBUG_LINE_NO:3095
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "5") ; #DEBUG_LINE_NO:3096
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "6") ; #DEBUG_LINE_NO:3097
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "7") ; #DEBUG_LINE_NO:3098
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "8") ; #DEBUG_LINE_NO:3099
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorHands as Form, "9") ; #DEBUG_LINE_NO:3100
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "0") ; #DEBUG_LINE_NO:3101
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "1") ; #DEBUG_LINE_NO:3102
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "2") ; #DEBUG_LINE_NO:3103
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "3") ; #DEBUG_LINE_NO:3104
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "4") ; #DEBUG_LINE_NO:3105
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "5") ; #DEBUG_LINE_NO:3106
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "6") ; #DEBUG_LINE_NO:3107
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "7") ; #DEBUG_LINE_NO:3108
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "8") ; #DEBUG_LINE_NO:3109
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorFeet as Form, "9") ; #DEBUG_LINE_NO:3110
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "0") ; #DEBUG_LINE_NO:3111
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "1") ; #DEBUG_LINE_NO:3112
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "2") ; #DEBUG_LINE_NO:3113
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "3") ; #DEBUG_LINE_NO:3114
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "4") ; #DEBUG_LINE_NO:3115
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "5") ; #DEBUG_LINE_NO:3116
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "6") ; #DEBUG_LINE_NO:3117
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "7") ; #DEBUG_LINE_NO:3118
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "8") ; #DEBUG_LINE_NO:3119
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorCloak as Form, "9") ; #DEBUG_LINE_NO:3120
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "0") ; #DEBUG_LINE_NO:3121
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "1") ; #DEBUG_LINE_NO:3122
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "2") ; #DEBUG_LINE_NO:3123
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "3") ; #DEBUG_LINE_NO:3124
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "4") ; #DEBUG_LINE_NO:3125
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "5") ; #DEBUG_LINE_NO:3126
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "6") ; #DEBUG_LINE_NO:3127
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "7") ; #DEBUG_LINE_NO:3128
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "8") ; #DEBUG_LINE_NO:3129
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorShield as Form, "9") ; #DEBUG_LINE_NO:3130
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "0") ; #DEBUG_LINE_NO:3131
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "1") ; #DEBUG_LINE_NO:3132
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "2") ; #DEBUG_LINE_NO:3133
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "3") ; #DEBUG_LINE_NO:3134
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "4") ; #DEBUG_LINE_NO:3135
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "5") ; #DEBUG_LINE_NO:3136
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "6") ; #DEBUG_LINE_NO:3137
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "7") ; #DEBUG_LINE_NO:3138
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "8") ; #DEBUG_LINE_NO:3139
      cleared_count += storageutil.ClearAllObjPrefix(handler._FrostData_ArmorIgnore as Form, "9") ; #DEBUG_LINE_NO:3140
      Debug.trace(("[Frostfall] Upgrade cleared " + cleared_count as String) + " old records.", 0) ; #DEBUG_LINE_NO:3141
    EndIf
    _Frost_Setting_DisplayTutorials.SetValueInt(2) ; #DEBUG_LINE_NO:3143
    Self.SendEvent_SKSE_SaveSettingToCurrentProfile("display_tutorials", _Frost_Setting_DisplayTutorials.GetValueInt()) ; #DEBUG_LINE_NO:3144
    Self.PopulateDefaultArmorData() ; #DEBUG_LINE_NO:3145
  EndIf
  If _Frost_PreviousVersion.GetValue() > 0.0 ; #DEBUG_LINE_NO:3147
    frostutil.GetFrostResistSystem().StartSystem() ; #DEBUG_LINE_NO:3148
  EndIf
  frostutil.GetClothingSystem().StartUp() ; #DEBUG_LINE_NO:3150
  Self.SendEvent_SKSE_ApplyMeterPreset(1) ; #DEBUG_LINE_NO:3151
  Debug.trace("[Frostfall] Upgraded to 3.1.", 0) ; #DEBUG_LINE_NO:3152
  _Frost_Upgraded_3_1.SetValueInt(2) ; #DEBUG_LINE_NO:3153
EndFunction

Function Upgrade_3_2()
  If _Frost_PreviousVersion.GetValue() > 0.0 ; #DEBUG_LINE_NO:3161
    If isSKYUILoaded ; #DEBUG_LINE_NO:3162
      Self.SendEvent_SKSE_Upgrade_3_2() ; #DEBUG_LINE_NO:3163
    EndIf
  EndIf
  Debug.trace("[Frostfall] Upgraded to 3.2.", 0) ; #DEBUG_LINE_NO:3166
  _Frost_Upgraded_3_2.SetValueInt(2) ; #DEBUG_LINE_NO:3167
EndFunction

Function SendEvent_SKSE_Upgrade_3_2()
  If isSKSELoaded ; #DEBUG_LINE_NO:3175
    Int handle = modevent.Create("Frostfall_Upgrade_3_2") ; #DEBUG_LINE_NO:3176
    If handle ; #DEBUG_LINE_NO:3177
      modevent.Send(handle) ; #DEBUG_LINE_NO:3178
    EndIf
  EndIf
EndFunction

Function Upgrade_3_2_1()
  If _Frost_PreviousVersion.GetValue() > 0.0 ; #DEBUG_LINE_NO:3188
    If isSKYUILoaded ; #DEBUG_LINE_NO:3189
      Self.SendEvent_SKSE_Upgrade_3_2_1() ; #DEBUG_LINE_NO:3190
    EndIf
  EndIf
  Debug.trace("[Frostfall] Upgraded to 3.2.1.", 0) ; #DEBUG_LINE_NO:3193
  _Frost_Upgraded_3_2_1.SetValueInt(2) ; #DEBUG_LINE_NO:3194
EndFunction

Function Upgrade_3_3_1()
  LItemSpellTomes25AllConjuration.AddForm(_Frost_SpellTomeBoundCloakLesser as Form, 1, 1) ; #DEBUG_LINE_NO:3202
  LItemSpellTomes25Conjuration.AddForm(_Frost_SpellTomeBoundCloakLesser as Form, 1, 1) ; #DEBUG_LINE_NO:3203
  LItemScroll25Skill.AddForm(_Frost_ScrollBoundCloakLesser as Form, 1, 1) ; #DEBUG_LINE_NO:3204
  LItemSpellTomes50AllConjuration.AddForm(_Frost_SpellTomeBoundCloakGreater as Form, 1, 1) ; #DEBUG_LINE_NO:3205
  LItemSpellTomes50Conjuration.AddForm(_Frost_SpellTomeBoundCloakGreater as Form, 1, 1) ; #DEBUG_LINE_NO:3206
  LItemSpellTomes50Spells.AddForm(_Frost_SpellTomeBoundCloakGreater as Form, 1, 1) ; #DEBUG_LINE_NO:3207
  If _Frost_PreviousVersion.GetValue() > 0.0 ; #DEBUG_LINE_NO:3208
    frostutil.GetClothingDatastoreHandler().CreateProtectionKeywordValueMaps() ; #DEBUG_LINE_NO:3209
    If isSKSELoaded ; #DEBUG_LINE_NO:3210
      _frost_armorprotectiondatastorehandler ap = frostutil.GetClothingDatastoreHandler() ; #DEBUG_LINE_NO:3211
      ap.SetArmorDataByKey("260764___Campfire.esm", ap.GEARTYPE_CLOAK, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:3212
      ap.SetArmorDataByKey("260765___Campfire.esm", ap.GEARTYPE_CLOAK, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:3213
      ap.SetArmorDataByKey("356637___Frostfall.esp", ap.GEARTYPE_CLOAK, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, False) ; #DEBUG_LINE_NO:3214
      ap.SetArmorDataByKey("359400___Frostfall.esp", ap.GEARTYPE_CLOAK, 12, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, True) ; #DEBUG_LINE_NO:3215
    EndIf
    If !isSKSELoaded ; #DEBUG_LINE_NO:3217
      frostutil.GetLegacyArmorDatastore().InitializeCustomArrays() ; #DEBUG_LINE_NO:3218
    EndIf
    _frost_clothingsystem clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:3220
    Armor[] tempArmor = new Armor[31] ; #DEBUG_LINE_NO:3221
    Int i = 0 ; #DEBUG_LINE_NO:3222
    While i < 31 ; #DEBUG_LINE_NO:3223
      tempArmor[i] = clothing.WornGearForms[i] ; #DEBUG_LINE_NO:3224
      i += 1 ; #DEBUG_LINE_NO:3225
    EndWhile
    clothing.WornGearMainForms = new Armor[5] ; #DEBUG_LINE_NO:3227
    clothing.WornGearForms = new Armor[26] ; #DEBUG_LINE_NO:3228
    Int armorCount = commonarrayhelper.ArrayCountArmor(tempArmor) ; #DEBUG_LINE_NO:3229
    Int j = 0 ; #DEBUG_LINE_NO:3230
    While j < armorCount ; #DEBUG_LINE_NO:3231
      Armor theArmor = tempArmor[j] ; #DEBUG_LINE_NO:3232
      If theArmor ; #DEBUG_LINE_NO:3233
        PlayerRef.UnequipItem(theArmor as Form, False, True) ; #DEBUG_LINE_NO:3234
        Utility.wait(0.5) ; #DEBUG_LINE_NO:3235
        PlayerRef.EquipItem(theArmor as Form, False, True) ; #DEBUG_LINE_NO:3236
      EndIf
      j += 1 ; #DEBUG_LINE_NO:3238
    EndWhile
    Utility.wait(2.0) ; #DEBUG_LINE_NO:3240
    _Frost_ReleaseNotes_3_3_1.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:3241
  EndIf
  Debug.trace("[Frostfall] Upgraded to 3.3.1.", 0) ; #DEBUG_LINE_NO:3243
  _Frost_Upgraded_3_3_1.SetValueInt(2) ; #DEBUG_LINE_NO:3244
EndFunction

Function Upgrade_3_4_1()
  frostutil.GetClimateSystem().InitializeArrays() ; #DEBUG_LINE_NO:3252
  hotfix341 = True ; #DEBUG_LINE_NO:3253
EndFunction

Function Upgrade_3_4()
  If _Frost_PreviousVersion.GetValue() > 0.0 ; #DEBUG_LINE_NO:3260
    frostutil.GetPlayerStateSystem().StartSystem() ; #DEBUG_LINE_NO:3261
    _Frost_ReleaseNotes_3_4.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:3262
  EndIf
  Debug.trace("[Frostfall] Upgraded to 3.4.", 0) ; #DEBUG_LINE_NO:3264
  _Frost_Upgraded_3_4.SetValueInt(2) ; #DEBUG_LINE_NO:3265
EndFunction
