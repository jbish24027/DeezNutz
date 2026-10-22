Scriptname ISE_MainQuestScript extends Quest  
OsexIntegrationMain property ostim auto
RaceMenuPluginXPMSE Property XPMSE Auto
SOS_API property SOSapi auto


actor[] property FemaleActorsInScene auto
actor[] property ActorsInScene auto
string[] property RaceGrpNames auto
string property Key_OrgasmTimes = "ISE_CumTimes" auto
bool Property isUsingSOS Auto

;Player body parts length
;Used to store and get reset for scaling back after ostim scene
float[] property CachedPlayerLimbsLength auto

Event OnInit()
    ConsoleUtil.PrintMessage("ISE_MainQuestScript: OnInit")

    UnRegisterAllEvents()
    RegisterAllEvents()

    ;Referencing scritps
    MCM_UpdateMod(false)
    ;Self check
    ModSelfCheck()

EndEvent

Event OnLoadGameGlobal()
    UnRegisterAllEvents()
    RegisterAllEvents()

    ;Self check
    ModSelfCheck()
   
EndEvent

Event OStimStart(String EventName, String sceneId, Float index, Form Sender)
    ;Auto adjust player limbs length
    If (ostim.IsPlayerInvolved() && isLimbsAdjusterEnabled())
        ScalePlayerLimbsLengthToOne()
    EndIf

    ;Get actors data
    FemaleActorsInScene = papyrusUtil.ResizeActorArray(FemaleActorsInScene, 0)
    ActorsInScene = OThread.GetActors(0)

    int i = ActorsInScene.Length
    while i
		i -= 1
        if ostim.AppearsFemale(ActorsInScene[i])
            FemaleActorsInScene = papyrusUtil.PushActor(FemaleActorsInScene, ActorsInScene[i])
        Endif
	endWhile

    ;Reset cum times
    int FemIndex = FemaleActorsInScene.Length
    While FemIndex
        FemIndex -= 1
        StorageUtil.UnsetIntValue(FemaleActorsInScene[FemIndex], Key_OrgasmTimes)
    EndWhile

    RegisterForModEvent("ostim_scenechanged", "OStimSceneChanged")
    RegisterForModEvent("ostim_end", "OStimEnd")
	RegisterForModEvent("ostim_orgasm", "OstimOrgasm")
EndEvent


Event OStimSceneChanged(String EventName, String sceneId, Float index, Form Sender)
    ResetExpressionForAllFemale()

    int j = ActorsInScene.Length
    ;Debug.notification(OMetadata.GetActionTypes(sceneId))
    ;---------------------------------------------------------Blowjob-----------------------------------------------------------------------------
    if OMetadata.FindAction(sceneId, "blowjob") > -1
        float DickSize
        While j
            j -= 1
            ;Find current actor if is in BJ action
            int ActionID = OMetadata.FindActionForActor(sceneId, j, "blowjob") 

            if ActionID != -1 ; If this actor is giving a blowjob
                Actor Giver = OStim.GetActor(OMetadata.GetActionActor(sceneId, ActionID))
                Actor Receiver = OStim.GetActor(OMetadata.GetActionTarget(sceneId, ActionID))
                If (isUsingSOS)
                    DickSize = SOSapi.GetSize(Receiver)
                else
                    int Raceindex = RaceGrpNames.Find(Receiver.GetRace().GetName())
                    if (Raceindex != -1)
                        DickSize = TNG_PapyrusUtil.GetRaceGrpMult(Raceindex)
                        ;Debug.MessageBox("Dick Size\nRaceMorph: " + DickSize + "Addon: " + TNG_PapyrusUtil.GetRaceGrpAddn(Raceindex))
                    Else
                        Debug.notification("Can't find " + Receiver.GetRace().GetName() + " in Race List, pls register it from MCM")
                    Endif
                EndIf

                ;Debug.MessageBox(Giver.GetDisplayName() + " is giving a blowjob!" + "\nDick Size : " + DickSize)

                SRApplyBJExpression(Giver, DickSize)
            Endif
        EndWhile
        ;--------------------------------------------------Kissing Expression-------------------------------------------------
    ElseIf (OMetadata.FindAction(sceneId, "kissing") > -1)
        While j
            j -= 1
            ;kissing is two size, find the female actor
            Actor CurActor = ostim.GetActor(j)
            If (ostim.AppearsFemale(CurActor))
                MuFacialExpressionExtended.SetExpressionByName(CurActor, "Kiss", 100)
            EndIf
        EndWhile

    Elseif (ContainKeyword(Ometadata.GetActionTypes(sceneId), "kissing"))
        int ActionID = GetActionIDByKeyword(sceneId, "kissing")
        
        If (ActionID != -1)
            Actor Giver = ostim.GetActor(OMetadata.GetActionActor(sceneId, ActionID))
            If (ostim.AppearsFemale(Giver))
                MuFacialExpressionExtended.SetExpressionByName(Giver, "Kiss", 100)
                ;Debug.MessageBox("Playing a licking expression on " + Giver.GetDisplayName())
            EndIf
        EndIf
    Elseif (OMetadata.FindAction(sceneId, "suckingnipple") > -1)
        int ActionID = GetActionIDByKeyword(sceneId, "suckingnipple")
        If (ActionID != -1)
            Actor Giver = ostim.GetActor(OMetadata.GetActionActor(sceneId, ActionID))
            If (ostim.AppearsFemale(Giver))
                MuFacialExpressionExtended.SetExpressionByName(Giver, "Kiss", 100)
                MuFacialExpressionExtended.SetExpressionByName(Giver, "Puckering_Lips", 50)
                debug.MessageBox("Playing puckering lips expression on " + Giver.GetDisplayName())
            EndIf
        EndIf
    ;--------------------------------------------------Licking---------------------------------------------------------------------------------
    Elseif (ContainKeyword(OmetaData.GetActionTypes(sceneId), "rimjob") || ContainKeyword(OmetaData.GetActionTypes(sceneId), "cunnilingus"))
        int ActionID = GetActionIDByKeyword(sceneId, "rimjob")
        If (ActionID == -1)
            ActionID = GetActionIDByKeyword(sceneId, "cunnilingus")
        EndIf
        If (ActionID != -1)
            Actor Giver = ostim.GetActor(OMetadata.GetActionActor(sceneId, ActionID))
            If (ostim.AppearsFemale(Giver))
                Utility.Wait(0.5)
                MuFacialExpressionExtended.SetExpressionByName(Giver, "Kiss", 50)
                MuFacialExpressionExtended.SetExpressionByName(Giver, "Lick", 100)
                ;Debug.MessageBox("Playing rimjob expression on " + Giver.GetDisplayName())
            EndIf
        EndIf
    ElseIf (ContainKeyword(Ometadata.GetActionTypes(sceneId), "licking"))
        while j
            j -= 1
            int ActionID = GetActionIDByKeyword(sceneId, "licking")
            If (ActionID != -1)
                Actor Giver = ostim.GetActor(OMetadata.GetActionActor(sceneId, ActionID))
                Actor Receiver = ostim.GetActor(OMetadata.GetActionTarget(sceneId, ActionID))
                If (ostim.AppearsFemale(Giver))
                    Utility.Wait(0.25)
                    MuFacialExpressionExtended.SetExpressionByName(Giver, "Lick", 100)
                    ;Debug.MessageBox("Playing a licking expression on " + Giver.GetDisplayName())
                EndIf
                If (ostim.AppearsFemale(Receiver))
                    MuFacialExpressionExtended.SetExpressionByName(Receiver, "Tired", 100)
                    ;Debug.MessageBox("Playing a licking expression on " + Receiver.GetDisplayName())
                EndIf
            EndIf
        EndWhile
        ;-------------------------------------------------Vaginal & Anal Sex-------------------------------------------------------------------
    Elseif OMetadata.FindAction(sceneId, "vaginalsex") > -1 || OMetadata.FindAction(sceneId, "analsex") > -1
        float DickSize
        while j
            j -= 1
            int ActionID = OMetadata.FindActionForTarget(sceneId, j, "vaginalsex")
            If (ActionID == -1)
                ActionID = OMetadata.FindActionForTarget(sceneId, j, "analsex")
            EndIf

            If (ActionID != -1)
                Actor Giver = OStim.GetActor(OMetadata.GetActionActor(sceneId, ActionID))
                Actor Receiver = OStim.GetActor(OMetadata.GetActionTarget(sceneId, ActionID))

                ;Get big dick expression
                int BigDExpMult

                If (isUsingSOS)
                    DickSize = SOSapi.GetSize(Giver)
                    BigDExpMult = ((DickSize - 4) * 20) as int
                else
                    int Raceindex = RaceGrpNames.Find(Giver.GetRace().GetName())
                    if (Raceindex != -1)
                        DickSize = TNG_PapyrusUtil.GetRaceGrpMult(Raceindex)
                        BigDExpMult = ((DickSize - 1) * 200) as int
                        ;Debug.MessageBox("Dick Size\nRaceMorph: " + DickSize + "Addon: " + TNG_PapyrusUtil.GetRaceGrpAddn(Raceindex))
                    Else
                        Debug.notification("Can't find " + Giver.GetRace().GetName() + " in Race List, pls register it from MCM")
                    Endif
                EndIf

                ;Get cum face expression
                int CumExpMult = storageutil.GetIntValue(Receiver, Key_OrgasmTimes) * 50

                ;scaling when added up exceed from 100
                If ((CumExpMult + BigDExpMult) > 100 && CumExpMult != 0 && BigDExpMult != 0)
                    float pA = BigDExpMult as float / (BigDExpMult + CumExpMult) as float
                    float pB = CumExpMult as float / (BigDExpMult + CumExpMult) as float

                    BigDExpMult = (BigDExpMult * pA) as int
                    CumExpMult = 100 - BigDExpMult

                    ;Debug.MessageBox("BigD scaler: " + pA +"   CumExp scaler: " + pB + "\nRevaluated mult\n: Cum: " + CumExpMult + " to " + (CumExpMult * pB) as int + "\n BigD: " + BigDExpMult + " to " + (BigDExpMult * pA) as int)
                EndIf

                SRApplyInnerSexExpresion(Receiver, CumExpMult, BigDExpMult)
                EndIf
        EndWhile
    endif
EndEvent

Event OnKeyDown(int KeyPress)
    if KeyPress == 34
        If (XPMSE)
            ResetPlayerLimbsLength()
        else
            Debug.MessageBox("XPMSE not referenced!")
        EndIf
    Elseif KeyPress == 35
        If (XPMSE)
            ScalePlayerLimbsLengthToOne()
        EndIf
    Endif
EndEvent

Event OstimOrgasm(string eventName, string strArg, float numArg, Form sender)
    actor CumedActor = ostim.GetMostRecentOrgasmedActor()
    int CumTimes = storageutil.GetIntValue(CumedActor, Key_OrgasmTimes)

    if (storageutil.GetIntValue(CumedActor, Key_OrgasmTimes) == 0)
        StorageUtil.SetIntValue(CumedActor, Key_OrgasmTimes, 1)
    Endif

    CumTimes += 1
    StorageUtil.SetIntValue(CumedActor, Key_OrgasmTimes, CumTimes)
    ;Debug.notification(CumedActor.GetDisplayName() + "'s cum time: " + CumTimes)
EndEvent

Event OStimEnd(String EventName, String sceneId, Float index, Form Sender)
    ;Auto adjust player limbs length
    If (ostim.IsPlayerInvolved() && isLimbsAdjusterEnabled())
        ResetPlayerLimbsLength()
    EndIf

    ResetExpressionForAllFemale()
    FemaleActorsInScene = papyrusUtil.ResizeActorArray(FemaleActorsInScene, 0)
    ActorsInScene = papyrusUtil.ResizeActorArray(ActorsInScene, 0)
    
    UnregisterForModEvent("ostim_scenechanged")
    UnregisterForModEvent("ostim_end")
	UnregisterForModEvent("ostim_orgasm")
EndEvent
;--------------------------------------Expression functions--------------------------------------
Function SRApplyBJExpression(Actor akActor, float DickSize)
    ;Debug.Notification("SRApplyBJExpression")
    int multiplier
    int smallDickMultiplier
    int BigDickMultiplier

    ;Remap multipliers
    if isUsingSOS
        ;SOS settings
        ;Base stretch for size: 1 ~ 6
        ;Large stretch for size: 7~10, but not as accurated as base former

        multiplier = ((DickSize - 1) * 20) as int

        if DickSize > 6
            BigDickMultiplier = ((DickSize - 6) * 25) as int
        Endif
    Else
        ;TNG settings
        ;Support stretch for size 1 ~ 1.5s
        If (DickSize > 1)
            multiplier = ((DickSize - 1) * 200) as int
            BigDickMultiplier = (((DickSize - 1.5)) * 300) as int
        Else
            smallDickMultiplier = ((1 - DickSize) * 200) as int
        EndIf
    Endif


    ;Clamping values
    If (multiplier > 100)
        multiplier = 100
    EndIf
    If (BigDickMultiplier > 100)
        BigDickMultiplier = 100
    EndIf
    Utility.Wait(0.25)

    ;Apply expressions
    ;Basic expressions for default size 1
    MuFacialExpressionExtended.SetExpressionByName(akActor, "Sucked_Cheeks", 100 - multiplier)
    MuFacialExpressionExtended.SetExpressionByName(akActor, "Kiss", 100)
	MuFacialExpressionExtended.SetExpressionByName(akActor, "ChJSh", 30)
    MuFacialExpressionExtended.SetExpressionByName(akActor, "Eyes_relaxed", 60)
    MuFacialExpressionExtended.SetExpressionByName(akActor, "Puckering_Lips", multiplier - 33)

    If (isUsingSOS)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "BJ_SOS_Size1", 100)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "BJ_SOS_Stretch", multiplier)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "BJ_SOS_Stretch_Large", BigDickMultiplier)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Stress", BigDickMultiplier - 33)
    Else
        MuFacialExpressionExtended.SetExpressionByName(akActor, "BJ_TNG_Size1", 100)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "BJ_TNG_Stretch", multiplier)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "BJ_TNG_Stretch_Small", smallDickMultiplier)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "BJ_SOS_Stretch_Large", BigDickMultiplier)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Stress", BigDickMultiplier - 33)
    EndIf
    
    ;Debug.MessageBox(akActor.GetDisplayName() + " is giving a blowjob!" + "\nDick Size : " + DickSize + "\nMultiplier: " + multiplier + "\nBig Dick Multiplier: " + BigDickMultiplier)
EndFunction

Function SRApplyInnerSexExpresion(Actor akActor, int CumExpMult, int BigDExpMult)

    ;Random expression
    int CumExpression = OSANative.RandomInt(0, 2)
    int BigDickExpression = OSANative.RandomInt(0, 3)
    Utility.Wait(0.25)
    
    ;-------------------------------------------------------CUM FACE---------------------------------------------------------------------
    If (CumExpression == 0)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Ahegao", CumExpMult)
    ElseIf (CumExpression == 1)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Happy_surprise", CumExpMult)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Small_smile", CumExpMult)
    ElseIf (CumExpression == 2)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Tired", CumExpMult)
    EndIf
    MuFacialExpressionExtended.SetExpressionByName(akActor, "LookUp", CumExpMult)

    ;-------------------------------------------------------Big Dick---------------------------------------------------------------------
    If (BigDickExpression == 0)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Stress", (BigDExpMult * 0.5) as int)
    ElseIf (BigDickExpression == 1)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Biting_lips_2", (BigDExpMult * 0.66) as int)
    ElseIf (BigDickExpression == 2)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "Skeptical", (BigDExpMult * 0.66) as int)
    ElseIf (BigDickExpression == 3)
        MuFacialExpressionExtended.SetExpressionByName(akActor, "DialogueSurprised", BigDExpMult)
    EndIf
    MuFacialExpressionExtended.SetExpressionByName(akActor, "Forehead Animation wrinkles", (BigDExpMult * 0.5) as int)

    ;Debug.MessageBox(akActor.GetDisplayName() + " is receiving a inner sex! \nCumexp" +  CumExpression + ": " + CumExpMult + "\nBigDexp" + BigDickExpression + ": " + BigDExpMult + "\nCum times: " + storageutil.GetIntValue(akActor, Key_OrgasmTimes))
           
EndFunction

Function SRResetAllExpression(Actor akActor)
    MuFacialExpressionExtended.RevertExpression(akActor)
EndFunction

Function ResetExpressionForAllFemale()
    int i = FemaleActorsInScene.Length
    While i
        i -= 1
        SRResetAllExpression(FemaleActorsInScene[i])
    EndWhile
EndFunction



;-------------------------------------Register begins-------------------------------------
Function RegisterAllEvents()
    RegisterForModEvent("ostim_start", "OStimStart")
EndFunction

Function UnRegisterAllEvents()
    UnRegisterForModEvent("ostim_start")
EndFunction

Function RegisterRaceGrp()
    RaceGrpNames = TNG_PapyrusUtil.GetRaceGrpNames()
    int len = RaceGrpNames.Length
    int i
    while i < len
        String CurString = RaceGrpNames[i]
        int SpliterIndex = stringutil.Find(CurString, ":")
        RaceGrpNames[i] = Stringutil.Substring(CurString, SpliterIndex + 1, stringutil.GetLength(CurString) - SpliterIndex)
        ConsoleUtil.PrintMessage(RaceGrpNames[i])
        i += 1
    EndWhile
EndFunction

;------------------------------------Utils-------------------------------------------------
bool Function ContainKeyword(string[] ActionList, string inkeyword, string excluded = "")
    int index = ActionList.Length
    While (index)
        index -= 1
        int KywIndex = StringUtil.Find(ActionList[index], inkeyword)
        If (KywIndex != -1)
            If (excluded != "")
                string ThisString = StringUtil.Substring(ActionList[index], KywIndex, StringUtil.GetLength(inkeyword))
                If (ThisString != excluded)
                    return true
                EndIf
            else
                return true
            EndIf
        EndIf
    EndWhile
EndFunction

int Function GetActionIDByKeyword(string sceneId, string inkeyword)
    string[] Actions = OMetadata.GetActionTypes(sceneId)
    int ActionIndex = Actions.Length
    While (ActionIndex)
        ActionIndex -= 1
        string CurAction = Actions[ActionIndex]
            if (StringUtil.Find(CurAction, inkeyword) != -1)
                int ActionID = OMetadata.FindAction(sceneId, CurAction)
                If (ActionID != -1)
                    ;Debug.MessageBox("Target action: " + CurAction + " | ID: " + ActionID)
                    return ActionID
                EndIf
            Endif
    EndWhile
    return -1
EndFunction

Function GetPlayerLimbsLength()
    If (XPMSE)
        float[] TempArray = PapyrusUtil.FloatArray(5)
        TempArray[0] = (XPMSE.GetNodePosition(game.GetPlayer(), true, XPMSE.NINODE_LEFT_THIGH_CME, XPMSE.RMX_LEG_THIGH_KEY)[2])
        TempArray[1] = (XPMSE.GetNodePosition(game.GetPlayer(), true, XPMSE.NINODE_LEFT_CALF_CME, XPMSE.RMX_LEG_CALF_KEY)[2])
        TempArray[2] = (XPMSE.GetNodePosition(game.GetPlayer(), true, XPMSE.NINODE_BODY_UPPER_CME, XPMSE.RMX_SPINE0_KEY)[2])
        TempArray[3] = (XPMSE.GetNodePosition(game.GetPlayer(), true, XPMSE.NINODE_SPINE_CME, XPMSE.RMX_SPINE1_KEY)[2])
        TempArray[4] = (XPMSE.GetNodePosition(game.GetPlayer(), true, XPMSE.NINODE_SPINE_1_CME, XPMSE.RMX_SPINE2_KEY)[2])
        TempArray[5] = (XPMSE.GetNodePosition(game.GetPlayer(), true, XPMSE.NINODE_SPINE_2_CME, XPMSE.RMX_SPINE3_KEY)[2])

        CachedPlayerLimbsLength = TempArray

        Debug.MessageBox("Player's legs and spine length are stored!")
    else
        Debug.MessageBox("Can't find XPMSE.esp!\nPlease check if you're using the newset XPMSE")
        return
    EndIf
Endfunction

Function ScalePlayerLimbsLengthToOne()
    XPMSE.OnSliderChanged("XPMSEChangeLegLengthThigh", 0)
    XPMSE.OnSliderChanged("XPMSEChangeLegLengthCalf", 0)
    XPMSE.OnSliderChanged("XPMSEChangeSpine0Length", 0)
    XPMSE.OnSliderChanged("XPMSEChangeSpine1Length", 0)
    XPMSE.OnSliderChanged("XPMSEChangeSpine2Length", 0)
    XPMSE.OnSliderChanged("XPMSEChangeSpine3Length", 0)
EndFunction

Function ResetPlayerLimbsLength()
    XPMSE.OnSliderChanged("XPMSEChangeLegLengthThigh", CachedPlayerLimbsLength[0])
    XPMSE.OnSliderChanged("XPMSEChangeLegLengthCalf", CachedPlayerLimbsLength[1])
    XPMSE.OnSliderChanged("XPMSEChangeSpine0Length", CachedPlayerLimbsLength[2])
    XPMSE.OnSliderChanged("XPMSEChangeSpine1Length", CachedPlayerLimbsLength[3])
    XPMSE.OnSliderChanged("XPMSEChangeSpine2Length", CachedPlayerLimbsLength[4])
    XPMSE.OnSliderChanged("XPMSEChangeSpine3Length", CachedPlayerLimbsLength[5])
EndFunction

int Function GetExternalInt(string modesp, int id) Global
	return (game.GetFormFromFile(id, modesp) as GlobalVariable).GetValueInt()
endfunction

Function MCM_UpdateMod(bool notInstall = true)

    ;Scripts referencing
    ostim = OUtils.GetOStim()
    XPMSE = game.GetFormFromFile(0x000800, "XPMSE.esp") as RaceMenuPluginXPMSE
    ;Preparing SOS/TNG
    if Game.GetModByName("Schlongs of Skyrim.esp") != 255
        SOSapi = Game.GetFormFromFile(0x1eda4, "Schlongs of Skyrim.esp") as SOS_API
        isUsingSOS = true
    else
        isUsingSOS = false
        RegisterRaceGrp()
	endif

    ;Message
    If (notInstall)
        Debug.MessageBox("ISE is updated!")
    EndIf
ENdFunction

bool Function isLimbsAdjusterEnabled()
    return GetExternalInt("OImprovedSexExpression.esp", 0x000801) == 1
EndFunction

Function ModSelfCheck()
    ;Checking XPMSE
    If (isLimbsAdjusterEnabled())
        If (XPMSE)
            ;GetPlayerLimbsLength()
        else
            Debug.MessageBox("The Mod needs to be updated from MCM")
        EndIf
    EndIf
EndFunction