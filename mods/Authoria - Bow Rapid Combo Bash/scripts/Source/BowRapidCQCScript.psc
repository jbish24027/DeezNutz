ScriptName BowRapidCQCScript Extends activemagiceffect

;-- Variables ---------------------------------------
Actor Player
Int WAT
Perk QuickShotUnlock

;-- Properties --------------------------------------
bowbbconfigscript Property BowRP Auto
Idle Property HKSIdleA Auto
Idle Property HKSIdleB Auto
Idle Property HKSIdleC Auto
Idle Property HKSIdleD Auto
Idle Property HKSIdleE Auto
Idle Property HKSIdleF Auto

;-- Functions ---------------------------------------

; Skipped compiler generated GetState

; Skipped compiler generated GotoState

Function SafeUnregisterForAnimationEvent(ObjectReference objRef, String eventName)
  If objRef == None ; #DEBUG_LINE_NO:21
    Return  ; #DEBUG_LINE_NO:22
  EndIf
  If objRef ; #DEBUG_LINE_NO:24
    Self.UnRegisterForAnimationEvent(objRef, eventName) ; #DEBUG_LINE_NO:25
  EndIf
EndFunction

Bool Function HasQuickShotUnlock()
  If Player == None
    Return False
  EndIf
  If QuickShotUnlock == None
    QuickShotUnlock = Game.GetFormFromFile(0x000BB5, "Requiem - Weapons and Armor Redone.esp") as Perk
  EndIf
  Return QuickShotUnlock != None && Player.HasPerk(QuickShotUnlock)
EndFunction

Event OnEffectStart(Actor akTarget, Actor akCaster)
  Player = akTarget ; #DEBUG_LINE_NO:34
  If Player as Bool && (Player as ObjectReference) as Bool ; #DEBUG_LINE_NO:35
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackA") ; #DEBUG_LINE_NO:36
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackB") ; #DEBUG_LINE_NO:37
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackC") ; #DEBUG_LINE_NO:38
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackD") ; #DEBUG_LINE_NO:39
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackE") ; #DEBUG_LINE_NO:40
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackF") ; #DEBUG_LINE_NO:41
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_StageStartA") ; #DEBUG_LINE_NO:42
    Self.RegisterForAnimationEvent(Player as ObjectReference, "HKS_StageEndA") ; #DEBUG_LINE_NO:43
    Self.RegisterForAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:44
    Self.RegisterForAnimationEvent(Player as ObjectReference, "tailcombatidle") ; #DEBUG_LINE_NO:45
    Self.GotoState("BasicState") ; #DEBUG_LINE_NO:46
  EndIf
EndEvent

Event OnEffectFinish(Actor akTarget, Actor akCaster)
  Player = None ; #DEBUG_LINE_NO:51
EndEvent

Event OnUnload()
  Self.CleanupAnimationEvents() ; #DEBUG_LINE_NO:55
EndEvent

Function CleanupAnimationEvents()
  If Player == None ; #DEBUG_LINE_NO:59
    Return  ; #DEBUG_LINE_NO:60
  EndIf
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackA") ; #DEBUG_LINE_NO:62
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackB") ; #DEBUG_LINE_NO:63
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackC") ; #DEBUG_LINE_NO:64
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackD") ; #DEBUG_LINE_NO:65
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackE") ; #DEBUG_LINE_NO:66
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_AttackF") ; #DEBUG_LINE_NO:67
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_StageStartA") ; #DEBUG_LINE_NO:68
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "HKS_StageEndA") ; #DEBUG_LINE_NO:69
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:70
  Self.UnRegisterForAnimationEvent(Player as ObjectReference, "tailcombatidle") ; #DEBUG_LINE_NO:71
  Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255)) ; #DEBUG_LINE_NO:72
EndFunction

;-- State -------------------------------------------
State BCWaitInput1

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey1
      If !Self.HasQuickShotUnlock()
        Return
      EndIf
      Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop")
      Player.PlayIdle(HKSIdleD)
      Self.UnRegisterForKey(BowRP.BCKey1)
      WAT = 0
      Self.GotoState("BasicState")
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey1)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey1)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" || asEventName == "HKS_StageEndA" ; #DEBUG_LINE_NO:79
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:80
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State BTrackCombo1

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey1
      If !Self.HasQuickShotUnlock()
        Return
      EndIf
      WAT = 3
      Self.UnRegisterForKey(BowRP.BCKey1)
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey1)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey1)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" ; #DEBUG_LINE_NO:107
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:108
    EndIf
    If asEventName == "HKS_StageStartA" ; #DEBUG_LINE_NO:110
      If WAT == 0 ; #DEBUG_LINE_NO:111
        Self.GotoState("BCWaitInput1") ; #DEBUG_LINE_NO:112
      ElseIf WAT == 3 ; #DEBUG_LINE_NO:113
        If !Self.HasQuickShotUnlock()
          WAT = 0
          Self.GotoState("BasicState")
          Return
        EndIf
        Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:114
        Player.PlayIdle(HKSIdleD) ; #DEBUG_LINE_NO:115
        Self.UnRegisterForKey(BowRP.BCKey1) ; #DEBUG_LINE_NO:116
        WAT = 0 ; #DEBUG_LINE_NO:117
        Self.GotoState("BasicState") ; #DEBUG_LINE_NO:118
      EndIf
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State BTrackCombo2

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey1
      If !Self.HasQuickShotUnlock()
        Return
      EndIf
      WAT = 3
      Self.UnRegisterForKey(BowRP.BCKey1)
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey1)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey1)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" ; #DEBUG_LINE_NO:143
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:144
    EndIf
    If asEventName == "HKS_StageStartA" ; #DEBUG_LINE_NO:146
      If WAT == 0 ; #DEBUG_LINE_NO:147
        Self.GotoState("bcwaitinput2") ; #DEBUG_LINE_NO:148
      ElseIf WAT == 3 ; #DEBUG_LINE_NO:149
        If !Self.HasQuickShotUnlock()
          WAT = 0
          Self.GotoState("BasicState")
          Return
        EndIf
        Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:150
        Player.PlayIdle(HKSIdleC) ; #DEBUG_LINE_NO:151
        Self.UnRegisterForKey(BowRP.BCKey1) ; #DEBUG_LINE_NO:152
        WAT = 0 ; #DEBUG_LINE_NO:153
        Self.GotoState("BasicState") ; #DEBUG_LINE_NO:154
      EndIf
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State BasicState

  Function OnKeyDown(Int KeyCode)
    If !ui.IsMenuOpen("Dialogue Menu") && !Utility.IsInMenuMode()
      If KeyCode == BowRP.BCKey1
        If !Self.HasQuickShotUnlock()
          Return
        EndIf
        Player.PlayIdle(HKSIdleC)
        Self.UnRegisterForKey(BowRP.BCKey1)
      EndIf
      If KeyCode == BowRP.BCKey2
        Player.PlayIdle(HKSIdleE)
        Self.UnRegisterForKey(BowRP.BCKey2)
      EndIf
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey1)
    Self.RegisterForKey(BowRP.BCKey2)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey1)
    Self.UnRegisterForKey(BowRP.BCKey2)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "HKS_AttackA" ; #DEBUG_LINE_NO:179
      Self.GotoState("NormalCombo1") ; #DEBUG_LINE_NO:180
    EndIf
    If asEventName == "HKS_AttackB" ; #DEBUG_LINE_NO:182
      Self.GotoState("NormalCombo2") ; #DEBUG_LINE_NO:183
    EndIf
    If asEventName == "HKS_AttackC" ; #DEBUG_LINE_NO:185
      Self.GotoState("BTrackCombo1") ; #DEBUG_LINE_NO:186
    EndIf
    If asEventName == "HKS_AttackD" ; #DEBUG_LINE_NO:188
      Self.GotoState("BTrackCombo2") ; #DEBUG_LINE_NO:189
    EndIf
    If asEventName == "HKS_AttackE" ; #DEBUG_LINE_NO:191
      Self.GotoState("ctrackcombo1") ; #DEBUG_LINE_NO:192
    EndIf
    If asEventName == "HKS_AttackF" ; #DEBUG_LINE_NO:194
      Self.GotoState("ctrackcombo2") ; #DEBUG_LINE_NO:195
    EndIf
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" ; #DEBUG_LINE_NO:197
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:198
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State Clean

  Event onBeginState()
    WAT = 0 ; #DEBUG_LINE_NO:294
    Self.GotoState("BasicState") ; #DEBUG_LINE_NO:295
  EndEvent
EndState

;-- State -------------------------------------------
State NormalCombo1

  Function OnKeyDown(Int KeyCode)
    If KeyCode == input.GetMappedKey("Left Attack/Block", 255)
      WAT = 1
      Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" ; #DEBUG_LINE_NO:303
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:304
    EndIf
    If asEventName == "HKS_StageStartA" ; #DEBUG_LINE_NO:306
      If WAT == 0 ; #DEBUG_LINE_NO:307
        Self.GotoState("ncwaitinput1") ; #DEBUG_LINE_NO:308
      ElseIf WAT == 1 ; #DEBUG_LINE_NO:309
        If !Self.HasQuickShotUnlock()
          WAT = 0
          Self.GotoState("BasicState")
          Return
        EndIf
        Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:310
        Player.PlayIdle(HKSIdleB) ; #DEBUG_LINE_NO:311
        Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255)) ; #DEBUG_LINE_NO:312
        WAT = 0 ; #DEBUG_LINE_NO:313
        Self.GotoState("BasicState") ; #DEBUG_LINE_NO:314
      EndIf
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State NormalCombo2

  Function OnKeyDown(Int KeyCode)
    If KeyCode == input.GetMappedKey("Left Attack/Block", 255)
      WAT = 2
      Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" ; #DEBUG_LINE_NO:339
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:340
    EndIf
    If asEventName == "HKS_StageStartA" ; #DEBUG_LINE_NO:342
      If WAT == 0 ; #DEBUG_LINE_NO:343
        Self.GotoState("ncwaitinput2") ; #DEBUG_LINE_NO:344
      ElseIf WAT == 2 ; #DEBUG_LINE_NO:345
        If !Self.HasQuickShotUnlock()
          WAT = 0
          Self.GotoState("BasicState")
          Return
        EndIf
        Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:346
        Player.PlayIdle(HKSIdleA) ; #DEBUG_LINE_NO:347
        Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255)) ; #DEBUG_LINE_NO:348
        WAT = 0 ; #DEBUG_LINE_NO:349
        Self.GotoState("BasicState") ; #DEBUG_LINE_NO:350
      EndIf
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State bcwaitinput2

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey1
      If !Self.HasQuickShotUnlock()
        Return
      EndIf
      Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop")
      Player.PlayIdle(HKSIdleC)
      Self.UnRegisterForKey(BowRP.BCKey1)
      WAT = 0
      Self.GotoState("BasicState")
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey1)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey1)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" || asEventName == "HKS_StageEndA" ; #DEBUG_LINE_NO:375
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:376
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State ccwaitinput1

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey2
      Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop")
      Player.PlayIdle(HKSIdleF)
      Self.UnRegisterForKey(BowRP.BCKey2)
      WAT = 0
      Self.GotoState("BasicState")
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey2)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey2)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" || asEventName == "HKS_StageEndA" ; #DEBUG_LINE_NO:403
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:404
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State ccwaitinput2

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey2
      Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop")
      Player.PlayIdle(HKSIdleE)
      Self.UnRegisterForKey(BowRP.BCKey2)
      WAT = 0
      Self.GotoState("BasicState")
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey2)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey2)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" || asEventName == "HKS_StageEndA" ; #DEBUG_LINE_NO:230
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:231
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State ctrackcombo1

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey2
      WAT = 4
      Self.UnRegisterForKey(BowRP.BCKey2)
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey2)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey2)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" ; #DEBUG_LINE_NO:258
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:259
    EndIf
    If asEventName == "HKS_StageStartA" ; #DEBUG_LINE_NO:261
      If WAT == 0 ; #DEBUG_LINE_NO:262
        Self.GotoState("ccwaitinput1") ; #DEBUG_LINE_NO:263
      ElseIf WAT == 4 ; #DEBUG_LINE_NO:264
        Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:265
        Player.PlayIdle(HKSIdleF) ; #DEBUG_LINE_NO:266
        Self.UnRegisterForKey(BowRP.BCKey2) ; #DEBUG_LINE_NO:267
        WAT = 0 ; #DEBUG_LINE_NO:268
        Self.GotoState("BasicState") ; #DEBUG_LINE_NO:269
      EndIf
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State ctrackcombo2

  Function OnKeyDown(Int KeyCode)
    If KeyCode == BowRP.BCKey2
      WAT = 4
      Self.UnRegisterForKey(BowRP.BCKey2)
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(BowRP.BCKey2)
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(BowRP.BCKey2)
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" ; #DEBUG_LINE_NO:431
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:432
    EndIf
    If asEventName == "HKS_StageStartA" ; #DEBUG_LINE_NO:434
      If WAT == 0 ; #DEBUG_LINE_NO:435
        Self.GotoState("ccwaitinput2") ; #DEBUG_LINE_NO:436
      ElseIf WAT == 4 ; #DEBUG_LINE_NO:437
        Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop") ; #DEBUG_LINE_NO:438
        Player.PlayIdle(HKSIdleE) ; #DEBUG_LINE_NO:439
        Self.UnRegisterForKey(BowRP.BCKey2) ; #DEBUG_LINE_NO:440
        WAT = 0 ; #DEBUG_LINE_NO:441
        Self.GotoState("BasicState") ; #DEBUG_LINE_NO:442
      EndIf
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State ncwaitinput1

  Function OnKeyDown(Int KeyCode)
    If KeyCode == input.GetMappedKey("Left Attack/Block", 255)
      If !Self.HasQuickShotUnlock()
        Return
      EndIf
      Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop")
      Player.PlayIdle(HKSIdleB)
      Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
      WAT = 0
      Self.GotoState("BasicState")
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" || asEventName == "HKS_StageEndA" ; #DEBUG_LINE_NO:467
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:468
    EndIf
  EndEvent
EndState

;-- State -------------------------------------------
State ncwaitinput2

  Function OnKeyDown(Int KeyCode)
    If KeyCode == input.GetMappedKey("Left Attack/Block", 255)
      If !Self.HasQuickShotUnlock()
        Return
      EndIf
      Debug.SendAnimationEvent(Player as ObjectReference, "Idlestop")
      Player.PlayIdle(HKSIdleA)
      Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
      WAT = 0
      Self.GotoState("BasicState")
    EndIf
  EndFunction

  Event onBeginState()
    Self.RegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event onEndState()
    Self.UnRegisterForKey(input.GetMappedKey("Left Attack/Block", 255))
  EndEvent

  Event OnAnimationEvent(ObjectReference akSource, String asEventName)
    If asEventName == "tailcombatidle" || asEventName == "Idlestop" || asEventName == "HKS_StageEndA" ; #DEBUG_LINE_NO:495
      Self.GotoState("Clean") ; #DEBUG_LINE_NO:496
    EndIf
  EndEvent
EndState
