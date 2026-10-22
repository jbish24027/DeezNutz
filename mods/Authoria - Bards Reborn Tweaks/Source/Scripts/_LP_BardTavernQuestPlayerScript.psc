ScriptName _LP_BardTavernQuestPlayerScript Extends ReferenceAlias

;-- Variables ---------------------------------------
Location LocationREF
Actor PlayerREF

;-- Properties --------------------------------------
ReferenceAlias Property Alias_Innkeeper Auto
LocationAlias Property Alias_Location Auto
MiscObject Property Gold001 Auto
ReferenceAlias Property Journal Auto
Actor Property PlayerREF Auto
Spell Property _LP_BardExperiencedAbility Auto
Quest Property _LP_BardJournalQuest Auto
GlobalVariable Property _LP_BardKeepJournal Auto
GlobalVariable Property _LP_BardQuestsCompleted Auto
FormList Property _LP_BardRank00Locations Auto
FormList Property _LP_BardRank01Locations Auto
FormList Property _LP_BardRank02Locations Auto
Spell Property _LP_BardRenownedAbility Auto
GlobalVariable Property _LP_BardSkill Auto
FormList Property _LP_BardTavernCounts Auto
FormList Property _LP_BardTavernLocations Auto
Spell Property _LP_BardWellKnownAbility Auto

;-- Functions ---------------------------------------

; Skipped compiler generated GetState

; Skipped compiler generated GotoState

Event OnInit()
  LocationREF = Alias_Location.GetLocation() ; #DEBUG_LINE_NO:24
EndEvent

Event OnLocationChange(Location akOldLoc, Location akNewLoc)
  If PlayerREF.IsInLocation(Alias_Location.GetLocation()) == False ; #DEBUG_LINE_NO:28
    If Self.GetOwningQuest().GetStage() == 0 ; #DEBUG_LINE_NO:29
      Self.GetOwningQuest().Stop() ; #DEBUG_LINE_NO:30
    ElseIf Self.GetOwningQuest().GetStage() == 10 ; #DEBUG_LINE_NO:31
      Self.GetOwningQuest().SetObjectiveFailed(10, True) ; #DEBUG_LINE_NO:32
      Self.GetOwningQuest().SetStage(0) ; #DEBUG_LINE_NO:33
      Self.GetOwningQuest().Stop() ; #DEBUG_LINE_NO:34
    EndIf
  EndIf
EndEvent

Function RewardPlayer()
  Float BardSkill = _LP_BardSkill.GetValue() ; #DEBUG_LINE_NO:40
  _LP_BardQuestsCompleted.Mod(1 as Float) ; #DEBUG_LINE_NO:41
  ObjectReference JournalREF = Journal.GetReference() ; #DEBUG_LINE_NO:44
  Quest JournalQuest = _LP_BardJournalQuest ; #DEBUG_LINE_NO:45
  If JournalREF ; #DEBUG_LINE_NO:46
    PlayerREF.RemoveItem(JournalREF as Form, 1, 1 as Bool, None) ; #DEBUG_LINE_NO:47
  EndIf
  Int i = _LP_BardTavernLocations.GetSize() ; #DEBUG_LINE_NO:49
  Int RewardRank = 0 ; #DEBUG_LINE_NO:50
  While i > 0 ; #DEBUG_LINE_NO:51
    i -= 1 ; #DEBUG_LINE_NO:52
    If LocationREF as Form == _LP_BardTavernLocations.GetAt(i) ; #DEBUG_LINE_NO:53
      (_LP_BardTavernCounts.GetAt(i) as GlobalVariable).SetValue(((_LP_BardTavernCounts.GetAt(i) as GlobalVariable).GetValue() as Int + 1) as Float) ; #DEBUG_LINE_NO:54
      Int j = _LP_BardRank01Locations.GetSize() ; #DEBUG_LINE_NO:55
      While j > 0 ; #DEBUG_LINE_NO:56
        j -= 1 ; #DEBUG_LINE_NO:57
        If LocationREF as Form == _LP_BardRank01Locations.GetAt(j) ; #DEBUG_LINE_NO:58
          RewardRank = 1 ; #DEBUG_LINE_NO:59
        EndIf
      EndWhile
      j = _LP_BardRank02Locations.GetSize() ; #DEBUG_LINE_NO:62
      While j > 0 ; #DEBUG_LINE_NO:63
        j -= 1 ; #DEBUG_LINE_NO:64
        If LocationREF as Form == _LP_BardRank02Locations.GetAt(j) ; #DEBUG_LINE_NO:65
          RewardRank = 2 ; #DEBUG_LINE_NO:66
        EndIf
      EndWhile
    EndIf
  EndWhile
  Self.CheckForNewPerks(BardSkill) ; #DEBUG_LINE_NO:71
  Int RewardGold = Self.CalculateGold(BardSkill, RewardRank) ; #DEBUG_LINE_NO:72
  ; ARR Bards Reborn Tweaks: per-venue daily cooldown. _AuthBardPaidToday (FormList) accumulates the
  ; taverns paid on the current in-game day held in _AuthBardGigDay, and reverts when the day rolls
  ; over - so re-performing at a tavern already paid today yields 0 gold (the gig still completes and
  ; renown still ticked above in CheckForNewPerks). Forms are pulled by FormID from our master patch,
  ; like the loose bard scripts already do, so no quest-alias VMAD property wiring is needed.
  GlobalVariable AuthGigDay = Game.GetFormFromFile(0x00000802, "Authoria - Master Patch - Bards Reborn Tweaks.esp") as GlobalVariable
  FormList AuthPaidToday = Game.GetFormFromFile(0x00000803, "Authoria - Master Patch - Bards Reborn Tweaks.esp") as FormList
  If AuthGigDay && AuthPaidToday && LocationREF
    Float AuthToday = (Utility.GetCurrentGameTime() as Int) as Float
    If AuthGigDay.GetValue() != AuthToday
      AuthPaidToday.Revert()
      AuthGigDay.SetValue(AuthToday)
    EndIf
    If AuthPaidToday.HasForm(LocationREF as Form)
      RewardGold = 0
    Else
      AuthPaidToday.AddForm(LocationREF as Form)
    EndIf
  EndIf
  If RewardGold > 0
    PlayerREF.AddItem(Gold001 as Form, RewardGold, False) ; #DEBUG_LINE_NO:73
  EndIf
  If _LP_BardKeepJournal.GetValue() as Int > 0 ; #DEBUG_LINE_NO:74
    JournalQuest.Stop() ; #DEBUG_LINE_NO:75
    JournalQuest.Start() ; #DEBUG_LINE_NO:76
  EndIf
EndFunction

Int Function CalculateGold(Float BardSkill, Int RewardRank)
  Int[] RewardAmounts = new Int[3] ; #DEBUG_LINE_NO:81
  ; ARR Bards Reborn Tweaks gig retune: base 10/12/18 (was 10/15/25) and renown multiplier 1/2/3/5
  ; (was geometric 1/2/4/8); skill scalar kept at 0.01 -> single-gig ceiling 180 (was 400).
  RewardAmounts[0] = 10 ; #DEBUG_LINE_NO:82
  RewardAmounts[1] = 12 ; #DEBUG_LINE_NO:83
  RewardAmounts[2] = 18 ; #DEBUG_LINE_NO:84
  Int Multiple = 1 ; #DEBUG_LINE_NO:85
  If PlayerREF.HasSpell(_LP_BardExperiencedAbility as Form) ; #DEBUG_LINE_NO:86
    Multiple = 2 ; #DEBUG_LINE_NO:87
  ElseIf PlayerREF.HasSpell(_LP_BardWellKnownAbility as Form) ; #DEBUG_LINE_NO:88
    Multiple = 3 ; #DEBUG_LINE_NO:89
  ElseIf PlayerREF.HasSpell(_LP_BardRenownedAbility as Form) ; #DEBUG_LINE_NO:90
    Multiple = 5 ; #DEBUG_LINE_NO:91
  EndIf
  Int RewardGold = ((RewardAmounts[RewardRank] * Multiple) as Float * (1 as Float + BardSkill * 0.01)) as Int ; #DEBUG_LINE_NO:93
  Return RewardGold ; #DEBUG_LINE_NO:94
EndFunction

Function CheckForNewPerks(Float BardSkill)
  If (PlayerREF.HasSpell(_LP_BardExperiencedAbility as Form) == 0 as Bool) && (PlayerREF.HasSpell(_LP_BardWellKnownAbility as Form) == 0 as Bool) && (PlayerREF.HasSpell(_LP_BardRenownedAbility as Form) == 0 as Bool) ; #DEBUG_LINE_NO:98
    If _LP_BardQuestsCompleted.GetValue() as Int > 14 ; #DEBUG_LINE_NO:99
      PlayerREF.AddSpell(_LP_BardExperiencedAbility, True) ; #DEBUG_LINE_NO:100
    EndIf
  ElseIf (PlayerREF.HasSpell(_LP_BardWellKnownAbility as Form) == 0 as Bool) && (PlayerREF.HasSpell(_LP_BardRenownedAbility as Form) == 0 as Bool) ; #DEBUG_LINE_NO:102
    Int WellKnown = 0 ; #DEBUG_LINE_NO:103
    Int i = 0 ; #DEBUG_LINE_NO:104
    Int NumTaverns = _LP_BardTavernLocations.GetSize() ; #DEBUG_LINE_NO:105
    While i < NumTaverns ; #DEBUG_LINE_NO:106
      If (_LP_BardTavernCounts.GetAt(i) as GlobalVariable).GetValue() as Int >= 1 ; #DEBUG_LINE_NO:107
        WellKnown += 1 ; #DEBUG_LINE_NO:108
      EndIf
      i += 1 ; #DEBUG_LINE_NO:110
    EndWhile
    If WellKnown > 10 ; #DEBUG_LINE_NO:112
      PlayerREF.RemoveSpell(_LP_BardExperiencedAbility) ; #DEBUG_LINE_NO:113
      PlayerREF.AddSpell(_LP_BardWellKnownAbility, True) ; #DEBUG_LINE_NO:114
    EndIf
  ElseIf PlayerREF.HasSpell(_LP_BardWellKnownAbility as Form) == 1 as Bool ; #DEBUG_LINE_NO:116
    If BardSkill >= 100 as Float ; #DEBUG_LINE_NO:117
      PlayerREF.RemoveSpell(_LP_BardWellKnownAbility) ; #DEBUG_LINE_NO:118
      PlayerREF.AddSpell(_LP_BardRenownedAbility, True) ; #DEBUG_LINE_NO:119
    EndIf
  EndIf
EndFunction
