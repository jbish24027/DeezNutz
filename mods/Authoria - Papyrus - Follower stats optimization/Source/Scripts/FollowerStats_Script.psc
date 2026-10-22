Scriptname FollowerStats_Script extends Quest

Import PO3_SKSEFunctions

; refs
Faction Property PotentialHireling Auto
Faction Property CurrentHireling Auto
Faction Property PotentialFollowerFaction Auto
Faction Property CurrentFollowerFaction Auto
FormList Property FollowerStats_BlockList Auto
FormList Property FollowerStats_CustomActorsList Auto
FormList Property FollowerStats_PerksList Auto
FormList Property FollowerStats_SpellsList Auto
FormList Property FollowerStats_EffectsList Auto
FollowerStats_MCM Property Config Auto
Spell Property FollowerStats_DialogCatcherCloakAb Auto
String[] Property ResistAVs Auto

; config
String[] Property AVNames Auto
Int Property iMaxDisplayed Auto
Int Property iMinSkillValue Auto

Bool Property bStatsOpened Auto Hidden
Actor Property DialogTarget Auto Hidden

Int[] AVs ; skill AVs of currentActor
Bool bProcessing

Event OnInit()
    Init()
EndEvent

Function Init()
    UpdateConfig()
    Inject()

    If Config.iDisplay == 3
        UnregisterForAllMenus()
    Else
        RegisterForMenu("Dialogue Menu")
        ; these are the various menus that can be opened while dialog menu is active
        RegisterForMenu("BarterMenu")
        RegisterForMenu("ContainerMenu")
        RegisterForMenu("Crafting Menu")
        RegisterForMenu("InventoryMenu")
        RegisterForMenu("MagicMenu")
        RegisterForMenu("Training Menu")
        RegisterForMenu("GiftMenu")
    EndIf

    If Config.iHotkey > 0
        RegisterForKey(Config.iHotkey)
    Else
        UnregisterForAllKeys()
    EndIf
EndFunction

Event OnMenuOpen(String asMenu)
    If asMenu == "Dialogue Menu"
        Actor currentActor = GetPlayerDialogTarget()
        If ! currentActor || FollowerStats_BlockList.HasForm(currentActor)
            Return
        EndIf

        If ShouldDisplayStats(currentActor)
            bStatsOpened = True
            ShowForActor(currentActor)
        EndIf
    ElseIf bStatsOpened
        UI.Invoke("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats.Menu_mc.hide")
    EndIf
EndEvent

Event OnKeyUp(Int KeyCode, Float HoldTime)
    If UI.IsTextInputEnabled()
        Return
    EndIf

    Actor currentActor = Game.GetCurrentCrosshairRef() as Actor
    If currentActor
        bStatsOpened = True
        ShowForActor(currentActor)
    ElseIf bStatsOpened
        UI.Invoke("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats.Menu_mc.close")
        bStatsOpened = False
    EndIf
EndEvent

Function ShowForActor(Actor akActor)
    If bProcessing || ! akActor
        Return
    EndIf
    bProcessing = True
    UI.Invoke("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats.Menu_mc.close")
    UI.InvokeString("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats.Menu_mc.setData", Serialize(akActor))
    bProcessing = False
EndFunction

; this is janky af
Actor Function GetPlayerDialogTarget()
    ; IsInDialogueWithPlayer() always fails for commanded actors;
    ; the DialogTarget here is set from talkToSummonsPerkScript script
    If DialogTarget
        Return DialogTarget
    EndIf

    Actor currentActor = Game.GetCurrentCrosshairRef() as Actor
    If currentActor
        If currentActor.IsInDialogueWithPlayer()
            Return currentActor
        EndIf
    EndIf

    currentActor = None
    If FollowerStats_DialogCatcherCloakAb
        FollowerStats_DialogCatcherCloakAb.Cast(Game.GetPlayer())
        Utility.Wait(0.2) ; wait for FollowerStats_DialogCatcherHitScript to fill DialogTarget
        If DialogTarget
            If DialogTarget.IsInDialogueWithPlayer()
                currentActor = DialogTarget
            EndIf
        EndIf
    EndIf

    Return currentActor
EndFunction

Event OnMenuClose(String asMenu)
    If asMenu == "Dialogue Menu"
        bStatsOpened = False
        DialogTarget = None
        UI.Invoke("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats.Menu_mc.close")
    ElseIf bStatsOpened
        UI.Invoke("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats.Menu_mc.show")
    EndIf
EndEvent

Bool Function ShouldDisplayStats(Actor akActor)
    If akActor.IsCommandedActor()
        Return Config.bSummons
    ElseIf Config.iDisplay == 0
        Return IsPotentialFollower(akActor) && ! IsRecruited(akActor)
    ElseIf Config.iDisplay == 1
        Return IsPotentialFollower(akActor)
    Else
        Return True
    EndIf
EndFunction

Function Inject()
    If ! UI.GetBool("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats._visible")
        string[] args = new string[2]
        args[0] = "FollowerStats"
        args[1] = Utility.RandomInt(2000, 4000)
        UI.InvokeStringA("HUD Menu", "_root.HUDMovieBaseInstance.createEmptyMovieClip", args)
        UI.InvokeString("HUD Menu", "_root.HUDMovieBaseInstance.FollowerStats.loadMovie", "followerstats_inject.swf")
    EndIf
EndFunction

Bool Function IsPotentialFollower(Actor akActor)
    Return akActor.IsInFaction(PotentialHireling) || akActor.IsInFaction(PotentialFollowerFaction) || FollowerStats_CustomActorsList.HasForm(akActor) || FollowerStats_CustomActorsList.HasForm(akActor.GetActorBase())
EndFunction

Bool Function IsRecruited(Actor akActor)
    Return akActor.IsPlayerTeammate()
EndFunction

String Function Serialize(Actor akActor)
    String blockMargin = Config.iBlockMargin
    String inlineMargin = Config.iInlineMargin

    Int i = 0
    If Config.bShowResists
        While i < ResistAVs.Length
            inlineMargin += "," + (akActor.GetAV(ResistAVs[i]) as Int)
            i += 1
        EndWhile
    EndIf

    ; Active Effects is lumped up with blockMargin data, reason:
    ; gradual degradation for UI skin mods that have overwritten followerstats_inject.swf
    i = FollowerStats_EffectsList.GetSize()
    While i != 0
        i -= 1
        MagicEffect thisEffect = FollowerStats_EffectsList.GetAt(i) as MagicEffect
        If akActor.HasMagicEffect(thisEffect)
            blockMargin += "," + PO3_SKSEFunctions.GetFormEditorId(thisEffect)
        EndIf
    EndWhile

    String result = Config.iScale + "|" + Config.iPosition + "|" + blockMargin + "|" + inlineMargin + "|" + akActor.GetBaseActorValue("Health") as Int + "|" + akActor.GetBaseActorValue("Magicka") as Int + "|" + akActor.GetBaseActorValue("Stamina") as Int + "|" + akActor.GetLevel() + "|"

    ; perks
    If FollowerStats_PerksList.GetSize()
        Form[] actorPerks = GetSpecialPerks(akActor.GetActorBase())
        i = actorPerks.Length
        While i != 0
            i -= 1
            result += PO3_SKSEFunctions.GetFormEditorId(actorPerks[i]) + "|"
        EndWhile
    EndIf

    ; skills
    If ! Config.bHideSkills
        i = 0
        AVs = new Int[18]
        While i < AVNames.Length
            AVs[i] = akActor.GetAV(AVNames[i]) as Int
            i += 1
        EndWhile

        Int[] highestAVs = Utility.CreateIntArray(iMaxDisplayed, -1)
        i = 0
        Bool bBreak
        While i < highestAVs.Length && bBreak == False
            Int index = GetHighestArrayValue(highestAVs)
            If index == -1
                bBreak = True
            Else
                highestAVs[i] = index
                result += index + "/" + AVs[index] + "|"
            EndIf
            i += 1
        EndWhile
    EndIf

    ; spells
    i = FollowerStats_SpellsList.GetSize()
    While i != 0
        i -= 1
        Spell thisSpell = FollowerStats_SpellsList.GetAt(i) as Spell
        If akActor.HasSpell(thisSpell)
            result += PO3_SKSEFunctions.GetFormEditorId(thisSpell) + "|"
        EndIf
    EndWhile

    Return result
EndFunction

Form[] Function GetSpecialPerks(ActorBase akBase)
    Form[] result
    Int i = PO3_SKSEFunctions.GetPerkCount(akBase)
    While i != 0
        i -= 1
        Perk currentPerk = PO3_SKSEFunctions.GetNthPerk(akBase, i)
        If FollowerStats_PerksList.HasForm(currentPerk)
            If ! result
                result = new Form[1]
                result[0] = currentPerk
            Else
                result = Utility.ResizeFormArray(result, result.Length + 1, currentPerk)
            EndIf
        EndIf
    EndWhile

    Return result
EndFunction

Int Function GetHighestArrayValue(Int[] Excludes)
    Int iHighestIndex = -1
    Int iCurrentHighestValue
    Int i
    While i < AVs.Length
        If AVs[i] > iMinSkillValue && AVs[i] >= iCurrentHighestValue && Excludes.Find(i) == -1
            iHighestIndex = i
            iCurrentHighestValue = AVs[i]
        EndIf
        i += 1
    EndWhile
    Return iHighestIndex
EndFunction

Function UpdateConfig()
    Config = (Self as Quest) as FollowerStats_MCM
    Config.UpdateSettings()
EndFunction
