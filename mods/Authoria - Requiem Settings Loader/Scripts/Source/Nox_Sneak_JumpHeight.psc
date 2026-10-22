Scriptname Nox_Sneak_JumpHeight Extends ActiveMagicEffect



Perk	Property	Acrobatics	Auto
Perk	Property	Stealth		Auto

Float	HeightDefault = 76.0



Function UpdateJumpHeight()

	If (Game.GetPlayer().HasPerk(Acrobatics))
		Game.SetGameSettingFloat("fJumpHeightMin", HeightDefault * (1.0 + Game.GetPlayer().GetActorValue("Sneak") / 100.0) * 1.5)

	ElseIf (Game.GetPlayer().HasPerk(Stealth))
		Game.SetGameSettingFloat("fJumpHeightMin", HeightDefault * (1.0 + Game.GetPlayer().GetActorValue("Sneak") / 100.0))

	Else
		Game.SetGameSettingFloat("fJumpHeightMin", HeightDefault)
	EndIf

EndFunction



Event OnInit()
	RegisterForMenu("StatsMenu")
	; Authoria fix: take the base jump height from MCM Helper storage, never from the live
	; game setting - the live setting can already hold a sneak-boosted value when this effect
	; is re-added on save load, which compounded the boost into HeightDefault.
	Float storedBase = MCM.GetModSettingFloat("Requiem", "fJumpHeightMin:General")
	If (storedBase > 0.0)
		HeightDefault = storedBase
	Else
		HeightDefault = 76.0
	EndIf
	UpdateJumpHeight()
EndEvent

Event OnPlayerLoadGame()
	UpdateJumpHeight()
EndEvent

Event OnMenuClose(string menu)
	UpdateJumpHeight()
EndEvent
