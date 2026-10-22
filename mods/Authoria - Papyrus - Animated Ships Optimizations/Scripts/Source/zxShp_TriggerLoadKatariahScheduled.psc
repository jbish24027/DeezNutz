Scriptname zxShp_TriggerLoadKatariahScheduled extends ObjectReference  
zxShp_ShipScheduleQuestScrippt Property qManager Auto
ObjectReference Property EnablerRef Auto

Event OnCellAttach()
	if !IsDisabled()
		if !qManager
			return
		endif
		if qManager.GetState() == "Busy" 
			return
		elseif !qManager.IsShipDay() || (EnablerRef && !EnablerRef.IsDisabled())
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
