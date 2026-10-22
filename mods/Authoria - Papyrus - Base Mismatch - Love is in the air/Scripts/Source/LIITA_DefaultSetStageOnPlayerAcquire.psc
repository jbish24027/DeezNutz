Scriptname LIITA_DefaultSetStageOnPlayerAcquire extends ReferenceAlias
{LIITA-specific alias-safe version of defaultSetStageOnPlayerAcquireItem.}

Quest Property myQST Auto
{Quest upon which to set stage. Defaults to this alias's owning quest.}
Int Property preReqStage = -1 Auto
{(Optional) Stage that must be set for this script to run. Default: none.}
Int Property StageToSet Auto
{Set this stage when the player picks up this item.}

Auto State waiting
    Event OnContainerChanged(ObjectReference akNewContainer, ObjectReference akOldContainer)
        If akNewContainer != Game.GetPlayer()
            Return
        EndIf

        Quest qst = myQST
        If qst == None
            qst = GetOwningQuest()
        EndIf
        If qst == None
            Return
        EndIf

        If preReqStage == -1 || (qst.IsRunning() && qst.GetStageDone(preReqStage))
            qst.SetStage(StageToSet)
            GoToState("inactive")
        EndIf
    EndEvent
EndState

State inactive
EndState