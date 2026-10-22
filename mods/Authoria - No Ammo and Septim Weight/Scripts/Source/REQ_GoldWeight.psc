Scriptname REQ_GoldWeight extends REQ_CoreScript
{show the gold weight in the inventory as a coin purse}

MiscObject Property gold Auto

MiscObject Property displayPurse Auto
{a quest item added to the player's inventory to display the total gold weight}
ObjectReference Property hidePursePlace Auto
{container where the purse can be hidden when the player has no cash in their inventory}

Bool goldWeightEnabled = True
Float requiemGoldWeight = 0.0025

Event OnInit()
    parent.OnInit()
    RegisterForModEvent("Authoria_NoAmmoWeight_GoldToggleChanged", "OnGoldWeightToggleChanged")
    goldWeightEnabled = getGoldWeightEnabled()
EndEvent

Event OnItemAdded(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akSourceContainer)
    If (!goldWeightEnabled)
        return
    EndIf

    If (akBaseItem == gold)
        updateGoldWeightDisplay()
    EndIf
EndEvent

Event OnItemRemoved(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akDestContainer)
    If (!goldWeightEnabled)
        If (akBaseItem == displayPurse && akDestContainer != hidePursePlace)
            akDestContainer.removeItem(displayPurse, 1, true, hidePursePlace)
        EndIf
        return
    EndIf

    If (akBaseItem == gold)
        updateGoldWeightDisplay()
    ElseIf (akBaseItem == displayPurse && akDestContainer != hidePursePlace)
        akDestContainer.removeItem(displayPurse, 1, true, hidePursePlace)
    EndIf
EndEvent

Event OnPlayerLoadGame()
    parent.OnPlayerLoadGame()
    RegisterForModEvent("Authoria_NoAmmoWeight_GoldToggleChanged", "OnGoldWeightToggleChanged")
    goldWeightEnabled = getGoldWeightEnabled()
    If (goldWeightEnabled)
        updateGoldWeightDisplay()
    Else
        disableGoldWeight()
    EndIf
EndEvent

Function initScript(Int currentVersion, Int nevVersion)
    RegisterForModEvent("Authoria_NoAmmoWeight_GoldToggleChanged", "OnGoldWeightToggleChanged")
    goldWeightEnabled = getGoldWeightEnabled()
    If (goldWeightEnabled)
        updateGoldWeightDisplay()
    Else
        disableGoldWeight()
    EndIf
EndFunction

Function shutdownScript(Int currentVersion, Int nevVersion)
    ; a new one will be spawned by restarting the parent quest
    player.removeItem(displayPurse, player.getItemCount(displayPurse), true)
    hidePursePlace.removeItem(displayPurse, hidePursePlace.getItemCount(displayPurse), true)
EndFunction

Event OnGoldWeightToggleChanged(Int enabled)
    goldWeightEnabled = enabled as Bool
    If (goldWeightEnabled)
        updateGoldWeightDisplay()
    Else
        disableGoldWeight()
    EndIf
EndEvent

Bool Function getGoldWeightEnabled()
    If MCM.IsInstalled()
        return MCM.GetModSettingBool("Requiem", "bEnableGoldWeight:General")
    EndIf
    return True
EndFunction

Function disableGoldWeight()
    gold.setWeight(0.0)
    displayPurse.setWeight(0.0)
    If (player.getItemCount(displayPurse) > 0)
        player.removeItem(displayPurse, player.getItemCount(displayPurse), true, hidePursePlace)
    EndIf
EndFunction

Function updateGoldWeightDisplay()
    gold.setWeight(requiemGoldWeight)
    Float weight = player.getItemCount(gold) * gold.getWeight()
    displayPurse.setWeight(weight)
    If (weight == 0 && player.getItemCount(displayPurse) > 0)
        player.removeItem(displayPurse, 1, true, hidePursePlace)
    ElseIf (weight > 0 && player.getItemCount(displayPurse) == 0)
        hidePursePlace.removeItem(displayPurse, 1, true, player)
    EndIf
EndFunction
