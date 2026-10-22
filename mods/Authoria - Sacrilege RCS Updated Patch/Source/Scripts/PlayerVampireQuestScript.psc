ScriptName PlayerVampireQuestScript extends Quest Conditional

int CurrentAge = 0
spell CurrentSpell
spell RacialSpell

globalvariable Property SQL_Stages_Global_Dominate_IllusionBonus Auto

static Property XMarker Auto

string Property SQL_ActorValue Auto

formlist Property SQL_RacesVampire Auto

formlist Property DLC1CrimeFactions Auto

spell Property SQL_Mortal_Spell_Good_StillHeart_Ab Auto

spell Property SQL_Mortal_Spell_VampiricDrain_Stage4_Deprecated Auto

spell Property SQL_Scaling_Spell_Stage2_Ab Auto

message Property SQL_Help_Hunger Auto

spell Property SQL_Mortal_Spell_Good_Dominate_Ab Auto

globalvariable Property PlayerIsVampire Auto

magiceffect Property DLC1VampireChangeEffect Auto

message Property SQL_Age_Message_AgeTo4 Auto

spell Property VampireCureDisease Auto

globalvariable Property SQL_Mechanics_Global_Age_Threshold_Base Auto

spell Property SQL_Mortal_Spell_SunDamage_Ab_Stage2 Auto

race Property NordRace Auto

spell Property SQL_Mortal_Spell_Age_Ab_Age5_Description Auto

spell Property SQL_Mortal_Spell_Age_Ab_Age2_Description Auto

spell Property SQL_Mortal_Spell_Age_Ab_Age1_Description Auto

idle Property VampireFeedingBedRight Auto

idle Property VampireFeedingBedrollRight Auto

globalvariable Property SQL_Ranks_Global_Positive_110 Auto

spell Property SQL_Stages_Spell_Stage4_Power Auto

race Property CureRace Auto

faction Property VampirePCFaction Auto

spell Property SQL_Mortal_Spell_SunDamage_Ab_Stage3 Auto

spell Property SQL_Mortal_Spell_WeaknessToFire_Ab_Stage2 Auto

globalvariable Property SQL_Ranks_Global_Positive_105 Auto

spell Property SQL_Mortal_Spell_Bad_MockeryOfLife_Ab Auto

imagespacemodifier Property VampireTransformDecreaseISMD Auto

spell Property SQL_Mortal_Spell_Age_Ab_Age4_Description Auto

spell Property SQL_Mortal_Spell_WeaknessToFire_Ab_Stage3 Auto

spell Property SQL_Scaling_Spell_Stage3_Ab Auto

race Property DLC1VampireBeastRace Auto

message Property SQL_Mechanics_Message_VampireFeed Auto

actor Property Player Auto

spell Property SQL_Mortal_Spell_Good_UnderTheIce_Ab Auto

message Property SQL_Mechanics_Message_RaceBroken Auto

Quest Property VC01 Auto

globalvariable Property GameDaysPassed Auto

race Property NordRaceVampire Auto

imagespacemodifier Property VampireTransformIncreaseISMD Auto

globalvariable Property SQL_Mechanics_Global_Age_Threshold Auto

spell Property SQL_Mortal_Spell_VampiricDrain_Stage2_Deprecated Auto

globalvariable Property SQL_Ranks_Global_Negative_025 Auto

spell Property SQL_Stages_Spell_Stage3_Power Auto

magiceffect Property SQL_Racial_Effect_SnowElf_Ab Auto

int Property VampireStatus Auto Conditional

effectshader Property VampireChangeFX Auto

spell Property SQL_Mortal_Spell_WeaknessToFire_Ab_Stage4 Auto

message Property SQL_Mechanics_Message_ScriptsBroken Auto

string Property SQL_ActorValueNegativeHalf Auto

magiceffect Property SQL_Racial_Effect_HighElf_Ab Auto

spell Property SQL_Mortal_Spell_ResistFrost_Ab_Stage1 Auto

spell Property SQL_Mortal_Spell_Power_VampiresSight Auto

spell Property DiseasePorphyricHemophelia Auto

spell Property SQL_Mortal_Spell_Good_NightstalkersStrength_Ab Auto

message Property SQL_Mechanics_Message_VampireProgressionStage3 Auto

string Property SQL_ActorValueNegative Auto

magiceffect Property DLC1VampireChangeFXEffect Auto

float Property LastFeedTime Auto

message Property SQL_Age_Message_AgeTo6 Auto

formlist Property CrimeFactions Auto

message Property SQL_Age_Message_AgeTo2 Auto

formlist Property SQL_Racial Auto

spell Property SQL_Mortal_Spell_SunDamage_Ab_Stage1 Auto

globalvariable Property SQL_Mechanics_Global_Age Auto

spell Property SQL_Mortal_Spell_Age_Ab_Age3_Description Auto

sound Property MagVampireTransform01 Auto

spell Property SQL_Stages_Spell_Stage2_Power Auto

spell Property SQL_Mortal_Spell_WeaknessToFire_Ab_Stage1 Auto

float Property FeedTimer Auto

globalvariable Property VampireFeedReady Auto

spell Property SQL_Mortal_Spell_Power_VampiresSeduction Auto

globalvariable Property SQL_Mechanics_Global_Age_Threshold_Add Auto

globalvariable Property SQL_Ranks_Global_Negative_050 Auto

message Property SQL_Mechanics_Message_VampireProgressionStage4 Auto

magiceffect Property SQL_Racial_Effect_Redguard_Ab Auto

formlist Property DLC1VampireHateFactions Auto

spell Property SQL_Mortal_Spell_VampiricDrain_Stage1 Auto

spell Property SQL_Mortal_Spell_ResistFrost_Ab_Stage2 Auto

spell Property SQL_Mortal_Spell_Bad_Forsaken_Ab Auto

globalvariable Property SQL_Mechanics_Global_AgeToStarveResistMult Auto

spell Property SQL_Mortal_Spell_VampiricDrain_Stage3_Deprecated Auto

spell Property DLC1VampireChange Auto

message Property SQL_Age_Message_AgeTo3 Auto

spell Property SQL_Scaling_Spell_Stage4_Ab Auto

spell Property SQL_Mortal_Spell_Good_FierceHunger_Ab Auto

formlist Property SQL_Races Auto

spell Property SQL_Mortal_Spell_ResistFrost_Ab_Stage3 Auto

spell Property SQL_Mortal_Spell_ResistDisease_Ab Auto

spell Property SQL_Mortal_Spell_SunDamage_Ab_Stage4 Auto

message Property SQL_Age_Message_AgeTo5 Auto

spell Property SQL_Scaling_Spell_Stage1_Ab Auto

spell Property SQL_Mortal_Spell_ResistFrost_Ab_Stage4 Auto

spell Property SQL_Mechanics_Spell_HiddenVampireAbilities_Ab Auto

message Property SQL_Mechanics_Message_VampireProgressionStage2 Auto

Event OnUpdateGameTime()
    SetAgeVariables()
    FeedTimer = GameDaysPassed.value - LastFeedTime
    if game.IsMovementControlsEnabled() && game.IsFightingControlsEnabled() && Player.GetCombatState() == 0 && !Player.HasMagicEffect(DLC1VampireChangeEffect) && !Player.HasMagicEffect(DLC1VampireChangeFXEffect)
        SQL_Help_Hunger.ShowAsHelpMessage("SQL_HungerStage2Event", 5.0, 0, 1)
        Devolve(false)
    endif
    if Player.GetRace() == DLC1VampireBeastRace
        AdvanceAge(Player, 2)
    elseif Player.HasMagicEffect(SQL_Racial_Effect_HighElf_Ab) && VampireStatus == 1
        AdvanceAge(Player, 1.3)
    elseif Player.HasMagicEffect(SQL_Racial_Effect_Redguard_Ab)
        AdvanceAge(Player, 1.15)
    else
        AdvanceAge(Player, 1)
    endif
EndEvent

spell Function SetCurrentSpell(spell akSpell)
    CurrentSpell = akSpell
EndFunction

Function AdvanceAge(actor akPlayer, float afAgeAmount)
    if CurrentAge < 5
        SQL_Mechanics_Global_Age.Mod(afAgeAmount)
        if SQL_Mechanics_Global_Age.GetValue() >= SQL_Mechanics_Global_Age_Threshold.GetValue()
            CurrentAge = CurrentAge + 1
            if CurrentAge == 1
                SQL_Age_Message_AgeTo2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                SetAgeVariables()
                SetAgeAb()
            elseif CurrentAge == 2
                SQL_Age_Message_AgeTo3.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                SetAgeVariables()
                SetAgeAb()
            elseif CurrentAge == 3
                SQL_Age_Message_AgeTo4.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                SetAgeVariables()
                SetAgeAb()
            elseif CurrentAge == 4
                SQL_Age_Message_AgeTo5.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                SetAgeVariables()
                SetAgeAb()
            elseif CurrentAge == 5
                SQL_Age_Message_AgeTo6.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                SetAgeVariables()
                SetAgeAb()
            endif
            if CurrentAge < 5
                SQL_Mechanics_Global_Age.SetValue(0)
                SQL_Mechanics_Global_Age_Threshold.Mod(SQL_Mechanics_Global_Age_Threshold.GetValue() + SQL_Mechanics_Global_Age_Threshold_Add.GetValue())
            else
                SQL_Mechanics_Global_Age.SetValue(SQL_Mechanics_Global_Age_Threshold.GetValue())
            endif
        endif
    endif
EndFunction

Function AddVampireSpells(actor akPlayer)
    Player.AddSpell(SQL_Mortal_Spell_VampiricDrain_Stage1, false)
    Player.AddSpell(SQL_Mortal_Spell_Power_VampiresSight, false)
    Player.AddSpell(SQL_Mortal_Spell_Power_VampiresSeduction, false)
    Player.AddSpell(SQL_Mortal_Spell_Bad_Forsaken_Ab, false)
    Player.AddSpell(SQL_Mortal_Spell_Bad_MockeryOfLife_Ab, false)
    Player.AddSpell(SQL_Mortal_Spell_Good_Dominate_Ab, false)
    Player.AddSpell(SQL_Mortal_Spell_Good_FierceHunger_Ab, false)
    Player.AddSpell(SQL_Mortal_Spell_Good_StillHeart_Ab, false)
    Player.AddSpell(SQL_Mortal_Spell_Good_UnderTheIce_Ab, false)
    Player.AddSpell(SQL_Mechanics_Spell_HiddenVampireAbilities_Ab, false)
    Player.AddSpell(SQL_Mortal_Spell_Good_NightstalkersStrength_Ab, false)
EndFunction

Function VampireCure(actor akPlayer)
    game.IncrementStat("Vampirism Cures", 1)
    UnregisterforUpdateGameTime()
    VampireStatus = 0
    StopHate(Player, true)
    Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage1)
    Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage2)
    Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage3)
    Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage4)
    Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage1)
    Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage2)
    Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage3)
    Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage4)
    Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage1)
    Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage2)
    Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage3)
    Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage4)
    Player.RemoveSpell(SQL_Stages_Spell_Stage2_Power)
    Player.RemoveSpell(SQL_Stages_Spell_Stage3_Power)
    Player.RemoveSpell(SQL_Stages_Spell_Stage4_Power)
    Player.RemoveSpell(SQL_Scaling_Spell_Stage1_Ab)
    Player.RemoveSpell(SQL_Scaling_Spell_Stage2_Ab)
    Player.RemoveSpell(SQL_Scaling_Spell_Stage3_Ab)
    Player.RemoveSpell(SQL_Scaling_Spell_Stage4_Ab)
    Player.RemoveSpell(SQL_Mortal_Spell_VampiricDrain_Stage1)
    Player.RemoveSpell(SQL_Mortal_Spell_VampiricDrain_Stage2_Deprecated)
    Player.RemoveSpell(SQL_Mortal_Spell_VampiricDrain_Stage3_Deprecated)
    Player.RemoveSpell(SQL_Mortal_Spell_VampiricDrain_Stage4_Deprecated)
    Player.RemoveSpell(SQL_Mortal_Spell_Power_VampiresSight)
    Player.RemoveSpell(SQL_Mortal_Spell_Power_VampiresSeduction)
    Player.RemoveSpell(SQL_Mortal_Spell_Bad_Forsaken_Ab)
    Player.RemoveSpell(SQL_Mortal_Spell_Bad_MockeryOfLife_Ab)
    Player.RemoveSpell(SQL_Mortal_Spell_Good_Dominate_Ab)
    Player.RemoveSpell(SQL_Mortal_Spell_Good_FierceHunger_Ab)
    Player.RemoveSpell(SQL_Mortal_Spell_Good_StillHeart_Ab)
    Player.RemoveSpell(SQL_Mortal_Spell_Good_UnderTheIce_Ab)
    Player.RemoveSpell(SQL_Mortal_Spell_Good_NightstalkersStrength_Ab)
    CurrentAge = 0
    Player.SetActorValue(SQL_ActorValue, 0.0)
    Player.SetActorValue(SQL_ActorValueNegative, 0.25)
    SQL_Mechanics_Global_Age_Threshold.SetValue(SQL_Mechanics_Global_Age_Threshold_Base.GetValue())
    SQL_Ranks_Global_Positive_105.SetValue(5)
    SQL_Ranks_Global_Positive_110.SetValue(10)
    SQL_Ranks_Global_Negative_025.SetValue(75)
    SQL_Stages_Global_Dominate_IllusionBonus.SetValue(15)
    if CurrentSpell
        Player.RemoveSpell(CurrentSpell)
        CurrentSpell = None
    endif
    Player.RemoveSpell(SQL_Mechanics_Spell_HiddenVampireAbilities_Ab)
    if !CureRace
        ; RCS: resolve the mortal race from the current (vampire) race via proxy
        Race MortalRace = RaceCompatibility.GetRaceByVampireRace(Player.GetRace())
        if MortalRace != None
            Player.SetRace(MortalRace)
        else
            Player.SetRace(NordRace)
        endif
    else
        Player.SetRace(CureRace)
    endif
    Player.RemoveSpell(RacialSpell)
    PlayerIsVampire.SetValue(0)
    Player.DispelSpell(SQL_Mortal_Spell_Power_VampiresSight)
    Player.RemoveSpell(SQL_Mortal_Spell_Power_VampiresSight)
    Player.SendVampirismStateChanged(false)
    Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age1_Description)
    Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age2_Description)
    Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age3_Description)
    Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age4_Description)
    Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age5_Description)
EndFunction

bool Function Devolve(bool abForceDevolve)
    float RacialThresholdMult = 1.0
    if Player.HasMagicEffect(SQL_Racial_Effect_Redguard_Ab)
        RacialThresholdMult = 1.5
    elseif Player.HasMagicEffect(SQL_Racial_Effect_HighElf_Ab) && VampireStatus == 1
        RacialThresholdMult = 2.0
    endif
    float AgeThresholdMult = 1.0 + CurrentAge * SQL_Mechanics_Global_AgeToStarveResistMult.GetValue()
    float TotalMult = RacialThresholdMult * AgeThresholdMult
    if (FeedTimer >= 3 * TotalMult || abForceDevolve) && VampireStatus == 3 && !Player.HasMagicEffect(SQL_Racial_Effect_SnowElf_Ab)
        VampireFeedReady.SetValue(3)
        SQL_Mechanics_Message_VampireProgressionStage4.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        VampireStatus = 4
        VampireProgression(Player, 4)
        FeedTimer == 3 * RacialThresholdMult
        UnregisterforUpdateGameTime()
    elseif (FeedTimer >= 2 * TotalMult || abForceDevolve) && VampireStatus == 2
        VampireFeedReady.SetValue(2)
        SQL_Mechanics_Message_VampireProgressionStage3.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        VampireStatus = 3
        VampireProgression(Player, 3)
        FeedTimer == 2 * RacialThresholdMult
    elseif (FeedTimer >= 1 * TotalMult || abForceDevolve) && VampireStatus == 1
        VampireFeedReady.SetValue(1)
        SQL_Mechanics_Message_VampireProgressionStage2.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        VampireStatus = 2
        VampireProgression(Player, 2)
        FeedTimer == 1 * RacialThresholdMult
    endif
EndFunction

Function VampireProgression(actor akPlayer, int VampireStage)
    if VampireStage == 2
        VampireTransformIncreaseISMD.applyCrossFade(2.0)
        utility.Wait(2.0)
        imagespacemodifier.removeCrossFade(1.0)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage1)
        Player.AddSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage2, false)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage3)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage4)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage1)
        Player.AddSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage2, false)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage3)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage4)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage1)
        Player.AddSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage2, false)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage3)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage4)
        Player.RemoveSpell(SQL_Stages_Spell_Stage2_Power)
        Player.AddSpell(SQL_Stages_Spell_Stage3_Power, false)
        Player.AddSpell(SQL_Stages_Spell_Stage4_Power, false)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage1_Ab)
        Player.AddSpell(SQL_Scaling_Spell_Stage2_Ab, false)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage3_Ab)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage4_Ab)
    elseif VampireStage == 3
        VampireTransformIncreaseISMD.applyCrossFade(2.0)
        utility.Wait(2.0)
        imagespacemodifier.removeCrossFade(1.0)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage1)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage2)
        Player.AddSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage3, false)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage4)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage1)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage2)
        Player.AddSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage3, false)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage4)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage1)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage2)
        Player.AddSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage3, false)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage4)
        Player.RemoveSpell(SQL_Stages_Spell_Stage2_Power)
        Player.RemoveSpell(SQL_Stages_Spell_Stage3_Power)
        Player.AddSpell(SQL_Stages_Spell_Stage4_Power, false)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage1_Ab)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage2_Ab)
        Player.AddSpell(SQL_Scaling_Spell_Stage3_Ab, false)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage4_Ab)
    elseif VampireStage == 4
        VampireTransformIncreaseISMD.applyCrossFade(2.0)
        utility.Wait(2.0)
        imagespacemodifier.removeCrossFade(1.0)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage1)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage2)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage3)
        Player.AddSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage4, false)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage1)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage2)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage3)
        Player.AddSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage4, false)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage1)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage2)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage3)
        Player.AddSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage4, false)
        Player.RemoveSpell(SQL_Stages_Spell_Stage2_Power)
        Player.RemoveSpell(SQL_Stages_Spell_Stage3_Power)
        Player.RemoveSpell(SQL_Stages_Spell_Stage4_Power)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage1_Ab)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage2_Ab)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage3_Ab)
        Player.AddSpell(SQL_Scaling_Spell_Stage4_Ab, false)
        StartHate(Player)
    elseif VampireStage == 1
        Player.AddSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage1, false)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage2)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage3)
        Player.RemoveSpell(SQL_Mortal_Spell_ResistFrost_Ab_Stage4)
        Player.AddSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage1, false)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage2)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage3)
        Player.RemoveSpell(SQL_Mortal_Spell_WeaknessToFire_Ab_Stage4)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage2)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage3)
        Player.RemoveSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage4)
        Player.AddSpell(SQL_Mortal_Spell_SunDamage_Ab_Stage1, false)
        Player.AddSpell(SQL_Stages_Spell_Stage2_Power, false)
        Player.AddSpell(SQL_Stages_Spell_Stage3_Power, false)
        Player.AddSpell(SQL_Stages_Spell_Stage4_Power, false)
        Player.AddSpell(SQL_Scaling_Spell_Stage1_Ab, false)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage2_Ab)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage3_Ab)
        Player.RemoveSpell(SQL_Scaling_Spell_Stage4_Ab)
    endif
EndFunction

Function VampireChange(actor Target)
    game.DisablePlayerControls(true, true, false, false, false, true, true, false, 0)
    VampireChangeFX.play(Target, -1.0)
    VampireTransformIncreaseISMD.applyCrossFade(2.0)
    objectreference myXmarker = Target.PlaceAtMe(XMarker, 1, false, false)
    MagVampireTransform01.play(myXmarker)
    myXmarker.Disable(false)
    utility.Wait(2.0)
    imagespacemodifier.removeCrossFade(1.0)
    VampireChangeFX.stop(Target)
    race PlayerRace = Target.GetActorBase().GetRace()
    CureRace = PlayerRace
    ; RCS: resolve the vampire race via Race Compatibility proxy so custom races work
    Race VampireRace = RaceCompatibility.GetVampireRaceByRace(PlayerRace)
    if VampireRace != None
        Target.SetRace(VampireRace)
        ; find the matching racial vampire ability by proxy-matching SQL_Races
        int RaceID = 0
        int Size = SQL_Races.GetSize()
        while RaceID < Size
            if RaceCompatibility.GetIsRaceByProxy(PlayerRace, SQL_Races.GetAt(RaceID) as Race)
                RacialSpell = (SQL_Racial.GetAt(RaceID) as spell)
                Target.AddSpell(RacialSpell, false)
                RaceID = Size
            else
                RaceID = RaceID + 1
            endif
        endwhile
    else
        SQL_Mechanics_Message_RaceBroken.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        Target.SetRace(NordRaceVampire)
    endif
    VampireCureDisease.Cast(Target, None)
    VampireStatus = 1
    VampireProgression(Player, 1)
    AddVampireSpells(Player)
    RegisterForUpdateGameTime(1.0)
    LastFeedTime = GameDaysPassed.value
    PlayerIsVampire.SetValue(1)
    utility.Wait(1.0)
    game.EnablePlayerControls(true, true, true, true, true, true, true, true, 0)
    if VC01.GetStageDone(200) == 1
        VC01.SetStage(25)
    endif
    CurrentAge = 0
    Player.SetActorValue(SQL_ActorValue, 0.0)
    Player.SetActorValue(SQL_ActorValueNegative, 0.25)
    SQL_Mechanics_Global_Age_Threshold.SetValue(SQL_Mechanics_Global_Age_Threshold_Base.GetValue())
    SQL_Ranks_Global_Positive_105.SetValue(5)
    SQL_Ranks_Global_Positive_110.SetValue(10)
    SQL_Ranks_Global_Negative_025.SetValue(75)
    Player.SendVampirismStateChanged(true)
    SetAgeVariables()
    SetAgeAb()
EndFunction

Function VampireFeedBed()
    game.GetPlayer().PlayIdle(VampireFeedingBedRight)
EndFunction

int Function TestIntegrity()
    return 777
EndFunction

Function StopHate(actor akPlayer, bool akForceStopHate)
    if !(VampireStatus == 4) || akForceStopHate == true
        Player.RemoveFromFaction(VampirePCFaction)
        Player.SetAttackActorOnSight(false)
        int i = 0
        while i < DLC1VampireHateFactions.GetSize()
            (DLC1VampireHateFactions.GetAt(i) as faction).SetPlayerEnemy(false)
            i = i + 1
        endwhile
    endif
EndFunction

Function VampireFeedBedRoll()
    game.GetPlayer().PlayIdle(VampireFeedingBedrollRight)
EndFunction

Function StartHate(actor akPlayer)
    Player.AddtoFaction(VampirePCFaction)
    int i = 0
    while i < DLC1VampireHateFactions.GetSize()
        (DLC1VampireHateFactions.GetAt(i) as faction).SetPlayerEnemy(true)
        i = i + 1
    endwhile
EndFunction

Function VampireFeed()
    VampireTransformDecreaseISMD.applyCrossFade(2.0)
    utility.Wait(2.0)
    imagespacemodifier.removeCrossFade(1.0)
    game.IncrementStat("Necks Bitten", 1)
    SQL_Mechanics_Message_VampireFeed.Show(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    VampireFeedReady.SetValue(0)
    LastFeedTime = GameDaysPassed.value
    VampireStatus = 1
    VampireProgression(Player, 1)
    StopHate(Player, false)
    UnregisterforUpdateGameTime()
    RegisterForUpdateGameTime(1.0)
EndFunction

Function SetAgeVariables()
    if CurrentAge == 0
        Player.SetActorValue(SQL_ActorValue, 0.0)
        Player.SetActorValue(SQL_ActorValueNegative, 0.25)
        Player.SetActorValue(SQL_ActorValueNegativeHalf, 0.5)
        SQL_Ranks_Global_Positive_105.SetValue(5)
        SQL_Ranks_Global_Positive_110.SetValue(10)
        SQL_Ranks_Global_Negative_025.SetValue(75)
        SQL_Ranks_Global_Negative_050.SetValue(50)
        SQL_Stages_Global_Dominate_IllusionBonus.SetValue(15)
    elseif CurrentAge == 1
        Player.SetActorValue(SQL_ActorValue, 100.0)
        Player.SetActorValue(SQL_ActorValueNegative, 0.35)
        Player.SetActorValue(SQL_ActorValueNegativeHalf, 0.55)
        SQL_Ranks_Global_Positive_105.SetValue(10)
        SQL_Ranks_Global_Positive_110.SetValue(20)
        SQL_Ranks_Global_Negative_025.SetValue(65)
        SQL_Ranks_Global_Negative_050.SetValue(45)
        SQL_Stages_Global_Dominate_IllusionBonus.SetValue(20)
    elseif CurrentAge == 2
        Player.SetActorValue(SQL_ActorValue, 200.0)
        Player.SetActorValue(SQL_ActorValueNegative, 0.45)
        Player.SetActorValue(SQL_ActorValueNegativeHalf, 0.6)
        SQL_Ranks_Global_Positive_105.SetValue(15)
        SQL_Ranks_Global_Positive_110.SetValue(30)
        SQL_Ranks_Global_Negative_025.SetValue(55)
        SQL_Ranks_Global_Negative_050.SetValue(40)
        SQL_Stages_Global_Dominate_IllusionBonus.SetValue(25)
    elseif CurrentAge == 3
        Player.SetActorValue(SQL_ActorValue, 300.0)
        Player.SetActorValue(SQL_ActorValueNegative, 0.55)
        Player.SetActorValue(SQL_ActorValueNegativeHalf, 0.65)
        SQL_Ranks_Global_Positive_105.SetValue(20)
        SQL_Ranks_Global_Positive_110.SetValue(40)
        SQL_Ranks_Global_Negative_025.SetValue(45)
        SQL_Ranks_Global_Negative_050.SetValue(35)
        SQL_Stages_Global_Dominate_IllusionBonus.SetValue(30)
    elseif CurrentAge == 4
        Player.SetActorValue(SQL_ActorValue, 400.0)
        Player.SetActorValue(SQL_ActorValueNegative, 0.65)
        Player.SetActorValue(SQL_ActorValueNegativeHalf, 0.7)
        SQL_Ranks_Global_Positive_105.SetValue(25)
        SQL_Ranks_Global_Positive_110.SetValue(50)
        SQL_Ranks_Global_Negative_025.SetValue(35)
        SQL_Ranks_Global_Negative_050.SetValue(30)
        SQL_Stages_Global_Dominate_IllusionBonus.SetValue(35)
    elseif CurrentAge == 5
        Player.SetActorValue(SQL_ActorValue, 500.0)
        Player.SetActorValue(SQL_ActorValueNegative, 0.75)
        Player.SetActorValue(SQL_ActorValueNegativeHalf, 0.75)
        SQL_Ranks_Global_Positive_105.SetValue(30)
        SQL_Ranks_Global_Positive_110.SetValue(60)
        SQL_Ranks_Global_Negative_025.SetValue(25)
        SQL_Ranks_Global_Negative_050.SetValue(25)
        SQL_Stages_Global_Dominate_IllusionBonus.SetValue(40)
    endif
EndFunction

Function SetAgeAb()
    if CurrentAge == 0
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age1_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age2_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age3_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age4_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age5_Description)
    elseif CurrentAge == 1
        Player.AddSpell(SQL_Mortal_Spell_Age_Ab_Age1_Description, false)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age2_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age3_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age4_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age5_Description)
    elseif CurrentAge == 2
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age1_Description)
        Player.AddSpell(SQL_Mortal_Spell_Age_Ab_Age2_Description, false)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age3_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age4_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age5_Description)
    elseif CurrentAge == 3
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age1_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age2_Description)
        Player.AddSpell(SQL_Mortal_Spell_Age_Ab_Age3_Description, false)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age4_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age5_Description)
    elseif CurrentAge == 4
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age1_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age2_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age3_Description)
        Player.AddSpell(SQL_Mortal_Spell_Age_Ab_Age4_Description, false)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age5_Description)
    elseif CurrentAge == 5
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age1_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age2_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age3_Description)
        Player.RemoveSpell(SQL_Mortal_Spell_Age_Ab_Age4_Description)
        Player.AddSpell(SQL_Mortal_Spell_Age_Ab_Age5_Description, false)
    endif
EndFunction

spell Function GetCurrentSpell()
    return CurrentSpell
EndFunction

