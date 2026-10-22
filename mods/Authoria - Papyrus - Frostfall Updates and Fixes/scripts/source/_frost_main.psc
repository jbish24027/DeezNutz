ScriptName _Frost_Main Extends Quest
{ This script handles starting the mod for the first time, setting appropriate start-up aliases, and running compatibility on startup. }

;-- Variables ---------------------------------------
Bool gave_friend_items = False
Bool isSKYUILoaded = False
Int stars_counter = 0
Bool started_via_stars = False

;-- Properties --------------------------------------
GlobalVariable Property FrostfallRunning Auto
GlobalVariable Property GameHour Auto
ReferenceAlias Property PlayerAlias Auto
Actor Property PlayerRef Auto
ReferenceAlias Property RiverwoodFriend Auto
Armor Property _Camp_ArmorSonsBoots Auto
Armor Property _Camp_Cloak_BasicBurlap Auto
MiscObject Property _Camp_Tent_LeatherSmall1BR_MISC Auto
GlobalVariable Property _Frost_CheckInitialEquipment Auto
ImageSpaceModifier Property _Frost_ColdISM_Level3 Auto
ImageSpaceModifier Property _Frost_ColdISM_Level4 Auto
ImageSpaceModifier Property _Frost_ColdISM_Level5 Auto
GlobalVariable Property _Frost_DatastoreInitialized Auto
Armor Property _Frost_DummyBoots Auto
Armor Property _Frost_DummyCuirass Auto
Armor Property _Frost_DummyGauntlets Auto
Armor Property _Frost_DummyHelmet Auto
Armor Property _Frost_DummyShield Auto
Message Property _Frost_FirstStartup_1 Auto
Message Property _Frost_FirstStartup_2 Auto
Message Property _Frost_FirstStartup_3 Auto
Message Property _Frost_FirstStartup_3SE Auto
Spell Property _Frost_LegacyConfig_Spell Auto
Spell Property _Frost_NoWait_Spell Auto
Activator Property _Frost_PerkNodeController_Endurance Auto
Message Property _Frost_StartStarsMsg Auto
Message Property _Frost_StartingUpDoneMsg Auto
Message Property _Frost_StartingUpMsg Auto
Book Property _Frost_SurvivorsGuide Auto
Quest Property _Frost_TrackingQuest Auto

;-- Functions ---------------------------------------

; Skipped compiler generated GetState

; Skipped compiler generated GotoState

Event OnInit()
  isSKYUILoaded = Game.GetFormFromFile(16779284, "SkyUI_SE.esp") as Bool || Game.GetFormFromFile(16779284, "SkyUI.esp") as Bool ; #DEBUG_LINE_NO:46
  If isSKYUILoaded && _Frost_LegacyConfig_Spell ; #DEBUG_LINE_NO:47
    PlayerRef.RemoveSpell(_Frost_LegacyConfig_Spell) ; #DEBUG_LINE_NO:48
  ElseIf _Frost_LegacyConfig_Spell
    PlayerRef.AddSpell(_Frost_LegacyConfig_Spell, False) ; #DEBUG_LINE_NO:50
  EndIf
  Self.RegisterForSingleUpdate(5 as Float) ; #DEBUG_LINE_NO:53
EndEvent

Event OnUpdate()
  If !Game.IsFightingControlsEnabled() || PlayerRef.IsInInterior() ; #DEBUG_LINE_NO:62
    Self.RegisterForSingleUpdate(5 as Float) ; #DEBUG_LINE_NO:63
    Return  ; #DEBUG_LINE_NO:64
  EndIf
  If _Frost_TrackingQuest && _Frost_TrackingQuest.GetStage() == 0 ; #DEBUG_LINE_NO:67
    If isSKYUILoaded ; #DEBUG_LINE_NO:68
      _Frost_TrackingQuest.SetStage(10) ; #DEBUG_LINE_NO:69
    Else
      _Frost_TrackingQuest.SetStage(15) ; #DEBUG_LINE_NO:71
    EndIf
  EndIf
  If _Frost_TrackingQuest && (_Frost_TrackingQuest.GetStage() == 10 || _Frost_TrackingQuest.GetStage() == 15) && !started_via_stars ; #DEBUG_LINE_NO:75
    If !camputil.IsRefInInterior(PlayerRef as ObjectReference) && PlayerRef.GetAngleX() <= -55.0 && (GameHour.GetValue() > 19.0 || GameHour.GetValue() < 7.0) ; #DEBUG_LINE_NO:76,77,78
      stars_counter += 1 ; #DEBUG_LINE_NO:79
      If stars_counter >= 2 ; #DEBUG_LINE_NO:80
        Self.StartPrompt() ; #DEBUG_LINE_NO:81
      EndIf
    EndIf
    Self.RegisterForSingleUpdate(5 as Float) ; #DEBUG_LINE_NO:84
  EndIf
  If !gave_friend_items ; #DEBUG_LINE_NO:87
    Self.AddFriendItems() ; #DEBUG_LINE_NO:88
    Self.RegisterForSingleUpdate(5 as Float) ; #DEBUG_LINE_NO:89
  EndIf
EndEvent

Function StartPrompt()
  If !_Frost_StartStarsMsg
    stars_counter = 0
    Return
  EndIf
  Int i = _Frost_StartStarsMsg.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:94
  If i == 0 ; #DEBUG_LINE_NO:95
    started_via_stars = True ; #DEBUG_LINE_NO:96
    FrostfallRunning.SetValueInt(2) ; #DEBUG_LINE_NO:97
    Self.StartFrostfall(False) ; #DEBUG_LINE_NO:98
  Else
    stars_counter = 0 ; #DEBUG_LINE_NO:100
  EndIf
EndFunction

Function RegisterForModEvents()
  fallbackeventemitter startEvent = frostutil.GetEventEmitter_StartFrostfall() ; #DEBUG_LINE_NO:105
  fallbackeventemitter stopEvent = frostutil.GetEventEmitter_StopFrostfall() ; #DEBUG_LINE_NO:106
  startEvent.RegisterFormForModEventWithFallback("Frost_StartFrostfall", "StartFrostfall", Self as Form) ; #DEBUG_LINE_NO:108
  stopEvent.RegisterFormForModEventWithFallback("Frost_StopFrostfall", "StopFrostfall", Self as Form) ; #DEBUG_LINE_NO:109
EndFunction

Function StartFrostfall(Bool abBypassStartupMessage)
  Debug.trace("[Frostfall] Starting Frostfall...", 0) ; #DEBUG_LINE_NO:113
  If _Frost_StartingUpMsg
    _Frost_StartingUpMsg.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:114
  EndIf
  frostutil.GetClothingDatastoreHandler().InitializeDatastore() ; #DEBUG_LINE_NO:116
  If !Self.IsRunning() ; #DEBUG_LINE_NO:118
    Self.Start() ; #DEBUG_LINE_NO:119
  EndIf
  PlayerAlias.ForceRefTo(PlayerRef as ObjectReference) ; #DEBUG_LINE_NO:121
  Self.StartModFirstTime(abBypassStartupMessage) ; #DEBUG_LINE_NO:122
  If _Frost_TrackingQuest
    _Frost_TrackingQuest.SetStage(20) ; #DEBUG_LINE_NO:123
  EndIf
  Utility.Wait(2.0) ; #DEBUG_LINE_NO:124
  Self.StartAllSystems() ; #DEBUG_LINE_NO:125
  frostutil.GetCompatibilitySystem().RunCompatibility() ; #DEBUG_LINE_NO:126
  frostutil.GetCompatibilitySystem().SendEvent_FrostfallLoaded() ; #DEBUG_LINE_NO:127
  Self.CheckInitialEquipment() ; #DEBUG_LINE_NO:128
  If _Frost_StartingUpDoneMsg
    _Frost_StartingUpDoneMsg.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:129
  EndIf
  Debug.trace("[Frostfall] Frostfall is now running.", 0) ; #DEBUG_LINE_NO:130
EndFunction

Function StopFrostfall()
  Debug.trace("[Frostfall] Stopping Frostfall...", 0) ; #DEBUG_LINE_NO:134
  If Self.IsRunning() ; #DEBUG_LINE_NO:135
    Self.Stop() ; #DEBUG_LINE_NO:136
  EndIf
  PlayerAlias.Clear() ; #DEBUG_LINE_NO:138
  Self.StopAllSystems() ; #DEBUG_LINE_NO:139
  If !Game.IsFastTravelControlsEnabled() ; #DEBUG_LINE_NO:140
    Game.EnableFastTravel(True) ; #DEBUG_LINE_NO:141
  EndIf
  PlayerRef.RemoveSpell(_Frost_NoWait_Spell) ; #DEBUG_LINE_NO:143
  _Frost_ColdISM_Level3.Remove() ; #DEBUG_LINE_NO:144
  _Frost_ColdISM_Level4.Remove() ; #DEBUG_LINE_NO:145
  _Frost_ColdISM_Level5.Remove() ; #DEBUG_LINE_NO:146
  Self.RemoveAllMeters() ; #DEBUG_LINE_NO:147
  Self.UnregisterCampfireSkill() ; #DEBUG_LINE_NO:148
  Debug.trace("[Frostfall] Frostfall shut down successfully.", 0) ; #DEBUG_LINE_NO:149
EndFunction

Function StartAllSystems()
  frostutil.GetClothingDatastoreHandler().StartSystem() ; #DEBUG_LINE_NO:153
  frostutil.GetClimateSystem().StartSystem() ; #DEBUG_LINE_NO:154
  frostutil.GetHeatSourceSystem().StartSystem() ; #DEBUG_LINE_NO:155
  frostutil.GetClothingSystem().StartSystem() ; #DEBUG_LINE_NO:156
  frostutil.GetRescueSystem().StartSystem() ; #DEBUG_LINE_NO:157
  frostutil.GetShelterSystem().StartSystem() ; #DEBUG_LINE_NO:158
  frostutil.GetWarmthSystem().StartSystem() ; #DEBUG_LINE_NO:159
  frostutil.GetCoverageSystem().StartSystem() ; #DEBUG_LINE_NO:160
  frostutil.GetExposureSystem().StartSystem() ; #DEBUG_LINE_NO:161
  frostutil.GetWetnessSystem().StartSystem() ; #DEBUG_LINE_NO:162
  frostutil.GetFrostResistSystem().StartSystem() ; #DEBUG_LINE_NO:163
  frostutil.GetPlayerStateSystem().StartSystem() ; #DEBUG_LINE_NO:164
EndFunction

Function StopAllSystems()
  frostutil.GetClothingDatastoreHandler().StopSystem() ; #DEBUG_LINE_NO:168
  frostutil.GetClimateSystem().StopSystem() ; #DEBUG_LINE_NO:169
  frostutil.GetHeatSourceSystem().StopSystem() ; #DEBUG_LINE_NO:170
  frostutil.GetClothingSystem().StopSystem() ; #DEBUG_LINE_NO:171
  frostutil.GetRescueSystem().StopSystem() ; #DEBUG_LINE_NO:172
  frostutil.GetShelterSystem().StopSystem() ; #DEBUG_LINE_NO:173
  frostutil.GetWarmthSystem().StopSystem() ; #DEBUG_LINE_NO:174
  frostutil.GetCoverageSystem().StopSystem() ; #DEBUG_LINE_NO:175
  frostutil.GetExposureSystem().StopSystem() ; #DEBUG_LINE_NO:176
  frostutil.GetWetnessSystem().StopSystem() ; #DEBUG_LINE_NO:177
  frostutil.GetFrostResistSystem().StopSystem() ; #DEBUG_LINE_NO:178
  frostutil.GetPlayerStateSystem().StopSystem() ; #DEBUG_LINE_NO:179
  Utility.Wait(2 as Float) ; #DEBUG_LINE_NO:180
EndFunction

Function CheckInitialEquipment()
  If !_Frost_CheckInitialEquipment
    Return
  EndIf
  _Frost_CheckInitialEquipment.SetValue(2 as Float) ; #DEBUG_LINE_NO:184
  PlayerRef.AddItem(_Frost_DummyCuirass as Form, 1, True) ; #DEBUG_LINE_NO:185
  PlayerRef.AddItem(_Frost_DummyHelmet as Form, 1, True) ; #DEBUG_LINE_NO:186
  PlayerRef.AddItem(_Frost_DummyGauntlets as Form, 1, True) ; #DEBUG_LINE_NO:187
  PlayerRef.AddItem(_Frost_DummyBoots as Form, 1, True) ; #DEBUG_LINE_NO:188
  PlayerRef.AddItem(_Frost_DummyShield as Form, 1, True) ; #DEBUG_LINE_NO:189
  PlayerRef.EquipItem(_Frost_DummyCuirass as Form, False, True) ; #DEBUG_LINE_NO:190
  Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:191
  PlayerRef.EquipItem(_Frost_DummyHelmet as Form, False, True) ; #DEBUG_LINE_NO:192
  Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:193
  PlayerRef.EquipItem(_Frost_DummyGauntlets as Form, False, True) ; #DEBUG_LINE_NO:194
  Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:195
  PlayerRef.EquipItem(_Frost_DummyBoots as Form, False, True) ; #DEBUG_LINE_NO:196
  Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:197
  PlayerRef.EquipItem(_Frost_DummyShield as Form, False, True) ; #DEBUG_LINE_NO:198
  Utility.Wait(2.0) ; #DEBUG_LINE_NO:199
  _Frost_CheckInitialEquipment.SetValue(1 as Float) ; #DEBUG_LINE_NO:200
  PlayerRef.RemoveItem(_Frost_DummyCuirass as Form, 1, True, None) ; #DEBUG_LINE_NO:201
  PlayerRef.RemoveItem(_Frost_DummyHelmet as Form, 1, True, None) ; #DEBUG_LINE_NO:202
  PlayerRef.RemoveItem(_Frost_DummyGauntlets as Form, 1, True, None) ; #DEBUG_LINE_NO:203
  PlayerRef.RemoveItem(_Frost_DummyBoots as Form, 1, True, None) ; #DEBUG_LINE_NO:204
  PlayerRef.RemoveItem(_Frost_DummyShield as Form, 1, True, None) ; #DEBUG_LINE_NO:205
  Utility.Wait(1.0) ; #DEBUG_LINE_NO:206
  _frost_clothingsystem Clothing = frostutil.GetClothingSystem() ; #DEBUG_LINE_NO:207
  If Clothing.initial_body ; #DEBUG_LINE_NO:208
    PlayerRef.EquipItem(Clothing.initial_body as Form, False, True) ; #DEBUG_LINE_NO:209
    Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:210
  EndIf
  If Clothing.initial_head ; #DEBUG_LINE_NO:212
    PlayerRef.EquipItem(Clothing.initial_head as Form, False, True) ; #DEBUG_LINE_NO:213
    Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:214
  EndIf
  If Clothing.initial_hands ; #DEBUG_LINE_NO:216
    PlayerRef.EquipItem(Clothing.initial_hands as Form, False, True) ; #DEBUG_LINE_NO:217
    Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:218
  EndIf
  If Clothing.initial_feet ; #DEBUG_LINE_NO:220
    PlayerRef.EquipItem(Clothing.initial_feet as Form, False, True) ; #DEBUG_LINE_NO:221
    Utility.Wait(0.200000003) ; #DEBUG_LINE_NO:222
  EndIf
  If Clothing.initial_shield ; #DEBUG_LINE_NO:224
    PlayerRef.EquipItem(Clothing.initial_shield as Form, False, True) ; #DEBUG_LINE_NO:225
  EndIf
EndFunction

Function AddFriendItems()
  Actor friend = RiverwoodFriend.GetActorRef() ; #DEBUG_LINE_NO:230
  If friend ; #DEBUG_LINE_NO:231
    If friend.GetItemCount(_Camp_Tent_LeatherSmall1BR_MISC as Form) == 0 ; #DEBUG_LINE_NO:232
      friend.AddItem(_Camp_Tent_LeatherSmall1BR_MISC as Form, 1, False) ; #DEBUG_LINE_NO:233
    EndIf
    If friend.GetItemCount(_Camp_ArmorSonsBoots as Form) == 0 ; #DEBUG_LINE_NO:241
      friend.AddItem(_Camp_ArmorSonsBoots as Form, 1, False) ; #DEBUG_LINE_NO:242
    EndIf
    gave_friend_items = True ; #DEBUG_LINE_NO:244
  EndIf
EndFunction

Function StartModFirstTime(Bool abBypassStartupMessage)
  If _Frost_TrackingQuest && _Frost_TrackingQuest.GetStage() == 20 ; #DEBUG_LINE_NO:249
    Return  ; #DEBUG_LINE_NO:250
  Else
    If !abBypassStartupMessage && _Frost_FirstStartup_1 ; #DEBUG_LINE_NO:253
      _Frost_FirstStartup_1.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:254
    EndIf
    Utility.Wait(1 as Float) ; #DEBUG_LINE_NO:256
    If _Frost_SurvivorsGuide
      PlayerRef.AddItem(_Frost_SurvivorsGuide as Form, 1, False) ; #DEBUG_LINE_NO:257
    EndIf
    Utility.Wait(6 as Float) ; #DEBUG_LINE_NO:258
    If _Frost_FirstStartup_2
      _Frost_FirstStartup_2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:259
    EndIf
    Utility.Wait(1 as Float) ; #DEBUG_LINE_NO:260
    If isSKYUILoaded && _Frost_FirstStartup_3 ; #DEBUG_LINE_NO:261
      _Frost_FirstStartup_3.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:262
    ElseIf _Frost_FirstStartup_3SE
      _Frost_FirstStartup_3SE.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) ; #DEBUG_LINE_NO:264
    EndIf
  EndIf
EndFunction

Function UnregisterCampfireSkill()
  GlobalVariable CampfireAPIVersion = Game.GetFormFromFile(258494, "Campfire.esm") as GlobalVariable ; #DEBUG_LINE_NO:270
  If CampfireAPIVersion as Bool && CampfireAPIVersion.GetValueInt() >= 4 ; #DEBUG_LINE_NO:271
    Bool b = camputil.UnregisterPerkTree(_Frost_PerkNodeController_Endurance, "Frostfall.esp") ; #DEBUG_LINE_NO:272
  Else
    Debug.trace("[Campfire] ERROR: Unable to register Campfire Skill System for Frostfall.esp. Campfire was not found or the version loaded is not compatible. Expected CampUtil API 4 or higher, got " + CampfireAPIVersion.GetValueInt() as String, 0) ; #DEBUG_LINE_NO:274
  EndIf
EndFunction

Function RemoveAllMeters()
  If camputil.GetSKSELoaded() ; #DEBUG_LINE_NO:279
    Self.SendEvent_FrostfallRemoveExposureMeter() ; #DEBUG_LINE_NO:280
    Self.SendEvent_FrostfallRemoveWetnessMeter() ; #DEBUG_LINE_NO:281
    Self.SendEvent_FrostfallRemoveWeathersenseMeter() ; #DEBUG_LINE_NO:282
  EndIf
EndFunction

Function SendEvent_FrostfallRemoveExposureMeter()
  Int handle = modevent.Create("Frostfall_RemoveExposureMeter") ; #DEBUG_LINE_NO:287
  If handle ; #DEBUG_LINE_NO:288
    modevent.Send(handle) ; #DEBUG_LINE_NO:289
  EndIf
EndFunction

Function SendEvent_FrostfallRemoveWetnessMeter()
  Int handle = modevent.Create("Frostfall_RemoveWetnessMeter") ; #DEBUG_LINE_NO:294
  If handle ; #DEBUG_LINE_NO:295
    modevent.Send(handle) ; #DEBUG_LINE_NO:296
  EndIf
EndFunction

Function SendEvent_FrostfallRemoveWeathersenseMeter()
  Int handle = modevent.Create("Frostfall_RemoveWeathersenseMeter") ; #DEBUG_LINE_NO:301
  If handle ; #DEBUG_LINE_NO:302
    modevent.Send(handle) ; #DEBUG_LINE_NO:303
  EndIf
EndFunction
