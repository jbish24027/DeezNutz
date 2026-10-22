scriptName aaaEAS_Onehands extends ActiveMagicEffect

GlobalVariable Property aaGlvSheathWpOnly auto

Potion Property EasDummyItem auto

Actor SelfRef

Float RightItemScale

Bool AnimePlay = False
Bool ChairAnimePlay = False
Bool ItemShrink = False
Bool FPPlayer = False

Bool DispelRequested = False

Function RequestDispel()
	If DispelRequested
		Return
	EndIf
	DispelRequested = True
	Self.Dispel()
EndFunction

Event OnEffectStart(Actor akTarget, Actor akCaster)
	SelfRef = akTarget
	DispelRequested = False
	AnimePlay = False
	ChairAnimePlay = False
	
	If SelfRef.GetAnimationVariableInt("IsStaggering") == 1 || SelfRef.IsSwimming() || SelfRef.GetAnimationVariableInt("bInJumpState") == 1 || !PO3_SKSEFunctions.GetActorKnockState(SelfRef) == 0 as Bool
		RequestDispel()
	ElseIf SelfRef.GetSitState() == 0
		If aaGlvSheathWpOnly.GetValue()
			If SelfRef.IsWeaponDrawn()
				RequestDispel()
			Else
				EasStandingSWO()
			EndIf
		Else
			EasStanding()
		EndIf
	ElseIf SelfRef.GetAnimationVariableInt("bIsRiding") == 1
		If aaGlvSheathWpOnly.GetValue()
			If SelfRef.IsWeaponDrawn()
				RequestDispel()
			Else
				EasRidingSWO()
			EndIf
		Else
			EasRiding()
		EndIf
	ElseIf SelfRef.GetAnimationVariableBool("bEasChairState")
		EasChair()
	ElseIf SelfRef.GetAnimationVariableBool("bEasTableChairState")
		EasTableAndStool()
	ElseIf SelfRef.GetAnimationVariableBool("bEasCrossLeggedAndLedge")
		EasTableAndStool()
	Else
		RequestDispel()
	EndIf
EndEvent

Event OnAnimationEvent(ObjectReference akSource, String asEventName)
	If akSource == SelfRef as ObjectReference && asEventName == "EasEnd"
		RequestDispel()
	EndIf
endEvent

Event OnEffectFinish(Actor akTarget, Actor akCaster)
	DispelRequested = True
    GotoState("Busy")
	
	If AnimePlay
		If ItemShrink
			netimmerse.setNodeScale(SelfRef as ObjectReference, "Weapon", RightItemScale, False)
			ItemShrink = False
		EndIf
		
		If EasDummyItem
			SelfRef.RemoveItem(EasDummyItem as Form, 1, True, None)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	ElseIf ChairAnimePlay
		If EasDummyItem
			SelfRef.RemoveItem(EasDummyItem as Form, 1, True, None)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	EndIf
EndEvent

;状態分岐後のメインの処理-------------------------------------------------------------------------------------------------------------

Function EasChair()
	If EasDummyItem
		SelfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	ChairAnimePlay = True
	
	If SelfRef.GetAnimationVariableInt("i1stPerson") == 1
		; do nothing... yet..
	Else
		RegisterForAnimationEvent(SelfRef as ObjectReference, "EasEnd")
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "ChairVampireEatingStart")
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "EasChairStart")
		Utility.Wait(0.500000)
		
		If SelfRef.GetAnimationVariableBool("bEasSitState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

Function EasTableAndStool()
	If EasDummyItem
		SelfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	ChairAnimePlay = True
	
	If SelfRef.GetAnimationVariableInt("i1stPerson") == 1
		; do nothing... yet..
	Else
		RegisterForAnimationEvent(SelfRef as ObjectReference, "EasEnd")
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "EasChairStart")
		Utility.Wait(0.500000)
		
		If SelfRef.GetAnimationVariableBool("bEasSitState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

Function EasStanding()
	If EasDummyItem != None
		SelfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimePlay = True
	
	If SelfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		RegisterForAnimationEvent(SelfRef as ObjectReference, "EasEnd")
		rShrink()
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		If SelfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(4.30000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

Function EasStandingSWO()
	If EasDummyItem != None
		SelfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimePlay = True
	
	If SelfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		RegisterForAnimationEvent(SelfRef as ObjectReference, "EasEnd")
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		
		If SelfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(4.30000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

Function EasRiding()
	If EasDummyItem != None
		SelfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimePlay = True
	
	If SelfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		RegisterForAnimationEvent(SelfRef as ObjectReference, "EasEnd")
		rShrink()
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		
		If SelfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

Function EasRidingSWO()
	If EasDummyItem != None
		SelfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimePlay = True
	
	If SelfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		RegisterForAnimationEvent(SelfRef as ObjectReference, "EasEnd")
		Debug.SendAnimationEvent(SelfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		
		If SelfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

;状態分岐後のメインの処理-------------------------------------------------------------------------------------------------------------

;アイテム縮小-------------------------------------------------------------------------------------------------------------
Function rShrink()
    If SelfRef.IsWeaponDrawn()
        If SelfRef.GetEquippedItemType(1) == 0 || SelfRef.GetEquippedItemType(1) == 7 || SelfRef.GetEquippedItemType(1) == 9;抜刀状態で障害にならないアイテム(0素手、7弓、9魔法 のどれか)を持っていた時
            return
        Else    
            RightItemScale = NetImmerse.GetNodeScale(SelfRef, "Weapon", False)
            
			If RightItemScale == 0.01
				RightItemScale = 1.00
			EndIf
			
			ItemShrink = True
            NetImmerse.setNodeScale(SelfRef, "Weapon", 0.01, False) 
        EndIf
    EndIf
EndFunction
;アイテム縮小-------------------------------------------------------------------------------------------------------------

State Busy
;===============================================================================================================================================

	Event OnAnimationEvent(ObjectReference akSource, string asEventName)
	EndEvent

	Event OnEffectFinish(Actor akTarget, Actor akCaster)
	DispelRequested = True
	EndEvent

;===============================================================================================================================================
EndState