Scriptname eeeHorseSpellScript extends activemagiceffect

GlobalVariable Property Saddles Auto
GlobalVariable Property HorseProtected Auto
GlobalVariable Property HorseConfidence Auto

Keyword Property ArmorHorseSaddle Auto
Keyword Property ConfidenceIgnored Auto
Keyword Property ProtectedIgnored Auto

Outfit Property NakedHorseOutfit Auto

Actor thisHorseRef = None

Float DefaultConfidence

Event OnInit()
	RegisterForMenu("Journal Menu")
EndEvent

Event OnEffectStart(Actor akTarget, Actor akCaster)
	thisHorseRef = akTarget
	DefaultConfidence = thisHorseRef.GetActorValue("Confidence")
	CheckSaddle()
	SetProtected()
	SetConfidence()
EndEvent

Event OnMenuClose(String MenuName)
	If MenuName == "Journal Menu" && thisHorseRef
		SetProtected()
		SetConfidence()
	EndIf
EndEvent

Event OnPackageChange(Package akOldPackage)
	SetProtected()
EndEvent

Event OnEffectFinish(Actor akTarget, Actor akCaster)
	If thisHorseRef && thisHorseRef != None && !thisHorseRef.IsDead() && HorseConfidence.GetValue() < 5 && !thisHorseRef.HasKeyword(ConfidenceIgnored)
		Spell FRH_Spell = Game.GetFormFromFile(0x00A,"Followers Ride Horses.esp") as Spell
		If FRH_Spell && thisHorseRef.HasSpell(FRH_Spell)
			Return
		EndIf
		thisHorseRef.SetActorValue("Confidence", DefaultConfidence)
	EndIf
EndEvent

Event OnItemAdded(Form akBaseItem, int aiItemCount, ObjectReference akItemReference, ObjectReference akSourceContainer)
	If Saddles.GetValue() as Bool && akBaseItem.HasKeyword(ArmorHorseSaddle)
		Outfit thisHorseOutfit = thisHorseRef.GetLeveledActorBase().GetOutfit()
		Armor EquippedSaddle = thisHorseOutfit.getNthPart(0) as Armor
		If thisHorseOutfit != NakedHorseOutfit
			thisHorseRef.RemoveItem(EquippedSaddle)
		EndIf
		thisHorseRef.EquipItem(akBaseItem,true)
	EndIf
EndEvent

Event OnDying(Actor akKiller)
	If akKiller
		Debug.Notification(thisHorseRef.GetDisplayName()+" was killed by "+akKiller.GetDisplayName())
	else
		Debug.Notification(thisHorseRef.GetDisplayName()+" died.")
	EndIf
	Dispel()
EndEvent

Function SetProtected() 
	If !thisHorseRef.HasKeyword(ProtectedIgnored)
		If !(thisHorseRef.IsDead() || thisHorseRef.IsGhost() || thisHorseRef.IsEssential() || thisHorseRef.GetLeveledActorBase().IsInvulnerable())
			thisHorseRef.GetLeveledActorBase().SetProtected(HorseProtected.GetValue() as Bool)
		EndIf
	EndIf
EndFunction

Function SetConfidence()
	If thisHorseRef && thisHorseRef != None && !thisHorseRef.IsDead()
		If !thisHorseRef.HasKeyword(ConfidenceIgnored) && HorseConfidence.GetValue() < 5
			Spell FRH_Spell = Game.GetFormFromFile(0x00A,"Followers Ride Horses.esp") as Spell
			If FRH_Spell && thisHorseRef.HasSpell(FRH_Spell)
				Return
			EndIf
			thisHorseRef.SetActorValue("Confidence", HorseConfidence.GetValue())
		EndIf
	EndIf
EndFunction

Function CheckSaddle()
	; Authoria: only strip the outfit saddle when the Saddles toggle is ON (same test OnItemAdded uses).
	; With Saddles OFF nothing re-equips the saddle, so stripping it left horses bare.
	If Saddles.GetValue() as Bool
		Outfit thisHorseOutfit = thisHorseRef.GetLeveledActorBase().GetOutfit()
		If thisHorseOutfit != NakedHorseOutfit && thisHorseOutfit.GetNumParts() == 1
			Armor currentSaddle = thisHorseOutfit.getNthPart(0) as Armor
			If currentSaddle.HasKeyword(ArmorHorseSaddle)
				thisHorseRef.SetOutfit(NakedHorseOutfit)
				thisHorseRef.AddItem(currentSaddle)
			EndIf
		EndIf
	EndIf
EndFunction