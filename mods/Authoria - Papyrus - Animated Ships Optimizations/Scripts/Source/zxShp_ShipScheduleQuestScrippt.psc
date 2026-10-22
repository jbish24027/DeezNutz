Scriptname zxShp_ShipScheduleQuestScrippt extends Quest  

Actor Property PlayerRef Auto

Bool Property bToggleOnly = False Auto
{Toggle Ships Only. If True, this script does not activate ship script.Used for too wide range.}

GlobalVariable Property GameHour  Auto  
{It's gamehour}

GlobalVariable Property GameDay  Auto
{It's gameday}

int Property iShipDay = 0 Auto
{0:EveryDay.Ships appear on days that are multiples of this value.}  

int Property iHoliDay = 0 Auto
{0:No Holidy.Ships do not appear on days that are multiples of this value. }  

FormList Property ShipListMorning Auto  
{Optional: List of boats showing up in the morning -> noon.}

FormList Property ShipListNoon  Auto 
{Optional: List of boats showing up in the Noon -> Afternoon.} 

FormList Property ShipListNight  Auto  
{Optional: List of boats showing up in the Evening -> Morning.} 

FormList Property ShipListMidNight  Auto 
{Optional: List of boats showing up in the Midnight.} 

FormList Property ShipListDayTime Auto 
{Optional: List of boats showing up in the daytime.} 

Bool Function IsShipDay()
	if iShipDay == 0 
		return True
	else
		if GameDay
			if GameDay.GetValueInt()% iShipDay == 0
				return True
			else
				return False
			endif
		else
			return True
		endif
	endif
EndFunction

Bool Function IsShipHoliDay()
	if  iHoliDay == 0
		return false
	else
		if GameDay
			if GameDay.GetValueInt()% iHoliDay == 0
				return True
			else
				return False
			endif
		else
			return false
		endif
	endif
EndFunction

String Function GetTimeZone()
	Float ftime = GameHour.GetValue()
	if ftime >= 5.0 && ftime < 10.0
		Return "Morning" 
	elseif ftime >= 10.0 && ftime < 14.0
		return "Noon"
	elseif ftime >= 14.0 && ftime < 19.0
		return  "AfterNoon"

	elseif (ftime >= 19.0 && ftime < 22.0) || (ftime>= 2.0 && ftime < 5.0)
		return "Night"
	else
		return "MidNight"
	endif
EndFunction

Function ToggleShips(Formlist fList, bool bToggle = True)
	if !fList
		return
	endif

	int iSize = fList.GetSize()
	if iSize <= 0
		return
	endif
	int counter = 0
	ObjectReference tmp
	zxShp_DistantShiptBase ShipScript

	While counter < iSize
		tmp = fList.GetAt(counter) as ObjectReference
		if tmp
			ShipScript = tmp as zxShp_DistantShiptBase
			if bToggle
				SafeEnableLinkedRefs(tmp)
				SafeSetEnabled(tmp, True)
			else
				if ShipScript && !ShipScript.IsPlayerNearShipRef()
					DisablePassenger(tmp)
					SafeSetEnabled(tmp, False)
				elseif !ShipScript
					DisablePassenger(tmp)
					SafeSetEnabled(tmp, False)
				endif
			endif
		endif
		Counter += 1
	endWhile
EndFunction

Function SetShipSchedule(String sTimeZone)
	if sTimeZone == "Morning" 	; 5:00 ~ 11:00
		ToggleShips(ShipListDaytime, True)
		ToggleShips(ShipListMorning, True)
		ToggleShips(ShipListNoon, False)
		ToggleShips(ShipListNight, False)
		ToggleShips(ShipListMidNight, False)

	elseif sTimeZone == "Noon" ; 11:00 ~ 13:00
		ToggleShips(ShipListDaytime, True)
		ToggleShips(ShipListMorning, True)
		ToggleShips(ShipListNoon, True)
		ToggleShips(ShipListNight, False)
		ToggleShips(ShipListMidNight, False)

	elseif sTimeZone == "AfterNoon"	 ;13:00 ~ 19 :00
		ToggleShips(ShipListDaytime, True)
		ToggleShips(ShipListMorning, False)
		ToggleShips(ShipListNoon, True)
		ToggleShips(ShipListNight, False)
		ToggleShips(ShipListMidNight, False)

	elseif sTimeZone == "Night"	;19 : 00 ~ 5:00
		ToggleShips(ShipListDaytime, False)
		ToggleShips(ShipListMorning, False)
		ToggleShips(ShipListNoon, False)
		ToggleShips(ShipListNight, True)
		ToggleShips(ShipListMidNight, False)

	elseif sTimeZone == "MidNight" ; 22:00 ~ 2:00
		ToggleShips(ShipListDaytime, False)
		ToggleShips(ShipListMorning, False)
		ToggleShips(ShipListNoon, False)
		ToggleShips(ShipListNight, True)
		ToggleShips(ShipListMidNight, True)	
	endif
EndFunction

Function DisableAllShips()
	ToggleShips(ShipListDaytime, False)
	ToggleShips(ShipListMorning, False)
	ToggleShips(ShipListNoon, False)
	ToggleShips(ShipListNight, False)
	ToggleShips(ShipListMidNight, False)	
EndFunction

Function ActivateShipsList(Formlist fList)
	if !fList || bToggleOnly
		return
	endif

	int iSize = fList.GetSize()
	if iSize <= 0
		return
	endif
	int Counter = 0
	ObjectReference tmp

	While Counter < iSize
		tmp = fList.GetAt(counter) as ObjectReference
		ActivateShipRef(tmp)
		Counter += 1
	endWhile
EndFunction

Function ActivateShipRef(ObjectReference ShipRef)
	if !ShipRef
		return
	endif

	zxShp_DistantShiptBase ShipScript = ShipRef as zxShp_DistantShiptBase
	if !ShipScript
		return
	endif

	int Loadcounter = 0
	While !ShipRef.Is3Dloaded() && LoadCounter < 20
		Utility.Wait(0.1)
		LoadCounter += 1
	endWhile
	ShipScript.UpdateShip()
EndFunction

Function SetUpdateShips(String sTimeZone)
	if sTimeZone == "Morning" 	; 5:00 ~ 10:00
		ActivateShipsList(ShipListDayTime)
		 ActivateShipsList(ShipListMorning)

	elseif sTimeZone == "Noon" ; 10:00 ~ 14:00
		ActivateShipsList(ShipListDayTime)
		 ActivateShipsList(ShipListMorning)
		 ActivateShipsList(ShipListNoon)

	elseif sTimeZone == "AfterNoon"	 ;14:00 ~ 19 :00
		ActivateShipsList(ShipListDayTime)
		ActivateShipsList(ShipListNoon)

	elseif sTimeZone == "Night"	;19 : 00 ~ 5:00
		 ActivateShipsList(ShipListNight)

	elseif sTimeZone == "MidNight"	;22: 00 ~ 2:00
		 ActivateShipsList(ShipListNight)
		 ActivateShipsList(ShipListMidNight)
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

State Busy
EndState



