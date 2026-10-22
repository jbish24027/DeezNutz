Scriptname zxShp_TriggerLoadShipScheduledSingle extends ObjectReference  

int Property ScheduleMask Auto
zxShp_SingleShipManagerQuestScript Property qManager Auto
{1:Morning, 16:Noon, 256 : Afternoon, 4096: Night, 65536: MidNight}

Event OnCellAttach()
	if !IsDisabled()
		if !qManager
			return
		endif
		ObjectReference ShipRef = GetLinkedRef()
		if !ShipRef
			return
		endif
		qManager.CheckShipSchedule(ShipRef, ScheduleMask, qManager.GetCurrentTimeZoneMask())
		if ShipRef.IsDisabled()
			return
		endif
		zxShp_DistantShiptBase ShipScript = ShipRef as zxShp_DistantShiptBase
		if !ShipScript
			return
		endif
		int counter = 0
		While !ShipRef.Is3DLoaded() && counter < 20
			Utility.Wait(0.1)
			counter += 1
		endWhile
		ShipScript.UpdateShip()
		;Debug.Notification("Single Ships Update Start")
	endif
EndEvent

