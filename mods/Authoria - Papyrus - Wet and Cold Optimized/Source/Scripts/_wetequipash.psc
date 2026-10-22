Scriptname _wetequipash extends activemagiceffect  

;====================================================================================

Armor RandomCover
Armor RandomGoggles

GlobalVariable Property _WetIsAshStorm Auto

_WetQuestScript Property _WetQuest Auto

Bool Property IsAshStorm Auto
Bool NoCover
Bool NoGoggles
Bool Cleaned

Actor targ

;====================================================================================

Function Clean()
	If !Cleaned && targ
		Cleaned = True
		;Armor[] wornArmor = GetWornArmor(targ)
		If RandomCover
			targ.RemoveItem(RandomCover)
		EndIf
		If RandomGoggles
			targ.RemoveItem(RandomGoggles)
		EndIf
		;ReequipArmor(targ, wornArmor)
		targ.RemoveSpell(_WetQuest._WetNPCEquipAshSpell)
		GoToState("Dead")
	EndIf
EndFunction


Function AshChecks()
	If _WetQuest.FaceCoversOn
		If !_WetQuest.SKSE64Installed
			If !targ.WornHasKeyword(_WetQuest.ArmorHelmet)
				NoCover = True
			EndIf
		ElseIf !targ.GetWornForm(0x00001000) && !targ.GetWornForm(0x00004000)
			NoCover = True
		EndIf
	EndIf
	If _WetQuest.GogglesOn
		If !_WetQuest.SKSE64Installed
			If !targ.WornHasKeyword(_WetQuest.ArmorHelmet)
				NoGoggles = True
			EndIf
		ElseIf !targ.GetWornForm(0x04000000)
			NoGoggles = True
		EndIf
	EndIf
	If NoCover || NoGoggles
		GoToState("Alive")
	EndIf
EndFunction

;====================================================================================

Armor Function PickArmor(FormList SourceList, Int ListSize)
	If !SourceList || ListSize <= 0
		Return None
	EndIf
	Int iRandomIndex = Utility.RandomInt(1, ListSize) - 1
	Return SourceList.GetAt(iRandomIndex) as Armor
EndFunction

Function ChooseFaceCover()
	RandomCover = PickArmor(_WetQuest._WetFaceCoverAshList, _WetQuest.AshFaceCoverSize)
	If RandomCover
		targ.AddItem(RandomCover)
		targ.EquipItem(RandomCover, true)
	EndIf
EndFunction

Function ChooseGoggles()
	FormList GogglesList
	Int iIndex
	Int GoggleChance = Utility.RandomInt(1, 30)
	If GoggleChance < 8
		GogglesList = _WetQuest._WetGogglesChitinList
		iIndex = _WetQuest.AshGogglesChitinSize
	ElseIf GoggleChance < 11
		GogglesList = _WetQuest._WetGogglesDwemerList
		iIndex = _WetQuest.AshGogglesDwemerSize
	EndIf
	If GogglesList
		RandomGoggles = PickArmor(GogglesList, iIndex)
		If RandomGoggles
			targ.AddItem(RandomGoggles)
			targ.EquipItem(RandomGoggles, true)
		EndIf
	EndIf
EndFunction

;====================================================================================
 
Event OnEffectStart(Actor akTarget, Actor akCaster)
	targ = akTarget
	If IsAshStorm
		GoToState("IsAshStorm")
	Else
		If !_WetQuest.AshFollowersOnly
			If !_WetQuest.FollowerAshOn
				If !targ.IsPlayerTeammate()
					AshChecks()
				EndIf
			Else
				AshChecks()
			EndIf
		ElseIf targ.IsPlayerTeammate()
			AshChecks()
		EndIf
	EndIf
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
			If NoCover
				ChooseFaceCover()
			EndIf
			If NoGoggles
				ChooseGoggles()
			EndIf
		EndIf
	EndEvent

	;Event OnLostLOS(Actor akViewer, ObjectReference akTarget)
	;	
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
		GoToState("Dead")
	EndEvent

EndState

;====================================================================================

State IsAshStorm

	Event OnBeginState()
		_WetIsAshStorm.SetValue(1)
	EndEvent

	Event OnEffectFinish(Actor akTarget, Actor akCaster)
		_WetIsAshStorm.SetValue(0)
	EndEvent

EndState

State Dead
EndState
