ScriptName _Authoria_Init_MasterSequence extends Quest

Quest Property RequiemInstallQuest Auto
Quest Property StartingChoicesQuest Auto

Spell Property Traits_SelectionSpell Auto

GlobalVariable Property _Authoria_Init_Running Auto

Message Property WelcomeMessage Auto
Message Property DifficultyMessage Auto
Message Property FinishMessage Auto

Bool RequiemDone
Bool StartingChoicesDone
Bool TraitsDone
Bool SequenceStarted

Event OnInit()
    If _Authoria_Init_Running
        _Authoria_Init_Running.SetValueInt(0)
    EndIf

    RegisterForMenu("RaceSex Menu")
    RegisterSequenceEvents()
    HoldDevotionStartup()
EndEvent

Event OnMenuClose(String menuName)
    If menuName == "RaceSex Menu"
        UnregisterForMenu("RaceSex Menu")
        StartSequence()
    EndIf
EndEvent

Function RegisterSequenceEvents()
    RegisterForModEvent("_Authoria_Init_RequiemDone", "OnRequiemDone")
    RegisterForModEvent("_Authoria_Init_StartingChoicesDone", "OnStartingChoicesDone")
    RegisterForModEvent("_Authoria_Init_TraitsDone", "OnTraitsDone")
EndFunction

Function StartSequence()
    If SequenceStarted
        Return
    EndIf

    SequenceStarted = True
    SetRunning(True)
    LockPlayer()

    RequiemDone = False
    SendModEvent("_Authoria_Init_RunRequiemInstall")
    WaitForRequiem()
    LockPlayer()

    ShowWelcomePrompt()

    StartingChoicesDone = False
    If StartingChoicesQuest
        StartingChoicesQuest.Start()
    Else
        StartingChoicesDone = True
    EndIf
    WaitForStartingChoices()
    LockPlayer()
    Utility.Wait(2.0)

    TraitsDone = False
    If Traits_SelectionSpell
        Traits_SelectionSpell.Cast(Game.GetPlayer())
    Else
        TraitsDone = True
    EndIf
    WaitForTraits()
    LockPlayer()
    Utility.Wait(2.0)

    ; Requiem birthsign selection (Requiem - Birthsigns Redone, via the SkySigns b612 UI).
    ; Resolved at runtime so no ESP master/property fill is needed; completion is detected
    ; by the ChooseBirthsign power removing itself once a birthsign is picked.
    Spell chooseBirthsign = Game.GetFormFromFile(0x000813, "Requiem - Birthsigns Redone.esp") as Spell
    If chooseBirthsign
        Actor player = Game.GetPlayer()
        player.AddSpell(chooseBirthsign, False)
        Utility.Wait(0.1)
        chooseBirthsign.Cast(player)
        WaitForBirthsign(player, chooseBirthsign)
    Else
        Debug.Trace("[Authoria Init] ChooseBirthsign spell not found; skipping birthsign step.")
    EndIf
    LockPlayer()
    Utility.Wait(1.0)

    ; Devotion race-based startup popup(s): driven here so they appear AFTER the
    ; birthsign grid and BEFORE the difficulty message. Held since OnInit; release the
    ; gate and block until every popup is dismissed (choice+confirm for choice races,
    ; a single info box otherwise). Blocks with no timeout; the difficulty step re-locks.
    WaitForDevotion()
    LockPlayer()
    Utility.Wait(1.0)

    Debug.Trace("[Authoria Init] Showing difficulty picker.")
    String recordingName = PickDifficultyRecording()
    Debug.Trace("[Authoria Init] Difficulty picker selected recording: " + recordingName)
    LockPlayer()

    RebuildMcmRegistrations()
    LockPlayer()

    If recordingName
        Debug.Trace("[Authoria Init] Starting MCM Recorder playback: " + recordingName)
        McmRecorder_Player.PlayRecording(recordingName, mcmLoadWaitTime = 30.0, verbose = False)
        Debug.Trace("[Authoria Init] Finished MCM Recorder playback: " + recordingName)
    EndIf
    LockPlayer()

    PlayOStimRecording()
    LockPlayer()

    ShowFinishPrompt()

    FinishSequence()
EndFunction

Function ShowWelcomePrompt()
    If _Authoria_Init_PrismUI.ShowNotice("welcome", "{}")
        String promptAction = WaitForPrismaPromptAction()
        _Authoria_Init_PrismUI.Close()
        If promptAction == "notice|welcome|continue"
            Return
        EndIf
        Debug.Trace("[Authoria Init] PRISMA welcome prompt unavailable or timed out; using vanilla fallback.")
    EndIf

    If WelcomeMessage
        WelcomeMessage.Show()
    EndIf
EndFunction

Function ShowFinishPrompt()
    If _Authoria_Init_PrismUI.ShowNotice("finish", "{}")
        String promptAction = WaitForPrismaPromptAction()
        _Authoria_Init_PrismUI.Close()
        If promptAction == "notice|finish|continue"
            Return
        EndIf
        Debug.Trace("[Authoria Init] PRISMA finish prompt unavailable or timed out; using vanilla fallback.")
    EndIf

    If FinishMessage
        FinishMessage.Show()
    EndIf
EndFunction

String Function PickDifficultyRecording()
    If _Authoria_Init_PrismUI.ShowChoice("difficulty", "{}")
        String promptAction = WaitForPrismaPromptAction()
        _Authoria_Init_PrismUI.Close()
        If promptAction == "difficulty|easy"
            Return "Authoria_Easy"
        ElseIf promptAction == "difficulty|normal"
            Return "Authoria_Base"
        ElseIf promptAction == "difficulty|hard"
            Return "Authoria_Hard"
        Else
            Debug.Trace("[Authoria Init] PRISMA difficulty prompt unavailable, timed out, or returned unexpected action: " + promptAction)
        EndIf
    EndIf

    If !DifficultyMessage
        Return "Authoria_Base"
    EndIf

    Int choice = DifficultyMessage.Show()
    If choice == 0
        Return "Authoria_Easy"
    ElseIf choice == 2
        Return "Authoria_Hard"
    EndIf
    Return "Authoria_Base"
EndFunction

; --- NSFW-profile OStim recording -------------------------------------------
; The NSFW profile ships an extra MCM Recorder preset in
; `Authoria - Ostim tweaks and Patches\McmRecorder\AUTHORIA_OSTIM` that configures the
; adult stack. It must run right after the difficulty recording and before the finish
; prompt. OStim.esp is active ONLY in the NSFW profile, so gating on it leaves the Main
; profile's sequence byte-for-byte unchanged (this whole step is skipped there).
; `Game.IsPluginInstalled` covers both regular and ESL-flagged plugins.
Function PlayOStimRecording()
    If !Game.IsPluginInstalled("OStim.esp")
        Return
    EndIf

    Debug.Trace("[Authoria Init] OStim detected; starting MCM Recorder playback: AUTHORIA_OSTIM")
    McmRecorder_Player.PlayRecording("AUTHORIA_OSTIM", mcmLoadWaitTime = 30.0, verbose = False)
    Debug.Trace("[Authoria Init] Finished MCM Recorder playback: AUTHORIA_OSTIM")
EndFunction

; --- SkyUI MCM registration rebuild -----------------------------------------
; SkyUI does not let menus register on their own. SKI_ConfigManager broadcasts
; SKICP_configManagerReady and every menu answers it at once. RegisterMod puts the
; manager into its BUSY state while it works, and BUSY overrides RegisterMod to return
; -2 without doing anything, so every menu that calls during that window is dropped for
; that round. Dropped menus retry on the next broadcast -- but ONLY until one succeeds:
; SKI_ConfigBase.OnConfigManagerReady returns early forever once _configManager is set.
; SKI_ConfigManager.CleanUp() then blanks any slot whose menu reads GetFormID() == 0 at
; that instant. A menu that registers and is later blanked is gone for the session and
; never retries, because it believes it is already in. With ~125 menus answering the same
; broadcast that is a lottery, and the loser is stable across new games.
;
; ForceReset sends SKICP_configManagerReset first, which clears _configManager on every
; menu, then wipes all 128 slots and re-broadcasts. That clears the per-menu latch, so
; everything registers again from scratch. Run it before playback so the recording always
; sees a complete list.
Function RebuildMcmRegistrations()
    ; SKI_ConfigManagerInstance, the quest SkyUI puts the config manager on.
    SKI_ConfigManager manager = Game.GetFormFromFile(0x00000802, "SkyUI_SE.esp") as SKI_ConfigManager
    If !manager
        Debug.Trace("[Authoria Init] MCM rebuild skipped: SkyUI config manager not found.")
        Return
    EndIf

    Int before = CountRegisteredMcms(manager)
    Debug.Trace("[Authoria Init] MCM rebuild: " + before + " menu(s) registered before reset.")

    manager.ForceReset()

    ; ForceReset re-broadcasts immediately; SkyUI then re-broadcasts every 5 seconds for
    ; six rounds and every 30 seconds after that. Menus turned away by the BUSY lock come
    ; in over those rounds, so wait for the count to stop moving rather than a fixed time.
    ; WaitMenuMode is used because this runs while the sequence is driving menus.
    Int stable = 0
    Int last = -1
    Float elapsed = 0.0
    While stable < 4 && elapsed < 180.0
        Utility.WaitMenuMode(2.0)
        elapsed += 2.0
        Int current = CountRegisteredMcms(manager)
        If current == last && current > 0
            stable += 1
        Else
            stable = 0
        EndIf
        last = current
    EndWhile

    Debug.Trace("[Authoria Init] MCM rebuild: " + last + " menu(s) registered after " + elapsed + "s (was " + before + ").")

    If last < before
        Debug.Trace("[Authoria Init] MCM rebuild WARNING: fewer menus than before the reset.")
    EndIf
EndFunction

Int Function CountRegisteredMcms(SKI_ConfigManager manager)
    String[] names = manager.ModNames
    If !names
        Return 0
    EndIf
    Int count = 0
    Int i = 0
    While i < names.Length
        If names[i] != ""
            count += 1
        EndIf
        i += 1
    EndWhile
    Return count
EndFunction

String Function WaitForPrismaPromptAction()
    ; Blocks until the user acts on the PRISMA prompt. No timeout: the sequence must
    ; wait for the player, however long they take.
    While True
        While _Authoria_Init_PrismUI.GetPendingActionCount() > 0
            String promptAction = _Authoria_Init_PrismUI.ConsumeNextAction()
            If promptAction != ""
                Return promptAction
            EndIf
        EndWhile
        Utility.WaitMenuMode(0.1)
    EndWhile
    Return ""
EndFunction

Function LockPlayer()
    Game.GetPlayer().SetDontMove(True)
    Game.DisablePlayerControls(abMovement = True, abFighting = True, abCamSwitch = True, abLooking = True, abSneaking = True, abMenu = False, abActivate = True, abJournalTabs = False)
EndFunction

Function FinishSequence()
    _Authoria_Init_PrismUI.Close()
    SetRunning(False)
    Game.GetPlayer().SetDontMove(False)
    Game.EnablePlayerControls()
    Stop()
EndFunction

Function FailSequence(String reason)
    Debug.Trace("[Authoria Init] " + reason)
    ReleaseDevotionStartup()
    _Authoria_Init_PrismUI.Close()
    SetRunning(False)
    Game.GetPlayer().SetDontMove(False)
    Game.EnablePlayerControls()
EndFunction

Function SetRunning(Bool running)
    If _Authoria_Init_Running
        _Authoria_Init_Running.SetValueInt(running as Int)
    EndIf
EndFunction

Bool Function WaitForRequiem()
    While !RequiemDone
        Utility.WaitMenuMode(0.5)
    EndWhile
    Return RequiemDone
EndFunction

Bool Function WaitForStartingChoices()
    While !StartingChoicesDone
        Utility.WaitMenuMode(0.5)
    EndWhile
    Return StartingChoicesDone
EndFunction

Bool Function WaitForTraits()
    While !TraitsDone
        Utility.WaitMenuMode(0.5)
    EndWhile
    Return TraitsDone
EndFunction

Bool Function WaitForBirthsign(Actor player, Spell chooseBirthsign)
    While player.HasSpell(chooseBirthsign)
        Utility.WaitMenuMode(0.5)
    EndWhile
    Return !player.HasSpell(chooseBirthsign)
EndFunction

; --- Devotion startup-popup integration -------------------------------------
; Devotion's PDV__ManagerQuest (00C325:Devotion.esp) shows its race-based startup
; popup(s) on a 1s tick once the origin race resolves (right as RaceMenu closes) and
; its own gate -- the PapyrusUtil StorageUtil int "PDV.Startup.UnifiedChoiceComplete"
; -- is not yet 1. Origin capture is one-way: once captured it stays resolved, so a
; control lock cannot re-suppress the popup. The gate is therefore the only reliable
; hold, and it must be set BEFORE origin resolves. We use only Devotion's public
; StorageUtil contract -- no Devotion file is edited, no property is filled.

Bool Function IsDevotionPresent()
    Return Game.GetFormFromFile(0x00C325, "Devotion.esp") != None
EndFunction

Function HoldDevotionStartup()
    ; Called from OnInit at game start (before origin can resolve) so Devotion's popup
    ; is held until the master sequence drives it at the birthsign -> difficulty step.
    If IsDevotionPresent()
        StorageUtil.SetIntValue(None, "PDV.Startup.UnifiedChoiceComplete", 1)
        Debug.Trace("[Authoria Init] Devotion detected; startup popup held (UnifiedChoiceComplete=1).")
    EndIf
EndFunction

Function ReleaseDevotionStartup()
    ; Fail-safe: if the sequence aborts before the Devotion step runs, never leave
    ; Devotion's startup permanently muted. Clearing the gate lets Devotion show its
    ; popup normally once controls are restored.
    If IsDevotionPresent()
        StorageUtil.SetIntValue(None, "PDV.Startup.UnifiedChoiceComplete", 0)
    EndIf
EndFunction

Bool Function WaitForDevotion()
    ; Skip cleanly if Devotion is not installed.
    If !IsDevotionPresent()
        Return True
    EndIf

    ; Release the held gate; Devotion's manager fires the popup(s) on its next tick.
    StorageUtil.SetIntValue(None, "PDV.Startup.UnifiedChoiceComplete", 0)

    ; Safety net for the rare custom-race deferral where origin has not captured yet:
    ; Devotion's IsOriginCaptureSafe needs movement + menu controls enabled. Enable
    ; controls so origin can resolve, but keep the player pinned. The caller re-locks
    ; after this returns.
    Actor player = Game.GetPlayer()
    Game.EnablePlayerControls()
    player.SetDontMove(True)

    While StorageUtil.GetIntValue(None, "PDV.Startup.UnifiedChoiceComplete") != 1
        Utility.WaitMenuMode(0.5)
    EndWhile

    Return StorageUtil.GetIntValue(None, "PDV.Startup.UnifiedChoiceComplete") == 1
EndFunction

Event OnRequiemDone(String eventName, String strArg, Float numArg, Form sender)
    RequiemDone = True
EndEvent

Event OnStartingChoicesDone(String eventName, String strArg, Float numArg, Form sender)
    StartingChoicesDone = True
EndEvent

Event OnTraitsDone(String eventName, String strArg, Float numArg, Form sender)
    TraitsDone = True
EndEvent
