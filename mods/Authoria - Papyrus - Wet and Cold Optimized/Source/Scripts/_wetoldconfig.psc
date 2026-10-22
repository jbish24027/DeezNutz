Scriptname _wetoldconfig extends activemagiceffect

Message Property _WetConfigColdMsg Auto
Message Property _WetConfigColdGearMsg Auto
Message Property _WetConfigMsg Auto
Message Property _WetConfigToggleMsg Auto
Message Property _WetConfigWetMsg Auto

_WetQuestScript Property _WetQuest Auto
_WetSkyUIConfig Property _WetSKConfigQuest Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
	If akTarget && _WetQuest && akTarget == _WetQuest.PlayerRef
		akTarget.RemoveSpell(_WetQuest._WetOldConfigSpell)
	EndIf
EndEvent
