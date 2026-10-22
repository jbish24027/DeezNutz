Scriptname WEPrisonerAliasScript extends ReferenceAlias  

;This script pops a message box when activating the prisoner
;if player frees, adds captors, himself, and prisoner to factions to make people hate each other
;You should make sure elsewhere that the captors have aggression high enough to attack their enemies


Topic Property WESharedDialoguePrisonerSetFree Auto

idle Property OffsetBoundStandingStart Auto
idle Property OffsetStop  Auto

Message Property WEPrisonerMessageBox Auto
Faction Property WEPrisonerFreedFaction Auto

Faction Property WEPrisonerFreedCombatCaptorFaction Auto
Faction Property WEPrisonerFreedCombatPrisonerFaction Auto

ReferenceAlias Property Captor1 Auto
ReferenceAlias Property Captor2 Auto
ReferenceAlias Property Captor3 Auto
ReferenceAlias Property Captor4 Auto
ReferenceAlias Property Captor5 Auto

bool bound = True

int iDoNothing = 0
int iSetFree = 1
int iSetFreeShareItems = 2


Event OnLoad()
	if bound
		GetActorReference().playIdle(OffsetBoundStandingStart)
		GetActorReference().BlockActivation(true)
	EndIf

EndEvent

Event OnActivate(ObjectReference akActionRef)

	if GetActorReference().IsDead() ;|| GetActorReference().IsinCombat()
; 		debug.trace(self + "OnActivate() IsDead() or IsInCombat() so not showing message box")	
	
	Elseif Bound == true	
; 		debug.trace(self + "OnActivate() will call show message box")	
		Actor ActorRef = GetActorReference()

		int result = WEPrisonerMessageBox.show()

		if result == iDoNothing
			;debug.Notification("DO NOTHING")
			
		elseif result == iSetFree
			;debug.Notification("SET FREE")	
			FreePrisoner(ActorRef, OpenInventory = False)
			
		elseif result == iSetFreeShareItems
			;debug.Notification("SET FREE SHARE ITEMS")	
			FreePrisoner(ActorRef, OpenInventory = True)		
		EndIf
	
	EndIf
EndEvent

Event OnHit(objectReference akAggressor, Form akSource, Projectile akProjectile, bool abPowerAttack, bool abSneakAttack, bool abBashAttack, bool abHitBlocked)
	if AkAggressor == game.getPlayer()
		Game.GetPlayer().AddToFaction(WEPrisonerFreedCombatPrisonerFaction)
		;TryToAddToFaction(WEPrisonerFreedCombatPrisonerFaction)
		; If checks to validate properties added by USKP 1.2.6 because they were throwing Papyrus errors and aborting the function.
		if( Captor1 )
			Captor1.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
		EndIf
		if( Captor2 )
			Captor2.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
		EndIf
		if( Captor3 )
			Captor3.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
		EndIf
		if( Captor4 )
			Captor4.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
		endif
		if( Captor5 )
			Captor5.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
		EndIf
	endif
endEvent


Function FreePrisoner(Actor ActorRef, bool playerIsLiberator= true, bool OpenInventory = False)
; 	debug.trace(self + "FreePrisoner(" + ActorRef + "," + playerIsLiberator + ", " + OpenInventory +")")	

	if OpenInventory
		ActorRef.openInventory(True)
		while Utility.IsInMenuMode() ; for SkyrimSouls
		endwhile
	EndIf
	
	if playerIsLiberator
		ActorRef.StopCombat()
	endif

	Actor playerRef = Game.GetPlayer()

	ActorRef.AddToFaction(WEPrisonerFreedFaction)
	ActorRef.AddToFaction(WEPrisonerFreedCombatPrisonerFaction)
	ActorRef.EvaluatePackage()
	ActorRef.PlayIdle(OffsetStop) ; USKP 2.0.1 - The property is defined for this purpose but was never used. Free his hands!
	if playerIsLiberator
		playerRef.AddToFaction(WEPrisonerFreedCombatPrisonerFaction)
		ActorRef.SetPlayerTeammate(true, false)
	EndIf
	
	if playerIsLiberator || (Captor1 && Captor1.GetActorReference().GetKiller() == playerRef) || (Captor2 && Captor2.GetActorReference().GetKiller() == playerRef) \
	|| (Captor3 && Captor3.GetActorReference().GetKiller() == playerRef) || (Captor4 && Captor4.GetActorReference().GetKiller() == playerRef) \
	|| (Captor5 && Captor5.GetActorReference().GetKiller() == playerRef)
		ActorRef.Say(WESharedDialoguePrisonerSetFree)
	endif
	bound = False
	ActorRef.BlockActivation(false)
	
	; Ifchecks to validate properties added by USKP 1.2.6 because they were throwing Papyrus errors and aborting the function.
	if( Captor1 )
		Captor1.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor2 )
		Captor2.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor3 )
		Captor3.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor4 )
		Captor4.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor5 )
		Captor5.TryToAddToFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	
	ActorRef.EvaluatePackage()

	WECrimeFactionAliasScript crimeFactionScript = (Self as ReferenceAlias) as WECrimeFactionAliasScript
	if crimeFactionScript
		crimeFactionScript.SetCrimeFaction()
	endif

EndFunction

Function ClearFactions()
;call when quest shuts down
; 	debug.trace(self + "FreePrisoner")

	Game.GetPlayer().RemoveFromFaction(WEPrisonerFreedCombatPrisonerFaction)
	GetActorReference().SetPlayerTeammate(false, false)

	TryToRemoveFromFaction(WEPrisonerFreedCombatCaptorFaction)
	; Ifchecks to validate properties added by USKP 1.2.6 because they were throwing Papyrus errors and aborting the function.
	if( Captor1 )
		Captor1.TryToRemoveFromFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor2 )
		Captor2.TryToRemoveFromFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor3 )
		Captor3.TryToRemoveFromFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor4 )
		Captor4.TryToRemoveFromFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf
	if( Captor5 )
		Captor5.TryToRemoveFromFaction(WEPrisonerFreedCombatCaptorFaction)
	EndIf

EndFunction
