Scriptname _WetNPCSPID_Script extends ActiveMagicEffect  

;====================================================================================

_WetQuestScript Property _WetQuest Auto

Bool Property GearColdFX Auto
Bool Property GearColdChildFX Auto
Bool Property GearRainFX Auto
Bool Property GearSurvFX Auto
Bool Property GearAshFX Auto
Bool Property NPCFX Auto
Bool Property NPCColdFX Auto
Bool Property NPCColdDeadFX Auto
Bool Property NPCRainFX Auto

Actor targ

;====================================================================================

Function Clean()
	targ.RemoveSpell(_WetQuest._WetNPCEquipColdChildSpell)
	targ.RemoveSpell(_WetQuest._WetNPCEquipColdSpell)
	targ.RemoveSpell(_WetQuest._WetNPCEquipRainSpell)
	targ.RemoveSpell(_WetQuest._WetNPCEquipSurvivalSpell)
	targ.RemoveSpell(_WetQuest._WetNPCEquipAshSpell)
	GoToState("Nothing")
EndFunction

;====================================================================================
 
Event OnEffectStart(Actor Target, Actor Caster)
	targ = Target
	If targ
		If !_WetQuest.ModUpdated
			If NPCFX || NPCColdFX || NPCColdDeadFX || NPCRainFX
				GoToState("Nothing")
			ElseIf GearColdFX
				GoToState("GearColdFX")
			ElseIf GearColdChildFX
				GoToState("GearColdChildFX")
			ElseIf GearRainFX
				GoToState("GearRainFX")
			ElseIf GearSurvFX
				GoToState("GearSurvFX")
			ElseIf GearAshFX
				GoToState("GearAshFX")
			EndIf
		Else
			Clean()
		EndIf
	EndIf
EndEvent

;====================================================================================

State GearColdFX

	Event OnBeginState()
		targ.AddSpell(_WetQuest._WetNPCEquipColdSpell)
		GoToState("Nothing")
	EndEvent

EndState

State GearColdChildFX

	Event OnBeginState()
		targ.AddSpell(_WetQuest._WetNPCEquipColdChildSpell)
		GoToState("Nothing")
	EndEvent

EndState

State GearRainFX

	Event OnBeginState()
		targ.AddSpell(_WetQuest._WetNPCEquipRainSpell)
		GoToState("Nothing")
	EndEvent

EndState

State GearSurvFX

	Event OnBeginState()
		targ.AddSpell(_WetQuest._WetNPCEquipSurvivalSpell)
		GoToState("Nothing")
	EndEvent

EndState

State GearAshFX

	Event OnBeginState()
		targ.AddSpell(_WetQuest._WetNPCEquipAshSpell)
		GoToState("Nothing")
	EndEvent

EndState

State Nothing
EndState
