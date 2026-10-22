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



Event OnEffectStart(Actor akTarget, Actor akCaster)
	; self is NOT bound when REQ_MCM re-applies this ability during load/init -> ONLY global Game.* here.
	; HeightDefault is read from fJumpHeightMin, which REQ_MCM sets to the configured base right before
	; AddSpell -- preserving the MCM "set base -> readd -> rescale" contract.
	HeightDefault = Game.GetGameSettingFloat("fJumpHeightMin")
	UpdateJumpHeight()
EndEvent

Event OnPlayerLoadGame()
	; self IS bound here -> safe for the SKSE menu registration; also REQUIRED (registrations clear on load).
	RegisterForMenu("StatsMenu")
	UpdateJumpHeight()
EndEvent

Event OnMenuClose(string menu)
	If (menu == "StatsMenu")
		UpdateJumpHeight()
	EndIf
EndEvent
