Scriptname _wetequipcold extends activemagiceffect  

;====================================================================================

Armor RandomHood
Armor RandomGloves
Armor RandomCloak
Armor RandomFaceCover

Race tRace

_WetQuestScript Property _WetQuest Auto

Bool Property Cold Auto
;Bool InVanillaColdTimed
Bool Cleaned
Bool IsTraveler
Bool IsNord
Bool NoCloak
Bool NoHood
Bool NoGloves
Bool NoFaceCover

Int CurrentTime
Int IsBlizzard

Form UnequippedItem

Actor targ

;====================================================================================

Function Clean()
	If !Cleaned && targ
		Cleaned = True
		;Armor[] wornArmor = GetWornArmor(targ)
		If RandomHood
			targ.RemoveItem(RandomHood)
			;targ.RemoveFromFaction(_WetQuest._WetColdHoodFaction)
		EndIf
		If RandomGloves
			targ.RemoveItem(RandomGloves)
			;targ.RemoveFromFaction(_WetQuest._WetColdGloveFaction)
		EndIf
		If RandomCloak
			targ.RemoveItem(RandomCloak)
			;targ.RemoveFromFaction(_WetQuest._WetColdCloakFaction)
		EndIf
		If RandomFaceCover
			targ.RemoveItem(RandomFaceCover)
			;targ.RemoveFromFaction(_WetQuest._WetColdFaceCoversFaction)
		EndIf
		;ReequipArmor(targ, wornArmor)
		targ.RemoveSpell(_WetQuest._WetNPCEquipColdSpell)
		GoToState("Dead")
	EndIf
EndFunction

;====================================================================================		EFF compatibility, credits to bluedanieru

;Armor[] Function GetWornArmor(Actor target)
	;If _WetQuest.EFFInstalled && _WetQuest.FollowerColdOn
		;Armor[] wornForms = new Armor[30]
		;int index
		;int slotsChecked
		;slotsChecked += 0x00100000
		;slotsChecked += 0x00200000 ;ignore reserved slots
		;slotsChecked += 0x80000000
	 
		;int thisSlot = 0x01
		;while (thisSlot < 0x80000000)
			;if (Math.LogicalAnd(slotsChecked, thisSlot) != thisSlot) ;only check slots we haven't found anything equipped on already
				;Armor thisArmor = target.GetWornForm(thisSlot) as Armor
				;if (thisArmor)
					;wornForms[index] = thisArmor
					;index += 1
					;slotsChecked += thisArmor.GetSlotMask() ;add all slots this item covers to our slotsChecked variable
				;else ;no armor was found on this slot
					;slotsChecked += thisSlot
				;endif
			;endif
			;thisSlot *= 2 ;double the number to move on to the next slot
		;endWhile
		;return wornForms
	;EndIf
;EndFunction

;Function ReequipArmor(Actor target, Armor[] wornArmor)
	;If _WetQuest.EFFInstalled && _WetQuest.FollowerColdOn
		;int index = 0
		;while(index < 30 && wornArmor[index])
			;if(target.GetItemCount(wornArmor[index]) > 0 && !target.isEquipped(wornArmor[index]))
				;target.equipItem(wornArmor[index])
			;endif
			;index += 1
		;endWhile
	;EndIf
;EndFunction

;====================================================================================

Armor Function PickArmor(FormList SourceList, Int ListSize, Int ChanceMult = 1)
	If !SourceList || ListSize <= 0 || ChanceMult <= 0
		Return None
	EndIf
	Int iRandomIndex = Utility.RandomInt(1, ListSize * ChanceMult) - 1
	If iRandomIndex >= ListSize
		Return None
	EndIf
	Return SourceList.GetAt(iRandomIndex) as Armor
EndFunction

Function NordRaceCheck()
	If (tRace != _WetQuest.NordRace && tRace != _WetQuest.NordRaceVampire) || _WetQuest._WetIsBlizzarding.GetValue() as Int == 1
	ElseIf NoCloak
		IsNord = True
	EndIf
	GoToState("Cold")
EndFunction

Function ColdChecks()
	tRace = targ.GetRace()
	If _WetQuest.DGSnowElf && tRace == _WetQuest.DGSnowElf as Race
	Else
		If _WetQuest.SKSE64Installed
			If _WetQuest.ColdHoodsOn && !targ.GetWornForm(0x00000002)
				NoHood = True
			EndIf
			If _WetQuest.ColdCloaksOn && !targ.IsEquipped(_WetQuest._WetCloakClippingArmorList) && !targ.GetWornForm(0x00010000)
				NoCloak = True
			EndIf
		EndIf
		If _WetQuest.ColdGlovesOn
			If !_WetQuest.SKSE64Installed
				If !targ.WornHasKeyword(_WetQuest.ArmorGauntlets) && !targ.WornHasKeyword(_WetQuest.ClothingHands)
					NoGloves = True
				EndIf
			ElseIf !targ.GetWornForm(0x00000008)
				NoGloves = True
			EndIf
		EndIf
		If _WetQuest.ColdCoversOn
			If !_WetQuest.SKSE64Installed
				If !targ.WornHasKeyword(_WetQuest.ArmorHelmet)
					NoFaceCover = True
				EndIf
			ElseIf !targ.GetWornForm(0x00001000) && !targ.GetWornForm(0x00004000)
				NoFaceCover = True
			EndIf
		EndIf
		If NoFaceCover || NoHood || NoGloves || NoCloak
			CurrentTime = _WetQuest.CurrentTime
;			InVanillaColdTimed = _WetQuest.InVanillaColdTimed
			If _WetQuest.ExcludeNords
				If CurrentTime > 6 && CurrentTime < 20
					NordRaceCheck()
				;ElseIf InVanillaColdTimed
				;	NordRaceCheck()
				Else
					GoToState("Cold")
				EndIf
			;ElseIf InVanillaColdTimed
			;	NordRaceCheck()
			;Else
			;	GoToState("Cold")
			EndIf
		EndIf
	EndIf
EndFunction

;====================================================================================			Cold Gear Functions

Function ChooseHood()
	Int EquipChance = 1
	If IsNord && !_WetQuest._WetIsBlizzarding.GetValue() as Int == 1
		EquipChance = 2
	EndIf
	If _WetQuest.WiCInstalled
		If targ.WornHasKeyword(_WetQuest.ClothingBody)
			RandomHood = PickArmor(_WetQuest._WetHoodColdList, _WetQuest.ColdHoodSize, EquipChance)
		ElseIf RandomFaceCover
			RandomHood = PickArmor(_WetQuest._WetHoodColdList, _WetQuest.ColdHoodSize, EquipChance)
		Else
			RandomHood = PickArmor(_WetQuest._WetHoodColdArmoredList, _WetQuest.ColdHoodArmoredSize, 2 * EquipChance)
			If !RandomHood
				RandomHood = PickArmor(_WetQuest._WetHoodColdList, _WetQuest.ColdHoodSize, EquipChance)
			EndIf
		EndIf
	Else
		RandomHood = PickArmor(_WetQuest._WetHoodColdList, _WetQuest.ColdHoodSize, EquipChance)
	EndIf
	If RandomHood
		targ.AddItem(RandomHood)
		targ.EquipItem(RandomHood, true)
		;targ.AddToFaction(_WetQuest._WetColdHoodFaction)
	EndIf
EndFunction

Function ChooseHoodChild()
	RandomHood = PickArmor(_WetQuest._WetHoodColdChildList, _WetQuest.ColdHoodChildSize)
	If RandomHood
		targ.AddItem(RandomHood)
		targ.EquipItem(RandomHood, true)
		;targ.AddToFaction(_WetQuest._WetColdHoodFaction)
	EndIf
EndFunction

Function ChooseCloak()
	If RandomHood && RandomHood.HasKeyWord(_WetQuest._WetIsScarf)
		Return
	EndIf
	If IsNord
		RandomCloak = PickArmor(_WetQuest._WetCloakColdList, _WetQuest.ColdCloakSize, 5)
	Else
		RandomCloak = PickArmor(_WetQuest._WetCloakColdList, _WetQuest.ColdCloakSize)
	EndIf
	If RandomCloak
		targ.AddItem(RandomCloak)
		targ.EquipItem(RandomCloak, true)
		;targ.AddToFaction(_WetQuest._WetColdCloakFaction)
	EndIf
EndFunction

Function ChooseGloves()
	RandomGloves = PickArmor(_WetQuest._WetGlovesList, _WetQuest.ColdGlovesSize)
	If RandomGloves
		targ.AddItem(RandomGloves)
		targ.EquipItem(RandomGloves, true)
		;targ.AddToFaction(_WetQuest._WetColdGloveFaction)
	EndIf
EndFunction

Function ChooseFaceCover()
	Int EquipChance
	If targ.IsInFaction(_WetQuest._WetIsTravelerFaction)
		IsTraveler = True
	EndIf
	If _WetQuest._WetIsBlizzarding.GetValue() as Int == 1
		If CurrentTime > 6 && CurrentTime < 20
			If IsTraveler
				EquipChance = 2
			Else
				EquipChance = 3
			EndIf
		Else
			EquipChance = 1
		EndIf
	Else
		If CurrentTime > 6 && CurrentTime < 20
			If IsTraveler
				EquipChance = 4
			Else
				EquipChance = 8
			EndIf
		Else
			If IsTraveler
				EquipChance = 2
			Else
				EquipChance = 4
			EndIf
		EndIf
	EndIf
	If EquipChance > 0
		RandomFaceCover = PickArmor(_WetQuest._WetFaceCoverColdList, _WetQuest.ColdFaceCoverSize, EquipChance)
		If RandomFaceCover
			targ.AddItem(RandomFaceCover)
			targ.EquipItem(RandomFaceCover, true)
			;targ.AddToFaction(_WetQuest._WetColdFaceCoversFaction)
		EndIf
	EndIf
EndFunction

;====================================================================================
 
Event OnEffectStart(Actor akTarget, Actor akCaster)
	targ = akTarget
	If Cold
		If !_WetQuest.ColdFollowersOnly
			If !_WetQuest.FollowerColdOn
				If !targ.IsPlayerTeammate()
					ColdChecks()
				EndIf
			Else
				ColdChecks()
			EndIf
		ElseIf targ.IsPlayerTeammate()
			ColdChecks()
		EndIf
	ElseIf !_WetQuest.ColdFollowersOnly && _WetQuest.ColdHoodsOn && !targ.WornHasKeyword(_WetQuest.ArmorHelmet) && !targ.WornHasKeyword(_WetQuest.ClothingHead)
		If _WetQuest.SKSE64Installed
			If !targ.GetWornForm(0x00000002)
				GoToState("ColdChild")
			EndIf
		Else
			GoToState("ColdChild")
		EndIf
	EndIf
EndEvent

Event OnCellDetach()
	Clean()
EndEvent

Event OnUnload()
	Clean()
EndEvent

Event OnDetachedFromCell()
	Clean()
EndEvent

Event OnEffectFinish(Actor akTarget, Actor akCaster)
	Clean()
EndEvent

Event OnDying(Actor akKiller)
	Cleaned = True
	;If targ
	;	targ.RemoveFromFaction(_WetQuest._WetColdHoodFaction)
	;	targ.RemoveFromFaction(_WetQuest._WetColdGloveFaction)
	;	targ.RemoveFromFaction(_WetQuest._WetColdCloakFaction)
	;	targ.RemoveFromFaction(_WetQuest._WetColdFaceCoversFaction)
	;EndIf
	GoToState("Dead")
EndEvent

;====================================================================================

State Cold

	Event OnBeginState()
		Actor PlayerRef = _WetQuest.PlayerRef
		;If (_WetQuest.RecentlyChangedLoc || PlayerRef.GetDistance(targ) as Int > 2048)
		;	OnLostLOS(PlayerRef, targ)
		;Else
		;	RegisterForSingleLOSLost(PlayerRef, targ)
		;EndIf

		If targ
			;Armor[] wornArmor = GetWornArmor(targ)
			;If !InVanillaColdTimed
			;	If NoFaceCover && !IsNord
			;		ChooseFaceCover()
			;	EndIf
			;	If NoHood
			;		ChooseHood()
			;	EndIf
			;	If NoCloak && targ.GetSitState() as Int == 0
			;		ChooseCloak()
			;	EndIf
			;ElseIf !IsNord && NoHood
			;	ChooseHood()
			;EndIf
			If NoFaceCover && !IsNord
				ChooseFaceCover()
			EndIf
			If !IsNord && NoHood
				ChooseHood()
			EndIf
			If NoGloves
				ChooseGloves()
			EndIf
			If NoCloak && targ.GetSitState() as Int == 0
				ChooseCloak()
			EndIf			
			;ReequipArmor(targ, wornArmor)
		EndIf
	EndEvent

	;Event OnLostLOS(Actor akViewer, ObjectReference akTarget)
	;	
	;EndEvent

EndState

;====================================================================================

State ColdChild

	Event OnBeginState()
		Actor PlayerRef = _WetQuest.PlayerRef
		If PlayerRef.GetDistance(targ) as Int < 2048
			RegisterForSingleLOSLost(PlayerRef, targ)
		Else
			OnLostLOS(PlayerRef, targ)
		EndIf
	EndEvent

	Event OnLostLOS(Actor akViewer, ObjectReference akTarget)
		If targ
			;Armor[] wornArmor = GetWornArmor(targ)
			ChooseHoodChild()
			;ReequipArmor(targ, wornArmor)
		EndIf
	EndEvent

EndState

State Dead
EndState
