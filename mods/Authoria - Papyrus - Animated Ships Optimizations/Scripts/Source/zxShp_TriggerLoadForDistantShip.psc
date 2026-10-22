Scriptname zxShp_TriggerLoadForDistantShip extends ObjectReference  

Event OnLoad()
	zxShp_DistantShiptBase MyShip = GetLinkedRef() as zxShp_DistantShiptBase
	if MyShip
		MyShip.UpdateShip()
	endif
EndEvent

Event OnCellAttach()
	if !IsDisabled()
		zxShp_DistantShiptBase MyShip = GetLinkedRef() as zxShp_DistantShiptBase
		if MyShip
			MyShip.UpdateShip()
		endif
	endif
EndEvent
