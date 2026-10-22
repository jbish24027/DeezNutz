Scriptname zxShp_DistantShiptBase extends ObjectReference  
;====================
;Properties
;====================
 Int Property NodeMax = 4 Auto
{Default:4}
Float Property fRidableHeight = 32.0 Auto
{Default:32}
Float Property fSoundRangeMult = 1.0 Auto
{Default:1.0}
Float Property fNPCResetDistance = 1024.0 Auto
{Default:1500}
Keyword Property LinkCustom01  Auto  
Sound Property AMBShipCreakBaseLP  Auto  
Actor Property PlayerRef Auto

;====================
;Variables
;====================
ObjectReference MyRef ; Persistent
ObjectReference ShipMarker
Bool bActive = False
Bool bFirstUpdate = False
Bool bAllowSailToday = True
int SoundInstanceID = -1
Int fDayLastUpdate = -1

;====================
;Event
;====================
Event OnInit()
	MyRef = self
	ShipMarker = MyRef.GetLinkedRef(LinkCustom01)
EndEvent

Event OnCellAttach()
	MyRef = self
	ShipMarker = MyRef.GetLinkedRef(LinkCustom01)
EndEvent

Event OnActivate(ObjectReference akActionRef)
 	if akActionRef && PlayerRef && akActionRef == (PlayerRef as ObjectReference)
		UpdateShip()
		if akActionRef.GetPositionZ() - Self.GetPositionZ() < fRidableHeight
			akActionRef.MoveToNode(self, "RidingShipNodePlayer")
			ApplyShipSound(True)
		endif
	endif
EndEvent

Event OnUpdate()
	 if  !bActive || !MyRef || !PlayerRef || !MyRef.Is3DLoaded() || MyRef.IsDisabled()
		;Debug.Notification("Stopped Update Ship")
		ApplyShipSound(False)
		return
	endif


	if !SetShipMarker()
		ApplyShipSound(False)
		return
	endif
	Float d
	float distanceOrigin = MyRef.GetDistance(PlayerRef)
	float distanceShip = ShipMarker.GetDistance(PlayerRef)
	;Debug.Notification(distanceOrigin +" : " + distanceShip)

	; Check Valid Distance
	if distanceOrigin >  distanceShip
		d = distanceShip
	else
		d = distanceOrigin
	endif
	if d>32000 ; 8 cell
		;Debug.Notification("Ship is out of the script's range.")
		bActive = False
		ApplyShipSound(False)
		return

	elseif d>9000 ;2.25 cell
		;Debug.Notification("Ship is Waiting Mode.")
		RegisterForSingleUpdate(d*0.000625)
		ApplyShipSound(False)
		return

	else	
		;Debug.Notification("Ship is checking NPC Position.")
		SetNPConShip()
		ApplyShipSound((distanceShip <= 1800*fSoundRangeMult))
		RegisterForSingleUpdate(1.0+d*0.0005)
	endif
EndEvent

Event OnCellDetach()
	bActive = False
	ApplyShipSound(False)
EndEvent

Event OnUnload()
	bActive = False
EndEvent

;====================
;Function
;====================
Function SetNPConShip()
	if !MyRef || !ShipMarker
		return
	endif

	GoToState("Busy")
	Actor Target = MyRef.GetLinkedRef() as Actor
	int counter = 0 

	while Target && counter < 15
		if Target
			if !Target.IsDisabled() && !Target.IsDead() && !Target.IsInCombat()
			if bFirstUpdate || ShipMarker.GetDistance(Target) > fNPCResetDistance || Target.GetPositionZ() - MyRef.GetPositionZ() < -64.0 || Target.IsSwimming()
				ResetPassengerPosition(Target, counter)
			endif
			endif
			Target = Target.GetLinkedRef() as Actor
		endif
		counter += 1
	endwhile

	Utility.wait(0.1)
	bFirstUpdate = False
	GoToState("")
EndFunction

Function ResetPassengerPosition(Actor Trg, int index)
	if !Trg || !ShipMarker
		return
	endif

	int loadcounter = 0
	int iNodeMax = NodeMax
	if iNodeMax <= 0
		iNodeMax = 1
	endif

	if !Trg.IsGhost()
		Trg.SetAlpha(0.0)
	endif
	Trg.StopTranslation()
	Trg.MoveTo(ShipMarker) 
	Utility.wait(0.001)
	While !Trg.Is3DLoaded() &&  loadcounter < 20
		Utility.wait(0.1)
		 loadcounter += 1
	endWhile
	Trg.SplineTranslateToRefNode(self, "RidingShipNode" + ((index % iNodeMax) as String), 1.0, 10000.0, 128.0)	
	Utility.wait(0.001)
	Trg.StopTranslation()
	if !Trg.IsGhost()
		Trg.SetAlpha(1.0, True)
	endif
	return
EndFunction 


Function UpdateShip()
	if !bActive
		bFirstUpdate = True
		bActive = True
		RegisterForSingleUpdate(1.5)
	endif
EndFunction

Function ApplyShipSound(Bool bEnable)
	if !PlayerRef || !AMBShipCreakBaseLP
		SoundInstanceID = -1
		return
	endif

	if bEnable
		if SoundInstanceID == -1
			SoundInstanceID = AMBShipCreakBaseLP.Play(PlayerRef)
			Sound.SetInstanceVolume(SoundInstanceID, 0.5) 
		endif
	else
		if SoundInstanceID != -1
			Sound.StopInstance(SoundInstanceID) 
			SoundInstanceID = -1
		endif
	endif
EndFunction

Bool Function SetShipMarker()
	if !MyRef || !PlayerRef
		return False
	endif

	if ShipMarker == None
		ShipMarker = MyRef.GetLinkedRef(LinkCustom01)
		if ShipMarker == None
			Debug.Notification("Ship does not have Position Maker Ref")
			return False
		endif
	endif

	if !ShipMarker.Is3DLoaded()
		ShipMarker.MoveTo(PlayerRef)
		Utility.wait(0.0001)
	endif
	if MyRef.HasNode("ShipCenterNode")
		ShipMarker.MoveToNode(self, "ShipCenterNode")
		return True
	else
		;Debug.Notification("No Ship Center Node")
		return False
	endif

EndFunction


ObjectReference  Function GetNearestShipRef()
	if !MyRef
		return None
	endif

	if !ShipMarker || !PlayerRef
		return MyRef
	endif

	if (MyRef.GetDistance(PlayerRef) > ShipMarker.GetDistance(PlayerRef) )
		return ShipMarker
	else
		return MyRef
	endif
EndFunction

ObjectReference  Function GetShipMarkerRef()
		return ShipMarker
EndFunction

Bool  Function IsPlayerNearShipRef()
		if !ShipMarker || !PlayerRef
			return False
		endif
		return ShipMarker.GetDistance(PlayerRef) <= fNPCResetDistance
EndFunction

Int Function GetDayLastUpdate()
		Return fDayLastUpdate
EndFunction

Function SetDayLastUpdate(int i)
	fDayLastUpdate = i
EndFunction

Bool Function IsAllowSailToday()
		return bAllowSailToday
EndFunction

Function SetAllowSailToday(bool b)
		 bAllowSailToday = b
EndFunction
;====================
State Busy
;====================
Function SetNPConShip()
;Do Nothing
EndFunction

EndState
