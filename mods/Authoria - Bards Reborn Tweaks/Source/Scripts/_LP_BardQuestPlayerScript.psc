ScriptName _LP_BardQuestPlayerScript extends ReferenceAlias
; ARR - Bards Reborn Tweaks integration overrides:
;  D1  drop BaB's play-power / songbook-power grants (SgT activate-to-play wins); keep populating
;      _LP_BardKnownSongbooks from instruments so the max-level picker still has content.
;  D4  RewardPlayer no longer touches Speechcraft (Bardic Speech owns it) and mirrors the skill
;      via the bridge instead of +1.
;  D5  BaB's own audience quest is replaced by SgT's reaction layer (so even max-level picker
;      performances drive SgT NPC reactions + the player self-reaction anim).
;  D8  BaB's automatic follower second-part (duet) is removed; only SgT's dialogue duet remains.
;  D9  OpenKnownSongMenu() = the play-a-song-you-know menu, invoked by the MCM-configurable
;      hotkey (registered on the BaB config quest, which calls this).
;  Bridge: _LP_BardSkill = Max(_Talent_Drum/Lute/Flute) so BR exams, Spellsong crafting,
;      perks and the spy quest keep working off the best instrument.

float SongEndTime
float SongStartTime
int FrostfallAnimationSetting
int InstrumentA
int SongWasStopped
int SoundREF
int CameraState
armor Shield
armor Lute

globalvariable Property _LP_BardAudienceHostile Auto

globalvariable Property _LP_BardHasSKSE Auto

globalvariable Property _LP_BardSongSons Auto

idle Property IdleLuteStart Auto

book Property _LP_BardSongbookLute Auto

armor Property _LP_BardLuteArmor Auto

globalvariable Property _LP_BardFactionAggression Auto

formlist Property _LP_BardDrums Auto

formlist Property _LP_BardSongsSons Auto

formlist Property _LP_BardSongsImperial Auto

idle Property IdleFluteStart Auto

quest Property _LP_BardTavernQuest Auto

globalvariable Property _LP_BardHasFrostfall Auto

spell Property _LP_BardExperiencedAbility Auto

quest Property _LP_BardSpyHandlerQuest Auto

bardsongsscript Property BardSongs Auto

formlist Property _LP_BardInstruments Auto

spell Property _LP_BardWellKnownAbility Auto

actor Property PlayerREF Auto

ReferenceAlias Property Journal Auto

globalvariable Property _LP_BardCustomFit Auto

book Property _LP_BardSongbookFlute Auto

idle Property IdleDrumStart Auto

quest Property _LP_BardJarlQuest Auto

globalvariable Property _LP_BardIsPlaying Auto

spell Property _LP_BardRenownedAbility Auto

idle Property IdleSilentBow Auto

soundcategory Property AudioCategoryMUS Auto

formlist Property _LP_BardLutes Auto

quest Property _LP_BardJournalQuest Auto

book Property _LP_BardSongbookDrum Auto

globalvariable Property _LP_BardSongImperial Auto

formlist Property _LP_BardKnownSongbooks Auto

globalvariable Property _LP_BardKeepJournal Auto

globalvariable Property _LP_BardSkill Auto

idle Property IdleStop_Loose Auto

formlist Property _LP_BardFlutes Auto

; --- ARR Bards Reborn Tweaks additions ---
globalvariable Property _Talent_Drum Auto
globalvariable Property _Talent_Lute Auto
globalvariable Property _Talent_Flute Auto
globalvariable Property _Talent_IsPerformingGood Auto
globalvariable Property _Talent_IsPerformingTerrible Auto
globalvariable Property _Talent_ReceiveOvation Auto
globalvariable Property Bard_A_Glob Auto
quest Property _talent_BardAudienceQuest Auto
formlist Property Auth_LearnedSongbooks Auto
formlist Property _LP_BardSongsofSkyrimFemale Auto
formlist Property _LP_BardSongsofSkyrimMale Auto
book Property _LP_BardSongbookSkyrim Auto
book Property _LP_BardSongbookSkyrimRevised Auto
; quick-play hotkey: the SgT instrument spells (adding one fires that instrument's play effect)
spell Property _Talent_DrumSpell Auto
spell Property _Talent_FluteSpell Auto
spell Property _Talent_LuteSpell Auto
; forced-song handoff to SgT's shell: a picker stashes the chosen song here, then fires the
; instrument's SgT spell; _talent_playinstrument reads these off this (persistent) alias.
sound Property ARR_ForcedSound Auto Hidden
int Property ARR_ForcedLength Auto Hidden
int Property ARR_ForcedInstrument Auto Hidden
formlist Property ARR_ForcedVerses Auto Hidden
int Property ARR_ForcedVerseCount Auto Hidden
bool Property ARR_ForcedIsVoice Auto Hidden
bool Property ARR_ForcedActive Auto Hidden
; the instrument the player activated to OPEN a picker (1=Drum/2=Flute/3=Lute, 0=unknown/show-all).
; set by _talent_playinstrument.OnEffectStart before the picker fires; read by OpenSongPicker and
; the max-level UIE picker so both filter songs to the activated instrument.
int Property ARR_PickerInstrument Auto Hidden
; ---

Event OnInit()
    AddInventoryEventFilter(_LP_BardInstruments)
EndEvent

Event OnUpdate()
    if (_LP_BardAudienceHostile.GetValue() as int) > 0 || SongWasStopped
        _LP_BardAudienceHostile.SetValue(0)
        StopPlaying(false)
    elseif utility.GetCurrentRealTime() >= SongEndTime
        StopPlaying(true)
    else
        RegisterForSingleUpdate(0.5)
    endif
EndEvent

Event OnKeyDown(int KeyCode)
    if KeyCode == 44 || KeyCode == 275
        StopSong()
    endif
EndEvent

Function StopSong()
    if utility.GetCurrentRealTime() - SongStartTime > 2
        SongWasStopped = 1
        UnRegisterForAllKeys()
    endif
EndFunction

Function Sing(formlist Verse, int nVerses, int A, int B)
    if HasInstrument(A) == false
        debug.Notification("You don't have the right instrument.")
        StopPlaying(false)
        return
    endif
    InstrumentA = A
    if (_LP_BardFactionAggression.GetValue() as int) == 1
        if _LP_BardSongsImperial.Find((Verse.GetAt(0) as sound)) >= 0
            _LP_BardSongImperial.SetValue(1)
        elseif _LP_BardSongsSons.Find((Verse.GetAt(0) as sound)) >= 0
            _LP_BardSongSons.SetValue(1)
        endif
    endif
    StartPlaying()
    SongWasStopped = 0
    int i = 0
    while i < nVerses
        if !SongWasStopped
            (Verse.GetAt(i) as sound).PlayAndWait(PlayerREF)
        endif
        i = i + 1
    endwhile
    StopPlaying(!SongWasStopped)
EndFunction

Function Play(sound Song, float SoundLength, int A, int B)
    if PlayerREF.IsInCombat() == true
        debug.Notification("You cannot use this musical ability in combat")
    else
        if HasInstrument(A) == false
            debug.Notification("You don't have the right instrument.")
            StopPlaying(false)
            return
        endif
        InstrumentA = A
        if (_LP_BardFactionAggression.GetValue() as int) == 1
            if _LP_BardSongsImperial.Find(Song) >= 0
                _LP_BardSongImperial.SetValue(1)
            elseif _LP_BardSongsSons.Find(Song) >= 0
                _LP_BardSongSons.SetValue(1)
            endif
        endif
        StartPlaying()
        SoundREF = Song.Play(PlayerREF)
        if !SoundREF
            debug.Notification("You don't know that song")
            StopPlaying(false)
        else
            SongWasStopped = 0
            SongEndTime = utility.GetCurrentRealTime() + SoundLength
            RegisterForSingleUpdate(0.5)
        endif
    endif
EndFunction

bool Function StandStill()
    if PlayerREF.IsInCombat() == true
        debug.Notification("You cannot use this musical ability in combat")
        return false
    else
        _LP_BardIsPlaying.SetValue(1)
        CameraState = game.GetCameraState()
        game.ForceThirdPerson()
        game.SetInChargen(true, false, false)
        if PlayerREF.IsWeaponDrawn()
            if _LP_BardHasSKSE
                PlayerREF.SheatheWeapon()
            else
                game.DisablePlayerControls(true, true, false, false, false, true, true, false, 0)
                game.EnablePlayerControls(true, true, true, true, true, true, true, true, 0)
            endif
            utility.Wait(2.0)
        endif
        if _LP_BardHasSKSE
            game.DisablePlayerControls(true, true, true, false, true, true, true, true, 0)
            RegisterForKey(44)
            RegisterForKey(275)
        endif
        if (_LP_BardHasFrostfall.GetValue() as int) == 1
            FrostfallAnimationSetting = ((game.GetFormFromFile(33854056, "Chesko_Frostfall.esp") as globalvariable).GetValue() as int)
            (game.GetFormFromFile(33854056, "Chesko_Frostfall.esp") as globalvariable).SetValue(1)
        endif
        return true
    endif
EndFunction

Function CancelMenu()
    if (_LP_BardHasFrostfall.GetValue() as int) == 1
        (game.GetFormFromFile(33854056, "Chesko_Frostfall.esp") as globalvariable).SetValue(FrostfallAnimationSetting)
    endif
    game.SetInChargen(false, false, false)
    if _LP_BardHasSKSE
        game.EnablePlayerControls(true, true, true, true, true, true, true, true, 0)
        ; drop the stop-keys StandStill registered, so a cancelled/empty picker (which skips the
        ; PlayThroughSgT/SingThroughSgT unregister) doesn't leave 44/275 hooked on this persistent alias.
        UnregisterForKey(44)
        UnregisterForKey(275)
    endif
    if CameraState == 0
        game.ForceFirstPerson()
    endif
    _LP_BardIsPlaying.SetValue(0)
EndFunction

Function StartPlaying()
    UnequipShield()
    BardSongs.StopAllSongs()
    SongStartTime = utility.GetCurrentRealTime()
    if InstrumentA == 1
        PlayerREF.PlayIdle(IdleDrumStart)
    elseif InstrumentA == 2
        PlayerREF.PlayIdle(IdleFluteStart)
    elseif InstrumentA == 3
        UnequipLute()
        PlayerREF.PlayIdle(IdleLuteStart)
    endif
    AudioCategoryMUS.Mute()
    ; SgT audience reactions (replaces BaB's applause quest) - a picker performance is "good".
    ; Match SgT/FPI exactly: a BARE SetStage(10). Never Stop()/Start() the audience quest - force-
    ; starting 00AFE0 fills its Bystander1-5 aliases with the nearby humans and runs the scene over
    ; them, starving the SGE comment quests so no spoken critique/praise plays. Leaving its lifecycle
    ; alone keeps the nearby NPCs free to comment.
    _Talent_IsPerformingTerrible.SetValue(0)
    _Talent_IsPerformingGood.SetValue(1)
    _Talent_ReceiveOvation.SetValue(0)
    _talent_BardAudienceQuest.SetStage(10)
EndFunction

Function StopPlaying(bool SongFinished)
    PlayerREF.PlayIdle(IdleStop_Loose)
    _LP_BardSongImperial.SetValue(0)
    _LP_BardSongSons.SetValue(0)
    if (_LP_BardHasFrostfall.GetValue() as int) == 1
        (game.GetFormFromFile(33854056, "Chesko_Frostfall.esp") as globalvariable).SetValue(FrostfallAnimationSetting)
    endif
    game.SetInChargen(false, false, false)
    if _LP_BardHasSKSE
        game.EnablePlayerControls(true, true, true, true, true, true, true, true, 0)
        ; the BaB a-cappella play path (Sing/Play) ends here without CancelMenu, so unregister the
        ; StandStill stop-keys here too - covers normal completion and interrupted plays alike.
        UnregisterForKey(44)
        UnregisterForKey(275)
    endif
    EquipShield()
    EquipLute()
    if !SongFinished
        if SoundREF
            sound.StopInstance(SoundREF)
        endif
        utility.Wait(1.0)
    else
        ; SgT ovation + player self-reaction for a finished (max-level picker) performance
        _Talent_ReceiveOvation.SetValue(1)
        if _talent_BardAudienceQuest.GetStage() == 10
            _talent_BardAudienceQuest.SetStage(20)
        endif
        Bard_A_Glob.SetValue(utility.RandomInt(7, 9))
        debug.SendAnimationEvent(PlayerREF, "idlesilentbow")
        utility.Wait(2.2)
        debug.SendAnimationEvent(PlayerREF, "OffsetStop")
        Bard_A_Glob.SetValue(0)
        RewardPlayer()
        if _talent_BardAudienceQuest.GetStage() == 20
            _talent_BardAudienceQuest.SetStage(200)
        endif
    endif
    _Talent_IsPerformingGood.SetValue(0)
    _Talent_IsPerformingTerrible.SetValue(0)
    _talent_BardAudienceQuest.Stop()
    AudioCategoryMUS.UnMute()
    _LP_BardIsPlaying.SetValue(0)
    if CameraState == 0
        game.ForceFirstPerson()
    endif
EndFunction

Function RewardPlayer()
    ; train the instrument that was just played (picker performances train too, so skill keeps
    ; rising once the picker becomes the default; SgT's random play trains via its own MessageAndEXP)
    globalvariable trained = None
    if InstrumentA == 1
        trained = _Talent_Drum
    elseif InstrumentA == 2
        trained = _Talent_Flute
    elseif InstrumentA == 3
        trained = _Talent_Lute
    endif
    if trained
        int gain = utility.RandomInt(1, 3)
        float spd = PlayerREF.GetActorValue("Speechcraft")
        if spd > 24 && spd < 51
            gain = gain + 1
        elseif spd > 50 && spd < 75
            gain = gain + 2
        elseif spd > 74
            gain = gain + 3
        endif
        int nv = (trained.GetValue() as int) + gain
        if nv > 100
            nv = 100
        endif
        trained.SetValue(nv)
    endif
    ; bridge: mirror BaB _LP_BardSkill onto the best SgT instrument mastery (cap 100)
    int best = (_Talent_Drum.GetValue() as int)
    if (_Talent_Lute.GetValue() as int) > best
        best = (_Talent_Lute.GetValue() as int)
    endif
    if (_Talent_Flute.GetValue() as int) > best
        best = (_Talent_Flute.GetValue() as int)
    endif
    if best > 100
        best = 100
    endif
    _LP_BardSkill.SetValue(best)
    objectreference JournalREF = Journal.GetReference()
    quest JournalQuest = _LP_BardJournalQuest
    if JournalREF
        PlayerREF.RemoveItem(JournalREF, 1, 1)
    endif
    if _LP_BardSpyHandlerQuest.IsRunning() == 0 && _LP_BardSpyHandlerQuest.IsCompleted() == 0
        ; ARR: the bard-spy questline now needs Bard Skill >= 50 (was 25) - a fairer bar on the
        ; mirrored SgT mastery curve. Still also requires an earned renown ability (below).
        if (_LP_BardSkill.GetValue() as int) >= 50 && (PlayerREF.HasSpell(_LP_BardExperiencedAbility) || PlayerREF.HasSpell(_LP_BardWellKnownAbility) || PlayerREF.HasSpell(_LP_BardRenownedAbility))
            _LP_BardSpyHandlerQuest.Start()
        endif
    endif
    ; ARR: gigs award NOTHING below Bard Skill 26 (best instrument >= 26). Don't advance the
    ; tavern/jarl gig to its payout stage until the player has real skill - so no gold, no jarl
    ; reward, and no renown progress accrues from sub-26 performances.
    if best >= 26
        if _LP_BardTavernQuest.GetStage() == 10
            _LP_BardTavernQuest.SetStage(100)
            utility.Wait(1.0)
            PlayerREF.PlayIdle(IdleSilentBow)
        endif
        if _LP_BardJarlQuest.GetStage() == 10
            _LP_BardJarlQuest.SetStage(100)
            utility.Wait(1.0)
            PlayerREF.PlayIdle(IdleSilentBow)
        endif
    endif
    if (_LP_BardKeepJournal.GetValue() as int) > 0
        JournalQuest.Stop()
        JournalQuest.Start()
    endif
EndFunction

Function OpenKnownSongMenu()
    ; D9 / picker redesign - the sub-100 LEARNED picker: play a song from a songbook you have
    ; explicitly learned (regional/unique/custom - NOT the basic per-instrument books, which you'd
    ; have merely by carrying the instrument), filtered to the instrument you activated. Routes
    ; through the single OpenSongPicker; the max-level full picker calls it with instrument books on.
    OpenSongPicker(ARR_PickerInstrument, false)
EndFunction

; --- ARR Bards Reborn Tweaks: live songbook enumeration (section A redesign) ---------------------
; Both pickers source from ONE master pair-list: _LP_BardSongbooks (061A81) <-> _LP_BardSongbookSpells
; (061A80), which together list EVERY songbook (regional + unique + custom + the 3 instrument books)
; and its paired learn-spell, in lock-step index order. A songbook is "known" exactly the way the
; MCM Songbooks page decides its toggle: PlayerREF.HasSpell(spell) || _LP_BardKnownSongbooks.HasForm
; (book). That test is retroactive (works for books learned before this build), consolidate-mode-
; independent, and needs no separate Auth_LearnedSongbooks list. These base records are static forms
; in BecomeABard.esp (a master), so GetFormFromFile resolves them with no extra VMAD wiring - exactly
; like GetLearnedList() already does for the patch's own list.

formlist Function GetAllSongbooks()
    return (game.GetFormFromFile(0x00061A81, "BecomeABard.esp") as formlist)
EndFunction

formlist Function GetAllSongbookSpells()
    return (game.GetFormFromFile(0x00061A80, "BecomeABard.esp") as formlist)
EndFunction

book Function GetCustomSongbook()
    return (game.GetFormFromFile(0x00012852, "BecomeABard.esp") as book)
EndFunction

miscobject Function GetCustomTitle()
    return (game.GetFormFromFile(0x00061FEF, "BecomeABard.esp") as miscobject)
EndFunction

formlist Function GetCustomNames()
    return (game.GetFormFromFile(0x00061A8C, "BecomeABard.esp") as formlist)
EndFunction

formlist Function GetCustomLengths()
    return (game.GetFormFromFile(0x00060FAB, "BecomeABard.esp") as formlist)
EndFunction

formlist Function GetCustomInstrumentsA()
    return (game.GetFormFromFile(0x00060FAC, "BecomeABard.esp") as formlist)
EndFunction

formlist Function GetCustomInstrumentsB()
    return (game.GetFormFromFile(0x00060FAD, "BecomeABard.esp") as formlist)
EndFunction

; the primary instrument (InstrumentsA) of song #songIdx in songbook #bookIdx. Custom-songbook
; songs carry their instrument on the editable _LP_BardCustomSongbookInstrumentsA globals, every
; other songbook carries it on its own book script array.
int Function GetSongInstrument(formlist allBooks, book customBook, int bookIdx, int songIdx)
    book theBook = (allBooks.GetAt(bookIdx) as book)
    if theBook == customBook
        return ((GetCustomInstrumentsA().GetAt(songIdx) as globalvariable).GetValue() as int)
    endif
    return (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).InstrumentsA[songIdx]
EndFunction

; is songbook #bookIdx available to a picker right now? "Known" is decided exactly like the MCM
; Songbooks page: HasSpell(its learn-spell) || _LP_BardKnownSongbooks.HasForm(it). abIncludeInstrument
; Books gates the three BASIC per-instrument books (Drum/Flute/Lute): they are auto-added to
; _LP_BardKnownSongbooks merely by CARRYING the instrument, so the max-level full picker includes
; them (true) but the sub-100 LEARNED picker excludes them (false) - otherwise simply holding an
; instrument would replace SgT's low-skill random play with a picker.
bool Function IsBookAvailable(formlist allBooks, formlist allSpells, int bookIdx, bool abIncludeInstrumentBooks)
    book theBook = (allBooks.GetAt(bookIdx) as book)
    if !abIncludeInstrumentBooks && (theBook == _LP_BardSongbookDrum || theBook == _LP_BardSongbookFlute || theBook == _LP_BardSongbookLute)
        return false
    endif
    return PlayerREF.HasSpell((allSpells.GetAt(bookIdx) as spell)) || _LP_BardKnownSongbooks.HasForm(allBooks.GetAt(bookIdx))
EndFunction

; does the player have >=1 available songbook containing a song playable on aInstrument? Replaces the
; old "Auth_LearnedSongbooks non-empty" gate so a picker only opens when it will have content (and the
; activate falls through to SgT random play otherwise). aInstrument 0 = any; abIncludeInstrumentBooks
; per IsBookAvailable (true for the mastered full picker, false for the learned picker).
bool Function KnowsSongbookForInstrument(int aInstrument, bool abIncludeInstrumentBooks)
    formlist allBooks = GetAllSongbooks()
    formlist allSpells = GetAllSongbookSpells()
    book customBook = GetCustomSongbook()
    if allBooks == None || allSpells == None
        return false
    endif
    int NumBooks = allBooks.GetSize()
    int bookIdx = 0
    while bookIdx < NumBooks
        if IsBookAvailable(allBooks, allSpells, bookIdx, abIncludeInstrumentBooks)
            int NumSongs = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).Names.Length
            int s = 0
            while s < NumSongs
                if aInstrument == 0 || GetSongInstrument(allBooks, customBook, bookIdx, s) == aInstrument
                    return true
                endif
                s = s + 1
            endwhile
        endif
        bookIdx = bookIdx + 1
    endwhile
    return false
EndFunction

; the unified picker: enumerate available songbooks live, list only songs for aInstrument
; (aInstrument 0 = show all, the safe degrade if instrument detection ever misses), pre-counting
; each book's matches so a book with no matching song never adds an orphan header. abIncludeInstrument
; Books per IsBookAvailable. The chosen song is dispatched through SgT's shell (PlayThroughSgT /
; SingThroughSgT) just as before.
Function OpenSongPicker(int aInstrument, bool abIncludeInstrumentBooks)
    ; clear any stale forced-song latch before arming a fresh pick: if a prior handoff set
    ; ARR_ForcedActive but the SgT effect never consumed it (rare - the player couldn't receive the
    ; spell), it must not bleed into this pick or the next random performance.
    ARR_ForcedActive = false
    if (_LP_BardIsPlaying.GetValue() as int) != 0
        return
    endif
    formlist allBooks = GetAllSongbooks()
    formlist allSpells = GetAllSongbookSpells()
    book customBook = GetCustomSongbook()
    miscobject customTitle = GetCustomTitle()
    formlist customNames = GetCustomNames()
    if allBooks == None || allSpells == None
        debug.Notification("You have not learned any songbooks to play from yet.")
        return
    endif
    if StandStill() == false
        return
    endif
    uilistmenu Songbook = (uiextensions.GetMenu("uilistmenu", true) as uilistmenu)
    int[] FormListIndices = new int[128]
    int[] SongListIndices = new int[128]
    int NumBooks = allBooks.GetSize()
    int bookIdx = 0
    int MenuIndex = 0
    while bookIdx < NumBooks && MenuIndex < 128
        book theBook = (allBooks.GetAt(bookIdx) as book)
        bool isCustom = (theBook == customBook)
        if IsBookAvailable(allBooks, allSpells, bookIdx, abIncludeInstrumentBooks)
            int NumSongs = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).Names.Length
            ; pre-count this book's songs that match the instrument filter
            int matches = 0
            int s = 0
            while s < NumSongs
                if aInstrument == 0 || GetSongInstrument(allBooks, customBook, bookIdx, s) == aInstrument
                    matches = matches + 1
                endif
                s = s + 1
            endwhile
            if matches > 0 && MenuIndex < 128
                string Title
                if isCustom
                    Title = customTitle.GetName()
                else
                    Title = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).Title
                endif
                int HeaderIndex = MenuIndex
                Songbook.AddEntryItem(Title, -1, MenuIndex, true)
                MenuIndex = MenuIndex + 1
                s = 0
                while s < NumSongs && MenuIndex < 128
                    if aInstrument == 0 || GetSongInstrument(allBooks, customBook, bookIdx, s) == aInstrument
                        string Name
                        if isCustom
                            Name = (customNames.GetAt(s) as miscobject).GetName()
                        else
                            Name = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).Names[s]
                        endif
                        Songbook.AddEntryItem(Name, HeaderIndex, MenuIndex, false)
                        FormListIndices[MenuIndex] = bookIdx
                        SongListIndices[MenuIndex] = s
                        MenuIndex = MenuIndex + 1
                    endif
                    s = s + 1
                endwhile
            endif
        endif
        bookIdx = bookIdx + 1
    endwhile
    if MenuIndex == 0
        ; nothing known for this instrument (the gate should have caught it; degrade gracefully)
        debug.Notification("You don't know any songs for that instrument yet.")
        CancelMenu()
        return
    endif
    Songbook.OpenMenu()
    int i = Songbook.GetResultInt()
    if i < 0 || i >= MenuIndex
        ; -1 = the player dismissed the menu; anything outside [0, MenuIndex) is an out-of-range
        ; selection (e.g. a header row) we never wrote a song index for - treat both as cancel.
        CancelMenu()
        return
    endif
    DispatchChosenSong(allBooks, customBook, FormListIndices[i], SongListIndices[i])
EndFunction

; play the chosen song through SgT's shell. Skyrim songbooks (voiced multi-verse) -> SingThroughSgT
; off the gendered verse formlists; custom songbook -> sound + length/instrument from its editable
; globals; every other songbook -> sound + length/instrument from its own book script arrays.
Function DispatchChosenSong(formlist allBooks, book customBook, int bookIdx, int songIdx)
    book theBook = (allBooks.GetAt(bookIdx) as book)
    if theBook == _LP_BardSongbookSkyrim || theBook == _LP_BardSongbookSkyrimRevised
        ; pick the sex-appropriate verse list FIRST, then take the verse count from the list we
        ; actually play - the male/female lists can differ in length, so reading NumVerses off the
        ; female list while playing the male one could under/over-run the verse loop.
        formlist Song
        int Sex = (PlayerREF.GetBaseObject() as actorbase).GetSex()
        if Sex == 1
            Song = (_LP_BardSongsofSkyrimFemale.GetAt(songIdx) as formlist)
        else
            Song = (_LP_BardSongsofSkyrimMale.GetAt(songIdx) as formlist)
        endif
        if Song == None
            debug.Notification("You don't know that song")
            CancelMenu()
            return
        endif
        int NumVerses = Song.GetSize()
        _lp_bardsongbookscript bs = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript)
        int vA = bs.InstrumentsA[songIdx]
        int vB = bs.InstrumentsB[songIdx]
        SingThroughSgT(Song, NumVerses, vA, vB)
    elseif theBook == customBook
        sound ChosenSong = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).Songs[songIdx]
        int ChosenLength = ((GetCustomLengths().GetAt(songIdx) as globalvariable).GetValue() as int)
        int cA = ((GetCustomInstrumentsA().GetAt(songIdx) as globalvariable).GetValue() as int)
        int cB = ((GetCustomInstrumentsB().GetAt(songIdx) as globalvariable).GetValue() as int)
        PlayThroughSgT(ChosenSong, ChosenLength, cA, cB)
    else
        sound ChosenSong = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).Songs[songIdx]
        int ChosenLength = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).Lengths[songIdx]
        int cA = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).InstrumentsA[songIdx]
        int cB = (allBooks.GetAt(bookIdx) as _lp_bardsongbookscript).InstrumentsB[songIdx]
        PlayThroughSgT(ChosenSong, ChosenLength, cA, cB)
    endif
EndFunction

Function QuickPlay()
    ; D9 hotkey - play the instrument you're carrying without opening the inventory.
    ; Adding the SgT instrument spell fires the same activate-to-play logic as clicking it.
    if (_LP_BardIsPlaying.GetValue() as int) != 0
        return
    endif
    bool hasDrum = HasInstrument(1)
    bool hasFlute = HasInstrument(2)
    bool hasLute = HasInstrument(3)
    int count = 0
    if hasDrum
        count = count + 1
    endif
    if hasFlute
        count = count + 1
    endif
    if hasLute
        count = count + 1
    endif
    if count == 0
        debug.Notification("You have no instrument to play.")
    elseif count == 1
        if hasDrum
            PlayInstrumentByType(1)
        elseif hasFlute
            PlayInstrumentByType(2)
        else
            PlayInstrumentByType(3)
        endif
    else
        uilistmenu Menu = (uiextensions.GetMenu("uilistmenu", true) as uilistmenu)
        int drumIdx = -1
        int fluteIdx = -1
        int luteIdx = -1
        if hasDrum
            drumIdx = Menu.AddEntryItem("Drum", -1, -1, false)
        endif
        if hasFlute
            fluteIdx = Menu.AddEntryItem("Flute", -1, -1, false)
        endif
        if hasLute
            luteIdx = Menu.AddEntryItem("Lute", -1, -1, false)
        endif
        Menu.OpenMenu()
        int sel = Menu.GetResultInt()
        if sel >= 0
            if sel == drumIdx
                PlayInstrumentByType(1)
            elseif sel == fluteIdx
                PlayInstrumentByType(2)
            elseif sel == luteIdx
                PlayInstrumentByType(3)
            endif
        endif
    endif
EndFunction

Function PlayInstrumentByType(int aType)
    spell toCast = None
    if aType == 1
        toCast = _Talent_DrumSpell
    elseif aType == 2
        toCast = _Talent_FluteSpell
    elseif aType == 3
        toCast = _Talent_LuteSpell
    endif
    if toCast
        if PlayerREF.HasSpell(toCast)
            PlayerREF.RemoveSpell(toCast)
        endif
        PlayerREF.AddSpell(toCast, false)
    endif
EndFunction

Function PlayThroughSgT(sound Song, int SongLength, int A, int B)
    ; Route a picker-chosen INSTRUMENTAL song through SgT's performance shell (movement +
    ; reactions + anims + first-person) instead of BaB's locked StandStill shell.
    if A < 1 || A > 3 || Song == None
        ; no SgT instrument shell exists for Voice/None - keep BaB's behaviour (StandStill is
        ; still active from the menu, so this plays locked, exactly as before).
        Play(Song, SongLength as float, A, B)
        return
    endif
    if HasInstrument(A) == false
        debug.Notification("You don't have the right instrument.")
        CancelMenu()
        return
    endif
    ; release the menu freeze (StandStill) so SgT's own movement-aware control setup takes over,
    ; and drop the BaB stop-keys it registered.
    UnregisterForKey(44)
    UnregisterForKey(275)
    CancelMenu()
    ARR_ForcedIsVoice = false
    ARR_ForcedSound = Song
    ARR_ForcedLength = SongLength
    ARR_ForcedInstrument = A
    ARR_ForcedActive = true
    PlayInstrumentByType(A)
EndFunction

Function SingThroughSgT(formlist Verse, int nVerses, int A, int B)
    ; Route a picker-chosen VOICED (multi-verse) song through SgT's shell. Only works when the
    ; song is accompanied by an instrument (1-3); a cappella (0/4) has no SgT trigger spell.
    if A < 1 || A > 3
        ; a cappella / voice-only: keep BaB's voiced shell (StandStill still active = locked).
        Sing(Verse, nVerses, A, B)
        return
    endif
    if HasInstrument(A) == false
        debug.Notification("You don't have the right instrument.")
        CancelMenu()
        return
    endif
    UnregisterForKey(44)
    UnregisterForKey(275)
    CancelMenu()
    ARR_ForcedIsVoice = true
    ARR_ForcedSound = None
    ARR_ForcedVerses = Verse
    ARR_ForcedVerseCount = nVerses
    ARR_ForcedInstrument = A
    ARR_ForcedActive = true
    PlayInstrumentByType(A)
EndFunction

bool Function HasInstrument(int A)
    if A == 0 || A == 4
        return true
    elseif A == 1
        int i = 0
        int n = _LP_BardDrums.GetSize()
        while i < n
            if PlayerREF.GetItemCount(_LP_BardDrums.GetAt(i)) > 0
                return true
            endif
            i = i + 1
        endwhile
        return false
    elseif A == 2
        int mangled_i_0 = 0
        int mangled_n_1 = _LP_BardFlutes.GetSize()
        while mangled_i_0 < mangled_n_1
            if PlayerREF.GetItemCount(_LP_BardFlutes.GetAt(mangled_i_0)) > 0
                return true
            endif
            mangled_i_0 = mangled_i_0 + 1
        endwhile
        return false
    elseif A == 3
        int mangled_i_2 = 0
        int mangled_n_3 = _LP_BardLutes.GetSize()
        while mangled_i_2 < mangled_n_3
            if PlayerREF.GetItemCount(_LP_BardLutes.GetAt(mangled_i_2)) > 0
                return true
            endif
            mangled_i_2 = mangled_i_2 + 1
        endwhile
        return false
    endif
    return false
EndFunction

Function UnequipShield()
    Shield = PlayerREF.GetEquippedShield()
    if !(Shield == None)
        PlayerREF.UnequipItem(Shield, 0, 1)
    endif
EndFunction

Function EquipShield()
    if !(Shield == None)
        PlayerREF.EquipItem(Shield, 0, 1)
    endif
EndFunction

Function UnequipLute()
    if PlayerREF.IsEquipped(_LP_BardLuteArmor)
        PlayerREF.UnequipItem(_LP_BardLuteArmor, 0, 1)
        Lute = _LP_BardLuteArmor
    endif
EndFunction

Function EquipLute()
    if !(Lute == None)
        if _LP_BardCustomFit.GetValue() == 1
            armoraddon LuteAA = Lute.GetNthArmorAddon(0)
            LuteAA.SetModelPath("LP\\instruments\\lutecloseAA.nif", false, false)
            LuteAA.SetModelPath("LP\\instruments\\lutecloseAA.nif", false, true)
        endif
        PlayerREF.EquipItem(Lute, 0, 1)
        Lute = None
    endif
EndFunction

Event OnItemAdded(form akBaseItem, int aiItemCount, objectreference akFormReference, objectreference akSourceContainer)
    ; D1 - do NOT grant any BaB play power; only keep the instrument's songbook in the known list
    ; so the max-level picker (and learned-song path) have content. SgT's activate-to-play wins.
    if _LP_BardDrums.HasForm(akBaseItem)
        if !_LP_BardKnownSongbooks.HasForm(_LP_BardSongbookDrum)
            _LP_BardKnownSongbooks.AddForm(_LP_BardSongbookDrum)
        endif
    elseif _LP_BardFlutes.HasForm(akBaseItem)
        if !_LP_BardKnownSongbooks.HasForm(_LP_BardSongbookFlute)
            _LP_BardKnownSongbooks.AddForm(_LP_BardSongbookFlute)
        endif
    elseif _LP_BardLutes.HasForm(akBaseItem)
        if !_LP_BardKnownSongbooks.HasForm(_LP_BardSongbookLute)
            _LP_BardKnownSongbooks.AddForm(_LP_BardSongbookLute)
        endif
    endif
EndEvent

Event OnItemRemoved(form akBaseItem, int aiItemCount, objectreference akItemReference, objectreference akDestContainer)
    if _LP_BardDrums.HasForm(akBaseItem)
        if HasInstrument(1) == 0
            _LP_BardKnownSongbooks.RemoveAddedForm(_LP_BardSongbookDrum)
        endif
    elseif _LP_BardFlutes.HasForm(akBaseItem)
        if HasInstrument(2) == 0
            _LP_BardKnownSongbooks.RemoveAddedForm(_LP_BardSongbookFlute)
        endif
    elseif _LP_BardLutes.HasForm(akBaseItem)
        if HasInstrument(3) == 0
            _LP_BardKnownSongbooks.RemoveAddedForm(_LP_BardSongbookLute)
        endif
    endif
EndEvent
