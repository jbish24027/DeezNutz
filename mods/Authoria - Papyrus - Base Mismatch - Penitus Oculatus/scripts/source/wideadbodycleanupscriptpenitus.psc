Scriptname WIDeadBodyCleanupScriptPenitus extends ReferenceAlias  

;**** This should ONLY BE USED ON UNIQUE ACTORS!!! ****

;This script cleans up dead actors, enables a container (ie grave/crypt) and moves all their inventory, after it Loads/unloads after a certain period of time.
;If you need to temporarily stop someone from being cleaned up, put them in the WINoBodyCleanupFaction faction.

;please do not modify this script without talking to jduvall

WIFunctionsScript Property WI Auto
{Pointer to WIFunctionsScript attached to WI quest. You MUST set this or things will be broken.}

float Property DaysBeforeCleanUp = 0.5 Auto
{Default = 0.5: What's the minimum amount of time (in days) that the body should stick around before being cleaned up. (Clean up happens during while loop.)}

ObjectReference Property DeathContainer Auto
{Container to move all the items the actor has in his inventory when cleaned up.}


state Dead
	;do nothing
	Event OnDeath(Actor akKiller)
	EndEvent
	
EndState


Event OnDeath(Actor akKiller)

	GoToState("Dead")
	
	if DeathContainer
		
		bool cleanedUp = false	
		
		while cleanedUp == false
; 			debug.trace("WIDeadBodyCleanupScript" + self + "OnDeath() In While Loop, will try cleaning up after waiting " + DaysBeforeCleanUp)
			
			utility.waitGameTime(DaysBeforeCleanUp * 24)
		
			cleanedUp = checkForCleanup()
		
		endWhile
			
	else
; 		debug.trace("WIDeadBodyCleanupScript" + self + " WARNING: NO DeathContainer!", 2)
	
	endif
		
EndEvent


bool function checkForCleanup()
    Actor actorRef = GetActorReference()
    if actorRef == None
        return true
    endif

    if WI != None && actorRef.IsInFaction(WI.WINoBodyCleanupFaction)
        ; Suspend cleanup until the faction setting is removed.
    Elseif actorRef.Is3DLoaded() == False
        cleanUpBody()
        return true
    EndIf

    return false
endfunction

function cleanUpBody()
    Actor actorRef = GetActorReference()
    if actorRef == None || WI == None || DeathContainer == None
        return
    endif

    actorRef.MoveTo(WI.WIDeadBodyCleanupCellMarker)

    If DeathContainer.GetParentCell() == WI.WIDeadBodyCleanupCellMarker.GetParentCell()
        Return
    EndIf

    DeathContainer.SetActorOwner(actorRef.GetActorBase())
    DeathContainer.Enable()

    ConsoleUtil.SetSelectedReference(actorRef)
    ConsoleUtil.ExecuteCommand("unequipall")

    Form[] questItems = PO3_SKSEFunctions.GetQuestItems(actorRef)
    int i = questItems.Length
    While i
        i -= 1
        Form akItem = questItems[i]
        int count = actorRef.GetItemCount(akItem)
        actorRef.RemoveItem(akItem, count, akOtherContainer=DeathContainer)
    EndWhile

    i = actorRef.GetNumItems()
    While i
        i -= 1
        Form akItem = actorRef.GetNthForm(i)
        int count = actorRef.GetItemCount(akItem)
        DeathContainer.AddItem(akItem, count)
    EndWhile
EndFunction

