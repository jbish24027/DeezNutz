Scriptname zxShp_TriggerLoadShipScheduled extends ObjectReference  
zxShp_ShipScheduleQuestScrippt Property qManager Auto

Event OnCellAttach()
	if !IsDisabled()
		if !qManager
			return
		endif
		if qManager.GetState() == "Busy"
			return
		elseif !qManager.IsShipDay() || qManager.IsShipHoliDay()
			qManager.GoToState("Busy")
			qManager.DisableAllShips()
			qManager.GoToState("")
			return
		else
			qManager.GoToState("Busy")
			String sTimeZone = qManager.GetTimeZone()
			qManager.SetShipSchedule(sTimeZone)
			utility.Wait(0.1)
			qManager.SetUpdateShips(sTimeZone)
			qManager.GoToState("")
			return
		endif
	endif
EndEvent
