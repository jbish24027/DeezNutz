Scriptname DAK_StealLabelScript extends ReferenceAlias
{houseCARL DAK Fix: drives the DAK_IsStealing global from the engine's real theft
 check (ObjectReference.IsOffLimits) for the item under the crosshair, so DAK's
 Steal/normal activation label matches the ACTUAL steal behaviour instead of the
 IsOwner heuristic that misfires on unowned items.}

GlobalVariable Property DAK_IsStealing Auto

Event OnInit()
    RegisterForCrosshairRef()
EndEvent

Event OnPlayerLoadGame()
    RegisterForCrosshairRef()
EndEvent

Event OnCrosshairRefChange(ObjectReference akReference)
    If akReference && akReference.IsOffLimits()
        DAK_IsStealing.SetValue(1.0)
    Else
        DAK_IsStealing.SetValue(0.0)
    EndIf
EndEvent
