scriptName aaaEAS_Twohands extends ActiveMagicEffect

GlobalVariable Property aaGlvSheathWpOnly auto

Potion Property EasDummyItem auto

Actor selfRef

Float RightItemScale
Float LeftItemScale

Bool AnimePlay = False
Bool AnimeUmaPlay = False
Bool ChairAnimePlay = False
Bool rItemShrink = False
Bool lItemShrink = False
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
	selfRef = akTarget
	DispelRequested = False
	AnimePlay = False
	AnimeUmaPlay = False
	ChairAnimePlay = False

	If selfRef.GetAnimationVariableInt("IsStaggering") == 1 || selfRef.IsSwimming() || selfRef.GetAnimationVariableInt("bInJumpState") == 1 || !po3_skseFunctions.GetActorKnockState(selfRef) == 0 as Bool
		RequestDispel()
	ElseIf selfRef.GetSitState() == 0
		If aaGlvSheathWpOnly.GetValue()
			If selfRef.IsWeaponDrawn()
				RequestDispel()
			Else
				EasStandingSWO()
			EndIf
		Else
			EasStanding()
		EndIf
	ElseIf selfRef.GetAnimationVariableInt("bIsRiding") == 1
		If aaGlvSheathWpOnly.GetValue()
			If selfRef.IsWeaponDrawn()
				RequestDispel()
			Else
				EasRidingSWO()
			EndIf
		Else
			EasRiding()
		EndIf
	ElseIf selfRef.GetAnimationVariableBool("bEasChairState")
		EasChair()
	ElseIf selfRef.GetAnimationVariableBool("bEasTableChairState")
		EasTableAndStool()
	ElseIf selfRef.GetAnimationVariableBool("bEasCrossLeggedAndLedge")
		EasTableAndStool()
	Else
		RequestDispel()
	EndIf
EndEvent

Event OnAnimationEvent(ObjectReference akSource, string asEventName)
    If akSource == selfRef as ObjectReference && asEventName == "EasEnd"
		RequestDispel()
	EndIf
EndEvent

Event OnEffectFinish(Actor akTarget, Actor akCaster)
	DispelRequested = True
    GotoState("Busy")
	
	If AnimePlay
		selfRef.SetAnimationVariableBool("bEasTwoHandState", False)
		If selfRef.GetAnimationVariableBool("bEasTwoHandCycle")
			selfRef.SetAnimationVariableBool("bEasTwoHandCycle", False)
		EndIf
		
		rlExpand()
		
		If EasDummyItem 
			selfRef.RemoveItem(EasDummyItem as Form, 1, True, none)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	ElseIf AnimeUmaPlay
		rlExpand()
		
		If EasDummyItem 
			selfRef.RemoveItem(EasDummyItem as Form, 1, True, none)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	ElseIf ChairAnimePlay
		rlExpand()
		
		If EasDummyItem 
			selfRef.RemoveItem(EasDummyItem as Form, 1, True, none)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	EndIf
EndEvent

;状態分岐後のメインの処理-------------------------------------------------------------------------------------------------------------
Function EasChair()
    If EasDummyItem 
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	ChairAnimePlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		; do nothing... yet..
	Else
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		uneqShrink()
		Debug.SendAnimationEvent(selfRef as ObjectReference, "ChairVampireEatingStart")
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasChairStart")
		Utility.Wait(0.500000)
		
		If selfRef.GetAnimationVariableBool("bEasSitState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

Function EasTableAndStool()
   If EasDummyItem 
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	ChairAnimePlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		; do nothing... yet..
		RequestDispel()
	Else
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		uneqShrink()
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasChairStart")
		Utility.Wait(0.500000)
		
		If selfRef.GetAnimationVariableBool("bEasSitState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction

Function EasStanding()
   If EasDummyItem 
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimePlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		selfRef.SetAnimationVariableBool("bEasTwoHandState", True)
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		
		If selfRef.IsWeaponDrawn()
			rShrink()
			lShrink()
		Else
			uneqShrink()
		EndIf
		
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		
		If selfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(4.30000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction  

Function EasStandingSWO()
    If EasDummyItem 
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimePlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		AnimePlay = True
		selfRef.SetAnimationVariableBool("bEasTwoHandState", True)
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		uneqShrink()
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		
		If selfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(4.30000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction  

Function EasRiding()
    If EasDummyItem 
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimeUmaPlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		
		If selfRef.IsWeaponDrawn()
			rShrink()
			lShrink()
		Else
			uneqShrink()
		EndIf
		
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		
		If selfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction  

Function EasRidingSWO()
   If EasDummyItem 
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	AnimeUmaPlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMA")
		Utility.Wait(4.30000)
		Debug.SendAnimationEvent(selfRef as ObjectReference, "OffsetGPMAStop")
		RequestDispel()
	Else
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		uneqShrink()
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasStart")
		Utility.Wait(0.500000)
		
		If selfRef.GetAnimationVariableBool("bEasState")
			Utility.Wait(5.00000)
			RequestDispel()
		Else
			RequestDispel()
		EndIf
	EndIf
EndFunction  

;状態分岐後のメインの処理-------------------------------------------------------------------------------------------------------------
;アイテム拡大縮小-------------------------------------------------------------------------------------------------------------
Function rShrink()
    If selfRef.GetEquippedItemType(1) == 0 || selfRef.GetEquippedItemType(1) == 7 || selfRef.GetEquippedItemType(1) == 9
        return
    Else    
        RightItemScale = NetImmerse.GetNodeScale(selfRef, "Weapon", False)
        
		If RightItemScale == 0.01
			RightItemScale = 1.00
		EndIf
		
		NetImmerse.SetNodeScale(selfRef, "Weapon", 0.01, False) 
		rItemShrink = True
    EndIf
EndFunction

Function lShrink()
    If selfRef.GetEquippedItemType(0) == 0 || selfRef.GetEquippedItemType(0) == 5 || selfRef.GetEquippedItemType(0) == 6 || selfRef.GetEquippedItemType(0) == 9
        return
    Else    
        LeftItemScale = NetImmerse.GetNodeScale(selfRef, "Shield", False)
        
		If LeftItemScale == 0.01
			LeftItemScale = 1.00
		EndIf

        NetImmerse.SetNodeScale(selfRef, "Shield", 0.01, False) 
		lItemShrink = True
    EndIf
EndFunction

Function uneqShrink()
    If selfRef.GetEquippedItemType(0) == 10 || selfRef.GetEquippedItemType(0) == 11
        LeftItemScale = NetImmerse.GetNodeScale(selfRef, "Shield", False)
		
        If LeftItemScale == 0.01
			LeftItemScale = 1.00
		EndIf
		
        NetImmerse.SetNodeScale(selfRef, "Shield", 0.01, False)
		lItemShrink = True
    EndIf
EndFunction 

Function rlExpand()
    If ( rItemShrink )
        NetImmerse.SetNodeScale(selfRef, "Weapon", RightItemScale, False)
        rItemShrink = False
    EndIf
    If ( lItemShrink )
        NetImmerse.SetNodeScale(selfRef, "Shield", LeftItemScale, False)
        lItemShrink = False
    EndIf
EndFunction

;アイテム拡大縮小-------------------------------------------------------------------------------------------------------------
State Busy
;===============================================================================================================================================

	Event OnAnimationEvent(ObjectReference akSource, string asEventName)
	EndEvent

	Event OnEffectFinish(Actor akTarget, Actor akCaster)
	DispelRequested = True
	EndEvent

;===============================================================================================================================================
EndState