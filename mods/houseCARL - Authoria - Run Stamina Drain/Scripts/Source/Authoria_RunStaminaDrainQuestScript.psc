Scriptname Authoria_RunStaminaDrainQuestScript extends Quest
{Applies a small stamina drain when the player sustains full-run movement speed.}

Float Property SpeedThreshold = 300.0 Auto
Float Property DrainPerSecond = 1.25 Auto
Float Property CheckInterval = 0.5 Auto
Float Property MinStamina = 1.0 Auto
Bool Property IgnoreSneaking = True Auto
Bool Property IgnoreSwimming = True Auto
Bool Property IgnoreSprinting = True Auto

Actor PlayerRef
Float LastX
Float LastY
Bool HasSample = False

Event OnInit()
	PlayerRef = Game.GetPlayer()
	TakeSample()
	RegisterForSingleUpdate(GetSafeInterval())
EndEvent

Event OnUpdate()
	Float interval = GetSafeInterval()

	If PlayerRef == None
		PlayerRef = Game.GetPlayer()
	EndIf

	If ShouldDrain(interval)
		Float stamina = PlayerRef.GetActorValue("Stamina")
		If stamina > MinStamina
			PlayerRef.DamageActorValue("Stamina", DrainPerSecond * interval)
		EndIf
	EndIf

	RegisterForSingleUpdate(interval)
EndEvent

Float Function GetSafeInterval()
	If CheckInterval < 0.1
		Return 0.1
	EndIf

	Return CheckInterval
EndFunction

Bool Function ShouldDrain(Float afInterval)
	If PlayerRef == None
		Return False
	EndIf

	If IgnoreSneaking && PlayerRef.IsSneaking()
		TakeSample()
		Return False
	EndIf

	If IgnoreSwimming && PlayerRef.IsSwimming()
		TakeSample()
		Return False
	EndIf

	If IgnoreSprinting && PlayerRef.IsSprinting()
		TakeSample()
		Return False
	EndIf

	If PlayerRef.IsOnMount()
		TakeSample()
		Return False
	EndIf

	If PlayerRef.GetSitState() != 0
		TakeSample()
		Return False
	EndIf

	Float currentX = PlayerRef.GetPositionX()
	Float currentY = PlayerRef.GetPositionY()

	If !HasSample
		LastX = currentX
		LastY = currentY
		HasSample = True
		Return False
	EndIf

	Float dx = currentX - LastX
	Float dy = currentY - LastY
	Float thresholdDistance = SpeedThreshold * afInterval
	Float distanceSquared = (dx * dx) + (dy * dy)
	Float thresholdSquared = thresholdDistance * thresholdDistance

	LastX = currentX
	LastY = currentY

	If distanceSquared >= thresholdSquared
		Return True
	EndIf

	Return False
EndFunction

Function TakeSample()
	If PlayerRef != None
		LastX = PlayerRef.GetPositionX()
		LastY = PlayerRef.GetPositionY()
		HasSample = True
	EndIf
EndFunction
