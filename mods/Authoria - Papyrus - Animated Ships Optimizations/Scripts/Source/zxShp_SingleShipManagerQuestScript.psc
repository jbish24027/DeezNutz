Scriptname zxShp_SingleShipManagerQuestScript extends Quest  

Actor Property PlayerRef Auto
GlobalVariable Property GameHour  Auto  
GlobalVariable Property GameDay  Auto  
GlobalVariable Property gChanceShip Auto

int Function GetCurrentTimeZoneMask()
	Float ftime = GameHour.GetValue()
	if ftime >= 5.0 && ftime < 10.0
		Return 0x00000001
	elseif ftime >= 10.0 && ftime < 14.0
		Return 0x00000010
	elseif ftime >= 14.0 && ftime < 19.0
		Return 0x00000100
		
	elseif (ftime >= 19.0 && ftime < 22.0) || (ftime>= 2.0 && ftime < 5.0)
		Return 0x00001000
	else
		Return 0x00010000
	endif
EndFunction

Function CheckShipSchedule(ObjectReference ShipRef, int ValidTimeZone, int CurrentTimeZone)
	if !ShipRef
		Debug.Notification("SingleShipManager : Cannot find ship Ref")
		return
	endif
	zxShp_DistantShiptBase ShipScript = ShipRef as zxShp_DistantShiptBase
	if !ShipScript
		return
	endif

	RandomShipsPerDay(ShipRef)
	
	if !ShipScript.IsAllowSailToday() || Math.LogicalAnd(ValidTimeZone, CurrentTimeZone) != CurrentTimeZone
		if !ShipScript.IsPlayerNearShipRef()
			DisablePassenger(ShipRef)
			SafeSetEnabled(ShipRef, False)
		endif
		return
	else		
		if ShipRef.IsDisabled()
			SafeSetEnabled(ShipRef, True)
			SafeEnableLinkedRefs(ShipRef)
			return
		endif
	endif
EndFunction

Function DisablePassenger(ObjectReference myRef)
	if !myRef
		return
	endif

	ObjectReference tmp = myRef.GetLinkedRef()
	int counter = 0
	While tmp && counter < 15
		if tmp.Is3DLoaded()
			tmp.StopTranslation()
		endif
		SafeSetEnabled(tmp, False)
		tmp = tmp.GetLinkedRef()
		counter += 1
	endwhile
EndFunction

Function RandomShipsPerDay(ObjectReference myRef)
	if !myRef || !GameDay || !gChanceShip
		return
	endif

	zxShp_DistantShiptBase ShipScript = myRef as zxShp_DistantShiptBase
	if !ShipScript
		return
	endif

	int iLastDayUpdate = ShipScript.GetDayLastUpdate()
	int iCurrentDay = GameDay.GetValueInt()

	if iLastDayUpdate != -1 && Math.abs(iLastDayUpdate - iCurrentDay) < 1
		return
	else
		ShipScript.SetAllowSailToday(Utility.RandomInt(0,100) <= gChanceShip.GetValueInt())
		ShipScript.SetDayLastUpdate(iCurrentDay)
		return
	endif
EndFunction

Function SafeEnableLinkedRefs(ObjectReference StartRef)
	if !StartRef
		return
	endif

	ObjectReference CurrentLink = StartRef.GetLinkedRef()
	int Counter = 0
	While CurrentLink && Counter < 15
		SafeSetEnabled(CurrentLink, True)
		CurrentLink = CurrentLink.GetLinkedRef()
		Counter += 1
	endWhile
EndFunction

Bool Function SafeSetEnabled(ObjectReference TargetRef, Bool bEnable)
	if !TargetRef
		return False
	endif

	if TargetRef.GetEnableParent()
		return False
	endif

	Bool bFade = False
	if PlayerRef
		bFade = PlayerRef.HasLOS(TargetRef)
	endif

	if bEnable
		TargetRef.EnableNoWait(bFade)
	else
		TargetRef.DisableNoWait(bFade)
	endif
	return True
EndFunction
