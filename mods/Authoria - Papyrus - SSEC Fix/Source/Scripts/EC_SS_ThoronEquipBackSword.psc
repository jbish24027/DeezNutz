Scriptname EC_SS_ThoronEquipBackSword extends ReferenceAlias

Ammo Property EC_SS_JygSwordBack Auto
Float Property RetrySeconds = 5.0 Auto

Event OnInit()
	RegisterForSingleUpdate(RetrySeconds)
EndEvent

Event OnUpdate()
	Actor thoron = GetActorReference()
	If thoron == None
		RegisterForSingleUpdate(RetrySeconds)
		Return
	EndIf

	If EC_SS_JygSwordBack == None
		Return
	EndIf

	If thoron.GetItemCount(EC_SS_JygSwordBack) <= 0
		thoron.AddItem(EC_SS_JygSwordBack, 1, True)
	EndIf

	Utility.Wait(0.5)
	thoron.EquipItem(EC_SS_JygSwordBack, True)
EndEvent
