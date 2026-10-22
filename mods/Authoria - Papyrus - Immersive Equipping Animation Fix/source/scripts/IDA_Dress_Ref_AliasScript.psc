Scriptname IDA_Dress_Ref_AliasScript extends ReferenceAlias  

GlobalVariable Property EnableAnimation Auto
GlobalVariable Property IDA_Glob Auto
GlobalVariable Property IDA_DressHead Auto
GlobalVariable Property IDA_DressBody Auto
GlobalVariable Property IDA_DressHands Auto
GlobalVariable Property IDA_DressFeet Auto
GlobalVariable Property IDA_DressNeck Auto
GlobalVariable Property IDA_UndressHead Auto
GlobalVariable Property IDA_UndressBody Auto
GlobalVariable Property IDA_UndressHands Auto
GlobalVariable Property IDA_UndressFeet Auto
GlobalVariable Property IDA_UndressNeck Auto
GlobalVariable Property IDA_NoFirstPerson Auto
GlobalVariable Property IDA_DressRing Auto
GlobalVariable Property IDA_UndressRing Auto

Keyword property ArmorHelmet auto
Keyword property ArmorCuirass auto
Keyword property ClothingBody auto
Keyword property ClothingHead auto
Keyword property ClothingPouch auto

Actor PlayerREF
Actor Property PlayerRef Auto

Alias htPlayerAlias

Event OnInit()
	If Game.IsPluginInstalled("Helmet Toggle 2.esp") ; Checks if mod is installed
		Quest htQuest = (Game.GetFormFromFile(0x0000800, "Helmet Toggle 2.esp") as Quest) as HT_MCM
		htPlayerAlias = htQuest.GetAlias(1)
	Else
		htPlayerAlias = None
	EndIf
	
EndEvent

Event OnPlayerLoadGame()
	If Game.IsPluginInstalled("Helmet Toggle 2.esp") ; Checks if mod is installed
		Quest htQuest = (Game.GetFormFromFile(0x0000800, "Helmet Toggle 2.esp") as Quest) as HT_MCM
		htPlayerAlias = htQuest.GetAlias(1)
	Else
		htPlayerAlias = None
	EndIf
	
EndEvent

Event OnObjectEquipped(Form akBaseObject, ObjectReference akReference)
	Keyword ignoreArmor = None
	Armor equippedArmor = None
	Int slotMask = 0

	If akBaseObject == None
		Return
	EndIf

	If EnableAnimation.GetValue() as Bool && IDA_Glob.GetValue() == 0 && PlayerRef.GetSitState() == 0 && PlayerRef.GetFlyingState() == 0 && !PlayerRef.IsWeaponDrawn() && PlayerRef.GetSleepState() == 0 && !PlayerRef.IsSwimming() && !PlayerRef.GetNoBleedoutRecovery()
		If PlayerRef.GetAnimationVariableBool("bIsInMT") && !PlayerRef.GetAnimationVariableBool("bInJumpState") && !PlayerRef.GetAnimationVariableBool("isEquipping") && !PlayerRef.GetAnimationVariableBool("isUnequipping")
			ignoreArmor = Keyword.GetKeyword("IDA_IgnoreArmor")
			If ignoreArmor != None && PlayerRef.WornHasKeyword(ignoreArmor)
				Return
			EndIf

			equippedArmor = akBaseObject as Armor
			If equippedArmor != None
				slotMask = equippedArmor.GetSlotMask()
			EndIf
			
			if IDA_DressHead.GetValue() == 1  && akBaseObject.HasKeyword(ArmorHelmet)
				IDA_Glob.SetValue(1)	  
				
				If !(htPlayerAlias as HT_PlayerAlias).htMCM.HT_EnableHelmet.GetValue() || !(htPlayerAlias as HT_PlayerAlias).HT_HelmetState.GetValue()
					if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
						Game.ForceThirdPerson()
					EndIf		
					
					Debug.SendAnimationEvent(PlayerRef, "equiphelmet")		  
					Utility.Wait(2.2)
					Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
				EndIf
				
				IDA_Glob.SetValue(0)
			elseif  IDA_DressHead.GetValue() == 1  && akBaseObject.HasKeyword(ClothingHead)
				IDA_Glob.SetValue(1)	
				
				If !(htPlayerAlias as HT_PlayerAlias).htMCM.HT_EnableHelmet.GetValue() || !(htPlayerAlias as HT_PlayerAlias).HT_HelmetState.GetValue()
					if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
						Game.ForceThirdPerson()
					EndIf	
					
					Debug.SendAnimationEvent(PlayerRef, "equiphood")		  
					Utility.Wait(2.2)
					Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
				EndIf
				
				IDA_Glob.SetValue(0)		  
			elseif slotMask == 8 && IDA_DressHands.GetValue() == 1  
				if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
					Game.ForceThirdPerson()
				EndIf	
					
				IDA_Glob.SetValue(1)		  
				Debug.SendAnimationEvent(PlayerRef, "equiphands")	
				Utility.Wait(2.5)
				Debug.SendAnimationEvent(PlayerRef, "OffsetStop") 
				IDA_Glob.SetValue(0)			  
			elseif slotMask == 128 && IDA_DressFeet.GetValue() == 1  
				if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
					Game.ForceThirdPerson()
				EndIf	

				IDA_Glob.SetValue(1)		  
				Debug.SendAnimationEvent(PlayerRef, "equipboots")	
				Utility.Wait(3.5)
				Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
				IDA_Glob.SetValue(0)			  
			elseif (akBaseObject.HasKeyword(ArmorCuirass)||akBaseObject.HasKeyword(ClothingBody)) && IDA_DressBody.GetValue() == 1 || slotMask == 4 && IDA_DressBody.GetValue() == 1  
				if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
					Game.ForceThirdPerson()
				EndIf	
				
				IDA_Glob.SetValue(1)		 
				Debug.SendAnimationEvent(PlayerRef, "equipcuirass")	
				Utility.Wait(2.5)
				Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
				IDA_Glob.SetValue(0)			  
			elseif slotMask == 32 && IDA_DressNeck.GetValue() == 1  
				if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
					Game.ForceThirdPerson()
				EndIf	
				
				IDA_Glob.SetValue(1)		 
				Debug.SendAnimationEvent(PlayerRef, "equipneck")	
				Utility.Wait(3.6)
				Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
				IDA_Glob.SetValue(0)	  
			elseif slotMask == 64 && IDA_DressRing.GetValue() == 1  
				if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
					Game.ForceThirdPerson()
				EndIf	
				
				IDA_Glob.SetValue(1)		 
				Debug.SendAnimationEvent(PlayerRef, "equipring")	
				Utility.Wait(3.6)
				Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
				IDA_Glob.SetValue(0)	  
			endif	 	 
		EndIf	
	EndIf
EndEvent

Event OnObjectUnequipped(Form akBaseObject, ObjectReference akReference)
	Armor equippedArmor = None
	Int slotMask = 0

	If akBaseObject == None
		Return
	EndIf

	equippedArmor = akBaseObject as Armor
	If equippedArmor != None
		slotMask = equippedArmor.GetSlotMask()
	EndIf

	If EnableAnimation.GetValue() as Bool && IDA_Glob.GetValue() == 0 && PlayerRef.GetSitState() == 0 && PlayerRef.GetFlyingState() == 0 && !PlayerRef.IsWeaponDrawn() && PlayerRef.GetSleepState() == 0 && !PlayerRef.IsSwimming() && !PlayerRef.GetNoBleedoutRecovery()
		if  IDA_UndressHead.GetValue() == 1  && akBaseObject.HasKeyword(ArmorHelmet)
			If (htPlayerAlias as HT_PlayerAlias).HT_HelmetState.GetValue() > 0 && (htPlayerAlias as HT_PlayerAlias).htMCM.HT_EnableHelmet.GetValue()
				Return
			EndIf
			 
			if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && !IDA_NoFirstPerson.GetValue()
				 Game.ForceThirdPerson()
			EndIf
			
			IDA_Glob.SetValue(1)	  
			Debug.SendAnimationEvent(PlayerRef, "unequiphelmet")	
			Utility.Wait(2.5)
			Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
			IDA_Glob.SetValue(0)			  
		elseif  IDA_UndressHead.GetValue() == 1  && akBaseObject.HasKeyword(ClothingHead)
			If (htPlayerAlias as HT_PlayerAlias).HT_HelmetState.GetValue() > 0 && (htPlayerAlias as HT_PlayerAlias).htMCM.HT_EnableHood.GetValue()
				Return
			EndIf
				 
			if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
				 Game.ForceThirdPerson()
			EndIf	  
			
			IDA_Glob.SetValue(1)	  
			Debug.SendAnimationEvent(PlayerRef, "unequiphelmet")	
			Utility.Wait(2.2)
			Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
			IDA_Glob.SetValue(0)			  
		elseif slotMask == 8 && IDA_UndressHands.GetValue() == 1  
			if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1
				If !IDA_NoFirstPerson.GetValue()
					 Game.ForceThirdPerson()
				EndIf
			EndIf	
				  
			IDA_Glob.SetValue(1)		  
			Debug.SendAnimationEvent(PlayerRef, "unequiphands")	
			Utility.Wait(2.5)
			Debug.SendAnimationEvent(PlayerRef, "OffsetStop") 
			IDA_Glob.SetValue(0)			  
		elseif slotMask == 128 && IDA_UndressFeet.GetValue() == 1  
			if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
				 Game.ForceThirdPerson()
			EndIf
			
			IDA_Glob.SetValue(1)		  
			Debug.SendAnimationEvent(PlayerRef, "unequipboots")	
			Utility.Wait(3.5)
			Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
			IDA_Glob.SetValue(0)			  
		elseif (akBaseObject.HasKeyword(ArmorCuirass)||akBaseObject.HasKeyword(ClothingBody)) && IDA_UndressBody.GetValue() == 1 || slotMask == 4 && IDA_UndressBody.GetValue() == 1   
			if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && !IDA_NoFirstPerson.GetValue()
				 Game.ForceThirdPerson()
			EndIf
			
			IDA_Glob.SetValue(1)		 
			Debug.SendAnimationEvent(PlayerRef, "unequipcuirass")	
			Utility.Wait(2.5)
			Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
			IDA_Glob.SetValue(0)		  
		elseif slotMask == 32 && IDA_UndressNeck.GetValue() == 1  
			if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
				 Game.ForceThirdPerson()
			EndIf 
			
			IDA_Glob.SetValue(1)		 
			Debug.SendAnimationEvent(PlayerRef, "unequipneck")	
			Utility.Wait(3.5)
			Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
			IDA_Glob.SetValue(0)			  
		elseif slotMask == 64 && IDA_UndressRing.GetValue() == 1  
			if PlayerRef.GetAnimationVariableInt("i1stPerson") == 1 && IDA_NoFirstPerson.GetValue()
				 Game.ForceThirdPerson()
			EndIf		 
			
			IDA_Glob.SetValue(1)		 
			Debug.SendAnimationEvent(PlayerRef, "equipring")	
			Utility.Wait(3.6)
			Debug.SendAnimationEvent(PlayerRef, "OffsetStop")
			IDA_Glob.SetValue(0)	  
		endif	 	 
	EndIf	
EndEvent
