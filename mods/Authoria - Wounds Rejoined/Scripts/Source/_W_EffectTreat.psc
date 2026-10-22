Scriptname _W_EffectTreat extends activemagiceffect  

_W_QuestScript Property libs Auto

Event OnEffectStart(Actor akTarget, Actor akCaster)
	libs.TreatWounds()
endEvent