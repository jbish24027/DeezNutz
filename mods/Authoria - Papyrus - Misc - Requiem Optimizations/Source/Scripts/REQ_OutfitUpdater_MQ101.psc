Scriptname REQ_OutfitUpdater_MQ101 extends Actor
{Updates Ralof's and Hadvar's outfits once the Helgen tower Stormcloak is killed by Alduin.
ARR: guarded for Alternate Perspective alt-starts -- only runs for a genuine Helgen prisoner
start, never touches the player's gear, and is null/unloaded-safe so it cannot log
native-object errors.}

Actor   Property Hadvar          Auto
Actor   Property Ralof           Auto
Outfit  Property Outfit_Ralof    Auto
Outfit  Property Outfit_Hadvar   Auto
Armor   Property PrisonerClothes Auto
Armor   Property PrisonerBoots   Auto
Armor   Property PlayerRobe      Auto
Armor   Property PlayerBoots     Auto

Event OnDeath(Actor akKiller)
	; Genuine vanilla Helgen prisoner start only. On an Alternate Perspective alt-start the
	; player never carried prisoner rags, so do nothing -- and never alter the player's gear.
	Actor playerRef = Game.GetPlayer()
	If !playerRef || playerRef.GetItemCount(PrisonerClothes) == 0
		Return
	EndIf
	If Hadvar && Hadvar.Is3DLoaded()
		Hadvar.SetOutfit(Outfit_Hadvar)
	EndIf
	If Ralof && Ralof.Is3DLoaded()
		Ralof.SetOutfit(Outfit_Ralof)
	EndIf
EndEvent
