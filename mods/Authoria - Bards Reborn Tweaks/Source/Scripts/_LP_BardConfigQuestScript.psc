ScriptName _LP_BardConfigQuestScript extends SKI_ConfigBase

int CourtingToggle
int PreferredInstrumentText
int[] TavernCounts
int[] SongbookUniqueToggles
string CSOptionPage
int StoreJournal
int[] CustomLengthSliders
int CSPageSwitchNames
int SongbookCheatToggle
int[] CSPageCloseNames
int DancingToggle
int CSPageSwitchTitle
int CSPageCloseTitle
int StoreFit
string CSPage
int FactionAggressionToggle
int[] SongbookRegionalToggles
int CSPageSwitchLengths
int SpeechToggle
int JournalToggle
int[] CustomInstrumentsA
string[] Instruments
int CSPageSwitchInstruments
int CSRenameIndex
int StoreConsolidate
Actor[] Followers
int[] FollowerToggles
string MyPage
int ConsolidateToggle
string[] Pages
int CustomSongbookToggle
int[] CustomInstrumentsB
int CustomFitText
int AuthKeyOption
int AuthStoredKey

; --- ARR Bards Reborn Tweaks: play-known-anytime hotkey ---
globalvariable Property Auth_PlayKnownHotkey Auto
_LP_BardQuestPlayerScript Property Bard Auto
; per-instrument masteries shown on the Performance Log page (the <global=> book tag fails to
; resolve these cross-plugin SgT globals at book-render, so the MCM is the reliable readout)
globalvariable Property _Talent_Drum Auto
globalvariable Property _Talent_Lute Auto
globalvariable Property _Talent_Flute Auto
; ---

referencealias Property Follower02 Auto

globalvariable Property _LP_BardSongbookCheat Auto

globalvariable Property _LP_BardCourting Auto

formlist Property _LP_BardCustomSongbookInstrumentsA Auto

formlist Property _LP_BardSongbookSpellsRegional Auto

referencealias Property Follower04 Auto

miscobject Property _LP_BardCustomSongbookTitle Auto

book Property _LP_BardSongbookCustom Auto

referencealias Property Journal Auto

formlist Property _LP_BardCustomSongbookNames Auto

globalvariable Property _LP_BardConsolidateSongbook Auto

referencealias Property Follower01 Auto

formlist Property _LP_BardSongbookSpellsUnique Auto

armor Property _LP_BardLuteArmor Auto

globalvariable Property _LP_BardPreferredInstrument Auto

referencealias Property Follower00 Auto

globalvariable Property _LP_BardKeepJournal Auto

faction Property _LP_BardDoNotPlayFaction Auto

formlist Property _LP_BardSongbooksUnique Auto

globalvariable Property _LP_BardCustomFit Auto

globalvariable Property _LP_BardSkill Auto

spell Property _LP_BardSongbookCustomAbility Auto

spell Property _LP_BardSongbookAbility Auto

referencealias Property Follower03 Auto

formlist Property _LP_BardSongbookSpells Auto


formlist Property _LP_BardTavernCounts Auto

actor Property PlayerREF Auto

quest Property _LP_BardJournalQuest Auto

formlist Property _LP_BardCustomSongbookLengths Auto

formlist Property _LP_BardSongbooksRegional Auto

formlist Property _LP_BardKnownSongbooks Auto

globalvariable Property _LP_BardDancing Auto

formlist Property _LP_BardSongbooks Auto

formlist Property _LP_BardTavernLocations Auto

globalvariable Property _LP_BardFactionAggression Auto

formlist Property _LP_BardCustomSongbookInstrumentsB Auto

Event OnConfigInit()
    Pages = new string[5]
    Pages[0] = "Options"
    Pages[1] = "Songbooks"
    Pages[2] = "Custom Songbook"
    Pages[3] = "Performance Log"
    Pages[4] = "Followers"
    Instruments = new string[5]
    Instruments[0] = "None"
    Instruments[1] = "Drum"
    Instruments[2] = "Flute"
    Instruments[3] = "Lute"
    Instruments[4] = "Voice"
    TavernCounts = new int[30]
    SongbookRegionalToggles = new int[20]
    SongbookUniqueToggles = new int[30]
    CustomLengthSliders = new int[9]
    CustomInstrumentsA = new int[9]
    CustomInstrumentsB = new int[9]
    CSPageCloseNames = new int[9]
    FollowerToggles = new int[5]
    Followers = new Actor[5]
EndEvent

Event OnConfigOpen()
    StoreFit = (_LP_BardCustomFit.GetValue() as int)
    StoreJournal = (_LP_BardKeepJournal.GetValue() as int)
    StoreConsolidate = (_LP_BardConsolidateSongbook.GetValue() as int)
    Followers[0] = Follower00.GetActorRef()
    Followers[1] = Follower01.GetActorRef()
    Followers[2] = Follower02.GetActorRef()
    Followers[3] = Follower03.GetActorRef()
    Followers[4] = Follower04.GetActorRef()
EndEvent

Event OnConfigClose()
    if StoreFit > (_LP_BardCustomFit.GetValue() as int)
        bool Equip = false
        if PlayerREF.IsEquipped(_LP_BardLuteArmor)
            PlayerREF.UnEquipItem(_LP_BardLuteArmor, 0, 1)
            Equip = true
        endif
        armoraddon _LP_BardLuteArmorAA = _LP_BardLuteArmor.GetNthArmorAddon(0)
        _LP_BardLuteArmorAA.SetModelPath("LP\\instruments\\luteAA.nif", false, false)
        _LP_BardLuteArmorAA.SetModelPath("LP\\instruments\\luteAA.nif", false, true)
        if Equip
            PlayerREF.EquipItem(_LP_BardLuteArmor, 0, 1)
        endif
    elseif (_LP_BardCustomFit.GetValue() as int) > StoreFit
        bool mangled_equip_0 = false
        if PlayerREF.IsEquipped(_LP_BardLuteArmor)
            PlayerREF.UnEquipItem(_LP_BardLuteArmor, 0, 1)
            mangled_equip_0 = true
        endif
        armoraddon mangled__lp_bardlutearmoraa_1 = _LP_BardLuteArmor.GetNthArmorAddon(0)
        mangled__lp_bardlutearmoraa_1.SetModelPath("LP\\instruments\\lutecloseAA.nif", false, false)
        mangled__lp_bardlutearmoraa_1.SetModelPath("LP\\instruments\\lutecloseAA.nif", false, true)
        if mangled_equip_0
            PlayerREF.EquipItem(_LP_BardLuteArmor, 0, 1)
        endif
    endif
    if StoreJournal > (_LP_BardKeepJournal.GetValue() as int)
        if Journal.GetReference()
            PlayerREF.RemoveItem(Journal.GetReference(), 1, 1)
            utility.Wait(0.5)
            _LP_BardJournalQuest.Stop()
        endif
    elseif (_LP_BardKeepJournal.GetValue() as int) > StoreJournal
        _LP_BardJournalQuest.Start()
    endif
    if StoreConsolidate > (_LP_BardConsolidateSongbook.GetValue() as int)
        ExpandSongbook()
    elseif (_LP_BardConsolidateSongbook.GetValue() as int) > StoreConsolidate
        ConsolidateSongbook()
    endif
EndEvent

Event OnTextInputOpen(string asEventName, string asStringArg, float afNumArg, form akSender)
    string CurrentName = ""
    if CSRenameIndex > -1
        CurrentName = (_LP_BardCustomSongbookNames.GetAt(CSRenameIndex) as miscobject).GetName()
    else
        CurrentName = _LP_BardCustomSongbookTitle.GetName()
    endif
    uilib_1.TextInputMenu_SetData("Rename " + CurrentName + " to...", "")
EndEvent

Event OnTextInputClose(string asEventName, string asText, float afCancelled, form akSender)
    uilib_1.TextInputMenu_Release((Self as form))
    if !afCancelled
        if CSRenameIndex > -1
            _LP_BardCustomSongbookNames.GetAt(CSRenameIndex).SetName(asText)
        else
            _LP_BardCustomSongbookTitle.SetName(asText)
        endif
    endif
EndEvent

Event OnPageReset(string Page)
    int CustomSongbook
    MyPage = Page
    if Page == ""
        LoadCustomContent("skyui/res/mcm_logo.dds", 258, 95)
        return
    else
        UnloadCustomContent()
    endif
    if Page == "Options"
        SetCursorFillMode(Self.TOP_TO_BOTTOM)
        AddHeaderOption("Main Options", 0)
        PreferredInstrumentText = AddTextOption("Preferred Instrument", Instruments[(_LP_BardPreferredInstrument.GetValue() as int)], 0)
        CourtingToggle = AddToggleOption("Courting", (_LP_BardCourting.GetValue() as int), 0)
        DancingToggle = AddToggleOption("NPC Dancing", (_LP_BardDancing.GetValue() as int), 0)
        FactionAggressionToggle = AddToggleOption("Factions Respond to Songs", (_LP_BardFactionAggression.GetValue() as int), 0)
        AuthKeyOption = AddKeyMapOption("Quick-Play Instrument (Hotkey)", AuthStoredKey, 0)
        JournalToggle = AddToggleOption("Keep a Journal in Inventory", (_LP_BardKeepJournal.GetValue() as int), 0)
        if (_LP_BardCustomFit.GetValue() as int) == 0
            CustomFitText = AddTextOption("Wanderer's Lute Custom Fit", "Loose", 0)
        else
            CustomFitText = AddTextOption("Wanderer's Lute Custom Fit", "Snug", 0)
        endif
        AddEmptyOption()
        AddHeaderOption("Songbook Options", 0)
        if !(game.GetModByName("UIExtensions.esp") == 255)
            ConsolidateToggle = AddToggleOption("Consolidate Songbooks", (_LP_BardConsolidateSongbook.GetValue() as int), 0)
        else
            ConsolidateToggle = AddToggleOption("Consolidate Songbooks", 0, Self.OPTION_FLAG_DISABLED)
        endif
        SongbookCheatToggle = AddToggleOption("Enable Songbook Cheat Menu", (_LP_BardSongbookCheat.GetValue() as int), 0)
        SetCursorPosition(1)
        AddTextOption("Mod Version No.", "6.1.2", Self.OPTION_FLAG_DISABLED)
        AddTextOption("Compatible Plugins Detected:", "", Self.OPTION_FLAG_DISABLED)
        if !(game.GetModByName("Dragonborn.esm") == 255)
            AddToggleOption("Dragonborn", 1, Self.OPTION_FLAG_DISABLED)
        endif
        if !(game.GetModByName("WindhelmSSE.esp") == 255)
            AddToggleOption("Capital Windhelm Expansion", 1, Self.OPTION_FLAG_DISABLED)
        endif
        if !(game.GetModByName("LPMerchants.esp") == 255)
            AddToggleOption("Become a Merchant", 1, Self.OPTION_FLAG_DISABLED)
        endif
        if !(game.GetModByName("Chesko_Frostfall.esp") == 255)
            AddToggleOption("Frostfall", 1, Self.OPTION_FLAG_DISABLED)
        endif
    elseif Page == "Songbooks"
        if (_LP_BardSongbookCheat.GetValue() as int) == 0
            AddTextOption("Disabled on Options Page", "", Self.OPTION_FLAG_DISABLED)
        else
            SetCursorFillMode(Self.TOP_TO_BOTTOM)
            AddHeaderOption("Regional Songbooks", 0)
            ; clamp to the toggle-array sizes (SongbookRegionalToggles[20] / SongbookUniqueToggles[30])
            ; so a future songbook-adding mod that grows either formlist past its cap can't write the
            ; option-id arrays out of bounds (a Papyrus array OOB aborts the whole page build).
            int NumBooks = _LP_BardSongbooksRegional.GetSize()
            if NumBooks > 20
                NumBooks = 20
            endif
            int i = 0
            while i < NumBooks
                SongbookRegionalToggles[i] = AddToggleOption((_LP_BardSongbooksRegional.GetAt(i) as _lp_bardsongbookscript).Title, ((PlayerREF.HasSpell((_LP_BardSongbookSpellsRegional.GetAt(i) as spell)) || _LP_BardKnownSongbooks.HasForm(_LP_BardSongbooksRegional.GetAt(i))) as int), 0)
                i = i + 1
            endwhile
            SetCursorPosition(1)
            AddHeaderOption("Unique Songbooks", 0)
            NumBooks = _LP_BardSongbooksUnique.GetSize()
            if NumBooks > 30
                NumBooks = 30
            endif
            i = 0
            while i < NumBooks
                SongbookUniqueToggles[i] = AddToggleOption((_LP_BardSongbooksUnique.GetAt(i) as _lp_bardsongbookscript).Title, ((PlayerREF.HasSpell((_LP_BardSongbookSpellsUnique.GetAt(i) as spell)) || _LP_BardKnownSongbooks.HasForm(_LP_BardSongbooksUnique.GetAt(i))) as int), 0)
                i = i + 1
            endwhile
        endif
    elseif Page == "Custom Songbook"
        if CSPage == ""
            CSOptionPage = ""
            SetTitleText("Custom Songbook")
            SetCursorFillMode(Self.TOP_TO_BOTTOM)
            AddHeaderOption("Custom Songbook", 0)
            if PlayerREF.HasSpell(_LP_BardSongbookCustomAbility) || _LP_BardKnownSongbooks.HasForm(_LP_BardSongbookCustom)
                CustomSongbook = 1
            endif
            CustomSongbookToggle = AddToggleOption("Enable", CustomSongbook, 0)
            CSPageSwitchTitle = AddTextOption("Set Songbook Title", "", 0)
            CSPageSwitchNames = AddTextOption("Set Song Names", "", 0)
            CSPageSwitchLengths = AddTextOption("Set Song Lengths", "", 0)
            CSPageSwitchInstruments = AddTextOption("Set Song Instruments", "", 0)
        elseif CSPage == "Custom Songbook Title"
            CSOptionPage = "Custom Songbook Title"
            CSPage = ""
            SetTitleText("Rename Custom Songbook")
            SetCursorFillMode(Self.TOP_TO_BOTTOM)
            CSPageCloseTitle = AddTextOption(_LP_BardCustomSongbookTitle.GetName(), "Rename", 0)
        elseif CSPage == "Custom Song Names"
            CSOptionPage = "Custom Song Names"
            CSPage = ""
            SetTitleText("Rename Custom Songs")
            SetCursorFillMode(Self.TOP_TO_BOTTOM)
            AddHeaderOption("Song Names", 0)
            int mangled_i_2 = 0
            while mangled_i_2 < 9
                CSPageCloseNames[mangled_i_2] = AddTextOption((_LP_BardCustomSongbookNames.GetAt(mangled_i_2) as miscobject).GetName(), "Rename", 0)
                mangled_i_2 = mangled_i_2 + 1
            endwhile
            SetCursorPosition(1)
            AddHeaderOption("File Names", 0)
            mangled_i_2 = 0
            while mangled_i_2 < 9
                AddTextOption("Custom0" + (mangled_i_2 + 1) + ".xwm", "", Self.OPTION_FLAG_DISABLED)
                mangled_i_2 = mangled_i_2 + 1
            endwhile
        elseif CSPage == "Custom Song Lengths"
            CSOptionPage = "Custom Song Lengths"
            CSPage = ""
            SetTitleText("Custom Song Lenths")
            SetCursorFillMode(Self.TOP_TO_BOTTOM)
            AddHeaderOption("Length in Seconds", 0)
            int mangled_i_3 = 0
            while mangled_i_3 < 9
                CustomLengthSliders[mangled_i_3] = AddSliderOption("Custom0" + (mangled_i_3 + 1) + ".xwm", ((_LP_BardCustomSongbookLengths.GetAt(mangled_i_3) as globalvariable).GetValue() as int), "{0} seconds", 0)
                mangled_i_3 = mangled_i_3 + 1
            endwhile
        elseif CSPage == "Custom Song Instruments"
            CSOptionPage = "Custom Song Instruments"
            CSPage = ""
            SetTitleText("Custom Song Instruments")
            SetCursorFillMode(Self.TOP_TO_BOTTOM)
            AddHeaderOption("Primary Instrument", 0)
            int mangled_i_4 = 0
            while mangled_i_4 < 9
                CustomInstrumentsA[mangled_i_4] = AddTextOption("Custom0" + (mangled_i_4 + 1) + ".xwm Instrument A", Instruments[((_LP_BardCustomSongbookInstrumentsA.GetAt(mangled_i_4) as globalvariable).GetValue() as int)], 0)
                mangled_i_4 = mangled_i_4 + 1
            endwhile
            SetCursorPosition(1)
            AddHeaderOption("Secondary Instrument", 0)
            mangled_i_4 = 0
            while mangled_i_4 < 9
                CustomInstrumentsB[mangled_i_4] = AddTextOption("Custom0" + (mangled_i_4 + 1) + ".xwm Instrument B", Instruments[((_LP_BardCustomSongbookInstrumentsB.GetAt(mangled_i_4) as globalvariable).GetValue() as int)], 0)
                mangled_i_4 = mangled_i_4 + 1
            endwhile
        endif
    elseif Page == "Performance Log"
        SetCursorFillMode(Self.TOP_TO_BOTTOM)
        AddHeaderOption("Skill Level", 0)
        AddTextOption("Bard Skill", (_LP_BardSkill.GetValue() as int), 0)
        AddTextOption("Drum Mastery", (_Talent_Drum.GetValue() as int), 0)
        AddTextOption("Lute Mastery", (_Talent_Lute.GetValue() as int), 0)
        AddTextOption("Flute Mastery", (_Talent_Flute.GetValue() as int), 0)
        AddHeaderOption("Tavern Counts", 0)
        int mangled_i_5 = 0
        int j = 0
        while mangled_i_5 < _LP_BardTavernLocations.GetSize() && j < 9
            TavernCounts[mangled_i_5] = AddTextOption(_LP_BardTavernLocations.GetAt(mangled_i_5).GetName(), ((_LP_BardTavernCounts.GetAt(mangled_i_5) as globalvariable).GetValue() as int), 0)
            j = j + 1
            mangled_i_5 = mangled_i_5 + 1
        endwhile
        SetCursorPosition(1)
        while mangled_i_5 < _LP_BardTavernLocations.GetSize() && mangled_i_5 < 30
            TavernCounts[mangled_i_5] = AddTextOption(_LP_BardTavernLocations.GetAt(mangled_i_5).GetName(), ((_LP_BardTavernCounts.GetAt(mangled_i_5) as globalvariable).GetValue() as int), 0)
            mangled_i_5 = mangled_i_5 + 1
        endwhile
    elseif Page == "Followers"
        SetCursorFillMode(Self.TOP_TO_BOTTOM)
        AddHeaderOption("Bard Followers", 0)
        int mangled_i_6 = 0
        while mangled_i_6 < 5
            if Followers[mangled_i_6]
                FollowerToggles[mangled_i_6] = AddToggleOption(Followers[mangled_i_6].GetActorBase().GetName(), !Followers[mangled_i_6].IsInFaction(_LP_BardDoNotPlayFaction), 0)
            endif
            mangled_i_6 = mangled_i_6 + 1
        endwhile
        SetCursorPosition(1)
        AddTextOption("The follower list is refreshed each time", "", Self.OPTION_FLAG_DISABLED)
        AddTextOption("you play.", "", Self.OPTION_FLAG_DISABLED)
        AddEmptyOption()
        AddTextOption("To see newly-added followers in this list,", "", Self.OPTION_FLAG_DISABLED)
        AddTextOption("play any song.", "", Self.OPTION_FLAG_DISABLED)
    endif
EndEvent

Event OnOptionHighlight(int Option)
    if MyPage == "Options"
        if Option == AuthKeyOption
            SetInfoText("Hotkey to start playing the instrument you are carrying, without opening your inventory. If you hold more than one, you will be asked which to play.")
        elseif Option == PreferredInstrumentText
            SetInfoText("Your preferred instrument for multi-part songs")
        elseif Option == FactionAggressionToggle
            SetInfoText("Enables Stormcloak songs to enrage Imperials, and vice versa")
        elseif Option == CourtingToggle
            SetInfoText("Enables performances to influence relationship rank with NPCs")
        elseif Option == DancingToggle
            SetInfoText("Enables NPC dancing while you are playing songs")
        elseif Option == CustomFitText
            SetInfoText("Whether the lute sits far away or very close to the back  (Select Loose option if you wear bulky armor or arrows)  Exit the MCM for changes to be applied")
        elseif Option == SongbookCheatToggle
            SetInfoText("Enables the songbook cheat page on the next page of the MCM")
        elseif Option == ConsolidateToggle
            SetInfoText("Whether to consolidate all songbook powers into one.  Requires UIExtensions.  Consolidated songbook can be convenient, but is a little slower to fire and has a limit of 128 entries.")
        endif
    elseif MyPage == "Performance Log"
        int NumTaverns = _LP_BardTavernLocations.GetSize()
        if NumTaverns > 30
            NumTaverns = 30
        endif
        int i = 0
        while i < NumTaverns
            if Option == TavernCounts[i]
                SetInfoText("Number of times you've performed at the " + _LP_BardTavernLocations.GetAt(i).GetName())
            endif
            i = i + 1
        endwhile
    elseif MyPage == "Custom Songbook"
        if CSOptionPage == ""
            if Option == CSPageSwitchTitle
                SetInfoText("Rename the Custom Songbook")
            elseif Option == CSPageSwitchNames
                SetInfoText("Set the name of each song in your Custom Songbook")
            elseif Option == CSPageSwitchLengths
                SetInfoText("Set the length of each song in your Custom Songbook")
            elseif Option == CSPageSwitchInstruments
                SetInfoText("Set the instruments to use with each song in your Custom Songbook")
            else
                SetInfoText("Place these custom songs in the folder Skyrim\\Data\\Sound\\FX\\Mus\\Bard\\Custom")
            endif
        elseif CSOptionPage == "Custom Songbook Title" || CSOptionPage == "Custom Song Names"
            SetInfoText("Selecting RENAME will close the MCM and open a text box.  DO NOT change the file name in your data folder (Custom01.xwm, etc).  This only changes the name in-game.")
        elseif CSOptionPage == "Custom Song Lengths" || CSOptionPage == "Custom Song Instruments"
            SetInfoText("Place these custom songs in the folder Skyrim\\Data\\Sound\\FX\\Mus\\Bard\\Custom")
        endif
    elseif MyPage == "Songbooks"
        SetInfoText("Songbooks are abilities, just like special racial abilities.  Select them in your spell menu and press Z to use.")
    elseif MyPage == "Followers"
        SetInfoText("Followers left unchecked will not play music with you and will join the audience.")
    endif
EndEvent

Event OnOptionSliderOpen(int Option)
    if CSOptionPage == "Custom Song Lengths"
        int i = 0
        while i < 9
            if Option == CustomLengthSliders[i]
                SetSliderDialogStartValue(((_LP_BardCustomSongbookLengths.GetAt(i) as globalvariable).GetValue() as int))
                SetSliderDialogDefaultValue(60)
                SetSliderDialogRange(1, 300)
                SetSliderDialogInterval(1)
            endif
            i = i + 1
        endwhile
    endif
EndEvent

Event OnOptionSliderAccept(int Option, float value)
    if CSOptionPage == "Custom Song Lengths"
        int i = 0
        while i < 9
            if Option == CustomLengthSliders[i]
                (_LP_BardCustomSongbookLengths.GetAt(i) as globalvariable).SetValue(value)
                SetSliderOptionValue(Option, value, "{0} seconds", false)
            endif
            i = i + 1
        endwhile
    endif
EndEvent

Event OnOptionSelect(int Option)
    if MyPage == "Options"
        if Option == CourtingToggle
            if (_LP_BardCourting.GetValue() as int) == 0
                _LP_BardCourting.SetValue(1)
                SetToggleOptionValue(Option, 1, false)
            else
                _LP_BardCourting.SetValue(0)
                SetToggleOptionValue(Option, 0, false)
            endif
        elseif Option == DancingToggle
            if (_LP_BardDancing.GetValue() as int) == 0
                _LP_BardDancing.SetValue(1)
                SetToggleOptionValue(Option, 1, false)
            else
                _LP_BardDancing.SetValue(0)
                SetToggleOptionValue(Option, 0, false)
            endif
        elseif Option == FactionAggressionToggle
            if (_LP_BardFactionAggression.GetValue() as int) == 0
                _LP_BardFactionAggression.SetValue(1)
                SetToggleOptionValue(Option, 1, false)
            else
                _LP_BardFactionAggression.SetValue(0)
                SetToggleOptionValue(Option, 0, false)
            endif
        elseif Option == JournalToggle
            if (_LP_BardKeepJournal.GetValue() as int) == 0
                _LP_BardKeepJournal.SetValue(1)
                SetToggleOptionValue(Option, 1, false)
            else
                _LP_BardKeepJournal.SetValue(0)
                SetToggleOptionValue(Option, 0, false)
            endif
        elseif Option == SongbookCheatToggle
            if (_LP_BardSongbookCheat.GetValue() as int) == 0
                _LP_BardSongbookCheat.SetValue(1)
                SetToggleOptionValue(Option, 1, false)
            else
                _LP_BardSongbookCheat.SetValue(0)
                SetToggleOptionValue(Option, 0, false)
            endif
        elseif Option == ConsolidateToggle
            if (_LP_BardConsolidateSongbook.GetValue() as int) == 0
                _LP_BardConsolidateSongbook.SetValue(1)
                SetToggleOptionValue(Option, 1, false)
            else
                _LP_BardConsolidateSongbook.SetValue(0)
                SetToggleOptionValue(Option, 0, false)
            endif
        elseif Option == PreferredInstrumentText
            int Current = (_LP_BardPreferredInstrument.GetValue() as int)
            if Current < 4
                _LP_BardPreferredInstrument.SetValue(Current + 1)
                SetTextOptionValue(Option, Instruments[Current + 1], false)
            elseif Current == 4
                _LP_BardPreferredInstrument.SetValue(1)
                SetTextOptionValue(Option, Instruments[1], false)
            endif
        elseif Option == CustomFitText
            if (_LP_BardCustomFit.GetValue() as int) == 0
                _LP_BardCustomFit.SetValue(1)
                SetTextOptionValue(Option, "Snug", false)
            else
                _LP_BardCustomFit.SetValue(0)
                SetTextOptionValue(Option, "Loose", false)
            endif
        endif
    elseif MyPage == "Custom Songbook"
        if CSOptionPage == ""
            if Option == CSPageSwitchTitle
                CSPage = "Custom Songbook Title"
                ForcePageReset()
            elseif Option == CSPageSwitchNames
                CSPage = "Custom Song Names"
                ForcePageReset()
            elseif Option == CSPageSwitchLengths
                CSPage = "Custom Song Lengths"
                ForcePageReset()
            elseif Option == CSPageSwitchInstruments
                CSPage = "Custom Song Instruments"
                ForcePageReset()
            elseif Option == CustomSongbookToggle
                formlist LLcustom = GetLearnedList()
                if PlayerREF.HasSpell(_LP_BardSongbookCustomAbility) || _LP_BardKnownSongbooks.HasForm(_LP_BardSongbookCustom)
                    PlayerREF.RemoveSpell(_LP_BardSongbookCustomAbility)
                    _LP_BardKnownSongbooks.RemoveAddedForm(_LP_BardSongbookCustom)
                    if LLcustom
                        LLcustom.RemoveAddedForm(_LP_BardSongbookCustom)
                    endif
                    SetToggleOptionValue(Option, 0, false)
                else
                    if (_LP_BardConsolidateSongbook.GetValue() as int) == 0
                        PlayerREF.AddSpell(_LP_BardSongbookCustomAbility, 0)
                    else
                        _LP_BardKnownSongbooks.AddForm(_LP_BardSongbookCustom)
                        PlayerREF.AddSpell(_LP_BardSongbookAbility, 0)
                    endif
                    if LLcustom && !LLcustom.HasForm(_LP_BardSongbookCustom)
                        LLcustom.AddForm(_LP_BardSongbookCustom)
                    endif
                    SetToggleOptionValue(Option, 1, false)
                endif
            endif
        elseif CSOptionPage == "Custom Songbook Title"
            if Option == CSPageCloseTitle
                CSRenameIndex = -1
                int Esc = input.GetMappedKey("Tween Menu", 255)
                while utility.IsInMenuMode()
                    input.TapKey(Esc)
                    utility.WaitMenuMode(0.25)
                endwhile
                uilib_1.TextInputMenu_Open((Self as form))
            endif
        elseif CSOptionPage == "Custom Song Names"
            int i = 0
            while i < 9
                if Option == CSPageCloseNames[i]
                    CSRenameIndex = i
                endif
                i = i + 1
            endwhile
            int mangled_esc_7 = input.GetMappedKey("Tween Menu", 255)
            while utility.IsInMenuMode()
                input.TapKey(mangled_esc_7)
                utility.WaitMenuMode(0.25)
            endwhile
            uilib_1.TextInputMenu_Open((Self as form))
        elseif CSOptionPage == "Custom Song Instruments"
            int mangled_i_8 = 0
            while mangled_i_8 < 9
                if Option == CustomInstrumentsA[mangled_i_8]
                    int mangled_current_9 = ((_LP_BardCustomSongbookInstrumentsA.GetAt(mangled_i_8) as globalvariable).GetValue() as int)
                    if mangled_current_9 < 3
                        (_LP_BardCustomSongbookInstrumentsA.GetAt(mangled_i_8) as globalvariable).SetValue(mangled_current_9 + 1)
                        SetTextOptionValue(Option, Instruments[mangled_current_9 + 1], false)
                    elseif mangled_current_9 == 3
                        (_LP_BardCustomSongbookInstrumentsA.GetAt(mangled_i_8) as globalvariable).SetValue(1)
                        SetTextOptionValue(Option, Instruments[1], false)
                    endif
                endif
                mangled_i_8 = mangled_i_8 + 1
            endwhile
            mangled_i_8 = 0
            while mangled_i_8 < 9
                if Option == CustomInstrumentsB[mangled_i_8]
                    int mangled_current_10 = ((_LP_BardCustomSongbookInstrumentsB.GetAt(mangled_i_8) as globalvariable).GetValue() as int)
                    if mangled_current_10 < 3
                        (_LP_BardCustomSongbookInstrumentsB.GetAt(mangled_i_8) as globalvariable).SetValue(mangled_current_10 + 1)
                        SetTextOptionValue(Option, Instruments[mangled_current_10 + 1], false)
                    elseif mangled_current_10 == 3
                        (_LP_BardCustomSongbookInstrumentsB.GetAt(mangled_i_8) as globalvariable).SetValue(1)
                        SetTextOptionValue(Option, Instruments[1], false)
                    endif
                endif
                mangled_i_8 = mangled_i_8 + 1
            endwhile
        endif
    elseif MyPage == "Songbooks"
        ; ARR: keep Auth_LearnedSongbooks in sync with MCM-toggled songbooks so the play-known
        ; hotkey/learned picker sees songbooks enabled here (not just ones read from a book).
        formlist LL = GetLearnedList()
        int NumBooks = _LP_BardSongbooksRegional.GetSize()
        if NumBooks > 20
            NumBooks = 20
        endif
        int mangled_i_11 = 0
        while mangled_i_11 < NumBooks
            if Option == SongbookRegionalToggles[mangled_i_11]
                if PlayerREF.HasSpell((_LP_BardSongbookSpellsRegional.GetAt(mangled_i_11) as spell)) || _LP_BardKnownSongbooks.HasForm(_LP_BardSongbooksRegional.GetAt(mangled_i_11))
                    PlayerREF.RemoveSpell((_LP_BardSongbookSpellsRegional.GetAt(mangled_i_11) as spell))
                    _LP_BardKnownSongbooks.RemoveAddedForm(_LP_BardSongbooksRegional.GetAt(mangled_i_11))
                    if LL
                        LL.RemoveAddedForm(_LP_BardSongbooksRegional.GetAt(mangled_i_11))
                    endif
                    SetToggleOptionValue(Option, 0, false)
                else
                    if (_LP_BardConsolidateSongbook.GetValue() as int) == 0
                        PlayerREF.AddSpell((_LP_BardSongbookSpellsRegional.GetAt(mangled_i_11) as spell), 0)
                    else
                        _LP_BardKnownSongbooks.AddForm(_LP_BardSongbooksRegional.GetAt(mangled_i_11))
                        PlayerREF.AddSpell(_LP_BardSongbookAbility, 0)
                    endif
                    if LL && !LL.HasForm(_LP_BardSongbooksRegional.GetAt(mangled_i_11))
                        LL.AddForm(_LP_BardSongbooksRegional.GetAt(mangled_i_11))
                    endif
                    SetToggleOptionValue(Option, 1, false)
                endif
            endif
            mangled_i_11 = mangled_i_11 + 1
        endwhile
        NumBooks = _LP_BardSongbooksUnique.GetSize()
        if NumBooks > 30
            NumBooks = 30
        endif
        mangled_i_11 = 0
        while mangled_i_11 < NumBooks
            if Option == SongbookUniqueToggles[mangled_i_11]
                if PlayerREF.HasSpell((_LP_BardSongbookSpellsUnique.GetAt(mangled_i_11) as spell)) || _LP_BardKnownSongbooks.HasForm(_LP_BardSongbooksUnique.GetAt(mangled_i_11))
                    PlayerREF.RemoveSpell((_LP_BardSongbookSpellsUnique.GetAt(mangled_i_11) as spell))
                    _LP_BardKnownSongbooks.RemoveAddedForm(_LP_BardSongbooksUnique.GetAt(mangled_i_11))
                    if LL
                        LL.RemoveAddedForm(_LP_BardSongbooksUnique.GetAt(mangled_i_11))
                    endif
                    SetToggleOptionValue(Option, 0, false)
                else
                    if (_LP_BardConsolidateSongbook.GetValue() as int) == 0
                        PlayerREF.AddSpell((_LP_BardSongbookSpellsUnique.GetAt(mangled_i_11) as spell), 0)
                    else
                        _LP_BardKnownSongbooks.AddForm(_LP_BardSongbooksUnique.GetAt(mangled_i_11))
                        PlayerREF.AddSpell(_LP_BardSongbookAbility, 0)
                    endif
                    if LL && !LL.HasForm(_LP_BardSongbooksUnique.GetAt(mangled_i_11))
                        LL.AddForm(_LP_BardSongbooksUnique.GetAt(mangled_i_11))
                    endif
                    SetToggleOptionValue(Option, 1, false)
                endif
            endif
            mangled_i_11 = mangled_i_11 + 1
        endwhile
    elseif MyPage == "Followers"
        int mangled_i_12 = 0
        while mangled_i_12 < 5
            if Option == FollowerToggles[mangled_i_12] && Followers[mangled_i_12]
                if Followers[mangled_i_12].IsInFaction(_LP_BardDoNotPlayFaction) == 0
                    Followers[mangled_i_12].AddToFaction(_LP_BardDoNotPlayFaction)
                    SetToggleOptionValue(Option, 0, false)
                else
                    Followers[mangled_i_12].RemoveFromFaction(_LP_BardDoNotPlayFaction)
                    SetToggleOptionValue(Option, 1, false)
                endif
            endif
            mangled_i_12 = mangled_i_12 + 1
        endwhile
    endif
EndEvent

Function ConsolidateSongbook()
    int i
    int NumBooks = _LP_BardSongbooks.GetSize()
    int AddSongbook = 0
    while i < NumBooks
        if PlayerREF.HasSpell((_LP_BardSongbookSpells.GetAt(i) as spell))
            _LP_BardKnownSongbooks.AddForm((_LP_BardSongbooks.GetAt(i) as book))
            PlayerREF.RemoveSpell((_LP_BardSongbookSpells.GetAt(i) as spell))
            AddSongbook = 1
        endif
        i = i + 1
    endwhile
    if AddSongbook == 1
        PlayerREF.AddSpell(_LP_BardSongbookAbility, 0)
    endif
EndFunction

Function ExpandSongbook()
    int i
    int NumBooks = _LP_BardSongbooks.GetSize()
    while i < NumBooks
        if _LP_BardKnownSongbooks.HasForm(_LP_BardSongbooks.GetAt(i))
            PlayerREF.AddSpell((_LP_BardSongbookSpells.GetAt(i) as spell), 0)
            _LP_BardKnownSongbooks.RemoveAddedForm(_LP_BardSongbooks.GetAt(i))
        endif
        i = i + 1
    endwhile
    PlayerREF.RemoveSpell(_LP_BardSongbookAbility)
EndFunction

; --- ARR: the play-known-anytime learned-songbook list (Auth_LearnedSongbooks 000800), shared
; with _LP_BardReadSongbookScript; resolved by FormID so no extra property/VMAD wiring is needed.
formlist Function GetLearnedList()
    return (game.GetFormFromFile(0x00000800, "Authoria - Master Patch - Bards Reborn Tweaks.esp") as formlist)
EndFunction

; --- ARR Bards Reborn Tweaks: play-known-anytime hotkey handling ---
Event OnGameReload()
    parent.OnGameReload()
    AuthStoredKey = (Auth_PlayKnownHotkey.GetValue() as int)
    UnregisterForKey(AuthStoredKey)
    if AuthStoredKey > 0
        RegisterForKey(AuthStoredKey)
    endif
EndEvent

Event OnKeyDown(int keyCode)
    if keyCode == AuthStoredKey && AuthStoredKey > 0
        if !utility.IsInMenuMode() && Bard != None
            Bard.QuickPlay()
        endif
    endif
EndEvent

Event OnOptionKeyMapChange(int option, int keyCode, string conflictControl, string conflictName)
    if option == AuthKeyOption
        UnregisterForKey(AuthStoredKey)
        Auth_PlayKnownHotkey.SetValue(keyCode)
        AuthStoredKey = keyCode
        if keyCode > 0
            RegisterForKey(keyCode)
        endif
        SetKeyMapOptionValue(option, keyCode, false)
    endif
EndEvent

