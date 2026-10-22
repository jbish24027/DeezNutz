ScriptName _Talent_PlayInstrument extends activemagiceffect
; ARR - Bards Reborn Tweaks. Re-based on the First Person Interactions superset of this script
; (it already merges Offset-Movement + Player-Reactions + first-person/ImprovedCamera + favorites/
; inventory-menu handling). Our integration on top:
;   * play-mode select on activate: mastered (>=100) -> BaB full-library picker; else learned
;     songbooks -> learned-song picker (any skill); else SgT random tier play.
;   * end of a finished random performance: cap skill at 100, mirror _LP_BardSkill = best instrument,
;     and advance any pending BaB tavern/jarl gig (economy rides this hook now).
;   * SgT's auto buffs/debuffs and passive inn-tip donations removed (D7/D10) - buffs come from BR Spellsongs.

int Broken
bool ALLGUD_Was_On
bool returntofirstperson
int SongToPlay
int SpecialInstrument
; FPI update: the player's mapped "Toggle POV" key (keyboard device 0 / controller device 2),
; registered during a performance so first<->third person toggles on the player's real keybind
; instead of the old hardcoded 33/273.
int iPOVKey
int iPOVControllerKey

; --- ARR Bards Reborn Tweaks: forced-song state for THIS cast (read from the BabBard alias at
; OnEffectStart). When set, a picker handed us a chosen song to play through SgT's shell instead
; of running the random tier play - so movement, NPC reactions, anims and first-person all happen.
bool bForcedThisCast
bool bForcedVoiceThisCast
sound ForcedSongThisCast
int ForcedLengthThisCast
formlist ForcedVersesThisCast
int ForcedVerseCountThisCast

; --- ARR Bards Reborn Tweaks additions ---
globalvariable Property TalentDrum Auto
globalvariable Property TalentLute Auto
globalvariable Property TalentFlute Auto
globalvariable Property LPBardSkill Auto
quest Property TavernQuest Auto
quest Property JarlQuest Auto
spell Property SongbookAbility Auto
formlist Property LearnedSongbooks Auto
_LP_BardQuestPlayerScript Property BabBard Auto
; ---

sound Property DuoSongs_2 Auto

message Property _Talent_Pro_OK3 Auto

message Property _Talent_Clueless_Broken1 Auto

idle Property IdleStop_Loose Auto

message Property _Talent_Clueless_OK4 Auto

globalvariable Property _Talent_ReceiveOvation Auto

globalvariable Property _Talent_IsPerformingTerrible Auto

message Property _Talent_BardLevel_Positive Auto

message Property _Talent_Decent_OK3 Auto

bardsongsscript Property BardSongs Auto

scene Property _talent_LetsPlayTogether2 Auto

quest Property MS05 Auto

actor Property PlayerRef Auto

referencealias Property Bard Auto

message Property _Talent_Decent_OK2 Auto

quest Property _talent_BardAudienceQuest Auto

message Property _Talent_Decent_OK Auto

message Property _Message_Standing Auto

globalvariable Property Bard_A_Glob Auto

globalvariable Property ExpertiseGlobal Auto

spell Property Instrumentspell Auto

musictype Property _Talent_Silence Auto

message Property _Talent_Clueless_OK1 Auto

message Property _Talent_Beginner_OK Auto

message Property _Talent_Clueless_OK3 Auto

spell Property MarriageRested Auto

referencealias Property Buddy Auto

scene Property _talent_BardAudienceQuestScene Auto

sound Property BeginnerSongs Auto

scene Property _talent_LetsPlayTogether1 Auto

message Property _Talent_Clueless_OK Auto

globalvariable Property _Talent_EnableMovement Auto

idle Property IdleToPlay Auto

sound Property ProSongs Auto

quest Property CollegeRecover Auto

message Property _Talent_Clueless_Broken2 Auto

message Property _Talent_Pro_OK1 Auto

message Property _Talent_Pro_OK Auto

message Property _Talent_Clueless_OK7 Auto

globalvariable Property _Talent_IsPerformingGood Auto

keyword Property LocTypeInn Auto

message Property _Talent_Clueless_Broken3 Auto

message Property _Talent_BardLevel_OK Auto

globalvariable Property _Talent_DummyForALLGUD Auto

message Property _Talent_Clueless_OK5 Auto

message Property _Talent_Clueless_OK2 Auto

light Property Torch01 Auto

sound Property CluelessSongs Auto

message Property _Talent_Beginner_OK1 Auto

message Property _Talent_Clueless_OK6 Auto

miscobject Property DummyInstrument Auto

globalvariable Property _Talent_FollowerPlays Auto

spell Property Rested Auto

miscobject Property Instrument Auto

sound Property DuoSongs_1 Auto

message Property _Talent_Pro_Positive Auto

sound Property BardLevelSongs Auto

sound Property HalfDecentSongs Auto

message Property _Talent_Clueless_Negative Auto

message Property _Talent_Clueless_Broken Auto

message Property _Talent_Beginner_Negative Auto

sound Property OBJCWBarricadeDestroyed Auto

message Property _Talent_Clueless_OK8 Auto

message Property _Talent_BardLevel_OK1 Auto

spell Property WellRested Auto

message Property _Talent_BardLevel_OK2 Auto

message Property _Talent_Pro_OK2 Auto

Event OnEffectStart(actor akTarget, actor akCaster)
    if !Bard_A_Glob && game.IsPluginInstalled("SkyrimsGotTalent_AnimAddon.esp")
        Bard_A_Glob = (game.GetFormFromFile(2048, "SkyrimsGotTalent_AnimAddon.esp") as globalvariable)
    endif
    ; --- ARR: consume any forced song the picker handed us (do this BEFORE any early return so
    ; a dropped cast can never leave the flag stuck and hijack the next normal activation) ---
    bForcedThisCast = false
    bForcedVoiceThisCast = false
    if BabBard && BabBard.ARR_ForcedActive
        bForcedThisCast = true
        bForcedVoiceThisCast = BabBard.ARR_ForcedIsVoice
        ForcedSongThisCast = BabBard.ARR_ForcedSound
        ForcedLengthThisCast = BabBard.ARR_ForcedLength
        ForcedVersesThisCast = BabBard.ARR_ForcedVerses
        ForcedVerseCountThisCast = BabBard.ARR_ForcedVerseCount
        BabBard.ARR_ForcedActive = false
    endif
    ; ---
    ; fresh per-cast song handle so the picker-gate / early-return OnEffectFinish never tries to
    ; Sound.StopInstance a stale instance id left over from a previous performance.
    SongToPlay = 0
    if PlayerRef.IsSwimming() == true || !(PlayerRef.GetSitState() == 0) && !PlayerRef.GetAnimationVariableBool("bGPMAInstalled")
        game.GetPlayer().RemoveSpell(Instrumentspell)
        _Message_Standing.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        return
    endif
    if ui.IsMenuOpen("FavoritesMenu")
        ui.InvokeString("HUD Menu", "_global.skse.CloseMenu", "FavoritesMenu")
    elseif ui.IsMenuOpen("InventoryMenu")
        game.DisablePlayerControls(true, true, false, false, false, true, true, false, 0)
        utility.Wait(0.1)
        game.EnablePlayerControls(true, true, true, true, true, true, true, true, 0)
    endif
    ; --- ARR Bards Reborn Tweaks play-mode select (skipped when a song is forced - the picker
    ; already chose, and re-running this would recurse straight back into the picker).
    ; Derive which instrument THIS effect copy is for - each instrument's MGEF binds ExpertiseGlobal
    ; to that instrument's mastery global - and hand it to the picker so it filters songs to it. ---
    int actInst = 0
    if ExpertiseGlobal == TalentDrum
        actInst = 1
    elseif ExpertiseGlobal == TalentFlute
        actInst = 2
    elseif ExpertiseGlobal == TalentLute
        actInst = 3
    endif
    if BabBard
        BabBard.ARR_PickerInstrument = actInst
    endif
    if !bForcedThisCast && BabBard
        ; mastered (>=100) -> the full-library picker (includes the basic per-instrument books);
        ; below 100 -> the learned picker, but ONLY if the player has explicitly learned a songbook
        ; with a song for this instrument (carrying an instrument alone must NOT pre-empt SgT's
        ; low-skill random play). Either picker filters its song list to actInst.
        if ExpertiseGlobal.GetValue() >= 100.0
            if BabBard.KnowsSongbookForInstrument(actInst, true)
                game.GetPlayer().RemoveSpell(Instrumentspell)
                SongbookAbility.Cast(PlayerRef)
                return
            endif
        elseif BabBard.KnowsSongbookForInstrument(actInst, false)
            game.GetPlayer().RemoveSpell(Instrumentspell)
            BabBard.OpenKnownSongMenu()
            return
        endif
    endif
    ; ---
    ; forced (picker-chosen) songs are menu-invoked and have a defined length/verse count, so we
    ; don't arm SgT's hold-Activate-to-play / camera-toggle controls for them - that avoids the
    ; menu's own Activate-release instantly stopping the song. SgT random play keeps them.
    if !bForcedThisCast
        RegisterForControl("Activate")
        RegisterForControl("Jump")
        ; FPI update: register the player's actual Toggle-POV keybind for the first<->third-person
        ; toggle, falling back to 33/273 only when the action is unmapped on both devices.
        iPOVKey = input.GetMappedKey("Toggle POV", 0)
        iPOVControllerKey = input.GetMappedKey("Toggle POV", 2)
        if iPOVKey <= 0 && iPOVControllerKey <= 0
            RegisterForKey(33)
            RegisterForKey(273)
        else
            if iPOVKey > 0
                RegisterForKey(iPOVKey)
            endif
            if iPOVControllerKey > 0
                RegisterForKey(iPOVControllerKey)
            endif
        endif
    endif
    _Talent_IsPerformingTerrible.SetValue(0.0)
    _Talent_IsPerformingGood.SetValue(0.0)
    _Talent_ReceiveOvation.SetValue(0.0)
    if _Talent_DummyForALLGUD.GetValue() == 1.0
        _Talent_DummyForALLGUD.SetValue(0.0)
        ALLGUD_Was_On = true
    endif
    if _Talent_EnableMovement.GetValue() == 1.0
        game.DisablePlayerControls(false, true, false, false, false, false, true, false, 0)
        PlayerRef.AddItem(DummyInstrument, 1, true)
    elseif !(PlayerRef.GetSitState() == 0)
        game.DisablePlayerControls(false, true, false, false, false, false, true, false, 0)
    else
        game.DisablePlayerControls(true, true, false, false, false, false, true, false, 0)
    endif
    PlayerRef.UnequipItemSlot(39)
    if skse.GetVersion()
        light playerTorch = (PlayerRef.GetEquippedObject(0) as light)
        if playerTorch
            PlayerRef.UnequipItemEx(playerTorch, 0, false)
        endif
    elseif PlayerRef.GetEquippedItemType(0) == 11
        PlayerRef.UnequipItem(Torch01, false, false)
    endif
    if PlayerRef.IsWeaponDrawn()
        PlayerRef.SheatheWeapon()
        utility.Wait(2.0)
    endif
    _Talent_Silence.Add()
    ; GUARD: GetCurrentLocation() is None outdoors / in unkeyworded cells; calling HasKeyword on it
    ; threw "no native object" and ABORTED the whole OnEffectStart (no song, no reaction, no EXP).
    location curLoc = PlayerRef.GetCurrentLocation()
    if curLoc && curLoc.HasKeyword(LocTypeInn)
        BardSongs.StopAllSongs()
    endif
    if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1
        if (game.GetFormFromFile(2099, "FirstPersonInteractions.esp") as globalvariable).GetValue() == 0.0
            game.ForceThirdPerson()
            returntofirstperson = true
        endif
    endif
    utility.Wait(0.1)
    if bForcedVoiceThisCast
        PlayVoicedPerformance()
    else
        PlayMusic()
        if bForcedThisCast
            ; a picker hands a curated song length; floor it so a mis-authored 0/short length can't
            ; fire OnUpdate almost immediately and produce a zero-length performance.
            float upd = ForcedLengthThisCast as float
            if upd < 5.0
                upd = 32.8
            endif
            RegisterForSingleUpdate(upd)
        else
            RegisterForSingleUpdate(32.8)
        endif
    endif
EndEvent

Function PlayMusic()
    utility.Wait(0.1)
    if PlayerRef.GetSitState() == 0 && _Talent_EnableMovement.GetValue() == 0.0
        PlayerRef.PlayIdle(IdleToPlay)
    else
        debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
    endif
    truedirectionalmovement.ToggleDisableHeadtracking("False", true)
    utility.Wait(0.9)
    ; --- ARR: a picker-chosen instrumental song plays THAT sound for its stored length; the
    ; reaction/EXP (MessageAndEXP at OnUpdate) and OnEffectFinish cleanup run unchanged. ---
    if bForcedThisCast
        if ForcedSongThisCast
            SongToPlay = ForcedSongThisCast.Play(PlayerRef)
        endif
        ; a picker/forced song reacts to the player's ACTUAL skill (booed when low, praised when
        ; high) just like busking, instead of always being treated as a good performance - this is
        ; what lets the boo scene fire for a low-skill picker play (#3).
        SetPerformanceTierFromSkill()
        _talent_BardAudienceQuest.SetStage(10)
        return
    endif
    ; ---
    float Expertise = ExpertiseGlobal.GetValue()
    if Expertise < 26.0
        SongToPlay = CluelessSongs.Play(PlayerRef)
        PlayerRef.SetExpressionOverride(3, 75)
        utility.Wait(2.0)
        _Talent_IsPerformingTerrible.SetValue(1.0)
        _talent_BardAudienceQuest.SetStage(10)
    elseif Expertise < 46.0
        SongToPlay = BeginnerSongs.Play(PlayerRef)
        PlayerRef.SetExpressionOverride(4, 60)
        utility.Wait(2.0)
        _Talent_IsPerformingTerrible.SetValue(1.0)
        _talent_BardAudienceQuest.SetStage(10)
    elseif Expertise < 66.0
        SongToPlay = HalfDecentSongs.Play(PlayerRef)
        PlayerRef.SetExpressionOverride(2, 50)
        utility.Wait(2.0)
        _Talent_IsPerformingGood.SetValue(2.0)
    elseif Expertise < 86.0
        _Talent_IsPerformingGood.SetValue(1.0)
        _talent_BardAudienceQuest.SetStage(10)
        PlayerRef.SetExpressionOverride(2, 60)
        if _Talent_FollowerPlays.GetValue() == 0.0
            SongToPlay = BardLevelSongs.Play(PlayerRef)
        elseif _Talent_FollowerPlays.GetValue() == 1.0
            SongToPlay = DuoSongs_1.Play(PlayerRef)
        else
            SongToPlay = DuoSongs_2.Play(PlayerRef)
        endif
        _Talent_FollowerPlays.SetValue(0.0)
    else
        _Talent_IsPerformingGood.SetValue(1.0)
        PlayerRef.SetExpressionOverride(2, 70)
        _talent_BardAudienceQuest.SetStage(10)
        int RandomNum = utility.RandomInt(1, 4)
        if _Talent_FollowerPlays.GetValue() == 0.0
            if RandomNum == 1
                SongToPlay = BardLevelSongs.Play(PlayerRef)
            else
                SongToPlay = ProSongs.Play(PlayerRef)
            endif
        elseif _Talent_FollowerPlays.GetValue() == 1.0
            SongToPlay = DuoSongs_1.Play(PlayerRef)
        else
            SongToPlay = DuoSongs_2.Play(PlayerRef)
        endif
        _Talent_FollowerPlays.SetValue(0.0)
    endif
EndFunction

Function PlayVoicedPerformance()
    ; --- ARR: a picker-chosen VOICED song (e.g. a Songs-of-Skyrim verse list) played through
    ; SgT's shell. We reuse the same movement/anim/first-person setup OnEffectStart already did,
    ; then sing the verses sequentially (PlayAndWait blocks, so this drives its own completion
    ; instead of RegisterForSingleUpdate), then run the reaction/EXP and end the effect. ---
    utility.Wait(0.1)
    if PlayerRef.GetSitState() == 0 && _Talent_EnableMovement.GetValue() == 0.0
        PlayerRef.PlayIdle(IdleToPlay)
    else
        debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
    endif
    truedirectionalmovement.ToggleDisableHeadtracking("False", true)
    utility.Wait(0.9)
    SetPerformanceTierFromSkill()
    _talent_BardAudienceQuest.SetStage(10)
    int i = 0
    while i < ForcedVerseCountThisCast
        if ForcedVersesThisCast
            sound verse = (ForcedVersesThisCast.GetAt(i) as sound)
            if verse
                verse.PlayAndWait(PlayerRef)
            endif
        endif
        i = i + 1
    endwhile
    ; post-song reaction + EXP + skill bridge + gig trip (same hook the instrumental path uses),
    ; then drop the spell to fire OnEffectFinish for the standard cleanup.
    MessageAndEXP()
    EndPerformanceCleanup()
    game.GetPlayer().RemoveSpell(Instrumentspell)
EndFunction

; --- ARR Bards Reborn Tweaks (section B): audience-reaction trigger -------------------------------
; The audience reaction fires with a BARE _talent_BardAudienceQuest.SetStage(10), exactly as SgT and
; FPI do it (inline in PlayMusic / PlayVoicedPerformance). We deliberately do NOT Stop()/Start() the
; audience quest: force-starting 00AFE0 fills its Bystander1-5 reference aliases with the nearby
; humans and runs the audience SCENE over them, which reserves those exact NPCs away from the
; Start-Game-Enabled comment quests (_Talent_DuringPerformanceComments 0089B4 / ...Positive 009FAE)
; so they never speak the ambient critique/praise. Leaving 00AFE0's lifecycle alone (SgT's design)
; is what keeps the nearby NPCs free to comment - the cause of the "no spoken reactions" regression.

; Set the performance-tier globals from the player's ACTUAL instrument skill, mirroring the random
; play tiers (skill < 46 reads as a poor performance -> boo scene; otherwise good -> praise scene).
; Used by the forced/picker instrumental and voiced paths so a deliberately-played song is judged on
; skill instead of always counting as "good" (the cause of "no boos at low skill" for picker plays).
Function SetPerformanceTierFromSkill()
    if ExpertiseGlobal.GetValue() < 46.0
        _Talent_IsPerformingTerrible.SetValue(1.0)
        _Talent_IsPerformingGood.SetValue(0.0)
        PlayerRef.SetExpressionOverride(4, 60)
    else
        _Talent_IsPerformingTerrible.SetValue(0.0)
        _Talent_IsPerformingGood.SetValue(1.0)
        PlayerRef.SetExpressionOverride(2, 60)
    endif
EndFunction

; --- ARR Bards Reborn Tweaks: end-of-performance teardown ----------------------------------------
; Self-relative input registrations (Update/Control/Key) MUST be cleared while the effect is still
; BOUND - i.e. BEFORE the self-RemoveSpell that ends a performance. Calling this from OnUpdate /
; OnControlUp / PlayVoicedPerformance just before RemoveSpell, instead of leaving the Unregister
; calls in the now-UNBOUND OnEffectFinish, is what stops the per-performance "no native object
; bound" errors SgT's self-dispel pattern logged. The engine also drops these on effect end, so
; OnEffectFinish no longer repeats them.
Function EndPerformanceCleanup()
    UnregisterForUpdate()
    UnregisterForControl("Activate")
    UnregisterForControl("Jump")
    ; FPI update: drop the player's mapped Toggle-POV keybind(s); the 33/273 unregister covers the
    ; unmapped-fallback case. UnregisterForKey on a key that was never registered is a no-op.
    if iPOVKey > 0
        UnregisterForKey(iPOVKey)
    endif
    if iPOVControllerKey > 0
        UnregisterForKey(iPOVControllerKey)
    endif
    UnregisterForKey(33)
    UnregisterForKey(273)
EndFunction

Event OnControlUp(string control, float HoldTime)
    if control == "Activate" || control == "Jump"
        EndPerformanceCleanup()
        PlayerRef.RemoveSpell(Instrumentspell)
        _talent_LetsPlayTogether1.Stop()
        _talent_LetsPlayTogether2.Stop()
        PlayerRef.RemoveItem(DummyInstrument, 1, true)
        if Buddy.GetActorReference() == None
        else
            Buddy.GetActorReference().ClearLookAt()
        endif
    endif
EndEvent

Event OnKeyDown(int KeyCode)
    ; FPI update: the Toggle-POV keys are the only keys this effect registers, so any OnKeyDown is a
    ; first<->third-person toggle. (The old "if KeyCode == 33 || 273" guard would reject a custom
    ; Toggle-POV bind now that we register the player's actual keybind.)
    if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1
        PlayerRef.PlayIdle(IdleStop_Loose)
        debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
        utility.Wait(0.1)
        game.ForceThirdPerson()
        debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
    elseif PlayerRef.GetAnimationVariableInt("i1stPerson") == 0
        PlayerRef.PlayIdle(IdleStop_Loose)
        debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
        utility.Wait(0.1)
        game.ForceFirstPerson()
        utility.Wait(0.1)
        debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
    endif
EndEvent

Event OnUpdate()
    EndPerformanceCleanup()
    game.GetPlayer().RemoveSpell(Instrumentspell)
    MessageAndEXP()
EndEvent

Event OnEffectFinish(actor akTarget, actor akCaster)
    _Talent_IsPerformingTerrible.SetValue(0.0)
    _Talent_IsPerformingGood.SetValue(0.0)
    truedirectionalmovement.ToggleDisableHeadtracking("False", false)
    PlayerRef.RemoveItem(DummyInstrument, 1, true)
    if ALLGUD_Was_On == true
        _Talent_DummyForALLGUD.SetValue(1.0)
        ALLGUD_Was_On = false
    endif
    ; NOTE: this runs on the now-UNBOUND effect (every end path self-RemoveSpell's the instrument
    ; spell, which dispels THIS effect). Self-relative natives (UnregisterForUpdate/Control/Key)
    ; would throw "no native object bound" here, so that teardown moved to EndPerformanceCleanup()
    ; which runs BEFORE the RemoveSpell while the effect is still bound. Everything below is
    ; PlayerRef / global / quest / Sound-global work, which runs safely on an unbound effect.
    if _talent_BardAudienceQuest && _talent_BardAudienceQuest.GetStage() == 10
        _talent_BardAudienceQuest.SetStage(20)
    endif
    PlayerRef.ClearExpressionOverride()
    PlayerRef.PlayIdle(IdleStop_Loose)
    debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
    utility.Wait(0.3)
    if SongToPlay
        sound.StopInstance(SongToPlay)
        SongToPlay = 0
    endif
    game.EnablePlayerControls(true, true, true, true, true, true, true, true, 0)
    _Talent_Silence.Remove()
    if returntofirstperson == true
        utility.Wait(2.5)
        if skse.GetPluginVersion("ImprovedCameraSE") < 0
            game.ForceFirstPerson()
        endif
        returntofirstperson = false
    endif
    utility.Wait(4.5)
    if _talent_BardAudienceQuest && _talent_BardAudienceQuest.GetStage() == 20
        _talent_BardAudienceQuest.SetStage(200)
    endif
    _Talent_IsPerformingTerrible.SetValue(0.0)
    _Talent_IsPerformingGood.SetValue(0.0)
EndEvent

Function MessageAndEXP()
    int randomglobterrible = utility.RandomInt(1, 3)
    int randomglobmedium = utility.RandomInt(4, 6)
    int randomglobgreat = utility.RandomInt(7, 9)
    float Expertise = ExpertiseGlobal.GetValue()
    int RandomNum = utility.RandomInt(1, 14)
    _Talent_ReceiveOvation.SetValue(1.0)
    if Expertise < 26.0
        utility.Wait(1.4)
        if Bard_A_Glob
            Bard_A_Glob.SetValue(randomglobterrible)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
            utility.Wait(2.2)
            Bard_A_Glob.SetValue(0.0)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
        endif
        SpecialInstrument = CollegeRecover.GetStage()
        if RandomNum == 1 && !(SpecialInstrument == 40) && !(SpecialInstrument == 15)
            int MessageRandom = utility.RandomInt(1, 4)
            if MessageRandom == 1
                _Talent_Clueless_Broken.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            elseif MessageRandom == 2
                _Talent_Clueless_Broken2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            elseif MessageRandom == 3
                _Talent_Clueless_Broken1.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            else
                _Talent_Clueless_Broken3.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            endif
            Broken = OBJCWBarricadeDestroyed.Play(PlayerRef)
            PlayerRef.RemoveItem(Instrument, 1, false)
        elseif RandomNum > 1 && RandomNum < 6
            _Talent_Clueless_Negative.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 6
            _Talent_Clueless_OK.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 7
            _Talent_Clueless_OK1.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 8
            _Talent_Clueless_OK2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 9
            _Talent_Clueless_OK3.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 10
            _Talent_Clueless_OK4.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 11
            _Talent_Clueless_OK5.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 12
            _Talent_Clueless_OK6.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum == 13
            _Talent_Clueless_OK7.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            _Talent_Clueless_OK8.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
    elseif Expertise < 46.0
        utility.Wait(1.4)
        if Bard_A_Glob
            Bard_A_Glob.SetValue(randomglobterrible)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
            utility.Wait(2.2)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
            Bard_A_Glob.SetValue(0.0)
        endif
        if RandomNum < 8
            _Talent_Beginner_Negative.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum < 10
            _Talent_Beginner_OK.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            _Talent_Beginner_OK1.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
    elseif Expertise < 66.0
        utility.Wait(1.4)
        if Bard_A_Glob
            Bard_A_Glob.SetValue(randomglobmedium)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
            utility.Wait(2.2)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
            Bard_A_Glob.SetValue(0.0)
        endif
        if RandomNum < 4
            _Talent_Decent_OK.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum < 8
            _Talent_Decent_OK2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            _Talent_Decent_OK3.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
    elseif Expertise < 86.0
        utility.Wait(1.4)
        if Bard_A_Glob
            Bard_A_Glob.SetValue(randomglobgreat)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
            utility.Wait(2.2)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
            Bard_A_Glob.SetValue(0.0)
        endif
        if RandomNum < 7
            _Talent_BardLevel_Positive.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum < 9
            _Talent_BardLevel_OK.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum < 12
            _Talent_BardLevel_OK2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            _Talent_BardLevel_OK1.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
    else
        utility.Wait(1.4)
        if Bard_A_Glob
            Bard_A_Glob.SetValue(randomglobgreat)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMA")
            utility.Wait(2.2)
            debug.SendAnimationEvent(PlayerRef, "OffsetGPMAStop")
            Bard_A_Glob.SetValue(0.0)
        endif
        if RandomNum < 7
            _Talent_Pro_Positive.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum < 9
            _Talent_Pro_OK1.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum < 11
            _Talent_Pro_OK2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elseif RandomNum < 13
            _Talent_Pro_OK3.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        else
            _Talent_Pro_OK.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        endif
    endif
    int Exp = utility.RandomInt(1, 3)
    float Speech = PlayerRef.GetActorValue("Speechcraft")
    if Speech > 24.0 && Speech < 51.0
        Exp = Exp + 1
    elseif Speech > 50.0 && Speech < 75.0
        Exp = Exp + 2
    elseif Speech > 74.0
        Exp = Exp + 3
    endif
    if MS05.GetStage() == 300
        Exp = Exp + 2
    endif
    if PlayerRef.HasSpell(Rested) || PlayerRef.HasSpell(WellRested) || PlayerRef.HasSpell(MarriageRested)
        Exp = Exp + 2
    endif
    if Exp < 1
        Exp = 0
    endif
    ExpertiseGlobal.SetValue(ExpertiseGlobal.GetValue() + Exp)
    if ExpertiseGlobal.GetValue() > 100.0
        ExpertiseGlobal.SetValue(100.0)
    endif
    ; --- ARR Bards Reborn Tweaks: mirror BaB _LP_BardSkill = best instrument; fire BaB gig economy ---
    int best = (TalentDrum.GetValue() as int)
    if (TalentLute.GetValue() as int) > best
        best = (TalentLute.GetValue() as int)
    endif
    if (TalentFlute.GetValue() as int) > best
        best = (TalentFlute.GetValue() as int)
    endif
    if best > 100
        best = 100
    endif
    LPBardSkill.SetValue(best)
    ; ARR: gigs award NOTHING below Bard Skill 26 (best instrument >= 26) - don't advance the
    ; tavern/jarl gig to payout until the player has real skill (no gold/jarl/renown from sub-26 play).
    if best >= 26
        if TavernQuest.GetStage() == 10
            TavernQuest.SetStage(100)
        endif
        if JarlQuest.GetStage() == 10
            JarlQuest.SetStage(100)
        endif
    endif
EndFunction
