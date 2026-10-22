Scriptname REQ_StaminaConsumption extends REQ_CoreScript
{wait for keypress events signaling player actions like jumping or attacking and emulate stamina usage}

Spell Property AttackCost Auto
Spell Property BlockCost Auto
Spell Property JumpCost Auto
Spell Property Dodge Auto

Spell Property BullRushCone Auto
Spell Property HorseChargeCone Auto

Spell Cone = None

; bull rush/trample related internal variables
Actor sprinter

; --- OStim scene compatibility (Authoria - Ostim tweaks and Patches) -----------------------------
; Requiem watches the Jump / Attack / Block / Sprint controls to emulate stamina costs, but those
; same keys are used to control an active OStim scene. While the player is in an OStim scene we skip
; the key-driven costs. OActor.IsInOStim is an OStim native (see OActor.psc); OStim is a hard
; dependency of this NSFW profile so the call is always bound. This is the OStim re-expression of the
; SexLab faction gate the personal SexLab list used (per RULES.md rule 5, port-only).
; --- end OStim scene compatibility --------------------------------------------------------------

Function RegisterKeys(Bool reregister)
	UnregisterForAllControls()
	UnregisterForAllMenus()
	If (reregister)
		RegisterForControl("Right Attack/Block")
		RegisterForControl("Left Attack/Block")
		RegisterForControl("Jump")
		RegisterForControl("Sprint")
		RegisterForMenu("Cursor Menu")
	EndIf
EndFunction

Event OnControlDown(String Control)

	If (!Utility.IsInMenuMode() && !OActor.IsInOStim(Player))
		If (Control == "sprint" ) ;Dodge moves and charge attacks
			GotoState("Working")
			If (Player.IsSprinting() || Player.IsOnMount())
				UnregisterForUpdate()
				If (Player.IsOnMount())
					Cone = HorseChargeCone
					sprinter = Game.FindClosestActor(Player.X, Player.Y, Player.Z - 200.0, 190.0) ;use the horse as sprinter
				Else
					Cone = BullRushCone
					sprinter = Player
				EndIf
				RegisterForSingleUpdate(2)
			ElseIf (!Player.HasMagicEffect(Dodge.GetNthEffectMagicEffect(0)) && Player.GetAV("Stamina") >= 15.0)
				Dodge.Cast(Player,Player)
			EndIf

			GotoState("")
		ElseIf (Control == "Jump")
			If (!Player.IsSwimming() && !Player.IsOnMount())
				Player.AddSpell(Jumpcost, False)
			EndIf
		ElseIf Control == "Right Attack/Block" && player.GetEquippedItemType(1) == 7
			Player.AddSpell(AttackCost, False)
		ElseIf Control == "Left Attack/Block" && player.GetAnimationVariableBool("Isblocking") ; RRO-207
			Player.AddSpell(BlockCost, False)
		EndIf
	EndIf
EndEvent

State Working
	Event OnControlDown(String Control)
	EndEvent
EndState

Event OnUpdate()
	If (sprinter.IsSprinting() && !sprinter.IsGhost())
		Cone.Cast(Player, None)
		RegisterForSingleUpdate(0.1)
	Else
		sprinter = None
		Cone = None
	EndIf
EndEvent

Event OnMenuClose(String MenuName)
	RegisterKeys(True)
EndEvent

Event OnPlayerLoadGame()
    parent.OnPlayerLoadGame()
	RegisterKeys(True)
EndEvent

Function shutdownScript(Int currentVersion, Int nevVersion)
	RegisterKeys(False)
EndFunction

Function initScript(Int currentVersion, Int nevVersion)
	RegisterKeys(True)
EndFunction
