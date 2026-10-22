scriptName aaaEAS_Onehands_table extends ActiveMagicEffect

;aaaEAS_Onehands_table Ver1.2.0 b

GlobalVariable Property aaGlvMenuChair auto
GlobalVariable Property aaGlvMenuTable auto
GlobalVariable Property aaGlvSheathWpOnly auto
GlobalVariable Property aaGlvSetSmallTable auto

Message Property aaaUseTableMessage auto

Potion Property EasDummyItem auto

Actor selfRef

float RightItemScale
float LeftItemScale

Bool AnimePlay = False
Bool ChairAnimePlay = False
Bool ChairEUAnimePlay = False
Bool ItemShrink = False
Bool TorchShrink = False
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
	ChairAnimePlay = False
	ChairEUAnimePlay = False
		
	If selfRef.GetAnimationVariableInt("IsStaggering") == 1 || selfRef.IsSwimming() || selfRef.GetAnimationVariableInt("bInJumpState") == 1 || !PO3_SKSEFunctions.GetActorKnockState(selfRef) == 0 as Bool
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
		If aaGlvMenuChair.GetValue() == 1
			Int intIndex = aaaUseTableMessage.Show(0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000)
			
			If intIndex == 0
				EasChairEU()
			ElseIf intIndex == 1
				EasChair()
			EndIf
		ElseIf aaGlvMenuChair.GetValue() == 2
			EasChairEU()
		ElseIf aaGlvMenuChair.GetValue() == 0
			EasChair()
		EndIf
	ElseIf selfRef.GetAnimationVariableBool("bEasTableChairState")
		If aaGlvMenuTable.GetValue() == 1
			Int intindex = aaaUseTableMessage.Show(0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000)
			
			If intindex == 0
				EasTableAndStoolEU()
			ElseIf intindex == 1
				EasTableAndStool()
			EndIf
		ElseIf aaGlvMenuTable.GetValue() == 2
			EasTableAndStoolEU()
		ElseIf aaGlvMenuTable.GetValue() == 0
			EasTableAndStool()
		EndIf
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
		If ItemShrink
			NetImmerse.setNodeScale(selfRef as ObjectReference, "Weapon", RightItemScale, False)
			ItemShrink = False
		EndIf
		
		If EasDummyItem
			selfRef.RemoveItem(EasDummyItem as Form, 1, True, None)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	ElseIf ChairAnimePlay
		If EasDummyItem
			selfRef.RemoveItem(EasDummyItem as Form, 1, True, None)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	ElseIf ChairEUAnimePlay
		If TorchShrink
			NetImmerse.setNodeScale(selfRef as ObjectReference, "Shield", LeftItemScale, False)
			TorchShrink = False
		EndIf
		
		If EasDummyItem
			selfRef.RemoveItem(EasDummyItem as Form, 1, True, None)
		EndIf
		
		If FPPlayer
			Game.ForceFirstPerson()
		EndIf
	EndIf
EndEvent

;状態分岐後のメインの処理-------------------------------------------------------------------------------------------------------------
function EasChairEU()
    ChairEUAnimePlay = True
	
	If EasDummyItem
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		FPPlayer = True
		Game.ForceThirdPerson()
	EndIf
	
	RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
	
	If selfRef.GetEquippedItemType(0) == 11
		LeftItemScale = NetImmerse.GetNodeScale(selfRef as ObjectReference, "Shield", False)
		
		If LeftItemScale == 0.01
			LeftItemScale = 1.00
		EndIf
		
		NetImmerse.setNodeScale(selfRef as ObjectReference, "Shield", 0.0100000, False)
		TorchShrink = True
	EndIf
	
	Debug.SendAnimationEvent(selfRef as ObjectReference, "ChairVampireEatingStart")
	
	If aaGlvSetSmallTable.GetValue()
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasChairEuStStart")
	Else
		Debug.SendAnimationEvent(selfRef as ObjectReference, "EasChairEuStart")
	EndIf
	
	Utility.Wait(0.500000)
	
	If selfRef.GetAnimationVariableBool("bEasSitState")
		Utility.Wait(6.50000)
		RequestDispel()
	Else
		RequestDispel()
	EndIf
EndFunction

function EasChair()
    If EasDummyItem
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	ChairAnimePlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		; do nothing... yet..
	Else
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
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

function EasTableAndStoolEU()
    ChairEUAnimePlay = True
	
	If EasDummyItem
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		FPPlayer = True
		Game.ForceThirdPerson()
	EndIf
	
	RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
	
	If selfRef.GetEquippedItemType(0) == 11
		LeftItemScale = NetImmerse.GetNodeScale(selfRef as ObjectReference, "Shield", False)
		
		If LeftItemScale == 0.01
			LeftItemScale = 1.00
		EndIf
		
		NetImmerse.setNodeScale(selfRef as ObjectReference, "Shield", 0.0100000, False)
		TorchShrink = True
	EndIf
	
	Debug.SendAnimationEvent(selfRef as ObjectReference, "EasChairEuStart")
	Utility.Wait(0.500000)
	
	If selfRef.GetAnimationVariableBool("bEasSitState")
		Utility.Wait(6.50000)
		RequestDispel()
	Else
		RequestDispel()
	EndIf
EndFunction

function EasTableAndStool()
    If EasDummyItem
		selfRef.AddItem(EasDummyItem as Form, 1, True)
	EndIf
	
	ChairAnimePlay = True
	
	If selfRef.GetAnimationVariableInt("i1stPerson") == 1
		; do nothing... yet..
	Else
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
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

function EasStanding()
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
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		rShrink()
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

function EasStandingSWO()
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
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
		rShrink()
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

function EasRiding()
    If EasDummyItem
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

function EasRidingSWO()
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
		RegisterForAnimationEvent(selfRef as ObjectReference, "EasEnd")
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