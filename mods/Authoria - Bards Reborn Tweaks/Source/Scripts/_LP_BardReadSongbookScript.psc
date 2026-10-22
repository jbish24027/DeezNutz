ScriptName _LP_BardReadSongbookScript extends ObjectReference
; ARR - Bards Reborn Tweaks: maintains Auth_LearnedSongbooks (the "songs you know" list
; used by the play-known-anytime hotkey) in parallel with _LP_BardKnownSongbooks, so a
; songbook the player has explicitly LEARNED (by reading it) becomes playable at any skill.

message Property _LP_BardMenuLearn Auto

globalvariable Property _LP_BardConsolidateSongbook Auto

formlist Property _LP_BardKnownSongbooks Auto

spell Property _LP_BardSongbookAbility Auto

actor Property PlayerREF Auto

spell Property SongbookSpell Auto

book Property Songbook Auto

message Property _LP_BardMenuUnlearn Auto

formlist Function GetLearnedList()
    return (game.GetFormFromFile(0x00000800, "Authoria - Master Patch - Bards Reborn Tweaks.esp") as formlist)
EndFunction

Event OnRead()
    formlist LearnedList = GetLearnedList()
    ; "known" is mode-agnostic: a book counts as learned if it is in EITHER store - the consolidated
    ; _LP_BardKnownSongbooks list OR the player holding its individual SongbookSpell. This keeps
    ; learn/unlearn consistent even when the Consolidate MCM option is toggled between reads of the
    ; same book (the old per-mode keying could leave a book registered in one store but not the other,
    ; double-granting on re-learn or stranding the ability on unlearn).
    bool isKnown = _LP_BardKnownSongbooks.HasForm(Songbook) || PlayerREF.HasSpell(SongbookSpell)
    if isKnown
        if _LP_BardMenuUnlearn.Show() == 0
            ; UNLEARN: clear the book from BOTH stores, whichever mode it was learned in.
            if PlayerREF.HasSpell(SongbookSpell)
                PlayerREF.RemoveSpell(SongbookSpell)
            endif
            if _LP_BardKnownSongbooks.HasForm(Songbook)
                _LP_BardKnownSongbooks.RemoveAddedForm(Songbook)
                if _LP_BardKnownSongbooks.GetSize() == 0
                    PlayerREF.RemoveSpell(_LP_BardSongbookAbility)
                endif
            endif
            if LearnedList
                LearnedList.RemoveAddedForm(Songbook)
            endif
        endif
    else
        if _LP_BardMenuLearn.Show() == 0
            ; LEARN: register the book in the form the CURRENT mode uses (consolidated list + shared
            ; ability, or the individual songbook spell).
            if (_LP_BardConsolidateSongbook.GetValue() as int) == 1
                if !_LP_BardKnownSongbooks.HasForm(Songbook)
                    _LP_BardKnownSongbooks.AddForm(Songbook)
                endif
                if _LP_BardKnownSongbooks.GetSize() == 1
                    PlayerREF.AddSpell(_LP_BardSongbookAbility, 0)
                endif
            else
                PlayerREF.AddSpell(SongbookSpell, true)
            endif
            if LearnedList && !LearnedList.HasForm(Songbook)
                LearnedList.AddForm(Songbook)
            endif
        endif
    endif
EndEvent
