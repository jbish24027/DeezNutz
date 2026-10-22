ScriptName _LP_BardPlaySongbookUIEScript extends activemagiceffect
; ARR - Bards Reborn Tweaks: the max-level full-library picker, fired by _LP_BardSongbookAbility
; (cast by _talent_playinstrument when the activated instrument is mastered, and castable as a
; LesserPower from the magic menu). Section A redesign: it now just delegates to the alias's single
; OpenSongPicker, which enumerates currently-known songbooks LIVE (HasSpell || KnownList.HasForm,
; consolidate-independent + retroactive) and filters songs to the instrument the player activated
; (ARR_PickerInstrument, stashed by _talent_playinstrument before the cast; 0 = show all). The chosen
; song still plays through SgT's shell (movement + reactions + anims). Shipped LOOSE (overrides BSA).

_lp_bardquestplayerscript Property Bard Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
    if Bard
        ; the mastered full library: include the basic per-instrument books too
        Bard.OpenSongPicker(Bard.ARR_PickerInstrument, true)
    endif
EndEvent

