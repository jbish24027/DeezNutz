ScriptName Authoria_RMS_BagEffectScript extends ActiveMagicEffect
{Authoria Requiem patch 2026-09-06 for Rovan's Market Stall 1.4.1.
 Runs when the player uses the Market Stall Bag (an Ingestible) from the inventory. The game has
 already consumed the bag by the time this fires. Since 1.4.0 the author deploys by DROPPING a
 craftable kit: the drop starts placement mode (a stall outline follows the player), E / R / Shout
 locks the position in (a confirm/cancel menu), and the kit is refunded on cancel, on a failed build,
 on pack-up and on recall. The bag does the same from the inventory:
   - not in placement mode: the same checks as the kit drop (stall limit, combat / indoors / prison),
     then placement mode starts. A refused use hands the bag straight back. From here on the
     controller owns the bag: it returns one on cancel, on a failed build, on pack-up and on recall
     (see RMS_ControllerScript.GiveStallBag).
   - already in placement mode: this use locks the outline in, like pressing E - and since the outline
     was already paid for by the first bag, the bag this use consumed comes straight back.
 One bag per stall, up to the author's five.}

quest Property MasterQuest Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
    Actor PlayerRef = Game.GetPlayer()
    if PlayerRef == None || akTarget != PlayerRef
        return
    endif
    RMS_ControllerScript Controller = MasterQuest as RMS_ControllerScript
    if Controller == None
        Debug.Notification("Market stall: controller missing, bag returned.")
        ; cannot reach the controller, so no GiveStallBag() - fall back to the patch's own item
        Potion Bag = Game.GetFormFromFile(0x000801, "Authoria - Patch - Rovan Market Stall - Requiem.esp") as Potion
        if Bag != None
            PlayerRef.AddItem(Bag, 1, true)
        endif
        return
    endif
    if Controller.IsInPlacementMode
        ; second use while the outline is out: lock it in (confirm/cancel menu). The outline was paid
        ; for by the first bag, so the one this use consumed comes back whatever the menu decides;
        ; a cancel or a failed build returns the first bag through the controller.
        Controller.LockInPlacement()
        Controller.GiveStallBag()
        return
    endif
    if Controller.IsInFollowerTargetMode
        Debug.Notification("Finish assigning the stall attendant first.")
        Controller.GiveStallBag()
        return
    endif
    if Controller.GetActiveStallCount() >= 5 || Controller.FindAvailableSlot() == -1
        ; the author's stall limit, with the author's message
        if Controller.RMS_MSG_MaxStallsReached != None
            Controller.RMS_MSG_MaxStallsReached.Show()
        else
            Debug.Notification("You have reached the maximum active stall limit (5/5).")
        endif
        Controller.GiveStallBag()
        return
    endif
    if !Controller.ValidateDeployment()
        ; combat, indoors or imprisoned - the controller showed the mod's own message
        Controller.GiveStallBag()
        return
    endif
    ; close the inventory menu so the outline is in view at once (the author's kit script does the same)
    Game.DisablePlayerControls(false, false, false, false, false, true, false, false, 0)
    Game.EnablePlayerControls(false, false, false, false, false, true, false, false, 0)
    ; first use: the outline appears 185 units ahead and follows where you look. E / R / Shout, or the
    ; bag again, locks it in. From here the controller returns the bag on cancel, failure, pack-up, recall.
    Controller.StartPlacementMode()
EndEvent
