Scriptname _wetequipsurvival extends activemagiceffect  

;====================================================================================

Form RandomWaterskin

Armor RandomBackpack

_WetQuestScript Property _WetQuest Auto

Bool Cleaned
Bool IsTraveler

Actor targ

;====================================================================================

Function Clean()
	If !Cleaned && targ
		Cleaned = True
		If RandomBackpack
			targ.RemoveItem(RandomBackpack)
		EndIf
		If RandomWaterskin
			targ.RemoveItem(RandomWaterskin)
		EndIf
		targ.RemoveFromFaction(_WetQuest._WetIsTravelerFaction)
		targ.RemoveSpell(_WetQuest._WetNPCEquipSurvivalSpell)
		GoToState("Dead")
	EndIf
EndFunction

;====================================================================================

Form Function PickForm(FormList SourceList, Int ListSize, Int ChanceMult = 1)
	If !SourceList || ListSize <= 0 || ChanceMult <= 0
		Return None
	EndIf
	Int iRandomIndex = Utility.RandomInt(1, ListSize * ChanceMult) - 1
	If iRandomIndex >= ListSize
		Return None
	EndIf
	Return SourceList.GetAt(iRandomIndex)
EndFunction

Function ChooseBackpack(FormList BackpackList, Int ListSize)
	If IsTraveler
		RandomBackpack = PickForm(BackpackList, ListSize, 2) as Armor
	Else
		RandomBackpack = PickForm(BackpackList, ListSize, 6) as Armor
	EndIf
	If RandomBackpack
		targ.AddItem(RandomBackpack)
		targ.EquipItem(RandomBackpack, true)
	EndIf
EndFunction

Function ChooseBackpackLeatherAdjust()
	Utility.Wait(1.0)
	Armor EquippedCloak
	If _WetQuest.SKSE64Installed
		EquippedCloak = targ.GetWornForm(0x00010000) as Armor
	EndIf
	If EquippedCloak && EquippedCloak.HasKeyword(_WetQuest.ArmorMaterialHide)
		ChooseBackpack(_WetQuest._WetBPLeatherFarList, _WetQuest.SurvLeatherBPFarSize)
	Else
		ChooseBackpack(_WetQuest._WetBPLeatherList, _WetQuest.SurvLeatherBPSize)
	EndIf
EndFunction

Function ChooseBackpackRoot()
	If _WetQuest.CampfireInstalled
		Int BagChance = Utility.RandomInt(1, 100)
		If !_WetQuest._WetBPFurList || _WetQuest.SurvFurBPSize <= 0
			ChooseBackpackLeatherAdjust()
		ElseIf _WetQuest.IsInCold
			If BagChance < 61
				ChooseBackpack(_WetQuest._WetBPFurList, _WetQuest.SurvFurBPSize)
			Else
				ChooseBackpackLeatherAdjust()
			EndIf
		Else
			If BagChance < 71
				ChooseBackpackLeatherAdjust()
			Else
				ChooseBackpack(_WetQuest._WetBPFurList, _WetQuest.SurvFurBPSize)
			EndIf
		EndIf
	Else
		ChooseBackpackLeatherAdjust()
	EndIf
EndFunction

Function ChooseWaterskin()
	If _WetQuest.WaterskinList && _WetQuest.WaterskinListSize > 0
		If IsTraveler
			RandomWaterskin = PickForm(_WetQuest.WaterskinList, _WetQuest.WaterskinListSize, 3)
		Else
			RandomWaterskin = PickForm(_WetQuest.WaterskinList, _WetQuest.WaterskinListSize, 6)
		EndIf
		If RandomWaterskin
			targ.AddItem(RandomWaterskin)
			If _WetQuest.WaterskinEquipSpell
				targ.AddSpell(_WetQuest.WaterskinEquipSpell)
			EndIf
		EndIf
	EndIf
EndFunction

;====================================================================================
 
Event OnEffectStart(Actor akTarget, Actor akCaster)
	targ = akTarget
	If targ.WornHasKeyword(_WetQuest.ClothingBody)
		targ.AddToFaction(_WetQuest._WetIsTravelerFaction)
		IsTraveler = True
	EndIf
	Utility.Wait(0.5)
	GoToState("Alive")
EndEvent

;====================================================================================

State Alive

	Event OnBeginState()
		;Actor PlayerRef = _WetQuest.PlayerRef
		;If PlayerRef.GetDistance(targ) as Int < 2048
		;	RegisterForSingleLOSLost(PlayerRef, targ)
		;Else
		;	OnLostLOS(PlayerRef, targ)
		;EndIf
		If targ
			If _WetQuest.SurvGearOn
				If _WetQuest.SurvBPOn
					If !_WetQuest.SKSE64Installed
						ChooseBackpackRoot()
					ElseIf !targ.GetWornForm(0x00020000)
						ChooseBackpackRoot()
					EndIf
				EndIf
				If _WetQuest.SurvModItemsOn
					ChooseWaterskin()
				EndIf
			EndIf
		EndIf
	EndEvent

	;Event OnLostLOS(Actor akViewer, ObjectReference akTarget)
	;	If targ
	;		If _WetQuest.SurvGearOn
	;			If _WetQuest.SurvBPOn
	;				If !_WetQuest.SKSE64Installed
	;					ChooseBackpackRoot()
	;				ElseIf !targ.GetWornForm(0x00020000)
	;					ChooseBackpackRoot()
	;				EndIf
	;			EndIf
	;			If _WetQuest.SurvModItemsOn
	;				ChooseWaterskin()
	;			EndIf
	;		EndIf
	;	EndIf
	;EndEvent

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
		targ.RemoveFromFaction(_WetQuest._WetIsTravelerFaction)
		GoToState("Dead")
	EndEvent

EndState

State Dead
EndState
