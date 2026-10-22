Scriptname _WS_Main extends Quest
{Basic Wenches OStim - transaction / scene controller.}

; This plugin's basename is fixed, so forms are resolved by file (no VMAD properties).
String Property MODFILE = "Authoria - Basic Wenches OStim.esp" AutoReadOnly

; --- form helpers ---------------------------------------------------------
GlobalVariable Function GVar(int aiFormID)
    Return Game.GetFormFromFile(aiFormID, MODFILE) as GlobalVariable
EndFunction

ReferenceAlias Function HiredWench()
    Return Self.GetAlias(1) as ReferenceAlias   ; alias ID 1 = HiredWench
EndFunction

; --- cost: inverse of Speech, clamped 50..500 -----------------------------
Int Function ComputeCost()
    Float speech = Game.GetPlayer().GetActorValue("Speechcraft")
    Float t = (speech - 15.0) / 85.0
    If t < 0.0
        t = 0.0
    ElseIf t > 1.0
        t = 1.0
    EndIf
    Int cost = (500.0 - (t * 450.0)) as Int
    cost = ((cost + 2) / 5) * 5    ; round to nearest 5
    If cost < 50
        cost = 50
    ElseIf cost > 500
        cost = 500
    EndIf
    Return cost
EndFunction

; --- pre-roll: runs every time the dialogue menu OPENS ---------------------
; Sets the globals the proposition lines' conditions read, so the wench's
; reply (broke / success x4 / fail x4) is already decided when the player
; clicks the option. One roll per menu open.
Function RollProposition()
    Actor pl = Game.GetPlayer()
    Int cost = ComputeCost()
    GVar(0x800).SetValueInt(cost)                       ; _WS_Cost (displayed = charged)
    GVar(0x803).SetValueInt(Utility.RandomInt(1, 4))    ; _WS_Variation
    If pl.GetItemCount(Game.GetForm(0xF)) < cost
        GVar(0x802).SetValueInt(2)                      ; _WS_Outcome = broke
    ElseIf Utility.RandomInt(1, 100) <= GVar(0x801).GetValueInt()
        GVar(0x802).SetValueInt(1)                      ; _WS_Outcome = success
    Else
        GVar(0x802).SetValueInt(0)                      ; _WS_Outcome = failure
    EndIf
EndFunction

; --- success line clicked: pay her + she follows ---------------------------
Function AcceptProposition(Actor akWench)
    If akWench == None
        Return
    EndIf
    Int cost = GVar(0x800).GetValueInt()
    Game.GetPlayer().RemoveItem(Game.GetForm(0xF), cost, true, akWench)
    HiredWench().ForceRefTo(akWench)          ; alias package = follow the player
    akWench.EvaluatePackage()
    GVar(0x804).SetValueInt(1)                ; _WS_Active = hired
EndFunction

; --- "Here is good." -> begin the OStim scene -----------------------------
Function StartWenchScene(Actor akWench)
    If akWench == None
        Return
    EndIf
    ; The partner is already chosen and roles are obvious - suppress OStim's
    ; add-actor and dom/sub role prompts for THIS start only, leaving only the
    ; furniture prompt. These are OStim MCM globals; save + restore the user's
    ; own settings once the (asynchronous) start has finished.
    GlobalVariable addActors = Game.GetFormFromFile(0xE45, "OStim.esp") as GlobalVariable
    GlobalVariable roleStraight = Game.GetFormFromFile(0xDF3, "OStim.esp") as GlobalVariable
    GlobalVariable roleGay = Game.GetFormFromFile(0xDF4, "OStim.esp") as GlobalVariable
    Int prevAdd = addActors.GetValueInt()
    Int prevStraight = roleStraight.GetValueInt()
    Int prevGay = roleGay.GetValueInt()
    addActors.SetValueInt(0)
    roleStraight.SetValueInt(0)
    roleGay.SetValueInt(0)

    OThread.QuickStart(OActorUtil.ToArray(Game.GetPlayer(), akWench))
    HiredWench().Clear()                      ; drop the follow package
    GVar(0x804).SetValueInt(0)                ; _WS_Active = idle (re-hireable)

    ; Player-thread start is async - wait until it is actually running (all
    ; startup prompts done), or give up after 15s, then restore the settings.
    Int tries = 30
    While tries > 0 && !OThread.IsRunning(0)
        Utility.Wait(0.5)
        tries -= 1
    EndWhile
    addActors.SetValueInt(prevAdd)
    roleStraight.SetValueInt(prevStraight)
    roleGay.SetValueInt(prevGay)
EndFunction

; --- "On second thought - not now." ---------------------------------------
Function DismissWench()
    HiredWench().Clear()
    GVar(0x804).SetValueInt(0)
EndFunction
