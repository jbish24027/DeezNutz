Scriptname IceWraithParticlesSCRIPT extends ActiveMagicEffect
{Particles to auto add to ice wraith}

;===============================================

import utility
import actor
import form
;===============================================
Actor selfRef
VisualEffect Property IceWraithParticles01 Auto
Armor Property SkinIceWraithSmokeFins Auto
VisualEffect Property FXIceWraith2ndFormEffect Auto

String Property GroundDiveIceHazard Auto
String Property ChangeForms Auto
Spell Property WallOfFrostIceWraith Auto

Float Property scaleRangeMax = 1.1 Auto
Float Property scaleRangeMin = 0.9 Auto
Explosion Property deathExplosion Auto
Activator Property AshPileObject Auto
{The object we use as a pile.}

Bool isSummoned = False
Bool isFinished = False
Bool setupComplete = False
Bool finsEquipped = False
Bool effectEnabled = False

Event OnEffectStart(Actor Target, Actor Caster)
	selfRef = caster
	isSummoned = False
	isFinished = False
	setupComplete = False
	finsEquipped = False
	effectEnabled = False

	If selfRef == None
		Return
	EndIf

	If selfRef.IsCommandedActor()
		isSummoned = True
	EndIf

	effectEnabled = True

	; Added by USKP to prevent this effect from appearing on the player.
	If selfRef == Game.GetPlayer()
		If IsEffectValid()
			Dispel()
		EndIf
		effectEnabled = False
		Return
	EndIf

	TrySetup()
EndEvent

Function TrySetup()
	If isFinished || setupComplete || !IsSetupSafe()
		Return
	EndIf

	If selfRef == Game.GetPlayer()
		Dispel()
		effectEnabled = False
		Return
	EndIf

	selfRef.SetScale(RandomFloat(scaleRangeMin, scaleRangeMax))
	IceWraithParticles01.Play(selfRef, -1)
	FXIceWraith2ndFormEffect.Play(selfRef, -1)
	selfRef.EquipItem(SkinIceWraithSmokeFins)
	finsEquipped = True

	If GroundDiveIceHazard
		RegisterForAnimationEvent(selfRef, GroundDiveIceHazard)
	EndIf

	If ChangeForms
		RegisterForAnimationEvent(selfRef, ChangeForms)
	EndIf

	setupComplete = True
EndFunction

Event OnEffectFinish(Actor akTarget, Actor akCaster)
	isFinished = True
	effectEnabled = False
	CleanupFX()
EndEvent

Function CleanupFX()
	If selfRef == None
		Return
	EndIf

	If selfRef.Is3DLoaded()
		IceWraithParticles01.Stop(selfRef)
		FXIceWraith2ndFormEffect.Stop(selfRef)
	EndIf

	If finsEquipped
		selfRef.UnEquipItem(SkinIceWraithSmokeFins)
		finsEquipped = False
	EndIf
EndFunction

Event OnAnimationEvent(ObjectReference akSource, string asEventName)
	If selfRef == None || !selfRef.Is3DLoaded()
		Return
	EndIf

	If asEventName == GroundDiveIceHazard
		WallOfFrostIceWraith.Cast(selfRef)
	EndIf

	If asEventName == ChangeForms
		selfRef.PlaySubGraphAnimation("SkinFadeOut")
		Wait(2.0)
		If selfRef != None && selfRef.Is3DLoaded()
			selfRef.PlaySubGraphAnimation("SkinFadeIn")
		EndIf
	EndIf
EndEvent

Event OnDying(Actor myKiller)
	CleanupFX()

	If selfRef == None
		Return
	EndIf

	; Summoned ice wraiths should not drop lootable ice piles.
	If isSummoned
		Return
	EndIf

	If !selfRef.Is3DLoaded()
		Return
	EndIf

	selfRef.PlaceAtMe(deathExplosion)

	selfRef.SetCriticalStage(selfRef.CritStage_DisintegrateStart)
	selfRef.AttachAshPile(AshPileObject)
	selfRef.SetAlpha(0.0, True)
	Wait(1.0)
	selfRef.SetCriticalStage(selfRef.CritStage_DisintegrateEnd)
EndEvent

Bool Function IsSetupSafe()
	If !IsEffectValid() || selfRef == None || !selfRef.IsEnabled() || selfRef.IsDead() || !selfRef.Is3DLoaded()
		Return False
	EndIf

	Cell parentCell = selfRef.GetParentCell()
	If parentCell == None || !parentCell.IsAttached()
		Return False
	EndIf

	Return True
EndFunction

Bool Function IsEffectValid()
	If !effectEnabled
		Return False
	EndIf

	If !Self || StringUtil.Find(Self as String, "<None>") >= 0
		effectEnabled = False
		Return False
	EndIf

	If GetTargetActor() == None
		effectEnabled = False
		Return False
	EndIf

	Return True
EndFunction
