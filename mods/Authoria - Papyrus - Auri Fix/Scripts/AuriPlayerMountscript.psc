Scriptname AuriPlayerMountScript extends ReferenceAlias
;=====================================================================================
;              							PROPERTIES                  					 
;=====================================================================================	
import Game
import Utility 

Actor Property Auri Auto
Actor Property Player auto
Actor Property ThistlefootRef Auto

Faction Property CurrentFollowerFaction Auto

GlobalVariable Property AuriOnMount Auto
GlobalVariable property AuriShouldRideMount auto

ObjectReference Property ThistlefootReturnMarker Auto

bool Property Dismounting Auto

;=====================================================================================
;              							FUNCTIONS                  					 
;=====================================================================================
Function AuriMount()
	If Auri.GetDistance(ThistleFootRef) > 1650 || !(ThistleFootRef.Is3DLoaded())
		ThistlefootRef.Enable()	
		Float AngleZ = Auri.GetAngleZ()
		ThistleFootRef.MoveTo(Auri, 128.0 * Math.Sin(AngleZ), 128.0 * Math.Cos(AngleZ), 0.0, true)
	EndIf
	AuriShouldRideMount.SetValue(1)	
	Auri.EvaluatePackage()
	ThistlefootRef.EvaluatePackage()
	AuriOnMount.SetValue(1)
EndFunction

Function AuriDismount()	
	AuriShouldRideMount.SetValue(0)
	Auri.EvaluatePackage()
	ThistlefootRef.EvaluatePackage()
	AuriOnMount.SetValue(0)
	Auri.Dismount()
	Wait(2)
	Actor PlayerRef = ResolvePlayerRef()
	If (PlayerRef != None) && ((!PlayerRef.IsSneaking()) && (Auri.IsSneaking())) ;this is a failsafe for edge cases where Auri may get stuck sneaking
		Auri.StartSneaking()
	EndIf
EndFunction

Actor Function ResolvePlayerRef()
	Actor PlayerRef = Self.GetActorRef()
	If PlayerRef == None
		PlayerRef = Player
	EndIf
	If PlayerRef == None
		PlayerRef = GetPlayer()
	EndIf
	Return PlayerRef
EndFunction

Function Setup()
	Actor PlayerRef = ResolvePlayerRef()
	If PlayerRef != None
		RegisterForAnimationEvent(PlayerRef, "tailHorseMount")
  		RegisterForAnimationEvent(PlayerRef, "tailHorseDismount")
  		RegisterForAnimationEvent(PlayerRef, "HorseExitOut")
		RegisterForAnimationEvent(PlayerRef, "JumpLandEnd")
	EndIf
	
	If (GetModByName("AmazingFollowerTweaks.esp") != 255)
		Faction TweakIgnoreFaction = GetFormFromFile(0x141763, "AmazingFollowerTweaks.esp") as Faction
		If (TweakIgnoreFaction != none)
			If !(Auri.IsInFaction(TweakIgnoreFaction))
				Auri.AddToFaction(TweakIgnoreFaction)
			EndIf
		EndIf
	EndIf
	
	If (GetModByName("Convenient Horses.esp") != 255)
		Faction CHHorseFaction = GetFormFromFile(0x6FD0C, "Convenient Horses.esp") as Faction
		If (CHHorseFaction != none)
			If Auri.IsInFaction (CHHorseFaction)
				Auri.RemoveFromFaction(CHHorseFaction)
			EndIf
		EndIf
	EndIf
	
	If (GetModByName("ConvenientHorses_BlackList.esp") != 255)
		Faction CHBlacklistFaction = GetFormFromFile(0x00000800, "ConvenientHorses_BlackList.esp") as Faction
		If (CHBlacklistFaction != None)
			If !(Auri.IsInFaction(CHBlacklistFaction))
				Auri.AddToFaction(CHBlacklistFaction)
			EndIf
		EndIf
	EndIf
	
	If (GetModByName("nwsFollowerFramework.esp") != 255)
		Faction NoHorseFaction = GetFormFromFile(0x153FBE, "nwsFollowerFramework.esp") as Faction
		If (NoHorseFaction != none)
			If !(Auri.isInFaction(NoHorseFaction))
				Auri.AddToFaction(NoHorseFaction)
			EndIf
		EndIf
	EndIf
EndFunction
;=====================================================================================
;              							EVENTS                  					 
;=====================================================================================
Event OnAnimationEvent (ObjectReference akSource, string asEventName)
	Actor PlayerRef = ResolvePlayerRef()
	If (PlayerRef != None) && (akSource == PlayerRef) && (Auri.IsInFaction(CurrentFollowerFaction))
		If asEventName == "tailHorseMount"
			AuriMount()
		Else 
			Debug.Trace(asEventName + " Dismounting=" + Dismounting)
				If Dismounting
					If (asEventName == "HorseExitOut" || asEventName == "JumpLandEnd")
						;Debug.Trace("Make Auri Dismount")
						Wait(3)
						Auri.EvaluatePackage()
						Dismounting = false
						;Debug.Trace("Evaluate Auri package and Dismounting set to false")
					EndIf
				EndIf
				If asEventName == "tailHorseDismount"
					Dismounting = true
					;Debug.Trace("Dismounting set to true")
				EndIf
				;If asEventName = "HorseExitOut"
					;Wait(3)
				;EndIf
				AuriDismount()
		EndIf
	EndIf
	
	;If (akSource == Self.GetActorRef()) && (asEventName == "tailHorseMount") && (Auri.IsInFaction(CurrentFollowerFaction)) && (AuriOnMount.GetValue() == 0))
		;AuriMount()
	;ElseIf ((akSource == Self.GetActorRef()) && (asEventName == "tailHorseDismount") && (Auri.IsInFaction(CurrentFollowerFaction)) && (AuriOnMount.GetValue() == 1))
		;AuriDismount()
    ;EndIf
EndEvent

Event OnPlayerLoadGame()
	Setup()
	Actor PlayerRef = ResolvePlayerRef()
	If ((Auri.IsInFaction(CurrentFollowerFaction)) && (PlayerRef != None) && (PlayerRef.IsOnMount()) && (AuriShouldRideMount.GetValue() == 0))
    	AuriMount()
 	EndIf
EndEvent

Event OnPlayerFastTravelEnd(float afTravelGameTimeHours)
	Actor PlayerRef = ResolvePlayerRef()
	If Auri.IsInFaction(CurrentFollowerFaction)
		If !Auri.IsOnMount()
			AuriShouldRideMount.SetValue(0)
		EndIf
		Auri.Disable()
		Wait(1)
		Auri.Enable()
		If (PlayerRef != None) && PlayerRef.IsOnMount() && !Auri.IsOnMount()
			AuriMount()
		EndIf
		Auri.EvaluatePackage()
	EndIf
EndEvent

Event OnInit()
	Dismounting = False
    Setup()
EndEvent
